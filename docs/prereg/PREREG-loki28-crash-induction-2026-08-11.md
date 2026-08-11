# PREREG — LOKI-28 "CRASH INDUCTION AT SCALE"

**Arm:** builder, s31, 2026-08-11. **Committed BEFORE leg creation** (two-clock:
this file's git author time vs the platform `createdAt` of the first match).

**Bot:** `bots/_v131loki14`. **Control / incumbent:** `bots/_v148ferryfirst` = **v112**
(shipped 13:14Z — the control is the CURRENT incumbent, not v104).

---

## TARGET BAND (`tools/target_value.py --band`, run BEFORE this document)

**TARGET BAND: Big O (+110), HTTP 418 (+108), Leviathan (+106), 0033 (+78),
team lazy (+70); gaps +70..+110; win pays +19.18..+20.89; reachable YES.**

Top five of the reachable band at our 1658. Same discipline that s28 failed by
firing a flawless leg at teams 550–860 points below us.

## THE WEAPON — an APPROVED class, already built, never scored

Our launcher picks up an **enemy** builder (`can_launch` has **no team check and
no vision guard**, pickup d²≤2, throw 1≤d²≤26, 0 ammo, position-only mutation)
and throws it to a legal **map-border** tile. That bot's own code then queries an
off-map neighbour, raises, and **the engine permanently destroys that unit for
the rest of the match** (`0x1ac5c` → `Game::destroy_entity`; `SystemExit` and
`KeyboardInterrupt` are the only exemptions). We spend one throw.

**⭐ ENGINE FACTS RE-VERIFIED TODAY AGAINST `fcode 2.3.7`.** The CLI bumped
2.3.6 → 2.3.7 and the engine `.so` hash CHANGED, so every launcher fact was
treated as provisional until checked. **Named symbol set is IDENTICAL between the
two binaries** (2,468 symbols each; the only diffs are Rust hash suffixes and
`GCC_except_table` renumbering — recompile artefacts), and `can_launch`,
`finish_firing_turret`, `distribute_resources`, `scale_percent` and
`destroy_entity` are all present with identical counts. **No engine function was
added, removed or renamed. The guard matrix stands.**

**FIELD-LEVEL PREMISE, MEASURED TODAY, not quoted:** `tools/crash_census.py` on a
random 400-game sample of the archive — **515 crash candidates, 129 of 400 games
carrying at least one** (team A 220 / team B 295), against 6,425+7,098
damage-deaths for scale. **The field crashes constantly and unaided.** We patched
our own instance of this bug in `eco.py`; most teams have not.

## ⛔ WHY THIS HAS NEVER BEEN SCORED — AN INSTRUMENT FAILURE, NOT A NEGATIVE

LOKI-14's leg planned to read its own arm tag out of the live replay.
**`print()` is STRIPPED from platform-downloaded replays — 30,664 `BotOutput`
events, stdout empty in 30,664 of 30,664.** The leg decoded **314 kidnaps** off
the wire, so the mechanism demonstrably fired; **the read-out as written was not
executable and the weapon was never scored on the currency.**

⇒ **THIS LEG READS ARMS AND DOSES FROM ENGINE-SIDE FACTS ONLY** — throw
destinations and entity removals off the wire. **No stdout is consulted for any
quantity in this document.**

## PRECONDITION / ADMISSION — measured per cell BEFORE claiming anything

**The precondition is enemy-builder ARRIVAL within d²≤2 of one of our launchers.**
This is the same class of precondition that killed LOKI-19's panel, where
SmartFridge delivered the premise in **7.6%** of rounds — *less than half the rate
the plank existed to exploit*, and only 1 of 4 admitted cells carried it.

⚠ **I HAVE NOT MEASURED PER-CELL ARRIVAL FOR THESE FIVE TEAMS AND I AM FIRING
ANYWAY, DELIBERATELY, ON THE CLOCK.** ~420 rated matches remain in the game. The
leg's own replays measure arrival directly, so **admission is read OUT of this leg
rather than gating entry to it.** The cost of that choice, stated up front:
**if arrival is near zero in both arms the leg is INADMISSIBLE and I have spent a
window learning that.** That is an acceptable trade at this clock and would not
have been a week ago.

## PRIMARY BAR — the currency, and what it cannot do

**`PRIMARY_CURRENCY: game_share`.** Recorded across the 25 unrated games vs v112's
game share on the same five cells.

⛔ **25 GAMES CANNOT RESOLVE GAME SHARE — MDE ≈ ±20pp — AND THIS LEG IS
REGISTERED AS A DOSE-AND-MECHANISM PROBE, NOT A CURRENCY READ.** A currency
verdict requires pooling windows.

## THE MECHANISM BAR — sized, with a NO-INFORMATION branch, PRE-COMMITTED

Read from the wire via `tools/corpus/replay_throws.py` (throw kind/destination)
and `tools/crash_census.py` (unexplained enemy unit removals):

| quantity | prediction if the weapon works |
|---|---|
| **KIDNAP throws/game** (EXILE of an enemy builder to a border tile) | **RISES vs v112** |
| **enemy crash_candidates/game caused after our throw** | **RISES vs v112** |
| enemy builders alive at r250 | falls or holds |

**BAND, COMPUTED FROM BOTH ARMS' REALIZED COUNTS — never from a stored rate.**
The stored-comparator defect cost LOKI-27 two inverted headline rows today; the
band here is computed at read-out from the two arms actually played, using a
**GAME-CLUSTER BOOTSTRAP**, not Poisson. *(Poisson understated LOKI-27's sd by
4.3× — var/mean was 14.8 — and the honest interval there was ±530%, not ±124%.)*

| outcome | verdict |
|---|---|
| kidnap rate AND crash rate both rise ≥ 2 sd (cluster bootstrap) | **MECHANISM CONFIRMED** |
| either falls ≥ 2 sd | **DEAD** — runs backwards |
| **inside the band** | **NO INFORMATION — back to the POOL, NOT demoted** |
| kidnap opportunities ≈ 0 in both arms | **INADMISSIBLE** — precondition absent |

**⛔ AND A SINGLE-GAME LEVERAGE CHECK IS MANDATORY AT READ-OUT.** LOKI-27's
direction turned out to rest on **one game supplying 38% of its INSERT signal**
and **one match supplying its whole EXILE row** — found by a peer AFTER I had
published the ship justification. **This read-out reports the leave-one-game-out
and leave-one-match-out range before any verdict sentence is typed.**

## PROCEDURE — rated-cost controls

* **ROLLBACK TARGET IS v112, NOT v104.** `MAIN=112` must be passed to
  `unrated_run.sh`, whose default is 104 and is now WRONG. A default that was
  right this morning is a live hazard this afternoon.
* Fire just after an observed pairing; cadence re-derived from recent rows
  (`:12:59 / :32:59 / :52:59`), never hardcoded. **Read `createdAt` from `--json`,
  never the `match list` table column — the display value lags ~2 minutes and
  lands on the wrong side of a submit.**
* Holder restored to v112 and confirmed on the `Active bot:` line, never `$?`.
* **v112 is ~1 rated match old and converging.** Prototype exposure is ~20 s
  inside a 20-minute pairing cycle, so the cost to its convergence is one
  interrupted gap at most — but it is not zero and is recorded here.

## WHAT WOULD MAKE ME DROP THIS PLANK

* Kidnap throws/game flat or down vs v112 → **DEAD**.
* Kidnaps rise but enemy crash rate does not → **DEAD**: we are throwing bodies
  around without inducing the fault, which is the LOKI-25 shape (bought the
  numerator).
* Kidnap opportunities ≈ 0 → **INADMISSIBLE**, not refuted.
* Any uncaught exception in OUR units attributable to the diff → **DEAD**.

---

# AMENDMENT 1 — 2026-08-11 13:2xZ, **BEFORE LEG CREATION**, ADD-ONLY (adds a control)

**Raised by the side lane. The defect is mine and it is a JOIN, not a number.**

## 1a. WHAT MY 2.3.7 CHECK ACTUALLY ESTABLISHED, AND WHAT IT DID NOT

I wrote *"the guard matrix stands."* **What I measured is that the SYMBOL SET is
identical — 2,468 named symbols each, no function added, removed or renamed.
THAT IS THE API SURFACE. IT IS NOT THE FUNCTION BODIES.** The `.so` hash CHANGED,
so something in that binary IS different, and I attributed the delta to Rust hash
suffixes and `GCC_except_table` renumbering — **an inference from symbol NAMES,
not a comparison of CODE.** The conclusion may well be right; **it is not
measured, and I stated it as measured.**

## 1b. ⛔ WHY THAT GAP IS WORST-SHAPED FOR *THIS* LEG SPECIFICALLY

This plank's entire mechanism is: **an uncaught exception from `run()` → the
engine permanently destroys that unit.** That is **the single most likely
behaviour an organiser patches in a point release** — "bots get permanently
killed by their own exceptions" is the most complained-about rule any bot league
has. **A patch to it changes a function BODY and leaves the symbol set
byte-for-byte identical.**

⇒ **THE FAILURE MODE: THE LEG COULD NOT DISTINGUISH "THE TRICK DOESN'T WORK" FROM
"THE TRICK WAS PATCHED", AND WOULD BANK THE SECOND AS THE FIRST.** Under D12 that
retires a road on evidence about the ENGINE rather than about the PLANK — the
worst outcome available to us, and `CLAUDE.md` lists this weapon as open
*precisely because it was never balance-changed*.

## 1c. ⭐ THE ADDED CONTROL — IN-LEG, COSTS NOTHING, PRE-COMMITTED BEFORE THE FIRE

**Measure the OPPONENTS' UNAIDED unexplained unit removals in this leg's own
replays** — crashes we did not cause — and compare against the historical field
rate measured today: **`crash_census.py`, random 400-game sample of the archive,
515 crash candidates, 129 of 400 games carrying at least one.**

| in-leg observation | reading |
|---|---|
| opponents still crash unaided at ~the historical rate | **the engine still destroys units on uncaught exceptions.** A null is then about OUR PLANK and is bankable. |
| opponents' unaided crash rate **collapses to ~zero** | **THE ENGINE WAS PATCHED. The leg is INADMISSIBLE, not a refutation.** No road is retired. |

**This is read off the SAME wire already being decoded** — no extra window, no
extra decode pass, no delay to the fire. Same shape as the placebo arm that made
LOKI-14 readable.

⚠ **Stated limit:** the historical 515/400 pools both teams across the archive and
is not opponent-matched to these five cells, so it bounds the comparison loosely.
**A collapse to ~zero is interpretable; a modest shift is not.** The control is
built to catch a PATCH, which is a step change, not a drift.

## 1d. OFFLINE, NOT A BLOCKER ON THIS LEG

Both binaries are retained. **Diff the `__TEXT` bytes, or disassemble
`can_launch` and the exception path in each and diff those two function bodies.**
If they match modulo relocations, the "non-event" verdict is fully established
and can be stated as measured. **Until then it is established FOR THE SYMBOL
TABLE ONLY, and this document says so wherever it is quoted.**

## 1e. ⭐ THE OFFLINE DIFF WAS RUN BEFORE THE FIRE. NOW MEASURED, NOT INFERRED.

**MY 1a SELF-CRITICISM WAS CORRECT AND SO WAS THE ORIGINAL CONCLUSION — the
method was insufficient, the answer was right. Both halves matter.**

**⛔ FIRST, THE FINDING THAT KILLS THE LAZY VERSION OF MY CLAIM:
`__text` — ALL EXECUTABLE CODE — DIFFERS IN 47,404 OF 572,364 BYTES (8.3%).**
So "the symbol set is identical, therefore the engine is unchanged" was **not a
safe inference**, and had I stopped there I would have fired a leg on it.

**THEN THE FUNCTION-BODY DIFFS, disassembled and compared with only the Rust
symbol-hash suffixes normalised (`17h<16 hex>E` → `17hXE`) — addresses, opcodes
and call targets otherwise raw:**

| function | instructions | result |
|---|---:|---|
| `Controller::can_launch` | 390 | **IDENTICAL** |
| `Game::destroy_entity` | 2,443 | **IDENTICAL** |
| `runner::GameRunner::run` | 3,144 | **IDENTICAL** |
| `runner::run` | 1,643 | **IDENTICAL** |
| `runner::watchdog::Watchdog::arm` | 2,685 | **IDENTICAL** |
| `runner::validate_bot_ast` | 1,119 | **IDENTICAL** |

**`__text` addr/size/offset are identical in both binaries (0x1c40 / 0x8b9cc /
7232) and `can_launch` sits at the same address 0x3704**, so the layout did not
move; the 8.3% is call-offset and embedded-hash churn, not semantics.

⇒ **THE EXCEPTION→DESTROY PATH AND THE LAUNCHER PATH ARE UNCHANGED IN 2.3.7.**
The weapon is not patched. **This is now established on CODE, not on symbol
names.**

**⛔ THE IN-LEG CONTROL IN 1c STAYS ARMED ANYWAY.** It costs nothing, it is read
off a wire already being decoded, and it guards a case this diff does not cover:
**the PLATFORM may run a build we cannot download.** A local binary diff says
what OUR engine does; the opponents' unaided crash rate says what THEIRS does.
**Keeping a control after the risk it was written for is retired is cheap; the
converse is not.**
