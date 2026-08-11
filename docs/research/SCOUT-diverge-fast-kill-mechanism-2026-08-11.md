# SCOUT — diverge's fast core-kill mechanism, reconstructed from the wire

Side lane, 2026-08-11. Read-only commission: extract *how a fast core kill is
executed*, as a mechanism we could adopt. `PLAY_DEFENCE: never` — nothing below
is a defensive recommendation, and where the evidence only supports a defensive
fix it is called out as a null.

**No plank is proposed and no verdict is issued.** This is a mechanism read-out.

Clock: analysis run 2026-08-11T08:34:15Z (`date -u`, same shell). Repo at
`1ccc20b7a223fd0febaccdd73398f1a843205e90` (2026-08-11T10:34:13+02:00).

---

## 1. Coverage, population, n

**Population A — diverge vs us (rated ladder only, `corpus/ladder_games.tsv`).**
100 games across **20 matches**, 2026-08-09T05:02Z → 2026-08-11T06:33Z, 15 maps.
Record: we won 43, lost 57. **The independent unit is the MATCH (n=20), not the
game** — five games share a pairing, a map set and both bot versions.

| class | games | archived + decoded |
|---|---|---|
| they killed our core, turns < 250 (`DV_FASTLOSS`) | 51 | **49 (96.1%)** |
| they killed our core, turns ≥ 250 | 6 | 6 |
| we killed their core, turns < 250 | 35 | 34 |
| we won slow / on tiebreak | 8 | 7 |

⚠ **Two corrections to the commissioning brief.** Coverage of the 51 fast losses
is **49/51 = 96.1%, not 100%** (`replay_archive/` is missing two). And the median
kill round over those 51 is **r92**, not r103 (p25 80, p75 126, min 59, max 226).
Neither changes the shape of the finding.

**Population B — diverge vs third parties.** 300 archived games from
`corpus/meta_join.tsv` where diverge played someone other than us (40+ opponents,
ladder and unrated mixed). Used only for Control 2, never for a rate about us.

**Population C — our own fast core-kill wins.** `ladder_games.tsv` has 957 games
we won by `core_destroyed` inside r250; **677 are archived (70.7%)**, 643 after
excluding diverge. Version mix is wide (v104 157, v102 125, v80 61, v72 36, …),
so every Control-3 number is also reported **restricted to v102/v104 (n=282)**,
the versions that actually played diverge.

**diverge's own versions are NOT pinned by `ladder_games.oppver` — it is NULL for
all 100 games.** Recovered from `corpus/league_matches.tsv` instead: diverge
shipped **15 versions** in the window (v1 on 08-08T19:42Z → v12/v15 by 08-11).
Section 6 shows the mechanism is stable across all 11 versions we hold replays
for, which is why pooling them is defensible.

---

## 2. Instruments, and the checks that could have failed

Everything below is decoded from the raw `.replay26` wire with the repo's own
primitives (`tools/replay_census.py`: `fields`, `read_pos`, `parse_entity`), per
`tools/replay_schema.md`. Scripts: `scratchpad/dv_timeline.py` (build/death/
fire/attack/HP/economy timeline), `scratchpad/dv_throw.py` (throws with
destination tiles). **Not committed; they are scratch instruments.**

**Team byte → seat mapping.** Nothing in the repo documents whether the `team`
byte in `corpus/builds.tsv` / `events.tsv` is `a`/`b`. Derived and driven both
ways: over **13,440 archived games with exactly one core death**, winner side `a`
⇔ dead core `team == 1` (7,085) and winner side `b` ⇔ dead core `team == 0`
(6,355), **0 exceptions**. So **TEAM_A == 0, TEAM_B == 1**. Both cells are
populated, so this is a check that could have come out the other way.

**Our own side.** `meta_join.us_side` where present; otherwise derived as
`winner_seat if won else the other seat`. The derivation agrees with
`meta_join` on **2,360/2,360** overlapping games, 0 mismatches.

**Core-damage attribution** (which unit hit the core, per round). `fireTurret`
carries only `from`/`to`, so the source is resolved by looking up the building
occupying the `from` tile; `builderAttack` carries the bot id. Validated against
the engine's own `updateHp` deltas on the core:

* With the true damage table (sentinel 18 / gunner 7 / builder 2), **99.80% of
  159,449 round-cells are fully explained** (the residual is heal-in-the-same-
  round, positive and truncated at max HP). Under-attribution: 325 cells.
* **Negative control 1** — swap gunner and sentinel damage: failures jump from
  325 to **44,736 cells (28.1%)**.
* **Negative control 2** — zero damage table: **83,772 cells (52.5%)**.
* **Negative control 3** — builder attack = 5 instead of 2: passes the
  under-attribution test (it over-attributes) but fails the modulo-4 heal test
  40,185 vs 13,431. Both directions of error are therefore detected.
* **End-to-end ledger:** on every game where a core died, *damage delivered +
  net HP change* closes at **−500 to −517 HP, 49/49 and 643/643** (the ≤17
  overshoot is the killing blow). The chain is sound.

**A detector I built, checked, and then DROPPED.** "Is the forward sentinel
placed on an 8-way firing line through the enemy core footprint?" scored 100%
(diverge) / 96.9% (us) — but the **null for random in-range tiles is 72.5%**
(20,000 draws). A near-constant column validates anything. Not reported as a
finding.

**Positive controls the commission specified, both came out right:** we *do*
build forward sentinels → detected in 74–94% of our fast wins; we do *~zero*
builder melee → 15% all-versions, and section 5 shows the detector fires 19,090
times on our older versions, so the zero is not a decoder gap.

---

## 3. The mechanism, reconstructed

### 3.1 One game end to end (`67f7806c…_game_5`, map `lighthouse`, our v104, we die r59 — the fastest of the 51)

Cores at (3,3) diverge / (11,11) us, d² = 128 apart (12 tiles).

```
r0–r3   diverge spawns FOUR builder bots (r0, r1, r2, r3) and lays 1 conveyor
r4      barrier at (5,3) — orthogonally adjacent to its OWN core footprint
r8      SENTINEL at (8,7): d²=25 to OUR core, i.e. inside sentinel range 32,
        and diagonally in line with our footprint tile (12,11)
r9–r13  conveyors + first harvester at home (r13)
r12     first damage to our core — 18 every 2 rounds from that one sentinel
r14     a diverge builder arrives at (11,10): d² = 1, orthogonally adjacent to
        our core footprint. It never leaves.
r15     LAUNCHER at (10,11): d² = 1 from our core, sitting on our spawn ring
r15+    the parked builder attacks the core EVERY round: 2 dmg / 2 Ti
r15–r58 grind at ~11 dmg/round while the launcher throws away every builder we
        spawn next to the core
r58     our core dies
```

Our side that game: harvesters and conveyors at home from r4, two barriers next
to *their* core at r20/r21 — and **zero damage to their core all game**.

### 3.2 The same thing, over all 49 fast losses

Every number is the diverge side of the 49 archived fast losses; dispersion is
min / p25 / **MED** / p75 / max.

| plank | present | round it lands |
|---|---|---|
| 4 builder bots by r5 | 49/49 (100%) | r0, r1, r2, r3 (modal, exact) |
| barrier adjacent to **own** core | 43/49 (88%) | 4 / 4 / **4** / 4 / 6 |
| first conveyor (home economy) | 49/49 | 1 / 2 / **4** / 6 / 10 |
| **forward sentinel inside range of our core** | 42/49 (86%) | 3 / 14 / **19** / 27 / 164 |
| **launcher within d²≤8 of our core** | 33/49 (67%) | 6 / 13 / **19** / 28 / 146 |
| **builder parked on our core, attacking** | 47/49 (96%) | 8 / 14 / **26** / 33 / 145 |
| first harvester (home) | 48/49 | 5 / 9 / **12** / 16 / 25 |
| **first damage to our core** | 49/49 (100%) | 5 / 9 / **13** / 23 / 38 |

Composition and clock:

* **Distinct sources that hit our core:** 1 / 3 / **4** / 4 / 7 per game —
  1.76 sentinels, 1.69 melee builders, 0.29 gunners on average.
* **Damage share:** sentinel **80.9%**, builder melee **14.4%**, gunner 4.7%.
* **Where they shoot from:** d² to our core 1 / 2 / **5** / 25 / 41. Median 5 is
  *diagonally adjacent to the footprint*. d² to their **own** core: median 122.
  The weapons are built at our house, not theirs.
* **Grind, not burst:** span from first damage to our core's death is
  38 / 56 / **76** / 112 / 208 rounds at **9.87 dmg/round** (median).
* **They deliver a median 776 HP to kill a 500 HP core** — we heal a median 272
  HP back and it does not matter, because their emplacement out-produces it.
* **Melee persistence:** the parked builder attacks for a median of **41 rounds**
  per game, longest unbroken run median **26 rounds**.

### 3.3 The launcher, which is the part we do not have at all

diverge builds **essentially exactly one launcher per game** (299 launchers in
300 third-party games) and parks it on the **enemy** core: d² to enemy core
1 / 4 / **5** / 9 / 277; **94.3%** of their launchers are closer to the enemy
core than to their own.

What it does, measured from `moveBuilderBot` steps with manhattan > 1 attributed
to an adjacent launcher:

* **712 throws of OUR builder bots** across the 49 fast losses (41/49 games have
  at least one), first throw at median **r15**, median **10 throws/game**, max 53.
* **712 of 712 (100%) push the bot AWAY from its own core**, by a median of
  **+43 d²** (roughly 5–6 tiles). Third-party games: 3,790 of 3,793 (99.9%).
* Only **11.7%** land on a map-border tile, so this is **not** LOKI-14-style
  crash induction. It is displacement: the defender's builders are removed from
  the tile where they could heal the core or kill the emplacement, every time
  they arrive, for 0 ammo and a +1 cooldown.

**That is the load-bearing insight.** The sentinel + melee pair only produces
~11 dmg/round; 500 HP takes ~50 rounds. Fifty rounds of uninterrupted grind
next to a live enemy core is not free — it is bought by the launcher, which
denies the defender the adjacency it needs to intervene.

---

## 4. Control 1 — within-opponent: what separates their fast kills from their slow ones

**Answer: nothing on their side. Their opening is invariant.** Same bot, same
opponent (us), four outcome classes:

| diverge's own timeline | fast kill (49) | slow kill (6) | we killed them fast (34) | we won slow (7) |
|---|---|---|---|---|
| first damage to enemy core | **r13** | r6 | r16 | r13 |
| first forward sentinel | r19 | r4 | r17 | r18 |
| barrier by own core | r4 | r4 | r4 | r4 |
| first harvester | r12 | r12 | r12 | r12 |
| builder bots by r5 | 4 | 4 | 4 | 4 |
| damage share sentinel / melee / gunner | 81 / 14 / 5 % | 87 / 6 / 7 % | 81 / 14 / 5 % | 87 / 13 / 0 % |

Pooling all 396 diverge games we hold, **first-core-damage round is identical
between their fast kills and everything else: median r16 vs r17.** Commit timing
does not discriminate because it does not vary.

**What varies is our side of the same games.** Same 49 games:

| our side | fast loss (49) | we killed them fast (34) |
|---|---|---|
| damage we delivered to their core | median **270** | median 864 |
| games where we never touched their core at all | **17 / 49 (35%)** | 0 / 34 |
| distinct sources we got onto their core | 0.69 / game | 1.56 / game |

⇒ **The within-opponent control is a null on "they do something special in the
fast games". The fast kill is their default, executed the same way every time;
the 43 games we win are games where our own clock beat theirs.** This is a
mechanism to copy, not an event to react to.

*(Observational dose contrasts across all 396 diverge games — melee ≥20 rounds
→ 51.3% kill-inside-250 vs 17.3% without — are reported here only as a caveat:
they are reverse-causal-suspect, because "got a builder parked on their core for
20 rounds" is partly an outcome of already winning. Do not read them as effects.)*

---

## 5. Control 2 — do they do it to everyone, or to us?

**To everyone.** 300 archived games vs 40+ third parties:

| plank | vs us (49 fast losses) | vs third parties (300) |
|---|---|---|
| forward sentinel in range of enemy core | 86% @ r19 | **76% @ r20** |
| launcher within d²≤8 of enemy core | 67% @ r19 | **53% @ r26** |
| builder melee on enemy core | 96% @ r26 | **86% @ r25** |
| barrier adjacent to own core, r≤8 | 88% @ r4 | **87% @ r4** |
| 4 builder bots by r5 | 4 | 4 |
| first damage to enemy core | r13 | **r17** |
| launcher throws that push the victim away from its own core | 100% | **99.9%** |

**Consequence:** this is a general-purpose opening, not a counter aimed at our
bot. It is therefore a *design* we can read off and reuse, and it is being run
against the whole ladder — which also means every team above us has already seen
it, and our copy would not be a surprise to them.

---

## 6. Stability across their 15 versions

Pooling diverge's versions is safe. Per version (n = archived games we hold):

| ver | n | fwd sentinel | med r | fwd launcher | med r | melee | med r | first dmg |
|---|---|---|---|---|---|---|---|---|
| 3 | 20 | 55% | 22 | 70% | 25 | 100% | 18 | r16 |
| 4 | 15 | 53% | 18 | 80% | 23 | 100% | 16 | r14 |
| 5 | 25 | 84% | 23 | 60% | 30 | 96% | 28 | r23 |
| 6 | 10 | 100% | 17 | 80% | 22 | 100% | 26 | r15 |
| 7 | 15 | 87% | 14 | 87% | 23 | 80% | 18 | r18 |
| 8 | 75 | 81% | 20 | 57% | 18 | 91% | 19 | r14 |
| 9 | 75 | 69% | 21 | 44% | 20 | 85% | 26 | r17 |
| 10 | 10 | 80% | 20 | 70% | 29 | 90% | 30 | r22 |
| 12 | 130 | 72% | 19 | 49% | 24 | 78% | 26 | r16 |
| 14 | 5 | 60% | 16 | 40% | 23 | 100% | 18 | r16 |
| 15 | 15 | 93% | 19 | 60% | 40 | 93% | 26 | r21 |

Eleven versions over three days, one design.

---

## 7. Control 3 — do we already do it?

**Two of the four planks: no. Not partially — not at all.**

The cleanest cut is the **same 96 head-to-head games, both sides, not conditioned
on outcome**, restricted to the versions that actually played (n=71 games on
our v102/v104):

| plank | **diverge** | **us (v102/v104)** |
|---|---|---|
| forward sentinel in range of enemy core | 72% @ med **r19** | 75% @ med **r44** |
| launcher parked on enemy core (d²≤8) | 58% @ med **r19** | **2 / 71 (3%)** |
| builder parked on enemy core, attacking | 87% @ med **r25** | **0 / 71 (0%)** |
| **any damage at all to the enemy core** | **96/96 (100%)** @ med **r14** | **54/71 (76%)** @ med **r51** |

And on our own 643 archived fast core-kill wins (all opponents), restricted to
v102/v104 (n=282):

* forward sentinel: **94%**, median **r64** (all-versions: 74%, r35)
* launcher within d²≤8 of the enemy core: **0 / 282**
* builder melee on the enemy core: **0 / 282**
* first damage to the enemy core: median **r64**

**Trap checks on the two 0-of-N results, because a zero has the shape of a
decoder gap:**

1. *Launcher.* We built **482 launchers** in those 643 games — the detector
   fires. They are simply at home: median d² to our **own** core = 8, median d²
   to the **enemy** core = 261, and only **2.1%** are nearer the enemy core than
   ours. diverge: 94.3%. **Our launcher and their launcher are different
   weapons.** Corroborated by their throw direction: **69% of our enemy-bot
   throws move the victim TOWARD its own core** (median −28 d²) — we are
   clearing intruders off our doorstep. **100% of theirs push it away** (median
   +43 d²).
2. *Builder melee.* Our v102/v104 emits **zero `builderAttack` events of any
   kind, on any target, across 282 games**. Our older versions emit **19,090**
   across 294 of 361 games. The detector works; the current line dropped the
   builder attack action entirely.

**⇒ The gap is real and it is three-part: we commit ~30–45 rounds later, we
never park a builder on the enemy core, and we never park a launcher there.**
Our damage *rate once committed* is comparable (8.91 vs 9.87 dmg/round; span
r80 vs r76) — **the whole difference is when the clock starts.**
`turns ≈ first_damage + span`: diverge 13 + 76 ≈ 91 (observed median 92); us
64 + 80 ≈ 144 (observed median 150 on v102/v104).

### 7.1 Corroborated in our own source — and it names the CAUSE of the lag

Per the standing rule *"before pre-registering any plank, grep the incumbent for
the behaviour — the cheapest possible null is a leg that tests a feature we
already shipped"*, the three planks were checked against our own trees
(`bots/_v115dodge` = frozen incumbent, single-file; `bots/_v135loki18` and
`bots/_v136loki19` = the two newest loki packages). The code agrees with the
replays, and adds the *why*.

**Launcher — the source says it outright.** `bots/_v136loki19/main.py:581-583`,
verbatim docstring: *"One Launcher, near home. ~70% of all launcher activity in
the field is defensive disposal and ours is ~97% defensive — so this is bought
as home defence first and as the raid ferry second."* Both trees ban the
launcher from the eight tiles adjacent to **our own** core
(`_v136loki19/main.py:610-613`, `_v115dodge/main.py:1992`) and both call
`_try_build_launcher` only from `_defend` (`main.py:639` / `main.py:3590`).
`grep build_launcher` finds **no site that anchors on the enemy core in either
tree.** Independent confirmation of the 0/282 measurement, from the other
direction: the placement is a design decision, not an emergent accident.

**⚠ CORRECTION TO §7's "we do not have it at all" — the parked melee raider IS
BUILT, just not in anything that has played.** `bots/_v136loki19/raid.py:131-234`
(`_raid`) drives a builder to a seat on the 12-tile ring around the enemy core,
tracks `self.raid_station`, and re-navigates when displaced (it even has
exile/throw detection at `raid.py:167-187`). `_raid_act` step 1, comment
*"STANDING ON A SEAT: peck the Core"* (`raid.py:254-271`), fires on the core
every round the cooldown allows. It is **silenced in `_v135loki18`** by
`LOKI_QUIET_ON = True` (`doctrine.py:1470`) with no override, and **re-enabled in
`_v136loki19`** by `LOKI19_CORE_PECK_ON = True` (`doctrine.py:1526`). The
incumbent `_v115dodge` has a weaker relative — `_saboteur` → `_sabotage_prio`
ranks `EntityType.CORE: 1` (`main.py:2559-2564, 2570-2573, 2767-2811`) — but no
seat-holding concept. **So the melee plank is LOKI-19's delta and it is
unmeasured; the 0/282 is a fact about v102/v104, not about what exists in the
tree.** Anyone pre-registering "park a builder on their core" would be
re-testing built code.

**Forward sentinel — our lag is an explicit ECONOMY GATE, and this is the single
most actionable line in the document.** `_try_forward_sentinel`
(`_v136loki19/raid.py:392-454`) refuses to build until **all** of:

* `ct.read_store(SLOT_HARVESTERS) >= LOKI_FWD_MIN_HARV` — **2 harvesters**
  (`raid.py:415`, `doctrine.py:1247`)
* `ct.get_global_resources() >= cost + LOKI_FWD_TI_FLOOR` — **40 Ti banked on
  top of the sentinel** (`raid.py:418`, `doctrine.py:1246`)
* fewer than `LOKI_FWD_GUN_CAP = 3` forward guns live (`raid.py:410`)
* a real firing line, via `ct.can_fire_from(bp, facing, EntityType.SENTINEL,
  target)` (`raid.py:439`)

The round-based bypass exists and is **switched off**: `LOKI2_RUSH_ON = False`
(`doctrine.py:1391`), which would otherwise relax the gate to 0 harvesters /
8 Ti inside round 60. `_v115dodge` gates the same way (`_plan_siege`,
`main.py:2616-2638`, `ECO_NEED = 3` harvesters once one gun exists).

**diverge has no such gate.** Their first damage lands at r13 and their first
harvester at r12 — the attack *precedes* the economy. Ours waits for 2
harvesters plus a 40 Ti buffer, and lands at median r44–r64. **The 25–45 round
lag measured on the wire is not a pathing or a CPU limitation; it is a
threshold in `doctrine.py`, and `LOKI2_RUSH_ON` is the switch that was built to
remove it.** Whether removing it is *good* is exactly what a live leg would
have to answer — this document does not claim it is.

**One plank we cannot copy without breaking programme, stated so it is not
mistaken for a recommendation:** their r4 barrier orthogonally adjacent to their
*own* core footprint (361/361 early barriers, 100% adjacent, present in 87% of
all their games) is a home-tile denial — it is the mirror of the melee plank,
pre-empting an enemy builder from parking where their own melee builder parks on
us. It is **defensive**, `PLAY_DEFENCE: never` applies, and it is recorded here
only because it is part of the observed opening.

---

## 8. Plain statement of the mechanism

> **Four builder bots by r3. One sentinel built inside `SENTINEL_ATTACK_RADIUS_SQ`
> of the enemy core (d² ≤ 32), placed by a walking builder, landing ~r19. One
> launcher parked within d² ≤ 8 of the enemy core, ~r19, whose only job is to
> throw away every enemy builder that comes adjacent — 100% of throws push the
> victim ~5 tiles off its own core. One builder parked orthogonally adjacent to
> the core footprint attacking it every single round from ~r25 for a median of 41
> rounds. Home economy is built in PARALLEL, never as a gate: first conveyor r4,
> first harvester r12, ~3 harvesters total. First core damage lands at median
> r13. The emplacement then grinds ~10 HP/round through ~272 HP of the
> defender's healing and kills a 500 HP core in ~76 more rounds.**

Three properties worth naming:

1. **The economy is never a gate.** They start the attack before their first
   harvester exists (first damage r13, first harvester r12) and build the belt
   anyway. Under `R1000_IS_DEFEAT` this is exactly the "economy is instrumental"
   posture, executed.
2. **It is cheap.** ~1 sentinel + ~1 launcher + 2 Ti/round of melee + 5 Ti/round
   of sentinel ammo. No army, no second wave, ~4 builder bots all game.
3. **The launcher is the enabler, not the damage.** It deals none of the 41,870
   HP. It buys the ~50 uninterrupted rounds the other two planks need.

**What we already have:** the forward sentinel — but ~25–45 rounds late, and
§7.1 shows the lag is an explicit 2-harvester / 40-Ti gate in `doctrine.py`
with a built, switched-off bypass (`LOKI2_RUSH_ON = False`).
**What we have built but never measured:** the parked melee raider —
`_v136loki19/raid.py` holds a seat on the enemy ring and pecks the core; it is
0/282 on the versions that played, not 0 in the tree.
**What we do not have at all, in code or on the wire:** the forward launcher.
Our own source calls the launcher *"home defence first"* and bans it from the
tiles next to our own core; 0/282 games and 0 build sites anchored on the enemy
core. **This is the only one of the four planks that is genuinely absent.**

---

## 9. LIMITS — the biggest threats to this finding

1. **⚠ THE BIGGEST ONE: everything here is observational and nothing has been
   tested live.** Per the standing rule (`REFUTATION WITHOUT LIVE-GAME BACKING`),
   this document may **prioritise** a road; it may not open or close one. In
   particular *"the launcher buys the grind"* is a **narrative fit to
   co-occurrence**, not a measured effect. The only honest test is a live leg
   where the dose is delivered by us and the falsifier is named in advance.
2. **n=20 matches, not 100 games.** Five games share a pairing, a map set and
   both versions. Any interval computed on n=100 is overconfident. The
   third-party population (300 games) is likewise ~60 matches.
3. **Selection on the outcome.** `DV_FASTLOSS` is *defined* as games they won
   fast, so "they had a builder on our core for 41 rounds" is partly a
   consequence of winning, not only a cause. Section 4's unconditioned
   both-sides cut on all 96 games is the guard; the dose contrasts in §4 are
   explicitly NOT guarded and are labelled as such.
4. **Population C (our 643 fast wins) is 70.7% archived and pools opponents.**
   It answers "do we do this" but not "would it work" — those are different
   questions and only the first is answered here.
5. **The third-party population mixes ladder and unrated**, per the standing
   corpus-surface rule. It is used ONLY for Control 2 (does diverge run the
   same opening) and never for a rate about our record.
6. **Their side is pinned; the pin is coarse.** `ladder_games.oppver` is NULL
   for all 100 games; versions came from `league_matches.tsv` at match
   granularity. Section 6 shows stability across 11 versions, which mitigates
   but does not remove the risk that a specific version differs.
7. **0.20% of core-damage round-cells are under-attributed** (a `fireTurret`
   whose source tile could not be resolved). Immaterial at these effect sizes,
   but it is not zero.
8. **`print()`-derived evidence was never used**, per the s28 correction —
   every fact here is an engine-side event (position, entity, HP delta).
9. **Us-only sample.** The 49 fast losses are our own tape. Population B widens
   the opponent set for diverge's behaviour but not for the outcome rates.
10. **The replay populations and the source read are about DIFFERENT bots.**
    §7's 0/282 measures platform versions v102/v104. §7.1 reads
    `_v115dodge` / `_v135loki18` / `_v136loki19`. The mapping from platform
    version number to tree was **not** verified in this commission, so
    "our code does X" and "our games show Y" are two claims joined by an
    assumption. The one place it demonstrably matters is the melee raider,
    which is 0 on the wire and present in `_v136loki19` — flagged inline.

---

## 10. What this does NOT say

* It does not propose a plank, a prereg, a build order, or a ship decision.
* It does not claim diverge's opening would work for us — our chassis, our
  pathing and our CPU budget are not theirs.
* It does not recommend any defensive change. The two defensive observations
  (their r4 home barrier; our home launcher clearing intruders) are recorded as
  description and are off-programme as planks.
* It does not price the road. `tools/target_value.py` has not been run, and
  under the s28 rule that gate belongs to whoever writes the pre-registration —
  **diverge sits near our own rating, so the band question is live and unanswered
  here.**
