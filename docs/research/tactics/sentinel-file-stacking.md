---
tactic: Sentinel file — stack obstacle-ignoring shooters on one ray to beat the adjacency heal cap
source: https://wiki.screepspl.us/Combat/ (damage-vs-heal doctrine); the formation itself is unsourced
origin: inference by tactics sweep 2 applied to our ruleset; Screeps combat doctrine for the framing only
evidence: inference
transfers: yes — BUT GATED ON AN UNVERIFIED ENGINE FACT, PROBE BEFORE BUILDING
---

WHAT IT IS — **Inference by tactics sweep 2. There is no source for this
formation; do not attribute it to any team.** The reasoning:

- The defender's heal throughput **at any one tile** is hard-capped by orthogonal
  adjacency: at most **4 builder bots** can heal a given tile, so **≈16 HP/round
  for 4 Ti/round**. There is no way to add a fifth.
- The attacker's damage **at that same tile** is capped only by titanium.
- **Sentinels ignore obstacles.** So in principle any number of sentinels can be
  stacked in single file along the same ray, all firing *through each other* into
  the same tile.

WHY IT MIGHT TRANSFER — **This is the structural break in the 2.2:1 defensive edge,
if it exists anywhere.** The defender's heal is a *linear-law, density-capped*
resource; the attacker's fire is a *concentrable* one — the Lanchester distinction.

Sentinel: 18 damage, reload 2 → ~6-9 HP/round each. Against a 16 HP/round cap you
need **2-3 sentinels bearing on one tile** to make net progress, and **every
sentinel beyond that is pure surplus the defender cannot answer.** Barriers do not
help them: sentinel line shots pass straight through.

This is also the arithmetic behind the alpha-strike discipline in
[sweep 2](2026-08-09-sweep-2.md): sub-threshold damage is not merely inefficient,
it is a **2.2:1 donation.**

WHAT WOULD KILL IT — four things, and the fourth is decisive:

1. `MAX_TEAM_UNITS = 50` caps the fleet alongside builders and harvesters.
2. Sentinel scale is **+20% each** — the 6th costs ~3× base. The surplus is not free.
3. If `reload 2` means firing every 3rd round, per-sentinel rate drops to ~6
   HP/round and you need 3+ just to break even.
4. **UNVERIFIED AND DECISIVE: I have not established that two sentinels on the same
   ray can both hit the same tile.** If the engine resolves a line shot as *"first
   entity hit"*, the rear sentinel's shot is absorbed by the friendly sentinel in
   front, and the entire formation is not merely useless but self-blocking.

BUILDER HOOK — **An engine probe, not a bot, and it gates the whole block.** Place
3 friendly sentinels in a straight file with one enemy barrier at the end of the
ray; call `can_fire` / `fire` from each and read the HP deltas on the barrier.

- Rear sentinels damage the barrier → **the tactic is live** and deserves a design.
- Rear sentinels hit the friendly in front (or cannot fire) → **refile as
  `transfers: no`** and delete this block's premise.

Cheap, deterministic, and it answers a question that also constrains our *own*
defensive turret spacing — if sentinels block each other, our home ring geometry
is currently unchecked against that.

Related: [sweep 2](2026-08-09-sweep-2.md) ·
[heal arithmetic](../heal-arithmetic-2026-08-09.md) ·
[machinery audit](../machinery-audit-2026-08-09.md) (sentinels cannot rotate — so a
mis-sited sentinel file cannot be re-aimed, only destroyed and rebuilt)
