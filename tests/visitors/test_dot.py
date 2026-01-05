import pytest
import re
from arel.visitors.dot import Dot
from arel.collectors.plain_string import PlainString
from arel.nodes.functions import Sum, Exists, Max, Min, Avg
from arel.nodes import NamedFunction, Not, Group, On, Grouping, Offset, UnqualifiedColumn, ValuesList, Limit
from arel.nodes import Assignment, Between, DoesNotMatch, Equality, GreaterThan, GreaterThanOrEqual
from arel.nodes import In, LessThan, LessThanOrEqual, Matches, NotEqual, NotIn, TableAlias, As, JoinSource, Casted
from arel.nodes import And, Or
from arel.nodes import BindParam, Distinct
from arel.nodes import InfixOperation
from arel.nodes.regexp import Regexp, NotRegexp
from arel.nodes import SelectCore, SelectStatement, InsertStatement, UpdateStatement, DeleteStatement
from arel.nodes.ordering import Ascending
from arel.nodes.case import Case, When, Else
from arel.nodes.window import CurrentRow
from arel.nodes.unary_operation import UnaryOperation
from arel.nodes.cte import With
from arel import Table, build_quoted

class TestDot:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.visitor = Dot()

    def assert_edge(self, edge_name, dot_string):
        pattern = f'->.*label="{re.escape(str(edge_name))}"'
        assert re.search(pattern, dot_string), f"Edge '{edge_name}' not found in dot string"

    def test_arel_nodes_sum(self):
        op = Sum("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_exists(self):
        op = Exists("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_max(self):
        op = Max("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_min(self):
        op = Min("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_avg(self):
        op = Avg("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_named_function(self):
        func = NamedFunction("omg", "omg")
        self.visitor.accept(func, PlainString())
        pass

    def test_arel_nodes_not(self):
        op = Not("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_group(self):
        op = Group("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_on(self):
        op = On("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_grouping(self):
        op = Grouping("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_offset(self):
        op = Offset("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_ordering(self):
        from arel.nodes.ordering import Ascending
        op = Ascending("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_unqualified_column(self):
        op = UnqualifiedColumn("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_values_list(self):
        op = ValuesList("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_limit(self):
        op = Limit("a")
        self.visitor.accept(op, PlainString())
        pass

    def test_arel_nodes_assignment(self):
        binary = Assignment("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_between(self):
        binary = Between("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_does_not_match(self):
        binary = DoesNotMatch("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_equality(self):
        binary = Equality("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_greater_than(self):
        binary = GreaterThan("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_greater_than_or_equal(self):
        binary = GreaterThanOrEqual("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_in(self):
        binary = In("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_less_than(self):
        binary = LessThan("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_less_than_or_equal(self):
        binary = LessThanOrEqual("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_matches(self):
        binary = Matches("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_not_equal(self):
        binary = NotEqual("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_not_in(self):
        binary = NotIn("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_table_alias(self):
        binary = TableAlias("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_as(self):
        binary = As("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_join_source(self):
        binary = JoinSource("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_casted(self):
        binary = Casted("a", "b")
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_and(self):
        binary = And(["a", "b"])
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_or(self):
        binary = Or(["a", "b"])
        self.visitor.accept(binary, PlainString())
        pass

    def test_arel_nodes_bind_param(self):
        node = BindParam(1)
        collector = PlainString()
        dot = self.visitor.accept(node, collector).value
        assert 'label="<f0>' in dot and 'BindParam' in dot

    def test_arel_nodes_current_row(self):
        node = CurrentRow()
        collector = PlainString()
        dot = self.visitor.accept(node, collector).value
        assert 'label="<f0>' in dot and 'CurrentRow' in dot

    def test_arel_nodes_distinct(self):
        node = Distinct()
        collector = PlainString()
        dot = self.visitor.accept(node, collector).value
        assert 'label="<f0>' in dot and 'Distinct' in dot

    def test_arel_nodes_case_and_friends(self):
        foo = build_quoted("foo")
        node = Case(foo)
        node.conditions = [When(foo, build_quoted(1))]
        node.default = Else(build_quoted(0))

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'Case' in dot
        self.assert_edge("case", dot)
        self.assert_edge("conditions", dot)
        self.assert_edge("default", dot)
        assert 'label="<f0>' in dot and 'When' in dot
        assert 'label="<f0>' in dot and 'Else' in dot

    def test_arel_nodes_infix_operation(self):
        node = InfixOperation("&&", build_quoted(1), build_quoted(2))

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'InfixOperation' in dot
        self.assert_edge("operator", dot)
        self.assert_edge("left", dot)
        self.assert_edge("right", dot)

    def test_arel_nodes_regexp(self):
        table = Table('users')
        node = Regexp(table['name'], build_quoted("foo%"))

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'Regexp' in dot
        self.assert_edge("left", dot)
        self.assert_edge("right", dot)
        self.assert_edge("case_sensitive", dot)

    def test_arel_nodes_not_regexp(self):
        table = Table('users')
        node = NotRegexp(table['name'], build_quoted("foo%"))

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'NotRegexp' in dot
        self.assert_edge("left", dot)
        self.assert_edge("right", dot)
        self.assert_edge("case_sensitive", dot)

    def test_arel_nodes_unary_operation(self):
        from arel.nodes.unary_operation import UnaryOperation
        node = UnaryOperation("-", 1)

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'UnaryOperation' in dot
        self.assert_edge("operator", dot)
        self.assert_edge("expr", dot)

    def test_arel_nodes_with(self):
        from arel.nodes.cte import With
        node = With(["query1", "query2", "query3"])

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'With' in dot
        self.assert_edge("0", dot)
        self.assert_edge("1", dot)
        self.assert_edge("2", dot)

    def test_arel_nodes_select_core(self):
        node = SelectCore()

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'SelectCore' in dot
        self.assert_edge("source", dot)
        self.assert_edge("projections", dot)
        self.assert_edge("wheres", dot)
        self.assert_edge("windows", dot)
        self.assert_edge("groups", dot)
        self.assert_edge("comment", dot)
        self.assert_edge("havings", dot)
        self.assert_edge("set_quantifier", dot)
        self.assert_edge("optimizer_hints", dot)

    def test_arel_nodes_select_statement(self):
        node = SelectStatement()

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'SelectStatement' in dot
        self.assert_edge("cores", dot)
        self.assert_edge("limit", dot)
        self.assert_edge("orders", dot)
        self.assert_edge("offset", dot)
        self.assert_edge("lock", dot)
        self.assert_edge("with_", dot)

    def test_arel_nodes_insert_statement(self):
        node = InsertStatement()

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'InsertStatement' in dot
        self.assert_edge("relation", dot)
        self.assert_edge("columns", dot)
        self.assert_edge("values", dot)
        self.assert_edge("select", dot)

    def test_arel_nodes_update_statement(self):
        node = UpdateStatement()

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'UpdateStatement' in dot
        self.assert_edge("relation", dot)
        self.assert_edge("wheres", dot)
        self.assert_edge("values", dot)
        self.assert_edge("orders", dot)
        self.assert_edge("limit", dot)
        self.assert_edge("offset", dot)
        self.assert_edge("comment", dot)
        self.assert_edge("key", dot)

    def test_arel_nodes_delete_statement(self):
        node = DeleteStatement()

        dot = self.visitor.accept(node, PlainString()).value

        assert 'label="<f0>' in dot and 'DeleteStatement' in dot
        self.assert_edge("relation", dot)
        self.assert_edge("wheres", dot)
        self.assert_edge("orders", dot)
        self.assert_edge("limit", dot)
        self.assert_edge("offset", dot)
        self.assert_edge("comment", dot)
        self.assert_edge("key", dot)

