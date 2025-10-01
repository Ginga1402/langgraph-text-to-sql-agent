from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from typing import Literal
from langchain_core.messages import AIMessage, HumanMessage


from configuration import model_name,database_name

# Setup LLM
model_llm = ChatOllama(base_url="http:localhost:11434", model= model_name)

# Setup Database
db = SQLDatabase.from_uri(database_name)










### Create tools

@tool
def list_tables() -> str:
    """Get list of all database tables."""
    return str(db.get_usable_table_names())

@tool  
def get_schema(table_names: str) -> str:
    """Get schema for specified tables. Input should be comma-separated table names."""
    return db.get_table_info(table_names.split(", "))

@tool
def generate_sql(question: str, context: str) -> str:
    """Generate SQL query based on question and database context."""
    prompt = f"""
    Based on this database schema:
    {context}
    
    Question: {question}
    
    Write a SQL query to answer the question. Return ONLY the SQL query with no explanations or markdown formatting.
    """
    response = model_llm.invoke(prompt)
    # Clean the response to extract just the SQL
    sql = response.content.strip()
    # Remove common markdown formatting
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

@tool
def run_query(query: str) -> str:
    """Execute SQL query on database."""
    try:
        result = db.run(query)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def generate_response(question: str, sql_query: str, result: str) -> str:
    """Generate natural language response from SQL query and result."""
    # prompt = f"""
    # Question: {question}
    # SQL Query: {sql_query}
    # Result: {result}
    
    # Provide a clear, natural language explanation of the result. Be concise and direct.
    # """

    prompt = f"""
    You are an AI assistant. Given a question, its SQL query, and the result, 
    answer in natural, human-like language.

    Question: {question}
    SQL Query: {sql_query}
    Result: {result}

    Guidelines:
    - Speak directly to the user, as if explaining the finding to them.
    - Do not mention the query or the database process.
    - Focus on the meaning of the result.
    - Keep it concise, but feel free to add a small insight or context if it feels natural.
    - Use smooth, conversational wording.

    Answer:
    """


    response = model_llm.invoke(prompt)
    return response.content.strip()





##### Create Nodes

def list_tables_node(state: MessagesState):
    tables = list_tables.invoke({})
    return {"messages": [AIMessage(content=f"Available tables: {tables}")]}

def get_schema_node(state: MessagesState):
    schema = get_schema.invoke({"table_names": "Track, Genre"})
    return {"messages": [AIMessage(content=f"Schema info: {schema}")]}

def generate_sql_node(state: MessagesState):
    question = state["messages"][0].content  # Access .content directly
    context = state["messages"][-1].content  # Access .content directly
    sql = generate_sql.invoke({"question": question, "context": context})
    return {"messages": [AIMessage(content=f"Generated SQL: {sql}")]}

def run_query_node(state: MessagesState):
    sql = state["messages"][-1].content.replace("Generated SQL: ", "")
    result = run_query.invoke({"query": sql})
    return {"messages": [AIMessage(content=f"Query result: {result}")]}


def generate_response_node(state: MessagesState):
    question = state["messages"][0].content
    sql_msg = state["messages"][-2].content
    result_msg = state["messages"][-1].content
    
    sql_query = sql_msg.replace("Generated SQL: ", "")
    query_result = result_msg.replace("Query result: ", "")
    
    response = generate_response.invoke({
        "question": question, 
        "sql_query": sql_query, 
        "result": query_result
    })
    return {"messages": [AIMessage(content=f"Natural language response: {response}")]}





### Creating the Workflow Graph

builder = StateGraph(MessagesState)

# Add nodes
builder.add_node("list_tables", list_tables_node)
builder.add_node("get_schema", get_schema_node)
builder.add_node("generate_sql", generate_sql_node)
builder.add_node("run_query", run_query_node)
builder.add_node("generate_response", generate_response_node)


# Add edges
builder.add_edge(START, "list_tables")
builder.add_edge("list_tables", "get_schema")
builder.add_edge("get_schema", "generate_sql")
builder.add_edge("generate_sql", "run_query")
builder.add_edge("run_query", "generate_response")
builder.add_edge("generate_response", END)

# Compile the agent
agent = builder.compile()





def format_final_output(result):
    messages = result["messages"]
    question = messages[0].content
    sql_query = messages[-3].content.replace("Generated SQL: ", "")
    query_result = messages[-2].content.replace("Query result: ", "")
    natural_response = messages[-1].content.replace("Natural language response: ", "")
    
    return {
        "sql_query": sql_query,
        "output": query_result,
        "natural_language_response": natural_response
    }




# question = "How many customers are from the USA?"
# result = agent.invoke({"messages": [HumanMessage(content=question)]})
# formatted_output = format_final_output(result)
# print(formatted_output)