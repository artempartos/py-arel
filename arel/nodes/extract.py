from typing import Any
from arel.nodes.node_expression import NodeExpression

class Extract(NodeExpression):
    def __init__(self, expr: Any, field: str):
        super().__init__()
        self.expr = expr
        self.field = field

    def __hash__(self) -> int:
        return hash((self.__class__, self.expr, self.field))

    def __eq__(self, other: Any) -> bool:
        return (
            super().__eq__(other) and
            self.field == getattr(other, 'field', None)
        )

