from __future__ import annotations
from typing import List, Any
from arel.nodes.node import Node

class Fragments(Node):
    def __init__(self, values: List[Any] = None):
        super().__init__()
        self.values = values if values is not None else []

    def __add__(self, other: Any) -> 'Fragments':
        from arel import arel_node
        if not arel_node(other):
            raise ValueError("Expected Arel node")
        if isinstance(other, Fragments):
            return self.__class__(self.values + other.values)
        return self.__class__(self.values + [other])

    def __iadd__(self, other: Any) -> 'Fragments':
        from arel import arel_node
        if not arel_node(other):
            raise ValueError("Expected Arel node")
        if isinstance(other, Fragments):
            self.values.extend(other.values)
        else:
            self.values.append(other)
        return self

    def __hash__(self) -> int:
        return hash(tuple(self.values))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.values == getattr(other, 'values', None)
        )

