# BUILD REPORT — `bots/_v543burst` (THE BANK-BURST PAIR), s53, 2026-08-21

**QUEUE #71's GATE half and QUEUE #80's CONSUMER half, built together in one
flag-gated tree forked from `bots/_v542wave`.** The gate is an EDGE-TRIGGERED
bank crossing at 200 Ti with an eco-saturation qualifier and **no round gate**;
the consumer is the **FORWARD SENTINEL PAIR at d² ≤ 32 of the ENEMY core**,
placed by the incumbent's own siting machinery, promoted above the collar for
the duration of the window, plus the magazine that keeps it from being two
statues.

Wall clock from `date -u` in the same shell call: tree seeded `12:59:51Z`,
plank committed `13:12:02Z` (`9f64c4426`), report written `13:15Z`. Parent
`bots/_v542wave` last touched `11:50:29Z` (`28fde0637`).

**⛔ THIS BUILD MAKES NO VALUE CLAIM.** Nothing here is a screen, a verdict or a
ship recommendation. It is a tree, its self-checks, and an honest statement of
what the mechanism did on the one live cell it was allowed to touch.

---

## ⛔ TOP LINE — FIVE SENTENCES

1. **THE DIFF IS ADD-ONLY: 538 inserted lines, ZERO deleted, ZERO modified,
   across three files** (`doctrine.py` +192, `siege.py` +295, `main.py` +51;
   `eco.py` and `raid.py` byte-identical). Nothing in the parent's behaviour is
   edited — the plank is inserted, never substituted.
2. **The gate arms FROM BELOW** — the game starts at 470 Ti, so a bare level
   test on 200 fires at r0 in 100.0% of games; `v543_armed` starts `False` and
   is set only by an observation of `ti < 200`. ⛔ **BUT DO NOT CITE THE LATCH
   AS LOAD-BEARING: measured over 1,405 real rated game-sides it is worth
   EXACTLY 0.0pp**, because on real series the harvester clause blocks the
   opening endowment first. The latch, `FS_V543_PEAK` and the net-rise term are
   mutually redundant substitutes; all three stay, none of them is the dial.
   **The dial is the threshold: 17.5% of game-sides at 200, 35.5% at 150**
   (§4.7 — and it corrects a claim this build first wrote into its own doctrine
   block).
3. **The consumer is the SECOND sentinel, because the first already jumps the
   collar and the second does not.** `_v518_early_sentinel` is gated on
   `live <= 0`; after that the only route to a pair is rung 4, the *bottom* of
   the ladder, plus a rebuy surcharge on top of the whole remaining collar
   reserve. The burst window replaces the collar reserve — and nothing else —
   for at most two live sentinels (§2.2).
4. **⚠ MECHANISM FIRST. At the shipped setting the gate fired 0 times in both
   instrumented live games — and the tapes say why: neither game contains an
   edge crossing of 200 Ti at all** (§4.3; the instrument is not blind — the
   same runs' positive-control tape emitted 294 lines). **A forced-dose probe
   at a lowered threshold then drove the whole path end to end — gate → PAIR
   purchase → ammo waiver, 0 tracebacks — and exposed a map-coverage defect:
   on midgard the ferry-siege lane never runs at all, so the consumer has no
   site to execute from** (§4.4). Corpus dose at the shipped setting: **~17.5%
   of game-sides, median first fire r178** (§4.7).
5. **Flag-off identity is argued statically and is CLEAN under a self-tested
   audit** (R1/R2/R3, mutation positive control fires 3 violations on a
   deliberately unguarded copy) — **the DYNAMIC half (paired NOISE_OFF identity
   games vs the frozen parent) was NOT run and is owed by the screen lane**
   (§3).

---

## 1. THE GATE (#71's half)

### 1.1 What the evidence deleted, and what it left

| term | shipped in `_v542wave` | in `_v543burst` | why |
|---|---|---|---|
| round gate | `SURGE_MIN_RND = 300` | **none** | #80's precondition: moving it 300→250→200 changes the fire rate by **0.00pp**; 150 buys ≤ +0.16pp. The floor was always the binding term. |
| threshold | `SURGE_TI_FLOOR = 1500` | `FS_V543_BURST_TI = 200` | 1500 fires in **0 of 590** kill-window crossings and is a fossil of an economy we no longer run (ever-≥1500: v80 30.9%, v90 35.6% → v140 1.21%). 200 fires **25.6%**, median first crossing **r67**, **18.5%** before r150. |
| shape | level test | **EDGE, armed from below** | only **10.3%** of games hold 200 for ten consecutive rounds ⇒ a level/sustained test throws the fire rate away. And a bare level test fires at r0 on the 470-Ti opening endowment — the measured defect in `LOKI_SURPLUS_TI = 260` (satisfied in 100.0% of games, trivially, at r0). |
| consumer | `SURGE_ECO_CAP` → eco hands | forward sentinel pair | the surge's kill-hardware half (`SURGE_EXTRA`) has one definition and no reader; it was dropped in the modular refactor. |

⛔ **`SURGE_*` AND `LOKI_SURPLUS_TI` ARE UNTOUCHED**, deliberately, per the build
brief: `doctrine.py:402-405` is left exactly as `_v542wave` ships it so the diff
stays minimal and this plank is separable from that fossil.

### 1.2 THE EXACT OPERATIONALIZATION (the two sentences the brief asked for)

> **A burst fires on the first round where the team bank is at or above 200 Ti
> having been observed strictly below 200 Ti at some earlier round of this
> body's life (the edge), the bank is the MAXIMUM of the last 8 rounds and is
> net non-falling across them (eco spend has saturated while income keeps
> arriving), and `SLOT_HARVESTERS ≥ 2` (income exists at all).**
> **A fire opens a 40-round WINDOW; no second fire is possible while a window
> is open; the latch re-arms only on a subsequent observation of `ti < 200`;
> and at most 3 windows open per body per match.**

Constant-by-constant, all in `bots/_v543burst/doctrine.py`:

| constant | value | role |
|---|---|---|
| `FS_V543_BURST_TI` | 200 | the fire threshold |
| `FS_V543_REARM_TI` | 200 | the arm-from-below threshold (equal ⇒ a pure crossing, no hysteresis) |
| `FS_V543_RISE_RNDS` | 8 | length of the income window (two passive ticks) |
| `FS_V543_RISE_TI` | 0 | required net bank change over that window |
| `FS_V543_PEAK` | True | current bank must be the window's maximum |
| `FS_V543_MIN_HARV` | 2 | `SLOT_HARVESTERS` floor |
| `FS_V543_WINDOW` | 40 | rounds a window stays open |
| `FS_V543_MAX_FIRES` | 3 | windows per body per match |

**Why the window and not the level:** the first purchase drops the bank straight
back under the threshold, so a level test funds exactly one sentinel and then
re-arms. The pair is the load-bearing element in the field evidence, so the
funding authority has to outlive the crossing that created it. 40 rounds is the
study's own pre-burst doubling window and sits inside its 30-round
first-sentinel→core-death constant.

**⚠ `FS_V543_PEAK` WAS ADDED MID-BUILD BECAUSE THE BUILD'S OWN TEST DROVE THE
NET-RISE TERM TO THE WRONG VERDICT.** A trace that spiked eight rounds ago and
has been draining since still reads net-up over the window — which is a delivery
landing into an *active* eco hand, the opposite of saturation. The peak test is
a shape test over the nine samples already held; it is **not** a confirmation
delay (those are what the 10.3%-sustained figure forbids) and it is free at a
genuine crossing, where the bank is the window maximum by construction. It is
its own flag so an arm can price it.

### 1.3 Why the state lives per-body and not in the comms store

⛔ **The engine gives EVERY UNIT ITS OWN `Player` INSTANCE** — stated verbatim at
`.venv/lib/python3.13/site-packages/fcode/data/starter_bot.py:3`: *"Each unit
gets its own Player instance; the engine calls run() once per round."* So `self`
is **not** a team channel, and a naive "the Core computes it, the raider reads
it" design needs a store slot. **All 16 slots already have a live writer**
(mapped in this build's precondition read; the only reclaimable capacity is
bit-level, chiefly slot 13 bits 11-31).

The design avoids the question entirely: the gate's **inputs are team-global**
(`get_global_resources()` and `read_store(SLOT_HARVESTERS)`), so two bodies that
have been alive the same rounds reach the same verdict without any coordination.
A body born mid-game simply has no history yet and cannot fire until it has 8
rounds of it — the conservative direction. Cost: **nine integers and O(1) per
unit per round**, no map scan, no cache invalidation.

---

## 2. THE CONSUMER (#80's half)

### 2.1 What the field evidence actually specifies

From `docs/research/REPLAY-STUDY-focalground-bankburst-2026-08-21.md` (their v32,
n=80): the burst is a **forward siege**, not a home battery — 67% of their
sentinels sit within d² ≤ 32 of the **enemy** core, 7% within d² ≤ 32 of their
own; **first sentinel → enemy core death median 30 rounds** (n=48 v32, n=201
v18–22); **P(kill | salvo of ≥2 within 12 rounds) = 0.92 vs 0.00 without**
(⚠ a collider — losing early prevents the salvo — so it reads as *"their kill
channel IS the pair"*, never as an effect size). A pair landing r150 kills ~r180:
inside `KILL_TARGET`, well inside `DEFENCE_ADMISSION_BAR`'s r300.

**⛔ WHAT IS NOT COPIED: their 750–800 Ti threshold.** Our median peak bank is
470 = the opening endowment, and it is 470 through p95. Copying the threshold
copies a delay we cannot pay for. What transfers is the SHAPE — an edge, then a
pair — at our bank size.

### 2.2 The one thing that was structurally missing, and it is the SECOND sentinel

Grepped against the parent, not asserted:

* `_fs_try_sentinel` (`siege.py:6040` in the parent) **already** does everything
  the study describes about siting: it scores the ≤4 tiles orthogonally adjacent
  to the raider, requires `can_fire_from(pos, facing, SENTINEL, core_tile)` and
  **d² ≤ 32 to an enemy core tile**, excludes ring seats, penalises visible enemy
  gunner axes, and prefers a **different side** of the core for the second. **It
  is reused verbatim and not modified.**
* `FS_SENTINEL_MAX = 2` and `FS_SENT_BUY_MAX = 4` **already permit a pair.** No
  cap was raised by this build.
* Sentinel **#1** already outranks the collar: `_v518_early_sentinel`, gated
  `live <= FS_V518_EARLY_MAX_LIVE` (= 0), i.e. it shuts the moment one sentinel
  stands.
* Sentinel **#2** exists only as **rung 4** — the bottom of the ladder, whose own
  docstring says it "fires on the rounds the collar has nothing actionable left"
  — and it must clear `len(needed) × barrier_cost + sentinel_cost` (the whole
  remaining collar) **plus** `FS_SENT_REBUY_TI`.

⇒ **the burst window's job is to let the pair close.** `_v543_pair` sits in the
ladder directly below `_v518_early_sentinel` and directly above rung 1
(`siege.py` ladder, the `not _v521_near` block).

**What is waived, precisely:** `_fs_sentinel_ok` — the collar reserve and the
salt/eco disjunct gate — replaced by `sentinel_cost + FS_V543_RESERVE (24)`.
**What is NOT waived:** every guard inside `_fs_try_sentinel` — `FS_SENTINEL_MAX`
live, `FS_SENT_BUY_MAX` lifetime purchases, `FS_SENTINEL_TI_FLOOR`, the
`FS_SENT_REBUY_TI` surcharge on purchases after the first (**and
`FS_V543_RESERVE` is set EQUAL to it, 24, so the rebuy guard survives
numerically intact**), the d² ≤ 32 siting, the alignment predicate, the gunner-
axis/ring/side scoring.

⛔ **`_v543_pair` does not call `_fs_rung`.** That falsifier re-asks every *higher*
rung and reports a non-empty `hi` list as a bug; a clause that deliberately
outranks rung 1 would trip it on every firing. `_v518_early_sentinel` does not
call it either, for the same reason.

**"Second follows first as soon as fundable"** is exactly what the window
implements: the clause re-runs every ring round the window is open and buys the
moment `ti ≥ sentinel_cost + 24` again, without waiting for another crossing.

### 2.2b ⭐⭐ THE BYPASS OF `_fs_sentinel_ok` IS DELIBERATE, AND v177's MAIDEN DECODE IS WHY

Relayed mid-build by the coordinating lane from
`docs/research/DECODE-ringrace-8013d088-2026-08-21.md` (v177's maiden, 5 games):

* **our forward sentinel lands r100–128; the opponent's lands r21–58**;
* **first core damage = our-forward-sentinel-round + 1 in 4/4** — the sentinel
  *is* the damage clock;
* conversion cost from raider arrival to sentinel: **91–112 rounds**;
* **the binding term is `_fs_sentinel_ok` (`siege.py:5792`): its salt disjunct
  fired 0 times in 5 games**, so every sentinel waited out
  `FS_SENT_RND_FLOOR = 60` (`doctrine.py:3165`) on the eco disjunct **plus 40–68
  further rounds of hesitancy**;
* all core damage in the maiden was sentinel −18; **zero builder pecks** —
  consistent with the pair being the kill channel this plank funds.

⇒ **A burst whose median first crossing is r67, routed through a gate that
cannot open before r60 and in practice opens 40–68 rounds after that, would be
throttled by the exact path that makes the shipped bot late.** The edge trigger
exists to buy the pair EARLY; running it through that gate would delete its
reason to exist.

**The build already satisfies this and it was verified rather than assumed:**
`_v543_pair` carries its **own** funding disjunct (`ti ≥ sentinel_cost +
FS_V543_RESERVE`) and **never calls `_fs_sentinel_ok`**; `_fs_try_sentinel`,
which it does call, contains **zero** references to that gate, to the salt/eco
disjuncts or to `FS_SENT_RND_FLOOR` (grepped over the whole function body).
**The bypass is FLAG-SCOPED — a new disjunct inside a `LOKI_FS_V543`-guarded
clause, not an edit to the shared gate** — so with the master off every other
caller meets `_fs_sentinel_ok` exactly as the parent wrote it, which is also
what keeps the ablation identity in §3 intact.

⭐ **Observed, not just argued: the forced-dose probe bought its sentinel at
r28 on atoll s7 (§4.4) — 32 rounds INSIDE the r60 floor** the eco disjunct would
have imposed on every other route to a forward sentinel.

⚠ **The obvious hazard of a bypass, named:** `_fs_sentinel_ok`'s eco disjunct
also encodes *"we can sustain a sentinel"* (two connected harvesters). The burst
substitutes its own income evidence for that — `FS_V543_MIN_HARV = 2` plus a
bank that is net non-falling over 8 rounds — which is a **stronger** income
statement than the gate's, but it is a different one, and it is not the term the
gate was tuned on. If the screen shows bursts buying sentinels that immediately
starve for ammunition, this is the first place to look.

### 2.3 Ammo — integrated, not duplicated

The parent already converts in small just-in-time chunks off a demand-driven
ladder keyed to `SLOT_FWD_GUN`: `ammo_target = max(…, min(120, 40 + 20 ×
fwd_guns))`, i.e. **60 for one forward sentinel and 80 for a pair**, converted in
`chunk` steps by the Core at `main.py`'s drip. **None of that is duplicated and
`ammo_target` is untouched.**

The defect the plank would otherwise create is in the **floor**, not the target:
the drip is gated `ti > ti_floor`, and under seal-only `ti_floor ≥ 12 × barrier +
FS_SEAL_MARGIN + 6` — roughly 120 Ti at the measured 2.6–3.1× scale — while a
200-Ti burst that has just bought a pair leaves ~20. **Without a waiver the pair
stands empty until the bank climbs back over a reserve the burst itself just
spent.** (Focalground hit the mirror image and it is SURPRISE #1 of the study:
they hold *zero* ammunition through the whole buildup, so a builder killed on the
round it plants sentinel #1 leaves them with 800 idle Ti.)

`_v543_ammo_waive` lowers **only that floor**, to `FS_V543_AMMO_FLOOR = 12`, and
is bounded four ways: a window must be open; `SLOT_FWD_GUN` must be non-zero (a
forward sentinel was actually bought); the floor never goes below 12 (one barrier
stays affordable); and at most `FS_V543_AMMO_MAX = 120` Ti may be converted under
the waiver per match, **charged in full** (over-charging spends the budget
faster, which is the conservative direction).

⚠ **Note a free interaction, in our favour:** the T4 ghost-magazine brake zeroes
`fwd_guns` when the magazine has not fallen for `T4_AMMO_IDLE_RNDS` rounds, i.e.
when nothing is firing. The waiver reads the same variable, so **a dead forward
sentinel switches the waiver off automatically.** No new code.

---

## 3. THE FLAG-OFF ABLATION IDENTITY

**The claim, stated so it can fail:** with `LOKI_FS_V543 = False`,
`bots/_v543burst` behaves exactly as `bots/_v542wave`.

**Argument 1 — the diff is ADD-ONLY.** `diff -r` reports **0 deleted and 0
modified lines** in all five files; 538 lines are inserted and nothing else
changes. A parent behaviour that is never edited cannot be altered except through
one of the inserted read sites, and those are enumerable.

**Argument 2 — every inserted read site is master-dominated, checked
mechanically.** `scratchpad/s53_v543_build/flagoff_audit.py` (adapted verbatim
from the v541 build's instrument; only the flag table and the selftest cases are
renamed) enforces three rules by AST: **R1** no module-level assignment reads a
v543 name (arm construction appends overrides to `doctrine.py`'s end, so a
derived module-level constant would carry the pre-override value); **R2** every
subordinate-flag read is either lexically inside a `_v543_*` method or
short-circuit-dominated by `LOKI_FS_V543`; **R3** every call into the `_v543_*`
family from outside it is short-circuit-dominated by `LOKI_FS_V543`.

```
--selftest            10 cases, 3 rules, each driven to BOTH verdicts -> PASS
bots/_v543burst       CLEAN -- R1/R2/R3 satisfied (master=LOKI_FS_V543, 16 subordinate flags)
MUTATION CONTROL      one guard removed from main.py -> VIOLATIONS: 3 (R3 + 2×R2), exit 1
```

The mutation control is the part that makes the CLEAN meaningful: an audit that
has never returned a violation on this tree has not been seen to audit.

**Argument 3 — the state initialisation is unconditional and that is harmless.**
`main.py`'s `__init__` sets thirteen `v543_*` fields unconditionally (`-1`, `[]`,
`False`, `0`). **Writing a field nobody reads cannot change behaviour**, and R2/R3
enumerate every read. This is the same argument the v541 build made for its three
fields, and it is stated rather than hidden.

**Argument 4 — the state machine is inert with the flag off, tested.**
`gate_test.py` drives `_v543_tick` with the master off and with the plank off
over a trace that fires twice with them on: **0 fires, 0 open rounds, and
`v543_rnd` still `-1` with `v543_hist` still empty** — the method returns on its
first line and does not even record history.

⛔ **WHAT IS MISSING, AND IT IS THE HALF THIS TREE CANNOT SUPPLY: THE DYNAMIC
IDENTITY.** The house standard is a paired NOISE_OFF battery — flag-off arm vs
the frozen parent, same seeds, expect 0 rows differing, with the same tape
showing the plank moved something when it is on. **That battery was not run
here** (the box is on an 8-worker ANCHOR-CLASS corefill battery and this build is
under a near-zero-local-game budget). **The static audit is a lexical/short-
circuit argument, not a reachability proof** — it would not catch a guard hidden
behind an intermediate variable. **The screen lane owns the dynamic half.**

---

## 4. SELF-CHECKS RUN

### 4.1 The gate state-machine test — `scratchpad/s53_v543_build/gate_test.py`

Drives `_v543_tick` against synthetic bank traces with a stub controller. **Ten
checks, and every guard is driven to BOTH verdicts:**

```
PASS  opening endowment never fires          fires=[]        (470 flat, 60 rounds)
PASS  crossing from below fires              fires=[11]
PASS  window opens for FS_V543_WINDOW rounds fire=11 last_open=25
PASS  falling bank does not fire             fires=[] spent=7   (PEAK clause)
PASS  no harvesters does not fire            fires=[] noharv=15
PASS  two crossings, two windows             fires=[10, 81]
PASS  MAX_FIRES caps the windows             fires=3 cap=3
PASS  master off never fires                 rnd=-1 hist=[]
PASS  plank off never fires                  rnd=-1
PASS  never-seen-below never arms            (bank starts and stays at 250)
FAILURES: 0
```

⭐ **This test earned its place before it passed: its "falling bank" case FAILED
on the first run and that failure is what produced `FS_V543_PEAK`** (§1.2). A
test that only ever agreed with the code would have shipped the weaker gate.

### 4.2 Compile / import

`python -m py_compile` on all five files: OK. Import smoke of `main.py` under
`.venv/bin/python` (3.13.7): `Player()` constructs, all thirteen `v543_*` fields
present, all four `_v543_*` methods bound, `LOKI_FS_V543=True FS_V543_BURST=True
FS_V543_BURST_TI=200 FS_V543_WINDOW=40 FS_V543_LOG=False`, `NOISE_ON=True` (the
parent's shipped value — see §6).

### 4.3 ⚠ LIVE SMOKE — TWO GAMES, AND THE MECHANISM READ IS **ZERO**

Two single games were run `nice -n 19` against the running corefill battery (load
was 4.7 of 10 cores; a single extra process is a throughput perturbation, not a
correctness one — each game is its own process with its own seed). The tree on
disk was **not** used directly: a scratch copy with `FS_V543_LOG = True` and
`NOISE_ON = False` appended was played against `bots/_v542wave`.

| | map/seed | result | tracebacks | `V543` tape lines |
|---|---|---|---|---|
| smoke 1 | midgard s21 | **A wins, core_destroyed, r365** | **0** | **0** |
| smoke 2 | midgard s21 (+ positive control) | **A wins, core_destroyed, r294** | **0** | **0** |

**⛔ READ THE MECHANISM FIRST, AND IT SAYS THE TRIGGER NEVER FIRED.** Per the
row's own instruction, a flat outcome with a zero dose says nothing about the
plank. Both games are clean (0 tracebacks, 0 destroyed units, both won by core
kill inside r300), but **neither exercised the plank.**

**AND THE INSTRUMENT IS NOT BLIND — that was checked rather than assumed.**
Smoke 2 additionally set `FS_V518_TIWATCH = True`, whose tape uses the same
stderr channel; it emitted **294 lines**. So the channel works and `0` is a real
count.

**WHY IT DID NOT FIRE, off that same tape:** the game contains **no edge crossing
of 200 Ti at all.** The bank runs 500 → 470 → 434 → … and is ≥200 on only **16
of 294 rounds, all before the first dip below 200**; the simulated
armed-from-below crossing count over the whole game is **0**. Max bank = 500, at
r0. This is one game inside the 74.4% of games where the corpus says a 200-Ti
crossing does not occur; it is **a sample of one and is not evidence about the
fire rate.**

⚠ **The two games are not a matched pair and must not be read as one:** the
opponent tree ships `NOISE_ON = True`, so the same seed gave 365 and 294 rounds.
Determinism requires a NOISE_OFF opponent, which is a battery-construction task.

### 4.4 ⭐ THE FORCED-DOSE PROBE — the consumer path RUNS END TO END, and a map-coverage defect fell out of it

A zero-dose smoke proves nothing about the consumer, so a **scratch probe arm**
(threshold dropped to `FS_V543_BURST_TI = FS_V543_REARM_TI = 60`, tape on, noise
off — **not a shippable configuration and it exists nowhere in `bots/`**) was run
to force the path. Two games, both `nice -n 19`.

**atoll s7 — the plank executes end to end, 0 tracebacks, won by core kill:**

```
V543 FIRE 24 id 1  ti 93  rise 46 harv 2 n 1 until 64     <- Core
V543 FIRE 24 id 3  ti 93  rise 46 harv 2 n 1 until 64     <- raider
V543 FIRE 24 id 15 ti 93  rise 46 harv 2 n 1 until 64     <- raider
V543 PAIR 28 id 3  live 0 ti 103 need 7 orth 5 n 1 until 64
V543 AMMO 30 amt 27 floor 12 fwd 1 spent 27 bind 1
V543 FIRE 66 id 15 ti 101 rise 32 harv 3 n 2 until 106
V543 PAIR 100 id 15 live 0 ti 113 need 6 orth 5 n 1 until 106
V543 AMMO 102 amt 16 floor 12 fwd 2 spent 63 bind 4
```

Three things are settled by that tape and each was a real open question:
* **the gate, the consumer and the magazine all execute**, in that order, with
  no exception and no destroyed unit;
* **three different bodies reached the identical verdict on the identical round
  (r24) with no coordination** — the per-body design's whole premise, observed
  rather than argued;
* **the ammo waiver binds and converts** (`floor 12`, `fwd` rising 1 → 2), which
  is the failure this build predicted and pre-empted.

⚠ **AND ONE THING IT DOES NOT SHOW: A SIMULTANEOUS PAIR.** Both purchases read
`live 0` — the second (r100) is a **replacement** for a dead first, not a second
barrel. On this cell the plank bought a sentinel and later re-bought one. **The
pair is the plank's thesis and this probe did not demonstrate it.** Nor can the
r28 purchase be attributed to the plank without an ablation arm — `_v518_early_
sentinel` might have taken it a few rounds later. Both are screen questions.

**⛔ midgard s21 — 0 `PAIR` lines, AND THE REASON IS A COVERAGE DEFECT WORTH MORE
THAN THE PROBE.** The same arm fires the gate three times (r34/r77/r118, all
`id 1`) and never buys. A one-line debug tape added to the probe arm's `_fs_turn`
emitted **0 lines in the entire midgard game against 222 on atoll**:

> **⇒ ON MIDGARD THE FERRY-SIEGE LANE NEVER RUNS AT ALL, so `_v543_pair` — which
> lives in that lane's ladder — HAS NO SITE TO EXECUTE FROM.** The forward
> sentinel that midgard *does* buy comes from `raid.py:_try_forward_sentinel`, a
> different lane with its own cap and its own 40-Ti floor.

**This is a real scope limit on the plank and it is stated here rather than
discovered by a flat screen** (§7.7): the map gating that `_v534`/`_v535`/`_v538`
built decides whether this plank has a consumer at all. **The screen must select
maps where the FS lane runs, or it will measure a gate with nothing attached.**
⚠ **And note what it implies for the raid lane: at burst time the raid path's own
`ti ≥ cost + LOKI_FWD_TI_FLOOR (40)` is ALREADY satisfied** (a 200-Ti bank buys a
60–91-Ti sentinel with room to spare), so a burst clause there would add
approximately nothing — **the FS ladder is starved and the raid lane is not.**
That is why the plank is scoped to the FS lane, and it is an argument, not a
measurement.

### 4.5 TWO ORDERING DEFECTS FOUND ON REVIEW, AFTER THE FIRST SMOKE, AND FIXED

Both are the same class — *the state machine was only being ticked on the paths
that consume it* — and neither would have raised an exception or shown up in a
compile:

1. **`_v543_ammo_waive` tested `fwd_guns` BEFORE ticking.** The Core would then
   record no bank history until the first forward sentinel was already standing,
   and would need `FS_V543_RISE_RNDS` further rounds before the waiver could
   bind — a delay landing exactly on the rounds the fresh pair has an empty
   magazine, i.e. on the state the waiver exists for. **Fixed: tick first,
   unconditionally.**
2. **Raider bodies only ticked inside `_v543_pair`**, which sits behind
   `action_cooldown == 0`, behind arrival at the ring and behind `not
   _v521_near`. A body ticking only there carries a history full of holes and —
   worse — **can arrive at the ring during a high-bank phase, never once observe
   `ti < 200`, and therefore NEVER ARM.** **Fixed: `_fs_turn` ticks once per
   round for every raider**, on the body's own clock rather than the ladder's;
   `_v543_tick` is idempotent per round so the ladder's call is still correct.

The atoll tape in §4.4 is post-fix and is what shows three bodies agreeing on
r24; the §4.3 smoke games are pre-fix, which does not affect their reading (both
contained no crossing at any threshold).

### 4.7 ⭐⭐ THE DOSE PRE-READ — MEASURED ON 1,405 REAL RATED GAME-SIDES, AND IT CORRECTS THIS BUILD'S OWN DOCTRINE COMMENT

Commissioned alongside the build and run against the corpus, **not** against our
own arena: the exact `_v543_tick` predicate replayed over per-round bank series
decoded at `--step 1` from `replay_archive` (`tools/bank_under_harassment.py`
primitives). **Population: 1,405 game-sides, our versions 159–177, 100% RATED
LADDER** (all 1,405 match ids present in `ladder_games.tsv`, 0 in
`unrated_games.tsv` — no rated/unrated pooling). Median series 222 rounds; only
30.8% of games survive past r300. Harvester clause modelled as the monotone
high-water ratchet, which is `SLOT_HARVESTERS`'s real semantics.

**NEGATIVE CONTROL, and it must come out the other way for any of this to
count:** the same simulator with the latch replaced by a bare level test
`bank ≥ 200` fires in **1,405 of 1,405 game-sides at median round 0** (r0 bank
reads exactly 470). The instrument can produce the other verdict.

| arm | fires ≥1× (ALL, n=1405) | 172–177 (n=195) | first fire, median | fires before r300 (all games) |
|---|---|---|---|---|
| **150 / 150** (fallback) | **35.5%** | 29.2% | **r127** IQR[83,192] | **31.5%** |
| **200 / 200** (shipped) | **17.5%** ±2.5pp | 15.4% ±6.3pp | r178.5 IQR[83,275] | 14.1% |
| 260 / 260 | 11.5% | 9.2% | r196 | 8.3% |

*(intervals with the rated DEFF = 1.529 applied.)* Capture rate against the
crossings that exist at all: 96% at 150, 84% at 200, 85% at 260 — **the gate is
not throwing away available crossings; the threshold is what there is.**

⛔⛔ **AND HERE IS THE CORRECTION, WRITTEN DOWN BECAUSE IT FALSIFIES A CLAIM THIS
BUILD PUT IN ITS OWN DOCTRINE BLOCK.** The full 2×2×2 decomposition (latch ×
PEAK × RISE) over the same 1,405 series:

```
latch peak rise   fires   rate
  1    1    1      246    17.5%   <- shipped
  1    1    0      246    17.5%
  1    0    1      246    17.5%
  0    1    1      246    17.5%   <- LATCH REMOVED: byte-identical
  0    0    0      277    19.7%   <- only removing ALL THREE moves anything
```

**Removing the arm-from-below latch alone costs exactly 0.0pp.** My docstring
argued the latch is what keeps the 470-Ti opening endowment out; on real series
**it is `FS_V543_MIN_HARV` that does that** (the harvester ratchet does not reach
2 by r7). The three clauses are complete substitutes — any one of them suppresses
the same ~31 games — and the `HISTORY DEPTH` clause is **exactly inert**.
Dropping `harv ≥ 2` on its own is worth +1.1pp.

**What I changed and what I did not.** The latch and both qualifiers **stay**:
each costs zero, the latch is the semantically correct guard, and unlike the
harvester clause it does not depend on the eco lane's timing to hold. **The
doctrine comment is amended in place** (`doctrine.py`, above `FS_V543_REARM_TI`)
so nobody cites the latch as load-bearing on the strength of a synthetic trace.
⚠ **This is exactly the failure mode the house rules name: a guard that has never
been driven to the other verdict on the real distribution has not been seen to
guard.** My `gate_test.py` case *"opening endowment never fires"* is true of a
flat-470 synthetic and does not establish what it appeared to establish.

**⛔ WHAT THIS MEANS FOR THE PREREG, and it is not comfortable: at the shipped
200/200 the plank is INERT IN ~5 OF EVERY 6 GAMES, and the median first fire
(r178) sits close to the r300 bar with only 14.1% of ALL game-sides firing before
it.** On dose grounds the **150/150 arm is the one worth firing first** (~2× the
dose, median r127, 31.5% before r300). That is a screen decision for the owning
lane, not mine — but the number belongs in the prereg before the leg, not after.

**Caveats carried verbatim from the measurement:** (i) these are trajectories from
bots that do **not** contain the plank, so the ≥1-fire rate and the first-fire
round are sound counterfactuals while everything downstream (2nd/3rd fires) is
not — the plank re-shapes the series it reads; (ii) simulated as **one body alive
from r0**, so per-body divergence and mid-game births are unmodelled (the
conservative direction); (iii) it assumes the tick is reached every round, which
is what §4.5's second fix now guarantees for raiders and which the Core satisfies
outside the endgame branch; (iv) 69.2% of game-sides end before r300, so "never
fired" and "the game was already over" are confounded — **conditional on reaching
r300 the rate is 24.9%.**

### 4.6 CPU

`_v543_tick` is O(1) per unit per round: one `get_global_resources`, one
`read_store` on the fire path only, and a list of at most nine `(round, bank)`
pairs pruned by a `while`. No map scan, no BFS, no per-round full-map read. The
`FS_V543_PEAK` loop is over those same ≤9 entries.

---

## 5. FILES AND LINES TOUCHED

```
bots/_v543burst/doctrine.py  +192  -0     the constant block (EOF append, house pattern)
bots/_v543burst/siege.py     +295  -0     _v543_on/_v543_tick/_v543_pair/_v543_ammo_waive/
                                          _v543_ammo_spent  +  the ladder insertion
bots/_v543burst/main.py       +51  -0     __init__ state (13 fields) + the convert-floor
                                          waiver + its accounting call
bots/_v543burst/eco.py         0   -0     byte-identical to _v542wave
bots/_v543burst/raid.py        0   -0     byte-identical to _v542wave
                             ----  ---
                             +538   -0    ADD-ONLY
```

Insertion points (line numbers in `_v543burst`):

| what | site |
|---|---|
| constant block | `doctrine.py:6081-6258` (EOF append, after the v541 block; master at `:6160`) |
| `_v543_*` methods | `siege.py:2885-3124` (`_v543_on` `:2891`, `_v543_tick` `:2894`, `_v543_pair` `:3006`, `_v543_ammo_waive` `:3078`, `_v543_ammo_spent` `:3109` — immediately after `_v518_early_sentinel`, before `_v518_gap_mark`) |
| ladder insertion (rung 1'b) | `siege.py:3798-3814` (inside the `not _v521_near` block, below `_v518_early_sentinel`, above rung 1) |
| per-body state | `main.py:221-246` |
| convert-floor waiver | `main.py:1092-1111` |
| waiver accounting | `main.py:1126-1130` |

**Mechanism counters — where they are:**

| counter | meaning |
|---|---|
| `self.v543_fires` | **windows opened (the row's "trigger fires per game")** |
| `self.v543_bought` | **sentinels this clause bought (the pair-landed counter)** |
| `self.v543_full` / `v543_poor` / `v543_nosite` | consumer refusals: pair already standing / bank under cost+reserve / no aligned d²≤32 site |
| `self.v543_spent` / `v543_noharv` | gate non-fires: bank fell or was not the window peak / under `FS_V543_MIN_HARV` |
| `self.v543_ammo_ti` / `v543_ammo_bind` | Ti converted under the waiver, and the rounds it actually lowered the floor (the denominator that makes a zero readable) |

**Tape:** `FS_V543_LOG = False` **on disk**, stderr only, three record types —
`V543 FIRE rnd id ti rise harv n until`, `V543 PAIR rnd id live ti need orth n
until`, `V543 AMMO rnd amt floor fwd spent bind`. **`pair-landed-round` is also
readable ENGINE-SIDE** from sentinel creation events and positions in a local
replay, which is the reading that does not depend on our own stdout at all
(platform replays strip it; local screens are the fixture here either way).

---

## 6. NOISE / DEBUG FLAGS — UNCHANGED FROM THE PARENT

Verified by diff: `bots/_v543burst/doctrine.py` is `_v542wave`'s bytes followed by
the v543 block, so **every pre-existing flag carries its parent value
unchanged**, including `NOISE_ON = True`, `LOKI_BELTBREAK_LOG = True`,
`LOKI_L4_LOG = True`, `LOKI_SAMESTOP_LOG = True` and all 45 `*_LOG` flags that
ship `False`. The new `FS_V543_LOG` ships `False`, like every other instrument in
this tree.

⚠ **`NOISE_ON = True` is the parent's shipped value and is what makes paired
identity games require a NOISE_OFF arm on BOTH sides.** The smoke arm used for
§4.3 was a scratch copy outside `bots/`; the shipped tree has no smoke edits.

---

## 7. KNOWN RISKS AND OPEN QUESTIONS

1. **⚠ THE DOSE IS THE WHOLE RISK.** The corpus says a 200-Ti crossing occurs in
   25.6% of games; the gate adds a peak test, a net-rise test and a harvester
   floor on top of that, each of which can only reduce it. **If the screen reads
   a near-zero dose the primary is uninformative** — this is the soft-knob lesson
   the row already carries. The **pre-registered fallback arm** is
   `FS_V543_BURST_TI = FS_V543_REARM_TI = 150` (menu: fires 47.3%, median r95,
   36.9% before r150) — named here, before any data, so it cannot be chosen
   afterwards. ⭐ **THE DOSE PRE-READ CAME BACK AND IT VINDICATES THE FALLBACK
   BEFORE THE SCREEN RUNS: 17.5% at the shipped 200 against 35.5% at 150, with
   the median first fire moving r178 → r127** (§4.7, n=1,405 rated game-sides).
   The shipped arm is thin enough that a flat primary would be uninformative by
   construction.
2. **The collar-reserve waiver is a real cost and it is not measured here.**
   Inside a window the pair outranks barriers and is funded from money the collar
   was holding. `_v518_early_sentinel`'s own build measured its (tighter) version
   of the same displacement at ~one barrier-round per period with no forward
   sentinel alive. **Ours is looser** — it waives the reserve, not just the wait.
   The screen must carry the collar-closure and barrier counters, not only the
   kill round.
3. **The ammo waiver inverts a `max()` cascade, which nothing else in this tree
   does.** It is bounded four ways (§2.3) and its binding is counted
   (`v543_ammo_bind`), but the deadlock argument that built the collar floor —
   *two reserves that can meet on the same bank deadlock* — is exactly what a
   lowered floor plays with. **Watch for barrier starvation inside windows.**
4. **`FS_V543_MAX_FIRES` is per BODY, not per team.** Three raiders can open
   three windows each. Bounded in practice by `FS_SENT_BUY_MAX = 4` lifetime
   purchases and `FS_SENTINEL_MAX = 2` live, both untouched — but the *window*
   count in a tape is a per-body number and must be summed carefully.
5. **`SLOT_HARVESTERS` is a high-water mark, not a live census.** The
   income-exists clause therefore reads "we have built two harvesters", not "two
   are alive". The net-rise clause is the term that actually detects income, so
   this is a floor, not the load-bearing test — but it is a known
   over-permissiveness.
7. **⛔ MAP COVERAGE — THE CONSUMER ONLY EXISTS WHERE THE FERRY-SIEGE LANE
   RUNS.** Measured, not assumed (§4.4): `_fs_turn` was called **222 times on
   atoll s7 and 0 times on midgard s21**. On maps where the FS lane is gated
   off, the gate still fires and there is nothing to spend it on. **A screen
   pooled over a map set that is mostly FS-gated will read a near-zero pair
   count and it will not be the plank's fault.** Either select the map pool or
   report the FS-lane share alongside the dose.
6. **Bodies born mid-game are conservative by construction** (no history ⇒ no
   fire for 8 rounds, and no fire ever if they never observe a sub-200 bank).
   Acceptable, and stated so a zero from a late body is not read as a bug.

---

## 8. DELIBERATE DEVIATIONS FROM THE BRIEF

1. **The consumer does NOT override v521's NEAR suppression.** The brief asked
   for a pair on trigger; the ladder suppresses a *second* sentinel while the
   collar is one or two seats from closing (`_v521_near`), a clause that was
   screened on its own with an explicit asymmetric argument. `_v543_pair` sits
   **inside** the `not _v521_near` block, so that measured behaviour is
   unchanged. Overriding it would have been a second, entangled change. **Open
   question for the owning lane: is the NEAR suppression right *inside a burst
   window*, when the money is provably there?**
2. **No raider BODY is funded by the burst.** The study's lead indicator is a
   builder camping at d² ≤ 32 for a median 30 rounds before the sentinel, and the
   brief mentioned funding the pair "plus their ammo" only. Spawning extra
   forward bodies on the trigger would add +20% cost scale each and is a
   different plank; the burst spends only on hardware and magazine. Named as an
   open follow-up, not silently dropped.
3. **`FS_V543_PEAK` is an addition to the specified qualifier**, not in the
   brief's wording — added because the build's own test falsified the plain
   net-rise form (§1.2). It is separately flagged so it can be priced or removed.
4. **`FS_V543_MAX_FIRES = 3` and `FS_V543_WINDOW = 40` are my numbers**, not the
   evidence's. The evidence pins the threshold (200) and the shape (edge, pair);
   the window length is argued from the study's 40-round pre-burst doubling and
   its 30-round pair→death constant, and the fire cap is the house convention
   that every repeated verb carries a bound. **Both are tunable and neither is
   measured.**
5. **Only 2 live smoke games, not a battery.** The brief allowed skipping live
   smoke entirely if the corefill battery was at risk; two `nice`d single games
   were judged a smaller perturbation than shipping a tree that had never met the
   engine. The dynamic identity battery was **not** run (§3).

---

## 9. REPRODUCING THIS

```bash
# static flag-off audit (self-test first -- it must fail on its own dirty cases)
.venv/bin/python scratchpad/s53_v543_build/flagoff_audit.py --selftest
.venv/bin/python scratchpad/s53_v543_build/flagoff_audit.py bots/_v543burst

# the gate state machine, both verdicts on every guard
.venv/bin/python scratchpad/s53_v543_build/gate_test.py bots/_v543burst

# one instrumented live game (tape on, decision noise off, scratch arm only)
cp -R bots/_v543burst /tmp/logarm
printf '\nFS_V543_LOG = True\nNOISE_ON = False\n' >> /tmp/logarm/doctrine.py
.venv/bin/fcode run /tmp/logarm bots/_v542wave maps/midgard.map26 \
    --seed 21 --tle 10 --json --replay /tmp/smoke.json 2>/tmp/smoke.err
grep '^V543' /tmp/smoke.err          # mechanism counters
```
