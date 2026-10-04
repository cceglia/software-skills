---
description: Grill a small change, keep a resumable implementation ledger, then explore, develop with Matt Pocock's tdd, independently review, fix, and commit it in one workflow.
---


# my-grill-to-implementation

## Invocation

Explicit-only Antigravity workflow. Run `/my-grill-to-implementation`; never trigger it through semantic skill matching.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use roles from `.agents/agents.md`: `explore`, `develop`, `review`.

Use this light path only when SPEC/tickets would add unnecessary ceremony. Require Matt Pocock's `grill-with-docs` and `tdd`; use harness-native `explore`, `develop`, and fresh independent `review` roles.

## Ledger

Maintain one resumable ledger at `./.agents/tmp/implementation/<slug>.md` containing only current truth: status, scope/decisions, constraints, repository evidence, agreed test seams, ordered slices/progress, starting revision, changed files, validation, review cycles/findings, commit, and `Next action`.

Statuses: `grilling | ready-for-implementation | exploring | developing | reviewing | blocked | completed`.

On resume, read the ledger first and reconcile with branch/HEAD/working tree. Ledger is authoritative for intent; git/filesystem for existing code. Checkpoint after every material grill round, subagent result, review result, and phase boundary.

## Workflow

1. Invoke `grill-with-docs`; update the ledger after each material round. When decisions and test seams are settled, record ordered testable slices, set `ready-for-implementation`, and obtain explicit implementation approval.
2. Run read-only `explore`; persist only implementation-relevant evidence.
3. Run `develop` with the ledger/evidence and require it to load `tdd` plus the smallest sufficient discovered skills. It implements the slices without committing, preserves unrelated changes, validates narrowly while working and fully at the end, and reports loaded/missing skills, changed files, validation, and blockers.
4. Run a **fresh** read-only `review` against the complete task diff, ledger, and validation evidence. Require `VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED` plus blocking findings.
5. On `CHANGES_REQUIRED`, persist findings, run a new `develop` fix pass, validate, then run another fresh review. Maximum 3 review cycles; never approve by self-review.
6. After approval create exactly one task-scoped commit, excluding `./.agents/tmp/`; preserve unrelated changes. Record the commit, set `completed`, and stop.
