# Validation report — 4.6.0 (`claude` branch)

Validated on 2026-10-31.

## Passed

- root `AGENTS.md` is present and contains the required maintenance invariants;
- 7 canonical skills; 6 explicit workflows; `my-software-design-doc` stays model-invocable;
- `source/shared/response-style.md` is the only canonical response-style source; every generated skill carries it at default level 80;
- `asd-ste100` is slash-only (`disable-model-invocation: true`, `user-invocable: true`), asks level and scope with `AskUserQuestion` only without arguments, and supports `help`, `status`, `off`, `replies`, and `docs`;
- every skill writes the active directive into subagent prompts, and report/verdict contracts keep precedence over style;
- skills removed in 4.0.0 (except the restored `my-implement-orchestrator`) are absent from source, generated profile, and installs;
- `dist/` contains only the Claude Code profile (`dist/skills/`);
- no generated skill uses `agent:`/`context:` frontmatter, names a subagent type, or references `.claude/agents`;
- every delegating skill carries the generated "never prescribe a subagent type" block;
- `my-grill-to-implementation` delegates exploration and per-slice development (with Matt Pocock's `tdd`), commits each slice after green validation, and gates the whole change with a final fresh review and fix -> commit -> new review cycles; no worktrees, PRs, or pushes;
- `my-implement-orchestrator` commits per ticket after green validation, reviews only important tickets individually, and gates the whole change with a final `code-review` and fix -> commit -> new review cycles before tracker finalization; no worktrees, PRs, or pushes;
- installer tests passed for project scope, global scope (`~/.claude` and `$CLAUDE_CONFIG_DIR`), `--force`, `--dry-run`, leftover skill/agent notices, and git exclude;
- `npm pack --dry-run` includes `AGENTS.md` and `dist/skills/`.

## Upstream invocation constraint

Matt Pocock currently marks `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, and `implement-spec` as user-invoked. Claude Code may therefore reject nested invocation of those user-only skills from another skill. This repository does not patch third-party skill invocation policy.
