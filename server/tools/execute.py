import sqlite3


def execute_sql(query: str, db_client):
    if "SELECT" not in query.strip().upper():
        raise PermissionError("Error: Only SELECT queries are permitted for execution.")

    try:
        cursor = db_client.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = (
                [desc[0] for desc in cursor.description] if cursor.description else []
            )
        return column_names, results
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error: Query failed. Details: {e}") from e
