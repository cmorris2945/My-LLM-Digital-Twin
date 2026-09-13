from pathlib import Path

import pytest

from app.memory import MemoryStore


@pytest.fixture
def store(tmp_path: Path) -> MemoryStore:
    return MemoryStore(tmp_path / "avatar.db")


def test_pending_memory_is_not_retrieved(store: MemoryStore) -> None:
    candidate = store.propose("Chris prefers reproducible scientific systems.")

    assert candidate.status == "pending"
    assert store.retrieve("What does Chris think about reproducibility?") == []


def test_only_approved_memory_is_retrieved(store: MemoryStore) -> None:
    candidate = store.propose(
        "Chris prefers reproducible scientific systems.", kind="preference"
    )
    approved = store.review(candidate.id, "approved")

    results = store.retrieve("What does Chris prefer about reproducible systems?")

    assert approved.status == "approved"
    assert [memory.id for memory in results] == [candidate.id]


def test_rejected_memory_cannot_be_approved_later(store: MemoryStore) -> None:
    candidate = store.propose("This statement should not become identity.")
    store.review(candidate.id, "rejected")

    with pytest.raises(KeyError):
        store.review(candidate.id, "approved")


def test_conversation_history_keeps_original_order(store: MemoryStore) -> None:
    store.add_turn("session", "user", "First")
    store.add_turn("session", "assistant", "Second")
    store.add_turn("session", "user", "Third")

    assert store.recent_turns("session", limit=2) == [
        {"role": "assistant", "content": "Second"},
        {"role": "user", "content": "Third"},
    ]

