# SPEC — the slot rule fires on a NEUTRAL holder three-quarters of the time by k=27, and that base rate is written down nowhere

> ## ✅ IMPLEMENTED s33, 2026-08-12 04:5xZ — `e74aab9`. DO NOT REBUILD.
> Built by the side lane on Magnus's direct instruction (*"Fix your findings
> please"*), which widened this lane's write surface for it.
> **`tools/slot_denoms.py`** (pure functions, 25 selftest cells) +
> **`tools/monitors/ship_watch.py`** (7 new cells). Live line now reads:
> `… RULE=held … p_null=0.75 dd_z=-0.83 dd_k=28 resolvable_k=147 sd_pm=8.66
> net_act_src=derived lg_age_min=39.6`.
> **The rule is untouched** — no threshold moved, no arming point changed,
> `slot_rule.py` not edited. `ladder_games.tsv` feeds the diagnostics only and
> never the alarm; **an unreadable ladder degrades the columns to `NA` and the
> rule STILL frees the slot** (driven in the selftest).
> Calibration against the 40k bootstrap in §1: k=8 **14.1/14.1**, k=27
> **73.7/74.6**, k=60 **97.0/97.0**, at **0.03 s per poll**.

**Side lane, s33, 2026-08-12 ~04:4xZ. Owner: builder.**
**Companion to `SPEC-drawdown-resolvability-and-the-net_act-origin-2026-08-12.md`
— same family (a threshold printed without its denominator), different column.
That spec stands unchanged; this one does not modify it.**

**⛔ THIS IS NOT A PROPOSAL TO CHANGE THE RULE.** The threshold, the arming point
and the "frees, never forces" semantics all stay exactly as they are. **The
change is one printed column**, so the verdict cannot be read as more than it is.

---

## 1. THE MEASUREMENT

`tools/slot_rule.py:97,131` — `slot_free = armed and net5 <= -21`, `ARM_AFTER`
gives `armed` at **k ≥ 8**, and `net5` is a **rolling five-match** net recomputed
every match. So from match 8 onward **every new match is a fresh chance to trip.**

Measured on `corpus/ladder_games.tsv` (795 matches collapsed by `match` id,
newest row `2026-08-12T03:52:59.613Z`), per-match interval **mean +0.188,
sd 8.664**, then **centred to model a TRUE-ZERO holder**:

```
ANALYTIC   P(net5 <= -21 | true zero), one window   = Phi(-1.0840) = 13.9%
EMPIRICAL  sliding-5 over the real centred tape     = 113/791     = 14.3%
```

**Two methods, independently computed, agreeing to 0.4pp** — the empirical one
carries whatever fat tails the real distribution has, so the agreement is
evidence the normal approximation is safe here rather than assumed.

**Bootstrap** (40,000 trials, resampling the centred intervals, arming at k≥8) —
**P(a genuinely zero-effect holder frees the slot at least once within k matches):**

| k | 8 | 10 | 12 | 20 | **27** | 40 | 60 |
|---|---|---|---|---|---|---|---|
| P(fires \| true zero) | **14.1%** | 24.7% | 33.9% | 60.4% | **74.6%** | 88.7% | **97.0%** |

---

## 2. WHAT THIS MEANS, AND THE ASYMMETRY IS THE USEFUL PART

**`SLOT FREE` is close to uninformative on its own at the k values we act at, and
`RULE=held` is the informative half.** By k=27 a neutral holder has already
tripped the rule in **three runs out of four**; by k=60 in **97**. So:

* **"the slot was freed" barely narrows anything** — it is the majority outcome
  for a bot with no effect at all;
* **"the slot was NEVER freed" is a real signal**, because only ~25% of neutral
  holders get to k=27 without tripping.

**Nobody has been reading it in that direction**, and the column that would let
them does not exist.

**⭐ THE REPO ALREADY HAS THE RIGHT DOCTRINE AND IS MISSING ONLY THE NUMBER.**
`slot_rule.py:29` is explicit — *"It does not decide. `slot_free` is a
[signal]"* — and the standing slot-swap rule is recorded as **"stop-loss + wake,
never an n=8 evaluation."** **That framing is correct and this spec supports it
rather than correcting it.** What is missing is that **the wake's base rate has
never been quantified**, so nothing stops a successor reading a fired rule as
evidence. `HANDOVER.md` calls k=8 *"the decision point"*, and at k=8 the rule
fires on **14.1%** of bots that do nothing at all.

**⚠ AND IT BEARS ON THE LIVE HOLDER, which is exactly why it needs a column and
not a paragraph.** v114 is at **k=27 with the rule never having fired**. Under a
true-zero holder that outcome has probability **25.4%**. **The reading of that is
the builder's, not mine** — this lane writes no verdicts — but it should be made
**with the base rate visible**, because the same fact reads as "nothing has
happened" without it and as "the quiet half" with it.

---

## 3. THE CHANGE — ONE COLUMN

Add to the `ship_watch` line, beside `RULE=`:

* **`p_null=<P(a zero-effect holder would have fired by THIS k)>`**

so `RULE=SLOT FREE ... p_null=0.75` is self-limiting on the line where it is
read, and `RULE=held ... p_null=0.75` says what the silence is worth.

**Sourcing, same discipline as the companion spec:** the centred per-match sd
comes **off the tape at runtime** (8.664 today), never from a constant. Compute
`p_null` from the bootstrap at import time or ship a small lookup keyed on k with
the sd it was built at, **and print that sd** so a successor can see when it has
drifted.

---

## 4. SELFTEST — BOTH DIRECTIONS, AND THE SECOND CELL IS THE LOAD-BEARING ONE

| cell | fixture | must |
|---|---|---|
| **fires late** | zero-mean tape, k=27, rule fired | print `p_null ≈ 0.75` |
| **fires early** | zero-mean tape, k=8, rule fired | print `p_null ≈ 0.14` — **materially different from the k=27 cell**, or the column is a constant and validates anything |
| **never fires** | zero-mean tape, k=27, no fire | still print `p_null`, because the silence is the informative half |
| **sd drift** | tape with sd doubled | `p_null` must MOVE — a `p_null` that ignores its own sd is the docstring-constant defect one level up |

---

## 5. LIMITS — stated, not buried

* **⭐ AMENDED SAME DAY — THIS LIMIT WAS TOO HARSH AND THE RESEARCH ARM MEASURED
  IT RATHER THAN ARGUING IT.** I originally wrote that the i.i.d. bootstrap made
  `p_null` *"an order-of-magnitude base rate, not a p-value"*, because real
  ladder deltas should carry serial structure through the rating gap. **Tested,
  on the same centred deltas:**
  ```
  lag-1 r +0.052 · lag-2 +0.022 · lag-3 +0.012 · lag-4 +0.048 · lag-5 +0.075
  Ljung-Box Q(5) = 8.99   vs chi2_5 95% crit 11.07   -> NO DETECTABLE STRUCTURE
  moving-block bootstrap (block=10) vs i.i.d.:
     k=8   14.2% / 14.1%      k=27  74.8% / 72.6%      k=60  97.1% / 96.4%
  ```
  **The i.i.d. assumption is supported, and where it fails the gap is ≤2.2pp and
  runs CONSERVATIVE for the argument** — under blocks, v114's *"held at k=27"*
  sits at **27.4%** rather than 25.2%, i.e. marginally *less* surprising.
  ⇒ **`p_null` is robust to serial structure within ~2pp**, not
  order-of-magnitude only. *(Reproduction and both tests: research arm, s33,
  independently resampled — their per-window count 113/791 is identical to the
  row and every bootstrap cell sits inside Monte Carlo noise of mine.)*
* **Two limits that survive it, because the tests above do not address them:**
  **absence of DETECTABLE autocorrelation at n=795 is not proof of
  independence** — lag-5 at +0.075 is the largest and is the one to re-check as
  n grows — and **the sample is us-only, which no resampling fixes.**
  **It is still not a p-value: it is a base rate with a measured robustness
  bound.**
* **Us-only sample.** Every figure describes OUR ladder run (795 matches), not
  the field's.
* **This does not touch the SPRT bounds**, which are correctly sized for the
  rates they name (fast k≥3 at −10/match, slow k≥17 at −4/match — computed in the
  companion spec).
* **It changes no threshold and frees no slot.** If the builder decides the rule
  should be tightened, that is a separate decision on separate evidence and this
  spec takes no position on it.
