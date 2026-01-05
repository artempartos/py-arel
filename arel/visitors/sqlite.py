from typing import Any
from arel.visitors.to_sql import ToSql

class SQLite(ToSql):
    def visit_arel_nodes_unary_Lock(self, o: Any, collector: Any) -> Any:
        # Locks are not supported in SQLite
        return collector

    def visit_arel_nodes_regexp_Regexp(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " REGEXP "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_regexp_NotRegexp(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " NOT REGEXP "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_select_statement_SelectStatement(self, o: Any, collector: Any) -> Any:
        # SQLite defaults limit to -1 if offset is set without limit
        if o.offset and not o.limit:
            from arel.nodes.unary import Limit
            o.limit = Limit(-1)
        return super().visit_arel_nodes_select_statement_SelectStatement(o, collector)

    def visit_arel_nodes_binary_IsNotDistinctFrom(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " IS "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_binary_IsDistinctFrom(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " IS NOT "
        collector = self.visit(o.right, collector)
        return collector

