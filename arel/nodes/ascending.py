from arel.nodes.ordering import Ordering

class Ascending(Ordering):
    def reverse(self) -> 'Descending':
        from arel.nodes.descending import Descending
        return Descending(self.expr)

    def direction(self) -> str:
        return 'asc'

    def is_ascending(self) -> bool:
        return True

    def is_descending(self) -> bool:
        return False

