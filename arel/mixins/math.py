from typing import Any

class MathMixin:
    def __mul__(self, other: Any) -> 'Multiplication':
        from arel.nodes.infix_operation import Multiplication
        return Multiplication(self, other)

    def __add__(self, other: Any) -> 'Grouping':
        from arel.nodes.grouping import Grouping
        from arel.nodes.infix_operation import Addition
        return Grouping(Addition(self, other))

    def __sub__(self, other: Any) -> 'Grouping':
        from arel.nodes.grouping import Grouping
        from arel.nodes.infix_operation import Subtraction
        return Grouping(Subtraction(self, other))

    def __truediv__(self, other: Any) -> 'Division':
        from arel.nodes.infix_operation import Division
        return Division(self, other)

    def __and__(self, other: Any) -> 'Grouping':
        from arel.nodes.grouping import Grouping
        from arel.nodes.infix_operation import BitwiseAnd
        return Grouping(BitwiseAnd(self, other))

    def __or__(self, other: Any) -> 'Grouping':
        from arel.nodes.grouping import Grouping
        from arel.nodes.infix_operation import BitwiseOr
        return Grouping(BitwiseOr(self, other))

    def __xor__(self, other: Any) -> 'Grouping':
        from arel.nodes.grouping import Grouping
        from arel.nodes.infix_operation import BitwiseXor
        return Grouping(BitwiseXor(self, other))

    def __lshift__(self, other: Any) -> 'Grouping':
        from arel.nodes.grouping import Grouping
        from arel.nodes.infix_operation import BitwiseShiftLeft
        return Grouping(BitwiseShiftLeft(self, other))

    def __rshift__(self, other: Any) -> 'Grouping':
        from arel.nodes.grouping import Grouping
        from arel.nodes.infix_operation import BitwiseShiftRight
        return Grouping(BitwiseShiftRight(self, other))

    def __invert__(self) -> 'BitwiseNot':
        from arel.nodes.unary_operation import BitwiseNot
        return BitwiseNot(self)

