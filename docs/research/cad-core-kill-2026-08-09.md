# The CAD mechanism: a two-piece core siege that out-produces our clearance, and it is map-conditional

**Side lane, 2026-08-09 13:32 CEST, on the builder's ASK (their spec: what
applies damage in the terminal window and from where; do our core-kill wins
differ; are the tiebreak losses the same shape; stratify by map and
round-of-core-death, NOT their version). Corpus-scale read — zero replay
downloads, zero deep reads needed: the regenerated decoder tables answered
everything.**

**Version tag:** live v92 (holder at 1534 @ 526 per builder, mid-read);
analysis spans our v55→v83 vs CAD 107-120 — version-invariance on both
sides is the established premise (revert-brackets doc), so no version cut.
Data: 75 attributed CAD-vs-us replays already in `replay_archive/`, decoded
via the preserved side-lane decoders (dc reconciles at exactly 20,929
league-wide deaths; 0 errors). One decoder defect found and fixed en route
(§ methods).

## The mechanism, in one paragraph

CAD kills our core with **turret fire and nothing else — 99.8% of the
124,168 HP of damage our core took across 75 games is gunner/sentinel
shots (builder attacks: 0.2%)**. The weapon is two-piece: **point-blank
gunners planted against our core** (189 core-shooting gunners, 100% inside
our home band, shots-weighted median d² = 5, planted from median r172) plus
**stand-off sentinels** (144, shots-weighted median d² = 26, 28% planted
OUTSIDE our home band — beyond any gunner answer, ignoring obstacles),
arriving later (median r261) and carrying **65% of the damage**
(80,766 HP vs 43,190). Median 4 core-shooting turrets per game; the top
tile carries ~49% of a game's core shots. Our core dies at **median r361**
(p25 r256, p75 r558) — mid-game grind, exactly as the builder's
turns-based read predicted.

## Why we lose it: a replacement-rate war, and we lose the production race

The clearance table is the discriminator (all 333 core-shooting turrets,
survivorship-corrected — see methods):

| outcome | games | core-shooters/game | core shots/game | we killed | median lifetime of killed |
| --- | ---: | ---: | ---: | ---: | ---: |
| our core dies | 47 | 5.6 | 186 | **49%** | 9 rounds |
| tiebreak | 17 | 2.9 | 93 | 82% | 24 |
| their core dies | 11 | 1.9 | 30 | 90% | 47 |

Read it with the lifetime column: **in losses we kill their plants FAST
(9-round median) and still lose, because they arrive at 5.6/game and half
survive anyway.** We do not fail to fight; we fail to out-produce. The
heal race says the same: in losses our core heals back only **0.76** of
incoming damage (2,117 dmg/game vs 1,613 heal); in tiebreaks **0.98**; in
wins 1.00. The core dies when sustained turret DPS exceeds the 4 HP/Ti
heal channel's throughput — an economy contest at the core tile.

## The map split is close to binary (builder's stratum #1)

62/75 games join unambiguously to `ladder_games` for a map label:

- **~100% core-death maps:** heart (7/7), archipelago (7/7), drumlin (6/6),
  saga (4/4), snowflake, jackpot, nordkap, hive (3/3 each), atoll (2/2),
  eider (4/5).
- **We survive:** fjordgate (0/2), moonrise (1/5), antler (1/4),
  lighthouse (1/4), meander (2/4).

Cell sizes are 2-7 — individually weak, but the pattern is 9 maps at
~always vs 5 maps at ~rarely, which is not a coin-flip shape. Hypothesis
worth one code/map read (NOT settled here): the survive-maps are the ones
where terrain or distance breaks the stand-off sentinel line to our core.
**This is the builder's cheapest lever if it holds: the fight is decided
by map class, so a map-conditional defence posture prices at 9 maps' worth
of the CAD bleed, and per the turret-mix doc map width already predicts
turret mix league-wide.**

## Our own wins are the same weapon, used earlier (builder's question #2)

Mirror read, games where THEIR core dies (n=11, median death r217 — 144
rounds earlier than theirs): **28 of our 35 core-shooting turrets are
gunners at median d² = 10 to their core, planted from median r125, 56 core
shots/game.** Same two-piece shape, gunner-heavy, ~50 rounds earlier than
CAD's plants. The matchup is a race between two versions of the same
siege; whoever's plants land first wins. We win it 11 times of 75 in this
set — when our early aggression lands before their economy scales.

## The tiebreak games are absorbed sieges, not absent ones (question #3)

Tiebreak games still see 93 CAD core shots/game (half the loss-rate
intensity, triple the win-rate), and **almost every tiebreak game ends
with our core healed to full 500 HP** — when the siege fails, it fails
completely. The `(match, turns)` join cannot separate individual tiebreak
games (they all run exactly 1000 turns — a structural join limit, noted),
but the one verified tiebreak LOSS (antler) absorbed 107 core shots, ended
at 500 HP, and lost on titanium anyway: **the siege's second win path is
economic — even a fully-healed siege taxes the heal channel and the
defence enough to lose the collection race.** n=1 verified, labelled as
such; the 80% tiebreak win rate (builder's count) says this path is the
minority one.

## What this changes

1. **The version-invariance puzzle is resolved mechanically.** A two-piece
   core siege is chassis behaviour, not a tuning constant — it survives
   their churn and ours. Builder-death instruments never saw it because
   builders are not the target.
2. **"Cover the ≥5-kill tiles" logic does not transfer to this problem.**
   The gunner half is point-blank (d²≤9 for three-quarters of shots) —
   spawn-adjacent barriers/arcs might contest it — but the sentinel half
   (65% of damage, 28% planted outside our band, obstacle-ignoring) is
   untouchable by tile denial in our band. Any response has to price BOTH
   pieces or it re-runs the SITE/ESCALATE lesson.
3. **The heal channel is the measured bottleneck** (0.76 vs 0.98 heal/dmg
   is the loss/survive line). Whether the answer is more heal throughput,
   earlier clearance, or out-racing them to their core (our own wins say
   the last one works 15% of the time as-is) is a build question — with
   the standing caveat that "divert economy to defence" is refuted at
   −7.8pp and any response must name what it PRODUCES.
4. **Next cheapest evidence, in order:** (a) the map-class hypothesis — a
   terrain read of the 5 survive-maps vs the 9 death-maps against the
   sentinel stand-off geometry (free, corpus + map files); (b) per-round
   heal-throughput ceiling arithmetic vs measured CAD DPS curves (free,
   rule arithmetic — S1 before anything); (c) only then a build.

## Methods & provenance

Pipeline: `attrib.tsv` join (75 files) → preserved decoders
(`dc_decode`/`rx_decode`/`bb_decode`, 2,735 files 0 errors, dc_deaths
reconciles at exactly 20,929 rows against the published attribution) →
three analysis passes (scripts in session scratchpad `cadpass/`).
Reconciliation that carries the damage claims: turret damage computed from
shot counts × nominal damage (124.0k) matches the independent HP-ledger
total (124.2k) to **0.2%**.

**Decoder defect found and fixed en route:** `rx_decode.py`'s shooter
table emits x=−1 for any turret destroyed before game end (`pos_of.pop`
on removeEntity) — 57% of core-shooting turrets, a survivorship bias that
had inflated the survivor-only geometry. Fixed in a scratchpad COPY
(`pos_ever` dict; the validated original in
`docs/research/scripts/side-lane-2026-08-09/` is untouched); regression
check: all 745 survivor tiles byte-identical between old and fixed runs,
0 mismatches, 0 residual x=−1, and the fixed join covers 333/333 shooters
with shot totals matching the independent rx_shot aggregate exactly.
**If the research arm productises these decoders, this fix should travel —
flagged to both arms.**

Limits: 75 of ~100 CAD games are attributed+archived (the missing 25 are
unarchived, not excluded by choice); tiebreak-game won/lost labels join
ambiguously (all-1000-turn games), so §tiebreak leans on the builder's
match-level 16-4 count; map cells are n=2-7; "d2_enemy" plant distances
come from `corpus/builds.tsv` and inherit its validation, not re-derived
here.
