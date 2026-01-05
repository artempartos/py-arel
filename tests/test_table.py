import pytest
from arel import Table, sql
from arel.nodes.sql_literal import SqlLiteral
from arel.nodes.joins import InnerJoin, FullOuterJoin, OuterJoin, RightOuterJoin
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestTable:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine
        self.relation = Table('users')

    def test_project(self):
        table = Table('users')
        query = table.project('*')
        must_be_like(query.to_sql(), 'SELECT * FROM "users"')

    def test_where(self):
        table = Table('users')
        query = table.project('*').where(table['id'].eq(1))
        must_be_like(query.to_sql(), 'SELECT * FROM "users" WHERE "users"."id" = 1')

    def test_order(self):
        table = Table('users')
        query = table.project('*').order(table['id'].desc())
        must_be_like(query.to_sql(), 'SELECT * FROM "users" ORDER BY "users"."id" DESC')

    def test_take_skip(self):
        table = Table('users')
        query = table.project('*').take(10).skip(20)
        must_be_like(query.to_sql(), 'SELECT * FROM "users" LIMIT 10 OFFSET 20')

    def test_should_create_join_nodes(self):
        join = self.relation.create_join("foo", "bar")
        assert isinstance(join, InnerJoin)
        assert join.left == "foo"
        assert join.right == "bar"

    def test_should_create_join_nodes_with_full_outer_join_klass(self):
        join = self.relation.create_join("foo", "bar", FullOuterJoin)
        assert isinstance(join, FullOuterJoin)
        assert join.left == "foo"
        assert join.right == "bar"

    def test_should_create_join_nodes_with_outer_join_klass(self):
        join = self.relation.create_join("foo", "bar", OuterJoin)
        assert isinstance(join, OuterJoin)
        assert join.left == "foo"
        assert join.right == "bar"

    def test_should_create_join_nodes_with_right_outer_join_klass(self):
        join = self.relation.create_join("foo", "bar", RightOuterJoin)
        assert isinstance(join, RightOuterJoin)
        assert join.left == "foo"
        assert join.right == "bar"

    def test_skip_should_add_an_offset(self):
        sm = self.relation.skip(2)
        must_be_like(sm.to_sql(), 'SELECT FROM "users" OFFSET 2')

    def test_having_adds_a_having_clause(self):
        mgr = self.relation.having(self.relation['id'].eq(10))
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" HAVING "users"."id" = 10')

    def test_join_noops_on_nil(self):
        mgr = self.relation.join(None)
        must_be_like(mgr.to_sql(), 'SELECT FROM "users"')

    def test_join_raises_empty_join_error_on_empty(self):
        from arel.errors import EmptyJoinError
        with pytest.raises(EmptyJoinError):
            self.relation.join("")

    def test_join_takes_a_second_argument_for_join_type(self):
        right = self.relation.alias()
        predicate = self.relation['id'].eq(right['id'])
        mgr = self.relation.join(right, OuterJoin).on(predicate)
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" LEFT OUTER JOIN "users" "users_2" ON "users"."id" = "users_2"."id"')

    def test_join_creates_an_outer_join(self):
        right = self.relation.alias()
        predicate = self.relation['id'].eq(right['id'])
        mgr = self.relation.outer_join(right).on(predicate)
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" LEFT OUTER JOIN "users" "users_2" ON "users"."id" = "users_2"."id"')

    def test_group_should_create_a_group(self):
        manager = self.relation.group(self.relation['id'])
        must_be_like(manager.to_sql(), 'SELECT FROM "users" GROUP BY "users"."id"')

    def test_alias_should_create_a_node_that_proxies_to_a_table(self):
        node = self.relation.alias()
        assert node.name == "users_2"
        assert node['id'].relation == node

    def test_new_should_accept_a_hash(self):
        rel = Table('users', as_="foo")
        assert rel.table_alias == "foo"

    def test_new_ignores_as_if_it_equals_name(self):
        rel = Table('users', as_="users")
        assert rel.table_alias is None

    def test_new_should_accept_literal_sql(self):
        rel = Table(sql("generate_series(4, 2)"))
        assert rel.name == sql("generate_series(4, 2)")

    def test_new_should_accept_arel_nodes(self):
        from arel.nodes.named_function import NamedFunction
        node = NamedFunction("generate_series", [4, 2])
        rel = Table(node)
        assert rel.name == node

    def test_order_should_take_an_order(self):
        manager = self.relation.order("foo")
        must_be_like(manager.to_sql(), 'SELECT FROM "users" ORDER BY foo')

    def test_take_should_add_a_limit(self):
        manager = self.relation.take(1)
        manager.project(SqlLiteral("*"))
        must_be_like(manager.to_sql(), 'SELECT * FROM "users" LIMIT 1')

    def test_project_can_project(self):
        manager = self.relation.project(SqlLiteral("*"))
        must_be_like(manager.to_sql(), 'SELECT * FROM "users"')

    def test_project_takes_multiple_parameters(self):
        manager = self.relation.project(SqlLiteral("*"), SqlLiteral("*"))
        must_be_like(manager.to_sql(), 'SELECT *, * FROM "users"')

    def test_where_returns_a_tree_manager(self):
        from arel.tree_manager import TreeManager
        manager = self.relation.where(self.relation['id'].eq(1))
        manager.project(self.relation['id'])
        assert isinstance(manager, TreeManager)
        must_be_like(manager.to_sql(), 'SELECT "users"."id" FROM "users" WHERE "users"."id" = 1')

    def test_should_have_a_name(self):
        assert self.relation.name == "users"

    def test_getitem_manufactures_an_attribute_if_the_symbol_names_an_attribute_within_the_relation(self):
        column = self.relation['id']
        assert column.name == "id"

    def test_equality_is_equal_with_equal_ivars(self):
        relation1 = Table('users', as_="zomg")
        relation2 = Table('users', as_="zomg")
        array = [relation1, relation2]
        assert len(set(array)) == 1

    def test_equality_is_not_equal_with_different_ivars(self):
        relation1 = Table('users', as_="zomg")
        relation2 = Table('users', as_="zomg2")
        array = [relation1, relation2]
        assert len(set(array)) == 2
