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

The net is less time catching the agent's mistakes, and more trust when it says "done".

## Who this is for

For you if you already run Claude Code (or another agent) on real work and want it to behave more like a careful senior engineer.

Especially if you ship to other people (a product, a library, a service) and "works on my machine" or "looks done" isn't good enough.

Not for you yet if you haven't installed superpowers. This is a layer on top. Start with superpowers, then come back.

## What it is not

Not a fork or replacement of superpowers. It runs alongside it.

Not magic, not a model change. It's a set of instructions the agent reads.

Not a process or a workflow. superpowers covers that. This is reflexes, not steps.

## Status and what it costs

In development. v0.1, four skills.

The rules come from one real production project. Sample size is one. They've caught real bugs and real false claims there, but nobody yet knows which ones generalize perfectly. They will change.

It costs more tokens and time, on purpose. The agent reads the source before it answers, adds logs as it builds, checks its own tests and prose. That's slower and not free. Careful work usually is. The trade is fewer wrong answers and less rework, and for serious work that's worth it. If you want fast and cheap over careful, this layer isn't for you.

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

Install both, then just work. The skills activate on their own when they're relevant. You don't call them. One thing to try first: ask the agent "does our code do X?" and watch it read the source before answering instead of guessing. That's `verify-against-code` firing.

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

- [`verify-against-code`](skills/verify-against-code/SKILL.md) — read the source before you claim what the code does.
- [`logging-for-remote-diagnosis`](skills/logging-for-remote-diagnosis/SKILL.md) — instrument so one log dump from a stranger explains the bug.
- [`de-ai-prose`](skills/de-ai-prose/SKILL.md) — make written text read like a person wrote it.
- [`tests-with-teeth`](skills/tests-with-teeth/SKILL.md) — a test must fail when the feature breaks.

## What's next

More instincts are in the queue: entry-point-audit, question-the-premise, project-onto-all-systems, and a few more. Each one ships only after it survives the same test the four here passed. It has to change behavior with a concrete example, not just sound wise. Some candidates won't make it, and that's fine.

## These aren't the last word

Take them, edit them, delete the ones that don't fit your work, merge them into your own set, or rewrite them in your own voice. This isn't doctrine. It's a base to build your own instincts on. If a rule makes your agent stronger, keep it. If it doesn't, drop it. The goal is only to make you stronger, so you can grow your own skills and projects on top of this layer.

## Feedback

Found a rule that doesn't hold in your domain, or one that helped? Open an issue. This set is n=1 today. Real use from other projects is how it stops being n=1.

## Credit and license

Built to run on top of [superpowers](https://github.com/obra/superpowers) by Jesse Vincent and Prime Radiant. MIT, see [LICENSE](LICENSE).
