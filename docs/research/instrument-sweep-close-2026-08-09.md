# Instrument sweep, closing report: `sprt.py` and `paired_vs_pooled.py`

**Research arm, session 20, 2026-08-09 02:5x CEST.** Live **v80**, window n=6/20.
**Zero downloads, read-only** — no arena run, no bot touched. Closes queue item 2.

---

## `sprt.py` — the decision rule is SOUND. The numbers printed beside it are not.

### Verified good: the accept/reject rule honours its nominal error rates

Simulated 6,000 runs per condition against the tool's own defaults
(p0=0.45, p1=0.55, alpha=beta=0.05, budget 480):

```
true p = 0.45 (H0 boundary)   P(accept H1) =  5.2%   <- nominal alpha 5%   OK
true p = 0.40 (clearly H0)    P(accept H1) =  0.2%                        OK
true p = 0.55 (H1 boundary)   P(accept H0) =  5.0%   <- nominal beta  5%   OK
true p = 0.60 (clearly H1)    P(accept H0) =  0.4%                        OK
```

**The gate does what it claims.** Despite the docstring's own worry about the
independence assumption, the Wald boundaries deliver their advertised error
rates on this design. No change needed to how a KEEP/REFUTE decision from
`sprt.py` is trusted.

### The defect: the reported win rate and Wilson CI are biased BY THE STOP

`report()` prints, with no caveat attached:

```
{bot} (reference) win rate: {wins}/{n} = {rate}   Wilson 95% CI [lo, hi]
```

Both are conditioned on the stopping decision, and **anyone reading an
`sprt.py` output is by definition reading one that stopped.**

```
TRUE 50%   H1 stops (44.9% of runs)  report 56.6%   bias +6.6pp   Wilson covers truth 89.2%
           H0 stops (46.4%)          report 43.4%   bias -6.6pp   Wilson covers truth 89.5%
TRUE 55%   H1 stops (94.4%)          report 58.4%   bias +3.4pp   Wilson covers truth 96.7%
           pooled over all runs                     bias +2.5pp   Wilson covers truth 91.8%
TRUE 60%   H1 stops (99.9%)          report 63.1%   bias +3.1pp   Wilson covers truth 95.6%
```

**An H1 stop overstates the effect by roughly 3 percentage points**, more when
the true edge is small, and the Wilson interval delivers ~90% coverage rather
than 95%. Same family as the `ceiling.py` collider: conditioning on an outcome
(here, "the boundary was crossed") and then reading a statistic computed over
the conditioned sample.

**Partially mitigated already, and worth crediting:** the H1 verdict string
says *"Confirm with a fixed-480 arena run before shipping."* That is exactly
the right remedy and it is in the tool. What is missing is any indication that
the printed rate and CI are themselves biased — so a reader who quotes them
without re-running inherits the inflation silently.

**Recommendation (builder's call, tool is theirs):** label that one line as
biased-at-a-stop with the magnitude, or suppress the CI at a boundary stop.
Nothing else in the tool needs to change.

### A third number worth having: the budget interaction

```
true p = 55%,  budget 120  ->  H1 53.0%,  UNDECIDED 44.3%
               budget 240  ->  H1 83.7%,  UNDECIDED 12.0%
               budget 480  ->  H1 94.0%,  UNDECIDED  1.1%
```

**At a 120-match budget, a genuinely +5pp bot returns UNDECIDED 44% of the
time.** This is the sequential-test face of the `leg-power-19pct` row and it
argues the same thing from a different direction: 120 is not a budget that can
resolve the plank sizes this project actually builds.

## `paired_vs_pooled.py` — clean, and already carries its own refutation

No conditioning defect. It is a read-only diagnostic that measured the
pooled-vs-paired CI hypothesis, found **1.06x — worthless**, and has the
negative result plus its cause (NOISE_ON reseeds `spawn_salt`, so a shared
(map, seed) is not a shared opening) written into its own docstring. Nothing
to add.

---

## Sweep closing status — queue item 2

```
ceiling.py            CLEAN after the 2026-08-08 fix. conversion is conditioned
                      but attenuating, not inverting; kill_rate is the verdict metric.
pair.py               CLEAN. The r1000-conditioned line is unbiased as a rate.
sprt.py               DECISION RULE SOUND. Printed win rate + Wilson CI biased
                      ~+3pp at an H1 stop; undocumented.
paired_vs_pooled.py   CLEAN.
band instrument       BROKEN (look-ahead bias on a live rating join) -> fixed by
                      the builder's named-cohort amendment.
my own pool table     BROKEN (row-level attribution) -> retracted.
my own grind argument UNSUPPORTED (needs an unmeasured backfire rate) -> caveated.
```

**Four instruments swept, three clean, one defect found and it is cosmetic
relative to the gate it sits on.** The two genuinely broken things this sweep
found were both mine or the band split — not the arena toolchain, which came
through better than the night's error rate would have predicted.

## Caveats

- All figures in this document are simulations of the tool's algorithm, not
  runs of the tool. They test the arithmetic as written in `sprt.py:120-139`,
  reproduced independently; they do not test the harness around it (ticket
  pairing, discards on incomplete pairs, error handling).
- The pair-discard logic at a stop (`discarded: N in-flight match(es)`) could in
  principle bias results if discards were outcome-correlated. **I did not test
  this** — it needs the harness, not the arithmetic. Flagged, not cleared.
