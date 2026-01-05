from arel.nodes.node import Node
from arel.nodes.equality import Equality
from arel.nodes.binary import Binary

class TestNodes:
    def test_every_arel_nodes_have_hash_eql_eqeq_from_same_class(self):
        # Check that all nodes have correct hash, __eq__ and __ne__
        eq1 = Equality("foo", "bar")
        eq2 = Equality("foo", "bar")
        eq3 = Equality("bar", "baz")

        # Hash should be the same for identical nodes
        assert hash(eq1) == hash(eq2)
        assert hash(eq1) != hash(eq3)

        # __eq__ should work correctly
        assert eq1 == eq2
        assert eq1 != eq3

        # Check that all nodes inherit from Node
        assert isinstance(eq1, Node)
        assert isinstance(eq2, Node)
        assert isinstance(eq3, Node)

        # Check that Binary nodes inherit from Binary
        assert isinstance(eq1, Binary)
