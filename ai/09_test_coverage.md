# Arel Tests Progress

Tracking implementation progress: Ruby → Python

- ✅ = Done
- ❌ = Not done

---

## attributes/attribute_test.rb

| Test | Ruby | Python |
|------|------|--------|
| can be constructed with a Union | ✅ | ✅ |
| can be constructed with a beginless range ending in -Infinity | ✅ | ✅ |
| can be constructed with a list | ✅ | ✅ |
| can be constructed with a quoted exclusive range starting from -Infinity | ✅ | ✅ |
| can be constructed with a quoted infinite range | ✅ | ✅ |
| can be constructed with a quoted range ending at Infinity | ✅ | ✅ |
| can be constructed with a quoted range starting from -Infinity | ✅ | ✅ |
| can be constructed with a random object | ✅ | ✅ |
| can be constructed with a range ending at Infinity | ✅ | ✅ |
| can be constructed with a range implicitly ending at Infinity | ✅ | ✅ |
| can be constructed with a range implicitly starting at Infinity | ✅ | ✅ |
| can be constructed with a range starting from -Infinity | ✅ | ✅ |
| can be constructed with a range where the begin and end are equal | ✅ | ✅ |
| can be constructed with a standard range | ✅ | ✅ |
| can be constructed with a subquery | ✅ | ✅ |
| can be constructed with an endless range starting from Infinity | ✅ | ✅ |
| can be constructed with an exclusive range | ✅ | ✅ |
| can be constructed with an exclusive range implicitly ending at Infinity | ✅ | ✅ |
| can be constructed with an exclusive range starting from -Infinity | ✅ | ✅ |
| can be constructed with an infinite range | ✅ | ✅ |
| does not type cast SqlLiteral nodes | ✅ | ✅ |
| does not type cast by default | ✅ | ✅ |
| should accept various data types. | ✅ | ✅ |
| should create a AVG node | ✅ | ✅ |
| should create a Contains node | ✅ | ✅ |
| should create a Descending node | ✅ | ✅ |
| should create a DoesNotMatch node | ✅ | ✅ |
| should create a GreaterThan node | ✅ | ✅ |
| should create a GreaterThanOrEqual node | ✅ | ✅ |
| should create a Grouping node | ✅ | ✅ |
| should create a LessThan node | ✅ | ✅ |
| should create a LessThanOrEqual node | ✅ | ✅ |
| should create a MAX node | ✅ | ✅ |
| should create a Matches node | ✅ | ✅ |
| should create a Min node | ✅ | ✅ |
| should create a NotEqual node | ✅ | ✅ |
| should create a SUM node | ✅ | ✅ |
| should create an Ascending node | ✅ | ✅ |
| should create an Overlaps node | ✅ | ✅ |
| should generate != in sql | ✅ | ✅ |
| should generate && in sql | ✅ | ✅ |
| should generate < in sql | ✅ | ✅ |
| should generate <= in sql | ✅ | ✅ |
| should generate = in sql | ✅ | ✅ |
| should generate > in sql | ✅ | ✅ |
| should generate >= in sql | ✅ | ✅ |
| should generate @> in sql | ✅ | ✅ |
| should generate ANDs in sql | ✅ | ✅ |
| should generate ASC in sql | ✅ | ✅ |
| should generate DESC in sql | ✅ | ✅ |
| should generate IN in sql | ✅ | ✅ |
| should generate LIKE in sql | ✅ | ✅ |
| should generate NOT IN in sql | ✅ | ✅ |
| should generate NOT LIKE in sql | ✅ | ✅ |
| should generate ORs in sql | ✅ | ✅ |
| should generate proper SQL | ✅ | ✅ |
| should generate the proper SQL | ✅ | ✅ |
| should handle comparing with a subquery | ✅ | ✅ |
| should handle nil | ✅ | ✅ |
| should not eat input | ✅ | ✅ |
| should produce sql | ✅ | ✅ |
| should return a count node | ✅ | ✅ |
| should return an equality node | ✅ | ✅ |
| should take a distinct param | ✅ | ✅ |
| type casts when given an explicit caster | ✅ | ✅ |

## attributes/math_test.rb

| Test | Ruby | Python |
|------|------|--------|
| attribute node should be compatible with & | ✅ | ✅ |
| attribute node should be compatible with * | ✅ | ✅ |
| attribute node should be compatible with + | ✅ | ✅ |
| attribute node should be compatible with - | ✅ | ✅ |
| attribute node should be compatible with / | ✅ | ✅ |
| attribute node should be compatible with << | ✅ | ✅ |
| attribute node should be compatible with >> | ✅ | ✅ |
| attribute node should be compatible with ^ | ✅ | ✅ |
| attribute node should be compatible with \| | ✅ | ✅ |
| average should be compatible with & | ✅ | ✅ |
| average should be compatible with * | ✅ | ✅ |
| average should be compatible with + | ✅ | ✅ |
| average should be compatible with - | ✅ | ✅ |
| average should be compatible with / | ✅ | ✅ |
| average should be compatible with << | ✅ | ✅ |
| average should be compatible with >> | ✅ | ✅ |
| average should be compatible with ^ | ✅ | ✅ |
| average should be compatible with \| | ✅ | ✅ |
| count should be compatible with & | ✅ | ✅ |
| count should be compatible with * | ✅ | ✅ |
| count should be compatible with + | ✅ | ✅ |
| count should be compatible with - | ✅ | ✅ |
| count should be compatible with / | ✅ | ✅ |
| count should be compatible with << | ✅ | ✅ |
| count should be compatible with >> | ✅ | ✅ |
| count should be compatible with ^ | ✅ | ✅ |
| count should be compatible with \| | ✅ | ✅ |
| maximum should be compatible with & | ✅ | ✅ |
| maximum should be compatible with * | ✅ | ✅ |
| maximum should be compatible with + | ✅ | ✅ |
| maximum should be compatible with - | ✅ | ✅ |
| maximum should be compatible with / | ✅ | ✅ |
| maximum should be compatible with << | ✅ | ✅ |
| maximum should be compatible with >> | ✅ | ✅ |
| maximum should be compatible with ^ | ✅ | ✅ |
| maximum should be compatible with \| | ✅ | ✅ |
| minimum should be compatible with & | ✅ | ✅ |
| minimum should be compatible with * | ✅ | ✅ |
| minimum should be compatible with + | ✅ | ✅ |
| minimum should be compatible with - | ✅ | ✅ |
| minimum should be compatible with / | ✅ | ✅ |
| minimum should be compatible with << | ✅ | ✅ |
| minimum should be compatible with >> | ✅ | ✅ |
| minimum should be compatible with ^ | ✅ | ✅ |
| minimum should be compatible with \| | ✅ | ✅ |

## attributes_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| responds to lower | ✅ | ✅ |

## collectors/bind_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test compile gathers all bind params | ✅ | ✅ |

## collectors/composite_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test composite collector performs multiple collections at once | ✅ | ✅ |
| test retryable on composite collector propagates | ✅ | ✅ |

## collectors/sql_string_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test compile | ✅ | ✅ |
| test returned sql uses utf8 encoding | ✅ | ✅ |

## collectors/substitute_bind_collector_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test compile | ✅ | ✅ |
| test quoting is delegated to quoter | ✅ | ✅ |

## crud_test.rb

| Test | Ruby | Python |
|------|------|--------|
| should call delete on the connection | ✅ | ✅ |
| should call insert on the connection | ✅ | ✅ |
| should call update on the connection | ✅ | ✅ |

## delete_manager_test.rb

| Test | Ruby | Python |
|------|------|--------|
| chains | ✅ | ✅ |
| handles limit properly | ✅ | ✅ |
| uses from | ✅ | ✅ |
| uses where values | ✅ | ✅ |

## factory_methods_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test cast | ✅ | ✅ |
| test coalesce | ✅ | ✅ |
| test create and | ✅ | ✅ |
| test create false | ✅ | ✅ |
| test create join | ✅ | ✅ |
| test create on | ✅ | ✅ |
| test create string join | ✅ | ✅ |
| test create table alias | ✅ | ✅ |
| test create true | ✅ | ✅ |
| test grouping | ✅ | ✅ |
| test lower | ✅ | ✅ |

## insert_manager_test.rb

| Test | Ruby | Python |
|------|------|--------|
| accepts a select query in place of a VALUES clause | ✅ | ✅ |
| accepts sql literals | ✅ | ✅ |
| allows sql literals | ✅ | ✅ |
| can create a ValuesList node | ✅ | ✅ |
| combines columns and values list in order | ✅ | ✅ |
| converts to sql | ✅ | ✅ |
| defaults the table | ✅ | ✅ |
| inserts false | ✅ | ✅ |
| inserts null | ✅ | ✅ |
| inserts time | ✅ | ✅ |
| is chainable | ✅ | ✅ |
| literals in multiple values are not escaped | ✅ | ✅ |
| noop for empty list | ✅ | ✅ |
| takes a Table and chains | ✅ | ✅ |
| takes a list of lists | ✅ | ✅ |
| works with multiple single values | ✅ | ✅ |
| works with multiple values | ✅ | ✅ |

## nodes/and_test.rb

| Test | Ruby | Python |
|------|------|--------|
| allows aliasing | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |

## nodes/as_test.rb

| Test | Ruby | Python |
|------|------|--------|
| converts right to SqlLiteral if a string | ✅ | ✅ |
| converts right to SqlLiteral if a symbol | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| makes an AS node | ✅ | ✅ |
| returns a Cte node using the LHS's name and the RHS as the relation | ✅ | ✅ |

## nodes/ascending_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test ascending? | ✅ | ✅ |
| test construct | ✅ | ✅ |
| test descending? | ✅ | ✅ |
| test direction | ✅ | ✅ |
| test equality with same ivars | ✅ | ✅ |
| test inequality with different ivars | ✅ | ✅ |
| test reverse | ✅ | ✅ |

## nodes/bin_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test default to sql | ✅ | ✅ |
| test equality with same ivars | ✅ | ✅ |
| test inequality with different ivars | ✅ | ✅ |
| test mysql to sql | ✅ | ✅ |
| test new | ✅ | ✅ |

## nodes/binary_test.rb

| Test | Ruby | Python |
|------|------|--------|
| generates a hash based on its value | ✅ | ✅ |
| generates a hash specific to its class | ✅ | ✅ |

## nodes/bind_param_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal to other bind params with the same value | ✅ | ✅ |
| is not equal to bind params with different values | ✅ | ✅ |
| is not equal to other nodes | ✅ | ✅ |

## nodes/bound_sql_literal_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal components | ✅ | ✅ |
| is not equal with different components | ✅ | ✅ |

## nodes/case_test.rb

| Test | Ruby | Python |
|------|------|--------|
| allows aliasing | ✅ | ✅ |
| clones case, conditions and default | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| sets case expression from first argument | ✅ | ✅ |
| sets default case from second argument | ✅ | ✅ |

## nodes/casted_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal when eql? returns true | ✅ | ✅ |

## nodes/comment_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal contents | ✅ | ✅ |
| is not equal with different contents | ✅ | ✅ |

## nodes/count_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| should alias the count | ✅ | ✅ |
| should compare the count | ✅ | ✅ |

## nodes/cte_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with unequal ivars | ✅ | ✅ |
| returns an Arel::Table using the Cte's name | ✅ | ✅ |
| returns self | ✅ | ✅ |

## nodes/delete_statement_test.rb

| Test | Ruby | Python |
|------|------|--------|
| clones wheres | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |

## nodes/descending_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test ascending? | ✅ | ✅ |
| test construct | ✅ | ✅ |
| test descending? | ✅ | ✅ |
| test direction | ✅ | ✅ |
| test equality with same ivars | ✅ | ✅ |
| test inequality with different ivars | ✅ | ✅ |
| test reverse | ✅ | ✅ |

## nodes/distinct_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal to other distinct nodes | ✅ | ✅ |
| is not equal with other nodes | ✅ | ✅ |

## nodes/equality_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| makes an OR node | ✅ | ✅ |
| makes and AND node | ✅ | ✅ |
| takes an engine | ✅ | ✅ |

## nodes/extract_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| should alias the extract | ✅ | ✅ |
| should extract field | ✅ | ✅ |
| should not mutate the extract | ✅ | ✅ |

## nodes/false_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal to other false nodes | ✅ | ✅ |
| is not equal with other nodes | ✅ | ✅ |

## nodes/filter_test.rb

| Test | Ruby | Python |
|------|------|--------|
| should add filter to expression | ✅ | ✅ |
| should alias the expression | ✅ | ✅ |
| should reference the window definition by name | ✅ | ✅ |

## nodes/fragments_test.rb

| Test | Ruby | Python |
|------|------|--------|
| can be joined with other nodes | ✅ | ✅ |
| fails if joined with something that is not an Arel node | ✅ | ✅ |
| is equal with equal values | ✅ | ✅ |
| is not equal with different values | ✅ | ✅ |

## nodes/grouping_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| should create Equality nodes | ✅ | ✅ |

## nodes/homogeneous_in_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test custom attribute node | ✅ | ✅ |
| test in | ✅ | ✅ |

## nodes/infix_operation_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test construct | ✅ | ✅ |
| test equality with same ivars | ✅ | ✅ |
| test inequality with different ivars | ✅ | ✅ |
| test operation alias | ✅ | ✅ |
| test operation ordering | ✅ | ✅ |

## nodes/insert_statement_test.rb

| Test | Ruby | Python |
|------|------|--------|
| clones columns and values | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |

## nodes/named_function_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test construct | ✅ | ✅ |
| test equality with same ivars | ✅ | ✅ |
| test inequality with different ivars | ✅ | ✅ |

## nodes/node_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test all nodes are nodes | ✅ | ✅ |
| test includes factory methods | ✅ | ✅ |

## nodes/not_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| makes a NOT node | ✅ | ✅ |

## nodes/or_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| makes an OR node | ✅ | ✅ |

## nodes/over_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| should alias the expression | ✅ | ✅ |
| should reference the window definition by name | ✅ | ✅ |
| should use definition in sub-expression | ✅ | ✅ |
| should use empty definition | ✅ | ✅ |

## nodes/select_core_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test clone | ✅ | ✅ |
| test equality with same ivars | ✅ | ✅ |
| test inequality with different ivars | ✅ | ✅ |
| test set quantifier | ✅ | ✅ |

## nodes/select_statement_test.rb

| Test | Ruby | Python |
|------|------|--------|
| clones cores | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |

## nodes/sql_literal_test.rb

| Test | Ruby | Python |
|------|------|--------|
| fails if joined with something that is not an Arel node | ✅ | ✅ |
| generates a Fragments node | ✅ | ✅ |
| is equal with equal contents | ✅ | ✅ |
| is not equal with different contents | ✅ | ✅ |
| makes a count node | ✅ | ✅ |
| makes a distinct node | ✅ | ✅ |
| makes a grouping node with an and node | ✅ | ✅ |
| makes a grouping node with an or node | ✅ | ✅ |
| makes a sql literal node | ✅ | ✅ |
| makes an equality node | ✅ | ✅ |
| serializes into YAML | ✅ | ✅ |

## nodes/sum_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| should alias the sum | ✅ | ✅ |
| should order the sum | ✅ | ✅ |

## nodes/table_alias_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| returns a Cte node using the TableAlias's name and relation | ✅ | ✅ |

## nodes/true_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal to other true nodes | ✅ | ✅ |
| is not equal with other nodes | ✅ | ✅ |

## nodes/unary_operation_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test construct | ✅ | ✅ |
| test equality with same ivars | ✅ | ✅ |
| test inequality with different ivars | ✅ | ✅ |
| test operation alias | ✅ | ✅ |
| test operation ordering | ✅ | ✅ |

## nodes/update_statement_test.rb

| Test | Ruby | Python |
|------|------|--------|
| clones wheres and values | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |

## nodes/window_test.rb

| Test | Ruby | Python |
|------|------|--------|
| is equal to other current row nodes | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| is not equal with other nodes | ✅ | ✅ |

## nodes_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test every arel nodes have hash eql eqeq from same class | ✅ | ✅ |

## select_manager_test.rb

| Test | Ruby | Python |
|------|------|--------|
| accepts symbols | ✅ | ✅ |
| accepts symbols as sql literals | ✅ | ✅ |
| adds a lock node | ✅ | ✅ |
| appends a comment to the generated query | ✅ | ✅ |
| can be aliased | ✅ | ✅ |
| can be empty | ✅ | ✅ |
| can have a non-table alias as relation name | ✅ | ✅ |
| can have multiple items specified separately | ✅ | ✅ |
| can make a subselect | ✅ | ✅ |
| can receive any node | ✅ | ✅ |
| chains | ✅ | ✅ |
| converts right to SqlLiteral if a string | ✅ | ✅ |
| converts strings to SQLLiterals | ✅ | ✅ |
| converts to sqlliterals | ✅ | ✅ |
| converts to sqlliterals with multiple items | ✅ | ✅ |
| copies from | ✅ | ✅ |
| copies limits | ✅ | ✅ |
| copies order | ✅ | ✅ |
| copies where | ✅ | ✅ |
| copies where clauses | ✅ | ✅ |
| copies where clauses when nesting is triggered | ✅ | ✅ |
| creates an update statement | ✅ | ✅ |
| creates new cores | ✅ | ✅ |
| generates order clauses | ✅ | ✅ |
| gives me back the where sql | ✅ | ✅ |
| handles database-specific statements | ✅ | ✅ |
| has order attributes | ✅ | ✅ |
| ignores strings when table of same name exists | ✅ | ✅ |
| joins itself | ✅ | ✅ |
| joins wheres with AND | ✅ | ✅ |
| knows take | ✅ | ✅ |
| knows where | ✅ | ✅ |
| makes an AS node by grouping the AST | ✅ | ✅ |
| makes sql | ✅ | ✅ |
| makes strings literals | ✅ | ✅ |
| makes updates to the correct copy | ✅ | ✅ |
| noops on nil | ✅ | ✅ |
| overwrites projections | ✅ | ✅ |
| raises EmptyJoinError on empty | ✅ | ✅ |
| reads projections | ✅ | ✅ |
| removes LIMIT when nil is passed | ✅ | ✅ |
| responds to join | ✅ | ✅ |
| returns inner join sql | ✅ | ✅ |
| returns nil when there are no wheres | ✅ | ✅ |
| returns order clauses | ✅ | ✅ |
| returns outer join sql | ✅ | ✅ |
| returns string join sql | ✅ | ✅ |
| returns the join source of the select core | ✅ | ✅ |
| sets the quantifier | ✅ | ✅ |
| should add an offset | ✅ | ✅ |
| should chain | ✅ | ✅ |
| should create an exists clause | ✅ | ✅ |
| should create and nodes | ✅ | ✅ |
| should create insert managers | ✅ | ✅ |
| should create join nodes | ✅ | ✅ |
| should create join nodes with a full outer join klass | ✅ | ✅ |
| should create join nodes with a right outer join klass | ✅ | ✅ |
| should create join nodes with an outer join klass | ✅ | ✅ |
| should except two managers | ✅ | ✅ |
| should hand back froms | ✅ | ✅ |
| should intersect two managers | ✅ | ✅ |
| should remove an offset | ✅ | ✅ |
| should return limit | ✅ | ✅ |
| should return the ast | ✅ | ✅ |
| should return the offset | ✅ | ✅ |
| should support WITH RECURSIVE | ✅ | ✅ |
| should support any ast | ✅ | ✅ |
| should support basic WITH | ✅ | ✅ |
| should union all | ✅ | ✅ |
| should union two managers | ✅ | ✅ |
| takes *args | ✅ | ✅ |
| takes a class | ✅ | ✅ |
| takes a partition | ✅ | ✅ |
| takes a partition and an order | ✅ | ✅ |
| takes a partition with multiple columns | ✅ | ✅ |
| takes a range frame, between two delimiters | ✅ | ✅ |
| takes a range frame, bounded following | ✅ | ✅ |
| takes a range frame, bounded preceding | ✅ | ✅ |
| takes a range frame, current row | ✅ | ✅ |
| takes a range frame, unbounded following | ✅ | ✅ |
| takes a range frame, unbounded preceding | ✅ | ✅ |
| takes a rows frame, between two delimiters | ✅ | ✅ |
| takes a rows frame, bounded following | ✅ | ✅ |
| takes a rows frame, bounded preceding | ✅ | ✅ |
| takes a rows frame, current row | ✅ | ✅ |
| takes a rows frame, unbounded following | ✅ | ✅ |
| takes a rows frame, unbounded preceding | ✅ | ✅ |
| takes a string | ✅ | ✅ |
| takes a symbol | ✅ | ✅ |
| takes an attribute | ✅ | ✅ |
| takes an order | ✅ | ✅ |
| takes an order with multiple columns | ✅ | ✅ |
| takes multiple args | ✅ | ✅ |
| takes sql literals | ✅ | ✅ |
| takes strings | ✅ | ✅ |
| takes the full outer join class | ✅ | ✅ |
| takes the right outer join class | ✅ | ✅ |
| takes three params | ✅ | ✅ |
| takes two params | ✅ | ✅ |
| test join sources | ✅ | ✅ |
| uses alias in sql | ✅ | ✅ |

## table_test.rb

| Test | Ruby | Python |
|------|------|--------|
| adds a having clause | ✅ | ✅ |
| can project | ✅ | ✅ |
| creates an outer join | ✅ | ✅ |
| ignores as if it equals name | ✅ | ✅ |
| is equal with equal ivars | ✅ | ✅ |
| is not equal with different ivars | ✅ | ✅ |
| manufactures an attribute if the symbol names an attribute within the relation | ✅ | ✅ |
| noops on nil | ✅ | ✅ |
| raises EmptyJoinError on empty | ✅ | ✅ |
| returns a tree manager | ✅ | ✅ |
| should accept Arel nodes | ✅ | ✅ |
| should accept a hash | ✅ | ✅ |
| should accept literal SQL | ✅ | ✅ |
| should add a limit | ✅ | ✅ |
| should add an offset | ✅ | ✅ |
| should create a group | ✅ | ✅ |
| should create a node that proxies to a table | ✅ | ✅ |
| should create join nodes | ✅ | ✅ |
| should create join nodes with a klass | ✅ | ✅ |
| should have a name | ✅ | ✅ |
| should take an order | ✅ | ✅ |
| takes a second argument for join type | ✅ | ✅ |
| takes multiple parameters | ✅ | ✅ |

## update_manager_test.rb

| Test | Ruby | Python |
|------|------|--------|
| adds columns to the AST when group value is a String | ✅ | ✅ |
| adds columns to the AST when group value is a Symbol | ✅ | ✅ |
| can be accessed | ✅ | ✅ |
| can be set | ✅ | ✅ |
| chains | ✅ | ✅ |
| generates a where clause | ✅ | ✅ |
| generates an update statement | ✅ | ✅ |
| generates an update statement with joins | ✅ | ✅ |
| handles limit properly | ✅ | ✅ |
| sets having | ✅ | ✅ |
| should not quote sql literals | ✅ | ✅ |
| takes a list of lists | ✅ | ✅ |
| takes a string | ✅ | ✅ |
| updates with null | ✅ | ✅ |

## visitors/dispatch_contamination_test.rb

| Test | Ruby | Python |
|------|------|--------|
| dispatches properly after failing upwards | ✅ | ✅ |
| is threadsafe when implementing superclass fallback | ✅ | ⏭️ (skipped - requires Ruby-specific mechanisms) |

## visitors/dot_test.rb

| Test | Ruby | Python |
|------|------|--------|
| test ActiveModel Attribute | ✅ | ⏭️ (skipped - requires ActiveModel) |
| test Arel Nodes And | ✅ | ✅ |
| test Arel Nodes As | ✅ | ✅ |
| test Arel Nodes Assignment | ✅ | ✅ |
| test Arel Nodes Avg | ✅ | ✅ |
| test Arel Nodes Between | ✅ | ✅ |
| test Arel Nodes BindParam | ✅ | ✅ |
| test Arel Nodes Case and friends | ✅ | ✅ |
| test Arel Nodes Casted | ✅ | ✅ |
| test Arel Nodes CurrentRow | ✅ | ✅ |
| test Arel Nodes DeleteStatement | ✅ | ✅ |
| test Arel Nodes Distinct | ✅ | ✅ |
| test Arel Nodes DoesNotMatch | ✅ | ✅ |
| test Arel Nodes Equality | ✅ | ✅ |
| test Arel Nodes Exists | ✅ | ✅ |
| test Arel Nodes GreaterThan | ✅ | ✅ |
| test Arel Nodes GreaterThanOrEqual | ✅ | ✅ |
| test Arel Nodes Group | ✅ | ✅ |
| test Arel Nodes Grouping | ✅ | ✅ |
| test Arel Nodes In | ✅ | ✅ |
| test Arel Nodes InfixOperation | ✅ | ✅ |
| test Arel Nodes InsertStatement | ✅ | ✅ |
| test Arel Nodes JoinSource | ✅ | ✅ |
| test Arel Nodes LessThan | ✅ | ✅ |
| test Arel Nodes LessThanOrEqual | ✅ | ✅ |
| test Arel Nodes Limit | ✅ | ✅ |
| test Arel Nodes Matches | ✅ | ✅ |
| test Arel Nodes Max | ✅ | ✅ |
| test Arel Nodes Min | ✅ | ✅ |
| test Arel Nodes Not | ✅ | ✅ |
| test Arel Nodes NotEqual | ✅ | ✅ |
| test Arel Nodes NotIn | ✅ | ✅ |
| test Arel Nodes NotRegExp | ✅ | ✅ |
| test Arel Nodes Offset | ✅ | ✅ |
| test Arel Nodes On | ✅ | ✅ |
| test Arel Nodes Or | ✅ | ✅ |
| test Arel Nodes Ordering | ✅ | ✅ |
| test Arel Nodes RegExp | ✅ | ✅ |
| test Arel Nodes SelectCore | ✅ | ✅ |
| test Arel Nodes SelectStatement | ✅ | ✅ |
| test Arel Nodes Sum | ✅ | ✅ |
| test Arel Nodes TableAlias | ✅ | ✅ |
| test Arel Nodes UnaryOperation | ✅ | ✅ |
| test Arel Nodes UnqualifiedColumn | ✅ | ✅ |
| test Arel Nodes UpdateStatement | ✅ | ✅ |
| test Arel Nodes ValuesList | ✅ | ✅ |
| test Arel Nodes With | ✅ | ✅ |
| test named function | ✅ | ✅ |

## visitors/mysql_test.rb

| Test | Ruby | Python |
|------|------|--------|
| allows a custom string to be used as a lock | ✅ | ✅ |
| can handle subqueries | ✅ | ✅ |
| concats a string | ✅ | ✅ |
| concats columns | ✅ | ✅ |
| defaults limit to 18446744073709551615 | ✅ | ✅ |
| defaults to FOR UPDATE when locking | ✅ | ✅ |
| ignores MATERIALIZED modifiers | ✅ | ✅ |
| ignores NOT MATERIALIZED modifiers | ✅ | ✅ |
| should construct a valid generic SQL statement | ✅ | ✅ |
| should escape LIMIT | ✅ | ✅ |
| should handle column names on both sides | ✅ | ✅ |
| should handle nil | ✅ | ✅ |
| should handle nulls first | ✅ | ✅ |
| should handle nulls first reversed | ✅ | ✅ |
| should handle nulls last | ✅ | ✅ |
| should handle nulls last reversed | ✅ | ✅ |
| should know how to visit | ✅ | ✅ |
| uses DUAL for empty from | ✅ | ✅ |

## visitors/postgres_test.rb

| Test | Ruby | Python |
|------|------|--------|
| allows a custom string to be used as a lock | ✅ | ✅ |
| can handle ESCAPE | ✅ | ✅ |
| can handle case insensitive | ✅ | ✅ |
| can handle subqueries | ✅ | ✅ |
| defaults to FOR UPDATE | ✅ | ✅ |
| encloses LATERAL queries in parens | ✅ | ✅ |
| increments each bind param | ✅ | ✅ |
| produces LATERAL queries with alias | ✅ | ✅ |
| should construct a valid generic SQL statement | ✅ | ✅ |
| should escape LIMIT | ✅ | ✅ |
| should handle Contains | ✅ | ✅ |
| should handle Overlaps | ✅ | ✅ |
| should handle column names on both sides | ✅ | ✅ |
| should handle nil | ✅ | ✅ |
| should know how to generate parenthesis when supplied with many Dimensions | ✅ | ✅ |
| should know how to visit | ✅ | ✅ |
| should know how to visit case sensitive | ✅ | ✅ |
| should know how to visit with CubeDimension Argument | ✅ | ✅ |
| should know how to visit with array arguments | ✅ | ✅ |
| should support DISTINCT | ✅ | ✅ |
| should support DISTINCT ON | ✅ | ✅ |

## visitors/sqlite_test.rb

| Test | Ruby | Python |
|------|------|--------|
| defaults limit to -1 | ✅ | ✅ |
| does not support locking | ✅ | ✅ |
| should construct a valid generic SQL statement | ✅ | ✅ |
| should handle column names on both sides | ✅ | ✅ |
| should handle nil | ✅ | ✅ |

## visitors/to_sql_test.rb

| Test | Ruby | Python |
|------|------|--------|
| allows chaining multiple conditions | ✅ | ✅ |
| can be built by adding SQL fragments one at a time | ✅ | ✅ |
| can be chained as a predicate | ✅ | ✅ |
| can define a dispatch method | ✅ | ✅ |
| can handle ESCAPE | ✅ | ✅ |
| can handle ranges bounded by infinity | ✅ | ✅ |
| can handle subqueries | ✅ | ✅ |
| can handle three dot ranges | ✅ | ✅ |
| can handle two dot ranges | ✅ | ✅ |
| does not quote BindParams used as part of a ValuesList | ✅ | ✅ |
| encloses SELECT statements with parentheses | ✅ | ✅ |
| handles CTEs with a MATERIALIZED modifier | ✅ | ✅ |
| handles CTEs with a NOT MATERIALIZED modifier | ✅ | ✅ |
| handles CTEs with no MATERIALIZED modifier | ✅ | ✅ |
| handles Cte nodes | ✅ | ✅ |
| handles table aliases | ✅ | ✅ |
| ignores excess named parameters | ✅ | ✅ |
| is not preparable when an array | ✅ | ✅ |
| is preparable when a subselect | ✅ | ✅ |
| joins subexpressions | ✅ | ✅ |
| quotes nested arrays | ✅ | ✅ |
| raises not implemented error | ✅ | ✅ |
| refuses mixed binds | ✅ | ✅ |
| requires all named bind params to be supplied | ✅ | ✅ |
| requires positional binds to match the placeholders | ✅ | ✅ |
| should apply Not to the whole expression | ✅ | ✅ |
| should chain predications on named functions | ✅ | ✅ |
| should compile Arel nodes | ✅ | ✅ |
| should compile literal SQL | ✅ | ✅ |
| should compile node names | ✅ | ✅ |
| should compile nodes with bind params | ✅ | ✅ |
| should construct a valid generic SQL statement | ✅ | ✅ |
| should contain a single space before ORDER BY | ✅ | ✅ |
| should escape LIMIT | ✅ | ✅ |
| should escape strings | ✅ | ✅ |
| should handle Addition | ✅ | ✅ |
| should handle BitwiseAnd | ✅ | ✅ |
| should handle BitwiseNot | ✅ | ✅ |
| should handle BitwiseOr | ✅ | ✅ |
| should handle BitwiseShiftLeft | ✅ | ✅ |
| should handle BitwiseShiftRight | ✅ | ✅ |
| should handle BitwiseXor | ✅ | ✅ |
| should handle Concatenation | ✅ | ✅ |
| should handle Contains | ✅ | ✅ |
| should handle Division | ✅ | ✅ |
| should handle Multiplication | ✅ | ✅ |
| should handle Overlaps | ✅ | ✅ |
| should handle Subtraction | ✅ | ✅ |
| should handle arbitrary operators | ✅ | ✅ |
| should handle column names on both sides | ✅ | ✅ |
| should handle false | ✅ | ✅ |
| should handle nil | ✅ | ✅ |
| should handle nil with named functions | ✅ | ✅ |
| should handle nulls first | ✅ | ✅ |
| should handle nulls first reversed | ✅ | ✅ |
| should handle nulls last | ✅ | ✅ |
| should handle nulls last reversed | ✅ | ✅ |
| should handle true | ✅ | ✅ |
| should know how to visit | ✅ | ✅ |
| should mark collector as non-retryable if SQL literal is not retryable | ✅ | ✅ |
| should mark collector as non-retryable when visiting SQL literal | ✅ | ✅ |
| should mark collector as non-retryable when visiting bound SQL literal | ✅ | ✅ |
| should mark collector as non-retryable when visiting delete statement node | ✅ | ✅ |
| should mark collector as non-retryable when visiting insert statement node | ✅ | ✅ |
| should mark collector as non-retryable when visiting named function | ✅ | ✅ |
| should mark collector as non-retryable when visiting update statement node | ✅ | ✅ |
| should not change retryable if SQL literal is marked as retryable | ✅ | ✅ |
| should not quote sql literals | ✅ | ✅ |
| should quote LIMIT without column type coercion | ✅ | ✅ |
| should return 1=0 when empty right which is always false | ✅ | ✅ |
| should return 1=1 when empty right which is always true | ✅ | ✅ |
| should use the underlying table for checking columns | ✅ | ✅ |
| should visit Arel Nodes And | ✅ | ✅ |
| should visit Arel Nodes Assignment | ✅ | ✅ |
| should visit Arel Nodes Or | ✅ | ✅ |
| should visit Arel SelectManager, which is a subquery | ✅ | ✅ |
| should visit As | ✅ | ✅ |
| should visit Class | ✅ | ✅ |
| should visit Date | ✅ | ✅ |
| should visit DateTime | ✅ | ✅ |
| should visit Float | ✅ | ✅ |
| should visit Hash | ✅ | ✅ |
| should visit Integer | ✅ | ✅ |
| should visit NilClass | ✅ | ✅ |
| should visit Not | ✅ | ✅ |
| should visit Set | ✅ | ✅ |
| should visit TrueClass | ✅ | ✅ |
| should visit built-in functions | ✅ | ✅ |
| should visit built-in functions operating on distinct values | ✅ | ✅ |
| should visit named functions | ✅ | ✅ |
| should visit string subclass | ✅ | ✅ |
| squashes parenthesis on multiple union alls | ✅ | ✅ |
| squashes parenthesis on multiple unions | ✅ | ✅ |
| supports #when with two arguments and no #then | ✅ | ✅ |
| supports extended case expressions | ✅ | ✅ |
| supports other bound literals as binds | ✅ | ✅ |
| supports simple case expressions | ✅ | ✅ |
| unsupported input should raise UnsupportedVisitError | ✅ | ✅ |
| will only consider named binds starting with a letter | ✅ | ✅ |
| works with BindParams | ✅ | ✅ |
| works with array values | ✅ | ✅ |
| works with lists | ✅ | ✅ |
| works with named binds | ✅ | ✅ |
| works with positional binds | ✅ | ✅ |
| works without default branch | ✅ | ✅ |
| wraps nested groupings in brackets only once | ✅ | ✅ |

---

## Summary

- **Total test files:** 59
- **Total tests:** 639
