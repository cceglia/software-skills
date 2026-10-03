---
description: Improve logical blank-line spacing without changing behavior or comments.
---


# my-improve-spacing

## Invocation

Explicit-only Antigravity workflow. Run `/my-improve-spacing`; never trigger it through semantic skill matching.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use `.agents/agents.md`: `@explore`, `@develop`, and `@review`.

Improve logical blank-line spacing in the invocation scope; empty scope means the repository. Exclude generated, vendored/third-party, build-artifact, and non-manually-maintained files.

For one small explicit target, edit directly. For broad scope, use one `explore` role to create coherent non-overlapping batches, then process batches sequentially with one `develop` role at a time. Each worker reads applicable repository instructions and `CODING_STANDARDS.md`, preserves unrelated changes, runs the appropriate formatter when useful, and never commits.

Use blank lines only to expose cohesive phases such as validation/guards, synchronization/state change, argument preparation, external calls, persistence/I/O, cleanup, and result construction. Keep one operation together, remove excessive or misleading spacing, preserve compact language idioms and formatter conventions, and report long functions instead of refactoring them.

Editing boundary: whitespace only, plus unavoidable formatter changes. Do not add/rewrite comments or change behavior, control flow, expressions, names, APIs, contracts, or architecture.

Report scope, direct/batched mode, changed files, spacing improvements, skipped/blocked areas, and structurally difficult functions. Do not review or commit.
