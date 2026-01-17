"""
Text2SQL - Natural Language to SQL Converter
Main application combining FastAPI backend and Streamlit frontend
"""

import os
import json
from typing import Optional, List, Dict
from datetime import datetime

import streamlit as st
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from openai import OpenAI

# ==================== FastAPI Models ====================

class TextToSQLRequest(BaseModel):
    """Request model for text-to-SQL conversion"""
    question: str = Field(..., min_length=1, description="Natural language question")
    database: str = Field(..., description="Target database name")
    context: Optional[str] = Field(None, description="Additional context")


class TextToSQLResponse(BaseModel):
    """Response model for text-to-SQL conversion"""
    sql: str
    explanation: str
    database: str
    status: str
    error: Optional[str] = None
    confidence: float


class ExecuteQueryRequest(BaseModel):
    """Request model for query execution"""
    sql: str = Field(..., description="SQL query to execute")
    database: str = Field(..., description="Target database")
    limit: int = Field(default=1000, description="Result limit")


# ==================== FastAPI Setup ====================

app = FastAPI(
    title="Text2SQL API",
    description="Convert natural language to SQL queries",
    version="1.0.0"
)


# ==================== LLM Handler ====================

class LLMHandler:
    """Handle interactions with OpenAI API"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    
    def generate_sql(
        self,
        question: str,
        database: str,
        schema_info: str,
        context: Optional[str] = None
    ) -> tuple[str, str, float]:
        """
        Generate SQL query from natural language using LLM
        
        Args:
            question: Natural language question
            database: Target database name
            schema_info: Database schema information
            context: Additional context
            
        Returns:
            Tuple of (sql_query, explanation, confidence_score)
        """
        
        system_prompt = f"""You are an expert SQL developer. Convert natural language questions to SQL queries.
Database: {database}
Schema Information:
{schema_info}

Rules:
1. Generate only valid SQL queries
2. Use appropriate JOINs when needed
3. Include WHERE clauses for filters
4. Use proper aliases for tables
5. Optimize for readability
6. Return only the SQL query, no explanations in the query itself"""
        
        user_message = f"""Question: {question}"""
        if context:
            user_message += f"\n\nAdditional Context: {context}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Extract explanation if available
            explanation = f"Converted '{question}' to SQL query for {database} database"
            
            # Confidence score based on response (simplified)
            confidence = 0.9  # Default high confidence
            
            return sql_query, explanation, confidence
            
        except Exception as e:
            raise ValueError(f"LLM API Error: {str(e)}")


# ==================== Database Handler ====================

class DatabaseHandler:
    """Handle database connections and queries"""
    
    # Sample schema information for demonstration
    SCHEMAS = {
        "HR": """
        Tables:
        - EMPLOYEES (employee_id, first_name, last_name, email, department_id, salary)
        - DEPARTMENTS (department_id, department_name, manager_id)
        - JOBS (job_id, job_title, min_salary, max_salary)
        """,
        "BANKING": """
        Tables:
        - CUSTOMERS (customer_id, name, email, phone, created_date)
        - ACCOUNTS (account_id, customer_id, account_type, balance, created_date)
        - TRANSACTIONS (transaction_id, account_id, amount, transaction_date, type)
        """,
        "MUSIC": """
        Tables:
        - ARTISTS (artist_id, name, genre)
        - ALBUMS (album_id, artist_id, title, release_date)
        - SONGS (song_id, album_id, title, duration)
        """,
    }
    
    def get_schema_info(self, database: str) -> str:
        """Get schema information for database"""
        if database not in self.SCHEMAS:
            raise ValueError(f"Database '{database}' not supported")
        return self.SCHEMAS[database]
    
    def validate_sql(self, sql: str) -> bool:
        """Basic SQL validation"""
        sql_upper = sql.upper().strip()
        
        # Check for dangerous operations
        dangerous_keywords = ["DROP", "DELETE FROM", "TRUNCATE", "ALTER", "CREATE USER"]
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return False
        
        # Check for SELECT statement
        if not sql_upper.startswith("SELECT"):
            return False
        
        return True
    
    def execute_query(self, sql: str, database: str, limit: int = 1000) -> Dict:
        """Execute SQL query (mock implementation)"""
        
        if not self.validate_sql(sql):
            raise ValueError("Invalid or unsafe SQL query")
        
        # Mock execution result
        return {
            "status": "success",
            "rows_returned": 0,
            "execution_time_ms": 145,
            "message": "Query execution simulated (set up database connection for real execution)",
            "data": []
        }


# ==================== FastAPI Endpoints ====================

db_handler = DatabaseHandler()


@app.post("/api/text-to-sql", response_model=TextToSQLResponse)
async def text_to_sql(request: TextToSQLRequest):
    """Convert natural language to SQL query"""
    
    try:
        # Get schema information
        schema_info = db_handler.get_schema_info(request.database)
        
        # Initialize LLM handler
        llm = LLMHandler()
        
        # Generate SQL
        sql, explanation, confidence = llm.generate_sql(
            question=request.question,
            database=request.database,
            schema_info=schema_info,
            context=request.context
        )
        
        return TextToSQLResponse(
            sql=sql,
            explanation=explanation,
            database=request.database,
            status="success",
            confidence=confidence
        )
        
    except ValueError as e:
        return TextToSQLResponse(
            sql="",
            explanation="",
            database=request.database,
            status="error",
            error=str(e),
            confidence=0.0
        )


@app.post("/api/execute")
async def execute_query(request: ExecuteQueryRequest):
    """Execute SQL query"""
    
    try:
        result = db_handler.execute_query(request.sql, request.database, request.limit)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/databases")
async def get_databases():
    """Get list of available databases"""
    return {
        "databases": list(db_handler.SCHEMAS.keys())
    }


@app.get("/api/schemas/{database}")
async def get_schema(database: str):
    """Get schema for specific database"""
    try:
        schema = db_handler.get_schema_info(database)
        return {
            "database": database,
            "schema": schema
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ==================== Streamlit UI ====================

def run_streamlit():
    """Run Streamlit interface"""
    
    st.set_page_config(
        page_title="Text2SQL",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔍 Text2SQL - Natural Language to SQL Converter")
    st.markdown("Convert natural language questions into SQL queries powered by OpenAI")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        selected_db = st.selectbox(
            "Select Database",
            ["HR", "BANKING", "MUSIC"]
        )
        
        st.markdown("---")
        st.subheader("📊 About")
        st.markdown("""
        **Text2SQL** uses OpenAI GPT-4o-mini to convert:
        - Natural language questions → SQL queries
        - Works with multiple databases
        - Validates and explains generated queries
        
        **Features:**
        - 🚀 Fast SQL generation
        - ✅ Query validation
        - 📝 Explanations
        - 🗄️ Multi-database support
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Ask a Question")
        question = st.text_area(
            "Enter your question in natural language",
            placeholder="e.g., Show me all employees in the Sales department with salary > 50000",
            height=100
        )
    
    with col2:
        st.subheader("Options")
        add_context = st.checkbox("Add additional context")
        context = ""
        if add_context:
            context = st.text_area("Additional context", height=100)
    
    # Execute button
    if st.button("🚀 Generate SQL", use_container_width=True):
        if not question:
            st.error("Please enter a question")
        else:
            with st.spinner("Generating SQL query..."):
                try:
                    # Call API
                    api_base = "http://127.0.0.1:8000"
                    
                    import requests
                    response = requests.post(
                        f"{api_base}/api/text-to-sql",
                        json={
                            "question": question,
                            "database": selected_db,
                            "context": context if context else None
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Display results
                        st.success("✅ SQL Query Generated Successfully")
                        
                        # SQL Query
                        st.subheader("Generated SQL")
                        st.code(data["sql"], language="sql")
                        
                        # Explanation
                        st.subheader("📝 Explanation")
                        st.info(data["explanation"])
                        
                        # Confidence
                        st.subheader("🎯 Confidence Score")
                        st.progress(min(data["confidence"], 1.0))
                        
                        # Execute button
                        if st.button("Execute Query"):
                            with st.spinner("Executing query..."):
                                exec_response = requests.post(
                                    f"{api_base}/api/execute",
                                    json={
                                        "sql": data["sql"],
                                        "database": selected_db
                                    }
                                )
                                if exec_response.status_code == 200:
                                    result = exec_response.json()
                                    st.success("✅ Query Executed")
                                    st.json(result)
                                else:
                                    st.error(f"Execution failed: {exec_response.text}")
                    else:
                        st.error(f"Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure FastAPI backend is running on http://127.0.0.1:8000")
    
    # Examples
    st.markdown("---")
    st.subheader("💡 Example Questions")
    
    examples = {
        "HR": [
            "Show me all employees in the Sales department",
            "Find employees with salary greater than 50000",
            "List top 10 highest paid employees"
        ],
        "BANKING": [
            "Show all transactions for customer ID 123",
            "Find accounts with balance > 10000",
            "List transactions from last 30 days"
        ],
        "MUSIC": [
            "Show all albums by artist ID 5",
            "List songs longer than 5 minutes",
            "Find the most recent albums"
        ]
    }
    
    if selected_db in examples:
        for i, example in enumerate(examples[selected_db], 1):
            st.caption(f"{i}. {example}")


# ==================== Main ====================

if __name__ == "__main__":
    import sys
    
    # Check if running as API or UI
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        # Run FastAPI
        uvicorn.run(
            app,
            host=os.getenv("API_HOST", "127.0.0.1"),
            port=int(os.getenv("API_PORT", "8000"))
        )
    else:
        # Run Streamlit
        run_streamlit()
