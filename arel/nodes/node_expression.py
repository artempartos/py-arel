from arel.nodes.node import Node
from arel.mixins.predications import PredicationsMixin
from arel.mixins.alias_predication import AliasPredicationMixin
from arel.mixins.order_predications import OrderPredicationsMixin
from arel.mixins.expressions import ExpressionsMixin
from arel.mixins.math import MathMixin

class NodeExpression(Node, PredicationsMixin, AliasPredicationMixin, OrderPredicationsMixin, ExpressionsMixin, MathMixin):
    pass
