# LIVELOCK-SIGNATURE DISCRIMINATOR — DISEASE-PREVALENCE vs AREA, 2026-08-14T16:1xZ

**Pipeline NEXT-2.** Question: MAPCODE (`_v197mapcode` vs `_v187saltidle_f`/v123,
local screen, n=5,400) reads **93.7% on eight new-pool maps, 53.0% on
frostgate+royale** (coordination.md 15:2x blocks, `SEGMENT-SWEEP-2026-08-14.md`
lines 107-118, cross-verified below against the raw TSV). Two stories compete:
**(A) DISEASE-PREVALENCE** — v123's pathfinding livelock (no `MAP_CODES` entry
→ greedy dominant-axis pathing → wall-pocket lock) simply didn't fire much on
frostgate/royale, so the fix had nothing to fix there. **(B) AREA** — both weak
maps are 20×20=400 and something about small-area geometry caps the fix's
value regardless of disease. This report measures the disease **directly**, in
**v123's own games**, per map, and decides between them.

## THE INDICATOR — two operationalizations, one ground truth

The "0/14 signature" (SHIP-mapcode-2026-08-13.md, PREREG-mapcode-live-2026-08-13.md):
a livelocked builder tree shows **zero (or near-zero) harvesters built** and
**near-zero build/action events** — measured on the verified vs-starter runs at
**9 builder actions in 1,000 rounds, 98.7% of moves immediate reversals**,
killing at turns **71 (midgard) / 115 (ragnarok) / 86 (yulerune)**. Two
independent channels operationalize this on v123's actual games:

**Indicator D (direct, small-N, ground-truth-grade).** `corpus/join.tsv`
(ourver=123, 65 archived platform games decoded to real replay files) joined
to `corpus/build_agg.tsv` on `file`+`team`=`our_team`, summing `build_harvester`
across all bands for total harvesters built, and summing all `build_*` +
`batk` metrics for total build/attack actions. `DISEASE_D := harvesters==0`
(the literal 0/14 reading); a softer `harvesters<=1` cell reported alongside.
**This is the only channel with true per-round build events; it is also the
thinnest — 65 games total, 2 each on frostgate/royale, 0 on ragnarok.**

**Indicator P (proxy, large-N, self-play).** `scratchpad/overnight/MAPCODE.tsv`
(the MAPCODE screen itself, n=5,400, ~288 games/map, winner/cond/turns only —
no build events). Among v123's **lost** games on a map: `DISEASE_P := (cond ==
core_destroyed AND turns<=150) OR (cond == tiebreak)` — a defenceless economy
either gets rushed down fast (71-115-turn ground truth, comfortably under the
150 threshold) or survives to r1000 with nothing to show for it. **This channel
is well-powered (n=133-289/map) but not perfectly specific** — see the legacy
calibration below.

## VALIDATION CELL — both indicators, both directions

| indicator | case | expected | observed |
|---|---|---|---|
| D | valkyrie archived game, file `…replay26`: harv=0, 18 total actions, turns=1000, cond=`titanium_collected` (a full-length game with no economy — the "draws r1000" form of the signature) | POSITIVE | **harv==0 → fires.** Order-of-magnitude matches the ground-truth 9 actions/1000 rounds. |
| D | drumlin archived game: harv=16, 253 actions, turns=496, won | NEGATIVE | **harv=16 → does not fire.** |
| D | icefloe archived games (STRONG-side new-pool map): harv 2/4/4/5/6, actions 50-193 | NEGATIVE (indicator must not fire on every new-pool game indiscriminately) | **0/5 fire under harv==0.** Confirms the indicator discriminates rather than blanket-triggering on "new pool." |
| P | ground-truth kills at turns 71/86/115 (midgard/yulerune/ragnarok vs starter) | POSITIVE | **All three < 150 → fire by construction.** |
| P | same valkyrie archived game as above (turns=1000, cond=tiebreak) | POSITIVE | **Fires — cross-validates against Indicator D on the same real game.** |
| P | same fjordgate archived disease-positive game (harv=0, turns=104, cond=core_destroyed) | POSITIVE | **turns<=150 → fires — second cross-validation against D.** |
| P | midgard archived game: harv=12 (healthy, D says clean), turns=437, cond=core_destroyed | NEGATIVE | **turns>150, not tiebreak → does not fire.** Agrees with D on the same game. |

Both indicators drive positive and negative correctly on known cases, and the
two channels **agree with each other** on the three archived games checked
against both (a real cross-validation, not a coincidence of design). D and P
are answering related but not identical questions (raw game-count ground truth
vs. self-play loss-shape at scale) — used together below.

## CALIBRATION — indicator P has a non-trivial false-positive floor

Legacy maps (both trees have live `MAP_CODES` entries — **no livelock
mechanism possible for either side**) still read Indicator P at
**antler 20.1%, drumlin 21.9%, nordkap 27.3%, fjordgate 34.8%, archipelago
55.6% — pooled 32.1% @703.** Ordinary rush-kill and tiebreak patterns occur on
their own; per-map heterogeneity in this baseline is real and as wide as
20-56pp. **Any new-pool map's Indicator-P reading is read against this
[20.1%, 55.6%] noise band, not against zero**, before being called "disease."

## PER-MAP DISEASE TABLE — all ten new-pool maps, control tree (v123)

| map | area | T-win% (MAPCODE screen, side) | D: n / harv=0 / harv<=1 | P: n(losses) / disease-on-loss | vs legacy band [20.1,55.6] |
|---|---|---|---|---|---|
| drakkarfjord | 900 | ~100% | 3 / 0 / 0 | 289 / **57.1%** [51.3,62.7] | **ABOVE** |
| midgard | 900 | 100% | 4 / 0 / 0 | 288 / 54.2% [48.4,59.8] | at ceiling |
| ragnarok | 900 | ~100% | **0 / — / —** (data gap) | 287 / 51.2% [45.5,56.9] | within (upper) |
| glacierkeep | 900 | ~82% | 2 / 0 / 0 | 235 / 22.6% [17.7,28.3] | within (⚠ own table defect — see below) |
| valkyrie | 900 | 92% | 6 / 1 / **5** | 265 / 34.3% [28.9,40.2] | within |
| **auroraveil** | **400** | ~93% | 3 / 1 / **3** | 269 / **62.1%** [56.2,67.7] | **ABOVE** |
| **icefloe** | **400** | 84% | 5 / 0 / 0 | 242 / 36.4% [30.6,42.6] | within — ambiguous |
| **yulerune** | **400** | 100% | 1 / 0 / 0 (n=1, uninformative) | 288 / **78.1%** [73.0,82.5] | **ABOVE (highest of all 15 maps)** |
| **frostgate** | **400** | ~46% | 2 / 0 / 0 | 133 / **18.0%** [12.4,25.4] | **BELOW band floor — lowest of all 15 maps** |
| **royale** | **400** | ~60% | 2 / 0 / 0 | 172 / 26.2% [20.2,33.2] | within, near floor |

**⚠ glacierkeep confound, named:** its own `EXTRA_MAP_CODES` entry was itself
wrong at MAPCODE-screen time (center ore cluster missing 4 real ore tiles),
corrected the next day by `_v218mapfix` (`SCREEN-mapfix-2026-08-14.md`). Its
comparatively muted T-win% (82%) and P-rate (22.6%) may reflect the treatment
tree fighting its own bad table there, not less disease in the control. It is
excluded from the decisive test below.

## THE DECISIVE TEST — area held constant, disease still separates

The task's own falsifier: hold area fixed at 400 across all five 400-maps and
ask whether disease still tracks the 93.7%-vs-53.0% split.

**auroraveil + icefloe + yulerune (STRONG, 400-area) pooled Indicator P:
480/799 = 60.1% [56.6, 63.4]**
**frostgate + royale (WEAK, 400-area) pooled Indicator P: 69/305 = 22.6%
[18.3, 27.6]**
**z = 11.13.**

Two of the three (auroraveil 62.1%, yulerune 78.1%) clear the legacy noise
ceiling (55.6%) outright — genuine excess disease, not map-to-map noise —
**on the same 400 area class that frostgate (18.0%, below the noise floor) and
royale (26.2%, at the floor) sit in.** Indicator D corroborates directionally
on auroraveil (1/3 harv=0, 3/3 harv≤1 — the strongest direct read of any
map, tied with valkyrie) while frostgate/royale show 0/2 on both direct cuts.
icefloe (36.4%, within the legacy band) does not independently clear the bar
either way and is read as **underpowered, not contradictory** — its direct-data
n=5 could not distinguish a 0% from a 40% true disease rate.

**Area cannot be the explanation for a gap that persists with area fixed.**
Two of three same-area strong maps show disease clearly in excess of the
disease-free (legacy) baseline; frostgate and royale sit at or below that same
baseline — the two lowest (or near-lowest) Indicator-P readings of all 15
maps in the screen, direct-map or legacy. **Attribution B dies on its own
falsifier, exactly as specified in the task brief.**

## CAVEATS, carried forward

- Indicator D's n is thin everywhere (2-6/map on the weak/mixed maps, **0 for
  ragnarok** — a genuine data gap, not a zero read) and cannot alone resolve
  any single map; it is corroborating, not load-bearing, except where it
  agrees with a well-powered Indicator-P read (auroraveil, valkyrie).
- Indicator P is not perfectly specific (20.1-55.6% base rate on
  disease-impossible legacy maps) — readings inside that band (glacierkeep,
  ragnarok, valkyrie, icefloe) are **not proof of absence**, only "not provably
  present by this test." The verdict rests on the maps that clear the band
  (drakkarfjord, auroraveil, yulerune) against the maps that sit at/under its
  floor (frostgate, royale), which is where area is held constant and the
  contrast is largest.
- This report answers the **pre-fix disease-prevalence question** specifically
  (control tree, v123). It does not re-litigate the separate, already-settled
  ladder cut in `SEGMENT-SWEEP-2026-08-14.md` ("area does nothing within NEW:
  400 55.0% vs 900 55.9%") — that is a **post-fix win-rate** cut on a different
  population (current-era ladder, ourver≥125) and is consistent with, not
  contradicted by, this result.

## VERDICT

**DISEASE-PREVALENCE.** Held area constant at 400 across auroraveil, icefloe,
yulerune, frostgate, royale: disease clears the disease-free baseline on 2 of
3 strong-side maps and stays at/under it on both weak-side maps (z=11.13
pooled), with direct build-event data agreeing wherever it has power
(auroraveil, valkyrie). The parent's livelock did not fire much on
frostgate/royale — the fix had less to fix there — not because 400-area
suppresses the fix's value.
