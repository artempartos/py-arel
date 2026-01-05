# AREL Classes Documentation

## Core Classes

---

## Arel::Table

**File:** `arel/table.rb`

**Purpose:** Represents a database table. Entry point for building queries.

**Attributes:**
- `name` - table name
- `table_alias` - table alias (AS)
- `@klass` - associated ActiveRecord class (optional)
- `@type_caster` - for type casting

**Key methods:**
- `[](name)` - get attribute (column) of table
- `alias(name)` - create table alias (TableAlias)
- `from` - create SelectManager for table
- `project(*columns)` - SELECT columns
- `where(condition)` - add WHERE condition
- `join(relation, klass)` - add JOIN
- `outer_join(relation)` - LEFT OUTER JOIN
- `group(*columns)` - GROUP BY
- `order(*expr)` - ORDER BY
- `take(amount)` - LIMIT
- `skip(amount)` - OFFSET
- `having(expr)` - HAVING

**Mixins:**
- `FactoryMethods` - factory methods
- `AliasPredication` - `as()` method

---

## Arel::TreeManager

**File:** `arel/tree_manager.rb`

**Purpose:** Base class for all query managers (Select, Insert, Update, Delete).

**Attributes:**
- `@ast` - root AST node

**Key methods:**
- `to_sql(engine)` - compile to SQL
- `to_dot` - AST visualization in DOT format

**Nested module StatementMethods:**
Common methods for UPDATE/DELETE:
- `take(limit)` - LIMIT
- `offset(offset)` - OFFSET
- `order(*expr)` - ORDER BY
- `key=` - primary key for subqueries
- `where(expr)` - add WHERE
- `wheres=` - set all WHERE conditions

---

## Arel::SelectManager

**File:** `arel/select_manager.rb`

**Purpose:** Builds SELECT queries.

**Attributes:**
- `@ast` - SelectStatement
- `@ctx` - current SelectCore (last in cores)

**Key methods:**
- `project(*projections)` - SELECT columns
- `from(table)` - FROM
- `where(expr)` - WHERE
- `join(relation, klass)` - JOIN
- `outer_join(relation)` - LEFT OUTER JOIN
- `on(*exprs)` - ON condition for last JOIN
- `group(*columns)` - GROUP BY
- `having(expr)` - HAVING
- `order(*expr)` - ORDER BY
- `take(limit)` - LIMIT
- `skip(amount)` - OFFSET
- `lock(locking)` - FOR UPDATE
- `distinct(value)` - DISTINCT
- `distinct_on(value)` - DISTINCT ON (PostgreSQL)
- `union(other)` - UNION
- `intersect(other)` - INTERSECT
- `except(other)` - EXCEPT
- `with(*subqueries)` - WITH (CTE)
- `lateral(table_name)` - LATERAL (PostgreSQL)
- `window(name)` - window function
- `exists` - EXISTS
- `as(other)` - subquery with alias
- `optimizer_hints(*hints)` - optimizer hints
- `comment(*values)` - SQL comment

**Mixins:**
- `Crud` - methods for INSERT/UPDATE/DELETE

---

## Arel::InsertManager

**File:** `arel/insert_manager.rb`

**Purpose:** Builds INSERT queries.

**Key methods:**
- `into(table)` - INSERT INTO
- `insert(fields)` - add values
- `columns` - list of columns
- `values=` - set VALUES
- `select(select)` - INSERT ... SELECT
- `create_values(values)` - create ValuesList
- `create_values_list(rows)` - create ValuesList for multiple rows

---

## Arel::UpdateManager

**File:** `arel/update_manager.rb`

**Purpose:** Builds UPDATE queries.

**Key methods:**
- `table(table)` - UPDATE table
- `set(values)` - SET column = value
- `where(expr)` - WHERE (inherited)
- `order(*expr)` - ORDER BY
- `take(limit)` - LIMIT
- `offset(offset)` - OFFSET
- `group(columns)` - for subqueries
- `having(expr)` - for subqueries
- `comment(value)` - comment

---

## Arel::DeleteManager

**File:** `arel/delete_manager.rb`

**Purpose:** Builds DELETE queries.

**Key methods:**
- `from(relation)` - DELETE FROM
- `where(expr)` - WHERE
- `order(*expr)` - ORDER BY
- `take(limit)` - LIMIT
- `offset(offset)` - OFFSET
- `group(columns)` - for subqueries
- `having(expr)` - for subqueries
- `comment(value)` - comment

---

## Arel::Attributes::Attribute

**File:** `arel/attributes/attribute.rb`

**Purpose:** Represents a table column.

**Inherits:** `Struct.new(:relation, :name)`

**Attributes:**
- `relation` - table that owns the column
- `name` - column name

**Mixins:**
- `Expressions` - aggregate functions
- `Predications` - conditions (eq, gt, lt...)
- `AliasPredication` - as() method
- `OrderPredications` - asc(), desc()
- `Math` - arithmetic

**Key methods:**
- `lower` - LOWER(column)
- `type_caster` - get type caster
- `type_cast_for_database(value)` - cast value to database type

---

# AST Nodes

---

## Arel::Nodes::Node

**File:** `arel/nodes/node.rb`

**Purpose:** Base class for all AST nodes.

**Mixins:**
- `FactoryMethods`

**Key methods:**
- `not` - wrap in NOT
- `or(right)` - combine with OR (in Grouping)
- `and(right)` - combine with AND
- `invert` - invert (NOT)
- `to_sql(engine)` - compile to SQL
- `fetch_attribute` - get Attribute if present
- `equality?` - is this an equality condition?

---

## Arel::Nodes::NodeExpression

**File:** `arel/nodes/node_expression.rb`

**Purpose:** Node with predicate and expression support.

**Inherits:** Node

**Mixins:**
- `Expressions` - aggregate functions
- `Predications` - conditions
- `AliasPredication` - as()
- `OrderPredications` - asc(), desc()
- `Math` - arithmetic

---

## Arel::Nodes::Binary

**File:** `arel/nodes/binary.rb`

**Purpose:** Node with two children (left, right).

**Attributes:**
- `left` - left operand
- `right` - right operand

**Derived classes:**
- `As` - AS (with to_cte())
- `Between` - BETWEEN
- `GreaterThan`, `GreaterThanOrEqual`
- `LessThan`, `LessThanOrEqual`
- `Equality`, `NotEqual`
- `In`, `NotIn`
- `IsDistinctFrom`, `IsNotDistinctFrom`
- `Join`, `InnerJoin`, `OuterJoin`, `FullOuterJoin`, `RightOuterJoin`
- `Assignment` - for SET in UPDATE
- `Union`, `UnionAll`, `Intersect`, `Except`

**Module FetchAttribute:**
Allows extracting Attribute from binary node.

---

## Arel::Nodes::Unary

**File:** `arel/nodes/unary.rb`

**Purpose:** Node with single child.

**Attributes:**
- `expr` (alias: `value`)

**Derived classes:**
- `Bin` - BINARY (MySQL)
- `Cube`, `RollUp`, `GroupingSet` - GROUP BY extensions
- `DistinctOn` - DISTINCT ON (PostgreSQL)
- `Group` - GROUP BY element
- `GroupingElement` - grouping element
- `Lateral` - LATERAL (PostgreSQL)
- `Limit` - LIMIT
- `Lock` - FOR UPDATE
- `Not` - NOT
- `Offset` - OFFSET
- `On` - ON condition for JOIN
- `OptimizerHints` - optimizer hints

---

## Arel::Nodes::Nary (And, Or)

**File:** `arel/nodes/nary.rb`

**Purpose:** Node with N children.

**Attributes:**
- `children` - array of child nodes
- `left` - first element (for compatibility)
- `right` - second element (for compatibility)

**Derived classes:**
- `And` - logical AND
- `Or` - logical OR

---

## Arel::Nodes::Grouping

**File:** `arel/nodes/grouping.rb`

**Purpose:** Grouping expression in parentheses.

**Inherits:** Unary

Overrides `fetch_attribute` to delegate to inner expression.

---

## Arel::Nodes::Terminal (Distinct)

**File:** `arel/nodes/terminal.rb`

**Purpose:** Terminal node without data.

**Derived classes:**
- `Distinct` - DISTINCT

---

## Arel::Nodes::True, False

**Files:** `arel/nodes/true.rb`, `arel/nodes/false.rb`

**Purpose:** TRUE and FALSE literals.

**Inherit:** NodeExpression

---

## Arel::Nodes::Ordering (Ascending, Descending)

**Files:** `arel/nodes/ordering.rb`, `arel/nodes/ascending.rb`, `arel/nodes/descending.rb`

**Purpose:** Sort direction.

**Inherits:** Unary

**Methods:**
- `reverse()` - change direction
- `direction` - :asc or :desc
- `ascending?`, `descending?`
- `nulls_first()`, `nulls_last()`

**Derived classes:**
- `Ascending` - ASC
- `Descending` - DESC
- `NullsFirst` - NULLS FIRST
- `NullsLast` - NULLS LAST

---

## Arel::Nodes::SelectStatement

**File:** `arel/nodes/select_statement.rb`

**Purpose:** Complete SELECT query.

**Attributes:**
- `cores` - array of SelectCore (for UNION)
- `orders` - ORDER BY
- `limit` - LIMIT
- `offset` - OFFSET
- `lock` - FOR UPDATE
- `with` - WITH (CTE)

---

## Arel::Nodes::SelectCore

**File:** `arel/nodes/select_core.rb`

**Purpose:** SELECT query core (without ORDER BY, LIMIT).

**Attributes:**
- `source` - JoinSource (FROM + JOINs)
- `projections` - SELECT columns
- `wheres` - WHERE conditions
- `groups` - GROUP BY
- `havings` - HAVING
- `windows` - WINDOW definitions
- `set_quantifier` - DISTINCT/ALL
- `optimizer_hints` - hints
- `comment` - comment

---

## Arel::Nodes::JoinSource

**File:** `arel/nodes/join_source.rb`

**Purpose:** Data source with JOINs.

**Inherits:** Binary

**Attributes:**
- `left` - main table
- `right` - array of JOINs

**Methods:**
- `empty?` - no table and no JOINs

---

## Arel::Nodes::InsertStatement

**File:** `arel/nodes/insert_statement.rb`

**Purpose:** INSERT query.

**Attributes:**
- `relation` - table
- `columns` - columns
- `values` - ValuesList or SqlLiteral
- `select` - for INSERT ... SELECT

---

## Arel::Nodes::UpdateStatement

**File:** `arel/nodes/update_statement.rb`

**Purpose:** UPDATE query.

**Attributes:**
- `relation` - table (can be JoinSource)
- `values` - array of Assignment
- `wheres` - WHERE conditions
- `orders` - ORDER BY
- `limit`, `offset`
- `groups`, `havings` - for subqueries
- `key` - primary key for subqueries
- `comment`

---

## Arel::Nodes::DeleteStatement

**File:** `arel/nodes/delete_statement.rb`

**Purpose:** DELETE query.

**Attributes:**
- Similar to UpdateStatement

---

## Arel::Nodes::SqlLiteral

**File:** `arel/nodes/sql_literal.rb`

**Purpose:** Raw SQL fragment.

**Inherits:** String (!)

**Attributes:**
- `retryable` - whether query can be retried

**Mixins:**
- `Expressions`, `Predications`, `AliasPredication`, `OrderPredications`

**Methods:**
- `+(other)` - concatenation with another Arel node → Fragments

---

## Arel::Nodes::BoundSqlLiteral

**File:** `arel/nodes/bound_sql_literal.rb`

**Purpose:** SQL literal with bind parameters.

**Attributes:**
- `sql_with_placeholders` - SQL with ? or :name
- `positional_binds` - positional parameters [val1, val2]
- `named_binds` - named parameters {name: val}

Checks bind correctness on creation.

---

## Arel::Nodes::Casted, Quoted

**File:** `arel/nodes/casted.rb`

**Purpose:** Wrappers for values.

### Casted
Value with type casting via attribute.

**Attributes:**
- `value` - original value
- `attribute` - Attribute for type casting

**Methods:**
- `value_for_database` - value cast to database type

### Quoted
Value without type casting.

**Inherits:** Unary

### Nodes.build_quoted(other, attribute)
Factory method for creating Casted/Quoted:
- If `other` is Node, Attribute, Table, SelectManager, SqlLiteral → return as is
- If attribute exists → Casted
- Otherwise → Quoted

---

## Arel::Nodes::BindParam

**File:** `arel/nodes/bind_param.rb`

**Purpose:** Bind parameter for prepared statements.

**Attributes:**
- `value` - ActiveModel::Attribute or value

**Methods:**
- `nil?` - is value nil?
- `value_before_type_cast` - value before type casting
- `infinite?` - infinity?
- `unboundable?` - cannot bind?

---

## Arel::Nodes::Function

**File:** `arel/nodes/function.rb`

**Purpose:** Base class for SQL functions.

**Attributes:**
- `expressions` - function arguments
- `distinct` - DISTINCT inside function

**Mixins:**
- `WindowPredications` - over()
- `FilterPredications` - filter()

**Derived classes:**
- `Sum`, `Exists`, `Max`, `Min`, `Avg`

---

## Arel::Nodes::Count

**File:** `arel/nodes/count.rb`

**Purpose:** COUNT() function.

**Inherits:** Function

Accepts `distinct` parameter in constructor.

---

## Arel::Nodes::NamedFunction

**File:** `arel/nodes/named_function.rb`

**Purpose:** Arbitrary named function.

**Attributes:**
- `name` - function name
- `expressions` - arguments (inherited)

---

## Arel::Nodes::Extract

**File:** `arel/nodes/extract.rb`

**Purpose:** EXTRACT(field FROM expr).

**Inherits:** Unary

**Attributes:**
- `expr` - date/time expression (inherited)
- `field` - field (year, month, day...)

---

## Arel::Nodes::Case

**File:** `arel/nodes/case.rb`

**Purpose:** CASE WHEN ... THEN ... ELSE ... END.

**Attributes:**
- `case` - optional expression for comparison
- `conditions` - array of When nodes
- `default` - Else node

**Methods (chaining):**
- `when(condition, expression)` - add WHEN
- `then(expression)` - add THEN to last WHEN
- `else(expression)` - set ELSE

**Helper classes:**
- `When` (Binary) - WHEN left THEN right
- `Else` (Unary) - ELSE expr

---

## Arel::Nodes::Window, NamedWindow

**File:** `arel/nodes/window.rb`

**Purpose:** Window functions.

### Window
**Attributes:**
- `orders` - ORDER BY inside window
- `partitions` - PARTITION BY
- `framing` - Rows or Range

**Methods:**
- `order(*expr)` - add ORDER BY
- `partition(*expr)` - add PARTITION BY
- `frame(expr)` - set frame
- `rows(expr)` - ROWS frame
- `range(expr)` - RANGE frame

### NamedWindow
Named window (WINDOW name AS ...).

**Additionally:**
- `Rows`, `Range` (Unary) - frame type
- `CurrentRow` (Node) - CURRENT ROW
- `Preceding`, `Following` (Unary) - N PRECEDING/FOLLOWING

---

## Arel::Nodes::Over

**File:** `arel/nodes/over.rb`

**Purpose:** expr OVER window.

**Inherits:** Binary

**Attributes:**
- `left` - expression (function)
- `right` - window or window name

---

## Arel::Nodes::InfixOperation

**File:** `arel/nodes/infix_operation.rb`

**Purpose:** Infix operation: left operator right.

**Inherits:** Binary

**Attributes:**
- `operator` - operator (:+, :-, :*, :/, etc)

**Mixins:**
- `Expressions`, `Predications`, `OrderPredications`, `AliasPredication`, `Math`

**Derived classes:**
- `Multiplication` (*), `Division` (/)
- `Addition` (+), `Subtraction` (-)
- `Concat` (||)
- `Contains` (@>), `Overlaps` (&&)
- `BitwiseAnd` (&), `BitwiseOr` (|), `BitwiseXor` (^)
- `BitwiseShiftLeft` (<<), `BitwiseShiftRight` (>>)

---

## Arel::Nodes::UnaryOperation

**File:** `arel/nodes/unary_operation.rb`

**Purpose:** Unary operation.

**Inherits:** Unary

**Attributes:**
- `operator` - operator

**Derived classes:**
- `BitwiseNot` (~)

---

## Arel::Nodes::Matches, DoesNotMatch

**File:** `arel/nodes/matches.rb`

**Purpose:** LIKE / NOT LIKE.

**Inherits:** Binary

**Attributes:**
- `escape` - ESCAPE character
- `case_sensitive` - case sensitivity

---

## Arel::Nodes::Regexp, NotRegexp

**File:** `arel/nodes/regexp.rb`

**Purpose:** Regular expressions (PostgreSQL: ~, MySQL: REGEXP).

**Inherits:** Binary

**Attributes:**
- `case_sensitive` - case sensitivity

---

## Arel::Nodes::In, NotIn

**File:** `arel/nodes/in.rb`

**Purpose:** IN / NOT IN.

**Inherits:** Binary

**Methods:**
- `equality?` → true for In
- `invert()` - convert In ↔ NotIn

---

## Arel::Nodes::HomogeneousIn

**File:** `arel/nodes/homogeneous_in.rb`

**Purpose:** Optimized IN for homogeneous values.

**Inherits:** Node (!)

**Attributes:**
- `values` - array of values
- `attribute` - attribute
- `type` - :in or :notin

**Methods:**
- `casted_values` - values after type casting
- `proc_for_binds` - proc for bind parameters

---

## Arel::Nodes::Equality

**File:** `arel/nodes/equality.rb`

**Purpose:** Equality condition (=).

**Inherits:** Binary

**Methods:**
- `equality?` → true
- `invert()` → NotEqual

---

## Arel::Nodes::TableAlias

**File:** `arel/nodes/table_alias.rb`

**Purpose:** Table alias (table AS alias).

**Inherits:** Binary

**Attributes:**
- `left` / `relation` - table
- `right` / `name` / `table_alias` - alias name

**Methods:**
- `[](name)` - get attribute
- `table_name` - original table name
- `to_cte` - convert to CTE
- Type casting methods (delegate to relation)

---

## Arel::Nodes::With, WithRecursive

**File:** `arel/nodes/with.rb`

**Purpose:** WITH (Common Table Expression).

**Inherits:** Unary

**Attributes:**
- `expr` / `children` - array of CTEs

---

## Arel::Nodes::Cte

**File:** `arel/nodes/cte.rb`

**Purpose:** Individual CTE: name AS (query).

**Inherits:** Binary

**Attributes:**
- `left` / `name` - CTE name
- `right` / `relation` - query
- `materialized` - MATERIALIZED / NOT MATERIALIZED

**Methods:**
- `to_cte` - return self
- `to_table` - create Table with CTE name

---

## Arel::Nodes::Join and derivatives

**Files:** `inner_join.rb`, `outer_join.rb`, `full_outer_join.rb`, `right_outer_join.rb`, `string_join.rb`, `leading_join.rb`

**Purpose:** JOIN nodes.

**Inherit:** Binary (Join)

**Attributes:**
- `left` - joined table
- `right` - ON condition

**Types:**
- `InnerJoin` - INNER JOIN
- `OuterJoin` - LEFT OUTER JOIN
- `FullOuterJoin` - FULL OUTER JOIN
- `RightOuterJoin` - RIGHT OUTER JOIN
- `StringJoin` - raw SQL join
- `LeadingJoin` - special join (inherits InnerJoin)

---

## Arel::Nodes::ValuesList

**File:** `arel/nodes/values_list.rb`

**Purpose:** VALUES (...), (...) for INSERT.

**Inherits:** Unary

**Attributes:**
- `expr` / `rows` - array of value arrays

---

## Arel::Nodes::Comment

**File:** `arel/nodes/comment.rb`

**Purpose:** SQL comment /* comment */.

**Attributes:**
- `values` - array of comment strings

---

## Arel::Nodes::Fragments

**File:** `arel/nodes/fragments.rb`

**Purpose:** Combination of multiple SQL fragments.

**Attributes:**
- `values` - array of nodes

**Methods:**
- `+(other)` - add node

---

## Arel::Nodes::UnqualifiedColumn

**File:** `arel/nodes/unqualified_column.rb`

**Purpose:** Column without table qualification (for SET in UPDATE).

**Inherits:** Unary

**Attributes:**
- `expr` / `attribute` - Attribute

**Methods:**
- `relation`, `column`, `name` - delegate to attribute

---

## Arel::Nodes::Filter

**File:** `arel/nodes/filter.rb`

**Purpose:** FILTER (WHERE ...) for aggregate functions.

**Inherits:** Binary

**Mixins:**
- `WindowPredications` - can apply OVER
- `AliasPredication` - can give alias
