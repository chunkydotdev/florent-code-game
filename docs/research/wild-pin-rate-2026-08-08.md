# Wild pin-rate: how often does SLOT_UNDER latch on sightings alone with zero core damage?

Research arm, 2026-08-08 ~16:53 UTC. Repo HEAD `380633f`. Read-only: no bot edits, no
arena, no downloads — everything below comes off `replay_archive/` as it sits on disk.

**Version tags**

| thing | path | md5 |
| --- | --- | --- |
| live v80 "Eir 9b" | `bots/_v89sh/main.py` | `e12f85855654e9e78227582d0dc15d4b` |

All source line-cites below are `bots/_v89sh/main.py`, this exact file.

**Purpose.** The bot latches `SLOT_UNDER` (binary) on enemy *sightings* near our Core
and, once latched, holds it for up to 50 idle rounds, gating expensive posture (builder
recalls, heal-over-economy, economy caps). A proposed redesign wants severity tiers so
cheap responses stay sighting-triggered while the expensive tier requires evidence of
actual damage. **This note prices that redesign**: how often, in wild games, does the
binary latch pin posture for a large share of the game while the opponent never lands a
hit on our core?

---

## Verdict up front

**The pin-without-damage shape is real, recurring, and concentrated — not diffuse
noise — but it is a minority shape overall.** At the `armed ≥ 80%` cut, **8/150 = 5.3%**
of wild v77+-era ladder games show the latch armed for at least 80% of the game while
our core takes **zero** damage during every armed round. Rarer at tighter cuts (3.3% at
≥95%), more common at looser ones (8.7% at ≥50%) — see the full distribution below.

**The number that decides the price is the duration split, not the raw rate.** The 8
zero-damage-pinned games split cleanly in two:
- **4 are full 1000-round games against one opponent (Ouroboros), and we lost all 4 on
  the titanium-collected tiebreak** — the posture stayed pinned defensively for the
  entire game against a threat that never fired a shot that landed, and we lost the
  economic race that the redesign's own PURPOSE text names ("economy caps") as one of
  the gated behaviours.
- **The other 4 are decisive core-destroyed wins** (110–580 rounds) where we killed the
  enemy core before the wasted posture had time to cost anything.

So: when the pin-without-damage shape survives long enough to matter, it correlates
**100% (4/4)** with a loss. That is the Elo-relevant number, not the headline 5.3% —
most instances of the shape are harmless because the game ends first.

**Would tiers help?** Yes, substantially, even short of the zero-damage extreme. Across
all 150 v77+ ladder games, switching the *expensive*-tier gate from "any sighting in the
last 50 rounds" to "any core damage in the last 50 rounds" would cut expensive-tier armed
time by a **mean 41.2% / median 29.4%** — and for the 86 games that are pinned (≥80%
armed) under the current binary latch, damage-freshness gating still cuts their armed
time by a **mean 40.0% / median 25.7%**. In the 8 zero-damage-pinned games specifically,
a damage-freshness gate would release the expensive tier **100% of the time** (it would
never arm at all, since no damage ever occurs).

Reading straight off the PURPOSE framing in the task: this is **not a correctness
nicety**. It is a specific, opponent-concentrated failure mode (Ouroboros, our single
worst matchup at 1-14 in the v77+ ladder cohort) where the binary latch keeps us
defensively postured for entire full-length games against a threat that is present but
inert, and we lose those games on the economy tiebreak the gated behaviours were
supposed to protect. It is a minority of games (5.3%) but a real, recurring, and costly
minority.

---

## 1. Trigger geometry (confirmed from source, live v80)

| branch | condition | cite |
| --- | --- | --- |
| Core self-scan | enemy GUNNER/SENTINEL, `d² ≤ 64` of Core's own position | `:1518-1522` |
| Core self-scan | enemy BUILDER_BOT, `d² ≤ 16` | `:1526-1530` |
| Core self-scan | our Core's HP drops this round | `:1531-1533` |
| Builder scan | enemy GUNNER/SENTINEL within `gun_sense`, enemy BUILDER_BOT within `b_sense`, **measured from `self.core`**, which is `ct.get_position(eid)` on the CORE entity | `:2003-2027` |
| Latch decay | `SLOT_ATK_RND` refreshes on every trigger; latch clears after 50 consecutive rounds with none | `:1541-1548`, mirrored at the builder-scan writer |

`d` is measured from the Core's **NW-corner anchor**, not the 2×2 footprint (confirmed
independently 2026-08-08 in `docs/research/fjordgate-collapse-owner-2026-08-08.md`; this
note's parser reproduces that anchor exactly, from `Map.CorePosition.position`, the same
field `ct.get_position()` returns for a Core entity).

**`gun_sense`/`b_sense` are 64/16 in every wild v80 game, never the 100/36 "big square"
variant.** `self.gun_sense = 100 if (B8_ON and _big_square) else 64` and the matching
`b_sense` line (`:1945-1946`) are the only assignment sites besides the constructor
default (`:1345-1346`, also 64/16); `B8_ON = False` (`:451`), verified by grepping every
`B8_ON` occurrence in the file — nothing else touches it. So the two branches (core
self-scan and builder scan) use **identical geometry**: enemy turret `d²≤64` OR enemy
builder `d²≤16` OR our Core HP drop, unified. This note measures that one geometry, with
the 50-round decay tail, directly from replay entity positions — it does not depend on
any in-bot debug print (the live v80 bot has none; the `IN r=...` instrument line
referenced in the task's `fjord_disc/instr.py` bundle only exists in dev-arm builds used
for a different, det-seeded study and was not reused here).

---

## 2. Corpus

`replay_archive/` as of this read: 546 `*.meta.json`, 2,731 `*.replay26`. Filtered to
matches where `teamAName == "OpenSverige"` or `teamBName == "OpenSverige"` (seat fixed
for the whole best-of-five and `teamAName` is always engine `TEAM_A`, per
`docs/research/bo5-seat-assignment-2026-08-08.md` — used directly, no re-derivation
needed): **222 matches**, all with 5/5 replay files present.

| cohort | matches | games | note |
| --- | --- | --- | --- |
| **v77+ ladder (headline)** | 30 | **150** | our `teamVersion ∈ {77,78,79,80}`, `triggeredBy == 'ladder'` — the current trigger-radius code, rated |
| v77+ unrated (secondary) | 9 | 45 | same code, excluded from headline per instructions |
| pre-v77 ladder (secondary) | 134 | 670 | our `teamVersion` 64–76, earlier/partially-different latch code (35-round decay pre-v79, per source comment `:1541-1548`) |

Opponents in the v77+ ladder headline cohort (15 distinct): Kings College Munich,
Lunds Stallions, Focalground, Ouroboros, Memtrace (15 games each — 3 matches per
opponent), Askar City, Team 48, CtrlAltDefeat (10 each — 2 matches), Leviathan,
Powerpuff Girls (10 each), opensverige - plan B, arsonist duck, The Bisons, Banminary,
0033 (5 each — 1 match).

---

## 3. Method

Per game: replayed `PlaceEntity` / `MoveBuilderBot` / `RemoveEntity` / `UpdateHp` /
`UpdatePlayers` / `DistributeResources` to track live entity positions, our Core's HP
deltas (64-bit two's-complement decoded), and titanium delivered. Per round, evaluated
the unified trigger geometry above against the current entity snapshot; modeled
`SLOT_UNDER` with the 50-round decay tail (`armed(r) = trigger(r) OR (r - last_trigger <
50)`). A second, alternative model — **damage-freshness gating** — substitutes "any core
damage in the last 50 rounds" for "any sighting in the last 50 rounds," to quantify what
requiring evidence for the expensive tier would do.

---

## 4. Trigger occupancy: armed-fraction distribution (v77+ ladder, n=150)

| stat | value |
| --- | --- |
| any trigger at all | 148/150 (98.7%) |
| never triggered | 2/150 (`Powerpuff Girls` g2, `0033` g1 — both short/clean games) |
| min / p25 / median / p75 / max armed fraction | 0.000 / 0.539 / 0.836 / 0.969 / 0.999 |
| mean armed fraction | 0.721 |

So the latch is armed for *most of the game* in the median case — that alone is not the
interesting number (a single early trigger plus the 50-round tail keeps it loosely
engaged most of a 1000-round game against almost any opponent that ever gets a builder
or turret near our home). The interesting number is what happens **while** it's armed.

---

## 5. Headline metric: pin-without-damage, at three cut lines

"Pinned": armed fraction ≥ cut. "Zero-damage-in-armed": our Core takes 0 total damage
across every round the latch is armed (equivalently: 0 damage all game, since the
geometry latches on any HP drop too — a nonzero-damage round is always itself a trigger
round). No game had damage strictly between 0 and 5 (smallest single hit is 7, a
gunner shot), so "zero" and "≤5, i.e. negligible" are identical buckets throughout.

| cohort | cut | pinned | pinned & zero-damage | rate |
| --- | --- | --- | --- | --- |
| **v77+ ladder (headline)** | ≥50% | 116/150 | 13 | **8.7%** |
| **v77+ ladder (headline)** | **≥80%** | 86/150 | **8** | **5.3%** |
| **v77+ ladder (headline)** | ≥95% | 44/150 | 5 | 3.3% |
| v77+ unrated (secondary) | ≥50% | 39/45 | 5 | 11.1% |
| v77+ unrated (secondary) | ≥80% | 27/45 | 3 | 6.7% |
| v77+ unrated (secondary) | ≥95% | 11/45 | 0 | 0.0% |
| pre-v77 ladder (secondary) | ≥50% | 565/670 | 50 | 7.5% |
| pre-v77 ladder (secondary) | ≥80% | 441/670 | 35 | 5.2% |
| pre-v77 ladder (secondary) | ≥95% | 256/670 | 17 | 2.5% |

**The pre-v77 cohort agrees closely with v77+ at every cut** (5.2% vs 5.3% at ≥80%) —
this is not an artifact of one era's code; it is a stable property of the geometry and
the field the bot plays against, largely undisturbed by the 35→50-round decay change.

---

## 6. Duration distribution (v77+ ladder, ≥80% cut)

| bucket | pinned (86 games) | pinned & zero-damage (8 games) |
| --- | --- | --- |
| short (<200 rounds) | 24 | 2 |
| mid (200–599 rounds) | 30 | 2 |
| long (600–1000 rounds) | 32 | **4** |

Median game length overall: 366.5 rounds. Median length of a pinned (≥80%) game: 444
rounds — pinned games skew longer, as expected (more rounds for a threat to be sighted
once and for the 50-round tail to keep re-arming).

**The 8 zero-damage-pinned games, individually:**

| match | game | opponent | rounds | armed frac | win condition | outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `d694094e` | 3 | Ouroboros | 1000 | 0.937 | titanium_collected | **loss** |
| `d694094e` | 4 | Ouroboros | 1000 | 0.919 | titanium_collected | **loss** |
| `78dd80a3` | 3 | Ouroboros | 1000 | 0.823 | titanium_collected | **loss** |
| `78dd80a3` | 4 | Ouroboros | 1000 | 0.952 | titanium_collected | **loss** |
| `1e8c4e1b` | 2 | Kings College Munich | 580 | 0.998 | core_destroyed | win |
| `b4287ac4` | 3 | CtrlAltDefeat | 218 | 0.991 | core_destroyed | win |
| `208e84f8` | 5 | Memtrace | 110 | 0.964 | core_destroyed | win |
| `2874c55e` | 3 | Memtrace | 110 | 0.964 | core_destroyed | win |

**Every full-length (1000-round) zero-damage-pinned game is a loss; every
decisive-win game is short.** The pattern is not "the pin causes the loss" in a
mechanically proven sense — Ouroboros beats us broadly (see §7) — but it is the only
subgroup where the shape had 1000 rounds to matter, and in all 4 of those rounds we lost
the exact tiebreak (`titanium_collected`) that a "heal-over-economy / economy caps"
gate would be protecting or sacrificing.

---

## 7. Per-opponent table (v77+ ladder, n=150)

| opponent | games | W-L | mean armed frac | pinned ≥80% | zero-dmg-pinned @80% |
| --- | --- | --- | --- | --- | --- |
| **Ouroboros** | 15 | **1-14** | 0.832 | 12 | **4** |
| Kings College Munich | 15 | 7-8 | 0.773 | 9 | 1 |
| Lunds Stallions | 15 | 5-10 | 0.931 | 13 | 0 |
| Memtrace | 15 | 12-3 | 0.733 | 9 | 2 |
| Focalground | 15 | 4-11 | 0.359 | 2 | 0 |
| Askar City | 10 | 8-2 | 0.811 | 7 | 0 |
| CtrlAltDefeat | 10 | 7-3 | 0.881 | 8 | 1 |
| Team 48 | 10 | 4-6 | 0.821 | 6 | 0 |
| Leviathan | 10 | 9-1 | 0.422 | 2 | 0 |
| Powerpuff Girls | 10 | 2-8 | 0.698 | 4 | 0 |
| opensverige - plan B | 5 | 5-0 | 0.703 | 3 | 0 |
| arsonist duck | 5 | 1-4 | 0.495 | 2 | 0 |
| The Bisons | 5 | 3-2 | 0.701 | 2 | 0 |
| Banminary | 5 | 4-1 | 0.892 | 4 | 0 |
| 0033 | 5 | 2-3 | 0.684 | 3 | 0 |

**Ouroboros produces half (4/8) of the zero-damage-pinned games in the whole cohort,
and is our single worst matchup (1-14).** It is a strong opponent overall (1053
matches played, ~1598 rating vs our ~1568-1598 across these games) — the pin shape
is not the sole explanation of the record — but it is the opponent where the shape
recurs, is full-length, and coincides with a loss every time. No other opponent
produces more than 1 instance of the shape, and none produces it in a full-length loss.

**The known wild exemplar named in the task (v78 vs "Landers")** is confirmed present
but falls in the **unrated** secondary cohort: match `a3e6dd54…`, game 1, v78, meander
opponent Landers — rounds=1000, armed=0.919 the entire game, **0 core damage all
1000 rounds**, `turret_present_no_dmg` in 919/919 trigger rounds, `win_condition =
titanium_collected`, and we lost it. Same shape as the Ouroboros cases: a parked
turret sits in range, never lands a hit, and the game resolves on the economy
tiebreak. Excluded from the headline rate per instructions (unrated), reported here
because it independently corroborates the mechanism. `cad_probe`, our frozen practice
opponent, is excluded entirely — it is not in this corpus (wild only).

---

## 8. Would the tiers help? (§5 of the task)

Classified every trigger-round in the 86 pinned (≥80%) v77+ ladder games by what was
actually present:

| cause | share of trigger-rounds in pinned games |
| --- | --- |
| enemy turret present, 0 damage this round | 59.0% |
| our Core took damage this round | 31.7% |
| enemy builder present (d²≤16), 0 damage this round | 9.3% |

**Roughly 68% of trigger-rounds in pinned games are "enemy present, nothing landed"**
— exactly the population a damage-freshness requirement targets. Simulating a
damage-freshness gate (expensive tier armed only if Core damage occurred within the
last 50 rounds, same decay constant) against the same 150 v77+ ladder games:

| cohort | mean reduction in expensive-tier armed time | median reduction |
| --- | --- | --- |
| all 150 games | 41.2% | 29.4% |
| the 86 pinned (≥80%) games | 40.0% | 25.7% |
| the 8 zero-damage-pinned games | **100%** (never arms) | 100% |

This is not an all-or-nothing question — even in games where the enemy does eventually
land a hit, the current sighting-only latch keeps the expensive tier engaged roughly a
quarter to two-fifths longer than a damage-recency gate would. The zero-damage subset is
the clean floor: a damage-freshness expensive tier would never engage at all for those 8
games, releasing builder recalls / heal-over-economy / economy caps for their full
duration, all while the cheap (sighting-only) tier remains untouched by this proposal
and keeps reacting the instant an enemy is sighted.

---

## 9. Pricing verdict

**Worth real Elo, concentrated rather than diffuse.** The raw pin-without-damage rate
(5.3% of v77+ ladder games at the ≥80% cut) reads small in isolation, and most instances
of the shape (short/decisive wins) don't have time to cost anything — so taken as a flat
rate this would look like a correctness nicety. **The number that overturns that
reading is the duration-conditioned one: every full-length instance of the shape (4/4)
coincides with a loss, and half of all instances (4/8) come from a single opponent
(Ouroboros) who we lose to at 1-14 — our worst wild matchup in this era, with a real
independent corroboration in the unrated Landers game the task pointed at.** A binary
latch that stays pinned for 1000 rounds against a threat that never lands a hit, on our
single worst matchup, gating exactly the economy behaviours we then lose the tiebreak
on, is a specific, identifiable, and recurring cost — not noise.

Second supporting number: the damage-freshness simulation shows the redesign isn't a
narrow edge-case fix — it changes expensive-tier armed time by ~30-40% on the *median*
game, pinned or not, because ~68% of trigger-rounds in pinned games are sightings with
nothing landing. The release isn't confined to the 8 extreme games; it's a broad
tightening with an extreme, well-evidenced tail.

**What would change this verdict:** if Ouroboros-style opponents (patient, turret-heavy,
economy-race play) are rare going forward on the ladder, the concentrated cost shrinks
toward "rare, but still worth shipping given it's cheap to add." If a future decode shows
the tiebreak losses in the 4 full-length games were decided by something else entirely
(e.g., harvester count or titanium-stored, not the defensive posture itself), the causal
story weakens to correlation-only — worth stating explicitly: **this note establishes
correlation (100% of full-length pin-without-damage games are losses, on the exact
tiebreak metric the gated behaviours protect) and mechanism plausibility (the redesign's
own stated targets — heal-over-economy, economy caps — are literally the behaviours kept
engaged), not a proven causal chain from "latch stayed armed" to "we lost."** A clean
causal read would need an ablation (replay or re-simulate the same games with the
tiered gate) rather than another correlational pass over the same games.

---

## 10. Self-checks

| check | result | method |
| --- | --- | --- |
| **Parser end-to-end validation** | **1110/1110 team-sides, 0 mismatches**: `core_deliv × 10 == titaniumCollected` exactly, across every game in the full 222-match OpenSverige corpus (not just v77+) | computed both quantities independently per game (`DistributeResources` moves landing on our Core footprint, vs `UpdatePlayers.titaniumCollected`) and diffed |
| Parse errors | 0/1110 games | try/except around every game parse, none raised |
| All 5 replay files present per match, v77+ era | 195/195 (30 matches × 5, plus 9 × 5 unrated = 195 checked) | filesystem existence check before parsing |
| Seat/team mapping | used directly from `docs/research/bo5-seat-assignment-2026-08-08.md` (`teamAName` == engine `TEAM_A`, fixed per match, 583/583 + 158/158 validated there) | no re-derivation; cited, not re-measured |
| Core anchor vs footprint | anchor used throughout (`Map.CorePosition.position`, the NW corner), matching `docs/research/fjordgate-collapse-owner-2026-08-08.md`'s finding and `tools/replay_schema.md`'s documented convention | source read + schema doc cross-check |
| `gun_sense`/`b_sense` always 64/16 in live v80 | confirmed: `B8_ON = False` (`:451`), the only other assignment site is gated `if (B8_ON and _big_square)` (`:1945-1946`) | `grep -n B8_ON bots/_v89sh/main.py` — 3 hits, none elsewhere |
| Damage decode | 64-bit two's-complement (`delta -= 2**64` when `delta >= 2**63`) | per `tools/replay_schema.md` UpdateHp convention, matches prior notes' method |
| "Negligible" vs "zero" damage buckets are identical | confirmed: no game had 1 ≤ damage ≤ 5; smallest possible single hit is 7 (gunner) | swept both thresholds over the full result set, byte-identical counts at every cut |
| `fjord_disc/instr.py` reuse | **not reused for the wild measurement** — its `SLOT_UNDER` extraction depends on a Core `BotOutput` debug print (`IN r=...`) that only exists in instrumented dev-arm builds (`_v93w`/`_v93wb` variants for a det-seeded probe study), not in the live v80 bot or in wild replays. This note's parser recomputes the trigger geometry directly from entity positions instead, which is more robust (works on every wild game, not just instrumented ones) | source read of `instr.py` + grep for the `IN r=` print pattern in `bots/_v89sh/main.py` (absent) |
| Known wild exemplar (Landers) | reproduced independently: same match id family, same shape (zero damage, high armed fraction, titanium_collected loss); this note's metric (core damage received) differs from `docs/research/meander-delivery-owner-2026-08-08.md`'s Q4 metric (titanium *delivered by us*) — related but distinct measurements of the same underlying game, not a re-derivation of the same number | cross-referenced by match id and manual inspection of both notes' criteria |

---

## Confidence

High on the mechanical numbers (parser validated end-to-end at 1110/1110, geometry
read directly from the live source with line cites, latch/decay model matches the
source's own logic exactly). Medium on the causal story in the pricing verdict — the
4-full-length-games-all-losses pattern is a strong, specific, well-evidenced
correlation with a plausible mechanism (the redesign's own stated gate targets), but
n=4 is small and this note does not run a counterfactual (replaying those games with a
tiered gate) to prove the posture itself, rather than opponent strength generally, was
the decisive factor.
