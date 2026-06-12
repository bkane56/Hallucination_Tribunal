from pathlib import Path

import pytest
from pydantic import ValidationError

from hallucination_tribunal.core.config import Settings, _api_root, _monorepo_root


def test_settings_max_upload_bytes():
    settings = Settings(max_upload_size_mb=25, openai_api_key="test-key")
    assert settings.max_upload_bytes == 25 * 1024 * 1024


def test_settings_defaults():
    assert Settings.model_fields["llm_provider"].default == "openai"
    assert Settings.model_fields["embedding_provider"].default == "openai"
    settings = Settings(openai_api_key="test-key", retrieval_mode="hybrid")
    assert settings.retrieval_mode == "hybrid"


def test_settings_requires_openai_api_key_when_using_openai():
    with pytest.raises(ValidationError):
        Settings(openai_api_key="", llm_provider="openai")


def test_settings_cors_origins():
    settings = Settings(
        frontend_url="https://app.example.com",
        cors_allowed_origins="https://staging.example.com, https://preview.example.com",
        openai_api_key="test-key",
    )
    assert "https://app.example.com" in settings.cors_origins
    assert "http://localhost:3000" in settings.cors_origins
    assert "https://staging.example.com" in settings.cors_origins
    assert "https://preview.example.com" in settings.cors_origins


def test_api_root_points_at_package_tree():
    api_root = _api_root()
    assert (api_root / "src" / "hallucination_tribunal").is_dir()


def test_monorepo_root_when_data_present():
    mono = _monorepo_root()
    if mono is None:
        return
    assert (mono / "data").is_dir()
    assert (mono / "apps" / "api").is_dir()


def test_settings_project_root_without_monorepo(monkeypatch):
    monkeypatch.setattr(
        "hallucination_tribunal.core.config._monorepo_root",
        lambda: None,
    )
    settings = Settings(openai_api_key="test-key")
    assert settings.project_root == _api_root()


def test_settings_vercel_defaults(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    settings = Settings(openai_api_key="test-key")
    assert settings.storage_root == "/tmp/hallucination-tribunal"
    assert settings.api_root_path == "/server"
    assert settings.resolve_path("./data/chroma") == Path(
        "/tmp/hallucination-tribunal/chroma"
    )
