# SCREEN PREREG — `gunaxabl` (QUEUE #33): ablate `LOKI_GUNAXIS_PENALTY` on the v140 chassis

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies and commits; this
agent wrote no code under `bots/` and fired no shard.

**STATUS: committed BEFORE the `GUNAXABL` shard is appended to
`scratchpad/corefill_work.txt` and BEFORE its first game.** Two-clock form: this
commit's git author time vs the shard tape's own `# FIXTURE … start=` stamp
(`tools/overnight.sh` writes it before the first game, so the leg clock is a
START and not a first-completed-row). Drafting session wall clock at write time:
`2026-08-14T21:05:36Z` (`date -u`), repo HEAD `2026-08-14T23:05:34+02:00`.

---

## ⛔ READ THIS BEFORE RATIFYING — THE ROW'S PREMISE IS STALE AND THE SCREEN HAS BEEN RUN TWICE

`QUEUE.md:392` says the flag was **"never ablated"** and, re-verified s40,
**"Ablation question stands, never run."** Both halves are false as of
2026-08-13. Recomputed by this agent from the raw shard tapes:

| shard | treatment | control | chassis | pool | n | our game share | band | reading |
|---|---|---|---|---|---|---|---|---|
| `GUNAX0` | `_v183gunaxis0` | `_v169launchlate160` | v116 | **8-map (RETIRED)** | 5,408 | **48.00%** | ±1.32 | outside-BELOW ⇒ ablation COSTS |
| `GUNAXIS0` | `_v206gunaxis0` | `_v197mapcode` | v125 | 15-map (current) | 2,752 | **49.45%** | ±1.85 | **inside band ⇒ could not separate** |

⭐ **AND A THIRD PRIOR THAT SHAPES THE EXPECTED MAGNITUDE:** the knob's VALUE
was swept on the v114 chassis / 8-map pool and is flat either side of 8 —
`GUNPEN4` (penalty 4) **49.93% ±1.33 @ 5,408** and `GUNPEN16` (penalty 16)
**50.72% ±1.33 @ 5,408**, both inside band
(`scratchpad/overnight/GUNPEN{4,16}.result_cache`). Taken with `GUNAX0`'s
−2.00pp at penalty 0, the response looks like a **STEP at zero, not a
gradient**: what matters is whether the term exists, not how big it is. That is
the shape this screen is sized for, and it is why the ablation (8 → 0) is the
right arm rather than another dose point.

Both trees are on disk and both diffs are the one-line change this prereg
proposes (`diff bots/_v197mapcode/doctrine.py bots/_v206gunaxis0/doctrine.py`
⇒ `1533c1533`, `= 8` → `= 0`, nothing else).

⛔ **`docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md:99` reads these as
"ANSWERED TWICE … both BELOW 50 ⇒ the flag DOES something" and that over-reads
the second one.** `GUNAXIS0`'s interval is 47.60–51.30 and contains 50. One
shard resolved the question; the other did not, and the two differ on **chassis
AND map pool simultaneously** — perfectly collinear, so "the flag matters less
on v125" and "the flag matters less on the 15-map pool" fit identically. That is
the confound this repo names by name.

**⇒ WHAT IS ACTUALLY OPEN is exactly one cell: the ablation on the CURRENT
chassis (v140 `_v223sealrepair`, md5 `c4e563af`) and the CURRENT 15-map pool.**
This document registers that cell and nothing wider.

**⇒ AND THE ROW'S DECISION MAY ALREADY BE MAKEABLE WITHOUT IT.** #33 exists to
gate #30 and #31a. `GUNAX0` + the dose probe below are already enough to say the
flag *does something*. If the lane's use for #33 is only to release that gate,
**the cheaper action is to close the row on the evidence in hand and re-spend
5,400 cores elsewhere.** Fire this screen only if the lane wants the effect
SIZED on the tree it ships. That trade is the ratifier's call and is written
here so it is made deliberately.

---

## RATIFY: Hypothesis

**Removing `LOKI_GUNAXIS_PENALTY` (8 → 0) from the shipped v140 tree lowers our
local game share against that same tree by at least 1.33pp** — i.e. the
gun-axis avoidance term is load-bearing on the chassis and map pool we actually
ship, not only on the retired v116/8-map fixture where `GUNAX0` measured it.

---

## THE CHANGE — one constant, named to `file:line`

```
bots/_v240gunaxabl/doctrine.py:1533
  OLD:  LOKI_GUNAXIS_PENALTY = 8
  NEW:  LOKI_GUNAXIS_PENALTY = 0   # QUEUE #33 ablation, gunaxabl 2026-08-14
```

Nothing else in the tree changes. `bots/_v240gunaxabl/` is a byte-for-byte copy
of `bots/_v223sealrepair/` apart from that one line; the builder verifies with
`diff -rq` naming exactly one file and `diff` naming exactly one line.

**TREATMENT TREE: `bots/_v240gunaxabl` (copy of `bots/_v223sealrepair`, md5 of
concatenated `*.py` = `c4e563af4730b4c1595c679fc25098e7` before the edit).**

### Where the constant is read — every site, with anchors

Grepped over the whole incumbent tree (`grep -rn "GUNAXIS" bots/_v223sealrepair/`):

* **DEFINITION — `bots/_v223sealrepair/doctrine.py:1533`** — `LOKI_GUNAXIS_PENALTY = 8`
  (comment at `:1531-1532`: *"penalty for a raid station sitting on a live enemy
  gunner's ray. Same units as `LOKI_EXILE_PENALTY`"*, which is 24 at
  `doctrine.py:1286`).
* **READ — `bots/_v223sealrepair/raid.py:815-816`**, the ONLY read in the tree:

```python
            if (s.x, s.y) in gun_axis:
                score += LOKI_GUNAXIS_PENALTY
```

* **Binding:** `raid.py:64` is `from doctrine import *`, so the constant reaches
  the read site by star-import — there is no second definition and no shadowing.

**STOP CONDITION 1 — IS IT WIRED? YES.** One definition, one read, both live.
This is not the dead-constant case.

### The exact decision path the read changes

`raid.py:728 _raid_station(ct, E, near)` chooses which of the twelve ring
stations a raider walks to, by `min` over a score key built at `raid.py:796-821`:

| term | value | line |
|---|---|---|
| Manhattan distance to the station | `+|dx|+|dy|` | `:796` |
| corner with no unsealed seat left | `+12` | `:801` |
| corner with an open seat | `−6` | `:803` |
| seat (peck station) | `−3` | `:806` |
| station within d²≤2 of an enemy launcher | `+LOKI_EXILE_PENALTY` (24) | `:809` |
| **station on a visible enemy gunner's ray** | **`+LOKI_GUNAXIS_PENALTY` (8)** | **`:815-816`** |
| already standing here (hysteresis) | `−2` | `:818` |

`gun_axis` is built at `raid.py:751,768-776` from
`ct.get_attackable_tiles_from(gunner_pos, gunner_facing, EntityType.GUNNER)`
over every enemy `GUNNER` in `get_nearby_buildings()`.

**Two short-circuits sit above the read and both are real:**
1. `raid.py:741-742` — when `near` is False the function returns a slot-derived
   station and **never reaches the scoring loop at all**. `near` is
   `established or d² ≤ LOKI_APPROACH_DSQ` (`raid.py:189-191`).
2. `raid.py:743-744` — a cached station is returned unless
   `rnd >= self.raid_rescan`, i.e. the loop runs at most once per
   `LOKI_RAID_RESCAN` = 6 rounds per raider (`doctrine.py:1290`).

**STOP CONDITION 2 — DOES THE ABLATION CHANGE A DECISION? YES, MEASURED, NOT
INFERRED.** At 8 the term is large relative to the distance term on a
twelve-tile ring (the whole ring spans a few Manhattan steps), so it routinely
flips the argmin. The dose probe below drives it to both verdicts.

---

## DOSE — the probe this agent ran, both verdicts, 2026-08-14

Two probe trees in the session scratchpad (never under `bots/`), each a copy of
`bots/_v223sealrepair` carrying the **same** stderr instrument inserted after
`raid.py:822 self.raid_station = best`; the arms differ ONLY in
`doctrine.py:1533`. `diff` of the two `raid.py` files is empty, so **the
instrument cannot be reading its own switch** — the failure mode `tools/dose.sh`
was written for. 15-map pool × 2 seeds × 2 arms = 60 games vs the unmodified
incumbent, `--tle 10`, `--replay /dev/null`, stderr captured per game.

**DOSE: the CHOSEN raid station stands on a live enemy gunner's ray in 2.076% of station rescans with the flag ablated to 0 vs 0.577% as shipped at 8 (n=30 games per arm, 12,090 and 12,134 rescans respectively, 2026-08-14).**

That is a **3.60× reduction** in on-ray station occupancy attributable to the
one constant. The flag does what its comment says it does.

**STOP CONDITION 3 — MECHANISM OCCURRENCE. NOT RARE, MEASURED ON THIS FIXTURE:**

| quantity | flag ON (8) | flag OFF (0) |
|---|---|---|
| station rescans per game | 404.5 | 403.0 |
| rescans where an enemy gunner is visible at all | **33.6%** | **24.5%** |
| rescans with ≥1 candidate station on a ray | **22.6%** (91.3/game) | **13.2%** (53.0/game) |
| rescans where the CHOSEN station is on a ray | **0.577%** (2.33/game) | **2.076%** (8.37/game) |

⚠ **The two arms play different games, so the denominators are not matched** —
this is a population/occurrence read, not a paired estimate. Both arms
nonetheless show the mechanism has a live population on every map class in the
pool, and the per-rescan on-ray rate (the bottom row) is the arm-comparable one.

⛔ **THE FIXTURE'S ONE STRUCTURAL WEAKNESS, STATED UP FRONT.** The penalty
dodges *enemy* gunners, and in self-play the enemy is our own bot, which builds
**1.26 gunners/game against Leviathan 13.86 / Erebus 8.35 / Lunds Stallions
10.56** (`scratchpad/corefill_work.txt:619-622`). **A local screen therefore
under-represents the rays this flag exists to dodge by roughly 4–11×, and an
inside-band result bounds the LOCAL value of the flag, never its ladder value.**

---

## Instrument, fixture and units

* **SURFACE: local** — corefill shard, `tools/corefill.sh` + `tools/overnight.sh`.
* **CLUSTER UNIT: none** — CLAUDE.md's enumeration performed, not asserted.
  MATCH cluster: local corefill has no 5-game matches; each row is one game on
  its own seed, so a stratum cannot hold two members of a match — **cluster
  dead**. OPPONENT cluster: every row of the shard is played against the same
  single control tree, so opponent is a constant and carries no between-cluster
  variance — **cluster dead**. Applicable design effect is the measured local
  constant **DEFF = 0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit).
  ⛔ The platform constants (1.529 rated / 1.833 unrated) are NOT applied here:
  over-applying a correction is an error in the same family as omitting it, and
  it would widen every interval below by 24–35% for correlation that is not
  present.
* **ESTIMATOR: unweighted treatment game share** = (rows with `winner == T`) /
  (all rows), read over the shard tape's own rows only. One local row is one
  game, so **game share and win rate are the same number here** — the "win rate
  is not a verdict" rule governs MATCH win rate on the platform and does not
  apply to this fixture; no hedge is needed.
* **PINNED: N/A — local self-play. Opponent version is fixed by construction
  (the control tree is a file on disk), so there is nothing to pin and no
  opponent churn to absorb.**
* **TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure; no submission, no activation, no unrated challenge. `tools/target_value.py` prices rated opponents and has no input here.**
* **POOL_ERA: post-2026-08-13-rotation** · **POOL ERA: post-2026-08-13-rotation**
  (both spellings written deliberately — the underscore form is what the lane
  asked for, the spaced form is the one `tools/prereg_check.py`'s vocabulary
  parses; normalise to one when the format lands). The 15-map pool at
  `tools/overnight.sh:68`: antler archipelago auroraveil drakkarfjord drumlin
  fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale
  valkyrie yulerune).
* **SPANS-POOL-CHANGE: no** — the shard starts and ends inside the current pool
  era. ⚠ `GUNAX0` (48.00%) sits in the RETIRED 8-map era and **is not poolable
  with this shard** for that reason alone, independent of the chassis change.
* **Shard line to append:**
  `GUNAXABL    bots/_v240gunaxabl     bots/_v223sealrepair   5400 312000`
  (seed base 312000 is unused; the highest live base in
  `scratchpad/corefill_work.txt` is 308000 / `SEALFLOOR6`).

---

## RATIFY: Decision rule

* **PLANNED n: 5400 games** (one standard shard, both seat orders played by
  `tools/overnight.sh:109-110`).
* **BOUNDARY: 5400 games** — LOCAL surface, one shard row = one game, there are
  no accepts and no attempt/accept distinction to miscount.
* **BASE RATE: 50.00%** — the structural A/A expectation of a seat-balanced
  self-play shard.
* **BASE RATE SOURCE:** `NULL125` (`bots/_v198null125`, a byte-identical copy of
  `_v197mapcode`, vs `_v197mapcode`), **51.04% ±1.32 at n=5400 on this same
  15-map pool** (`scratchpad/overnight/NULL125.result_cache`, recomputed from
  `NULL125.tsv` by this agent). Its interval 49.72–52.36 contains 50, so 50.00
  stands as the comparator — **but the null cell ran ~1pp HIGH, and our KEEP bar
  sits only 1.33pp below 50, so a marginal outside-below reading is the one most
  exposed to that residual.** Disclosed, not corrected. ⚠ There is no null cell
  on the v140 chassis itself; NULL125 is v125, same pool.
* **BAR: 48.67% or lower** on the ablation arm's game share.
* **BAR SOURCE:** the OB-F ±1.33pp band at n=5400, which is this fixture's own
  95% half-width — recomputed here as **±1.320pp** at
  `1.96·sqrt(p̄(1−p̄)·0.98/5400)`, p̄ = 0.49335. The bar is the band edge, so the
  design has zero slack by construction and that is deliberate.
* **REFERENCE n: none** — the comparator arm is generated inside the same shard
  from the same seeds; there is no fixed external reference that cannot grow, so
  no resolution floor applies.

**THREE BRANCHES, pre-committed:**

1. **KEEP (flag is load-bearing) — share ≤ 48.67%.** Ablating costs ≥1.33pp on
   the shipped chassis. `LOKI_GUNAXIS_PENALTY` stays at 8, #33 closes
   "confirmed", and #30 / #31a are released to be judged on their own merits.
2. **REAL NEGATIVE (flag is a net cost) — share ≥ 51.33%.** We shipped a plank
   that hurts. Delete the term, and the whole `gun_axis` machinery
   (`raid.py:751,768-776,815-816`) is re-opened rather than extended.
3. **DROP BAND — 48.67% < share < 51.33%: COULD NOT SEPARATE.**
   ⛔ **This branch is written "the screen could not separate an ablation effect
   from zero at ±1.33pp on this fixture", NEVER "the effect is zero".** The
   mechanism is dosed (3.60×, above), so an inside-band result means the flag
   fires and buys under 1.33pp of local game share — and the fixture
   under-represents enemy gunners 4–11×, so it does not bound the ladder value.

**⚠ WHAT n WOULD BE NEEDED, because this planned n cannot do everything.**
At DEFF 0.98: excluding a **2.00pp** effect (the `GUNAX0` point estimate) needs
**n ≥ 2,353** — comfortably inside this shard. Excluding a **1.33pp** effect
needs **n ≥ 5,321** — this shard, just. Excluding the **0.55pp** effect that
`GUNAXIS0` actually pointed at on the current pool needs **n ≥ 31,114 games,
5.8 shards.** ⇒ **THIS SCREEN CANNOT DISTINGUISH "the flag is worth 0.55pp" FROM
"the flag is worth nothing", AND IT IS NOT DESIGNED TO.** It distinguishes
"worth ≥1.33pp" from "worth less than that". A ratifier who needs the 0.55pp
question answered should not fire this shard; they should budget six.

* **CUT-SHORT: floor 2700 games.** Below 2700 rows nothing is read and no branch
  is claimed — the rows are KEPT and remain poolable with a later completion of
  the same shard on the same seed base, and with nothing else. At 2700 ≤ n <
  5400 the ONLY claim permitted is branch 1 or 2 read at that n's own wider band
  (±1.87pp at 2700), never branch 3: **an under-powered shard cannot deliver a
  "could not separate" verdict, because that is what an under-powered shard
  always says.** The floor (2700) is ≤ the planned n (5400).

### Obligation 12 — the futility gates, sized

**GATE RESOLUTION: GATE-1000 cannot discriminate its own branches (±3.07pp half-width against a 2.0pp boundary) and is UNRESOLVED BY CONSTRUCTION; GATE-2700 (±1.87pp) resolves the decision only at share < 48.13%; an unresolved gate CONTINUES to the planned n of 5400 and banks nothing.**

`docs/prereg/RULE-futility-gates-2026-08-13.md` binds every shard from its first
row. Its ablation clause applies here (LOW share means the flag helps).

* **GATE-1000 (n ≥ 1000), rule "drop if share < 48.0%".** Half-width at n=1000 is
  **±3.07pp**. The gate's branch boundary sits 2.0pp from 50, i.e. **inside its
  own interval**: at n=1000 this gate **CANNOT discriminate 48.0% from 50.0%**.
  It is **UNRESOLVED BY CONSTRUCTION** and is declared so here, before the fire.
* **GATE-2700 (n ≥ 2700).** Half-width **±1.87pp**. This gate resolves the
  DECISION-REACHED branch **only if share + 1.87 < 50, i.e. share < 48.13%**.
  Any reading at or above 48.13% leaves the decision **UNRESOLVED** at that gate.
* **PRE-COMMITTED DEFAULT WHEN A GATE IS UNRESOLVED: CONTINUE TO THE PLANNED n
  AND BANK NOTHING.** The permissive branch here is "stop early and bank the
  decision"; the restrictive branch is "no decision, keep filling". An
  **UNRESOLVED** gate takes the restriction, never the permission — granting an
  early decision on an estimate that cannot tell 48 from 50 is exactly the
  flatter Obligation 12 exists to stop.
  ⭐ **This is not hypothetical: `GUNAXIS0` was dropped at GATE-2700 on 49.45%,
  which under this sizing is UNRESOLVED and would have continued.** That drop is
  why the current-pool cell is still open, and it is the single clearest reason
  to size a gate before firing rather than after.

---

## MECHANISM METRIC — the one thing only this change can move

**MECHANISM METRIC READS: raid.py:815-816 — the `if (s.x, s.y) in gun_axis: score += LOKI_GUNAXIS_PENALTY` term, observed as the fraction of raid-station rescans in which the CHOSEN station lies on a live enemy gunner's ray. TREATMENT DIFF TOUCHES: doctrine.py (one line, :1533). INTERSECTION: yes — `raid.py:64` is `from doctrine import *`, so the changed constant binds into the read site through the import; the metric is read on the exact line the diff makes inert, and it cannot read identically in both arms.**

**TREATMENT DIFF REFS: HEAD -- bots/** (the arm tree does not exist yet — this
prereg is committed BEFORE it is built, which is the correct order; re-run
`tools/prereg_check.py` once `bots/_v240gunaxabl` lands and the intersection
becomes computable rather than declared).

**Downstream mechanism read, deferred and named so the deferral is a decision.**
The queue row's own metric — *gunner-covered forward builder deaths per game*,
shipped baseline **0.60/game**, movement bar **≥0.15/game**, with **sentinel-only
forward deaths 0.32/game as the negative control that must NOT move** — needs
KEPT replays, and corefill runs `--replay /dev/null`. `tools/dose.py` is the
instrument (it already classifies BUILD/DEATH rows as forward vs home) and a
32-game/arm kept-replay batch is the read. **The screen does not substitute for
it and it does not gate the screen.** ⚠ Its own default map list
(`tools/dose.py:56`) is the RETIRED 8-map pool and must be overridden to the
15-map pool before it is run, or the read lands in the wrong era.

**PRE-STATE (Obligation 7):** the outcome variable is game share, and the
predicted-change set is not already in the target state: on the current chassis
and pool the only existing reading is `GUNAXIS0` at **49.45%, inside the band**,
i.e. **branch 3**, not branch 1. The hypothesis predicts a move to branch 1
(≤48.67%) — a cell that is demonstrably NOT already there, so the prediction can
fail honestly. The mechanism side is also not pre-satisfied in the trivial
direction: the dose separates the arms 3.60×, so a null cannot be blamed on an
undelivered treatment.

---

## RATIFY: Segment

**MAP SEGMENT: RAY-EXPOSED maps — auroraveil, drakkarfjord, frostgate, glacierkeep.**
**PRIMARY SEGMENT: RAY-EXPOSED maps (auroraveil, drakkarfjord, frostgate, glacierkeep).**

**Mechanism reason.** A gunner's shot is a straight line **blocked by
obstacles** and reaching only r²=13; a sentinel's ignores obstacles. The penalty
therefore only has a population where enemy gunner rays actually survive the
terrain to reach the twelve ring stations. That is a terrain property, and the
dose probe measures it directly rather than through a size proxy: the segment is
**the maps on which ≥15% of station rescans carried at least one penalised
station IN BOTH ARMS** — auroraveil (53.7% / 22.4%), drakkarfjord (35.9% /
57.9%), frostgate (28.0% / 19.7%), glacierkeep (50.7% / 19.6%). Three maps sat
at ~0% in both arms (midgard 0.0/0.0, royale 0.0/0.9, fjordgate 0.0/2.4).
⚠ The segment is defined from the **DOSE PROBE** (design phase, 2 games per map
per arm — thin, and stated as thin), never from the screen's own rows.

**EXPECTED DIRECTION: NEGATIVE** — the ablation arm's game share on the
RAY-EXPOSED segment sits **BELOW** its pooled share, because removing the
avoidance term costs most where the rays exist. A segment reading at or above
the pooled share falsifies the segment claim even if the pooled bar is met.

**SEGMENT VALUE CEILING: 26.7% x 4.0pp = 1.07pp pooled** (4 of the 15 maps carry
the mechanism; an on-segment effect of 4.0pp is the largest this fixture has any
reason to expect, given `GUNAX0`'s pooled 2.00pp on a fixture whose gunner
density was no higher).

**Segment resolution.** 4/15 of 5400 is **1,440 games**, half-width **±2.56pp**,
so an on-segment outside-below reading requires **≤ 47.44%**. Per Obligation
15c, a pooled result in branch 3 that clears the segment bar triggers a
**re-screen as a NEW leg with its own n and its own seed base** — the rows that
suggest a segment may not also confirm it.

---

## Secondary column — kill round, and the exclusion restatement

The flag is **defensive in character** (it keeps a raider off a firing line), so
`DEFENCE_ADMISSION_BAR: kill_round_non_regression` applies, and it applies in
the direction that bites an ablation: the risk is that **keeping** the flag
detours raiders and slows our own kill under `R1000_IS_DEFEAT` /
`KILL_WINDOW_RND: 250`.

* **Column:** median `turns` over `cond == core_destroyed` rows, per arm, read
  off the shard tape (both columns already exist in the row schema).
* **A/A noise floor:** `NULL125`, byte-identical arms, read **T 211.5 vs C 208.5
  rounds** — a +3.0-round treatment-slot offset with nothing changed.
* **Material threshold: |Δ median kill round| ≥ 10 rounds** (>3× that floor).
* ⛔ **RESTATEMENT BEFORE BANKING.** "Removing the flag did not slow the kill" is
  a fail-to-exclude claim and may not be banked in that form. It is banked only
  as an EXCLUSION: *the 95% bootstrap CI (10,000 resamples) on the difference of
  median kill rounds excludes a +10-round regression.* If the CI does not
  exclude it, the column reads **UNRESOLVED** and no kill-round claim is made.
  (No design-effect inflation is applied to this CI either: same fixture, same
  DEFF 0.98, same two dead clusters.)

**Hot-turn cost: NEUTRAL — and this is a limitation of the screen, not a
footnote.** Ablating the constant removes one integer comparison and add per
candidate station per rescan (≈12 stations, at most once per 6 rounds per
raider). It does **NOT** remove the expensive half: `gun_axis` is still built
every rescan by the `get_attackable_tiles_from` loop at `raid.py:751,768-776`,
which is unconditional on the constant and runs identically in both arms.
⇒ **This screen prices the DECISION, never the CPU cost of computing it. A
"delete the feature" ship is a different and larger diff and would need its own
arm.** Budget context: 10,000 µs/unit/turn, worst observed 8,748 µs on 900-area
maps, and `get_cpu_time_elapsed()` reads **ZERO locally**, so the local CPU
instrument is dead and no local run can clear a chassis gate.

---

## RATIFY: FALSIFIER

**FALSIFIER: the ablation arm finishes at or above 51.33% game share at n=5400.**
That refutes the hypothesis outright and inverts the plank: `LOKI_GUNAXIS_PENALTY`
would be a shipped term that costs us, `GUNAX0`'s v116 reading would be
era-bound rather than general, and #30 / #31a — which propose pointing the same
avoidance machinery at sentinels — would be extending a mechanism measured
negative rather than a mechanism measured positive.

Two further pre-committed off-prediction outcomes:

* **Segment falsifier:** the RAY-EXPOSED segment share lands at or above the
  pooled share. The mechanism story (rays need terrain to survive) is then wrong
  even if the pooled bar is met, and no conditional ship may be built on it.
* **Dose falsifier / NO-POPULATION guard:** the shard cannot re-measure dose
  (`--replay /dev/null`), so the probe above is the population evidence. Should a
  later kept-replay batch on this same pool and chassis read on-ray station
  occupancy **below 0.5% in the ablated arm** — i.e. contradict the 2.076%
  measured here — this leg is **NO POPULATION**, its currency reading says
  nothing about avoidance, and it must not be quoted against #30.

---

## Interaction with live legs

Two shards are live on the same control tree (`bots/_v223sealrepair`) and the
same 15-map pool:

* **`SEALFLOOR6`** (`bots/_v238sealfloor6`, seed base 308000) — diff is
  `doctrine.py:1228`, `LOKI_SEAL_TI_FLOOR` 0 → 6. Different constant, different
  consumer (the seal spend gate), no shared line with `:1533`.
* **`SALTREF2`** (`bots/_v231saltref`, seed base 32310000, remote worker) — diff
  is `doctrine.py` plus `raid.py:512-520`, inside `_raid_act`'s salt peck budget.
  **Same module as our read site, different function** (`_raid_act` vs
  `_raid_station`) and no shared lines.

⇒ **No confound within this screen:** separate shards, disjoint seed bases
(GUNAXABL takes 312000), each arm measured against the same control. The one
real interaction is **resource**: three 5,400-game shards contend for the same
cores. ⚠ And a durable note for later — all three arms sit in the raid layer,
so any future COMBO of them needs attribution against its best single
ingredient, not only against the control.

---

**PROVENANCE:** `QUEUE.md` (row #33, line 392) · `CLAUDE.md` · `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` · `tools/prereg_check.py` · `bots/_v223sealrepair/doctrine.py` · `bots/_v223sealrepair/raid.py` · `bots/_v223sealrepair/eco.py` · `bots/_v223sealrepair/main.py` · `bots/_v197mapcode/doctrine.py` · `bots/_v206gunaxis0/doctrine.py` · `docs/prereg/SCREEN-gunaxis0-2026-08-13.md` · `docs/prereg/RULE-futility-gates-2026-08-13.md` · `scratchpad/corefill_work.txt` · `scratchpad/corefill.log` · `scratchpad/corefill_relaunch.log` · `scratchpad/gate_watch_state.txt` · `scratchpad/overnight/GUNAX0.tsv` · `scratchpad/overnight/GUNAXIS0.tsv` · `scratchpad/overnight/GUNPEN4.result_cache` · `scratchpad/overnight/GUNPEN16.result_cache` · `scratchpad/overnight/NULL125.tsv` · `scratchpad/overnight/NULL125.result_cache` · `tools/overnight.sh` · `tools/corefill.sh` · `tools/dose.sh` · `tools/dose.py` · `docs/research/QUEUE-ECONOMICS-SWEEP-2026-08-14.md` · plus this agent's own 60-game dose probe run on 2026-08-14 from copies of `bots/_v223sealrepair` held in the session scratchpad (no file under `bots/` was created or modified).
