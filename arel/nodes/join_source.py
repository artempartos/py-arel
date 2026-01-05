from arel.nodes.binary import Binary

class JoinSource(Binary):
    def __init__(self, single_source: any, joinop: list = None):
        super().__init__(single_source, joinop if joinop is not None else [])

    def is_empty(self) -> bool:
        return not self.left and not self.right

