# ⭐ QUEUE FOR THE BUILDER — FORWARD EFFICIENCY: WE PAY 4.57× AS MANY BUILDERS PER FORWARD BUILD

**Research arm, s30, 2026-08-11. Two independent instruments, both reported.
Population: our 5,143 games vs 3,080 THIRD-PARTY games of nine ≥1900 teams
(sporks, Clankers, Jython, Lorem Ipsum, not adgato, Erebus, The Flotte
Experience, Pantheon, O(1)) — games we are not in, so not an echo loop.**

## THE HEADLINE

**Instrument A — `corpus/events.tsv`, one table, same method both sides:**

| | games | forward deaths/game | forward builds/game | **DEATHS PER FORWARD BUILD** |
|---|---:|---:|---:|---:|
| **US** | 5,143 | **1.79** | **13.91** | **0.1290** |
| **TOP (3rd-party)** | 3,080 | 0.67 | 23.59 | **0.0282** |
| ratio | | 2.69× | 0.59× | **4.57×** |

**Instrument B — direct replay decode, 120 games per group, positions per round:**

| | fwd builder-rounds/game | fwd builds/game | **ROUNDS PER FORWARD BUILD** | fwd share of builder-rounds |
|---|---:|---:|---:|---:|
| **US** | **742.7** | 13.62 | **54.55** | 36.4% |
| **TOP** | 494.9 | 20.68 | **23.93** | 27.2% |
| ratio | 1.50× | 0.66× | **2.28×** | |

**⇒ WE SPEND 50% MORE TIME IN THE ENEMY HALF, PRODUCE 41% FEWER FORWARD BUILDS,
AND LOSE 4.57× AS MANY BUILDERS PER FORWARD BUILD.**

The two instruments agree and **decompose the gap cleanly**, since
`deaths per build = deaths per round × rounds per build`:

* **~2.28× is DWELL** — our raiders stand forward far longer per thing built.
* **~2.0× is PER-ROUND HAZARD** — measured separately at 2.915 vs 0.847 deaths
  per 1k forward builder-rounds.

**Roughly half the problem is loitering and half is where we loiter.**

## WHY THIS IS THE RIGHT TARGET AND LOKI-25 WAS NOT

`FORWARD-HAZARD-geometry-2026-08-11.md` measured the ceiling on the routing
half: our builders stand on gunner-covered tiles **2.04% of forward builder-rounds
against a 1.34% map baseline — 1.53× chance**, so **perfect tile selection cuts
exposure by at most 34%.**

**The dwell half is 2.28× and has no such ceiling.** It is the larger lever and it
is the one nothing has been aimed at.

## ⛔ POWER AUDIT — AMENDED 2026-08-11, AFTER THE BAR BELOW FAILED ITS OWN CHECK

**The bar specified below said "deaths per forward build, a RATIO" and did NOT
name the aggregation. Measured, 4,831 of our games:**

| estimator | value | MDE at n=64/arm |
|---|---:|---:|
| **mean of per-game ratios** (what I originally implied) | 0.1541, sd 0.4007, **CV 2.60** | **129% of level** |
| **pooled ratio** (total deaths ÷ total builds), game-resampled bootstrap | 0.1281, SE 0.0330 | **102% of level** |

**Both are useless at n=64. The one I implied is the worse of the two.** This is
the defect this repo logged when four defensible estimators straddled the
ring-hold threshold inside 0.010 — **a bar names its estimator or it can be met
and missed by choosing one afterwards.**

**The obvious rescue does not work either.** Self-play looks like a free paired
design (same map, same seed, both arms in one game). **Measured within-game
correlation between the two sides' deaths-per-forward-build: r = +0.027 —
variance reduction 3%.** Reported because it is the design I would otherwise have
prescribed.

### ⇒ THE FIX: POOLED RATIO, GAME-RESAMPLED BOOTSTRAP, **n ≈ 440 PER ARM**

Detecting a move that closes **half** the top-tier gap (a 39% reduction) needs
SE ≈ 0.0126 → **~440 games/arm, 880 total.** **A 4,096-game self-play screen has
already been run today, so 880 costs zero unrated windows.** The protected floor
rides along in the same run.

**⚠ And one correction to a rule in circulation:** *"mechanism bars are ~160×
cheaper"* is true of LOKI-25 (huge effect, low-variance statistic) and **NOT of
this plank** — here the mechanism bar needs 880 games and the win rate at 880
detects 4.7pp. **Comparable, not 160× apart. The principle is right; the multiple
is a property of that plank.**

## ⛔ THE BAR MUST BE A RATIO, AND THIS IS THE DESIGN CONTRIBUTION

**LOKI-25 died because it moved a numerator and a denominator together**: deaths
−24%, forward presence −23%, deaths per forward build −2.3%. **Any plank in this
family can buy its metric by simply going forward less.**

⇒ **PRIMARY BAR: `deaths per forward build`, a RATIO.**
⇒ **PROTECTED DENOMINATOR: `forward builds/game` must NOT fall** — pre-register a
floor (our current 13.91) and treat a breach as the falsifier, exactly as LOKI-25's
5d was written and then fired.

**Both quantities are already in `events.tsv`, so the read-out needs no new
decoder and the builder's 64-game self-play harness can compute both.**

## WHERE TO LOOK IN THE TREE — NAMED, NOT PRESCRIBED

The dwell constants a raider is governed by: `raid.py:232-234`
(`raid_pause_until = rnd + 60`; **both `3` and `60` are bare literals with no
doctrine constant** — found by the a–f library agent), `ESCORT_STALL_RNDS = 25`
(`doctrine.py:158`), `LAUNCH_STALL_RNDS = 36` (`doctrine.py:108`),
`LAUNCH_GIVEUP_RND = 180` (`doctrine.py:103`).

**I am naming the constants and NOT the intervention.** I do not know whether the
fix is a shorter pause, an earlier rotate-out, or acting-then-leaving — and
guessing the intervention is the error I made twice today on healer eviction.

## PRECONDITION: MEASURED, AND THE DOSE IS THE WHOLE BEHAVIOUR

742.7 forward builder-rounds per game across 5,143 games. **There is no
"does the treatment ever fire" risk** — this is what our raiders do all game.

## ⚠ WHAT THIS IS NOT

* **Not a causal claim.** Top teams may produce forward builds faster *because*
  they are better, not the reverse. **Cross-sectional, behavioural premise ⇒ under
  D12 this PRIORITISES a road and does not retire or confirm one.**
* **The TOP group is nine teams**, chosen by rating ≥1900 before the cut was run.
* **"Forward build" counts every non-builder-bot build with `d2_enemy < d2_own`**,
  so it mixes turrets with conveyors — the same definitional caveat LOKI-25's
  read-out carried.
* Instrument B samples one game per match; Instrument A uses all games.
