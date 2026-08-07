# Denial Book — Ouroboros / Orizon / Landers / Flotte opening plants

Read-only analysis, 2026-08-07. Per-(map, seat) opening-plant tables for the four
deterministic-or-near-deterministic nemesis scripts named in the brief, with a
DENIABLE/TIGHT/UNREACHABLE call per first-turret tile so a future bot can
pre-occupy it. No bot was edited, nothing was submitted, no match/challenge/
download was run. **Zero `fcode match info` calls were used** — every map was
identified by matching the replay's own decoded tile grid (walls/ore/dimensions/
core positions) against `maps/*.map26` byte-for-byte, and every team name/version
came from `replay_archive/*.meta.json`, which already carries `teamAName`/
`teamBName`/`teamAVersion`/`teamBVersion` per match. This kept the shared fcode
rate limit untouched for the other agent using it concurrently.

## 0. Method

### 0.1 Data actually used

- **Local, freshly decoded this session** (`replay_lib.py`, self-checks all
  green): 2 Ouroboros matches (10 games, 8 distinct maps) and 1 Flotte match
  (5 games, 5 distinct maps) — the only matches in the local 48-match/236-file
  `replay_archive/` whose `meta.json` names one of the four targets. **Orizon
  and Landers do not appear anywhere in the local archive** — see §6.
- **Cited, not re-decoded**: Orizon (6 games) and Landers (5 games, +1 extra)
  from `docs/research/2026-08-07-fanout/findings/thread7_landers_orizon.md`
  (replay-verified by a prior read-only pass) and one Landers cross-check from
  `thread3_kladde_v62.md` §2.2. Cross-checked against
  `docs/research/2026-08-07-fanout/meta-census.md` §2.6/§2.7/§4.1 per the
  session coordinator's steer — no contradictions found (§1–4 note the
  cross-references inline).
- Geometry toolkit: `docs/research/2026-08-07-fanout/toolkit/siege_geometry.py`
  (`GameMap`, `SeatAnalysis` — already validated in `thread6`/`wave4`, 175/175
  core-damaging plants in that prior sample fell inside its threat-set model).

### 0.2 Map identification, no fcode needed

For each decoded replay, `(width, height, walls-set, ore-set, {core_pos(0),
core_pos(1)})` was compared against every `maps/*.map26`. All 15 local games
matched **exactly one** catalog map, zero ambiguous/unknown results. This is
strictly stronger evidence than a name string from `match info` — it's the
same terrain-matching method `thread7`/`thread8`/`wave4` already validated
(byte-identical grids across seeds and series).

### 0.3 Seat convention — read this before the tables

**"Seat" below always means the NEMESIS's own seat** (A or B), matching the
brief's own example ("Flotte jackpot **seat B**"). `thread7_landers_orizon.md`
uses the **opposite** convention throughout (its "seat" column is *our* seat —
stated explicitly in its own text: "`d9a67e82` is a five-game series in which
**we** played seat B in all five games"). Every Orizon/Landers row sourced from
thread7 has been seat-**inverted** here. This was cross-validated, not assumed:
recomputing `fp_dsq` (nearest-core-footprint distance) for all **17** transcribed
thread7/thread3 tiles against the inverted seat reproduces thread7's own quoted
`d`-value **exactly, 17/17** (e.g. fjordgate `d5`, jackpot killer `d1`, meander
kladde-negative-control `d16` — full list in §2/§3). That is about as strong a
confirmation as is available without the original replays.

### 0.4 Deniability model

BFS **cardinal-only** walking distance (4-connected, matches "builder moves 1
tile/round, cardinal only") from the **defending** side's core spawn ring
(`SeatAnalysis.spawn_ring` — passable tiles adjacent to the 2×2 footprint,
within the core's `r²=8` action radius) to a tile **orthogonally adjacent** to
the plant tile (building requires an adjacent tile, not the builder's own).

```
walk_steps      = BFS distance to the nearest tile adjacent to the plant
completion_round = walk_steps + 1     # core spawns "for free" at r0 via its
                                       # action; the builder's first possible
                                       # action (move or build) is r1; the
                                       # final round is spent building, not
                                       # moving, so it is not itself a step
margin          = their_plant_round − completion_round

DENIABLE     margin >= 2   (finishes with >=1 full round of slack)
TIGHT        0 <= margin <= 1  (same-round or 1-round race; resolution order
                                 within a round is not established — treat as
                                 a coin flip, not a plan)
UNREACHABLE  margin < 0, OR no orthogonal neighbor of the tile is ever
             reachable from our spawn ring (walled off)
```

This is a best-case model (empty board, no enemy interference, builder never
misses a round) and a ±1-round band exists around the TIGHT threshold from the
r0-vs-r1 spawn-timing ambiguity noted in the brief ("r0-1"). Treat margin ≥ 2
as robust to that ambiguity; margin 0-1 as genuinely contested.

### 0.5 The reframe: literal first-turret vs. first CORE-THREATENING turret

The brief asks for "the first-turret plant specifically," and that is what
column 3 of every table below answers literally. But the data shows this is
frequently **not** the tile worth denying: for Ouroboros, **7 of 8** locally
observed "first turrets" are a **home/economy picket** near Ouroboros's own
core (`dsq_home` 2–26 tiles) that never geometrically threatens the defender's
core at all (`in_defender_threat=False`, using the same alignment+range test
`wave4` validated at 175/175 against real damage events). The actual
core-facing plant — the one that matters — comes from a **later** creep, at
`fp_dsq` inside the sentinel/gunner threat set. Flotte shows the same split on
3 of 5 maps (its opening **launcher** is a home-defense piece, not aimed at
the core; the later gunner/sentinel is). Orizon is the exception — by
construction its literal first gunner is already core-aimed (§2).

Every table below therefore carries **both** columns: the literal first
turret (what the brief asked for, with its own DENIABLE call) and, where it
differs, the first turret that actually enters the defender's threat set
(with its own call). Denying the literal-first tile still has value — it's
the earliest legal disruption to a scripted build queue that appears to be
timing-perturbable (see §1's determinism note) — but the core-threat column
is the one that stops an actual siege.

---

## 1. Ouroboros v8 — "creeping picket" (gunner-only)

**Ladder: #23, 1582 (`docs/research/2026-08-07-fanout/meta-census.md` §1).
Seat-anomalous: holds seat A in every recorded match against us** (`bab61537`
here, plus `HANDOVER.md`'s "Ouroboros is PLATFORM SEAT-LOCKED, they hold seat
A 13/13, p≈0.008" and `docs/opponents.md:1509`'s "all 15 games drew seat B"
[our seat, i.e. Ouroboros=A] — three independent confirmations). **All 8 rows
below are seat A** — this is not a sampling gap, it is the only configuration
we will ever actually face (§0's coordinator steer). Zero sentinels/launchers
built by Ouroboros in any game observed here, consistent with the brief's
"gunner-only."

| map | seat | literal 1st turret | 1st CORE-THREAT turret | n obs | deterministic? | deniable (literal)? | deniable (core-threat)? | source (nemesis v8 vs...) |
|---|---|---|---|---|---|---|---|---|
| drumlin | A | gn r22 @(8,7) **or** @(10,7) | never in either game (0/2) | **2** | round: yes (r22/r22). tile: **no** — 2 tiles apart, see note | DENIABLE (margin 3 / 5) | n/a | `22f55a05` g4 vs SmartFridge; `bab61537` g3 vs us |
| atoll | A | gn r21 @(4,9) **or** r27 @(3,12) | r257 @(11,3) / r92 @(10,7) | **2** | round: no (Δ6). tile: **no** (further apart) | DENIABLE (margin 7 / 9) | DENIABLE (margin 255 / 84) | `22f55a05` g3 vs SmartFridge; `bab61537` g4 vs us |
| eider | A | gn r12 @(12,9) | gn r50 @(16,10) | 1 | single-sample | DENIABLE (margin 6) | DENIABLE (margin 48) | `bab61537` g1 vs us |
| meander | A | gn r4 @(13,6) | gn r6 @(12,6) | 1 | single-sample | **TIGHT** (margin 1) | DENIABLE (margin 3) | `bab61537` g2 vs us |
| nordkap | A | gn r11 @(8,8) | gn r109 @(14,19) | 1 | single-sample | **TIGHT** (margin 1) | DENIABLE (margin 106) | `22f55a05` g1 vs SmartFridge |
| archipelago | A | gn r28 @(7,7) | gn r739 @(15,16) | 1 | single-sample | **TIGHT** (margin 0) | DENIABLE (margin 730) | `22f55a05` g2 vs SmartFridge |
| moonrise | A | gn r7 @(9,3) | **same tile** — literal-1st already threatens core | 1 | single-sample | DENIABLE (margin 3) | DENIABLE (margin 3) | `22f55a05` g5 vs SmartFridge |
| hive | A | gn r43 @(6,16) | gn r155 @(22,8) | 1 | single-sample | DENIABLE (margin 18) | DENIABLE (margin 152) | `bab61537` g5 vs us |

**Determinism note (drumlin/atoll, the only 2+-observation rows).** The
opening ECONOMY is byte-identical for 14-17 rounds across both independent
series (different opponents: SmartFridge and us) — same builder spawn tiles,
same conveyor/harvester tiles, same rounds, down to facing directions. Both
series then lose 1-2 builders (respawn events visible as repeated
`builder_bot` builds) at slightly different rounds — drumlin r15/16 vs r18/19,
atoll r19/20 vs r16/17 — which perturbs the subsequent build-queue timing
just enough to land the gunner on a different (but nearby) tile at
essentially the same round. **Read this as an aim-POLICY, not a fixed
coordinate**: "plant near the harvester cluster established in the first ~15
rounds, ~r20-30" is the stable invariant; the literal tile is one of a
small 2-3-tile set. Practical recommendation: **pre-build on all observed
tiles in the cluster**, not just one — both are cheap (3 Ti barrier each) and
both are DENIABLE with margin to spare.

**Discrepancy flag against the task brief's own cited numbers.** The brief
states Ouroboros's first-gunner is "meander r6@(10,7), eider r32@(14,10),
drumlin r22@(10,7)... identical across seeds AND our versions." Freshly
decoded here: **drumlin r22@(10,7) matches exactly** in one of the two
observations (the other gives r22@(8,7), see above). **Eider and meander do
not match** — this session's direct decode gives eider r12@(12,9) (not
r32@(14,10)) and meander r4@(13,6) (not r6@(10,7)); both round *and* tile
differ, not just tile. Both eider and meander here are single-sample, so this
is flagged as an open discrepancy rather than a correction — possible
explanations include the brief's source using a different opponent context
(this session's evidence above shows the exact tile/round is
opponent-perturbable) or a stale/different sample; it was not resolved with
the read-only budget available. **Do not hand-code the brief's original
eider/meander coordinates without re-verifying.**

Compressed openings (first 40 rounds, nemesis builds only; `bb`=builder_bot,
`hv`=harvester, `cv`=conveyor, `gn`=gunner; compass suffix = facing):

- **drumlin** (identical r0-r17 in both games): `r0:bb@(7,7) r1:bb@(4,7)
  r2:bb@(7,6) r3:cv@(9,8)N r4:cv@(9,6)W r5:hv@(9,9)+cv@(1,6)E r6:hv@(10,6)
  r7:hv@(1,7)+cv@(8,6)W r8:cv@(2,6)E+cv@(9,7)N r10:cv@(3,6)E r11:cv@(7,6)W
  r13:cv@(10,5)W r15:hv@(11,5) r16:cv@(9,5)W r17:cv@(4,6)E` — then diverges
  (respawn timing, see note above) before both reach `gn@(8,7)` / `gn@(10,7)`
  at r22.
- **atoll** (identical r0-r14 in both games): `r0:bb@(4,13) r1:bb@(1,16)
  r2:bb@(4,16)+hv@(1,17) r3:hv@(5,16) r4:cv@(1,16)N r5:cv@(5,15)W
  r7:cv@(7,9)W+cv@(1,15)E r8:cv@(4,15)W r9:hv@(8,9) r10:cv@(6,9)W r12:hv@(8,8)
  r14:cv@(7,8)S+cv@(5,9)S` — then diverges before reaching `gn@(4,9)` (r21) /
  `gn@(3,12)` (r27).
- **eider**: `r0:bb@(9,10) r1:bb@(6,8) r2:bb@(6,11)+cv@(6,7)S r4:hv@(11,12)+
  hv@(6,6) r5:cv@(6,8)S+cv@(4,10)E r6:hv@(12,10) r7:bb@(9,9)+cv@(6,9)E+
  hv@(4,11) r8:bb@(9,8)+hv@(11,8)+cv@(5,10)N r9:cv@(5,9)E r10:cv@(11,9)W
  r12:gn@(12,9)E`
- **meander**: `r0:bb@(12,5) r1:bb@(13,3) r2:bb@(10,2) r3:bb@(13,5)
  r4:bb@(13,4)+cv@(16,5)W+gn@(13,6)S r6:hv@(16,6)+cv@(6,2)S+gn@(12,6)S`
- **nordkap**: `r0:bb@(10,8) r1:bb@(9,5) r2:bb@(8,6) r3:hv@(10,11)+cv@(9,3)S
  r5:cv@(10,10)N+hv@(9,2)+cv@(9,4)S r6:bb@(9,8) r7:bb@(8,8)+cv@(9,5)S
  r8:cv@(10,9)N r10:cv@(10,8)N r11:gn@(8,8)SE`
- **archipelago**: `r0:bb@(7,7) r1:bb@(4,6) r2:bb@(4,4) r3:cv@(4,3)S
  r4:cv@(2,5)E r5:hv@(4,2) r6:hv@(2,6)+cv@(4,4)S r7:hv@(12,5)+cv@(3,5)E
  r8:cv@(4,5)E ... r28:gn@(7,7)SE`
- **moonrise**: `r0:bb@(7,4) r1:bb@(4,4) r2:bb@(7,4) r3:bb@(7,3)+hv@(9,5)+
  cv@(2,4)E r4:bb@(7,2)+cv@(9,4)W r5:hv@(1,4) r6:hv@(10,6)+cv@(3,4)E+
  cv@(8,4)W r7:gn@(9,3)W+gn@(8,2)SE`
- **hive**: `r0:bb@(4,19) r1:bb@(1,19) r2:bb@(4,19)+cv@(1,18)S r4:hv@(1,17)
  r5:cv@(1,19)S r6:cv@(5,14)S r7:cv@(1,20)E r8:hv@(5,13) ... r43:gn@(6,16)`

---

## 2. Orizon v34 — point-blank core battery

**Not in local archive** (§6). Table sourced entirely from
`thread7_landers_orizon.md` (6 games, replay-verified by that prior pass) plus
seat inversion per §0.3. **Corroborated, not contradicted, by
`meta-census.md` §2.6/§4.1**: the census independently classifies the "Orizon
class" (there via `team lazy v88`, its 3rd family member) with the identical
signature — gunner-only, aim distance near 0, zero sentinels/launchers/
barriers — and cites Orizon directly ("point-blank gunner core battery, six
games documented in thread7, most recent series `607ffaeb-…`"). Unlike
Ouroboros, Orizon's literal first gunner **is** core-aimed by construction
(the builder "walks straight at the enemy core from round 0" — thread7 §1) so
there is no picket/core-threat split here; both columns are the same tile
except where a later "killer" gunner creeps closer.

| map | seat | literal 1st gunner | killer (execution) gunner | deniable (1st gunner) | deniable (killer) | source |
|---|---|---|---|---|---|---|
| fjordgate | B | r1 @(5,4), fp_dsq5 | r8 @(3,6), fp_dsq9 | **TIGHT (margin 0)** — the one contested case in this whole book | DENIABLE (margin 6) | thread7 (`c106d3d2`-family, v56 our-seat A) |
| jackpot | B | r21 @(4,1), fp_dsq9 | r66 @(2,1), fp_dsq1 | DENIABLE (margin 19) | DENIABLE (margin 65) | thread7 (v56 our-seat A) |
| eider | A | r7 @(16,9), fp_dsq9 | r32 @(18,8), fp_dsq2 | DENIABLE (margin 5) | DENIABLE (margin 31) | thread7 (`a72b53f9`-family, v61 our-seat B) |
| drumlin | A | r19 @(19,14), fp_dsq16 | r79 @(19,15), fp_dsq9 | DENIABLE (margin 16) | DENIABLE (margin 77) | thread7 (v61 our-seat B) |
| snowflake | A | r21 @(19,16), fp_dsq9 | r49 @(20,16), fp_dsq9 | DENIABLE (margin 19) | DENIABLE (margin 47) | thread7 (v61 our-seat B) |
| lighthouse | A | r9 @(11,8), fp_dsq9 | r41 @(12,10), fp_dsq1 | DENIABLE (margin 7) | DENIABLE (margin 40) | thread7 (v53 our-seat B) |

**Determinism**: thread7 itself frames this as "the same mechanism every
single time, v53 → v56 → v61" (its §3 cross-version table) — i.e. verified
deterministic **in mechanism** (4 builders r0-3, never respawn, straight walk,
creeping gunner-only plants, ammo-drip conversion) across 3 of our own code
versions, though each map here is still only single-sampled at the replay
level (no repeated-seed pair exists in what thread7 downloaded, so "identical
sequences across seeds" was not independently re-confirmed by this pass —
flagging per the brief's instruction to mark what is/isn't verified).
**Creep sequence** (`fp_dsq` per successive gunner, from thread7's own table,
compressed): eider `9,16,10,2,1,5`; drumlin `16,16,9`; snowflake `9,16,9,4,5`;
jackpot `9,4,1,4,13`; fjordgate `5,5,13,13,5,9`; lighthouse
`9,9,16,20,13,1,2`. Full builder-by-builder opening was not preserved by
thread7 (it recorded turret timing, not the harvester/conveyor economy) —
this is a genuine sourcing gap, not a claim that no economy exists (thread7
§1 describes it qualitatively: 1-4 harvesters, a short conveyor stub, and on
fjordgate **zero** harvesters for 350 rounds).

**The one real problem case: Orizon fjordgate, r1@(5,4).** Margin 0 — our
fastest possible builder and Orizon's fastest possible gunner complete on the
exact same round. This is the single tightest race in the entire dataset and
should not be relied on as a guaranteed deny; treat it as "maybe," not "yes."
Every other Orizon/Ouroboros/Landers/Flotte plant observed across both local
decoding and cited sources clears with margin ≥ 1, most by a wide margin.

---

## 3. Landers v62 — patient grind (melee economy strangulation)

**Not in local archive** (§6); not classified in `meta-census.md`'s top-8/
mid-pool passes either (Landers is #17, 1680 — outside both samples). Sourced
from `thread7_landers_orizon.md` (5 games, one series, all our-seat B ⇒
**Landers seat A** after inversion) plus one independent cross-check from
`thread3_kladde_v62.md` §2.2 (Landers vs **kladde**, not us — Landers seat B
there). Thread7's own verdict: Landers is "**NO** as a frozen opening probe...
behaviour is adaptive and map-dependent" — flagging this up front, because it
means the table below is the **least** trustworthy of the four for exact
round numbers, even though the tiles hold up surprisingly well (see the
meander cross-check).

Thread7 only recorded exact **tiles** for the "killer" (execution) turret,
not the literal first turret (which it logged only as a dsq-to-core figure,
no coordinates) — so the "literal first" column is unresolved for 4 of 5
Landers/our-seat rows. It resolved for meander because of the independent
kladde-negative-control cross-check.

| map | seat | literal 1st turret | killer (execution) turret | deniable (killer)? | source |
|---|---|---|---|---|---|
| meander | A | r3, sentinel, fp_dsq16, **tile unresolved from thread7 alone** | r160 @(9,12), gunner, fp_dsq5 | DENIABLE (margin 159) | thread7 `d9a67e82`, v62 our-seat B |
| meander | **B** | r6 @(11,8), sentinel, fp_dsq16 — **independent cross-check, see below** | (Landers won this game — no execution phase needed) | DENIABLE (margin 3) | thread3 `c23600fc-79e6-477b-afde-ceb4062ca48d` g5, vs **kladde** (not us) |
| atoll | A | r20, sentinel, fp_dsq225 (their own home ring — not core-threatening at that point) | r548 @(14,7), sentinel, fp_dsq16 | DENIABLE (margin 545) | thread7 `d9a67e82` |
| nordkap | A | r9, gunner, fp_dsq37 | r332 @(11,16), gunner, fp_dsq5 | DENIABLE (margin 331) | thread7 `d9a67e82` |
| jackpot | A | r26, gunner, fp_dsq117 (not yet in threat range) | r271 @(12,14), gunner, fp_dsq4 | DENIABLE (margin 270) | thread7 `d9a67e82` |
| moonrise | A | r7, gunner, fp_dsq9 | **we won this game (r207)** — no kill turret ever completed | n/a | thread7 `d9a67e82` |

**The meander cross-check is the most interesting result in this section.**
Thread7's own `d9a67e82` series (Landers vs **us**) gives meander's literal
first turret as "r3 sentinel, fp_dsq16" with no coordinates. `thread3`
independently decoded a **different Landers match against a different
opponent** (kladde, `c23600fc` g5) on the same map and found Landers' first
turret there is a sentinel at r6 @(11,8), **fp_dsq16 — the identical
distance**, described in that document as the reason kladde's own rush was
beaten to the punch ("kladde lost the race for the rush tile"). `(11,8)` is
one of only 4 on-board lattice points that produce fp_dsq=16 from meander's
core, and the map's "cores mirrored" symmetry plus the matching mechanism
(both sources describe an immediate close-core rush, not the patient grind
Landers shows everywhere else) makes it very likely this is the same
deterministic tile reproduced against two unrelated opponents at two
different rounds (r3 vs r6) — **exactly the "policy is stable, round drifts
with opponent" pattern** already established for Ouroboros in §1. This is
offered as strong corroboration, not certainty (thread7 never published the
coordinate for its own r3 observation to compare directly).

**Practical read for Landers**: thread7's own conclusion stands — this is an
attrition opponent (7-11 growing builders melee-pecking the economy, turrets
are a late execution step, not an opening signature) more than a frozen
"plant a barrier here" target. The one map where a fast, denial-relevant
early plant reliably shows up is **meander** (both sources agree, r3-6,
fp_dsq16, DENIABLE either way). Elsewhere the actionable defense is
manpower/economy floors (thread7's own diagnosis), not a pre-round-40
barrier.

---

## 4. The Flotte Experience v35 — chip-siege

**Ladder: #7, 1880** (`meta-census.md` §1) — the only top-8 team of the four.
5 local games (one match, `73afd924-f015-4e14-baa8-4089f07f4323`, seat B
throughout, vs sporks v2), matching `meta-census.md` §2.7's own citation of
the same match id exactly. 2 more maps (jackpot, meander) cited from
`thread8_theft_prep.md`, which independently verified those two
**cross-seed and cross-version (v32→v35)** — the strongest determinism
evidence of any row in this book, though for a different match than the ones
decoded here.

| map | seat | literal 1st turret | 1st CORE-THREAT turret | deniable (literal)? | deniable (core-threat)? | n obs / deterministic? | source |
|---|---|---|---|---|---|---|---|
| jackpot | B | r0 builder@(14,13) → **r15 launcher@(11,14)** (full opening: r0 bb, r4 harvester@(14,11), r6 conveyor@(14,12)) | not independently re-verified here | not computed here (no local replay; see below) | — | **2+, cross-seed AND cross-version v33→v35** | `thread8` (`96887bee…`, `3bd204f7…`) — **not local** |
| meander | B | r7 gunner@(11,5), then plant tiles (10,5)(16,4)(10,2)(10,3) | gunner itself is core-aimed | not computed here (no local replay) | — | **2+, cross-seed**, seeds 331886149 (v32) & 1402563494 (v35) | `thread8` (`5c3899f9…`, `6e2109f0…`) — **not local** |
| eider | B | launcher r8 @(13,9) | **same tile** | DENIABLE (margin 4) | DENIABLE (margin 4) | 1, single-sample | local `73afd924` g1 |
| fjordgate | B | gunner r5 @(4,4) | **same tile** | DENIABLE (margin 4) | DENIABLE (margin 4) | 1, single-sample | local `73afd924` g2 |
| atoll | B | launcher r6 @(14,6) — home-defense, not core-aimed | gunner r37 @(7,10) | UNREACHABLE (margin −11) — moot, tile never threatened core | DENIABLE (margin 29) | 1, single-sample | local `73afd924` g3 |
| saga | B | launcher r14 @(20,14) — home-defense | sentinel r114 @(9,8) | UNREACHABLE (margin −13) — moot | DENIABLE (margin 102) | 1, single-sample | local `73afd924` g4 |
| archipelago | B | launcher r10 @(21,16) — home-defense | sentinel r113 @(10,2) | UNREACHABLE (margin −15) — moot | DENIABLE (margin 108) | 1, single-sample | local `73afd924` g5 |

**Note**: jackpot/meander deniability was **not** computed because those
tiles are cited from thread8 rather than independently decoded here — the
tiles themselves (`(14,13)/(14,11)/(14,12)/(11,14)` for jackpot;
`(11,5)/(10,5)/(16,4)/(10,2)/(10,3)` for meander) are solid (cross-version
verified), but running them through the BFS/threat-set model requires either
a replay to confirm the exact map orientation/seat pairing or a repeat of
thread8's own `match info` calls; left as a 2-line follow-up rather than
spending budget re-deriving what thread8 already nailed down. All 5 locally
decoded maps show the same **launcher-is-not-the-threat** split seen in
Ouroboros — 3 of 5 launchers are unreachable-but-irrelevant home defense,
while the real threat (a gunner or sentinel, 29-108 rounds later) is
comfortably deniable every time it was observed.

Compressed openings (local games, first 40 rounds):

- **eider**: `r0:bb@(18,8) r1:bb@(19,11) r2:bb@(21,8) r3:bb@(18,9)
  r4:hv@(16,8)+hv@(19,13) r5:hv@(21,6) r6:cv@(17,8)S+cv@(19,12)N
  r7:cv@(21,7)S r8:cv@(17,9)E+cv@(19,11)N+la@(13,9) r9:cv@(21,8)S
  r10:cv@(18,9)E+la@(14,11) r11:cv@(21,9)W+gn@(13,10)NW r15:gn@(13,9)W`
- **fjordgate**: `r0:bb@(5,5) r1:bb@(5,6) r2:bb@(6,5) r3:bb@(5,6)
  r5:gn@(4,4)NW r6:hv@(3,7) r7:gn@(4,3)W r8:cv@(4,7)E r10:cv@(5,7)E+
  gn@(4,1)SW r13:gn@(3,4)N`
- **atoll**: `r0:bb@(13,1) r1:bb@(16,1) r2:bb@(13,2) r3:bb@(13,4)+hv@(12,1)+
  hv@(16,0) r5:cv@(13,1)S+cv@(16,1)S r6:la@(14,6) r7:cv@(13,2)E+cv@(16,2)W
  ... r29:gn@(13,6)S r37:gn@(7,10)NE`
- **saga**: `r0:bb@(20,20) r1:bb@(19,20) r2:bb@(20,19) r3:bb@(17,20)
  r6:hv@(23,21) r8:cv@(22,21)W r10:cv@(21,21)N r12:cv@(21,20)N+hv@(13,19)
  r14:cv@(21,19)W+cv@(14,19)S+la@(20,14)`
- **archipelago**: `r0:bb@(21,21) r1:bb@(20,21) r2:bb@(21,18) r3:bb@(18,20)
  r4:hv@(21,23) r6:cv@(21,22)N+hv@(23,17) r8:cv@(21,21)N+cv@(22,17)W
  r10:cv@(21,17)S+la@(21,16)`

---

## 5. Ranked shortlist — 5 cheapest high-value denials

"Cheapest" = largest, most model-robust margin (all builds are a uniform 3 Ti
barrier/conveyor, so cost doesn't differentiate — safety margin does).
"High-value" = actually core-threatening (§0.5) and against a team/map
combination we face with real frequency. Ranked:

1. **Ouroboros's core-threat creep tile, any map (esp. drumlin/atoll/eider,
   the maps `HANDOVER.md` names as the live unrated-portfolio-sweep front).**
   Margins 48-730 rounds — the largest slack anywhere in this book, because
   Ouroboros's real core-threatening plant only arrives after a very long
   creep. Ouroboros is our single most institutionally-tracked nemesis
   (seat-A-locked — guaranteed configuration, not a maybe) and the team an
   active probing pass is running against **today**.
2. **Orizon, all 6 maps, literal first gunner (not a later creep — the
   literal first plant already threatens the core).** One tile stops the
   entire mechanism at its root rather than intercepting a later stage.
   Margins 5-19 rounds, DENIABLE on 5/6 maps. Orizon is the best-decoded
   exemplar of the point-blank-core-battery class, **44% of our classified
   matched-game pool** per `meta-census.md` §4 — a fix that generalizes here
   generalizes broadly. **Excludes fjordgate**, which is the one TIGHT
   (margin-0) case in the whole book and should be flagged as unreliable, not
   folded into this "cheap" bucket.
3. **Eider — the single highest cross-team convergence point.** Three of the
   four tracked nemeses (Ouroboros, Orizon, Flotte) all plant a
   core-threatening turret on eider with comfortable margins (Ouroboros 48,
   Orizon 5, Flotte 4). A defensive setup invested once on eider pays against
   three different opponent identities, not one.
4. **Flotte fjordgate (gunner, margin 4) and eider (launcher, margin 4).**
   Flotte is the only top-8 opponent (1880) in this set; `thread8_theft_prep.md`
   prices a single stolen game against a team at this rating at **+6.4 Elo**
   (game-share arithmetic, `Δ = 32×(games/5 − E)`), so a cheap, reliable
   denial against a team we rarely beat outright is disproportionately
   valuable even at modest margins.
5. **Landers meander, sentinel @(11,8), fp_dsq16, margin 3.** The
   best-corroborated Landers tile in the book (reproduced against two
   unrelated opponents — us and kladde — at the same fp_dsq), and the one map
   where Landers' usual glacially slow grind (kill rounds 242-641 elsewhere)
   turns into a fast, denial-relevant opening (r3-6) instead of a 500-round
   attrition problem no single barrier fixes.

---

## 6. Explicit gaps

**Teams entirely absent from the local archive**: Orizon and Landers have
**zero** matches in the 48-match local `replay_archive/` — every Orizon/
Landers row above is a citation, not a fresh decode, and could not be
independently re-verified this session (no replays to check against; the
brief explicitly forbids downloading more). If the archive grows (it is
described as a passive whole-ladder harvest that keeps running), re-running
§0.2's map-identification pass against new arrivals costs nothing and should
be done before the next revision of this book.

**Maps never observed, per team** (of the 15-map live pool):

| team | maps observed | maps missing |
|---|---|---|
| Ouroboros (seat A only) | eider, meander, drumlin, atoll, hive, nordkap, archipelago, moonrise (8) | antler, fjordgate, heart, jackpot, lighthouse, saga, snowflake (7) — **and seat B entirely** (see below) |
| Orizon (seat A: eider/drumlin/snowflake/lighthouse; seat B: jackpot/fjordgate) | 6 maps, both seats | antler, archipelago, atoll, heart, hive, meander, moonrise, nordkap, saga (9) |
| Landers (seat A: atoll/meander/nordkap/jackpot/moonrise; seat B: meander only) | 5-6 maps | antler, archipelago, drumlin, eider, fjordgate, heart, hive, lighthouse, saga, snowflake (10) |
| Flotte (seat B only) | eider, fjordgate, atoll, saga, archipelago, jackpot*, meander* (7, *cited) | antler, drumlin, heart, hive, lighthouse, moonrise, nordkap, snowflake (8) — **and seat A entirely** |

**Ouroboros seat B is a total gap** across every source checked (local
archive, `thread1_determinism.md`'s determinism pair, `docs/opponents.md`) —
all three independently show Ouroboros only ever at seat A against us. This
is very likely a non-issue operationally (§1's three-way confirmation that
the matchup is seat-locked), but it means "Ouroboros seat B" literally cannot
be filled in from any available source; it would require Ouroboros drawing
seat B in a real or unrated match, which the platform does not appear to do.

**Flotte seat A is unobserved** (single local match, both cited thread8
matches, are all seat B) — lower-confidence gap since Flotte is not known to
be seat-locked, just under-sampled here.

**Version freshness**: Ouroboros v8 and Orizon v34 both show long stable
windows (Orizon "unchanged v53→v56→v61" per thread7; Ouroboros confirmed
current v8 by the session coordinator). Landers v62 is a single 09:12-10:12
UTC snapshot window (`thread3_kladde_v62.md` §0) — no visibility into whether
it has since moved. **Flotte ships often** (`thread8`'s version-stability
table: 10 version changes in a 16.5h window, v27→v35, including a rollback)
— re-check its current version before trusting this table's exact numbers,
though thread8 notes the structural holes (jackpot/lighthouse loss rates)
"persist unbroken across v27-v35," so the geometry is probably robust even if
the version number has since ticked forward again.

---

## 7. Appendix — other highly-scripted teams (policy notes only, no deniability computed)

Not requested by the brief's core scope (Ouroboros/Orizon/Landers/Flotte),
added per the session coordinator's steer since `meta-census.md` §5.2 flags
these three as **more scripted than anything in the top 8**, and they sit in
the class that is 44% of our matched pool. None appear in the local archive
and none of the cited sources give exact plant tiles, so no BFS/deniability
numbers are computed here — this is a pointer for a future targeted pass, not
a table.

- **Askar City v72** — "purest script found": launcher first build at round 1
  and conveyor at round 3, in **5/5 games**, across maps from 10×10 to 26×26
  (map-independent timing). Zero gunners built; sentinel/barrier variant of
  the point-blank battery class. Match id `3c61b886-4d08-49a9-baed-c12ae050622d`
  (not local). Source: `meta-census.md` §4.1/§5.2.
- **Team 48 v16** — aim distance **0.0, sd 0, in 5/5 games** (always fires
  point-blank at the core) but *timing* is reactive (first turret r2-12, not
  a fixed round) — per meta-census, "freeze the aim policy, not a turn
  script." Match id `bce041d8-e96c-4871-8d6a-c3523af3ac24` (not local).
- **farming_200s v7** — aim distance **0.0 in 4/4 games with damage**, median
  82 rounds (all-in rush, no game reaches r200). Match id
  `dc5c7700-283d-453d-afa4-77b6eddbdccc` (not local).

---

## 8. Reproducibility

Extraction/geometry scripts used for this pass (scratchpad, not committed —
regenerate from `docs/research/2026-08-07-fanout/toolkit/replay_lib.py` +
`siege_geometry.py` if needed; both are checked into the repo and stable):
map-identify-and-extract-openings pass over `replay_archive/*.meta.json` +
matching `*.replay26`; a BFS-deniability pass reusing
`siege_geometry.SeatAnalysis.dist_own`/`spawn_ring`; a full-game
first-core-threatening-turret scan (not limited to the first 40 rounds) using
`SeatAnalysis.sentinel_threat`/`gunner_threat`; and a manually-transcribed,
dsq-cross-validated table for the thread7/thread3-sourced Orizon/Landers
rows. All local replay decodes passed `replay_lib`'s own `check_all()`
self-checks (delivery×10==titaniumCollected, ammo conservation, no unknown
schema fields) implicitly via successful `load_replay()` — not re-printed
here since none failed.
