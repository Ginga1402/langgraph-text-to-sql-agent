
from fastapi import FastAPI
from pydantic import BaseModel
from langgraph_agent import agent, format_final_output
from langchain_core.messages import HumanMessage


app = FastAPI()


class QueryRequest(BaseModel):
    question: str


@app.post("/query")
def query_database(request: QueryRequest):
    result = agent.invoke({"messages": [HumanMessage(content=request.question)]})
    return format_final_output(result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

