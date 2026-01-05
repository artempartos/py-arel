import pytest
from arel import Table
from arel.mixins.factory_methods import FactoryMethodsMixin
from arel.nodes.joins import Join, StringJoin
from arel.nodes.table_alias import TableAlias
from arel.nodes.nary import And
from arel.nodes.grouping import Grouping
from arel.nodes.unary import On
from arel.nodes.true import True_
from arel.nodes.false import False_
from arel.nodes.named_function import NamedFunction

class Factory(FactoryMethodsMixin):
    pass

class TestFactoryMethods:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.factory = Factory()

    def test_create_join(self):
        join = self.factory.create_join("one", "two")
        assert isinstance(join, Join)
        assert join.right == "two"

    def test_create_table_alias(self):
        table_alias = self.factory.create_table_alias("one", "two")
        assert isinstance(table_alias, TableAlias)
        assert table_alias.right == "two"

    def test_create_and(self):
        and_node = self.factory.create_and(["foo", "bar"])
        assert isinstance(and_node, And)
        assert and_node.children == ["foo", "bar"]

    def test_create_string_join(self):
        join = self.factory.create_string_join("foo")
        assert isinstance(join, StringJoin)
        assert join.left == "foo"

    def test_grouping(self):
        grouping = self.factory.grouping("one")
        assert isinstance(grouping, Grouping)
        assert grouping.expr == "one"

    def test_create_on(self):
        on = self.factory.create_on("one")
        assert isinstance(on, On)
        assert on.expr == "one"

    def test_create_true(self):
        true_node = self.factory.create_true()
        assert isinstance(true_node, True_)

    def test_create_false(self):
        false_node = self.factory.create_false()
        assert isinstance(false_node, False_)

    def test_lower(self):
        lower = self.factory.lower("one")
        assert isinstance(lower, NamedFunction)
        assert lower.name == "LOWER"
        # In Python expressions can be a list or a single element
        if isinstance(lower.expressions, list):
            assert len(lower.expressions) == 1
        else:
            assert lower.expressions == "one"

    def test_coalesce(self):
        relation = Table('users')
        field_node = relation['active']
        coalesce = self.factory.coalesce(field_node, 0)
        assert isinstance(coalesce, NamedFunction)
        assert coalesce.name == "COALESCE"
        if isinstance(coalesce.expressions, list):
            assert field_node in coalesce.expressions or coalesce.expressions == [field_node, 0]
        else:
            assert coalesce.expressions == field_node

    def test_cast(self):
        relation = Table('users')
        field_node = relation['active']
        cast = self.factory.cast(field_node, "boolean")
        assert isinstance(cast, NamedFunction)
        assert cast.name == "CAST"
        if isinstance(cast.expressions, list):
            as_node = cast.expressions[0]
        else:
            as_node = cast.expressions
        from arel.nodes.binary import As
        assert isinstance(as_node, As)
        assert as_node.left == field_node
        assert str(as_node.right) == "boolean"

