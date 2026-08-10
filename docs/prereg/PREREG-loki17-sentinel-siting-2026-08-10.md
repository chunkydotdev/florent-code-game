# PREREG — LOKI-17: SENTINEL SITING, FIRST-FIT → BEST-FIT

**PROVENANCE: a corpus/archive cut AND a tactics-library file, converging.**
The archive autopsy (195 replays, three opponents) and the library mining pass
found **the same line of code on the same day, neither knowing about the other**.
This is the **first non-negative library provenance** since Magnus created the
field — arrived at by convergence, not by going looking for a citation to write
down.

**TARGET BAND: every opponent we are paired with.** This is a fix to our own
play, so it pays across the whole reachable band (`us−80…us+125`, **18 teams**,
a 5-0 paying **+12.56 to +21.30**) rather than against a chosen stratum.
**First plank of the day that does not have to argue about who it is aimed at.**

**Committed BEFORE any bot edit exists.** Body certified at
`git log --diff-filter=A`; amendments self-certify and may only ADD.

---

## The defect, measured before any intervention

**~48% of the sentinels we build cannot shoot the enemy core on the round they
are built** — off every firing ray, out of range, or both. Nearest-**footprint-tile**
basis from each replay's own `map.cores` (the corpus `d2_enemy` column uses the
core ANCHOR and overstates).

| our sentinel builds | vs Ouroboros (n=522) | vs Askar City (n=283) | **Askar's own (n=253)** |
|---|---:|---:|---:|
| median nearest d² to enemy core | **32** — its range limit exactly | 25 | **18** |
| in range (d² ≤ 32) | 55.9% | 70.0% | **83.8%** |
| in range **and** on a ray | **52.1%** | 65.4% | **77.9%** |

**Measured across three separate opponents, so it is not a fact about any of
them.** We plant our longest-ranged weapon at the edge of its own reach.

## The mechanism, corrected against the code

The library relay says `_try_forward_sentinel` takes *"the first legal adjacent
tile with no scoring at all"* and that the hypothetical-turret predicate is
called *"zero times about an enemy"*. **Both are wrong for the live bot**, and
the truth is a better-specified plank. `bots/_v130loki13/raid.py:422-438`:

```python
for d in CARDINALS:
    bp = p.add(d)
    for target in tiles:
        if bp.distance_squared(target) > 32:                       continue  # RANGE checked
        facing = bp.direction_to(target)
        if not ct.can_fire_from(bp, facing, SENTINEL, target):     continue  # RAY checked
        if not ct.can_build_sentinel(bp, facing):                  continue
        ct.build_sentinel(bp, facing)                                        # FIRST hit wins
        return True
```

**The guard exists. The CHOICE does not.** It accepts the **first** tile that can
fire, never the best, so the site is decided by wherever the builder happened to
be standing when the predicate first passed — **which is exactly why the
distribution piles up at d²=32, the boundary.**

**⇒ FIRST-FIT vs BEST-FIT, not a missing check.** The aggregate 44%
out-of-range is consistent with this: **other build paths do not carry the
guard**, and the census counts every sentinel, not only forward ones.

## Bars — stated before any intervention exists, taken intact from the pre-data read

1. **PRIMARY (mechanism): shootable-on-build rate** (nearest-footprint **d² ≤ 32
   AND on one of the 8 rays) rises 52.1% → >85%**, and **median sentinel
   lifetime 27 → >74 rounds** (the Askar City level).
2. **MEDIATOR:** builder melee hits in r0–150 fall **median 63 → <20**; builder
   deaths **3.56/100 rounds → <1.5**.
3. **CURRENCY:** **median game length <300 rounds** and core-kill share rises.
   **Not a win rate** — a r1000 `titanium_collected` win is a defeat, and the
   ladder pays game share, not match wins.
4. **FALSIFIER, PRE-STATED AND IT FORKS THE ROAD:** if sentinels are placed
   correctly, **survive**, and the game **still runs past r500 with their core
   above 250 HP**, then the range asymmetry is not the lever — **the constraint
   is TRANSIT, and the lever is insertion, not placement.** That is a different
   plank and this prereg names it as a fork rather than absorbing it.

## ⛔ KNOWN LIMIT, in the body and not in a footnote

**No decoder in `tools/` emits sentinel FACING**, so **52.1% is an UPPER BOUND
on what can actually fire — the true baseline is worse.** Consequences,
pre-committed:

* The primary's **baseline may move down** when a facing decoder exists. **The
  >85% target does not move with it** — it is an absolute standard taken from
  Askar's 77.9% plus headroom, not a delta from our own number.
* If the facing decode lands before the leg fires, **it replaces the baseline and
  the change is recorded**; it cannot be used to re-choose the target.

## Measurement

Read-out on **archived replays only** — this plank needs no new games to measure
its primary, which is why it is cheap. Currency read via `leg_read.py` with
`--live-cells` from a calibration, `--bar` in the primary currency only, and
**per ring-stratum** (D34). Opponent version pinned from `league_matches.tsv`,
never `ladder_games.tsv.oppver` (NULL, and a null column reads as "no change").

## What this leg may not do

It may not be read as a win-rate result; it may not borrow LOKI-16's or
LOKI-14's bars; and **no threshold here may be revised because an implementation
turned out to reach a different number** — the bars predate the intervention and
stay that way.
