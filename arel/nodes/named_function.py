from __future__ import annotations
from typing import List, Any, Union
from arel.nodes.functions import Function

class NamedFunction(Function):
    def __init__(self, name: str, expr: Union[List[Any], Any]):
        # In Ruby Function accepts expr as is and stores in @expressions
        # If expr is not a list, wrap for Function, but keep original
        if isinstance(expr, list):
            super().__init__(expr)
        else:
            super().__init__([expr])
            # Override expressions for compatibility with Ruby behavior
            self.expressions = expr
        self.name = name

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.name)

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.name == getattr(other, 'name', None)

