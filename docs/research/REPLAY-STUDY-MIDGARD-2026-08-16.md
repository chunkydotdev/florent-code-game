# REPLAY STUDY: MIDGARD — why we lose our worst map, from 86 decoded games (2026-08-16, builder s47)

PROVENANCE: opus subagent commissioned by the builder on Magnus's watch-the-
games directive (study 3 of 3; siblings: REPLAY-STUDY-0033 and
REPLAY-STUDY-TOPTEAM-MICRO, same date). Sample: all 86 archived midgard games
(30W/56L = 34.9%). The collision-pair mechanism was excluded up front
(research closed it 16/16 same day). Decoding via replay_census primitives.
Agent report verbatim below.

## The map fact that drives everything
30x30, cores (2,2)/(26,26), 180°-rotational. The centre is a WALLED VAULT —
a 10x10 wall ring around a 2x2 ore block, with exactly four 2-tile gates.
BFS on the real grid: shortest core-to-core walk is 45 steps, AND the
shortest walk that never enters the centre box is ALSO 45 steps.
**Avoiding the vault costs zero.**

## Piece 1 — EDGE-LANE APPROACH (the finding)
Opponent perimeter raiders reach d²≤8 of our core 68% (106/156) at median
r76.5; their vault raiders 29% (56/194) at median r98 — 39pp and ~21 rounds
for zero extra distance, and not a selection artefact (perimeter raiders
depart earlier AND transit faster). WE TAKE THE VAULT ON 248 OF 252 RAIDER
TRACKS (98.4%). Per-opponent perimeter share vs our win rate: Spearman −0.61
(n=11); games where ≥50% of their raiders go perimeter: we win 15.4% vs
50.0% otherwise. Our worst midgard beaters are the heaviest edge users
(gsxWins 100%/0-4, diverge 78.6%/0-6, 0033 62.9%/1-9, Erebus 54.8%/0-6);
the vault-users are the ones we beat (HTTP 418 0%/6-3).
Anchors: d6b9de83…_game_1 (gsxWins 18/18 perimeter, arrive r50, we die
r213); 5a954b7a…_game_5 (Erebus arrive r48; our raid never arrives).
⇒ Pure destination/navigation change (#63's own genre). Midgard-specific by
construction (ragnarok same cut: 61 vs 57, near-null — its centre is no vault).

## Piece 2 — LAUNCHER RELAY ("bot cannon")
Builder stands at d²≤2 of a launcher, is thrown d²≤26, builds the next
launcher, repeats: ~6 tiles/2 rounds ≈ 3x walking, and the chain ferries
every later raider. 61 opponent instances across 15 maps (Jython 23,
Memtrace 21, Juusto 7); 0 by us. Midgard within-team contrast: WITH chain
arrive r17/r19/r30; SAME TEAMS without it r50/r52/r54. Anchor: 1dec675d…_g3
— Jython launchers r1/r3/r5/r7/r9/r16 up the top edge then down the column
(the perimeter route, MECHANISED), first bot at our core r17.
⚠ The 39.3%-vs-52.4% win-rate split is confounded with their version/era —
prioritiser, not verdict.

## Piece 3 — THE ONE-CONSTANT VERSION: UN-GATE OUR OWN FERRY
LAUNCHER_MIN_RND = 160 (doctrine.py:1536, enforced main.py:613) forbids ANY
launcher before r160 on every map. Midgard is decided at r101-150 (21 of 56
losses). Self-catapults measured: us n=6 at median r288; opponents n=33 at
median r18. The constant was swept POOLED ACROSS MAPS — the "caps fitted on
smaller maps" suspect confirmed at source. Smallest shippable: make
LAUNCHER_MIN_RND a function of core separation.

## Piece 4 — RELEASE RAIDER #1 BEFORE THE BELT
Our WALKING is not the problem (our vault transit 38 rounds vs their 53).
The loss is upstream: first departure ours r22 (r24 in losses, r16.5 in
wins) vs theirs r13.5. Arrival order nearly decides the game: we arrive
first → 64.7% wins; they arrive first → 13.0% (and they arrive first in
46/86). Their first conveyor lands r4-5 vs our r7 and they STILL leave 8
rounds earlier — ordering, not income.

## Piece 5 — SCALE DISCIPLINE IN THE KILL WINDOW
r60 scale: ours 306% vs their 280% (converged 354% by r150) — every
decisive-window build costs us ~9% more. Source: 9.1 builders/game vs 7.8,
and 73.4% of our builder-rounds are spent by bots that NEVER reach d²≤64 of
the enemy core (their 39.0% arrival share). They bank the difference
(273 Ti at r100 vs our 126).

## Roads CLOSED (do not re-spend a leg)
Conveyors do NOT block builder movement (38,011 moves onto live conveyor
tiles, 0 onto solid buildings — eco.py:824's omission of CONVEYOR/SPLITTER
is CORRECT; only BUILDER_BOT is missing, already DESIGN-63 F1). Ammo
starvation is THEIR failure not ours (forward-turret-alive-but-ammo<10:
us 10.8%, them 28.6%). Midfield economy symmetric (17.4 vs 17.2%). Kill
path symmetric (sentinels do the core damage both ways).

## Why we lose midgard — the mechanism paragraph
Longest approach in the pool (45 steps) + the only four-gate walled centre.
We funnel 98.4% of raider tracks through a 2-tile gate; the field routes
~half its raiders around the edge FOR IDENTICAL DISTANCE (68% arrival at
r76.5 vs 29% at r98). We also leave ~11 rounds late and field 9.1 builders
of which 73% never arrive (scale 306% vs 280% at r60). Median first contact
at their core r88-92 against a decision band of r101-150 — we show up with a
dozen rounds of margin, in ones and twos (peak concurrency 2.35 vs 2.81;
zero-bots-arrive games 12/86 vs 3/86), and 88 of our builder deaths happen
inside our own home radius vs 7 of theirs. We do not lose midgard at their
core — we lose it in transit and in the queue behind it, on a map that
offers a free way around the obstacle we insist on walking through.
