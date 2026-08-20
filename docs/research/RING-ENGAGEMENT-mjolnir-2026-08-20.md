# RING ENGAGEMENT — does Mjolnir's ring-claim explain our per-map split against it?

**Research arm, s51, 2026-08-20T04:42Z.** Direct Magnus ask; deliverable feeds the builder's
ANTI-RING build.
**Fixture:** 900 LOCAL replays, `scratchpad/s51_vs_holder/rep/` — 15 maps × 30 seeds × 2 seats,
our head `bots/_v525flip` vs `bots/_x3r0v165mjolnirB` (x3r0's "Mjolnir restore-B w31", imported
2026-08-20T03:59Z). Results tape `scratchpad/s51_vs_holder/head_vs_v165.tsv`, md5
`728a9473ccb94b58adc42e0fd6159bf8`, 900 rows, produced by the builder's screen. **No platform
matches, no downloads.** Instrument: `scratchpad/s51_ring/ringtape.py`; per-game output
`scratchpad/s51_ring/ring_games.tsv`.

**Subjects on every number below: OUR-BOT-vs-ONE-OPPONENT, LOCAL harness, `_v525flip` vs
`_x3r0v165mjolnirB` only, 900 games, 60 per map (30 seeds × 2 seats).** Nothing here is a
ladder read and nothing generalises to other opponents.

---

## 1. Headline

1. **YES, v165 carries the ring arm — and MORE of it than v162.** `RING_ON = True` in
   `bots/_x3r0v165mjolnirB/doctrine.py:6205`; all 30 `RING_*` constants are **byte-identical to
   v162** after line-ending normalisation, and `ring.py` has GROWN 641 → 1,049 lines with two new
   waves: **ARM 4 BELT EVICT** (`BELT_EVICT_ON`, wave 30 — evicts our buildings off *conveyor-chain*
   tiles, not just sockets) and **WAVE 31 PLANK A, the gate split** (`_ring_door_shut` /
   `_ring_evict_gate_ok` — the peck de-gates from the harvester shell when their door is shut).
   The ring is not a legacy flag on this build; it is the part x3r0 is actively developing.
2. **The claim fires in 900 of 900 games — but the first two claims are NOT the ring arm.**
   Median onset **round 2** (851 games at r2, 45 at r3, 4 at r6). That is `OPEN_ON`'s **prefill**
   (`opening.py`, deadline r3), which the doctrine itself calls "two ring claims". The RING arm's
   own floor is `RING_FLOOR_MIN_RND = 6`, and **the earliest third claim in all 900 games is
   exactly r6** — zero games before it. So:
   * **claim ≥ 3 sockets is a clean engine-side marker that the RING arm itself acted.**
   * **It fired in 653 of 900 games (72.6%)** — 174 by r20 (`RING_FLOOR_RND`), 479 after r20
     (the trigger), **247 never**.
3. **NO — ring engagement does not explain the sweep/crater split.** At **matched early
   engagement** the map gap is essentially undiminished:

   | matched stratum | sweep maps | crater maps | gap |
   |---|---|---|---|
   | claim@r20 == 2 (the prefill floor, both sides mean exactly 2.000) | 149/171 = **87.1%** | 43/201 = **21.4%** | **65.7pp ± 8.0** |
   | claim@r40 ≤ 2 | 150/168 = **89.3%** | 42/192 = **21.9%** | **67.4pp ± 8.0** |
   | mean claim over r40–100 ≤ 2 | 144/159 = **90.6%** | 40/150 = **26.7%** | **63.9pp ± 8.9** |

   (sweep = ragnarok/royale/nordkap/frostgate; crater = icefloe/auroraveil/yulerune/glacierkeep.
   Intervals are 95% with **DEFF = 1.130**, measured on this fixture's own seed-pair clustering —
   ICC 0.130 over 450 (map, seed) pairs of 2 games. The correction is applied because these are
   **exclusion** claims: the gap's CI excludes zero, so widening makes them harder, not easier.)
4. **And NO crude geometry covariate explains it either.** Across the 15 maps: r(win%, core d²)
   = +0.31, BFS core-to-core path +0.23, height +0.26, width +0.21, wall% +0.09, ore count +0.10,
   walls near their core −0.04, free apron −0.09. **n = 15 — none of these is significant.** The
   decisive counter-case is arithmetic, not statistical: **royale, frostgate and yulerune are all
   20×20 with core d² = 196**, and we take them at **92%, 62% and 18%**. Map size, core separation
   and socket count cannot produce that.
   ⇒ **The honest verdict is not "geometry beats engagement". It is: the split is MAP-BOUND and
   RING-INDEPENDENT — it survives matching on engagement, and it is not carried by any geometry
   scalar we can measure. Something else map-specific (route structure / ore siting / where the
   opening lands) owns it.**

---

## 2. The instrument and its controls

`scratchpad/s51_ring/ringtape.py` walks the turn stream and, at end of each round, codes each of
**Mjolnir's own 8 orthogonal core sockets** (wall-filtered): `Mc` their conveyor/splitter (= a
ring claim), `Mb` their other building, `Md` their body, `Ob`/`Oc` OUR building, `Od` our body,
`.` empty. The socket geometry helper is **imported from** `scratchpad/s51_closure_autopsy/seattape.py`
so the two tools cannot drift. Pecks are `UpdateHp` delta **−2** (builder attack) resolved against
a never-popped id registry.

**Every guard was driven to BOTH verdicts:**

| control | PASS branch | FAIL branch (must exist) |
|---|---|---|
| round-for-round agreement with `seattape.py` on the shared quantity | 5 games (antler, ragnarok, icefloe, royale, yulerune), **0 mismatches of 2,124 rounds** | same crosscheck against a **+3,+3 shifted anchor**: **375 mismatches of 377** |
| socket anchor is the specific tiles, not "near the core" | true anchor mean claim **1.223** | shifted anchor **0.000** |
| seat convention (A/B ⇒ which team is Mjolnir) | replay `winner` field vs the results tape: **900/900 agree** | seat deliberately inverted: **0/100 agree** |
| −2 filter is SELECTING, not passing everything | one replay's full delta alphabet: `−7:450, −2:220, +1..+4:385` | — |
| peck counter has been seen to read zero | **19 of 900** games have zero socket pecks | 825 games read > 0 |

---

## 3. Per-map table

`claim@r` = number of their 8 sockets holding **their own conveyor**, at that round, mean over the
60 games (r150 restricted to games still alive). `trigger fired` = games reaching claim ≥ 3.
`our block share` / `their claim share` = share of socket-rounds over the whole game.
**\* ragnarok has only 6 non-wall sockets; every other map has 8.**

| map | our win (n=60) | med turn | claim@r20 | claim@r40 | claim@r150 (alive) | claim max | trigger fired | our block share | their claim share | pecks/game | size | core d² | BFS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ragnarok * | 60/60 = 100% | 128 | 2.00 | 1.13 | 0.86 (n=28) | 2.00 | **0/60** | 65% | 15% | 14 | 30x30 | 1152 | 46 |
| royale | 55/60 = 92% | 206 | 2.32 | 2.70 | 3.10 (n=52) | 4.35 | 41/60 | 46% | 35% | 49 | 20x20 | 196 | 21 |
| nordkap | 39/60 = 65% | 284 | 2.23 | 2.32 | 2.26 (n=54) | 4.05 | 33/60 | 55% | 31% | 56 | 20x26 | 144 | 11 |
| frostgate | 37/60 = 62% | 174 | 3.27 | 2.82 | 1.58 (n=36) | 3.83 | 47/60 | 58% | 26% | 48 | 20x20 | 196 | 13 |
| drakkarfjord | 33/60 = 55% | 593 | 2.00 | 1.42 | 0.83 (n=60) | 3.52 | 23/60 | 65% | 19% | 88 | 30x30 | 976 | 42 |
| midgard | 30/60 = 50% | 338 | 2.00 | 3.00 | 5.02 (n=55) | 6.22 | **60/60** | 22% | 59% | 60 | 30x30 | 1152 | 46 |
| valkyrie | 27/60 = 45% | 365 | 1.98 | 1.77 | 3.59 (n=58) | 4.82 | 49/60 | 35% | 41% | 49 | 30x30 | 576 | 25 |
| antler | 26/60 = 43% | 257 | 1.98 | 2.88 | 2.71 (n=45) | 3.80 | 46/60 | 42% | 31% | 82 | 14x18 | 64 | 7 |
| archipelago | 25/60 = 42% | 278 | 2.42 | 4.22 | 6.22 (n=59) | 6.53 | 59/60 | 12% | 68% | 46 | 26x26 | 392 | 28 |
| fjordgate | 22/60 = 37% | 234 | 2.40 | 2.42 | 2.94 (n=48) | 3.60 | 39/60 | 29% | 33% | 38 | 10x10 | 32 | 6 |
| drumlin | 20/60 = 33% | 325 | 2.22 | 2.60 | 2.66 (n=58) | 4.05 | 45/60 | 57% | 30% | 75 | 25x25 | 338 | 24 |
| glacierkeep | 16/60 = 27% | 595 | 2.00 | 1.88 | 0.90 (n=60) | 5.32 | 44/60 | **61%** | 28% | 92 | 30x30 | 576 | 23 |
| yulerune | 11/60 = 18% | 214 | 2.50 | 2.52 | 4.75 (n=55) | 6.32 | 56/60 | 32% | 51% | 80 | 20x20 | 196 | 27 |
| auroraveil | 10/60 = 17% | 290 | 2.00 | 1.98 | 3.77 (n=57) | 5.12 | 55/60 | 27% | 41% | 51 | 20x20 | 256 | 19 |
| icefloe | 8/60 = 13% | 288 | 2.15 | 2.62 | 3.96 (n=57) | 5.53 | 56/60 | 26% | 46% | 79 | 20x20 | 452 | 28 |

**`claim@r20` is flat at ≈2 on every map** (r with win% = **+0.08**). The between-map spread only
appears later — r40 −0.21, r80 −0.27, r150 −0.40, claim_max −0.62, tail-50 −0.68 — which is
exactly the window in which the outcome is already being decided.

**The single map that breaks every simple story is glacierkeep:** their ring engagement over
r40–100 is the second-lowest of all 15 maps (1.17 claimed sockets), **our** blocking occupancy is
the **highest** (6.27 of 8), and we win **27%**. Maximum socket denial, minimum enemy ring, still
a losing map.

---

## 4. Engagement vs geometry — the verdict, and what it cannot separate

**Verdict: RING ENGAGEMENT IS NOT THE CARRIER OF THE SPLIT.** Restated as the exclusion it has to
be to survive the DEFF correction: *at matched early engagement, the 95% CI on the sweep−crater
gap is 65.7 ± 8.0pp and excludes zero* — an engagement-only account of the split is **excluded**,
on three independent matching windows (r20, r40, r40–100), with the r40–100 stratum **biased
against us** (crater games in it carry MORE engagement, 1.41 vs 0.93, and still lose by 64pp).

**Engagement is not nothing, though.** Pooled within-map, high (≥3) vs low (≤2) claim@r40 is worth
**−15.1pp** to us across the 10 maps that have both cells — about a fifth of the between-map gap,
and driven by nordkap (−74pp) and drumlin (−22pp), with antler (+15) and valkyrie (+16) going the
other way. And the coarse split is stark: **trigger fired → we win 34.6% ± 3.9 (n=653); never
fired → 78.1% ± 5.5 (n=247)**.

**⚠ THAT 43pp CONTRAST IS NOT A CAUSAL EFFECT, AND THE DIRECTION RUNS THE WRONG WAY.** Three
measured reasons the correlation is confounded, each of which would produce it with zero causal
contribution from the ring:

1. **Their claim is a RESPONSE to our pressure, by their own doctrine and by the tape.** In
   **509 of 650 games (78.3%)** the third claim lands **after** our first building enters
   `RING_NEAR_DSQ` (d² ≤ 16) of their core — median lag **22 rounds**. Around that event their
   claim goes from 2.16 to 2.55 (Δ +0.39; 29.9% of games up, 11.1% down).
2. **Engagement is CENSORED by game length, and we win the short games.** Mean claim_max is 3.40
   in games ending before r150 and 5.06–5.12 past r250. Games we win have median turn 259 and mean
   claim_max 3.57; games we lose 283 and 5.51. **A ring cannot grow in a game that has ended.**
   ragnarok's `0/60 trigger fired` is partly this: median turn 128.
3. **The same censoring runs through our own occupancy.** On icefloe our block share is 66.4% in
   games we win and 19.8% in games we lose. Within every map, `block(win) > block(lose)`. That is
   the signature of *winning causes ring presence*, not the reverse.

**What I therefore cannot separate, stated plainly:** the within-map −15.1pp engagement
association cannot be decomposed into (a) the ring costing us the game and (b) losing the game
letting their ring grow. Only the **between-map** question is settled, and it is settled by
matching, not by adjustment: **whatever makes a crater map a crater map, it is not their ring
engagement, because holding engagement fixed leaves 64–67pp of the gap standing.**

---

## 5. EVICT-AND-REPLACE: the measured dose

Pooled over 900 games (our buildings standing on THEIR sockets):

* **9,588 brick episodes (10.7/game).** 6,440 ended; **3,148 were still standing at game end.**
* **54,490 builder-attack pecks land on our socket entities — 60.5/game, median 55, p90 112,
  max 284.** At 2 Ti per peck that is **121 Ti/game** of Mjolnir's titanium spent on eviction.
* **99.76% of that effort hits BARRIERS**: victims are barrier 54,361 · conveyor 103 · gunner 26.
  Our seal on their ring is a barrier wall and their whole evict arm is aimed at it.
* **Retake latency: median 1 round.** When one of our bricks dies, their conveyor is back on the
  tile the **next** round — exactly what `DOCTRINE.md` claims ("our conveyor goes back on the tile
  the round it dies"), now confirmed engine-side.
* **But retake COVERAGE is only 33.9%**: 2,181 of 6,440 ended episodes were re-occupied by any
  Mjolnir building within 60 rounds. `RING_EVICT_TI_FLOOR`, the funded-retake-only rule and their
  bank are visibly binding.
* **Their own claims are not cheap to keep either:** 5,140 claim episodes (5.7/game), of which
  **1,968 (38.3%) were removed**; median surviving claim lifetime when it does die is 62 rounds.
  Our bots spend **40.6 pecks/game (81 Ti)** attacking their ring.
* **Occupancy at steady state: we hold 3.27 of their ~7.9 sockets (42%) with a blocking building;
  their conveyors hold 2.95 (37%); 17% sit empty.**

---

## 6. Implications for the ANTI-RING build

1. **DO NOT BUY THE COLLAR AGAIN — WE ALREADY OWN THE RING AND IT IS NOT PAYING.** We hold 42% of
   their sockets on average, 61.8% inside the sweep-matched stratum, **61% on glacierkeep where we
   win 27%** and **57% on drumlin where we win 33%**. Across the 15 maps r(win%, our block share)
   = **+0.48 at n=15** — suggestive at best, and with two direct counterexamples. **Additional
   socket denial is the plank with the weakest remaining headroom in this matchup.** Any anti-ring
   spend must be justified against that, not against the intuition that their ring is what beats us.
2. **THE EVICTION IS ALREADY A TAR PIT, AND WE SHOULD PRICE IT AS ONE RATHER THAN DEEPEN IT.**
   They spend **121 Ti/game** pecking, **99.8% of it into barriers** — a 30 HP / 3 Ti-base barrier
   absorbs 15 pecks = **30 Ti of theirs**, a ~10:1 nominal exchange at scale 1.0 and still ~3:1 at
   scale 3.0, and their arm is capped at `RING_EVICT_BODIES = 2` bodies × `RING_EVICT_TRY_RNDS = 20`
   rounds per tile. **We are already winning that exchange 900 games running and it converts to
   46.6% overall.** ⇒ **A cheaper or tougher decoy brick buys more of an exchange we are already
   winning. Do not build it. If anything, the finding argues for spending LESS on the seal and
   moving the titanium to the kill.**
3. **CLEAR-THEN-REBUILD IS DEAD; ONLY CLEAR-AND-STAND WORKS — and DPS+cripple beats collar
   precisely here.** Median retake latency is **1 round**. Any plan whose step 2 is "and then we
   build on the freed tile next turn" loses the race by construction. What the tape does support:
   their retake coverage is only **33.9%**, and their claim episodes die at a 38.3% rate — so the
   socket is *takeable*, just not *reservable*. **A mode that removes the conveyor and leaves a
   BODY on the tile in the same action window is the only shape that beats a 1-round refill;
   a mode that removes it and walks away funds their arm.**
4. **PICK THE MAP, NOT THE PLANK — AND MEASURE THE CRATERS ON SOMETHING THAT IS NOT THE RING.**
   64–67pp of the split survives matching on engagement and is not carried by size, core
   separation, path length, wall density, ore count or socket count. **royale 92% and yulerune 18%
   are the same 20×20 board at the same core d² = 196.** ⇒ The next autopsy should be a
   **route/opening** autopsy on the three craters (icefloe, auroraveil, yulerune) — where our
   opening lands, when our first body reaches their apron, and what kills our raiders — **not more
   ring instrumentation.** The ring question is answered; spending the next leg on it would be
   testing a plank we already ship against a mechanism we have just excluded.

---

## 7. Provenance

* Instrument: `scratchpad/s51_ring/ringtape.py` (modes `--game`, `--batch`, `--crosscheck`,
  `--mutate`). Per-game output: `scratchpad/s51_ring/ring_games.tsv` (900 rows, 0 parse failures).
* Reused, not re-derived: socket geometry from `scratchpad/s51_closure_autopsy/seattape.py`;
  wire parsing from `tools/replay_census.py`; map decode from `tools/map_encode.py`.
* Opponent tree: `bots/_x3r0v165mjolnirB` (`corpus/version_trees.tsv:97`, imported
  2026-08-20T03:48Z). Doctrine text: `bots/_x3r0v162mjolnir/DOCTRINE.md`, "WAVE 22, TRACK 3 —
  PLANK RING".
* No `corpus/*.tsv` was read for a denominator; no platform call was made.
