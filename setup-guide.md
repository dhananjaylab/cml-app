# Quick Setup Guide

## Prerequisites

- Python 3.10+
- pip package manager
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/dhananjaylab/cml-app.git
cd cml-app
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r 0_session-install-dependencies/requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_CHAT_MODEL=gpt-4o-mini

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
```

Or export directly:
```bash
export OPENAI_API_KEY=sk-your-api-key-here
export OPENAI_CHAT_MODEL=gpt-4o-mini
```

### 5. Run the Application

**Option A: Run FastAPI Backend Only**
```bash
cd 3_app-run-python-script
python app.py --api
```
API will be available at: http://127.0.0.1:8000/docs

**Option B: Run Streamlit Frontend Only**
```bash
cd 3_app-run-python-script
streamlit run app.py
```
Frontend will be available at: http://127.0.0.1:8501

**Option C: Run Both (Recommended)**

Terminal 1:
```bash
cd 3_app-run-python-script
python app.py --api
```

Terminal 2:
```bash
cd 3_app-run-python-script
streamlit run app.py
```

Then visit http://127.0.0.1:8501

## Development

### Code Formatting
```bash
pip install black isort flake8
black . --line-length 88
isort .
flake8 .
```

### Testing
```bash
pip install pytest pytest-cov
pytest tests/ -v
```

## Project Structure

```
cml-app/
├── 0_session-install-dependencies/
│   ├── install-dependencies.py
│   └── requirements.txt
├── 3_app-run-python-script/
│   └── app.py                    # Main application
├── docs/
│   └── ARCHITECTURE.md           # System architecture
├── README.md                      # Project overview
├── CONTRIBUTING.md               # Contribution guidelines
├── setup-guide.md               # This file
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
└── catalog-entry.yaml            # Project metadata
```

## Troubleshooting

**Issue: "OPENAI_API_KEY not set"**
- Make sure to set the environment variable before running the app
- Check: `echo $OPENAI_API_KEY`

**Issue: "Module not found"**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Issue: Port already in use**
- Change port: `python app.py --api --port 8001`
- Or kill process: `lsof -ti:8000 | xargs kill -9`

**Issue: Streamlit can't connect to API**
- Make sure FastAPI backend is running first
- Check API is accessible: `curl http://127.0.0.1:8000/health`

## API Endpoints

### Text to SQL
```bash
curl -X POST "http://127.0.0.1:8000/api/text-to-sql" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show all employees in sales",
    "database": "HR"
  }'
```

### Execute Query
```bash
curl -X POST "http://127.0.0.1:8000/api/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "sql": "SELECT * FROM EMPLOYEES",
    "database": "HR"
  }'
```

### Get Databases
```bash
curl http://127.0.0.1:8000/api/databases
```

### Get Schema
```bash
curl http://127.0.0.1:8000/api/schemas/HR
```

### Health Check
```bash
curl http://127.0.0.1:8000/health
```

## Next Steps

- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Check [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Review [README.md](README.md) for full documentation

## Support

For issues, please open a GitHub issue or refer to the main README.
