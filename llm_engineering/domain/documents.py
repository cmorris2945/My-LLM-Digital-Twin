"""
Document Models for the Digital Twin System

This module re-exports all document models from types.py
for backward compatibility and easy importing.
"""

# Import all document classes from types.py
from .types import (
    DataCategory,
    Document,
    RepositoryDocument,
    PostDocument, 
    ArticleDocument,
    UserDocument
)

# Import base class for direct access
from .base.nosql import NoSQLBaseDocument

# Export everything for easy importing
__all__ = [
    'NoSQLBaseDocument',
    'DataCategory',
    'Document',
    'RepositoryDocument', 
    'PostDocument', 
    'ArticleDocument',
    'UserDocument'
]
