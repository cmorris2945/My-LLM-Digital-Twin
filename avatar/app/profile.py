"""Load the operator-reviewed identity documents used by the avatar."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROFILE_FILES = (
    "identity.md",
    "principles.md",
    "style.md",
    "goals.md",
)


@dataclass(frozen=True)
class ProfileBundle:
    sections: dict[str, str]

    def as_prompt_context(self) -> str:
        blocks = []
        for filename in PROFILE_FILES:
            content = self.sections.get(filename, "").strip()
            if content:
                blocks.append(f"SOURCE: profile/{filename}\n{content}")
        return "\n\n".join(blocks)


def load_profile(directory: Path) -> ProfileBundle:
    sections: dict[str, str] = {}
    for filename in PROFILE_FILES:
        path = directory / filename
        sections[filename] = path.read_text(encoding="utf-8") if path.exists() else ""
    return ProfileBundle(sections=sections)

