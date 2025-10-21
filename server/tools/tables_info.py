import sqlite3
from ..core.config import get_db_connection
from ..core.schemas import TableInfo, ColumnInfo, ForeignKeyInfo, TableResult


def get_tables_info_structured(table_names: list[str]) -> TableResult:
    """
    Securely retrieves schema, foreign keys, and sample rows for specified tables.

    Args:
        table_names: A list of table names to query.
        connection: An active sqlite3 database connection.

    Returns:
        A dictionary mapping each table name to a TableInfo object or an error message.
    """
    if not table_names:
        return {}

    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    allowed_tables = {row["name"] for row in cursor.fetchall()}

    results: TableResult = {}
    for table_name in table_names:
        if table_name not in allowed_tables:
            results[table_name] = (
                f"Error: Table '{table_name}' not found in the database."
            )
            continue

        try:
            cursor.execute(f'PRAGMA table_info("{table_name}");')
            schema_info = [
                ColumnInfo(
                    name=col["name"],
                    type=col["type"],
                    notnull=bool(col["notnull"]),
                    is_primary_key=bool(col["pk"]),
                )
                for col in cursor.fetchall()
            ]

            cursor.execute(f'PRAGMA foreign_key_list("{table_name}");')
            fk_info = [
                ForeignKeyInfo(
                    from_column=fk["from"],
                    to_table=fk["table"],
                    to_column=fk["to"],
                )
                for fk in cursor.fetchall()
            ]

            cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 3;')
            column_names = [desc[0] for desc in cursor.description]
            sample_rows = [dict(zip(column_names, row)) for row in cursor.fetchall()]

            results[table_name] = TableInfo(
                schema=schema_info, foreign_keys=fk_info, sample_rows=sample_rows
            )

        except sqlite3.Error as e:
            results[table_name] = f"Error retrieving info for table '{table_name}': {e}"

    return results


def format_table_info(results: TableResult) -> str:
    output_parts = []
    if not results:
        return "No table information to display."

    for table_name, info in results.items():
        part = f"Table: `{table_name}`\n"
        part += f"Schema: {[col.__dict__ for col in info.schema]}\n"
        if info.foreign_keys:
            part += f"Foreign Keys: {[fk.__dict__ for fk in info.foreign_keys]}\n"

        sample_cols = list(info.sample_rows[0].keys()) if info.sample_rows else []
        part += f"Sample Rows (Columns: {sample_cols}):\n{info.sample_rows}"
        output_parts.append(part)

    return "\n\n".join(output_parts)
