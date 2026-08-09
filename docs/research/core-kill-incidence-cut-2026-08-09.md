# The core-kill INCIDENCE cut — what separates the games we land a core kill from the games we don't

**Research arm, 2026-08-09.** Read-only with respect to the bot; no arena, no
submissions, **zero replay downloads** (every byte read was already on disk).

**Version tag.** Live ladder slot **v94 = `bots/_v115dodge`, treehash `6ae6871c`**.
Corpus git sha as handed to me: `7418e13` (~6,233 replays). **The keeper daemon
had already moved past that when I froze:** `corpus/manifest.json` at freeze time
read `git_sha d3f9ef9`, `archive_replays 6353`, built `2026-08-09T14:29:44Z`.
I froze at that state and every number below comes from the frozen copies, not
from live `corpus/`.

### Frozen inputs (md5, rows excluding header)

| file | rows | md5 |
| --- | ---: | --- |
| `corpus/ladder_games.tsv` | 2,715 | `ca2c6f599839fb30d9284b28bdec46d2` |
| `corpus/join.tsv` | 1,445 | `e943d4ac38e5339ac7c577263b9156cf` |
| `corpus/build_agg.tsv` | 149,543 | `67e06c508ff70b3379c0996a9ff4a672` |
| `corpus/econ.tsv` | 37,114 | `b6724abf215064ccaf70867db8fdb20b` |
| `corpus/flow.tsv` | 68,065 | `b2672b31cbf94e1e1033dc2e7de76493` |
| `corpus/events.tsv` | 1,034,628 | `569796904e15be637192b81afdd29b51` |
| `corpus/builds.tsv` | 92,801 | `3c7dd227d407656a845fe4d98d7b40ff` |
| `corpus/throws.tsv` | 100,046 | `4bdf02e5a0233ce805f3a08825f4fb2c` |

### Derived here (new decoders, 1,445 joined replays each, 0 errors)

| file | rows | md5 | produced by |
| --- | ---: | --- | --- |
| `fineband.tsv` | 18,508 | `658b0c3518592d93efa9a16c3bcb9092` | `fineband_econ.py` |
| `positions.tsv` | 18,508 | `507334dcc9561d91a8bd7578f3400449` | `fineband_positions.py` |
| `mech.moves.tsv` | 301,577 | `9073f80c00f660fdfdcec4052e26a930` | `mechanism_slot_under.py` |
| `mech.games.tsv` | 2,890 | `9e264d0411aad87a4c5956500b268da0` | `mechanism_slot_under.py` |

Scripts: `docs/research/scripts/2026-08-09-core-kill-incidence/` —
`fineband_econ.py`, `fineband_positions.py`, `mechanism_slot_under.py` (decoders),
`build_dataset.py`, `analyze.py`, `probe.py`, `mechanism_report.py`.
Re-runnable against any frozen snapshot dir.

---

## THE QUESTION, AND WHY IT IS INCIDENCE AND NOT SPEED

`PROGRAMME.md` sets `PRIMARY_CURRENCY: core_kill_share`,
`SECONDARY_CURRENCY: time_to_core_kill`, `KILL_WINDOW_RND: 250`, and everyone has
been building toward the **window**. The ladder cut that motivated this work says
the window is not the binding constraint: of 827 ladder core-kill wins the median
is r151 and **74.4% are already inside r250**, holding at 71.4% against opponents
rated 1600+. What is scarce is the kill **happening at all** — `core_kill_share`
runs 22-41% by band, and against Ouroboros it is 9 in 155 (5.8%), of which 8 are
inside r250 at median r95.

So: **we are already fast; we almost never arrive.** This document asks what
distinguishes arriving from not arriving.

---

## DESIGN — and specifically how it defends against outcome-conditioning

The failure mode this cut had to survive is that almost every measurable feature
is a **consequence** of winning. The library's own statement of it:

> *"Any 'X rarely happens by round N' comparison where X TAKES TIME TO ARRANGE is
> conditioning on survival. The fix is a per-round hazard, which is also the only
> form a bot can act on."*

Four defences, in order of how much work they do.

**1. LANDMARK AT r50 — and this one is airtight here, not merely careful.**
Every feature is accumulated strictly inside `[0, T)`. The population at landmark
`T` is every joined ladder game still running at round `T`. **The earliest core
kill anywhere in the 1,445-game corpus is round 61.** So at `T=50` the landmark
population is 1,444 of 1,445 games (one game ended earlier, a loss) and there is
**zero survival censoring**: no `r0-50` feature can be downstream of an outcome
that has not happened in any game yet. Landmarks at `T=100` and `T=150` are
reported too, but they *are* censored — they drop the fast kills — and are
labelled as secondary throughout.

**2. FOUR STRATIFICATIONS, and a feature must survive all four.** Opponent
identity is the dominant confounder in this corpus, and our own bot version is a
second one that is easy to miss: **27 of our versions appear in the corpus and
their core-kill share runs 0% to 100%.** A "we healed more in kill games" result
could be nothing but "the versions that heal more are the versions that kill
more". Every test is a **van Elteren stratified rank test** (the stratified
Wilcoxon) run under:

| stratification | strata | what it kills |
| --- | ---: | --- |
| `oppbef` quartile | 4 | "strong opponents are just harder" |
| opponent **name** | 26 | any between-opponent effect at all |
| **our own `ourver`** | 27 | "that feature is a version signature" |
| opponent × `ourver` | 50 | both at once (n=675 of 1,444, 193 kills — low power, but confound-proof) |

Effect size is the stratum-weighted AUC, using **the same weights the test uses**,
so the reported AUC can never disagree in sign with its own `z`. AUC 0.5 is null;
AUC below 0.5 means the feature is **lower** in kill games.

**3. MULTIPLICITY.** **K = 64 features** were tested (29 per side × 2 sides, plus
map area, opponent rating, and two controls), **pre-listed in `analyze.py` before
the first run** and Holm-adjusted as one family, under each stratification
separately. A feature is a **FINDING** only if Holm-adjusted p < 0.05 under **all
four** stratifications with a consistent sign. Raw p < 0.05 that does not survive
is reported as a **LEAD** and labelled. Everything in §"post-hoc probes" is
explicitly post-hoc characterisation of an already-established discriminator and
adds no tests to the family.

**4. TWO CONTROLS.**
- *Negative:* a seeded shuffle of a real feature. Must be null. **It is** —
  AUC 0.525/0.525/0.527/0.526, Holm p = 1.0 in all four.
- *Positive:* a late, admittedly-consequential feature (their conveyors destroyed
  by r150). This one is instructive: it reaches Holm p = 0.018 under rating
  strata and **collapses to null under opponent strata** (AUC 0.501). A feature
  that looks consequential across opponents and vanishes within them is exactly
  the artefact the design was built to remove, and it demonstrates the machinery
  removing it.

---

## VALIDATION

Three independent decoders were cross-checked against the packaged corpus before
any result was read. **1,445 files × 2 teams = 2,890 file-team cells.**

```
fineband vs build_agg[r0-150] shot          : 2890 agree / 0 disagree
fineband vs build_agg[r0-150] batk          : 2890 agree / 0 disagree
fineband vs build_agg[r0-150] batk_core     : 2890 agree / 0 disagree
fineband vs econ[r0-150]      ammo_converted: 2890 agree / 0 disagree
events   vs build_agg[r0-150] build_gunner  : 2890 agree / 0 disagree
events   vs build_agg[r0-150] build_sentinel: 2890 agree / 0 disagree
events   vs build_agg[r0-150] build_harvester:2890 agree / 0 disagree
events   vs build_agg[r0-150] build_builder_bot: 2890 agree / 0 disagree
events   vs build_agg[r0-150] build_conveyor: 2890 agree / 0 disagree
```

**All-zero column sweep on the new files** (the trap-5/trap-6 class — an exact
zero is a bug signature before it is a finding): every one of
`shot, batk, batk_core, ammo_converted, heals, tled, ti_end, ammo_end,
ti_collected_end, bots_mean, collar8_mean, collar2_mean, fwd_mean, r36_rounds,
r20_rounds` is non-zero in aggregate. Full output in the scratchpad
`validation.txt`.

**The two's-complement HP trap:** across the 1,445 joined replays the mechanism
decoder sees **523,802 negative** and **502,504 positive** `updateHp` deltas.
Both signs present, so the sign handling is live rather than silently collapsing —
the exact failure that once produced "0 core damage across 11,895 insertions".

**Traps honoured:** `placeEntity` rotation re-emit guarded in all three new
decoders (a build is the FIRST `placeEntity` for an id); `econ.tsv.shots` and
`econ.tsv.deliveries` never read (both zero in every row) — shots come from the
fine-band decoder, cross-validated against `build_agg.tsv metric=='shot'`;
`BuilderAttack` (Update field 13) used rather than HP arithmetic;
throws restricted to `amb == 'one'`; **version columns never used for
stratification** (`oppver` is the literal string "None" everywhere — our own
`ourver` IS populated and IS used).

**Population.** 1,445 archived replays join to our ladder games (100% of
`join.tsv`; the join's own reconciliation is 1,445/1,445). **479 are core-kill
wins by us (33.1%)**, 536 are core-kill losses, 430 decided on titanium.
Outcome variable throughout is **"did WE win by `core_destroyed`"**, not "did we
win".

---

## RESULT 1 — THE PRE-REGISTERED SEARCH: 6 of 64 features are robust

Holm-adjusted p < 0.05 under **all four** stratifications, consistent sign.
"Worst Holm p" is the largest of the four.

| # | feature | ours/theirs | AUC (rating / opp / ourver / opp×ver) | worst Holm p | direction |
| ---: | --- | --- | --- | ---: | --- |
| 1 | `THEM_ti_collected_end_w50` — their titanium collected by r50 | **theirs** | 0.325 / 0.331 / 0.329 / 0.342 | 5.3e-06 | **LOW → we kill** |
| 2 | `US_shot_w50` — our turret shots fired r0-50 | ours | 0.643 / 0.636 / 0.652 / 0.677 | 1.5e-07 | **HIGH → we kill** |
| 3 | `US_ammo_converted_w50` — our Ti→ammo r0-50 | ours | 0.642 / 0.628 / 0.648 / 0.641 | 1.4e-04 | HIGH → we kill |
| 4 | `THEM_b_harvester_w50` — their harvesters built r0-50 | **theirs** | 0.316 / 0.362 / 0.314 / 0.373 | 4.0e-04 | LOW → we kill |
| 5 | `THEM_b_conveyor_w50` — their conveyors built r0-50 | **theirs** | 0.364 / 0.393 / 0.365 / 0.377 | 2.0e-03 | LOW → we kill |
| 6 | `THEM_ti_end_w50` — their titanium banked at r50 | **theirs** | 0.364 / 0.395 / 0.372 / 0.382 | 3.6e-03 | LOW → we kill |

Medians, kill games vs non-kill games: their titanium collected **100 vs 180**,
their harvesters **2 vs 3**, their conveyors **8 vs 12**, their bank **25 vs 47**;
our shots **13 vs 8**, our ammo converted **138 vs 96**.

**Six features, two constructs.** Rank correlations: the four enemy features
inter-correlate +0.42 to +0.81; our two correlate **+0.870** with each other; and
across the divide the correlation is **+0.03 to −0.13**. They are two nearly
orthogonal signals:

- **THEIRS — "their early economy failed to launch."**
- **OURS — "we are already shooting by r50."**

Each survives conditioning on the other (strata = opponent × tertile of the
other): `US_shot` inside tertiles of their titanium collected, AUC 0.638,
p = 6.7e-11; their titanium collected inside tertiles of our shots, AUC 0.314,
p < 1e-15.

### What died, and it is worth naming

Several features that look like the obvious answer are **artefacts of opponent
identity** — strong under rating-band strata, null within opponent:

| feature | AUC rating strata | AUC opponent strata |
| --- | ---: | ---: |
| `THEM_turfwd_w50` their turrets on our half | 0.639 | 0.506 |
| `THEM_tur36_w50` their turrets near our core | 0.645 | 0.552 |
| `THEM_ammo_converted_w50` | 0.655 | 0.526 |
| `THEM_fwd_mean_w50` their builders on our half | 0.598 | 0.533 |
| `US_heals_w50` our builder heals | 0.663 | 0.560 (and 0.536 under opp×ver) |
| `US_collar8_mean_w50` our builders on our collar | 0.592 | 0.518 |

**"Enemy turret count / type mix / forwardness / collar occupancy"** — four of the
shapes named as priority candidates — **all land here.** They tell you which
opponent you are playing, not which game you are in. `US_heals_w50` is the
cleanest illustration: median 31 in kill games against 9.5 in non-kill games, an
apparently overwhelming result, that shrinks to almost nothing once our own bot
version is held constant. It was a version signature.

**Also null:** map area, opponent rating, seat, our own turret placement forward,
our builder attacks on their core, our throws, their launcher builds, their
throws (enemy interception), CPU timeouts on our side, every attrition counter on
both sides.

---

## RESULT 2 — DID "OUR OPENING IS A CONSTANT" HOLD?

**It held for production and broke for contact — and the split is exactly along
the line that matters.**

**17 of 30** of our own `r0-50` medians are *identical* between kill and non-kill
games, including every production counter: builder bots (5 vs 5), harvesters
(3 vs 3), turrets (2 vs 2), sentinels (1 vs 1), gunners (0 vs 0), launchers
(0 vs 0), barriers (0 vs 0), builders alive (4.80 vs 4.80), turrets forward
(1 vs 1). **Not one of those production counters is a robust discriminator.**

Our coefficient of variation confirms it is us, not the measurement: builder bots
built, CV **0.09 for us against 0.26 for them (2.74×)**; builders alive, 0.09
against 0.23 (2.40×); sentinels, 0.53 against 1.46 (2.76×). **Our opening really
is close to a constant and theirs is not.**

What broke the claim is that two of our `r0-50` counters are **not opening
choices at all** — `US_shot_w50` and `US_ammo_converted_w50` are *reactive*.
They record that contact happened early and we engaged it. So the corrected
statement is:

> **Nothing we BUILD early discriminates. What discriminates on our side is
> whether we were already fighting.**

That is a weaker claim than "the variance is entirely the opponent's", and it is
the one the data supports. Four of the six robust features are still theirs, and
the single largest effect is theirs.

---

## RESULT 3 — POST-HOC PROBES (characterisation, not new tests)

### The actionable 2×2, split at population medians

| our shots r0-50 | their Ti collected by r50 | n | core-kill wins | **incidence** |
| --- | --- | ---: | ---: | ---: |
| ≤ 10 | > 170 | 338 | 47 | **13.9%** |
| ≤ 10 | ≤ 170 | 447 | 138 | **30.9%** |
| > 10 | > 170 | 333 | 108 | **32.4%** |
| > 10 | ≤ 170 | 326 | 186 | **57.1%** |

**4.1× from corner to corner**, and both axes move within levels of the other.

As one ordered signal, `rank(our shots) − rank(their Ti collected)`, by quintile:

| quintile | n | core-kill wins | **incidence** | median kill round |
| --- | ---: | ---: | ---: | ---: |
| Q1 (quietest) | 288 | 33 | **11.5%** | 284 |
| Q2 | 289 | 60 | 20.8% | 185 |
| Q3 | 289 | 84 | 29.1% | 182 |
| Q4 | 289 | 123 | 42.6% | 147 |
| Q5 (most violent) | 289 | 179 | **61.9%** | 117 |

**5.4× on incidence, monotone across all five quintiles, and the median kill
round falls from r284 to r117 across the same range.** The secondary currency
comes along for free.

### The signal predicts speed too — but only our half of it

Among core-kill wins only, rank correlation with the round of the kill:

| feature | corr with kill round |
| --- | ---: |
| `US_shot_w50` | **−0.457** |
| `US_ammo_converted_w50` | **−0.449** |
| `THEM_ti_collected_end_w50` | −0.092 |
| `THEM_b_harvester_w50` | −0.035 |
| `THEM_b_conveyor_w50` | −0.011 |
| `THEM_ti_end_w50` | +0.078 |

Being already armed and shooting by r50 is strongly associated with a **faster**
kill. Their economy failing is associated with **whether** we get there, not how
fast. Two currencies, two different levers.

### Map is a fifth stratification and it changes nothing

All six hold with strata = map (15 maps, 87-110 games each): their titanium
collected AUC 0.314 (z −11.5), their harvesters 0.308 (z −12.0), our shots 0.662
(z +9.9), our ammo 0.666 (z +10.1).

### Opponent holdout — not opponent-fitted

Splitting the 33 opponents into two halves by alternating corpus size:

| feature | AUC half A (n=744) | AUC half B (n=655) |
| --- | ---: | ---: |
| `THEM_ti_collected_end_w50` | 0.355 | 0.309 |
| `THEM_b_harvester_w50` | 0.392 | 0.334 |
| `THEM_b_conveyor_w50` | 0.382 | 0.403 |
| `THEM_ti_end_w50` | 0.424 | 0.367 |
| `US_shot_w50` | 0.649 | 0.624 |
| `US_ammo_converted_w50` | 0.634 | 0.622 |

### What are they doing instead? Nothing — the economy just fails

Within opponent, comparing their lowest tertile of `r0-50` titanium collected
against their highest (n = 447 each):

| their feature, r0-50 | low-economy games | high-economy games |
| --- | ---: | ---: |
| titanium collected | 51.3 | 290.1 |
| harvesters built | **1.64** | **4.45** |
| turrets built | 2.90 | 2.84 |
| gunners built | 1.88 | 1.70 |
| sentinels built | 0.57 | 0.62 |
| launchers built | 0.46 | 0.51 |
| titanium converted to ammo | 161.8 | 163.3 |
| builder bots built | 4.45 | 4.73 |
| **unit-turns lost to CPU timeout** | **2.80** | **0.55** |
| → our core-kill rate | **45%** | **23%** |

**They did not trade economy for military.** Turrets, ammo, gunners, sentinels,
launchers and builders are all flat; only the economy differs — and their CPU
timeouts are **5× higher** in the low-economy games. This is not a strategic
choice we are reading. It is **the opponent's opening partially failing**, and
one visible cause of the failure is their own bot losing turns to the 10 ms
budget.

This is important for the trigger reading: the enemy signal is **not** "they
committed to aggression". It is **"their economy did not come up"**.

### Ouroboros cell — reported separately, UNDERPOWERED

`n = 105` archived joined games, **5 core-kill wins (4.8%)**. Five positives
cannot carry an inference and nothing here is concluded from. Directions match
the population on all six:

| feature | mean, kill games | mean, non-kill | unstratified MW p |
| --- | ---: | ---: | ---: |
| their titanium collected by r50 | 170.0 | 274.7 | 0.178 |
| their harvesters r0-50 | 2.4 | 4.7 | 0.041 |
| their conveyors r0-50 | 10.0 | 17.1 | 0.031 |
| their titanium banked at r50 | 29.4 | 78.2 | 0.057 |
| our shots r0-50 | 13.2 | 9.5 | 0.074 |
| our ammo converted r0-50 | 136.6 | 101.8 | 0.071 |

Six raw p-values at n=5 positives, none Holm-adjusted, all consistent in sign
with the population result. Treat as **corroboration of direction only**.

Context: Ouroboros is a **strong-economy** opponent against us — **4.61 harvesters
and 269.7 titanium collected by r50** on average, the **second-highest early
harvester count of the 26 opponents with ≥10 archived games**. Under
this cut, the reason we do not kill their core is not that they intercept our
raiders (they build 0 launchers and throw 0 bots in 105 games — measured
separately) and not that they pin us at home (see §Mechanism below). It is that
**their opening does not fail**, and the trigger this cut identifies simply does
not fire against them.

---

## RESULT 4 — THE PRE-REGISTERED MECHANISM TEST (`SLOT_UNDER` / the shelled core)

Handed to me as a named hypothesis derived from our own source, and **exempted
from the K=64 Holm family** because it was specified before measurement and does
not draw on the search's multiplicity. Stated as: *a raider within `dsq 25` of a
damaged home core heals it and RETURNS from `run()` before `_raid` is called; the
50-round `SLOT_UNDER` latch keeps this on permanently against a shelling
opponent, so our raiders never leave home.*

### Finding 4a — the cited code is not in any game in this corpus

`near_home = p.distance_squared(self.core) <= 25` and the block that follows it
exist in **`_v105loki1`, `_v117loki2`, `_v117off`, `_v118loki2b`,
`_v118lokinorush`, `_v118off`, `_v119loki3`, `_v119loki3off`, `_probe_loki3gate`
only** — grep across all 234 bot directories. **`bots/_v115dodge`, the incumbent
that produced the ladder corpus, has no `near_home` and no `dsq 25` gate at all.**
Our versions in the corpus run `ourver` 64-94; the gate first appears at v105.

**No game in this corpus was played by a bot containing the cited line.** The
mechanism cannot be confirmed or refuted where it lives, from this data. What
*can* be tested is the behaviour the line is supposed to cause, in the Eir family
that does have the `SLOT_UNDER`-gated core heal.

### Finding 4b — the pin is REAL, very large, and at the WRONG THRESHOLD

P(one of our builder bots moves this round), r0-150, by distance to our own core,
split by whether our core was damaged at the start of the round — with **the
opponent's builders around the opponent's own core as a control**:

| window | US n (dmg) | US P(move) dmg | US P(move) full | **US suppression** | THEM P(move) dmg | THEM full | THEM suppression |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| d² ∈ {1,2,4,5} — **orthogonally adjacent to the core footprint** | 143,812 | **0.155** [0.153,0.157] | 0.683 | **−0.527** | 0.282 | 0.434 | −0.152 |
| d² 6-20 — near but NOT adjacent | 47,510 | 0.637 | 0.678 | −0.041 | 0.627 | 0.608 | +0.020 |
| d² 21-25 — **inside the `dsq 25` gate** | 6,000 | 0.577 | 0.633 | −0.055 | 0.522 | 0.558 | −0.035 |
| d² 26-30 — **just outside the `dsq 25` gate** | 11,891 | 0.501 | 0.584 | −0.082 | 0.560 | 0.511 | +0.049 |
| d² 31-60 | 28,998 | 0.601 | 0.621 | −0.020 | 0.605 | 0.575 | +0.031 |

A builder standing beside our damaged core moves **15.5% of rounds against 68.3%
when the core is at full HP** — a 4.4× suppression on n = 143,812 samples, with
the within-game placebo behaving exactly as the mechanism requires. The
opponent's own builders show only −0.152 in the same window, so **this is our
code, not a property of the game.**

But the threshold is **orthogonal adjacency to the 2×2 core footprint**, which is
what `can_heal()` enforces — d² ∈ {1,2,4,5} from the anchor. **d² = 8 is the
diagonal corner, one tile further out and adjacent to nothing, and the
suppression is gone there** (0.633 vs 0.641 full-HP). There is **no step at
d² = 25**: 21-25 shows −0.055 and 26-30 shows −0.082, i.e. *slightly more*
suppression just outside the gate than just inside it. **The `dsq 25` gate is not
what pins anything.** It never could be — `_heal_core` walks the footprint and
lets `can_heal()` enforce adjacency, so even in the Loki line `near_home` only
skips a scan; the binding constraint is adjacency, one tile wide.

### Finding 4c — no 50-round latch signature

P(move) for our near-home builders against rounds since our core last lost HP:

| rounds since our core last took damage | near (d²≤25) n | P(move) | far (d²>25) n | P(move) |
| --- | ---: | ---: | ---: | ---: |
| 1-5 | 206,534 | **0.318** | 87,187 | 0.485 |
| 5-10 | 20,752 | 0.569 | 8,855 | 0.542 |
| 10-25 | 29,701 | 0.591 | 18,094 | 0.585 |
| 25-50 | 24,739 | 0.628 | 19,618 | 0.591 |
| 50-75 ← latch expiry | 14,205 | 0.665 | 11,579 | 0.582 |
| 75-150 | 11,837 | 0.682 | 10,385 | 0.611 |
| never damaged | 271,971 | 0.688 | 185,006 | 0.534 |

**Recovery is essentially complete by 10 rounds and there is no break at 50.**
The suppression tracks *contemporaneous damage*, not the latch — which is exactly
what the code says, because `can_heal()` refuses a full-HP core and the latch only
opens the door. **The 50-round persistence the hypothesis predicts is absent.**

### Finding 4d — the Ouroboros premise does not hold, and dispersal does not buy kills

Per opponent (≥10 archived games, N stated in the full table):

- Our core is damaged in **8.8% of rounds against Ouroboros** — among the *lowest*
  in the whole field, below Lunds Stallions (39.0%), The Bisons (56.4%),
  arsonist duck (63.1%). Their 99 shots/game are largely **not landing on our
  core**. The premise "against them the latch is effectively always on" is false.
- Our builders sit **outside d²=25 in 47.2% of samples against Ouroboros**, above
  the field median. **Our raiders do leave home against Ouroboros.**
- Across the 26 opponents with ≥10 games: corr(their shots/game, our dispersal)
  = **−0.280**; corr(share of rounds our core is damaged, our dispersal) =
  **−0.450**. So the dose-response for the *pin* is real and in the predicted
  direction.
- But corr(our dispersal, our core-kill share) = **−0.171** — the **wrong sign**.
  And within opponent, only **9 of 21** opponents show higher dispersal in the
  games we land a core kill, mean difference **−0.018**. Against Ouroboros
  specifically, dispersal is **lower** in the 5 kill games (0.217) than in the
  non-kill games (0.402).

**Verdict on the mechanism.** Real effect, wrong threshold, wrong latch, and no
demonstrated payoff. Specifically:

1. **CONFIRMED:** a damaged core pins our builders hard, and it is our code.
2. **REFUTED:** the threshold is orthogonal adjacency (d² ∈ {1,2,4,5}), **not
   `dsq 25`**. No step at 25 exists.
3. **REFUTED:** no ~50-round persistence. Recovery completes in ~10 rounds.
4. **REFUTED:** the Ouroboros premise. Our core is damaged less often against
   Ouroboros than against most of the field, and our builders are more dispersed,
   not less.
5. **NOT SUPPORTED:** dispersal does not predict core kills within opponent.
   Repairing the pin would free roughly the builders standing on four tiles; the
   corpus gives no evidence that those bodies being elsewhere converts to kills.
6. **UNTESTABLE HERE:** the cited Loki line itself. It is not in any archived
   game. If the builder wants it measured, that is an arena question, not a
   corpus question.

I am reporting this as a **refutation of the specific defect claim, with a
confirmed but differently-located behaviour underneath it.** The builder should
not spend a plank on the `dsq 25` gate on this evidence.

---

## ACTIONABILITY — can a bot read this at runtime?

Ranked by **buildability as a trigger**, which is not the same order as effect
size.

### Tier 1 — readable by a single unit, zero latency, no scouting: "are we already shooting?"

`US_shot_w50` (AUC 0.64-0.68, worst Holm p 1.5e-07) and `US_ammo_converted_w50`
(0.63-0.65) are one construct, and the **core can compute it exactly, alone, with
two numbers it already has**:

```
ammo_spent_so_far = (cumulative amount the core has passed to convert_ammo)
                    - ct.get_global_ammo()
```

The core is the only unit that calls `convert_ammo`, so it can keep the running
total in its own instance state — no store slot, no cross-unit pooling, no
last-writer-wins hazard. Ammunition has **no passive income and no source but
conversion**, so the difference is spent ammo, and spent ammo is shots
(gunner 4, sentinel 10). One integer, one getter, available every round from
round 0.

Caveat, and it is the important one: **this is a marker, not a proven dial.**
The observational association cannot separate "we chose to arm early and that
caused kills" from "there was something to shoot at, and that caused both". The
0.870 correlation with ammo conversion, and the fact that conditioning each on
the other leaves both weak (AUC 0.568 and 0.549), says they are one thing seen
twice. **Only an arena A/B can turn this into a dial**, and that is the builder's
instrument, not mine. What the corpus does say is that if a bot wants a *cheap,
free, single-unit reading of how violent this game already is*, this is the best
one available and it also predicts speed (corr −0.457 with kill round).

### Tier 2 — readable, but costs a scout and one round of store latency: "did their economy come up?"

`THEM_b_harvester_w50` and `THEM_b_conveyor_w50` are the runtime-readable proxies
for the largest effect in the cut (`THEM_ti_collected_end_w50`, AUC 0.32). Their
early economy sits close to their own core:

| their r0-50 building | n | median d² to their core | within d²≤20 (a builder's vision) | within d²≤36 | within d²≤64 |
| --- | ---: | ---: | ---: | ---: | ---: |
| harvester | 4,275 | 25 | **43.6%** | 73.8% | 88.2% |
| conveyor | 16,227 | 13 | **70.1%** | 83.7% | 94.3% |

**One builder bot parked at their ring sees 70% of their early conveyors and 44%
of their early harvesters** through `get_nearby_buildings` /
`get_entity_type` inside r²=20. Conveyor count is the better read of the two —
denser, closer in, and 16,227 observations against 4,275.

Cost, stated honestly: one builder's tempo plus the travel, and one store slot to
publish the count (a **single** writer, so last-writer-wins is safe; **writes are
visible only next round, so a one-round latency**; and **negative writes raise and
destroy the unit**, so the slot must carry a non-negative count).

### Tier 3 — NOT runtime-readable, report only

`THEM_ti_collected_end_w50` (the largest single effect, AUC 0.32) and
`THEM_ti_end_w50` are the **enemy's global titanium counters**. There is no
`Controller` getter for the opponent's resources — `get_global_resources()` is
this team's balance. **Inadmissible as a trigger.** Nearest sensible proxy is
Tier 2's harvester/conveyor count, which correlates +0.81 / +0.65 with it.

### What a trigger built on this would look like, and what it would be worth

Both tiers are independent (rank corr +0.03 to −0.13), so a bot reading **both**
spans 13.9% → 57.1% core-kill incidence, and a bot reading **only Tier 1** still
spans 13.9%/30.9% → 32.4%/57.1% — roughly 2× within either level of the enemy
signal. The ordered composite runs 11.5% → 61.9% monotone across quintiles with
median kill round falling r284 → r117.

**And note what the trigger is NOT.** Tactics sweep 14 found that every deadline
attack that converted elsewhere fired as a conditional fallback keyed to a
scouting trigger — BC2025 The Kragle rushing *only when scouting found the
economic opening denied*. This cut converges with that on the **shape** (an
observable enemy state, read early, gating commitment) but **not on the content**.
Kragle's trigger was *our* opening being denied. Ours is **theirs failing** — and
§"what are they doing instead" shows they are not substituting into military at
all; their turrets, ammo and builders are flat and only the economy differs, with
5× the CPU timeouts. So the honest statement of the trigger is:

> **Commit when the opponent's economy has not come up by r50 — not when they
> have committed to aggression.**

That is a materially different trigger from the one the Kragle analogy would
suggest, and it should not be implemented as "rush when they look aggressive".

---

## NON-COVERAGE AND LIMITS — stated, not implied

1. **This is observational. Nothing here is a causal claim.** Every result is an
   association measured in a landmark window. The landmark and the four
   stratifications rule out reverse causation from the outcome and the two
   biggest confounders; they do not rule out an unmeasured common cause. The
   ordering of the actionability tiers reflects this: Tier 1 is a marker whose
   dial-ness is untested.
2. **The archive is not a random sample of the field.** 1,445 joined games across
   33 opponents, per-opponent coverage 5-130. Every per-opponent number states
   its N. "Ouroboros never does X" always means "never against us, in 105
   archived games".
3. **`ourver` spans 64-94 — a moving bot.** Stratifying by version removes the
   between-version confound but means the effect is an average over 24 versions
   of ourselves, not a property of v94. It cannot say whether the incumbent
   specifically behaves this way.
4. **The r100 and r150 landmarks are censored** and their levels are not
   comparable to r50. Only the r50 landmark is censoring-free, and only it carries
   the findings.
5. **Ouroboros is 5 positives.** Reported for direction only, adjusted for
   nothing.
6. **The mechanism test could not touch the code it was about.** The `dsq 25`
   gate is Loki-only and Loki has no ladder games in this corpus. §4b-4d test the
   Eir family's `SLOT_UNDER`-gated core heal, which is a related but distinct
   thing.
7. **`P(move)` includes move-cooldown rounds.** The placebo split is what
   separates choice from cooldown — cooldown does not care whether our core is
   damaged — but the absolute levels are not "fraction of rounds the bot chose to
   move".
8. **Shots are attributed by shooter position** (the same method as
   `replay_builds.py`); a `fireTurret` whose position matches no live
   gunner/sentinel is dropped. The 2,890/2,890 agreement with `build_agg.tsv`
   means my decoder reproduces the packaged one exactly — it does not
   independently prove either is right.
9. **Launcher throws landing exactly one tile away are undercounted** (trap 3);
   `UNATTRIB` throws are excluded, not guessed. Throws were null in the search
   regardless.
10. **Not examined:** per-round titanium and ammo *trajectories* (only band-end
    snapshots), damage attribution per source, splitters (208 builds corpus-wide),
    map terrain and ore geometry beyond map identity as a stratum, and the
    `league_games.tsv` / `league_matches.tsv` tables entirely.
11. **`corpus/flow.tsv` was frozen but never read.** It is listed in the
    provenance table for reproducibility; no number in this document comes from
    it.
