import pytest
from arel.nodes.bound_sql_literal import BoundSqlLiteral

class TestBoundSqlLiteral:
    def test_equality_with_equal_components(self):
        node1 = BoundSqlLiteral("foo + ?", [2], {})
        node2 = BoundSqlLiteral("foo + ?", [2], {})

        array = [node1, node2]
        assert len(set(array)) == 1

    def test_inequality_with_different_components(self):
        node1 = BoundSqlLiteral("foo + ?", [2], {})
        node2 = BoundSqlLiteral("foo + ?", [3], {})
        node3 = BoundSqlLiteral("foo + :bar", [], {"bar": 2})

        array = [node1, node2, node3]
        assert len(set(array)) == 3

