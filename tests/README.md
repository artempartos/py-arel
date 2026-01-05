# Arel Test Porting Status (Ruby -> Python)

This project uses **pytest** for testing.
All tests are 1:1 ports of original Ruby Arel tests.

## How to run tests
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/python
```

## Test Status

### Nodes
- [x] **test_node.py** (original: `tests/arel/nodes/node_test.rb`)
    - [x] FactoryMethods presence
    - [x] Check that all nodes inherit from base Node
- [x] **test_binary.py** (original: `tests/arel/nodes/binary_test.rb`)
    - [x] Binary nodes hashing
    - [x] Object comparison (Equality)
- [x] **test_unary.py** (original: `tests/arel/nodes/not_test.rb` + others)
    - [x] Unary nodes comparison
- [x] **test_and.py** (original: `tests/arel/nodes/and_test.rb`)
    - [x] N-ary And comparison
    - [x] Aliases (as) for And nodes
- [x] **test_or.py** (original: `tests/arel/nodes/or_test.rb`)
    - [x] OR creation logic via `.or()`
    - [x] N-ary Or comparison
- [x] **test_terminal.py** (original: `tests/arel/nodes/true_test.rb`, `false_test.rb`, `distinct_test.rb`)
    - [x] True, False, Distinct nodes comparison
- [x] **test_equality.py** (original: `tests/arel/nodes/equality_test.rb`)
    - [x] OR/AND creation from Equality
    - [x] Object comparison
- [x] **test_sql_literal.py** (original: `tests/arel/nodes/sql_literal_test.rb`)
    - [x] `.count()` support
    - [x] `+` operator for Fragments
    - [x] `eq_any` / `eq_all` grouping
- [x] **test_case.py** (original: `tests/arel/nodes/case_test.rb`)
    - [x] Case/When/Else initialization
    - [x] Cloning (copy)
    - [x] Comparison and aliases
- [x] **test_insert_statement.py** (original: `tests/arel/nodes/insert_statement_test.rb`)
    - [x] Columns and values cloning
    - [x] Statements comparison
- [x] **test_select_core.py** (original: `tests/arel/nodes/select_core_test.rb`)
    - [x] All fields cloning (deep copy)
    - [x] DISTINCT generation in SQL
    - [x] Complex comparison with all fields (wheres, groups, windows...)
- [x] **test_select_statement.py** (original: `tests/arel/nodes/select_statement_test.rb`)
    - [x] Cores cloning
    - [x] Comparison with all modifiers (limit, offset, lock)

### Attributes
- [x] **test_attribute.py** (original: `tests/arel/attributes/attribute_test.rb`)
    - [x] Predicates: `not_eq`, `gt`, `eq`, `matches`
    - [x] `None` handling (IS NULL / IS NOT NULL)
    - [x] Any/All predicates (`eq_any`, `not_eq_all`)
    - [x] Aggregate functions (`average`, `sum`, `max`, `min`, `count`)

### Managers & Core
- [x] **test_table.py** (original: `tests/arel/table_test.rb`)
    - [x] Basic SELECT generation
    - [x] Method chaining `project().where().order().take()`
- [x] **test_select_manager.py** (original: `tests/arel/select_manager_test.rb`)
    - [x] Custom JoinSources
    - [x] String literals support in project/group
    - [x] Complex subqueries and statement aliases
    - [x] `HAVING` and `ON` logic
    - [x] `EXISTS` check

## Legend
- [x] - Test ported to pytest and passes successfully
- [ ] - Test planned for porting
