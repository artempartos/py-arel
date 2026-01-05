import pytest
from arel import Table, sql
from arel.nodes.unary import Lock, DistinctOn, Limit
from arel.nodes.distinct import Distinct
from arel.nodes.select_statement import SelectStatement
from arel.nodes.select_core import SelectCore
from arel.nodes import build_quoted
from arel.visitors.postgresql import PostgreSQL
from arel.collectors.sql_string import SQLString
from tests.python.helper import MockEngine, must_be_like

class TestPostgreSQL:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(PostgreSQL)
        Table.engine = self.engine
        self.visitor = self.engine.connection.visitor
        self.table = Table('users')
        self.attr = self.table['id']

    def compile(self, node):
        return self.visitor.accept(node, SQLString()).value

    def test_defaults_to_for_update(self):
        sql_result = self.compile(Lock(sql("FOR UPDATE")))
        must_be_like(sql_result, "FOR UPDATE")

    def test_allows_a_custom_string_to_be_used_as_a_lock(self):
        node = Lock(sql("FOR SHARE"))
        sql_result = self.compile(node)
        must_be_like(sql_result, "FOR SHARE")

    def test_should_escape_limit(self):
        sc = SelectStatement()
        sc.limit = Limit(build_quoted("omg"))
        sc.cores[0].projections.append(sql("DISTINCT ON"))
        sc.orders.append(sql("xyz"))
        sql_result = self.compile(sc)
        assert "LIMIT 'omg'" in sql_result
        assert sql_result.count("LIMIT") == 1

    def test_should_support_distinct_on(self):
        core = SelectCore()
        core.set_quantifier = DistinctOn(sql("aaron"))
        sql_result = self.compile(core)
        assert "DISTINCT ON ( aaron )" in sql_result or "DISTINCT ON (aaron)" in sql_result

    def test_should_support_distinct(self):
        core = SelectCore()
        core.set_quantifier = Distinct()
        sql_result = self.compile(core)
        assert "DISTINCT" in sql_result

    def test_matches_should_know_how_to_visit(self):
        node = self.table['name'].matches("foo%")
        assert node.case_sensitive == False
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" ILIKE \'foo%\'')

    def test_matches_should_know_how_to_visit_case_sensitive(self):
        node = self.table['name'].matches("foo%", None, True)
        assert node.case_sensitive == True
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" LIKE \'foo%\'')

    def test_matches_can_handle_escape(self):
        node = self.table['name'].matches("foo!%", "!")
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" ILIKE \'foo!%\' ESCAPE \'!\'')

    def test_matches_can_handle_subqueries(self):
        subquery = self.table.project('id').where(self.table['name'].matches("foo%"))
        node = self.attr.in_(subquery)
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."id" IN (SELECT id FROM "users" WHERE "users"."name" ILIKE \'foo%\')')

    def test_does_not_match_should_know_how_to_visit(self):
        node = self.table['name'].does_not_match("foo%")
        assert node.case_sensitive == False
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" NOT ILIKE \'foo%\'')

    def test_does_not_match_should_know_how_to_visit_case_sensitive(self):
        node = self.table['name'].does_not_match("foo%", None, True)
        assert node.case_sensitive == True
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" NOT LIKE \'foo%\'')

    def test_does_not_match_can_handle_escape(self):
        node = self.table['name'].does_not_match("foo!%", "!")
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" NOT ILIKE \'foo!%\' ESCAPE \'!\'')

    def test_does_not_match_can_handle_subqueries(self):
        subquery = self.table.project('id').where(self.table['name'].does_not_match("foo%"))
        node = self.attr.in_(subquery)
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."id" IN (SELECT id FROM "users" WHERE "users"."name" NOT ILIKE \'foo%\')')

    def test_bind_param_increments_each_bind_param(self):
        from arel.nodes.bind_param import BindParam
        query = self.table['name'].eq(BindParam(1)).and_(self.table['id'].eq(BindParam(1)))
        sql_result = self.compile(query)
        must_be_like(sql_result, '"users"."name" = $1 AND "users"."id" = $2')

    def test_is_not_distinct_from_should_construct_a_valid_generic_sql_statement(self):
        test = Table('users')['name'].is_not_distinct_from("Aaron Patterson")
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."name" IS NOT DISTINCT FROM \'Aaron Patterson\'')

    def test_is_not_distinct_from_should_handle_column_names_on_both_sides(self):
        test = Table('users')['first_name'].is_not_distinct_from(Table('users')['last_name'])
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" IS NOT DISTINCT FROM "users"."last_name"')

    def test_is_not_distinct_from_should_handle_nil(self):
        from arel.nodes.binary import IsNotDistinctFrom
        val = build_quoted(None, self.table['active'])
        sql_result = self.compile(IsNotDistinctFrom(self.table['name'], val))
        must_be_like(sql_result, '"users"."name" IS NOT DISTINCT FROM NULL')

    def test_is_distinct_from_should_handle_column_names_on_both_sides(self):
        test = Table('users')['first_name'].is_distinct_from(Table('users')['last_name'])
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" IS DISTINCT FROM "users"."last_name"')

    def test_is_distinct_from_should_handle_nil(self):
        from arel.nodes.binary import IsDistinctFrom
        val = build_quoted(None, self.table['active'])
        sql_result = self.compile(IsDistinctFrom(self.table['name'], val))
        must_be_like(sql_result, '"users"."name" IS DISTINCT FROM NULL')

    def test_should_handle_contains(self):
        from arel.nodes.infix_operation import Contains
        inner = build_quoted('{"foo":"bar"}')
        outer = Table('products')['metadata']
        sql_result = self.compile(Contains(outer, inner))
        must_be_like(sql_result, '"products"."metadata" @> \'{"foo":"bar"}\'')

    def test_should_handle_overlaps(self):
        from arel.nodes.infix_operation import Overlaps
        column = Table('products')['tags']
        search = build_quoted("{foo,bar,baz}")
        sql_result = self.compile(Overlaps(column, search))
        must_be_like(sql_result, '"products"."tags" && \'{foo,bar,baz}\'')

    def test_encloses_lateral_queries_in_parens(self):
        subquery = self.table.project('id').where(self.table['name'].matches("foo%"))
        sql_result = self.compile(subquery.lateral())
        must_be_like(sql_result, "LATERAL (SELECT id FROM \"users\" WHERE \"users\".\"name\" ILIKE 'foo%')")

    def test_produces_lateral_queries_with_alias(self):
        subquery = self.table.project('id').where(self.table['name'].matches("foo%"))
        sql_result = self.compile(subquery.lateral("bar"))
        must_be_like(sql_result, "LATERAL (SELECT id FROM \"users\" WHERE \"users\".\"name\" ILIKE 'foo%') bar")

    def test_regexp_should_know_how_to_visit(self):
        node = self.table['name'].matches_regexp("foo.*")
        assert node.case_sensitive == True
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" ~ \'foo.*\'')

    def test_regexp_can_handle_case_insensitive(self):
        node = self.table['name'].matches_regexp("foo.*", False)
        assert node.case_sensitive == False
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" ~* \'foo.*\'')

    def test_regexp_can_handle_subqueries(self):
        subquery = self.table.project('id').where(self.table['name'].matches_regexp("foo.*"))
        node = self.attr.in_(subquery)
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."id" IN (SELECT id FROM "users" WHERE "users"."name" ~ \'foo.*\')')

    def test_not_regexp_should_know_how_to_visit(self):
        node = self.table['name'].does_not_match_regexp("foo.*")
        assert node.case_sensitive == True
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" !~ \'foo.*\'')

    def test_not_regexp_can_handle_case_insensitive(self):
        node = self.table['name'].does_not_match_regexp("foo.*", False)
        assert node.case_sensitive == False
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" !~* \'foo.*\'')

    def test_not_regexp_can_handle_subqueries(self):
        subquery = self.table.project('id').where(self.table['name'].does_not_match_regexp("foo.*"))
        node = self.attr.in_(subquery)
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."id" IN (SELECT id FROM "users" WHERE "users"."name" !~ \'foo.*\')')

    def test_cube_should_know_how_to_visit_with_array_arguments(self):
        from arel.nodes.unary import Cube
        node = Cube([self.table['name'], self.table['bool']])
        sql_result = self.compile(node)
        must_be_like(sql_result, 'CUBE( "users"."name", "users"."bool" )')

    def test_cube_should_know_how_to_visit_with_grouping_element_argument(self):
        from arel.nodes.unary import Cube, GroupingElement
        dimensions = GroupingElement([self.table['name'], self.table['bool']])
        node = Cube(dimensions)
        sql_result = self.compile(node)
        must_be_like(sql_result, 'CUBE( "users"."name", "users"."bool" )')

    def test_cube_should_know_how_to_generate_parenthesis_when_supplied_with_many_dimensions(self):
        from arel.nodes.unary import Cube, GroupingElement
        dim1 = GroupingElement(self.table['name'])
        dim2 = GroupingElement([self.table['bool'], self.table['created_at']])
        node = Cube([dim1, dim2])
        sql_result = self.compile(node)
        must_be_like(sql_result, 'CUBE( ( "users"."name" ), ( "users"."bool", "users"."created_at" ) )')

    def test_grouping_set_should_know_how_to_visit_with_array_arguments(self):
        from arel.nodes.unary import GroupingSet
        node = GroupingSet([self.table['name'], self.table['bool']])
        sql_result = self.compile(node)
        must_be_like(sql_result, 'GROUPING SETS( "users"."name", "users"."bool" )')

    def test_grouping_set_should_know_how_to_visit_with_grouping_element_argument(self):
        from arel.nodes.unary import GroupingSet, GroupingElement
        group = GroupingElement([self.table['name'], self.table['bool']])
        node = GroupingSet(group)
        sql_result = self.compile(node)
        must_be_like(sql_result, 'GROUPING SETS( "users"."name", "users"."bool" )')

    def test_grouping_set_should_know_how_to_generate_parenthesis_when_supplied_with_many_dimensions(self):
        from arel.nodes.unary import GroupingSet, GroupingElement
        group1 = GroupingElement(self.table['name'])
        group2 = GroupingElement([self.table['bool'], self.table['created_at']])
        node = GroupingSet([group1, group2])
        sql_result = self.compile(node)
        must_be_like(sql_result, 'GROUPING SETS( ( "users"."name" ), ( "users"."bool", "users"."created_at" ) )')

    def test_rollup_should_know_how_to_visit_with_array_arguments(self):
        from arel.nodes.unary import RollUp
        node = RollUp([self.table['name'], self.table['bool']])
        sql_result = self.compile(node)
        must_be_like(sql_result, 'ROLLUP( "users"."name", "users"."bool" )')

    def test_rollup_should_know_how_to_visit_with_grouping_element_argument(self):
        from arel.nodes.unary import RollUp, GroupingElement
        group = GroupingElement([self.table['name'], self.table['bool']])
        node = RollUp(group)
        sql_result = self.compile(node)
        must_be_like(sql_result, 'ROLLUP( "users"."name", "users"."bool" )')

    def test_rollup_should_know_how_to_generate_parenthesis_when_supplied_with_many_dimensions(self):
        from arel.nodes.unary import RollUp, GroupingElement
        group1 = GroupingElement(self.table['name'])
        group2 = GroupingElement([self.table['bool'], self.table['created_at']])
        node = RollUp([group1, group2])
        sql_result = self.compile(node)
        must_be_like(sql_result, 'ROLLUP( ( "users"."name" ), ( "users"."bool", "users"."created_at" ) )')

