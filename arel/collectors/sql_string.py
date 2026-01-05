from __future__ import annotations
from typing import Any, Callable, Optional, List
from arel.collectors.plain_string import PlainString

class SQLString(PlainString):
    def __init__(self):
        super().__init__()
        self.preparable = True
        self.retryable = True
        self._bind_index = 1

    def add_bind(self, bind: Any, block: Callable[[int], str]) -> 'SQLString':
        self << block(self._bind_index)
        self._bind_index += 1
        return self

    def add_binds(self, binds: List[Any], proc_for_binds: Optional[Callable] = None, block: Optional[Callable[[int], str]] = None) -> 'SQLString':
        placeholders = []
        for _ in binds:
            placeholders.append(block(self._bind_index))
            self._bind_index += 1
        self << ", ".join(placeholders)
        return self

