import pytest
from arel.nodes.comment import Comment

class TestComment:
    def test_equality_with_equal_contents(self):
        array = [Comment(["foo"]), Comment(["foo"])]
        assert len(set(array)) == 1

    def test_inequality_with_different_contents(self):
        array = [Comment(["foo"]), Comment(["bar"])]
        assert len(set(array)) == 2

