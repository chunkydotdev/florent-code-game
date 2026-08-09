# Which tile is actually binding? — the binding-tile cut

**Research arm, session 28. Decoded 2026-08-10. Direct successor to
`stalled-stack-cut-2026-08-09.md`, which proved harvesters are blocked by their own output
tile and could not say why that tile was full.**

**Population: all 8,519 `.replay26` files in `replay_archive/`, decoded, 0 errors. LADDER.
Headline arms are the 2,271 round-1000 games with a `meta.json` attribution and
`related == 'none'` → 579 US team-sides and 3,384 third-party team-sides.
No downloads. No bot, arena or prereg touched.**

---

## 0. The answer in three lines

**The binding tile is almost never a merge, a splitter, a saturated trunk or a core entry.
It is the end of a conveyor line that does not reach the core.** 68.6% of our lost harvester
emission sits behind a conveyor pointing at something that cannot receive a stack — empty
ground, a wall, our own turret, an enemy building, or another conveyor pointing back at it.
A further 15.9% is a harvester with no receiving neighbour at all.

**Merges bind 0.01% of the time. Splitters 0.00%. Core entry 0.00006% — one round in
1,798,862.**

**The prescription the data supports is the one the brief did not list: not fewer lines, not
more lines, not different lines — *terminated* lines, and a builder that repairs them.**

---

## 1. The binding-tile distribution

Unit of analysis: one **blocked harvester-round** — a round in which a harvester was due to
emit (r ≥ last emission + 4, or ≥ its build round before its first) and did not. For each
one, the harvester's stalled output tiles are walked downstream along conveyor facings to the
most downstream tile that also did not move; that tile is the **binding tile**, and it is
classified by what its own output tile is. Weight 1.0 per blocked harvester-round, split
evenly when a harvester's several outputs resolve to different binding tiles.

**US — OpenSverige, 579 round-1000 team-sides, 1,798,862 blocked harvester-rounds**
**FIELD — 3,384 third-party round-1000 team-sides (meta.json-attributed), 6,669,090**

| binding-tile class | what it means | US share | US Ti/game | FIELD share | FIELD Ti/game |
| --- | --- | --- | --- | --- | --- |
| `DEAD_END_GROUND` | line points at an empty tile | **39.61%** | 3,076 | 31.45% | 1,550 |
| `NO_OUTPUT_BUILT` | harvester has no receiving neighbour at all | **15.92%** | 1,236 | 28.81% | 1,419 |
| `DOWNSTREAM_MOVED` | genuine saturation — downstream did move | **14.29%** | 1,110 | 18.75% | 924 |
| `DEAD_END_BUILDING` | line points at a turret / barrier | **13.15%** | 1,021 | 6.88% | 339 |
| `HEAD_TO_HEAD` | two conveyors pointing at each other | **9.94%** | 772 | 1.57% | 77 |
| `INTO_HARVESTER` | line points at a harvester (never accepts) | 5.64% | 438 | 3.26% | 161 |
| `ENEMY_NET` | line feeds an enemy conveyor | 0.74% | 58 | 0.68% | 33 |
| `OUTPUT_OCCUPIED_MOVING` | output busy but flowing | 0.29% | 23 | 0.50% | 25 |
| `DEAD_END_WALL` | line points into a wall | 0.20% | 16 | 8.01% | 395 |
| `OTHER_CARRIER` | misc. carrier terminus | 0.04% | 3 | 0.02% | 1 |
| **`MERGE_LOST`** | **two feeders, one tile, we lost the round** | **0.01%** | **1** | **0.01%** | **1** |
| **`SPLITTER_SIDE_REJECT`** | **splitter refused a non-back feed** | **0.00%** | **0** | **0.01%** | **1** |
| **`CORE_ENTRY`** | **the core face itself was the constraint** | **0.00006%** | **0** | **0.00%** | **0** |
| `OUTPUT_FREE_BUT_IDLE` | *residual — output was free and it still didn't emit* | 0.17% | 13 | 0.03% | 2 |
| `UNEXPLAINED_EMPTY` | *residual — no structural reason found* | 0.0003% | 0 | 0.00002% | 0 |

Titanium conversion: 4 blocked rounds = one missed 10 Ti emission slot, so 1 blocked
harvester-round = 2.5 Ti. **The total this produces — 7,767 Ti/game of lost emission for US —
reproduces the parent cut's independently derived 7,800 Ti/game to within 0.4%, from a
different instrument.** That agreement is the reason the Ti column is quoted at all.

### The two residual buckets are the honesty check, and they are empty

`OUTPUT_FREE_BUT_IDLE` and `UNEXPLAINED_EMPTY` are where a blocked harvester-round lands when
the model cannot explain it. Together they are **0.17% (US) and 0.03% (field)**. Under
injected corruption they rise to **72.1%** (see §5). **99.8% of blocked harvester-rounds have
a structural explanation, and the bucket that would catch a wrong model demonstrably fires.**

### Regrouped into things a builder can actually do

| action | US share of all blocked | US Ti/game |
| --- | --- | --- |
| **finish the line** — it ends on ground where nothing was ever built | **33.4%** | 2,592 |
| **repair the line** — a carrier once stood on that tile and was destroyed | **23.9%** | 1,855 |
| **stop building into our own turrets/barriers** | **11.1%** | 862 |
| **fix facings** — head-to-head conveyors, lines into harvesters, into walls | **15.8%** | 1,226 |
| **give the harvester an output at all** | **15.9%** | 1,236 |
| enemy building blocks the line (contested, not purely a build bug) | 6.1% | 472 |
| **genuine saturation — the line was running and still couldn't take it** | **14.3%** | 1,110 |

(Rows overlap slightly by construction: the first three are sub-classes of the two
`DEAD_END_*` rows and are quoted against the same denominator.)

---

## 2. The prescription

**The data supports exactly one of the brief's five candidates, and it is the last one — with
its wording corrected.**

- ❌ **fewer, shorter lines (long runs saturate).** Saturation is 14.3% of our lost emission
  pooled and **0.1% at the median team-side** (§4). Our lines are not saturated; the median
  one of ours is broken.
- ❌ **more parallel lines into distinct core-entry tiles (merges bind).** Merges bind
  0.01%. Core entry binds one round in 1.8 million. Adding entry tiles addresses 0.01% of the
  problem. **This is the claim in the document with the weakest instrument — see the
  under-count caveat below, which I could bound but not eliminate.**
- ❌ **fewer / differently placed splitters.** Splitters are 58,721 of 40,363,446 carrier
  pushes archive-wide — **0.15%**. They bind 0.00% for us. There is nothing here to fix.
- ❌ **harvester siting closer to the core.** The median binding tile is 5 tiles from our own
  core and 3 hops downstream of the harvester (§3). Distance is not the driver; **85% of
  binding tiles have no directed path to the core at any distance.**
- ✅ **"the network is fine and harvester placement is the problem" — half right, and the
  useful half.** The network's *topology* is not fine and its *capacity* is not the problem.
  **The lines do not terminate at the core.**

**The single build change the data supports: a terminus invariant plus a repair loop.**
Before a builder lays or keeps a conveyor, the chain from that tile must reach a friendly core
footprint tile by following facings; when it does not — because it was never finished, because
a segment was destroyed, or because we built a turret on top of it — that is the highest-value
action available to that builder. Concretely, in order of measured mass:

1. **Never leave a line unterminated** (33.4%). A conveyor whose facing points at empty ground
   is a cork, and it corks everything upstream of it for the rest of the game.
2. **Repair destroyed segments** (23.9%). We currently do not. A single lost conveyor
   permanently disables its whole upstream line.
3. **Do not place turrets on our own conveyor route** (11.1%). Our own sentinels, launchers
   and gunners are the terminus of 11% of our blocked mass — *more than the enemy's buildings
   are* (6.1%).
4. **Assert facing coherence** (15.8%). Head-to-head conveyor pairs alone are 9.9% of our
   blocked mass against the field's 1.6% — this one is close to a live bug and is ours
   specifically.

**Priority note from §3: a median of 3 tiles carries 80% of a team-side's blocked mass.** This
does not need a network rewrite. It needs three tiles fixed per game.

### The one place my instrument is structurally biased, and by how much

**The walk under-counts merges by construction, and I could not remove the bias — only bound
it.** `MERGE_LOST` can only fire in a round where the contended downstream tile was *empty* at
r−1. A merge that costs a feeder one round leaves that tile *occupied*, so on the next round
the walk passes straight through it and attributes the stall to whatever binds further
downstream. **A merge that repeats therefore hides behind its own consequence.**

Two things bound it. First, `DOWNSTREAM_MOVED` — 14.3% pooled, 0.1% median — is the class that
catches "the line is flowing and my stack still didn't get on", which is what a chronic merge
looks like from upstream; it is measured, and it is the whole of the capacity-type mass.
Second, on the `MERGE_LOST` events that *do* fire, the fan-in degree of the contended tile is
recorded:

```
  US   : fan-in 1 : 131.0 weight    fan-in 2 : 93.9    fan-in 3 : 7.5   (n = 232)
  FIELD: fan-in 1 : 428.8 weight    fan-in 2 : 292.3   fan-in 3 : 42.8  (n = 764)
```

**56% of them have only ONE conveyor pointing at the contended tile — so they are not merges
at all, they are timing.** True multi-feeder contention is ~0.006% of our blocked mass. **The
bias is real; the quantity it could be hiding is bounded by the 14.3% saturation class, and
the median team-side of ours has 0.1% of that.**

---

## 3. Where the binding tile is, and how many there are

**Distance (US / field, round-1000):**

| measure | US | FIELD |
| --- | --- | --- |
| Chebyshev distance, binding tile → own core footprint | median **5** | median 4 |
| chain hops, harvester's output tile → binding tile | median **3** | median 2 |
| **binding tiles with NO directed path to own core** | **85.15%** | **76.26%** |

The binding tile is close to the core in *space* and unreachable from it in *topology*. That
is the finding in one line: **we are not failing to move titanium far enough, we are failing to
connect it at all.**

**Chokepoints per team-side (round-1000):**

| measure | US (n=553) | FIELD (n=2,228) |
| --- | --- | --- |
| distinct binding tiles per team-side | median **10** (q1 4, q3 19) | median 4 (q1 2, q3 10) |
| share of blocked mass on the single worst tile | median **44.7%** | median 52.0% |
| tiles needed to cover 80% of blocked mass | median **3** | median 2 |

**Many chokepoints, few that matter.** A typical game of ours has ten binding tiles and three
of them carry four fifths of the loss.

**This reconciles the parent cut's smallest number with its largest one.** ~10 corked tiles ×
10 Ti = ~100 Ti visibly stranded at round 1000 (the parent measured a 150 Ti median), while
those same corks withhold 7,767 Ti of emission. **The stranded-stack figure was never small
because the mechanism was small — it was small because a cork weighs one stack and blocks a
barrel.** Ratio ≈ 1:78.

---

## 4. Ours vs third-party — and the mixture that would have defeated the aggregate

**Method rule 7 bites on my own number.** For US, `DOWNSTREAM_MOVED` (saturation) is **14.3%
mass-pooled but 0.1% at the median team-side**:

| share of blocked mass | US per-side q1 / med / q3 / p90 | US mass-pooled | FIELD per-side med | FIELD pooled |
| --- | --- | --- | --- | --- |
| broken chain | 0.507 / **0.802** / 0.968 / 0.992 | 0.686 | **0.761** | 0.512 |
| saturation | 0.000 / **0.001** / 0.082 / 0.403 | 0.143 | **0.000** | 0.188 |
| no output built | 0.013 / **0.064** / 0.256 / 0.502 | 0.159 | **0.022** | 0.288 |

**Only 6.1% of our team-sides are majority-saturation-bound, holding 9.5% of the blocked
mass** (field: 11.1% of sides, 19.1% of mass). Quoting the pooled 14.3% as "our lines are
one-seventh saturated" would have been wrong: **the median line of ours is not saturated at
all, and a handful of games carry all of it.**

**Per-team spread of the "chain does not reach the core" share** (teams with ≥8 round-1000
team-sides and ≥200 blocked harvester-rounds; team names from `meta.json`):

```
  field per-team median:  min 0.000   q1 0.352   med 0.666   q3 0.936   max 1.000  (51 teams)
  US                   :  0.802                                          (512 team-sides)
```

The field is a mixture of incompatible doctrines and its mean means nothing. What *is*
informative is which end of it the productive teams sit at:

| team | n | broken | saturation | no-output |
| --- | --- | --- | --- | --- |
| **US OpenSverige** | 512 | **0.802** | **0.001** | 0.064 |
| Memtrace | 17 | 0.000 | **0.894** | 0.011 |
| Bean counters | 85 | 0.043 | **0.816** | 0.006 |
| Viktor5776 | 51 | 0.274 | **0.424** | 0.013 |
| sporks | 30 | 0.169 | **0.421** | 0.112 |
| ph | 29 | 0.366 | **0.409** | 0.026 |
| PromptNPray | 86 | 0.250 | **0.392** | 0.023 |
| Git Glam | 72 | 0.708 | 0.001 | 0.045 |
| StarTrekker / S / Troupe / Tim Tam | 133/125/123/101 | 1.000 | 0.000 | 0.000 |
| Cookie / Kvarnholmen / O(1) | 79/132/15 | 0.000 | 0.000 | **≥0.93** |

**Every team the parent cut identified as converting a large economy — Bean counters,
PromptNPray, Viktor5776, sporks, ph — is saturation-bound. We are breakage-bound.** Their
harvesters stall because the pipe is full; ours stall because the pipe goes nowhere. That is
the same distinction as §2 and it is visible in the field without reference to us.

### An independent instrument agrees

`tools/replay_census.py`'s `chain_dir` (directed conveyor reachability to own core, on
end-of-game state, validated against `fcode run --json`) was written for a different question
by a different session and knows nothing about this decode. On round-1000 games:

| arm | harvesters alive at end | undirected connected | **directed connected** |
| --- | --- | --- | --- |
| **US** (126 files) | 1,003 | 75.8% | **58.8%** |
| our opponents *in our games* (not a field baseline) | 813 | 77.7% | **74.3%** |
| third-party, meta.json-attributed (128 files) | 1,067 | 66.1% | **55.2%** |

**We lay 17.0pp more road than we point anywhere; our opponents' gap is 3.4pp.** Per-team
directed rate across third-party teams with ≥30 surviving harvesters (n=10): min 0, q1 29,
med 48, q3 81, max 100 — **Viktor5776 100.0%**, Bean counters 79.7%, TKB 0.0%.

---

## 5. Instrument validation — teeth per guard, per branch

**Guard `ti_ok` (core deliveries × 10 == `Player.titaniumCollected`).**
**4,542 / 4,542 PASS** over every round-1000 attributed team-side; **17,031 / 17,038 PASS**
across the entire archive. The 7 failures are all `core_destroyed` games where the decode
counts 1–2 stacks *more* than the final `updatePlayers`, i.e. deliveries landing after the
last player snapshot in a game that ended mid-round. **Stated rather than suppressed: this
guard is not vacuous, it fails on 0.04% of team-sides, and none of them are in the headline
population.**

**Three injected corruptions, each of which must fire, and each fires differently** (40
replays, clean baseline in the left column):

| | clean | `silence` (drop all moves after r200) | `freeze` (drop moves off a fixed tile lattice from r100) | `scramble` (rotate every conveyor facing 90°) |
| --- | --- | --- | --- | --- |
| `ti_ok` | 80/80 PASS | **36 PASS / 44 FAIL** | **72 PASS / 8 FAIL** | 80/80 PASS *(correct — the guard does not read facing)* |
| blocked harvester-rounds | 49,377 | **112,623** | 50,767 | 49,377 |
| `OUTPUT_FREE_BUT_IDLE` | 0.08% | **66.72%** | 4.91% | 0.94% |
| `UNEXPLAINED_EMPTY` | 0.00% | **5.41%** | **15.71%** | **9.39%** |
| `DEAD_END_WALL` | 3.09% | 0.88% | 3.01% | **12.54%** |
| `DEAD_END_OFFMAP` | 0.00% | 0.00% | 0.00% | **4.50%** |
| `INTO_HARVESTER` | 3.17% | — | 2.84% | **13.32%** |
| `DOWNSTREAM_MOVED` | 12.45% | 0.51% | 6.03% | **~0%** |

**`scramble` is the load-bearing test.** It leaves the resource stream untouched and rotates
only the conveyor `direction` field, so `ti_ok` correctly stays clean while the classification
inverts. **The classification therefore depends on the facing field and could not have been
produced by any facing assignment.** `silence` and `freeze` prove the residual buckets are not
decorative: they go from 0.08% to 72.1% and from 0.00% to 15.7%.

**The parent's control, reproduced with a different instrument (method rule 3).** The parent
asked whether *one canonical* output tile was occupied. This decode asks whether *every
structurally receivable orthogonal neighbour* was occupied — a different question with a
different failure mode:

```
  US   : due-and-blocked rounds with NO free output  99.83%   (n=1,798,862)
         NOT-due rounds with no free output          30.93%   (n=1,920,488)   <- the control
         separation                                 +68.90 pp
  FIELD: 99.97% vs 38.07%,  +61.90 pp                (n=6,669,090 / 5,373,087)
```

Parent: +69.4pp (US) and +73.8pp (field). **Two instruments, same mechanism, same magnitude.**

**Entity-map integrity, which the dead-end classes rest on.** Over 300 replays: 62,170
building placements, **0 placed onto a tile holding a different live entity, 0 placements of a
previously removed id, 0 buildings changing tile.** The 17.9% of `removeEntity` ids that are
unknown to the building map are builder bots and cores (both excluded from it by design) and
cause no deletion. **So a `DEAD_END_GROUND` verdict is not a bookkeeping hole.**

**Both branches of the ours/field partition were tested (method rule 2).** The seat comes from
`meta_join.us_side`, derived by `meta_attrib.py` from `meta.json`'s `teamAId`, **not** from
`winnerSide` — TRAP 7's circularity does not apply. `related != 'none'` excluded from both
arms (130 files). The arms differ materially on every headline (broken 0.802 vs 0.761 median
but 9.94% vs 1.57% on head-to-head, 0.20% vs 8.01% on walls), so the seat variable carries
signal and is not near-constant.

**A rejected alternative, tested rather than assumed.** `DOWNSTREAM_MOVED` could have been an
engine iteration-order artefact — a chain that only shifts as a unit when the downstream
conveyor is processed first. If the engine iterates by entity id, same-round chain shift would
occur only when the downstream conveyor has the lower id, and **line throughput would be
decided by build order.** Measured over 120 replays, 367,264 conveyor→conveyor pushes:

```
  downstream id LOWER  : chain shifted same round  52.55%  (n=128,243)
  downstream id HIGHER : chain shifted same round  49.19%  (n=239,021)
```

**No effect. Build order does not gate line throughput.** `DOWNSTREAM_MOVED` is ordinary
congestion.

---

## 6. Two capacity facts, measured with opportunity — and one that cannot be measured at all

The brief instructed me to build nothing on the retracted "1 stack per core-entry tile per
round" ceiling. I did not. I measured capacity directly instead, archive-wide over all 8,519
replays, and **state the denominator every time**.

**(a) A carrier tile pushes at most 1 stack per round. This one is real.**

```
  carrier tile-rounds pushing exactly 1 stack : 40,363,446
  carrier tile-rounds pushing 2 or more       :          0
  conveyor tiles that sustained exactly 100 pushes in a 100-round window : 9,559
  conveyor tiles that ever exceeded 100 in a 100-round window            :     0
```

**This ceiling is conditioned on opportunity, which is exactly what the retracted one was
not.** 9,559 conveyor tiles sat at the cap continuously for a hundred rounds. The condition
under which the cap could have been exceeded arises constantly and it is never exceeded.

**(b) A core footprint tile takes 2 stacks in a round — and geometry, not the engine, is why
it never takes 3.**

```
  core footprint tile-rounds receiving 1 stack  : 4,591,933
  core footprint tile-rounds receiving 2 stacks :   215,837   (4.49%)
  core footprint tile-rounds receiving 3+       :         0
  core tiles sustaining >100 stacks per 100-round window : 1,077
```

This independently replicates the builder arm's refutation (they measured 532/13,706 on 60
games; I get 215,837/4,807,770 on 8,519) and strengthens it: **1,077 core tiles sustained more
than one stack per round for a hundred consecutive rounds.** Capacity is not 1.

**But the "is it 2, or more?" question cannot be answered from replays at all, and here is
why.** A 2×2 core footprint tile has exactly **two** orthogonal neighbours that are not
themselves core tiles. Each of those can push at most 1 stack per round by (a). **So the
supply into any single core tile is capped at 2 by the map, before the engine has an opinion.**
The observed maximum of 2 is fully explained without positing an engine ceiling. **A third
stack is never offered, so "never observed" carries no information — the same fault as the
retracted claim, and it is unfixable from this data.** An engine probe is the only instrument
that can settle it, and **nothing in this document depends on the answer.**

**(c) The core face, as a raw rate with a measured denominator.** The whole 2×2 core has
**8** orthogonally adjacent external tiles. Each pushes ≤1 stack/round (measured, 0/40,363,446
exceptions). So total core intake admits **8 stacks/round = 80 Ti/round**, and that denominator
is measured rather than assumed. **We deliver 10,500 Ti/game = 1.05 stacks/round.** Headroom at
the core face is therefore **≥7.6×**, and the *reason* we do not use it is §1, not the face.

**I am not restating the brief's 25% core-entry utilisation, and no number here divides by an
unmeasured capacity.**

---

## 7. What I could not measure

1. **Whether the engine caps core-tile intake, and at what value.** §6(b): the map supplies at
   most 2 and the engine is never asked for 3. **Unanswerable from replays. Needs an engine
   probe.** Nothing here depends on it.
2. **The actual within-round resolution order of the distribution step.** I refuted build-order
   (entity id) as the gate on same-round chain shift, but did not identify what does gate it.
   `DOWNSTREAM_MOVED` (14.3% pooled / 0.1% median for us) is therefore labelled "saturation"
   on the evidence that the downstream tile *did* move — which is sound — but its fine
   structure is unexplained. **If someone wants to attack the last 14%, that is the open
   mechanism.**
3. **Merges are structurally under-counted by the walk** — see §2. Bounded, not eliminated.
   **Also note that `DOWNSTREAM_MOVED` mass (257,004) exceeds the mass whose binding tile has a
   directed path to the core (223,363), so a locally flowing line can still terminate at a dead
   end further down.** "The line is moving" does not imply "the line arrives".
4. **Splitters are untestable at this n.** 58,721 pushes of 40,363,446 archive-wide (0.15%),
   `SPLITTER_SIDE_REJECT` = 0 rounds for us and 966 for the field. **I can say splitters are
   not a mechanism anyone currently uses; I cannot say what would happen if they were.**
5. **`NO_OUTPUT_BUILT` (15.9%) conflates two different failures** — a harvester built with no
   output conveyor ever, and one whose only output was destroyed leaving no receiver adjacent.
   The `ever_carrier` split that separates `DEAD_END_GROUND` into never-built vs destroyed was
   not applied to this class. **The "give the harvester an output at all" row in §2 therefore
   does not distinguish siting from repair.**
6. **Round-1000 games only, for every headline.** 579 US team-sides of 2,318 attributed; 5,993
   of 8,264 attributed files end before round 1000 and are excluded entirely. **Nothing here
   describes economies in games decided by a core kill**, which is where the class-weighted
   battery says most of our losses live.
7. **Denominator exclusions, stated explicitly (method rule 4).** Of 8,519 decoded files: 125
   have no `meta_join` row, 130 are `related != 'none'`, 5,993 are not round-1000. The
   round-1000 arms are 579 US / 3,384 third-party team-sides. **The third-party arm is 51 teams
   at ≥8 team-sides and is a mixture (§4) — its pooled figures are reported only alongside the
   per-team spread, never as "the field baseline".**
8. **The Ti conversion (2.5 Ti per blocked harvester-round) assumes the 4-round emission
   clock.** It is the parent's validated clock and my total reproduces theirs to 0.4%, but
   every Ti figure in §1 inherits that assumption. **The share columns do not.**
9. **A harvester that is blocked and also happens to be dead-ended in more than one direction
   is attributed fractionally** (weight split evenly across distinct binding tiles). At
   `hops = 0` — 19.3% of our mass — the harvester's own output tile is the binding tile, so
   the split rarely engages, but it is a modelling choice, not a measurement.

---

## Appendix — reproducing this

Scripts are session-scratch and die with the session (~450 lines against
`tools/replay_census.fields`). The load-bearing decisions:

- **Conveyor output geometry is exact and was verified before it was used**: 655,507 of
  655,507 conveyor pushes went to `pos + delta(direction)`, and 660,243 of 660,243 inbound
  moves came from a side other than the conveyor's own output tile. **A conveyor accepts from
  3 sides and outputs to the 4th, exactly as documented.**
- **Splitters accept only from the back** (`pos + delta(opposite(direction))`), confirmed on
  the move stream, and output to the facing direction plus at least one perpendicular.
- **Harvesters do not have one output tile.** Of 1,509 harvesters in a 171-replay probe, 857
  used exactly 1 output tile, 416 used 2, 186 used 3 and 50 used 4. **The parent cut's "the
  harvester's output tile" is a mode, not a property**, which is why this decode tests every
  structurally receivable orthogonal neighbour instead. It is also why the control in §5 is a
  genuinely different instrument rather than a re-run.
- **Turrets, barriers and harvesters never accept a stack**, so a conveyor facing one is a
  terminus. This is the documented rule and it is what makes `DEAD_END_BUILDING` and
  `INTO_HARVESTER` mean what they say.
- **Occupancy has no snapshot** (TRAP: `Conveyor.stored` is never populated on `placeEntity`)
  and must be integrated from `distributeResources` — update field 4, which per the builder
  arm this session is the field `replay_econ.py` loops over and discards, and is therefore the
  root cause of TRAP 8's dead `deliveries` column.
- **A carrier destroyed while holding a stack must terminate that stack's residency**, or the
  tile reads as a permanent stall.
- **Entity ids and resource stack ids share one global counter** (TRAP 1). Only identity and
  ordering are used; the one place magnitude was tested — the build-order hypothesis in §5 —
  compared ids *within* the building space only, and returned a null.
