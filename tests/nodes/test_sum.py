import pytest
from arel import Table
from arel.nodes.functions import Sum
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestSum:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.engine.connection.visitor.accept(node, SQLString()).value

    def test_should_alias_the_sum(self):
        table = Table('users')
        sql = self.compile(table['id'].sum().as_("foo"))
        must_be_like(sql, 'SUM("users"."id") AS foo')

    def test_equality_with_equal_ivars(self):
        array = [Sum(["foo"]), Sum(["foo"])]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Sum(["foo"]), Sum(["foo!"])]
        assert len(set(array)) == 2

    def test_should_order_the_sum(self):
        table = Table('users')
        sql = self.compile(table['id'].sum().desc())
        must_be_like(sql, 'SUM("users"."id") DESC')

