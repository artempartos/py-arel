from __future__ import annotations
from typing import Any, List

class SubstituteBinds:
    def __init__(self, quoter: Any, delegate: Any):
        self.quoter = quoter
        self.delegate = delegate

    def __lshift__(self, str_val: str) -> 'SubstituteBinds':
        self.delegate << str_val
        return self

    def add_bind(self, bind: Any, block: Any = None) -> 'SubstituteBinds':
        self.delegate << self.quoter.quote(bind.value_for_database() if hasattr(bind, 'value_for_database') else bind)
        return self

    def add_binds(self, binds: List[Any], proc_for_binds: Any = None, block: Any = None) -> 'SubstituteBinds':
        for i, bind in enumerate(binds):
            if i > 0:
                self.delegate << ", "
            self.add_bind(bind)
        return self

    @property
    def value(self) -> Any:
        return self.delegate.value
