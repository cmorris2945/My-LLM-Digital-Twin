"""Human-governed persistent memory and conversation history."""

from __future__ import annotations

import math
import re
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


MemoryStatus = Literal["pending", "approved", "rejected"]
TOKEN_PATTERN = re.compile(r"[a-z0-9']+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "for",
    "from",
    "i",
    "in",
    "is",
    "it",
    "my",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "with",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def tokens(text: str) -> set[str]:
    return {
        token
        for token in TOKEN_PATTERN.findall(text.lower())
        if len(token) > 1 and token not in STOPWORDS
    }


@dataclass(frozen=True)
class MemoryRecord:
    id: int
    content: str
    kind: str
    status: str
    source: str
    confidence: float
    created_at: str
    reviewed_at: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class MemoryStore:
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'rejected')),
                    source TEXT NOT NULL,
                    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
                    created_at TEXT NOT NULL,
                    reviewed_at TEXT
                );

                CREATE TABLE IF NOT EXISTS conversation_turns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_memories_status
                    ON memories(status);
                CREATE INDEX IF NOT EXISTS idx_turns_conversation
                    ON conversation_turns(conversation_id, id);
                """
            )

    @staticmethod
    def _row_to_memory(row: sqlite3.Row) -> MemoryRecord:
        return MemoryRecord(
            id=row["id"],
            content=row["content"],
            kind=row["kind"],
            status=row["status"],
            source=row["source"],
            confidence=row["confidence"],
            created_at=row["created_at"],
            reviewed_at=row["reviewed_at"],
        )

    def propose(
        self,
        content: str,
        kind: str = "fact",
        source: str = "user",
        confidence: float = 1.0,
    ) -> MemoryRecord:
        clean_content = content.strip()
        if not clean_content:
            raise ValueError("Memory content cannot be empty")
        if not 0 <= confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO memories
                    (content, kind, status, source, confidence, created_at)
                VALUES (?, ?, 'pending', ?, ?, ?)
                """,
                (clean_content, kind.strip() or "fact", source.strip() or "user", confidence, utc_now()),
            )
            memory_id = int(cursor.lastrowid)
            row = connection.execute(
                "SELECT * FROM memories WHERE id = ?", (memory_id,)
            ).fetchone()
        return self._row_to_memory(row)

    def review(self, memory_id: int, status: Literal["approved", "rejected"]) -> MemoryRecord:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE memories
                SET status = ?, reviewed_at = ?
                WHERE id = ? AND status = 'pending'
                """,
                (status, utc_now(), memory_id),
            )
            if cursor.rowcount != 1:
                raise KeyError(f"Pending memory {memory_id} was not found")
            row = connection.execute(
                "SELECT * FROM memories WHERE id = ?", (memory_id,)
            ).fetchone()
        return self._row_to_memory(row)

    def list(self, status: MemoryStatus | None = None) -> list[MemoryRecord]:
        with self._connect() as connection:
            if status is None:
                rows = connection.execute(
                    "SELECT * FROM memories ORDER BY id DESC"
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT * FROM memories WHERE status = ? ORDER BY id DESC",
                    (status,),
                ).fetchall()
        return [self._row_to_memory(row) for row in rows]

    def retrieve(self, query: str, limit: int = 6) -> list[MemoryRecord]:
        approved = self.list(status="approved")
        query_tokens = tokens(query)
        if not query_tokens:
            return approved[:limit]

        ranked: list[tuple[float, MemoryRecord]] = []
        for memory in approved:
            memory_tokens = tokens(memory.content)
            overlap = len(query_tokens & memory_tokens)
            if not overlap:
                continue
            score = (overlap / math.sqrt(max(len(memory_tokens), 1))) * memory.confidence
            ranked.append((score, memory))

        ranked.sort(key=lambda item: (item[0], item[1].id), reverse=True)
        return [memory for _, memory in ranked[:limit]]

    def add_turn(self, conversation_id: str, role: str, content: str) -> None:
        if role not in {"user", "assistant"}:
            raise ValueError("Role must be user or assistant")
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO conversation_turns
                    (conversation_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (conversation_id, role, content.strip(), utc_now()),
            )

    def recent_turns(self, conversation_id: str, limit: int = 12) -> list[dict[str, str]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT role, content
                FROM conversation_turns
                WHERE conversation_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (conversation_id, limit),
            ).fetchall()
        return [dict(row) for row in reversed(rows)]

