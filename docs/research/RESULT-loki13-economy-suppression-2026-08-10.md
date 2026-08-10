# RESULT — LOKI-13, economy suppression (`PAVE_TRAIL_ON` off) on live teams

Prereg `docs/prereg/PREREG-loki13-economy-suppression-2026-08-10.md`
(git author **04:51:12Z**, pre-leg amendment **05:04:36Z**); leg fired
**05:40:41Z**, rollback verified **05:41:00Z** — a **66-second** activation
window. Treatment = v102 with **one constant**, `PAVE_TRAIL_ON: True -> False`;
`main.py`, `raid.py`, `eco.py` byte-identical.

## CURRENCY — **NULL BY PRE-REGISTRATION. The word is written.**

| | control (v102) n=50 | LOKI-13 (v104) n=25 |
|---|---|---|
| **`core_kill_share`** | **21/50 = 42.0%** | **15/25 = 60.0%** |
| `r1000_rate` (= DEFEAT) | 6/50 = 12.0% | 2/25 = 8.0% |
| our kill turns, median | 246 | 184 |
| kills inside r250 | 11/21 | 11/15 |

    delta +18.0pp     Fisher exact two-sided p = 0.152

**The prereg pre-committed, before the data existed:** *"n=50 control vs n=25
treatment resolves roughly 25-30pp. A delta under that is a null and I will
write the word."* **+18.0pp is under it. This is a NULL.** Direction is
favourable and it is the third consecutive leg whose point estimate flatters
the treatment while failing its own resolution bar — which is exactly the
pattern LOKI-11 showed before doubling n took +16.0pp to +0.0pp.

## ⚠ TWO OF FIVE CELLS HAVE A SEAT FLIP, BOTH TOWARD SEAT A

| opponent | control | LOKI-13 | seat |
|---|---|---|---|
| **The Bisons** | **0/10 = 0%** | **1/5 = 20%** | A |
| gsxWins | 3/10 = 30% | 3/5 = 60% | A |
| CtrlAltDefeat | 4/10 = 40% | 3/5 = 60% | **B→A** |
| I Stone | 6/10 = 60% | 4/5 = 80% | **B→A** |
| Leviathan | 8/10 = 80% | 4/5 = 80% | B→B |

**`I Stone` had never played seat A in any prior pinned window** — this is a
configuration the control has never sampled, so that cell is not paired with
anything. **The only cell with an unchanged seat, Leviathan, moved by exactly
zero.** That is not decisive at n=5 per cell, but it is the correct thing to
notice first and it points the same way the null does.

## THE SURPRISE, RECORDED BEFORE IT IS EXPLAINED AWAY

**WE KILLED A BISONS CORE.** 1/5, after **0 for 20** across every prior window,
both seats, both versions, five pinned maps.

Per the directive's fourth clause — *"a surprise is the point, not an anomaly;
write it down before explaining it away"* — that is recorded here and
**explicitly NOT claimed as a result**: n=5, seat A, and one kill against a
0-for-20 floor is exactly the observation a floor cell produces by chance
eventually. **It is the first crack in the only cell that has never moved, and
it earns a targeted leg rather than a paragraph of theory.**

Also: **jackpot 5/5** kills, snowflake 4/5, atoll 4/5 — against **fjordgate
0/5, which is now 0 kills across every arm of every leg tonight.**

## ⛔ NOT A VERDICT — THE MECHANISM BAR IS UNREAD

Bar A (**conveyors/game <= 27**, i.e. <= 0.70x the control's 38.20, derived from
the flag's own paired-seed action of 51->33 / 61->41 / 75->32) **has not been
decoded from the leg's replays.** Bar B (`titanium_collected`, forward
sentinels, **ammo and shots**) likewise.

**The prereg pre-commits: MECHANISM A missed -> THE LEG ANSWERED NOTHING.**
This document is not a verdict until those lines are filled in, and the
currency table above must not be quoted without this sentence attached.
