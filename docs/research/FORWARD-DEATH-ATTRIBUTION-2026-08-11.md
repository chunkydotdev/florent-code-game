# ⭐ THE FORWARD-HAZARD GAP, FULLY ATTRIBUTED — AND THE "UNEXPLAINED 2.3×" WAS MY ARITHMETIC ERROR

**Research arm, s31, 2026-08-11.** 13,771 replays, **0 parse failures, 0 skipped.**
Script `scratchpad/fwd_death_attrib_s31.py`; output `scratchpad/_fwd_attrib_full.txt`;
41,385 death rows in `scratchpad/fwd_death_rows_s31.tsv`.

**ANCHOR REPRODUCED (stop-condition cleared):** US **2.90** vs published 2.92,
TOP **0.87** vs 0.84, ratio **3.36×** vs 3.47×. Numerator and denominator over the
same side-set (US 5,243 sides; TOP 4,345 sides from 3,285 games, the 1,060
TOP-vs-TOP games contributing two each).

## ⛔ 1. THE CORRECTION, AND IT IS MINE

I published — in `QUEUE.md`, in the queue doc, and in a message to both lanes —
that *"tile exposure explains at most 1.53× of a 3.47× gap, so ~2.3× is
unaccounted."* **That is wrong. The terms MULTIPLY; I treated them as adding.**

| term | ratio | log-share |
|---|---:|---:|
| **A** enemy turrets EXIST, per forward builder-round | **1.77×** | **47.3%** |
| **B** share of them IN RANGE of our tile | 1.57× | 37.0% |
| **C** damage per turret-in-range-round | 1.05× | 4.3% |
| **D** damage absorbed per death | 1.15× | 11.4% |
| **PRODUCT** | **3.36×** | = the anchor |

**There was never a residual.** `B = 1.57×` **independently reproduces
`FORWARD-HAZARD`'s ray-based 1.53× on a different instrument** (range only,
facing and LOS ignored) — corroboration, not identity. The "2.3×" was `A×C×D`.

## 2. THE WHOLE GAP IS ONE QUANTITY

**We take 2.92× the damage per forward builder-round** — 143.50 vs 49.09 per 1k —
and it is **2.4–4.0× in every band**. Nothing else moves.

## ⭐ 3. `A` IS OUR FORWARD *TIMING*, NOT THE OPPONENT'S BUILD

| group | sides | deaths/1k fwd-rnds | enemy turrets alive | in range | dmg/1k |
|---|---:|---:|---:|---:|---:|
| US | 5,243 | 2.90 | 3.76 | 1.186 | 143.50 |
| **US_vTOP** | 115 | **1.54** | **3.94** | 0.908 | 77.53 |
| TOP | 4,345 | 0.87 | 2.12 | 0.427 | 49.09 |
| **TOP_vTOP** | 2,120 | **0.52** | **2.19** | 0.379 | 29.06 |
| TOP_vOTH | 2,225 | 1.23 | 2.06 | 0.477 | 70.01 |

**Against the same class of opponent, 3.94 turrets are alive per our forward round
against 2.19 per theirs. Opponent-matched the gap is 1.54/0.52 = 2.96× —
opponent selection accounts for only ~10% of the log gap.**

*(INFERENCE)* The alive-ratio runs **1.14× at r0-59 → 2.25× at r500-999**, and
**30.5% of our forward rounds sit in r500-999 against TOP's 16.8%.** **We hold
forward posture late, into a turret field that has matured.**

## ⭐ 4. TRANSIT vs STATION — THE ANSWER IS **NEITHER**

Hazard by rounds-since-last-move is **non-monotone, and the same shape for both
groups**:

| state | % of US fwd rounds | % of US fwd deaths | deaths/1k | vs mean |
|---|---:|---:|---:|---:|
| moved last round | 49.63% | 44.62% | 2.61 | **0.90×** |
| 2 rounds ago | 3.78% | 9.74% | 7.48 | 2.58× |
| **3–9** | **7.70%** | **30.84%** | **11.63** | **4.00×** |
| 10–29 | 6.79% | 8.76% | 3.74 | 1.29× |
| 30+ | 32.10% | 6.05% | 0.55 | **0.19×** |

**They die 2–9 rounds AFTER they stop moving — 40.6% of forward deaths in 11.5% of
forward rounds, at 4× mean hazard. Moving is BELOW-average hazard. Parked 30+
rounds is the safest state in the game.**

⇒ **LAUNCHER DELIVERY'S PREMISE IS NOT SUPPORTED.** It removes the traverse —
44.6% of deaths, in the *least* hazardous state — and **drops the bot straight
into the peak-hazard window.** Ceiling ~45% of forward deaths, **no hazard-per-round
discount** (US/TOP is **4.06× within transit** and **5.2–5.9× within the stopped
states**). The saving is purely *"fewer forward rounds per build"* — LOKI-25's
lever, pulled without also cutting builds. **Honest, small, and not the 2.3×.**

**And the mix runs the wrong way as an explanation:** our movement-state mix is
**favourable** (32.1% parked 30+ vs TOP's 12.3%). **Standardised to TOP's mix our
rate RISES 2.90 → 4.11 and the gap WIDENS to 4.74×.**

## 5. TWO STORIES KILLED OUTRIGHT

* **"We fail to disengage or heal" is DEAD.** Moved-after-first-damage **76.74% vs
  76.81%**; ever-healed 14.34% vs 13.96%; episode first-damage→death 12 vs 11
  rounds. *(The ambush-vs-linger framing was unanswerable as posed — 40 HP against
  7/18 damage means no builder can die from full in one round.)*
* **Depth runs AGAINST the story.** We stand 9% deeper (0.316 vs 0.345
  exposure-weighted) but **die shallower** (median 0.300 vs 0.263).
* **We do not crash: 0.00% no-damage removals for US, 1.02% for TOP.**

## 6. CONTROLS

* **Attribution completeness: US 99.47% EXACT / 0.53% over / 0.00% unattributed.**
  Nothing hides in a residual.
* **Must-come-out-otherwise:** HOME deaths differ from forward (US 83.28% vs
  87.51% gunner-only), and the `VSUS` group recovers our own fingerprint
  unprompted — **64.29% sentinel-only: we kill with sentinels, they kill us with
  gunners.** `TOP` (games we are not in) and `VSUS` (our opponents in our games)
  are labelled on every line and **never pooled** — the s30 `FIELD_vsUS` trap.
* **Exposure moved onto a ROUND-START clock.** On `dwell.py`'s post-move clock a
  continuously-moving bot shot before its own move counts TRANSIT in the
  denominator and STATION in the numerator. **That fix alone manufactures or
  destroys the entire §4 result** and costs 0.02 on the anchor.

## 7. CAVEATS THE ANALYSIS RAISED AGAINST ITSELF

* **`B` ignores facing and line-of-sight**, so it is a range proxy; agreeing with
  the ray-based 1.53× to 0.04 is corroboration, not identity.
* *(INFERENCE)* **"Moved last round" is partly a RESPONSE to danger** — fleeing
  resets the clock — which blurs the transit/station boundary in both directions.
  **The bucket shape is robust; the causal reading of it is not.**
