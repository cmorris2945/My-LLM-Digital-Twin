"""FastAPI entry point for the local Chris Avatar MVP."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import PROJECT_ROOT, settings
from app.memory import MemoryStore
from app.model import ModelUnavailableError, OllamaClient
from app.profile import load_profile
from app.prompt import build_system_prompt
from app.schemas import ChatRequest, ChatResponse, MemoryProposalRequest, MemoryResponse


app = FastAPI(
    title=settings.app_name,
    description=(
        "I am a PhD student at the University of Florida researching digital twin "
        "technology and artificial intelligence for healthcare and bioinformatics."
    ),
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "app" / "static"), name="static")

store = MemoryStore(settings.database_path)
model = OllamaClient(
    settings.ollama_url,
    settings.model,
    timeout_seconds=settings.request_timeout_seconds,
)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(PROJECT_ROOT / "app" / "static" / "index.html")


@app.get("/api/health")
def health() -> dict[str, object]:
    model_online = model.is_available()
    return {
        "status": "ready" if model_online else "model_offline",
        "model_online": model_online,
        "model": settings.model,
        "ollama_url": settings.ollama_url,
        "approved_memories": len(store.list(status="approved")),
        "pending_memories": len(store.list(status="pending")),
        "external_actions_enabled": False,
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    message = request.message.strip()
    relevant_memories = store.retrieve(message)
    profile = load_profile(settings.profile_dir)
    system_prompt = build_system_prompt(profile, relevant_memories)
    history = store.recent_turns(request.conversation_id)

    try:
        reply = model.chat(system_prompt, history, message)
    except ModelUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    store.add_turn(request.conversation_id, "user", message)
    store.add_turn(request.conversation_id, "assistant", reply)
    return ChatResponse(
        reply=reply,
        model=settings.model,
        retrieved_memory_ids=[memory.id for memory in relevant_memories],
    )


@app.get("/api/memories", response_model=list[MemoryResponse])
def list_memories(
    status: Literal["pending", "approved", "rejected"] | None = Query(default=None),
) -> list[dict[str, object]]:
    return [memory.to_dict() for memory in store.list(status=status)]


@app.post("/api/memories", response_model=MemoryResponse, status_code=201)
def propose_memory(request: MemoryProposalRequest) -> dict[str, object]:
    memory = store.propose(
        request.content,
        kind=request.kind,
        source=request.source,
        confidence=request.confidence,
    )
    return memory.to_dict()


def _review_memory(memory_id: int, status: Literal["approved", "rejected"]):
    try:
        return store.review(memory_id, status).to_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/memories/{memory_id}/approve", response_model=MemoryResponse)
def approve_memory(memory_id: int) -> dict[str, object]:
    return _review_memory(memory_id, "approved")


@app.post("/api/memories/{memory_id}/reject", response_model=MemoryResponse)
def reject_memory(memory_id: int) -> dict[str, object]:
    return _review_memory(memory_id, "rejected")
