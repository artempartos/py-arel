from typing import Any
from arel.mixins.expressions import ExpressionsMixin
from arel.mixins.predications import PredicationsMixin
from arel.mixins.alias_predication import AliasPredicationMixin
from arel.mixins.order_predications import OrderPredicationsMixin
from arel.mixins.math import MathMixin

class Attribute(ExpressionsMixin, PredicationsMixin, AliasPredicationMixin, OrderPredicationsMixin, MathMixin):
    def __init__(self, relation: Any, name: str):
        self.relation = relation
        self.name = name

    def type_caster(self) -> Any:
        return self.relation.type_for_attribute(self.name)

    def lower(self) -> 'Node':
        return self.relation.lower(self)

    def type_cast_for_database(self, value: Any) -> Any:
        return self.relation.type_cast_for_database(self.name, value)

    def able_to_type_cast(self) -> bool:
        return self.relation.able_to_type_cast()

    def __hash__(self) -> int:
        return hash((self.relation, self.name))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.relation == other.relation and
            self.name == other.name
        )

