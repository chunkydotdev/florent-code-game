# In-bot opponent recognition: feasibility (2026-08-08)

**The design question.** Could one shipped bot work out *which opponent lineage it is
playing* from inside the game by ~round 15, so that per-lineage counter branches are
selected at runtime instead of us re-shipping a whole bot to counter a specific team?

---

## VERDICT

**Class-level lineage recognition by r15 is NOT feasible. Detection of one specific
opponent *action* is, and it is the only thing worth shipping.**

| question | answer |
|---|---|
| 8-way class recognition @ r15 | **NO.** 5-fold-CV accuracy **0.380** vs a 0.309 majority baseline — **62% error**, a 7 pp lift. Adding map identity: 0.407. |
| 8-way class recognition ever (r60) | **NO.** CV **0.459** at r60. The ceiling is a feature-set ceiling, not a timing one. |
| pairwise: cad-family vs economy | **YES-ish**, +28.5 pp lift @ r15 (the only pair above +20). |
| pairwise: everything else | **NO.** picket vs economy +4.5 pp, picket vs patient **−1.6 pp**, economy vs patient **−3.6 pp**, all-in-rush vs point-blank **+0.0 pp**. |
| "did the enemy just ferry a builder at us?" | **YES.** Precision **1.000** (0 false alarms in 880 games), recall 0.53 vs ground truth, fires median **r5**, and **median 5 rounds earlier than v85hsd's already-shipped threat trigger**. |
| is it early enough for the counters we care about? | **Mostly NO.** vs CtrlAltDefeat it precedes their first forward turret in only **38%** of games. vs Ouroboros it never fires at all. |
| do per-map priors beat recognition? | **For predicting the opponent, there is nothing to beat:** map-only CV is **0.266**, *below* the 0.309 majority baseline. Map and opponent are statistically independent — the ladder does not correlate them. Map priors are worth having for *geometry*, never for *identity*. |

**One-line recommendation:** do not build a lineage classifier. Build (or rather, extend
the existing threat latch with) a **ferry-detection flag** — it is free, it is
zero-false-positive, and it buys a median 5 rounds over what we ship today. Everything
else the archive says is: react to threat geometry, not to opponent identity.

---

## 0. Version tags and provenance

| | |
|---|---|
| Archive read | `replay_archive/` as of **2026-08-08 evening**: 2,756 files, 450 `*.meta.json`, 728 MB. Read-only. No games run, nothing downloaded, no platform calls. |
| Our matches in it | **176 matches / 880 games** (127 ladder-triggered), 35 distinct opponent teams, **2026-08-07T11:31Z → 2026-08-08T10:06Z**. |
| Our version span in corpus | v64 (9 matches) … v76 (5); heaviest at v72 (36), v68 (26), v75 (20). |
| Live at write time | **v76** on the slot (per `HANDOVER.md`); candidate lineage `bots/_v85hsd`. |
| Seat rule used | `docs/research/bo5-seat-assignment-2026-08-08.md`: metadata `teamAName` **IS** engine `TEAM_A`, fixed for all five games (158/158 matches, p=1.4e-132). So `teamAName=='OpenSverige'` → we are engine team 0. |
| Decode | stdlib protobuf reader per `tools/replay_schema.md`, built on `tools/replay_census.py`'s `fields()`. Scripts: session scratchpad `opp_recog/{vis,jobs,eval,eval2..eval7}.py`. |
| Prior decodes cited, not re-derived | `ouro-probe-refreeze-spec-2026-08-08.md`, `cad-probe-refreeze-spec-2026-08-08.md`, `cad-v116-first-read-2026-08-07.md`, `kings-college-classification-2026-08-07.md`, `orizon-family-2026-08-07.md`, `clankers-classification-2026-08-07.md`, `sporks-decode-2026-08-07.md`, `unclassified-five-2026-08-07.md`, `v72-bleed-{cad-family,nonfamily}-2026-08-08.md`, `v76-first-read-2026-08-08.md`, `elo-weighted-battery-2026-08-08.md`. |
| **Weekly map pool caveat** | The 15-map pool **rotates weekly** (`docs/runbook.md:42`) and the organisers have said it changed and stays hidden until the tournament (`docs/runbook.md:5`, `README.md:31-32`). **Every map-fingerprint number below has a one-week shelf life.** The map-prior conclusion (§5) does not depend on the pool and survives rotation. |

### 0.1 Vision model — stated explicitly, because everything hangs on it

For each round *r*, the set of tiles we can sense is the union over our living units of a
disc around that unit:

| unit | vision r² | modelled as |
|---|---|---|
| Core | 36 | nearest tile of the 2×2 footprint |
| Builder bot | 20 | its tile |
| Gunner / Sentinel / Launcher | 13 / 32 / 26 | its tile |
| Conveyor / Splitter / Harvester / Barrier | — | no vision |

An enemy entity counts as *seen* the first round it stands on a tile inside that union.
Three assumptions, all conservative:

1. **Visibility is evaluated at START of round r** (positions after round r−1's updates).
   An enemy building placed in round *r* is earliest-visible in *r+1*. Real detection is
   therefore **≤1 round earlier** than every number here.
2. **No line-of-sight occlusion is modelled.** The engine's `is_in_vision` is
   radius-only per the Controller reference, so this should be exact; if the engine ever
   adds occlusion, these numbers are optimistic.
3. **Our vision footprint is whatever our archived bots actually fielded.** Median **13
   living units at r15** (p10 = 9, p90 = 17) across 880 games. A future bot with a
   dedicated forward scout would see more; a leaner bot would see less. The counterfactual
   is not measured.

---

## 1. Feature inventory — what is actually visible to us, r0-r15

Only features computable from `Controller` getters are listed. Enemy ammo, enemy global
titanium, enemy `convert_ammo` cadence, enemy build costs and enemy stdout are **not
queryable** — every ammo-ladder signature in the decode docs (CAD's 8/8/8, sporks'
`convert_ammo(17)@r0`, Viktor's 50@r0, team lazy's 12/12/12) is **unusable in-bot.** That
alone strips the sharpest constants out of the classification docs.

### 1.1 Class-level table (fraction of games, all map sizes, r ≤ 15)

`ferry` = an enemy builder seen at manhattan distance from **their** core greater than it
could have walked (see §1.3). `fwd_turret` = enemy turret seen within d²≤50 of our core.
`pb_turret` = within d²≤13. `creep` = any enemy conveyor/splitter/harvester seen.
`raider` = enemy builder seen within d²≤25 of our core. `silence` = we saw nothing at all.

| class | n | ferry | fwd_turret | pb_turret | creep | raider | fire | silence | med #seen | med min-dist |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| point-blank | 215 | 0.20 | 0.58 | 0.46 | 0.34 | 0.19 | 0.53 | 0.19 | 5 | 3.0 |
| picket | 155 | 0.24 | 0.43 | 0.27 | 0.50 | 0.25 | 0.45 | 0.19 | 6 | 5.8 |
| economy | 135 | **0.03** | 0.30 | 0.10 | 0.46 | 0.13 | 0.29 | 0.34 | 4 | 5.7 |
| **cad-family** | 100 | **0.83** | 0.67 | 0.52 | 0.33 | 0.43 | 0.66 | **0.06** | 5 | 3.0 |
| all-in-rush | 45 | 0.38 | 0.64 | 0.20 | **0.09** | 0.24 | 0.64 | 0.11 | 4 | 4.0 |
| patient-melee | 30 | **0.00** | 0.30 | 0.17 | 0.50 | 0.10 | 0.37 | 0.27 | 4.5 | 6.4 |
| patient-standoff | 10 | 0.00 | 0.20 | 0.10 | 0.50 | 0.00 | 0.30 | 0.50 | 1 | 6.3 |
| heal-tank | 5 | 0.00 | 0.20 | 0.00 | 0.00 | 0.40 | 0.20 | 0.40 | 5 | 5.0 |
| unclassified | 185 | 0.13 | 0.47 | 0.34 | 0.44 | 0.10 | 0.48 | 0.23 | 4 | 4.2 |

**Read this table as a negative result.** Only the `ferry` column separates anything.
Every other column overlaps heavily: `fwd_turret` runs 0.30-0.67 across *all* classes,
`creep` 0.33-0.50 for four different classes, `silence` 0.06-0.50 with wide within-class
spread. A classifier fed the non-ferry columns is reading noise.

### 1.2 Per-lineage table (n ≥ 10 games, r ≤ 15)

| team | class | n | ferry | fwd_turret | pb_turret | creep | raider | silence | med ferry-detect r |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Powered by SmartFridge | unclassified | 80 | 0.26 | 0.55 | 0.53 | 0.29 | 0.10 | 0.16 | 7 |
| **Lunds Stallions** | picket* | 60 | **0.62** | 0.52 | 0.50 | 0.30 | 0.42 | 0.07 | 5 |
| Team 48 | point-blank | 55 | 0.13 | 0.47 | 0.47 | 0.31 | 0.05 | 0.25 | 10 |
| **CtrlAltDefeat** | cad-family | 55 | **0.75** | 0.76 | 0.55 | 0.33 | 0.55 | 0.09 | **3** |
| Powerpuff Girls | picket | 50 | 0.00 | 0.30 | 0.12 | 0.56 | 0.08 | 0.30 | — |
| **Ouroboros** | picket | 45 | **0.00** | 0.47 | 0.13 | 0.69 | 0.20 | 0.22 | — |
| gsxWins | point-blank | 45 | 0.53 | 0.71 | 0.42 | 0.49 | 0.33 | 0.16 | 6.5 |
| **Kings College Munich** | cad-family | 45 | **0.84** | 0.56 | 0.49 | 0.33 | 0.29 | 0.02 | 6 |
| OopsGotYourElo | economy | 45 | 0.02 | 0.31 | 0.16 | 0.38 | 0.13 | 0.33 | 14 |
| I Stone | economy | 45 | 0.00 | 0.16 | 0.02 | 0.49 | 0.13 | 0.36 | — |
| 0033 | economy | 40 | 0.00 | 0.50 | 0.15 | 0.55 | 0.15 | 0.28 | — |
| Askar City | point-blank | 35 | 0.14 | 0.51 | 0.49 | 0.09 | 0.29 | 0.20 | 8 |
| Leviathan | point-blank | 30 | 0.00 | 0.60 | 0.57 | 0.40 | 0.07 | 0.23 | — |
| Banminary | all-in-rush | 30 | 0.43 | 0.73 | 0.07 | 0.03 | 0.30 | 0.10 | 6 |
| Orizon | point-blank | 25 | 0.00 | 0.64 | 0.60 | 0.36 | 0.12 | 0.16 | — |
| sporks | unclassified | 25 | 0.00 | 0.52 | 0.16 | 0.52 | 0.04 | 0.32 | — |
| Memtrace | point-blank | 20 | 0.35 | 0.65 | 0.20 | 0.45 | 0.35 | 0.05 | 9 |
| Landers | patient-melee | 15 | 0.00 | 0.33 | 0.20 | 0.47 | 0.20 | 0.27 | — |
| Torsko | unclassified | 15 | 0.00 | 0.00 | 0.00 | 0.40 | 0.07 | **0.60** | — |
| farming_200s | all-in-rush | 15 | 0.00 | 0.47 | 0.47 | 0.20 | 0.13 | 0.13 | — |
| team lazy | unclassified | 10 | 0.00 | 0.90 | 0.90 | 0.90 | 0.30 | 0.10 | — |
| The Flotte Experience | unclassified | 10 | 0.00 | 0.60 | 0.00 | 0.60 | 0.00 | 0.10 | — |
| kladde chatte tville | patient-standoff | 10 | 0.00 | 0.20 | 0.10 | 0.50 | 0.00 | 0.50 | — |
| Pivot | unclassified | 10 | 0.00 | 0.30 | 0.30 | 0.60 | 0.10 | 0.40 | — |
| Pantheon | unclassified | 10 | 0.00 | 0.10 | 0.00 | 0.60 | 0.10 | 0.20 | — |
| Coreflood | patient-melee | 10 | 0.00 | 0.30 | 0.10 | 0.40 | 0.00 | 0.30 | — |

\* **Class-map correction, flagged.** Lunds Stallions is mapped to `picket` in
`elo-weighted-battery-2026-08-08.md`, but it ferries in 0.62 of games — stable across
their v37/v42/v44/v45 (5/5, 12/20, 11/20, 9/15). `v72-bleed-cad-family-2026-08-08.md`
§Q3 independently decoded Lunds v45 as launcher-at-r1 + one r3 mid-map throw, i.e. a
CAD-family *dialect* with a surviving launcher. **The ferry flag is not a proxy for the
`picket` class and the class map should not be read as if it were.**

### 1.3 The ferry test, and why it is the only clean one

An enemy builder spawns on a tile within the core's action radius (r²=8), so at most
manhattan-2 from the footprint, and thereafter moves ≤1 cardinal tile per round.
Therefore at round *r* it can be at manhattan ≤ *r*+2 from its own core, and

> **manhattan(enemy builder, their core) > r + 2 ⟹ it was thrown by a launcher.**

Their core position is available to us at **round 0** (`enemy_core_for(w,h,own)` in
`bots/_v85hsd/main.py:1043`, already written to `SLOT_ENEMY_CORE` on round 0), so this
is a two-subtraction test on entities we already enumerate.

**Ground-truth validation** — against actual `moveBuilderBot` events with |Δ| > 1 (which
is definitionally a launcher throw), over all 880 games:

| | count |
|---|---:|
| detector fires **and** a throw happened | 211 |
| detector fires, **no** throw happened (false alarm) | **0** |
| throw happened, detector missed (vision-limited) | 188 |
| neither | 481 |
| | **precision 1.000, recall 0.529** |

Zero false alarms at every map size (small/mid/large all 0.000 at both r15 and r60). The
margin is the reason: at margin 1 the test is unsound (a spawn at manhattan 2 trips it);
at margin 2 it is provably sound; at margin ≥ 4 recall collapses (cad-family drops
0.79 → 0.42).

The recall loss is **not** a class-behaviour question, it is a geometry question. Where a
throw actually happened by r15:

| class | small ≤16 | mid 17-22 | large ≥23 |
|---|---|---|---|
| cad-family | threw 0.71, **detected 0.50** | threw 1.00, **detected 0.90** | threw 0.98, **detected 0.86** |
| all-in-rush | threw 0.29, detected 1.00 | threw 0.64, detected 0.57 | threw 0.74, **detected 0.35** |
| point-blank | threw 0.46, detected 0.62 | threw 0.45, detected 0.52 | threw 0.43, **detected 0.39** |
| picket | threw 0.24, detected 1.00 | threw 0.24, detected 0.90 | threw 0.31, detected 0.79 |
| economy | threw 0.24, detected 0.17 | threw 0.21, detected 0.00 | threw 0.01, — |

Two distinct blind spots, worth separating:

- **Small maps: the throw is too short to be provably impossible.** On a 10×10 the whole
  map is 18 manhattan across; a throw of 4 tiles at r2 lands at manhattan 5 ≤ r+2 only
  just fails the test, and often passes it. This is a *soundness tax*, not a vision
  problem. (`cad-probe-refreeze` independently reports CAD builds **no launcher at all**
  on 10×10 — 4 of 5 v117 games — so the class behaviour changes there too.)
- **Large maps: the raider lands outside our vision.** Detection waits until it walks in.

### 1.4 Features that exist in the decode docs but are NOT observable early

Reproduced from the doc synthesis so nobody re-proposes them:

| signature | lineage | why unusable in-bot by r15 |
|---|---|---|
| `convert_ammo` ladders (8/8/8; 17@r0; 50@r0; 12/12/12; 20×4) | CAD, KCM, sporks, Viktor, team lazy, Orizon | **no API for enemy ammo or enemy conversions** |
| launcher built r1 adjacent to their core, self-destroyed r6 | CAD, KCM (25/25, 35/35) | at **their** core — outside our vision on every map ≥17 |
| builder spawn vectors (`r0,r1,r2,r8..`; five bots r0-r4) | Ouroboros, Clankers, sporks | at their core |
| home picket / home screen (22.6% of gunners at d>144) | Ouroboros, Clankers, sporks | their half |
| counterbattery latency (median 15.5 r) | CAD | only fires if **we** plant forward first |
| 0 splitters ever; harvester/conveyor counts at r25 | CAD, Ouroboros, sporks | their half |
| heal-line volume (2,600 heals / 5 games) | Clankers | their half |

---

## 2. Discriminability

### 2.1 Multi-class ceiling

`bayes ceiling` = accuracy if you memorised the empirical most-likely class per feature
cell (an over-fit upper bound). `CV` = honest 5-fold cross-validation, **split by match**
so the five games of a best-of-five never straddle the fold. 695 classified games, 8
classes, majority baseline **0.309**.

| round | behaviour-only ceiling | behaviour-only **CV** | +map ceiling | +map **CV** |
|---:|---:|---:|---:|---:|
| 10 | 0.485 | 0.361 | 0.574 | 0.390 |
| **15** | 0.517 | **0.380** | 0.639 | 0.407 |
| 20 | 0.576 | 0.429 | 0.709 | 0.458 |
| 30 | 0.555 | 0.403 | 0.701 | 0.416 |
| 60 | 0.563 | **0.459** | 0.668 | 0.442 |
| map only | — | — | 0.311 | **0.266** |

The gap between ceiling (0.52) and CV (0.38) is the over-fit; the gap between CV (0.38)
and baseline (0.31) is the real information. **7 percentage points.** Waiting to r60
buys 8 more, still under 0.46 — i.e. **more than half of all games would be routed to the
wrong counter branch**, forever, at any round.

### 2.2 Pairwise separability (CV lift in pp over that pair's majority baseline)

Negative or near-zero means "the features are worse than always guessing the bigger
class."

**@ r15:**

| | all-in-rush | point-blank | picket | economy | patient-melee |
|---|---:|---:|---:|---:|---:|
| **cad-family** | +5.5 (145) | +10.2 (315) | +18.4 (255) | **+28.5** (235) | +3.1 (130) |
| **all-in-rush** | | **+0.0** (260) | +8.0 (200) | +7.8 (180) | +6.7 (75) |
| **point-blank** | | | +5.9 (370) | +11.1 (350) | **+0.0** (245) |
| **picket** | | | | +4.5 (290) | **−1.6** (185) |
| **economy** | | | | | **−3.6** (165) |

**@ r30** the picture barely moves (cad-vs-economy +26.4, point-blank-vs-economy +21.4,
all-in-rush-vs-point-blank **−0.4**, economy-vs-patient **−8.5**).

Everything above +18 pp is the ferry column doing the work. Strip ferry and there is no
usable pair.

### 2.3 Map-size split

`cad-family` (the one separable class) vs each other class, r15 CV lift:

| | small ≤16 | mid 17-22 | large ≥23 |
|---|---|---|---|
| vs point-blank | **−2.0** (n=49) | +5.9 (68) | +11.6 (198) |
| vs picket | +10.3 (39) | +22.6 (62) | +20.8 (154) |
| vs economy | +15.4 (39) | **+28.9** (45) | **+29.1** (151) |
| vs all-in-rush | — | +6.2 (32) | +5.4 (92) |
| vs patient-melee | — | +0.0 (27) | +1.2 (82) |

**This inverts the intuition in the brief.** Small maps are the *worst* case, not the
best. The reason is §1.3: on a small map everything is visible but the ferry test cannot
prove a short throw impossible, so the one informative feature goes dark. Large maps
lose vision but keep the ferry test sound, because the throws are long.

Earliest round at which ≥80% / ≥90% of games show *anything at all* in our vision:

| class | small ≤16 | mid 17-22 | large ≥23 |
|---|---|---|---|
| cad-family | r80=7 r90=7 | r80=5 r90=6 | r80=11 r90=14 |
| all-in-rush | r80=10 r90=12 | r80=6 r90=7 | r80=15 r90=22 |
| point-blank | r80=8 r90=11 | r80=9 r90=15 | r80=17 r90=20 |
| picket | r80=11 r90=13 | r80=8 r90=10 | r80=21 r90=24 |
| economy | r80=11 r90=14 | r80=16 r90=16 | r80=18 r90=21 |
| patient-melee | r80=15 r90=16 | r80=13 r90=15 | r80=19 r90=23 |

So on large maps we do not reliably see *anything* until r17-24 — but seeing something is
not the bottleneck. The bottleneck is that what we see is not diagnostic.

---

## 3. Later-round fallback, and where recognition arrives TOO LATE

### 3.1 There is no useful later round

§2.1 already answers it: CV accuracy is 0.380 @ r15 and 0.459 @ r60. The curve is flat
because the missing information is *categorical* (enemy ammo, enemy base geometry), not
*temporal*. **Waiting does not fix a feature-set problem.** Do not spend a rev on "same
classifier, later trigger."

### 3.2 The ferry flag vs the deadlines it would have to beat

The counter that a ferry flag would gate is an anti-insertion guard (barrier/turret on
the landing ring, or a defensive turret pulled forward in the build order). Its deadline
is whichever comes first: the raider reaching our core ring, or their forward turret
going up.

| deadline | n | median lead | p10 | p90 | frac lead ≤ 0 | frac lead ≥ 3 |
|---|---:|---:|---:|---:|---:|---:|
| enemy entity reaches d ≤ 5 of our core | 205 | **+3** | 0 | 9 | 0.31 | 0.52 |
| enemy entity reaches the core-adjacent ring (d ≤ 2.8) | 178 | **+8** | 0 | 29 | 0.12 | **0.84** |
| first enemy turret planted within d ≤ 7 of our core | 187 | **+4** | −1 | 20 | 0.31 | 0.49 |

So: **~4-8 rounds of warning against the thing that actually kills us (a turret or a
raider on the core ring), 84% of the time ≥3 rounds.** That is a real, usable window —
enough to place one barrier or bring one turret forward.

### 3.3 TOO-LATE FLAGS — per counter lever

| counter lever | its commitment window | when recognition arrives | verdict |
|---|---|---|---|
| **anti-Ouroboros early standoff sentinel** (commit ~r5-15) | r5-15 | **never** — Ouroboros ferry rate **0.00** in 45/45 games, and its r15 profile (silence 0.22, creep 0.69, fwd_turret 0.47) is statistically indistinguishable from `economy` (0.34/0.46/0.30) and from Powerpuff (0.30/0.56/0.30). Ouro's first gunner is *placed* at median r16 — after the window closes. | **TOO LATE / IMPOSSIBLE.** This lever can only ever be gated on map geometry or shipped unconditionally. |
| **anti-CAD insertion guard** | r2-5 (`cad-probe-refreeze`: throw r2, forward turret r3, first blood r4-5) | ferry flag median **r3** for CtrlAltDefeat — but it precedes their first forward turret in only **0.38** of games, and 0.40 of CAD games already have a forward turret planted **by r3**. | **TOO LATE for CAD proper.** For **KCM** it is better: median detect r6 vs forward turret r7, precedes in **0.81** of games. |
| **anti-rush early defensive turret** | r5-10 (all-in-rush first near-turret median r10, p10=2) | ferry median r7.5, precedes in 0.62 (n=16 only) | **MARGINAL**, and thin. |
| **anti-point-blank** | first near-turret median r12, p10=4 | ferry median r9, precedes in 0.60 (n=48) | **MARGINAL.** Leviathan (the sharpest point-blank threat, gunner at d²≤9 median r12 per `v72-bleed-nonfamily` §3) **never trips the ferry flag** — 0/30 games. |
| **generic threat latch (already shipped)** | continuous | see §3.4 | **works today; the ferry flag improves it.** |

### 3.4 Marginal value over what we already ship

`bots/_v85hsd/main.py:1430-1445` already latches `SLOT_UNDER`/`SLOT_THREAT` on: enemy
GUNNER/SENTINEL within d²≤64 of the core, enemy BUILDER_BOT within d²≤16 of the core, or
a core HP drop. Comparing the ferry flag to that shipped trigger, on the same games:

| | |
|---|---|
| both fire (n=184) | ferry **earlier 125 (0.68)**, same round 57 (0.31), later **2** |
| median rounds ferry precedes the shipped trigger | **5.0** (p75 = 10, p90 = 21) |
| ferry fires and the shipped trigger never does (by r60) | **27 games** |
| shipped fires and ferry never does | 514 games |

Per class, median lead of the ferry flag over the shipped trigger: cad-family **+3.0**,
all-in-rush +2.5, point-blank +6.0, picket **+11.0**, unclassified +9.0.

**This is the whole business case.** Not "know who you're playing" — *"know 5 rounds
sooner that a builder is being thrown at you."*

---

## 4. Robustness / decay under churn

| feature | stability evidence | verdict |
|---|---|---|
| **ferry test** (physics-based) | Depends on **no** opponent constant. It follows from move rules + core action radius. Cannot decay unless the engine changes. | **PERMANENT** |
| ferry *rate* per team | CAD: v107 8/10, v116 9/10, v117 24/35 (0.69-0.90). KCM: v1 38/45 (0.84). Lunds: v37 5/5, v42 12/20, v44 11/20, v45 9/15. gsxWins: v18 5/10, v19 3/5, v20 5/10, v22 11/20. | **STABLE across every observed version bump.** Corroborates `cad-probe-refreeze` P7 (opening byte-stable v107→v116→v117) and `kings-college` (invariant across v7 and v1). |
| ferry rate per team, downward drift | none observed; but Lunds shipped v37→v47 inside 24h (`ouro-refreeze` §5.3.4) and only v45 is decoded. | watch |
| the *class map* itself | Lunds is mis-classed (§1.2); Askar City is "convergent, not family" (`orizon-family` §6); `0033` was reclassified once already. | **the class map decays faster than any behaviour we measured** — a further argument against branching on class |
| map fingerprints | pool rotates weekly and is hidden until the tournament | **one-week shelf life** |
| 10×10 branch behaviour | CAD and KCM both run a *different bot* on 10×10 (no launcher; point-blank gunners from r1) | any ferry-gated counter must **not** be the 10×10 plan |

---

## 5. Per-map priors vs runtime recognition

### 5.1 Map priors cannot predict the opponent — measured, not assumed

Global class mix over 695 classified games: point-blank 0.31, picket 0.22, economy 0.19,
cad-family 0.14, all-in-rush 0.06, patient-melee 0.04, patient-standoff 0.01,
heal-tank 0.01. Per-map top-class share, for every map with n ≥ 20:

| map (w,h,coreA,coreB) | n | top class | share | global share |
|---|---:|---|---:|---:|
| (26,26,5,5,19,19) | 103 | point-blank | 0.27 | 0.31 |
| (28,20,7,9,19,9) | 96 | point-blank | 0.31 | 0.31 |
| (18,18,2,14,14,2) | 56 | point-blank | 0.30 | 0.31 |
| (25,15,11,3,11,10) | 53 | point-blank | 0.30 | 0.31 |
| (24,24,4,4,18,18) | 49 | point-blank | 0.33 | 0.31 |
| (14,18,6,4,6,12) | 48 | point-blank | 0.35 | 0.31 |
| (21,8,5,3,14,3) | 47 | picket | 0.30 | 0.22 |
| (25,25,5,5,18,18) | 46 | point-blank | 0.30 | 0.31 |
| (20,26,9,6,9,18) | 45 | point-blank | 0.40 | 0.31 |
| (16,16,3,3,11,11) | 43 | economy | 0.28 | 0.19 |
| (16,16,0,0,14,14) | 38 | point-blank | 0.32 | 0.31 |
| (10,10,2,2,6,6) | 36 | point-blank | 0.31 | 0.31 |
| (25,25,2,20,21,3) | 35 | point-blank | 0.31 | 0.31 |

Every per-map share sits on the global share. Formally: a map-only classifier scores
**CV 0.266**, *below* the 0.309 majority baseline. **Map and opponent are independent.**
The ladder draws maps without regard to whom you are paired with, exactly as expected.

### 5.2 What map priors ARE good for

Map identity is nearly free and perfectly reliable: `known_map_for(w, h, own_core, ct)`
(`bots/_v85hsd/main.py:1053`) resolves the exact terrain grid at round 0 from dims +
core anchors, disambiguating the two 26×26 and the eider/heart collision from sensed
terrain. Our seat is known at round 0 too (`ct.get_team()`, plus core position).

So the map buys **geometry**, and geometry is where the archive says the leverage is:

- **Core separation predicts threat timing far better than class does.** First enemy
  entity reaching d≤5 of our core: cad-family median r7, all-in-rush r6, point-blank r9,
  picket r11, economy r14, patient-melee r19 — a 13-round spread across classes. But
  `ouro-refreeze` §5.1 documents Ouroboros' *own* first gunner moving r2-r10 (D≤9) vs
  r19-r57 (D≥17) purely on map separation — a larger swing than the entire between-class
  spread, from one lineage.
- The same doc set supplies map-keyed rules that need **no** identification: sporks is
  9W-0L on cardinal-axis maps and 6W-10L on diagonal (`sporks-decode` §per-map);
  `v76-first-read` Law 5 — all 6 wins at core separation d²≤81, 8 of 9 losses at d²≥144;
  CAD is 0-5 on 10×10.

### 5.3 Expected-value comparison

| design | information gained | error rate | cost | assessment |
|---|---|---|---|---|
| **runtime class recognition** | 7 pp over prior @ r15 | **62% misroute** | new feature code, needs a store slot, needs per-class branches, decays with the class map | **negative EV.** A branch that fires on the wrong class 62% of the time applies the wrong counter more often than the right one; each wrong counter costs tempo against a class it was not designed for. |
| **per-map priors on opponent identity** | **0 pp** (below baseline) | worse than guessing | — | **worthless. Do not build.** |
| **per-map priors on geometry** (core separation, axis, wall density, throw-landing tiles) | large and reliable | n/a — no classification involved | already half-built (`known_map_for`, `enemy_core_for`, `_plan_siege`) | **positive EV**, and it is what the existing map tables already serve |
| **ferry flag (threat detection, no identity)** | median **5 rounds** of extra warning, **zero** false alarms | 0.00 FPR; 0.47 miss rate (misses are silent, i.e. degrade to today's behaviour) | ~10 lines inside an existing loop, no new slot needed | **positive EV, smallest scope.** Recommended. |

**The map-prior-vs-recognition question resolves as neither.** Map priors are useless for
identity; recognition is too inaccurate for identity. The thing that pays is a
physics-derived *threat* detector that is agnostic to who is on the other side.

---

## 6. Implementability sketch (ferry flag only)

### 6.1 Store slots — there are none free

`bots/_v85hsd/main.py:816-846` uses **all 16 slots**: 0 `ROLE_N`, 1 `UNDER`, 2 `ATK_RND`,
3 `ENEMY_CORE`, 4 `HARVESTERS`, 5 `ECO_READY`, 6 `LAUNCHER`, 7 `HOME_GUN`, 8 `DROPPED`,
9 `HEAL_BUDGET`, 10 `LAUNCH_ID`, 11 `LAUNCH_RND`, 12 `LAUNCHED_ID`, 13 `DEFEND_BEAT`,
14 `THREAT`, 15 `SIEGE`.

**No new slot is needed.** `SLOT_UNDER` is currently written as 0/1; widen its domain to
0 = clear, 1 = threat, **2 = ferried insertion** (a strictly stronger threat). Verified:
**all eight** read sites test truthiness only — `!= 0` at lines 1809, 2168, 2176, 3070,
3370, 3676 and bare truthiness at 2196, 2421 — so a value of 2 is backward-compatible
with every one of them, and the new branch tests `== 2`. `SLOT_THREAT` already carries
the packed position. No migration work beyond that grep.

### 6.2 Code — rides inside the loop that already exists

The threat scan at `main.py:1430` already iterates `ct.get_nearby_entities()` and already
calls `get_team` / `get_entity_type` / `get_position` on each. The addition is one
manhattan distance against a value already in the store:

```python
# inside the existing `for eid in ct.get_nearby_entities():` loop, after the
# team check, alongside the existing BUILDER_BOT branch:
if et == EntityType.BUILDER_BOT:
    ep = ct.get_position(eid)
    ec = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))   # written round 0
    if ec is not None:
        # nearest tile of their 2x2 footprint
        mdx = 0 if ec.x <= ep.x <= ec.x + 1 else min(abs(ep.x - ec.x), abs(ep.x - ec.x - 1))
        mdy = 0 if ec.y <= ep.y <= ec.y + 1 else min(abs(ep.y - ec.y), abs(ep.y - ec.y - 1))
        # spawn ring is manhattan<=2 (core action r^2=8); walk is 1/round.
        if mdx + mdy > ct.get_current_round() + 2:
            under = True
            threat = ep
            ct.write_store(SLOT_THREAT, pack_pos(ep))
            ct.write_store(SLOT_UNDER, 2)      # 2 == ferried insertion
            break
```

**CPU:** the enclosing loop already runs. The marginal work is one `read_store`, one
`unpack_pos`, six comparisons and two adds **per enemy builder in vision** — bounded by
the enemy's builder count (median ≤6 in every lineage decoded). Well under 50 µs against
the 10 ms/unit budget; `get_cpu_time_elapsed()` gating is unnecessary. No map sweep, no
`get_nearby_tiles()`, no per-round recomputation.

**Correctness guards:** `unpack_pos` returns `None` before round 0's write lands (the
store is write-buffered), so the `is not None` check is load-bearing — without it the
first round raises and, per the engine rule, **permanently destroys the unit**. The whole
block belongs inside the existing try/except discipline.

### 6.3 What the flag must NOT be wired to

- **Not to a 10×10 branch.** CAD and KCM both run a launcher-free point-blank bot there
  (`cad-probe-refreeze` §3.1, `kings-college` §2.1) and the test's recall on small maps is
  0.50 anyway.
- **Not to a "this is CtrlAltDefeat" conclusion.** Precision for the *action* is 1.000;
  precision for "this is cad-family" is **0.457** (79 tp / 94 fp). Six teams across four
  classes ferry.
- **Not to a barrier on the landing tile.** `cad-probe-refreeze` §3.2 established CAD
  carries a *ranked* destination list and skips impassable tiles, re-acquiring the
  preferred tile on a later throw — **a barrier displaces, it does not deny.**

---

## 7. Self-checks

**Archive coverage per lineage (n games, of 880).** point-blank 215 (Team 48 55, gsxWins
45, Askar City 35, Leviathan 30, Orizon 25, Memtrace 20, SingleCore 5); picket 155 (Lunds
60, Powerpuff 50, Ouroboros 45); cad-family 100 (CtrlAltDefeat 55, KCM 45); economy 135
(OopsGotYourElo 45, I Stone 45, 0033 40, Viktor5776 5); all-in-rush 45 (Banminary 30,
farming_200s 15); patient-melee 30 (Landers 15, Coreflood 10, Jacobs Code 5);
patient-standoff 10 (kladde); heal-tank 5 (Clankers); unclassified 185 (SmartFridge 80,
sporks 25, Torsko 15, team lazy 10, Flotte 10, Pivot 10, Pantheon 10, + 6 teams at 5).

**Underpowered rows, do not act on alone:** heal-tank (n=5), patient-standoff (n=10),
Jacobs Code / Viktor5776 / SingleCore / Clankers (n=5 each), and the all-in-rush
lead-time cell (n=16). Cookie is in the class map but has **zero** games in this archive
(its `docs/opponents.md` entry predates it).

**Assumptions restated.** (1) Seat rule from `bo5-seat-assignment` taken as given — it is
the load-bearing input and is itself validated at p=1.4e-132. (2) Vision is radius-only,
no occlusion. (3) Visibility evaluated at start-of-round, so all detection rounds are
pessimistic by ≤1. (4) Our vision footprint = what our v64-v76 bots actually fielded
(median 13 units at r15); a scouting rev would shift recall upward and is not modelled.
(5) CV folds split by **match**, not game, so a series' five games never straddle a fold —
without this, accuracy inflates by several points on opponents we played repeatedly.
(6) The class→team map is inherited from `elo-weighted-battery-2026-08-08.md` §1 and is
**wrong for Lunds Stallions** on this evidence (§1.2); the multi-class numbers in §2.1
therefore carry an unknown amount of *label* noise, which biases them **upward** relative
to a corrected map — the negative verdict is safe.

**One prediction this doc makes, for later falsification.** If the ferry flag is shipped,
it should latch before the current `SLOT_UNDER` trigger in roughly **2 of 3** games
against CtrlAltDefeat / KCM / Lunds / gsxWins / Banminary / Memtrace, by a median of
about **5 rounds**, and it should **never** latch against Ouroboros, Orizon, Leviathan,
Team 48, I Stone, 0033, farming_200s, sporks, kladde, Landers or Coreflood. Any latch
against that second list is a bug in the manhattan bound, not a new opponent behaviour.
