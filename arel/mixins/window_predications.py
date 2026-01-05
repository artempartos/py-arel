from typing import Any, Optional

class WindowPredicationsMixin:
    def over(self, expr: Optional[Any] = None) -> 'Over':
        from arel.nodes.window import Over
        return Over(self, expr)

