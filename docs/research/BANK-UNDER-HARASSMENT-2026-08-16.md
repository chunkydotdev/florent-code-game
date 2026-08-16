# QUEUE #80 PRECONDITION: does our banked titanium pile up when we are harassed?

**Research arm, 2026-08-16T13:32:33Z (`date -u`), repo `ca177b7e`.**
**Instrument:** `tools/bank_under_harassment.py` (new, this cut). Free corpus /
replay cut — **no games fired, no platform window spent.**

---

## 0. THE ONE-LINE VERDICT

**NO-GO ON THE PREMISE AS WRITTEN, GO ON A RE-PRICED VERSION OF THE ROW.**

* **Harassment does NOT fatten the bank. It thins it, at every round from r50 to
  r200.** Games in the top harassment tertile at r100 peak at a **median 105 Ti**
  over r101-300 against **152 Ti** for the bottom tertile, and reach 260 Ti in
  **9.0% vs 15.8%** of games. Restated as the exclusion the `DEFF` direction
  clause requires: **harassment cannot raise the 260-Ti fire rate by more than
  +1.7pp (95% CI, DEFF 1.529).** The proposer's mechanism is not merely absent,
  it runs backwards.
* **`SURGE_TI_FLOOR = 1500` is unreachable inside the kill window on the current
  tree: 0 of 590 games.** It is barely reachable at all — 0.6% (v140) / 2.2%
  (v152) of games touch 1500 Ti at ANY round, all of them in the r300+ tail that
  `R1000_IS_DEFEAT` already writes off.
* **But a trigger at ~200 Ti is genuinely live: it fires in 25.6% of games,
  median first crossing r67, and 18.5% of games cross it before r150.** At the
  ~300% cost scale the belt census measured, **200 Ti is three gunners or two
  sentinels.** The row survives if its threshold is re-priced by an order of
  magnitude and stops being conditioned on harassment.
* ⭐ **AND THE ROW'S GREP MISSED A SECOND, ALREADY-SHIPPED BANK TRIGGER.**
  `main.py:263-268` buys extra builder-bot seats at **`LOKI_SURPLUS_TI = 260`**
  and again at **`LOKI_RICH_TI = 700`**. So "ZERO bank-triggered offensive spend"
  is wrong as stated — and measured, **the 260 gate fires in 15.9% of games while
  the 700 gate fires in 1.4%, i.e. `LOKI_RICH_TI` is effectively dead code.**

---

## 1. POPULATION — the enumeration rule, with its count

**RULE:** every row of `corpus/join.tsv` whose `ourver` is `140` or `152`, whose
replay is present in `replay_archive/`.
**COUNT: 590 games, across 118 matches and 19 distinct opponents. 0 dropped.**

* `join.tsv` is **ladder-only** (rated). Nothing here is a win-rate denominator,
  and `meta_join` is not used, so the "never `meta_join` for a denominator" rule
  is not engaged.
* **Why v140 + v152 and not v140 alone:** v140 (`bots/_v223sealrepair`, 360
  games) is the tree the belt census read and the tree QUEUE #80 greps against;
  v152 (230 games) is the current holder. Pooling buys power and the two agree
  on every headline (v140 alone: 19.7% ever ≥260, v152 alone: 17.8%).
  **The 5,506 games on other versions are NOT pooled** — see §6, where they are
  used as a deliberate positive control, because the pre-v102 trees are a
  different economy entirely.
* **Seat** comes from `join.our_team`, which the belt census cross-checked
  against the name-derived `meta_join.us_side` at 4,185/4,185 — **not** the
  winner-derived field (TRAP 7).

**CLUSTERS PRESENT, enumerated per the DEFF procedure:**
1. **MATCH** — 5 games per match, and a harassment tertile holds many games from
   the same match. **Survives.**
2. **OPPONENT** — 19 opponents over 590 games; a tertile holds many games against
   the same one. **Survives.**
⇒ Both live ⇒ **pooled rated DEFF = 1.529** is the applicable constant, and it is
applied to every interval below.

---

## 2. WHY A NEW DECODER — the corpus cannot answer this, and the missing column has a name

**⛔ `corpus/econ.tsv` is the only tape carrying a titanium BALANCE, and its grain
is `file × team × BAND` over exactly four bands** — `r0-150`, `r150-200`,
`r200-300`, `r300+` (`tools/corpus/replay_econ.py:band`). Its `ti_end` column
therefore exists at **four round boundaries and nowhere else**. There is **no
`ti` at r50, r100 or r250 anywhere in `corpus/`**, so the requested trajectory is
not a query, it is a decode. The same is true of the harassment side:
`build_agg.tsv`'s `batk` is banded identically.

Both quantities **are on the wire, per round** — `updatePlayers` (Update field 6)
carries `PlayerState.titanium` / `.titaniumCollected` / `.ammo` for both teams
every round, and `builderAttack` (field 13) carries `{attacker id, target Pos}`.
They were aggregated away at decode time, not unavailable. `tools/x3r0_measure.py`
was read first; it decodes ammo-vs-turret and heal-seat questions and carries no
bank trajectory, so it was not extendable to this.

**The new decoder is cross-validated against the tape it replaces**, on 30 v140
files at `--step 1`:

| check | result |
| --- | --- |
| `ti_us` at round 149/199/299 vs `econ.tsv` `ti_end` for `r0-150`/`r150-200`/`r200-300` | **40 / 40 exact, 0 mismatches** |
| `ticol_us` vs `econ.tsv` `ti_collected_end` | **40 / 40 exact** |
| `eatk_us` ⊆ `build_agg.tsv` `batk` for the enemy team, r0-150 | **0 violations in 19 games**; 1,437 of 1,509 enemy builder attacks (95.2%) resolve onto one of our entities |

**⚠ ONE DEFECT FOUND AND FIXED IN THE DECODER ITSELF, and it is the class of bug
this repo keeps finding: buildings and builder bots share tiles.** A builder bot
may stand ON a conveyor. A single `pos → id` map silently reassigns that belt
tile to the bot, and an enemy attack on the belt then resolves as *"they attacked
a builder bot"* — which is not even a legal target. Measured on the first smoke
file: **16 of 138 enemy attacks mis-resolved, and the belt-attack column read a
clean, plausible, wrong 0.** Fixed by keeping `bldg_at` and `bot_at` separate.
Caught only because an exact zero on a column that should be non-zero is a bug
signature.

**⚠ SAMPLING RATE IS LOAD-BEARING AND NEARLY COST ME THE ANSWER.** The bank is
spiky. At `--step 10` the v140 pool reads **6.7%** of games ever touching 260 Ti;
at `--step 1` the same pool reads **19.7%**. A coarse sample walks straight past
the spikes, and *"does a trigger ever fire"* is exactly a spike question.
**Every threshold number in this document is `--step 1`.**

---

## 3. THE HARASSMENT DEFINITION, AND WHY THIS ONE

**DEFINITION: a z-summed index of four counters, all of them things DONE TO US,
all measured cumulatively at a stated round.**

| component | wire source | why it is admissible |
| --- | --- | --- |
| `eatk_us` | `builderAttack` (13) by an enemy builder whose target tile holds one of OUR entities | the literal pecking in Magnus's sentence |
| `eshots` | `fireTurret` (12) attributed by shooter tile to an enemy turret | turret pressure; melee alone misses half the harassment |
| `obot_deaths` | `removeEntity` (3) of one of our builder bots | **the v140 tree contains no `self_destruct` call** (grepped), so every one is done to us |
| `ebuild_ourhalf` | enemy `placeEntity` of a non-bot nearer OUR core than theirs | the barrier-planting in Magnus's sentence |

**WHAT WAS DELIBERATELY REJECTED AND WHY:**
* **Our conveyor / harvester death counts.** Confounded in the wrong direction:
  `destroy()` is free, uncooldowned and `eco.py` uses it for belt reroutes, so
  our own repairs would be scored as enemy harassment.
* **Game outcome, game length, "we got cut down".** These are **colliders** —
  the thing harassment might cause, not the harassment. They appear in §8 only
  as read-back validation, never as a grouping variable.

**Two label timings are reported, because they answer different questions:**
* **CONTEMPORANEOUS** (§4) — index at round *t*, bank at round *t*. This is what
  a live trigger would actually see.
* **FORWARD-LOOKING** (§5) — index frozen at r100, bank scored over r101-300.
  The label uses nothing after r100, so the bank being scored is strictly in the
  future of the harassment supposed to cause it.

**PREDICTION REGISTERED BEFORE THE CUT** (stated here as it was reasoned, and it
was wrong): *if the stall mechanism is real, the HIGH tertile should show a
higher median bank and a materially higher rate of crossing 260 Ti.*

---

## 4. THE TRAJECTORY — whole population, then split

**Bank, all 590 games** (`ti_us`, n = games still running at that round):

| rnd | n alive | mean | p25 | **median** | p75 | p90 | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 590 | 469.9 | 470 | **470** | 470 | 470 | 470 |
| 25 | 590 | 62.0 | 16 | **42** | 84 | 165 | 267 |
| 50 | 587 | 40.2 | 11 | **27** | 50 | 83 | 269 |
| 100 | 529 | 52.2 | 12 | **40** | 76 | 111 | 414 |
| 150 | 395 | 61.0 | 12 | **48** | 86 | 127 | 632 |
| 200 | 267 | 72.6 | 14 | **58** | 102 | 144 | 648 |
| 250 | 188 | 73.7 | 12 | **42** | 106 | 143 | 701 |
| 300 | 130 | 101.8 | 12 | **42** | 106 | 234 | 1154 |

**This reconciles with the belt census** (median 44 Ti at r150 on v140; this cut
reads 46 on v140 alone, 48 pooled) — two decoders, different code paths,
same answer.

**Read the shape, not just the level: the opening 470 Ti is gone by r25 and the
bank is FLAT for the rest of the game.** It is not a reservoir filling up. It is
a float.

**CONTEMPORANEOUS SPLIT — index at t, bank at t:**

| rnd | n | grp | n | med `eatk` | med `eshots` | **ti med** | ti p75 | ti p90 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 587 | LOW | 196 | 0 | 2 | **45** | 69 | 151 |
| 50 | | HIGH | 196 | 17 | 16 | **16** | 37 | 61 |
| 100 | 529 | LOW | 177 | 12 | 16 | **50** | 90 | 122 |
| 100 | | HIGH | 177 | 48 | 39 | **31** | 65 | 89 |
| 150 | 395 | LOW | 132 | 28 | 28 | **58** | 98 | 151 |
| 150 | | HIGH | 132 | 71 | 64 | **44** | 76 | 115 |
| 200 | 267 | LOW | 89 | 36 | 40 | **58** | 103 | 136 |
| 200 | | HIGH | 89 | 94 | 91 | **49** | 99 | 130 |
| 250 | 188 | LOW | 63 | 40 | 46 | **30** | 68 | 129 |
| 250 | | HIGH | 63 | 123 | 127 | **67** | 113 | 182 |

**The prediction is refuted, and refuted with the sign flipped**: from r50 to
r200 the harassed tertile holds LESS, not more, at the median and at every upper
quantile.

---

## 5. FORWARD-LOOKING CELL — and the exclusion

Index frozen at r100; bank scored over r101-300. n = 177 per tertile.

| grp | n | peak bank med | p75 | p90 | max |
| --- | --- | --- | --- | --- | --- |
| LOW | 177 | **152** | 198 | 278 | 1,154 |
| HIGH | 177 | **105** | 152 | 245 | 723 |

| threshold ever reached in r101-300 | LOW | HIGH | HIGH − LOW | 95% CI (DEFF 1.529) |
| --- | --- | --- | --- | --- |
| ≥ 200 Ti | 23.7% | 13.6% | **−10.2pp** | **[−20.1, −0.2]pp** |
| ≥ 260 Ti | 15.8% | 9.0% | −6.8pp | [−15.2, **+1.7**]pp |
| ≥ 300 Ti | 5.6% | 2.3% | −3.4pp | [−8.4, **+1.6**]pp |

⭐ **STATED AS AN EXCLUSION, per the DEFF direction clause** — a fail-to-exclude
null would be flattered by the widening, so the claim is restated the other way:
**the data exclude harassment raising the 260-Ti fire rate by more than +1.7pp,
and the 300-Ti rate by more than +1.6pp.** The 200-Ti interval additionally
excludes zero in the *negative* direction, which is the opposite of the row's
premise.

---

## 6. WHY THERE IS NO BANK — the income ledger, which is the useful part

Over r20 → r150, 395 games, income defined as harvester deliveries
(`ticol` delta) plus passive 2.5 Ti/round:

| sink | Ti | share of income |
| --- | --- | --- |
| builds + core spawns (residual) | 273,742 | **61.2%** |
| **`convert_ammo`** | 108,763 | **24.3%** |
| heals (1 Ti each) | 37,186 | 8.3% |
| builder attacks (2 Ti each) | 31,518 | 7.0% |
| **change in the bank** | **−3,554** | **−0.8%** |

**Income over that window is ~1,130 Ti per game and the bank ends 9 Ti LOWER
than it started.** The economy is homeostatic by construction: whatever arrives
is spent within a few rounds, a quarter of it swept into ammunition by the core's
conversion branch (`main.py:216-252`).

⭐ **THIS IS THE ACTIONABLE FINDING AND IT REFRAMES THE ROW.** #80 asks *"when we
are sitting on titanium, spend it on kill hardware."* We are never sitting on
titanium **because a sweep already exists and it buys ammunition and eco hands.**
The design question is not *how do we detect a surplus* — it is *which sink wins
when the two compete*. A bank-triggered offense surge that fires at 200 Ti is
competing directly with `ammo_target` and with `LOKI_SURPLUS_TI = 260`, and the
plank has to say which one yields.

**Corroborating mechanism read (v140, 25-round windows):** even in the 29,184
windows where we build **nothing at all**, the bank gains a median of **+1 Ti**
— income of ~112 Ti per window goes to ammo (47.9), heals (26.9) and attacks
(4.9) instead. **Stalling the BUILD channel does not bank titanium**, which is
precisely the assumption #80's harassment premise rests on.

**And harassment does not even stall the build channel.** In the v140 cut, our
builds per round over r100-200 are **0.13 in the HIGH tertile against 0.07 in the
LOW** — under pressure we build *more*, because we are rebuilding.

---

## 7. IF THE ROW IS RE-PRICED: the threshold distribution

Kill-window crossings, 590 games, `--step 1`. Read this as the menu a trigger
designer picks from.

| threshold | fires in r21-300 | median first rnd | **fires before r150** | sustained ≥10 consecutive rnds |
| --- | --- | --- | --- | --- |
| 100 Ti | 78.6% | r32 | 72.2% | 40.3% |
| 150 Ti | 47.3% | r95 | **36.9%** | 21.5% |
| **200 Ti** | **25.6%** | **r67** | **18.5%** | **10.3%** |
| 250 Ti | 17.5% | r106 | 11.2% | 4.4% |
| **260 Ti** (`LOKI_SURPLUS_TI`) | **15.9%** | r118 | 10.0% | 4.1% |
| 300 Ti | 4.6% | r156 | 2.0% | 3.7% |
| 500 Ti | 2.2% | r203 | — | 1.9% |
| **700 Ti** (`LOKI_RICH_TI`) | **1.4%** | r248 | — | 0.5% |
| 1000 Ti | 0.3% | r252 | — | 0.3% |
| **1500 Ti** (`SURGE_TI_FLOOR`) | **0.0% (0 / 590)** | — | **0.0%** | 0.0% |

**Pricing, at the belt census's modelled ~304% scale at r150:** gunner 60 Ti,
sentinel 91 Ti, launcher 60 Ti, builder bot 91 Ti.
⇒ **200 Ti = 3 gunners, or 2 sentinels, or 2 raider bodies.** That is a real
purchase, not a rounding error — and it is available in a quarter of games at a
median r67, comfortably inside the window where the kill has to land.

**The honest counterweight:** only **10.3%** of games hold 200 Ti for ten
consecutive rounds. The crossings are mostly transients. A trigger with any
hysteresis or confirmation delay will fire in far fewer games than 25.6%, so the
mechanism counter QUEUE #80 already demands (surge firings per game before r300)
must be read on the *shipped* gate, not on this table.

---

## 8. CONTROLS

**POSITIVE CONTROL — the same instrument, same columns, on the tiebreak-turtle
era.** If it cannot see a fat bank anywhere, a thin reading proves nothing.

| version | n | med peak | p90 peak | max | **≥1500 Ti** |
| --- | --- | --- | --- | --- | --- |
| v68 | 95 | 135 | 8,115 | 20,186 | **25.3%** |
| v72 | 135 | 202 | 6,960 | 20,144 | **23.0%** |
| v80 | 315 | 195 | 8,849 | 24,565 | **33.7%** |
| v90 | 80 | 401 | 10,237 | 16,111 | **38.8%** |
| v94 | 140 | 146 | 6,560 | 24,068 | **24.3%** |
| v104 | 510 | 138 | 263 | 12,550 | 1.8% |
| **v140** | 360 | 150 | 276 | 11,181 | **0.6%** |
| **v152** | 230 | 147 | 280 | 9,719 | **2.2%** |

**The instrument reads 38.8% on v90 and 0.6% on v140. It is not blind, and
`SURGE_TI_FLOOR = 1500` was calibrated on an economy that no longer exists** —
those trees had median game lengths of 260-673 turns against today's 184-192.
This is a threshold that has outlived its distribution, exactly as QUEUE #71
argues about `SURGE_MIN_RND`.

**NEGATIVE CONTROL — md5(file) parity, same statistics, same population:**

| arm | n | peak bank med | p90 | ever ≥260 |
| --- | --- | --- | --- | --- |
| arm0 | 293 | 133 | 265 | 11.6% |
| arm1 | 236 | 139 | 268 | 14.8% |

A meaningless split moves the median peak by 6 Ti and the fire rate by 3.2pp.
The harassment split moves them by **47 Ti and 6.8pp** — larger than noise, and
**pointing the wrong way for the row.**

**INSTRUMENT DISCRIMINATION — does the index track real damage?** (Read *after*
the split; none of these built it.)

| grp | n | belt alive @r150 | harvesters @r150 | turrets @r150 | median game length | win rate |
| --- | --- | --- | --- | --- | --- | --- |
| LOW | 177 | **39** | 5 | 2 | 209 | **63.8%** |
| HIGH | 177 | **15** | 4 | 1 | 187 | **42.4%** |

The index cuts our surviving belt by 62%, costs 21pp of win rate and shortens the
game by 22 rounds. **It is measuring harassment.** The null in §5 is therefore a
null about the bank, not a null about the instrument — which is the distinction
the brief asked to be able to make.

---

## 9. THE SURPRISE, FLAGGED BEFORE IT IS EXPLAINED AWAY

**At r250 the contemporaneous split FLIPS: the HIGH tertile holds a median 67 Ti
against LOW's 30, and 6.3% of HIGH games are above 260 Ti against 1.6% of LOW.**
This is the one cell in the entire cut that supports the proposer's mechanism,
and it is the cell his sentence describes most literally — a long, grinding,
pecked game where our spend has finally run out of places to go.

**Now the explanation, and it is why the cell does not rescue the row:** n = 63
per tertile, the 22% of games still running at r250 are a survivorship-selected
slice, and **r250 is past the point where `DEFENCE_ADMISSION_BAR` says the kill
should have landed.** A trigger that only becomes true in games we are already
losing on the programme's clock is `SURGE_MIN_RND = 300`'s defect wearing a
different number. **It is written down anyway, because it is the shape Magnus
described and it is the cell a future cut should re-read at higher n.**

**Second, smaller surprise:** the enemy's builder attacks on us land almost
entirely on **barriers** — in the smoke sample, 115 of 138 resolved enemy attacks
hit our barrier seal, 0 hit our belt. Our belt is not what gets pecked; our wall
is. That is a finding for the seal planks, not for this one.

---

## 10. WHAT THIS SAYS TO QUEUE #80

1. **The GO/NO-GO precondition as written resolves NO-GO.** Harassed games do not
   accumulate a bank; they accumulate less than clean games. Any version of the
   row that *conditions the surge on being harassed* should be dropped.
2. **The row is not dead — its threshold is off by a factor of seven.** A
   200-Ti gate fires in 25.6% of games at median r67; the shipped 1500-Ti gate
   fires in 0 of 590. Re-pricing is a one-constant change and the mechanism
   counter can be read immediately.
3. ⛔ **CORRECTION TO THE ROW'S GREP.** "ZERO bank-triggered offensive spend"
   overstates it: `main.py:263-268` already buys extra builder-bot seats at
   `LOKI_SURPLUS_TI = 260` (+3 seats) and `LOKI_RICH_TI = 700` (+3 more), with
   the comment *"surplus bank is turned into bodies"*. **Measured, the 260 gate
   fires in 15.9% of games and the 700 gate in 1.4% — `LOKI_RICH_TI` is dead
   code on the current distribution.** Whatever #80 builds must be designed
   against that existing gate, not beside it.
4. **The real competition is `convert_ammo`, which already eats 24.3% of
   income.** A surge that spends the same titanium on hardware is taking it from
   the magazine. That trade is the plank, and it is testable locally without a
   bank trigger at all: hold the trigger fixed and move `ammo_target`.

---

## 11. REPRODUCING THIS

```bash
# decode (all 4,190 joined ladder games, ~35 s on 5 workers)
.venv/bin/python tools/bank_under_harassment.py /tmp/traj.tsv --step 1 --max-round 1000
# every cell above
.venv/bin/python tools/bank_under_harassment.py --report /tmp/traj.tsv 140,152
```

`--step 1` is not optional for any threshold claim (§2). The trajectory TSV is
~1.4 M rows / ~200 MB and is deliberately **not** committed to `corpus/` — it is
a derived view, rebuildable in under a minute, and the corpus already carries the
banded form in `econ.tsv`.
