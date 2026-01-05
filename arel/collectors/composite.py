from __future__ import annotations
from typing import Any, Tuple

class Composite:
    def __init__(self, left: Any, right: Any):
        self.left = left
        self.right = right

    @property
    def value(self) -> Tuple[Any, Any]:
        return (self.left.value, self.right.value)

    def __lshift__(self, str_val: str) -> 'Composite':
        self.left << str_val
        return self

    def add_bind(self, bind: Any, block: Any = None) -> 'Composite':
        self.left.add_bind(bind, block)
        self.right.add_bind(bind, block)
        return self

    def add_binds(self, binds: list, proc_for_binds: Any = None, block: Any = None) -> 'Composite':
        self.left.add_binds(binds, proc_for_binds, block)
        self.right.add_binds(binds, proc_for_binds, block)
        return self

    @property
    def retryable(self) -> bool:
        return getattr(self.left, 'retryable', False) and getattr(self.right, 'retryable', False)

    @retryable.setter
    def retryable(self, value: bool) -> None:
        if hasattr(self.left, 'retryable'):
            self.left.retryable = value
        if hasattr(self.right, 'retryable'):
            self.right.retryable = value

