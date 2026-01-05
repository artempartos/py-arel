import copy
from arel.nodes.select_statement import SelectStatement

class TestSelectStatement:
    def test_clones_cores(self):
        statement = SelectStatement(['a', 'b', 'c'])
        dolly = copy.copy(statement)
        assert dolly.cores == statement.cores
        assert dolly.cores is not statement.cores

    def test_is_equal_with_equal_ivars(self):
        statement1 = SelectStatement(['a', 'b', 'c'])
        statement1.offset = 1
        statement1.limit = 2
        statement1.lock = False
        statement1.orders = ['x', 'y', 'z']
        statement1.with_ = "zomg"

        statement2 = SelectStatement(['a', 'b', 'c'])
        statement2.offset = 1
        statement2.limit = 2
        statement2.lock = False
        statement2.orders = ['x', 'y', 'z']
        statement2.with_ = "zomg"

        array = [statement1, statement2]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_ivars(self):
        statement1 = SelectStatement(['a', 'b', 'c'])
        statement1.offset = 1
        statement1.limit = 2
        statement1.lock = False
        statement1.orders = ['x', 'y', 'z']
        statement1.with_ = "zomg"

        statement2 = SelectStatement(['a', 'b', 'c'])
        statement2.offset = 1
        statement2.limit = 2
        statement2.lock = False
        statement2.orders = ['x', 'y', 'z']
        statement2.with_ = "wth"
        array = [statement1, statement2]
        assert len(set(array)) == 2
