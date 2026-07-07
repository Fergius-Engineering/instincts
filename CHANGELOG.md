# Changelog

## 0.7.0 — 2026-07-07
- The turnstile is now sticky. 0.5.0 demanded a Skill load every time an instinct applies; on an honest reading of a typical fix-and-commit task that is six to eleven loads (measured: two letter-compliance runs made 9 and 11 calls and judged the repeats required, and under a deadline the same setup collapsed to 2 calls with the rest skipped "from memory"). The rule now: load each instinct once, the first time it applies in the session, and it stays active; after a compact that ate the text, reload it. The boundary stays hard — acting on a skill never loaded this session is still a violation — but the cost argument is spent. Rationalization table rebuilt from the observed excuses ("loading it won't change what I'm about to type", "no time for ceremony", "the map line tells me enough").
- New: `docs/expectations.md` — the behavioral bar we hold the plugin to, numbered and checkable. Audits check the plugin against that list now instead of re-inventing the bar each time.
- `using-instincts`: a precedence section (user instructions win over instincts, mirroring superpowers — there was no precedence rule anywhere in the plugin). Map lines are now each skill's trigger clause only: the no-duplicate-logic line was functionally the whole skill, so an agent could comply from the map without loading anything. A leftover source-project phrase ("freezes the field") left with the payoff clauses.
- The one-time superpowers pairing question moved from the skill into the SessionStart hook: bash checks `~/.instincts/asked` and injects the question only until it's been answered. Steady-state payload shrinks for everyone past their first session. The hook still writes nothing to disk — the agent writes the marker, disclosed, as before.
- `session-start` hardening: the payload is assembled raw and escaped once — the primer and the `<IMPORTANT>` wrapper used to bypass the escaper, so one future quote in the primer would have broken injection in every harness at once. YAML frontmatter is no longer injected, and the escaper covers `\f`, `\b`, `\v`. Verified by running the hook in four scenarios, including planted quotes and control characters.
- `run-hook.cmd`: a failing hook now propagates its real exit code. `exit /b %ERRORLEVEL%` inside an if-block expands at parse time and returned a stale 0 — reproduced: a hook exiting 5 read as success. Fixed with delayed expansion (`!ERRORLEVEL!`); bare `exit /b` does not propagate either, tested. The no-bash fallback now leaves one stderr note instead of vanishing without a trace.
- `logging-for-remote-diagnosis`: "key values" means ids, sizes, counts, and reasons — not payloads. Credentials and tokens never; personal data is payload too. A probe agent instrumenting a login handler kept the password and token out on its own but logged the user's email on every line — that's the line this closes.
- `fix-in-the-shared-layer`: the audit suggested a consent line for shared-behavior changes; a probe run already surfaced the blast radius to the lead before landing, so no edit was made. Recorded here so the finding doesn't resurface.
- README: the hook section now says the injection re-fires on `/clear` and compact and injects the full entry skill, not a "reminder"; "not for you yet without superpowers" replaced with the standalone story the rest of the README already tells; the Windows note mentions the stderr trace; status links `docs/expectations.md`.
- `plugin.json` gains homepage/repository; dead `"async": false` removed from `hooks.json`.

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
