# Changelog — my-grill-to-implementation

## 3.1.1 — 2026-10-06

- Stated explicitly that every slice is implemented by a subagent, never directly by the orchestrator; the final fresh review is unchanged.

## 3.1.0 — 2026-10-06

- Intermediate slice review restricted to data migration, data-loss risk, or a new security boundary; announced to the user first.

## 3.0.0 — 2026-10-06

- OpenCode V2-only distribution; installer asks only for project or global scope.
- Each slice is developed with `tdd` by a fresh `develop` role and committed after green tests/typecheck; one fresh `review` of the whole change runs at the end, followed by fix -> commit -> new review cycles (max 3). The single final commit is gone.
- Optional intermediate review after high-risk slices, at the agent's discretion.
- Works only in the current checkout: no worktrees, branches, pull requests, or pushes. Roles run sequentially; parallelism only across different repositories.

## 2.5.0 — 2026-10-03

- Develop now explicitly loads Matt Pocock's `tdd` at pre-agreed seams.
- Preserved the `explore -> develop -> fresh review -> fix/review` light workflow and resumable ledger.

## 2.4.0 — 2026-10-03

- Development now explicitly runs `explore -> develop -> review`.
- Strengthened fresh-session resume checkpoints and `Next action`.

## 2.3.0 — 2026-10-03

- Package version synchronized with the grill-to-SPEC workflow update; no skill-specific behavior change.

## 2.2.0 — 2026-10-03

- Removed the generated skill registry and switched routing to native harness skill discovery.
- Moved ephemeral workflow state under `./.agents/tmp/`.
- Reduced duplicated workflow instructions and tightened the skill contract.

## 2.0.0 — 2026-10-03

- Added native OpenCode V2, Codex, Claude Code, and Antigravity adapters generated from one canonical workflow.
- Moved harness-local runtime state to `./.agents/tmp/` where applicable.
- Preserved explicit/manual invocation semantics using each harness's native controls.
- Added harness-native delegation/review primitives instead of relying on OpenCode-specific worker syntax.

## 1.0.0 — 2026-10-02

- Converted the former `software-commands` `my-grill-to-implementation` command into an OpenCode V2 skill.
- Enabled explicit slash invocation.
- Disabled model auto-invocation with `metadata.opencode/autoinvoke: "false"`.
- Replaced command-template `$ARGUMENTS` semantics with explicit invocation-input semantics.