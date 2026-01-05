import pytest
from arel import Table
from arel.nodes.table_alias import TableAlias
from arel.nodes.cte import Cte

class TestTableAlias:
    def test_is_equal_with_equal_ivars(self):
        relation1 = Table('users')
        node1 = TableAlias(relation1, 'foo')
        relation2 = Table('users')
        node2 = TableAlias(relation2, 'foo')
        array = [node1, node2]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_ivars(self):
        relation1 = Table('users')
        node1 = TableAlias(relation1, 'foo')
        relation2 = Table('users')
        node2 = TableAlias(relation2, 'bar')
        array = [node1, node2]
        assert len(set(array)) == 2

    def test_returns_a_cte_node_using_the_table_alias(self):
        from arel import star
        relation = Table('users').project(star())
        table_alias = TableAlias(relation, 'foo')
        cte = table_alias.to_cte()

        assert isinstance(cte, Cte)
        assert cte.name == 'foo'
        assert cte.relation == relation

