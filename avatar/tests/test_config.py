from pathlib import Path

from app.config import _load_local_env


def test_local_env_does_not_override_existing_environment(
    tmp_path: Path, monkeypatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "AVATAR_TEST_EXISTING=file-value\nAVATAR_TEST_NEW=new-value\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("AVATAR_TEST_EXISTING", "process-value")
    monkeypatch.delenv("AVATAR_TEST_NEW", raising=False)

    _load_local_env(env_file)

    assert __import__("os").environ["AVATAR_TEST_EXISTING"] == "process-value"
    assert __import__("os").environ["AVATAR_TEST_NEW"] == "new-value"

