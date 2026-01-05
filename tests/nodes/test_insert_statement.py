import copy
from arel.nodes.insert_statement import InsertStatement

class TestInsertStatement:
    def test_clones_columns_and_values(self):
        statement = InsertStatement()
        statement.columns = ['a', 'b', 'c']
        statement.values = ['x', 'y', 'z']

        dolly = copy.copy(statement)
        assert dolly.columns == statement.columns
        assert dolly.values == statement.values

        assert dolly.columns is not statement.columns
        assert dolly.values is not statement.values

    def test_is_equal_with_equal_ivars(self):
        statement1 = InsertStatement()
        statement1.columns = ['a', 'b', 'c']
        statement1.values = ['x', 'y', 'z']
        statement2 = InsertStatement()
        statement2.columns = ['a', 'b', 'c']
        statement2.values = ['x', 'y', 'z']

        array = [statement1, statement2]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_ivars(self):
        statement1 = InsertStatement()
        statement1.columns = ['a', 'b', 'c']
        statement1.values = ['x', 'y', 'z']
        statement2 = InsertStatement()
        statement2.columns = ['a', 'b', 'c']
        statement2.values = ['1', '2', '3']
        array = [statement1, statement2]
        assert len(set(array)) == 2
