import pytest
from arel import Table
from arel.nodes.bind_param import BindParam
from arel.select_manager import SelectManager
from arel.visitors.to_sql import ToSql
from arel.collectors.bind import Bind
from tests.python.helper import MockEngine

class TestBind:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def collect(self, node):
        return self.engine.connection.visitor.accept(node, Bind())

    def compile(self, node):
        return self.collect(node).value

    def ast_with_binds(self, bvs):
        table = Table('users')
        manager = SelectManager(table)
        manager.where(table['age'].eq(BindParam(bvs[0])))
        manager.where(table['name'].eq(BindParam(bvs[1])))
        return manager.ast

    def test_compile_gathers_all_bind_params(self):
        binds = self.compile(self.ast_with_binds(["hello", "world"]))
        assert binds == ["hello", "world"]

        binds = self.compile(self.ast_with_binds(["hello2", "world3"]))
        assert binds == ["hello2", "world3"]

