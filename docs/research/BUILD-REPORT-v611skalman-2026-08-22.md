# BUILD REPORT — `bots/_v611skalman`: SK_HOME_LAUNCHER, a DEFAULT-OFF measured arm

**Builder s54, 2026-08-22T02:49Z (`date -u` in the same shell).** Copy of
`_v610skalman` + ONE arm, `SK_HOME_LAUNCHER`, **built complete and shipped
DEFAULT OFF**. Artefacts `scratchpad/s54_v611/`. Fixture = the authored
NOISE_OFF `_v542wave` benchmark copy, 15 pool maps × both seats = 30 games, seed
pinned at 7 (map/seat vary, seed never). No game-share claim, no submit, no
platform match, no commit.

**⛔ NO ADOPTION LANGUAGE IN THIS DOCUMENT, BY COMMISSION.** The arm is a
phase-boundary question (the ratified structure gates AMPLIFY on parity; the
benchmark ships launchers and our replication chassis ships none). This report
is the dose table that informs Magnus's decision. It says what the arm does and
what it costs, and it does not say what to do about it.

---

## 0. THE HEADLINE, IN ONE TABLE

30 games, treadmill-fixed chassis, every arm re-run and never reused.
`OFF` is byte-identical to the v610 shipped tape in 30 of 30 replays.

| arm | kills | **by-r300** | med kill | core-dead | **M1 A/B** | **gap-0** | **1-barrier class** | **Ti** |
|---|---|---|---|---|---|---|---|---|
| **OFF** (= v610 ship, identity 30/30) | **14** | **11** | 188.5 | 16 | 34.2 / 33.3 | 45.6% | 39.7% | 12,940 |
| **ON** (arm as designed) | 10 | 9 | 220.5 | 18 | **50.9 / 48.5** | **69.8%** | **17.4%** | **21,310** |
| **ON, density off** (`geom`) | 12 | **11** | 220.5 | 16 | 41.2 / 48.4 | 64.6% | 17.1% | **22,270** |

**THE ARM DOES EXACTLY WHAT THE v610 QUEUE SAID IT WOULD, AND THE CAP IT WAS
BUILT TO LIFT MOVES FURTHER THAN ANY PLANK THIS LINE HAS SHIPPED.** M1 belt
connectivity goes 34/33 → **51/49** (v610's PLANK 1, "the best this line has
read", reached 36.8/37.1). The one-barrier class — the structural cap named in
the v610 report — goes **39.7% → 17.4%**. Delivered titanium goes **+65%**.
Harvesters the BFS calls UNREACHABLE at end of game go **24 → 5**.

**AND ON THE STATED CURRENCY IT IS A NEGATIVE AS DESIGNED AND A NULL AS
ABLATED.** by-r300 11 → 9 with the density term on; **11 → 11 with it off**,
where kills read 12 and delivered Ti is *higher* still.

---

## 1. THE MECHANISM, AND THE FIXTURE FACT THAT NOBODY HAD

⭐⭐ **`_v542wave` SHIPS LAUNCHERS AND FERRIES ITS OWN BUILDERS WITH THEM. THE
OFF TAPE ALREADY CONTAINS 404 THROWS AND 217 OF THEM ARE OUR BODIES BEING
KIDNAPPED.** Probed while building the instrument (auroraveil seat A): team-B
`launcher` planted at (9,15) r5 and (10,9) r7; their own builder 4 thrown
(10,16)→(10,10), d²=36, r6. Pooled over the 30-game OFF tape:

```
THEIR throws            404  (13.5/game)   of which their own ferry  187
                                            of which OUR bodies      217
OUR throws                0
```

**CONSEQUENCE FOR EVERY THROW INSTRUMENT THIS PROJECT WILL EVER WRITE: "a
builder jumped more than one tile" is true 404 times in the CONTROL tape and is
not our throw.** `scratchpad/s54_v611/throws.py` therefore attributes every jump
to a specific live launcher by the engine's own two bounds (pickup d² ≤ 2 from
the origin, 1 ≤ d² ≤ 26 to the destination, both measured from the launcher) and
reports multi-team candidates as AMBIGUOUS rather than assigning them.

**⭐ THE ATTRIBUTOR IS VALIDATED AGAINST THE BOT'S OWN COUNTER, EXACTLY:**
the tree's `hl_throws` counter, read off stderr on a re-run of the identical
30 games, reads **391**. The replay attributor reads **352 attributed + 39
ambiguous = 391**. Zero missed, zero misattributed; the ambiguity is
conservative and the residual is named.

---

## 2. THE DOSE TABLE

### 2.1 Throws, victims, displacement, return

| | **ON** | **geom** |
|---|---|---|
| our throws | 352 (11.7/game) | 432 (14.4/game) |
| games with ≥ 1 throw | 16/30 | 18/30 |
| launcher BUILT | **24/30 games, median r17** | 23/30, median r16 |
| launcher DIED | **1 of 24** (median life 487 r) | 1 of 23 |
| victim kind | **builder_bot 352/352** | builder_bot 432/432 |
| **⛔ own-team victims** | **0** | **0** |
| victim was seat-adjacent at pickup | 209/352 = **59.4%** | 249/432 = 57.6% |
| displacement d² | median **16**, mean 16.6, max 41 | median 16, mean 16.7, max 41 |
| displacement, tiles (Chebyshev) | median **4**, max 6 | median 4, max 6 |
| re-thrown before returning | **308 of 352** | 379 of 432 |
| **RETURN, strict** (back to a tile that can work one of our 8 seats) | 22/44, median **6 r** | 28/53, median 4 r |
| **RETURN, generous** (back inside our home ring, d² ≤ 13) | 30/44, median **3 r** | 35/53, median 2 r |

⛔ **READ THE RE-THROW ROW BEFORE THE RETURN ROWS.** 308 of 352 throws land on a
body that has walked back into the launcher's **pickup disc** but not back onto
a tile from which it can work a seat. That is the mechanism working — the
launcher runs a treadmill on the same collar-layer — and it is also why the
strict-return denominator is 44 and not 352. A re-throw is not a censored
return and is excluded from both denominators; reporting it as censoring would
have inflated the effect roughly eightfold.

**Their body comes back FAST — median 3 rounds to the home ring, 6 to a working
tile — and is thrown again.** The displacement is 4 tiles, not a removal.

### 2.2 The re-lay interruption

| | OFF | ON | geom |
|---|---|---|---|
| enemy building placements on OUR 8 seats | 204 (2.82 / 100 r) | 183 (**2.31**) | 180 (2.36) |
| enemy occupancy EPISODES on our seats | 204 (6.8/game) | 186 (6.2) | — |
| **their RE-LAY events after our seal dies** | **16** | **8** | — |
| enemy-held seats at END (median) | 6.5 | **5.0** | 5.0 |
| enemy-held over the GAME (median of medians) | 7.0 | **5.0** | — |
| enemy barriers on our seats at end | 180 | **155** | 157 |
| first enemy building on a seat | r11, 30/30 | r11, 30/30 | r11, 30/30 |

**The collar still lands at r11 in 30 of 30 games — the arm does not prevent the
cage, it thins it.** Seats held drop by 1.5 of 8; their re-lay events halve.

### 2.3 THE CAP LIFT (the number the arm was commissioned for)

| | OFF | ON | geom | v610 PLANK 1 (for scale) |
|---|---|---|---|---|
| **M1 belt connectivity, seat A / B** | 34.2 / 33.3 | **50.9 / 48.5** | 41.2 / 48.4 | 36.8 / 37.1 |
| harvesters alive at end | 68 | **86** | 82 | 54 |
| gap 0 (route home COMPLETE) | 45.6% | **69.8%** | 64.6% | — |
| **ONE-BARRIER CLASS** | 39.7% | **17.4%** | 17.1% | 29.6% |
| one-build-from-home TOTAL | 44.1% | **19.8%** | 22.0% | — |
| UNREACHABLE harvesters | 24 | **5** | — | — |
| **Ti collected** | 12,940 | **21,310** | **22,270** | 12,750 |

**M1 target is 83 (the benchmark). This is the first arm on this line to reach
half of it.**

### 2.4 The kill line

| | OFF | ON | geom |
|---|---|---|---|
| kills | 14 | 10 | 12 |
| **by-r300** | **11** | 9 | **11** |
| median kill round | 188.5 | 220.5 | 220.5 |
| our core dead | 16 | 18 | 16 |
| unanswered-streak median / max / ≥40 | 13.0 / 95 / 6 | 15.0 / 61 / 2 | 14.0 / 55 / **1** |
| loss channel | 16/16 sentinel | table WITHHELD (see §4) | 17/18 sentinel |

**Kill-line cells that moved (ON vs OFF):** LOST 6 — `bifrost_B`,
`holmgang_A`, **`icefloe_A` (the v609 named recovery, r136 → died r164)**,
`skald_A`, `skald_B` (r118 → died r712), `stavkirke_B`. GAINED 2 —
`jotunheim_B`, `yggdrasil_A`.
**geom:** LOST 5, GAINED 3 (it recovers `stavkirke_B` and `helheim_B`, loses
`fimbulwinter_B`).

**The 12 named cells, OFF → ON → geom:**

| cell | OFF (= v610 ship) | ON | geom |
|---|---|---|---|
| icefloe A | **KILL r136** | died r164 | died r164 |
| helheim A | died r387 | died r192 | died r362 |
| midgard A | died r95 | died r95 | died r95 |
| midgard B | died r113 | died r69 | died r69 |
| fimbulwinter A | KILL r160 | KILL r224 | KILL r224 |
| fimbulwinter B | KILL r150 | KILL r166 | r1000 tie |
| bifrost A | died r157 | r1000 tie | r1000 tie |
| longhouse A | died r297 | died r222 | died r115 |
| paths A | KILL r605 | **KILL r145** | **KILL r145** |
| stavkirke A | KILL r294 | KILL r268 | KILL r268 |
| helheim B | died r144 | died r137 | **KILL r202** |
| skald B | KILL r118 | died r712 | died r147 |

⚠ **28 of 30 CELLS CHANGE UNDER THIS ARM.** One home building rewrites the whole
tape. That makes every per-cell attribution weaker than usual and it is why the
±2 columns below are reported and not claimed.

### 2.5 Dose curve

| arm | kills | by-r300 | med kill | core-dead | Ti | note |
|---|---|---|---|---|---|---|
| OFF | 14 | **11** | 188.5 | 16 | 12,940 | identity control |
| `SK_HL_MIN_ROUND = 0` | 10 | **5** | 296.0 | 17 | 21,320 | buy before the collar is visible |
| **`= 10` (designed)** | 10 | 9 | 220.5 | 18 | 21,310 | |
| `= 25` | 8 | **5** | 221.5 | 21 | 18,330 | buy after the cage is shut |
| `SK_HL_SEAT_DENSITY = False` | **12** | **11** | 220.5 | **16** | **22,270** | pure geometry |
| `SK_HL_VICTIM_SEAT_ONLY = True` | 10 | 9 | 220.0 | 18 | 17,040 | strict collar-layer only |
| `SK_HOME_LAUNCHER_MAX = 2` | 9 | 7 | 188 | 19 | 14,670 | partially unreachable, §4 |
| ⛔ `SK_HL_TEAM_CHECK = False` | **7** | **5** | 236 | 21 | **8,690** | DIRTY control |
| ⛔ `SK_HL_DROP_RING_DSQ = 0` | 11 | 8 | 224 | 18 | 12,180 | DIRTY control¹ |
| ⛔ `SK_HL_THROW_MIN_DSQ = 4` | 9 | 8 | 224 | 18 | 20,780 | short-throw siting¹ |
| ⛔ `SK_HL_RESERVE = 0` | 11 | 9 | 224 | 17 | 21,800 | ¹ |

¹ measured on the chassis *before* the treadmill fix (§3); the three arms above
the line were re-run on the fixed chassis and are directly comparable.

**THE TIMING DOSE IS THE SHARPEST READING IN THE TABLE: by-r300 reads 5 / 9 / 5
at r0 / r10 / r25.** The window is narrow and it is the window the census
predicted — the first enemy building lands at median r11.

**AND THE DENSITY TERM IS A MEASURED NEGATIVE.** Weighting the site by observed
seat occupancy is worse than plain geometry on every primary column (kills 10 vs
12, by-r300 9 vs 11, core-dead 18 vs 16, Ti 21,310 vs 22,270). The designed
value is kept as the flag default so the arm is reported as designed; the flag
comment now carries the measurement.

---

## 3. ⛔ THE DEFECT THIS BUILD FOUND IN ITSELF, AND IT IS v610's LESSON REPEATING

**THE FIRST CUT MEMOISED THE LAUNCHER SITE FOR THE WHOLE GAME AND NEVER
RE-VALIDATED IT.** Measured with the tree's own counters on stderr, 30 games:

```
launcher BUILT in                      19/30 games
keeper rounds spent WALKING at a site  1,183
worst single game (fimbulwinter B)     656 keeper rounds, can_build_launcher
                                       False 324 times, launcher NEVER built
```

**656 keeper rounds walking at one dead tile — in the arm built precisely
because "the keeper's turn is the scarce resource".** fimbulwinter seat B is one
of the kill-line cells the arm lost. `SK_HL_SITE_GIVEUP = 12` (ban the site and
re-pick) + `SK_HL_SITE_TRIES = 2` (give up for the game) fixes it:

```
                     first cut      fixed
keeper walk rounds     1,183          209    (-82%)
worst single game        656           18
launcher built in       19/30        24/30
throws                   368          391
```

**The fix recovered the keeper's turns and did NOT recover the kill line**
(10 / 9 both before and after). That is what makes the by-r300 reading a
statement about the mechanism rather than about my bug.

---

## 4. THE FIVE COST LINES

**(1) SCALE.** One launcher is **+10 percentage points on the ONE GLOBAL
ADDITIVE cost factor**, which stands at **190–271% (median 219%)** when the buy
lands — i.e. a **~4.6% relative rise in the price of every later build of every
type**, the second sentinel included. Downstream, measured:

| | OFF | ON | geom |
|---|---|---|---|
| 2nd door-gun median round | 65.5 | **93** | 97.5 |
| 2nd sentinel median round, **in the games we LOST** | r51 | (withheld) | **r102** |
| funding-wait GAMES | 18/30 | 19/30 | 17/30 |
| funding-wait ROUNDS (S1→S2) | 1,068 | **1,719** | 1,562 |
| S2 stood, in losses | 12/16 | 14/20 | 9/18 |

**The funding-wait revisit gets WORSE in rounds, not better, despite +65%
delivered titanium.** The launcher buys income and spends the thing the income
was for.

**(2) KEEPER ROUNDS.** After the treadmill fix: **209 walk rounds across 30
games (median 3 per game where it builds, max 18)** plus **one build turn**, plus
8 `get_tile_building_id` reads a round for the density census while the launcher
is unbuilt (≈ r0–r30). Against v610 PLANK 1's 1,018 extra keeper turns for a
four-point by-r300 loss, this is roughly a fifth of the price.

**(3) LAUNCHER SURVIVAL.** **It survives: 1 death in 24 builds**, median life 487
rounds. Their pecks do not answer it — their entire peck budget is still our belt
at our core (241 of 266 pecks in the ON tape).

**(4) THEIR COUNTER-KIDNAP GOES UP.** Their throws of OUR bodies: **217 (OFF) →
294 (ON) → 379 (geom)**, and our builder deaths **29 → 56 → 49**. We hold more
territory, we field more bodies, and more of them stand where their forward
launchers can reach. **This is the largest single cost in the table and it was
not predicted.**

**(5) CRASH-CLASS OBSERVATION — ZERO, AND NOT AIMED AT.** Thrown enemy builders
removed with **no damage event in the removal round: 0 of 352 (ON), 0 of 432
(geom)**; 7 and 5 respectively died with damage. No-damage builder removals of
any kind, either team, across all three tapes: **0**. The arm throws to the
FARTHEST passable tile toward the enemy, never to a border, and the channel did
not open by accident.

---

## 5. THE OTHER FINDING: A PRE-EXISTING v608 DEFECT, LOCATED AND NOT FIXED

The ON tape shows **23 pecks by our own builders on our OWN buildings** (0 in
OFF): bifrost B r100–111 into our conveyor at (24,3), skald A r86–92 into our
harvester at (7,5), yggdrasil B r81–82 into our conveyor at (26,24).

**LOCATED BY A DRIVEN PROBE, not by inspection:** a debug tree that reports the
call site of any `fire()` landing on a friendly tile names **`_counter_march`**,
6 times in bifrost alone. v608 PLANK 2 marches at the corefire shooter's
**LATCHED TILE** and has **no team check on what stands there now** — when the
enemy sentinel dies and our own belt is later built on that tile, the keeper
pecks it.

**NOT FIXED IN THIS TREE, deliberately: any fix would break the OFF arm's
byte-identity with v610 and confound the only control this experiment has.**
It is a one-line guard, it is a v612 item, and the anchor is
`sk_roles.py:_counter_march`, the `ct.fire(tgt)` at the end.

---

## 6. VERIFICATION

* **Static 13/13 scans PASS, 87/87 dirty controls FIRE** (14 new S13 controls
  for this arm, including "remove the team guard", "drop the treadmill bound",
  "let the site take a delivery seat", "raise the throw bound past the engine's",
  "ship the arm ON").
  ⭐ **Two S13 controls came back BROKEN on the first run and the hole was in the
  SCAN, not the tree** — `if self.hl_built >= SK_HOME_LAUNCHER_MAX:` appears in
  both the BUY and the WALK, and `path_arbiter_ok(ct, site, rnd)` also appears in
  `_cover_gun_action`, so a file-wide regex was satisfied by a different method.
  Fixed by scoping the assertions to the AST body of `_home_launcher_action`.
  **Second wave running in which the control battery caught the instrument.**
* **IDENTITY CONTROL: `SK_HOME_LAUNCHER = False` is byte-identical to the v610
  shipped tape in 30 of 30 replays.** The arm is provably inert with the flag off
  — no keeper build, therefore no launcher, therefore the `EntityType.LAUNCHER`
  dispatch branch is never reached.
* **ALIVENESS RUN WITH THE ARM ON** (a flags-off aliveness pass would not
  execute one line of it): 12 games, both seats, **0 tracebacks, 0 no-damage
  removals**; injected-NameError control fires (8 tracebacks, 8 no-damage builder
  removals).
* **THE THROW INSTRUMENT'S OWN SELFTEST: 7/7 CONTROLS FIRE** — pickup bound
  driven to 0 attributes nothing; throw bound driven to 1 attributes nothing;
  the side flip swaps ours/theirs exactly (337↔530); the seat-lay counter is
  side-dependent; the return detector produces both verdicts; the crash-class
  detector produces both verdicts. On the OFF tape, control 5 is reported
  **SKIPPED** rather than passed — that tape has 0 of our throws by construction
  and a vacuous 0/0 is not a pass.
* **⛔ THE DIRTY TEAM-CHECK CONTROL IS DRIVEN LIVE, NOT ASSERTED:** with
  `SK_HL_TEAM_CHECK = False` the launcher threw **542 of 1,295 bodies belonging
  to US**, and the arm reads kills 7 / by-r300 5 / Ti 8,690. The engine has no
  team check on `can_launch`; this is what it costs.
* **Fidelity, per seat** (seats split into manifests): drip lattice
  **100.0 / 100.0** (bar 97.3) · M4b forward point-blank **0.0 / 0.0** · M4d
  sentinel point-blank **0.0 / 0.0** · M1 **50.9 / 48.5**.
* **Tape reproduced from the shipped tree after the last edit:** `tapeF_off`,
  `tapeF_on`, `tapeF_geom` vs `tape3_*` — **0/30 differ each**; `tapeF_off` vs
  the v610 shipped tape — **0/30 differ**.
* **CPU wall-clock, 6 games: 9.57 s (v610) → 9.07 s (v611 arm ON). 0 engine
  timeouts and 0 tracebacks in the 30-game ON tape.** **Platform CPU test STILL
  OWED.**
* **THE LOSS-ANATOMY TABLE FOR THE ON ARM IS WITHHELD BY THE INSTRUMENT'S OWN
  CONTROL** — its S2-stood discriminator reads 0.70 in both won and lost games
  ("IDENTICAL, control did not fire"), and the tool refuses to print a table it
  cannot discriminate. Reported as withheld rather than worked around.
* **DISCLOSED, a bound that did NOT fire:** `SK_HOME_LAUNCHER_MAX` is a
  **per-BODY** counter, so a successor keeper can buy a second launcher. A
  team-wide bound was added (refuse if any friendly LAUNCHER is in
  `vis_friend`) and it is **inert on this fixture — 25 builds in 24 games both
  with and without it, and the ON tape is byte-identical across the change**.
  skald seat B still builds two, by a keeper that cannot see the first. The
  guard binds only the `MAX = 2` arm, which is therefore only partially
  reachable and whose row should be read with that caveat.

⚠ **FIXTURE CAVEAT on every number here:** ONE authored opponent, local screen,
30 games. Local balanced batteries read DEFF ≈ 0.98 so naive intervals are
approximately honest, but a ±2 on a 30-cell bar is not a resolvable difference
and is not claimed as one. **28 of 30 cells move under this arm**, which makes
the tape noisier than the usual plank, not less.

---

## 7. WHAT THE TABLE SAYS, WITHOUT SAYING WHAT TO DO

1. **The mechanism is confirmed and the aim is right.** The launcher reaches the
   collar-layer (59.4% of victims are seat-adjacent at pickup), displaces it 4
   tiles, and it comes back in a median of 3 rounds and is thrown again. Their
   re-lay events halve, seats held drop 6.5 → 5.0.
2. **The cap it was built to lift, lifts further than anything this line has
   shipped.** M1 34/33 → 51/49 against a benchmark of 83; the one-barrier class
   39.7% → 17.4%; unreachable harvesters 24 → 5; delivered Ti +65%.
3. **On the stated currency it is a negative as designed (by-r300 11 → 9) and a
   NULL as ablated (`geom`: 11 → 11, kills 12, Ti +72%).** The whole by-r300
   difference between those two arms is the site-scoring term.
4. **The cost is not the keeper's turn this time** (209 walk rounds + 1 build,
   against v610 PLANK 1's 1,018 pecks). **It is the second sentinel** — the
   +10-point scale pushes the second gun from r65 to r93 and the S1→S2 funding
   wait from 1,068 to 1,719 rounds — **and their counter-kidnap**, which rises
   217 → 294 with our builder deaths 29 → 56.
5. **The crash channel did not open and was not aimed at: 0 of 352.**
6. **`R1000_IS_DEFEAT` is untouched by this arm** — it converts no tiebreaks
   into kills on net, and the economy it buys is instrumental by the programme's
   own words.

---

## 8. v612 QUEUE

1. **`_counter_march` has no team check on its latched target tile** — 23 pecks
   into our own conveyor/harvester, located by a driven probe (§5). One line,
   pre-existing since v608, deliberately not fixed here.
2. **`SK_HL_SEAT_DENSITY` is a measured negative** (§2.5). If the arm is ever
   priced again, price it OFF first.
3. **Their counter-kidnap is the unpriced half of the launcher axis.** They
   threw 217 of our bodies in the CONTROL tape and 294–379 under the arm, and we
   have never measured what those throws cost us. The tree ships a displacement
   guard (`SK_TELEPORT_DSQ`, `raid.py`'s import); whether it covers the ECO
   builders is **still unknown and is now the cheapest open question on this
   axis**.
4. **The team-wide launcher bound is inert on this fixture** (§6). If `MAX > 1`
   is ever wanted, it needs a store slot and there are none free.
5. **Platform CPU test still owed** (standing).
