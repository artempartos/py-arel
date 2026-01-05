class ArelError(Exception): pass
class EmptyJoinError(ArelError): pass

class BindError(ArelError):
    def __init__(self, message: str, sql: str = None):
        if sql:
            super().__init__(f"{message} in: {repr(sql)}")
        else:
            super().__init__(message)

class UnsupportedVisitError(ArelError):
    def __init__(self, obj):
        super().__init__(f"Unsupported visit: {obj}")

