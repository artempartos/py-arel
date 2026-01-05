from typing import Any
from arel.nodes.unary import Unary

class UnaryOperation(Unary):
    def __init__(self, operator: str, operand: Any):
        super().__init__(operand)
        self.operator = operator

class BitwiseNot(UnaryOperation):
    def __init__(self, operand: Any):
        super().__init__("~", operand)

