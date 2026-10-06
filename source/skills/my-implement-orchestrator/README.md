# my-implement-orchestrator

Implements approved tracker tickets with:

```text
per ticket:        develop(tdd) → validation green → commit
exceptional ticket: + code-review of that ticket → (fix → commit → new code-review)*
at the end:        code-review → (develop fix(tdd) → commit → new code-review)* → tracker finalization
```

A ticket is reviewed individually only for a high and concrete risk (data migration, data-loss risk, new security boundary), announced to the user beforehand. It works only in the current checkout (no worktrees, branches, pull requests, or pushes) and runs subagents sequentially, in parallel only across different repositories. It uses Matt Pocock's model-invokable `tdd` and `code-review` primitives.
