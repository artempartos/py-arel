from typing import Any
from arel.table import Table
from arel.select_manager import SelectManager
from arel.insert_manager import InsertManager
from arel.update_manager import UpdateManager
from arel.delete_manager import DeleteManager
from arel.nodes import build_quoted, SqlLiteral

def sql(string: str, *args, retryable: bool = False) -> Any:
    from arel.nodes.bound_sql_literal import BoundSqlLiteral
    if args:
        # If there are additional arguments, create BoundSqlLiteral
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            # sql("?", [1, 2, 3])
            return BoundSqlLiteral(string, positional_binds=list(args[0]), named_binds={})
        elif len(args) == 1 and isinstance(args[0], dict):
            # sql(":id", {"id": 1})
            return BoundSqlLiteral(string, positional_binds=[], named_binds=args[0])
        else:
            # sql("?", 1, 2, 3) -> positional_binds=[1, 2, 3]
            return BoundSqlLiteral(string, positional_binds=list(args), named_binds={})
    return SqlLiteral(string, retryable=retryable)

def star() -> SqlLiteral:
    return SqlLiteral("*")

def arel_node(obj: any) -> bool:
    from arel.nodes.node import Node
    from arel.attributes.attribute import Attribute
    return isinstance(obj, (Node, SqlLiteral, Attribute))

__all__ = [
    'Table', 'SelectManager', 'InsertManager', 'UpdateManager', 'DeleteManager',
    'sql', 'star', 'arel_node', 'build_quoted'
]

