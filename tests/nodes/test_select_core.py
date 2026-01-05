import copy
import pytest
from arel import Table
from arel.nodes.select_core import SelectCore
from arel.nodes.distinct import Distinct
from arel.nodes.comment import Comment
from arel.visitors.to_sql import ToSql
from tests.python.helper import MockEngine, must_be_like

class TestSelectCore:
    def test_clone(self):
        core = SelectCore()
        core.from_ = ['a', 'b', 'c']
        core.projections = ['d', 'e', 'f']
        core.wheres = ['g', 'h', 'i']

        dolly = copy.copy(core)

        assert core.from_ == dolly.from_
        assert core.projections == dolly.projections
        assert core.wheres == dolly.wheres

        assert core.from_ is not dolly.from_
        assert core.projections is not dolly.projections
        assert core.wheres is not dolly.wheres

    def test_set_quantifier(self):
        core = SelectCore()
        core.set_quantifier = Distinct()
        engine = MockEngine(ToSql)
        Table.engine = engine
        viz = engine.connection.visitor
        from arel.collectors.sql_string import SQLString
        sql = viz.accept(core, SQLString()).value
        must_be_like(sql, "SELECT DISTINCT")

    def test_equality_with_same_ivars(self):
        core1 = SelectCore()
        core1.from_       = ['a', 'b', 'c']
        core1.projections = ['d', 'e', 'f']
        core1.wheres      = ['g', 'h', 'i']
        core1.groups      = ['j', 'k', 'l']
        core1.windows     = ['m', 'n', 'o']
        core1.havings     = ['p', 'q', 'r']
        core1.comment     = Comment(["comment"])

        core2 = SelectCore()
        core2.from_       = ['a', 'b', 'c']
        core2.projections = ['d', 'e', 'f']
        core2.wheres      = ['g', 'h', 'i']
        core2.groups      = ['j', 'k', 'l']
        core2.windows     = ['m', 'n', 'o']
        core2.havings     = ['p', 'q', 'r']
        core2.comment     = Comment(["comment"])

        array = [core1, core2]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        core1 = SelectCore()
        core1.from_       = ['a', 'b', 'c']
        core1.projections = ['d', 'e', 'f']
        core1.wheres      = ['g', 'h', 'i']
        core1.groups      = ['j', 'k', 'l']
        core1.windows     = ['m', 'n', 'o']
        core1.havings     = ['p', 'q', 'r']
        core1.comment     = Comment(["comment"])

        core2 = SelectCore()
        core2.from_       = ['a', 'b', 'c']
        core2.projections = ['d', 'e', 'f']
        core2.wheres      = ['g', 'h', 'i']
        core2.groups      = ['j', 'k', 'l']
        core2.windows     = ['m', 'n', 'o']
        core2.havings     = ['l', 'o', 'l']
        core2.comment     = Comment(["comment"])

        array = [core1, core2]
        assert len(set(array)) == 2

        core2.havings     = ['p', 'q', 'r']
        core2.comment     = Comment(["other"])
        array = [core1, core2]
        assert len(set(array)) == 2
