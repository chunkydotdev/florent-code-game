# Thread 11 — Seat time-to-first-delivery (TTFD)

2026-08-07. Read-only replay analysis. Question: does seat B structurally lag seat A
in early-economy timing on atoll/heart/lighthouse, and if so is the lag ours or the
field's, and where does it come from (harvester build, chain completion, or contact
interference)?

## Method

- Source: `all_games_flat.json`, filtered to `map ∈ {atoll, heart, lighthouse}` and
  `our_ver >= 54`. 34 games matched that filter; 16 were selected for a seat/win-loss
  -balanced sample (3 already cached, 11 new downloads via the shared fetcher — under
  the 14-download cap; 2 more turned out to already be cached mid-run).
- Every game is scored **per team** (both sides), giving 32 team-observations. Whichever
  side is not "us" in a given game is the field-control observation for that game's
  opponent — e.g. in an "our seat A" game, the opponent occupies seat B and contributes
  a field data point for seat B, and vice versa. This is what lets the same 16-game
  sample answer both "is there a seat effect" and "is it ours or everyone's."
- Metrics (via `replay_lib.py` / `first_delivery_round`, validated toolkit — delivery
  x10 == `titaniumCollected` passes on every file below):
  - `FH` = round of first harvester build (`r.first_build(team, 'harvester')`)
  - `FD` = round of first delivered stack (`first_delivery_round`)
  - `chain` = FD − FH (time from harvester existing to first stack landing — the
    conveyor-routing phase)
  - `spawn30` = builder-bot spawns in rounds 0–29
  - `FC` = first round any unit (core/builder_bot/gunner/sentinel/launcher) of team A
    is within `dsq<=20` of a unit of team B — this event is necessarily the **same
    round for both teams** in a game, so it cannot itself explain a seat-differential
    in delivery timing; it can only explain a *same-round-for-both* slowdown.
  - delivered-curve checkpoints at r100/r250/r500/r1000 (or final, if the game ended
    core_destroyed before that round)
- `our_ver` is tagged on every "us" row (see Version note at the end).

## Game list (16 games, 32 rows)

| map | match | g | seat(us) | our_ver | opponent | we_won | wincond | n_rounds |
|---|---|---|---|---|---|---|---|---|
| atoll | `2618b9b4` | 3 | A | 59 | I Stone | L | titanium_collected | 1000 |
| atoll | `3b2c12df` | 3 | A | 56 | Oresund Overflow | L | harvesters | 1000 |
| atoll | `ad08eb70` | 5 | A | 62 | OopsGotYourElo | W | titanium_collected | 1000 |
| atoll | `63bb2c30` | 1 | B | 61 | Team 48 | L | core_destroyed | 86 |
| atoll | `2cfcb658` | 4 | B | 54 | Ouroboros | L | core_destroyed | 490 |
| atoll | `40748bb2` | 1 | B | 54 | Askar City | W | core_destroyed | 84 |
| heart | `3712fb12` | 3 | A | 55 | Lunds Stallions | L | core_destroyed | 184 |
| heart | `2618b9b4` | 1 | A | 59 | I Stone | W | titanium_collected | 1000 |
| heart | `17622ae0` | 3 | B | 56 | Ouroboros | L | titanium_collected | 1000 |
| heart | `f33c0f0d` | 5 | B | 54 | Memtrace | W | titanium_collected | 1000 |
| heart | `63bb2c30` | 5 | B | 61 | Team 48 | W | core_destroyed | 241 |
| lighthouse | `c2e57b46` | 2 | A | 60 | Lunds Stallions | L | core_destroyed | 189 |
| lighthouse | `c106d3d2` | 1 | A | 56 | Orizon | W | core_destroyed | 102 |
| lighthouse | `abbf93b4` | 1 | A | 56 | Askar City | W | core_destroyed | 290 |
| lighthouse | `f33c0f0d` | 1 | B | 54 | Memtrace | W | core_destroyed | 136 |
| lighthouse | `585d3457` | 2 | B | 54 | I Stone | W | core_destroyed | 230 |

Note: **no lighthouse-B loss exists at our_ver>=54** in the whole `all_games_flat.json`
(the newest lighthouse-B loss on record is v53, `2d5fe52f…` g5 vs Powerpuff Girls). That
bucket is win-only for us in the current-version window — itself worth flagging, not
filled in against the brief's version floor.

## Per-game, per-team metrics

FH/FD/chain in rounds; `—` = never happened before the game ended.

| map | match g# | seat | us/opp | FH | FD | chain | spawn30 | FC |
|---|---|---|---|---|---|---|---|---|
| atoll | 2618b9b4 g3 | A | us  | 3 | 8 | 5 | 5 | 14 |
| atoll | 2618b9b4 g3 | B | opp | 6 | 8 | 2 | 5 | 14 |
| atoll | 3b2c12df g3 | A | us  | 3 | 8 | 5 | 5 | 6 |
| atoll | 3b2c12df g3 | B | opp | 3 | 9 | 6 | 5 | 6 |
| atoll | ad08eb70 g5 | A | us  | 3 | 8 | 5 | 5 | 10 |
| atoll | ad08eb70 g5 | B | opp | 2 | 7 | 5 | 4 | 10 |
| atoll | 63bb2c30 g1 | A | opp | 4 | 9 | 5 | 4 | 11 |
| atoll | 63bb2c30 g1 | B | us  | 4 | 9 | 5 | 5 | 11 |
| atoll | 2cfcb658 g4 | A | opp | 2 | 8 | 6 | 5 | 10 |
| atoll | 2cfcb658 g4 | B | us  | 4 | 9 | 5 | 5 | 10 |
| atoll | 40748bb2 g1 | A | opp | 17 | 24 | 7 | 4 | 7 |
| atoll | 40748bb2 g1 | B | us  | 4 | 9 | 5 | 5 | 7 |
| heart | 3712fb12 g3 | A | us  | 8 | 21 | 13 | 5 | 3 |
| heart | 3712fb12 g3 | B | opp | 12 | 33 | 21 | 4 | 3 |
| heart | 2618b9b4 g1 | A | us  | 8 | 33 | 25 | 5 | 4 |
| heart | 2618b9b4 g1 | B | opp | 120 | 89† | −31† | 5 | 4 |
| heart | 17622ae0 g3 | A | opp | 6 | 19 | 13 | 5 | 6 |
| heart | 17622ae0 g3 | B | us  | 12 | 27 | 15 | 5 | 6 |
| heart | f33c0f0d g5 | A | opp | 11 | 22 | 11 | 4 | 6 |
| heart | f33c0f0d g5 | B | us  | 12 | 53 | 41 | 5 | 6 |
| heart | 63bb2c30 g5 | A | opp | 8 | — | — | 4 | 4 |
| heart | 63bb2c30 g5 | B | us  | 12 | 109 | 97 | 5 | 4 |
| lighthouse | c2e57b46 g2 | A | us  | 3 | 10 | 7 | 5 | 3 |
| lighthouse | c2e57b46 g2 | B | opp | 10 | 25 | 15 | 4 | 3 |
| lighthouse | c106d3d2 g1 | A | us  | 3 | 10 | 7 | 5 | 3 |
| lighthouse | c106d3d2 g1 | B | opp | — | — | — | 4 | 3 |
| lighthouse | abbf93b4 g1 | A | us  | 3 | 17 | 14 | 5 | 2 |
| lighthouse | abbf93b4 g1 | B | opp | 9 | 12 | 3 | 4 | 2 |
| lighthouse | f33c0f0d g1 | A | opp | 5 | 11 | 6 | 4 | 5 |
| lighthouse | f33c0f0d g1 | B | us  | 5 | 12 | 7 | 5 | 5 |
| lighthouse | 585d3457 g2 | A | opp | 7 | 10 | 3 | 5 | 11 |
| lighthouse | 585d3457 g2 | B | us  | 5 | 12 | 7 | 5 | 11 |

† **heart `2618b9b4` g1, team B**: FD=89 is not team B's own economy. Traced the
resource-move chain for stack id 131: it originates at (14,5) — **our** (team A, seat A)
harvester built round 62 — flows through our own conveyors, then crosses onto **team
B's** conveyors at (18,8)/(19,8) (both owned by entity ids 17/25, team 1), and lands on
B's core footprint at round 89. B had not built a harvester yet (FH=120). This is a real
resource-routing leak matching the CLAUDE.md note that "resources can still be pushed
onto an opposing team's conveyor network or core" — in this game **we fed the enemy's
tiebreak stat** by routing a conveyor chain adjacent to their network. It's a distinct,
concrete bug from the seat-timing question, but it inflates the "opp seat B" FD bucket
below; B's FH=120 is the reliable number for that row, not FD=89.

## Aggregates: seat A vs seat B, ours vs field (median, values listed)

| map | who | seat A FD | seat B FD | Δ (B−A) | seat A FH | seat B FH | ΔFH |
|---|---|---|---|---|---|---|---|
| atoll | us  | 8 `[8,8,8]` | 9 `[9,9,9]` | **+1** | 3 `[3,3,3]` | 4 `[4,4,4]` | **+1** |
| atoll | opp | 9 `[9,8,24]` | 8 `[8,9,7]` | **−1** | 4 `[4,2,17]` | 3 `[6,3,2]` | **−1** |
| heart | us  | 27 `[21,33]` | 53 `[27,53,109]` | **+26** | 8 `[8,8]` | 12 `[12,12,12]` | **+4** |
| heart | opp | 20.5 `[19,22,—]` | 61†`[33,89†]` | **+40.5†** | 8 `[6,11,8]` | 66†`[12,120]` | **+58†** |
| lighthouse | us  | 10 `[10,10,17]` | 12 `[12,12]` | **+2** | 3 `[3,3,3]` | 5 `[5,5]` | **+2** |
| lighthouse | opp | 10.5 `[11,10]` | 18.5 `[25,—,12]` | **+8** | 6 `[5,7]` | 9.5 `[10,—,9]` | **+3.5** |

(† = distorted by the `2618b9b4` g1 leak above; on FH alone the opp-seat-B heart gap is
still large — one real value at 120, one at 12 — small-n, treat as directional not
precise.)

Chain-time (FD−FH) median by bucket, the clearest signal:

| map | us seat A | us seat B | opp seat A | opp seat B |
|---|---|---|---|---|
| atoll | 5 `[5,5,5]` | 5 `[5,5,5]` | 6 `[5,6,7]` | 5 `[2,6,5]` |
| heart | 19 `[13,25]` | 41 `[15,41,97]` | 12 `[13,11,—]` | −5†`[21,−31†]` |
| lighthouse | 7 `[7,7,14]` | 7 `[7,7]` | 4.5 `[6,3]` | 9 `[15,—,3]` |

`spawn30` (builder-bot spawns in rounds 0–29) shows **no seat signal anywhere**: every
bucket across all three maps and both us/opp sits at 4 or 5, with no consistent
direction by seat — see the `spawn30` column in the per-game table above. Whatever
drives the FD/FH gaps on heart, it is not "seat B spawns fewer builders early."

## Delivered-curve checkpoints (r100/r250/r500/r1000)

Only informative for the games that actually reach each checkpoint; core_destroyed
games truncate at `n_rounds` and carry their final value forward. Full per-game figures
are in `results.json`; the six 1000-round games (all `titanium_collected` or
`harvesters` wincond) are the only ones with real r250/r500/r1000 data:

| map | match g# | seat | us/opp | r100 | r250 | r500 | r1000 |
|---|---|---|---|---|---|---|---|
| atoll | 2618b9b4 g3 | A | us  | 770 | 2150 | 4060 | 7110 |
| atoll | 2618b9b4 g3 | B | opp | 430 | 1820 | 4900 | 11410 |
| atoll | 3b2c12df g3 | A | us  | 470 | 1200 | 2450 | 4950 |
| atoll | 3b2c12df g3 | B | opp | 460 | 1210 | 2460 | 4950 |
| atoll | ad08eb70 g5 | A | us  | 780 | 2270 | 4770 | 9770 |
| atoll | ad08eb70 g5 | B | opp | 360 | 740 | 1780 | 4280 |
| heart | 2618b9b4 g1 | A | us  | 530 | 2690 | 6920 | 14420 |
| heart | 2618b9b4 g1 | B | opp | 30 | 610 | 2880 | 5730 |
| heart | 17622ae0 g3 | A | opp | 220 | 1700 | 5440 | 12950 |
| heart | 17622ae0 g3 | B | us  | 400 | 1800 | 2420 | 3670 |
| heart | f33c0f0d g5 | A | opp | 310 | 1200 | 2450 | 7330 |
| heart | f33c0f0d g5 | B | us  | 310 | 1060 | 3560 | 8560 |

Note the early-checkpoint reversal in `2618b9b4` g1: our seat-A r100 (530) is already
17x the opponent seat-B r100 (30) — an early lead consistent with the FD gap — but by
r1000 the multiple has shrunk to ~2.5x, i.e. seat B's economy, once it gets going, ramps
at a comparable or faster rate; the seat-B tax on heart looks like a *start-line* delay,
not a *sustained* growth-rate penalty. `17622ae0` g3 tells the opposite story for us
(seat B there): the gap actually widens from r250 to r1000 (12950 vs 3670 final) —
though that game we lost outright to the opponent's stronger economy overall, not
narrowly on timing, so it's a weaker read on the seat effect specifically.

## First-contact vs first-delivery ordering

On heart and lighthouse, first contact (`FC`) happens at round 2–6 in every game —
consistently and substantially **before** first delivery (round 8–109). On atoll,
contact (round 6–14) and delivery (round 7–24) happen close together, sometimes either
order. Because `FC` is the same round for both teams in a game by construction (it's one
shared proximity event), it cannot be the source of a *seat-differential* in delivery
timing — a shared early-contact event affects both sides identically. It rules out
"contested-tile interference" as the mechanism for the seat-B lag: the lag would have to
come from something asymmetric in each team's own build sequence, not from the contact
event itself.

## Win correlation

Across the 16 games, the team that delivered first won 4, lost 8 (2 tied FD, 2 games
where one side never delivered). Faster delivery does **not** predict winning in this
sample — most of these games (10/16) are decided by `core_destroyed`, where combat
timing dominates outcome regardless of who opened faster; even in the `titanium_collected`
games, the round-1000 tiebreak is **total** delivered by round 1000, not who delivered
*first* (e.g. heart `f33c0f0d` g5: opponent delivered first at round 22 vs our round 53,
but we finished with more total delivered — 8560 vs 7330 — and won). FD/FH measure
opening-economy speed, not the game's eventual winner; they're not the same question.

## Verdict on the opening-reorder hypothesis

**The hypothesis holds on heart, does not hold on atoll, and is weak/field-only on
lighthouse. It is not a single, uniform, all-map effect — the fix, if pursued, needs to
be map-specific.**

- **heart**: real, large, structural seat-B delivery lag — median **+26 rounds** for us,
  and directionally even larger for the field (opponents' own seat-B first-harvester
  round is 12 vs 8, a genuine +4-round gap independent of the leak). The gap is driven
  almost entirely by **chain-completion time** (FD−FH), not by when the harvester gets
  built: FH gaps are small (+1 to +6 rounds) but chain-time gaps are large (us: median
  19→41, roughly +22; the harvester exists on schedule, but wiring it to the core takes
  much longer as seat B). Present in both our data and the field's ⇒ **engine/map tax,
  not our opening specifically** — though ours (+22 chain rounds) is comparable in
  magnitude to what limited field data shows.
- **atoll**: FD is functionally tied by seat (8 vs 9 rounds, a 1-round gap) — but that
  1-round gap is **perfectly deterministic in our own data alone** (FH exactly 3 in all
  3 seat-A games, exactly 4 in all 3 seat-B games, regardless of our_ver 54–62) and
  **absent in the field's data** (opponents' seat-A/seat-B FH medians are both ~3-4 with
  no consistent direction). That is: on atoll, the field shows no seat effect at all, but
  *our own bot* has a small, rock-solid, version-independent 1-round tax when spawning
  as seat B — reads as an artifact of our own fixed build-order logic (e.g. a
  direction-preference or move-order that isn't adapted to starting orientation), not an
  engine tax. Small (1 round) but worth a look since it's 100% reproducible.
- **lighthouse**: mixed. Our own FD gap is negligible (10 vs 12, +2 rounds, matches a
  +2-round FH gap — same small deterministic-looking pattern as atoll, 3 vs 5). The
  field's gap is larger (10.5 vs 18.5) but n=2 per bucket with one clear outlier
  (`c2e57b46` g2, opponent seat B at FD=25) and one reversal elsewhere
  (`abbf93b4` g1: opponent seat B delivered *faster* than our seat A, 12 vs 17) — too
  thin to call structural with confidence.

**So**: seat-B delivery lag is real and sizeable on heart (for everyone), a small fixed
tax specific to our own opening on atoll and lighthouse (~1–2 rounds, not the field's
problem), and the ~28-31% seat-B win-rate handicap quoted in the brief cannot be
explained by opening-economy timing alone on atoll or lighthouse — timing there is
essentially fine, so whatever drives that win-rate gap on those two maps has to be
something else (most likely combat/turn-order advantage directly, not the economic
open). Heart is the one map where "fix the opening reorder" is actually the right lever;
atoll/lighthouse need a different diagnosis.

## Version note

`our_ver` is tagged on every "us" row above. The sample is too thin to cleanly split
current-line (v59+) vs older generations (v54–58) — most map×seat buckets have only 1-3
games spanning versions 54 through 62. What the data does show: on atoll, FD/FH values
are **identical** regardless of version within a seat (seat A: FD=8 at v56, v59, *and*
v62; seat B: FD=9 at v54, v54, *and* v61), and the same holds on lighthouse seat B
(FD=12 at both v54 games). That argues the opening build-order timing measured here has
been constant across our whole v54+ line — this is not a recent regression, it's been
present at least since v54.

## Downloads used

11 new downloads via the shared fetcher (2 more targets turned out already cached
mid-run): `ad08eb70…` g5, `63bb2c30…` g1, `40748bb2…` g1, `3712fb12…` g3, `2618b9b4…` g1,
`f33c0f0d…` g5, `c106d3d2…` g1, `abbf93b4…` g1, `f33c0f0d…` g1, `585d3457…` g2,
`63bb2c30…` g5. Under the 14-download cap. Already-cached at start: `2618b9b4…` g3,
`3b2c12df…` g3, `17622ae0…` g3; found already-cached mid-run: `2cfcb658…` g4, `c2e57b46…` g2.
