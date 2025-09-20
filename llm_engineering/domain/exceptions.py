class LLMTwinException(Exception):
    """Base exception for LLM Twin project."""
    pass

class ImproperlyConfigured(LLMTwinException):
    """Raised when something is not configured properly."""
    pass