# The ammo gap, and three opponents with a compute fragility

**Research arm, 2026-08-09 (session 22).** From replay streams that had never
been read. **Version tag:** live **v89 "Eir 9c hivethaw (rollback)"** =
`bots/_v100hf`, md5 `9e85cae5`, tree hash `4558be91`; `team info` reports
**1551.64 @ 489** at time of writing (1524 @ 486 at my 06:41 boot).
**Corpus:** all 3,831 archived replays, `corpus/econ.tsv` (14,493 rows) joined
via `corpus/join.tsv` (reconciled 1,155/1,155). **Zero replay downloads.**

---

## 0. WHY THIS EXISTS

A field audit over 120 random archived replays found **eight Update streams that
no decoder in this repo had ever read**:

```
botOutput           1,077,308 events / 120 replays   <- execTimeUs + tled flag
setMoveCooldown       360,365
setActionCooldown     158,780
builderHeal            69,686
updatePlayers          55,378                        <- per-round Ti / ammo
distributeResources    49,440
coreConvertAmmo        25,196                        <- the whole ammo supply side
builderBuild           12,260
```

Two useful negatives from the same audit: **zero `indicatorLine`/`indicatorDot`
events** and **no non-empty `botOutput.stdout` anywhere in the sample**. No
opponent in this league leaks debug draws or prints. That intel route is closed;
nobody should go looking again.

---

## 1. **AN AMENDMENT TO MY OWN DELIVERABLE, PUBLISHED ONE HOUR EARLIER**

`late-game-doctrine-2026-08-09.md` §2 reported that in r200-300 we fire 5.8
turret shots per game against Ouroboros's 103, and framed the whole r200-300
deficit as **turret production**. Turrets fire from a global ammo pool with no
passive income, so "few shots" has two possible causes and I only tested one.
**Ammo is a genuine co-constraint and the deliverable overstated the production
half.**

Per game, r200-300:

| opponent | ammo converted THEM / US | titanium still held THEM / US |
|---|---|---|
| Ouroboros | **441.6 / 34.8** | 478.6 / **635.1** |
| Lunds Stallions | 300.9 / 53.0 | 115.8 / 300.9 |
| Powerpuff Girls | 294.3 / 41.0 | 317.6 / **603.7** |
| CtrlAltDefeat | 235.7 / 84.0 | 151.6 / 395.3 |
| Kings College Munich | 202.7 / 59.6 | 183.9 / 400.7 |
| Leviathan | 155.5 / 92.2 | 217.9 / 231.3 |

**We finish that window holding MORE titanium than they do and having bought a
twelfth as much ammunition.** Against Ouroboros: they convert 441.6 and end on
478 Ti; we convert 34.8 and sit on 635.

Pooled over the six, ammo converted per game by band:

```
r0-150     THEM 407.6   US 219.9   1.9x
r150-200   THEM 149.1   US  42.9   3.5x
r200-300   THEM 276.1   US  58.9   4.7x
r300+      THEM 1156.1  US 267.2   4.3x
```

**The divergence opens at r150 again** — now four instruments agree on that
boundary (conversion ratio, raider survival, turret production/placement, ammo
conversion).

**Corrected reading of the r200-300 shot deficit:** turret production is still
the larger term (~10x: 2.0 builds/game vs 0.2) and ammo the smaller (4.7x), but
both are real and **the ammo half is far cheaper to fix** — `convert_ammo` costs
no action cooldown and can be called the same turn. A turret with no ammo is a
30 Ti statue, and we are building statues on a 635 Ti bank.

This is the same banking pathology the counter-battery work has hit before
("we bank 1,165-8,093 Ti unspent"), measured for the first time on the ammo
channel specifically.

## 2. **THREE OPPONENTS HAVE A COMPUTE FRAGILITY. WE HAVE NONE.**

`botOutput` carries `tled` (the engine's own flag for "this unit exceeded its
10 ms and its turn was discarded") and `execTimeUs`, **for both teams, every
unit, every round**. Across all archived games with a resolved opponent:

| team | games | their TLE'd turns | their total turns | **TLE rate** |
|---|---|---|---|---|
| The Bisons | 20 | 864 | 18,591 | **4.65%** |
| Leviathan | 70 | 6,457 | 146,890 | **4.40%** |
| Ouroboros | 85 | 26,356 | 744,333 | **3.54%** |
| Lunds Stallions | 115 | 4,522 | 530,254 | 0.85% |
| Coreflood | 10 | 168 | 63,109 | 0.27% |
| OopsGotYourElo | 75 | 529 | 607,921 | 0.09% |
| *23 other teams incl. sporks-tier* | — | 0 | — | **0.00%** |
| **OpenSverige (us)** | — | ~0 | — | **0.00%** |

**Ouroboros — the team that destroys our core more often than any other in
r200-300 (22 kills, 18.0% of games alive at r200) — discards 26,356 unit-turns
across 85 games and beats us anyway.**

**The distribution is the finding, not the mean.** For Ouroboros:

```
games with any TLE:  37 of 85  (44%)
TLE per game:        median 0   mean 310   max 3,508
```

This is **not** a bot that is uniformly slow. It is a bot with a **conditional
blow-up**: nothing in most games, then a state arrives and it loses hundreds to
thousands of unit-turns. That is the most exploitable shape a weakness can have,
and it is Magnus's play-the-players mandate in its purest form.

**WHAT I HAVE NOT DONE, and it is the whole value of this:** I have not
identified the trigger. The obvious candidates are entity-count scaling (their
per-unit scan is O(entities) and our unit count crosses a threshold), pathfinding
blow-ups when routes are blocked, or vision-set size. **`corpus/econ.tsv` already
carries per-band `cpu_sum_us`, `cpu_max_us` and `turns_run`, so the trigger is
findable by correlating their per-round CPU against observable game state in the
same replays — no new data needed.** That is the highest-value open item I have.

Our own 0.00% is worth reading twice: it means **we are leaving compute on the
table.** Mean CPU is 642-1,123 µs/turn against a 10,000 µs budget — under 12%.
Every "this is too expensive to compute" decision in our bot should be re-asked.

## 3. LIMITS

- Attribution comes from `join.tsv` (1,165 of 3,831 archived files map to one of
  our ladder games). Per-opponent coverage is 5-115 archived games; rows with
  <5 games are shown but should not be leaned on.
- Team attribution for `botOutput` needs the unit to have appeared in a
  `placeEntity`. **The Core is never placed as an entity, so core turns are
  excluded from both teams' totals** — an equal-handed undercount, but it means
  these are *builder-and-turret* turn counts, not all turns.
- `ti_end`/`ammo_end` are the last `updatePlayers` value seen inside each band,
  not a band average.
- Everything here is measured **against us**. The league-wide pull now running
  (`tools/corpus/league_matches.py`) will say whether Ouroboros also blows up
  against the top tier, which would separate "our states trigger it" from "their
  bot is just fragile". **Until that lands, do not read the 44% as ours to
  induce.**
