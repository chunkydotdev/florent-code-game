# KCM first-win decode + C1 validation — match `c821193d`, 2026-08-07

**Version tags (rule 2):** us = **OpenSverige v68 chokewall** (`379a5d80`), them =
**Kings College Munich v1** (`dfa9be96`) — the *same* KCM version as the
classification corpus, so this is a same-era natural experiment.
Match **`c821193d-88a5-4a4a-bdee-c749a9a45b0e`**, ladder, completed
2026-08-07T20:19:36Z, **3-2 to us** (Elo ±4.69; 1545.35→1550.04 us,
1577.77→1573.08 them). Our first-ever ladder win vs KCM; prior record 1-9 in
games today. Research arm, session 14. 5 games decoded from
`replay_archive/`, no downloads, no bots touched.

**Seat: we are Team A in all five games** (verified per game by the KCM
signature — launcher on a core-adjacent tile at r1, destroyed r6, `8/8/8` ammo
ladder, zero splitters — all on Team B in 5/5).

## Decode method

Scratch walker built on `tools/replay_census.py`'s wire helpers
(`fields`/`scalars`/`read_pos`/`KIND_FIELDS`), written under the session
scratchpad, not in the repo. **`placeEntity` deduped by entity id** per
`docs/tooling.md`: 277 re-emissions across the 5 games, **all 277 carried a
changed `direction`, and all 277 were on gunners** — i.e. re-emission == a
`rotate()` call, exactly as the gotcha says, and sentinels never re-emit (they
cannot rotate; `rotate()` is gunner-only). Naive counting would have read
game 5 as "223 US gunners"; the true figure is **4 gunners + 219 rotations**.

Three independent validations of the parse:

| Check | Result |
| --- | --- |
| End-of-game counts / first-build rounds vs `tools/replay_census.py` | exact, 5/5 games |
| Ammo identity `10·sentinel_shots + 4·gunner_shots + final_ammo == total_converted` | **exact on all 10 team-sides**, zero slack |
| Core damage vs shot count (`sentinel 18 dmg`) | g1 39 shots × 18 = 702 = KCM core's total damage; g3 33 × 18 = 594. Exact |

The ammo identity is the strong one: it independently pins the fire count, the
turret-type attribution and the conversion stream simultaneously.

---

## VERDICT

### The predictor is **REFUTED** — it fails in both directions in this match

"≥3 KCM turrets simultaneously alive at d²≤36 of our core ⇒ we lose" was 9/9
(plus 1/1 the other way) in the classification corpus. Here it goes **3/5**,
with a counterexample on each side:

- **Game 1 (WIN):** KCM held **3 turrets at d²≤36 of our core from r19 to the
  end of the game — 78 rounds** — and we won anyway, by core kill at r96.
- **Game 4 (LOSS):** KCM **never** got 3 simultaneously inside d²≤36 (max 2,
  and only for r64-r136), and we lost by core destruction at r658.

Widening the radius does not save it: at d²≤49 and d²≤64 games 1 and 4 give
exactly the same counts. Lowering the threshold to ≥2 is worse (it would
predict losses in games 1 and 3, both wins). **Radius-and-count is the wrong
shape of rule.**

### The refinement that does separate 5/5: **ray coverage, not radius**

A gunner/sentinel fires along **one compass ray** from its facing. A gunner can
`rotate()` (10 Ti, 1 cooldown) so any on-ray tile inside r²=13 is reachable; a
**sentinel cannot rotate at all**, so it only ever covers its build-time ray out
to r²=32. Classify every KCM turret inside d²≤36 of our core by whether *any*
live friendly turret had it on a reachable firing ray during its lifetime:

| | n | killed by our turret fire | took zero turret shots |
| --- | --- | --- | --- |
| **COVERED** (on-ray + in range, facing-aware) | **8** | **8** | 0 |
| **UNCOVERED** | **15** | **0** | **15** |

**8/8 and 15/15, perfect separation, no exceptions.** Of the 15 uncovered, 6
were eventually ground down by builder-attack squads (13 attacks × 2 dmg kills a
25 HP gunner — v68 does this reliably) and **9 survived to the end of the
game**. Every game-losing turret is in the uncovered column: game 4's KCM
sentinel #1819 @(9,5) (uncovered from r559, fired the killing shot at r658) and
game 5's two gunners on tile **(7,5)**, d²=1 from our core footprint, which
between them put **175 of the 219 shots** that killed us — and were never once
shot at, in 345 rounds of being one tile from our core.

### C1 implication — one paragraph

**C1's mechanism is real and is 8/8 when it applies, but "home ring at radius R"
is the wrong specification and "re-aiming" is not available to sentinels.** Game 2
is C1 working exactly as designed: our home sentinel #15 at (9,8), one tile off
our core footprint, facing S, two-shot KCM's single inserted gunner at r10; they
never established again in 1000 rounds, our core took **zero damage all game**,
and we won 15920-50 on titanium. But game 5 is C1 *already running and still
losing*: our home gunner #142 @(6,9) rotated **171 times** and killed 5 of the 13
insertions — every one of them a covered tile — while the 8 uncovered ones,
including both (7,5) gunners, went untouched and killed us. So C1 must be
specified as **ray coverage of the tiles adjacent to our own core**, with each
turret's *facing* chosen at build time, not as a radius. Two hard consequences
for the build: (1) **sentinels cannot be re-aimed** — a mis-faced home sentinel
is dead weight until a builder `destroy()`s it (free) and pays 30 Ti × scale to
rebuild, so a fixed multi-ray ring beats one swivelling sentinel; (2) **the
rotate-thrash we ship today is the single largest leak in the losses** — 219
rotations in game 5 is **~2190 Ti at the documented 10 Ti/rotate, out of 2920 Ti
collected all game (75% of income)** — the 219 is measured from the replay, the
Ti figure is that count times the rules-doc cost. For comparison, eight
fixed-facing sentinels from a fresh scale is 30 × (1.0+1.2+…+2.4) ≈ **408 Ti**
(estimate from the cost-scaling rules, not measured). Spend the ring, not the
rotations.

---

## Per-game table

| | Map | Cores (us / KCM) | Core sep d² | Result | Rounds | Max simul KCM turrets at d²≤36 | Rounds held | Predictor says | Actual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **g1** | 18×18 | (2,14) / (14,2) | 288 | **WIN** core_destroyed | 97 | **3** | r19→r96 (**78 rd**) | LOSS | **WIN — refuted** |
| **g2** | 20×26 | (9,6) / (9,18) | 144 | **WIN** titanium 15920-50 | 1000 | 1 | r7→r9 (3 rd) | WIN | WIN ✓ |
| **g3** | 25×25 | (2,20) / (21,3) | 650 | **WIN** core_destroyed | 114 | 2 | r44→r61 (18 rd) | WIN | WIN ✓ |
| **g4** | 24×24 | (4,4) / (18,18) | 392 | **LOSS** core_destroyed | 659 | **2** | r64→r136 (73 rd) | WIN | **LOSS — refuted** |
| **g5** | 26×26 | (5,5) / (19,19) | 392 | **LOSS** core_destroyed | 458 | **5** | ≥3 from r367 (91 rd) | LOSS | LOSS ✓ |

Volume table (all counts deduped by entity id; shots are `FireTurret` events):

| | our shots (onto their core) | KCM shots (onto our core) | our builder attacks / heals | KCM builder attacks / heals | Ti collected us-KCM | our turrets built | KCM turrets built | our rotations | KCM rotations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| g1 | 43 (39) | 160 (148) | 0 / 251 | 0 / 48 | 450-410 | 2 | 5 | 0 | 0 |
| g2 | 65 (24) | 241 (**0**) | 171 / 145 | 14 / 27 | **15920-50** | 12 | 21 | 0 | 1 |
| g3 | 33 (**33**) | 53 (17) | 29 / 39 | 31 / 21 | 260-250 | 2 | 4 | 0 | 1 |
| g4 | 74 (50) | 245 (134) | 160 / 472 | 227 / 96 | 9520-8850 | 7 | 10 | 3 | 13 |
| g5 | 92 (13) | 278 (**219**) | 143 / 323 | 109 / 99 | 2920-**5020** | 7 | 23 | **219** | 40 |

Core HP ledgers (from `updateHp`):

| | our core: dmg / healed / min HP | their core: dmg / healed / min HP |
| --- | --- | --- |
| g1 | 1036 / 954 / **409** (survived) | 702 / 192 / dead r96 |
| g2 | **0 / 0 / 500** | 245 / 80 / 306 |
| g3 | 119 / 119 / 493 | 594 / 84 / dead r113 |
| g4 | 1961 / 1453 / dead r658 | 702 / 356 / **46** (healed back to 154) |
| g5 | 1690 / 1187 / dead r457 | 157 / 157 / **500** (fully healed) |

---

## Q1 — the predictor, per game

Counts are simultaneous-alive KCM gunners/sentinels/launchers whose tile is at
d²≤36 from the nearest tile of our core's 2×2 footprint.

- **g1 — 3, held 78 rounds, and we WON.** Gunners #24 @(5,12) d²=8 (r10),
  #40 @(1,13) d²=2 (r18), #44 @(0,14) d²=4 (r19). **None of the three ever
  died** — all alive at r96 when their core fell. They put 148 shots into our
  core (1036 dmg); our heal line put back 954 and the core bottomed at 409/500.
  This is a clean refutation: full establishment, sustained for 78 rounds, and
  the game still went to us.
- **g2 — 1, held 3 rounds, WIN.** Gunner #13 @(9,9) d²=4, built r7, dead r10.
  Nothing else ever entered d²≤36 in 1000 rounds (at d²≤64: 4 turrets, max 2
  simultaneous).
- **g3 — 2, held r44-r61, WIN.** Gunners #73 @(5,18) d²=8 (r42→r62) and
  #76 @(6,20) d²=9 (r44→r85). Never 3.
- **g4 — 2, held r64-r136, LOSS.** Sentinel #110 @(9,9) d²=32 (r45→r231),
  gunner #159 @(2,5) d²=4 (r64→r137), sentinel #885 @(9,4) d²=16 (r326→r335),
  sentinel #1819 @(9,5) d²=16 (r559→end). Only ever 2 at once. The second
  counterexample: never established by the rule, and we lost by core kill.
- **g5 — 5, ≥3 from r367 onward (91 rounds), LOSS.** 13 near-core turrets over
  the game; the rule fires correctly here.

**Radius refinements tested and rejected:** d²≤25, d²≤49 and d²≤64 give
*identical* max-simultaneous counts to d²≤36 in games 1 and 4, so no radius
change rescues the rule. Threshold ≥2 at d²≤36 would predict LOSS in games 1
and 3 (both wins) — strictly worse. The rule as written now stands at 13/15
across the classification corpus plus this match, with documented failures in
both directions; **treat it as a weak correlate, not a gate.**

---

## Q2 — the win mechanism: what actually stopped them

Short answer: **only 1 of our 3 wins was C1's mechanism.** The other two were
won by *our* turret, not by stopping theirs.

**g2 — this IS C1, textbook.** Their one insertion, gunner #13 @(9,9), landed
r7 at d²=4 from our core. Our **home** sentinel #15 @(9,8) — d²=1 from the core
footprint, built r7, facing **S**, i.e. the ray straight through (9,9) — hit it
twice (2 × 18 = 36 on a 25 HP gunner) with 2 builder attacks alongside; dead at
**r10, three rounds after landing**. They never re-established inside d²≤36 for
the remaining 990 rounds. Our core finished at **500/500, zero damage taken all
game**, and the tiebreak was 15920-50. Kill came from a **HOME** turret, one tile
from the core.

**g1 — not C1. A forward sentinel won a damage race we nearly lost.** Their
establishment was *never* stopped (all 3 gunners alive at the end, 0 shots and
0 builder attacks aimed at any of them). We won because sentinel **#37 @(9,3)**,
built r16, **facing E**, sitting at d²=25 from their core on a clean E ray onto
footprint tile (14,3), fired **39 shots, all 39 onto that same tile** = 702
damage = exactly their core's whole damage ledger. It survived 81 rounds — and
the margin was razor-thin:

- KCM's counter-gunner #48 @(12,3) went up r21 (lag 5 after our sentinel), on
  the **W ray at d²=9**, and fired **6 consecutive shots r22-r27** — 42 damage
  on a 40 HP sentinel, i.e. exactly lethal.
- Our heal line healed tile (9,3) on **r23-r33** (11 heals, +44 HP). The
  sentinel bottomed at **18/40 on r27**. Two more gunner shots kill it.
- On **r26 KCM's titanium hit 0** and their ammo fell to 17→1. From r27 they
  lived on the 10 Ti/4 rounds passive drip (ammo 0-3 for the rest of the game)
  and **#48 never fired again in 70 rounds**.

So g1 turned on their bankruptcy at r26 plus 11 heals, not on any denial of
ours. **Do not bank this as a repeatable mechanism.**

**g3 — not C1 either; their counter-gunner reflex simply never fired.** Our
sentinel **#58 @(17,8)**, built r28, **facing NE**, at d²=32 (exact max sentinel
range) on a clean NE ray onto footprint tile (21,4): 33 shots, all 33 onto that
tile, 594 damage, core dead r113. It took **zero damage in 86 rounds**. KCM's
nearest turret was gunner #51 @(16,10), built r25 — offset (+1,−2) from our
sentinel, which **is not on any compass ray**, so it could not have hit it even
after rotating. They banked 120 Ti and 48 unspent ammo and never planted a
counter. Their two near-core gunners were killed by **13 builder attacks each**
(r62, r85) — melee, not turrets — and by then our sentinel had been grinding
their core since r29.

**Are the wins C1's mechanism? 1 of 3 (game 2).** Games 1 and 3 are the mirror
image: *we* played KCM's own "max-range sentinel on a clean ray onto a core
footprint tile" finisher, and it worked because in each case no enemy turret was
on a ray to it (g3) or the one that was ran out of ammo (g1).

---

## Q3 — the loss mechanism

Yes, both losses are the classification's pattern, with the counter-gunner
geometry now measurable.

**g4 (24×24, dead r658).** Our forward sentinel #207 @(14,14) r84, facing SE at
d²=32 onto (18,18) — the identical construction that won g1/g3. KCM answered
with gunner #298 @(16,16) at **r139, on the NW ray at d²=8**; our sentinel died
**r147** after 63 rounds and 32 shots (576 dmg — their core hit **46/500** and
they healed it back to 154). Our replacement gunner #361 @(16,21) r163 was
answered by their gunner #399 @(17,22) r180 on the **NW ray at d²=2** and died
r185. After that we had nothing forward, and their uncovered sentinel #1819
@(9,5) (r559) delivered the kill. **Shots: us 74, them 245 (3.3×).**

**g5 (26×26, dead r457).** All three forward attempts died to on-ray gunners
within 6-15 rounds: sentinel #49 @(15,16) r19→r27 (their #47 @(15,17), N ray,
d²=1); gunner #97 @(17,18) r37→r52 (their #117 @(18,17), SW ray, d²=2, plus
**6 builder attacks**); gunner #123 @(16,19) r53→r59 (their #117 again, SW ray,
d²=8). **Shots: us 92, them 278 (3.0×)** and only **13 of our 92** landed on
their core — their core finished **500/500, fully healed**.

**Every single one of our forward turrets that died had a KCM gunner on a
compass ray at d² ∈ {1, 2, 8, 9}.** The two that lived (g1 #37, g3 #58) are the
only ones where that was not true (g3) or where the shooter went broke (g1).

Shot-count context: we under-shoot in **all five** games, wins included (ratios
0.27, 0.27, 0.62, 0.30, 0.33), so raw shot volume does **not** separate wins
from losses in this match — C5 remains a real defect but it is not the
discriminator here. What separates them is **where our shots land**: 91%, 37%,
100%, 68%, 14% of our shots hit their core footprint in g1-g5.

---

## Q4 — map, seat, context

| | Map | Our core | KCM core | Core sep d² | Ore total | Ore within d²≤100 of each core | Walls |
| --- | --- | --- | --- | --- | --- | --- | --- |
| g1 | 18×18 | (2,14) | (14,2) | 288 | 8 | 6 / 6 | 18 |
| g2 | 20×26 | (9,6) | (9,18) | 144 | 22 | 17 / 17 | 74 |
| g3 | 25×25 | (2,20) | (21,3) | 650 | 12 | 4 / 4 | 34 |
| g4 | 24×24 | (4,4) | (18,18) | 392 | 36 | 16 / 16 | 164 |
| g5 | 26×26 | (5,5) | (19,19) | 392 | 32 | 13 / 13 | 70 |

- **Seat: we are Team A in all 5 games** — seat does not vary and therefore
  explains nothing here.
- **Ore is exactly symmetric** around the two cores in all 5 maps (identical
  near-core ore counts). No ore-layout advantage either way.
- **Map size does not separate wins from losses** (wins 18×18 / 20×26 / 25×25;
  losses 24×24 / 26×26 — and 25×25 > 24×24 by area). Core separation does not
  separate them either (win at 650, loss at 392, win at 288).
- **Game length does:** our wins ended at r97, r114 and the r1000 tiebreak; our
  losses ran r659 and r458. Both wins-by-kill were **fast** — a max-range
  sentinel up by r16/r28 and their core dead by r96/r113. Our losses are long
  grinds where their volume advantage compounds.
- **v68's delivery-freeze defect is visible in the losses:** `chain_dir` vs
  `chain` (from `replay_census.py`) is 5/12 vs 10/12 in g4 and **0/2 vs 1/2** in
  g5, against KCM's 10/14 and 11/12. In g5 we collected 2920 to their 5020 while
  laying 56 conveyors to their 36.
- **g5's real economic hole is the rotate-thrash, not the ore:** 219 rotations ≈
  2190 Ti at 10 Ti each, against 2920 Ti collected. Our two home gunners #142
  (171 rotations, 47 shots) and #553 (48 rotations, 18 shots) cost roughly
  **34 Ti of rotation per shot fired** on top of ammo, and each rotation also
  burns that gunner's action for the round.

---

## Q5 — deltas vs the standing classification (flagging changes only)

**Confirmed unchanged (5/5):** launcher on a core-adjacent tile at **r1**,
**destroyed r6**; ammo `8 / 8 / 8` on r0/r1/r2; **zero splitters**; forward
turrets gunner-dominant; the diagonal/max-range placement discipline.

New or contradicted:

1. **The 4th ammo conversion is no longer tied to the first turret.** It is 24
   in 4/5 games but fires at **r6-r14 regardless**: g1 r10 (first turret r10 ✓),
   g2 r6 (first turret r7), **g4 r14 with their first turret not until r45**,
   g5 r14 (first turret r18). The classification's "convert_ammo(24) on the
   round the first turret is built" does not hold.
2. **g3's 4th conversion is 32, not 24**, and it fires at r29 (their first
   turret was r25). First observed deviation from the 24 constant. n=1.
3. **Only ONE opening throw on the two big maps.** g1/g2/g3 show the expected
   3 throws (r2/r3/r4, r2/r4/r5, r2/r4/r5), but **g4 (24×24) and g5 (26×26)
   show exactly one throw, at r2**, and nothing after. The classification
   describes 2-3 throws at r2-r4 as invariant. Worth re-checking: they may now
   abort throws 2-3 on large maps, or the target tile was occupied.
4. **6 barriers per game in g4 and g5** (first at r53 and r229), against the
   classification's "≤4 barriers in any game". g1/g2/g3: zero.
5. **KCM now uses builder attacks, including against turrets.** 227 builder
   attacks in g4, 109 in g5, 31 in g3, 14 in g2 — and **6 of them landed on our
   forward gunner #97 in g5**. The classification states "They never use builder
   attacks for this; it is turret-on-turret." Contradicted.
6. **One proactive home turret, g5.** Their first turret inside d²≤36 of their
   own core went up **r18**, one round *before* our first forward turret (r19).
   Everywhere else home defence is reactive as described (g1 r21 vs our r16;
   g2 r9 vs our r7; g4 r139 vs our r84; g3 none at all). **UNCERTAIN** — a
   1-round lead in a single game is not enough to call it a behaviour change.
7. **Their counter-gunner reflex failed to fire at all in g3** — 86 rounds of a
   forward sentinel shooting their core, 120 Ti and 48 ammo banked, and no
   counter-turret built. New failure mode; the reflex is not unconditional.
8. **Gunner rotations: 0 / 1 / 1 / 13 / 40.** g5's 40 is above the
   classification's observed 0-22 range.
9. **The launcher-throw denial loop from `docs/tooling.md` reproduces, on our
   side.** In g5 our launcher #50 @(4,5) threw KCM raiders to (0,2) **115 times
   between r54 and r418** (attributed by adjacency to the pre-throw tile, per
   the tooling.md rule). It did not save the game — consistent with the ferry
   pre-mortem's PARK verdict.

---

## What this says to do next (for the builder)

1. **Re-spec C1 as ray coverage, not a radius ring.** The metric to build and
   test against is: *for every tile within d²≤9 of our core footprint, is there
   a live friendly turret whose firing ray passes through it, in range?* The
   evidence is 8/8 vs 15/15 on exactly that predicate.
2. **Sentinels cannot be re-aimed** (0 direction changes on any sentinel in 277
   re-emissions; `rotate()` is gunner-only). A home sentinel ring is a
   *fixed-facing* ring — pick facings at build time, and use free `destroy()` +
   rebuild if a facing must change.
3. **Kill the rotate-thrash.** 219 rotations = ~75% of game 5's titanium income
   for 65 shots. A fixed multi-ray ring costs roughly an order of magnitude less
   for the same coverage.
4. **Our own wins came from KCM's own finisher.** Both win-by-kill games used a
   sentinel at max range (d²=25/32) on a clean compass ray onto a core footprint
   tile, up by r16-r28. Its survival is the whole question, and its survival is
   decided by whether *their* counter-gunner can get on a ray to it — so the
   forward-sentinel placement rule should be: **prefer tiles that are off the
   compass rays of the tiles between it and their core**, which is exactly where
   g3's #58 sat and g4's #207 did not.
5. **Cross-check UNCERTAIN:** the ray-coverage law is n=23 turrets over 5 games
   in one match. Re-running the same predicate over the classification's 10
   vs-us games (`b3656fe7`, `9a32a859`) would either promote it to a rule or
   kill it. The classification's own numbers are *consistent* with it — its one
   prior win was a covered insertion (their gunner at (12,5) killed by our
   sentinel at (12,2), "clean N-S alignment, d²=9") — but that has not been
   re-decoded here.

## Addendum (overnight ~23:00): independent replication at n=405 — the n=1 caveat is retired

The builder arm re-cut its 60-game `_v81e6e`-vs-`cad_probe` baseline replays
with a v2 facing-aware ray-coverage counter (this doc's predicate: gunner =
all 8 rays at d²≤13, sentinel = fixed facing ray at d²≤32; script in the
builder session's scratchpad, `predictor2_count.py`). **The law reproduces at
n=405 established turrets: covered median lifetime 8 rounds (in wins) / 11
(losses) vs uncovered 81 / 105.** Independent corpus (probe, not KCM),
independent implementation, same separation.

One boundary the builder's data adds, which item 2 above predicted: the
*aggregate* coverage rate does NOT separate wins from losses vs `cad_probe`
(29% vs 31% — the probe saturates both columns with uncovered turrets).
Coverage is a per-turret lethality law, not a game-outcome scalar; any gate
built on it needs the mechanism triplet (coverage rate up + uncovered-survivor
count down + win rate up), which is how the builder pre-registered the C1
race gate. Rotation-thrash is also confirmed fork-specific: our line's
baseline median is 0 rotations (piece I), vs the 171-219 thrash measured here
in x3r0's line.
