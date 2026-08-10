---
tactic: (A) THE COMMIT TRIGGER IS A PRIOR, NOT A SIGHTING — four Battlecode teams launch the attack at a SET of symmetry-derived candidate positions at round 0, and revise only by DISPROOF. Measured here: our own map pool never yields a singleton candidate, and a wrong guess costs a second full trip
source: https://battlecode.org/assets/files/postmortem-2025-confused.pdf
origin: Battlecode 2025 confused; Battlecode 2020 confused; Battlecode 2023 Gone Fishin'; Battlecode 2023 4 Musketeers; Battlecode 2021 wololo
evidence: documented
transfers: yes
---

> **OVERLAP NOTICE for the research lead.** A concurrent sweep filed
> [`symmetry-is-the-only-free-information-about-the-unseen-map`](symmetry-is-the-only-free-information-about-the-unseen-map.md)
> and [`the-winner-stored-a-tri-state-and-resolved-unknown-two-ways`](the-winner-stored-a-tri-state-and-resolved-unknown-two-ways.md),
> which cover the symmetry *channel* and the *representation of UNKNOWN* from BC2023 winner
> source code. **This file is the COMMIT RULE and the map-pool MEASUREMENT** (candidate-set
> size, `Rot180` hit rate, and the tempo price of a wrong guess) and does not re-derive
> either. Merge or cross-link as you see fit; the measurement section is unique to this file.

## WHAT IT IS

Sweep 20C asked what actually triggers commitment to an attack on a target the attacker
cannot see. **In Battlecode the answer is never a sighting.** It is a prior derived from map
symmetry, acted on immediately, and revised only when an observation *disproves* it.

**1. The default belief, stated as a default (BC2025 confused).** Maps are guaranteed one of
three symmetries, and the bot picks one before seeing anything:

> *"Soldiers defaulted to assuming rotational symmetry unless proven otherwise, directing
> them towards the map center initially."*

> *"This offered a strategic advantage, serving as the optimal location for determining the
> map’s symmetry while also minimizing the distance to potential enemy tower locations."*

**Referent check.** *"This"* is the preceding sentence's behaviour — defaulting to rotational
symmetry and heading to the map centre. The claimed advantage is explicitly **two things at
once**: the centre is the best place to *disambiguate* the symmetry and it is *on the way* to
the enemy. The information the disambiguation reads is static:

> *"Symmetry could be deduced from wall and ruin locations, which remained constant
> throughout the game."*

**2. The belief is a CANDIDATE SET the attacker walks (BC2020 confused).** Their rusher's
behaviour list opens with the no-information case, and it is not "wait" or "scout":

> *"If it does not know the enemy HQ location, it goes to the unchecked possible locations,
> since there are only three possible symmetries (horizontal, vertical, rotational)"*

**Referent check.** *"it"* is the first spawned miner — the postmortem's sentence is
*"We assign our first spawned miner as the "rusher", which will do the following things."*
(straight quotes as in the source); this is item 1 of that list, and items 2-4 describe what it
does once it *does* see the HQ. (Item 5 — the 180-round abort — is already held by
[`abandon-the-plan-on-a-progress-timeout`](abandon-the-plan-on-a-progress-timeout.md) and is
not re-derived here.)

**3. Elimination, not confirmation, is the update rule (BC2023 Gone Fishin').**

> *"The symmetry possibilities are recorded in the shared array, waiting for scouts to
> eliminate them."*

> *"If the symmetry is not confirmed, all units will check if a newly seen tile eliminates an
> existing symmetry."*

**4. And the guess is what the ATTACK is aimed at (BC2023 4 Musketeers).**

> *"Based on your HQ locations, you can guess the enemy HQ locations and move towards them to
> see if you can find an HQ."*

**5. THE DOCUMENTED FAILURE, from the same team that later built the elimination machinery.**
Gone Fishin' shipped a hardcoded belief with no revision path and it cost them a tournament:

> *"Before Sprint 1, we assumed a rotational symmetry, as all three maps up for scrimmages
> were rotationally symmetrical."*

> *"This decision was due to time constraints and eventually backfired quite heavily in
> Sprint 1."*

**Referent check.** *"This decision"* is the assumption of rotational symmetry stated in the
immediately preceding sentence. The sentence after names the fix: *"We immediately
implemented a MapRecorder after Sprint 1."* **The failure was not the prior. It was the prior
with no disproof channel.**

**6. And when the disproof test cannot be COMPUTED, the default points at the attack
(BC2021 wololo).** His burying units needed to know whether the enemy Enlightenment Center
was already enveloped; the exact graph search did not fit the bytecode budget:

> *"my code performed a highly truncated version of a graph search in the form of a hardcoded
> triple nested loop, and assumed that the opponent EC was not buried if the third loop
> called for the graph search to continue further beyond"*

> *"Despite the fact that the graph search was hardcoded and truncated to ignore many
> possible use cases, it tended to function perfectly in the vast majority of cases."*

**Referent check.** *"the opponent EC"* is the enemy Enlightenment Center (their base);
"buried" is wololo's term for enveloping it in units so it cannot build. The unevaluable case
resolves to **not-yet-done** — i.e. keep committing — rather than to assume-success-and-leave.
(That gloss is this file's paraphrase of the code path wololo describes; his own words are
the two quotes above.)

## THE MEASUREMENT THIS SWEEP RAN, BECAUSE THE OBVIOUS OBJECTION IS "SYMMETRY MAKES IT MOOT"

**Instrument:** `Replay.cores`, `width`, `height` from `tools/replay_census.py`, over a
**1-in-9 file sample of the local `replay_archive/` (1,129 replays parsed, of 12,201 files
present), deduplicated to 20 unique maps** by `(W, H, md5(tiles))`. **Population: maps
appearing in this repo's local replay archive as of 2026-08-10 — ladder and sparring series,
not the organisers' full generator space.** For each map, the three rectangle transforms of
our own core's NW corner were computed: `Hrefl = (W-2-x, y)`, `Vrefl = (x, H-2-y)`,
`Rot180 = (W-2-x, H-2-y)`.

| result | count | share |
| --- | ---: | ---: |
| true enemy core is one of the 3 candidates | 20 / 20 | **100%** |
| **distinct** candidate positions = 3 | 15 / 20 | 75% |
| distinct candidate positions = 2 | 5 / 20 | 25% |
| **distinct candidate positions = 1 (i.e. no ambiguity)** | **0 / 20** | **0%** |
| `Rot180` is a correct answer | 17 / 20 | **85%** |
| `Vrefl` is a correct answer | 5 / 20 | 25% |
| `Hrefl` is a correct answer | 3 / 20 | 15% |

**Guard check, per the standing instruments rule:** re-running the "is the enemy core among
the candidates?" test with the true enemy core shifted by `(+3, +5)` (mod map bounds) gives
**0/20** — the check does produce the other verdict, so the 20/20 above is not a constant
column.

**And the price of guessing wrong, from a second pass (1-in-17 sample, 598 replays, 18 unique
maps):** the maximum Manhattan separation between the candidate positions has a median of
**24**, against a median true Manhattan distance from our core to the enemy core of **24** —
**median ratio 100%.** In 17 of 18 maps the two numbers are equal.

**Read that plainly: on this map pool, walking to the wrong symmetry candidate costs
approximately the entire journey a second time.** A builder bot moves one cardinal step per
move cooldown and cannot act on a moving turn, so a median wrong guess is on the order of
**24+ rounds of a 250-round kill window, paid at the far end of the map.**

## WHY IT MIGHT TRANSFER

- **BC2025 confused's exact default is the empirically right default here: 85% Rot180.**
  That is a one-line constant with a measured hit rate, available at round 0 from
  `get_map_width()`, `get_map_height()` and `get_position()`, with no scouting, no store slot
  and no CPU.
- **The candidate set is at most 3 and never 1**, so the BC2020-confused structure (walk the
  unchecked candidates) is directly expressible, and the ordering is not arbitrary: try
  `Rot180` first, then whichever of `Vrefl`/`Hrefl` is distinct from it.
- **Elimination is cheap for us in one specific way and expensive in every other.** Terrain
  never changes here, exactly as in BC2025 confused — but see the killer below.
- **It answers (A) for our programme's clock.** Every rule in this file fires at **round 0**.
  Against our own tape (before r200 we go 277-148, 65.2%; after r200, 164-363, 31.1%), a
  commit rule that needs no observation is the only class of commit rule that can fire early
  enough to matter.

## WHAT WOULD KILL IT

- **THE BIG ONE — we cannot do Battlecode-style symmetry elimination, because our engine
  refuses out-of-vision terrain queries.** Measured in this repo 2026-08-08
  (`docs/game-model.md`): `get_tile_env()`, `is_tile_passable()` and `get_tile_building_id()`
  **raise `GameError: Position out of vision range`** for an in-bounds tile the unit cannot
  currently see. Every source above eliminates symmetries by comparing terrain across the
  axis from data structures fed by sensing; BC2025 om nom does it by projecting *whole
  bitmask rows*. **We can only compare tiles we have physically stood near** (builder vision
  r²=20, ~4.5 tiles). Symmetry elimination here is a walking cost, not a bytecode cost, and
  that inverts the economics every source assumed.
- **Which means the disproof channel Gone Fishin' says you must have is the expensive part,
  and their failure mode is our default state.** A hardcoded `Rot180` with no disproof channel
  is precisely what *"backfired quite heavily"* — and on the 15% of maps where it is wrong it
  costs a full second traverse.
- **Our maps are 8x8 to 30x30 and the sample is 20 maps.** The 85% is a point estimate on a
  small, repo-local pool; the organisers' generator could weight symmetries differently in a
  tournament map set, exactly as BC2021's finals were *"mostly large maps"*.
- **A candidate set does not tell you the target is worth attacking**, only where it is. That
  is the other half, and it is
  [`retract-the-target-only-on-a-look-not-on-a-clock`](retract-the-target-only-on-a-look-not-on-a-clock.md).

## BUILDER HOOK

Two things, in order, and the first is free.

1. **Constant, no branch:** compute `enemy_core_guess = Rot180(own_core)` once at round 0 on
   the `Player` instance and point the existing forward walk at it. Measure `core_kill_share`
   and `time_to_core_kill` split by **whether the guess was right** — the replay knows the
   true core, so the split is computable after the fact even though the bot cannot see it.
   That directly prices the 15%.
2. **Only if (1) shows the 15% is expensive:** en-route disproof. A raider walking to the
   `Rot180` candidate passes near the map centre; have it compare each tile it can actually
   see against the mirrored tile *it has already seen* (its own half), and drop a candidate on
   the first mismatch. Cost is one dict of visited tiles per unit and no store slot.
   **Do not build (2) before measuring (1)** — on 85% of maps it is pure overhead.

## SOURCES QUOTED IN THIS FILE

- https://battlecode.org/assets/files/postmortem-2025-confused.pdf
- https://battlecode.org/assets/files/postmortem-2020-confused.pdf
- https://battlecode.org/assets/files/postmortem-2023-gone-fishin.pdf
- https://battlecode.org/assets/files/postmortem-2023-4-musketeers.pdf
- https://battlecode.org/assets/files/postmortem-2021-wololo.pdf

Every quoted string above was verified verbatim by literal `grep -F` against the flattened
primary text (`pdftotext` then `tr -s ' \n\t\f\r' ' '`) during tactics sweep 20C
(2026-08-10 04:11 UTC, repo HEAD `a08669c`). The measurement tables are this sweep's own
instrument run against the local replay archive, with the population stated inline.
