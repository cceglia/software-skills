# Software Engineering Skills

A multi-skill repository for reusable AI-agent workflows focused on software engineering.

The repository is intentionally structured so every skill is self-contained and can be installed independently.

## Available skills

| Skill | Version | Purpose |
|---|---:|---|
| `software-design-doc` | `1.0.0` | Create or review software design documentation with interactive requirements discovery and delegated codebase exploration. |

## Repository structure

```text
software-engineering-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
└── skills/
    └── software-design-doc/
        ├── SKILL.md
        ├── README.md
        ├── VERSION
        ├── CHANGELOG.md
        └── references/
            ├── intake-guide.md
            ├── design-doc-template.md
            └── review-checklist.md
```

Future skills should be added as siblings under `skills/`:

```text
skills/
├── software-design-doc/
├── code-review/
├── api-design/
└── refactoring-plan/
```

Each skill must remain self-contained.

## Install

List the skills exposed by the repository:

```bash
npx skills add OWNER/REPOSITORY --list
```

Install one skill for OpenCode:

```bash
npx skills add OWNER/REPOSITORY \
  --skill software-design-doc \
  --agent opencode
```

Install it globally:

```bash
npx skills add OWNER/REPOSITORY \
  --skill software-design-doc \
  --agent opencode \
  --global
```

Replace `OWNER/REPOSITORY` with your GitHub repository, for example `your-name/software-engineering-skills`.

## Skill versioning

Every skill is versioned independently using Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

The canonical version belongs in the skill's `SKILL.md` metadata:

```yaml
metadata:
  version: "1.0.0"
```

Each skill also contains:

- `VERSION` — a plain-text mirror of the current version for humans and simple tooling.
- `CHANGELOG.md` — the history of that individual skill.

Changing one skill does **not** require bumping the versions of unrelated skills.

Recommended increments:

- **PATCH** — wording fixes or small behavioral corrections that do not materially change the workflow.
- **MINOR** — backwards-compatible capabilities, new optional workflows, references, or meaningful behavior improvements.
- **MAJOR** — breaking behavioral changes, changed assumptions, removed workflows, or substantially different agent contracts.

### Git tags

For public releases, skill-specific tags are recommended:

```text
software-design-doc-v1.0.0
code-review-v1.2.0
```

This keeps release history understandable even when many independently versioned skills share one repository.

## Adding a new skill

Create a new directory:

```text
skills/<skill-name>/
```

At minimum it must contain:

```text
skills/<skill-name>/SKILL.md
```

Recommended structure:

```text
skills/<skill-name>/
├── SKILL.md
├── README.md
├── VERSION
├── CHANGELOG.md
└── references/
```

The `name` in `SKILL.md` must match the directory name.

Use `metadata.version` for the skill version so the manifest remains compatible with the Agent Skills specification.

## License

MIT. See `LICENSE`.
