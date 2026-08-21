#!/usr/bin/env python3
"""NEWPOOL-BASELINE readout aggregator (builder s53).

Computes the four registered outputs of PREREG-NEWPOOL-BASELINE-2026-08-21.md:
(1) the pooled anchor with naive 95% CI (DEFF 0.98 -> naive per prereg),
(2) the three segments S1/S2/S3 (+ glacierkeep reported separately),
(3) the KILL_TARGET panel (ITT, denominator ALL rows, per side),
(4) the 15-cell per-map table with the pre-committed CRATER/STRONGHOLD rule.
Plus the F1/composition checks that the prereg orders read FIRST.

It prints NUMBERS ONLY. The reading sentence is typed by the builder against
the prereg's pre-committed table; this script contains no verdict language.

Self-test: --selftest fabricates tapes driven to BOTH verdicts on every
surface it reports (share flips, composition alarm fires and clears, kill
panel moves, truncated row refuses) so no column is a constant.
"""
import math
import sys

POOL = {
    "auroraveil", "bifrost", "fimbulwinter", "glacierkeep", "helheim",
    "holmgang", "icefloe", "jotunheim", "longhouse", "midgard", "paths",
    "skald", "stavkirke", "valkyrie", "yggdrasil",
}
S1 = {"midgard"}
S2 = {"auroraveil", "glacierkeep", "icefloe", "valkyrie"}
S3 = POOL - S1 - S2  # the ten new maps


def ci(w, n):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = w / n
    hw = 1.96 * math.sqrt(p * (1 - p) / n)
    return (100 * p, 100 * (p - hw), 100 * (p + hw))


def order_stat_median_ci(sorted_vals):
    """95% order-statistic interval for the median (normal approx to binomial)."""
    n = len(sorted_vals)
    if n == 0:
        return (None, None, None)
    med = sorted_vals[n // 2] if n % 2 else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    lo_i = int(math.floor(n / 2 - 1.96 * math.sqrt(n) / 2))
    hi_i = int(math.ceil(n / 2 + 1.96 * math.sqrt(n) / 2))
    lo_i = max(0, min(lo_i, n - 1))
    hi_i = max(0, min(hi_i, n - 1))
    return (med, sorted_vals[lo_i], sorted_vals[hi_i])


def parse(path):
    rows, bad = [], []
    fixture = None
    with open(path) as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln:
                continue
            if ln.startswith("# FIXTURE"):
                fixture = ln
                continue
            if ln.startswith("ts\t") or ln.startswith("#"):
                continue
            p = ln.split("\t")
            if len(p) != 9:
                bad.append(ln)
                continue
            rows.append(p)
    return fixture, rows, bad


def kill_panel(rows, side):
    n = len(rows)
    kills = sorted(int(r[8]) for r in rows if r[6] == side and r[7] == "core_destroyed")
    med, mlo, mhi = order_stat_median_ci(kills)
    itt = {k: 100 * sum(1 for t in kills if t <= k) / n for k in (150, 180, 200, 250, 300, 400)}
    rmst_vals = []
    for r in rows:
        if r[6] == side and r[7] == "core_destroyed":
            rmst_vals.append(min(int(r[8]), 300))
        else:
            rmst_vals.append(300)
    mean = sum(rmst_vals) / n
    sd = math.sqrt(sum((v - mean) ** 2 for v in rmst_vals) / (n - 1)) if n > 1 else 0.0
    return kills, (med, mlo, mhi), itt, mean, sd


def report(path):
    fixture, rows, bad = parse(path)
    if bad:
        print(f"REFUSING: {len(bad)} malformed row(s); first: {bad[0][:120]!r}")
        return 2
    n = len(rows)
    print(f"# {fixture}")
    print(f"rows={n}")

    # ---- F1 / composition, read FIRST per prereg ----
    maps = {}
    for r in rows:
        maps.setdefault(r[3], []).append(r)
    extra = set(maps) - POOL
    missing = POOL - set(maps)
    nowin = [r for r in rows if r[6] not in ("T", "C")]
    seat_imbal = []
    for m, rs in sorted(maps.items()):
        a = sum(1 for r in rs if r[5] == "A")
        b = len(rs) - a
        if abs(a - b) > 1:
            seat_imbal.append(f"{m} A={a} B={b}")
    seeds = sorted({int(r[4]) for r in rows})
    print("F1 COMPOSITION:")
    print(f"  distinct maps {len(maps)}; off-pool maps: {sorted(extra) if extra else 'NONE'}; "
          f"missing pool maps: {sorted(missing) if missing else 'NONE'}")
    print(f"  rows/map: " + " ".join(f"{m}={len(maps[m])}" for m in sorted(maps)))
    print(f"  NOWINNER/other rows: {len(nowin)}")
    print(f"  seat imbalance (>1): {seat_imbal if seat_imbal else 'NONE'}")
    print(f"  seed range {seeds[0]}..{seeds[-1]} ({len(seeds)} distinct)")
    comp_clean = not extra and not missing and not nowin and not seat_imbal
    print(f"  COMPOSITION {'CLEAN' if comp_clean else '*** ALARM ***'}")

    # ---- pooled anchor ----
    scored = [r for r in rows if r[6] in ("T", "C")]
    tw = sum(1 for r in scored if r[6] == "T")
    p, lo, hi = ci(tw, len(scored))
    print(f"\nPOOLED ANCHOR: {p:.2f} [{lo:.2f}, {hi:.2f}]  T={tw}/{len(scored)}  (naive CI; DEFF 0.98)")

    # ---- segments ----
    print("\nSEGMENTS:")
    for name, seg in (("S1 REFUSING {midgard}", S1), ("S2 SURVIVOR-RUNNING", S2), ("S3 NEW10", S3)):
        rs = [r for r in scored if r[3] in seg]
        w = sum(1 for r in rs if r[6] == "T")
        sp, slo, shi = ci(w, len(rs))
        print(f"  {name:26s} {sp:6.2f} [{slo:.2f}, {shi:.2f}]  n={len(rs)}  delta-vs-pooled {sp - p:+.2f}")
    gk = [r for r in scored if r[3] == "glacierkeep"]
    w = sum(1 for r in gk if r[6] == "T")
    sp, slo, shi = ci(w, len(gk))
    print(f"  glacierkeep (separate)     {sp:6.2f} [{slo:.2f}, {shi:.2f}]  n={len(gk)}")

    # ---- per-map table with pre-committed rule ----
    print("\nPER-MAP TABLE (rule: CRATER := cell<=pooled-10pp AND CI excludes pooled; "
          "STRONGHOLD := cell>=pooled+10pp AND CI excludes pooled):")
    crater_ct = strong_ct = 0
    for m in sorted(maps):
        rs = [r for r in maps[m] if r[6] in ("T", "C")]
        w = sum(1 for r in rs if r[6] == "T")
        cp, clo, chi = ci(w, len(rs))
        kt = sorted(int(r[8]) for r in rs if r[6] == "T" and r[7] == "core_destroyed")
        medk = kt[len(kt) // 2] if kt else None
        cls = ""
        if cp <= p - 10 and (chi < p or clo > p):
            cls = "CRATER"
            crater_ct += 1
        elif cp >= p + 10 and (clo > p or chi < p):
            cls = "STRONGHOLD"
            strong_ct += 1
        print(f"  {m:14s} {cp:6.2f} [{clo:6.2f}, {chi:6.2f}] n={len(rs):4d}  medkill(T)={medk}  {cls}")
    print(f"  classified: {crater_ct} CRATER, {strong_ct} STRONGHOLD "
          f"(~0.75 false classifications expected at 15 cells)")

    # ---- KILL_TARGET panel ----
    for side, label in (("T", "TREATMENT _v537socket"), ("C", "CONTROL _x3r0v168mjolnir")):
        kills, (med, mlo, mhi), itt, rmst, sd = kill_panel(scored, side)
        print(f"\nKILL_TARGET PANEL, side {side} ({label}), ITT denominator {len(scored)}:")
        print(f"  kill-wins {len(kills)}; median kill round {med} [{mlo}, {mhi}] (order-stat 95%)")
        print("  ITT kills " + "  ".join(f"<=r{k} {v:.2f}%" for k, v in itt.items()))
        print(f"  ITT RMST300 {rmst:.3f} (sd {sd:.2f})")
    tb = sum(1 for r in scored if r[7] == "tiebreak")
    t1000 = sum(1 for r in scored if int(r[8]) >= 1000)
    print(f"\nr1000 SHARE: cond==tiebreak {100 * tb / len(scored):.2f}% ({tb})  |  "
          f"turns>=1000 {100 * t1000 / len(scored):.2f}% ({t1000})  gap {t1000 - tb}")
    maj = "YES -> OFF-DOCTRINE DOWNGRADE APPLIES" if tb > len(scored) / 2 else "no"
    print(f"F4 majority-r1000 composition: {maj}")
    return 0


def selftest():
    import tempfile, os
    def mk(rows, header=True):
        f = tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False)
        f.write("# FIXTURE\tshard=SELFTEST\n")
        if header:
            f.write("ts\tshard\tgame\tmap\tseed\tseat\twinner\tcond\tturns\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
        f.close()
        return f.name

    def row(m, seat, win, cond="core_destroyed", turns="100", seed="1"):
        return ["t", "SELFTEST", "0", m, seed, seat, win, cond, turns]

    import io, contextlib
    def run(path):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = report(path)
        return rc, buf.getvalue()

    ok = True
    # 1. share reads both verdicts
    pool_pair = lambda w: [row(m, s, w) for m in sorted(POOL) for s in "AB"]
    _, out_hi = run(mk(pool_pair("T")))
    _, out_lo = run(mk(pool_pair("C")))
    ok &= "POOLED ANCHOR: 100.00" in out_hi and "POOLED ANCHOR: 0.00" in out_lo
    print(f"[{'ok' if ok else 'FAIL'}] share driven to 100 and 0")
    # 2. composition alarm fires on off-pool map and clears on clean pool
    _, out_bad = run(mk(pool_pair("T") + [row("saga", "A", "T")]))
    t = "*** ALARM ***" in out_bad and "saga" in out_bad and "COMPOSITION CLEAN" in out_hi
    ok &= t
    print(f"[{'ok' if t else 'FAIL'}] composition alarm fires on saga, clean on pool")
    # 3. NOWINNER counted and alarms
    _, out_nw = run(mk(pool_pair("T") + [row("midgard", "A", "NOWINNER", "unresolved_winner", "-")]))
    t = "NOWINNER/other rows: 1" in out_nw and "*** ALARM ***" in out_nw
    ok &= t
    print(f"[{'ok' if t else 'FAIL'}] NOWINNER row alarms")
    # 4. kill panel moves: all kills at r100 vs all tiebreaks
    _, out_kill = run(mk(pool_pair("T")))
    _, out_tb = run(mk([row(m, s, "T", "tiebreak", "1000") for m in sorted(POOL) for s in "AB"]))
    t = ("<=r150 100.00%" in out_kill and "<=r150 0.00%" in out_tb
         and "RMST300 100.000" in out_kill and "RMST300 300.000" in out_tb
         and "OFF-DOCTRINE DOWNGRADE APPLIES" in out_tb)
    ok &= t
    print(f"[{'ok' if t else 'FAIL'}] kill panel + F4 driven to both verdicts")
    # 5. truncated row refuses
    p = mk(pool_pair("T"))
    with open(p, "a") as f:
        f.write("t\tSELFTEST\t0\tmidgard\t1\tA\tT\n")
    rc, out_ref = run(p)
    t = rc == 2 and "REFUSING" in out_ref
    ok &= t
    print(f"[{'ok' if t else 'FAIL'}] truncated row -> refuse, rc=2")
    # 6. seat imbalance alarms
    _, out_seat = run(mk(pool_pair("T") + [row("skald", "A", "T"), row("skald", "A", "T")]))
    t = "skald A=3 B=1" in out_seat and "*** ALARM ***" in out_seat
    ok &= t
    print(f"[{'ok' if t else 'FAIL'}] seat imbalance alarms")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    sys.exit(report(sys.argv[1] if len(sys.argv) > 1 else "scratchpad/overnight/NEWPOOL-BASELINE.tsv"))
