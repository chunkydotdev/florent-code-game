#!/usr/bin/env python3
"""REPLACEMENT LATENCY from the forced-death probe.

Per game: the round the SEALER was killed (`PRESKILL520`), and the first
`FS ARRIVE` at a STRICTLY LATER round -- i.e. a body of ours back at the ring.
Latency = that round - the kill round.  A game with no later ARRIVE is
NEVER-REPLACED and is reported as such, NOT as a large number and NOT dropped:
dropping it flatters the median exactly where the plank fails.

⛔ THE CAP IS MAGNUS'S: ~15 rounds from death to a body engaging.  v513
measured 10 of 14 replaced at a MEDIAN OF 90 ROUNDS, 0 inside the cap.

SELFTEST drives: a tape with a kill and a later arrival (latency), a tape with
a kill and NO later arrival (never-replaced, must not read 0), a tape with an
arrival BEFORE the kill only (must not count it), and a tape with no kill at
all (excluded from the denominator, not counted as replaced).
"""
import sys
from pathlib import Path


def one(lines):
    kill = None
    arrivals = []
    for ln in lines:
        if ln.startswith("PRESKILL520 "):
            try:
                k = int(ln.split()[1])
            except (ValueError, IndexError):
                continue
            if kill is None or k < kill:
                kill = k
        elif ln.startswith("FS ARRIVE "):
            try:
                arrivals.append(int(ln.split()[2]))
            except (ValueError, IndexError):
                continue
    if kill is None:
        return None                      # no probe fired: not in the denominator
    later = [a for a in arrivals if a > kill]
    return (kill, min(later) - kill if later else None)


def med(v):
    v = sorted(v)
    if not v:
        return -1
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0


def report(logdir, name):
    lat, never, nokill = [], 0, 0
    for f in sorted(Path(logdir).glob("*.err")):
        r = one(open(f, errors="replace").read().splitlines())
        if r is None:
            nokill += 1
            continue
        if r[1] is None:
            never += 1
        else:
            lat.append(r[1])
    n = len(lat) + never
    print("%-8s probe fired in %2d games (%d had no arrival to kill) | "
          "REPLACED %2d/%2d | median latency %5s | <=15 in %d/%d | "
          "<=30 in %d/%d | never replaced %d"
          % (name, n, nokill, len(lat), n, med(lat),
             sum(1 for x in lat if x <= 15), n,
             sum(1 for x in lat if x <= 30), n, never))
    if lat:
        print("         latencies: %s" % sorted(lat))


SYN = [
    (["PRESKILL520 60 id 3 body 1", "FS ARRIVE 70 id 9 body 1 at (1, 1) dsq 1"],
     (60, 10)),
    (["PRESKILL520 60 id 3 body 1"], (60, None)),
    (["FS ARRIVE 10 id 3 body 1 at (1, 1) dsq 1", "PRESKILL520 60 id 3 body 1"],
     (60, None)),
    (["FS ARRIVE 10 id 3 body 1 at (1, 1) dsq 1"], None),
]


def selftest():
    ok = True
    for i, (tape, want) in enumerate(SYN):
        got = one(tape)
        if got != want:
            print("SELFTEST FAIL case %d: %s != %s" % (i, got, want))
            ok = False
    if med([]) != -1:
        print("SELFTEST FAIL: empty median is not -1"); ok = False
    if med([1, 2, 3]) != 2 or med([1, 2, 3, 4]) != 2.5:
        print("SELFTEST FAIL: median"); ok = False
    print("SELFTEST:", "PASS" if ok else "FAIL",
          "| cases:", [one(t) for t, _w in SYN])
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for d in sys.argv[1:]:
        report(d, Path(d).parent.name)
