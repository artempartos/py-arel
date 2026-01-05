from __future__ import annotations
from typing import Any, List, Optional
from arel.visitors.visitor import Visitor
from arel.collectors.sql_string import SQLString

class ToSql(Visitor):
    def visit_arel_nodes_distinct_on_DistinctOn(self, o: Any, collector: Any) -> Any:
        raise NotImplementedError("DISTINCT ON not implemented for this db")
    def __init__(self, connection: Any):
        super().__init__()
        self.connection = connection

    def compile(self, node: Any, collector: Optional[Any] = None) -> str:
        if collector is None:
            collector = SQLString()
        return self.accept(node, collector).value

    # Visit methods for common nodes

    def visit_arel_nodes_insert_statement_InsertStatement(self, o: Any, collector: Any) -> Any:
        collector.retryable = False
        collector << "INSERT INTO "
        collector = self.visit(o.relation, collector)

        if o.columns:
            collector << " ("
            self.inject_join(o.columns, collector, ", ")
            collector << ")"

        if o.values:
            collector << " VALUES "
            collector = self.visit(o.values, collector)
        elif o.select:
            collector << " "
            collector = self.visit(o.select, collector)

        return collector

    def visit_arel_nodes_update_statement_UpdateStatement(self, o: Any, collector: Any) -> Any:
        collector.retryable = False
        o = self.prepare_update_statement(o)
        collector << "UPDATE "
        collector = self.visit(o.relation, collector)

        if o.values:
            collector << " SET "
            self.inject_join(o.values, collector, ", ")

        self.collect_nodes_for(o.wheres, collector, " WHERE ", " AND ")
        self.collect_nodes_for(o.orders, collector, " ORDER BY ")
        self.maybe_visit(o.limit, collector)
        self.maybe_visit(o.comment, collector)
        return collector

    def has_join_sources(self, o: Any) -> bool:
        """Check if statement has join sources"""
        from arel.nodes.join_source import JoinSource
        return isinstance(o.relation, JoinSource) and o.relation.right and len(o.relation.right) > 0

    def has_limit_or_offset_or_orders(self, o: Any) -> bool:
        """Check if statement has limit, offset or orders"""
        return o.limit is not None or o.offset is not None or (o.orders and len(o.orders) > 0)

    def prepare_update_statement(self, o: Any) -> Any:
        """Prepare update statement - create subquery with IN if needed"""
        if o.key and (self.has_limit_or_offset_or_orders(o) or self.has_join_sources(o)):
            import copy
            stmt = copy.copy(o)
            stmt.limit = None
            stmt.offset = None
            stmt.orders = []

            from arel.nodes.unary import Grouping
            from arel.nodes.in_ import In
            columns = Grouping(o.key)
            subselect = self.build_subselect(o.key, o)
            stmt.wheres = [In(columns, subselect)]

            if self.has_join_sources(o):
                stmt.relation = o.relation.left

            if o.groups:
                stmt.groups = o.groups
            if o.havings:
                stmt.havings = o.havings

            return stmt
        else:
            return o

    def prepare_delete_statement(self, o: Any) -> Any:
        """Prepare delete statement - same as prepare_update_statement"""
        return self.prepare_update_statement(o)

    def build_subselect(self, key: Any, o: Any) -> Any:
        """Build subselect for UPDATE/DELETE with key"""
        from arel.nodes.select_statement import SelectStatement
        from arel.nodes.select_core import SelectCore

        stmt = SelectStatement()
        core = stmt.cores[0]
        core.from_ = o.relation
        core.wheres = o.wheres
        core.projections = [key]

        if o.groups:
            core.groups = o.groups
        if o.havings:
            core.havings = o.havings

        stmt.limit = o.limit
        stmt.offset = o.offset
        stmt.orders = o.orders

        return stmt

    def visit_arel_nodes_delete_statement_DeleteStatement(self, o: Any, collector: Any) -> Any:
        collector.retryable = False
        o = self.prepare_delete_statement(o)
        collector << "DELETE FROM "
        collector = self.visit(o.relation, collector)

        self.collect_nodes_for(o.wheres, collector, " WHERE ", " AND ")
        self.collect_nodes_for(o.orders, collector, " ORDER BY ")
        self.maybe_visit(o.limit, collector)
        self.maybe_visit(o.comment, collector)
        return collector

    def visit_arel_nodes_select_statement_SelectStatement(self, o: Any, collector: Any) -> Any:
        if o.with_:
            collector = self.visit(o.with_, collector)
            collector << " "

        for core in o.cores:
            collector = self.visit(core, collector)

        if o.orders:
            collector << " ORDER BY "
            self.inject_join(o.orders, collector, ", ")

        # Collect windows from all cores
        all_windows = []
        for core in o.cores:
            if hasattr(core, 'windows') and core.windows:
                all_windows.extend(core.windows)

        if all_windows:
            collector << " WINDOW "
            self.inject_join(all_windows, collector, ", ")

        self.maybe_visit(o.limit, collector)
        self.maybe_visit(o.offset, collector)
        self.maybe_visit(o.lock, collector)
        return collector

    def visit_arel_nodes_select_core_SelectCore(self, o: Any, collector: Any) -> Any:
        collector << "SELECT"

        self.maybe_visit(o.set_quantifier, collector)
        self.collect_nodes_for(o.projections, collector, " ")

        if o.source and (not hasattr(o.source, 'is_empty') or not o.source.is_empty()):
            collector << " FROM "
            collector = self.visit(o.source, collector)

        self.collect_nodes_for(o.wheres, collector, " WHERE ", " AND ")
        self.collect_nodes_for(o.groups, collector, " GROUP BY ")
        self.collect_nodes_for(o.havings, collector, " HAVING ", " AND ")
        self.maybe_visit(o.comment, collector)
        return collector

    def visit_arel_nodes_join_source_JoinSource(self, o: Any, collector: Any) -> Any:
        if o.left:
            collector = self.visit(o.left, collector)
        if o.right:
            if o.left:
                collector << " "
            self.inject_join(o.right, collector, " ")
        return collector

    def visit_arel_nodes_joins_InnerJoin(self, o: Any, collector: Any) -> Any:
        collector << "INNER JOIN "
        collector = self.visit(o.left, collector)
        if o.right:
            collector << " "
            collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_joins_OuterJoin(self, o: Any, collector: Any) -> Any:
        collector << "LEFT OUTER JOIN "
        collector = self.visit(o.left, collector)
        if o.right:
            collector << " "
            collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_joins_FullOuterJoin(self, o: Any, collector: Any) -> Any:
        collector << "FULL OUTER JOIN "
        collector = self.visit(o.left, collector)
        if o.right:
            collector << " "
            collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_joins_RightOuterJoin(self, o: Any, collector: Any) -> Any:
        collector << "RIGHT OUTER JOIN "
        collector = self.visit(o.left, collector)
        if o.right:
            collector << " "
            collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_joins_StringJoin(self, o: Any, collector: Any) -> Any:
        return self.visit(o.left, collector)

    def visit_arel_nodes_unary_On(self, o: Any, collector: Any) -> Any:
        collector << "ON "
        return self.visit(o.expr, collector)

    def visit_arel_nodes_binary_As(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " AS "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_binary_Assignment(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " = "
        # Assignment.right can be Node, Attribute or a regular value
        if hasattr(o.right, '__class__') and hasattr(o.right, 'to_sql'):
            collector = self.visit(o.right, collector)
        else:
            collector << self.quote(o.right)
        return collector

    def visit_arel_nodes_filter_Filter(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " FILTER (WHERE "
        collector = self.visit(o.right, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_window_Over(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " OVER "
        if o.right is None:
            collector << "()"
        else:
            from arel.nodes.sql_literal import SqlLiteral
            if isinstance(o.right, SqlLiteral):
                collector = self.visit(o.right, collector)
            elif isinstance(o.right, str):
                collector << self.quote_column_name(o.right)
            else:
                collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_window_NamedWindow(self, o: Any, collector: Any) -> Any:
        collector << self.quote_column_name(o.name)
        collector << " AS "
        return self.visit_arel_nodes_window_Window(o, collector)

    def visit_arel_nodes_window_Window(self, o: Any, collector: Any) -> Any:
        collector << "("

        if o.partitions:
            collector << "PARTITION BY "
            self.inject_join(o.partitions, collector, ", ")

        if o.orders:
            if o.partitions:
                collector << " "
            collector << "ORDER BY "
            self.inject_join(o.orders, collector, ", ")

        if o.framing:
            if o.partitions or o.orders:
                collector << " "
            collector = self.visit(o.framing, collector)

        collector << ")"
        return collector

    def visit_arel_nodes_window_Rows(self, o: Any, collector: Any) -> Any:
        collector << "ROWS"
        if o.expr:
            collector << " "
            collector = self.visit(o.expr, collector)
        return collector

    def visit_arel_nodes_window_Range(self, o: Any, collector: Any) -> Any:
        collector << "RANGE"
        if o.expr:
            collector << " "
            collector = self.visit(o.expr, collector)
        return collector

    def visit_arel_nodes_window_Preceding(self, o: Any, collector: Any) -> Any:
        if o.expr:
            collector = self.visit(o.expr, collector)
        else:
            collector << "UNBOUNDED"
        collector << " PRECEDING"
        return collector

    def visit_arel_nodes_window_Following(self, o: Any, collector: Any) -> Any:
        if o.expr:
            collector = self.visit(o.expr, collector)
        else:
            collector << "UNBOUNDED"
        collector << " FOLLOWING"
        return collector

    def visit_arel_nodes_window_CurrentRow(self, o: Any, collector: Any) -> Any:
        collector << "CURRENT ROW"
        return collector

    def visit_arel_nodes_table_alias_TableAlias(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " "
        # If right (name) is SqlLiteral, don't quote it (Ruby compatibility)
        from arel.nodes.sql_literal import SqlLiteral
        if isinstance(o.right, SqlLiteral):
            collector << str(o.right)
        else:
            collector << self.quote_table_name(o.right)
        return collector

    def visit_arel_nodes_equality_Equality(self, o: Any, collector: Any) -> Any:
        right = o.right
        collector = self.visit(o.left, collector)
        if right is None or (hasattr(right, "is_nil") and right.is_nil()):
            collector << " IS NULL"
        else:
            collector << " = "
            collector = self.visit(right, collector)
        return collector

    def visit_arel_nodes_binary_NotEqual(self, o: Any, collector: Any) -> Any:
        right = o.right
        collector = self.visit(o.left, collector)
        if right is None or (hasattr(right, "is_nil") and right.is_nil()):
            collector << " IS NOT NULL"
        else:
            collector << " != "
            collector = self.visit(right, collector)
        return collector

    def visit_arel_nodes_binary_IsNotDistinctFrom(self, o: Any, collector: Any) -> Any:
        # Check if right is None or nil
        right = o.right
        if right is None or (hasattr(right, "is_nil") and right.is_nil()):
            collector = self.visit(o.left, collector)
            collector << " IS NULL"
        else:
            collector = self.is_distinct_from(o, collector)
            collector << " = 0"
        return collector

    def visit_arel_nodes_binary_IsDistinctFrom(self, o: Any, collector: Any) -> Any:
        # Check if right is None or nil
        right = o.right
        if right is None or (hasattr(right, "is_nil") and right.is_nil()):
            collector = self.visit(o.left, collector)
            collector << " IS NOT NULL"
        else:
            collector = self.is_distinct_from(o, collector)
            collector << " = 1"
        return collector

    def is_distinct_from(self, o: Any, collector: Any) -> Any:
        # Ruby: CASE WHEN left = right OR (left IS NULL AND right IS NULL) THEN 0 ELSE 1 END
        collector << "CASE WHEN "
        collector = self.visit(o.left, collector)
        collector << " = "
        collector = self.visit(o.right, collector)
        collector << " OR ("
        collector = self.visit(o.left, collector)
        collector << " IS NULL AND "
        collector = self.visit(o.right, collector)
        collector << " IS NULL) THEN 0 ELSE 1 END"
        return collector

    def visit_arel_nodes_binary_GreaterThan(self, o: Any, collector: Any) -> Any:
        return self.infix_value(o, collector, " > ")

    def visit_arel_nodes_binary_GreaterThanOrEqual(self, o: Any, collector: Any) -> Any:
        return self.infix_value(o, collector, " >= ")

    def visit_arel_nodes_binary_LessThan(self, o: Any, collector: Any) -> Any:
        return self.infix_value(o, collector, " < ")

    def visit_arel_nodes_binary_LessThanOrEqual(self, o: Any, collector: Any) -> Any:
        return self.infix_value(o, collector, " <= ")

    def visit_arel_nodes_binary_Between(self, o: Any, collector: Any) -> Any:
        from arel.nodes.nary import And
        collector = self.visit(o.left, collector)
        collector << " BETWEEN "
        if isinstance(o.right, And):
            # Between.right is And([left, right])
            if len(o.right.children) == 2:
                collector = self.visit(o.right.children[0], collector)
                collector << " AND "
                collector = self.visit(o.right.children[1], collector)
            else:
                collector = self.visit(o.right, collector)
        else:
            collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_in__In(self, o: Any, collector: Any) -> Any:
        attr, values = o.left, o.right

        if isinstance(values, list):
            collector.preparable = False

            if len(values) == 0:
                collector << "1=0"
                return collector

            # Filter out unboundable values
            values = [v for v in values if not self.unboundable(v)]

            if len(values) == 0:
                collector << "1=0"
                return collector

            collector = self.visit(attr, collector)
            collector << " IN ("
            collector = self.inject_join(values, collector, ", ")
            collector << ")"
            return collector
        else:
            collector = self.visit(attr, collector)
            collector << " IN ("
            collector = self.visit(values, collector)
            collector << ")"
            return collector

    def visit_arel_nodes_homogeneous_in_HomogeneousIn(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.attribute, collector)
        if o.type == 'in':
            collector << " IN ("
        else:
            collector << " NOT IN ("
        # Use bind parameters for values
        for i, value in enumerate(o.values):
            if i > 0:
                collector << ", "
            from arel.nodes.bind_param import BindParam
            collector = self.visit(BindParam(value), collector)
        collector << ")"
        return collector

    def visit_arel_nodes_ordering_NullsFirst(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.expr, collector)
        collector << " NULLS FIRST"
        return collector

    def visit_arel_nodes_ordering_NullsLast(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.expr, collector)
        collector << " NULLS LAST"
        return collector

    def visit_arel_nodes_matches_Matches(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " LIKE "
        collector = self.visit(o.right, collector)
        if o.escape:
            collector << " ESCAPE "
            collector = self.visit(o.escape, collector)
        return collector

    def visit_arel_nodes_matches_DoesNotMatch(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << " NOT LIKE "
        collector = self.visit(o.right, collector)
        if o.escape:
            collector << " ESCAPE "
            collector = self.visit(o.escape, collector)
        return collector

    def visit_arel_nodes_binary_NotIn(self, o: Any, collector: Any) -> Any:
        attr, values = o.left, o.right

        if isinstance(values, list):
            collector.preparable = False

            if len(values) == 0:
                collector << "1=1"
                return collector

            # Filter out unboundable values
            values = [v for v in values if not self.unboundable(v)]

            if len(values) == 0:
                collector << "1=1"
                return collector

            collector = self.visit(attr, collector)
            collector << " NOT IN ("
            collector = self.inject_join(values, collector, ", ")
            collector << ")"
            return collector
        else:
            collector = self.visit(attr, collector)
            collector << " NOT IN ("
            collector = self.visit(values, collector)
            collector << ")"
            return collector

    def visit_arel_nodes_nary_And(self, o: Any, collector: Any) -> Any:
        return self.inject_join(o.children, collector, " AND ")

    def visit_arel_nodes_nary_Or(self, o: Any, collector: Any) -> Any:
        return self.inject_join(o.children, collector, " OR ")

    def visit_arel_nodes_unary_Bin(self, o: Any, collector: Any) -> Any:
        return self.visit(o.expr, collector)

    def visit_arel_nodes_unary_Not(self, o: Any, collector: Any) -> Any:
        collector << "NOT ("
        collector = self.visit(o.expr, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_unary_operation_UnaryOperation(self, o: Any, collector: Any) -> Any:
        collector << f" {o.operator}"
        collector = self.visit(o.expr, collector)
        return collector

    def visit_arel_nodes_unary_operation_BitwiseNot(self, o: Any, collector: Any) -> Any:
        collector << " ~ "
        collector = self.visit(o.expr, collector)
        return collector

    def visit_arel_nodes_distinct_Distinct(self, o: Any, collector: Any) -> Any:
        collector << "DISTINCT"
        return collector

    def visit_arel_nodes_grouping_Grouping(self, o: Any, collector: Any) -> Any:
        # Ruby: if expr is already Grouping, don't add extra parentheses
        from arel.nodes.grouping import Grouping
        if isinstance(o.expr, Grouping):
            collector = self.visit(o.expr, collector)
        else:
            collector << "("
            collector = self.visit(o.expr, collector)
            collector << ")"
        return collector

    def visit_arel_nodes_unary_Grouping(self, o: Any, collector: Any) -> Any:
        # Fallback for when Grouping is imported from unary.py
        collector << "("
        collector = self.visit(o.expr, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_unary_Group(self, o: Any, collector: Any) -> Any:
        return self.visit(o.expr, collector)

    def visit_arel_nodes_unary_Limit(self, o: Any, collector: Any) -> Any:
        collector << "LIMIT "
        return self.visit(o.expr, collector)

    def visit_arel_nodes_unary_Lock(self, o: Any, collector: Any) -> Any:
        return self.visit(o.expr, collector)

    def visit_arel_nodes_unary_Offset(self, o: Any, collector: Any) -> Any:
        collector << "OFFSET "
        return self.visit(o.expr, collector)

    def visit_arel_nodes_ascending_Ascending(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.expr, collector)
        collector << " ASC"
        return collector

    def visit_arel_nodes_descending_Descending(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.expr, collector)
        collector << " DESC"
        return collector

    def visit_arel_nodes_true_True_(self, o: Any, collector: Any) -> Any:
        collector << "TRUE"
        return collector

    def visit_arel_nodes_false_False_(self, o: Any, collector: Any) -> Any:
        collector << "FALSE"
        return collector

    def visit_arel_nodes_case_Case(self, o: Any, collector: Any) -> Any:
        collector << "CASE "
        if o.case:
            collector = self.visit(o.case, collector)
            collector << " "
        if o.conditions:
            for condition in o.conditions:
                collector = self.visit(condition, collector)
                collector << " "
        if o.default:
            collector = self.visit(o.default, collector)
            collector << " "
        collector << "END"
        return collector

    def visit_arel_nodes_case_When(self, o: Any, collector: Any) -> Any:
        collector << "WHEN "
        collector = self.visit(o.left, collector)
        collector << " THEN "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_case_Else(self, o: Any, collector: Any) -> Any:
        collector << "ELSE "
        collector = self.visit(o.expr, collector)
        return collector

    def visit_arel_nodes_ordering_Descending(self, o: Any, collector: Any) -> Any:
        # Fallback for when Descending is imported from ordering.py
        collector = self.visit(o.expr, collector)
        collector << " DESC"
        return collector

    def visit_arel_nodes_ordering_Ascending(self, o: Any, collector: Any) -> Any:
        # Fallback for when Ascending is imported from ordering.py
        collector = self.visit(o.expr, collector)
        collector << " ASC"
        return collector

    def visit_arel_nodes_functions_Avg(self, o: Any, collector: Any) -> Any:
        return self.aggregate("AVG", o, collector)

    def visit_arel_nodes_functions_Exists(self, o: Any, collector: Any) -> Any:
        collector << "EXISTS ("
        collector = self.visit(o.expressions, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_functions_Sum(self, o: Any, collector: Any) -> Any:
        return self.aggregate("SUM", o, collector)

    def visit_arel_nodes_functions_Max(self, o: Any, collector: Any) -> Any:
        return self.aggregate("MAX", o, collector)

    def visit_arel_nodes_functions_Min(self, o: Any, collector: Any) -> Any:
        return self.aggregate("MIN", o, collector)

    def visit_arel_nodes_functions_Count(self, o: Any, collector: Any) -> Any:
        return self.aggregate("COUNT", o, collector)

    def visit_arel_nodes_count_Count(self, o: Any, collector: Any) -> Any:
        return self.aggregate("COUNT", o, collector)

    def visit_arel_table_Table(self, o: Any, collector: Any) -> Any:
        collector << self.quote_table_name(o.name)
        if o.table_alias:
            collector << " " << self.quote_table_name(o.table_alias)
        return collector

    def visit_arel_attributes_attribute_Attribute(self, o: Any, collector: Any) -> Any:
        from arel.nodes.table_alias import TableAlias
        if isinstance(o.relation, TableAlias):
            join_name = o.relation.right
        else:
            join_name = o.relation.table_alias or o.relation.name
        collector << self.quote_table_name(join_name) << "."
        # If column name is "*", don't quote it
        if str(o.name) == "*":
            collector << "*"
        else:
            collector << self.quote_column_name(o.name)
        return collector

    def visit_arel_nodes_bind_param_BindParam(self, o: Any, collector: Any) -> Any:
        if hasattr(collector, 'add_bind'):
            return collector.add_bind(o.value, lambda i: "?")
        else:
            collector << "?"
            return collector

    def visit_arel_nodes_values_list_ValuesList(self, o: Any, collector: Any) -> Any:
        collector << "VALUES "
        rows = o.rows if hasattr(o, 'rows') else o.expr
        for i, row in enumerate(rows):
            if i > 0:
                collector << ", "
            collector << "("
            if isinstance(row, list):
                for j, value in enumerate(row):
                    if j > 0:
                        collector << ", "
                    if value is None:
                        collector << "NULL"
                    else:
                        collector = self.visit(value, collector)
            else:
                if row is None:
                    collector << "NULL"
                else:
                    collector = self.visit(row, collector)
            collector << ")"
        return collector

    def visit_arel_nodes_infix_operation_InfixOperation(self, o: Any, collector: Any) -> Any:
        collector = self.visit(o.left, collector)
        collector << f" {o.operator} "
        collector = self.visit(o.right, collector)
        return collector

    def visit_arel_nodes_unqualified_column_UnqualifiedColumn(self, o: Any, collector: Any) -> Any:
        collector << self.quote_column_name(o.name)
        return collector

    def visit_arel_nodes_sql_literal_SqlLiteral(self, o: Any, collector: Any) -> Any:
        # Ruby: collector.retryable &&= o.retryable
        # This means: if collector.retryable == False, keep False, otherwise set to o.retryable
        collector.retryable = collector.retryable and o.retryable
        collector << str(o)
        return collector

    def visit_arel_nodes_bound_sql_literal_BoundSqlLiteral(self, o: Any, collector: Any) -> Any:
        collector.retryable = False
        import re
        from arel import arel_node

        bind_index = 0

        def new_bind(value):
            nonlocal collector, bind_index
            from arel.nodes.bound_sql_literal import BoundSqlLiteral
            if isinstance(value, BoundSqlLiteral):
                # Nested BoundSqlLiteral: expand it by processing its binds directly
                # For sql("?", [1, 2, sql("?", 3)]), the nested sql("?", 3) should become just ?
                # So we extract the bind parameters from the nested literal
                if value.positional_binds:
                    # Extract the first bind parameter (there should be only one for simple cases)
                    # For sql("?", 3), we want to output just ? (the bind parameter 3)
                    if len(value.positional_binds) == 1:
                        # Simple case: sql("?", 3) -> just output ? for the bind parameter 3
                        collector.add_bind(value.positional_binds[0], lambda i: "?")
                    else:
                        # Multiple binds: process each one
                        for i, nested_bind in enumerate(value.positional_binds):
                            if i > 0:
                                collector << ", "
                            collector = new_bind(nested_bind)
                elif value.named_binds:
                    # Named binds: process each one
                    for name, nested_value in value.named_binds.items():
                        collector = new_bind(nested_value)
                else:
                    # No binds, just output the SQL
                    collector << value.sql_with_placeholders
            elif arel_node(value):
                collector = self.visit(value, collector)
            elif isinstance(value, list):
                if len(value) == 0:
                    collector << self.quote(None)
                else:
                    # Check if there are arel nodes in the list
                    has_arel_nodes = any(arel_node(v) for v in value)
                    if not has_arel_nodes:
                        # All values are regular, use add_binds
                        collector.add_binds(value, None, lambda i: "?")
                    else:
                        # There are arel nodes, process one by one
                        for i, v in enumerate(value):
                            if i > 0:
                                collector << ", "
                            if arel_node(v):
                                collector = self.visit(v, collector)
                            else:
                                collector.add_bind(v, lambda i: "?")
            else:
                collector.add_bind(value, lambda i: "?")
            return collector

        if o.positional_binds:
            # Process positional bind parameters (?)
            # Check if we have nested BoundSqlLiteral nodes
            from arel.nodes.bound_sql_literal import BoundSqlLiteral
            has_nested = any(isinstance(bind, BoundSqlLiteral) for bind in o.positional_binds)

            if has_nested:
                # When there are nested BoundSqlLiteral nodes, expand them
                # Process all bind parameters, expanding nested literals
                for bind_value in o.positional_binds:
                    if bind_index > 0:
                        collector << ", "
                    collector = new_bind(bind_value)
                    bind_index += 1
            else:
                # Normal processing: match placeholders with binds
                parts = re.split(r'(\?)', o.sql_with_placeholders)
                for part in parts:
                    if part == '?':
                        if bind_index < len(o.positional_binds):
                            value = o.positional_binds[bind_index]
                            bind_index += 1
                            collector = new_bind(value)
                        else:
                            collector << part
                    else:
                        collector << part
        else:
            # Process named bind parameters (:name)
            parts = re.split(r'(:)(?<!::)([a-zA-Z]\w*)', o.sql_with_placeholders)
            i = 0
            while i < len(parts):
                if parts[i] == ':' and i + 1 < len(parts):
                    name = parts[i + 1]
                    if name in o.named_binds:
                        value = o.named_binds[name]
                        collector = new_bind(value)
                        i += 2
                    else:
                        collector << parts[i]
                        i += 1
                else:
                    collector << parts[i]
                    i += 1

        return collector

    def visit_arel_nodes_fragments_Fragments(self, o: Any, collector: Any) -> Any:
        return self.inject_join(o.values, collector, " ")

    def visit_arel_nodes_casted_Casted(self, o: Any, collector: Any) -> Any:
        collector << self.quote(o.value_for_database())
        return collector

    def visit_arel_nodes_casted_Quoted(self, o: Any, collector: Any) -> Any:
        collector << self.quote(o.expr)
        return collector

    def visit_builtins_int(self, o: int, collector: Any) -> Any:
        collector << str(o)
        return collector

    def visit_builtins_float(self, o: float, collector: Any) -> Any:
        collector << str(o)
        return collector

    def visit_builtins_bool(self, o: bool, collector: Any) -> Any:
        collector << self.quote(o)
        return collector

    def visit_builtins_str(self, o: str, collector: Any) -> Any:
        collector << self.quote(o)
        return collector

    def visit_builtins_list(self, o: list, collector: Any) -> Any:
        return self.inject_join(o, collector, ", ")

    def visit_builtins_set(self, o: set, collector: Any) -> Any:
        return self.inject_join(list(o), collector, ", ")

    def visit_builtins_dict(self, o: dict, collector: Any) -> Any:
        collector << self.quote(str(o))
        return collector

    def visit_builtins_type(self, o: type, collector: Any) -> Any:
        collector << self.quote(o.__name__)
        return collector

    def visit_datetime_datetime(self, o: Any, collector: Any) -> Any:
        from datetime import datetime
        if isinstance(o, datetime):
            collector << self.quote(o.strftime("%Y-%m-%d %H:%M:%S"))
        return collector

    def visit_datetime_date(self, o: Any, collector: Any) -> Any:
        from datetime import date
        if isinstance(o, date):
            collector << self.quote(o.strftime("%Y-%m-%d"))
        return collector

    def visit_decimal_Decimal(self, o: Any, collector: Any) -> Any:
        from decimal import Decimal
        if isinstance(o, Decimal):
            collector << str(o)
        return collector

    def visit_arel_select_manager_SelectManager(self, o: Any, collector: Any) -> Any:
        collector << "("
        collector = self.visit(o.ast, collector)
        collector << ")"
        return collector

    def visit_list(self, o: List[Any], collector: Any) -> Any:
        return self.inject_join(o, collector, ", ")

    # Helper methods

    def unboundable(self, value: Any) -> bool:
        from arel.nodes.bind_param import BindParam
        from arel.nodes.sql_literal import SqlLiteral
        from arel.nodes.bound_sql_literal import BoundSqlLiteral
        return isinstance(value, (BindParam, SqlLiteral, BoundSqlLiteral))

    def quote(self, value: Any) -> str:
        return self.connection.quote(value)

    def quote_table_name(self, name: str) -> str:
        return self.connection.quote_table_name(name)

    def quote_column_name(self, name: str) -> str:
        return self.connection.quote_column_name(name)

    def maybe_visit(self, thing: Any, collector: Any) -> Any:
        if thing is None:
            return collector
        collector << " "
        return self.visit(thing, collector)

    def inject_join(self, list_val: List[Any], collector: Any, join_str: str) -> Any:
        for i, x in enumerate(list_val):
            if i > 0:
                collector << join_str
            collector = self.visit(x, collector)
        return collector

    def collect_nodes_for(self, nodes: List[Any], collector: Any, spacer: str, connector: str = ", ") -> None:
        if nodes:
            collector << spacer
            self.inject_join(nodes, collector, connector)

    def infix_value(self, o: Any, collector: Any, value: str) -> Any:
        collector = self.visit(o.left, collector)
        collector << value
        return self.visit(o.right, collector)

    def infix_value_with_paren(self, o: Any, collector: Any, value: str, suppress_parens: bool = False) -> Any:
        from arel.nodes.binary import Union, UnionAll
        if not suppress_parens:
            collector << "( "

        # Recursively handle nested Union/UnionAll nodes
        if type(o.left) == type(o):  # Same class (Union or UnionAll)
            collector = self.infix_value_with_paren(o.left, collector, value, True)
        else:
            collector = self.grouping_parentheses(o.left, collector, False)

        collector << value

        if type(o.right) == type(o):  # Same class (Union or UnionAll)
            collector = self.infix_value_with_paren(o.right, collector, value, True)
        else:
            collector = self.grouping_parentheses(o.right, collector, False)

        if not suppress_parens:
            collector << " )"
        return collector

    def grouping_parentheses(self, o: Any, collector: Any, always_wrap_selects: bool = True) -> Any:
        from arel.nodes.select_statement import SelectStatement
        if isinstance(o, SelectStatement) and (always_wrap_selects or self.require_parentheses(o)):
            collector << "("
            collector = self.visit(o, collector)
            collector << ")"
            return collector
        else:
            return self.visit(o, collector)

    def require_parentheses(self, o: Any) -> bool:
        from arel.nodes.select_statement import SelectStatement
        if isinstance(o, SelectStatement):
            return bool(o.orders) or o.limit is not None or o.offset is not None
        return False

    def visit_arel_nodes_with__With(self, o: Any, collector: Any) -> Any:
        collector << "WITH "
        return self.collect_ctes(o.children, collector)

    def visit_arel_nodes_with__WithRecursive(self, o: Any, collector: Any) -> Any:
        collector << "WITH RECURSIVE "
        return self.collect_ctes(o.children, collector)

    def visit_arel_nodes_cte_With(self, o: Any, collector: Any) -> Any:
        collector << "WITH "
        return self.collect_ctes(o.children, collector)

    def visit_arel_nodes_cte_WithRecursive(self, o: Any, collector: Any) -> Any:
        collector << "WITH RECURSIVE "
        return self.collect_ctes(o.children, collector)

    def visit_arel_nodes_cte_Cte(self, o: Any, collector: Any) -> Any:
        # For CTE names, if it's a SqlLiteral, don't quote it
        from arel.nodes.sql_literal import SqlLiteral
        if isinstance(o.name, SqlLiteral):
            collector << str(o.name)
        else:
            collector << self.quote_table_name(o.name)
        collector << " AS "

        if o.materialized is True:
            collector << "MATERIALIZED "
        elif o.materialized is False:
            collector << "NOT MATERIALIZED "

        collector = self.visit(o.relation, collector)
        return collector

    def collect_ctes(self, children: Any, collector: Any) -> Any:
        for i, child in enumerate(children):
            if i > 0:
                collector << ", "
            collector = self.visit(child.to_cte(), collector)
        return collector

    def visit_arel_nodes_binary_Union(self, o: Any, collector: Any) -> Any:
        return self.infix_value_with_paren(o, collector, " UNION ")

    def visit_arel_nodes_binary_UnionAll(self, o: Any, collector: Any) -> Any:
        return self.infix_value_with_paren(o, collector, " UNION ALL ")

    def visit_arel_nodes_binary_Intersect(self, o: Any, collector: Any) -> Any:
        collector << "( "
        collector = self.infix_value(o, collector, " INTERSECT ")
        collector << " )"
        return collector

    def visit_arel_nodes_binary_Except(self, o: Any, collector: Any) -> Any:
        collector << "( "
        collector = self.infix_value(o, collector, " EXCEPT ")
        collector << " )"
        return collector

    def visit_arel_nodes_named_function_NamedFunction(self, o: Any, collector: Any) -> Any:
        if hasattr(collector, 'retryable'):
            collector.retryable = False
        collector << o.name
        collector << "("
        if o.distinct:
            collector << "DISTINCT "
        self.inject_join(o.expressions, collector, ", ")
        collector << ")"
        return collector

    def visit_arel_nodes_extract_Extract(self, o: Any, collector: Any) -> Any:
        collector << f"EXTRACT({o.field.upper()} FROM "
        collector = self.visit(o.expr, collector)
        collector << ")"
        return collector

    def visit_arel_nodes_comment_Comment(self, o: Any, collector: Any) -> Any:
        """Visit Comment node - append SQL comments"""
        comments = []
        for v in o.values:
            # Sanitize comment - remove */ and /* to prevent SQL injection
            sanitized = str(v).replace("*/", "").replace("/*", "")
            comments.append(f"/* {sanitized} */")
        collector << " ".join(comments)
        return collector

    def aggregate(self, name: str, o: Any, collector: Any) -> Any:
        collector << f"{name}("
        if o.distinct:
            collector << "DISTINCT "
        self.inject_join(o.expressions, collector, ", ")
        collector << ")"
        return collector
