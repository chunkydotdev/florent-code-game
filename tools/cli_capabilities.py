#!/usr/bin/env python3
"""CLI CAPABILITY WATCH — alarm on platform capabilities we have never triaged.

⛔ WHY THIS EXISTS (two measured instances, both expensive):
1. **`fcode submit` AUTO-ACTIVATES.** Documented in `docs/fcode-cli.md:262`
   for days while the always-loaded procedure said "activate only in the
   instant before firing" — a prototype went live on the rated ladder.
2. **`match unrated --match <id>` PINS THE OPPONENT'S SUBMISSION.** Fully
   documented at `docs/fcode-cli.md:330-342` since 2026-08-09 (`5353bd3`),
   named in ZERO booted files, while `CLAUDE.md` carried "nothing pins or
   even reads THEIRS" as a standing limitation. Rediscovered 2026-08-13
   mid-leg, costing a design amendment and a churn flag.

**The failure class: a capability EXISTS in the tool, is documented in a
reference nobody boots, and is contradicted by the file everybody boots.**
Another boot-file line does not fix it — the next capability lands the same
way. **A tool that reads the tool does.**

WHAT IT DOES: captures `--help` for every command and subcommand, extracts
every option flag, and diffs against `docs/reference/cli-capabilities.json`
(the TRIAGE file). Three alarm classes:
  * **UNTRIAGED** — a flag exists that no human has classified. THE POINT.
  * **NEW** — a flag appeared since the snapshot (platform shipped something).
  * **GONE** — a flag we rely on has disappeared.
Triage values are free text; the discipline is that every flag has one.

Exit 0 = clean, 2 = alarms (⚠ read the CLAUDE.md rule: exit code is NOT a
health signal on this platform — this tool's OWN output is, and it prints
`CLI-CAP: OK`/`CLI-CAP: ALARM` as the load-bearing line).

Usage:
  cli_capabilities.py                 # check against the triage file
  cli_capabilities.py --update        # record current flags as UNTRIAGED
  cli_capabilities.py --selftest
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"
TRIAGE = ROOT / "docs" / "reference" / "cli-capabilities.json"
FLAG_RE = re.compile(r"^\s{2,}(--[a-z0-9][a-z0-9-]*)", re.M)


def help_text(*args: str) -> str:
    p = subprocess.run([str(FCODE), *args, "--help"], capture_output=True,
                       text=True, timeout=60)
    # ⚠ exit code is NOT a health signal here; presence of a Usage: line is
    return (p.stdout or "") + (p.stderr or "")


def subcommands(text: str) -> list[str]:
    out, in_cmds = [], False
    for line in text.splitlines():
        if line.strip() == "Commands:":
            in_cmds = True
            continue
        if in_cmds:
            m = re.match(r"^\s{2,}([a-z][a-z0-9-]*)\s", line)
            if m:
                out.append(m.group(1))
            elif line.strip() == "":
                continue
            elif not line.startswith(" "):
                break
    return out


def scan() -> dict[str, list[str]]:
    """{command path: [flags]} for the root and every (sub)command."""
    caps: dict[str, list[str]] = {}
    root = help_text()
    if "Usage:" not in root:
        raise SystemExit("CLI-CAP: BLIND — `fcode --help` returned no Usage: "
                         "line; refusing to report a verdict")
    caps[""] = sorted(set(FLAG_RE.findall(root)))
    for cmd in subcommands(root):
        t = help_text(cmd)
        caps[cmd] = sorted(set(FLAG_RE.findall(t)))
        for sub in subcommands(t):
            st = help_text(cmd, sub)
            caps[f"{cmd} {sub}"] = sorted(set(FLAG_RE.findall(st)))
    return caps


def load_triage() -> dict:
    if TRIAGE.exists():
        return json.loads(TRIAGE.read_text())
    return {}


def check(caps: dict, triage: dict) -> tuple[list, list, list]:
    untriaged, new, gone = [], [], []
    for cmd, flags in sorted(caps.items()):
        known = triage.get(cmd, {})
        for f in flags:
            if f not in known:
                new.append(f"{cmd} {f}".strip())
            elif not known[f] or known[f] == "UNTRIAGED":
                untriaged.append(f"{cmd} {f}".strip())
    for cmd, known in sorted(triage.items()):
        for f in known:
            if f not in caps.get(cmd, []):
                gone.append(f"{cmd} {f}".strip())
    return untriaged, new, gone


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true",
                    help="record current flags, marking unknown ones UNTRIAGED")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    caps = scan()
    triage = load_triage()
    if args.update:
        merged = {c: {f: triage.get(c, {}).get(f, "UNTRIAGED") for f in fl}
                  for c, fl in caps.items()}
        TRIAGE.parent.mkdir(parents=True, exist_ok=True)
        TRIAGE.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n")
        n = sum(1 for c in merged.values() for v in c.values() if v == "UNTRIAGED")
        print(f"wrote {TRIAGE.relative_to(ROOT)} — "
              f"{sum(len(v) for v in merged.values())} flags, {n} UNTRIAGED")
        return 0
    untriaged, new, gone = check(caps, triage)
    for label, items in (("NEW (platform shipped something)", new),
                         ("UNTRIAGED (nobody has classified this)", untriaged),
                         ("GONE (a flag we recorded has vanished)", gone)):
        for i in items:
            print(f"  {label.split()[0]:9s} {i}")
    total = len(untriaged) + len(new) + len(gone)
    print(f"CLI-CAP: {'ALARM' if total else 'OK'} — "
          f"{sum(len(v) for v in caps.values())} flags across {len(caps)} "
          f"commands; {len(new)} new, {len(untriaged)} untriaged, {len(gone)} gone")
    return 2 if total else 0


def selftest() -> int:
    """Both-ways on the DIFF, and on the parser that feeds it."""
    caps = {"match unrated": ["--map", "--match"], "": ["--version"]}
    # all classified -> silent
    t = {"match unrated": {"--map": "used", "--match": "pins opponent"},
         "": {"--version": "n/a"}}
    assert check(caps, t) == ([], [], []), "clean case alarmed"
    # ⭐ THE CELL THAT MATTERS: the real incident, replayed. --match present in
    # the CLI, absent from triage -> must alarm as NEW.
    t2 = {"match unrated": {"--map": "used"}, "": {"--version": "n/a"}}
    u, n, g = check(caps, t2)
    assert n == ["match unrated --match"], f"failed to flag the real incident: {n}"
    # explicitly-UNTRIAGED must alarm too (a placeholder is not a decision)
    t3 = {"match unrated": {"--map": "used", "--match": "UNTRIAGED"},
          "": {"--version": "n/a"}}
    u, n, g = check(caps, t3)
    assert u == ["match unrated --match"], f"UNTRIAGED not flagged: {u}"
    # a vanished flag alarms
    t4 = {"match unrated": {"--map": "used", "--match": "x", "--json": "x"},
          "": {"--version": "n/a"}}
    assert check(caps, t4)[2] == ["match unrated --json"]
    # help parser: pulls flags and subcommands out of real click output shape
    sample = ("Usage: fcode match [OPTIONS] COMMAND\n\nOptions:\n"
              "  --help  Show this.\n\nCommands:\n  list  List matches.\n"
              "  info  Show a match.\n")
    assert FLAG_RE.findall(sample) == ["--help"]
    assert subcommands(sample) == ["list", "info"]
    print("selftest PASS (clean silent; the real --match incident alarms as NEW; "
          "placeholder UNTRIAGED alarms; vanished flag alarms; parser extracts "
          "flags + subcommands)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
