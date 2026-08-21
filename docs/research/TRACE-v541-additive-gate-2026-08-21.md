# TRACE — WHICH GATE SILENCED v541's ADDITIVE CORE-PECK IN THE KLADDEDOSE LEG

**Lane:** research/trace agent, commissioned off **QUEUE #109**. **Opened**
2026-08-21T13:38:39Z, **closed** 2026-08-21T13:46:48Z, repo HEAD `c7439ab9f`.
**Zero platform matches fired** — in the event, none was needed.

**Subject:** `bots/_v542wave` = the shipped **v177 "Baltsars banditer v2"** (activated
2026-08-21T12:26:39.942Z; maiden pairing 12:31:10.314Z carries `ourver=177` —
`docs/coordination.md:72099`, `:72206`). **The tree is byte-clean at HEAD**:
`git status --porcelain bots/_v542wave` is empty and the only commit touching that
directory is `28fde0637` (2026-08-21T09:50:29Z), i.e. before the 12:26 activation.
`tools/submit_clean.py` stages `*.py` only and appends no overrides, so
**`doctrine.py` as read below is the doctrine the platform ran.** MEASURED.

**This document is a CLAIM, not a verdict.** Every line is labelled **MEASURED**
(read off the shipped bytes, driven in the harness, or decoded off the leg's replays),
**BOUNDED** (constrained, not pinned), or **INFERENCE**.

---

## 0. HEADLINE

**MEASURED — THE BINDING TERM IS NONE OF THE THREE CANDIDATES THE ROW NAMES. IT IS THE
MASTER FLAG ON THE FUNCTION ITSELF.**

`_v541_core_attack` (`bots/_v542wave/siege.py:4542`) opens its body with

```python
4567        if not (FS_V541_COREPECK and FS_V541_IDLEPECK):
4568            return False
```

and **`FS_V541_IDLEPECK = False`** (`bots/_v542wave/doctrine.py:5937`). That is the
FIRST executable statement, ahead of the target lookup (`:4569`), ahead of
`FS_V541_NEED_SENTINEL` (`:4572`), ahead of `_v541_funded` (`:4578`) — which is where
**both** the ammunition clause and the collar/sentinel reserve live. **In the shipped
configuration the additive path returns `False` unconditionally, on every call, in every
game state.**

⇒ **The row's candidates (a) `FS_V541_AMMO_AWARE` and (c) `FS_V541_TI_FLOOR` /
`FS_V541_KEEP_SENT` WERE NEVER EXECUTED ON THE ADDITIVE PATH — not once, in any of the
25 leg games.** This is not an estimate: `_v541_funded` (siege.py:4334), the function
that contains the ammunition clause, has **exactly one caller in the whole tree**
(`siege.py:4578`), and that caller sits downstream of the `return False` above.
MEASURED by static reachability (`grep -n "_v541_funded" bots/_v542wave/*.py`).

Candidate (b), the idle predicate, **is evaluated** at the two siege call sites — it is
the left operand of the `and` at `siege.py:3711` and `:3786` — but **its verdict is
discarded**: whichever way it goes, `_v541_core_attack` refuses. On the raid call site
(`raid.py:478`) it is not even reached: `FS_V541_IDLEPECK` is tested *before*
`_salt_idle_ok` in that conjunct.

### Refusal coverage of the exposure (4,171 (round, adjacent-body) cells; §3)

| clause | anchor | executions | refusals | **coverage** | label |
|---|---|---|---|---|---|
| **`FS_V541_IDLEPECK` master gate** | siege.py:4567 / doctrine.py:5937 | every call | every call | **100%** | MEASURED |
| ammunition clause | siege.py:4360-4361 | **0** | 0 | **0%** | MEASURED |
| collar + `TI_FLOOR` + `KEEP_SENT` reserve | siege.py:4385-4391 | **0** | 0 | **0%** | MEASURED |
| idle predicate `_v541_idle_ok` | siege.py:4265 | evaluated | not load-bearing | **0%** | MEASURED |

### Fix shape

**FIXABLE BY A CONSTANT — `FS_V541_IDLEPECK = False → True`, one line,
`doctrine.py:5937`.** No code change, no new predicate, no new state. But read §5:
the constant was shipped `False` **deliberately, with a written argument**, and the
KLADDEDOSE leg did not test that argument. **Flipping it re-opens a road the build's own
author closed on doctrine, not a road the leg closed on data** — and §4 shows the
counterfactual is live, so the flip is a real treatment with a real cost, not a bug fix.

### And the leg's 0/1,969 is not explained by the additive path at all

The additive path was inert. The observable — **1,969 of our builder attacks, 1,917 into
enemy conveyors, 0 into any core** (`DECODE-kladdedose-leg-2026-08-21.md` §1) — is
produced by the **other** half, the REDIRECT, whose binding term is `_v541_finishable`.
See §2 (P4) and §6.

---

## 1. THE COMPLETE ENUMERATION: every path from "our builder is orthogonally adjacent to an enemy-core tile" to "an attack lands on that core"

MEASURED — from `grep -n "ct\.fire(" bots/_v542wave/*.py` (13 sites), each opened and
classified. Turret-fire sites in `main.py` (`:1784`, `:1860`, `:2234`, `:2278`, `:2301`,
`:2386`) and the raid/siege turret sites are not builder melee and are excluded with that
reason; the seven remaining builder-melee paths are:

| # | path | fire anchor | governing conjuncts | shipped verdict |
|---|---|---|---|---|
| **P1** | raid clause 1, "standing on a seat: peck the Core" | `raid.py:298` | `on_seat and ti >= LOKI_PECK_TI_FLOOR and not LOKI_QUIET_ON` (`raid.py:292`) | **DEAD** — `LOKI_QUIET_ON = True` (`doctrine.py:1687`) |
| **P2** | `_raid_peck`, whose priority table ranks `EntityType.CORE` at `pr = 0` | `raid.py:759` (table `:737-750`) | `ti >= LOKI_PECK_TI_FLOOR and not LOKI_QUIET_ON` (`raid.py:388`) | **DEAD** — same flag |
| **P3** | `_fs_try_peck` (siege layer's core peck) | `siege.py:4235` | `if LOKI_QUIET_ON: return False` (`siege.py:4223`) | **DEAD** — same flag |
| **P4** | **v541 REDIRECT** `_v541_corefirst` | `siege.py:4416` via `:4477` | `FS_V541_COREPECK and FS_V541_RAID_ON` (`raid.py:421`) → `FS_V541_COREPECK and FS_V541_COREFIRST` (`:4468`) → `_v541_core_target is not None` (`:4470`) → **`_v541_finishable`** (`:4473`) → `_v541_funded_build` (`:4475`) → `_v541_fire` (`:4477`) | **LIVE, and it refused on `_v541_finishable` in 25/25 games** — §6 |
| **P5** | **v541 ADDITIVE** `_v541_core_attack`, 3 call sites | `siege.py:4416` via `:4580` | **`FS_V541_COREPECK and FS_V541_IDLEPECK` (`:4567`)** → target (`:4569`) → `FS_V541_NEED_SENTINEL` (`:4572`) → `_v541_funded` (`:4578`, = ammo clause + reserve) → `_v541_fire` (`:4580`) | **DEAD at the first conjunct** — `FS_V541_IDLEPECK = False` |
| **P6** | `_fs_try_clear` (collar seat clearing) | `siege.py:4212` | iterates `needed`, the collar's ring seats (`:4197`) | **cannot reach a core** — the ring is disjoint from the 2×2 footprint by construction |
| **P7** | eco siphon melee | `eco.py:2452` | `if LOKI_QUIET_ON: return False` (`eco.py:2449`) | **DEAD** — same flag, and it targets belts |

**P5's three call sites, in full:**

```
siege.py:3711   if FS_V541_COREPECK and self._v541_idle_ok(ct, E, p, needed) \
siege.py:3712           and self._v541_core_attack(ct, E, p, needed):      # sealer body, rung 5
siege.py:3786   if FS_V541_COREPECK and self._v541_supp_idle_ok(ct, E, p, needed) \
siege.py:3787           and self._v541_core_attack(ct, E, p, needed):      # support body, rung 5
raid.py:478     if FS_V541_COREPECK and FS_V541_RAID_ON and FS_V541_IDLEPECK \
raid.py:479             and self._salt_idle_ok(ct, E, p, near) \
raid.py:480             and self._v541_core_attack(ct, E, p, []):          # raid clause 8
```

**⇒ FS_V541_IDLEPECK=False kills ALL THREE**, and the raid site short-circuits on it
before `_salt_idle_ok` runs. The two siege sites evaluate their idle predicate first —
so `_v541_idle_ok`'s work is done and thrown away, which is exactly why the leg's
"consistent with the ammo clause/idle predicate holding it shut" reading was not
separable from the flag: **all three hypotheses predict the same zero, and only one of
them is executing.** MEASURED.

---

## 2. BOTH-WAYS DRIVE — every conjunct, refused and allowed

**Method declared:** UNIT-LEVEL drive of the shipped predicate functions with a mocked
`Controller`, **not** a full game. The functions come from the shipped modules
unmodified (`sys.path` → `bots/_v542wave`, `import siege`); the only mutation is to
module-level FLAG CONSTANTS, and in the "must allow" cells **that mutation IS the
treatment** — it is precisely what a fix would change. One input oracle is stubbed and
declared: `_fs_stand_target`, which is the INPUT to `_v541_idle_ok`, not part of the
clause under test.

Harness: **`scratchpad/s53_v541trace_harness.py`**. **39 cells, 0 mismatches.**

| clause | anchor | REFUSE cell | ALLOW cell | result |
|---|---|---|---|---|
| **C0 master gate** | siege.py:4567 | shipped `IDLEPECK=False`, **every other clause satisfied** (adjacent, core HP 30, sentinel live, ammo 10 000, bank 10 000) → `False`, `ct.fire` never called | same state, `IDLEPECK=True` → `True`, fired at (20,20) | **BOTH** |
| C1 target | siege.py:4395-4406 | body at (5,5); body DIAGONAL at (19,19) → `False` | body orthogonal at (19,20) → `True` | **BOTH** |
| C2 `NEED_SENTINEL` | siege.py:4572 | `True` + 0 live sentinels → `False` | `False` + 0 live; `True` + 1 live → `True` | **BOTH** |
| **C3 ammunition clause** | siege.py:4360-4361 | live sentinel + ammo **119** (`< AMMO_MIN=120`) → `False` | (a) 0 live sentinels + ammo 0 → `True`; (b) live + ammo **120** (boundary) → `True`; `AMMO_AWARE=False` + live + ammo 0 → `True` | **BOTH** |
| **C4 reserve** | siege.py:4385-4391 | no live sentinel, `ti=43` (reserve 0·3+6+8+30 = **44**) → `False`; live sentinel, `ti=13` (reserve **14**) → `False`; `TI_FLOOR` 8→9 with `ti=14` → `False`; `needed=3` barriers, `ti=22` (reserve **23**) → `False` | `ti=44`; `ti=14`; `needed=3`, `ti=23`; `KEEP_SENT=False`, 0 live, `ti=14` → all `True` | **BOTH**, and each of the three terms (`len(needed)·barrier`, `TI_FLOOR`, `KEEP_SENT`) moved on its own |
| C5 budget / fire gate | siege.py:4408-4418 | `v541_pecks == 60`; `action_cd = 1`; `can_fire()` False → `False` | `v541_pecks == 59` → `True` | **BOTH** |
| **C6 idle predicate** | siege.py:4265-4298 | station elsewhere → `False`; `get_move_cooldown` raises → `False` (fails CLOSED); `_fs_stand_target` raises → `False` | move cd ≠ 0 → `True`; `st is None` → `True`; standing on its station → `True` | **BOTH**, all six documented branches |
| **C7 the call site is an `and`** | siege.py:3711 | `_v541_idle_ok` returned **True** and the rung STILL did not fire, shipped flags | — | **the idle predicate is NOT the binding term**, demonstrated on the shipped conjunct |
| **C8 redirect / finisher** | siege.py:4429, :4479 | core HP 500 → `False`; HP **121** → `False`; HP 12 with 55 pecks spent (budget 10) → `False`; `get_hp` raises → `False` (fails CLOSED) | HP **120** (boundary) → `True`; HP 30 → `True`; HP 10 with budget 10 → `True`; `FINISH_ON=False` + HP 500 → `True` (**the measured-and-refuted unconditional form**) | **BOTH** |

**⚠ THE ONE CLAUSE THAT CANNOT BE DRIVEN BOTH WAYS BY ITSELF: `FS_V541_FINISH_HP`.**
MEASURED — `siege.py:4527-4528` takes `cap = min(FS_V541_FINISH_HP,
2*(FS_V541_MAX_PECKS - self.v541_pecks))`, and `2 × 60 = 120`, **the same number**.
Driven: with `FINISH_HP` raised to 500 and `MAX_PECKS` left at 60, a core at HP 340 (the
leg's own `adjmin` minimum) still refuses, and the allow boundary stays at exactly 120.
Only when `MAX_PECKS` is *also* raised (to 200) does HP 340 allow, with the new boundary
at 400. **⇒ `FS_V541_FINISH_HP` is DOUBLE-LOCKED with `FS_V541_MAX_PECKS`; it is not a
single-constant lever, and a one-line raise of it would be a no-op.** This is not
documented in the doctrine block, which describes the min but does not note that the two
constants are numerically coincident at the shipped values.

---

## 3. LEG-STATE EVALUATION — the counterfactual the builder actually needs

Since the binding term is a compile-time constant, its coverage is 100% by construction
and no replay is required to establish it. The replays answer the **next** question:
**if `FS_V541_IDLEPECK` had shipped `True`, which downstream clause would have refused,
and how often?**

Script: **`scratchpad/s53_v541trace_legstate.py`**, over the leg's 25 archived replays
(`replay_archive/{6db3add5…, 6bf8980e…, 73e920b9…, 7c3e9ae0…, 99bb733a…}`). Our side
is resolved from `teamAName`/`teamBName` per match, never assumed (the leg contains one
match where we are team B).

**Reconstructed per round, engine-side:** our global **ammunition** and **titanium**
(update field 6 `updatePlayers`, `d[1]`/`d[7]` — the decode
`tools/corpus/replay_econ.py:316-330` uses); our live **forward sentinels** (ours, kind
sentinel, `dsq_core(pos, ENEMY core) ≤ 40` — the engine truth behind
`_fs_live_sentinels_vision`, `siege.py:5668-5677`); **orthogonal adjacency** of our
builders to the enemy core footprint; and whether each adjacent body **moved** or
**attacked** that round (the idle proxy).

### 3.1 Instrument validation — both controls, and one caught bug

* **POSITIVE CONTROL, adjacency: 25/25 agreement.** My `adj_rounds` column matches the
  independently written `arr_rounds` of the banked `scratchpad/s53_kladdedose/leg25.tsv`
  **digit-for-digit in all 25 games** (101/389/127/65/83/54/98/66/107/147/22/104/17/78/
  119/63/105/205/149/344/150/935/230/65/101). MEASURED.
* **POSITIVE CONTROL, ammo/titanium: agrees with `replay_econ.py` on both files, both
  teams** — `6db3add5` g1: A `ti=137 ammo=24`, B `ti=2996 ammo=0`; `6bf8980e` g5: A
  `ti=10 ammo=135`, B `ti=1303 ammo=0`. MEASURED.
* ⛔ **AND THAT CONTROL CAUGHT A BUG IN MY OWN DECODER, WHICH IS THE ONLY REASON IT IS
  WORTH ANYTHING.** The first version carried the previous value forward on an absent
  field (`d.get(7, ammo[prev])`). **proto3 omits zero-valued fields**, so a ZERO
  magazine or a ZERO bank read as the last NONZERO one — biasing exactly the cells the
  ammunition and reserve clauses key on, and in the flattering direction (fewer
  refusals). The disagreement showed up on `6db3add5` g1 team B (econ `0`,
  carry-forward `10`). Fixed to absent-means-0; the fix moved the pooled counts by 7
  cells of 4,171 (`res_refuse` 1,667 → 1,674). **Small here; it would not have been
  small on a bank-limited cut.**
* **Column liveness:** none of the refusal columns is constant — `ammo_refuse` ranges
  0–16 across games, `res_refuse` 4–242, and the reserve sweep in §3.3 moves the pooled
  total 474 → 1,674 → 2,366. A constant column validates anything; these are not.

### 3.2 Pooled result (shipped constants, `sent_cost = 30`)

```
DENOMINATOR   4,171 (round, adjacent-body) cells   over   3,924 adjacent rounds
              (the readout's "~3,900 exposed adjacent rounds" — confirmed)

  idle cells (body neither moved nor attacked)   2,771   66.4%
  cells with >=1 LIVE FORWARD SENTINEL of ours     130    3.1%   <-- see below

  AMMUNITION CLAUSE would refuse                    27    0.6%
  RESERVE (collar+TI_FLOOR+KEEP_SENT) would refuse 1,674  40.1%
  BOTH would refuse                                  3    0.1%
  NEITHER would refuse (the peck would have FIRED) 2,473  59.3%
                                  of those, idle   1,475
```

**⇒ MEASURED: the ammunition clause is not the binding term even counterfactually —
0.6% of the exposure.** And it is **BOUNDED far tighter than that by structure**: the
clause requires `live > 0` (`siege.py:4360`), and **we had a live forward sentinel in
only 130 of 4,171 cells (3.1%)**. **3.1% is the CEILING on the ammunition clause's
coverage in this leg no matter what the ammo series says.** ⇒ **the KLADDEDOSE readout's
registered alternative — "the ammunition clause winning its 2 Ti is not separable in
that leg" — is now SEPARATED AND BOUNDED at ≤3.1%, and measured at 0.6%.** MEASURED /
BOUNDED.

*(That 3.1% is itself convergent with `DECODE-ringrace-8013d088-2026-08-21`: our forward
sentinel lands r100–128 while arrival is r8–19, so for most of the exposure there is no
sentinel to starve — which is branch (a) of the doctrine block's own exhaustive split
(`doctrine.py:6029-6032`) doing exactly what it was written to do.)*

### 3.3 Decomposing the reserve — `KEEP_SENT` is the term that binds

Sweeping only the `KEEP_SENT` sentinel-price term (`siege.py:4389-4390`):

| sentinel price used | reserve when no forward sentinel | `res_refuse` | share of 4,171 |
|---|---|---|---|
| 0 (KEEP_SENT term removed) | 6 + 8 = **14** | 474 | **11.4%** |
| **30 (base cost, the shipped term at scale 1.0)** | 6 + 8 + 30 = **44** | **1,674** | **40.1%** |
| 45 (sentinel at scale 1.5) | 6 + 8 + 45 = **59** | 2,366 | **56.7%** |

**⇒ `FS_V541_KEEP_SENT` contributes ~29 pp of the 40 pp; `FS_V541_TI_FLOOR = 8` and
`FS_SEAL_MARGIN = 6` together account for the remaining ~11 pp.** MEASURED. And since
the live scaled sentinel cost is ≥ 30 (scale starts at 1.0 and only rises), **40.1% is a
LOWER bound on the reserve's true refusal share** — the 45-Ti row is the more realistic
mid-game figure. BOUNDED.

### 3.4 What is NOT reconstructible, stated rather than hidden

1. **`len(needed)`** — the collar's remaining barrier debt — is per-body private state
   and is not on the wire. The reserve is computed with `needed = []`, which is the
   RAID call site's own value (`raid.py:480`) and a strict **lower bound** on the two
   siege call sites' reserve. **⇒ reserve refusals are a LOWER bound.** BOUNDED.
2. **`_fs_live_sentinels` is a VISION census** max'd with a team-global beat
   (`siege.py:5658-5666`). This script computes the engine truth (all our sentinels
   within d²≤40 of the enemy core), an **upper** bound on the vision census. A larger
   `live` makes the ammunition clause **more** likely to refuse and the `KEEP_SENT` term
   **less** likely to refuse — the two therefore bracket rather than agree, and the
   0.6%/3.1% ammunition figures are upper bounds while the 40.1% reserve figure is a
   lower bound. **Both errors point the same way as the headline.** BOUNDED.
3. **Ammo and titanium are END-OF-ROUND values**; the bot reads them mid-turn.
   Intra-round spend (a barrier, a sentinel, a `convert_ammo`) is not separable at round
   resolution. BOUNDED.
4. **The idle column is a PROXY** — "this body neither moved nor attacked this round" is
   *not* `_v541_idle_ok`, which asks whether the walker *would* have moved. It is
   reported (66.4%) as context and **no clause verdict rests on it**. BOUNDED.

---

## 4. WHAT THE COUNTERFACTUAL MEANS — the flip is a real treatment, not a no-op

**MEASURED: had `FS_V541_IDLEPECK` shipped `True`, the additive peck would have been
FUNDED and ALLOWED on 2,473 of 4,171 exposed cells (59.3%)** — subject to the idle
predicate, the per-body 60-peck cap, and the action cooldown, none of which is
reconstructible at cell level (§3.4).

The per-body cap alone bounds the dose hard: `FS_V541_MAX_PECKS = 60`
(`doctrine.py:6059`) is a **lifetime** budget per body, so the additive path could not
have delivered more than 60 pecks = **120 HP** from any single body regardless of how
many rounds it stood there. Against a 500 HP core with an enemy builder healing at +4/Ti,
**one body cannot kill through this path** — which the docstring says outright
(`siege.py:4517`: *"never a solo kill plan"*). INFERENCE from the constants, not measured
on a fixture.

⇒ **The flip is worth measuring and is not free.** The doctrine block's arithmetic
(`doctrine.py:6005-6018`: peck = 1.00 HP/Ti, sentinel ammunition = 1.80 HP/Ti, one bank)
prices the cost, and the ws1 battery that produced the ammunition clause measured the
un-clauseed first build at **−8.9 pp timely-kill vs beltbreak2** (`doctrine.py:5994-5998`)
— but §3.2 shows the ammunition clause would have been inert in 96.9% of this leg's
exposure, so **that battery's harm channel is largely absent from the kladde fixture**.
The two facts do not contradict; they say the flip must be measured **on a fixture where
our forward sentinel is actually alive during exposure**, and kladde is not one.

---

## 5. WHY THE CONSTANT IS `False`, AND WHY THAT MATTERS FOR THE FIX CALL

The flag was not left off by accident. `doctrine.py:5937-5949` states the argument:
the v174 autopsy *"licenses TARGET PRIORITY, not a new verb"*; the additive clause
*"ADDS an action on a round the parent spent idle, so it spends titanium that would
otherwise have become sentinel ammunition"*. `raid.py:446-454` repeats it at the call
site. And `siege.py:4546-4552` states the asymmetry: the redirect is free in both
currencies, the additive is free in neither.

**⇒ FIX-SHAPE CALL: FIXABLE BY A CONSTANT, BUT THE CONSTANT IS A SHIP DECISION, NOT A
REPAIR.** The KLADDEDOSE leg measured the additive path at zero because it was switched
off; **it did not measure whether switching it on helps or harms.** Anyone reading the
leg's refutation as "the additive path is broken, fix the ammo clause" would be fixing a
clause that never ran. INFERENCE, but a narrow one.

**Two candidate reframings for the next wave, in the shape the row asked for:**

* **(i) FLIP `FS_V541_IDLEPECK` → `True` and measure it as a two-arm plank.** One line.
  Counterfactually live on 59.3% of kladde-class exposure. Needs a fixture where our
  forward sentinel exists during exposure, or the ammunition clause — the whole reason
  the first build lost 8.9 pp — is untested by the leg that fires it.
* **(ii) LEAVE IT OFF and treat the additive path as correctly disabled** — in which
  case **QUEUE #109's question is answered and the row closes**, and the real refutation
  standing against v541 is the redirect half (§6), which is a *different* mechanism with
  a *different* fix.

**Not a recommendation between them — that is the builder's call.** What is established
is that the row's three named candidates are all zero-coverage and cannot be the answer.

---

## 6. THE REDIRECT HALF — where the leg's 0/1,969 actually comes from

MEASURED, from the banked `DECODE-kladdedose-leg-2026-08-21.md` §2-§3 (not re-derived):

* Our builders were **orthogonally adjacent to the enemy core in 25/25 games**.
* **`adjmin`** — the minimum enemy-core HP over rounds one of our builders stood
  orthogonally adjacent — was **500 in 19 games**, and its **minimum across all 25 games
  was 340**.
* The finisher gate is **≤ 120**. ⇒ **"NEVER IN FINISHING RANGE" 25/25, "IN RANGE AND
  DID NOT FIRE" 0/25.**

Combining with §1's chain: `_v541_corefirst` reaches `_v541_finishable` (`:4473`)
whenever a body is orthogonally adjacent, and **`_v541_finishable` refused in every such
round** because HP > 120 always. **⇒ `_v541_funded_build` — and therefore `TI_FLOOR` and
`KEEP_SENT` — executed ZERO times on the redirect path in this leg as well.** MEASURED
(static chain + the decode's `adjmin` column).

**⇒ ACROSS BOTH HALVES, THE COLLAR/SENTINEL RESERVE AND THE AMMUNITION CLAUSE RAN A
COMBINED ZERO TIMES IN THE 25 GAMES.** Neither can be the binding term of anything the
leg observed.

**And the redirect's gate is NOT fixable by one constant** (§2's double-lock finding):
raising `FS_V541_FINISH_HP` alone is a no-op above 120 because `2 × FS_V541_MAX_PECKS`
is also 120. To reach the leg's own best case (`adjmin = 340`) both constants must move,
and `MAX_PECKS ≥ 170` is a 340 Ti per-body spend at 1.00 HP/Ti against a healed core —
i.e. the thing the doctrine block already prices as the losing conversion. **⇒ DEAD BY
DESIGN as a constant fix; the redirect's precondition is an upstream damage engine
landing the core under 120, which is the readout's own conclusion and the v543burst
dependency.** MEASURED (the double-lock drive) + INFERENCE (the pricing).

---

## 7. CORRECTIONS TO THE RECORD

Two published statements are corrected by this trace. Both are cheap corrections — the
zero they describe is real; the attributed cause is not.

1. ⛔ **QUEUE #109's own GREP block** reads: *"the live additive path runs via
   `_v541_core_attack` (`siege.py:4542`, called `:3712`/`:3787`) gated by
   `FS_V541_AMMO_AWARE and live > 0 and get_global_ammo() < FS_V541_AMMO_MIN`
   (`siege.py:4360-4361`) and the reserve constants."* **The path is not LIVE and it is
   not gated by those clauses** — it returns `False` at `siege.py:4567` on the same flag
   the row's *first* sentence correctly quotes (`FS_V541_IDLEPECK = False`, the additive
   clause SHIPPED OFF). **The row states the fact and then describes a live path in the
   next clause; the two halves of one cell contradict each other.**
2. ⛔ **The KLADDEDOSE readout** (`docs/coordination.md:72249`, banked field fact (2)):
   *"the ADDITIVE peck path (no HP gate) also fired zero — consistent with the ammo
   clause/idle predicate holding it shut, not separable inside this leg as registered."*
   **It is separable, and not by a leg — by reading the function.** The ammo clause
   executed zero times; the idle predicate's verdict was discarded. The zero is
   *consistent* with those hypotheses only in the sense that a dead branch is consistent
   with everything.

**The class:** both readings inferred a *gate* from an *absence* without checking
reachability first. **A clause that never executed cannot be the clause that refused** —
and static reachability is a five-minute check that no amount of leg power substitutes
for.

---

## 8. FILES

| file | what it is |
|---|---|
| `scratchpad/s53_v541trace_harness.py` | the both-ways drive, 39 cells, 0 mismatches (`.venv/bin/python scratchpad/s53_v541trace_harness.py`) |
| `scratchpad/s53_v541trace_legstate.py` | leg-state reconstruction; `--sent-cost` sweeps the `KEEP_SENT` term |
| `scratchpad/s53_v541trace_check.py` | the ammo/titanium positive control against `tools/corpus/replay_econ.py` |
| `docs/research/DECODE-kladdedose-leg-2026-08-21.md` | the banked leg decode; §6 reuses its `adjmin` column rather than re-deriving it |
| `scratchpad/s53_kladdedose/leg25.tsv` | the banked per-game table used as the adjacency positive control |
