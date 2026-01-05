import pytest
from arel import Table, sql
from arel.nodes.binary import As
from arel.nodes.cte import Cte
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine

class TestAs:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def test_makes_an_as_node(self):
        attr = Table('users')['id']
        as_node = attr.as_(sql("foo"))
        assert as_node.left == attr
        assert str(as_node.right) == "foo"

    def test_converts_right_to_sql_literal_if_a_string(self):
        attr = Table('users')['id']
        as_node = attr.as_("foo")
        from arel.nodes.sql_literal import SqlLiteral
        assert isinstance(as_node.right, SqlLiteral)

    def test_converts_right_to_sql_literal_if_a_symbol(self):
        attr = Table('users')['id']
        as_node = attr.as_("foo")  # In Python there are no symbols, use string
        from arel.nodes.sql_literal import SqlLiteral
        assert isinstance(as_node.right, SqlLiteral)

    def test_is_equal_with_equal_ivars(self):
        array = [As("foo", "bar"), As("foo", "bar")]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_ivars(self):
        array = [As("foo", "bar"), As("foo", "baz")]
        assert len(set(array)) == 2

    def test_returns_a_cte_node_using_the_lhs(self):
        table = Table('users')
        as_node = As(table, "foo")
        cte_node = as_node.to_cte()

        assert isinstance(cte_node, Cte)
        assert cte_node.name == as_node.left.name
        assert cte_node.relation == as_node.right

