import pytest
from arel import Table
from arel.nodes.select_statement import SelectStatement
from arel.nodes.unary import Offset, Lock
from arel.nodes.binary import IsNotDistinctFrom
from arel import sql
from arel.nodes import build_quoted
from arel.visitors.sqlite import SQLite
from arel.collectors.sql_string import SQLString
from tests.python.helper import MockEngine, must_be_like

class TestSQLite:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(SQLite)
        Table.engine = self.engine
        self.visitor = self.engine.connection.visitor

    def compile(self, node):
        return self.visitor.accept(node, SQLString()).value

    def test_defaults_limit_to_minus_one(self):
        stmt = SelectStatement()
        stmt.offset = Offset(1)
        sql_result = self.compile(stmt)
        # SQLite adds LIMIT -1 when there's OFFSET without LIMIT
        must_be_like(sql_result, "SELECT LIMIT -1 OFFSET 1")

    def test_does_not_support_locking(self):
        node = Lock(sql("FOR UPDATE"))
        sql_result = self.compile(node)
        assert sql_result == ""

    def test_should_construct_a_valid_generic_sql_statement_for_is_not_distinct_from(self):
        test = Table('users')['name'].is_not_distinct_from("Aaron Patterson")
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."name" IS \'Aaron Patterson\'')

    def test_should_handle_column_names_on_both_sides(self):
        test = Table('users')['first_name'].is_not_distinct_from(Table('users')['last_name'])
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" IS "users"."last_name"')

    def test_should_handle_nil(self):
        table = Table('users')
        val = build_quoted(None, table['active'])
        from arel.nodes.binary import IsNotDistinctFrom
        sql_result = self.compile(IsNotDistinctFrom(table['name'], val))
        must_be_like(sql_result, '"users"."name" IS NULL')

    def test_is_distinct_from_should_handle_column_names_on_both_sides(self):
        test = Table('users')['first_name'].is_distinct_from(Table('users')['last_name'])
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" IS NOT "users"."last_name"')

    def test_is_distinct_from_should_handle_nil(self):
        table = Table('users')
        val = build_quoted(None, table['active'])
        from arel.nodes.binary import IsDistinctFrom
        sql_result = self.compile(IsDistinctFrom(table['name'], val))
        must_be_like(sql_result, '"users"."name" IS NOT NULL')

