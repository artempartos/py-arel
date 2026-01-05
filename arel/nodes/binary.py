from typing import Any, Optional
from arel.nodes.node_expression import NodeExpression

class Binary(NodeExpression):
    def __init__(self, left: Any, right: Any):
        super().__init__()
        self.left = left
        self.right = right

    def __hash__(self) -> int:
        left_hash = tuple(self.left) if isinstance(self.left, list) else self.left
        right_hash = tuple(self.right) if isinstance(self.right, list) else self.right
        return hash((self.__class__, left_hash, right_hash))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.left == other.left and
            self.right == other.right
        )

    def __copy__(self) -> 'Binary':
        import copy
        new = self.__class__.__new__(self.__class__)
        new.left = copy.copy(self.left) if self.left is not None else None
        new.right = copy.copy(self.right) if self.right is not None else None
        return new

class FetchAttribute:
    def fetch_attribute(self, block: Any) -> None:
        # In Python, we might need a different way to handle blocks,
        # but following Ruby's yield for now.
        from arel.attributes.attribute import Attribute
        if isinstance(self.left, Attribute):
            block(self.left)
        elif isinstance(self.right, Attribute):
            block(self.right)

class As(Binary):
    def to_cte(self) -> 'Cte':
        from arel.nodes.cte import Cte
        return Cte(self.left.name, self.right)

class Between(Binary, FetchAttribute):
    pass

class GreaterThan(Binary, FetchAttribute):
    def invert(self) -> 'LessThanOrEqual':
        from arel.nodes.binary import LessThanOrEqual
        return LessThanOrEqual(self.left, self.right)

class GreaterThanOrEqual(Binary, FetchAttribute):
    def invert(self) -> 'LessThan':
        from arel.nodes.binary import LessThan
        return LessThan(self.left, self.right)

class LessThan(Binary, FetchAttribute):
    def invert(self) -> 'GreaterThanOrEqual':
        from arel.nodes.binary import GreaterThanOrEqual
        return GreaterThanOrEqual(self.left, self.right)

class LessThanOrEqual(Binary, FetchAttribute):
    def invert(self) -> 'GreaterThan':
        from arel.nodes.binary import GreaterThan
        return GreaterThan(self.left, self.right)

class IsDistinctFrom(Binary, FetchAttribute):
    def invert(self) -> 'IsNotDistinctFrom':
        from arel.nodes.binary import IsNotDistinctFrom
        return IsNotDistinctFrom(self.left, self.right)

class IsNotDistinctFrom(Binary, FetchAttribute):
    def invert(self) -> 'IsDistinctFrom':
        from arel.nodes.binary import IsDistinctFrom
        return IsDistinctFrom(self.left, self.right)

class NotEqual(Binary, FetchAttribute):
    def invert(self) -> 'Equality':
        from arel.nodes.equality import Equality
        return Equality(self.left, self.right)

class NotIn(Binary, FetchAttribute):
    def invert(self) -> 'In':
        from arel.nodes.in_ import In
        return In(self.left, self.right)

class Assignment(Binary): pass
class Join(Binary): pass
class Union(Binary): pass
class UnionAll(Binary): pass
class Intersect(Binary): pass
class Except(Binary): pass

