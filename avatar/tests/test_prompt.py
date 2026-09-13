from app.memory import MemoryRecord
from app.profile import ProfileBundle
from app.prompt import build_system_prompt


def test_prompt_separates_identity_from_inference() -> None:
    profile = ProfileBundle(
        sections={
            "identity.md": "Chris is an AI researcher.",
            "principles.md": "Prefer evidence.",
            "style.md": "Be direct.",
            "goals.md": "Build reliable systems.",
        }
    )
    memory = MemoryRecord(
        id=7,
        content="Chris chose a deterministic baseline for the first validation.",
        kind="decision",
        status="approved",
        source="decision log",
        confidence=1.0,
        created_at="2026-09-13T00:00:00+00:00",
        reviewed_at="2026-09-13T00:01:00+00:00",
    )

    prompt = build_system_prompt(profile, [memory])

    assert "Never claim to be Chris" in prompt
    assert "documented position" in prompt
    assert "MEMORY 7 [decision" in prompt
    assert "Chris chose a deterministic baseline" in prompt

