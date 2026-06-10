from hallucination_tribunal.tribunal.prompts import format_context, load_prompt
from hallucination_tribunal.models.domain import RetrievedSource


def test_load_witness_prompt():
    prompt = load_prompt("witness")
    assert "Witness" in prompt["system"]
    assert "output_schema" in prompt


def test_format_context_empty():
    assert "No retrieved evidence" in format_context([])


def test_format_context_with_source():
    sources = [
        RetrievedSource(
            chunk_id="c1",
            document_id="d1",
            filename="policy.md",
            page_number=2,
            section_title="Rules",
            text="Approval required.",
            similarity_score=0.8,
        )
    ]
    text = format_context(sources)
    assert "policy.md" in text
    assert "Approval required." in text
