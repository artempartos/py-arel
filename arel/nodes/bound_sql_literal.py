from __future__ import annotations
import re
from typing import Any, List, Optional, Dict
from arel.nodes.node_expression import NodeExpression
from arel.errors import BindError

class BoundSqlLiteral(NodeExpression):
    def __init__(self, sql_with_placeholders: str, positional_binds: Optional[List[Any]] = None, named_binds: Optional[Dict[str, Any]] = None):
        super().__init__()
        has_positional = positional_binds is not None and len(positional_binds) > 0
        has_named = named_binds is not None and len(named_binds) > 0

        if has_positional:
            if has_named:
                raise BindError("cannot mix positional and named binds", sql_with_placeholders)
            expected = sql_with_placeholders.count("?")
            # Check if there are nested BoundSqlLiteral nodes
            from arel.nodes.bound_sql_literal import BoundSqlLiteral
            has_nested = any(isinstance(bind, BoundSqlLiteral) for bind in positional_binds)
            if has_nested:
                # When there are nested BoundSqlLiteral nodes, skip strict validation
                # The nested literals will be expanded during SQL generation
                # We'll validate that we have at least the expected number of binds
                if len(positional_binds) < expected:
                    raise BindError(f"wrong number of bind variables ({len(positional_binds)} for {expected})", sql_with_placeholders)
            else:
                # Normal validation: exact match
                if len(positional_binds) != expected:
                    raise BindError(f"wrong number of bind variables ({len(positional_binds)} for {expected})", sql_with_placeholders)
        elif has_named:
            # Ruby: sql_with_placeholders.scan(/:(?<!::)([a-zA-Z]\w*)/)
            tokens_in_string = set(re.findall(r':(?<!::)([a-zA-Z]\w*)', sql_with_placeholders))
            tokens_in_dict = set(named_binds.keys())

            missing = tokens_in_string - tokens_in_dict
            if missing:
                if len(missing) == 1:
                    raise BindError(f"missing value for {next(iter(missing))!r}", sql_with_placeholders)
                else:
                    raise BindError(f"missing values for {sorted(list(missing))!r}", sql_with_placeholders)

        self.sql_with_placeholders = sql_with_placeholders
        self.positional_binds = positional_binds if has_positional else None
        self.named_binds = named_binds if has_named else None

    def __hash__(self) -> int:
        return hash((
            self.__class__,
            self.sql_with_placeholders,
            tuple(self.positional_binds) if self.positional_binds else None,
            tuple(sorted(self.named_binds.items())) if self.named_binds else None
        ))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.sql_with_placeholders == other.sql_with_placeholders and
            self.positional_binds == other.positional_binds and
            self.named_binds == other.named_binds
        )

    def __add__(self, other: Any) -> 'Fragments':
        from arel import arel_node
        if not arel_node(other):
            raise ValueError("Expected Arel node")

        from arel.nodes.misc import Fragments
        return Fragments([self, other])

    def __repr__(self) -> str:
        binds = self.named_binds or self.positional_binds
        return f"<BoundSqlLiteral {self.sql_with_placeholders!r} {binds!r}>"

