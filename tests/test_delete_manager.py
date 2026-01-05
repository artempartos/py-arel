import pytest
from arel import Table
from arel.delete_manager import DeleteManager
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestDeleteManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, manager):
        return manager.to_sql()

    def test_handles_limit_properly(self):
        table = Table('users')
        dm = DeleteManager()
        dm.take(10)
        dm.from_(table)
        dm.key = table['id']
        sql_result = self.compile(dm)
        assert 'LIMIT 10' in sql_result

    def test_uses_from(self):
        table = Table('users')
        dm = DeleteManager()
        dm.from_(table)
        sql_result = self.compile(dm)
        must_be_like(sql_result, 'DELETE FROM "users"')

    def test_from_chains(self):
        table = Table('users')
        dm = DeleteManager()
        assert dm.from_(table) == dm

    def test_uses_where_values(self):
        table = Table('users')
        dm = DeleteManager()
        dm.from_(table)
        dm.where(table['id'].eq(10))
        sql_result = self.compile(dm)
        must_be_like(sql_result, 'DELETE FROM "users" WHERE "users"."id" = 10')

    def test_where_chains(self):
        table = Table('users')
        dm = DeleteManager()
        assert dm.where(table['id'].eq(10)) == dm

