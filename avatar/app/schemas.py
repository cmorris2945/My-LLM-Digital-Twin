"""HTTP request and response models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20_000)
    conversation_id: str = Field(default="main", min_length=1, max_length=100)


class ChatResponse(BaseModel):
    reply: str
    model: str
    retrieved_memory_ids: list[int]


class MemoryProposalRequest(BaseModel):
    content: str = Field(min_length=1, max_length=10_000)
    kind: Literal[
        "fact", "preference", "belief", "hypothesis", "decision", "correction", "style"
    ] = "fact"
    source: str = Field(default="user", min_length=1, max_length=200)
    confidence: float = Field(default=1.0, ge=0, le=1)


class MemoryResponse(BaseModel):
    id: int
    content: str
    kind: str
    status: str
    source: str
    confidence: float
    created_at: str
    reviewed_at: str | None

