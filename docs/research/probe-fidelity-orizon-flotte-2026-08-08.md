# Probe fidelity: `orizon_probe` and `flotte_probe` vs wild play — 2026-08-08

**Research arm, archive-only.** No bot edits, no arena runs, no local matches, no
platform downloads. Everything below is measured from `replay_archive/` on disk.

| Thing | Version / stamp |
|---|---|
| Live submission | v80 "Eir 9b" = `bots/_v89sh/main.py`, md5 `e12f85855654e9e78227582d0dc15d4b` (verified on disk) |
| `bots/orizon_probe/main.py` | frozen instrument; provenance header cites `thread7_landers_orizon.md` (6 games, our v53→v56→v61) + `orizon-family-2026-08-07.md` §1-5 (18 games, incl. `607ffaeb` = Orizon **v34**). Extraction 2026-08-07 |
| `bots/flotte_probe/main.py` | frozen instrument; provenance header cites platform match `0a88ca71` games 3-4, played against our live **v7**. Extraction 2026-08-06 |
| Wild corpus | `replay_archive/` — 554 matches / 2,770 replays on disk; 81 matches involve one of the five subject teams; **405 games / 810 team-sides parsed** for this read |
| Measurement code | scratchpad harness over `tools/replay_census.py` primitives; no `BotOutput` dependency anywhere |

**None of the extraction-source matches are in the archive** (`0a88ca71`,
`607ffaeb`, `bce041d8`, `a72b53f9`, `c106d3d2`, `d9a67e82` — all absent). The
control cohorts below are therefore *proxies* for the extraction moment, not the
extraction games themselves. For Orizon the proxy is strong (control cohort is
the same version, v34, as the extraction series). For Flotte it is weak (the
extraction version is unknown and unrecoverable; nearest archive version is v35,
~1 day later).

---

## 0. Bottom line

| Probe | Verdict | Confidence | Disposition |
|---|---|---|---|
| `orizon_probe` | **CLASS-VALID** | High on the type/geometry predicates, medium on magnitude | **Usable as a field instrument** for the Orizon-team point-blank battery class, with two named qualifications (execution-reliability inflation; gunner-heal is Orizon-only within the family). No re-freeze. |
| `flotte_probe` | **CLASS-DRIFTED**, and two predicates were **never valid** | High | **Attribution-only. Needs a re-freeze.** The payload (small fixed economy + saboteur + deep sentinel) is real and got *stronger*; the turret/launcher layer is wrong and was wrong at extraction. |

The `+11.6` orizon separation is **not** a straw-opponent artifact in kind — wild
Orizon v34 plays exactly the mechanism the probe reproduces, at 100% turret-type
purity — but it *is* inflated in degree: the probe fires the pattern in 100% of
games, wild Orizon in roughly 60-70%. Detail in §2.5.

The Flotte leg (91.7 vs 86.7, overlapping) is measuring a bot that builds ~2
launchers per game and rebuilds 13-15 gunners; the probe builds zero launchers
and caps at 2 gunners for the whole match. That leg is a matchup artifact on the
turret axis, in the same family as the cad case.

---

## 1. Method

Predicates are derived **from each probe's own source** (§2.1, §3.1), stated as
counting tests with thresholds, then measured on wild games from entity
positions and engine events. Two cohorts per probe:

* **RECENT** — games completed on 2026-08-08 (most recent archived play).
* **CONTROL** — games completed on 2026-08-07, i.e. adjacent to the extraction
  date. The control cohort exists to prove the *measurement method* reproduces
  the signature at the time it was extracted; a predicate that fails in both
  cohorts is an **extraction defect**, not drift.

Geometry conventions:

* `fp_dsq` — squared distance from a tile to the **nearest enemy Core footprint
  tile** (the thread7 / denial-book convention). `fp_dsq ≤ 13` = a gunner
  standing there is in range of the Core; `≤ 4` = point-blank.
* `lane frac` — for a turret, `d(own core) / core separation`; for a builder,
  `d_home / (d_home + d_enemy)`, so 0 = own Core, 1 = enemy Core. Used instead
  of raw distance because map sizes range 10x10 to 28x20 and an absolute
  threshold silently changes meaning between maps.
* `in-range frac` — the fraction of a team's gunner **plants** that landed at
  `fp_dsq ≤ 13`. This is the sharpest single number in the whole read, because
  `orizon_probe` has it pinned at **1.00 by construction**.
* `core-shot frac` — the fraction of a team's turret shots whose target tile was
  an enemy Core footprint tile.
* `crosser` — a builder bot that reaches lane frac ≥ 0.70; "stay" = it never
  came back below 0.35 afterwards.

---

## 2. `orizon_probe`

### 2.1 Signature derived from the probe source

From the module docstring and the code that implements it
(`bots/orizon_probe/main.py`):

| # | Predicate (testable) | Threshold | Source in the probe |
|---|---|---|---|
| O1 | Exactly 4 builder bots, spawned r0-r3, never another | `n_bots == 4` | `BUILDER_TARGET = 4`, `_run_core` returns once `spawned >= BUILDER_TARGET` |
| O2 | Zero sentinels, ever | `n_sentinel == 0` | no `build_sentinel` call exists in the file |
| O3 | Zero launchers, ever | `n_launcher == 0` | no `build_launcher` call exists |
| O4 | Zero barriers, ever | `n_barrier == 0` | no `build_barrier` call exists |
| O5 | Economy is a stub: ≤4 harvesters + short conveyor run | `n_harvester ≤ 4` | `HARVESTER_TARGET = 3`, `MAX_CHAIN = 8`, `ECO_GIVEUP_RND = 60` |
| O6 | First gunner planted early, already in range of the enemy Core | `first plant r ≤ 25` and `fp_dsq ≤ 13` | `_plant_gunner` gated on `can_fire_from(site, facing, GUNNER, core_tile)` |
| O7 | Plants creep to point-blank | `min fp_dsq ≤ 4` | plant sites ranked `(shadowed, fp_dsq, x, y)`, closest wins |
| O8 | A sustained multi-gun battery on the Core | `≥2 gunners alive at fp_dsq ≤ 13 simultaneously` | no gunner cap below `GUNNER_TARGET = 16`; guns are never destroyed by the probe |
| O9 | Ammo pump: convert nearly every round, hold little titanium | `convert rate ≥ 0.4`, `median titanium ≤ 60` | `_convert` runs every round, `amount = min(ti - reserve, 20)` |
| O10 | 116-207 gunner shots per game | `shots ≥ 100` | consequence of O9 + the battery |
| O11 | Builders heal their own gunners | `≥3 heals on own gunners` | `_heal_adjacent`, gunners ranked first |
| O12 | Forward builders never melee | `builder attacks ≈ 0` | deliberate deviation, documented in the docstring |
| O13 | A lancer walks at the enemy Core from r0 | `≥1 crosser`, early | `ROLE_LANCER`, `_forward_move` with `lancer=True` |
| O14 | **Every** gunner plant is Core-aligned and in range | `in-range frac == 1.00` | structural: `_plant_gunner` only accepts sites that pass `can_fire_from` on a Core footprint tile |
| O15 | Never rotates | — | no `rotate()` call exists |

O14 is not stated as a claim in the docstring; it is an unavoidable consequence
of the plant gate, and it turns out to be the load-bearing difference against
wild play (§2.5). O15 is **unmeasurable in this format** — the replay schema has
no direction-update message, and `placeEntity` re-emissions do not track
rotation reliably; it is excluded from the verdict.

### 2.2 Wild corpus

Orizon is **v34 in every archived game**, 2026-08-07T13:06 through
2026-08-08T14:48 — including the extraction series' version. Orizon has not
shipped a new submission inside the archive window, so for this probe the usual
"probe is N versions stale" concern does not apply at all.

| Cohort | Matches | Games | Version | Opponents | Rated |
|---|---|---|---|---|---|
| RECENT | `c99aa374`, `ecde38a8` (2026-08-08) | 10 | v34 | Viktor5776 v3, Kleos v56 (**third parties, not us**) | both ladder |
| CONTROL | `047ea519`, `123ca2f6`, `646e8a3a`, `8a5ea626`, `9f457fb1`, `50ca5e87` (2026-08-07) | 30 | v34 | OpenSverige v64/65/68/69 (us) ×25, Memtrace v28 ×5 | 5 ladder matches + 1 unrated |

Family context (the probe claims to instrument a 4-team block, "~46% of the
field"): `team lazy` (110 games, v88→v147), `Team 48` (90 games, v16 throughout),
`Leviathan` (75 games, v9→v32) were measured on the same predicates for §2.6.

### 2.3 Predicate results

| # | Predicate | CONTROL (30 games, v34) | RECENT (10 games, v34) | Read |
|---|---|---|---|---|
| O1 | `n_bots == 4` | 17/30 (57%) | 6/10 (60%) | **PARTIAL** — median 4, but long games respawn (max 28 bots). The probe's docstring already declares it freezes the short-game rule; confirmed, and the deviation is on the record. |
| O2 | zero sentinels | **30/30 (100%)** | **10/10 (100%)** | HOLDS |
| O3 | zero launchers | **30/30 (100%)** | **10/10 (100%)** | HOLDS |
| O4 | zero barriers | 23/30 (77%) | 8/10 (80%) | MOSTLY — 1-12 barriers in 7 control / 2 recent games. Pre-existing, small. |
| O5 | `n_harvester ≤ 4` | 25/30 (83%), median 2 | 7/10 (70%), median 3 | HOLDS |
| O6 | first plant `fp_dsq ≤ 13` | 20/30 (67%), median r8 | 8/10 (80%), median r24 | HOLDS |
| O7 | `min fp_dsq ≤ 4` | 19/30 (63%) | 8/10 (80%) | HOLDS (`≤13`: 29/30, 10/10) |
| O8 | `≥2` point-blank gunners alive | 26/30 (87%) | **10/10 (100%)** | HOLDS |
| O9 | convert rate ≥0.4 / median Ti ≤60 | 19/30 (63%) / 22/30 (73%) | 4/10 (40%) / **10/10 (100%)** | HOLDS on the titanium-band form; the "nearly every round" form is optimistic (wild median rate 0.44 / 0.32) |
| O10 | shots ≥100 | 23/30 (77%), median **280** | **10/10 (100%)**, median **270** | HOLDS — wild fires *more* than the decode's 116-207 band |
| O11 | ≥3 heals on own gunners | 16/30 (53%) | 5/10 (50%) | HOLDS for Orizon; see §2.6 — this is the family split |
| O12 | no builder melee | median 0 (13 events total, all onto turrets) | median 0 (34 events, all onto gunners) | HOLDS |
| O13 | ≥1 crosser | 29/30 (97%), earliest median r17 | 10/10 (100%), earliest median r20.5 | HOLDS |
| O14 | in-range frac == 1.00 | **3/30 (10%)**, median **0.46** | **3/10 (30%)**, median **0.62** | **DIVERGES** — see §2.5 |

### 2.4 Verdict — **CLASS-VALID**

The signature still describes Orizon's current play, and the strongest form of
that statement is available here: **the subject has not changed version.** Wild
Orizon is v34 in the extraction series and v34 in its two most recent archived
matches. Every type-level predicate that defines the class — gunner-only,
zero sentinels, zero launchers, tiny stub economy, lancer from r0, creep to
point-blank, ammunition pump, gunner-healing builders — reproduces at 50-100% in
both cohorts, and the recent cohort is *cleaner* on the battery predicates than
the control cohort (O7 63%→80%, O8 87%→100%, O10 77%→100%).

**Confidence: high** on the type and geometry predicates (they are counting
tests over 40 games with a validated parser), **medium** on magnitude (the
recent cohort is 10 games from 2 matches against two opponents we have never
played, so the absolute rates carry a wide interval).

**What would change the answer:** (a) Orizon shipping v35+ — the whole verdict
rests on version identity, and the archive's most recent Orizon game is
2026-08-08T14:48; (b) a recent cohort against defenders resembling ours (both
recent matches are vs third parties — Viktor5776 and Kleos — so the measured
plant geometry is partly a response to *their* defence, not ours); (c) evidence
that the family members diverged enough that "Orizon class" no longer implies
"~46% of the field" (see §2.6 — this is already partly true).

### 2.5 The straw-opponent question — is the mechanism the same?

**Answer: same mechanism, inflated firing rate. The `+11.6` is real in kind and
optimistic in degree.**

*Same in kind.* Wild Orizon v34 builds gunners and nothing else — zero
sentinels and zero launchers in 40/40 games — walks a builder at our Core from
r0 (crosser in 39/40 games), plants inside gunner range of the Core footprint
(`fp_dsq ≤ 13` reached in 39/40 games, `≤ 4` in 27/40), keeps 2+ point-blank
guns alive simultaneously in 36/40 games, and pumps titanium into ammunition at
a median 0.32-0.44 converts/round while holding its bank in the 0-60 band. That
is the probe's mechanism, not an invention.

*Inflated in degree, on two measurable axes.*

**(1) Plant purity / execution reliability.** `orizon_probe` accepts a plant
site only if a hypothetical gunner there passes `can_fire_from` against a Core
footprint tile, so **100% of its gunners shoot the Core**. Wild Orizon:

| | CONTROL (30 games) | RECENT (10 games) |
|---|---|---|
| in-range frac, median | **0.46** | **0.62** |
| games at 1.00 | 3/30 | 3/10 |
| games below 0.50 | **15/30** | **4/10** |
| core-shot frac, median | 0.69 | 0.75 |

Half of wild Orizon's gunners in the control cohort, and a third in the recent
cohort, are planted where they cannot shoot the Core at all. This is the same
thing `orizon-family-2026-08-07.md` §1 recorded as "Orizon is visibly failing to
execute its own script" — measured here as a rate rather than described. The
probe never fails. So a defence tuned against the probe is being graded on the
*best-case* presentation of the class, at roughly 1.6× (recent) to 2.2×
(control) the wild concentration of Core-directed guns.

Direction of the bias: the probe is **harder** than average wild Orizon per
game. That means a defensive fix that wins on the probe is not being flattered
by a weak opponent — but the *field value* of that fix is the probe margin
times the wild rate at which the pattern actually fires, and that rate is not 1.
Taking `in-range frac ≥ 0.5` as "the pattern fired", it is 15/30 in control and
6/10 in recent. A first-order field-weighted read of the +11.6 is therefore
closer to **+6 to +8**, not +11.6.

**(2) Gunner-healing is Orizon-only within the family.** The probe deliberately
takes "Orizon's harder reading" and heals its front gunners. Measured, per game,
heals landing on own gunners:

| Team | CONTROL median | RECENT median | games with ≥3 |
|---|---|---|---|
| Orizon | 3 | 1.5 | 53% / 50% |
| Team 48 | 0 | 0 | **2% / 8%** |
| Leviathan | 0 | 0 | **2% / 2%** |
| team lazy | 0 | 4 | 38% / 51% |

So the probe is faithful to Orizon and materially harsher than two of the four
teams the class is supposed to cover. Counterbattery results read against the
probe transfer to Orizon and (now) team lazy; against Team 48 and Leviathan the
probe over-states how hard the guns are to kill.

**Nothing in the probe reproduces a pattern wild play no longer produces.** The
one structural over-reach (O14, plant purity) is a *frequency and purity*
difference, not a phantom behaviour — which is a materially better position than
`cad_probe`, whose forward sentinels and early throws are behaviours wild CAD
does not perform at all.

### 2.6 Family fidelity (the "~46% of the field" claim)

The probe's provenance claims one shared script across Orizon / team lazy /
Team 48 / Leviathan. Measured over 315 games, the four are *not* interchangeable
in 2026-08-08 play:

| Predicate | Orizon (40) | Team 48 (90) | Leviathan (75) | team lazy (110) |
|---|---|---|---|---|
| zero sentinels | 100% | **100%** | 85% → 74% | 100% → 88% |
| zero launchers | 100% | 80% / 84% | 100% | 100% |
| zero barriers | 77% / 80% | **100%** | 75% → **40%** | **100%** |
| in-range frac (median) | 0.46 / 0.62 | **1.00 / 1.00** | 0.94 → **0.61** | 1.00 → 0.78 |
| core-shot frac (median) | 0.69 / 0.75 | **0.96 / 0.94** | 0.88 → 0.62 | 0.85 → 0.74 |
| ≥3 gunner heals | 53% / 50% | 2% / 8% | 2% / 2% | 38% → 51% |
| gunners built (median) | 10 / 11.5 | 4 / 4 | 11.5 / 12 | 4 / 7 |

Notable: **Team 48 v16 is a purer instance of the probe's plant discipline than
Orizon is** (in-range frac 1.00 in 87/87 games, core-shot frac 0.94-0.96) while
being a much softer instance of its defence (no gunner heals). Leviathan has
drifted — barriers appeared (zero-barrier games 75%→40%) and its plant discipline
degraded (in-range frac 0.94→0.61). The class label still covers all four on
"gunner-only point-blank battery"; it does not cover them on defence or on
volume.


---

## 3. `flotte_probe`

### 3.1 Signature derived from the probe source

| # | Predicate (testable) | Threshold | Source in the probe |
|---|---|---|---|
| F1 | 4 builders spawned r0-r3; only saboteur replacements after | `n_bots == 4` at r0-r3 | `OPENING_BUILDERS = 4`, `MAX_BUILDERS = 6` |
| F2 | **Exactly 3** harvesters, never expanded | `n_harvester == 3`, no build after ~r10 | `ECO_HARVESTERS = 3`, hard-capped in `_eco_seek_ore` |
| F3 | Shortest possible conveyor runs | `n_conveyor` small | `MAX_CHAIN = 24`, chain laid straight back to Core |
| F4 | **1-2 forward gunners**, planted in **r12-19**, at lane fractions **0.18** and **0.60**; never replaced | `n_gunner ≤ 2` total; first plant r12-19; lane frac ≈0.18/0.60 | `GUNNER_TARGET = 2`, `GUNNER_WINDOW_START = 12`, `GUNNER_FRACTIONS = (0.18, 0.60)` |
| F5 | No launchers, no barriers | `n_launcher == 0` | no `build_launcher` / `build_barrier` call exists |
| F6 | Builder #4 crosses into enemy territory ~r15-20 and never comes home | `≥1 crosser`, cross ≈ r15-20, never returns | `SABOTEUR_ROLE = 3`, `_cross_or_loiter`, "never retreat, never return home" |
| F7 | Saboteur kills harvesters with melee and loiters on the wreckage | `harvester attacks ≥5`, `harvester kills ≥1`, deep rounds large | `_attack_adjacent` with harvester priority, `_loiter` |
| F8 | **2 sentinels** deep in enemy territory, from two angles, after 15 harvester-quiet rounds | `n_sentinel == 2`, `fp_dsq ≤ 32`, lane frac high | `SENTINEL_TARGET = 2`, `HARV_QUIET_ROUNDS = 15`, `LATERAL_OFFSET = 3` |
| F9 | Steady ammo trickle from r0 | convert rate > 0 from r0 | `_bank_ammo`, `AMMO_CHUNK = 6` |

### 3.2 Wild corpus

| Cohort | Matches | Games | Version | Opponents |
|---|---|---|---|---|
| RECENT | `0f4d9826`, `b9074b42`, `8232e2f0`, `67ce4204`, `a7534d35`, `ae42843f`, `0ed69121`, `883acaab`, `8e85d256`, `aea2e5e8`, `47def9cd` (2026-08-08) | 55 (**53 distinct**, 2 exact repeats) | **v38** | Lorem Ipsum ×15, not adgato ×10, Clankers, PbSF, OpenSverige ×10, Jython, Pivot |
| CONTROL | `73afd924`, `d7b66129` (v35); `780059e5`, `8a625993`, `f68a7d14`, `e5796b91`, `449dab71`, `79b4066c`, `24286407` (v36) (2026-08-07) | 45 | **v35 / v36** | sporks, HTTP 418, kladde, PbSF, team lazy ×10, O(1) ×20 |

**Wild Flotte is now v44 (per the builder arm's fleet audit); the archive tops
out at v38.** So even the RECENT cohort is 6 versions behind live wild. The
extraction version is older still and unrecoverable — `0a88ca71` is not in the
archive, and it was played against our **v7**, which places it many days and
many Flotte versions before v35.

### 3.3 Predicate results

| # | Predicate | CONTROL (45 games, v35/36) | RECENT (55 games, v38) | Read |
|---|---|---|---|---|
| F1 | `n_bots == 4` at r0-r3 | 30/45 (67%) | 46/55 (84%) | **HOLDS**, tightened |
| F2 | `n_harvester == 3` | 21/45 (47%); ≤4 in 43/45 (96%) | 38/55 (69%); ≤4 in 54/55 (98%) | **HOLDS** — extra harvesters are late rebuilds (r>50), not expansion |
| F3 | short conveyor runs | median 9 (1-21) | median 13 (8-39) | HOLDS (probe cap 24) |
| F4a | `n_gunner ≤ 2` total | **0/45 (0%)**, median **13** | **1/55 (2%)**, median **15** | **DEAD in both cohorts** |
| F4b | first gunner in r12-19 | 7/45 (16%) | 20/55 (36%) | **DEAD** (median first plant r21 / r20) |
| F4c | first-two lane frac ≈ 0.18 / 0.60 | median **0.66** | median **0.51** | **DEAD** — no screener at 18% exists |
| F4d | concurrent gunners alive | median alive 2, max median 4 | median alive 2, max median 3 | The "1-2 forward gunners" reads true **only as a concurrency statement** — wild keeps ~2 up and *continuously rebuilds*; the probe plants 2 and stops forever |
| F5 | no launchers | **7/45 (16%)** — 38/45 build ≥1 | **1/55 (2%)** — 54/55 build ≥1, median **2**, built r3-22 (median **r10**) | **DEAD in both cohorts** |
| F6 | ≥1 crosser that never returns | 44/45 (98%), earliest cross median **r27** | 50/55 (91%), earliest cross median **r27** | **HOLDS** (probe says r15-20; wild ~r27 on the lane-frac-0.70 test) |
| F7 | harvester attacks ≥5 | 20/45 (44%) | **44/55 (80%)** | **HOLDS**, materially strengthened |
| F7 | harvester kills ≥1 | 19/45 (42%) | **39/55 (71%)** | **HOLDS**, strengthened |
| F8a | `n_sentinel == 2` | 15/45 (33%) ≥2; 27/45 (60%) ≥1 | 13/55 (24%) ≥2; 45/55 (82%) ≥1 | **PARTIAL** — one sentinel is typical, not two |
| F8b | sentinel deep and in Core range | **49/49 plants at `fp_dsq ≤ 32`**, lane frac median **0.79** | **61/61 plants at `fp_dsq ≤ 32`**, lane frac median **0.75** | **HOLDS exactly** |
| F8c | trigger is harvester-quiet | plant round median **121**, range 109-787 | plant round median **124**, range 92-640 | **SUSPECT** — the tight r109-124 clustering across 20 different opponents reads as a round-number trigger, not a state trigger |
| F9 | ammo trickle | convert rate median 0.37 | median 0.38 | HOLDS |

### 3.4 Drift between cohorts (turret geometry)

On top of the never-valid predicates, wild Flotte's turret program moved
*between* the cohorts, away from the Core and toward lane screening:

| Metric | CONTROL (v35/36) | RECENT (v38) |
|---|---|---|
| first plant `fp_dsq ≤ 13` | 21/45 (47%) | **5/55 (9%)** |
| `min fp_dsq ≤ 4` | 25/45 (56%) | **9/55 (16%)** |
| in-range frac, median | 0.50 | **0.27** |
| max point-blank guns alive, median | 2 | **1** |
| core-shot frac, median | 0.44 | **0.31** |
| ≥3 gunner heals | 15/45 (33%) | 37/55 (67%) |

### 3.5 Verdict — **CLASS-DRIFTED** (with two predicates never valid)

Precisely which predicates died and what replaced them:

* **F4 (1-2 forward gunners at 18%/60%, planted once) — dead, and dead at
  extraction.** Replaced by a **continuous gunner rebuild program**: 13-15
  gunners built per game, ~2 alive at any time, first plant around r20-21, at
  ~0.5-0.66 of the lane. The probe's version of this is a one-shot: two gunners,
  then never again for the rest of the match. Against a defence that kills
  turrets, the probe's screen evaporates and wild Flotte's does not.
* **F5 (no launchers) — dead, and dead at extraction.** Wild Flotte builds
  ~2 launchers at around r10 in 98% of recent games (84% in control). Launchers
  throw builder bots — including *our* builders — which is a whole interaction
  channel the probe cannot present at all.
* **F8a (two sentinels) — partially dead.** One is typical. The geometry (deep,
  lane frac 0.75-0.79, always within sentinel range of the Core) is exactly
  right, so this is a count error, not a shape error.
* **Drifted since extraction (F4/geometry):** the point-blank component of the
  gunner program roughly halved from v35/36 to v38 (in-range frac 0.50→0.27).
* **Held and strengthened:** the economy discipline (F1-F3) and the saboteur
  payload (F6-F7). Harvester-hunting nearly doubled in prevalence from control
  to recent. Whatever else changed, the strangulation payload is real, current,
  and the thing worth instrumenting.

**Confidence: high.** 100 games / 20 matches / 3 versions, both cohorts, with a
validated parser; the two dead predicates fail by margins that cannot be noise
(0/45 and 1/55 for `n_gunner ≤ 2`; 84% and 98% launcher presence against a probe
that has none).

**What would change the answer:** only new evidence about **v44**, which the
archive does not contain. If v44 dropped launchers and reverted to a 2-gunner
screen, the probe would be closer to valid than this read says — but nothing in
the v35→v36→v38 trajectory points that way (launcher usage went *up*, 84%→98%).
A single archived v44 series would settle it.


---

## 4. Disposition

### `orizon_probe` — **usable as a field instrument**, with two disclosed qualifications

No re-freeze needed. It is, as of tonight, the *only* instrument we own whose
subject has not shipped a new version since extraction (Orizon: v34 at
extraction, v34 in its two most recent archived matches).

Conditions of use, to be quoted alongside any orizon leg:

1. **Purity qualification.** The probe presents the point-blank pattern at
   100% plant purity; wild Orizon runs 0.46-0.62. Report probe margins as
   *pattern-conditional*, and if a field-weighted number is wanted, discount by
   the wild firing rate (≈0.5-0.6). For the standing `+11.6`: field-weighted,
   read it as roughly **+6 to +8**.
2. **Family qualification.** Gunner-healing is Orizon-and-team-lazy behaviour;
   Team 48 and Leviathan do not do it (2-8% of games). A counterbattery claim
   validated on the probe is *conservative* for those two, not invalid — but the
   "~46% of the field" framing overstates how uniform the block is, and the
   in-range/heal split in §2.6 should replace it.

Optional strengthening (not required): a **second** orizon instrument frozen on
Team 48 v16 — which is a purer plant-discipline instance (in-range frac 1.00 in
87/87 games) with no gunner heals — would separate "can we kill the guns" from
"can we out-heal the healer", which the current single probe conflates.

### `flotte_probe` — **attribution-only; re-freeze required before any field claim**

Tonight's leg (91.7 vs 86.7, overlapping) stands as attribution-only with a
fidelity caveat, correctly. Do not promote it.

The re-freeze must add or fix, in priority order:

1. **Launchers** — ~2 built around r10, in 98% of recent games. Currently absent
   from the probe entirely. This is the single largest missing interaction.
2. **Continuous gunner rebuild** — replace `GUNNER_TARGET = 2` (lifetime) with a
   *standing* target of ~2 alive and rebuild-on-death, ~13-15 built over a
   ~200-round game; first plant ~r20; lane fraction ~0.5, not 0.18/0.60.
3. **One sentinel, not two** — keep the geometry (deep, lane frac ~0.75, always
   `fp_dsq ≤ 32`); reduce the count; consider a round-clocked trigger near r120
   rather than the harvester-quiet state trigger, which the data does not
   support.
4. **Keep untouched:** the economy (4 builders r0-r3, exactly 3 harvesters,
   short chains) and the saboteur payload (crosses ~r27 by the lane-frac test,
   never returns, hunts harvesters, loiters) — both validated and stronger in
   v38 than at extraction.

**Extraction source for the re-freeze.** In preference order, all in-archive:

* `47def9cd` (v38 vs not adgato v19, 5 games, ladder, 2026-08-08T10:14) —
  most recent Flotte series in the archive.
* `8e85d256` + `0ed69121` (v38 vs Lorem Ipsum v25, 10 games; note g1/g3 of one
  duplicate g5/g2 of the other — 8 distinct games).
* `a7534d35` (v38 vs Jython v93) and `ae42843f` (v38 vs Pivot v73) for map
  spread.
* Deliberately **not** `883acaab` / `aea2e5e8` (v38 vs OpenSverige) as the
  primary source: freezing off games against ourselves bakes our own behaviour
  into the instrument, which is exactly the failure mode the cad case exposed.

**Caveat on the re-freeze itself:** v38 is 6 versions behind live wild v44. A
re-freeze off v38 is an improvement but not a validation. If any Flotte field
claim is to be load-bearing, a v44 series should be downloaded first (1 match =
5 games is enough for the turret/launcher layer).

---

## 5. Self-checks

**5.1 Parser end-to-end validation.** `core_deliv × 10 == titaniumCollected`
checked per team-side per game across the whole corpus used here:
**809/810 team-sides exact** (405 games, both sides). The single exception is
`40e85246` game 1 side A (`sporks` v2, not a subject team): parsed 113 stacks
= 1130 Ti vs reported 1120. Diagnosed, not waved: the last delivery onto that
Core's footprint lands in round 103, which is the round that Core was destroyed
(`winCondition = core_destroyed`, winner B) — an uncredited final stack. Last
delivery round and last `updatePlayers` round are both 103. No subject-team side
mismatched.

**5.2 The TEAM_A trap.** Entity team is parsed with default `0`, never `None`
(proto3 omits `TEAM_A = 0` from the wire). Cross-checked: every game resolves
exactly two Cores to two distinct teams; per-side entity counts attribute to the
meta's `teamAName`/`teamBName` consistently across all 81 matches; and the
delivery check in 5.1 is itself team-partitioned, so a team-attribution error
would have shown up as a systematic delivery mismatch rather than a single one.

**5.3 No `BotOutput` dependency.** Every metric in this document is derived from
`placeEntity`, `moveBuilderBot`, `removeEntity`, `fireTurret`, `builderAttack`,
`builderHeal`, `coreConvertAmmo`, `distributeResources` and `updatePlayers`.
No metric reads stdout, indicator lines, or indicator dots. This was a stated
trap (an instrument that reads our own debug prints works only on instrumented
dev builds) and it is avoided by construction, not by inspection.

**5.4 FireTurret ordering trap (`replay_schema.md` §S1).** Fire events can be
emitted after the victim's `removeEntity` in the same round, so target
resolution by live tile occupancy manufactures false attributions. Not exposed
here: `core-shot frac` resolves a shot's target against the **static Core
footprint from `map.cores`**, which never moves and is never removed mid-game.
Shooter attribution uses a building-tile index; turrets are immovable and are
only removed when destroyed, so a shot emitted from a tile whose turret died the
same round resolves to no team and is simply not counted (conservative, and it
affects at most the final round of a turret's life).

**5.5 Control-cohort reproduction.** The control cohort is the method check.
For Orizon it reproduces the extracted signature at the extraction version
(v34): O2/O3 at 100%, O7 at 63%, O8 at 87%, O13 at 97% — i.e. the harness
recovers the same class the 2026-08-07 decode described from a different
toolchain (`replay_lib.py` then, this harness now), including the family
plant-distance shapes. For Flotte it reproduces the payload predicates
(F1/F2/F6/F7) and shows F4/F5 failing *identically* in both cohorts — which is
what licenses the "extraction defect, not drift" call rather than a drift call.

**5.6 Cohort independence.** Bots in this game are deterministic and map
identity is fully determined by the map, so repeated (map, versions) pairings
produce identical games. Detected and reported: **2 exact-repeat game pairs in
the Flotte RECENT cohort** (both vs Lorem Ipsum v25), so 55 games = 53 distinct.
No repeats in the other three cohorts.

**5.7 Method for each claim.**

| Claim | Method |
|---|---|
| build counts by type | `placeEntity` events, counted per team per kind over the whole match (so rebuilds count; "alive" counts are stated separately) |
| plant `fp_dsq` / creep | plant position vs the *enemy* Core footprint from `map.cores` |
| in-range / core-shot fractions | plants at `fp_dsq ≤ 13` over all plants; `fireTurret.to` ∈ enemy Core footprint over all shots |
| concurrent battery size | full entity set rebuilt each round; gunners alive per team at `fp_dsq ≤ 13` and `≤ 4` |
| crossers / saboteur | per-builder position tracks from `placeEntity` + `moveBuilderBot`; lane fraction `d_home/(d_home+d_enemy)`; crossing at ≥0.70, return at ≤0.35 |
| harvester attacks / kills | `builderAttack` resolved against the building-tile index at event time; a kill = the attacked harvester's `removeEntity` within 1 round of an attack by that team |
| heals by target type | `builderHeal` resolved against the building-tile index |
| convert rate / titanium band | `coreConvertAmmo` per team; titanium series from `updatePlayers` |
| version / date / rated | `*.meta.json` (`teamAVersion`, `teamBVersion`, `completedAt`, `triggeredBy`) |

**5.8 Known limits.**

* **Rotation is unmeasurable** in this format (no direction-update message), so
  the probes' "never rotates" (orizon) / "rotates to reacquire" (flotte) claims
  are untested. Excluded from both verdicts.
* Orizon's RECENT cohort is 10 games from 2 matches against 2 opponents we have
  never played; the geometry it shows is partly a response to their defences.
* Flotte's RECENT cohort is v38, 6 versions behind live wild v44.
* None of the extraction-source matches are on disk, so "reproduces the
  extraction" is established by version identity (Orizon) or by proxy (Flotte),
  never by re-running the original decode.

---

## 6. Per-game measurements

### ORIZON v34 — RECENT cohort (2026-08-08, 2 matches, 10 games)

| match g | date | opp | R | bots | harv | gun built | in-range frac | 1st plant (r, fp_dsq) | min fp_dsq | pb max | gun alive max | cvt rate | shots | on core | core-shot frac | gun heals | S/L/B | result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `c99aa374` g1 | 08-08 | Viktor5776 v3 | 94 | 4 | 2 | 7 | 0.71 | r28, 9 | 1 | 5 | 6 | 0.255 | 101 | 87 | 0.86 | 0 | 0/0/0 | W |
| `c99aa374` g2 | 08-08 | Viktor5776 v3 | 136 | 4 | 3 | 10 | 0.9 | r21, 9 | 1 | 4 | 5 | 0.676 | 210 | 159 | 0.76 | 5 | 0/0/0 | W |
| `c99aa374` g3 | 08-08 | Viktor5776 v3 | 1000 | 5 | 0 | 13 | 0.31 | r2, 9 | 5 | 3 | 6 | 0.264 | 527 | 393 | 0.75 | 3 | 0/0/0 | L |
| `c99aa374` g4 | 08-08 | Viktor5776 v3 | 100 | 4 | 2 | 8 | 1.0 | r30, 9 | 1 | 7 | 7 | 0.46 | 103 | 78 | 0.76 | 0 | 0/0/2 | W |
| `c99aa374` g5 | 08-08 | Viktor5776 v3 | 1000 | 4 | 3 | 5 | 1.0 | r34, 9 | 1 | 3 | 3 | 0.253 | 611 | 59 | 0.10 | 0 | 0/0/0 | L |
| `ecde38a8` g1 | 08-08 | Kleos v56 | 482 | 7 | 6 | 15 | 0.53 | r7, 17 | 1 | 2 | 4 | 0.448 | 384 | 348 | 0.91 | 0 | 0/0/0 | W |
| `ecde38a8` g2 | 08-08 | Kleos v56 | 394 | 4 | 1 | 15 | 0.27 | r3, 9 | 9 | 2 | 5 | 0.264 | 188 | 51 | 0.27 | 3 | 0/0/0 | L |
| `ecde38a8` g3 | 08-08 | Kleos v56 | 556 | 8 | 5 | 44 | 0.34 | r17, 16 | 1 | 5 | 7 | 0.369 | 427 | 298 | 0.70 | 11 | 0/0/0 | L |
| `ecde38a8` g4 | 08-08 | Kleos v56 | 155 | 4 | 3 | 9 | 1.0 | r27, 9 | 1 | 8 | 8 | 0.606 | 267 | 232 | 0.87 | 0 | 0/0/2 | W |
| `ecde38a8` g5 | 08-08 | Kleos v56 | 1000 | 12 | 7 | 43 | 0.19 | r34, 5 | 1 | 4 | 6 | 0.179 | 272 | 41 | 0.15 | 14 | 0/0/0 | L |

### ORIZON v34 — CONTROL cohort (2026-08-07, 6 matches, 30 games)

| match g | date | opp | R | bots | harv | gun built | in-range frac | 1st plant (r, fp_dsq) | min fp_dsq | pb max | gun alive max | cvt rate | shots | on core | core-shot frac | gun heals | S/L/B | result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `047ea519` g1 | 08-07 | OpenSverige v64 | 1000 | 28 | 4 | 47 | 0.43 | r9, 9 | 1 | 3 | 8 | 0.687 | 930 | 681 | 0.73 | 25 | 0/0/0 | L |
| `047ea519` g2 | 08-07 | OpenSverige v64 | 550 | 4 | 0 | 16 | 0.81 | r1, 5 | 1 | 5 | 5 | 0.305 | 294 | 260 | 0.88 | 9 | 0/0/0 | W |
| `047ea519` g3 | 08-07 | OpenSverige v64 | 493 | 4 | 0 | 18 | 0.89 | r4, 9 | 1 | 4 | 6 | 0.485 | 459 | 281 | 0.61 | 1 | 0/0/0 | W |
| `047ea519` g4 | 08-07 | OpenSverige v64 | 95 | 4 | 2 | 7 | 0.43 | r19, 288 | 5 | 2 | 4 | 0.705 | 150 | 120 | 0.80 | 9 | 0/0/0 | W |
| `047ea519` g5 | 08-07 | OpenSverige v64 | 1000 | 8 | 1 | 17 | 0.06 | r3, 9 | 9 | 1 | 5 | 0.314 | 441 | 10 | 0.02 | 7 | 0/0/0 | L |
| `123ca2f6` g1 | 08-07 | OpenSverige v65 | 1000 | 8 | 3 | 39 | 0.26 | r7, 9 | 4 | 4 | 4 | 0.254 | 319 | 21 | 0.07 | 13 | 0/0/0 | L |
| `123ca2f6` g2 | 08-07 | OpenSverige v65 | 307 | 4 | 2 | 9 | 0.56 | r19, 9 | 1 | 3 | 5 | 0.554 | 275 | 223 | 0.81 | 2 | 0/0/5 | W |
| `123ca2f6` g3 | 08-07 | OpenSverige v65 | 241 | 4 | 2 | 8 | 0.25 | r15, 136 | 9 | 2 | 5 | 0.672 | 294 | 247 | 0.84 | 0 | 0/0/0 | W |
| `123ca2f6` g4 | 08-07 | OpenSverige v65 | 119 | 4 | 2 | 10 | 0.3 | r26, 369 | 1 | 2 | 6 | 0.37 | 100 | 74 | 0.74 | 0 | 0/0/0 | W |
| `123ca2f6` g5 | 08-07 | OpenSverige v65 | 1000 | 7 | 0 | 22 | 0.18 | r2, 9 | 1 | 2 | 5 | 0.61 | 802 | 43 | 0.05 | 10 | 0/0/0 | L |
| `646e8a3a` g1 | 08-07 | OpenSverige v65 | 119 | 4 | 2 | 9 | 0.89 | r19, 16 | 1 | 5 | 6 | 0.555 | 112 | 65 | 0.58 | 8 | 0/0/4 | L |
| `646e8a3a` g2 | 08-07 | OpenSverige v65 | 261 | 9 | 5 | 30 | 0.77 | r12, 9 | 1 | 7 | 9 | 0.448 | 248 | 165 | 0.67 | 3 | 0/0/0 | W |
| `646e8a3a` g3 | 08-07 | OpenSverige v65 | 1000 | 6 | 0 | 25 | 0.08 | r3, 9 | 9 | 1 | 5 | 0.605 | 667 | 25 | 0.04 | 3 | 0/0/0 | L |
| `646e8a3a` g4 | 08-07 | OpenSverige v65 | 107 | 4 | 3 | 10 | 1.0 | r7, 9 | 1 | 4 | 4 | 0.654 | 158 | 139 | 0.88 | 4 | 0/0/0 | W |
| `646e8a3a` g5 | 08-07 | OpenSverige v65 | 106 | 4 | 3 | 6 | 0.5 | r22, 9 | 9 | 3 | 5 | 0.321 | 52 | 40 | 0.77 | 0 | 0/0/3 | L |
| `8a5ea626` g1 | 08-07 | Memtrace v28 | 102 | 4 | 1 | 9 | 0.22 | r22, 514 | 5 | 2 | 6 | 0.402 | 96 | 72 | 0.75 | 0 | 0/0/0 | W |
| `8a5ea626` g2 | 08-07 | Memtrace v28 | 1000 | 4 | 2 | 9 | 0.56 | r13, 340 | 1 | 2 | 6 | 0.489 | 968 | 913 | 0.94 | 0 | 0/0/0 | L |
| `8a5ea626` g3 | 08-07 | Memtrace v28 | 97 | 4 | 1 | 6 | 0.33 | r16, 242 | 9 | 2 | 5 | 0.454 | 117 | 79 | 0.68 | 0 | 0/0/0 | W |
| `8a5ea626` g4 | 08-07 | Memtrace v28 | 101 | 4 | 0 | 6 | 0.5 | r4, 9 | 9 | 2 | 5 | 0.297 | 74 | 23 | 0.31 | 0 | 0/0/0 | L |
| `8a5ea626` g5 | 08-07 | Memtrace v28 | 1000 | 4 | 0 | 7 | 0.0 | r16, 288 | 288 | 0 | 5 | 0.007 | 10 | 0 | 0.00 | 0 | 0/0/0 | L |
| `9f457fb1` g1 | 08-07 | OpenSverige v68 | 294 | 4 | 2 | 15 | 0.67 | r3, 9 | 1 | 5 | 8 | 0.724 | 446 | 322 | 0.72 | 1 | 0/0/1 | W |
| `9f457fb1` g2 | 08-07 | OpenSverige v68 | 1000 | 22 | 6 | 54 | 0.39 | r15, 185 | 2 | 10 | 14 | 0.338 | 458 | 194 | 0.42 | 95 | 0/0/7 | L |
| `9f457fb1` g3 | 08-07 | OpenSverige v68 | 77 | 4 | 2 | 6 | 0.67 | r17, 9 | 5 | 4 | 6 | 0.429 | 96 | 74 | 0.77 | 0 | 0/0/0 | L |
| `9f457fb1` g4 | 08-07 | OpenSverige v68 | 1000 | 5 | 0 | 15 | 0.13 | r2, 25 | 4 | 1 | 5 | 0.292 | 440 | 2 | 0.00 | 4 | 0/0/0 | L |
| `9f457fb1` g5 | 08-07 | OpenSverige v68 | 569 | 17 | 9 | 34 | 0.38 | r7, 9 | 1 | 4 | 9 | 0.402 | 411 | 227 | 0.55 | 75 | 0/0/1 | W |
| `50ca5e87` g1 | 08-07 | OpenSverige v69 | 174 | 5 | 0 | 10 | 0.8 | r2, 9 | 1 | 6 | 6 | 0.224 | 73 | 51 | 0.70 | 0 | 0/0/0 | L |
| `50ca5e87` g2 | 08-07 | OpenSverige v69 | 322 | 8 | 11 | 29 | 0.9 | r7, 9 | 1 | 10 | 11 | 0.599 | 380 | 246 | 0.65 | 11 | 0/0/0 | W |
| `50ca5e87` g3 | 08-07 | OpenSverige v69 | 81 | 4 | 2 | 7 | 1.0 | r7, 9 | 1 | 2 | 2 | 0.716 | 95 | 70 | 0.74 | 9 | 0/0/0 | L |
| `50ca5e87` g4 | 08-07 | OpenSverige v69 | 1000 | 11 | 9 | 27 | 0.33 | r7, 9 | 1 | 3 | 5 | 0.205 | 285 | 45 | 0.16 | 5 | 0/0/12 | L |
| `50ca5e87` g5 | 08-07 | OpenSverige v69 | 201 | 5 | 3 | 3 | 1.0 | r21, 9 | 5 | 3 | 3 | 0.433 | 225 | 219 | 0.97 | 2 | 0/0/0 | L |

### FLOTTE v38 — RECENT cohort (2026-08-08, 11 matches, 55 games)

| match g | date | opp | R | bots (spawn r) | harv (rounds) | conv | gun built | gun alive max | 1st gun r | 1st-2 lane frac | in-range frac | sent (rounds, fp_dsq) | laun | core-shot frac | harv atk | harv kills | crossers (stay) | deep r | result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `0f4d9826` g1 | 08-08 | Clankers v2 | 211 | 4 (0,1,2,3) | 3 (4,12,23) | 21 | 18 | 4 | 48 | [0.9, 0.9] | 0.61 | 1 (r115/25) | 2 | 0.33 | 0 | 0 | 2 (2) | 86 | W |
| `0f4d9826` g2 | 08-08 | Clankers v2 | 290 | 4 (0,1,2,3) | 3 (4,7,14) | 10 | 51 | 4 | 30 | [0.99, 0.76] | 0.98 | 1 (r152/32) | 2 | 0.28 | 39 | 1 | 1 (1) | 20 | W |
| `0f4d9826` g3 | 08-08 | Clankers v2 | 949 | 5 (0,1,2,3,24) | 1 (10) | 8 | 2 | 2 | 5 | [0.5, 0.75] | 0.5 | 0 () | 1 | 0.00 | 10 | 0 | 1 (1) | 34 | L |
| `0f4d9826` g4 | 08-08 | Clankers v2 | 238 | 4 (0,1,2,3) | 3 (4,6,17) | 15 | 13 | 3 | 27 | [0.79, 0.79] | 0.15 | 1 (r104/25) | 2 | 0.49 | 18 | 2 | 2 (2) | 22 | W |
| `0f4d9826` g5 | 08-08 | Clankers v2 | 312 | 5 (0,1,2,3,30) | 3 (5,6,6) | 17 | 21 | 3 | 33 | [0.37, 0.45] | 0.9 | 1 (r245/25) | 2 | 0.07 | 0 | 0 | 1 (1) | 76 | W |
| `b9074b42` g1 | 08-08 | Lorem Ipsum v23 | 840 | 4 (0,1,2,3) | 3 (8,136,194) | 15 | 14 | 3 | 14 | [0.5, 0.57] | 0.57 | 1 (r428/25) | 2 | 0.38 | 28 | 2 | 2 (1) | 51 | L |
| `b9074b42` g2 | 08-08 | Lorem Ipsum v23 | 168 | 4 (0,1,2,3) | 3 (3,6,13) | 10 | 11 | 4 | 17 | [0.12, 0.12] | 0.64 | 1 (r92/25) | 2 | 0.24 | 0 | 0 | 1 (1) | 69 | W |
| `b9074b42` g3 | 08-08 | Lorem Ipsum v23 | 181 | 4 (0,1,2,3) | 3 (5,5,6) | 9 | 14 | 3 | 21 | [0.66, 1.22] | 0.07 | 1 (r129/25) | 2 | 0.08 | 30 | 1 | 2 (2) | 32 | L |
| `b9074b42` g4 | 08-08 | Lorem Ipsum v23 | 164 | 4 (0,1,2,3) | 3 (4,4,5) | 9 | 7 | 3 | 23 | [0.45, 1.03] | 0.71 | 2 (r111/25,r124/25) | 2 | 0.28 | 44 | 1 | 1 (1) | 31 | W |
| `b9074b42` g5 | 08-08 | Lorem Ipsum v23 | 300 | 4 (0,1,2,3) | 4 (3,3,15,112) | 16 | 20 | 4 | 23 | [0.29, 0.54] | 0.15 | 0 () | 2 | 0.08 | 31 | 2 | 2 (1) | 44 | L |
| `8232e2f0` g1 | 08-08 | Powered by SmartFridge v40 | 148 | 4 (0,1,2,3) | 3 (6,12,31) | 18 | 10 | 4 | 41 | [0.11, 0.76] | 0.1 | 2 (r110/18,r126/32) | 1 | 0.62 | 10 | 1 | 2 (2) | 36 | W |
| `8232e2f0` g2 | 08-08 | Powered by SmartFridge v40 | 218 | 4 (0,1,2,3) | 2 (7,40) | 21 | 10 | 6 | 12 | [0.53, 0.63] | 0.2 | 1 (r164/25) | 2 | 0.55 | 14 | 1 | 1 (1) | 29 | W |
| `8232e2f0` g3 | 08-08 | Powered by SmartFridge v40 | 168 | 4 (0,1,2,3) | 3 (4,4,5) | 8 | 17 | 6 | 14 | [0.19, 0.45] | 0.06 | 1 (r112/25) | 2 | 0.45 | 46 | 4 | 2 (2) | 19 | W |
| `8232e2f0` g4 | 08-08 | Powered by SmartFridge v40 | 1000 | 10 (0,1,2,3,207) | 3 (4,6,17) | 38 | 228 | 5 | 14 | [0.25, 0.25] | 0.0 | 0 () | 2 | 0.00 | 0 | 0 | 1 (0) | 1 | W |
| `8232e2f0` g5 | 08-08 | Powered by SmartFridge v40 | 753 | 4 (0,1,2,3) | 3 (4,7,14) | 20 | 9 | 2 | 16 | [0.25, 0.2] | 0.44 | 0 () | 2 | 0.94 | 14 | 1 | 1 (1) | 61 | W |
| `67ce4204` g1 | 08-08 | not adgato v19 | 349 | 4 (0,1,2,3) | 3 (7,11,22) | 21 | 23 | 4 | 15 | [0.56, 0.56] | 0.0 | 0 () | 2 | 0.00 | 14 | 1 | 2 (2) | 65 | L |
| `67ce4204` g2 | 08-08 | not adgato v19 | 944 | 4 (0,1,2,3) | 4 (5,6,6,913) | 10 | 23 | 4 | 13 | [0.45, 0.42] | 0.17 | 1 (r176/25) | 1 | 0.83 | 47 | 4 | 2 (2) | 17 | W |
| `67ce4204` g3 | 08-08 | not adgato v19 | 284 | 4 (0,1,2,3) | 3 (4,4,5) | 8 | 46 | 6 | 15 | [0.34, 0.34] | 0.22 | 2 (r111/25,r234/25) | 2 | 0.16 | 45 | 3 | 1 (1) | 34 | L |
| `67ce4204` g4 | 08-08 | not adgato v19 | 1000 | 4 (0,1,2,3) | 2 (7,8) | 12 | 40 | 3 | 5 | [0.4, 0.4] | 1.0 | 1 (r640/25) | 2 | 0.85 | 14 | 1 | 4 (1) | 37 | W |
| `67ce4204` g5 | 08-08 | not adgato v19 | 176 | 4 (0,1,2,3) | 3 (6,12,43) | 11 | 15 | 3 | 14 | [0.46, 0.57] | 0.0 | 0 () | 1 | 0.00 | 18 | 1 | 3 (0) | 28 | L |
| `a7534d35` g1 | 08-08 | Jython v93 | 214 | 4 (0,1,2,3) | 3 (6,6,7) | 18 | 22 | 3 | 14 | [0.59, 0.59] | 0.82 | 2 (r124/25,r194/25) | 2 | 0.49 | 29 | 1 | 4 (2) | 37 | W |
| `a7534d35` g2 | 08-08 | Jython v93 | 167 | 4 (0,1,2,3) | 3 (7,8,18) | 20 | 12 | 2 | 18 | [0.49, 0.49] | 0.0 | 2 (r112/32,r133/25) | 2 | 0.20 | 24 | 1 | 3 (3) | 36 | W |
| `a7534d35` g3 | 08-08 | Jython v93 | 224 | 4 (0,1,2,3) | 3 (4,4,5) | 8 | 31 | 4 | 11 | [0.51, 0.42] | 0.13 | 1 (r166/32) | 2 | 0.23 | 38 | 1 | 3 (1) | 22 | W |
| `a7534d35` g4 | 08-08 | Jython v93 | 231 | 4 (0,1,2,3) | 2 (8,16) | 9 | 17 | 3 | 20 | [0.79, 0.5] | 0.94 | 1 (r128/25) | 1 | 0.29 | 5 | 0 | 3 (0) | 23 | L |
| `a7534d35` g5 | 08-08 | Jython v93 | 155 | 4 (0,1,2,3) | 3 (5,5,7) | 10 | 21 | 4 | 22 | [0.74, 0.65] | 0.1 | 1 (r113/25) | 2 | 0.34 | 11 | 1 | 2 (2) | 49 | W |
| `ae42843f` g1 | 08-08 | Pivot v73 | 149 | 4 (0,1,2,3) | 3 (4,12,23) | 19 | 15 | 3 | 29 | [0.71, 0.67] | 0.87 | 2 (r115/32,r136/25) | 2 | 0.45 | 33 | 1 | 2 (2) | 52 | W |
| `ae42843f` g2 | 08-08 | Pivot v73 | 135 | 5 (0,1,2,3,50) | 3 (4,6,17) | 15 | 4 | 2 | 28 | [0.83, 0.26] | 0.0 | 5 (r97/32,r115/16,r119/9) | 2 | 0.45 | 14 | 1 | 2 (2) | 22 | W |
| `ae42843f` g3 | 08-08 | Pivot v73 | 189 | 4 (0,1,2,3) | 4 (3,3,18,68) | 17 | 19 | 5 | 26 | [0.64, 0.08] | 0.32 | 2 (r111/25,r179/13) | 2 | 0.45 | 0 | 0 | 2 (1) | 66 | W |
| `ae42843f` g4 | 08-08 | Pivot v73 | 144 | 4 (0,1,2,3) | 2 (7,17) | 13 | 4 | 3 | 23 | [0.42, 0.71] | 0.0 | 2 (r114/32,r116/25) | 2 | 0.54 | 20 | 0 | 2 (2) | 25 | W |
| `ae42843f` g5 | 08-08 | Pivot v73 | 208 | 4 (0,1,2,3) | 3 (3,6,13) | 8 | 18 | 6 | 11 | [0.28, 0.91] | 0.44 | 1 (r168/32) | 2 | 0.32 | 62 | 2 | 3 (2) | 29 | W |
| `0ed69121` g1 | 08-08 | Lorem Ipsum v25 | 213 | 4 (0,1,2,3) | 3 (6,12,19) | 19 | 16 | 3 | 55 | [0.86, 0.16] | 0.0 | 1 (r188/25) | 1 | 0.00 | 13 | 0 | 2 (2) | 45 | L |
| `0ed69121` g2 | 08-08 | Lorem Ipsum v25 | 230 | 4 (0,1,2,3) | 4 (5,5,6,133) | 9 | 15 | 3 | 21 | [0.66, 0.66] | 0.0 | 1 (r208/25) | 2 | 0.06 | 34 | 2 | 1 (1) | 34 | L |
| `0ed69121` g3 | 08-08 | Lorem Ipsum v25 | 409 | 4 (0,1,2,3) | 3 (3,6,13) | 11 | 8 | 3 | 21 | [0.25, 1.38] | 0.62 | 0 () | 2 | 0.31 | 34 | 1 | 3 (1) | 31 | L |
| `0ed69121` g4 | 08-08 | Lorem Ipsum v25 | 252 | 4 (0,1,2,3) | 3 (4,12,19) | 17 | 5 | 3 | 35 | [0.82, 0.82] | 0.4 | 0 () | 2 | 0.29 | 14 | 1 | 2 (2) | 65 | W |
| `0ed69121` g5 | 08-08 | Lorem Ipsum v25 | 277 | 4 (0,1,2,3) | 3 (7,8,21) | 20 | 4 | 1 | 13 | [0.45, 0.45] | 0.25 | 1 (r114/25) | 2 | 0.74 | 0 | 0 | 1 (1) | 90 | W |
| `883acaab` g1 | 08-08 | OpenSverige v75 | 195 | 4 (0,1,2,3) | 3 (3,3,15) | 15 | 9 | 4 | 43 | [0.9, 0.9] | 0.67 | 1 (r130/13) | 2 | 0.46 | 14 | 1 | 2 (1) | 45 | W |
| `883acaab` g2 | 08-08 | OpenSverige v75 | 146 | 4 (0,1,2,3) | 3 (4,12,19) | 18 | 9 | 4 | 33 | [0.2, 0.82] | 0.78 | 2 (r113/25,r137/32) | 2 | 0.56 | 0 | 0 | 2 (2) | 85 | W |
| `883acaab` g3 | 08-08 | OpenSverige v75 | 821 | 4 (0,1,2,3) | 4 (4,5,6,121) | 10 | 35 | 3 | 12 | [0.44, 0.44] | 0.57 | 2 (r156/25,r272/25) | 2 | 0.39 | 55 | 1 | 1 (0) | 15 | W |
| `883acaab` g4 | 08-08 | OpenSverige v75 | 329 | 5 (0,1,2,3,38) | 3 (4,4,5) | 8 | 25 | 5 | 11 | [0.51, 0.51] | 0.28 | 1 (r115/25) | 2 | 0.54 | 35 | 2 | 3 (2) | 36 | W |
| `883acaab` g5 | 08-08 | OpenSverige v75 | 172 | 4 (0,1,2,3) | 2 (8,49) | 8 | 10 | 3 | 7 | [0.35, 0.6] | 0.6 | 1 (r115/25) | 2 | 0.35 | 20 | 1 | 4 (2) | 43 | W |
| `8e85d256` g1 | 08-08 | Lorem Ipsum v25 | 285 | 4 (0,1,2,3) | 3 (6,6,7) | 23 | 16 | 3 | 22 | [0.91, 0.77] | 0.38 | 0 () | 2 | 0.19 | 19 | 1 | 4 (1) | 21 | L |
| `8e85d256` g2 | 08-08 | Lorem Ipsum v25 | 409 | 4 (0,1,2,3) | 3 (3,6,13) | 11 | 8 | 3 | 21 | [0.25, 1.38] | 0.62 | 0 () | 2 | 0.31 | 34 | 1 | 3 (1) | 31 | L |
| `8e85d256` g3 | 08-08 | Lorem Ipsum v25 | 184 | 4 (0,1,2,3) | 3 (4,4,5) | 9 | 11 | 3 | 16 | [0.19, 0.45] | 0.27 | 1 (r114/25) | 2 | 0.24 | 42 | 3 | 1 (1) | 49 | W |
| `8e85d256` g4 | 08-08 | Lorem Ipsum v25 | 459 | 4 (0,1,2,3) | 2 (8,56) | 13 | 11 | 3 | 14 | [0.5, 0.5] | 0.36 | 1 (r328/25) | 2 | 0.16 | 24 | 1 | 2 (1) | 27 | L |
| `8e85d256` g5 | 08-08 | Lorem Ipsum v25 | 213 | 4 (0,1,2,3) | 3 (6,12,19) | 19 | 16 | 3 | 55 | [0.86, 0.16] | 0.0 | 1 (r188/25) | 1 | 0.00 | 13 | 0 | 2 (2) | 45 | L |
| `aea2e5e8` g1 | 08-08 | OpenSverige v76 | 130 | 6 (0,1,2,3,43) | 3 (3,6,17) | 10 | 8 | 4 | 22 | [0.28, 0.56] | 0.12 | 1 (r92/32) | 2 | 0.63 | 0 | 0 | 4 (2) | 9 | W |
| `aea2e5e8` g2 | 08-08 | OpenSverige v76 | 159 | 4 (0,1,2,3) | 3 (4,12,23) | 18 | 16 | 5 | 29 | [0.71, 0.64] | 0.75 | 2 (r115/25,r133/25) | 2 | 0.57 | 25 | 2 | 2 (2) | 89 | W |
| `aea2e5e8` g3 | 08-08 | OpenSverige v76 | 170 | 4 (0,1,2,3) | 3 (4,4,5) | 8 | 17 | 4 | 16 | [0.51, 0.51] | 0.18 | 1 (r116/25) | 2 | 0.26 | 29 | 1 | 2 (2) | 32 | W |
| `aea2e5e8` g4 | 08-08 | OpenSverige v76 | 321 | 4 (0,1,2,3) | 2 (7,11) | 20 | 11 | 3 | 30 | [0.51, 0.17] | 0.0 | 1 (r112/25) | 0 | 0.41 | 0 | 0 | 2 (0) | 25 | W |
| `aea2e5e8` g5 | 08-08 | OpenSverige v76 | 365 | 5 (0,1,2,3,64) | 1 (8) | 8 | 15 | 5 | 8 | [0.56, 0.4] | 0.73 | 1 (r109/25) | 1 | 0.66 | 0 | 0 | 2 (1) | 61 | W |
| `47def9cd` g1 | 08-08 | not adgato v19 | 196 | 4 (0,1,2,3) | 5 (4,5,6,52,76) | 8 | 9 | 4 | 17 | [0.32, 0.4] | 0.0 | 1 (r140/25) | 2 | 0.27 | 19 | 1 | 2 (2) | 32 | W |
| `47def9cd` g2 | 08-08 | not adgato v19 | 410 | 4 (0,1,2,3) | 3 (4,4,5) | 8 | 51 | 7 | 14 | [0.34, 0.3] | 0.29 | 2 (r112/25,r354/25) | 2 | 0.27 | 29 | 2 | 2 (2) | 57 | L |
| `47def9cd` g3 | 08-08 | not adgato v19 | 176 | 4 (0,1,2,3) | 4 (6,12,19,67) | 18 | 10 | 4 | 53 | [0.83, 0.15] | 0.0 | 1 (r112/32) | 1 | 0.23 | 34 | 1 | 1 (1) | 55 | L |
| `47def9cd` g4 | 08-08 | not adgato v19 | 571 | 8 (0,1,2,3,145) | 4 (4,6,29,89) | 39 | 22 | 4 | 35 | [0.77, 0.61] | 0.05 | 1 (r218/25) | 2 | 0.08 | 0 | 0 | 6 (6) | 45 | L |
| `47def9cd` g5 | 08-08 | not adgato v19 | 591 | 6 (0,1,2,3,76) | 3 (7,8,18) | 21 | 27 | 4 | 17 | [0.49, 0.49] | 0.11 | 1 (r132/32) | 2 | 0.77 | 20 | 1 | 1 (1) | 61 | L |

### FLOTTE v35/v36 — CONTROL cohort (2026-08-07, 9 matches, 45 games)

| match g | date | opp | R | bots (spawn r) | harv (rounds) | conv | gun built | gun alive max | 1st gun r | 1st-2 lane frac | in-range frac | sent (rounds, fp_dsq) | laun | core-shot frac | harv atk | harv kills | crossers (stay) | deep r | result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `73afd924` g1 | 08-07 | sporks v2 | 770 | 4 (0,1,2,3) | 4 (4,4,5,678) | 10 | 96 | 4 | 11 | [0.51, 0.5] | 0.44 | 2 (r300/25,r746/25) | 2 | 0.02 | 34 | 3 | 2 (2) | 46 | L |
| `73afd924` g2 | 08-07 | sporks v2 | 218 | 4 (0,1,2,3) | 1 (6) | 2 | 4 | 3 | 5 | [0.5, 0.64] | 1.0 | 0 () | 0 | 1.00 | 0 | 0 | 2 (0) | 5 | L |
| `73afd924` g3 | 08-07 | sporks v2 | 190 | 4 (0,1,2,3) | 3 (3,3,15) | 16 | 13 | 4 | 29 | [0.24, 0.63] | 0.15 | 1 (r129/25) | 2 | 0.44 | 29 | 1 | 2 (2) | 73 | W |
| `73afd924` g4 | 08-07 | sporks v2 | 156 | 4 (0,1,2,3) | 3 (6,12,19) | 17 | 18 | 4 | 52 | [0.81, 0.93] | 0.5 | 1 (r114/25) | 1 | 0.57 | 41 | 0 | 1 (1) | 43 | W |
| `73afd924` g5 | 08-07 | sporks v2 | 152 | 4 (0,1,2,3) | 3 (4,6,12) | 9 | 11 | 5 | 36 | [0.66, 0.61] | 0.82 | 2 (r113/25,r142/25) | 2 | 0.57 | 24 | 1 | 2 (2) | 37 | W |
| `d7b66129` g1 | 08-07 | HTTP 418 v65 | 1000 | 4 (0,1,2,3) | 5 (6,12,19,269,328) | 21 | 15 | 3 | 55 | [0.86, 0.56] | 0.0 | 3 (r111/32,r140/16,r152/13) | 1 | 0.44 | 14 | 1 | 2 (2) | 804 | L |
| `d7b66129` g2 | 08-07 | HTTP 418 v65 | 1000 | 9 (0,1,2,3,152) | 6 (4,12,19,39,61) | 18 | 37 | 3 | 28 | [0.17, 0.73] | 0.0 | 6 (r113/25,r280/25,r656/25) | 2 | 0.36 | 17 | 1 | 4 (4) | 711 | L |
| `d7b66129` g3 | 08-07 | HTTP 418 v65 | 321 | 5 (0,1,2,3,144) | 4 (5,5,6,99) | 13 | 20 | 4 | 22 | [0.66, 0.66] | 0.0 | 3 (r176/25,r202/25,r227/32) | 2 | 0.26 | 44 | 3 | 3 (3) | 54 | L |
| `d7b66129` g4 | 08-07 | HTTP 418 v65 | 151 | 4 (0,1,2,3) | 2 (6,6) | 10 | 8 | 6 | 9 | [0.64, 0.73] | 1.0 | 0 () | 0 | 0.99 | 0 | 0 | 2 (2) | 38 | W |
| `d7b66129` g5 | 08-07 | HTTP 418 v65 | 327 | 6 (0,1,2,3,83) | 1 (4) | 2 | 16 | 3 | 48 | [0.9, 0.79] | 0.12 | 0 () | 2 | 0.02 | 0 | 0 | 4 (4) | 37 | L |
| `780059e5` g1 | 08-07 | kladde chatte tville (och oss) v65 | 102 | 4 (0,1,2,3) | 1 (6) | 2 | 5 | 3 | 3 | [0.25, 0.64] | 1.0 | 0 () | 0 | 0.96 | 0 | 0 | 2 (1) | 68 | L |
| `780059e5` g2 | 08-07 | kladde chatte tville (och oss) v65 | 219 | 5 (0,1,2,3,89) | 1 (4) | 2 | 5 | 3 | 32 | [0.9, 0.86] | 1.0 | 0 () | 2 | 0.73 | 0 | 0 | 2 (2) | 24 | L |
| `780059e5` g3 | 08-07 | kladde chatte tville (och oss) v65 | 227 | 4 (0,1,2,3) | 4 (4,6,12,166) | 9 | 35 | 2 | 47 | [0.65, 0.56] | 0.03 | 1 (r117/13) | 2 | 0.00 | 45 | 3 | 1 (1) | 100 | L |
| `780059e5` g4 | 08-07 | kladde chatte tville (och oss) v65 | 333 | 5 (0,1,2,3,83) | 4 (3,3,15,108) | 19 | 15 | 4 | 33 | [0.63, 0.63] | 0.13 | 3 (r114/25,r252/25,r296/13) | 2 | 0.50 | 4 | 0 | 2 (1) | 31 | W |
| `780059e5` g5 | 08-07 | kladde chatte tville (och oss) v65 | 191 | 5 (0,1,2,3,136) | 1 (4) | 3 | 14 | 2 | 12 | [0.71, 0.62] | 0.93 | 0 () | 2 | 0.21 | 0 | 0 | 2 (2) | 67 | L |
| `8a625993` g1 | 08-07 | Powered by SmartFridge v28 | 59 | 4 (0,1,2,3) | 1 (4) | 3 | 4 | 3 | 13 | [0.87, 1.08] | 1.0 | 0 () | 2 | 1.00 | 0 | 0 | 2 (1) | 41 | W |
| `8a625993` g2 | 08-07 | Powered by SmartFridge v28 | 105 | 5 (0,1,2,3,32) | 2 (6,10) | 15 | 3 | 3 | 6 | [0.9, 1.29] | 1.0 | 0 () | 0 | 1.00 | 0 | 0 | 3 (3) | 40 | W |
| `8a625993` g3 | 08-07 | Powered by SmartFridge v28 | 164 | 4 (0,1,2,3) | 3 (4,4,5) | 9 | 19 | 6 | 14 | [0.19, 0.45] | 0.11 | 1 (r118/25) | 2 | 0.33 | 46 | 4 | 2 (2) | 36 | W |
| `8a625993` g4 | 08-07 | Powered by SmartFridge v28 | 155 | 4 (0,1,2,3) | 3 (4,12,23) | 20 | 13 | 5 | 26 | [0.11, 0.72] | 0.15 | 1 (r113/25) | 2 | 0.47 | 35 | 2 | 2 (2) | 47 | W |
| `8a625993` g5 | 08-07 | Powered by SmartFridge v28 | 230 | 5 (0,1,2,3,44) | 2 (3,3) | 6 | 16 | 4 | 13 | [0.12, 0.08] | 0.06 | 2 (r120/25,r164/16) | 2 | 0.35 | 28 | 2 | 2 (2) | 26 | W |
| `f68a7d14` g1 | 08-07 | team lazy v94 | 169 | 4 (0,1,2,3) | 2 (6,6) | 10 | 6 | 4 | 8 | [0.73, 0.9] | 1.0 | 0 () | 0 | 0.92 | 0 | 0 | 2 (2) | 82 | W |
| `f68a7d14` g2 | 08-07 | team lazy v94 | 155 | 5 (0,1,2,3,83) | 3 (4,12,19) | 20 | 14 | 5 | 35 | [0.82, 0.98] | 0.29 | 1 (r119/25) | 2 | 0.43 | 0 | 0 | 3 (3) | 28 | W |
| `f68a7d14` g3 | 08-07 | team lazy v94 | 182 | 5 (0,1,2,3,112) | 3 (4,4,5) | 8 | 7 | 3 | 12 | [0.51, 0.12] | 0.0 | 1 (r116/25) | 2 | 0.30 | 29 | 3 | 1 (1) | 40 | W |
| `f68a7d14` g4 | 08-07 | team lazy v94 | 241 | 4 (0,1,2,3) | 3 (5,5,7) | 9 | 26 | 4 | 28 | [0.83, 0.12] | 0.5 | 1 (r147/25) | 2 | 0.39 | 25 | 2 | 1 (1) | 64 | W |
| `f68a7d14` g5 | 08-07 | team lazy v94 | 285 | 4 (0,1,2,3) | 1 (3) | 1 | 6 | 2 | 10 | [0.79, 0.79] | 1.0 | 0 () | 2 | 0.95 | 0 | 0 | 3 (3) | 262 | L |
| `e5796b91` g1 | 08-07 | O(1) v8 | 142 | 4 (0,1,2,3) | 3 (4,4,5) | 8 | 13 | 7 | 11 | [0.51, 0.12] | 0.23 | 1 (r114/25) | 2 | 0.39 | 14 | 1 | 1 (1) | 72 | W |
| `e5796b91` g2 | 08-07 | O(1) v8 | 1000 | 4 (0,1,2,3) | 3 (3,3,15) | 15 | 5 | 2 | 33 | [0.9, 1.17] | 1.0 | 0 () | 2 | 0.00 | 0 | 0 | 1 (1) | 153 | W |
| `e5796b91` g3 | 08-07 | O(1) v8 | 162 | 5 (0,1,2,3,117) | 3 (5,5,7) | 9 | 11 | 7 | 23 | [0.73, 0.73] | 0.45 | 2 (r122/25,r142/25) | 2 | 0.40 | 0 | 0 | 3 (3) | 69 | W |
| `e5796b91` g4 | 08-07 | O(1) v8 | 204 | 4 (0,1,2,3) | 3 (4,6,12) | 9 | 18 | 5 | 54 | [1.11, 0.07] | 0.39 | 2 (r113/25,r126/25) | 2 | 0.35 | 0 | 0 | 2 (2) | 63 | W |
| `e5796b91` g5 | 08-07 | O(1) v8 | 1000 | 4 (0,1,2,3) | 1 (8) | 3 | 4 | 2 | 6 | [0.57, 0.78] | 1.0 | 0 () | 2 | 0.13 | 0 | 0 | 2 (2) | 36 | L |
| `449dab71` g1 | 08-07 | team lazy v104 | 149 | 4 (0,1,2,3) | 3 (4,4,5) | 8 | 20 | 3 | 11 | [0.51, 0.51] | 0.1 | 2 (r109/25,r110/25) | 2 | 0.28 | 60 | 5 | 2 (2) | 22 | W |
| `449dab71` g2 | 08-07 | team lazy v104 | 136 | 4 (0,1,2,3) | 3 (5,5,6) | 9 | 16 | 4 | 14 | [0.59, 0.59] | 0.69 | 2 (r114/25,r115/25) | 2 | 0.44 | 46 | 3 | 2 (2) | 40 | W |
| `449dab71` g3 | 08-07 | team lazy v104 | 134 | 4 (0,1,2,3) | 3 (3,3,15) | 15 | 16 | 6 | 48 | [0.75, 0.75] | 1.0 | 2 (r115/25,r119/25) | 2 | 0.57 | 28 | 2 | 2 (2) | 35 | W |
| `449dab71` g4 | 08-07 | team lazy v104 | 150 | 4 (0,1,2,3) | 3 (4,6,12) | 9 | 13 | 4 | 30 | [0.39, 0.66] | 0.54 | 2 (r114/25,r140/13) | 2 | 0.40 | 46 | 3 | 2 (2) | 32 | W |
| `449dab71` g5 | 08-07 | team lazy v104 | 1000 | 4 (0,1,2,3) | 1 (4) | 3 | 22 | 3 | 11 | [0.62, 0.62] | 0.91 | 0 () | 2 | 0.53 | 0 | 0 | 2 (2) | 158 | L |
| `79b4066c` g1 | 08-07 | O(1) v10 | 181 | 5 (0,1,2,3,98) | 3 (6,12,31) | 18 | 7 | 5 | 34 | [0.18, 0.93] | 0.29 | 1 (r116/25) | 1 | 0.39 | 0 | 0 | 2 (2) | 87 | W |
| `79b4066c` g2 | 08-07 | O(1) v10 | 514 | 4 (0,1,2,3) | 2 (6,10) | 11 | 22 | 4 | 7 | [0.77, 0.73] | 1.0 | 0 () | 0 | 0.82 | 0 | 0 | 2 (2) | 252 | L |
| `79b4066c` g3 | 08-07 | O(1) v10 | 1000 | 5 (0,1,2,3,269) | 1 (4) | 2 | 8 | 3 | 25 | [0.94, 0.97] | 0.62 | 0 () | 2 | 0.04 | 0 | 0 | 3 (3) | 24 | W |
| `79b4066c` g4 | 08-07 | O(1) v10 | 149 | 4 (0,1,2,3) | 3 (5,5,13) | 17 | 11 | 6 | 25 | [0.15, 0.2] | 0.18 | 1 (r115/25) | 2 | 0.57 | 28 | 2 | 1 (1) | 38 | W |
| `79b4066c` g5 | 08-07 | O(1) v10 | 158 | 5 (0,1,2,3,98) | 3 (4,12,23) | 19 | 8 | 4 | 44 | [0.9, 0.9] | 1.0 | 2 (r135/25,r137/25) | 2 | 0.64 | 0 | 0 | 3 (3) | 44 | W |
| `24286407` g1 | 08-07 | O(1) v11 | 361 | 4 (0,1,2,3) | 1 (6) | 2 | 8 | 3 | 4 | [0.53, 0.25] | 1.0 | 0 () | 0 | 0.80 | 0 | 0 | 3 (2) | 350 | L |
| `24286407` g2 | 08-07 | O(1) v11 | 189 | 4 (0,1,2,3) | 1 (3) | 1 | 3 | 3 | 9 | [0.76, 0.79] | 1.0 | 0 () | 2 | 0.92 | 0 | 0 | 3 (3) | 69 | L |
| `24286407` g3 | 08-07 | O(1) v11 | 1000 | 4 (0,1,2,3) | 1 (8) | 3 | 4 | 2 | 6 | [0.57, 0.78] | 1.0 | 0 () | 2 | 0.13 | 0 | 0 | 2 (2) | 36 | L |
| `24286407` g4 | 08-07 | O(1) v11 | 182 | 5 (0,1,2,3,68) | 3 (5,5,6) | 9 | 13 | 5 | 21 | [0.66, 0.66] | 0.31 | 2 (r114/25,r121/25) | 2 | 0.27 | 0 | 0 | 3 (3) | 87 | W |
| `24286407` g5 | 08-07 | O(1) v11 | 160 | 4 (0,1,2,3) | 3 (5,5,6) | 11 | 9 | 4 | 14 | [0.26, 0.19] | 0.22 | 1 (r112/25) | 2 | 0.53 | 34 | 3 | 1 (1) | 16 | W |
