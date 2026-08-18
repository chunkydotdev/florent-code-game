#!/usr/bin/env python3
"""M4 scan: find builder bodies whose POSITION is constant for >= K rounds.
Self-test: a synthetic tape with one 12-round stall and one clean walker must
return exactly one stall; a tape with no stalls must return zero."""
import sys, collections, re

def scan(lines, K=8):
    seen = collections.defaultdict(list)   # id -> [(rnd,pos,role,fs,stuck)]
    for ln in lines:
        if not ln.startswith("RC POS "):
            continue
        f = ln.split()
        try:
            rnd = int(f[2]); uid = int(f[4]); seat=f[6]; role = f[8]; fs = f[10]
            pos = f[14]; stuck = f[16]
        except Exception:
            continue
        seen[uid].append((rnd, pos, role, fs, stuck, seat))
    out = []
    for uid, rows in seen.items():
        run_start = None; run_pos = None; last = None
        for r in rows:
            if run_pos is None or r[1] != run_pos:
                if run_pos is not None and last[0] - run_start >= K:
                    out.append((uid, run_start, last[0], run_pos, last[2], last[3], last[4], last[5]))
                run_pos = r[1]; run_start = r[0]
            last = r
        if run_pos is not None and last[0] - run_start >= K:
            out.append((uid, run_start, last[0], run_pos, last[2], last[3], last[4], last[5]))
    return sorted(out, key=lambda t: t[1])

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        good = ["RC POS %d id 3 seat 0 role raid fs 1 body 1 pos %d,%d stuck 0" % (i, i, 0) for i in range(1, 30)]
        bad = ["RC POS %d id 4 seat 1 role expand fs 0 body 1 pos 5,5 stuck 0" % i for i in range(1, 14)]
        a = scan(good); b = scan(good + bad)
        assert len(a) == 0, a
        assert len(b) == 1 and b[0][0] == 4 and b[0][1] == 1 and b[0][2] == 13, b
        print("SELFTEST OK: clean tape 0 stalls, stalled tape 1 stall", b[0])
        sys.exit(0)
    for path in sys.argv[1:]:
        rows = scan(open(path).read().splitlines())
        print("== %s  stalls>=8rnd: %d" % (path, len(rows)))
        for r in rows[:12]:
            print("   id %-4d r%-4d..r%-4d pos %-7s role %-7s fs %s stuck %s seat %s" % r)
