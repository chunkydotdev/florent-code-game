# v1 — Can cheaper models build incrementally better bots?

**Date:** 2026-08-08 · **Author:** third session (main dir, not an arm)
**Versions in scope:** live v83 `_v97e11` (md5 56b9d178) vs v82 `_v97hv` (md5 e4aad212)
**Surfaces touched:** none. Read-only diagnostic, scratch-first.
**Relayed:** both live florent sessions, 2026-08-08 ~20:5x (arm identity unresolved —
neither live session matched coordination.md's builder ref `af1aa9a9`).

---

## Answer

**Not yet, and the blocker is not the models.** The standard head-to-head leg
has **19% power** against a genuinely good plank. Four out of five real
improvements are structurally required to read "no verdict." Adding cheaper
models to that loop adds candidates to the part of the system that is already
saturated.

The fix is not a better model or a better statistic. It is **more matches**,
and matches are nearly free: local eval capacity exceeds the decision rate by
roughly 50-100x.

---

## 1. The fix I expected, refuted by my own run

**Pre-stated hypothesis.** `tools/arena.py:148` computes `wilson(wins, n)`,
treating every match as an i.i.d. Bernoulli trial, while `arena.py:114-117`
deliberately plays matches in (map, seed) blocks. `tools/sprt.py` inherits the
same assumption and its docstring flags it. Stockfish's fishtest scores game
*pairs* rather than games and documents ~15% lower variance from it; this
game's map structure looked far stronger than chess opening-book bias, so I
predicted **3-5x tighter CI on the same matches**. Refutation threshold stated
in advance: **under 1.5x kills it.**

**Measured** — `_v97hv` vs `_v97e11`, 15 maps × 6 seeds × 2 seat orderings,
180 matches, 6 of 16 cores:

```
POOLED (what arena.py's accept rule uses)
  93/180 = 51.7%   Wilson95 [44.4%, 58.9%]   half-width 7.22pp

PAIRED / blocked on (map, seed)
  90 blocks        95%     [44.8%, 58.5%]    half-width 6.83pp
  block outcomes {lose both: 18, split: 51, win both: 21}

  CI half-width ratio pooled/paired = 1.06x
  between-map sd of block means = 0.114
```

**1.06x. Do not build it.**

Two independent reads confirm the blocks carry almost no shared structure:

- The block distribution is near what *independence* predicts. At p=0.517,
  expected 21 / 45 / 24 vs observed 18 / 51 / 21 — a slight excess of splits,
  which is the entire 6%.
- Between-map sd of block means is **0.114**, *below* the **0.135** that pure
  sampling noise generates at 6 blocks/map. There is **no detectable map
  effect at all** for this pair of bots. (Stated narrowly: for *this* pair.
  Map effects are bot-dependent and `program.md` records strong per-map seat
  effects for other comparisons.)

**Mechanism, and it is already documented in our own notes.**
`docs/tooling.md:256`: `NOISE_ON=True` seeds `spawn_salt` from live entropy, so
two matches sharing a (map, seed) do **not** share an opening — the game
diverges immediately. **The pairing is cosmetic under NOISE_ON.** `sprt.py`'s
independence worry is misplaced in the regime it actually runs in.

---

## 2. The number that matters

Variance here is irreducible per-game noise. No estimator recovers it; only
`n` moves it.

Wilson lower bound clears 50% when `p_obs > 0.5 + 1.96·SE`. With a true +5pp
effect, power = `P(Z > 1.96 − 0.05/SE)`:

| leg size | power at **+5pp** | wall clock (6 cores) |
|---|---|---|
| **n=120** ← current standard head-to-head | **19%** | 3.4 min |
| n=384 | 50% | 11 min |
| n=800 | 80% | 22 min |
| n=2,200 | 80% at **+3pp** | 62 min |

**Throughput is measured, not estimated:** 180 heavy-bot matches in **302s** on
**6 of 16 cores**, with both other florent sessions running. ≈2,150 matches/hr
throttled; ~4-5k on the full machine; ~17k overnight on 6 cores.

We make ~10-20 gated decisions/day at 120-480 matches each. **Local eval
capacity exceeds decision rate by 50-100x.**

---

## 3. What this re-reads on the existing tape

- **The 15h / 57-Elo deadlock.** An underpowered instrument produces
  ambiguity → ambiguity produces analysis → analysis produces documents. That
  is exactly the measured `doc:code churn 0.14 → 1.88` and eleven hours of zero
  bot lines. Last 25 `results.tsv` rows: **14 notes/caveats, 6 verdicts, 5
  baselines.** The loop's output became commentary on its own measurements.
- **Why v83 shipped as a 7-plank bundle** at `55.0 [46.1, 63.6]`. Bundling is
  what you do when the instrument cannot resolve one plank — and it destroys
  attribution, so the next generation's hypotheses are built on unattributed
  results. Single planks *are* resolvable; it costs ~22 minutes each.
- **The loosened gate treats the symptom.** "Parity passes" at ±8pp admits
  changes that are genuinely 8pp worse. This is **not** an argument to
  re-tighten it — shipping beat paralysis and `ship-gate.md` was the right call
  at 19:40. It is an argument that the cheaper fix was 22 minutes of idle CPU,
  and still is.

---

## 4. Recommended, in order

1. **Raise the standard leg 120 → ~800.** Nothing else on this list matters
   until this lands.
2. **Re-run at power the rows decided at n=120** — `e1-bundle-h2h`,
   `_v96ft2-h2h`, `ft2-vs-bundle-direct`. At 19% power, "no separation" was
   never evidence of no separation. There may be shipped-but-unattributed
   planks already on the tape. **Cheapest high-value action available.**
3. **Promote `det.py` from attribution-only to the screening gate — keyed on
   DISTINCT SHAPES, not pair count.** ([Amended](#amendments) on the research
   arm's correction, 2026-08-08 ~21:1x.) NOISE_OFF paired runs have no
   *within-configuration* sampling variance, so the inferential unit becomes
   the configuration and **effective n = the number of distinct game shapes,
   not the number of matches run.** Two counterexamples the same night: a
   4-seed leg that was one distinct game replicated four times, and an identity
   control with 44 distinct shapes out of 120 matches. A gate keyed on pair
   count inherits a *worse* version of the defect this entry diagnoses — it
   reports n=120 while holding n=44. `det.py` now prints the distinct-shape
   count; the gate must read it, and the power table in §2 must be computed on
   that number. The butterfly caveat remains correct about attributing
   *mechanism* from individual flips, and remains wrong as a reason to refuse
   the *aggregate* paired rate as a decision statistic. Screen deterministic
   (on distinct shapes) → confirm stochastic at n≈800.
4. **Replace serial screen→confirm with racing.** F-Race / irace is the
   standard method for tuning against a noisy stochastic objective on a fixed
   budget. Its **elitist racing** structurally guarantees the returned best is
   the one evaluated most — replacing the manual every-10-accepts winner's-curse
   retest in `program.md`.
5. **`tools/tune_params.json` → CMA-ES or irace.** Three params declared, never
   swept. Zero tokens, no model in the loop. Cheaper than a cheap model is no
   model.
6. **Only then, cheap-model mutation operators at volume** — Haiku/Sonnet for
   small single-mechanism edits, top tier reserved for structural leaps,
   deletions, and hypothesis generation from replays. Note the inversion: the
   expensive model's worst use is adjudicating noisy measurements, which is
   where it currently sits.
7. **Pay the overfitting bill before step 4, not after.** Race on 10 maps, gate
   ships on 5 the candidates never saw. Rotate seeds per generation.

---

## 5. Grounding, with the precondition stated

Every "cheap model + more samples" result shares one precondition that is
usually dropped in the retelling: **a cheap, trustworthy, high-throughput
verifier.** Ours is cheap and fast but *not trustworthy at the effect size we
work at* — which is why item 6 is last, not first.

- **FunSearch** (Romera-Paredes et al., *Nature* 2024) — explicitly chose a
  fast-inference, lower-quality LLM over a slower better one, and ran ~10⁶
  samples. The LLM is a mutation operator; the evaluator carries correctness.
  https://www.nature.com/articles/s41586-023-06924-6
- **Large Language Monkeys** (Brown et al. 2024) — coverage scales as a power
  law in samples; a >10x cheaper model at 5 samples beats frontier single-shot
  on cost. Explicit that this converts to *performance* only where solutions
  are **automatically verifiable**. https://arxiv.org/abs/2407.21787
- **X-evolve** (2025) — ablates 8B→72B, finds search performance "largely
  consistent"; effectiveness comes from the scaffold, not model priors.
  https://arxiv.org/pdf/2508.07932
- **AlphaEvolve** (DeepMind 2025) — Flash for breadth, Pro for occasional
  depth. A heterogeneous ensemble, not a tier swap.
  https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
- **Huang et al.** (ICLR 2024) — intrinsic self-correction without external
  feedback *degrades* performance. The cheap runner must never judge its own
  edit; `program.md`'s "no verdict is a discard, not a maybe" is correct and
  must stay mechanical as volume rises. https://arxiv.org/pdf/2310.01798
- **Chen et al.** (NeurIPS 2024) — performance is **non-monotone** in the
  number of LLM calls: more helps easy items, hurts hard ones. Don't set N by
  budget. https://arxiv.org/html/2403.02419v2
- **Blum & Hardt**, *The Ladder* (ICML 2015) — adaptive repeated submissions
  overfit the holdout; a threshold-release rule bounds it. Our Wilson rule *is*
  that mechanism, and the implication is direct: **as candidate volume rises,
  the threshold must not fall.** https://proceedings.mlr.press/v37/blum15.pdf
- **F-Race / irace** (Birattari et al. 2002; López-Ibáñez et al. 2016) —
  racing with statistical elimination + elitist racing.
  https://mlopez-ibanez.github.io/irace/
- **Mutation Without Variation** (2026) — diversity collapse is a documented
  failure mode of LLM-driven program evolution; FunSearch's island model and
  ELM's MAP-Elites archive are the mitigations. We already have behavior
  descriptors on the tape (delivered titanium, full-length rate, per-class
  results) — an archive keyed on those would stop averaging "wins the
  tiebreak" and "survives the rush" into a bot that does neither, which is the
  tension HANDOVER's own strategic read names.
  https://arxiv.org/pdf/2606.05408 · https://arxiv.org/abs/2206.08896

---

## Outcome — adopted same night

Relayed to both arms ~20:5x; both replied within ~20 min. Builder = session
`af1aa9a9`; research = `284161ab`.

- **Both arms independently reproduced the power arithmetic before adopting
  it** (builder: 19% / 50% / 81% / 93% at n=1200; research: 19.2% / 50.0% /
  80.9%, matching to the decimal). Tape row `leg-power-19pct`.
- **It corrected a live conclusion within the hour.** The builder had just
  written `_v98hg-refuted` off an n=120 paired leg: 42 discordant, 20 toward /
  22 against, difference −1.67pp, SE = √42/120 = 5.40pp, **CI [−12.3, +8.9],
  15% power against +5pp.** A real +5pp effect sits comfortably inside. Row
  corrected to *"no effect detected at 15% power"* and re-running at n=600.
  **This is the entry's thesis happening in real time: a plank was closed on an
  instrument that would have missed a real effect five times in six.**
- Builder on the deadlock re-read: *"The gate was the symptom; you found the
  cause"* — and noted it indicts a ship made the same night.
- Item 2 reordered on the builder's reasoning, correctly: **HG first**, because
  it is the only underpowered row where a real effect changes what gets built
  next. The E-family rows are shipped-or-parked, so re-measuring them buys
  attribution, not decisions. They take the caveat now and the re-run when cheap.
- `paired_vs_pooled.py` promoted into `tools/` by the builder (their lane),
  **with the refutation preserved alongside it** — a negative result that
  prevents a build is worth as much as a positive one, and "pairing is cosmetic
  because NOISE_ON reseeds spawn_salt from live entropy" is exactly what someone
  re-derives from scratch in three weeks.

## Amendments

**A1 — item 3 must key on distinct shapes (research arm + builder, concurring;
NOT adopted tonight).** See item 3 above, rewritten. Effective n for a
deterministic gate is the distinct-shape count, not the pair count. Two live
counterexamples the same evening: a 4-seed leg that was one distinct game
replicated, and a 44/120 shape count on an identity control. A gate keyed on
pair count reports n=120 while holding n=44 — a strictly worse version of the
defect this entry diagnoses. Correct call to defer it: worth doing, not worth
doing fast.

**A2 — the distinct-shape correction makes §2's live example *stronger*, and
propagates into the HG re-run.** SE scales as `1/√r` where `r` = distinct
shapes / nominal pairs. If HG's leg runs at the identity control's r≈0.37, the
planned n=600 delivers **~24% power, not 54%**, and n=1200 delivers ~43%, not
83%. Stated narrowly: 44/120 came from an *identity* control, which has low
shape diversity by construction, so a real-effect leg should do better —
**measure r on the HG leg itself before trusting the 54%.** The general rule:
any power figure on a deterministic leg is nominal until divided by its shape
ratio.

**A3 — `fcode submit` AUTO-ACTIVATES (builder's correction to my context).**
There is no upload-without-shipping, so ladder windows are ~1h each, serial,
and unparallelisable. This does not weaken the recommendations; it sharpens
what they are *for*. Local eval is ~50-100x underused; ladder eval is fully
saturated. **Therefore: do all discrimination locally at real power, and spend
each scarce window on a head that is already resolved.** `ship-gate.md`'s
"ship the biggest available change per window" was the right response to scarce
windows *given an instrument that could not resolve one plank* — but bundling
was a workaround for the underpowered instrument, not for the scarce window.
At n=800 legs of 22 min you can resolve ~3 planks/hour locally and ship the one
that won, getting attribution **and** a pre-validated head on the same window.

**A4 — live instance of the adaptive-overfitting risk behind item 7** (research
arm). The probe fleet was tuned against opponents it was then measured against,
and two of five probes turned out class-invalid the same night. Item 7 (hold
out maps; Blum & Hardt) should be on the record **before** item 4 (racing) ever
runs — racing multiplies candidate volume against a fixed evaluation set, which
is exactly the regime the Ladder result bounds.

## Falsifiable predictions from this entry

1. Re-running `_v96ft2-h2h` (currently `0.592 [0.502, 0.675]`, n=120) at n=800
   returns a verdict rather than a straddle, in ~22 min. **If it still
   straddles at n=800, the true effect is under ~3.5pp and the plank is not
   worth a window** — which is itself the decision that could not be reached
   at n=120.
2. A NOISE_OFF paired leg resolves a smaller effect than a NOISE_ON leg of the
   same match count. (v1 measured only the NOISE_ON case; this is untested.)
3. Raising the standard leg to 800 does **not** slow ship cadence, because
   windows (~8 matches ≈ 1h) remain the binding constraint on shipping, not
   local measurement.
