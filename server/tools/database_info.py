import sqlite3


def get_db_info(db_client):
    tables_columns = {}
    try:
        
        cursor = db_client.cursor()
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
