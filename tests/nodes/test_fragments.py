import pytest
from arel import sql
from arel.nodes.fragments import Fragments

class TestFragments:
    def test_equality_with_equal_values(self):
        array = [Fragments(["foo", "bar"]), Fragments(["foo", "bar"])]
        assert len(set(array)) == 1

    def test_inequality_with_different_values(self):
        array = [Fragments(["foo"]), Fragments(["bar"])]
        assert len(set(array)) == 2

    def test_can_be_joined_with_other_nodes(self):
        fragments = Fragments(["foo", "bar"])
        sql_node = sql("SELECT")
        joined_fragments = fragments + sql_node

        assert fragments.values == ["foo", "bar"]
        assert joined_fragments.values == ["foo", "bar", sql_node]

    def test_fails_if_joined_with_something_that_is_not_an_arel_node(self):
        fragments = Fragments([])
        with pytest.raises((ValueError, TypeError)):
            fragments + "Not a node"

