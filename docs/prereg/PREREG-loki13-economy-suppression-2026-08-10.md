# PREREG — LOKI-13: ECONOMY SUPPRESSION (`PAVE_TRAIL_ON` off)

**Committed BEFORE submission, activation and leg creation.** Line `loki`.
Platform clock quoted in the commit body, per the standing self-certifying rule.

    bots/_v130loki13 = bots/_v124loki8 (v102, live) with PAVE_TRAIL_ON: True -> False

`main.py`, `raid.py`, `eco.py` **byte-identical** to v102; the `doctrine.py` diff
is that one line plus its comment.

**Comparator: the pinned-testbed control at n=50** (v102, two windows, same 5
opponents, same 5 pinned maps: fjordgate, jackpot, atoll, saga, snowflake).
Control currency, already banked: `core_kill_share` **21/50 = 42.0%**,
`r1000_rate` **6/50 = 12.0%**, our kill median 246.

## The defect

The pave trail drops a conveyor on the tile a builder just vacated, on every
move, **uncapped** — `ECO_CAP` gates HARVESTERS only (`eco.py`,
`harv < self._eco_cap(ct)`). Nothing bounds the conveyor stream.

**Live-measured on the pinned testbed, both arms of the LOKI-11 leg:**

| conveyors/game | |
|---|---|
| **us, v102** | **38.20** |
| us, LOKI-11 (rush) | 20.92 |
| The Bisons (live replay autopsy) | ~11 |
| Cookie (archive — a hypothesis under the live-evidence standard) | 0.42 |
| Prompt Engineers Anonymous (archive, 230 games) | 0 conveyors, 0 harvesters, 0 sentinels EVER |

**LOKI-11 already established that half this dose is free**: conveyors 38.20 ->
20.92, harvesters 5.44 -> 3.12, **39% fewer of our own units lost**, and
`core_kill_share` did not regress. **This plank asks where the other half
breaks.** Under `R1000_IS_DEFEAT` the titanium a conveyor buys does not score —
it can only ever fund a kill, and 38 conveyors is not funding a kill at r32.

## Bars — ECONOMY BARRED SEPARATELY FROM CURRENCY

Adopted from the side lane, and it is the correction that makes a negative
result readable: Cookie and PEA prove the extreme is **viable**, not that it is
**viable for us** — they pair zero economy with a rush we have not shown we can
execute. So *"we cut conveyors 60% and lost"* must not be allowed to read as
*"economy suppression fails"* when it may be *"we cut the economy without buying
the kill it was meant to fund."*

**MECHANISM A (the cut landed):** conveyors built per game. Control **38.20**.
**BAR: <= 25/game.** Decoded from the leg's own replays, same decoder and the
same full-2x2-footprint method used for LOKI-11.

**MECHANISM B (the money went somewhere):** `titanium_collected` per game and
forward sentinels per game, both arms. **No bar** — this is the diagnostic that
separates *"we spent it on the kill"* from *"we simply have less."*

**VERDICT (PRIMARY_CURRENCY): `core_kill_share`** vs the control's **21/50**,
reported with its interval, **per-opponent Δ column mandatory** (the LOKI-11
headline was two of five cells and I will not publish another aggregate without
the split), and the seat mix printed.

**MECHANISM A missed -> THE LEG ANSWERED NOTHING** about economy suppression.

## Bars are sized from the CONTROL ARM'S OWN LIVE NUMBERS, not from a local run

**LOKI-11's bars were sized off one local match against `_probe_victim` and both
premises turned out false — the bars passed while the story they encoded was
wrong.** Every threshold above is taken from the live pinned control at n=50 or
from the LOKI-11 arms. **No number in this prereg comes from a local run against
a probe we wrote.**

## Falsifier

1. **Cut lands, `core_kill_share` flat -> LABELLED NULL**, and the plank is then
   a pure cost saving: same kills for ~45% less economy, which is worth having
   but is not a currency gain and will not be written as one.
2. **Cut lands, `core_kill_share` DOWN, `titanium_collected` DOWN -> the economy
   was funding the kill.** The direct refutation, and the most likely outcome.
3. **Cut lands, `core_kill_share` DOWN, `titanium_collected` FLAT -> the pave
   trail was doing something other than economy** (screening, pathing, blocking)
   and the plank has hit a mechanism nobody modelled. Labelled, not banked.
4. **Cut lands, `core_kill_share` UP -> 38 conveyors/game were actively costing
   us kills**, which is the largest single finding available on this line.

**Pre-committed against convenience:** n=50 control vs n=25 treatment resolves
roughly 25-30pp. **A delta under that is a null and I will write the word**, as
I did for LOKI-11 at +16.0pp.

## Cost — measured, not estimated

**LOKI-11's true rated cost was ZERO rated ladder matches** (verified: every
recent ladder match carries `ourver=102`). Ladder pairings land ~10 minutes
apart; the activation window is shorter than one interval. Procedure:
**serve the rate-limit wait with v102 live, activate LOKI-13 only in the instant
before firing, roll back on the fifth accepted challenge.**
Absolute floor **1550** stands — the slot rule cannot fire inside a sub-8-match
activation, so the floor and lane attention are the only protection.
