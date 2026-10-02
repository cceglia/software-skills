# Software Engineering Skills

A multi-skill repository for reusable AI-agent workflows focused on software engineering.

The repository is intentionally structured so every skill is self-contained and can be installed independently.

## Available skills

| Skill | Version | Purpose | Invocation |
|---|---:|---|---|
| `my-software-design-doc` | `1.0.0` | Create or review software design documentation with interactive requirements discovery and delegated codebase exploration. | automatic/on-demand |
| `my-git-commit` | `1.0.0` | Git commit ALL changes in files. Never amends. | explicit `/my-git-commit` only |
| `my-grill-to-implementation` | `1.0.0` | Grill a change, persist decisions and execution state, then implement and independently review it without creating a SPEC or tickets. | explicit `/my-grill-to-implementation` only |
| `my-grill-to-plan` | `1.0.0` | Interview the user and inspect the repository to produce a complete implementation plan in chat while continuously persisting grilling state. | explicit `/my-grill-to-plan` only |
| `my-implement-orchestrator` | `1.0.0` | Implement approved tracker tickets one at a time with independent review, bounded fixes, task-scoped commits and tracker finalization. | explicit `/my-implement-orchestrator` only |
| `my-improve-code` | `1.0.0` | Improve comments/documentation and logical spacing with batched develop subagents, without changing behavior. | explicit `/my-improve-code` only |
| `my-improve-comments` | `1.0.0` | Improve code comments and documentation with batched develop subagents. | explicit `/my-improve-comments` only |
| `my-improve-spacing` | `1.0.0` | Improve logical blank-line spacing with batched develop subagents. | explicit `/my-improve-spacing` only |
| `my-plan-to-spec` | `1.0.0` | Turn a completed grilling state and resolved plan into a reviewed, implementation-ready SPEC and publish it through the configured tracker. | explicit `/my-plan-to-spec` only |
| `my-review-changes` | `1.0.0` | Review a specified set of modified files, or the current working-tree changes, using one independent read-only review subagent. | explicit `/my-review-changes` only |
| `my-spec-to-tickets` | `1.0.0` | Decompose an approved SPEC into concise implementation tickets, review only the tickets, and publish them through the configured tracker. | explicit `/my-spec-to-tickets` only |
| `my-update-skills-list` | `1.0.0` | Read all SKILL.md files from user and project skill directories and regenerate ./.opencode/skills.json. | explicit `/my-update-skills-list` only |

The skills converted from `software-commands` are **manual-only on OpenCode V2**: each has `slash: true` and `metadata.opencode/autoinvoke: "false"`, so it remains callable with `/...` without being advertised to the model for automatic selection.
## Repository structure

```text
software-engineering-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
└── skills/
    ├── my-software-design-doc/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── VERSION
    │   ├── CHANGELOG.md
    │   └── references/
    ├── my-git-commit/
    │   └── ...
    ├── my-grill-to-implementation/
    │   └── ...
    └── <other-skill>/
        ├── SKILL.md
        ├── README.md
        ├── VERSION
        └── CHANGELOG.md
```

Each skill remains self-contained. Converted command skills preserve their former command ID as the skill directory/ID.

## Install

List the skills exposed by the repository:

```bash
npx skills add OWNER/REPOSITORY --list
```

Install one skill for OpenCode:

```bash
npx skills add OWNER/REPOSITORY \
  --skill my-software-design-doc \
  --agent opencode
```

Install it globally:

```bash
npx skills add OWNER/REPOSITORY \
  --skill my-software-design-doc \
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
my-software-design-doc-v1.0.0
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
