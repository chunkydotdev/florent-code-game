# Wave 4 — SIEGE-PLANT CROSS-CHECK

Research session 2026-08-07, wave 4 of the day's replay research. Read-only: no repo
edits, no `fcode run/submit/activate/unrated/test`, no new downloads — every replay
below was already in `SCRATCH/replay_cache/replays/`. Toolkit: `replay_lib.py` +
`siege_geometry.py` (see thread 6, `thread6_barrier_geometry.md`, for the threat
model being cross-checked here). Scripts: `wave4_crosscheck.py` (extraction),
`wave4_aggregate.py` (stats). Raw per-plant data: `wave4_raw.json`.

## 0. Sample

**43 games** decoded: every cached OUR-loss replay vs the five named nemeses
(Lunds Stallions, CtrlAltDefeat, Orizon, Ouroboros, Powerpuff Girls), plus **7
kladde-adjacent third-party games** from thread 3's master table (kladde vs Erebus /
not adgato / Besvikomat / Landers / O(1) — kladde never faces us, so the **sieged
team's core** is used as the victim reference in each of those 7, resolved from
`match_info`'s actual per-game `winnerSide`, not assumed). One kladde game
(`225f2360 g5`, jackpot) ended `titanium_collected` with no core death, so both
seats were scored independently (labelled `kladde=victim` / `kladde=besieger` and
folded into those two buckets below).

**Geometry note:** rather than trusting `maps/*.map26` to be byte-identical to what
was actually played, the threat model was rebuilt from **each replay's own tile
grid and core positions** (`ReplayMapAdapter` in `wave4_crosscheck.py`) and then
cross-checked against the static map file for all 13 map names touched — **13/13
exact match** (tiles, dimensions, both core NW corners). The static maps are
confirmed identical to what ladder actually plays.

**721 enemy gunner/sentinel build events** extracted (genuinely-new builds only —
`replay_lib` already routes gunner `rotate()` re-emits to `.entity_updates`, not
`.builds`, so no rotation-inflation risk here). Spot-checked against
`entity_census()`: Ouroboros's 34-gunner game (`d0116d59 g3`, drumlin) matches
`entity_census(r)['A']['built']['gunner'] == 34` exactly.

**175 of the 721 were core-damaging** (dealt confirmed >0 damage to the victim's
core per `damage_log(team=besieger, target_kind="core")`, attributed by entity id
back to the specific build event — friendly fire structurally excluded since the
filter requires `source_team == besieger, target_team == victim`).

## 1. Per-nemesis table

`n_plants` = all enemy gunner/sentinel builds. `in_threat%` = share of **all**
plants inside the union of `sentinel_threat`/`gunner_threat` (i.e. geometrically
*capable* of ever hitting the core, any range). `coredmg` = plants that actually
landed core damage. `coredmg_in_threat%` = coverage metric (a). `not_aligned` =
plants that can NEVER hit the core regardless of range (fails the 8-ray alignment
test outright — economy/picket turrets, metric (c)).

| bucket | games | maps | n_plants | in_threat% (all) | n_coredmg | coredmg_in_threat% | not_aligned | fp_dsq range (all) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Lunds Stallions | 9 | antler, eider, heart, hive, jackpot, lighthouse, saga | 72 | 30.6% | 13 | **100%** | 30 | 1–514 |
| CtrlAltDefeat | 2 | drumlin, heart | 35 | 34.3% | 9 | **100%** | 10 | 1–425 |
| Orizon | 7 | drumlin, eider, fjordgate, hive, jackpot, lighthouse, snowflake | 60 | 66.7% | 27 | **100%** | 15 | 1–613 |
| Ouroboros | 13 | antler, atoll, drumlin, eider, heart, hive, jackpot, nordkap, saga, snowflake | 268 | 16.4% | 15 | **100%** | 174 | 1–530 |
| Powerpuff Girls | 4 | drumlin, fjordgate, hive, saga | 65 | 21.5% | 8 | **100%** | 33 | 1–485 |
| kladde-adj (kladde=besieger) | 4 | eider, jackpot, meander, saga | 103 | 67.0% | 63 | **100%** | 20 | 5–452 |
| kladde-adj (kladde=victim) | 4 | drumlin, hive, jackpot, meander | 118 | 62.7% | 40 | **100%** | 36 | 1–313 |
| **TOTAL** | **43** | 13 map names | **721** | **38.1%** | **175** | **100.0%** | **318** | 1–613 |

Gunner-only threat tiles (in `gunner_threat` but not `sentinel_threat`) landed
**zero** observed core-damaging or non-core-damaging plants across all 721 — matches
thread 6 §3's finding that the gunner set is a strict subset of the sentinel set on
every map; there is still exactly one geometry to defend.

## 2. (a) Coverage: does the threat model catch every plant that actually hit the core?

**175 / 175 = 100.0%.** Every single core-damaging enemy turret in the sample sits
inside the computed `sentinel_threat ∪ gunner_threat` set for its map and seat.
**Zero misses.** This holds independently in every one of the 7 buckets above (each
is 100%), across 13 of the 15 catalogued maps and both directions of the kladde
matches (kladde as besieger and as victim) — the strongest form of validation
available from this sample: not one counter-example.

Sanity cross-check built into the same result: the **maximum `fp_dsq` among all 175
core-damaging plants is 25** (never exceeds the sentinel's `r²=32` ceiling — this
follows from the game engine's own firing rule, so it is really validating that the
alignment/distance arithmetic in `siege_geometry.py` matches the engine's actual
line-of-fire test, not an independent finding about strategy).

## 3. (b) `fp_dsq` distribution: actual plants vs. the theoretical 5–32 band

All 721 plants (both threatening and not):

| range | count | % |
| --- | --- | --- |
| `fp_dsq` < 5 | 78 | 10.8% |
| `fp_dsq` in [5, 32] (the claimed band) | 271 | 37.6% |
| `fp_dsq` > 32 | 372 | 51.6% |

Histogram: `0-2: 33, 3-8: 78, 9-16: 78, 17-32: 160, 33-50: 67, 51+: 305`.

The **175 core-damaging plants only**:

| range | count | % |
| --- | --- | --- |
| `fp_dsq` < 5 | 59 | **33.7%** |
| `fp_dsq` in [5, 32] | 116 | 66.3% |
| `fp_dsq` > 32 | 0 | 0.0% |

Two things worth flagging against the "5–32" framing:

1. **A full third of real core damage (59/175) comes from `fp_dsq` < 5** — i.e. the
   d=1/d=2 shell (the core's 8 orthogonal input tiles and their diagonal neighbours)
   that thread 6 §3 already called out as "free" denial if the economy is wired.
   Lowest observed: `fp_dsq=1` (adjacent-to-footprint), e.g. Ouroboros
   `d0116d59 g3` drumlin r415, gunner at (18,20), 462 dmg dealt over the game;
   CtrlAltDefeat `a5671738 g1` drumlin r338, gunner at (4,5), 403 dmg. A denial
   scheme that only covers `fp_dsq 5-32` would miss a third of observed damage —
   but this isn't a gap in thread 6's own recommendation, which explicitly prices
   the d=1/d=2 ring separately (§3, "36 Ti... already ours if the economy is
   wired") rather than folding it into the mid-band.
2. **51.6% of all plants sit outside `fp_dsq 32` entirely** and — consistent with
   (a) — **zero of them ever damaged the core.** These are structurally incapable
   by range alone, before alignment is even considered.
3. Highest observed core-damaging `fp_dsq` = 25, from kladde-as-besieger's sentinel
   sieges (`c23600fc g3` eider, `73624f1b g1` saga) — sentinels dealing 684–1512
   damage each from the outer shell of the threat set, consistent with thread 6's
   claim that sentinels, not gunners, own the outer ring (unblockable by walls).

By turret type, of the 175 core-damaging plants: **91 gunner / 84 sentinel** — but
of the *builds*, gunners outnumber sentinels 588:133 overall. Conversion rate:
gunner builds land core damage **15.5%** of the time, sentinel builds **63.2%** of
the time — over 4x higher hit-conversion per sentinel plant, consistent with the
sentinel's unblockable ray being the structurally dominant threat.

## 4. (c) Non-core-aligned plants (economy-sniping / picket turrets)

**318 / 721 (44.1%)** of all enemy turret builds are **not ray-aligned with any core
footprint tile at all** — they cannot hit the core under any facing, at any range.
A further **128 (17.8%)** are aligned but sit at `fp_dsq > 32`, past even the
sentinel's ceiling — also structurally incapable. Combined, **446 / 721 (61.9%)** of
all observed enemy turret plants in loss games **could never have threatened the
core**, regardless of enemy intent.

Zero of the 318 non-aligned plants dealt any core damage (as physics requires) —
confirms the extraction pipeline and the alignment test agree with ground truth.

Ouroboros is the extreme case: 268 total gunner/sentinel builds across 13 games but
only 44 (16.4%) ever geometrically threaten the core and only 15 landed damage — the
bulk (174 non-aligned, 65%) are picket/harvester-defense turrets scattered off any
core ray. This is direct evidence for thread 6 §6/§7's "reactive beats prophylactic"
conclusion: most of what a real opponent builds isn't a core siege at all, so a
static prophylactic ring denying the *geometric* threat set would be paying to deny
tiles the opponent mostly doesn't use, while doing nothing about the picket turrets
that dominate build volume.

## 5. (d) The HUNT_BAND_DSQ=41 question

**First, a correction to the premise.** `bots/_v72e2/main.py:1543` reads:

```python
if min(t.distance_squared(bp) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
```

`core_tiles(self.core)` (line 432-433) expands the NW-corner anchor `self.core` to
**all 4 footprint tiles** and the comparison takes the **min** — this is exactly
thread 6's `fp_dsq` (nearest-footprint distance), **not** a bare NW-corner distance.
The in-code comment at that call site confirms it: *"measured to the nearest tile of
the 2x2 footprint."* So the shipped code is already using the fp_dsq convention, not
the nw_dsq convention the task description attributed to it.

Both are reported below for completeness, since the task asked for `nw_dsq`
specifically:

| metric | plants > 41 | / core-damaging total | % |
| --- | --- | --- | --- |
| `nw_dsq` > 41 | **0** | 175 | 0.0% |
| `fp_dsq` > 41 (the actual coded metric) | **0** | 175 | 0.0% |

**Zero core-damaging plants exceed 41 by either convention, in this 43-game / 13-map
sample.** The maximum observed `nw_dsq` among all 175 core-damaging plants is
**exactly 41** — one plant sits right at the current boundary: kladde-as-victim,
`69a0c821 g4` (hive, kladde on side A), a sentinel built round 52 at tile `(7,24)`,
`fp_dsq=25 / nw_dsq=41`, dealt 126 core damage over the game. Everything else is
comfortably inside. Max `fp_dsq` among core-damaging plants is 25 (7 below the
`fp_dsq` cut, 16 below the `nw_dsq` cut).

**Evidence reading:** in this sample, **HUNT_BAND_DSQ=41 has not been observed to
miss a single actual core-damaging plant**, on 13 of the 15 catalogued maps
(archipelago and moonrise absent from the cache — no cached loss touches them). This
is supportive but not dispositive: n=175 is a sample of what got *built and fired
successfully*, not an exhaustive census of every geometrically-legal `fp_dsq 33-32..50`
tile a smarter or differently-configured opponent could plant on — thread 6 §2 notes
the true `sentinel_threat` set reaches `nw_dsq 50` on 10/15 maps, so tiles between 42
and 50 exist and are geometrically live, they are simply **unobserved** in this
particular loss sample, not proven safe. Recommend: leave the constant where it is:
the evidence supports it, but "0 misses in 175 samples, mostly against 5 opponents"
is not strong enough grounds to *raise* it, and there is now a concrete example
(the hive nw_dsq=41 plant) of a real core-killing shot sitting exactly at the
boundary.

## 6. Verdict

Thread 6's threat-set geometry — ray alignment to a core footprint tile plus the
turret's own range (sentinel r²≤32 unblockable, gunner r²≤13 wall-blocked) —
**catches every single core-damaging enemy turret plant observed: 175/175, across
7 buckets, 43 games, 13 maps, zero exceptions.** That is the headline result of this
cross-check: the model is not just theoretically sound (thread 6's geometric proof),
it is empirically complete against real opponent behaviour, including kladde's
deliberate siege play in both directions. The `fp_dsq`/`nw_dsq` band data adds
texture rather than contradiction — a third of real damage comes from the
close-in d≤4 shell thread 6 already prices separately as "free" economy-adjacent
denial, sentinels convert to core damage 4x more often than gunners per build, and
**62% of all observed enemy turret builds in these losses were never core-aligned or
in-range at all** — direct support for thread 6's "reactive beats prophylactic"
conclusion, since a prophylactic ring would spend Ti denying ground that most real
opponents (Ouroboros above all) mostly don't use. On the open HUNT_BAND_DSQ=41
question: 0/175 core-damaging plants exceed it by either distance convention, and
the code already uses the nearest-footprint convention (not NW-corner, contrary to
the question's premise) — the constant has no observed counter-example in this
sample, but the sample doesn't exercise the `nw_dsq 42-50` zone that thread 6's own
full geometric model shows is live on 10/15 maps, so absence of evidence there is
not yet evidence of absence.
