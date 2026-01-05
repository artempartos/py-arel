class PlainString:
    def __init__(self):
        self._str = ""

    @property
    def value(self) -> str:
        return self._str

    def __lshift__(self, str_val: str) -> 'PlainString':
        self._str += str_val
        return self

