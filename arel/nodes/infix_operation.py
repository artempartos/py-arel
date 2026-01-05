from arel.nodes.binary import Binary

class InfixOperation(Binary):
    def __init__(self, operator: str, left: any, right: any):
        super().__init__(left, right)
        self.operator = operator

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.operator))

    def __eq__(self, other: any) -> bool:
        return super().__eq__(other) and self.operator == getattr(other, 'operator', None)

class Multiplication(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("*", left, right)

class Division(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("/", left, right)

class Addition(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("+", left, right)

class Subtraction(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("-", left, right)

class Concat(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("||", left, right)

class BitwiseAnd(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("&", left, right)

class BitwiseOr(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("|", left, right)

class BitwiseXor(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("^", left, right)

class BitwiseShiftLeft(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("<<", left, right)

class BitwiseShiftRight(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__(">>", left, right)

class Contains(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("@>", left, right)

class Overlaps(InfixOperation):
    def __init__(self, left: any, right: any):
        super().__init__("&&", left, right)
