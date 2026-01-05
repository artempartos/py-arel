from typing import Any
from arel.nodes.unary import Unary

class ValuesList(Unary):
    @property
    def rows(self) -> Any:
        return self.expr

