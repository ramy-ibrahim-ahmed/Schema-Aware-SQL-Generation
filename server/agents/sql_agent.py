from ..graph.state import State
from ..store.prompts.factory import PromptFactory
from ..core.schemas import SQLQueryResponse
from ..store.nlp.interface import BaseNLP


def SQLAgent(state: State, nlp: BaseNLP) -> State:
    user_message = state.get("user_message", "")
    relevant_relations = state.get("relevant_relations", "")
    last_sql = state.get("sql_query", "")
    error = state.get("error_message", "")

    if error:
        prompt = PromptFactory().get_prompt("system_fix_sql")
        messages = prompt.format(
            user_message=user_message,
            relevant_relations=relevant_relations,
            last_sql=last_sql,
            error=error,
        )
    else:
        prompt = PromptFactory().get_prompt("system_sql")
        messages = prompt.format(
            user_message=user_message,
            relevant_relations=relevant_relations,
        )

    response: SQLQueryResponse = nlp.struct_output(
        model_name="gemini-2.5-flash",
        messages=messages,
        structure=SQLQueryResponse,
        instructions="generate structured output",
    )

    return {"sql_query": response.sql, "error_message": ""}
