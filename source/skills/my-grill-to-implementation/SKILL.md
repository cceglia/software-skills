---
name: my-grill-to-implementation
description: Grill a change, persist decisions, implement it after explicit approval, independently review it, and create one task-scoped commit.
license: MIT
compatibility: Canonical multi-harness source; use scripts/build.py to generate native profiles.
metadata:
  version: "2.2.0"
---

# my-grill-to-implementation

Use this lightweight workflow when a change needs explicit design decisions but not a SPEC/ticket pipeline. Do not create a SPEC or tracker tickets.

Use at most one active subagent. Load `grilling` and `domain-modeling` for design, `implement` before coding, and `code-review` in a fresh independent `review` role. Select any additional skills through the active harness's native skill discovery; never invent skill names. A worker must load every skill passed to it and block if a required skill cannot be loaded.

## State

Maintain exactly one resumable file:

```text
./.agents/tmp/implementation/<work-slug>.md
```

Keep it concise and current. Track only: status, implementation approval, goal/scope, resolved decisions, constraints/invariants, relevant repository evidence, rejected alternatives, open questions, validation seams, ordered implementation slices/progress, review cycle/findings, starting branch/revision, commit, and next action.

Statuses: `grilling | ready-for-implementation | implementing | reviewing | blocked | completed`.

Resolve resume state by explicit path, then unambiguous slug/title, then the only non-terminal state. If multiple states are plausible, stop instead of guessing. On resume, reconcile state with branch/HEAD/working tree; state is authoritative for intent, git/filesystem for existing code.

## 1. Grill

Read relevant repository instructions/domain docs. Inspect directly when small; use read-only `explore` for broad discovery. Distinguish repository facts from user decisions, resolve domain language, persist durable domain knowledge/ADRs only when warranted, identify validation seams, and produce ordered testable slices.

When no blocking design question remains, persist:

```text
Status: ready-for-implementation
Implementation approval: pending
```

Show the slices and ask for explicit approval, then end the turn. Never start implementation without recorded approval. A material later change to scope/architecture/constraints resets approval to `pending`.

## 2. Implement

After approval, record starting branch/revision, inspect the working tree, preserve unrelated changes, set `Status: implementing`, and implement one slice at a time. Validate each slice narrowly, persist results, then run the full relevant validation after all slices.

If implementation exposes a new material product/domain decision, return to grilling instead of guessing.

## 3. Review

Set `Status: reviewing` and run a fresh read-only `review` role with `code-review`, the state file, starting revision/current diff, authored files, validation results, and prior findings.

Require:

```text
VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED
SUMMARY: ...
SKILLS_LOADED: ...
SKILLS_NOT_LOADED: ...
BLOCKING_CODE_FINDINGS: id, severity, location, problem, required change, evidence
NON_BLOCKING_CODE_NOTES: ...
VALIDATION_CHECK: ...
REVIEWED_CODE_FILES: ...
```

Persist the result before acting. Maximum 3 review cycles. On `CHANGES_REQUIRED`, fix only blocking findings, validate, and run a fresh review. Block on reviewer `BLOCKED`, exhausted cycles, repeated blocker, unavailable decision, or missing required skill.

## 4. Commit

Only after `APPROVED`, create exactly one task-scoped commit containing only this work. Always exclude `./.agents/tmp/` and preserve unrelated changes. If the task boundary cannot be isolated, block instead of making a mixed commit.

Record the commit, set `Status: completed`, and report the outcome concisely.
