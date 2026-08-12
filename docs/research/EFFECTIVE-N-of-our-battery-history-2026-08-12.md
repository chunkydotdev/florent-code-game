# EFFECTIVE n OF OUR BATTERY HISTORY — `QUEUE.md` #15, ANSWERED

**Research arm, s33, 2026-08-12 ~04:5xZ.** Instrument: `tools/effective_n.py`
(`--selftest` passes, driven to DEGENERATE and to OK and through a collision cell).
**No games were run for this** — every number below comes from battery rows already
on disk, which is why it was available to a lane that cannot run arena.

---

## THE HEADLINE, AND IT IS A CONTROLLED CONTRAST, NOT A ONE-ARM READING

At **matched 3 seeds per cell**, counting cells where every seed produced an
identical outcome (*the seed changed nothing*):

| configuration | population | fully-degenerate cells |
|---|---|---|
| **`NOISE_ON = True`** | 17 overnight shards, **29,296 cells** | **2 — 0.007%** |
| **`NOISE_ON = False`** | `dodge` 88/128 · `dodge2` 88/128 · `loki1base` 92/128 · `loki2b` 97/128 | **68.8% – 75.8%** |
| **`NOISE_ON = False`** | `collar`, 2 seeds/cell | **80.6%** |

**⭐ THIS CONTRAST SURVIVES THE AMENDMENT BELOW, AND MATCHING `seeds_per_cell` IS
WHY.** At k=3 the `NOISE_ON=True` arm sits **at the 3.00 ceiling** and the
`NOISE_ON=False` arm at **1.37** — below ceiling, therefore real information. The
control being ceiling-pinned means the separation printed here is a **LOWER BOUND**:
it can only be wider, never narrower. The decision to match seeds-per-cell across
arms was load-bearing rather than tidy, which is only visible in hindsight.

**A four-order-of-magnitude separation, and the fingerprint used on the
`NOISE_ON=True` arm is COARSER** (the overnight schema has no `collected` column,
so `(winner, cond, turns)` is all there is) — **which biases toward finding
degeneracy in the arm that shows none.** The true separation is wider than printed.

**⇒ s32's finding replicates and its stated boundary is now closed.** s32 measured
ONE bot pair on FOUR maps and correctly refused to generalise (D12). This is **five
independent legs, four distinct opponents** (clanker / flotte / ouroboros / kladde),
**eight maps, both seats, both arms** — and the `NOISE_ON=True` control shows the
instrument returns the other verdict on 29,296 real cells.

---

## WHAT IT COSTS US IN PRACTICE — SMALLER THAN #15 PROJECTED, AND THE REASON MATTERS

`QUEUE.md` #15 projected *"a 1,024-game 8-map battery could carry ~8–16 distinct
outcomes rather than 1,024"* — a one-to-two-order-of-magnitude overstatement.
**Measured on the legs we actually ran, the realised overstatement is ~2.2×:**

```
dodge      384 rows -> 175 distinct games      loki1base  384 -> 168
dodge2     384 rows -> 175 distinct games      loki2b     384 -> 165
collar     144 rows ->  86 distinct games
```

**The projection was right about the MECHANISM and wrong about the SCALE, for one
reason: overstatement grows with seeds-per-cell, and these legs ran only 2–3.**
A cell that replays one game contributes 1 no matter how many seeds you spend on
it, so:

> **⭐ THE DAMAGE IS `seeds_per_cell`, NOT `rows`. Our historical `NOISE_ON=False`
> legs were protected from a catastrophic overstatement only by being SMALL.**

> ## ⛔ AMENDED SAME DAY — THE 338-SEED PROJECTION IS **WITHDRAWN**. IT WAS WRONG TWICE.
>
> **This paragraph originally read: *"A `NOISE_ON=False` battery at that scale would
> carry roughly 1.4 distinct games per cell — an effective n near 180 out of 5,408,
> a ~30× overstatement."* Both halves of that sentence are defective.** Flagged by
> the side lane within ~20 minutes of the commit, ahead of the sizing decisions it
> was heading for; I verified every claim against the primary before conceding.
>
> **DEFECT 1 — THE ARITHMETIC MIXED TWO POPULATIONS.** `180 ≈ 128 cells × 1.4`, but
> **128 is the `_det` legs' cell count** (8 maps × 2 seats × 2 arms × 4 opponents),
> while **5,408 is an overnight shard's row count, and that shard has 16 cells**
> (`map`, `seat`; 338 seeds each) — verified both by direct count. I took the cell
> count of one population and the row count of another. **Corrected within its own
> logic the figure would be 16 × 1.37 ≈ 22, i.e. ~246×, so the error ran AGAINST my
> own argument — the hazard I was warning about would be ~8× worse, not smaller.**
>
> **DEFECT 2 — AND THIS IS THE ONE THAT KILLS IT: THE ESTIMATOR IS CENSORED ABOVE AT
> `k`, SO THE PROJECTION IS NOT IDENTIFIED.** Distinct-outcomes-per-cell cannot exceed
> the seed budget: a cell drawn 3 times reports at most 3. Censoring the *same*
> `NULL114` shard to smaller `k` shows the statistic returning **exactly `k`**:
> ```
> k=2 -> 2.00   k=3 -> 3.00   k=5 -> 5.00   k=10 -> 10.00      (all pinned AT ceiling)
> k=50 -> 46.44   k=338 -> 238.44           (truth: 1.4x overstatement)
> ```
> **Apply my projection method to that checkable shard and it predicts 112.7× where
> the real answer is 1.4×.** Since distinct-outcomes is non-decreasing in `k`, the
> measured **1.37 distinct/cell at k=3 is a LOWER BOUND** and says nothing about
> k=338. **The honest interval is effective n ∈ [22, 5408] — completely
> unidentified.**
>
> **WHAT WOULD SETTLE IT:** one shard — the same battery config with
> `NOISE_ON=False` at 338 seeds/cell. Builder ask, cheap, and it would also settle
> whether `det.py:135-142`'s *"the seed drives nothing that is still switched on"*
> means literally 1.0 distinct/cell (⇒ ~338×) or something above it.
>
> **INSTRUMENT FIXED, and the cell that would have caught this is the cell that was
> certifying it.** `effective_n.py` now prints `seeds_per_cell` and the cell key on
> every line and returns a **`CEILING`** verdict when mean distinct/cell ≥ 0.98·k,
> refusing to be quoted as an overstatement factor there. The old selftest asserted
> *"eff_n is near the row count"* as its PASS condition for the independent fixture
> — **which is the ceiling read, so the one cell that could have caught this was
> instead certifying it.** New cells: a known-independent fixture censored to k=3
> must read `CEILING`, not `OK`; degeneracy must still outrank `CEILING` (a cell
> returning 1 of 3 is BELOW ceiling and is real information); and the collision
> fixture must read NOT-at-ceiling, so `CEILING` cannot become a constant that
> fires on everything.

**The live hazard is therefore real in DIRECTION and UNQUANTIFIED in SIZE**, and
tonight's shards did not run into it: all 17 ran `NOISE_ON = True` (verified at
`doctrine.py:474` in `_v146gunaxis`, `_v146null`, `_v154gunferry`, `_v140noseal`,
`_v145bestfit` — checked, not assumed).

---

## THE PRESCRIPTION THAT MANUFACTURES IT IS STILL IN THE GATE

`gate.py` instructs *"flip `NOISE_ON` to False in this COPY"* and **63 of 256 bot
trees carry `NOISE_ON = False`** as a result. Its own cited authority,
`tools/det.py:135-142`, already says that under `NOISE_ON=False` *"the seed drives
nothing that is still switched on"*, prints `LOW REPLICATION`, and exits 2.
**The two files contradict each other and the gate cites the one that refutes it.**
This report supplies the number that was missing from that argument.

**⇒ BUILDABLE CHANGE (builder-owned):** a battery whose **n is quoted** must not
pin `NOISE_ON = False` on both sides. Determinism belongs in the *reproducibility*
check (`det.py`'s job), not in the *measurement* run. If a gate wants both, it must
report **effective n**, not row count.

---

## ⛔ AND MOST OF OUR BATTERY HISTORY CAN NEVER BE AUDITED FOR THIS

Established by a delegated sweep with a positive control on every search family
(the method was required to find `scratchpad/overnight/NULL114.tsv` each time):

* **`tools/arena.py` builds a per-game result dict (`:47-88`) and never writes it.**
  `main()` prints aggregates and discards the games. Confirmed independently by
  `docs/legs/LEG-loki17-battery-2026-08-10.md:55`: *"`tools/arena.py` does not retain
  replays — it reports win rates and discards the games."*
* **`tools/mech_battery.py:181-183` is the ONLY runner that persists per-game rows**
  (`full.json`). That subset is what this report measures.
* **The `_abl_c0.._abl_c4` ablation legs have NO per-game rows anywhere** — every
  trace is prose reporting an aggregate. `git log --all --diff-filter=D` shows none
  was ever committed and deleted. **Their effective n is unknowable, permanently.**

⇒ **The answer to "how much of our battery history has an effective n nobody
computed" has two parts: for the `mech_battery` legs it is now computed and it is
~2.2×; for everything `arena.py` ran and for every `_abl_*` leg it CANNOT be
computed, because the rows were never written.** That is the more durable finding,
and the fix is one line in `arena.py`.

---

## SCOPE — WHAT THIS DOES NOT SAY

* It does **not** retire any past conclusion. A 2.2× effective-n overstatement
  widens intervals; it does not flip signs, and I have not re-scored any leg.
* The `NOISE_ON=False` legs measured here ran **2–3 seeds/cell**, so the per-leg
  degeneracy percentages are estimated on few draws per cell; the *contrast* with
  29,296 control cells is the robust part, not any single leg's percentage.
* `(win, cond, turns, collected)` is a **fingerprint, not proof of identity**. It
  can only ever **undercount** distinct games, so every effective-n figure here is
  a **lower bound** — which is the safe direction for this claim and the unsafe
  direction for the control, where it still read 0.007%.
