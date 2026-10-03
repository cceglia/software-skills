---
name: my-spec-to-tickets
description: Decompose an approved SPEC into concise reviewed implementation tickets and publish them through the configured tracker.
license: MIT
compatibility: Codex with native Agent Skills sidecars and project agents.
metadata:
  version: "2.2.0"
---

# my-spec-to-tickets

## Invocation

Explicit-only Codex workflow. Invoke `$my-spec-to-tickets`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use project agents in `.codex/agents/`: `explore`, `develop`, and `review`.

Resolve the approved SPEC from the invocation input. If it cannot be resolved, ask for it and stop.

Read repository instructions and `docs/agents/issue-tracker.md`; if tracker configuration is unusable, ask the user to run `setup-matt-pocock-skills`. Use configured triage-label strings only.

The SPEC is authoritative and already reviewed: do not edit or re-review it, do not treat missing implementation as a defect, and do not duplicate normative SPEC text into tickets.

Use one subagent at a time:

- `explore`: read-only evidence for decomposition;
- `develop`: ticket authoring/corrections only;
- `review`: independent ticket review.

No subagent may mutate git state.

## Workflow

1. **Explore.** Collect only evidence needed to split work: affected components/contracts, dependencies, invariants, compatibility/migrations, observability, and test seams. Block if required evidence is inaccessible.

2. **Draft tickets.** `develop` creates one verifiable implementation slice per ticket. Each ticket includes outcome, in/out scope, affected components, dependencies, SPEC reference, exact covered SPEC IDs, only ticket-specific sequencing/context, and definition of done. The full set must cover all implementation-relevant requirements/ACs without hidden work or duplication.

3. **Review tickets.** `review` checks slice specificity, SPEC references/IDs, complete coverage, dependency ordering/no cycles, repository alignment, and absence of invented or duplicated requirements.

Require:

```text
VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED
SUMMARY: ...
BLOCKING_FINDINGS: ...
NON_BLOCKING_NOTES: ...
COVERAGE_CHECK: ...
DEPENDENCY_GRAPH_CHECK: ...
REPOSITORY_ALIGNMENT_CHECK: ...
VALIDATION: ...
REVIEWED_DOCUMENTS: ...
```

For `CHANGES_REQUIRED`, correct with `develop` and review again. Maximum 5 cycles; block if the same material finding survives two correction attempts.

4. **Publish.** Only after `APPROVED`, publish tickets and native relationships through the configured tracker. Apply configured `ready-for-agent` labeling only when available.

Report ticket references, verdict, cycles, validations, modified tickets, and blockers. Stop before implementation.
