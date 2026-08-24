# BUILD REPORT — the wave map catalogue, and the day the fortress lost to a grep
**Builder s58, 2026-08-24. GAME CONTEXT: in-game Florent Code League — every
term below is an engine mechanic in a sandboxed bot-vs-bot competition.**

## The headline
`_v542wave` (the retired rush line) + a regenerated map catalogue reads
**142/270 = 52.6% [46.6, 58.6]** head-to-head against the real Mjolnir v188
(batches 54.4% / 56.7% / 46.7%), up from a powered base of **35/90 = 38.9%**.
The IMPROVEMENT is significant (~2.3σ); **strict superiority is NOT
established** (the CI includes 50). Parity-plus with the strongest bot on the
team's account, achieved in one session from a 1/30 starting point.

## The arc (each step tape-anchored)
1. **Magnus's directive** ("beat mjolnir with our new bot; figure out what we
   are doing wrong") forced a re-baseline against the REAL v188
   (`fcode submission download 188`) instead of the v105-era fixture every
   F2 number had been measured against. Result: `_v632heim` (the week's
   fortress line) **1/30**; `_v542wave` **12/30**. The week's iteration
   target was a stale snapshot ~80 versions old.
2. **Real v188 is nondeterministic** (noise ON; our fixtures are noiseoff
   ports) — and so is live-config wave (`main.py:1226` spawn_salt from
   unseeded OS entropy; the banked v542wave determinism certificate is
   NOISE-off-config-scoped and stands). All single-run grids are samples;
   every read here is n>=90.
3. **The surge plank (agent-built, REFUSED honestly):** a late-eco pivot
   (WAVE_LATE_SURGE, 14 clauses) built harvesters 1-2 -> 10-13 and moved
   delivery NOWHERE (belts unfinishable on contested ground); its funding
   clauses cost defence (core deaths 24->40/80). Ablation n=540: OFF 52.2%
   beats every ON arm. Shipped OFF (statically unreachable). Banked
   sub-findings: the pinned-link-queue deadlock (two of our own bodies
   deadlock a belt forever), route-length-first ore ordering, the
   12-harvesters-2-connected delivery shape.
4. **The real defect, found by the agent's binder analysis:** wave's
   MAP_CODES/EXTRA_MAP_CODES predate the current 15-map pool.
   `known_map_for` returned **None on every live map** -> no ore partition
   AND no pathfinding (greedy compass steps; invisible 2-cycles — a
   *successful* move every round, so the stuck counter never fires; measured
   350-round livelocks with the harvester ratchet pinned at 1-2).
5. **The fix:** `tools/map_encode.py` (built s36 for this exact class,
   selftest byte-for-byte + corruption control) encoded all 15 pool maps;
   entries installed in `EXTRA_MAP_CODES`, key-verified, MAPTRUST confirms
   at runtime. One commit. +13.7pp.

## The doctrine line (route to a standing rule)
**Exact-tile constants expire with map/pool changes.** This is the s36
livelock class resurrected verbatim by a pool rotation: the fix existed, the
tool existed, and the tree still expired because nothing re-runs the encoder
on rotation. Candidate standing rule: a pool-rotation event triggers
`map_encode.py` against every live tree's catalogue (a 5-minute mechanical
step), and any tree whose catalogue misses a live map is flagged by a boot
check. Routed to the wrap for Magnus/queue admission.

## What remains (successor levers, none built)
- **Consistent holes at n=9:** holmgang A+B, longhouse A — mid-game
  core-grind losses on small/close maps where v188's raid package dominates;
  a matchup problem, not an instrument one.
- The agent's diagnosed-but-unbuilt candidates: global (not per-unit)
  unfinished-belt record; MAP_CODES for any future rotation.
- The ferry-rush answer (LAUNCHER_MIN_RND=0 read null at n=14 pre-catalogue;
  untested on top of the catalogue — interaction plausible, pathfinding now
  exists).
- The same catalogue fix applies to every retired tree in this lineage
  (`_v488beltbreak2` etc.) if any is ever revived.

## Ship status
NOT shipped. The ship decision is Magnus's word, denominated honestly:
head-to-head parity-plus [46.6, 58.6] at n=270 vs a field-verified
51.2%/260-game holder; wave+catalogue's FIELD rate unmeasured (the catalogue
is opponent-independent self-repair, so the field effect should be
directionally positive, but that is an inference, not a measurement).
Slot untouched all session; zero rated exposure from any of this work.
