from __future__ import annotations
from typing import List, Any, Optional
from arel.nodes.node import Node

class InsertStatement(Node):
    def __init__(self, relation: Any = None):
        super().__init__()
        self.relation = relation
        self.columns: List[Any] = []
        self.values: Optional[Any] = None
        self.select: Optional[Any] = None

    def __hash__(self) -> int:
        values_hash = tuple(self.values) if isinstance(self.values, list) else self.values
        return hash((self.relation, tuple(self.columns), values_hash, self.select))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.relation == getattr(other, 'relation', None) and
            self.columns == getattr(other, 'columns', None) and
            self.select == getattr(other, 'select', None) and
            self.values == getattr(other, 'values', None)
        )

    def __copy__(self) -> 'InsertStatement':
        import copy
        new = super().__copy__()
        new.columns = copy.copy(self.columns)
        new.values = copy.copy(self.values) if self.values else None
        new.select = copy.copy(self.select) if self.select else None
        return new

