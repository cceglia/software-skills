---
name: my-spec-to-tickets
description: Explicit-only workflow. Turn an approved canonical SPEC into implementation tickets by delegating decomposition and publishing to Matt Pocock's to-tickets skill.
license: MIT
compatibility: Shared Agent Skills profile for Codex, Claude Code, OpenCode V2, and Antigravity; native support files install separately.
metadata:
  version: "2.5.1"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-spec-to-tickets

## Invocation

Explicit-only workflow. Run it only when the user explicitly requests it by name; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

Require Matt Pocock's `to-tickets`; if unavailable, return `BLOCKED`.

Resolve the approved canonical SPEC from invocation input. Invoke `to-tickets` with that SPEC as source of truth and let it own decomposition, dependencies, approval quiz, and tracker destination. Do not duplicate those rules, edit the SPEC, or start implementation.

Return the created ticket references and any blocker, then stop.
