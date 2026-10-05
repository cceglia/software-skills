# Validation report — 3.0.0 (`claude` branch)

Validated on 2026-10-05.

## Passed

- root `AGENTS.md` is present and contains the required maintenance invariants;
- 10 canonical skills; 9 explicit workflows;
- `dist/` contains only the Claude Code profile (`dist/skills/`);
- no generated skill uses `agent:`/`context:` frontmatter, names a subagent type, or references `.claude/agents`;
- every delegating skill carries the generated "never prescribe a subagent type" block;
- `my-grill-to-implementation` delegates exploration, development (with Matt Pocock's `tdd`), and a fresh review to subagents;
- `my-grill-to-spec` keeps only a resumable ledger under `.agents/tmp`, delegates canonical SPEC ownership to `to-spec`, uses a fresh post-publish reviewer, and stops before tickets;
- `my-spec-to-tickets` remains a thin `to-tickets` wrapper;
- `my-implement-orchestrator` requires `tdd` + `code-review` and enforces `develop -> review -> fix -> new review` before commit;
- installer tests passed for project scope, global scope (`~/.claude` and `$CLAUDE_CONFIG_DIR`), `--force`, `--dry-run`, legacy-agent notice, and git exclude;
- `npm pack --dry-run` includes `AGENTS.md` and `dist/skills/`.

## Upstream invocation constraint

Matt Pocock currently marks `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, and `implement-spec` as user-invoked. Claude Code may therefore reject nested invocation of those user-only skills from another skill. This repository does not patch third-party skill invocation policy. `my-implement-orchestrator` avoids that problem by composing Matt's model-invokable `tdd` and `code-review` primitives.
