import pytest
from arel import Table
from arel.nodes.homogeneous_in import HomogeneousIn
from arel.nodes.named_function import NamedFunction
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestHomogeneousIn:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.engine.connection.visitor.accept(node, SQLString()).value

    def test_in(self):
        table = Table('users')
        expr = HomogeneousIn(["Bobby", "Robert"], table['name'], 'in')
        sql = self.compile(expr)
        # HomogeneousIn uses placeholders for values
        must_be_like(sql, '"users"."name" IN (?, ?)')

    def test_custom_attribute_node(self):
        table = Table('users')
        node = NamedFunction("COALESCE", [table['nickname'], table['name']])
        expr = HomogeneousIn(["Bobby", "Robert"], node, 'in')
        sql = self.compile(expr)
        # HomogeneousIn uses placeholders for values
        must_be_like(sql, 'COALESCE("users"."nickname", "users"."name") IN (?, ?)')

