# Text2SQL - Natural Language to SQL Query Converter

[![GitHub Stars](https://img.shields.io/github/stars/dhananjaylab/cml-app?style=social)](https://github.com/dhananjaylab/cml-app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

A full-stack application that converts natural language questions into SQL commands using Large Language Models (LLMs) and modern Python web frameworks. Perfect for democratizing database access and reducing SQL learning curves.

## 🎯 Features

- **Natural Language Processing**: Convert plain English questions into SQL queries instantly
- **Multi-Database Support**: HR, Banking, Music, and Waterfall sample databases
- **FastAPI Backend**: High-performance RESTful API for query conversion and execution
- **Streamlit Frontend**: Intuitive interactive chat interface for end-users
- **RAG Architecture**: FAISS vector search for intelligent document indexing and semantic understanding
- **OpenAI Integration**: Powered by GPT-4o-mini for accurate SQL generation
- **Query Execution**: Direct SQL execution with result display
- **Error Handling**: Comprehensive error messages and query validation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Oracle Database (or compatible SQL database)
- OpenAI API key
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/dhananjaylab/cml-app.git
cd cml-app

# Install dependencies
pip install -r 0_session-install-dependencies/requirements.txt
```

### Configuration

Set the following environment variables:

```bash
export OPENAI_API_KEY=sk-your-api-key-here
export OPENAI_CHAT_MODEL=gpt-4o-mini
export HR_USER=HR
export HR_PASSWORD=your_password
export HR_DSN=your_db_host:1521/XEPDB1
```

### Running the Application

```bash
# Terminal 1: Start the FastAPI backend
cd 3_app-run-python-script
python app.py --host 127.0.0.1 --port 8000

# Terminal 2: Start the Streamlit frontend
streamlit run app.py --server.port 8501 --server.address 127.0.0.1
```

Visit:
- **Frontend**: http://127.0.0.1:8501
- **API Docs**: http://127.0.0.1:8000/docs

## 📁 Project Structure

```
cml-app/
├── 0_session-install-dependencies/
│   ├── install-dependencies.py      # Dependency installer
│   └── requirements.txt              # Python package dependencies
├── 3_app-run-python-script/
│   ├── app.py                        # FastAPI & Streamlit application
│   └── utils/
│       ├── llm_handler.py           # LLM integration
│       ├── database.py              # Database connectivity
│       └── vector_search.py         # FAISS vector search
├── docs/
│   └── ARCHITECTURE.md              # System architecture documentation
├── README.md                         # This file
├── CONTRIBUTING.md                  # Contribution guidelines
├── .gitignore                        # Git ignore rules
├── catalog-entry.yaml               # Project metadata
└── LICENSE                          # MIT License
```

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | Streamlit, Altair |
| **LLM** | OpenAI GPT-4o-mini |
| **Vector DB** | FAISS |
| **Database** | Oracle Database, SQLAlchemy |
| **Data Processing** | Pandas, NumPy, PyArrow |
| **Language** | Python 3.10+ |

## 📝 Usage Examples

### Via REST API

```bash
curl -X POST "http://127.0.0.1:8000/api/text-to-sql" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show me all employees in the sales department",
    "database": "HR"
  }'
```

### Via Streamlit UI

1. Open http://127.0.0.1:8501
2. Select database schema
3. Type your question in natural language
4. Click "Generate SQL"
5. View generated SQL and execute results

## 🔧 Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Formatting

```bash
black . --line-length 88
isort .
flake8 .
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and components
- [Contributing](CONTRIBUTING.md) - How to contribute
- [API Reference](#) - Detailed API documentation

## 🐛 Known Issues & Limitations

- Currently supports Oracle Database (PostgreSQL/MySQL support planned)
- Requires valid OpenAI API key for LLM functionality
- RAG performance depends on vector database size and query complexity

## 🚧 Roadmap

- [ ] Support for PostgreSQL and MySQL
- [ ] Local LLM support (Ollama, LLaMA)
- [ ] Advanced query optimization
- [ ] Query execution history and caching
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] Cloud deployment guides (AWS, GCP, Azure)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Dhananjay**
- GitHub: [@dhananjaylab](https://github.com/dhananjaylab)
- Connect for AI/ML, Database, and Full-Stack projects

## ⭐ Show Your Support

If you found this project helpful, please star the repository! Your support motivates continued development.

## 📧 Support

For issues, questions, or suggestions, please [open an issue](https://github.com/dhananjaylab/cml-app/issues) on GitHub.