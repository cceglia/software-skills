# Validation report — 4.0.0 (`claude` branch)

Validated on 2026-10-05.

## Passed

- root `AGENTS.md` is present and contains the required maintenance invariants;
- 5 canonical skills; 4 explicit workflows; `my-software-design-doc` stays model-invocable;
- skills removed in 4.0.0 are absent from source, generated profile, and installs;
- `dist/` contains only the Claude Code profile (`dist/skills/`);
- no generated skill uses `agent:`/`context:` frontmatter, names a subagent type, or references `.claude/agents`;
- every delegating skill carries the generated "never prescribe a subagent type" block;
- `my-grill-to-implementation` delegates exploration, development (with Matt Pocock's `tdd`), and a fresh review to subagents;
- installer tests passed for project scope, global scope (`~/.claude` and `$CLAUDE_CONFIG_DIR`), `--force`, `--dry-run`, leftover skill/agent notices, and git exclude;
- `npm pack --dry-run` includes `AGENTS.md` and `dist/skills/`.

## Upstream invocation constraint

Matt Pocock currently marks `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, and `implement-spec` as user-invoked. Claude Code may therefore reject nested invocation of those user-only skills from another skill. This repository does not patch third-party skill invocation policy.
