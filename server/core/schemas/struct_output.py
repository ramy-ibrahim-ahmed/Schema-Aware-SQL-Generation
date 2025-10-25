from pydantic import BaseModel


class TableNamesResponse(BaseModel):
    tables: list[str]


class SQLQueryResponse(BaseModel):
    sql: str
