from typing import Any, Optional
from arel.nodes.binary import Binary
from arel.nodes.unary import Unary

class With(Unary):
    @property
    def children(self) -> Any:
        return self.expr

class WithRecursive(With): pass

class Cte(Binary):
    def __init__(self, name: str, relation: Any, materialized: Optional[bool] = None):
        super().__init__(name, relation)
        self.materialized = materialized

    @property
    def name(self) -> str:
        return self.left

    @property
    def relation(self) -> Any:
        return self.right

    def __hash__(self) -> int:
        return hash((self.name, self.relation, self.materialized))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.name == other.name and
            self.relation == other.relation and
            self.materialized == other.materialized
        )

    def to_cte(self) -> 'Cte':
        return self

    def to_table(self) -> 'Table':
        from arel.table import Table
        return Table(self.name)

