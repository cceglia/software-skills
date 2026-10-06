# OpenCode V2 references

The OpenCode V2 profile was checked against the following product documentation on 2026-10-03.

- Skills: https://opencode.ai/v2/docs/skills
- Agents: https://opencode.ai/v2/docs/agents
- Permissions: https://opencode.ai/v2/docs/permissions

Adapter assumptions: project skills and agents under `.opencode/`, user-level ones under `~/.config/opencode` (`$OPENCODE_CONFIG_DIR` or `$XDG_CONFIG_HOME/opencode` when set), `slash`, `metadata.opencode/autoinvoke`, `metadata.opencode/slash`, V2 `subagent`, ordered `permissions`, built-in `explore`, project custom subagents.

Re-check these references before changing frontmatter, directories, agent configuration, invocation controls, or permission semantics.
