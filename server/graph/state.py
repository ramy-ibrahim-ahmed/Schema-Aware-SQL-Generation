from typing_extensions import TypedDict


class State(TypedDict):
    user_message: str
    relevant_relations: str
    sql_query: str
    sql_result: str
    response: str
    error_message: str
    error_count: int = 0
