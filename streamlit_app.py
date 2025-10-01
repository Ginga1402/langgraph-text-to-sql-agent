import streamlit as st
import time
from langgraph_agent import agent, format_final_output, db
from langchain_core.messages import HumanMessage
from configuration import model_name

# Page config
st.set_page_config(
    page_title="Text-to-SQL Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sql-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .result-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .response-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown('<h1 class="main-header">🔍 Text-to-SQL Agent</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Database Info")
    st.success(f"Connected to: {db.dialect}")
    tables = db.get_usable_table_names()
    st.write("**Available Tables:**")
    for table in tables:
        st.write(f"• {table}")
    
    st.markdown("---")
    st.header("💡 Example Questions")
    example_questions = [
        "How many customers are from the USA?",
        "What is the total revenue from all invoices?",
        "Which genre has the most tracks?",
        "Who are the top 5 customers by total purchases?",
        "What is the average track length by genre?"
    ]
    
    for i, question in enumerate(example_questions):
        if st.button(f"📝 {question}", key=f"example_{i}"):
            st.session_state.question = question

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🤖 Ask Your Question")
    question = st.text_area(
        "Enter your question about the database:",
        value=st.session_state.get('question', ''),
        height=100,
        placeholder="e.g., How many customers are from the USA?"
    )
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        submit = st.button("🚀 Submit", type="primary")
    with col_btn2:
        if st.button("🗑️ Clear"):
            st.session_state.question = ""
            st.rerun()

with col2:
    st.header("⚙️ Processing Steps")
    if submit and question:
        progress_container = st.container()

# Process question
if submit and question:
    with st.spinner("Processing your question..."):
        try:
            # Show progress
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔍 Analyzing database tables...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                status_text.text("📋 Getting table schemas...")
                progress_bar.progress(40)
                time.sleep(0.5)
                
                status_text.text("🧠 Generating SQL query...")
                progress_bar.progress(60)
                time.sleep(0.5)
                
                status_text.text("⚡ Executing query...")
                progress_bar.progress(80)
                
                # Run the agent
                result = agent.invoke({"messages": [HumanMessage(content=question)]})
                formatted_output = format_final_output(result)
                
                status_text.text("✅ Generating response...")
                progress_bar.progress(100)
                time.sleep(0.5)
                
                status_text.text("🎉 Complete!")
            
            # Display results
            st.markdown("---")
            st.header("📊 Results")
            
            # SQL Query
            st.subheader("🔧 Generated SQL Query")
            st.markdown(f'<div class="sql-box"><code>{formatted_output["sql_query"]}</code></div>', 
                       unsafe_allow_html=True)
            
            # Raw Results
            st.subheader("📈 Query Results")
            st.markdown(f'<div class="result-box">{formatted_output["output"]}</div>', 
                       unsafe_allow_html=True)
            
            # Natural Language Response
            st.subheader("💬 Natural Language Response")
            st.markdown(f'<div class="response-box">{formatted_output["natural_language_response"]}</div>', 
                       unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with LangChain, LangGraph, and Streamlit | "
    f"Powered by {model_name} via Ollama"
    "</div>", 
    unsafe_allow_html=True
)