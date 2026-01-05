# py-arel Testing Strategy

## Test Structure

```
tests/
├── conftest.py                 # Fixtures
├── test_table.py               # Table tests
├── test_select_manager.py      # SelectManager tests
├── test_insert_manager.py      # InsertManager tests
├── test_update_manager.py      # UpdateManager tests
├── test_delete_manager.py      # DeleteManager tests
├── nodes/
│   ├── test_node.py            # Base node tests
│   ├── test_binary.py          # Binary nodes
│   ├── test_unary.py           # Unary nodes
│   ├── test_nary.py            # And/Or tests
│   ├── test_equality.py        # Equality tests
│   ├── test_in.py              # In/NotIn tests
│   ├── test_function.py        # Function tests
│   ├── test_window.py          # Window function tests
│   ├── test_case.py            # Case/When tests
│   ├── test_cte.py             # CTE tests
│   ├── test_ordering.py        # Ordering tests
│   ├── test_literals.py        # SqlLiteral tests
│   └── test_casted.py          # Casted/Quoted tests
├── visitors/
│   ├── test_to_sql.py          # Base SQL visitor
│   ├── test_postgresql.py      # PostgreSQL visitor
│   ├── test_mysql.py           # MySQL visitor
│   ├── test_sqlite.py          # SQLite visitor
│   └── test_dot.py             # DOT visitor
├── attributes/
│   └── test_attribute.py       # Attribute tests
├── collectors/
│   ├── test_sql_string.py
│   ├── test_bind.py
│   └── test_composite.py
├── mixins/
│   ├── test_predications.py    # Predications mixin
│   ├── test_expressions.py     # Expressions mixin
│   └── test_math.py            # Math mixin
└── integration/
    ├── test_complex_queries.py # Complex query tests
    └── test_real_db.py         # Real database tests
```

---

## Fixtures (conftest.py)

```python
import pytest
from arel import Table
from arel.visitors import ToSql, PostgreSQL, MySQL, SQLite

class MockConnection:
    """Mock database connection for testing."""

    def quote(self, value):
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        return f"'{value}'"

    def quote_table_name(self, name):
        if isinstance(name, str):
            return f'"{name}"'
        return str(name)

    def quote_column_name(self, name):
        if isinstance(name, str):
            return f'"{name}"'
        return str(name)

    def sanitize_as_sql_comment(self, value):
        return value.replace("*/", "* /")


@pytest.fixture
def connection():
    return MockConnection()


@pytest.fixture
def visitor(connection):
    return ToSql(connection)


@pytest.fixture
def pg_visitor(connection):
    return PostgreSQL(connection)


@pytest.fixture
def mysql_visitor(connection):
    return MySQL(connection)


@pytest.fixture
def sqlite_visitor(connection):
    return SQLite(connection)


@pytest.fixture
def users():
    return Table("users")


@pytest.fixture
def posts():
    return Table("posts")


@pytest.fixture
def comments():
    return Table("comments")


def compile(node, visitor):
    """Helper to compile node to SQL."""
    from arel.collectors import SQLString
    collector = SQLString()
    return visitor.accept(node, collector).value
```

---

## Node Tests

### test_node.py

```python
import pytest
from arel.nodes import Node, NodeExpression
from arel.nodes.unary import Not, Grouping
from arel.nodes.nary import And, Or


class TestNode:
    """Tests for base Node class."""

    def test_not_creates_not_node(self, users):
        """Test node.not_() creates Not wrapper."""
        condition = users['active'].eq(True)
        result = condition.not_()

        assert isinstance(result, Not)
        assert result.expr == condition

    def test_or_creates_grouping_with_or(self, users):
        """Test node.or_() creates Grouping(Or(...))."""
        left = users['active'].eq(True)
        right = users['admin'].eq(True)
        result = left.or_(right)

        assert isinstance(result, Grouping)
        assert isinstance(result.expr, Or)
        assert result.expr.children == [left, right]

    def test_and_creates_and_node(self, users):
        """Test node.and_() creates And node."""
        left = users['active'].eq(True)
        right = users['verified'].eq(True)
        result = left.and_(right)

        assert isinstance(result, And)
        assert result.children == [left, right]

    def test_invert_creates_not_node(self, users):
        """Test node.invert() creates Not wrapper."""
        condition = users['active'].eq(True)
        result = condition.invert()

        assert isinstance(result, Not)
        assert result.expr == condition
```

### test_binary.py

```python
import pytest
from arel.nodes.binary import (
    Binary, Equality, NotEqual,
    GreaterThan, GreaterThanOrEqual,
    LessThan, LessThanOrEqual,
    In, NotIn
)


class TestBinary:
    """Tests for Binary nodes."""

    def test_binary_has_left_and_right(self):
        """Test Binary stores left and right."""
        node = Binary("left", "right")

        assert node.left == "left"
        assert node.right == "right"

    def test_binary_equality(self):
        """Test Binary nodes are equal if same class and same children."""
        node1 = Binary("a", "b")
        node2 = Binary("a", "b")
        node3 = Binary("a", "c")

        assert node1 == node2
        assert node1 != node3

    def test_binary_hash(self):
        """Test Binary nodes have consistent hash."""
        node1 = Binary("a", "b")
        node2 = Binary("a", "b")

        assert hash(node1) == hash(node2)

        # Can be used as dict key
        d = {node1: "value"}
        assert d[node2] == "value"


class TestEquality:
    """Tests for Equality node."""

    def test_is_equality_returns_true(self, users):
        """Test Equality.is_equality() returns True."""
        node = users['id'].eq(1)
        assert node.is_equality() is True

    def test_invert_returns_not_equal(self, users):
        """Test Equality.invert() returns NotEqual."""
        eq = users['id'].eq(1)
        result = eq.invert()

        assert isinstance(result, NotEqual)
        assert result.left == eq.left
        assert result.right == eq.right


class TestComparisons:
    """Tests for comparison nodes."""

    def test_greater_than_invert(self, users):
        """Test GreaterThan.invert() returns LessThanOrEqual."""
        gt = users['age'].gt(18)
        result = gt.invert()

        assert isinstance(result, LessThanOrEqual)

    def test_less_than_invert(self, users):
        """Test LessThan.invert() returns GreaterThanOrEqual."""
        lt = users['age'].lt(65)
        result = lt.invert()

        assert isinstance(result, GreaterThanOrEqual)
```

---

## Predications Tests

### test_predications.py

```python
import pytest
from arel.nodes.binary import Equality, NotEqual, GreaterThan, In, Matches
from arel.nodes.nary import And, Or
from arel.nodes.unary import Grouping


class TestPredicationsEq:
    """Tests for eq/not_eq methods."""

    def test_eq_creates_equality(self, users):
        """Test eq() creates Equality node."""
        result = users['name'].eq('John')

        assert isinstance(result, Equality)
        assert result.left == users['name']

    def test_not_eq_creates_not_equal(self, users):
        """Test not_eq() creates NotEqual node."""
        result = users['name'].not_eq('John')

        assert isinstance(result, NotEqual)

    def test_eq_with_none(self, users):
        """Test eq(None) for IS NULL."""
        result = users['deleted_at'].eq(None)

        assert isinstance(result, Equality)
        # SQL should be "IS NULL"


class TestPredicationsComparison:
    """Tests for comparison methods."""

    def test_gt_creates_greater_than(self, users):
        result = users['age'].gt(18)
        assert isinstance(result, GreaterThan)

    def test_gteq_creates_greater_than_or_equal(self, users):
        from arel.nodes.binary import GreaterThanOrEqual
        result = users['age'].gteq(18)
        assert isinstance(result, GreaterThanOrEqual)

    def test_lt_creates_less_than(self, users):
        from arel.nodes.binary import LessThan
        result = users['age'].lt(65)
        assert isinstance(result, LessThan)

    def test_lteq_creates_less_than_or_equal(self, users):
        from arel.nodes.binary import LessThanOrEqual
        result = users['age'].lteq(65)
        assert isinstance(result, LessThanOrEqual)


class TestPredicationsIn:
    """Tests for in/not_in methods."""

    def test_in_with_list(self, users):
        """Test in_() with list of values."""
        result = users['status'].in_(['active', 'pending'])

        assert isinstance(result, In)

    def test_in_with_subquery(self, users, posts):
        """Test in_() with SelectManager."""
        subquery = posts.project(posts['user_id']).where(posts['published'].eq(True))
        result = users['id'].in_(subquery)

        assert isinstance(result, In)
        # Right should be the subquery's AST


class TestPredicationsMatches:
    """Tests for matches/does_not_match methods."""

    def test_matches_creates_matches_node(self, users):
        result = users['name'].matches('%John%')

        assert isinstance(result, Matches)
        assert result.case_sensitive is False

    def test_matches_with_escape(self, users):
        result = users['name'].matches('%John\\%%', escape='\\')

        assert result.escape is not None

    def test_matches_case_sensitive(self, users):
        result = users['name'].matches('%John%', case_sensitive=True)

        assert result.case_sensitive is True


class TestPredicationsAnyAll:
    """Tests for *_any and *_all methods."""

    def test_eq_any_creates_or(self, users):
        """Test eq_any([1, 2, 3]) creates OR conditions."""
        result = users['id'].eq_any([1, 2, 3])

        assert isinstance(result, Grouping)
        assert isinstance(result.expr, Or)

    def test_eq_all_creates_and(self, users):
        """Test eq_all([1, 2, 3]) creates AND conditions."""
        result = users['id'].eq_all([1, 2, 3])

        assert isinstance(result, Grouping)
        assert isinstance(result.expr, And)
```

---

## Visitor Tests

### test_to_sql.py

```python
import pytest
from arel import Table
from arel.collectors import SQLString


class TestToSqlEquality:
    """Tests for Equality SQL generation."""

    def test_equality_with_value(self, users, visitor, connection):
        """Test users['name'].eq('John') generates correct SQL."""
        node = users['name'].eq('John')

        result = compile(node, visitor)

        assert result == '"users"."name" = \'John\''

    def test_equality_with_none(self, users, visitor):
        """Test eq(None) generates IS NULL."""
        node = users['deleted_at'].eq(None)

        result = compile(node, visitor)

        assert result == '"users"."deleted_at" IS NULL'

    def test_not_equal_with_none(self, users, visitor):
        """Test not_eq(None) generates IS NOT NULL."""
        node = users['deleted_at'].not_eq(None)

        result = compile(node, visitor)

        assert result == '"users"."deleted_at" IS NOT NULL'


class TestToSqlSelect:
    """Tests for SELECT SQL generation."""

    def test_simple_select(self, users, visitor):
        """Test simple SELECT *."""
        query = users.project('*')

        result = compile(query.ast, visitor)

        assert 'SELECT' in result
        assert 'FROM "users"' in result

    def test_select_with_columns(self, users, visitor):
        """Test SELECT specific columns."""
        query = users.project(users['name'], users['email'])

        result = compile(query.ast, visitor)

        assert '"users"."name"' in result
        assert '"users"."email"' in result

    def test_select_with_where(self, users, visitor):
        """Test SELECT with WHERE."""
        query = (users
            .project(users['name'])
            .where(users['active'].eq(True)))

        result = compile(query.ast, visitor)

        assert 'WHERE' in result
        assert '"users"."active" = TRUE' in result

    def test_select_with_order(self, users, visitor):
        """Test SELECT with ORDER BY."""
        query = (users
            .project(users['name'])
            .order(users['created_at'].desc()))

        result = compile(query.ast, visitor)

        assert 'ORDER BY' in result
        assert '"users"."created_at" DESC' in result

    def test_select_with_limit_offset(self, users, visitor):
        """Test SELECT with LIMIT and OFFSET."""
        query = (users
            .project(users['name'])
            .take(10)
            .skip(20))

        result = compile(query.ast, visitor)

        assert 'LIMIT 10' in result
        assert 'OFFSET 20' in result


class TestToSqlJoin:
    """Tests for JOIN SQL generation."""

    def test_inner_join(self, users, posts, visitor):
        """Test INNER JOIN."""
        query = (users
            .project(users['name'], posts['title'])
            .join(posts)
            .on(posts['user_id'].eq(users['id'])))

        result = compile(query.ast, visitor)

        assert 'INNER JOIN' in result
        assert 'ON' in result

    def test_outer_join(self, users, posts, visitor):
        """Test LEFT OUTER JOIN."""
        query = (users
            .project(users['name'])
            .outer_join(posts)
            .on(posts['user_id'].eq(users['id'])))

        result = compile(query.ast, visitor)

        assert 'LEFT OUTER JOIN' in result


class TestToSqlFunctions:
    """Tests for function SQL generation."""

    def test_count(self, users, visitor):
        """Test COUNT()."""
        query = users.project(users['id'].count())

        result = compile(query.ast, visitor)

        assert 'COUNT(' in result

    def test_count_distinct(self, users, visitor):
        """Test COUNT(DISTINCT ...)."""
        query = users.project(users['id'].count(True))

        result = compile(query.ast, visitor)

        assert 'COUNT(DISTINCT' in result

    def test_sum(self, users, visitor):
        """Test SUM()."""
        query = users.project(users['amount'].sum())

        result = compile(query.ast, visitor)

        assert 'SUM(' in result


def compile(node, visitor):
    collector = SQLString()
    return visitor.accept(node, collector).value
```

### test_postgresql.py

```python
import pytest


class TestPostgreSQLMatches:
    """Tests for PostgreSQL LIKE/ILIKE."""

    def test_case_insensitive_match_uses_ilike(self, users, pg_visitor):
        """Test case insensitive match uses ILIKE."""
        node = users['name'].matches('%john%')

        result = compile(node, pg_visitor)

        assert 'ILIKE' in result

    def test_case_sensitive_match_uses_like(self, users, pg_visitor):
        """Test case sensitive match uses LIKE."""
        node = users['name'].matches('%John%', case_sensitive=True)

        result = compile(node, pg_visitor)

        assert 'LIKE' in result
        assert 'ILIKE' not in result


class TestPostgreSQLBindParams:
    """Tests for PostgreSQL bind parameters."""

    def test_bind_params_use_dollar_notation(self, users, pg_visitor):
        """Test bind params use $1, $2, etc."""
        from arel.nodes.casted import BindParam
        from arel.collectors import SQLString

        # This would need actual bind param integration
        pass


class TestPostgreSQLDistinctOn:
    """Tests for PostgreSQL DISTINCT ON."""

    def test_distinct_on(self, users, pg_visitor):
        """Test DISTINCT ON generation."""
        query = (users
            .project(users['name'])
            .distinct_on(users['country']))

        result = compile(query.ast, pg_visitor)

        assert 'DISTINCT ON' in result


def compile(node, visitor):
    from arel.collectors import SQLString
    collector = SQLString()
    return visitor.accept(node, collector).value
```

---

## Integration Tests

### test_complex_queries.py

```python
import pytest
from arel import Table, sql


class TestComplexQueries:
    """Tests for complex real-world queries."""

    def test_multi_join_query(self, users, posts, comments, visitor):
        """Test query with multiple JOINs."""
        query = (users
            .project(users['name'], posts['title'], comments['body'])
            .join(posts).on(posts['user_id'].eq(users['id']))
            .join(comments).on(comments['post_id'].eq(posts['id']))
            .where(users['active'].eq(True))
            .order(posts['created_at'].desc())
            .take(10))

        result = compile(query.ast, visitor)

        # Should contain all tables
        assert '"users"' in result
        assert '"posts"' in result
        assert '"comments"' in result

        # Should have proper structure
        assert 'FROM "users"' in result
        assert 'INNER JOIN "posts"' in result
        assert 'INNER JOIN "comments"' in result

    def test_subquery_in_where(self, users, posts, visitor):
        """Test subquery in WHERE clause."""
        active_authors = (posts
            .project(posts['user_id'])
            .where(posts['published'].eq(True)))

        query = (users
            .project(users['name'])
            .where(users['id'].in_(active_authors)))

        result = compile(query.ast, visitor)

        # Should contain subquery
        assert 'SELECT' in result
        assert 'IN (' in result

    def test_cte_query(self, users, visitor):
        """Test CTE (WITH clause)."""
        active_users = (users
            .project(users['*'])
            .where(users['active'].eq(True))
            .as_('active_users'))

        query = (users.from_()
            .with_(active_users.to_cte())
            .project(sql('*'))
            .from_(Table('active_users')))

        result = compile(query.ast, visitor)

        assert 'WITH' in result
        assert 'active_users' in result

    def test_window_function_query(self, users, visitor):
        """Test window function."""
        query = (users
            .project(
                users['name'],
                users['salary'].sum().over(
                    users.window('dept_window')
                        .partition(users['department_id'])
                ).as_('dept_total')
            ))

        result = compile(query.ast, visitor)

        assert 'OVER' in result
        assert 'PARTITION BY' in result

    def test_case_when_query(self, users, visitor):
        """Test CASE WHEN."""
        status = (users['active']
            .when(True).then('Active')
            .when(False).then('Inactive')
            .else_('Unknown'))

        query = (users
            .project(users['name'], status.as_('status')))

        result = compile(query.ast, visitor)

        assert 'CASE' in result
        assert 'WHEN' in result
        assert 'THEN' in result
        assert 'ELSE' in result
        assert 'END' in result


def compile(node, visitor):
    from arel.collectors import SQLString
    collector = SQLString()
    return visitor.accept(node, collector).value
```

---

## Running Tests

```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov=arel --cov-report=html

# Specific file
pytest tests/test_select_manager.py

# Specific test
pytest tests/test_select_manager.py::TestSelectManager::test_where

# Verbose
pytest tests/ -v

# Stop on first failure
pytest tests/ -x
```

---

## CI/CD Configuration

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run tests
        run: |
          pytest tests/ --cov=arel --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```
