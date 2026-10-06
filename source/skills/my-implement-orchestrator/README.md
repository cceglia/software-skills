# my-implement-orchestrator

Implements approved tracker tickets with:

```text
per ticket:        develop(tdd) → validation green → commit
important ticket:  + code-review of that ticket → (fix → commit → new code-review)*
at the end:        code-review → (develop fix(tdd) → commit → new code-review)* → tracker finalization
```

Only important tickets (high-risk or foundational) are reviewed individually. It works only in the current checkout (no worktrees, branches, pull requests, or pushes) and runs subagents sequentially, in parallel only across different repositories. It uses Matt Pocock's model-invokable `tdd` and `code-review` primitives.
