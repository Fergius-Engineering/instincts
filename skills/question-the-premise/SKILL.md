---
name: question-the-premise
description: Use when stuck after several failed fixes on the same hypothesis - step back and question whether you're fixing the right layer at all, before trying the next fix. Being data-driven inside a wrong frame still fails.
---

## The rule

Working by hypothesis, test, confirm only helps inside the right frame. If two or three well-reasoned fixes all fail, the likely problem is your premise, not your next fix. Stop and ask: have I actually confirmed the bug is in the layer I'm attacking?

## Fires when

Two or three fixes on the same hypothesis have all failed. A symptom that looks impossible — works in one path, fails in another that shares the same code. You're about to do a big rewrite or a deep dive to force the current theory to work.

## How to apply

After about two or three failed fixes, treat the premise as the suspect, not the code. Get an outside view from someone or something that sees the whole story and has no stake in your theory.

Chase the impossible-looking discrepancy. It points at the layer you're not looking at.

And one more thing: a missing log line is not proof the code didn't run. The log level may have been off. Verify, don't infer from silence.

## Worked example

A test is flaky. You add a retry, still flaky. You add a sleep, still flaky. You mock the clock, still flaky. Three reasoned fixes, all failed.

The premise was wrong. Another test in the suite mutates a shared global, and the run order decides the outcome. Every timing fix was reading the wrong layer entirely.

The tell was right there the whole time: it passed alone but failed in the suite. That impossible-looking symptom was pointing at the real layer.

## Red flags

| Thought | Reality |
|---|---|
| "Just one more fix and it'll work" after 2–3 have failed | Suspect the premise instead. |
| "No log line for it, so it didn't run" | Or the log level was off. Verify emission. |
| "I'll just rewrite this module" | Before you've confirmed the bug is even in that module. |
