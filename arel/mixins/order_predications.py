class OrderPredicationsMixin:
    def asc(self) -> 'Ascending':
        from arel.nodes.ordering import Ascending
        return Ascending(self)

    def desc(self) -> 'Descending':
        from arel.nodes.ordering import Descending
        return Descending(self)

