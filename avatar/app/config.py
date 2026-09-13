"""Environment-driven application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_local_env(path: Path) -> None:
    """Load simple KEY=VALUE entries without overriding the process environment."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            os.environ.setdefault(key, value)


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
    _load_local_env(PROJECT_ROOT / ".env")
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
