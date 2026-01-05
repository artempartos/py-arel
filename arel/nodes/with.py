from typing import Any, List, Optional
from arel.nodes.unary import Unary

class With(Unary):
    @property
    def children(self) -> Any:
        return self.expr

class WithRecursive(With): pass

