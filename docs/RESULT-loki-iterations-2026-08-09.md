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

---

## ROBUSTNESS — MY HEADLINE p IS NOT ROBUST TO DROPPING ORIZON

**Magnus reports Orizon has fallen below 1400. We are ~1595, so they are out of
our matchmaking bracket** — a ladder-relevant verdict should weight them near
zero, and they are one of the three opponents in the fixture above.

Per-opponent core-kill wins, n=5 each:

| arm | Ouroboros | Orizon | CAD | ALL | **ex-Orizon** |
| --- | ---: | ---: | ---: | ---: | ---: |
| v94 Eir | 1 | 2 | 2 | 5/15 | **3/10 = 30%** |
| LOKI-4 | 3 | 3 | 2 | 8/15 | 5/10 |
| LOKI-5 | 4 | 5 | 3 | 12/15 | 7/10 = 70% |
| LOKI-6 | 1 | 4 | 3 | 8/15 | 4/10 |
| **LOKI-7** | **4** | **5** | **4** | **13/15** | **8/10 = 80%** |

| comparison | with Orizon | **without Orizon** |
| --- | --- | --- |
| LOKI-7 vs Eir | 13/15 vs 5/15, **p = 0.0078** | 8/10 vs 3/10, **p = 0.070** |
| LOKI-5 vs Eir | 12/15 vs 5/15, p = 0.025 | 7/10 vs 3/10, p = 0.179 |

**⇒ The significance was leaning on games against a team we will not meet.
Effect size holds (80% vs 30%); significance does not survive the n drop.**
I am not going to quote p = 0.0078 again without this line attached.

**What DOES survive, and it is the reassuring part: LOKI-7 beats Eir in EVERY
opponent cell — 4 v 1, 5 v 2, 4 v 2 — three independent opponents, same
direction each time.** Consistency across cells is weaker than a p-value but it
is not nothing, and it is the kind of evidence a single lucky opponent cannot
manufacture.

**FIXTURE CHANGE, from here:** Orizon is dropped from verdict fixtures and
replaced with bracket-relevant opponents (Lunds Stallions, Kings College
Munich). `orizon_probe` is **kept** as an offline instrument — it has the best
resolution in the pool (50% baseline, and it is what caught the rush costing
share) — but it is a **calibrated measuring stick, not a ladder-representative
opponent**, and D11 verdict wording should say so.

## EIR ON THE LONG MAP BAND — the fair cross-band comparison

v94 Eir, long band (saga, atoll, lighthouse, drumlin, hive), 3 opponents, n=15:
**7-8, core-kill share 6/15 = 40.0%** — including an **0-5 wipe by Ouroboros**
and a 5-0 sweep of Orizon.

| | short band | long band |
| --- | --- | --- |
| v94 Eir | 33.3% (5/15) | 40.0% (6/15) |
| LOKI-5 | 80.0% (12/15) | 60.0% (6/10, 2 opponents) |

**Loki leads on both bands, and its advantage NARROWS on long maps** (+46.7pp
short, +20.0pp long). Consistent with the line's mechanism being about
ARRIVAL: the longer the walk, the less a returned round is worth.

---

## UPWARD BAND — Magnus: *"Should we collect some data vs 1600+ opponents too?"*

**The challenge was correct and it was the sharpest one aimed at these numbers.**
Every figure above was earned against teams at or below us (live, from our own
Elo log: Ouroboros 1542, KCM 1550, Lunds 1576, CAD 1603, us 1604) — plus Orizon
at 1396. **Loki had zero upward data, so "86.7%" was consistent with harvesting
weak collars.**

**LOKI-8 and v94 Eir, MATCHED — same opponent, same five maps, n=5 per cell:**

| opponent | Elo vs us | v94 Eir | **LOKI-8** |
| --- | ---: | ---: | ---: |
| Ouroboros | −62 | 1/5 | **4/5** |
| CtrlAltDefeat | ~0 | 2/5 | **4/5** |
| Lunds Stallions | −28 | 2/5 | **3/5** |
| **Big O** | **+200** | 2/5 | **3/5** |
| **Jython** | **+337** | 0/5 | **1/5** |
| **pooled** | | **7/25 = 28.0%** | **15/25 = 60.0%** |

**Fisher two-sided p = 0.045. LOKI-8 is ahead in 5 of 5 cells — no ties, no
reversals — across a 540-Elo span.** The sign test alone is p = 0.0625.

**⇒ The advantage is NOT confined to weaker opponents.** It survives at +200 and
at +337, where both bots are losing overall: Eir goes 0-5 against Jython and
Loki goes 1-4. **Loki does not beat stronger teams — it dies less totally, and
takes a core with it.**

**AND THE DOSE-RESPONSE IS REAL, which is the honest limit:**

| band | LOKI-8 core-kill share |
| --- | --- |
| bracket (−62 … 0 Elo) | 15/20 = **75%** |
| +200 Elo | 3/5 = **60%** |
| +337 Elo | 1/5 = **20%** |

**The kill advantage decays with opponent strength.** It does not vanish, but
anyone quoting 75–86% should say which band it came from. **This is now the
number I would carry into a ship decision, not the short-map 86.7%.**

## LOKI-8 (raiders exempt from the home heal + melee recall) — VERDICT

Across the bracket four: **15-5, 15/20 = 75%** core-kill share, matching LOKI-7
on the two shared cells and extending cleanly to two opponents LOKI-7 never
played. **It is the best-tested arm on the line and the one I would ship** —
but LOKI-7 vs LOKI-8 has never been run head to head on the same fixture, and
**at these n they are indistinguishable.** I am not claiming 8 > 7.
