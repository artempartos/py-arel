import pytest
import copy
from arel.nodes.delete_statement import DeleteStatement

class TestDeleteStatement:
    def test_clone_clones_wheres(self):
        statement = DeleteStatement()
        statement.wheres = ['a', 'b', 'c']

        dolly = copy.copy(statement)
        assert dolly.wheres == statement.wheres
        assert dolly.wheres is not statement.wheres

    def test_equality_with_equal_ivars(self):
        statement1 = DeleteStatement()
        statement1.wheres = ['a', 'b', 'c']
        statement2 = DeleteStatement()
        statement2.wheres = ['a', 'b', 'c']
        array = [statement1, statement2]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        statement1 = DeleteStatement()
        statement1.wheres = ['a', 'b', 'c']
        statement2 = DeleteStatement()
        statement2.wheres = ['1', '2', '3']
        array = [statement1, statement2]
        assert len(set(array)) == 2

