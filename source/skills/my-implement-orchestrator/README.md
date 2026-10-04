# my-implement-orchestrator

Implements approved tracker tickets one at a time with:

```text
develop(tdd) → code-review → (develop fix(tdd) → code-review)* → scoped commit → tracker finalization
```

It uses Matt Pocock's model-invokable `tdd` and `code-review` primitives. It does not call `implement` or `implement-spec`, which upstream marks user-invoked only.
