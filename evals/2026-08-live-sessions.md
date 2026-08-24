# What 545 live sessions say about this plugin

The README has promised real numbers since the first release. These are the first ones. They come
from the author's own working sessions rather than from authored test cases, because the thing worth
knowing — whether a reflex layer actually fires while you are three hours into a real problem — is
exactly what a test case cannot reproduce.

Measured 2026-08-25, on the machine where the plugin has been installed since 2026-07-07.

## What was measured

Every session transcript on disk: 607 files, of which 545 carried the plugin's injected payload
(53,885 assistant turns). The rest predate the install or ran with plugins disabled. Four projects,
one developer, one target model. Aggregates only — no transcript content left the machine, and the
numbers below are all the analysis produced.

The miner reads each transcript for Skill calls, tool calls, file paths and hook injections. It was
checked against a session whose behavior was known by hand before trusting it on the rest.

## The turnstile fires, and it holds up as sessions get long

| Session length | sessions | with at least one instinct loaded |
|---|---|---|
| under 10 turns | 147 | 10% |
| 10 to 29 | 143 | 10% |
| 30 to 99 | 81 | 38% |
| 100 to 299 | 131 | 56% |
| 300 or more | 43 | **100%** |

Not one marathon session went by without a reflex loading. The worry that motivated this measurement,
that the layer goes quiet once the session gets long and crowded, is not what happens.

Load density stays flat at roughly seven loads per thousand turns, which is what the sticky rule from
0.7.0 is designed to produce: load once, keep it, stop paying the toll.

## The sticky rule holds exactly

Sessions that loaded the same skill twice: **0 out of 176** that loaded anything at all. Before 0.7.0
the rule demanded a load per occurrence, and measured runs made nine to eleven calls on a single task.
That fix works.

## The announcement half of the rule never happened

The entry skill used to say: load the skill, then announce "Using [instinct] to …". Of 400 loads
across the corpus, 346 have no trace of any announcement near them, and only 25 name the skill at all.
Six sessions were read by hand to be sure: the pattern is a plain sentence about what is being done,
then the Skill call.

So the plugin cut that clause in 0.9.0. The Skill call is the visible trace — it is in the transcript
and in the UI — and an English skill id dropped into a sentence in another language reads as noise,
which is presumably why the model kept dropping it. Keeping the rule would have meant spending payload
budget on a ceremony that seven of eight loads skip anyway.

## Firing is concentrated in two skills

`verify-against-code` (135 loads) and `de-ai-prose` (116) account for 63% of everything. Seven skills
fired three times or fewer in 545 sessions.

That could mean the situation never came up. It mostly doesn't. Below, each "opportunity" is a
deliberately narrow signal — the session ran a test command, edited two or more UI files, and so on —
so every count understates how often the skill's own trigger was present.

| skill | opportunity signal | opportunities | fired |
|---|---|---|---|
| verify-against-code | session ran 30+ turns | 255 | 47% |
| de-ai-prose | 2+ edits to .md/.html/.txt | 207 | 42% |
| tests-with-teeth | ran a test command | 65 | 22% |
| build-release-mindset | ran a build or CI command | 61 | 25% |
| independent-review-gate | ran `git commit` | 58 | **3%** |
| performance-at-scale | perf words in the user's own prompt | 24 | 0% |
| project-onto-all-systems | 2+ edits to model or schema files | 15 | 13% |
| ux-designer-mindset | 2+ edits to UI files | 5 | 0% |

## The finding that changed the release

Of 63 sessions that ran `git commit`, 59 had no review of any kind before the commit: not the
instinct, not a review skill from superpowers, not a review subagent. Tightening the set to sessions
that committed **and** touched five or more code files leaves 47 sessions, with the gate firing in 2
of them and any review at all in 4.

These were not small commits. Median 33 file edits and 359 turns per session.

Three things this does not say. The opportunity detectors are crude, and "ran git commit" is not the
same set as "called shippable work done". Transcripts show the absence of a review, not the presence
of a defect — nothing here proves those commits were bad. And the sessions had no comparison arm
without the plugin, so this measures the layer's own firing rate, not its benefit.

What it does say is that the gate standing between "I think this is done" and everyone else's machine
was firing on one commit in twenty-five, and no amount of skill text had changed that.

## What was done about it, and whether it worked

The wording lever was already known to be dead: an earlier A/B of a widened trigger moved nothing
across two model tiers, which is why 0.8.0 shipped no skill text at all.

So 0.9.0 adds a hook instead. It runs before a Bash or PowerShell command, matches only `git commit`,
`git push` and `gh pr create`, and injects one sentence pointing at the review gate. It never blocks,
and it says plainly that it does not override an instruction to commit.

Tested on a repository with five files of finished, uncommitted work, asked to commit:

| arm | gate loaded |
|---|---|
| plugin without the hook | 1 of 8 runs |
| plugin with the hook | 4 of 5 runs |
| the same, counting only runs where the hook actually fired | 4 of 4 |

The one run that missed never ran a commit command, so the hook had nothing to fire on.

## Honest summary

Two things in this plugin are now measured rather than argued: the turnstile fires and scales, and the
sticky rule holds. One thing was measured and cut. One was measured, found broken, fixed with a
mechanism instead of more words, and re-measured.

None of this establishes that the reflexes make the work better. That needs a comparison against
sessions without the plugin doing the same work, which one developer's transcripts cannot provide.
It remains the open question, and it is still stated as open in the README.
