#!/usr/bin/env python3
"""Measure how the instincts layer behaves in your own Claude Code sessions.

Reads session transcripts, counts when instinct skills were loaded, and prints
aggregates. Nothing leaves your machine and nothing is written anywhere.

    python measure-live-sessions.py [--root PATH] [--json out.json]

Default root is ~/.claude/projects. Numbers in evals/2026-08-live-sessions.md
came from this script.

The second half of the report is the useful part: for each skill it looks for
sessions where that skill's own trigger was plainly present, and reports how
often it actually loaded. Trigger signals differ by the kind of project, so the
script guesses the shape of each session first - a UE session's moments are a
cook and a package, a Python service's are a test run and a deploy. Detector
fidelity is the whole game here: a signal that is merely nearby, like grepping a
log while debugging, is not the same as the skill's own trigger.
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

UNREAL_HINT = re.compile(r"(\.uplugin|\.uproject|\.uasset|RunUAT|Build\.bat|UnrealEditor|/Source/|\\Source\\)", re.I)
PY_HINT = re.compile(r"(\.py\b|pytest|venv|pip install|systemd|Get-ScheduledTask)", re.I)

TEST_CMD = re.compile(r"(pytest|npm (run )?test|jest|go test|dotnet test|RunUAT.*RunTests|-ExecCmds=.*Automation)", re.I)
BUILD_CMD = re.compile(r"(RunUAT|Build\.bat|BuildCookRun|docker build|npm run build|gh workflow|dotnet publish|\.github)", re.I)
DEPLOY_CMD = re.compile(r"(systemd-run|Restart-Service|Start-ScheduledTask|scp |rsync |steamcmd|kubectl|docker compose up)", re.I)
LOG_READ = re.compile(r"(\.log\b|Get-Content .*log|tail -f|journalctl|Select-String .*log)", re.I)
PROFILE_CMD = re.compile(r"(stat unit|stat fps|unrealinsights|\.utrace|cProfile|py-spy|perf record|Measure-Command)", re.I)
BUILD_PATH = re.compile(r"(\.github[/\\]|Dockerfile|docker-compose|\.gitlab-ci|Jenkinsfile|[/\\]Build[/\\]|\.uplugin$|package\.json$|pyproject\.toml$)", re.I)
DIAG_WORDS = re.compile(r"(log|crash|telemetr|diagnos|sentry|alert|лог|краш|телеметр|диагност|алерт)", re.I)

UI_PATH = re.compile(r"(widget|/ui/|\\ui\\|wbp_|umg|slate|hud|\.tsx$|\.jsx$|\.css$)", re.I)
MODEL_PATH = re.compile(r"(dataasset|datatable|savegame|schema|migration|models?\.py|\.sql$|config\.ya?ml)", re.I)
SHARED_PATH = re.compile(r"(plugins[/\\]|[/\\]lib[/\\]|[/\\]common[/\\]|[/\\]shared[/\\]|[/\\]utils?[/\\])", re.I)
PERF_WORDS = re.compile(r"(fps|hitch|profil|optimi[sz]|slow|latency|memory leak|просадк|тормоз|оптимиз)", re.I)
BUG_WORDS = re.compile(r"(bug|crash|broken|fails?|regression|баг|краш|падает|сломал)", re.I)
EXT_STATE = re.compile(r"(renamed|deleted|moved|missing file|удалил|переименовал|переместил)", re.I)


def content_blocks(message):
    c = message.get("content")
    if isinstance(c, list):
        for b in c:
            if isinstance(b, dict):
                yield b


def read_session(path):
    s = {"injected": False, "turns": 0, "loads": [], "announced": 0, "commit": False,
         "code_edits": 0, "prose_edits": 0, "reviewed_elsewhere": False, "ship_gate": 0,
         "paths": [], "cmds": [], "user_text": ""}
    turn_texts, user_text = [], []
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
        if kind == "user" and not entry.get("isSidechain"):
            c = (entry.get("message") or {}).get("content")
            if isinstance(c, str):
                user_text.append(c[:4000])
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
                    cmd = str(inp.get("command") or "")[:600]
                    s["cmds"].append(cmd)
                    if re.search(r"git\s+commit", cmd):
                        s["commit"] = True
                elif name in ("Edit", "Write", "NotebookEdit"):
                    p = str(inp.get("file_path") or "")
                    s["paths"].append(p)
                    low = p.lower()
                    if low.endswith(PROSE_EXT):
                        s["prose_edits"] += 1
                    elif low.endswith(CODE_EXT):
                        s["code_edits"] += 1
        turn_texts.append(texts)

    for idx, skill in s["loads"]:
        window = []
        for j in (idx - 1, idx, idx + 1):
            if 0 <= j < len(turn_texts):
                window.extend(turn_texts[j])
        if any(skill in t for t in window):
            s["announced"] += 1
    s["user_text"] = "\n".join(user_text)
    return s


def shape(s):
    blob = " ".join(s["paths"]) + " " + " ".join(s["cmds"])
    if UNREAL_HINT.search(blob):
        return "unreal"
    if PY_HINT.search(blob):
        return "service"
    return "generic"


def opportunities(s):
    """Which skills had their trigger plainly present in this session."""
    kind = shape(s)
    cmds = " ".join(s["cmds"])
    paths = " ".join(s["paths"])
    hits = set()

    if s["commit"] and s["code_edits"] >= 5:
        hits.add("independent-review-gate")
    if TEST_CMD.search(cmds):
        hits.add("tests-with-teeth")
    if len(BUILD_PATH.findall(paths)) >= 1 or (kind == "service" and DEPLOY_CMD.search(cmds) and s["code_edits"]):
        hits.add("build-release-mindset")
    if s["code_edits"] >= 3 and DIAG_WORDS.search(s["user_text"]):
        hits.add("logging-for-remote-diagnosis")
    if PROFILE_CMD.search(cmds) or (PERF_WORDS.search(s["user_text"]) and s["code_edits"]):
        hits.add("performance-at-scale")
    if len(UI_PATH.findall(paths)) >= 2:
        hits.add("ux-designer-mindset")
    if len(MODEL_PATH.findall(paths)) >= 2:
        hits.add("project-onto-all-systems")
    if len(SHARED_PATH.findall(paths)) >= 2 and BUG_WORDS.search(s["user_text"]):
        hits.add("fix-in-the-shared-layer")
    if EXT_STATE.search(s["user_text"]):
        hits.add("user-action-edge-cases")
    if s["prose_edits"] >= 2:
        hits.add("de-ai-prose")
    if s["turns"] >= 30:
        hits.add("verify-against-code")
    return kind, hits


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

    shapes = collections.Counter(shape(s) for s in live)
    print("session shapes: " + ", ".join("%s %d" % kv for kv in shapes.most_common()))

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
    repeats = sum(1 for s in live if len(s["loads"]) != len({sk for _, sk in s["loads"]}))
    print("sessions that loaded the same skill twice: %d (the sticky rule should keep this at 0)" % repeats)

    print("\ntrigger present -> did it fire")
    opp = collections.defaultdict(lambda: [0, 0])
    per_shape = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
    for s in live:
        kind, hits = opportunities(s)
        loaded = {sk for _, sk in s["loads"]}
        for sk in hits:
            opp[sk][0] += 1
            per_shape[kind][sk][0] += 1
            if sk in loaded:
                opp[sk][1] += 1
                per_shape[kind][sk][1] += 1
    print("  %-30s %8s %7s %7s" % ("skill", "moments", "fired", "rate"))
    for sk in sorted(opp, key=lambda k: -opp[k][0]):
        n, hit = opp[sk]
        print("  %-30s %8d %7d %6.0f%%" % (sk, n, hit, 100.0 * hit / max(n, 1)))

    for kind in sorted(per_shape):
        rows = [(sk, v[0], v[1]) for sk, v in per_shape[kind].items() if v[0] >= 5]
        if not rows:
            continue
        print("\n  %s sessions only" % kind)
        for sk, n, hit in sorted(rows, key=lambda r: -r[1]):
            print("    %-28s %8d %7d %6.0f%%" % (sk, n, hit, 100.0 * hit / n))

    never = [sk for sk in SKILLS if not any(sk == s2 for s in live for _, s2 in s["loads"])]
    if never:
        print("\nnever loaded once in this corpus: " + ", ".join(never))

    if args.json_out:
        with io.open(args.json_out, "w", encoding="utf-8") as f:
            json.dump([{k: v for k, v in s.items() if k not in ("cmds", "user_text", "paths")} for s in live], f)
        print("\nwrote %s" % args.json_out)


if __name__ == "__main__":
    main()
