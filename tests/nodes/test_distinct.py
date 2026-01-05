from arel.nodes.distinct import Distinct
from arel.nodes.node import Node

class TestDistinct:
    def test_is_equal_to_other_distinct_nodes(self):
        array = [Distinct(), Distinct()]
        assert len(set(array)) == 1

    def test_is_not_equal_with_other_nodes(self):
        array = [Distinct(), Node()]
        assert len(set(array)) == 2

