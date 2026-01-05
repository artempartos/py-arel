from typing import Any

class ExpressionsMixin:
    def count(self, distinct: bool = False) -> 'Count':
        from arel.nodes.count import Count
        return Count([self], distinct)

    def sum(self) -> 'Sum':
        from arel.nodes.functions import Sum
        return Sum([self])

    def maximum(self) -> 'Max':
        from arel.nodes.functions import Max
        return Max([self])

    def minimum(self) -> 'Min':
        from arel.nodes.functions import Min
        return Min([self])

    def average(self) -> 'Avg':
        from arel.nodes.functions import Avg
        return Avg([self])

    def extract(self, field: str) -> 'Extract':
        from arel.nodes.extract import Extract
        return Extract(self, field)

