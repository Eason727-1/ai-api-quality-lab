# Test Plan

## Scope

The test suite verifies the `/health` and `/v1/evaluate` endpoints, request validation,
deterministic scoring, Chinese text handling, traceability and basic prompt-injection/data-leakage rules.

## Test design

| Category | Technique | Representative case |
| --- | --- | --- |
| Functional | Equivalence partitioning | complete vs. partial keyword coverage |
| Boundary | Boundary value analysis | threshold `0/100`, text max length |
| Contract | Schema assertions | stable fields and HTTP status codes |
| Security | Risk phrase rules | prompt leakage, API key, script tag |
| Regression | Parameterized pytest | repeated execution in GitHub Actions |

## Exit criteria

- All automated tests pass.
- Statement coverage is at least 90%.
- Every response score stays within `0..100`.
- Unsafe output cannot pass even when the numeric threshold is `0`.

