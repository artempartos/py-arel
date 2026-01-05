from arel.nodes.true import True_
from arel.nodes.false import False_
from arel.nodes.distinct import Distinct
from arel.nodes.node import Node

class TestTerminal:
    def test_true_equality(self):
        array = [True_(), True_()]
        assert len(set(array)) == 1

        array = [True_(), Node()]
        assert len(set(array)) == 2

    def test_false_equality(self):
        array = [False_(), False_()]
        assert len(set(array)) == 1

        array = [False_(), Node()]
        assert len(set(array)) == 2

    def test_distinct_equality(self):
        array = [Distinct(), Distinct()]
        assert len(set(array)) == 1

        array = [Distinct(), Node()]
        assert len(set(array)) == 2
