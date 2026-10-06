---
name: my-improve-code
description: Improve comments/documentation and logical spacing without changing runtime behavior.
license: MIT
compatibility: Canonical Claude Code source; use scripts/build.py to generate the installable profile.
metadata:
  version: "4.2.0"
---

# my-improve-code

Improve comments/documentation and logical blank-line spacing in the invocation scope; empty scope means the repository. Exclude generated, vendored/third-party, build-artifact, and non-manually-maintained files.

For one small explicit target, edit directly. For broad scope, use one read-only exploration subagent to create coherent non-overlapping batches, then process batches sequentially with one editing subagent at a time. Each worker reads applicable repository instructions and `CODING_STANDARDS.md`, preserves unrelated changes, formats modified files when appropriate, and never commits.

Apply two passes to each target:

1. **Comments/documentation:** prefer self-documenting code; keep only comments that add non-obvious intent, rationale, constraints, invariants, lifecycle/security behavior, compatibility, error strategy, architecture, or trade-offs. Prefer **why** over paraphrasing **what**; remove stale/redundant comments while preserving useful TODO/FIXME and required API docs.
2. **Spacing:** use blank lines to expose cohesive phases; keep one operation together, remove excessive/misleading spacing, preserve language/formatter idioms, and report long functions instead of refactoring them.

Editing boundary: comments/documentation, whitespace, and unavoidable formatter changes only. Never change behavior, control flow, expressions, algorithms, names, APIs, contracts, or architecture.

Report scope, direct/batched mode, changed files, comment and spacing improvements, skipped/blocked areas, and structurally difficult functions. Do not review or commit.
