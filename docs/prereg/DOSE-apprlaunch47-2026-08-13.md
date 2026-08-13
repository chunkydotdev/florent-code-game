# DOSE PREREG — #47 (iteration 4): approach-triggered launcher

**Committed before any dose game (two-clock: this commit's git author time vs
run wall clocks in the readout).** Builder s37, 2026-08-13. Built from queue
row #47 as stocked by research (same day); mechanism carry-over per the row:
eviction-when-launcher-exists needs no re-proof (205 r<160 evictions,
`DOSE-launch0evict45`). This dose tests only the CONDITIONAL claim.

## The plank

`bots/_v207apprlaunch` = incumbent `_v197mapcode` + `LOKI_APPR_LAUNCHER`:
an enemy builder bot within `LOKI_APPR_DSQ=50` of our core (seen by the unit
deciding the launcher build) waives `LAUNCHER_MIN_RND` and zeroes
`LAUNCHER_RESERVE` for that decision. Cap stays 1 (the existing latch).
Outside the triggered state the behaviour is the incumbent's. Per-round
`GATE45` arithmetic log carried from iteration 2 on research's request, so
trigger-timing attribution (approach round vs bank vs build round) is
readable. Tags: `APPR45` (trigger, with bank), `GATE45`, `EVICT45`.

## Bars (fixture `_probe_creeper`, frozen; 8 games × {midgard, frostgate},
## seeds 994001-8, kept replays)

1. **VALIDITY — PRE-treatment denominator (iter-3's collider fix):** enemy
   builders APPROACH (APPR45 ≥1) in ≥6 of 8 games per map. Plants are NOT
   the denominator — the treatment suppresses them.
2. **DOSE BAR (a) — the conditional's triggered half:** among games with
   APPR45, a launcher is BUILT at r<160 in ≥half (readable as EVICT45 r<160
   or the launcher's build via GATE45 cessation; the definitive read is the
   replay's entity events if tags are ambiguous). **FALSIFIER: 0 r<160
   launcher builds across all approached games ⇒ approach detection triggers
   too late to beat the bank drain — the row's named fallback (spend-freeze
   fork) becomes the design, and the GATE45 log shows the bank level at
   trigger to prove it.**
3. **DOSE BAR (b) — the conditional's quiet half is screened, not dosed:**
   the creeper fixture approaches in every game, so (b) — launcher count 0
   in unsieged games — cannot be read here. It is the corefill screen's job
   (`APPRLAUNCH` vs `_v197mapcode`, self-play: the incumbent's raiders DO
   enter our half, so self-play prices the trigger's false-positive premium
   — the −6.34pp hazard — exactly where it lives). Named here so nobody
   reads the dose as having covered it.
4. **TAG-ATTRIBUTION CONTROL (2 games, frostgate):** scratch copy with
   `LOKI_APPR_LAUNCHER=False`, tags present: 0 APPR45/GATE45, 0 r<160
   EVICT45; r≥160 legacy throws disclosed.

## Sequence if bars pass

Corefill screen `APPRLAUNCH` (the unsieged premium is the named hazard; an
inside-band screen + a met dose is the plank's case) → pinned live leg vs
CAL-3 C1/C4 (LingLing40, team lazy) with its own prereg and research's
fire-order coordination. Feed-interruption is the live mechanism metric.
