import copy
from arel.nodes.case import Case, When, Else
from arel.nodes.casted import build_quoted
from arel.nodes.sql_literal import SqlLiteral

class TestCase:
    def test_sets_case_expression_from_first_argument(self):
        node = Case("foo")
        assert node.case == "foo"

    def test_sets_default_case_from_second_argument(self):
        node = Case(None, "bar")
        assert node.default == "bar"

    def test_clones_case_conditions_and_default(self):
        foo = build_quoted("foo")
        node = Case()
        node.case = foo
        node.conditions = [When(foo, foo)]
        node.default = foo

        dolly = copy.copy(node)

        assert dolly.case == node.case
        assert dolly.case is not node.case

        assert dolly.conditions == node.conditions
        assert dolly.conditions is not node.conditions

        assert dolly.default == node.default
        assert dolly.default is not node.default

    def test_is_equal_with_equal_ivars(self):
        foo = build_quoted("foo")
        one = build_quoted(1)
        zero = build_quoted(0)

        case1 = Case(foo)
        case1.conditions = [When(foo, one)]
        case1.default = Else(zero)

        case2 = Case(foo)
        case2.conditions = [When(foo, one)]
        case2.default = Else(zero)

        array = [case1, case2]
        assert len(set(array)) == 1

    def test_is_not_equal_with_different_ivars(self):
        foo = build_quoted("foo")
        bar = build_quoted("bar")
        one = build_quoted(1)
        zero = build_quoted(0)

        case1 = Case(foo)
        case1.conditions = [When(foo, one)]
        case1.default = Else(zero)

        case2 = Case(foo)
        case2.conditions = [When(bar, one)]
        case2.default = Else(zero)

        array = [case1, case2]
        assert len(set(array)) == 2

    def test_allows_aliasing(self):
        node = Case("foo")
        as_node = node.as_("bar")
        assert as_node.left == node
        assert isinstance(as_node.right, SqlLiteral)
