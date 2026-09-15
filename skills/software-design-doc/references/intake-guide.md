# Interactive Intake Guide

Use this guide only when information is missing. It is not a questionnaire that must always be completed in full.

## Initial intake

If not already known, establish:

1. What is being designed?
2. What outcome or problem motivates it?
3. Where is the relevant documentation?
4. If there is no documentation, is there an existing codebase?
5. If neither documentation nor implementation exists, what requirements or problem statement are already known?

A concise opening can be:

> Before I design this, I need to establish the source of truth. Where should I look for existing documentation (for example README, docs/, ADR/RFC, API specs, tickets, diagrams), or should I treat this as a greenfield project with no existing documentation? If there is an existing codebase, I will delegate its exploration to subagents and only ask you for information that cannot be recovered reliably from the project.

Do not ask this if the user already supplied the answer.

## Knowledge-gap questions

After documentation/code exploration, ask only questions whose answers materially affect the design.

Useful categories include:

### Behavior

- What must the system do in the important user/caller scenarios?
- Which existing behaviors must remain compatible?

### Data and correctness

- What data is authoritative?
- Is strong consistency required anywhere?
- Can operations be retried or duplicated safely?

### Scale and performance

- What workload shape matters: request rate, data volume, concurrency, batch size, growth?
- Are there latency or throughput targets that constrain architecture?

### Reliability

- What failure or downtime is acceptable?
- Are there recovery objectives or degraded modes that matter?

### Integrations and constraints

- Which external systems must be integrated?
- Are specific technologies, cloud services, runtimes, or deployment environments mandatory?

### Security / privacy / compliance

- What sensitive data or privilege boundaries exist?
- Are there regulatory, residency, retention, or audit requirements?

### Delivery

- Must the change be backward compatible?
- Is migration required?
- Is a phased rollout or zero-downtime rollout required?

## Blocking-question rule

Ask a question before finalizing the design when plausible answers would lead to materially different high-cost decisions.

Examples:

- SQL vs. event store depends on correctness/history requirements.
- synchronous vs. asynchronous integration depends on latency and failure semantics.
- migration design depends on downtime and compatibility constraints.
- tenancy isolation depends on security/compliance requirements.

If the answer only changes a low-cost implementation detail, do not block the design. Record an assumption or defer the detail.

## Greenfield rule

When there is no existing documentation or code, the user's requirements become the main evidence source.

Do not create fictional current-state sections. Instead build a minimum viable requirements baseline, then design from it.

If the user does not yet know an answer, preserve it as an explicit assumption or open issue unless the uncertainty is too consequential to proceed safely.
