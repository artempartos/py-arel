from typing import Any, List, Optional, Type, TYPE_CHECKING
from arel.mixins.factory_methods import FactoryMethodsMixin
from arel.mixins.alias_predication import AliasPredicationMixin

if TYPE_CHECKING:
    from arel.nodes.node import Node
    from arel.nodes.binary import TableAlias
    from arel.select_manager import SelectManager
    from arel.attributes.attribute import Attribute

class Table(FactoryMethodsMixin, AliasPredicationMixin):
    engine: Optional[Any] = None

    def __init__(self, name: str, as_: Optional[str] = None, klass: Optional[Any] = None, type_caster: Optional[Any] = None):
        self.name = name
        self.klass = klass
        self.type_caster = type_caster if type_caster else (klass.type_caster if klass else None)

        if str(as_) == self.name:
            as_ = None
        self.table_alias = as_

    def alias(self, name: Optional[str] = None) -> 'TableAlias':
        if name is None:
            name = f"{self.name}_2"
        from arel.nodes.table_alias import TableAlias
        return TableAlias(self, name)

    def from_(self) -> 'SelectManager':
        from arel.select_manager import SelectManager
        return SelectManager(self)

    def join(self, relation: Any, klass: Optional[Type['Node']] = None) -> 'SelectManager':
        return self.from_().join(relation, klass)

    def outer_join(self, relation: Any) -> 'SelectManager':
        from arel.nodes.joins import OuterJoin
        return self.join(relation, OuterJoin)

    def group(self, *columns: Any) -> 'SelectManager':
        return self.from_().group(*columns)

    def order(self, *expr: Any) -> 'SelectManager':
        return self.from_().order(*expr)

    def where(self, condition: Any) -> 'SelectManager':
        return self.from_().where(condition)

    def project(self, *things: Any) -> 'SelectManager':
        return self.from_().project(*things)

    def take(self, amount: int) -> 'SelectManager':
        return self.from_().take(amount)

    def skip(self, amount: int) -> 'SelectManager':
        return self.from_().skip(amount)

    def having(self, expr: Any) -> 'SelectManager':
        return self.from_().having(expr)

    def __getitem__(self, name: Any) -> 'Attribute':
        from arel.attributes.attribute import Attribute
        from arel.nodes.sql_literal import SqlLiteral
        # If SqlLiteral is passed (e.g., star()), use its string value
        if isinstance(name, SqlLiteral):
            name = str(name)
        if self.klass and hasattr(self.klass, 'attribute_aliases'):
            name = self.klass.attribute_aliases.get(name, name)
        return Attribute(self, name)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.name == other.name and
            self.table_alias == other.table_alias
        )

    def type_cast_for_database(self, attr_name: str, value: Any) -> Any:
        return self.type_caster.type_cast_for_database(attr_name, value)

    def type_for_attribute(self, name: str) -> Any:
        return self.type_caster.type_for_attribute(name)

    def able_to_type_cast(self) -> bool:
        return self.type_caster is not None

