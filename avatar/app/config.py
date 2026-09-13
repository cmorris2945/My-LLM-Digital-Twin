"""Environment-driven application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _resolve_path(value: str, default: Path) -> Path:
    raw = Path(value).expanduser() if value else default
    return raw if raw.is_absolute() else (PROJECT_ROOT / raw).resolve()


@dataclass(frozen=True)
class Settings:
    app_name: str
    model: str
    ollama_url: str
    database_path: Path
    profile_dir: Path
    request_timeout_seconds: float


def load_settings() -> Settings:
    return Settings(
        app_name=os.getenv("AVATAR_APP_NAME", "Chris Avatar"),
        model=os.getenv("AVATAR_MODEL", "qwen3:8b"),
        ollama_url=os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/"),
        database_path=_resolve_path(
            os.getenv("AVATAR_DATABASE_PATH", ""), PROJECT_ROOT / "data" / "avatar.db"
        ),
        profile_dir=_resolve_path(
            os.getenv("AVATAR_PROFILE_DIR", ""), PROJECT_ROOT / "profile"
        ),
        request_timeout_seconds=float(
            os.getenv("AVATAR_REQUEST_TIMEOUT_SECONDS", "120")
        ),
    )


settings = load_settings()

