import pytest
import copy
from arel import Table
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestExtract:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.engine.connection.visitor.accept(node, SQLString()).value

    def test_should_extract_field(self):
        table = Table('users')
        sql = self.compile(table['timestamp'].extract("date"))
        must_be_like(sql, 'EXTRACT(DATE FROM "users"."timestamp")')

    def test_should_alias_the_extract(self):
        table = Table('users')
        sql = self.compile(table['timestamp'].extract("date").as_("foo"))
        must_be_like(sql, 'EXTRACT(DATE FROM "users"."timestamp") AS foo')

    def test_should_not_mutate_the_extract(self):
        table = Table('users')
        extract = table['timestamp'].extract("date")
        before = copy.copy(extract)
        extract.as_("foo")
        assert extract == before

    def test_equality_with_equal_ivars(self):
        table = Table('users')
        array = [table['attr'].extract("foo"), table['attr'].extract("foo")]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        table = Table('users')
        array = [table['attr'].extract("foo"), table['attr'].extract("bar")]
        assert len(set(array)) == 2

