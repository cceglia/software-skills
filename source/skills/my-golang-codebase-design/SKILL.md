---
name: my-golang-codebase-design
description: Improve Go packages into deep modules with a narrow facade over internal domains, one package at a time, behind an allowlist gate.
license: MIT
compatibility: Canonical Claude Code source; use scripts/build.py to generate the installable profile.
metadata:
  version: "4.9.1"
---

# my-golang-codebase-design

Reshape Go packages into deep modules with Matt Pocock's `codebase-design` skill in every design and implementation pass. The interface is everything a caller must know; the implementation hides behind it.

**Require `codebase-design`. If it is missing, return `BLOCKED` and ask the user to install it.** Load the available Go skills that match the files and tools of the package.

## Target

`$ARGUMENTS` selects one package, a package list, or a directory; empty means the repository. Exclude `cmd/*`: a `main` has no interface to protect, so move logic into real packages and do not wrap it in a facade. Exclude generated, vendored, and non-manually-maintained files.

Migrate one package at a time, sequentially, in dependency order. Start from the pilot package the user names, otherwise from the package with the most external callers.

## Package layout rule

Every Go package has a facade and an `internal`. The facade names only what a caller must name: exported types with their public methods, constructors, constants, and errors used with `errors.Is`/`errors.As`. Helpers, intermediate steps, caches, heaps, and accumulators go unexported into `<package>/internal/<domain>`. Split by domain, not by file kind.

These constraints decide the shape:

- A method must live in the same package as its receiver type. Types with behavior therefore belong in the facade.
- Methods cannot be declared on an alias of a non-local type. Pure DTOs (JSON contracts) may live in `internal` and be exposed through an alias; their methods come from the alias.
- The import arrow is facade → internal only, never the reverse. Avoid a cycle by declaring in `internal` the interfaces it needs; facade types satisfy them structurally.
- Do not create an interface where only one implementation exists. A hypothetical seam is noise: use concrete types and constructors, except where variation is real.
- Expose only symbols that other packages actually consume. Everything else becomes unexported inside `internal`.
- Types genuinely shared across domains go in `internal/model`.

## Workflow

1. **Establish the baseline.** Read repository instructions, `CODING_STANDARDS.md`, the layout ADRs, the module graph, and the anti-drift gate in the Makefile (for example `programs/Makefile`). Record the exported surface and its external callers. Do not start a package when build, vet, or tests are already red.
2. **Plan the queue.** Delegate read-only exploration to a subagent and persist a temporary ledger at `./.agents/tmp/implementation/<slug>.md`: ordered packages, facade candidates, the `internal/<domain>` split, shared types, callers, tests, and the gate entry. The ledger is never committed.
3. **Design each interface.** Apply `codebase-design`: maximize depth (behavior per unit of interface), run the deletion test, place a seam only where variation is real, and treat the interface as the test surface. Prefer the smallest facade a caller can use correctly.
4. **Implement one package.** Delegate to an editing subagent that loads `codebase-design` and the Go skills. Move implementation into `internal/<domain>`, keep the facade minimal, and update every caller and test. Preserve behavior, output, error semantics, and public contracts. Never force a migration that cannot preserve them.
5. **Validate the package.** Run `go build ./...`, `go vet ./...`, the package and repository tests, and the gate target. Only a green result advances the queue.
6. **Close the gate.** Add the package to the Makefile allowlist in the same change, one package per entry, so the old layout cannot drift back. Make the gate global when the migration is finished.
7. **Record the decision.** If an existing ADR rejects the split, write a new ADR that supersedes it, with the pilot evidence, and add a `Package layout` section to `CODING_STANDARDS.md`. Do not edit the superseded ADR.

## Boundaries

- Stop at, do not decide, an edge case: return it with description, impact, and options.
- Preserve unrelated changes and format modified files.
- Do not review or commit. Report the change and let the user decide the commit and review path.
- Re-run validation after every package; a red result blocks the remaining queue.

## Report

Report the queue, the migrated packages with their facade/`internal` split, the symbols removed from the public surface, the callers updated, the gate entries, build/vet/test results, the ADR and `CODING_STANDARDS.md` updates, skipped packages and why, edge cases, and the packages that still use the old layout.
