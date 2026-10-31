---
description: Improve logical blank-line spacing without changing behavior or comments.
---

# my-improve-spacing

## Invocation

User-invoked OpenCode V2 command. Treat `$ARGUMENTS` plus the immediately relevant conversation context as the invocation input.

## Harness roles

Use OpenCode V2 child-session roles: `explore`, `develop`.

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

Improve logical blank-line spacing in the invocation scope; empty scope means the repository. Exclude generated, vendored/third-party, build-artifact, and non-manually-maintained files.

For one small explicit target, edit directly. For broad scope, use one `explore` role to create coherent non-overlapping batches, then process batches sequentially with one `develop` role at a time. Each worker reads applicable repository instructions and `CODING_STANDARDS.md`, preserves unrelated changes, runs the appropriate formatter when useful, and never commits.

Use blank lines only to expose cohesive phases such as validation/guards, synchronization/state change, argument preparation, external calls, persistence/I/O, cleanup, and result construction. Keep one operation together, remove excessive or misleading spacing, preserve compact language idioms and formatter conventions, and report long functions instead of refactoring them.

Editing boundary: whitespace only, plus unavoidable formatter changes. Do not add/rewrite comments or change behavior, control flow, expressions, names, APIs, contracts, or architecture.

Report scope, direct/batched mode, changed files, spacing improvements, skipped/blocked areas, and structurally difficult functions. Do not review or commit.
