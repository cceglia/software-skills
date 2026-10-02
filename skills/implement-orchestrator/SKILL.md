---
name: implement-orchestrator
description: Implement approved tracker tickets one at a time with independent review, bounded fixes, task-scoped commits and tracker finalization.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# implement-orchestrator

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/implement-orchestrator`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

You are the implementation orchestrator.

Input:

```text
WORK_ITEM_SOURCE:
invocation input
```

Do not invent missing requirements.

## Configuration

Read repository instructions and `docs/agents/issue-tracker.md`.

If tracker configuration is missing or unusable, stop and ask the user to run `setup-matt-pocock-skills`.

If `docs/agents/triage-labels.md` exists, use only its configured strings for applicable canonical label roles. Never invent or hardcode label names.

Read `./.opencode/skills.json` exactly once before the first subagent and keep it as an immutable registry snapshot.

## Execution rules

* Use exactly one active subagent globally.
* Development/fixes MUST use `task` with `subagent_type: develop`.
* Reviews MUST use `task` with `subagent_type: review`.
* The orchestrator resolves work, routes skills, tracks reports, commits and finalizes tracker items; it MUST NOT implement, fix or review application code itself.
* The review agent performs standards + SPEC checks in its own session and MUST NOT spawn reviewers.
* Never start work whose dependencies are unresolved or cyclic.

Before starting implementation, ask for a positive integer `MAX_REVIEW_CYCLES`. Keep it immutable for the run.

A unit lifecycle is:

```text
develop → review → (develop fix → review)* → commit → tracker finalization
```

A ticket MUST be finalized in the tracker immediately after its approved implementation is committed. Do not start, resolve for execution, or delegate work on the next ticket until finalization of the current ticket has been attempted. Never defer successful-ticket finalization until the end of the run.

The initial review is cycle 1. If cycle `MAX_REVIEW_CYCLES` is not `APPROVED`, the unit is `BLOCKED`.

## 1. Resolve implementation units

Resolve `WORK_ITEM_SOURCE` using the configured tracker workflow.

The normal implementation unit is an approved implementation ticket produced from a SPEC.

For every ticket:

1. resolve its authoritative SPEC reference;
2. load the complete ticket and SPEC;
3. resolve ticket dependencies/native relationships;
4. block the ticket if the SPEC is inaccessible, the ticket lacks a resolvable SPEC reference, or dependencies are unresolved.

The **ticket defines implementation scope**.  
The **referenced SPEC defines normative requirements, decisions, acceptance criteria and tests**.

Do not implement the whole SPEC unless the current ticket explicitly covers it.

Process ready tickets one at a time in dependency order.

Track per unit: ticket reference/title, SPEC reference, blockers, skill plans, changed files, reports, review cycle, status and commit hash.

## 2. Route skills

For every lifecycle stage, calculate the smallest sufficient skill plan from:

* ticket scope;
* referenced SPEC requirements/ACs/tests;
* repository instructions, language/framework, affected files and tests;
* relevant security, performance, architecture and domain concerns.

Validate every selected skill against the registry snapshot.

Plans contain:

```text
mandatory_skills
additional_skills
selection_reasons
```

Mandatory:

* development/fix: `implement`
* review: `code-review`

Load all selected skills in the target subagent before it acts. If the registry is invalid or a selected skill cannot be loaded, block that stage.

Do not load unrelated workflow/delegation skills.

## 3. Develop and review

### Development/fix

Start exactly one `develop` subagent and pass:

```text
Ticket: {ticket_reference}, {title}
SPEC: {spec_reference}
Ticket scope: {scope}
Covered SPEC IDs: {spec_ids}
Repository: {repository_reference}
Mandatory skills: {mandatory_skills}
Additional skills: {additional_skills}
Selection reasons: {selection_reasons}
Review findings to fix: {findings_or_none}
```

Require it to:

* load all listed skills first;
* read the complete ticket, referenced SPEC and repository instructions;
* implement only the ticket scope while satisfying the referenced SPEC requirements;
* preserve unrelated changes;
* run relevant tests/validation;
* return status, summary, loaded/missing skills, files changed, validations/results, uncertainties and blockers;
* create no commit and perform no stage/push/reset/clean/stash/discard operation.

### Review

After each development/fix, start one new `review` subagent with the ticket, referenced SPEC, changed manually authored files, reports, previous findings, cycle number and review skill plan.

Review only the current ticket implementation for:

* ticket scope;
* referenced SPEC requirements/decisions/ACs/tests;
* correctness/regressions;
* security/performance;
* data/API compatibility;
* repository standards;
* tests and unintended scope.

The reviewer is read-only and MUST NOT edit, fix, stage, commit, push or delegate.

Return exactly:

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

On `CHANGES_REQUIRED`, if review cycles remain, recalculate the fix skill plan and run one `develop` fix followed by a new independent review.

Stop the unit as `BLOCKED` when:

* the reviewer returns `BLOCKED`;
* `MAX_REVIEW_CYCLES` is exhausted without approval;
* substantially the same blocking finding survives two fix attempts.

Do not commit without `APPROVED`.

## 4. Commit and finalize

After approval, inspect the complete working tree including untracked files.

Create exactly one task-scoped commit for the ticket containing all and only task-related implementation, tests, generated files, configuration, migrations, documentation and lock-file changes.

Leave unrelated changes untouched. If the task boundary cannot be isolated safely, block instead of creating a mixed commit.

Do not use automatic closing keywords.

Immediately after the approved task-scoped commit is created, finalize that ticket using the configured tracker mechanism **before any work begins on the next ticket**. This is a mandatory per-ticket transition, not an end-of-run batch action.

The required order is:

```text
APPROVED → task-scoped commit → tracker status/finalization → next ticket
```

If tracker finalization fails, record the failure and do not report the ticket as completed. Do not close/finalize a blocked or failed ticket.

Apply configured triage labels only when their canonical roles are applicable; never invent labels.

## Final response

Report:

* configured source platform/tracker;
* registry status;
* `MAX_ACTIVE_SUBAGENTS: 1`;
* `MAX_REVIEW_CYCLES`;
* resolved tickets and SPEC references;
* per ticket: status, skill plans, review cycles, summary, validations, findings, approved files, commit hash/subject and blockers;
* finalized and unfinalized tracker items with reasons.

Never report `completed` unless the ticket implementation was independently approved, all task-related files were committed, unrelated changes were untouched, and tracker finalization succeeded where applicable.
