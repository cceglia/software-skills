#!/usr/bin/env python3
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source" / "skills"
DIST = ROOT / "dist"
VERSION = "2.2.0"

MANUAL = {
    "my-git-commit",
    "my-grill-to-implementation",
    "my-grill-to-plan",
    "my-implement-orchestrator",
    "my-improve-code",
    "my-improve-comments",
    "my-improve-spacing",
    "my-plan-to-spec",
    "my-review-changes",
    "my-spec-to-tickets",
}

DISPLAY = {
    "my-software-design-doc": ("Software Design Doc", "Create or review software design documents", "Use $my-software-design-doc to create or review a software design document."),
    "my-git-commit": ("Git Commit All Changes", "Commit project changes except .agents/tmp", "Use $my-git-commit to commit all project changes except .agents/tmp, without amending."),
    "my-grill-to-implementation": ("Grill to Implementation", "Grill, implement, review, and commit", "Use $my-grill-to-implementation to grill this change, implement it after approval, independently review it, and commit it."),
    "my-grill-to-plan": ("Grill to Plan", "Interview decisions and produce a plan", "Use $my-grill-to-plan to grill this request and produce a complete implementation plan."),
    "my-implement-orchestrator": ("Implementation Orchestrator", "Implement approved tickets with review cycles", "Use $my-implement-orchestrator to implement approved work items with native skill discovery and independent review."),
    "my-improve-code": ("Improve Code", "Improve comments and spacing without behavior changes", "Use $my-improve-code to improve comments and logical spacing without changing behavior."),
    "my-improve-comments": ("Improve Comments", "Improve code comments and documentation safely", "Use $my-improve-comments to improve comments and documentation without changing behavior."),
    "my-improve-spacing": ("Improve Spacing", "Improve logical blank-line spacing safely", "Use $my-improve-spacing to improve logical spacing without changing behavior."),
    "my-plan-to-spec": ("Plan to SPEC", "Turn a grilled plan into a reviewed SPEC", "Use $my-plan-to-spec to turn completed grilling state into a reviewed implementation-ready SPEC."),
    "my-review-changes": ("Review Changes", "Independently review modified files", "Use $my-review-changes to independently review requested files or current working-tree changes."),
    "my-spec-to-tickets": ("SPEC to Tickets", "Decompose an approved SPEC into reviewed tickets", "Use $my-spec-to-tickets to decompose an approved SPEC into concise reviewed implementation tickets."),
}

ARG_HINT = {
    "my-git-commit": "[optional context]",
    "my-grill-to-implementation": "[change request | .agents/tmp/implementation state]",
    "my-grill-to-plan": "[change request]",
    "my-implement-orchestrator": "[work item source]",
    "my-improve-code": "[scope]",
    "my-improve-comments": "[scope]",
    "my-improve-spacing": "[scope]",
    "my-plan-to-spec": "[.agents/tmp/grill/<plan>.md]",
    "my-review-changes": "[files | directory | glob]",
    "my-spec-to-tickets": "[approved SPEC]",
}


def parse_skill(path: Path):
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---\n", 4)
    if not text.startswith("---\n") or end < 0:
        raise ValueError(f"Invalid skill frontmatter: {path}")
    fm = text[4:end]
    body = text[end + 5 :]
    name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
    desc = re.search(r"^description:\s*(.+)$", fm, re.M).group(1).strip()
    return name, desc, body, path.parent


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def copy_assets(src_dir: Path, dst_dir: Path):
    if (src_dir / "references").exists():
        shutil.copytree(src_dir / "references", dst_dir / "references", dirs_exist_ok=True)
    (dst_dir / "VERSION").write_text(VERSION + "\n", encoding="utf-8")


def insert_after_h1(body: str, block: str) -> str:
    m = re.search(r"^# .+$", body, re.M)
    if not m:
        return block.rstrip() + "\n\n" + body
    pos = m.end()
    return body[:pos] + "\n\n" + block.rstrip() + body[pos:]


def invocation_block(name: str, harness: str) -> str:
    line = {
        "opencode": f"Explicit-only OpenCode V2 workflow. Run `/{name}`; never invoke it implicitly.",
        "codex": f"Explicit-only Codex workflow. Invoke `${name}`; never invoke it implicitly.",
        "claude": f"Explicit-only Claude Code workflow. Run `/{name}`; never invoke it implicitly.",
        "antigravity": f"Explicit-only Antigravity workflow. Run `/{name}`; never trigger it through semantic skill matching.",
        "shared": "Explicit-only workflow. Run it only when the user explicitly requests it by name; never invoke it implicitly.",
    }[harness]
    args = (
        "Treat `$ARGUMENTS` plus immediately relevant conversation context as the invocation input."
        if harness == "claude"
        else "Treat command/skill arguments plus immediately relevant conversation context as the invocation input."
    )
    return f"## Invocation\n\n{line}\n\n{args}"


def mapping_block(harness: str) -> str:
    return {
        "opencode": "## Harness roles\n\nUse OpenCode V2 child sessions: built-in `explore` plus bundled `develop` and `review`.",
        "codex": "## Harness roles\n\nUse project agents in `.codex/agents/`: `explore`, `develop`, and `review`.",
        "claude": "## Harness roles\n\nUse project agents in `.claude/agents/`: `explore`, `develop`, and `review`.",
        "antigravity": "## Harness roles\n\nUse `.agents/agents.md`: `@explore`, `@develop`, and `@review`.",
        "shared": "## Harness roles\n\nUse the active harness's installed `explore`, `develop`, and `review` support roles.",
    }[harness]


def adapt_body(name: str, body: str, harness: str) -> str:
    if name in MANUAL:
        block = invocation_block(name, harness)
        if name != "my-git-commit":
            block += "\n\n" + mapping_block(harness)
        body = insert_after_h1(body, block)

    if name == "my-software-design-doc":
        replacements = {
            "opencode": "Use the built-in OpenCode V2 `explore` subagent for broad codebase discovery.",
            "codex": "Use the project Codex `explore` agent for broad codebase discovery.",
            "claude": "Use the project Claude Code `explore` subagent for broad codebase discovery.",
            "antigravity": "Use the `@explore` role from `.agents/agents.md` for broad codebase discovery.",
            "shared": "Use the active harness's installed read-only `explore` role for broad codebase discovery.",
        }
        body = body.replace("Use the harness-mapped read-only `explore` role for broad codebase discovery.", replacements[harness])

    if name == "my-review-changes" and harness == "claude":
        body = body.replace(
            mapping_block("claude"),
            "## Harness role\n\nClaude Code frontmatter already runs this workflow in the bundled `review` subagent; do not delegate again.",
            1,
        )
        body = body.replace(
            "Otherwise use one fresh independent read-only `review` role. Pass the resolved files, complete diff, repository instructions/standards, and available validation results.",
            "This skill already runs in a fresh bundled `review` subagent via its Claude Code frontmatter. Review the resolved files, complete diff, repository instructions/standards, and available validation results directly; do not delegate again.",
        )
    return body


def load_skills():
    result = {}
    for p in sorted(SRC.glob("*/SKILL.md")):
        n, d, b, sd = parse_skill(p)
        result[n] = (d, b, sd)
    return result


def build_opencode(skills):
    root = DIST / "opencode" / ".opencode"
    sroot, aroot = root / "skills", root / "agents"
    sroot.mkdir(parents=True, exist_ok=True)
    aroot.mkdir(parents=True, exist_ok=True)

    for name, (desc, body, srcd) in skills.items():
        d = sroot / name
        d.mkdir(parents=True, exist_ok=True)
        fm = ["---", f"name: {name}", f"description: {desc}", "license: MIT"]
        if name in MANUAL:
            fm += ["compatibility: OpenCode V2; explicit slash invocation only.", "slash: true", "metadata:", f'  version: "{VERSION}"', "  opencode/autoinvoke: false", "  opencode/slash: true"]
        else:
            fm += ["compatibility: OpenCode V2 with native subagents.", "metadata:", f'  version: "{VERSION}"']
        fm += ["---", ""]
        (d / "SKILL.md").write_text("\n".join(fm) + adapt_body(name, body, "opencode"), encoding="utf-8")
        copy_assets(srcd, d)

    (aroot / "develop.md").write_text('''---
description: Scoped implementation and authoring worker for software-skills workflows.
mode: subagent
permissions:
  - action: subagent
    resource: "*"
    effect: deny
  - action: shell
    resource: "git commit*"
    effect: deny
  - action: shell
    resource: "git push*"
    effect: deny
  - action: shell
    resource: "git reset*"
    effect: deny
  - action: shell
    resource: "git clean*"
    effect: deny
  - action: shell
    resource: "git stash*"
    effect: deny
---

Follow the delegated scope exactly. Read repository instructions, load every skill requested by the parent, preserve unrelated changes, validate the work, never commit/push, and report loaded/missing skills, changed files, validation, and blockers.
''', encoding="utf-8")
    (aroot / "review.md").write_text('''---
description: Independent read-only reviewer for software-skills workflows.
mode: subagent
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: subagent
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: ask
  - action: shell
    resource: "git status*"
    effect: allow
  - action: shell
    resource: "git diff*"
    effect: allow
  - action: shell
    resource: "git log*"
    effect: allow
---

Review independently. Read repository instructions and every skill requested by the parent, inspect supplied evidence/diffs first, never edit or mutate repository state, never delegate, and report loaded/missing skills plus the exact verdict schema requested.
''', encoding="utf-8")


def write_openai_sidecar(d: Path, name: str):
    display, short, default = DISPLAY[name]
    allow = "false" if name in MANUAL else "true"
    ad = d / "agents"
    ad.mkdir(exist_ok=True)
    (ad / "openai.yaml").write_text(
        "interface:\n"
        f"  display_name: {q(display)}\n"
        f"  short_description: {q(short)}\n"
        f"  default_prompt: {q(default)}\n"
        "policy:\n  products:\n    - CODEX\n"
        f"  allow_implicit_invocation: {allow}\n",
        encoding="utf-8",
    )


def build_codex(skills):
    sroot = DIST / "codex" / ".agents" / "skills"
    aroot = DIST / "codex" / ".codex" / "agents"
    sroot.mkdir(parents=True, exist_ok=True)
    aroot.mkdir(parents=True, exist_ok=True)

    for name, (desc, body, srcd) in skills.items():
        d = sroot / name
        d.mkdir(parents=True, exist_ok=True)
        fm = f'''---\nname: {name}\ndescription: {desc}\nlicense: MIT\ncompatibility: Codex with native Agent Skills sidecars and project agents.\nmetadata:\n  version: "{VERSION}"\n---\n'''
        (d / "SKILL.md").write_text(fm + adapt_body(name, body, "codex"), encoding="utf-8")
        copy_assets(srcd, d)
        write_openai_sidecar(d, name)

    agents = {
        "explore": ("read-only", "Explore only the delegated repository scope. Read AGENTS.md first, return concise evidence, never edit or mutate repository state, and do not spawn agents unless explicitly requested."),
        "develop": ("workspace-write", "Implement only the delegated scope. Read AGENTS.md, load every skill requested by the parent, preserve unrelated changes, validate the work, never commit/push/reset/clean/stash, and report loaded/missing skills, changed files, validation, and blockers."),
        "review": ("read-only", "Review independently from implementation. Read AGENTS.md and every requested review skill, inspect supplied diffs/evidence first, never edit or mutate state, never spawn agents, and return the exact requested verdict schema including loaded/missing skills."),
    }
    for name, (sandbox, instructions) in agents.items():
        (aroot / f"{name}.toml").write_text(
            f'name = "{name}"\ndescription = "{name.capitalize()} worker for software-skills workflows."\nsandbox_mode = "{sandbox}"\ndeveloper_instructions = """\n{instructions}\n"""\n',
            encoding="utf-8",
        )


def build_claude(skills):
    sroot = DIST / "claude-code" / ".claude" / "skills"
    aroot = DIST / "claude-code" / ".claude" / "agents"
    sroot.mkdir(parents=True, exist_ok=True)
    aroot.mkdir(parents=True, exist_ok=True)

    for name, (desc, body, srcd) in skills.items():
        d = sroot / name
        d.mkdir(parents=True, exist_ok=True)
        lines = ["---", f"name: {name}", f"description: {desc}", "license: MIT", "compatibility: Claude Code with native skill controls and project subagents."]
        if name in MANUAL:
            lines += ["disable-model-invocation: true", "user-invocable: true"]
            if ARG_HINT.get(name):
                lines.append(f"argument-hint: {q(ARG_HINT[name])}")
        if name == "my-review-changes":
            lines += ["context: fork", "agent: review", "background: false"]
        lines += ["metadata:", f'  version: "{VERSION}"', "---", ""]
        (d / "SKILL.md").write_text("\n".join(lines) + adapt_body(name, body, "claude"), encoding="utf-8")
        copy_assets(srcd, d)

    (aroot / "explore.md").write_text('''---
name: explore
description: Read-only repository explorer for software-skills workflows.
tools: Read, Grep, Glob, Bash, Skill
model: inherit
permissionMode: plan
---

Inspect only the delegated scope. Read repository instructions first, return concise evidence, never edit or mutate repository/external state, and do not delegate unless explicitly requested.
''', encoding="utf-8")
    (aroot / "develop.md").write_text('''---
name: develop
description: Scoped implementation and authoring worker for software-skills workflows.
model: inherit
permissionMode: default
---

Follow the delegated scope. Read repository instructions, load every skill requested by the parent, preserve unrelated changes, validate the work, never commit/push/reset/clean/stash, and report loaded/missing skills, changed files, validation, and blockers.
''', encoding="utf-8")
    (aroot / "review.md").write_text('''---
name: review
description: Independent read-only reviewer for software-skills workflows.
tools: Read, Grep, Glob, Bash, Skill
model: inherit
permissionMode: plan
---

Review independently. Read repository instructions and every requested review skill, inspect supplied diffs/evidence first, never edit or mutate state, never delegate, and return the exact requested verdict schema including loaded/missing skills.
''', encoding="utf-8")


def build_antigravity(skills):
    root = DIST / "antigravity" / ".agents"
    sroot, wroot, rroot = root / "skills", root / "workflows", root / "rules"
    sroot.mkdir(parents=True, exist_ok=True)
    wroot.mkdir(parents=True, exist_ok=True)
    rroot.mkdir(parents=True, exist_ok=True)

    name = "my-software-design-doc"
    desc, body, srcd = skills[name]
    d = sroot / name
    d.mkdir(parents=True, exist_ok=True)
    fm = f'''---\nname: {name}\ndescription: {desc}\nlicense: MIT\ncompatibility: Google Antigravity / Antigravity IDE; semantic on-demand skill.\nmetadata:\n  version: "{VERSION}"\n---\n'''
    (d / "SKILL.md").write_text(fm + adapt_body(name, body, "antigravity"), encoding="utf-8")
    copy_assets(srcd, d)

    for name in sorted(MANUAL):
        desc, body, _ = skills[name]
        (wroot / f"{name}.md").write_text(f"---\ndescription: {desc}\n---\n\n" + adapt_body(name, body, "antigravity"), encoding="utf-8")

    (root / "agents.md").write_text('''# Software Skills Agent Team

Use these roles only when a workflow requests them; keep at most one active worker unless the workflow says otherwise.

## @explore
Read-only repository discovery. Return concise evidence; never edit or mutate state.

## @develop
Scoped implementation/authoring. Load every requested skill, preserve unrelated changes, validate, never commit/push, and report loaded/missing skills, changes, validation, and blockers.

## @review
Fresh independent read-only review. Load every requested review skill, never edit or mutate state, and return the exact verdict schema including loaded/missing skills.
''', encoding="utf-8")
    (rroot / "software-skills-runtime.md").write_text('''# Software Skills Runtime Rules

- `./.agents/tmp/` is ephemeral runtime state; never stage, commit, or review it.
- Grill state: `./.agents/tmp/grill/`.
- Direct implementation state: `./.agents/tmp/implementation/`.
- Explicit workflows live in `.agents/workflows/`; `my-software-design-doc` remains a semantic skill.
- Use `.agents/agents.md` when a workflow requests `@explore`, `@develop`, or `@review`.
''', encoding="utf-8")


def build_shared(skills):
    sroot = DIST / "shared" / ".agents" / "skills"
    sroot.mkdir(parents=True, exist_ok=True)
    for name, (desc, body, srcd) in skills.items():
        d = sroot / name
        d.mkdir(parents=True, exist_ok=True)
        shared_desc = f"Explicit-only workflow. {desc}" if name in MANUAL else desc
        lines = [
            "---",
            f"name: {name}",
            f"description: {shared_desc}",
            "license: MIT",
            "compatibility: Shared Agent Skills profile for Codex, Claude Code, OpenCode V2, and Antigravity; native support files install separately.",
            "metadata:",
            f'  version: "{VERSION}"',
        ]
        if name in MANUAL:
            lines += ['  opencode/autoinvoke: "false"', '  opencode/slash: "true"']
        lines += ["---", ""]
        (d / "SKILL.md").write_text("\n".join(lines) + adapt_body(name, body, "shared"), encoding="utf-8")
        copy_assets(srcd, d)
        write_openai_sidecar(d, name)


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    skills = load_skills()
    missing = (MANUAL | {"my-software-design-doc"}) - set(skills)
    if missing:
        raise SystemExit(f"Missing canonical skills: {sorted(missing)}")
    build_opencode(skills)
    build_codex(skills)
    build_claude(skills)
    build_antigravity(skills)
    build_shared(skills)
    print(f"Built {len(skills)} canonical skills for 4 native harness profiles + shared .agents profile")


if __name__ == "__main__":
    main()
