# SCREEN PREREG — `bodyaware` (QUEUE #63): the builder BFS learns that bodies block

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies and commits; this
agent wrote no code under `bots/`, appended no shard row, and fired no game
other than one throw-away local replay used to drive the CPU-instrument check in
§7 (written to the session scratchpad, never to the repo).

**STATUS: committed BEFORE the `BODYAWR` shard is appended to
`scratchpad/corefill_work.txt`, BEFORE `bots/_v242bodyaware` exists on disk, and
BEFORE its first game.** Two-clock form: this commit's git author time against
the shard tape's own `# FIXTURE … start=` stamp, which `tools/overnight.sh:100`
writes before the first game (a START, not a first-completed-row). Drafting
session wall clock at write time: **`2026-08-14T23:43:21Z`** (`date -u`), repo
HEAD `cf09255 2026-08-15T01:42:34+02:00`.

---

## ⛔⛔ READ THIS BEFORE RATIFYING — THE DESIGN'S OWN SEPARATION CONTROL FAILED, AND IT COSTS THIS PREREG ITS HEADLINE

`docs/research/DESIGN-63-long-approach-arrival-2026-08-14.md` §4 wrote its fifth
falsifier before the data existed: *"C1 must be materially lower [on
valkyrie/glacierkeep] than on midgard. If C1 is equally high on our best maps,
the indicator is measuring something that does not track outcome and it
validates nothing — the constant-column failure."*

**IT CAME OUT THE OTHER WAY.** Exposure-normalised C1 as a share of ALL nav
rounds, all four maps 30×30, 88 games each
(`scratchpad/c63_probe_s43/report_all.txt`):

| map | role in the design | **C1 % of all nav rounds** | 95% CI |
|---|---|---|---|
| **ragnarok** | primary (long-approach) | **28.4%** | [24.7, 31.3] |
| **glacierkeep** | CONTROL (one of our BEST cells) | **19.3%** | [15.7, 23.6] |
| **midgard** | primary — the map `#63` is NAMED for | **13.7%** | [12.5, 15.0] |
| **valkyrie** | CONTROL (one of our BEST cells) | **12.6%** | [10.8, 14.5] |

**midgard is statistically indistinguishable from valkyrie and LOWER than
glacierkeep.** The indicator does not order the maps the way the outcome
deficit does — it inverts inside the primary segment itself.

**⇒ THREE CLAIMS ARE BARRED FROM THIS DOCUMENT AND FROM ANYTHING BANKED OFF IT:**
1. **That BODYAWARE fixes the midgard deficit.** midgard is the LOWEST-dose cell
   of the four. Nothing here supports it and the probe actively contradicts it.
2. **That BODYAWARE moves the 3.3× ours-vs-theirs lock ratio.** The probe reads
   OUR tree only; opponents' internals are unreadable. The design said this in
   §2 before any row existed and it is inherited unchanged.
3. **That `#63`'s inherited segment `{midgard, ragnarok}` is this arm's segment.**
   It is RETIRED here, with the reason on the page. See "RATIFY: Segment".

**WHAT SURVIVES, and it is the design's own stated fallback: ABSOLUTE
BUILDER-ROUNDS RECOVERED.** §2 of the design: *"the arm must be justified by the
absolute builder-rounds it recovers, never by the ratio."* That is the whole
case this prereg makes, and it is a large absolute number: **21.8% of every nav
round we play proposes a first step the move layer refuses because a builder bot
is standing on it.** A defect that fires on one nav round in five, pooled, is
worth a screen even with no map story attached — and having no map story is a
strictly weaker, more honest claim than the one the row was written on.

---

## RATIFY: Hypothesis

**Adding builder-bot positions (both teams) to `_bfs_direction`'s `blocked` set,
with ONE body-free retry when the body-aware search finds no goal, raises our
LOCAL game share against the shipped v140 tree (`bots/_v223sealrepair`) to
51.93% or higher, POOLED over the 15-map corefill pool at n = 10,800 games.**

The channel is `R1000_IS_DEFEAT`-compatible and offensive, not defensive: a
builder that stops proposing a step it cannot take arrives sooner, so the
predicted surface reads are **fewer `tiebreak` rows and a lower median
`core_destroyed` turn count**, both registered as secondary columns below.

**EXPECTED DIRECTION: POSITIVE** (pooled; no segment is claimed).

⛔ **AND THE HYPOTHESIS HAS A CREDIBLE OPPOSITE, WHICH IS WHY IT CAN FAIL.**
Bodies are transient. Today a refused step costs one round and the perpendicular
fallback succeeds **87.1% of the time**; BODYAWARE instead commits the BFS to a
body-free route that may be strictly LONGER than standing still for one round
while the blocker walks on. **If waiting beats detouring, this arm costs game
share and slows the kill.** That is not a hedge — it is the falsifier, priced
below.

---

## THE CHANGE — `file:line`, old → new

**TREATMENT TREE: `bots/_v242bodyaware`** — a byte-for-byte copy of
`bots/_v223sealrepair` (v140 "Loki v10") apart from one function.
**Only `eco.py` changes; `diff -rq` must name exactly one file.**

`bots/_v223sealrepair/eco.py:809-896`, `_bfs_direction`. Four hunks:

**(1) `eco.py:829-833` — the blocked tuple gains the only mobile occupant, into
its own set so pass 2 can remove it.**
```
  OLD (:826-833)
                ep = ct.get_position(eid)
                if et == EntityType.CORE:
                    blocked.update((c.x, c.y) for c in core_tiles(ep))
                elif et in (
                    EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
                    EntityType.HARVESTER, EntityType.BARRIER,
                ):
                    blocked.add((ep.x, ep.y))

  NEW
                ep = ct.get_position(eid)
                if et == EntityType.CORE:
                    blocked.update((c.x, c.y) for c in core_tiles(ep))
                elif et == EntityType.BUILDER_BOT:          # BODYAWARE (#63)
                    bodies.add((ep.x, ep.y))                # both teams
                elif et in (
                    EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
                    EntityType.HARVESTER, EntityType.BARRIER,
                ):
                    blocked.add((ep.x, ep.y))
```

**(2) `eco.py:815` and `:837` — declare and clean the new set.**
```
  after :815  blocked = set(self.map_walls)
  NEW         bodies = set()                    # BODYAWARE (#63)

  after :837  blocked.discard(start)
  NEW         bodies.discard(start)
```

**(3) `eco.py:865-874` — hoist the `order` construction ABOVE the two-pass loop.**
Pure code motion; `desired`/`side`/`order` do not depend on `blocked`, so this
changes nothing and exists only to keep the diff to one loop.

**(4) `eco.py:839-896` — wrap goal construction + BFS in a two-pass loop; the
two `return p.cardinal_direction_to(target)` failure exits become `continue`.**
```
  NEW  for _pass in (0, 1):
           if _pass == 1 and not bodies:
               break                       # no bodies -> pass 0 WAS today's search
           blk = (blocked | bodies) if _pass == 0 else blocked
           <existing :839-859 goal construction, every `blocked` -> `blk`>
           if start in goals:
               return Direction.CENTRE
           if not goals:
               continue                    # was :863 `return p.cardinal_direction_to(target)`
           <existing :875-895 BFS, every `blocked` -> `blk`>
               # :881-882 CPU guard UNCHANGED: `return p.cardinal_direction_to(target)`
           # queue drained without a goal
           continue                        # was :896 `return p.cardinal_direction_to(target)`
       return p.cardinal_direction_to(target)
```

### Two implementation points the design leaves implicit — DERIVED FROM ITS OWN INVARIANT, not chosen

The design's guarantee is: *"where a body-free detour exists it is taken; where
none exists, behaviour is byte-identical to today."* That invariant uniquely
determines both open points, so neither is a redesign:

* **The retry fires on BOTH failure paths** — empty `goals` (`:862`) and a
  drained queue (`:896`). Both are "the body-aware world model produced no
  route"; retrying on only one leaves the other reaching today's greedy step
  through a strictly worse world model, which is the naive-version death the
  design names.
* **The retry does NOT fire on CPU exhaustion** (`:881-882` keeps its `return`).
  The design's COST paragraph says the degenerate case *"degrades to today's
  greedy step rather than to a timeout"* via that guard — an abort is not a
  finding of "no route", and letting it trigger a second full BFS would double
  the cost precisely where the budget already ran out.

⚠ **RATIFIER'S CALL:** if the lane reads either point differently, change it
here BEFORE the tree is built. This document is the spec the tree is built to.

---

## STOP CONDITIONS — the three the brief demands, answered

**1. IS THE CHANGE ALREADY IN THE TREE? NO — verified by grep, not by memory.**
`grep -rn "BUILDER_BOT" bots/_v223sealrepair/eco.py` returns **exactly one hit,
`eco.py:292`**, inside an unrelated unit filter. `EntityType.BUILDER_BOT` does
not appear in `_bfs_direction` (`:809-896`) or anywhere else in the navigation
path. `grep -rn "_bfs_direction" bots/_v223sealrepair/` returns the definition
(`eco.py:809`), the single call site (`eco.py:901`, inside `_nav`), and two
comments (`doctrine.py:479`, `:593`). **One definition, one live call site — this
is a BEHAVIOUR, not a dead spec, and the behaviour we want is absent.**

**2. MECHANISM OCCURRENCE — MEASURED, AND IT AGREES WITH THE TREE.** The probe
(§below) says the FIRST refused step is a builder-bot tile in **67.6% of
refusals / 21.8% of all nav rounds**. That is exactly what `eco.py:829-833`
predicts: every other blocking class IS in the tuple, so the omitted class
should dominate the refusals. It does. **No disagreement between the source read
and the measurement.**

**3. LATER RULINGS ON THIS ROW — grepped, not assumed.** `grep -n` over
`docs/coordination.md` for `#63` / `BODYAWARE` (never reading the file whole)
returns the design delivery (`:50833-50851`), the segment-value line
(`:51938-51952`), and one live routing note at **`:52001`: "HELD … the plank is
worth at most ~2pp pooled, so it should not jump a leg that can pay more."**
**The row is HELD-not-killed.** ⇒ **This prereg is a candidate for a free
overnight slot, not a queue-jump.** At draft time `scratchpad/corefill.log`
reads `running=2/8 … unstarted=0` — six worker slots idle — which is the
condition under which a held row is the right thing to fire.

---

## DOSE — the probe, its negative control, and what is NOT yet dosed

**DOSE: the first refused nav step classifies as BUILDER-BOT-ON-TILE in 67.6% of refusals (102,707 / 152,042) vs 0.02% for the CONVEYOR/SPLITTER negative-control class (14 / 61,346) read by the same classifier on the same rows (n = 352 games, 471,812 nav rounds, incumbent `bots/_v223sealrepair`, 2026-08-14, `scratchpad/c63_probe_s43/report_all.txt`).**

**The probe drove FOUR verdicts, not one, which is what makes it a check:**

| drive | reading | verdict it produced |
|---|---|---|
| **C0 premise control** (design §4's first falsifier) | `can_move` into an occupied tile **False in 1000/1000 rounds**; `can_move` into a verified-EMPTY adjacent tile **True in 1000/1000**, same bot, same turn | **BOTH verdicts from one instrument.** F2 stands: the move layer refuses a body tile |
| **C1** (the addressable class) | **67.6%** of refusals | the dominant class |
| **belt negative control** | CONVEYOR/SPLITTER **0.02%** of refusals | the classifier CAN return ~0 — it is not a constant column |
| **out-of-bounds control** | **0.0%**, and *"refused, tile reads FREE"* **0.5%** | the accounting closes; the residual unexplained refusal rate is half a percent |

Accounting: the report's own header states **"all 5 identities hold on every
row"**, and the instrumented tree won **178/352 = 50.6%** of its self-play games
— **the instrumentation is not costing games.**

**⛔ WHAT IS *NOT* DOSED, STATED PLAINLY: THIS IS A POPULATION PROBE ON THE
INCUMBENT, NOT AN ARM-VS-ARM DOSE.** No treatment tree exists, so nobody has yet
shown that BODYAWARE *reduces* C1. That read is registered as a **PRE-FIRE GATE**
below and the shard may not be scored until it passes. Treating the population
number as delivery evidence is the exact substitution the dose-probe rule exists
to stop.

**⛔ AND THE SELF-PLAY CAVEAT, carried forward rather than quoted away.** The
probe fixture is self-play, so the **27.0% ENEMY-body half of C1 is a property of
playing ourselves** and will not transfer to the ladder unchanged; only the
**friendly 40.5% of refusals = 13.1% of all nav rounds** transfers cleanly.
**The LOCAL screen registered here has the same structure, so both halves are
live inside it and the local addressable share is the full 21.8% — which means a
positive local reading OVERSTATES the ladder value of this arm by up to ~1.7×,
and that discount is owed to any ship decision taken off it.**

---

## Instrument, fixture and units

* **SURFACE: local** — corefill shard, `tools/corefill.sh` + `tools/overnight.sh`,
  `--tle 10`, `--replay /dev/null`, 15-map pool, both seat orders.
* **CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted.
  **MATCH cluster:** corefill has no 5-game matches; one row is one game on its
  own seed, so a stratum cannot hold two members of a match — **dead**.
  **OPPONENT cluster:** every row is played against the same single control tree
  on disk, so opponent is a constant carrying no between-cluster variance —
  **dead**. Applicable design effect is the measured local constant **DEFF =
  0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit).
  ⛔ The platform constants (1.529 rated / 1.833 unrated) are NOT applied:
  over-applying a correction is an error in the same family as omitting it and
  would widen every interval here by 24–35% for correlation that is not present.
* **ESTIMATOR: unweighted treatment game share** = rows with `winner == T` over
  all non-comment, non-`NOWINNER` rows of `scratchpad/overnight/BODYAWR.tsv`.
  One local row is one game, so game share and win rate are the same number on
  this fixture; the "win rate is not a verdict" rule governs MATCH win rate on
  the platform and does not reach here.
* **PINNED: N/A — local self-play.** The opponent version is fixed by
  construction (a directory on disk), so there is nothing to pin and no opponent
  churn to absorb.
* **TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input.** The rated-value question this arm must answer LATER is priced in the design's §5 line (≤ ~2pp pooled on the rated ladder) and is what the CPU gate below is weighed against.
* **POOL_ERA: post-2026-08-13-rotation** · **POOL ERA: post-2026-08-13-rotation**
  (both spellings deliberately — the underscore form is the lane's, the spaced
  form is what `tools/prereg_check.py` parses). The 15-map pool at
  `tools/overnight.sh:68`: antler archipelago auroraveil drakkarfjord drumlin
  fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale
  valkyrie yulerune.
* **SPANS-POOL-CHANGE: no** — the shard starts and ends inside the current pool
  era, and the probe it is gated on was itself run entirely on new-pool maps.
* **CELL VERSION CHURN: N/A — not a panel.** There are no opponent cells: one
  control tree, pinned by being a file. No churn exists to count.

**Shard line to append to `scratchpad/corefill_work.txt`:**
```
BODYAWR     bots/_v242bodyaware    bots/_v223sealrepair   10800 336000
```

**BASENAME-COLLISION CHECK, BOTH DIRECTIONS** (`tools/overnight.sh:78` refuses
on `$B == *$C*` **or** `$C == *$B*`, because scoring is a SUBSTRING match on the
`Winner:` line and a one-way check reads ~100% for the treatment):
* `_v242bodyaware` contains `_v223sealrepair`? **NO.**
* `_v223sealrepair` contains `_v242bodyaware`? **NO.**
* `ls bots/ | grep -iE "bodyaware|_v242|_v243"` → **empty**, so no existing tree
  can collide with the new basename either.
* Shard-name collision (file paths in `scratchpad/overnight/`, both directions):
  `BODYAWR` contains no existing shard name and no existing shard name contains
  `BODYAWR` — `grep -iE "BODY|BDY|AWR"` over the shard column of
  `scratchpad/corefill_work.txt` and over `ls scratchpad/overnight/` returns
  **empty**.

**SEED BASE 336000, span 336000–336674.** `tools/overnight.sh:121` advances the
seed every 16 games, so 10,800 games consume 675 seeds. The probe burned
330000–335999; the highest live base in the worklist is **314000 (`SENTTHR`)**.
**No overlap in either direction.**

---

## RATIFY: Decision rule

* **PLANNED n: 10800 games** (two standard shards' worth on ONE tape and ONE
  seed base; 10800 = 15 maps × 2 seats × 360, so map/seat balance is exact).
* **BOUNDARY: 10800 games** — LOCAL surface, one row is one game; there are no
  accepts and no attempt/accept distinction to miscount.
* **BASE RATE: 50.00%** — the structural A/A expectation of a seat-balanced
  self-play shard.
* **BASE RATE SOURCE:** `NULL125` (`bots/_v198null125`, a renamed byte-identical
  copy of `_v197mapcode`, against `_v197mapcode`), **51.04% ±1.32 at n = 5,400 on
  this same 15-map pool** (`scratchpad/overnight/NULL125.result_cache`). Its
  interval 49.72–52.36 contains 50, so 50.00 stands as the comparator — **but the
  null cell ran ~1pp HIGH and there is no null cell on the v140 chassis itself,
  so a marginally-clearing KEEP is the reading most exposed to that residual.**
  Disclosed, not corrected.
* **BAR: 51.93% or higher** on the treatment arm's pooled game share at n = 10,800.
* **BAR SOURCE:** constructed, not observed — `50.00 + MDE(1.00pp) + half_width(0.93pp)`.
  Half-width recomputed here as **±0.933pp** from `1.96·sqrt(p̄(1−p̄)·0.98/10800)`
  at p̄ = 0.50965. **Clearing this bar means the 95% interval excludes BOTH 50.00
  AND the indifference threshold below it** — which is the point of putting the
  MDE inside the bar rather than beside it.
* **REFERENCE n: none** — the comparator is generated inside the same shard from
  the same seeds, so no fixed external reference contributes a variance floor.

### ⭐ THE PRE-SPECIFIED MDE, AND HOW IT WAS CHOSEN — sized off the value we must EXCLUDE, never off one we hope to observe

**MDE: +1.00pp. WE WILL CALL THIS ARM A MISS IF ITS TRUE LOCAL EFFECT IS AT OR
BELOW +1.00pp OF GAME SHARE.**

**There is no observed point estimate to size off, and that is deliberate** — the
treatment tree does not exist, so nothing in this document can be circular. The
indifference threshold comes from the arm's PRICE, which is knowable before any
row:

> **BODYAWARE doubles a BFS on the hot path of a chassis measured at 8,847 µs of
> a 10,000 µs per-unit budget, watched by an alarm that fires at 9,200 µs**
> (`corpus/cpu_watch.log`, `tools/monitors/cpu_watch.py:41`). **That is ~353 µs
> of headroom to the alarm and ~1,153 µs to the ceiling — 3.5% and 11.5%.** An
> arm that buys less than a point of game share does not justify spending that
> margin, whatever its p-value.

**The sizing then follows mechanically rather than being negotiated:**

| quantity | value at n = 10,800, DEFF 0.98 |
|---|---|
| σ (game share) | **0.4763pp** |
| 95% half-width | **±0.933pp** |
| smallest excluded effect at the bar | **1.00pp** |
| effect detected with 80% power | **≥ 2.41pp** |
| n needed to EXCLUDE 1.00pp (half-width < 1.00) | **9,412** ⇒ 10,800 is the next balanced multiple of 30 |
| n needed to DETECT 1.00pp at 80% power | **19,230** — NOT bought, and this leg does not claim it |

**⇒ WHAT THIS LEG CAN AND CANNOT DO, in one sentence each.** It can separate
"worth more than a point" from "worth a point or less". It **cannot** distinguish
"worth 0.6pp" from "worth nothing" — that needs 19,230 games (3.6 standard
shards) and is not what is being bought. A ratifier who needs the sub-point
question answered should not fire this; they should budget four shards.

⚠ **The cheaper alternative, priced so the choice is deliberate:** a single
5,400-game shard gives ±1.320pp, which forces the bar to **52.32%** and drops
80%-power detection to **≥ 3.20pp** — a bar this arm has no reason to clear.
**10,800 is the smallest n at which the registered MDE is expressible.** Six
worker slots are idle at draft time, which is why the larger leg is the right
call tonight and might not be tomorrow.

### THREE BRANCHES, pre-committed

1. **KEEP — share ≥ 51.93%.** BODYAWARE is worth more than a point of local game
   share. The arm goes to a combo/ship decision, **gated on the CPU release gate
   in §7, which it does not automatically pass.**
2. **REAL NEGATIVE — share ≤ 49.07%.** The interval excludes 50 downward:
   BODYAWARE COSTS us. The detour-beats-waiting hypothesis wins, `#63`'s
   navigation road narrows to DESTINATION changes only, and the F1 omission at
   `eco.py:829-833` is reclassified from defect to **deliberate-and-correct**.
   ⚠ **The negative branch is intentionally NOT symmetric with the positive one**
   (0.93pp below 50 against 1.93pp above): a credible harm kills an arm that also
   costs CPU, so no indifference margin is granted on the downside. Stated here
   rather than discovered in the analysis.
3. **DROP BAND — 49.07% < share < 51.93%: COULD NOT SEPARATE.**
   ⛔ **Written as "the screen could not separate the effect from the ≤1.00pp
   indifference region at ±0.93pp on this fixture", NEVER as "the effect is
   zero".** The mechanism has a measured population of 21.8% of nav rounds; an
   inside-band reading bounds the arm at roughly ≤1pp locally and says nothing
   about the ladder, where the addressable share is up to 1.7× smaller.

* **CUT-SHORT: floor 5400 games.** Below 5,400 rows nothing is read and no branch
  is claimed; the rows are KEPT and remain poolable with a later completion of
  the same shard on the same seed base, and with nothing else. At
  5,400 ≤ n < 10,800 the ONLY claims permitted are branches 1 or 2 read at that
  n's own wider band (±1.320pp, so KEEP needs ≥ 52.32% and REAL NEGATIVE
  ≤ 48.68%), **never branch 3 — an under-powered shard cannot deliver a
  "could not separate" verdict, because that is what an under-powered shard
  always says.** The floor (5,400) is ≤ the planned n (10,800).

### Obligation 12 — the futility gates, sized, with the direction of the default worked out

**GATE RESOLUTION: GATE-1000 cannot discriminate its own branch (±3.07pp against a 2.0pp boundary) and is UNRESOLVED BY CONSTRUCTION; GATE-2700 (±1.87pp) resolves only outside 48.63–52.37%; GATE-5400 (±1.32pp) resolves only outside 49.18–51.82%; and because these are FUTILITY gates the pre-committed default on an UNRESOLVED reading is the RESTRICTION, which here is the DROP, not the continuation.**

`docs/prereg/RULE-futility-gates-2026-08-13.md` binds every shard from its first
row. Applied, with the arithmetic done in advance:

* **GATE-1000 (n ≥ 1000), rule "drop if share < 48.0%".** Half-width **±3.07pp**;
  the boundary sits 2.0pp from 50, i.e. **inside its own interval**. It cannot
  tell 48.0 from 50.0 and is declared **UNRESOLVED BY CONSTRUCTION** before the
  fire.
* **GATE-2700 (n ≥ 2700), rule "drop if share ≤ 50.5%".** Half-width **±1.87pp**.
  Resolved only at share ≤ 48.63% (clearly futile) or share > 52.37% (clearly
  worth continuing); **UNRESOLVED between**.
* **GATE-5400 (n ≥ 5400) — the true halfway of a 10,800-game leg, added here
  because Magnus's rule was written for a 5,400 shard and "halfway" must move
  with n.** Rule: **drop if share ≤ 50.9%**. Derivation, not taste: the final
  informative edge is 51.93, so finishing from ≤50.9 at halfway requires the
  second 5,400 to run **≥ 52.96** — a worse buy than re-spending the cores.
  Half-width **±1.320pp**; resolved only outside 49.18–51.82%.
* ⭐ **THE DEFAULT, AND ITS DIRECTION IS THE OPPOSITE OF THE ONE THIS REPO WROTE
  LAST NIGHT — which is why it is derived here rather than copied.** Obligation
  12's rule is *"an unresolved gate takes the RESTRICTION, never the
  PERMISSION"*. In `SCREEN-gunaxabl` the gate was an early-stop-and-bank, so the
  permission was STOPPING and the restriction was CONTINUING. **Here the gate is
  a FUTILITY gate: the permission is CONTINUING to spend 8,100 more cores on an
  arm that has not shown itself; the restriction is the DROP.** ⇒ **an UNRESOLVED
  futility gate DROPS the shard**, which is also Magnus's rule as literally
  written. A futility drop is **not a refutation**: rows are kept, the arm stays
  a combo ingredient, and the label is recorded with its n and share.

---

## MECHANISM METRIC — and the instrument that produces it, because the shard tape cannot

**MECHANISM METRIC READS: bots/_v242bodyaware/eco.py:829-833 — the `blocked`-set construction of `_bfs_direction`, observed as C1, the share of ALL nav rounds whose FIRST refused step is refused because a builder bot occupies the tile. TREATMENT DIFF TOUCHES: bots/_v242bodyaware/eco.py. INTERSECTION: yes — the metric is computed by classifying the step that `_bfs_direction` returns, so it reads the exact function the diff rewrites and cannot read identically in both arms.**

**TREATMENT DIFF REFS: HEAD -- bots/** (the arm tree does not exist yet — this
prereg is committed BEFORE it is built, which is the correct order; re-run
`tools/prereg_check.py --fire` once `bots/_v242bodyaware` lands and the
intersection becomes computed rather than declared).

⛔ **THE SHARD TAPE CANNOT CARRY THIS METRIC AND MUST NOT BE ASKED TO.** The row
schema is `ts shard game map seed seat winner cond turns` and the runner uses
`--replay /dev/null`; there is no mechanism column, and our own `print()` output
is unreadable on the platform anyway. **The instrument is the existing probe
harness at `scratchpad/c63_probe_s43/`** — `instrument_eco.patch` +
`instrument_main.patch` applied to a scratch copy of the tree, rows read by that
directory's reader script, `run_c63.sh` as the driver. It has already produced
the incumbent numbers in this document, its accounting identities close on every
row, and its instrumentation costs 0.6pp of self-play games.

### ⭐ PRE-FIRE DELIVERY GATE — the shard may not be SCORED until this passes

**Re-run that harness with BODYAWARE patched into the treatment copy, same four
maps, same 352-game budget, and require:**

| gate | incumbent (measured) | required of the treatment | why this number |
|---|---|---|---|
| **G1 — C1 as a share of all nav rounds, pooled** | **21.8%** [19.2, 24.2] | **< 11.0%** | a first step into a visible body should be nearly eliminated: an adjacent tile is always inside a builder's r²=20 vision, so the residual IS the retry-fired population. **Less than a halving means the retry fires on most rounds — a non-delivery AND a CPU finding at once** |
| **G2 — retry-fire rate** (pass 0 finds no goal) | n/a (no retry exists) | **≤ 20% of nav rounds** | above this the "one extra BFS" is effectively unconditional; see §7 |
| **G3 — accounting** | all 5 identities hold | all 5 identities hold | an instrument that stops balancing is not measuring |

**A failure of G1 or G2 means the arm was not delivered as specified. The shard
is then not scored, and the reading banked is "BODYAWARE as written does not
change the world model it was designed to change" — which is a real finding
about the design, not about the currency.**

**PRE-STATE (Obligation 7): neither the outcome nor the mechanism is already in
its predicted state.** **Outcome:** no BODYAWARE tree exists; the only reading on
this chassis-and-pool cell is the structural 50.00% of a bot against itself, so
the predicted 51.93% is a cell demonstrably NOT already there. **Mechanism:** C1
sits at 21.8%, not at the predicted <11.0%, so a null cannot be blamed on a
treatment that was already true.

---

## §7 — HOT-TURN COST: **ADDS**, and the local instrument for it is DEAD (measured tonight, not assumed)

**VERDICT: ADDS.** BODYAWARE adds one `EntityType` comparison per nearby entity
(inside a loop that already runs) plus, on the failure path, **one complete
repeat of the BFS**. The design itself calls the 30×30 CPU probe *"a release
gate, not a nicety"*.

**⛔ AND THE INSTRUMENT SITUATION IS WORSE THAN THE BRIEF STATES — I DROVE IT
BOTH WAYS.** It is already known that `ct.get_cpu_time_elapsed()` returns 0
under local `fcode run` (`bots/_v223sealrepair/doctrine.py:1072`). **The replay
side is dead too:** one local game (`bots/_v223sealrepair` vs itself, midgard,
seed 999001, `--tle 10`) written to a kept replay and decoded with
`tools/tle_census.py` returns **12 rows with `tled = 0`, `exec_sum = 0`,
`exec_max = 0`, `over10k = 0`** — every timing field zero, on a game carrying
**1,649 builder-bot turns** across its round bands.

**The positive control that makes that absence meaningful is LIVE and running:**
`tools/monitors/cpu_watch.py` decodes PLATFORM replays with the same code path
and `corpus/cpu_watch.log` currently reports **"worst our-max 8,847 µs
(threshold 9,200)"**. **Same decoder, nonzero on the platform, zero locally.**
⇒ the zeros are the local engine, not a broken reader.

**⇒ NO LOCAL FIXTURE — SHARD, ARENA, OR KEPT-REPLAY — CAN MEASURE THIS ARM'S
CPU COST IN µs. THE SCREEN BELOW IS BLIND TO IT BY CONSTRUCTION, AND A CLEAN
SCREEN IS NOT A CLEAN CPU RESULT.**

**So the CPU gate binds the SHIP, not the screen, and it has two halves:**
* **LOCAL PROXY (executable now, inside the pre-fire gate above): G2, the
  retry-fire rate, plus BFS node-expansions per builder-turn in both arms.**
  These are the direct drivers of the doubling and are Python counters, not
  engine timers. **If the retry fires on more than 20% of nav rounds the
  doubling is effectively unconditional — that is a FINDING that blocks the ship
  on its own, independent of whatever the game-share column says**, and it is
  recorded as such rather than as a footnote to a positive result.
* **PLATFORM GATE (the only µs read that exists): `cpu_watch` already runs
  continuously against our platform replays with a 9,200 µs alarm.** The first
  live leg carrying BODYAWARE is therefore self-instrumenting — **but only ~353
  µs of headroom separates today's worst turn from that alarm**, so the ship
  decision must budget for the alarm firing and for an immediate rollback.

---

## Secondary columns — the kill channel, stated as EXCLUSIONS before they are read

`R1000_IS_DEFEAT` is unconditional, and a navigation change should pay through
ARRIVAL. Both columns come free off the shard tape (`cond`, `turns`).

* **C-KILL — median `turns` over `cond == core_destroyed` rows, per arm.**
  Predicted **DOWN** (earlier kill). A/A noise floor: `NULL125`, byte-identical
  arms, read **T 211.5 vs C 208.5 rounds** — a +3.0-round offset with nothing
  changed. **Material threshold: |Δ median| ≥ 10 rounds** (>3× that floor).
* **C-R1000 — share of rows with `cond == tiebreak`, per arm.** Predicted
  **DOWN**. Reference density from a live shard on the same control tree:
  `GUNAXABL` reads **130 / 2,242 = 5.8% tiebreak**.
* ⛔ **RESTATEMENT BEFORE BANKING, and it binds even though this arm is not
  defensive.** *"BODYAWARE did not slow the kill"* is a FAIL-TO-EXCLUDE claim and
  may not be banked in that form — DEFF laundering aside, the direction of the
  risk here is real (a detour is longer than a wait). It is banked ONLY as an
  exclusion: **the 95% bootstrap CI (10,000 resamples) on the difference of
  median kill rounds excludes a +10-round regression.** If it does not, the
  column reads **UNRESOLVED** and no kill-round claim is made in either
  direction. No design-effect inflation is applied: same fixture, same DEFF 0.98,
  same two dead clusters.

---

## RATIFY: Segment

**MAP SEGMENT: none expected — this arm is registered POOLED over the 15-map pool, and `#63`'s inherited segment is RETIRED here rather than carried.**

Three reasons, in the order they bind:

1. **The inherited segment is CONTRADICTED, not merely unsupported.** The design
   inherited `{midgard, ragnarok}` from the row. The probe reads **midgard at
   13.7% — the LOWEST of the four maps measured**, below both control maps.
   A segment whose name-map is its weakest dose cell is not a segment.
2. **A mechanism-defined replacement is NOT DECLARABLE from this probe.** The
   honest dose ordering is ragnarok 28.4 > glacierkeep 19.3 > midgard 13.7 >
   valkyrie 12.6, which would suggest `{ragnarok, glacierkeep}` — **but 11 of the
   15 pool maps were never probed**, so that cut would be a 2-map claim over a
   15-map pool with two-thirds of the pool unmeasured. Declaring it would be
   exactly the subgroup fishing Obligation 15b forbids, dressed as mechanism.
3. **The mechanism is present EVERYWHERE it was looked for.** C1 spans
   12.6–28.4% of nav rounds and **no cell is near zero**. A pooled screen
   therefore is not measuring a conditional plank as zero — it is measuring a
   broadly-distributed one at its true pooled size, diluted at worst by the ratio
   between the pooled 21.8% and the best cell's 28.4%, i.e. ~1.3×.

**A per-map column IS registered — DESCRIPTIVE, with NO bar and NO branch.** It
exists so a future leg can define a segment properly over all 15 maps.
⛔ **It may not rescue a pooled miss.** Per Obligation 15c, a segment suggested by
these rows requires a NEW leg with its own n and its own seed base; the rows that
suggest a segment may not also confirm it. **The pooled reading is the verdict.**

---

## RATIFY: FALSIFIER

**FALSIFIER: the treatment arm finishes at or below 49.07% game share at n = 10,800.**
That refutes the hypothesis outright and inverts the plank: the F1 omission at
`eco.py:829-833` becomes a feature rather than a defect, "wait one round" beats
"route around", and the navigation half of `#63` closes — leaving only
DESTINATION changes (re-pick targets so columns never form), which is a different
design needing a different note.

Three further pre-committed off-prediction outcomes, each of which lands
somewhere other than "the arm is good":

* **DELIVERY falsifier (pre-fire gate G1).** The treatment's C1 does not fall
  below 11.0% of nav rounds. The world model did not change as designed; the
  shard is not scored; the finding is about the design, not the currency.
* **CPU falsifier (pre-fire gate G2).** The retry fires on more than 20% of nav
  rounds. The "one extra BFS" is unconditional in practice, the arm is blocked
  from ship on a chassis with 3.5% alarm headroom **whatever the game-share
  column reads**, and the design's step-3 fallback needs bounding (e.g. a
  per-turn retry budget) before this road reopens.
* **CHANNEL falsifier.** The currency bar is met while **C-KILL rises by ≥10
  rounds and C-R1000 rises**. The arm then wins games by some route other than
  arriving sooner; under `R1000_IS_DEFEAT` that is not the plank that was
  registered, and it may not be banked as one without a new mechanism read.

---

## Interaction with the live legs — required line

Two shards are running against the same control tree (`bots/_v223sealrepair`) on
the same 15-map pool at draft time (`ps`, `scratchpad/overnight/*.heartbeat`,
2026-08-14T23:43Z):

* **`GUNAXABL`** (`bots/_v240gunaxabl`, seed base 312000, 2154/5400) — diff is
  `doctrine.py:1533`, `LOKI_GUNAXIS_PENALTY` 8 → 0, consumed at `raid.py:815-816`
  in `_raid_station`'s scoring loop. **Different module, different function,
  no shared line with `eco.py:809-896`.**
* **`SENTTHR`** (`bots/_v241sentthreat`, seed base 314000, 2135/5400) — the #30
  sentinel-threat arm, likewise in the raid/turret layer.
* *(`SEALFLOOR6`, seed base 308000, is no longer running: its heartbeat is 43
  minutes stale against a 1-minute cadence and `corefill.log` reads
  `running=2/8`. Reported as an observation about the board, not as a claim about
  that shard's outcome — `scratchpad/RESULT-sealfloor6-GATE2700.txt` is the file
  that decides it.)*

⇒ **NO CONFOUND WITHIN THIS SCREEN:** separate shards, disjoint seed bases
(BODYAWR takes 336000–336674), each arm measured independently against the same
control. The one real interaction is **RESOURCE** — a 10,800-game leg beside two
5,400-game legs contends for 8 cores, and it is proposed precisely because six
slots read idle at draft time. ⚠ **If the board fills, BODYAWR is the row to
defer**, per `docs/coordination.md:52001` (`#63` is HELD, worth ≤ ~2pp pooled).

**⛔ AND THE ONE ORDERING RULE INHERITED FROM THE DESIGN, §6 — it does not bind
this leg but it binds the next one.** BODYAWARE changes which tiles a builder
walks into, which is the input SPAWNPOCKET's placement rule is defined over; the
interaction runs ONE WAY (BODYAWARE can change SPAWNPOCKET's measured effect on
midgard, not the reverse). **On the shared midgard cell the two arms must not be
measured concurrently.** This leg is LOCAL, pooled, and claims no midgard cell,
so nothing is confounded here — **but any later live or per-map read of either
arm on midgard inherits the rule**, and this document is where the second prereg
should find it rather than rediscovering it in an analysis.

---

**PROVENANCE:** `QUEUE.md` (row #63, line 150) · `CLAUDE.md` · `docs/research/DESIGN-63-long-approach-arrival-2026-08-14.md` · `docs/prereg/RULE-futility-gates-2026-08-13.md` · `docs/prereg/SCREEN-gunaxabl-2026-08-14.md` (format template only) · `docs/coordination.md` (grepped by line for `#63`/`BODYAWARE`, never read whole: `:50833-50851`, `:51938-51952`, `:52001`) · `bots/_v223sealrepair/eco.py` · `bots/_v223sealrepair/doctrine.py` · `tools/prereg_check.py` · `tools/overnight.sh` · `tools/corefill.sh` · `tools/tle_census.py` · `tools/monitors/cpu_watch.py` · `corpus/cpu_watch.log` · `scratchpad/corefill_work.txt` · `scratchpad/corefill.log` · `scratchpad/c63_probe_s43/` (the s43 probe directory: `report_all.txt`, `c0_raw.txt`, `c0_valkyrie.txt`, `c0_ragnarok.txt`, `instrument_eco.patch`, `instrument_main.patch`, `run_c63.sh` and its reader) · `scratchpad/overnight/NULL125.result_cache` · `scratchpad/overnight/GUNAXABL.tsv` · `scratchpad/overnight/*.heartbeat` · plus one throw-away local game run by this agent (`bots/_v223sealrepair` vs itself, midgard, seed 999001, `--tle 10`) whose kept replay was written to the session scratchpad and decoded to establish that local replays carry no exec-time fields. No file under `bots/`, `tools/`, or `scratchpad/` was created or modified by this agent.
