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

Best on top of superpowers — that's the intended setup and the order that makes sense. It works standalone too; you get the reflexes without the process layer around them.

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

In development, at v0.9.0 with nineteen skills. Still early. The bar we hold it to is written down in [docs/expectations.md](docs/expectations.md) — every audit checks the plugin against that list, and the same file says which parts of the bar we have not managed to measure yet. Rules land here when a control run shows they change something: the August 2026 review tested five candidate rules and shipped none of them, because on a fresh context with one task in it a frontier model already did what they said.

There are numbers now, from 545 live sessions rather than from authored test cases: [evals/2026-08-live-sessions.md](evals/2026-08-live-sessions.md). They say the turnstile fires and scales with session length, the sticky rule holds exactly, one rule was ceremony and got cut, and the review gate was firing on one commit in twenty-five until a hook fixed it. They do not say the reflexes make the work better — that needs a comparison arm this corpus cannot provide, and the README will keep saying so until it exists.

The rules come from one real production project. Sample size is one. They've caught real bugs and real false claims there, but nobody yet knows which ones generalize perfectly. They will change.

It costs more tokens and time, on purpose. The agent reads the source before it answers, adds logs as it builds, checks its own tests and prose. That's slower and not free. Careful work usually is. The trade is fewer wrong answers and less rework, and for serious work that's worth it. If you want fast and cheap over careful, this layer isn't for you.

## Known limitations

Where this is thin, said plainly, so you decide with eyes open.

- n=1, and no numbers yet. The rules come from one production project. We don't have a clean "+X% tokens, -Y% rework" figure or a reproducible eval across many projects. We know that's exactly what this needs, and the plan is to measure it properly rather than invent a number that sounds good. Until then, treat the benefit as a reasoned bet, not a measured fact, and if you want a number, measure it on your own work.
- English only. The skills are written in English and tuned for English prompts. On other languages they may fire less reliably.
- Not tested across every model. Built and used on the larger Claude models. On smaller or older ones the behavior may degrade.
- On Windows, activation needs bash. Both hooks run through bash (Git Bash). With no bash on PATH they skip quietly — one note lands in the hook's stderr, visible in debug logs, but the session itself won't tell you. The skills still work if the agent reaches for them by description; what's lost is the automatic reminder at session start and the nudge before a commit.
- Instructions, not enforcement. These are rules the agent follows, not code that forces anything. Reliability is the model's compliance, not a guarantee.
- Installed as a set. You get all nineteen, not a pick-list. You can ignore or stop using any one, but there's no per-skill install today.

## How it works

Each skill is a plain markdown file. The agent reads the relevant one when it's relevant and follows it. No black box. You can read every rule in this repo before you install it.

There are also two small hooks, both shell scripts you can read in `hooks/`. Neither one reads or changes your code; all they do is put text into the session.

The first runs at session start — and again after `/clear` or a context compaction — and injects the entry skill: the rule plus the map of all nineteen reflexes. That's what makes the agent reach for them without you having to ask. On a machine's first sessions it also carries a one-time setup question, until it's been answered once.

The second runs before a shell command and stays silent unless that command is a `git commit`, a `git push` or a `gh pr create`. Then it adds one sentence pointing at the review gate. It never blocks the command and never argues with you: if you asked for the commit, the commit happens. It exists because measurement said the gate was being walked past on twenty-four commits in twenty-five, and no wording of the skill itself had moved that.

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
