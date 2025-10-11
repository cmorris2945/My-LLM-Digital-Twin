"""
Document Models for the Digital Twin System

This module re-exports all document models from types.py
for backward compatibility and easy importing.


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
"""

from abc import ABC
from typing import Optional

from pydantic import UUID4, Field

from .base import NoSQLBaseDocument
from .types import DataCategory


class UserDocument(NoSQLBaseDocument):
    first_name: str
    last_name: str

    class Settings:
        name = "users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Document(NoSQLBaseDocument, ABC):
    content: dict
    platform: str
    author_id: UUID4 = Field(alias="author_id")
    author_full_name: str = Field(alias="author_full_name")


class RepositoryDocument(Document):
    name: str
    link: str

    class Settings:
        name = DataCategory.REPOSITORIES


class PostDocument(Document):
    image: Optional[str] = None
    link: str | None = None

    class Settings:
        name = DataCategory.POSTS


class ArticleDocument(Document):
    link: str

    class Settings:
        name = DataCategory.ARTICLES
