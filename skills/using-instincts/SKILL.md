---
name: using-instincts
description: Use when doing any work in a project that has the instincts plugin installed
---

superpowers is the base process: brainstorm, spec, plan, TDD, verify. instincts is one level finer — a set of working reflexes that keep that process honest rather than just followed. This skill is the map to them.

## The rule

When an instinct below applies to what you're about to do, **load it with the Skill tool before you act** — the same discipline superpowers puts on any skill the moment it applies. Then announce "Using [instinct] to …" and follow the skill you loaded.

**Applying the principle "from memory" is NOT using the instinct.** Naming verify-against-code in your reasoning and moving on is skipping it. When you paraphrase the idea instead of loading the skill you lose its current text, you lose its checklist, and you leave no visible trace that the reflex ran — which is exactly how corners get cut. The reflex runs when you invoke the skill, not when you recall that it exists.

An earlier version of this map said these skills "activate on their own — you don't have to invoke them." That was wrong: it read as permission to internalize the principle instead of running it, and skills got skipped even with superpowers installed. There is no such exemption. instincts are not carved out of the invoke-the-skill rule; if anything they bind harder.

**Violating the letter here is violating the spirit.** "I honored the idea without loading the skill" is not compliance.

### Red flags — you are skipping an instinct

- "I already applied that principle in my head."
- "I know what it says, loading it is just ceremony."
- "These activate on their own; invoking is optional."
- "superpowers' invoke rule is about superpowers skills, not these."
- You named an instinct (verify-against-code, entry-point-audit, tests-with-teeth …) in your reasoning without a Skill call for it.

All of these mean: STOP, load the skill with the Skill tool, then proceed.

| Rationalization | Reality |
|---|---|
| "I applied it internally — same result" | No. You worked from memory, not the current text. No checklist, no trace, corners cut. |
| "The skill just restates what I know" | Then loading it costs seconds and confirms it. If it doesn't, you were about to skip a step. |
| "They activate on their own" | Skills don't self-execute. Nothing runs until you call the Skill tool. |
| "superpowers already forces skills, so these are covered / exempt" | Not exempt either way — you still invoke each instinct explicitly, like any skill. |

## The instincts, by what they protect

Load the one that matches the move you're about to make.

Verify against the world, not your memory:
- **verify-against-code** — before you assert anything about what the code or product does.
- **question-the-premise** — when several fixes on one hypothesis have all failed; suspect the layer, not the next fix.
- **critical-thinking** — before building someone's proposal, run it through one concrete example; catch the flaw before code.

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

This set is small and still evolving. It was distilled from real work on one production project, correcting real mistakes. That's the whole claim — and it's separate from the rule above: be humble about how proven the set is, be strict about loading the skill when it applies.

## Pairing with superpowers

These are built to sit on top of superpowers, which gives the base process: brainstorm, spec, plan, TDD, verify. superpowers isn't bundled here. It's a separate plugin the user installs alongside instincts.

Mention this at most once, ever. Follow these steps exactly so the user is never asked twice across sessions:

1. If the superpowers skills are already available in the session, say nothing. There's nothing to set up.
2. Otherwise, check for a marker file at `~/.instincts/asked` in the user's home directory. If it exists, say nothing. The user has already been asked once, and once is enough.
3. If the marker is absent and superpowers is not present, ask once: "instincts is meant to run on top of superpowers as its base. Want me to give you the install commands, or run instincts on its own?" The base installs with `/plugin marketplace add obra/superpowers` then `/plugin install superpowers`.
4. When they answer, record the outcome so the question doesn't come back next session: write an empty marker file at `~/.instincts/asked`. Mention it in the same reply, in one short line ("I'll note this at `~/.instincts/asked` so I don't ask again"), and skip writing it if they'd rather you didn't. Don't turn this into a second question or a separate prompt. The marker is the only thing that stops the question repeating each session, so write it unless they opt out.
5. If they decline, tell them they can add superpowers later, or use their own base instead, whether that's superpowers or any other process framework they prefer. instincts works standalone either way.

The marker is what keeps this a one-time question. Without step 4, you would nag the user every session, which is exactly what this avoids.
