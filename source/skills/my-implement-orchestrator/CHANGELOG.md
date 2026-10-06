# Changelog — my-implement-orchestrator

## 4.3.0 — 2026-10-06

- Individual ticket `code-review` restricted to data migration, data-loss risk, or a new security boundary; announced to the user first.

## 4.2.0 — 2026-10-06

- Restored after its removal in 4.0.0.
- Per ticket: develop(tdd) -> green validation -> commit. Only important tickets (high-risk or foundational) get their own `code-review`; one `code-review` of the whole change runs at the end, with fix -> commit -> new review cycles before tracker finalization.
- Works only in the current checkout: no worktrees, branches, pull requests, or pushes. Subagents run sequentially; parallelism only across different repositories.

## 3.0.0 — 2026-10-05

- Claude Code-only profile: installs into project `.claude/skills` or global `~/.claude/skills`.
- Subagent delegation no longer names a subagent type; Claude Code chooses the most suitable subagent.

## 2.5.0 — 2026-10-03

- Replaced the invalid dependency on user-only `implement` with Matt Pocock's model-invokable `tdd`.
- Replaced the custom ticket review stage with Matt Pocock's `code-review`.
- Added a mandatory `develop -> code-review -> fix -> new code-review` loop; no commit is allowed after fixes until a subsequent clean review.

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

- Converted the former `software-commands` `my-implement-orchestrator` command into an OpenCode V2 skill.
- Enabled explicit slash invocation.
- Disabled model auto-invocation with `metadata.opencode/autoinvoke: "false"`.
- Replaced command-template `$ARGUMENTS` semantics with explicit invocation-input semantics.