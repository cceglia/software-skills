---
name: my-grill-to-implementation
description: Grill a small change, keep a resumable implementation ledger, then explore, develop with Matt Pocock's tdd, independently review, fix, and commit it in one workflow.
license: MIT
compatibility: Canonical Claude Code source; use scripts/build.py to generate the installable profile.
metadata:
  version: "4.0.0"
---

# my-grill-to-implementation

Use this light path only when SPEC/tickets would add unnecessary ceremony. Require Matt Pocock's `grill-with-docs` and `tdd`; delegate exploration, development, and a fresh independent review to subagents.

## Ledger

Maintain one resumable ledger at `./.agents/tmp/implementation/<slug>.md` containing only current truth: status, scope/decisions, constraints, repository evidence, agreed test seams, ordered slices/progress, starting revision, changed files, validation, review cycles/findings, commit, and `Next action`.

Statuses: `grilling | ready-for-implementation | exploring | developing | reviewing | blocked | completed`.

On resume, read the ledger first and reconcile with branch/HEAD/working tree. Ledger is authoritative for intent; git/filesystem for existing code. Checkpoint after every material grill round, subagent result, review result, and phase boundary.

## Workflow

1. Invoke `grill-with-docs`; update the ledger after each material round. When decisions and test seams are settled, record ordered testable slices, set `ready-for-implementation`, and obtain explicit implementation approval.
2. Delegate read-only exploration to a subagent; persist only implementation-relevant evidence.
3. Delegate development to a subagent with the ledger/evidence and require it to load `tdd` plus the smallest sufficient discovered skills. It implements the slices without committing, preserves unrelated changes, validates narrowly while working and fully at the end, and reports loaded/missing skills, changed files, validation, and blockers.
4. Delegate a **fresh** read-only review to a new subagent against the complete task diff, ledger, and validation evidence. Require `VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED` plus blocking findings.
5. On `CHANGES_REQUIRED`, persist findings, delegate a new development fix pass, validate, then run another fresh review. Maximum 3 review cycles; never approve by self-review.
6. After approval create exactly one task-scoped commit, excluding `./.agents/tmp/`; preserve unrelated changes. Record the commit, set `completed`, and stop.
