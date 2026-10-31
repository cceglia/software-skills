---
name: asd-ste100
description: Set the ASD-STE100 response style for the session, at a level and scope you choose.
license: MIT
compatibility: Canonical Claude Code source; use scripts/build.py to generate the installable profile.
metadata:
  version: "4.6.0"
---

# asd-ste100

## Activation

Read `$ARGUMENTS` and follow the first matching case.

- **No arguments:** call the environment's question tool once, with both questions in the same call:
  - Level: `80 (default)`, `60`, `90`, `100`, or a custom number.
  - Scope: `Replies only (default)` or `Replies and in-chat documents`.

  If the user cancels or gives no answer, use level 80 and replies only. Then print the confirmation line.

- **`help`:** print the level table and the syntax below. Do not activate or change the session.

- **`off`:** deactivate the style for the rest of the session, including the default 80 that skills carry. Print the confirmation line.

- **`status`:** print the active level and scope. Do not change them.

- **A level, a scope, or both:** apply them without a question. `replies` means replies only. `docs` means replies and in-chat documents. An unknown word or a number outside 1-100 is invalid: ask one short question with the environment's question tool and change nothing.

## Levels

| Level | Rules |
| --- | --- |
| 1-39 | Short sentences, one idea per sentence, active voice, common words, no filler |
| 40-69 | + allowed verb forms, no nominalizations, no avoidable phrasal verbs, one term per concept, no semicolons |
| 70-89 (default 80) | + 20 words in a procedure and 25 in a description, paragraphs of 6 sentences or fewer with a topic sentence, compound nouns of 3 words or fewer, complete sentences, STE lists, condition before command |
| 90-100 | + exact word count and an audit of verb forms and terminology before you send |

## Syntax

```text
/asd-ste100                 ask level and scope
/asd-ste100 60 docs         level 60, replies and in-chat documents
/asd-ste100 replies         replies only, keep the level
/asd-ste100 help            show this table
/asd-ste100 status          show the active level and scope
/asd-ste100 off             deactivate
```

## Confirmation and persistence

- Confirmation, one line, in the user's language: `STE100 mode active: level <level>, scope <scope>, until the end of the session.` For `off`, use `STE100 mode off.`
- Keep the level and the scope in the session. Do not ask the user to repeat them.
- A later `/asd-ste100` replaces them. `off` clears them.
- Write the active directive in every subagent prompt, as described in **Delegation** above.
- If the session context is compacted, re-apply the last known directive. If you cannot find it, use level 80 and replies only.
