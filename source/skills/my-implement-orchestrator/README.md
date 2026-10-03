# my-implement-orchestrator

Implement approved tracker tickets one at a time with independent review, bounded fixes, task-scoped commits and tracker finalization.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-implement-orchestrator/SKILL.md` | `/my-implement-orchestrator` |
| Codex | `.agents/skills/my-implement-orchestrator/SKILL.md` + `agents/openai.yaml` | `$my-implement-orchestrator` |
| Claude Code | `.claude/skills/my-implement-orchestrator/SKILL.md` | `/my-implement-orchestrator` |
| Antigravity | `.agents/workflows/my-implement-orchestrator.md` | `/my-implement-orchestrator` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
