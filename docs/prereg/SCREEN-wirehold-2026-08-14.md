# ⛔ NOT DRAFTABLE — WIREHOLD (`SIPHON_WIRE_RNDS` 12 → 96): DOSE PROBE REFUTES THE SCREEN BEFORE LOCK

**VERDICT, FIRST, SO IT CANNOT BE SKIMMED PAST: do not create a `WIREHOLD`
shard.** The mechanism this plank exists to remove is real, it is reachable, and
it was observed firing — **and it fires 0.042 times per game, in 3.3% of games
(4 of 120), on the exact fixture proposed.** The arithmetic ceiling of the whole
plank is **1.67pp** pooled under a fair-coin baseline in the games it touches;
the 5,400-game corefill band is **±1.32pp**. ⭐ **And the predicted PRIMARY
SEGMENT is REFUTED by the same probe: zero preemptions on midgard and zero on
ragnarok — the two maps the plank was designed around — while all four
occurrences landed on archipelago, drumlin, fjordgate and frostgate, one of
which (fjordgate) was named as the near-absent short-haul control.**

**STATUS: committed BEFORE any `WIREHOLD` shard row exists — and none is to be
created.** Two-clock: this file's git author time against the first `WIREHOLD`
row, which does not exist and must not. The shard key `WIREHOLD` appears **0
times** in `scratchpad/corefill_work.txt` at draft. Drafted
**2026-08-14T21:23:16Z** (`date -u`, same shell call), repo at `4568b0f9`.
⚠ The registration block in §9 is the design that was **REJECTED**. It is on the
page so the lane can audit the rejection and, if it overrides, lock a real
document — **not** as an authorisation. Nothing here fires.

**PROVENANCE: docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · tools/prereg_check.py · tools/inert_check.py · tools/effective_n.py · tools/overnight.sh · tools/corefill.sh · tools/arena.py · bots/_v223sealrepair/eco.py · bots/_v223sealrepair/doctrine.py · bots/_v223sealrepair/main.py · bots/_v239wirehold/doctrine.py · bots/_v239wirehold/eco.py · bots/_v178salt · docs/coordination.md (grep only: `SIPHON_WIRE_RNDS`, `link_queue`, `wire_tick`, lines 40895-40975) · docs/prereg/SCREEN-seatscan-2026-08-14.md · maps/*.map26**

Drafted by a FRESH opus agent with **no inherited session context** beyond the
item brief. Every number tagged ⭐MEASURED was produced by this agent in this
session from games it ran itself; everything else is quoted from the files
above. **No row of any live shard (SEALFLOOR6, SALTREF2) was read.**

---

## 1. WHAT WAS VERIFIED AGAINST THE TREE, AND WHAT WAS NOT

The brief asked for anchors rather than trust. Ledger:

| claim | verdict | anchor |
|---|---|---|
| Diff is exactly one line | ✅ VERIFIED | `diff -r bots/_v239wirehold bots/_v223sealrepair` → `doctrine.py:904` only, `12` → `96` |
| `SIPHON_WIRE_RNDS` is genuinely READ (not one of the 43 dead constants) | ✅ VERIFIED | sole read site `bots/_v223sealrepair/eco.py:537`; grep over both trees returns the definition (`doctrine.py:904`), its comment (`:898`) and that one read |
| `eco.py:537` is the read site | ✅ VERIFIED | `if self.link_queue and ct.get_current_round() - since < SIPHON_WIRE_RNDS: return` |
| The overwrite at `:541-543` abandons the in-flight chain | ✅ VERIFIED | `path = self._link_path(ct, bp)` / `self.wire_pending.pop(0)` / `if path: self.link_source = bp; self.link_queue = path` — the old list is rebound, not merged |
| `_build_next_link` keeps no record | ✅ VERIFIED | `eco.py:581` pops on build; `link_queue` is referenced at 16 sites (`main.py:61,408`, `eco.py:505-1217`) and **none** copies or archives it before the rebind |
| `wire_pending` is fed only at `eco.py:511`, on the `link_queue`-non-empty branch | ✅ VERIFIED | `_wire_on_build` (`:504-511`); the empty branch plans immediately at `:507` |
| `_wire_tick` runs for every builder every round | ✅ VERIFIED | `main.py:445`, unconditional after the CPU-exhaustion early return |
| `_link_path` walks harvester-end-first (`#66(d)` already ships) | ✅ VERIFIED | flood from core-adjacent goals (`eco.py:392-399`), parent-chain walk (`:448-453`), `_build_next_link` pops `[0]` (`:550`), fallback `path.reverse()` (`:497-501`) |
| Routable chain lengths are long on midgard/ragnarok, short on fjordgate | ✅ VERIFIED **and independently re-measured in-game** | ⭐MEASURED START lengths, 648 chains over 120 games: midgard 2…38, ragnarok 2…21, fjordgate 2…5. Overall **54.2% of chains started are > 6 tiles** |
| "12 rounds buys ~6 tiles" (act/move mutual exclusion) | ⚠ NOT DIRECTLY MEASURED | the rule is in `CLAUDE.md`; I did not time a chain end-to-end. It is **not load-bearing for the verdict** — §3 kills the plank on occurrence, upstream of chain speed |
| `_l4_repair`'s "DEAD HEADS: chains this bot abandoned mid-walk" corroborates *this* defect | ❌ **DOES NOT SUPPORT IT** | `eco.py:645-651` says the heads are chains `_build_next_link` "never returns to **because it pops its queue as it lays it**" — that is the **builder walking away** (`:551` returns False when the head is non-adjacent), a *different* abandonment path from `_wire_tick` preemption. ⭐MEASURED: 648 chains started, 220 completed, **at most 5 of the 428 incomplete ones (1.2%) came from preemption** |
| Missed emissions are queued, not destroyed (`bots/_probe_beltstall`) | ⚠ NOT RE-VERIFIED | taken from the brief; it is the plank's *safety* argument and is moot once the plank is not fired |
| "earlier delivery funds the r22 sentinel bank" | ❌ **COULD NOT VERIFY** | no `r22` bank constant found in `doctrine.py` (the raid/defence gates I can see are `DEFEND_BEAT_MIN_RND=10`, `MEDIC_EARLY_MIN_RND=40`, `HUNT_MIN_RND=120`, `LOKI_COLD_INSERT_RND=150`). ⭐MEASURED: preemptions fire at rounds **19, 52, 54, 56, 112 (median 54)** — *after* any opening bank, so the stated kill channel is not available on this timing even if the effect were large |

## 2. THE INSTRUMENT, AND ITS CONTROLS

Two byte-copies of the **control** tree in scratchpad (never under `bots/`, the
verified one-line diff is untouched), differing only in `doctrine.py:904` and
carrying five stderr counters: `START` (chain planned), `CHAINDONE` (queue
drained by building), `PEND` (a 2nd harvester queued behind an in-flight chain),
`HASACC` (a pending harvester acquired an acceptor and left the queue), and the
branch at `eco.py:539` labelled `PREEMPT` when `link_queue` was non-empty and
`NORMAL` when it was not.

Fixture: the **15-map pool** (`tools/overnight.sh:68`), seeds 90001-90004, both
seat orders, `--tle 10` and `--replay /dev/null` exactly as `overnight.sh:135`
runs the real screen. **120 games per arm**, plus **60 per arm** against
`bots/_v178salt`.

**Controls, per the instruments rule — each guard driven to the other verdict:**
* **The counter is not constant.** `waited=` printed **12** in every control
  preemption and **96** in every treatment preemption. A broken or hardcoded
  probe cannot track the constant it is reading.
* **The rare branch is not the only branch.** `PEND` fired 23 times and `HASACC`
  14 times, so the pending-harvester path was exercised heavily; it is
  specifically the preemption branch that is rare.
* **Both arms produced both verdicts.** `PREEMPT` 5 (control) vs 2 (treatment);
  vs salt, 5 vs 0.
* ⛔ **ONE ANALYSIS WAS DISCARDED AS AN INSTRUMENT ALARM, AND IT IS REPORTED
  RATHER THAN QUIETLY DROPPED.** I first compared the two arms cell-by-cell and
  got **120 of 120 cells differing, including 91 that never `PEND`ed** — which is
  impossible if the constant is the only difference. Determinism control: the
  **same command, same `--seed`, run three times** gave kills at turn 88 / 274 /
  1000; with `--tle 0`, turns 116 / 853 / 301; with `PYTHONHASHSEED=0`, turns
  785 / 164 / 129; and on **shipped trees with no probe at all** (`v223` vs
  `_v178salt`, midgard, seed 12345) turns 124 / 198 / 373 / 152. **`--seed` does
  not reproduce a local game.** This is **already-known repo knowledge, not a
  discovery** — `tools/effective_n.py` records the cause, and it is still live in
  the shipped tree at `bots/_v223sealrepair/main.py:288`
  (`random.Random().randrange(97)` with no argument, `NOISE_ON = True`,
  `doctrine.py:474`). ⇒ **No per-cell attribution is possible on this fixture and
  none is claimed here.** The occurrence rates below are population averages over
  120 independent games and are unaffected.

## 3. ⭐MEASURED — MECHANISM OCCURRENCE, THE NUMBER THE LEG OWED

**Control arm (`SIPHON_WIRE_RNDS = 12`, i.e. the live bot), 120 games:**

| event | count | per game | games with ≥1 | Wilson 95% |
|---|---|---|---|---|
| `START` (chain planned) | 648 | 5.40 | — | — |
| `CHAINDONE` (chain completed) | 220 | 1.83 | — | — |
| `PEND` (precondition present) | 23 | 0.19 | 17 / 120 = **14.2%** | [9.0, 21.5] |
| `HASACC` (pending resolved without the timer) | 14 | 0.12 | — | — |
| `NORMAL` (planned, queue already empty) | 4 | 0.03 | — | — |
| **`PREEMPT` (the branch the constant gates)** | **5** | **0.042** | **4 / 120 = 3.3%** | **[1.3, 8.3]** |

**The precondition is present in 14.2% of games and the timer still almost never
decides anything, because the dominant resolution is `HASACC`: 14 of 23 pending
harvesters acquired an acceptor after 1-9 rounds (usually 1-4) and left the queue
without ever consulting `SIPHON_WIRE_RNDS`.** The builder plants its second
harvester near the belt it is laying, and the belt reaches it.

**Treatment arm (`= 96`), same 120 cells: `PREEMPT` 5 → 2**, both at
`waited=96`. **The entire behavioural footprint of this one-line change is ~3
avoided chain-abandonments per 120 games.**

**Abandoned chain lengths at preemption: 1, 4, 5, 7, 11 tiles (median 5, total
28 across 120 games = 0.23 tiles/game).** Not the 21-43 tile long-haul chains the
plank was reasoned from. At 3 Ti a conveyor that is **~0.7 Ti/game** of avoidable
waste against a game that mines ~1,000 Ti — and it overstates the harm, because
`_link_path` does not treat friendly conveyors as blocked (`eco.py:404-421`) and
`_build_next_link` pops already-occupied tiles (`:554-559`), so a replanned chain
routes *through* and partially completes the abandoned one.

## 4. ⭐MEASURED — THE SEGMENT PREDICTION IS REFUTED, NOT WEAK

| segment | maps | games | games with ≥1 `PREEMPT` |
|---|---|---|---|
| predicted primary (long-haul) | midgard, ragnarok | 16 | **0** |
| observed | archipelago, drumlin, fjordgate, frostgate | 32 | **4 (12.5%)** |
| remainder | the other 9 pool maps | 72 | **0** |

midgard and ragnarok produce the longest chains (up to 38 and 21 tiles) and the
largest pending queues (`qlen` up to 19) — **and every one of their pendings
resolved by `HASACC` at `waited` 1-4.** ⇒ **A screen segmented on the predicted
maps would measure the plank at exactly zero, and a pooled screen would measure
0.042 events/game.** A segment-value ceiling built on {midgard, ragnarok} would
have been built on a false segment.

## 5. ⭐MEASURED — AND THE SIGN IS NOT OBVIOUSLY POSITIVE: A HARM DIRECTION

`SIPHON_WIRE_RNDS` is doing **two jobs**, and its own comment says so
(`doctrine.py:901-903`): *"long enough that a normal chain … finishes first,
**short enough that a wedged queue cannot orphan the new harvester for the rest
of the match**"*. The second job is the escape hatch from a **stalled**
`link_queue` — and the stall is live in the shipped tree: `eco.py:554` still
reads `occupied = ct.get_tile_building_id(tile) is not None` with **no team
check**, the exact defect the side lane certified at
`docs/coordination.md:40920-40953` (s35), where an enemy barrier on a trunk tile
is popped as "already built", the head becomes non-adjacent, and `:551` refuses
it forever. `_wire_tick`'s timeout is then the **only** thing that ever re-plans.

⭐MEASURED against `bots/_v178salt` — the adversary that builds exactly that
position — **60 games per arm**:

| arm | `PREEMPT` events | games with ≥1 | Wilson 95% |
|---|---|---|---|
| `= 12` (live) | **5** | 5 / 60 = **8.3%** | [3.6, 18.1] |
| `= 96` (treatment) | **0** | 0 / 60 = **0.0%** | [0.0, 6.0] |

⇒ **On a belt-cutting opponent the treatment does not delay the escape hatch, it
disables it within the match** — five pending harvesters that were re-routed at
+12 rounds instead wait out the game unwired. The mechanism is twice as common on
that fixture (8.3% vs 3.3%) and the sign there is **negative**. A screen run only
against `_v223sealrepair` cannot see this, and would have been read as if it
generalised.

## 6. WHY NO n RESCUES IT — THE ARITHMETIC, WRITTEN OUT

Occurrence `f = 4/120 = 3.33%` of games. The plank can only change a game it
touches, so:

* absolute ceiling (every touched game flips from a **certain loss** to a
  **certain win**): **3.33pp**
* ceiling under a fair-coin baseline in touched games: **1.67pp**
* realistic value (median 5 conveyor tiles ≈ 15 Ti and ~10 builder-rounds
  recovered, at median round 54, in 3.3% of games): **well under 0.5pp**

Against the local band (DEFF **0.98**, balanced-by-construction, s39 audit — the
platform constants 1.529/1.833 are **not** applied and applying them here would
widen intervals 24-35% for correlation that is not present):

| n | half-width 95% | 80%-power MDE |
|---|---|---|
| 1,000 | ±3.07pp | — |
| 2,700 | ±1.87pp | — |
| **5,400** | **±1.32pp** | **1.86pp** |
| 10,800 | ±0.93pp | 1.31pp |

**80% power at 1.67pp needs 6,887 games; at 0.5pp it needs 76,832.** The
5,400-game screen is powered *only* for the fair-coin ceiling — i.e. only if
**every single avoided 5-tile chain abandonment decides a match.** That is not a
close call.

**DEFF enumeration, performed rather than asserted** (`CLAUDE.md` procedure —
name every cluster, state whether the stratum can hold more than one member):
1. **MATCH cluster** — a local corefill row is one game and there are no
   5-game matches on this surface; the cluster does not exist. **Dies.**
2. **OPPONENT cluster** — one control tree for the whole shard, so every row
   shares it and the stratum cannot contrast members. **Removed by design.**
3. ⇒ applicable local DEFF **0.98** (pair-weighted, ρ = −0.020, 124 shards).
A per-map cut would keep an opponent cluster on the platform; **on this local
fixture there is no second opponent, so no per-map re-enumeration arises.**

## 7. PROGRAMME FIT — AND THE KILL CHANNEL COULD NOT BE MADE

`R1000_IS_DEFEAT: yes`, `KILL_WINDOW_RND: 250`, and **economy is instrumental: it
buys the kill, it never scores.** This plank's direct channel is titanium
delivery timing, which is off-currency. The brief proposed the kill channel is
"earlier delivery funds the r22 sentinel bank and the raid ⇒ shows up as kill
round". ⛔ **I could not make that link and I am saying so plainly rather than
asserting it:** no r22 bank gate exists in `doctrine.py` that I could find, and
⭐MEASURED the preemptions fire at rounds **19, 52, 54, 56, 112 (median 54)** —
after any opening bank and inside/after the raid's own window. **A plank whose
only channel is `titanium_collected` is at best a correctness fix**, and this one
is a correctness fix worth ~0.7 Ti/game.

**Hot-turn rider (direction confirmed, magnitude corrected).** `_wire_tick` runs
per builder per round (`main.py:445`) but **returns on line 531 unless
`wire_pending` is non-empty**, so the `_link_path` BFS at `:539` is a **one-shot
per pending entry**, not a per-round cost — the brief's "issuing FEWER BFS calls"
is right in direction and small in magnitude: at most `SIPHON_WIRE_QUEUE = 3`
deferred BFS calls per builder per game. ⭐ **And the change does NOT delay normal
wiring at all**: when chain #1 finishes, `link_queue` is empty, the `:537` guard
is false regardless of the constant, and chain #2 is planned the same round. The
constant gates **only** the abandonment of an in-flight chain. Rider verdict:
**REDUCES per-turn work, negligibly.** (`get_cpu_time_elapsed()` reads ZERO
locally, so no local timing was taken.)

## 8. CO-ORDINATION — NO RULING SUPERSEDES THIS, AND ONE BINDS ON IT

`grep -n` over `docs/coordination.md` (never read whole) for `SIPHON_WIRE_RNDS`,
`wire_tick` and `chain preempt` returns **zero** rulings — the plank has no prior
decision for or against. `link_queue` returns five hits; four are unrelated and
**one binds**: the **s35 side-lane certification at `:40920-40953`**, the
team-blind `occupied` pop, which is the wedge this constant is the escape hatch
from (§5). It is **not** a ruling against this plank; it is the reason the plank's
sign is not obviously positive.

**Interaction with live and queued work:** this shares the 15-map ground with
**SEALFLOOR6** (barrier-seal floor, local, running) and **SALTREF2** (salt,
remote, running) — declining to create a `WIREHOLD` shard removes a contended
core rather than adding one, so there is no scheduling cost to this verdict.
`QUEUE.md #63` (long-approach arrival) and `#50` (pave the walk-out, premise
already dead at d²≤2) touch the same trunk geometry; **#66 variation (d)
(harvester-end-first + backfill) is confirmed ALREADY SHIPPED** (§1) and needs no
leg either.

## 9. THE REGISTRATION BLOCK THAT WAS **REJECTED**

⚠ **This block records the design the probe killed. It is not an authorisation
and no shard may be created from it.** It is complete so the lane can audit the
rejection against the same obligations a fired leg carries.

**TREATMENT TREE: bots/_v239wirehold (built; diff verified at exactly one line, `doctrine.py:904` 12 → 96) — NOT TO BE FIRED**
**TARGET BAND: N/A — local corefill screen, ZERO live rated exposure; no submit, no activation, no prototype on the ladder, so `tools/target_value.py`'s reachable-band gate does not bind.**
**PINNED: N/A — local screen against a byte-frozen local control (`bots/_v223sealrepair`); the pin/never-pin design rule governs PLATFORM legs only.**
**SURFACE: local**
**CLUSTER UNIT: none — enumeration performed in §6; both clusters die, applicable DEFF = 0.98 (local, pair-weighted, s39 audit)**
**ESTIMATOR: pooled game share = treatment wins / (rows − NOWINNER rows), unweighted, over `WIREHOLD.tsv` rows only. No map weighting, no seat weighting, no pooling with any other shard.**
**DOSE: ⛔ THE GATE THAT CLOSED THIS DOCUMENT — chain-preemptions 1.67 per 100 games in the TREATMENT (`=96`) vs 4.17 per 100 games in the CONTROL (`=12`), n=120 games per arm, 15-map pool, both seat orders, counted at the branch described in §3. Both verdicts produced by the same counter (`waited=` printed 96 and 12 respectively). ⭐ The probe SEPARATES the arms and therefore is not inert — it refutes the leg on MAGNITUDE, not on absence: 0.042 events/game cannot move a bar of ±1.33pp (§6).**
**PLANNED n: 5400 games — NOT AUTHORISED**
**BOUNDARY: 5400 shard rows = 5400 games (LOCAL fixture: 1 game per row; the platform `games = 5 × accepts` identity has no accepts to close on here)**
**CUT-SHORT: below n=1000 this shard would publish descriptive tallies only and take NO comparative look — moot, as no shard is created**
**BAR: 51.33**
**BASE RATE: 50.0**
**BAR SOURCE: the standing corefill band — the house ±1.33pp band at n=5400, same construction as `docs/prereg/SCREEN-seatscan-2026-08-14.md`. With local DEFF 0.98 the computed half-width is `1.96*sqrt(0.25*0.98/5400)` = ±1.32pp, so the house band is marginally conservative and is used unchanged.**
**BASE RATE SOURCE: structural null of a paired local screen — `tools/overnight.sh:135-136` plays every (seed, map) in BOTH seat orders, so under H0 the shard is a byte-identical null and the expected treatment share is exactly 50.0. No historical population is consumed.**
**REFERENCE n: none**
**POOL ERA: post-2026-08-13-rotation — the 15-map local pool at `tools/overnight.sh:68` (antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune). Every number on this page was measured on that pool in this session; no rated-tape era boundary bounds anything here, because no number here comes from the rated tape.**
**SPANS-POOL-CHANGE: no — all 240 probe games were run 2026-08-14T21:0x-21:2xZ, inside one pool era.**
**MECHANISM METRIC READS: doctrine.py:904**
**TREATMENT DIFF TOUCHES: doctrine.py**
**TREATMENT DIFF REFS: --no-index bots/_v223sealrepair bots/_v239wirehold**
**INTERSECTION: YES — doctrine.py is in both sets, the same shape a doctrine-constant plank takes in SCREEN-seatscan-2026-08-14.md.**

`SIPHON_WIRE_RNDS` at `doctrine.py:904` is the constant whose VALUE **is** the
treated quantity, and the preemption count is a direct function of it; the guard
that reads it is `eco.py:537` and the branch it gates is `eco.py:539-543`.
⚠ **THE OB13 PASS IS NARROWER THAN IT LOOKS AND IS DECLARED RATHER THAN BANKED:**
the OBSERVABLE half of the metric lives in a file the diff does not touch, and a
file-level check keyed only on the observable would read INERT. It is **not**
inert — §3 measured the guard firing 5 times in the control and 2 in the
treatment. ⛔ **THE LIVE OBJECTION TO THIS LEG WAS NEVER INERTNESS. IT IS
MAGNITUDE — which Obligation 13 does not test, and which killed this document
anyway (§6).**
⚠ **NOTE ON THE REFS, because the default is wrong for an arm that already
exists:** with no refs the checker intersects against `git diff HEAD`, i.e. the
repo's *uncommitted working tree* — which on this run returned another lane's
in-flight `tools/nav_lock_census.py` and produced a spurious FAIL. Both trees
here are tracked and clean, so the only meaningful diff is tree-to-tree and is
named explicitly above.
**GATE RESOLUTION: the screen at n=5400 discriminates a true pooled effect ≥ 1.86pp at 80% power (§6), against an arithmetic ceiling of 1.67pp and a realistic value under 0.5pp. ⇒ THE SCREEN IS POWERED FOR NOTHING THIS PLANK CAN PRODUCE. UNRESOLVED is not merely the modal outcome, it is the CERTAIN one, and an UNRESOLVED gate defaults to the RESTRICTION, never the permission — the constant stays at 12 and the arm is not promoted.**
**PRE-STATE: the predicted-change set is NOT already in the target state — `bots/_v223sealrepair` ships `SIPHON_WIRE_RNDS = 12` (`doctrine.py:904`, grep) and `bots/_v239wirehold` ships 96, so the contrast exists. ⛔ PARTIAL PRE-SATISFACTION, DECLARED: the null the brief set out to fix — `QUEUE.md` #66 variation (d), harvester-end-first + backfill — IS ALREADY THE SHIPPED BEHAVIOUR (§1), so that half of the item required no arm at all.**
**PRIMARY SEGMENT: {archipelago, drumlin, fjordgate, frostgate} — 4 of 15 pool maps (26.7%), the ⭐MEASURED set on which any preemption at all was observed (4 of 32 games, 12.5%). ⛔ THIS IS NOT THE SEGMENT THE PLANK WAS DESIGNED FOR: the brief's long-haul primary {midgard, ragnarok} measured 0 of 16 games and is REFUTED (§4).**
**EXPECTED DIRECTION: POSITIVE on-segment and EXACTLY ZERO off-segment against `bots/_v223sealrepair`; ⛔ NEGATIVE against belt-cutting opponents of the `_v178salt` class, where the treatment removes the wedge escape entirely (5 → 0 preemptions in 60 games, §5). A single pooled sign is therefore NOT predicted, and that alone disqualifies the design.**
**SEGMENT VALUE CEILING: 26.7% x 6.25pp on-segment = 1.67pp pooled**
**CELL VERSION CHURN: N/A — local screen, no opponent cells, nothing to churn.**

## FALSIFIER

**The falsifier fired BEFORE the leg, which is the whole point of a dose gate.**
It was pre-committed in this form: *the plank is drafted only if the branch at
`eco.py:539` with a non-empty `link_queue` fires often enough that the screen's
±1.32pp band can see its ceiling — concretely, ≥ 1 occurrence per ~15 games on
the proposed fixture, concentrated on the declared long-haul segment.* ⭐MEASURED:
**1 occurrence per 24 games, and zero on the declared segment.** Both halves
fail. **The leg is not drafted.**

**What would reopen it, stated so the road is bounded and not sealed:**
1. A plank aimed at the **dominant** abandonment cause rather than this one —
   ⭐MEASURED 428 of 648 chains never completed and at most 5 (1.2%) were
   preemptions; the rest are the builder walking off a non-adjacent head
   (`eco.py:551`). **That is a ~100x larger target sitting in the same function.**
2. The **team-blind `occupied` pop at `eco.py:554`** — the s35 certification's
   one-line fix (copy the guard from `:516-517`), which is what actually orphans
   chains against real opponents, and which this plank would make *worse* by
   extending the wedge timeout eightfold.
Neither is this diff, and neither is authorised here.

---

⛔ **A final note on what this document is NOT.** `tools/prereg_check.py`'s own
DOSE clause reads *"a premise-refuted probe writes no prereg at all."* This page
is that probe's report, filed at the prereg path it was commissioned under, with
the rejected registration preserved for audit. **Every machine-checkable
obligation is declared and every recomputed quantity closes — and a green
checker run on this file certifies the FORM of a design that the file itself
rejects on the EVIDENCE. Do not read the token as the verdict. The verdict is at
the top.**
