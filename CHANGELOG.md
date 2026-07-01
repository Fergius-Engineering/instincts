# Changelog

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
