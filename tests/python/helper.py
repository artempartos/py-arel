# Compatibility alias for existing imports
# This file re-exports from tests.helper to maintain backward compatibility
from tests.helper import MockEngine, MockConnection, must_be_like

__all__ = ['MockEngine', 'MockConnection', 'must_be_like']

