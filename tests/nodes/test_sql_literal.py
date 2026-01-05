import pytest
import arel
from arel.nodes import SqlLiteral, Fragments
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestSqlLiteral:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        arel.Table.engine = self.engine
        self.visitor = self.engine.connection.visitor

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.visitor.accept(node, SQLString()).value

    def test_makes_a_sql_literal_node(self):
        sql = arel.sql("foo")
        assert isinstance(sql, SqlLiteral)

    def test_makes_a_count_node(self):
        node = SqlLiteral("*").count()
        must_be_like(self.compile(node), "COUNT(*)")

    def test_makes_a_distinct_node(self):
        node = SqlLiteral("*").count(True)
        must_be_like(self.compile(node), "COUNT(DISTINCT *)")

    def test_makes_an_equality_node(self):
        node = SqlLiteral("foo").eq(1)
        must_be_like(self.compile(node), "foo = 1")

    def test_is_equal_with_equal_contents(self):
        array = [SqlLiteral("foo"), SqlLiteral("foo")]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_contents(self):
        array = [SqlLiteral("foo"), SqlLiteral("bar")]
        assert len(set(array)) == 2

    def test_makes_a_grouping_node_with_an_or_node(self):
        node = SqlLiteral("foo").eq_any([1, 2])
        must_be_like(self.compile(node), "(foo = 1 OR foo = 2)")

    def test_makes_a_grouping_node_with_an_and_node(self):
        node = SqlLiteral("foo").eq_all([1, 2])
        must_be_like(self.compile(node), "(foo = 1 AND foo = 2)")

    def test_generates_a_fragments_node(self):
        sql1 = arel.sql("SELECT *")
        sql2 = arel.sql("FROM users")
        fragments = sql1 + sql2
        assert isinstance(fragments, Fragments)
        assert fragments.values == [sql1, sql2]

    def test_fails_if_joined_with_something_that_is_not_an_arel_node(self):
        sql = arel.sql("SELECT *")
        with pytest.raises((ValueError, TypeError)):
            sql + "Not a node"

    def test_serializes_into_yaml(self):
        try:
            import yaml
            yaml_literal = SqlLiteral("foo").to_yaml()
            assert yaml.safe_load(yaml_literal) == "foo"
        except ImportError:
            pytest.skip("PyYAML not installed")
