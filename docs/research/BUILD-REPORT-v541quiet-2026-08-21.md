# BUILD REPORT — `bots/_v541quiet` (v541 CORE-PECK PRIORITY), 2026-08-21

**Parent:** `bots/_v537socket` (ladder v174). **Master flag:** `FS_V541_COREPECK`.
**Build dir / instruments:** `scratchpad/s52_v541_build/`.
**Clock:** all timestamps from `date -u` in the issuing shell. Build ran
2026-08-21 **07:52Z → 08:40Z**.
**Local-fcode constraint honoured:** `scratchpad/overnight/V537POOL.tsv` held
**2,383 rows at 07:52Z and 3,958 at 08:39Z**, both under the 5,400 gate. **ZERO
local fcode runs were issued.** Every game in this report ran on **ws1
(work-server-1, 16 cores)** through `tools/remote_battery.py`. No `tools/*` file
was edited.

---

## 0. THE THREE THINGS THAT MATTER, BEFORE ANYTHING ELSE

**⭐ SURPRISE 1 — THE PAIRED BATTERY WAS NOT PAIRED, AND IT INVALIDATED THE
FIRST THREE CELLS OF THIS BUILD.** The arms shipped `NOISE_ON = True`;
`main.py:1190` seeds `spawn_salt` from an **unseeded `random.Random()`**, so an
fcode game is not reproducible. Measured on the **frozen parent arm run twice**
against the same opponent, maps, seeds, seat and host:

| control | timely-kill ≤r300 | median kill | rows differing (parent vs itself) |
|---|---|---|---|
| parent vs `_v488beltbreak2`, run 1 | **105/180 = 58.3%** | 179 | — |
| parent vs `_v488beltbreak2`, run 2 | **86/180 = 47.8%** | 202 | **177/180** |
| parent vs `_x3r0v173mjolnir`, run 1 | 47/180 = 26.1% | 261 | — |
| parent vs `_x3r0v173mjolnir`, run 2 | 53/180 = 29.4% | 273 | **176/180** |

**A SAME-BOT SWING OF 10.5pp AND 23 ROUNDS AT n=180.** Every effect this build
was about to report sat inside it. `tools/remote_battery.py`'s own docstring
already carried the fact — *"Control: NOISE_ON, same host, repeat run → 11/12
and 12/12 rows differ"* — and the 0/12 determinism it certifies is for
**NOISE_OFF arms only**. My error was assuming the stub harness's NOISE_OFF
poke reached the battery; it does not (that poke is an in-process `setattr`,
and the battery ships trees to fcode).
⇒ **A PAIRED BATTERY IN THIS REPO IS PAIRED ONLY IF EVERY TREE IN IT — BOTH
ARMS *AND* THE OPPONENT — HAS `NOISE_ON = False` ON DISK.** With that done the
parent reproduced itself **0/180 across two separate runs**, and everything in
§4 is measured on that fixture.

**⭐ SURPRISE 2 — THE AUTOPSY'S FIX, TAKEN LITERALLY, IS REFUTED ON THIS
FIXTURE.** The unconditional redirect (core over conveyor at core adjacency,
exactly as `AUTOPSY-v174-losses-2026-08-21.md` §5.2 specifies) **lost every
timely kill in the one cell where it acted** vs beltbreak2 (18/18 → 0/18) and
was **uniformly slower** vs mjolnir. Adding a **finisher condition** — redirect
only when the core is inside the peck budget's finishing range — flipped the
same cell to **strictly faster with no primary regression**. §4.3.

**⛔ SURPRISE 3 — THE EFFECT LIVES IN ONE `(map, seat)` CELL, SO THE
GAME-LEVEL p-VALUES IN THIS BUILD ARE VOID.** All 18 differing rows vs
beltbreak2 are `midgard_*_B`, and the 18 seeds return **one unique kill pair**
(268, 270) — ρ ≈ 1 inside the stratum. **Effective n = 1 cell, not 18 games.**
Every table below reports the cell count as the effect size and the p-value
only alongside it. §4.4.

---

## 1. WHY THE SILENCE EXISTED — read before judging the change

`LOKI_QUIET_ON` (`doctrine.py:1687`, LOKI-7/v123) silences **all** builder
melee. It was a **measured win, not a tidy-up**: v96 went 12-3 with core-kill
share **12/15 = 80%** against v94 Eir's 33% (p=0.025). The mechanism is an
ENGINE RULE: **acting and moving are mutually exclusive for a builder**, this
line wins on ARRIVAL, so every peck is a step not taken. The second half is
arithmetic: **2 damage a round against a 500 HP core that one enemy builder
heals at +4 for 1 Ti is not progress.**

**And the harm has been resurrected once, at a measured price.** `_v178salt`
(LOKI-SALT, 2026-08-12, 25 live games) re-opened a melee verb with a *narrower*
target than this one. Its mechanism confirmed perfectly (20/20 salts on a tile
the same bot had pecked to ≤2 HP; 6.68 barriers/game vs a 3.48-3.72 baseline)
and it **failed on kill round: 13 kills at median r179 against a pooled r129,
Mann-Whitney p=0.008.** The diagnosis was never the mechanism — ~10 pecks is
~10 rounds of not walking.

⇒ **The harm to guard against is named and measurable: ROUNDS TAKEN FROM
MOVEMENT.** Not "melee", not "Ti spend". The tree already carries three
carve-outs that pierce QUIET for targets whose own arithmetic inverts (conveyor
melee `doctrine.py:1744`; `FS_CLEAR_RING_ON`; `FS_HOME_TURRET_RESPONSE`), and
each is narrow by construction.

---

## 2. THE PREMISE OF RECORD, AND THE MID-BUILD CORRECTION

This build began from `FIELD-DEBUT-v174-2026-08-21.md` §5.3 (raiders reach
d²≤2 of the enemy core in **25/25** rated games; **builder core damage 0 HP in
25/25**; our first sentinel r67+ against kladde's r9 home guard) and its first
design **un-silenced the verb** — an additive, idle-gated core peck.

**That premise was corrected mid-build**, and the correction is the report's
premise source: **`docs/research/AUTOPSY-v174-losses-2026-08-21.md` §5.2**, ten
match games decoded —

> **556 builder attacks. 517 into enemy CONVEYORS. 12 into gunners. 27 onto
> tiles whose target was already dead. ZERO into an enemy CORE. And 419 of
> those attacks were made WHILE STANDING NEXT TO AN ENEMY CORE, 407 of them
> into a 20 HP conveyor.**

⇒ **THE VERB IS NOT SILENT. IT IS MISDIRECTED.** `LOKI_QUIET_ON` forbids the
**core** (`raid.py:290`) while the LOKI-SALT carve-out permits the **belt**, so
an established raider spends its one action per turn on the cheapest object in
reach with the win condition one tile away. kladde g1: bot #3 parked on their
socket **64 consecutive rounds**, 51 attacks on the conveyor at (25,27), 0 on
the core — **in a game we won**, which is why *do-we-win* is not a dose control
for this fix. kladde g3: 229 attacks, 226 into conveyors, 0 into the core.

**What changed in the tree because of it:**
* the master was **renamed `FS_V541_ATTACK` → `FS_V541_COREPECK`** — "attack"
  described un-silencing a verb, which is not what this builds;
* the shipped clause became a **target-priority REDIRECT above the salt verb**
  (`raid.py` clause 6.5), not a new verb below it;
* the additive form was **demoted to `FS_V541_IDLEPECK`, shipped OFF**;
* `LOKI_QUIET_ON` stays `True` and `raid.py:290` stays silenced. **The −10.83
  v527 wholesale-un-silencing precedent is not tested here and is not
  challenged.**

---

## 3. THE GATING SHIPPED

`FS_V541_COREPECK = True` (master) · `FS_V541_COREFIRST = True` (the redirect)
· `FS_V541_FINISH_ON = True`, `FS_V541_FINISH_HP = 120` (the finisher
condition) · `FS_V541_IDLEPECK = False` (additive form, off) ·
`FS_V541_AMMO_AWARE = True`, `FS_V541_AMMO_MIN = 120` · `FS_V541_KEEP_SENT =
True` · `FS_V541_TI_FLOOR = 8` · `FS_V541_MAX_PECKS = 60` ·
`FS_V541_NEED_SENTINEL = False` · `FS_V541_LOG = False`.

**The redirect fires only when all of these hold:**
1. the body is **orthogonally adjacent to an enemy CORE footprint tile** — the
   engine's own requirement for the attack verb, and **not** implied by the
   field report's `arr2` (d²≤2 includes diagonals; the harness drives that
   negative case explicitly);
2. **the core is FINISHABLE**: `hp ≤ min(FS_V541_FINISH_HP, 2 × remaining peck
   budget)`. §4.3 is why;
3. **funding**: strictly above the whole remaining collar
   (`len(needed)×barrier + FS_SEAL_MARGIN + 8`) and, while no forward sentinel
   is alive, **a whole sentinel's price on top** — a peck may never be the
   reason the first sentinel is unaffordable, since 100% of our measured core
   damage is sentinel damage;
4. per-body budget `< 60` pecks (120 Ti / 120 HP ceiling per body).

**Target discipline:** the **enemy core and nothing else**. Never buildings
generally — destroying an enemy building removes its contribution to their cost
scale and makes everything they build cheaper (CLAUDE.md guard-matrix sweep), so
demolition is a gift.

**Two funding forms, and the asymmetry is deliberate.** The REDIRECT takes the
build reserve only; the ADDITIVE clause takes the build reserve **plus the
ammunition clause**. Reason: a peck is **2 damage for 2 Ti = 1.00 HP/Ti**,
while the same 2 Ti as sentinel ammunition is 2/10 of an 18-damage shot =
**1.80 HP/Ti** (`convert_ammo` is 1:1 and the only ammo source), and
`main.py`'s KILL-phase magazine drains the bank to the collar floor — so an
*additive* peck converts the damage budget from the 1.80 channel into the 1.00
channel. That premise is **false for the redirect**, where the same 2 Ti goes
to a conveyor either way; applying the clause there would refuse the core and
hand the titanium to the belt.

**The harm check is built into the additive clause's gate.** `_v541_idle_ok`
reproduces the parent's own walker (`_fs_walk` / `_fs_supp_walk` /
`_raid_station`, per layer) clause for clause and permits an action only where
that walker's decision was "stand still". **The redirect needs no such gate at
all** — it takes a round the parent was already spending on an action and swaps
the target. That is a strictly stronger safety argument than the idle gate, and
it is why the two clauses sit on opposite sides of the salt verb.

---

## 4. MEASUREMENT

### 4.0 Instruments — all four self-tested **both ways**, per guard, per branch

| file | what it answers | selftest |
|---|---|---|
| `flagoff_audit.py` | static flag-off: R1 no derived module-level constant; R2 every subordinate read dominated by the master; R3 every call into the `_v541_*` family guarded | **10 cases, 3 rules, each driven to both verdicts** — including the short-circuit-ORDER case (master as a *later* `and` operand must FAIL) |
| `harness.py` | mechanism/dose on `tools/stub_engine.py`, calling the **real** methods | **41 assertions**; every gate driven to both verdicts, incl. both sides of the r300-analogue boundaries (core HP 120 fires / 121 refuses) and two vacuity controls on the harm check |
| `diverge.py` | did the flag change the game at all; and the flag-off certificate | identity + divergence both produced; **all 5 compared columns driven individually** |
| `paired.py` | McNemar on the PROGRAMME primary, paired sign test on kill round, the noise control, and the `(map,seat)` breakdown | 9 groups, each both ways |

**Two instrument defects were caught by these selftests and are recorded
because a check that has never produced the other verdict has not been seen to
check:**
* `harness.py` set `P.team` to the **stub's** `Team.A` while `ct.get_team()`
  returns the **fcode** enum — so every friendly entity read as hostile and
  `_fs_live_sentinels` returned 0 on a board with a sentinel standing on it.
  **Two selftest cases failed and named it.** Without them the sentinel-reserve
  guard would have "passed" while never once seeing a sentinel.
* `diverge.py` originally compared the `winner` column. run_grid writes the
  **winning arm's directory name** there, so on every row where both arms won
  it differs by construction. The first read scored `winner = 123/180`, of
  which ~63 was arm-name. **A column that differs by construction validates
  anything.** Excluded, with a selftest case that drives `winner` differing on
  every row and requires **zero** divergence.

### 4.1 Dose — and what is DEFERRED

**The exact field-comparable dose (builder-attack events per game and core HP
dealt by builders) is DEFERRED and is NOT claimed here.** Reading it needs a
replay decode; `remote_battery.py` returns the run_grid tape, not replays, and
local fcode is barred until V537POOL reaches 5,400 rows. `FS_V541_LOG` exists
for it but is useless on platform replays (`stdout` empty in 30,664/30,664
BotOutput events, CLAUDE.md s28), so the post-V537POOL read is a **local replay
decode**, not a stdout scrape.

**What IS measured, both ways:**

*Per-call, on the stub engine (real methods, real gates):*

| configuration | fired | enemy core HP | our Ti | pecks |
|---|---|---|---|---|
| `FS_V541_COREPECK = True` (shipped) | **yes** | **−2** | **−2** | 0→1 |
| `FS_V541_COREPECK = False` | no | 0 | 0 | 0 |
| parent tree | *the method does not exist* (counter-control) | — | — | — |

*Per-game, on ws1 — the divergence proxy.* Under NOISE_OFF two identical trees
produce identical tapes, so a differing row is a board on which the flag
changed play. **Necessary, not sufficient, for "the verb fired"; with a
single-verb diff it is the only candidate.**

### 4.2 The NOISE_OFF fixture is sound

`parent` vs `parent`, two **separate** ws1 runs, 180 matched cells:
**0/180 rows differ.** The same instrument reads **18/180** for the treatment
arm in the same grid — the positive control sits beside the negative one.

### 4.3 The headline: unconditional redirect vs finisher

All rows: ws1, NOISE_OFF, 5 maps × 18 seeds × 2 seats = **180 matched cells per
arm per opponent**, arms interleaved on the same seeds.

| arm | opponent | rows differing | **timely-kill ≤r300 (ITT, all games)** | McNemar | kill clock, cells both killed |
|---|---|---|---|---|---|
| **unconditional redirect** | `_v488beltbreak2` | 18/180 | **108 vs 126 = −10.0pp** | A-only 0, **B-only 18** | 0 faster, 0 slower (126) |
| **unconditional redirect** | `_x3r0v173mjolnir` | 24/180 | 64 vs 64 = 0.0pp | 0 / 0 | **0 faster, 18 SLOWER** (115) |
| **finisher (SHIPPED)** | `_v488beltbreak2` | 18/180 | **126 vs 126 = 0.0pp** | 0 / 0 | **18 FASTER, 0 slower** (144) |
| **finisher (SHIPPED)** | `_x3r0v173mjolnir` | **0/180** | 64 vs 64 = 0.0pp | 0 / 0 | **ZERO DOSE** |
| **flag-off** | `_v488beltbreak2` | **0/180** | identical | — | — |

**The unconditional form is refuted and the mechanism is LOKI-QUIET's own
argument arriving from the other side.** A conveyor is 20 HP — **ten pecks** —
and the tenth **severs a delivery chain**: 2 damage a round *finishes* it. A
500 HP core that one enemy builder heals at +4 does not finish, at 250 pecks
and 500 Ti. **The redirect trades a target where the arithmetic inverts for the
one target where it never has.** `doctrine.py:1744` says exactly this in
advance; the battery measured the price of ignoring it.

**The synthesis, which is what ships:** both readings are right about
*different core HP*. Pecking a **full** core instead of cutting a belt is the
mistake the battery found; pecking a core that is 30 HP from dead **while**
sawing a belt is the mistake the autopsy found. So the redirect is conditioned
on the only thing that separates them — is this core inside finishing range of
the budget this body still holds. **That makes the clause a FINISHER, which is
what the verb's price supports and what the brief asked for. It is never a solo
kill plan: 500 HP is 250 pecks and 500 Ti.**

### 4.4 ⛔ THE SIZE OF ALL OF THIS — read before quoting any number above

`(map, seat)` breakdown, 10 cells per opponent:

| arm | opponent | cells with ANY dose | what happens there |
|---|---|---|---|
| unconditional | beltbreak2 | **1 of 10** — `midgard` seat B | 18/18 rows; timely **18 → 0**; we lose the cell |
| unconditional | mjolnir | **2 of 10** — `midgard` A, `nordkap` B | midgard A: kill r134 → **r136, slower**; nordkap B: no kill either way |
| **finisher** | beltbreak2 | **1 of 10** — `midgard` seat B | 18/18 rows; timely **18 → 18**; kill r270 → **r268** |
| **finisher** | mjolnir | **0 of 10** | nothing |

**Within `midgard` seat B the 18 seeds return ONE unique kill pair, (268, 270).
The seeds do not vary the outcome: ρ ≈ 1 in the stratum.**
⇒ **EFFECTIVE n = 1 `(map,seat)` CELL, NOT 18 GAMES. The p = 0.0000 figures in
§4.3 are artefacts of counting one observation eighteen times and must not be
quoted alone.** This is CLAUDE.md's design-effect *procedure* applied: enumerate
the clusters, ask whether the stratum can hold more than one member, use the
DEFF of those that survive. Here the `(map,seat)` cluster survives with
eighteen identical members.

**⇒ HONEST VERDICT ON THE LOCAL SCREEN: the shipped finisher form is
NON-REGRESSIVE on both opponents and shows a 2-round acceleration in the single
cell where it fires — and it fires in 1 of 20 (map, seat) cells. THE LOCAL
SCREEN CANNOT CONFIRM THIS PLANK. It can only fail to refute it, and it does
fail to refute it.** The standing rider applies in full: local cannot confirm
for siege shapes. **The real test is a pre-registered unrated leg against a
pinned home-guard opponent (kladde-class), which our imported trees are not.**

### 4.5 The harm check — has LOKI-QUIET's measured harm returned?

**The harm to reproduce is "rounds taken from movement", the thing that cost
`_v178salt` its leg.** Three independent readings, all negative:

1. **Structural.** The shipped clause is a REDIRECT: it never adds an action,
   so there is no step for it to consume. The additive clause, which could,
   **ships OFF**.
2. **Predicate-level (stub engine, both trees, same boards).** The parent's own
   `_fs_walk` was driven on 5 boards and its movement recorded; the child's
   `_v541_idle_ok` was asked the same question. **0 conflicts over 5 boards**,
   with both vacuity controls firing (≥1 board makes the parent walk; ≥1 board
   opens the gate). ⚠ Five boards is a predicate check, not a field.
3. **Outcome-level (ws1, NOISE_OFF).** LOKI-SALT's failure signature is a
   **rising** kill round. The shipped arm's paired sign test reads **18 faster,
   0 slower** vs beltbreak2 and **0/0** vs mjolnir. **The signature is absent
   and its opposite is present** — subject in full to §4.4's one-cell caveat.

**VERDICT: the harm has not returned.** The refuted *unconditional* arm did not
show it either — it lost games by giving up belt cuts, not by giving up steps —
which is itself worth recording: **this plank's failure mode is not the one
LOKI-QUIET warned about.**

### 4.6 Flag-off identity

* **Empirical:** `FS_V541_COREPECK = False` vs the frozen parent, ws1,
  NOISE_OFF, 180 matched cells: **0/180 rows differ on all compared columns**,
  in the same grid where the treatment arm read 18/180.
* **Static:** `flagoff_audit.py` reports **CLEAN — R1/R2/R3 satisfied, 12
  subordinate flags** over all 5 files. No module-level constant derives from
  an `FS_V541_*` name; every subordinate read is short-circuit-dominated by the
  master or lexically inside a `_v541_*` method; every call into that family
  from outside it is master-guarded.
* **The one thing that is unconditional, stated openly:** `main.py` initialises
  three per-body fields (`v541_pecks`, `v541_st_rnd`, `v541_st`) with the flag
  off. Writing a field nothing reads cannot change behaviour, and R2/R3
  enumerate the read sites. The 0/180 identity run is what covers it
  empirically.
* **Parent arm provenance:** `scratchpad/s52_v541_build/arms/parent` was
  verified md5-identical to `bots/_v537socket` (`PARENT_FREEZE.md5`).

---

## 5. WHAT THIS DOES AND DOES NOT LICENSE

**Licensed:**
* Shipping the **finisher-conditioned redirect** as non-regressive on this
  fixture, with §4.4's one-cell caveat attached to every number.
* **Retiring the unconditional (autopsy-literal) redirect** as locally
  refuted — with the mechanism named, not just the outcome.
* The **NOISE_OFF requirement** as a standing rule for every paired battery in
  this repo, arms **and** opponent (§0, surprise 1). This is the most
  transferable output of the build.
* The **peck-vs-ammunition exchange rate** (1.00 vs 1.80 HP/Ti) as a
  rules-level fact needing no fixture.

**NOT licensed:**
* Any currency or win-rate verdict. Local, us-authored opponents, 1-2 live
  cells.
* Any claim that this plank helps against a **home-guard** opponent. Our
  imported trees are Mjolnir-class; kladde-class is untested here, and kladde
  is the opponent the premise came from.
* Any dose claim in field-comparable units (attacks/game, builder core HP) —
  **deferred to a post-V537POOL local replay decode** (§4.1).
* Quoting §4.3's p-values without §4.4.

---

## 6. DEFERRED / OPEN

1. **The field-comparable dose count** (builder attacks into cores per game;
   core HP dealt by builders) — post-V537POOL local replay decode. The field
   baseline is **0 in 25/25**, so any nonzero is the both-ways dose.
2. **A pinned unrated leg vs a kladde-class home-guard opponent.** This is the
   only fixture that can confirm the plank; `fcode match unrated <team>
   --match <past_match_id>` pins their version.
3. **`FS_V541_FINISH_HP` is reasoned, not swept** (it is the body's own
   remaining peck budget). A sweep is open work.
4. **`FS_V541_IDLEPECK`** — the additive form. The autopsy's own tape shows
   established bodies idle for **85, 205 and 973 consecutive rounds**; the
   clause is built, gated and self-tested, and ships off pending a leg.
5. **The siege-layer analogue is untouched.** `_fs_try_clear` (ring ladder rung
   3) pecks enemy buildings on collar seats and can carry the same
   misdirection, but it has a structural purpose the salt verb lacks
   (unblocking a seat the collar needs). Named, not changed.
6. **Does the ammunition clause belong on the SALT verb too?** The 517 conveyor
   attacks each cost 2 Ti out of the same bank the magazine draws on. Out of
   scope here; the arithmetic is in §3.
7. **The `midgard` seat-B degeneracy** — 18 seeds producing one outcome — is a
   property of the local seed set, not of this plank. Worth a look for every
   build that reads this fixture.

---

## 7. MANIFEST — every artefact this build produced

**Tree:** `bots/_v541quiet/`. Changed vs parent: `doctrine.py` (the v541 flag
block), `siege.py` (the `_v541_*` family), `raid.py` (clause 6.5 redirect,
clause 8 additive, `import sys`), `main.py` (3 per-body state fields).
`eco.py` unchanged. Frozen: `scratchpad/s52_v541_build/TREE_FINAL.md5`.

**Arms** (`scratchpad/s52_v541_build/`):

| path | configuration | role |
|---|---|---|
| `arms/parent` | `bots/_v537socket` verbatim, md5-verified (`PARENT_FREEZE.md5`) | control |
| `arms_n0/parent` | as above + `NOISE_ON = False` | control, deterministic |
| `arms_n0/v541` | shipped config + `NOISE_ON = False` | **treatment** |
| `arms_n0/v541flagoff` | `FS_V541_COREPECK = False` + `NOISE_ON = False` | identity certificate |
| `arms/v541both` | `FS_V541_IDLEPECK = True` | built, **not fired** (see §6.4) |
| `opps_n0/beltbreak2`, `opps_n0/mjolnir` | opponents + `NOISE_ON = False` | fixture |

**Instruments**, all `--selftest` clean, each guard driven to both verdicts:
`flagoff_audit.py` (10 cases / 3 rules), `harness.py` (41 assertions),
`diverge.py` (5 columns individually), `paired.py` (9 groups),
`summarise.py` (reused from `scratchpad/s51_v523_build/`, re-selftested here).

**Tapes** (each `<dir>/<arm>.tsv`, run_grid format, plus `RESULT.txt` and
`_raw/<host>/` driver logs):

| dir | fixture | status |
|---|---|---|
| `grid_mjolnir`, `grid_beltbreak`, `grid2_mjolnir`, `grid2_beltbreak` | NOISE_ON | ⛔ **VOID** — retained *only* as the §0 noise control |
| `n0_beltbreak`, `n0_mjolnir` | NOISE_OFF, unconditional redirect | valid; §4.3 rows 1-2 |
| `fin_beltbreak` | NOISE_OFF, shipped finisher + flag-off arm | valid; §4.3 rows 3, 5 and §4.6 |
| `fin_mjolnir` | NOISE_OFF, shipped finisher | valid; §4.3 row 4 (zero dose) |
| `reel_check` | NOISE_OFF, `midgard` only | §8 reproduction check |

**Logs:** `OUT_grid*.log`, `OUT_n0_*.log`, `OUT_fin_*.log`, `OUT_reel_check.log`
(driver transcripts, incl. the oversubscription refusal at 08:08:26Z).
**Selftest transcripts:** `OUT_flagoff_selftest.txt`, `OUT_flagoff_scan.txt`.

---

## 8. REEL — WHAT TO WATCH, AND WHAT THERE IS TO WATCH IT WITH

⛔ **THERE ARE NO REPLAYS, AND THAT IS A LIMIT RATHER THAN A STYLE CHOICE.**
This build made **zero local `fcode` runs** (V537POOL gate, §0) and
`tools/remote_battery.py` returns the run_grid **tape**, not replays; the remote
scratch is reaped by the driver's own cleanup (`_raw/<host>/` holds driver logs
and per-block tapes only — 20 files, no `.replay26`). **So the reel is a
deterministic re-run recipe.** That substitute is only worth anything because
the fixture was *proved* reproducible: the frozen parent reproduced itself
**0/180 across two separate ws1 runs** (§4.2).

**Re-executed at 2026-08-21 08:45:22Z and it reproduced the stored cell
byte-for-byte: `v541` 0/36 rows differ, `parent` 0/36 rows differ.** That check
is this reel's substitute for pressing play.

### REEL 1 — ⭐⭐ **THE ONLY CELL THE PLANK ACTS IN: `midgard`, seat B, vs `_v488beltbreak2`**

*There is exactly one, and that is the finding — §4.4. Watch it knowing it is a
single `(map, seat)` observation replicated over 18 degenerate seeds, not 18
independent games.*

```
.venv/bin/python tools/remote_battery.py \
    --arm v541=scratchpad/s52_v541_build/arms_n0/v541 \
    --arm parent=scratchpad/s52_v541_build/arms_n0/parent \
    --opp scratchpad/s52_v541_build/opps_n0/beltbreak2 \
    --maps midgard --seeds 1-18 --block-size 3 --par 5 \
    --hosts work-server-1 --out <outdir> --runid <runid>

.venv/bin/python scratchpad/s52_v541_build/paired.py \
    <outdir>/v541.tsv <outdir>/parent.tsv
```

| seat B, all 18 seeds | kill round | timely ≤r300 |
|---|---|---|
| `parent` (`_v537socket`) | r270 | 18/18 |
| **`v541` shipped (finisher)** | **r268** | **18/18** |
| `v541` unconditional redirect (`FS_V541_FINISH_ON = False`) | **our core dies r289** | **0/18** |

**Read all three rows together — the middle one is only interesting next to the
third.** The same clause, on the same board, with and without the finisher
condition, is the difference between shaving two rounds off a kill and losing
the game outright. Seat **A** on the same map and every other map is
**byte-identical to the parent**; the whole plank lives in this one row.
To watch the refuted arm, flip `FS_V541_FINISH_ON` to `False` in
`arms_n0/v541/doctrine.py` and re-run the recipe above — that reproduces
`n0_beltbreak`.

### REEL 2 — THE FLAG-OFF CERTIFICATE (same recipe, third arm)

```
    --arm flagoff=scratchpad/s52_v541_build/arms_n0/v541flagoff   # add, --par 3
.venv/bin/python scratchpad/s52_v541_build/diverge.py \
    <outdir>/v541flagoff.tsv <outdir>/parent.tsv --expect same
```
**0/180 rows differ**, in the same grid where the treatment arm reads 18/180.
**The positive control is in the same table as the negative one**, which is the
only reason the zero means anything.

### REEL 3 — ⛔ **THERE IS NO REEL FOR THE NOISE_ON CELLS, AND WHY**

`grid_*` and `grid2_*` are **VOID and not re-runnable by construction**: their
arms carry `NOISE_ON = True`, `main.py:1190` seeds `spawn_salt` from an
**unseeded** `random.Random()`, and re-running them produces a different tape
every time — measured at **177/180 and 176/180 rows differing for the frozen
parent against itself** (§0). **A recipe that cannot reproduce its own output is
not a reel**, so none is given. Those four tapes are retained for exactly one
purpose: they *are* the evidence for the noise finding, and deleting them would
delete it.

### 8.1 What replaces this section

The mechanism dose in field units (builder attacks into cores per game; core HP
dealt by builders, field baseline **0 in 25/25**) is deferred to a
post-V537POOL **local replay decode** (§6.1). **When that lands it produces real
replays, and those replace this reel.**

---

## 9. WHERE THE TRANSFERABLE RULE LIVES

⭐ **THE TRANSFERABLE RULE FROM THIS BUILD IS §0 SURPRISE 1, AND IT IS HEADED
THERE FOR A READER WHO SKIMS: *a paired battery in this repo is paired only if
every tree in it — both arms AND the opponent — has `NOISE_ON = False` on
disk.*** It is stated in the report's first section under its own bolded
heading, restated in `scratchpad/s52_v541_build/paired.py`'s module docstring
(the file a future author runs to read a paired cell), and carried in the
commit message. **`tools/remote_battery.py` is NOT edited** — the constraint
forbids it — so a future author who reaches only for the tool gets its existing
docstring, which already records the NOISE_ON control at 11-12/12 rows
differing; this build is the worked example of what ignoring that costs.
