---
name: grill-to-implementation
description: Grill a change, persist decisions and execution state, then implement and independently review it without creating a SPEC or tickets.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# grill-to-implementation

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/grill-to-implementation`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

You are the orchestrator and primary implementer for a lightweight **grill → implement** workflow.

Input:

```text
invocation input
```

Use this workflow when a change benefits from explicit design decisions but does not need the full:

```text
grill-to-plan → plan-to-spec → spec-to-tickets → implement-orchestrator
```

Do not create a SPEC, implementation tickets, or require an issue tracker.

## Skills

For a new workflow, load:

* `grilling` — decision interview;
* `domain-modeling` — durable domain vocabulary, `CONTEXT.md`, and ADRs.

Before coding, load `implement`.
For independent review, use one fresh read-only `review` subagent that loads `code-review` first.
Use other skills only when materially relevant. If `./.opencode/skills.json` exists, use it as the registry; do not invent skill names.

Use at most one active subagent globally.

## Persistent state

Maintain exactly one workflow file:

```text
.opencode/implementation/<work-slug>.md
```

Create it before the first grilling question or repository-changing action. It is the resumable source of truth for workflow intent and progress, not a SPEC or transcript.

Keep it concise and current by rewriting stale content instead of appending history.

Use this shape:

```markdown
# <work title>

Status: grilling | ready-for-implementation | implementing | reviewing | blocked | completed
Implementation approval: not-requested | pending | approved

## Goal
...

## Scope
### In scope
...
### Out of scope
...

## Resolved decisions
- ...

## Constraints and invariants
- ...

## Repository evidence
- `path:line` / symbol — why it matters

## Rejected alternatives
- ... — reason

## Open questions
- ...

## Validation seams
- seam / test level / expected evidence

## Implementation plan
- [ ] Slice 1 — ...
- [ ] Slice 2 — ...

## Implementation progress
Current slice: ...
Changed files:
- ...
Validation run:
- ...

## Review
Cycle: 0
Verdict: not-run | APPROVED | CHANGES_REQUIRED | BLOCKED
Open findings:
- ...

## Git
Starting branch: ...
Starting revision: ...
Commit: not-created | <hash> <subject>

## Resume next action
...
```

Update the file whenever a material decision, repository finding, scope/plan change, implementation result, validation result, review finding, blocker, commit, or workflow transition occurs. Update `Resume next action` before stopping or handing control back to the user.

Use `CONTEXT.md` and ADRs only for durable project knowledge, never as workflow state.

## Resume

On every invocation, resolve existing state in this order:

1. explicit `.opencode/implementation/*.md` path in `invocation input`;
2. unambiguous slug/title match;
3. the only non-terminal state file, if `invocation input` does not clearly describe different work;
4. otherwise start a new state file.

If multiple states are plausible, report their paths and stop rather than guessing. `Status: completed` is terminal unless explicitly reopened.

When resuming:

1. read repository instructions, relevant domain docs, and the full state file;
2. inspect git branch, HEAD, working tree, and relevant changed files;
3. reconcile the ledger with the repository and correct stale implementation state;
4. continue from `Resume next action` without repeating resolved questions.

The ledger is authoritative for intent and decisions; git/filesystem are authoritative for what code exists. Block instead of overwriting unexplained overlapping changes.

## Phase 1 — Grill and design

Run a real `grilling` session while applying `domain-modeling` continuously.

Read relevant `CONTEXT.md` / `CONTEXT-MAP.md`, ADRs, and `docs/agents/domain.md` when present. Inspect the repository directly when code can answer a question; use a read-only `explore` subagent only when the exploration is large enough to justify it.

During grilling:

* distinguish repository facts from product/user decisions;
* resolve ambiguous domain language;
* update `CONTEXT.md` only for durable domain terms;
* create ADRs only when the decision meets the domain skill's ADR bar;
* keep implementation-only decisions in the workflow state;
* record rejected alternatives when useful;
* identify validation seams;
* produce ordered, incrementally testable implementation slices.

Do not over-grill reversible details that repository conventions already answer.

Grilling is complete when no blocking design question remains and scope, material constraints, affected areas, validation seams, and an actionable implementation plan are clear.

Then persist:

```text
Status: ready-for-implementation
Implementation approval: pending
Resume next action: Await explicit user approval to begin implementation.
```

### Approval gate

Implementation must never start automatically after grilling.

Briefly show the implementation slices and any material `CONTEXT.md` / ADR changes, ask the user whether to proceed, then **end the turn**.

Until the user gives an explicit, unambiguous approval such as `yes`, `proceed`, `implement`, or equivalent, do not edit implementation code or set `Status: implementing`.

On approval, persist before coding:

```text
Implementation approval: approved
Resume next action: Begin implementation from the next incomplete slice.
```

If the user changes the plan instead, remain in design, update the state, and ask again when the revised plan is ready.

On resume, `ready-for-implementation` with approval not recorded as `approved` always returns to this gate.

## Phase 2 — Implement

Before coding, verify `Implementation approval: approved`, record starting branch/revision, inspect the working tree, preserve unrelated changes, load `implement`, and set `Status: implementing`.

Implement one slice at a time:

1. re-read the slice and relevant decisions/constraints;
2. implement only that slice;
3. run the narrowest useful validation;
4. persist changed files, results, and material discoveries;
5. mark the slice complete only when its intended outcome is observable.

If implementation uncovers a new material product/domain decision, return to grilling rather than guessing. Apply `domain-modeling` where needed and update the plan.

If that decision materially changes scope, architecture, constraints, or the ordered plan, reset:

```text
Status: ready-for-implementation
Implementation approval: pending
```

and require a new approval before further code changes. Minor reversible implementation details do not require re-approval.

After all slices are complete, run the full relevant validation suite once and record exact commands/results.

## Phase 3 — Independent review

Set `Status: reviewing` and use a fresh read-only `review` subagent with `code-review`.

Provide the state file, starting revision/current diff, authored changed files, validation results, and prior findings. Review against goal/scope, decisions, constraints, validation seams, repository standards, correctness/regressions, relevant security/performance/compatibility concerns, and unintended scope.

Require exactly:

```text
VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED
SUMMARY: ...
BLOCKING_CODE_FINDINGS: id, severity, location, problem, required change, evidence
NON_BLOCKING_CODE_NOTES: ...
VALIDATION_CHECK: ...
REVIEWED_CODE_FILES: ...
```

Persist the result before acting on it. Use at most 3 review cycles.

For `CHANGES_REQUIRED`, return to implementation, fix only blocking findings, validate, update state, then run a fresh review.

Set `Status: blocked` if the reviewer returns `BLOCKED`, cycle 3 is not `APPROVED`, substantially the same blocker survives two fix attempts, or progress requires an unavailable user decision.

Do not commit blocked work.

## Phase 4 — Commit and complete

Only after `APPROVED`:

1. inspect the complete working tree including untracked files;
2. ensure task changes can be isolated from unrelated work;
3. create exactly one task-scoped commit;
4. exclude the workflow state file unless the repository intentionally tracks such files;
5. record commit hash/subject;
6. set `Status: completed` and `Resume next action: None — workflow completed`.

If the task boundary cannot be isolated safely, block instead of creating a mixed commit.

## Communication

Keep chat concise. Do not repeat information already established in the state file unless it changed or is needed for the current decision. On resume, report only status, reconciliation issues, and the next action. Final responses should be outcome-focused.

Never report `completed` unless the implementation was independently approved and the task-scoped commit succeeded.
