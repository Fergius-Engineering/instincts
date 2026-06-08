---
name: independent-review-gate
description: Use before you call complex or shippable work done - get a fresh, independent review of the whole change. Your own pass plus green tests is not enough; you read past your own mistakes.
---

## The rule

Your own review and a green test suite are not enough. You're invested in the approach, so you read past your own mistakes, and the tests only cover what you already thought to check. Before calling complex work done, have someone or something with no stake review the whole change.

A fresh set of eyes catches the defect that's obvious in hindsight and invisible to you.

## Fires when

Finishing a feature or a spec. Before merging. Before claiming "done" on anything non-trivial, or anything that ships to other people.

## How to apply

Hand the full diff to an independent reviewer with explicit angles to check: correctness, edge cases, the branches no test touches, backward compatibility. Fix the blockers and cover each one with a test. Then re-review the fix itself — a second pass catches the inverted-fix mistake faster than a new test would.

The green suite is not the gate. The independent verdict is.

## Worked example

Your change passes all 200 tests and your own read-through. A reviewer with fresh eyes notices that one branch — the error path no test covers — has an inverted condition: it retries on success and gives up on failure.

The suite was green because it only ran the happy path. Your own review missed it because you "knew" what the code was meant to do, so you read what you intended instead of what you wrote.

The independent pass caught it before users did.

## Red flags

| Thought | Reality |
|---|---|
| "Tests pass, so it's done" | Tests only cover what you thought to test. |
| "I already reviewed it myself" | You can't see your own blind spot. |
| "It's obviously correct" | The expensive bugs always look obvious until they bite. |
