# v73 "Eir 7" production read — the pre-registered rev-4 mechanism read

**Status: COMPLETE.** Executes `docs/research/eir6b-production-read-spec-2026-08-07.md`
rev 3 (checks 0-8, the 6e base) and rev 4 (checks 9-13, the shipped graft),
against v73's **first two ladder matches**.

## Version tags and corpus (rule 2)

| | |
|---|---|
| **Subject** | **v73 "Eir 7"** = `bots/_v84g/main.py`, md5 `cbb0b8b449110f89be9765028fbf8c54` (re-verified on disk) |
| Base code-read for the diff | `bots/_v81e6e/main.py`, md5 `31a10eb2ff2d141db3460587b4c13f84` ("6e") |
| Bot dirs code-read | `bots/_v84g/` and `bots/_v81e6e/` only. No other bot source was opened. |
| Graft under test | E2b ore-pave ban + E1 peacetime ammo floor (CAPPED, `E1_RESERVE_CAP = 23`) + S1 intercept own-building guard — the entire `_v81e6e → _v84g` diff is 242 lines and contains nothing else |
| **Corpus** | **BOTH archived v73 windows**, zero downloads |
| Corpus A | `240a626c-18a3-4c25-bd49-7b7cc28bf003` — OpenSverige **v73** 3-2 Leviathan **v25**, ladder, completed 2026-08-08T04:35:25Z, Elo **+5.41**. We are replay **TEAM_A**. |
| Corpus B | `b5a37d0b-87f5-46c6-968b-ef19099d90f9` — 0033 **v43** 5-0 OpenSverige **v73**, ladder, completed 2026-08-08T04:46:24Z, Elo **−15.47**. We are replay **TEAM_B**. |
| **v73 ladder record** | **1W-1L matches, 3-7 on games, net −10.06 Elo** (1615.44 → 1620.85 → 1605.38) |

**Scope caveat, on every line below.** n = 10 games across **two** opponents,
one match each. This is a first-window *mechanism* read, not a trajectory
verdict. Per-check results are reported as CONFIRMED / FAIL-SIGNATURE-SEEN /
NOT-EXERCISED; KEEP/REFUTED is the builder's call. Several checks rest on ≤3
firing events and are marked accordingly.

**Channel limitation, stated once and load-bearing.** Replays carry `print()`
output only; **stderr is invisible in a replay**. `_v84g:1166` wraps the whole
dispatch in `try/except` and writes the traceback to **stderr**, once per unit.
So "zero diagnostic prints" is unmeasurable in production *by construction* —
every such check below is answered behaviourally, and the absence of an
exception trace in a replay is never evidence that no exception fired. Both
corpora contain **0 captured stdout lines** from either side, which is
consistent with everything and proves nothing.

---

## VERDICT BLOCK

| # | Check | Verdict |
|---|---|---|
| 0 | Piece N launcher-teleport pave guard | **CONFIRMED** (2/2 our-side throws kept acting the next round; weak n) |
| 1 | Core heal ≡ 5.1 semantics (siege-gated, uncapped) | **CONFIRMED** (0 core heals in confirmed-quiet rounds, 10/10 games; 0 heal-stalls) |
| 2 | K'' budgeted trunk repair | **FAIL-SIGNATURE-SEEN** (alive but near-inert: 22 heals / 131 standing opportunities; not crowding anything) |
| 3 | Pop floor | **CONFIRMED** (0 zero-population windows, 10/10; no harvester runaway) |
| 4 | Piece I rotation latch | **CONFIRMED** (6 rotations / 0 oscillations / 60 Ti across 10 games vs v65's 166/50/1,660 in one) |
| 5 | Piece H endgame switch + dump cap | **NOT-EXERCISED** — and the gate shut itself; see SURPRISE S1 |
| 6 | Piece J counterbattery | **CONFIRMED** (home-band turret builds 0-3/game; no v65-style 7/11 blowout) |
| 7 | Floor-vs-trunk attribution split | **CONFIRMED** (no heal monopoly; builds and melee continue through every siege) |
| 8 | Constants re-extraction | **NOT THIS CORPUS** — still due, now quadruple-due (see below) |
| 9 | **E2b ore-pave ban** | **CONFIRMED** — **0 / 239** relays on ore, against **1,286** trail sites on ore |
| 10 | **E1-capped peacetime ammo floor** | **CONFIRMED** — 0 sub-floor peacetime conversions / 608; measured cap cost = **12 turret-rounds** |
| 11 | **S1 own-building fire guard** | **CONFIRMED** — **0 / 1,925** melee swings on our own buildings (v69-line baseline: 11%) |
| 12 | _v85hs BEFORE-baselines | measured; table below. Headline: **the seat premise is half right and the disease is elsewhere** |
| 13 | Class priority | **SATISFIED TWICE** (Leviathan v25 = bleed family; 0033 v43 = bleed nonfamily) |

### So-what

**All three grafted pieces are production-clean and none of them touches what
lost the seven games.** E2b, E1-capped and S1 fire zero violations across 10
games with live, exercised denominators (1,286 ore trail sites; 608
conversions; 1,925 melee swings), and the E1 cap's measured cost is 12
turret-rounds in 10 games. The 6e base also holds: the 5.1 core-heal gate is
intact (0 quiet-round core heals), the rotation latch is quiet (6 rotations
total), the pop floor never let a game hit zero builders.

**What actually killed us is one mechanism, and v73 does not address it.** In
**all five** 0033 losses, **100% of the damage that killed our core came from
enemy SENTINELS** — and across all 11 of 0033's in-band turrets, the number of
rounds any of them spent inside **any** of our turrets' firing rays is **zero**
(0/64, 0/32, 0/124, 0/64, 0/91, 0/44, 0/86, 0/26, 0/123, 0/99, 0/22). The same
shape is present against Leviathan: their point-blank gunner in corpus A g4
lived 738 uncovered rounds at d²=5 from our core anchor. This is exactly the
bleed-doc "one sentinel on an uncovered bearing" mode, v73 does not ship the L3
ray-coverage fix, and it is **expected-unfixed, not a graft regression**. Say so
plainly to the builder: the ship was clean and the bleed class it was aimed at
is untouched by it.

**And the next worker's premise needs one correction before it is built
against.** The heal-seat plank is half right. Truly-impassable heal-seat
blocking is real but small (median **1** of 8 in corpus A, **0** in corpus B) —
and 884 of the 941 blocked seat-rounds in corpus A are the **enemy's** forward
gunner, not our own buildings. Our own blockers total 57 seat-rounds, of which
**28 are a hand-coded map special case** (`hive_bunker`, `_v84g:2951-2972`,
which deliberately plants a barrier at `(20,4)` — a core heal seat — on the
25x25 `(21,3)` seat). Meanwhile the two worst episodes in the corpus are
**zero-heal sieges with FREE seats**: corpus B g2 and g4, 504 damage each, 28
damage rounds each, **zero core heals**, **zero of our builders on any seat in
any of those 56 rounds**, median 7-8 of 8 seats free, bank ≥1 in 56/56 rounds.
The disease is **convergence**, not seat availability.

---

## Seat-map verification (self-check #1)

Re-verified inside the replays before any attribution, per the standing
incident class.

**Corpus A: we are replay TEAM_A.** Five independent lines agree.
1. TEAM_A wins g2/g4/g5 = 3, matching `scoreA: 3` for `teamAId = 379a5d80… = OpenSverige`.
2. **Ammo-conversion cap.** TEAM_A's conversion amounts never exceed **16** in
   any of the five games (`amt = min(16, …)`, `_v84g:1405`); TEAM_B's reach 20,
   30, 32.
3. **CPU guard.** TEAM_A logs **0** TLE unit-rounds; TEAM_B logs **335**
   (84/14/134/36/67), every one on a builder bot.
4. **Launchers.** TEAM_A builds them (g3 r9 `(6,7)`, g5 r16 `(3,4)`); TEAM_B
   never does.
5. **Population shape.** TEAM_A's live builders sit at 4-7 (`MAX_BUILDERS = 5`
   plus replacements); TEAM_B at 4.

**Corpus B: we are replay TEAM_B.** Same instruments.
1. TEAM_A wins all five, matching `scoreA: 5` for `teamAId = 74ae65ff… = 0033`.
2. TEAM_B's conversions top out at exactly **16** in all five games; TEAM_A's
   reach 20 in four of five.
3. TEAM_B builds launchers (g1 r18, g4 r18, g5 r10); TEAM_A never does.
4. TEAM_B's builder population caps at 5.

---

## Rev-3 checks (the 6e base)

### Check 0 — piece N, launcher-teleport pave guard. CONFIRMED (weak n).

Launchers present in 5 of 10 games, **all of them ours** (corpus A g3 r9, g5
r16; corpus B g1 r18, g4 r18, g5 r10). Neither opponent built a launcher in
either corpus, so the "enemy throws our builder" vector — the ancestral crash's
original trigger — never arose.

Displacement events (`moveBuilderBot` with Manhattan step > 1), per the throw
trap, attributed to a launcher within d²≤2 of the origin tile:

| Game | r | bot | from → to | launcher | acted after? |
|---|---|---|---|---|---|
| A g5 | 46 | theirs #8 | (4,3)→(2,9) | ours #27 | — (theirs) |
| A g5 | 48 | theirs #6 | (4,3)→(2,9) | ours #27 | — (theirs) |
| A g5 | 52 | theirs #8 | (3,5)→(2,9) | ours #27 | — (theirs) |
| **B g1** | **75** | **OURS #11** | (18,17)→(14,14) | ours #52 | **yes, r76; 155 further action-rounds to r230** |
| **B g5** | **19** | **OURS #11** | (11,10)→(8,6) | ours #33 | **yes, r20; 77 further action-rounds to r107** |

Both of our thrown builders acted on the very next round and kept acting for
the rest of their lives. **Zero post-throw idling and zero post-throw death
without a damage cause.**

Two riders the spec could not have known: (a) the pre-N failure mode was never
unit death — `run()` catches everything (`_v84g:1166`), so the bug cost **one
action-round**, and the behavioural test is "did the thrown unit act next
turn"; (b) the "zero diagnostic prints" formulation of this check is
**unmeasurable in production** because the traceback goes to stderr. Both
throws are ours, so n = 2; this is confirmation, not proof of coverage.

### Check 1 — core heal ≡ 5.1 semantics. CONFIRMED, both directions.

`under` reconstructed two-sidedly from the replay against both writers
(`_core`'s own scan `_v84g:1220-1253`, gunner/sentinel d²≤64 and builder d²≤16
from the core anchor, plus the 50-round `SLOT_ATK_RND` latch; and any friendly
unit's copy at `:1693-1711`). A round is **confirmed-quiet** only when quiet
under both bounds.

| | A g1 | A g2 | A g3 | A g4 | A g5 | B g1 | B g2 | B g3 | B g4 | B g5 |
|---|---|---|---|---|---|---|---|---|---|---|
| under-latched rounds | 92% | 86% | 98% | 99% | 70% | 52% | 93% | 96% | 68% | 86% |
| core-heal actions | 149 | 302 | 769 | 632 | 180 | 59 | 0 | 176 | 0 | 95 |
| **in confirmed-quiet rounds** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |
| **before first core damage** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |
| runs ≥10 damage-rounds with no core heal | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 | — | 0 |

**Neither failure direction fires.** The v1 anti-pattern (un-gated core heal
from r0) is absent: not one core heal in a confirmed-quiet round, and not one
before the core first took damage, in any of ten games. The capping artefact is
also absent: no siege episode contains a ≥10-round stretch of core damage
without a heal *while builders were seated*.

The raw "27-31% of builder turns" number **does** reproduce (29.5 / 30.5 / 32.1
/ 12.7 / 26.7% in corpus A) and must not be misread as the v1 signature — in
this corpus the siege latch is on for 86-99% of the game, so a 30% heal share
is 5.1 semantics working under continuous shelling, not a peacetime leak. The
discriminator is the quiet-round count, and it is zero.

*(The two zero-heal games, B g2 and B g4, are NOT a check-1 failure — the
builders were never adjacent to the core. See check 12a.)*

### Check 2 — K'' budgeted trunk repair. FAIL-SIGNATURE-SEEN (near-inert).

| | A g1 | A g2 | A g3 | A g4 | A g5 | B g1 | B g2 | B g3 | B g4 | B g5 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trunk-repair heals | 4 | 0 | 6 | 0 | 0 | 0 | 0 | 11 | 0 | 1 | **22** |
| standing opportunities (unit-rounds beside a damaged own relay) | 10 | 0 | 9 | 33 | 0 | 0 | 24 | 41 | 5 | 9 | **131** |
| rounds with bank ≥ `MEDIC_TI_FLOOR` (20) | 57% | 56% | 82% | 22% | 80% | — | — | — | — | — | |

The arm is **not dead** — v1's depth gate measured exactly zero firings, this
measures 22 — but it converts only **17% of standing opportunities**. Two
mechanisms, both visible in the numbers:

1. **The Core branch pre-empts it.** `_v84g:1935-1940` runs `_heal_core` first
   whenever `under` is latched and returns on success; `under` was latched
   86-99% of the corpus-A rounds. A builder seated beside a damaged core never
   reaches the trunk arm at all.
2. **The bank gate binds.** `MEDIC_TI_FLOOR = 20` against a bank whose median
   is 10-41 and which sits below 20 for 78% of corpus-A g4.

The budget also binds where the arm does fire, exactly as designed: allowance =
`(30 + SLOT_HEAL_BUDGET)//5` ≥ 6, and the top spenders are **6** (unit #12, A
g3), **6** and **5** (units #4 and #6, B g3).

**No opportunity cost.** 22 trunk heals against 310 builds and 1,925 melee
swings over ten games — 0.9% of our acting turns. The K'' arm cannot be what
is costing tempo; the honest read is that it is buying almost nothing either.

### Check 3 — pop floor. CONFIRMED.

**Zero zero-population windows in 10/10 games.** Live-builder minimum after r20:
4/5/5/5/5 (corpus A) and 5/3/5/4/1 (corpus B); means 3.5-6.2. The konly-era
~r235-250 zero windows do not recur.

Not expressing as harvester-spam: live harvesters peak at 3/4/5/3/7 and
4/2/3/3/4 and end at the peak or one below in every game — no runaway, no
collapse-to-zero either.

### Check 4 — piece I rotation latch. CONFIRMED.

Gunner/sentinel re-facings counted as `placeEntity` re-emissions on an existing
id with a changed `direction` (per the rotation trap — re-emissions deduped
before any build count anywhere in this read).

| | ours | A→B→A reversals | Ti burned |
|---|---|---|---|
| **v73, 10 games** | **6** (A g4: #54 E→NE r138, NE→E r147; B g1: #81 S→W r155, #159 SW→N r231; B g5: #92 N→W r192, #108 W→N r192) | **0** | **60** |
| v65, nordkap g3 alone (bug baseline) | 166 | 50 | 1,660 |
| opponents, same 10 games | 17 | 0 | — |

The two same-game pairs (A g4 #54 nine rounds apart, B g5 two different gunner
ids in one round) are not oscillations on a single facing — `ROTATE_COOLDOWN_RNDS
= 8` holds in both. The latch is intact under losing pressure (four of the six
are from the 0-5 sweep).

### Check 5 — piece H endgame switch + dump cap. NOT-EXERCISED.

One r1000 game exists: **corpus A g4** (28x20, `titanium_collected`, we won
640-0 delivered). The dump **never fired**, and not because of the cap.

From r950 to r1000 our **only** live turret was a gunner at `(16,10)`, which is
**d² = 82** from our core anchor `(7,9)`. `_core_turret_mix` (`_v84g:2546`)
scans the *Core's own* r²=36 vision, so it returned `(0, 0)`, `endgame_dumped`
stayed `False`, and piece H's core half was skipped every round from r960.

The ten conversions at r960/964/968/972/976/980/984/988/992/996 (amounts
6/8/6/7/9/6/6/8/6/8) are the **ordinary 16-per-turn drip**, converting each
passive tick against the under-siege floor of 12 at a bank of 11-12. Builder
half: **0 harvesters built at r ≥ 960** (three alive, none with adjacent free
ore). End state: our stored Ti **18** vs theirs **42** — we would have lost
tiebreak #3, and the game resolved at tiebreak #1 anyway.

**Dump cap: NOT-EXERCISED** (the bank never approached it; the binding term was
`ti − 2 × harvester_cost`). **Every r1000 game in the project's corpora still
resolves at tiebreak step 1** — this game takes the tally to 19/19.

See SURPRISE S1: the gate that shut is a latent no-op, not a one-off.

### Check 6 — piece J counterbattery. CONFIRMED (tame shape).

Our gunner/sentinel builds, split by distance-squared from our own core anchor
(home band = d² ≤ 64; launchers excluded — they are not counterbattery):

| | A g1 | A g2 | A g3 | A g4 | A g5 | B g1 | B g2 | B g3 | B g4 | B g5 |
|---|---|---|---|---|---|---|---|---|---|---|
| home-band builds | 3 | 0 | 3 | 2 | 0 | 0 | 1 | 1 | 0 | 2 |
| forward builds | 0 | 3 | 2 | 1 | 1 | 3 | 0 | 0 | 2 | 1 |

Distribution 0-3 per game against v65 production's **1/7/11/4/0** and the
pre-J baseline of exactly-1. The pathological tail is gone; the arm is live
(non-zero in 6 of 10 games). The r69-class core kill the positive signature
calls for does not appear here — neither opponent is a thin-house battery team.

### Check 7 — floor-vs-trunk attribution split. CONFIRMED clean.

| Game | core heals | trunk heals | other heals | builds | melee | spawns | delivered (us/them) |
|---|---|---|---|---|---|---|---|
| A g1 | 149 | 4 | 7 | 33 | 33 | 7 | 380 / 810 |
| A g2 | 302 | 0 | 0 | 29 | 163 | 5 | 540 / 1,350 |
| A g3 | 769 | 6 | 10 | 34 | 760 | 7 | 2,200 / 6,610 |
| A g4 | 632 | 0 | 14 | 25 | 91 | 5 | 640 / 0 |
| A g5 | 180 | 0 | 0 | 57 | 86 | 6 | 940 / 290 |
| B g1 | 59 | 0 | 0 | 35 | 330 | 5 | 560 / 1,380 |
| B g2 | 0 | 0 | 4 | 27 | 120 | 5 | 400 / 890 |
| B g3 | 176 | 11 | 0 | 16 | 93 | 5 | 130 / 840 |
| B g4 | 0 | 0 | 0 | 30 | 92 | 5 | 340 / 300 |
| B g5 | 95 | 1 | 0 | 24 | 157 | 5 | 670 / 1,440 |

No game reproduces the 972-heal starvation monopoly. The heaviest heal game is
A g3 (769 core heals over 389 rounds = 32.1% of builder-turns) and it still
took **34 builds and 760 melee swings** in the same window; the longest game,
A g4, spends 12.7% of builder-turns on heals. Floor and trunk are cleanly
separable and the trunk arm is too small to hide behind the floor (check 2).

### Check 8 — constants re-extraction. NOT THIS CORPUS.

Neither Leviathan nor 0033 is a deterministic-book team we hold rows for.
Still due, and now **quadruple**-due: our-version change (v73), the family
churn wave, the M1 throw-destination unfreeze, and now 0033's v42→v43 bump
(see the opponent section).

---

## Rev-4 checks (the shipped graft)

### Check 9 — E2b ore-pave ban. CONFIRMED.

| | our relays placed | **on an ORE tile** | our trail sites on ore | their relays | their relays on ore |
|---|---|---|---|---|---|
| Corpus A (5 games) | 139 | **0** | **1,077** | 50 | 0 |
| Corpus B (5 games) | 100 | **0** | **209** | 126 | **1** |
| **Total** | **239** | **0 (0.00%)** | **1,286** | 176 | 1 |

"Trail sites on ore" is the honest denominator for this piece: a cardinal move
by one of our builders **off** an ore tile is exactly the `pave_prev` site
piece F would pave with no terrain test (`_v84g:3885-3892`). 1,286 such steps,
zero conveyors laid on ore. On the specific maps, the E2b gate had 62 / 81 /
917 / 104 / 79 opportunities in corpus A g2-g4 and corpus B g1/g4 alone.

**The metric is live in this corpus**, and provably so: 0033 laid a conveyor on
ore in corpus B g1 at `(13,6)` r128, and *both* opponents habitually bury ore
under **barriers** — Leviathan 4 tiles in corpus A g3 (`(12,10)` r8, `(11,8)`
r10, `(12,12)` r154, `(11,6)` r240), 0033 4 tiles in corpus B (`(15,14)` r94,
`(15,12)` r95, `(14,13)` r96, `(11,7)` r34). Eight harvester sites permanently
denied by the opposition; zero by us.

*Scope, unchanged from the v69 read:* this tests the observable, not the code
path. The undecoded-map linker BFS (`_v84g:3582-3595`, red-flagged in the file
itself) still has no ore clause and remains untested — no game here forced it.

### Check 10 — E1-capped peacetime ammo floor. CONFIRMED, with a priced cost.

**Part 1 — sub-floor peacetime conversions: 0.**

Floor reconstructed per conversion as `max(12 if weapons else 52,
min(harvester_cost, 23) + 23)` in peacetime (`_v84g:1397-1402`), with
`harvester_cost = floor((1 + 0.05·n)·20)` replayed from our own harvester
builds and `weapons` proxied by a monotone count of our turrets ever built
(the same conservative proxy the v69 read used; it can only *over*state
`weapons`, which lowers the floor and makes the test stricter). A conversion
counts as a violation only if it fires in a **confirmed-quiet** round (quiet
under both `under` bounds), before r960, with a pre-round bank more than one
passive tick below `floor + 4`.

| | conversions | in confirmed-quiet rounds | **violations** |
|---|---|---|---|
| Corpus A | 429 | 9 | **0** |
| Corpus B | 179 | 11 | **0** |
| **Total** | **608** | **20** | **0** |

Same qualification as the v69 read, sharper here: the siege latch is on for
52-99% of rounds, so peacetime is rare and the floor is **rarely load-bearing**
— 20 conversion-eligible quiet rounds in 10 games. The zero is clean but thin.

**Part 2 — starvation under the cap. The cap is nearly exonerated; the
starvation is real and is a bank problem.**

Turret-rounds where one of our live gunners/sentinels had an enemy entity on
its facing ray inside its range, and the team's ammo was below that turret's
shot cost:

| | turret-rounds with an on-ray target | **ammo-starved** | of those, in **peacetime** | of those, bank in the **E1-blockable band 16-45** |
|---|---|---|---|---|
| Corpus A | 247 | 88 (36%) | 7 | **0** |
| Corpus B | 251 | 148 (59%) | 34 | **12** |
| **Total** | **498** | **236 (47%)** | **41** | **12** |

Against the v69-era baseline of **0 / 1,190** this looks alarming, and the
headline number should not be quoted without the attribution: **195 of the 236
starved turret-rounds are under the siege latch, where E1 changes nothing** —
the floor there is 12, exactly as before the graft. E1 can only bite in
peacetime, and only when the bank sits between the old floor (12) and the new
one (43-46). That band accounts for **12 turret-rounds in ten games**, all in
corpus B g1. Every other starved round had a bank the drip could not have spent
anyway (bank < 16) or ammo policy was not the binding constraint.

**Measured cost of `E1_RESERVE_CAP = 23`: ≤12 turret-rounds / 10 games.** The
ammo problem is that the bank median is 10-41 Ti, not that the floor is 46.

### Check 11 — S1 intercept own-building guard. CONFIRMED.

**Our builder melee swings landing on a tile that holds one of our own
buildings: 0 of 1,925.**

| | our melee swings | **on our own building** |
|---|---|---|
| Corpus A | 1,133 | **0** |
| Corpus B | 792 | **0** |
| v69-line baseline (same defect, teammate lineage) | 4,755 | 535 (**11%**) |

The defect's trigger condition was present and abundant: enemy builders parked
on our conveyors throughout both corpora (see below). Zero swings.

**The turret arm of this question is a decode trap, and it is now closed.**
Corpus A g3 contains 30 `FireTurret` events from **our** gunner #237 at
`(10,11)` onto `(10,10)`, a tile carrying **our own conveyor** — which reads
like an uncovered S1 sibling in `_turret`. Verified at the HP-delta level: in
**25 of 30** it is the **enemy builder bot #8 standing on that tile** that takes
the −7, and in **0 of 30** does our conveyor lose a single HP.

> **A turret shot resolves against the UNIT on the target tile. A builder
> attack resolves against the BUILDING on the target tile.** They are not the
> same rule, and a walker that assumes the melee rule for turrets manufactures a
> 30-event own-fire defect that does not exist.

`_turret`'s picker (`_v84g:3961-3971`) already requires an enemy team on the
tile, so the turret path was never exposed. S1's scope — the `_intercept`
adjacent branch only — is correct and complete.

### Check 12 — _v85hs BEFORE-baselines. Measured. The premise needs one correction.

#### (a) Heal-seat occupancy at every core-damage round

The 8 tiles orthogonally adjacent to our 2x2 core footprint, sampled at the
end of the round preceding each core-damage round. **RAW** = seat carries any
building. **IMPASSABLE** = seat carries a building a builder bot cannot stand
on, or is wall/off-map. Passability validated empirically, not assumed: across
both corpora builder bots were observed standing on a tile holding a
**conveyor 7,075 times** and on a tile holding any other building type **zero
times** (splitters never appeared in either corpus, so splitter passability is
**UNTESTED** here; it is classed with conveyor below on structural grounds).

| | damage rounds | RAW med | RAW p90 | RAW mean | **IMPASS med** | **IMPASS p90** | IMPASS mean | our own builders seated, med | free seats, med |
|---|---|---|---|---|---|---|---|---|---|
| **Corpus A** (Leviathan) | 925 | **4** | 7 | 3.96 | **1** | 1 | 0.95 | 2 | 5 |
| **Corpus B** (0033) | 204 | **3** | 4 | 2.70 | **0** | 1 | 0.30 | 1 | 7 |
| prior habit baseline (raw) | — | 4 | 8 | — | — | — | — | — | — |

**The raw baseline reproduces (median 4, p90 7 vs the recorded 4/8) and the
impassable number is an order of magnitude smaller.** The refinement is
confirmed: most raw occupancy is our own conveyors, which still seat a healer.

Blocker composition, by entity and owner, in blocked-seat-rounds:

| blocker | corpus A | corpus B | note |
|---|---|---|---|
| **enemy gunner** parked on our seat | **868** | 0 | Leviathan's core mechanism |
| enemy barrier | 0 | 16 | 0033 g3 |
| **our own launcher** | 11 | 18 | A g5, B g1 |
| **our own barrier** | 0 | **28** | **B g4 — the `hive_bunker` special case** |
| **total** | 879 | 62 | |

Two things the next worker should carry:

1. **In corpus A the blocker is the OPPONENT, not us** (868 of 879). Leviathan
   plants a gunner on a core-orthogonal tile by r9-12 and rebuilds it as fast
   as we kill it. A self-blocking fix does not touch this; a "clear the seat"
   fix does.
2. **In corpus B every one of our 46 self-blocked seat-rounds is a building we
   chose to put there**, and 28 of them are `_v84g:2951-2972` — the
   `hive_bunker` map special case that *deliberately builds a barrier at
   `(20,4)`* on the 25x25 `(21,3)` seat. `(21,3)`'s footprint is
   `{(21,3),(22,3),(21,4),(22,4)}`, so `(20,4)` **is** one of the eight heal
   seats. Corpus B g4 is that exact map and seat: 504 damage, 28 damage rounds,
   **zero core heals**, core dead at r128.

**And the finding that outranks both.** The two zero-heal sieges are not
blocking failures at all:

| episode | damage | damage rounds | core heals | rounds with ≥1 of our builders on a seat | free seats (med) | bank ≥1 |
|---|---|---|---|---|---|---|
| **B g2 r78-132** | 504 | 28 | **0** | **0 / 28** | **8** | 28/28 |
| **B g4 r56-128** | 504 | 28 | **0** | **0 / 28** | 7 | 28/28 |

Seats free, money available, and no healer ever arrived. **Convergence, not
availability, is the plank to build.**

#### (b) Spawn total vs the soft ceiling

| | A g1 | A g2 | A g3 | A g4 | A g5 | B g1 | B g2 | B g3 | B g4 | B g5 |
|---|---|---|---|---|---|---|---|---|---|---|
| lifetime spawns | 7 | 5 | 7 | 5 | 6 | 5 | 5 | 5 | 5 | 5 |
| ceiling (`spawn_cap 5` + `REPLACEMENT_MAX 8`) | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 |
| with surge (`+SURGE_EXTRA 5`) | 18 | … | … | … | … | … | … | … | … | … |
| max bank after r20 | 64 | 68 | 85 | 42 | 87 | 28 | 20 | 140 | 44 | 51 |

**The ceiling is not binding and there is no idle bank behind it.** Every game
spends 5 of the 500 opening titanium on the first five builders (bank at those
spawns: 470/434/392/354), and the post-opening bank never once reaches
`REPLACE_TI_FLOOR = 250` — peak 20-140, median 10-41. The five post-opening
spawns in the corpus (A g1 r29/r48, A g3 r140/r176, A g5 r70) all fire off the
pop-floor/siege clauses at banks of 63-86, i.e. the clauses that exist
*because* 250 is unmeetable. **Answer: the soft ceiling is NOT the constraint;
titanium is.** Any plank that raises the ceiling buys nothing in this class of
game.

#### (c) Heal/damage ratio per core-siege episode vs the bimodal law

Ratio = (core-heal actions × 4 HP) / core damage taken in the episode.
Law under test: ≥0.94 survives, ≤0.86 dies.

| episode | damage | heals | **ratio** | core outcome | law |
|---|---|---|---|---|---|
| A g1 r19-115 | 1,085 | 149 | **0.55** | dead r115 | ✔ |
| A g2 r30-199 | 1,169 | 302 | **1.03** | survived 482 HP | ✔ |
| A g3 r13-241 | 2,052 | 448 | **0.87** | (→) | ✔ |
| A g3 r262-388 | 1,505 | 251 | **0.67** | dead r388 | ✔ |
| A g4 r15-68 | 364 | 91 | **1.00** | (→) | ✔ |
| A g4 r182-186 | 35 | 0 | 0.00 | (→) | (5 rounds) |
| A g4 r226-228 | 21 | 2 | 0.38 | (→) | (3 rounds) |
| A g4 r294-997 | 1,883 | 522 | **1.11** | survived 496 HP | ✔ |
| A g5 r45-120 | 966 | 155 | **0.64** | **survived 254 HP** | ✘ |
| B g1 r173-235 | 738 | 59 | **0.32** | dead r235 | ✔ |
| B g2 r78-132 | 504 | 0 | **0.00** | dead r132 | ✔ |
| B g3 r19-108 | 1,206 | 176 | **0.58** | dead r108 | ✔ |
| B g4 r56-128 | 504 | 0 | **0.00** | dead r128 | ✔ |
| B g5 r39-47 | 90 | 1 | 0.04 | (→) | (9 rounds) |
| B g5 r73-154 | 792 | 72 | **0.36** | dead r154 | ✔ |

**The law replicates in production: 10 of 11 substantive episodes fall on the
correct side.** The single exception is corpus A g5 (0.64, survived at 254 HP)
— and it survived because we killed *their* core at r134 first, i.e. the siege
was interrupted rather than won. The two 0.00 ratios are the zero-heal sieges
of (a).

### Check 13 — class priority. SATISFIED TWICE.

Corpus A is Leviathan v25 (bleed-list family member); corpus B is 0033 v43
(v72-bleed-nonfamily). Both are exactly the classes the graft's case was
written against. See the opponent sections.

---

## Opponent read 1 — the Leviathan era question

**Answer: v25 matches the FAMILY-RUSH read, not the v26-era zero-rush read —
but it is a GUNNER rush, and it converts slower than the family median.**

Aggression signatures, corpus A, all replay-events:

| | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| first turret planted at d²≤26 of **our** core | **r9** `(10,2)` d²26; **r10** `(7,2)` d²5 | r29 `(7,5)` **d²4** | **r12** `(9,9)` **d²4** | **r12** `(9,9)` **d²4** | r44 `(6,5)` d²5 |
| first core damage to us | r19 | r30 | **r13** | **r15** | r45 |
| gunners built | 6 | 6 | **24** | 10 | 4 |
| **sentinels built** | 0 | 0 | **2 (first r190)** | 0 | 0 |
| **launchers built** | 0 | 0 | 0 | 0 | 0 |
| **builder attacks** | 6 | 0 | **39** | 15 | 0 |
| result | W core r116 | L core r200 | W core r389 | L Ti r1000 | L core r134 |

- **Forward-turret placement is unambiguous rush behaviour.** In three of five
  games a gunner stands on or beside our core footprint by **r9-r12**, and 100%
  of the core damage we took in g1/g2/g4/g5 came from **gunners** (g3: 3,017
  gunner + 540 sentinel).
- **They re-plant the same tile relentlessly.** In g3 a gunner appears at
  `(9,9)` (d²=4) at r12/29/88/179/196 and at `(9,8)` (d²=5) at
  r96/261/276/289/303/318/333/348/366 — a ~13-round rebuild cadence matching how
  fast we kill it. 24 gunners in one game.
- **Contradicts the v26-era decode directly.** That decode reported 0
  sentinels / 0 launchers / 0 builder-attacks in 5 games. v25 has **2
  sentinels, 60 builder-attacks** and the forward-gunner opening. Launchers are
  0 in both, which is the only agreement.
- **Does not match the family's median-64-round kill.** Their two wins land at
  **r116** and **r389**.

**Recommendation:** treat the family classification as VALID for v25 in
mechanism (point-blank forward battery inside r12, sustained, builder-attacks
present) and treat "fastest, median 64" as **not reproduced** against v73. The
inconsistency with the 024d13d6 v26-era decode should be resolved by
re-checking that decode's **seat mapping** before its zero-rush datum is
trusted — this read found the same instruments (conversion cap, TLE profile,
launcher habit) sufficient to settle seat in minutes, and a seat inversion would
produce exactly a "Leviathan does nothing" reading.

## Opponent read 2 — 0033 v43 and the 0-5 sweep

**The bleed-doc mechanism reproduces almost exactly, and it is the whole
match.**

- **Economy first.** Delivered Ti, theirs/ours: 1,380/560 · 890/400 · 840/130 ·
  300/340 · 1,440/670. Ratio ≥2.1x in four of five (6.5x in g3). *g4 breaks the
  rule* — they delivered **less** than us (300 vs 340) and still killed our core
  at r128 off a single r43 sentinel plant.
- **Then the sentinel, at the bleed-doc distance, and it never dies.**

| game | sentinel | tile | **d² to our core anchor** | built | died | **rounds inside ANY of our turret rays** |
|---|---|---|---|---|---|---|
| B g1 | #261 | (14,14) | 32 | r172 | **never** | **0 / 64** |
| B g1 | #302 | (13,18) | 25 | r204 | **never** | **0 / 32** |
| B g2 | #119 | (12,3) | **4** | r69 | **never** | **0 / 64** |
| B g3 | #45 | (6,4) | **4** | r18 | **never** | **0 / 91** |
| B g3 | #108 | (6,3) | 9 | r65 | **never** | **0 / 44** |
| B g4 | #102 | (18,1) | 13 | r43 | **never** | **0 / 86** |
| B g5 | #88 | (11,6) | 25 | r32 | **never** | **0 / 123** |
| B g5 | #270 | (12,6) | 26 | r133 | **never** | **0 / 22** |

  d² = 4-32 against the bleed-doc's "d²=5-25". Eight sentinels, **zero deaths,
  zero rounds under any of our guns.**

- **100% of the core damage in all five losses came from sentinels.** Not one
  point from a gunner or a builder melee swing, in any of the five games.
- **v73 does not ship the L3 ray-coverage fix, so this is EXPECTED-UNFIXED.**
  State it that way to the builder: the 0-5 is not a graft regression, it is
  the named bleed class arriving on schedule against a bot that does not yet
  answer it.
- **The same gap is live against Leviathan.** Corpus A g4's gunner #126 at
  `(8,11)`, d²=5 from our core anchor, lived **738 rounds with 0 rounds inside
  any of our turret rays**; all 25 of their in-band turrets in corpus A g3 spent
  0 covered rounds. Pooled: **45 of the 46 in-band enemy turrets in corpus A and
  11 of 11 in corpus B spent zero rounds under any of our guns** — the single
  exception is corpus A g1 #27, covered 7 rounds of 106. Across both corpora we
  aimed at the thing killing our core in **7 turret-rounds**.

**New behaviour vs the bleed-doc v43 profile** (they bumped v42→v43 right after
losing 4-1 to our v66):
1. **Gunners alongside the sentinel** — 4/1/0/1/4 built, including deep forward
   ones at `(6,10)` r24 and `(5,2)` r156 in g1, and `(3,5)` r107 in g5. The
   profile said sentinel-only.
2. **Barriers as an opening/denial habit** — 6/0/3/2/4 built, **four of them
   laid directly on ore tiles** (g1 `(15,14)` r94, `(15,12)` r95, `(14,13)` r96;
   g5 `(11,7)` r34), permanently denying those harvester sites. This is the
   exact loss E2b protects *us* from, run deliberately as offence.
3. **A pure-tempo win with no economy lead** (g4, above), which the "economy to
   2:1 first" profile does not predict.
4. **Zero TLEs**, unlike Leviathan.

---

## SURPRISES

**S1 (own side, high value) — piece H's gate is core-vision-scoped and shuts
itself exactly when our own opening succeeds.** `_core_turret_mix`
(`_v84g:2546-2560`) counts only turrets inside the **Core's** r²=36 vision. Our
opening habitually plants a **forward** sentinel/gunner — **13 of our 25
gunner/sentinel builds across the two corpora are forward, at d² 80-481 from
our own core anchor**. In corpus A g4 — the only r1000 game, i.e.
the only game H exists for — our last surviving turret was that forward gunner
at d²=82, the gate read `(0, 0)`, and the endgame switch never fired. The
in-file comment already flags this ("a forward siege gun out of Core sight reads
zero — conservative in the right direction"), but the conservatism is total: in
the one production r1000 game the arm was a no-op. Cheap candidate fix: count
turrets via the same store the builders write, or widen the scan; the arithmetic
of the dump cap is untouched either way.

**S2 (decode law) — turret fire and builder melee resolve against different
things.** A `FireTurret` at a tile carrying both a building and a bot damages
the **bot**; a `BuilderAttack` at the same tile damages the **building**.
Verified at HP-delta level over 30 events (25 enemy-bot hits, 0 own-building
hits). Any parser that assumes one rule for both will manufacture own-fire
defects or miss the real S1 class. Worth adding to `tools/replay_schema.md`.

**S3 (opponent) — Leviathan forfeits a third of its turns to CPU timeouts and
we cannot punish it.** 335 opponent unit-rounds with `BotOutput.tled` across the
5 games (84 / 14 / 134 / 36 / 67), **every one on a builder bot**, against 0 on
our side. In g1 that is 84 timed-out builder turns in a 116-round game — and
they still won it by core kill. Their turret line does not depend on their
builders' turns; ours does.

**S4 (both opponents) — ore burial is a live denial play we neither run nor
defend.** 8 harvester sites permanently denied across the two corpora by
enemy barriers/conveyors laid on ore (Leviathan 4, 0033 4). Same mechanism E2b
was grafted to stop us doing to ourselves. There is no code path in `_v84g` that
notices an ore tile has been buried, and none that does it to them.

**S5 (own side) — two of the five 0-5 losses are zero-heal sieges with free
seats and a live bank.** Corpus B g2 (r78-132) and g4 (r56-128): 504 damage
each, 28 damage rounds each, **0 core heals**, **0 rounds with any of our
builders on a core seat**, median 7-8 of 8 seats free, bank ≥1 in all 56 rounds.
Not a heal-policy failure, not a seat-blocking failure, not a money failure —
the healers never came home. This is the single largest unexplained gap in the
corpus and it is where the next plank should point.

**S6 (own side, small) — a map special case builds an impassable barrier on a
core heal seat.** `hive_bunker` (`_v84g:2951-2972`) plants a barrier at
`(20,4)` on the 25x25 `(21,3)` seat, which is one of the eight core-orthogonal
tiles. Corpus B g4 is that map and seat, and it is one of the two zero-heal
sieges. Whether the bunker's value outweighs a permanently lost seat is now a
question with a production data point attached, not a hypothesis.

---

## SELF-CHECKS

- **Seat map.** Verified independently inside the replays for both matches,
  five instruments each; see the seat-map section. Corpus A = TEAM_A, corpus B
  = TEAM_B, both matching their meta `scoreA`.
- **Delivery identity.** `core_deliv × 10 == titaniumCollected`: **20 / 20
  team-sides, 0 mismatches** (10 games × 2 sides). This is the schema doc's
  end-to-end geometry check and it passes everywhere.
- **Core-damage ledger identity.** Per game, `500 + Σ(all UpdateHp deltas on
  our core id) == final core HP`: exact in 10/10 (deaths land at −2/−4, the
  killing blow's overshoot). Event-level attribution of enemy damage
  (enemy `FireTurret` landing on our footprint at 7/18 per gunner/sentinel shot,
  enemy `BuilderAttack` on our footprint at 2) reproduces **100.0% of actual
  core damage in 10 of 10 games** — corpus A: gunners 1,085 / 1,169 / 3,017 +
  540 sentinel / 2,303 / 966; corpus B: **sentinels 738 / 504 / 1,206 / 504 /
  882, gunners and melee zero**. Per-source splits are therefore event-level
  attributions, not round-level apportionment.
- **Heal identity.** Core-heal actions × 4 HP vs the positive HP deltas on our
  core: exact where no overheal clamp applies (A g5 720 = 720, B g1 236 = 236,
  B g3 704 = 704) and short by the clamp elsewhere (A g1 596 vs 583, A g4 2,528
  vs 2,299) — the expected direction and the expected size.
- **Walker vs `tools/replay_census.py`.** End-of-game per-type entity counts on
  our side cross-checked against the census TSV for all 5 corpus-B games
  (conveyors 20/15/7/20/7 and harvesters 4/2/2/3/4): **exact on all 10
  comparisons**. Winner, win condition, round count and map dimensions match on
  all 10 games.
- **Rotation dedupe.** `placeEntity` re-emissions on an existing id are
  excluded from every build count in this document and counted as rotations only
  when `direction` changed (check 4).
- **Throw attribution.** Displacements detected as `moveBuilderBot` with
  Manhattan step > 1 and attributed to a launcher within **d² ≤ 2 including
  diagonals** of the origin tile — 5/5 displacements attributed.
- **Passability.** Not assumed: measured as 7,075 observed builder-bot-on-
  conveyor tile-rounds and 0 for every other building type. Splitters never
  appeared in either corpus, so their classification is **UNCERTAIN** (grouped
  with conveyor).
- **`under` reconstruction** is a two-sided bound using end-of-round positions,
  the same convention and the same ±1-round approximation as the v69 read.
  **UNCERTAIN at ±1 round.** Every peacetime claim requires quiet under *both*
  bounds.
- **Pre-conversion bank** is the end-of-previous-round `UpdatePlayers` value
  (that message is emitted once per turn, after the conversion), so the E1 test
  carries the same ±10 Ti proxy error as the v69 read and absorbs it with the
  one-passive-tick margin. **UNCERTAIN at the ±10 Ti level.**
- **Ammo starvation** uses end-of-previous-round ammo and an idealised firing
  ray (range + collinear facing, ignoring gunner line-of-sight obstruction and
  action cooldown). It therefore **over**counts opportunities for gunners; the
  attribution split (peacetime vs siege, bank band) is the load-bearing number
  and is unaffected.
- Scratch parsers: `walk.py`, `pass1.py` … `pass7.py`, `endgame.py` in the
  session scratchpad. **Read-only throughout: no bots edited, no arena runs, no
  downloads, no tape or HANDOVER writes.**

## Open questions

- **Why did no builder come home in corpus B g2 and g4?** 56 damage rounds,
  free seats, live bank, zero seated healers. Needs a per-builder trace of
  where they were and what role they held — the single highest-value follow-up
  in this corpus, and it is a different plank from the seat-blocking one.
- **Ray coverage (L3).** 7 covered turret-rounds out of ~1,500 in-band enemy
  turret-rounds across both corpora. This is the measured size of the prize; it
  is also the loss mode of both opponents. Builder's call whether it becomes the
  next piece.
- **Is `hive_bunker`'s barrier worth a heal seat?** One production game says no;
  one game is one game.
- **Does piece H ever fire in production?** Zero firings in the only r1000 game
  because of the core-vision gate (S1). Twice-unverified is now three times.
- **K'' at 17% of opportunities** — is the bank gate (`MEDIC_TI_FLOOR = 20`) or
  the core-branch pre-emption the binding one? Cheap offline A/B; the arm
  currently buys ~nothing and costs ~nothing.
- **Re-verify 024d13d6's seat mapping** before the Leviathan v26 zero-rush datum
  is used again.
