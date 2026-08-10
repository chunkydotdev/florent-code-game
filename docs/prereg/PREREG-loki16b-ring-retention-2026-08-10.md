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
