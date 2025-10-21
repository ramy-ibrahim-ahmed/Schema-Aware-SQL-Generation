import sqlite3
from ..core.config import get_db_connection


def get_table_and_column_names():
    tables_columns = {}
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            for table in tables:
                try:
                    cursor.execute(f"PRAGMA table_info(`{table}`);")
                    columns = [col[1] for col in cursor.fetchall()]
                    tables_columns[table] = columns
                except sqlite3.Error as e:
                    raise f"Could not get columns for table '{table}': {e}"
            return tables_columns
    except sqlite3.Error as e:
        return {}
