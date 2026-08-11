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

> ## ⛔⛔ SIGN ERROR — CORRECTED IN PLACE 2026-08-11T18:1xZ (s32, research arm). THE TWO SCOREABLE CELLS WERE PUBLISHED WITH INVERTED SIGNS.
> **Flagged by the SIDE LANE; the discriminating check was mine and I ran it.** The table
> as first published read `v104 − v92 = −86` and `v104 − v102 = −77`, which **contradicts
> this document's own fitted θ three lines above** (1686 − 1600 = **+86**; 1686 − 1609 =
> **+77**). Two of three flipped and `v92 − v102 = −9` was correct — so it is not a stated
> convention (a convention flips all three); it matches computing `v92 − v104` under the
> label `v104 − v92`.
> **WHICH SIDE WAS THE TYPO — SETTLED AGAINST THE PRIMARY SOURCE, NOT INTERNALLY.**
> Re-derived from `corpus/ladder_games.tsv` with a **deliberately different estimator**
> (single-parameter logistic inversion on mean opponent rating at match time — no MLE, no
> seat term, no bootstrap): **v104 − v92 = +82.9 · v104 − v102 = +73.2 · v92 − v102 =
> −9.7.** All three agree with the FITTED θ to within ~4 Elo.
> **⇒ THE POINT ESTIMATES ARE CORRECT AND THE DELTA ROW WAS THE TYPO.**
> **WHY IT MATTERED, AND IT IS NOT COSMETIC:** these are **the only two of Part A's six
> pairings with a ladder side at all**, and the overnight run's Amendment 1 bar —
> pre-committed before any game ran — fires on inversion: *"local ranks the ladder-WORST
> bot as locally BEST ⇒ LOCAL SCREENS DO NOT PREDICT THE LADDER. Stop screening for the
> rest of the week; ship on mechanism alone."* Against the live CAL shards (both COMPLETE
> at 2000/2000 — `CAL_v104v92` 68.90% ⇒ implied +138.2, `CAL_v104v102` 55.50% ⇒ implied
> +38.4) the corrected signs read **AGREE on both cells**; the published signs would have
> read **INVERTED on both** and **stopped a week of screening on a maximal falsification
> that did not happen.**
> `tools/overnight_read.py:49` carries the correct numbers independently
> (`LADDER = {"_v130loki13": 1686, "_v115dodge": 1600, "_v124loki8": 1609}`), so the TOOL
> was never affected — **the exposure was a human write-up quoting this table, seeing the
> tool disagree, and reconciling the wrong way.**
> **A THIRD SURFACE, from the side lane, and it was inside this document all along:** the
> **rating-snapshot column two cells to the left** gives v104−v92 = 1668−1552 = **+116**
> and v104−v102 = 1668−1600 = **+68**. **Three independent surfaces — snapshots, the MLE
> fit, and my re-derivation — agree on the sign of all three pairings, and the published
> −86/−77 contradicts all three.** The cheapest check was two columns away from the error.
> **⚠ ON THE FORM OF THIS CORRECTION (side lane's objection, and it is a fair one).** This
> document is cited by `docs/PLAN-overnight-2026-08-11.md` §2b and **predates the games**,
> so an in-place edit risks a two-clock cert certifying numbers that moved after the run.
> **Kept in place deliberately, on the ground that a cert is broken by a SILENT change and
> not by an announced one** — the original stands in git (`2c261c8`), this block is dated
> and states exactly what moved, and **no point estimate changed: only a sign the fitted
> table already contradicted.** The standalone chain-of-custody artefact is the side
> lane's **`FLAG-partA-ladder-sign-2026-08-11.md`**; deliberately NOT duplicated into a
> second document, because `audit_trigger` reads **13.57** on cross-lane analysis today
> and both lanes agreed not to add to that numerator without a decision attached.

| pairing | ladder-side ordering | usable? |
|---|---|---|
| v104 − v92 | **+86, CI [+5, +169]** ⭐ *sign corrected s32* | ✅ **SIGN RESOLVED** |
| v104 − v102 | **+77, CI [+29, +125]** ⭐ *sign corrected s32* | ✅ **SIGN RESOLVED** |
| v92 − v102 | −9, CI [−104, +71] | ⛔ **sign NOT resolved** |
| v112 − anything (×3) | ⭐ **NO LONGER TRUE — see the v112 block below** | ⚠ **estimable, not resolved** |

**⇒ OF PART A'S SIX PAIRINGS, ONLY TWO HAVE A RESOLVED LADDER-SIDE ORDERING TO
PREDICT.** The other four cannot be scored from the archive at any local n — a
65,000-game local run does not fix a missing ladder side.

## ⭐ ADDED s32, 2026-08-11T18:1xZ — **v112's "0 GAMES / NOT ESTIMABLE" WENT STALE WHILE THIS DOCUMENT SAT**

**The table above says `v112 | 0 | — NOT ESTIMABLE —`. That was true when written and
is false now.** A corpus sync at **17:59Z decoded 1,197 new replays**, and v112 now
carries ladder games. Computed by me from `corpus/ladder_games.tsv`, match-level
bootstrap (4,000 resamples over MATCHES, not games), same crude estimator validated
against the MLE above to ~4 Elo:

| version | games | matches | win rate | mean opp | **implied θ** | 95% CI | window |
|---|---:|---:|---:|---:|---:|---|---|
| **v112** | 70 | **14** | 57.1% | 1673.1 | **1723.0** | **[1616, 1832]** | 13:32Z–17:52Z |
| v104 | 510 | 102 | 52.4% | 1666.1 | 1682.4 | [1652, 1714] | 08-10 07:22Z–08-11 13:12Z |

**⚠ READ THE CI, NOT THE POINT ESTIMATE. v112 [1616, 1832] and v104 [1652, 1714]
OVERLAP heavily ⇒ v112 − v104 is NOT SIGN-RESOLVED, so this does NOT add a scoreable
Part A cell and the "only two pairings" conclusion above STANDS.** What changed is
narrower and still worth recording: **v112 has a ladder-side estimate at all for the
first time**, it is directionally the strongest version we have fielded, and **14
matches is the denominator** — the interval is ±~108 Elo because five games share a
pairing, which is exactly why the bootstrap is over matches.
**⛔ DO NOT QUOTE 1723 WITHOUT THE INTERVAL.** On 14 matches that number will move.

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
