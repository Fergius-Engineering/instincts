---
name: tests-with-teeth
description: Use whenever you write or review a test. A test that still passes after you delete the feature it covers is hollow. Run the five questions before accepting any test.
---

## The rule

A test exists to fail when the thing it covers breaks. If you could delete the feature and the test stays green, it protects nothing. It's worse than no test, because it looks like coverage. Before accepting any test, run it through five questions.

## The five questions

1. **Removal** — mentally delete the line the test targets. Does the test now fail? If no, it's hollow.
2. **Reach** — list every guard and early return between setup and the assertion. Does the setup trip one of them first, so execution never reaches the target? Then the assertion is dead.
3. **Distinguishability** — would the test pass for a wrong implementation too? Give two inputs different values so the test can only pass if the right one was used.
4. **Environment gap** — what does the real feature rely on that the test harness lacks (a real database, a registry, a network)? If the gap means the real path can't run, test at the lowest level that does run and label what it does and doesn't prove.
5. **Algorithm gap** — is the novel logic (a sort, a filter, a dedup) tested directly? An end-to-end test can produce the right final output through a compensating bug. Test the tricky function on its own with inputs that would expose a wrong algorithm.

## Worked example

You're testing a discount function. The test: `applyDiscount(cart)` returns a number >= 0. It passes. It's hollow. It passes whether the discount is 10%, 0%, or the function just returns the original total. Now make it distinguish: a $100 cart with a 10% code should return exactly $90. Delete the discount math and it returns $100, and the test fails. That version has teeth.

## Red flags

| Test smell | Why it's hollow |
|---|---|
| Asserts "does not crash" | Not crashing isn't correctness. |
| Asserts a value >= 0 / not null | Passes for almost any implementation. |
| Setup uses an input that triggers an early return | The assertion is never reached. |
| Same value passed for two different inputs | Can't tell which one the code used. |
| Only an end-to-end path, novel logic never tested alone | A compensating bug can hide. |
