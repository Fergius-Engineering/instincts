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

The first time these skills come up in a session, check whether the superpowers skills are available. If they aren't, ask the user once: "instincts is meant to run on top of superpowers as its base. Want me to give you the install commands, or run instincts on its own?" The base installs with `/plugin marketplace add obra/superpowers` then `/plugin install superpowers`.

If they decline, don't ask again in this session. Tell them they can add it later, or use their own base instead, whether that's superpowers or any other process framework they prefer. instincts works standalone either way.
