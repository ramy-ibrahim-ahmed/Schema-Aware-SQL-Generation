import sqlite3
from ..graph.state import State
from ..store.nlp.interface import BaseNLP
from ..tools.database_info import get_db_info
from ..store.prompts.factory import PromptFactory
from ..core.schemas import TableNamesResponse
from ..tools.tables_info import get_relations_info


def IdentifyAgent(state: State, nlp: BaseNLP, db_path) -> State:
    try:
        user_message = state.get("user_message")
        with sqlite3.connect(db_path) as db_client:
            info = get_db_info(db_client)
        info_str = "\n".join(
            [
                f"- Table: `{name}`, Columns: {', '.join(cols)}"
                for name, cols in info.items()
            ]
        )
        prompt = PromptFactory().get_prompt(prompt_type="system_identifier")
        messages = prompt.format(db_info=info_str, user_message=user_message)
        response: TableNamesResponse = nlp.struct_output(
            model_name="gemini-2.5-flash",
            messages=messages,
            structure=TableNamesResponse,
            instructions="generate structured output"
        )
        if not response.tables:
            return {
                "relevant_relations": "No relevant tables were identified for the question."
            }

        with sqlite3.connect(db_path) as db_client:
            relevant_relations = get_relations_info(response.tables, db_client)
        return {"relevant_relations": relevant_relations}

    except Exception as e:
        print(f"!!! IDENTIFY AGENT FAILED: {e}")
        return {
            "relevant_relations": f"Error: Failed to identify relevant tables or fetch schema. Details: {e}"
        }
