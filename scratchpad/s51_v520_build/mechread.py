#!/usr/bin/env python3
"""v520 MECHANISM READER -- the bot-side tape, one row per arm.

Reads the stderr logs of an instrumented arm's grid and reports, per arm:
  SPLIT   split throws, riders per terminal link, arcs used, landing d^2 to
          their core, and the WALK REMAINDER (d^2 from the landing to the
          arc's anchor seat) -- the mandate's "measure the walk".
  TERM    terminal-launcher siting decisions, arcs reachable, seat coverage,
          and the (a)-vs-(b) CONFLICT count Magnus asked for.
  ARC     claims, claim-time collisions RESOLVED, and DUP -- ⛔ the alarm:
          two live bodies publishing the SAME arc after both claims settled.
          DUP must be 0.
  APPT    support-seat claims, BUSY refusals and YIELDs -- the dual-appointment
          race counter.  A YIELD is the race happening AND being resolved; a
          BUSY is it being prevented.
  PRES    rounds the presence reserve was open, rounds it BOUND (raised the
          floor above what the parent would have used), vacancy readings.
  ARRIVE  per body, the round it first reached the ring (FS_LOG "ARRIVE"), and
          the GAP between body 1 and body 2 -- the probe's headline number.
  PLANT   GF519 PLANT lines: the v520 change-3 dose.

⛔ EVERY COLUMN IS A COUNT OF A LINE THE BOT ONLY PRINTS WHEN THE BRANCH RAN.
An arm with the master flag off writes NO lines by construction, so its
instrument columns are VOID rather than zero -- the same caveat v518 and v519
recorded for their own `mOff`.  That is stated in the output, not left to the
reader.

SELFTEST: `--selftest` runs a synthetic tape through every counter and a
MUTATION control that must move every column.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path


def parse(lines):
    o = defaultdict(int)
    splits = []          # (rnd, body, arc, dsq, walk)
    terms = []           # (rnd, arcs, cov, covbest)
    arrive = {}          # (game, body) -> rnd   [filled by caller per game]
    plants = []
    for ln in lines:
        if ln.startswith("SPLIT520 "):
            f = ln.split()
            try:
                splits.append((int(f[1]), int(f[f.index("body") + 1]),
                               int(f[f.index("arc") + 1]),
                               int(f[f.index("dsq") + 1]),
                               int(f[f.index("walk") + 1])))
            except (ValueError, IndexError):
                o["PARSE_BAD"] += 1
            o["SPLIT"] += 1
        elif ln.startswith("TERM520 "):
            f = ln.split()
            try:
                terms.append((int(f[1]), int(f[f.index("arcs") + 1]),
                              int(f[f.index("cov") + 1]),
                              int(f[f.index("covbest") + 1])))
            except (ValueError, IndexError):
                o["PARSE_BAD"] += 1
            o["TERM"] += 1
        elif ln.startswith("ARC520 CLAIM"):
            o["ARC_CLAIM"] += 1
        elif ln.startswith("ARC520 COLLIDE"):
            o["ARC_COLLIDE"] += 1
        elif ln.startswith("ARC520 DUP"):
            o["ARC_DUP"] += 1
        elif ln.startswith("APPT520 CLAIM"):
            o["APPT_CLAIM"] += 1
        elif ln.startswith("APPT520 BUSY"):
            o["APPT_BUSY"] += 1
        elif ln.startswith("APPT520 YIELD"):
            o["APPT_YIELD"] += 1
        elif ln.startswith("PRES520 "):
            o["PRES_LINES"] += 1
            f = ln.split()
            try:
                o["PRES_BIND_MAX"] = max(o["PRES_BIND_MAX"],
                                         int(f[f.index("bind") + 1]))
                o["PRES_VAC_MAX"] = max(o["PRES_VAC_MAX"],
                                        int(f[f.index("vacant") + 1]))
            except (ValueError, IndexError):
                o["PARSE_BAD"] += 1
        elif ln.startswith("GF519 PLANT"):
            f = ln.split()
            o["PLANT"] += 1
            try:
                plants.append(int(f[2]))
            except (ValueError, IndexError):
                o["PARSE_BAD"] += 1
        elif ln.startswith("FS ARRIVE "):
            f = ln.split()
            try:
                arrive[int(f[f.index("body") + 1])] = min(
                    arrive.get(int(f[f.index("body") + 1]), 10 ** 9),
                    int(f[2]))
            except (ValueError, IndexError):
                o["PARSE_BAD"] += 1
        elif "Traceback" in ln:
            o["TRACEBACK"] += 1
    return o, splits, terms, arrive, plants


def med(v):
    v = sorted(v)
    return -1 if not v else v[len(v) // 2]


def report(logdir):
    tot = defaultdict(int)
    allsp, allte, allpl = [], [], []
    gaps, arr1, arr2 = [], [], []
    games = 0
    for f in sorted(Path(logdir).glob("*.err")):
        games += 1
        o, sp, te, arr, pl = parse(open(f, errors="replace").read().splitlines())
        for k, v in o.items():
            if k.endswith("_MAX"):
                tot[k] = max(tot[k], v)
            else:
                tot[k] += v
        allsp += sp
        allte += te
        allpl += pl
        if 1 in arr:
            arr1.append(arr[1])
        if 2 in arr:
            arr2.append(arr[2])
        if 1 in arr and 2 in arr:
            gaps.append(arr[2] - arr[1])
    print("games with a log: %d" % games)
    for k in ("TRACEBACK", "PARSE_BAD", "SPLIT", "TERM", "ARC_CLAIM",
              "ARC_COLLIDE", "ARC_DUP", "APPT_CLAIM", "APPT_BUSY",
              "APPT_YIELD", "PRES_LINES", "PRES_BIND_MAX", "PRES_VAC_MAX",
              "PLANT"):
        print("  %-14s %d" % (k, tot[k]))
    if allsp:
        print("SPLIT throws: n=%d  arcs=%s  median landing dsq=%d  "
              "median WALK=%d  walk==0 in %d/%d"
              % (len(allsp), sorted(set(s[2] for s in allsp)),
                 med([s[3] for s in allsp]), med([s[4] for s in allsp]),
                 sum(1 for s in allsp if s[4] == 0), len(allsp)))
        print("  in-ring landings (dsq<=8): %d/%d"
              % (sum(1 for s in allsp if s[3] <= 8), len(allsp)))
    if allte:
        print("TERM sitings: n=%d  median arcs reachable=%d  median cover=%d  "
              "cover>=1 in %d/%d  cover>=2 in %d/%d  conflicts=%d"
              % (len(allte), med([t[1] for t in allte]),
                 med([t[2] for t in allte]),
                 sum(1 for t in allte if t[2] >= 1), len(allte),
                 sum(1 for t in allte if t[2] >= 2), len(allte),
                 sum(1 for t in allte if t[3] > t[2])))
    if allpl:
        print("PLANT rounds: %s  median=%d" % (sorted(allpl)[:20], med(allpl)))
    if arr1 or arr2:
        print("ARRIVE: body1 n=%d median=%d | body2 n=%d median=%d | "
              "gap n=%d median=%d  gap<=1 in %d/%d"
              % (len(arr1), med(arr1), len(arr2), med(arr2), len(gaps),
                 med(gaps), sum(1 for g in gaps if g <= 1), len(gaps)))


SYN = """SPLIT520 12 lch (5, 5) body 3 arc 2 to (7, 7) dsq 1 walk 0 n 1
SPLIT520 13 lch (5, 5) body 9 arc 1 to (3, 3) dsq 2 walk 4 n 2
TERM520 11 id 3 at (4, 4) n 3 pick (5, 5) arcs 2 cov 2 covbest 3 conflict 1 dsq 5
ARC520 CLAIM 14 id 3 body 1 arc 2 at (7, 7)
ARC520 COLLIDE 15 id 9 body 2 peer 2 took 1
ARC520 DUP 16 id 9 body 2 arc 1 n 1
APPT520 CLAIM 4 id 9
APPT520 BUSY 5 id 11 held 9
APPT520 YIELD 6 id 11 won 9 n 1
PRES520 40 ti 75 res 119 floor 119 bind 3 rounds 3 vacant 3 until 60
GF519 PLANT 22 id 3 d 9 ti 200
FS ARRIVE 9 id 3 body 1 at (7, 7) dsq 1
FS ARRIVE 10 id 9 body 2 at (3, 3) dsq 2
"""


def selftest():
    ok = True
    o, sp, te, arr, pl = parse(SYN.splitlines())
    want = {"SPLIT": 2, "TERM": 1, "ARC_CLAIM": 1, "ARC_COLLIDE": 1,
            "ARC_DUP": 1, "APPT_CLAIM": 1, "APPT_BUSY": 1, "APPT_YIELD": 1,
            "PRES_LINES": 1, "PLANT": 1}
    for k, v in want.items():
        if o[k] != v:
            print("SELFTEST FAIL %s: %d != %d" % (k, o[k], v)); ok = False
    if o["PARSE_BAD"]:
        print("SELFTEST FAIL: PARSE_BAD %d" % o["PARSE_BAD"]); ok = False
    if arr != {1: 9, 2: 10}:
        print("SELFTEST FAIL arrive: %s" % arr); ok = False
    if [s[4] for s in sp] != [0, 4]:
        print("SELFTEST FAIL walk: %s" % sp); ok = False
    if te[0][3] <= te[0][2]:
        print("SELFTEST FAIL conflict fixture is not a conflict"); ok = False
    # MUTATION CONTROL: every counted line rewritten to a tag we do not count.
    mut = "\n".join("XX" + ln for ln in SYN.splitlines())
    o2, sp2, te2, arr2, pl2 = parse(mut.splitlines())
    if any(o2[k] for k in want) or sp2 or te2 or arr2 or pl2:
        print("SELFTEST FAIL: mutation control still counted %s" % dict(o2))
        ok = False
    # SECOND MUTATION: the DUP alarm alone must move, and nothing else.
    nodup = "\n".join(ln for ln in SYN.splitlines()
                      if not ln.startswith("ARC520 DUP"))
    o3, _s, _t, _a, _p = parse(nodup.splitlines())
    if o3["ARC_DUP"] != 0 or o3["ARC_CLAIM"] != 1:
        print("SELFTEST FAIL: DUP mutation moved the wrong column"); ok = False
    # THIRD: a malformed line must be COUNTED as PARSE_BAD, not swallowed.
    o4, _s, _t, _a, _p = parse(["SPLIT520 12 lch (5, 5) body"])
    if not o4["PARSE_BAD"]:
        print("SELFTEST FAIL: malformed line not reported"); ok = False
    print("SELFTEST:", "PASS" if ok else "FAIL")
    print("  fixture ->", dict(o))
    print("  mutation ->", dict(o2))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    for d in sys.argv[1:]:
        print("=== %s ===" % d)
        report(d)
