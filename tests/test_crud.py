import pytest
from arel import Table
from arel.select_manager import SelectManager
from arel.insert_manager import InsertManager
from arel.update_manager import UpdateManager
from arel.delete_manager import DeleteManager
from arel.mixins.crud import CrudMixin

class FakeCrudder(SelectManager, CrudMixin):
    def __init__(self, engine=None):
        super().__init__()
        self.engine = engine

class TestCrud:
    def test_insert_should_call_insert_on_connection(self):
        table = Table('users')
        fc = FakeCrudder()
        fc.from_(table)
        im = fc.compile_insert([[table['id'], "foo"]])
        assert isinstance(im, InsertManager)

    def test_update_should_call_update_on_connection(self):
        table = Table('users')
        fc = FakeCrudder()
        fc.from_(table)
        from arel.attributes.attribute import Attribute
        stmt = fc.compile_update([[table['id'], "foo"]], Attribute(table, "id"))
        assert isinstance(stmt, UpdateManager)

    def test_delete_should_call_delete_on_connection(self):
        table = Table('users')
        fc = FakeCrudder()
        fc.from_(table)
        stmt = fc.compile_delete()
        assert isinstance(stmt, DeleteManager)

