---
name: my-implement-orchestrator
description: Implement approved tracker tickets one at a time with native skill discovery, independent review, task-scoped commits, and tracker finalization.
license: MIT
compatibility: Codex with native Agent Skills sidecars and project agents.
metadata:
  version: "2.2.0"
---

# my-implement-orchestrator

## Invocation

Explicit-only Codex workflow. Invoke `$my-implement-orchestrator`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use project agents in `.codex/agents/`: `explore`, `develop`, and `review`.

Implement approved work items from the invocation input. Never invent missing requirements.

## Setup

Read repository instructions and `docs/agents/issue-tracker.md`; if tracker configuration is unusable, ask the user to run `setup-matt-pocock-skills`. Use configured triage-label strings only.

Use exactly one active subagent. The orchestrator resolves work, selects skills, tracks reports, commits, and finalizes tracker items; it does not implement or review application code itself.

Before implementation, ask for a positive integer `MAX_REVIEW_CYCLES` and keep it fixed for the run.

Per ticket:

```text
develop → review → (develop fix → review)* → commit → tracker finalization
```

Do not start the next ticket before finalization of the current one is attempted.

## 1. Resolve tickets

Use the configured tracker workflow. For each ticket, resolve the authoritative SPEC and dependencies. Block when the SPEC/reference is missing or dependencies are unresolved/cyclic.

The ticket defines implementation scope; the referenced SPEC defines normative requirements, decisions, ACs, and tests. Process ready tickets one at a time in dependency order.

## 2. Select skills

Use the **active harness's native skill discovery**. For each develop/fix/review stage, choose the smallest sufficient set from ticket/SPEC scope, repository instructions, language/framework, affected files/tests, and relevant domain/security/performance concerns.

Mandatory skills:

- develop/fix: `implement`;
- review: `code-review`.

Do not invent skill names or load unrelated workflow/delegation skills. Pass the exact selected names to the target worker. The worker must load every listed skill before acting and report `SKILLS_LOADED` / `SKILLS_NOT_LOADED`; any missing required skill blocks that stage.

## 3. Develop and review

Run one fresh `develop` role with ticket/SPEC scope, covered SPEC IDs, selected skills, repository context, and any review findings. Require it to preserve unrelated changes, validate its work, report changed files/results/blockers, and never commit or mutate git history.

After each develop/fix, run one fresh independent read-only `review` role against the ticket, SPEC, authored changes, validation evidence, prior findings, cycle number, and selected review skills.

Require:

```text
VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED
SUMMARY: ...
SKILLS_LOADED: ...
SKILLS_NOT_LOADED: ...
BLOCKING_CODE_FINDINGS: id, severity, location, problem, required change, evidence
NON_BLOCKING_CODE_NOTES: ...
CODE_VALIDATION: ...
REVIEWED_CODE_FILES: ...
APPROVED_CODE_FILES: ...
```

For `CHANGES_REQUIRED`, recalculate fix skills and run a new develop→review cycle while cycles remain. Block on reviewer `BLOCKED`, exhausted cycles, or the same blocking finding surviving two fixes. Never commit without `APPROVED`.

## 4. Commit and finalize

After approval, inspect the complete working tree. Create exactly one task-scoped commit containing all and only ticket-related changes; always exclude `./.agents/tmp/` and preserve unrelated work. Block if the task boundary cannot be isolated safely. Do not use automatic closing keywords.

Immediately finalize/update the ticket through the configured tracker. If finalization fails, record it and do not report the ticket as completed.

## Report

Report tracker, `MAX_REVIEW_CYCLES`, resolved tickets/SPECs, selected and loaded skills, review cycles, validations/findings, approved files, commit hash/subject, tracker-finalization result, and blockers.

A ticket is `completed` only when independently approved, task changes are committed without unrelated files, and required tracker finalization succeeds.
