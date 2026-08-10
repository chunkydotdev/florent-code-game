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

---

# MECHANISM BARS READ. **BAR A: NOT MET. THE LEG ANSWERED NOTHING.**

All 25 treatment and all 50 control games decoded cleanly — **0 unreadable, 0
excluded, 0 decode errors** (several needed retries against the flapping
platform; none were dropped). Seats resolved per match. Forward-sentinel
definition identical to LOKI-11's banked method. Cross-validated two ways: the
decode matched `tools/replay_census.py` and `replay_autopsy.py` exactly on a
sample file, and forward-sentinel totals matched `replay_builds.py`'s
independent FORWARD/HOME classification exactly.

| per game, our team | LOKI-13 (n=25) | control (n=50) | ratio |
|---|---:|---:|---:|
| **conveyors built — BAR A** | **33.32** | **38.66** | **0.86** |
| harvesters built | 4.64 | 5.22 | 0.89 |
| builder bots spawned | 6.68 | 6.92 | 0.97 |
| forward sentinels built | 2.04 | 4.58 | **0.45** |
| `titanium_collected` | 1074.80 | 1727.80 | **0.62** |
| ammo converted | 505.12 | 458.98 | 1.10 |
| ammo end balance | 62.16 | 38.94 | 1.60 |
| shots fired | 45.88 | 47.08 | 0.98 |
| our own units lost | 2.56 | 5.86 | **0.44** |

**BAR A was `<= 27/game` (`<= 0.70x` control). Measured 33.32, ratio 0.86.
NOT MET, and not marginally — the miss is decisive.**

**⇒ PER THE PRE-REGISTRATION: THE LEG ANSWERED NOTHING ABOUT ECONOMY
SUPPRESSION. The +18.0pp currency reading CANNOT be attributed to the flag**
and is not evidence for or against the plank. Written as pre-committed, and the
currency table earlier in this document must not be quoted without it.

## THE REASON IT MISSED IS THE FINDING, AND IT IS THE SAME FAULT AS LOKI-11's

The bar was derived from **the flag's own paired-seed action**, measured
locally: **0.65x / 0.67x / 0.43x**. That was the fix for LOKI-11's bar problem
and it was the right fix in shape. **On live teams the same flag produced
0.86x.**

**THE FLAG'S OWN ACTION DOES NOT TRANSFER FROM LOCAL TO LIVE.** Almost certainly
because local games against our probes run long (500+ turns) so the pave trail
dominates the conveyor count, while live games are shorter and more contested so
deliberate line-building dominates instead. **A ratio measured on the treatment
alone is still a ratio measured on a fixture** — and I wrote in the amendment
that "the RATIO transfers, the absolute does not." **That was an assumption, not
a measurement, and it is now falsified.**

## AND THE BAR METRIC WAS A POOR PROXY EVEN SO — the downstream moved far more

Conveyors fell only 14%, but in the same games **`titanium_collected` fell 38%,
forward sentinels fell 55%, and our own unit losses fell 56%.** The quantity the
bar measured barely moved while the quantities it was standing in for moved
enormously. **A treatment-occurrence check that under-reads its own treatment by
this much is a badly chosen proxy regardless of how it was derived.**

**The honest statement is therefore doubly negative and both halves matter:**
the leg answered nothing about economy suppression, **and** the method fix that
was supposed to prevent exactly this failure did not work either.

## What is left standing, none of it claimed

* **Ammo is NOT the constraint.** Conversion was *higher* under treatment
  (1.10x), end balance 1.60x, shots flat (0.98x). The pre-leg worry that we
  would "cut the economy and then not afford to shoot" is **not what happened** —
  we ended games holding *more* unspent ammunition. That was worth instrumenting
  and it came back clean.
* Treatment lost **56% fewer of its own units** while firing the same number of
  shots. Unattributed, and interesting.
* **The Bisons kill (1/5 after 0-for-20) stands as a recorded surprise**, and is
  now explicitly NOT attributable to this flag either.
