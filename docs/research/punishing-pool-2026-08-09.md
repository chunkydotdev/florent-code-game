# Is the lethality leg runnable locally? Yes — and my own §4 was too broad

**Research arm, session 20, 2026-08-09 01:5x CEST.** Live **v80 "Eir 9b"**,
window n=6/20. **Zero downloads, read-only** (`results.tsv` tape + `bots/`
inventory; no arena, no verdicts). Answers the builder's blocking question:
*"the settling leg may not be runnable locally at all."*

---

## 1. Method, and a correction to my own first pass

The question is which local opponents have a **non-zero backfire rate** — i.e.
which can punish an over-push. Proxy: opponents we do **not** dominate.

My first aggregation pooled every tape row mentioning an opponent and took the
median win rate. **That was wrong.** It mixed:
- map-restricted legs (hive-only rows at 0/32),
- probe-**fidelity** rows (which measure the *probe's* faithfulness, not our win
  rate against it),
- full batteries.

It reported `kladde_probe` at 43%. The correct figure is 73%. I caught it before
relaying; recording the error because it is the same pooling failure this queue's
rule 6 exists for.

Corrected filter: n≥120, not map-restricted, not a probe-fidelity row.

## 2. The pool, by domination status

```
opponent           legs   median wr        range        status
opp_v39              14       80.7%   57.1-99.2%    DOMINATED
rush_probe            2       87.9%   80.8-95.0%    DOMINATED
flotte_probe          4       85.0%   76.7-86.7%    DOMINATED
rush_probe_fast      11       80.0%   60.4-96.7%    DOMINATED
kladde_probe          2       73.0%   72.1-73.8%    DOMINATED
--------------------------------------------------------------
opp_v63              10       64.4%   53.1-80.8%    CONTESTED
opp_v67               2       64.1%   51.9-76.3%    CONTESTED
opp_v69               4       61.7%   52.5-64.2%    CONTESTED
opp_v78               2       59.2%   56.4-62.0%    CONTESTED
opp_v49               3       58.8%   55.4-97.1%    CONTESTED
opp_v68               4       57.4%   46.0-70.0%    CONTESTED
opp_v50              14       55.0%   40.0-93.3%    CONTESTED
opp_v45              11       53.3%    0.0-70.0%    CONTESTED
ouroboros_probe       1       53.1%          n=128  CONTESTED
opp_v72               1       49.0%          n=120  CONTESTED
opp_v74               4       48.4%   44.2-60.0%    CONTESTED
orizon_probe          1       47.2%          n=120  CONTESTED
--------------------------------------------------------------
opp_v44               9       40.8%   22.1-61.3%    *** WE LOSE
opp_v76               4       38.3%   34.2-42.5%    *** WE LOSE
band_probe            1       26.7%          n=120  *** WE LOSE
```

**The leg is runnable.** The premise that the pool is uniformly dominated is not
supported: twelve opponents sit in 45–65% and three beat us outright.

## 3. The correction I owe on my own §4

I told the builder its ceiling battery "used kladde_probe and ouroboros_probe,
both of which we beat 87–93%", and it adopted that framing. **The 87–93% figure
is kladde only.** The builder's own message described the ouroboros_probe leg as
"harder — win rates NOT matched", and the tape puts us at ~53% against it
(n=128).

**So `ouroboros_probe` is contested, not dominated, and the strength-axis half of
the builder's battery is NOT invalidated by my mechanism.** Only the kladde half
is. My §4 was stated too broadly, the builder repeated it back, and it would have
retired a valid leg. The mechanism stands; its reach does not extend to
ouroboros_probe.

## 4. The limitation that does constrain the leg

**Every `opp_vNN` is our own archived lineage** — `opp_v76` is byte-identical to
our platform v76. So the entire *non-dominated* self-play pool is our own code.

Backfire measured against our own lineage may not generalise: our versions share
our failure modes, and a punish they execute is a punish we already know how to
build. The genuinely *external* replicas are the probes — and among those, only
`band_probe` (26.7%), `orizon_probe` (47.2%) and `ouroboros_probe` (~53%) are
non-dominated, each with **one leg** behind the estimate.

So the honest position is narrower than "runnable":

- **Runnable against a non-dominated pool: YES**, using
  `ouroboros_probe` + `band_probe` + `orizon_probe` (external, contested-to-losing)
  and `opp_v76` + `opp_v44` (self-play, we lose).
- **Runnable against a non-dominated pool of *external* opponents with
  well-established win rates: NOT YET.** The three external candidates rest on
  one leg each. Their domination status should be re-measured before the leg is
  scored on them, or the leg inherits a single-leg estimate as its premise.

## 5. Recommendation

Score the lethality dial on **overall win rate** against a pool split three ways,
and report the arms separately rather than pooled:

1. `ouroboros_probe`, `band_probe`, `orizon_probe` — external, non-dominated.
   **The load-bearing arm.**
2. `opp_v76`, `opp_v44` — self-play, we lose. Confirms the effect exists but
   cannot establish it generalises beyond our own code.
3. `kladde_probe` or `rush_probe` — dominated. **Included deliberately as a
   negative control**: my mechanism predicts this arm reports Regime A regardless
   of what arms 1 and 2 show. If it does not, the mechanism is wrong and that is
   worth knowing.

Arm 3 is the part I would not skip. It makes the leg a test of my own claim as
well as of the lethality question, at the cost of one extra arm.

## 6. Caveats

- Win rates are pooled across many of *our* versions and several years of tape;
  they are a domination *screen*, not a current measurement. A pool chosen on
  them should be spot-checked at current head before the leg is scored.
- Single-leg estimates (`band_probe`, `orizon_probe`, `ouroboros_probe`,
  `opp_v72`) are marked as such and should not be treated as established.
- `opp_v56`, `opp_v58`, `cad_probe`, `clanker_probe` have no qualifying rows —
  unmeasured, not absent.
