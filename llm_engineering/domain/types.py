from abc import  ABC
from typing import Optional

from pydantic import UUID4, Field

from .base import NoSQLBaseDocument
from .types import DataCategory

from enum import StrEnum

class DataCategory(StrEnum):
    PROMPT = "prompt"
    QUERIES = "queries"
    INSTRUCT_DATASET_SAMPLES = "instruct_dataset_samples"
    INSTRUCT_DATASET = "instruct_dataset"
    PREFERENCE_DATASET_SAMPLES = "preference_dataset_samples"
    PREFERENCE_DATASET = "preference_dataset"

    POSTS = "posts"
    ARTICLES = "atricles"
    REPOSITORIES = "repositories"

    class Documnet(NoSQLBaseDocument,ABC):
        content: dict
        platform: str
        author_id: UUID = Field(alias="author_is")
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

    class UserDocument(NoSQLBaseDocument):
        first_name: str
        last_name: str

        class Settings:
            name: "users"

        @property
        def full_name(self):
            return f"{self.first_name} {self.last_name}"
        
        




