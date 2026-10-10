# my-grill-to-implementation

Light path: `grill-with-docs` → resumable implementation ledger → exploration subagent → per slice: development subagent with `tdd` → green validation → commit → at the end: fresh review subagent → (fix → commit → new fresh review)* → completed.

It works only in the current checkout (no worktrees, branches, pull requests, or pushes) and runs subagents sequentially, in parallel only across different repositories.

The plan is written as `spec.md` (slices) in the spec folder from `docs/agents/issue-tracker.md` (run `/setup-matt-pocock-skills` first) and committed last.

Resume with the temporary ledger `./.agents/tmp/implementation/<slug>.md`.
