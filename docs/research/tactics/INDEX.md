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
| 1 | Battlecode postmortems: late-game conversion, breaking stalemates | **in flight** | 2026-08-09 | — |
| 2 | Cross-league trickster/asymmetric play (steering deterministic opponents, denial, baiting, body-blocking, tiebreak manipulation) | **in flight** | 2026-08-09 | — |
| 3 | Engine/rule-edge exploits + post-hoc rule patches (best index of what worked) | **in flight** | 2026-08-09 | — |
| 4 | CPU/time-limit exploitation — inducing opponent timeouts | unswept | — | — |
| 5 | Turret/tower placement doctrine and advancing a firing line (tower-defence + RTS theory) | unswept | — | — |
| 6 | Cost-inflation attacks (making the opponent's buildings dearer) | unswept | — | — |
| 7 | Limited-bandwidth team coordination (our 16 ints) — patterns from Halite/Ants | unswept | — | — |
| 8 | Economy: harvest saturation, expansion timing, when to stop expanding | unswept | — | — |
| 9 | Opening theory and build-order steering in symmetric-map games | unswept | — | — |
| 10 | Endgame/tiebreak play when the win condition is a score, not a kill | unswept | — | — |
| 11 | Anti-rush and defensive-line theory (what makes a line hold) | unswept | — | — |
| 12 | Unit-displacement mechanics elsewhere (our launcher throws EITHER team's bots) | unswept | — | — |

**Why topic 4 is not merely academic:** we measured (2026-08-09,
`docs/research/ammo-and-cpu-2026-08-09.md`) that Ouroboros discards **26,356
unit-turns across 85 games** — median 0 per game, mean 310, **max 3,508**, firing
in 44% of games. Leviathan 4.40%, The Bisons 4.65%. Every 1800+ team and we
ourselves sit at 0.00%. A conditional compute blow-up in three opponents is the
most exploitable shape a weakness can have, and we do not yet know the trigger.

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
