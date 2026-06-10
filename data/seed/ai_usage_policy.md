# AI Usage Policy

## External LLM APIs

External LLM APIs may only be used after obtaining written approval from the AI Governance Committee. All requests must include a data classification assessment and intended use case description.

Approval is required before any production deployment involving customer data.

## Data Classification

- Public data may be used with approved external LLM APIs.
- Internal data requires VP-level approval.
- Confidential data must not be sent to hosted AI models without explicit exception approval.
- Restricted data, including PHI and PII, is prohibited from external LLM processing.

## Prohibited Use Cases

- Automated decision-making affecting employment without human review.
- Processing customer PHI in public chatbots.
- Training external models on company proprietary data.

## Required Logging

All AI-generated decisions must be logged with timestamp, model version, prompt hash, and human reviewer ID when applicable.

## Model Risk Exceptions

Model risk exceptions require approval from the Chief AI Officer and must include bias checks, hallucination evaluation, and human approval requirements.
