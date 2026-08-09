# PLANK SITE re-price: the prediction and the read, stated BEFORE the battery

**Research arm, session 24, 2026-08-09.** Queue item #4. **This document is written
before any re-price battery is run, so that the result is a TEST rather than a fresh
measurement.** Nothing in it may be edited after the battery fires; corrections go in
an appended block with a timestamp.

**Version tag:** live **v91** = `bots/_v100hf`, tree `4558be91`. The re-price is the
builder's to execute (I do not run arena). My lane's contribution is this
pre-registration, and one finding about the original battery that changes what the
re-price can be for.

---

## 1. What is being re-priced

`_v113site` gates the forward siege programme off above d²=81. Measured 2026-08-09
against `_v113off`, **300 games, self-play pool** (the pool is `bots/opp_v*`, which
we now know is **our own prior versions**):

```
OVERALL   control 96/150 (64.0%)   site 86/150 (57.3%)   -6.7pp
narrow <=81    24/40 -> 24/40   +0.0pp   (gate CANNOT fire here)
mid 128-144    28/40 -> 26/40   -5.0pp
wide 288-392   36/60 -> 28/60  -13.3pp
hive 650        8/10 ->  8/10   +0.0pp   (n=10)
```

The verdict was carried by **dose-response** — zero where the gate is inert, damage
scaling with how much of the forward programme it removes — plus the exact-zero null
band. That is the strongest attribution shape this harness offers, and I am not
disputing the shape.

## 2. **THE FINDING THAT CHANGES WHAT THE RE-PRICE CAN BE FOR**

**No band of that battery, including the headline, is distinguishable from zero at
its own n under the pooled estimator that `arena.py` reports.**

| band | delta | pooled SE | z | p (two-sided) |
| --- | ---: | ---: | ---: | ---: |
| OVERALL | −6.7pp | 5.77pp | −1.15 | **0.25** |
| seat B | −13.3pp | 8.16pp | −1.63 | 0.10 |
| narrow ≤81 | +0.0pp | 11.18pp | 0.00 | 1.00 |
| mid 128–144 | −5.0pp | 11.18pp | −0.45 | 0.66 |
| wide 288–392 | −13.3pp | 9.13pp | −1.46 | 0.14 |
| hive 650 | +0.0pp | 22.36pp | 0.00 | 1.00 |

**And the "exact zero" in the null band is not evidence of a tight null** — at 40 v
40 its 95% interval is roughly ±22pp. It is consistent with the gate being inert
there, which is what we believe on mechanism; it is not independent confirmation of
it.

**The one honest caveat, and it matters.** The repo uses two estimators. For a
**paired** leg the tape uses the discordant-pair form (`v1-2026-08-08-measurement-power.md`:
*"42 discordant, 20 toward / 22 against, difference −1.67pp, SE = √42/120 = 5.40pp"*).
If the SITE legs were paired and discordance ran at the ~35% rate of that one
documented leg, SE would be ≈ √105/300 = **3.4pp**, giving z ≈ −1.96 and p ≈ 0.05 —
**borderline, not noise.** Which estimator applies depends on a number that **was
never reported: the discordant-pair count for the SITE battery.**

> **ASK, and it is cheaper than any battery: report the discordant-pair count for
> the original SITE legs.** Without it, −6.7pp sits somewhere between "clearly
> indistinguishable from zero" (p 0.25) and "borderline" (p 0.05), and neither arm
> can say which. **`tools/paired_vs_pooled.py` already measured that pairing is
> cosmetic under NOISE_ON** (ratio 1.06×, because spawn_salt reseeds from live
> entropy), which pushes me toward the pooled reading — but that was measured on a
> different pair of bots and I am not going to assume it transfers.

**Consequence for the re-price, stated plainly: a re-price sized like the original
cannot resolve the question it is being run to answer.** Minimum detectable effect
at 80% power, two-sided, pooled:

| games per arm | MDE |
| ---: | ---: |
| 150 (the original) | 16.2pp |
| 300 | 11.4pp |
| 500 | 8.9pp |
| 1000 | 6.3pp |

The literature's prediction for a self-play → field re-price is that the effect
**halves** (Agade's published ~30% → ~15%). Detecting −3.35pp at 80% power needs
**≈3,500 games per arm.** That is not happening.

## 3. The pre-stated predictions

Ordered by how much I am willing to stake on them.

**P1 — SIGN SURVIVES (confidence: moderate, ~70%).** The re-priced overall delta is
**negative**. Basis: dose-response is a mechanism argument, not a magnitude argument,
and mechanism arguments transfer across pools better than magnitudes do. **Falsified
by** a positive point estimate whose interval excludes zero — which, per §2, this
battery is very unlikely to be able to produce, so treat P1 as **nearly untestable at
realistic n** and say so rather than counting a within-noise negative as a hit.

**P2 — MAGNITUDE SHRINKS (confidence: moderate, ~65%).** The re-priced |delta| is
**smaller than 6.7pp**. Basis: two published amputation re-prices in another game
(Agade's factor ≈2 on his own headline; Magus reporting an outright sign flip).
**I am NOT predicting a factor of 2** — HANDOVER is right that one figure from
another game is not a divisor, and I will not launder it into one by quoting a
range. **Falsified by** a re-priced |delta| ≥ 6.7pp.

**P3 — THE BAND ORDERING SURVIVES (confidence: high, ~85%). This is the prediction I
actually want tested, because it is the only one the harness can resolve.** In the
re-price, `narrow ≤81` is closer to zero than `wide 288–392`, and the ordering
narrow → mid → wide is monotone in the negative direction. Basis: the narrow band is
a **built-in null by construction** — the gate cannot fire there — so it is the one
comparison that does not depend on effect size, only on the gate doing what the code
says it does. **Falsified by** narrow showing a larger |delta| than wide, which would
mean the gate is doing something outside its stated scope and would invalidate the
original attribution as well as the re-price.

**P4 — THE FOREIGN POOL MOVES IT MORE THAN NOISE (confidence: low, ~40%).** The
foreign-pool delta differs from the self-play delta by more than their combined
intervals. **I expect this to fail**, and its failure is informative: it would say
the pool substitution is not measurable at this n, which is itself the answer to
"should we keep re-pricing things against probes".

## 4. The read, stated before the numbers

* **The primary read is P3, not P1 or P2.** A magnitude re-price at this n cannot
  produce a decision; a band-ordering check can produce a **falsification** of the
  original attribution, which is worth more.
* **`NOT-REFUTED (n=…)`, never `pass`** — the standing rule, and it binds harder here
  than usual given §2.
* **Both directions get recorded.** If the re-price comes back less negative, that
  does **not** license re-opening forward siting: the original verdict already
  survives on mechanism, and "smaller than we thought" is not "positive".
* **The probes are imitations and are miscalibrated** (`ouroboros_probe` measured
  86 pts over-confident against its real class). A foreign-pool number is **better
  than self-play and is not field.** Any sentence written about this result must
  carry the pool label — the s22 "LOKI-3 FIELD VERDICT" mislabelling is exactly the
  failure this rule exists to stop.
* **Excluding `cad_probe`** from paired runs — it is the only probe calling
  `random.`.

## 5. What I think this item is actually worth, said plainly

**The builder's own assessment is right: SITE re-priced can at best produce a firmer
"don't do that". It cannot produce a ship.** §2 sharpens that — it probably cannot
even produce a firm "don't do that", because the instrument is not powered for the
magnitude in question.

**The highest-value thing in this document is not the re-price. It is the discordant
pair count ask in §2**, which costs one number, applies retroactively to every
300-game battery on the scoreboard (LOKI-3 +0.0, HOME −2.0, FLOOR −0.7, SITE −6.7,
ESCALATE −7.8), and would tell us whether "four knobs, all nulls" means *the
subsystem is inert* or *the instrument could not see it*. **Those are very different
conclusions and the scoreboard currently does not distinguish them.**

I am not asserting the second. I am saying the board cannot presently rule it out,
and that one count would.

---

**Pre-registration closed at the timestamp of this commit. No band, threshold, or
prediction above may be revised in place.**
