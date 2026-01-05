import pytest
from arel.nodes.window import Window, NamedWindow, CurrentRow
from arel.nodes.node import Node

class TestWindow:
    def test_equality_with_equal_ivars(self):
        window1 = Window()
        window1.orders = [1, 2]
        window1.partitions = [1]
        window1.frame(3)
        window2 = Window()
        window2.orders = [1, 2]
        window2.partitions = [1]
        window2.frame(3)
        array = [window1, window2]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        window1 = Window()
        window1.orders = [1, 2]
        window1.partitions = [1]
        window1.frame(3)
        window2 = Window()
        window2.orders = [1, 2]
        window2.partitions = [1]
        window2.frame(4)
        array = [window1, window2]
        assert len(set(array)) == 2

class TestNamedWindow:
    def test_equality_with_equal_ivars(self):
        window1 = NamedWindow("foo")
        window1.orders = [1, 2]
        window1.partitions = [1]
        window1.frame(3)
        window2 = NamedWindow("foo")
        window2.orders = [1, 2]
        window2.partitions = [1]
        window2.frame(3)
        array = [window1, window2]
        assert len(set(array)) == 1

    def test_inequality_with_different_ivars(self):
        window1 = NamedWindow("foo")
        window1.orders = [1, 2]
        window1.partitions = [1]
        window1.frame(3)
        window2 = NamedWindow("bar")
        window2.orders = [1, 2]
        window2.partitions = [1]
        window2.frame(3)
        array = [window1, window2]
        assert len(set(array)) == 2

class TestCurrentRow:
    def test_equality_to_other_current_row_nodes(self):
        array = [CurrentRow(), CurrentRow()]
        assert len(set(array)) == 1

    def test_inequality_with_other_nodes(self):
        array = [CurrentRow(), Node()]
        assert len(set(array)) == 2

