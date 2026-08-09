# The r150 wall is ours, not the game's

**Research arm, 2026-08-09 (session 22).** Builder's priority question: *"is the
r150 conversion wall a fact about US or a fact about THE GAME?"*
**Answer: about us.** At the top of the ladder the kill hazard **accelerates**
through exactly the window where ours collapses.

**Version tag:** live **v89 "Eir 9c hivethaw (rollback)"** = `bots/_v100hf`,
md5 `9e85cae5`, tree hash `4558be91`; `team info` 1551.64 @ 489, rank #32.
**Corpus:** `corpus/league_matches.tsv` (27,073 unique ladder matches, the whole
league) → `corpus/league_games.tsv` (**3,705 games / 741 matches** between the
six teams at ≥1800 mean at-match rating). **Zero replay downloads**; both pulls
are the free `match list` / `match info` channel.

---

## 0. WHY THIS COULD NOT BE ASKED BEFORE

Every corpus this project has built was `--mine`. That is structural: we sit at
~1550 and never play the top tier, so "the field" has always meant *the 1500-1650
band that plays us*. **`fcode match list --team <id>` works for any of the 113
teams**, which makes the top tier's games against each other readable for the
first time. This document is the first measurement in the repo taken on a
population we are not part of.

## 1. THE TABLE

A core kill by **either** side, among games still alive at each band's start.
Identical measure on both populations.

| band | TOP-vs-TOP (n=3,705) | OUR GAMES (n=2,435) |
|---|---|---|
| r0-150 | 20.7% | **23.3%** |
| r150-200 | 18.7% | 10.3% |
| r200-300 | **38.0%** | 16.6% |
| r300+ | **70.2%** | 34.4% |

| | TOP-vs-TOP | OURS |
|---|---|---|
| games ending in a core kill | **88.1%** | 61.8% |
| median kill round | 229 | 198 |
| games reaching r1000 | **11.9%** | **37.2%** |

**Read row one first: our r0-150 hazard is HIGHER than the top tier's.** We are
more decisive than sporks-tier in the opening. Then at r150 we halve while they
hold, and from r200 they run away.

## 2. IT IS UNIFORM — not one team, not one map

| team | games | kill% | r200-300 hazard | reach r1000 |
|---|---|---|---|---|
| Pantheon | 1,525 | 90.3% | 40.4% | 9.7% |
| not adgato | 1,190 | 89.6% | 42.5% | 10.4% |
| Pivot | 1,505 | 87.0% | 36.9% | 13.0% |
| Jython | 1,465 | 87.7% | 34.2% | 12.3% |
| sporks | 1,425 | 84.1% | 32.8% | 15.9% |
| Clankers | 300 | 97.0% | 60.2% | 3.0% |

Every one of them sits between 32.8% and 60.2% in r200-300 against **our 16.6%**.
By map, top-tier kill rates run 78.2% (jackpot) to 95.4% (nordkap) — no map is a
grind map at the top. **hive, the map we have spent two sessions on, is 89.6%.**

## 3. THREE CONSEQUENCES

**1. Late conversion is available in this ruleset, and it is the main way games
end at the top.** Any doctrine that treats the late game as inherently
unconvertible is contradicted. This is the first positive field evidence for the
late-turret direction rather than a mere refutation of the alternative.

**2. Our "grind pocket" is a symptom, not a strategy.** We reach r1000 in 37.2%
of games; the top tier in 11.9%. The 58.2-58.5% win rate we have been protecting
in r1000 games is us being good at a state the best teams treat as a failure to
close. **A plank justified by "it improves our r1000 tiebreak position" is
optimising the consolation prize.** This does not argue for unshipping anything —
the grind is 26-49% of our games and real Elo — but it reframes "time is their
asset": the top tier does not let games get there at all.

**3. It sharpens the target.** The r200-300 gap against the top tier is
**38.0% vs 16.6%**, larger than the gap against the 1550+ band we have been
measuring. Whatever we build for that window should be scored against the top
tier's rate, not against the band that happens to play us.

## 4. THE CONFOUND, AND WHY THE SHAPE SURVIVES IT

**Top-vs-top has two strong teams; our games have at most one.** That inflates
their absolute hazard in every band and I cannot remove it from this table. A
reader who wants to discount the levels is entitled to.

What survives:
- **A strength confound raises a curve; it does not change its sign.** Theirs
  rises monotonically (20.7 → 18.7 → 38.0 → 70.2). Ours collapses at r150 and
  only partially recovers (23.3 → 10.3 → 16.6 → 34.4). Two different shapes, not
  two heights.
- **The r0-150 row is the internal control.** If we were simply weaker overall we
  would trail there too. We lead there.

Further limits: `turnsPlayed` on a `core_destroyed` game is taken as the kill
round. The ≥1800 cut is on **mean at-match `ratingBefore`** per team across the
league table, so a team hovering near 1800 could shift the membership slightly;
Clankers at n=300 is thin and should not be quoted alone. The league table itself
covers 2026-08-01 → 2026-08-09 and 71 teams appear in it (113 are ranked; the
remainder have no completed ladder matches in range).

## 5. WHAT I HAVE NOT DONE

This says the top tier converts late; it does **not** say how. The mechanism read
is `late-game-doctrine-2026-08-09.md`, and that one was measured against the
1550+ band **that plays us**, not against these six. Re-running the turret
production and placement census on top-tier replays would need replay downloads
— **we hold zero replays of any of these 3,705 games** — and that is the single
best use of a paced download budget on the board. Specified, not spent: the
builder owns that call.
