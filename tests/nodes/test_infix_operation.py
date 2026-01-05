import pytest
from arel.nodes.infix_operation import InfixOperation
from arel.nodes.binary import As
from arel.nodes.ordering import Descending

class TestInfixOperation:
    def test_construct(self):
        operation = InfixOperation('+', 1, 2)
        assert operation.operator == '+'
        assert operation.left == 1
        assert operation.right == 2

    def test_operation_alias(self):
        operation = InfixOperation('+', 1, 2)
        alias = operation.as_("zomg")
        assert isinstance(alias, As)
        assert alias.left == operation
        assert str(alias.right) == "zomg"

    def test_operation_ordering(self):
        operation = InfixOperation('+', 1, 2)
        ordering = operation.desc()
        assert isinstance(ordering, Descending)
        assert ordering.expr == operation
        assert ordering.is_descending() == True

    def test_equality_with_same_ivars(self):
        array = [InfixOperation('+', 1, 2), InfixOperation('+', 1, 2)]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [InfixOperation('+', 1, 2), InfixOperation('+', 1, 3)]
        assert len(set(array)) == 2

