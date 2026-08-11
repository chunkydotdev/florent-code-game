# PREREG — LOKI-16b: RING RETENTION, ON THE BAR NAMED IN ADVANCE

**PROVENANCE: a prior leg (LOKI-16) + a corpus cut.** Nothing in
`docs/research/tactics/` spoke to this plank.

**TARGET BAND: gaps −41..+20, a 5-0 pays 14.11..16.92, reachable 4/4** — the
four PANEL-3 admitted cells (Askar City, Lunds Stallions, farming_200s, Powered
by SmartFridge).

**Committed BEFORE the first challenge.** Treatment `bots/_v133loki16` = v106,
UNCHANGED from the LOKI-16 leg. **The bot does not change; the BAR does, and it
was named before LOKI-16 was read out.**

## What LOKI-16 settled and what it did not

**Mechanism demonstrated:** long-hold episodes roughly double — **≥50 rounds:
11.8% treatment vs 5.6% control**, carrying 85.8% of treatment seat-rounds; on
fjordgate we hold **longer (+0.182)** with **fewer** body-rounds (−0.216
seat-rounds/round), the pin-one-raider signature.

**What killed it was the BAR, not the plank.** Coverage read **+0.086** against
a **≥+0.08** bar with a bootstrap CI of **[−0.038, +0.196]**, and **four
defensible estimators straddled the threshold inside 0.010**. I refused to
rescue it by swapping to the better statistic after seeing the data, and
pre-registered that statistic for this leg instead. **This is that leg.**

## PRIMARY BAR — named with its estimator and its clustering unit (D33)

**LONGEST-HOLD / GAME-LENGTH**, i.e. the longest single unbroken occupancy of an
enemy-ring tile divided by the game's round count.

* **Estimator: GAME-MEAN.** Named here, before data. No other estimator may be
  substituted at read-out.
* **Clustering unit: MATCH** (5 games share an opponent and a scheduling
  instant). Bootstrap resampled by match, 4,000 draws.
* **BAR: ≥ +0.15 on the 12-ring stratum.** LOKI-16 measured +0.182 / +0.184 /
  +0.264 / +0.263 on the four 12-ring maps. **+0.15 sits below the smallest of
  those and above zero by a margin the CI can carry** — it is deliberately not
  set at the observed mean, because a bar set at the point estimate is a coin
  flip by construction.

## ⛔ MAP STRATUM IS MANDATORY (D34), NOT AN ANALYSIS CHOICE

`tools/map_admits.py`: **fjordgate/atoll/saga/snowflake = 12-tile ring;
`jackpot` = 5.** The plank's geometry does not exist on jackpot, where LOKI-16
read **−0.023** while the four 12-ring maps read +0.18..+0.26.

**The bar is on the 12-RING STRATUM ONLY. Pooling across strata is forbidden by
this pre-registration.** `jackpot` is still PLAYED and reported — dropping it
would be fitting the panel to the plank — but its games do not enter the primary.

## CONTROL, and its disclosed defect

**Control = PANEL-3's v104 games on the same four cells, same five maps**
(185 games, 15:43–18:21Z). Reusing it costs no rate-limited games.

**⚠ DISCLOSED BEFORE FIRING:** `tools/oppver_window.py` shows **Askar City
shipped v87→v90 at 18:12Z and Lunds Stallions v62→v63 at 16:52Z, INSIDE the
control window.** So for those two cells the control pools two opponent builds.
**Consequence, pre-committed: the primary is computed on all four cells, and
ALSO on the two clean cells alone (farming_200s, SmartFridge). If those two
readings disagree in SIGN, the leg is unattributable and says so.**

## Secondary, and what may not be claimed

* **Kill-speed score is reported and is NOT the verdict** —
  `KILL_SPEED_IS_LEG_VERDICT: no`; sd 7.74/game needs ~2,100 games/arm.
* **Win rate is never a verdict.**
* **Cost side, from LOKI-16 and expected to repeat:** enemy-ring tiles holding
  our building at game end **2.64 vs 3.65**. A retention gain that costs more
  than this is not a gain.

## FALSIFIER

**If longest-hold/length clears +0.15 on the 12-ring stratum AND the kill-speed
score does not improve, retention is not converting into kills** — the body is
being held where it does not pay, and the lever is insertion depth, not
retention. That is a different plank and this prereg names it as the fork.

## Cost

**Requires activating v106.** Measured rated cost of a leaked ladder match is
**~−8 Elo** (3 leaks today, −24.67 total). v104 sits at ~1659 with the rollback
line at 1615. **Attended only; roll back and VERIFY before the session closes.**

---

# CLOSING NOTE — WHAT THE LEG BANKED, AND WHY NO VERDICT IS WRITTEN TONIGHT

**The runner completed its own schedule** (8 cycles, exited cleanly, holder
verified `v104` on the platform — not from the runner's log). **Banked: 10
challenges / 50 games**, spread 3·3·2·2 across farming_200s, SmartFridge,
Askar City, Lunds Stallions. Prototype exposure ~10 s per cycle.

**⚠ THIS PRE-REGISTRATION NEVER FIXED AN n, AND THAT IS A DEFECT IN IT.**
It named the bar, the estimator, the clustering unit, the stratum and the
falsifier — and **no sample size**. So there is no pre-committed line to say
whether 50 games is enough, which means **I could argue it either way after
seeing the data, which is exactly what a prereg exists to prevent.**
Recorded as a defect in the document rather than resolved in my favour.

**NO VERDICT IS WRITTEN TONIGHT, for a reason that is not the n:**
**the primary — longest-hold/length, game-mean, match-clustered — requires a
replay decode that does not exist yet.** Retention episodes are not in any
current tool; LOKI-16's figures came from a bespoke pass. **A bar cannot be read
by a decoder nobody has written.**

**DISPOSITION: BANKED AND UNREAD, not abandoned and not null.** The distinction
matters. LOKI-14b was ABANDONED because it was stopped below its own explicit
dose gate and no bar could attach. **This leg ran its schedule to completion;
what is missing is the instrument, not the data.** The 50 games are clean,
holder-verified, and will read exactly as well tomorrow.

**OWED BEFORE ANY READ-OUT, in order:**
1. **The retention decoder** — longest unbroken occupancy of an enemy-ring tile,
   per game, from `replay_archive`. Both `map_admits` (ring geometry) and
   `replay_census.parse_entity` (positions per round) already exist; this is
   assembly.
2. **An n decision made explicitly**, on the record, before the number is read —
   either "50 games is what we have and here is its interval" or "fire more
   first". **Not chosen after seeing the estimate.**
3. **`oppver_window.py` re-run over the treatment window**, since the control's
   Askar and Lunds cells already straddled a version boundary.

---

# MEASUREMENT — NOT A VERDICT. The decoder now exists; the n decision does not.

**`tools/ring_retention.py` built and selftested** (12 on open terrain, 5 in a
corner, walls reduce it). It decodes the pre-registered primary directly:
longest unbroken run of rounds with one of our builders on an enemy-ring tile,
over game length, game-mean, 12-ring stratum.

| arm | 12-ring stratum | clipped (jackpot) |
|---|---|---|
| **LOKI-16b (v106)** | **0.782** (n=40 games) | 0.598 (n=10) |
| **control v104 (PANEL-3)** | **0.765** (n=148 games) | 0.647 (n=37) |
| **difference** | **+0.017** | −0.049 |

## ⛔ NO VERDICT IS DECLARED, AND THE REASON IS PROCEDURAL, NOT THE NUMBER

**This prereg fixed no n.** By the time the control was read I had already seen
the treatment arm, **so any sample-size rule chosen from here is chosen with
partial data in hand.** That position was written down BEFORE the control was
run, not after — the sequence is in the session transcript and in this file's
ordering.

**So this is recorded as a MEASUREMENT.** Against a bar of **≥ +0.15**, the
observed difference is **+0.017** — an order of magnitude short — but *"the
plank missed"* is a verdict, and the discipline that makes a verdict worth
anything is exactly the discipline that says I cannot write one here.

**What a successor needs to close it:**
1. **A pre-committed n and interval**, decided by someone who has not seen these
   arms, or a bootstrap CI computed under a rule fixed in advance.
2. **Match-clustered resampling** — the prereg names MATCH as the clustering
   unit and these are game-means; 40 games are 10 matches.
3. **`oppver_window.py` on the treatment window**, since the control's Askar and
   Lunds cells already straddled version boundaries.

## AND THE HONEST READ OF WHAT +0.017 PROBABLY MEANS

**Both arms sit at ~0.77-0.78, i.e. a body is on the enemy ring for roughly
three quarters of the game in BOTH.** That is consistent with D30's finding that
ring presence is **already implemented in the incumbent** — the margin LOKI-16
was built to attack was RETENTION, and on this decoder the incumbent already
retains about as well as the treatment.

**If that survives a proper reading, the plank's mechanism is not absent — it is
already ours**, which is the cheapest possible null and the third time today a
plank has died to *"grep the incumbent first"*.

---

# ⛔ THE +0.017 IS WITHDRAWN. THE DECODER DOES NOT REPRODUCE LOKI-16.

Side-lane flag, and it is the fourth time today the same check has mattered:
**a new decoder's first output must never be trusted against a number produced
by a different decoder.** LOKI-16's +0.18–0.26 came from a bespoke pass;
`ring_retention.py` was built tonight. So the positive-control test is: **run
the new tool over LOKI-16's ORIGINAL games and see whether it reproduces them.**

| map | LOKI-16 reported | `ring_retention.py` on the SAME games |
|---|---:|---:|
| fjordgate | **+0.182** | **−0.201** ⟵ **SIGN FLIP** |
| atoll | +0.184 | +0.112 |
| saga | +0.264 | +0.052 |
| snowflake | +0.263 | −0.017 |
| jackpot | −0.023 | −0.064 |

*(treatment `arm_loki16` 75 games vs control `arm_v104` 165 games, the same two
arms LOKI-16 was read on.)*

**IT DOES NOT REPRODUCE. Not one map lands near its reported value, and
fjordgate — the map whose "+0.182 with FEWER bodies" was quoted as the
pin-one-raider signature — comes out NEGATIVE.**

## Consequences

1. **`+0.017` says nothing about the plank and is withdrawn as evidence.** The
   two arms were decoded by an instrument that cannot reproduce the measurement
   it was built to extend.
2. **LOKI-16's own +0.18–0.26 is now equally unsupported** — one of the two
   decoders is wrong and nothing here says which. The bespoke pass is not in the
   tree and cannot be re-run; `ring_retention.py` is selftested on geometry
   (12 open / 5 corner / walls reduce) but that tests the RING, not the
   OCCUPANCY rule.
3. **The likely divergence is the definition, not a bug.** "Longest unbroken run
   with ANY of our builders on a ring tile" (mine) and "longest episode for ONE
   body" (plausibly the original) are different statistics that share a name —
   **exactly the `undamaged` failure, where the census doc and
   `crash_census.py` differed by 3.8% under one word.**

## What this leaves

**LOKI-16b remains BANKED AND UNREAD, and now so is LOKI-16.** The 50 + 75
games are clean and holder-verified. **What does not exist is an agreed
definition of the primary** — and that is a smaller, sharper problem than
either leg: write the occupancy rule down, implement it once, and both legs
read out against it.

**FOURTH INSTRUMENT INVERSION TODAY** (sentinel shootable 52.1% → 0/319 → 100%;
`undamaged` 2,401 vs 2,310; the `CORE_PAIRS`/CLI symmetry claim; now this).
**Every one was the instrument, never the bot. The only thing that has reliably
caught them is running the new tool against a number the old one produced.**

---

# AMENDMENT 2 — THE TWO DECISIONS THIS DOCUMENT SAID MUST BE MADE BEFORE THE NUMBER IS READ

**Written 2026-08-11 06:2x CEST by the s29 BUILDER (`date`, same shell call).
ADD-only. Committed BEFORE any corrected retention figure for either arm has
been computed or seen.** The prereg's own "What is needed" list asks for exactly
these two and records that neither was made. They are made here.

## 2a. THE STATISTIC IS `hold_pinned`, AND THE BAR'S PROVENANCE DECIDES IT — NOT THE PROSE

The research arm's adjudication (2026-08-11, seven forced-answer cells)
establishes that **"longest hold" names two legitimately different statistics**:

* **`hold_any`** — longest run of rounds with **≥1 of our builders on ≥1 ring tile**
* **`hold_pinned`** — longest run of **the same builder on the same tile**

Its relay cell forces **1.000** and **0.500** respectively and **neither decoder
is wrong there.** This is an ambiguity, not a defect — and this document
predicted it in its own limitations section: *"'longest unbroken run with ANY of
our builders on a ring tile' and 'longest episode for ONE body' are different
statistics that share a name — exactly the `undamaged` failure."*

**THE PROSE IS GENUINELY AMBIGUOUS AND I AM NOT RESOLVING IT ON THE PROSE.**
The PRIMARY BAR section says *"the longest single unbroken occupancy of **an**
enemy-ring tile"* (singular tile, unspecified body); the MEASUREMENT section says
*"one of our builders on an enemy-ring tile"* (any body). **Those point different
ways and both are in this file.**

**WHAT DECIDES IT IS WHERE THE NUMBER `+0.15` CAME FROM.** This document sets the
bar as *"≥ +0.15 ... LOKI-16 measured +0.182 / +0.184 / +0.264 / +0.263 ... +0.15
sits below the smallest of those."* **The bar was CALIBRATED on LOKI-16's four
map figures, and research establishes those figures are `hold_pinned`.**

⇒ **A bar derived from `hold_pinned` values, applied to a `hold_any` read-out, is
a threshold in one unit tested against a quantity in another.** That is the exact
error class this repo has now logged four times in one day (52.1% at 45° vs
exact-ray; two definitions of `undamaged` 3.8% apart; the sentinel metric
inverted three times; this). **The statistic is `hold_pinned` because the bar is
only meaningful against the thing that produced it.**

**`hold_any` MAY STILL BE REPORTED** — it is a real quantity and the prose
arguably asks for it — **but it carries NO BAR and the words "clears", "meets"
and "fails" are FORBIDDEN next to it.**

## 2b. THE DECODER IS `ring_read.py`. `ring_retention.py` IS RETIRED FOR THIS PURPOSE.

Research's adjudication, on synthetic replays written as real engine protobuf
with both decoders imported unmodified: `tools/ring_retention.py:128` applies
**no entity-kind filter**, so **every BUILDING of ours on an enemy-ring tile
counts as ring occupancy, permanently, until destroyed.** Measured over 65 games,
our entity-rounds on the enemy ring: **barrier 48.8% · builder_bot 33.6% ·
conveyor 17.5% · sentinel 0.2% — 66.4% of what it calls "a body" is not a body.**

**It does not merely add an offset, it flips the sign**, because the control lays
**more** ring buildings than the treatment on all four 12-ring maps, so the
contaminant enters opposite to the signal. Decomposed on fjordgate: **−0.201 →
+0.174** on the kind filter alone (+0.375 of a 0.383 gap).

**Forced-answer cell that settles it: a BARRIER on the ring with zero
builder-rounds must read 0.000. `ring_retention` reads 0.900. `ring_read` reads
0.000.** Floor and ceiling both covered, seven cells.

⇒ **The withdrawn `+0.017` (treatment 0.782 / control 0.765) is VOID — it was
`ring_retention` output and 66% of it was buildings. It is not a prior, not a
weak signal, and must not be cited as either.**

**⚠ I AM NOT FULLY BLIND AND I AM SAYING SO RATHER THAN CLAIMING I AM.** I have
seen that void figure, and I have seen research's decomposition showing the
kind-filtered fjordgate figure for **LOKI-16's** games is ≈ +0.174. **I have NOT
seen any corrected figure for LOKI-16b's own 50 games in either arm.** The
partial information runs in the plank's favour, which is the direction that
should make a reader more suspicious of a positive read-out, not less.

## 2c. THE n DECISION: **READ THE 50. DO NOT FIRE MORE FIRST. AND IT IS UNDERPOWERED.**

Made explicitly, on the record, before the estimate exists — which is what this
document asked for and did not get the first time.

**The decision is to read what we have**, because the treatment arm is **~40
games on the 12-ring stratum = ~8 matches**, and the pre-registered clustering
unit is the **MATCH**. **A match-clustered bootstrap on n≈8 cannot resolve a
±0.15 bar**, and firing more would mean activating v106 and paying rated exposure
for a plank whose decoder was only agreed twenty minutes ago. **The cheap,
correct order is: read it, see whether the mechanism moved at all, and let THAT
decide whether a powered confirmation leg is worth the exposure.**

**PRE-COMMITTED READ-OUT LANGUAGE, so the n decision cannot be laundered at
write-up.** This is the LOKI-14b Amendment 7 shape and the LOKI-17 Amendment 1c
shape, applied to power rather than to a threshold:

| what the 12-ring `hold_pinned` read shows | how it MUST be written |
|---|---|
| point ≥ +0.15 **and** bootstrap CI lower bound > 0 | **"clears the pre-registered bar at n≈8 matches; underpowered, and a confirmation leg is now WORTH the exposure."** The word **"confirmed" is FORBIDDEN.** |
| point ≥ +0.15, CI straddles 0 | **"the expected outcome at this n. Consistent with the bar, resolves nothing."** The words **"null", "refuted", "fails" are FORBIDDEN.** |
| point in (0, +0.15) | improved, below bar — a partial result, stated as one. |
| point ≤ 0 | **the mechanism did not move in the direction predicted.** This IS informative at any n and may be written plainly. |

**AND THE ASYMMETRY IS DELIBERATE:** a negative is readable at n≈8 because the
prediction was a *doubling*; a positive is not, because the CI cannot exclude
zero. **A leg can be underpowered for confirming and adequately powered for
killing, and pretending otherwise in either direction is the failure.**

## 2d. WHAT THIS AMENDMENT MAY NOT DO

It may not move the +0.15 bar, the game-mean estimator, the match clustering
unit, or the 12-ring stratum — all four predate the data and stay. It may not
pool `jackpot` into the primary. **And it may not be read as reviving the
withdrawn +0.017 under a new name.**

---

# READ-OUT — LOKI-16b CLEARS ITS PRE-REGISTERED BAR. WRITTEN IN THE LANGUAGE AMENDMENT 2c COMMITTED TO, BEFORE THE NUMBER EXISTED.

**Builder verdict, s29, 2026-08-11 06:3x CEST (`date`, same shell call).**

## THE NUMBER

Pooled **12-ring stratum**, game-mean, match-clustered bootstrap, 4,000 draws,
control restricted to the four pre-registered cells:

| statistic | LOKI-16b (10m vs 25m) | LOKI-16 (15m vs 33m) |
|---|---|---|
| **per-(bot,tile) = `hold_pinned` — THE PRE-REGISTERED PRIMARY** | **+0.164 [+0.073, +0.253]** | +0.223 [+0.088, +0.346] |
| any-builder = `hold_any` (no bar, Amendment 2a) | +0.137 [+0.045, +0.226] | +0.184 [+0.050, +0.308] |
| `ring_retention.py` as written (retired, Amendment 2b) | +0.023 [−0.051, +0.104] | −0.013 [−0.152, +0.107] |

**Point estimate +0.164 ≥ the +0.15 bar, bootstrap CI lower bound +0.073 > 0.
That is ROW 1 of the Amendment 2c table, and its language is mandatory:**

> **CLEARS THE PRE-REGISTERED BAR AT n≈8 MATCHES; UNDERPOWERED, AND A
> CONFIRMATION LEG IS NOW WORTH THE EXPOSURE.**

**The word "confirmed" is forbidden here by 2c and is not used.** This is one
leg, ~8 treatment match-clusters, and a margin of 0.014 over the bar.

## THE CALIBRATION CHECK RAN BEFORE THE READ-OUT AND PASSED — and the flag that demanded it was itself withdrawn

The side lane flagged that the +0.15 bar was sized on figures from the decoder
Amendment 2b retires, and pre-committed three outcomes. **Outcome 1 fires:** the
four 12-ring maps under the blessed decoder reproduce **to the third decimal** —
`atoll +0.184 · fjordgate +0.182 · saga +0.264 · snowflake +0.263` (jackpot
−0.023, excluded by the stratum rule). **All four > +0.15. Calibration survives.**

**And the flag dissolved on its own author's re-check:** the apparent
+0.182 → +0.174 drift was **two granularities of the same decoder**
(per-(bot,tile) vs any-builder), not two decoders. **The original four were
`ring_read` per-tile all along; nothing moved and no margin shrank.**

## ⭐ THE STATISTIC CHOICE WAS THE DECIDING CALL, AND IT WAS MADE BLIND

**per-tile +0.164 CLEARS · any-builder +0.137 MISSES.** The two differ by 0.027
across a bar sitting between them. **Amendment 2a chose `hold_pinned` on the
BAR'S PROVENANCE — because +0.15 was calibrated on LOKI-16's figures and those
are per-tile — and it was committed at `3b56e9b` 06:15:21, before this number
existed.** The blind replication that produced it launched at `14d7720`
06:08:52 and was never briefed with the adjudication or the amendment.
**Two clocks, verified by the builder against `git log`, not accepted on report.**

**Had 2a gone the other way this leg would read as a miss.** That is the whole
case for choosing an estimator on provenance before the data rather than on
prose after it, and it is worth more than this leg's result.

## WHAT QUALIFIES IT — stated here, not in a footnote

1. **The effect is concentrated in the clean cells: +0.245 clean
   (farming_200s, SmartFridge) vs +0.056 dirty (Askar City, Lunds Stallions,
   both of which shipped a new opponent version inside the control window) — a
   4.4x magnitude difference.** The pre-registered gate was **SIGN**, and both
   agree in sign, **so the gate passes as written.** But the disclosed version
   confound predicted exactly this shape and it is not priced.
2. **No equal-cell reweighting.** The prereg names game-mean, so unweighted is
   correct as pre-registered; the arms do not share a panel mix and that
   difference is unpriced.
3. **`ring_read.py` has never seen a game with a wall inside the enemy ring**
   (0/240 in this corpus), so its missing wall filter is untested rather than
   clean.
4. **The kill-speed / core-kill currency is NOT read here.** Under
   `KILL_SPEED_IS_LEG_VERDICT: no` this is a mechanism result only. **The
   prereg's own fork stands unresolved: if retention clears and kill-speed does
   not improve, retention is not converting into kills.** That is the next
   question and this leg does not answer it.
5. **Amendment 2c's Flag-2 question — `P(point ≤ 0 | true = +0.15, 8 clusters)`
   — is MOOT FOR THIS READ-OUT and remains open for any future one.** It governs
   the KILL band only, and the kill band did not fire. **It must be computed
   before that row is ever used.**

## AND THE WITHDRAWN +0.017 IS VOID FOR A SECOND, INDEPENDENT REASON

Amendment 2b voided it on entity kinds (66.4% of its "bodies" were buildings).
The replication adds a second: **its control pooled 0033 and The Bisons, two
opponents not in the treatment arm at all** (148 games; restricting to the four
pre-registered cells gives 100). **Two independent defects in one figure.**

## AN INSTRUMENT FINDING THAT OUTLIVES THIS LEG

**`ring_retention.py --selftest` PASSES and is worthless.** It exercises
12-on-open / 5-in-corner / walls-reduce — **the RING GEOMETRY** — and never
touches the **occupancy rule**, which is the thing that was wrong. **A green
selftest that tests the geometry of a metric while leaving its definition
untested.** That signature is worth hunting elsewhere in `tools/`: the
decomposition shows the entity-kind filter alone accounts for **+0.375 of a
0.383 gap, and it flips the sign** — because v104 forward-barriers the enemy
ring harder than v106, so the contaminant enters opposite to the signal.

**And the knockdown argument came from inside this prereg:** it lists
*"enemy-ring tiles holding our building at game end, 2.64 vs 3.65"* as the
**COST SIDE**. **A quantity pre-registered as the COST cannot simultaneously be
the PRIMARY** — `ring_retention`'s number was 97.9% that cost metric wearing the
primary's name with the sign reversed.


---

# CORRECTION 1 — A SECONDARY ROW IN THE READ-OUT IS MISLABELLED. THE PRIMARY AND THE VERDICT ARE UNAFFECTED.

**2026-08-11 07:2x CEST.** Found by building `tools/ring_read.py --selftest`,
which forced the question the prose never had to answer. **Verified in the code
by the builder before correcting.**

## THE ERROR
The read-out table's second row reads **`any-builder = hold_any … +0.137`**.
**`ring_read.py` computes no `hold_any` statistic at all.** From the code:

```
per_bot_tile[(eid, p)]  -> "tile_episodes"   same bot, SAME tile
per_bot_any[eid]        -> "bot_episodes"    same bot, ANY ring tile
```

**`bot_episodes` is a THIRD quantity**, not the adjudication's `hold_any`
(*"longest run with >=1 of OUR BUILDERS anywhere on the ring"*). **The RELAY
forced-answer cell proves the difference: with bot A on tile T for rounds 0-49
and bot B on the SAME tile for 50-99, true `hold_any` is 100 and `bot_episodes`
maxes at 50.** No series in `decode()` returns 100 there.

=> **The `+0.137` is real and is "longest run of the SAME BOT on the ring";
it is NOT `hold_any` and must not be quoted as one.** Anything quoting
`hold_any` off this tool today is quoting the wrong series.

## WHAT THIS DOES NOT TOUCH — AND THE REASON IS STRUCTURAL, NOT LUCKY
* **The PRIMARY is `tile_episodes` = `hold_pinned` = `+0.164 [+0.073, +0.253]`.
  Correct as published.** Amendment 2a selected it on the **bar's provenance**
  (the +0.15 bar was calibrated on LOKI-16's per-tile figures), and that argument
  never referred to the mislabelled series.
* **The verdict is unchanged**: clears the bar at n~8 match-clusters,
  underpowered, "confirmed" still forbidden.
* **Amendment 2a's "hold_any MAY be reported but carries NO BAR" clause did its
  job** — the mislabelled number was already barred from bearing weight. **A
  guard written for a different reason contained this error's blast radius.**

## THE GENERAL POINT, WHICH IS WHY THIS IS WRITTEN DOWN
**Three lanes discussed `hold_any` vs `hold_pinned` for hours and agreed a
definition. Nobody checked that the tool implemented EITHER of them under those
names.** The adjudication named two statistics; the code has two series; the
names were matched **by position rather than by semantics**. It took a
forced-answer cell — the RELAY, whose entire purpose is separating the two — and
**it was exposed the moment that cell existed.** Seventh units-not-data incident
of 2026-08-11 and **the first one caught by an instrument rather than by a
person.**
