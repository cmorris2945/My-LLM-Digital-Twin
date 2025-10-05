"""
Custom Exceptions for the LLM Engineering Domain

This module defines custom exceptions used throughout the application.
"""


class ImproperlyConfigured(Exception):
    """
    Raised when the application is not properly configured.
    
    Examples:
    - Missing required settings
    - Invalid configuration values
    - Missing required classes or methods
    """
    pass


class DatabaseError(Exception):
    """
    Raised when database operations fail.
    
    Examples:
    - Connection failures
    - Query errors
    - Data validation errors
    """
    pass


class CrawlerError(Exception):
    """
    Raised when web crawling operations fail.
    
    Examples:
    - Network timeouts
    - Invalid URLs
    - Parsing errors
    """
    pass
