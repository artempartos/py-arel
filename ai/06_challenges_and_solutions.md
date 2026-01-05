# Challenges When Porting to Python and Their Solutions

## 1. Language Differences

### 1.1 Ruby Mixins vs Python Multiple Inheritance

**Problem:** Ruby uses `include Module` to add methods. Python uses multiple inheritance.

**Ruby:**
```ruby
class Attribute < Struct.new(:relation, :name)
  include Arel::Expressions
  include Arel::Predications
  include Arel::AliasPredication
end
```

**Python Solution:**
```python
class Attribute(PredicationsMixin, ExpressionsMixin, AliasMixin):
    def __init__(self, relation, name):
        self.relation = relation
        self.name = name
```

**Problem:** MRO (Method Resolution Order) order matters. Python searches methods left to right.

**Solution:** Use correct base class order and avoid name conflicts.

---

### 1.2 Ruby Struct

**Problem:** `Attribute < Struct.new(:relation, :name)` creates a class with getters/setters.

**Solution 1: dataclass**
```python
from dataclasses import dataclass

@dataclass
class Attribute(PredicationsMixin):
    relation: Any
    name: str
```

**Solution 2: NamedTuple**
```python
from typing import NamedTuple, Any

class AttributeBase(NamedTuple):
    relation: Any
    name: str

class Attribute(AttributeBase, PredicationsMixin):
    pass
```

**Solution 3: Regular class**
```python
class Attribute(PredicationsMixin):
    __slots__ = ('relation', 'name')

    def __init__(self, relation, name):
        self.relation = relation
        self.name = name
```

**Recommendation:** Use regular classes for flexibility with mixins.

---

### 1.3 Ruby String Inheritance (SqlLiteral)

**Problem:** `SqlLiteral < String` - Ruby allows inheriting from built-in types.

**Ruby:**
```ruby
class SqlLiteral < String
  include Arel::Expressions
  include Arel::Predications
end
```

**Python Problem:** Inheriting from `str` is limited - `str` is immutable.

**Solution 1: Inherit from str**
```python
class SqlLiteral(str, PredicationsMixin):
    def __new__(cls, value, retryable=False):
        instance = super().__new__(cls, value)
        instance._retryable = retryable
        return instance

    @property
    def retryable(self):
        return self._retryable
```

**Solution 2: Wrapper**
```python
class SqlLiteral(PredicationsMixin):
    def __init__(self, value, retryable=False):
        self._value = str(value)
        self._retryable = retryable

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"SqlLiteral({self._value!r})"

    def __eq__(self, other):
        if isinstance(other, SqlLiteral):
            return self._value == other._value
        return self._value == other

    def __hash__(self):
        return hash(self._value)

    def __bool__(self):
        return bool(self._value)

    def __len__(self):
        return len(self._value)
```

**Recommendation:** Solution 2 is more flexible and clear.

---

### 1.4 Ruby method_missing / respond_to_missing

**Problem:** Ruby Visitor uses dynamic dispatch via `method_missing`.

**Ruby:**
```ruby
def visit(object, collector = nil)
  dispatch_method = dispatch[object.class]
  send dispatch_method, object, collector
rescue NoMethodError => e
  # fallback to parent classes
end
```

**Python Solution:**
```python
def visit(self, object, collector=None):
    method_name = self._get_dispatch_method(object.__class__)
    method = getattr(self, method_name, None)

    if method is None:
        # Walk through MRO to find handler
        for klass in object.__class__.__mro__[1:]:
            method_name = self._get_dispatch_method(klass)
            method = getattr(self, method_name, None)
            if method is not None:
                break

    if method is None:
        raise TypeError(f"Cannot visit {object.__class__}")

    return method(object, collector) if collector else method(object)
```

---

### 1.5 Ruby alias / alias_method

**Problem:** Ruby creates method aliases: `alias :== :eql?`

**Python Solution:**
```python
class Node:
    def eql(self, other):
        return self.__class__ == other.__class__

    __eq__ = eql  # Create alias
```

Or via decorator:
```python
def alias(*names):
    def decorator(method):
        method._aliases = names
        return method
    return decorator

# In __init_subclass__ or metaclass - copy methods
```

---

### 1.6 Ruby attr_accessor / attr_reader

**Problem:** Ruby automatically creates getters/setters.

**Ruby:**
```ruby
attr_accessor :left, :right
attr_reader :values
```

**Python Solution:** Use regular attributes or property:

```python
class Binary:
    def __init__(self, left, right):
        self.left = left  # readable and writable
        self.right = right

class Comment:
    def __init__(self, values):
        self._values = values  # private

    @property
    def values(self):  # read-only
        return self._values
```

---

### 1.7 Ruby block (&block)

**Problem:** Ruby passes blocks to methods.

**Ruby:**
```ruby
def add_bind(bind, &block)
  self << yield(@bind_index)
  @bind_index += 1
end
```

**Python Solution:** Use callable:

```python
def add_bind(self, bind, block):
    self << block(self._bind_index)
    self._bind_index += 1
```

Or lambda:
```python
collector.add_bind(value, lambda i: f"${i}")
```

---

### 1.8 Ruby respond_to? / is_a?

**Problem:** Ruby checks object capabilities.

**Ruby:**
```ruby
value.respond_to?(:unboundable?) && value.unboundable?
other.is_a?(Symbol)
```

**Python Solution:**

```python
# respond_to?
hasattr(value, 'unboundable') and value.unboundable()

# is_a?
isinstance(other, str)  # Symbol → str in Python

# Duck typing
try:
    result = value.unboundable()
except AttributeError:
    result = False
```

---

### 1.9 Ruby Symbol

**Problem:** Ruby Symbol `:name` vs Python.

**Solution:** In Python just use strings. Where symbol semantics are needed - can use Enum.

```python
from enum import Enum, auto

class Direction(Enum):
    ASC = auto()
    DESC = auto()
```

---

### 1.10 Ruby nil handling

**Problem:** Ruby `nil` has many methods, Python `None` - doesn't.

**Ruby:**
```ruby
@ast.limit && @ast.limit.expr  # safe navigation
klass&.type_caster  # safe navigation operator
```

**Python Solution:**

```python
# Explicit check
self._ast.limit.expr if self._ast.limit else None

# getattr with default
getattr(klass, 'type_caster', None)

# Python 3.10+ pattern matching
match self._ast.limit:
    case None:
        return None
    case limit:
        return limit.expr
```

---

## 2. Architectural Challenges

### 2.1 Circular Imports

**Problem:** Arel has many interdependent classes.

**Solution 1: TYPE_CHECKING**
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arel.nodes import Equality

class Attribute:
    def eq(self, other) -> 'Equality':
        from arel.nodes.binary import Equality
        return Equality(self, other)
```

**Solution 2: Lazy imports**
```python
def eq(self, other):
    # Import inside method
    from arel.nodes.binary import Equality
    return Equality(self, other)
```

**Solution 3: Module restructuring**
Extract common types into a separate module without dependencies.

---

### 2.2 Class-level variables

**Problem:** Ruby class-level variables and methods.

**Ruby:**
```ruby
class Table
  @engine = nil
  class << self; attr_accessor :engine; end
end
```

**Python Solution:**
```python
class Table:
    engine = None  # class variable

    @classmethod
    def set_engine(cls, engine):
        cls.engine = engine
```

---

### 2.3 Deep Clone

**Problem:** Ruby `clone` vs Python copying.

**Ruby:**
```ruby
def initialize_copy(other)
  super
  @cores = @cores.map { |x| x.clone }
end
```

**Python Solution:**
```python
import copy

class SelectStatement:
    def __copy__(self):
        new = SelectStatement.__new__(SelectStatement)
        new.cores = [copy.copy(c) for c in self.cores]
        new.orders = [copy.copy(o) for o in self.orders]
        # ...
        return new

    def __deepcopy__(self, memo):
        new = SelectStatement.__new__(SelectStatement)
        new.cores = copy.deepcopy(self.cores, memo)
        # ...
        return new
```

---

### 2.4 Connection/Engine integration

**Problem:** Arel is tightly coupled with ActiveRecord connection.

**Ruby:**
```ruby
def to_sql(engine = Table.engine)
  collector = Arel::Collectors::SQLString.new
  engine.with_connection do |connection|
    connection.visitor.accept(@ast, collector).value
  end
end
```

**Python Solution:**

```python
class Engine:
    """Abstract base for database engine."""
    def __init__(self, visitor_class):
        self._visitor_class = visitor_class

    def create_visitor(self):
        return self._visitor_class(self)

    def quote(self, value):
        raise NotImplementedError

    def quote_table_name(self, name):
        raise NotImplementedError

    def quote_column_name(self, name):
        raise NotImplementedError


class PostgreSQLEngine(Engine):
    def __init__(self):
        from arel.visitors import PostgreSQL
        super().__init__(PostgreSQL)

    def quote(self, value):
        if value is None:
            return 'NULL'
        if isinstance(value, bool):
            return 'TRUE' if value else 'FALSE'
        if isinstance(value, (int, float)):
            return str(value)
        return f"'{str(value).replace(chr(39), chr(39)+chr(39))}'"

    def quote_table_name(self, name):
        return f'"{name}"'

    def quote_column_name(self, name):
        return f'"{name}"'


# Usage
Table.engine = PostgreSQLEngine()
```

---

## 3. API Compatibility

### 3.1 Ruby method naming

**Problem:** Ruby methods can end with `?` and `!`.

**Ruby:**
```ruby
equality?
ascending?
empty?
```

**Python Solution:**

```python
# Option 1: is_ prefix
def is_equality(self) -> bool:
    return False

def is_ascending(self) -> bool:
    return True

def is_empty(self) -> bool:
    return not self.left and not self.right

# Option 2: Properties
@property
def empty(self) -> bool:
    return not self.left and not self.right
```

---

### 3.2 Ruby operators

**Problem:** Ruby allows overriding any operators.

**Ruby:**
```ruby
def or(right)
  Grouping.new Or.new([self, right])
end
```

**Python Solution:**

```python
# or/and/not - reserved keywords!
def or_(self, right):
    return Grouping(Or([self, right]))

def and_(self, right):
    return And([self, right])

def not_(self):
    return Not(self)

# For chaining, can use | and & operators
def __or__(self, other):
    return self.or_(other)

def __and__(self, other):
    return self.and_(other)

def __invert__(self):
    return self.not_()
```

**Usage:**
```python
# Method call
users['active'].eq(True).or_(users['admin'].eq(True))

# Operator overloading
users['active'].eq(True) | users['admin'].eq(True)
~users['deleted'].eq(True)  # NOT
```

---

### 3.3 Ruby [] operator

**Problem:** Ruby `table[:column]` vs Python.

**Solution:** Python supports this directly:

```python
class Table:
    def __getitem__(self, name):
        if isinstance(name, str):
            # Handle alias resolution if needed
            pass
        return Attribute(self, name)
```

---

### 3.4 Method chaining

**Problem:** All methods must return `self` for chaining.

**Solution:** Explicitly return `self`:

```python
def where(self, expr):
    self._ctx.wheres.append(expr)
    return self  # IMPORTANT!

def order(self, *exprs):
    self._ast.orders.extend(exprs)
    return self  # IMPORTANT!
```

---

## 4. Testing

### 4.1 Test Structure

Recommended structure mirroring source code:

```
tests/
├── conftest.py
├── test_table.py
├── test_select_manager.py
├── nodes/
│   ├── test_binary.py
│   ├── test_unary.py
│   └── ...
├── visitors/
│   ├── test_to_sql.py
│   ├── test_postgresql.py
│   └── ...
└── integration/
    └── test_complex_queries.py
```

### 4.2 Fixtures

```python
# conftest.py
import pytest
from arel import Table
from arel.visitors import PostgreSQL

@pytest.fixture
def users():
    return Table('users')

@pytest.fixture
def posts():
    return Table('posts')

@pytest.fixture
def engine():
    return MockEngine()

@pytest.fixture
def visitor(engine):
    return PostgreSQL(engine)
```

### 4.3 Test Example

```python
def test_equality(users, visitor):
    """Test users[:name].eq('John')"""
    node = users['name'].eq('John')

    # Test node structure
    assert isinstance(node, Equality)
    assert isinstance(node.left, Attribute)
    assert node.left.name == 'name'

    # Test SQL generation
    from arel.collectors import SQLString
    collector = SQLString()
    result = visitor.accept(node, collector)
    assert result.value == '"users"."name" = \'John\''
```

---

## 5. Recommendations

### 5.1 Implementation Order

1. **Start with Node and base nodes** - Binary, Unary, Nary
2. **Add SqlLiteral** - needed everywhere
3. **Implement Casted/Quoted** - for values
4. **Add Attribute** - entry point for predications
5. **Implement Predications** - eq, gt, lt, in...
6. **Create Statement nodes** - Select, Insert, Update, Delete
7. **Implement Managers** - SelectManager first
8. **Add Table** - tie everything together
9. **Implement ToSql Visitor** - base
10. **Add specific visitors** - PostgreSQL, MySQL, SQLite

### 5.2 Iterative Development

At each step:
1. Implement class
2. Write tests
3. Check API compatibility with Ruby
4. Document differences

### 5.3 Type hints

Use type hints everywhere:

```python
from typing import Any, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from arel.nodes import Node
    from arel.table import Table

def eq(self, other: Any) -> 'Equality':
    ...

def where(self, expr: Union['Node', 'TreeManager']) -> 'SelectManager':
    ...
```

### 5.4 Documentation

Every public class and method should have a docstring:

```python
class Equality(Binary):
    """Represents an equality condition (=).

    Generates SQL like: "table"."column" = 'value'

    When the right side is None, generates: "table"."column" IS NULL

    Examples:
        >>> users['name'].eq('John')
        # "users"."name" = 'John'

        >>> users['deleted_at'].eq(None)
        # "users"."deleted_at" IS NULL
    """
    pass
```
