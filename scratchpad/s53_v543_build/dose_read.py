#!/usr/bin/env python3
"""v543 INSTRUMENT #4 -- THE DOSE TAPE READER (RATIFY-C precondition).

Reads the per-game `V543` stderr tapes produced by `identity_grid.py --keep-err`
and reports the two PRE-COMMITTED floor shares plus the pair-existence clause.

⛔ THE FLOORS ARE NOT THIS FILE'S TO CHOOSE. They are passed in and printed
beside the measurement so the comparison is visible rather than asserted:
    fires>=1  >= 20.0% of games
    bought>=1 >=  8.0% of games
    PAIR-EXISTS: at least one purchase with live>=1 anywhere in the tape

TAPE GRAMMAR (siege.py / main.py, all stderr, one line per event):
    V543 FIRE <rnd> id <id> ti <ti> rise <n> harv <n> n <fires> until <rnd>
    V543 PAIR <rnd> id <id> live <live> ti <ti> need <n> orth <n> n <n> until <r>
    V543 AMMO <rnd> amt <n> floor <n> fwd <n> spent <n> bind <n>
`live` is field 7 (1-indexed) on a PAIR line -- the live forward-sentinel count
AT THE MOMENT OF PURCHASE, which is the field the simultaneous-pair claim rests
on.

⚠ AN EMPTY TAPE DIRECTORY MUST NOT READ AS 0.0% -- that is a blind instrument
reporting a verdict. `--min-games` refuses to print a share below it.

    dose_read.py TAPEDIR --min-games 500 --floor-fires 20.0 --floor-bought 8.0
    dose_read.py --selftest
"""
from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

if __name__ == "__main__":
    import sys as _hg
    if "-h" in _hg.argv[1:] or "--help" in _hg.argv[1:]:
        print(__doc__)
        raise SystemExit(0)


def parse_tape(text):
    """-> (n_fire_lines, n_pair_lines, n_pair_live_ge1, n_ammo_lines)."""
    f = p = pl = am = 0
    for line in text.splitlines():
        w = line.split()
        if len(w) < 3 or w[0] != "V543":
            continue
        if w[1] == "FIRE":
            f += 1
        elif w[1] == "PAIR":
            p += 1
            # ... id <id> live <live> ...
            try:
                if w[5] == "live" and int(w[6]) >= 1:
                    pl += 1
            except (IndexError, ValueError):
                pass
        elif w[1] == "AMMO":
            am += 1
    return f, p, pl, am


CASES = [
    ("no tape at all", "", (0, 0, 0, 0)),
    ("one fire, no purchase",
     "V543 FIRE 67 id 1 ti 158 rise 22 harv 3 n 1 until 107\n", (1, 0, 0, 0)),
    ("purchase at live 0 is NOT a pair",
     "V543 PAIR 28 id 3 live 0 ti 103 need 7 orth 5 n 1 until 64\n",
     (0, 1, 0, 0)),
    ("purchase at live 1 IS a pair",
     "V543 PAIR 137 id 3 live 1 ti 128 need 7 orth 6 n 2 until 164\n",
     (0, 1, 1, 0)),
    ("unrelated stderr is ignored",
     "TIWATCH518 40 ti 12 ammo 0\nTraceback (most recent call last)\n",
     (0, 0, 0, 0)),
    ("mixed tape",
     "V543 FIRE 67 id 1 ti 158 rise 22 harv 3 n 1 until 107\n"
     "V543 PAIR 70 id 4 live 0 ti 99 need 2 orth 2 n 1 until 107\n"
     "V543 PAIR 88 id 4 live 1 ti 120 need 2 orth 2 n 2 until 107\n"
     "V543 AMMO 72 amt 20 floor 12 fwd 1 spent 20 bind 1\n", (1, 2, 1, 1)),
]


def selftest() -> int:
    ok = True
    for label, src, want in CASES:
        got = parse_tape(src)
        good = got == want
        print(f"  {'PASS' if good else 'FAIL'}  {label}: {got} (want {want})")
        ok = ok and good
    print("SELFTEST", "PASS" if ok else "FAIL",
          f"-- {len(CASES)} cases; parser driven to fire/no-fire, "
          "pair/no-pair and live0/live1 both ways")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tapedir", nargs="?")
    ap.add_argument("--rows", help="the run's TSV manifest -- THE DENOMINATOR. "
                    "⛔ Tape FILES are written only for games with non-empty "
                    "stderr, so counting files would silently drop every "
                    "zero-tape game and bias both shares UPWARD, in the "
                    "flattering direction. A game with no tape is a game with "
                    "no fire, and it belongs in the denominator.")
    ap.add_argument("--min-games", type=int, default=1)
    ap.add_argument("--floor-fires", type=float, default=20.0)
    ap.add_argument("--floor-bought", type=float, default=8.0)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.tapedir:
        ap.error("give a tape directory, or --selftest")

    files = sorted(Path(a.tapedir).glob("*.err"))
    n = len(files)
    manifest = None
    if a.rows:
        with open(a.rows) as fh:
            hdr = fh.readline().rstrip("\n").split("\t")
            manifest = [dict(zip(hdr, ln.rstrip("\n").split("\t")))
                        for ln in fh if ln.strip()]
        n = len(manifest)
        missing = n - len(files)
        print(f"DENOMINATOR from manifest: {n} games; tape files: {len(files)}; "
              f"games with NO tape file: {missing} "
              f"(counted as fires=0, bought=0)")
        if missing < 0:
            print("⛔ MORE TAPES THAN GAMES -- stale tape directory. STOP.")
            return 2
    if n < a.min_games:
        print(f"⛔ BLIND: {n} tapes found, --min-games {a.min_games}. "
              "REFUSING to print a share.")
        return 2

    fires_games = bought_games = pair_games = 0
    tot = collections.Counter()
    per_map_games = collections.Counter()
    per_map_fire = collections.Counter()
    per_map_bought = collections.Counter()
    per_seat_fire = collections.Counter()
    per_seat_games = collections.Counter()
    pair_lines = []
    if manifest is not None:
        # ⛔ PER-CELL DENOMINATORS COME FROM THE MANIFEST TOO, for the same
        # reason the global one does: a map whose games all fell silent would
        # otherwise vanish from the table instead of reading 0%.
        for r in manifest:
            per_map_games[r["map"]] += 1
            per_seat_games[r["seat"]] += 1
    for f in files:
        arm, opp, mp, seed, seat = f.stem.split("_")
        txt = f.read_text()
        fl, pr, pl, am = parse_tape(txt)
        tot["fire_lines"] += fl
        tot["pair_lines"] += pr
        tot["pair_live_ge1"] += pl
        tot["ammo_lines"] += am
        if manifest is None:
            per_map_games[mp] += 1
            per_seat_games[seat] += 1
        if fl:
            fires_games += 1
            per_map_fire[mp] += 1
            per_seat_fire[seat] += 1
        if pr:
            bought_games += 1
            per_map_bought[mp] += 1
        if pl:
            pair_games += 1
            for line in txt.splitlines():
                w = line.split()
                if len(w) > 6 and w[:2] == ["V543", "PAIR"] and w[5] == "live" \
                        and int(w[6]) >= 1:
                    pair_lines.append(f"{f.stem}: {line.strip()}")

    def share(k):
        return 100.0 * k / n

    print(f"GAMES WITH A TAPE FILE: {n}")
    print()
    print("PRE-COMMITTED FLOORS (registered in the draft prereg, not set here)")
    for label, got, floor in (
            ("fires>=1 ", share(fires_games), a.floor_fires),
            ("bought>=1", share(bought_games), a.floor_bought)):
        verdict = "PASS" if got >= floor else "FAIL"
        print(f"  {label}  {got:5.1f}%  ({int(round(got * n / 100))}/{n})"
              f"   floor {floor:4.1f}%   -> {verdict}")
    pe = "PASS" if tot["pair_live_ge1"] else "FAIL"
    print(f"  PAIR-EXISTS (>=1 purchase at live>=1)   "
          f"{tot['pair_live_ge1']} events in {pair_games} games   -> {pe}")
    print()
    print("COUNTER TOTALS (lines across all tapes)")
    for k in ("fire_lines", "pair_lines", "pair_live_ge1", "ammo_lines"):
        print(f"  {k:16s} {tot[k]}")
    print()
    print("PER-MAP  (games / fires>=1 / bought>=1)")
    for mp in sorted(per_map_games):
        g = per_map_games[mp]
        print(f"  {mp:14s} {g:4d}   fire {per_map_fire[mp]:3d} "
              f"({100.0*per_map_fire[mp]/g:5.1f}%)   bought "
              f"{per_map_bought[mp]:3d} ({100.0*per_map_bought[mp]/g:5.1f}%)")
    print()
    print("PER-SEAT fires>=1")
    for st in sorted(per_seat_games):
        g = per_seat_games[st]
        print(f"  seat {st}: {per_seat_fire[st]}/{g} ({100.0*per_seat_fire[st]/g:.1f}%)")
    if pair_lines:
        print()
        print(f"PAIR EVENTS AT live>=1 ({len(pair_lines)}):")
        for ln in pair_lines[:20]:
            print("  " + ln)
    return 0


if __name__ == "__main__":
    sys.exit(main())
