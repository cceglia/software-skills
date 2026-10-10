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

The installer only writes skill files. It never deletes anything; if it finds skills removed in 4.0.0 or the `explore`/`develop`/`review` subagents installed by older releases, it lists them so you can remove them.

## Skills

| Skill | Invocation | Purpose |
| --- | --- | --- |
| `my-grill-to-implementation` | `/my-grill-to-implementation` | Light path: grill, explore, implement and commit every slice with `tdd`, then a final review with fix/review cycles |
| `my-implement-orchestrator` | `/my-implement-orchestrator` | Implement tracker tickets with `tdd` and per-ticket commits; review a ticket individually only in exceptional high-risk cases, then a final `code-review` with fix/review cycles |
| `my-improve-code` | `/my-improve-code` | Improve comments and spacing without behavior changes |
| `my-improve-comments` | `/my-improve-comments` | Improve comments/documentation only |
| `my-improve-spacing` | `/my-improve-spacing` | Improve logical blank-line spacing only |
| `my-software-design-doc` | automatic or `/my-software-design-doc` | Create or review software design documents |

Every workflow except `my-software-design-doc` is explicit-only (`disable-model-invocation: true`).

### Subagents

Skills that delegate work (exploration, development, review) **do not name a subagent type**. Claude Code picks the most suitable available subagent for each delegation; the skill only states the scope and constraints (read-only, no commits, skills to load, expected report). No custom agents are installed.

## Matt Pocock dependency

These workflows compose Matt Pocock's skills instead of duplicating them. Install them in Claude Code:

```bash
npx skills add mattpocock/skills
```

Run `setup-matt-pocock-skills` once per repository so Matt's skills know the configured issue tracker.

### Removed workflows

`my-grill-to-spec`, `my-spec-to-tickets`, `my-review-changes`, and `my-git-commit` were removed in 4.0.0: use Matt Pocock's skills directly (`grill-with-docs`, `to-spec`, `to-tickets`, `code-review`). `my-implement-orchestrator` was restored in 4.2.0. The installer never deletes files, but it lists removed skills still present in the destination so you can delete them.

### Ticket path

```text
my-implement-orchestrator
  per ticket:
    -> development subagent + tdd
    -> tests/typecheck green
    -> one commit (ticket reference in the message)
    -> exceptional ticket only: code-review of that ticket -> (fix -> commit -> new code-review)*
  at the end:
    -> code-review since the starting revision
    -> (development fix + tdd -> commit -> new code-review)*
    -> tracker finalization
```

A ticket is reviewed individually only for a high and concrete risk (data migration, data-loss risk, new security boundary), which the agent announces beforehand; a public contract or dependent tickets are not enough. every other ticket is covered by the final review. Same working-copy rules as the light path.

### Light path

```text
my-grill-to-implementation
  -> grill-with-docs
  -> spec.md in the tracker's spec folder (committed last) + .agents/tmp/implementation/<slug>.md ledger
  -> exploration subagent
  per slice:
    -> development subagent + tdd
    -> tests/typecheck green
    -> one commit
  at the end:
    -> fresh review subagent (diff since the starting revision)
    -> (development fix + tdd -> commit -> new fresh review)*
    -> completed
```

It works only in the current checkout (no worktrees, branches, pull requests, or pushes) and runs subagents sequentially, in parallel only across different repositories. An intermediate slice review happens only under the same exceptional high-risk criteria, announced beforehand.

## Runtime state and resume

All workflow state lives in the project under:

```text
./.agents/tmp/
└── implementation/<slug>.md
```

The ledger survives context exhaustion. Reinvoke the workflow with the ledger path:

```text
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
