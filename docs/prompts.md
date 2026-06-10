# Prompts

Prompt templates live in `apps/api/src/hallucination_tribunal/prompts/`:

| File | Role |
|---|---|
| witness.yaml | Initial grounded answer |
| claim_extraction.yaml | Factual claim decomposition |
| prosecutor.yaml | Adversarial objection generation |
| judge.yaml | Per-claim verdict assignment |
| final_revision.yaml | Final user-facing answer |

Each prompt includes system instructions, grounding rules, and output schema.
