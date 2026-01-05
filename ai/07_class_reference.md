# Complete AREL Class Reference

This is a complete list of all classes in AREL with brief descriptions.

## Managers

| Ruby class | Python class | Description |
|------------|--------------|-------------|
| `Arel::Table` | `Table` | Database table representation |
| `Arel::TreeManager` | `TreeManager` | Base class for managers |
| `Arel::SelectManager` | `SelectManager` | SELECT builder |
| `Arel::InsertManager` | `InsertManager` | INSERT builder |
| `Arel::UpdateManager` | `UpdateManager` | UPDATE builder |
| `Arel::DeleteManager` | `DeleteManager` | DELETE builder |

## Attributes

| Ruby class | Python class | Description |
|------------|--------------|-------------|
| `Arel::Attributes::Attribute` | `Attribute` | Table column |

## Base Nodes

| Ruby class | Python class | Description |
|------------|--------------|-------------|
| `Arel::Nodes::Node` | `Node` | Base AST node |
| `Arel::Nodes::NodeExpression` | `NodeExpression` | Node with predications |
| `Arel::Nodes::Binary` | `Binary` | Node with left/right |
| `Arel::Nodes::Unary` | `Unary` | Node with expr |
| `Arel::Nodes::Nary` | `Nary` | Node with children |

## Statement Nodes

| Ruby class | Python class | Description |
|------------|--------------|-------------|
| `Arel::Nodes::SelectStatement` | `SelectStatement` | SELECT query |
| `Arel::Nodes::SelectCore` | `SelectCore` | SELECT core (without ORDER BY) |
| `Arel::Nodes::InsertStatement` | `InsertStatement` | INSERT query |
| `Arel::Nodes::UpdateStatement` | `UpdateStatement` | UPDATE query |
| `Arel::Nodes::DeleteStatement` | `DeleteStatement` | DELETE query |

## Comparison Nodes (Binary)

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Equality` | `Equality` | Equality | `=` |
| `Arel::Nodes::NotEqual` | `NotEqual` | Inequality | `!=` |
| `Arel::Nodes::GreaterThan` | `GreaterThan` | Greater than | `>` |
| `Arel::Nodes::GreaterThanOrEqual` | `GreaterThanOrEqual` | Greater than or equal | `>=` |
| `Arel::Nodes::LessThan` | `LessThan` | Less than | `<` |
| `Arel::Nodes::LessThanOrEqual` | `LessThanOrEqual` | Less than or equal | `<=` |
| `Arel::Nodes::Between` | `Between` | Between | `BETWEEN` |
| `Arel::Nodes::In` | `In` | Membership | `IN` |
| `Arel::Nodes::NotIn` | `NotIn` | Not in | `NOT IN` |
| `Arel::Nodes::IsDistinctFrom` | `IsDistinctFrom` | Distinct | `IS DISTINCT FROM` |
| `Arel::Nodes::IsNotDistinctFrom` | `IsNotDistinctFrom` | Not distinct | `IS NOT DISTINCT FROM` |

## Pattern Matching Nodes (Binary)

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Matches` | `Matches` | Pattern match | `LIKE` |
| `Arel::Nodes::DoesNotMatch` | `DoesNotMatch` | Pattern mismatch | `NOT LIKE` |
| `Arel::Nodes::Regexp` | `Regexp` | Regular expression | `~` |
| `Arel::Nodes::NotRegexp` | `NotRegexp` | Doesn't match | `!~` |

## Logical Nodes

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::And` | `And` | Logical AND | `AND` |
| `Arel::Nodes::Or` | `Or` | Logical OR | `OR` |
| `Arel::Nodes::Not` | `Not` | Logical NOT | `NOT` |

## Unary Nodes

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Grouping` | `Grouping` | Parentheses grouping | `(...)` |
| `Arel::Nodes::Limit` | `Limit` | Limit | `LIMIT` |
| `Arel::Nodes::Offset` | `Offset` | Offset | `OFFSET` |
| `Arel::Nodes::Lock` | `Lock` | Lock | `FOR UPDATE` |
| `Arel::Nodes::On` | `On` | JOIN condition | `ON` |
| `Arel::Nodes::Group` | `Group` | Grouping | `GROUP BY` |
| `Arel::Nodes::Bin` | `Bin` | Binary (MySQL) | `BINARY` |
| `Arel::Nodes::Cube` | `Cube` | CUBE | `CUBE` |
| `Arel::Nodes::RollUp` | `RollUp` | ROLLUP | `ROLLUP` |
| `Arel::Nodes::GroupingSet` | `GroupingSet` | Grouping Sets | `GROUPING SETS` |
| `Arel::Nodes::GroupingElement` | `GroupingElement` | Grouping element | `()` |
| `Arel::Nodes::Lateral` | `Lateral` | Lateral (PostgreSQL) | `LATERAL` |
| `Arel::Nodes::DistinctOn` | `DistinctOn` | DISTINCT ON (PostgreSQL) | `DISTINCT ON` |
| `Arel::Nodes::OptimizerHints` | `OptimizerHints` | Optimizer hints | `/*+ ... */` |

## Terminal Nodes (no data)

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Distinct` | `Distinct` | Distinct | `DISTINCT` |
| `Arel::Nodes::True` | `True_` | True | `TRUE` |
| `Arel::Nodes::False` | `False_` | False | `FALSE` |

## Ordering Nodes (Unary)

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Ordering` | `Ordering` | Base ordering | - |
| `Arel::Nodes::Ascending` | `Ascending` | Ascending | `ASC` |
| `Arel::Nodes::Descending` | `Descending` | Descending | `DESC` |
| `Arel::Nodes::NullsFirst` | `NullsFirst` | NULLs first | `NULLS FIRST` |
| `Arel::Nodes::NullsLast` | `NullsLast` | NULLs last | `NULLS LAST` |

## Join Nodes (Binary)

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Join` | `Join` | Base JOIN | - |
| `Arel::Nodes::InnerJoin` | `InnerJoin` | Inner join | `INNER JOIN` |
| `Arel::Nodes::OuterJoin` | `OuterJoin` | Outer join | `LEFT OUTER JOIN` |
| `Arel::Nodes::FullOuterJoin` | `FullOuterJoin` | Full outer join | `FULL OUTER JOIN` |
| `Arel::Nodes::RightOuterJoin` | `RightOuterJoin` | Right outer join | `RIGHT OUTER JOIN` |
| `Arel::Nodes::StringJoin` | `StringJoin` | Raw SQL join | - |
| `Arel::Nodes::LeadingJoin` | `LeadingJoin` | Leading join | `INNER JOIN` |
| `Arel::Nodes::JoinSource` | `JoinSource` | Source with JOINs | - |

## Set Operations (Binary)

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Union` | `Union` | Union | `UNION` |
| `Arel::Nodes::UnionAll` | `UnionAll` | Union all | `UNION ALL` |
| `Arel::Nodes::Intersect` | `Intersect` | Intersection | `INTERSECT` |
| `Arel::Nodes::Except` | `Except` | Except | `EXCEPT` |

## Alias & CTE Nodes

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::As` | `As` | Alias | `AS` |
| `Arel::Nodes::TableAlias` | `TableAlias` | Table alias | `table AS alias` |
| `Arel::Nodes::With` | `With` | CTE | `WITH` |
| `Arel::Nodes::WithRecursive` | `WithRecursive` | Recursive CTE | `WITH RECURSIVE` |
| `Arel::Nodes::Cte` | `Cte` | Individual CTE | `name AS (query)` |

## Function Nodes

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Function` | `Function` | Base function | - |
| `Arel::Nodes::Count` | `Count` | Count | `COUNT()` |
| `Arel::Nodes::Sum` | `Sum` | Sum | `SUM()` |
| `Arel::Nodes::Max` | `Max` | Maximum | `MAX()` |
| `Arel::Nodes::Min` | `Min` | Minimum | `MIN()` |
| `Arel::Nodes::Avg` | `Avg` | Average | `AVG()` |
| `Arel::Nodes::Exists` | `Exists` | Exists | `EXISTS()` |
| `Arel::Nodes::NamedFunction` | `NamedFunction` | Named function | `func()` |
| `Arel::Nodes::Extract` | `Extract` | Extract | `EXTRACT()` |

## Window Nodes

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Window` | `Window` | Window function | `() | (PARTITION BY...) ` |
| `Arel::Nodes::NamedWindow` | `NamedWindow` | Named window | `name AS (...)` |
| `Arel::Nodes::Over` | `Over` | OVER | `expr OVER window` |
| `Arel::Nodes::Filter` | `Filter` | FILTER | `FILTER (WHERE ...)` |
| `Arel::Nodes::Rows` | `Rows` | Frame type | `ROWS` |
| `Arel::Nodes::Range` | `Range_` | Frame type | `RANGE` |
| `Arel::Nodes::Preceding` | `Preceding` | Preceding | `N PRECEDING` |
| `Arel::Nodes::Following` | `Following` | Following | `N FOLLOWING` |
| `Arel::Nodes::CurrentRow` | `CurrentRow` | Current row | `CURRENT ROW` |

## Case/When Nodes

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Case` | `Case` | CASE expression | `CASE WHEN ... END` |
| `Arel::Nodes::When` | `When` | WHEN condition | `WHEN ... THEN ...` |
| `Arel::Nodes::Else` | `Else` | ELSE part | `ELSE ...` |

## Arithmetic Nodes (InfixOperation)

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::InfixOperation` | `InfixOperation` | Infix operation | `left op right` |
| `Arel::Nodes::Multiplication` | `Multiplication` | Multiplication | `*` |
| `Arel::Nodes::Division` | `Division` | Division | `/` |
| `Arel::Nodes::Addition` | `Addition` | Addition | `+` |
| `Arel::Nodes::Subtraction` | `Subtraction` | Subtraction | `-` |
| `Arel::Nodes::Concat` | `Concat` | Concatenation | `\|\|` |
| `Arel::Nodes::Contains` | `Contains` | Contains (PostgreSQL) | `@>` |
| `Arel::Nodes::Overlaps` | `Overlaps` | Overlaps | `&&` |
| `Arel::Nodes::BitwiseAnd` | `BitwiseAnd` | Bitwise AND | `&` |
| `Arel::Nodes::BitwiseOr` | `BitwiseOr` | Bitwise OR | `\|` |
| `Arel::Nodes::BitwiseXor` | `BitwiseXor` | Bitwise XOR | `^` |
| `Arel::Nodes::BitwiseShiftLeft` | `BitwiseShiftLeft` | Left shift | `<<` |
| `Arel::Nodes::BitwiseShiftRight` | `BitwiseShiftRight` | Right shift | `>>` |

## Unary Operations

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::UnaryOperation` | `UnaryOperation` | Unary operation | `op expr` |
| `Arel::Nodes::BitwiseNot` | `BitwiseNot` | Bitwise NOT | `~` |

## Literal & Value Nodes

| Ruby class | Python class | Description |
|------------|--------------|-------------|
| `Arel::Nodes::SqlLiteral` | `SqlLiteral` | Raw SQL |
| `Arel::Nodes::BoundSqlLiteral` | `BoundSqlLiteral` | SQL with binds |
| `Arel::Nodes::Casted` | `Casted` | Value with type cast |
| `Arel::Nodes::Quoted` | `Quoted` | Value without type cast |
| `Arel::Nodes::BindParam` | `BindParam` | Bind parameter |

## Misc Nodes

| Ruby class | Python class | Description | SQL |
|------------|--------------|-------------|-----|
| `Arel::Nodes::Assignment` | `Assignment` | Assignment | `col = val` |
| `Arel::Nodes::UnqualifiedColumn` | `UnqualifiedColumn` | Column without table | `col` |
| `Arel::Nodes::ValuesList` | `ValuesList` | Values list | `VALUES (...)` |
| `Arel::Nodes::Comment` | `Comment` | Comment | `/* ... */` |
| `Arel::Nodes::Fragments` | `Fragments` | SQL fragments | - |
| `Arel::Nodes::HomogeneousIn` | `HomogeneousIn` | Optimized IN | `IN (...)` |

## Visitors

| Ruby class | Python class | Description |
|------------|--------------|-------------|
| `Arel::Visitors::Visitor` | `Visitor` | Base visitor |
| `Arel::Visitors::ToSql` | `ToSql` | SQL compiler |
| `Arel::Visitors::MySQL` | `MySQL` | MySQL specific |
| `Arel::Visitors::PostgreSQL` | `PostgreSQL` | PostgreSQL specific |
| `Arel::Visitors::SQLite` | `SQLite` | SQLite specific |
| `Arel::Visitors::Dot` | `Dot` | DOT visualization |

## Collectors

| Ruby class | Python class | Description |
|------------|--------------|-------------|
| `Arel::Collectors::PlainString` | `PlainString` | Simple string collector |
| `Arel::Collectors::SQLString` | `SQLString` | SQL with binds |
| `Arel::Collectors::Bind` | `Bind` | Binds only |
| `Arel::Collectors::Composite` | `Composite` | Two collectors |
| `Arel::Collectors::SubstituteBinds` | `SubstituteBinds` | Bind substitution |

## Mixins

| Ruby module | Python mixin | Description |
|-------------|--------------|-------------|
| `Arel::Predications` | `PredicationsMixin` | Conditions (eq, gt, in...) |
| `Arel::Expressions` | `ExpressionsMixin` | Aggregates (count, sum...) |
| `Arel::Math` | `MathMixin` | Arithmetic (+, -, *, /) |
| `Arel::OrderPredications` | `OrderPredicationsMixin` | Sorting (asc, desc) |
| `Arel::AliasPredication` | `AliasPredicationMixin` | Alias (as) |
| `Arel::WindowPredications` | `WindowPredicationsMixin` | Windows (over) |
| `Arel::FilterPredications` | `FilterPredicationsMixin` | Filter (filter) |
| `Arel::FactoryMethods` | `FactoryMethodsMixin` | Factory methods |
| `Arel::Crud` | `CrudMixin` | CREATE/UPDATE/DELETE |

## Errors

| Ruby class | Python class | Description |
|------------|--------------|-------------|
| `Arel::ArelError` | `ArelError` | Base error |
| `Arel::EmptyJoinError` | `EmptyJoinError` | Empty JOIN |
| `Arel::BindError` | `BindError` | Bind parameter error |
