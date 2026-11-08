# Changelog — my-spec-review

## 4.9.1 — 2026-11-08

- `/my-spec-review`: the verifier classifies problems as `BLOCKING` or `NON_BLOCKING`; only blocking problems are fixed and drive the loop. Non-blocking problems are kept as notes, passed to later verifiers so they are not re-verified, and listed in the final report.

## 4.9.0 — 2026-11-08

- Added `/my-spec-review`: loops a fresh read-only verification of a spec and its issues (traceability, contradictions, testability, terminology), fixes every problem through the configured tracker, and stops only when a new fresh verification is clean, bounded by `MAX_REVIEW_CYCLES`. Product/domain decisions go to the user; nothing is committed or pushed.
