from typing import Any

class FilterPredicationsMixin:
    def filter(self, expr: Any) -> 'Filter':
        from arel.nodes.filter import Filter
        return Filter(self, expr)

