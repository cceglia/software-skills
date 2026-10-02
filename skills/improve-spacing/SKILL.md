---
name: improve-spacing
description: Improve logical blank-line spacing with batched develop subagents.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# improve-spacing

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/improve-spacing`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

Improve logical blank-line spacing in the requested scope.

Scope: `invocation input`

## Scope

- Empty scope means the entire repository.
- The scope may be a file, directory, package/module, function, or method.
- If a function/method is named, modify only it.
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


## Spacing rules

Treat `CODING_STANDARDS.md` → `Functions & Methods` as authoritative; preserve stricter applicable repository instructions.

Within functions/methods, use blank lines to expose cohesive phases such as validation, guards, synchronization, state changes, argument preparation, external calls, persistence/I/O, cleanup, and final result construction.

- Keep statements together when they implement one operation or decision.
- Do not insert blank lines mechanically.
- Do not split cohesive operations.
- Remove excessive or misleading blank lines.
- Preserve compact language idioms and formatter conventions.
- Do not refactor long functions; report them instead.

## Editing boundary

The `develop` subagent MAY change whitespace only, except minimal formatter-driven changes.

It MUST NOT add/remove/rewrite comments or change runtime behavior, control flow, expressions, names, APIs, contracts, or architecture.

## Final report

Report:

- scope processed;
- execution mode (`direct` or `batched-subagents`);
- batch count and changed files when applicable;
- logical-spacing improvements;
- skipped or blocked files/batches;
- functions that remain structurally difficult to read.

Do not review or commit. Use `review-changes` separately when review is desired.
