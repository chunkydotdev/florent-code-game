# What Jython changed: v137 -> v149 decoded off the replay corpus

**Research arm, 2026-08-16. Read-only corpus analysis. No bots edited, no matches run.**
Question, from Magnus: *Jython was below us and is now #1 at 2134 (1,515 matches); we are at 1802. What did they change?*
The WHEN was already established and is not re-derived here: the step is **v146**
(2026-08-15T00:12:59, 88.0% game share over 25 games), sustained by **v149**
(first seen 02:52:59, 64.9% over 225 games, carried 1860 -> 2055). Pre-jump
reference is **v137**.

---

## SUMMARY (six lines)

1. **They swapped the gunner out for the sentinel.** Gunner builds **4.04 -> 0.94** per game, sentinel **2.57 -> 5.47**; gunner shots **67 -> 17**, sentinel shots **23 -> 50**. Up in **7 of 7** common opponents.
2. **The forward sentinel now arrives at round 27 instead of round 44, and in twice as many games.** First sentinel *adjacent* to the enemy core: median **r95 -> r28**, present in **44.2% -> 89.0%** of games (+44.7pp, CI [+32.4,+57.1]).
3. **They stopped chewing the core with builder bots.** Builder attacks on the enemy core **84.8 -> 17.4** per game; builder bots built **13.9 -> 7.1**.
4. **What did NOT change is the striking part: the disposable launcher ladder.** Both versions ferry a builder bot to the enemy core by **median round 9** using launchers built and demolished at ~1-2 round lifetimes. Launcher volume, kidnap volume, forward-barrier ring and the harvester opening are all unchanged. **v146/v149 changed the payload, not the delivery.**
5. **Both controls stayed flat.** HTTP 418 at a *fixed* v103 (223 vs 278 replays) and Kvarnholmen at a fixed v18 (230 vs 205) move on **none** of the headline metrics across the same two dates; a 1,200-comparison split-half placebo on the v137 cohort fired 0.6% of the time.
6. **Most transferable: the delivery, not the payload.** We already build forward sentinels for the same stated reason (1.92/game), collar barriers and defensive kidnap — we just arrive at **median r30** where Jython arrives at **median r7**, the fastest in the league. **A launcher chain used as TRANSPORT is unqueued and unimplemented** (`ct.destroy()` appears zero times in our tree). Its cost objection is already answered by row **#60** — but pitch it as an arrival-round plank, because #60 measured and closed the scale-saving version.

---

## 1. Populations, and what they are

| cohort | what | replays | matches | dates | trigger mix |
|---|---|---|---|---|---|
| **PRE** | Jython **v137**, Jython's own side | **165** | 33 | all 2026-08-14 | 85 unrated / 80 ladder |
| **POST** | Jython **v149**, Jython's own side | **145** | 29 | all 2026-08-15 | 125 unrated / 20 ladder |
| **CONTROL A** | **HTTP 418 v103** — version *identical* on both dates | 223 / 278 | — | 08-14 vs 08-15 | mixed |
| **CONTROL B** | **Kvarnholmen v18** — version *identical* on both dates | 230 / 205 | — | 08-14 vs 08-15 | mixed |

Jython's team index is derived per file from `meta_join.teamAName`/`teamBName`,
never assumed to be 0. Every number below is **Jython's own side only** unless
it says otherwise.

**All four cohorts are post-rotation** (the 2026-08-13 map change): every replay
completed 08-14 or 08-15. Map identity could not be matched (`league_maps.tsv`
stops at 08-14 and covers only 16 named teams — **0 of 145** v149 replays carry a
map name), so map pool was controlled on **map SIZE profile** instead, read
per-replay off `events.tsv`: both cohorts draw the same 7 sizes, total-variation
distance **PRE vs POST = 0.059**, while the *control's own* shift across the same
dates is larger at **0.119** and still produced null deltas.

---

## 2. WHAT MOVED

All intervals are **DEFF-corrected at 1.833** (pooled unrated, s40 2026-08-14) —
both the match and the opponent cluster can hold more than one game in these
cohorts, so the pooled constant applies.

### 2.1 Gunner -> sentinel substitution (the composition change)

| metric, per game | v137 (n=165) | v149 (n=145) | delta, 95% CI | CONTROL A | CONTROL B |
|---|---|---|---|---|---|
| gunner builds | 4.04 | 0.94 | **-3.10 [-4.39,-1.80]** | +0.40 (incl 0) | +0.57 (incl 0) |
| sentinel builds | 2.57 | 5.47 | **+2.90 [+1.15,+4.64]** | -0.17 (incl 0) | -0.23 (incl 0) |
| gunner shots | 67.1 | 17.4 | **-49.7 [-72.7,-26.8]** | +11.4 (incl 0) | — |
| sentinel shots | 23.0 | 50.3 | **+27.4 [+15.5,+39.2]** | -11.7 (incl 0) | — |
| games with a gunner in range of the enemy core | 33.3% | 7.6% | **-25.7pp [-37.1,-14.4]** | +5.5pp (incl 0) | — |

**Opponent-balanced** (unweighted mean of per-opponent means over the **7
opponents both cohorts faced** — 0033, Dino, Lorem Ipsum, O(1), OpenSverige,
Torsko, ph; 95 PRE games / 110 POST games): gunner **2.97 -> 0.99**, sentinel
**1.61 -> 6.14**. **Sentinel is up in 7 of 7 opponent cells; gunner is down in 6
of 7.**

The split is both at home and forward — sentinels **HOME 0.12 -> 1.59** and
**FORWARD 2.45 -> 3.88** per game; gunners **HOME 2.14 -> 0.50**, **FORWARD 1.90
-> 0.43**. The ammo budget barely moved (`ammo_converted` 559 -> 600, CI includes
0) — the same ammunition is now spent through a weapon with **r²=32 reach that
ignores obstacles** instead of one with r²=13 that does not.

### 2.2 The forward sentinel arrives ~67 rounds earlier, in twice as many games

| metric | v137 | v149 | delta, 95% CI | CONTROL A |
|---|---|---|---|---|
| first sentinel within its own range (d²≤32) of the enemy core | mean 92.7, **median r44** | mean 50.2, **median r27** | **-42.5 [-81.5,-3.5]** | 165.3 -> 161.7, median r116 both (incl 0) |
| first sentinel *adjacent* to the enemy core (d²≤13) | mean 195.2, **median r95** | mean 66.5, **median r28** | **-128.7 [-199.1,-58.3]** | 163.6 -> 164.8 (incl 0) |
| share of games with a forward sentinel | 76.4% | 95.2% | **+18.8pp [+8.8,+28.8]** | 58.3% -> 55.8% (incl 0) |
| share with a sentinel *at* the enemy core | 44.2% | **89.0%** | **+44.7pp [+32.4,+57.1]** | 31.4% -> 34.5% (incl 0) |

Sentinel median build round falls **r265 -> r143** overall, and in the r0-30
window their sentinels sit at median **d²=10 from the enemy core** — one to three
tiles off the footprint, inside a range that ignores intervening walls.

### 2.3 Builder-bot melee on the core is abandoned

| metric, per game | v137 | v149 | delta, 95% CI | CONTROL A |
|---|---|---|---|---|
| builder attacks **on the enemy core** | 84.8 | 17.4 | **-67.4 [-99.2,-35.6]** | 0.00 -> 0.00 (never does this) |
| builder attacks, all targets | 295.9 | 90.1 | **-205.8 [-282.4,-129.1]** | 62.5 -> 56.7 (incl 0) |
| builder bots built | 13.87 | 7.06 | **-6.81 [-9.67,-3.95]** | +0.34 (incl 0) |
| heals | 164 | 96 | **-68** | -26 (incl 0) |

A builder does 2 damage per attack; a 500 HP core is 250 attacks. v137 was
grinding the core down by hand and paying for it in builder bots. v149 shoots it.

### 2.4 Within-cohort mechanism check (observational, not causal)

Stratifying v149's own games on *when* the forward sentinel went up:

| stratum | v137 | v149 |
|---|---|---|
| forward sentinel by r50 | n=82, P(kill)=0.43, median kill **r454** | n=105, P(kill)=**0.74**, median kill **r120** |
| forward sentinel r51+ | n=44, P(kill)=0.57, median kill r547 | n=33, P(kill)=0.88, median kill r171 |
| **no forward sentinel** | n=39, P(kill)=**0.10** | n=7, P(kill)=**0.00** |

**No forward sentinel, essentially no kill — in both versions.** The v149 change
is that the same stratum now converts at **median r120 instead of r454**, i.e.
the sentinels are not merely present earlier, they are *firing at the core* where
v137's largely were not (sentinel shot rate 0.046/round -> 0.169/round).

### 2.5 Outcomes — real, but read the caveat

| metric | v137 | v149 | delta, 95% CI | CONTROL A | CONTROL B |
|---|---|---|---|---|---|
| P(enemy core destroyed) | 0.39 | 0.74 | **+0.35 [+0.21,+0.49]** | +0.03 (incl 0) | +0.04 (incl 0) |
| P(own core destroyed) | 0.44 | 0.19 | **-0.25 [-0.38,-0.11]** | +0.02 | -0.04 |
| game length (last event round) | 494.9 | 296.8 | **-198 [-285,-111]** | -48.6 (incl 0) | +11.3 (incl 0) |
| mean kill round (decisive games) | 492 (n=64) | 219 (n=107) | **-273** | -11 (incl 0) | +65 (incl 0) |

Opponent-balanced over the 7 common opponents: **P(kill) 0.28 -> 0.66** (up in
6/7, flat in 1, down in 0); **P(own core dies) 0.61 -> 0.26** (down in 6/7).

⚠ **CAVEAT, stated plainly.** The v149 archive is **125 of 145 unrated**. Split
by trigger, the *outcome* gain sits almost entirely in the unrated stratum
(unrated P(kill) 0.35 -> 0.78; the 20 ladder games read 0.42 -> 0.45 and P(own
core dies) 0.35 -> 0.55). **n=20 ladder games cannot carry a verdict**, and the
platform rating (+306 in a day) says the ladder gain is real — so the honest
reading is that our archive cannot independently confirm the *magnitude* of the
outcome change on the rated surface. **The composition and timing deltas hold in
BOTH strata** (sentinel 3.42 -> 5.65 ladder / 1.76 -> 5.44 unrated; gunner 4.88
-> 2.50 ladder / 3.25 -> 0.69 unrated), which is what this document rests on.

---

## 3. WHAT DID **NOT** MOVE — and this is the load-bearing negative

### 3.1 The disposable launcher ladder was already there in v137

This is the single most interesting structure in Jython's bot, and **v146/v149
did not introduce it.** Reconstructed from one v149 replay
(`02d1be66-…_game_1.replay26`, 30x30, Jython = team 1, opponent 0033):

```
r1  BUILD launcher (24,14)  d2_own=4    d2_enemy=484     <- next to their own core
r2  DEATH launcher (24,14)                               <- demolished one round later
r3  BUILD launcher (18,15)  d2_own=65   d2_enemy=257     <- ~6 tiles further
r4  DEATH launcher (18,15)
r5  BUILD launcher (12,14)  d2_own=196  d2_enemy=100
r6  DEATH launcher (12,14)
r7  BUILD launcher ( 7,15)  d2_own=362  d2_enemy=26
r9  BUILD launcher ( 2,12)  d2_own=580  d2_enemy=4       <- ADJACENT TO THE ENEMY CORE, ROUND 9
r14 BUILD launcher ( 1,16)               d2_enemy=5
r16 BUILD launcher ( 1,13)               d2_enemy=2
r22 BUILD sentinel ( 0,15)               d2_enemy=5      <- the payload
```

A builder bot builds a launcher one tile ahead; the launcher throws it forward
(engine limit d²≤26 from the launcher, ~5 tiles); the bot builds the next
launcher; the spent launcher is removed. **A ~24-tile crossing in 9 rounds, at
one hop every two rounds.**

Measured across the cohorts, both versions:

| ladder metric | v137 | v149 |
|---|---|---|
| launcher builds/game | 6.39 | 5.66 (**CI includes 0**) |
| **median launcher lifetime (build -> death, same tile)** | **2 rounds** | **1 round** |
| share of launchers living ≤3 rounds | 57.7% | 72.6% |
| launchers built by r15 / destroyed by r15 | 3.04 / 1.99 | 4.19 / 2.72 |
| net launchers standing at r15 | 1.04 | 1.46 |
| **first launcher at the enemy core (d²≤13)** | **median r9** | **median r9** (mean 22.6 -> 19.0, CI includes 0) |
| share of games where that happens | 78.2% | 89.7% (+11.5pp, CI [+0.6,+22.3] — marginal) |

**INFERRED, not measured:** the demolition is very likely there to keep the
**additive global cost scale** flat — a launcher is +10% and destruction removes
its contribution (`CLAUDE.md`, engine-confirmed s26). The corpus carries no scale
trace, so this is a hypothesis about why, not a measurement.

### 3.2 Also unchanged

* **Forward barrier ring at the enemy core.** 92.1% -> 98.6% of games; first one
  at median **r7 -> r9**; **96-98% of all their barriers are built in the enemy
  half**, at median d²=4-5 from the enemy core. The per-game count fell 22.4 ->
  15.2 but games are 40% shorter — the *opening* barrier rate is flat-to-up
  (r0-50: 6.10 -> 6.91, CI includes 0). Spawn-tile denial / core walling, in both
  versions.
* **Kidnap volume.** Enemy-builder throws (`throws.tsv` kind `EXILE`): **median
  17 -> 14 per game**. Present at high volume in both. ⚠ The *means* (48.4 ->
  32.4) are outlier-driven — **5 of 145 v149 games carry 52.5% of all throws**
  (max 3,925 in one game, a launcher ping-pong loop with victim life 2.3 rounds).
  **Report the median.**
* **Kidnap does not crash victims — for them either.** Using the new s42 victim
  columns: of victims that DIED, **0 of 98 (v137) and 0 of 57 (v149)** carry the
  `vhp == 0` no-HP-event crash signature. Their exiles are combat deaths, not
  exception-induction.
* **Economy opening.** First harvester median **r6 -> r7**; harvester builds in
  r0-50 **2.27 -> 2.72**. Conveyor r0-50 **7.07 -> 9.59**. Whole-game harvester
  and conveyor totals fall, but that tracks the 198-round shorter game.
* **Map pool** (see §1) and **map size** (mean width 22.95 -> 23.26).

---

## 4. CONTROLS AND INSTRUMENT CHECKS

* **Two version-fixed controls**, chosen because their submission version is
  byte-identical across the two dates: **HTTP 418 v103** (223 vs 278 replays) and
  **Kvarnholmen v18** (230 vs 205). **Neither moves on any headline metric** —
  sentinel builds, gunner builds, P(kill), game length, forward-sentinel arrival
  round, forward-sentinel share: every interval includes 0. The one thing the
  controls *do* show is a mild era drift in build-to-enemy-core distances
  (barrier d²_enemy -16.7 for the control vs -14.9 for Jython) — **so Jython's
  barrier-geometry shift is ERA, not a Jython change, and is excluded above.**
  Sentinel d²_enemy moves *+34.3 for Jython and -21.2 for the control*, opposite
  directions, so that one is real.
* **Placebo.** 200 random split-halves of the v137 cohort x 6 headline metrics =
  1,200 comparisons; **7 (0.6%)** exceeded their 95% CI against an expected ~5%.
  The instrument returns null when it should.
* **Seat mapping validated, not assumed.** `meta_join.us_side` 'a' -> team 0,
  'b' -> team 1 agrees with `join.tsv.our_team` in **4,115 of 4,115** overlapping
  rows.
* **Cross-instrument agreement.** `events.tsv` BUILD counts equal
  `build_agg.tsv` `build_*` counts at **ratio 1.000** for all 7 entity types x
  both Jython cohorts — so TRAP 1 (rotate re-emits `placeEntity` and inflates
  gunner builds) is not biting here.
* **Constant-column sweep** over the 1,231-file subset of `econ.tsv`: only
  **`deliveries`** is dead (constant 0, TRAP 8). It is not used anywhere above.
  `shots`/`shots_gunner`/`shots_sentinel` are populated in this subset and were
  cross-checked against `build_agg`'s `shot`.
* **`wincond.tsv` is stale** (built 2026-08-15 05:54) and covers **0 of 145**
  v149 replays — a win-condition cut off it would have silently dropped the
  entire POST cohort. Win/kill/turns were re-derived from in-replay `DEATH core`
  events instead.
* **`meta_join`, not `ladder_games`, is correct here** — the subject is another
  team's games, and no win-rate denominator for *our* rated record is computed.

---

## 5. FIELD CONTEXT — how rare is this?

Across every 2026-08-15-or-later replay in the archive, per team, own side
(teams with ≥60 archived games; **archive coverage is uneven and us-heavy, so
treat this as a ranking, not a census**):

| team | games | launchers/gm | fwd sentinels/gm | **% games reaching the enemy core (d²≤13)** | **median round of arrival** |
|---|---|---|---|---|---|
| **Jython** | 475 | 5.27 | 3.01 | 100.0% | **7** |
| Powered by SmartFridge | 115 | 5.58 | 0.21 | 100.0% | 26 |
| Juusto | 300 | 3.47 | 2.06 | 97.3% | 21 |
| lingling_40h | 225 | 3.17 | 1.05 | 84.0% | 38 |
| **OpenSverige (us)** | 827 | **0.26** | **1.92** | 93.2% | **30** |
| Torsko | 955 | 0.00 | 1.91 | 25.0% | 111 |
| HTTP 418 | 318 | 0.00 | 1.21 | 78.0% | 47 |

**Jython arrives at the enemy core faster than any other team in the league, by
14 rounds over the next-fastest, and only four teams build launchers at volume at
all.**

## 6. OUR OWN RATED READ ON THEM

`ladder_games.tsv`: **55 rated ladder games vs Jython across 11 matches.**
2026-08-13 we took 12/15 (80%) against their v33/v119; 2026-08-14 we took 19/40
(48%) against v136/v137/v144/v145. **We have played zero rated games against
v146 or later** — we have no rated read at all on the version that took them to
#1.

---

## 7. TRANSFERABILITY

### T1 — Disposable launcher ladder (fast forward delivery). **THE ONE WORTH A LEG — and it contradicts a premise our incumbent is built on.**
* **What it is:** builder builds a launcher one tile ahead, is thrown ~5 tiles by
  it, builds the next, and the spent launcher is demolished. ~4 launchers built
  and ~2.7 demolished by r15; net 1.5 standing. Arrival at the enemy core by
  **median r9**.
* **THE SHARP POINT — and it is the MOVEMENT, not the money.** The demolish step
  on its own is already-known and already-closed (QUEUE **#60**, withdrawn, from
  Juusto — see the cross-check below). What is new is using the chain **as a
  transport mechanism**. `bots/_v223sealrepair/main.py:598-608` states our
  current doctrine and its reasoning verbatim:
  > *"THE COST WE ACTUALLY PAY, and it is not the 20 Ti: each launcher adds +10%
  > to the ONE GLOBAL ADDITIVE scale factor, which inflates EVERY subsequent
  > build of EVERY type … **Bought at r10 that surcharge is levied on the entire
  > game**; bought at r150 it is levied on the tail only."*

  Our answer to that cost was **LOKI-42 LAUNCHER DEFERRAL —
  `doctrine.py:1536, LAUNCHER_MIN_RND = 160`: we build no launcher at all before
  round 160.** Jython's answer to the same cost is the opposite and, on the
  engine's own rule, better: **build at r1 and DESTROY it at r2.** Destruction
  removes the +10% contribution (`CLAUDE.md`, engine-confirmed s26), so the
  surcharge is levied for **one to two rounds**, not for the whole game. The
  premise in that comment — that an early launcher taxes the entire match — is
  **true only for a launcher you keep.**
* **We have no mechanism for this at all.** `grep -n "\.destroy(\|can_destroy"`
  over the entire incumbent (`main.py`, `raid.py`, `eco.py`, `doctrine.py`)
  returns **zero matches**. We have never demolished one of our own buildings.
  `ct.destroy()` is free, uncooldowned and unlimited per turn.
* **What we do have:** a ferry (`raid.py:851 _advertise_for_hop`, `:875
  _launcher_turn`) that throws our own bot forward from **one launcher near
  home** (`main.py:615` — *"One Launcher, near home"*). We ride a launcher; we
  do not chain them.
* **Why it matters to OUR programme specifically:** `R1000_IS_DEFEAT`, kill
  window r300, our median kill is r174 and our median death r187 — a
  thirteen-round race. **Field-wide we arrive at the enemy core at median r30 and
  Jython at median r7.** Moving the earlier side of that race is exactly the
  currency `PROGRAMME.md` pays.
* **What would have to change:** (a) a build-hop-demolish loop in the raid path;
  (b) `LAUNCHER_MIN_RND` relaxed or bypassed for ladder launchers specifically;
  (c) a first use of `ct.destroy()` anywhere in the tree.
* **Risks, honestly:** each hop leaves a builder alone in enemy territory; the
  ferried bot is itself a kidnap target; ~4 launcher builds is ~60-80 Ti of
  opening spend competing with harvesters; and the demolition step is exactly
  where a bug leaves the +10% standing.
* **Pre-registrable falsifier:** if the ladder does not reduce our median
  round-of-first-build-within-d²≤13-of-the-enemy-core below ~r15, it has not
  delivered its mechanism regardless of what happens to win rate.

### T2 — Gunner -> sentinel substitution. **WE ALREADY DO THIS, AND FOR THE SAME STATED REASON.**
Field cut: we build **1.92 forward sentinels/game and 0.74 gunners/game** —
already sentinel-weighted, closer to v149 than to v137. `doctrine.py:1231-1237`
says it outright: *"The barrier collar blocks LOS, so a GUNNER ray dies on our
own wall. The [sentinel] … shoots THROUGH the seal into the Core. 18 dmg"*, with
`LOKI_FWD_GUN_CAP = 3`. **Jython arrived at a conclusion we already hold.** Low
headroom; not a plank. The residue is *reliability* — they place a forward
sentinel in 95.2% of games.

### T3 — Forward barrier ring at the enemy core. **RIGHT DOCTRINE, WRONG VOLUME AND CLOCK.**
Jython: barriers at median d²=4-5 of the enemy core, **~15/game, first at r9**.
Us: the same geometry (`raid.py:267-280`, the collar; 99% on the enemy ring,
median d²=4) at **4.2/game, first at median r65** — the gap QUEUE **#31** (the
barrier family, open) already names against Clankers/Pantheon at 15-18/game. So
this is a live, queued volume/timing plank and Jython is a second independent
sighting of the high-volume form. Note the dependency: **you cannot ring a core
you cannot reach by r9**, so T3's clock is downstream of T1's.

### T4 — Builder-melee de-emphasis. **NOT A PLANK FOR US.**
Their change was to stop doing something we do less of anyway. Worth knowing as
an opponent model, not as an adoption.

### T5 — Kidnap. **CONFIRMS A NEGATIVE WE ALREADY HOLD — WITH ONE LIVE THREAD.**
Jython kidnaps at median 14-17 enemy builders/game and **0 of 155 victim deaths
across both cohorts carry the `vhp == 0` crash signature.** Independent
corroboration, from another team's bot, that exile-to-border is not converting
into permanent unit destruction at any measurable rate on the current field.
We already exile defensively (`raid.py:909-931`, unaimed, farthest-from-our-core).
The *forward* form is QUEUE **#58**, refuted as designed — but refuted **against
0033, whose builders never enter the d²≤2 pickup envelope**. Jython's builders
demonstrably do come forward. That is a target-selection question #58 did not
get to ask, not a reopening of #58.

### Our incumbent's doctrine, for the record
`raid.py`'s collar: raiders advance to a 12-tile ring around the enemy core
(`raid.py:88-100`), seal the heal seats with barriers to drive the defender's
heal rate to zero (`raid.py:20-29`, 3 Ti / 30 HP barrier vs 15 pecks to break —
a 10:1 exchange), and the damage comes from a **forward sentinel** planted so its
ray already contains a core tile (`raid.py:636-698`) — *sentinel and not gunner
"not as a preference, it is forced: barriers block LOS… the Sentinel line ignores
obstacles"* (`raid.py:639-641`). Builder melee is globally silenced
(`LOKI_QUIET_ON = True`, `doctrine.py:1488`). **One stationary launcher near home**
exiles intruders and single-hop-ferries our raiders (`main.py:593-663`,
`raid.py:875-958`) — **never a chain.** Structurally we are already the v149
shape; we are slow to arrive and thin on volume.

### QUEUE cross-check (full sweep, `QUEUE.md` read in full)

| plank | QUEUE row | status | shipped in `_v223sealrepair`? |
|---|---|---|---|
| **T1 ladder as a MOVEMENT relay** | **none** | **GENUINE GAP — unqueued** | no |
| T1's demolish step, alone | **#60 "RENT, DON'T OWN"** (`QUEUE.md:158`) | **WITHDRAWN by its own owner** | no (`ct.destroy` = 0 hits) |
| launcher, home/approach-triggered | **#47** (`:145`) | **LIVE ROAD CLOSED** s40 (`_v207apprlaunch` 8/20 vs 9/20) | no |
| launcher stationed forward to evict | **#58** | **REFUTED AS DESIGNED** (0.04 evictions/game vs a >1.0 bar, vs 0033) | no |
| T2 forward sentinel | **#23** (⭐⭐⭐ "FORWARD PLACEMENT"), **#41** siting, **#42** volume-not-sequence | open, tuning volume/timing | **yes** — `raid.py:636-698`, cap 3 |
| T3 gunner→sentinel | **#21 "THE GUNNER COUNT"** | open, and its conclusion is the **inverse** (*"ADDITIVE, not a swap"*) | **yes, already sentinel-first** — `main.py:556-559` |
| T4 forward barrier ring | **#31 barrier family** (`:644`), **#52**, **#53** | open, volume gap: we run **4.2/game from r65**, field leaders 15-18 | **yes** — `raid.py:267-280` |
| T5 kidnap | **#51**, **#38**, **#59** | open (defensive form) | **yes, defensively only** — `raid.py:909-931`, unaimed |

**⛔ THE ROW THAT MATTERS MOST IS #60, AND IT CUTS BOTH WAYS.** It already
carries the demolish mechanism — imported from **Juusto**, not Jython (*"403
launchers in 110 games, 402 demolished at an age of exactly 2 rounds"*) — with
the engine fact source-read, and with exactly the argument I reached
independently: *"The launcher premium our own sweep priced at −6.34pp is the
PERMANENT scale contribution of a launcher we KEEP; a demolished one leaves none
of it."*

**It was WITHDRAWN by its owner ~10 minutes after stocking, on a measurement:**
*"launcher = **2.0% of a 308.2% scale contribution at 8.2% coverage**"* — i.e.
for our bot the scale saving from renting launchers is ~2% of the scale we carry,
which is not worth a leg. Its registered mechanism metric was separately inert
(`get_scale_percent()` at r50/r100/r150 while `LAUNCHER_MIN_RND = 160`).

**⇒ THE HONEST CONSEQUENCE FOR T1: DO NOT PITCH IT AS A SCALE PLANK. #60 already
measured that road and closed it.** The demolish step is an **enabler** — it is
what makes four launchers in the opening affordable at all — but the **payoff is
delivery speed**: arrival at the enemy core at median **r7-9 instead of r30**,
20+ rounds earlier into a race our own median kill (r174) loses to our own median
death (r187) by thirteen rounds. That is a **movement mechanism**, and **no
QUEUE row proposes one.** #47 and #58 are both *stationary* launcher designs and
both are closed; #60 is a *cost* design and is withdrawn. **T1 is genuinely new
work, and it must be pre-registered on an ARRIVAL-ROUND bar, not a scale curve.**

⚠ **And #60's own limit transfers verbatim: the titanium is NOT refunded, only
the scale contribution.** Four ladder launchers is ~80 Ti spent in the r0-15
window — the same window that buys our harvesters. That is the cost the arm has
to beat.

Rows #47/#58 already record the field fact that motivates the payload half:
*"Jython, Focalground, LingLing40 at 22-33 throws/game against us"*. **This
document is the first read of HOW Jython gets those throws that far forward.**

---

## 8. WHAT I COULD NOT DETERMINE

1. **Whether the demolition is for the cost scale.** INFERRED from the additive
   +10%/-10% rule and the measured 1-2 round launcher lifetime. The corpus has no
   scale trace; an engine probe or a `get_scale_percent` read would settle it.
2. **Which entity lands the killing damage.** The corpus deliberately omits
   per-source damage attribution (`corpus-howto.md`, "What this does NOT give
   you"). The sentinel story is an inference from co-timing plus the shot counts,
   not a damage ledger.
3. **The rated magnitude of the outcome gain** — only 20 v149 ladder games are
   archived (§2.5).
4. **Map-name-level matching for v149** — 0 of 145 replays carry a map name;
   controlled on size profile instead.
5. **Their source.** Every mechanism sentence here is a hypothesis about observed
   behaviour, from one worked replay plus cohort aggregates.
6. **What v146 specifically did** — only 10 v146 replays are archived, too few to
   separate it from v149. Everything above is the v137 -> v149 delta.
