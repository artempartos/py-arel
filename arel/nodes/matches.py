from arel.nodes.binary import Binary
from arel.nodes.casted import build_quoted

class Matches(Binary):
    def __init__(self, left: any, right: any, escape: any = None, case_sensitive: bool = False):
        super().__init__(left, right)
        self.escape = build_quoted(escape) if escape else None
        self.case_sensitive = case_sensitive

class DoesNotMatch(Matches): pass

