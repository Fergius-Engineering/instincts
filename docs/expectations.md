# Expectations

What we expect an agent to actually do in a session with instincts installed. This is the reference we pull the plugin toward: audits check the plugin against these numbers, and every finding is either a violated expectation or a missing one. When reality teaches us something, the expectation changes first and the plugin follows.

Each entry is written to be checkable — from a transcript, from the repo, or by running a script. If an expectation can't be checked, it doesn't belong here.

## Activation

- **E1.** In a fresh session in a project with the plugin installed, the agent knows the reflex map without being asked. The hook injects the entry skill on startup, `/clear`, and compact — in Claude Code, Cursor, and Copilot CLI.
- **E2.** The injected payload routes, it doesn't teach. Reading the injection alone must never be enough to execute a skill's method — the method lives behind the Skill tool. A map line that summarizes the method is a bug.
- **E3.** The assembled steady-state payload stays under ~950 words (0.7.0 measures 906, down from ~970 at 0.6.0) and must not grow release-over-release without a written reason in the CHANGELOG. The one-time setup question appears only until it's been answered once on that machine, then never again.

## Turnstile

- **E4.** When an instinct applies to the move at hand, the agent loads it with the Skill tool and announces it — before acting on it, the first time it applies in the session.
- **E5.** Loads are sticky. Once loaded, the skill stays active for the rest of the session with no repeat ritual. After a compact that dropped the skill's text, the agent reloads it before relying on it.
- **E6.** The layer never demands per-occurrence loads. A typical task costs at most one load per applicable skill; a rule that requires six or more loads to be followed honestly is a broken rule, not a strict one.
- **E7.** No instinct is acted on from memory or from the map line alone. If the agent names an instinct, there is a Skill call for it in this session's transcript.
- **E8.** User instructions win. CLAUDE.md and direct requests override any instinct; the agent never cites a skill to refuse what the user explicitly asked for.

## Content

- **E9.** Every skill passes the teeth test: a concrete worked example in a neutral domain, and after generalization the rule still changes behavior. Fortune cookies get cut, not shipped.
- **E10.** Nothing from the source project leaks into skill text or the map — no engine names, no game domain, no phrasing that only makes sense in the original codebase.
- **E11.** Descriptions and map lines carry the trigger only: when to fire, never how the method works.
- **E12.** A skill that sits close to a superpowers skill says which one it sharpens and how it differs, so the pair never reads as a duplicate.
- **E13.** Skills don't contradict each other, and a skill that tells the agent to expose data carries the matching safety line (logging: ids, sizes, counts — never payloads, credentials, or personal data).

## Cross-platform

- **E14.** Hooks work on macOS and Linux with system bash, and on Windows with Git Bash. Hook scripts stay LF. On a bash-less Windows machine the plugin degrades to skills-only, and the README says exactly that.
- **E15.** The Windows wrapper propagates the hook's real exit code. A hook that fails must be visible as failing, not swallowed into success.
- **E16.** The injected JSON survives any future edit of the skill text: quotes, backslashes, and control characters are escaped on the assembled payload, not on hand-picked fragments.

## Honesty

- **E17.** README claims match the implementation exactly — hook events, payload behavior, the standalone story. Drift between the README and the code is a bug of the same rank as a code bug.
- **E18.** No manufactured numbers, no staged endorsements. n=1 is stated plainly until a real eval exists.
- **E19.** `plugin.json` and `marketplace.json` versions always match, and every release bumps them together with a CHANGELOG entry.
