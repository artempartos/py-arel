# AREL Python Implementation Plan

## General Strategy

Implementation should be as close as possible to Ruby API, but taking into account Python specifics.

### Implementation Phases

1. **Phase 1: Core** - base classes and nodes
2. **Phase 2: Predications** - conditions and expressions
3. **Phase 3: Managers** - query managers
4. **Phase 4: Visitors** - SQL compilation
5. **Phase 5: Database adapters** - database-specific code
6. **Phase 6: Integration** - integration and tests

---

## Phase 1: Core

### 1.1 Base Structure

```
arel/
├── __init__.py          # Public API
├── table.py             # Table class
├── tree_manager.py      # TreeManager base
├── select_manager.py    # SelectManager
├── insert_manager.py    # InsertManager
├── update_manager.py    # UpdateManager
├── delete_manager.py    # DeleteManager
├── errors.py            # Exceptions
├── nodes/
│   ├── __init__.py      # Export all nodes
│   ├── node.py          # Node, NodeExpression
│   ├── binary.py        # Binary and derivatives
│   ├── unary.py         # Unary and derivatives
│   ├── nary.py          # And, Or
│   ├── terminal.py      # Distinct
│   ├── statements.py    # Select/Insert/Update/Delete Statement
│   ├── functions.py     # Function, Count, Sum, etc
│   ├── window.py        # Window, Over, Rows, Range
│   ├── case.py          # Case, When, Else
│   ├── cte.py           # With, Cte
│   ├── joins.py         # All join types
│   ├── literals.py      # SqlLiteral, BoundSqlLiteral
│   ├── casted.py        # Casted, Quoted, BindParam
│   └── misc.py          # Comment, Fragments, etc
├── attributes/
│   ├── __init__.py
│   └── attribute.py     # Attribute class
├── visitors/
│   ├── __init__.py
│   ├── visitor.py       # Base Visitor
│   ├── to_sql.py        # ToSql visitor
│   ├── mysql.py         # MySQL visitor
│   ├── postgresql.py    # PostgreSQL visitor
│   ├── sqlite.py        # SQLite visitor
│   └── dot.py           # Dot visualization
├── collectors/
│   ├── __init__.py
│   ├── plain_string.py
│   ├── sql_string.py
│   ├── bind.py
│   ├── composite.py
│   └── substitute_binds.py
├── mixins/
│   ├── __init__.py
│   ├── predications.py
│   ├── expressions.py
│   ├── math_operations.py
│   ├── order_predications.py
│   ├── alias_predication.py
│   ├── window_predications.py
│   ├── filter_predications.py
│   └── factory_methods.py
└── crud.py              # CRUD mixin
```

### 1.2 Base Node Classes

```python
# arel/nodes/node.py

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any
from abc import ABC

if TYPE_CHECKING:
    from arel.visitors import Visitor

class Node(ABC):
    """Base class for all AST nodes."""

    def not_(self) -> 'Not':
        from arel.nodes.unary import Not
        return Not(self)

    def or_(self, right: 'Node') -> 'Grouping':
        from arel.nodes.unary import Grouping
        from arel.nodes.nary import Or
        return Grouping(Or([self, right]))

    def and_(self, right: 'Node') -> 'And':
        from arel.nodes.nary import And
        return And([self, right])

    def invert(self) -> 'Not':
        from arel.nodes.unary import Not
        return Not(self)

    def to_sql(self, engine=None) -> str:
        from arel.collectors import SQLString
        collector = SQLString()
        # Need engine.connection.visitor...
        raise NotImplementedError

    def fetch_attribute(self):
        return None

    def is_equality(self) -> bool:
        return False

    def __hash__(self) -> int:
        return hash(self.__class__)

    def __eq__(self, other: Any) -> bool:
        return self.__class__ == other.__class__


class NodeExpression(Node):
    """Node with predications and expressions support."""
    # Mixins will be added via composition or multiple inheritance
    pass
```

### 1.3 Binary, Unary, Nary

```python
# arel/nodes/binary.py

from typing import Any, Optional
from .node import NodeExpression

class Binary(NodeExpression):
    """Node with left and right children."""

    def __init__(self, left: Any, right: Any):
        super().__init__()
        self.left = left
        self.right = right

    def __hash__(self) -> int:
        return hash((self.__class__, self.left, self.right))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.left == other.left and
            self.right == other.right
        )

    def __copy__(self):
        import copy
        new = self.__class__.__new__(self.__class__)
        new.left = copy.copy(self.left) if self.left else None
        new.right = copy.copy(self.right) if self.right else None
        return new


# arel/nodes/unary.py

class Unary(NodeExpression):
    """Node with single child."""

    def __init__(self, expr: Any):
        super().__init__()
        self.expr = expr

    @property
    def value(self) -> Any:
        return self.expr

    def __hash__(self) -> int:
        return hash(self.expr)

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.expr == other.expr
        )


# arel/nodes/nary.py

from typing import List, Any

class Nary(NodeExpression):
    """Node with N children."""

    def __init__(self, children: List[Any]):
        super().__init__()
        self.children = children

    @property
    def left(self) -> Any:
        return self.children[0] if self.children else None

    @property
    def right(self) -> Any:
        return self.children[1] if len(self.children) > 1 else None

    def __hash__(self) -> int:
        return hash((self.__class__, tuple(self.children)))

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__ and
            self.children == other.children
        )


class And(Nary):
    pass


class Or(Nary):
    pass
```

---

## Phase 2: Predications

### 2.1 Implementation via Mixins

Python supports multiple inheritance, which allows implementing mixins:

```python
# arel/mixins/predications.py

from typing import Any, List, Optional, TYPE_CHECKING
from abc import ABC

if TYPE_CHECKING:
    from arel.nodes import Node

class PredicationsMixin(ABC):
    """Mixin providing predicate methods."""

    def eq(self, other: Any) -> 'Equality':
        from arel.nodes.binary import Equality
        return Equality(self, self._quoted_node(other))

    def not_eq(self, other: Any) -> 'NotEqual':
        from arel.nodes.binary import NotEqual
        return NotEqual(self, self._quoted_node(other))

    def gt(self, other: Any) -> 'GreaterThan':
        from arel.nodes.binary import GreaterThan
        return GreaterThan(self, self._quoted_node(other))

    def gteq(self, other: Any) -> 'GreaterThanOrEqual':
        from arel.nodes.binary import GreaterThanOrEqual
        return GreaterThanOrEqual(self, self._quoted_node(other))

    def lt(self, other: Any) -> 'LessThan':
        from arel.nodes.binary import LessThan
        return LessThan(self, self._quoted_node(other))

    def lteq(self, other: Any) -> 'LessThanOrEqual':
        from arel.nodes.binary import LessThanOrEqual
        return LessThanOrEqual(self, self._quoted_node(other))

    def in_(self, other: Any) -> 'In':
        from arel.nodes.binary import In
        from arel.select_manager import SelectManager

        if isinstance(other, SelectManager):
            return In(self, other.ast)
        elif hasattr(other, '__iter__') and not isinstance(other, (str, bytes)):
            return In(self, self._quoted_array(other))
        else:
            return In(self, self._quoted_node(other))

    def not_in(self, other: Any) -> 'NotIn':
        from arel.nodes.binary import NotIn
        from arel.select_manager import SelectManager

        if isinstance(other, SelectManager):
            return NotIn(self, other.ast)
        elif hasattr(other, '__iter__') and not isinstance(other, (str, bytes)):
            return NotIn(self, self._quoted_array(other))
        else:
            return NotIn(self, self._quoted_node(other))

    def matches(self, other: Any, escape: Optional[str] = None,
                case_sensitive: bool = False) -> 'Matches':
        from arel.nodes.binary import Matches
        return Matches(self, self._quoted_node(other), escape, case_sensitive)

    def does_not_match(self, other: Any, escape: Optional[str] = None,
                       case_sensitive: bool = False) -> 'DoesNotMatch':
        from arel.nodes.binary import DoesNotMatch
        return DoesNotMatch(self, self._quoted_node(other), escape, case_sensitive)

    # _any methods
    def eq_any(self, others: List[Any]) -> 'Grouping':
        return self._grouping_any('eq', others)

    def not_eq_any(self, others: List[Any]) -> 'Grouping':
        return self._grouping_any('not_eq', others)

    # _all methods
    def eq_all(self, others: List[Any]) -> 'Grouping':
        return self._grouping_all('eq', others)

    # ... more methods ...

    def _quoted_node(self, other: Any) -> Any:
        from arel.nodes import build_quoted
        return build_quoted(other, self)

    def _quoted_array(self, others: List[Any]) -> List[Any]:
        return [self._quoted_node(v) for v in others]

    def _grouping_any(self, method: str, others: List[Any], *extras) -> 'Grouping':
        from arel.nodes.unary import Grouping
        from arel.nodes.nary import Or

        nodes = [getattr(self, method)(o, *extras) for o in others]
        result = nodes[0]
        for node in nodes[1:]:
            result = Or([result, node])
        return Grouping(result)

    def _grouping_all(self, method: str, others: List[Any], *extras) -> 'Grouping':
        from arel.nodes.unary import Grouping
        from arel.nodes.nary import And

        nodes = [getattr(self, method)(o, *extras) for o in others]
        return Grouping(And(nodes))
```

### 2.2 Applying Mixins

```python
# arel/nodes/node.py

from arel.mixins.predications import PredicationsMixin
from arel.mixins.expressions import ExpressionsMixin
from arel.mixins.math_operations import MathMixin
from arel.mixins.order_predications import OrderPredicationsMixin
from arel.mixins.alias_predication import AliasPredicationMixin

class NodeExpression(
    Node,
    PredicationsMixin,
    ExpressionsMixin,
    MathMixin,
    OrderPredicationsMixin,
    AliasPredicationMixin
):
    """Node with full predication support."""
    pass
```

---

## Phase 3: Managers

### 3.1 TreeManager

```python
# arel/tree_manager.py

from typing import Optional, TYPE_CHECKING
from arel.mixins.factory_methods import FactoryMethodsMixin

if TYPE_CHECKING:
    from arel.nodes import Node

class TreeManager(FactoryMethodsMixin):
    """Base class for query managers."""

    def __init__(self):
        self._ast: Optional['Node'] = None

    @property
    def ast(self) -> 'Node':
        return self._ast

    def to_sql(self, engine=None) -> str:
        from arel.collectors import SQLString
        collector = SQLString()
        # engine.connection.visitor.accept(self.ast, collector).value
        raise NotImplementedError

    def to_dot(self) -> str:
        from arel.visitors import Dot
        from arel.collectors import PlainString
        collector = PlainString()
        visitor = Dot()
        return visitor.accept(self.ast, collector).value

    def __copy__(self):
        import copy
        new = self.__class__.__new__(self.__class__)
        new._ast = copy.copy(self._ast)
        return new
```

### 3.2 SelectManager

```python
# arel/select_manager.py

from typing import Any, List, Optional, Union
from arel.tree_manager import TreeManager
from arel.mixins.crud import CrudMixin

class SelectManager(TreeManager, CrudMixin):
    """Builds SELECT queries."""

    def __init__(self, table=None):
        super().__init__()
        from arel.nodes.statements import SelectStatement
        self._ast = SelectStatement(table)
        self._ctx = self._ast.cores[-1]

    def project(self, *projections: Any) -> 'SelectManager':
        from arel.nodes.literals import SqlLiteral
        for p in projections:
            if isinstance(p, (str, type(None))):
                p = SqlLiteral(str(p) if p else '*')
            self._ctx.projections.append(p)
        return self

    def from_(self, table: Any) -> 'SelectManager':
        from arel.nodes.literals import SqlLiteral
        from arel.nodes.joins import Join

        if isinstance(table, str):
            table = SqlLiteral(table)

        if isinstance(table, Join):
            self._ctx.source.right.append(table)
        else:
            self._ctx.source.left = table
        return self

    def where(self, expr: Any) -> 'SelectManager':
        if isinstance(expr, TreeManager):
            expr = expr.ast
        self._ctx.wheres.append(expr)
        return self

    def join(self, relation: Any, klass=None) -> 'SelectManager':
        if relation is None:
            return self

        from arel.nodes.joins import InnerJoin, StringJoin
        from arel.nodes.literals import SqlLiteral
        from arel.errors import EmptyJoinError

        if klass is None:
            klass = InnerJoin

        if isinstance(relation, (str, SqlLiteral)):
            if not relation:
                raise EmptyJoinError()
            klass = StringJoin

        join = self.create_join(relation, None, klass)
        self._ctx.source.right.append(join)
        return self

    def outer_join(self, relation: Any) -> 'SelectManager':
        from arel.nodes.joins import OuterJoin
        return self.join(relation, OuterJoin)

    def on(self, *exprs: Any) -> 'SelectManager':
        from arel.nodes.unary import On
        expr = self._collapse(exprs)
        self._ctx.source.right[-1].right = On(expr)
        return self

    def group(self, *columns: Any) -> 'SelectManager':
        from arel.nodes.unary import Group
        from arel.nodes.literals import SqlLiteral

        for column in columns:
            if isinstance(column, str):
                column = SqlLiteral(column)
            self._ctx.groups.append(Group(column))
        return self

    def having(self, expr: Any) -> 'SelectManager':
        self._ctx.havings.append(expr)
        return self

    def order(self, *exprs: Any) -> 'SelectManager':
        from arel.nodes.literals import SqlLiteral

        for expr in exprs:
            if isinstance(expr, str):
                expr = SqlLiteral(expr)
            self._ast.orders.append(expr)
        return self

    def take(self, limit: Optional[int]) -> 'SelectManager':
        from arel.nodes.unary import Limit
        self._ast.limit = Limit(limit) if limit is not None else None
        return self

    def skip(self, offset: Optional[int]) -> 'SelectManager':
        from arel.nodes.unary import Offset
        self._ast.offset = Offset(offset) if offset is not None else None
        return self

    def distinct(self, value: bool = True) -> 'SelectManager':
        from arel.nodes.terminal import Distinct
        self._ctx.set_quantifier = Distinct() if value else None
        return self

    # ... more methods ...

    @property
    def limit(self) -> Optional[int]:
        return self._ast.limit.expr if self._ast.limit else None

    @property
    def constraints(self) -> List[Any]:
        return self._ctx.wheres

    @property
    def orders(self) -> List[Any]:
        return self._ast.orders

    def _collapse(self, exprs):
        from arel.nodes.literals import SqlLiteral

        exprs = [e for e in exprs if e is not None]
        exprs = [SqlLiteral(e) if isinstance(e, str) else e for e in exprs]

        if len(exprs) == 1:
            return exprs[0]
        else:
            return self.create_and(exprs)
```

---

## Phase 4: Visitors

### 4.1 Base Visitor

```python
# arel/visitors/visitor.py

from typing import Any, Optional, Dict, Type

class Visitor:
    """Base visitor implementing dispatch mechanism."""

    _dispatch_cache: Dict[Type, str] = {}

    def __init__(self):
        pass

    @classmethod
    def _get_dispatch_method(cls, klass: Type) -> str:
        if klass not in cls._dispatch_cache:
            # Convert Arel::Nodes::Equality to visit_Arel_Nodes_Equality
            name = klass.__module__ + '.' + klass.__qualname__
            method_name = 'visit_' + name.replace('.', '_')
            cls._dispatch_cache[klass] = method_name
        return cls._dispatch_cache[klass]

    def accept(self, object: Any, collector: Any = None) -> Any:
        return self.visit(object, collector)

    def visit(self, object: Any, collector: Any = None) -> Any:
        method_name = self._get_dispatch_method(object.__class__)
        method = getattr(self, method_name, None)

        if method is None:
            # Try to find method for parent class
            for base in object.__class__.__mro__[1:]:
                method_name = self._get_dispatch_method(base)
                method = getattr(self, method_name, None)
                if method is not None:
                    # Cache the resolution
                    self._dispatch_cache[object.__class__] = method_name
                    break

        if method is None:
            raise TypeError(f"Cannot visit {object.__class__}")

        if collector is not None:
            return method(object, collector)
        else:
            return method(object)
```

### 4.2 ToSql Visitor

```python
# arel/visitors/to_sql.py

from typing import Any, Optional
from .visitor import Visitor

class UnsupportedVisitError(Exception):
    def __init__(self, object):
        super().__init__(
            f"Unsupported argument type: {object.__class__.__name__}. "
            "Construct an Arel node instead."
        )

class ToSql(Visitor):
    """Compiles AST to SQL."""

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def compile(self, node, collector=None):
        if collector is None:
            from arel.collectors import SQLString
            collector = SQLString()
        return self.accept(node, collector).value

    # Statement visitors

    def visit_arel_nodes_statements_SelectStatement(self, o, collector):
        if o.with_:
            collector = self.visit(o.with_, collector)
            collector << " "

        for core in o.cores:
            collector = self.visit_arel_nodes_statements_SelectCore(core, collector)

        if o.orders:
            collector << " ORDER BY "
            self._inject_join(o.orders, collector, ", ")

        collector = self._maybe_visit(o.limit, collector)
        collector = self._maybe_visit(o.offset, collector)
        collector = self._maybe_visit(o.lock, collector)

        return collector

    def visit_arel_nodes_statements_SelectCore(self, o, collector):
        collector << "SELECT"

        collector = self._maybe_visit(o.set_quantifier, collector)

        self._collect_nodes_for(o.projections, collector, " ")

        if o.source and not o.source.is_empty():
            collector << " FROM "
            collector = self.visit(o.source, collector)

        self._collect_nodes_for(o.wheres, collector, " WHERE ", " AND ")
        self._collect_nodes_for(o.groups, collector, " GROUP BY ")
        self._collect_nodes_for(o.havings, collector, " HAVING ", " AND ")

        collector = self._maybe_visit(o.comment, collector)

        return collector

    # Binary visitors

    def visit_arel_nodes_binary_Equality(self, o, collector):
        right = o.right

        if self._unboundable(right):
            collector << "1=0"
            return collector

        collector = self.visit(o.left, collector)

        if right is None or (hasattr(right, 'nil') and right.nil()):
            collector << " IS NULL"
        else:
            collector << " = "
            collector = self.visit(right, collector)

        return collector

    def visit_arel_nodes_binary_NotEqual(self, o, collector):
        right = o.right

        if self._unboundable(right):
            collector << "1=1"
            return collector

        collector = self.visit(o.left, collector)

        if right is None or (hasattr(right, 'nil') and right.nil()):
            collector << " IS NOT NULL"
        else:
            collector << " != "
            collector = self.visit(right, collector)

        return collector

    # ... many more visit methods ...

    # Helper methods

    def _maybe_visit(self, thing, collector):
        if thing is None:
            return collector
        collector << " "
        return self.visit(thing, collector)

    def _inject_join(self, list_, collector, join_str):
        for i, item in enumerate(list_):
            if i > 0:
                collector << join_str
            collector = self.visit(item, collector)
        return collector

    def _collect_nodes_for(self, nodes, collector, spacer, connector=", "):
        if nodes:
            collector << spacer
            self._inject_join(nodes, collector, connector)

    def _quote(self, value):
        return self.connection.quote(value)

    def _quote_table_name(self, name):
        return self.connection.quote_table_name(name)

    def _quote_column_name(self, name):
        return self.connection.quote_column_name(name)

    def _unboundable(self, value):
        return hasattr(value, 'unboundable') and value.unboundable()
```

---

## Phase 5: Database Adapters

Each adapter inherits ToSql and overrides specific methods.

```python
# arel/visitors/postgresql.py

from .to_sql import ToSql

class PostgreSQL(ToSql):
    """PostgreSQL-specific SQL compiler."""

    BIND_BLOCK = lambda i: f"${i}"

    def visit_arel_nodes_binary_Matches(self, o, collector):
        op = " LIKE " if o.case_sensitive else " ILIKE "
        collector = self._infix_value(o, collector, op)
        if o.escape:
            collector << " ESCAPE "
            collector = self.visit(o.escape, collector)
        return collector

    def visit_arel_nodes_binary_Regexp(self, o, collector):
        op = " ~ " if o.case_sensitive else " ~* "
        return self._infix_value(o, collector, op)

    def visit_arel_nodes_unary_DistinctOn(self, o, collector):
        collector << "DISTINCT ON ( "
        collector = self.visit(o.expr, collector)
        collector << " )"
        return collector

    # ... more PostgreSQL-specific methods ...
```

---

## Phase 6: Integration & Testing

### 6.1 Public API

```python
# arel/__init__.py

from arel.table import Table
from arel.select_manager import SelectManager
from arel.insert_manager import InsertManager
from arel.update_manager import UpdateManager
from arel.delete_manager import DeleteManager
from arel.nodes import build_quoted
from arel.nodes.literals import SqlLiteral

def sql(string: str, retryable: bool = False) -> SqlLiteral:
    """Create a SQL literal."""
    return SqlLiteral(string, retryable=retryable)

def star() -> SqlLiteral:
    """Create a * literal."""
    return SqlLiteral('*')

def arel_node(obj) -> bool:
    """Check if object is an Arel node."""
    from arel.nodes.node import Node
    from arel.nodes.literals import SqlLiteral
    from arel.attributes import Attribute
    return isinstance(obj, (Node, SqlLiteral, Attribute))

__all__ = [
    'Table',
    'SelectManager',
    'InsertManager',
    'UpdateManager',
    'DeleteManager',
    'sql',
    'star',
    'arel_node',
    'build_quoted',
]
```

### 6.2 Usage Examples

```python
from arel import Table, sql

# Create table
users = Table('users')

# Simple SELECT
query = (users
    .project(users['name'], users['email'])
    .where(users['active'].eq(True))
    .order(users['created_at'].desc())
    .take(10))

# With JOINs
posts = Table('posts')
query = (users
    .project(users['name'], posts['title'])
    .join(posts)
    .on(posts['user_id'].eq(users['id']))
    .where(users['active'].eq(True)))

# Complex conditions
query = (users
    .where(users['age'].gt(18).and_(users['country'].eq('US')))
    .where(users['name'].matches('%John%')))

# Aggregations
query = (users
    .project(users['country'], users['id'].count())
    .group(users['country'])
    .having(users['id'].count().gt(10)))

# Window functions
query = (users
    .project(
        users['name'],
        users['salary'].sum().over(
            Window().partition(users['department'])
        ).as_('dept_total')
    ))
```
