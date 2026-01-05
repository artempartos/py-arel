from arel.nodes.nary import And
from arel.nodes.binary import As
from arel.nodes.sql_literal import SqlLiteral

class TestAnd:
    def test_is_equal_with_equal_ivars(self):
        array = [And(["foo", "bar"]), And(["foo", "bar"])]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_ivars(self):
        array = [And(["foo", "bar"]), And(["foo", "baz"])]
        assert len(set(array)) == 2

    def test_allows_aliasing(self):
        aliased = And(["foo", "bar"]).as_("baz")
        assert isinstance(aliased, As)
        assert isinstance(aliased.right, SqlLiteral)
