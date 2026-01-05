import pytest
from arel import Table
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestMath:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.engine = MockEngine(ToSql)
        Table.engine = self.engine

    def compile(self, node):
        from arel.collectors.sql_string import SQLString
        return self.engine.connection.visitor.accept(node, SQLString()).value

    def test_average_should_be_compatible_with_multiplication(self):
        table = Table('users')
        sql = self.compile(table['id'].average() * 2)
        must_be_like(sql, 'AVG("users"."id") * 2')

    def test_average_should_be_compatible_with_division(self):
        table = Table('users')
        sql = self.compile(table['id'].average() / 2)
        must_be_like(sql, 'AVG("users"."id") / 2')

    def test_count_should_be_compatible_with_multiplication(self):
        table = Table('users')
        sql = self.compile(table['id'].count() * 2)
        must_be_like(sql, 'COUNT("users"."id") * 2')

    def test_count_should_be_compatible_with_division(self):
        table = Table('users')
        sql = self.compile(table['id'].count() / 2)
        must_be_like(sql, 'COUNT("users"."id") / 2')

    def test_maximum_should_be_compatible_with_multiplication(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() * 2)
        must_be_like(sql, 'MAX("users"."id") * 2')

    def test_maximum_should_be_compatible_with_division(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() / 2)
        must_be_like(sql, 'MAX("users"."id") / 2')

    def test_minimum_should_be_compatible_with_multiplication(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() * 2)
        must_be_like(sql, 'MIN("users"."id") * 2')

    def test_minimum_should_be_compatible_with_division(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() / 2)
        must_be_like(sql, 'MIN("users"."id") / 2')

    def test_attribute_node_should_be_compatible_with_multiplication(self):
        table = Table('users')
        sql = self.compile(table['id'] * 2)
        must_be_like(sql, '"users"."id" * 2')

    def test_attribute_node_should_be_compatible_with_division(self):
        table = Table('users')
        sql = self.compile(table['id'] / 2)
        must_be_like(sql, '"users"."id" / 2')

    def test_average_should_be_compatible_with_addition(self):
        table = Table('users')
        sql = self.compile(table['id'].average() + 2)
        must_be_like(sql, '(AVG("users"."id") + 2)')

    def test_average_should_be_compatible_with_subtraction(self):
        table = Table('users')
        sql = self.compile(table['id'].average() - 2)
        must_be_like(sql, '(AVG("users"."id") - 2)')

    def test_count_should_be_compatible_with_addition(self):
        table = Table('users')
        sql = self.compile(table['id'].count() + 2)
        must_be_like(sql, '(COUNT("users"."id") + 2)')

    def test_count_should_be_compatible_with_subtraction(self):
        table = Table('users')
        sql = self.compile(table['id'].count() - 2)
        must_be_like(sql, '(COUNT("users"."id") - 2)')

    def test_maximum_should_be_compatible_with_addition(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() + 2)
        must_be_like(sql, '(MAX("users"."id") + 2)')

    def test_maximum_should_be_compatible_with_subtraction(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() - 2)
        must_be_like(sql, '(MAX("users"."id") - 2)')

    def test_minimum_should_be_compatible_with_addition(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() + 2)
        must_be_like(sql, '(MIN("users"."id") + 2)')

    def test_minimum_should_be_compatible_with_subtraction(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() - 2)
        must_be_like(sql, '(MIN("users"."id") - 2)')

    def test_attribute_node_should_be_compatible_with_addition(self):
        table = Table('users')
        sql = self.compile(table['id'] + 2)
        must_be_like(sql, '("users"."id" + 2)')

    def test_attribute_node_should_be_compatible_with_subtraction(self):
        table = Table('users')
        sql = self.compile(table['id'] - 2)
        must_be_like(sql, '("users"."id" - 2)')

    def test_average_should_be_compatible_with_bitwise_and(self):
        table = Table('users')
        sql = self.compile(table['id'].average() & 2)
        must_be_like(sql, '(AVG("users"."id") & 2)')

    def test_average_should_be_compatible_with_bitwise_or(self):
        table = Table('users')
        sql = self.compile(table['id'].average() | 2)
        must_be_like(sql, '(AVG("users"."id") | 2)')

    def test_average_should_be_compatible_with_bitwise_xor(self):
        table = Table('users')
        sql = self.compile(table['id'].average() ^ 2)
        must_be_like(sql, '(AVG("users"."id") ^ 2)')

    def test_average_should_be_compatible_with_bitwise_shift_left(self):
        table = Table('users')
        sql = self.compile(table['id'].average() << 2)
        must_be_like(sql, '(AVG("users"."id") << 2)')

    def test_average_should_be_compatible_with_bitwise_shift_right(self):
        table = Table('users')
        sql = self.compile(table['id'].average() >> 2)
        must_be_like(sql, '(AVG("users"."id") >> 2)')

    def test_count_should_be_compatible_with_bitwise_and(self):
        table = Table('users')
        sql = self.compile(table['id'].count() & 2)
        must_be_like(sql, '(COUNT("users"."id") & 2)')

    def test_count_should_be_compatible_with_bitwise_or(self):
        table = Table('users')
        sql = self.compile(table['id'].count() | 2)
        must_be_like(sql, '(COUNT("users"."id") | 2)')

    def test_count_should_be_compatible_with_bitwise_xor(self):
        table = Table('users')
        sql = self.compile(table['id'].count() ^ 2)
        must_be_like(sql, '(COUNT("users"."id") ^ 2)')

    def test_count_should_be_compatible_with_bitwise_shift_left(self):
        table = Table('users')
        sql = self.compile(table['id'].count() << 2)
        must_be_like(sql, '(COUNT("users"."id") << 2)')

    def test_count_should_be_compatible_with_bitwise_shift_right(self):
        table = Table('users')
        sql = self.compile(table['id'].count() >> 2)
        must_be_like(sql, '(COUNT("users"."id") >> 2)')

    def test_maximum_should_be_compatible_with_bitwise_and(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() & 2)
        must_be_like(sql, '(MAX("users"."id") & 2)')

    def test_maximum_should_be_compatible_with_bitwise_or(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() | 2)
        must_be_like(sql, '(MAX("users"."id") | 2)')

    def test_maximum_should_be_compatible_with_bitwise_xor(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() ^ 2)
        must_be_like(sql, '(MAX("users"."id") ^ 2)')

    def test_maximum_should_be_compatible_with_bitwise_shift_left(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() << 2)
        must_be_like(sql, '(MAX("users"."id") << 2)')

    def test_maximum_should_be_compatible_with_bitwise_shift_right(self):
        table = Table('users')
        sql = self.compile(table['id'].maximum() >> 2)
        must_be_like(sql, '(MAX("users"."id") >> 2)')

    def test_minimum_should_be_compatible_with_bitwise_and(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() & 2)
        must_be_like(sql, '(MIN("users"."id") & 2)')

    def test_minimum_should_be_compatible_with_bitwise_or(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() | 2)
        must_be_like(sql, '(MIN("users"."id") | 2)')

    def test_minimum_should_be_compatible_with_bitwise_xor(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() ^ 2)
        must_be_like(sql, '(MIN("users"."id") ^ 2)')

    def test_minimum_should_be_compatible_with_bitwise_shift_left(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() << 2)
        must_be_like(sql, '(MIN("users"."id") << 2)')

    def test_minimum_should_be_compatible_with_bitwise_shift_right(self):
        table = Table('users')
        sql = self.compile(table['id'].minimum() >> 2)
        must_be_like(sql, '(MIN("users"."id") >> 2)')

    def test_attribute_node_should_be_compatible_with_bitwise_and(self):
        table = Table('users')
        sql = self.compile(table['id'] & 2)
        must_be_like(sql, '("users"."id" & 2)')

    def test_attribute_node_should_be_compatible_with_bitwise_or(self):
        table = Table('users')
        sql = self.compile(table['id'] | 2)
        must_be_like(sql, '("users"."id" | 2)')

    def test_attribute_node_should_be_compatible_with_bitwise_xor(self):
        table = Table('users')
        sql = self.compile(table['id'] ^ 2)
        must_be_like(sql, '("users"."id" ^ 2)')

    def test_attribute_node_should_be_compatible_with_bitwise_shift_left(self):
        table = Table('users')
        sql = self.compile(table['id'] << 2)
        must_be_like(sql, '("users"."id" << 2)')

    def test_attribute_node_should_be_compatible_with_bitwise_shift_right(self):
        table = Table('users')
        sql = self.compile(table['id'] >> 2)
        must_be_like(sql, '("users"."id" >> 2)')

