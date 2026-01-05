from typing import Any
from arel.nodes.node import Node

class BindParam(Node):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def __hash__(self) -> int:
        return hash((self.__class__, self.value))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BindParam) and self.value == other.value

class BoundSqlLiteral(Node):
    def __init__(self, sql: str, binds: list, positional: bool = True):
        super().__init__()
        self.sql = sql
        self.binds = binds
        self.positional = positional

    def __hash__(self) -> int:
        return hash((self.__class__, self.sql, tuple(self.binds), self.positional))

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, BoundSqlLiteral) and
            self.sql == other.sql and
            self.binds == other.binds and
            self.positional == other.positional
        )
