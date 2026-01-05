import pytest
from arel.nodes.bind_param import BindParam
from arel.nodes.node import Node

class TestBindParam:
    def test_is_equal_to_other_bind_params_with_same_value(self):
        assert BindParam(1) == BindParam(1)
        assert BindParam("foo") == BindParam("foo")

    def test_is_not_equal_to_other_nodes(self):
        assert BindParam(None) != Node()

    def test_is_not_equal_to_bind_params_with_different_values(self):
        assert BindParam(1) != BindParam(2)

