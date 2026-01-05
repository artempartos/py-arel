from __future__ import annotations
from typing import List, Any
from arel.nodes.functions import Function

class Count(Function):
    def __init__(self, expr: List[Any], distinct: bool = False):
        super().__init__(expr)
        self.distinct = distinct

    def __hash__(self) -> int:
        expr_hash = tuple(self.expressions) if isinstance(self.expressions, list) else self.expressions
        return hash((expr_hash, self.distinct))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.expressions == other.expressions and
            self.distinct == other.distinct
        )

