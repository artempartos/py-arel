from __future__ import annotations
from typing import Any, List
from arel.nodes.node_expression import NodeExpression
from arel.mixins.window_predications import WindowPredicationsMixin
from arel.mixins.filter_predications import FilterPredicationsMixin

class Function(NodeExpression, WindowPredicationsMixin, FilterPredicationsMixin):
    def __init__(self, expr: List[Any]):
        super().__init__()
        self.expressions = expr
        self.distinct = False

    def __hash__(self) -> int:
        expr_hash = tuple(self.expressions) if isinstance(self.expressions, list) else self.expressions
        return hash((expr_hash, self.distinct))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.expressions == other.expressions and
            self.distinct == other.distinct
        )

class Sum(Function): pass
class Exists(Function): pass
class Max(Function): pass
class Min(Function): pass
class Avg(Function): pass

