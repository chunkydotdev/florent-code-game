# Thread 5 — Turret-Targeting Idiom Census

**Date:** 2026-08-07 · Read-only replay analysis · No repo edits, no fcode run/submit/activate/unrated/test.

**Question:** does any nemesis's sentinel run the tutorial-idiom bug — "loop `get_attackable_tiles()`,
fire at the first occupied tile" — which (per `docs/game-model.md:263-273`, engine-verified) makes
N/NE/NW/W-facing turrets engage the **farthest** candidate on their line and E/SE/S/SW engage the
**nearest**, because the tile list is absolute row-major (y asc, x asc), not distance-ordered? If so, a
3-Ti bait barrier placed far on that ray should absorb their fire forever.

## Headline finding: the "farthest" signal in raw data is mostly a CORE-PRIORITY confound, not the bug

Every sentinel in this sample that has the *core itself* as a candidate on its ray overwhelmingly
prefers to hit the core (see per-team tables). Because these are forward-siege turrets sitting near
the enemy core, the core is very often *geometrically* the farthest candidate on the ray too — so
"chooses farthest" and "chooses core" are almost perfectly collinear in the raw data and cannot be
told apart without splitting on candidate composition.

**Once core-containing candidate sets are excluded, the clean facing-correlated near/far signature
the brief hypothesized does not survive for any of the 5 nemeses at usable sample size.** This is the
central, load-bearing result of this census — see the core-free breakdown in each team's section.
Two further methodology notes that materially changed the numbers versus a naive first pass, kept here
because they explain why raw counts and this report's "n" disagree so much:

1. **Raw shot counts wildly overstate independent evidence.** Sentinels reload every 2 rounds and, in
   this data, keep re-engaging the same target for as long as it (or its replacement on the same tile)
   remains the top pick — e.g. Lunds Stallions turret `#34` fires 185 times at facing NORTH across
   `c00e6c30_g4_antler` but that collapses to **15 distinct targeting decisions** once consecutive
   repeats of the same chosen entity are merged. All classification below uses **distinct decisions**
   (a shot counts as a new decision only when the chosen entity id differs from this shooter's
   immediately preceding pick); raw shot totals are reported alongside only as practical
   "how much fire does this generate" context.
2. **"Chosen" is resolved via the replay's own damage attribution (`HpEvent.target_id`), not by
   matching the fired-at tile to a candidate.** Builder Bots can stand on buildings (README trap #11),
   so a tile can hold two entities; the library's `_attribute()` pass already reconciles this exactly
   (100% attribution, ammo-conservation self-check passes on all games used — see per-game
   `check_ammo()`/`check_delivery()` output, all PASS). Guessing from tile alone mis-resolved a small
   number of co-located shots in an earlier pass of this script.

**Toolkit note (own methodology bug found and fixed during this thread, not in `replay_lib.py`):**
a Core's 2×2 footprint intersects a straight ray at up to 2 tiles, so the same core entity can appear
as two different-distance "candidates." Nearest/farthest classification dedupes by entity id (keeping
its nearest occurrence); row-major-first classification correctly keeps both footprint tiles as
separate list entries, since that is what `get_attackable_tiles()` would actually enumerate.

## Data sources (all read via `replay_lib.py`, self-checks PASS: delivery×10==titaniumCollected,
ammo converted−spent==final, 100% damage attribution, no unknown fields, on every file below)

| nemesis | games | source | downloaded this thread |
| --- | --- | --- | --- |
| Lunds Stallions | `c00e6c30_g4` (antler, 391r), `c2e57b46_g2` (lighthouse, 189r), `c2e57b46_g5` (heart, 160r) | scratch cache | g4, g2, g5 (g3/g4-other already cached) |
| CtrlAltDefeat | `a5671738_g1` (drumlin, 398r), `a5671738_g4` (heart, 501r) | scratch cache | g1 (g4 was already cached) |
| Powerpuff Girls | `12df1f45_g1` (saga, 1000r), `g2` (fjordgate, 259r), `g3` (drumlin, 1000r), `g5` (hive, 318r) | scratch cache | g2, g5 (g1/g3 already cached, included per brief) |
| Flotte (`The Flotte Experience`) | `73afd924` g1-g5 (28x20/770r, 10x10/218r, 18x18/190r, 24x24/156r, 26x26/152r) | repo `replay_archive/`, match `sporks` vs Flotte (not an OpenSverige game — see caveat below) | none, already archived |
| kladde (`kladde chatte tville (och oss)`) | `225f2360` g2 (meander)/g5 (jackpot), `691f2554` g1 (meander)/g3 (hive)/g5 (eider), `69a0c821` g4 (hive), `f0c33e9e` g1 (jackpot) | scratch cache, **cached by the thread-3 agent**, mapped here via `match_info` team names (`grep -l kladde replay_cache/match_info/*.json`) | **none — per instruction, no additional kladde games downloaded** |

**Flotte caveat:** the only cached Flotte match in `replay_archive/` (`73afd924`) is `sporks` vs
`The Flotte Experience`, not an OpenSverige game. The idiom is a property of Flotte's own bot code,
not of the opponent, so this should generalize — but it means the candidate pool being shot at is
`sporks`'s units, not ours, and is noted as provenance, not treated as equivalent to a direct read.

Total sentinel Fire events inspected: **1423** (Lunds 253, CtrlAltDefeat 59, Powerpuff 91, Flotte 121,
kladde 899 — kladde's raw count is far larger because these 7 games include two long, heavily-sieged
matches, `225f2360_g5_jackpot` at 384 fires and `f0c33e9e_g1_jackpot` at 165). Data quality: every
shot has a resolvable shooter (`unresolved=0` for all 5 teams — no shots dropped for missing
shooter/direction). Separately, the ground-truth target (`HpEvent.target_id`) could not be placed on
the reconstructed ray at either snapshot round for a handful of shots — Lunds 3/253, kladde 13/899,
all others 0 — most likely a target that died the same round it was hit and dropped out of both the
pre- and post-round position snapshots; these are excluded from candidate-set classification (kept in
raw fire totals). Friendly fire was seen once, in Flotte's data, excluded from classification.

## Per-team results

Facings are grouped by the brief's prediction: **far-predicted** = N, NE, NW, W; **near-predicted** =
E, SE, S, SW. "Pick" is relative to the candidate set present at that decision (nearest / farthest /
middle of 3+). "RMF" = chosen entity was the row-major-first occupied tile on the ray (the literal
"first occupied tile in `get_attackable_tiles()`" the bait hypothesis needs).

### Lunds Stallions — n=21 distinct decisions (228 raw shots)

| | core-present | core-free |
| --- | --- | --- |
| n | 17 | 4 |
| core chosen when present | 7/17 (41%) | — |
| pick distribution | mixed | far-facings only: 1 near, 2 far, 1 mid |
| RMF agreement | — | 2/4 |

All 21 decisions were on far-predicted facings (NORTH n=13, NORTHWEST n=3, WEST n=5 — decisions,
not shots); zero near-predicted-facing multi-candidate decisions were observed in this sample, so the
near side of the prediction is completely untested for Lunds. Within far-predicted facings the pick
distribution is nearest=4, farthest=8, middle=9 (see raw JSON). Neither "always farthest" (38%) nor
"always nearest" (19%) nor row-major-first (2/4 core-free, coin flip) describes this team. Concrete
example of the confound: shooter id `#34` at `c00e6c30_g4_antler`
faces NORTH into its own line of our conveyor(d²=4)/builder(d²=9)/core(d²=16,25); it alternates among
all three as our units die and respawn (rounds 20-216), which is exactly why raw shot counts (185 on
this one shooter alone) collapse to only 15 real decisions.

**Classification: INDETERMINATE / MIXED.** n too small and too noisy to fit absolute-enumeration,
geometric-nearest, or a clean priority table.
**Bait-barrier verdict: NOT supported by current evidence (n=21, core-free n=4).**

### CtrlAltDefeat — n=2 distinct decisions (37 raw multi-candidate shots, 59 total sentinel fires)

Both decisions chose the core: shooter `#971` r456 (`a5671738_g4_heart`, NORTHWEST, core d²=8 vs.
a live sentinel of ours at d²=2 — core was NOT nearest, chosen anyway) and shooter `#1012` r473
(same game, SOUTH, core d²=25 vs. our conveyor at d²=16). **core_chosen = 2/2.** Zero core-free
decisions exist in this sample — we have no data at all on how this bot picks among non-core targets.

**Classification: INDETERMINATE, n far too small (2).** The 2/2 core-preference is suggestive but not
a sample; cannot confirm or rule out absolute-enumeration, since every observed decision is confounded
by core-priority and core-free behavior was never observed.
**Bait-barrier verdict: UNKNOWN (n=2).**

### Powerpuff Girls — n=14 distinct decisions (80 raw shots)

| | core-present | core-free |
| --- | --- | --- |
| n | 5 | 9 |
| core chosen when present | 5/5 (100%) | — |
| pick distribution (core-free) | — | nearest 4, farthest 3, middle 2 |
| RMF (core-free) | — | 4/9 |

Core-free decisions are all on **near-predicted** facings (EAST, SOUTH, SOUTHEAST) — the single
far-predicted (NORTHEAST) decision had the core present, so far-predicted-facing behavior is
untested once core is excluded. Core-free near-predicted split (4 near / 3 far / 2 mid, n=9) is
close to a coin flip, not the 100%-ish signature the raw EAST data (24/32 raw shots nearest)
suggested before dedup and before removing core-driven shots. Example: shooter `#172`/`#181`/`#283`
(`12df1f45_g2_fjordgate`) face EAST with the enemy core at d²=1 or d²=4 — always nearest AND always
core, textbook confound.

**Classification: INDETERMINATE, weak/no signal once core is removed (core-free n=9, near-predicted
only).** The apparent EAST/NORTHEAST clean split in raw data is explained by "always hit the core,"
not by facing-dependent ray-scan order.
**Bait-barrier verdict: NOT supported by current evidence for the far-predicted facings that would
matter (0 core-free far-facing decisions observed).**

### Flotte — n=29 distinct decisions (57 raw shots)

| | core-present | core-free |
| --- | --- | --- |
| n | 29 (100% of decisions) | 0 |
| core chosen when present | **0/29 (0%)** | — |

Flotte is the one team where core-priority does **not** explain the pattern — quite the opposite:
the core is a candidate in every single multi-candidate decision observed (it's always geometrically
present given these are close-quarters siege turrets) and is **never** chosen, even when it is the
sole "farthest" option. This rules out geometric-farthest and rules out core-priority; it is
consistent with either geometric-nearest or "row-major-first among non-core-type candidates."

- **SOUTHWEST** (near-predicted): n=22, **100% nearest** — clean, e.g. shooter `#524`
  (`73afd924_g1`) hits the nearest conveyor at d²=8 or d²=18 across 17 separate re-targets (the
  conveyor dies and is rebuilt by the opponent on the same tile repeatedly, each one a fresh,
  independent decision, not a lock-on artifact — see raw JSON for the id list). Shooter `#418`
  (`73afd924_g5`) repeats the pattern, n=6.
- **WEST** (far-predicted): n=6 (all one shooter, `#204` in `73afd924_g3`), **0/6 farthest** —
  directly contradicts the far-prediction. Picks split nearest (2, d²=9) / middle (4, d²=16), toggling
  between them as the near tile's occupant (a conveyor) is destroyed and rebuilt, never touching the
  core at d²=25 that is present throughout every one of these 6 decisions. This doesn't fit
  "row-major-first among non-core candidates" cleanly either (that would predict the same one of
  {9,16} every time for a fixed facing, not a toggle) — unresolved anomaly, most likely explained by
  the near tile's occupant intermittently not existing between the reload window and the retarget
  snapshot. n=6, one shooter only — do not over-read.
- **NORTHWEST**: n=1, indeterminate alone.
- Far-predicted facings combined (WEST + NORTHWEST): n=7, 0/7 farthest, 3 nearest, 4 middle.

**Classification: partial evidence for geometric-nearest / "never targets core," clean on SW
(n=22) but the single far-predicted facing tested (WEST, n=7) directly contradicts the
absolute-enumeration far-prediction.**
**Bait-barrier verdict: NOT VIABLE as specified (far-bait requires a far-facing preference we did not
observe — WEST facing shows 0/7 farthest). A different exploit is suggested instead: Flotte's
sentinels structurally will not finish off a core while any other candidate sits on the same ray —
worth a separate, non-bait investigation if useful.**

### kladde chatte tville (och oss) — n=82 distinct decisions (441 raw multi-candidate shots, 899 total sentinel fires, by far the largest sample)

| | core-present | core-free |
| --- | --- | --- |
| n | 55 | 27 |
| core chosen when present | 48/55 (87%) | — |
| pick distribution (core-free) | — | nearest 18, middle 3, farthest 6 |
| RMF, all decisions | 60/82 (73%) | 13/27 (48%, coin flip) |
| core-free by prediction | — | near-facings n=8 (7 near/1 far); far-facings n=19 (11 near/5 far/3 mid) |

This is the team where the raw-data "far bias" looked strongest before deconfounding: WEST facing
alone has **58 distinct decisions with 45 chosen farthest (78%)**, and overall RMF
agreement across all 82 decisions is 73% — the best fit for absolute-enumeration in the whole census
at face value. **But 55/82 of those decisions have the core present, and it is chosen 87% of the
time** (e.g. WEST-facing core_present=47/58, core_chosen=42/47). Once core-containing decisions are
excluded (27 remain, the actual test of the ray-scan-order hypothesis): RMF agreement drops to a coin
flip (48%), and the pick distribution actually **leans nearest even on far-predicted facings**
(11 nearest vs 5 farthest, n=19) — the opposite of the predicted direction. Near-predicted facings
core-free (n=8) do lean nearest (7/8, 88%), but that's the "obvious" direction anyway and doesn't
distinguish absolute-enumeration from geometric-nearest.

**Classification: PRIORITY-TABLE (core-first) with a probable geometric-nearest fallback, NOT
absolute-enumeration.** The clean-looking WEST/RMF signal is a core-priority + siege-geometry
confound, not the row-major-order bug. Confidence is the highest in this census (n=82 total, n=27
core-free) precisely because it's the largest sample, and that size is what let the confound surface
in the first place — smaller-n teams above may have the identical confound undetected.
**Bait-barrier verdict: NOT VIABLE.** A far bait would only intercept the 13% of core-present shots
where kladde doesn't already hit the core, and does nothing for the majority pattern (hit the core
directly) or for the core-free fallback (leans nearest, not far).

## Secondary, lower-confidence pass: gunner rotation direction choice

This tests a **different** decision (which of 8 facings to rotate to when multiple opposing entities
are visible within r²≤13) than the sentinel near/far bug, and a gunner's shot physically stops at the
first blocking tile regardless of aim — so even if a rotation "mis-aims," the shot's own physics, not
list-scan order, decides who gets hit. Reported for completeness only; does not bear on the bait
hypothesis.

| team | rotation moments with ≥2 visible opposing entities | new facing aligned to *any* visible target | new facing aligned to the *nearest* visible target |
| --- | --- | --- | --- |
| Lunds Stallions | 25 | 16 (64%) | 11 (44%) |
| CtrlAltDefeat | 20 | 20 (100%) | 4 (20%) |
| Powerpuff Girls | 39 | 23 (59%) | 16 (41%) |
| Flotte | 108 | 100 (93%) | 52 (48%) |
| kladde | (not separately tabulated — see raw JSON `gunner_rotations.kladde`; low rotation counts, see per-game table below) |

No team shows a clean "always rotate toward nearest" pattern; CtrlAltDefeat always rotates toward
*some* visible target (100%) but rarely the nearest one (20%) — mildly interesting, not pursued
further given the physics caveat above.

## Bottom line

| nemesis | n (distinct decisions / raw multi-candidate shots / total sentinel fires) | classification | bait-barrier verdict |
| --- | --- | --- | --- |
| Lunds Stallions | 21 / 228 / 253 | indeterminate / mixed | NOT supported |
| CtrlAltDefeat | 2 / 37 / 59 | indeterminate, n too small | UNKNOWN (n=2) |
| Powerpuff Girls | 14 / 80 / 91 | indeterminate, weak signal | NOT supported |
| Flotte | 29 / 57 / 121 | partial geometric-nearest, never-targets-core; far-facing test contradicts prediction | NOT VIABLE as specified |
| kladde | 82 / 441 / 899 | priority-table (core-first) + geometric-nearest fallback | NOT VIABLE |

**No nemesis in this census shows clean, deconfounded evidence of the absolute-enumeration
"first-occupied-tile" bug the bait-barrier strategy depends on.** The engine mechanism itself
(`get_attackable_tiles()` is absolute row-major, verified in `docs/game-model.md`) is real and not in
question — what this census tested is whether these 5 opponents' bot code actually falls into that
trap, and at the sample sizes available, none of them do cleanly. The dominant real pattern instead is
core-priority: four of five nemeses hit the core whenever it's a legal candidate (CtrlAltDefeat 2/2,
Powerpuff 5/5, kladde 48/55); Flotte is the outlier that structurally avoids the core when any other
target shares its ray, which is a different, real, and possibly more useful finding than the one this
thread went looking for, but is not "bait absorbs their fire" — it's "they won't finish the kill shot
while distracted," worth a separate write-up if this line is pursued further.

## Raw data

Full per-shot records (candidates, chosen id, facing, round, ids) for every sentinel Fire and gunner
rotation analyzed: `SCRATCH/thread5/turret_census_raw.json`. Analysis script:
`SCRATCH/thread5/analyze_turret_targeting.py` (re-runnable, prints per-game counts to stderr).
