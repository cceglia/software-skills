---
name: my-improve-code
description: Improve comments/documentation and logical spacing with batched develop subagents, without changing behavior.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-improve-code

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/my-improve-code`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

Improve comments/documentation **and** logical blank-line spacing in the requested scope.

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


For each batch, the same `develop` subagent performs both passes.

## Pass 1 — comments/documentation

Treat `CODING_STANDARDS.md` → `Comments & Documentation` as authoritative.

- Prefer self-documenting code.
- Keep comments only when they add non-obvious intent, rationale, constraints, invariants, lifecycle/security behavior, compatibility, error strategy, architecture, or deliberate trade-offs.
- Prefer **why** over paraphrasing **what** the code does.
- Remove stale, redundant, speculative, obsolete, or obvious comments.
- Keep useful TODO/FIXME comments and public/exported API documentation compliant with local conventions.
- Keep comments concise and stable.

## Pass 2 — logical spacing

Treat `CODING_STANDARDS.md` → `Functions & Methods` as authoritative.

Use blank lines to expose cohesive phases such as validation, guards, synchronization, state changes, argument preparation, external calls, persistence/I/O, cleanup, and final result construction.

- Keep cohesive operations together.
- Do not insert blank lines mechanically.
- Remove excessive or misleading blank lines.
- Preserve compact language idioms and formatter conventions.
- Do not refactor long functions; report them instead.

## Editing boundary

The `develop` subagent MAY change only:

- comments/documentation;
- blank-line/whitespace formatting;
- minimal formatter-driven formatting required for modified files.

It MUST NOT change runtime behavior, expressions, algorithms, control flow, names, APIs, contracts, or architecture, and MUST NOT perform unrelated refactoring.

## Final report

Report:

- scope processed;
- execution mode (`direct` or `batched-subagents`);
- batch count and changed files when applicable;
- comment/documentation improvements;
- logical-spacing improvements;
- skipped or blocked files/batches;
- functions that remain structurally difficult to read.

Do not review or commit. Use `my-review-changes` separately when review is desired.
