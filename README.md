# Py-Arel

Python port of [Arel](https://github.com/rails/arel) library (Ruby) for building SQL queries via Abstract Syntax Tree (AST).

## About

**Arel** (A Relational Algebra) is a powerful library that allows you to build SQL queries programmatically using an Abstract Syntax Tree instead of working with raw SQL strings. This Python port brings the same capabilities to Python developers.

### Why Arel?

- **Type-safe query building**: Build queries programmatically with full IDE support
- **Database agnostic**: Write queries once, compile to different SQL dialects (PostgreSQL, MySQL, SQLite)
- **Composable**: Easily combine, modify, and transform queries
- **Safe**: Avoid SQL injection by design - values are properly quoted and parameterized
- **Powerful**: Support for complex queries including CTEs, window functions, subqueries, and more

### Key Features

- ✅ **Complete AST representation** of SQL queries
- ✅ **Visitor pattern** for SQL generation with database-specific adapters
- ✅ **Method chaining** for fluent query building
- ✅ **Predications**: `eq()`, `gt()`, `in_()`, `matches()`, `between()`, and more
- ✅ **Aggregate functions**: `count()`, `sum()`, `avg()`, `max()`, `min()`
- ✅ **Window functions**: `over()`, `partition()`, `rows()`, `range()`
- ✅ **CTEs** (Common Table Expressions): `with()`, `with_recursive()`
- ✅ **Set operations**: `union()`, `intersect()`, `except()`
- ✅ **Complex JOINs**: Inner, Outer, Full Outer, Right Outer
- ✅ **Subqueries**: Use SelectManager as values in conditions
- ✅ **Type casting**: Automatic type conversion for database values

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/py-arel.git
cd py-arel

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from arel import Table

# Create a table representation
users = Table('users')
posts = Table('posts')

# Simple SELECT query
query = (users
    .project(users['name'], users['email'])
    .where(users['active'].eq(True))
    .order(users['created_at'].desc())
    .take(10))

# Compile to SQL (requires an engine/connection)
sql = query.to_sql(engine)
# => SELECT "users"."name", "users"."email"
#    FROM "users"
#    WHERE "users"."active" = TRUE
#    ORDER BY "users"."created_at" DESC
#    LIMIT 10
```

### More Examples

```python
from arel import Table, sql

users = Table('users')
posts = Table('posts')

# JOIN query
query = (users
    .project(users['name'], posts['title'])
    .join(posts)
    .on(posts['user_id'].eq(users['id']))
    .where(users['active'].eq(True)))

# Aggregation with GROUP BY and HAVING
query = (users
    .project(users['country'], users['id'].count())
    .group(users['country'])
    .having(users['id'].count().gt(10)))

# Window functions
from arel.nodes.window import Window
query = (users
    .project(
        users['name'],
        users['salary'].sum().over(
            Window().partition(users['department'])
        ).as_('dept_total')
    ))

# CTE (Common Table Expression)
active_users = (users
    .project(users['*'])
    .where(users['active'].eq(True))
    .as_('active_users'))

query = (users.from_()
    .with_(active_users.to_cte())
    .project(sql('*'))
    .from_(Table('active_users')))

# Complex conditions
query = (users
    .where(
        users['age'].gt(18)
        .and_(users['country'].eq('US'))
        .or_(users['verified'].eq(True))
    ))

# IN with subquery
active_authors = posts.project(posts['user_id']).where(posts['published'].eq(True))
query = (users
    .project(users['name'])
    .where(users['id'].in_(active_authors)))
```

## API Differences from Ruby

Due to Python's syntax limitations, some method names differ from Ruby:

| Ruby | Python | Reason |
|------|--------|---------|
| `or` | `or_` | `or` is a reserved keyword |
| `and` | `and_` | `and` is a reserved keyword |
| `not` | `not_` | `not` is a reserved keyword |
| `in` | `in_` | `in` is a reserved keyword |
| `from` | `from_` | `from` is a reserved keyword |
| `True` node | `True_` | `True` is a reserved word |
| `False` node | `False_` | `False` is a reserved word |
| `equality?` | `is_equality()` | Python doesn't support `?` in names |
| `ascending?` | `is_ascending()` | Python doesn't support `?` in names |

## Project Structure

```
py-arel/
├── arel/                    # Main library code
│   ├── __init__.py         # Public API exports
│   ├── table.py            # Table class (entry point)
│   ├── tree_manager.py     # Base class for query managers
│   ├── select_manager.py   # SELECT query builder
│   ├── insert_manager.py   # INSERT query builder
│   ├── update_manager.py   # UPDATE query builder
│   ├── delete_manager.py   # DELETE query builder
│   ├── nodes/              # AST nodes
│   │   ├── node.py         # Base Node class
│   │   ├── binary.py       # Binary nodes (left, right)
│   │   ├── unary.py        # Unary nodes (expr)
│   │   ├── nary.py         # N-ary nodes (And, Or)
│   │   ├── statements.py   # Statement nodes (Select, Insert, etc.)
│   │   ├── functions.py    # Function nodes (Count, Sum, etc.)
│   │   ├── window.py       # Window function nodes
│   │   ├── case.py         # CASE WHEN nodes
│   │   ├── cte.py          # CTE nodes (With, Cte)
│   │   ├── joins.py        # JOIN nodes
│   │   ├── literals.py     # SqlLiteral, BoundSqlLiteral
│   │   └── ...             # Other node types
│   ├── visitors/            # SQL compilers
│   │   ├── visitor.py      # Base Visitor class
│   │   ├── to_sql.py       # Main SQL compiler
│   │   ├── mysql.py        # MySQL-specific compiler
│   │   ├── postgresql.py   # PostgreSQL-specific compiler
│   │   ├── sqlite.py       # SQLite-specific compiler
│   │   └── dot.py          # DOT graph visualization
│   ├── collectors/          # Result collectors
│   │   ├── plain_string.py # Simple string collector
│   │   ├── sql_string.py   # SQL string with bind params
│   │   ├── bind.py         # Bind values collector
│   │   └── composite.py    # Composite collector
│   ├── mixins/              # Mixins for functionality
│   │   ├── predications.py # Conditions (eq, gt, in, etc.)
│   │   ├── expressions.py  # Aggregate functions
│   │   ├── math_operations.py # Arithmetic operations
│   │   └── ...             # Other mixins
│   └── attributes/          # Table attributes
│       └── attribute.py     # Column representation
├── tests/                   # Test suite
│   ├── test_table.py       # Table tests
│   ├── test_select_manager.py # SelectManager tests
│   ├── nodes/              # Node tests
│   ├── visitors/           # Visitor tests
│   ├── attributes/         # Attribute tests
│   └── ...                 # Other tests
├── ai/                      # Documentation
│   ├── 01_architecture_overview.md
│   ├── 02_classes_documentation.md
│   ├── 03_visitors_documentation.md
│   ├── 04_mixins_documentation.md
│   ├── 05_python_implementation_plan.md
│   ├── 06_challenges_and_solutions.md
│   ├── 07_class_reference.md
│   ├── 08_testing_strategy.md
│   └── 09_test_coverage.md
├── Dockerfile               # Docker image
├── docker-compose.yml       # Docker Compose config
├── requirements.txt         # Python dependencies
└── Makefile                # Convenient commands
```

## Quick Start with Docker

### Requirements
- Docker
- Docker Compose (optional, can use `docker` directly)

### First Setup

```bash
# Quick check that everything works
./check-docker.sh

# Or manually:
docker-compose build
```

### Running Tests

```bash
# Build image (if not built yet)
make build
# or
docker-compose build

# Run all tests
make test
# or
docker-compose run --rm py-arel pytest tests/ -v

# Run specific test
make test-file FILE=test_table.py
# or
docker-compose run --rm py-arel pytest tests/test_table.py -v

# Run with coverage
docker-compose run --rm py-arel pytest tests/ --cov=arel --cov-report=html
```

### Interactive Work

```bash
# Start container in background
make up

# Enter container
make shell
# or
docker-compose exec py-arel /bin/bash

# Inside container you can run tests directly
pytest tests/ -v
python3 -c "from arel import Table; print(Table('users').project('*').to_sql())"
```

### Cleanup

```bash
# Stop and remove containers
make down

# Full cleanup (containers + images)
make clean
```

## Development without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Run tests
pytest tests/ -v
# or
python3 -m pytest tests/
```

## How It Works

### 1. Building Queries

Queries are built using method chaining on `Table` and `SelectManager` objects:

```python
users = Table('users')
query = users.project(users['name']).where(users['active'].eq(True))
```

Each method call creates AST nodes that represent the query structure.

### 2. AST Representation

The query is represented as a tree of nodes:

```
SelectStatement
├── SelectCore
│   ├── projections: [Attribute(name='name')]
│   ├── source: JoinSource
│   │   └── left: Table(name='users')
│   └── wheres: [Equality(left=Attribute, right=True)]
└── orders: []
```

### 3. SQL Compilation

A Visitor traverses the AST and generates SQL:

```python
from arel.visitors import ToSql
from arel.collectors import SQLString

visitor = ToSql(connection)
collector = SQLString()
sql = visitor.accept(query.ast, collector).value
# => SELECT "users"."name" FROM "users" WHERE "users"."active" = TRUE
```

### 4. Database-Specific Compilation

Different visitors handle database-specific SQL:

- **PostgreSQL**: Uses `ILIKE`, `~`, `~*`, `IS DISTINCT FROM`, `LATERAL`, etc.
- **MySQL**: Uses `CONCAT()`, `REGEXP`, `DUAL`, `<=>` (NULL-safe equality)
- **SQLite**: Uses `IS`, `IS NOT`, handles `LIMIT -1` for OFFSET without LIMIT

## Documentation

Comprehensive documentation is available in the `ai/` directory:

- **[Architecture Overview](ai/01_architecture_overview.md)** - Core concepts and architecture
- **[Class Documentation](ai/02_classes_documentation.md)** - Detailed class reference
- **[Visitors Documentation](ai/03_visitors_documentation.md)** - SQL compilation details
- **[Mixins Documentation](ai/04_mixins_documentation.md)** - Available mixins and methods
- **[Implementation Plan](ai/05_python_implementation_plan.md)** - Implementation roadmap
- **[Challenges & Solutions](ai/06_challenges_and_solutions.md)** - Porting challenges
- **[Class Reference](ai/07_class_reference.md)** - Quick class reference
- **[Testing Strategy](ai/08_testing_strategy.md)** - Testing approach
- **[Test Coverage](ai/09_test_coverage.md)** - Test porting status

## Porting Status

This is a **work-in-progress** port of Ruby Arel to Python. Current status:

- ✅ **Core AST nodes**: Binary, Unary, Nary, Statements
- ✅ **Query builders**: SelectManager, InsertManager, UpdateManager, DeleteManager
- ✅ **Predications**: All comparison and matching methods
- ✅ **Expressions**: Aggregate functions (count, sum, avg, etc.)
- ✅ **SQL compilation**: Base ToSql visitor
- ✅ **Database adapters**: PostgreSQL, MySQL, SQLite
- ✅ **Advanced features**: CTEs, Window functions, Subqueries
- ✅ **Test coverage**: 725+ tests ported from Ruby

See [ai/09_test_coverage.md](ai/09_test_coverage.md) for detailed test porting status.

## Contributing

Contributions are welcome! Please:

1. Check existing issues and pull requests
2. Follow the existing code style
3. Add tests for new features
4. Update documentation as needed
5. Ensure all tests pass: `make test`

## License

This project is a port of Arel, which is part of Ruby on Rails and is licensed under the MIT License.

## Acknowledgments

- Original [Arel](https://github.com/rails/arel) library by the Rails team
- Ruby on Rails community for the excellent design

## Related Projects

- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and ORM
- [Pony ORM](https://ponyorm.org/) - Python ORM with query builder
- [Peewee](https://github.com/coleifer/peewee) - Small, expressive Python ORM
