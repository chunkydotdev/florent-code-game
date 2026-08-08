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

---

# ADDENDUM (02:1x) — **RETRACTION. The builder's refusal was right, and my §2 table was built wrong.**

The builder refused my correction to its ceiling battery and I checked the
primary expecting to confirm my figure. **The primary refutes me, and the defect
is worse than the single number.**

## The single number first

My "ouroboros_probe ~53% (n=128)" came from the **PIECE D guard-matrix row**,
whose `winrate` column (0.531) is the row's *overall* rate across a battery of
band/flotte/kladde legs. `ouroboros_probe` merely appears somewhere in its text.
**I attributed a pooled row's headline number to an opponent named inside it.**

The tape states the real figure explicitly, in the SHIP BATTERY row:

```
kladde 75.0 [69.2,80.1] · flotte 86.7 · band 90.0 · ouroboros_probe 72.5 [66.5,77.8]
· opp_v56 61.7 · opp_v63 57.9 /480
```

**ouroboros_probe is 72.5% — dominated.** The builder's fresh battery puts it at
79.2–93.3% at current head. Its original framing was right in the strongest form
and my "rescue" of its strength-axis leg was unfounded. **"Structurally
incapable" stays.**

## The defect is systemic, not local

My §2 table was built by substring-matching an opponent name against a row and
taking the **row-level** `winrate`. Every pooled row therefore contributed its
headline number to whichever opponent matched first. Re-parsed to use the
per-opponent figures stated *inside* descriptions:

```
opponent          obs   median          range        status      I HAD SAID
band_probe         45    88.3%    5.0-100.0%    DOMINATED     26.7% WE LOSE
flotte_probe        9    86.7%   75.0-93.3%     DOMINATED     85.0% dominated
ouroboros_probe     4    77.1%   72.5-79.2%     DOMINATED     53.1% CONTESTED
kladde_probe       43    72.1%    0.0-87.5%     DOMINATED     73.0% dominated
rush_probe_fast     5    68.3%   60.4-97.5%     DOMINATED     80.0% dominated
orizon_probe       15    66.7%    4.8-94.6%     DOMINATED     47.2% CONTESTED
opp_v63            11    60.0%   30.0-100.0%    CONTESTED
opp_v50             7    58.8%   53.3-64.2%     CONTESTED
opp_v74             4    56.2%   48.4-60.0%     CONTESTED
opp_v45             5    50.0%    3.3-78.3%     CONTESTED
opp_v69             3    41.7%   40.0-43.3%     WE LOSE
opp_v44             3    40.8%   40.6-40.8%     WE LOSE
opp_v76             3    38.3%   38.3-42.5%     WE LOSE
```

**Three of my status calls invert: `band_probe`, `orizon_probe` and
`ouroboros_probe` are all DOMINATED, not contested-or-losing.**

## What this does to the recommendation

**ARM 1 OF MY THREE-ARM DESIGN DOES NOT EXIST.** Every external replica —
band, flotte, kladde, orizon, ouroboros, rush — is dominated. There is no
external opponent in the local pool that can punish us.

**So the builder's original concern was correct and my headline was wrong.** The
corrected position:

- **Runnable against external non-dominated opponents: NO. None exist locally.**
- **Runnable against our own lineage: yes** — `opp_v76` 38.3%, `opp_v44` 40.8%,
  `opp_v69` 41.7%, plus contested `opp_v63`/`opp_v50`/`opp_v74`/`opp_v45`. With
  the §3 caveat intact and now load-bearing rather than secondary: these share
  our code, so a punish they execute is one we already know how to build.
- **Against real opponents: only `fcode match unrated`**, at ~30 games/hour,
  which the builder had already identified as unable to buy a verdict.

**Arm 3 (the dominated negative control) survives and is now nearly the whole
external pool** — which is itself the finding: if every external probe reports
Regime A, that is consistent with my mechanism *and* with the mechanism being
vacuous, and the two cannot be separated without a punisher.

## What survives

§2's *narrow* claim — that the pool is not "~3 effective opponents" — survives:
there are ~7 usable self-play opponents spanning 38–60%. **The claim that any of
them are external does not.**

## Process note against myself

This is the **third** attribution error in one analysis chain: kladde at 43%
(pooled map-restricted legs), ouroboros at 53% (row-level attribution), and now
the whole table. Each was the same failure — **taking a number from a row that
answers a different question than the one I was asking.** Queue rule 6 says a
null needs the treatment in the pool; the sibling rule this establishes is:
**a per-opponent claim requires a per-opponent figure, never a row-level one.**
I caught the first myself, missed the second, and only found the third because
the builder refused a correction that flattered its own work.
