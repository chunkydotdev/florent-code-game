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

---

# AMENDMENT 1 — THE "KNOWN LIMIT" WAS FALSE. TRUE BASELINES IN. **TARGET UNCHANGED.**

**Committed before the leg fires and before any measurement of the
intervention.** ADD-only: it strikes a false limitation, records true baselines,
voids a stated justification, and pre-commits an interpretation. **No bar moves.**

## 1a. STRUCK: "no decoder in `tools/` emits sentinel FACING"

**False on both halves, and I verified it rather than taking the retraction.**
`Sentinel { Direction direction = 1 }` is a declared field of
`PlaceEntity.Entity`; **`replay_census.py` has decoded `direction` since it was
written** (`Ent.__slots__` carries it, line 186); and **`tools/loki9_facing.py`
is a shipped tool built entirely on turret facing**, whose docstring says
*"Facing is on the wire… `parse_entity` already decodes it. Nothing is
inferred."*

**The limit was asserted without grepping `tools/` for a decoder, and I put it
in this prereg's body.** Straight D30 — *an audit of the evidence is not an
audit of the codebase* — committed by the research arm and **not caught by me,
who owns the file.** The primary is now measurable **exactly**, not as a bound.

**Validation, and it is the strongest instrument work of the day:**

| check | RAW | ROT+45° | ROT+90° | FLIP-Y |
|---|---:|---:|---:|---:|
| conveyor delivery tile = `from + delta(facing)` (204,819 moves) | **1.0000** | 0.0000 | 0.0000 | 0.5837 |
| gunner shot on facing ray (12,759 `FireTurret`) | **1.0000** | 0.0000 | 0.0000 | 0.1736 |

Two independent signals, both perfect, **and one compass step takes both to
exactly zero — so it is not a constant column.** The **FLIP-Y residual is the
compass control**: 0.5837 is exactly the E/W conveyors, the two directions a
y-flip cannot break, **confirming NORTH = (0,−1) empirically rather than by
quoting `CLAUDE.md` at it.**

## 1b. TRUE BASELINES — and the number that moved is not ours

| population | n | in range | UPPER (any ray) | **TRUE (actual facing)** |
|---|---:|---:|---:|---:|
| ours vs Ouroboros | 522 | 55.9% | 52.1% | **50.4%** |
| ours vs Askar City | 283 | 70.0% | 65.4% | **62.2%** |
| **Askar City's OWN** | 253 | 83.8% | 77.9% | **67.6%** |

**The ratchet clause worked and was worth 1.7pp** — our baseline barely moves
(52.1 → **50.4**). The primary's baseline is **50.4%**.

## 1c. ⚠ THE TARGET'S JUSTIFICATION IS VOID. THE TARGET IS NOT.

Line 88 derives `>85%` as *"an absolute standard taken from Askar's 77.9% plus
headroom."* **Askar's TRUE figure is 67.6%, so >85% now stands 17.4pp above the
best real bot observed, not 7.1pp.** The justification is withdrawn.

**THE TARGET DOES NOT MOVE.** Moving a bar because it started to look
unreachable is the exact case this project's convention names as forbidden — and
an unreachable-looking bar is precisely when moving it feels most reasonable.
**What is pre-committed instead is the INTERPRETATION**, in the shape Amendment
7 of `PREREG-loki14b` established:

| measured shootable-on-build | how it MUST be written |
|---|---|
| **> 85%** | **TARGET MET.** |
| **67.6% – 85%** | **"MATCHED OR BEAT THE BEST BOT OBSERVED; pre-registered target not met."** The word **"failed" is FORBIDDEN** in this range. |
| **50.4% – 67.6%** | improved over baseline, below every comparator — a partial result, stated as one. |
| **≤ 50.4%** | the intervention did not move the mechanism. |

**And a caveat that must travel with the 67.6% comparator: Askar is a WEAKER
EXEMPLAR than the headline implied.** Conditioning on in-range sentinels only,
**ours face the core 90.1% / 88.9%; Askar's only 80.7%** — a fifth of their
in-range sentinels are deliberately pointed away, consistent with aiming at
approaching bodies. **Deriving our standard from them was borrowing from a
different objective.**

## 1d. THE EDIT ATTACKS THE RIGHT VARIABLE — and this is why

**Our deficit is almost entirely RANGE: 44.1% of our sentinels are out of reach,
and the ones in reach are aimed correctly** (90.1%), because `raid.py` already
builds with `facing = bp.direction_to(target)` behind a `can_fire_from` gate.
**Askar's deficit is mostly FACING.**

**Closest-first, tie-broken by coverage, is a RANGE fix — and range is where our
loss is.** The plank is better aimed than its own justification was.

## 1e. A LOAD-BEARING PROPERTY OF THE PRIMARY, NEWLY ESTABLISHED

Across 120 replays, gunner ids were re-emitted with a **changed direction 2,393
times**; sentinel ids were re-emitted **0 times across 322 sentinels**. The field
mutates for exactly the type with `rotate()` and never for the one without.
**⇒ For a sentinel, built facing IS its facing for life. "Shootable-on-build" is
PERMANENT, not a decaying snapshot** — which is what makes it a legitimate
primary rather than a moment-in-time proxy. Nobody had established this.

## 1f. A FIGURE IN THE BODY DOES NOT REPRODUCE

Line 29 gives Askar's own median nearest-footprint d² as **18**. Re-derivation
gets **13** nearest-footprint and **17** anchor-basis — **so the anchor basis
leaked into one cell of a table declared as nearest-footprint.** Every other cell
in all three columns reproduces to the digit. **Corrected to 13.** Cosmetic for
the rates; it is still an error inside a pre-registration and is recorded rather
than edited away.

## 1g. LIMITS THAT REMAIN, stated so they are not discovered at read-out

1. **`can_fire_from` semantics are replicated as pure geometry only** (d²≤32 +
   collinear). Sentinel shots ignore obstacles, but the engine was not read to
   rule out a further predicate (minimum range, first-entity stop). **If one
   exists, TRUE is still an upper bound by an unmeasured amount.**
2. **The 67.6% comparator rests on ONE opponent.** Ouroboros builds **zero**
   sentinels across all 195 games — independently corroborating the autopsy —
   so no third comparator exists.
3. **On-build, not on-kill.** Neither figure says a shootable sentinel ever
   fired at the core or did damage. The currency bar remains the currency bar.
