---
name: my-spec-review
description: Loop an independent fresh review of a spec and its issues, fix the problems in the chosen scope (blocking only, all, or blocking then all), and stop only when a new review finds none in scope.
license: MIT
compatibility: Claude Code with native skill controls.
disable-model-invocation: true
user-invocable: true
argument-hint: "[spec | spec and issues]"
metadata:
  version: "4.11.0"
---

# my-spec-review

## Invocation

Explicit-only Claude Code workflow. Run `/my-spec-review`; never invoke it implicitly.

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

Make a spec and its issues correct, complete and consistent. Never approve by self-review: every verification runs in a fresh read-only subagent that has not seen earlier findings or fixes.

Read repository instructions and `docs/agents/issue-tracker.md`; if the tracker file is missing, return `BLOCKED` and ask the user to run `/setup-matt-pocock-skills`. `$ARGUMENTS` names the spec (and optionally its issues); empty means the most recent spec and the issues that reference it. Before the first cycle, obtain a positive integer `MAX_REVIEW_CYCLES` and ask the user for `FIX_SCOPE`; keep both fixed:

- `BLOCKING_ONLY`: fix only `BLOCKING` problems; `NON_BLOCKING` problems stay as notes.
- `ALL`: fix `BLOCKING` and `NON_BLOCKING` problems in every cycle.
- `BLOCKING_THEN_ALL`: run the `BLOCKING_ONLY` loop until clean, then fix the accumulated notes and continue as `ALL`.

```text
BLOCKING_ONLY:     verify -> blocking? -> fix blocking -> new fresh verify -> ... -> no blocking
ALL:               verify -> any problem? -> fix all -> new fresh verify -> ... -> no problems
BLOCKING_THEN_ALL: BLOCKING_ONLY loop -> fix notes -> ALL loop
```

## Verify

Delegate to a fresh read-only subagent per cycle. It never sees earlier findings or fixes. While notes are kept (`BLOCKING_ONLY`, and the first phase of `BLOCKING_THEN_ALL`), also give it the accumulated non-blocking notes (location and title only); it must not re-verify, re-report or re-rank them. It checks, against the code and the domain docs:

- Spec: contradictions, ambiguity, missing decisions, acceptance criteria that cannot be tested, test seams that are absent or wrong, claims about the code that are false.
- Issues: each issue traces to the spec, no spec requirement lacks an issue, dependencies and order are correct, scope and acceptance criteria match the spec, no duplicates or overlap.
- Spec and issues together: terminology, names and decisions are identical in both.

It returns `PROBLEMS` (possibly empty) with location, evidence, impact, a proposed fix and a class: `BLOCKING` (wrong, contradictory, untestable, missing or misleading enough to break implementation) or `NON_BLOCKING`. Reject nitpicks that change no meaning. While notes are kept, add each new `NON_BLOCKING` problem to the notes; a note is not verified again.

## Fix

The problems to fix are those in `FIX_SCOPE` for the current phase. For each, decide yourself when the spec or domain docs already define the answer. When the answer is a new product or domain decision, ask the user, then continue. Pass only the decided problems to one fix pass that edits the spec and issues through the tracker defined in `docs/agents/issue-tracker.md`, preserves unrelated content, and does not implement code. Never commit, push or create branches unless the tracker file prescribes it for specs.

## Loop

Repeat verify and fix. A fix always requires a new fresh verification: never stop after fixing. A loop is clean when a fresh verification returns no problems in scope: no `BLOCKING` problems for `BLOCKING_ONLY`, no problems at all for `ALL`. For `BLOCKING_THEN_ALL`, when the first loop is clean, fix the notes, drop them, and start the `ALL` loop with a new fresh verification. `MAX_REVIEW_CYCLES` bounds each loop; if it is exhausted with problems in scope left, return `CHANGES_REQUIRED` with them instead of reporting success.

Report spec and issue references, `FIX_SCOPE`, cycles run, problems found and fixed per cycle (by class), decisions the user made, final verdict (`CLEAN`, `CHANGES_REQUIRED` or `BLOCKED`), the non-blocking notes left unfixed, and blockers.

## Subagents

Never prescribe a subagent type: Claude Code chooses the most suitable available subagent for each delegation. State the delegated scope and constraints (read-only, no commits, skills to load, expected report) in the subagent prompt.
