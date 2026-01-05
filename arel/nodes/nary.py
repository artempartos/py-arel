from __future__ import annotations
from typing import List, Any
from arel.nodes.node_expression import NodeExpression

class Nary(NodeExpression):
    def __init__(self, children: List[Any]):
        super().__init__()
        self.children = children

    @property
    def left(self) -> Any:
        return self.children[0] if self.children else None

    @property
    def right(self) -> Any:
        return self.children[1] if len(self.children) > 1 else None

    def fetch_attribute(self, block: Any) -> bool:
        return bool(self.children) and all(child.fetch_attribute(block) for child in self.children)

    def __hash__(self) -> int:
        return hash((self.__class__, tuple(self.children)))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.children == other.children
        )

class And(Nary): pass
class Or(Nary): pass

