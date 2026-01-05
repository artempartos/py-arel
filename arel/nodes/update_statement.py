from __future__ import annotations
from typing import List, Any, Optional
from arel.nodes.node import Node

class UpdateStatement(Node):
    def __init__(self, relation: Any = None):
        super().__init__()
        self.relation = relation
        self.wheres: List[Any] = []
        self.values: List[Any] = []
        self.groups: List[Any] = []
        self.havings: List[Any] = []
        self.orders: List[Any] = []
        self.limit: Optional[Any] = None
        self.offset: Optional[Any] = None
        self.comment: Optional[Any] = None
        self.key: Optional[Any] = None

    def __hash__(self) -> int:
        wheres_hash = tuple(self.wheres) if isinstance(self.wheres, list) else self.wheres
        values_hash = tuple(self.values) if isinstance(self.values, list) else self.values
        orders_hash = tuple(self.orders) if isinstance(self.orders, list) else self.orders
        return hash((
            self.relation, wheres_hash, values_hash,
            orders_hash, self.limit, self.offset, self.comment, self.key
        ))

    def __copy__(self) -> 'UpdateStatement':
        import copy
        new = self.__class__.__new__(self.__class__)
        new.relation = copy.copy(self.relation) if self.relation else None
        new.wheres = copy.copy(self.wheres)
        new.values = copy.copy(self.values)
        new.groups = copy.copy(self.groups)
        new.havings = copy.copy(self.havings)
        new.orders = copy.copy(self.orders)
        new.limit = copy.copy(self.limit) if self.limit else None
        new.offset = copy.copy(self.offset) if self.offset else None
        new.comment = copy.copy(self.comment) if self.comment else None
        new.key = copy.copy(self.key) if self.key else None
        return new

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.relation == getattr(other, 'relation', None) and
            self.wheres == getattr(other, 'wheres', None) and
            self.values == getattr(other, 'values', None) and
            self.groups == getattr(other, 'groups', None) and
            self.havings == getattr(other, 'havings', None) and
            self.orders == getattr(other, 'orders', None) and
            self.limit == getattr(other, 'limit', None) and
            self.offset == getattr(other, 'offset', None) and
            self.comment == getattr(other, 'comment', None) and
            self.key == getattr(other, 'key', None)
        )

