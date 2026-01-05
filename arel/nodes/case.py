from __future__ import annotations
from typing import Any, List, Optional
from arel.nodes.node_expression import NodeExpression
from arel.nodes.binary import Binary
from arel.nodes.unary import Unary
from arel.nodes.casted import build_quoted

class Case(NodeExpression):
    def __init__(self, expression: Any = None, default: Any = None):
        self.case = expression
        self.conditions: List[When] = []
        self.default = default

    def when(self, condition: Any, expression: Any = None) -> 'Case':
        self.conditions.append(When(build_quoted(condition), expression))
        return self

    def then(self, expression: Any) -> 'Case':
        self.conditions[-1].right = build_quoted(expression)
        return self

    def else_(self, expression: Any) -> 'Case':
        self.default = Else(build_quoted(expression))
        return self

    def __hash__(self) -> int:
        return hash((self.case, tuple(self.conditions), self.default))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.case == other.case and
            self.conditions == other.conditions and
            self.default == other.default
        )

    def __copy__(self) -> 'Case':
        import copy
        new = super().__copy__()
        new.case = copy.copy(self.case) if self.case else None
        new.conditions = [copy.copy(x) for x in self.conditions]
        new.default = copy.copy(self.default) if self.default else None
        return new

class When(Binary): pass
class Else(Unary): pass

