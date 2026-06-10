from hallucination_tribunal.core.config import Settings


def test_settings_max_upload_bytes():
    settings = Settings(max_upload_size_mb=25)
    assert settings.max_upload_bytes == 25 * 1024 * 1024


def test_settings_defaults():
    settings = Settings()
    assert settings.llm_provider == "ollama"
    assert settings.embedding_provider == "local"
    assert settings.retrieval_mode == "hybrid"
