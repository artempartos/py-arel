from arel.nodes.binary import Binary, FetchAttribute

class Equality(Binary, FetchAttribute):
    def is_equality(self) -> bool:
        return True

    def invert(self) -> 'NotEqual':
        from arel.nodes.binary import NotEqual
        return NotEqual(self.left, self.right)

