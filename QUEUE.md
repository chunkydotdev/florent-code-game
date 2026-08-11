# BUILD QUEUE — ideas to TEST, in fire order

**Magnus, 2026-08-11 (s31), standing directive:** *"you need to be constantly
putting experiments to test, there should be a queue with ideas to build, the
researcher will be responsible to make sure there are ideas to build."*

**OWNERSHIP.** RESEARCH keeps this stocked — it is their deliverable that this
file is never empty. BUILDER fires from the top and never idles waiting for
analysis. **An empty queue is a research failure, not a builder pause.**

**THE CLOCK.** ~420 rated matches remain in the entire game (~84/day, measured
646->749 in 29.5 h). Rating converges in ~100 matches ⇒ **about four
ship-and-converge cycles left.** A ship converges in the BACKGROUND, so an
unshipped plank is a certain zero and every idle hour on the slot is spent.

**ADMISSION — an item is queueable only with all four:**
1. the CHANGE, named to the constant or branch
2. the MECHANISM METRIC only that change can move
3. the FIXTURE it is measured on, and whether that fixture can resolve it
4. why it is worth a slot **now** (`tools/target_value.py` band if it is a live leg)

---

## FIRING NOW
| # | plank | change | mechanism metric | status |
|---|---|---|---|---|
| 1 | **LOKI-27 ferry-first** | ferry request outranks home exile | INSERT:EXILE ratio | ⭐ **SHIPPED 13:14Z** — v112 LIVE, verified on the `Active bot:` line. Ends v104's 29 h 25 m hold. Rollback: `fcode submission activate 104`. |

## NEXT UP — ready to build
| # | plank | change | mechanism metric | why now |
|---|---|---|---|---|
| ~~2~~ | ~~**Idle-builder defence**~~ | **WITHDRAWN — WE ALREADY SHIP IT.** See below. |
| 2 | **DESTROY ENEMY TURRETS** | not yet specified — **intervention deliberately NOT named** | enemy turrets alive per forward builder-round (term `A`) | **Largest single term on the board: 1.77x, 47.3% of the log hazard gap. Reduces `A` DIRECTLY, does not touch forward-round counts, and therefore escapes the LOKI-25 numerator/denominator trap BY CONSTRUCTION.** |

**⛔ #2 WITHDRAWN — THE CHEAPEST NULL IN THIS REPO IS A LEG THAT TESTS A FEATURE
WE ALREADY SHIP, AND THIS WAS ONE.** Research's idle/active split gave the number
that unblocked it AND the warning that killed it: **bucket B ("active, home") is
92% HEAL** — 65,673 heal-rounds against 1,532 build and 3,980 attack in the 20
rounds before our core dies. **grep of the shipped tree confirms it**:
`eco.py:312 _heal_core`, `eco.py:322 _heal_adjacent`, `eco.py:125 heal_seats`
(tiles that exist ONLY to heal the core), multi-healer convergence at `:16-17`,
and `main.py:160-188 SLOT_UNDER` — an under-attack flag that already retargets
`ammo_target` and `ti_floor`. **The 2.44 "active home" builders are our own
heal line showing up in the data.** Two minutes of grep, one window saved.

**AND THREE MEASURED REASONS IT WOULD NOT HAVE PAID ANYWAY:**
* **Idleness carries NO loss-specific information**: idle share **25.76% in
  losses vs 27.59% in WINS**, flat straight through the core's destruction. What
  differs is WHERE activity sits, not how much there is.
* **Median bank at T-1 is 28 Ti.** At 2 Ti per 2 damage a redirected builder
  cannot do much — a cap independent of headcount.
* The genuinely expensive bucket (forward AND mid-action) is **0.18
  builders/game**, so the kill-budget objection was small — **my "admissible by
  construction" was still wrong, but the number landed in my favour.**

**⭐ TWO ENGINE FACTS ESTABLISHED AS BY-PRODUCTS, both correcting standing belief:**
**a builder bot's action cooldown is NEVER >0 at decision time** (only the value
`1` is ever written, 93.9% of one builder's consecutive actions are exactly 1
round apart) ⇒ **"builders act every other round" is FALSE.** And **99.75% of idle
rounds carry a `BotOutput`** — the engine ran `run()` and it emitted nothing —
with `tled` at **0.00% for us vs 1.52% on the field**, so that zero is real and
not a dead column.

**⛔ AND MY OWN "FORWARD TIMING" ENTRY FROM 20 MINUTES AGO IS ALSO REFUTED, BY THE
ARM THAT PROPOSED IT.** *"We go forward late into a matured turret field"* fails:
enemies build the SAME turrets against us as against the top tier EARLY
(**r0-59 ratio 1.04, r60-179 ratio 1.00**); divergence is entirely late, which is
**DOWNSTREAM of clearing, not upstream of it**. **The field is the same size when
we get there.**

⇒ **What differs from the first minute is DESTRUCTION: cumulatively the enemy
builds 1.19x more turrets against us while we destroy 0.88x as many.** That is
why #2 above is now *destroy enemy turrets* — and it is OFFENSE, so it needs no
defence-admission bar at all.

⚠ **Caveat carried from the source:** deaths-per-build *within* a band is a flow
ratio, not a survival share (a turret built in one band can die in the next).
**The cumulative totals are the clean comparison.**

| ~~3~~ | ~~**Arrive without traversing**~~ | **WITHDRAWN 2026-08-11 — its premise is refuted.** See below. |
| 3 | ⭐⭐ **WE DO NOT CLEAR TURRETS — the field matures because we leave it standing** *(replaces "forward timing", which research tested and refuted — see below)* | not named — **the intervention is deliberately NOT specified**; the target quantity is enemy turrets DESTROYED | **enemy turret deaths per side-game, and standing enemy turret count per forward builder-round (term `A`)** | archive-measurable now; a leg needs the usual fixture | **Term `A` is 1.77x and 47.3% of the log gap — the largest single term on the board.** ⛔ **The "we go forward late" reading is REFUTED: enemies build the SAME turrets against us as against the top tier EARLY (r0-59 ratio 1.04, r60-179 ratio 1.00) and only diverge LATE (1.39x, 1.64x, 2.36x) — which is DOWNSTREAM of clearing, not upstream.** **What differs from the first minute is DESTRUCTION: deaths-per-build within band 24.0% vs 35.4% at r0-59 and 47.4% vs 67.0% at r60-179.** **Cumulative: enemy builds 7.68/game against us vs 6.45 against TOP (1.19x) while we destroy 3.01 vs their 3.42 (0.88x).** ⇒ **This is OFFENSE, not timing — it reduces `A` directly and does not touch forward-round counts, so it escapes the LOKI-25 trap by construction.** |

**⛔ #3 REPLACED. THE ORIGINAL PREMISE ("the traverse is what kills us") IS
REFUTED BY RESEARCH'S OWN ATTRIBUTION CUT (13,771 replays, 0 parse failures,
anchor reproduced: US 2.90 vs 2.92, TOP 0.87 vs 0.84).**

**AND THE "UNEXPLAINED ~2.3x" THAT MOTIVATED THE WHOLE ROAD NEVER EXISTED — it
was an arithmetic error (terms MULTIPLY, they were treated as ADDING), corrected
by its own author.** The gap decomposes exactly:

| term | factor | log-share |
|---|---:|---:|
| **A. enemy turrets EXIST near us** (per fwd builder-round) | **1.77x** | **47.3%** |
| B. share of them IN RANGE of our tile | 1.57x | 37.0% |
| C. damage per turret-in-range-round | 1.05x | 4.3% |
| D. damage absorbed per death | 1.15x | 11.4% |
| **product** | **3.36x** | = the anchor |

**B = 1.57x independently reproduces `FORWARD-HAZARD`'s ray-based 1.53x on a
different instrument.** So *"exposure explains 1.53x, leaving 2.3x unaccounted"*
was never a residual.

**⛔ AND TRANSIT-vs-STATION KILLS THE LAUNCHER-DELIVERY CASE SPECIFICALLY:**
our forward builders die **2-9 rounds AFTER they stop moving** — 40.6% of forward
deaths in 11.5% of forward rounds, at **4x mean hazard**. **MOVING IS BELOW-AVERAGE
HAZARD (0.90x). Parked 30+ rounds is the SAFEST state in the game (0.19x).**
⇒ **Launcher delivery removes the traverse — the LEAST hazardous state, 44.6% of
deaths — and drops the bot straight into the PEAK-hazard window.** Ceiling ~45%
of forward deaths with **no hazard-per-round discount**. The saving is purely
"fewer forward rounds per build", **the same lever LOKI-25 pulled.**

**⭐ THE GENERATIVE FINDING, AND IT IS `A`:** opponent-matched, we see **3.94
enemy turrets alive per forward round vs TOP's 2.19**, and the opponent-matched
gap is **2.96x** — opponent selection is only ~10% of it. The alive-ratio runs
**1.14x at r0-59 -> 2.25x at r500-999**, and **30.5% of our forward rounds sit in
r500-999 against TOP's 16.8%.** **We are forward LATE, into a turret field that
has matured.**

**TWO STORIES KILLED OUTRIGHT, so nobody re-queues them:** *"we fail to disengage
or heal"* is **dead** (moved-after-first-damage 76.74% vs 76.81%; ever-healed
14.34% vs 13.96%). And **we do not crash** — no-damage removals 0.00% US vs 1.02%
TOP. **Our movement-state mix is FAVOURABLE**; standardised to TOP's mix our rate
RISES 2.90 -> 4.11 and the gap WIDENS to 4.74x.

⚠ **Carried caveat, flagged by the agent against itself:** *"moved last round"* is
partly a RESPONSE to danger, so the transit/station boundary is blurred in both
directions. **The bucket shape is robust; the causal reading of it is not.**

## ⭐ UNBLOCKED — BUILD THESE WITHOUT WAITING FOR RESEARCH

**Stocked by research s31 after auditing this file and finding ZERO buildable
items: #1 shipped, #2 blocked on a number I owe, #3 gated on #4, and #4 is a
research cut rather than a plank. Every blocker was mine.** These three depend on
**nothing I am running.**

| # | plank | change | mechanism metric | fixture — can it resolve? | why now |
|---|---|---|---|---|---|
| **5** | ⭐ **CRASH INDUCTION AT SCALE** | **already built** — `bots/_v131loki14`: launcher kidnaps an **enemy** builder (`can_launch` has no team check, no vision guard) and throws it to a legal **map-border** tile, where their own code queries an off-map neighbour, raises, and **the engine permanently destroys that unit for the match** | **enemy builder-bot removals with NO preceding damage event** — read ENGINE-SIDE off the wire via `tools/crash_census.py`. **NOT our own throw count**, which measures what we did rather than what landed | **live unrated. YES** — the dose is already demonstrated at **314 kidnaps** in the LOKI-14 leg, and the outcome is an entity-removal event, not a log line | **Highest ceiling on the board, APPROVED CLASS (Magnus asked the organisers), already built, and never scored on the currency.** Field baseline: **2,451 unexplained unit removals by opponents across 1,855 games, against 0 by us** — most teams do not guard what we patched in `eco.py`. **⛔ Its only prior failure was an INSTRUMENT failure, not a negative: the leg planned to read its arm tag from `print()`, and the platform strips stdout (0 of 30,664 `BotOutput` events). That read-out no longer has to be attempted that way.** |
| **6** | **BEST-FIT SENTINEL PLACEMENT — one repeat** | re-run the placement arm **with the 10 ms TLE enabled**, after cutting its per-turn cost | forward sentinel siting quality **and** `get_cpu_time_elapsed()` per turret turn | local self-play, TLE **on**. **YES at n=4,096** (MDE 3.1pp) | **The dead-list entry invites exactly this**: it won 6/6 with the CPU limit disabled and lost 5/6 with it on, at **n=12**. That is a **CPU-cost regression, not a placement refutation** — the road is open and only this implementation died. Cheap, and it does not consume a knob slot because it changes an algorithm, not a constant. |
| **7** | **ORE-BARRIER CARVE-OUT** | barrier (3 Ti) an ore tile that a forward gun **already covers** | rounds-to-first-enemy-harvester on covered ore tiles; enemy builder-turns spent clearing | live unrated. **PARTIAL** — the metric is readable, but see the caveat | Never measured, and **both primaries explicitly preserved this carve-out** while killing the parent. The price refutation that buried it was computed under the **retired** currency and is void. Clearing a 3 Ti barrier costs them **~30 Ti and ~15 builder-turns** — a tempo weapon nobody priced as one. **⚠ RANKED LAST DELIBERATELY: its channel is the enemy's economy, which is instrumental under `R1000_IS_DEFEAT`. Build it only if 5 and 6 are both in flight.** |

| **8** | ⭐⭐ **SEAT-RELATIVE SCAN ORDER** — *found by READING the tree, not by measuring* | `doctrine.py:26` — `CARDINALS = [NORTH, EAST, SOUTH, WEST]`, a **fixed ABSOLUTE order**, consumed by **20+ first-match-wins scans** across `main.py` and `eco.py` (`:480 :551 :617`, `eco :330 :391 :433 :465 :511 :682 :812 :919 :975 :1029` …). Also `eco.py:640` sweeps `self.ang += 0.65` rad from a **fixed absolute angle**. ⇒ **"toward the enemy" is a different cardinal for each seat, so identical code takes a different branch depending on which side we spawn.** Fix: order the scan by `cardinal_direction_to(enemy_core)` — same code, seat-relative. | **the seat gap on byte-identical arms** — currently **A 53.91% vs B 46.34%, z = 3.54** | **the 4,096-game byte-identical null, WHICH ALREADY EXISTS AND IS POWERED.** Re-run it with seat-relative ordering: **if the gap closes, confirmed.** ⚠ pin `NOISE_ON = False` in the measured copies (see RNG note) | **A measured 7.6pp self-play seat gap, confirmed twice** (research's algebraic `s = 54.126%` off the nine-arm screen; the side lane's `53.91%` off byte-identical arms — two populations, two methods, ~0.2pp apart). **Maps account for ~1.8pp of it (third-party same-8-maps 51.76%, n.s.); the residual is OURS.** If half of every game is played at a self-inflicted disadvantage, closing it is worth **~+1–2pp ≈ +7–14 Elo from a MECHANISM, not a knob.** **⛔ NOT YET ESTABLISHED: I have shown the ORDER IS ABSOLUTE and that a seat gap EXISTS; I have NOT shown any specific site changes the outcome. The null re-run is the test, and it can come out the other way.** *(Ladder cannot settle it: our rated win rate by our seat is +1.80pp ±3.20pp on `ladder_games` — MDE 4.58pp, and detecting 2pp needs ~9,800 games/seat against the 1,885 we have. **The ladder check CANNOT resolve the hypothesis it was proposed to test.**)* |

| **9** | **EXILE-FIRST — the deliberate inverse of what just shipped** | invert LOKI-27: launcher prioritises grabbing an **ENEMY** builder over ferrying our own | INSERT:EXILE ratio (same metric, opposite prediction) | live unrated, **or** the local null at n=4,096 | **The tactics library's strongest cross-league inversion, and we just shipped the other direction.** Sweep 12: **BC2020's Delivery Drone has our Launcher's EXACT verb signature**, and that field **converged on grabbing the enemy's unit and never on ferrying their own forward.** LOKI-27 went the opposite way on our own reasoning. **One of the two is wrong and the pair is a clean A/B on a shipped baseline** — the cheapest possible way to find out, and it costs no new mechanism. |
| **10** | **BLIND THEIR GUN WITH THEIR OWN BODY** | launcher throws a kidnapped **enemy** builder onto the tile their own gunner is aiming through | enemy gunner shots-on-target per game (their turret blanked) | live unrated — **⚠ needs a gunner-line decoder; `tools/loki9_facing.py` exists but computes EXACT-RAY collinearity, a different predicate from `ALIGNED_DEG=45` tolerance. Pick one and say which.** | Sourced (`tactics/blind-their-gun-with-their-own-body.md`, `the-blockade-blanks-your-own-guns.md`). **A gunner's shot is a straight line that does NOT pierce** (unlike a sentinel), so one body in the lane blanks it — **and it costs them a unit AND their turret's output from one throw, 0 ammo.** Ranked below 5 because the decoder question is unsettled. |

**⭐ THE STOCKING RULE — MAGNUS, 2026-08-11 (s31), DIRECT: *"please make sure
there always is new items on the list for the builder to build and test, if the
queue runs empty we go stale, that is not acceptable."***

> **FLOOR: this file must hold ≥ 3 UNBLOCKED items at ALL times.**
> **Unblocked = the builder can start it today without waiting on a research
> number.** An item gated on a running cut is **not** unblocked and must not be
> counted toward the floor.
>
> **Dropping below 3 is a RESEARCH ALARM, not a builder pause.** Mechanised:
> **`.venv/bin/python tools/queue_check.py`** counts unblocked rows and exits
> non-zero below the floor. **Research runs it at boot, after every item is
> consumed, and at wrap.**
>
> **⚠ THE FAILURE THIS CLOSES IS THE ONE THAT ALREADY HAPPENED TODAY:** this file
> was audited at 15:2xZ with **1 shipped, 2 "next up" and 1 blocked — and ZERO
> buildable**, because #2 was blocked on a number research owed, #3 was gated on
> #4, and #4 was a research cut rather than a plank. **Every blocker was research's
> own.** A queue can read full and be empty.

**CHECKED AND CLOSED, s31 — not a plank, recorded so nobody re-opens it.** `CLAUDE.md`
flags that **`can_fire` returns TRUE at 0 ammo** and that firing then RAISES, which
would permanently destroy our own turret. **We are guarded:** `main.py:116` wraps
`_dispatch` in a blanket `try/except Exception` with a comment naming this exact
hazard. So the unguarded `ct.fire(best)` at `raid.py:382` — which sits *outside* its
local `try` — **costs that turret one turn, not the unit.** Residual cost is a
silently wasted turret turn, and `econ.tsv.ammo_end` (median 24–48) says we rarely
sit at 0. **Not worth a slot.**

## BLOCKED / NEEDS A NUMBER FIRST
| # | plank | blocker |
|---|---|---|
| 4 | ~~forward-death attribution~~ **DONE s31 — AND IT DISSOLVED ITS OWN PREMISE.** ⛔ *"tile exposure explains only 1.53x of a 3.47x gap; ~2.3x is unaccounted"* **WAS A RESEARCH ARITHMETIC ERROR: the terms MULTIPLY, they do not add.** `A` turrets exist 1.77x x `B` in-range 1.57x x `C` damage/turret-round 1.05x x `D` damage absorbed/death 1.15x = **3.36x, the anchor exactly.** There was never a residual. **`B`=1.57x independently reproduces the ray-based 1.53x on a different instrument.** ⇒ **The whole gap is that we take 2.92x the damage per forward builder-round, and `A` alone is 83% of what I called unexplained.** **`A` is our forward TIMING, not their build:** opponent-matched 3.94 vs 2.19 turrets alive, gap 2.96x, and **30.5% of our forward rounds sit in r500-999 against TOP's 16.8%.** `docs/research/FORWARD-DEATH-ATTRIBUTION-2026-08-11.md` |

## DEAD THIS SESSION — do not re-queue without new evidence
* **cap6** (`LOKI_FWD_GUN_CAP` 3->6) — **NO INFORMATION, and it is a knob-turn
  under the bar, so it does not consume a cycle.** ⛔ **REASON CORRECTED
  2026-08-11 (side lane): I first wrote "INERT BY CONSTRUCTION — we build 1.6-1.9
  forward sentinels/game so a cap of 3 never binds." THAT ARGUMENT IS WEAKER THAN
  IT READS AND I OVERSTATED IT TWICE.** (a) Those levels come from **the dose
  check itself**, not an independent source, so it is not a structural argument at
  all — it is the same measurement wearing a different hat. (b) **A MEAN CANNOT
  SHOW THAT A CAP ON SIMULTANEOUS-ALIVE NEVER BINDS** — a tail mechanism produces
  exactly the small mean shift observed. **The deciding number — the fraction of
  games reaching 3 simultaneous forward sentinels — was never computed.** The
  harness's own verdict line said `NO-INFORMATION back to the pool, NOT demoted`
  and I wrote it onto a DEAD list anyway, one hour after building the
  NO-INFORMATION branch to stop exactly that.
* **best-fit sentinel placement** — **CPU-COST REGRESSION**: with the 10 ms limit
  disabled it wins 6/6; with it on it loses 5/6. **n=12, on THIS laptop's timing
  rather than the platform's, and ⛔ THE COUNTS HAVE NO COMMITTED ARTEFACT — they
  exist in a session scrollback only. Do not re-quote them without a committed
  log.** This is the one row where machine load genuinely bites, because it is the
  only measurement that toggles `--tle`. **Worth one repeat before the ROAD is
  closed rather than just this implementation.**
* **gunner-axis / LOKI-25** — died s30 on a resolved mechanism falsifier
  (deaths -24%, presence -23%, ratio flat -2.3%). ROAD open, implementation dead.
* **forward-efficiency 880-game screen** — DROPPED for this horizon. Its protected
  denominator needs 700-900 games/arm and at 440 misses LOKI-25's own magnitude
  (3.21 vs a 3.278 threshold). Also: dwell is 17% of the gap, not 54% — the
  headline was a 120-game sampling artefact.

---

## ⛔ READ BEFORE TRUSTING ANY LOCAL NUMBER IN THIS FILE
**Our bot reseeds an UNSEEDED RNG every game** — and note the blast radius is
NARROWER than I first published: `h2h.sh` and `dose.py` run treatment and control
as **the two sides of ONE `fcode run` process**, so any load is common-mode with
no channel to favour an arm. **The 8x1024 screen, the 4,096 null and the
platform-side ferry-first leg all SURVIVE**; only best-fit's `--tle` toggle is
genuinely load-exposed. My first published cause (wall-clock CPU guard) was WRONG
— `doctrine.py:1072-1075` in our own tree says `get_cpu_time_elapsed()` reads 0
under local `fcode run`. **Exchangeable i.i.d. salt leaves pooled estimates
unbiased; the load story would have meant systematic bias. Opposite worlds.** `bots/_v130loki13/main.py:276`:
`self.spawn_salt = random.Random().randrange(97) if NOISE_ON else 0`, with
`NOISE_ON = True`. **`--seed` never controlled it.** Identical seed/map/bots gave
kill turns 109, 118, 227, 302, 527, 118.

⇒ **"SEED-MATCHED PAIRING" IS AN ILLUSION IN EVERY LOCAL BATTERY WE RUN**, including
s30's 8x1024 screens, the 4,096-game null, and `dose.py`. The noise is unbiased so
POOLED estimates stand; PAIRED designs buy nothing they claim to buy.

**`gate.py` HAS WARNED ABOUT THIS ALL ALONG** — *"paired fixtures do not pair
against a bot that reseeds"* — **and `h2h.sh` and `dose.py` both bypass gate.py,
which the standing rule calls the sole entry to a battery.** The check existed;
the tools that needed it skipped it. **Fix: pin `NOISE_ON = False` in the measured
COPIES, or route every battery through the gate.**
