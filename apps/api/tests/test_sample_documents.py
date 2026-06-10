import pytest


@pytest.mark.asyncio
async def test_list_sample_documents(client):
    response = await client.get("/documents/samples")
    assert response.status_code == 200
    data = response.json()
    assert "samples" in data
    assert "categories" in data
    assert len(data["samples"]) >= 10
    assert data["samples"][0]["sample_id"]
    assert data["samples"][0]["title"]
    assert data["samples"][0]["filename"].startswith("sample-")


@pytest.mark.asyncio
async def test_import_sample_document(client):
    response = await client.post(
        "/documents/samples/import",
        json={"sample_ids": ["nist-ai-rmf"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["imported"]) == 1
    assert data["imported"][0]["status"] == "indexed"
    assert data["imported"][0]["chunk_count"] > 0

    repeat = await client.post(
        "/documents/samples/import",
        json={"sample_ids": ["nist-ai-rmf"]},
    )
    assert repeat.status_code == 200
    repeat_data = repeat.json()
    assert len(repeat_data["skipped"]) == 1
    assert repeat_data["skipped"][0]["message"] == "Already in corpus"

    list_resp = await client.get("/documents/samples")
    nist = next(
        sample for sample in list_resp.json()["samples"] if sample["sample_id"] == "nist-ai-rmf"
    )
    assert nist["already_imported"] is True


@pytest.mark.asyncio
async def test_import_unknown_sample(client):
    response = await client.post(
        "/documents/samples/import",
        json={"sample_ids": ["not-a-real-sample"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["errors"]) == 1
    assert "Unknown sample document" in data["errors"][0]["message"]


@pytest.mark.asyncio
async def test_import_sample_documents_requires_ids(client):
    response = await client.post("/documents/samples/import", json={"sample_ids": []})
    assert response.status_code == 422
