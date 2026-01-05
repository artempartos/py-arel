import pytest
from arel import Table
from arel.update_manager import UpdateManager
from arel.nodes.bind_param import BindParam
from arel.nodes.joins import InnerJoin
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestUpdateManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, manager):
        return manager.to_sql()

    def test_should_not_quote_sql_literals(self):
        table = Table('users')
        um = UpdateManager()
        um.table(table)
        um.set([[table['name'], BindParam(1)]])
        sql_result = self.compile(um)
        must_be_like(sql_result, 'UPDATE "users" SET "name" = ?')

    def test_handles_limit_properly(self):
        table = Table('users')
        um = UpdateManager()
        um.key = "id"
        um.take(10)
        um.table(table)
        um.set([[table['name'], None]])
        sql_result = self.compile(um)
        assert 'LIMIT 10' in sql_result

    def test_sets_having(self):
        users_table = Table('users')
        posts_table = Table('posts')
        join_source = InnerJoin(users_table, posts_table)

        update_manager = UpdateManager()
        update_manager.table(join_source)
        update_manager.group("posts.id")
        update_manager.having("count(posts.id) >= 2")

        assert update_manager._ast.havings == ["count(posts.id) >= 2"]

    def test_adds_columns_to_ast_when_group_value_is_string(self):
        users_table = Table('users')
        posts_table = Table('posts')
        join_source = InnerJoin(users_table, posts_table)

        update_manager = UpdateManager()
        update_manager.table(join_source)
        update_manager.group("posts.id")
        update_manager.having("count(posts.id) >= 2")

        assert len(update_manager._ast.groups) == 1
        group_ast = update_manager._ast.groups[0]
        from arel.nodes.unary import Group
        from arel.nodes.sql_literal import SqlLiteral
        assert isinstance(group_ast, Group)
        assert isinstance(group_ast.expr, SqlLiteral)
        assert str(group_ast.expr) == "posts.id"
        assert update_manager._ast.havings == ["count(posts.id) >= 2"]

    def test_adds_columns_to_ast_when_group_value_is_symbol(self):
        users_table = Table('users')
        posts_table = Table('posts')
        join_source = InnerJoin(users_table, posts_table)

        update_manager = UpdateManager()
        update_manager.table(join_source)
        # In Python there are no symbols, use string
        update_manager.group("posts.id")
        update_manager.having("count(posts.id) >= 2")

        assert len(update_manager._ast.groups) == 1
        group_ast = update_manager._ast.groups[0]
        from arel.nodes.unary import Group
        from arel.nodes.sql_literal import SqlLiteral
        assert isinstance(group_ast, Group)
        assert isinstance(group_ast.expr, SqlLiteral)
        assert str(group_ast.expr) == "posts.id"
        assert update_manager._ast.havings == ["count(posts.id) >= 2"]

    def test_set_updates_with_null(self):
        table = Table('users')
        um = UpdateManager()
        um.table(table)
        um.set([[table['name'], None]])
        sql_result = self.compile(um)
        must_be_like(sql_result, 'UPDATE "users" SET "name" = NULL')

    def test_set_takes_a_string(self):
        from arel.nodes.sql_literal import SqlLiteral
        table = Table('users')
        um = UpdateManager()
        um.table(table)
        um.set(SqlLiteral("foo = bar"))
        sql_result = self.compile(um)
        must_be_like(sql_result, 'UPDATE "users" SET foo = bar')

    def test_set_takes_a_list_of_lists(self):
        table = Table('users')
        um = UpdateManager()
        um.table(table)
        um.set([[table['id'], 1], [table['name'], "hello"]])
        sql_result = self.compile(um)
        must_be_like(sql_result, 'UPDATE "users" SET "id" = 1, "name" = \'hello\'')

    def test_set_chains(self):
        table = Table('users')
        um = UpdateManager()
        assert um.set([[table['id'], 1], [table['name'], "hello"]]) == um

    def test_table_generates_an_update_statement(self):
        um = UpdateManager()
        um.table(Table('users'))
        sql_result = self.compile(um)
        must_be_like(sql_result, 'UPDATE "users"')

    def test_table_chains(self):
        um = UpdateManager()
        assert um.table(Table('users')) == um

    def test_table_generates_an_update_statement_with_joins(self):
        from arel.nodes.join_source import JoinSource
        um = UpdateManager()

        table = Table('users')
        join_source = JoinSource(
            table,
            [table.create_join(Table('posts'))]
        )

        um.table(join_source)
        sql_result = self.compile(um)
        must_be_like(sql_result, 'UPDATE "users" INNER JOIN "posts"')

    def test_where_generates_a_where_clause(self):
        table = Table('users')
        um = UpdateManager()
        um.table(table)
        um.where(table['id'].eq(1))
        sql_result = self.compile(um)
        must_be_like(sql_result, 'UPDATE "users" WHERE "users"."id" = 1')

    def test_where_chains(self):
        table = Table('users')
        um = UpdateManager()
        um.table(table)
        assert um.where(table['id'].eq(1)) == um

    def test_key_can_be_set(self):
        table = Table('users')
        um = UpdateManager()
        um.key = table['foo']
        assert um._ast.key == table['foo']

    def test_key_can_be_accessed(self):
        table = Table('users')
        um = UpdateManager()
        um.key = table['foo']
        assert um.key == table['foo']

