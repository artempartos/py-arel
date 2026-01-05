import pytest
from arel import Table
from arel.nodes.unary import Not

class TestNot:
    def test_makes_a_not_node(self):
        attr = Table('users')['id']
        expr = attr.eq(10)
        node = expr.not_()
        assert isinstance(node, Not)
        assert node.expr == expr

    def test_equality_with_equal_ivars(self):
        array = [Not("foo"), Not("foo")]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Not("foo"), Not("baz")]
        assert len(set(array)) == 2

