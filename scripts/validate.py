#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source" / "skills"
SHARED = ROOT / "source" / "shared"
DIST = ROOT / "dist"
VERSION = "4.8.0"
EXPECTED = {
    "asd-ste100",
    "my-grill-to-implementation",
    "my-implement-orchestrator",
    "my-improve-code",
    "my-improve-comments",
    "my-improve-spacing",
    "my-golang-codebase-design",
    "my-software-design-doc",
}
MANUAL = EXPECTED - {"my-software-design-doc"}

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def frontmatter(path: Path) -> tuple[dict, str]:
    text = read(path)
    if not text.startswith("---\n"):
        fail(f"missing frontmatter: {path.relative_to(ROOT)}")
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"unterminated frontmatter: {path.relative_to(ROOT)}")
        return {}, text
    raw, body = text[4:end], text[end + 5 :]
    if yaml is not None:
        try:
            value = yaml.safe_load(raw) or {}
            if not isinstance(value, dict):
                raise TypeError("frontmatter is not a mapping")
            return value, body
        except Exception as exc:
            fail(f"invalid YAML in {path.relative_to(ROOT)}: {exc}")
            return {}, body
    parsed: dict[str, object] = {}
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z0-9_./-]+):\s*(.*)$", line)
        if m:
            raw_value = m.group(2).strip().strip('"')
            parsed[m.group(1)] = {"true": True, "false": False}.get(raw_value, raw_value)
    return parsed, body


def nested(mapping: dict, *keys):
    cur: object = mapping
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def check_skill_dir(root: Path, expected: set[str] = EXPECTED) -> None:
    got = {p.parent.name for p in root.glob("*/SKILL.md")}
    if got != expected:
        fail(f"{root.relative_to(ROOT)} skills mismatch: expected {sorted(expected)}, got {sorted(got)}")
    for path in root.glob("*/SKILL.md"):
        fm, _ = frontmatter(path)
        if fm.get("name") != path.parent.name:
            fail(f"name/directory mismatch: {path.relative_to(ROOT)}")
        if nested(fm, "metadata", "version") not in (VERSION, None):
            fail(f"wrong version in {path.relative_to(ROOT)}")
        if len(path.read_text(encoding="utf-8").splitlines()) > 250:
            fail(f"skill should remain concise (<250 lines): {path.relative_to(ROOT)}")


REMOVED = ("my-git-commit", "my-grill-to-spec", "my-review-changes", "my-spec-to-tickets")
FORBIDDEN = REMOVED + ("my-update-skills-list", "skills.json", "./.tmp/", ".opencode", ".codex", "subagent_type", "my-grill-to-plan", "my-plan-to-spec", ".claude/agents", "harness-mapped", "harness-native")
DELEGATING = EXPECTED - {"asd-ste100"}


def validate_source() -> None:
    check_skill_dir(SRC)
    style = read(SHARED / "response-style.md")
    for token in (
        "## Response style (ASD-STE100)",
        "**Level:** 80",
        "**Scope:** replies only",
        "`docs`",
        "the subagent prompt",
        "Never remove required report fields",
    ):
        if token not in style:
            fail(f"shared response style missing invariant: {token}")
    for name in EXPECTED:
        if read(SRC / name / "VERSION").strip() != VERSION:
            fail(f"source VERSION mismatch for {name}")
    text = "\n".join(p.read_text(encoding="utf-8") for p in SRC.glob("*/SKILL.md"))
    text += "\n" + style
    for forbidden in FORBIDDEN + ("`explore` role", "`develop` role", "`review` role"):
        if forbidden in text:
            fail(f"obsolete token remains in canonical source: {forbidden}")
    if "./.agents/tmp/implementation/" not in text:
        fail("canonical source missing runtime path ./.agents/tmp/implementation/")
    light = read(SRC / "my-grill-to-implementation" / "SKILL.md")
    for token in ("grill-with-docs", "`tdd`", "`codebase-design`", "exploration", "development", "fresh** read-only review", "./.agents/tmp/implementation/", "Next action", "develop(tdd+codebase-design) -> validation green -> commit", "new fresh review", "never create worktrees", "pull requests", "starting revision", "Run subagents sequentially", "different repositories"):
        if token not in light:
            fail(f"my-grill-to-implementation missing light-flow invariant: {token}")
    orchestrator = read(SRC / "my-implement-orchestrator" / "SKILL.md")
    for token in ("`tdd`", "`codebase-design`", "`code-review`", "develop(tdd+codebase-design) -> validation green -> commit", "Do not review tickets individually by default", "new `code-review`", "MAX_REVIEW_CYCLES", "never create worktrees", "pull requests", "starting revision", "Run subagents sequentially", "different repositories"):
        if token not in orchestrator:
            fail(f"my-implement-orchestrator missing flow invariant: {token}")
    style_skill = read(SRC / "asd-ste100" / "SKILL.md")
    for token in ("the environment's question tool", "**No arguments:**", "`help`", "`off`", "`status`", "`replies`", "`docs`", "subagent prompt", "1-100"):
        if token not in style_skill:
            fail(f"asd-ste100 skill missing invariant: {token}")
    golang = read(SRC / "my-golang-codebase-design" / "SKILL.md")
    for token in (
        "`codebase-design`",
        "facade",
        "`internal/<domain>`",
        "`errors.Is`/`errors.As`",
        "`cmd/*`",
        "allowlist",
        "`Package layout`",
        "`CODING_STANDARDS.md`",
        "`go build ./...`",
        "`go vet ./...`",
        "./.agents/tmp/implementation/",
        "one package at a time",
        "Do not create an interface where only one implementation exists",
    ):
        if token not in golang:
            fail(f"my-golang-codebase-design missing invariant: {token}")


def validate_claude() -> None:
    if {p.name for p in DIST.iterdir()} != {"skills"}:
        fail(f"dist must contain only the Claude Code skills profile, got {sorted(p.name for p in DIST.iterdir())}")
    root = DIST / "skills"
    check_skill_dir(root)
    for name in EXPECTED:
        fm, body = frontmatter(root / name / "SKILL.md")
        if {"agent", "context"} & set(fm):
            fail(f"Claude {name} must not pin a subagent via agent/context frontmatter")
        if name in DELEGATING and "Never prescribe a subagent type" not in body:
            fail(f"Claude {name} missing autonomous subagent selection block")
        if name in MANUAL:
            if fm.get("disable-model-invocation") is not True or fm.get("user-invocable") is not True:
                fail(f"Claude {name} missing explicit-only invocation fields")
            if f"/{name}" not in body:
                fail(f"Claude {name} missing slash invocation text")
        elif fm.get("disable-model-invocation"):
            fail(f"Claude {name} must remain model-invocable")
        for token in ("## Response style (ASD-STE100)", "the subagent prompt", "Never remove required report fields"):
            if token not in body:
                fail(f"Claude {name} missing response style invariant: {token}")

    _, style_body = frontmatter(root / "asd-ste100" / "SKILL.md")
    for token in ("the `AskUserQuestion` tool", "**No arguments:**", "`help`", "`off`", "`status`", "`replies`", "`docs`"):
        if token not in style_body:
            fail(f"Claude asd-ste100 missing invariant: {token}")
    if "the environment's question tool" in style_body:
        fail("Claude asd-ste100 kept the canonical tool placeholder")


def validate_agents_md() -> None:
    text = read(ROOT / "AGENTS.md")
    for token in (
        "source/skills/",
        "source/shared/",
        "./.agents/tmp/",
        "my-grill-to-implementation",
        "my-implement-orchestrator",
        "Do not review tickets individually by default",
        "develop(tdd+codebase-design) -> validation green -> commit",
        "Removed in 4.0.0",
        "my-update-skills-list",
        "my-plan-to-spec",
        "native skill discovery",
        "subagent type",
        "scripts/build.py",
        "scripts/validate.py",
    ):
        if token not in text:
            fail(f"AGENTS.md missing maintenance invariant: {token}")


def validate_global() -> None:
    files = [p for p in DIST.rglob("*") if p.is_file() and p.suffix in {".md", ".yaml", ".toml"}]
    text = "\n".join(p.read_text(encoding="utf-8") for p in files)
    for forbidden in FORBIDDEN:
        if forbidden in text:
            fail(f"obsolete token remains in generated profile: {forbidden}")
    if "./.agents/tmp/" not in text:
        fail("generated profile missing ./.agents/tmp runtime invariant")


def main() -> int:
    validate_source()
    validate_claude()
    validate_agents_md()
    validate_global()
    if errors:
        print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("OK: canonical source and Claude Code profile validated")
    print(f"- canonical skills: {len(EXPECTED)}")
    print(f"- explicit workflows: {len(MANUAL)}")
    print("- response style: shared ASD-STE100 block, default level 80")
    print("- runtime state: resumable ledgers under ./.agents/tmp/implementation")
    print("- skill routing: Claude Code native skill discovery; no skills.json registry")
    print("- subagents: no prescribed subagent types; Claude Code chooses autonomously")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
