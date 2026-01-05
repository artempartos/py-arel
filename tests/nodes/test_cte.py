import pytest
from arel import Table
from arel.nodes.cte import Cte

class TestCte:
    def test_equality_with_equal_ivars(self):
        array = [
            Cte("foo", "bar", materialized=True),
            Cte("foo", "bar", materialized=True)
        ]
        assert len(set(array)) == 1

    def test_inequality_with_unequal_ivars(self):
        array = [
            Cte("foo", "bar", materialized=True),
            Cte("foo", "bar")
        ]
        assert len(set(array)) == 2

    def test_to_cte_returns_self(self):
        cte = Cte("foo", "bar")
        assert cte.to_cte() == cte

    def test_to_table_returns_an_arel_table_using_cte_name(self):
        table = Cte("foo", "bar").to_table()
        assert isinstance(table, Table)
        assert table.name == "foo"

