# AREL Architecture Overview

## What is AREL?

AREL (A Relational Algebra) is a library for building SQL queries as an Abstract Syntax Tree (AST). Instead of working with SQL strings, AREL allows programmatic construction of queries that are then compiled to SQL for a specific database.

## Core Concepts

### 1. AST (Abstract Syntax Tree)
Each SQL query is represented as a tree of nodes (`Node`). This allows:
- Programmatic manipulation of queries
- Compilation to different SQL dialects
- Query optimization and analysis

### 2. Visitor Pattern
The Visitor pattern is used to traverse and compile the AST. Each node is "visited" by a visitor that generates the corresponding SQL.

### 3. Predications
Methods for creating conditions (predicates): `eq`, `not_eq`, `gt`, `lt`, `matches`, `in`, etc.

## Module Structure

```
arel/
├── table.rb                 # Entry point - table representation
├── tree_manager.rb          # Base class for all managers
├── select_manager.rb        # SELECT query manager
├── insert_manager.rb        # INSERT query manager
├── update_manager.rb        # UPDATE query manager
├── delete_manager.rb        # DELETE query manager
├── nodes/                   # All AST nodes
│   ├── node.rb              # Base node class
│   ├── node_expression.rb   # Node with predications support
│   ├── binary.rb            # Binary nodes (left, right)
│   ├── unary.rb             # Unary nodes (expr)
│   ├── nary.rb              # N-ary nodes (And, Or)
│   └── ...                  # Specific node types
├── visitors/                # SQL compilers
│   ├── visitor.rb           # Base visitor
│   ├── to_sql.rb            # Main SQL compiler
│   ├── mysql.rb             # MySQL-specific
│   ├── postgresql.rb        # PostgreSQL-specific
│   └── sqlite.rb            # SQLite-specific
├── collectors/              # Result collectors
│   ├── sql_string.rb        # SQL string builder
│   └── bind.rb              # Bind parameters collector
├── attributes/              # Attributes (columns)
│   └── attribute.rb         # Table column representation
└── predications.rb          # Mixin with condition methods
```

## Node Class Hierarchy

```
Node
├── NodeExpression (with Predications, Math, Expressions)
│   ├── Binary (left, right)
│   │   ├── Equality, NotEqual
│   │   ├── GreaterThan, LessThan, etc.
│   │   ├── In, NotIn
│   │   ├── Join, InnerJoin, OuterJoin
│   │   ├── As, TableAlias
│   │   └── InfixOperation (+, -, *, /)
│   ├── Unary (expr)
│   │   ├── Not, Grouping
│   │   ├── Limit, Offset, Lock
│   │   ├── Ascending, Descending
│   │   └── With, WithRecursive
│   ├── Nary (children)
│   │   ├── And
│   │   └── Or
│   ├── Function
│   │   ├── Count, Sum, Max, Min, Avg
│   │   └── NamedFunction
│   ├── SelectStatement
│   ├── Case
│   ├── Casted, Quoted
│   └── Terminal (no data)
│       ├── True, False
│       └── Distinct
├── SelectCore
├── InsertStatement
├── UpdateStatement
├── DeleteStatement
└── SqlLiteral (inherits String!)
```

## Mixins (Modules)

### Predications
Methods for creating conditions:
- `eq(other)` → Equality
- `not_eq(other)` → NotEqual
- `gt(other)` → GreaterThan
- `lt(other)` → LessThan
- `gteq(other)` → GreaterThanOrEqual
- `lteq(other)` → LessThanOrEqual
- `matches(pattern)` → Matches (LIKE)
- `in(values)` → In
- `between(range)` → Between or composition
- `is_distinct_from(other)`
- And many others...

### Expressions
Aggregate functions:
- `count()` → Count
- `sum()` → Sum
- `maximum()` → Max
- `minimum()` → Min
- `average()` → Avg
- `extract(field)` → Extract

### Math
Arithmetic operations:
- `+`, `-`, `*`, `/`
- `&`, `|`, `^` (bitwise)
- `<<`, `>>` (shifts)
- `~` (bitwise NOT)

### OrderPredications
- `asc()` → Ascending
- `desc()` → Descending

### AliasPredication
- `as(name)` → As

### WindowPredications
- `over(window)` → Over

### FilterPredications
- `filter(condition)` → Filter

### FactoryMethods
Factory methods for creating nodes:
- `create_true()`, `create_false()`
- `create_join()`, `create_on()`
- `create_and()`, `grouping()`
- `lower()`, `coalesce()`, `cast()`

## Collectors

Collectors gather the result of AST traversal:

### SQLString
Collects SQL string and manages bind parameters:
```ruby
collector << "SELECT "
collector.add_bind(value) { |i| "?" }
```

### Bind
Collects only bind values without SQL.

### Composite
Combines two collectors for parallel collection.

### SubstituteBinds
Substitutes values instead of bind placeholders.

## Data Flow

```
Table.new(:users)
    ↓
users[:name].eq("John")
    ↓
Equality(
  Attribute(relation=users, name="name"),
  Casted("John", Attribute)
)
    ↓
ToSql Visitor
    ↓
'"users"."name" = \'John\''
```

## Usage Example

```ruby
users = Arel::Table.new(:users)

# Simple SELECT
query = users.project(users[:name], users[:email])
            .where(users[:active].eq(true))
            .order(users[:created_at].desc)
            .take(10)

# Get SQL
query.to_sql
# => SELECT "users"."name", "users"."email"
#    FROM "users"
#    WHERE "users"."active" = TRUE
#    ORDER BY "users"."created_at" DESC
#    LIMIT 10
```
