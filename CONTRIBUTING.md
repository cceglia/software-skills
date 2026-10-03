# Contributing

## Source of truth

Edit `source/skills/<skill-name>/`; never hand-edit `dist/`. Regenerate with `python3 scripts/build.py`.

Canonical `SKILL.md` files stay harness-neutral. Harness-specific frontmatter, sidecars, agents, workflows, and rules belong in `scripts/build.py`.

## Runtime invariants

Ephemeral state is limited to:

```text
./.agents/tmp/grill/
./.agents/tmp/implementation/
```

There is no skill registry. Workflows select skills through the active harness's native discovery; delegated workers must load the exact selected skills and block when a required skill is unavailable.

Never stage, commit, or review `./.agents/tmp/`. Do not ignore `.agents/` globally.

## Skill style

Keep `SKILL.md` concise and single-source-of-truth:

- state each invariant once;
- prefer short workflow steps over repeated prose;
- keep harness mapping out of canonical bodies;
- reference supporting files instead of duplicating long guidance;
- preserve exact output schemas only when callers depend on them.

## Versioning and validation

Keep repository-wide versions synchronized for adapter/contract changes. Update the skill `VERSION` and changelog when semantics change.

Run:

```bash
python3 scripts/build.py
python3 scripts/validate.py
npm test
npm pack --dry-run
```

Validation must confirm native invocation behavior, isolated review where required, no obsolete registry/runtime paths, and no canonical/generated skill over 250 lines.
