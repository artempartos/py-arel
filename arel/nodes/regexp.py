from arel.nodes.binary import Binary

class Regexp(Binary):
    def __init__(self, left: any, right: any, case_sensitive: bool = True):
        super().__init__(left, right)
        self.case_sensitive = case_sensitive

class NotRegexp(Regexp): pass

