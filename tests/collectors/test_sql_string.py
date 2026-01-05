import pytest
from arel import Table
from arel.nodes.bind_param import BindParam
from arel.select_manager import SelectManager
from arel.visitors.to_sql import ToSql
from arel.collectors.sql_string import SQLString
from tests.python.helper import MockEngine, must_be_like

class TestSqlString:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def collect(self, node):
        return self.engine.connection.visitor.accept(node, SQLString())

    def compile(self, node):
        return self.collect(node).value

    def ast_with_binds(self):
        table = Table('users')
        manager = SelectManager(table)
        manager.where(table['age'].eq(BindParam("hello")))
        manager.where(table['name'].eq(BindParam("world")))
        return manager.ast

    def test_compile(self):
        sql = self.compile(self.ast_with_binds())
        must_be_like(sql, 'SELECT FROM "users" WHERE "users"."age" = ? AND "users"."name" = ?')

    def test_returned_sql_uses_utf8_encoding(self):
        sql = self.compile(self.ast_with_binds())
        # In Python strings are UTF-8 by default, check that it's a string
        assert isinstance(sql, str)

