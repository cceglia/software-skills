---
description: Loop an independent review of a spec and its issues, fix the problems in the chosen scope (blocking only, all, or blocking then all), and stop only when a fresh review finds none in scope.
---

# my-spec-review

Make a spec and its issues correct, complete and consistent. Never approve by self-review: every verification runs in a fresh read-only subagent that has not seen earlier findings or fixes.

Read repository instructions and `docs/agents/issue-tracker.md`; if the tracker file is missing, return `BLOCKED` and ask the user to run `/setup-matt-pocock-skills`. `$ARGUMENTS` names the spec (and optionally its issues); empty means the most recent spec and the issues that reference it. Before the first cycle, obtain a positive integer `MAX_REVIEW_CYCLES` and ask the user for `FIX_SCOPE`; keep both fixed:

- `BLOCKING_ONLY`: fix only `BLOCKING` problems; `NON_BLOCKING` problems stay as notes.
- `ALL`: fix `BLOCKING` and `NON_BLOCKING` problems in every cycle.
- `BLOCKING_THEN_ALL`: run the `BLOCKING_ONLY` loop until clean, then fix the accumulated notes and continue as `ALL`.

```text
BLOCKING_ONLY:     verify -> blocking? -> fix blocking -> new fresh verify -> ... -> no blocking
ALL:               verify -> any problem? -> fix all -> new fresh verify -> ... -> no problems
BLOCKING_THEN_ALL: BLOCKING_ONLY loop -> fix notes -> ALL loop
```

## Verify

Delegate to a fresh read-only subagent per cycle. It never sees earlier findings or fixes. While notes are kept (`BLOCKING_ONLY`, and the first phase of `BLOCKING_THEN_ALL`), also give it the accumulated non-blocking notes (location and title only); it must not re-verify, re-report or re-rank them. It checks, against the code and the domain docs:

- Spec: contradictions, ambiguity, missing decisions, acceptance criteria that cannot be tested, test seams that are absent or wrong, claims about the code that are false.
- Issues: each issue traces to the spec, no spec requirement lacks an issue, dependencies and order are correct, scope and acceptance criteria match the spec, no duplicates or overlap.
- Spec and issues together: terminology, names and decisions are identical in both.

It returns `PROBLEMS` (possibly empty) with location, evidence, impact, a proposed fix and a class: `BLOCKING` (wrong, contradictory, untestable, missing or misleading enough to break implementation) or `NON_BLOCKING`. Reject nitpicks that change no meaning. While notes are kept, add each new `NON_BLOCKING` problem to the notes; a note is not verified again.

## Fix

The problems to fix are those in `FIX_SCOPE` for the current phase. For each, decide yourself when the spec or domain docs already define the answer. When the answer is a new product or domain decision, ask the user, then continue. Pass only the decided problems to one fix pass that edits the spec and issues through the tracker defined in `docs/agents/issue-tracker.md`, preserves unrelated content, and does not implement code. Never commit, push or create branches unless the tracker file prescribes it for specs.

## Loop

Repeat verify and fix. A fix always requires a new fresh verification: never stop after fixing. A loop is clean when a fresh verification returns no problems in scope: no `BLOCKING` problems for `BLOCKING_ONLY`, no problems at all for `ALL`. For `BLOCKING_THEN_ALL`, when the first loop is clean, fix the notes, drop them, and start the `ALL` loop with a new fresh verification. `MAX_REVIEW_CYCLES` bounds each loop; if it is exhausted with problems in scope left, return `CHANGES_REQUIRED` with them instead of reporting success.

Report spec and issue references, `FIX_SCOPE`, cycles run, problems found and fixed per cycle (by class), decisions the user made, final verdict (`CLEAN`, `CHANGES_REQUIRED` or `BLOCKED`), the non-blocking notes left unfixed, and blockers.
