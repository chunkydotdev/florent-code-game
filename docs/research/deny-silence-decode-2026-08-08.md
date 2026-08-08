# Deny-arm silence — mechanism decode (BUILD GATE)

**Research-arm decode, 2026-08-08.** Read-only: no games run, no bot files
touched, no platform calls, no downloads. Every input on disk.

**Version stamp.** Live v80 = `bots/_v89sh/main.py`, md5
`e12f85855654e9e78227582d0dc15d4b` (prefix `e12f8585`) — reconfirmed against
the working tree at read time (`md5 bots/_v89sh/main.py`). Source line numbers
below are from that file (5,077 lines).

**Games decoded (5 named zero-fire games + 8 firing controls + 7 zero-exposure
games = all 20 games of 4 matches):**

| corpus | match | seat | games decoded |
|---|---|:--:|---|
| v80 | `16e6c29f-92d5-42a3-b2a2-ac46cbf9cfb2` (Ouroboros v8) | B | g1–g5 |
| v80 | `fe0c595f-a734-4200-a2ba-a0650db22b49` (Memtrace v33) | A | g1–g5 |
| v77 | `d694094e-018d-4d85-8201-2ac9befc162c` (Ouroboros v8) | B | g1–g5 |
| v77 | `922b5da8-9d0d-456b-8bd9-501cb9f3355a` (CtrlAltDefeat) | A | g1–g5 |

Seats read from meta `teamAName`/`teamBName`, never assumed.

**Sources.** `docs/research/v80-production-read-2026-08-08.md` (§2, §4b — the
zero-fire game list and the corpus deny census);
`docs/research/v77-truncated-mechanism-read-2026-08-08.md` **CORRECTION
section only** — its published base-four deny/exposure figures are WITHDRAWN
and were not used; `tools/replay_schema.md`; `tools/replay_census.py` (wire
primitives only). Decoder: fresh implementation in this session's scratchpad
(`deny.py`, `deep.py`, `cascade.py`).

---

## Verdict in one paragraph

**The five zero-fire games do not share one mechanism. They split 3/2, and
the split is clean and measurable.** In three of them
(`16e6c29f` g1, `16e6c29f` g3, `d694094e` g4) the siphoned harvester was an
**orphan standing 8–15 tiles from every builder we owned**, and the deny arm's
acquisition scan — which runs off `get_nearby_buildings()`, i.e. builder
vision r²=20 — could not see it: a builder was inside vision of the siphon
tile on **4.0% / 10.8% / 5.0%** of exposure rounds, and after the role filter
and the 4-round phase gate the arm got a total of **8 / 6 / 12** acquisition
chances across 817 / 213 / 913 exposure rounds. In the other two
(`fe0c595f` g1, `922b5da8` g2) vision was **100.0%** available for the whole
window and the arm still never fired, because the only builders standing in
that vision were in **roles that never reach the deny call** — a role_n == 1
interceptor grinding an ineligible belt one tile away for 760 rounds, and a
role_n == 2 expander captured permanently by the Core-heal / converge /
defend-succession pipeline while the team ran out of units to replace it.
**Candidate 1 (in its vision-scoped reverse form) is CONFIRMED BINDING on 3/5;
role-and-dispatch precedence is CONFIRMED BINDING on 2/5. Candidate 4 (bank
guard) and CPU bailout are CONTRADICTED on all 5. Candidate 2 (phase gate) is
a co-binding amplifier on the 3, never a standalone cause. Candidate 3 (ban
list) is CONTRADICTED as a primary mechanism on 4/5 and UNTESTABLE-FROM-REPLAY
on a 33-round residual in `fe0c595f` g1.**

---

## 0. Parser validation (before any finding)

| check | result |
|---|---|
| **Delivery identity** `core_deliv × 10 == titaniumCollected`, per team-side per game | **40/40 exact** (20 games × 2 sides), zero mismatches |
| Parser trap honoured | `Entity.team` read as proto3 implicit-presence → defaults to **0**, never `None` (`tools/replay_census.py` convention, reused verbatim) |
| Exposure reproduction vs. v80 read | 913 / 360 / 211 / 817 / 760 vs. published 914 / 362 / 211 / 818 / 761 — **off by ≤2**, explained below |
| Zero/non-zero deny classification vs. v80 read | **20/20 games agree**, including all five named zero-fire games |
| Builder-passability of belts (needed for reachability claims) | **10,994** builder-rounds standing on an **enemy** conveyor and **74,529** on a friendly one, across the 20 games; **zero** co-occupancy with harvester / splitter / barrier / turret / core. Conveyors are passable to either team's bots; every other building is not |

**Two declared divergences from the published numbers, neither load-bearing.**

1. **Exposure off by ≤2 rounds per game.** I evaluate geometry at *round
   start* (state after round r−1's updates, which is what the bot acting in
   round r sees). The v80 read's figures are 1–2 higher, consistent with an
   end-of-round snapshot. Direction and magnitude are constant; no conclusion
   moves.
2. **My deny counts run ~7% higher on the firing games** (`16e6c29f` g2 51 vs
   47, g4 10 vs 9, g5 256 vs 239; `d694094e` g1 48 vs 44, g2 34 vs 32, g3 179
   vs 167). Same off-by-one snapshot boundary plus, probably, a stricter
   eligibility test on their side. **The zero-fire classification — the only
   thing this read depends on — is identical on all 20 games.** I flag it and
   build nothing on the absolute counts.

**I found no reason to doubt the v80 read's figures.** They reproduce here.

---

## 1. What the code actually requires (source read, `_v89sh`)

Read in full before reasoning: `_find_siphon` (:4254), `_siphon_taken`
(:4300), `_siphon_deny` (:4318), `_expand` (:3604), `_builder` (:1937),
`_hunt_turret` (:3121), `_core_shelled` (:3100), `_live_home_gun` (:3039),
`_bfs_direction`/`_nav` (:4498/:4590), `_cpu_exhausted` (:1485).

The deny call sits at **`main.py:3800`, inside `_expand`**. Everything that
returns before it is a hard block. In code order:

| # | gate | source | effect |
|---|---|---|---|
| G1 | `_dispatch` → `_builder` | :1474 | builder bots only |
| G2 | `_hunt_turret` returns True | :2184 | turn spent hunting a near-Core turret |
| G3 | universal adjacent Core heal / trunk heal | :2245–2264 | `return` on a heal |
| G4 | `_rank2_hold` / `_home_defend` map gates | :2281–2318 | `return` |
| G5 | `_cpu_exhausted` (CPU_BUDGET_US = 8000) | :2330 | `return` |
| G6 | **role dispatch** | :2339–2346 | `role_n == 0` → `_saboteur`; `role_n == 4` → `_defend`; `role_n == 3` → `_saboteur` once `SLOT_HARVESTERS ≥ 4` and `rnd ≥ 12`; **only `role_n ∈ {1, 2} ∪ {≥5}` enter `_expand`** |
| G7 | `hive_freeze` | :3614–3624 | on 25×25 with our Core at (2,20)/(21,3), past r42, with a live home gun → `_expand` returns **unconditionally, forever** |
| G8 | `role_n == 1 and _intercept()` | :3634 | `return` |
| G9 | `_expand` action phase — link build / medic heal | :3647, :3720 | `return` |
| G10 | `_cpu_exhausted` again | :3730 | `return` |
| G11 | **MULTI-HEALER CONVERGENCE** — `role_n == 2 or ≥5`, `SLOT_UNDER != 0`, `_core_shelled()` | :3764–3778 | `return` **every round**, whether or not it can heal |
| — | **`_siphon_deny`** | **:3800** | |

Inside `_siphon_deny` itself: bank guard `< SIPHON_FIRE_TI` (2 Ti) at :4327;
under-fire ban at :4343; ransom ban at `rnd - siphon_since > SIPHON_MAX_RNDS`
(24) at :4360; phase gate `(rnd + self.idx) % SIPHON_SCAN_EVERY` (4) at :4367;
then `_find_siphon`, whose candidate set comes from `ct.get_nearby_buildings()`
— **vision-scoped, builder vision r² = 20** — and requires **both** one of our
harvesters and the enemy belt inside that radius.

**Role model, validated empirically.** `role_n` is the builder's spawn index
(SLOT_ROLE_N read-then-increment on first run; the Core spawns ≤1 builder per
turn, so each first run lands in a distinct round and the one-round write
buffer cannot collide). Across the four **firing** control games I identified
every unit that produced a deny event: **`16e6c29f` g5 (21 units), `922b5da8`
g4 (6), `d694094e` g3 (16), `16e6c29f` g2 (4) — 47 firing units, and every
single one has `role_n ∈ {1, 2} ∪ {≥5}`. Zero fires from role_n 0, 3 or 4, ever.**
G6 is real and it is the largest single filter in the file.

**Fire-latency calibration.** For every firing unit in those control games I
counted how many rounds it passed the full acquisition gate
(role-eligible ∧ bank ≥ 2 ∧ in phase ∧ belt+harvester in vision) *before* its
first deny event: **median 2, p90 3–14, max 30.** Only two units in the whole
control set had ≥8 gate-passes and never fired (one is a role_n == 1
interceptor). So: **a unit with a handful of gate-passes and no fire is
normal; a unit with 50+ gate-passes and no fire is an anomaly that needs its
own explanation.** This calibration is what makes the per-game verdicts below
falsifiable rather than hand-waved.

---

## 2. Reconstruction, per game

### 2.0 The master table

`inVis` = fraction of exposure rounds on which **any** of our living builders
was within vision (dsq ≤ 20) of an eligible siphon tile. `roleVis` =
builder-rounds where a **role-eligible** builder had **both** the belt and its
harvester in vision. `gate` = those, after the bank guard and the 4-round
phase gate — i.e. the number of acquisition chances the arm actually got.

| match | g | exposure rnds | **deny** | inVis | roleVis | **gate** |
|---|:--:|---:|---:|---:|---:|---:|
| `16e6c29f` | 1 | 913 | **0** | **5.0%** | 72 | **12** |
| `16e6c29f` | 2 | 294 | 51 | 100.0% | 665 | 169 |
| `16e6c29f` | 3 | 213 | **0** | **10.8%** | 24 | **6** |
| `16e6c29f` | 4 | 20 | 10 | 100.0% | 43 | 11 |
| `16e6c29f` | 5 | 913 | 256 | 62.7% | 977 | 248 |
| `fe0c595f` | 1 | 211 | **0** | **100.0%** | **318** | **79** |
| `d694094e` | 1 | 842 | 48 | 100.0% | 4,490 | 1,063 |
| `d694094e` | 2 | 927 | 34 | 94.2% | 1,743 | 432 |
| `d694094e` | 3 | 930 | 179 | 57.1% | 1,144 | 289 |
| `d694094e` | 4 | 817 | **0** | **4.0%** | 33 | **8** |
| `d694094e` | 5 | 4 | 0 | 0.0% | 0 | 0 |
| `922b5da8` | 2 | 760 | **0** | **100.0%** | **1,048** | **263** |
| `922b5da8` | 4 | 246 | 150 | 91.9% | 538 | 132 |

(The seven remaining games have zero exposure and zero deny — the healthy gate
the v80 read reports, reproduced.)

The five zero-fire games are **bimodal on `inVis`**: {4.0%, 5.0%, 10.8%} and
{100.0%, 100.0%}. Every firing game sits at 57–100%. That is the split.

---

### 2.1 GROUP A — vision starvation (`16e6c29f` g1, `16e6c29f` g3, `d694094e` g4)

All three have the same shape: **a single orphan harvester of ours, standing
in no-man's-land or inside the enemy half, tapped by a single enemy belt tile
that is never contested and never changes identity.**

| game | map | our Core | exposed harvester | dsq harv→our Core | dsq harv→their Core | siphon tile | rounds held |
|---|---|---|---|---:|---:|---|---:|
| `16e6c29f` g1 | 16×16 | (11,11) | **(9,2)** | 85 (≈9.2 tiles) | **37 (≈6.1 tiles)** | (8,2) | **913 / 913** |
| `16e6c29f` g3 | 25×25 | (21,3) | (17,17) | 212 (≈14.6) | 234 | (17,18) | 213 |
| " | " | " | (7,7) | 212 (≈14.6) | 194 | (7,8) | 147 |
| `d694094e` g4 | 26×26 | (19,19) | (14,13) | 61 (≈7.8) | 145 | (14,12) | **817 / 817** |

**Where our builders were.** Median distance from the *nearest* living builder
to the eligible siphon tile, over the exposure window:

| game | median nearest dsq | p25 | fraction of rounds ≤ 20 (in vision) |
|---|---:|---:|---:|
| `16e6c29f` g1 | **125** (≈11.2 tiles) | 89 | **0.050** |
| `16e6c29f` g3 | **65** (≈8.1 tiles) | 40 | **0.108** |
| `d694094e` g4 | **128** (≈11.3 tiles) | 72 | **0.040** |

Contrast with the four firing controls: median nearest dsq **1, 1, 9, 16**;
in-vision fraction **1.000, 0.919, 0.627, 0.571**.

**Unit supply was not the problem.** `16e6c29f` g1 ran **38** builders,
`d694094e` g4 **24**, `16e6c29f` g3 **16**. They were all working ore and home
duty in the other half of the board. In `16e6c29f` g1 the best-placed unit of
all 38 got **19** in-vision rounds in a 913-round exposure, and the best
*role-eligible-and-in-phase* unit got **3** acquisition chances — against a
calibrated fire latency whose median is 2 and whose p90 is 3–14.

**Bank was not the problem.** Rounds with global titanium < 2 during exposure:
**34/913, 6/213, 0/817.**

**`hive_freeze` was checked and is NOT armed in `16e6c29f` g3**, even though
that game's geometry (25×25, our Core at (21,3)) matches G7 exactly. The gate
also requires `_live_home_gun()`, and I decoded the whole game: **0 of 356
rounds had any friendly Gunner or Sentinel within dsq 41 of our Core
footprint.** The freeze never fired. Ruled out on evidence, not assumption.
(Recorded because the same geometry recurs — `fe0c595f` g5 is 25×25 with our
Core at (2,20) — and a future game that *does* build a home gun there will
kill the deny arm outright for every expander from r42 to the end.)

**Attribution for Group A: the acquisition scan is vision-scoped and nobody
was ever there.** The phase gate is a genuine co-factor — it cut 72 → 12,
24 → 6 and 33 → 8 — but it is a multiplier on an already-near-empty set, not
the cause.

---

### 2.2 GROUP B, case 1 — `922b5da8` g2: the interceptor holding the wrong tile

28×20, our Core (7,9), theirs (19,9). 1000 rounds, `titanium_collected` loss
873–305. Exposure r240 → r999.

**One tile, one belt, 760 rounds.** The eligible geometry is a single pair:
our harvester at **(12,19)**, tapped by enemy conveyor **id 456 at (11,19)** —
**the same entity id for all 760 rounds.** It is never damaged, never
destroyed, never rebuilt.

**Our builder 5 was parked at (12,19)'s diagonal, (12,18), for the entire
window** — position (12,18) at r240, r300, r400, r500, r600, r700, r800, r900,
never moving. `role_n == 1`: the single interceptor seat, short-circuited at
`main.py:3634` before `_siphon_deny` is ever reached.

**And it was attacking — 355 times — the tile ONE SQUARE NORTH of the siphon:
(11,18).** That tile is an enemy belt that is *not* adjacent to any harvester
of ours, so it is worth nothing to deny. It churned through at least nine
distinct enemy conveyor ids over the window (1234 for 103 rounds; 904, 478,
501, 533, 569, 611, 657, 696 for ~20 rounds each — i.e. ~10 pecks, a kill,
a rebuild, repeat). **We paid ~710 Ti in pecks to kill a conveyor the enemy
rebuilt nine times, one tile away from the belt that was draining us for 760
rounds untouched.** That duty has no ransom cap; the deny arm's
`SIPHON_MAX_RNDS` would have caught exactly this pattern, but the deny arm
never got the unit.

**Everyone else was out of vision until the endgame.** Of the 263 gate-passes
in this game, **190 (72%) belong to builder 5** (the interceptor). The other
**73 belong entirely to the r ≥ 887 tail** — spread over five role_n ≥ 5
expanders (23, 23, 10, 9, 8 each) during a late southward drift, in a window
where the calibrated fire latency (median 2, p90 up to 14) makes a max of 23
per unit borderline rather than damning. **For r240–r886 — 647 rounds, 85% of
the exposure — the only unit of ours ever inside vision of the siphon tile was
the one unit structurally forbidden from acting on it.**

Bank was never a factor: **0 rounds below 2 Ti** in the whole window.
CPU was never a factor: median builder turn 789 µs, p99 5,131 µs, 3 turns of
7,167 above 8,000 µs (0.04%), zero TLEs.

**Attribution: role/dispatch precedence (G8, `role_n == 1` → `_intercept`)
for 85% of the window; vision starvation for the rest.**

---

### 2.3 GROUP B, case 2 — `fe0c595f` g1: one eligible unit, and it was eaten by the heal pipeline

21×8 (the small corridor map), our Core (5,3), theirs (14,3). 476 rounds,
lost by `core_destroyed`. Exposure r20 → r230, again **a single pair**: our
harvester **(9,5)** tapped by enemy conveyor **id 44 at (10,5)**.

**The team was five builders and never grew.** Spawns: ids 3, 5, 7, 10, 13 at
rounds 0, 1, 2, 3, 4 → `role_n` 0, 1, 2, 3, 4. **No builder was spawned after
round 4, in a 476-round game.** Global titanium median **20**, p90 **31**, and
below 30 on **381 of 476 rounds**, against a builder cost that has already
scaled past 70 — the Core could not afford a replacement. Deaths: b10 r57,
b13 r74, b5 r155.

Which leaves the roster, against G6:

| id | role_n | reaches `_expand`? | fate |
|---|:--:|---|---|
| 3 | 0 | **no** — `_saboteur` | parked at (8,4) all game, 17 attacks; in vision of the siphon tile on **211/211** rounds and structurally unable to act on it |
| 5 | 1 | yes, subject to `_intercept` | 27 gate-passes; **died r155** |
| **7** | **2** | **yes** | the only clean case — see below |
| 10 | 3 | **no** after r12 (harvesters ≥ 4) | died r57 |
| 13 | 4 | **no** — `_defend` | died r74 |

**Builder 7's timeline, decoded round by round (r18–r70) and spot-checked to
r470:**

- **r20–r52**: expand-role, in vision (dsq to belt 10–16, to harvester 5–9),
  bank 7–57, Core at **500/500** so G11 converge is off, and it takes **no
  action at all** — pure two-tile movement, (7,5)↔(8,5), (7,6)↔(8,6).
  **8 clean gate-passes with no fire.** This is the one residual anomaly in
  the whole read (§3, candidate 3).
- **r50**: our Core starts taking damage. `SLOT_UNDER` is latched on
  **211/211** exposure rounds (an enemy unit is inside the home band every
  single round), and the Core is below max HP on **182/211**.
- **r53 onward**: b7 walks to **(6,5)** — orthogonally adjacent to Core tile
  (6,4) — and **never leaves it again**, through r470. It heals the Core
  **160 times** in the 211-round window and moves 47 times. Zero builds, zero
  attacks. That is G3 (universal adjacent heal) on the rounds its cooldown is
  zero and **G11 (MULTI-HEALER CONVERGENCE, `role_n == 2`) on every round in
  between** — G11 returns whether or not it can heal, which is precisely why
  the off-cooldown rounds do not fall through to deny either.
- **r74**: b13, the `role_n == 4` defender, dies. `SLOT_DEFEND_BEAT` goes
  stale after `DEFEND_BEAT_STALE_RNDS = 6`, and the DEFEND-ROLE SUCCESSION at
  :2077 promotes b7 (the one `role_n == 2` unit) to `role = "defend"`
  **permanently and irreversibly** (the branch is exactly-once by
  construction). From ~r81 the deny arm has **no reachable unit on the team at
  all** for the remaining 150 rounds of exposure.

Bank was near-irrelevant: 5 rounds below 2 Ti out of 211. CPU was irrelevant:
p99 1,631 µs, max 3,414 µs, **zero** turns above the 8,000 µs guard.

**Attribution: dispatch precedence (G3 + G11 + defend-succession) plus unit
starvation, for 178 of the 211 exposure rounds (84%). A 33-round residual at
the head (r20–r52, 8 gate-passes) is not resolvable from replay — see
candidate 3.**

---

## 3. Candidate-by-candidate verdict

### Candidate 1 — acquisition-only adjacency / vision-scoped acquisition

**Split verdict, and the two halves must not be conflated.**

- **The stated form — "`_find_siphon` requires adjacency at acquisition time,
  and the sticky hold in `_siphon_deny` never re-checks it" — is CONTRADICTED
  as a silence mechanism, on logic, not data.** Re-read :4348–4365: the hold
  only clears on the tile going dead or on the 24-round ransom. A stale hold
  makes the arm attack a belt that is *no longer* adjacent to a harvester —
  that produces **false positives**, which is exactly the "FP-looking" class
  the v80 read already documents (2,743 events, Addendum 2's two innocent
  producers). It cannot produce silence. **This half of candidate 1 is not the
  defect.**
- **The reverse form named in the brief — "a harvester being siphoned far from
  every builder is INVISIBLE, because `get_nearby_buildings()` is
  vision-scoped (r² = 20)" — is CONFIRMED BINDING on 3 of 5 games**
  (`16e6c29f` g1, `16e6c29f` g3, `d694094e` g4), covering **1,943 of the
  2,914 zero-fire exposure harvester-rounds (67%)**. Evidence: in-vision
  fraction 4.0% / 10.8% / 5.0% against 57–100% in every firing game; median
  nearest-builder distance 8–11 tiles; total acquisition chances 8 / 6 / 12
  against a calibrated fire latency of median 2. **Contradicted on the other
  2** (`fe0c595f` g1 and `922b5da8` g2, both at 100.0% in-vision).

### Candidate 2 — phase gate (`(rnd + idx) % SIPHON_SCAN_EVERY`)

**CONTRADICTED as a standalone cause; CONFIRMED as a co-binding amplifier on
the three Group A games.**

No builder can ever be permanently out of phase: `idx = get_id() & 0xFF` is a
constant per unit and `(rnd + idx) % 4 == 0` recurs every 4 rounds for every
possible `idx`. The gate is a uniform 4× discount on scan opportunities. That
is harmless when the in-vision window is hundreds of rounds long (Group B,
firing controls) and materially harmful when it is 5–19 rounds long: in Group
A it cut role-eligible in-vision builder-rounds **72 → 12, 33 → 8, 24 → 6**.
Since the fire-latency calibration says a unit typically needs ~2 gate-passes,
turning a 19-round look into 2–3 chances is the difference between a likely
fire and a coin flip. **It cannot be the fix on its own — removing it entirely
would still leave Group A at 24–72 builder-rounds of contact against
1,943 exposure rounds — but any fix that does not also address it will
under-deliver on exactly these games.**

### Candidate 3 — ban list (`SIPHON_BAN_RNDS = 200`, `SIPHON_MAX_RNDS = 24`)

**CONTRADICTED as the primary mechanism on 4 of 5 games.
UNTESTABLE-FROM-REPLAY on the 33-round residual in `fe0c595f` g1.**

The ban ledger is per-unit and per-tile, and a ban can only exist *after* an
acquisition. Bounding argument:

- `16e6c29f` g1: **at most 12** acquisitions could ever have happened, spread
  over 8 distinct units — while **38 builders** lived in that game, 30 of
  which never had a single gate-pass. A per-unit ban ledger cannot explain 38
  silent units.
- `16e6c29f` g3 (≤6 acquisitions / 16 builders) and `d694094e` g4 (≤8 / 24):
  same argument.
- `922b5da8` g2: the dominant silent unit is the `role_n == 1` interceptor,
  which never reaches `_siphon_deny` at all, so it can neither acquire nor
  ban. Ruled out.
- `fe0c595f` g1, r20–r52: **this is where it is live and unresolvable.** If b7
  acquired (10,5) at r21, `_siphon_deny` returns True every round thereafter,
  the ransom rule fires at r46 (`rnd - siphon_since > 24`), and the tile is
  banned for that unit until **r246 — past the r230 end of exposure**, which
  would silence the game single-handedly. b7's behaviour over r21–r45 is
  *consistent* with a hold (zero builds, zero heals, movement only) and
  *inconsistent* with a working deny nav (the movement is a two-tile
  ping-pong, and after r33 it drifts **west, away** from the target). I cannot
  separate "held a target its navigator could not close on, then banned it"
  from "never acquired" — both render identically in the replay, because
  `_siphon_deny`'s non-adjacent branch produces nothing but a move. **What is
  certain is that this only covers 33 of the game's 211 exposure rounds; the
  other 178 are dispatch precedence, on hard evidence.**

**Note for the builder:** the reachability sub-question *is* settled, and it
does not favour the ban story. The corpus proves conveyors are bot-passable
for both teams (10,994 enemy-belt-standing builder-rounds), and I hand-checked
the r21 geometry: a 6-step path (7,4)→(7,3)→(8,3)→(9,3)→(10,3)→(10,4)
existed and was clear. The target was reachable; the nav did not take it.
`_bfs_direction` (:4498) degrades to a **greedy `cardinal_direction_to` step
whenever `self.map_grid is None`** — i.e. on any map not in the decoded table
— and this 21×8 board's ping-pong is exactly that degradation's signature.
Whether that greedy nav was steering a held siphon target or an ore target is
the thing I cannot tell apart.

### Candidate 4 — bank guard (`get_global_resources() < SIPHON_FIRE_TI`)

**CONTRADICTED on all five games.** Rounds with global titanium below 2 during
the exposure window:

| game | rounds < 2 Ti | of exposure | share |
|---|---:|---:|---:|
| `16e6c29f` g1 | 34 | 913 | 3.7% |
| `16e6c29f` g3 | 6 | 213 | 2.8% |
| `fe0c595f` g1 | 5 | 211 | 2.4% |
| `d694094e` g4 | **0** | 817 | 0.0% |
| `922b5da8` g2 | **0** | 760 | 0.0% |

Two of the five games — including the worst of the two Group B cases, where
the arm had 263 acquisition chances — **never once** had the bank below the
guard. This is not the fjordgate insolvency defect recurring. The guard is
real and it does clear the target (:4331), but it is not what silenced these
games. **Separating it mattered and it separates cleanly.**

### Also asked: role / dispatch precedence

**CONFIRMED BINDING, and it is the largest single filter in the file.**
Empirically validated: **47 firing units across four control games, every one
with `role_n ∈ {1, 2} ∪ {≥5}`; zero fires from `role_n` 0, 3 or 4 in any game
decoded.** Concretely: `role_n == 0` is a saboteur, `role_n == 4` a defender,
`role_n == 3` a saboteur from r12, `role_n == 1` short-circuits into
`_intercept` (:3634), `role_n == 2` and `role_n ≥ 5` are captured by
MULTI-HEALER CONVERGENCE (:3764) for the whole of any siege, and `role_n == 2`
can be promoted out of expand permanently by DEFEND-ROLE SUCCESSION (:2077)
six rounds after the defender dies. On `fe0c595f` g1 that chain removed the
team's *only* eligible unit at r81 and the bank could not buy another. On
`922b5da8` g2 it removed the only in-vision unit for 647 consecutive rounds.

### Also asked: were builders alive and action-capable near the exposure?

Yes in Group B (100% in-vision, 5 and 14 builders, action ledgers dominated by
heals and by attacks on ineligible tiles), no in Group A (4–11% in-vision
despite 16–38 builders). Full per-builder action ledgers are in §2.2/§2.3.

### Also asked: CPU-budget bailouts (`_cpu_exhausted`)

**CONTRADICTED.** Measured from `BotOutput.execTimeUs` over every our-builder
turn in the five games, against `CPU_BUDGET_US = 8000`:

| game | our-builder turns | median µs | p99 µs | max µs | turns ≥ 8000 µs | TLEs |
|---|---:|---:|---:|---:|---:|---:|
| `fe0c595f` g1 | 1,226 | 267 | 1,631 | 3,414 | **0 (0.00%)** | 0 |
| `16e6c29f` g1 | 2,699 | 195 | 2,054 | 6,359 | **0 (0.00%)** | 0 |
| `922b5da8` g2 | 7,167 | 789 | 5,131 | 9,066 | 3 (0.04%) | 0 |
| `d694094e` g4 | 7,500 | 1,191 | 6,519 | 9,232 | 5 (0.07%) | 0 |
| `16e6c29f` g3 | 1,147 | 319 | 8,282 | 8,685 | 33 (2.88%) | 0 |

And these are *whole-turn* totals; the pre-deny portion is a strict subset.
Even the worst game trips the guard on under 3% of turns.

---

## 4. Which fix the evidence licenses

The four candidate fix shapes are mutually exclusive, so this section names
one and says what it costs. **The builder owns the fix; there are no tuning
numbers here.**

### The evidence licenses a DISPATCH fix, not an acquisition-gate fix

Stated plainly: **relaxing `_find_siphon` — dropping the phase gate, widening
the scan radius, re-checking adjacency on the hold, or loosening the bank
guard — cannot recover the two worst games in the corpus, because in both of
them the arm's acquisition path was never the thing that failed.** In
`fe0c595f` g1 and `922b5da8` g2 the geometry was inside vision on **100.0%**
of exposure rounds and the arm still got zero fires, because the units
standing in that vision were in roles that return before `main.py:3800`. Those
two games carry **971 of the 2,914 zero-fire exposure harvester-rounds** and,
in the v80 window, `fe0c595f` g1 alone carries 27 of the 297 leaked stacks the
v80 read attributes to silent-under-exposure games.

Equally plainly: **the dispatch fix alone cannot recover the other three**,
where nothing our team owned was ever within eight tiles of the tap. Group A
needs the siphon sighting to travel further than one builder's r²=20 — a
*published* target, not a wider scan.

The two halves have a common shape and only one candidate matches it:

> **Make the siphon target a TEAM-LEVEL fact rather than a per-unit
> observation, and make the duty assignable to a unit that is free to take
> it.** Whatever unit sees the tap publishes it; whatever unit is
> role-eligible and free claims it, whether or not the tap is inside its own
> vision.

That single change addresses both failure modes: it lets the `role_n == 0`
saboteur standing at (8,4) in `fe0c595f` g1 — in vision of the tap on
**211/211** rounds — hand the sighting to somebody who can act on it, and it
lets a far-away expander in `16e6c29f` g1 be sent to a tap it could never
have seen. It also subsumes candidate 2 entirely (a published fact does not
need re-scanning on a phase), which is the right relationship: the phase gate
is only harmful because acquisition is per-unit and momentary.

### Risk surface of that fix shape — three named hazards

1. **There is no free store slot.** `SLOT_ROLE_N` … `SLOT_SIEGE` occupy
   **0–15, all sixteen**, in `_v89sh`. A published siphon target must either
   reclaim a slot (the file has already done this once — slot 9's
   `SLOT_LINKS_DONE` was provably dead) or pack into an existing one. That is
   the single largest implementation constraint and it is not negotiable.
2. **Store writes are buffered and last-write-wins.** The file's own
   `K_HEAL_BUDGET_ON` comment rules out a team-wide heal *ledger* for exactly
   this reason, and the B8 `SLOT_THREAT` block (:2001–2034) documents a real
   bug where the last qualifying sighting in iteration order won the slot. A
   published siphon tile inherits that hazard verbatim: with several builders
   seeing several taps, some deterministic per-unit tiebreak (the B8 block
   uses smallest core-distance) is required or the slot will oscillate.
3. **Claiming across the map re-opens a refuted class.** `_siphon_taken`
   (:4300) currently enforces one attacker per tile by *local observation*;
   a published target has no such natural bound, and the file carries two
   prior refutations of pulling workers off the economy (the eider 8/16 → 0/16
   ablation and the fjordgate rush regression, both cited at :3157–3163). A
   dispatch fix that recalls distant expanders is the same trade in a new
   costume and needs its own bound.

### What this read does NOT license

- **Any change to the bank guard.** Contradicted on 5/5, zero-binding on 2/5.
- **Any change to the ban/ransom constants.** Contradicted as primary on 4/5;
  the one live case covers 33 rounds of one game and cannot be separated from
  "never acquired". Touching `SIPHON_BAN_RNDS` or `SIPHON_MAX_RNDS` on this
  evidence is tuning against an unmeasured quantity.
- **Any change to the sticky-hold adjacency re-check.** It is an
  FP-suppression change, not a silence fix, and the v80 read already has an
  innocent explanation for the FP class.

### One adjacent finding the builder should see

`hive_freeze` (:3614) returns `_expand` **unconditionally, for the rest of the
match**, on 25×25 maps with our Core at (2,20) or (21,3), past r42, once a
home gun is alive. It did **not** fire in `16e6c29f` g3 (verified: zero
friendly turrets within dsq 41 of our Core in all 356 rounds) — but that
geometry is a live map in the ladder pool (it recurred as `fe0c595f` g5), and
on any such game where we *do* build a home gun, **every deny, every link,
every harvester and every ore walk stops permanently for every expander.** Not
this defect. Worth a separate look.

---

## 5. What would change the answer

1. **A firing/non-firing pair on the same map with the same orphan geometry.**
   The Group A verdict rests on a correlation (in-vision fraction vs. deny
   count) across 13 exposed games, with n=3 zero-fire cases. A game where a
   builder *was* in vision of a far orphan for 20+ rounds and still did not
   fire would break it.
2. **Instrumentation on `siphon_pos`.** One `print()` of the held target per
   acquisition would settle the `fe0c595f` g1 residual (§3, candidate 3)
   outright and is the only thing that can. Replay `BotOutput.stdout` is
   captured, so this is cheap and does not need a new corpus.
3. **A `SIPHON_SCAN_EVERY = 1` ablation.** Would separate candidate 2's
   amplifier role from candidate 1's cause role in Group A directly. My
   claim that it cannot be sufficient on its own is arithmetic (24–72
   builder-rounds of contact against 1,943 exposure rounds), not measurement.
4. **A `role_n`-labelled trace.** My role model is inferred from spawn order
   and validated on 47 firing units with zero counterexamples, but it is still
   an inference. A single stderr line per builder naming its `role_n` and
   final `role` would make it a measurement.
5. **If the v80 read's per-game deny counts are the authoritative ones**, my
   ~7% higher absolute counts (§0) would want reconciling before anyone builds
   on *counts*. Nothing in this read does; it builds only on zero-vs-non-zero,
   where we agree 20/20.

---

## 6. Self-checks — how every claim above was verified

| # | claim | verification |
|---|---|---|
| 1 | Parser is sound | `core_deliv × 10 == titaniumCollected` on **40/40** team-sides across the 20 decoded games; also cross-checked against `tools/replay_census.py`'s independent walk on the same files |
| 2 | Team-0 trap honoured | Ownership read via `parse_entity`'s implicit-presence default (`team = 0`); our own entities appear in every count (e.g. our harvesters, our builders, our deliveries all non-zero in all 20 games) |
| 3 | Live bot identity | `md5 bots/_v89sh/main.py` = `e12f85855654e9e78227582d0dc15d4b`, `wc -l` = 5,077 |
| 4 | Zero-fire game list | Independently recomputed from replays; **20/20 games agree** with `v80-production-read` §2/§4b on zero-vs-non-zero, including all five named games |
| 5 | Exposure figures | Recomputed (913/360/211/817/760); within ≤2 of published, direction explained (round-start vs round-end snapshot), declared in §0 |
| 6 | v77 published deny/exposure figures not reused | Only the CORRECTION section of `v77-truncated-mechanism-read` was consulted; all v77 numbers here are recomputed from `d694094e`/`922b5da8` replays directly |
| 7 | Deny call site and gate order | Read `_expand` (:3604–3855) and `_builder` (:1937–2347) **in full**, line by line, before any attribution; gate table in §1 is transcribed from those reads |
| 8 | Role model (`role_n` = spawn index; only 1/2/≥5 reach `_expand`) | (a) source: SLOT_ROLE_N read-then-increment at :1949–1971 with ≤1 spawn per Core turn; (b) empirical: **47 firing units across 4 control games, 100% with `role_n ∈ {1,2,≥5}`, zero exceptions** |
| 9 | Fire-latency calibration (median 2 gate-passes) | Computed per firing unit in `16e6c29f` g5, `922b5da8` g4, `d694094e` g3; only 2 units corpus-wide had ≥8 gate-passes and never fired |
| 10 | In-vision fractions | Per-round dsq from every living our-builder to every eligible belt tile, threshold r²=20 (builder vision, CLAUDE.md + `get_nearby_buildings` default) |
| 11 | Group A orphan geometry | Per-round enumeration of (our harvester, adjacent enemy belt) pairs; each game's exposure resolves to 1–2 fixed tiles held for the full window; distances measured to both Cores |
| 12 | `hive_freeze` not armed in `16e6c29f` g3 | Full-game scan for friendly Gunner/Sentinel within `HUNT_BAND_DSQ = 41` of our Core footprint: **0 of 356 rounds** |
| 13 | `922b5da8` g2 single-belt identity | Entity-id census on tiles (11,19) and (11,18): id 456 present at (11,19) for **760/760** rounds; ≥9 distinct ids cycled at (11,18) |
| 14 | b5 attacked (11,18) 355 times | `BuilderAttack` (update field 13) events filtered by attacker team and target tile |
| 15 | `fe0c595f` g1 roster and fates | `placeEntity`/`removeEntity` ledger: spawns r0–r4 only; deaths r57/r74/r155; b7 position (6,5) from r53 to end |
| 16 | b7 healed the Core 160× | `BuilderHeal` (field 15) events, target tiles matched against our 2×2 Core footprint (NW-corner convention per `replay_schema.md`) |
| 17 | Bank timeline | `UpdatePlayers.Player.titanium` (field 1) per round, our team side |
| 18 | CPU never binding | `BotOutput.execTimeUs` (field 3) and `tled` (field 4) per our-builder turn, compared to `CPU_BUDGET_US = 8000` |
| 19 | Conveyors bot-passable, other buildings not | Co-occupancy census of builder-bot tiles vs. building tiles across all 20 games: 74,529 friendly-conveyor + 10,994 **enemy**-conveyor co-occupancies; **zero** with harvester/splitter/barrier/turret/core |
| 20 | Store fully allocated | `grep -n "^SLOT_[A-Z_]* = " bots/_v89sh/main.py` → slots 0–15, no gaps |
| 21 | FireTurret ordering trap | Not applicable — no claim here rests on turret-fire attribution; all action attribution uses `BuilderAttack`/`BuilderHeal`/`BuilderBuild`, which carry the acting unit's id explicitly |
| 22 | Round alignment | `turns[i] IS round i`, 0-based, per `replay_schema.md`; geometry evaluated at round start, which is the state the unit acting in round `r` observes |
