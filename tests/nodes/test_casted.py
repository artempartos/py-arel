import pytest
from arel.nodes.casted import Casted

class TestCasted:
    def test_hash_is_equal_when_eql_returns_true(self):
        one = Casted(1, 2)
        also_one = Casted(1, 2)

        assert hash(one) == hash(also_one)

