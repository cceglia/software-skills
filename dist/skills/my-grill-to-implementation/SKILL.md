---
name: my-grill-to-implementation
description: Grill a small change, keep a resumable implementation ledger, then explore, implement every slice with Matt Pocock's tdd and per-slice commits, and gate the whole change with a final independent review and fix/review cycles.
license: MIT
compatibility: Claude Code with native skill controls.
disable-model-invocation: true
user-invocable: true
argument-hint: "[change request | .agents/tmp/implementation state]"
metadata:
  version: "4.10.0"
---

# my-grill-to-implementation

## Invocation

Explicit-only Claude Code workflow. Run `/my-grill-to-implementation`; never invoke it implicitly.

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

Use this light path only when SPEC/tickets would add unnecessary ceremony. Require Matt Pocock's `grill-with-docs`, `tdd` and `codebase-design`; delegate exploration, development, and a fresh independent review to subagents.

```text
per slice:  develop(tdd+codebase-design) -> validation green -> commit
at the end: fresh review -> (develop fix(tdd+codebase-design) -> commit -> new fresh review)* -> completed
```

## Ledger

Maintain one resumable, temporary ledger at `./.agents/tmp/implementation/<slug>.md` containing only current truth: status, a pointer to the spec, repository evidence, starting revision per repository, slice progress, commits per slice, validation, review cycles/findings, and `Next action`. The ledger is never committed.

Statuses: `grilling | ready-for-implementation | exploring | developing | reviewing | fixing | blocked | completed`.

On resume, read the ledger first and reconcile with branch/HEAD/working tree. The spec is authoritative for intent; git/filesystem for existing code. Checkpoint after every material grill round, subagent result, commit, review result, and phase boundary.

## Spec

Read `docs/agents/issue-tracker.md` (and `docs/agents/domain.md`) first; if missing, return `BLOCKED` and ask the user to run `/setup-matt-pocock-skills`. The plan is the spec: write it as `spec.md` in the spec folder that tracker file defines (local markdown: `.scratch/<slug>/spec.md`) with scope/decisions, constraints, agreed test seams, and the ordered slices; never one ticket per slice. For a remote tracker with no folder, publish the same spec as one issue as the file prescribes and commit nothing for it.

## Working copy

Work only in the current checkout of each involved repository: never create worktrees, branches, or pull requests, and never push. Record each repository's starting revision (`HEAD`) before the first slice; every review compares against it.

Run subagents sequentially. Parallelism is allowed only across different repositories, for slices with no pending dependency between them; never run two subagents in the same repository at once.

## Workflow

1. Invoke `grill-with-docs`; update the ledger after each material round. When decisions and test seams are settled, write the spec with ordered testable slices, set `ready-for-implementation`, and obtain explicit implementation approval.
2. Delegate read-only exploration to a subagent; persist only implementation-relevant evidence.
3. Every slice is implemented by a subagent, never directly by you: for each slice in order, delegate development to a fresh subagent with the ledger/evidence and require it to load the mandatory skills `tdd` and `codebase-design` plus the smallest sufficient discovered skills. It implements only that slice, shapes module interfaces with `codebase-design` without contradicting the spec, never commits, preserves unrelated changes, validates its work, and reports loaded/missing skills, changed files, validation, and blockers. A missing mandatory skill blocks the slice; a missing language/tool skill does not. Re-run the project's tests and typecheck yourself; only when green, create exactly one commit with only that slice's changes, excluding the spec and `./.agents/tmp/`. Block if the boundary cannot be isolated safely.
4. Do not review slices individually by default. Only for a high and concrete risk (a data migration, a risk of data loss, or a new security boundary; a public contract or later slices depending on it is not enough), run an intermediate fresh review of that slice before later slices build on it, after telling the user which slice and why; its findings follow step 6.
5. After all slices are committed, delegate a **fresh** read-only review to a new subagent against `git diff <starting-revision>...HEAD`, the ledger, and validation evidence. Require `VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED` plus blocking findings.
6. On `CHANGES_REQUIRED`, persist only the blocking findings, delegate a new development fix pass that loads the mandatory `tdd` and `codebase-design` skills, validate, commit the fixes, then run another fresh review in a new subagent. Maximum 3 review cycles; never approve by self-review.
7. After a clean review, commit the spec as the last commit (never the ledger or `./.agents/tmp/`), record the commits, set `completed`, and stop.

## Subagents

Never prescribe a subagent type: Claude Code chooses the most suitable available subagent for each delegation. State the delegated scope and constraints (read-only, no commits, skills to load, expected report) in the subagent prompt.
