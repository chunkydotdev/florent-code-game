# PLAYBOOK — Bean counters **v68**, watched round by round

**PART v68 of a two-part playbook.** A sibling agent covers the **v47 classic**
era; a merge pass follows. **Every section here is self-contained and carries
its own anchors** so the merge can lift them without re-deriving.

**Commissioned:** 2026-08-21 by Magnus, principal, who asked for maximum detail:
*"The more detailed we can do it the better."* This is decode-level *watching* —
what the banked statistics look like as actual play, with round numbers, tiles
and entity ids.

**BASE, cited not re-derived:** `docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md`
(the statistical study, s53). Where a number here is quoted from it, it is
marked **[STUDY §x]**. Everything else in this file was decoded fresh from the
replay bytes for this part.

**Ground.** Team `Bean counters`, id `47803c19-e264-4492-bd62-fbdd58cfd7e6`,
rank 1. **v68 shipped 2026-08-21T07:12:59Z** and held the slot unbroken to at
least 14:21:10Z: **29 decided rated matches, 29 wins, 84.8% of 145 rated games,
+141.3 rating (2153.1 → 2294.4)** [STUDY §4.1].

**Clock:** `date -u` in-shell — study read at **2026-08-21T15:38:11Z**.
**Repo HEAD at watch time:** `ef0a2e8c5` (2026-08-21T17:35:26+02:00).
**Corpus:** `corpus/manifest.json` `built_utc = 2026-08-21T15:33:00Z`,
`git_sha 1d5a6dbde`, 86,185 archived replays, join agree-rate 1.0000.

**Instrument.** One probe written for this part, over the wire-level primitives
in `tools/replay_census.py` (`fields` / `read_pos` / `parse_entity`), per
`tools/replay_schema.md`:

* `scratchpad/s53_beanwatch68_tape.py` — full per-round event tape
  (builds / rotations / moves / deaths / turret fire / builder attacks+heals /
  ammo converts / per-round player state / core-ring occupancy).

**Labelling discipline.** **MEASURED** = read off the replay bytes by the probe.
**EYEBALL** = read off a rendered board or a tape by a human eye without a
control. **INFERENCE** = a causal reading. Refuted guesses are retained, struck
through in place, never deleted.

---

## HOW TO READ THIS

§0 is the slate and the instrument controls. **§1, §2, §8 are the cross-cut
findings** — measured over 112 archived v68 games with a mirror control on every
one. **§3, §5, §6, §7 are the game-by-game watches** (match A Pantheon, match C
us, match B HTTP 418, match D Leviathan). **§4 is the kill arc.** §9 is the
one-line catalog, §10 where it bends, §11 what we could copy, §12 the caveats,
§13 the probe index.

**Three things in here contradict or extend the base study, and they are flagged
where they occur:** the ore-denial plank (§1, extends [STUDY §6.3 CANDIDATE C]),
the displacement loop (§5.1, reopens what [STUDY §3.8] closed), and the
sentinel's inability to rotate (§3.4, the mechanism behind [STUDY §5.4]'s
latency).

## 0. THE GAME SLATE, AND HOW TO WATCH ALONG

**Five matches, 25 games, all v68, all inside the 07:12Z→14:21Z run.** Sources
split two ways, and the split is stated because it matters for reproducibility:
**the archiver had not yet pulled two of them**, so those were fetched
read-only with `fcode match replay` into `scratchpad/s53_beanwatch68_replays/`
(**noted, per the commission**). Nothing else was fired; no submissions, no
rated games, no commits.

| # | match | when (UTC) | opponent | score | replay location |
|---|---|---|---|---|---|
| **A** | `0798229c-f30b-4db3-9102-52c421880cb8` | 11:32:59Z | **Pantheon v105** | **3-2** (the closest call) | pulled → `scratchpad/s53_beanwatch68_replays/` |
| **B** | `05d99bef-68a5-487d-9657-33147216921f` | 13:51:10Z | **HTTP 418 v124** | 5-0 | `replay_archive/` |
| **C** | `32b80f90-9ac4-4c4e-9d80-528b785e5526` | 08:11:52Z (unrated) | **OpenSverige v175 — US** | **0-5** | `replay_archive/` |
| **D** | `07bdf19b-c22d-45e2-8a2c-6f587195cda7` | 14:01:10Z | **Leviathan v91** | 4-1 | pulled → `scratchpad/s53_beanwatch68_replays/` |

**Watch-along commands** (the CLI was checked with `--help` first; it writes an
HTML page under repo-root `scratchpad/replay_view/` and prints the path, and it
never opens a browser):

```bash
# A — Pantheon 3-2, the two games Bean counters LOST are games 2 and 4
.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_2.replay26
.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_4.replay26
# A — the cleanest WIN of that match (24x24 maze, kill at r114)
.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_5.replay26
# B — HTTP 418 sweep
.venv/bin/python tools/replay_view.py replay_archive/05d99bef-68a5-487d-9657-33147216921f_game_1.replay26
# C — what it does to US
.venv/bin/python tools/replay_view.py replay_archive/32b80f90-9ac4-4c4e-9d80-528b785e5526_game_5.replay26
# D — Leviathan; game 1 is the one Bean counters lost
.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch68_replays/07bdf19b-c22d-45e2-8a2c-6f587195cda7_game_1.replay26
```

⚠ **`replay_view.py` is explicitly NOT an instrument** (its own docstring says
so). Every number in this file comes from the tape probe, not from the picture.

### Which replay team index is Bean counters — VERIFIED, not assumed

`teamA` in `corpus/league_matches.tsv` ⇒ replay team **0**. **Positive control
run in both directions and it passes 15/15 games across three matches with
different A/B assignments:** match A (BC = A) replay `winner` reads
t0,t1,t0,t1,t0 = **3-2 for t0**, matching the platform's `scoreA=3`; match B
(BC = **B**) reads t1 five times = **5-0 for teamB**, matching `scoreB=5`; match
C (BC = A, us = B) reads t0 five times = our recorded 0-5. **A decoder that had
the sides backwards would have failed match B and match C in opposite
directions.**

### The instrument, and the two controls it had to pass

`scratchpad/s53_beanwatch68_tape.py` emits every `Update` in the replay as a
labelled line: `BUILD / ROT / REEMIT / MOVE / THROW / DIE / FIRE / BATK / BHEAL
/ AMMO / STACK-STATE / RING`. It reuses `tools/replay_census.py`'s wire
primitives; it does not re-derive protobuf parsing.

1. **Cross-decoder agreement — MEASURED.** On
   `05d99bef…_game_1.replay26` the tape emits **111 BUILD events, split t0=56 /
   t1=55**. `corpus/events.tsv`, written months earlier by
   `tools/corpus/replay_events.py`, holds **111 BUILD rows for the same file**,
   splitting **t0 = 3 barrier + 5 builder_bot + 39 conveyor + 5 harvester + 3
   launcher + 1 sentinel = 56** and **t1 = 20 + 4 + 23 + 3 + 4 + 1 = 55**. Two
   decoders, same number, same split. *(The `placeEntity`-on-rotate trap from
   `corpus-howto.md` TRAP 1 is guarded: a re-emit for a known id becomes `ROT` or
   `REEMIT`, never `BUILD`.)*
2. **Mutation test on the ore flag — MEASURED.** The tape marks every harvester
   build ` ORE` or ` !!NOT-ORE`. On that same file it reads **9 ORE / 0
   NOT-ORE** — which on its own proves nothing, because a constant column
   validates anything. Mutating `envat()` to `return 0` flips it to **0 ORE / 9
   NOT-ORE**. The branch fires both ways.

---

## 1. THE HEADLINE OF THIS PART — a plank the statistical study did not see

**Bean counters barrier the ORE TILE, and they have been doing it since v47.**

**MEASURED, 112 archived v68 games**, `scratchpad/s53_beanwatch68_oredeny.py`,
with the mirror control (identical code path, side index swapped):

| | **Bean counters v68** | **their opponents, same 112 games** |
|---|---|---|
| barriers built | 2,068 | 815 |
| **barriers landing on an ORE tile** | **784 (37.9%)** | 60 (**7.4%**) |
| enemy harvester deaths (their kills) | 200 | 49 |
| **…where the killer barriers that ore tile within 30 rounds** | **185 (92.5%)** | 11 (22.4%) |
| **median latency, harvester death → barrier on that tile** | **1 round** (p90 15, min 0) | 1 round (n=11) |
| ore barriers on a tile that NEVER held a harvester (pre-emptive) | **491 (62.6% of their ore barriers)** | 47 |
| of the 784: in the **enemy's** half / own half / midline | **559 / 201 / 24** | 49 / 1 / 10 |

**The habit in one sentence: when a Bean counters builder finishes chewing an
enemy harvester, the very next thing it does — median ONE round later — is drop
a 3 Ti barrier on the ore tile so the harvester cannot be rebuilt.** And two
thirds of their ore barriers are not even reactive: they are dropped on ore that
nobody has harvested yet, at a median round of 66.

**It is doctrine, not a v68 novelty — CONTROL RUN, and it changes what the merge
should say.** Same probe, 150 randomly-sampled archived **v47** games:
**35.9% of barriers on ore (994/2,770), 90.6% of their harvester kills covered
within 30 rounds (317/350), median latency 1 round.** ⇒ **v47 and v68 are the
same on this plank.**

⚠ **NOTE FOR THE MERGE, checked rather than assumed:** the sibling part
`docs/research/PLAYBOOK-beancounters-PART-v47-2026-08-21.md` (805 lines, read at
17:5xZ) **does not carry this plank** — a grep for `ore` returns only map-legend
and belt lines. **That is not a contradiction between the two parts**, because
the v47 agent watched five games in depth and this cell needs a 150-game census
to see; the v47 control column above was computed here, with the same probe, on
v47 replays. **The merge should take the v47 number from this file and say so,
rather than reading the sibling's silence as a negative.**

⛔ **AND IT IS THE ONE THING THE STATISTICAL STUDY GOT BACKWARDS.**
`REPLAY-STUDY-beancounters-v47v68-2026-08-21.md` §6.1 rows *"barrier on an enemy
ORE tile to pre-empt their harvester — **NO**, no such branch exists"* (a
file:line GREP of our own tree, which is correct), and then §6.3 CANDIDATE C
calls it *"the one genuinely new road in the study"* and **holds it**, on the
grounds that the evidence was only the per-(map, seat) opening-determinism table
and we cannot choose the map. **That reasoning is now moot: the trigger is not a
map lookup at all.** What Bean counters actually run is map-free and needs no
scouting:

> *when an enemy harvester on tile T dies, build a barrier on T.*

That is exactly the "generalised, map-free trigger" CANDIDATE C said had to be
specified before the road could be admitted. **It is specified, it is running on
the rank-1 bot, and it has a measured base rate of 92.5% coverage at a
1-round latency across 112 games.**

**And our side of it is a clean zero — MEASURED with the same probe on 150 of
our own archived games (v175/v176/v177, `scratchpad/s53_beanwatch68_oursample.tsv`):
we built 0 of 1,381 barriers on an ore tile. Exactly zero.** The probe is not
blind on that fixture — it reads **85 of 1,180 (7.2%)** for the opponents in
those same games, and 24 of our 77 harvester deaths get their tile barriered by
the opponent. **So the zero is ours, not the instrument's.**
**INFERENCE:** our tree almost certainly treats ore as reserved-for-harvesters
and filters it out of barrier candidate tiles. That is a one-predicate change,
not a feature.

---

## 2. TWO MORE CROSS-CUT HABITS, MEASURED BEFORE THE GAME-BY-GAME

These two are quantified across all **112 archived v68 games** first, because
every game section below is an instance of them.

### 2.1 The quadrupled rotation is a TARGET-EXHAUSTION RE-AIM, not a patrol

[STUDY §4.2] measured gunner `rotate()` going **2.0 → 8.1 per game** from v47 to
v68 and left it as a number. Watched, it is a rule.

**MEASURED, `scratchpad/s53_beanwatch68_rot.py`, 919 BC rotations over 112 games**,
mirror control on the same code path:

| | **BC v68** (919 rotations) | **opponents, same games** (206) |
|---|---|---|
| the turret had already FIRED from that tile before rotating | **97%** | 87% |
| **its last target DIED within 3 rounds of the rotate** | **64%** | 47% |
| its last target had died earlier | 19% | 36% |
| its last target was still ALIVE (i.e. a rotate off a live target) | 17% | 17% |
| **fires again within 3 rounds of the rotate** | **91%** | 68% |
| median rounds from the rotate to the next shot | **1** | 1 |
| median rounds since its last shot before the rotate | 1 (p90 **6**) | 1 (p90 **31**) |

**Read it as a loop:** shoot down the line → the last thing on that line dies →
pay 10 Ti and one round of cooldown to swing the barrel → shoot again next
round. **The p90 "rounds since last shot" is the sharpest cell: 6 for Bean
counters against 31 for the field.** Their guns rotate while still hot; the
field's rotate after going cold. **INFERENCE: the forward gunner is not a
defensive emplacement being re-aimed occasionally, it is a demolition tool
walking its way through everything inside r²=13 of where it stands.**

**Price it.** 8.1 rotations × 10 Ti ≈ **81 Ti a game in rotation fees alone** —
about the cost of four harvesters, spent purely on aiming.

### 2.2 Ammunition is JUST-IN-TIME and QUANTISED to the shot

[STUDY §3.3] recorded "~56 `convert_ammo` calls a game, a ~10 Ti top-up roughly
every third round". Watched, it is much tighter than that.

**MEASURED, `scratchpad/s53_beanwatch68_ammo2.py`, 112 v68 games**, mirror
control:

| | **BC v68** | **opponents, same games** |
|---|---|---|
| `convert_ammo` calls per game (median) | **67** (p90 102) | 23.5 |
| **round of the FIRST convert (median)** | **27.5** (p10 11) | **1.0** (p10 0) |
| **peak ammo BALANCE ever held (median / p90 / max)** | **26 / 34 / 42** | 30 / **184** / 184 |
| game-total converted Ti **minus** game-total shot cost (median) | **+10** (p10 +2) | +10 (p90 **+90**) |
| **convert amount is an exact sum of 4s and 10s** (gunner 4/shot, sentinel 10/shot) | **8,054 / 8,278 = 97.3%** | 2,011 / 3,755 = **53.6%** |

**The rule: they convert the exact cost of the shots they are about to take, on
the round before they take them, and they never hold more than about three
sentinel shots' worth.** In match A game 5 the whole-game figures are
**558 Ti converted against 554 Ti of shots — a residual of exactly one gunner
shot** — and the per-round series reads `(r33 +14 → r33 spends 14)`,
`(r34 +14 → r35 spends 14)`: **33 of their 58 converts that game exactly equal
the NEXT round's shot bill.**

⛔ **AND HERE IS THE TRAP I ALMOST WROTE, KEPT IN PLACE.** My first draft of this
section called the convert series *"a free read on their intent, one round
early"* — a **+10** announces a sentinel shot next round, a **+14** a sentinel
and a gunner. **That is true of the REPLAY and false of the GAME.** `CoreConvertAmmo`
is an event in the replay file; the `Controller` API exposes
`get_global_ammo()` for **this team's** balance and has no getter for the
opponent's ammo or converts at all. **So this is a scouting fact for us, not an
in-match signal for our bot** — it tells the analyst when their first turret
went up (median r27.5) and how thin their ammo cushion is (peak 26). Nothing in
`bots/` can subscribe to it.

**What IS actionable, and it is the same fact from the other side: their ammo
cushion is ~2 sentinel shots deep and their titanium bank is nearly empty**
[STUDY §5.5: mean end bank 137 Ti on v68]. **INFERENCE, untested:** a burst of
cost they must answer with titanium — repairs, rebuilt barriers, a forced
rotation — competes directly with the next round's shots, because the shots are
being funded a round at a time. This is a hypothesis a leg could test; it is not
a measurement.

---

## 3. MATCH A — Pantheon v105, 11:32:59Z, **3-2**: the closest call of the run

`0798229c-f30b-4db3-9102-52c421880cb8` · BC = **team A = replay t0** ·
ratings before: BC **2249.42**, Pantheon **2143.00** · `eloDeltaA` = **−1.553**.
⭐ **A 3-2 WIN THAT COST THEM RATING** — the exact arithmetic CLAUDE.md flags
(`delta = 32 × (S − E)`, S = games/5): at a 106-point gap, 3-5 games is below
expectation. **Pantheon is the only opponent in the 29-0 run that took two games
in one match.**

Per-game outcome, read off the replay `winner` field:

| game | map | rounds | winner | cond |
|---|---|---|---|---|
| 1 | 22×22 | 222 | **BC** | core_destroyed |
| **2** | **16×16** | **117** | **PANTHEON** | core_destroyed |
| 3 | 26×12 | 295 | **BC** | core_destroyed |
| **4** | **30×30** | **144** | **PANTHEON** | core_destroyed |
| 5 | 24×24 | 115 | **BC** | core_destroyed |

**All five ended in a core kill. Nothing went to r1000 and nothing went past
r295.** This is a knife fight in both directions.

### 3.1 GAME 5 (24×24 maze, BC kill at r114) — the doctrine executed cleanly

Watch: `.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_5.replay26`

The map is a symmetric maze; BC's core sits at **(1,11)** on the west wall,
Pantheon's at **(21,11)** on the east wall, with a walled spine down the middle
and ore in pockets. Row 15 is one of only two clear east-west corridors.

```
  0 .###.###.######.###.###.       t0 = BEAN COUNTERS core @ (1,11)
  1 .#o#.#o#.#oooo#.#o#.#o#.       t1 = Pantheon      core @ (21,11)
  2 .#.#.#.#.#....#.#.#.#.#.       'o' = ORE_TITANIUM  '#' = WALL
  3 .#.#.#............#.#.#.
  4 .#....................#.
  5 ..........####..........
  6 .......####oo####.......   <- ore pair (11,6),(12,6): BC barriers BOTH
  7 #...####........####...#
  8 o...#..............#...o   <- (0,8) BC harvester r5 | (23,8) Pantheon r7
  9 #.........####.........#
 10 .....######..######.....
 11 ..........o##o..........   <- (10,11) BC harv r13 | (13,11) Pantheon harv r19
 12 ..........o##o..........   <- (10,12) BC harv r10 | (13,12) BC BARRIERS r60
 13 .....######..######.....
 14 ..........####..........
 15 #..##..............##..#   <- THE CORRIDOR. Both siege bots walk it.
 16 o...####........####...o
 17 #......####oo####......#   <- ore pair (11,17),(12,17): BC barriers BOTH
 18 ..........####..........
 19 .#....................#.
```

**Rounds 0-3 — four builders, and that is all of them, forever.** `r0` bot **#3**
at (0,10); `r1` bot **#5** at (1,13); `r2` bot **#9** at (3,11); `r3` bot **#13**
at (3,12). **No fifth builder is ever spawned, and none of the four ever dies.**
All four are alive at r114 when the game ends. Pantheon spawns five (#4, #6, #10,
#14 in r0-3, then a fifth **#39 at r12**).

**Rounds 1-15 — the home belt, laid by two bots while two others leave.**
#3 works the north face: conveyor (1,10)→S at r1, harvester **(0,8)** at r5 (ore,
p10 of [STUDY §3.2]'s r2-14 window), conveyors (1,9),(1,8). #5 works the south
face: (1,14)→N r2, harvester **(0,16)** r6, conveyors (1,15),(1,16),(1,13).
Meanwhile **#13 lays a five-conveyor westward chain along row 12 — (4,12) r6,
(6,12) r7, (5,12) r9, (7,12) r10, (8,12) r12 — all facing W, i.e. pointing home**,
and **#9 runs ahead of it along row 11 to the midfield ore and plants harvesters
at (10,12) r10 and (10,11) r13.** By r15 the economy is finished and two of the
four builders are already 9 tiles from home.

**Round 16-31 — THE COLUMN. Two builders walk the corridor in lockstep, one
round apart, and neither builds anything for fifteen rounds.**

```
 #5 : r19 (5,15) r20 (6,15) r21 (7,15) ... r30 (16,15) r31 (17,15)
 #13:            r21 (6,15) r22 (7,15) ... r31 (16,15)
                 ^ trailer is always exactly one tile behind the leader
```

**r32 — the handoff, and it is the prettiest single move in the game.** #5 steps
OFF (17,15) to (17,14); **#13, standing on (16,15), builds the SENTINEL on
(17,15) — the tile the leader just vacated — the same round.** Orthogonal
adjacency is the engine's build rule, so the trailer can only build onto a tile
it is beside; the leader's job is to have walked that tile and left.
**MEASURED** (build ids and rounds off the tape); **INFERENCE** on the intent.

**And (17,15) is not an arbitrary tile.** Sentinel range is r²=32 and its line
ignores obstacles. `(17,15) → (21,11)` is **dx=+4, dy=−4, d² = 32 — exactly at
maximum range, on the NE diagonal, aimed at the core's NW footprint corner.**
The sentinel is built facing **NE**. It opens fire at **r33** and its first shot
is `(17,15)->(21,11) core#2`. **It shoots the core through the entire maze from
maximum range on round 33 of the game, and it is never seriously contested.**

**Rounds 27-36 — the forward gunners.** #9, doubling back, builds a gunner at
**(6,14) r27** facing S — that one is a mid-map skirmisher and it dies at r55.
The important one is #5's: **gunner #114 at (20,13), round 36, facing E** —
**one tile diagonal from Pantheon's core footprint.** #5 built it from (20,14).
**From first spawn to a gunner on the enemy doorstep: 36 rounds.**

**Rounds 36-62 — THE CAGE, tile by tile.** Pantheon's core ring is the 8 tiles
`(21,10) (22,10) (20,11) (23,11) (20,12) (23,12) (21,13) (22,13)`. Bean counters
took 7 of them and the order is not arbitrary — **every ring barrier goes up on
the round AFTER a conveyor on that tile dies**, i.e. they are converting
*delivery faces* one at a time as their guns clear them:

```
                 x=20   21    22    23
        y=10           r53   r52†          †(22,10) needed THREE builds:
        y=11    r44   CORE  CORE   r59       r52 (died r53), r55 (died r60),
        y=12    r61   CORE  CORE   r57       r62 — it is the tile Pantheon
        y=13           ---   r40             fought hardest for
                        ^ (21,13) NEVER SEALED — the 8th tile, open all game
```

| round | event |
|---|---|
| r39 | Pantheon conveyor #15 on **(22,13)** dies (killed by gunner #114 firing E) |
| **r40** | BC barrier **(22,13)** — built by **#5** from (22,14); ring 1/8 |
| r40 | gunner #114 **rotates E → N** (its E line is now empty) |
| r43 | Pantheon conveyor #104 on **(20,11)** dies (gunner #114 firing N) |
| **r44** | BC barrier **(20,11)** — **#13** from (19,11); ring 2/8. #114 rotates **N → SE** |
| r51 | Pantheon conveyor #17 on **(22,10)** dies |
| **r52** | BC barrier **(22,10)** — #5 from (21,10) — **killed by Pantheon at r53** |
| **r53** | BC barrier **(21,10)** — #13 from (20,10); ring 3/8 |
| **r55** | BC barrier **(22,10)** again — #5 from (23,10) — killed at r60 |
| **r57** | BC barrier **(23,12)** — #5 from (23,11); ring 5/8 |
| **r59** | BC barrier **(23,11)** — #5 from (23,10); ring 6/8 |
| **r61** | BC barrier **(20,12)** — #13 from (19,12) |
| **r62** | BC barrier **(22,10)** a **third** time; **ring 7/8, and it holds to the end** |

**The walk that produces this is a circumnavigation.** #5's path from r35:
`(20,14) → (21,14) → (22,14) → (23,14) → (23,13) → (23,12) → (23,11) → (23,10)
→ (22,10) → (21,10)` — **it walks a full lap around the enemy core clockwise,
dropping a barrier on each ring tile as it passes**, while #13 covers the two
west faces `(20,11)`/`(20,12)` from the inside lane. **Two bots, two lanes,
opposite sides.**

**Rounds 62-114 — the strangle, and the ORE BARRIERS.** With the ring at 7/8 the
game is decided; what the builders do next is §1's plank, live:

| round | event |
|---|---|
| r62-r76 | **#9 chews Pantheon's harvester on (13,11)** — 15 consecutive `builderAttack`s (2 dmg each = 30 HP), then one more at **r76 that lands on an EMPTY tile** |
| **r77** | **#9 barriers (13,11)** — the ore tile, 1 round after the kill |
| r64-r78 | **#5 chews Pantheon's harvester on (23,8)** — 15 consecutive attacks, same 1-round overshoot at r78 |
| **r79** | **#5 barriers (23,8)** |
| r89 | #5 barriers **(21,1)** — ore, never harvested by anyone (pre-emptive) |
| r95 | #9 barriers **(11,6)** — ore, pre-emptive |
| r97-r111 | #9 chews Pantheon's harvester on **(12,6)** — 15 attacks + the overshoot |
| **r112** | #9 barriers **(12,6)** |
| r114 | **Pantheon's core dies.** Sentinel #101 has been shooting it from (17,15) since r33 |

**Pantheon's answer, and it nearly worked: they healed the core.** From **r49 to
r114, builder #6 healed Pantheon's own core on (21,12) on 46 separate rounds** —
1 Ti for +4 HP, essentially every round it could. Against a sentinel at 18
damage on a 2-round reload (≈9 HP/round) plus a gunner, 4 HP/round of healing is
a ~45% tax on the siege. **It bought them 81 rounds and it was not enough.**

**A 2 Ti habit worth naming: the overshoot attack.** In all three harvester
chews above, the *last* attack in the series lands on the round the target has
already died — a `builderAttack` on an empty tile. The engine permits it and
charges 2 Ti. **MEASURED** three times in this game; the tape prints it as
`BATK t0 #N -> (x, y) none`.

### 3.2 GAME 5 — the four builders, id-tracked end to end

**MEASURED, `scratchpad/s53_beanwatch68_roles.py`** (a build is attributed to the
only friendly builder orthogonally adjacent to the built tile that round;
ambiguous attributions are reported, not guessed — **1 ambiguous of 45 in this
game**).

| bot | spawn | dies | builds | what it actually is |
|---|---|---|---|---|
| **#3** | (0,10) r0 | **never** | 7 conveyor, 1 harvester (0,8) | **HOME KEEPER.** Never leaves the home quadrant. Rebuilds the ring conveyor (3,12) three times (r30, r34, r106) and heals it. batk **3**, bheal **4** |
| **#5** | (1,13) r1 | **never** | 5 conveyor, 1 harv (0,16), **1 gunner (20,13)**, **8 barriers** | **CAGE WALKER.** Home belt to r15, then the corridor march, the forward gunner at r36, the clockwise lap, 6 ring barriers + 2 ore barriers. batk **19** |
| **#9** | (3,11) r2 | **never** | 2 harv (10,12),(10,11), 2 conveyor, **1 gunner (6,14)**, **6 barriers — all on ORE** | **ORE DENIER / midfield raider.** Highest melee count: batk **30**, all on enemy harvesters and one enemy barrier |
| **#13** | (3,12) r3 | **never** | 5 conveyor, **1 SENTINEL (17,15)**, 3 ring barriers | **SIEGE ENGINEER.** Lays the long belt, walks the corridor as trailer, plants the max-range sentinel, then holds the west ring faces. batk **0**, bheal **5** (heals its own barrier (20,11) five times, r63-r67) |

**Four bots, four jobs, zero deaths, zero replacements.** [STUDY §3.8] measured
0.42 builder deaths per game and a 91% replacement rate at median latency 2 —
this game is the modal case: **nobody kills their builders at all.**

### 3.3 GAME 2 (16×16, **BC's core dies at r116**) — the small-map knife fight they lost

Watch: `.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_2.replay26`

Open board, cores **12 tiles apart** at (7,1) and (7,13). Ore in four clusters
plus two side pairs.

**BC NEVER BUILT A SENTINEL IN THIS GAME.** Not one, in 117 rounds. On a board
this small there is barely a tile that is both inside sentinel reach (r²≤32) and
outside a defending gunner's (r²>13) — and v68's answer is to skip the standoff
gun entirely and fight with gunners. **MEASURED off the tape**: t0 turret builds
are `gunner (9,10) r14 · gunner (10,12) r18 · gunner (7,7) r21 · gunner (10,12)
r25 · gunner (10,12) r29 · gunner (4,12) r69 · gunner (5,12) r71 · gunner
(10,15) r101`. Eight gunners, zero sentinels.

⭐ **AND THEY FED THE SAME TILE THREE TIMES.** (10,12) is 2 tiles from Pantheon's
core ring. BC built a gunner there at **r18 (died r24, age 6)**, again at **r25
(died r27, age 2)**, again at **r29 (died r31, age 2)**. Pantheon's own gunners
sat at (9,11) r17 and (11,11) r20, both covering it. **Three gunners, ~60+ Ti at
scale, six rounds of life between them, into a tile that had already killed
two.**

**Pantheon out-raced them on the ring and never let go**, and this is the one
game in the slate where the tourniquet ran the other way at speed:

| | first ring tile | 3/8 | 5/8 | 6/8 |
|---|---|---|---|---|
| **Pantheon → BC's ring** | **r23** (6,1) | **r33** | **r59** | **r81** |
| BC → Pantheon's ring | r74 (6,13) | r80 | r91 | r105 |

**Pantheon was 51 rounds ahead on the first ring tile and 24 ahead at 6/8.**
BC's cage arrived, tidy and complete, about thirty rounds after the game was
already lost. Core dies r116.

**The ore plank still fires even while losing** — (7,10), Pantheon's harvester
tile, killed at r96: BC barriers it **r97** (dies r98, age 1), **r101** (dies
r111), **r113**. Three barriers on one ore tile in seventeen rounds, in a game
they are losing. **INFERENCE: the ore-denial branch has no "am I winning?"
gate.**

### 3.4 GAME 4 (30×30, **BC's core dies at r143**) — the big-map failure mode, and the mechanism

Watch: `.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_4.replay26`

Cores at (2,14) and (26,14): **24 tiles apart on the biggest map in the pool.**

| round | event |
|---|---|
| r26 | BC barrier (18,14) — the advance marker, 8 tiles out from the enemy core |
| **r28** | **BC sentinel #108 at (21,14) facing E** — d²=25 to the enemy core, the classic standoff tile |
| r29 | Pantheon gunner #111 at (22,14) facing W — head-on into the sentinel's line. **Dies r31, age 2** |
| **r32** | **Pantheon sentinel #120 at (21,16) facing N** — **two tiles SOUTH of BC's sentinel, i.e. OFF ITS FIRING AXIS** |
| **r37** | **BC's sentinel #108 dies, age 9.** Pantheon's #120 lives to r81 — **49 rounds** |
| r37-r127 | **BC has NO sentinel for ninety rounds** |
| r68-r80 | BC tries gunners forward: (26,19) r68 (dies r73), (28,17) r73, (20,16) r75, (28,16) r80, (20,17) r80 |
| **r71 / r73** | **Pantheon counter-invades with TWO sentinels at (8,14) and (7,14)** — 5-6 tiles from BC's core, and they live **49 and 48 rounds** |
| r114/r115 | BC finally answers with gunners at (8,15),(7,16); both dead by r132 |
| r117 | BC's **first and only** ring tile on Pantheon, (25,14) |
| r122 | Pantheon holds **4/8** of BC's ring |
| r128 | BC builds a second sentinel at (23,17) — **100 rounds after the first one died** |
| **r143** | **BC's core dies** |

⭐⭐ **THE MECHANISM, AND IT IS AN ENGINE RULE, NOT A HABIT: A SENTINEL CANNOT
ROTATE.** `can_rotate` / `rotate` are **gunner-only** (CLAUDE.md's Controller
reference; 10 Ti + cooldown 1). **MEASURED confirmation on the tape: of 1,125
facing changes across 112 v68 games — 919 Bean counters, 206 opponents — ALL
1,125 are gunners. Zero sentinels. Zero conveyors.** A forward sentinel is
therefore a **fixed-facing gun aimed at one line, permanently blind to
everything off it**, and its only recourse when attacked from the side is to be
rebuilt somewhere else.

**Pantheon exploited exactly that at r32: it did not duel the sentinel, it stood
beside the sentinel's line.** BC's #108 was pointed E at the core and could not
answer a gun sitting 2 tiles south. It died in 9 rounds; the thing that killed it
lived 49.

**And v68 is very slow to try again.** MEASURED across 112 v68 games: BC builds
**2.04 sentinels a game**, first at a **median round 46** (p10 15, p90 115), with
a **median 42 rounds between consecutive sentinel builds**, and the ones that die
live a **median of 12 rounds** (p10 7). [STUDY §5.4] measured the same thing from
the other side — v68 sentinel replacement latency **median 33 rounds, p90 111**.
**Break the sentinel and the siege stops for a third of a game.**

### 3.5 THE BEND, GENERALISED — v68 is a SMALL-MAP bot

**MEASURED, 112 archived v68 games, banded by map area:**

| map band | n games | **BC game wins** | median game length | gunners/game | **median max enemy-ring tiles held** |
|---|---|---|---|---|---|
| **SMALL** (≤18×18, area ≤324) | 38 | **38 (100%)** | 133.5 | 5.76 | **7 of 8** |
| **MID** (20×20 … 24×24) | 49 | 43 (88%) | 139 | 4.51 | 5 of 8 |
| **BIG** (>576: 26×12, 28×18, 25×25, 30×30) | 25 | **17 (68%)** | 143 | 4.44 | 5 of 8 |

⭐ **AND THE GRADIENT SURVIVES HOLDING THE OPPONENT FIXED**, which is the control
that matters, because map draw and opponent are entangled in this pool:

| opponent | SMALL | MID | BIG |
|---|---|---|---|
| **Pantheon** (40 games) | **13/13 = 100%** | 11/15 = 73% | **6/12 = 50%** |
| Part-timers (25 games) | 5/5 | 13/13 | 7/7 — 100% everywhere |
| Ouroboros (11) | 6/6 | 5/5 | — |
| HTTP 418 (archived, 4) | — | 4/4 | — |

**Against a competent opponent, Bean counters v68 wins every small-map game and
half the big-map games.** Part-timers is the control that shows the gradient is
not about the map alone — a weak opponent loses everywhere.

**INFERENCE on why, and every clause of it was watched in game 4:** on a big map
the walk to the enemy core is 10-15 rounds longer, so the first sentinel lands
later; the standoff tile is further from the escort, so it is easier to flank
off-axis; the sentinel cannot rotate to answer; the replacement takes a median
33-42 rounds; and the ring seal tops out at 5/8 instead of 7/8 because the two
cage bots are strung out over more ground. **Space is what the doctrine cannot
buy.**

⚠ **CAVEAT, stated inline per the numbers-carry-subjects rule:** these 112 games
are **90% unrated challenges** — the same fixture caveat as [STUDY §8.1] — and
the map bands are not balanced across opponents. The **within-Pantheon** row is
the one to quote.

---

## 4. THE v68 KILL ARC, IN PHASES — MEASURED, not inferred

**112 archived v68 games.** First-occurrence round of each landmark, Bean
counters' side, median (p10 / p90):

| phase | landmark | **median round** | p10 | p90 | coverage |
|---|---|---|---|---|---|
| **I. THE FOUR** | first builder bot | **0** | 0 | 0 | 112/112 |
| | **FOURTH builder bot** | **3** | **3** | **3** | 112/112 |
| **II. THE BELT** | first conveyor | 2 | 1 | 6 | 112/112 |
| | first harvester | **5** | 3 | 12 | 112/112 |
| **III. THE MARCH** | first barrier (anywhere) | 33 | 14 | 56 | 112/112 |
| | **first FORWARD turret** (built nearer the enemy core than its own) | **34** | 16 | 49 | 111/112 |
| | first gunner | 36 | 14 | 56 | 109/112 |
| | **first turret at d² ≤ 13 of the enemy core** | **41** | 21 | 65 | 111/112 |
| | first sentinel | 46 | 15 | **115** | 108/112 |
| **IV. THE CAGE** | first tile taken on the ENEMY core ring | **52** | 31 | 80 | 108/112 |
| **V. THE KILL** | **enemy core dies** (games BC wins, n=98) | **131** | 98 | 234 | 87.5% of games |
| | game length, all games | 139 | 101 | 311 | 112 |

⭐ **The r131 median reproduces [STUDY §4.2]'s 131 exactly, on a different game
set (112 archived, vs their frozen 90) with a different decoder.** That is a
free cross-check and it passed.

**Builder count is a constant, not a policy: 104 of 112 games spawn EXACTLY four
builder bots, 7 spawn five, 1 spawns six — and the fourth always lands on round
3 (p10 = p90 = 3).**

**What buys the 15-round speedup over v47 (146 → 131), watched:** phase III is
where the whole difference lives. v47 sent its builders into the enemy *economy*
and spent 129 attacks a game chewing harvesters [STUDY §4.2]; v68 sends the same
builders down a corridor and spends the time putting a gun **on the core** —
first forward turret r34, first turret inside d²≤13 of the core r41. **The
economy raid did not get faster; it got deleted, and the walk replaced it.**

**And the phases overlap by design:** the cage's first ring tile (r52) arrives
*after* the first forward turret (r34) and *after* the first point-blank turret
(r41), because in every game watched the ring tiles are taken **as the forward
guns clear them** — a conveyor on a ring tile dies to gunner fire, and a barrier
goes onto that tile the next round (§3.1's table shows it seven times in one
game). **The guns open the ring; the barriers keep it open.**

---

## 5. MATCH C — **OpenSverige v175 (US) 0-5**, 08:11:52Z, unrated

`32b80f90-9ac4-4c4e-9d80-528b785e5526` · BC = **team A = t0**, we are **t1**.
**This is what the new doctrine does to us, and it is not close.**

| game | map | rounds | BC sentinels: (round, tile, **d² to OUR core**) | ring **they** held on us | ring **we** held on them | **Ti collected BC / US** |
|---|---|---|---|---|---|---|
| 1 | 30×30 | 163 | (r26, (21,14), **25**) · (r113, (24,18), 13) | **8/8** | 2/8 | **1,610 / 80** |
| 2 | 26×12 | 161 | (r35, (19,10), **25**) | 7/8 | 6/8 | **1,590 / 200** |
| 3 | 28×18 | 154 | (r75, (27,7), **5**) · (r132, (22,11), 8) | 6/8 | 6/8 | **1,340 / 290** |
| 4 | 12×12 | 139 | (r56, (7,11), **5**) | **8/8** | 4/8 | **1,170 / 40** |
| 5 | 20×20 | 104 | (r54, (17,4), **1**) · (r72, (12,2), 25) · (r99, (16,4), **2**) | 3/8 | 4/8 | **1,170 / 160** |

**They out-collected us by 8× to 30× in every game.** [STUDY §9] is right that
`titanium_collected` is off-currency for us — but it is a *thermometer*, and it
reads that our economy was shut.

**And here is the single most uncomfortable number in this file: across all five
games we built ZERO gunners and ZERO sentinels in four of them.** Our build
census, `scratchpad/s53_beanwatch68_tape.py`, per game:

```
 g1 US: 7 builders, 5 launchers, 11 conveyors, 1 harvester, 3 barriers   -- 0 turrets
 g2 US: 6 builders, 4 launchers, 16 conveyors, 3 harvesters, 7 barriers  -- 0 turrets
 g3 US: 6 builders, 5 launchers, 26 conveyors, 4 harvesters, 7 barriers  -- 0 turrets
 g4 US: 5 builders, 1 launcher, 11 conveyors, 2 harvesters, 4 barriers,
        2 SENTINELS, 2 GUNNERS
 g5 US: 5 builders, 4 launchers, 18 conveyors, 4 harvesters, 5 barriers  -- 0 turrets
```
**And we finished each game holding 20-22 unspent ammunition** — converted, never
fired, because there was nothing to fire it from.

**The kill mechanism against us, tile by tile — game 5 is the cleanest:**
our core at **(17,2)**, theirs at (1,16), 20×20.

| round | what happened |
|---|---|
| r1-r8 | **We ferry.** Our builder #4 is thrown four times — (16,3)→(11,6)→(7,10)→(3,14)→(0,16) — building a disposable launcher at each hop (#7 (15,3) r1, #13 (11,7) r3, #18 (7,11) r5, #23 (3,15) r7). **It reaches their core ring in EIGHT rounds.** This part works |
| r9-r22 | We take **4 of their 8 ring tiles**: (0,17) r9, (1,15) r11, (0,16) r12, (3,17) r22. Then we stop. **We never get past 4/8 and we never build a gun** |
| r12 | BC's first gunner, (6,15) — home side, killing our forward launcher line |
| r26-r43 | BC's builders lay **seven barriers** across the midfield — (10,12),(9,11),(11,13),(6,10),(11,3),(11,8),(4,6) |
| r49 | BC gunner (15,6) — **9 tiles into our half.** It rotates four times (r53 NE→S, r60 S→E, r70 E→N, r83 N→SE) and lives **54 rounds** |
| **r54** | **BC SENTINEL at (17,4) — d² = 1 from our core footprint. Point blank, on our ring tile.** |
| r72 | second sentinel (12,2), d²=25 |
| r99 | third sentinel (16,4), d²=2 |
| **r103** | **our core dies** |

⛔ **A GUESS I MADE AND THEN CHECKED, KEPT IN PLACE.** My first reading was
*"the r54 sentinel alone accounts for the kill clock — 500 HP ÷ 9 HP/round ≈ 55
rounds, r54 + 49 = r103"*. **The arithmetic fits and the tape says it is wrong.**
Counting the actual `FireTurret` events landing on our core:

```
 sentinel #163 (17,4)  d²=1   25 shots,  r55 -> r103   =  450 dmg
 sentinel #195 (12,2)  d²=25  13 shots               =  234 dmg
 sentinel #245 (16,4)  d²=2    2 shots               =   36 dmg
 gunners: ZERO shots at our core.  builder attacks on our core: ZERO.
                                              total 720 dmg on a 500 HP core
```
**It is the NEST, not the first gun — #163 is 62% of it** — and the surplus over
500 is our own core healing. **What does hold is [STUDY §5.7]: every point of
damage to our core came from sentinel fire. Not one gunner shot, not one builder
melee.** A "fits the clock" coincidence is exactly the kind of number that gets
published; the discriminator was counting the events.

**INFERENCE, and it is the plainest reading available:** we spent the game
reaching their doorstep and doing nothing when we got there, and they spent it
walking a gun to ours. **A seal without a gun is a blockade; a gun without a seal
is a kill.**

### 5.1 ⭐⭐ AND WE ACCIDENTALLY RAN THE BEST EXPERIMENT IN THE SLATE

**In match C game 2 our launcher put one of Bean counters' four builders into an
infinite loop and held it there for 37 rounds.**

**MEASURED off the tape** (26×12; BC core (2,5), ours (22,5); our launcher #137
built at **(1,7)** on **r52**):

```
 r52   we build launcher #137 at (1,7)                 [20 Ti, once]
 r54   THROW  BC builder #8  (2,8) -> (0,11)
 r55-58 #8 walks (0,11)->(0,10)->(0,9)->(1,9)->(2,9)
 r59   #8 steps back onto (2,8)  ->  THROW  (2,8) -> (0,11)
 r64   ...identical...            ->  THROW
 r69   THROW    r74  THROW    r79  THROW    r84  THROW
 r91   THROW  (one cycle took 7 rounds; the bot took a longer way round)
```
**Eight throws, r54 → r91, cycle length median 5 rounds (p10 5, p90 7), the
SAME destination tile (0,11) all eight times, and the SAME five-tile return
route on seven of the eight.** Their builder never varied the plan, never routed
around the launcher, and **never attacked it** — Bean counters build no
launchers and have no counter-throw code at all [STUDY §3.9: 0 launchers and 0
throws in 1,385 games].

**Census across the whole v68 archive: a Bean counters builder has been thrown
exactly EIGHT times in 112 archived v68 games — and all eight are these, in our
match. Nobody else in the league has thrown one.**

⛔ **The border-crash channel did NOT fire, and that is consistent with the
banked evidence, not against it.** `(0,11)` is a west-border tile. Their builder
survived all eight throws. [STUDY §3.9]: of 162 kidnaps of a Bean counters
builder across the archive, 95 landed on a border tile and **1 died**, against a
2.2% field baseline. **We should stop expecting the crash and start using the
displacement.**

⭐ **THIS REOPENS A ROAD [STUDY §3.8] CLOSED.** That section retired *"kill their
four builders"* because they lose only 0.42 builders a game and replace 91% of
them within a median of 2 rounds. **But a thrown builder is not a dead builder —
so no replacement is triggered at all.** One 20 Ti launcher removed **25% of
their entire workforce** (they run exactly four builders, r0-r3, in 104 of 112
games) for 37 rounds and counting, with zero further spend and zero risk.
**Denial by displacement is not the same road as denial by killing, and the data
that closed the second one says nothing about the first.**

⚠ **HONEST n: this is ONE loop, in ONE game, against ONE builder.** It is a
mechanism demonstration, not a rate. What it justifies is a pre-registered leg,
not a shipped plank.

---

## 6. MATCH B — HTTP 418 v124, 13:51:10Z, **5-0** — the sweep, and the point-blank nest

`05d99bef-68a5-487d-9657-33147216921f` · BC = **team B = t1** ·
`eloDeltaA = −6.374` (HTTP 418's loss).

**HTTP 418 is the team that beat their v47 70% of the time [STUDY §4.3] — the
only counter in the field that builds launchers. Against v68 it took zero
games.**

**MEASURED, BC's turret geometry in this match — read the d² column, it is the
whole story:**

| game | map | rounds | BC sentinels (round, tile, **d² to enemy core**) | BC gunners (round, **d² to enemy core**) |
|---|---|---|---|---|
| 1 | 22×22 | 130 | r51 (5,6) **25** | r34 **49** · r36 **197** (home) · **r61 d²=5** |
| 2 | 26×12 | 180 | **r79 (0,8) d²=8** · **r96 (1,8) d²=5** | r14 **205** (home) · **r47 d²=4** · r102 **9** · **r106 d²=2** · r133 **4** · r157 109 |
| 3 | 20×20 | 150 | r24 (6,5) 18 · **r86 (4,1) d²=1** | r22 193 (home) · r45 25 · **r70 d²=5** · r77 **4** · r78 32 |
| 4 | 20×20 | 181 | r79 (9,5) **9** · r167 (5,6) 32 | r51 26 · **r67 d²=10** · **r76 d²=5** · **r92 d²=9** · r115 49 |
| 5 | 24×24 | 111 | **r42 (2,10) d²=1** · **r100 (3,14) d²=5** | r25 325 (home) · **r36 d²=4** · **r48 d²=5** |

**[STUDY §3.5] measured v68 sentinels at d²≤13 of the enemy core in 53.3% of
builds, against v47's 23.9%, and called it *"v68 abandons that caution and walks
onto the core"*. Watched, "walks onto the core" is literal: `d² = 1` means the
sentinel is standing ON a ring tile of the enemy core**, i.e. on the same eight
tiles the barriers are supposed to occupy. **In this match six of nine
sentinels and twelve of twenty-nine gunners are at d² ≤ 10 of the enemy core**
(counted off the table above).

**And every game also carries at least one deep-HOME gunner** — d² = 197, 205,
193, 325 to the enemy core, i.e. sitting in their own base — built early
(r14-r36); game 4's nearest equivalent is the r115/r117 pair at d² 49/36. That is
[STUDY §3.6]'s ring-sweeper: the gun that clears forward turrets out of their own
half at 79.7% (v47) / 76.6% (v68). **One home gun, three-to-nine forward.**

**Economy, end of game (BC / HTTP 418 titanium collected):**
820/320 · 2,280/840 · 1,660/310 · 2,120/880 · 1,170/230.

---

## 7. MATCH D — Leviathan v91, 14:01:10Z, **4-1** — and the game they lost is a 273-round strangle

`07bdf19b-c22d-45e2-8a2c-6f587195cda7` · BC = **team A = t0** · Leviathan won
**game 1**.

**Game 1 (30×30, BC's core dies r272) is the mirror of everything above, run
against them.** Leviathan does not play Bean counters' game — it plays Bean
counters' game *harder*:

| | Bean counters | **Leviathan** |
|---|---|---|
| builder bots | **4** | **9** |
| conveyors | 25 | **88** |
| harvesters | 3 | 7 |
| gunners | **1** (r23) | 0 |
| sentinels | **1** (r33) | **8** |
| **max ring tiles held on the opponent** | 2/8 | **8/8** |
| titanium collected | **240** | **2,280** |

| round | event |
|---|---|
| r23 | BC gunner (15,24), **d²=4 from Leviathan's core** — point-blank, early |
| r33 | BC sentinel (12,25), **d²=5** — also point-blank |
| — | both are gone by the midgame, and **BC never builds another turret in 240 remaining rounds** |
| r58/r66 | BC takes 2 of Leviathan's 8 ring tiles, and never gets a third |
| **r67 → r91** | **Leviathan seals BC's ring one tile at a time: 1/8 r67, 2/8 r70, 3/8 r74, 4/8 r77, 5/8 r81, 6/8 r84, 7/8 r88, 8/8 r91** — 24 rounds from first tile to full seal |
| r91 → r272 | **the seal holds for 181 rounds.** BC collects 240 Ti in the whole game |
| r245-r258 | Leviathan stacks **seven sentinels** at (14,8),(14,7),(14,6),(13,4),(12,5),(17,5),(11,6) |
| r272 | BC's core dies |

**INFERENCE:** on a 30×30 board v68 shot its whole siege budget in the first 35
rounds, at point-blank range, and had no plan B. The rest of the game it laid
barriers.

**And the counter-recipe is measurable.** MEASURED across all 112 archived v68
games, banded by **the most ring tiles the OPPONENT ever held on Bean counters**:

| opponent's seal on BC's ring | n games | **BC wins** | median BC `ti_collected` | median game length |
|---|---|---|---|---|
| 0-3 of 8 | 71 | **68 (96%)** | 1,280 | 125 |
| 4-5 of 8 | 19 | **19 (100%)** | 1,540 | 139 |
| **6-7 of 8** | 17 | **8 (47%)** | 1,340 | 179 |
| **8 of 8** | 5 | 3 (60%) | 1,330 | 386 |
| **pooled ≥6/8** | **22** | **11 (50%)** | — | — |

**The discontinuity is at SIX TILES. Below it Bean counters win 87 of 90 (96.7%);
at six or more they win 11 of 22 (50%).**

⚠⚠ **THIS IS CORRELATIONAL AND I AM NOT GOING TO DRESS IT UP.** Games where an
opponent reaches 6/8 are also games that ran longer (median 179/386 vs 125) —
more rounds is more chance to seal — and are plausibly games where Bean counters
were already losing for other reasons. **Reverse causation is entirely live
here.** What the cell licenses is *"the seal-back is the shape that shows up in
every game they lose"*, which is what [STUDY §5.2] found by a different route
(O(1) seals 8/8 in 58% of games and takes 54%). **It does not license a causal
dose curve, and a leg would have to establish one.**

**One more, and it is the disappointing half:** BC's **first forward sentinel
dying** moves them from **63/65 wins (97%)** to **35/43 (81%)**. **Killing the
first siege gun is worth ~16pp and is not remotely sufficient.** The seal-back is
the bigger lever.

---

## 8. ⭐⭐ THE MEAT GRINDER — v68 will rebuild a gunner on a tile that has already killed thirty of them

Found while auditing repeat builds, not looked for. **MEASURED,
`scratchpad/s53_beanwatch68_retile.py`, 112 archived v68 games:** Bean counters
built 780 turrets on 701 distinct tiles; **79 of those builds are a rebuild on a
tile where one of their own turrets had already died.** Median rebuild latency
**4 rounds** (p10 1). And the tail is not a tail, it is a policy:

| game | map | tile | **d² to the ENEMY core** | **turret builds on that ONE tile** | deaths on it | **lifespan of each** | span |
|---|---|---|---|---|---|---|---|
| `74a8f527…` game (12×12, r418, **BC won**) | 12×12 | **(0,0)** | **2** | **31 gunners** | 31 | **every single one lived exactly 1 round** | r125 → r298 |
| `487a97fe…` game (20×20, r213, **BC lost**) | 20×20 | **(16,15)** | **4** | **30 gunners** | 30 | 2-3 rounds each | r29 → r192 |

**Thirty-one gunners onto one tile, each dying the round after it is built, for
173 rounds.** At a mid-game cost scale a gunner is 30-45 Ti, so this is on the
order of **1,000+ titanium poured into a single tile** — and in the second case
they lost the game while doing it.

**INFERENCE on the mechanism (and it is a guess about their code, flagged as
such): their forward-turret placement scores a tile by geometry — nearness to the
enemy core, firing lines — and carries no memory that the tile has killed
everything ever put on it.** [STUDY §5.4] concluded *"break the guns, not the
belt"*, which is right; **this sharpens it to "break the guns on a tile they will
re-seed, and they will keep paying"**.

⚠ **n = 79 rebuild events across 112 games, of which two tiles account for 61.**
The heavy cases are rare — 2.9% of their turret tiles are built on more than
once. **What is cheap to test is whether the behaviour is TRIGGERABLE**: does a
reliably-covered tile near our core reproduce it? That is a leg, not a
conclusion.

---

## 9. THE COMPRESSED TACTIC CATALOG

Every line: the tactic, the sharpest measured number, the anchor.

| # | tactic | sharpest number | where |
|---|---|---|---|
| 1 | **Four builders, round 0-3, and never another** | exactly 4 in **104 of 112 games**; the 4th lands on r3 with p10 = p90 = 3 | §4 |
| 2 | **Fixed builder roles** | home-keeper / cage-walker / ore-denier / siege-engineer; **all four alive at the end** of match A g5, 0 ambiguous of 45 builds after 1 | §3.2 |
| 3 | **Ore-tile denial after a harvester kill** | **92.5%** of their harvester kills get a barrier on that ore tile, **median latency 1 round** (185/200) | §1 |
| 4 | **Pre-emptive ore denial** | **491 of 784** ore barriers are on tiles nobody ever harvested, median round 66 | §1 |
| 5 | **Two-bot corridor column with a tile handoff** | leader vacates (17,15) at r32, trailer at (16,15) builds the sentinel on it the same round | §3.1 |
| 6 | **Max-range diagonal sentinel** | (17,15)→(21,11) is **d² = 32 exactly**, sentinel max range, opens fire r33 | §3.1 |
| 7 | **Forward gunner on the doorstep** | gunner at (20,13), **r36**, one diagonal from the core footprint; first forward turret at median **r34** across 112 games | §3.1, §4 |
| 8 | **Point-blank sentinel** | 7 of 9 sentinels at **d² ≤ 10** in match B; **d² = 1** (i.e. standing on the ring) three times in the slate | §6, §5 |
| 9 | **One home gunner, always** | d² 193-325 to the enemy core, built r14-r36, in every game of match B — the ring sweeper | §6 |
| 10 | **Rotation = target exhaustion** | **64%** of 919 rotations follow their last target's death within 3 rounds; **91%** fire again within 3; median 1 | §2.1 |
| 11 | **Rotations are gunners only** | **1,125 of 1,125** facing changes are gunners. **A sentinel cannot rotate** — engine rule | §3.4 |
| 12 | **Just-in-time ammunition** | **97.3%** of 8,278 converts are exact sums of 4s and 10s; peak balance held median **26**; first convert median **r27.5** | §2.2 |
| 13 | **Cage built as the guns clear it** | 7 ring tiles in match A g5, **every one built the round after a conveyor died on it**; (22,10) rebuilt three times | §3.1 |
| 14 | **Cage by circumnavigation** | one bot walks a full clockwise lap of the enemy core, dropping a barrier per ring tile; the other covers the two far faces | §3.1 |
| 15 | **The overshoot attack** | the last `builderAttack` of every chew series lands on an already-empty tile — 2 Ti, three times in one game | §3.1 |
| 16 | **Same-tile turret rebuild** | **31 gunners on one tile, each living 1 round**, r125→r298 | §8 |
| 17 | **Sentinel scarcity** | **2.04 sentinels/game**, first at median **r46**, **42 rounds** between consecutive builds, median lifespan **12** | §3.4 |
| 18 | **No launchers, no throws, no counter-throw** | 0 launchers in 112 v68 games; a BC builder thrown 8 times never adapted its route | §5.1 |
| 19 | **No "am I losing?" gate** | the ore-denial branch fires three times in 17 rounds in a game they are losing at r97-113 | §3.3 |
| 20 | **Kill clock** | median **r131** when they win (n=98) — reproduces [STUDY §4.2]'s 131 on a different set | §4 |

---

## 10. WHERE IT BENDS — ranked, with the caveat attached to each

1. **BIG MAPS. This is the biggest single crack, and it survives holding the
   opponent fixed.** vs Pantheon: **SMALL 13/13 (100%) · MID 11/15 (73%) · BIG
   6/12 (50%)**. Pooled over all opponents: 38/38 · 43/49 · 17/25.
   *Caveat: 90% unrated pool, unbalanced map draw across opponents — quote the
   within-Pantheon row.* (§3.5)
2. **THE UNROTATABLE SENTINEL, FLANKED OFF-AXIS.** Pantheon killed a forward
   sentinel in **9 rounds** by placing its own sentinel **2 tiles off the
   victim's firing line**; the killer lived 49. **A sentinel cannot rotate —
   1,125 of 1,125 measured facing changes are gunners.** *Caveat: this is an
   engine rule (safe) plus one watched instance of the counter (n=1 for the
   tactic itself).* (§3.4)
3. **SEAL THEIR RING BACK, AND THE THRESHOLD IS SIX TILES.** Opponent holds ≤5
   of 8: BC wins **87/90 = 96.7%**. Opponent holds ≥6: BC wins **11/22 = 50%**.
   *Caveat: CORRELATIONAL — 6/8 games run longer (median 179 vs 125) and may
   already be games they were losing. Reverse causation live.* (§7)
4. **THE 90-ROUND SENTINEL GAP.** Kill the forward sentinel and it is replaced at
   a **median 33-42 rounds** (p90 111); in match A g4 the gap was **91 rounds**
   on a 30×30. *Caveat: killing the FIRST forward sentinel only moves them 97% →
   81%. Necessary, nowhere near sufficient.* (§3.4, §7)
5. **THE DISPLACEMENT LOOP.** One 20 Ti launcher held one of their four builders
   in a 5-round throw cycle for **37 rounds, 8 throws, same destination tile
   every time, same return route 7 of 8 times.** They have **no launcher, no
   counter-throw and no re-plan.** *Caveat: n = 1 loop, 1 game, 1 builder — a
   mechanism demonstration, not a rate. And the CRASH channel did NOT fire: the
   builder survived all 8 border throws, consistent with [STUDY §3.9]'s 1 death
   in 95 border exiles.* (§5.1)
6. **THE MEAT GRINDER.** They will re-seed a killed turret onto the same tile —
   **31 times, one round of life each.** *Caveat: rare (2.9% of their turret
   tiles); the question worth a leg is whether it is TRIGGERABLE.* (§8)
7. **SMALL MAPS KILL THE STANDOFF, AND THEY KNOW IT.** On 16×16 in match A g2
   they built **zero sentinels** and fought with eight gunners — three of which
   went onto the same covered tile (10,12) at r18/r25/r29 and lived 6, 2 and 2
   rounds. *Caveat: n = 1 game for the zero-sentinel behaviour; the
   gunners-per-game rise on small maps (5.76 vs 4.44) is the 112-game version.*
   (§3.3)

---

## 11. WHAT WE COULD COPY — and what we already have

*(Drafted for the merge and for research to admit or reject. **No QUEUE row was
written, no bot file was touched, nothing was fired, nothing was committed.**)*

**COPY 1 — ORE-TILE DENIAL. The cheapest and the best-evidenced.**
The trigger is map-free: *when an enemy harvester on tile T dies, barrier T.*
They run it at **92.5% coverage, 1-round latency, across both v47 and v68**; **we
run it at 0.0% — literally 0 of 1,381 barriers on an ore tile in 150 of our
recent games**, while our opponents manage 7.2% in the same games. This is
almost certainly a single exclusion predicate in our barrier tile filter.
**[STUDY §6.3 CANDIDATE C] held this road for lack of a map-free trigger. The
trigger is now specified and measured; the hold reason is gone.**
⚠ Owed before any prereg: `tools/target_value.py`, a GREP of the incumbent's
barrier-tile filter for the ore exclusion, and a hot-turn cost stamp.
⚠ **PROGRAMME check:** its only channel is the opponent's `titanium_collected`,
which is **off-currency** under `R1000_IS_DEFEAT` — so it must be argued as
*"opens the lane"* (a starved opponent builds fewer turrets), not as economy.
**That argument is not made by this file.**

**COPY 2 — FLANK THE SENTINEL, DO NOT DUEL IT.** A sentinel cannot rotate. Any
turret we place **off a forward sentinel's firing ray** is fighting something
that physically cannot shoot back. Pantheon did it at 2 tiles' offset and won a
49-vs-9-round trade. **We already have the code path** — `_door_turret`
(`main.py:1653-1744`), `FS_DOOR_TYPES`, `FS_DOOR_DSQ = 40` per [STUDY §6.1] —
what it may lack is the *axis* term. [STUDY §6.1] notes we have
`FS_SENTINEL_GUNAXIS_PENALTY` for placing OUR sentinels off an enemy gunner's
axis; the mirror (place our answer off THEIR sentinel's axis) is the thing to
grep for. **This overlaps [STUDY §6.3 CANDIDATE A DOORWIDE] and the merge must
say how, before either is admitted.**

**COPY 3 — DISPLACEMENT, NOT DECAPITATION.** We already ship launchers and
`_fs_evict`. What match C game 2 shows is that a launcher parked on their
**approach tile** — not their core — recycles the same builder every 5 rounds
forever, because a displaced builder is alive and therefore never replaced. **We
have exactly four targets to choose from and their spawn rounds are 0,1,2,3.**
⚠ n=1. This is a leg.

**COPY 4 — THE TWO-BOT COLUMN WITH A TILE HANDOFF.** Leader walks, trailer
builds on the vacated tile. It costs nothing but ordering, and it puts the
turret one round earlier than a single bot that must walk-then-build.
⚠ **EYEBALL-grade on the intent**; the rounds and ids are MEASURED but I have
not shown it is a rule rather than a coincidence of two bots on one corridor.

**DO NOT COPY — already ours, or refuted:**
* **The ring cage.** [STUDY §6.1/§6.2] — we ship it, target it harder (75.4% of
  our barriers vs their 55.5%) and start earlier (r12 vs r35). Our gap is
  *completion*, not adoption.
* **CPU denial.** [STUDY §3.7] — 0 TLEs in 90,930 v68 unit-turns. Dead.
* **Border crash-induction against them.** Their builder survived all 8 border
  throws in our own match, on top of [STUDY §3.9]'s 1-in-95. Not demonstrated.
* **"Kill their four builders."** [STUDY §3.8] — 91% replaced in 2 rounds.
  **But see COPY 3: displacing is a different verb and that refutation does not
  reach it.**

---

## 12. CAVEATS, KEPT INTACT

1. **Population.** The 112-game cross-cut cells are **archived v68 games, ~90%
   unrated challenges** — the same fixture caveat as [STUDY §8.1]. Unrated pools
   PROTOTYPES on the challenger side, so every "BC vs the field" share here
   overstates them relative to their rated record. **The five matches watched
   game-by-game are four rated + one unrated (match C, ours), stated per match.**
2. **Clustering.** Games cluster in matches (5 per match) and in opponents. **No
   half-width in this file has the CLUSTER-DEFF correction applied, because
   every cell here is a point estimate or a within-game count, not an interval.**
   Any cell promoted to a bar must be re-stated with the CLAUDE.md DEFF (1.833
   unrated / 1.529 rated) first. **The two cells most at risk of being
   over-read are §3.5's map gradient and §7's 6/8 threshold.**
3. **The 6/8 seal threshold is correlational.** Longer games, and plausibly
   already-losing games, both push the seal count up. Stated in §7 and repeated
   here because it is the cell most likely to be lifted out of context.
4. **v68 is under a day old.** 112 archived games, 30 rated matches. Several
   cells (the 8-throw loop, the two meat-grinder tiles, the zero-sentinel
   small-map game) rest on **n = 1 game**, and say so inline.
5. **Build attribution to a specific builder bot is positional** — the only
   friendly builder orthogonally adjacent to the built tile that round. Ambiguity
   is reported (**1 of 45** in match A g5), never guessed. Turret-removal and
   ore-coverage matching is by **tile + later round**, not entity id, matching
   [STUDY §8.7]'s method and inheriting its blur on rebuilds.
6. **Fire attribution resolves the shooter and target by tile occupancy at ROUND
   START**, per `tools/replay_schema.md`'s FireTurret ordering trap. Targets that
   die earlier in the same round therefore read as blank rather than as whatever
   moved onto the tile — that is deliberate.
7. **`replay_view.py` is not an instrument** and nothing in this file is sourced
   from a rendered picture. Its own docstring makes the same point.
8. **Two matches (A and D) were fetched with `fcode match replay` because the
   archiver had not reached them.** They are in `scratchpad/s53_beanwatch68_replays/`
   and are **not** in `corpus/`, so a re-run of the 112-game cross-cuts will not
   include them. Every cross-cut number in this file is computed on the 112
   **archived** games only; matches A and D contribute narrative, not statistics.
9. **Nothing was fired, submitted, or committed.** No edits to `QUEUE.md`,
   `bots/`, `tools/`, or `corpus/`. The only file written outside `scratchpad/`
   is this one. Probes: `scratchpad/s53_beanwatch68_*`.

---

## 13. PROBE INDEX (for the merge, and for whoever re-runs this)

| file | what it does |
|---|---|
| `scratchpad/s53_beanwatch68_tape.py` | the per-round event tape; `--only`, `--from/--to`, `--map`, `--summary` |
| `scratchpad/s53_beanwatch68_roles.py` | per-builder-bot role trace with positional build attribution |
| `scratchpad/s53_beanwatch68_oredeny.py` | ore-tile denial + kill→barrier latency, with mirror control |
| `scratchpad/s53_beanwatch68_oredeny2.py` | the same, split by map half |
| `scratchpad/s53_beanwatch68_rot.py` | rotation-stimulus probe, with mirror control |
| `scratchpad/s53_beanwatch68_ammo.py` / `_ammo2.py` | convert-to-fire and just-in-time ammo, with mirror control |
| `scratchpad/s53_beanwatch68_retile.py` | same-tile rebuild / meat-grinder probe |
| `scratchpad/s53_beanwatch68_v68files.tsv` | the 112 archived v68 games (file, BC side, opponent) |
| `scratchpad/s53_beanwatch68_v47sample.tsv` | 150 random archived v47 games (the ore-denial control) |
| `scratchpad/s53_beanwatch68_oursample.tsv` | 150 of our own v175-v177 games (the zero-ore control) |
| `scratchpad/s53_beanwatch68_replays/` | matches A and D, pulled read-only from the platform |
