---
name: my-plan-to-spec
description: Explicit-only workflow. Turn a completed grilling state into a reviewed, implementation-ready SPEC and publish it through the configured tracker.
license: MIT
compatibility: Shared Agent Skills profile for Codex, Claude Code, OpenCode V2, and Antigravity; native support files install separately.
metadata:
  version: "2.2.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-plan-to-spec

## Invocation

Explicit-only workflow. Run it only when the user explicitly requests it by name; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use the active harness's installed `explore`, `develop`, and `review` support roles.

Turn the resolved plan into a normative, implementation-ready SPEC.

## Preconditions

Read repository instructions and `docs/agents/issue-tracker.md`. If tracker configuration is missing or unusable, stop and ask the user to run `setup-matt-pocock-skills`. Use configured triage-label strings when present; never invent labels.

Resolve the relevant `./.agents/tmp/grill/<plan-slug>.md`. It must contain `Status: ready-for-spec`; otherwise report the blocker instead of reconstructing missing decisions.

Resolved grilling decisions are authoritative unless the user changes them. Ask only when verification exposes a new material ambiguity or contradiction.

Use one subagent at a time:

- `explore`: read-only repository verification;
- `develop`: SPEC authoring/corrections only;
- `review`: independent read-only review.

Every subagent reads applicable repository instructions first. `develop` and `review` also load `clean-code-principles` and `clean-architecture`. No subagent may mutate git state.

## Workflow

1. **Verify repository context.** Use `explore` to collect only evidence needed to formalize the plan: relevant files/symbols, architecture/contracts, persistence, security boundaries, compatibility/migration conventions, observability/test seams, and contradictions. If verification creates a new product decision, ask the user and update grilling state before authoring.

2. **Author.** Delegate to `develop` with the grilling state, relevant conversation, repository evidence, instructions, and tracker context. Use `US/FR/NFR/INV/DEC/AC/TEST/RISK-###` identifiers. Requirements must be precise and testable; every `AC` maps to at least one `TEST` and vice versa. Cover, where applicable: problem/goals/non-goals, terminology, current-system evidence, actors/stories, requirements/invariants, architecture/responsibilities, contracts, data/migrations, lifecycle/concurrency, failure/recovery, security/privacy, NFRs, observability, rollout/rollback/compatibility, testing, delivery slices, risks/trade-offs, decision log, assumptions and evidence limits. Use `Not applicable` with a reason instead of empty boilerplate.

3. **Review.** Run a fresh `review` against the SPEC, grilling state, and repository evidence. It must check fidelity to resolved decisions, repository alignment, unambiguous scope/contracts/lifecycle, security and migration completeness where relevant, measurable NFRs, full requirement→AC→TEST traceability, and delivery-slice coverage.

Require:

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

For `CHANGES_REQUIRED`, delegate corrections to `develop` and review again. Maximum 5 review cycles; block if the same material finding survives two correction attempts or a required user decision remains unresolved.

4. **Publish.** Only after `APPROVED`, publish/finalize through the configured tracker and apply configured labels when applicable. Preserve the grilling-state reference and material decisions according to tracker capabilities.

Report the SPEC reference, state path, verdict, review cycles, validations, documentation changes, and blockers. Stop before ticket creation or implementation.
