Secure your agents at: CodeAstra.dev

## AI Agent Privacy Notice

Astra Sentinel found a possible pattern where sensitive user, customer, or patient data may be passed directly into an AI agent or LLM context.

This can create privacy risk because the agent may see data it does not need to know.

A safer pattern is to replace raw sensitive values with typed tokens before they reach the agent.

Example:

Before: Book appointment for John Smith, DOB 04/12/1988
After: Book appointment for [CVT:NAME:patient_name], DOB [CVT:DOB:patient_dob]

The agent can still perform the workflow, but it never sees the raw sensitive data.

Detected pattern examples:
```json
[
  {
    "pattern": "unprotected_ai_context",
    "evidence": "chatollama(base_url='http:localhost:11434', model=model_name)"
  }
]
```

This notice was generated from a privacy scan. Please review before merging.

Secure your agents at: CodeAstra.dev

---

# 📚 Text-to-SQL Agent: Natural Language Database Query System

**Text-to-SQL LangGraph Agent is an open-source AI workflow that transforms natural language questions into SQL queries and insightful answers—powered locally by Ollama and Open Source LLM's, without relying on function calling.**

## 🎯 Project Description

This project demonstrates an intelligent Text-to-SQL Agent that transforms natural language questions into executable SQL queries and returns human-readable results. Built to bridge the gap between business users and database systems, it enables anyone to query databases using plain English without SQL knowledge.

The system processes questions like "How many customers are from the USA?" and automatically generates the corresponding SQL query, executes it against the database, and provides both technical results and conversational explanations.

It is implemented in two ways:

  1. Jupyter Notebook (text_to_SQL_Langchain_agent.ipynb) — utilizes LangChain’s built-in SQL agent.

  2. Custom LangGraph Workflow — uses sequential nodes and custom tools for deterministic SQL generation and execution.


### 🏗️ Technical Architecture

The system follows a modular, stateful architecture combining **LangGraph**, **Ollama**, and **SQLite** for controlled Text-to-SQL generation.

#### LangGraph Agent Pipeline
- Manages conversation flow using **MessagesState**
- Executes **5 sequential nodes** with deterministic routing (`START → END`)
- Integrates **custom @tool decorators** for database operations

#### LLM Integration
- **Model:** CodeGemma 7B Instruct (Q4_K_S) - Configurable
- **Inference Engine:** Ollama (`http://localhost:11434`)
- **Context Handling:** Structured prompts with schema injection and response formatting

#### Database Layer
- **Engine:** SQLite using LangChain’s `SQLDatabase` abstraction
- **Schema:** Chinook music database with 11 tables - Configurable
- **Safety:** Read-only operations enforced with query validation



### ✨ Key Features

- **🧠 Intelligent Query Processing**: Converts natural language questions into accurate SQL queries, understands table relationships, and handles complex multi-table joins.  
- **🔄 Multiple Interfaces**: Accessible via Streamlit web app (interactive dashboard), FastAPI REST endpoints (for integrations), and Jupyter Notebook (for development and experimentation).  
- **🛡️ Production-Ready Safety**: Ensures read-only database operations, robust error handling, query validation, and automatic result limiting to prevent misuse or overload.  
- **📊 Rich Output Formats**: Returns structured responses including generated SQL queries, raw database results, and natural-language explanations for better interpretability.  


## 📁 Project Structure
```
📦 langgraph-text-to-sql-agent
│
├── configuration.py        # Environment setup and configurations
├── FastAPI.py              # API layer for backend integration
├── langgraphagent.py       # Core LangGraph workflow and agent logic
├── streamlitapp.py         # Streamlit frontend for user interaction
├── text_to_SQL_Langchain_agent.ipynb   # Jupyter notebook (LangChain agent version)
└── README.md
└── License

```

### 💡 Use Cases

- **Data Exploration**: Ask natural language questions to explore relational data without writing SQL.  
- **Business Intelligence**: Generate quick insights from structured databases for decision-making.  
- **Developer Tools**: Integrate the FastAPI endpoint into analytics dashboards or internal data systems.  
- **Education & Training**: Teach SQL concepts interactively by showing natural language to SQL conversions.  
- **AI Agents Integration**: Use as a backend for chatbots or virtual assistants requiring database access.  


---

## 🧭 Demo Sample Images

**Streamlit Interface**

<img width="1915" height="1080" alt="Image" src="https://github.com/user-attachments/assets/93324b05-b375-4cff-a76f-c6a2cf9a2175" />

**FastAPI Response**

<img width="1718" height="878" alt="Image" src="https://github.com/user-attachments/assets/2a500b25-98ee-4743-baed-c7a76f5c35d1" />

---

## 🛠️ Installation Instructions

### Prerequisites
- Python 3.10+
- CUDA-compatible GPU (optional, for faster processing)
- 8GB+ RAM recommended

### Step 1: Clone Repository
```bash
git clone https://github.com/Ginga1402/langgraph-text-to-sql-agent.git
cd langgraph-text-to-sql-agent
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```


### Step 3: Set Up Ollama (LLM Backend)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the required model
ollama pull codegemma:7b-instruct-v1.1-q4_K_S
```

### Step 4: Configure Paths
Update the paths in `configuration.py` to match your system:
```python
model_name = "codegemma:7b-instruct-v1.1-q4_K_S"
database_name = "sqlite:///Chinook.db"
```

## 📖 Usage

### Starting the Application

1. **Start the FastAPI Server**:
```bash
python FastAPI.py
```
The API will be available at `http://localhost:8000`

2. **Launch the Streamlit Interface**:
```bash
streamlit run streamlit_app.py
```
The web interface will open at `http://localhost:8501`

### ⚙️ Basic Workflow


1. **User Input** → The user asks a natural language question (e.g., *“How many customers are from the USA?”*).  
2. **List Tables** → The system retrieves available table names from the SQLite database.  
3. **Get Schema** → The schema for relevant tables is extracted to provide context to the LLM.  
4. **Generate SQL** → The LLM (CodeGemma 7B via Ollama) creates a syntactically correct SQL query.  
5. **Run Query** → The SQL query is safely executed with validation and read-only enforcement.  
6. **Generate Response** → The system returns a structured output including:  
   - The generated SQL query  
   - Raw database results  
   - A natural language explanation of the findings  

**Workflow Graph:**  
 
START → list_tables → get_schema → generate_sql → run_query → generate_response → END

---

### 🧱 Technologies Used



| Technology | Description | Link |
|------------|-------------|------|
| **LangChain** | Framework for building LLM-driven applications | [LangChain](https://python.langchain.com) |
| **LangGraph** | Node-based agent orchestration for LLM workflows | [LangGraph](https://github.com/langchain-ai/langgraph) |
| **Ollama** | Local LLM inference engine | [Ollama](https://ollama.ai) |
| **CodeGemma 7B (Q4_K_S)** | Quantized instruction-tuned model for code understanding | [Gemma Models](https://ai.google.dev/gemma) |
| **SQLite** | Lightweight relational database for structured data | [SQLite](https://sqlite.org) |
| **FastAPI** | High-performance API framework for Python | [FastAPI](https://fastapi.tiangolo.com) |
| **Streamlit** | Web framework for building interactive data apps | [Streamlit](https://streamlit.io) |
| **Pydantic** | Data validation using Python type annotations | [pydantic.dev](https://pydantic.dev/) |

## 🤝 Contributing

Contributions to this project are welcome! If you have ideas for improvements, bug fixes, or new features, feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Star History

If you find Text-to-SQL-Agent useful, please consider giving it a star ⭐ on GitHub!
