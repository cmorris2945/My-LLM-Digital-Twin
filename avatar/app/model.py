"""Small Ollama adapter with no dependency on GPT or Claude."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ModelUnavailableError(RuntimeError):
    """Raised when the configured local model service cannot answer."""


class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout_seconds: float = 120):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def is_available(self) -> bool:
        request = Request(f"{self.base_url}/api/tags", method="GET")
        try:
            with urlopen(request, timeout=2):
                return True
        except (HTTPError, URLError, TimeoutError):
            return False

    def chat(
        self,
        system_prompt: str,
        history: list[dict[str, str]],
        user_message: str,
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": user_message},
        ]
        body = json.dumps(
            {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.35},
            }
        ).encode("utf-8")
        request = Request(
            f"{self.base_url}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ModelUnavailableError(
                f"Ollama returned HTTP {exc.code}: {detail[:300]}"
            ) from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ModelUnavailableError(
                "The local model is unavailable. Start Ollama and pull the configured model."
            ) from exc

        try:
            content = payload["message"]["content"].strip()
        except (KeyError, TypeError, AttributeError) as exc:
            raise ModelUnavailableError("Ollama returned an unexpected response") from exc
        if not content:
            raise ModelUnavailableError("Ollama returned an empty response")
        return content

