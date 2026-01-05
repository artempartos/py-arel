from arel import Table
from arel.nodes.nary import Or

class TestOr:
    def test_makes_an_or_node(self):
        attr = Table('users')['id']
        left = attr.eq(10)
        right = attr.eq(11)
        node = left.or_(right)
        assert node.expr.left == left
        assert node.expr.right == right

        oror = node.or_(right)
        assert oror.expr.left == node
        assert oror.expr.right == right

    def test_is_equal_with_equal_ivars(self):
        array = [Or(["foo", "bar"]), Or(["foo", "bar"])]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_ivars(self):
        array = [Or(["foo", "bar"]), Or(["foo", "baz"])]
        assert len(set(array)) == 2
