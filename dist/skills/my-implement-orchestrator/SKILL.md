---
name: my-implement-orchestrator
description: Implement approved tracker tickets with develop/TDD and per-ticket commits, review a ticket individually only in exceptional high-risk cases, then gate the whole change with repeated Matt Pocock code-review cycles before tracker finalization.
license: MIT
compatibility: Claude Code with native skill controls.
disable-model-invocation: true
user-invocable: true
argument-hint: "[work item source]"
metadata:
  version: "4.9.1"
---

# my-implement-orchestrator

## Invocation

Explicit-only Claude Code workflow. Run `/my-implement-orchestrator`; never invoke it implicitly.

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

Implement approved tracker work without inventing requirements. Require Matt Pocock's `tdd`, `codebase-design` and `code-review`; if missing, return `BLOCKED`. Matt's `implement` and `implement-spec` are user-only upstream skills, so this orchestrator composes their model-invokable primitives instead.

Read repository instructions and `docs/agents/issue-tracker.md`. Before implementation, obtain a positive integer `MAX_REVIEW_CYCLES` and keep it fixed.

```text
per ticket:        develop(tdd+codebase-design) -> validation green -> commit
exceptional ticket: + code-review of that ticket -> (develop fix(tdd+codebase-design) -> commit -> new code-review)*
at the end:        code-review -> (develop fix(tdd+codebase-design) -> commit -> new code-review)* -> tracker finalization
```

A ticket's referenced SPEC is normative for requirements, decisions, acceptance criteria, and agreed test seams.

## Working copy

Work only in the current checkout of each involved repository: never create worktrees, branches, or pull requests, and never push. Record each repository's starting revision (`HEAD`) before the first ticket; it is the fixed point for the final `code-review` of that repository.

Run subagents sequentially. Parallelism is allowed only across different repositories, for tickets with no pending dependency between them; never run two subagents in the same repository at once.

## Develop

Process ready tickets one at a time in dependency order. Delegate each develop/fix pass to a fresh subagent with ticket/SPEC pointers and relevant repository context. Require it to load, in every ticket and fix pass, the mandatory skills `tdd` and `codebase-design`, plus every available skill specific to the language, framework or tool it will work with (discover them from the skills list; load the ones that match the files and tools the ticket touches). Require it to use only pre-agreed test seams, shape module interfaces with `codebase-design` without contradicting the SPEC, preserve unrelated changes, validate its work, report loaded/missing skills and changed files, and never commit or rewrite git history. A missing mandatory skill or a newly exposed product/domain decision blocks the ticket; a missing language/tool skill does not.

After each pass, re-run the project's tests and typecheck yourself. Only when they are green, create exactly one commit containing only that ticket's changes, excluding `./.agents/tmp/`, with the ticket reference in the message so `code-review` can find the spec. Preserve unrelated work and block if the boundary cannot be isolated safely.

## Exceptional ticket review

Do not review tickets individually by default; the final review covers them. Review a ticket on its own only for a high and concrete risk: a data migration, a risk of data loss, or a new security boundary. A public contract, or other tickets depending on it, is not enough. Before launching it, tell the user which ticket and why, and record the reason in the report. Then run `code-review` right after the ticket's commit with the commit before that ticket as fixed point, and apply the review loop before starting dependent tickets.

## Review loop

After all tickets are committed, invoke Matt's `code-review` per repository with the recorded starting revision as fixed point. Treat blocking Standards or Spec findings as `CHANGES_REQUIRED`; a blocked review is `BLOCKED`; otherwise the cycle is approved.

On `CHANGES_REQUIRED`, pass only the blocking findings to a fresh develop fix pass that loads the mandatory `tdd` and `codebase-design` skills, validate, commit the fixes (so `code-review` sees them), then run a **new `code-review`**. Repeat until approved or `MAX_REVIEW_CYCLES` is exhausted. Never finalize after fixes without a clean subsequent review.

## Finalize

After the final review is clean, finalize/update every ticket through the configured tracker; do not report completion if finalization fails.

Report ticket/SPEC references, commits per repository, tickets reviewed individually and why, review cycles, validation, tracker result, and blockers.

## Subagents

Never prescribe a subagent type: Claude Code chooses the most suitable available subagent for each delegation. State the delegated scope and constraints (read-only, no commits, skills to load, expected report) in the subagent prompt.
