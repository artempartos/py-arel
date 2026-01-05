from __future__ import annotations
from typing import List, Any, Optional
from arel.nodes.node import Node
from arel.nodes.join_source import JoinSource

class SelectCore(Node):
    def __init__(self, relation: Any = None):
        super().__init__()
        self.source = JoinSource(relation)
        self.set_quantifier: Optional[Any] = None
        self.optimizer_hints: Optional[Any] = None
        self.projections: List[Any] = []
        self.wheres: List[Any] = []
        self.groups: List[Any] = []
        self.havings: List[Any] = []
        self.windows: List[Any] = []
        self.comment: Optional[Any] = None

    @property
    def from_(self) -> Any:
        return self.source.left

    @from_.setter
    def from_(self, value: Any) -> None:
        self.source.left = value

    def __hash__(self) -> int:
        return hash((
            self.source, self.set_quantifier, tuple(self.projections),
            self.optimizer_hints, tuple(self.wheres), tuple(self.groups),
            tuple(self.havings), tuple(self.windows), self.comment
        ))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.source == getattr(other, 'source', None) and
            self.set_quantifier == getattr(other, 'set_quantifier', None) and
            self.optimizer_hints == getattr(other, 'optimizer_hints', None) and
            self.projections == getattr(other, 'projections', None) and
            self.wheres == getattr(other, 'wheres', None) and
            self.groups == getattr(other, 'groups', None) and
            self.havings == getattr(other, 'havings', None) and
            self.windows == getattr(other, 'windows', None) and
            self.comment == getattr(other, 'comment', None)
        )

    def __copy__(self) -> 'SelectCore':
        import copy
        new = super().__copy__()
        new.source = copy.copy(self.source) if self.source else None
        new.projections = copy.copy(self.projections)
        new.wheres = copy.copy(self.wheres)
        new.groups = copy.copy(self.groups)
        new.havings = copy.copy(self.havings)
        new.windows = copy.copy(self.windows)
        return new

