from typing import Any, Optional
from arel.nodes.binary import Binary, Join

class InnerJoin(Join): pass
class OuterJoin(Join): pass
class FullOuterJoin(Join): pass
class RightOuterJoin(Join): pass

class StringJoin(Join):
    def __init__(self, left: Any, right: Any = None):
        super().__init__(left, right)

class LeadingJoin(InnerJoin): pass
