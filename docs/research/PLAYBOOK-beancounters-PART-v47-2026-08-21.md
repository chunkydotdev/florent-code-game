# PLAYBOOK — Bean counters, the **v47** era: watched, round by round

**PART 1 OF 2.** This part covers **v47** (their incumbent 2026-08-16T19:30Z ..
2026-08-21T04:12:59Z). A sibling agent covers **v68** (the line that replaced it
at 07:12:59Z on 2026-08-21). A merge pass follows, so every section below is
written to stand alone and every claim carries its own anchors.

**Commissioned:** 2026-08-21 by Magnus, who asked for maximum detail — *"The
more detailed we can do it the better."* The banked statistical study
(`docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md`) already says
*what they do on average*. **This document is what statistics cannot show: the
actual play, watched.** Its numbers are cited from that study, not re-derived,
except where a cell is per-game and had to be decoded here.

**Team:** `Bean counters`, id `47803c19-e264-4492-bd62-fbdd58cfd7e6`, rank 1.
**Agent:** s53 deep-watch replay agent, read-only except this file.
**Repo HEAD at watch start:** `ef0a2e8c5` (2026-08-21T17:35:26+02:00);
**at watch end:** `c953ccabe` — another lane committed while this ran, so the
tree moved underneath it. Nothing in this document depends on repo state.
Watch started 2026-08-21T15:40:21Z, finished 2026-08-21T16:1xZ (`date -u`,
in-shell). **Corpus denominator:** the same frozen v47 set the base study used
(1,235 archived games), read from `replay_archive/` via `corpus/meta_join.tsv`;
the keeper daemon appends while a study runs, so counts here will not reproduce
exactly against a later `meta_join`.

**Labelling, per house rules:** **MEASURED** = decoded off the replay bytes by
the instruments named in §0. **EYEBALL** = read off a rendered tape by a human
(me) without a control. **INFERENCE** = a causal sentence. Refuted guesses are
retained, struck through in prose but never deleted.

---

## THE SHORT VERSION

**What v47 actually is, watched:** four builders spawned in the first four
rounds and never a fifth, split into four fixed jobs that run in parallel for
the whole game — a **siege engineer** that walks to your core at round 0 and
spends the game standing on your eight ring tiles, a **raider** that chews your
harvesters ten attacks at a time, a **nest builder** that plants sentinels in
the band your gunners cannot reach, and a **home economist** that lays the belt
and then repairs it. In the median game **one single builder places every
barrier on your ring** and another **never comes near you at all**.

**The five things I did not know before watching:**

1. **The cage has no trigger.** The siege engineer leaves home on round 0 and
   builds its first barrier on `walk distance + 1` — round 11 in the fastest
   game, exactly the number of tiles it walked. There is nothing to bait.
2. **Kill a harvester, lose the ore.** They barrier the ore tile within three
   rounds **80.3% of the time** — against a **1.0% placebo** on a different ore
   tile in the same window. A temporary kill becomes permanent denial.
3. **Your own ring collar is not cover.** **92.6% of their 45,262 sentinel
   shots land on an enemy core footprint tile, and 46.5% of those are fired
   straight through one of your own buildings.** Collaring your ring delays
   their *barriers* by 20–30 rounds; it does nothing to their *guns*.
4. **Their seal leaks and they cut the hole themselves.** 4,323 of their ring
   barriers vanish with no enemy attack on them — their own builder cannot
   stand on a tile it has sealed. **The league retakes 0.8% of those openings.
   That is 3.5 free reopenings per game that nobody takes.**
5. **The ammunition drip is a live read-out of their turret inventory.** They
   convert exactly the next shots' cost — `4` per gunner, `10` per sentinel —
   and **98.0% of 69,417 conversions fit that lattice**, against the field's
   78.1%. A long silence on the wire means nothing of theirs can shoot.

**How Pivot beat them 0-5 on the rated ladder, in one sentence:** Pivot planted
**one 20 Ti gunner on Bean counters' delivery face at round 60**; it fired **94
shots at two conveyor tiles** and lived 98 rounds; Bean counters **rebuilt one
of those tiles sixteen times, fired 70 shots in the entire game to Pivot's 201,
and finished with two live home gunners, 12 banked ammunition and a core at
−15 HP.** Their `titanium_collected` was frozen at 1,480 for the last 128
rounds while four harvesters and eighteen conveyors sat alive on a severed belt.
**Their kill chain is economy → ammunition → turrets, and they have a repair
loop for a shot belt but no removal loop for the thing shooting it.**

**And the fact that reframes the whole siege:** in that game their sentinels
landed **630 damage on Pivot's core, taking it to 74/500 at round 161** — and
Pivot **healed exactly 630 back in 158 heal actions**, while Bean counters
healed their own core **zero times**. Repair is **0.25 Ti per hit point**;
a sentinel shot is **0.56**. **Defence is 2.2× cheaper than offence per HP —
but only after you have suppressed the turrets, which is what Pivot actually
did (median forward-turret life against them: 7 rounds).**

---

## 0. INSTRUMENTS, AND THEIR GUARDS

Two probes were written for this watch, both read-only, both prefixed
`s53_beanwatch47_`:

| file | what it does |
|---|---|
| `scratchpad/s53_beanwatch47_tape.py` | decodes one `.replay26` into a per-round event tape: builds (kind/team/tile/facing/**which builder built it**, via `BuilderBuild` field 16 matched to the round's `placeEntity`), deaths (with age), builder moves, `builderAttack`(13)/`builderHeal`(15) with target-owner classification, `coreConvertAmmo`(14), `fireTurret`(12) with shooter resolved by tile, `updatePlayers`(6) titanium/ammo/collected, core HP deltas, and an **8-tile ring occupancy snapshot for both cores every round** |
| `scratchpad/s53_beanwatch47_watch.py` | renders that tape as a narrative: ASCII map, turret ledger, ammo series, ring timeline, per-builder role trace, full round tape |

Neither hand-rolls the wire format: both import `fields` / `read_pos` /
`parse_entity` / `scalars` / `parse_update_hp` from `tools/replay_census.py`,
per `docs/research/corpus-howto.md`'s "ask it, don't rebuild it".

**GUARD SUITE — `scratchpad/s53_beanwatch47_guard.py`, run per game, each guard
with a complement that MUST come out the other way.**

* **GUARD A — build attribution.** Every build must be attributable to a builder
  id *except* core spawns, which emit no `BuilderBuild`. On the reference game
  the unattributed set is `{builder_bot: 12}` and the attributed set is
  `{conveyor 72, gunner 20, harvester 15, barrier 14, sentinel 5}` — i.e. the
  residual is exactly the 4+8 core spawns and nothing else. **PASS.** (A decoder
  that mis-matched targets would leave conveyors unattributed too.)
* **GUARD B — geometry, end to end.** `DistributeResources` moves landing on a
  core footprint × 10 must equal that team's final `Player.titaniumCollected`
  (`tools/replay_schema.md:165`). Reference game: BC `1480 == 1480`, Pivot
  `3340 == 3340`. **Complement run:** the same count with the footprint
  deliberately shifted `(+5,+5)` returns `340 / 0` — i.e. the check *can* fail
  and does when the geometry is wrong. **PASS with a live complement.**
* **GUARD C — mirror.** Every per-side counter is produced by one code path with
  the team index swapped, and the known asymmetries must flip. Reference game:
  builder attacks on enemy harvesters BC **396** vs Pivot **24**; the study's
  pooled figure is BC 128.7 vs opponents 18.9 (§3.6) — same direction, same
  order. **PASS.**

**What the instrument does NOT see.** `print()`/`BotOutput.stdout` is stripped
from platform replays (CLAUDE.md, s28 correction), so no arm tag, no internal
state flag, no target list is readable. **Every "trigger" in this document is
therefore an INFERENCE from engine-side facts — position, round, event order —
and is labelled as such.** Cooldowns are in the tape (fields 7/8) but were not
consumed; damage attribution per source is deliberately absent
(`corpus-howto.md` §"What this does NOT give you").

---

## 1. THE GAME SLATE

Five games watched at decode level. Every one carries its replay path and a
ready-to-run viewer line. `tools/replay_view.py` writes an HTML page and prints
the path; it never opens a browser, and **it is explicitly not an instrument** —
its own docstring says so — so nothing below is cited from it, it is only for
Magnus to watch along.

| tag | match / game | fixture | BC ver | opponent | map | result | why on the slate |
|---|---|---|---|---|---|---|---|
| **G-A** | `02c59670-…` g1 | **RATED ladder** 03:32:59.724Z | v47 | Pivot v236 | *(§4)* | **BC core destroyed** | the 0-5 loss — where the doctrine cracks |
| **G-B** | `02c59670-…` g3 | RATED, same match | v47 | Pivot v236 | *(§4)* | **BC core destroyed** | the longest fight of the five — recovery attempts |
| **G-C** | `4c901c39-…` g4 | unrated, 2026-08-18T17:30:40Z | v47 | **OpenSverige v162 (us)** | 20×20 | BC kill r138 | what they do to **us**, tile by tile |
| **G-D** | `3bf73ae7-…` g3 | unrated | v47 | Part-timers | 20×20 | **BC kill r60** | their **fastest** kill in 1,235 games |
| **G-E** | `9ee3a878-…` g3 | unrated | v47 | 0033 | 30×30 | BC kill r102 | full strangle arc, big map, strong opponent |

**⚠ SUBSTITUTION, MARKED EXPLICITLY as the commission requires.** The commission
asked for *"their fastest-killing available opponent cell as the closest-to-rush
proxy"* and noted that **no rush-era cell exists** — their non-adgato games are
all v23, pre-rush. **G-D is that substitution.** It is the fastest cell available
in the v47 archive (Part-timers, median kill round **121**, n=344 BC kill-wins;
minimum **60**), and it is *not* a rush: it is the same strangle doctrine
executed against an opponent that builds **0.05 barriers/game and never seals**
(study §4.3). **Read G-D as "the doctrine with no friction", not as "their rush".**

The Pivot rated match `02c59670-cc8c-4528-a4ec-09ab0f85a0da` was **not in the
archive** (checked: 0 hits in 103,197 files, 0 rows in `meta_join.tsv`). Pulled
read-only with `fcode match replay` at 2026-08-21T15:37Z into
`scratchpad/s53_beanwatch47_replays/`, **not** into `replay_archive/`, so the
keeper daemon's ledger is untouched. Noted per the commission.

*(Sections 2–5 are the games, watched. §6 turns what they showed into measured,
mirrored, control-guarded counters over all 1,235 v47 games. §7–§9 are roles,
the scheme, and the counter notes. §10 is how to watch along.)*

---

## 2. G-D — THE DOCTRINE WITH NO FRICTION (their fastest kill, r60)

**Replay:** `replay_archive/3bf73ae7-2da3-4dc3-bd2b-5ce265d702a2_game_3.replay26`
**Watch along:**
```
.venv/bin/python tools/replay_view.py replay_archive/3bf73ae7-2da3-4dc3-bd2b-5ce265d702a2_game_3.replay26
```
BC = **team 1**, core NW `(16,9)`. Part-timers = team 0, core NW `(2,9)`.
20×20, core-to-core d² = 196 (14 tiles of pure x). Ends **r59, `core_destroyed`,
Part-timers' core at −4 HP.** This is the fastest of 834 v47 core-kills.

**⚠ It is on the slate as the rush-proxy SUBSTITUTION** (§1). Part-timers is the
control-case opponent — 0.05 barriers a game, never seals (study §4.3) — so what
you are watching is **the doctrine running with the friction removed**, not a
different, faster doctrine. Every phase below appears in the harder games too;
it just takes three times as long.

### 2.1 The map, and why the whole game is one row

```
    01234567890123456789
  0 %%%%............%%%%
  4 ....o..........o....
  9 ..PP..o.oooo.o..AA..     <- both cores sit on rows 9-10; the ore is BETWEEN them
 10 ..PP..o.oooo.o..AA..
 14 ...o....%%%%...o....
 19 %%%%............%%%%
```
`A` = Bean counters' core, `P` = the victim's, `o` = ore.

### 2.2 The opening is four spawns and nothing else — r0..r3

| round | BC action |
|---|---|
| r0 | spawn **bot4** at `(15,10)` |
| r1 | spawn **bot6** at `(15,9)` |
| r2 | spawn **bot8** at `(16,11)`; first conveyor `(14,9)` facing **E** |
| r3 | spawn **bot11** at `(15,10)` |

Four builders in four rounds and **never a fifth** — the study's 4.4
builders/game (§3.3), watched. Note the spawn tiles: `(15,10)`, `(15,9)` and
`(16,11)` are three of BC's own eight ring tiles, and `(15,9)`/`(15,10)` are the
**west** pair, i.e. the pair facing the enemy.

**The belt is laid pointing INTO the core, from the outside in.** `(14,9)` E is
built at r2 — before `(15,9)` E at r4, which is the ring tile that actually
touches the core. **MEASURED, this game:** conveyor facings at r2/r4/r5/r8 are
`E,E,N,N` and every one of them points at the next tile in a chain that
terminates on the core footprint. Nothing is ever built facing away.

### 2.3 The cage — and the first tile is chosen before the game starts

**bot4 does not build anything for eleven rounds.** It spawns at `(15,10)` at
r0 and walks. Its first act of the game, at **r11**, is a **barrier on
`(4,10)`** — a ring tile of the *enemy* core, 11 tiles from where it was born.

**The arithmetic is exact.** To build on `(4,10)` a builder must stand
orthogonally adjacent, i.e. on `(5,10)`. From `(15,10)` that is 10 cardinal
steps; moving one tile per round in r1..r10 puts it on `(5,10)` at the end of
r10, and it builds at r11. **First cage round = walk distance + 1, to the
round.**

⇒ **INFERENCE, and it is the most important structural claim in this section:
the cage has NO STIMULUS. It is not triggered by anything the victim does.** It
is scheduled at spawn, and the round it lands is a pure function of map
geometry. There is no reactive branch to bait, no threshold to stay under. The
only things that move the start round are *distance* and *whether the tile is
already occupied* (§4.3 shows what happens when it is).

**The ring, with build rounds per tile.** Victim core NW `(2,9)`; footprint
`{(2,9),(3,9),(2,10),(3,10)}`. Ring tiles are numbered here clockwise from the
NW-of-north tile — this numbering is used for every game in this document:

```
              idx0        idx1
              (2,8)       (3,8)
              r44 #       r32 #
        +-------------------------+
 idx7   |                         |   idx2
 (1,9)  |   [2,9]        [3,9]    |   (4,9)
 r47 #  |                         |   r13 #
        |                         |
 idx6   |   [2,10]       [3,10]   |   idx3
 (1,10) |                         |   (4,10)
  never |                         |   r11 #   <-- FIRST
        +-------------------------+
              (2,11)      (3,11)
              idx5        idx4
              never       never
                                        BC's core lies EAST, at (16,9)
```

**Build order: `(4,10)` r11 → `(4,9)` r13 → `(3,8)` r32 → `(2,8)` r44 →
`(1,9)` r47.** Five of eight, and the game ended before the rest.

Read against the victim's **belt entry point**, which is the thing the
commission asked for: the victim's own delivery conveyors stood on `idx0
(2,8)` and `idx1 (3,8)` — its **north** face — from r13. **BC did not go
there first.** It took the two tiles of the **east** face, the face pointing at
its own core, because those were **empty**. The victim's belt-entry tiles were
taken **third and fourth, and only by eviction** (§2.4).

⇒ **The rule, stated as watched: BC takes the nearest EMPTY ring tile first, and
comes back for the occupied ones later.** Cross-game confirmation and the
honest limit on it are in §6.3.

### 2.4 Eviction — the tourniquet tightening, and it is a metronome

The victim's conveyor on `idx1 (3,8)` is a 20 HP building. A builder attack does
2 damage for 2 Ti. **Watched:**

```
r16 r17 r18 r19   atk (3,8)      ]
r20 r21 ... r25   [interrupted]   > 10 attacks total = 20 damage
r26 r27 r28 r29 r30 r31  atk (3,8) ]
r31   the conveyor DIES
r32   BARRIER planted on (3,8)          <- +1 round
```
and again, without the interruption:
```
r34 .. r43  atk (2,8)  (10 consecutive attacks, 2 dmg each)
r43   the conveyor DIES
r44   BARRIER planted on (2,8)          <- +1 round
```

**Two for two at exactly one round.** Cross-game this is **MEASURED at 67.4% of
2,699 evictions capped within 3 rounds, mean latency 1.08 rounds** (§6.2) —
against the field's 38.6% at 1.50.

**The interrupt at r20–r25 is worth naming**, because it is the only thing that
ever stopped the melee: at r20 bot6 planted a sentinel on `(8,9)` and at **r21
destroyed its own sentinel and put a barrier on the same tile.** `(8,9)` is an
**ore** tile. **EYEBALL: they mis-sited a turret onto ore and corrected it one
round later, for free** (`destroy` costs nothing and has no cooldown). It cost
them a turret's worth of titanium and six rounds of cage melee.

### 2.5 The nest — barriers first, then the guns, in the band a gunner cannot answer

```
r26  barrier (4,15)
r29  barrier (3,14)
r30  SENTINEL (2,15) facing NORTH   d2 to victim core = 36 (nearest footprint tile (2,10): 25)
r32  SENTINEL (3,15) facing NORTH   d2 to nearest footprint tile (3,10): 25
```

**Both sentinels sit at d² = 25 from the tile they are shooting.** Gunner attack
radius is r²=13; sentinel is r²=32. **25 is inside a sentinel's reach and
outside every gunner's** — the study's median v47 sentinel distance is exactly
25 (§3.5) and here you can watch it being chosen.

**The barriers come BEFORE the guns, and `(3,14)` sits directly NORTH of the
sentinel at `(3,15)` — i.e. inside its own firing line.** That only works
because **a sentinel's line ignores obstacles**. A gunner nest built this way
would shoot its own wall. **INFERENCE: the barrier shell is deliberate, and it
is priced on a rule that applies to sentinels only.**

### 2.6 The kill — 28 shots, and an ammunition policy that holds nothing

From r31 the two sentinels alternate onto `(2,10)` and `(3,10)`, both core
footprint tiles, **18 damage a shot**. Core HP 500 → **−4 at r59**. `500 − 18×28
= −4`: **exactly 28 sentinel shots, no other damage source touched that core.**

The ammunition series, verbatim (**MEASURED**, `CoreConvertAmmo` events):

```
r21:10  r31:10  r32:10  r34:30  r38:30  r40:20  r43:30  r47:30
r49:20  r51:20  r52:20  r54:20  r56:20  r58:20        14 calls, 290 Ti
```

Note what it is not: there is no opening bank, no reserve, no round number at
which they "switch to ammo". **The first call is r21 — the round they first put
a sentinel on the board — and from r49 it is a flat `20 every two rounds`,
which is exactly two sentinels × 10 ammo firing on a reload-2 cadence.** Their
ammo balance oscillates between 0 and 30 for the whole game.

**Contrast the victim:** Part-timers converted **92 Ti in a single call at r0**
and never converted again, and never fired a shot.

### 2.7 Ore capping — kill the harvester, then take the tile away for good

```
r23 .. r44   bot6 attacks the victim's harvester on (6,10)  [ore]
r45          the harvester DIES
r45          BARRIER planted on (6,10) — the SAME ROUND
```
A barrier on an ore tile makes `can_build_harvester` false there forever (short
of destroying the barrier). **This converts a temporary kill into permanent
denial**, and it is not in the banked study. Cross-game: **BC caps 80.3% of the
2,862 enemy harvesters it kills on ore, against the field's 43.8% in the same
games** (§6.1).

### 2.8 Who did what — the four builders, traced

| bot | spawn | builds | attacks | where it lived |
|---|---|---|---|---|
| **bot4** | r0 `(15,10)` | **5 barriers, ALL on the enemy ring. Zero conveyors, zero harvesters, zero turrets.** | 18 on enemy ring conveyors, 6 on an enemy harvester | action centroid **d²=1 from the victim's core** |
| **bot6** | r1 `(15,9)` | 5 conveyors, 2 harvesters, 1 (aborted) sentinel, 1 barrier | **22 on enemy harvesters**, 8 on enemy conveyors | centroid `(7.7,10.0)` — mid-map |
| **bot8** | r2 `(16,11)` | 2 harvesters, 4 conveyors, **3 barriers + 2 sentinels = the nest** | 4+3 | centroid `(8.8,12.4)` — the south lane to the nest |
| **bot11** | r3 `(15,10)` | **10 conveyors, 2 harvesters** — the home belt | 10 on enemy harvesters (after r50) | centroid `(15.1,7.6)`, **d²=173 from the victim** |

**Four builders, four jobs, and they do not swap while all four are alive:**
siege engineer, raider, nest builder, home economist. The home economist
converts to raider once the belt is finished (r50+). Cross-game evidence that
this is doctrine rather than one game's accident is in §7.


---

## 3. G-E — THE FULL ARC AGAINST A REAL ECONOMY (0033, 30×30, kill r102)

**Replay:** `replay_archive/9ee3a878-7909-4772-ba8c-e521fb5408c2_game_3.replay26`
**Watch along:**
```
.venv/bin/python tools/replay_view.py replay_archive/9ee3a878-7909-4772-ba8c-e521fb5408c2_game_3.replay26
```
BC = **team 0**, core NW `(2,14)`. 0033 = team 1, core NW `(26,14)`. 30×30,
core-to-core d² = **576** (24 tiles). Ends r102, `core_destroyed`.

This is the doctrine against an opponent that **collars its own core**: by r25
0033 holds **all eight** of its own ring tiles with its own conveyors
(`[cccccccc]` in the ring timeline). Watch what that costs Bean counters.

### 3.1 The cage becomes a siege — and it never lands

BC cannot place a barrier on an occupied tile, so bot12 (the siege engineer)
has to evict first. The whole cage effort of this game is **two tiles**:

```
r28..r37   bot12 attacks 0033's ring conveyor on (25,14)   10 attacks
r37        it dies
r38        BARRIER on (25,14)                              <- +1 round
r40..r49   bot12 attacks 0033's ring conveyor on (25,15)   10 attacks
r49        it dies
r50        BARRIER on (25,15)                              <- +1 round
```
`(25,14)` and `(25,15)` are the **west** face — the face pointing at BC's own
core. Same rule as G-D: nearest face first. **Maximum simultaneous hold: 2 of
8.** Against Part-timers they had 5 of 8 by r47.

**The seal then falls apart, and BC breaks it themselves.** The ring timeline
oscillates 2 → 1 → 2 → 1 → 0 → 1 → 0 → 1 over r50–r60. Traced to the event:

```
r50  BC barrier (25,15) built by bot12
r52  BC barrier (25,15) DIES, and bot12 MOVES (24,15) -> (25,15) the same round
r53  bot12 moves (25,15) -> (24,15)
r54  BC rebuilds the barrier on (25,15)
r55  BC destroys it again, bot12 moves onto (25,15)
r56  BC destroys its own (25,14) barrier, bot12 moves onto (25,14)
r57  BC rebuilds (25,15)
r59  BC destroys (25,15) again, bot12 moves onto it
r60  0033 REBUILDS ITS OWN CONVEYOR ON (25,15)   <- the victim retakes the tile
     BC rebuilds the barrier on (25,14)
```

⇒ **MEASURED, and confirmed at population scale: Bean counters' own siege
builder demolishes its own seal to walk through it.** A builder bot cannot stand
on a tile holding a building, including its own, so the tile it most wants to
stand on is the tile it just sealed. Across 1,235 v47 games (§6.5): **4,323 of
BC's ring barriers disappear without any enemy attack or shot on them, against
1,506 that are actually killed — i.e. 74% of BC's own seal-tile losses are
self-inflicted.**

### 3.2 The nest — and this time the guns walk right up to the core

```
r51  SENTINEL (24,14) facing EAST   d2 to nearest enemy core tile (26,14) = 4
r65  SENTINEL (26,10) facing SOUTH  d2 to nearest enemy core tile (26,14) = 16
```
Both are inside a defending gunner's r²=13 at the first one, and both shoot
**straight through 0033's own ring collar** — `(25,14)` and `(26,13)` are
occupied for most of the game and the sentinel line ignores them.

⇒ **This is the fact that makes the whole doctrine work, and it is measured at
scale (§6.4): 92.6% of all 45,262 v47 sentinel shots land on an enemy CORE
footprint tile, and 46.5% of those were fired through at least one enemy
building standing on the same line.** A ring collar of your own conveyors stops
their *barriers*; it does not stop their *sentinels*. **It is not cover.**

### 3.3 The gunner that could not let go — 38 rounds on one target

```
r22  0033 plants a SENTINEL on (11,14) facing SW  (mid-map, d2=225 from its own core)
r23  BC plants a GUNNER on (11,15) — orthogonally adjacent, facing NORTH, straight at it
r24  BC's gunner fires at (11,14).  It then fires at (11,14) on EVERY round
     from r24 to r61 inclusive — 38 consecutive rounds.
     0033 heals that sentinel TWICE per round (2 x 4 = 8 HP) against 7 damage.
r58  0033's titanium hits 0.  The heals stop.
r61  the sentinel finally dies.
```

**The answer verb is real and it is fast — 1 round from plant to counter-plant,
1 round more to first shot.** Cross-game it is **mean 1.18 rounds and it kills
the answered turret within 15 rounds 87.2% of the time** (§6.6). But note what
it cost here: **38 rounds × 4 ammo = 152 Ti of ammunition converted at exactly
4 Ti a round, to kill one turret that was being out-healed by 1 HP a round.**
BC never rotated that gunner and never gave up on the target.

**MEASURED at scale (§6.7): 407 of BC's 468 turret fire-runs of ≥10 consecutive
rounds on one tile (87.0%) are against a target its owner is healing** — against
329 of 1,119 (29.4%) for their opponents in the same games.

### 3.4 The ammunition drip, in its purest form

This game shows the rule that G-D only hinted at. **MEASURED**, verbatim:

```
r24 .. r51   4 Ti EVERY ROUND, 28 calls in a row      <- one gunner alive, reload 1
r52 .. r62   14 / 14 / 4 / 14 / 4 / 14 / 4 / 14 / 4   <- gunner + one sentinel (reload 2)
r63, r65     10, 10
r68 .. r100  20 every 2-4 rounds                      <- two sentinels
                                                          55 calls, 516 Ti
```
`4 = one gunner shot. 10 = one sentinel shot. 14 = 4+10. 20 = 10+10.`
**The amount converted is the exact ammunition cost of the shots the live
turrets are about to fire, and nothing more.** Their balance never accumulates.

**Cross-game (§6.8): of 69,417 v47 `convert_ammo` calls, only 1,371 — 2.0% —
are an amount that does not fit `4×live_gunners + 10×live_sentinels` or one of
its parts. Their opponents in the same games miss the lattice on 21.9% of
60,498 calls.** ⇒ **The convert series is a live read-out of their turret
inventory.** A `4` means one gunner, a `14` means a gunner and a sentinel, a
`0` for many rounds means they have nothing that can shoot.

### 3.5 Ore capping again

```
r31..r44   BC attacks 0033's harvester on (18,15)  [ore]
r45        it dies
r46        BARRIER on (18,15)          <- +1 round
r50        BARRIER on (18,14)          <- the neighbouring ore tile, unprompted
```

### 3.6 The builders

| bot | spawn tile | job |
|---|---|---|
| **bot12** | r3 `(4,14)` — BC's own ring tile **facing the enemy** | **siege engineer.** Its action centroid is d²=1 from 0033's core for rounds 0-49. 22 attacks on enemy conveyors, 6 barriers, 1 sentinel |
| **bot3** | r0 `(3,16)` | home gunner + raider, then **joins the siege** (centroid d²=1 from the enemy core in r50-99, 32 attacks on enemy conveyors) |
| **bot5** | r1 `(2,16)` | home belt (9 conveyors, 2 harvesters) → **forward nest** (sentinel `(26,10)`, barrier) + 14 attacks on enemy harvesters |
| **bot8** | r2 `(3,16)` | **stays home for the whole game** — 9 conveyors, 1 harvester, then **14 heals on BC's own conveyors** from r50. Its centroid never leaves d²>537 from the enemy |

**One builder is a dedicated home repairman.** That is the entire content of the
study's "heals on own buildings 20.6/game" (§3.6) — it is one bot, from about
r50, walking its own belt.

---

## 4. G-C — WHAT THEY DO TO **US**, TILE BY TILE (our v162, kill r138)

**Replay:** `replay_archive/4c901c39-79dd-45dc-a5ae-06db6f5e3a25_game_4.replay26`
**Watch along:**
```
.venv/bin/python tools/replay_view.py replay_archive/4c901c39-79dd-45dc-a5ae-06db6f5e3a25_game_4.replay26
```
BC = **team 1**, core NW `(9,17)`. **OpenSverige v162 = team 0**, core NW
`(9,1)`. 20×20, core-to-core d² = 256. **Our core dies at r137.** This is game 4
of the 5-0 on 2026-08-18; we have played their v47 twice and their v68 once and
lost **0 of 15 games** (study §2, premise correction 2).

### 4.1 r5 — they shoot our forward launcher off the board before it acts

```
r1   WE plant a launcher on (10,4)    d2=10 from OUR core   (home)
r3   WE plant a launcher on (9,10)    - we destroy it ourselves at r4
r5   WE plant a launcher on (11,15)   d2=8 from THEIR core  (forward)
r5   THEY plant a GUNNER on (11,16) facing NORTH — the tile directly south
     of our launcher, aiming at it, IN THE SAME ROUND
r6,7,8,9,10   the gunner fires at (11,15) every round.  30 HP / 7 dmg = 5 shots.
r10  our forward launcher dies, age 5, having thrown nothing.
```

**Latency from our forward plant to their counter-plant: 0 rounds. To their
first shot: 1 round. To the kill: 5 rounds.** This is the verb behind the
study's 79.7% forward-turret removal rate (§3.6), watched at the tile level.

**INFERENCE, and the alternative is not excluded:** a same-round answer is
consistent with a reaction (their builder simply acts later in the round order)
and also with a pre-planned gunner that happened to land there. The 1-round
version in G-E (§3.3) and the population mean of 1.18 rounds (§6.6) make the
reactive reading much the more likely, but no replay can show the branch.

### 4.2 r29–r45 — they take the middle ore away from us

The four centre ore tiles are `(9,9) (10,9) (9,10) (10,10)`.

```
r29  BARRIER on (9,9)     <- contested centre ore, no harvester there, nobody's yet
r32  BARRIER on (10,10)
r38  our harvester on (6,7) [ore] dies to their melee
r39  BARRIER on (6,7)                       <- +1 round, ore capped
r60  BARRIER on (10,9)
```
and then, once the game is theirs:
```
r80  they build their OWN harvester on (9,10)
r89  they DESTROY their own barrier on (9,9) and build a HARVESTER on it
r102 they DESTROY their own barrier on (10,9) and build a HARVESTER on it
```
⇒ **The centre-ore barriers are a land-grab, not just denial: they hold the
tile with 3 Ti of barrier until they have a spare builder-turn, then convert it
into their own 20 Ti harvester.** **EYEBALL** on the intent; **MEASURED** on the
sequence (rounds and tiles above).

### 4.3 r54–r100 — our own ring collar bought us 46 rounds, and they ground it off

We collared our own core: all 8 of our ring tiles held by our own conveyors by
**r54**. Their first barrier on our ring did not land until **r100** — against
**r11** on Part-timers, who left theirs open.

Then the eviction metronome, on our ring, four times:

```
tile        melee window        dies    THEIR BARRIER
(8,2)       r91 .. r98          r99     r100     <- +1
(10,0)      r102 .. r110        r111    r112     <- +1
(9,0)       r114 .. r122        r123    r124     <- +1
(8,1)       r125 .. r133        r134    r135     <- +1
```
Ten builder attacks (2 damage each) per 20 HP conveyor, then a barrier the
next round. **Four for four at exactly one round.** Our ring, at the end:

```
              idx0        idx1
              (9,0)       (10,0)
              r124 #      r112 #
        +-------------------------+
 idx7   |                         |   idx2
 (8,1)  |   [9,1]        [10,1]   |   (11,1)
 r135 # |                         |   ours, shot dead r123
        |                         |
 idx6   |   [9,2]        [10,2]   |   idx3
 (8,2)  |                         |   (11,2)
 r100 # |                         |   ours, shot dead r120
        +-------------------------+
              (9,3)       (10,3)
              idx5        idx4
              ours, dead r116   ours, dead r109
                                     THEIR core lies SOUTH, at (9,17)
```
**Their first cage tile on us was `(8,2)` — the WEST face, not the south face
they were approaching from.** They took whichever tile their siege builder
could clear first. By r135 they held 4 of 8; every other ring tile was simply
empty, its conveyor shot away.

### 4.4 The kill — a sentinel through our own collar, and a gunner walking a ladder

```
r42   SENTINEL (10,7) facing N    d2 to our core = 37  -- killed r70, age 28
r81   SENTINEL (12,2) facing WEST d2 to our core = 10
r97   GUNNER   (11,3) facing SW   d2 to our core = 8
r118  SENTINEL (4,2)  facing EAST d2 to our core = 26
```

**The sentinel at `(12,2)` fires WEST at `(9,2)` — a core footprint tile —
from r90 onward.** The line from `(12,2)` runs `(11,2) → (10,2) → (9,2)`, and
**`(11,2)` held OUR OWN CONVEYOR until r120.** It shot straight through it for
thirty rounds. Our collar was not cover.

**The gunner at `(11,3)` is the more instructive one.** A gunner's shot *is*
blocked, so it eats its way in, and rotates when its line runs out:

| round | facing | what it shoots | what happens |
|---|---|---|---|
| r97 | **SW** | `(10,4)` — **our home launcher** | 5 shots, launcher dies **r102** (age 101) |
| r103 | SW | `(9,5)` — next thing on the line | dies r105 |
| **r106** | **SW→W** | `(10,3)` our ring conveyor | dies r109; then `(9,3)`, dies r116 |
| **r117** | **W→N** | `(11,2)` our ring conveyor | dies r120; then `(11,1)`, dies r123 |
| **r125** | **N→NW** | `(10,2)` — **OUR CORE**, 7 damage a round, to the end | |

**Rotation latency: 1–2 rounds after the current facing line empties (r105→r106,
r116→r117, r123→r125).** Three rotations, 30 Ti, and the ladder ends on our
core. **This is a targeting policy, not a wander: every rotation moves the
gunner one facing closer to the core and it never rotates away.**

### 4.5 The arithmetic of the last forty rounds — and our answer to it

From r98 to r137 we healed our own core **once per round, +4 HP for 1 Ti**,
40 times. Their incoming was, per two rounds, `18 (sentinel) + 18 (sentinel) +
7+7 (gunner)` ≈ **21.5 HP a round.** **Our repair covered 19% of it.**

Their ammunition series over the same window is the drip in its final form —
`24 / 4 / 24 / 4 / 24 …` alternating: `24 = 10+10+4` on the rounds both
sentinels reload, `4 = the gunner alone` in between. **58 calls, 608 Ti, and
they finished the game holding 90 Ti.**

Ours: **8 calls, 36 Ti, for the entire game.**


---

## 5. THE COLLAPSE — the RATED 0-5 against Pivot, watched round by round

**Match `02c59670-cc8c-4528-a4ec-09ab0f85a0da`, created 2026-08-21T03:32:59.724Z.
Bean counters v47 0 — 5 Pivot v236. Rating 2054.74 → −10.25.** This was v47's
**second-to-last day** as their incumbent; they shipped v64 at 04:32:59Z, an hour
later, and v68 by 07:12:59Z (study §2). ⚠ Not archived — pulled read-only for
this watch (§1).

Pivot is the opponent that hurts v47 most: **61.0% of 300 archived games end
with Bean counters' core destroyed** (study §4.3), and the fixture caveat there
is load-bearing — 300 games means Pivot has been *drilling* against them with
prototypes. What follows is the shape of the counter, not a claim about its
rated strength.

**Match shape, decoded (all five, `titanium_collected` from the final
`updatePlayers`, core HP from the HP ledger):**

| game | map | rounds | condition | BC collected | Pivot collected | BC core |
|---|---|---|---|---|---|---|
| **g1 (G-A)** | 30×30 | 329 | `core_destroyed` | 1,480 | 3,340 | **destroyed** |
| g2 | 20×20 | 1000 | `titanium_collected` | 10,780 | 13,390 | survived at **300/500** |
| **g3 (G-B)** | 20×26 | 450 | `core_destroyed` | 2,810 | 4,530 | **destroyed** |
| g4 | 30×30 | 221 | `core_destroyed` | 620 | 2,070 | **destroyed** |
| g5 | 30×30 | 160 | `core_destroyed` | 400 | 1,390 | **destroyed** |

**Four of five ended with Bean counters' core physically destroyed, and the
fifth was a r1000 tiebreak they also lost.** Pivot's core finished at **500/500
in all five games.** ⚠ That is the *final* number, not a damage claim: in g1
Bean counters' sentinels took it from 500 down to **284 by round 100** and Pivot
**healed all of it back** (the `+4` core heals are visible on almost every round
of the tape from r101). **The siege connected and was simply out-repaired.**

### 5.1 G-A, game 1 — belt amputation, and 269 rounds of not answering it

**Replay:** `scratchpad/s53_beanwatch47_replays/02c59670-…_game_1.replay26`
```
.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch47_replays/02c59670-cc8c-4528-a4ec-09ab0f85a0da_game_1.replay26
```
BC = team 0, core NW `(2,2)`. Pivot core NW `(26,26)`. 30×30, **core-to-core
d² = 1152 — corner to corner, the longest walk on the slate.**

**PHASE 1, r0–r75 — parity.** Both economies build out. At r75 BC leads on
collection 750 to 680 and holds 627 Ti. Nothing is wrong yet.

**PHASE 2, r39–r60 — Pivot starts putting gunners on Bean counters' doorstep,
and BC answers correctly.**

| round | Pivot plants | d² to BC's core | BC answers | outcome |
|---|---|---|---|---|
| r39 | gunner `(12,4)` | 104 | — | dies r46 (age 7) |
| r52 | gunner `(7,4)` | 29 | **r53 gunner `(5,4)` facing E** | dies r57 (age 5) |
| r54 | gunner `(7,1)` | 26 | **r55 gunner `(5,1)` facing E** | dies r59 (age 5) |
| **r60** | **gunner `(7,2)`** | **25** | r60 BC rotates `(5,4)` E→NE, which points at `(7,2)` | **lives 98 rounds** |

**The doorstep answer works twice and then stops working, and BC never notices.**

**PHASE 3, r62–r155 — the amputation.** Pivot's gunner on `(7,2)` fires
**86 times at `(5,2)` and 8 times at `(4,2)`** — and nothing else, ever. Those
two tiles are the conveyors carrying BC's south belt into `(4,2)`, which is one
of only **two** of its own eight ring tiles BC ever occupied.

**Bean counters rebuilt `(5,2)` SIXTEEN TIMES.** The cycle is visible in the
tape as a metronome — `BC-c(5,2)` at r78, r84, r90, r96, r102, r108 …,
`BC+c(5,2)/W` at r79, r85, r91, r97, r103, r109 … — **one rebuild per six
rounds, for tens of rounds, into a gun that never moved.**

⛔ **AND THE GUN WAS INSIDE THEIR OWN GUNNER'S REACH THE WHOLE TIME.**
`(7,2)` is d² = 8 from BC's gunner at `(5,4)` and d² = 5 from its gunner at
`(5,1)` — both well inside r²=13. BC **rotated `(5,4)` to face it at r60** and
then **fired zero shots from it for the remaining 269 rounds.**

**MEASURED, the whole-game fire ledger:**
* **Bean counters' total turret fire, all turrets, all 329 rounds: 70 shots.
  Pivot's: 201.**  Bean counters' two home gunners account for **15** of the 70,
  all of them before r78.
* **Pivot's gunner on `(7,2)` alone fired 94 — more than Bean counters' entire
  team, all game.**
* BC finished the game with **both home gunners alive, 12 banked ammunition,
  and a core at −15 HP.**

**PHASE 4, r148–r189 — the belt dies and the rebuild loop gives up.** Once
`(4,2)` — the delivery face — falls at r148 and again at r155, Pivot's gunners
walk the chain outward: BC loses `(2,5)` r145, `(3,6)` r158, `(2,7)` r168,
`(2,9)` r177, `(2,8)` r181, `(3,8)` r184, `(4,8)` r187. BC rebuilds frantically
— `(1,6)`, `(1,7)`, `(0,7)`, `(0,6)` — each rebuild living 2–6 rounds. **After
r189 Bean counters never builds another conveyor for the remaining 140 rounds.**

**PHASE 5, r175–r328 — a live economy delivering nothing.**

| r | BC Ti | BC ammo | **BC collected** | BC harvesters | BC conveyors | Pivot collected |
|---|---|---|---|---|---|---|
| 150 | 131 | 22 | 1,450 | 4 | 19 | 1,420 |
| 175 | 21 | 12 | 1,470 | 4 | 20 | 1,670 |
| 200 | 10 | 12 | **1,480** | 4 | 18 | 1,920 |
| 250 | 2 | 12 | **1,480** | 2 | 18 | 2,420 |
| 300 | 8 | 12 | **1,480** | 2 | 18 | 2,960 |
| 328 | 6 | 12 | **1,480** | 2 | 18 | 3,340 |

**`titanium_collected` is frozen at 1,480 for 128 rounds while four harvesters
and eighteen conveyors sit alive on the board.** Their harvesters `(3,9)` and
`(2,11)` were not killed until r243 and r250 — they pumped into a severed belt
for ninety rounds. This is CLAUDE.md's *"a harvester with no route home is worth
zero on it, forever"*, playing out on the rank-1 bot.

**PHASE 6, r285–r328 — the execution.** With BC holding 0–11 Ti, Pivot plants a
sentinel on `(8,2)` (r285, fires at core tile `(3,2)` 22 times) and a gunner on
`(4,0)` (r294, fires at core tile `(2,2)` 17 times). `(4,0)` is **diagonally
adjacent to BC's still-living gunner on `(5,1)`.** A single `rotate(NW)` — 10 Ti
and one cooldown — would have put it first in that gunner's line. **BC never
rotated, and had 12 ammunition banked when its core died at r328.**

**⇒ THE COLLAPSE MECHANISM, stated plainly.** Bean counters lost this game to
**one 20 Ti gunner planted on their delivery face at round 60**. It was inside
their own home gunner's reach and inside their own builders' melee reach, and
they answered it with **sixteen rebuilds of the conveyor it was shooting** and
**zero shots**. The doctrine has a repair loop and a cage loop and a nest loop;
**it has no loop that says "the thing that keeps breaking my belt is a building
I could remove".**

### 5.2 G-B, game 3 — the recovery attempts, and why fourteen of them failed

**Replay:** `scratchpad/s53_beanwatch47_replays/02c59670-…_game_3.replay26`
```
.venv/bin/python tools/replay_view.py scratchpad/s53_beanwatch47_replays/02c59670-cc8c-4528-a4ec-09ab0f85a0da_game_3.replay26
```
BC = team 0, core NW `(9,6)`; Pivot `(9,18)`. 20×26, core-to-core d² = **144** —
the *closest* pair on the slate, and this is the longest game of it: **450
rounds.** This is the one to watch for the recovery attempts, because Bean
counters keeps trying for 400 rounds.

**The cage stalls at 4/8 and is then sealed shut by the victim.**
```
r49 (9,20) #     r52 (8,19) #     r56 (8,18) #     r59 (9,17) #      -> 4 of 8
r67  Pivot builds its OWN conveyor on (11,18)
r119 Pivot builds its OWN conveyor on (11,19)       -> [#cccc###], frozen for 331 rounds
```
**Pivot's counter to the cage is not to break it — it is to occupy the rest of
its own ring first.** From r119 to the end, neither side moves a ring tile.
*(And the mirror: Pivot never puts a single building on Bean counters' ring in
450 rounds — 0/8, all game. Pivot does not cage. It guns.)*

**Fourteen recovery attempts, thirteen deaths, median life 7 rounds.** Every one
is answered by an adjacent Pivot gunner, and the answers get faster as the game
goes on:

| BC plants | round | d² to Pivot's core | Pivot's answer | lag | BC turret dies |
|---|---|---|---|---|---|
| sentinel `(5,14)` | r60 | 32 | gunner `(6,13)` | **+9** | r76 (age 16) |
| sentinel `(10,13)` | r85 | 26 | gunner `(9,14)` facing NE | **+1** | r92 (age 7) |
| gunner `(12,5)` | r100 | *(home)* | Pivot gunner `(13,6)` already live since r79 | — | r107 (age 7) |
| gunner `(12,5)` **again** | r146 | *(home)* | — | — | survives; Pivot's `(13,6)` dies r147 |
| sentinel `(13,15)` | r172 | 25 | gunner `(12,15)` facing E | **+2** | r180 (age 8) |
| sentinel `(12,17)` | r243 | 10 | gunner `(11,16)` facing SE | **+0** | r249 (age 6) |
| gunner `(14,16)` | r252 | 29 | gunner `(13,16)` facing E | **+0** | r256 (age 4) |
| gunner `(11,16)` | r258 | 8 | gunner `(12,17)` facing NW | **+0** | r261 (age 3) |
| sentinel `(13,16)` | r269 | 20 | gunner `(14,16)` facing W | **+0** | r275 (age 6) |
| sentinel `(12,19)` | r285 | 10 | gunner `(11,20)` facing NE | **+2** | — |
| sentinel `(14,15)` | r316 | 34 | gunner `(13,15)` facing E | **+2** | r324 (age 8) |
| sentinel `(12,17)` | r331 | 10 | gunner `(12,16)` facing S | **+1** | r338 (age 7) |

**By r243 Pivot is answering in the SAME ROUND, five times in a row.** It is
Bean counters' own doorstep verb (§4.1) played back at them, and Pivot has an
edge on the trade: a 20 Ti gunner deletes a 30 Ti sentinel in 3–8 rounds.

⛔ **REFUTED IN PASSING — RETAINED.** Watching G-B I formed the hypothesis
*"they re-plant turrets onto tiles where their own turret just died — that is the
defect"*. It looks true here (`(12,5)` at r100 and again at r146; `(12,17)` at
r243 and again at r331). **It does not survive the population check: BC
re-plants on a tile where it already lost a turret 566 times in 1,235 games
(0.46/game), and their opponents in the same games do it 1,005 times
(0.81/game). BC does it LESS than the field.** The defect is not where they
re-plant; it is that they keep buying the same losing exchange (§5.3).

**Their economy dies the same way as in G-A, more slowly.** Harvesters alive: 6
at r225 → 4 at r275 → 2 at r325 → 1 at r350 → **0 from r375 to r450**.
`titanium_collected` freezes at **2,810 from r400**, with 36 conveyors still
standing. Final: BC 2,810 collected vs Pivot 4,530; BC 0 harvesters vs Pivot 8.

**And Pivot's endgame is four turrets on the doorstep in twenty-one rounds** —
sentinel `(14,6)` r417 (d²=25), gunner `(11,4)` r421 (d²=8), gunner `(10,3)`
r430 (d²=10), gunner `(8,4)` r438 (d²=5). **Bean counters' last turret of any
kind was planted at r331.**

### 5.3 What Pivot did that the doctrine could not answer — four things

1. **IT PUT GUNS ON THE BELT, NOT ON THE CORE.** 94 of Pivot's shots in G-A went
   into two conveyor tiles. Bean counters' entire kill chain is *economy → ammo
   → turrets*; severing the first link disarms the last one, and their code has
   no branch that treats a belt tile being shot as a *turret* problem.
2. **IT ANSWERED EVERY FORWARD TURRET ADJACENTLY, IN VOLUME, AND WON THE
   TRADE.** G-B: 32 Pivot turret plants against 14 BC plants; BC's median
   forward-turret life **7 rounds**. A 20 Ti gunner deleting a 30 Ti sentinel is
   a losing exchange, and BC repeated it fourteen times without changing
   anything about where or when it planted.
3. **IT OUT-HEALED THE SIEGE.** Pivot heals ~307 times a game on its own
   buildings (study §4.3) against Bean counters' 20.6. Every BC melee dose is
   ten builder-turns; every Pivot heal is one. **In G-E the same asymmetry pinned
   a BC gunner on one target for 38 rounds** (§3.3).
4. **IT DENIED THE CAGE BY OCCUPYING ITS OWN RING FIRST.** G-B r119: Pivot fills
   its four remaining ring tiles with its own conveyors and the seal is frozen
   at 4/8 for 331 rounds. Cross-game, the same move is worth **+27 rounds of
   delay** on the first cage build (§6.3).

**What Pivot did NOT do, and it matters: it never caged.** 0 of 8 on Bean
counters' ring across all 450 rounds of G-B. The counter-doctrine that beats
v47 in these games is **guns on the belt plus heals**, not a mirrored tourniquet.
*(O(1) and DinooniD do mirror the tourniquet and also beat them — study §4.3 —
so there are two working counters, and only one of them is on this slate.)*


### 5.4 The heal arithmetic — the exact reason the siege lost

**MEASURED on G-A, whole game, from the HP ledger and the heal events:**

```
Bean counters landed 35 sentinel shots on Pivot's core footprint  =  630 damage
Pivot healed its own core 158 times                               =  +630 HP, exactly
Pivot's core low point:  74 / 500,  at round 161
Bean counters healed their own core:  0 times, all game
```

**Their siege got a rank-2 opponent's core to 74 HP and then watched it go back
to 500.**

And the exchange rate is an **engine fact, not an inference** — a rules-level
arithmetic that no number of games overturns (CLAUDE.md point 6's carve-out):

| action | cost | effect | **Ti per HP** |
|---|---|---|---|
| `heal` (builder) | 1 Ti | +4 HP | **0.25** |
| sentinel shot | 10 ammo = 10 Ti (convert is 1:1) | 18 damage | **0.56** |
| gunner shot | 4 ammo = 4 Ti | 7 damage | **0.57** |

⇒ **Repairing a core is 2.2× cheaper per hit point than shooting one.** Pivot
undid 350 Ti of Bean counters' ammunition with 158 Ti of heals.

⚠ **The honest limit, and it is why this is not a free lunch.** Heal throughput
is capped by builder-turns: 4 HP per builder per round. Pivot's actual heal rate
in G-A was **0.48 heals a round** (158 over 329 rounds, max 3 in any one round)
— it only *matched* the incoming 1.9 HP/round because **Pivot had already killed
the turrets**, holding BC's whole-game output to 35 shots. In G-C, against three
live BC turrets doing ~21.5 HP a round, our own core repair ran at 6.7 HP/round
and covered less than a third. **The heal race is winnable only after turret
suppression, never instead of it.**

---

## 6. THE SMALL TACTICS CATALOG — watched, then measured across 1,235 games

Every row below was first *seen* in one of the five slate games and then counted
over the frozen v47 set (n = 1,235 archived games, 2026-08-16T19:30Z ..
2026-08-21T04:21Z). **Every counter is produced by one code path with the team
index swapped, so the "field" column is the same measurement on their opponents
in the same games.** Probes: `scratchpad/s53_beanwatch47_census.py`,
`…_census2.py`, `…_census3.py`, `…_orecap.py`, `…_roles.py`, `…_takeover.py`,
`…_collar.py`.

### 6.1 ORE CAPPING — kill the harvester, then barrier the tile

**Watched:** G-D r45, G-C r38→r39, G-E r45→r46 (all three games on the slate
that killed an enemy harvester on ore).

| | Bean counters v47 | their opponents, same games |
|---|---|---|
| enemy harvester deaths on an ore tile | 2,862 | 2,812 |
| **that tile barriered within 3 rounds** | **2,298 = 80.3%** | 1,231 = 43.8% |
| **PLACEBO — a *different* ore tile barriered in the same window** | **28 = 1.0%** | 4 = 0.1% |
| barriers they put on ore tiles with **no** preceding enemy harvester death | 6,178 | 587 |

**The placebo is the guard, and it works:** 80.3% against a 1.0% base rate, from
the identical code path. *(The 6,178 uncued ore barriers say the habit is
broader than the reaction — they barrier ore they simply do not want you to
have — but the reaction is real and it is 80× the base rate.)*

### 6.2 EVICTION — melee the ring tile clear, barrier it the next round

**Watched:** G-D (2/2 at +1 round), G-C (4/4 at +1 round), G-E (2/2 at +1 round).
The melee dose is **ten builder attacks** — 2 damage each against a 20 HP
conveyor — and it runs on consecutive rounds unless the bot is pulled away.

| | Bean counters v47 | field |
|---|---|---|
| enemy buildings dying off their own core's ring | 2,699 | 1,957 |
| **that tile barriered by the attacker within 3 rounds** | **1,819 = 67.4%** | 755 = 38.6% |
| **mean latency, death → barrier** | **1.08 rounds** | 1.50 rounds |

### 6.3 THE CAGE'S START IS GEOMETRY, NOT A TRIGGER

**Watched:** G-D — bot4 spawns r0 at `(15,10)`, walks ten tiles, builds the
first cage barrier at r11. `walk distance + 1`, exactly.

**The first ring tile they take:** n = 1,180 games with any ring build.
**99.4% of first cage tiles are a BARRIER** (1,173/1,180; 7 gunners). By face,
relative to the direction of their own core:

| | Bean counters | field |
|---|---|---|
| the face pointing at the attacker (APPROACH) | 542 (45.9%) | 421 (47.4%) |
| a side face (FLANK) | 607 (51.4%) | 373 (41.9%) |
| **the far face (OPPOSITE)** | **31 (2.6%)** | 95 (10.7%) |
| mean round of the first ring build | 49.9 | 47.1 |

⇒ **They essentially never start the cage on the far side of your core** — 2.6%.
Which of APPROACH/FLANK they pick is decided by **which tile is empty**.

**And that is the defensive lever, MEASURED with the distance confound
controlled.** Median round of Bean counters' *first* ring build, by how many of
its own eight ring tiles the victim was holding at round 30:

| victim's own ring tiles held @r30 | near (d²<150) | mid (150–350) | far (d²≥350) |
|---|---|---|---|
| 0 | r11 (n=25) | r20 (n=40) | r34 (n=84) |
| 1 | r4 (n=46) | r27 (n=59) | r41 (n=65) |
| 2 | r7 (n=54) | r29 (n=116) | r61 (n=200) |
| 3 | r10 (n=62) | r40 (n=124) | r51 (n=77) |
| 4 | r9 (n=32) | r41 (n=42) | r48 (n=75) |
| **5+** | **r26 (n=16)** | **r43 (n=31)** | **r65 (n=32)** |

and the price they pay for it, same cut: **median Bean-counters melee attacks on
the victim's ring tiles rises from 0 (ring empty) to 40–62 (ring occupied).**

⇒ **Occupying your own ring converts a free 3 Ti barrier into ~10 builder-turns
of melee per tile, and pushes their first cage build 20–30 rounds later.**
⚠ **Observational, not experimental** — a team that collars its own ring is also
a better team in other ways. The mechanism (the melee column) is the part that
is not confoundable.

### 6.4 THE SENTINEL SHOOTS THROUGH YOUR COLLAR

**Watched:** G-C — sentinel `(12,2)` facing W hits core tile `(9,2)` for thirty
rounds with our own conveyor standing on `(11,2)` in between. G-E — sentinel
`(24,14)` facing E hits `(26,14)` through 0033's ring conveyor on `(25,14)`.

| v47 sentinel fire | Bean counters | field |
|---|---|---|
| total sentinel shots | 45,262 | 14,579 |
| **shots landing on an enemy CORE footprint tile** | **41,911 = 92.6%** | 9,726 = 66.7% |
| shots passing through ≥1 **enemy** building on the same line | 20,533 = 45.4% | 4,724 = 32.4% |
| **core shots fired through enemy cover** | **19,493 = 46.5% of core shots** | 3,954 = 40.7% |

⇒ **Nine out of ten Bean counters sentinel shots are aimed at your core, and
nearly half of those are fired through something of yours.** A ring collar
blocks their barriers; **it is not cover.** Only killing the sentinel, or
denying the tile before it is planted, stops the damage.

### 6.5 THEIR SEAL LEAKS, AND THEY MAKE THE HOLE THEMSELVES

**Watched:** G-E r52–r60 — bot12 destroys its own barrier on `(25,15)`, steps
onto the tile, steps off, rebuilds; four times in eight rounds; on r60 the
victim rebuilt its own conveyor there in the gap.

| ring barriers the ATTACKER placed, and lost | Bean counters | field |
|---|---|---|
| killed by the defender (melee or fire) | 1,506 | 167 |
| **disappeared with no attack and no shot on them** | **4,323** | 66 |
| …of those, an own builder steps onto the tile within 1 round | 1,425 (33%) | 43 |
| …replaced by their own conveyor within 5 rounds | 2,524 (58%) | 1 |
| **…and the DEFENDER retook the tile within 5 rounds** | **34 = 0.8%** | 5 |

⇒ **74% of the seal tiles Bean counters lose, they demolish themselves** — a
builder cannot stand on a tile holding a building, including its own —
**and the field converts 0.8% of those 4,323 openings.** That is 3.5
uncontested reopenings of the seal per game, league-wide, going unused.

### 6.6 THE DOORSTEP ANSWER — how they clear a forward turret

**Watched:** G-C r5 (0-round lag, launcher dead in 5), G-E r22→r23 (1-round lag).

| | Bean counters | field |
|---|---|---|
| forward turrets planted against them (turret closer to the defender's core than to its own; launchers included) | 6,162 | 3,881 |
| **ever shot at by the defender** | **3,811 = 61.9%** | 1,639 = 42.2% |
| …**within 0–1 rounds of the plant** | 1,162 | 452 |
| mean rounds from plant to first shot at it | **12.6** | 15.8 |
| answered by a counter-turret on an **orthogonally adjacent tile** within 3 rounds | 344 | 291 |
| …mean lag of that counter-plant | **1.18 rounds** | 0.96 |
| …**and the answered turret dies within 15 rounds** | **300/344 = 87.2%** | 205/291 = 70.4% |

⇒ The study's 79.7%-vs-33.5% removal gap resolves into two separate verbs:
**(a) they shoot at 62% of what you plant against the field's 42%, and (b) when
they bother to plant a counter-turret next to it, it dies 87% of the time.**

### 6.7 THEY DO NOT LET GO OF A TARGET

**Watched:** G-E r24–r61 — one gunner, 38 consecutive rounds, one tile, a target
being healed for +8 a round against 7 damage. It only died when the victim's
titanium hit zero.

| runs of ≥10 consecutive rounds of one turret firing one tile | Bean counters | field |
|---|---|---|
| number of such runs | 468 | 1,119 |
| total rounds spent inside them | 11,780 | 24,356 |
| **…where the target was being HEALED during the run** | **407 = 87.0%** | 329 = 29.4% |

Their gunner rotation rate is **2.0 a game** (study §4.2), so a gunner that
acquires an un-killable target keeps it. ⚠ **Part of this split is a base-rate
artefact** — the teams they face heal ~140 times a game and they heal ~21
(study §3.6), so their targets are simply more likely to be healed. The
non-artefactual half is the **11,780 rounds** and the **2.0 rotations**.

### 6.8 THE AMMUNITION DRIP IS A READ-OUT OF THEIR TURRET INVENTORY

**Watched:** G-E `4 ×28 rounds → 14/4 alternating → 20 every 2` and G-C
`4 → 10 → 14/4 → 24/4`, each transition landing on the exact round a turret was
planted or lost.

| `convert_ammo` calls | Bean counters | field |
|---|---|---|
| calls | 69,417 | 60,498 |
| titanium converted | 654,974 (9.4 / call) | 488,934 (8.1 / call) |
| amount == `4·gunners + 10·sentinels` exactly | 18,067 (26.0%) | 27,421 (45.3%) |
| amount == one component of it (`4·g` or `10·s`) | 22,684 (32.7%) | 3,890 (6.4%) |
| an even amount under the full cost | 27,295 (39.3%) | 15,939 (26.3%) |
| **an amount that fits none of the above** | **1,371 = 2.0%** | 13,248 = 21.9% |

⇒ **98.0% of their conversions fit the turret-cost lattice.** A `4` on the wire
means one live gunner; a `14` means a gunner and a sentinel; a long silence
means **nothing of theirs can currently shoot.**

### 6.9 FORWARD-TURRET SURVIVAL — the gunner-proof band is worth +30% of a life

Turret lifetime in rounds, by d² from the turret to the nearest tile of the
**enemy** core footprint (v47 games; a turret alive at the end is credited with
the rounds it lived):

| placement | BC n | **BC median life** | field n | field median life |
|---|---|---|---|---|
| home side | 3,078 | **72** | 1,957 | 13 |
| **d² ≤ 13** (inside a defending gunner's reach) | 1,354 | **20** | 3,570 | 11 |
| **d² 14–32** (sentinel band, gunner-proof) | 2,192 | **26** | 1,106 | 15 |
| d² 33–64 | 261 | 17 | 590 | 10 |
| d² > 64 | 96 | 15 | 586 | 12 |

⇒ **The band doctrine is worth a measured +6 rounds of median life (20 → 26,
+30%)** — the first survival number this project has had on it. And the home
column is the ring-clearance advantage seen from the other side: **their home
turrets live 72 rounds against the field's 13, a 5.5× gap.**

### 6.10 THE BUILD/DESTROY THRASH — a real pathology, at a real rate

Tiles built on **five or more times by the same team in one game**:

| | Bean counters | field |
|---|---|---|
| such tiles, over 1,235 games | 639 (0.52 / game) | 221 (0.18 / game) |
| builds spent on them | 12,368 | 2,067 |
| of those tiles, on a core ring | 215 | 31 |
| of those tiles, alternating between **kinds** (barrier ↔ conveyor) | 130 | 42 |
| **worst single tile in one game** | **893 builds** | 111 |

**Watched:** G-A — `(5,2)` rebuilt **16 times** into a gunner that never moved
(§5.1). And in `008b7e55-…_game_5` a ring tile enters a **two-round barrier ↔
conveyor oscillation that runs from r379 past r407** — the seal subroutine and
the belt subroutine fighting over the same tile, each undoing the other, at
~6 Ti and one builder-turn per cycle.


---

## 7. PER-UNIT ROLES — the four builders, and what happens when one dies

### 7.1 They specialise, and it is not close

Four builders in the first four rounds, **4.38 a game over 1,235 games** against
their opponents' 5.81, and a fifth is essentially never spawned. Watched in
G-D (§2.8) and G-E (§3.6); measured over the whole set
(`scratchpad/s53_beanwatch47_roles.py`):

| | Bean counters | field |
|---|---|---|
| games with ≥4 barriers on the enemy ring | 924 | 225 |
| **share of those barriers placed by the SINGLE busiest builder — median** | **1.000** | 0.857 |
| …mean | 0.873 | 0.821 |
| **most-forward builder: share of its actions within d² ≤ 9 of the enemy core, median** | **0.848** | 0.667 |
| **least-forward builder: same share, median** | **0.000** | 0.000 |

⇒ **In the median Bean counters game, ONE builder places every single barrier on
your core ring, spends 85% of its actions inside d² ≤ 9 of your core, and never
touches the home economy. Another never comes near you at all.**

### 7.2 The four jobs, named

Read off G-D and G-E at the individual-bot level, and consistent in both:

| job | how to recognise it on the wire | G-D | G-E |
|---|---|---|---|
| **SIEGE ENGINEER** | builds *only* barriers; every barrier on your ring; melees the buildings standing on your ring; action centroid d² ≈ 1 from your core from ~r10 | bot4 (spawned **r0**) | bot12 (spawned **r3**) |
| **RAIDER** | melees your harvesters, 10 consecutive attacks per target; centroid mid-map | bot6 | bot3 (later bot5) |
| **NEST BUILDER** | builds the forward sentinels and the barriers that shell them; travels a flank lane | bot8 | bot5 |
| **HOME ECONOMIST / REPAIRMAN** | conveyors and harvesters only, then **heals its own belt**; never leaves home | bot11 | bot8 (14 own-conveyor heals from r50) |

**The siege engineer is identified by its SPAWN TILE, not by spawn order.** In
both games it is the bot spawned on the ring tile of Bean counters' own core
that faces the enemy — G-D `(15,10)` with the enemy due west; G-E `(4,14)` with
the enemy due east. **EYEBALL** across two games; the population version of the
claim (the 1.000 top-share above) is measured, the *spawn-tile* rule is not.

### 7.3 Killing the siege engineer — what it actually buys

The study's §3.8 says builders are replaced 91% of the time in a median 2
rounds and concludes *"kill their four builders"* is dead. **That is right about
the UNIT and wrong about the JOB**, and the distinction is worth a measured
number:

**MEASURED** (`scratchpad/s53_beanwatch47_takeover.py`): deaths of a Bean
counters builder that had already done ≥3 siege acts (a ring barrier, or a
melee on a building standing on the ring), n = **93** across 1,235 games:

| | Bean counters | field |
|---|---|---|
| siege-bot deaths | 93 (0.075 / game) | 105 |
| **the siege job is resumed at all** | 81 = **87.1%** | 48 = 45.7% |
| **median rounds until the next siege act** | **11** | 21 |
| mean / p90 | 18.2 / 45 | 34.2 / 82 |
| the successor is a **different** builder | **81 of 81** | 48 of 48 |
| the successor is a **newly spawned** builder | **3 of 81** | 18 of 48 |
| **the job is never resumed for the rest of the game** | **12 = 12.9%** | 57 = 54.3% |

⇒ **Killing the builder standing on your ring buys a median of 11 rounds of cage
progress and a 12.9% chance the cage stops permanently — and the replacement is
always one of the three survivors walking over, never a fresh spawn.** The
2-round replacement figure is about the *body*; the job takes eleven rounds
because someone has to walk there. ⚠ The siege bot dies only 0.075 times a game
unprompted, so this is a window you have to *make*, not one that arrives.

---

## 8. THE GRANDIOSE SCHEME — the strangle arc in phases

Assembled from the five slate games; the round boundaries are the medians and
anchors already cited, not a fitted model. **Phases run in parallel, not in
sequence** — that is the point of the four-way specialisation.

| phase | rounds (typical) | who | what | anchor |
|---|---|---|---|---|
| **P0 — LEVY** | r0–r3 | core | spawn exactly four builders, one per round, then stop forever | 4.38/game, study §3.3; G-D r0-r3 |
| **P1 — DEPART** | r0–r(d) | siege engineer | walks to your core the instant it is spawned, building nothing on the way. `d` = walk distance | G-D: 10 tiles, first act r11 |
| **P1′ — BELT** | r2–r40 | home economist (+ nest builder early) | conveyors laid outward-in, terminating on their own core; harvesters at median r5 | study §3.2; G-D r2/r4 |
| **P2 — CAGE OPENS** | median **r35** (mean r50) | siege engineer | first barrier on the nearest EMPTY tile of your 8-ring. 99.4% a barrier; 2.6% chance it is the far face | §6.3 |
| **P3 — RAID + ORE CAP** | r18 onward | raider | 10-attack doses on your harvesters; **80.3% of the ore tiles it clears get barriered within 3 rounds** | §6.1; G-D r23-r45 |
| **P4 — EVICT** | from ~r30 | siege engineer | 10-attack doses on whatever of yours stands on your own ring; barrier lands **1.08 rounds** after the corpse | §6.2; G-C r91-r135 |
| **P5 — NEST** | median **r50** first sentinel | nest builder | barriers first, then sentinels, in the d² 14–32 band, shelled by their own barriers *inside the firing line* (legal because sentinels ignore obstacles) | §6.9; G-D r26/r29 → r30/r32 |
| **P6 — DRIP** | from the round the first turret exists | core | `convert_ammo` of exactly the next shots' cost, every round or two, forever. No bank | §6.8 |
| **P7 — GRIND** | to the end | all four | sentinels put 92.6% of their shots on your core footprint, through your own buildings; home gunners answer anything you plant | §6.4, §6.6 |

**The branch when caging fails** — and this is the honest part, because it is
what happens against every good opponent. There is **no branch**. Watched in
G-B: the seal stalls at 4/8 at r59 and Bean counters keeps the same four jobs
running for **391 more rounds**, planting fourteen forward turrets into an
opponent answering them adjacently and losing thirteen of them at a median age
of seven. Watched in G-A: the seal reaches 2/8, the nest is wiped in 31 rounds,
and after r106 they **never buy another turret** while spending the next 80
rounds rebuilding one conveyor tile sixteen times.

**Map-conditional variation seen on this slate: only one, and it is distance.**
The cage's opening round tracks the walk (§6.3: median r11/r20/r34 for near/mid/
far at an empty ring), and nothing else about the doctrine changes between a
20×20 and a 30×30. The study's determinism finding (95.4% identical first-six
builds within an exact map × seat cell, §3.2) says the same thing from the other
end: **the plan is a function of the map, fixed before the opponent moves.**

---

## 9. PER-TACTIC COUNTER NOTES — the measured habit each one leans on

*(play-the-players. Every row names the number it rests on and its section.
These are notes for a prereg author, not admitted planks — nothing here has been
tested in a live game, and per CLAUDE.md point 6 none of it closes or opens a
road until it has been.)*

| # | their tactic | the measured habit / blindness | what a plank could lean on |
|---|---|---|---|
| **C1** | the cage | **first cage build lands `walk distance + 1`; 2.6% chance it is the far face; 99.4% a barrier** (§6.3) | The tile is predictable from geometry alone before the game starts. Pre-occupying your own ring pushes it **20–30 rounds later** and costs them ~10 builder-turns per tile (§6.3). We already ship `LOKI_BARRIER_SEAL_ON`; this is about **our own** ring, which the study measured at 9.3% enemy-full-seal against us — i.e. we are already hard to cage. **The unpriced half is whether OUR collar is worth its conveyor cost.** |
| **C2** | eviction | **barrier follows the corpse in 1.08 rounds, 67.4% of the time** (§6.2) | A one-round window on a known tile, ~1,800 times across 1,235 games. Anything of ours that re-occupies that tile inside one round denies the seal tile permanently — a 3 Ti barrier of ours is as good as theirs. **The field takes 0.8% of the equivalent openings (§6.5).** |
| **C3** | self-inflicted seal holes | **4,323 self-destroys of their own ring barriers; defenders retake 34 of them = 0.8%** (§6.5) | **3.5 uncontested reopenings per game.** A builder parked on our own ring that rebuilds into any gap the same round would convert most of them. This is the cheapest row in the table and nobody in the league is taking it. |
| **C4** | the sentinel nest | **92.6% of their sentinel shots are at a core tile and 46.5% go through your own buildings** (§6.4) | Cover does not work; **tile denial before the plant** does. Their nest sites are shelled by their own barriers built 1–4 rounds *before* the sentinel (G-D r26/r29 → r30/r32) — **a barrier appearing in the d²14–32 band of our core is a 1–4 round warning that a sentinel is coming to that spot.** |
| **C5** | forward-turret placement | **d²≤13 median life 20 rounds vs d²14–32 median 26** (§6.9) | Their own numbers say the close plants die 30% faster. A defender that reliably answers inside the band (not just inside gunner reach) attacks the profitable half of their nest. |
| **C6** | the doorstep answer | **they shoot at 61.9% of forward turrets, mean lag 12.6 rounds; the adjacent counter-plant answers 344 times at 1.18 rounds and kills 87.2%** (§6.6) | The 38.1% they never shoot at is the window. And the adjacent-plant answer is a *turret* answer — it needs a builder-turn and 20–30 Ti; **when their titanium is low it does not happen** (G-A after r175: BC held 0–11 Ti and answered nothing for 150 rounds). |
| **C7** | target lock | **468 fire-runs ≥10 rounds, 87% of them onto a healed target; 2.0 rotations a game** (§6.7) | **A healed decoy pins a gunner indefinitely.** In G-E one gunner spent 38 rounds and 152 Ti of ammunition on a sentinel healed +8/round against its 7 damage. Cheap to test: a barrier or spare turret in a home gunner's line, plus one builder healing it. |
| **C8** | the ammunition drip | **98.0% of conversions fit `4g+10s`; a long silence means nothing of theirs can shoot** (§6.8) | Not a lever on them — **an instrument for us.** Their convert series is a free live read-out of their turret inventory for any post-hoc analysis. |
| **C9** | the belt | **G-A: one 20 Ti gunner on their delivery face, 94 shots, 16 rebuilds, 0 shots back, `titanium_collected` frozen for 128 rounds** (§5.1) | **The collapse mechanism, and it is the biggest item here.** Their kill chain is economy → ammo → turrets; a gun on the belt disarms the guns. They have a repair loop for it and no removal loop. ⚠ n = 2 games watched; the population version of "do they answer a gun on their belt" is **not measured by this document** and should be before anything is built. |
| **C10** | the siege engineer | **killing it buys a median 11 rounds and a 12.9% permanent stop** (§7.3) | A named, bounded window. It is one identifiable unit (median top-share **1.000**) standing adjacent to our core from ~r35, escortless. **They build 0 launchers in 1,385 games** (study §3.9) — they have no counter-throw, and this is the unit a throw would displace. |
| **C11** | the thrash | **0.52 tiles/game rebuilt ≥5 times; worst 893 builds on one tile** (§6.10) | Not a lever by itself — a symptom of two subroutines fighting. But it means **a tile we can make contested-but-not-lethal drains builder-turns**, which is the same shape as C7 for builders instead of turrets. |
| **C12** | CPU | closed by the study: 3 timeouts in 1,825,401 unit-turns (§3.7) | **Do not spend a leg.** |

**And the one that is about us, not them.** In G-C their gunner walked a
rotation ladder — SW (our launcher) → W (our ring conveyors) → N (more ring
conveyors) → NW (our core) — **rotating 1–2 rounds after each facing line ran
out of targets, three times, ending on our core** (§4.4). Our own gunners in
that game rotated zero times. Their v47 rotation rate is 2.0/game and their v68
rate is 8.1 (study §4.2) — **they are buying more of this verb, not less.**

---

## 10. FOR MAGNUS — watch along

`tools/replay_view.py` renders a `.replay26` to a self-contained HTML page with
a round slider and click-to-drop numbered tile markers, writes it under
`scratchpad/replay_view/`, prints the path, and **never opens a browser** —
open the printed path yourself. **It is not an instrument** (its own docstring
says so) and no claim in this document is cited from it. Note it draws map,
entities and HP bars only: **attacks and turret fire are not drawn as beams**,
they show up as the target's HP bar dropping.

```bash
# G-A — the RATED 0-5 vs Pivot, game 1. Watch (5,2) from round 60 onward.
.venv/bin/python tools/replay_view.py \
  scratchpad/s53_beanwatch47_replays/02c59670-cc8c-4528-a4ec-09ab0f85a0da_game_1.replay26

# G-B — same match, game 3. The 400-round turret attrition; watch r243-r275.
.venv/bin/python tools/replay_view.py \
  scratchpad/s53_beanwatch47_replays/02c59670-cc8c-4528-a4ec-09ab0f85a0da_game_3.replay26

# G-C — what they do to US (our v162). Watch our ring (9,1) from r90.
.venv/bin/python tools/replay_view.py \
  replay_archive/4c901c39-79dd-45dc-a5ae-06db6f5e3a25_game_4.replay26

# G-D — their fastest kill in 1,235 games, r60. The whole doctrine in one screen.
.venv/bin/python tools/replay_view.py \
  replay_archive/3bf73ae7-2da3-4dc3-bd2b-5ce265d702a2_game_3.replay26

# G-E — the full arc vs 0033 on 30x30. Watch (25,14)/(25,15) from r28.
.venv/bin/python tools/replay_view.py \
  replay_archive/9ee3a878-7909-4772-ba8c-e521fb5408c2_game_3.replay26
```

**And the text tape, which is what this document was written from:**
```bash
# whole-game narrative, both sides interleaved (--bc is Bean counters' team index)
.venv/bin/python scratchpad/s53_beanwatch47_watch.py <replay> --bc <0|1> --all
# just the rounds you care about
.venv/bin/python scratchpad/s53_beanwatch47_watch.py <replay> --bc 0 --tape --from 60 --to 160
```
`--bc` per slate game: **G-A 0 · G-B 0 · G-C 1 · G-D 1 · G-E 0.**

---

## 11. CAVEATS

1. **Five games is five games.** Every per-game claim (§2–§5) is EYEBALL-grade
   unless it appears in §6 with an n. The catalog in §6 is the part that
   generalises; the game sections are what made me look for it.
2. **Population.** The v47 set is 1,235 archived games of which **1,115 are
   unrated challenges**, which pools PROTOTYPES on the challenger side
   (study §8.1). Every "field" column is therefore a mixture, and the
   *internal* ratio (them vs the opponents they faced) is the comparison to
   quote, never a cross-fixture difference against our own numbers.
3. **Clustering.** No half-widths are printed in §6. The counts are large and
   the effects are 2–80×, but games cluster in matches and opponents (CLAUDE.md
   DEFF 1.833 unrated / 1.529 rated) and **any of these cells that later carries
   an interval must apply it.** Where a claim is close-run — §6.3's collar
   table, the near-distance band especially — that is said in place.
4. **The two Pivot games are ONE match.** G-A and G-B share an opponent, an
   opponent version, and a twenty-minute slice of the ladder. They are two
   draws from one cluster, not two independent observations.
5. **`print()` is stripped from platform replays**, so no trigger in this
   document is read from their code's own output. Every "stimulus" sentence is
   an INFERENCE from position, round and event order, and is labelled.
6. **Turret and building matching is POSITIONAL where entity ids were not
   available** — the study's caveat 7 applies to §6.1/§6.2/§6.5, which pair a
   death on a tile with a later build on the same tile. Rebuilds on one tile
   blur a pairing; the effect is symmetric across the BC and field columns, and
   §6.10 shows rebuilding is the more common on the BC side, so **§6.1/§6.2 may
   be slightly generous to Bean counters.**
7. **Two hypotheses were refuted while watching and are RETAINED in place:**
   the re-plant-on-a-grave defect (§5.2 — they do it *less* than the field,
   0.46 vs 0.81 a game) and the reading of §6.5's self-destroys as pure
   builder-traffic (58% are followed by their own conveyor, not by a walk).
8. **Nothing was fired, submitted, or committed.** No edits to `QUEUE.md`,
   `bots/`, `tools/`, or any ledger. The Pivot match replays were pulled
   read-only into `scratchpad/s53_beanwatch47_replays/`, deliberately **not**
   into `replay_archive/`, so the keeper daemon's `decoded.txt` ledger is
   untouched. All probes are `scratchpad/s53_beanwatch47_*`.
9. **This is PART 1 of 2 and it covers a version that is no longer live.** v47
   stopped playing rated matches at **2026-08-21T04:12:59Z**; **v68 has played
   every rated match since 07:12:59Z** (study §2). Everything here is about the
   doctrine's *spine*, which the study shows is unchanged across v47/v64/v68
   (the ring and the home economy), plus the parts v68 abandoned (the raid) or
   doubled (the gunners). **The v68 part of this playbook is the live opponent;
   read the merge, not this half alone.**
