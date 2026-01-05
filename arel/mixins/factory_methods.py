from __future__ import annotations
from typing import Any, List, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from arel.nodes.node import Node
    from arel.nodes.joins import InnerJoin

class FactoryMethodsMixin:
    def create_true(self) -> 'Node':
        from arel.nodes.true import True_
        return True_()

    def create_false(self) -> 'Node':
        from arel.nodes.false import False_
        return False_()

    def create_table_alias(self, relation: Any, name: str) -> 'Node':
        from arel.nodes.table_alias import TableAlias
        return TableAlias(relation, name)

    def create_join(self, to: Any, constraint: Any = None, klass: Optional[Type['Node']] = None) -> 'Node':
        if klass is None:
            from arel.nodes.joins import InnerJoin
            klass = InnerJoin
        return klass(to, constraint)

    def create_string_join(self, to: Any) -> 'Node':
        from arel.nodes.joins import StringJoin
        return self.create_join(to, None, StringJoin)

    def create_and(self, clauses: List[Any]) -> 'Node':
        from arel.nodes.nary import And
        return And(clauses)

    def create_on(self, expr: Any) -> 'Node':
        from arel.nodes.unary import On
        return On(expr)

    def grouping(self, expr: Any) -> 'Node':
        from arel.nodes.grouping import Grouping
        return Grouping(expr)

    def lower(self, column: Any) -> 'Node':
        from arel.nodes.named_function import NamedFunction
        from arel.nodes import build_quoted
        return NamedFunction("LOWER", [build_quoted(column)])

    def coalesce(self, *exprs: Any) -> 'Node':
        from arel.nodes.named_function import NamedFunction
        return NamedFunction("COALESCE", list(exprs))

    def cast(self, name: Any, type_: Any) -> 'Node':
        from arel.nodes.named_function import NamedFunction
        return NamedFunction("CAST", [name.as_(type_)])

