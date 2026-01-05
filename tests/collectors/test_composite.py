import pytest
from arel import Table
from arel.nodes.bind_param import BindParam
from arel.select_manager import SelectManager
from arel.visitors.to_sql import ToSql
from arel.collectors.sql_string import SQLString
from arel.collectors.bind import Bind
from arel.collectors.composite import Composite
from tests.python.helper import MockEngine, must_be_like

class TestComposite:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def collect(self, node):
        sql_collector = SQLString()
        bind_collector = Bind()
        collector = Composite(sql_collector, bind_collector)
        return self.engine.connection.visitor.accept(node, collector)

    def compile(self, node):
        return self.collect(node).value

    def ast_with_binds(self, bvs):
        table = Table('users')
        manager = SelectManager(table)
        manager.where(table['age'].eq(BindParam(bvs[0])))
        manager.where(table['name'].eq(BindParam(bvs[1])))
        return manager.ast

    def test_composite_collector_performs_multiple_collections_at_once(self):
        sql, binds = self.compile(self.ast_with_binds(["hello", "world"]))
        must_be_like(sql, 'SELECT FROM "users" WHERE "users"."age" = ? AND "users"."name" = ?')
        assert binds == ["hello", "world"]

        sql, binds = self.compile(self.ast_with_binds(["hello2", "world3"]))
        must_be_like(sql, 'SELECT FROM "users" WHERE "users"."age" = ? AND "users"."name" = ?')
        assert binds == ["hello2", "world3"]

    def test_retryable_on_composite_collector_propagates(self):
        sql_collector = SQLString()
        bind_collector = Bind()
        collector = Composite(sql_collector, bind_collector)
        collector.retryable = True

        assert sql_collector.retryable == True
        assert bind_collector.retryable == True

