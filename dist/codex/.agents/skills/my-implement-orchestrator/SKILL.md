---
name: my-implement-orchestrator
description: Implement approved tracker tickets with develop/TDD, repeated Matt Pocock code-review gates, scoped commits, and tracker finalization.
license: MIT
compatibility: Codex with native Agent Skills sidecars and project agents.
metadata:
  version: "2.5.1"
---

# my-implement-orchestrator

## Invocation

Explicit-only Codex workflow. Invoke `$my-implement-orchestrator`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use project agents in `.codex/agents/`: `develop`.

Implement approved tracker work without inventing requirements. Require Matt Pocock's `tdd` and `code-review`; if missing, return `BLOCKED`. Matt's `implement` and `implement-spec` are user-only upstream skills, so this orchestrator composes their model-invokable primitives instead.

Read repository instructions and `docs/agents/issue-tracker.md`. Before implementation, obtain a positive integer `MAX_REVIEW_CYCLES` and keep it fixed.

Per ticket:

```text
develop(tdd) → code-review → (develop fix(tdd) → code-review)* → commit → tracker finalization
```

Process ready tickets one at a time in dependency order; a ticket's referenced SPEC is normative for requirements, decisions, acceptance criteria, and agreed test seams.

## Develop

Run a fresh harness-native `develop` role with ticket/SPEC pointers and relevant repository context. Require it to load `tdd` plus the smallest sufficient discovered skills, use only pre-agreed test seams, preserve unrelated changes, validate its work, report loaded/missing skills and changed files, and never commit or rewrite git history. Missing required skills or a newly exposed product/domain decision blocks the ticket.

## Review loop

After every develop/fix pass, invoke Matt's `code-review` against the ticket's fixed starting revision and the authoritative SPEC/ticket context. Treat blocking Standards or Spec findings as `CHANGES_REQUIRED`; a blocked review is `BLOCKED`; otherwise the cycle is approved.

On `CHANGES_REQUIRED`, persist only the blocking findings, run a fresh `develop` fix pass, validate, then run a **new `code-review`**. Repeat until approved or `MAX_REVIEW_CYCLES` is exhausted. Never commit after fixes without a clean subsequent review.

## Commit and finalize

After approval, create exactly one task-scoped commit containing only ticket-related changes and excluding `./.agents/tmp/`. Preserve unrelated work and block if the boundary cannot be isolated safely. Then finalize/update the ticket through the configured tracker; do not report completion if finalization fails.

Report ticket/SPEC references, review cycles, validation, commit, tracker result, and blockers.
