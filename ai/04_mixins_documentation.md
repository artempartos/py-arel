# Mixins Documentation

## Arel::Predications

**File:** `arel/predications.rb`

**Purpose:** Methods for creating conditions (predicates). This is the most important mixin.

**Included in:**
- `Attribute`
- `NodeExpression`
- `SqlLiteral`
- `InfixOperation`

### Comparison Methods

```ruby
# Equality
eq(other)         # → Equality.new(self, quoted(other))
not_eq(other)     # → NotEqual.new(self, quoted(other))

# Comparison
gt(right)         # → GreaterThan.new(self, quoted(right))
gteq(right)       # → GreaterThanOrEqual.new(self, quoted(right))
lt(right)         # → LessThan.new(self, quoted(right))
lteq(right)       # → LessThanOrEqual.new(self, quoted(right))

# Distinct
is_distinct_from(other)       # → IsDistinctFrom
is_not_distinct_from(other)   # → IsNotDistinctFrom
```

### *_any / *_all Group Methods

```ruby
# *_any - OR between all conditions
eq_any(others)    # → Grouping(eq(o1) OR eq(o2) OR ...)
not_eq_any(others)
gt_any(others)
gteq_any(others)
lt_any(others)
lteq_any(others)
in_any(others)
not_in_any(others)
matches_any(others, escape, case_sensitive)
does_not_match_any(others, escape)

# *_all - AND between all conditions
eq_all(others)    # → Grouping(And(eq(o1), eq(o2), ...))
not_eq_all(others)
gt_all(others)
gteq_all(others)
lt_all(others)
lteq_all(others)
in_all(others)
not_in_all(others)
matches_all(others, escape, case_sensitive)
does_not_match_all(others, escape)
```

### IN / NOT IN

```ruby
in(other)
# If other is SelectManager → In.new(self, other.ast)
# If other is Enumerable → In.new(self, quoted_array(other))
# Otherwise → In.new(self, quoted(other))

not_in(other)
# Similarly
```

### BETWEEN

```ruby
between(range)
# Complex logic for handling Range:
# - Checks unboundable?, infinity?
# - For open-ended ranges generates gt/lt/gteq/lteq
# - For exclude_end? uses lt instead of lteq
# - For same begin/end → eq
# - Otherwise → Between.new(self, And([left, right]))

not_between(range)
# Reverse logic
```

### LIKE / Regexp

```ruby
matches(other, escape = nil, case_sensitive = false)
# → Matches.new(self, quoted(other), escape, case_sensitive)

does_not_match(other, escape = nil, case_sensitive = false)
# → DoesNotMatch.new(self, quoted(other), escape, case_sensitive)

matches_regexp(other, case_sensitive = true)
# → Regexp.new(self, quoted(other), case_sensitive)

does_not_match_regexp(other, case_sensitive = true)
# → NotRegexp.new(self, quoted(other), case_sensitive)
```

### CASE WHEN

```ruby
when(right)
# → Case.new(self).when(quoted(right))
```

### Others

```ruby
concat(other)     # → Concat.new(self, other) - for ||
contains(other)   # → Contains.new(self, quoted(other)) - for @>
overlaps(other)   # → Overlaps.new(self, quoted(other)) - for &&
```

### Helper Methods

```ruby
quoted_array(others)
# Converts array to array of quoted values

private:
grouping_any(method_id, others, *extras)
# Creates Grouping with Or of all conditions

grouping_all(method_id, others, *extras)
# Creates Grouping with And of all conditions

quoted_node(other)
# → Nodes.build_quoted(other, self)

infinity?(value)
# value.respond_to?(:infinite?) && value.infinite?

unboundable?(value)
# value.respond_to?(:unboundable?) && value.unboundable?

open_ended?(value)
# value.nil? || infinity?(value) || unboundable?(value)
```

---

## Arel::Expressions

**File:** `arel/expressions.rb`

**Purpose:** Aggregate functions.

**Included in:**
- `Attribute`
- `NodeExpression`
- `SqlLiteral`
- `InfixOperation`

### Methods

```ruby
count(distinct = false)   # → Count.new([self], distinct)
sum                       # → Sum.new([self])
maximum                   # → Max.new([self])
minimum                   # → Min.new([self])
average                   # → Avg.new([self])
extract(field)            # → Extract.new([self], field)
```

---

## Arel::Math

**File:** `arel/math.rb`

**Purpose:** Arithmetic and bitwise operations.

**Included in:**
- `Attribute`
- `NodeExpression`
- `InfixOperation`

### Methods

```ruby
# Arithmetic
*(other)    # → Multiplication.new(self, other)
+(other)    # → Grouping(Addition.new(self, other))
-(other)    # → Grouping(Subtraction.new(self, other))
/(other)    # → Division.new(self, other)

# Bitwise operations
&(other)    # → Grouping(BitwiseAnd.new(self, other))
|(other)    # → Grouping(BitwiseOr.new(self, other))
^(other)    # → Grouping(BitwiseXor.new(self, other))
<<(other)   # → Grouping(BitwiseShiftLeft.new(self, other))
>>(other)   # → Grouping(BitwiseShiftRight.new(self, other))
~@          # → BitwiseNot.new(self) - unary ~
```

**Note:** `+`, `-` and bitwise operations are wrapped in `Grouping` for correct precedence.

---

## Arel::OrderPredications

**File:** `arel/order_predications.rb`

**Purpose:** Sorting methods.

**Included in:**
- `Attribute`
- `NodeExpression`
- `SqlLiteral`
- `InfixOperation`

### Methods

```ruby
asc     # → Ascending.new(self)
desc    # → Descending.new(self)
```

---

## Arel::AliasPredication

**File:** `arel/alias_predication.rb`

**Purpose:** Method for creating alias.

**Included in:**
- `Table`
- `Attribute`
- `NodeExpression`
- `SqlLiteral`
- `InfixOperation`
- `Over`
- `Filter`

### Methods

```ruby
as(other)
# other = other.name if other.is_a?(Symbol)
# → As.new(self, SqlLiteral.new(other, retryable: true))
```

---

## Arel::WindowPredications

**File:** `arel/window_predications.rb`

**Purpose:** Method for window functions.

**Included in:**
- `Function`
- `Filter`

### Methods

```ruby
over(expr = nil)
# → Over.new(self, expr)
# expr can be Window, window name or nil
```

---

## Arel::FilterPredications

**File:** `arel/filter_predications.rb`

**Purpose:** FILTER method for aggregate functions.

**Included in:**
- `Function`

### Methods

```ruby
filter(expr)
# → Filter.new(self, expr)
```

---

## Arel::FactoryMethods

**File:** `arel/factory_methods.rb`

**Purpose:** Factory methods for creating nodes.

**Included in:**
- `Node`
- `Table`
- `TreeManager`

### Methods

```ruby
create_true           # → True.new
create_false          # → False.new

create_table_alias(relation, name)
# → TableAlias.new(relation, name)

create_join(to, constraint = nil, klass = InnerJoin)
# → klass.new(to, constraint)

create_string_join(to)
# → create_join(to, nil, StringJoin)

create_and(clauses)
# → And.new(clauses)

create_on(expr)
# → On.new(expr)

grouping(expr)
# → Grouping.new(expr)

lower(column)
# → NamedFunction.new("LOWER", [build_quoted(column)])

coalesce(*exprs)
# → NamedFunction.new("COALESCE", exprs)

cast(name, type)
# → NamedFunction.new("CAST", [name.as(type)])
```

---

## Arel::Crud

**File:** `arel/crud.rb`

**Purpose:** Methods for creating INSERT/UPDATE/DELETE from SELECT.

**Included in:**
- `SelectManager`

### Methods

```ruby
compile_insert(values)
# Creates InsertManager and calls insert(values)

create_insert
# → InsertManager.new

compile_update(values, key = nil)
# Creates UpdateManager with:
# - set(values)
# - take(limit), offset(offset), order(*orders)
# - wheres = constraints
# - comment(comment)
# - key = key
# - groups, havings from current context

compile_delete(key = nil)
# Creates DeleteManager similarly
```
