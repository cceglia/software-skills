#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source"
SKILLS = SRC / "skills"
COMMANDS = SRC / "commands"
DIST = ROOT / "dist"
VERSION = "4.0.0"
EXPECTED_SKILLS = {"my-software-design-doc"}
EXPECTED_COMMANDS = {
    "my-grill-to-implementation",
    "my-implement-orchestrator",
    "my-improve-code",
    "my-improve-comments",
    "my-improve-spacing",
}

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


def check_skill_dir(root: Path, expected: set[str]) -> None:
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


def check_command_dir(root: Path, expected: set[str], *, built: bool) -> None:
    got = {p.stem for p in root.glob("*.md")}
    if got != expected:
        fail(f"{root.relative_to(ROOT)} commands mismatch: expected {sorted(expected)}, got {sorted(got)}")
    for path in root.glob("*.md"):
        fm, body = frontmatter(path)
        if not fm.get("description"):
            fail(f"missing command description: {path.relative_to(ROOT)}")
        if len(path.read_text(encoding="utf-8").splitlines()) > 250:
            fail(f"command should remain concise (<250 lines): {path.relative_to(ROOT)}")
        if built:
            if "$ARGUMENTS" not in body:
                fail(f"generated command missing $ARGUMENTS: {path.relative_to(ROOT)}")
            if "User-invoked OpenCode V2 command" not in body:
                fail(f"generated command missing invocation block: {path.relative_to(ROOT)}")
            if "opencode/autoinvoke" in body or "\nslash:" in body:
                fail(f"generated command carries skill invocation metadata: {path.relative_to(ROOT)}")


FORBIDDEN = ("my-grill-to-spec", "my-spec-to-tickets", "my-review-changes", "my-update-skills-list", "skills.json", "./.tmp/", ".opencode/grill", ".opencode/implementation", "subagent_type", "my-grill-to-plan", "my-plan-to-spec")


def validate_source() -> None:
    check_skill_dir(SKILLS, EXPECTED_SKILLS)
    check_command_dir(COMMANDS, EXPECTED_COMMANDS, built=False)

    for name in EXPECTED_SKILLS:
        if read(SKILLS / name / "VERSION").strip() != VERSION:
            fail(f"source VERSION mismatch for {name}")
    for name in EXPECTED_COMMANDS:
        if (SKILLS / name).exists():
            fail(f"user-invoked workflow must not ship as a skill: source/skills/{name}")
    if (COMMANDS / "my-software-design-doc.md").exists():
        fail("my-software-design-doc must remain a skill, not a command")

    files = list(SKILLS.glob("*/SKILL.md")) + list(COMMANDS.glob("*.md"))
    text = "\n".join(p.read_text(encoding="utf-8") for p in files)
    for forbidden in FORBIDDEN:
        if forbidden in text:
            fail(f"obsolete token remains in canonical source: {forbidden}")
    if "./.agents/tmp/implementation/" not in text:
        fail("canonical source missing runtime path ./.agents/tmp/implementation/")

    light = read(COMMANDS / "my-grill-to-implementation.md")
    for token in ("grill-with-docs", "`tdd`", "exploration", "development", "fresh** read-only review", "./.agents/tmp/implementation/", "Next action", "develop(tdd) -> validation green -> commit", "new fresh review", "never create worktrees", "pull requests", "starting revision", "Run subagents sequentially", "different repositories"):
        if token not in light:
            fail(f"my-grill-to-implementation missing light-flow invariant: {token}")
    orchestrator = read(COMMANDS / "my-implement-orchestrator.md")
    for token in ("`tdd`", "`code-review`", "develop(tdd) -> validation green -> commit", "Do not review tickets individually by default", "new `code-review`", "MAX_REVIEW_CYCLES", "never create worktrees", "pull requests", "starting revision", "Run subagents sequentially", "different repositories"):
        if token not in orchestrator:
            fail(f"my-implement-orchestrator missing flow invariant: {token}")


def validate_opencode() -> None:
    if {p.name for p in DIST.iterdir()} != {".opencode"}:
        fail(f"dist must contain only the OpenCode V2 profile, got {sorted(p.name for p in DIST.iterdir())}")
    root = DIST / ".opencode"
    check_skill_dir(root / "skills", EXPECTED_SKILLS)
    check_command_dir(root / "commands", EXPECTED_COMMANDS, built=True)
    for name, roles in {
        "my-grill-to-implementation": "`explore`, `develop`, `review`",
        "my-implement-orchestrator": "`develop`",
    }.items():
        _, body = frontmatter(root / "commands" / f"{name}.md")
        if f"Use OpenCode V2 child-session roles: {roles}." not in body:
            fail(f"OpenCode {name} command missing harness roles mapping")
    for agent in ("develop", "review"):
        fm, _ = frontmatter(root / "agents" / f"{agent}.md")
        if fm.get("mode") != "subagent":
            fail(f"OpenCode {agent} missing mode: subagent")


def validate_agents_md() -> None:
    text = read(ROOT / "AGENTS.md")
    for token in (
        "source/commands/",
        "source/skills/",
        "./.agents/tmp/",
        "my-grill-to-implementation",
        "my-implement-orchestrator",
        "Do not review tickets individually by default",
        "develop(tdd) -> validation green -> commit",
        "OpenCode V2",
        "native discovery",
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
    validate_opencode()
    validate_agents_md()
    validate_global()
    if errors:
        print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("OK: canonical source and OpenCode V2 profile validated")
    print(f"- canonical skills: {len(EXPECTED_SKILLS)}")
    print(f"- user-invoked commands: {len(EXPECTED_COMMANDS)}")
    print("- runtime state: resumable ledgers under ./.agents/tmp/implementation")
    print("- discovery: native OpenCode V2 commands and skills; no skills.json registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
