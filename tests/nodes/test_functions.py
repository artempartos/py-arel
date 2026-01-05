from arel.nodes.named_function import NamedFunction

class TestNamedFunction:
    def test_construct(self):
        function = NamedFunction("omg", "zomg")
        assert function.name == "omg"
        assert function.expressions == "zomg"

    def test_equality_with_same_ivars(self):
        array = [
            NamedFunction("omg", "zomg"),
            NamedFunction("omg", "zomg")
        ]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        array = [
            NamedFunction("omg", "zomg"),
            NamedFunction("zomg", "zomg")
        ]
        assert len(set(array)) == 2
