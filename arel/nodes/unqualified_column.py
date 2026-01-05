from typing import Any
from arel.nodes.unary import Unary

class UnqualifiedColumn(Unary):
    @property
    def attribute(self) -> Any:
        return self.expr

    @property
    def relation(self) -> Any:
        return self.expr.relation

    @property
    def column(self) -> Any:
        return self.expr.column

    @property
    def name(self) -> str:
        return self.expr.name

