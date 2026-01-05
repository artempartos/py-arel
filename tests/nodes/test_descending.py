import pytest
from arel.nodes.ascending import Ascending
from arel.nodes.descending import Descending

class TestDescending:
    def test_construct(self):
        descending = Descending("zomg")
        assert descending.expr == "zomg"

    def test_reverse(self):
        descending = Descending("zomg")
        ascending = descending.reverse()
        assert isinstance(ascending, Ascending)
        assert descending.expr == ascending.expr

    def test_direction(self):
        descending = Descending("zomg")
        assert descending.direction() == 'desc'

    def test_is_ascending(self):
        descending = Descending("zomg")
        assert descending.is_ascending() == False

    def test_is_descending(self):
        descending = Descending("zomg")
        assert descending.is_descending() == True

    def test_equality_with_same_ivars(self):
        array = [Descending("zomg"), Descending("zomg")]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Descending("zomg"), Descending("zomg!")]
        assert len(set(array)) == 2

