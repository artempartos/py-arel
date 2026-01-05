from typing import Any, Optional

class CrudMixin:
    def compile_insert(self, values: Any) -> 'InsertManager':
        im = self.create_insert()
        im.insert(values)
        return im

    def create_insert(self) -> 'InsertManager':
        from arel.insert_manager import InsertManager
        return InsertManager()

    def compile_update(self, values: Any, key: Any = None) -> 'UpdateManager':
        from arel.update_manager import UpdateManager
        um = UpdateManager(self.source)
        um.set(values)
        um.take(self.limit)
        um.skip(self.offset)
        um.order(*self.orders)
        um.wheres = self.constraints
        um.comment(self.comment())
        um.key = key

        um._ast.groups = self._ctx.groups
        for h in self._ctx.havings:
            um.having(h)
        return um

    def compile_delete(self, key: Any = None) -> 'DeleteManager':
        from arel.delete_manager import DeleteManager
        dm = DeleteManager(self.source)
        dm.take(self.limit)
        dm.skip(self.offset)
        dm.order(*self.orders)
        dm.wheres = self.constraints
        dm.comment(self.comment())
        dm.key = key
        dm._ast.groups = self._ctx.groups
        for h in self._ctx.havings:
            dm.having(h)
        return dm

