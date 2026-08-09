---
tactic: Imprisonment — throw an enemy builder into a prebuilt cell and hold it with heal arithmetic
source: https://superflux.dev/blog/battlesnake-2018
origin: Battlesnake 2018 (emergent trap-and-starve); the arithmetic below is ours
evidence: documented (principle) / inference (our implementation — inference by tactics sweep 3)
transfers: partial — GATED ON ONE UNVERIFIED ENGINE FACT
---

WHAT IT IS — Battlesnake's emergent winning behaviour: *"my snake would wrap around
it, trapping it. When the 'chicken-snake' decided it had been spinning for long
enough and it was time to eat, there was nowhere to go."* A cheaper variant pinned
the victim against terrain and starved it. The author reports it *"worked very
well"* in 1v1.

**Our version: prebuild an empty 1-tile cell (4 barriers around one empty tile)
inside our own territory within r²=26 of a launcher, then throw an enemy builder
into it.**

WHY IT MIGHT TRANSFER — **This is where our ruleset is better than the source
game's**, and it is the most underexplored thing in either sweep.

- The prisoner breaks out by attacking a barrier: **2 damage for 2 Ti per turn.**
- We repair it: **+4 HP for 1 Ti per turn.**
- **Heal beats attack 2× on rate and 2× on cost simultaneously**, so a maintained
  barrier is *mathematically unbreakable by a single enemy builder.*
- **Builder bots move cardinally only** — four barriers seal a tile with **no
  diagonal escape.** ~12 Ti before scale, and barriers scale at only +1%.
- The prisoner keeps taxing their **+20% builder cost scale** and occupying one of
  their **50 unit slots** for the rest of the match.

Compare the alternative: killing that builder *refunds* their scale and frees the
slot. See [[displace-dont-kill]].

WHAT WOULD KILL IT — Two engine facts decide it, and **only one is known**:

1. **UNVERIFIED AND DECISIVE:** does `can_launch` accept a target tile that is
   fully enclosed by buildings? If the engine requires connectivity or a path, the
   prebuilt-cell play is dead and the cell must be sealed manually *after* the
   throw — much harder and probably not worth it.
2. **Two enemy builders adjacent to the cell deal 4 dmg/turn against one healer's
   4 HP/turn — an exact tie.** A two-builder rescue breaks it, so the cell must sit
   somewhere their second builder will not reach, or we must be willing to commit a
   second healer.

**SCOPE NOTE — this is NOT the tactic the builder refuted on 2026-08-09 08:52.**
That probe (`bots/_probe_prison`) tested building a barrier *on top of a standing
bot* and found `can_build_barrier = False` even though `is_tile_empty = True` —
build legality is strictly stronger than `is_tile_empty`. **A prebuilt empty cell
that a bot is thrown into is a different proposition and is untouched by that
result.** Recorded explicitly per the s22 §4 warning that *"refuted alone is not
refuted"*: a kill criterion for one formulation must not be read as closing a
different one.

*Second-order note: the same probe established that parking a builder on a tile
makes that tile unbuildable — which is why a spawn-lock fails against a competent
opponent. That cuts against cell-building near a defended enemy too: they can deny
our cell tiles by standing on them, if they ever notice.*

BUILDER HOOK — **One boolean, ~12 Ti, one match.** Prebuild the cell inside our
territory within a launcher's r²=26, then call
`can_launch(enemy_bot_pos, cell_tile)` and read the return. True → this is a real
strategy and deserves a real design. False → file as `transfers: no` and stop.

Related: [[launcher-defensive-interception]] · [[displace-dont-kill]] ·
[sweep 3](2026-08-09-sweep-3.md) · [heal arithmetic](../heal-arithmetic-2026-08-09.md)
