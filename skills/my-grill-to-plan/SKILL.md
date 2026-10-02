---
name: my-grill-to-plan
description: Interview the user and inspect the repository to produce a complete implementation plan in chat while continuously persisting grilling state.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-grill-to-plan

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/my-grill-to-plan`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

Load the `grill-with-docs` skill and follow it for `invocation input`.

Use repository exploration subagents when needed, with only one active subagent at a time.

## Persistent grilling state

Maintain one persistent state file for this planning session:

```text
.opencode/grill/<plan-slug>.md
```

Create it at the start, or resume the existing file when continuing the same plan.

Keep it concise and rewrite it as the current source of truth rather than appending a transcript.

Track:

* `Status`: `in-progress` or `ready-for-spec`;
* goal and scope;
* resolved decisions;
* constraints;
* repository evidence relevant to decisions;
* rejected alternatives and reasons;
* open questions;
* current implementation plan.

Whenever a user answer, repository finding, or reconsideration changes the plan, update the state file **before asking the next question or continuing the grill**.

Do not use `CONTEXT.md` as grilling state; leave it to `grill-with-docs` for durable domain vocabulary and documentation.

At completion:

1. ensure there are no unresolved blocking questions;
2. update the state file with the final consolidated plan;
3. set `Status: ready-for-spec`;
4. return the consolidated plan in the current chat and include the state-file path.

Do not create a SPEC, create tickets, implement the feature, or modify application code.

invocation input
