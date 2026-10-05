# Changelog — my-software-design-doc

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

# Changelog

All notable changes to `my-software-design-doc` are documented here.

This skill follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

## 1.0.0 - 2026-09-15

### Added

- Initial public version of the software design documentation skill.
- Interactive intake that asks where existing project documentation can be found.
- Explicit support for documented existing projects, undocumented existing projects, and greenfield projects.
- Requirements discovery when no useful documentation or implementation exists yet.
- Knowledge-gap analysis separating facts, assumptions, decisions, and unknowns.
- Blocking vs. non-blocking missing-information handling.
- Mandatory delegation of broad codebase exploration to OpenCode subagents.
- Design document template and final review checklist.