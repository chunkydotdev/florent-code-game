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

1. **THE DIFF IS ADD-ONLY: 483 inserted lines, ZERO deleted, ZERO modified,
   across three files** (`doctrine.py` +178, `siege.py` +254, `main.py` +51;
   `eco.py` and `raid.py` byte-identical). Nothing in the parent's behaviour is
   edited — the plank is inserted, never substituted.
2. **The gate arms FROM BELOW, and that is the whole reason it is not
   `LOKI_SURPLUS_TI` in a new costume.** The game starts at 470 Ti, so a level
   test on 200 is satisfied at r0 in 100.0% of games; `v543_armed` starts
   `False` and is set only by an observation of `ti < 200`. The build's own
   state-machine test drives this to both verdicts (§4.1).
3. **The consumer is the SECOND sentinel, because the first already jumps the
   collar and the second does not.** `_v518_early_sentinel` is gated on
   `live <= 0`; after that the only route to a pair is rung 4, the *bottom* of
   the ladder, plus a rebuy surcharge on top of the whole remaining collar
   reserve. The burst window replaces the collar reserve — and nothing else —
   for at most two live sentinels (§2.2).
4. **⚠ MECHANISM FIRST, AND THE FIRST READ IS ZERO: the gate fired 0 times in
   the one instrumented live game (midgard s21, 294 rounds), and the tape says
   why — that game contains NO edge crossing of 200 Ti at all** (bank falls from
   500 and is ≥200 on only 16 rounds, all before the first dip). The instrument
   is not blind: the same run's positive-control tape emitted 294 lines (§4.3).
   The corpus says crossings exist in 25.6% of games at a median r67; one game
   is a sample of one.
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
modified lines** in all five files; 483 lines are inserted and nothing else
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

### 4.4 CPU

`_v543_tick` is O(1) per unit per round: one `get_global_resources`, one
`read_store` on the fire path only, and a list of at most nine `(round, bank)`
pairs pruned by a `while`. No map scan, no BFS, no per-round full-map read. The
`FS_V543_PEAK` loop is over those same ≤9 entries.

---

## 5. FILES AND LINES TOUCHED

```
bots/_v543burst/doctrine.py  +178  -0     the constant block (EOF append, house pattern)
bots/_v543burst/siege.py     +254  -0     _v543_on/_v543_tick/_v543_pair/_v543_ammo_waive/
                                          _v543_ammo_spent  +  the ladder insertion
bots/_v543burst/main.py       +51  -0     __init__ state (13 fields) + the convert-floor
                                          waiver + its accounting call
bots/_v543burst/eco.py         0   -0     byte-identical to _v542wave
bots/_v543burst/raid.py        0   -0     byte-identical to _v542wave
                             ----  ---
                             +483   -0    ADD-ONLY
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
   afterwards. A dose pre-read simulating this exact predicate over the corpus's
   per-round bank series was commissioned alongside this build; **its numbers are
   not in this report and must not be inferred from it.**
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
