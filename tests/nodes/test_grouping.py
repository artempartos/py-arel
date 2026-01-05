import pytest
from arel.nodes.grouping import Grouping
from arel.nodes import build_quoted
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestGrouping:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.engine.connection.visitor.accept(node, SQLString()).value

    def test_should_create_equality_nodes(self):
        grouping = Grouping(build_quoted("foo"))
        sql = self.compile(grouping.eq("foo"))
        must_be_like(sql, "('foo') = 'foo'")

    def test_equality_with_equal_ivars(self):
        array = [Grouping("foo"), Grouping("foo")]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Grouping("foo"), Grouping("bar")]
        assert len(set(array)) == 2

