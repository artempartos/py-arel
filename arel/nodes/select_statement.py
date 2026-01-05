from __future__ import annotations
from typing import List, Any, Optional
from arel.nodes.node import Node
from arel.nodes.node_expression import NodeExpression
from arel.nodes.join_source import JoinSource

class SelectStatement(NodeExpression):
    def __init__(self, relation: Any = None):
        super().__init__()
        from arel.nodes.select_core import SelectCore
        self.cores = [SelectCore(relation)]
        self.orders: List[Any] = []
        self.limit: Optional[Any] = None
        self.lock: Optional[Any] = None
        self.offset: Optional[Any] = None
        self.with_: Optional[Any] = None

    def __hash__(self) -> int:
        return hash((tuple(self.cores), tuple(self.orders), self.limit, self.lock, self.offset, self.with_))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.cores == getattr(other, 'cores', None) and
            self.orders == getattr(other, 'orders', None) and
            self.limit == getattr(other, 'limit', None) and
            self.lock == getattr(other, 'lock', None) and
            self.offset == getattr(other, 'offset', None) and
            self.with_ == getattr(other, 'with_', None)
        )

    def __copy__(self) -> 'SelectStatement':
        import copy
        new = super().__copy__()
        new.cores = [copy.copy(x) for x in self.cores]
        new.orders = copy.copy(self.orders)
        new.limit = copy.copy(self.limit) if self.limit else None
        new.lock = copy.copy(self.lock) if self.lock else None
        new.offset = copy.copy(self.offset) if self.offset else None
        new.with_ = copy.copy(self.with_) if self.with_ else None
        return new

