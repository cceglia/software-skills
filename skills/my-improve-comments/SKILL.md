---
name: my-improve-comments
description: Improve code comments and documentation with batched develop subagents.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-improve-comments

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/my-improve-comments`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

Improve comments and documentation in the requested scope.

Scope: `invocation input`

## Scope

- Empty scope means the entire repository.
- The scope may be a file, directory, package/module, function, or method.
- If a function/method is named, modify only it and its directly associated documentation comment when relevant.
- Resolve unambiguous targets from repository contents.
- Exclude generated code, vendored/third-party code, build artifacts, and files not maintained manually.

## Execution model

For a single explicit file, function, method, or similarly small unambiguous scope, the primary agent MUST perform the task directly.

Do not use `explore`, `develop`, or any other subagent for that small scope.

For an empty, directory, package/module, glob, multi-file, repository-wide, or otherwise broad scope, the primary agent becomes an orchestrator and MUST NOT edit source files directly.

Use exactly one active subagent at a time:

- `explore` — read-only scope discovery and batching;
- `develop` — edits one assigned batch only.

For a broad scope, run exactly one `explore` subagent first. It must:

- read applicable repository instructions;
- identify relevant manually maintained files;
- identify local conventions and files to skip;
- group **multiple related files per batch** whenever they share the same module, conventions, or change pattern;
- maximize useful work per batch while keeping the batch comfortably within one subagent context;
- prefer coherent multi-file batches over one-file batches;
- use a one-file batch only when that file is unusually large, complex, isolated, or has materially different instructions;
- keep batches non-overlapping and dependency-aware;
- return each batch with its file list, rationale, and order.

As a practical default, group several small/medium related files together (often roughly 5–20 files), but let repository structure and file size determine the real batch size rather than enforcing a fixed count.

The orchestrator MUST use that batch plan instead of broadly reading or editing the repository itself.

Process broad-scope batches sequentially. For each batch, run exactly one `develop` subagent.

The `develop` subagent must read `CODING_STANDARDS.md` plus applicable `AGENTS.md` / `CLAUDE.md`, process **all files in its assigned batch**, stay within the permitted editing boundary, preserve unrelated changes, run the appropriate formatter when available, and create no commits.

For direct small-scope execution, the primary agent must follow the same standards and editing boundary itself.

If a broad-scope batch cannot be completed safely, stop and report the blocker rather than continuing informally.


## Comment rules

Treat `CODING_STANDARDS.md` → `Comments & Documentation` as authoritative; preserve stricter applicable repository instructions.

- Prefer self-documenting code.
- Comments must add information not obvious from the code.
- Explain intent, rationale, constraints, assumptions, invariants, lifecycle/security behavior, compatibility, error strategy, architecture, or deliberate trade-offs when useful.
- Prefer **why** over paraphrasing **what** the next statement does.
- Remove stale, redundant, speculative, obsolete, or obvious comments.
- Keep useful TODO/FIXME comments and make them concrete when surrounding context supports it.
- Keep public/exported API documentation compliant with language conventions.
- Keep comments concise, technical, precise, and stable across minor implementation changes.

If a comment merely paraphrases the code, omit it.

## Editing boundary

The `develop` subagent MAY modify comments/documentation only, except minimal formatter-driven changes.

It MUST NOT change runtime behavior, control flow, expressions, names, APIs, contracts, architecture, or perform unrelated refactoring.

## Final report

Report:

- scope processed;
- execution mode (`direct` or `batched-subagents`);
- batch count and changed files when applicable;
- comment/documentation improvements;
- skipped or blocked files/batches.

Do not review or commit. Use `my-review-changes` separately when review is desired.
