import sqlite3
from ..core.config import get_db_connection


def execute_sql(query: str):
    if "SELECT" not in query.strip().upper():
        raise PermissionError("Error: Only SELECT queries are permitted for execution.")

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = (
                [desc[0] for desc in cursor.description] if cursor.description else []
            )
            return column_names, results
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error: Query failed. Details: {e}") from e
