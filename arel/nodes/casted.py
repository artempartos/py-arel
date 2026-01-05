from typing import Any, Optional, TYPE_CHECKING
from arel.nodes.node_expression import NodeExpression
from arel.nodes.unary import Unary

if TYPE_CHECKING:
    from arel.attributes.attribute import Attribute

class Casted(NodeExpression):
    def __init__(self, value: Any, attribute: 'Attribute'):
        super().__init__()
        self.value = value
        self.attribute = attribute

    @property
    def value_before_type_cast(self) -> Any:
        return self.value

    def is_nil(self) -> bool:
        return self.value is None

    def value_for_database(self) -> Any:
        if self.attribute.able_to_type_cast():
            return self.attribute.type_cast_for_database(self.value)
        else:
            return self.value

    def __hash__(self) -> int:
        return hash((self.__class__, self.value, self.attribute))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.value == other.value and
            self.attribute == other.attribute
        )

class Quoted(Unary):
    @property
    def value_for_database(self) -> Any:
        return self.expr

    @property
    def value_before_type_cast(self) -> Any:
        return self.expr

    def is_nil(self) -> bool:
        return self.expr is None

    def is_infinite(self) -> bool:
        import math
        # Check if expr is float infinity
        if isinstance(self.expr, float):
            return math.isinf(self.expr)
        # Check if expr has infinite method
        if hasattr(self.expr, "infinite"):
            infinite_attr = getattr(self.expr, "infinite", None)
            if callable(infinite_attr):
                try:
                    return infinite_attr()
                except TypeError:
                    return False
            else:
                return bool(infinite_attr)
        return False

def build_quoted(other: Any, attribute: Optional['Attribute'] = None) -> Any:
    from arel.nodes.node import Node
    from arel.attributes.attribute import Attribute
    from arel.table import Table
    from arel.select_manager import SelectManager
    from arel.nodes.sql_literal import SqlLiteral

    # In Python we check types
    if isinstance(other, (Node, Attribute, Table, SelectManager, SqlLiteral)):
        return other

    if isinstance(attribute, Attribute):
        return Casted(other, attribute)
    else:
        return Quoted(other)

