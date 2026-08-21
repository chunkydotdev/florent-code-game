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

---

## 9. REEL — WHAT TO WATCH, AND WHAT THERE IS TO WATCH IT WITH

⛔ **THERE ARE NO REPLAYS. THE REEL IS A RE-RUN RECIPE, AND THAT IS A LIMIT, NOT
A STYLE CHOICE.** This build made **zero `fcode` runs** (§7), so there is no
`.replay` for any cell below. What exists is the fake-engine tape plus a
deterministic recipe that regenerates it byte-for-byte on demand — the fixture
is NOISE_OFF and was proved deterministic by a parent-vs-parent self control
(§4.1). Every recipe below was **re-executed at `08:01:38Z` and reproduced its
cell exactly**; that check is the reel's substitute for pressing play.

**When the live dose in §8.1 lands, THAT is the real reel and it replaces this
section.** Until then, a reader who wants to see the plank work runs these.

### 9.1 The three cells worth watching, in order

**REEL 1 — ⭐⭐ THE SURPRISE CELL: `atoll`, wipe @ r190.** *This is the one to
watch first, because it is the cell that argues against the plank as much as
for it.*

```
.venv/bin/python scratchpad/s52_v539_build/harness.py \
    --endgame --maps atoll --rounds 340 --wipe-at 190
```

| | `_v537socket` | `_v539resilience` |
|---|---|---|
| first rebuild | **never (-1)** | **r224** |
| famine declared | — (no detector) | **r213** |
| core mouth alive, post-wipe rounds | **0** | **112** |
| delivery sightings | **0** | **28** |
| ⚠ rounds bank ≥ sentinel bar (107 Ti) | **27** | **19** |
| ⚠ turrets built post-wipe | **3** | **1** |
| bank at end | 92 | 114 |

**Read both halves.** The parent's economy is dead for the rest of the game —
mouth 0, delivery 0, no rebuild ever — and it converts that into **three
turrets** off a bank nothing is drawing down. v539 re-establishes delivery 11
rounds after declaring famine and buys **one**. **That trade is the whole
`DEFENCE_ADMISSION_BAR` question in a single cell** and the fixture cannot
settle it, because it contains no opponent for either turret to shoot.

**REEL 2 — THE CLEAN MECHANISM CELL: `atoll`, wipe @ r100.**

```
.venv/bin/python scratchpad/s52_v539_build/harness.py \
    --endgame --maps atoll --rounds 340 --wipe-at 100
```
Parent `252/85/22` vs v539 `132/202/51` (rebuild round / mouth-alive rounds /
delivery sightings). **120 rounds of tempo, and the belt alive for 202 rounds
against 85.** This is what the plank looks like when nothing argues back.

**REEL 3 — THE ONE REVERSE CELL, LEFT IN: `heart`, wipe @ r190.**

```
.venv/bin/python scratchpad/s52_v539_build/harness.py \
    --endgame --maps heart --rounds 340 --wipe-at 190
```
v539 rebuilds earlier (r214 vs r220) and then holds the mouth for **fewer**
rounds (58 vs 104) with fewer deliveries (15 vs 26) — the only cell in 50 where
the belt metric goes the wrong way. **No explanation is offered.** It is the
first cell to look at if the live dose disappoints.

### 9.2 The divergence reel — where the two bots first differ

```
.venv/bin/python - <<'EOF'
import sys; sys.path.insert(0, "scratchpad/s52_v539_build")
from harness import identity_cmp
for m in ("atoll", "eider", "heart", "nordkap", "drakkarfjord"):
    print(identity_cmp(m, 340, 140, a="_v537socket", b="_v539resilience"))
EOF
```
**Every map: `first_divergence = 161`** — the famine declaration round. There is
no behavioural difference of any kind before it. Swap `b=` for
`scratchpad/s52_v539_build/arms/v539flagoff` and every line reads
`identical: True`.

### 9.3 The full batteries

```
# 25 paired cells, run 1 (the §4.2 table)
.venv/bin/python scratchpad/s52_v539_build/harness.py --endgame \
  --maps atoll,eider,heart,nordkap,drakkarfjord --rounds 340 \
  --wipe-at 100,130,160,190,220 > OUT_endgame_run1.tsv
.venv/bin/python scratchpad/s52_v539_build/agg.py OUT_endgame_run1.tsv

# the replicate (§4.3): identical command, --wipe-at 110,140,170,200,230
# the THREE-ARM run incl. v539.1 (§11.2):
.venv/bin/python scratchpad/s52_v539_build/harness.py --endgame \
  --maps atoll,eider,heart,nordkap,drakkarfjord --rounds 340 \
  --wipe-at 100,130,160,190,220 \
  --arms _v537socket,_v539resilience,scratchpad/s52_v539_build/arms/v539_1_floor
# the consumer table (§3):
.venv/bin/python scratchpad/s52_v539_build/consumers.py _v539resilience
# every instrument, both verdicts per guard:
.venv/bin/python scratchpad/s52_v539_build/harness.py   --selftest
.venv/bin/python scratchpad/s52_v539_build/agg.py       --selftest
.venv/bin/python scratchpad/s52_v539_build/consumers.py --selftest
```

⚠ **`agg.py` output is PAIRED-ONLY for a reason** (§4.1): absolute cells are
comparable **within** one harness invocation and **not across** invocations,
because `fcode`'s enums hash by identity. Compare two runs as replicates; never
subtract their absolute numbers.

---

## 10. MANIFEST

Everything this build wrote, with the md5 it was committed at. Disk verified at
`08:01:09Z`: **82 Gi free**, all paths present and readable, no mode-444 file
written or required (`bots/_v488beltbreak2` was never touched by this build).

### 10.1 Shipped tree — `bots/_v539resilience/` (`ARM_FREEZE.md5`)

| file | note |
|---|---|
| `doctrine.py` | + the LOKI-REESTABLISH block (§1) |
| `eco.py` | rung A (`_eco_spendable`), honest-slot branch (off) |
| `main.py` | rungs B and C, per-unit state |
| `siege.py` | detector + readers, folded into `_fs_eco_publish` |
| `raid.py` | **unchanged from the parent** |

Parent `bots/_v537socket` frozen `07:35:52Z` (`PARENT_FREEZE.md5`) and
**re-verified byte-identical** `07:54:41Z` (`PARENT_REFREEZE.md5`) — the two
files `diff` clean.

### 10.2 ⛔ THE FIRST VERSION OF THIS TABLE CERTIFIED THE WRONG FILES

The md5 table committed at `08:02:52Z` was **misaligned**: it was built by
`paste`-ing `md5 -q` output (argument order) against `ls` output (sort order),
so every hash sat beside the wrong filename — `harness.py` was credited with
`OUT_consumers_parent.txt`'s hash, and so on down the list. **A manifest that
certifies the wrong artefact is worse than no manifest**, because it reads as a
check that passed. Caught at `08:07:5xZ` by regenerating with `md5` (which
prints its own filenames) rather than `md5 -q`. The table below is that output,
verbatim, and **the rule taken from it: never pair hashes and names from two
separately-ordered commands.**

### 10.3 Instruments — all three carry `--selftest`, all drive every guard both ways

| file | md5 | what |
|---|---|---|
| `scratchpad/s52_v539_build/harness.py` | `050e059e9801d865bfe6b50bde4ebbc0` | fake-engine famine harness: detector / gate / floor-sweep / endgame / identity |
| `scratchpad/s52_v539_build/agg.py` | `d042a53a27ff8fe9e44cc726edb42144` | paired aggregator + sign test |
| `scratchpad/s52_v539_build/consumers.py` | `64953ea895cd00096c54ffc5059d7443` | `SLOT_HARVESTERS` site enumeration (§3) |

### 10.3.1 Tapes

| file | md5 | contents |
|---|---|---|
| `OUT_endgame_run1.tsv` | `fb036cdb7e3acfb70cb3c079b6ec6118` | 25 paired cells, wipes 100–220 (§4.2) |
| `OUT_endgame_run2.tsv` | `cee771497a4e124c365ec2c19a6cfac2` | the replicate, wipes 110–230 (§4.3) |
| `OUT_endgame_run3_threearm.tsv` | `2a8bc8803b8a1bb04fe49fc651812462` | **three-arm run incl. v539.1 (§11)** |
| `OUT_agg_run1.txt` | `030773146d59b1145aea6787ecdd8e3a` | §4.2 table + sign tests |
| `OUT_agg_run2.txt` | `14a38f39dd047ee13a2c4e67c8e7d7fd` | §4.3 |
| `OUT_identity.txt` | `09a235410967a712da1383fe2247e027` | **six identity batteries, re-run on FINAL bytes (§5, §11.3)** |
| `OUT_floor_sweep.txt` | `ac17551cab5c1d392ead1381e92f9964` | **the v539.1 four-way bank sweep (§11.2)** |
| `OUT_consumers_parent.txt` | `c025ca04607e5a39992029fdefcedfb5` | 13 sites |
| `OUT_consumers_v539.txt` | `e8eb0a6c015703353cb7ca533124851a` | 15 sites |
| `OUT_selftest_harness.txt` | `30527489a869607e502fe9f27a557eaf` | 11 groups, all pass |
| `OUT_selftest_agg.txt` | `e61c32ba97465535f0e8422f8954ec55` | 4 groups, all pass |
| `OUT_selftest_consumers.txt` | `6d3d35c8dbf0b9cc382fd0cbc5f3e361` | 4 groups, all pass |
| `OUT_endgame.txt` | `0c94bef8d75ef8f41f0a02853aa2a116` | ⛔ **SUPERSEDED — the pre-NOISE_OFF run.** Kept because §4.1's non-determinism finding is read off it. **Do not quote its numbers.** |
| `ARM_FREEZE.md5` | `c8a68e3a1e7bbdb8f2d5d97a5d65782e` | the shipped tree's per-file hashes, final bytes |
| `PARENT_FREEZE.md5` / `PARENT_REFREEZE.md5` | both `60ab7e173e739bba1247901ef792dbd5` | parent byte-unchanged across the whole build |

### 10.3.2 Arms

| arm | one line changed | purpose |
|---|---|---|
| `arms/v539flagoff/` | `LOKI_FS_V539 = False` | flag-off identity (§5 B) |
| `arms/v539_1_floor/` | `FS_V539_RESERVE_FLOOR = True` | **the v539.1 conservative arm (§11)** |

Both are byte copies of the **final** shipped tree, rebuilt at `08:06:16Z`
after the last code change, and both compile.

### 10.4 What was NOT produced, and why

* **No `.replay`, no platform tape, no Elo row.** Zero `fcode` runs; V537POOL
  held **2,461 of 5,400 rows at `07:54:41Z`**, **2,674 at `08:01:09Z`** and
  **2,897 at `08:08:04Z`** — all three under the gate.
* **No stderr tape.** `FS_V539_LOG` ships `False`, and platform replays strip
  stdout regardless (CLAUDE.md s28). The `V539 DECLARE/CLEAR` lines exist for a
  **local** dose only and §8.1 says so.
* **No CPU measurement.** The plank makes the Core poll `_fs_eco_mouth` every
  round instead of stopping at the v514 latch (§1.1). That is a real per-round
  cost on one unit with a 10 ms budget and **it is unmeasured**; add it to the
  live dose.

---

## 11. v539.1 — THE RESERVE-FLOOR ARM, AND WHAT IT TURNED OUT TO BE

Accepted from the side-lane audit: §6's surprise (the parent ahead 16-to-0 on
post-wipe sentinel-affordable rounds) is a `DEFENCE_ADMISSION`-shaped risk — the
plank buying economy with the kill budget — and the battery will want both arms
rather than an argument. **Built, unit-verified both ways, shipped OFF.**

**THE RULE.** Under `FS_V539_RESERVE_FLOOR`, rung A's waiver additionally
requires `bank − cost >= sentinel_cost + SIEGE_HEAL_RESERVE_TI` — the literal
bar `main.py` checks before buying a sentinel. **The rebuild waits rather than
raiding the kill budget.**

### 11.1 ⭐⭐ THE SURPRISE: THE FLOOR MAKES RUNG A EXACTLY INERT

Written before it is explained. A four-way sweep — **17 bank levels ×
{conveyor, harvester} cost × {collar live, collar idle} = 68 cells**
(`OUT_floor_sweep.txt`, `harness.py --selftest` §9):

| arm | cells differing from the PARENT's `_eco_spendable` verdict |
|---|---|
| floor **ON** | **0 of 68** |
| floor **OFF** (shipped v539) | conveyor/idle `[4, 8, 16]` · conveyor/collar `[4, 8, 16]` · harvester/idle `[24, 32]` · **harvester/collar `[24, 32, 40, 44, 46, 48, 52, 60]`** |

**The region where rung A matters is exactly the region the floor forbids**, so
the floor does not soften the lifeline — it deletes it. ⇒ **v539.1 is a clean
ABLATION of rung A: draft + seat-3 hold, no funding waiver.** That is a more
useful arm than the one requested, and it is not what the design intended.

⛔ **The first version of this check asserted the opposite** ("the arm acts, it
is not a no-op", tested under a live collar) and **failed**. It is recorded here
rather than deleted: the collar reserve is clamped by `FS_ECO_LIFELINE`, so it
almost never pushes the parent below its own bar for a cheap link.

### 11.2 What the ablation costs, measured

Three-arm endgame, final bytes, 25 paired (map, wipe) cells
(`OUT_endgame_run3_threearm.tsv`), each arm scored against the parent:

| metric | v539 (shipped) W/L/T | **v539.1 (floor) W/L/T** |
|---|---|---|
| first rebuild round | **21 / 0 / 4** | **0 / 0 / 25** |
| mouth alive rounds | **20 / 1 / 4** | **0 / 0 / 25** |
| delivery sightings | **19 / 1 / 5** | **0 / 0 / 25** |
| rounds bank ≥ sentinel bar | 0 / 16 / 9 | **0 / 0 / 25** |
| turrets built post-wipe | 0 / 2 / 23 | **0 / 0 / 25** |
| famine declared | 25 / 25 | **25 / 25** |
| `run()` raised (all 3 arms) | — | **0** |

**v539.1 is outcome-identical to the parent on every counted metric in all 25
cells** — while still declaring famine 25/25 and still diverging from the parent
in state (§11.3). ⇒ **RUNG A IS THE WHOLE PLANK. Rungs B and C are necessary
scaffolding that accomplish nothing on their own**: a drafted body with no
funding walks to the ore and cannot buy the harvester.

⚠ **THE HONEST READING FOR THE BATTERY: on this fixture v539.1 neither costs
nor gains anything.** It is a null arm here. Only a live leg — with an opponent,
a real bank trajectory and turret purchases that actually matter — could
separate it from the parent. **Spending games on it is a decision to test
whether §6's cost is real, not to test the rebuild.**

### 11.3 Identity, re-proven on the FINAL bytes (`08:06:29Z`)

Re-run after the last code change, NOISE_OFF, 5 maps, 340 rounds:

| battery | expectation | result |
|---|---|---|
| **A** parent vs parent | identical | **5/5 identical** |
| **B** `LOKI_FS_V539 = False` vs parent | identical | **5/5 identical** |
| **C** flag ON vs parent, no wipe | identical | **5/5 identical** |
| **D** flag ON vs parent, wipe@140 | must diverge | **5/5 diverge, round 161 on every map** |
| **E** v539.1 vs shipped v539, wipe@140 | must diverge (rung A ablated) | **5/5 diverge: r162, r192, r164, r192, r163** |
| **F** v539.1 vs parent, wipe@140 | must diverge (B and C still act) | **5/5 diverge, round 161 on every map** |

**E's divergence rounds are the shipped arm's first-rebuild rounds** — the exact
place the ablated lifeline bites. **F proves v539.1 is not simply the parent
recompiled**, which is what makes §11.2's all-ties table a finding rather than a
tautology.

### 11.4 Added to the deferred list

7. **RUN v539.1 AS THE THIRD ARM** of the `r300` screen (§8.2). §11.2 predicts
   it reads as the parent; if it does not, the fixture is missing something the
   live game has.

---

## 12. ⛔ PROVENANCE DEFECT — THE v539.1 WORK IS COMMITTED UNDER ANOTHER LANE'S
MESSAGE

Recorded because a searchable record that points at the wrong commit is the
same failure class as §10.2's misaligned manifest: it reads as correct.

**WHAT HAPPENED.** At `08:09:46Z` this build ran `git add` on its three paths
and then, in the next shell call, `git commit`. Between the two, the **research
lane committed** — with no pathspec — and its commit took everything sitting in
the shared index. **All 19 v539 paths (the `FS_V539_RESERVE_FLOOR` code, both
arms, the refreshed tapes, §10.2's manifest fix and §11) are therefore recorded
inside `a03f63c32`, a RESEARCH two-loss-autopsy commit**, and this build's own
`git commit` then found nothing staged and exited without creating anything.

**NOTHING IS LOST AND NOTHING IS WRONG IN THE TREE.** Verified at `08:11:06Z`
against `HEAD`:

| check | result |
|---|---|
| all 19 v539 paths present in `a03f63c32` | **yes** |
| `bots/_v539resilience/doctrine.py` flags in HEAD | `LOKI_FS_V539 = True`, `FS_V539_REEST = True`, `FS_V539_RESERVE_FLOOR = False`, `FS_V539_HONEST_SLOT = False`, `FS_V539_LOG = False` — **all as intended** |
| `arms/v539_1_floor` in HEAD | `FS_V539_RESERVE_FLOOR = True` |
| `arms/v539flagoff` in HEAD | `LOKI_FS_V539 = False` |
| working tree vs HEAD, all three paths | **clean** |
| `harness.py --selftest` on HEAD bytes | **PASSED** |

**WHAT IS ACTUALLY DAMAGED IS SEARCHABILITY.** `git log --grep RESERVE_FLOOR`
and `git log --oneline -- bots/_v539resilience` both point a reader at a
research autopsy about `kladde` and `frostgate`. **This section is the index
entry that commit should have carried**, and §11 is the content.

**THE HISTORY IS NOT REWRITTEN.** `a03f63c32` is pushed and other lanes have it;
rewriting shared history to fix an attribution would trade a labelling defect
for a real one.

**THE RULE TAKEN, and it is mechanical rather than a promise to be careful:**
with concurrent lanes on one working tree, **`git add` opens a window in which
another lane's `git commit` owns your work.** Use the **pathspec form** —
`git commit <paths> -m …`, which commits those paths' working-tree state and
never touches the shared index — for every multi-lane commit. *This section is
committed that way.*
