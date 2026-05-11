"""PDF Solution Book Analyzer - RAG-based learning system"""

import os
from typing import Dict, List, Optional, Tuple
import PyPDF2
import pdfplumber
from pathlib import Path
from datetime import datetime

try:
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI
except ImportError:
    print("Warning: LangChain components not fully available")


class PDFAnalyzer:
    """Analyzes PDF solution books and teaches from them using RAG."""
    
    def __init__(self, vector_store_path: str = "./vector_store"):
        """Initialize PDF analyzer.
        
        Args:
            vector_store_path: Path to store vector embeddings
        """
        self.vector_store_path = vector_store_path
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.documents = {}
        self.vector_stores = {}
        self.metadata = {}
        
        # Create vector store directory if it doesn't exist
        Path(vector_store_path).mkdir(parents=True, exist_ok=True)
    
    def extract_pdf_content(self, pdf_path: str) -> Dict:
        """Extract text and metadata from PDF.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted content and metadata
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pages_content = []
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    tables = page.extract_tables()
                    pages_content.append({
                        "page": page_num + 1,
                        "text": text,
                        "tables": tables
                    })
                
                return {
                    "file": pdf_path,
                    "total_pages": len(pdf.pages),
                    "pages": pages_content,
                    "extracted_at": datetime.now().isoformat()
                }
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def index_pdf(self, pdf_path: str, subject: str = "General") -> Dict:
        """Index PDF for semantic search using FAISS.
        
        Args:
            pdf_path: Path to PDF file
            subject: Subject of the PDF (Math, Science, etc.)
            
        Returns:
            Indexing status and metadata
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Extract content
            content = self.extract_pdf_content(pdf_path)
            
            # Create embeddings and vector store
            embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            all_texts = []
            for page in content["pages"]:
                if page["text"]:
                    chunks = text_splitter.split_text(page["text"])
                    all_texts.extend(chunks)
            
            # Create vector store
            vector_store = FAISS.from_texts(
                texts=all_texts,
                embedding=embeddings
            )
            
            # Store for later use
            doc_id = Path(pdf_path).stem
            self.documents[doc_id] = content
            self.vector_stores[doc_id] = vector_store
            self.metadata[doc_id] = {
                "file": pdf_path,
                "subject": subject,
                "indexed_at": datetime.now().isoformat(),
                "pages": content["total_pages"],
                "chunks": len(all_texts)
            }
            
            return {
                "status": "success",
                "document_id": doc_id,
                "subject": subject,
                "pages": content["total_pages"],
                "chunks_created": len(all_texts),
                "indexed_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def search_solutions(self, query: str, doc_id: Optional[str] = None, top_k: int = 5) -> List[Dict]:
        """Search for relevant solutions in indexed PDFs.
        
        Args:
            query: Search query
            doc_id: Specific document to search (None = search all)
            top_k: Number of results to return
            
        Returns:
            List of relevant solution snippets
        """
        results = []
        
        search_docs = {doc_id: self.vector_stores[doc_id]} if doc_id and doc_id in self.vector_stores else self.vector_stores
        
        for doc, vector_store in search_docs.items():
            try:
                docs = vector_store.similarity_search(query, k=top_k)
                for doc_result in docs:
                    results.append({
                        "document": doc,
                        "content": doc_result.page_content,
                        "subject": self.metadata[doc].get("subject", "General")
                    })
            except Exception as e:
                print(f"Error searching {doc}: {str(e)}")
        
        return results[:top_k]
    
    def teach_from_solution(self, question: str, doc_id: Optional[str] = None) -> Dict:
        """Teach the student using solutions from PDFs.
        
        Args:
            question: Student's question
            doc_id: Specific document to use (None = search all)
            
        Returns:
            Teaching explanation based on PDF solutions
        """
        # Search for relevant solutions
        solutions = self.search_solutions(question, doc_id, top_k=3)
        
        if not solutions:
            return {
                "status": "no_solutions_found",
                "question": question,
                "message": "No relevant solutions found in the indexed PDFs"
            }
        
        # Generate teaching explanation
        solution_context = "\n\n".join([
            f"Solution from {s['subject']}:\n{s['content']}"
            for s in solutions
        ])
        
        llm = ChatOpenAI(model_name="gpt-4", openai_api_key=self.api_key)
        
        prompt = f"""
Based on the following solution materials, explain how to answer this question:

Question: {question}

Solution Materials:
{solution_context}

Provide:
1. Step-by-step explanation
2. Key concepts from the solutions
3. How to apply this to similar problems
4. Why this approach works
"""
        
        explanation = llm.predict(text=prompt)
        
        return {
            "status": "success",
            "question": question,
            "explanation": explanation,
            "sources": len(solutions),
            "source_subjects": list(set([s["subject"] for s in solutions])),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_indexed_documents(self) -> List[Dict]:
        """Get list of all indexed documents.
        
        Returns:
            List of indexed document metadata
        """
        return [
            {"id": doc_id, **metadata}
            for doc_id, metadata in self.metadata.items()
        ]
    
    def remove_document(self, doc_id: str) -> Dict:
        """Remove a document from the index.
        
        Args:
            doc_id: Document ID to remove
            
        Returns:
            Removal status
        """
        if doc_id not in self.documents:
            return {"status": "error", "message": "Document not found"}
        
        del self.documents[doc_id]
        del self.vector_stores[doc_id]
        del self.metadata[doc_id]
        
        return {
            "status": "success",
            "removed_document": doc_id,
            "timestamp": datetime.now().isoformat()
        }