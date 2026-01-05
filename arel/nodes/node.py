from typing import Any, Optional, TYPE_CHECKING
from arel.mixins.factory_methods import FactoryMethodsMixin

if TYPE_CHECKING:
    from arel.table import Table

class Node(FactoryMethodsMixin):
    def not_(self) -> 'Node':
        from arel.nodes.unary import Not
        return Not(self)

    def or_(self, right: Any) -> 'Node':
        from arel.nodes.unary import Grouping
        from arel.nodes.nary import Or
        return Grouping(Or([self, right]))

    def and_(self, right: Any) -> 'Node':
        from arel.nodes.nary import And
        return And([self, right])

    def invert(self) -> 'Node':
        from arel.nodes.unary import Not
        return Not(self)

    def to_sql(self, engine: Optional[Any] = None) -> str:
        if engine is None:
            from arel.table import Table
            engine = Table.engine

        from arel.collectors.sql_string import SQLString
        collector = SQLString()

        # This will be implemented when we have visitors
        return engine.connection.visitor.accept(self, collector).value

    def fetch_attribute(self, block: Optional[Any] = None) -> None:
        pass

    def is_equality(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        return self.__class__ == other.__class__

    def __hash__(self) -> int:
        return hash(self.__class__)

    def __copy__(self) -> 'Node':
        import copy
        new = self.__class__.__new__(self.__class__)
        new.__dict__.update(self.__dict__)
        return new

