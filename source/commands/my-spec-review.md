---
description: Loop an independent review of a spec and its issues, fix every problem found, and stop only when a fresh review finds none.
---

# my-spec-review

Make a spec and its issues correct, complete and consistent. Never approve by self-review: every verification runs in a fresh read-only subagent that has not seen earlier blocking findings or fixes.

Read repository instructions and `docs/agents/issue-tracker.md`; if the tracker file is missing, return `BLOCKED` and ask the user to run `/setup-matt-pocock-skills`. `$ARGUMENTS` names the spec (and optionally its issues); empty means the most recent spec and the issues that reference it. Before the first cycle, obtain a positive integer `MAX_REVIEW_CYCLES` and keep it fixed.

```text
verify(fresh, read-only) -> blocking problems? -> fix blocking only -> new fresh verify -> ... -> clean
```

## Verify

Delegate to a fresh read-only subagent per cycle. Give it the spec and issue pointers plus the accumulated non-blocking notes (location and title only). It must not re-verify, re-report or re-rank those notes. It never sees earlier blocking findings or fixes. It checks, against the code and the domain docs:

- Spec: contradictions, ambiguity, missing decisions, acceptance criteria that cannot be tested, test seams that are absent or wrong, claims about the code that are false.
- Issues: each issue traces to the spec, no spec requirement lacks an issue, dependencies and order are correct, scope and acceptance criteria match the spec, no duplicates or overlap.
- Spec and issues together: terminology, names and decisions are identical in both.

It returns `PROBLEMS` (possibly empty) with location, evidence, impact, a proposed fix and a class: `BLOCKING` (wrong, contradictory, untestable, missing or misleading enough to break implementation) or `NON_BLOCKING`. Reject nitpicks that change no meaning. Add each new `NON_BLOCKING` problem to the notes; notes are never fixed and never verified again.

## Fix

For each `BLOCKING` problem, decide yourself when the spec or domain docs already define the answer. When the answer is a new product or domain decision, ask the user, then continue. Pass only the decided `BLOCKING` problems to one fix pass that edits the spec and issues through the tracker defined in `docs/agents/issue-tracker.md`, preserves unrelated content, and does not implement code. Never commit, push or create branches unless the tracker file prescribes it for specs.

## Loop

Repeat verify and fix. A fix always requires a new fresh verification: never stop after fixing. Stop only when a fresh verification returns no `BLOCKING` problems. If `MAX_REVIEW_CYCLES` is exhausted with `BLOCKING` problems left, return `CHANGES_REQUIRED` with them instead of reporting success.

Report spec and issue references, cycles run, blocking problems found and fixed per cycle, decisions the user made, final verdict (`CLEAN`, `CHANGES_REQUIRED` or `BLOCKED`), the non-blocking notes left unfixed, and blockers.
