from typing import Any
from arel.visitors.to_sql import ToSql

class MySQL(ToSql):
    def visit_arel_nodes_binary_Union(self, o: Any, collector: Any) -> Any:
        collector << "("
        collector = super().visit_arel_nodes_binary_Union(o, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_binary_Intersect(self, o: Any, collector: Any) -> Any:
        collector << "("
        collector = super().visit_arel_nodes_binary_Intersect(o, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_binary_Except(self, o: Any, collector: Any) -> Any:
        collector << "("
        collector = super().visit_arel_nodes_binary_Except(o, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_limit_Limit(self, o: Any, collector: Any) -> Any:
        collector << "LIMIT "
        collector = self.visit(o.expr, collector)
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

    def visit_arel_nodes_unary_Bin(self, o: Any, collector: Any) -> Any:
        collector << "CAST("
        collector = self.visit(o.expr, collector)
        collector << " AS BINARY)"
        return collector

    def visit_arel_nodes_select_statement_SelectStatement(self, o: Any, collector: Any) -> Any:
        # MySQL defaults limit to 18446744073709551615 if offset is set without limit
        if o.offset and not o.limit:
            from arel.nodes.unary import Limit
            o.limit = Limit(18446744073709551615)
        return super().visit_arel_nodes_select_statement_SelectStatement(o, collector)

    def visit_arel_nodes_select_core_SelectCore(self, o: Any, collector: Any) -> Any:
        # MySQL uses DUAL for empty from
        if not o.source or (hasattr(o.source, 'is_empty') and o.source.is_empty()):
            from arel import sql
            o.source = sql("DUAL")
        return super().visit_arel_nodes_select_core_SelectCore(o, collector)

    def visit_arel_nodes_binary_IsNotDistinctFrom(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " <=> "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_binary_IsDistinctFrom(self, o: Any, collector: Any) -> Any:
        collector << "NOT "
        collector = self.visit_arel_nodes_binary_IsNotDistinctFrom(o, collector)
        return collector

    def visit_arel_nodes_infix_operation_Concat(self, o: Any, collector: Any) -> Any:
        collector << "CONCAT("
        collector = self.visit(o.left, collector)
        collector << ", "
        collector = self.visit(o.right, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_ordering_NullsFirst(self, o: Any, collector: Any) -> Any:
        # MySQL doesn't support NULLS FIRST, so we use IS NOT NULL, expr
        collector = self.visit(o.expr.expr, collector)
        collector << " IS NOT NULL, "
        collector = self.visit(o.expr, collector)
        return collector

    def visit_arel_nodes_ordering_NullsLast(self, o: Any, collector: Any) -> Any:
        # MySQL doesn't support NULLS LAST, so we use IS NULL, expr
        collector = self.visit(o.expr.expr, collector)
        collector << " IS NULL, "
        collector = self.visit(o.expr, collector)
        return collector

    def visit_arel_nodes_cte_Cte(self, o: Any, collector: Any) -> Any:
        # MySQL ignores MATERIALIZED modifiers
        collector << self.quote_table_name(o.name)
        collector << " AS "
        collector = self.visit(o.relation, collector)
        return collector

