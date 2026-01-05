import re

class MockConnection:
    def quote(self, value):
        if value is None: return "NULL"
        if isinstance(value, bool): return "'t'" if value else "'f'"  # Ruby style: 't' for True, 'f' for False
        if isinstance(value, (int, float)): return str(value)
        escaped = str(value).replace("'", "''")
        return f"'{escaped}'"

    def quote_table_name(self, name):
        return f'"{name}"'

    def quote_column_name(self, name):
        return f'"{name}"'

class MockEngine:
    def __init__(self, visitor_class):
        self.connection = MockConnection()
        self.connection.visitor = visitor_class(self.connection)


def must_be_like(actual, expected):
    """
    Helper function similar to Ruby's must_be_like.
    Normalizes whitespace in SQL strings before comparison.
    Replaces multiple whitespace characters with a single space and strips leading/trailing whitespace.

    Usage in tests:
        from tests.helper import must_be_like
        must_be_like(query.to_sql(), "SELECT * FROM users")
    """
    normalized_actual = re.sub(r'\s+', ' ', str(actual)).strip()
    normalized_expected = re.sub(r'\s+', ' ', str(expected)).strip()
    assert normalized_actual == normalized_expected, \
        f"Expected SQL to match (normalized):\n  Expected: {normalized_expected}\n  Actual:   {normalized_actual}"
