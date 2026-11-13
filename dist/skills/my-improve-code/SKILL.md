---
name: my-improve-code
description: Improve comments/documentation and logical spacing without changing runtime behavior.
license: MIT
compatibility: Claude Code with native skill controls.
disable-model-invocation: true
user-invocable: true
argument-hint: "[scope]"
metadata:
  version: "4.11.0"
---

# my-improve-code

## Invocation

Explicit-only Claude Code workflow. Run `/my-improve-code`; never invoke it implicitly.

Treat `$ARGUMENTS` plus immediately relevant conversation context as the invocation input.

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

Improve comments/documentation and logical blank-line spacing in the invocation scope; empty scope means the repository. Exclude generated, vendored/third-party, build-artifact, and non-manually-maintained files.

For one small explicit target, edit directly. For broad scope, use one read-only exploration subagent to create coherent non-overlapping batches, then process batches sequentially with one editing subagent at a time. Each worker reads applicable repository instructions and `CODING_STANDARDS.md`, preserves unrelated changes, formats modified files when appropriate, and never commits.

Apply two passes to each target:

1. **Comments/documentation:** prefer self-documenting code; keep only comments that add non-obvious intent, rationale, constraints, invariants, lifecycle/security behavior, compatibility, error strategy, architecture, or trade-offs. Prefer **why** over paraphrasing **what**; remove stale/redundant comments while preserving useful TODO/FIXME and required API docs.
2. **Spacing:** use blank lines to expose cohesive phases; keep one operation together, remove excessive/misleading spacing, preserve language/formatter idioms, and report long functions instead of refactoring them.

Editing boundary: comments/documentation, whitespace, and unavoidable formatter changes only. Never change behavior, control flow, expressions, algorithms, names, APIs, contracts, or architecture.

Report scope, direct/batched mode, changed files, comment and spacing improvements, skipped/blocked areas, and structurally difficult functions. Do not review or commit.

## Subagents

Never prescribe a subagent type: Claude Code chooses the most suitable available subagent for each delegation. State the delegated scope and constraints (read-only, no commits, skills to load, expected report) in the subagent prompt.
