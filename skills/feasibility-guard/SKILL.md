---
name: feasibility-guard
description: Use before building or agreeing to build something - push back when the work is unnecessary, over-complex, fragile, or heavier than the value it returns. Saying "skip this" or "simpler is enough" is part of the job.
---

## The rule

Not every request should be built as asked. Before you start, weigh the cost against the value. If a feature is over-engineered, a test would be flaky and need heavy mocking, or a check would drown the user in false positives, say so and propose the smaller thing. Agreeing to bad work quickly is not helping.

## Fires when

About to build a feature, write a test, or add a check. When a request sounds big or clever. When you catch yourself reaching for a lot of mocking or scaffolding.

## How to apply

Ask "is this worth the effort, and will it actually work?" before you start.

Flag a test that would be fragile or need mocking half the system. Flag a check that would fire on too many false positives. Flag complexity that outweighs the benefit. Offer the smaller version, or say skip it.

Don't just agree because it was asked.

## Worked example

You're asked to add a test for a function, but covering it properly would mean mocking the database, the clock, the network, and three collaborators, and the test would break on any refactor. That's a fragile test that protects almost nothing. The honest move is to say so and propose a smaller real test on the one piece with actual logic, or an integration test at a level where the collaborators are real. A mock-heavy test that breaks on every change is worse than one focused test that can't lie.

## Red flags

| Thought | Reality |
|---|---|
| "They asked for it, so build it" | Asked is not the same as worth it. |
| "I'll just mock everything" | A test held up by ten mocks is testing the mocks. |
| "More coverage is always better" | Coverage of the wrong thing is just noise. |
