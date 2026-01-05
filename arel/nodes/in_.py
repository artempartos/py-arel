from arel.nodes.binary import Binary, FetchAttribute

class In(Binary, FetchAttribute):
    def is_equality(self) -> bool:
        return True

    def invert(self) -> 'NotIn':
        from arel.nodes.binary import NotIn
        return NotIn(self.left, self.right)

