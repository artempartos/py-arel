from __future__ import annotations
from typing import Any, List, Optional, Union, TYPE_CHECKING
from arel.tree_manager import TreeManager
from arel.mixins.crud import CrudMixin
from arel.nodes.select_statement import SelectStatement
from arel.nodes.select_core import SelectCore
from arel.nodes.unary import Offset, Limit, Lock, Group, On
from arel.nodes.comment import Comment
from arel.nodes.window import NamedWindow
from arel.nodes.distinct import Distinct
from arel.nodes.binary import As
from arel.nodes.joins import Join, InnerJoin, StringJoin, OuterJoin
from arel.nodes.sql_literal import SqlLiteral
from arel.nodes.nary import And
from arel.errors import EmptyJoinError

if TYPE_CHECKING:
    from arel.nodes.node import Node

class SelectManager(TreeManager, CrudMixin):
    def __init__(self, table: Any = None):
        super().__init__()
        self._ast = SelectStatement(table)
        self._ctx = self._ast.cores[-1]

    def __copy__(self) -> 'SelectManager':
        """Create a shallow copy of this SelectManager (Ruby clone compatibility)"""
        import copy
        new_manager = SelectManager.__new__(SelectManager)
        new_manager._ast = copy.copy(self._ast)
        new_manager._ctx = new_manager._ast.cores[-1]
        return new_manager

    @property
    def limit(self) -> Optional[Any]:
        return self._ast.limit.expr if self._ast.limit else None

    @property
    def taken(self) -> Optional[Any]:
        """Alias for limit (Ruby compatibility)"""
        return self.limit

    @property
    def constraints(self) -> List[Any]:
        return self._ctx.wheres

    @property
    def offset(self) -> Optional[Any]:
        return self._ast.offset.expr if self._ast.offset else None

    @offset.setter
    def offset(self, amount: Optional[int]) -> None:
        """Setter for offset (Ruby compatibility: alias offset= skip)"""
        if amount is not None:
            self._ast.offset = Offset(amount)
        else:
            self._ast.offset = None

    def skip(self, amount: Optional[int]) -> 'SelectManager':
        if amount is not None:
            self._ast.offset = Offset(amount)
        else:
            self._ast.offset = None
        return self

    def exists(self) -> 'Exists':
        from arel.nodes.functions import Exists
        return Exists(self._ast)

    def as_(self, other: Any) -> 'TableAlias':
        from arel.nodes.table_alias import TableAlias
        from arel.nodes.unary import Grouping
        return TableAlias(Grouping(self._ast), SqlLiteral(str(other), retryable=True))

    def lock(self, locking: Any = True) -> 'SelectManager':
        if locking is True:
            locking = SqlLiteral("FOR UPDATE")
        elif isinstance(locking, str):
            locking = SqlLiteral(locking)

        self._ast.lock = Lock(locking)
        return self

    @property
    def locked(self) -> Optional[Any]:
        return self._ast.lock

    def on(self, *exprs: Any) -> 'SelectManager':
        self._ctx.source.right[-1].right = On(self._collapse(list(exprs)))
        return self

    def group(self, *columns: Any) -> 'SelectManager':
        for column in columns:
            if isinstance(column, str):
                column = SqlLiteral(column)
            self._ctx.groups.append(Group(column))
        return self

    def from_(self, table: Any) -> 'SelectManager':
        if isinstance(table, str):
            table = SqlLiteral(table)

        if isinstance(table, Join):
            self._ctx.source.right.append(table)
        else:
            self._ctx.from_ = table

        return self

    @property
    def froms(self) -> List[Any]:
        return [core.from_ for core in self._ast.cores if core.from_ is not None]

    def join(self, relation: Any, klass: Any = InnerJoin) -> 'SelectManager':
        if relation is None:
            return self

        if isinstance(relation, str):
            if not relation:
                raise EmptyJoinError()
            klass = StringJoin
        elif isinstance(relation, SqlLiteral):
            if not str(relation):
                raise EmptyJoinError()
            klass = StringJoin

        self._ctx.source.right.append(self.create_join(relation, None, klass))
        return self

    def outer_join(self, relation: Any) -> 'SelectManager':
        return self.join(relation, OuterJoin)

    def having(self, expr: Any) -> 'SelectManager':
        self._ctx.havings.append(expr)
        return self

    def window(self, name: str) -> 'NamedWindow':
        window = NamedWindow(name)
        self._ctx.windows.append(window)
        return window

    def project(self, *projections: Any) -> 'SelectManager':
        for p in projections:
            if isinstance(p, (str, type(None))):
                p = SqlLiteral(str(p) if p else '*')
            self._ctx.projections.append(p)
        return self

    @property
    def projections(self) -> List[Any]:
        return self._ctx.projections

    @projections.setter
    def projections(self, value: List[Any]) -> None:
        self._ctx.projections = value

    def optimizer_hints(self, *hints: Any) -> 'SelectManager':
        if hints:
            from arel.nodes.unary import OptimizerHints
            self._ctx.optimizer_hints = OptimizerHints(list(hints))
        return self

    def distinct(self, value: bool = True) -> 'SelectManager':
        self._ctx.set_quantifier = Distinct() if value else None
        return self

    def distinct_on(self, value: Any) -> 'SelectManager':
        if value:
            from arel.nodes.unary import DistinctOn
            self._ctx.set_quantifier = DistinctOn(value)
        else:
            self._ctx.set_quantifier = None
        return self

    def order(self, *expr: Any) -> 'SelectManager':
        for x in expr:
            if isinstance(x, str):
                x = SqlLiteral(x)
            self._ast.orders.append(x)
        return self

    @property
    def orders(self) -> List[Any]:
        return self._ast.orders

    def where(self, expr: Any) -> 'SelectManager':
        if isinstance(expr, TreeManager):
            expr = expr.ast
        self._ctx.wheres.append(expr)
        return self

    def where_sql(self, engine: Any = None) -> Optional[Any]:
        """Returns WHERE clause SQL as SqlLiteral, or None if no wheres"""
        if not self._ctx.wheres:
            return None

        if engine is None:
            from arel.table import Table
            engine = Table.engine

        and_node = self.create_and(self._ctx.wheres)
        sql_str = and_node.to_sql(engine)
        return SqlLiteral(f"WHERE {sql_str}")

    def union(self, operation: Any = None, other: Any = None) -> Any:
        """Union this manager with another manager or node.

        If called with one argument: union(self.ast, operation.ast)
        If called with two arguments: union operation (like 'all'), other manager
        """
        from arel.nodes.binary import Union, UnionAll

        if other is not None:
            # Two arguments: operation (like 'all') and other manager
            if isinstance(operation, str) and operation.lower() == 'all':
                node_class = UnionAll
            else:
                node_class = Union
            return node_class(self._ast, other.ast if hasattr(other, 'ast') else other)
        else:
            # One argument: other manager
            return Union(self._ast, operation.ast if hasattr(operation, 'ast') else operation)

    def intersect(self, other: Any) -> Any:
        from arel.nodes.binary import Intersect
        return Intersect(self._ast, other.ast if hasattr(other, 'ast') else other)

    def except_(self, other: Any) -> Any:
        from arel.nodes.binary import Except
        return Except(self._ast, other.ast if hasattr(other, 'ast') else other)

    def with_(self, *subqueries: Any) -> 'SelectManager':
        from arel.nodes.cte import With, WithRecursive
        if subqueries and isinstance(subqueries[0], str) and subqueries[0].lower() == "recursive":
            node_class = WithRecursive
            subqueries = subqueries[1:]
        else:
            node_class = With

        flattened = []
        for s in subqueries:
            if isinstance(s, list):
                flattened.extend(s)
            else:
                flattened.append(s)

        self._ast.with_ = node_class(flattened)
        return self

    def lateral(self, table_name: Any = None) -> 'Lateral':
        """Create a LATERAL subquery node.

        Args:
            table_name: Optional table name/alias. If None, uses ast. If provided, uses as_(table_name).

        Returns:
            Lateral node wrapping the subquery.
        """
        from arel.nodes.unary import Lateral
        if table_name is None:
            base = self._ast
        else:
            base = self.as_(table_name)
        return Lateral(base)

    def take(self, limit: int) -> 'SelectManager':
        if limit is not None:
            self._ast.limit = Limit(limit)
        else:
            self._ast.limit = None
        return self

    @property
    def join_sources(self) -> List[Any]:
        return self._ctx.source.right

    @property
    def source(self) -> Any:
        return self._ctx.source

    def comment(self, *values: str) -> Union['SelectManager', 'Comment']:
        if values:
            self._ctx.comment = Comment(list(values))
            return self
        else:
            return self._ctx.comment

    def _collapse(self, exprs: List[Any]) -> Any:
        exprs = [e for e in exprs if e is not None]
        exprs = [SqlLiteral(e) if isinstance(e, str) else e for e in exprs]

        if len(exprs) == 1:
            return exprs[0]
        else:
            return self.create_and(exprs)

