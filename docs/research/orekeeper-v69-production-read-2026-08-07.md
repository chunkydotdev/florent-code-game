# v69 "orekeeper" production read — testing the five pre-registered predictions

**Status: COMPLETE.** Closes Q5 of
`docs/research/orekeeper-v69-delta-read-2026-08-07.md`, which could not be
answered at the time ("zero v69 matches in `replay_archive/`"). Corpus is now
15 v69 games across 3 ladder matches, plus a 5-game matched v68 control
against the same opponent version.

**Version tags (rule 2).** Subject = **v69 "orekeeper"**,
`bots/opp_v69/main.py`, md5 `562b01e900d9c17a267d85c6e6f6e914` (re-verified
against the delta read's stamp). Control = **v68 "chokewall"**, md5
`04811b4a3f065f861e74ab626db559df`.

| Match id | Fixture | Score (ours) | Completed (UTC) | Elo Δ |
|---|---|---|---|---|
| `4d5fcf04-492d-4353-af25-0ee777ddbd4f` | OpenSverige **v69** vs I Stone **v18** | **4-1 W** | 20:30:44 | +8.85 |
| `fb335c41-253a-4129-8613-e6b09c164a9f` | OopsGotYourElo **v21** vs OpenSverige **v69** | **1-4 L** | 20:41:22 | −7.89 |
| `54107b82-c56c-4712-bd6d-611254395cfb` | Powerpuff Girls **v18** vs OpenSverige **v69** | **2-3 L** | 20:54:19 | −2.76 |
| `39c40ef7-065d-4878-94c5-4fcba9a2d6ad` (control) | OpenSverige **v68** vs OopsGotYourElo **v21** | **5-0 W** | 19:19:01 | +18.39 |

v69's first three ladder matches: **1 match win, 2 losses, 7-8 on games, net
**−1.80 Elo** (1550.04 → 1548.24). All parses validated by
`core_deliv * 10 == titaniumCollected`: **40/40 team-sides, 0 mismatches.**

---

## VERDICT BLOCK

### Scorecard: 3 CONFIRMED / 1 REFUTED / 1 NOT EXERCISED

| # | Pre-registered prediction (abbreviated) | Verdict |
|---|---|---|
| 1 | Chain-wiredness still collapses in long games; the 5/11-class delivery freeze recurs | **NOT EXERCISED** (control-matched) |
| 2 | Zero conveyors ever placed on an ore tile by the pave path (E2b) | **CONFIRMED** (0/725 vs control 10/725) |
| 3 | On a ≤8-ore decoded map, no builder sits on ore >~1 round (E2a) | **CONFIRMED** (max idle run 1-2 rounds, 3 games) |
| 4 | Melee swings vs a single enemy building id cap near 8 per builder per 300 rounds (E4) | **REFUTED** (worst = 346 consecutive futile swings) |
| 5 | Peacetime ammo conversion stops firing with bank in 12-50 Ti and turrets alive (E1) | **CONFIRMED** (0 violations / 1190 converts vs control 55 / 679) |

### So-what, for the morning graft conversation

**Two of the four E-pieces are production-verified and graft-clean; the other
two are near-inert, and none of them touches what actually lost us games
tonight.** E2b (ore pave ban) and E1 (peacetime ammo floor) both hold
perfectly against a matched v68 control on the same maps — 10 ore-paves and 55
below-floor conversions in five v68 games, versus zero of each in fifteen v69
games. Take both. E2a works exactly as designed but only *where its gate is
open*: it fired on 5 of 15 seats and produced 1-2 round ore residence there,
while the ten gate-OFF seats produced idle ore parks of 34, 49, 58, 59 and
**208** consecutive rounds — including a 20x26 map sitting at **74 embedded
walls, six short of the 80 threshold**, in a game we lost 4,120 to 23,310
delivered. The gate, not the fix, is the bug; widening it is a one-line graft
with a measured 5-of-15-seat expansion available. E4 is the one to *not*
prioritise: the ledger does show its 300-round-ban signature (8 pairs in v69,
0 in the control) and the share of futile pairs falls 23.4% → 6.0%, but 924 of
the 1,190 residual futile swings land on **gunners** — the counterbattery path
E4 explicitly does not cover — so a single builder still burned 346
consecutive no-progress swings on one gunner id. Most important for the
merge conversation: **the delivery-freeze defect the delta read called
UNTOUCHED never fired in this corpus, and neither did it in the v68 control**
— all three v69 losses to OopsGotYourElo were *core deaths or an economy-scale
tiebreak loss* (18 harvesters to our 12, 24 to our 9), not a frozen chain. The
morning conversation should therefore be about opening tempo and harvester
scaling on the second seat, not about chain repair, and it should carry one
new exploit we found: **a builder parked on top of a v69 conveyor makes v69
attack its own conveyor forever** (489 swings / 978 Ti in one game), a bug the
delta read did not predict.

---

## Prediction-by-prediction

### Prediction 1 — delivery freeze

> "Chain-wiredness still collapses in long games — the 5/11-class freeze
> should recur at a similar rate, because nothing repairs a cut chain."

**Verdict: NOT EXERCISED (control-matched).**

Long games available: 5 v69 games at r≥600 (three at r1000), 4 v68 control
games at r1000. **Zero freezes on either side.** Longest no-delivery gap for
v69 in any of the 15 games is **8 rounds**; longest dead tail is 28 rounds
(4d5fcf04/g5, a 113-round loss). The v68 read's signature — "delivered Ti
froze permanently at r59-350, 649-940 dead rounds" — does not appear anywhere,
**including in the v68 control**, so this corpus cannot discriminate. The
freeze regime came from the strong unrated burst (sporks/Jython/Pivot), not
from ladder opposition.

Two calibration findings that *are* usable:

- **Partial wiredness collapse ≠ delivery freeze.** fb335c41/g4 ends at
  **36/76 directed-wired (47%)** and still delivered on r999. 54107b82/g4 ends
  at 8/16. Low wiredness alone is not the instrument; the freeze needs
  wiredness collapse *and* a stalled cumulative-delivery series.
- **The defect is visible in a mild form.** In fb335c41/g4 v69's wired count
  is 36 at r500 and still 36 at r1000, while total relays rise 69 → 76: it
  laid ~7 more conveyors over 500 rounds and attached **zero** of them. That
  is `_build_next_link` popping occupied tiles, exactly as the delta read
  described, just not severe enough to stop the pipe.

### Prediction 2 — E2b ore pave ban

> "**Zero conveyors ever placed on an `ORE_TITANIUM` tile by the pave path**
> (E2b, map-agnostic). One such placement falsifies E2b's coverage."

**Verdict: CONFIRMED.**

| Version | Relays placed | On an ore tile | Games with ≥1 ore-pave |
|---|---|---|---|
| **v69** (15 games) | **725** | **0 (0.00%)** | **0 / 15** |
| v68 control (5 games) | 725 | 10 (1.38%) | 4 / 5 |

The denominators are identical by coincidence, which makes the comparison
unusually clean. v68's ore-paves: 4 in g2 (25x25 — `(11,5)` r211, `(13,11)`
r218, `(13,10)` r223, `(12,10)` r232), 2 each in g3, g4, g5. **The 25x25
`(5,5)/(18,18)` map is in both corpora**: v68 paved 4 of its 263 relays onto
ore there; v69 placed 96 and 126 relays on the same map across two games with
zero ore-paves. Opponents in the same games paved ore 5 times, so the metric
is live and the zero is not an artefact of nobody ever building near ore.

*Caveat on scope:* this tests the observable, not the code path. The delta
read's gap 3 (`_build_next_link` has no ore check on undecoded maps) is
**untested** — all 15 games were on decoded maps, where `_link_path`'s BFS
already blocks ore. The regression vector named in the delta read (a legacy
chain tile on ore that can now never be re-laid) also never arose.

### Prediction 3 — E2a scarce-ore step-off

> "On a ≤ 8-ore decoded map, no builder should sit on an ore tile for more
> than ~1 consecutive round (E2a). A long park there falsifies E2a's gate or
> means the map was not decoded."

**Verdict: CONFIRMED.**

Three games ran on decoded maps with ≤8 ore — exactly the maps E2a's new
clause unlocks. Longest run of consecutive rounds with a v69 builder standing
on ore *and not acting*:

| Game | Map | Ore | Walls | Gate | Idle ore-run |
|---|---|---|---|---|---|
| 4d5fcf04/g3 | 18x18 | 8 | 18 | **ON (E2a ore≤8)** | **2** |
| fb335c41/g2 | 18x18 | 8 | 18 | **ON (E2a ore≤8)** | **1** |
| fb335c41/g3 | 10x10 | 6 | 10 | **ON (E2a ore≤8)** | **1** |
| 4d5fcf04/g1 | 26x26 | 38 | 208 | ON (walls≥80) | 2 |
| 54107b82/g3 | 28x20 | 28 | 122 | ON (walls≥80) | 3 |
| 4d5fcf04/g2 | 25x25 | 30 | 4 | OFF | 10 |
| fb335c41/g5 | 25x25 | 30 | 4 | OFF | **34** |
| 4d5fcf04/g5 | 25x15 | 24 | 8 | OFF | **58** |
| 54107b82/g4 | 20x26 | 22 | **74** | OFF | **59** |
| 54107b82/g5 | 25x15 | 24 | 8 | OFF | **208** |

(remaining 5 gate-OFF games: idle runs 0-2)

Every gate-ON seat is ≤3 rounds; every long park is on a gate-OFF seat. The
separation is total. Two riders:

- **The pathology is unchanged where the gate is shut.** 4d5fcf04/g5 builder
  #10 spent 61 rounds on ore taking **60 moves and 1 build**, oscillating
  (6,1)↔(6,0) 29 rounds each — x3r0's own described "mv→adjacent,
  mv→onto-ore" loop. 54107b82/g5 builder #6 sat at (7,6) for **225 of 228**
  on-ore rounds with **7 actions total, all moves, zero builds**. 54107b82/g4
  builder #307 oscillated (11,13)↔(11,12), both ore, 65 of 67 rounds.
- **SURPRISE (mechanism, see below): the step-off is unreachable for an
  acting unit.** 4d5fcf04/g1 shows a 120-round ore residence on a gate-ON map,
  which looks like a falsification until you separate idle from busy: builder
  #3 attacked on **125 of 125** on-ore rounds. The step-off block sits below
  `if ct.get_move_cooldown() != 0: return` (:2867), and acting blocks
  movement, so a saboteur camped on ore never reaches the gate at all.

### Prediction 4 — E4 melee futility ledger

> "Melee swings against any single enemy building id should now cap near 8 per
> builder per 300 rounds (E4), versus v68's measured 865-swing tail."

**Verdict: REFUTED.**

Simulating E4's own rule from the replay (per (builder, target-building-id)
pair, count consecutive swings after which target HP did not fall):

| | v69 (15 games) | v68 control (5 games) |
|---|---|---|
| enemy-target pairs | 285 | 64 |
| pairs with a futile run > 8 | **17 (6.0%)** | 15 (23.4%) |
| worst futile run | **346** | 98 |
| swings inside >8 futile runs | 1,190 (79/game) | 976 (195/game) |
| pairs showing a ≥250-round gap after a futile run (ban signature) | **8** | **0** |

Worst offenders, all v69: builder #635 → gunner #455, **353 swings / 346
consecutive with no HP progress**, r383-741 (fb335c41/g5); builder #8 → gunner
#415, 138 swings / 136 futile (same game); builder #1246 → gunner #684, 162
swings, r414-999 (fb335c41/g4).

The cap does not exist in production. But the residue's *shape* says the
ledger is working inside its declared scope: **924 of the 1,190 residual
futile swings are against gunners and 47 against sentinels** — turrets, i.e.
the counterbattery path the delta read explicitly listed as uncovered —
whereas v68's futile swings were spread across gunners (454), conveyors (350)
and barriers (172), the `_sabotage_prio` diet E4 now polices. The 8 v69 pairs
that resume after a ≥250-round gap (0 in the control) are the ban firing.

**Exploit residue stands and is larger than the delta read estimated.** The
delta read priced a healed bait at "8 swings × 2 Ti = 16 Ti per builder per
300-round ban". Production says a bait that draws the *counterbattery* chooser
instead of `_sabotage_prio` is not rate-limited at all: a single surviving
gunner absorbed 353 swings (706 Ti) from one builder over 358 rounds.

### Prediction 5 — E1 peacetime ammo floor

> "Peacetime ammo conversion should stop firing whenever the bank sits between
> 12 and 50 Ti with turrets alive (E1) — a visible flat stretch in converted
> ammo against a low bank."

**Verdict: CONFIRMED.**

`under` was reconstructed from the replay against both of its writers
(`_core` :802-825 core-vision scan; :1274-1278, any friendly unit scanning the
same core-relative radii `gun_sense`=64 / `b_sense`=16), giving a narrow lower
bound and a wide upper bound. A conversion violates E1 if it fires with
`under` false under **both** reconstructions and a pre-round bank more than 10
Ti (one passive tick) below `ti_floor + 4`.

| | conversions | in confirmed-quiet rounds | **violations** |
|---|---|---|---|
| **v69** (15 games) | **1,190** | 273 | **0** |
| v68 control (5 games) | 679 | 527 | **55** |

v68's violations are unambiguous: 39c40ef7/g4 alone has 41 conversions with 2
home guns alive, no enemy anywhere near its core, and a bank of 16-21 Ti.
v69 does this zero times in more than 1,700 conversion-eligible rounds.

**The important qualification for the exploit side.** `under` is true in
**69-99% of rounds in 13 of the 15 v69 games** (median 92%; the two exceptions
are 30% and 36%, both games we were winning decisively). The 50-round latch
plus "any enemy builder within d²≤16 of our core, spotted by *any* of our
units" makes peacetime rare in contested play. So the delta read's "directly
exploitable 38-Ti-wide band" is real but narrow: it is only open in the
minority of rounds where no enemy unit has come near the core for 50
consecutive rounds. **v69 is only meaningfully slower to fill its magazine
when it is already comfortably ahead.**

---

## Additional requested items

### (a) E2a / E2b firing evidence

Covered in full under predictions 2 and 3. Summary: **E2b fired everywhere
and worked** (0/725 vs 10/725 control). **E2a's new clause was exercised on 3
of 15 seats** (18x18 ×2 at 8 ore, 10x10 at 6 ore) and produced 1-2 round ore
residence on all three; the pre-existing walls≥80 clause covered 2 more seats.
On the 10 gate-OFF seats the un-fixed pathology recurred at up to 208
consecutive idle rounds. The pool's ore counts, decoded from the replays:
6, 8, 8, 12, 12, 22, 24, 24, 28, 30, 30, 32, 32, 38 — so **`≤8` unlocks
exactly the 10x10 and the 18x18**, and the next map up is at 12. The wall
counts tell the same razor-thin story the v68 read flagged: 4, 8, 8, 10, 18,
18, 22, 22, 34, 64, 64, 74, 122, 208 — **74 and 64 sit just under the 80
threshold**, and the 74-wall seat (54107b82/g4, 20x26) is one of the worst
parks in the corpus.

### (b) SLOT_HARVESTERS post-wipe behaviour — NOT EXERCISED

**No v69 game wiped a harvester count to zero.** Across all 15 games the
minimum harvester count after the peak was: 5,15,6,3,3,2,3,4,12,9,**1**,7,2,3,3.
The closest approach is 54107b82/g1 (peak 3 @r24 → 1, never 0) and
54107b82/g4 (peak 6 @r83 → 3). The v68 control likewise never zeroed
(min-after-peak 8,12,15,3,14). The monotonic high-water signature described in
the delta read — pave and ammo gating continuing as if harvesters exist after
they are gone — therefore **had no opportunity to appear**, and the finding
stands as a code-level claim only, still unverified in production. Worth
re-testing the first time an opponent wipes his harvester line.

*(Note for the record: `SLOT_HOME_GUN` at :1956/:2524/:2528 is a monotonic
counter with the same never-decrement shape as `SLOT_HARVESTERS` — the delta
read named only the latter.)*

### (c) Delivered Ti + wiredness, both sides, per game

`wired` = directed wiredness at end of game (conveyors/splitters with a
facing-respecting path into a Core footprint tile) / total live relays.
`gap` = longest no-delivery stretch after first delivery; `tail` = rounds
after the last delivery.

| Game | Map | End | our delivTi | their delivTi | our gap/tail | their gap/tail | our wired | their wired |
|---|---|---|---|---|---|---|---|---|
| 4d5fcf04/g1 | 26x26 | W core r429 | 4,080 | 3,680 | 3/0 | 3/1 | 23/31 | 16/16 |
| 4d5fcf04/g2 | 25x25 | W core r327 | 4,850 | 2,070 | 4/0 | 18/1 | 77/96 | 9/12 |
| 4d5fcf04/g3 | 18x18 | **W Ti r1000** | **4,970** | **4,880** | 2/1 | 4/0 | 43/63 | 4/4 |
| 4d5fcf04/g4 | 16x16 | W core r61 | 320 | 480 | 4/1 | 2/2 | 12/20 | 17/17 |
| 4d5fcf04/g5 | 25x15 | L core r113 | 300 | 1,030 | 4/**28** | 2/1 | 2/13 | 26/26 |
| fb335c41/g1 | 16x16 | L core r121 | 100 | 1,220 | 4/1 | 4/0 | 4/6 | 26/41 |
| fb335c41/g2 | 18x18 | L core r205 | 980 | 1,000 | 4/1 | 3/1 | 6/13 | 4/4 |
| fb335c41/g3 | 10x10 | **W Ti r1000** | 6,710 | 200 | 4/0 | 8/**925** | 52/53 | 0/5 |
| fb335c41/g4 | 28x20 | **L Ti r1000** | 17,410 | 26,570 | 3/0 | 3/0 | 36/76 | 117/133 |
| fb335c41/g5 | 25x25 | L core r742 | 10,240 | 21,300 | 8/1 | 3/0 | 68/125 | 122/132 |
| 54107b82/g1 | 25x25 | L core r594 | 1,780 | 6,860 | 4/4 | 4/0 | 5/5 | 57/57 |
| 54107b82/g2 | 28x20 | L core r396 | 7,700 | 9,490 | 2/1 | 3/0 | 25/29 | 48/49 |
| 54107b82/g3 | 28x20 | W core r162 | 690 | 0 | 4/3 | —/162 | 15/23 | 0/5 |
| 54107b82/g4 | 20x26 | L core r905 | 4,120 | 23,310 | 4/2 | 2/0 | 8/16 | 51/51 |
| 54107b82/g5 | 25x15 | W core r263 | 930 | 530 | 4/1 | 22/103 | 17/17 | 0/8 |
| *39c40ef7/g1* | 28x20 | W core r218 | 1,610 | 0 | 3/0 | —/218 | 38/48 | 0/0 |
| *39c40ef7/g2* | 25x25 | W Ti r1000 | 25,420 | 22,590 | 4/0 | 3/0 | 141/254 | 91/113 |
| *39c40ef7/g3* | 26x26 | W Ti r1000 | 26,240 | 21,910 | 3/0 | 2/0 | 117/162 | 50/71 |
| *39c40ef7/g4* | 18x18 | W Ti r1000 | 9,510 | 320 | 4/1 | 8/905 | 33/78 | 2/13 |
| *39c40ef7/g5* | 25x15 | W Ti r1000 | 15,630 | 8,320 | 3/0 | 4/0 | 45/133 | 16/16 |

**Every r1000 game in the corpus resolved at tiebreak step 1, titanium
delivered** (`win_condition == "titanium_collected"` in 7/7). Steps 2
(harvesters alive) and 3 (stored Ti) were never reached — the v68 read's
11/11 finding now stands at **18/18**. Dump-stored-Ti plays remain wasted.

Note that in **both** r1000 games v69 won, its stored Ti was *also* ahead or
near-level (1,266 vs 1,355; 3,989 vs 10) — the margin lived entirely in
delivery. In 4d5fcf04/g3 the whole game came down to **90 Ti** (4,970 vs
4,880), i.e. **nine stacks**, against an opponent running 2 harvesters to our
6. See the surprise below for where 978 Ti went in that game.

### (d) SURPRISES — behaviour the delta read did not predict

**S1 (high value) — v69 attacks its own conveyor, indefinitely, when an enemy
builder parks on it.** In 4d5fcf04/g3, an OpenSverige builder (#5) at (4,9)
swung at tile (3,9) on **489 occasions between r308 and r999** — every other
round for 692 rounds. On that tile sat **our own conveyor #162** and a
**parked enemy builder bot #400 at full 40 HP the entire time**. The builder
attack damages the *building* on the tile, so each swing took 2 HP off our own
conveyor (its HP oscillates 18↔20 as the chain medic heals it back) while the
enemy bot was never touched and never moved. Cost: **978 Ti of swings** plus
the heals, in a game won by 90 Ti of delivery. The same shape appears twice
more (4d5fcf04/g2, builder #5 → own conveyor #709, 28 swings, enemy builder #4
parked on it; fb335c41/g5, 18 swings). Aggregate: **535 of v69's 4,755 melee
swings (11%) landed on its own buildings**, against 22 of 1,376 (2%) for v68.
E4's ledger cannot catch it — the ledger is keyed on *enemy* building ids in
`_sabotage_prio`. **This is a directly exploitable, low-cost denial play: park
one builder on a v69 conveyor and it pays 2 Ti/swing forever to hit itself.**

**S2 — the ore step-off is dead behind an acting unit.** Reported under
prediction 3: the E2a/step-off block lives in the move phase after
`if ct.get_move_cooldown() != 0: return` (:2867). A builder that acts every
round (a saboteur camped on ore, 125/125 rounds in 4d5fcf04/g1) never reaches
it. Any graft of E2a into our line should hoist the ore check above the
move-cooldown gate or it inherits the same hole.

**S3 — no crashes, no TLEs, no output.** Across all 20 games and both sides:
**0 CPU timeouts, 0 captured stdout, 0 tracebacks.** The ancestral pave-crash
class (v69:3536) produced no observable unit loss in v69's own line, exactly
as the delta read predicted (his `run()` swallows it; the trail freshness gate
nulls the stale tile). Our piece-N fix remains worth ~nothing to him.

**S4 — v69 barely uses launchers; the opponent does.** v69 threw 0-1 times per
game (5 throws across 15 games). OopsGotYourElo threw **108 times in
fb335c41/g4** and 163 times against v68 in 39c40ef7/g5. In fb335c41/g4 v69
lost **15 builder bots to OGE's 0**. The Piece-F handshake gap named in the
delta read (enemy-launcher throws miss the reset) is being exercised hard by
the top ladder opponent and is worth a targeted look.

---

## Per-match sections

### `fb335c41` — OopsGotYourElo v21 4-1 OpenSverige v69 (highest value)

The stress test the brief asked for, and **it did not stress what we expected
it to.** Of the four losses, **three were core deaths** (r121, r205, r742) and
only one reached r1000. The single tiebreak loss was decided at step 1,
delivered Ti, 17,410 to 26,570 — with v69 delivering continuously through r999
and no freeze anywhere.

Per-game mechanism:

- **g1 (16x16, seat (11,11)), L core r121.** Economy collapse, not chain
  failure: v69 built **2 harvesters (r7, r11)** to OGE's 7, first delivery
  **r89 vs r9**, 6 relays vs 42, 17 turret shots vs 124. Core dead at r121.
- **g2 (18x18, seat (14,2)), L core r205.** Even on economy (980 vs 1,000
  delivered, 3 harvesters each) and lost on the fight: 114 shots vs 196.
- **g3 (10x10, seat (6,6)), W Ti r1000.** Our only win. **OGE froze**, not us:
  its delivery stopped at r74 and never resumed (925 dead rounds, 0/5 wired at
  end) while v69 ramped 80 → 1,750 → 4,130 → 6,710. This is the delivery-freeze
  defect — on the other side of the board.
- **g4 (28x20, seat (19,9)), L Ti r1000.** The tiebreak loss. Level to r500
  (7,430 vs 7,460), then OGE pulled away on scale: **18 harvesters to our 12,
  133 relays at 117/133 wired to our 76 at 36/76**. v69's wired count sat at
  36 from r500 to r1000 while it kept laying conveyor — the mild form of the
  untouched defect, costing growth rather than causing a freeze. OGE also
  threw 108 times, and we lost 15 builders to their 0.
- **g5 (25x25, seat (18,18)), L core r742.** Blowout: **9 harvesters to 24**,
  42 turret shots to 875, 10,240 delivered to 21,300, core dead r742.

**Matched control (`39c40ef7`, v68 5-0 vs the same OGE v21).** Two maps recur:

| Map | v68 | v69 |
|---|---|---|
| 18x18 `(2,14)/(14,2)` | seat (2,14), **W Ti r1000**, 9,510 vs 320 | seat (14,2), **L core r205**, 980 vs 1,000 |
| 25x25 `(5,5)/(18,18)` | seat (5,5), **W Ti r1000**, 25,420 vs 22,590 | seat (18,18), **L core r742**, 10,240 vs 21,300 |
| 28x20 `(7,9)/(19,9)` | seat (7,9), **W core r218**, 1,610 vs 0 | seat (19,9), **L Ti r1000**, 17,410 vs 26,570 |

**Load-bearing caveat: the seats are inverted on all three shared maps** —
OpenSverige was team A in the v68 match and team B in the v69 match. Given the
project's own standing finding that seat matters enormously on some maps, this
comparison **cannot** be read as "v69 is worse than v68". What it does
establish is that the v69 losses are opening-tempo and economy-scale losses
(harvester counts 2/3/9/12 against 7/3/24/18), not delivery-continuity losses,
and that nothing in the v69 patch addresses that axis.

### `4d5fcf04` — OpenSverige v69 4-1 I Stone v18

The healthy sample. Four wins, three of them core kills before r430, one
r1000 tiebreak win by **90 delivered Ti**. Notable for containing the corpus's
best E2a evidence (g3, 18x18 at 8 ore, idle ore-run 2) and its worst self-
attack incident (g3, 489 swings on our own conveyor — in the same 90-Ti game).
g5 is the one loss: 25x15, gate OFF, a 58-round idle ore park, wiredness
ending at 2/13 and the corpus's longest dead delivery tail (28 rounds) in a
113-round game.

### `54107b82` — Powerpuff Girls v18 3-2 OpenSverige v69

Two wins by core kill (r162, r263), three losses by core kill (r396, r594,
r905). **g4 is the graft-brief exhibit**: 20x26 with **74 embedded walls**, six
below `ORE_STEPOFF_MIN_WALLS`, 22 ore (above the E2a ≤8 clause) — so both
step-off clauses are shut. Result: builder #307 oscillating on two adjacent
ore tiles for 65 of 67 rounds, builder #4 parked 52 rounds, harvesters peaking
at 6 and falling to 3, wiredness 8/16, and a 4,120-to-23,310 delivered-Ti
loss. g1 shows the same family: 3 harvesters down to 1, 15 of 20 relays
destroyed, 1,780 vs 6,860.

---

## Method notes

- **Parser.** Fresh per-round walker,
  `scratchpad/v69_walk.py`, built on the wire primitives in
  `tools/replay_schema.md`. Full turn-by-turn entity state (place / move /
  remove / hp / players / attack / heal / build / convert / fire / output).
  Validated by `core_deliv * 10 == titaniumCollected` on **40/40 team-sides**.
  Turret counts deduped by entity id per the tooling doc's rotation gotcha
  (`placeEntity` re-emission); throws detected as `moveBuilderBot` with
  displacement > 1 tile.
- **Two parser bugs found and fixed mid-read, both worth writing down.**
  (1) `UpdatePlayers` has **two** levels of nesting — `UpdatePlayers { Players
  players = 1 }` then `Players { Player a = 1; Player b = 2 }`. Reading one
  level yields the raw `Player` submessage bytes as "titanium". (2) `int32`
  negatives in `UpdateHp.delta` are **64-bit sign-extended** varints, so the
  fix-up is `if v >= 1<<63: v -= 1<<64`, not `1<<31 / 1<<32`. With the wrong
  mask every HP reading is astronomically large and every futility analysis is
  garbage.
- **Building-at-tile resolution must be an authoritative `pos → id` index**,
  maintained on place/remove (and seeded with both Core footprints, which are
  never placed by an update). Scanning the entity dict for "first entity at
  this position" mis-attributes attacks whenever a tile is rebuilt, and it
  hides the S1 finding entirely, because **builder bots stand on top of
  conveyors** — a target tile routinely holds both a building and a unit.
- **Wiredness** computed both directed (facing-respecting, reverse-BFS from
  Core footprint tiles; splitters output to the three cardinals that are not
  their back) and undirected, sampled every 20 rounds. Directed is reported
  throughout; it is the sharper measure per `tools/replay_census.py`.
- **`under` reconstruction (E1)** is a two-sided bound, not a point estimate,
  because the flag has two writers with different visibility (`_core`'s own
  r²=36 scan and any friendly unit's scan at :1274). Violations were only
  counted when quiet under both bounds *and* more than one passive tick below
  the floor. Pre-conversion bank is the **end-of-previous-round** value —
  `UpdatePlayers` is emitted once per turn, after the conversion — so it is a
  proxy; the margin rule absorbs the error. **UNCERTAIN** at the ±10 Ti level.
- **`weapons` proxy (E1)** is a monotonic count of own turrets ever built,
  standing in for `SLOT_HOME_GUN`, which counts only turrets built at specific
  home sites. This can only *over*state `weapons`, which lowers the floor from
  52 to 46 and therefore makes the violation test **conservative**.
- **`under` fraction and E4 futility runs** use end-of-round entity positions,
  a one-round approximation of what the bot saw. **UNCERTAIN** at ±1 round.
- **Map decode status** determined offline by matching each replay's
  (width, height, both core anchors) against `MAP_CODES` + `EXTRA_MAP_CODES` in
  `bots/opp_v69/main.py`. All 20 games were on decoded maps; runtime
  disambiguation between the two ambiguous 26x26 and 28x20 entries was not
  independently verified (**UNCERTAIN**), but both candidates in each pair fall
  on the same side of the walls≥80 threshold, so the gate state is unaffected.
- **Ore-run classification** splits consecutive on-ore residence into *idle*
  and *busy* by whether the builder attacked during the run — necessary
  because the step-off gate is unreachable while acting (S2). Reporting a
  single "max ore run" conflates a working saboteur with a stuck builder and
  produces a false E2a falsification.
- Scratch parsers: `v69_walk.py`, `analyze.py`, `e1.py`, `final.py`,
  `drill.py`, `probe_pair.py` in the session scratchpad. Read-only throughout:
  no bots edited, no matches run, no downloads.

## Open questions

- **Does the delivery freeze still exist at all on current ladder opposition?**
  Zero occurrences in 20 games across both versions. The v68 read's 5/11 rate
  came from the strong unrated burst. Re-test needs that opponent class, not
  more ladder games.
- **How wide should E2a's gate be?** The measured pool splits at ore
  {6,8,8,12,...} and walls {…,64,74,122,208}. Moving the ore clause to ≤12 or
  the wall clause to ≥70 would have covered 3 more of tonight's 15 seats,
  including the 20x26 park that cost a 4,120-vs-23,310 game. Cheap offline
  check against the full decode table; needs x3r0's call before anyone grafts.
- **Is S1 (self-conveyor attack) reproducible on demand?** It fired 3 times in
  15 games, always with an enemy builder parked on our relay. If it is that
  cheap to induce, it is a denial row for the book — but it also means *our*
  line needs the same guard before we graft anything melee-shaped from his.
- **What is E3?** Still no trace in the shipped file and nothing in production
  looks like a chain fix. Question for x3r0 stands unchanged.
- **Seat effects on the shared OGE maps.** Every v68/v69 comparison in this
  read is seat-inverted. A same-seat comparison needs either a rematch or an
  arena run, which is the builder's call, not this arm's.
