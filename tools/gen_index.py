#!/usr/bin/env python3
"""Generate `tools/INDEX.md` — 86 tools, grouped by THE QUESTION THEY ANSWER.

    .venv/bin/python tools/gen_index.py            # rewrite tools/INDEX.md
    .venv/bin/python tools/gen_index.py --check    # exit 1 if INDEX.md is stale
    .venv/bin/python tools/gen_index.py --selftest

===== WHY THIS EXISTS =====
`tools/` holds 86 python entry points plus 18 corpus builders, 13 monitors and
~20 shell scripts, and **there was no index of any kind**. `docs/tooling.md`
named SIX of them. Ten appeared in no document at all; most of the rest appeared
only inside `QUEUE.md`, an ~80k-token file, which is not discoverability.

**83 of 86 carry a real module docstring** — the knowledge existed and was simply
never collected. So this GENERATES rather than curates: a hand-written index is
a second source of truth that goes stale the first time someone adds a tool, and
this repo has measured that failure mode repeatedly (`docs/tooling.md` naming 6
of 86; `builder.md` bounding `coordination.md` at "41k lines" when it had grown
to 57k).

===== WHAT IT CANNOT DO, STATED PLAINLY =====
Grouping is by NAME PATTERN against `GROUPS` below. That is a heuristic, and a
tool whose name does not match lands in `unclassified` — **visibly**, rather than
being silently filed somewhere plausible. An unclassified tool is a prompt to
name it better or to add a pattern; it is not an error.

The read-only/mutating flag is a STATIC scan for write and subprocess calls. It
is deliberately over-inclusive: a tool that only writes a temp file still reads
`mutates`. **Treat `read-only` as a claim worth trusting and `mutates` as "check
before running blind", never the reverse.**
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
INDEX = TOOLS / "INDEX.md"

# (heading, blurb, name patterns). Order matters: first match wins.
GROUPS = [
    ("Live state — what is true right now",
     "Start here. These answer questions about the ladder, the holder and the "
     "control. **`now.py` is the single canonical entry point**; the others are "
     "narrower reads of the same surfaces.",
     (r"^now$", r"^fleet_health$", r"^freshness$", r"^ship_ledger$",
      r"^delta_status$", r"^plank_status$", r"^control_pin$", r"^era_guard$")),
    ("Gates — things that REFUSE",
     "Run before an action, and they exit nonzero to stop it. This repo's "
     "measured finding is that a tool that exits 1 binds where a paragraph "
     "does not.",
     (r"^gate$", r"^auto_gate$", r"^prereg_check$", r"^preflight$", r"^queue_check$",
      r"^target_value$", r"^rate_budget$", r"^claim_check$", r"^cite_check$",
      r"^name_check$", r"^inert_check$", r"^corpus_sanity$", r"^slot_rule$",
      r"^slot_sprt$", r"^sprt$", r"^audit_trigger$", r"^cli_capabilities$")),
    ("Shipping and the ladder slot",
     "⛔ `fcode submit` AUTO-ACTIVATES. Only ever submit via `submit_clean.py`.",
     (r"^submit_clean$", r"^ship_", r"^leg_", r"^match_ledger$", r"^oppver_window$",
      r"^escape_tape$", r"^ladder_census$", r"^reprice$")),
    ("Running batteries and the fleet",
     "Local shards and remote workers. The operator interface is: append a line "
     "to `scratchpad/corefill_work.txt`.",
     (r"^arena$", r"^fleet_dispatch$", r"^watchdog$", r"^stack$", r"^rebase_arm$",
      r"^det$", r"^dose$", r"^mech_battery$", r"^tune$", r"^stub_engine$",
      r"^overnight_read$", r"^treehash$")),
    ("Reading the replay corpus",
     "⛔ Query `corpus/` before writing a new decoder — a question that used to "
     "cost a session now costs a `csv.DictReader`.",
     (r"census$", r"^replay_", r"_read$", r"^rdiff$", r"^bank_trace$", r"^peck_",
      r"^ring_", r"^kidnap_", r"^crash_", r"^throw", r"^camp_detect$",
      r"^collar_census$", r"^choke_census$", r"^dodge_capture$", r"^escape_",
      r"^field_deaths$", r"^nav_lock_census$", r"^border_defect_scan$",
      r"^turret_selfkill_census$", r"^wincond_backfill$", r"^core_entry$")),
    ("Statistics and power",
     "Design effects, MDE, effective n. ⛔ Games are NOT independent — see "
     "`CLAUDE.md` on DEFF before quoting any interval.",
     (r"^effective_n$", r"^mde$", r"^paired_vs_pooled$", r"^pair$", r"^score$",
      r"^slot_denoms$", r"^fixture_starvation$")),
    ("Maps and the engine",
     "Map generation, encoding, and engine-level probes.",
     (r"^make_map$", r"^map_", r"^cpu_lag_probe$", r"^tle_census$", r"^ceiling$",
      r"^loki\d", r"^rentgun_drive$", r"^fwd_read$")),
]


def docstring_head(path: Path) -> str:
    try:
        d = ast.get_docstring(ast.parse(path.read_text()))
    except (SyntaxError, OSError):
        return "*(does not parse)*"
    if not d:
        return "*(no docstring)*"
    for line in d.splitlines():
        if line.strip():
            return line.strip()
    return "*(empty docstring)*"


def mutates(path: Path) -> bool:
    """Over-inclusive on purpose: `read-only` must be trustworthy."""
    try:
        src = path.read_text()
    except OSError:
        return True
    return bool(re.search(
        r"open\([^)]*['\"][wa]|\.write_text\(|\.mkdir\(|shutil\.|os\.remove|"
        r"os\.unlink|subprocess\.(run|call|Popen)", src))


def classify(stem: str) -> int | None:
    for i, (_h, _b, pats) in enumerate(GROUPS):
        if any(re.search(p, stem) for p in pats):
            return i
    return None


def build() -> str:
    tools = sorted(TOOLS.glob("*.py"))
    buckets: dict[int | None, list[Path]] = {}
    for f in tools:
        if f.name in ("gen_index.py",):
            continue
        buckets.setdefault(classify(f.stem), []).append(f)

    out = [
        "# tools/ — INDEX",
        "",
        "**GENERATED by `tools/gen_index.py`. Do not edit by hand** — regenerate with",
        "`.venv/bin/python tools/gen_index.py`. A hand-edited index is a second source",
        "of truth, and this repo has measured that failure mode more than once",
        "(`docs/tooling.md` named 6 of 86 tools; a boot file bounded a 57k-line file",
        'at "41k lines" for days).',
        "",
        "**Every tool honours `--help`**: side-effect-free, prints its docstring, exits 0.",
        "Enforced by `tests/test_instruments.py::TestHelpContract`.",
        "",
        "`mutates` = a static scan found a write or a subprocess call. It is deliberately",
        "over-inclusive: **trust `read-only`, and check before running a `mutates` tool",
        "blind** — never the reverse.",
        "",
        "⭐ **If you only run one thing: `.venv/bin/python tools/now.py`** — what is live,",
        "what the control is, and how stale every state surface is.",
        "",
    ]
    for i, (head, blurb, _p) in enumerate(GROUPS):
        rows = buckets.get(i, [])
        if not rows:
            continue
        out += [f"## {head}", "", blurb, "",
                "| tool | | what it answers |", "| --- | --- | --- |"]
        for f in rows:
            flag = "✏️" if mutates(f) else "👁"
            out.append(f"| [`{f.name}`]({f.name}) | {flag} | {docstring_head(f)} |")
        out.append("")

    rest = buckets.get(None, [])
    if rest:
        out += ["## Unclassified", "",
                "⚠ **These matched no group pattern in `gen_index.py`.** That is a "
                "prompt, not an error: either the name does not say what the tool "
                "does, or `GROUPS` needs a pattern. Listed openly rather than filed "
                "somewhere plausible.", "",
                "| tool | | what it answers |", "| --- | --- | --- |"]
        for f in rest:
            flag = "✏️" if mutates(f) else "👁"
            out.append(f"| [`{f.name}`]({f.name}) | {flag} | {docstring_head(f)} |")
        out.append("")

    out += ["---", "",
            f"**{sum(len(v) for v in buckets.values())} tools indexed** "
            f"(👁 read-only, ✏️ writes or shells out). Subdirectories not covered here: "
            "`tools/monitors/` (daemons — see `fleet_health.py` for what should be "
            "running), `tools/corpus/` (corpus builders), `tools/dash/`, `tools/vps/`.",
            ""]
    return "\n".join(out)


def selftest() -> int:
    bad = 0

    def check(label, got, want):
        nonlocal bad
        ok = got == want
        bad += (not ok)
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<54} got={got} want={want}")

    check("classify routes a known gate", GROUPS[classify("gate")][0][:5], "Gates")
    check("classify routes a census to the corpus group",
          "corpus" in GROUPS[classify("crash_census")][0].lower(), True)
    check("an unmatched name is None, not silently bucketed",
          classify("zzz_nonexistent_tool"), None)
    body = build()
    # Count TABLE ROWS, not raw string occurrences: tool names also appear in
    # group blurbs (`now.py`, `gate.py`, `submit_clean.py`), so a naive count
    # double-counts. The first draft of this cell did exactly that and failed
    # on a correct index -- the assertion was wrong, not the generator.
    rows = [l for l in body.splitlines() if l.startswith("| [`")]
    listed = [l.split("`")[1] for l in rows]
    expect = sorted(f.name for f in TOOLS.glob("*.py") if f.name != "gen_index.py")
    check("every tool has exactly one table row", sorted(listed), expect)
    check("no tool is listed twice", len(listed), len(set(listed)))
    check("the index names now.py as the entry point", "tools/now.py" in body, True)
    print("\nPASS: routing works, unmatched names surface, no tool is listed twice."
          if not bad else f"\n*** {bad} case(s) wrong ***")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if INDEX.md differs from what would be generated")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    body = build()
    if a.check:
        cur = INDEX.read_text() if INDEX.exists() else ""
        if cur != body:
            print("STALE: tools/INDEX.md does not match the tree. "
                  "Run: .venv/bin/python tools/gen_index.py")
            return 1
        print("tools/INDEX.md is current.")
        return 0
    INDEX.write_text(body)
    print(f"wrote {INDEX} ({len(body.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
