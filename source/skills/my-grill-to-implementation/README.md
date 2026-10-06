# my-grill-to-implementation

Light path: `grill-with-docs` → resumable implementation ledger → exploration subagent → per slice: development subagent with `tdd` → green validation → commit → at the end: fresh review subagent → (fix → commit → new fresh review)* → completed.

It works only in the current checkout (no worktrees, branches, pull requests, or pushes) and runs subagents sequentially, in parallel only across different repositories.

Resume with `./.agents/tmp/implementation/<slug>.md`.
