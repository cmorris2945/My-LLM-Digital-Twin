"""
Domain Types and Document Models

This module contains type definitions, enums, and document models
used throughout the domain layer of the application.
"""

from abc import ABC
from typing import Optional
from enum import StrEnum

from pydantic import UUID4, Field

from .base.nosql import NoSQLBaseDocument


class DataCategory(StrEnum):
    """
    Categories of data that can be crawled and stored.
    
    These correspond to MongoDB collection names where
    different types of content are stored.
    """
    # Training data categories
    PROMPT = "prompt"
    QUERIES = "queries"
    INSTRUCT_DATASET_SAMPLES = "instruct_dataset_samples"
    INSTRUCT_DATASET = "instruct_dataset"
    PREFERENCE_DATASET_SAMPLES = "preference_dataset_samples"
    PREFERENCE_DATASET = "preference_dataset"

    # Content categories
    POSTS = "posts"
    ARTICLES = "articles"  
    REPOSITORIES = "repositories"


class Document(NoSQLBaseDocument, ABC):  
    """
    Abstract base class for all content documents.
    
    This represents any piece of content that can be crawled
    (repositories, posts, articles). All content is linked to
    a user (author) and contains platform information.
    """
    content: dict                                           
    platform: str                                          
    author_id: UUID4 = Field(alias="author_id")           
    author_full_name: str = Field(alias="author_full_name")


class RepositoryDocument(Document):
    """
    Represents a code repository (GitHub, GitLab, etc.).
    
    Contains information about code repositories including
    README content, repository metadata, and links.
    """
    name: str    # Repository name
    link: str    # Repository URL

    class Settings:
        name = DataCategory.REPOSITORIES


class PostDocument(Document):
    """
    Represents social media posts (LinkedIn, Twitter, etc.).
    
    Contains social media posts, professional updates,
    and other short-form content.
    """
    image: Optional[str] = None    # Image URL if post contains image
    link: str | None = None        # Link to original post

    class Settings:
        name = DataCategory.POSTS


class ArticleDocument(Document):
    """
    Represents long-form articles (Medium, blogs, etc.).
    
    Contains blog posts, technical articles, and other
    long-form written content.
    """
    link: str    # Article URL

    class Settings:
        name = DataCategory.ARTICLES


class UserDocument(NoSQLBaseDocument):
    """
    Represents a user in the system.
    
    This is the main entity that owns all other content.
    All crawled content is linked to a user.
    """
    first_name: str
    last_name: str

    class Settings:
        name = "users"  

    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"


# Export all classes for easy importing
__all__ = [
    'DataCategory',
    'Document',
    'RepositoryDocument', 
    'PostDocument', 
    'ArticleDocument',
    'UserDocument'
]
