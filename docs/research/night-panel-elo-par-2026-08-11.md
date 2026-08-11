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
