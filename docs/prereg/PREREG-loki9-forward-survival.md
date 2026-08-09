# PREREG — LOKI-9, forward ordnance survival

**Committed BEFORE leg creation** (two-clock standard: this file's git author
time must predate the platform `createdAt` of every leg it governs).
Line `loki`. Comparator **LOKI-8 = `bots/_v124loki8`** — the previous line
iteration, per `PROGRAMME.md: COMPARE_AGAINST`, **not** the frozen incumbent.

## The claim being tested

We already place a gunner within `d²<=13` of the enemy core in **38% of games**,
and it **dies in a median 18 rounds against the top tier's 62** (57.2% of ours
dead inside 30 rounds, n=1,132, vs 26.3% of theirs, n=2,529). Per-gunner firing
rate is **identical** (63 vs 62 shots) and the deficit is **flat across every
distance band**, so this is not a siting or a geometry defect — the ordnance
arrives and does not persist. The live bot makes **zero** `destroy()` /
`self_destruct()` calls, so those deaths are enemy action.

**LOKI-9 changes ONLY what the forward builder does AFTER a placement we already
make.** It adds no placement policy, no new build decision, and does not touch
the home counterbattery path. This line's measured law is that every gain was a
removal or a repositioning and both added mechanisms failed; a flag flip is
preferred to new code and the exact hunk is committed before the leg.

## Bars, stated before the leg

* **DID-IT-FIRE (mechanism, NOT the verdict):** forward-turret **survival to 30
  rounds**, computed offline from the leg's own replays, per-turret, distance
  held fixed. **The baseline is LOKI-8's survival ON THE CONTROL ARM OF THIS
  LEG, not the 42.8% corpus figure** — that 42.8% (100 − 57.2% dead inside 30,
  n=1,132) is **pooled across our ladder versions v64–v102**, so it is a
  different subject from LOKI-8 and cannot anchor a paired bar. Bar: **LOKI-9's
  survival must exceed LOKI-8's on the same opponents and maps by >=15pp**, with
  both arms' raw counts reported. The corpus 42.8% is context for why the plank
  exists, and is **not** the comparator.
* **VERDICT (the currency, `PROGRAMME.md: PRIMARY_CURRENCY`): `core_kill_share`
  vs LOKI-8**, both arms on the same opponents, same maps, same n. Bar: LOKI-9
  **must not be below** LOKI-8, and to be called a gain must exceed it with the
  paired test reported alongside the interval.
* **SECONDARY:** `time_to_core_kill`, reported, never substituted for the above.

## The falsifier, and the cheap close

**If survival moves and `core_kill_share` does not, that is a LABELLED NULL and
the road closes.** I will write the word "null" and the plank is dead — a
mechanism metric never substitutes for the currency, and an off-prediction win
is labelled rather than banked. **If survival does not move, the leg answered
nothing about the plank** and is a treatment-verification failure, not evidence
against forward survival (this is the D7 shape and it is why the mechanism bar
exists separately).

## Opponent set — saturation is disqualifying

**Excluded as SATURATED:** `clanker` (we win 96.7%) and `ouroboros` (93.3%). A
plank measured only against these has not been measured (D5/D11).
**Included as RESOLVING:** `cad` (66.7%) and `orizon` (50.0%).
Unrated legs only, between ladder games. Seats varied and RECORDED this time —
s25 varied them without controlling them, and `ladder_games.tsv`'s `seat` column
is the WINNER's side, not ours (TRAP 7), so seat comes from the in-replay index.

## Power, stated honestly up front

The comparable LOKI-7 fixture is **saturated at 86.7%**, where 15/15 vs 13/15
gives **p=0.483** and a <=10pp effect needs **~350/arm**. `core_kill_share` is
the currency precisely because win rate cannot resolve on this pool. **If the
leg returns a null at feasible n, that is a null about THIS n, and I will report
the n rather than the direction.**

## What would make me abandon rather than iterate

Survival rises past the bar **and** `core_kill_share` is flat or down across
both resolving opponents. That would say the forward gunner's persistence is not
what converts, and the next lever is conversion, not survival.
