---
name: my-improve-comments
description: Improve comments and documentation without changing runtime behavior.
license: MIT
compatibility: Claude Code with native skill controls.
disable-model-invocation: true
user-invocable: true
argument-hint: "[scope]"
metadata:
  version: "4.0.0"
---

# my-improve-comments

## Invocation

Explicit-only Claude Code workflow. Run `/my-improve-comments`; never invoke it implicitly.

Treat `$ARGUMENTS` plus immediately relevant conversation context as the invocation input.

Improve comments/documentation in the invocation scope; empty scope means the repository. Exclude generated, vendored/third-party, build-artifact, and non-manually-maintained files.

For one small explicit target, edit directly. For broad scope, use one read-only exploration subagent to create coherent non-overlapping batches, then process batches sequentially with one editing subagent at a time. Each worker reads applicable repository instructions and `CODING_STANDARDS.md`, preserves unrelated changes, formats modified files when appropriate, and never commits.

Follow local standards. Prefer self-documenting code and comments that explain non-obvious intent, rationale, constraints, invariants, lifecycle/security behavior, compatibility, error strategy, architecture, or deliberate trade-offs. Prefer **why** over paraphrasing **what**. Remove stale, redundant, speculative, obsolete, or obvious comments; preserve useful TODO/FIXME and required public API documentation.

Editing boundary: comments/documentation only, plus unavoidable formatter changes. Never change behavior, control flow, expressions, names, APIs, contracts, or architecture.

Report scope, direct/batched mode, changed files, material improvements, skipped/blocked areas, and any code that remains difficult to document cleanly. Do not review or commit.

## Subagents

Never prescribe a subagent type: Claude Code chooses the most suitable available subagent for each delegation. State the delegated scope and constraints (read-only, no commits, skills to load, expected report) in the subagent prompt.
