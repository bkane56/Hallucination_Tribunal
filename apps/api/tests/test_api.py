import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_readiness_check(client, monkeypatch):
    async def ollama_ok():
        return True

    monkeypatch.setattr(
        "hallucination_tribunal.api.routes._ollama_reachable",
        ollama_ok,
    )
    response = await client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["directories_ready"] is True
    assert data["providers"]["ollama_reachable"] is True


@pytest.mark.asyncio
async def test_list_documents_empty(client):
    response = await client.get("/documents")
    assert response.status_code == 200
    assert "documents" in response.json()


@pytest.mark.asyncio
async def test_corpus_overview(client):
    response = await client.get("/corpus/overview")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert "samples" in data
    assert "categories" in data
    assert len(data["samples"]) > 0


@pytest.mark.asyncio
async def test_upload_invalid_type(client):
    files = {"file": ("bad.exe", b"binary", "application/octet-stream")}
    response = await client.post("/documents/upload", files=files)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_evaluation_runs_empty(client):
    response = await client.get("/evaluations/runs")
    assert response.status_code == 200
    assert "runs" in response.json()


@pytest.mark.asyncio
async def test_rebuild_index_empty(client):
    response = await client.post("/documents/rebuild-index")
    assert response.status_code == 200
    assert "rebuilt_count" in response.json()
    content = b"# Test Policy\nExternal LLM APIs require approval."
    files = {"file": ("policy.md", content, "text/markdown")}
    upload = await client.post("/documents/upload", files=files)
    assert upload.status_code == 200
    doc = upload.json()
    assert doc["status"] == "indexed"
    assert doc["chunk_count"] > 0

    doc_id = doc["document_id"]
    get_resp = await client.get(f"/documents/{doc_id}")
    assert get_resp.status_code == 200

    delete_resp = await client.delete(f"/documents/{doc_id}")
    assert delete_resp.status_code == 200

    missing = await client.get(f"/documents/{doc_id}")
    assert missing.status_code == 404
