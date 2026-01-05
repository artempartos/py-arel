from typing import Any
from arel.nodes.node_expression import NodeExpression

class Unary(NodeExpression):
    def __init__(self, expr: Any):
        super().__init__()
        self.expr = expr

    @property
    def value(self) -> Any:
        return self.expr

    def __hash__(self) -> int:
        expr_hash = tuple(self.expr) if isinstance(self.expr, list) else self.expr
        return hash((self.__class__, expr_hash))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.expr == other.expr
        )

    def __copy__(self) -> 'Unary':
        import copy
        new = super().__copy__()
        new.expr = copy.copy(self.expr) if self.expr is not None else None
        return new

class Bin(Unary): pass
class Cube(Unary): pass
class DistinctOn(Unary): pass
class Group(Unary): pass
class GroupingElement(Unary): pass
class GroupingSet(Unary): pass
class Lateral(Unary): pass
class Limit(Unary): pass
class Lock(Unary): pass
class Not(Unary): pass
class Offset(Unary): pass
class On(Unary): pass
class OptimizerHints(Unary): pass
class RollUp(Unary): pass

class Grouping(Unary):
    def fetch_attribute(self, block: Any) -> None:
        self.expr.fetch_attribute(block)

    def able_to_type_cast(self) -> bool:
        """Delegate able_to_type_cast to wrapped expression"""
        if hasattr(self.expr, 'able_to_type_cast'):
            return self.expr.able_to_type_cast()
        return False

    def type_cast_for_database(self, name: str, value: Any) -> Any:
        """Delegate type_cast_for_database to wrapped expression"""
        if hasattr(self.expr, 'type_cast_for_database'):
            return self.expr.type_cast_for_database(name, value)
        return value

    def type_for_attribute(self, name: str) -> Any:
        """Delegate type_for_attribute to wrapped expression"""
        if hasattr(self.expr, 'type_for_attribute'):
            return self.expr.type_for_attribute(name)
        return None

