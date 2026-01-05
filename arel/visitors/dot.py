from typing import Any, List, Optional, Dict, Callable
from arel.visitors.visitor import Visitor

class Node:
    def __init__(self, name: str, node_id: int, fields: Optional[List[Any]] = None):
        self.name = name
        self.id = node_id
        self.fields = fields or []

class Edge:
    def __init__(self, name: Any, from_node: Node):
        self.name = name
        self.from_node = from_node
        self.to: Optional[Node] = None

class Dot(Visitor):
    def __init__(self):
        super().__init__()
        self._nodes: List[Node] = []
        self._edges: List[Edge] = []
        self._node_stack: List[Node] = []
        self._edge_stack: List[Edge] = []
        self._seen: Dict[int, Node] = {}

    def accept(self, object: Any, collector: Any) -> Any:
        self.visit(object)
        collector << self.to_dot()
        return collector

    def visit_arel_nodes_functions_Function(self, o: Any) -> None:
        self.visit_edge(o, "expressions")
        self.visit_edge(o, "distinct")

    def visit_arel_nodes_unary_Unary(self, o: Any) -> None:
        self.visit_edge(o, "expr")

    def visit_arel_nodes_binary_Binary(self, o: Any) -> None:
        self.visit_edge(o, "left")
        self.visit_edge(o, "right")

    def visit_arel_nodes_unary_operation_UnaryOperation(self, o: Any) -> None:
        self.visit_edge(o, "operator")
        self.visit_edge(o, "expr")

    def visit_arel_nodes_infix_operation_InfixOperation(self, o: Any) -> None:
        self.visit_edge(o, "operator")
        self.visit_edge(o, "left")
        self.visit_edge(o, "right")

    def visit_arel_nodes_regexp_Regexp(self, o: Any) -> None:
        self.visit_edge(o, "left")
        self.visit_edge(o, "right")
        self.visit_edge(o, "case_sensitive")

    def visit_arel_nodes_regexp_NotRegexp(self, o: Any) -> None:
        self.visit_edge(o, "left")
        self.visit_edge(o, "right")
        self.visit_edge(o, "case_sensitive")

    def visit_arel_nodes_ordering_Ordering(self, o: Any) -> None:
        self.visit_edge(o, "expr")

    def visit_arel_nodes_table_alias_TableAlias(self, o: Any) -> None:
        self.visit_edge(o, "name")
        self.visit_edge(o, "relation")

    def visit_arel_nodes_count_Count(self, o: Any) -> None:
        self.visit_edge(o, "expressions")
        self.visit_edge(o, "distinct")

    def visit_arel_nodes_values_list_ValuesList(self, o: Any) -> None:
        self.visit_edge(o, "rows")

    def visit_arel_nodes_string_join_StringJoin(self, o: Any) -> None:
        self.visit_edge(o, "left")

    def visit_arel_nodes_window_Window(self, o: Any) -> None:
        self.visit_edge(o, "partitions")
        self.visit_edge(o, "orders")
        self.visit_edge(o, "framing")

    def visit_arel_nodes_window_NamedWindow(self, o: Any) -> None:
        self.visit_edge(o, "partitions")
        self.visit_edge(o, "orders")
        self.visit_edge(o, "framing")
        self.visit_edge(o, "name")

    def visit_arel_nodes_window_CurrentRow(self, o: Any) -> None:
        # intentionally left blank
        pass

    def visit_arel_nodes_distinct_Distinct(self, o: Any) -> None:
        # intentionally left blank
        pass

    def visit_arel_nodes_extract_Extract(self, o: Any) -> None:
        self.visit_edge(o, "expressions")

    def visit_arel_nodes_named_function_NamedFunction(self, o: Any) -> None:
        self.visit_edge(o, "name")
        self.visit_edge(o, "expressions")
        self.visit_edge(o, "distinct")

    def visit_arel_nodes_insert_statement_InsertStatement(self, o: Any) -> None:
        self.visit_edge(o, "relation")
        self.visit_edge(o, "columns")
        self.visit_edge(o, "values")
        self.visit_edge(o, "select")

    def visit_arel_nodes_select_core_SelectCore(self, o: Any) -> None:
        self.visit_edge(o, "source")
        self.visit_edge(o, "projections")
        self.visit_edge(o, "wheres")
        self.visit_edge(o, "windows")
        self.visit_edge(o, "groups")
        self.visit_edge(o, "comment")
        self.visit_edge(o, "havings")
        self.visit_edge(o, "set_quantifier")
        self.visit_edge(o, "optimizer_hints")

    def visit_arel_nodes_select_statement_SelectStatement(self, o: Any) -> None:
        self.visit_edge(o, "cores")
        self.visit_edge(o, "limit")
        self.visit_edge(o, "orders")
        self.visit_edge(o, "offset")
        self.visit_edge(o, "lock")
        self.visit_edge(o, "with_")

    def visit_arel_nodes_update_statement_UpdateStatement(self, o: Any) -> None:
        self.visit_edge(o, "relation")
        self.visit_edge(o, "wheres")
        self.visit_edge(o, "values")
        self.visit_edge(o, "orders")
        self.visit_edge(o, "limit")
        self.visit_edge(o, "offset")
        self.visit_edge(o, "comment")
        self.visit_edge(o, "key")

    def visit_arel_nodes_delete_statement_DeleteStatement(self, o: Any) -> None:
        self.visit_edge(o, "relation")
        self.visit_edge(o, "wheres")
        self.visit_edge(o, "orders")
        self.visit_edge(o, "limit")
        self.visit_edge(o, "offset")
        self.visit_edge(o, "comment")
        self.visit_edge(o, "key")

    def visit_arel_table_Table(self, o: Any) -> None:
        self.visit_edge(o, "name")

    def visit_arel_nodes_casted_Casted(self, o: Any) -> None:
        self.visit_edge(o, "value")
        self.visit_edge(o, "attribute")

    def visit_arel_nodes_homogeneous_in_HomogeneousIn(self, o: Any) -> None:
        self.visit_edge(o, "values")
        self.visit_edge(o, "type")
        self.visit_edge(o, "attribute")

    def visit_arel_attributes_attribute_Attribute(self, o: Any) -> None:
        self.visit_edge(o, "relation")
        self.visit_edge(o, "name")

    def visit_arel_nodes_nary_And(self, o: Any) -> None:
        self.visit_children(o)

    def visit_arel_nodes_nary_Or(self, o: Any) -> None:
        self.visit_children(o)

    def visit_arel_nodes_cte_With(self, o: Any) -> None:
        self.visit_children(o)

    def visit_arel_nodes_bind_param_BindParam(self, o: Any) -> None:
        self.visit_edge(o, "value")

    def visit_arel_nodes_comment_Comment(self, o: Any) -> None:
        self.visit_edge(o, "values")

    def visit_arel_nodes_case_Case(self, o: Any) -> None:
        self.visit_edge(o, "case")
        self.visit_edge(o, "conditions")
        self.visit_edge(o, "default")

    def visit_children(self, o: Any) -> None:
        if hasattr(o, 'children') and o.children is not None:
            for i, child in enumerate(o.children):
                self.edge(i, lambda child=child: self.visit(child))

    def visit_edge(self, o: Any, method: str) -> None:
        if hasattr(o, method):
            value = getattr(o, method)
            # Always create edge, even for None values
            # For None, visit will add it to fields of current node
            # For lists, create one edge with method name, then visit list elements with indices
            if isinstance(value, list):
                self.edge(method, lambda value=value: self.visit_list_elements(value))
            else:
                self.edge(method, lambda value=value: self.visit(value))

    def visit_list_elements(self, lst: list) -> None:
        """Visit list elements with indices (for edges from visit_edge)"""
        if len(lst) == 0:
            # For empty lists, create EmptyList node
            node_id = id(lst)
            if node_id not in self._seen:
                node = Node("EmptyList", node_id)
                self._seen[node_id] = node
                self._nodes.append(node)
            if self._edge_stack:
                self._edge_stack[-1].to = self._seen[node_id]
            return
        # Visit first element to set parent edge.to
        # The parent edge should point to the first element's node
        if len(lst) > 0 and self._edge_stack:
            parent_edge = self._edge_stack[-1]
            # Visit first element - this will create a node and set it in _seen
            self.visit(lst[0])
            # Find the node for first element
            first_node_id = id(lst[0])
            if first_node_id in self._seen:
                parent_edge.to = self._seen[first_node_id]
        # Then visit all elements with indices
        for i, member in enumerate(lst):
            self.edge(i, lambda member=member: self.visit(member))

    def visit(self, o: Any, collector: Any = None) -> Any:
        # Handle None - add to fields of current node (like visit_NilClass in Ruby)
        # But also create a node so edge has a target
        if o is None:
            if self._node_stack:
                self._node_stack[-1].fields.append(None)
            # Create a special node for None so edge has a target
            node_id = id(None)
            if node_id not in self._seen:
                node = Node("None", node_id)
                self._seen[node_id] = node
                self._nodes.append(node)
            if self._edge_stack:
                self._edge_stack[-1].to = self._seen[node_id]
            return

        # Handle primitive types - add them as fields to current node
        # But also set edge.to to current node so edge is created
        if isinstance(o, (str, int, float, bool)):
            if self._node_stack:
                self._node_stack[-1].fields.append(o)
                # Set edge.to to current node so edge is created
                if self._edge_stack:
                    self._edge_stack[-1].to = self._node_stack[-1]
            return

        # Handle list (when visited directly, not from visit_edge)
        if isinstance(o, list):
            if len(o) == 0:
                # For empty lists, create a special node so edge has a target
                node_id = id(o)
                if node_id not in self._seen:
                    node = Node("EmptyList", node_id)
                    self._seen[node_id] = node
                    self._nodes.append(node)
                if self._edge_stack:
                    self._edge_stack[-1].to = self._seen[node_id]
                return
            for i, member in enumerate(o):
                self.edge(i, lambda member=member: self.visit(member))
            return

        # Handle dict
        if isinstance(o, dict):
            for i, (key, value) in enumerate(o.items()):
                self.edge(f"pair_{i}", lambda key=key, value=value: self.visit((key, value)))
            return

        # Handle tuple
        if isinstance(o, tuple):
            for i, member in enumerate(o):
                self.edge(i, lambda member=member: self.visit(member))
            return

        # Handle set
        if isinstance(o, set):
            for i, member in enumerate(o):
                self.edge(i, lambda member=member: self.visit(member))
            return

        # Check if we've seen this object before
        node_id = id(o)
        if node_id in self._seen:
            if self._edge_stack:
                self._edge_stack[-1].to = self._seen[node_id]
            return

        # Create new node
        klass_name = o.__class__.__name__
        module_name = o.__class__.__module__.replace(".", "_")
        full_name = f"{module_name}_{klass_name}"

        node = Node(full_name, node_id)
        self._seen[node_id] = node
        self._nodes.append(node)

        def visit_node():
            Visitor.visit(self, o)

        self.with_node(node, visit_node)

    def edge(self, name: Any, func: Callable) -> None:
        if not self._node_stack:
            return
        edge = Edge(name, self._node_stack[-1])
        self._edge_stack.append(edge)
        self._edges.append(edge)
        func()
        self._edge_stack.pop()

    def with_node(self, node: Node, func: Callable) -> None:
        if self._edge_stack:
            self._edge_stack[-1].to = node

        self._node_stack.append(node)
        func()
        self._node_stack.pop()

    def quote(self, string: str) -> str:
        return str(string).replace('"', '\\"')

    def to_dot(self) -> str:
        lines = ['digraph "Arel" {', 'node [width=0.375,height=0.25,shape=record];']

        for node in self._nodes:
            label = f"<f0>{node.name}"
            for i, field in enumerate(node.fields):
                label += f"|<f{i + 1}>{self.quote(field)}"
            lines.append(f'{node.id} [label="{label}"];')

        for edge in self._edges:
            if edge.to:
                lines.append(f'{edge.from_node.id} -> {edge.to.id} [label="{self.quote(edge.name)}"];')

        lines.append('}')
        return '\n'.join(lines)
