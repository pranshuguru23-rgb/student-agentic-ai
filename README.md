# 🎓 Student Agentic AI - Intelligent Tutor System

An advanced AI-powered tutoring platform that combines intelligent tutoring, PDF solution book analysis, personalized study scheduling, and task management. Deploy locally via CLI or scale on Microsoft Azure.

## ✨ Key Features

### 🤖 Intelligent Tutoring System
- Multi-subject support (Math, Science, English, History, etc.)
- Adaptive learning difficulty levels
- Real-time question answering with detailed explanations
- Multi-turn conversations with memory
- Progress tracking and performance analytics
- Learning style personalization

### 📚 PDF Solution Book Analysis
- Extract and analyze content from solution books
- Semantic indexing and vector embeddings
- Retrieval-Augmented Generation (RAG) for accurate teaching
- Match student questions to relevant solutions
- Generate teaching explanations from solution methodologies
- Support for equations, diagrams, and complex content

### 📅 Smart Study Scheduling
- Personalized study plan generation
- Intelligent task prioritization
- Conflict detection and optimization
- Adaptive re-scheduling based on progress
- Smart reminders and notifications
- Schedule visualization and management

### ✅ Task Management
- Create, categorize, and prioritize tasks
- Deadline tracking with smart reminders
- Completion status tracking
- Task-schedule integration
- Productivity analytics
- Overdue task notifications

## 🚀 Deployment Options

### Local CLI (Quick Start)
```bash
pip install -r requirements.txt
python -m src.cli.main interactive
```

### Docker
```bash
docker-compose up
```

### Microsoft Azure
- Azure Functions (serverless)
- Azure Blob Storage (PDFs)
- Azure Cosmos DB (scalable data)
- GitHub Actions CI/CD pipeline

## 📖 Documentation

- [Setup Guide](docs/SETUP.md) - Quick start instructions
- [Deployment Guide](docs/DEPLOYMENT.md) - Azure deployment
- [Architecture](docs/ARCHITECTURE.md) - System design
- [API Reference](docs/API.md) - REST API docs
- [Features](docs/FEATURES.md) - Detailed features

## 🛠️ Technology Stack

- **AI/ML**: LangChain, OpenAI GPT-4
- **PDF Processing**: PyPDF2, pdfplumber
- **Vector Search**: FAISS (local), Azure Cognitive Search (cloud)
- **Database**: SQLite (local), Cosmos DB (Azure)
- **CLI**: Click, Rich, Typer
- **Cloud**: Azure Functions, Blob Storage, Cosmos DB
- **CI/CD**: GitHub Actions
- **Testing**: pytest

## 🎯 Quick Commands

```bash
# Ask a question
ask: What is photosynthesis?

# Upload PDF solution book
upload-pdf: /path/to/solutions.pdf

# Generate study schedule
schedule: Math - 2 weeks, 2 hours/day

# Add a task
add-task: Complete calculus homework - Due tomorrow

# View schedule
view-schedule

# Check progress
check-progress
```

## 📦 Project Structure

```
student-agentic-ai/
├── src/
│   ├── agents/           # AI agents (tutor, PDF analyzer, scheduler)
│   ├── models/           # Data models
│   ├── database/         # Database layer
│   ├── utils/            # Utility functions
│   ├── cli/              # CLI interface
│   └── azure/            # Azure cloud functions
├── tests/                # Test suite
├── docs/                 # Documentation
├── docker/               # Docker configs
└── azure/                # Azure deployment
```

## 🔐 Environment Setup

Create a `.env` file:
```
OPENAI_API_KEY=your_api_key
AZURE_CONNECTION_STRING=your_connection_string
DATABASE_URL=sqlite:///student_ai.db
```

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines.

## 📞 Support

For issues and questions, please open a GitHub issue.

---

**Made with ❤️ for students everywhere**