# Changelog — my-spec-review

## 4.9.0 — 2026-11-08

- Added `/my-spec-review`: loops a fresh read-only verification of a spec and its issues (traceability, contradictions, testability, terminology), fixes every problem through the configured tracker, and stops only when a new fresh verification is clean, bounded by `MAX_REVIEW_CYCLES`. Product/domain decisions go to the user; nothing is committed or pushed.
