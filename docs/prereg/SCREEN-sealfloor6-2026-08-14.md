# SCREEN PREREG — SEALFLOOR6: `LOKI_SEAL_TI_FLOOR 0 → 6`, the floor's UPWARD arm (QUEUE #53)

**STATUS: committed BEFORE the `SEALFLOOR6` shard's first row exists** (two-clock:
this file's git author time vs the first `SEALFLOOR6` row's timestamp in
`scratchpad/overnight/SEALFLOOR6.tsv` / `scratchpad/corefill.log`; the side lane
certifies the pair). No row of this shard exists at commit time and none may be
read before it does. Drafted 2026-08-14T20:16:51Z (`date -u`, same shell call),
repo at `7f2a1c6f`.

**PROVENANCE: docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md · QUEUE.md (row #53) · docs/prereg/SCREEN-sealrepair-2026-08-14.md · bots/_v238sealfloor6/doctrine.py:1225-1232 · bots/_v238sealfloor6/raid.py:270**

Drafted by a FRESH agent with **no inherited session context** beyond the four
inputs above plus the builder's handed facts (recorded verbatim in §1). Files
opened read-only to VERIFY a stated fact rather than to source a new one:
`bots/_v223sealrepair/doctrine.py:1228` and `raid.py:270` (the control's
constant and consumer), `diff` of the two trees (the one-hunk claim),
`bots/_v238sealfloor6/raid.py:62-65` (the import binding),
`bots/_v238sealfloor6/doctrine.py:1580` (the salt-floor asymmetry),
`tools/overnight.sh:60,95-110` (fixture, seat alternation, `--tle 10`),
`tools/corefill.sh:96,165` (launcher + basename-collision refusal),
`tools/overnight_read.py:540-575` (the kill-round read-out),
`tools/prereg_check.py` (token vocabulary and arithmetic),
`docs/prereg/RULE-futility-gates-2026-08-13.md`, `docs/prereg/SCREEN-sealsweep-2026-08-14.md`,
`docs/prereg/SCREEN-nestshot-2026-08-14.md`, `docs/prereg/SCREEN-v140vs145-2026-08-14.md`
(structure only), `docs/research/SPEC-pool-era-token-2026-08-14.md`,
`tools/panel_read.py:94` (the 900-area map list), `scratchpad/corefill_work.txt`
(seedbase collision check), `ls -l maps/` (map-patch state).
**No shard row of any kind was read; no game was run by this agent.**

---

## 1. THE ARM — one constant, one line (builder-handed, cited as such)

**Handed by the builder this session, and stated as handed rather than
re-derived:**

* **TREATMENT `bots/_v238sealfloor6`** — the exact one-line diff against the
  CONTROL: `doctrine.py:1228` `LOKI_SEAL_TI_FLOOR 0 → 6`. **Compile-checked;
  smoke-tested 2 games, no tracebacks.**
* **CONTROL `bots/_v223sealrepair`** = **v140, the LIVE incumbent**
  (mapfix + SEALFLOOR0 + l4repair, shipped 2026-08-14 11:37Z).
* **History:** the floor was **born at 12**, swept **downward to 0**
  (`SEALFLOOR0`, **53.94 two-host pooled**), and 0 shipped inside v140. **This
  arm tests the midpoint 6, UPWARD from the shipped 0.**
* **Related, untouched asymmetry:** `LOKI_SALT_TI_FLOOR = 12` at
  `doctrine.py:1580`, whose own comment says *"matches `LOKI_SEAL_TI_FLOOR`"* —
  it has not matched since SEALFLOOR0 shipped. **Not in this arm's diff and not
  claimed by it**; recorded because a floor result here is the evidence that
  would motivate a salt-floor arm next, and because the stale comment is a live
  drift flag.

**Verified at draft (not asserted):** `diff -r` of the two trees returns
**exactly one differing `.py` file** (`doctrine.py`) and **exactly one differing
line** (1228). `raid.py` is byte-identical between the arms
(md5 `ca31be16a0ac5cb2c1423527233922ef`), which is BY DESIGN and is the subject
of the Obligation-13 line below.

### Why this is not a re-run of SEALFLOOR0

`SEALFLOOR0` measured **0 vs 12** on the v125-era chassis against
`bots/_v197mapcode`. This arm measures **6 vs 0** on the v140 chassis against
the live incumbent. **Different contrast, different control, different chassis.**
The re-scoped #53 row's finding is the reason this arm exists: the floor was
explored **DOWNWARD ONLY** — the upward arm `SEALFLOOR24` was
**ALLOCATION-cancelled, not futility-dropped** — so **0 is not "the swept
optimum"; it is the only non-baseline value ever measured.**

---

## 2. REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen, ZERO live rated exposure; `tools/target_value.py`'s reachable-band question does not bind (no submit, no activation, no prototype exposure).**
**PINNED: N/A — local screen. The control is a byte-frozen local tree (`bots/_v223sealrepair`), so opponent churn cannot reach this shard; the pin/never-pin design rule governs PLATFORM legs only.**
**SURFACE: local**
**CLUSTER UNIT: none — enumeration in §3; both clusters die, applicable DEFF = 0.98 (local, measured)**
**ESTIMATOR: pooled game share = treatment wins / (rows − NOWINNER rows), unweighted, over `SEALFLOOR6.tsv` rows only. No map weighting, no seat weighting, no pooling with any other shard.**
**DOSE: seal-guard deferral window 6 Ti wide (treatment — the bank must reach cost+6) vs 0 Ti wide (flag-off control tree `bots/_v223sealrepair` — the bank need only reach cost) — the guard is `raid.py:270`, the constant `doctrine.py:1228`; n = 1 diff hunk, single-occurrence verified in both trees**
**PLANNED n: 5400 games**
**BOUNDARY: 5400 shard rows = 5400 games (LOCAL fixture: 1 game per row; the platform `games = 5 × accepts` identity has no accepts to close on here — declared exemption in §10)**
**CUT-SHORT: below n=1000 this shard publishes descriptive tallies only and takes NO comparative look; a futility drop at either gate publishes the label, the n and the share and makes NO claim about the constant beyond "not worth more cores now"**
**BAR: 51.33**
**BASE RATE: 50.0**
**BAR SOURCE: OB-F final band upper edge at n=5400 (= the 95% half-width, ±1.33pp, DEFF 0.98), the standing corefill screen band; identical construction to `SCREEN-sealsweep-2026-08-14.md` and `SCREEN-nestshot-2026-08-14.md`**
**BASE RATE SOURCE: structural null of a paired local screen — `tools/overnight.sh:95-110` plays every (seed, map) in BOTH seat orders (`ORD` A and B), so under H0 the expected treatment share is exactly 50.0. No historical population is consumed by the bar.**
**REFERENCE n: none — `SEALFLOOR0`'s finals are cited as a DIRECTION PRIOR only (§5) and are a comparator in no bar on this page**
**POOL ERA: local 15-map pool, `maps/*.map26` as read by `tools/overnight.sh:109-110`, post-patch geometry (valkyrie and glacierkeep rewritten 2026-08-14, file mtimes 14:53 and 09:01 local shell tz; the other 13 unchanged since 08-06). The `SEALFLOOR0` prior in §5 was measured on the SAME 15-map local pool but with PRE-patch valkyrie/glacierkeep — era-labelled, and one more reason it is a prior and not a comparator. The rated-tape pool boundary 2026-08-13T07:12:59Z bounds no number on this page, because no number on this page comes from the rated tape.**
**MECHANISM METRIC READS: raid.py:270 (`if LOKI_BARRIER_SEAL_ON and ti >= ct.get_barrier_cost() + LOKI_SEAL_TI_FLOOR:`). TREATMENT DIFF TOUCHES: doctrine.py (line 1228, the sole hunk). INTERSECTION: YES — via the constant import (§4).**
**GATE RESOLUTION: §6 — the band discriminates a true effect ≥ ~1.91pp at 80% power; UNRESOLVED (final inside 48.67–51.33) defaults to the RESTRICTION — the shipped constant 0 stays, the arm is not promoted.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock — the live tree ships floor 0 (`bots/_v223sealrepair/doctrine.py:1228`, verified at draft), the treatment value 6 appears in no shipped or previously-screened tree, and the 6-vs-0 contrast has never been measured on any fixture. There is no cell here that is pre-satisfied.**
**MAP SEGMENT: the 10 ≤676-area maps — antler, archipelago, auroraveil, drumlin, fjordgate, frostgate, icefloe, nordkap, royale, yulerune — versus the 5 900-area maps (drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie). MECHANISM: the floor binds only while the global bank sits in the 6-Ti window [cost, cost+6); that window is a FIXED ABSOLUTE 6 Ti while the bank grows monotonically with elapsed rounds (passive 10/4 plus harvester delivery), so the floor's dose is concentrated in the early, thin-bank rounds — i.e. where raiders reach the enemy spawn ring SOONEST relative to income. Approach length is the terrain property; area is its available proxy.**
**EXPECTED DIRECTION: NEGATIVE on-segment, ~ZERO off-segment — treatment share BELOW 50 on the 10 short-approach maps and ≈50 on the 5 900-area maps.**
**SEGMENT VALUE CEILING: 66.7% x 4.5pp on-segment = 3.00pp pooled**

### Proxy dilution, declared (Obligation 15's own warning, applied against this doc)

Obligation 15 says a mechanism-specific segment beats a size class *"whenever
the mechanism names a terrain property"*. **This mechanism names ROUNDS-TO-FIRST-
SEAL-OPPORTUNITY, and no per-map approach-length table exists in the repo at
draft time.** Map area is therefore a **declared proxy, and a proxy dilutes** —
the segment reads weaker than the true mechanism-specific split would. **The
cheap research item this names: a per-map core-to-enemy-ring distance table,
after which this segment should be re-declared on the real property.** Recorded
so a weak segment reading is not mistaken for a weak mechanism.

**EXACTLY ONE PRIMARY SEGMENT (15b).** Every other cut on this shard —
per-map, per-seat (`ORD` A vs B), the three-class CQ/STD/GRAND split, the
patched-vs-unpatched map pair — is **DESCRIPTIVE ONLY** and may not be used to
rescue a pooled fail. Named explicitly here so none can be promoted later.

**15c applies:** a pooled fail that CLEARS the pre-declared primary segment
in the predicted direction buys a **NEW screen with its own n** on that segment.
**The rows that suggested the segment may never confirm it.**

---

## 3. CLUSTER ENUMERATION (CLAUDE.md scope procedure, performed in writing)

1. **MATCH cluster — DIES.** A local shard has no 5-game match wrapper; each row
   is an independently seeded single game (`tools/overnight.sh:95` — `seed =
   SEEDLO + n/16`, one game per (seed, map, ORD) triple). No stratum can hold
   two games from one match because no match object exists.
2. **OPPONENT cluster — DEGENERATE.** Exactly one opponent
   (`bots/_v223sealrepair`) for all 5400 rows; no between-opponent contrast is
   drawn, so there is no multi-member opponent stratum to inflate.

⇒ **Applicable DEFF = 0.98** (local pair-weighted, ρ = −0.020, 124 shards, s39
audit). **The platform constants 1.529 / 1.833 are NOT imported** — doing so
would widen these intervals 24–35% for correlation that is not there.

⚠ **The one place this could bite:** the s39 audit found local outlier arms with
strong map interaction at DEFF ≈ 1.20–1.25, and this arm declares a map segment.
**The segment split is therefore INDICATIVE; a segment claim is banked only via
the 15c re-screen, never off these rows.**

---

## 4. OBLIGATION 13 — the intersection, stated exactly

```
MECHANISM METRIC READS:  raid.py:270
TREATMENT DIFF TOUCHES:  doctrine.py:1228  (sole hunk; raid.py byte-identical)
INTERSECTION:            YES — via the constant import
```

**The honest form, because the two files are different and that is the whole
point:** the metric's read site is `raid.py:270`, which is **byte-identical
between the arms**; the diff is in `doctrine.py:1228`, which **defines the value
that guard compares against**, bound by `raid.py:64` `from doctrine import *`.
**The diffed line IS the guard's threshold.**

**⛔ AND THIS IS NOT LOKI-18, which is the failure the obligation exists to
catch — the distinction is the VALUE, not the file.** LOKI-18's metric sat
downstream of a guard whose **behaviour could not differ** between arms, so it
read 100%/100% and could not have moved whatever the plank did. Here the guard's
**threshold differs by 6 Ti by construction**, so the guard's outcome differs on
every turn where the bank lands in the window. **A same-file check would have
passed LOKI-18's bar only if the constant had moved; a same-file check FAILS
this arm while the mechanism is live.** ⇒ **Flagged for the builder, not
resolved here: `tools/prereg_check.py`'s COMPUTED `OB13_INTERSECTION` compares
FILE PATHS, so it renders FAIL on a constant-carrying diff whenever a diff is
computable.** Run against this document at draft time it renders **WARN, not
FAIL** — and only because the arm tree `bots/_v238sealfloor6/` is **untracked**,
so `git diff --name-only HEAD` yields no path for it. **The pass is therefore
an accident of the tree's git state, not a verified intersection**, and the
FAIL arrives the moment the arm tree is committed. The general case — a constant
in `doctrine.py` consumed in `raid.py`/`eco.py` — is the majority of this
project's sweep arms. Triage item, filed as a finding rather than worked around.

---

## 5. DIRECTION PRIOR AND HYPOTHESIS (⚖ builder ratifies)

**⚖ HYPOTHESIS.** *A non-zero seal floor buys back more than it costs: holding
6 Ti of change defers a marginal seal in order to keep a peck (2 Ti) or a second
barrier affordable in the same window, and the deferred seat is usually still
free a few rounds later.* **If true, floor 6 beats floor 0 — an INTERIOR
OPTIMUM between the shipped 0 and the born 12.**

**⚖ EXPECTED DIRECTION (pooled): treatment share BELOW 50.0.** The only measured
point on this curve runs the other way — `SEALFLOOR0` (0 vs 12) came in
**ABOVE** 50 (**53.94 two-host pooled**, builder-handed; era-labelled in §2), i.e.
**lower floor won at the 12-Ti step.** The straight-line reading of that single
measurement is **monotone harm in the floor**, which predicts 6 loses to 0. **The
hypothesis above is the interesting alternative, not the base case, and this
prereg registers the base case as the expectation so that a win is a SURPRISE
and reads as one.**

**⚠ The prior is one point, on a different chassis, against a different control,
on a pre-patch map era. It orders the expectation; it does not size it.**

---

## 6. DESIGN, GATES AND THE DECISION RULE (⚖ builder ratifies the branch labels)

**Fixture.** `tools/corefill.sh` → `tools/overnight.sh`, full 15-map post-patch
pool, `--tle 10` wall-clock enforced (`overnight.sh:107-110`), `--replay
/dev/null`, both seat orders per seed. Worklist row, builder-handed:

```
SEALFLOOR6  bots/_v238sealfloor6  bots/_v223sealrepair  5400  308000
```

Seedbase 308000 is disjoint from every row in `scratchpad/corefill_work.txt`
(verified at draft: nearest neighbours 306000 and 302000; this shard consumes
308000–308337). Basenames `_v238sealfloor6` / `_v223sealrepair` do not collide
as substrings, so `corefill.sh:96`'s scoring refusal does not trigger.

**⛔ READ HYGIENE:** the shard key is **`SEALFLOOR6` exactly**. A `grep
SEALFLOOR` pools **`SEALFLOOR0`** (v125 chassis, control `_v197mapcode`) and
**`SEALFLOOR0R`** (its remote replication) — **a different contrast entirely**.
Any read that cannot show it matched the exact key is not a read of this shard.

**n and resolution.** n = 5400, p̄ ≈ 0.5, DEFF 0.98:

| quantity | in pp | **in games (of 5400)** |
|---|---|---|
| 1 SE | 0.68pp | 36.7 |
| **95% half-width** | **±1.33pp** | **±72** |
| **80%-power MDE** (one-sample vs 0.5, Z=2.802) | **≈1.91pp** *(quoted 2.0pp)* | **≈103** |
| OB-F final band | 48.67 – 51.33 | **2629 – 2771** |

**GATES (per `RULE-futility-gates-2026-08-13.md`, read ONCE each at first
crossing; the builder types the decision, the watcher never decides):**

* **GATE-1000 (n ≥ 1000): drop if share < 48.0% — i.e. ≤ 479 of 1000.** Label
  `FUTILITY-EARLY`.
* **GATE-2700 (n ≥ 2700): drop if share ≤ 50.5% — i.e. ≤ 1363 of 2700.** Label
  `FUTILITY-ALONE`.
* This is **not an ablation arm** (LOW does not determine the decision on its
  own — see the branch table), so the `DECISION-REACHED` clause does not apply.

**⚖ DECISION RULE (proposed; the branch labels are the judgment lines):**

| final at n=5400 | in games | branch |
|---|---|---|
| **≥ 51.33%** | **≥ 2772** | **OUTSIDE-ABOVE → KEEP-dev.** The interior-optimum hypothesis survives. Mandatory next step is **D26 replication** (seed 309000, scored alone, same-side pooling), and the kept-replay dose check of §8 is **OWED before any verdict sentence cites mechanism**. No ship implication: `SHIP_SIT` governs and v140 is sitting. |
| **48.67% – 51.33%** | 2629 – 2771 | **NO-INFORMATION → DROP, constant unchanged.** Per the pre-committed UNRESOLVED default: the restriction, never the permission. Written as *"the screen could not separate floor 6 from floor 0 at ±1.33pp"*, **never** as *"6 is equal to 0"* and never as *"0 measured better"*. |
| **≤ 48.67%** | **≤ 2628** | **OUTSIDE-BELOW → REAL NEGATIVE, road closes upward.** Floor 6 is worse than the shipped 0; combined with SEALFLOOR0's downward result this is two points consistent with monotone harm, and the never-run `SEALFLOOR24` arm is **not worth its cores**. #53's floor third is then ANSWERED (not merely stale) and the row re-scopes to timing + geometry only. |

**D26:** any final with |share − 50| ≥ 2.0pp (≤2592 or ≥2808 games) replicates
at seed 309000.

**⚖ KEEP-dev vs DROP, stated as the single sentence the builder ratifies:**
*only an OUTSIDE-ABOVE final keeps this arm alive; the band and everything below
it drop the arm and leave `LOKI_SEAL_TI_FLOOR = 0` shipped.*

---

## 7. THE KILL-ROUND RIDER (defence bar, scored as an EXCLUSION)

`PROGRAMME.md` `DEFENCE_ADMISSION_BAR: kill_round_non_regression` binds: the
seal is a defensive/denial asset and a floor that slows our own kill is
off-programme whatever it does to share.

**⚖ THE RIDER, in both units:** the arm passes iff the 95% CI on
**Δ median kill round (treatment − control)**, paired by seed,
**EXCLUDES +10 rounds** — **+10 rounds ≈ +5.7% of our 174-round median kill
round** (us-only, `CLAUDE.md`).

**⛔ RESTATED AS AN EXCLUSION BEFORE ANY DEFF IS APPLIED, per CLAUDE.md's
direction clause.** *"No significant rise in kill round"* is a fail-to-exclude
claim, and widening an interval makes that class of claim EASIER — DEFF applied
to the unrestated form would launder a weak null into a confident one. The bar
above is the exclusion form: **the CI must exclude the +10 regression**, and the
applicable DEFF is 0.98 (§3).

**UNRESOLVED ⇒ RESTRICTION:** if the CI cannot exclude +10, the rider does **not
pass**, and an OUTSIDE-ABOVE share does **not** promote the arm on its own.

**⛔ THE CONDITIONING TRAP, named before the read** (`tools/h2h.sh:194`):
`tools/overnight_read.py:556-558` prints *median kill round GIVEN a kill*, with
the kill counts beside it. A change in **which games end in a kill** moves that
median without anything getting faster or slower. ⇒ **The rider is reported as a
pair — P(core-kill win) AND median-kill-round-given-a-kill, both arms, with both
kill counts — or it is not reported.**

---

## 8. DOSE — what is verified, what is OWED, and its pre-declared direction

**VERIFIED AT DRAFT (code level, both verdicts):** the guard threshold at
`raid.py:270` is `barrier_cost + 6` in the treatment and `barrier_cost + 0` in
the control; single-occurrence constant, one hunk, both trees inspected. The
deferral window is **6 Ti wide vs 0 Ti wide**.

**⛔ NOT VERIFIED — DECLARED GAP, not discovered later.** The **behavioural**
dose (seals built/game, seal uptime = seat-rounds sealed / seat-rounds
available, first-seal round) is **NOT pre-measured**: this shard runs
`--replay /dev/null`, so it cannot produce those counters, and no probe shard
was run for this arm. **A kept-replay spot check (≥20 games per arm, replays
retained) is OWED before any verdict sentence from this screen cites
mechanism** — in either direction.

**⚖ PRE-DECLARED DIRECTION for that owed check, so it is falsifiable rather than
confirmatory** (builder-handed expectation, recorded as handed):

* **seals built/game: FLAT to SLIGHTLY DOWN** in the treatment;
* **first-seal round: LATER** in the treatment (the deferral is a timing shift);
* **seal uptime: FLAT to DOWN.**

**If the kept-replay check shows seals/game UP, or first-seal round EARLIER, the
dose is not the dose this document describes and the mechanism story is wrong
whatever the share did.** That is the anti-Goodhart clause for this arm.

**Scale note, because it bounds the dose a priori:** barrier cost is
`floor(scale × 3)`, so the window `[cost, cost+6)` is a **fixed absolute 6 Ti**
whose relative bite **shrinks as the global scale factor grows**. The dose is
therefore front-loaded in the game — which is the mechanism reason behind the
§2 segment and its expected sign.

---

## 9. COUPLING CLASS AND WHAT THIS SCREEN MAY CONCLUDE

**COUPLING CLASS (from #53's own row metadata): SELF-KNOWLEDGE / FIELD-UNIVERSAL**
— the seat geometry is ours, the spawn-ring pressure is universal ⇒
**screen-trustworthy at full weight**, which is exactly why a local shard is the
right instrument for this row and why no live window is spent on it.

**NOT LICENSED by this screen:**
* **No ship implication.** `SHIP_SIT` governs; v140 is sitting. An
  OUTSIDE-ABOVE final buys a D26 replication and a dose check, not an
  activation.
* **No combo claim.** This is a single-knob arm against the incumbent.
* **No claim about `LOKI_SALT_TI_FLOOR`** (still 12, `doctrine.py:1580`). Its
  comment's *"matches `LOKI_SEAL_TI_FLOOR`"* is stale prose today and stays
  stale after this shard whatever it reads; a salt-floor arm is a separate row.
* **No claim about seal TIMING or seal GEOMETRY** — #53's other two thirds,
  untouched here.

---

## FALSIFIER

**The hypothesis (§5) is falsified by any of:**

1. **A final ≤ 48.67% (≤ 2628 of 5400)** — floor 6 is measurably worse than the
   shipped 0, and the upward-floor road closes for values ≤ 6.
2. **A futility drop at either gate** (≤479/1000 or ≤1363/2700) — the arm is not
   worth more cores; no interior optimum is claimed at this resolution.
3. **A final inside the band** — the interior-optimum hypothesis is not
   supported at ±1.33pp; the shipped constant stays by the UNRESOLVED default.
   *(This is the modal outcome for a 6-Ti knob and is pre-typed as a drop, not
   as a null to be argued with.)*
4. **A kept-replay dose check showing seals/game UP or first-seal round EARLIER**
   — the mechanism is not the one described, and any share reading is
   unattributable regardless of sign.

**The PRIMARY SEGMENT prediction is falsified** if the treatment's share on the
10 ≤676-area maps is **≥** its share on the 5 900-area maps. *(A reversal — the
floor helping exactly where it binds hardest — is the surprise that would
promote the interior-optimum reading, and per 15c it buys its own screen with
its own n; it does not rescue a pooled fail on these rows.)*

---

## 10. OBLIGATIONS REGISTER (`docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md`)

* **Ob. 7 (PRE-STATE / outcome form):** satisfied — outcome is **game share IN
  OUR FAVOUR** on this shard, not a win-condition mix; the predicted-change set
  is verified not pre-satisfied (§2 `PRE-STATE`).
* **Ob. 8 (denominator rule):** single control, single fixture, single shard;
  the denominator is 5400 rows from one worklist row, pooled with nothing.
* **Ob. 12 (gate carries its resolution statement + pre-committed unresolved
  default):** satisfied in §6, including the explicit restriction default.
* **Ob. 13 (`file:line` + intersection):** satisfied in §4, **including the
  tool-level false positive it exposes**, flagged rather than worked around.
* **Ob. 14 (opponent version stability):** **N/A by shape** — the control is a
  byte-frozen local tree, not a platform cell. No `CELLS:` line exists.
* **Ob. 15a/b/c (map dependence):** satisfied in §2 with one primary segment, a
  signed direction, a recomputable value ceiling, an explicit descriptive-only
  list, and the proxy-dilution declaration.
* **Ob. 1–4, 6, 9–11:** Ouroboros/CAD-leg-specific or platform-mechanism-leg
  specific; they do not instantiate on a local single-knob screen. Stated rather
  than skipped.
* **⛔ NOT SATISFIED, and the reason is structural — `BOUNDARY` in accepts.**
  `tools/prereg_check.py`'s `BOUNDARY_UNITS` demands the boundary in **both
  accepts and games** with the platform identity `games = 5 × accepts`. **A
  local shard has no accepts**: one row is one game, and there is no 5-game
  match wrapper (which is also why the MATCH cluster dies in §3). The boundary
  is declared in the only two units it has — **5400 rows = 5400 games** — and
  the identity check **cannot close on this fixture**. Flagged as a
  local-fixture exemption the tool does not yet model, not as a waived
  obligation.
* **⛔ SECOND TOOL FINDING, from running the checker against an earlier draft of
  this page: `DOSE_BOTH_VERDICTS` PASSED OFF THE WRONG NUMBERS.** That draft's
  DOSE line opened with the read site `raid.py:270`, and `raw_number()` takes
  the **first float in each half of the `vs` split** — so the tool reported
  *"treatment 270.0 vs control 0.0"* and rendered **ok**, comparing a LINE
  NUMBER against a dose. **A guard that returns the right verdict off the wrong
  quantity has not checked anything** (CLAUDE.md instruments rule; Obligation 11
  in its general form). The DOSE line on this page is reworded so the parsed
  numbers are the actual doses (6 vs 0), and the parser's positional
  fragility is filed for the builder as a triage item.

## Target-value line

Local screen, zero live exposure ⇒ payout gate N/A (see §2 `TARGET BAND`).
