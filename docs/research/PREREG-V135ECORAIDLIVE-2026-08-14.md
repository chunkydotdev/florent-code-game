# PREREG — V135-ECORAID-LIVE pinned leg (research s39, 2026-08-14)

**STATUS: committed BEFORE leg creation** (two-clock standard; side lane
certifies vs platform `createdAt`). Research designs; the BUILDER executes.
Supersedes `PREREG-V135CHAR-2026-08-14.md` (nothing fired under it).

## Subject and question
**v135** (x3r0's authorized run, live since ~07:20:45Z; holder verified by
this lane at `fcode status`). The builder verified the pulled artifact
**byte-identical to `bots/_v213ecoraid`** — the rc8.5/ECORAID tree whose
pre-declared live pooled read was **23/50 (46.0%) vs control 12/25 (48.0%),
NO SUPPORT** (typed 05:12Z; that verdict STANDS and is not re-opened here).
x3r0 shipped it on 56.8% self-play vs v134 — the self-play-flattery class
this lane decomposed in s38. **Question: the FAMILY's live performance at
larger n, now that the family holds the slot anyway at zero cost.**

## Design
- **PINNED leg** (treatment-style fixture ⇒ pins mandatory per the s36
  pinning spec), on the five family cells at the SAME pins used by all seven
  rc8.x legs: **team lazy v222 · Leviathan v67 · LingLing40 v40 · Juusto v7
  · Coreflood v83** (`--match <past_match_id>` per cell; builder holds the
  pin ids from MC).
- **One pinned match per cell per leg = 25 games/leg.** This prereg licenses
  legs of this shape while v135 holds; each leg is announced on the tape at
  fire time.
- **UNITS (side-lane flag folded in pre-fire): every n in this prereg counts
  GAMES, at 5 games per accepted match.** One leg = 5 accepts ≈ one 20-min
  rate window at the runner's observed ~4.2-min accept pacing. The pooled
  threshold "n ≥ 75" therefore means 75 games (rc8.5's 50 + this leg's 25),
  never 75 accepts.
- Zero submits, zero activations, zero rated exposure (v135 already holds).
- **Stop:** any holder change ends the series at the last complete leg.

## Read rules (declared before data)
1. Per-leg descriptive tally at any n.
2. **PRE-DECLARED POOLED FAMILY READ: this series' games + rc8.5's 50 live
   games pool into a FAMILY-LIVE surface** (pooling license = the tree
   byte-identity; if that identity claim fails verification the pool is
   VOID and legs read alone). Statistic: pooled game share with 95%
   Clopper-Pearson CI, reported against the rc8.5 control arm's 12/25
   (48.0%) as reference. First pooled read at total family-live n ≥ 75
   (i.e. after leg 1 completes); subsequent reads only at each completed
   leg, not between.
3. This measures the FAMILY LIVE, labeled as such — it does NOT re-open the
   builder's typed rc8.5 verdict, and the verdict sentence on anything this
   surface produces stays the builder's.
4. No ship/slot verdict language from this lane — the slot call is
   Magnus's/x3r0's; the deliverable is the report (this doubles as the v135
   characterization for the armed analysis task).

## Instrument alarms
- Any game decoding `ourver` ≠ 135 voids its leg (holder changed mid-leg).
- Any decoded `oppver` differing from its cell's pin = the pin did not take
  or the decode is wrong — report, do not read that cell (standing rule).

## Target-value line
Unrated, zero rated exposure ⇒ payout gate N/A. Band read at boot (07:03Z):
15 admissible at our 1790; cells lazy/Juusto/Coreflood/LingLing40 in-band,
Leviathan out-of-band kept for family-pin continuity.
