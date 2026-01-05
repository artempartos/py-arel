from __future__ import annotations
from typing import List, Any
from arel.nodes.node import Node

class Comment(Node):
    def __init__(self, values: List[str]):
        super().__init__()
        self.values = values

    def __hash__(self) -> int:
        return hash(tuple(self.values))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.values == getattr(other, 'values', None)
        )

