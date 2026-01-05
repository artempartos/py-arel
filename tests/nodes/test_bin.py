import pytest
import copy
from arel import Table, sql
from arel.nodes.unary import Bin
from arel.visitors.to_sql import ToSql
from arel.visitors.mysql import MySQL
from arel.collectors.sql_string import SQLString
from tests.python.helper import MockEngine

class TestBin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def test_new(self):
        assert Bin("zomg")

    def test_default_to_sql(self):
        viz = self.engine.connection.visitor
        node = Bin(sql("zomg"))
        assert viz.accept(node, SQLString()).value == "zomg"

    def test_mysql_to_sql(self):
        mysql_engine = MockEngine(MySQL)
        Table.engine = mysql_engine
        viz = mysql_engine.connection.visitor
        node = Bin(sql("zomg"))
        assert viz.accept(node, SQLString()).value == "CAST(zomg AS BINARY)"

    def test_equality_with_same_ivars(self):
        array = [Bin("zomg"), Bin("zomg")]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Bin("zomg"), Bin("zomg!")]
        assert len(set(array)) == 2

