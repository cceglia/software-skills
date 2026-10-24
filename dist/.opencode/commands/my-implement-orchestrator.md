---
description: Implement approved tracker tickets with develop/TDD and per-ticket commits, review a ticket individually only in exceptional high-risk cases, then gate the whole change with repeated Matt Pocock code-review cycles before tracker finalization.
---

# my-implement-orchestrator

## Invocation

User-invoked OpenCode V2 command. Treat `$ARGUMENTS` plus the immediately relevant conversation context as the invocation input.

## Harness roles

Use OpenCode V2 child-session roles: `develop`.

Implement approved tracker work without inventing requirements. Require Matt Pocock's `tdd`, `codebase-design` and `code-review`; if missing, return `BLOCKED`. Matt's `implement` and `implement-spec` are user-only upstream skills, so this orchestrator composes their model-invokable primitives instead.

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

Process ready tickets one at a time in dependency order. Delegate each develop/fix pass to a fresh subagent with ticket/SPEC pointers and relevant repository context. Require it to load, in every ticket and fix pass, the mandatory skills `tdd` and `codebase-design`, plus every available skill specific to the language, framework or tool it will work with (discover them from the skills list; load the ones that match the files and tools the ticket touches). Require it to use only pre-agreed test seams, shape module interfaces with `codebase-design` without contradicting the SPEC, preserve unrelated changes, validate its work, report loaded/missing skills, changed files, and edge cases, and never commit or rewrite git history. A missing mandatory skill or a newly exposed product/domain decision blocks the ticket; a missing language/tool skill does not.

Require it to stop at, not decide, any edge case it finds and return an `EDGE CASES` section (possibly empty) with description, impact, and options. For each one: if the ticket/SPEC already defines the behavior, decide yourself and note it in the report; otherwise report it to the user, have them choose the resolution, and relaunch a subagent on that point.

After each pass, re-run the project's tests and typecheck yourself. Only when they are green, create exactly one commit containing only that ticket's changes, excluding `./.agents/tmp/`, with the ticket reference in the message so `code-review` can find the spec. Preserve unrelated work and block if the boundary cannot be isolated safely.

## Exceptional ticket review

Do not review tickets individually by default; the final review covers them. Review a ticket on its own only for a high and concrete risk: a data migration, a risk of data loss, or a new security boundary. A public contract, or other tickets depending on it, is not enough. Before launching it, tell the user which ticket and why, and record the reason in the report. Then run `code-review` right after the ticket's commit with the commit before that ticket as fixed point, and apply the review loop before starting dependent tickets.

## Review loop

After all tickets are committed, invoke Matt's `code-review` per repository with the recorded starting revision as fixed point. Treat blocking Standards or Spec findings as `CHANGES_REQUIRED`; a blocked review is `BLOCKED`; otherwise the cycle is approved.

On `CHANGES_REQUIRED`, pass only the blocking findings to a fresh develop fix pass, validate, commit the fixes (so `code-review` sees them), then run a **new `code-review`**. Repeat until approved or `MAX_REVIEW_CYCLES` is exhausted. Never finalize after fixes without a clean subsequent review.

## Finalize

After the final review is clean, finalize/update every ticket through the configured tracker; do not report completion if finalization fails.

Report ticket/SPEC references, commits per repository, tickets reviewed individually and why, review cycles, validation, tracker result, and blockers.
