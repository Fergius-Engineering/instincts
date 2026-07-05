---
name: using-instincts
description: Use when doing any work in a project that has the instincts plugin installed
---

superpowers is the base process: brainstorm, spec, plan, TDD, verify. instincts is one level finer — a set of working reflexes that keep that process honest rather than just followed. This skill is the map to them.

## The rule

When an instinct below applies to what you're about to do, **load it with the Skill tool before you act** — the same discipline superpowers puts on any skill the moment it applies. Then announce "Using [instinct] to …" and follow the skill you loaded.

Applying the principle "from memory" is not using the instinct. When you paraphrase the idea instead of loading the skill, you lose its current text and its checklist, and nothing shows the reflex ran — which is exactly how corners get cut. There is no self-activation exemption: nothing runs until you call the Skill tool. Violating the letter here is violating the spirit; "I honored the idea without loading the skill" is not compliance.

| Rationalization | Reality |
|---|---|
| "I applied it internally — same result" | No. You worked from memory, not the current text. No checklist, no trace, corners cut. |
| "The skill just restates what I know" | Then loading it costs seconds and confirms it. If it doesn't, you were about to skip a step. |
| "They activate on their own" | Skills don't self-execute. Nothing runs until you call the Skill tool. |
| "superpowers already forces skills, so these are covered / exempt" | Not exempt either way — you still invoke each instinct explicitly, like any skill. |
| You named an instinct in your reasoning without a Skill call for it | Naming it is not running it. Load the skill, then proceed. |

## The instincts, by what they protect

Load the one that matches the move you're about to make.

Verify against the world, not your memory:
- **verify-against-code** — before you assert anything about what the code or product does.
- **question-the-premise** — when several fixes on one hypothesis have all failed; suspect the layer, not the next fix.
- **critical-thinking** — before building someone's proposal, run it through one concrete example; catch the flaw before code.
- **plan-with-teeth** — before writing an implementation plan or entering plan mode; a plan's claims are read from the source, not remembered.

Build for the failure you won't be there to see:
- **logging-for-remote-diagnosis** — while building anything that could fail on a machine you can't reach.
- **fix-the-root-cause** — when fixing a bug; fix the layer that made the bad state, not the symptom.
- **fix-in-the-shared-layer** — a bug in your own shared code is a gap every caller has; fix it where it lives.

Look wider than the line in front of you:
- **entry-point-audit** — before a change that must hold everywhere; find every entry point first.
- **project-onto-all-systems** — project any change onto cache, notifications, persistence, undo, tests.
- **user-action-edge-cases** — for anything you depend on: what if the user renames, moves, deletes, or duplicates it?
- **feasibility-guard** — before building; push back on work that's fragile or heavier than its value.
- **opportunistic-fixes** — spotted something wrong in the area you're already in? surface it, get an OK, fix it; don't expand scope.
- **no-duplicate-logic** — before adding a case to an existing function, read the whole thing; the case may already be there, and a second block doubles the output.

Design for real conditions, not the happy path:
- **performance-at-scale** — on a hot path, design for the largest realistic input; a linear scan that's fine in the test freezes the field.
- **build-release-mindset** — touching build, release, or CI? start clean, fail fast, version artifacts, validate outputs, know the rollback.
- **ux-designer-mindset** — walk the interaction and the edge states; a green build says nothing about how the thing feels.

Finish honestly:
- **tests-with-teeth** — when you write or review a test; it must fail when the feature breaks.
- **de-ai-prose** — before showing any prose a human will read.
- **independent-review-gate** — before calling complex work done; get a fresh review, green tests aren't enough.

## Pairing with superpowers

These sit on top of superpowers, the base process, installed separately. If the superpowers skills are available in the session, say nothing. Otherwise check for the marker file `~/.instincts/asked`; if it exists, say nothing. If it's absent, ask once: "instincts is meant to run on top of superpowers as its base. Want me to give you the install commands, or run instincts on its own?" (the base installs with `/plugin marketplace add obra/superpowers`, then `/plugin install superpowers`). When they answer, write the empty marker `~/.instincts/asked`, mention it in one short line, and skip writing it if they'd rather you didn't — the marker is the only thing that stops the question repeating each session. If they decline superpowers, instincts works standalone, on their own base or none.
