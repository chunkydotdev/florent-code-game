# CUT-120(a) — the TRRR stall decode: what outlasts Mjolnir's push in the 52 round-1000 games

> **GAME CONTEXT (rider added s56, 2026-08-22 ~12:1xZ, per Magnus's 11:16Z directive; the
> resolution below is unchanged):** everything in this document describes moves in the
> Florent Code League — a sandboxed bot-vs-bot programming competition on a simulated
> grid, within organiser-approved rules. "Kill", "takedown", "eviction" and similar terms
> refer exclusively to in-game mechanics between competing game bots.
> **Header correction, same rider:** the SUBJECT paragraph below stamps the dev head as
> `bots/_v622nestfall`; the line head moved to `bots/_v623healweld` at 11:40Z, three
> minutes before this doc was written (delta: one healguard conjunct, sk_roles.py:5150;
> sk_maps/sk_common byte-identical, so every anchor cited here is unshifted). Left in
> place, corrected here — a banked doc takes riders.

**Queue row:** #120 half (a), STUDY-FIRST, banked-corpus decode, zero games played.
**Clock:** written 2026-08-22T11:43:21Z (`date -u` in the measuring shell). Repo HEAD at
measurement time `f0a8ac781`.
**SUBJECT — read this before quoting any number below:** every "us/our" figure in this
document is the behaviour of **MJOLNIR v176/v179** (with v165/v168/v174 in the tail),
x3r0's holder line. **This is NOT Skalman evidence.** The Skalman dev head
(`bots/_v622nestfall`) is a different tree and nothing measured here transfers to it as a
measured claim — see §9 for what crossing the trees would and would not license.

## 0. Provenance — every input file

| input | role |
| --- | --- |
| `corpus/ladder_games.tsv` | pool definition + outcome/cond/turns/map/version metadata (8,025 rows) |
| `corpus/join.tsv` | replay file → match → **our team index**; the seat key |
| `replay_archive/*.replay26` | 85 TRRR game replays + 45 control replays, all already on disk; **nothing downloaded, platform untouched** |
| `tools/replay_census.py` | wire primitives reused (`fields`, `read_pos`, `parse_entity`, `scalars`, `packed_varints`) |
| `tools/corpus/replay_autopsy.py` | the attribution model this decode is modelled on (rotation-re-emit guard, signed `updateHp`, damage-target law) |
| `tools/replay_schema.md` | protobuf schema + gotchas |
| `docs/research/corpus-howto.md` | corpus traps 1-8 |
| `bots/_v176idlecull/`, `bots/_v179rushon/` | READ-ONLY source read of the forward-sentinel gate (§7); **the local-directory-name → platform-version mapping is a repo convention and was NOT verified against a submission manifest** |
| `scratchpad/s56_trrr_extract.py` | the extractor written for this cut (read-only over replays) |
| `scratchpad/s56_trrr_an.py`, `scratchpad/s56_trrr_games.jsonl`, `scratchpad/s56_ctrl_games.jsonl`, `scratchpad/s56_trrr_games_SWAP.jsonl` | intermediates |

Everything in this document is MEASURED off those files unless the line carries
**EYEBALL** or **INFERENCE**.

---

## 1. The pool, re-derived (matches the row's registered framing exactly)

MEASURED from `corpus/ladder_games.tsv`, filter `opp == 'TRRR'`:

- **85 rated games**, **17 matches × exactly 5 games** (`Counter({5: 17})`).
- Dates 2026-08-20 (15) / 08-21 (40) / 08-22 (30). Their versions: **v45 ×70, v44 ×15**.
- Ours: **v176 ×60, v165 ×10, v168 ×5, v174 ×5, v179 ×5** — Mjolnir.
- **Our core destroyed pre-r1000: 0 of 85.**
- **52 games reach turns ≥ 1000**; we won 5, they won 47. `cond` over the 52:
  `titanium_collected` 51, `harvesters` 1 (the `harvesters` game is one of our 5 wins,
  `5182a078…_game_5.replay26`, fjordgate) — so **all 47 of their wins are
  `titanium_collected`**, as registered.
- **33 games end before r1000, all 33 won by us on `core_destroyed`**, median 226 rounds
  (min 111, max 628).

Cluster note carried on every interval below: **the 85 games are 17 clusters of 5.** All
CIs in this document are **match-level bootstraps (4,000 resamples of the 17 matches)**,
not game-level binomials. Crude match-level variance inflation on the kill indicator
measured here: **1.63** — in the same family as the repo's rated pooled DEFF 1.529.
Per-map cells are n ≤ 9 so **no interval is quoted per map at all** (§6).

## 2. Instrument validation — four checks, each able to fail

1. **Replay-internal `winner` vs ladder `won` (through the join seat): 0 disagreements /
   85.** `wincond` vs `cond`: **0 / 85**. `turns`: **0 / 85**.
2. **Independent behavioural seat fingerprint** (the join seat descends from `winnerSide`,
   which corpus-howto TRAP 7 says is circular for seat statistics, so the seat needed a
   non-winner-derived check). Pattern chosen because it *could* have returned the
   disconfirming case — "both sides build launchers" or "them only":
   **join-us built ≥1 launcher in 77 / 85 games; join-them in 0 / 85.**
   TRRR builds **zero launchers in all 85 games** and throws **zero** bots.
3. **Delivery geometry end-to-end** (`tools/replay_schema.md`'s cheapest parser check):
   `Player.titaniumCollected == 10 × (DistributeResources moves landing on a core
   footprint tile)` — **170 / 170 team-sides, 0 mismatches.**
4. **Damage ledger self-check**: attributed core damage (FireTurret resolved by shooter
   entity + BuilderAttack, with the unit-priority rule) vs the summed negative
   `updateHp` deltas on the core id — **agrees in 85 / 85 games**, both pools.

**INSTRUMENT CONTROL (corrupted input).** `S56_CORRUPT=teamswap` flips the team byte on
every entity and event and the whole extraction was re-run over the same 85 files:

| | games where "us" built a launcher | where "them" did | median heal on "their" core | median dmg |
| --- | --- | --- | --- | --- |
| clean | **77 / 85** | **0 / 85** | 340 | 762 |
| team-swapped | **0 / 85** | **77 / 85** | **0** | **0** |

and the team-agnostic invariant (total core damage summed over both cores) is
**157,662 in both runs** — so the corruption moved exactly the labelling and nothing else.
A per-team number that did not move under this control would be a constant column.

Not used anywhere in this cut: `BotOutput.stdout` (dead on both surfaces),
`econ.tsv.deliveries` / `.shots` (TRAPs 5/6/8), `ladder_games.seat` (TRAP 7).

---

## 3. What TRRR is: a pure farm with no core-attack behaviour at all

MEASURED over all 85 games:

- **Damage on our core: 0 in 85 / 85 games.** Not "we survived" — **zero HP removed.**
- **Their builderAttacks landing on our core footprint: 0** (total, all games).
- **Their turret shots hitting our core: 0** (total, all games).
- **Their launchers built: 0. Their throws: 0.**
- And yet their builder bots stand on one of the **8 tiles orthogonally adjacent to our
  core** for a **median 173 bot-rounds per game** — they are repeatedly in melee position
  on our core and never take the action.

So the pairing is structurally one-sided: **TRRR cannot end a game any way except the
r1000 collection tiebreak**, and every game is decided by whether Mjolnir's core takedown
lands. The 33 kills are ours; the 52 stalls are theirs.

Their end-state economy in the 52: **`titanium_collected` median 15,210 vs our 1,395**
(ITT over the 52). In the 33 it is **620 vs 1,930** — the margin reverses with the outcome,
which is why key 1 is not the thing to study; the takedown is.

---

## 4. The 52 split into TWO distinct stall modes, not one

The 52 r1000 games are **bimodal on whether our damage ever reaches their core at all**:

| mode | n | share of the 52 | 95% CI (match bootstrap) |
| --- | --- | --- | --- |
| **A — NO CONTACT**: zero HP ever removed from their core, all 1000 rounds | **20** | **38.5%** | [24.5, 51.9] |
| **B — OUT-HEALED**: damage lands and is healed back | **32** | 61.5% | — |

Control direction: **0 of the 33 kill games** are mode A (by construction, but the
zero-damage share is a real 20/52 vs 0/33 split, not a definitional artefact of the r1000
cut — a stalled game *could* have driven the core to 1 HP and 6 of the 52 did get it under
250).

Whole-pool damage ledger, by source, on **their** core:

| pool | total attributed | sentinel | builder melee |
| --- | --- | --- | --- |
| mode A (20) | 0 | — | — |
| mode B (32) | 119,738 | **119,376 (99.7%)** | 362 (0.3%) |
| kills (33) | 37,924 | **37,458 (98.8%)** | 466 (1.2%) |

**Mjolnir kills cores with sentinels.** Builder melee on the enemy core is ~1% of damage
and its median is **0 attacks per game** in every pool — consistent with the forgone-melee
finding already banked on this subject in QUEUE #119.

### 4A. Mode B is a heal race that ties almost exactly

- **48 of the 52** r1000 games end with **their core at exactly 500 HP** (net damage 0).
  The four exceptions net 6 / 26 / 118 / 216. **No game in the 52 nets ≥ 250.**
- Mode B whole-game: **damage 119,738, healed back 119,372 → heal/damage = 0.997.**
  Median per game: **2,004 dealt, 2,004 healed**, deepest dent to HP 321.
- Rates inside the assault window (first to last damaging round), per game medians:

| pool | our dmg/round | their heal/round | best 10-round NET dent |
| --- | --- | --- | --- |
| mode B (32) | **8.12** | **8.12** | 94 |
| kills (33) | **10.12** | **3.00** | 140 |

  The core has 500 HP. A 94-HP best burst never gets there; a 140 does, repeatedly.
- Their heal crew: in mode B, **~2.99 of their builder bots stand on their own core's 8
  adjacent tiles, on 65.9% of all rounds** (median 659 rounds/game, 1,631 bot-rounds).
  Mode A: 1.10 bots, 14.9% of rounds. Kills: 1.51 bots, 44.4% of rounds.
- The crew is **reactive**: their bot-rounds on their own core ring average **0.197 per
  round before our first core damage and 2.304 after** (mode B). Kills: 0.273 → 1.411.
- Exchange arithmetic (engine constants, not measured here): their heal is **4 HP per
  1 Ti**; our sentinel is **18 dmg per 10 ammo = 1.8 dmg per Ti**. **They undo our damage
  at 2.2× our titanium efficiency**, while out-collecting us ~11:1 in these games.
  **INFERENCE: no damage-side plank wins this exchange on economy.**

### 4B. Mode A: the bodies arrive, the sentinel never does

In the 20 mode-A games our push is *physically present* and does nothing to the core:

- our builder bots spend a **median 696 bot-rounds within d² ≤ 8 of their core**;
- at least one of our bots stands **on one of their 8 core-adjacent tiles for a median 464
  rounds — 46.4% of the game**;
- our builders land a **median 86 attacks within d² ≤ 8 of their core** and **0 on the
  core itself**;
- **but the closest sentinel we ever build to their core has median d² = 292**, and
  **only 1 of 67 mode-A sentinels (1.5%) is built inside sentinel range (r² ≤ 32)**.

| pool | our sentinels built / game | median d² to their core | share inside r²≤32 | median build round |
| --- | --- | --- | --- | --- |
| mode A (20) | 3.35 | **325** | **1.5%** | r202 |
| mode B (32) | 6.19 | 68 | **44.9%** | r229 |
| kills (33) | 5.09 | 58 | **41.7%** | r126 |

**Games that ever have an in-range sentinel: mode A 2/20 (10.0%, CI [0.0, 16.7]) vs
32/32 and 33/33.** That is the cleanest single separation in the whole cut, and the
control comes out the other way absolutely.

Anchor (mode A): `48a8cd27-844c-4afb-be4a-63a90b068f46_game_3.replay26`, icefloe, 1000
rounds — **1,849 of our bot-rounds inside d²≤8 of their core, 862 rounds with a bot in
melee position on it, 37 builder attacks nearby, 0 damage on the core**, closest sentinel
d² = 370.

Anchor (mode B): `7d6db988-f3ec-4a3b-ab88-75e0b413a573_game_1.replay26`, midgard —
**19,872 damage dealt to their core, 19,656 healed back**, min HP 256, **ends at 500**.
Busiest heal round r457: 36 damage in, +32 healed the same round.

Anchor (kill): `be316e8e-fed4-46dd-8886-63fd5fa43405_game_1.replay26`, fimbulwinter,
**111 rounds, 504 damage, 0 heal, 1 in-range sentinel.**

---

## 5. REFUTED MECHANISMS — retained, with the control that killed each

**R1. "TRRR's heal race is the TRRR mechanism." REFUTED as opponent-specific.**
Control pool built by inverting the opponent filter: **45 non-TRRR r1000 losses**, same
our-version era (v165-v179), 11 opponents (Besvikomat 12, I Stone 11, kladde 7, …), same
extractor. Result: **22 of 23 damaged control games also have heal/damage ≥ 0.90**, and
their bots-on-own-core-ring density is **0.71/round vs TRRR's 0.81**. So "the core got
healed back to full" is **what an r1000 loss looks like generically**, not a TRRR trait.
What *is* TRRR-scale is the **volume absorbed**: median core damage **1,026 (TRRR) vs 180
(control)**. ⇒ **The heal ratio must not be reported as the discriminator.** It also
carries a partial tautology (a core that dies cannot be healed past its damage); restricted
to r<150 it is 0.981 (mode B) vs 0.575 (kills), which reduces but does not remove it.

**R2. "A wall/seal denies us anywhere to put a sentinel." REFUTED.**
Free (non-wall, building-free) tiles with a core footprint tile inside sentinel range
r²≤32, median per game:

| round | mode A | mode B | kills |
| --- | --- | --- | --- |
| r100 | 45.5 / 79.5 (57.7%) | 46.0 / 76.0 (63.3%) | 45.0 / 66.0 (63.6%) |
| r200 | 38.5 (48.4%) | 44.0 (58.0%) | 38.0 (51.8%) |

38-46 legal firing sites exist in **every** pool including the 20 mode-A games. Their core
ring *is* sealed — the 12 tiles touching their footprint reach **12/12 their-buildings by
r999, 0 empty from r100 onward** — but the seal does not reach far enough to matter, because
a sentinel shoots from range and **its line ignores obstacles**. Space is not the constraint.

**R3. "Their rebuild loop out-repairs us, so demolition is the stall." REFUTED as the
stall driver, retained as a fact.** Their median rebuild latency on a lost building tile is
**0 rounds** (same-round replacement), p90 50-93 — attacking their belt is close to
worthless. But this is equally true in the kill games (latency median 0, p90 50), so it
does not separate the populations.

**R4. "Poking early wakes their heal crew, so the stall is caused by arriving too soon."
REFUTED — non-monotone.** Stall rate by tercile of first-core-damage round, over the 65
games with any damage: **r8-37 → 62% stalled (n=21); r44-170 → 36% (n=22); r171-492 → 50%
(n=22)**. No direction; the hypothesis is not supported.

**R5. "Their belt attacks destroy our economy." REFUTED in that form.** TRRR lands a
median **947 builderAttacks/game** in the 52 (vs 217 in the 33) and our conveyor losses run
**32 (mode A) / 17 (mode B) / 0 (kills)** per game. But **our harvester count never
collapses** — 3 to 5 alive at every 50-round band through r1000. What collapses is
throughput per harvester (§7). The units survive; the route home does not. **INFERENCE**,
because delivery routing is not directly observable in the replay.

**R6. "It is map-shaped." NOT SUPPORTED.** 21 maps, largest cell n = 9. Stall/kill by map:
fimbulwinter 4/5, valkyrie 4/4, icefloe 5/3, midgard 6/1, bifrost 2/3, longhouse 3/2,
auroraveil 4/1, yggdrasil 4/1, skald 3/2, paths 1/4, helheim 2/2, stavkirke 4/0,
glacierkeep 3/0, plus eight cells of n ≤ 2. Nothing is quotable at these cell sizes and
**no map interval is computed**. **And 13 of the 17 matches contain BOTH outcomes** — since
a match's 5 games are 5 different maps, the fork is per-game, not per-match.

**R7. "It is seat-shaped." REFUTED.** Our seat index: 52-pool **34 B / 18 A (65.4% B)**;
33-pool **21 B / 12 A (63.6% B)**. 1.8pp apart.

---

## 6. Map and seat distributions (item 5), stated as counts only

Seat, from `join.tsv.our_team` cross-checked by the launcher fingerprint (§2.2):
stalls 18 A / 34 B, kills 12 A / 21 B. Maps as listed in R6. **No claim is made in either
dimension** — the seat split is flat and the map cells are too small, and the MAP cluster
the repo's DEFF procedure names is not separately correctable here because a match's five
games sit on five different maps (so MATCH and MAP are near-orthogonal in this pool, and
the per-map cells that would need the correction are n ≤ 9 anyway).

---

## 7. THE DISCRIMINATOR — the r0-100 delivery margin, measured before any game can end

The minimum game length in the 33-kill pool is **111 rounds**, so **at r100 no game in
either population has ended**. Every quantity below is therefore an unbiased matched read
with no survivorship selection.

| quantity, r0-100 | 52-r1000 | 33-kill | AUC |
| --- | --- | --- | --- |
| **our stacks delivered − their stacks delivered** | **−12.3** (med −10) | **+27.2** (med +29) | **0.140** |
| their stacks delivered | 51.9 | 29.4 | 0.724 |
| our stacks delivered | 39.6 | 56.6 | 0.293 |
| their harvesters built | 4.0 | 3.2 | 0.645 |
| our harvesters built | 2.9 | 3.7 | 0.337 |
| **our core damage dealt** | **235.4** | **216.5** | **0.486** |
| their core heal | 222.7 | 142.3 | 0.534 |
| **our in-range sentinels standing** | **0.6** | **0.6** | **0.475** |
| our bot-rounds near their core | 81.6 | 87.2 | 0.473 |
| our ammo converted | 196.3 | 213.3 | 0.408 |

**Read the two bolded rows against each other.** At r100 the *military* state is
indistinguishable — same damage dealt (AUC 0.486), same forward sentinels (0.475), same
bodies in their base (0.473). The *economic* state already separates the populations
(AUC 0.140, i.e. 0.860 in the reverse direction).

Confusion table on the sign of the r0-100 margin (all 85 games):

| | kills | stalls | kill rate | 95% CI (17-match bootstrap) |
| --- | --- | --- | --- | --- |
| margin **> 0** at r100 | 27 | 14 | **65.9%** | [50.0, 81.4] |
| margin **≤ 0** at r100 | 6 | 38 | **13.6%** | [2.4, 27.3] |
| base rate | 33 | 52 | 38.8% | [25.9, 51.8] |

**Difference +52.3pp, CI [36.0, 68.8].** Mean margin, stall minus kill: **−39.5 stacks,
CI [−48.3, −30.8]**. Taking the r0-200 window instead: 70% vs 11%, AUC 0.103.
Sign of the margin predicts the outcome in **65/85 games (76.5%)** against a 61.2%
always-say-stall baseline — a real but not decisive early fork.

### 7A. What the losing margin turns into

Per 50-round band, medians over games still running:

```
                          r0-50  r50-100 r100-150 r150-200 r200-250 r250-300 r300-350 r350-400
52-r1000  our harvesters alive   3.0    3.0     3.0     3.0     4.0     4.0     4.0     4.5
52-r1000  our stacks delivered  18.0   23.0    22.0    19.5    18.5     6.0     0.5     5.0
52-r1000  our stacks / living harvester
                                 5.7    9.7     8.3     5.5     3.8     2.5     0.7     2.3
52-r1000  their stacks          15.0   38.0    46.5    47.0    49.0    59.5    71.0    78.5
33-kill   our stacks delivered  20.0   37.0    38.5    50.0    50.0    70.0    81.0    55.0
33-kill   our stacks / living harvester
                                 5.5   10.4     8.3     8.1     6.9     9.1     9.4     7.9
```

A living harvester routed to the core delivers **12.5 stacks per 50 rounds** (one every 4
rounds). In the stall pool our per-harvester throughput falls **9.7 → 0.0 while the
harvester count holds at 3-5**; in the kill pool it holds at 7.9-10.4. **Our economy does
not die of unit loss, it dies of route loss** (INFERENCE — the route is not directly
observable; the supporting facts are the flat harvester count, the 32-vs-0 conveyor losses,
and TRRR's 947 builderAttacks/game).

Downstream, in the same pool: our ammo conversion floors at **~70-79 Ti per 50 rounds from
r250 onward**, which is almost exactly the passive income (10 Ti / 4 rounds = 125 per 50
rounds). **INFERENCE: past ~r300 we are firing on passive income alone** — ~7.5 sentinel
shots per 50 rounds ≈ **2.7 damage/round**, against a heal crew delivering **8.12
HP/round**. At that point the core arithmetically cannot fall. Our end-of-game ammo
balance in the 52 is a median **24.5** (theirs 187) — we are ammo-empty, not ammo-banked.

### 7B. The gate this shortage most likely closes (source read, CAVEATED)

`bots/_v179rushon/raid.py:386-448` — `_try_forward_sentinel`, the only path that plants a
sentinel whose line already contains an enemy core tile. Its gates, in order:

```
LOKI_FWD_GUN_CAP    = 3     live forward sentinels               (doctrine.py:1219)
LOKI_FWD_MIN_HARV   = 2     "do not open the siege before the economy exists" (:1247)
LOKI_FWD_TI_FLOOR   = 40    bank left AFTER paying for the sentinel           (:1246)
                            (rush waiver only inside r<60: LOKI2_RUSH_* :1391-1394;
                             LOKI2_RUSH_ON is False in v176, True in v179 — 5 of 85 games)
raid.py:415         raider must be within d^2 <= 50 of a core tile
raid.py:422-433     a CARDINAL neighbour of the raider must satisfy
                    can_fire_from(...SENTINEL, core tile) and can_build_sentinel(...)
```

In the 20 mode-A games the proximity gate is plainly satisfied (696 bot-rounds inside
d²≤8) and the harvester gate is satisfied (3-5 alive at every band), which leaves the
**bank floor** and the **cardinal-neighbour LOS/emptiness test** as the candidates.

**HONEST LIMIT — the bank-floor candidate is NOT established.** Our global titanium sits
**below 100 Ti for 94% of rounds r50-400 in both stall modes and 84% in the kill games**
(medians; means 88/85/79%). The floor is chronically near-binding in *every* pool, so the
control comes out only slightly the other way. It is a **plausible contributor, not a
demonstrated cause**, and the cardinal-neighbour geometry test was not instrumented.
**Second caveat: the mapping `bots/_v179rushon` → platform v179 is a repo naming
convention and was not verified against a submission manifest in this cut.**

---

## 8. Content-duplicate check (item 6)

Fingerprint = SHA1 of the full ordered build-event sequence `(round, team, kind, x, y)`
per game, guarded against the rotation re-emit (a build is the first `placeEntity` carrying
a given entity id).

- **84 distinct fingerprints over 85 games. Exact-duplicate share: 2 games = 2.4%.**
- The one pair: `65c33c1e-9e23-443d-8ebf-4b684816f7a9_game_2.replay26` and
  `ceab2431-6e4d-488a-9eed-c4747e7cd563_game_1.replay26` — both **skald, 139 turns,
  `core_destroyed`, won by us, their v45**.
- Looser near-duplicate key `(map, n_builds, turns, our_seat)`: **3 groups of 2 = 6 games
  (7.1%)** — skald/42/139, yggdrasil/344/1000, bifrost/136/162.

**Compare 17.3% in BC's v47 field pool** (`CUT-116-beltgun-answer-2026-08-21.md` §1.7).
This pool is an order of magnitude cleaner, so the CONTENT-DUPLICATE cluster is **not**
applied to the intervals above; the MATCH cluster is (§1). Removing the two duplicate
games does not move any headline (both are kills, 2 of 33).

---

## 9. Answer to the row's question, and what #120(b) should do

### The mechanism, stated plainly

**There is no single stall mechanism, and the one that was easiest to reach for is wrong.**

1. **The stall is not a wall.** Their core ring is fully sealed by r100 and it is
   irrelevant — sentinel fire ignores obstacles and 38-46 legal firing sites exist in every
   pool (R2).
2. **The stall is not "their heal rate is special".** Heal-answers-damage is what *every*
   opponent's r1000 loss looks like (22/23 in an 11-opponent control) (R1).
3. **The stall is our own r0-100 economy losing, and everything else follows.**
   The single discriminating quantity measured before any game can end is the
   **delivery margin in rounds 0-100**: −12.3 stacks in the stalls vs +27.2 in the kills,
   AUC 0.140, kill rate 65.9% vs 13.6% by its sign (+52.3pp, CI [36.0, 68.8]).
   At that same round the *military* state is indistinguishable (damage AUC 0.486,
   in-range sentinels 0.475).
4. **The two stall modes are the two ways that shortage cashes out** (INFERENCE for the
   causal link; the components are each measured):
   - **Mode A (20/52)** — the forward-sentinel gate never opens: only 2/20 games ever have
     a sentinel inside r²≤32, against 65/65 elsewhere. Bodies are in their base for 46% of
     the game and do nothing to the core.
   - **Mode B (32/52)** — the sentinel arrives, then runs out of ammo. Our fire decays to
     passive income (~2.7 dmg/round) while their reactive 3-bot heal crew delivers
     8.12 HP/round. Median 2,004 damage, 2,004 healed, core ends at 500.
5. **The fork is readable early.** By r100 the economic sign is set; by r150 the net dent
   has already diverged (mean 17 vs 164). It is not a slow grind that could have gone
   either way at r600 — 48 of 52 stalls never net more than 0 damage all game.

### What #120(b) should build — and the tree-crossing warning first

⚠ **CROSSES TREES.** Every number above is Mjolnir v176/v179 (x3r0's holder). The Skalman
head `bots/_v622nestfall` has a different economy, a different siege path and a different
turret doctrine. **Nothing here is a measured claim about Skalman.** What transfers is the
*opponent-side arithmetic* (TRRR's heal exchange rate and their zero core-attack
behaviour), which is a property of TRRR, not of us.

**Recommendation: do NOT build a TRRR-specific counter. The row's condition for (b) —
"only if (a) names a mechanism the head's existing stall plan-B does not answer" — is not
met in the shape the row anticipated.** The row anticipated "a wall/heal shape"; the decode
says the shape is our own early economy, which is a general plank and not a TRRR counter.
Three concrete consequences:

- **The r1000 stall against TRRR is not a defence problem and not a turret problem.** A
  plank that adds damage loses on arithmetic: their heal is 4 HP/Ti, our sentinel is
  1.8 dmg/Ti, and they out-collect us ~11:1 in these games. **INFERENCE: no damage-side
  plank wins this exchange.**
- **The only mechanically live counter is healer denial, and Mjolnir already runs it at
  ~1/20th of the needed dose.** MEASURED: our launchers performed **740 builder tosses of TRRR bots (the mechanic historically called "kidnap" in this repo) — 740 lifts of TRRR
  builder bots across the 85 games (8.7/game)**, of which **234 (31.6%) lifted a bot
  straight off their own core ring**, moving it from median d² 5 to d² 53 (~7 tiles).
  In the heal-race pool that is **95 evictions over 32 games ≈ 3 per game**, against a
  crew present for ~660 rounds per game. Each eviction buys roughly the victim's walk-back
  (~7+ rounds × 4 HP ≈ 28 HP). **To beat 500 HP the ring has to be held clear, not poked
  three times.** If anything is built for this class, it is *sustained* ring eviction by a
  launcher parked on their core ring — and that is an existing approved-class mechanism
  (the launcher builder-toss, approved 2026-08-10), so it needs no new organiser question, only a dose.
- **The higher-value item is the general one:** whatever holds our delivery route open
  through r100-300 against a belt-harassing farm bot. In this pool that alone flips a
  13.6% kill rate to 65.9%. It is not a TRRR plank; it is an economy-robustness plank, and
  it should be priced against the whole field, not this pairing.

### Open cells this cut did not close

1. **Why the mode-A forward-sentinel gate stays shut** — bank floor vs the cardinal-
   neighbour LOS/emptiness test at `raid.py:422-433`. Distinguishing them needs a
   per-round instrumented replay of the raider's candidate sites, not an aggregate.
   (And the local-tree → platform-version mapping needs verifying first.)
2. **Whether our delivery collapse is route breakage or a build-order choice** — the route
   is not observable in the replay; the flat harvester count and the 32-vs-0 conveyor
   losses are consistent with breakage but do not prove it.
3. **Their v48**, shipped ~11:01Z on 2026-08-22, is entirely unmeasured. All 85 games here
   are v44/v45. A v45 pin via `fcode match unrated <team> --match <past_match_id>` remains
   available if (b) is ever run.
4. **The `hostile` flag on rebuild events** uses a last-hit cache that is never cleared;
   the "rebuild followed a hostile hit" shares are **EYEBALL**, not measured.

---

## 10. Reproduction

```bash
# pool + file list
.venv/bin/python - <<'PY'
import csv
rows=[r for r in csv.DictReader(open('corpus/ladder_games.tsv'),delimiter='\t') if r['opp']=='TRRR']
for r in rows: print('replay_archive/'+r['s3'])
PY
# extraction (read-only over replay_archive)
.venv/bin/python scratchpad/s56_trrr_extract.py $(cat scratchpad/s56_trrr_files.txt) \
    > scratchpad/s56_trrr_games.jsonl
# instrument control
S56_CORRUPT=teamswap .venv/bin/python scratchpad/s56_trrr_extract.py \
    $(cat scratchpad/s56_trrr_files.txt) > scratchpad/s56_trrr_games_SWAP.jsonl
```

`scratchpad/s56_trrr_an.py` carries the pool join (`ladder_games` × `join` × the JSONL) and
the `report()` helper; the per-section analyses were run as one-off scripts against it and
are reproducible from the numbers and definitions stated inline above.
