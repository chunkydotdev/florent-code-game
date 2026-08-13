# RECORD — mutation-test evidence for two tools (claim_check items, s36)

Written 2026-08-13 (builder s36) because `tools/claim_check.py` fires on both:
a claimed test whose record no file names is a claim ahead of its record.

## tools/dash/shard_diffcheck.py — BACKED, run by the builder this session

Built by the dash subagent (commit `bcd560d`), **re-run by the builder against
the restarted live server** (the live 8787 process predated the new code; the
subagent's own run used a second port). Output, 2026-08-13 ~09:23Z:

    A. STRICT — PASS (74 shards × 6 fields identical, 0 mismatches)
    B. LIVE   — PASS (captures 40s apart; every idle hb_age tracked the clock
                 to within 3s — frozen fails AND drifting fails)
    C. MAPS   — PASS (62 shards agree in sign RETIRED>0 <=> pre-rotation/MIXED;
                 12 under-400 shards SKIPPED as no-rate, which is not zero)
    SELFTEST  — A OK · A2 OK · B1 OK · B2 OK · B3 OK · C OK
    VERDICT: PASS

The check's own two self-catches (idle hb_age must advance EXACTLY the
inter-capture gap; membership changes only when the worklist mtime is newer)
are in the subagent's report, relayed in the s36 coordination tail.

## tools/ship_ledger.py — claim UPHELD for the tool, fixture DECAYED, repair routed

The s35 drive (15/15 cells, control forced to refuse) is recorded in the s35
builder wrap (coordination tail, 2026-08-13T07:5xZ block). **Re-run s36: cells
1–2 now FAIL (16 leaks vs expected 2; +16.44 vs −8.01) — NOT tool breakage:
those cells pinned a REAL `ladder_games.tsv` window as their fixture and the
s36 corpus backfill (+1,108 replays) rewrote history under them.** Cell 4
(synthetic rows) still passes both directions, including the freshness refusal.
⇒ A selftest fixture pinned to a live surface decays with the surface — the
defect class `overnight_read`'s calibration cells already taught. **Repair
(synthetic-row fixtures for cells 1–2) is a routed task in the s36 builder
session; until it lands, ship_ledger verdicts lean on cell 4's guards plus the
direct per-match `ourver` pairing-boundary check, which tonight's leg uses
independently of this tool.**
