from arel.nodes.binary import Binary
from arel.mixins.window_predications import WindowPredicationsMixin
from arel.mixins.alias_predication import AliasPredicationMixin

class Filter(Binary, WindowPredicationsMixin, AliasPredicationMixin):
    def __init__(self, left: any, right: any):
        super().__init__(left, right)
