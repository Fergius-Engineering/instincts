---
name: using-instincts
description: Read once when starting work in a project that has the instincts plugin installed - explains that instincts is the reflex layer on top of superpowers and points to the individual instinct skills
---

superpowers is the base. It gives you a process: brainstorm, spec, plan, TDD, verify. instincts is one level finer. It works on reflexes, not workflow — the habits that make a process honest rather than just followed.

These skills activate on their own when relevant. You don't have to invoke this one first. It's a map, not a turnstile.

The four pilot skills:

- **verify-against-code** — fires before you assert anything about what the code or product does. In an answer, a doc, a commit message, store copy. Confirm against the primary source before stating it.
- **logging-for-remote-diagnosis** — fires while building any mechanic that could fail on a machine you can't reach. Instrument as you write, not after.
- **de-ai-prose** — fires before showing any prose a human will read. Run a read-back pass and cut the tells.
- **tests-with-teeth** — fires whenever you write or review a test. Run the five questions before accepting it.

This set is small and still evolving. It was distilled from real work on one production project, correcting real mistakes. That's the whole claim.

## Pairing with superpowers

These are built to sit on top of superpowers, which gives the base process: brainstorm, spec, plan, TDD, verify. superpowers isn't bundled here. It's a separate plugin the user installs alongside instincts.

Mention this at most once, ever. Follow these steps exactly so the user is never asked twice across sessions:

1. If the superpowers skills are already available in the session, say nothing. There's nothing to set up.
2. Otherwise, check for a marker file at `~/.instincts/asked` in the user's home directory. If it exists, say nothing. The user has already been asked once, and once is enough.
3. If the marker is absent and superpowers is not present, ask once: "instincts is meant to run on top of superpowers as its base. Want me to give you the install commands, or run instincts on its own?" The base installs with `/plugin marketplace add obra/superpowers` then `/plugin install superpowers`.
4. Right after you ask, create the marker file `~/.instincts/asked` (an empty file is enough), whether they said yes or no. This is the only thing that stops the question from coming back in future sessions. Do not skip it.
5. If they decline, tell them they can add superpowers later, or use their own base instead, whether that's superpowers or any other process framework they prefer. instincts works standalone either way.

The marker is what keeps this a one-time question. Without step 4, you would nag the user every session, which is exactly what this avoids.
