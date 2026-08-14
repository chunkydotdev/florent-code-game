# SEGMENT SWEEP — map-segment-conditional effects across all historical screens

Written 2026-08-14T15:12:17Z (data-investigation agent, Magnus-authorized Fable tier).

## ⛔ HEADER CAVEAT — READ FIRST

**Everything below is POST-HOC and HYPOTHESIS-GENERATING.** These segments were
cut AFTER the screens ran; every "hit" is a candidate for a pre-registered
segment re-screen (new leg, its own n, its own prereg committed before launch)
and is **never evidence itself**. The multiplicity accounting below says why:
with ~114 comparisons, 2σ hits are expected by chance. The candidates ranked
here clear far higher bars than that, but the rule stands — no hit in this file
ships anything or closes any road.

## Data surfaces and winner encoding

- `scratchpad/overnight/*.tsv` — 126 local shard screens, schema
  `ts shard game map seed seat winner cond turns`.
- `scratchpad/overnight-remote/worker@work-server-1/*.tsv` — 4 remote shards,
  same schema.
- **Winner encoding found: `T` / `C` / `NOWINNER`** — uniform across all 130
  files (local: T=242,474 C=240,435 NOWINNER=32; remote: T=5,208 C=4,329
  NOWINNER=53). No older encodings encountered. NOWINNER rows (85 total,
  0.017%) excluded from all shares.
- Platform: **`corpus/ladder_games.tsv` HAS a `map` column** (used below).
  **`corpus/meta_join.tsv` has NO map column** (columns are file/match/game/
  sides/versions/ratings/scores) — platform read therefore uses ladder only,
  per instructions, no improvised decode.
- Treatment/control identity per shard read from `scratchpad/corefill_work.txt`
  (T = treatment tree, C = control tree; T-share is the treatment's game share).

## Scope limitation that bounds the whole sweep

**71 of ~130 arms have ZERO 900-area games** — every screen fired before the
map-pool change (~2026-08-13) ran on the legacy-only local pool. The entire
GUN\* / BURST\* / LAUNCH\* / CAP\* / AMMO\* / SHIPGATE\* / old-SALT\* record is
**silent on segment structure, not clean on it**. Any segment question about
those families needs a fresh mixed-pool screen; the archive cannot answer it.
The sweep below covers the ~40 arms screened on the mixed pool (5 legacy +
10 new maps).

## Instrument and negative control

z is the pooled-variance two-proportion test, segment vs complement (identical,
via the subset-covariance identity, to (seg − pooled)/SE(diff)). Naive binomial
SEs per the DEFF≈0.98 note.

**Selftest (both directions, per standing practice):** hand-computed case
matches to 4 decimals; planted null reads z=0.000; planted effect reads z=+3.81
and flips sign when arms are swapped; **400 simulated true-null shards pushed
through the full pipeline produced 10 hits at |z|≥2.5 vs 9.9 expected** — the
instrument fires when it must and stays quiet when it must.

**Negative control (true-null shards — byte-identical or null-band pairs:
NULL114, NULL123, NULL125, NULLSALT, NULLHOST, SHIPGATENULL, SR\*NULL):**
6 computable comparisons (the rest are pre-pool-change, no 900 games),
**0 of 6 at |z|≥2, max |z| = 1.96** (NULLHOST lockheavy, n=78 — noise-sized).
The method shows no segment structure where none can exist.

**Positive control, unplanned but decisive:** NEG125 is `_v187saltidle_f` vs
`_v197mapcode` — literally the inverse of the MAPCODE arm — and reads
**z=+18.2 legacy / −11.3 lockheavy, the mirror image of MAPCODE's structure.**
The sweep detects genuinely map-conditional effects at full strength. (NEG
shards are known-worse treatments, not nulls; they are excluded from candidates
and reported here as controls only.)

## Comparison count / multiplicity

- **114 local comparisons run** (arms with both segments populated × 2
  segmentations); **112 valid** (MAPFIX and MAPFIX2 lock-comparisons are
  degenerate — those screens ran valkyrie+glacierkeep only, 1 map per side,
  excluded); **104 valid non-control**. Platform adds 4 (era × segmentation).
- Expected by chance among the 104: **~4.7 at |z|≥2, ~1.3 at |z|≥2.5, ~0.28 at
  |z|≥3. Observed: 15 / 12 / 10.** The excess at 3σ (10 vs 0.28) is not a
  multiplicity artifact; the structure is real. Which hits are *causal* (the
  plank) vs *confounded* (the control tree, the era) is what re-screens decide.

## Ranked candidate table (valid, non-control, |z|≥2, by |z|)

Shares are treatment game-share (T wins / decided games). "Pair" is
treatment vs control tree.

| # | arm | pair (T vs C) | segment | seg share @n | comp share @n | pooled @n | z | class |
|---|-----|----------------|---------|--------------|---------------|-----------|------|-------|
| 1 | MAPCODE | v197mapcode vs v187saltidle_f | legacy | 48.7% @1444 | 85.6% @2884 | 73.3% @4328 | −25.9 | **CLASS2 SEGMENT-DRAG on the shipped plank** |
| 2 | ROUTEONLY | v194routelink vs v178salt | legacy | 38.2% @1212 | 52.3% @2420 | 47.6% @3632 | −8.03 | **CLASS1 RETRO-RESCUE (per-map form, see below)** |
| 3 | SEALFLOOR0 | v219sealfloor0 vs v197mapcode | lockheavy | 47.4% @1077 | 56.6% @4319 | 54.8% @5396 | −5.41 | **CLASS2 SEGMENT-DRAG (remote-replicated)** |
| 4 | IDLEVSALT2 | v187saltidle_f vs v178salt | lockheavy | 47.6% @508 | 59.1% @2037 | 56.8% @2545 | −4.67 | CLASS2 SEGMENT-DRAG |
| 5 | SALTOFF | v199saltoff (salt OFF) vs v197mapcode | legacy | 33.7% @934 | 26.4% @1860 | 28.8% @2794 | +4.03 | mechanism map (removal arm; inverse read) |
| 6 | X3R0V134 | x3r0_v134 benchmark vs v197mapcode | legacy | 45.5% @374 | 56.9% @742 | 53.0% @1116 | −3.61 | opponent-relative: our 900-side weakness vs this benchmark |
| 7 | SEALFLOOR0R (remote) | v219sealfloor0 vs v197mapcode | lockheavy | 49.0% @1068 | 54.8% @4279 | 53.7% @5347 | −3.43 | replicate of #3 |
| 8 | DEST14A | v228dest14a vs v223sealrepair | lockheavy | 40.5% @222 | 53.0% @891 | 50.5% @1113 | −3.32 | borderline CLASS1: non-lock side 52.97% @891 misses the 53-bar by 0.03pp |
| 9 | L4REPAIR2 | v215l4repair vs v197mapcode | lockheavy | 50.7% @1076 | 55.9% @4319 | 54.9% @5395 | −3.12 | CLASS2 (repair-family cluster member) |
| 10 | SEALREPAIR | v223sealrepair vs v218mapfix | lockheavy | 55.8% @908 | 60.6% @3645 | 59.7% @4518 | −2.60 | relative drag only (seg still >50) |
| 11 | SEALREPAIRR (remote) | v223sealrepair vs v218mapfix | lockheavy | 52.0% @660 | 57.5% @2650 | 56.4% @3310 | −2.59 | replicate of #10 |
| 12 | OSCLOCK2 | v224osclock2 vs v218mapfix | legacy | 50.6% @605 | 44.4% @1204 | 46.5% @1809 | +2.47 | weak rescue shape (legacy side doesn't clear 53) |
| 13 | APPRLAUNCH2 | v207apprlaunch vs v197mapcode | lockheavy | 49.4% @1080 | 53.1% @4320 | 52.4% @5400 | −2.23 | weak CLASS2 |

Excluded as degenerate: MAPFIX (+3.94) / MAPFIX2 (+3.38) "lock" rows — these
screens ran only valkyrie (59% / 62% @~1080) vs glacierkeep (52% / 53% @1080),
which is per-map data, not a segment read.

### The headline: MAPCODE decomposed (candidate #1)

The shipped plank's own screen, cut three ways:

- **900-area minus frostgate/royale: 93.7% @2308** (midgard/yulerune/
  drakkarfjord/ragnarok at 100%, auroraveil 93%, valkyrie 92%, icefloe 84%,
  glacierkeep 82%)
- **frostgate+royale: 53.0% @576** (frostgate 46% @288, royale 60% @288) — z
  vs rest = −11.8. **Two of the ten new maps look unfixed by the map-code
  table.**
- **legacy: 48.7% @1444 — the shipped tree LOSES on legacy maps to the very
  bot it displaced** (antler 46%, drumlin 48%, fjordgate 48%, archipelago 50%,
  nordkap 52%).

The platform corroborates both cuts independently (see platform section):
current-era ladder legacy 46.9%, frostgate 44%, royale 48%.

### The per-map rescue: ROUTEONLY (candidate #2)

Pooled 47.6% — read as a fail and deferred ("attribution, not a bar arm").
But **icefloe+drakkarfjord: 77.3% @484 vs 43.0% @3148 on the other 13 maps,
z=+14.0** (icefloe 81% @242, drakkarfjord 73% @242).
**Named confound:** ROUTEONLY shares its control tree (`_v178salt`) with
IDLEVSALT2, whose own icefloe reads 84.1% @170 — so "v178salt is peculiarly
weak on icefloe" fits the same data. The re-screen below is designed to break
exactly this confound (re-base against the current incumbent).

## Mechanism clusters

1. **Seal-FLOOR/REPAIR sub-family drags on lock-heavy maps — 5 arms, all
   negative, two of them independent remote replicates:** SEALFLOOR0 (−5.41),
   SEALFLOOR0R (−3.43), L4REPAIR2 (−3.12), SEALREPAIR (−2.60), SEALREPAIRR
   (−2.59). Meanwhile **SEALFLOOR24 leans the OTHER way on lockheavy (53.4%
   @204, z=+0.97)** — coherent story: **on midgard/ragnarok/valkyrie a seal
   FLOOR > 0 is worth keeping; floor=0 is the drag.** The rest of the seal
   family (SEALFIRST +1.32, MAPSEAL −0.16, MAPSEALX7 +1.21, SEAL139 +0.49) is
   flat, so this is the floor/repair knob, not "seal" wholesale.
2. **The salt plank's value is concentrated on 900-area maps** (inverse read of
   the removal arm SALTOFF, pooled 28.8%): removal costs most on
   frostgate/drakkarfjord/icefloe/ragnarok (removal share 18.5% @744 vs 32.6%
   elsewhere, z=−7.2) and least on legacy (33.7%). Not a gating candidate —
   salt pays everywhere — but it maps where the plank earns.
3. **An icefloe(/drakkarfjord) route-mechanism cluster:** ROUTEONLY 81%/73%,
   IDLEVSALT2 icefloe 84% — both vs the same v178salt control (confound noted
   above), with MAPCODE icefloe 84% vs v187 on a different pair. Carrying-water
   hypothesis: route-link-style behavior is disproportionately strong on the
   two big water/channel maps.
4. Weak leans, recorded not ranked: ECORAID family 4/4 same-sign negative on
   lockheavy (mean z −0.50); OSCLOCK family 2/2 legacy-positive (+0.9, +2.5).

## Platform side (`ladder_games.tsv` — map column exists; per-game `won`)

| era | legacy | 900-area | lockheavy | 900 non-lock |
|-----|--------|----------|-----------|--------------|
| ourver≥125 (mapcode era, 08-13→) | **68/145 = 46.9%** | 158/285 = 55.4% | 48/94 = 51.1% | 110/191 = 57.6% |
| ourver<125 | 1583/3026 = 52.3% | 11/28 = 39.3% | 2/10 | 9/18 | 

(Old era also played 1,376 games on retired-pool maps at 48.8% — outside the
fixed segments. Old-era 900 cells are unreadable, n≤28: the ladder pool only
gained the 900 maps ~08-13, so the era comparison is effectively new-era-only
on that side.)

- **legacy-vs-900 in the current era: z = −1.68** — not 2σ alone at n=430, but
  it is the SAME direction as MAPCODE's local legacy drag (z=−25.9), on a
  different opponent population. Two surfaces, one story: **the shipped bot is
  currently below 50% on legacy maps.**
- Per-900-map, ourver≥125: valkyrie 78% @27, glacierkeep 73% @30, yulerune 72%
  @36 vs **midgard 38% @34, ragnarok 42% @33, frostgate 44% @25, royale 48%
  @25**. Note midgard/ragnarok read 100% in the local MAPCODE screen vs v187 —
  fixed relative to our old self, still losing to the FIELD there. The
  frostgate/royale ladder weakness matches the local unfixed-maps cut exactly.

## THE THREE RE-SCREENS I WOULD FIRE FIRST

Costing basis, measured: local screens run at ~2.7 s/game (AMMO115: 5,408
games in 4h02m), and the runner already supports map-restricted pools (MAPFIX
precedent: 2,160 games on 2 maps). **A 2,700-segment-game leg ≈ 2h0m of one
local lane, zero rated cost.** Each leg gives SE ≈ 0.96pp on a share, i.e.
~±1.9pp at 2σ — enough to separate every effect size below. All three need a
committed prereg (treatment bar + falsifier) before launch, and a grep of the
incumbent first (per standing rule — cheapest null is a feature we already
ship).

1. **LEGACY-GATE THE MAPCODE-ERA REGRESSION.** Segment: legacy-only pool
   (antler/archipelago/drumlin/fjordgate/nordkap). Arms: current incumbent vs
   `_v187saltidle_f` (2,700 games) to confirm the drag on today's tree, then
   the gated variant (v187-era behavior when map ∈ legacy) vs incumbent.
   Expected direction (15a): incumbent <50% in the confirm leg; gated variant
   ≥53% in the treatment leg. This is the biggest prize: the drag sits on the
   SHIPPED plank and the ladder independently reads legacy at 46.9%.
   (Sibling, same family, second window: extend MAP_CODES to frostgate+royale
   — local 53.0% @576 vs 93.7% on the covered eight; ladder 44%/48%.)
2. **SEAL FLOOR >0 ON LOCK-HEAVY MAPS.** Segment: midgard+ragnarok+valkyrie
   only (~900 games/map at 2,700). Arms: sealfloor0 vs sealfloor24 (direct
   knob contrast) on the current chassis. Expected direction: floor24 ≥53% on
   the segment. Backing: 5-arm same-direction cluster incl. two remote
   replicates, plus SEALFLOOR24's opposite lean; also the ladder's two worst
   maps (midgard 38%, ragnarok 42%) sit in this segment.
3. **ROUTELINK REBASED, ICEFLOE+DRAKKARFJORD ONLY.** Segment: icefloe+
   drakkarfjord (~1,350 games/map at 2,700). Arms: route-link mechanism ported
   onto the current incumbent vs current incumbent. Expected direction:
   route-link ≥53%. This leg is built to kill its own confound: the 77.3% @484
   was measured against v178salt, which IDLEVSALT2 suggests is icefloe-weak —
   re-basing against the incumbent separates "routelink is great there" from
   "v178 was bad there". A null RETIRES the icefloe cluster cheaply; a hit
   rescues a dropped arm at map-gated strength (observed 77% on the segment).

— end of sweep. Nothing here is evidence; everything here is a question worth
2 hours of a lane.

## ⛔ ERRATUM (builder s39, ~15:2xZ — research's map_encode.py parse; correction at the record)
**The segment this report calls "900-area" is actually THE NEW POOL: five of
its ten maps are 20×20=400** (auroraveil, frostgate, icefloe, royale,
yulerune; only drakkarfjord/glacierkeep/midgard/ragnarok/valkyrie are 900).
The mislabel is the BUILDER'S (it was written into this agent's brief), not
the agent's. Every "900" segment label in this report reads as "new-pool";
every "legacy" label is confounded with SMALL maps (research's ladder cuts:
LEGACY&500+ = 52.8% vs LEGACY&small(<500) = 37.5%). CONSEQUENCE FOR
CANDIDATE 1: frostgate+royale are both 400-area, so MAPCODE's contrast may
be AREA or TABLE-MEMBERSHIP — research's constraint cuts: area does nothing
within NEW (400: 55.0 vs 900: 55.9) so membership survives as the candidate,
but the prereg's 15a primary is MEMBERSHIP IN MAP_CODES with AREA CLASS as a
declared covariate. LEGACY as a segment is retired everywhere: split at 500.
