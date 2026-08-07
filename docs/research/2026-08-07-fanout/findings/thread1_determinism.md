# Thread 1: Determinism Falsifier — findings (2026-08-07)

Scope: prove/disprove that identical (opponent, opponent version, map, our version,
our seat) pairings produce byte-identical replays across different `mapSeed`s, and
quantify how much of our 1160-game rated history is "re-lost" identical pairings.

All match ids below are full UUIDs unless truncated to an 8-char prefix for
readability (full ids are in `all_games_flat.json` and in the per-pair diff
output saved under `scratchpad/`).

### Definitions (for the build verdict)

- **Fingerprint** = the tuple `(turnsPlayed, winCondition, winnerId)` as recorded
  per game in `all_games_flat.json`: `turns` = `turnsPlayed`, `wincond` =
  `winCondition`, and `we_won` = `winnerId` resolved against `our_seat` (i.e.
  `we_won == (winnerId == our_seat)`). Two games are counted as
  fingerprint-identical iff all three match exactly.
- **Grouping key (STRICT)** = `(opp_name, opp_ver, map, our_ver, our_seat)`.
  By construction of this key, **`our_ver`, `opp_ver`, and `our_seat` are held
  constant across every member of a STRICT-key group** — i.e. both teams are
  running the identical two code versions and sitting in the identical seats in
  every game inside one group; the only thing that varies between members is
  `mapSeed` (and, trivially, `match`/`game` id). The LOOSE key in section 2
  deliberately drops `our_ver` and `our_seat` to test what happens when that
  constraint is relaxed.

### HEADLINE PROOF — verbatim, for the tape

**Round-by-round-confirmed identical pair:** match
`d0116d59-75ca-47bb-9be2-517d66c0e585` game **5** vs match
`89114461-4764-4636-bcac-6526e9bfcd3c` game **5** (Ouroboros oppv8, atoll,
ourv53, seatB; seeds 583862984 vs 84925165) — **227/227 rounds byte-identical**
across builds, moves, deaths, HP deltas, turret fires, builder actions,
`convertAmmo`, and resource moves, on identical map terrain, ending in the same
`core_destroyed` loss both times. Full detail and two more independently
confirmed identical pairs (194/194 rounds, 805/805 rounds) below.

## 1. Replay-level proof (6 required downloads + 2 extra)

Diff method: decoded every round's full event stream (builds, moves, deaths,
HP deltas, turret fires, builder attack/heal/build, `convertAmmo`, resource
moves) with `toolkit/replay_lib.py`, plus map terrain/tiles/wall/ore/core
layout, and compared round-by-round.

Checked the passive replay archive at
`/Users/junghard/Projects/Work/florent-code-game/replay_archive/manifest.json`
before downloading: it holds only 8 archived matches, none of which overlap
this thread's 8 target match ids (6 required + 2 extra), so every replay used
below was pulled fresh through the shared `CACHE` download path (paced, 4s
between real downloads) and cached at
`scratchpad/replay_cache/replays/<match>_g<n>.replay26` for reuse by other
threads.

### Pair A — Ouroboros oppv8, atoll, ourv53, seatB
`d0116d59-75ca-47bb-9be2-517d66c0e585` g5 (seed 583862984) vs
`89114461-4764-4636-bcac-6526e9bfcd3c` g5 (seed 84925165)

- Map/terrain: **identical** (18x18, same tiles/walls/ore/core positions) despite different seeds.
- Event stream: **IDENTICAL across all 227 rounds.** Every build, move, death, HP
  delta, fire, builder action, and resource move matches exactly, round for round.
- Outcome: both `core_destroyed` losses (winner=A, i.e. we lost as seatB), verdict
  matches metadata fingerprint exactly.

### Pair B — Lunds Stallions oppv41, hive, ourv53, seatA
`b17d5862-6283-4b51-a6d8-1f8a1d566635` g4 (seed 1465256372) vs
`2b00ef7c-b6fd-42c9-b046-1efd8fedc486` g5 (seed 1520846410)

- Map/terrain: **identical** (25x25, same layout) despite different seeds.
- Event stream: **IDENTICAL across all 194 rounds.**
- Outcome: both `core_destroyed` losses (winner=B), matches metadata.

### Pair C — Team 48 oppv16, lighthouse, ourv53, seatA
`dcfe2cf0-1a8e-4260-ad78-c2df8b9c78c9` g3 (seed 852537909) vs
`8ce1c0d9-eeeb-4c84-b2f4-2329d19e31cd` g2 (seed 1976190642)

- Map/terrain: **identical** (16x16) despite different seeds.
- Event stream: **IDENTICAL across all 805 rounds.**
- Outcome: both `core_destroyed` wins (winner=A), matches metadata.

**Verdict on the 3 required pairs: all IDENTICAL, full length, every decoded event
category.** `mapSeed` had zero observable effect in these three cases — same map
name -> same terrain, same opponent code + same our code + same seat -> same
outcome down to the individual entity ID, HP delta, and resource-stack hop. This
directly confirms the metadata-only hypothesis: these are not "coincidentally
similar" games, they are the *same game* replayed under a different seed label.

### Extra check (2 of the 2 allowed extra downloads) — the flagged Ouroboros drumlin group

The brief flagged `('Ouroboros', 8, 'drumlin', 53, 'B')` as a strict-key group
where the fingerprint (turns/wincond) *differs* across its 3 members
(1000t/titanium_collected, 528t/core_destroyed, 427t/core_destroyed — all
losses). I downloaded the two closer members to see where they part ways:

`d0116d59-75ca-47bb-9be2-517d66c0e585` g3 (seed 1886099049, 528t, core_destroyed)
vs `89114461-4764-4636-bcac-6526e9bfcd3c` g1 (seed 249458595, 427t, core_destroyed)

- Map/terrain: **identical** (25x25) — same as every other pair checked.
- Builds/moves/deaths/HP/fires/builder-actions/convert_ammo: **byte-identical
  through round 62.**
- **First divergence: round 63**, and it is *not* a bot decision — it's a
  resource-routing tie. At round 63 a team-A harvester (`#189`, built that same
  round at `(12,10)`) produces its first titanium stack. That tile has **two**
  valid adjacent conveyor acceptors: a team-A conveyor facing NORTH at `(12,9)`
  (built round 31) and a team-B conveyor facing EAST at `(12,11)` (built round
  47, i.e. an opposing conveyor sitting adjacent to our harvester — a live
  instance of the "push resources onto the opponent's network" case called out
  in CLAUDE.md). In the 528-turn game the stack routes south into the *enemy's*
  network `(12,10)->(12,11)`; in the 427-turn game it routes north into *our
  own* network `(12,10)->(12,9)`. No bot action differed to cause this — the two
  outcomes are a straight coin-flip on which adjacent acceptor wins the tie.
- This single routing fork **cascades**: every subsequent round's
  `resource_moves` differs (checked rounds 63-79, all differ), and by **round
  104** the divergence has propagated into actual bot behavior — builds, moves,
  HP, fires, builder actions start differing too (because our own bot reacts to
  its resource state). That snowball is consistent with the two games ending
  99 rounds apart (528 vs 427) at the same qualitative outcome (core destroyed,
  loss).

**Implication:** the engine is deterministic given (map, our code, opponent
code, seat) *except* at genuine N-way ties in resource routing, where the choice
is evidently seed-sensitive (or at least not a pure function of anything visible
in the decoded stream up to that point). This is rare — it requires a specific
board geometry where a harvester/conveyor has more than one valid acceptor
adjacent at once — which is why the three "always-identical" pairs above never
hit it, but drumlin's board does. This is a genuinely different mechanism from
what the "decision-noise injection" fix targets (bot-side randomization); it's
an engine-side tie-break. It doesn't weaken the main finding — 43/48 strict-key
multi-groups (89.6%) show zero such forks across their full length — but it
explains why a handful of groups (the 5 "diverging" ones below) don't reproduce
cleanly, and it's a mechanism worth knowing about if the decision-noise fix is
being reasoned about precisely.

## 2. Prize-pool accounting (all 1160 rated games, no downloads)

Ordering: `completed` timestamp per match (all 5 games of a match share one
timestamp) tie-broken by `(match, game)`; 232 matches x 5 games = 1160, clean.

**STRICT key** = (opp_name, opp_ver, map, our_ver, our_seat). **fingerprint** =
(turns, wincond, we_won).

- Multi-member groups (size >= 2): **48 groups / 103 games** (matches the
  pre-established number exactly).
- **Re-pair rate** (any game that repeats an earlier same-strict-key matchup,
  regardless of fingerprint): **55 / 1160 = 4.74%**.
- **Identical-fingerprint repeat games**: **48** (i.e. of the 103 games in
  multi-groups, 48 are chronologically-later repeats whose fingerprint exactly
  matches an earlier game in the same group) — of which **19 are LOSSES**, 29
  are wins.
  - All-agree groups (every member of the group shares one fingerprint): **43
    groups / 91 games** (91 - 43 = 48, consistent).
  - Full per-group breakdown is in the script output; largest contributors to
    the 19 re-lost games: Ouroboros/atoll/B (4 games, 3 repeats, all losses),
    Lunds Stallions/hive/A (3 games, 2 repeats, all losses), plus 17 other
    2-game groups contributing 1 repeat-loss each.
- **Elo projection**: 19 re-lost identical-fingerprint games x ~3.2 Elo/coinflip
  = **~60.8 Elo** already left on the table historically by not converting these
  to coin flips. Forward-looking, at the observed 4.74% strict re-pair rate with
  ~39.6% of repeats historically being losses (19/48), each additional game
  played contributes on the order of 4.74% x 39.6% x 3.2 ~= **0.06 Elo/game
  expected value** if the fix isn't applied — i.e. roughly 6 Elo per 100 games
  going forward, while our_ver and the opponent pool stay static. This is a
  lower bound: the retrospective 4.74% is suppressed by version churn (our_ver
  is part of the strict key and changed often across these 1160 games); during
  any stretch where our submitted version is genuinely static, the same-key
  recurrence rate should run higher than 4.74%.

**LOOSE key** = (opp_name, opp_ver, map), ignoring our_ver and our_seat —
reported separately, and interpreted carefully (see caveat below):

- Multi-member groups: **276 groups / 663 games**.
- Re-pair rate (any fingerprint): **387 / 1160 = 33.36%** — a third of all our
  rated games are against an opponent version we've already faced on that exact
  map, just possibly with different our-code or seat.
- Identical-fingerprint repeat games: **147** (66 losses, 81 wins) out of the
  387 loose re-pairs — a **38.0%** fingerprint-match rate among loose repeats,
  vs. **87.3%** (48/55) at the strict-key level.
- All-agree loose groups: 76 groups / 165 games.

**Caveat on the loose-key numbers (this is the answer to "do our version changes
break determinism"):** of the 147 identical-fingerprint loose repeats, **100**
have `(our_ver, our_seat)` genuinely different from the earlier occurrence — but
**84 of those 100** are the generic `(1000, titanium_collected, *)` /
`(1000, harvesters, *)` outcome, which is by far the most common fingerprint in
the whole dataset (267 of the 663 loose-multi-group games alone are
`(1000, titanium_collected, True/False)`). Matching on "went the distance and
one side out-economied the other" is a weak signal — it doesn't imply
byte-identical replays, just convergent macro-outcomes, and I did not verify any
cross-version pair at the replay level (no budget left; would need dedicated
downloads). Only **16 of the 100** cross-version matches are early
`core_destroyed` games with an *exact* matching turn count despite a different
`our_ver` (e.g. `I Stone`/meander: turns=75 exactly, `our_ver` 53->54; `0033`/
drumlin: turns=73 exactly, `our_ver` 54->62) — that's a much stronger
coincidence, and all 16 have the SAME seat before and after, with `our_ver`
deltas that are often adjacent-looking submission bumps, consistent with "the
code path this specific opponent/map exercises didn't change between those two
versions" rather than "the engine ignores our code." **Net read: the loose-key
numbers are consistent with the brief's expectation that our own version
changes should generally break the identical-fingerprint match — genuine
cross-version replay-identical repeats are rare (at most 16/663 = 2.4%, likely
fewer) once the generic 1000-turn outcome is filtered out.**

## 3. Sanity checks

### 3a. Identical fingerprint but turns==1000 (tiebreak games, fingerprint less conclusive)
11 of the 43 strict-key all-agree groups reach the full 1000 turns (listed with
match ids in the script output; e.g. `vjg/atoll/ourv20/A`, `Ouroboros/saga/
ourv53/B`, `Lunds Stallions/drumlin/ourv53/A`). These pass the coarse
turns+wincond+winner check but weren't replay-verified — full-length games give
many more rounds for the resource-routing tie-break (section 1, extra check) to
compound, so a matching fingerprint here is weaker evidence of a truly
byte-identical replay than the three confirmed pairs above. None of my 3
required-download pairs happened to be turn-1000 games, so this remains
unverified at the replay level, flagged as the brief asked.

### 3b. Strict-key groups where fingerprints DIFFER (real divergence)
**5 of 48** strict-key multi-groups (10.4%) have members with different
fingerprints — all 5 involve full-length or long games where the divergence had
room to compound:

1. **`Ouroboros/8/drumlin/53/B`** (the flagged one) — 3 games, turns
   1000/528/427, all losses. **Root cause identified above**: a resource-routing
   tie at round 63 between the 528t and 427t members, cascading into a full
   behavioral divergence by round 104. The 1000t member (`0ade6660` g1,
   never destroyed) is presumably an even earlier or different fork of the same
   mechanism (not downloaded — outside budget).
2. **`Troupe/1/vase/20/B`** — 2 games, both turns=1000, but wincond differs
   (`titanium_collected` vs `titanium_stored`) and outcome flips (True/False).
   Full-length game, consistent with an early tie-break-style fork compounding
   into a different final tiebreak stat by round 1000. Not replay-verified.
3. **`Cookie/2/nordkap/40/B`** — 2 games, turns 72 vs 1000, wincond
   `core_destroyed`/loss vs `titanium_collected`/win — the widest swing in the
   set (early rush death in one, full economic win in the other). Same
   metadata-only caveat; plausible same tie-break mechanism triggering very
   early and steering the whole game onto a different branch, but unconfirmed.
4. **`Lunds Stallions/41/eider/53/A`** — 3 games, turns 257/349/648, all
   `core_destroyed` losses. Same result each time (we lose to a core kill), but
   at very different rounds — consistent with tie-break-driven timing noise
   without changing the qualitative outcome.
5. **`gsxWins/16/atoll/53/A`** — 2 games, turns 96 vs 98, both `core_destroyed`
   losses. The smallest divergence of the 5 — only 2 rounds apart, same
   qualitative early-rush-loss outcome. Consistent with a late-stage tie-break
   nudge that doesn't have time to compound much before the core already falls.

None of groups 2-5 were replay-downloaded (budget spent on the 6 required + 2
extra on drumlin per the brief's cap); the drumlin mechanism is the best
metadata+replay-confirmed explanation available and is offered as the likely
shared cause, not a proven one for 2-5.

## 4. Bottom line for the decision-noise-injection question

- Determinism is **real and dominant**: 43/48 (89.6%) of strict-key multi-groups
  reproduce an identical fingerprint every time, and all 3 replay-verified pairs
  (plus the drumlin 528t/427t pair up to round 62) are byte-identical event
  streams, not just matching summary stats.
- It is **not perfect**: a genuine engine-level tie-break exists at multi-way
  resource-routing forks (harvester/conveyor tiles with >1 valid acceptor,
  observed concretely at drumlin round 63) that can be seed-sensitive and
  cascades into materially different games. This affects a minority (5/48,
  10.4%) of repeat groups and is a *different* mechanism from bot-decision
  noise — worth knowing about, doesn't undermine the fix.
- 19 of our 1160 rated games are proven-pattern re-losses (same opponent, map,
  our code, seat, byte-identical play) worth ~60.8 Elo cumulative if a
  decision-noise injection had turned each into a coin flip; the forward rate
  (4.74% strict re-pair, ~40% of those historically losses) implies roughly
  0.06 Elo/game expected value recovered per future game while versions stay
  static — small per-game, but compounds over the volume this ladder plays.

## Addendum (lead, post-verdict 2026-08-07)

- Verdict owned by measuring session: ACCEPTED as measured; on the tape in
  docs/game-model.md (commit fe5f73a) with the three byte-identical pair ids.
  Build action: decision noise = piece G in _v74e4, default OFF (once-per-match
  salt in the core's spawn-dispersion sort key; identity when off).
- Additional benefit recorded at the measuring session's request: per-game
  entropy also breaks the SEED-AMPLIFICATION collapse in local arena batteries
  (game-model.md "seed amplification" — adjacent seeds produce byte-identical
  games, so per-map rows are ~2 distinct games). With piece G on, local rows
  become distinct games again, at the cost of exact paired-seed A/B legs —
  paired comparisons must then pair on the salt, not the seed.
- Engine-side entropy source (harvester output routing tie-break when two
  adjacent acceptors are valid) is the one non-bot fork observed (5/48 groups);
  consequence recorded: do not assume pipeline-topology ties are stable.
