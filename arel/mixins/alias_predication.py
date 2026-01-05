from typing import Any

class AliasPredicationMixin:
    def as_(self, other: Any) -> 'As':
        if hasattr(other, 'name'):
            other = other.name

        from arel.nodes.binary import As
        from arel.nodes.sql_literal import SqlLiteral
        return As(self, SqlLiteral(str(other), retryable=True))

