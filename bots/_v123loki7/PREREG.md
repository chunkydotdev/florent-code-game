# LOKI-7 (v123) — LOKI-6's arrival fixes + LOKI-QUIET's silenced builder melee

version: unrated benchmark only. **NOT for the ladder** — Magnus holds that
  approval explicitly ("continue iterating until I approve the ladder for Loki").
dev_dir: bots/_v123loki7
line: loki. **COMPARE_AGAINST both parents on the identical fixture** —
  `_v122loki6` (v97) and the quiet arm (v96), same 5 short maps, same 3 opponents.

produces: **CORE-KILL SHARE.** Both parents measured well on that fixture:
  quiet 12/15 = 80% (p=0.025 vs Eir's 5/15 = 33%), LOKI-6 7/10 = 70%,
  LOKI-4 8/15 = 53%, v94 Eir 5/15 = 33%. The two changes are independent and
  share ONE mechanism: **acting and moving are mutually exclusive**, so both
  hand rounds back to movement — quiet frees rounds the raider spent ACTING,
  LOKI-6 frees rounds it spent STOOD DOWN. They should compose without
  double-counting.

falsifier: **core-kill share at or below BOTH parents.** Specifically: if
  LOKI-7 lands under 70%, the changes interfere rather than compose and the
  right move is to ship the better single parent, not the combination.

treatment_occurrence: quiet half is **verified by decode** — 0 builder attacks
  in 5 live games and 0/985 locally. LOKI-6 half is a **removal of blocks** and
  occurs only where the block would have fired; not separately verified, as
  stated in that iteration's own PREREG.

S5_unrated: **this IS the unrated read**, under Magnus's standing grant. Same
  fixture as every arm above so the comparison is real rather than two
  experiments.

## LIMITS AND THE WAY THIS LOSES

- **Two economy leaks are now stacked on one bot.** Quiet silences the SIPHON,
  which is real income; LOKI-6's launcher release can pay 20 Ti + 10% scale to
  rebuild a launcher that dies again. **If LOKI-7 measures below both parents,
  that interaction is the first place to look**, not the raid layer.
- **n=15, and I cannot control seat assignment.** Seats have varied per leg
  (quiet drew b/a/a, LOKI-6 a/a), which is better than the seat-locked earlier
  legs but is luck, not design. Research measured seat effects null league-wide
  at n=2,715, which bounds the confound without removing it.
- **quiet's advantage over LOKI-4 is NOT significant** (12/15 vs 8/15,
  p=0.245). Only its advantage over *Eir* is (p=0.025). So the line's internal
  ordering is still weakly determined and I will not present LOKI-7 as beating
  a settled predecessor.

---

## CORRECTION, WRITTEN BEFORE LOKI-7'S RESULTS EXIST

**One of the two premises above is now false, and I am striking it rather than
letting the leg be read against a claim I know is wrong.**

I stated *"LOKI-6 7/10 = 70%"* and built this iteration on "compose two winning
changes." **That 70% was read off an INCOMPLETE fixture — two opponents of
three — and the missing leg was the bad one.** LOKI-6 vs Ouroboros landed
**1-4, 1/5 core kills.** True LOKI-6 fixture total:

| arm | record | core-kill share |
| --- | --- | --- |
| v94 Eir | 11-4 | 5/15 = **33.3%** |
| LOKI-4 | 8-7 | 8/15 = **53.3%** |
| **LOKI-5 (quiet)** | **12-3** | **12/15 = 80.0%** |
| **LOKI-6 (arrival fixes)** | **8-7** | **8/15 = 53.3%** |

**⇒ LOKI-6 is NOT an improvement on LOKI-4. It is identical on the primary
currency (8/15 both) and identical on record (8-7 both).** The three arrival
defect fixes measured NULL on this fixture.

**So LOKI-7 is not "two winning changes composed." It is LOKI-5's silenced
melee — the one change with real evidence — carried on top of three fixes that
measured null.** The revised expectation is therefore: **LOKI-7 should land near
LOKI-5's 80%, not above it.** If it lands materially below 80%, the arrival
fixes are actively harmful in combination and the right ship is plain LOKI-5.

**The failure mode I committed here is worth naming because it is the one I
have been auditing in others all day: I read a partial fixture as a result.**
Three of five legs is not a fixture, and the honest rule is the one I already
apply to batteries — **an incomplete run has no number, not a provisional one.**
