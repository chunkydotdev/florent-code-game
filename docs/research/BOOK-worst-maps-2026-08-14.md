# BOOK — THE WORST-MAPS CELL {antler, midgard, fjordgate, ragnarok, frostgate}

**Written 2026-08-14T15:59:18Z (`date -u`) · head `696c739` · brief `docs/research/BRIEF-worst-maps-book-2026-08-14.md`**
*(the brief names the output `BOOK-worstmaps-…`; `docs/research/AGENT-PIPELINE.md:18` and the
spawn both name `BOOK-worst-maps-…` — this file, one artefact, no second copy.)*
**Era: `ourver >= 125` throughout, both axes. Rated surface `corpus/ladder_games.tsv` (430 games,
52.6%) for every denominator; `corpus/join.tsv` (395 rows / 79 matches) for mechanism — **checked, not
assumed: 0 of its 79 era matches lie outside the era ladder set, so no unrated leg is pooled in.**
Us-only unless a line says THEM. Nothing committed but this file.**

## 0. HEADLINE — FIVE CELLS, FOUR REAL, THREE MECHANISMS, ONE ARTEFACT

| cell | n | raw wr | mix-adj Δ (excl-self) | z (DEFF 1.07) | verdict |
|---|---|---|---|---|---|
| antler | 30 | 36.7% | **−13.0pp** | −1.47 | real, TINY mechanism |
| fjordgate | 26 | 38.5% | **−14.7pp** | −1.51 | real, TINY mechanism |
| midgard | 34 | 38.2% | **−19.3pp** | −2.38 | real, LONG-APPROACH mechanism |
| ragnarok | 33 | 42.4% | **−9.8pp** | −1.18 | real, LONG-APPROACH mechanism |
| frostgate | 25 | 44.0% | **−1.6pp** | **−0.17** | **NOT A CELL — opponent mix** |

**Grouped (baseline = our rate vs the SAME opponent off the group):
TINY {antler,fjordgate} n=56, 21 obs vs 29.59 exp, −15.3pp, z=−2.35, p=0.019 ·
BIG {midgard,ragnarok} n=67, 27 obs vs 37.43 exp, −15.6pp, z=−2.75, p=0.006 ·
frostgate n=25, −1.6pp, p=0.869 · ALL5 n=148, 59 obs vs 76.89 exp, −12.1pp, z=−3.06, p=0.0022.**
The TINY and BIG deficits are the same SIZE (−15.3 / −15.6pp) and have **opposite** mechanisms.
**Reproduction receipt:** the brief's own small-pair headline re-derives exactly on my instrument —
21 obs / 29.59 exp / z_naive −2.431 (brief: 21 / 29.6 / −2.43), `worstmap_expected.py`.

**Both easy outs are already closed and this book inherits that:** opponent concentration is 25–38% against a
60% bar with 9–11 distinct opponents per cell (`OPP-SEGMENT-MAP-2026-08-14.md`), and four of five cells sit at
or above the league's 60.2% favourite-win rate — frostgate at 64.3% is the pool's 3rd most favourite-friendly
map (research off `corpus/league_maps.tsv`, same day).
**Power, before the reading:** per-cell SE 8.1–9.7pp ⇒ **MDE 22.6–27.2pp at 80%**; only midgard clears alone,
so the pooled/grouped tests are load-bearing. Min stratum n=22 (frostgate, `join.tsv`); **0 cells below n=15**;
the lock-census join drops to n=16–24/cell (v125-only) and every line off it is flagged HINT.
**Units:** per-map bars take **NO** match DEFF — 0 of 430 (match,map) pairs carry >1 game, re-verified here;
residual opponent cluster **1.07** applied to every z above. **`econ.tsv` v2 (2026-08-14T14:01:25Z) is the
source of every cpu/tled figure**; no pre-rebuild cpu/turns number is cited.

## 1. antler (252, 14×18, cores 8.0 apart, 12 ore) — **SHARED trigger, PRIVATE failure**
1. Both economies halve on the terrain: our conveyors 7.51/100R vs 14.95 off-cell; **theirs 8.49 vs 14.39** — symmetric, so the compression is SHARED.
2. Our turrets die: sentinel survival **28%** (4.6 built, 3.3 killed) vs **59%** off-cell; gunner **32%** vs 72%. PRIVATE — theirs hold at 63%/49%.
3. They bring launchers, we bring none: **1.3/game vs our 0.0** (their off-cell rate 0.7, ours 0.3) — they double, we go to zero.
4. Our core dies in **66.7%** of antler games (worst cell in the pool) vs 45.3% against the same opponents elsewhere; theirs 25.9% vs 52.8%.
5. **Locks are NOT the channel here: 9.4% of our builder-rounds vs our 11.4% pool average** (theirs 5.6%).
6. Arrival is not the channel either: we arrive at median **r8** with 0% no-show, and within the cell arrival does not separate wins (r7) from losses (r8).

## 2. fjordgate (100, 10×10, cores 5.7 apart, **6 ore, all contested**) — **the extreme of the same class**
7. **Our belt is never built, not destroyed: 5.9 conveyors built/game vs 33.4 off-cell, only 2.6 lost.** They build **23.3** on the same tiles.
8. Standing at r150: us **2.5 conveyors / 1.5 harvesters**, them **12.5 / 3.0**. Our harvester survival **52%** vs their **95%**.
9. We are forward for **199 of ~214 median rounds** with **60% of the workforce** arriving — and their core still dies only 33.3% against our 62.5%.
10. Terrain: 90 free tiles, all 6 ore tiles equidistant-ish from both cores (top-right + bottom-left corners), cores 4 tiles apart diagonally.
11. **8.3% of fjordgate games we build NO harvester at all and 8.3% NO conveyor at all** (off-cell: 0.0% / 0.0%).
12. Locks again absent as a channel: 8.0% ours vs 5.3% theirs, both below their own pool rates.

## 3. THE TINY MECHANISM, IN ONE NUMBER — our raid edge is a COMMITMENT edge, and it is map-blind
13. **We send 50% of our builders to their core on EVERY map** (median arriver-share: antler 50%, fjordgate 60%, frostgate 50%, REST **50%**).
14. **Opponents send 20% by default — and 50–59% only on the tiny pair** (antler 50.0%, fjordgate 58.6%, REST **20.0%**; their no-show REST 19.2% vs antler 0.0%).
15. ⇒ **Where they stay home we win (valkyrie 77.8% with 48.0% of their games no-show; yulerune 72.2% / 35.3%); where they match our commitment we lose.** That answers the inversion question the pipeline carried: our best maps are the ones the opponent field declines to contest, not the ones favourites lose.
16. Our opening is **map-blind by construction**: the modal first-8 is `builder×5 → harvester → …` on antler (5/27), fjordgate (7/24), frostgate (10/22), midgard (12/31), ragnarok (11/30) and REST (123/261) — **five builder bots (+100% scale) bought before the first harvester on a 100-tile map with 6 ore.**

## 4. midgard (900, cores **33.9** apart — pool max, **16 ore, 3 within d²≤50 of home**) — **PRIVATE nav defect**
17. **Lock rate ours 35.6% of builder-rounds vs theirs 10.9% — 3.3×** (`HOME-LOCK-MECHANISM-2026-08-14.md` for ours; theirs newly measured, see §7).
18. Arrival collapses: median **r89** vs r27 against the same opponents elsewhere; **16.1% of games we never reach d²≤8**; forward-rounds 36 vs 129.5.
19. **Only 12.5% of our workforce ever arrives** (vs 50% everywhere else) while we build MORE builders there (8.9/game vs 6.7).
20. Our CPU is **2,689 µs/turn mean, 8,846 µs max = 88% of the 10 ms ceiling** (econ v2) — 5–12× our tiny-map cost (fjordgate 214 µs). **We never TLE anywhere: 0 tled turns on all 15 maps; opponents tle 43.3/1k turns on midgard.**
21. Within-cell, length-normalised: **losses carry 30.2% median lock burden, wins 13.7%** (Mann-Whitney z=−1.35, p=0.177, n=21 v125 games) — **HINT, the only cell where the lock/outcome link points the right way.**
22. Economy is NOT the failure: our conveyor survival 86%, harvester 72%, both at pool level; we simply never turn the economy into a kill (core death 58.1% vs 42.4%).

## 5. ragnarok (900, cores 33.9, 26 ore, 2 within d²≤50) — **same class, weaker dose**
23. Lock rate ours **14.1% vs theirs 5.2% (2.7×)**; arrival median **r52** vs r27; 3.3% no-show; 33.3% of the workforce arrives.
24. We out-build our own baseline there — **41.9 conveyors/game, the highest of any cell** — and still lose: this is a transport problem, not an income problem.
25. CPU 1,484 µs mean / 8,809 µs max; opponents tle 17.4/1k. Their launchers 1.3/game (vs 0.9 off-cell) with 28% survival — heavy launcher combat on the approach.
26. The within-cell lock/outcome link is **not** present (30.2/13.7 on midgard vs 13.7/11.8 here, p=0.369) — the dose is 2.5× smaller and so is the evidence.

## 6. frostgate (400, cores 14.0, 20 ore, 10–12 near home) — **the cell I could not explain, because there is nothing to explain**
27. **Mix-adjusted Δ = −1.6pp, z=−0.17, p=0.869.** Its 44.0% is what our own rate against those same opponents predicts. **The raw number is an opponent-mix artefact.**
28. Locks are the LOWEST of the five (6.7% ours / 3.3% theirs) and games the shortest (median 140 turns vs 171 pool).
29. One real asymmetry with no currency attached: our conveyor survival **68% vs their 90%** (17.4 built, 5.6 killed) — the central 12-tile ore field at rows 9–10 sits exactly between the cores and our trunk crosses it.
30. **Do not spend a plank here.** At MDE 26.8pp this cell cannot distinguish −1.6pp from 0; the honest answer is "not a deficit", not "unexplained deficit".
31. ⚠ Its dims+core-anchor twin **yulerune (20,20,2,9,16,9) reads 72.2%** — same geometry, opposite result — which is itself the cleanest disproof that geometry alone drives any of this.

## 7. SHARED vs PRIVATE, per cell — the brief's required verdict
| cell | mechanism | shared or private | evidence |
|---|---|---|---|
| antler | economy compression + turret attrition + their launcher edge | **SHARED trigger, PRIVATE failure** | both belts halve (7.5 vs 8.5/100R); our sentinel survival 28% vs their 63% |
| fjordgate | all-in raid consumes the workforce; belt never built | **PRIVATE** | 5.9 vs their 23.3 conveyors on identical terrain |
| midgard | nav limit-cycle + long approach | **PRIVATE, on a SHARED hazard** | ours 35.6% vs theirs 10.9% (their pool-max too) — 3.3× |
| ragnarok | same, weaker | **PRIVATE, on a SHARED hazard** | ours 14.1% vs theirs 5.2% — 2.7× |
| frostgate | none demonstrated | **n/a — artefact of opponent mix** | Δ −1.6pp, z −0.17 |
**Pooled private-defect scale: our lock rate 11.4% vs opponents' 4.7% across all maps (2.4×), and our harvesters die 22–48% of the time while theirs die 0–5%** (survival: us 52–78%, them 95–100%).

## 8. ROADS CLOSED HERE — five negatives, each with a control that produced the other verdict
32. **MAP_CODES twin-map misidentification: REFUTED.** All 25 pool maps have an exact terrain entry; both colliding keys — `(30,30,2,2,26,26)` midgard|ragnarok and `(20,20,2,9,16,9)` frostgate|yulerune — resolve **RIGHT at every call site** (core r²=36 and builder r²=20), margins 5–52 mismatched tiles, never 0. Controls: omniscient vision right on 15/15, corrupting a grid kills its exact match. `mapcode_collision_probe.py --selftest`.
33. **"Contested ore" as the terrain driver: REFUTED.** Spearman(win rate, % ore equidistant from both cores) = **−0.02** over 15 maps. (area +0.40, coreD +0.31, ore count +0.38 — none is a story at n=15.)
34. **"Locks cause the losses" as stated: REFUTED.** Games with ≥1 locked builder WIN more (59.8%, n=132) than games with none (52.4%, n=168) — a game-length confound (lock-present games run 187.5 vs 167.0 median rounds). Only the **length-normalised** version survives, and only on midgard (§4.21).
35. **Arrival lateness as the tiny-pair mechanism: REFUTED.** We arrive FASTEST on our two worst maps (r8, r6 vs r28 pool) and within-cell arrival does not separate outcomes (antler 7 vs 8; fjordgate 5 vs 8; midgard 86.5 vs 100.0).
36. **Our own CPU as any cell's mechanism: REFUTED.** 0 tled turns for us on all 15 maps (econ v2); the ceiling proximity on midgard (88%) is a cost signal, not a failure.

## 9. ONE LEAD, CONFOUND WELDED ON — the opponent-CPU harvest (Spearman(our wr, their tled/1k) = **+0.45**, n=15)
37. **Our two worst maps are the two lowest opponent-TLE maps in the pool: antler 0.02 and fjordgate 0.04 tled turns per 1,000 turns, against 43–74/1k on midgard/royale/glacierkeep/icefloe.**
38. ⚠ **Confounded with area** (Spearman(their tled/1k, area) = +0.43) and contradicted inside the set (midgard 43.3/1k and we lose; royale 53.6/1k and we read 48.0%). **A lead to size, never a result to explain** — and it is Loki-shaped if it holds: raising the entity count in their vision on a tiny map is a legal, documented way to buy the failure we get free elsewhere.

## 10. Routing — QUEUE rows (max existing id = **61**), each with an OBLIGATION 15 declaration
**#62 — TINY-MAP ECONOMY FLOOR (NEW).** Floor the belt before the raid on maps whose enemy core is ≤8 tiles away: require ≥2 live harvesters and ≥N conveyors before the 3rd builder goes forward, and stop buying 5 builders (+100% scale) ahead of the first harvester on a 100-tile map.
`MAP SEGMENT: tiny maps {fjordgate 100, antler 252} — the mechanism is core separation ≤8 tiles with every ore tile contested, which makes both sides raid by r8 and erases our 50%-vs-20% commitment edge. EXPECTED DIRECTION: POSITIVE on the segment, ~ZERO off it. PRIMARY SEGMENT: tiny maps (15b). Descriptive only: frostgate is explicitly NOT in it (Δ −1.6pp). Bars: kill-round non-regression + belt-standing-at-r150 as the mechanism dial (target 2.5 → their 12.5).`
**#63 — LONG-APPROACH ARRIVAL (NEW).** The target is arrival share (12.5% on midgard vs 50% everywhere), NOT another 2-cycle detector — `OSCLOCK`/`OSCLOCK2` screened negative twice and `HOME-LOCK-MECHANISM-2026-08-14.md:§5.3` recommends against a third.
`MAP SEGMENT: long-approach maps {midgard, ragnarok} — core separation 33.9 (pool max) with 3 and 2 ore inside d²≤50 of home, so every walk is long and nav exposure is maximal; our lock rate there is 3.3×/2.7× the opponents' on the same terrain. EXPECTED DIRECTION: POSITIVE on the segment, ~ZERO off it (valkyrie/glacierkeep are 900-area at separation 24.0 and we read 77.8%/73.3% — do NOT use the 900-area size class, it dilutes). PRIMARY SEGMENT: long-approach maps (15b). Bars: kill-round non-regression + arrival share and no-show rate as dials + CPU headroom watch (2,689 µs mean, 88% of ceiling).`
**#64 — FROSTGATE IS NOT A CELL (NOTE, no leg).** Records that the 44.0% is opponent mix (Δ −1.6pp, z −0.17, MDE 26.8pp) so the next reader of the worst-map table does not re-commission it. `MAP SEGMENT: none — no effect to segment.`
**#65 — OPPONENT-CPU HARVEST (NEW, HYPOTHESIS).** Test whether entity-count pressure inside enemy vision raises their tled rate on the tiny pair, where they currently run at 0.02–0.04/1k.
`MAP SEGMENT: tiny maps {fjordgate, antler} — the mechanism is that opponent per-turn cost scales with entities in vision and tiny maps currently give them none. EXPECTED DIRECTION: POSITIVE on the segment, ~ZERO off it (they already tle 43–74/1k on the big maps, so there is no headroom to buy). PRIMARY SEGMENT: tiny maps (15b). ⛔ Fire only after the area confound is sized — Spearman(their tled, area)=+0.43.`

## 11. Scripts — re-runnable, not re-arguable · all in `SP=/private/tmp/claude-501/-Users-junghard-…-a9e77d8e-…/scratchpad/wm` (ephemeral; the commands are the artefact)
* `era_games.tsv` ← `awk -F'\t' 'NR==1{next} $6+0>=125 {print $1"\t"$8"\t"$4"\t"$12"\t"$11"\t"$9"\t"$10"\t"$6"\t"$5}' corpus/join.tsv` (395 rows); `events_era.tsv` ← `awk -F'\t' 'NR==FNR{keep[$1]=1;next} FNR==1{print;next} ($1 in keep)' $SP/era_games.tsv corpus/events.tsv` (49,168 rows, 17 s)
* `worstmap_expected.py` [`--selftest`: planted null z=−0.49, planted −ve z=−20.0, +ve z=+19.5] — §0 · `worstmap_arrival.py <filelist> replay_archive <out> 8` [`--selftest`: monotone in threshold, saturating threshold arrives r0; 395/395 parsed, 0 failed, 25 s] — §1,2,4,5
* `worstmap_report.py` · `worstmap_permap.py` · `worstmap_rates.py` (length-normalised) · `worstmap_deaths.py` (built→destroyed) — §1–6 · `worstmap_lockjoin.py` (joins `…/248fc65e-…/scratchpad/census_v125.withmap.jsonl`) — §4.21, §8.34
* `mapcode_collision_probe.py` [`--selftest`] over `bots/_v223sealrepair/doctrine.py` + `maps/*.map26` — §8.32 · econ v2 cut: `awk -F'\t' 'NR==FNR{m[$1]=$2;ot[$1]=$4;next} …' $SP/era_games.tsv corpus/econ.tsv` — §4.20, §9

## 12. What I could NOT explain, said plainly
39. **frostgate** — no deficit to explain (§6), the one cell where the honest answer is "the raw 44.0% was the artefact". **The class-O lock mechanism is still unidentified** (`HOME-LOCK-MECHANISM-2026-08-14.md` refuted 5 candidates; 89.3% of locked bots are class O): this book measures its incidence and its 2.4–3.3× ours-vs-theirs ratio, it does not name its cause.
40. **Why our belt collapses on fjordgate** is measured (5.9 vs 23.3) but not traced to a source line — that trace is #62's first hour and must precede any arm. **antler's turret attrition (sentinel survival 28% vs 59%)** has no mechanism attached; candidates are their launcher edge (1.3/game vs our 0.0) or a line-of-fire property of 14×18. Unresolved.
