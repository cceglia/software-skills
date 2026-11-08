---
name: my-golang-codebase-design
description: Improve Go packages into deep modules with a narrow facade over internal domains, one package at a time, behind an allowlist gate.
license: MIT
compatibility: Claude Code with native skill controls.
disable-model-invocation: true
user-invocable: true
argument-hint: "[package | packages | directory]"
metadata:
  version: "4.9.0"
---

# my-golang-codebase-design

## Invocation

Explicit-only Claude Code workflow. Run `/my-golang-codebase-design`; never invoke it implicitly.

Treat `$ARGUMENTS` plus immediately relevant conversation context as the invocation input.

## Response style (ASD-STE100)

These defaults apply to every reply from this command or skill, unless the session has an explicit `/asd-ste100` directive. Precedence: the user's current instruction, then the session directive (including `off`), then these defaults.

- **Level:** 80. Apply the core rules below. Level 90 and above also require an exact word count and an audit of verb forms and terminology before you send.
- **Scope:** replies only. `docs` also applies the rules to documents that you write in chat. Code, paths, commands, identifiers, quoted errors, URLs, and files on disk stay unchanged. Explain them in plain prose.
- **Language:** answer in the user's language and apply these principles to it. English text follows ASD-STE100 literally. Other languages use the closest equivalent. For Italian, avoid `stare + gerundio`, compound tenses when a simple tense is clear, and long chains of subordinates.

### Core rules

1. Write one idea or one instruction in each sentence. Use a maximum of 20 words in a procedure and 25 words in a description.
2. Use the active voice. Use the passive voice only when the agent is unknown.
3. Use the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle as an adjective. Do not use the perfect, the progressive, or `-ing` as a verb in English.
4. Use plain and common words. Keep one term for one concept. Do not use nominalizations, avoidable phrasal verbs, filler, or hedging.
5. Keep compound nouns to three words. Write complete sentences and use articles.
6. Put one topic in each paragraph. Start the paragraph with a topic sentence. Use a maximum of six sentences.
7. Put a condition before its command. Do not use semicolons.
8. Keep a vertical list consistent: a colon after the lead-in, one marker style, a capital at the start, and a period only on complete sentences.
9. Do not change facts, code, or meaning. Do not invent values.

### Format

- Start with the result. Remove preambles, repeated summaries, and closing sentiment.
- Use a heading, a table, or a list only when it makes the content shorter or clearer.
- Never remove required report fields, evidence, risks, file paths, or verdict schemas. Apply the style to the prose around them.

### Delegation

When you delegate to a subagent, write this directive in the subagent prompt: the active level, the scope, the language rule, the core rules, and the precedence above. The subagent replies with the same style and keeps its report schema complete.

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

## Subagents

Never prescribe a subagent type: Claude Code chooses the most suitable available subagent for each delegation. State the delegated scope and constraints (read-only, no commits, skills to load, expected report) in the subagent prompt.
