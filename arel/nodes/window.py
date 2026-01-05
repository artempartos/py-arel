from __future__ import annotations
from typing import Any, List, Optional
from arel.nodes.node import Node
from arel.nodes.unary import Unary
from arel.nodes.binary import Binary
from arel.nodes.sql_literal import SqlLiteral
from arel.mixins.alias_predication import AliasPredicationMixin

class Window(Node):
    def __init__(self):
        super().__init__()
        self.orders: List[Any] = []
        self.partitions: List[Any] = []
        self.framing: Optional[Any] = None

    def order(self, *expr: Any) -> 'Window':
        self.orders.extend([
            SqlLiteral(str(x)) if isinstance(x, (str, bytes)) else x
            for x in expr
        ])
        return self

    def partition(self, *expr: Any) -> 'Window':
        self.partitions.extend([
            SqlLiteral(str(x)) if isinstance(x, (str, bytes)) else x
            for x in expr
        ])
        return self

    def frame(self, expr: Any) -> 'Window':
        self.framing = expr
        return self

    def rows(self, expr: Any = None) -> 'Rows':
        if self.framing:
            return Rows(expr)
        else:
            rows_obj = Rows(expr)
            self.frame(rows_obj)
            return rows_obj

    def range_(self, expr: Any = None) -> 'Range':
        if self.framing:
            return Range(expr)
        else:
            range_obj = Range(expr)
            self.frame(range_obj)
            return range_obj

    def __hash__(self) -> int:
        return hash((tuple(self.orders), self.framing))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.orders == other.orders and
            self.framing == other.framing and
            self.partitions == other.partitions
        )

class NamedWindow(Window):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def range(self, expr: Any = None) -> 'Range':
        """Alias for range_ to match Ruby API"""
        return self.range_(expr)

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.name)

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.name == other.name

class Rows(Unary): pass
class Range(Unary): pass

class CurrentRow(Node):
    def __hash__(self) -> int:
        return hash(self.__class__)

    def __eq__(self, other: Any) -> bool:
        return self.__class__ == other.__class__

class Preceding(Unary):
    def __init__(self, expr: Any = None):
        super().__init__(expr)

class Following(Unary):
    def __init__(self, expr: Any = None):
        super().__init__(expr)

class Over(Binary, AliasPredicationMixin):
    def operator(self) -> str:
        return "OVER"

