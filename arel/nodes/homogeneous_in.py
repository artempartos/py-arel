from typing import Any, List
from arel.nodes.node import Node

class HomogeneousIn(Node):
    def __init__(self, values: List[Any], attribute: Any, type: str):
        super().__init__()
        self.values = values
        self.attribute = attribute
        self.type = type

    def __hash__(self) -> int:
        return hash((self.attribute, tuple(self.values), self.type))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.attribute == getattr(other, 'attribute', None) and
            self.values == getattr(other, 'values', None) and
            self.type == getattr(other, 'type', None)
        )

    def equality(self) -> bool:
        return self.type == 'in'

    def invert(self) -> 'HomogeneousIn':
        new_type = 'notin' if self.type == 'in' else 'in'
        return HomogeneousIn(self.values, self.attribute, new_type)

    @property
    def left(self) -> Any:
        return self.attribute

    @property
    def right(self) -> Any:
        # In Ruby this is attribute.quoted_array(values), but for simplicity return values
        return self.values

class HomogeneousNotIn(HomogeneousIn): pass
