# Design Doc Review Checklist

Use this checklist before presenting the design as ready for review.

## Discovery and evidence

- [ ] The starting mode is understood: documented existing project, undocumented existing project, greenfield with requirements, or greenfield with incomplete requirements.
- [ ] Relevant documentation locations were obtained from the user or explicitly confirmed absent.
- [ ] Existing codebase exploration was delegated to subagents rather than broadly performed in the primary agent context.
- [ ] Subagent findings identify relevant files/symbols and unresolved questions instead of dumping large amounts of code into the primary context.
- [ ] Important repository facts were verified when needed.
- [ ] Existing behavior is not incorrectly treated as a product requirement.
- [ ] Facts, assumptions, decisions, and unknowns are distinguishable.

## Requirements and missing information

- [ ] Blocking unknowns that could materially change the architecture were identified.
- [ ] The user was asked for blocking information that could not reasonably be discovered from available evidence.
- [ ] The user was not asked to repeat information already present in the conversation or authoritative sources.
- [ ] Non-blocking uncertainty is recorded as an explicit assumption or open issue.
- [ ] No requirement, measurement, deadline, owner, approval, or compatibility guarantee was silently invented.
- [ ] For greenfield work, enough requirements were established to justify the consequential architecture decisions.

## Problem and scope

- [ ] The objective is understandable in one sentence.
- [ ] The background explains why the work is needed.
- [ ] Goals describe outcomes rather than merely technologies to adopt.
- [ ] Non-goals prevent likely scope misunderstandings.
- [ ] Assumptions and constraints are explicit.

## Design quality

- [ ] The highest-cost-to-reverse decisions are easy to find.
- [ ] Consequential choices include rationale.
- [ ] Consequential choices are tied to evidence, requirements, constraints, or explicit assumptions.
- [ ] Low-cost implementation details are not over-specified.
- [ ] Important interfaces/contracts are defined.
- [ ] Important data ownership, persistence, consistency, and migration concerns are addressed.
- [ ] Serious alternatives are recorded with concise rejection rationale.

## Understandability

- [ ] A reader can understand the document without an oral briefing.
- [ ] Project-specific terms are defined or avoided.
- [ ] At least one diagram is included when structure or flow is otherwise difficult to understand.
- [ ] Diagrams are editable/source-controlled when practical.
- [ ] A greenfield design does not imply that a nonexistent current architecture already exists.

## Production readiness

- [ ] Reliability/performance targets are measurable where relevant, or explicitly marked unknown instead of invented.
- [ ] Monitoring explains how failures or target violations are detected.
- [ ] Alerts are tied to actionable conditions.
- [ ] Logging covers important diagnostics and excludes sensitive data.
- [ ] Major failure modes and recovery behavior are described.
- [ ] Rollout and rollback are defined for risky production changes.

## Security and privacy

- [ ] Trust boundaries and untrusted inputs are considered.
- [ ] Authentication/authorization implications are covered where relevant.
- [ ] Sensitive data handling, retention, access, and encryption are addressed where relevant.
- [ ] Legal, regulatory, contractual, licensing, or residency constraints are addressed when applicable.

## Reviewability

- [ ] Decisions are distinguishable from open questions.
- [ ] Every open issue has a concrete next step.
- [ ] Blocking and non-blocking open issues are distinguishable when that matters.
- [ ] Unknown facts are marked rather than invented.
- [ ] The document contains enough detail to challenge the design before implementation, without becoming a line-by-line implementation plan.
