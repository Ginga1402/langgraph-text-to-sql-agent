

# Text-to-SQL Agent with LangGraph


A custom LangGraph workflow that converts natural language questions into SQL queries using open-source LLMs via Ollama. Built with custom tools to work with models that don't support function calling.

Tech Stack: LangChain, LangGraph, Ollama (CodeGemma 7B), SQLite
Features: Sequential workflow (list tables → get schema → generate SQL → execute → natural language response)
Usage: Run notebook_b.ipynb and ask questions like "How many customers are from the USA?"
Output: Returns structured response with SQL query, raw results, and natural language explanation
Database: Chinook music store database with 11 tables (Album, Artist, Customer, etc.)
