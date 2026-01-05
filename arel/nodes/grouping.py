from typing import Any
from arel.nodes.unary import Unary

class Grouping(Unary):
    def fetch_attribute(self, block: Any) -> None:
        self.expr.fetch_attribute(block)

