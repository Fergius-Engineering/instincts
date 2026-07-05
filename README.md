# instincts

> Make your coding agent act like a careful senior engineer, not an eager junior.

## What it is

[superpowers](https://github.com/obra/superpowers) is the base. It gives an agent a process: brainstorm, spec, plan, test, verify.

`instincts` is the next layer, one level finer. It doesn't change the workflow. It tunes the agent's reflexes so it acts more like a careful professional: check claims against the source, instrument for the bug you can't reproduce, write for humans, test so the test bites.

Order matters. superpowers first, instincts on top.

## What you get

**Fewer confident wrong answers.** The agent reads the code before telling you what it does, so "yes it works that way" is checked, not guessed. (`verify-against-code`)

**Bugs solved in one round, not five.** It logs enough that a single log dump explains a failure, even one from another machine. (`logging-for-remote-diagnosis`)

**Docs and messages you can actually ship.** Text reads like a person wrote it. (`de-ai-prose`)

**Green tests that mean something.** Tests fail when the feature breaks, so passing isn't a false comfort. (`tests-with-teeth`)

The net is less time catching the agent's mistakes, and more trust when it says "done". Those four are the headline. There are nineteen reflexes in all, listed further down.

## Who this is for

For you if you already run Claude Code (or another agent) on real work and want it to behave more like a careful senior engineer.

Especially if you ship to other people (a product, a library, a service) and "works on my machine" or "looks done" isn't good enough.

Not for you yet if you haven't installed superpowers. This is a layer on top. Start with superpowers, then come back.

## What it is not

Not a fork or replacement of superpowers. It runs alongside it.

Not magic, not a model change. It's a set of instructions the agent reads.

Not a process or a workflow. superpowers covers that. This is reflexes, not steps.

## How this sits with superpowers

A few of these skills sit close to a superpowers skill on purpose. Here's where, so nothing surprises you and you know which wins when both could fire.

- `verify-against-code` sharpens superpowers' verification-before-completion. Not just "did I verify" but "read the actual source before you claim it".
- `tests-with-teeth` sharpens test-driven-development. The test must fail when the feature breaks, with five concrete questions to check that.
- `independent-review-gate` is the non-optional version of requesting-code-review, for work that ships to other people.
- `question-the-premise` and `fix-the-root-cause` pair with systematic-debugging. superpowers debugs; these say which layer to debug.
- `critical-thinking` runs just before brainstorming. Pressure-test the idea with one example before you spec it.
- `plan-with-teeth` sharpens writing-plans. superpowers gives the plan its shape; this one makes every claim in it read from the source, with a check on every step.

Where both could fire, treat instincts as the finer pass on top of the superpowers step, not a replacement for it. Without superpowers these still work, they just have less process around them.

## Status and what it costs

In development, at v0.6.0 with nineteen skills. Still early.

The rules come from one real production project. Sample size is one. They've caught real bugs and real false claims there, but nobody yet knows which ones generalize perfectly. They will change.

It costs more tokens and time, on purpose. The agent reads the source before it answers, adds logs as it builds, checks its own tests and prose. That's slower and not free. Careful work usually is. The trade is fewer wrong answers and less rework, and for serious work that's worth it. If you want fast and cheap over careful, this layer isn't for you.

## Known limitations

Where this is thin, said plainly, so you decide with eyes open.

- n=1, and no numbers yet. The rules come from one production project. We don't have a clean "+X% tokens, -Y% rework" figure or a reproducible eval across many projects. We know that's exactly what this needs, and the plan is to measure it properly rather than invent a number that sounds good. Until then, treat the benefit as a reasoned bet, not a measured fact, and if you want a number, measure it on your own work.
- English only. The skills are written in English and tuned for English prompts. On other languages they may fire less reliably.
- Not tested across every model. Built and used on the larger Claude models. On smaller or older ones the behavior may degrade.
- On Windows, activation needs bash. The SessionStart hook runs through bash (Git Bash). With no bash on PATH it exits quietly, so the agent just won't get the startup nudge, and nothing tells you. The skills still work if the agent reaches for them by description; only the automatic reminder is lost.
- Instructions, not enforcement. These are rules the agent follows, not code that forces anything. Reliability is the model's compliance, not a guarantee.
- Installed as a set. You get all nineteen, not a pick-list. You can ignore or stop using any one, but there's no per-skill install today.

## How it works

Each skill is a plain markdown file. The agent reads the relevant one when it's relevant and follows it. No black box. You can read every rule in this repo before you install it.

There's also one small SessionStart hook: a shell script that runs at the start of each session and reminds the agent that the instincts are available and what each one is for. That's what makes the agent reach for them without you having to ask. It only injects text into the session. It doesn't read or change your code, and you can read the script in `hooks/`.

## Install

```
# 1. the base: superpowers (process)
/plugin marketplace add obra/superpowers
/plugin install superpowers

# 2. the reflex layer: instincts
/plugin marketplace add Fergius-Engineering/instincts
/plugin install instincts
```

## How to start

Install both, then just work. When a reflex applies, the agent loads the matching skill and says so — you don't have to ask for it by name. One thing to try first: ask the agent "does our code do X?" and watch it read the source before answering instead of guessing. That's `verify-against-code` firing.

## A tip: pair a worker with an advisor

Run a second, stronger model as a reviewer that can see the whole transcript, and have the working agent check in with it before it commits to an approach and before it calls anything done. A fresh set of eyes with no stake in the current plan catches wrong assumptions early, while they're still cheap to fix. It's the same idea as a senior engineer glancing over your shoulder at the right moments. This pairs naturally with `verify-against-code` and `tests-with-teeth`. The advisor is who you don't get to fool.

## Before and after

**Without instincts:**

> You: "Our signup trims whitespace from usernames, right?"
> Agent: "Yes, usernames are trimmed before saving."

**With instincts (`verify-against-code` fires):**

> You: "Our signup trims whitespace from usernames, right?"
> Agent: *opens the save path* "It lowercases the username but doesn't trim it. Leading spaces are saved as-is. Want me to add the trim?"

The second answer is the one that saves you a bug.

## The skills

Verify against the world, not your memory:
- [`verify-against-code`](skills/verify-against-code/SKILL.md) — read the source before you claim what the code does.
- [`question-the-premise`](skills/question-the-premise/SKILL.md) — after a few failed fixes, suspect the layer, not the next fix.
- [`critical-thinking`](skills/critical-thinking/SKILL.md) — run a proposal through one concrete example before you build it.
- [`plan-with-teeth`](skills/plan-with-teeth/SKILL.md) — plan from the source, not memory; attack the draft before it ships.

Build for the failure you won't be there to see:
- [`logging-for-remote-diagnosis`](skills/logging-for-remote-diagnosis/SKILL.md) — instrument so one log dump from a stranger explains the bug.
- [`fix-the-root-cause`](skills/fix-the-root-cause/SKILL.md) — fix the layer that made the bad state, not the symptom where it surfaced.
- [`fix-in-the-shared-layer`](skills/fix-in-the-shared-layer/SKILL.md) — a bug in your own shared code is a gap every caller has; fix it where it lives.

Look wider than the line in front of you:
- [`entry-point-audit`](skills/entry-point-audit/SKILL.md) — before a change that must hold everywhere, find every entry point first.
- [`project-onto-all-systems`](skills/project-onto-all-systems/SKILL.md) — project any change onto cache, notifications, persistence, undo, tests.
- [`user-action-edge-cases`](skills/user-action-edge-cases/SKILL.md) — what if the user renames, moves, deletes, or duplicates the thing you depend on?
- [`feasibility-guard`](skills/feasibility-guard/SKILL.md) — push back on work that's fragile or heavier than its value.
- [`opportunistic-fixes`](skills/opportunistic-fixes/SKILL.md) — fix the broken thing you notice in passing, but surface it and get an OK first.
- [`no-duplicate-logic`](skills/no-duplicate-logic/SKILL.md) — read the whole function before adding a case; a second parallel block doubles the output.

Design for real conditions, not the happy path:
- [`performance-at-scale`](skills/performance-at-scale/SKILL.md) — on a hot path, design for the largest realistic input, not the test fixture.
- [`build-release-mindset`](skills/build-release-mindset/SKILL.md) — touching build, release, or CI? start clean, fail fast, version artifacts, validate outputs, know the rollback.
- [`ux-designer-mindset`](skills/ux-designer-mindset/SKILL.md) — walk the interaction and the edge states; a green build says nothing about how it feels.

Finish honestly:
- [`tests-with-teeth`](skills/tests-with-teeth/SKILL.md) — a test must fail when the feature breaks.
- [`de-ai-prose`](skills/de-ai-prose/SKILL.md) — make written text read like a person wrote it.
- [`independent-review-gate`](skills/independent-review-gate/SKILL.md) — green tests and your own pass aren't enough; get a fresh review.

## What's next

This is the transferable set we had. One candidate was left out on purpose: stripped of its original war story, "think ahead and design for the future" turns into a fortune cookie, and a rule with no teeth isn't worth shipping. New ones get added only when they pass the same bar as these: change behavior with a concrete example, not just sound wise.

## These aren't the last word

Take them, edit them, delete the ones that don't fit your work, merge them into your own set, or rewrite them in your own voice. This isn't doctrine. It's a base to build your own instincts on. If a rule makes your agent stronger, keep it. If it doesn't, drop it. The goal is only to make you stronger, so you can grow your own skills and projects on top of this layer.

## Feedback

Found a rule that doesn't hold in your domain, or one that helped? Open an issue. This set is n=1 today. Real use from other projects is how it stops being n=1.

## Credit and license

Built to run on top of [superpowers](https://github.com/obra/superpowers) by Jesse Vincent and Prime Radiant. MIT, see [LICENSE](LICENSE).
