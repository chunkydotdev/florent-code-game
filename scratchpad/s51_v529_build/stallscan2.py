#!/usr/bin/env python3
"""M4 scan v2: stalls classified by DISTANCE TO BOTH CORES and by whether
_nav was called during the stall.  Self-test drives all four cells."""
import sys, collections

def cores(lines):
    for ln in lines:
        if ln.startswith("RC MAP "):
            f = ln.split()
            o = tuple(int(x) for x in f[7].split(","))
            t = tuple(int(x) for x in f[9].split(","))
            return o, t
    return None, None

def d2(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def scan(lines, K=8):
    o, t = cores(lines)
    pos = collections.defaultdict(list)
    navr = collections.defaultdict(set)
    for ln in lines:
        f = ln.split()
        if ln.startswith("RC POS "):
            pos[int(f[4])].append((int(f[2]), f[14], f[8], f[10], f[6]))
        elif ln.startswith("RC WALK "):
            navr[int(f[4])].add(int(f[2]))
    out = []
    for uid, rows in pos.items():
        rp = None; rs = None; last = None
        for r in rows:
            if rp is None or r[1] != rp:
                if rp is not None and last[0] - rs >= K:
                    out.append((uid, rs, last[0], rp, last[2], last[3], last[4]))
                rp = r[1]; rs = r[0]
            last = r
        if rp is not None and last[0] - rs >= K:
            out.append((uid, rs, last[0], rp, last[2], last[3], last[4]))
    res = []
    for uid, a, b, p, role, fs, seat in out:
        xy = tuple(int(x) for x in p.split(","))
        navs = sum(1 for r in range(a, b+1) if r in navr[uid])
        res.append(dict(uid=uid, a=a, b=b, pos=p, role=role, fs=fs, seat=seat,
                        dour=d2(xy, o) if o else -1,
                        dthem=d2(xy, t) if t else -1,
                        navs=navs, span=b-a))
    return sorted(res, key=lambda r: r["a"])

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        base = ["RC MAP w 30 h 30 ours 2,2 theirs 27,27"]
        # A: mid-map stall with NO nav calls; B: mid-map stall WITH nav calls;
        # C: a clean walker (no stall).
        A = ["RC POS %d id 4 seat 1 role expand fs 0 body 1 pos 15,15 stuck 0" % i for i in range(1, 15)]
        Bn = ["RC POS %d id 5 seat 2 role raid fs 1 body 2 pos 10,10 stuck 0" % i for i in range(1, 15)] + \
             ["RC WALK %d id 5 role raid fs 1 body 2 pos 10,10 tgt 1,1 want NORTH verdict STUCK1 mcd 0 acd 0" % i for i in range(1, 15)]
        C = ["RC POS %d id 6 seat 3 role raid fs 0 body 1 pos %d,3 stuck 0" % (i, i) for i in range(1, 15)]
        r = scan(base + A + Bn + C)
        ids = {x["uid"]: x for x in r}
        assert set(ids) == {4, 5}, ids
        assert ids[4]["navs"] == 0 and ids[5]["navs"] == 14, r
        assert ids[4]["dour"] == 13**2*2 and ids[5]["dthem"] == 17**2*2, r
        assert scan(base + C) == [], "clean walker must yield no stall"
        print("SELFTEST OK: nav-silent=%d nav-busy=%d clean=0" % (ids[4]["navs"], ids[5]["navs"]))
        sys.exit(0)
    allr = []
    for path in sys.argv[1:]:
        for r in scan(open(path).read().splitlines()):
            r["f"] = path.rsplit("/", 1)[-1]
            allr.append(r)
    mid = [r for r in allr if r["dour"] > 64 and r["dthem"] > 64]
    print("total stalls>=8: %d   MID-MAP (d^2>64 from BOTH cores): %d"
          % (len(allr), len(mid)))
    print("mid-map, nav-silent: %d   nav-called: %d"
          % (sum(1 for r in mid if r["navs"] == 0),
             sum(1 for r in mid if r["navs"] > 0)))
    # ⭐ PER-ARM ROLL-UP.  The pooled line above answers "does this fixture
    # produce stalls at all"; the M4 claim is a DIFFERENCE BETWEEN ARMS, and a
    # pooled count cannot carry it.  Arm = the leading two underscore-fields of
    # the tape filename (inst_off / inst_walk / inst_v528 / inst_mut).
    import collections as _c
    peragm = _c.defaultdict(lambda: [0, 0, 0])   # [files, all stalls, mid-map]
    seen = set()
    for r in allr:
        a = "_".join(r["f"].split("_")[:2])
        peragm[a][1] += 1
        if r["dour"] > 64 and r["dthem"] > 64:
            peragm[a][2] += 1
    import glob as _g
    for path in sys.argv[1:]:
        a = "_".join(path.rsplit("/", 1)[-1].split("_")[:2])
        if path not in seen:
            peragm[a][0] += 1
            seen.add(path)
    print()
    print("%-12s %6s %10s %10s" % ("arm", "games", "stalls>=8", "MID-MAP"))
    for a in sorted(peragm):
        f, n, m = peragm[a]
        print("%-12s %6d %10d %10d" % (a, f, n, m))
    if len({tuple(v[1:]) for v in peragm.values()}) < 2 and len(peragm) > 1:
        print("⛔ GUARD: every arm produced the SAME counts -- the scan cannot "
              "discriminate on this fixture, so a 0 is not a reading.")
    print()
    for r in sorted(mid, key=lambda r: -r["span"])[:20]:
        print("  %-24s id %-4d r%-4d..r%-4d span %-4d pos %-7s role %-7s fs %s seat %s dour %-5d dthem %-5d navs %d"
              % (r["f"], r["uid"], r["a"], r["b"], r["span"], r["pos"], r["role"],
                 r["fs"], r["seat"], r["dour"], r["dthem"], r["navs"]))
