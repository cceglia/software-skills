# Claude Code references

The Claude Code profile was checked against the following product documentation on 2026-10-05.

- Skills: https://code.claude.com/docs/en/skills
- Subagents: https://code.claude.com/docs/en/sub-agents

Adapter assumptions: project skills under `.claude/skills`, personal skills under `~/.claude/skills` (`$CLAUDE_CONFIG_DIR/skills` when set), `disable-model-invocation`, `user-invocable`, `argument-hint`, and `$ARGUMENTS` substitution. Skills do not use `context: fork`/`agent` and no project subagents are installed: Claude Code chooses the subagent for each delegation.

Codex, OpenCode V2, and Antigravity references are maintained on the `main` branch.
