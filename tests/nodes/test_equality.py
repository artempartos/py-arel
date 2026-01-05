from arel import Table
from arel.nodes.equality import Equality
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine

class TestEquality:
    def test_takes_an_engine(self):
        # Backwards compat: to_sql takes an engine
        engine = MockEngine(ToSql)
        Table.engine = engine
        attr = Table('users')['id']
        test = attr.eq(10)
        sql = test.to_sql(engine)
        assert sql is not None

    def test_or(self):
        attr = Table('users')['id']
        left = attr.eq(10)
        right = attr.eq(11)
        node = left.or_(right)
        assert node.expr.left == left
        assert node.expr.right == right

    def test_and(self):
        attr = Table('users')['id']
        left = attr.eq(10)
        right = attr.eq(11)
        node = left.and_(right)
        assert node.left == left
        assert node.right == right

    def test_is_equal_with_equal_ivars(self):
        array = [Equality("foo", "bar"), Equality("foo", "bar")]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_ivars(self):
        array = [Equality("foo", "bar"), Equality("foo", "baz")]
        assert len(set(array)) == 2
