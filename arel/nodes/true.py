from arel.nodes.node_expression import NodeExpression

class True_(NodeExpression):
    def __hash__(self) -> int:
        return hash(self.__class__)

    def __eq__(self, other: any) -> bool:
        return self.__class__ == other.__class__

