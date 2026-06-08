---
name: fix-in-the-shared-layer
description: Use when you hit a bug while building on your own shared code - a library, base class, SDK, or component. Fix it in the shared layer so every other caller inherits the fix, instead of patching around it in the one spot that surfaced it.
---

## The rule

A bug you hit while using your own shared code is almost never a one-off. It's a gap in the shared layer, and every other caller has it too, they just haven't tripped it yet. Fix it where it lives so the fix is inherited everywhere, instead of working around it in the one place you happened to notice.

## Fires when

While building one feature you hit a bug in a util, base class, component, or SDK that other features also use, and you're tempted to add a local workaround.

## How to apply

When a bug surfaces through shared code, ask "would another caller hit this too?" The answer is usually yes. Fix the shared layer and let every consumer inherit it. Then check the fix against the other callers, not just the one that surfaced it.

A workaround at your call site leaves the trap armed for the next person.

## Worked example

Building the invoices screen, you find your shared date-format helper crashes on a null date. The quick patch is a null check on the invoices screen. But the reports screen and the dashboard call the same helper and will crash the same way. Fixing the helper to handle null fixes all three at once, and stops the next screen from ever hitting it. The local patch would have left two known crashes waiting to be found.

## Red flags

| Thought | Reality |
|---|---|
| "I'll just guard it here" | The same trap is still armed everywhere else. |
| "It only happens in my screen" | It happens wherever the shared code is called. |
| "I don't want to touch the shared util" | That's exactly where the bug is. |
