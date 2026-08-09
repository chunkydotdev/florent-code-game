---
tactic: NEGATIVE — the league table. Across Battlecode 2017-2026, Halite I/II/III, Lux S1/S2, Terminal and CodinGame's full 94-game catalogue, player-built directed breakable transport DOES NOT EXIST. Exactly two competitive leagues have it
source: https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/kore_fleets/helpers.py
origin: leg 3 of sweep 19, over ~130 primary sources; Battlecode spec greps and the CodinGame catalogue enumeration are that leg's, not re-verified by me — see the provenance note
evidence: documented
transfers: no
---

WHAT IT IS — my brief pre-registered *"I expect Battlecode to contribute nothing to
this row"* and held open that a broad negative would be *"a GENUINE AND VALUABLE
NEGATIVE"*. **The Battlecode half is confirmed. The general half is not.**

| league | player-built directed transport? | how established |
| --- | --- | --- |
| **Battlecode 2017-2026** | **no, in any season** | leg 3 grepped every published season spec for `conveyor\|pipeline\|belt\|transport`: **0 hits, all seasons**. Resources either credit a global pool instantly or are physically carried by a unit. |
| Halite I / II | no | the action set is five moves (I/II adds dock/undock); **no build verb exists** |
| Halite III | no | engine command enum is exactly `Move`, `Spawn`, `Construct`; a `Dropoff` has a location and nothing else — **a destination that shortens the carry, not a route** |
| Lux S1 | no | roads are player-created and pillageable but are an **undirected per-tile cooldown scalar that carries nothing** |
| Lux S2 | no | lichen is **adjacency-grown from the factory**, not routed — a connectivity-gated bonus with no source, sink or direction |
| Terminal | no | two abstract global resource pools; nothing physically moves |
| CodinGame (94 games) | no | corpus-wide grep for `conveyor\|pipeline\|belt\|duct\|railway\|rail` → **0 hits across all 94 statements** |
| **Kaggle Kore Fleets** | **YES** | a string-encoded route, silently truncated — see [`invert-the-engines-own-constraint-into-a-pre-commit-gate`](invert-the-engines-own-constraint-into-a-pre-commit-gate.md) |
| **OpenTTD NoAI** | **YES** | AIs build and repair actual road and rail — the richest source in this sweep |
| Screeps | **partly** | roads are player-built and decay, but they are a movement optimisation, not the only path a resource can take |

**Two structurally distinct families keep getting mistaken for transport, and naming
them is the useful part of this file:**
1. **Destinations that shorten the carry** — Halite III dropoffs, Battlecode 2019
   churches, Battlecode 2020 refineries. A unit still carries the resource.
2. **Connectivity-gated bonuses** — Lux S2 lichen, CodinGame territory rules. A
   local pattern grants a global benefit; there is no source, no sink and no
   direction.
   **Neither can produce our failure**, because neither has a directed edge that can
   point at nothing.

**⚠ PROVENANCE, stated because this table is the sweep's load-bearing negative.**
The Battlecode spec greps and the CodinGame catalogue enumeration are **leg 3's
work, reported with per-year character counts and hit counts. I attempted to
re-fetch the Battlecode specs myself and every URL I tried returned 404**, so I
could not reproduce that grep independently. Two things bound the risk rather than
remove it: leg 3 reported one season (2021) at only 5,291 characters, which is
short enough to suspect an incomplete fetch of that one document; and **this
library independently read all 22 official Battlecode postmortems in sweeps 1, 3,
15 and 17A and no transport mechanic appears in any of them.** **The Battlecode
negative is well-supported and it is not first-hand.**

WHY IT MATTERS — this is what makes the rest of sweep 19 interpretable:

- **The brief's expectation was HALF right, and the wrong half is the one that
  matters.** *"No competitive league builds a fragile directed network, so nobody
  solved this"* is false — **two do, and one of them (OpenTTD NoAI) has answers to
  all four sub-questions.** But the field is two leagues wide, not twenty, which is
  why so much of sweep 19's material is community, academic or engine-source rather
  than competitor postmortem.
- **It explains the whole library's silence on this row until now.** Eighteen sweeps
  drew mostly on Battlecode, Halite, Lux, CodinGame and Terminal. **Not one of those
  five can exhibit our largest failure class.** The library was not failing to find
  the answer; it was searching a corpus in which the question cannot be asked.
- **And it bounds what "the field does X" can mean here.** Any claim in sweep 19 of
  the form "competitors converged on X" rests on **OpenTTD's seven AIs plus Screeps'
  open bots plus two Kore bots plus two Flatland winners.** That is a real field and
  a small one. **Treat every convergence in this sweep as suggestive of a good shape
  and never as a distribution.**

WHAT WOULD KILL IT — a Battlecode season, or a CodinGame game, with a player-placed
directed carrier. **The way to settle it first-hand is to re-fetch the seven
Battlecode spec documents from working URLs and re-run the grep**, which I could not
do tonight and which is the top item in this sweep's gaps.

BUILDER HOOK — none. This file exists so the next session does not re-sweep
Battlecode for logistics doctrine.
