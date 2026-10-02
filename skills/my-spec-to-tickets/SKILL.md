---
name: my-spec-to-tickets
description: Decompose an approved SPEC into concise implementation tickets, review only the tickets, and publish them through the configured tracker.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-spec-to-tickets

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/my-spec-to-tickets`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

You are the orchestrator for a **pre-implementation ticketing workflow**.

Input:

```text
invocation input
```

Resolve the approved `SPEC`. If it cannot be resolved, ask for it and stop.

## Configuration

Read repository instructions and `docs/agents/issue-tracker.md`.

If tracker configuration is missing or unusable, stop and ask the user to run `setup-matt-pocock-skills`.

If `docs/agents/triage-labels.md` exists, use its configured strings for canonical label roles. Never invent or hardcode label names.

All ticket publication and relationships MUST follow the configured tracker workflow.

## Rules

* The SPEC is already reviewed and is the authoritative source of normative requirements. Do not review or edit it.
* The feature is not implemented yet; never flag missing implementation as a defect.
* Do not duplicate the SPEC into tickets.
* Repository evidence is used only to determine implementation slices, affected components, dependencies and test seams.
* Never invent requirements or repository facts.
* Repository exploration, ticket authoring/corrections and ticket review MUST use one subagent at a time.
* The orchestrator MUST NOT write/edit tickets or implement application code.
* `explore` and `review` are read-only. `develop` may edit tickets only.
* No agent may perform git operations that change repository state.
* Every subagent must read applicable repository instructions first.

If `explore` is unavailable, use a read-only `review` subagent for repository exploration.

## 1. Explore

Run `explore` with the approved SPEC.

Collect only repository evidence needed for decomposition:

* affected architecture/components;
* contracts/models and integration points;
* implementation dependencies;
* invariants and compatibility constraints;
* migrations/observability concerns;
* useful test seams.

Do not search for the requested feature implementation.

If required repository evidence is inaccessible: `BLOCKED`.

## 2. Build tickets

Delegate ticket creation to `develop`, passing the approved SPEC, repository evidence and configured tracker workflow.

Each ticket MUST define one implementation slice and contain:

* one verifiable outcome;
* explicit in-scope / out-of-scope boundaries;
* affected components and ticket-to-ticket dependencies;
* concise repository context needed to locate the work;
* the authoritative SPEC reference;
* exact SPEC IDs covered (`FR/NFR/INV/DEC/AC/TEST` as applicable);
* ticket-specific sequencing or implementation notes that are not already normative in the SPEC;
* definition of done.

Tickets MUST reference the SPEC instead of copying its normative content.

Do not repeat requirement text, acceptance criteria, contracts, edge cases or test definitions already present in the SPEC unless a short excerpt is necessary to disambiguate the slice.

A ticket MUST NOT merely say “implement the SPEC”; its own scope, outcome and dependencies must be explicit.

The complete ticket set MUST cover every implementation-relevant SPEC requirement and acceptance criterion exactly where needed, without hidden/orphan work or unnecessary duplication.

Use native tracker relationships for SPEC→ticket structure and ticket dependencies when supported; otherwise use the configured reference format.

## 3. Review tickets

Run an independent `review` with all tickets, the approved SPEC and repository evidence.

Review **tickets only**. Do not assess, correct or re-approve the SPEC.

Verify:

* every ticket has a specific implementation slice;
* every ticket references the correct SPEC and exact covered IDs;
* tickets do not duplicate normative SPEC content;
* the complete set covers all implementation-relevant requirements/ACs;
* scope and dependency ordering are correct with no cycles;
* repository context is sufficient and evidence-backed;
* no requirement is invented, contradicted, hidden or orphaned.

Return exactly:

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

For `CHANGES_REQUIRED`, delegate corrections to `develop`, then run a new independent ticket review.

Repeat `review → develop → review` for at most 5 cycles. If substantially the same blocking finding survives 2 correction attempts: `BLOCKED`.

## 4. Publish

Only after `APPROVED`, publish/finalize all tickets using the configured tracker.

If triage labels are configured, apply the configured string for canonical `ready-for-agent`; otherwise do not invent a label.

Preserve each ticket's SPEC relationship and ticket dependency relationships using tracker-native mechanisms when available.

Report ticket references, verdict, review cycles, modified tickets, validations and blockers.

## Final boundary

Stop after producing, reviewing and publishing the tickets.

Do **not** implement the feature, modify application code, or continue into development.
