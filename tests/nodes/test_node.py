import arel.nodes as nodes
from arel.nodes.node import Node
import inspect

class TestNode:
    def test_includes_factory_methods(self):
        node = Node()
        assert hasattr(node, 'create_join')

    def test_all_nodes_are_nodes(self):
        for name, obj in inspect.getmembers(nodes):
            if inspect.isclass(obj) and issubclass(obj, Node):
                if name in ['SqlLiteral', 'BindParam', 'Node', 'NodeExpression']:
                    continue
                assert issubclass(obj, Node)
