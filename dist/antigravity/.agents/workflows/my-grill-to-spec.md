---
description: Grill a change with Matt Pocock's grill-with-docs, keep a resumable decision ledger, publish the canonical SPEC with to-spec, then independently review it.
---


# my-grill-to-spec

## Invocation

Explicit-only Antigravity workflow. Run `/my-grill-to-spec`; never trigger it through semantic skill matching.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use roles from `.agents/agents.md`: `review`.

Require Matt Pocock's `grill-with-docs` and `to-spec`. If either is unavailable, return `BLOCKED`. Do not duplicate their interview, domain-modeling, SPEC-synthesis, or tracker rules.

## Ledger

Maintain one resumable decision ledger at `./.agents/tmp/grill/<slug>.md`. It is runtime state, never the canonical SPEC. Keep only current truth: status, goal/scope, repository evidence, settled decisions, constraints, acceptance/test seams, rejected/out-of-scope choices, open questions, relevant Matt artifacts, canonical SPEC reference, and `Next action`.

Statuses: `grilling | ready-for-spec | publishing | reviewing | blocked | completed`.

If an existing ledger is supplied, read it first and resume from `Next action`; otherwise resolve only an unambiguous matching ledger. Reconcile tracker state before repeating any publishing step. Checkpoint after every material grill round and phase boundary; rewrite current truth, never a transcript.

## Workflow

1. Invoke `grill-with-docs`; let it own grilling and its native domain artifacts. Update the ledger after each material round until no blocking decision remains.
2. Set `ready-for-spec`, then invoke `to-spec` in the same session using the ledger plus relevant repository/Matt context. `to-spec` alone owns canonical SPEC synthesis and tracker destination; do not delegate SPEC writing to another subagent. Record the canonical reference and set `reviewing`.
3. Run one fresh independent read-only `review` role against the canonical SPEC, ledger, repository evidence, and applicable domain artifacts. Require `VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED` with concise blocking findings.
4. If review exposes a new product/domain decision, return to `grill-with-docs`. Otherwise correct only the documented SPEC issue and run a fresh review. Maximum 3 review cycles.
5. On approval set `completed`, persist the canonical SPEC reference, and **stop before tickets or implementation**.
