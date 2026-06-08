# The Hallucination Tribunal - Project Requirements

## IMPORTANT NOTES:
- This project will be uploaded to my personal webpage 'brianekane.com' (later).  This webpage will be part of my resume to aquire a new job in Frontend/Backend/AI engineering
- This project is a deomonstration project for Hiring Managers and Senior Engineers or Principle Engineers.  Keep that in mind when structuring and implementing this code.  It should be consise and functional as well as documented appropriately.
- Functional code should be tested at a minimum of 90% for all logic and UI displays.

## 1. Project Overview

The Hallucination Tribunal is a RAG-powered AI application designed to answer user questions from a controlled document corpus and then subject each answer to an adversarial review process.

The goal is not simply to retrieve documents and generate an answer. The goal is to demonstrate a production-aware RAG system that can:

- Retrieve relevant source material.
- Generate a grounded answer.
- Extract factual claims from the answer.
- Challenge those claims against retrieved evidence.
- Judge whether each claim is supported, partially supported, unsupported, or contradicted.
- Present the final answer with transparent citations and a verdict.

This project is intended as a portfolio-quality AI engineering application that demonstrates RAG architecture, agent orchestration, hallucination mitigation, document-grounding, evaluation, observability, and thoughtful user experience.

## 2. Project Name

The Hallucination Tribunal

### Github Repo

https://github.com/bkane56/Hallucination_Tribunal.git

## 3. Core Concept

The system should behave like a courtroom for AI-generated answers.

There are three primary AI roles:

### 3.1 The Witness

The Witness generates the initial answer using retrieved context from the document corpus.

The Witness must:
- Answer only from retrieved documents.
- Cite supporting source chunks.
- Avoid claims that are not grounded in retrieved evidence.
- State uncertainty when the evidence is incomplete.
- Avoid fabricating details.

### 3.2 The Prosecutor

The Prosecutor challenges the Witness answer.

The Prosecutor must:
- Extract individual factual claims from the Witness answer.
- Compare each claim against the retrieved context.
- Identify unsupported, exaggerated, vague, or contradicted claims.
- Explain why a claim is questionable.
- Suggest what evidence would be required to support the claim.

### 3.3 The Judge

The Judge produces the final verdict.

The Judge must:
- Review the Witness answer, the Prosecutor objections, and the source evidence.
- Assign a verdict to each claim:
  - Supported
  - Partially Supported
  - Unsupported
  - Contradicted
  - Not Enough Evidence
- Produce an overall answer reliability score.
- Recommend whether the final answer should be accepted, revised, or rejected.
- Produce a final user-facing answer that removes or qualifies unsupported claims.

## 4. Target Users

Primary users:
- Software engineering hiring managers.
- AI engineering recruiters.
- Senior engineers evaluating RAG maturity.
- Developers learning how hallucination mitigation works.
- Internal enterprise teams evaluating whether RAG output can be trusted.

Secondary users:
- Students learning RAG.
- Compliance-minded teams.
- Product managers evaluating AI answer quality.

## 5. Portfolio Goals

This project should demonstrate:

- Practical RAG implementation.
- Hybrid retrieval strategy.
- Agentic review workflow.
- Source citation handling.
- Claim-level verification.
- LLM evaluation design.
- User-facing explainability.
- Testable AI behavior.
- Clean production-style architecture.
- Security and privacy awareness.
- Clear documentation suitable for employers.

## 6. Recommended Tech Stack

### 6.1 Frontend

Use Next.js with TypeScript.

Requirements:
- Use React functional components.
- Use TypeScript throughout the frontend.
- Use a clean component-based architecture.
- Use accessible UI components.
- Support responsive layout.
- Use a simple, professional visual design with a courtroom theme.

Suggested UI framework:
- Tailwind CSS
- shadcn/ui

### 6.2 Backend

Use Python with FastAPI.
Use Pydantic structured output where relevent.

Requirements:
- Python 3.12 or 3.13.
- Use uv for Python package and runtime management.
- Do not use pip directly for dependency management.
- Expose REST endpoints for document ingestion, question answering, corpus management, and evaluation.
- Use Pydantic models for request and response schemas.

### 6.3 Package Management

Frontend:
- Use yarn.
- Do not use npm.

Backend:
- Use uv.
- Do not use pip.

### 6.4 Vector Database

Use one of the following:

Preferred local/demo option:
- ChromaDB


Requirements:
- Store document chunks.
- Store metadata for each chunk.
- Support retrieval by source, document type, and topic.
- Support deleting and rebuilding the index.

### 6.5 Embeddings

Support at least one local or low-cost embedding model.

Recommended:
- sentence-transformers/all-MiniLM-L6-v2 for local development.
- OpenAI text-embedding-3-small as optional hosted embedding provider.

The application should be designed so embedding providers can be swapped through configuration.

### 6.6 LLM Providers

Support provider abstraction.

Recommended:
- Ollama for local models.
- OpenAI as an optional provider.
- Anthropic as an optional provider if desired later.

The default demo should be able to run locally using Ollama to show privacy-aware architecture.

## 7. Environment Variables

Create a `.env.example` file with sanitized placeholder values.

Example format:

```env
APP_ENV=development
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000

LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2

OPENAI_API_KEY=sk-********
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

VECTOR_DB_PROVIDER=chromadb
CHROMA_PERSIST_DIRECTORY=./data/chroma

MAX_UPLOAD_SIZE_MB=25
CHUNK_SIZE=900
CHUNK_OVERLAP=150

LOG_LEVEL=info
```

Any documentation or generated files that mention secrets must show only the beginning of a value followed by asterisks.

## 8. Main User Flow

### 8.1 Document Upload

The user uploads one or more documents.

Supported formats:
- PDF
- Markdown
- TXT
- DOCX
- HTML

The system should:
- Extract text.
- Preserve source metadata.
- Chunk the document.
- Generate embeddings.
- Store chunks in the vector database.
- Display ingestion status.

### 8.2 Ask a Question

The user enters a question.

The system should:
- Retrieve relevant chunks.
- Generate an initial answer using the Witness role.
- Extract answer claims.
- Run Prosecutor review.
- Run Judge verdict.
- Return a final response with:
  - Answer
  - Citations
  - Claim table
  - Objections
  - Verdict
  - Reliability score

### 8.3 Review Tribunal Results

The user should see:

- Final Answer
- Overall Verdict
- Reliability Score
- Claims Reviewed
- Supported Claims
- Unsupported Claims
- Contradicted Claims
- Source Citations
- Prosecutor Objections
- Judge Explanation

## 9. Required Pages

### 9.1 Home Page

Purpose:
- Explain the project.
- Show the courtroom metaphor.
- Provide a clear call to action.

Content:
- Project description.
- Why hallucination detection matters.
- Short architecture summary.
- Link to upload documents.
- Link to ask questions.
- Link to evaluation dashboard.

### 9.2 Corpus Page

Purpose:
- Manage uploaded documents.

Features:
- Upload documents.
- View uploaded documents.
- View chunk counts.
- Delete documents.
- Rebuild index.
- Show ingestion errors.

### 9.3 Tribunal Page

Purpose:
- Main question-answering interface.

Features:
- Question input.
- Optional filters by document or category.
- Run Tribunal button.
- Display retrieval context.
- Display Witness answer.
- Display Prosecutor objections.
- Display Judge verdict.
- Display final revised answer.

#### Claim Docket Table

The Tribunal Page must include a claim-level review table called the "Claim Docket."

The Claim Docket should display every factual claim extracted from the Witness Answer and show how the Judge ruled on that claim.

Required columns:

| Column | Description |
|---|---|
| Claim | The factual claim extracted from the Witness Answer |
| Verdict | Supported, Partially Supported, Unsupported, Contradicted, or Not Enough Evidence |
| Confidence | Numeric confidence score from 0.00 to 1.00 |
| Evidence | Source document, page, section, or chunk supporting the verdict |
| Prosecutor Objection | Short explanation of any objection |
| Judge's Reasoning | Final explanation for the verdict |
| Recommended Revision | Suggested correction if the claim is weak or unsupported |

Verdict colors must follow the project color scheme:

| Verdict | Color |
|---|---|
| Supported | Verdict Teal, `#0F766E` |
| Partially Supported | Objection Amber, `#F59E0B` |
| Not Enough Evidence | Slate Gray, `#6B7280` |
| Unsupported | Overruled Red, `#B91C1C` |
| Contradicted | Dark Red, `#7F1D1D` |

The Claim Docket must be sortable by verdict and confidence score.

The user should be able to expand each row to see:
- The original sentence from the Witness Answer.
- Retrieved evidence used to evaluate the claim.
- Any contradictory evidence.
- The Prosecutor's objection.
- The Judge's final reasoning.

### 9.4 Evaluation Dashboard

Purpose:
- Demonstrate RAG quality measurement.

Features:
- Saved test questions.
- Expected source documents.
- Expected answer notes.
- Retrieval score.
- Faithfulness score.
- Unsupported claim count.
- Verdict distribution.
- Run all evaluations button.

### 9.5 Architecture Page

Purpose:
- Explain how the application works.

Features:
- Architecture diagram.
- Retrieval pipeline explanation.
- Agent workflow explanation.
- Data privacy notes.
- Limitations.

## 10. Backend API Requirements

### 10.1 Health Check

Endpoint:

```http
GET /health
```

Response:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### 10.2 Upload Document

Endpoint:

```http
POST /documents/upload
```

Requirements:
- Accept multipart file uploads.
- Validate file type.
- Reject files exceeding configured size limit.
- Store original file metadata.
- Extract text.
- Chunk text.
- Embed chunks.
- Save chunks to vector store.

Response:

```json
{
  "document_id": "uuid",
  "filename": "example.pdf",
  "status": "indexed",
  "chunk_count": 42
}
```

### 10.3 List Documents

Endpoint:

```http
GET /documents
```

Response:

```json
{
  "documents": [
    {
      "document_id": "uuid",
      "filename": "example.pdf",
      "file_type": "pdf",
      "chunk_count": 42,
      "created_at": "2026-06-06T12:00:00Z"
    }
  ]
}
```

### 10.4 Delete Document

Endpoint:

```http
DELETE /documents/{document_id}
```

Requirements:
- Delete document metadata.
- Delete associated chunks.
- Return success status.

### 10.5 Ask Tribunal

Endpoint:

```http
POST /tribunal/ask
```

Request:

```json
{
  "question": "What does the policy say about external LLM APIs?",
  "document_ids": ["uuid"],
  "top_k": 6
}
```

Response:

```json
{
  "question": "What does the policy say about external LLM APIs?",
  "final_answer": "The policy allows external LLM APIs only when...",
  "overall_verdict": "Partially Supported",
  "reliability_score": 0.78,
  "retrieved_sources": [],
  "witness_answer": {},
  "claims": [],
  "prosecutor_objections": [],
  "judge_verdict": {}
}
```

### 10.6 Run Evaluations

Endpoint:

```http
POST /evaluations/run
```

Requirements:
- Run predefined test cases.
- Store evaluation results.
- Return aggregate quality metrics.

## 11. Data Models

### 11.1 Document

Fields:
- document_id
- filename
- file_type
- original_path
- text_hash
- chunk_count
- created_at
- updated_at

### 11.2 Chunk

Fields:
- chunk_id
- document_id
- chunk_index
- text
- token_count
- embedding_id
- metadata
- source_page
- source_section

### 11.3 RetrievedSource

Fields:
- chunk_id
- document_id
- filename
- page_number
- section_title
- text
- similarity_score

### 11.4 WitnessAnswer

Fields:
- answer_text
- citations
- uncertainty_notes

### 11.5 Claim

Fields:
- claim_id
- claim_text
- claim_type
- cited_sources
- extracted_from_sentence

### 11.6 ProsecutorObjection

Fields:
- objection_id
- claim_id
- objection_type
- explanation
- missing_evidence
- contradicted_by_sources

### 11.7 JudgeVerdict

Fields:
- claim_id
- verdict
- confidence
- explanation
- supporting_sources
- recommended_revision

### 11.8 TribunalResult

Fields:
- tribunal_result_id
- question
- final_answer
- overall_verdict
- reliability_score
- retrieved_sources
- witness_answer
- claims
- prosecutor_objections
- judge_verdicts
- created_at

## 12. Retrieval Requirements

The system should support:

- Semantic vector retrieval.
- Keyword search if feasible.
- Hybrid retrieval as a preferred goal.
- Metadata filtering by document.
- Top-k configuration.
- Chunk overlap configuration.
- Retrieval result display.

Minimum viable retrieval:
- Vector search over chunk embeddings.

Preferred retrieval:
- Hybrid retrieval using vector similarity and keyword matching.
- Optional reranking stage.

## 13. Prompting Requirements

Create separate prompt templates for:

- Witness answer generation.
- Claim extraction.
- Prosecutor review.
- Judge verdict.
- Final answer revision.

Prompts should be stored as separate files or clearly separated modules.

Prompt files should include:
- System instructions.
- Role definition.
- Output schema.
- Grounding rules.
- Citation rules.
- Refusal or uncertainty behavior.

## 14. Witness Prompt Requirements

The Witness must follow these rules:

- Use only provided retrieved context.
- Do not use outside knowledge unless explicitly configured.
- Cite every material claim.
- Say "The provided documents do not contain enough evidence" when evidence is insufficient.
- Avoid absolute claims unless the source text supports them.
- Do not hide uncertainty.

## 15. Prosecutor Prompt Requirements

The Prosecutor must follow these rules:

- Break the Witness answer into factual claims.
- Ignore purely stylistic or transitional sentences.
- Check whether each claim is supported by retrieved source chunks.
- Flag unsupported generalizations.
- Flag claims that cite sources but are not actually supported by those sources.
- Flag contradictions.
- Return structured objections.

## 16. Judge Prompt Requirements

The Judge must follow these rules:

- Review the Witness answer, source context, and Prosecutor objections.
- Decide the verdict for each claim.
- Assign a numeric confidence score.
- Provide concise reasoning.
- Revise unsupported claims out of the final answer.
- Preserve supported useful information.
- Avoid introducing new unsupported claims.

## 17. Citation Requirements

Every final answer should include citations.

Citation behavior:
- Cite source document name.
- Cite page number when available.
- Cite section title when available.
- Cite chunk ID internally.
- Display citations in user-friendly form.

Example:

```text
The policy requires approval before using external LLM APIs. [AI Policy Handbook, p. 4]
```

## 18. Reliability Score

The reliability score should be calculated from claim-level verdicts.

Suggested scoring:

- Supported: 1.0
- Partially Supported: 0.6
- Not Enough Evidence: 0.4
- Unsupported: 0.0
- Contradicted: 0.0

Overall reliability score:

```text
sum(claim_scores) / number_of_claims
```

If there are no factual claims, return "Not Applicable".

## 19. Evaluation Requirements

Create a small evaluation dataset.

Each test case should include:
- Question
- Expected source document
- Expected key facts
- Known unsupported bait claim if useful
- Expected verdict behavior

Evaluation metrics:
- Retrieval hit rate
- Citation accuracy
- Unsupported claim count
- Contradicted claim count
- Final answer reliability
- Judge verdict consistency

Minimum test set:
- 10 test questions.

Preferred test set:
- 25 to 50 test questions.

## 20. Testing Requirements

Minimum test coverage:
- 90 percent for logic and UI.

Backend tests:
- Document ingestion tests.
- Chunking tests.
- Embedding provider abstraction tests.
- Retrieval tests.
- Claim extraction parser tests.
- Verdict scoring tests.
- API endpoint tests.

Frontend tests:
- Component rendering tests.
- Upload form tests.
- Tribunal result rendering tests.
- Claim table tests.
- Error state tests.
- Accessibility tests.

Recommended tools:
- Backend: pytest
- Frontend: Vitest and React Testing Library
- End-to-end: Playwright

## 21. Observability Requirements

The application should log:

- Document ingestion events.
- Retrieval query parameters.
- Retrieved chunk IDs.
- LLM provider used.
- Token usage if available.
- Latency per stage.
- Tribunal verdict summary.
- Evaluation results.

Do not log secrets.
Do not log full sensitive documents by default.

## 22. Security and Privacy Requirements

The application should:

- Never expose API keys in the frontend.
- Sanitize environment examples.
- Validate uploads.
- Limit file size.
- Store documents locally by default.
- Support local LLM mode through Ollama.
- Make hosted LLM usage explicit.
- Avoid sending uploaded documents to hosted APIs unless explicitly configured.
- Include a visible privacy note in the UI.

## 23. Error Handling Requirements

The application should handle:

- Unsupported file type.
- Empty document.
- Failed text extraction.
- Failed embedding generation.
- Empty retrieval results.
- LLM provider unavailable.
- Invalid JSON response from model.
- No claims extracted.
- Evaluation failures.

Errors should be user-friendly and actionable.

## 24. UI Requirements

The UI should feel like a modern software product, not a toy demo.

Suggested theme:
- Courtroom-inspired but professional.
- Use terms like Witness, Prosecutor, Judge, Verdict, Evidence, Objection, Sustained, Overruled.
- Avoid making the interface too gimmicky.

Main UI components:
- Document upload panel.
- Corpus table.
- Question input.
- Retrieved evidence panel.
- Witness answer card.
- Prosecutor objections panel.
- Judge verdict panel.
- Claim verification table.
- Final answer card.
- Reliability score meter.
- Evaluation dashboard charts.

### 24.1 Color Scheme

Use a professional courtroom-inspired color palette that feels serious, trustworthy, and slightly playful. Avoid common AI-style gradients, especially blue-to-magenta gradients.

Recommended palette: "Modern Courtroom"

| Purpose | Color Name | Hex | Usage |
|---|---|---:|---|
| Primary background | Deep Ink | `#111827` | App shell, header, dark sections |
| Main surface | Warm Parchment | `#F8F4EA` | Page background and document panels |
| Card surface | Soft Ivory | `#FFFDF7` | Cards, modals, answer panels |
| Primary action | Gavel Gold | `#D4A017` | Main buttons, active states, important accents |
| Secondary accent | Verdict Teal | `#0F766E` | Supported verdicts and success states |
| Warning accent | Objection Amber | `#F59E0B` | Partially supported claims and uncertainty states |
| Error accent | Overruled Red | `#B91C1C` | Unsupported or contradicted claims |
| Main text | Charcoal | `#1F2937` | Primary readable text |
| Muted text | Slate Gray | `#6B7280` | Metadata, timestamps, helper text |
| Border | Aged Paper Line | `#D6D3C8` | Card borders, dividers, table lines |

Design guidance:
- Use Warm Parchment as the main page background.
- Use Soft Ivory for cards and panels so content feels document-like.
- Use Deep Ink for the top navigation and footer.
- Use Gavel Gold sparingly for primary calls to action.
- Use Verdict Teal, Objection Amber, and Overruled Red consistently for claim verdict status.
- Avoid large gradients. If visual depth is needed, use subtle shadows, borders, and parchment-style surfaces instead.
- The UI should feel like a modern legal review tool, not a cartoon courtroom.

### 24.2 Courtroom-Themed UI Language

Use a professional courtroom metaphor throughout the application, but keep the design clean and enterprise-ready. The theme should make the application memorable without making it feel like a toy.

Use the following labels consistently:

| Feature | UI Label |
|---|---|
| Initial generated answer | Witness Answer |
| Retrieved source chunks | Evidence Locker |
| Claim review table | Claim Docket |
| Adversarial review | Prosecutor Objections |
| Final review | Judge's Verdict |
| Final user-facing answer | Final Ruling |
| Overall result | Tribunal Verdict |
| Saved evaluation run | Case File |
| Unsupported claim | Objection Sustained |
| Supported claim | Objection Overruled |

The UI should avoid cartoonish legal imagery. Do not use gavels, judges, wigs, or court clip art as major design elements. Use the courtroom theme through language, layout, badges, and subtle iconography.
## 25. Suggested Folder Structure

```text
hallucination-tribunal/
  README.md
  requirements.md
  .env.example
  docker-compose.yml

  apps/
    web/
      package.json
      src/
        app/
        components/
        lib/
        tests/

    api/
      pyproject.toml
      src/
        main.py
        api/
        core/
        documents/
        retrieval/
        tribunal/
        evaluations/
        prompts/
        models/
        tests/

  data/
    uploads/
    chroma/
    evals/

  docs/
    architecture.md
    rag-design.md
    prompts.md
    evaluation-plan.md
    privacy-and-security.md
```

## 26. Docker Requirements

Provide Docker support for local development.

Requirements:
- Dockerfile for frontend.
- Dockerfile for backend.
- docker-compose.yml for local stack.
- Optional service for vector database if using Qdrant.
- ChromaDB may run embedded locally if preferred.

## 27. README Requirements

The README should include:

- Project description.
- Screenshots or placeholders.
- Architecture diagram.
- Tech stack.
- Local setup steps.
- Environment variable setup.
- How to run frontend.
- How to run backend.
- How to upload documents.
- How to run Tribunal.
- How to run tests.
- How to run evaluations.
- Known limitations.
- Future roadmap.

## 28. Definition of Done

The project is complete when:

- A user can upload documents.
- The backend chunks and indexes documents.
- A user can ask a question.
- The Witness generates an answer from retrieved sources.
- The Prosecutor identifies claims and objections.
- The Judge produces verdicts and a revised answer.
- The UI displays answer, citations, claim table, objections, verdict, and reliability score.
- At least 10 evaluation questions exist.
- Logic and UI test coverage is at least 90 percent.
- README and architecture docs are complete.
- No secrets are committed.
- The app can run locally with documented commands.

## 29. Stretch Goals

Add these only after the MVP is complete:

- Reranking model.
- Multiple corpora.
- User accounts.
- Export Tribunal report as PDF.
- Compare multiple LLM providers.
- Human feedback on verdict correctness.
- Saved Tribunal sessions.
- Batch question evaluation.
- Confidence calibration.
- Browser extension for checking AI answers.
- GitHub Actions CI pipeline.
- Deployment to Render, Railway, or AWS.

## 30. Recommended Demo Script

Use this demo flow for portfolio or interview presentation:

1. Show the project home page.
2. Upload a small policy document.
3. Ask a question that has a clear answer in the document.
4. Show the Witness answer.
5. Show the Prosecutor objections.
6. Show the Judge verdict.
7. Ask a question that cannot be answered from the documents.
8. Show that the system refuses to hallucinate.
9. Open the evaluation dashboard.
10. Explain how this architecture could be used in enterprise AI governance.

## 31. Seed Document Ideas

Use safe, public, or self-created documents. Do not use confidential or proprietary material.

### 31.1 Best Documents for the Initial Demo

Create a small fictional internal AI policy packet:

1. AI Usage Policy
   - Rules for using internal and external LLMs.
   - Approval requirements.
   - Data classification rules.
   - Prohibited use cases.

2. Data Privacy and Classification Policy
   - Public, internal, confidential, restricted.
   - Rules for PII and PHI.
   - Handling of customer data.

3. Incident Response Runbook
   - Steps for reporting a security incident.
   - Escalation matrix.
   - Required timelines.

4. Software Engineering Standards
   - Testing expectations.
   - Code review rules.
   - Deployment requirements.
   - Logging standards.

5. Model Risk Review Checklist
   - Bias checks.
   - Hallucination checks.
   - Evaluation requirements.
   - Human approval requirements.

These documents are ideal because they allow questions where unsupported claims are easy to detect.

### 31.2 Fun Demo Documents

Use fictional or public-domain style documents:

1. Starship Operations Manual
   - Safety rules.
   - Maintenance requirements.
   - Crew roles.
   - Emergency protocols.

2. Wizard Academy Student Handbook
   - Spell safety policy.
   - Forbidden artifacts.
   - Exam rules.
   - Potion lab requirements.

3. Dragon Sanctuary Care Guide
   - Feeding rules.
   - Fireproofing requirements.
   - Visitor restrictions.
   - Emergency procedures.

4. Time Travel Ethics Policy
   - Rules against paradox creation.
   - Historical contamination limits.
   - Memory alteration restrictions.

5. Superhero League Charter
   - Membership rules.
   - Use-of-powers policy.
   - Civilian safety rules.
   - Disciplinary process.

These are memorable and make the project more fun during interviews.

### 31.3 Serious Enterprise Demo Documents

Use public or self-authored documents based on common enterprise patterns:

1. AI Governance Policy
2. Secure Software Development Lifecycle Policy
3. Cloud Deployment Checklist
4. Disaster Recovery Plan
5. Vendor Risk Assessment Policy
6. Data Retention Policy
7. Customer Support Escalation Policy
8. Acceptable Use Policy
9. Access Control Policy
10. Audit Logging Policy

### 31.4 Healthcare-Oriented Demo Documents

Use synthetic documents only.

1. Synthetic Clinic Documentation Policy
2. PHI Handling Policy
3. Medical Note Formatting Guide
4. Patient Message Triage Policy
5. Clinical AI Safety Review Checklist

This direction could connect well with healthcare AI roles, but avoid using real patient data.

### 31.5 Documents Designed to Test Hallucination

Create documents that intentionally contain:

1. Similar but different rules.
2. Conflicting policy versions.
3. Missing information.
4. Ambiguous statements.
5. Outdated policy sections.
6. Exceptions buried in footnotes.
7. Similar terms that should not be confused.
8. Tables with thresholds.
9. Conditional approval rules.
10. Acronyms with multiple meanings.

These documents make the Tribunal useful because the Prosecutor and Judge have real problems to catch.

## 32. Example Evaluation Questions

Use questions like:

1. Are external LLM APIs allowed?
2. Can confidential data be pasted into a public chatbot?
3. What approvals are needed before using AI with customer data?
4. What is the incident reporting timeline?
5. Does the policy allow PHI to be processed by hosted AI models?
6. What testing coverage is required before production release?
7. Who approves model risk exceptions?
8. What logging is required for AI-generated decisions?
9. Does the document mention SOC 2?
10. What does the policy say about dragon feeding after midnight?

The last question should only be answerable if the fun corpus is loaded. If not, the correct behavior is to say there is not enough evidence.

## 33. Success Criteria for Hiring Managers

A hiring manager should be able to see that this project demonstrates:

- Senior-level system design.
- Practical RAG implementation.
- Understanding of AI hallucination risk.
- Clear separation of concerns.
- Test-driven engineering discipline.
- Ability to explain AI system behavior.
- Awareness of privacy and security concerns.
- Product thinking and usability.
- Ability to build something memorable.
