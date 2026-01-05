from __future__ import annotations
from typing import Any
from arel.tree_manager import TreeManager
from arel.nodes.update_statement import UpdateStatement
from arel.nodes.binary import Assignment
from arel.nodes.unqualified_column import UnqualifiedColumn
from arel.nodes.sql_literal import SqlLiteral
from arel.nodes.unary import Group

class UpdateManager(TreeManager, TreeManager.StatementMethods):
    def __init__(self, table: Any = None):
        super().__init__()
        self._ast = UpdateStatement(table)

    def table(self, table: Any) -> 'UpdateManager':
        self._ast.relation = table
        return self

    def set(self, values: Any) -> 'UpdateManager':
        if isinstance(values, (str, SqlLiteral)):
            self._ast.values = [values]
        else:
            items = values.items() if isinstance(values, dict) else values
            self._ast.values = [
                Assignment(UnqualifiedColumn(column), value)
                for column, value in items
            ]
        return self

    def group(self, *columns: Any) -> 'UpdateManager':
        for column in columns:
            if isinstance(column, str):
                column = SqlLiteral(column)
            self._ast.groups.append(Group(column))
        return self

    def having(self, expr: Any) -> 'UpdateManager':
        self._ast.havings.append(expr)
        return self

    def comment(self, value: str) -> 'UpdateManager':
        self._ast.comment = value
        return self
