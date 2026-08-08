# PLAY-THE-PLAYERS FEASIBILITY — two parked plays, priced or killed (2026-08-08)

**Version-stamp:** archive as of 2026-08-08 ~13:20 CEST. Live **v77 "Eir 9"**. CAD
currently oscillating **{107, 117}**; Ouroboros **v8**, stable all window.
**Consumes:** `exploit-queue-brief-2026-08-08.md` §B (play-the-players supplement),
`cad-probe-refreeze-spec-2026-08-08.md` (E1/P1), `ouro-probe-refreeze-spec-2026-08-08.md` §6,
`ouroboros-v65-era-reverify-2026-08-07.md`, the ray-coverage law
(`kcm-win-c1-validation`, `kcm-wild-establishment-rates`, `v72-bleed-cad-family`).

**Provenance.** Read-only. No games run, nothing downloaded, no bot file touched.
85 CAD games + 50 Ouroboros games decoded from `replay_archive/` with
`docs/research/2026-08-07-fanout/toolkit/replay_lib.py` under `.venv/bin/python`.
Scratch scripts (not committed):
`…/scratchpad/ptp_feas/{q1_extract,q1_dist,q1_cover,q1_cover2,q1_kill,q1_expose,q2_ouro,q2_an,q2_an2,q2_cover}.py`.

---

## VERDICT LINES

> **Q1 — CAD answer-band coverability: NOT COVERABLE by a static rule.** The
> best single pre-placed cover turret covers **20.5%** of the plants that
> actually kill our siege turrets (leave-one-match-out CV on v117, n=122;
> in-sample best 27.0%, held-out across eras 18–21%). The unconstrained
> ceiling — ignoring buildability — is only 24–28%, so the limit is the
> distribution, not the terrain: CAD's kill-plants are spread over the whole
> 20-tile aligned star at d²≤13 and one ray reaches at most 5 of them.
> **Reaching 50% needs 5 cover turrets.** Kill the pre-coverage plank.
> **But the same corpus produced a better, free play (§1.5): 53% of the
> turrets that kill our siege turrets were ALREADY ON THE BOARD, AIMED, at the
> moment we planted.** A zero-Ti pre-plant predicate — *"is this tile on a live
> enemy turret's ray, with that turret already facing it?"* — flags **25% of our
> near-core plants**; those die **87%** of the time with a median life of
> **5 rounds** and 3 shots, against **23 rounds / 13 shots** for unflagged
> plants; **68 of 69** flagged plants had a clean alternative tile in the same
> band (median 12 free of 26). Holds in 14/15 matches and 4/5 opponents.

> **Q2 — Ouroboros steering stability: THE PRECONDITION IS UNTESTABLE FROM THE
> ARCHIVE — n=0.** The archive contains **zero** replicates of a fixed our-opening
> on a fixed (map, seat): 50 games, 25 (map, seat) cells, and **every game in a
> cell has a distinct our-opening signature** (one Bo5 per our-version, one game
> per map). f(our-opening) → their-first-gunner therefore cannot be checked for
> reproducibility on any map. **INSUFFICIENT DATA on all 25 cells.**
> What the corpus does say cuts *against* the play's value: on **6 of 16** cells
> with n≥2 Ouro's first-gunner tile is **identical across 2–4 completely
> different opponents/openings** (including SmartFridge v35 vs our v65), and in
> **7 of 16** cells its whole r0–r11 build queue is byte-identical across
> opponents — i.e. large parts of the opening are opponent-INVARIANT and not
> steerable at all. **No map qualifies for a Loki probe on present evidence.**
> The cheap replacement (§2.5): on the 4–5 cells where the first-gunner tile is
> map-determined *and* timing-feasible, pre-cover the known tile — no steering
> needed.

---

## 0. Corpus and self-checks

| | Q1 (CtrlAltDefeat) | Q2 (Ouroboros) |
|---|---|---|
| matches / games | **17 / 85** | **10 / 50** |
| era split | v107: 6 m / 30 g · v116: 2 / 10 · **v117: 9 / 45** | v8 only, 10 / 50 |
| opponents | OpenSverige v66–v76 (11 m), SmartFridge v30/v33, Lunds v42, gsxWins v18, Team 48 v16 | OpenSverige v64–v75 (9 m), SmartFridge v35 (1 m) |
| `replay_lib.check_all()` failures | **0 / 85** | **0 / 50** |
| delivery identity (`core_deliv×10 == titaniumCollected`) | pass, all team-sides | pass, all team-sides |
| ammo identity | pass, all team-sides | pass, all team-sides |
| map identification | — | **50/50** by exact (w, h, walls, ore) vs `maps/*.map26`, 0 UNKNOWN |
| seat stamp | from `meta.json` (`teamAName == TEAM_A`) | same |

Q1 objects: **280** siege turrets (ours-or-other-opponents', planted at d²≤36 of
CAD's core footprint), **202** of which died. Damage attribution into those 202:
**0 unattributed HP points** (every damage event matched a same-round Fire or
BuilderAttack by target tile + entity id — the FireTurret-after-removeEntity
ordering trap does not bite here, because attribution keys on `HpEvent.target_id`,
not on tile occupancy at event time).

Q1 v117-match list: `0803bd92` `922be463` `2b05487d` `c6383349` `3e8bd0bf`
`8704178a` `8d0e02c1` `37e6ccf9` `0ae5da15` (one more than the refreeze spec's 8 —
`0ae5da15`, our v75, landed 09:06Z).

---

## 1. Q1 — CAD ANSWER-BAND COVERABILITY

### 1.1 Reconciling with the refreeze spec's E1 row

The spec's E1 numbers (100% answered, median latency 15.5 r, 76% killed, ~34%
correctly aimed) are reproduced within definitional slack:

| definition | siege n | answered | killed | latency (med) | answer aimed at the siege tile |
|---|---:|---:|---:|---:|---:|
| all eras, any CAD turret planted in-band after us | 280 | 84% | 72% | 12 | 52% |
| **v117 only** | 158 | 88% | 77% | 13 | 49% |
| **v117 vs OpenSverige** | 88 | **94%** | **78%** | 12 | 51% |
| strict (1:1 match, answer must arrive before the siege turret dies) | 280 | 51% | — | 10 | 52% |

The "aimed" share reads higher than the spec's 34% because I score the answer's
**build-time facing** against the siege tile (8-way alignment, any k), where the
spec scored a narrower notion. Direction of the finding is unchanged: **about
half of CAD's answers are pointed somewhere else.**

### 1.2 The answer-plant distribution is DIFFUSE

Offsets canonicalised into a frame where the siege→CAD-core approach direction is
rotated/reflected onto EAST (cardinal approach) or SOUTHEAST (diagonal approach) —
the 8-element D4 lattice group, so all offsets stay on-lattice.

| frame | n | distinct offsets | modal offset | modal share | top-5 cumulative |
|---|---:|---:|---|---:|---:|
| cardinal approach | 114 | 33 | (2, 0) | 7.9% | 34.2% |
| diagonal approach | 121 | 32 | (2, 2) | 11.6% | 33.1% |

d² of the answer plant from the siege turret is spread across the whole band:
d²=1 (28), 2 (33), 4 (35), 5 (35), 8 (31), 9 (22), 10 (26), 13 (23). **No offset
carries more than 12% of the mass.** Anchoring the plants on CAD's *core* instead
of on our turret is worse still (modal share 6–9%).

One real structure: **74% of answer plants land on the CAD-core side of our
siege turret** (174 "toward" vs 29 "away", 32 flank). That is a half-plane, not a
ray — it does not compress into a placement rule.

### 1.3 The KILLER plant — the economically relevant target

Covering the *first* answer is the wrong objective; covering the turret that
actually kills ours is the right one. Top-damage-source attribution over the 202
dead siege turrets:

- killer kind: **191 gunners**, 4 sentinels, 7 builder bots
- **194 / 195** turret-killers sit at **d²≤13** of the victim — the band is real
- killer d² takes only the values **{1, 2, 4, 8, 9}** (+1 outlier at 25): every
  killer is **row-, column- or diagonal-ALIGNED** with our turret, because a
  gunner must be aligned to shoot. The killer support is therefore exactly the
  **20-tile aligned star** (4 cardinals × 3 steps + 4 diagonals × 2 steps).

Canonical killer-offset distribution (n=212 with a turret killer at d²≤13):

| cardinal-approach frame (n=106) | | diagonal-approach frame (n=106) | |
|---|---:|---|---:|
| (2,−2) (1,−1) (0,−1) (1,1) | 10.4% each | (1,1) | 16.0% |
| (1,0) (2,2) | 8.5% | (2,2) | 15.1% |
| (0,1) (3,0) (2,0) | 7.5% | (0,2) | 14.2% |
| top-5 cumulative | **50.0%** | top-3 cumulative | **45.3%** |

### 1.4 COVERABILITY — the answer is no

A rule is (approach class, canonical offset **X**, canonical facing **Y**, turret
type). At deploy time X and Y are un-canonicalised by the map's approach frame.
A rule counts as covering a killer plant only if the cover tile was **buildable at
siege-plant round** (in bounds; not wall/core; no building; ≥1 orthogonally
adjacent standable tile — conveyors and splitters count as standable) **and** the
killer tile lies on the ray (gunner: 8 directions, d²≤13, LOS-blocked by any
building at answer time; sentinel: d²≤32, obstacles ignored).

| corpus | n killer-plants | best static rule (one per approach class) | frame-free single rule | greedy 5 turrets |
|---|---:|---:|---:|---:|
| all eras | 212 | 24.5% | 22.6% | 50.5% |
| **v117** | 122 | 27.0% *(in-sample)* | 25.4% | 54.9% |
| v117 vs OpenSverige | 70 | 35.7% *(in-sample, n small)* | 31.4% | 65.7% |

Honest, out-of-sample numbers:

| held-out evaluation | coverage |
|---|---:|
| fit on v107+v116 → test on v117 | **18.0%** |
| fit on v117 → test on v107+v116 | 21.1% |
| **v117 leave-one-match-out** | **20.5%** |

**Why it caps there.** The unconstrained ceiling — best possible ray in the
canonical offset plane, ignoring buildability entirely — is **24.3–28.1%**
(cardinal 24.3%, diagonal 26.1% on v117). Buildability costs only ~5 points. The
binding constraint is geometric: a sentinel ray covers **5 collinear tiles**
(cardinal) or **4** (diagonal) out of a 20-tile star, and CAD spreads its killers
across all four axes.

Every killer plant *is* coverable by some ad-hoc placement (**oracle 212/212 =
100%**) — the failure is entirely in the "one static rule" requirement.

**Cost/benefit if built anyway.** One extra sentinel (30 Ti × scale) + 10 ammo
per shot, per siege turret, buying ~20% of the counter-turret answers. At the
observed 78% kill rate on our v117-era siege plants that is roughly a 16-point
reduction in siege-turret mortality for a doubled turret bill — and the cover
sentinel itself sits inside the same d²≤36 answer envelope, so it draws its own
counter. **Recommend: do not build the pre-coverage plank.**

**Failure modes, explicitly:** (a) ~75–80% of killers land off any single ray;
(b) rules fitted on one era transfer at ~18% — the best offset moves between
v107/v116 and v117, so the table has CAD-churn decay after all; (c) gunner-only
cover is much worse (11.5% in-sample) because LOS blocking kills the ray in a
built-up near-core band; (d) the cover turret is itself a siege turret and is
answered on the same schedule.

### 1.5 THE FREE PLAY THAT FELL OUT — pre-plant ray exposure

Median latency from siege plant to killer plant is **0**: the distribution is
bimodal — **49% of killers were already on the board before we planted** (+4%
same round), 48% arrive afterwards (median +11 r). Siege turrets killed by a
**pre-existing** turret live a median of **6** rounds; those killed by a genuine
later answer live **17**.

Everything a pre-existing killer needs to be seen is inside a builder's vision
(r²=20 > the d²≤13 band). So define a zero-cost pre-plant predicate:

> **AIMED-EXPOSED(tile)** — some live enemy gunner/sentinel is 8-way aligned with
> `tile`, within its attack range (gunner d²≤13 with clear LOS, sentinel d²≤32),
> **and is already facing that way**.

| class (all 85 games) | n | died | life (med) | shots (med) | dmg (mean) | core dmg (mean) |
|---|---:|---:|---:|---:|---:|---:|
| **AIMED-EXPOSED** | 69 (25%) | **87%** | **5.0** | 3.0 | 64 | 28 |
| ray-exposed but not yet aimed | 85 | 69% | 25.0 | 12.0 | 202 | 78 |
| clean | 126 | 66% | 23.0 | 13.0 | 138 | 113 |

| v117 only | n | died | life (med) | shots (med) | dmg (mean) |
|---|---:|---:|---:|---:|---:|
| **AIMED-EXPOSED** | 36 | **92%** | **4.0** | 2.5 | 51 |
| ray-exposed, not aimed | 45 | 76% | 28.0 | 16.0 | 163 |
| clean | 77 | 71% | 24.0 | 12.0 | 123 |

v117-vs-OpenSverige aimed-exposed: **n=27, 96% died, median life 4 rounds.**

Survival curves: clean plants survive past round 8 **91%** of the time and past
round 11 **83%**; exposed plants **52% / 45%**. The published covered-turret
lifetime band (8–11 rounds) is exactly where the two classes separate.

**Not a confound.** The separation survives stratification on every plausible
alternative driver:

| stratum | AIMED-EXPOSED (n, died, life) | CLEAN (n, died, life) |
|---|---|---|
| live CAD turrets 0–2 | 22, 86%, 6.5 | 116, 74%, 20 |
| live CAD turrets 3–6 | 38, 92%, 4.0 | 72, 58%, 38 |
| d² of plant from CAD core 0–4 | 14, 79%, 4.5 | 47, 70%, 17 |
| d² 5–9 | 32, 97%, 4.0 | 89, 72%, 21 |
| d² 10–25 | 17, 76%, 7.0 | 54, 67%, 28.5 |
| plant round 0–25 | 14, 86%, 7.0 | 75, 77%, 25 |
| plant round 76–200 | 27, 89%, 4.0 | 66, 58%, 23.5 |

Per-match: aimed-exposed is shorter-lived in **14 of 15** matches with ≥2 in each
cell (exception `922be463` vs Team 48, aimed n=4). Per-opponent it holds for
OpenSverige (4.0 vs 23.0), SmartFridge (4.0 vs 15.0), Lunds (5.5 vs 35.5) and
gsxWins (11.0 vs 22.0) — i.e. it is a **generic geometry law, not a CAD read**,
which also means it needs no opponent identification.

**Feasibility of acting on it.** Of the 69 aimed-exposed plants, **68 had at
least one non-exposed alternative** empty tile in the same d²-of-enemy-core band
(±6); median **12 free tiles of 26** candidates. The re-site is one tile, not a
strategy change.

**Note the refinement that matters:** *ray-exposed but not yet aimed* is
statistically indistinguishable from clean (25.0 vs 23.0 rounds). Gating on bare
alignment would flag 55% of plants and buy nothing; gating on **alignment +
current facing** flags 25% and buys everything. CAD's `rotate()` costs 10 Ti and
a cooldown, which is presumably why the un-aimed ray is not a real threat.

### 1.6 Q1 recommendation

- **KILL** the "pre-cover the answer band with a second turret" plank (queue-brief
  §B bullet 1). Measured out-of-sample coverage 18–21%, ceiling ~26%, cost one
  extra siege-envelope turret per siege turret.
- **PROMOTE** the AIMED-EXPOSED pre-plant predicate as a candidate plank for the
  E1 / CAD-family incoming-side work. Cost: a few lines and one loop over
  `get_nearby_units()` at build-site selection; 0 Ti. Expected effect on the 25%
  of near-core plants it flags: median life 5 → 23 rounds, median shots 3 → 13,
  mean damage 64 → 138. It is opponent-agnostic and gates purely on observed
  structures, so it satisfies the queue brief's own gating rule and inherits the
  recognition refutation for free.
- Acceptance instrument if built: re-run `q1_expose.py` against post-ship archives
  and check that our aimed-exposed plant share drops from 25% toward 0 without a
  fall in total near-core plants.

---

## 2. Q2 — OUROBOROS STEERING STABILITY IN THE WILD

### 2.1 The blocking structural fact

The steering play needs `f(our-opening) → their-first-gunner (round, tile)` to be
**reproducible**: same our-opening, same map, same seat ⇒ same plant. Testing
that needs at least two games sharing all three keys.

| grouping | groups with n≥2 |
|---|---:|
| (map, our seat, **our version**) | **0** |
| (map, our seat, **our r0–r6 opening hash**) | **0** |

Cause is structural, not accidental: the ladder gives one Bo5 per our-version
against Ouroboros, and a Bo5 plays five *different* maps. Every (map, seat) cell
in the archive therefore contains at most one game per our-version — and the
r0–r6 opening signature is distinct in **all 50 games** (25 cells, 2–4 distinct
openings each, never a repeat).

**Verdict per map: INSUFFICIENT DATA — all 25 cells, n(replicates)=0.** This is
not a thin-data caveat; the reproducibility precondition has *zero* observations
of any kind. It cannot be established from the archive at any future point either,
unless a deliberate repeat (same binary, same map, same seat) is run.

### 2.2 What the corpus *can* answer: is the first gunner opponent-sensitive at all?

Cells with n≥2 games (different our-versions, different openings):

| map / our seat | n | first-gunner tiles | round spread | facings | Ouro r0–r11 queue |
|---|---:|---|---:|---:|---|
| snowflake / A | 2 | **(17,18)** | 0 | 2 | **identical** |
| fjordgate / B | 2 | **(4,6)** | 0 | 1 | diverges (build #1, r1) |
| archipelago / B | 2 | **(7,7)** | 0 | 2 | **identical** |
| atoll / A | 2 | **(12,3)** | 2 | 1 | **identical** |
| meander / A | 3 | **(11,8)** | 1 | 2 | diverges (#1, r1) |
| saga / A | 3 | **(16,16)** | **26** | 1 | **identical** |
| heart / A | 2 | (17,9) (17,10) | 0 | 1 | diverges (#3, r6) |
| hive / B | 2 | (6,16) (6,17) | 1 | 2 | **identical** |
| drumlin / B | 2 | (8,7) (10,7) | 0 | 2 | **identical** |
| eider / A | 3 | (14,12) (15,9) | 3 | 3 | diverges (#7, r6) |
| moonrise / B | 2 | (8,6) (9,3) | 3 | 2 | diverges (#3, r3) |
| atoll / B | 3 | (3,12) (4,9) | 10 | 3 | **identical** |
| drumlin / A | 2 | (14,17) (16,14) | 13 | 2 | **identical** |
| eider / B | 3 | (12,9) (13,11) (14,10) | 17 | 2 | diverges (#9, r7) |
| antler / A | 4 | (4,9) (6,10) (7,8) (7,9) | 3 | 3 | diverges (#0, r0) |
| meander / B | 4 | (8,6) (10,6) (12,6) (13,6) | 4 | 2 | diverges (#2, r2) |

- **first-gunner TILE identical across all games in the cell: 6 / 16 (38%)**
- all tiles within Manhattan 2 of each other: **9 / 16 (56%)**
- round spread ≤4: **12 / 16**; median spread 2.5
- Ouro's whole r0–r11 build queue **byte-identical across different opponents in
  7 / 16 cells** — including `archipelago/B` (SmartFridge v35 vs our v65) and
  `atoll/B` (SmartFridge v35, our v64, our v65)
- where the queue does diverge, the first differing build is at index 0–9
  (rounds r0–r7), consistent with the published r3 divergence claim, but
  **antler/A diverges at build #0 (r0)** — Ouro's very first core spawn tile
  differs, i.e. divergence begins before there is much of our opening to key on
- secondary markers: **first harvester tile identical in 13/16 cells**, first
  conveyor **14/16**. (First sentinel is vacuous: Ouro built **0 sentinels, 0
  launchers, 0 barriers in 50/50 games** — the gunner-only fingerprint holds.)

Read together: a substantial part of Ouro's opening — including the first gunner
tile on 6 cells and the whole early queue on 7 — is **invariant to who it is
playing**. That is the opposite of steerable. On the remaining cells the tile
does move, but with one observation per opening we cannot attribute the movement
to our opening rather than to any other per-game difference, and the r0
divergence on antler/A shows at least some of the movement is not
opening-explicable.

### 2.3 Reconciliation with the refreeze spec §6

Every §6 STABLE row reproduces exactly (snowflake/A r22 @(17,18); fjordgate/B r2
@(4,6); atoll/A (12,3); atoll/B (3,12); meander/A (11,8); archipelago/B r28
@(7,7) incl. the cross-opponent SmartFridge game; saga/A (16,16); hive/B ±1
tile), and every CONDITIONAL row reproduces (eider/B three tiles / 17 rounds;
eider/A; meander/B row y=6 invariant with the column moving; antler/A;
drumlin/A). This deliverable adds three things §6 did not state: the
**invariance across a different opponent is broader than the single archipelago
row** (7 cells have identical early queues), the corpus contains **no replicate
of a fixed opening**, and the STABLE/CONDITIONAL split is **anti-correlated with
steerability** — a cell being STABLE means the first gunner is *not* moved by
changing opponent, which is exactly the case where steering has nothing to grip.

### 2.4 Does the steering-table premise survive wild contact?

**Not established, and the available evidence leans negative.**

- The premise's own precondition (reproducibility) is at n=0 — no map qualifies.
- Of the 16 testable cells, 6 show a first-gunner tile that four different
  opponents/openings could not move, and 7 show an opponent-invariant early build
  queue. On those cells the steering table would be a constant function.
- Even where the tile moves, the observed spread is 1–4 tiles inside a
  neighbourhood — the lever is short. A single sentinel ray covers 5 tiles, so on
  most of those cells one could cover the *whole observed tile set* without
  steering at all (§2.5), which strictly dominates a steering table that costs
  opening variants and carries decay.

**No map is recommended for a first Loki probe.** If the lane is kept alive at
all, the cheapest way to buy the missing evidence is one deliberate replicate —
the *same* binary, on the *same* map, in the *same* seat, twice — which the
ladder will not produce for us and which a local det run could (out of scope for
this read-only pass; note it costs 2 games, not a research window).

### 2.5 The cheap replacement, if the lane must pay something

If the first-gunner tile is map-determined, pre-cover it and skip the steering
entirely. Per cell: best single sentinel ray covering the observed tile set, plus
a timing check (a builder moves cardinally at ~1 tile/round, so earliest build ≈
Manhattan(our core → anchor) + 2 rounds, compared against the earliest observed
first-gunner round).

| map / seat | tiles observed | one ray covers | anchor / facing | Manhattan from our core | earliest gunner | in time? |
|---|---|---:|---|---:|---:|---|
| archipelago / B | 1 | 1/1 | (11,11) NW | 16 | r28 | **yes** |
| atoll / A | 1 | 1/1 | (8,7) NE | 13 | r19 | **yes** |
| saga / A | 1 | 1/1 | (12,12) SE | 16 | r26 | **yes** |
| snowflake / A | 1 | 1/1 | (13,14) SE | 17 | r22 | **yes** |
| hive / B | 2 | 2/2 | (6,12) S | 24 | r42 | **yes** |
| drumlin / B | 2 | 2/2 | (13,7) W | 16 | r22 | **yes** |
| heart / A | 2 | 2/2 | (17,8) S | 11 | r9 | no |
| meander / A | 1 | 1/1 | (11,5) S | 2 | r2 | no |
| fjordgate / B | 1 | 1/1 | (5,6) W | 1 | r2 | no |
| meander / B | 4 | 3/4 | (13,6) W | 6 | r4 | no |
| antler / A · atoll / B · drumlin / A · eider / A · eider / B · moonrise / B | 2–4 | 1–2 of 2–4 | — | — | — | tiles not co-linear |

**Six cells** (archipelago/B, atoll/A, saga/A, snowflake/A, hive/B, drumlin/B)
have a single ray that covers every observed first-gunner tile *and* enough lead
time to build it. The maps where geometry is easiest (fjordgate, meander) are
exactly the maps where the gunner arrives at r2–r3 and no forward sentinel can
exist yet — the timing/geometry trade is the real constraint on this whole lane.

Caveats before anyone builds this: n=2–3 per cell; the anchors sit forward of
midfield and inherit Ouro's home-screen problem (their d>64 gunner block has a
median 179-round lifespan and 44% of its fire goes into conveyors); and the
ray-coverage law is **necessary, not sufficient** (covered → killed only 63% in
the wild KCM corpus). Treat the table as a shortlist for a det feasibility pass,
not as a plank.

---

## 3. Self-checks and what was not computed

**Parsed / formed.** Q1: 85 games, 17 matches, 280 siege-turret records, 212
killer-plant cases with a turret killer at d²≤13, 0 check failures, 0
unattributed damage into the studied turrets. Q2: 50 games, 10 matches, 25
(map, seat) cells, 16 with n≥2, 0 groups at (map, seat, opening), 0 check
failures, 50/50 maps identified.

**Cross-validation.** Q1's rule search is a fit over ~2,000 candidate rules; every
headline coverage number is reported out-of-sample (leave-one-match-out on v117,
plus cross-era holdout). The §1.5 exposure predicate is a fixed geometric test,
not fitted, and is reported per-match and per-opponent.

**Traps handled.** FireTurret-after-removeEntity: all damage attribution keys on
`HpEvent.target_id` plus same-round Fire target tile, never on tile occupancy at
event order. Conveyors/splitters treated as bot-passable (standable) but as LOS
blockers for gunner rays. Gunner rotations reconstructed from `entity_updates` so
"facing at plant time" is the facing then, not the final facing. Core footprints
are 2×2 from the NW corner; all core distances are min-over-footprint.

**Not computed.** (a) Whether a re-sited siege turret would in fact live like a
clean one — the exposure result is observational, and the causal claim needs a
det A/B, not a decode. (b) Any survival model for the cover turret itself.
(c) Ouro-side: whether the r0 divergence on antler/A is opening-keyed or genuinely
stochastic — separating those needs the same replicate the §2.1 verdict is
blocked on. (d) Launcher/throw geometry (queue-brief §C) — out of scope for this
brief.
