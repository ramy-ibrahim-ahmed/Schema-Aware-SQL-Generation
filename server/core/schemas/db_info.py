from typing import List, Dict, Any, Union
from dataclasses import dataclass, field


@dataclass
class ColumnInfo:
    name: str
    type: str
    notnull: bool
    is_primary_key: bool


@dataclass
class ForeignKeyInfo:
    from_column: str
    to_table: str
    to_column: str


@dataclass
class TableInfo:
    schema: List[ColumnInfo]
    foreign_keys: List[ForeignKeyInfo] = field(default_factory=list)
    sample_rows: List[Dict[str, Any]] = field(default_factory=list)


TableResult = Dict[str, Union[TableInfo, str]]
