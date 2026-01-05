from arel.nodes.ordering import Ordering

class Descending(Ordering):
    def reverse(self) -> 'Ascending':
        from arel.nodes.ascending import Ascending
        return Ascending(self.expr)

    def direction(self) -> str:
        return 'desc'

    def is_ascending(self) -> bool:
        return False

    def is_descending(self) -> bool:
        return True

