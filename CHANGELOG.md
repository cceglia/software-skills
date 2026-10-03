# Changelog

## 2.2.0 — 2026-10-03

- Removed `my-update-skills-list` and the generated `skills.json` registry.
- Switched implementation workflows to native harness skill discovery with explicit worker load verification.
- Moved all ephemeral workflow state under `./.agents/tmp/`.
- Changed the installer Git-exclude rule to `/.agents/tmp/`.
- Reduced canonical skill size and removed duplicated workflow instructions.
- Kept harness-native invocation metadata, agents, workflows, rules, and Codex sidecars.

## 2.1.0 — 2026-10-03

- Added the custom zero-dependency Node.js installer with interactive harness/layout selection.
- Added non-interactive `--harness`, `--layout`, `--target`, `--force`, `--dry-run`, and `--git-exclude` options.
- Added the shared `.agents/skills` profile and Codex + Antigravity collision handling.

## 2.0.0 — 2026-10-03

- Introduced one canonical workflow source plus native OpenCode V2, Codex, Claude Code, and Antigravity adapters.
