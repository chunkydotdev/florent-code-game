# Juusto v13 seal-geometry study — the ferry-siege plank at 1847 vs the Jython 2178 reference

**BANKED by research s50, 2026-08-17 ~18:3xZ.** Agent report below (faithful, entities normalised). Ground: **ARCHIVE-ONLY, zero downloads** (1,281 Juusto games parsed, 0 errors) — P-FIELD-13 = 480 v13-vs-field games/17 opponents (8× the Jython study's n), P-FIELD-11 = 55, P-US-13 = 115 vs us. **Keeper hazard COMPLIED: all joins off an 18:19:08Z snapshot, coverage verified twice + vs live, md5-stable.** Decoder controls all driven both ways (40/40 match-score fold, flip control 0/40; damage-alphabet cross-decoder 448=448; non-constant ledger check passed).

## HEADLINE — THE 331-ELO DELTA IS EXECUTION, NOT IDEA (ranked by carried gap)
1. **Ferry 4 rounds late, 50% slower per hop:** launcher r4/throw r6 (Jython r1/r2); taxi cycle 3 rounds (build→+2 throw+self_destruct) vs Jython's 2; adjacency r41 in 51% of games vs r8 in 98%. **The plank's premise — on the ring before the enemy has an economy — is delivered in half their games, 33 rounds late.**
2. **8-tile seal = heal lock ONLY: 3,124/3,124 ring barriers on the 8 orthogonals, ZERO on corners in 1,281 games — while defenders birth 41.4% of builders on the 4 corners (top tile NW (−1,−1) 20.7%).** Juusto's "complete" seal is Jython's 8/12. Spawn denial is NOT a mechanism their seal operates (banded control: defender spawning falls to 0.0023/rd by r51-100 on its own, before the median r72 seal).
3. **No eviction arm: 0 of 1,990 throws** (Jython: 928 = 21%, the maintenance phase). Seal stalls near-side-first at median 6/8 (completion 25.6% vs Jython 41.7%; order measured: NEAR rank 1.36 → FAR 3.54 — they seal outward from arrival and the game ends before the far pair).
4. **Raider stream, not singleton:** median 2 bots reach d²≤8 (==1 in 14%); re-ferry on death, 3-round tax each (raw trace shows r6, r123, r150, r183 insertions in one game).
5. **Sentinel earlier/closer but thinner: r46, d²=16, 93.5% forward — 2.06/game vs 3.85, 58.6% destroyed.**
6. **104 builder attacks/game (95.6% on buildings, 0 EVER on the core)** — a harass arm Jython doesn't run; 104 actions not spent on seal or sentinel. v11→v13 era read: mechanism identical; melee doubled and shifted homeward (counter-siege arm added); outcome deltas confounded by opponent mix.
**NOT lacking:** identical launcher-side `self_destruct` (99.7% executed, lifetime exactly 2 in 2,009/2,043; 87.9-100% zero-adjacent; the 7 combat-killed read lifetime 9 — control fires); kill = **100.0% sentinel** (26,726 × −18; builder-on-core 0; 1/257 kills without an in-range sentinel); home defence identically absent.

## SEAL FINDINGS THAT BIND THE BUILD
- **Binary seal REPLICATED at 8× n and harder: 0 heals in 8,244 fully-sealed rounds** (occ-8), across every round band and a paired within-game control (123 games, 1,002 heals at occ 6-7 → 0 at occ 8, no game moving the wrong way). **The zero is MECHANICAL: 8 occupied edges leave no orthogonal stand-tile, so heal(core) is geometrically impossible.**
- **Partial-seal inversion replicated with the honest confound stated:** heal/rd 0.75 (occ 0) → 1.23 (occ 4) → 0.36 (occ 7) → 0.0000 (occ 8) under a siege-window control; intensity/occupancy still co-rise, so "partial provokes" is directional, not demonstrated. **The actionable half is established: below 8 nothing is bought; at 8 everything is.**
- Seal-vs-outcome (⚠ partly reverse-causal): peak 8/8 → 0.862 Juusto share, kill r132, timely 0.780; peak 0-2 → 0.220.

## ELEMENT TABLE (Jython v157 n=60 / Juusto v13 n=480 — shapes transfer, outcome rows are opponent-mix-confounded)
launchers/g 6.35/4.29 · relay ≥3 hops pre-r40 83%/40.4% · hop d² med 17/32 (they max-range every throw) · barriers/g 16.6/6.54 · ring share 77%(incl 31% corners)/99.5%(0 corners) · own-ring 5 ever/0 ever · full-orth seal 41.7%/25.6% (r52/r72; vs us r54) · first sentinel r38/r24 · sentinels/g 3.85/2.06 · gunners 0.67/0.45 · record 0.650±0.149 / 0.558±0.060 (DEFF 1.833) · kill median r125/r152 · timely-by-r300 53%/44.6% · own core dies 27%@r190 / 44%@r160 · r1000 7/60 / 12/480.

## DEFENDER'S CHAIR — our trees vs their siege (rated denominators only from ladder_games: all-era 38/85=0.447; v13 14/35=0.400; the 115-game archived pool is prototype-mixed, mechanism only)
1. **Forward turrets discriminate AGAIN, now from the defender's chair vs a second implementation: our wins carry 2.39 forward turrets / 3.98 sentinels vs losses' 0.51 / 1.56.** (Their forward-sentinel dose is FLAT across our wins/losses — the dose is not the variable; our response is.)
2. ⭐ **WE UNDER-KILL THEIR KILL WEAPON: their sentinels die 58.6% vs the field, 27.9% vs us** (147 built/41 destroyed in 115 games) — and it is 100% of their core damage. **The single highest-value target in the matchup, attacked at half the field's rate.**
3. **They rush us harder than the field** (first barrier r15 vs r21, 8/8 at r54 vs r72, first sentinel r28 vs r46) and vs us the plank is nearly pure forward-sentinel (median 0 raiders ever orth-adjacent to our footprint).
4. **The heal lockout is symmetric: 0.0000 of our core-heals/rd across 2,502 fully-sealed rounds** — our above-field reactive healing (1.05/rd unsealed) buys nothing at 8/8.
5. **Clear the ring EARLY or not at all: pre-r100 removal rate 21.6% in our wins vs 8.8% in losses (2.5×)** — replicates the s40 book's retained band split. Total removal barely separates. Our ring-clearing is inconsistent ACROSS OUR OWN TREES (8.8%-69.0% by version) — itself a build finding.
6. **We throw nothing back: 0.30 launchers/game, 6 throws/115 games, 0 evictions** — their raider and sentinel-builder stand in our half unmolested by an approved channel.

## WHAT THE DELTA TEACHES THE BUILD (agent's list, banked verbatim in substance)
2-round taxi not 3 · seal the 12 not the 8, and below 8 seal NOTHING · the seal is not the weapon and neither is the raider (both shapes now confirm: barriers make sentinel DPS un-out-healable) · build the maintenance/eviction arm Juusto skipped · crash channel unharvested by BOTH implementations (additive for us) · defensively: kill their sentinel, clear rings before r100.

## LIMITS (in force)
Not a controlled cross-column comparison (pools, n, eras differ; 160/480 games vs Erebus alone). Partial-inversion confounded (direction only). Seal-outcome table partly reverse-causal. 115-game vs-us pool is archived-mixed — never a win rate. No per-shot FireTurret→victim join (alphabet-attributed, 3-way validated). ourver→tree mapping from brief, not verified. Unmeasured: footprint-face targeting, their sentinel rebuild behaviour, whether 104 attacks/game pay. Artifacts in scratchpad `juusto_study/` incl. `all.jsonl` (1,281 games) + the 18:19:08Z corpus snapshot.
