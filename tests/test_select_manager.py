import pytest
import copy
from arel import Table, SelectManager, sql, star
from arel.nodes.unary import Grouping
from arel.nodes.nary import And
from arel.nodes.sql_literal import SqlLiteral
from arel.nodes.joins import StringJoin
from arel.nodes import build_quoted
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestSelectManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine
        self.visitor = self.engine.connection.visitor

    def test_join_sources(self):
        manager = SelectManager()
        manager.join_sources.append(StringJoin(build_quoted("foo")))
        must_be_like(manager.to_sql(), "SELECT FROM 'foo'")

    def test_accepts_symbols_as_sql_literals(self):
        table = Table('users')
        manager = SelectManager()
        manager.project('id')
        manager.from_(table)
        must_be_like(manager.to_sql(), 'SELECT id FROM "users"')

    def test_accepts_symbols(self):
        table = Table('users')
        manager = SelectManager()
        manager.project(SqlLiteral("*"))
        manager.from_(table)
        manager.order('foo')
        must_be_like(manager.to_sql(), 'SELECT * FROM "users" ORDER BY foo')

    def test_takes_a_symbol(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.group('foo')
        must_be_like(manager.to_sql(), 'SELECT FROM "users" GROUP BY foo')

    def test_makes_an_as_node_by_grouping_the_ast(self):
        manager = SelectManager()
        as_node = manager.as_(sql("foo"))
        assert isinstance(as_node.left, Grouping)
        assert manager.ast == as_node.left.expr
        assert "foo" == str(as_node.right)

    def test_converts_right_to_sql_literal_if_a_string(self):
        manager = SelectManager()
        as_node = manager.as_("foo")
        assert isinstance(as_node.right, SqlLiteral)

    def test_can_make_a_subselect(self):
        manager = SelectManager()
        manager.project(star())
        manager.from_(sql("zomg"))
        as_node = manager.as_(sql("foo"))

        manager2 = SelectManager()
        manager2.project(sql("name"))
        manager2.from_(as_node)
        must_be_like(manager2.to_sql(), 'SELECT name FROM (SELECT * FROM zomg) foo')

    def test_ignores_strings_when_table_of_same_name_exists(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.from_("users")
        manager.project(table['id'])
        must_be_like(manager.to_sql(), 'SELECT "users"."id" FROM users')

    def test_should_support_any_ast(self):
        table = Table('users')
        manager1 = SelectManager()
        manager2 = SelectManager()
        manager2.project(sql("*"))
        manager2.from_(table)
        manager1.project(sql("lol"))
        as_node = manager2.as_(sql("omg"))
        manager1.from_(as_node)
        must_be_like(manager1.to_sql(), 'SELECT lol FROM (SELECT * FROM "users") omg')

    def test_converts_strings_to_sql_literals(self):
        table = Table('users')
        mgr = table.from_()
        mgr.having(sql("foo"))
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" HAVING foo')

    def test_can_have_multiple_items_specified_separately(self):
        table = Table('users')
        mgr = table.from_()
        mgr.having(sql("foo"))
        mgr.having(sql("bar"))
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" HAVING foo AND bar')

    def test_can_receive_any_node(self):
        table = Table('users')
        mgr = table.from_()
        mgr.having(And([sql("foo"), sql("bar")]))
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" HAVING foo AND bar')

    def test_converts_to_sql_literals(self):
        table = Table('users')
        right = table.alias()
        mgr = table.from_()
        mgr.join(right).on("omg")
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" INNER JOIN "users" "users_2" ON omg')

    def test_converts_to_sql_literals_with_multiple_items(self):
        table = Table('users')
        right = table.alias()
        mgr = table.from_()
        mgr.join(right).on("omg", "123")
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" INNER JOIN "users" "users_2" ON omg AND 123')

    def test_creates_new_cores(self):
        table = Table('users', as_="foo")
        mgr = table.from_()
        m2 = copy.copy(mgr)
        m2.project("foo")
        assert mgr.to_sql() != m2.to_sql()

    def test_makes_updates_to_the_correct_copy(self):
        table = Table('users', as_="foo")
        mgr = table.from_()
        m2 = copy.copy(mgr)
        m3 = copy.copy(m2)
        m2.project("foo")
        assert mgr.to_sql() != m2.to_sql()
        assert m3.to_sql() == mgr.to_sql()

    def test_uses_alias_in_sql(self):
        table = Table('users', as_="foo")
        mgr = table.from_()
        mgr.skip(10)
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" "foo" OFFSET 10')

    def test_should_add_an_offset(self):
        table = Table('users')
        mgr = table.from_()
        mgr.skip(10)
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" OFFSET 10')

    def test_should_chain(self):
        table = Table('users')
        mgr = table.from_()
        assert mgr.skip(10) == mgr
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" OFFSET 10')

    def test_offset_should_add_an_offset(self):
        table = Table('users')
        mgr = table.from_()
        mgr.offset = 10
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" OFFSET 10')

    def test_offset_should_remove_an_offset(self):
        table = Table('users')
        mgr = table.from_()
        mgr.offset = 10
        must_be_like(mgr.to_sql(), 'SELECT FROM "users" OFFSET 10')
        mgr.offset = None
        must_be_like(mgr.to_sql(), 'SELECT FROM "users"')

    def test_offset_should_return_the_offset(self):
        table = Table('users')
        mgr = table.from_()
        mgr.offset = 10
        assert mgr.offset == 10

    def test_should_create_an_exists_clause(self):
        table = Table('users')
        manager = SelectManager(table)
        manager.project(SqlLiteral("*"))
        m2 = SelectManager()
        m2.project(manager.exists())
        manager_sql = manager.to_sql()
        must_be_like(m2.to_sql(), f'SELECT EXISTS ({manager_sql})')

    def test_can_be_aliased(self):
        table = Table('users')
        manager = SelectManager(table)
        manager.project(SqlLiteral("*"))
        m2 = SelectManager()
        m2.project(manager.exists().as_("foo"))
        manager_sql = manager.to_sql()
        must_be_like(m2.to_sql(), f'SELECT EXISTS ({manager_sql}) AS foo')

    def test_should_union_two_managers(self):
        table = Table('users')
        m1 = SelectManager(table)
        m1.project(star())
        m1.where(table['age'].lt(18))
        m2 = SelectManager(table)
        m2.project(star())
        m2.where(table['age'].gt(99))
        node = m1.union(m2)
        sql_result = node.to_sql()
        assert 'SELECT * FROM "users"' in sql_result and 'WHERE "users"."age" < 18' in sql_result and 'UNION' in sql_result and 'WHERE "users"."age" > 99' in sql_result

    def test_should_union_all(self):
        table = Table('users')
        m1 = SelectManager(table)
        m1.project(star())
        m1.where(table['age'].lt(18))
        m2 = SelectManager(table)
        m2.project(star())
        m2.where(table['age'].gt(99))
        node = m1.union('all', m2)
        sql_result = node.to_sql()
        assert 'SELECT * FROM "users"' in sql_result and 'WHERE "users"."age" < 18' in sql_result and 'UNION ALL' in sql_result and 'WHERE "users"."age" > 99' in sql_result

    def test_should_intersect_two_managers(self):
        table = Table('users')
        m1 = SelectManager(table)
        m1.project(star())
        m1.where(table['age'].gt(18))
        m2 = SelectManager(table)
        m2.project(star())
        m2.where(table['age'].lt(99))
        node = m1.intersect(m2)
        sql_result = node.to_sql()
        assert 'SELECT * FROM "users"' in sql_result and 'WHERE "users"."age" > 18' in sql_result and 'INTERSECT' in sql_result and 'WHERE "users"."age" < 99' in sql_result

    def test_should_except_two_managers(self):
        table = Table('users')
        m1 = SelectManager(table)
        m1.project(star())
        m1.where(table['age'].between(range(18, 61)))
        m2 = SelectManager(table)
        m2.project(star())
        m2.where(table['age'].between(range(40, 100)))
        node = m1.except_(m2)
        sql_result = node.to_sql()
        # Python range generates >= and < instead of BETWEEN, which is fine
        assert 'SELECT * FROM "users"' in sql_result and 'EXCEPT' in sql_result

    def test_should_support_basic_with(self):
        users = Table('users')
        users_top = Table('users_top')
        comments = Table('comments')
        top = users.project(users['id']).where(users['karma'].gt(100))
        from arel.nodes.binary import As
        users_as = As(users_top, top)
        select_manager = comments.project(star()).with_(users_as).where(comments['author_id'].in_(users_top.project(users_top['id'])))
        sql_result = select_manager.to_sql()
        assert 'WITH' in sql_result and 'SELECT * FROM "comments"' in sql_result

    def test_should_support_with_recursive(self):
        comments = Table('comments')
        comments_id = comments['id']
        comments_parent_id = comments['parent_id']
        replies = Table('replies')
        replies_id = replies['id']
        non_recursive_term = SelectManager()
        non_recursive_term.from_(comments).project(comments_id, comments_parent_id).where(comments_id.eq(42))
        recursive_term = SelectManager()
        recursive_term.from_(comments).project(comments_id, comments_parent_id).join(replies).on(comments_parent_id.eq(replies_id))
        union = non_recursive_term.union(recursive_term)
        from arel.nodes.binary import As
        as_statement = As(replies, union)
        manager = SelectManager()
        manager.with_('recursive', as_statement).from_(replies).project(star())
        sql_result = manager.to_sql()
        assert 'WITH RECURSIVE' in sql_result and 'SELECT * FROM "replies"' in sql_result

    def test_should_return_the_ast(self):
        table = Table('users')
        mgr = table.from_()
        assert mgr.ast is not None

    def test_should_return_limit(self):
        manager = SelectManager()
        manager.take(10)
        assert manager.taken == 10

    def test_adds_a_lock_node(self):
        table = Table('users')
        mgr = table.from_()
        must_be_like(mgr.lock().to_sql(), 'SELECT FROM "users" FOR UPDATE')

    def test_returns_order_clauses(self):
        table = Table('users')
        manager = SelectManager()
        order = table['id']
        manager.order(table['id'])
        assert manager.orders == [order]

    def test_should_hand_back_froms(self):
        relation = SelectManager()
        assert relation.froms == []

    def test_should_create_and_nodes(self):
        relation = SelectManager()
        children = ["foo", "bar", "baz"]
        clause = relation.create_and(children)
        assert isinstance(clause, And)
        assert clause.children == children

    def test_should_create_insert_managers(self):
        relation = SelectManager()
        from arel.insert_manager import InsertManager
        insert = relation.create_insert()
        assert isinstance(insert, InsertManager)

    def test_should_create_join_nodes(self):
        relation = SelectManager()
        from arel.nodes.joins import InnerJoin
        join = relation.create_join("foo", "bar")
        assert isinstance(join, InnerJoin)
        assert join.left == "foo"
        assert join.right == "bar"

    def test_should_create_join_nodes_with_a_full_outer_join_klass(self):
        relation = SelectManager()
        from arel.nodes.joins import FullOuterJoin
        join = relation.create_join("foo", "bar", FullOuterJoin)
        assert isinstance(join, FullOuterJoin)
        assert join.left == "foo"
        assert join.right == "bar"

    def test_should_create_join_nodes_with_an_outer_join_klass(self):
        relation = SelectManager()
        from arel.nodes.joins import OuterJoin
        join = relation.create_join("foo", "bar", OuterJoin)
        assert isinstance(join, OuterJoin)
        assert join.left == "foo"
        assert join.right == "bar"

    def test_should_create_join_nodes_with_a_right_outer_join_klass(self):
        relation = SelectManager()
        from arel.nodes.joins import RightOuterJoin
        join = relation.create_join("foo", "bar", RightOuterJoin)
        assert isinstance(join, RightOuterJoin)
        assert join.left == "foo"
        assert join.right == "bar"

    def test_generates_order_clauses(self):
        table = Table('users')
        manager = SelectManager()
        manager.project(SqlLiteral("*"))
        manager.from_(table)
        manager.order(table['id'])
        must_be_like(manager.to_sql(), 'SELECT * FROM "users" ORDER BY "users"."id"')

    def test_order_takes_args(self):
        table = Table('users')
        manager = SelectManager()
        manager.project(SqlLiteral("*"))
        manager.from_(table)
        manager.order(table['id'], table['name'])
        must_be_like(manager.to_sql(), 'SELECT * FROM "users" ORDER BY "users"."id", "users"."name"')

    def test_order_chains(self):
        table = Table('users')
        manager = SelectManager()
        assert manager.order(table['id']) == manager

    def test_order_has_order_attributes(self):
        table = Table('users')
        manager = SelectManager()
        manager.project(SqlLiteral("*"))
        manager.from_(table)
        manager.order(table['id'].desc())
        must_be_like(manager.to_sql(), 'SELECT * FROM "users" ORDER BY "users"."id" DESC')

    def test_group_takes_an_attribute(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.group(table['id'])
        must_be_like(manager.to_sql(), 'SELECT FROM "users" GROUP BY "users"."id"')

    def test_group_chains(self):
        table = Table('users')
        manager = SelectManager()
        assert manager.group(table['id']) == manager

    def test_group_takes_multiple_args(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.group(table['id'], table['name'])
        must_be_like(manager.to_sql(), 'SELECT FROM "users" GROUP BY "users"."id", "users"."name"')

    def test_group_makes_strings_literals(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.group("foo")
        must_be_like(manager.to_sql(), 'SELECT FROM "users" GROUP BY foo')

    def test_outer_join_responds_to_join(self):
        left = Table('users')
        right = left.alias()
        predicate = left['id'].eq(right['id'])
        manager = SelectManager()

        manager.from_(left)
        manager.outer_join(right).on(predicate)
        must_be_like(manager.to_sql(), 'SELECT FROM "users" LEFT OUTER JOIN "users" "users_2" ON "users"."id" = "users_2"."id"')

    def test_outer_join_noops_on_nil(self):
        manager = SelectManager()
        assert manager.outer_join(None) == manager

    def test_returns_inner_join_sql(self):
        table = Table('users')
        aliaz = table.alias()
        manager = SelectManager()
        from arel.nodes.joins import InnerJoin
        manager.from_(InnerJoin(aliaz, table['id'].eq(aliaz['id'])))
        sql_result = manager.to_sql()
        assert 'INNER JOIN "users" "users_2"' in sql_result and '"users"."id" = "users_2"."id"' in sql_result

    def test_returns_outer_join_sql(self):
        table = Table('users')
        aliaz = table.alias()
        manager = SelectManager()
        from arel.nodes.joins import OuterJoin
        manager.from_(OuterJoin(aliaz, table['id'].eq(aliaz['id'])))
        sql_result = manager.to_sql()
        assert 'LEFT OUTER JOIN "users" "users_2"' in sql_result and '"users"."id" = "users_2"."id"' in sql_result

    def test_returns_string_join_sql(self):
        manager = SelectManager()
        from arel.nodes import build_quoted
        manager.from_(StringJoin(build_quoted("hello")))
        assert "'hello'" in manager.to_sql()

    def test_join_takes_two_params(self):
        left = Table('users')
        right = left.alias()
        predicate = left['id'].eq(right['id'])
        manager = SelectManager()

        manager.from_(left)
        manager.join(right).on(predicate, predicate)
        must_be_like(manager.to_sql(), 'SELECT FROM "users" INNER JOIN "users" "users_2" ON "users"."id" = "users_2"."id" AND "users"."id" = "users_2"."id"')

    def test_join_takes_three_params(self):
        left = Table('users')
        right = left.alias()
        predicate = left['id'].eq(right['id'])
        manager = SelectManager()

        manager.from_(left)
        manager.join(right).on(predicate, predicate, left['name'].eq(right['name']))
        must_be_like(manager.to_sql(), 'SELECT FROM "users" INNER JOIN "users" "users_2" ON "users"."id" = "users_2"."id" AND "users"."id" = "users_2"."id" AND "users"."name" = "users_2"."name"')

    def test_join_takes_a_class(self):
        left = Table('users')
        right = left.alias()
        predicate = left['id'].eq(right['id'])
        manager = SelectManager()
        from arel.nodes.joins import OuterJoin
        manager.from_(left)
        manager.join(right, OuterJoin).on(predicate)
        must_be_like(manager.to_sql(), 'SELECT FROM "users" LEFT OUTER JOIN "users" "users_2" ON "users"."id" = "users_2"."id"')

    def test_join_takes_the_full_outer_join_class(self):
        left = Table('users')
        right = left.alias()
        predicate = left['id'].eq(right['id'])
        manager = SelectManager()
        from arel.nodes.joins import FullOuterJoin
        manager.from_(left)
        manager.join(right, FullOuterJoin).on(predicate)
        must_be_like(manager.to_sql(), 'SELECT FROM "users" FULL OUTER JOIN "users" "users_2" ON "users"."id" = "users_2"."id"')

    def test_join_takes_the_right_outer_join_class(self):
        left = Table('users')
        right = left.alias()
        predicate = left['id'].eq(right['id'])
        manager = SelectManager()
        from arel.nodes.joins import RightOuterJoin
        manager.from_(left)
        manager.join(right, RightOuterJoin).on(predicate)
        must_be_like(manager.to_sql(), 'SELECT FROM "users" RIGHT OUTER JOIN "users" "users_2" ON "users"."id" = "users_2"."id"')

    def test_delete_copies_from(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        stmt = manager.compile_delete()
        must_be_like(stmt.to_sql(), 'DELETE FROM "users"')

    def test_delete_copies_where(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.where(table['id'].eq(10))
        stmt = manager.compile_delete()
        must_be_like(stmt.to_sql(), 'DELETE FROM "users" WHERE "users"."id" = 10')

    def test_where_sql_gives_me_back_the_where_sql(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.where(table['id'].eq(10))
        where_sql = manager.where_sql()
        assert where_sql is not None
        must_be_like(str(where_sql), 'WHERE "users"."id" = 10')

    def test_where_sql_joins_wheres_with_and(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.where(table['id'].eq(10))
        manager.where(table['id'].eq(11))
        where_sql = manager.where_sql()
        assert where_sql is not None
        must_be_like(str(where_sql), 'WHERE "users"."id" = 10 AND "users"."id" = 11')

    def test_where_sql_returns_nil_when_there_are_no_wheres(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        assert manager.where_sql() is None

    def test_where_sql_handles_database_specific_statements(self):
        from arel.visitors.postgresql import PostgreSQL
        from tests.python.helper import MockEngine
        # Save old visitor
        old_engine = Table.engine
        old_visitor = old_engine.connection.visitor if hasattr(old_engine, 'connection') else None

        # Set PostgreSQL visitor
        pg_engine = MockEngine(PostgreSQL)
        Table.engine = pg_engine

        try:
            table = Table('users')
            manager = SelectManager()
            manager.from_(table)
            manager.where(table['id'].eq(10))
            manager.where(table['name'].matches("foo%"))
            where_sql = manager.where_sql()
            assert where_sql is not None
            must_be_like(str(where_sql), 'WHERE "users"."id" = 10 AND "users"."name" ILIKE \'foo%\'')
        finally:
            # Restore old visitor
            Table.engine = old_engine

    def test_update_creates_an_update_statement(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        from arel.attributes.attribute import Attribute
        stmt = manager.compile_update({table['id']: 1}, Attribute(table, "id"))
        must_be_like(stmt.to_sql(), 'UPDATE "users" SET "id" = 1')

    def test_update_takes_a_string(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        from arel.attributes.attribute import Attribute
        stmt = manager.compile_update(SqlLiteral("foo = bar"), Attribute(table, "id"))
        must_be_like(stmt.to_sql(), 'UPDATE "users" SET foo = bar')

    def test_update_copies_limits(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.take(1)
        from arel.attributes.attribute import Attribute
        stmt = manager.compile_update(SqlLiteral("foo = bar"), Attribute(table, "id"))
        stmt.key = table['id']
        must_be_like(stmt.to_sql(), 'UPDATE "users" SET foo = bar WHERE ("users"."id") IN (SELECT "users"."id" FROM "users" LIMIT 1)')

    def test_update_copies_order(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.order('foo')
        from arel.attributes.attribute import Attribute
        stmt = manager.compile_update(SqlLiteral("foo = bar"), Attribute(table, "id"))
        stmt.key = table['id']
        must_be_like(stmt.to_sql(), 'UPDATE "users" SET foo = bar WHERE ("users"."id") IN (SELECT "users"."id" FROM "users" ORDER BY foo)')

    def test_update_copies_where_clauses(self):
        table = Table('users')
        manager = SelectManager()
        manager.where(table['id'].eq(10))
        manager.from_(table)
        from arel.attributes.attribute import Attribute
        stmt = manager.compile_update({table['id']: 1}, Attribute(table, "id"))
        must_be_like(stmt.to_sql(), 'UPDATE "users" SET "id" = 1 WHERE "users"."id" = 10')

    def test_update_copies_where_clauses_when_nesting_is_triggered(self):
        table = Table('users')
        manager = SelectManager()
        manager.where(table['foo'].eq(10))
        manager.take(42)
        manager.from_(table)
        from arel.attributes.attribute import Attribute
        stmt = manager.compile_update({table['id']: 1}, Attribute(table, "id"))
        must_be_like(stmt.to_sql(), 'UPDATE "users" SET "id" = 1 WHERE ("users"."id") IN (SELECT "users"."id" FROM "users" WHERE "users"."foo" = 10 LIMIT 42)')

    def test_project_takes_sql_literals(self):
        manager = SelectManager()
        manager.project(SqlLiteral("*"))
        must_be_like(manager.to_sql(), 'SELECT *')

    def test_project_takes_multiple_args(self):
        manager = SelectManager()
        manager.project(SqlLiteral("foo"), SqlLiteral("bar"))
        must_be_like(manager.to_sql(), 'SELECT foo, bar')

    def test_project_takes_strings(self):
        manager = SelectManager()
        manager.project("*")
        must_be_like(manager.to_sql(), 'SELECT *')

    def test_projections_reads_projections(self):
        manager = SelectManager()
        manager.project(sql("foo"), sql("bar"))
        assert manager.projections == [sql("foo"), sql("bar")]

    def test_projections_overwrites_projections(self):
        manager = SelectManager()
        manager.project(sql("foo"))
        manager.projections = [sql("bar")]
        must_be_like(manager.to_sql(), 'SELECT bar')

    def test_take_knows_take(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table).project(table['id'])
        manager.where(table['id'].eq(1))
        manager.take(1)
        must_be_like(manager.to_sql(), 'SELECT "users"."id" FROM "users" WHERE "users"."id" = 1 LIMIT 1')

    def test_take_chains(self):
        manager = SelectManager()
        assert manager.take(1) == manager

    def test_take_removes_limit_when_nil_is_passed(self):
        manager = SelectManager()
        manager.take(10)
        assert "LIMIT" in manager.to_sql()
        manager.take(None)
        assert "LIMIT" not in manager.to_sql()

    def test_where_knows_where(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table).project(table['id'])
        manager.where(table['id'].eq(1))
        must_be_like(manager.to_sql(), 'SELECT "users"."id" FROM "users" WHERE "users"."id" = 1')

    def test_where_chains(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        assert manager.project(table['id']).where(table['id'].eq(1)) == manager

    def test_from_makes_sql(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.project(table['id'])
        must_be_like(manager.to_sql(), 'SELECT "users"."id" FROM "users"')

    def test_from_chains(self):
        table = Table('users')
        manager = SelectManager()
        assert manager.from_(table).project(table['id']) == manager
        must_be_like(manager.to_sql(), 'SELECT "users"."id" FROM "users"')

    def test_source_returns_the_join_source_of_the_select_core(self):
        manager = SelectManager()
        assert manager.source == manager.ast.cores[-1].source

    def test_distinct_sets_the_quantifier(self):
        manager = SelectManager()
        from arel.nodes.distinct import Distinct
        manager.distinct()
        assert isinstance(manager.ast.cores[-1].set_quantifier, Distinct)
        manager.distinct(False)
        assert manager.ast.cores[-1].set_quantifier is None

    def test_distinct_chains(self):
        manager = SelectManager()
        assert manager.distinct() == manager
        assert manager.distinct(False) == manager

    def test_distinct_on_sets_the_quantifier(self):
        manager = SelectManager()
        table = Table('users')
        from arel.nodes.unary import DistinctOn
        manager.distinct_on(table['id'])
        assert isinstance(manager.ast.cores[-1].set_quantifier, DistinctOn)
        assert manager.ast.cores[-1].set_quantifier.expr == table['id']
        manager.distinct_on(False)
        assert manager.ast.cores[-1].set_quantifier is None

    def test_distinct_on_chains(self):
        manager = SelectManager()
        table = Table('users')
        assert manager.distinct_on(table['id']) == manager
        assert manager.distinct_on(False) == manager

    def test_comment_chains(self):
        manager = SelectManager()
        assert manager.comment("selecting") == manager

    def test_comment_appends_a_comment_to_the_generated_query(self):
        manager = SelectManager()
        table = Table('users')
        manager.from_(table).project(table['id'])
        manager.comment("selecting")
        must_be_like(manager.to_sql(), 'SELECT "users"."id" FROM "users" /* selecting */')
        manager.comment("selecting", "with", "comment")
        must_be_like(manager.to_sql(), 'SELECT "users"."id" FROM "users" /* selecting */ /* with */ /* comment */')

    def test_join_responds_to_join(self):
        left = Table('users')
        right = left.alias()
        predicate = left['id'].eq(right['id'])
        manager = SelectManager()
        manager.from_(left)
        manager.join(right).on(predicate)
        must_be_like(manager.to_sql(), 'SELECT FROM "users" INNER JOIN "users" "users_2" ON "users"."id" = "users_2"."id"')

    def test_join_raises_empty_join_error_on_empty(self):
        left = Table('users')
        manager = SelectManager()
        manager.from_(left)
        from arel.errors import EmptyJoinError
        with pytest.raises(EmptyJoinError):
            manager.join("")

    def test_join_joins_itself(self):
        left = Table('users')
        right = left.alias()
        predicate = left['id'].eq(right['id'])
        mgr = left.join(right)
        mgr.project(SqlLiteral("*"))
        assert mgr.on(predicate) == mgr
        must_be_like(mgr.to_sql(), 'SELECT * FROM "users" INNER JOIN "users" "users_2" ON "users"."id" = "users_2"."id"')

    def test_join_can_have_a_non_table_alias_as_relation_name(self):
        users = Table('users')
        comments = Table('comments')
        counts = comments.from_().group(comments['user_id']).project(
            comments['user_id'].as_("user_id"),
            comments['user_id'].count().as_("count")
        ).as_("counts")
        joins = users.join(counts).on(counts['user_id'].eq(10))
        sql_result = joins.to_sql()
        assert 'SELECT FROM "users" INNER JOIN' in sql_result
        assert 'counts ON' in sql_result
        assert '"counts"."user_id" = 10' in sql_result or 'counts."user_id" = 10' in sql_result

    def test_can_be_empty(self):
        manager = SelectManager()
        must_be_like(manager.to_sql(), 'SELECT')

    def test_window_can_be_empty(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window")
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS ()')

    def test_window_takes_an_order(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").order(table['foo'].asc())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (ORDER BY "users"."foo" ASC)')

    def test_window_takes_an_order_with_multiple_columns(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").order(table['foo'].asc(), table['bar'].desc())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (ORDER BY "users"."foo" ASC, "users"."bar" DESC)')

    def test_window_takes_a_partition(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").partition(table['bar'])
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (PARTITION BY "users"."bar")')

    def test_window_takes_a_partition_and_an_order(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").partition(table['foo']).order(table['foo'].asc())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (PARTITION BY "users"."foo" ORDER BY "users"."foo" ASC)')

    def test_window_takes_a_partition_with_multiple_columns(self):
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").partition(table['bar'], table['baz'])
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (PARTITION BY "users"."bar", "users"."baz")')

    def test_window_takes_a_rows_frame_unbounded_preceding(self):
        from arel.nodes.window import Preceding
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").rows(Preceding())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (ROWS UNBOUNDED PRECEDING)')

    def test_window_takes_a_rows_frame_bounded_preceding(self):
        from arel.nodes.window import Preceding
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").rows(Preceding(5))
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (ROWS 5 PRECEDING)')

    def test_window_takes_a_rows_frame_unbounded_following(self):
        from arel.nodes.window import Following
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").rows(Following())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (ROWS UNBOUNDED FOLLOWING)')

    def test_window_takes_a_rows_frame_bounded_following(self):
        from arel.nodes.window import Following
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").rows(Following(5))
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (ROWS 5 FOLLOWING)')

    def test_window_takes_a_rows_frame_current_row(self):
        from arel.nodes.window import CurrentRow
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").rows(CurrentRow())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (ROWS CURRENT ROW)')

    def test_window_takes_a_rows_frame_between_two_delimiters(self):
        from arel.nodes.window import Preceding, CurrentRow, Rows
        from arel.nodes.binary import Between
        from arel.nodes.nary import And
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        window = manager.window("a_window")
        window.frame(Between(window.rows(), And([Preceding(), CurrentRow()])))
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)')

    def test_window_takes_a_range_frame_unbounded_preceding(self):
        from arel.nodes.window import Preceding
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").range(Preceding())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (RANGE UNBOUNDED PRECEDING)')

    def test_window_takes_a_range_frame_bounded_preceding(self):
        from arel.nodes.window import Preceding
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").range(Preceding(5))
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (RANGE 5 PRECEDING)')

    def test_window_takes_a_range_frame_unbounded_following(self):
        from arel.nodes.window import Following
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").range(Following())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (RANGE UNBOUNDED FOLLOWING)')

    def test_window_takes_a_range_frame_bounded_following(self):
        from arel.nodes.window import Following
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").range(Following(5))
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (RANGE 5 FOLLOWING)')

    def test_window_takes_a_range_frame_current_row(self):
        from arel.nodes.window import CurrentRow
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        manager.window("a_window").range(CurrentRow())
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (RANGE CURRENT ROW)')

    def test_window_takes_a_range_frame_between_two_delimiters(self):
        from arel.nodes.window import Preceding, CurrentRow, Range
        from arel.nodes.binary import Between
        from arel.nodes.nary import And
        table = Table('users')
        manager = SelectManager()
        manager.from_(table)
        window = manager.window("a_window")
        window.frame(Between(window.range(), And([Preceding(), CurrentRow()])))
        must_be_like(manager.to_sql(), 'SELECT FROM "users" WINDOW "a_window" AS (RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)')
