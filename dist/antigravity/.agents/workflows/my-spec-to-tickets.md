---
description: Turn an approved canonical SPEC into implementation tickets by delegating decomposition and publishing to Matt Pocock's to-tickets skill.
---


# my-spec-to-tickets

## Invocation

Explicit-only Antigravity workflow. Run `/my-spec-to-tickets`; never trigger it through semantic skill matching.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

Require Matt Pocock's `to-tickets`; if unavailable, return `BLOCKED`.

Resolve the approved canonical SPEC from invocation input. Invoke `to-tickets` with that SPEC as source of truth and let it own decomposition, dependencies, approval quiz, and tracker destination. Do not duplicate those rules, edit the SPEC, or start implementation.

Return the created ticket references and any blocker, then stop.
