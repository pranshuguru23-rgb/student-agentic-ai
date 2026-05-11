"""SQLite database initialization and management"""

import sqlite3
from pathlib import Path
from datetime import datetime


class StudentAIDatabase:
    """SQLite database for Student Agentic AI."""
    
    def __init__(self, db_path: str = "student_ai.db"):
        """Initialize database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                subject TEXT,
                description TEXT,
                priority TEXT,
                deadline TEXT,
                duration_hours REAL,
                status TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Learning Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                student_id TEXT,
                subject TEXT,
                started_at TEXT,
                ended_at TEXT,
                duration_minutes INTEGER
            )
        """)
        
        # PDF Documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pdf_documents (
                id TEXT PRIMARY KEY,
                filename TEXT,
                subject TEXT,
                file_path TEXT,
                indexed_at TEXT,
                total_pages INTEGER,
                chunks INTEGER
            )
        """)
        
        # Session History table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_history (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                question TEXT,
                answer TEXT,
                subject TEXT,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_task(self, task_data: dict):
        """Add a task to database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (id, title, subject, description, priority, deadline, duration_hours, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_data['id'],
            task_data['title'],
            task_data['subject'],
            task_data.get('description', ''),
            task_data.get('priority', 'medium'),
            task_data.get('deadline'),
            task_data.get('duration_hours', 1.0),
            task_data.get('status', 'pending'),
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_tasks(self):
        """Get all tasks from database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        
        conn.close()
        return tasks
    
    def add_pdf_document(self, doc_data: dict):
        """Add PDF document metadata to database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO pdf_documents (id, filename, subject, file_path, indexed_at, total_pages, chunks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_data['id'],
            doc_data['filename'],
            doc_data.get('subject', 'General'),
            doc_data['file_path'],
            datetime.now().isoformat(),
            doc_data.get('total_pages', 0),
            doc_data.get('chunks', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def get_indexed_pdfs(self):
        """Get all indexed PDF documents."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM pdf_documents")
        pdfs = cursor.fetchall()
        
        conn.close()
        return pdfs