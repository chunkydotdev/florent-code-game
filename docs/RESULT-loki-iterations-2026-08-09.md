# RESULT — the Loki line vs Eir on one fixture. Iterations 4 → 7.

All unrated, under Magnus's standing grant. **Identical fixture throughout:**
5 short maps (nordkap, eider, heart, moonrise, meander) × 3 real opponents
(Ouroboros, Orizon, CtrlAltDefeat) = **n=15 per arm**. Loki is NOT on the
ladder and does not go there until Magnus approves it.

## THE TABLE — PRIMARY CURRENCY IS `core_kill_share`

| arm | what changed | record | **core-kill share** |
| --- | --- | --- | --- |
| **v94 Eir** (incumbent) | — | 11-4 | **5/15 = 33.3%** |
| LOKI-4 | rush OFF | 8-7 | 8/15 = 53.3% |
| **LOKI-5 (quiet)** | **all builder melee silenced** | 12-3 | **12/15 = 80.0%** |
| LOKI-6 | 3 arrival defects fixed | 8-7 | 8/15 = 53.3% |
| **LOKI-7** | **LOKI-5 + LOKI-6 composed** | **13-2** | **13/15 = 86.7%** |

**LOKI-7 vs Eir on the primary currency: Fisher two-sided p = 0.0078.**
**Win rate over the same games: 13-2 vs 11-4, p = 0.65 — indistinguishable.**

> **The line now kills 2.6× as many enemy cores as the incumbent, on the same
> maps against the same opponents, without costing win rate.** That is precisely
> what `PROGRAMME.md` asks for, and it is the first time the Loki line has shown
> it against real teams rather than probes.

## WHAT IS *NOT* ESTABLISHED — and these matter

- **LOKI-7 vs LOKI-5 is p = 1.0.** They are indistinguishable. The composition
  may have added nothing; **13/15 vs 12/15 is one game.**
- **LOKI-7 vs LOKI-4 is p = 0.109 — NOT significant.** So no single iteration is
  individually proven against its own predecessor. The significant comparison is
  against **Eir**, which is the incumbent, not the previous line iteration.
- **LOKI-6's three arrival fixes measured exactly NULL** (8/15, identical to
  LOKI-4 on both record and share). I had reported them at "70%" off an
  incomplete fixture; the missing leg came back 1-4 and erased it.
- **n=15 per arm.** Directional. Seats varied per leg (LOKI-7 drew a/a/b,
  LOKI-5 b/a/a, Eir a/a/a, LOKI-4 b/b/b) — better than seat-locked, but luck
  rather than design. Research measured seat effects null league-wide at
  n=2,715, which bounds the confound without removing it.

## GENERALISATION — the effect is WEAKER OFF THE SHORT MAPS

Every number above is short-map only. LOKI-5 re-run on the **long** band (saga,
atoll, lighthouse, drumlin, hive), 2 opponents, n=10:

| | short maps | long maps |
| --- | --- | --- |
| LOKI-5 core-kill share | 80.0% (12/15) | **60.0% (6/10)** |

**Still well above Eir's 33.3% — but Eir's 33.3% was measured on short maps
only, so that is not a fair comparison and I am not making it.** The Eir
long-map baseline is the next measurement and it is cheap.

## THE MECHANISM, STATED AS A HYPOTHESIS

**Every winning change in this line has been a REMOVAL, not an addition.**
Rush off (LOKI-4), melee off (LOKI-5). The one iteration that tried to ADD a
mechanism — LOKI-3, the kidnap plank — failed its own treatment bar and was
held, because it duplicated something we already had cheaper in barriers.

The candidate mechanism is one engine rule: **acting and moving are mutually
exclusive for a builder bot.** Every peck, siphon hit and counterbattery swing
costs that raider its move, and the ladder says **arrival** is the scarce
quantity, not damage. LOKI-5 is the direct evidence: it went 3-2 against
CtrlAltDefeat while landing **ZERO builder attacks** (verified by replay
decode), so the melee was never load-bearing.

**This is a hypothesis consistent with the results, not a demonstrated cause.**
No ablation isolates "rounds returned to movement" from the other consequences
of silencing melee (titanium saved, siphon income lost, cost-scale unchanged).
