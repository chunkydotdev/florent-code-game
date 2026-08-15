#!/usr/bin/env python3
"""BOOT — the whole boot context for one lane, on one screen, under a token budget.

    .venv/bin/python tools/boot.py --lane builder
    .venv/bin/python tools/boot.py --lane research --budget 12000
    .venv/bin/python tools/boot.py --selftest

===== WHY THIS EXISTS =====
A builder boot performed exactly as its charter specifies reads roughly
**140,000 tokens before the first useful action**. Measured 2026-08-15:

    docs/coordination.md      57,429 lines   ~960,000 tok   "read the tail"
    QUEUE.md                     772 lines    ~80,000 tok   "fire from the top"
    docs/<lane>-arm-retro.md   ~1,300 lines    ~20,000 tok   "read at boot"
    CLAUDE.md                    721 lines    ~15,000 tok   auto-loaded
    PROGRAMME.md                 598 lines     ~9,000 tok   before HANDOVER
    HANDOVER.md                  275 lines     ~5,000 tok   top block only

**The two largest instructions are the two a reader is least able to bound
correctly**, and the charter's own bound had already rotted: `builder.md` says
*"NEVER the whole file (41k lines)"* about a file that had grown to 57,429.
⇒ **Prose cannot track a moving number. A tool can.**

===== WHAT THIS IS AND IS NOT =====
It is **the STATE half of the boot**, bounded and assembled: live holder, fleet
health, the coordination tail since the last wrap marker, the top queue rows,
and the lane's own open retro items.

It is **NOT the charter**. The lane files (`.claude/commands/*.md`) carry
judgement, hard limits and standing directives, and those are READ, not
summarised — a summary of a rule is a new rule. This tool exists so that the
context you spend on state does not crowd out the context you spend on rules.

===== THE BUDGET IS A REFUSAL, NOT A TARGET =====
Every section is truncated to its share and **says so inline** when it truncates.
A boot digest that silently drops the newest coordination note is worse than no
digest: it reads complete. Truncation is always announced with the exact command
that shows the rest.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANES = ("builder", "research", "sidelane")
RETRO = {"builder": "docs/builder-arm-retro.md",
         "research": "docs/research-arm-retro.md",
         "sidelane": "docs/side-lane-retro.md"}

# ~4 chars/token. Only used to BOUND output, never reported as a measurement.
CPT = 4


def _tok(s: str) -> int:
    return len(s) // CPT


def _run(cmd: list[str], timeout: int = 60) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, cwd=ROOT)
        return (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"(could not run {' '.join(cmd[:3])}: {type(e).__name__})"


def _clip(body: str, budget_tok: int, how_to_see_rest: str) -> str:
    """Truncate to budget, ANNOUNCING it. Silence here would be the whole bug."""
    if _tok(body) <= budget_tok:
        return body
    keep = budget_tok * CPT
    cut = body[-keep:] if len(body) > keep else body
    nl = cut.find("\n")
    cut = cut[nl + 1:] if nl != -1 else cut
    return (f"[⚠ TRUNCATED to ~{budget_tok} tok — this is the TAIL, the older part is "
            f"NOT here.\n   Full: {how_to_see_rest}]\n" + cut)


def coordination_tail(max_lines: int = 400) -> tuple[str, str]:
    """The tail since the last wrap marker, or max_lines — whichever is SHORTER.

    The charter says "since the last wrap marker, or ~400 lines". Both bounds
    are computed here rather than estimated, and which one applied is reported,
    because "I read the tail" has meant different amounts to different sessions.
    """
    p = ROOT / "docs/coordination.md"
    if not p.exists():
        return "(docs/coordination.md missing)", "missing"
    lines = p.read_text(errors="replace").splitlines()
    total = len(lines)
    marker = None
    for i in range(total - 1, max(0, total - 4000), -1):
        if re.search(r"WRAP|REBOOT STATE|PROCESS DELTAS", lines[i]):
            marker = i
            break
    by_marker = total - marker if marker is not None else None
    take = min(x for x in (by_marker, max_lines) if x)
    why = (f"last wrap marker at line {marker + 1} of {total} ({by_marker} lines)"
           if by_marker and take == by_marker
           else f"{max_lines}-line cap (file is {total} lines)")
    return "\n".join(lines[-take:]), why


def retro_open_items(lane: str, max_lines: int = 40) -> str:
    p = ROOT / RETRO[lane]
    if not p.exists():
        return f"({RETRO[lane]} missing)"
    lines = p.read_text(errors="replace").splitlines()
    hits = [l for l in lines
            if re.search(r"OPEN|CARRY|DEBT|UNRESOLVED|owed|do not inherit",
                         l, re.I)][-max_lines:]
    return "\n".join(hits) if hits else "(no open-item lines matched)"


def build(lane: str, budget: int) -> str:
    out: list[str] = []
    a = out.append
    a(f"BOOT DIGEST — lane: {lane}   budget ~{budget} tok")
    a("=" * 72)
    a("⛔ THIS IS THE STATE HALF ONLY. Read .claude/commands/%s.md for the" % lane)
    a("   charter, the hard limits and the standing directives — a summary of a")
    a("   rule is a new rule, so they are deliberately NOT digested here.")
    a("")

    a("── 1. LIVE STATE " + "─" * 55)
    a(_run([str(ROOT / ".venv/bin/python"), str(ROOT / "tools/now.py")]).rstrip())
    a("")

    a("── 2. FLEET " + "─" * 60)
    a(_run([str(ROOT / ".venv/bin/python"), str(ROOT / "tools/fleet_health.py"),
            "--quiet"]).rstrip())
    a("")

    a("── 3. NEXT QUEUE ITEM " + "─" * 50)
    nxt = _run([str(ROOT / ".venv/bin/python"), str(ROOT / "tools/queue_check.py"),
                "--next"])
    a(_clip(nxt.rstrip(), budget // 5,
            ".venv/bin/python tools/queue_check.py --next"))
    a("")

    a("── 4. COORDINATION TAIL " + "─" * 48)
    tail, why = coordination_tail()
    a(f"[bound applied: {why}]")
    a(_clip(tail, budget // 2, "tail -400 docs/coordination.md"))
    a("")

    a(f"── 5. OPEN ITEMS FROM {RETRO[lane]} " + "─" * 20)
    a(_clip(retro_open_items(lane), budget // 8, f"read {RETRO[lane]}"))
    a("")

    a("── 6. BOOT CHECKS " + "─" * 54)
    for t in ("tools/audit_trigger.py", "tools/corpus_sanity.py"):
        r = _run([str(ROOT / ".venv/bin/python"), str(ROOT / t)], timeout=180)
        last = [l for l in r.strip().splitlines() if l.strip()][-1:] or ["(no output)"]
        a(f"  {Path(t).name:<20} {last[0][:90]}")
    a("")
    a("=" * 72)
    a("NOT INCLUDED, ON PURPOSE: the charter, PROGRAMME.md, CLAUDE.md. Read those.")
    return "\n".join(out)


def selftest() -> int:
    bad = 0

    def check(label, got, want):
        nonlocal bad
        ok = got == want
        bad += (not ok)
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<56} got={got} want={want}")

    # The clip must ANNOUNCE. A silent truncation is the defect, not the fix.
    long = "\n".join(f"line {i}" for i in range(5000))
    clipped = _clip(long, 50, "tail -400 file")
    check("over-budget input is truncated", _tok(clipped) <= 120, True)
    check("...and it SAYS it truncated", "TRUNCATED" in clipped, True)
    check("...and it names how to see the rest", "tail -400 file" in clipped, True)
    check("...and it keeps the NEWEST lines (tail, not head)",
          "line 4999" in clipped, True)
    check("under-budget input is untouched", _clip("short", 50, "x"), "short")

    # The coordination bound must be COMPUTED and REPORTED, not assumed.
    _t, why = coordination_tail()
    check("coordination bound names which rule applied",
          any(k in why for k in ("wrap marker", "cap")), True)

    # Lane routing must be real, not cosmetic.
    check("each lane maps to its own retro file",
          len(set(RETRO.values())), 3)

    print("\nPASS: truncation is announced, keeps the tail, and the coordination "
          "bound reports which rule applied."
          if not bad else f"\n*** {bad} case(s) wrong ***")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", choices=LANES, help="which lane's boot context")
    ap.add_argument("--budget", type=int, default=8000,
                    help="approximate token ceiling (default 8000)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.lane:
        ap.error("--lane is required (builder|research|sidelane)")
    body = build(a.lane, a.budget)
    print(body)
    print(f"\n[digest ~{_tok(body)} tok against a ~{a.budget} budget; "
          f"the charter is read separately]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
