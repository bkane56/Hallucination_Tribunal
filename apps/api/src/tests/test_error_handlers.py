from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.error_handlers import register_error_handlers
from src.core.exceptions import NotFoundError, TribunalError


def _client_with_handlers() -> TestClient:
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/tribunal-error")
    def _raise_tribunal_error() -> None:
        raise TribunalError("Something failed.", details={"stage": "retrieval"})

    @app.get("/not-found")
    def _raise_not_found() -> None:
        raise NotFoundError("Document not found.")

    return TestClient(app, raise_server_exceptions=False)


def test_tribunal_error_returns_structured_payload() -> None:
    response = _client_with_handlers().get("/tribunal-error")
    assert response.status_code == 500
    payload = response.json()
    assert payload["error"]["code"] == "tribunal_error"
    assert payload["error"]["message"] == "Something failed."
    assert payload["error"]["details"] == {"stage": "retrieval"}


def test_not_found_error_status_code() -> None:
    response = _client_with_handlers().get("/not-found")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
