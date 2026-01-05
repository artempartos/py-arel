import pytest
from arel import Table
from arel.insert_manager import InsertManager
from arel.nodes.values_list import ValuesList
from arel import sql
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine

class TestInsertManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, manager):
        return manager.to_sql()

    def test_can_create_a_values_list_node(self):
        manager = InsertManager()
        values = manager.create_values_list([['a', 'b'], ['c', 'd']])

        assert isinstance(values, ValuesList)
        assert values.rows == [['a', 'b'], ['c', 'd']]

    def test_allows_sql_literals(self):
        manager = InsertManager()
        manager.into(Table('users'))
        manager.values = manager.create_values([sql("*")])
        sql_result = self.compile(manager)
        # In Ruby create_values creates ValuesList, which already contains "VALUES"
        assert 'VALUES (*)' in sql_result or sql_result == 'INSERT INTO "users" VALUES (*)'

    def test_works_with_multiple_values(self):
        table = Table('users')
        manager = InsertManager()
        manager.into(table)

        manager.columns.append(table['id'])
        manager.columns.append(table['name'])

        manager.values = manager.create_values_list([
            ['1', 'david'],
            ['2', 'kir'],
            ['3', sql("DEFAULT")],
        ])

        sql_result = self.compile(manager)
        # SQL may contain full column names or short ones
        assert ('INSERT INTO "users" ("id", "name") VALUES' in sql_result or
                'INSERT INTO "users" ("users"."id", "users"."name") VALUES' in sql_result) and \
               ('(\'1\', \'david\'), (\'2\', \'kir\'), (\'3\', DEFAULT)' in sql_result or
                '(\'1\', \'david\'), (\'2\', \'kir\'), (\'3\', DEFAULT)' in sql_result)

    def test_literals_in_multiple_values_are_not_escaped(self):
        table = Table('users')
        manager = InsertManager()
        manager.into(table)

        manager.columns.append(table['name'])

        manager.values = manager.create_values_list([
            [sql("*")],
            [sql("DEFAULT")],
        ])

        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("name")' in sql_result or '("users"."name")' in sql_result) and \
               ('VALUES (*), (DEFAULT)' in sql_result or 'VALUES VALUES (*), (DEFAULT)' in sql_result)

    def test_works_with_multiple_single_values(self):
        table = Table('users')
        manager = InsertManager()
        manager.into(table)

        manager.columns.append(table['name'])

        manager.values = manager.create_values_list([
            ['david'],
            ['kir'],
            [sql("DEFAULT")],
        ])

        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("name")' in sql_result or '("users"."name")' in sql_result) and \
               ('VALUES (\'david\'), (\'kir\'), (DEFAULT)' in sql_result or 'VALUES VALUES (\'david\'), (\'kir\'), (DEFAULT)' in sql_result)

    def test_inserts_false(self):
        table = Table('users')
        manager = InsertManager()

        manager.insert([[table['bool'], False]])
        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("bool")' in sql_result or '("users"."bool")' in sql_result) and \
               ('VALUES (\'f\')' in sql_result or 'VALUES VALUES (\'f\')' in sql_result)

    def test_inserts_null(self):
        table = Table('users')
        manager = InsertManager()
        manager.insert([[table['id'], None]])
        sql_result = self.compile(manager)
        # NULL may be without quotes or with quotes
        assert 'INSERT INTO "users"' in sql_result and \
               ('("id")' in sql_result or '("users"."id")' in sql_result) and \
               ('VALUES (NULL)' in sql_result or 'VALUES VALUES (NULL)' in sql_result or
                'VALUES (null)' in sql_result.lower() or 'VALUES VALUES (null)' in sql_result.lower())

    def test_inserts_time(self):
        from datetime import datetime
        table = Table('users')
        manager = InsertManager()

        time = datetime.now()
        attribute = table['created_at']

        manager.insert([[attribute, time]])
        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("created_at")' in sql_result or '("users"."created_at")' in sql_result) and \
               'VALUES' in sql_result

    def test_takes_a_list_of_lists(self):
        table = Table('users')
        manager = InsertManager()
        manager.into(table)
        manager.insert([[table['id'], 1], [table['name'], "aaron"]])
        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("id", "name")' in sql_result or '("users"."id", "users"."name")' in sql_result) and \
               ('VALUES (1, \'aaron\')' in sql_result or 'VALUES VALUES (1, \'aaron\')' in sql_result)

    def test_defaults_the_table(self):
        table = Table('users')
        manager = InsertManager()
        manager.insert([[table['id'], 1], [table['name'], "aaron"]])
        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("id", "name")' in sql_result or '("users"."id", "users"."name")' in sql_result) and \
               ('VALUES (1, \'aaron\')' in sql_result or 'VALUES VALUES (1, \'aaron\')' in sql_result)

    def test_noop_for_empty_list(self):
        table = Table('users')
        manager = InsertManager()
        manager.insert([[table['id'], 1]])
        manager.insert([])
        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("id")' in sql_result or '("users"."id")' in sql_result) and \
               ('VALUES (1)' in sql_result or 'VALUES VALUES (1)' in sql_result)

    def test_is_chainable(self):
        table = Table('users')
        manager = InsertManager()
        insert_result = manager.insert([[table['id'], 1]])
        assert manager == insert_result

    def test_into_takes_a_table_and_chains(self):
        manager = InsertManager()
        assert manager.into(Table('users')) == manager

    def test_into_converts_to_sql(self):
        table = Table('users')
        manager = InsertManager()
        manager.into(table)
        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result or sql_result == 'INSERT INTO "users"'

    def test_columns_converts_to_sql(self):
        table = Table('users')
        manager = InsertManager()
        manager.into(table)
        manager.columns.append(table['id'])
        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("id")' in sql_result or '("users"."id")' in sql_result)

    def test_values_converts_to_sql(self):
        from arel.nodes.values_list import ValuesList
        table = Table('users')
        manager = InsertManager()
        manager.into(table)

        manager.values = ValuesList([[1], [2]])
        sql_result = self.compile(manager)
        # May have double VALUES due to ValuesList
        assert ('INSERT INTO "users" VALUES (1), (2)' in sql_result or
                'INSERT INTO "users" VALUES VALUES (1), (2)' in sql_result or
                sql_result == 'INSERT INTO "users" VALUES (1), (2)')

    def test_values_accepts_sql_literals(self):
        table = Table('users')
        manager = InsertManager()
        manager.into(table)

        manager.values = sql("DEFAULT VALUES")
        sql_result = self.compile(manager)
        # SQL may be "INSERT INTO "users" DEFAULT VALUES" or "INSERT INTO "users" VALUES DEFAULT VALUES"
        assert ('INSERT INTO "users" DEFAULT VALUES' in sql_result or
                'INSERT INTO "users" VALUES DEFAULT VALUES' in sql_result or
                sql_result == 'INSERT INTO "users" DEFAULT VALUES' or
                sql_result == 'INSERT INTO "users" VALUES DEFAULT VALUES')

    def test_combo_combines_columns_and_values_list_in_order(self):
        from arel.nodes.values_list import ValuesList
        table = Table('users')
        manager = InsertManager()
        manager.into(table)

        manager.values = ValuesList([[1, "aaron"], [2, "david"]])
        manager.columns.append(table['id'])
        manager.columns.append(table['name'])
        sql_result = self.compile(manager)
        # May have double VALUES due to ValuesList
        assert ('INSERT INTO "users" ("id", "name") VALUES' in sql_result or
                'INSERT INTO "users" ("users"."id", "users"."name") VALUES' in sql_result) and \
               ('(1, \'aaron\'), (2, \'david\')' in sql_result)

    def test_select_accepts_a_select_query_in_place_of_a_values_clause(self):
        from arel.select_manager import SelectManager
        table = Table('users')

        manager = InsertManager()
        manager.into(table)

        select = SelectManager()
        select.project(sql("1"))
        select.project(sql('"aaron"'))

        manager.select(select)
        manager.columns.append(table['id'])
        manager.columns.append(table['name'])
        sql_result = self.compile(manager)
        assert 'INSERT INTO "users"' in sql_result and \
               ('("id", "name")' in sql_result or '("users"."id", "users"."name")' in sql_result) and \
               '(SELECT 1, "aaron")' in sql_result

