# Validation report — 2.5.1

Validated on 2026-10-04.

## Passed

- root `AGENTS.md` is present and contains the required maintenance invariants;
- 10 canonical skills; 9 explicit workflows;
- OpenCode V2, Codex, Claude Code, Antigravity, and shared `.agents` profiles build successfully;
- `my-grill-to-implementation` maps `explore`, `develop`, and `review` and requires Matt Pocock's `tdd` for develop/fix passes;
- `my-grill-to-spec` keeps only a resumable ledger under `.agents/tmp`, delegates canonical SPEC ownership to `to-spec`, uses a fresh post-publish reviewer, and stops before tickets;
- `my-spec-to-tickets` remains a thin `to-tickets` wrapper;
- `my-implement-orchestrator` requires `tdd` + `code-review` and enforces `develop -> review -> fix -> new review` before commit;
- no generated `skills.json`; runtime state stays under `./.agents/tmp/`;
- installer tests passed;
- `npm pack --dry-run` includes `AGENTS.md`, the generated native profiles, and hidden harness directories.

## Upstream invocation constraint

Matt Pocock currently marks `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, and `implement-spec` as user-invoked. Strict harnesses may therefore reject nested invocation of those user-only skills from another skill. This repository does not patch third-party skill invocation policy. `my-implement-orchestrator` avoids that problem by composing Matt's model-invokable `tdd` and `code-review` primitives.
