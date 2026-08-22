# DECODE — FIRST CONTACT, Skalman rc **v180**: reach, first-damage, fidelity-in-contact

**Fresh replay-decode agent, no inherited session context beyond the named inputs.**
Commissioned by RESEARCH s54 (`scratchpad/s54_firstcontact_decode_commission.md`, opened).
**Clock:** all times UTC from `date` in-shell; this document written **2026-08-22T10:09:12Z**.
**Repo HEAD at write time:** `d7dc2d3d9`. **Corpus manifest built** `2026-08-22T10:09:08Z`
(91,206 archived replays, join reconciliation 6,668/6,668 = 1.0000).

**Population.** The 13 first-contact matches, **65 games**, all `ourver = 180`, all
`triggeredBy = unrated`, fired 08:24:06Z–09:01:31Z:

| cell | opponent | their pinned version | matches | games | our score |
|---|---|---|---|---|---|
| **MIRROR** | Bean counters | **v68** (20/20 rows) | 4 | 20 | **1–19** |
| **PIVOT** | Pivot | **v249** (20/20 rows) | 4 | 20 | **0–20** |
| **KLADDE** | kladde chatte tville (och oss) | **v173** (25/25 rows) | 5 | 25 | **1–24** |

**Pin check (CLAUDE.md's instrument alarm): PASSES.** Every game in a cell decodes the
same `oppver`; no cell holds a mixed triple. `our_team` in `corpus/unrated_games.tsv` is
derived from `teamAId`/`teamBId` (`tools/corpus/unrated_games.py:154-158`), **not** from
any winner-derived field, so `corpus-howto` TRAP 7 does not reach this decode.

**Decoders — nothing hand-rolled that exists.** `scratchpad/s54_klad_lib.py` (event walker
over `tools/replay_census.py` primitives: rotation-re-emit guard, never-popped registry,
signed 64-bit HP deltas), `scratchpad/s54_klad_autopsy.py` (self-checking core-damage
ledger), `tools/skalman_fidelity.py` (the fidelity column set, per seat), `tools/crash_census.py`
(exception-death classifier, `--selftest` run and passed), and the CUT-116 facing probe
(`scratchpad/s54_fc_facing{,2}.py`) for the belt-gun line test. **Platform writes: none.
Platform reads: none** — every replay was already on disk. `bots/` was **not opened**;
every behavioural statement below is read off replay bytes.

---

## 0. VALIDATION — RUN FIRST, AND EVERY CONTROL DRIVEN TO THE OTHER VERDICT

### 0.1 Known-cell reproduction

Own decode path vs `corpus/unrated_games.tsv`, per game, on **rounds / `win_condition` /
winning seat**, and per match on the **score**:

```
65 of 65 games      turns EXACT       win_condition EXACT       winning seat EXACT
13 of 13 matches    score reproduced  (0-5 ×11, 1-4 ×2 — exactly the commission's list)
```

### 0.2 The controls, because a check that has never failed has not been seen to check

| control | result | reads |
|---|---|---|
| **MIS-PAIRED rows** (each corpus row validated against the *next* file) | turns_ok **65 → 1** | the turns check discriminates |
| same, `win_condition` | cond_ok **65 → 65** | ⛔ **`cond` is a CONSTANT COLUMN here: `core_destroyed` in 65 of 65 games.** The cond check has **zero discriminating power** on this pool and validates nothing (TRAP-8 shape). It is reported, not relied on |
| same, winning seat | won_ok **65 → 59** | weak: we lose 63/65, so a mis-pairing usually preserves the answer. Not load-bearing |
| **TRUNCATED replay** (first half of the bytes) | rounds 53 vs 95, cond `''` vs `core_destroyed` | the decode path *can* emit the other value |
| **DAMAGE-LEDGER self-check** (attributed FireTurret/BuilderAttack damage == summed negative `UpdateHp` deltas on the dying core) | **0 mismatches in 65 of 65 core deaths** | — |
| **LEDGER MUTATION** (sentinel damage constant 18 → 17) | **20/20 games mismatch** | the ledger is a real, 1-point-sensitive control |
| **RESIDUAL-HP ledger** (HP remaining at `removeEntity`, seeded from max HP) | **64 of 65 core deaths land on residual exactly 0** | the ledger's own positive control; the 1 exception is §2 |
| **`crash_census.py --selftest`** | fires 17 on the known-crashing side, **0 on both negative-control sides** | PASS |
| **cross-decoder count agreement** | the facing walker and the event walker independently produce **438 opponent turret lives and 239 of ours** — identical | two parsers, same answer |

**The load-bearing validation is therefore: turns (65/65, mis-pair → 1/65) + the 13 match
scores + the mutation-tested damage ledger.** The `cond` cell is decoration.

### 0.3 ⛔ THE POOL IS SMALLER THAN 65 GAMES — CONTENT-DUPLICATE CLUSTER, MEASURED

Fingerprint = full gameplay event stream (builds, moves, builder verbs, deaths, ammo
converts, HP) + map dimensions + game length, SHA-1, **`BotOutput` excluded** (its
`execTimeUs` is nondeterministic).

| cell | games | **distinct** | exact duplicates |
|---|---|---|---|
| MIRROR | 20 | **17** | 3 (15.0%) |
| PIVOT | 20 | **16** | 4 (20.0%) |
| KLADDE | 25 | **25** | 0 (0.0%) |
| **ALL** | 65 | **58** | **7 (10.8%)** |

The duplicate sets are byte-identical whole games repeated across *different matches* on
the same map and seat: `64a8beb6/3 == 919000f0/3 == ab068a0d/2`, `0e5b63ea/1 == 4bc7ed13/5`,
`0e5b63ea/2 == e46e55fd/5`, `4bc7ed13/4 == e46e55fd/1`, `64a8beb6/5 == 919000f0/1`,
`919000f0/4 == ab068a0d/1`.

**CONTROLS:** degenerate fingerprint (map dims only) 65 → 9 distinct, i.e. the pipeline can
emit duplicates; same file twice → identical (True); side-swapped fingerprint → different
(True).

⇒ **Every MIRROR and PIVOT bar below is computed on a pool whose effective n is ~16-17, not
20.** This is the CONTENT-DUPLICATE cluster of CLAUDE.md's four-cluster enumeration,
measured live on this pool rather than assumed.

### 0.4 ⭐ REFUTATION OF A CARRIED PREMISE: **kladde is the nondeterministic side here, not us**

`REPLAY-STUDY-kladde-v173-2026-08-22.md` §1.4 banked (INFERENCE-labelled) *"the
non-determinism in this pool is OURS, not theirs."* On **this** pool the opposite holds:

* KLADDE cell, side-resolved fingerprints: **OUR side distinct 22/25; THEIR side distinct 25/25.**
* Anchor, fully diffed: `0de59936/1` and `82a03bfd/1` (same map 24×24, same seat) are
  **event-for-event identical for 50 rounds**; the first divergence is
  `r50 MOVE (kladde builder #5) (21,18)→(22,18)` vs `(21,18)→(21,17)`. Both games still
  run 95 rounds and both cores die at r94.
* Entity 5's team byte is kladde's (verified against the map's core-team index).

**MEASURED:** our event stream is byte-identical across that pair while theirs is not.
**INFERENCE** on the cause (a CPU-time- or ordering-dependent branch on their side is
consistent with it; nothing on the wire names it). **This does not contradict the earlier
study's measurement** — different our-version, different pool — but it does mean the
"our jitter" attribution must not be carried forward as a property of the matchup.

---

## 1. THE HEADLINE, IN ONE TABLE — **WE NOW ARRIVE. WE DO NOT FINISH.**

| | MIRROR (BC v68) | PIVOT (v249) | KLADDE (v173) |
|---|---|---|---|
| **OUR REACH** — games with ≥1 point of damage on their core | **19/20 = 95.0%** | **19/20 = 95.0%** | **22/25 = 88.0%** |
| median round of our first damage | r53 | **r34** | **r39.5** |
| median total damage into their core | 227 | 243 | 198 |
| **THEIR REACH on us** | 19/20 = 95.0% | 20/20 = 100% | 24/25 = 96.0% |
| median round of their first damage | **r36** | r88 | r83 |
| median total damage into our core | 504 | 591.5 | 504 |
| median round our core dies | r121 | r159 | r116.5 |
| core-kill wins | 1/20 | 0/20 | 1/25 |
| — of those, by r300 | 1 | 0 | **0** (the kladde win lands r320) |
| our core dead by r300 | 19/20 | 19/20 | 16/25 |
| games ending `core_destroyed` | 20/20 | 20/20 | 25/25 (no r1000 stalls anywhere) |

### 1.1 ⭐⭐ THE KLADDE REACH BAR IS THE ONE THING THAT MOVED, AND IT MOVED A LOT

`REPLAY-STUDY-kladde-v173` §5 set the bar Skalman was to carry: **REACH** and
**FIRST-DAMAGE ROUND**, not game share. Against the same opponent version:

```
REACH on kladde's core   v175-v177 (STUDY §4.3, n=45)  31.1%
                         v180      (this decode, n=25) 88.0%
                         diff +56.9pp   95% hw 29.3pp (DEFF 1.434)   EXCLUDES ZERO
```
Median first-damage round **r134 → r39.5**. The teams that actually beat kladde arrive at
**r31–r57** (`not adgato` r39, Erebus r31, HTTP 418 r57). **v180 is inside that band.**

⚠ **DEFF enumeration, in writing.** MATCH cluster **LIVE** (5 games per match, 5 matches).
OPPONENT cluster **DEAD** (the comparison is kladde-v173 against kladde-v173). MAP cluster
**UNVERIFIED** — map *dimensions* repeat inside a match (e.g. `30x30` ×2 in `b6ec7f91`), and
dimensions are not map identities, so I could not run the "(match,map) pairs with >1 game"
test the worked example uses; treat the map cluster as possibly live. CONTENT-DUPLICATE
cluster **DEAD in the KLADDE cell** (0/25 duplicates, §0.3). Surviving correction applied =
within-opponent **1.434**. **Direction:** this is an EXCLUSION claim (reach rose), so the
widening makes it harder — the correct direction, and it still excludes zero.

⚠ **Confound to state: the KLADDE cell has no seat variation — we were seat B in 25 of 25
games.** MIRROR and PIVOT are 15 A / 5 B. A seat effect cannot be separated from the
kladde result.

### 1.2 …and the finishing bar did not move at all

Median damage delivered into their core is **198–243 of the 500 required**. We reach, we
put roughly two fifths of a core down, and then we stop. Damage into **our** core across
all 63 losses:

```
sentinel 32,886 (91.8%)   gunner 2,933 (8.2%)   builder attack 14 (0.0%)
```

**The single kill channel against us is the enemy forward sentinel, in all three cells.**
It is the dominant source in 59 of 63 losses; the 4 exceptions (`5ee3afec/4`, `64a8beb6/1`,
`ab068a0d/3`, `e200bcab/4`) are gunner-dominant and all Pivot-shaped, and even there the
sentinel contributes 216–288.

---

## 2. ⭐⭐⭐ THE GAME WE TOOK OFF BEAN COUNTERS WAS **NOT A DAMAGE KILL** — IT WAS A CRASH CASCADE

`5ee3afec_game_2` (30×30, our seat B, 75 rounds) is recorded in HANDOVER as *"the first
game ever taken off BC's doctrine."* The wire says what actually happened, and it is a
Loki-class result, not a Skalman-class one.

### 2.1 The measurement

```
r48   we build ONE sentinel #139 at (7,6), d² = 25 from BC's core footprint  (COPY-5 band)
r50-r72  it fires every 2 rounds into (3,2): 12 shots x 18 = 216 damage
r74   BC's CORE is REMOVED with 284 of 500 HP REMAINING   <- not a damage kill
```

And from **r46**, twenty-eight rounds before the end:

| BC builder | born | died | age | HP at removal |
|---|---|---|---|---|
| #126 | r46 | r47 | **1** | **40/40** |
| #133 | r47 | r48 | 1 | 40/40 |
| #138 | r48 | r49 | 1 | 40/40 |
| #141 | r49 | r50 | 1 | 40/40 |
| #144 | r50 | r51 | 1 | 40/40 |
| #150 | r51 | r52 | 1 | 40/40 |
| #156 | r52 | r53 | 1 | 40/40 |
| #183 | r59 | r60 | 1 | 40/40 |
| #200 | r66 | r67 | 1 | 40/40 |
| #219 | r73 | r74 | 1 | 40/40 |

**BC's four doctrine builders (#3, #5, #7, #9) are ALIVE AT THE END and acting normally
through r74** — verified move-by-move from r38 to r55 and their last action is r74. The ten
casualties are **fifth-and-beyond builders**, each destroyed on the turn after it spawned,
each at full HP, with no `updateHp` event of any kind.

### 2.2 The control that makes this unambiguous

| MIRROR game | BC builder bots built | extras beyond 4 | extras removed at age ≤1, full HP | BC core residual HP |
|---|---|---|---|---|
| 19 of 20 games | **exactly 4** | 0 | **0** | — (core never died) |
| **`5ee3afec/2`** | **14** | **10** | **10** | **284/500** |

Across **all 65 games** of the first-contact set, the count of enemy units removed at
age ≤ 1 with full HP is **10 — all ten of them in this one game.** BC's own
`exactly_four_builders` signature is 95.0% on the live tape (19/20) and the one violation
is the one game we won.

### 2.3 The reading

Per CLAUDE.md's engine facts: an uncaught exception escaping `run()` makes the engine
**permanently destroy that unit** (`0x1ac5c` → `Game::destroy_entity`); a CPU timeout does
not. A unit removed at full HP one round after birth, with no damage event, has exactly two
wire-compatible explanations — **an uncaught exception, or a voluntary `self_destruct()`**
— and `crash_census.py`'s docstring names that conflation itself. The core's removal at
284/500 admits `resign()` as a third.

**INFERENCE (strong, and labelled): this is a crash cascade, not a design.** A bot whose
four doctrine builders are alive and working, which holds a live gunner, whose core is at
57% HP, and which spawns a fifth builder every round for 28 rounds only to have it vanish
at full HP, is not executing `self_destruct()` ten times and then `resign()`ing. **The
MEASURED part is the full-HP removals, the exactly-4 control at 19/20, and the 284-HP
core.** The exception itself is not on the wire (platform replays carry no traceback and
strip stdout — CLAUDE.md s28/s54).

### 2.4 ⛔ THE TRIGGER IS **NOT** IDENTIFIED, AND THE OBVIOUS CANDIDATE IS REFUTED

The cascade begins at **r46**, the same round our first barrier landed on BC's core ring at
d² = 1, tile **(4,3)**. That is the whole of the temporal evidence, and it does not survive
a base-rate check:

```
games in which we placed >=1 barrier at d^2 <= 2 of the enemy core:   65 of 65
median round of our first such barrier:                              r39  (range r16-r147)
games showing the crash signature:                                   1 of 65
```

**We put barriers on the enemy ring in every single game of the set, and in 64 of them
nothing happened.** So "ring barrier at d²≤1" is *not* the trigger, and r46 is not even an
unusually early one. Nothing else about our play in that game is distinguishable from the
other nineteen: 4 builders, 5 harvesters, 17 conveyors, 5 barriers, 1 sentinel, 2 gunners,
**0 launchers, 0 throws.**

⇒ **The successor inherits a reproducible-looking anchor with an unknown cause.** The
cheapest next step is not analysis: it is **`fcode match unrated <Bean counters> --match
5ee3afec…`** (version-pinned re-run, CLAUDE.md's documented pinning capability) plus the
same map and seat, to see whether the cascade is deterministic. If it is, the trigger can be
bisected by local arms. **This is the single highest-value lead in the whole decode, and it
is off the Skalman axis entirely — it is crash-induction, the standing-permission class.**

---

## 3. KLADDE CELL — THE AMENDED BAR, PER GAME

**Definitions.** *Killer* = the single enemy entity that dealt the most damage into our core
(damage ledger, §0.2). *REACH-tile* = **any** turret of ours ever had the killer's firing
tile inside its attack **radius** — a deliberate **facing-free UPPER BOUND**: it ignores
facing and obstacles, so a `False` means we could not have covered that tile under *any*
facing. *REACH-path* = the same test against the tiles walked by the builder that planted
it, over the 12 rounds before the plant. *Answer latency* = rounds from the killer's build
to the first damage event on it (the standing column).

| game | map | killer | sited | d² to our core | REACH tile | REACH path | answered | **latency** | killer died | our 1st dmg on them | their 1st dmg on us | our dmg total | our core dies | our turrets |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0de59936/1 | 24×24 | sentinel #53 | r39 | 13 | ✗ (best 17) | ✓ | ✓ | 12 | — | r45 | r40 | 198 | **r94** | 3 |
| 0de59936/2 | 28×18 | sentinel #115 | r54 | 13 | ✓ | ✓ | ✗ | — | — | r72 | r55 | 252 | r92 | 1 |
| 0de59936/3 | 30×30 | sentinel #272 | r184 | 8 | ✗ (52) | ✓ | ✓ | 20 | r215 | r28 | r185 | 252 | r524 | 6 |
| 0de59936/4 | 20×20 | sentinel #212 | r448 | 16 | ✗ (25) | ✓ | ✓ | 19 | r486 | r21 | r449 | 144 | r521 | 4 |
| 0de59936/5 | 20×20 | sentinel #141 | r63 | 4 | ✗ (40) | ✗ (25) | ✗ | — | — | — | r64 | **0** | r91 | 2 |
| 82a03bfd/1 | 24×24 | sentinel #53 | r39 | 13 | ✗ (17) | ✓ | ✓ | 12 | — | r45 | r40 | 198 | r94 | 3 |
| 82a03bfd/2 | 18×18 | sentinel #143 | r77 | 25 | ✓ | ✓ | ✗ | — | — | r17 | r78 | 342 | r114 | 2 |
| 82a03bfd/3 | 30×30 | sentinel #273 | r184 | 8 | ✗ (52) | ✓ | ✓ | 16 | r213 | r28 | r185 | 270 | r717 | 7 |
| 82a03bfd/4 | 30×30 | sentinel #249 | r241 | 13 | ✗ (17) | ✓ | ✓ | 26 | r292 | r75 | r243 | 288 | r370 | 4 |
| 82a03bfd/5 | 20×20 | sentinel #141 | r63 | 4 | ✗ (40) | ✗ | ✗ | — | — | — | r64 | 0 | r91 | 2 |
| abd8f4fc/1 | 20×20 | sentinel #327 | r392 | 2 | ✓ | ✓ | ✗ | — | — | r21 | r394 | 144 | r448 | 2 |
| abd8f4fc/2 | 20×20 | sentinel #455 | r302 | 25 | ✗ (25) | ✗ | ✓ | 26 | — | r28 | r303 | 368 | r357 | 5 |
| abd8f4fc/3 | 30×30 | sentinel #103 | r67 | 8 | ✗ (17) | ✓ | ✓ | 13 | r98 | r28 | r68 | 72 | r158 | 3 |
| abd8f4fc/4 | 28×18 | sentinel #115 | r54 | 13 | ✓ | ✓ | ✗ | — | — | r72 | r55 | 252 | r92 | 1 |
| abd8f4fc/5 | 30×30 | sentinel #191 | r82 | 4 | ✗ (29) | ✗ | ✓ | 13 | — | r51 | r83 | 144 | r111 | 4 |
| b6ec7f91/1 | 24×24 | sentinel #124 | r83 | 25 | ✗ (**337**) | ✗ (146) | ✓ | 8 | — | r117 | r38 | 36 | r119 | 1 |
| b6ec7f91/2 | 30×30 | sentinel #191 | r82 | 4 | ✗ (29) | ✗ | ✓ | 13 | — | r51 | r83 | 252 | r111 | 4 |
| b6ec7f91/3 | 24×24 | sentinel #53 | r39 | 13 | ✗ (17) | ✓ | ✓ | 12 | — | r45 | r40 | 198 | r94 | 3 |
| b6ec7f91/4 | 20×20 | sentinel #141 | r63 | 4 | ✗ (40) | ✗ | ✗ | — | — | — | r64 | 0 | r91 | 2 |
| b6ec7f91/5 | 20×20 | sentinel #195 | r370 | 25 | ✗ (17) | ✓ | ✓ | 41 | — | r21 | r371 | 180 | r433 | 5 |
| d18b7d7b/1 | 12×12 | sentinel #179 | r176 | 25 | ✓ | ✓ | ✓ | 13 | r214 | r11 | r177 | 198 | r282 | 1 |
| d18b7d7b/2 | 30×30 | sentinel #233 | r161 | 25 | ✗ (20) | ✗ | ✓ | 27 | r207 | r34 | r162 | 522 | r329 | 6 |
| d18b7d7b/3 | 16×16 | sentinel #418 | r226 | 25 | ✓ | ✓ | ✓ | 17 | r262 | r18 | r228 | 828 | r275 | 1 |
| d18b7d7b/4 | 30×30 | sentinel #191 | r82 | 4 | ✗ (29) | ✗ | ✓ | 13 | — | r51 | r83 | 144 | r111 | 4 |
| **d18b7d7b/5** | 24×24 | **— WE WIN —** | — | — | — | — | — | — | — | **r45** | **never** | **500** | **survives** | 3 |

**Cell aggregates (24 losses):**

| bar | KLADDE | MIRROR | PIVOT | ALL (63 losses) |
|---|---|---|---|---|
| killer's tile inside a turret of ours (radius UPPER bound) | **6/24 = 25%** | 11/19 = 58% | 7/20 = 35% | 24/63 = 38% |
| killer's approach path inside a turret of ours | 15/24 = 62% | 14/19 = 74% | 10/20 = 50% | 39/63 = 62% |
| killer answered at all (≥1 damage event) | 71% | 74% | **100%** | 81% |
| **median answer latency** | **13 rnd** | 13 rnd | **5 rnd** | 12 rnd |
| killer killed | 33% | 21% | 25% | 27% |
| median siting round of the killer | r82 | r54 | r91 | r82 |

**The killer is a sentinel in 24 of 24 kladde losses, 63 of 63 losses overall.**

**Read.** In **three quarters of kladde losses we could not have covered the killer's tile
under any facing** — the sentinel is sited outside every turret we own, at a median d²=13
from *our* core. The approach path is coverable more often (62%), which is where a
counter-battery could act, but our median answer arrives **13 rounds** after the gun is
already firing at 9 HP/round. **The gap is siting-and-speed, not aim** (INFERENCE; the
MEASURED inputs are the radius test, the latency distribution and the 33% kill rate).

### 3.1 The forward-turret mirror control — the s54 numbers next to the s52-era numbers

Same function, same files, both directions. *Forward turret* = gunner/sentinel built within
d² ≤ 50 of the opposing core; *answered* = ≥1 damage event on it.

| direction | n | answered | median latency | killed | median life |
|---|---|---|---|---|---|
| **KLADDE: their forward turrets → answered by US** | 87 | **48%** | 13 | 30% | 34 |
| — the same cell at v175-v177 (STUDY §4.1) | 164 | 26% | 14 | 27% | 38 |
| **KLADDE: our forward turrets → answered by THEM** | 55 | **91%** | 4 | 89% | 9 |
| — the same cell at v175-v177 | 81 | 96% | 1 | 94% | 6 |
| MIRROR: theirs → answered by us | 86 | 43% | 10 | 44% | 27.5 |
| MIRROR: ours → answered by them | 33 | 70% | 8 | 70% | 14 |
| PIVOT: theirs → answered by us | 91 | 57% | 5 | 55% | 20 |
| PIVOT: ours → answered by them | 50 | 84% | 4.5 | 80% | 10 |

```
we answer kladde's forward turrets   26.2% (n=164) -> 48.3% (n=87)   +22.1pp
                                     95% hw 14.7pp (DEFF 1.434, within-opponent)  EXCLUDES ZERO
they answer ours                     96.3% (n= 81) -> 90.9% (n=55)    -5.4pp
                                     95% hw  9.6pp                     includes zero — NO CHANGE
```
⚠ Cluster enumeration: MATCH live, OPPONENT dead (within kladde-v173), CONTENT-DUPLICATE
dead in this cell (0/25), MAP unverified. ⚠ The second row is a **fail-to-exclude** result
and is stated as such — *no evidence their answer rate moved* — not as "unchanged".

**⇒ Our answer rate roughly doubled and their answer rate did not move. The asymmetry that
the s52/s54 studies called the crack is still 43 points wide.**

### 3.2 The kladde 1-4 arc: `d18b7d7b_game_5` — **what won it was a builder, not a gun**

24×24, our core (18,18), theirs (4,4), 321 rounds, we win. **kladde put ZERO damage on our
core in 321 rounds.**

```
r33-r40   3 harvesters, home
r38-r78   SEVEN barriers on kladde's core ring at d^2 = 1: (5,6) (4,6) (3,5) (3,4) (4,3) (5,3) (6,4)
r42       sentinel #52 @(0,0), d^2 = 32 exactly (the band's outer edge) -> answered r142, dies r146
r51       sentinel #66 @(0,9), d^2 = 32 exactly                        -> answered r91,  dies r96
          the two sentinels deal 54 of the 500 damage between them
r79-r320  builder bot #6 (born r1) stands adjacent to their core and MELEES IT
          223 builder attacks on the footprint x 2 dmg = 446 damage (89.2% of the kill)
          #6 takes ZERO damage all game (0 HP events, alive at end)
r320      final blow, builder #6, from (6,5)
```
Damage into their core, by 50-round band: `54 · 42 · 94 · 84 · 92 · 92 · 42` — a flat
2 HP/round grind for 241 rounds.

**What the taken game did differently: it sealed seven ring tiles and then parked an
un-answered builder on the core.** MEASURED: the seal, the melee count, and the zero damage
taken. **INFERENCE:** the ring seal is what left kladde with no siting tile from which a
sentinel line reached our builder — kladde built 4 sentinels and 2 gunners that game and
none of them ever damaged #6.

⚠ **PROGRAMME: this win is r320. It is on the wrong side of the r300 guard**, and its
mechanism is a 241-round strangle, which is the shape `R1000_IS_DEFEAT` was written against.
It is banked as a mechanism, not as a target.

---

## 4. MIRROR CELL — FIDELITY IN CONTACT vs THE NOISE_OFF FIXTURE

Subject = us (v180), one seat per run (`fid.sh`'s rule: a single `--side` over a both-seat
directory mis-attributes half the games). **Fixture reference = `scratchpad/s54_v620/t_ctrl_f1`,
the v620 grid's CONTROL arm on the NOISE_OFF `_v542wave` fixture, 15 maps × 2 seats** —
i.e. the line head, ≡ v619 ≡ v180 behaviourally per HANDOVER. **Live BC v68** is the same
instrument run on BC's side of the 20 mirror games, which is the first time these columns
have had a live target rather than a study-era one.

| metric | **FIXTURE A** | **FIXTURE B** | **MIRROR us** | PIVOT us | KLADDE us | **BC v68 LIVE** | BC study target |
|---|---|---|---|---|---|---|---|
| M1 belt connectivity (directed) | 42.1 | 30.3 | **17.4** | 46.2 | **19.6** | **90.4** | 81.4 |
| M2a cage ring share | 76.7 | 60.3 | 64.2 | 51.7 | **41.1** | 38.8 | 39.6 |
| M2b **full seal rate** | 0.0 | 0.0 | **0.0** | 0.0 | 0.0 | **50.0** | 22.2 |
| M2c first ring build (median r) | 39.5 | 32 | 33 | 39 | **58.5** | 45.0 | 52.0 |
| M2d ring tiles held (median max) | 4 | 6 | 6 | 4 | **2** | **7** | 6.0 |
| M3a **drip lattice share** | 100 | 100 | **100** | 100 | 100 | 97.5 | 97.3 |
| M3b **converts / game (median)** | **49** | **51** | **11** | **18** | **15** | 51 | 67 |
| M3c **Ti converted / game (median)** | **504** | **536** | **130** | **173** | **162** | 430 | 650 |
| M3d peak ammo (median) | 34 | 24 | 24 | 22 | 24 | 28 | 26 |
| M3e first convert round (median) | **14** | **15** | **35** | 29.5 | 31 | 26.5 | 27.5 |
| M4a forward turret **band** share | 94.1 | 96.6 | 96.9 | 96.1 | 100.0 | **23.2** | — |
| M4b forward turret **point-blank** share | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | **73.2** | — |
| M5b exactly-four-builders share | 66.7 | 66.7 | 60.0 | 60.0 | 52.0 | **95.0** | 92.9 |
| M6a barriers on ore share | 1.8 | 2.5 | 1.2 | 2.8 | 2.7 | **39.7** | 37.9 |
| M7 forward-turret removal (home clearance) | 50.0 | 56.1 | 37.6 | 56.6 | **20.8** | 69.2 | 76.6 |

*(n: fixture 15 per seat; MIRROR/PIVOT 20; KLADDE 25; BC-live 20. Every share above is
pooled over games with the metric's own denominator — read the per-metric `n` in
`scratchpad/s54v_fid_*.json`.)*

### 4.1 ⭐ THE VERB THAT BREAKS IN CONTACT IS **THE DRIP**, AND IT BREAKS BY A FACTOR OF FOUR

```
fixture   49-51 converts/game, 504-536 Ti, first convert r14-15
contact   11-18 converts/game, 130-173 Ti, first convert r29-35
```
The **lattice** holds perfectly (100% of amounts are exact sums of 4s and 10s in all five
populations — COPY 7's acceptance test passes everywhere), and the **peak balance** holds
(22-24 against the 26 target: we never bank). **What collapses is volume and start time.**

**INFERENCE, and the two candidate mechanisms are separable by a later cut, not by this
one:** the drip's `need` is defined by *live turrets that will fire next round*, and in
contact our forward turrets live a median **9-14 rounds** against the fixture's much longer
lives — so a correctly-implemented drip converting for a battery that keeps dying will
convert less by construction. The competing mechanism is funding: **M1 belt connectivity
falls 42/30 → 17-20** in the MIRROR and KLADDE cells, i.e. the belt does not survive contact
and there is less titanium to convert. Both are consistent with the same numbers. **MEASURED:
the volume drop, the latency slip, the turret lifetimes, and the M1 drop. The causal
ordering is not established here.**

### 4.2 The cage half degrades gracefully; the seal never existed

Ring share 76.7/60.3 → 64.2 (MIRROR) → 41.1 (KLADDE), ring tiles held 4/6 → 6 → **2**, first
ring build r32-39.5 → r58.5 against kladde. **Full seal is 0.0% in every population we have
ever measured on this line — fixture and contact alike — while live BC seals 50% of its
mirror games and holds a median 7 of 8 tiles.** The seal is not a contact regression; it is a
capability the line has never had.

### 4.3 ⭐ COPY 5's DEPENDENCY, MEASURED LIVE FOR THE FIRST TIME — **WE COPIED THE WRONG ERA'S RULE**

```
forward-turret siting        v180: band 96.9-100%,  point-blank 0.0%
                          BC v68 : band 23.2%,      point-blank 73.2%
home-ring clearance (M7)     v180: 37.6 / 56.6 / 20.8      BC v68 live: 69.2
```
PLAYBOOK COPY 5 states the dependency explicitly: *"do not copy the point-blank plant
without the clearance verb"*, and prescribes **band-first until clearance measures at
parity**. **v180 executes that prescription with near-perfect discipline** — 96.9-100% in
the d² 14-32 band, zero point-blank plants, in every cell. **And it is the losing side of
the trade against the bot it is replicating**, which plants 73.2% point-blank *because* its
clearance runs at 69.2%.

The prescription is not wrong; **the dependency is simply not satisfied and the band plant
alone does not kill.** Our band sentinels sit at d²=25-32 and deliver 198-243 damage before
dying. **This is the sharpest actionable read in the fidelity column set: the band rule is
being followed, and following it is not enough.**

### 4.4 Where the real BC kills us, relative to the benchmark copy

Real BC v68 lands its first damage on our core at **median r36** and our core dies at
**median r121** — the fastest of the three cells, and it kills with a forward **sentinel** in
18 of 19 losses (one gunner-dominant). Against the NOISE_OFF `_v542wave` fixture the line
head takes **14/30 kills** and survives past r300 in several games; against the real BC it
takes **1/20**, and that one is the crash of §2. **The fixture and the field disagree by
roughly an order of magnitude on this line's kill rate** — the fixture is an authored
opponent and prioritises, it does not establish prevalence (`FIDELITY-READ-v602`'s own
rider), and this is the first measurement of the size of that gap.

### 4.5 The mirror 1-4 arc: `5ee3afec_game_2` — see §2

The taken game is the crash cascade. **What "landed" was one band sentinel at d²=25 and 216
damage; what won was BC's core being removed at 284/500 HP.** Read as a Skalman result it is
a false positive: the fidelity verbs did nothing unusual in that game.

---

## 5. PIVOT CELL — KILL MECHANISM, AND THE BELT-GUN SHAPE

**0-20. Every game ends `core_destroyed` with our core dying at median r159** (range
r107-r396), the latest median of the three cells. **The killer is a forward sentinel in
20/20 games**, sited at median r91, at **median d² = 25 from our core (range 13-25)** —
tighter and further out than either other cell (MIRROR median 18, range 1-32; KLADDE median
13, range 2-25); damage into our core
splits **sentinel 82.1% / gunner 17.9%** in this cell (against MIRROR 93.2/6.8 and KLADDE
99.9/0.1) — **Pivot is the one opponent whose gunners carry real weight**, and it fields
4.7 gunners/game against our 1.6.

**We answered Pivot's killer in 20 of 20 games at median latency 5 rounds — and killed it in
5 of 20.** That is the cell's whole story: **we shoot back fastest here and still lose every
game**, because a 40-HP sentinel outside our gunners' r²=13 takes more than our answer
delivers before it has removed 500 HP at 9/round.

### 5.1 The belt-gun shape (CUT-116) **did appear against us — in all three cells**

Stimulus per CUT-116 §3: an opponent gunner/sentinel whose **actual firing line** (facing
tracked through `rotate()` re-emissions; gunner ray stops at the first wall/occupied tile,
sentinel ray ignores obstacles) covers a **live conveyor/splitter of ours** at any round of
its life. *Cutter* = a belt tile of ours actually died on that line.

| direction | cell | turret lives | **belt-gun** | belt-cutter | median onset latency | **we/they REMOVED it** |
|---|---|---|---|---|---|---|
| **their turrets aimed at OUR belt** | MIRROR | 106 | 37 (35%) | 31 (29%) | **0 rnd** | 62% |
| | **PIVOT** | 147 | **48 (33%)** | **24 (16%)** | **0 rnd** | 60% |
| | KLADDE | 185 | 49 (26%) | 36 (19%) | **0 rnd** | **33%** |
| **our turrets aimed at THEIR belt** | MIRROR | 59 | 13 (22%) | 4 (7%) | 0 rnd | 77% |
| | PIVOT | 84 | 24 (29%) | 6 (7%) | 0 rnd | 75% |
| | KLADDE | 96 | 28 (29%) | 4 (4%) | 0 rnd | 75% |

**Two things fall out, and the second is the uncomfortable one.**

1. **Yes — Pivot runs the belt-gun shape against us: 48 of 147 turret lives (33%) are sited
   already aimed at a live belt tile of ours (median onset latency 0 — the stimulus exists
   at build), and 24 of them cut a belt tile.** The same shape appears in all three cells at
   26-35%, so it is a **field-wide habit, not a Pivot signature.**
2. **Our removal of THEIR belt-guns runs 33-62%, against CUT-116's BC benchmark of
   75.9% ± 3.1 — while THEIR removal of OUR belt-guns runs 75-77%, exactly at that
   benchmark.** The opponents in this set answer a gun on their supply line like the rank-1
   bot does; against kladde we answer it one time in three.

⚠ These are pooled turret-life shares, not the games-as-units estimator CUT-116 publishes,
so they are **not** interval-comparable to the ±3.1 figure; the direction of the gap is far
larger than any plausible estimator difference, but the number is a point read.

---

## 6. CROSS-CELL — FIRST-DAMAGE TABLE, ALL 13 MATCHES

Median first-damage round, both directions, per match (`—` = never reached):

| cell | match | opp ver | our 1st dmg on them (g1..g5) | their 1st dmg on us (g1..g5) | our core death (g1..g5) |
|---|---|---|---|---|---|
| MIRROR | 0e5b63ea | 68 | 66, 73, 34, 39, 53 | 26, 22, 58, 73, 11 | 168, 77, 116, 101, 139 |
| MIRROR | 4bc7ed13 | 68 | 20, 48, **—**, 59, 66 | 48, 45, 82, 36, 26 | 102, 79, 168, 170, 168 |
| MIRROR | 5ee3afec | 68 | 31, **50**, 13, 30, 59 | 26, **never**, 105, 55, 34 | 118, **—**, 149, 80, 118 |
| MIRROR | e46e55fd | 68 | 59, 61, 55, 15, 73 | 36, 23, 91, 63, 22 | 170, 121, 129, 135, 77 |
| PIVOT | 64a8beb6 | 249 | 49, 28, 34, 56, 34 | 70, 56, 94, 105, 92 | 159, 136, 157, 163, 159 |
| PIVOT | 919000f0 | 249 | 34, **—**, 34, 24, 17 | 92, 171, 94, 88, 126 | 159, 396, 157, 186, 193 |
| PIVOT | ab068a0d | 249 | 24, 34, 49, 45, 19 | 88, 94, 70, 30, 88 | 186, 157, 159, 127, 126 |
| PIVOT | e200bcab | 249 | 20, 50, 34, 95, 27 | 84, 72, 43, 88, 95 | 138, 107, 181, 111, 216 |
| KLADDE | 0de59936 | 173 | 45, 72, 28, 21, **—** | 40, 55, 185, 449, 64 | 94, 92, 524, 521, 91 |
| KLADDE | 82a03bfd | 173 | 45, 17, 28, 75, **—** | 40, 78, 185, 243, 64 | 94, 114, 717, 370, 91 |
| KLADDE | abd8f4fc | 173 | 21, 28, 28, 72, 51 | 394, 303, 68, 55, 83 | 448, 357, 158, 92, 111 |
| KLADDE | b6ec7f91 | 173 | 117, 51, 45, **—**, 21 | 38, 83, 40, 64, 371 | 119, 111, 94, 91, 433 |
| KLADDE | d18b7d7b | 173 | 11, 34, 18, 51, **45** | 177, 162, 228, 83, **never** | 282, 329, 275, 111, **—** |

**Reach failures are 5 games of 65 (7.7%) for us, 2 of 65 (3.1%) for them.** Three of our
five are `0de59936/5`, `82a03bfd/5`, `b6ec7f91/4` — 20×20, killer sentinel at d²=4 from our
core, our core dead at r91, **and they are the same game three times over** (§0.3). The
other two are `4bc7ed13/3` and `919000f0/2`, both 22×22. **Both of their two failures are
the two games we won.**

### 6.1 Turret reach coverage — summary

| | MIRROR | PIVOT | KLADDE |
|---|---|---|---|
| our turrets built (gunner+sentinel) / game | 3.0 | 4.2 | 3.8 |
| — of which forward (d² ≤ 50 of their core) | 56% | 60% | 57% |
| their turrets built / game | 5.3 | 7.4 | 7.4 |
| — of which forward | 81% | 62% | 47% |
| killer's tile inside ANY turret of ours (radius upper bound) | 58% | 35% | **25%** |

**We field roughly half the turret volume of every opponent in this set**, and the fraction
of our turrets that go forward is stable at ~57-60% across all three.

### 6.2 ⭐ EXCEPTION-DEATHS OF **OUR** UNITS — the commission expected 0, and the answer is effectively 0

Two independent instruments:

**(a) `tools/crash_census.py` (never-had-an-hp-event rule), 65 files, selftest passed:**

| side | builder_bot | gunner | sentinel | total |
|---|---|---|---|---|
| **US** | **0** | 3 | 0 | **3** |
| THEM | 10 | 91 | 62 | 163 |

**(b) residual-HP-at-removal ledger (this decode's own, control: 64/65 core deaths land on
exactly 0):**

| side | units removed while still alive |
|---|---|
| **US** | builder_bot **0/98** · sentinel **0/114** · core **0/63** · gunner 3/28 |
| THEM | builder_bot 10/19 · gunner 101/127 · sentinel 64/96 · core 1/2 |

**Nothing of ours crashed.** Zero of our 98 builder-bot deaths and zero of our 114 sentinel
deaths are unexplained; **the builder bot is the only kind for which `self_destruct()` and a
crash are the sole full-HP explanations, and we have none.** The 3 gunners are removals of
our own turrets at full HP — indistinguishable on the wire from a friendly `destroy()`, and
the v602 report already names an `_escape` full-HP demolition class in this tree, so they
are almost certainly ours-on-purpose. **Flagged for the builder as a self-audit item, not as
a crash.**

The opposite column is the interesting one: **163 enemy units vanish undamaged**, of which
**10 enemy builder bots** — and all 10 are the §2 cascade. The 91 gunner / 62 sentinel
full-HP removals are overwhelmingly opponents demolishing and re-siting their own turrets
(kladde and Pivot both do it) and are **not** evidence of crashes.

---

## 7. WHAT REFUTES A COMMISSION PREMISE

1. **"n = 65 games on 3 opponents."** True as a file count, **false as an independent-sample
   count**: 7 of 65 games are byte-identical repeats of another game in the same cell
   (MIRROR 15%, PIVOT 20%, KLADDE 0%). Effective n is **58**, and the MIRROR/PIVOT cells are
   ~16-17. §0.3.
2. **"the 13 matches' replays… 5 games each"** — confirmed, 65/65 present and decodable.
   No refutation.
3. **The carried claim that the jitter in kladde games is ours.** On this pool our side is
   byte-identical across a matched pair and **kladde's is not**. §0.4.
4. **"BC-mirror 1/20 incl. THE FIRST GAME EVER TAKEN OFF BC'S DOCTRINE" (HANDOVER).** The
   game was taken, but **not by the doctrine** — BC's core was removed at 284/500 HP after a
   28-round full-HP builder cascade. Attributing it to Skalman's cage/nest/drip is a false
   positive. §2.
5. **`cond` as a validation column.** It is constant (`core_destroyed` 65/65) and cannot
   fail; any decode that reports "win_condition reproduced 65/65" as evidence has reported
   nothing. §0.2.
6. **The commission's framing that reach is the open question.** Reach is **fixed** (88-95%,
   excludes zero against the v175-177 baseline). The open question is now **conversion**:
   198-243 damage of the 500 needed, and a forward turret that lives 9-14 rounds.

---

## 8. WHAT THIS DECODE DID NOT ANSWER

* **The trigger of the §2 crash cascade.** The obvious candidate (our ring barrier at d²≤1)
  is refuted by a 65/65 base rate. Needs a **pinned re-fire on the same map and seat**
  (`--match 5ee3afec…`), not more decoding.
* **Whether the drip's collapse in contact is turret-lifetime-driven or funding-driven.**
  Both mechanisms fit the same numbers (§4.1). The discriminator is a per-round trace of
  `need` against balance, which this pass did not extract.
* **Whether the seal's absence is eviction, funding or an unreached acceptance threshold** —
  `FIDELITY-READ-v602`'s open item #1, still open at 0.0% full seal in every population.
* **Seat.** The KLADDE cell is 25/25 seat B; no seat contrast exists in it.
* **Map identity.** Map *dimensions* are recorded, map identities are not, so the MAP
  cluster of the DEFF enumeration could not be verified and is carried as possibly-live.

---

## 9. REPRODUCTION

```bash
.venv/bin/python scratchpad/s54_fc_decode.py                  # 65-game decode + validation
.venv/bin/python scratchpad/s54_fc_facing.py  MIRROR,PIVOT,KLADDE   # their turrets vs our belt
.venv/bin/python scratchpad/s54_fc_facing2.py MIRROR,PIVOT,KLADDE   # our turrets vs their belt
.venv/bin/python tools/skalman_fidelity.py --manifest scratchpad/s54v_fc_MIRROR_us.tsv \
    --label "FC MIRROR us(v180)" --era v68 --json scratchpad/s54v_fid_MIRROR_us.json
.venv/bin/python tools/crash_census.py --selftest
```
Artefacts: `scratchpad/s54_fc_games.json` (per-game decode), `scratchpad/s54v_resid.json`
(residual-HP ledger), `scratchpad/s54v_crash.json`, `scratchpad/s54v_fid_*.json`,
`scratchpad/s54v_fc_*.tsv` (manifests), `scratchpad/s54_fc_facing*.tsv`.

⚠ **`s54_fc_facing{,2}.py` default their version filter to `{'47','68'}` and silently write
an empty table if run with no argument.** Pass the cell names.
