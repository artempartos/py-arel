from arel.nodes.unary import Unary

class Ordering(Unary):
    def nulls_first(self) -> 'NullsFirst':
        return NullsFirst(self)

    def nulls_last(self) -> 'NullsLast':
        return NullsLast(self)

class NullsFirst(Ordering):
    def reverse(self) -> 'NullsLast':
        return NullsLast(self.expr.reverse())

class NullsLast(Ordering):
    def reverse(self) -> 'NullsFirst':
        return NullsFirst(self.expr.reverse())

class Ascending(Ordering):
    def reverse(self) -> 'Descending':
        return Descending(self.expr)

    def direction(self) -> str:
        return 'asc'

    def is_ascending(self) -> bool:
        return True

    def is_descending(self) -> bool:
        return False

class Descending(Ordering):
    def reverse(self) -> 'Ascending':
        return Ascending(self.expr)

    def direction(self) -> str:
        return 'desc'

    def is_ascending(self) -> bool:
        return False

    def is_descending(self) -> bool:
        return True

