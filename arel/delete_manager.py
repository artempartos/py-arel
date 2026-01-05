from __future__ import annotations
from typing import Any
from arel.tree_manager import TreeManager
from arel.nodes.delete_statement import DeleteStatement
from arel.nodes.sql_literal import SqlLiteral
from arel.nodes.unary import Group

class DeleteManager(TreeManager, TreeManager.StatementMethods):
    def __init__(self, table: Any = None):
        super().__init__()
        self._ast = DeleteStatement(table)

    def from_(self, relation: Any) -> 'DeleteManager':
        self._ast.relation = relation
        return self

    def group(self, *columns: Any) -> 'DeleteManager':
        for column in columns:
            if isinstance(column, str):
                column = SqlLiteral(column)
            self._ast.groups.append(Group(column))
        return self

    def having(self, expr: Any) -> 'DeleteManager':
        self._ast.havings.append(expr)
        return self

    def comment(self, value: str) -> 'DeleteManager':
        self._ast.comment = value
        return self

