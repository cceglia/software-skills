---
name: plan-to-spec
description: Turn a completed grilling state and resolved plan into a reviewed, implementation-ready SPEC and publish it through the configured tracker.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# plan-to-spec

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/plan-to-spec`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

Turn the resolved plan into a **normative, implementation-ready SPEC**.

Input:

```text
invocation input
```

## Inputs and configuration

Read repository instructions and `docs/agents/issue-tracker.md`.

If tracker configuration is missing or unusable, stop and ask the user to run `setup-matt-pocock-skills`.

If `docs/agents/triage-labels.md` exists, use its configured strings for canonical label roles. Never invent or hardcode label names.

Resolve the relevant `.opencode/grill/<plan-slug>.md` state file from `invocation input` or the current conversation.

The grilling state MUST have:

```text
Status: ready-for-spec
```

If it is missing, inaccessible, ambiguous, or still `in-progress`, stop and report the blocker instead of inventing missing plan state.

Treat the grilling state as the primary handoff from `grill-to-plan`. Use the current conversation to clarify provenance or recent corrections, but do not reopen decisions already recorded as resolved.

All SPEC publication MUST follow the configured tracker workflow.

## Rules

* Resolved grilling decisions are authoritative unless the user explicitly changes them.
* Ask the user only when SPEC formalization or repository verification reveals a **new blocking ambiguity or contradiction** not resolved by the grilling state.
* Repository evidence verifies implementation constraints; it does not replace explicit product decisions.
* Do not invent material decisions, repository facts, paths or symbols.
* The SPEC is normative and MUST use precise, testable behavior.
* Material `TBD`, `TODO`, contradictions or undefined failure behavior mean the SPEC is not ready.
* Every normative requirement MUST reach observable acceptance criteria and test evidence.
* Apply `clean-code-principles` and `clean-architecture`; encode SOLID obligations as `INV-###` / `NFR-###`.
* Repository verification, SPEC authoring/corrections and formal review MUST use one subagent at a time.
* The orchestrator MUST NOT write/edit the SPEC or implement application code.

Use:

* `explore` — read-only repository verification;
* `develop` — SPEC authoring/corrections only;
* `review` — read-only independent SPEC review.

If `explore` is unavailable, use a read-only `review` agent for verification.

Every subagent must first read applicable repository instructions. `develop`/`review` must also load `clean-code-principles` and `clean-architecture`.

No subagent may perform git operations that change repository state.

## 1. Verify repository context

Run `explore` with the complete grilling state, relevant conversation and known feature area.

Collect only evidence needed to formalize the plan correctly:

* repository revision and relevant `file:line` / symbols;
* current architecture, behavior, contracts and persistence;
* security/tenancy boundaries;
* compatibility/migration conventions;
* observability and test seams;
* responsibility/dependency boundaries;
* contradictions or evidence gaps that materially affect the plan.

Use targeted follow-up exploration only when needed.

If verification exposes a genuinely new material decision, ask the user before final authoring and update the grilling state with the newly resolved decision.

## 2. Author the SPEC

Delegate creation to `develop`, passing:

* the complete `ready-for-spec` grilling state;
* relevant conversation;
* repository verification reports;
* repository instructions;
* configured tracker context.

Use:

* `US-###` — user stories
* `FR-###` — functional requirements
* `NFR-###` — non-functional requirements
* `INV-###` — invariants
* `DEC-###` — implementation decisions
* `AC-###` — acceptance criteria
* `TEST-###` — tests/evidence
* `RISK-###` — risks

Use RFC 2119 keywords only for normative statements.

The SPEC must contain:

1. Executive Summary
2. Problem Statement
3. Goals and Success Measures
4. Out of Scope and Non-Goals
5. Terminology and Domain Glossary
6. Current System and Repository Evidence
7. Actors and User Stories
8. Functional Requirements
9. Domain Model and Invariants
10. Solution Architecture and Component Responsibilities
11. Implementation Decisions
12. External and Internal Contracts
13. Data Model, Persistence and Migration
14. State, Lifecycle, Concurrency and Timing
15. Failure Modes and Recovery
16. Security, Privacy and Abuse Resistance
17. Non-Functional Requirements
18. Observability and Operations
19. Deployment, Rollout, Compatibility and Rollback
20. Testing Decisions and Test Seams
21. Acceptance Criteria
22. Test and Evidence Traceability Matrix
23. Recommended Delivery Slices
24. Risks, Trade-offs and Rejected Alternatives
25. Decision Log
26. Assumptions and Evidence Limitations
27. Further Notes

Keep every section; use `Not applicable` with a reason where appropriate.

For each component define responsibility/non-responsibility, inputs/outputs, source of truth, dependencies, trust boundary, failure behavior and abstraction ownership/dependency injection.

Where applicable define validation/authorization, success/error semantics, null/missing behavior, identity/normalization, concurrency/transactions, retries/timeouts/idempotency, ordering/deduplication, limits/retention, secrets, migration/backfill/rollback, compatibility, telemetry and degraded/dependency-failure behavior.

Every `AC-###` MUST map to at least one `TEST-###`, and every test MUST map back to acceptance criteria.

Use:

| TEST-ID | AC-ID | Gate | Level | Fixture/dependencies | Scenario/action | Observable assertions | Required evidence |
| ------- | ----- | ---- | ----- | -------------------- | --------------- | --------------------- | ----------------- |

Recommended delivery slices must collectively cover the complete SPEC.

## 3. Review

Run a new independent `review` with the complete SPEC, grilling state and repository evidence.

Verify:

* the SPEC faithfully formalizes the resolved plan without reopening or inventing decisions;
* scope, architecture, responsibilities, lifecycle and contracts are unambiguous;
* repository claims are evidence-backed;
* security, compatibility, migration/rollback and dependency-failure behavior are complete where applicable;
* material NFRs are measurable;
* every requirement has AC coverage and every AC has TEST coverage;
* delivery slices cover the complete scope;
* no blocking placeholder, contradiction or unsupported claim remains.

Return:

```text
VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED
SUMMARY: ...
BLOCKING_FINDINGS: ...
NON_BLOCKING_NOTES: ...
TRACEABILITY_CHECK: ...
REPOSITORY_ALIGNMENT_CHECK: ...
VALIDATION: ...
REVIEWED_DOCUMENTS: ...
```

For `CHANGES_REQUIRED`, delegate corrections to `develop`, then run a new independent review.

Repeat `review → develop → review` for at most 5 cycles. If substantially the same blocking finding survives 2 correction attempts: `BLOCKED`.

If a finding requires a genuinely new material user decision, ask the user, update the grilling state, then resume.

## 4. Publish

Only after `APPROVED`, publish/finalize the SPEC using `docs/agents/issue-tracker.md`.

If triage labels are configured, apply the configured string for canonical `ready-for-agent`; otherwise do not invent a label.

Preserve the grilling-state reference, repository revision and material decisions according to tracker capabilities.

Report the SPEC reference, grilling-state path, verdict, review cycles, modified documentation, validations and blockers.

## Final boundary

Stop after producing, reviewing and publishing the SPEC.

Do **not** implement the feature, create implementation tickets, modify application code, or continue into development.
