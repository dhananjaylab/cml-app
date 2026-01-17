# Text2SQL - Architecture Documentation

## 📋 Overview

Text2SQL is a full-stack application that demonstrates modern AI/ML architecture for converting natural language queries into SQL commands. It showcases integration of LLMs, vector databases, and traditional SQL databases.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface                          │
│              Streamlit Web Application                      │
│         (Chat Interface, Query Results Display)             │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
├─────────────────────────────────────────────────────────────┤
│  • REST API Endpoints                                       │
│  • Request Validation (Pydantic)                            │
│  • Query Processing & Orchestration                         │
│  • Error Handling & Logging                                 │
└────────┬──────────────┬──────────────┬──────────────────────┘
         │              │              │
         ▼              ▼              ▼
   ┌──────────┐  ┌──────────────┐  ┌────────────┐
   │   LLM    │  │ Vector Store │  │ SQL Engine │
   │ Handler  │  │  (FAISS)     │  │(SQLAlchemy)|
   │          │  │              │  │            │
   │OpenAI    │  │ Embeddings   │  │ Oracle DB  │
   │GPT-4o    │  │ + Metadata   │  │            │
   └──────────┘  └──────────────┘  └────────────┘
```

## 🔄 Data Flow

### 1. Query Processing Pipeline

```
User Input (Natural Language)
    │
    ▼
┌─────────────────────────────────┐
│  Streamlit Frontend             │
│  - Accept user question         │
│  - Select database schema       │
│  - Display previous context     │
└────────────────┬────────────────┘
                 │
                 ▼
         ┌───────────────────┐
         │ FastAPI Backend   │
         │ - Validate input  │
         │ - Log request     │
         └─────────┬─────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ RAG Pipeline         │
        │ 1. Embed question    │
        │ 2. Search vectors    │
        │ 3. Retrieve context  │
        └──────────┬───────────┘
                   │
                   ▼
         ┌──────────────────────┐
         │ LLM (GPT-4o-mini)    │
         │ - Generate SQL       │
         │ - Add explanations   │
         │ - Validate syntax    │
         └──────────┬───────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ SQL Executor      │
          │ - Execute query   │
          │ - Handle errors   │
          │ - Format results  │
          └─────────┬─────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Response        │
           │ - SQL Query     │
           │ - Results       │
           │ - Metadata      │
           └────────┬────────┘
                    │
                    ▼
         ┌────────────────────┐
         │ Streamlit Frontend │
         │ Display Results    │
         └────────────────────┘
```

## 🧩 Core Components

### 1. Frontend (Streamlit)

**Purpose**: Provide intuitive user interface for natural language queries

**Responsibilities**:
- Display chat interface
- Accept user inputs
- Show SQL queries generated
- Display query results in formatted tables
- Manage session state
- Handle user interactions

**Technologies**: Streamlit, Altair (visualization)

### 2. Backend API (FastAPI)

**Purpose**: Handle business logic and orchestrate between components

**Responsibilities**:
- Expose REST endpoints
- Validate incoming requests
- Orchestrate pipeline execution
- Handle errors gracefully
- Log activities for debugging
- Cache results when applicable

**Key Endpoints**:
```
POST /api/text-to-sql
  - Convert natural language to SQL
  - Input: {question, database, context}
  - Output: {sql, explanation, status}

GET /api/databases
  - List available databases
  
GET /api/schemas/{database}
  - Get schema information
  
POST /api/execute
  - Execute generated SQL query
  - Input: {sql, database}
  - Output: {results, row_count, execution_time}
```

### 3. LLM Handler

**Purpose**: Interface with OpenAI API for SQL generation

**Responsibilities**:
- Prepare prompts with context
- Call OpenAI API
- Parse LLM responses
- Handle API errors and retries
- Manage token usage
- Cache completions

**Process**:
1. Build context from RAG search
2. Format system prompt with database schema
3. Create user prompt with question + context
4. Call OpenAI GPT-4o-mini
5. Parse and validate SQL response
6. Return clean SQL + explanation

### 4. Vector Store (FAISS)

**Purpose**: Enable semantic search over database schemas and documentation

**Responsibilities**:
- Index database documentation
- Create embeddings for queries
- Search for relevant context
- Return similar schemas/examples
- Improve SQL generation accuracy

**Data Indexed**:
- Table schemas
- Sample queries
- Domain knowledge
- Business context

### 5. Database Layer (Oracle + SQLAlchemy)

**Purpose**: Execute SQL queries and fetch results

**Responsibilities**:
- Manage database connections
- Execute validated SQL
- Handle transaction management
- Format and return results
- Handle database errors
- Provide schema information

## 📊 Data Models

### Request Model

```python
class TextToSQLRequest(BaseModel):
    question: str                    # Natural language question
    database: str                    # Target database
    context: Optional[str] = None    # Additional context
    max_results: int = 1000         # Result limit
```

### Response Model

```python
class TextToSQLResponse(BaseModel):
    sql: str                        # Generated SQL query
    explanation: str                # Why this query was generated
    database: str                   # Target database
    status: str                     # success, error, partial
    error: Optional[str] = None     # Error message if failed
    confidence: float               # Confidence score 0-1
```

## 🔐 Security Considerations

1. **SQL Injection Prevention**
   - Validate generated SQL syntax
   - Use parameterized queries
   - Escape user inputs

2. **API Security**
   - Input validation with Pydantic
   - Rate limiting
   - Request logging

3. **Database Access**
   - Read-only connections for queries
   - Credential management via environment variables
   - Connection pooling

4. **API Keys**
   - OpenAI API key in environment variables
   - Never commit secrets
   - Use .env for local development

## 🚀 Scalability & Performance

### Current Limitations
- Single-threaded Streamlit app
- FAISS stored in memory
- Sequential query processing

### Scalability Improvements

```
Future Architecture:
┌─────────────────────┐
│  Load Balancer      │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
┌────────┐   ┌────────┐
│API Pod1│   │API Pod2│  (Kubernetes)
└────┬───┘   └───┬────┘
     │           │
     └──────┬────┘
            ▼
     ┌────────────────┐
     │ Redis Cache    │
     └────────────────┘
            │
     ┌──────┴──────┐
     ▼             ▼
┌────────────┐ ┌──────────────┐
│Vector DB   │ │ Postgres     │
│(Pinecone)  │ │ (Read-only)  │
└────────────┘ └──────────────┘
```

### Performance Optimization
- Cache embeddings
- Connection pooling
- Query result caching
- Batch processing for RAG indexing
- Async API responses

## 📈 Monitoring & Logging

### Metrics Tracked
- API response time
- Query success/failure rate
- LLM API usage & costs
- Vector search latency
- Database query execution time

### Logging Strategy
- Info: API requests/responses
- Debug: Pipeline steps
- Warning: Query failures
- Error: System failures

## 🧪 Testing Strategy

```
Unit Tests
├── LLM Handler (mocked OpenAI)
├── SQL Validation
├── Database connections
└── API endpoints

Integration Tests
├── End-to-end pipelines
├── Database execution
└── RAG accuracy

Performance Tests
├── Response time
├── Vector search speed
└── Concurrent requests
```

## 🔄 Development Workflow

1. **Local Development**
   - Clone repository
   - Install dependencies
   - Set up .env file
   - Run backend & frontend locally

2. **Testing**
   - Unit tests before commits
   - Integration tests before PRs
   - Manual testing with various queries

3. **Deployment**
   - Docker containerization
   - CI/CD pipeline
   - Cloud deployment (AWS/GCP/Azure)

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [OpenAI API Guide](https://platform.openai.com/docs/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
