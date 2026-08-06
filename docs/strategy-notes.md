# Strategy notes

Analysis **derived** from [game-model.md](game-model.md) — arithmetic on the published numbers,
not observed behaviour. None of this is validated against a real match yet. When a match
contradicts something here, fix it here and note the correction in
[strategy-log.md](strategy-log.md).

## Most matches probably end in a tiebreak, and the tiebreak is economic

Killing a Core costs a lot: 500 HP means **28 Sentinel shots (280 ammo) or 72 Gunner shots
(288 ammo)** — plus getting and keeping a turret in range of it. Total passive income across
a whole 1000-round match is only ~2500 Ti, so a kill is affordable but not casual.

If no Core dies, the tiebreakers are, in order: **titanium collected → harvester count →
titanium stored → coin flip.** Two of the top three are pure economy, and the first is *gross*
collected, not what's left in the bank — spending doesn't hurt it.

**Implication:** a bot that only builds economy and never fights beats a mediocre aggressive
bot on tiebreak. Economy first is not the passive choice here; it's the scoring-aligned one.
Combat is for denying the enemy economy and defending our own.

## Healing badly out-economies damage

| Action | Effect | Ti cost | Ti per HP |
| --- | --- | --- | --- |
| Builder `heal` | +4 HP | 1 | **0.25** |
| Sentinel shot | 18 dmg | 10 (ammo) | 0.56 |
| Gunner shot | 7 dmg | 4 (ammo) | 0.57 |
| Builder `fire` | 2 dmg | 2 | 1.00 |

Healing is **4× cheaper than a builder's fire** and **~2× cheaper than any turret's**. Attrition
against a defended, healed target is a losing trade for the attacker at every level.

But heal rate is capped by actions: a Builder Bot heals **4 HP/round** (and can't move that
round). So per-round throughput decides it:

| Attacker | dmg/round | Healers needed to hold |
| --- | --- | --- |
| Builder `fire` | 2 | 1 (out-heals 2×) |
| Gunner | 7 | 2 (8 > 7) |
| Sentinel | 9 | 3 (12 > 9) |

**Implications:**
- Builder-on-building sabotage only works on **undefended** infrastructure. Against a single
  defending healer it's strictly a waste of titanium.
- Winning an attack means **burst above the heal rate** or **killing the healers first** — and
  builders can't shoot builders at all, so killing healers requires a turret.
- Defensively, one builder parked on a threatened conveyor junction neutralises enemy
  builder sabotage outright, for 1 Ti per 2 damage prevented.

## Harvesters have absurd ROI — delivery is the real constraint

A Harvester is 20 Ti base and produces 10 Ti every 4 rounds = **2.5 Ti/round**, which alone
**equals the entire team's passive income**. Payback is ~8 rounds at 100% scale, ~12 rounds
even at 150%.

The catch: a Harvester outputs **only to an adjacent building**, and idles if none can take a
stack. So the real cost of a harvester is *the conveyor chain back to the Core* — conveyor
titanium plus the builder-rounds to walk and lay it. Ore next to the Core is worth
dramatically more than distant ore.

**Implication:** the primary optimisation target early is not "more harvesters" but
"shortest delivery path per harvester". Rank ore by chain length, not by distance to the bot
that happened to see it.

**Upgraded from derivation to measurement (2026-08-06):** crediting is delivery-only — a
harvester with an incomplete chain earns zero balance and zero tiebreak-#1 credit for as long
as the chain stays incomplete (game-model.md, `bots/probe_credit`). "Build the harvester,
sort out routing later" is not a partial win; it is pure cost until the last conveyor closes
the path to the Core.

## Cost scale is a budget we spend, not a clock — and Builder Bots are the expensive part

Scale is **additive per entity built** and **decreases when entities are destroyed**:
conveyor/splitter/barrier +1%, harvester +5%, launcher +10%, **builder bot / gunner /
sentinel +20%**.

**A Builder Bot costs the same scale tax as a Sentinel — 20%, the joint most expensive thing
in the game, and four times a Harvester's.** That reframes everything:

- The shipped starter bot spawns a Builder Bot every round it can afford one. That is the
  single most scale-expensive habit available. Measured in a real match: by round 200 its
  scale hit 139%, pushing Builder Bot cost from 30 → 41 Ti, and it stayed there.
- **Bot count is a strategic decision, not a default.** Every extra builder makes all future
  harvesters, conveyors, and turrets permanently more expensive. A small crew that survives
  probably beats a large one that's constantly replaced — which is doubly true given that
  dead bots get respawned at the new, higher price.
- Conveyors are nearly free on this axis at +1%. **Twenty conveyor tiles cost less scale than
  one Builder Bot.** Long delivery chains are cheap; the bots that build them aren't.
- `ct.destroy()` gives the scale back, **costs nothing, has no cooldown, and is unlimited per
  round** — the only free action in the game. Demolishing a rerouted-around conveyor chain
  cuts the tax on everything built afterward, and refunds any stack in transit. Nothing in the
  tutorials or the starter bot does this.
- A bot that scouts for 100 rounds and builds nothing pays **zero** scale tax in that window.
  The cost of building early is real but so is the compounding from an early harvester —
  worth measuring rather than assuming.

The official docs claim the opposite conclusion ("build aggressively early... before costs
make expansion prohibitive"). That advice ignores that the cost rise *is caused by your own
building* and never decays with time. Worth testing rather than taking on faith — it's exactly
the sort of thing the field will follow by default.

## Sentinel looks strictly better than Gunner except for cost and rotation

| | Gunner | Sentinel |
| --- | --- | --- |
| dmg/round | 7 | **9** |
| Ti per damage | 0.57 | **0.56** |
| ammo/round sustained | **4** | 5 |
| HP | 25 | **40** |
| attack r² | 13 | **32** |
| Blocked by walls/units | **Yes** | No |
| Scale tax | 20% | 20% |
| Cost | **20 Ti** | 30 Ti |
| Rotate after build | **Yes** (10 Ti) | No |

Same scale tax, better on nearly every axis. The Gunner's real edges are the 10 Ti lower entry
price and being **re-aimable** — worth it for a corridor whose threat direction changes.
The Sentinel's unblockable line is a big deal: it shoots *through* the enemy's own units and
walls, so it can't be screened by a body.

**Untested guess:** default to Sentinels for anything static, Gunners only where the facing
needs to change. Needs a real A/B — this is exactly the kind of thing the tutorials'
Gunner-first framing might be quietly wrong about.

## Sustained fire is expensive

A Gunner firing every round burns **4 Ti/round** in ammo — **1.6× the team's entire passive
income**. A Sentinel firing on cooldown burns 5 Ti/round.

**Implication:** you cannot afford turrets that fire at nothing. Facing and placement should
mean a turret only has line on a tile enemies actually cross. Also, the ammo buffer should be
adaptive — the starter bot's fixed "top up to 20" wastes titanium in quiet phases and starves
in fights. The official docs explicitly call adaptive ammo an open problem the shipped starter
bot doesn't solve.

## Map size range is enormous and we get no say

8×8 to 30×30. That's a 14× area range. An 8×8 map means the Cores are nearly adjacent —
economy has no time to compound and rushing is likely dominant. A 30×30 means long delivery
chains, scouting matters, and early aggression may never arrive.

Combined with **best-of-five with random maps per game** and **fractional Elo scoring**
(a 5-0 moves rating far more than a 3-2), consistency across map sizes is worth more than peak
performance on one. A bot that dominates big maps and loses every small one nets nearly zero.

**Implication:** branch on `ct.get_map_width()`/`get_map_height()` early. Treat "small map
opening" and "large map opening" as separate strategies rather than tuning one compromise.

## Cheap robustness wins available immediately

- **Wrap `run()` in a top-level `try/except`.** An uncaught exception *permanently* deletes
  that unit for the rest of the match; a caught one costs nothing. There is no downside. The
  tutorials never mention doing this.
- **Budget CPU explicitly.** Overrunning 10 ms costs only that unit's round, so a bot that
  checks `ct.get_cpu_time_elapsed()` and bails out gracefully degrades instead of failing.
- **Always `--tle 10` locally.** `fcode run` does *not* enforce the time limit by default, so
  local matches will happily run code that dies on the ladder.

## Absolute-direction habits are bugs, and de-correlating builders wins games

Measured 2026-08-06 (strategy-log): removing every absolute-direction tie-break from the
starter lineage — full-ring spawn, randomised movement tie-break, randomised ore-tie choice,
shuffled build/heal scans — didn't just make the biased maps fair, it beat the
ring-spawn-only version **60.9% [54.8%, 66.7%]**. Fixed tie-breaks sent every builder to the
same first-enumerated target, colliding and shadowing each other; randomisation spreads them
for free. Corollaries:

- Any new logic that iterates tiles or directions in a fixed order and takes the first hit is
  suspect. Break ties randomly, or by an explicit seat-symmetric criterion.
- The arena's per-map **mirror seat split is the standing regression test** for this bug class.
- On 8×8, seat A wins ~4 in 5 no matter what we do (engine turn order, measured with a fully
  neutral bot). Small-map strategy should *assume* the seat, not fight it — and how the ladder
  assigns seats within a best-of-five is now a first-order platform question.

## Separation doctrine — everyone has AI loops; what actually differentiates

Assume every serious team runs LLM-assisted iteration (the organisers ship AGENTS.md — it's
the intended mode). The observed field still carries inherited starter bugs and ships
unmeasured versions by the dozen, so the differentiators are discipline-shaped, not
tool-shaped:

1. **Ratchet vs random walk.** A gated line only ever keeps true improvements; a vibes line
   accepts noise ~1 run in 6 and drifts. Weeks of compounding make this the primary edge —
   protect the gate above everything else.
2. **Private physics.** Every measured divergence from the published docs ((0,0) comms bug,
   spawn ring, delivery-only crediting, act-order economics, mislabeled symmetries, inert
   local CPU counter) is knowledge most teams don't have — because they trust the same docs
   we falsified. Keep probing exactly where everyone else trusts.
3. **Play the field distribution, not the abstract game.** Elo pays for beating the bots that
   exist. The starter lineage is the majority and its habits are predictable — inherited bugs
   are an exploit *class* (e.g. a corner-seated starter-lineage bot on jackpot delivers zero
   all game). Opponent dossiers + version tracking turn this into targeting data.
4. **Buy perishable advantages — automation makes them affordable.** The weekly map rotation
   expires map-specific work every Monday. Teams doing it by hand can't justify rebuilding
   opening books, per-map timing calendars, and tuned constants weekly; a pipeline can. The
   rotation is a moat FOR whoever automates recalibration, not against them.
5. **The human channel.** Replay-watching humans redirected our queue twice (rush meta,
   high-Elo scouting) — self-play can't see strategies nobody in the pool plays. Keep the
   human watching and the machine listening.

Corollary of 1+4: the variance that makes this game miserable to measure (identical bots
finishing 0-vs-10) is itself a moat — naive tuning chases noise and goes nowhere. Whoever
handles the statistics correctly gets to spend compute where others literally cannot.

## Borrowing from the RTS canon — what translates, and what doesn't

The 1306-rated ladder loss (2026-08-08, see opponents.md) was proxy-cannon-rush 101: static
weapons built in our base plus a worker body-blocking ours. Classic RTS theory maps well onto
this game — but every tactic must be re-derived from these mechanics, not imported on vibes.
Ranked by leverage-per-effort given where we are:

- **Scouting buys the timing information everything else needs.** Fog is real and vision
  radii are small (builder r²=20). One early builder pass toward the enemy Core costs only
  builder-rounds — zero titanium, zero scale tax — and converts "reactive defense" from a
  guess into a trigger. The field (starter-lineage) does not scout deliberately at all.
- **Wall-offs exist and nobody uses them.** Barriers: 3 Ti, +1% scale, block movement AND
  line of sight, and the starter lineage never builds one. Choke-blocking on the wally maps,
  and ring-adjacent placement against blocker builders, is the cheapest counter to everything
  we saw in that loss. (A barrier also blocks a Gunner's ray — though not a Sentinel's.)
- **Fixed facings make every contain leaky — theirs and ours.** Sentinels can never rotate.
  A sentinel contain has permanent blind angles: approach off-axis and it's furniture. The
  same discipline applies to our placement: cover chokes and harvest lines deliberately,
  don't just "face outward from the Core". This is *better* than StarCraft, where turrets turn.
- **Timing windows are computable per map.** The earliest possible enemy-sentinel-at-our-Core
  round is a function of Core separation and walk distance — an offline calculation per map.
  Defense triggers should key on that calendar and on scout sightings, not on our own
  harvester count (which is what the current bot does, and what the rush punished).
- **Worker harass economics we already derived:** heal (0.25 Ti/HP) beats chip damage, so
  sabotage only pays against undefended infrastructure — but the *threat* of harass forces
  the opponent to park healers, which is pure opportunity cost. One cheap menacing builder
  can tax an economy without ever firing.
- **The Launcher is mobility tech.** Throw range r²=26 moves a builder ~5 tiles in one
  action: fast expansion, surprise placement, and the clean answer to blocker builders
  (pick up an adjacent enemy builder — it works on either team — and yeet it).
- **What does NOT translate:** there is no unit micro (builders cannot attack units; turrets
  cannot move), so combat is placement geometry, not battles; there is no supply — the
  cost-scale tax is the real macro constraint and it has no StarCraft analog; and there is no
  detection layer or air. Import the strategic layer, never the tactical one.

## Underused API surface

Things the tutorials never touch, all plausibly worth exploiting:

- `can_fire_from()` / `get_attackable_tiles_from()` — **hypothetical** targeting. Evaluate
  where a turret *would* have line before spending 20–30 Ti on it. Turret placement is the
  most expensive irreversible decision we make; this makes it plannable.
- `Launcher.launch()` works on **enemy** Builder Bots — grab a saboteur that walks adjacent and
  throw it away. Also our own fast expansion: r²=26 is ~5 tiles in one action.
- `ct.destroy()` — reduces cost scale (above), and denies the enemy a healable target.
- Conveyors and Splitters are **bot-passable**, including the enemy's. Their logistics network
  is a highway into their base.
- `ct.rotate()` — a Gunner that re-aims is two turrets' coverage for 10 Ti.
- Splitter's spare sides = redundant delivery routes. One cut conveyor stops all income from
  that harvester; a second branch turns a cut into a throughput loss instead.
