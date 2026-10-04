---
name: my-improve-comments
description: Improve comments and documentation without changing runtime behavior.
license: MIT
compatibility: Codex with native Agent Skills sidecars and project agents.
metadata:
  version: "2.5.1"
---

# my-improve-comments

## Invocation

Explicit-only Codex workflow. Invoke `$my-improve-comments`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use project agents in `.codex/agents/`: `explore`, `develop`.

Improve comments/documentation in the invocation scope; empty scope means the repository. Exclude generated, vendored/third-party, build-artifact, and non-manually-maintained files.

For one small explicit target, edit directly. For broad scope, use one `explore` role to create coherent non-overlapping batches, then process batches sequentially with one `develop` role at a time. Each worker reads applicable repository instructions and `CODING_STANDARDS.md`, preserves unrelated changes, formats modified files when appropriate, and never commits.

Follow local standards. Prefer self-documenting code and comments that explain non-obvious intent, rationale, constraints, invariants, lifecycle/security behavior, compatibility, error strategy, architecture, or deliberate trade-offs. Prefer **why** over paraphrasing **what**. Remove stale, redundant, speculative, obsolete, or obvious comments; preserve useful TODO/FIXME and required public API documentation.

Editing boundary: comments/documentation only, plus unavoidable formatter changes. Never change behavior, control flow, expressions, names, APIs, contracts, or architecture.

Report scope, direct/batched mode, changed files, material improvements, skipped/blocked areas, and any code that remains difficult to document cleanly. Do not review or commit.
