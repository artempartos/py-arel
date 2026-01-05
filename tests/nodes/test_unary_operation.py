import pytest
from arel.nodes.unary_operation import UnaryOperation
from arel.nodes.binary import As
from arel.nodes.ordering import Descending

class TestUnaryOperation:
    def test_construct(self):
        operation = UnaryOperation('-', 1)
        assert operation.operator == '-'
        assert operation.expr == 1

    def test_operation_alias(self):
        operation = UnaryOperation('-', 1)
        alias = operation.as_("zomg")
        assert isinstance(alias, As)
        assert alias.left == operation
        assert str(alias.right) == "zomg"

    def test_operation_ordering(self):
        operation = UnaryOperation('-', 1)
        ordering = operation.desc()
        assert isinstance(ordering, Descending)
        assert ordering.expr == operation
        assert ordering.is_descending() == True

    def test_equality_with_same_ivars(self):
        array = [UnaryOperation('-', 1), UnaryOperation('-', 1)]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [UnaryOperation('-', 1), UnaryOperation('-', 2)]
        assert len(set(array)) == 2

