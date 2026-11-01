# Changelog — my-golang-codebase-design

## 4.8.0 — 2026-11-01

- Added `/my-golang-codebase-design`: reshapes Go packages into deep modules with Matt Pocock's `codebase-design` skill (mandatory; `BLOCKED` when missing) plus the available Go skills. Every package gets a narrow facade and an `internal/<domain>`; the skill migrates one package at a time in dependency order, preserves behavior and public contracts, validates with `go build`, `go vet`, tests and the Makefile allowlist gate, and records the decision with a new ADR plus a `Package layout` section in `CODING_STANDARDS.md`. `cmd/*` is excluded.
- The skill is explicit-only, like the other improvement workflows, and does not review or commit.
