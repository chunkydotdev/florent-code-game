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
