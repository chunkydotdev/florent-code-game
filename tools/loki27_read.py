#!/usr/bin/env python3
"""LOKI-27 FERRY-FIRST READ-OUT — frozen BEFORE the control arm was fired.

⛔ WHY THE COMMIT TIME OF THIS FILE MATTERS.
When this was written the TREATMENT arm was decoded and known (INSERT 13,
EXILE 60 over 25 games, ratio 1:4.6) and the CONTROL arm had **not been fired**.
The pre-registered bars were already fixed (`PREREG-loki27-ferryfirst-2026-08-11.md`
Amendment 1) — but the ANALYSIS CODE was not, and it would otherwise have been
written by someone who knew one arm's answer. Freezing it here, running it
against the treatment arm alone to prove it executes, and committing it BEFORE
pointing it at the control, is the same discipline as the prereg itself applied
one layer down. (Side lane's ask, 2026-08-11.)

WHAT IT COMPUTES, AND THE THREE THINGS THAT ARE NOT OBVIOUS
-----------------------------------------------------------
1. **THE BAND IS COMPUTED FROM BOTH ARMS' REALIZED COUNTS, NEVER FROM A STORED
   RATE.** Amendment 1b quotes "≈ +59%" beside the rule; that figure was derived
   from the stored corpus 0.91 INSERT/game and is **ILLUSTRATIVE ONLY** — the
   side lane retracted it against the treatment's realized 0.52/game. **The RULE
   binds: ratio rises by >= 2 sd OF THE DIFFERENCE.** A threshold expressed as a
   fixed percentage silently inherits whatever rate produced it, which is the
   stored-comparator defect one layer up.

2. **THE ADMISSION DENOMINATOR IS REPORTED AND IS NOT 25.** Only games containing
   at least one throw can carry the mechanism. If that count is small in BOTH
   arms the verdict is INADMISSIBLE — the leg measured nothing — and that is a
   different outcome from a refutation.

3. **INSIDE THE BAND IS `NO INFORMATION`, NOT `DEAD`.** Pre-registered in
   Amendment 1b/1c. The original falsifier ("INSERT does not rise -> DEAD") was
   withdrawn because at this n it would write up a real +25% effect as a refuted
   mechanism.

Usage:
  loki27_read.py <arm_label> <match_id> [match_id ...]                  # one arm
  loki27_read.py --compare TREATLABEL=id,id,... CTRLLABEL=id,id,...     # verdict
"""
from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from collections import Counter
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
AR = ROOT / "replay_archive"
OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"


def arm_counts(mids):
    """Decode one arm. Returns (Counter of our throw kinds, n_games, n_games_with_throw)."""
    files, ourteam = [], {}
    for m in mids:
        meta = AR / f"{m}.meta.json"
        if not meta.exists():
            print(f"  MISSING META {m} — replay not archived yet", file=sys.stderr)
            continue
        d = json.loads(meta.read_text())
        ourteam[m] = 0 if d.get("teamAId") == OURS else 1
        files += sorted(str(p) for p in AR.glob(f"{m}_game_*.replay26"))
    if not files:
        return Counter(), 0, 0
    out = subprocess.run(
        [str(ROOT / ".venv/bin/python"), str(ROOT / "tools/corpus/replay_throws.py")] + files,
        capture_output=True, text=True)
    rows = list(csv.DictReader(out.stdout.splitlines(), delimiter="\t"))
    c = Counter()
    with_throw = set()
    for r in rows:
        mid = r["file"].split("_game_")[0]
        if mid not in ourteam:
            continue
        if int(r["tteam"]) == ourteam[mid]:
            c[r["kind"]] += 1
            with_throw.add(r["file"])
    return c, len(files), len(with_throw)


def report(label, c, n, nt):
    ins, ex = c["INSERT"], c["EXILE"]
    print(f"\n  {label}   n={n} games   ADMISSION: {nt} of {n} games carry any throw")
    print(f"     INSERT  {ins:>4}   {ins/max(n,1):.2f}/game")
    print(f"     EXILE   {ex:>4}   {ex/max(n,1):.2f}/game")
    print(f"     RETREAT {c['RETREAT']:>4}")
    r = ins / ex if ex else float("nan")
    print(f"     INSERT:EXILE ratio = {r:.4f}"
          + (f"  (1:{ex/ins:.1f})" if ins else "  (no inserts)"))
    return ins, ex, r


def compare(t, ctl):
    (tc, tn, tnt), (cc, cn, cnt) = t[1], ctl[1]
    ti, te, tr = report(t[0], tc, tn, tnt)
    ci, ce, cr = report(ctl[0], cc, cn, cnt)

    print("\n" + "=" * 68)
    # --- ADMISSION FIRST. A leg that carries no dose cannot refute anything. ---
    if ti + ci == 0:
        print("  LOKI27_VERDICT: INADMISSIBLE — zero INSERTs in BOTH arms; the "
              "precondition is absent and the leg measured nothing.")
        return
    if tnt < 5 or cnt < 5:
        print(f"  ⚠ THIN ADMISSION: {tnt} and {cnt} games carry a throw. The "
              f"mechanism's effective n is that, NOT {tn}/{cn}.")

    # --- BAND FROM BOTH ARMS' REALIZED COUNTS. No stored rate anywhere. ---
    # Relative sd of a ratio of two Poisson counts ~ sqrt(1/ins + 1/ex);
    # difference of two such ratios adds in quadrature.
    def relsd(i, e):
        return math.sqrt(1.0 / max(i, 1) + 1.0 / max(e, 1))
    sd_diff = math.sqrt((tr * relsd(ti, te)) ** 2 + (cr * relsd(ci, ce)) ** 2)
    diff = tr - cr
    band = 2 * sd_diff
    print(f"\n  ratio treat {tr:.4f}   ctrl {cr:.4f}   diff {diff:+.4f}")
    print(f"  sd(diff) = {sd_diff:.4f}   informative band = |diff| >= {band:.4f}"
          f"  ({band/cr*100:.0f}% of the control ratio)" if cr else "")
    print("  (band computed from BOTH arms' REALIZED counts — the '+59%' in "
          "Amendment 1b is illustrative only and inherits a stored rate)")

    if diff >= band:
        print("\n  LOKI27_VERDICT: MECHANISM CONFIRMED — INSERT:EXILE ratio rose "
              ">= 2 sd. The plank does what it says.")
    elif diff <= -band:
        print("\n  LOKI27_VERDICT: DEAD — ratio ran BACKWARDS >= 2 sd "
              "(the _v139heal outcome).")
    else:
        print("\n  LOKI27_VERDICT: NO INFORMATION — inside the band. Back to the "
              "POOL, NOT demoted. This is NOT a refutation.")
    print("=" * 68)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "--compare":
        arms = []
        for spec in a[1:]:
            lab, ids = spec.split("=", 1)
            arms.append((lab, arm_counts(ids.split(","))))
        compare(arms[0], arms[1])
    else:
        lab, mids = a[0], a[1:]
        c, n, nt = arm_counts(mids)
        report(lab, c, n, nt)
