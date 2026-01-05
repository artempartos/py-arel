from __future__ import annotations
from typing import Any, List

class Bind:
    def __init__(self):
        self._binds = []

    @property
    def value(self) -> List[Any]:
        return self._binds

    def add_bind(self, bind: Any, block: Any = None) -> 'Bind':
        self._binds.append(bind)
        return self

    def add_binds(self, binds: List[Any], proc_for_binds: Any = None, block: Any = None) -> 'Bind':
        self._binds.extend(binds)
        return self

    def __lshift__(self, str_val: str) -> 'Bind':
        return self

    @property
    def retryable(self) -> bool:
        return getattr(self, '_retryable', True)

    @retryable.setter
    def retryable(self, value: bool) -> None:
        self._retryable = value
