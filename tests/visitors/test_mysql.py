import pytest
from arel import Table, sql
from arel.nodes.select_statement import SelectStatement
from arel.nodes.update_statement import UpdateStatement
from arel.nodes.unary import Offset, Limit, Lock
from arel.nodes import build_quoted
from arel.visitors.mysql import MySQL
from arel.collectors.sql_string import SQLString
from tests.python.helper import MockEngine, must_be_like

class TestMySQL:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(MySQL)
        Table.engine = self.engine
        self.visitor = self.engine.connection.visitor

    def compile(self, node):
        return self.visitor.accept(node, SQLString()).value

    def test_defaults_limit_to_18446744073709551615(self):
        stmt = SelectStatement()
        stmt.offset = Offset(1)
        sql_result = self.compile(stmt)
        # MySQL adds LIMIT 18446744073709551615 when there's OFFSET without LIMIT
        assert "LIMIT 18446744073709551615 OFFSET 1" in sql_result or sql_result == "SELECT FROM DUAL LIMIT 18446744073709551615 OFFSET 1"

    def test_should_escape_limit(self):
        sc = UpdateStatement()
        sc.relation = Table('users')
        sc.limit = Limit(build_quoted("omg"))
        sql_result = self.compile(sc)
        must_be_like(sql_result, "UPDATE \"users\" LIMIT 'omg'")

    def test_uses_dual_for_empty_from(self):
        stmt = SelectStatement()
        sql_result = self.compile(stmt)
        must_be_like(sql_result, "SELECT FROM DUAL")

    def test_defaults_to_for_update_when_locking(self):
        node = Lock(sql("FOR UPDATE"))
        sql_result = self.compile(node)
        must_be_like(sql_result, "FOR UPDATE")

    def test_allows_a_custom_string_to_be_used_as_a_lock(self):
        node = Lock(sql("LOCK IN SHARE MODE"))
        sql_result = self.compile(node)
        must_be_like(sql_result, "LOCK IN SHARE MODE")

    def test_concats_columns(self):
        table = Table('users')
        query = table['name'].concat(table['name'])
        sql_result = self.compile(query)
        must_be_like(sql_result, 'CONCAT("users"."name", "users"."name")')

    def test_concats_a_string(self):
        table = Table('users')
        query = table['name'].concat(build_quoted("abc"))
        sql_result = self.compile(query)
        must_be_like(sql_result, 'CONCAT("users"."name", \'abc\')')

    def test_is_not_distinct_from_should_construct_a_valid_generic_sql_statement(self):
        test = Table('users')['name'].is_not_distinct_from("Aaron Patterson")
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."name" <=> \'Aaron Patterson\'')

    def test_is_not_distinct_from_should_handle_column_names_on_both_sides(self):
        test = Table('users')['first_name'].is_not_distinct_from(Table('users')['last_name'])
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" <=> "users"."last_name"')

    def test_is_not_distinct_from_should_handle_nil(self):
        table = Table('users')
        val = build_quoted(None, table['active'])
        from arel.nodes.binary import IsNotDistinctFrom
        sql_result = self.compile(IsNotDistinctFrom(table['name'], val))
        must_be_like(sql_result, '"users"."name" <=> NULL')

    def test_is_distinct_from_should_handle_column_names_on_both_sides(self):
        test = Table('users')['first_name'].is_distinct_from(Table('users')['last_name'])
        sql_result = self.compile(test)
        must_be_like(sql_result, 'NOT "users"."first_name" <=> "users"."last_name"')

    def test_is_distinct_from_should_handle_nil(self):
        table = Table('users')
        val = build_quoted(None, table['active'])
        from arel.nodes.binary import IsDistinctFrom
        sql_result = self.compile(IsDistinctFrom(table['name'], val))
        must_be_like(sql_result, 'NOT "users"."name" <=> NULL')

    def test_regexp_should_know_how_to_visit(self):
        table = Table('users')
        node = table['name'].matches_regexp("foo.*")
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" REGEXP \'foo.*\'')

    def test_regexp_can_handle_subqueries(self):
        table = Table('users')
        attr = table['id']
        subquery = table.project('id').where(table['name'].matches_regexp("foo.*"))
        node = attr.in_(subquery)
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."id" IN (SELECT id FROM "users" WHERE "users"."name" REGEXP \'foo.*\')')

    def test_not_regexp_should_know_how_to_visit(self):
        table = Table('users')
        node = table['name'].does_not_match_regexp("foo.*")
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."name" NOT REGEXP \'foo.*\'')

    def test_not_regexp_can_handle_subqueries(self):
        table = Table('users')
        attr = table['id']
        subquery = table.project('id').where(table['name'].does_not_match_regexp("foo.*"))
        node = attr.in_(subquery)
        sql_result = self.compile(node)
        must_be_like(sql_result, '"users"."id" IN (SELECT id FROM "users" WHERE "users"."name" NOT REGEXP \'foo.*\')')

    def test_ordering_should_handle_nulls_first(self):
        test = Table('users')['first_name'].asc().nulls_first()
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" IS NOT NULL, "users"."first_name" ASC')

    def test_ordering_should_handle_nulls_last(self):
        test = Table('users')['first_name'].asc().nulls_last()
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" IS NULL, "users"."first_name" ASC')

    def test_ordering_should_handle_nulls_first_reversed(self):
        test = Table('users')['first_name'].asc().nulls_first().reverse()
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" IS NULL, "users"."first_name" DESC')

    def test_ordering_should_handle_nulls_last_reversed(self):
        test = Table('users')['first_name'].asc().nulls_last().reverse()
        sql_result = self.compile(test)
        must_be_like(sql_result, '"users"."first_name" IS NOT NULL, "users"."first_name" DESC')

    def test_cte_ignores_materialized_modifiers(self):
        from arel.nodes.cte import Cte
        from arel import star
        cte = Cte("foo", Table('bar').project(star()), materialized=True)
        sql_result = self.compile(cte)
        must_be_like(sql_result, '"foo" AS (SELECT * FROM "bar")')

    def test_cte_ignores_not_materialized_modifiers(self):
        from arel.nodes.cte import Cte
        from arel import star
        cte = Cte("foo", Table('bar').project(star()), materialized=False)
        sql_result = self.compile(cte)
        must_be_like(sql_result, '"foo" AS (SELECT * FROM "bar")')

