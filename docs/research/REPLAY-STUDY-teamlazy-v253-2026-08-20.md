# REPLAY STUDY — team lazy v253 (and v246), 2026-08-20

**Provenance.** Fresh opus subagent (no inherited session context beyond the
inputs named here), commissioned by the research lane s52, 2026-08-20.
**Method:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` (DISCIPLINE
section). **Inputs:** `corpus/join.tsv`, `corpus/ladder_games.tsv`,
`corpus/league_matches.tsv`, `corpus/events.tsv`, `corpus/builds.tsv`,
`corpus/build_agg.tsv`, `corpus/econ.tsv`, `replay_archive/*.replay26`
(85 files, all present locally), `tools/corpus/replay_autopsy.py`,
`tools/replay_schema.md`, `docs/research/corpus-howto.md`,
`docs/research/OPP-team-lazy-profile-2026-08-13.md` (the v222-era prior),
`QUEUE.md`, `bots/_v488beltbreak2/` (read-only control tree).
**Population:** the 80 rated ladder games we have decoded against team lazy at
their v246 and v253 (40 + 40), plus 5 at v247 held out as too thin.
**Surface:** rated ladder, us-only archive. No platform calls, no games fired,
no bot edits. Not committed by this agent.
**Interruptions:** this session was cut twice by machine-sleep API errors
mid-run. Completed measurement passes were retained (they are reproducible from
the scripts described inline); nothing was re-derived from memory.

Every claim below is tagged **MEASURED** (counted from decoded events) or
**EYEBALL** (seen, not yet counted). Refuted mechanisms are RETAINED.

---

## 0. Instrument checks run before anything was believed

**A. TRAP 7 cleared for this study — the seat variable is real, not
winner-derived.** `corpus-howto.md` warns that `join.our_team` descends from
`winnerSide` and that cross-checking it against `ladder_games.won` is circular.
The independent check the doc asks for is a **behavioural fingerprint**, and one
exists here with a hard zero on the other side: **we build launchers, team lazy
builds none.**

> **MEASURED.** Per-game launcher builds (`build_agg.tsv`, metric
> `build_launcher`) over all 85 files: the side `join.our_team` calls US has
> >0 launchers and the other side has 0 in **82 of 85 games; 0 contradictions;
> 3 uninformative** (neither side built one). Team lazy: **0 launchers and 0
> splitters in 80 of 80 games** — unchanged from the v222-era profile's
> "zero splitters, zero launchers, 10/10".

**B. The damage ledger self-checks.** `replay_autopsy.py` requires attributed
core damage to equal the summed `UpdateHp` deltas on the core id.
**MEASURED: 85 of 85 games report `MATCH`; 0 failures.**

**C. Dead columns avoided.** `econ.tsv`'s `shots` and `deliveries` are
identically zero (traps 5/8) and are not used here. Shot counts come from
`build_agg.tsv` metric `shot`.

---

## 1. P1–P3: what the premises hold up as

| premise | verdict | measured |
|---|---|---|
| P1: 275 all-time rated games vs them | **CONFIRMED** | 275 rows in `join.tsv` with `opp == "team lazy"` |
| P1: v246 19/40, v247 2/5, v253 20/40 | **CONFIRMED exactly** | v253 by match: 5/5, 2/5, 4/5, 1/5, 2/5, 4/5, 1/5, 1/5 = 20/40 |
| P1: v253 36/40 core_destroyed, median turns 274 | **CONFIRMED exactly** | 36 `core_destroyed`, 4 `titanium_collected` at r1000; median turns **274.0** |
| P2: share 50.0% over n=100 "modern" games | **NOT RE-DERIVABLE, and the 50.0% is a coincidence of two cells** | v246 47.5% and v253 50.0% pool to **39/80 = 48.8%**; whatever `move_miner` calls "modern" I could not reconstruct, so P2 stays UNVERIFIED as briefed |
| P3: 07:32Z v167 4-1, 14:12Z v168 1-4, 17:32Z v168 5-0 | **CONFIRMED against the decoded tape** | `938a1ed0…` ourver 167 → 4/5 · `cecbe8c8…` ourver 168 → 1/5 · `0808d065…` ourver 168 → 5/5 |

**Interval on the headline share, DEFF-corrected.**
Cluster enumeration (per the `CLAUDE.md` procedure, performed in writing rather
than asserted):
1. Clusters present: **MATCH** and **OPPONENT**.
2. **OPPONENT cluster is DEAD by construction** — this study's stratum is a
   single opponent, so a stratum cannot hold two opponents. **MATCH cluster is
   LIVE** for any pooled/seat cut: **MEASURED, every match contributes exactly
   5 games** to the pool.
3. Surviving DEFF = the rated **within-opponent** constant, **1.366**.

> **39/80 = 48.8%, 95% CI [35.9, 61.6]** (DEFF 1.366).
> v253 alone 20/40 = 50.0%, CI [31.9, 68.1]. v246 alone 19/40 = 47.5%,
> CI [29.4, 65.6]. **The two cells' CIs overlap almost entirely — nothing in
> the outcome data distinguishes their two versions.**

---

## 2. Q1 — WHAT SPLITS THE COIN FLIP: **THE MAP, and it is not close**

### 2.1 The discriminator

**MEASURED, pooled v246+v253, n=80 games, rated ladder, us-only archive:**

| map | our games | our wins | share | median turns |
|---|---|---|---|---|
| icefloe | 8 | 8 | **100%** | 236 |
| drakkarfjord | 5 | 5 | **100%** | 229 |
| yulerune | 2 | 2 | 100% | 174 |
| glacierkeep | 7 | 6 | 85.7% | 351 |
| drumlin | 7 | 6 | 85.7% | 297 |
| antler | 8 | 4 | 50.0% | 308 |
| midgard | 7 | 3 | 42.9% | 208 |
| frostgate | 5 | 2 | 40.0% | 287 |
| valkyrie | 3 | 1 | 33.3% | 446 |
| royale | 7 | 1 | 14.3% | 205 |
| nordkap | 8 | 1 | 12.5% | 380 |
| ragnarok | 4 | 0 | **0%** | 108 |
| fjordgate | 4 | 0 | **0%** | 225 |
| archipelago | 3 | 0 | 0% | 275 |
| auroraveil | 2 | 0 | 0% | 180 |

Grouped: **icefloe/drakkarfjord/yulerune/glacierkeep/drumlin = 27/29 (93.1%,
CI [83.9, 100.0])** against **nordkap/fjordgate/ragnarok/archipelago/
auroraveil/royale = 2/28 (7.1%, CI [0.0, 16.7])**. Per-map cells take
**DEFF = 1.0**: **MEASURED, 0 of 80 (match, map) cells hold more than one
game** — a 5-game match uses 5 different maps — so the match cluster dies and
the opponent cluster is already dead.

### 2.2 The control that could have come out the other way — and did not

A map ranking derived from the games it is scored on is circular. So it was
**cross-validated across their two versions**, both directions:

> **MEASURED. Train on v246 (maps with n≥2 and share ≥0.6 = GOOD, ≤0.4 = BAD),
> test on v253:** GOOD **13/17 = 76.5%** [56.3, 96.6] · BAD **4/15 = 26.7%**
> [4.3, 49.0]. Difference **49.8pp, 95% half-width 34.6pp → EXCLUDES 0.**
> **Reverse (train v253, test v246):** GOOD **14/17 = 82.4%** · BAD
> **3/14 = 21.4%**.

Out-of-sample in both directions, with the split learned on a disjoint set of
games against a different opponent version. This is not curve-fitting.

### 2.3 The stronger statement: games are near-DETERMINISTIC in (map, seat)

**MEASURED.** Of the **23 (map, seat) cells holding ≥2 games** in the pooled
80, **16 (69.6%) are unanimous in outcome**, covering 50 of 74 games in those
cells.

**Control (permutation, 2000 shuffles of the map label with seat held fixed):**
expected unanimity **29.6%**, p95 **44.0%**. **Observed 69.6%,
p(null ≥ observed) = 0.0000.** The control runs the other way when the map
label is destroyed, which is what makes the observed value mean something.

Three cells are identical down to the **turn count**, across different versions
on both sides:

* **midgard, seat A: 3/3 WINS at turn 91, 91, 91.**
  `8555c930-…_game_4` (their v246 / our v162) ·
  `0808d065-…_game_1` (their v253 / our v168) ·
  `938a1ed0-…_game_3` (their v253 / our v167).
  Three different version pairs, one identical kill round.
* **ragnarok, seat B: 3/3 LOSSES at turn 108, 108, 108.**
  `20d427cd-…_game_2` · `63efdec5-…_game_3` · `6ef9e9a7-…_game_1`
  (all their v246 / our v162).
* **midgard, seat B: 0/4** (turns 208, 508, 638, 1000) — the same map, the
  other seat, and the outcome flips completely.

### 2.4 Seat: a real marginal that mostly dissolves inside the map

**MEASURED:** seat A **27/45 = 60.0%** [43.3, 76.7] · seat B **12/35 = 34.3%**
[15.9, 52.7] (DEFF 1.366 — seat is constant within a match, 16 matches).
The v253 cell alone is starker: seat A 16/25 (64.0%) vs seat B 4/15 (26.7%).

**But conditioned on the v246-trained map class it largely goes away:**

| map class | seat A | seat B |
|---|---|---|
| GOOD | 20/23 (87.0%) | 11/14 (78.6%) |
| BAD | 3/18 (16.7%) | 1/15 (6.7%) |
| MID (midgard, valkyrie) | 4/4 | 0/6 |

⇒ **The seat marginal is mostly an unlucky map draw on the seat-B matches, with
one genuine residue: midgard, where seat decides the game outright (A 3/3 win
at r91, B 0/4).** Report seat as a *map-conditional* effect, not a global one.

### 2.5 So what actually happened on 2026-08-20?

**MEASURED.** The three same-day matches drew:

* 07:32Z, our v167, seat A → antler(L), icefloe(W), **midgard(W, r91)**,
  frostgate(W), drumlin(W) = 4-1. Four GOOD/MID-favourable maps.
* 14:12Z, our v168, seat B → frostgate(L), nordkap(L), **midgard(L)**,
  valkyrie(L), glacierkeep(W) = 1-4. Four BAD/seat-B-adverse maps.
* 17:32Z, our v168, seat A → **midgard(W, r91)**, icefloe(W), valkyrie(W),
  drakkarfjord(W), antler(W) = 5-0.

**The "wild inter-match swing on the same day, same their-version" is the map
and seat draw, not bot variance.** Same our-version v168 produced 1-4 and 5-0;
the 1-4 was seat B on a bad slate, the 5-0 was seat A on a good one.

**⇒ ANSWER TO Q1.** Nothing "game-level decides early" in the sense of a race
being run and won. **The outcome is very largely pre-committed by (map, seat)
before either bot does anything interesting**, and the divergence round is
correspondingly all over the place (pooled median 255 turns, quartiles
172–384; v253 alone median 274). The right
mental model for this cell is *a bag of 15 maps × 2 seats, ~30 near-fixed
outcomes, and each match draws 5 of them.* That is what makes a 5-0 and a 1-4
sit on the same day with an unchanged bot on both sides.

⚠ **Scope limit, stated inline:** these are OUR archived rated games only, at
our v162–v168. The map classification is a property of *this matchup*, not of
the maps in general, and it will move when either tree changes materially.

---

## 3. Q2 — THEIR MECHANISM

### 3.1 It is one channel, and it is the sentinel

**MEASURED, pooled 80 games, from the self-checking damage ledger:**

* **Damage into OUR core: 68,721 HP total (859/game) — sentinel 66,978 (97.5%),
  gunner 1,743 (2.5%), builder attacks 0.**
* **Damage into THEIR core: 42,696 HP — sentinel 42,696 (100.0%).**

Builder melee contributes **zero** core damage on either side despite
**MEASURED** 163.1 builder-attack events per game on their side and 73.7 on
ours (`build_agg` metric `batk`, 80 games) — those are spent on buildings, not
cores. Turret shots per game (metric `shot`): **THEM 167.1, US 55.8** — they
fire 3× as much and 97.5% of what lands on our core comes from 2.3
sentinels/game.
This confirms the v222-era profile's fact 2 at 8× the sample: **the kill is one
mechanism, a sentinel.**

### 3.2 Where they put it — point-blank, and it has not moved

**MEASURED**, turret builds with geometry (`builds.tsv`, pooled 80 games):

| side | kind | n | per game | median build round | FORWARD share | median d²(enemy core) |
|---|---|---|---|---|---|---|
| THEM | sentinel | 185 | 2.31 | r84 | **94%** | **5** |
| THEM | gunner | 227 | 2.84 | r68 | 15% | 122 |
| US | sentinel | 300 | 3.75 | r114 | 73% | **17** |
| US | gunner | 44 | 0.55 | r42 | 0% | 163 |
| US | launcher | 289 | 3.61 | r5 | 54% | 100 |

**Their sentinels sit at median d² = 5 from our core — touching it. Ours sit at
d² = 17 and land 30 rounds later.** Their gunners are a *home* weapon (15%
forward, median d² 122); their sentinel is the *away* weapon. This is the same
shape the v222 profile HP-verified at 12/12, now confirmed at v246/v253 with
185 sentinel builds.

**Worked anchor — `cecbe8c8-404f-484c-8e41-29959ba3346d_game_1`** (their v253,
our v168, seat B, 20×20, we lose at r153): their sentinel `#134` is built
**r75 at (16,11), d² = 4 from our core at (16,9)**, and then fires **18 damage
every second round from r92 to r152 unopposed** — 30 shots, 540 HP, the whole
core. Our own core took its first damage at r76 from that one building.
Second anchor — `7e716e11-a536-4689-8400-c81ac2bb990c_game_1` (nordkap, seat A,
we lose at r801): same class, sentinel-only channel.

### 3.3 What they fail to stop in our wins

**MEASURED, conditioned on result (pooled 80):**

* **Our wins (n=39):** damage into their core 27,972 HP (717/game); damage into
  ours 11,340 (291/game).
* **Our losses (n=41):** damage into their core 14,724 (359/game); into ours
  **57,381 (1,400/game)** — i.e. in a loss their sentinel keeps firing long
  after the core is dead-in-fact, and in a win we simply out-deliver a
  sentinel-vs-sentinel exchange.

They stop essentially **nothing** structurally: **MEASURED, they built 0
launchers and 0 splitters in 80/80 games**, so there is no displacement answer
to our raiders and no belt redundancy. Their answer to a forward turret is a
gunner, whose r²=13 is obstacle-blocked (QUEUE #41's premise), and it is
reactive.

### 3.4 Map-conditionality of their bot

**MEASURED.** Their build profile is **not** obviously map-switched — first
conveyor r7, first harvester r4.5–5, 4 builder spawns, 16–17 conveyors, 3–4
harvesters on both versions — but the *outcome* is violently map-conditional
(§2.1), and their siege timing does move with map size: their first
forward-in-range sentinel lands median r33 on the maps we win and r39 on those
we lose, while on nordkap (30×30) it slips to r104–135. **The honest reading is
that map size delays everybody, and the map effect in §2.1 is about geometry
(where the ore and the approach lanes are), not about a map table in their
bot.** I could not separate those two with the data available; flagged as
**open**, not resolved.

### 3.5 ⛔ TWO MECHANISMS REFUTED — RETAINED SO NOBODY RE-DERIVES THEM

**REFUTED 1 — "first blood on a core predicts the win." It does not; if
anything it runs backwards.**
**MEASURED, pooled 80:** games where WE damage their core first → **15/36
(41.7%) wins**; games where THEY damage ours first → **24/43 (55.8%) wins**.
Landing the first core hit is *anti*-correlated with winning here. Do not build
a plank or a bar on first-blood.

**REFUTED 2 — "our early forward sentinel is what loses these games." The
marginal says so loudly and the within-map control kills it.**
**MEASURED marginal:** our first FORWARD sentinel in range of their core lands
median **r104 in our wins** vs **r12 in our losses** — a 92-round gap that
looks like a smoking gun.
**Control (condition on map, since map is the dominant cause per §2):** of the
8 maps holding both outcomes, our winning games plant **later on 4 and earlier
on 4** — frostgate wins r5 vs losses r13, midgard r12 vs r12, drumlin r87 vs
r88. **The marginal is a map artefact: on the small/adjacent maps we can reach
their core by r12 and those are disproportionately the maps we lose.** The
early-plant story does not survive its own control and must not be quoted.

---

## 4. Q4 — VERSION CHURN: **POOL v246 WITH v253**

`league_matches.tsv` is the authority for their timeline and shows the churn the
brief describes (v239 → v253 inside the recent window). The question is whether
v246 and v253 are *behaviourally* the same bot.

**Test.** Build an 11-dimensional their-side profile per game from
`corpus/events.tsv` — first-build round and total count for conveyor,
harvester, gunner, sentinel, barrier, plus builder-bot spawns — take the median
profile per version group, and measure a scale-normalised L1 distance.
**Confound control: restrict both groups to games played against OUR v162**
(v246 n=35, v253 n=15), so our own tree is held fixed.

**Null:** randomly re-split the pooled v246+v253@v162 games into groups of the
same sizes, 3,000 times. **Positive controls:** their v230 (n=40) and v226
(n=25), versions far away in their history, measured against the same null.

> **MEASURED.**
> `d(v246@162, v253@162) = 0.115`. Null median 0.144, p95 0.282.
> **p(null ≥ observed) = 0.690 → INDISTINGUISHABLE.**
> **Control `d(v230, v253@162) = 0.395`, p = 0.0037 → DIFFERENT.**
> **Control `d(v226, v253@162) = 0.433`, p = 0.0017 → DIFFERENT.**

The instrument can and does return "different" — on two other versions of the
same opponent, against the same null. It returns "same" for v246 vs v253.

**Corroborating, and independent of that metric:** the three midgard/seat-A
games at identical turn 91 span **their v246 and their v253** (and our v162,
v167, v168). A version bump that changed behaviour could not leave a 91-round
scripted kill byte-identical.

**What did change, honestly reported (medians, their side, 40 vs 40):** first
gunner r28 → r22.5 · sentinels per game 1 → 2 · first barrier r36 → r42 ·
harvesters 3 → 4. Small, same-direction-as-noise, and inside the null.

> ### ⇒ **VERDICT: POOL. The study's n doubles to 80 games / 16 matches,
> 39/80 = 48.8% [35.9, 61.6].** Their v247 (n=5) is left out as too thin to
> place either way.

**Caveat with a subject:** the equivalence is measured on *build timings and
counts*, which is what `events.tsv` carries. A change in, say, targeting
priority that leaves the build script alone would not show up. The claim is
"same opening/economic script", not "identical binary".

---

## 5. Q3 — PIECES

*(Every piece was grepped against `QUEUE.md` and against the read-only control
tree `bots/_v488beltbreak2/` before being written. Rows **#40, #41, #42, #45,
#47, #51** already exist off `OPP-team-lazy-profile-2026-08-13.md` (their v222
era). Where a piece re-confirms one of those it is marked **CONFIRMS #n at
v246/v253 — evidence, not a new row**, so the queue is not duplicated. Only
P1 and P6 are candidates for new rows, and P6 is norms-blocked.)*

### P1 — **THE MAP IS THE MATCHUP: 27/29 on five maps, 2/28 on six others** *(candidate NEW row)*
**MEASURED**, §2.1–2.3, cross-validated across their versions in both
directions (76.5% vs 26.7% out-of-sample, difference excludes 0).
**Anchors (≥2, file + round):**
`7e716e11-a536-4689-8400-c81ac2bb990c_game_1` — nordkap, seat A, loss at r801,
median damage into their core across the BAD group is 162 HP of 500 ·
`20d427cd-…_game_2`, `63efdec5-…_game_3`, `6ef9e9a7-…_game_1` — ragnarok,
seat B, three losses at **turn 108 exactly** · against
`0808d065-…_game_1`, `938a1ed0-…_game_3`, `8555c930-…_game_4` — midgard,
seat A, three wins at **turn 91 exactly**, spanning both their versions and
three of ours.
**Control that could have run the other way:** the 2000-shuffle permutation of
the map label (observed cell-unanimity 69.6% vs null 29.6%, p = 0.0000), and
**a map-SIZE explanation, which is REFUTED** — by area, 900 = 57.7%,
400 = 54.2%, 625 = 85.7%, 676 = 0%, 520 = 12.5%, 100 = 0%. Size does not
order the outcome; specific maps do.
**Sketch vs doctrine (<r300 kill).** The GOOD group already plays the
programme: **62% of GOOD-map games are a core kill by us at ≤r300**, against
**4% on the BAD group** and 31.2% pooled. The BAD group is not a slow win, it
is a structural loss (median 900 HP into our core vs 162 into theirs). A
per-map arm is a *supported* extension point rather than new machinery: the
tree already carries a map-fingerprint table at
`bots/_v488beltbreak2/doctrine.py:1159-1168` keyed on
`(w, h, coreAx, coreAy, coreBx, coreBy)` plus a tile digest.
**⚠ Before admitting, grep QUEUE #62's "map-blindness half" and
`docs/research/OPP-SEGMENT-MAP-2026-08-14.md`** — a map-segment row may already
own part of this ground; I checked that no row targets *opponent-conditioned*
per-map behaviour, but the general map-blindness ground is claimed.

### P2 — **POINT-BLANK SENTINEL, CONFIRMED AT 8× THE SAMPLE — with one of #40's sub-premises DEAD**
**CONFIRMS #40 at v246/v253 — evidence, not a new row.**
**MEASURED:** 185 of their sentinels over 80 games, **94% FORWARD, median
d² = 5 from our core, median build r84**; sentinel is **97.5% of all damage
that reaches our core** and builder melee is **0%**. Their gunners are a home
weapon (15% forward, median d² 122). #40's grep still holds against the
current tree: `raid.py:112-122` derives `raid_seats` from the **enemy**
footprint (`heal_seats(E, …)`) and `LOKI_BARRIER_SEAL_ON` (`doctrine.py:1227`)
seals **their** ring — **there is still no barrier ring around OUR own core.**
**Anchors:** `cecbe8c8-…_game_1` — their sentinel `#134` built **r75 at (16,11),
d² = 4** from our core at (16,9), fires 18 dmg every 2 rounds **r92→r152**
unopposed, 540 HP, kills us at r153 · `7e716e11-…_game_1` — same channel,
sentinel-only, r801.
⛔ **REFUTED SUB-PREMISE, RETAINED: "they rebuild the siege turret on IDENTICAL
tiles" is NOT true at v246/v253.** **MEASURED:** 104 of their turret builds at
d² ≤ 8 from our core sit on **93 distinct tiles = 1.12 builds/tile**, and
**66 of 68 games have a maximum of ONE build per tile** (one game reaches 11).
**Control: our own builds on THEIR ring run 1.21 builds/tile — we repeat MORE
than they do**, so the instrument is not simply reporting "nobody repeats".
⇒ **#40 must be justified as denying the FIRST plant, not as farming a rebuild
loop.** The v222-era "identical tile ×5" observation has not survived their
churn.

### P3 — **THE CORE-TANK IS STILL THERE BUT THINNER**
**CONFIRMS #42's premise at v246/v253 — evidence, not a new row.**
**MEASURED:** **80% of their heal-HP lands on their own core** (22,962 HP
healed onto it across 80 games; was 92.3% of heal *events* at v222), but total
volume is only **52 heal events/game against our 182**. Our core absorbs 48,693
HP of healing over the same games — **we are now the bigger healer by 3.4×**.
⇒ #42's "beat the core-tank with simultaneous volume" arithmetic is *easier*
than the v222 profile implies: 138 HP median of core healing per game is well
under one sentinel's sustained 9 HP/round.

### P4 — **OUR FORWARD TURRETS ARE THE FRAGILE ONES, BY A FACTOR OF TWO**
**CONFIRMS #41 at v246/v253 and UPDATES ITS BASELINE — evidence, not a new row.**
**MEASURED**, forward turrets built within sentinel range of the enemy core
(`side == FORWARD`, `d2_enemy ≤ 32`, launchers excluded), death matched by
(team, kind, tile, round ≥ build):
**US: 206 built, 128 killed (62%), median life of the killed 15 rounds.**
**THEM: 171 built, 71 killed (42%), median life 31 rounds.**
The v222 profile's baseline was 10 rounds; it is **15** now, and the
*asymmetry* (62% vs 42%) is the sharper statement — it is the control, because
the same instrument on their turrets returns a materially different number.
**Anchors:** `cecbe8c8-…_game_1` — our sentinel at (8,9) built **r5, dead
r13**; replacement at (5,7) built **r13, dead r26**; their sentinel built r75
survives to the end · `7e716e11-…_game_1` — same pattern on nordkap.
**Sketch:** #41's proposal (site at d² 14–32, barrier the adjacent tiles) is
untouched in the current tree — `_try_forward_sentinel`
(`bots/_v488beltbreak2/raid.py:684`) still has **no minimum stand-off and no
adjacent-tile denial**.

### P5 — **AN UNCONTESTED KIDNAP SURFACE THAT WE USE 30 TIMES IN 80 GAMES**
**DEMAND-SIDE EVIDENCE FOR #47/#45/#51 vs a named opponent — not a new row.**
**MEASURED:** team lazy built **0 launchers and 0 splitters in 80 of 80 games**
⇒ (a) nothing in the field displaces our builders in this matchup, and (b) they
have **no belt redundancy**. Meanwhile `throws.tsv` over the same 80 games:
**366 INSERT + 83 RETREAT of our own bots, and only 30 EXILE of theirs, present
in 19 of 80 games.**
**Why it matters here specifically:** their *entire* kill mechanism is one
builder walking to our core ring and planting a sentinel (P2) — so the eviction
target is **identified by construction**, which is exactly the trigger #47 asks
for ("build the launcher on APPROACH DETECTION"). The current tree's EXILE
(`raid.py:1241-1271`) throws **whichever enemy builder happens to be adjacent
to a launcher**, with no role selection — #51's finding, re-confirmed against
this opponent.
**Anchors:** `cecbe8c8-…_game_1` r2 — our only throw of the game is an INSERT
of our **own** bot (15,9)→(9,9) while their planter walks in unopposed and
kills us at r153 · across the BAD-map group (28 games) our median EXILE count
is **0**.

### P6 — **CPU HEADROOM: THE v222 SELF-AUDIT HAS REVERSED, AND THEIRS SCALES WITH BOARD DENSITY** *(⛔ NORMS-BLOCKED, measurement only)*
**MEASURED** (`econ.tsv` `cpu_max_us`, per file × team × band, 80 games):
**THEM p50 3,584 · p99 8,159 · max 8,315 of a 10,000 µs budget.
US p50 1,062 · p99 2,960 · max 2,996. TLE'd turns: 0 on both sides.**
The v222 profile's fact 7 read *"they run cool (max 6,701); **WE** sit closer to
the TLE ceiling"* — **that is now false in both halves**: they have risen to 83%
of budget and we have fallen to 30%.
**And theirs scales with how much is on the board.** By tercile of total builds
in the game, their per-game `cpu_max` median runs **4,028 → 4,771 → 5,507**
(n = 26/27/27), peaking at 8,315 on 25×25.
⛔ **THIS IS A MEASUREMENT AND A HELD LEAD, NOT A PLANK.**
`docs/research/SIX-ROADS-STATUS-2026-08-13.md` is explicit that CPU-timeout
**induction is HELD ON NORMS pending Magnus's question to the organisers**, and
that measuring headroom is not inducing exhaustion. Do not merge the two. Bank
the number; the road stays where that file put it.

### P7 — **⛔ THREE ADJACENT QUEUE ROWS DO NOT APPLY TO THIS OPPONENT — checked, so nobody spends a leg finding out**

**#97 (Flotte-class builder-cull — "hard builder cap that is never replaced").
PRECONDITION FAILS. MEASURED:** their builder-spawn count per game is
**4 in 55 of 80 games**, but **>4 in 25 of 80** (5:7, 6:6, 7:6, 8:2, 9:2, 14:1,
53:1), and **114 of their spawns across the 80 games land after r10.**
Replacement test: of the **40 games in which ≥1 of their builders died, 25
(62%) saw a later spawn** — against a **control on our own side of 36 of 56
(64%)**, i.e. statistically the same behaviour. Flotte's signature was
0 replacements in 8 games; team lazy replaces about as readily as we do.
**They are not a cull target.** *(Their builders do die: 162 deaths across 80
games, in 40 of 80 — the kill is available, it just is not permanent.)*

**#59 (don't get farmed by the enemy launcher's pickup envelope). THREAT ABSENT
HERE. MEASURED: 0 enemy launchers in 80 of 80 games**, and `throws.tsv` records
**0 throws by their side.** #59 remains live against the field; it buys nothing
in this cell.

**#79 (plant-and-guard infiltrator, unkillable vs teams that build no turret).
PRECONDITION FAILS. MEASURED:** they build **2.84 gunners + 2.31 sentinels per
game** (80 games) and their gunners are specifically a home weapon (85% HOME,
median d² 122 from our core). A dormant infiltrator has a counter here.

### P8 — **⛔ CLOSED ROAD, RETAINED: there is no ammo-starvation lever here**
**MEASURED:** they convert a median **816 Ti/game into ammunition** against our
331. They are ammo-rich all game, and per `CLAUDE.md`'s guard-matrix sweep we
**cannot drain enemy ammo** in any case (`can_fire` returning true at 0 ammo is
a hazard to the *owner* of the turret, not a lever on them). Recorded so nobody
re-derives it from the 816.

---

## 6. Q5 — TARGET PRICING

**All figures MEASURED off `corpus/league_matches.tsv`, newest row for each
team 2026-08-20T18:52:59.748Z (the same match), so both ratings share one
clock.**

**Us (OpenSverige) 1846.2 at our v168 · team lazy 1787.3 at their v253 · gap
−58.9 (they are BELOW us).** Ladder pays `32 × (S − E)` with `S = games won / 5`
(`CLAUDE.md`, verified exactly), so at this gap `E = 0.584`:

| result | pays |
|---|---|
| 5-0 | **+13.32** |
| 4-1 | +6.92 |
| 3-2 | +0.52 |
| 2-3 | −5.88 |
| 1-4 | −12.28 |
| 0-5 | −18.68 |
| **our measured 48.8% share** | **−3.08 per match** |

> **The cell is currently a NET LOSS. Break-even is a 58.4% game share and we
> sit at 48.8% [35.9, 61.6].** The brief's *"a 5-0 pays +13.17"* is right to
> within rounding (+13.32 on the 18:52Z ratings); what it omits is that
> **anything below 3-2 costs us**, and 10 of our 16 archived matches against
> them were 2-3 or worse.

**Risk profile, MEASURED, our 16 pooled matches (game-wins per match):**
`5, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1`.
**Our 5-0s: 1. Their 5-0s: 0. Our 4-1s: 2. Their 4-1s: 4.** The tail is
asymmetric *against* us — they take 4-of-5 twice as often as we do — and the
mode is 2-3, i.e. −5.88.

**What the map fact does to this price, and it is the whole paragraph's point.**
Break-even needs **+9.6pp = ~7.7 more games of 80**. The BAD-map group is
**28 games at 2/28**; lifting that group alone from 7% to ~30% supplies ~6.4 of
those games, and to ~45% supplies ~10.6. **Everything about whether this
opponent is worth targeting lives in six maps we currently do not win — not in
their bot, which is 48.8% against us in aggregate and unchanged since v246.**

**Churn context for the pricing:** `league_matches.tsv` shows v246 live
2026-08-18T16:32Z, v247 at 17:52Z, **rolled back to v246 at 18:12Z**, then v253
from 2026-08-19T22:32Z — so v247 was a 20-minute reverted ship (which is also
why its 2/5 cell is safely excluded), and **v253 is v246 plus one batch.** They
remain a constant shipper, so this cell's rating gap and their version are both
short-lived facts; the map structure is the durable half.

---

## 7. Ledger row

```
2026-08-20	team lazy	253	80	docs/research/REPLAY-STUDY-teamlazy-v253-2026-08-20.md
```

*(games_covered = 80 — the 40 v253 games plus the 40 v246 games that §4 shows
are the same bot. The 5 v247 games are decoded but excluded.)*
