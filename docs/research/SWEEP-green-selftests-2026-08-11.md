# SWEEP — selftests that PASS while never exercising the definition the metric got wrong

**Side lane, 2026-08-11 04:3xZ** (`date`). Target nominated by the builder after
`ring_retention.py` was found to have passed its own selftest for its entire life
while inverting a result. Run by an opus subagent under a read-only boundary;
every mutant executed in scratch, **nothing in `tools/`, `bots/` or `docs/` was
edited**.

**THE REPORTING RULE, PRE-COMMITTED IN THE BRIEF:** no instrument is reported as
defective until **the specific input that PASSES its selftest and BREAKS its
metric has been constructed and run.** Suspicions without that case are listed
separately as leads. Every live number below carries the clock it was read at.

---

## THE SIGNATURE

**A test whose assertions all sit on one axis of a metric while the metric's
load-bearing definition sits on another.** Green exit, wrong quantity.
`ring_retention.py` asserts 12-tiles-on-open, 5-in-corner, walls-reduce — **the
ring geometry** — and never the **occupancy rule**, which was the broken part.

---

## F1 — `tools/audit_trigger.py` DIVIDES A 24-HOUR NUMERATOR BY AN UNWINDOWED DENOMINATOR, AND IS SUPPRESSING A FIRE

**Asserts:** that each of five rows *can* fire when fed a synthetic tripper.
**Does not assert:** that a row can stay **silent** on a healthy input, or that a
ratio's two sides share a window. The numerator is `git log --since=24.hours`;
the denominator is `results.tsv` rows `[-50:]` — **a row count with no clock at
all.** `results.tsv` has no timestamp column, so the tool cannot ask.

**Constructed case — and it is the LIVE state, not a hypothetical:** a builder
tape that stops being appended while docs keep landing.
```
results.tsv        33.9 h stale, 0 commits touching it in 24 h
docs/*.md in 24 h  53
LIVE:   [ ok ] cross-lane analysis 2.52  ->  "OK — 1/5 tripped; audit not indicated."
SAME WINDOW BOTH SIDES:  53 / 0  ->  53.0  vs threshold 4.0  ->  TRIP
```
With `ship cadence` already tripping that is **2/5 = FIRE** — the exact
*"many documents, no decisions"* state the row exists to detect. The selftest
cannot see it because its fixture is a **one-row tape**, where tail-window and
time-window coincide degenerately.

**`note:verdict` and `stuck_planks` read the same frozen tail**, and
`stuck_planks` uses `rows[-60:]` with no window — **the identical defect
`ship_cadence`'s own docstring says was found and fixed in s20 and left
uncorrected in its sibling.** None of the three reports the tape's age, in a repo
whose standing rule is *"a monitor that reads a file must report that file's
FRESHNESS."*

**Cost:** named in 11 docs and wired into `.claude/commands/builder.md` step 4 —
**it runs on every builder boot.** The audit-summon mechanism has been disarmed
for as long as the tape has been frozen.

## F2 — `tools/oppver_window.py` RETURNS **CLEAN** ON A STALE TAPE, AND CLEAN IS THE VERDICT THAT CERTIFIES D18

**Asserts:** `classify()` driven to all three verdicts — STRADDLED / CLEAN /
UNKNOWN. Correct in shape. **Does not assert:** anything about `timeline()`, the
function that builds the timeline from `corpus/league_matches.tsv`, or about that
file's freshness. `_OVERRIDE["timeline"]` bypasses the reader, so **the tape is
never in the test.**

**Constructed case (real tape, no override), newest row 62 min stale:**
```
Lunds Stallions  versions_on_tape=52 -> ('CLEAN','v64 throughout (52 versions on record all-time)')
The Bisons       versions_on_tape=4  -> ('CLEAN','v4  throughout')
0033             versions_on_tape=42 -> ('CLEAN','v50 throughout')
```
**Lunds Stallions is the docstring's OWN worked example of a cell shipping six
versions in eighteen hours**, reading `CLEAN` in a sentence that simultaneously
reports 52 versions on record. `main()` then prints *"no cell shipped inside the
window — D18 satisfied for this leg"* and exits 0. **The tool HAS an `UNKNOWN`
verdict and a docstring insisting UNKNOWN is not CLEAN; a stale tape routes
straight past it.**

**Second, smaller branch:** a version whose first *ladder* sighting lands after
the window end reads CLEAN rather than UNKNOWN. **Adversarially sized before
reporting:** across **2,729 league-wide version transitions** the gap between
last-game-on-old and first-on-new is **median 10.0 min, max 20.3 min, 0/2,729
over 60 min** — so this is a ~10-20 min tail, a footnote. **The stale-tape branch
is the serious one.**

## F3 — `tools/map_admits.py`'s GEOMETRY CONTROL DOES NOT TOUCH THE CODE THAT COMPUTES THE RING

**Asserts:** `classify()` to every flag and to silence; a fingerprint MISS on a
one-tile flip; and `open-terrain ring = 12`. **Does not assert:** anything
computed by `map_facts()`, the function that actually produces `rings`/`edges`.
The control builds its own set comprehension **inside the selftest body**;
`map_facts` is never called and `edges` is never exercised.

**Constructed case — the historical orthogonal-8 bug reintroduced into
`map_facts` in a scratch copy:**
```
[ok] open-terrain ring = 12
PASS: every flag fires on its own shape and stays silent otherwise ...
exit=0
```
while the tool's real output inverts on every panel map:

| map | real | mutant |
|---|---|---|
| fjordgate / atoll / saga / snowflake | 12/12 | **8/12 RING CLIPPED** |
| jackpot | 5/12 CLIPPED | 4/12 CLIPPED |

Every map flips to *"ring-hold planks are UNDEFINED here"* — the verdict that
retires a plank's whole fixture — **with the selftest green.** The docstring says
the 8-ring bug *"was caught only by checking against a number derived
independently by another lane"*; **the control then written does not re-run that
check.** Blast radius: `leg_read._ring_sizes()` imports it and drives the
`BY RING STRATUM` split; 6 doc mentions; D34 and LOKI-16's stratification.

## F4 — `tools/monitors/breakin_watch.py` VERIFIES A PRIVATE COPY OF `main()`, NOT `main()`

**Asserts:** breach / silence / blind — all three, right shape. **Does not
assert:** that `main()` contains any of them; `selftest.run()` re-implements the
floor comparison and the staleness branch inside itself.

**Constructed case — freshness branch DELETED from `main()` in a scratch tree:**
```
[ok] blind:  BLIND: tape unwritten for 0 min.
SELFTEST PASS   exit=0
```
**The blindness case passes with blindness detection removed from the running
monitor** — and blindness detection is the monitor's entire stated reason for
existing.

**Same family, worse:** `ship_watch.py` has a rich selftest (7 fixtures, both
SPRT bounds, a restart-on-OK regression) and **no freshness assertion anywhere**.
Its line carries `datetime.now()` — the PRINT time — never the age of the newest
tape row, and its fixtures are dated `2026-01-01`, seven months stale, every case
accepting them as live. **This is the incident `CLAUDE.md` records verbatim and
it is still unenforced.**

## F5 — THE PUBLISHED **CAUSE** OF THE KIDNAP-ZERO COLUMNS IS WRONG, AND THE "HEALTHY HALF" IS DILUTED 24%

Neither `corpus_sanity.py` nor `corpus/replay_throws.py` has a selftest.

**Published claim** (HANDOVER + night-panel doc): the columns are zero for
kidnaps because they key on the thrown bot's own enemy, so `core_atk` counts the
enemy hitting OUR core.

**Constructed test — split `throws.tsv` on `kind` instead of on team, 274,958
live rows:**
```
EXILE    171825  reached 0.00%   any_atk 0.00%   core_atk 0.00%
INSERT    77679  reached 22.68%  any_atk 10.58%  core_atk 2.25%
RETREAT   24201  reached 0.00%   any_atk 0.00%   core_atk 0.00%   <-- SAME TEAM
UNATTRIB   1253  reached 0.00%   ...
```
**RETREAT is same-team and identically zero across 24,201 rows. Team keying
cannot explain that.** Real cause, `replay_throws.py:134`:
`if kind == "INSERT": active[eid] = rec` — **only INSERT rows ever enter
`active`**, and both the `builderAttack` handler and the `reached` loop are gated
on it. For every non-INSERT throw **the columns are never computed at all**; the
team-keying line at :157 sits downstream of a gate never passed. **Re-keying
`foot[1-b.team]` would change nothing.**

**And `conditionally_dead()` — the check written to catch exactly this — splits
on `tteam == bteam`**, pooling the structurally-dead RETREAT rows into the half
it prints as healthy: published **17.29%** against a true INSERT rate of
**22.68%**. **The check committing the defect it was built to catch, one level
up.**

**⚠ SIDE-LANE SELF-CHECK, RUN BEFORE PUBLISHING THIS:** my own morning cuts used
`tteam == bteam`. Re-run under `kind == "INSERT"` for our v104 they are
**identical** — unrated 250/1247 = 20.0%, rated 98/246 = 39.8% either way. **The
dilution is real corpus-wide and does not reach my numbers.** Verified rather
than assumed, because the correction would have run in the direction that kills a
good leg.

## F6 — `ring_retention.py` IS STILL LIVE IN HEAD, AND THE INFLATION IS MEASURED

Not a discovery — the calibration case — but it is **present in HEAD, not
historical**. Re-run on 60 random archived games:
```
as shipped (no entity-kind filter)          : 0.284
with the builder-bot filter its docstring promises : 0.139
inflation                                    : +0.144  (103% high)
```
**Against a pre-registered bar of `>= +0.15`, the shipped tool reads 103% high.**

---

## LEADS — no constructed failing case yet, and what settles each

* **`leg_read.py:146-149` collapses the seat mix**: `seats.setdefault(opp, seat)`
  keeps the FIRST seat seen, so an opponent played in both seats prints as one
  letter — **in a function whose docstring exists to make the seat mix visible
  rather than assumed.** *Settles it:* one archived leg with the same opponent in
  both seats, diffed against per-match `teamAId`.
* **`target_value.py::_live_ratings()`** is bypassed by `_OVERRIDE["ratings"]`
  and takes each opponent's rating from their most recent match — **one match
  stale** — while overriding OUR rating with live `fcode status`. **Every printed
  gap is mixed-epoch by up to ±32 points, ~25% of the reachable band width.**
* **`loki9_facing.py`** asserts its primitives to both verdicts but never the
  census loop, whose three named traps are the load-bearing definitions;
  **`HUNT_BAND_DSQ` decides which turrets count at all and has never been driven
  to both verdicts.**
* **`crash_census.py`** (selftest not runnable read-only): the positive control
  only exercises `builder_bot`; the negative control cannot distinguish *"the
  detector correctly ignores friendly `destroy()`"* from *"this bot never calls
  it"* — a degenerate fixture for the exact ambiguity its docstring names.
  **`CLAUDE.md`'s published `2,451 unexplained removals ... against 0 by us`
  drops that caveat.**

## CLEAN — and this list is worth as much as the findings

**`corpus/meta_attrib.py` is the model.** Three corruption modes, each aimed at a
**different** check, each mutating **the real pipeline's own rows**, each
requiring agreement to COLLAPSE. Its third mode exists because the first two only
proved CHECK 1's teeth — **it reasons about which check each corruption reaches**,
which nothing else here does.

Also clean: **`score.py`** (both sides of every bucket boundary; tiebreak
asserted *identical* to a loss — the semantic, not a number; balance property as
an invariant), **`rate_budget.py`** (**the blind state must REFUSE, not permit**),
**`claim_check.py`** (includes the historical miss as a case), **`plank_status.py`**
(drives OK→STALE→OK→STALE on the real `check()`, and asserts an unrelated edit
does **not** clear the alarm).

**What the clean ones share: they call the PRODUCTION function; they assert
semantics rather than shape; they drive the check to the verdict that is
UNCOMFORTABLE; and each case names the incident that created it.**

## THE CATEGORY THAT MAY BE WORSE THAN ANY FINDING

**41 of 56 `__main__`-bearing modules under `tools/` have no selftest at all.**
Decision-bearing ones: **`replay_census.py` (84 doc mentions**, the shared wire
primitives every corpus decoder imports — one defect moves every number in the
repo), **`leg_read.py` (13)**, **`corpus_sanity.py` (9)**,
**`corpus/replay_throws.py` (8)**, **`gate.py`** (an enforcement instrument never
observed to refuse), **`slot_rule.py`/`slot_sprt.py`** (the stop-loss itself,
tested only indirectly), **`elo_logger.py`**, **`preflight.py`/`submit_clean.py`**.

## WHAT WAS NOT CHECKED — silence here is not clearance

Not run: `crash_census --selftest` (invokes `fcode run`), `breakin_watch`/
`ship_watch` un-flagged (they write into `corpus/`). Read but no failing case
constructed: `slot_rule`, `slot_sprt`, `sprt`, `gate`, `preflight`,
`submit_clean`. **Not opened at all:** `arena.py`, `tune.py`, `det.py`, `pair.py`,
`treehash.py`, `reprice.py`, `ceiling.py`, `collar_census.py`, `field_deaths.py`,
`tle_census.py`, `make_map.py`, `mech_battery.py`, `loki17_mech.py`,
`game_census.py`, `ladder_census.py`, most of `tools/corpus/`, and monitors
`match_watcher`, `opp_watcher`, `replay_archiver`, `sweep_watcher`,
`window_watcher`. **The `.sh` runners were grepped, not read.** **And it was not
verified that the fixes implied by F1-F6 are correct — only that the tests cannot
currently distinguish correct from broken.**
