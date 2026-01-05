from typing import Any
from arel.mixins.predications import PredicationsMixin
from arel.mixins.alias_predication import AliasPredicationMixin
from arel.mixins.order_predications import OrderPredicationsMixin
from arel.mixins.expressions import ExpressionsMixin

class SqlLiteral(PredicationsMixin, AliasPredicationMixin, OrderPredicationsMixin, ExpressionsMixin):
    def __init__(self, value: str, retryable: bool = False):
        self._value = str(value)
        self._retryable = retryable

    @property
    def retryable(self) -> bool:
        return self._retryable

    def fetch_attribute(self, block: Any = None) -> None:
        pass

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"SqlLiteral({self._value!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SqlLiteral):
            return self._value == other._value
        if isinstance(other, str):
            return self._value == other
        return False

    def __hash__(self) -> int:
        return hash(self._value)

    def __add__(self, other: Any) -> 'Fragments':
        from arel import arel_node
        if not arel_node(other):
            raise ValueError("Expected Arel node")

        from arel.nodes.fragments import Fragments
        if isinstance(other, Fragments):
            return Fragments([self] + other.values)
        return Fragments([self, other])

    def __iadd__(self, other: Any) -> 'Fragments':
        from arel import arel_node
        if not arel_node(other):
            raise ValueError("Expected Arel node")

        from arel.nodes.fragments import Fragments
        if isinstance(other, Fragments):
            return Fragments([self] + other.values)
        return Fragments([self, other])

    def to_yaml(self) -> str:
        """Serialize to YAML format"""
        try:
            import yaml
            return yaml.dump(self._value, default_flow_style=False).strip()
        except ImportError:
            # Fallback: return simple string representation if yaml is not available
            return f'"{self._value}"'
