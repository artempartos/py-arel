import pytest
from arel import Table
from arel.nodes.bind_param import BindParam
from arel.select_manager import SelectManager
from arel.visitors.to_sql import ToSql
from arel.collectors.sql_string import SQLString
from arel.collectors.substitute_binds import SubstituteBinds
from tests.python.helper import MockEngine, must_be_like

class TestSubstituteBindCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def ast_with_binds(self):
        table = Table('users')
        manager = SelectManager(table)
        manager.where(table['age'].eq(BindParam("hello")))
        manager.where(table['name'].eq(BindParam("world")))
        return manager.ast

    def compile(self, node, quoter):
        collector = SubstituteBinds(quoter, SQLString())
        return self.engine.connection.visitor.accept(node, collector).value

    def test_compile(self):
        class Quoter:
            def quote(self, val):
                return str(val)

        quoter = Quoter()
        sql = self.compile(self.ast_with_binds(), quoter)
        must_be_like(sql, 'SELECT FROM "users" WHERE "users"."age" = hello AND "users"."name" = world')

    def test_quoting_is_delegated_to_quoter(self):
        class Quoter:
            def quote(self, val):
                return f'"{val}"'  # Use double quotes as in Ruby

        quoter = Quoter()
        sql = self.compile(self.ast_with_binds(), quoter)
        must_be_like(sql, 'SELECT FROM "users" WHERE "users"."age" = "hello" AND "users"."name" = "world"')

