from __future__ import annotations
from typing import Any, List, Optional
from arel.tree_manager import TreeManager
from arel.nodes.insert_statement import InsertStatement
from arel.nodes.values_list import ValuesList
from arel.nodes.sql_literal import SqlLiteral

class InsertManager(TreeManager):
    def __init__(self, table: Any = None):
        super().__init__()
        self._ast = InsertStatement(table)

    def into(self, table: Any) -> 'InsertManager':
        self._ast.relation = table
        return self

    @property
    def columns(self) -> List[Any]:
        return self._ast.columns

    @property
    def values(self) -> Any:
        return self._ast.values

    @values.setter
    def values(self, val: Any) -> None:
        self._ast.values = val

    def select(self, select: Any) -> None:
        self._ast.select = select

    def insert(self, fields: Any) -> 'InsertManager':
        if not fields:
            return self

        if isinstance(fields, str):
            self._ast.values = SqlLiteral(fields)
        else:
            if self._ast.relation is None:
                # In Ruby: @ast.relation ||= fields.first.first.relation
                # This assumes fields is a dict or list of pairs where keys are Attributes
                first_key = list(fields.keys())[0] if isinstance(fields, dict) else fields[0][0]
                self._ast.relation = first_key.relation

            values = []
            items = fields.items() if isinstance(fields, dict) else fields
            for column, value in items:
                self._ast.columns.append(column)
                values.append(value)
            self._ast.values = self.create_values(values)

        return self

    def create_values(self, values: List[Any]) -> ValuesList:
        return ValuesList([values])

    def create_values_list(self, rows: List[List[Any]]) -> ValuesList:
        return ValuesList(rows)

