import pytest
from arel import Table
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestFilter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.engine.connection.visitor.accept(node, SQLString()).value

    def test_should_add_filter_to_expression(self):
        table = Table('users')
        sql = self.compile(table['id'].count().filter(table['income'].gteq(40000)))
        must_be_like(sql, 'COUNT("users"."id") FILTER (WHERE "users"."income" >= 40000)')

    def test_should_alias_the_expression(self):
        table = Table('users')
        sql = self.compile(table['id'].count().filter(table['income'].gteq(40000)).as_("rich_users_count"))
        must_be_like(sql, 'COUNT("users"."id") FILTER (WHERE "users"."income" >= 40000) AS rich_users_count')

    def test_should_reference_the_window_definition_by_name(self):
        table = Table('users')
        from arel.nodes.window import Window
        window = Window().partition(table['year'])
        sql = self.compile(table['id'].count().filter(table['income'].gteq(40000)).over(window))
        must_be_like(sql, 'COUNT("users"."id") FILTER (WHERE "users"."income" >= 40000) OVER (PARTITION BY "users"."year")')

