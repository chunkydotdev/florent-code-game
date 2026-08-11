# THE NIGHT PANEL: v104 SITS ON ELO PAR, AND THE DEFICIT IS NOT WHERE WE THOUGHT

**Research arm, s29, 2026-08-11 ~04:1xZ.** Commissioned by the builder arm as
assignment 1 of the session. Population fired by `tools/night_collector.sh`
2026-08-10 21:03Z → 03:46Z.

**Version tag:** our live/active bot **v104** for all 485 games. Corpus synced
2026-08-11 03:5xZ (16,766 replays, 0 new to decode, reconciliation 2,305/2,305 =
100.0000%). Dirs read: `corpus/meta_join.tsv`, `corpus/league_matches.tsv`,
`elo_history.tsv`, `scratchpad/arm_night.txt`.

---

## POPULATION — verified on the wire, not accepted on relay

97 match ids (`scratchpad/night_matchids.txt`) → **485 game rows in
`corpus/meta_join.tsv`**.

| check | result |
|---|---|
| `ourver` | **104 in 485/485** |
| `triggeredBy` | **`unrated` in 485/485** |
| rows in `corpus/ladder_games.tsv` | **0** |
| rows in `corpus/league_matches.tsv` | **0** |
| `us_side` a / b | 280 / 205 |

**This is UNRATED and it is its own population. It must never be pooled with
rated ladder rows** (D37: `meta_join` covers rated *and* unrated, and pooling
them counts our own prototype legs as opponent record).

**It is also SHIPPED-vs-SHIPPED, which is the good case.** v104 is the incumbent,
not a prototype, so the usual unrated-vs-ladder confound (unrated pools
PROTOTYPES, ladder pools SHIPPED BOTS) does not apply to this sample.

**D18 — the opponent's version IS pinned here**, and `meta_join` is the right
surface for it because these matches do not appear in `league_matches` at all.
**Their version moved mid-sample in 3 of 9 cells:** farming_200s v12→v13 (10/50),
kladde v86→v87 (40/15), CtrlAltDefeat v131→v132 (10/40).

---

## 1. GAME SHARE (us-only, unrated, n=485)

| opponent | W | n | share | their versions in-sample |
|---|---:|---:|---:|---|
| Powerpuff Girls | 39 | 50 | 0.780 | v57 |
| CtrlAltDefeat | 39 | 50 | 0.780 | v132(40) v131(10) |
| I Stone | 39 | 55 | 0.709 | v22 |
| gsxWins | 37 | 55 | 0.673 | v22 |
| Lunds Stallions | 36 | 55 | 0.655 | v64 |
| Landers | 34 | 55 | 0.618 | v93 |
| Team 48 | 24 | 50 | 0.480 | v17 |
| kladde chatte tville (och oss) | 19 | 55 | 0.345 | v87(15) v86(40) |
| farming_200s | 15 | 60 | 0.250 | v13(50) v12(10) |
| **TOTAL** | **282** | **485** | **0.581** | |

---

## 2. ⭐ THE READ THAT MATTERS: S − E, NOT S

The ladder pays `delta = 32 × (S − E)` (residual 0.000000 across 100 matches,
0.0000 across 678 — established s28). **So the quantity is the gap to Elo
expectation, not raw share.**

Ratings are **window-contemporaneous**, not current: ours = `elo_history` mean
**1675.0** over the collection window (n=77 rows, range 1660–1688); theirs =
`league_matches.ratingXBefore` mean over 2026-08-10T21:00Z–2026-08-11T03:50Z
(n_obs = 20 each).

| opponent | gap | n | S | E | **S−E** | Elo/match | their in-window swing |
|---|---:|---:|---:|---:|---:|---:|---:|
| **farming_200s** | +32.7 | 60 | 0.250 | 0.453 | **−0.203** | **−6.50** | **119.0** |
| **Team 48** | −89.9 | 50 | 0.480 | 0.627 | **−0.147** | **−4.69** | 40.1 |
| kladde | +46.7 | 55 | 0.345 | 0.433 | −0.088 | −2.81 | 62.6 |
| gsxWins | −107.4 | 55 | 0.673 | 0.650 | +0.023 | +0.73 | 63.4 |
| Landers | −44.1 | 55 | 0.618 | 0.563 | +0.055 | +1.76 | 37.6 |
| Lunds Stallions | −62.7 | 55 | 0.655 | 0.589 | +0.065 | +2.09 | 33.1 |
| Powerpuff Girls | −136.7 | 50 | 0.780 | 0.687 | +0.093 | +2.97 | 42.9 |
| I Stone | −68.2 | 55 | 0.709 | 0.597 | +0.112 | +3.59 | 36.9 |
| CtrlAltDefeat | −87.7 | 50 | 0.780 | 0.624 | +0.156 | +5.00 | 39.8 |
| **POOLED (n-weighted)** | | **485** | **0.581** | **0.577** | **+0.004** | **+0.14** | |

### (a) POOLED, v104 IS EXACTLY AT PAR — +0.004 share, +0.14 Elo/match over 485 games

Not bleeding, not climbing: *at* its rating. **Whatever the −438.6 Elo bleed-band
figure is measuring, it is not a uniform deficit spread across our diet**, because
nine cells and 485 games aggregate to zero. This is the strongest constraint the
sample places on the bleed hypothesis, and it redirects the mechanism hunt from
*"why is v104 weak"* to *"which specific cells, and why those"*.

### (b) THE DEFICIT IS NOT MONOTONE IN OPPONENT STRENGTH — 2 of 3 are teams BELOW us

**`Team 48` sits 90 points below us and returns −0.147 (−4.69 Elo/match).** By the
loss-cost arithmetic (CLAUDE.md, s28), a 0–5 there costs **−19.96** against
**−11.93** at farming_200s. **Underperforming a weaker team is the most expensive
failure mode available, and we have one.**

### (c) RAW SHARE MISRANKS AT LEAST ONE ADJACENT PAIR

Powerpuff Girls and CtrlAltDefeat both read **0.780** — but at −136.7 the expected
share is 0.687, so **Powerpuff Girls (+0.093) is a worse result than I Stone at
0.709 (+0.112)**. Ranking panel cells by raw share inverts real ordering.

### Per-cell significance — A SCREEN, NOT A TEST

Two-sided binomial vs E, **games treated as independent, which they are not** —
they are clustered in 5-game matches on shared maps, so these p-values are
**anti-conservative**:

farming_200s **0.0016** · CtrlAltDefeat 0.028 · Team 48 **0.040** · I Stone 0.100
· Powerpuff Girls 0.172 · kladde 0.221 · Lunds Stallions 0.341 · Landers 0.497 ·
gsxWins 0.779.

---

## ⚠ THE CAVEAT ON THIS DOCUMENT'S OWN HEADLINE

**`farming_200s` swung 119 rating points inside the collection window**
(1644.1 → 1763.1) — by far the least stable gap of the nine, and it carries the
largest number here. On **current** ratings (1753 vs our 1663, gap +90) the same
games give **−0.123**, not −0.203.

**The SIGN and the RANK are robust to the choice of rating epoch. The MAGNITUDE
is not.** −6.50 Elo/match must not be quoted without this.

---

## 3. WHAT IT PAYS — `tools/target_value.py`, all nine cells

```
TARGET BAND: gaps -132..+90, a 5-0 pays 10.22..20.07, reachable 5/9
```

**The two cells we underperform most are the two highest-paying reachable cells
on the board**: farming_200s (+90 on current ratings, p96 of 147 observed
pairings, 5-0 pays **+20.07**) and kladde (+51, p87, **+18.33**).

**The two cells we beat hardest are both OUT OF BAND**: Powerpuff Girls (−121)
and CtrlAltDefeat (−83), both flagged `** NO **`.

So the panel was not wasted — but **four of nine cells are unreachable**, and a
re-fire should weight toward the reachable band.

---

## STATUS — D12: THIS PRIORITISES, IT DOES NOT ESTABLISH

Observational, on one unrated window, no treatment and no control. It nominates
**farming_200s** and **Team 48** as the two cells worth a mechanism hunt, and it
retires *"v104 has a general deficit"* as a description of this sample. **It
closes no road** — under `FIXTURE_OF_RECORD: live_unrated` and the standing rule
that a refutation without live-game backing is a hypothesis, nothing here retires
anything.

**Open, and handed to running agents rather than answered here:** the loss anatomy
(kill-round vs cored-round per cell; fraction of losses landing before our own
median kill round, rated comparator 39%) and what separates the deficit cells
from the surplus cells, including the within-cell opponent-version split in the
three cells where D18 fires.

---

# PART 2 — LOSS ANATOMY, AND THE RACE FRAME IS STALE

*Appended ~04:3xZ. Same population. Join validated in three directions with a
flipped negative control; the independent check tallies the sidecar's
`scoreA`/`scoreB` against the replay-internal winner field: **97/97 matches,
flipped 0/97**. All 97 score lines are asymmetric, so the flip cannot pass by
symmetry. Unplanned exact reconciliation: **448/448 core-death games end at
exactly `turns-1`; 37/37 no-core-death games ran exactly 1000 turns.***

## ⭐ THE RACE FRAME IS A SNAPSHOT AT 2026-08-10T19:12:59Z AND ITS HEADLINE HAS HALVED

The builder's standing frame — *"107/109 v104 losses are CORE DEATHS, median
margin **+39** rounds in our favour, and we still lose 45%"* — could not be
reconciled against a 166-loss denominator. **Resolved: every number is correct,
at a cutoff 125 games ago.** Filtering `ladder_games.tsv` to `ourver=104` and
cutting at the creation time of the 109th loss:

| | kill median | death median | **margin** | core-death losses |
|---|---:|---:|---:|---:|
| **at that cutoff** (240 rows) | r170 | r209 | **+39** | 107/109 = 98.2% |
| **now** (365 rows) | r176 | r193 | **+17** | 163/166 = 98.2% |

**The margin more than halved and it moved from BOTH ends** — our kill 6 rounds
slower, their kill of us 16 rounds faster. The loss *mode* is unchanged (98.2%
core deaths, identical to the digit). **The race tightened.** Any plank sized
against +39 is sized against a number that no longer exists.

## THE ANATOMY (485 unrated games, us-only, v104)

448/485 decided by core death (92.4%), 37 to r1000 (7.6%).
- core-kill wins **n=271, median r169** (q1 126, q3 252) + 11 r1000 wins
- core-death losses **n=177, median r202** (q1 108, q3 340) + 26 r1000 losses

**Losses landing before our own median kill round: 74/203 = 36.5%** (all losses)
/ **74/177 = 41.8%** (core-death only). Rated comparator, recomputed
independently from `ladder_games.tsv`: **72/166 = 43.4% / 72/163 = 44.2%.**
**Same regime — the night population does not contradict the rated frame.**

| opponent | n | share | kill-W | medK | death-L | medD | loss<r169 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Team 48 | 50 | .480 | 24 | **140** | 25 | **93** | **23/26 = 88.5%** |
| farming_200s | 60 | .250 | 15 | **107** | 42 | 158 | 27/45 = 60.0% |
| gsxWins | 55 | .673 | 37 | 121 | 17 | 134 | 10/18 = 55.6% |
| CtrlAltDefeat | 50 | .780 | 34 | 187 | 9 ⚠ | 254 | 3/11 = 27.3% |
| Landers | 55 | .618 | 34 | 166 | 15 | 252 | 5/21 = 23.8% |
| Lunds Stallions | 55 | .655 | 35 | 189 | 14 | 238 | 4/19 = 21.1% |
| I Stone | 55 | .709 | 39 | 198 | 15 | **357** | 1/16 = 6.2% |
| kladde | 55 | .345 | 19 | 164 | 35 | **323** | 1/36 = **2.8%** |
| Powerpuff Girls | 50 | .780 | 34 | 182 | 5 ⚠ | **663** | 0/11 = 0.0% |

⚠ loss-side median on <10 obs — not to be quoted alone. Buckets over the 177
core-death losses: **zero** before r50 · 20.9% <r100 · 36.7% <r150 · 48.6% <r200
· 69.5% <r300 · 92.1% <r500.

## FOUR SURPRISES, RECORDED BEFORE BEING EXPLAINED AWAY

**(a) The 36.5% aggregate is two disjoint modes with no middle.** Three cells
(Team 48 88.5%, farming_200s 60.0%, gsxWins 55.6%) supply **60 of the 74** early
losses; six cells sit at 0–27%. ***"We get rushed" is false as a description of
the field*** — a third of it rushes us and the rest does not. **A plank aimed at
early-rush survival would be inert in six of nine cells.**

**(b) 63.5% of losses (129/203) land AFTER our own median kill round.** Against
kladde we lose 36 of 55 and **35 of those 36 come after r169, median r323**,
while our own median kill there is r164. Same shape at I Stone (94% late) and
Powerpuff (100% late). **The larger bucket is games we are alive in, past the
round at which we normally win, and do not finish.** *Timing is MEASURED;
"conversion problem" is INFERENCE from it and is flagged as such — two analysts
converged on this story quickly and it deserves an adversarial look before it
becomes a plank.*

**(c) Early-loss rate does not track game share.** kladde is our 2nd-worst cell
(.345) with the 2nd-*lowest* early-loss rate (2.8%); Powerpuff is our best (.780)
at 0%; gsxWins is a good cell (.673) at 55.6%. **Dying early explains exactly one
cell: Team 48** — medD r93 against our medK r140. **The same cell Part 1 flags at
S−E = −0.147 (p=0.040), 90 points BELOW us, where a loss costs −19.96. Two
independent reads land on one cell, with a named mechanism: they kill in r93 and
we need r140.**

**(d) The metric is unstable to which median you use, in one cell.**
farming_200s reads **60.0%** against the global r169 but **17.8%** against its own
cell median r107. gsxWins moves 55.6→44.4. The other seven are identical either
way. **Any headline must state the median it was measured against.**

## OPEN, NOT CLOSED
**r1000 rate is ~4x higher unrated than rated: 37/485 = 7.6% vs 7/365 = 1.9%**
(rated side verified independently: 7/365, W4/L3). Under `R1000_IS_DEFEAT` all 37
are defeats, including the 11 we "won". Opponent mix or a real unrated/rated
difference — not isolated, not closed.

## DECODER TRAP, for the repo's memory
**`max event round` is NOT a game-length proxy.** All 37 non-core-death games ran
1000 turns, but their last BUILD/DEATH event ranged **r31–r999** — a first pass
produced "a 31-round game with no core death", which is just a game that stopped
building. Real lengths come from the replay's field-3 turn buffers. **Caught by
the 448/448 + 37/37 known-answer reconciliation, not by inspection.** Also: one
game carries two core deaths (gsxWins, both r69) — counted as a kill, excluded
from the death distribution.

---

# ⛔ PART 3 — SELF-CORRECTION: PART 2's TREND CLAIM IS WITHDRAWN

*Appended ~04:5xZ, about 20 minutes after Part 2 was relayed and adopted by the
builder arm. **The correction is late — it reached a lane before it reached me.***

**WHAT I CLAIMED:** *"The margin more than halved and it moved from BOTH ends —
our kill 6 rounds slower, their kill of us 16 rounds faster. The race tightened."*

**THE METHOD ERROR: I compared a SUBSET to the WHOLE** (first 240 games against
all 365) **and reported the difference as change over time.** That is not a period
comparison and it is guaranteed to understate the movement. Disjoint periods:

| period | n | share | killW | medK | deathL | medD | **margin** |
|---|---:|---:|---:|---:|---:|---:|---:|
| EARLY (≤ cut) | 240 | .546 | 129 | r170 | 107 | r209 | **+39** |
| LATE (> cut) | 125 | .544 | 66 | r182 | 56 | r172 | **−10** |

So the true pooled movement is **+39 → −10 (−49 rounds)**, larger than reported —
**and still not established:**

- **Permutation test, 5,000 shuffles of the period label: p = 0.123**, and that
  **understates** p because games are clustered in 5-game matches. Clears nothing.
- **UNCONTROLLED CONFOUND — opponent composition.** Mean opponent rating is flat
  (1658.6 vs 1659.7) but the *teams* turned over almost entirely (early:
  kladde/farming_200s/Landers/Askar City; late: SmartFridge/diverge/Landers/Askar
  City). **Part 1 of this very document measures per-cell median kill rounds
  spanning r107–r198 — a 91-round spread.** Composition alone can move a pooled
  median by 12 rounds with nothing about our bot changing.
- **Within-opponent** (11 opponents with ≥5 games in both periods): median margin
  change **−51**, negative in 8 of 11 — directionally consistent, but per-cell n
  is 1–4 kill/death observations and the swings run **+254 to −282**. Noise with
  a tilt.

**WHAT SURVIVES:**
- ✅ **`+39` is computed on 240 of 365 available v104 games; the full-sample
  figure is `+17`.** A stale cutoff is a stale cutoff — arithmetic, unaffected.
- ✅ The 98.2% core-death share is stable to the digit across both cuts.
- ❌ **"The race tightened" / "moved from both ends" — WITHDRAWN.**

**THE LESSON, against this lane specifically.** The s28 wrap recorded that this
arm's checks fired on every other lane's work and never on its own. This one
fired on its own — **and it fired after the relay rather than before it**, which
is the same failure one step smaller. **A trend claim needs a disjoint-period
comparison and a composition control BEFORE it is sent, not after it is adopted.**

---

# ⛔ PART 4 — TEAM 48'S PROMOTION DOES NOT REPLICATE ON THE RATED SURFACE

Part 1 and Part 2 converged on Team 48 from two independent instruments and it was
promoted on that convergence. **A third surface inverts the sign.**

```
v104 UNRATED (night):  24/50  = 0.480    S-E = -0.147
v104 RATED          :   7/10  = 0.700    S-E = +0.107   (mean gap -65.7)
all-version RATED   : 113/180 = 0.628
```

**Both confounds are dead, which sharpens the contradiction rather than softening
it.** Same our-version (v104 on both sides). **D18 satisfied cleanly: Team 48 has
been on `v17` continuously since 2026-08-09T22:02Z**, verified across their whole
`league_matches` timeline — their bot is identical across both samples.

**What remains is power: the rated arm is 10 games = TWO MATCHES.** Fisher exact
two-sided **p = 0.302** (games as units, which already overstates). **The rated
sample cannot refute the unrated finding — but it is the only other evidence and
it points the other way.**

**Pairing frequency:** 180 rated game rows / 36 matches all-version = 4.99% of our
3,610-game rated diet, most recent 2026-08-10T17:32Z (current, not historic) —
but **only 10 of v104's 365 rated games (2.7%)**, not in v104's top 12 opponents.

**REVISED RECOMMENDATION, against this document's own earlier framing:** keep Team
48 as a **mechanism lead** — medD r93 against our medK r140 is a real, named,
measured gap — and **drop it as a currency target.** 2.7% of the rated diet, at
the reachable-band edge, rated sample inverted. **Cheap resolution: unrated games
are free; 50 more against Team 48 v17 settles whether 0.480 or 0.700 is real, at
a rate-limit cost and no rating cost.**

---

# PART 5 — WHAT SEPARATES THE CELLS, AND THE LARGEST EFFECT IN THE HARVEST

## ⛔ THE LAUNCHER RAID DELIVERED NOTHING — 0 of 4,169, with an INTERNAL control

```
NIGHT (485 games, unrated, v104), throws by thrower team (`throws.tsv.tteam`):
  OURS    4,169 throws   reached  124 (2.97%)   any_atk    0 (0.00%)   core_atk   0 (0.00%)
  THEIRS  2,258 throws   reached  102 (4.52%)   any_atk  107 (4.74%)   core_atk   7 (0.31%)
```

**The control is the opponent's own column: same decoder, same 485 files, same
fields — non-zero for them, zero for us.** That excludes a dead code path and a
broken column together, and it is stronger than the corpus-wide alive-check
(core_atk>0 in 1,749 rows). **We throw 1.8x as often as the field and convert
none of it.** Uncorrelated with the split in both directions (2.4 throws/game vs
CtrlAltDefeat at 0.780; 16.9 vs I Stone at 0.709).

*Instrument note, recorded rather than buried: the first verification pass keyed
on a column named `team`, which does not exist in `throws.tsv` (it is
`tteam`/`bteam`). It returned a clean, plausible **0** for every field. **A wrong
key name produces a constant zero indistinguishable from a finding** — the fourth
constant-column incident logged on this project. Caught only because it
disagreed with the agent's number.*

## THE CELL SET CHANGES MEMBERSHIP UNDER ELO NORMALISATION

| opponent | opp Elo | E | actual | residual |
|---|---:|---:|---:|---:|
| CtrlAltDefeat | 1589 | 0.622 | 0.780 | **+0.158** |
| I Stone | 1607 | 0.599 | 0.709 | +0.110 |
| Powerpuff Girls | 1536 | 0.687 | 0.780 | +0.093 |
| Lunds Stallions | 1612 | 0.588 | 0.655 | +0.066 |
| Landers | 1633 | 0.559 | 0.618 | +0.059 |
| gsxWins | 1561 | 0.657 | 0.673 | +0.015 |
| **kladde** | 1722 | 0.431 | 0.345 | **−0.085** |
| **Team 48** | 1588 | 0.622 | 0.480 | **−0.142** |
| **farming_200s** | 1713 | 0.448 | 0.250 | **−0.198** |

Independently reproduces Part 1 on a different rating epoch (−0.088 / −0.147 /
−0.203). **kladde's −0.085 sits inside the spread of cells we call wins — they are
a better team, not an anomaly.** The genuine anomalies are **farming_200s and
Team 48**.

**⭐ A NATURAL CONTROL, better than any Elo normalisation: Team 48 rated 1588.2,
CtrlAltDefeat rated 1588.6, n=50 each — 0.480 vs 0.780. Same rating to within
half a point, 30pp apart.** *(Unrated surface. Part 4's correction stands: v104's
RATED record vs Team 48 is 7/10 = 0.700, inverted, n=2 matches.)*

## THE MECHANISM: THE DOORSTEP-TURRET CONTEST

Turrets planted deep in the opponent's half — **scale-free ratio
`d²_own/(d²_own+d²_enemy) > 0.8`**, per 100 rounds of actual game length.
*(Absolute `d²_enemy ≤ 25` is a map-size artifact on 10x10, where half the board
qualifies; conclusions use the scale-free form.)*

| opponent | share | OURS/100r | THEIRS/100r | us:them | never plant deep |
|---|---:|---:|---:|---:|---:|
| Powerpuff Girls | 0.780 | 4.02 | 0.23 | 17.3 | 2.0% |
| kladde | 0.345 | 2.98 | 0.84 | 3.5 | 5.5% |
| CtrlAltDefeat | 0.780 | 1.68 | 0.58 | 2.9 | 24.0% |
| **gsxWins** | 0.673 | 0.64 | **1.32** | **0.49** | 23.6% |
| **Team 48** | 0.480 | 0.47 | **2.40** | **0.20** | **38.0%** |
| **farming_200s** | 0.250 | 0.34 | **1.66** | **0.21** | **40.0%** |

**Only three cells invert the ratio and two are the anomalies.** Downstream: vs
farming/Team 48 our Ti collected is **452/544 per game** against 3,417–4,867 in
the dominated cells; ammo converted 389/403 vs 626/1,268; whole-game shots
40.5/40.0 vs 54.6/113.4. **We are pinned in our own half, never fund the battery,
never fire.** Censoring removed (conditioned on surviving to r150) we still never
plant deep in **66.7%** of farming games and **57.1%** of Team 48 games, against
6.5–7.5% in kladde/Powerpuff. **A plank failure, not an opponent-strength story —
the only mechanism surviving Elo normalisation.**

**Team 48's rush is timeable and map-conditional:** median kill **r78–95** on the
four larger maps with 40–60% of games decided by r100, and **0% by r100 on 10x10**
(median kill r532). Pure forward gunners (96.3% of their mix), **zero
builder-attacks across all 50 games.** *Independently consistent with Part 2's
Team 48 medD r93 — two agents, two methods, one number.*

Our own offence stalls where they win: cause-specific kill hazard in r150–200 is
25–36% in dominated cells and collapses to **8.7% (kladde)** and **3.3%
(farming)**. **Team 48's is normal at 28.6% — their edge is entirely the r0–100
rush**, a different failure mode from the other two.

## ⭐ THE SURPRISE: OPPONENT × MAP IS THE LARGEST EFFECT HERE, AND IT CANCELS IN EVERY POOLED STATISTIC

The map panel is **perfectly balanced** — each cell exactly 10–12 games on each of
five maps — so this is not sampling. **Pooled share by map is nearly flat
(0.485–0.633), and that flatness is an average of ±0.3 within-map spread.**

10x10 vs all bigger maps, Fisher exact two-sided, 9 tests, Bonferroni α=0.0056:

| opponent | 10x10 | bigger | p |
|---|---:|---:|---:|
| **kladde** | 9/11 = **0.82** | 10/44 = **0.23** | **0.0005** ✅ |
| **Landers** | 2/11 = **0.18** | 32/44 = **0.73** | **0.0015** ✅ |
| Team 48 | 8/10 = 0.80 | 16/40 = 0.40 | 0.035 |
| gsxWins | 4/11 = 0.36 | 33/44 = 0.75 | 0.028 |
| farming_200s | 1/12 = 0.08 | 14/48 = 0.29 | 0.26 |

**kladde's entire deficit is one map class** — on 10x10 they are our best cell in
the whole population, on everything bigger our worst. **And Landers, a cell we
"win" at 0.618, is the exact mirror at the same effect size.** Nothing about
small or large maps is true *for us*: **the map decides whose plan is legal, and
in opposite directions for different opponents.**

**⇒ Every map-pooled read this project has run has averaged over a ±0.3 spread
that cancels.** That is a statement about our measurement practice, not about
v104.

## TWO MORE CLEAN NULLS

- **CPU is not it.** Our timeouts: **1 event across 485 games**; cpu_max 3.7–4.1ms
  against a 10ms budget, flat across cells. Theirs: 1,822 timeout events in 31
  games, **98% of them Lunds Stallions — a 0.655 cell.**
- **The archive turret-mix prior does not reproduce here.** Powerpuff **95.3%
  gunner** → 0.780; farming **100.0% gunner** → 0.250; kladde **67.4% sentinel**
  → 0.345; I Stone 43.7% sentinel → 0.709. **The field's mix on this panel is
  BIMODAL**, so the archive-wide 69.8/23.2/7.0 is a blend of two clusters no
  single opponent occupies. **This does not refute the archive measurement** — it
  says the average is not a description of any opponent.

## D18 VERSION SPLITS — ALL THREE UNDERPOWERED, ALL NULL, NOT TO BE READ
farming v12 0.40 → v13 0.22 (p=0.25) · kladde v86 0.40 → v87 0.20 (p=0.21) ·
CtrlAltDefeat v131 0.70 → v132 0.80 (p=0.67). Map mix balanced across every
version arm. **MDE ~40pp against observed gaps of 18–20pp.** Both losing cells
move in the "they shipped a counter" direction and neither is resolvable.

---

# PART 6 — THE r1000 GAP, CONTROLLED BY THE SIDE LANE (their cut, cited not restated)

The side lane took Part 2's open item (*r1000 rate 7.6% unrated vs 1.9% rated*)
and ran the control this document failed to name: **`night_collector.sh` pins
five maps, so the unrated population is a FIVE-MAP population and the rated
comparator spans twenty.** That omission was ours.

Their result, all `ourver=104`, `ladder_games.tsv`, `turns>=1000`:

| rated cut | r1000 | rate |
|---|---|---|
| all maps, all opponents | 7/365 | 1.9% |
| the 5 panel maps only | 3/121 | 2.5% |
| the same 9 opponents, all maps | 4/150 | 2.7% |
| **same 9 opponents AND the 5 maps** | **1/44** | **2.3%** |

**Neither map pool nor opponent mix explains the gap — both cheap explanations
are independently excluded.** But jointly controlled the cell is **one event in
forty-four**:

```
unrated 485 vs rated ALL          37/485 vs 7/365   Fisher p = 0.0001
unrated 485 vs rated SAME-9 opp   37/485 vs 4/150   Fisher p = 0.0350
unrated 485 vs SAME-9 + 5 maps    37/485 vs 1/44    Fisher p = 0.3531
```

**AGREED STATEMENT: the two cheapest explanations are each excluded, and the
jointly-controlled cell cannot resolve it at this n. NOT "established".** Their
own caveats, all correct: p-values treat games as independent when they cluster
in 5-game matches (the 0.0350 weakens most); **D18 is not satisfied across the
comparison** — the rated comparator spans v104's whole life, so the two samples
do not share an opponent-version era; seat uncontrolled (we initiate every
unrated challenge, the ladder assigns rated pairings).

**WHY IT MATTERS IF IT HOLDS:** `FIXTURE_OF_RECORD: live_unrated` plus
`R1000_IS_DEFEAT: yes` would mean **our fixture of record produces the outcome
the programme calls a defeat at 3–4x the rate the ladder does** — a statement
about the instrument, touching every leg we fire. **Powered version is buyable
with free unrated windows rather than arguable.**

---

# ⛔ PART 7 — PART 5's LAUNCHER-RAID HEADLINE IS WITHDRAWN, AND THE CORRECTED CUT FOUND A REGRESSION

*Appended ~05:2xZ. **Part 5's "THE LAUNCHER RAID DELIVERED NOTHING — 0 of 4,169"
is WRONG and is struck.** Caught by the builder arm after this document was
committed and pushed at `9a809d1`. This is the second retraction in this file and
the first one caught by another lane.*

## WHY IT WAS WRONG — confirmed at source, not accepted on relay

`tools/corpus/replay_throws.py:157,164` defines the outcome columns against
**the THROWN bot's own enemy**:
```python
if b is not None and tgt in foot[1 - b.team]:   # b = the THROWN bot
    rec["core_atk"] += 1
```
**For a KIDNAP, `b.team` is the enemy, so `foot[1 - b.team]` is OUR core** — the
column counts *the kidnapped bot coming back and hitting us*. Read literally it
is a **success** column for the kidnap, not a failure column. And `reached` at
0.00% over 172,547 cross-team throws is physically impossible as a real result,
which is proof on its own that the column is not measuring what was assumed.

**The split, using the `kind` column that was in `throws.tsv` all along and that
neither the agent nor this lane used:**

| thrower | class | n | reached | any_atk | core_atk |
|---|---|---:|---:|---:|---:|
| OURS | KIDNAP (EXILE) | **3,727 (89.4%)** | 0.00% | 0.00% | 0.00% |
| OURS | SELF-INSERT | 442 (10.6%) | 28.05% | 0.00% | 0.00% |
| THEIRS | KIDNAP (EXILE) | 1,927 | 0.00% | 0.00% | 0.00% |
| THEIRS | SELF-INSERT | 317 | 32.18% | 33.75% | 2.21% |

**89.4% of the 4,169 were kidnaps, whose columns cannot populate by
construction.** The "ours vs theirs" control in Part 5 compared **our kidnaps
against their self-inserts** — not the same quantity on both sides, which is
precisely the apples-to-oranges shape that control was written to exclude.
**"Same column" is not "same meaning" when the column is defined against a
per-row team.** Kidnap effectiveness has **no column in this table at all**;
measuring it is a decoder gap, not a null result.

## ⭐ BUT THE COMMENSURABLE HALF SURVIVES, AND IT IS A REGRESSION IN OUR OWN BOT

Restricted to `kind=INSERT` only — apples to apples — the zero does not go away,
**and it is ours alone.** RATED corpus, `join.tsv` authoritative `our_team`:

| era | who | n | reached | any_atk | core_atk |
|---|---|---:|---:|---:|---:|
| pre-v102 | OURS | 633 | 18.6% | **511 (80.7%)** | 111 (17.5%) |
| pre-v102 | THEIRS | 3,310 | 28.8% | 647 (19.5%) | 272 (8.2%) |
| **v102/104** | **OURS** | **475** | **38.1%** | **0 (0.0%)** | **0 (0.0%)** |
| v102/104 | THEIRS | 587 | 27.4% | 124 (21.1%) | 20 (3.4%) |

**Every one of our versions, with our own back-catalogue as the positive control:**
v65 100% · v67 84.6% · v68 80.8% · v69 100% · v70 83.3% · v71 90.9% · v72 80.0% ·
v74 71.4% · v75 100% · v76 65.8% · v79 85.7% · v80 87.5% · v84 83.3% · v86 66.7% ·
v89 70.0% · v90 81.2% · v91 82.6% · v92 100% · v94 81.4% · v101 100% (n=3) —
**then v102 (n=232) 0.0% and v104 (n=243) 0.0%.**

**Nineteen consecutive versions at 66–100%, then exactly zero twice on the two
largest samples in the table.** `P(0 in 475 | p = 0.807)` underflows to 0.

**THE DECODER-BREAK ALTERNATIVE IS DEAD.** In the **same v102/104-era files**, the
**opponents'** self-inserts still populate `any_atk` at **21.1% (124/587)** —
`builderAttack` events decode normally in those replays. **The events are there;
ours are not being generated.**

**AND THE DIRECTION IS THE WORST ONE: our reach rate nearly DOUBLED, 18.6% →
38.1%.** We put builder bots on the enemy core's doorstep more often than at any
point in our history **and then never swing.**

## WHY THIS IS THE DOORSTEP FINDING FROM A FOURTH DIRECTION

Part 5's separator (we get pinned, never fund the battery, never fire) and this
(we arrive and never swing) are the same story from two sides. **This one is the
most actionable of the four routes because it is a REGRESSION, not a design gap:
the behaviour existed in v94 and does not in v104, so there is a diff to read.**

Candidate to check first — **stated as a hypothesis, not a finding, and it is the
builder's to test, not this lane's:** a builder bot's `fire()` requires an
orthogonally adjacent tile, and `reached` is defined on exactly that adjacency.
**Our `reached` went UP while attacks went to zero, which fits a guard that admits
arrival but blocks the swing.**

## WHAT THIS LANE GOT WRONG, MECHANICALLY

The `kind` column already classified EXILE / INSERT / RETREAT and was sitting in
the table's header. **Neither the agent nor this lane used it — one `head -1`
away.** That is D34 repeating: *an audit of the evidence instead of an audit of
the codebase.* The within-sample control was the right instinct aimed at the
wrong axis.
