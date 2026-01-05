from typing import Any, List, Optional
from arel.visitors.to_sql import ToSql

class PostgreSQL(ToSql):
    def visit_arel_nodes_regexp_Regexp(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << (" ~ " if o.case_sensitive else " ~* ")
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_regexp_NotRegexp(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << (" !~ " if o.case_sensitive else " !~* ")
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_matches_Matches(self, o: Any, collector: Any) -> Any:
        op = " LIKE " if o.case_sensitive else " ILIKE "
        collector = self.visit(o.left, collector)
        collector << op
        collector = self.visit(o.right, collector)
        if o.escape:
            collector << " ESCAPE "
            collector = self.visit(o.escape, collector)
        return collector

    def visit_arel_nodes_matches_DoesNotMatch(self, o: Any, collector: Any) -> Any:
        op = " NOT LIKE " if o.case_sensitive else " NOT ILIKE "
        collector = self.visit(o.left, collector)
        collector << op
        collector = self.visit(o.right, collector)
        if o.escape:
            collector << " ESCAPE "
            collector = self.visit(o.escape, collector)
        return collector

    def visit_arel_nodes_bind_param_BindParam(self, o: Any, collector: Any) -> Any:
        return collector.add_bind(o.value, lambda i: f"${i}")

    def visit_arel_nodes_unary_Lock(self, o: Any, collector: Any) -> Any:
        return self.visit(o.expr, collector)

    def visit_arel_nodes_unary_DistinctOn(self, o: Any, collector: Any) -> Any:
        collector << "DISTINCT ON ( "
        collector = self.visit(o.expr, collector)
        collector << " )"
        return collector

    def visit_arel_nodes_binary_IsNotDistinctFrom(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " IS NOT DISTINCT FROM "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_binary_IsDistinctFrom(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " IS DISTINCT FROM "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_unary_Lateral(self, o: Any, collector: Any) -> Any:
        collector << "LATERAL "
        # Always wrap in parentheses for LATERAL queries
        collector = self.grouping_parentheses(o.expr, collector, True)
        return collector

    def visit_arel_nodes_unary_GroupingElement(self, o: Any, collector: Any) -> Any:
        collector << "( "
        collector = self.visit(o.expr, collector)
        collector << " )"
        return collector

    def visit_arel_nodes_unary_Cube(self, o: Any, collector: Any) -> Any:
        collector << "CUBE"
        collector = self.grouping_array_or_grouping_element(o, collector)
        return collector

    def visit_arel_nodes_unary_RollUp(self, o: Any, collector: Any) -> Any:
        collector << "ROLLUP"
        collector = self.grouping_array_or_grouping_element(o, collector)
        return collector

    def visit_arel_nodes_unary_GroupingSet(self, o: Any, collector: Any) -> Any:
        collector << "GROUPING SETS"
        collector = self.grouping_array_or_grouping_element(o, collector)
        return collector

    def grouping_array_or_grouping_element(self, o: Any, collector: Any) -> Any:
        """Utilized by GroupingSet, Cube & RollUp visitors to handle grouping aggregation semantics"""
        if isinstance(o.expr, list):
            collector << "( "
            collector = self.visit_list(o.expr, collector)
            collector << " )"
        else:
            collector = self.visit(o.expr, collector)
        return collector
