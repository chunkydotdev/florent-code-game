# Prior tracing — which load-bearing BELIEFS rest on evidence tonight undermined

**Research arm, 2026-08-10 (s26).** Companion to the verdict audit (which closed at zero
retractions). This audit covers **PRIORS**: things the library asserts as settled background,
which no verdict ledger indexes. **Trace and classify only — nothing in this document edits or
retracts any other document.**

**Scope swept:** `docs/research/tactics/INDEX.md` §"Standing context a sweep should know" and
the two blocks above it (the highest-yield target, and it was); `docs/research/*.md` (152
files, screened for probe-family dependence); `docs/game-model.md`, `docs/opponents.md`,
`docs/open-questions.md`, `docs/strategy-notes.md`, `docs/strategy-log.md`.

**Corpus used for re-derivation:** `corpus/join.tsv` (1,710 attributed ladder games),
`corpus/econ.tsv`, `corpus/build_agg.tsv`, `corpus/events.tsv`, `corpus/throws.tsv`,
`corpus/meta_join.tsv`. Manifest `2f0649c`, 9,143 archive replays.

---

## 0. THE ERA SPLIT, STATED ONCE, BECAUSE SEVEN ROWS BELOW DEPEND ON IT

`corpus/join.tsv`, our version histogram: **1,580 of 1,710 attributed ladder games are
v101-or-earlier (Eir), 130 are v102 (LOKI-8) — 92.4% / 7.6%.** In `meta_join.tsv` over all
2,363 of our side-games the split is 93.0% / 7.0%. **Any "we / our bot" figure pooled over the
archive is an Eir figure.** Every ERA-DRIFT row below was checked by recomputing the *same*
statistic on the v102 subset with the *same* instrument.

**Probe-family scope, checked rather than assumed** (method rule 2): `grep -rl "best_core or
best_any" bots/*/main.py` returns **exactly 5 files** — `band_probe`, `cad_probe`,
`flotte_probe`, `kladde_probe`, `orizon_probe`. `ouroboros_probe` and `razer_probe` do **not**
carry that line. The five is the right set.

---

## 1. THE CLASSIFIED TABLE

Buckets: **CLEAN 18 · ERA-DRIFT (c) 7 · PROBE-CONTAMINATED (a) 4 · FIXTURE-BLIND (b) 2 ·
UNTRACEABLE 3** — 34 load-bearing priors traced.

### ERA-DRIFT (c) — 7

| # | claim (quoted) | asserted at | evidence it rests on | class | conf |
|---|---|---|---|---|---|
| 1 | *"Everything about us breaks at r150. Five independent instruments agree: conversion ratio, raider survival (43→6 rounds), turret production, forward placement, ammo conversion."* | `tactics/INDEX.md:807-809` | Five instruments, all computed on our pooled ladder archive at live **v89/v90** (`late-game-doctrine-2026-08-09.md` version tag; `middle-game-hazard-and-economy-2026-08-09.md` §1, n=1,230). Population: 100% Eir. | **ERA-DRIFT (c)** | HIGH |
| 2 | *"We bank and do not spend. We end r200-300 holding more titanium than Ouroboros while buying a twelfth as much ammunition."* | `tactics/INDEX.md:812-813` | `ammo-and-cpu-2026-08-09.md:56` — subject is **Ouroboros specifically**, live v90. Subject error already published at `gunner-vs-sentinel-pricing-2026-08-09.md:424-427` (*"0.84×, not a twelfth"* vs top tier); era half unaddressed until now. | **ERA-DRIFT (c)** | HIGH |
| 3 | *"a bot that builds 0.2 turrets per game after r200 has no mechanism to clear a healing screen, which makes a healed core mathematically unkillable by attrition"* | `heal-arithmetic-2026-08-09.md:35-37`, propagated to `tactics/INDEX.md:814-820` | `late-game-doctrine-2026-08-09.md` §2, v89 archive; re-derived at 0.30 gunners / 0.61 turrets in `field-baselines-third-party-2026-08-09.md` §6 — same era. | **ERA-DRIFT (c)** | HIGH |
| 4 | *"353 games reached r1000 and we won 57.2%"* / the hazard curve *"29% → 55% → 72% → 76%"* | `tactics/INDEX.md:949-955` | `middle-game-hazard-and-economy-2026-08-09.md` §1, `join.tsv` n=1,230, live v90. **The source doc itself says at :78-80 *"The 57.2% is a pooled-lineage number and must not be quoted as a property of v90"* — the INDEX quotes it without that sentence.** | **ERA-DRIFT (c)** | HIGH |
| 5 | *"Home defence is the measured asset (+11.4 / +16.6 / +22.3pp over the field)"* | `tactics/INDEX.md:965-966`, `heal-arithmetic-2026-08-09.md:62`, `coordination.md:11340,11492` | 50-round-horizon turret survival from `events.tsv`, US n=2,121/676/600 home turrets. Population: our pooled archive = Eir. | **ERA-DRIFT (c)** | MEDIUM-HIGH |
| 6 | *"median kill round r296"* (in *"The field does not rush"*) | `tactics/INDEX.md:805-806` | `kill-timing-doctrine-2026-08-09.md:72` — the conditioning is **"THEY kill *us*", killer ≥1550**, i.e. the field's clock against the Eir archive, quoted as a field property. Already superseded in-library: `field-baselines-third-party-2026-08-09.md` §2-3 gives third-party **r211** raw / **r229** strength-and-gap-matched against **r283** for killing us, and instructs *"should be quoted as r283 vs r229"*. **The 12%-by-r100 half is CONFIRMED third-party at 13%, N=2,257 — that clause is clean.** | **ERA-DRIFT (c)** *(median clause only)* | HIGH |
| 7 | *"`core_destroyed` 15W–74L (17%) · `titanium_collected` 164W–158L (51%)"* — the origin of the standing *"we lose core fights, we're even on economy"* prior | `opponents.md:239-245` | 97 series / 485 games, **spanning submissions v1–v42** — two lineages before Eir, three before LOKI-8. Denominator stated in-doc; nobody has re-run it. | **ERA-DRIFT (c)** | HIGH |

### PROBE-CONTAMINATED (a) — 4

| # | claim (quoted) | asserted at | evidence it rests on | class | conf |
|---|---|---|---|---|---|
| 8 | *"`orizon_probe` — CLASS-VALID … Usable as a field instrument for the Orizon-team point-blank battery class … No re-freeze."* | `probe-fidelity-orizon-flotte-2026-08-08.md` (headline) | Source-derived predicates on `orizon_probe`/`flotte_probe` vs 405 wild games. **Every predicate tested is opening / turret-type / geometry / lane-fraction. Not one tests what the probe shoots at.** The bug line is `orizon_probe/main.py:1157`. | **PROBE-CONTAMINATED (a)** | HIGH |
| 9 | *"`band_probe` — USABLE AS A GUARD"* / *"`kladde_probe` — CLASS-VALID on shape"* | `probe-fidelity-guards-2026-08-08.md` (headline) | Predicates vs 160 wild games. §3.4 states the guard's own purpose: *"does a change break our repair line, our harvester defence, our ability to survive a late turret insertion?"* — and measures wild kladde killing 8.5 of our harvesters and forcing 398 heals/game. **Those are exactly the quantities `best_core or best_any` makes structurally unreachable.** §5 propagates the caveat to 20 named `results.tsv` acceptance rows; that propagation is now under-scoped. | **PROBE-CONTAMINATED (a)** | HIGH |
| 10 | *"Across all 18 games our side made ZERO trunk heals (every single heal targets the CORE footprint) … K's 'core+trunk' budget never trunk-heals at all"* | `k-drag-diagnosis-2026-08-07.md` (headline, suspect (a)) | 18 paired replays, fixtures `konly_orizon` / `base_orizon` / `konly_band` — `orizon_probe` + `band_probe` exclusively. **Identical in shape to the confirmed dead-heal misdiagnosis**: with no damage ever landing on a conveyor, the trunk-heal path had no opportunity to fire. Suspect (b) (*"zero heals at dsq>50"*) has the same shape. The measured drag magnitudes (−15 / −35 vs band) come from the same fixture. | **PROBE-CONTAMINATED (a)** | HIGH |
| 11 | The instrument-validity sub-table naming `orizon_probe` and `band_probe` as the two currently-valid instruments | `v5-instrument-coverage-2026-08-08.md` | Inherits rows 8-9. The doc's own headline (*"coverage of the bleed by a currently-valid instrument: 0.0%"*) is **unaffected or strengthened** — only the "which probes are trustworthy" sub-table is exposed. | **PROBE-CONTAMINATED (a)** *(sub-claim)* | MEDIUM |

### FIXTURE-BLIND (b) — 2

| # | claim (quoted) | asserted at | evidence it rests on | class | conf |
|---|---|---|---|---|---|
| 12 | *"archipelago seat A ~77-78% (n=64+), atoll ~28-31%, heart ~31%, lighthouse ~28%"* — flagged in-doc as *"the biggest open question in the project… worth several times what the jackpot bug was"* | `open-questions.md:92-100` | **Mirror runs (identical bots) plus one 480-match head-to-head. One arena fixture, never checked on the platform.** | **FIXTURE-BLIND (b)** | MEDIUM |
| 13 | *"local seeds vary games only weakly … a per-map arena row of N games is effectively ~2 distinct games"* | `game-model.md:92-101` | One candidate pair (**v55 vs `_v70cg` on snowflake**) generalised into a standing rule about every arena row. Never checked on a second pair or map. Load-bearing: it is the reason arena Wilson intervals are treated as overstated — **while `open-questions.md:69-83` still quotes three such intervals as settled effect sizes.** | **FIXTURE-BLIND (b)** | MEDIUM |

### UNTRACEABLE — 3

| # | claim (quoted) | asserted at | why untraceable | class | conf |
|---|---|---|---|---|---|
| 14 | *"[wild-measured: 1,471/1,472 throw events at d²≤2]"* | `game-model.md:293-295` | Cited only by nickname (*"cad-fodder feasibility read"*); the 1,471/1,472 denominator appears in no named research doc. **The mechanism itself is independently corroborated** at `clankers-noconfound-2026-08-07.md:399` (439/439) — so the *fact* is fine and only the *figure* is unsourced. | **UNTRACEABLE** *(figure only)* | HIGH |
| 15 | *"a conditional rate ~53% for `ladder1` and `aug7`, against a field average of 68.4%"* | `open-questions.md:121-126` | The **field** denominator is not stated and no research doc reproduces the 68.4%. Our half traces to `tools/replay_census.py` and is Eir-era. | **UNTRACEABLE** *(field half)* | HIGH |
| 16 | *"Payback is ~8 rounds at 100% scale, ~12 even at 150%"* | `strategy-notes.md:53-55` | Pure nameplate arithmetic, no fixture. Excludes conveyor cost and builder-rounds — which `open-questions.md:72-73` still lists as unanswered. **No empirical harvester payback measurement exists anywhere in the library.** | **UNTRACEABLE** *(as measurement)* | HIGH |

### CLEAN — 18 (stated, not omitted)

| # | claim (quoted) | asserted at | evidence it rests on | note |
|---|---|---|---|---|
| 17 | *"UNIT TURN ORDER IS GLOBAL ENTITY-ID ASCENDING"* — 26,078 pairs 0 inversions; independently 1,842,445 pairs over 205 replays, 0 inversions; **two causal tests that never read log ordering** | `tactics/INDEX.md:875-933` | Replay-derived + causal; era- and fixture-independent. | **The strongest prior in the library.** Its four consequences (mid-round creation, denied turns, core ids, id magnitude meaningless) inherit that. |
| 18 | *"healing is 4.00 HP/Ti and the best damage source is 1.80 HP/Ti … the defender wins any titanium-symmetric attrition race 2.2:1"*, incl. the 8.00 HP/Ti stacked-tile amendment | `tactics/INDEX.md:814-826`, `heal-arithmetic-2026-08-09.md` §1 | Ruleset arithmetic + `fcode/_types.py:578,345` read at source. No fixture, no population. | Untouched by all three contaminants. |
| 19 | *"POST-THROW DWELL IS ONE ROUND"* — 97,999 throws, modal dwell 1, 96.4% off the landing tile within one round; 33.5% land on an occupied tile | `tactics/INDEX.md:940-948` | `throws.tsv`. Verified: **4,178 distinct files, 1,259 ours and 2,919 third-party — ~70% of the population is not us**, so it is not an Eir property. | CLEAN. |
| 20 | *"MEASURED ENGINE FACTS"* — store buffered/last-writer-wins/negative write raises; gunner line blocked, sentinel line pierces; build legality > `is_tile_empty`; spawn ring is the 12-tile Chebyshev-1 ring | `tactics/INDEX.md:863-874` | s23 dedicated engine probes + `CORE_SPAWNING_RADIUS_SQ` at source. | CLEAN. |
| 21 | *"Only 12% of top-tier kills land by r100"* (the rush clause of row 6) | `tactics/INDEX.md:805` | Third-party replication, killer ≥1550, **N=2,257 → 13%**. | CLEAN — the doctrine survives; only the median in the same sentence does not. |
| 22 | *"Only 2.34% of forward throws at r200+ ever land a single attack on the enemy core"* | `tactics/INDEX.md:810-811`, `late-game-doctrine-2026-08-09.md` §0.1 | Eir population — **but it replicates and v102 agrees.** My cut of `throws.tsv`: our forward throws at r200+, Eir **1 of 42 = 2.38%**; **v102 0 of 27**. | CLEAN with note: Eir-sourced, direction and level confirmed on the current line. |
| 23 | *"we run a damage-to-repair ratio of 1.11:1 against the field's 2.79:1"* | `tactics/INDEX.md:817-818` | Eir-pooled — **but the category survives.** Recomputed from `econ.tsv` (ratio is denominator-free): **Eir us 1.05, v102 us 1.21; Eir field 2.76, v102 field 4.27.** Field level already revised to 1.96 third-party (composition, not behaviour) in `field-baselines` §4. | CLEAN with note: two published revisions to the *levels*, direction preserved in both eras. |
| 24 | *"our opening is a near-constant — r0-150 build medians are *identical* in wins and losses"* + the method warning that follows it | `tactics/INDEX.md:956-959` | Eir-pooled (n=678 games with turns ≥300). **Not rechecked: v102 has ~40 qualifying games, below any usable n (method rule 5/6).** | CLEAN with note. The *method warning* it carries — a paired differential whose variance lives on the other side of the subtraction is an opponent thermometer — is population-independent and stands regardless. |
| 25 | The sentinel-file `2.68` correction (*"⚠ CORRECTED — 2.68 WAS OUR OWN NUMBER, RELABELLED 'FIELD'"*, third-party re-derivation 2.13 at 3+, N=28,277) | `tactics/INDEX.md:833-844` | Already self-corrected in place against third-party data. | CLEAN. Model case of a prior repaired rather than left standing. |
| 26 | The seat-asymmetry null (*"DO NOT CHASE THIS — MEASURED NULL"*, replacement evidence p=0.48 / p=0.29) | `tactics/INDEX.md:900-929` | Invalid `winnerSide` evidence **withdrawn in place**, conclusion re-established on the in-replay team index. | CLEAN. |
| 27 | The arena-pool prerequisite block (*"OUR ARENA POOL CANNOT MEASURE A DEFENSIVE PLANK AT ALL"*) with its s26 three-part amendment | `tactics/INDEX.md:710-751` | Already amended tonight; names the probe authorship, the ladder as the live instrument (46.9% turret loss, 5,599/11,947 over 2,313 games), and `razer_probe`'s mis-calibration. | CLEAN — this is the block that *found* contaminant (a). |
| 28 | *"mostly you don't break it — you win on economy"*, as qualified by sweep 14 (BC2020/BC2023 were offence-dominant; the precondition we lack is cheap mobile continuously-producible damage) | `tactics/INDEX.md:845-862` | Literature sweep, quote-audited 16/16 verbatim. No fixture, no population. | CLEAN. |
| 29 | *"Δ = 32 × (games_won/5 − E) … each of the 5 games is worth ±6.4 Elo independently"* | `game-model.md:142-149` | Fit over 100 ladder matches, **zero residual**. | CLEAN — and the single most downstream-load-bearing prior in the library (it is why per-game win rate is the ladder currency). |
| 30 | *"Crediting is delivery-only … zero, over 990 measured rounds"* | `game-model.md:372-377`, reconfirmed `:495-499` (56 team-sides / 28 replays, zero mismatches) | Dedicated probes `probe_credit` / `probe_credit_nc` + independent replay reconfirmation. | CLEAN. Best-supported prior in `game-model.md`. |
| 31 | *"Spawnable tiles are exactly the 12-tile ring"* | `game-model.md:189-198` | Exhaustive tile-by-tile `can_spawn()` via `bots/probe_spawn`. | CLEAN. |
| 32 | *"Seat assignment is fixed for the whole best-of-five"* — 158 matches / 790 games, 583/583 | `game-model.md:82-89`, `bo5-seat-assignment-2026-08-08.md` | Platform metadata; lineage-independent. | CLEAN. |
| 33 | *"a rated game is a pure function of (opponent, opp_version, map, our_version, our_seat) — mapSeed does NOT vary the game"* | `game-model.md:503-515` | 1,160 rated games. | CLEAN on the determinism. **Note:** the attached *"19 re-LOST games (~61 Elo)"* and *"forward EV ~0.06 Elo/game"* are pooled-archive numbers and therefore Eir-sized. |
| 34 | *"Turrets do NOT fire on their own"* — a 1000-round match with Gunners and no code branch consumed zero ammo | `game-model.md:263-268` | **n = 1 match**, with the doc's own caveat that enemy line-crossing was not proven. | CLEAN with note: a mechanism claim on n=1, but the alternative would have been visible if it existed (method rule 3 satisfied). |

---

## 2. THE EXPOSURES WORTH ACTING ON, RANKED

### #1 — **THE WHOLE "STANDING CONTEXT" SECTION DESCRIBES EIR, AND THAT IS ONE FACT, NOT SEVEN**

Rows 1-5 are not five findings. **Every one of them is the same fact: the section was written
at v89/v90 and the live bot is v102, which behaves differently in exactly the places the
section makes claims about.** I re-ran four of the section's own instruments on the v102
subset with the same code path:

| instrument | Eir (v≤101) | **LOKI-8 (v102)** | verdict on the standing claim |
|---|---|---|---|
| **ammo converted, Ti per 100 rounds lived**, bands r0-150 / 150-200 / 200-300 / 300+ | **212 → 156 → 130 → 140** (the r150 break) | **209 → 300 → 253 → 135** | **INVERTED.** v102 converts *43% more* after r150, not half as much. n = 130 games / 17,869 + 3,736 + 4,553 + 11,103 round-slots. |
| **turrets built in r200-300 per game reaching r200** (us vs field, same games) | us **0.64** vs field **2.22** (reproduces the published 0.2 / ~2) | us **2.15** vs field **1.18** | **INVERTED.** n = 71 v102 game-sides reaching r200. The turret-production deficit is gone. |
| **titanium held at end of r200-300** (us vs field, same games) | us **506** vs field **348** — *"we bank and do not spend"* | us **95.7** vs field **209.5** | **INVERTED.** n = 71. v102 is the one running dry. |
| **share of games reaching r1000** / win rate there | **30.2%** of games, **56.4%** won (n=477) | **6.9%** of games, 1 of 9 won | **The current line barely reaches the clock.** The 57.2% cannot describe it; and 9 games is no number (method rule 6), so *nothing* about v102's clock play is currently measured. |
| **hazard at r151-300** (our win rate, core-decided games) | 46.3% (n=341) | 63.6% (n=55) | *"We lose the middle"* does not reproduce at n=55. |

**All five point the same way and they are internally consistent:** v102 spends its titanium
instead of banking it, buys ammunition after r150 instead of stopping, builds turrets in the
window Eir abandoned, and consequently plays decisive games instead of grinding to r1000.
**The section reads as a description of a bot we no longer field.**

**What this does NOT mean:** none of it says the *doctrine* is wrong. It says the **numbers
attached to the doctrine are Eir's**, and a sweep that reasons from *"we build 0.2 turrets
after r200"* is reasoning about a bot that builds 2.15.

### #2 — **THE HOME-DEFENCE ADVANTAGE, THE ONE THING WE CALL AN ASSET, DOES NOT REPRODUCE ON v102**

`+11.4 / +16.6 / +22.3pp` is the evidentiary floor under `THE FORWARD ROAD IS CLOSED` and under
the whole home-defence doctrine. Re-run with the same instrument (`events.tsv`, BUILD paired to
the next DEATH on the same tile and team, 50-round fixed horizon, censored builds dropped,
`d2_own ≤ 41` = HOME):

```
                 US n    US alive50    FIELD n   FIELD alive50    gap
Eir  HOME        5327       78.3%         8660       62.0%      +16.3pp   <- reproduces published
LOKI HOME         439       71.5%          520       81.5%      -10.0pp   <- sign flip
Eir  FAR         1383       35.1%         4627       60.8%      -25.7pp
LOKI FAR          361       11.6%          131       74.8%      -63.2pp
```

**Paired within opponent** (only opponents with n≥20 home turrets in *both* eras, because a
pooled flip is exactly where a mixture hides — method rule 7):

```
opponent               Eir gap      LOKI gap
farming_200s            +86.4        -22.6
Leviathan               +37.5        +23.8
CtrlAltDefeat           +22.3        +13.3
Kings College Munich    +11.2        -16.0
Powerpuff Girls         -14.6        -46.2
I Stone                 +18.2         +0.0  (both saturated at ~100%)
OopsGotYourElo           +9.0        -24.6
Memtrace                +16.3         +0.0  (both saturated at 100%)
```

**The gap narrows or flips in 5 of 8; it holds in 1; 2 are saturated and carry no
information.** Part of the pooled −10.0pp is mixture (Powerpuff Girls is 20% of v102's home
turrets and is negative in both eras), which is why the paired table matters — **and the paired
table still says the advantage shrank or reversed almost everywhere.**

**Stated at the honest strength:** n=439 v102 home turrets is enough to say *"does not
reproduce"*, and not enough to say *"is refuted"*. What is not defensible is quoting
`+11.4 / +16.6 / +22.3` as a current property.

### #3 — **BOTH "RESOLVING" FIXTURES WERE CERTIFIED BY AUDITS THAT NEVER TESTED TARGET SELECTION**

Rows 8-9 are a different kind of exposure from rows 1-7 and they are the reason I am not
reporting (a) as merely "rare". `cad_probe` and `orizon_probe` are the project's two resolving
fixtures. **`orizon_probe` was declared *"CLASS-VALID … usable as a field instrument"* and
`band_probe` *"USABLE AS A GUARD"* by two dedicated fidelity audits — and every predicate in
both audits tests opening, turret type, geometry, or lane fraction. Not one tests what the
probe shoots at.** The guard audit even states its own purpose as *"does a change break our
repair line, our harvester defence…"* — the precise quantities `best_core or best_any` makes
unreachable.

So the fixture problem is not four contaminated documents. **It is that the instrument that
exists to catch fixture defects has a blind spot in the same axis as the defect** — which is
the `\f`-in-the-grep-guard failure from `INDEX.md:54-60`, arriving in the fixture layer instead
of the quote layer. *A guard that has a blind spot is more dangerous than no guard.*

Prior art worth knowing: `cad-probe-refreeze-spec-2026-08-08.md` documented the **build-site
half** of the same core-only blindness two days early (P1: *"`_locate` accepts
`EntityType.CORE` only (`main.py:413-414`)"*; P8: zero builder attacks against wild CAD's 1,746
damage into our harvesters) and recommended the re-freeze. **The finding was available and the
fidelity audits did not consume it.**

### #4 — a smaller one, but it is *the biggest open question in the project* by its own label

Row 12. `open-questions.md:92-100` calls the per-map seat asymmetry *"worth several times what
the jackpot bug was"* on the strength of mirror-arena runs alone. **It has never been checked on
the ladder.** My cut of `join.tsv` × `meta_join.tsv` (our seat from `us_side`, n≥100 per map):

```
map            our seat a      our seat b      arena mirror claim
archipelago    47.6% (n=63)    43.5% (n=62)    seat A ~77-78%
atoll          51.5% (n=66)    54.7% (n=53)    seat A ~28-31%
heart          67.2% (n=58)    54.2% (n=59)    seat A ~31%
lighthouse     49.1% (n=55)    55.4% (n=65)    seat A ~28%
```

Direction agrees on 2 of 4 (atoll, lighthouse); **no map shows anything within 20 points of the
mirror magnitudes**, and heart points the opposite way. **The estimands differ** — a mirror
holds the bot constant and isolates terrain, while the ladder cut confounds opponent — so this
is not a refutation. It is the statement that **a claim carrying that much project priority has
one fixture behind it and the platform has never been asked.** Cheap to settle.

---

## 3. WHAT I COULD NOT TRACE, AND WHY

- **`1,471/1,472 throw events at d²≤2`** (`game-model.md:293`) — cited by nickname only
  (*"cad-fodder feasibility read"*); the denominator is in no named deliverable. **The
  mechanism survives on independent corroboration** (`clankers-noconfound:399`, 439/439), so
  this is an unsourced *figure*, not an unsupported *fact*.
- **the `68.4%` field chain-completion average** (`open-questions.md:126`) — no doc reproduces
  it and the population is unstated. Our 53% half traces to `tools/replay_census.py`.
- **harvester payback `~8 rounds / ~12 at 150%`** (`strategy-notes.md:53`) — traceable as
  arithmetic, untraceable as measurement. No empirical payback figure exists in the library,
  and the arithmetic omits two costs the file next door still lists as unanswered.
- **`"our opening is a near-constant"` on the current line** — not untraceable, but
  **unrecheckable**: v102 has ~40 games meeting the source's turns≥300 filter. Marked CLEAN
  with a note rather than guessed at, per method rule 6.

---

## 4. TWO THINGS ABOUT THE BRIEF ITSELF THAT I THINK ARE WRONG

1. **The figure is 99.83%, not 99.97%, and it is battery-set-specific rather than a property of
   the five probes.** `building-attackers-2026-08-10.md:644-658` — written by the author of the
   finding — reports that the same decoder over a **different 24-file arena population**
   (`ouroboros_probe` + `kladde_probe`, 8,325 turret shots) gives **46.1% core / 38.5% non-core
   / 10.8% bots**, and **13,056 `builderAttack` events** where the 480-game battery had zero.
   That cut did not include `cad_probe`, `band_probe`, `flotte_probe` or `orizon_probe`, so the
   two readings do not strictly contradict — **but "99.97% of that family's shots target our
   core" is a statement about one battery set, and it should carry that.** This is method rule 2
   applied to the brief.
2. **`ouroboros_probe` is a sixth bot with a hand-written variant of the same ordering**
   (`ouroboros_probe:1053`, per the discovery doc) while *not* matching the
   `best_core or best_any` grep — I verified the grep returns exactly the five. **If the
   behavioural family is six rather than five, `punishing-pool-2026-08-09.md` and
   `elo-weighted-battery-2026-08-08.md` §6 both move toward the line**, because the ouro leg is
   the strongest number in the hsb/hsd routing package. **Worth settling before this audit gets
   cited**, and I have deliberately not classified those two docs either way rather than guess.

---

## 5. WHETHER THE PRE-STATED EXPECTATION HELD

**It held, with one qualification that matters.** (c) ERA-DRIFT is **7** against (a)
PROBE-CONTAMINATED **4** and (b) FIXTURE-BLIND **2**, so population drift is indeed the bigger
contaminant by count — and by *severity*, since the (c) rows are the standing context the whole
library reads from, while three of the four (a) rows are individual deliverables.

**The qualification: (a) is not "rare" in the way the count suggests, because two of its four
rows are the certifications of the resolving fixtures themselves.** That is not four bad
documents; it is a bad *instrument*, and everything routed through it inherits. **The verdict
audit concluded the probe problem did not reach any decision. That is consistent with what I
found — and it is not the same as the probe problem being small.**

---

**Method notes, recorded because two of them nearly produced wrong numbers in this document.**
(1) `econ.tsv`'s `turns_run` is **unit-turns, not rounds** — my first pass at the ammo-band
instrument normalised by it and produced a per-side denominator mismatch of 1.5×; the table in
§2 is normalised by band-rounds reconstructed from `join.turns`. (2) `throws.tsv` column order
put `life` at field 13 and `core_atk` at 14; an off-by-one gave a 99.7% core-attack rate that
should have been obviously impossible, and was. (3) Turret-per-game figures use **games reaching
r200** as the denominator, not games with a build — the latter inflates by ~3×. (4) The paired
per-opponent turret table exists because the pooled flip in §2 could have been mixture, and
partly is.
