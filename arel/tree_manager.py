from __future__ import annotations
from typing import Any, Optional
from arel.mixins.factory_methods import FactoryMethodsMixin

class TreeManager(FactoryMethodsMixin):
    def __init__(self):
        self._ast: Optional[Any] = None

    @property
    def ast(self) -> Any:
        return self._ast

    def to_dot(self) -> str:
        from arel.visitors.dot import Dot
        from arel.collectors.plain_string import PlainString
        collector = PlainString()
        visitor = Dot()
        visitor.accept(self._ast, collector)
        return collector.value

    def to_sql(self, engine: Any = None) -> str:
        if engine is None:
            from arel.table import Table
            engine = Table.engine

        from arel.collectors.sql_string import SQLString
        collector = SQLString()
        return engine.connection.visitor.accept(self._ast, collector).value

    class StatementMethods:
        def take(self, limit: Any) -> 'TreeManager':
            from arel.nodes.unary import Limit
            from arel.nodes import build_quoted
            if limit is not None:
                self._ast.limit = Limit(build_quoted(limit))
            return self

        def skip(self, offset: Any) -> 'TreeManager':
            from arel.nodes.unary import Offset
            from arel.nodes import build_quoted
            if offset is not None:
                self._ast.offset = Offset(build_quoted(offset))
            return self

        def order(self, *expr: Any) -> 'TreeManager':
            self._ast.orders = list(expr)
            return self

        @property
        def key(self) -> Any:
            return self._ast.key

        @key.setter
        def key(self, key: Any) -> None:
            from arel.nodes import build_quoted
            if isinstance(key, list):
                self._ast.key = [build_quoted(k) for k in key]
            else:
                self._ast.key = build_quoted(key)

        @property
        def wheres(self) -> List[Any]:
            return self._ast.wheres

        @wheres.setter
        def wheres(self, exprs: List[Any]) -> None:
            self._ast.wheres = exprs

        def where(self, expr: Any) -> 'TreeManager':
            self._ast.wheres.append(expr)
            return self

