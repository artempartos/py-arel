import pytest
from arel.nodes.ascending import Ascending
from arel.nodes.descending import Descending

class TestAscending:
    def test_construct(self):
        ascending = Ascending("zomg")
        assert ascending.expr == "zomg"

    def test_reverse(self):
        ascending = Ascending("zomg")
        descending = ascending.reverse()
        assert isinstance(descending, Descending)
        assert ascending.expr == descending.expr

    def test_direction(self):
        ascending = Ascending("zomg")
        assert ascending.direction() == 'asc'

    def test_is_ascending(self):
        ascending = Ascending("zomg")
        assert ascending.is_ascending() == True

    def test_is_descending(self):
        ascending = Ascending("zomg")
        assert ascending.is_descending() == False

    def test_equality_with_same_ivars(self):
        array = [Ascending("zomg"), Ascending("zomg")]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Ascending("zomg"), Ascending("zomg!")]
        assert len(set(array)) == 2

