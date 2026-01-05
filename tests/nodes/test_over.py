import pytest
from arel import Table, sql
from arel.nodes.window import Window, Over
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestOver:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.engine.connection.visitor.accept(node, SQLString()).value

    def test_should_alias_the_expression(self):
        table = Table('users')
        sql_result = self.compile(table['id'].count().over().as_("foo"))
        must_be_like(sql_result, 'COUNT("users"."id") OVER () AS foo')

    def test_should_reference_the_window_definition_by_name_with_literal(self):
        table = Table('users')
        sql_result = self.compile(table['id'].count().over("foo"))
        must_be_like(sql_result, 'COUNT("users"."id") OVER "foo"')

    def test_should_reference_the_window_definition_by_name_with_sql_literal(self):
        table = Table('users')
        sql_result = self.compile(table['id'].count().over(sql("foo")))
        must_be_like(sql_result, 'COUNT("users"."id") OVER foo')

    def test_should_use_empty_definition_with_no_expression(self):
        table = Table('users')
        sql_result = self.compile(table['id'].count().over())
        must_be_like(sql_result, 'COUNT("users"."id") OVER ()')

    def test_should_use_definition_in_sub_expression(self):
        table = Table('users')
        window = Window().order(table['foo'])
        sql_result = self.compile(table['id'].count().over(window))
        must_be_like(sql_result, 'COUNT("users"."id") OVER (ORDER BY "users"."foo")')

    def test_equality_with_equal_ivars(self):
        array = [Over("foo", "bar"), Over("foo", "bar")]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Over("foo", "bar"), Over("foo", "baz")]
        assert len(set(array)) == 2

