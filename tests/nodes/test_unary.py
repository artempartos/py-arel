from arel.nodes.unary import Not

class TestUnary:
    def test_equality(self):
        n1 = Not("foo")
        n2 = Not("foo")
        assert n1 == n2
        assert len(set([n1, n2])) == 1

        n3 = Not("baz")
        assert n1 != n3
        assert len(set([n1, n3])) == 2
