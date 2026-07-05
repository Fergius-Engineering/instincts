# Changelog

## 0.6.0 — 2026-07-06
- Added `plan-with-teeth`: a plan's claims must be read from the source this session, not remembered. An assumptions ledger with [VERIFIED]/[HYPOTHESIS] labels, two or three real alternatives, a check on every step, and an attack pass on the draft before anyone sees it. Sharpens superpowers' writing-plans the way tests-with-teeth sharpens TDD. Nineteen skills total.
- README caught up with 0.5.0: the version and skill count were stale (still 0.4.0/eighteen), and "the skills activate on their own, you don't call them" contradicted the 0.5.0 turnstile rule. Both fixed.
- SessionStart primer now names the design-for-real-conditions group (missed when 0.4.0 added it), and the hook comment no longer says "four reflex skills".
- Audit pass over all nineteen skills. Every description now states only when to fire: a method summary in the description lets an agent follow the summary and skip the body, and almost every skill had one. Sharpens-lines added where a skill sits on a superpowers sibling (critical-thinking, question-the-premise, fix-the-root-cause, feasibility-guard, tests-with-teeth, independent-review-gate). opportunistic-fixes: a broken sentence in the rule rewritten, plus an explicit boundary with fix-in-the-shared-layer. fix-in-the-shared-layer got a new worked example (a timezone-mangling shared helper instead of a second null crash) so it stops mirroring fix-the-root-cause. question-the-premise now points to logging-for-remote-diagnosis instead of restating its absence-is-not-proof rule. de-ai-prose and tests-with-teeth gained their missing trigger and red-flags sections. Two source-project leaks neutralized ("eight engine versions", "live in the editor").
- `using-instincts` slimmed from ~1180 to ~740 words. It is injected into every session, so its length is a per-session tax: the red-flag list merged into the rationalization table, the history paragraph cut, the superpowers pairing protocol compressed, the provenance hedge left to the README.

## 0.5.0 — 2026-07-01
- `using-instincts` is now a turnstile. The old framing — "these activate on their own, you don't have to invoke them; a map, not a turnstile" — was read, even with superpowers installed, as permission to apply an instinct from memory and never load its skill, so the agent got the paraphrase but not the current text, the checklist, or a visible trace. That carve-out is removed: when an instinct applies you load it with the Skill tool and announce "Using [instinct]" before acting; applying it from memory does not count. Added red flags and a rationalization table (including "superpowers already forces skills, so these are exempt"). The SessionStart primer now carries the same MUST-invoke wording.
- Fixed a version drift: the `marketplace.json` plugin entry was still 0.3.1 while `plugin.json` had moved to 0.4.0. Both are now 0.5.0.

## 0.4.0 — 2026-06-23
- Added four design-for-reality instincts: `performance-at-scale`, `build-release-mindset`, `ux-designer-mindset`, `no-duplicate-logic`. Eighteen skills total.

## 0.3.1 — 2026-06-09
- `using-instincts`: the agent now discloses the `~/.instincts/asked` marker write in the same reply and lets the user opt out, instead of writing it silently.
- README: the metrics limitation now states plainly that real numbers and an eval are planned, not invented.

## 0.3.0 — 2026-06-09
- Added `critical-thinking` (run a proposal through one concrete example before building it) and `opportunistic-fixes` (surface and get an OK before fixing the broken thing you notice in passing). Fourteen skills total.
- README: added a superpowers overlap section and a known-limitations section.

## 0.2.0 — 2026-06-09
- Added eight skills: `question-the-premise`, `entry-point-audit`, `independent-review-gate`, `project-onto-all-systems`, `feasibility-guard`, `user-action-edge-cases`, `fix-in-the-shared-layer`, `fix-the-root-cause`. Twelve skills total.
- Added a SessionStart hook so the agent reaches for the skills without being asked.

## 0.1.0 — 2026-06-08
- First four pilot skills: `verify-against-code`, `logging-for-remote-diagnosis`, `de-ai-prose`, `tests-with-teeth`.
- Plugin and single-repo marketplace, entry skill, README.
