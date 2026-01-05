import pytest
import copy
from arel.nodes.update_statement import UpdateStatement

class TestUpdateStatement:
    def test_clone_clones_wheres_and_values(self):
        statement = UpdateStatement()
        statement.wheres = ['a', 'b', 'c']
        statement.values = ['x', 'y', 'z']

        dolly = copy.copy(statement)
        assert dolly.wheres == statement.wheres
        assert dolly.wheres is not statement.wheres

        assert dolly.values == statement.values
        assert dolly.values is not statement.values

    def test_equality_with_equal_ivars(self):
        statement1 = UpdateStatement()
        statement1.relation = "zomg"
        statement1.wheres = 2
        statement1.values = False
        statement1.orders = ['x', 'y', 'z']
        statement1.limit = 42
        statement1.key = "zomg"
        statement1.groups = ["foo"]
        statement1.havings = []
        statement2 = UpdateStatement()
        statement2.relation = "zomg"
        statement2.wheres = 2
        statement2.values = False
        statement2.orders = ['x', 'y', 'z']
        statement2.limit = 42
        statement2.key = "zomg"
        statement2.groups = ["foo"]
        statement2.havings = []
        array = [statement1, statement2]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        statement1 = UpdateStatement()
        statement1.relation = "zomg"
        statement1.wheres = 2
        statement1.values = False
        statement1.orders = ['x', 'y', 'z']
        statement1.limit = 42
        statement1.key = "zomg"
        statement2 = UpdateStatement()
        statement2.relation = "zomg"
        statement2.wheres = 2
        statement2.values = False
        statement2.orders = ['x', 'y', 'z']
        statement2.limit = 42
        statement2.key = "wth"
        array = [statement1, statement2]
        assert len(set(array)) == 2

