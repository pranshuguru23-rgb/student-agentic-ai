"""Intelligent Tutor Agent - Main tutoring AI"""

import os
from typing import Dict, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from datetime import datetime


class TutorAgent:
    """AI tutor that adapts to student learning style and pace."""
    
    DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        """Initialize tutor agent.
        
        Args:
            model: OpenAI model to use
            temperature: Creativity level (0-1)
        """
        self.model = model
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.llm = ChatOpenAI(
            model_name=model,
            temperature=temperature,
            openai_api_key=self.api_key
        )
        
        self.memory = ConversationBufferMemory()
        self.current_difficulty = "intermediate"
        self.session_history = []
        self.student_profile = {}
        
    def set_difficulty(self, level: str) -> None:
        """Set learning difficulty level.
        
        Args:
            level: 'beginner', 'intermediate', or 'advanced'
        """
        if level not in self.DIFFICULTY_LEVELS:
            raise ValueError(f"Difficulty must be one of {self.DIFFICULTY_LEVELS}")
        self.current_difficulty = level
    
    def answer_question(self, question: str, subject: str = "General") -> Dict:
        """Answer a student's question with adaptive explanation.
        
        Args:
            question: Student's question
            subject: Subject area
            
        Returns:
            Dictionary with answer, explanation, follow-up suggestions
        """
        difficulty_guide = {
            "beginner": "Explain in very simple terms, use analogies, avoid technical jargon",
            "intermediate": "Provide balanced explanation with some technical depth",
            "advanced": "Deep technical explanation with mathematical proofs and advanced concepts"
        }
        
        prompt = f"""
You are an expert tutor in {subject}. The student is at {self.current_difficulty} level.
{difficulty_guide[self.current_difficulty]}

Student Question: {question}

Provide:
1. Direct Answer (2-3 sentences)
2. Detailed Explanation (with examples if relevant)
3. Key Concepts to Remember (bullet points)
4. Follow-up Topics to Explore (2-3 suggestions)
5. Practice Problem (similar to the question)
"""
        
        response = self.llm.predict(text=prompt)
        
        result = {
            "question": question,
            "subject": subject,
            "difficulty": self.current_difficulty,
            "answer": response,
            "timestamp": datetime.now().isoformat()
        }
        
        self.session_history.append(result)
        return result
    
    def generate_practice_problems(self, topic: str, count: int = 3) -> List[Dict]:
        """Generate practice problems for a topic.
        
        Args:
            topic: Topic to practice
            count: Number of problems to generate
            
        Returns:
            List of practice problems with solutions
        """
        prompt = f"""
Generate {count} practice problems for {topic} at {self.current_difficulty} level.

For each problem, provide:
1. Problem Statement
2. Hints (2-3 hints)
3. Solution
4. Explanation of Solution
"""
        
        response = self.llm.predict(text=prompt)
        
        return {
            "topic": topic,
            "difficulty": self.current_difficulty,
            "count": count,
            "problems": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def explain_concept(self, concept: str, subject: str = "General") -> Dict:
        """Explain a complex concept in detail.
        
        Args:
            concept: Concept to explain
            subject: Subject area
            
        Returns:
            Detailed explanation with examples
        """
        prompt = f"""
Explain the concept of \"{concept}\" in {subject} at {self.current_difficulty} level.

Include:
1. Definition
2. Historical Context (if applicable)
3. Real-world Applications
4. Visual Description (if applicable)
5. Common Misconceptions
6. Examples and Analogies
7. Connection to Other Concepts
"""
        
        response = self.llm.predict(text=prompt)
        
        return {
            "concept": concept,
            "subject": subject,
            "difficulty": self.current_difficulty,
            "explanation": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def assess_understanding(self, topic: str) -> Dict:
        """Assess student understanding of a topic through questions.
        
        Args:
            topic: Topic to assess
            
        Returns:
            Assessment questions and evaluation guide
        """
        prompt = f"""
Create a brief assessment for {topic} at {self.current_difficulty} level.

Include:
1. 3 Multiple Choice Questions
2. 1 Short Answer Question
3. 1 Application Problem

For each question provide:
- Question
- Options (for MC)
- Correct Answer
- Explanation
- What it tests
"""
        
        response = self.llm.predict(text=prompt)
        
        return {
            "topic": topic,
            "difficulty": self.current_difficulty,
            "assessment": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_session_summary(self) -> Dict:
        """Get summary of current tutoring session.
        
        Returns:
            Session statistics and progress
        """
        return {
            "session_length": len(self.session_history),
            "topics_covered": list(set([h.get("subject") for h in self.session_history])),
            "difficulty_level": self.current_difficulty,
            "history": self.session_history,
            "timestamp": datetime.now().isoformat()
        }
    
    def clear_session(self) -> None:
        """Clear session history and memory."""
        self.session_history = []
        self.memory.clear()
        self.student_profile = {}