import sqlite3

DB_PATH = ""


def get_db_connection() -> sqlite3.Connection:
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        raise e
