import sqlite3
from ..graph.state import State
from ..tools.execute import execute_sql


def ExecuteNode(state: State, db_path) -> State:
    sql_query = state.get("sql_query", "")
    error_count = state.get("error_count", 0)

    try:
        with sqlite3.connect(db_path) as db_client:
            result = execute_sql(sql_query, db_client)
        return {"sql_result": result}

    except PermissionError as e:

        return {"sql_error": str(e), "error_count": error_count + 1}

    except sqlite3.Error as e:
        return {"sql_error": f"SQLite error: {e}", "error_count": error_count + 1}

    except Exception as e:
        return {"sql_error": f"Unexpected error: {e}", "error_count": error_count + 1}
