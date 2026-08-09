# Tactics library — ideas mined from comparable games, for the builder

**Standing mandate (Magnus, 2026-08-09):** the research arm is permanently
data-hungry and continuously mines strategies, tactics and ideas from comparable
games, converting them into things the builder can use. Boot instructions live in
`.claude/commands/research.md`. **Subagents are pre-authorised — no per-session
permission needed.**

This index exists so successive sessions **do not re-research the same ground.**
Update it in the same commit as any findings.

## How a sweep runs

1. Pick the next **unswept** or **stale** row from the wheel below.
2. Launch a background subagent (or several narrow ones) with an explicit brief:
   the ruleset summary, the question, and the demand for sources.
3. When it returns, write one file per usable tactic into this directory, mark
   the wheel row, and **relay to the builder** — subagent results die with the
   session.

Sweeps run **at boot**, **whenever the queue drains** (watch state is a sweep,
never an idle), and **after any measured surprise** that contradicts doctrine.

## File format

```markdown
---
tactic: <short name>
source: <URL>
origin: <competition / year / team, or "RTS theory">
evidence: documented | anecdotal | inference
transfers: yes | partial | no
---
WHAT IT IS — two or three sentences.
WHY IT MIGHT TRANSFER — against OUR ruleset specifically.
WHAT WOULD KILL IT — the rule or measurement that makes it inapplicable here.
BUILDER HOOK — the smallest thing that would test it, or "none yet".
```

**Rules.** Never invent a tactic or attribute one to a team that did not use it.
An untransferable tactic recorded as `transfers: no` **is a useful result** and
should be filed, not discarded — it stops the next session chasing it. A
plausible-sounding tactic with no source is pollution; mark it
`evidence: inference` and say whose inference.

## Our ruleset, for briefing subagents

Two teams, symmetric grid 8x8..30x30. Core 500 HP / 2x2. Builder bots (40 HP, the
only mobile unit; build/attack/heal/destroy on an orthogonally adjacent tile).
Turrets: gunner r²=13 dmg 7 / 4 ammo; sentinel r²=32 dmg 18, **ignores obstacles**
/ 10 ammo; launcher r²=26, throws a builder bot **from either team** to a passable
tile. One resource (titanium), moved physically by conveyors/splitters/harvesters
into the core; **core converts titanium→ammo 1:1, no passive ammo income**.
Build costs **scale up** per category as you build more. 16-slot integer team
comms store, writes visible next round. 1000 rounds; win by core kill, else
tiebreak on titanium delivered → harvesters alive → titanium stored. **10 ms CPU
per unit per turn; exceeding it silently discards that unit's turn.** An uncaught
exception permanently destroys that unit for the match.

## The wheel

| # | topic | status | swept | files |
|---|---|---|---|---|
| 1 | Battlecode postmortems: late-game conversion, breaking stalemates | **SWEPT** — 23 official PDFs 2019-2026 read in full. **Produced the heal-arithmetic finding.** | 2026-08-09 | [heal-arithmetic](../heal-arithmetic-2026-08-09.md), [sweep 1](2026-08-09-sweep-1.md) |
| 2 | Cross-league trickster/asymmetric play (steering deterministic opponents, denial, baiting, body-blocking, tiebreak manipulation) | **SWEPT** | 2026-08-09 | [sweep 1](2026-08-09-sweep-1.md), [spawn-smothering](spawn-smothering.md), [ore-tile-denial](ore-tile-denial.md), [ammo-drain-baiting](ammo-drain-baiting.md), [destroy-rebuild](destroy-rebuild-converter.md) |
| 3 | Engine/rule-edge exploits + post-hoc rule patches (best index of what worked) | **SWEPT** (8 Battlecode postmortem PDFs read in full) | 2026-08-09 | [sweep 1](2026-08-09-sweep-1.md) §3, §6 |
| 4 | CPU/time-limit exploitation — inducing opponent timeouts | **SWEPT.** Effect is real & tournament-deciding (StarCraft natural experiment); deliberate induction **BANNED BY NAME in BASIL and SC2 AI Arena** — held pending an organiser ruling | 2026-08-09 | [cpu-timeout-induction](cpu-timeout-induction.md) |
| 5 | Turret/tower placement doctrine and advancing a firing line | **SWEPT**, then **RE-AIMED** at the measured turret-survival flip. Its leading hypothesis (survival = avoidance) is **falsified by our own data**; its subsidiary findings are the most buildable material any sweep has produced — **the ablative barrier screen is ~8× HP/Ti and is SENTINEL-ONLY** | 2026-08-09 | [lanchester-commit-gate](lanchester-commit-gate.md), [sweep 1](2026-08-09-sweep-1.md), [sweep 7](2026-08-09-sweep-7.md) |
| 6 | Cost-inflation attacks (making the opponent's buildings dearer) | **SWEPT** — and inverted: killing an enemy builder REFUNDS their scale; imprison instead | 2026-08-09 | [exchange-rates](../exchange-rates-2026-08-09.md) §6 |
| 7 | Limited-bandwidth team coordination (our 16 ints) | **SWEPT** — 15 BC postmortems 2019-2026. **Produced a probe that found a latent bug**: the read-increment-write ticket idiom collapses silently under our buffered store, and `SLOT_ROLE_N` is safe only because the core spawns ≤1 builder/turn | 2026-08-09 | [sweep 5](2026-08-09-sweep-5.md), [store semantics](../store-semantics-2026-08-09.md) |
| 8 | Economy: harvest saturation, expansion timing, when to stop expanding | **SWEPT** — and it turned into a negative: **cost scaling never binds on harvesters** (break-even beyond any map's ore supply under both readings); it binds on the **+20% categories**. The corpus hooks then showed **the economy is not our constraint at all** | 2026-08-09 | [sweep 4](2026-08-09-sweep-4.md), [middle-game hazard](../middle-game-hazard-and-economy-2026-08-09.md) |
| 9 | Opening theory and build-order steering in symmetric-map games | **SWEPT** — **our constant is DEFENSIBLE** (fixed openings are the league norm; the anti-constant result needs cross-game memory the engine forbids). **The one qualification — an opening unconditional on MAP GEOMETRY — is a documented failure mode, and our own width gradient is it.** | 2026-08-09 | [sweep 6](2026-08-09-sweep-6.md) |
| 10 | Endgame/tiebreak play when the win condition is a score, not a kill | **SWEPT** (BC 2019 do-nothing, BC 2022 one-gold, Halite endgame flag, Spring'21 score+banked/3) | 2026-08-09 | [sweep 1](2026-08-09-sweep-1.md) §4 |
| 11 | Anti-rush and defensive-line theory — **re-aimed at "how does anyone break a 2.2:1 defensive edge?"** | **SWEPT** — 8 BC postmortem PDFs read in full + Screeps/Terminal/RTS theory. **Answer: mostly you don't, you win on economy; every league converged there independently.** | 2026-08-09 | [sweep 2](2026-08-09-sweep-2.md), [sentinel-file](sentinel-file-stacking.md) |
| 12 | Unit-displacement mechanics elsewhere (our launcher throws EITHER team's bots) | **SWEPT — and it INVERTS our current use.** BC2020's Delivery Drone has our Launcher's exact verb signature; that field converged on grabbing the **enemy's** unit defensively, never on ferrying their own forward | 2026-08-09 | [sweep 3](2026-08-09-sweep-3.md), [defensive-interception](launcher-defensive-interception.md), [displace-dont-kill](displace-dont-kill.md), [throw-into-prebuilt-cell](throw-into-prebuilt-cell.md) |

**Why topic 4 is not merely academic:** we measured (2026-08-09,
`docs/research/ammo-and-cpu-2026-08-09.md`) that Ouroboros discards **26,356
unit-turns across 85 games** — median 0 per game, mean 310, **max 3,508**, firing
in 44% of games. Leviathan 4.40%, The Bisons 4.65%. Every 1800+ team and we
ourselves sit at 0.00%. A conditional compute blow-up in three opponents is the
most exploitable shape a weakness can have, and we do not yet know the trigger.

**THE WHEEL IS NOW FULLY SWEPT (all 12 topics, 2026-08-09).** Successive sessions
should re-sweep STALE rows rather than pick unswept ones — and prefer re-aiming a
topic at a specific measured surprise, which is what produced the best results here
(topic 11 re-aimed at the 2.2:1 edge; topic 9 re-aimed at "our opening is a
constant").

## Model rule for sweeps

**Every subagent gets an explicit `model:` — `opus` or `sonnet`, never `fable`,
never omitted** (Magnus 2026-08-09, restating the 2026-08-08 s18 directive after
it drifted a second time). Sonnet for mechanical sweeps with a validated method;
Opus for anything that must grade its own sources — which is most tactics work,
since the whole value is in the evidence labels.

## Standing context a sweep should know

- **The field does not rush.** Only 12% of top-tier kills land by r100; median
  kill round r296.
- **Everything about us breaks at r150.** Five independent instruments agree:
  conversion ratio, raider survival (43→6 rounds), turret production, forward
  placement, ammo conversion.
- **Late offensive insertion is refuted for us** (`late-game-doctrine-2026-08-09.md`):
  2.34% of forward throws at r200+ ever land a single attack on the enemy core.
- **We bank and do not spend.** We end r200-300 holding more titanium than
  Ouroboros while buying a twelfth as much ammunition.
- **THE UNIFYING FACT (2026-08-09, `heal-arithmetic-2026-08-09.md`): healing is
  4.00 HP/Ti and the best damage source is 1.80 HP/Ti, so the defender wins any
  titanium-symmetric attrition race 2.2:1 — and builder attacks cannot touch
  enemy BUILDERS, so only turrets clear a healing screen.** We run a
  damage-to-repair ratio of 1.11:1 against the field's 2.79:1. Every sweep
  should be read against this: the question is never "how do we do more damage"
  but "how does anyone break a 2.2:1 defensive edge".
  **AMENDED 2026-08-09 (s23), from engine source:** one heal repairs *both* a
  friendly builder bot and a friendly building on the same tile for 1 Ti, and a
  bot may co-occupy only a **conveyor, splitter, or the allied core**. So the
  stack caps at 2 entities = **8.00 HP/Ti → 4.4:1 on a stacked tile**, and the
  load-bearing case is **a builder standing on a core footprint tile.** The
  defender's edge is larger than the headline, not smaller.
- **THE ANSWER TO THE STANDING QUESTION, from sweep 2:** *mostly you don't break
  it — you win on economy.* Every league swept converged there independently, and
  each one that reached a defence-dominant equilibrium was rescued by **a clock,
  not a tactic.** Our clock is round 1000 and our first tiebreak key is
  cumulative titanium delivered. **The crack that does exist is that our
  defender's heal is adjacency-capped at ~16 HP/round per tile while the
  attacker's damage on that tile is capped only by titanium** — concentration,
  not more damage.
- **MEASURED ENGINE FACTS (2026-08-09, s23 probes — stop assuming these).**
  **Store**: writes are buffered to next round; **last writer wins**; the
  read-increment-write ticket idiom **collapses silently** (5 writers → counter +1,
  all five believe they are unit #0); slot range is **unsigned 32-bit `[0, 2³²−1]`
  and a negative write RAISES**, which permanently destroys the unit.
  **Turret lines**: a **gunner** line is blocked by our own bots and buildings; a
  **sentinel** line passes through them (18 dmg landed through a friendly bot *and*
  a friendly barrier). `get_attackable_tiles()` **ignores occupancy** and reports
  the target as attackable in both cases.
  **Build legality** is strictly stronger than `is_tile_empty`; **spawn ring is the
  12-tile Chebyshev-1 ring** (`CORE_SPAWNING_RADIUS_SQ = 2`, not the r²=8 action
  radius).
- **THE MIDDLE GAME IS THE TARGET, NOT THE ECONOMY (2026-08-09, s23).** Conditional
  on a core kill, the chance it is **ours** rises monotonically **29% → 55% → 72% →
  76%** across r0-150 / r151-300 / r301-600 / r601-999 — but **353 games reached
  r1000 and we won 57.2%**. We win the opening and we win the clock; we die in the
  middle. **`disengage and out-economy` (sweep 2) is REFUTED as a change**: paired,
  we already out-build the field on conveyors (+13) and under-build turrets (−3,
  leading in only 20.1% of games). It is our status quo, not a lever.
- **METHOD WARNING from the same work: our opening is a near-constant** — r0-150
  build medians are *identical* in wins and losses; all the variance is the
  opponent's. **A paired differential whose variance lives on the other side of the
  subtraction is an opponent thermometer, not a strategy dial.**
- **THE FORWARD ROAD IS CLOSED (builder, 2026-08-09 09:05)** on three
  instruments, and sweep 3 corroborates it from an independent evidence path.
  Research amended the magnitude of one of those instruments — see
  [`loki3-anchor-and-fargun-recheck`](../loki3-anchor-and-fargun-recheck-2026-08-09.md)
  — without disturbing the verdict. **Home defence is the measured asset**
  (+11.4 / +16.6 / +22.3pp over the field), and the launcher tactics above are
  the ones that reinforce it rather than opening a sixth doctrine road.
