# software-skills

Native multi-harness software-engineering workflows for:

- OpenAI Codex
- Claude Code
- OpenCode V2
- Google Antigravity IDE

Repository: <https://github.com/cceglia/software-skills>

The repository keeps one canonical workflow source and generates harness-specific profiles. A custom zero-dependency Node.js installer lets you choose:

1. which harnesses to install;
2. whether skill packages go under the shared `.agents/skills` location or each harness' native project skill directory.

Harness-specific support files such as custom agents, workflows, rules, and Codex sidecars are installed automatically in the locations required by each runtime.

## Quick install

Run the installer directly from GitHub:

```bash
npx --yes github:cceglia/software-skills
```

The interactive installer asks:

```text
Select the harnesses to install:
  1) Codex
  2) Claude Code
  3) OpenCode V2
  4) Antigravity IDE
  a) All
Harnesses [comma-separated numbers, e.g. 1,2,4]:

Where should SKILL.md packages be installed?
  1) .agents/skills (shared Agent Skills location)
  2) Harness-native skill directories
Skill layout [1/2]:
```

Node.js 18+ is required. The installer itself has no npm runtime dependencies.


### Equivalent `npm exec` form

If you prefer the explicit npm package form:

```bash
npm exec --yes --package=github:cceglia/software-skills -- \
  software-skills \
  --harness all \
  --layout native
```

## Non-interactive install

Use `--harness` and `--layout` to skip the two interactive questions.

Install every harness using native skill directories:

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout native
```

Install every harness using one shared `.agents/skills` copy:

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout agents
```

Install Codex only:

```bash
npx --yes github:cceglia/software-skills \
  --harness codex \
  --layout native
```

Install Claude Code only:

```bash
npx --yes github:cceglia/software-skills \
  --harness claude-code \
  --layout native
```

Install OpenCode V2 only:

```bash
npx --yes github:cceglia/software-skills \
  --harness opencode \
  --layout native
```

Install Antigravity only:

```bash
npx --yes github:cceglia/software-skills \
  --harness antigravity \
  --layout native
```

Install a subset of harnesses:

```bash
npx --yes github:cceglia/software-skills \
  --harness codex,claude-code,opencode \
  --layout native
```

## Installer CLI reference

```text
software-skills [options]

--harness <list>
    Harnesses to install.
    Values: codex, claude-code, opencode, antigravity, all
    Multiple values are comma-separated.
    Example: --harness codex,claude-code

--layout <mode>
    Where SKILL.md packages are installed.
    Values: agents, native

    agents
        Use one shared .agents/skills installation.
        Harness-specific support files are still installed natively.

    native
        Use each harness' documented project skill directory.
        Claude Code -> .claude/skills
        OpenCode V2 -> .opencode/skills
        Codex -> .agents/skills
        Antigravity -> .agents/skills

--target <path>
    Project root to install into.
    Default: current working directory.

--force
    Overwrite existing managed files when their contents differ.
    Without --force, the installer stops rather than replacing them.

--dry-run
    Print every planned write without modifying the target project.

--git-exclude <mode>
    Controls whether /.agents/tmp/ is added to .git/info/exclude.
    Values: auto, yes, no
    Default: auto

    auto
        Add /.agents/tmp/ when the target is a Git repository or worktree.
        Otherwise do nothing.

    yes
        Require a Git repository and add /.agents/tmp/ if missing.

    no
        Never edit .git/info/exclude.

--help, -h
    Show installer help.

--version, -v
    Print installer version.
```

## Command examples with parameters

### Preview without writing

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout native \
  --dry-run
```

### Install into another repository

```bash
npx --yes github:cceglia/software-skills \
  --harness codex,claude-code \
  --layout native \
  --target ../my-project
```

### Overwrite an older installation

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout native \
  --force
```

### Use shared `.agents/skills` and overwrite existing managed files

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout agents \
  --force
```

### Do not touch `.git/info/exclude`

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout native \
  --git-exclude no
```

### Require `/.agents/tmp/` in the local Git exclude

```bash
npx --yes github:cceglia/software-skills \
  --harness codex \
  --layout native \
  --git-exclude yes
```

### Install into an explicit absolute path

```bash
npx --yes github:cceglia/software-skills \
  --harness opencode \
  --layout native \
  --target /path/to/project
```

### Show help

```bash
npx --yes github:cceglia/software-skills --help
```

### Show version

```bash
npx --yes github:cceglia/software-skills --version
```

## Pinning a branch, tag, or commit

Use npm's GitHub package syntax to run a specific repository ref.

Main branch:

```bash
npx --yes github:cceglia/software-skills#main
```

Tag:

```bash
npx --yes github:cceglia/software-skills#v2.2.0
```

Commit SHA:

```bash
npx --yes github:cceglia/software-skills#<commit-sha>
```

The same installer parameters can follow the package spec:

```bash
npx --yes github:cceglia/software-skills#main \
  --harness codex,claude-code \
  --layout native \
  --dry-run
```

## Running from a cloned repository

Clone:

```bash
git clone https://github.com/cceglia/software-skills.git
cd software-skills
```

Interactive:

```bash
node ./bin/software-skills.js
```

Non-interactive:

```bash
node ./bin/software-skills.js \
  --harness all \
  --layout native
```

Dry-run:

```bash
node ./bin/software-skills.js \
  --harness all \
  --layout native \
  --dry-run
```

Run against another project:

```bash
node ./bin/software-skills.js \
  --harness codex,opencode \
  --layout native \
  --target ../another-project
```

## What gets installed

### `--layout native`

| Harness | Skill packages | Harness-specific support files |
| --- | --- | --- |
| Codex | `.agents/skills/*` | `.codex/agents/*.toml`, `agents/openai.yaml` inside each skill |
| Claude Code | `.claude/skills/*` | `.claude/agents/*.md` |
| OpenCode V2 | `.opencode/skills/*` | `.opencode/agents/*.md` |
| Antigravity | `.agents/skills/*` | `.agents/workflows/*.md`, `.agents/rules/*`, `.agents/agents.md` |

Native layout is recommended when you want the strongest harness-specific behavior. For example, Claude Code's native skill profile can use `disable-model-invocation`, `user-invocable`, `argument-hint`, `context`, and `agent` fields directly in `SKILL.md`.

### `--layout agents`

Skill packages are installed once:

```text
.agents/skills/*
```

The shared profile is Agent-Skills-spec compliant. It also contains:

- OpenCode namespaced metadata under the standard `metadata` map;
- Codex `agents/openai.yaml` sidecars;
- explicit-only instructions in the skill descriptions/bodies.

Harness-specific support artifacts are still installed in their native locations:

```text
.codex/agents/*
.claude/agents/*
.opencode/agents/*
.agents/workflows/*
.agents/rules/*
.agents/agents.md
```

A single shared `SKILL.md` cannot simultaneously contain every vendor-only top-level frontmatter extension while remaining strictly compliant with the Agent Skills specification. Therefore, **native layout is the recommended mode when exact harness-specific invocation controls matter**. Shared layout is intended for teams that prefer one physical skill copy across compatible harnesses.

## Codex + Antigravity together

Codex and Antigravity both use `.agents/skills` as their documented project-level skill location. If both are selected with `--layout native`, the installer automatically uses the standards-compliant shared skill profile for that common directory, while still installing:

```text
.codex/agents/*
.agents/workflows/*
.agents/rules/*
.agents/agents.md
```

This prevents two different generated `SKILL.md` files from overwriting each other.

## Runtime state

All harnesses use:

```text
./.agents/tmp/grill/<plan-slug>.md
./.agents/tmp/implementation/<work-slug>.md
```

The workflows use `./.agents/tmp/` only for resumable runtime state and never include it in commits or code reviews. Skill selection uses each harness's native discovery; there is no generated skill registry.

By default the installer tries to add this rule to the repository-local Git exclude:

```text
/.agents/tmp/
```

It uses `.git/info/exclude` rather than changing the project's `.gitignore`.

## Existing files and `--force`

The installer is deliberately conservative. If a destination file already exists with different contents, installation stops and lists the conflicting files.

Inspect first:

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout native \
  --dry-run
```

Then overwrite only when intended:

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout native \
  --force
```

The installer does not delete unrelated files from harness directories.

## Source architecture

```text
source/skills/                    canonical workflow source
scripts/build.py                  generates harness profiles
scripts/validate.py               validates generated profiles
bin/software-skills.js            custom installer

dist/shared/.agents/skills/       standards-compliant shared profile
dist/codex/                       Codex-native profile
dist/claude-code/                 Claude Code-native profile
dist/opencode/                    OpenCode V2-native profile
dist/antigravity/                 Antigravity-native profile
```

Edit `source/skills/` first and regenerate distributions:

```bash
python3 scripts/build.py
```

Validate:

```bash
python3 scripts/validate.py
```

Test the installer:

```bash
npm test
```

## Native harness behavior

### OpenCode V2

The native profile uses `.opencode/skills`, OpenCode invocation metadata, the built-in `explore` agent, and bundled `develop` / `review` subagents.

### Codex

The profile uses `.agents/skills`, `agents/openai.yaml` invocation policy and UI metadata, plus project custom agents under `.codex/agents/`.

### Claude Code

The native profile uses `.claude/skills` with Claude-specific invocation/frontmatter properties and bundled project subagents under `.claude/agents/`.

### Antigravity

Manual workflows are native slash workflows under `.agents/workflows/`. The semantic design-document capability remains a skill. Runtime rules and specialized personas live under `.agents/rules/` and `.agents/agents.md`.

## License

MIT. See `LICENSE`.
