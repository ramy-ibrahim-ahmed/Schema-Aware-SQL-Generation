from fastapi import FastAPI
from pydantic import BaseModel
from .graph.workflow import init_workflow
from .store.nlp.factory import NLPFactory
from .core import get_settings

DB_PATH = r"C:\Users\ramyu\code\sql\lms.db"
SETTINGS = get_settings()
NLP = NLPFactory.create_nlp(provider="gemini", api_key=SETTINGS.GEMINI_API_KEY)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    context: str
    sql: str
    response: str


app = FastAPI()


@app.post("/api/v1/run", response_model=QueryResponse)
async def run_workflow(payload: QueryRequest):
    workflow = init_workflow(db_path=DB_PATH, nlp=NLP)
    messages = {"user_message": payload.query}
    response = workflow.invoke(messages)
    return QueryResponse(
        context=response.get("relevant_relations", ""),
        sql=response.get("sql_query", ""),
        response=response.get("response", ""),
    )
