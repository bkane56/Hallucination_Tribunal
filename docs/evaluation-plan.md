# Evaluation Plan

## Test Cases

10 cases in `data/evals/test_cases.json` covering:

- Grounded policy questions (eval-01 through eval-09)
- Out-of-corpus refusal behavior (eval-10: dragon feeding)

## Metrics

- Retrieval hit rate
- Citation accuracy
- Unsupported / contradicted claim counts
- Pass rate against expected behavior

## Running

```bash
curl -X POST http://localhost:8000/evaluations/run
```

Or use the Evaluation Dashboard UI.

## Baseline Targets

- Retrieval hit rate ≥ 80%
- Zero contradicted claims on grounded questions
- Correct refusal on out-of-corpus questions
