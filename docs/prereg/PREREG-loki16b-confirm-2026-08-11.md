# PREREG — LOKI-16b CONFIRMATION, **PROBE TIER**

**Written 2026-08-11 08:2xZ by the s30 BUILDER. Committed BEFORE leg creation.**
Parent: `docs/prereg/PREREG-loki16b-ring-retention-2026-08-10.md`, which read out
**+0.164 [+0.073, +0.253]** against a **+0.15** bar and whose own Amendment 2c
row 1 says *"clears the pre-registered bar at n≈8 matches; underpowered, and a
confirmation leg is now WORTH the exposure."* **This is that exposure.**

## ⭐ THIS IS A PROBE, NOT A LEG, AND THE TIER IS THE POINT

Adopted today after a day that produced full currency-grade ceremony for every
window and **six unfired free slots**. The repo already draws this line and we
were not using it: *a 25-game window is a DOSE AND MECHANISM probe; a currency
read requires pooling windows.*

**WHAT A PROBE MAY DO:** bank games against a pre-declared statistic and pool.
**WHAT IT MAY NOT DO: make a currency claim, or a verdict, from this window.**
No band language, no ship implication. **If it does not pool, it produced games
and nothing else, and that is an acceptable outcome for a free slot.**

## THE STATISTIC — inherited verbatim, not re-chosen

`hold_pinned` = longest same-bot-same-tile enemy-ring hold / game length,
**game-mean, 12-ring stratum, match-clustered bootstrap 4,000 draws**
(`tools/loki19_5d.py`, which implements exactly this and is selftested to both
verdicts). **No estimator, stratum or clustering unit is re-opened here** — the
parent's Amendment 2a chose `hold_pinned` on provenance before its data existed
and re-choosing now would be the laundering that document exists to prevent.

## ARMS, CELLS, n

* **TREATMENT: v106 "Loki v2 - ring" = LOKI-16b**, already `ready` on the
  platform — **no submit is required, so the auto-activation hazard does not
  arise.**
* **CONTROL: the ~400 banked v104 games**, which the side lane measured
  **still version-stable on 4 of 5 cells at 161 minutes.**
* **CELLS: the parent leg's own four** — `25288fdb`, `b2deaacd`, `eceb8455`,
  `7fd91e77` — for comparability with the +0.164.
  **⚠ `7fd91e77` is Powered by SmartFridge, which has failed SIX independent
  admission checks today** (arrival precondition, version churn, seat inversion,
  supplying the most favourable 5d number, no version-matched control, and being
  the most mid-range cell on the board while running ten versions in a day).
  **It is FIRED but PRE-COMMITTED AS REPORT-SEPARATELY-NEVER-POOLED**, the same
  disposal `f555166` gave Askar City. Dropping it outright would break
  comparability with the parent; pooling it would be the flattering move.
* **n THIS WINDOW: 5 challenges x 5 games = 25.** **Explicitly below resolution.**
  The side lane's sizing: **200 treatment games ≈ 8 windows ≈ 2.7 h resolves
  15pp.** This is window 1 of that, fired because a slot was free NOW.

## WHAT RESOLVES AT n=25 — the table, and it covers the GATES too

*(Standing rule adopted from LOKI-19: a resolution table sizes every GATE, not
only every BAR, and the pre-committed default when a gate does not discriminate
is the RESTRICTION.)*

| item | kind | resolves at 25 games? |
|---|---|---|
| `hold_pinned` vs +0.15 | BAR | **NO. Stated before firing.** Parent needed ~8 matches for a CI half-width of ±0.09; this is 5. **No comparison against +0.15 may be published from this window.** |
| dose (does v106 differ from v104 on ring occupancy at all) | GATE | **YES** — a large occurrence difference is visible at 25 games. If v106 shows no ring-occupancy difference, the leg is VOID and pooling is pointless. |
| 12-ring stratum admission per cell | GATE | **PARTIALLY.** Reported per cell with its n. A cell contributing <3 games in-stratum is reported and not pooled. |
| currency | — | **NOT MEASURED AND NOT CLAIMED.** |

## ⛔ TWO INHERITED HAZARDS, NAMED SO THEY ARE NOT REDISCOVERED

1. **The arms are not balanced on the fixture axes** — seat mix and map mix
   differ between any banked control and a fresh window, and the 12-ring
   exclusion is asymmetric *because of* the map imbalance. **Disclosed, not
   corrected**; a matched estimator chosen now is chosen after the data.
2. **`ring_read`'s two episode series are NOT `hold_any` and `hold_pinned`.**
   `tile_episodes` == `hold_pinned` is the primary; `bot_episodes` is a THIRD
   statistic and must never be quoted under either name.

## OBLIGATION 13 — the D42 check, run BEFORE firing

```
MECHANISM METRIC READS: bots/_v133loki16/eco.py  (ring seat selection)
TREATMENT DIFF TOUCHES: v106 vs v104 — to be confirmed by tools/inert_check.py
INTERSECTION: asserted below, not assumed
```
**If `inert_check` reports INERT, this window is not fired.**

## WHAT THIS PROBE MAY NOT DO

It may not publish a number against +0.15. It may not claim a currency effect.
It may not pool SmartFridge. It may not re-choose the estimator. **And it may not
be described as a confirmation until the pooled n is reached** — one window is
the first payment on that, not the thing itself.

---

# ⛔ AMENDMENT 1 — **I SKIPPED THIS DOCUMENT'S OWN GATE, SIXTY SECONDS AFTER WRITING IT.** POST-HOC, AND LABELLED AS SUCH.

**Written 2026-08-11 08:3xZ, AFTER the window fired.** §Obligation-13 above says,
verbatim: *"If `inert_check` reports INERT, this window is not fired."* **I did
not run it. I committed the prereg at 08:26:25Z and fired at 08:26:44Z — nineteen
seconds later.**

## A1.1 WHAT THE GATE SAYS, RUN LATE

```
INERT_CHECK: MALFORMED
  declared but NOT in the computed diff: "v106 vs v104 — to be confirmed by …"
  in the computed diff but NOT declared: doctrine.py, raid.py
```
**Two defects in my own declaration, neither of them subtle:**
1. `TREATMENT DIFF TOUCHES` was left as **placeholder prose** rather than a path
   list. The tool correctly refuses to compare a sentence to a file set.
2. `MECHANISM METRIC READS: bots/_v133loki16/eco.py` **is wrong.** I took it from
   `ring_read`'s docstring, which cites `eco.py` for the ring GEOMETRY
   (`heal_seats + core_corners`). **But the diff does not touch `eco.py`** — and
   LOKI-16b's own source comment says why, explicitly: *"Set here rather than in
   `main.__init__` so that file stays untouched."*

## A1.2 THE SUBSTANTIVE ANSWER — NOT INERT — AND IT WAS ESTABLISHED AFTER FIRING

The statistic is ring OCCUPANCY, produced by **`_ring_hold` in `raid.py`**, which
is exactly what the diff adds (`raid.py` +90 lines, `doctrine.py` +68).
**`v106 vs v104` touches `raid.py`; the metric reads `raid.py`; the intersection
is non-empty; the bar is NOT inert.** The window is therefore not void and the 25
games are on a live plank.

**⛔ BUT I DETERMINED THE READ PATH BY LOOKING AT THE DIFF, AFTER FIRING. That is
the precise reasoning `inert_check` exists to prevent** — a read path chosen once
the answer is visible is not a pre-registration, and *"it turned out fine"* is
the weakest possible defence. Recorded at full weight rather than corrected
quietly.

## A1.3 ⭐ THE LESSON, AND IT CORRECTS THE TIER IDEA I ADOPTED THIS MORNING

The PROBE tier was introduced hours earlier to cut ceremony after a day of six
unfired slots. **Within ninety seconds of its first use I treated "probe tier" as
licence to skip a GATE.** It is not.

> **THE TIER REDUCES THE WRITE-UP, NOT THE VERIFICATION.**
> A probe may skip bands, amendments, power tables and verdict language.
> **It may not skip a check that decides whether the window can learn anything** —
> those are seconds each, they are the cheap half, and they are the half that
> made this document wrong.

**AND THE SHAPE IS TODAY'S, FOR THE FIFTH TIME: a check I had, did not run, that
would have caught something.** LOKI-18 (`plank_status`, cost 25 games),
`corpus_sanity`'s fifty-hour STALE line, the ammo decoder's proto3 default, the
`meta_join`/`throws` join key, and now this. **Every one was seconds of work
placed after the expensive step instead of before it.**

## A1.4 WHAT THIS AMENDMENT MAY NOT DO

It may not be read as clearing the gate — the gate was **skipped**, and running
it late does not un-skip it. It may not move any bar, cell, statistic or the n.
It may not upgrade this window from PROBE. **And the corrected declaration below
is for the NEXT window, where it will be run BEFORE firing:**

```
MECHANISM METRIC READS: bots/_v133loki16/raid.py:112   (_ring_hold)
TREATMENT DIFF TOUCHES: raid.py, doctrine.py
INTERSECTION: raid.py — YES
```
