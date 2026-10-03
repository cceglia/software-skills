# my-review-changes

Review a specified set of modified files, or the current working-tree changes, using one independent read-only review subagent.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-review-changes/SKILL.md` | `/my-review-changes` |
| Codex | `.agents/skills/my-review-changes/SKILL.md` + `agents/openai.yaml` | `$my-review-changes` |
| Claude Code | `.claude/skills/my-review-changes/SKILL.md` | `/my-review-changes` |
| Antigravity | `.agents/workflows/my-review-changes.md` | `/my-review-changes` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
