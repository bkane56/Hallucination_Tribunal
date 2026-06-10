from hallucination_tribunal.retrieval.service import reciprocal_rank_fusion


def test_reciprocal_rank_fusion():
    list_a = ["a", "b", "c"]
    list_b = ["b", "a", "d"]
    fused = reciprocal_rank_fusion([list_a, list_b])
    ids = [item for item, _ in fused]
    assert "a" in ids
    assert "b" in ids
    assert ids[0] in {"a", "b"}
