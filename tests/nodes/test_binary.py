from arel.nodes.equality import Equality
from arel.nodes.binary import NotEqual, Binary

class TestBinary:
    def test_generates_a_hash_based_on_its_value(self):
        eq = Equality("foo", "bar")
        eq2 = Equality("foo", "bar")
        eq3 = Equality("bar", "baz")

        assert hash(eq) == hash(eq2)
        assert hash(eq) != hash(eq3)

        neq = NotEqual("foo", "bar")
        assert hash(eq) != hash(neq)

    def test_generates_a_hash_specific_to_its_class(self):
        eq = Equality("foo", "bar")
        neq = NotEqual("foo", "bar")
        assert hash(eq) != hash(neq)

    def test_every_arel_nodes_have_hash_eql_eqeq_from_same_class(self):
        # Check that all Binary nodes have correct hash, __eq__ and __ne__
        eq1 = Equality("foo", "bar")
        eq2 = Equality("foo", "bar")
        neq1 = NotEqual("foo", "bar")

        # Hash should be the same for identical nodes
        assert hash(eq1) == hash(eq2)
        assert hash(eq1) != hash(neq1)

        # __eq__ should work correctly
        assert eq1 == eq2
        assert eq1 != neq1

        # Check that all Binary nodes inherit from Binary
        assert isinstance(eq1, Binary)
        assert isinstance(neq1, Binary)
