import pytest
from arel import Table
from arel.visitors.to_sql import ToSql
from arel.nodes.count import Count
from tests.python.helper import MockEngine, must_be_like

class TestCount:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.engine.connection.visitor.accept(node, SQLString()).value

    def test_should_alias_the_count(self):
        table = Table('users')
        sql = self.compile(table['id'].count().as_("foo"))
        must_be_like(sql, 'COUNT("users"."id") AS foo')

    def test_should_compare_the_count(self):
        table = Table('users')
        sql = self.compile(table['id'].count().eq(2))
        must_be_like(sql, 'COUNT("users"."id") = 2')

    def test_equality_with_equal_ivars(self):
        array = [Count(["foo"]), Count(["foo"])]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Count(["foo"]), Count(["foo!"])]
        assert len(set(array)) == 2

