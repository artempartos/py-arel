from arel.nodes.false import False_
from arel.nodes.node import Node

class TestFalse:
    def test_is_equal_to_other_false_nodes(self):
        array = [False_(), False_()]
        assert len(set(array)) == 1

    def test_is_not_equal_with_other_nodes(self):
        array = [False_(), Node()]
        assert len(set(array)) == 2

