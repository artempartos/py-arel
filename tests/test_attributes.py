import pytest
from arel import Table
from arel.attributes.attribute import Attribute

class TestAttributes:
    def test_responds_to_lower(self):
        relation = Table('users')
        attribute = relation['foo']
        node = attribute.lower()
        assert node.name == "LOWER"
        # In Python expressions can be a list or a single element
        if isinstance(node.expressions, list):
            assert attribute in node.expressions or node.expressions == [attribute]
        else:
            assert node.expressions == attribute

    def test_equality_with_equal_ivars(self):
        array = [Attribute("foo", "bar"), Attribute("foo", "bar")]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [Attribute("foo", "bar"), Attribute("foo", "baz")]
        assert len(set(array)) == 2

