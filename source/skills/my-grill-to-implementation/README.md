# my-grill-to-implementation

Grill a change, persist decisions and execution state, then implement and independently review it without creating a SPEC or tickets.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-grill-to-implementation/SKILL.md` | `/my-grill-to-implementation` |
| Codex | `.agents/skills/my-grill-to-implementation/SKILL.md` + `agents/openai.yaml` | `$my-grill-to-implementation` |
| Claude Code | `.claude/skills/my-grill-to-implementation/SKILL.md` | `/my-grill-to-implementation` |
| Antigravity | `.agents/workflows/my-grill-to-implementation.md` | `/my-grill-to-implementation` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
