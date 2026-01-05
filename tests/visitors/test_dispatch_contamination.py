import pytest
from arel import Table
from arel.nodes.binary import Union
from arel.nodes.true import True_
from arel.nodes.false import False_
from arel.visitors.visitor import Visitor
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine

class TestDispatchContamination:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine
        self.table = Table('users')

    def test_dispatches_properly_after_failing_upwards(self):
        node = Union(True_(), False_())
        sql_before = node.to_sql()
        assert sql_before == "( TRUE UNION FALSE )"

        class CustomVisitor(Visitor):
            def visit_arel_nodes_binary_Union(self, o, collector=None):
                if collector is None:
                    return None
                return collector

            def visit_arel_nodes_true_True_(self, o, collector=None):
                # Alias to Union visitor
                return self.visit_arel_nodes_binary_Union(o, collector)

            def visit_arel_nodes_false_False_(self, o, collector=None):
                # Alias to Union visitor
                return self.visit_arel_nodes_binary_Union(o, collector)

        visitor = CustomVisitor()
        visitor.accept(node)

        sql_after = node.to_sql()
        assert sql_after == "( TRUE UNION FALSE )"
        assert sql_before == sql_after

