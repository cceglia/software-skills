# Changelog — my-improve-spacing

## 4.11.0 — 2026-11-13

- Package version synchronized with the removal of `my-golang-codebase-design`; no skill-specific behavior change.

## 4.8.0 — 2026-11-01

- Package version synchronized with the new `my-golang-codebase-design` skill; no skill-specific behavior change.

## 4.7.0 — 2026-10-31

- Package version synchronized with the mandatory `codebase-design` change; no skill-specific behavior change.

## 4.6.0 — 2026-10-31

- Package version synchronized with the shared ASD-STE100 response style; replies now follow level 80 by default.

## 4.3.0 — 2026-10-06

- Package version synchronized with the exceptional-review change; no skill-specific behavior change.

## 4.2.0 — 2026-10-06

- Package version synchronized with the restored `my-implement-orchestrator`; no skill-specific behavior change.

## 4.1.0 — 2026-10-05

- Package version synchronized with the `my-grill-to-implementation` flow update; no skill-specific behavior change.

## 4.0.0 — 2026-10-05

- Package version synchronized with the removal of workflows now covered by Matt Pocock's skills; no skill-specific behavior change.

## 3.0.0 — 2026-10-05

- Claude Code-only profile: installs into project `.claude/skills` or global `~/.claude/skills`.
- Subagent delegation no longer names a subagent type; Claude Code chooses the most suitable subagent.

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

- Converted the former `software-commands` `my-improve-spacing` command into an OpenCode V2 skill.
- Enabled explicit slash invocation.
- Disabled model auto-invocation with `metadata.opencode/autoinvoke: "false"`.
- Replaced command-template `$ARGUMENTS` semantics with explicit invocation-input semantics.