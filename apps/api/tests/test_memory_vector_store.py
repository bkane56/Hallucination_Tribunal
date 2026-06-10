from hallucination_tribunal.core.providers.memory_vector_store import InMemoryVectorStore
from hallucination_tribunal.models.domain import Chunk


def test_in_memory_vector_store_query_filters_by_document():
    store = InMemoryVectorStore()
    chunks = [
        Chunk(chunk_id="a", document_id="doc-1", chunk_index=0, text="alpha"),
        Chunk(chunk_id="b", document_id="doc-2", chunk_index=0, text="beta"),
    ]
    embeddings = [[1.0, 0.0], [0.0, 1.0]]
    metadatas = [
        {"document_id": "doc-1", "filename": "one.md"},
        {"document_id": "doc-2", "filename": "two.md"},
    ]
    store.upsert_chunks(chunks, embeddings, metadatas)

    results = store.query([1.0, 0.0], top_k=2, document_ids=["doc-1"])

    assert len(results) == 1
    assert results[0][0] == "a"
