#!/usr/bin/env python3
"""Measure how the instincts layer behaves in your own Claude Code sessions.

Reads session transcripts, counts when instinct skills were loaded, and prints
aggregates. Nothing leaves your machine and nothing is written anywhere.

    python measure-live-sessions.py [--root PATH] [--json out.json]

Default root is ~/.claude/projects. Numbers in evals/2026-08-live-sessions.md
came from this script.
"""
import argparse
import collections
import io
import json
import os
import re
import sys

SKILLS = [
    "build-release-mindset", "critical-thinking", "de-ai-prose", "entry-point-audit",
    "feasibility-guard", "fix-in-the-shared-layer", "fix-the-root-cause",
    "independent-review-gate", "logging-for-remote-diagnosis", "no-duplicate-logic",
    "opportunistic-fixes", "performance-at-scale", "plan-with-teeth",
    "project-onto-all-systems", "question-the-premise", "tests-with-teeth",
    "user-action-edge-cases", "using-instincts", "ux-designer-mindset",
    "verify-against-code",
]
CODE_EXT = (".cpp", ".h", ".hpp", ".c", ".cs", ".py", ".js", ".ts", ".tsx", ".java",
            ".go", ".rs", ".ps1", ".sh", ".yml", ".yaml", ".json")
PROSE_EXT = (".md", ".txt", ".html", ".rst")
MARKER = "instincts layer is installed"


def content_blocks(message):
    c = message.get("content")
    if isinstance(c, list):
        for b in c:
            if isinstance(b, dict):
                yield b


def read_session(path):
    s = {"injected": False, "turns": 0, "loads": [], "announced": 0, "commit": False,
         "code_edits": 0, "prose_edits": 0, "reviewed_elsewhere": False, "ship_gate": 0}
    turn_texts = []
    for line in io.open(path, encoding="utf-8", errors="replace"):
        if not line.startswith("{"):
            continue
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        kind = entry.get("type")
        if kind == "attachment":
            att = entry.get("attachment") or {}
            if MARKER in (att.get("stdout") or ""):
                s["injected"] = True
            if "about to leave this machine" in json.dumps(att):
                s["ship_gate"] += 1
            continue
        if kind != "assistant" or entry.get("isSidechain"):
            continue
        s["turns"] += 1
        texts, message = [], entry.get("message") or {}
        for b in content_blocks(message):
            if b.get("type") == "text":
                texts.append(b.get("text") or "")
            elif b.get("type") == "tool_use":
                name, inp = b.get("name") or "", b.get("input") or {}
                if name == "Skill":
                    skill = str(inp.get("skill") or "")
                    if skill.startswith("instincts:"):
                        s["loads"].append((s["turns"] - 1, skill.split(":", 1)[1]))
                    elif "code-review" in skill or "verification-before-completion" in skill:
                        s["reviewed_elsewhere"] = True
                elif name == "Agent":
                    s["reviewed_elsewhere"] = True
                elif name in ("Bash", "PowerShell"):
                    if re.search(r"git\s+commit", str(inp.get("command") or "")):
                        s["commit"] = True
                elif name in ("Edit", "Write", "NotebookEdit"):
                    p = str(inp.get("file_path") or "").lower()
                    if p.endswith(PROSE_EXT):
                        s["prose_edits"] += 1
                    elif p.endswith(CODE_EXT):
                        s["code_edits"] += 1
        turn_texts.append(texts)

    # an announcement counts if the skill's name shows up in the text around its load
    for idx, skill in s["loads"]:
        window = []
        for j in (idx - 1, idx, idx + 1):
            if 0 <= j < len(turn_texts):
                window.extend(turn_texts[j])
        if any(skill in t for t in window):
            s["announced"] += 1
    return s


def bucket(turns):
    if turns < 10:
        return "under 10"
    if turns < 30:
        return "10-29"
    if turns < 100:
        return "30-99"
    if turns < 300:
        return "100-299"
    return "300+"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.expanduser("~/.claude/projects"))
    ap.add_argument("--json", dest="json_out")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        sys.exit("no such directory: " + args.root)

    sessions = []
    for dirpath, _dirnames, filenames in os.walk(args.root):
        for fn in filenames:
            if not fn.endswith(".jsonl"):
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) < 2000:
                    continue
                sessions.append(read_session(p))
            except OSError:
                continue

    live = [s for s in sessions if s["injected"]]
    if not live:
        sys.exit("found %d transcripts, none with the instincts payload injected" % len(sessions))

    print("transcripts read: %d | with the payload injected: %d | assistant turns: %d"
          % (len(sessions), len(live), sum(s["turns"] for s in live)))

    print("\nfiring by session length")
    agg = collections.defaultdict(lambda: [0, 0])
    for s in live:
        a = agg[bucket(s["turns"])]
        a[0] += 1
        a[1] += 1 if s["loads"] else 0
    for b in ("under 10", "10-29", "30-99", "100-299", "300+"):
        if b in agg:
            n, hit = agg[b]
            print("  %-9s %4d sessions   %3d loaded something (%.0f%%)" % (b, n, hit, 100.0 * hit / n))

    loads = sum(len(s["loads"]) for s in live)
    announced = sum(s["announced"] for s in live)
    print("\nloads: %d | with the skill named in nearby text: %d (%.0f%%)"
          % (loads, announced, 100.0 * announced / max(loads, 1)))

    repeats = sum(1 for s in live
                  if len(s["loads"]) != len({sk for _, sk in s["loads"]}))
    print("sessions that loaded the same skill twice: %d (the sticky rule should keep this at 0)" % repeats)

    print("\nloads per skill")
    per = collections.Counter(sk for s in live for _, sk in s["loads"])
    for name in SKILLS:
        print("  %-30s %4d" % (name, per.get(name, 0)))

    shipping = [s for s in live if s["commit"] and s["code_edits"] >= 5]
    if shipping:
        gate = sum(1 for s in shipping if any(sk == "independent-review-gate" for _, sk in s["loads"]))
        other = sum(1 for s in shipping if s["reviewed_elsewhere"])
        print("\nsessions that committed with 5+ code-file edits: %d" % len(shipping))
        print("  independent-review-gate loaded: %d (%.0f%%)" % (gate, 100.0 * gate / len(shipping)))
        print("  reviewed some other way:        %d" % other)
        fired = sum(s["ship_gate"] for s in shipping)
        if fired:
            print("  ship-gate hook injections seen:  %d" % fired)

    if args.json_out:
        with io.open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(live, f)
        print("\nwrote %s" % args.json_out)


if __name__ == "__main__":
    main()
