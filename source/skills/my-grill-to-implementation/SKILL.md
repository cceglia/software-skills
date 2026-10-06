---
name: my-grill-to-implementation
description: Grill a small change, keep a resumable implementation ledger, then explore, implement every slice with Matt Pocock's tdd and per-slice commits, and gate the whole change with a final independent review and fix/review cycles.
license: MIT
compatibility: Canonical Claude Code source; use scripts/build.py to generate the installable profile.
metadata:
  version: "4.2.0"
---

# my-grill-to-implementation

Use this light path only when SPEC/tickets would add unnecessary ceremony. Require Matt Pocock's `grill-with-docs` and `tdd`; delegate exploration, development, and a fresh independent review to subagents.

```text
per slice:  develop(tdd) -> validation green -> commit
at the end: fresh review -> (develop fix(tdd) -> commit -> new fresh review)* -> completed
```

## Ledger

Maintain one resumable ledger at `./.agents/tmp/implementation/<slug>.md` containing only current truth: status, scope/decisions, constraints, repository evidence, agreed test seams, ordered slices/progress, starting revision per repository, commits per slice, validation, review cycles/findings, and `Next action`.

Statuses: `grilling | ready-for-implementation | exploring | developing | reviewing | fixing | blocked | completed`.

On resume, read the ledger first and reconcile with branch/HEAD/working tree. Ledger is authoritative for intent; git/filesystem for existing code. Checkpoint after every material grill round, subagent result, commit, review result, and phase boundary.

## Working copy

Work only in the current checkout of each involved repository: never create worktrees, branches, or pull requests, and never push. Record each repository's starting revision (`HEAD`) before the first slice; every review compares against it.

Run subagents sequentially. Parallelism is allowed only across different repositories, for slices with no pending dependency between them; never run two subagents in the same repository at once.

## Workflow

1. Invoke `grill-with-docs`; update the ledger after each material round. When decisions and test seams are settled, record ordered testable slices, set `ready-for-implementation`, and obtain explicit implementation approval.
2. Delegate read-only exploration to a subagent; persist only implementation-relevant evidence.
3. For each slice in order, delegate development to a fresh subagent with the ledger/evidence and require it to load `tdd` plus the smallest sufficient discovered skills. It implements only that slice, never commits, preserves unrelated changes, validates its work, and reports loaded/missing skills, changed files, validation, and blockers. Re-run the project's tests and typecheck yourself; only when green, create exactly one commit with only that slice's changes, excluding `./.agents/tmp/`. Block if the boundary cannot be isolated safely.
4. At your discretion, after a high-risk slice (for example migrations, public contracts, or security boundaries) run an intermediate fresh review of that slice before later slices build on it; its findings follow step 6.
5. After all slices are committed, delegate a **fresh** read-only review to a new subagent against `git diff <starting-revision>...HEAD`, the ledger, and validation evidence. Require `VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED` plus blocking findings.
6. On `CHANGES_REQUIRED`, persist only the blocking findings, delegate a new development fix pass with `tdd`, validate, commit the fixes, then run another fresh review in a new subagent. Maximum 3 review cycles; never approve by self-review.
7. After a clean review, record the commits, set `completed`, and stop.
