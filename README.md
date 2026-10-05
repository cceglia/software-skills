# software-skills — Claude Code edition

Software-engineering workflows packaged as native **Claude Code** skills.

Repository: <https://github.com/cceglia/software-skills>

> This is the `claude` branch: it installs the skills **only for Claude Code**. The multi-harness version (Codex, OpenCode V2, Antigravity, shared `.agents/skills`) lives on `main`.

## Install

The skills live on the `claude` branch, so always reference it with `#claude` in the package spec:

```bash
npx --yes github:cceglia/software-skills#claude
```

The interactive installer asks where to install:

```text
Where should the Claude Code skills be installed?
  1) Project (/path/to/project/.claude/skills)
  2) Global (/home/you/.claude/skills)
Scope [1/2]:
```

| Scope | Destination | Available in |
| --- | --- | --- |
| `project` | `<target>/.claude/skills/` | that project only (can be committed and shared with the team) |
| `global` | `~/.claude/skills/` (or `$CLAUDE_CONFIG_DIR/skills/`) | every project on your machine |

Node.js 18+ is required. The installer has no npm runtime dependencies.

### Non-interactive install

Install into the current project:

```bash
npx --yes github:cceglia/software-skills#claude --scope project
```

Install globally for your user:

```bash
npx --yes github:cceglia/software-skills#claude --scope global
```

Install into another project:

```bash
npx --yes github:cceglia/software-skills#claude --scope project --target ../my-project
```

Preview without writing:

```bash
npx --yes github:cceglia/software-skills#claude --scope global --dry-run
```

Overwrite an older installation:

```bash
npx --yes github:cceglia/software-skills#claude --scope global --force
```

Pin a specific commit of the branch:

```bash
npx --yes github:cceglia/software-skills#<commit-sha> --scope project
```

Equivalent explicit `npm exec` form:

```bash
npm exec --yes --package=github:cceglia/software-skills#claude -- software-skills --scope project
```

### From a cloned repository

```bash
git clone --branch claude https://github.com/cceglia/software-skills.git
```

```bash
node ./software-skills/bin/software-skills.js --scope global
```

## Installer CLI reference

```text
software-skills [options]

--scope <scope>
    Where the skills are installed.
    Values: project, global (aliases: local/repo, user/personal)
    Asked interactively when omitted.

    project   <target>/.claude/skills
    global    ~/.claude/skills, or $CLAUDE_CONFIG_DIR/skills when set

--target <path>
    Project root for --scope project.
    Default: current working directory. Rejected with --scope global.

--force
    Overwrite existing managed files when their contents differ.
    Without --force, the installer stops rather than replacing them.

--dry-run
    Print every planned write without modifying anything.

--git-exclude <mode>
    Controls whether /.agents/tmp/ is added to .git/info/exclude (project scope only).
    Values: auto (default), yes, no

--help, -h
--version, -v
```

The installer only writes skill files. It never deletes anything; if it finds the `explore`/`develop`/`review` subagents installed by older releases under `.claude/agents/`, it reports them so you can remove them.

## Skills

| Skill | Invocation | Purpose |
| --- | --- | --- |
| `my-grill-to-spec` | `/my-grill-to-spec` | Grill a change, keep a resumable ledger, publish the SPEC with `to-spec`, review it |
| `my-spec-to-tickets` | `/my-spec-to-tickets` | Turn an approved SPEC into tickets with `to-tickets` |
| `my-implement-orchestrator` | `/my-implement-orchestrator` | Implement tickets with `tdd` + repeated `code-review` gates |
| `my-grill-to-implementation` | `/my-grill-to-implementation` | Light path: grill, explore, develop with `tdd`, review, commit |
| `my-review-changes` | `/my-review-changes` | Independent read-only review of changed files |
| `my-improve-code` | `/my-improve-code` | Improve comments and spacing without behavior changes |
| `my-improve-comments` | `/my-improve-comments` | Improve comments/documentation only |
| `my-improve-spacing` | `/my-improve-spacing` | Improve logical blank-line spacing only |
| `my-git-commit` | `/my-git-commit` | Commit everything except `./.agents/tmp/` |
| `my-software-design-doc` | automatic or `/my-software-design-doc` | Create or review software design documents |

Every workflow except `my-software-design-doc` is explicit-only (`disable-model-invocation: true`).

### Subagents

Skills that delegate work (exploration, development, review) **do not name a subagent type**. Claude Code picks the most suitable available subagent for each delegation; the skill only states the scope and constraints (read-only, no commits, skills to load, expected report). No custom agents are installed.

## Matt Pocock dependency

These workflows compose Matt Pocock's skills instead of duplicating them. Install them in Claude Code:

```bash
npx skills add mattpocock/skills
```

Run `setup-matt-pocock-skills` once per repository so `docs/agents/issue-tracker.md` identifies the canonical tracker. `to-spec` and `to-tickets` own their output locations. With Matt's local-markdown tracker, the SPEC is `.scratch/<feature>/spec.md` and tickets are `.scratch/<feature>/issues/<NN>-<slug>.md`; with GitHub/GitLab/Linear or another configured tracker, they are native tracker issues.

### Full path

```text
my-grill-to-spec
  -> grill-with-docs
  -> .agents/tmp/grill/<slug>.md        (resumable decision ledger)
  -> to-spec
  -> canonical SPEC in configured tracker
  -> fresh independent SPEC review
  -> STOP

my-spec-to-tickets
  -> to-tickets
  -> canonical tickets in configured tracker
  -> STOP

my-implement-orchestrator
  -> develop + tdd
  -> code-review
  -> (develop fix + tdd -> new code-review)*
  -> scoped commit + tracker finalization
```

`my-grill-to-spec` never delegates SPEC authorship to a subagent: `to-spec` owns synthesis and publishing. A fresh review subagent is used only after the canonical SPEC exists, and the workflow stops after approval.

Matt's `implement` and `implement-spec` are user-invoked upstream skills, so `my-implement-orchestrator` composes the model-invokable primitives they rely on: `tdd` for develop/fix passes and `code-review` for every acceptance gate. Every fix must be followed by a new code review before commit.

### Light path

```text
my-grill-to-implementation
  -> grill-with-docs
  -> .agents/tmp/implementation/<slug>.md
  -> exploration subagent
  -> development subagent + tdd
  -> fresh review subagent
  -> (development fix -> fresh review)*
  -> one scoped commit
```

## Runtime state and resume

All workflow state lives in the project under:

```text
./.agents/tmp/
├── grill/<slug>.md
└── implementation/<slug>.md
```

Both ledgers survive context exhaustion. Reinvoke the same workflow with the ledger path:

```text
/my-grill-to-spec ./.agents/tmp/grill/<slug>.md
/my-grill-to-implementation ./.agents/tmp/implementation/<slug>.md
```

Workflows never include `./.agents/tmp/` in commits or code reviews. For project installs, the installer adds `/.agents/tmp/` to `.git/info/exclude` when the target is a Git repository. For global installs, add that rule yourself in each project where you use the workflows.

## Source architecture

```text
source/skills/            canonical skill source
scripts/build.py          generates dist/skills/ (Claude Code profile)
scripts/validate.py       validates source and generated profile
scripts/test-installer.js installer tests
bin/software-skills.js    installer
dist/skills/              generated, installable Claude Code skills
```

```bash
python3 scripts/build.py
```

```bash
python3 scripts/validate.py
```

```bash
npm test
```

## License

MIT. See `LICENSE`.
