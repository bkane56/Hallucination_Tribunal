from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_readiness_returns_provider_configuration() -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["providers"]["llm"] == "ollama"
    assert payload["providers"]["embedding"] == "local"
    assert payload["providers"]["vector_db"] == "chromadb"
    assert payload["directories_ready"] is True
    assert "uploads" in payload["data_directories"]
