from .graph.workflow import init_workflow
from .store.nlp.factory import NLPFactory

DB_PATH = r"D:\system\sql\lms.db"
GEMINI_API_KEY = "AIzaSyD9bEgveLP0H9Y_8_PQFWCdyH4YgO6FDrY"
NLP = NLPFactory.create_nlp(provider="gemini", api_key=GEMINI_API_KEY)

workflow = init_workflow(db_path=DB_PATH, nlp=NLP)

messages = {"user_message": "list the students in the AI department."}
for event in workflow.stream(messages):
    print(event)
