---
name: software-design-doc
description: Create or review software design documents for greenfield or existing software projects. Interactively discover requirements, ask for missing information, delegate broad codebase exploration to OpenCode subagents, and focus the document on consequential decisions, trade-offs, interfaces, operability, security, and unresolved questions.
license: MIT
compatibility: Designed for OpenCode; broad codebase exploration requires read-only exploration subagents so the primary agent can preserve its context for design reasoning.
metadata:
  version: "1.0.0"
  audience: "software-engineers"
  artifact: "design-doc"
---

# Software Design Documentation

Use this skill when the user asks for a design document, technical design, architecture proposal, RFC-like document, implementation design, migration design, or a review of an existing design.

The goal is not to describe every implementation detail. The goal is to make expensive, risky, cross-cutting, or hard-to-reverse decisions explicit early enough that they can be reviewed before implementation.

The skill supports all of these starting points:

- an existing project with documentation and code
- an existing project with code but little or no documentation
- a greenfield project with requirements but no implementation yet
- a greenfield project where even the requirements are still incomplete

## Core behavior

**Discover what can be discovered. Ask what must be asked. Never silently invent what matters.**

The primary agent is the design coordinator. It should preserve its context for requirements, decisions, trade-offs, questions, and the final design. Broad repository and codebase exploration must be delegated to subagents.

## Core principles

1. Prioritize decisions by the cost of being wrong.
   - Spend the most space on decisions that are expensive to reverse, affect multiple components or teams, create long-term operational burden, or introduce security/privacy/reliability risk.
   - Keep easily reversible details brief or omit them.

2. Make the document understandable without verbal context.
   - Put the objective, motivation, scope, and essential system context near the beginning.
   - Define project-specific terms when a reader outside the immediate team may not know them.

3. Describe outcomes before implementation choices.
   - Goals should describe user, system, team, or business outcomes.
   - Do not use a technology choice as a goal unless adopting that technology is itself the required outcome.

4. Define scope with both goals and non-goals.
   - Explicitly list plausible expectations that are intentionally out of scope.

5. Prefer selective depth over exhaustive boilerplate.
   - Include only sections that are relevant to the project.
   - Do not fill irrelevant sections just because they exist in the template.

6. Make trade-offs reviewable.
   - Document serious alternatives and why they were rejected.
   - State assumptions and constraints that materially shape the design.

7. Treat unresolved questions as first-class design information.
   - Every open issue should include the unresolved problem, plausible options, and the next action or owner needed to resolve it.
   - When an issue is resolved, preserve the decision and rationale.

8. Design for operation, not just implementation.
   - For production systems, address measurable reliability/performance targets, monitoring, alerting, logging, failure modes, rollout, rollback, and maintenance where relevant.

9. Use editable diagrams for structural complexity.
   - Prefer Mermaid unless the repository already uses another diagram format.
   - Diagrams should clarify component relationships, data flow, trust boundaries, deployment topology, or important sequences.

10. Keep evidence separate from assumptions.
   - Repository facts, user-provided requirements, inferred assumptions, design decisions, and unresolved questions must remain distinguishable.

## Mandatory subagent policy

### Preserve the primary agent context

The primary agent MUST NOT perform broad codebase exploration itself.

Broad exploration includes:

- recursively reading large directory trees
- searching the whole repository for architecture clues
- opening many implementation files to understand subsystem behavior
- tracing cross-package or cross-service call flows
- discovering all implementations of an interface or pattern
- mapping database, API, infrastructure, or test architecture across many files

Delegate these tasks to subagents so the primary context remains focused on design reasoning and interaction with the user.

### Which subagents to use

For an existing local codebase:

- Use the built-in `explore` subagent for read-only repository/codebase exploration.
- Prefer multiple focused `explore` tasks over one extremely broad task when the system has distinct areas such as API, persistence, infrastructure, security, or observability.
- Run independent exploration tasks in parallel when supported and useful.

For external dependency or upstream-source research:

- Use the built-in `scout` subagent when available.

Use another suitable specialized subagent when the repository defines one that is better matched to the task.

### What subagents should return

Ask exploration subagents for concise, decision-oriented summaries rather than raw dumps. Their response should include, where applicable:

- relevant files and directories
- current architecture/components
- important interfaces and contracts
- data stores and ownership
- dependencies and infrastructure
- tests or configuration that establish expected behavior
- constraints relevant to the proposed change
- inconsistencies or unclear areas
- facts that require primary-agent verification
- questions that cannot be answered from the repository

Request file paths and, when useful, symbols or line references so important findings can be verified without repeating broad exploration.

### What the primary agent may inspect directly

After subagent exploration, the primary agent MAY read a small, targeted set of files when necessary to:

- verify a high-impact claim
- inspect the exact shape of a public interface or schema
- resolve a contradiction between subagent findings
- quote or reference a precise repository fact in the design

This must remain targeted. Do not redo the subagent's broad exploration in the primary context.

### If subagents are unavailable

If subagent invocation is unavailable or denied, do not silently fall back to broad primary-agent exploration. Tell the user that the intended context-isolation mechanism is unavailable and proceed only with targeted inspection or user-provided context.

## Workflow

### 0. Establish the starting mode

Before drafting, determine which situation applies:

#### Mode A — Existing project with documentation

There is existing documentation and code or other implementation artifacts.

#### Mode B — Existing project without useful documentation

There is an implementation, but documentation is absent, incomplete, or outdated.

#### Mode C — Greenfield project with requirements

There is no meaningful implementation or existing project documentation yet, but the user has requirements or a reasonably clear problem statement.

#### Mode D — Greenfield project with incomplete requirements

There is no useful implementation/documentation and the problem itself still needs discovery.

Do not treat the absence of documentation as an error. Switch to requirements discovery instead.

### 1. Interactive intake

Use `references/intake-guide.md` as guidance for interactive discovery. It is a question menu, not a form that must be completed mechanically.

First establish what the user wants to design and where existing information can be found.

If the user has not already provided this information, ask for:

1. the change, system, feature, migration, or problem to design
2. where relevant existing documentation can be found, or confirmation that no relevant documentation exists
3. whether there is an existing codebase to inspect and, if so, its location/scope when that is not obvious

Examples of documentation sources:

- `README` files
- `docs/`, `architecture/`, `design/`, `adr/`, or `rfc/` directories
- requirements or product documents
- tickets / issue descriptions
- API specifications
- schemas
- diagrams
- previous design documents
- related repositories
- external references explicitly supplied by the user

Do not assume all relevant documentation is in the repository.

Do not ask the user for information that can reasonably be discovered from the provided documentation or codebase.

### 2. Discover existing context

#### For Mode A

Read the user-identified documentation first. Then delegate codebase exploration to `explore` subagents to verify the documentation and gather implementation facts relevant to the design.

If documentation conflicts with the code, record the discrepancy explicitly rather than silently choosing one.

#### For Mode B

Treat the codebase as an evidence source rather than as requirements documentation.

Delegate exploration to `explore` subagents. Reconstruct only the architecture relevant to the requested design. Do not attempt to reverse-engineer the entire system unless the requested design genuinely requires it.

Clearly distinguish:

- observed current behavior
- inferred intent
- requirements supplied by the user

Never assume that existing behavior is necessarily the desired behavior.

#### For Modes C and D

There may be nothing to inspect. Do not fabricate an existing architecture.

Use the intake process to establish enough product and system requirements to make consequential design decisions. The absence of documentation means the first useful artifact may be this design document itself.

### 3. Build a knowledge map

Before committing to a design, classify information into:

#### Known facts

Supported by user input, authoritative documents, or verified repository evidence.

#### Assumptions

Reasonable working assumptions that are not yet confirmed. State them explicitly.

#### Decisions

Choices made by the proposed design, with rationale where consequential.

#### Unknowns

Information that remains missing.

Then classify each unknown as:

- **Blocking** — a plausible answer could materially change the architecture, scope, safety, compatibility, cost, or another high-cost decision.
- **Non-blocking** — the design can proceed safely while recording the uncertainty.

### 4. Ask only high-value missing questions

Ask the user for blocking information before finalizing the design.

Prefer a small batch of related, high-value questions rather than repeatedly interrupting the user one question at a time.

Typical blocking questions may involve:

- user or caller expectations
- functional behavior
- backward compatibility
- allowed downtime
- data correctness or consistency requirements
- expected scale or workload shape
- latency or availability requirements
- deployment/infrastructure constraints
- required integrations
- technology constraints that are truly mandatory
- security/privacy/compliance requirements
- migration constraints
- ownership or organizational boundaries
- cost constraints when they materially affect architecture

Do not ask every category mechanically. Ask only questions whose answers matter to the proposed design.

For non-blocking unknowns, either:

- make an explicit, clearly labeled assumption, or
- record an Open Issue in the design document.

Never silently invent missing requirements, measurements, deadlines, owners, approvals, compatibility guarantees, or business constraints.

### 5. Greenfield requirements discovery

For Modes C and D, establish a minimum viable requirements baseline before designing the architecture.

At minimum, determine what is relevant from these areas:

- problem and motivation
- primary users/callers and important scenarios
- desired outcomes / goals
- explicit non-goals
- essential functional requirements
- important constraints
- integrations and external systems
- data that must be stored or exchanged
- scale/workload assumptions when architecture-sensitive
- reliability expectations when architecture-sensitive
- security/privacy/compliance needs when applicable
- rollout or migration needs when applicable

For Mode D, the first interaction may be requirements elicitation rather than architecture design. That is expected.

Do not force the user to answer irrelevant enterprise-style questions for a small project. Scale the intake to the risk and reversibility of the work.

### 6. Decide the appropriate document depth

Use a short design note when the change is local, low risk, easy to reverse, and affects few people.

Use a fuller design document when one or more of these apply:

- multiple engineers or teams must coordinate
- the work is expected to span a substantial period
- the design will live in production for a long time
- requirements or ownership boundaries are ambiguous
- data models, public interfaces, infrastructure, or persistence choices are hard to reverse
- failure could cause meaningful reliability, security, privacy, legal, or financial impact

When the user explicitly asks for a full design doc, create one even if the project is small, but keep irrelevant sections concise or omit them.

### 7. Identify the high-cost decisions

Before writing prose, identify the decisions with the highest reversal cost. Typical examples:

- system boundaries and ownership
- public API / CLI / event contracts
- persistence model and data migration strategy
- consistency and concurrency model
- programming language or runtime when it constrains the system materially
- infrastructure or managed-service choices with lock-in
- security trust boundaries and authentication/authorization model
- failure handling and recovery model
- compatibility and rollout strategy

Make these decisions easy to find in the final document.

### 8. Draft the design

Use `references/design-doc-template.md` as a menu, not a form. Remove sections that do not help reviewers make decisions.

At minimum, most non-trivial design docs should contain:

- title and status
- objective
- background / problem
- goals
- non-goals
- proposed design
- alternatives considered
- assumptions and/or open issues when relevant

Add other sections when relevant, especially scenarios, diagrams, current architecture, interfaces, data model, constraints, SLOs, monitoring/alerting, dependencies/infrastructure, security, privacy, logging, rollout/rollback, migration, testing, and timeline.

For greenfield work, omit `Current Architecture` unless there is a relevant predecessor, external system, or baseline architecture to describe.

### 9. Produce diagrams when they reduce ambiguity

Use Mermaid diagrams directly in Markdown when possible.

Choose the diagram type based on the question:

- `flowchart`: components, dependencies, trust boundaries, data flow
- `sequenceDiagram`: request flow, workflows, retries, asynchronous interactions
- `stateDiagram-v2`: lifecycle and state transitions
- `erDiagram`: important persisted data relationships

Keep diagrams conceptual. Do not reproduce every class or function.

### 10. Verify operational completeness

For production services or changes to production behavior, explicitly consider:

- availability, latency, throughput, capacity, or other measurable targets
- how those targets are measured
- alerts and actionable failure signals
- logs and sensitive-data exclusions
- expected failure modes and degradation behavior
- rollout strategy and rollback path
- backward/forward compatibility
- data migration safety when applicable

### 11. Verify security and privacy

When the system accepts untrusted input, crosses privilege boundaries, handles credentials, exposes public interfaces, or processes sensitive data, cover:

- attack surface
- trust boundaries
- authentication and authorization
- validation of untrusted input
- secrets handling
- encryption where relevant
- sensitive data categories
- data retention and access
- sensitive data that must not appear in logs

If a security/privacy section is omitted, make sure that omission is intentional rather than accidental.

### 12. Review the document before finishing

Use `references/review-checklist.md`.

The final document should let a reviewer answer:

- What problem are we solving and why now?
- What is explicitly in and out of scope?
- Which statements are facts, assumptions, decisions, or unresolved questions?
- What are the consequential technical decisions?
- What alternatives were seriously considered?
- How does data/control flow through the system?
- What can fail, and how do we detect/recover from it?
- What assumptions or constraints drive the design?
- What questions remain unresolved?

## Interaction rules

- Do not generate a polished final design immediately when critical context is missing.
- Ask for blocking information first.
- Do not ask the user to repeat information they already supplied.
- Do not ask questions that repository/document exploration can answer reliably.
- Explain briefly why a question is blocking when the reason is not obvious.
- When useful, offer concrete answer choices to reduce user effort, but always allow a custom answer.
- If the user explicitly wants to proceed despite unresolved blocking questions, document the resulting assumptions and risks prominently.

## Writing rules

- Prefer concrete statements over vague adjectives such as “fast”, “scalable”, “robust”, or “secure”. Replace them with measurable targets or explicit mechanisms where possible.
- Separate requirements from implementation choices.
- Separate facts, assumptions, decisions, and open questions.
- Explain why a consequential choice was made, not only what was chosen.
- Keep rejected alternatives brief unless their rejection is non-obvious or important for future readers.
- Do not fabricate measurements, requirements, deadlines, owners, approvals, or repository facts. Mark unknowns explicitly.
- Avoid line-by-line implementation plans unless the user specifically requests one.
- Prefer tables only when comparison is genuinely easier to scan than prose.
- Use code snippets only for interfaces, schemas, protocols, configuration shapes, or other details that materially affect the design.

## Default output location

If the user asks you to write the design into the repository and gives no path, use:

`docs/design/<short-kebab-case-title>.md`

If the repository already has an established RFC, ADR, proposal, or design-doc location, follow the repository convention instead.

## Source inspiration

This workflow is inspired by Michael Lynch's article “How to Write an Effective Software Design Document” from Refactoring English. Apply the underlying principles in original wording; do not copy the article text into generated documents.
