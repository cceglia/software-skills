---
name: my-implement-orchestrator
description: Implement approved tracker tickets with develop/TDD and per-ticket commits, review a ticket individually only in exceptional high-risk cases, then gate the whole change with repeated Matt Pocock code-review cycles before tracker finalization.
license: MIT
compatibility: Canonical OpenCode V2 source; use scripts/build.py to generate the installable profile.
metadata:
  version: "3.1.0"
---

# my-implement-orchestrator

Implement approved tracker work without inventing requirements. Require Matt Pocock's `tdd` and `code-review`; if missing, return `BLOCKED`. Matt's `implement` and `implement-spec` are user-only upstream skills, so this orchestrator composes their model-invokable primitives instead.

Read repository instructions and `docs/agents/issue-tracker.md`. Before implementation, obtain a positive integer `MAX_REVIEW_CYCLES` and keep it fixed.

```text
per ticket:        develop(tdd) -> validation green -> commit
exceptional ticket: + code-review of that ticket -> (develop fix(tdd) -> commit -> new code-review)*
at the end:        code-review -> (develop fix(tdd) -> commit -> new code-review)* -> tracker finalization
```

A ticket's referenced SPEC is normative for requirements, decisions, acceptance criteria, and agreed test seams.

## Working copy

Work only in the current checkout of each involved repository: never create worktrees, branches, or pull requests, and never push. Record each repository's starting revision (`HEAD`) before the first ticket; it is the fixed point for the final `code-review` of that repository.

Run subagents sequentially. Parallelism is allowed only across different repositories, for tickets with no pending dependency between them; never run two subagents in the same repository at once.

## Develop

Process ready tickets one at a time in dependency order. Delegate each develop/fix pass to a fresh subagent with ticket/SPEC pointers and relevant repository context. Require it to load `tdd` plus the smallest sufficient discovered skills, use only pre-agreed test seams, preserve unrelated changes, validate its work, report loaded/missing skills and changed files, and never commit or rewrite git history. Missing required skills or a newly exposed product/domain decision blocks the ticket.

After each pass, re-run the project's tests and typecheck yourself. Only when they are green, create exactly one commit containing only that ticket's changes, excluding `./.agents/tmp/`, with the ticket reference in the message so `code-review` can find the spec. Preserve unrelated work and block if the boundary cannot be isolated safely.

## Exceptional ticket review

Do not review tickets individually by default; the final review covers them. Review a ticket on its own only for a high and concrete risk: a data migration, a risk of data loss, or a new security boundary. A public contract, or other tickets depending on it, is not enough. Before launching it, tell the user which ticket and why, and record the reason in the report. Then run `code-review` right after the ticket's commit with the commit before that ticket as fixed point, and apply the review loop before starting dependent tickets.

## Review loop

After all tickets are committed, invoke Matt's `code-review` per repository with the recorded starting revision as fixed point. Treat blocking Standards or Spec findings as `CHANGES_REQUIRED`; a blocked review is `BLOCKED`; otherwise the cycle is approved.

On `CHANGES_REQUIRED`, pass only the blocking findings to a fresh develop fix pass, validate, commit the fixes (so `code-review` sees them), then run a **new `code-review`**. Repeat until approved or `MAX_REVIEW_CYCLES` is exhausted. Never finalize after fixes without a clean subsequent review.

## Finalize

After the final review is clean, finalize/update every ticket through the configured tracker; do not report completion if finalization fails.

Report ticket/SPEC references, commits per repository, tickets reviewed individually and why, review cycles, validation, tracker result, and blockers.
