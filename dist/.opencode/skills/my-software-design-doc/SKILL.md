---
name: my-software-design-doc
description: Create or review software design documents, discovering repository context and asking only for decisions that cannot be inferred safely.
license: MIT
compatibility: OpenCode V2 with native subagents.
metadata:
  version: "4.2.0"
---

# Software Design Documentation

## Response style (ASD-STE100)

These defaults apply to every reply from this command or skill, unless the session has an explicit `/asd-ste100` directive. Precedence: the user's current instruction, then the session directive (including `off`), then these defaults.

- **Level:** 80. Apply the core rules below. Level 90 and above also require an exact word count and an audit of verb forms and terminology before you send.
- **Scope:** replies only. `docs` also applies the rules to documents that you write in chat. Code, paths, commands, identifiers, quoted errors, URLs, and files on disk stay unchanged. Explain them in plain prose.
- **Language:** answer in the user's language and apply these principles to it. English text follows ASD-STE100 literally. Other languages use the closest equivalent. For Italian, avoid `stare + gerundio`, compound tenses when a simple tense is clear, and long chains of subordinates.

### Core rules

1. Write one idea or one instruction in each sentence. Use a maximum of 20 words in a procedure and 25 words in a description.
2. Use the active voice. Use the passive voice only when the agent is unknown.
3. Use the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle as an adjective. Do not use the perfect, the progressive, or `-ing` as a verb in English.
4. Use plain and common words. Keep one term for one concept. Do not use nominalizations, avoidable phrasal verbs, filler, or hedging.
5. Keep compound nouns to three words. Write complete sentences and use articles.
6. Put one topic in each paragraph. Start the paragraph with a topic sentence. Use a maximum of six sentences.
7. Put a condition before its command. Do not use semicolons.
8. Keep a vertical list consistent: a colon after the lead-in, one marker style, a capital at the start, and a period only on complete sentences.
9. Do not change facts, code, or meaning. Do not invent values.

### Format

- Start with the result. Remove preambles, repeated summaries, and closing sentiment.
- Use a heading, a table, or a list only when it makes the content shorter or clearer.
- Never remove required report fields, evidence, risks, file paths, or verdict schemas. Apply the style to the prose around them.

### Delegation

When you delegate to a subagent, write this directive in the subagent prompt: the active level, the scope, the language rule, the core rules, and the precedence above. The subagent replies with the same style and keeps its report schema complete.

Use this skill for technical designs, architecture proposals, RFC-like documents, migrations, or reviews of existing designs. Focus on consequential, cross-cutting, risky, or hard-to-reverse decisions rather than implementation trivia.

**Discover what can be discovered. Ask what must be asked. Never silently invent material facts or requirements.**

## Principles

- Separate verified facts, user requirements, assumptions, design decisions, and open questions.
- Define goals and non-goals before implementation choices.
- Spend detail in proportion to reversal cost and operational/security risk.
- Record serious alternatives and why they were rejected.
- Prefer measurable reliability/performance/security statements over vague adjectives.
- Cover operation, rollout/rollback, compatibility, migration, failure/recovery, observability, and privacy only where relevant.
- Use Mermaid when a diagram materially reduces ambiguity.

## Exploration

The primary agent coordinates design and user decisions; it must not consume its context with broad repository exploration.

Use the built-in OpenCode V2 `explore` subagent for broad codebase discovery. Ask for concise evidence: relevant files/symbols, architecture/components, contracts, data ownership, dependencies, tests/configuration, constraints, inconsistencies, and unresolved questions. The primary agent may inspect a small targeted set of files to verify high-impact claims or exact interfaces.

If isolated exploration is unavailable, do not silently perform a repository-wide scan in the primary context; continue with targeted inspection or user-provided context.

For external dependencies, use the active harness's web/research capability or a narrowly scoped research agent when available.

## Workflow

1. **Establish context.** Determine whether the work is an existing project (with or without useful docs) or greenfield (with complete or incomplete requirements). Read user-supplied/authoritative docs first; treat code as evidence, not desired behavior.

2. **Discover requirements/evidence.** Do not ask for information that documentation or repository inspection can answer reliably. For greenfield work, establish only the architecture-relevant baseline: problem, users/scenarios, goals/non-goals, functional needs, constraints, integrations/data, scale/reliability assumptions, security/privacy/compliance, and rollout/migration needs.

3. **Build a knowledge map.** Classify information as facts, assumptions, decisions, or unknowns. Mark unknowns `blocking` only when plausible answers could materially change scope, architecture, safety, compatibility, cost, or another high-cost decision.

4. **Ask high-value questions.** Ask compact groups of blocking questions. For non-blocking unknowns, state an assumption or record an open issue. Never fabricate measurements, deadlines, owners, approvals, compatibility guarantees, or business constraints.

5. **Identify high-cost decisions.** Examples include system boundaries, public contracts, persistence/migrations, consistency/concurrency, infrastructure lock-in, trust/auth boundaries, failure/recovery, and compatibility/rollout strategy.

6. **Draft.** Use `references/design-doc-template.md` as a menu, not a form. Most non-trivial designs should make objective, background, goals, non-goals, proposed design, alternatives, assumptions, and open issues easy to find. Add interfaces/data/security/operations/testing/rollout sections only when useful.

7. **Review.** Use `references/review-checklist.md`. A reviewer should be able to understand the problem, scope, evidence vs assumptions, consequential decisions, alternatives, data/control flow, failure handling, constraints, and remaining questions without verbal context.

## Interaction and writing

Use `references/intake-guide.md` for question ideas, not as a mandatory questionnaire. Ask before finalizing when blocking context is missing; if the user explicitly accepts unresolved risk, document the assumption prominently.

Keep the document concise, decision-oriented, and self-contained. Avoid line-by-line implementation plans unless requested. Use tables/code snippets only when they improve understanding of comparisons, contracts, schemas, protocols, or configuration.

If asked to write the document into the repository and no convention/path is supplied, use `docs/design/<short-kebab-case-title>.md`; otherwise follow the repository's established design/RFC/ADR location.
