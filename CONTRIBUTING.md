# Contributing

## Skill layout

Add each skill under:

```text
skills/<skill-name>/
```

The directory should contain its own `SKILL.md` and any resources needed by that skill.

Do not place skill-specific references in a shared root directory unless multiple skills intentionally depend on the same stable asset.

## Frontmatter

Use Agent Skills-compatible frontmatter. Keep custom fields inside `metadata`.

Example:

```yaml
---
name: example-skill
description: Explain what the skill does and when the agent should use it.
license: MIT
compatibility: Describe environment requirements only when relevant.
metadata:
  version: "1.0.0"
---
```

## Versioning

Skills use Semantic Versioning independently.

When changing a skill:

1. Update `metadata.version` in `SKILL.md`.
2. Update the skill's `VERSION` file with exactly the same version.
3. Add an entry to the skill's `CHANGELOG.md`.
4. Update the version shown in the root `README.md` skill table.
5. Optionally create a Git tag such as `<skill-name>-v1.2.0`.

Do not bump unrelated skills.

## Validation checklist

Before publishing a skill:

- directory name and `name` field match
- `description` explains both behavior and activation conditions
- `metadata.version` and `VERSION` match
- referenced files exist
- no user-specific secrets, local paths, or credentials are present
- the skill remains self-contained
- the changelog has been updated
