---
name: my-spec-to-tickets
description: Turn an approved canonical SPEC into implementation tickets by delegating decomposition and publishing to Matt Pocock's to-tickets skill.
license: MIT
compatibility: Canonical multi-harness source; use scripts/build.py to generate native profiles.
metadata:
  version: "2.5.1"
---

# my-spec-to-tickets

Require Matt Pocock's `to-tickets`; if unavailable, return `BLOCKED`.

Resolve the approved canonical SPEC from invocation input. Invoke `to-tickets` with that SPEC as source of truth and let it own decomposition, dependencies, approval quiz, and tracker destination. Do not duplicate those rules, edit the SPEC, or start implementation.

Return the created ticket references and any blocker, then stop.
