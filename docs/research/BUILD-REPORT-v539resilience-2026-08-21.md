# BUILD REPORT — `bots/_v539resilience` (v539), s52, 2026-08-21

**ONE PLANK: WHEN THE ECONOMY IS DESTROYED, DETECT IT AND REBUILD THE MINIMUM
THAT RE-FUNDS THE KILL.** Parent `bots/_v537socket`, md5-frozen at `07:35:52Z`
and re-verified byte-unchanged at `07:54:41Z`
(`scratchpad/s52_v539_build/PARENT_FREEZE.md5`, `PARENT_REFREEZE.md5`).

Magnus, watching the v174 rated loss to `lazy` (economy wiped by ~r100;
harvesters 0 and bank 5 Ti at r154; nothing ever rebuilt):

> *"Do we have any logic to re-establish our harvesting if we are attacked like
> this?"*

and, scoping the answer mid-build:

> *"maybe we shouldn't put effort into defending that much, we are an offensive
> player, we just want to hold out until we have killed the opponent. The issue
> is that we don't seem to put a sentinel at all in that game."*

This build wrote to `bots/_v539resilience`, `docs/research/` and
`scratchpad/s52_v539_build/` only. **No `tools/*` edit.** Wall clock from
`date -u` in the same shell call each time: context read `07:29:27Z`, parent
freeze + tree copy `07:35:52–07:36:00Z`, doctrine block `07:37:12Z`, code
`07:37–07:44Z`, harness build and its three false starts `07:41–07:51Z`,
NOISE_OFF determinism fix `07:50:54Z`, endgame battery run 1 `07:51:23Z`,
identity batteries `07:51:56Z`, consumer enumeration `07:53:50Z`, sentinel-gate
probe `07:54:31Z`, replicate run 2 `07:54:53Z`, parent re-freeze `07:54:41Z`.

---

## ⛔ TOP LINE — SEVEN SENTENCES

1. ⭐⭐ **THE COMMISSION'S ROOT CAUSE IS HALF RIGHT AND THE OTHER HALF POINTS
   THE OPPOSITE WAY.** `SLOT_HARVESTERS` really is a monotone high-water
   ratchet that lies after a wipe. But all **13** of its sites (11 reads)
   were enumerated (§3) and **the phantom makes them MORE permissive, not less** —
   the forward SENTINEL needs `>= 2`, the home LAUNCHER `>= 1`, both paving
   gates `>= 1`/`>= 2`. **Resetting the slot to an honest 0 would CLOSE the
   sentinel gate the phantom was holding open**, in the same breath in which
   Magnus asked why no sentinel was bought. The reset is therefore **BUILT AND
   SHIPPED OFF** (`FS_V539_HONEST_SLOT = False`) so a leg can price it.
2. ⭐ **THE TWO THINGS THAT ACTUALLY STOPPED THE REBUILD ARE FUNDING AND
   ROSTER, AND NEITHER IS THE RATCHET.** The bootstrap the commission thought
   was blocked is gated at `harv < ECO_CAP = 18`, so a phantom 5 never blocked
   it. What blocks it is (a) `_eco_spendable`'s collar + siege reserves sitting
   permanently above a wiped bank — the v513 change-C deadlock in its second
   costume — and (b) roles being assigned ONCE from a monotone ordinal with
   only `LOKI_ECO_SEATS = (1,2,3)` as economy, so **every replacement body
   spawned after a wipe is a RAIDER and the team has no expander for the rest
   of the match**.
3. **THE DETECTOR IS A DELIVERY DROUGHT, NOT A HEAD COUNT**, because no unit on
   this team can read a head count honestly (§2.1). The Core — already the
   single writer of `FS_ECO_SLOT` — declares famine when its own core-adjacent
   mouth has held no stack for 25 rounds, having delivered at least once. **It
   costs no store slot:** the famine bit and episode round ride bits 18 and
   19–29 of a word the Core already writes once per round.
4. **THE MECHANISM FIRES AND REPLICATES.** 25 paired (map, wipe-round) cells,
   NOISE_OFF, five pool maps: **first rebuild after the wipe — v539 earlier in
   21 cells, parent earlier in 0, 4 ties**; belt-mouth alive **20 v 1**;
   delivery sightings **19 v 1**. An independent replicate at five *different*
   wipe rounds reads **20 v 0 / 22 v 0 / 20 v 0**. Famine declared in **25/25**
   v539 cells and **0/25** parent cells.
5. ⚠ **THE COUNTER-CONTROL DOES NOT REPRODUCE "0 REBUILDS" AND THE REPORT SAYS
   SO.** The commission expected the parent to never rebuild. It usually does
   rebuild — **a median of 29 rounds later than v539** (mean 38.9, max 146,
   n = 46 of the 50 pooled cells where both arms rebuilt) — and it never
   rebuilds at all in **4 of 50** against v539's **0 of 50**. The sharper
   statistic is the belt: **the parent's core mouth is never alive again in
   7 of 50 cells; v539's in 0 of 50.** The plank's claim is TEMPO plus the
   elimination of that tail, not existence.
6. ⭐⭐ **THE SURPRISE, WRITTEN BEFORE IT IS EXPLAINED: v539 SPENDS ITS WAY OUT
   OF THE SENTINEL BAR.** Counting rounds after the wipe in which the bank sat
   at or above `sentinel + SIEGE_HEAL_RESERVE_TI` (107 Ti), **the PARENT is
   ahead in 16 of 25 cells and v539 in 0**; on atoll wipe@190 the parent builds
   3 post-wipe turrets to v539's 1. §6. No explanation is offered here.
7. ⚠ **NO PLAY, TEMPO, KILL-ROUND OR OUTCOME CLAIM IS MADE. THE DOSE IS
   DEFERRED AND NAMED.** The local box is running V537POOL (**2,461 of the
   required 5,400 rows at `07:54:41Z`**) and this build made **zero `fcode`
   runs**. Every number here is from a fake-engine unit harness with no
   opponent in it. **The tree may not enter any battery until the deferred
   items in §8 exist.**

---

## 0. ⛔ THE PARENT CHOICE IS A FORK, AND IT IS FLAGGED, NOT HIDDEN

The commission named `bots/_v537socket` as the parent verbatim and this build
obeyed it. **But the line has moved twice since v537**: `bots/_v538refine`
(gates the v537 socket claim on refusing maps) and `bots/_v541quiet` (spawned
at HEAD, `b0dbdb756`). **v539 is therefore a SIDE BRANCH off v537, not a
descendant of the current head**, and shipping it means re-merging the plank
onto whatever the head is at fire time. The plank is small and confined (§1),
so the re-merge is cheap — but it is a real cost and the decision to pay it is
not this build's to make.

---

## 1. THE PLANK AS BUILT

Seven edit sites, one doctrine block, **no new store slot**, **no `tools/*`
change**.

| # | file | site | what |
|---|---|---|---|
| A | `siege.py` | `_fs_eco_publish` | the latched early-return is skipped while the plank is on, so `held` is polled every round; the famine bits are folded into the **same single write** |
| B | `siege.py` | `_v539_famine_bits` (new) | CORE ONLY. Declare/clear the famine bit + episode round |
| C | `siege.py` | `_v539_famine_state` / `_v539_famine` / `_v539_lifeline` (new) | pure readers; every other body uses these |
| D | `main.py` | roster block, FS-appointment block, draft release | **RUNG B, the draft** |
| E | `main.py` | seat-3 defection | **RUNG C, the hold** |
| F | `eco.py` | `_eco_spendable` | **RUNG A, the lifeline** |
| G | `eco.py` | `_sync_harvesters` | the honest-slot reset, **shipped OFF** |

### 1.1 Why the famine bits ride an existing write

`read_store` returns the **pre-round** value. A second Core write to
`FS_ECO_SLOT` in the same turn would read a stale word and silently drop the
first — the r197 lost-update defect, same shape. So the famine bits are
computed inside `_fs_eco_publish` and land in its one write. The only cost is
that the `if conn and deliv: return` early-return can no longer fire while the
plank is on: the detector needs `held` every round, and `held` is exactly what
that return was skipping. **Flag off, the return is byte-identical.**

### 1.2 The three rungs and their bounds

**RUNG A — LIFELINE (fixes funding).** While a famine episode is young, an
**expander's** eco spend is exempt from the collar and siege reserves — the
same `essential` waiver v513 change C already grants the last link, for the
same reason. Bounded three ways: **expanders only** (a raider's spending is
never waived), **the first `FS_V539_LIFELINE_RNDS = 40` rounds of an episode**,
and **at most `FS_V539_MAX_EPISODES = 3` episodes per match**. `ti >= cost`
still holds, so the waiver can only spend income the wipe left us — ~100 Ti
over a 40-round window at passive rates. *This bound is where §6's cost comes
from and it is the first knob a battery should move.*

**RUNG B — DRAFT (fixes roster).** A body whose role is being assigned **while
famine holds** takes `"expand"` instead of `"raid"`. It touches **no existing
raider**: a body already walking the enemy ring keeps its role, which is the
`T4_BLEED` lesson already written in this tree ("recalling the whole economy on
a latch once finished a measured game with 0 titanium delivered"). The draft
**releases itself** the round delivery resumes.

**RUNG C — SEAT-3 HOLD.** Seat 3's one-way defection to the raid reads
`SLOT_HARVESTERS >= ECO_NEED` **on the ratchet**, i.e. on harvesters that may
all be dead. It is **suspended** while famine holds. ⛔ It is **held, never
reversed**: on a gated map seat 3 is the ferry-siege support raider and pulling
a body out of a live crew mid-siege is a bigger change than this plank is
allowed to be.

**The rebuild itself is not re-derived (D21d).** With funding and an expander
in hand, the existing `_expand` bootstrap builds the harvester and
`_wire_on_build` / `_build_next_link` lay the chain, exactly as in the opening.
This plank buys those two preconditions and nothing else.

### 1.3 The cap, and why it is not a number somebody chose

**The episode ends when titanium is seen arriving at our own core again.**
Delivery is both the trigger and the stop condition, so the cap *is* the
definition of "the kill is funded again" — Magnus's minimum economy, in the
engine's own terms. `FS_V539_MAX_RNDS = 120` and `FS_V539_MAX_EPISODES = 3` are
backstops for a famine that cannot be fixed, not the rule.

### 1.4 The opening is untouched, twice over

Famine cannot be declared before `FS_V539_MIN_RND = 60`, **and** it cannot be
declared until the belt has delivered at least once. A bot that has not yet
delivered is in its opening, not in a famine. (OPENFAST, s49.)

---

## 2. THE DETECTOR

### 2.1 ⛔ Why a live-vs-slot head count was rejected

The commission asked the Core to compare a LIVE harvester count against the
slot. **No unit on this team can read that count honestly.**

* `_sync_harvesters` — the site that writes the ratchet — runs on **BUILDERS**
  (`main.py`, inside the builder turn), not the Core. Builder vision is
  r² = 20 and the sync only runs within d² ≤ 64 of the Core, so **any single
  body's count is a LOWER BOUND**.
* That is *why* the slot is a ratchet: it is a **UNION over partial views**.
  Replacing a union with one of its members produces a famine call every time a
  body walks home past ore it cannot see.
* ⛔ **And the commission's premise that "the Core is the ONE writer" of
  `SLOT_HARVESTERS` is false.** The v514 change-A single-writer comment
  attaches to **slot 5** (`SLOT_ECO_READY`), not slot 4. Slot 4 has **two**
  writers today, both builder-side: `eco.py:816` (the ratchet) and `eco.py:2488`
  (the `+1` on build). Making the Core a third writer would have created
  exactly the lost-update hazard the comment exists to prevent.

### 2.2 What is read instead

`_fs_eco_mouth()` (v514) already gives the Core a friendly conveyor/splitter on
one of our own eight delivery seats whose facing points into the core
footprint, and whether it is **HOLDING a stack**. The mouth is always inside
Core vision, so the read never degrades.

```
famine := FS_ECO_BIT_DELIV is latched            (we have delivered at least once)
          AND round >= FS_V539_MIN_RND           (60)
          AND no `held` sighting for FS_V539_DROUGHT rounds   (25)
```

A connected harvester puts a stack on the mouth one round in four, so a
25-round drought on a delivering belt has probability ~0; 25 also outlasts the
residual stacks in flight when the last harvester dies. **A cut belt, a dead
harvester set and a shot-off mouth all read the same because they ARE the
same** — to the bank, and to `titanium_collected` (CLAUDE.md's own engine
probe: a harvester with no route home collected 0 over 998 rounds).

Measured, `harness.py --selftest` §3–§5:

| cell | result |
|---|---|
| wipe at r120, drought 25 | **declared r141** (= last stack r116 + 25) |
| belt never stops (control) | **never declared** |
| wipe at r5, `MIN_RND = 60` | **declared r60, never earlier** |
| `MIN_RND` pushed to 10⁶ (complement) | **never declared** |
| harvester restored at r200 | **famine CLEARED r200** |
| parent tree, same script | **never declared — it has no detector** |

---

## 3. THE CONSUMER TABLE (the commission's item (c))

Generated by `scratchpad/s52_v539_build/consumers.py` (selftest passes, incl. a
mutation test that renaming the slot yields 0 sites). **13 sites in the parent,
15 in v539** — the two added sites are the `live <` test and the `write` of the
flagged-off honest reset, and nothing else.

Two columns matter: what each site does under the **phantom** ratchet (today,
and in v539 as shipped, since v539 does **not** reset the slot), and what it
would do under an **honest 0** (`FS_V539_HONEST_SLOT = True`).

| # | site | test | under PHANTOM (shipped) | under HONEST 0 (flag on) |
|---|---|---|---|---|
| 1 | `eco.py:816/817` | `live > slot` → write | ratchet rises only | unchanged |
| 2 | `eco.py:819/832` | **v539 only**, `live < slot` and famine | **inert (flag off)** | ratchet falls to `live` |
| 3 | `eco.py:2261` | `>= 1` — opportunistic **pave** | **OPEN**: paving allowed | **CLOSES** — cannot pave while rebuilding |
| 4 | `eco.py:2423` | `harv = …` → `allow_pave = launcher or harv >= 2` | **OPEN** | **CLOSES** (hand-annotated: read here, tested next line) |
| 5 | `eco.py:2488/2490` | `+1` on build; `>= ECO_NEED` → `SLOT_ECO_READY` | suppressed under v514 | unchanged |
| 6 | `main.py:455` | `harv = …` → fed to `_fs_eco_publish` | sets CONN bit; **latches, never clears** | CONN may fail to latch on a *first* connection during famine |
| 7 | `main.py:1459` | `>= ECO_NEED` — **seat 3 defects to raid** | **the one harmful phantom**; v539 **holds it shut** (rung C) | would close on its own, but only after the defection already happened |
| 8 | `main.py:1874` | `< ECO_NEED` — counterbattery refusal | **PERMISSIVE**: phantom ≥3 skips the refusal | **CLOSES** counterbattery unless the Core is provably shelled |
| 9 | `main.py:1967` | `< 1` — home **LAUNCHER** | **OPEN** | **CLOSES** the home launcher and the ferry |
| 10 | `raid.py:714` | `< min_harv` (=2) — forward **SENTINEL** | **OPEN** | ⛔ **CLOSES THE SENTINEL GATE** |
| 11 | `raid.py:916` | `< LOKI_BELTBREAK_MIN_HARV` — beltbreak gunner | **OPEN** | **CLOSES** |
| 12 | `siege.py:4452` | `harv` → evictor recovery arithmetic | phantom **raises** assumed income, **lowers** the reserve floor | raises the floor: evictor launcher harder to fund |

**Read the right-hand column as a whole: of the nine gates the reset touches,
eight CLOSE and none opens.** That is the §1 top-line finding and the reason
`FS_V539_HONEST_SLOT` ships `False`.

### 3.1 The sentinel gate specifically (amendment item 3) — MEASURED

`_fs_eco_gate_ok` does **not** read `SLOT_HARVESTERS` directly. It reads the
CONN and DELIV bits of `FS_ECO_SLOT`, and CONN is set from
`harv >= FS_SENT_HARV_MIN` — i.e. from the ratchet — **and then LATCHES**
(`if conn and deliv: return`). Driven on the real code (`--selftest` §9):

| | value |
|---|---|
| gate before the wipe | **OPEN** |
| famine declared at r199 | **yes** (the dose landed) |
| gate during famine | **STILL OPEN** |
| CONN and DELIV bits during famine | **both still set**, alongside the famine bit |

⇒ **The famine reset as shipped does not close the sentinel gate**, because the
famine bits only ever touch bits 18 and 19–29 and the gate reads bits 0–1,
which are write-once. **This is correct under Magnus's s51 ruling and it is the
answer to the amendment's question:** the gate says "two harvesters were built
and the belt was demonstrably delivering", which remains a true historical
fact after a wipe; what a wipe removes is the *funding*, and funding is checked
separately at every purchase site. **A gate closed with no funding behind it
would be honest but useless** — it would refuse the sentinel twice for one
reason.

---

## 4. THE FAMINE HARNESS

`scratchpad/s52_v539_build/harness.py`, `agg.py`, `consumers.py` — all three
carry `--selftest` and all three drive **every guard to both verdicts**.
Outputs: `OUT_selftest_*.txt`, `OUT_endgame_run{1,2}.tsv`,
`OUT_agg_run{1,2}.txt`, `OUT_identity.txt`, `OUT_consumers_*.txt`.

**THE FIXTURE.** Our Core, our builders, real terrain from a pool map, **no
opponent**. At the wipe round every friendly HARVESTER / CONVEYOR / SPLITTER is
removed, the bank is cut to **5 Ti** and `SLOT_UNDER` is re-latched every round
for 60 rounds — the measured v174 board (`harvesters 0 / Ti 5 at r154`, under
sustained attack), which is what an economy attack looks like to
`_eco_spendable`. Both arms get the identical script.

### 4.1 ⛔ Three false starts, all of which would have read as clean nulls

Written down because each failed in the flattering direction and each was
caught only by a complement cell:

1. **The fcode type shim.** The trees do `from fcode import …`;
   `tools/stub_engine.py` uses its own shims and
   `fcode.EntityType.CONVEYOR == "conveyor"` is **False**. Unshimmed,
   `_dispatch` matched neither CORE nor BUILDER_BOT, `run()` did nothing, and
   **two selftest cells passed vacuously** off whatever `__init__` had left on
   the object.
2. **Position methods.** Both Positions are `(x, y)` NamedTuples so they
   compare and hash equal — which is why this was missed. What differs is that
   a stub Position's `.cardinal_direction_to()` returns a **stub** Direction and
   `eco.py`'s `DELTA` dict is keyed on **fcode** Directions, so the bot raised
   `KeyError` inside `_move`, caught it in its own top-level handler, and
   degraded silently. **A harness whose bot cannot move would have reported "0
   rebuilds" for both arms.**
3. ⭐ **NOISE_ON made the fixture non-deterministic.** `main.py` seeds a
   per-body `spawn_salt` from `random.Random()` — a fresh generator with no
   seed, which `random.seed()` cannot reach. **The same tree run twice in one
   process diverged at round 2**, and the first atoll cell read `parent 280 /
   v539 162` on one invocation and `parent 276 / v539 280` on the next: **the
   headline result reversed on noise alone.** Fixed by forcing `NOISE_ON =
   False` in every module (each has its own binding via `import *`), and proved
   by a **self-vs-self control**: parent vs parent, 5 maps, **identical on all
   5**. *That control is now the first thing the identity battery runs.*
   Consequently the scenario axis is the **wipe round**, not a random seed — a
   re-seeded rerun of a deterministic fixture is a copy, not a sample.

### 4.2 The famine table — 25 paired cells, run 1

`--maps atoll,eider,heart,nordkap,drakkarfjord --rounds 340 --wipe-at
100,130,160,190,220`. Cells are `first_rebuild_round / mouth_alive_rounds /
delivery_sightings`, all counted after the wipe. `-1` = never.

| map | wipe | `_v537socket` | `_v539resilience` |
|---|---|---|---|
| atoll | 100 | 252/85/22 | **132**/202/51 |
| atoll | 130 | 264/73/19 | **154**/183/46 |
| atoll | 160 | 288/49/13 | 288/49/13 *(tie)* |
| atoll | 190 | **-1/0/0** | **224**/112/28 |
| atoll | 220 | **-1/0/0** | **242**/92/23 |
| drakkarfjord | 100 | 302/198/10 | 302/216/10 |
| drakkarfjord | 130 | 314/186/7 | 314/186/7 *(tie)* |
| drakkarfjord | 160 | 271/110/18 | 271/138/18 |
| drakkarfjord | 190 | 273/114/17 | **241**/116/25 |
| drakkarfjord | 220 | 301/**0/0** | **243**/80/20 |
| eider | 100 | 268/65/17 | **122**/212/53 |
| eider | 130 | 248/87/22 | **188**/140/35 |
| eider | 160 | 260/73/19 | **192**/136/34 |
| eider | 190 | 272/63/16 | **214**/119/30 |
| eider | 220 | 276/57/15 | **242**/88/22 |
| heart | 100 | 128/184/46 | **124**/188/47 |
| heart | 130 | 160/150/38 | **154**/156/39 |
| heart | 160 | 192/118/30 | **184**/124/31 |
| heart | 190 | 220/104/26 | **214**/**58/15** ⚠ |
| heart | 220 | 252/26/7 | **244**/26/7 |
| nordkap | 100 | 232/103/26 | **122**/212/53 |
| nordkap | 130 | 220/115/29 | **188**/144/36 |
| nordkap | 160 | 224/111/28 | **192**/140/35 |
| nordkap | 190 | 240/95/24 | **214**/121/31 |
| nordkap | 220 | 272/116/17 | **244**/116/24 |

| metric | v539 better | parent better | tie |
|---|---|---|---|
| first rebuild round (lower) | **21** | **0** | 4 |
| mouth alive rounds (higher) | **20** | 1 | 4 |
| delivery sightings (higher) | **19** | 1 | 5 |
| harvesters built post-wipe | 3 | 0 | 22 |
| conveyors built post-wipe | 5 | 3 | 17 |
| **famine declared** | **25 / 25** | **0 / 25** | — |
| `run()` raised, both arms | **0** | **0** | — |

21 discordant cells all one way ⇒ sign test **p ≈ 1×10⁻⁶**. The one reverse
cell on `mouth`/`deliv` is **heart wipe@190** and it is left in the table.

### 4.3 The replicate — 25 more cells, fresh process, different wipe rounds

`--wipe-at 110,140,170,200,230`: **first rebuild 20 v 0 (5 ties) · mouth 22 v 0
(3) · delivery 20 v 0 (5) · famine 25/25 v 0/25 · raised 0.**

### 4.4 The counter-control, honestly

The commission expected the parent to reproduce the 2026-08-07 decode's **0
rebuilds**. **It does not.** Pooling both runs (50 paired cells):

| | parent | v539 |
|---|---|---|
| never rebuilt at all | **4 / 50** | **0 / 50** |
| core mouth never alive again post-wipe | **7 / 50** | **0 / 50** |
| rebuild delay vs the other arm (n = 46 both-rebuilt cells) | — | **median 29 rounds earlier, mean 38.9, max 146, min 0** |

Note the second row is the harder one: drakkarfjord @220 shows a parent
`first_rebuild = 301` with `mouth = 0 / deliv = 0` — a harvester **built with
no route home**, which is `titanium_collected = 0` by CLAUDE.md's own engine
probe. A rebuild counter alone would have scored that as a success for the
parent. **The claim this build supports is TEMPO plus the elimination of the
never-delivers tail; it is not "the parent cannot rebuild".**

---

## 5. FLAG-OFF AND INERTNESS — four batteries, and the one that must FAIL

`OUT_identity.txt`, NOISE_OFF, 5 maps, 340 rounds, per-round fingerprint of
every entity (id, type, position, hp, both cooldowns, facing) plus the whole
16-slot store, the bank and the ammo.

| battery | expectation | result |
|---|---|---|
| **A** parent vs parent, wipe@140 | identical | **identical 5/5** |
| **B** `LOKI_FS_V539 = False` arm vs parent, wipe@140 | identical | **identical 5/5** |
| **C** flag ON vs parent, **no wipe** | identical (the path is inert) | **identical 5/5** |
| **D** flag ON vs parent, wipe@140 | **must DIVERGE**, or A–C mean nothing | **diverges 5/5, at round 161 on every map** |

**Battery D's divergence round is the famine declaration round on all five
maps.** The first behavioural difference between v539 and its parent is
literally the moment famine is declared, and there is none before it.

The flag-off arm is `scratchpad/s52_v539_build/arms/v539flagoff` — a byte copy
of the shipped tree with the single line `LOKI_FS_V539 = False`. Every new name
is read inside the branch it guards (the v524/v528/v534/v537 convention), which
is what battery B measures rather than asserts.

---

## 6. ⭐⭐ THE SURPRISE — v539 SPENDS ITS WAY OUT OF THE SENTINEL BAR

Magnus's amendment asks for **kill terms**. The fixture has no opponent, so no
forward-sentinel purchase can fire and a turret count of 0 in both arms would
say nothing. What the fixture *can* answer is whether the bank ever recovers to
the level `main.py` actually checks before buying one:
`sentinel_cost + SIEGE_HEAL_RESERVE_TI` — **107 Ti** at the scale these games
reach. Counting post-wipe rounds spent at or above that bar:

| metric | v539 better | parent better | tie |
|---|---|---|---|
| **rounds the bank could afford a sentinel** | **0** | **16** | 9 |

Worked cells: atoll@100 parent 36 rounds v539 19 · nordkap@160 parent 75 v539
58 · drakkarfjord@220 parent 60 v539 30. And **atoll@190 the parent builds 3
post-wipe turrets to v539's 1**.

**This is the direct, mechanical consequence of rung A**, and it is the risk
the battery has to price: the lifeline exists to convert a stalled bank into
belt, so a bot that uses it necessarily sits above a bank threshold for fewer
rounds. The counter-argument — that restored delivery is *income*, and income
is what pays for the second and third sentinel — is **not demonstrated here**:
this fixture has 340 rounds, no opponent, and no reason for the bot to spend on
turrets. **It is stated as a hypothesis and it is exactly what
`DEFENCE_ADMISSION_BAR` will test.** No explanation is offered.

**The first knob to move if this bites:** `FS_V539_LIFELINE_RNDS` (40), or
ending the waiver as soon as a **mouth exists** (topology) rather than waiting
for the first delivery **sighting** — up to 4 rounds shorter, and a one-line
change.

---

## 7. ⛔ HONEST LIMITS

* **THIS PLANK HOLDS THE LINE SO THE KILL LANDS.** It is admissible only under
  `PLAY_DEFENCE: not_at_the_kill_s_expense` and it must clear
  `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression` — the share of ALL its
  games ending in a core-kill **by r300** must not fall against control. **Its
  battery will be scored that way and §6 is a live reason it might fail.**
  Nothing in this report claims it passes.
* **THE FIXTURE HAS NO OPPONENT.** Every number here is a branch-taken count,
  not a game. No win rate, no kill round, no Elo, no CPU claim.
* **THE STUB'S CORE IS ONE TILE, NOT 2×2**, and the stub has **no
  resource-stack physics** — delivery is scripted on the engine's 4-round
  cadence. The detector reads exactly that scripted channel, so the model *is*
  the fixture for this plank and would not be for any other.
* **`titanium_collected` IS OFF-CURRENCY.** Delivery numbers here are the
  mechanism, not the score (`R1000_IS_DEFEAT`). They matter because delivery
  buys the sentinel, and for no other reason.
* **THE DETECTOR CAN FALSE-POSITIVE** on a belt whose mouth is alive but which
  our Core cannot see holding a stack for 25 straight rounds. The cost is
  bounded (one 40-round waiver, drafted bodies that release themselves) and
  self-correcting, but it is not zero and it was not measured against a
  deliberately adversarial delivery pattern.
* **RUNG C HOLDS, IT DOES NOT REVERSE.** A seat-3 body that already defected
  before the famine stays a raider for the rest of the match.
* **THE PARENT IS A FORK** — see §0.

---

## 8. DEFERRED, AND NAMED (the B3 precedent)

**The tree may not enter any battery until items 1–2 exist.**

1. **A LIVE-ENGINE DOSE.** Zero `fcode` runs were made: V537POOL held **2,461
   of 5,400 rows at `07:54:41Z`**. The dose needed is an engine leg in which our
   economy is actually destroyed by an opponent, with the famine declaration
   read off **engine-side facts** (harvester entity removals, conveyor removals,
   post-wipe harvester builds) — **never off our own stderr**, which platform
   replays strip (CLAUDE.md s28: 30,664 of 30,664 `BotOutput` events empty).
   Local only, after the pool completes, because the `V539` tape is stderr.
2. **THE `r300` NON-REGRESSION SCREEN**, against the head of the line (not
   v537), with the timely-kill rate as primary. §6 says which way it might go.
3. **A LEG FOR `FS_V539_HONEST_SLOT`.** Built, off, and §3 predicts it closes
   eight gates and opens none. That prediction is falsifiable and cheap.
4. **THE RE-MERGE ONTO HEAD** (§0).
5. **AN ADVERSARIAL DELIVERY PATTERN** for the detector's false-positive rate
   (§7) — e.g. a belt kept alive but starved, which should *not* declare.
6. **THE LIFELINE-LENGTH SWEEP** (§6): `FS_V539_LIFELINE_RNDS` and the
   mouth-exists-vs-delivery-seen stop condition.
