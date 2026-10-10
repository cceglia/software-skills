---
name: my-grill-to-implementation
description: Grill a small change, keep a resumable implementation ledger, then explore, implement every slice with Matt Pocock's tdd and per-slice commits, and gate the whole change with a final independent review and fix/review cycles.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "3.2.0"
  opencode/autoinvoke: false
  opencode/slash: true
---

# my-grill-to-implementation

## Invocation

Explicit-only OpenCode V2 workflow. Run `/my-grill-to-implementation`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use OpenCode V2 child-session roles: `explore`, `develop`, `review`.

Use this light path only when SPEC/tickets would add unnecessary ceremony. Require Matt Pocock's `grill-with-docs` and `tdd`; delegate exploration, development, and a fresh independent review to subagents.

```text
per slice:  develop(tdd) -> validation green -> commit
at the end: fresh review -> (develop fix(tdd) -> commit -> new fresh review)* -> completed
```

## Ledger

Maintain one resumable, temporary ledger at `./.agents/tmp/implementation/<slug>.md` containing only current truth: status, a pointer to the spec, repository evidence, starting revision per repository, slice progress, commits per slice, validation, review cycles/findings, and `Next action`. The ledger is never committed.

Statuses: `grilling | ready-for-implementation | exploring | developing | reviewing | fixing | blocked | completed`.

On resume, read the ledger first and reconcile with branch/HEAD/working tree. The spec is authoritative for intent; git/filesystem for existing code. Checkpoint after every material grill round, subagent result, commit, review result, and phase boundary.

## Spec

Read `docs/agents/issue-tracker.md` (and `docs/agents/domain.md`) first; if missing, return `BLOCKED` and ask the user to run `/setup-matt-pocock-skills`. The plan is the spec: write it as `spec.md` in the spec folder that tracker file defines (local markdown: `.scratch/<slug>/spec.md`) with scope/decisions, constraints, agreed test seams, and the ordered slices; never one ticket per slice. For a remote tracker with no folder, publish the same spec as one issue as the file prescribes and commit nothing for it.

## Edge cases

Require every development/fix subagent to stop at, not decide, any edge case it finds and to return an `EDGE CASES` section (possibly empty) with description, impact, and options. For each one: if the spec already defines the behavior, decide yourself and record it in the ledger; otherwise report it to the user, have them choose the resolution, record it in the spec, and relaunch a subagent on that point.

## Working copy

Work only in the current checkout of each involved repository: never create worktrees, branches, or pull requests, and never push. Record each repository's starting revision (`HEAD`) before the first slice; every review compares against it.

Run subagents sequentially. Parallelism is allowed only across different repositories, for slices with no pending dependency between them; never run two subagents in the same repository at once.

## Workflow

1. Invoke `grill-with-docs`; update the ledger after each material round. When decisions and test seams are settled, write the spec with ordered testable slices, set `ready-for-implementation`, and obtain explicit implementation approval.
2. Delegate read-only exploration to a subagent; persist only implementation-relevant evidence.
3. Every slice is implemented by a subagent, never directly by you: for each slice in order, delegate development to a fresh subagent with the ledger/evidence and require it to load `tdd` plus the smallest sufficient discovered skills. It implements only that slice, never commits, preserves unrelated changes, validates its work, and reports loaded/missing skills, changed files, validation, blockers, and edge cases (see Edge cases). Re-run the project's tests and typecheck yourself; only when green, create exactly one commit with only that slice's changes, excluding the spec and `./.agents/tmp/`. Block if the boundary cannot be isolated safely.
4. Do not review slices individually by default. Only for a high and concrete risk (a data migration, a risk of data loss, or a new security boundary; a public contract or later slices depending on it is not enough), run an intermediate fresh review of that slice before later slices build on it, after telling the user which slice and why; its findings follow step 6.
5. After all slices are committed, delegate a **fresh** read-only review to a new subagent against `git diff <starting-revision>...HEAD`, the ledger, and validation evidence. Require `VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED` plus blocking findings.
6. On `CHANGES_REQUIRED`, persist only the blocking findings, delegate a new development fix pass with `tdd`, validate, commit the fixes, then run another fresh review in a new subagent. Maximum 3 review cycles; never approve by self-review.
7. After a clean review, commit the spec as the last commit (never the ledger or `./.agents/tmp/`), record the commits, set `completed`, and stop.
