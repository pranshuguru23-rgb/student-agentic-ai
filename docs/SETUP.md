# Setup Guide - Student Agentic AI

## Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/pranshuguru23-rgb/student-agentic-ai
cd student-agentic-ai
```

### 2. Set Up Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get it from: https://platform.openai.com/api-keys
```

### 3. Install Dependencies
```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Interactive Mode
```bash
python -m src.cli.main interactive
```

## Available Commands

### Ask a Question
```bash
python -m src.cli.main ask "What is photosynthesis?" --subject Science --difficulty intermediate
```

### Upload PDF Solution Book
```bash
python -m src.cli.main upload-pdf path/to/solutions.pdf --subject Mathematics
```

### Ask About PDFs
```bash
python -m src.cli.main ask-pdf "How do I solve this?"
```

### Create a Task
```bash
python -m src.cli.main add-task "Homework" "Math" --hours 2 --days 3 --priority high
```

### Generate Study Schedule
```bash
python -m src.cli.main schedule "Math" --days 7 --hours 2
```

### View Today's Plan
```bash
python -m src.cli.main today
```

### Check Progress
```bash
python -m src.cli.main progress
```

## Requirements

- Python 3.9+
- OpenAI API key
- Internet connection

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you've created `.env` file
- Add your OpenAI API key to `.env`

### "Module not found"
- Ensure you're in the correct directory
- Reinstall dependencies: `pip install -r requirements.txt`

### "PDF upload fails"
- Check file path is correct
- Ensure PDF file is readable
- File size should be under 50MB

## Next Steps

- Read [Architecture Guide](ARCHITECTURE.md) for system design
- Check [Deployment Guide](DEPLOYMENT.md) for Azure setup
- Explore [API Reference](API.md) for advanced usage