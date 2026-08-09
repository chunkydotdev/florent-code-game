# LOKI-4 — ore denial

Fork of `bots/_v103split`. New code: `denial.py` (the whole mechanism) plus a
`LOKI-4` constants block at the end of `doctrine.py`. `main.py` carries four
hooks and nothing else — the diff against the parent is ~45 lines.

**Ablation unit:** `ORE_DENIAL_ON = False` in `doctrine.py` makes every entry
point in `denial.py` return on its first line, reproducing `_v103split`.
Sub-flags `DENY_CRATER_ON` and `DENY_RECLAIM_ON` split the two arms apart.

---

## The mechanic (engine-probed, not inferred)

`bots/_probe_denial` on fjordgate, re-run today:

```
ore tile (6,0): is_tile_empty=True  can_build_harvester BEFORE=True
can_build_barrier=True   barrier_cost=3   harvester_cost=24
after our barrier stands:            can_build_harvester=FALSE
after we destroy() our own barrier:  can_build_harvester=TRUE
```

Harvesters may only be built on ore, so a 3 Ti barrier removes a 24 Ti site.
`ct.destroy()` is **allied-only**: clearing it costs them 30 HP at 2 dmg / 2 Ti
= 15 attacks, 30 Ti and 15 builder-turns. ~10:1 in titanium, ~15:1 in
builder-turns, and free for us to undo.

---

## Two arms

### 1. Generic reactive denial (enemy-side ore)

A unit already standing **orthogonally adjacent** to an unclaimed enemy-side ore
tile spends one turn and 3 Ti. No detour, no dedicated trip, no prediction.
Call sites: the `role_n == 0` saboteur and expanders, both at the **bottom** of
their action phase. Gated by `DENY_MAX_ENEMY_ORE` (map scarcity),
`DENY_MAX_RND = 150`, `DENY_MAX_BARRIERS = 4` per unit.

### 2. Crater denial (`DENY_CRATER_ON`)

Remembers ore tiles **in our own half** that an enemy harvester was standing on,
and seals them once they are freed — by anything: our turrets, our builders'
attacks, or their own teardown. **The turret half (actually killing the
harvester) is deliberately not implemented here** — it lives in `_v107loki3`, so
the two compose without either depending on the other.

Exempt from `DENY_MAX_ENEMY_ORE` (that gate measures scarcity on *their* side,
which says nothing about a tile in ours) and from `DENY_MAX_RND` (the flow it
targets is r150+). What replaces both gates is **evidence**: an enemy harvester
stood there, so we are not guessing that they want the tile.

Sighting memory is **per unit** — all 16 store slots are occupied, so there is
nowhere to publish it. Only a builder that personally saw the harvester can seal
its crater. That undercounts opportunities and never miscounts them.

### Reclaim (`DENY_RECLAIM_ON`)

`destroy()` is free, has no cooldown and is unlimited per turn, and the probe
confirmed `can_build_harvester` returns True in the **same** turn. So an
expander that later wants a tile it once denied takes its own barrier back.
Restricted to tiles this doctrine could have denied, so it can never dismantle
the home-defence barrier `_defend` plants near our Core.

---

## Why the economy is safe

On any tile we can economically work, **a harvester is a strictly better
barrier**: same permanence, same denial to them, plus 2.5 Ti/round. Both arms
therefore sit *below* the harvester build in the same action phase, and the
`get_action_cooldown() != 0` check on the first line of each makes "never trade
a harvester for a barrier" **structural** rather than a promise — any
higher-priority action has already consumed the cooldown by the time control
reaches denial.

Cost accounting:

- **Scale.** Cost scale is one global multiplier over all categories tracking
  *live* entities. A barrier is +1% while it stands, and since only we can
  remove it, that is usually the rest of the match. Capped at 4 + 4 barriers.
  Measured end-of-game scale ours vs opponent: 348.9 / 338.8 — a +10 point
  gap, ≈ +2 Ti on a 20-base harvester.
- **Builder-turns.** Zero dedicated trips and zero detours: placement requires
  the unit to be adjacent already. Cost is exactly one builder-turn per
  barrier, taken from units whose alternative action was the low-value melee
  peck. No expander turn is diverted from ore.

---

## What was built and then deleted, and why

Recorded here and in `doctrine.py` so none of it is rebuilt.

1. **Pre-emptive siting** (barrier the tile before they arrive). Dead on a
   pincer: the opening tile is predictable but unreachable (first harvesters
   land r2-13, p10 r6), the late tile is reachable but unpredictable (rank 4+ is
   82-86% of picks by r150). No window where both halves hold.
2. **A per-opponent tile book.** The apparent modal opening tile is just the
   nearest ore to that seat's Core — for them (42.9% rank-0, 81.1% top-3) and
   for us (49.9% / 85.5%) alike. The determinism is geometric, not behavioural,
   so a book would encode geometry we already derive and add a staleness hazard
   for no signal. (We already have one suspended hardcoded tile table from
   exactly this mistake.)
3. **A bounded 2-step detour** toward a planned tile. Removed with the
   pre-emptive half — it buys route risk for a denial that only pays when the
   tile was on the way anyway.
4. **Blanket home-side denial.** Measured over 497 invasion events: at the
   moment an enemy harvester lands on our side, the victim still has a **median
   of 5 unclaimed ore tiles** on that side, and 49.1% of invasions happen with
   ≥6 free. Median victim side size at those moments is 13 — invasion is a
   phenomenon of ore-rich maps, which are exactly the maps where denial is
   definitionally noise. The crater arm is what survives of this idea, and it
   survives because it is evidence-driven rather than speculative.

**Do-not, from research's exchange table:** cutting conveyors runs 4:1 *against*
us (~12 Ti of ammo to cut, 3 Ti for them to relay). The correct denial
primitive is a barrier on the ore tile, never damage on the line.

---

## The kill criterion, and it is half-failed

Pool ore census (15 maps, parsed from `maps/*.map26`): **314 ore tiles, mean
20.9 per map, mean 9.4 per side.** Replay census (250 archived games, 3,073
harvester builds): a team consumes a **median of 4 distinct sites** (p75 7,
p90 13).

**On the median map they have five spare sites, and denying two denies
nothing.** Enemy-side ore per map:

| deniable (≤7) | | noise (≥10) | |
|---|---|---|---|
| fjordgate | 2 | nordkap | 10 |
| atoll | 3 | heart | 11 |
| moonrise | 3 | drumlin | 13 |
| antler | 6 | eider | 16 |
| hive | 6 | snowflake | 16 |
| jackpot | 6 | saga | 17 |
| lighthouse | 6 | archipelago | 19 |
| meander | 7 | | |

The meander(7)/nordkap(10) gap is the only clean break in the pool.
`DENY_MAX_ENEMY_ORE = 7` sits in it and turns **arm 1 off on 7 of 15 maps**.

This is the honest read: **the generic arm has a low ceiling and is the weaker
half of the build.** The crater arm is the one with an exchange rate behind it,
and it is the one worth measuring.
