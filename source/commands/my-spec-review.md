---
description: Loop an independent review of a spec and its issues, fix every problem found, and stop only when a fresh review finds none.
---

# my-spec-review

Make a spec and its issues correct, complete and consistent. Never approve by self-review: every verification runs in a fresh read-only subagent that has not seen earlier findings or fixes.

Read repository instructions and `docs/agents/issue-tracker.md`; if the tracker file is missing, return `BLOCKED` and ask the user to run `/setup-matt-pocock-skills`. `$ARGUMENTS` names the spec (and optionally its issues); empty means the most recent spec and the issues that reference it. Before the first cycle, obtain a positive integer `MAX_REVIEW_CYCLES` and keep it fixed.

```text
verify(fresh, read-only) -> problems? -> fix -> new fresh verify -> ... -> clean
```

## Verify

Delegate to a fresh read-only subagent per cycle. Give it only the spec and issue pointers, never earlier findings. It checks, against the code and the domain docs:

- Spec: contradictions, ambiguity, missing decisions, acceptance criteria that cannot be tested, test seams that are absent or wrong, claims about the code that are false.
- Issues: each issue traces to the spec, no spec requirement lacks an issue, dependencies and order are correct, scope and acceptance criteria match the spec, no duplicates or overlap.
- Spec and issues together: terminology, names and decisions are identical in both.

It returns `PROBLEMS` (possibly empty) with location, evidence, impact and a proposed fix, ranked blocking first. Reject nitpicks that change no meaning.

## Fix

For each problem, decide yourself when the spec or domain docs already define the answer. When the answer is a new product or domain decision, ask the user, then continue. Pass the decided problems to one fix pass that edits the spec and issues through the tracker defined in `docs/agents/issue-tracker.md`, preserves unrelated content, and does not implement code. Never commit, push or create branches unless the tracker file prescribes it for specs.

## Loop

Repeat verify and fix. A fix always requires a new fresh verification: never stop after fixing. Stop only when a fresh verification returns no problems. If `MAX_REVIEW_CYCLES` is exhausted with problems left, return `CHANGES_REQUIRED` with the open problems instead of reporting success.

Report spec and issue references, cycles run, problems found and fixed per cycle, decisions the user made, final verdict (`CLEAN`, `CHANGES_REQUIRED` or `BLOCKED`), and blockers.
