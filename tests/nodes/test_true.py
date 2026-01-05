from arel.nodes.true import True_
from arel.nodes.node import Node

class TestTrue:
    def test_is_equal_to_other_true_nodes(self):
        array = [True_(), True_()]
        assert len(set(array)) == 1

    def test_is_not_equal_with_other_nodes(self):
        array = [True_(), Node()]
        assert len(set(array)) == 2

