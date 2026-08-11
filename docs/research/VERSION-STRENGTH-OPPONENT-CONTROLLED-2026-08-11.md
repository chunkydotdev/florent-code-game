# ⭐ VERSION STRENGTH WITH OPPONENT CONTROLS — THE LADDER SIDE OF PART A

**Research arm, s31, 2026-08-11.** Commissioned by the builder to replace Part A's
ladder side — a **rating snapshot** — with a **version effect estimated from
per-match data**, so the six local↔ladder residuals mean something.

## THE ESTIMATOR

For each game, `P(we win) = 1 / (1 + 10^((R_opp − θ_v)/400))`, where `R_opp` is the
**opponent's rating at match time** (`ladder_games.oppbef`, **0 missing of 3,740**)
and `θ_v` is a free strength parameter per version, fitted by maximum likelihood
with a shared seat term. **The functional form is the ladder's own** — verified
today to a max residual of 0.000000 on `delta = 32 × (S − E)` — so it is not an
assumption imported from outside.

**Why this removes most of the era confound:** the ladder continuously re-rates
every team, so *opponent rating at match time* is an era-calibrated yardstick. A
version measured against 1,700-rated opponents in a strengthening field is scored
against what those opponents were worth **then**.

**Uncertainty: bootstrap over MATCHES (193), not games** — five games share an
opponent and a pairing, so game-level resampling would understate the CIs.
Population: `ladder_games.tsv` (**never `meta_join`**, which pools rated with our
own unrated panel legs).

## RESULT

| version | games | **fitted θ** | 95% CI (match-bootstrap) | rating snapshot | **correction** |
|---|---:|---:|---|---:|---:|
| v92 | 80 | **1600** | [1520, 1681] | 1552 | **+48** |
| v102 | 390 | **1609** | [1578, 1641] | 1600 | **+9** |
| v104 | 495 | **1686** | [1656, 1717] | 1668 | **+18** |
| **v112** | **0** | **— NOT ESTIMABLE —** | | 1674 (k=4) | |

**Seat term: −2.8 Elo, 95% CI [−46, +37] — not resolved**, consistent with the
ladder being seat-symmetric overall (third-party seat-A share 50.137% ± 0.233pp).

## ⇒ WHAT PART A CAN AND CANNOT SCORE

| pairing | ladder-side ordering | usable? |
|---|---|---|
| v104 − v92 | **−86, CI [−169, −5]** | ✅ **SIGN RESOLVED** |
| v104 − v102 | **−77, CI [−125, −29]** | ✅ **SIGN RESOLVED** |
| v92 − v102 | −9, CI [−104, +71] | ⛔ **sign NOT resolved** |
| v112 − anything (×3) | no ladder estimate exists | ⛔ **unmeasurable** |

**⇒ OF PART A'S SIX PAIRINGS, ONLY TWO HAVE A RESOLVED LADDER-SIDE ORDERING TO
PREDICT.** The other four cannot be scored from the archive at any local n — a
65,000-game local run does not fix a missing ladder side.

**⛔ AND THE CORRECTION CHANGES AN ORDERING, WHICH IS THE POINT OF THE EXERCISE.**
On raw snapshots: **v92 1552 < v102 1600**. Opponent-controlled: **v92 1600 ≈
v102 1609**, indistinguishable. **A residual scored against the snapshots would
have counted a real local v102>v92 result as a HIT when the ladder does not
actually order them.**

**v112 is the one the builder most wants and it is the one with nothing.** Zero
archived games; its 1674 is **four rated matches taken at the bottom of a v104
drawdown**. ⇒ **Treat v112's ladder side as UNMEASURED, not as 1674.**

## CAVEATS

* **v92 is 80 games** — its CI spans 161 Elo and it carries the widest correction.
* All three corrections run **upward** (+48, +9, +18), i.e. snapshots understate
  every version measured. *(INFERENCE: consistent with ratings lagging a rising
  true strength, not established.)*
* The ladder pairs on rating, so opponents are not random — **conditioning on
  opponent rating is what handles that**, and it is the model's whole job.
* `oppver` is NULL over large stretches and **is not used here**; opponent strength
  enters only through `oppbef`, which is complete.
