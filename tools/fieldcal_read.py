#!/usr/bin/env python3
"""LEG-fieldcal-2026-08-16 READER — the registered read, and the refusal that guards it.

WHAT THIS IS. A re-runnable implementation of the estimators registered in
`docs/prereg/LEG-fieldcal-2026-08-16.md` (locked 2026-08-16T05:59:01Z) as amended
ADD-ONLY by `docs/prereg/AMENDMENT-LEG-fieldcal-catchup-2026-08-16.md`. It exists so
that the moment the leg crosses the CUT-SHORT floor the read is a RE-RUN, not a build.

⛔⛔ THE REFUSAL IS THE POINT, NOT A CAVEAT.
`§1 CUT-SHORT`, verbatim: "800 games total (40 games per arm in every surviving cell) is
the floor for any comparative claim. Below it: counts only, descriptive, no sign test, no
reversal claim."
⇒ Below 800 LEG-ARM games this tool emits NO (T-C) figure of any kind. Not greyed, not
parenthesised — ABSENT. Because a number printed with its warning elsewhere on the page
gets quoted without the warning, and the only qualifier that survives a copy-paste is one
on the SAME LINE as the number.

⛔ AND A CELL NEVER FIRES THE FALSIFIER, AT ANY n. The falsifier (§5) is registered over
the POOLED reading. A per-opponent cell is a DIFFERENT STATISTIC, not a small-n version of
the pooled one, so every per-cell line this tool prints carries its refusal INLINE and the
refusal is CATEGORICAL, never a precision argument. A precision phrasing invites "then at
what n would a cell count?", and for a cell the honest answer is NEVER.

REGISTERED DEFINITIONS IMPLEMENTED HERE, with the section that registers each:

  §1 ESTIMATOR / PRIMARY  exact two-sided binomial sign test over the pinned opponent
                          cells on sign(game_share_TREAT - game_share_CTRL); a cell scores
                          + iff treatment share STRICTLY exceeds control, - iff strictly
                          less, TIE iff exactly equal; ties EXCLUDED and the test recomputed
                          at the reduced k with the tie count reported.
  §1 ESTIMATOR / SECONDARY pooled ITT RMST at horizon 300 = the mean over ALL games of
                          min(turns, 300), "with any game not ending in our core-kill
                          scoring the full 300". Mean, not median. Boundary convention
                          `<300` (§1; checked identical to `<=300` in
                          RMST-ESTIMATOR-2026-08-16.md §3).
  §1 BAR                  >=9/10 cells share the sign => MEET (p = 0.0215); exactly 8/10 =>
                          UNRESOLVED (p = 0.1094); <=7/10 => MISS.
  §1 CUT-SHORT            leg floor 800 games; a cell that does not reach 40 games PER ARM
                          is EXCLUDED from the primary and NAMED WITH ITS COUNTS; the sign
                          test is recomputed at the surviving k. At k < 8 the primary is
                          UNRESOLVED and defaults to the restriction (§7).
  §1 CLUSTER UNIT         match+opponent (pooled) for the pooled reads; the PRIMARY takes NO
                          design effect — its unit of analysis IS the cluster (the cell).
  §3 DEFF OBLIGATION      every banked interval uses the leg's OWN re-measured design
                          effect, df-corrected, quoted beside the planning value.
  §5 FALSIFIER            pooled game share (T-C) <= -7.7pp, or pooled ITT RMST300 (T-C)
                          >= +10.1 rounds. -7.7pp is the 95% HALF-WIDTH AT 600 GAMES/ARM,
                          not a free-floating point threshold, and it is registered over the
                          POOLED reading only.
  §9.1 ARM IDENTITY       from engine-side / actor-side facts ONLY — never from our own
                          printed output, which the platform strips. Here: the scheduler's
                          consolidated accept ledger `scratchpad/arm_fieldcal_<arm>_<cell>.txt`
                          (written by `tools/fieldcal_scheduler.sh:invoke_runner`), CROSS-CHECKED
                          against the replay meta's `ourver` (A=140, B=154, scheduler :137-138).
  §9.3 PIN ASSERTION      for EVERY accepted match the decoded `oppver` must equal the
                          registered `theirver` for that cell. A mismatch VOIDS THAT CELL —
                          removed, k reduced, p recomputed. Not noted: removed.
  §9.5 ARCHIVE LAG        absence in the archive is NOT evidence; this tool reports the age
                          of the newest row it read and of the state tape, every run.

DATA SURFACES
  corpus/unrated_games.tsv        per-game decode of every archived NON-ladder match, outcome
                                  read off the replay binary (tools/corpus/unrated_games.py).
  scratchpad/fieldcal_state.tsv   the leg's state tape: ROUND, CLOCK2, per-(arm,cell) COUNT.
                                  ⛔ CITE THE STATE TAPE, NEVER scratchpad/fieldcal_scheduler.log
                                  — that log was TRUNCATED at 2026-08-16T07:40:13Z by a nohup
                                  relaunch using `>` instead of `>>`.
  scratchpad/arm_fieldcal_*.txt   per-(arm,cell) accept ledger: which match id belongs to which arm.

READ-ONLY. This tool opens files. It fires nothing, edits nothing, and never touches the
running scheduler.

Usage:
    .venv/bin/python tools/fieldcal_read.py
    .venv/bin/python tools/fieldcal_read.py --selftest      # the driven controls
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import glob
import math
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# REGISTERED CONSTANTS. Every one of these is frozen at lock (§13) and is
# transcribed here with the line that registers it. None is a tuning knob.
# ---------------------------------------------------------------------------
HORIZON = 300                     # §1 SECONDARY, §9.8 (no post-hoc horizon shopping)
CUT_SHORT_TOTAL = 800             # §1 CUT-SHORT: leg floor for ANY comparative claim
CUT_SHORT_PER_CELL_PER_ARM = 40   # §1 CUT-SHORT: cell admission
PLANNED_PER_ARM = 600             # §1 PLANNED n
MIN_K_FOR_PRIMARY = 8             # §1: at k < 8 the primary is UNRESOLVED
FALSIFIER_SHARE_PP = -7.7         # §5 (the 95% half-width at 600 games/arm)
FALSIFIER_RMST_ROUNDS = +10.1     # §5
PLANNING_DEFF_SHARE = 1.833       # §3 PLANNING value — appears in NO banked interval
PLANNING_DEFF_RMST = 1.42         # §3 PLANNING value — appears in NO banked interval

# §1 CELLS, in the registered order (also tools/fieldcal_scheduler.sh:105).
# label -> registered opponent version (`theirver`) for the §9.3 assertion.
CELLS: list[tuple[str, str]] = [
    ("Juusto", "13"),
    ("not_adgato", "23"),
    ("Erebus", "119"),
    ("kladde", "119"),
    ("gsxWins", "46"),
    ("0033", "57"),
    ("lingling_40h", "61"),
    ("HTTP_418", "103"),
    ("The_Bisons", "9"),
    ("farming_200s", "15"),
]
CELL_ORDER = [c for c, _ in CELLS]
THEIRVER = dict(CELLS)

# §2 THE ARMS / scheduler :137-138. A = control v140 (_v223sealrepair),
# B = treatment v154 (_v242bodyaware, BODYAWR).
ARM_VER = {"A": "140", "B": "154"}
ARM_ROLE = {"A": "CONTROL", "B": "TREATMENT"}

# The inline refusal strings. These travel ON THE SAME PHYSICAL LINE as every
# number they qualify, because a qualifier anywhere else detaches under copy-paste.
CELL_REFUSAL = ("— CELL, NOT THE POOLED STATISTIC: A CELL NEVER FIRES THE FALSIFIER, "
                "AT ANY n (§5 is registered over the POOLED reading) — NO COMPARATIVE CLAIM")
BELOW_FLOOR_TAG = "— BELOW CUT-SHORT FLOOR: NO COMPARATIVE CLAIM PERMITTED AT THIS n (§1)"


class Refusal(SystemExit):
    """A hard refusal. Raised, never warned — a warning gets scrolled past."""

    def __init__(self, msg: str):
        super().__init__("⛔ REFUSING: " + msg)


# ---------------------------------------------------------------------------
# LOADERS
# ---------------------------------------------------------------------------
REQUIRED_COLS = ("match", "game", "opp", "oppver", "ourver", "our_team",
                 "cond", "turns", "won", "createdAt")


def load_state_tape(path: str) -> dict:
    """CLOCK2, ROUND and the per-(arm,cell) accept COUNTs. §1 clock 2 is the
    platform createdAt of the FIRST ACCEPTED CHALLENGE of the leg."""
    if not os.path.exists(path):
        raise Refusal(f"no state tape at {path}; clock2 is unrecoverable and the leg era "
                      "cannot be delimited. The scheduler log is NOT a substitute — it was "
                      "truncated at 2026-08-16T07:40:13Z.")
    clock2, rnd = None, None
    counts: dict[tuple[str, str], int] = {}
    for line in open(path):
        f = line.rstrip("\n").split("\t")
        if not f or not f[0]:
            continue
        if f[0] == "CLOCK2" and len(f) > 1:
            clock2 = f[1].strip()
        elif f[0] == "ROUND" and len(f) > 1:
            rnd = f[1].strip()
        elif f[0] == "COUNT" and len(f) > 3:
            counts[(f[1], f[2])] = int(f[3])
    if not clock2:
        raise Refusal(f"{path} carries no CLOCK2 row; the leg era has no start boundary.")
    return {"clock2": clock2, "round": rnd, "counts": counts, "path": path,
            "mtime": os.path.getmtime(path)}


def load_arm_ledger(scratch: str) -> dict[str, tuple[str, str]]:
    """match id -> (arm, cell), read off the scheduler's consolidated accept files.

    §9.1: arm identity comes from engine-side / actor-side facts, never from our own
    stdout. §9.4.4: the outfile name IS the contract — `arm_fieldcal_<arm>_<cell>.txt`
    is what `invoke_runner` appends every accepted challenge to."""
    out: dict[str, tuple[str, str]] = {}
    pat = re.compile(r'"matchId":\s*"([0-9a-fA-F-]{36})"')
    for path in sorted(glob.glob(os.path.join(scratch, "arm_fieldcal_*.txt"))):
        base = os.path.basename(path)[len("arm_fieldcal_"):-len(".txt")]
        arm, _, cell = base.partition("_")
        if arm not in ARM_VER:
            raise Refusal(f"{base}: arm '{arm}' is not one of the registered arms {sorted(ARM_VER)}.")
        if cell not in THEIRVER:
            raise Refusal(f"{base}: cell '{cell}' is not in the registered §1 CELLS list.")
        for mid in pat.findall(open(path, errors="replace").read()):
            prev = out.get(mid)
            if prev and prev != (arm, cell):
                raise Refusal(f"match {mid} appears under BOTH {prev} and {(arm, cell)} in the "
                              "accept ledger — arm identity is ambiguous, which is an "
                              "instrument alarm, not a rounding problem.")
            out[mid] = (arm, cell)
    return out


def load_games(path: str) -> list[dict]:
    if not os.path.exists(path):
        raise Refusal(f"no game surface at {path}.")
    with open(path, newline="") as fh:
        rdr = csv.DictReader(fh, delimiter="\t")
        missing = [c for c in REQUIRED_COLS if c not in (rdr.fieldnames or [])]
        if missing:
            raise Refusal(f"{path} is missing required column(s) {missing}. The registered "
                          "estimators are not computable on this surface and a substitute "
                          "column is not a registered definition.")
        return list(rdr)


def parse_turns(row: dict, where: str) -> int:
    """⛔ A corrupt or absent `turns` is a REFUSAL, never a 0 and never a silent drop.
    A dropped row changes the ITT denominator; a 0 scores a phantom instant kill. Both
    move the registered secondary in the FLATTERING direction for a fast arm."""
    raw = (row.get("turns") or "").strip()
    if not raw.lstrip("+-").isdigit():
        raise Refusal(f"{where}: `turns` is {raw!r}, not an integer. ITT RMST{HORIZON} is a "
                      "mean over ALL games — a row that cannot be scored cannot be dropped "
                      "without moving the denominator, and cannot be zeroed without inventing "
                      "an instant kill.")
    t = int(raw)
    if t <= 0:
        raise Refusal(f"{where}: `turns` = {t}; a game cannot last <= 0 rounds.")
    return t


# ---------------------------------------------------------------------------
# THE REGISTERED ESTIMATORS
# ---------------------------------------------------------------------------
def our_core_kill(row: dict) -> bool:
    """§1 SECONDARY's own wording: a game "ending in OUR core-kill". That is BOTH
    cond == core_destroyed AND won == 1. A game the OPPONENT ends by killing OUR core
    is NOT our core-kill and scores the full horizon.
    ⚠ See the read-out's DEFINITION FLAG: the looser reading ("any core kill") is a
    materially different estimator, and this tool implements the registered one."""
    return row["cond"] == "core_destroyed" and str(row["won"]).strip() == "1"


def rmst_score(row: dict, where: str) -> int:
    """§1 SECONDARY: min(turns, H), with any game not ending in our core-kill scoring
    the full H. Boundary convention `<H` (identical to `<=H` under min(), and checked
    identical to 2dp on every local arm — RMST-ESTIMATOR-2026-08-16.md §3)."""
    t = parse_turns(row, where)
    if not our_core_kill(row):
        return HORIZON
    return min(t, HORIZON)


def rmst_score_loose(row: dict, where: str) -> int:
    """DEFINITION-SENSITIVITY COLUMN ONLY — the reading in which any game ending in a
    core kill (either team's) contributes min(turns, H). NOT the registered estimator.
    Printed so the size of the disagreement is visible rather than argued about."""
    t = parse_turns(row, where)
    if row["cond"] != "core_destroyed":
        return HORIZON
    return min(t, HORIZON)


def game_share(rows: list[dict]) -> float | None:
    """§1 PRIMARY's per-cell quantity and §6 row 4's pooled one: games won / games played.
    (The ladder pays game share, not match wins — CLAUDE.md.)"""
    if not rows:
        return None
    return sum(1 for r in rows if str(r["won"]).strip() == "1") / len(rows)


def binom_two_sided_p(k_pos: int, n: int) -> float:
    """Exact two-sided binomial p at pi = 0.5 (§4's own table: 10/10 0.0020,
    9/10 0.0215, 8/10 0.1094)."""
    if n == 0:
        return float("nan")
    obs = abs(k_pos - n / 2)
    tot = 0.0
    for i in range(n + 1):
        if abs(i - n / 2) >= obs - 1e-12:
            tot += math.comb(n, i)
    return tot / (2 ** n)


def deff_df_corrected(cluster_values: list[list[float]], binomial: bool) -> dict | None:
    """§3's re-measurement obligation, df-corrected (the uncorrected form is biased LOW).

    Method, the repo's own: DEFF = (observed sd of the cluster means)^2 divided by the
    sd those means would have under independence. For a binary outcome the independent
    reference is p̄(1-p̄)/m; for a continuous one it is the pooled within-cluster
    variance / m. df = k - 1 on the between term.
    Returns None (never a number) when there are too few clusters to estimate it.
    """
    clusters = [c for c in cluster_values if len(c) > 0]
    k = len(clusters)
    if k < 3:
        return None
    sizes = {len(c) for c in clusters}
    m = sum(len(c) for c in clusters) / k
    means = [sum(c) / len(c) for c in clusters]
    gmean = sum(sum(c) for c in clusters) / sum(len(c) for c in clusters)
    var_obs = sum((x - gmean) ** 2 for x in means) / (k - 1)      # df correction
    if binomial:
        var_ind = gmean * (1 - gmean) / m
    else:
        within = sum(sum((x - mu) ** 2 for x in c)
                     for c, mu in zip(clusters, means))
        dfw = sum(len(c) for c in clusters) - k
        if dfw <= 0:
            return None
        var_ind = (within / dfw) / m
    if var_ind <= 0:
        return None
    deff = var_obs / var_ind
    rho = (deff - 1) / (m - 1) if m > 1 else float("nan")
    return {"deff": deff, "rho": rho, "k": k, "m": m, "equal_sizes": len(sizes) == 1}


# ---------------------------------------------------------------------------
# THE READ
# ---------------------------------------------------------------------------
def build(games: list[dict], ledger: dict[str, tuple[str, str]], state: dict) -> dict:
    clock2 = state["clock2"]
    leg_era = [r for r in games if r["createdAt"] >= clock2]

    by_arm_cell: dict[tuple[str, str], list[dict]] = defaultdict(list)
    unledgered: list[dict] = []
    arm_alarms: list[str] = []
    pin_alarms: dict[str, list[str]] = defaultdict(list)

    for r in leg_era:
        hit = ledger.get(r["match"])
        if hit is None:
            unledgered.append(r)
            continue
        arm, cell = hit
        # CROSS-CHECK, not a second identifier: the ledger says which arm fired the
        # challenge; the replay meta says which of our versions actually played. If
        # those disagree the arm assignment is not trustworthy (§9.1/§9.2).
        if r["ourver"] != ARM_VER[arm]:
            arm_alarms.append(f"{r['match']} game {r['game']}: ledger says arm {arm} "
                              f"(v{ARM_VER[arm]}) but the replay meta says ourver="
                              f"v{r['ourver']}")
        # §9.3: the decoded oppver must equal the registered theirver for that cell.
        if r["oppver"] != THEIRVER[cell]:
            pin_alarms[cell].append(f"{r['match']}: oppver=v{r['oppver']} vs registered "
                                    f"theirver=v{THEIRVER[cell]}")
        by_arm_cell[(arm, cell)].append(r)

    # §9.3 voiding: a cell with ANY pin mismatch is REMOVED, not noted.
    voided = sorted(pin_alarms)
    live_cells = [c for c in CELL_ORDER if c not in voided]

    cell_stats = {}
    for cell in CELL_ORDER:
        entry = {"voided": cell in voided, "arms": {}}
        for arm in ("A", "B"):
            rows = by_arm_cell.get((arm, cell), [])
            where = f"cell {cell} arm {arm}"
            entry["arms"][arm] = {
                "n": len(rows),
                "accepts": len({r["match"] for r in rows}),
                "share": game_share(rows),
                "rmst": (sum(rmst_score(r, where) for r in rows) / len(rows)) if rows else None,
                "rmst_loose": (sum(rmst_score_loose(r, where) for r in rows) / len(rows)) if rows else None,
                "our_kills": sum(1 for r in rows if our_core_kill(r)),
                "kills_by_h": sum(1 for r in rows if our_core_kill(r)
                                  and parse_turns(r, where) < HORIZON),
                "opp_names": sorted({r["opp"] for r in rows}),
                "oppvers": sorted({r["oppver"] for r in rows}),
                "seats": {s: sum(1 for r in rows if r["our_team"] == s) for s in ("A", "B")},
                "rows": rows,
            }
        entry["min_per_arm"] = min(entry["arms"]["A"]["n"], entry["arms"]["B"]["n"])
        # §1 CUT-SHORT cell admission
        entry["admitted"] = (not entry["voided"]
                             and entry["min_per_arm"] >= CUT_SHORT_PER_CELL_PER_ARM)
        cell_stats[cell] = entry

    pooled = {}
    for arm in ("A", "B"):
        rows = [r for c in CELL_ORDER for r in by_arm_cell.get((arm, c), [])]
        where = f"pooled arm {arm}"
        pooled[arm] = {
            "n": len(rows),
            "accepts": len({r["match"] for r in rows}),
            "share": game_share(rows),
            "rmst": (sum(rmst_score(r, where) for r in rows) / len(rows)) if rows else None,
            "rmst_loose": (sum(rmst_score_loose(r, where) for r in rows) / len(rows)) if rows else None,
            "our_kills": sum(1 for r in rows if our_core_kill(r)),
            "kills_by_h": sum(1 for r in rows if our_core_kill(r)
                              and parse_turns(r, where) < HORIZON),
            "nonkill": sum(1 for r in rows if not our_core_kill(r)),
            "rows": rows,
        }

    total = pooled["A"]["n"] + pooled["B"]["n"]
    return {
        "clock2": clock2, "state": state, "leg_era_rows": len(leg_era),
        "unledgered": unledgered, "arm_alarms": arm_alarms, "pin_alarms": dict(pin_alarms),
        "voided": voided, "live_cells": live_cells, "cells": cell_stats,
        "pooled": pooled, "total": total,
        "above_floor": total >= CUT_SHORT_TOTAL,
        "newest_row": max((r["createdAt"] for r in games), default=None),
    }


def remeasure_deff(res: dict) -> dict:
    """§3: re-measure BOTH clusters on the leg's OWN games, df-corrected."""
    out = {}
    for arm in ("A", "B"):
        rows = res["pooled"][arm]["rows"]
        by_match: dict[str, list[dict]] = defaultdict(list)
        for r in rows:
            by_match[r["match"]].append(r)
        share_clusters = [[1.0 if str(r["won"]).strip() == "1" else 0.0 for r in v]
                          for v in by_match.values()]
        rmst_clusters = [[float(rmst_score(r, "deff")) for r in v] for v in by_match.values()]
        out[arm] = {
            "share_match": deff_df_corrected(share_clusters, binomial=True),
            "rmst_match": deff_df_corrected(rmst_clusters, binomial=False),
        }
    return out


def sign_test(res: dict) -> dict:
    """§1 PRIMARY. Only ever called above the CUT-SHORT floor."""
    plus = minus = tie = 0
    detail = []
    for cell in CELL_ORDER:
        e = res["cells"][cell]
        if not e["admitted"]:
            continue
        a, b = e["arms"]["A"]["share"], e["arms"]["B"]["share"]
        if b > a:
            plus += 1; s = "+"
        elif b < a:
            minus += 1; s = "-"
        else:
            tie += 1; s = "TIE"
        detail.append((cell, s, a, b))
    k = plus + minus                     # §1: ties EXCLUDED, recompute at reduced k
    top = max(plus, minus)
    p = binom_two_sided_p(top, k) if k else float("nan")
    if k < MIN_K_FOR_PRIMARY:
        verdict = f"UNRESOLVED — k={k} < {MIN_K_FOR_PRIMARY}; defaults to the RESTRICTION (§1, §7)"
    elif top >= 9:
        verdict = f"MEET (p={p:.4f}) — direction {'+ (treatment)' if plus > minus else '- (control)'}"
    elif top == 8:
        verdict = f"UNRESOLVED (p={p:.4f}) — §7: no directional claim in either direction"
    else:
        verdict = (f"MISS on the primary (p={p:.4f}) — the EXPECTED outcome; §1's "
                   "IMPOTENCE CLAUSE governs and this is not a refutation")
    return {"plus": plus, "minus": minus, "tie": tie, "k": k, "p": p,
            "verdict": verdict, "detail": detail}


def pct(x, nd=1):
    return "  n/a " if x is None else f"{100 * x:{4 + nd}.{nd}f}%"


def rnd(x, nd=2):
    return "   n/a" if x is None else f"{x:6.{nd}f}"


def render(res: dict, out=sys.stdout) -> None:
    w = lambda s="": print(s, file=out)
    now = _dt.datetime.now(_dt.timezone.utc)
    st = res["state"]

    w("=" * 108)
    w("LEG-fieldcal-2026-08-16 — REGISTERED READ")
    w("=" * 108)
    # §9.5: a monitor that reads a file reports that file's FRESHNESS or refuses a verdict.
    tape_age = (now - _dt.datetime.fromtimestamp(st["mtime"], _dt.timezone.utc)).total_seconds() / 60
    w(f"read at            {now.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    w(f"clock2 (§1)        {res['clock2']}  — leg era = createdAt >= clock2")
    w(f"state tape         {st['path']}  ROUND={st['round']}  age {tape_age:.1f} min")
    w(f"newest corpus row  {res['newest_row']}   ⚠ §9.5 THE ARCHIVE LAGS — absence is NOT evidence")
    w(f"arm identity       ledger scratchpad/arm_fieldcal_<arm>_<cell>.txt (§9.1/§9.4.4), "
      f"cross-checked vs replay-meta ourver (A=v140 CONTROL, B=v154 TREATMENT)")
    w("")

    # ---- instrument alarms first: a read printed above its own alarms gets quoted alone.
    w("-- INSTRUMENT CHECKS " + "-" * 87)
    w(f"  arm cross-check (ledger arm vs replay ourver)   "
      f"{'CLEAN' if not res['arm_alarms'] else 'ALARM — ' + str(len(res['arm_alarms'])) + ' row(s)'}")
    for a in res["arm_alarms"][:5]:
        w(f"      ⛔ {a}")
    w(f"  §9.3 pin assertion (decoded oppver == theirver) "
      f"{'CLEAN on every accepted match' if not res['pin_alarms'] else 'VOIDING ' + str(len(res['pin_alarms'])) + ' cell(s)'}")
    for cell, msgs in res["pin_alarms"].items():
        w(f"      ⛔ CELL {cell} VOIDED (§9.3: removed, not noted) — {msgs[0]}")
    other = defaultdict(int)
    for r in res["unledgered"]:
        other[(r["ourver"], r["opp"])] += 1
    w(f"  leg-era rows NOT in this leg's accept ledger    {len(res['unledgered'])} game(s) "
      f"— excluded from every number below")
    for (v, opp), n in sorted(other.items(), key=lambda kv: -kv[1]):
        w(f"      · ourver=v{v} vs {opp}: {n} games (not a leg arm and/or not our challenge)")
    w("")

    # ---- the floor
    w("-- CUT-SHORT FLOOR (§1) " + "-" * 84)
    if not res["above_floor"]:
        w(f"  ⛔ BELOW CUT-SHORT FLOOR: {res['total']}/{CUT_SHORT_TOTAL} — NO COMPARATIVE CLAIM "
          f"PERMITTED AT THIS n (prereg §1)")
        w(f"     §1 verbatim: \"800 games total (40 games per arm in every surviving cell) is the")
        w(f"     floor for any comparative claim. Below it: counts only, descriptive, no sign")
        w(f"     test, no reversal claim.\"")
        w(f"     ⇒ NO (T−C) figure is emitted anywhere below. Not greyed, not parenthesised: ABSENT.")
        nadm = sum(1 for c in CELL_ORDER if res["cells"][c]["admitted"])
        w(f"     ⚠ TWO CONDITIONS, NOT ONE: {res['total']}/{CUT_SHORT_TOTAL} games AND "
          f"{nadm}/{MIN_K_FOR_PRIMARY} cells at >={CUT_SHORT_PER_CELL_PER_ARM} games/arm. Crossing 800")
        w(f"       does NOT by itself resolve the primary — at k < {MIN_K_FOR_PRIMARY} admitted cells "
          f"it is UNRESOLVED and defaults to the restriction (§1, §7).")
    else:
        w(f"  ✅ CUT-SHORT floor CLEARED: {res['total']}/{CUT_SHORT_TOTAL} leg-arm games. "
          f"Comparative statistics ENABLED.")
    w("")

    # ---- per-arm descriptive (never a difference)
    w("-- PER-ARM DESCRIPTIVE " + "-" * 85)
    for arm in ("A", "B"):
        p = res["pooled"][arm]
        tag = BELOW_FLOOR_TAG if not res["above_floor"] else ""
        w(f"  ARM {arm} {ARM_ROLE[arm]:9s} v{ARM_VER[arm]}  n={p['n']:4d} games / {p['accepts']:3d} accepts   "
          f"share {pct(p['share'])}   ITT RMST{HORIZON} {rnd(p['rmst'])}   "
          f"our-core-kills {p['our_kills']:3d} (by r{HORIZON}: {p['kills_by_h']:3d})  {tag}")
    w(f"  ITT denominator check: every game scores exactly once; non-our-kill scores {HORIZON} "
      f"(A {res['pooled']['A']['nonkill']} such games, B {res['pooled']['B']['nonkill']}).")
    w("")

    # ---- per-cell, every line carrying its own refusal
    w("-- PER-CELL FILL AND DESCRIPTIVE (§1 CELLS order) " + "-" * 58)
    for cell in CELL_ORDER:
        e = res["cells"][cell]
        a, b = e["arms"]["A"], e["arms"]["B"]
        if e["voided"]:
            w(f"  {cell:14s} ⛔ VOIDED by §9.3 (pin mismatch) — removed from the primary, k reduced")
            continue
        if a["n"] == 0 and b["n"] == 0:
            w(f"  {cell:14s} UNFIRED — 0 games either arm  {CELL_REFUSAL}")
            continue
        adm = "ADMITTED" if e["admitted"] else \
              f"EXCLUDED from the primary (§1 CUT-SHORT: min {e['min_per_arm']} < {CUT_SHORT_PER_CELL_PER_ARM}/arm)"
        w(f"  {cell:14s} A {pct(a['share'])} ({a['n']:3d}g) RMST {rnd(a['rmst'])} | "
          f"B {pct(b['share'])} ({b['n']:3d}g) RMST {rnd(b['rmst'])} | {adm}  {CELL_REFUSAL}")
    w("")

    # ---- imbalance, §6.2: one heading, all axes
    w("-- §6.2 IMBALANCE, ONE HEADING, ALL AXES (disclose, do not correct) " + "-" * 40)
    for arm in ("A", "B"):
        seats = defaultdict(int)
        for r in res["pooled"][arm]["rows"]:
            seats[r["our_team"]] += 1
        w(f"  seat        arm {arm}: " + ", ".join(f"{k}={v}" for k, v in sorted(seats.items())))
    fills = ", ".join(f"{c}:{res['cells'][c]['arms']['A']['accepts']}/"
                      f"{res['cells'][c]['arms']['B']['accepts']}" for c in CELL_ORDER)
    w(f"  accepts A/B per cell: {fills}")
    w(f"  pin age / churn: §1 names Erebus (10) and kladde (17) HIGH-CHURN — REPORTABLE, "
      f"NOT POOLABLE into any relevance claim; farming_200s' pin was ~16h old at lock.")
    w("")

    # ---- DEFF, descriptive at this n
    w("-- §3 DEFF RE-MEASUREMENT ON THE LEG'S OWN GAMES (df-corrected) " + "-" * 44)
    d = remeasure_deff(res)
    for arm in ("A", "B"):
        for key, label, plan in (("share_match", "game share / MATCH cluster", PLANNING_DEFF_SHARE),
                                 ("rmst_match", f"RMST{HORIZON} / MATCH cluster", PLANNING_DEFF_RMST)):
            v = d[arm][key]
            tag = "" if res["above_floor"] else "  — PROVISIONAL, USED IN NO INTERVAL AT THIS n"
            if v is None:
                w(f"  arm {arm} {label:28s} not estimable (too few clusters){tag}")
            else:
                w(f"  arm {arm} {label:28s} DEFF {v['deff']:.3f} (rho {v['rho']:+.4f}, "
                  f"k={v['k']} clusters, m={v['m']:.1f})  vs PLANNING {plan}{tag}")
    w("  ⛔ §3: planning DEFFs (1.833 share / 1.42 RMST) appear in NO banked interval; the "
      "leg's own re-measured value does.")
    w("")

    # ---- the comparative block: emitted ONLY above the floor
    w("-- PRIMARY / SECONDARY / FALSIFIER " + "-" * 73)
    if not res["above_floor"]:
        w(f"  ⛔ NOT COMPUTED. below CUT-SHORT floor: {res['total']}/{CUT_SHORT_TOTAL} — no sign "
          f"test, no pooled (T−C), no reversal claim (§1).")
        w("  ⛔ The falsifier (§5) is NOT evaluated and its thresholds are NOT printed beside any "
          "number on this page: −7.7pp is the 95% HALF-WIDTH AT 600 GAMES/ARM over the POOLED")
        w("     reading, so placing it next to a below-floor or per-cell figure would invite a "
          "comparison the registration does not license.")
    else:
        st_ = sign_test(res)
        w(f"  PRIMARY (§1, §4) sign test over admitted cells: + {st_['plus']}  − {st_['minus']}  "
          f"TIE {st_['tie']} (excluded, k reduced)  k={st_['k']}")
        for cell, s, a, b in st_["detail"]:
            w(f"      {cell:14s} {s:3s}  A {pct(a)}  B {pct(b)}")
        w(f"  PRIMARY VERDICT: {st_['verdict']}")
        w("")
        dshare = res["pooled"]["B"]["share"] - res["pooled"]["A"]["share"]
        drmst = res["pooled"]["B"]["rmst"] - res["pooled"]["A"]["rmst"]
        dv = remeasure_deff(res)
        w(f"  SECONDARY (§1) pooled ITT RMST{HORIZON} (T−C) = {drmst:+.2f} rounds "
          f"[A {res['pooled']['A']['rmst']:.2f}, B {res['pooled']['B']['rmst']:.2f}]")
        w(f"  DESCRIPTIVE (§6 row 4, §6.1) pooled game share (T−C) = {100 * dshare:+.2f} pp "
          f"— DESCRIPTIVE ONLY, no bar, no verdict, no ship input")
        w(f"  FALSIFIER (§5) evaluation, POOLED reading only:")
        w(f"      game share  (T−C) {100 * dshare:+.2f} pp  vs registered <= {FALSIFIER_SHARE_PP} pp"
          f"  ⇒ {'FIRED' if 100 * dshare <= FALSIFIER_SHARE_PP else 'not fired'}")
        w(f"      RMST{HORIZON}    (T−C) {drmst:+.2f} rounds vs registered >= "
          f"+{FALSIFIER_RMST_ROUNDS} rounds ⇒ "
          f"{'FIRED' if drmst >= FALSIFIER_RMST_ROUNDS else 'not fired'}")
        w(f"      ⚠ the registered thresholds are the 95% HALF-WIDTHS AT {PLANNED_PER_ARM} GAMES/ARM; "
          f"this read has A={res['pooled']['A']['n']} / B={res['pooled']['B']['n']} games/arm.")
        w(f"      ⚠ §3 DIRECTION RULE: a NON-reversal is a fail-to-exclude and is banked as "
          f"\"the leg excludes reversals larger than X\" using the leg's OWN re-measured DEFF")
        w(f"        (share {dv['B']['share_match']['deff']:.3f} / "
          f"{dv['A']['share_match']['deff']:.3f}), never as \"the local finding is confirmed\".")
    w("")
    w("-- DEFINITION FLAG " + "-" * 89)
    la, lb = res["pooled"]["A"]["rmst_loose"], res["pooled"]["B"]["rmst_loose"]
    ra, rb = res["pooled"]["A"]["rmst"], res["pooled"]["B"]["rmst"]
    w("  §1 registers RMST as \"min(turns,300) with any game NOT ENDING IN OUR CORE-KILL scoring")
    w("  the full 300\" — implemented here. A looser reading (\"any core kill, either team's\")")
    if None not in (la, lb, ra, rb):
        tag = BELOW_FLOOR_TAG if not res["above_floor"] else ""
        w(f"  gives per-arm A {la:.2f} / B {lb:.2f} against the registered A {ra:.2f} / B {rb:.2f}"
          f"  {tag}")
        w(f"  ⇒ the clause moves the LEVEL of each arm by ~{abs(ra - la):.0f} rounds. The §5 falsifier "
          f"is a +{FALSIFIER_RMST_ROUNDS}-round threshold, so an estimator whose level moves that far")
        w("     under a PARAPHRASE is a live hazard at the 800 boundary. No difference is computed "
          "here — the point is about the instrument, not about this leg's result.")
    w("  The two are DIFFERENT ESTIMATORS. Only the registered one is the secondary.")
    w("=" * 108)


# ---------------------------------------------------------------------------
# SELFTEST — the driven controls. A guard that has only ever returned one
# verdict has not been seen to guard, so every guard is driven BOTH ways.
# ---------------------------------------------------------------------------
def _row(match, game, opp, oppver, ourver, cond, turns, won, seat="A",
         created="2026-08-16T07:00:00.000Z"):
    return {"file": f"{match}_game_{game}.replay26", "match": match, "game": str(game),
            "opp": opp, "oppver": oppver, "ourver": ourver, "our_team": seat,
            "map_w": "20", "map_h": "20", "cond": cond, "turns": str(turns),
            "won": str(won), "createdAt": created, "trigger": "unrated"}


def _synth(per_arm_per_cell: int, cells: list[str]):
    """A synthetic leg: `per_arm_per_cell` games for each arm in each named cell."""
    games, ledger = [], {}
    mid = 0
    for cell in cells:
        for arm in ("A", "B"):
            done = 0
            while done < per_arm_per_cell:
                mid += 1
                m = f"{mid:08d}-0000-0000-0000-000000000000"
                ledger[m] = (arm, cell)
                for g in range(1, 6):
                    if done >= per_arm_per_cell:
                        break
                    done += 1
                    # deterministic, mildly different arms so signs are non-degenerate
                    won = 1 if (done + (arm == "B")) % 2 == 0 else 0
                    turns = 150 + (done % 7) * 20 + (10 if arm == "B" else 0)
                    games.append(_row(m, g, cell, THEIRVER[cell], ARM_VER[arm],
                                      "core_destroyed", turns, won))
    return games, ledger


def _capture(res) -> str:
    import io
    buf = io.StringIO()
    render(res, out=buf)
    return buf.getvalue()


def selftest() -> int:
    state = {"clock2": "2026-08-16T06:00:00.000Z", "round": "T", "counts": {},
             "path": "<selftest>", "mtime": _dt.datetime.now().timestamp()}
    fails = []

    def check(name, expected, observed, ok):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         expected: {expected}\n"
              f"         observed: {observed}")
        if not ok:
            fails.append(name)

    print("DRIVEN CONTROLS — every guard driven to BOTH verdicts")

    # (c) RMST unit check on hand-computable rows.
    rows = [_row("m", 1, "Juusto", "13", "140", "core_destroyed", 100, 1),
            _row("m", 2, "Juusto", "13", "140", "core_destroyed", 400, 1),
            _row("m", 3, "Juusto", "13", "140", "core_destroyed", 300, 1)]
    scores = [rmst_score(r, "unit") for r in rows]
    mean = sum(scores) / 3
    check("RMST300 unit: turns 100/400/300 (all OUR kills)",
          "scores [100, 300, 300], mean 233.33",
          f"scores {scores}, mean {mean:.2f}",
          scores == [100, 300, 300] and abs(mean - 233.3333) < 1e-3)

    # (c2) the registered "our core-kill" clause, driven the other way.
    loss = _row("m", 4, "Juusto", "13", "140", "core_destroyed", 120, 0)
    check("RMST300 registered clause: a game the OPPONENT ends at turn 120",
          "300 (not our core-kill ⇒ full horizon), and the LOOSE reading gives 120",
          f"registered {rmst_score(loss,'u')}, loose {rmst_score_loose(loss,'u')}",
          rmst_score(loss, "u") == 300 and rmst_score_loose(loss, "u") == 120)

    # (d) corrupt / absent turns must REFUSE, not zero and not drop.
    for bad, label in ((("", "absent")), (("N/A", "corrupt")), (("0", "zero"))):
        r = _row("m", 5, "Juusto", "13", "140", "core_destroyed", bad, 1)
        try:
            rmst_score(r, "unit")
            got, ok = "returned a number", False
        except Refusal as e:
            got, ok = "Refusal raised", True
        check(f"corrupt `turns` ({label}={bad!r}) is REFUSED", "Refusal raised", got, ok)
    r_ok = _row("m", 6, "Juusto", "13", "140", "core_destroyed", 210, 1)
    check("...and a VALID `turns` is NOT refused (the guard's other verdict)",
          "210 scored, no refusal", f"{rmst_score(r_ok,'u')} scored", rmst_score(r_ok, "u") == 210)

    # (d2) a missing required column must REFUSE.
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False) as fh:
        fh.write("match\tgame\topp\n1\t1\tx\n")
        tmp = fh.name
    try:
        load_games(tmp); got, ok = "loaded", False
    except Refusal:
        got, ok = "Refusal raised", True
    check("a surface missing the `turns` column is REFUSED", "Refusal raised", got, ok)
    os.unlink(tmp)

    # (a) the floor refusal FIRES below 800.
    g, led = _synth(20, CELL_ORDER)                       # 20/arm/cell x 10 = 400 total
    res = build(g, led, state)
    out = _capture(res)
    ok = (not res["above_floor"] and "BELOW CUT-SHORT FLOOR: 400/800" in out
          and "NOT COMPUTED" in out and "(T−C)" not in out.split("DEFINITION FLAG")[0]
          .split("-- PRIMARY")[1] .replace("no pooled (T−C)", ""))
    check("(a) floor refusal FIRES at n=400 and NO (T−C) figure is emitted",
          "refusal printed, primary/secondary/falsifier NOT COMPUTED, no (T−C) value",
          f"above_floor={res['above_floor']}, refusal={'BELOW CUT-SHORT FLOOR: 400/800' in out}, "
          f"not-computed={'NOT COMPUTED' in out}", ok)

    # (b) the floor refusal DOES NOT fire at n >= 800; comparison emitted WITHOUT it.
    g, led = _synth(60, CELL_ORDER)                       # 60/arm/cell x 10 = 1200 total
    res2 = build(g, led, state)
    out2 = _capture(res2)
    pooled_block = out2.split("-- PRIMARY / SECONDARY / FALSIFIER")[1].split("-- DEFINITION FLAG")[0]
    pooled_lines = [l for l in pooled_block.splitlines()
                    if "pooled ITT RMST" in l or "pooled game share" in l]
    ok = (res2["above_floor"] and "CUT-SHORT floor CLEARED: 1200/800" in out2
          and "PRIMARY VERDICT" in out2 and len(pooled_lines) == 2
          and all("NO COMPARATIVE CLAIM" not in l and "BELOW CUT-SHORT" not in l
                  for l in pooled_lines))
    check("(b) at n=1200 the pooled comparison is EMITTED and carries NO refusal string",
          "floor cleared, sign test run, pooled (T−C) lines present and clean",
          f"above_floor={res2['above_floor']}, pooled lines={len(pooled_lines)}, "
          f"clean={all('NO COMPARATIVE CLAIM' not in l for l in pooled_lines)}", ok)

    # (c) THE CATEGORICAL CELL RULE: per-cell lines STILL carry the refusal at n>=600/arm.
    cell_lines = [l for l in out2.splitlines()
                  if l.strip().startswith(tuple(CELL_ORDER)) and "|" in l]
    ok = len(cell_lines) == 10 and all(CELL_REFUSAL in l for l in cell_lines)
    check("(c) at 60 games/arm/cell (600/arm) EVERY per-cell line STILL carries the inline refusal",
          "10 cell lines, all carrying the categorical cell refusal",
          f"{len(cell_lines)} cell lines, {sum(CELL_REFUSAL in l for l in cell_lines)} carrying it", ok)

    # (e) §9.3 pin assertion VOIDS a cell — and is clean when the pin holds.
    g3 = [dict(r) for r in g]
    for r in g3:
        if r["opp"] == "Erebus":
            r["oppver"] = "999"
    res3 = build(g3, led, state)
    out3 = _capture(res3)
    st3 = sign_test(res3)
    ok = (res3["voided"] == ["Erebus"] and "CELL Erebus VOIDED" in out3
          and st3["k"] + st3["tie"] == 9 and not res2["voided"])
    check("(e) §9.3 pin mismatch VOIDS that cell and reduces k — and is CLEAN when pins hold",
          "voided=['Erebus'], k reduced to 9 admitted cells; control run voided=[]",
          f"voided={res3['voided']}, admitted k={st3['k'] + st3['tie']}, control voided={res2['voided']}", ok)

    # (f) the arm cross-check alarms on a ledger/ourver disagreement, and is clean otherwise.
    g4 = [dict(r) for r in g]
    g4[0]["ourver"] = "125"
    res4 = build(g4, led, state)
    ok = len(res4["arm_alarms"]) == 1 and not res2["arm_alarms"]
    check("(f) arm cross-check ALARMS when the ledger arm and the replay ourver disagree",
          "1 alarm on the corrupted row; 0 on the clean run",
          f"corrupted={len(res4['arm_alarms'])}, clean={len(res2['arm_alarms'])}", ok)

    # (g) §1 cell exclusion: a thin cell is excluded and NAMED, a fat one admitted.
    g5, led5 = _synth(20, ["Juusto"])
    g6, led6 = _synth(60, [c for c in CELL_ORDER if c != "Juusto"])
    off = {m: v for m, v in led6.items()}
    off.update(led5)
    res5 = build(g5 + g6, off, state)
    out5 = _capture(res5)
    ok = (not res5["cells"]["Juusto"]["admitted"] and res5["cells"]["Erebus"]["admitted"]
          and "EXCLUDED from the primary (§1 CUT-SHORT: min 20 < 40/arm)" in out5)
    check("(g) §1 CUT-SHORT excludes a <40/arm cell BY NAME and admits a >=40/arm one",
          "Juusto EXCLUDED and named with its count; Erebus ADMITTED",
          f"Juusto admitted={res5['cells']['Juusto']['admitted']}, "
          f"Erebus admitted={res5['cells']['Erebus']['admitted']}", ok)

    # (h) the sign test itself, driven to a known answer.
    p = binom_two_sided_p(9, 10)
    p8 = binom_two_sided_p(8, 10)
    p10 = binom_two_sided_p(10, 10)
    ok = (abs(p - 0.0215) < 5e-4 and abs(p8 - 0.1094) < 5e-4 and abs(p10 - 0.0020) < 5e-4)
    check("(h) exact two-sided binomial reproduces §4's own table",
          "10/10 0.0020, 9/10 0.0215, 8/10 0.1094",
          f"{p10:.4f}, {p:.4f}, {p8:.4f}", ok)

    print()
    if fails:
        print(f"SELFTEST: FAIL — {len(fails)} control(s): {fails}")
        return 1
    print("SELFTEST: OK — every guard driven to both verdicts")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--games", default=os.path.join(ROOT, "corpus", "unrated_games.tsv"))
    ap.add_argument("--state", default=os.path.join(ROOT, "scratchpad", "fieldcal_state.tsv"))
    ap.add_argument("--scratch", default=os.path.join(ROOT, "scratchpad"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    state = load_state_tape(a.state)
    ledger = load_arm_ledger(a.scratch)
    if not ledger:
        raise Refusal(f"no arm_fieldcal_*.txt accept ledger under {a.scratch}; arm identity "
                      "has no engine-side source and §9.1 forbids inferring it from our own "
                      "output.")
    games = load_games(a.games)
    render(build(games, ledger, state))
    return 0


if __name__ == "__main__":
    sys.exit(main())
