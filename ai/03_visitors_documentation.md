# Visitors and Collectors Documentation

## Visitors

### Arel::Visitors::Visitor

**File:** `arel/visitors/visitor.rb`

**Purpose:** Base class for all visitors. Implements Visitor pattern for AST traversal.

**How it works:**
1. Stores `@dispatch` - cache mapping class → method name
2. On `visit(object)` gets method name from cache
3. Calls method `visit_ClassName(object, collector)`
4. If method not found - searches through ancestor classes

**Key code:**
```ruby
def self.dispatch_cache
  @dispatch_cache ||= Hash.new do |hash, klass|
    hash[klass] = :"visit_#{(klass.name || '').gsub('::', '_')}"
  end.compare_by_identity
end

def visit(object, collector = nil)
  dispatch_method = dispatch[object.class]
  send dispatch_method, object, collector
rescue NoMethodError => e
  # Search through ancestors...
end
```

---

### Arel::Visitors::ToSql

**File:** `arel/visitors/to_sql.rb`

**Purpose:** Main AST → SQL compiler. Generates standard SQL.

**Attributes:**
- `@connection` - database connection (for quoting)

**Main visit methods:**

#### Statements
- `visit_Arel_Nodes_SelectStatement` - SELECT with WITH, ORDER BY, LIMIT, OFFSET, LOCK
- `visit_Arel_Nodes_SelectCore` - SELECT ... FROM ... WHERE ... GROUP BY ... HAVING
- `visit_Arel_Nodes_InsertStatement` - INSERT INTO ... VALUES
- `visit_Arel_Nodes_UpdateStatement` - UPDATE ... SET ... WHERE
- `visit_Arel_Nodes_DeleteStatement` - DELETE FROM ... WHERE

#### Operators
- `visit_Arel_Nodes_Equality` - `=` or `IS NULL`
- `visit_Arel_Nodes_NotEqual` - `!=` or `IS NOT NULL`
- `visit_Arel_Nodes_GreaterThan` / `LessThan` / `GreaterThanOrEqual` / `LessThanOrEqual`
- `visit_Arel_Nodes_Between` - BETWEEN
- `visit_Arel_Nodes_In` / `NotIn` - IN / NOT IN
- `visit_Arel_Nodes_Matches` / `DoesNotMatch` - LIKE / NOT LIKE
- `visit_Arel_Nodes_And` / `Or` - AND / OR
- `visit_Arel_Nodes_Not` - NOT
- `visit_Arel_Nodes_IsDistinctFrom` / `IsNotDistinctFrom`

#### JOINs
- `visit_Arel_Nodes_JoinSource` - FROM table JOINs
- `visit_Arel_Nodes_InnerJoin` - INNER JOIN
- `visit_Arel_Nodes_OuterJoin` - LEFT OUTER JOIN
- `visit_Arel_Nodes_FullOuterJoin` - FULL OUTER JOIN
- `visit_Arel_Nodes_RightOuterJoin` - RIGHT OUTER JOIN
- `visit_Arel_Nodes_StringJoin` - raw SQL
- `visit_Arel_Nodes_On` - ON condition

#### Functions
- `visit_Arel_Nodes_Count` - COUNT()
- `visit_Arel_Nodes_Sum` / `Max` / `Min` / `Avg` - aggregate functions
- `visit_Arel_Nodes_NamedFunction` - arbitrary function
- `visit_Arel_Nodes_Extract` - EXTRACT()
- `visit_Arel_Nodes_Exists` - EXISTS()

#### Window Functions
- `visit_Arel_Nodes_Window` - window (PARTITION BY, ORDER BY, FRAME)
- `visit_Arel_Nodes_NamedWindow` - name AS window
- `visit_Arel_Nodes_Over` - expr OVER window
- `visit_Arel_Nodes_Rows` / `Range` - ROWS / RANGE
- `visit_Arel_Nodes_Preceding` / `Following` - N PRECEDING/FOLLOWING
- `visit_Arel_Nodes_CurrentRow` - CURRENT ROW
- `visit_Arel_Nodes_Filter` - FILTER (WHERE ...)

#### CTEs
- `visit_Arel_Nodes_With` - WITH
- `visit_Arel_Nodes_WithRecursive` - WITH RECURSIVE
- `visit_Arel_Nodes_Cte` - name AS (query)

#### Set Operations
- `visit_Arel_Nodes_Union` - UNION
- `visit_Arel_Nodes_UnionAll` - UNION ALL
- `visit_Arel_Nodes_Intersect` - INTERSECT
- `visit_Arel_Nodes_Except` - EXCEPT

#### Values & Literals
- `visit_Arel_Nodes_Casted` / `Quoted` - quote value
- `visit_Arel_Nodes_True` / `False` - TRUE / FALSE
- `visit_Arel_Nodes_SqlLiteral` - raw SQL
- `visit_Arel_Nodes_BoundSqlLiteral` - SQL with bind parameters
- `visit_Arel_Nodes_BindParam` - bind parameter (?)
- `visit_Arel_Nodes_ValuesList` - VALUES (...)

#### Misc
- `visit_Arel_Nodes_TableAlias` - table alias
- `visit_Arel_Table` - table name
- `visit_Arel_Attributes_Attribute` - "table"."column"
- `visit_Arel_Nodes_UnqualifiedColumn` - column (without table)
- `visit_Arel_Nodes_Grouping` - (expr)
- `visit_Arel_Nodes_Ordering` / `Ascending` / `Descending` - ORDER BY
- `visit_Arel_Nodes_NullsFirst` / `NullsLast` - NULLS FIRST/LAST
- `visit_Arel_Nodes_Limit` / `Offset` - LIMIT / OFFSET
- `visit_Arel_Nodes_Lock` - FOR UPDATE
- `visit_Arel_Nodes_Distinct` - DISTINCT
- `visit_Arel_Nodes_Case` / `When` / `Else` - CASE WHEN
- `visit_Arel_Nodes_Assignment` - column = value (for UPDATE)
- `visit_Arel_Nodes_InfixOperation` - left op right
- `visit_Arel_Nodes_UnaryOperation` - op expr
- `visit_Arel_Nodes_Comment` - /* comment */
- `visit_Arel_Nodes_OptimizerHints` - /*+ hints */
- `visit_Arel_Nodes_Fragments` - SQL fragments
- `visit_Array` - comma-separated

**Helper methods:**
- `quote(value)` - quote value
- `quote_table_name(name)` - quote table name
- `quote_column_name(name)` - quote column name
- `maybe_visit(thing, collector)` - visit if not nil
- `inject_join(list, collector, join_str)` - join list with separator
- `collect_nodes_for(nodes, collector, spacer, connector)` - collect nodes
- `aggregate(name, o, collector)` - aggregate function
- `infix_value(o, collector, value)` - infix operation
- `infix_value_with_paren(o, collector, value)` - with parentheses handling for UNION
- `prepare_update_statement(o)` - prepare UPDATE (may create subquery)
- `build_subselect(key, o)` - build subquery for UPDATE/DELETE with LIMIT

**Unsupported types:**
Throws `UnsupportedVisitError` for:
- String, Symbol, Hash, NilClass
- Integer, Float, BigDecimal
- Date, DateTime, Time
- TrueClass, FalseClass
- Class

---

### Arel::Visitors::MySQL

**File:** `arel/visitors/mysql.rb`

**Purpose:** MySQL-specific compiler.

**Overrides:**

- `visit_Arel_Nodes_Bin` → `CAST(expr AS BINARY)`
- `visit_Arel_Nodes_UnqualifiedColumn` → doesn't qualify (MySQL allows)
- `visit_Arel_Nodes_SelectStatement` → adds huge LIMIT if OFFSET exists
- `visit_Arel_Nodes_SelectCore` → FROM DUAL if no table
- `visit_Arel_Nodes_Concat` → `CONCAT(left, right)` (instead of ||)
- `visit_Arel_Nodes_IsNotDistinctFrom` → `<=>`
- `visit_Arel_Nodes_IsDistinctFrom` → `NOT <=>`
- `visit_Arel_Nodes_Regexp` → `REGEXP`
- `visit_Arel_Nodes_NotRegexp` → `NOT REGEXP`
- `visit_Arel_Nodes_NullsFirst` → `expr IS NOT NULL, expr ASC/DESC`
- `visit_Arel_Nodes_NullsLast` → `expr IS NULL, expr ASC/DESC`
- `visit_Arel_Nodes_Cte` → without MATERIALIZED (not supported)

**prepare_update_statement:**
MySQL allows JOIN in UPDATE directly, but not with LIMIT/OFFSET/ORDER.

**build_subselect:**
MySQL requires sub-subquery due to optimizer_switch='derived_merge=on'.

---

### Arel::Visitors::PostgreSQL

**File:** `arel/visitors/postgresql.rb`

**Purpose:** PostgreSQL-specific compiler.

**Overrides:**

- `visit_Arel_Nodes_UpdateStatement` → UPDATE t1 SET ... FROM t2 WHERE (for JOINs)
- `visit_Arel_Nodes_Matches` → ILIKE for case insensitive
- `visit_Arel_Nodes_DoesNotMatch` → NOT ILIKE
- `visit_Arel_Nodes_Regexp` → `~` or `~*`
- `visit_Arel_Nodes_NotRegexp` → `!~` or `!~*`
- `visit_Arel_Nodes_DistinctOn` → `DISTINCT ON (expr)`
- `visit_Arel_Nodes_GroupingElement` → `(expr)` for CUBE/ROLLUP
- `visit_Arel_Nodes_Cube` → `CUBE(...)`
- `visit_Arel_Nodes_RollUp` → `ROLLUP(...)`
- `visit_Arel_Nodes_GroupingSet` → `GROUPING SETS(...)`
- `visit_Arel_Nodes_Lateral` → `LATERAL (query)`
- `visit_Arel_Nodes_InnerJoin` → `CROSS JOIN` if no ON
- `visit_Arel_Nodes_IsNotDistinctFrom` → `IS NOT DISTINCT FROM`
- `visit_Arel_Nodes_IsDistinctFrom` → `IS DISTINCT FROM`

**bind_block:** Returns `$1`, `$2` ... instead of `?`

**prepare_update_statement:**
PostgreSQL allows FROM for UPDATE. Creates table alias and self-join.

---

### Arel::Visitors::SQLite

**File:** `arel/visitors/sqlite.rb`

**Purpose:** SQLite-specific compiler.

**Overrides:**

- `visit_Arel_Nodes_UpdateStatement` → like PostgreSQL (FROM for JOINs)
- `visit_Arel_Nodes_TableAlias` → table AS alias (AS required)
- `visit_Arel_Nodes_Lock` → ignores (not supported)
- `visit_Arel_Nodes_SelectStatement` → LIMIT -1 if OFFSET without LIMIT
- `visit_Arel_Nodes_IsNotDistinctFrom` → `IS`
- `visit_Arel_Nodes_IsDistinctFrom` → `IS NOT`
- `infix_value_with_paren` → handles Grouping for UNION

---

### Arel::Visitors::Dot

**File:** `arel/visitors/dot.rb`

**Purpose:** AST visualization in DOT format (for Graphviz).

**Internal classes:**
- `Node` - graph node
- `Edge` - graph edge

**Attributes:**
- `@nodes` - all nodes
- `@edges` - all edges
- `@node_stack` - current nodes stack
- `@edge_stack` - current edges stack
- `@seen` - already visited objects

**Methods:**
- `visit_*` for each node type - adds edges for attributes
- `to_dot` - generates DOT string

**Output:**
```dot
digraph "Arel" {
node [width=0.375,height=0.25,shape=record];
123456 [label="<f0>Arel::Nodes::Equality"];
123456 -> 789012 [label="left"];
...
}
```

---

## Collectors

### Arel::Collectors::PlainString

**File:** `arel/collectors/plain_string.rb`

**Purpose:** Simple string collector.

**Attributes:**
- `@str` - collected string

**Methods:**
- `<<(str)` - add string
- `value` - get result

---

### Arel::Collectors::SQLString

**File:** `arel/collectors/sql_string.rb`

**Purpose:** SQL collector with bind parameter support.

**Inherits:** PlainString

**Attributes:**
- `@bind_index` - bind parameter counter
- `preparable` - whether prepared statement can be used
- `retryable` - whether query can be retried

**Methods:**
- `add_bind(bind, &block)` - add bind, call block to get placeholder
- `add_binds(binds, proc_for_binds, &block)` - add multiple binds

**Usage:**
```ruby
collector.add_bind(value) { |i| "?" }  # → "?"
collector.add_bind(value) { |i| "$#{i}" }  # → "$1"
```

---

### Arel::Collectors::Bind

**File:** `arel/collectors/bind.rb`

**Purpose:** Collects only bind values (without SQL).

**Attributes:**
- `@binds` - array of values

**Methods:**
- `<<(str)` - ignores strings
- `add_bind(bind)` - adds value to array
- `add_binds(binds, proc_for_binds)` - adds multiple values
- `value` - returns array of values

---

### Arel::Collectors::Composite

**File:** `arel/collectors/composite.rb`

**Purpose:** Combines two collectors for parallel collection.

**Attributes:**
- `@left`, `@right` - nested collectors
- `preparable`, `retryable`

**Methods:**
- All operations delegated to both collectors
- `value` → `[left.value, right.value]`

**Usage:**
```ruby
# Collect SQL and binds simultaneously
composite = Composite.new(SQLString.new, Bind.new)
visitor.accept(ast, composite)
sql, binds = composite.value
```

---

### Arel::Collectors::SubstituteBinds

**File:** `arel/collectors/substitute_binds.rb`

**Purpose:** Substitutes values instead of placeholders.

**Attributes:**
- `@quoter` - object for quoting
- `@delegate` - nested collector

**Methods:**
- `add_bind(bind)` - quotes and adds value
- `add_binds(binds)` - quotes all and adds

**Usage:**
```ruby
# SQL with substituted values (for logging)
sub = SubstituteBinds.new(connection, PlainString.new)
visitor.accept(ast, sub)
sql_with_values = sub.value
```
