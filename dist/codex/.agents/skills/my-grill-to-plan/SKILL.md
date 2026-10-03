---
name: my-grill-to-plan
description: Interview the user and inspect the repository to produce a complete implementation plan while persisting concise grilling state.
license: MIT
compatibility: Codex with native Agent Skills sidecars and project agents.
metadata:
  version: "2.2.0"
---

# my-grill-to-plan

## Invocation

Explicit-only Codex workflow. Invoke `$my-grill-to-plan`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use project agents in `.codex/agents/`: `explore`, `develop`, and `review`.

Load `grill-with-docs` and apply it to the invocation input. Use the read-only `explore` role when repository inspection is large enough to justify delegation; keep at most one active subagent.

## State

Maintain one resumable file:

```text
./.agents/tmp/grill/<plan-slug>.md
```

Create it at the start or resume the matching plan. Rewrite it as the current source of truth; do not append a transcript.

Keep only:

- `Status: in-progress | ready-for-spec`;
- goal and scope;
- resolved decisions and constraints;
- relevant repository evidence;
- rejected alternatives;
- open questions;
- current implementation plan.

Update the file whenever a material answer or repository finding changes the plan, before continuing the grill.

When no blocking question remains, persist the final plan, set `Status: ready-for-spec`, and return the plan plus state-file path.

Do not create a SPEC, tickets, or application-code changes.
