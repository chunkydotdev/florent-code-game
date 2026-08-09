# Offensive-mechanic catalog: the full A/B/C, ban-evidence ranked — and the theory I tested instead of asserting

**Side lane, 2026-08-09 15:20 CEST. The third playbook piece (with
early-kill-arsenal + mechanic-bans + dirty-tricks-shortlist). Companion
doc-mine (opus, whole tactics library + s24 deliverables + HANDOVER +
ban docs) persisted here because the agent transcript dies with the session.
Magnus's principle drove the last hour — "if we don't test our theories we
never discover anything" — and it just paid: I re-tested a mechanic I had
asserted dead and found it real (§B2).**

## The one I tested this turn — kidnap-into-arc is NOT displacement-only

Earlier I dismissed launcher kidnap as "displacement only, 0 core attacks."
That used the wrong metric (core attacks, not turret kills). **Tested the
right question in the corpus:** of 61,109 enemy-bot throws, **159 put the
kidnapped builder on a tile where the THROWER's own turret killed it within 4
rounds** (0.26% base rate; **OpenSverige 0.54%**, 60 of 11,106 — we already do
it twice the field rate, by accident). Sentinel kills dominate the examples
(thrown → 1-2 sentinel shots → dead, 2-4 rounds later). **Revised verdict:
the offensive-kill form of kidnap is real and observable, just not deliberate
— the same "happens by accident, could be done on purpose" shape as the
sentinel rush.** Correlational (the throw co-occurs with the death; I have not
shown the throw *caused* the arc placement) — the builder's S2 probe is what
establishes causation. But "0 offensive value" was wrong, and I only know that
because I tested it.

## (A) LIVE + EARLY, positive evidence — ban-evidence rows first

| # | mechanic | why it survives (ban/measure) | opponent aim |
| --- | --- | --- | --- |
| **A1** | **Early sentinel/gunner core plant** (Banminary: 3 turrets, d²≈18, r17) | organisers nerfed every adjacent line, **never the turret push to the core**; Screeps/Terminal ban forward-planting by rule, we have **no territorial restriction at all** | Ouroboros (static v8); NOT CAD (survive-to-r1000) |
| **A2** | **Launcher kidnap, offensive forms** | **"ZERO balance changes ever"** — only entity never touched | Ouroboros/Powerpuff/Leviathan/Orizon build no launchers; KCM & CAD never throw (0/170) |
| **A3** | **Spawn-ring collar, BODY form** (Loki-3) | BC2023 patched spawn-camp (→ worked); BC2024 used it legally (→ came back) | any; forward so <r150 |
| **A4** | **Off-axis approach vs never-rotating gunners** — NEW, cheap (~20 lines) | flanking a directional defence won a BC2021 award; sentinel facing is **permanent for everyone** | **Memtrace, OopsGotYourElo, Team 48, The Bisons, gsxWins, Focalground: 0.0 rotations, every version** |
| **A5** | **Reactive ore denial** (barrier an adjacent ore tile) | BC2019→field-wide BC2020, never nerfed; ~87:1 with a harvester kill | universal (hive: 12 ore tiles) |
| **A6** | **Lunds r3 insertion-tile fixture** — earliest exploit on the board | "not one cell varies across versions"; 19 (map,seat) cells | **Lunds only** (also the most meta-manipulable team) |
| **A7** | **Tiebreak key-1 pressure** (deliver early, spend freely) | never patched; spending provably can't cost key 1 (6,453/6,454) | CAD (16-4 at tiebreak) — Eir's job |
| **A8** | **Pipeline heal-uptime** (drain-refutation survivor) | +7pp win p=0.045 via +1.69 Ti/rd to OUR economy | universal, not an exploit |
| **A9** | **Sentinel file at N=2-3** | reload-2 nerf preserved, stacking untouched; probe-legal (fires through friendlies) | universal; broad field doesn't scale its guard |

## (B) PLAUSIBLE, UNMEASURED — probe before build (Magnus's "test it" list)

These are the theories worth *testing* precisely because they're cheap and
free-tool-eligible, not asserting down:
1. **Kidnap-into-arc, deliberate** — S2 probe (does a thrown enemy eat our fire
   same-round?). Corpus says the incidental form is real (§B2 above).
2. **Imprisonment via prebuilt cell** — one boolean: `can_launch(enemy_pos,
   fully_enclosed_tile)`. NOT touched by the barrier-on-standing-bot refutation.
3. **Crash induction** — highest ceiling; BC2009 precedent won an award; needs
   a probe + delivery vector. (My separate join: field no-damage deaths are NOT
   throw-correlated, so it's not currently weaponised — the probe tests whether
   WE can induce it, which the corpus can't answer.)
4. **Degraded-branch induction** — aim past their iteration cap, not their
   clock; two BC winners' postmortems document it; not the banned act.
5. **Resource theft onto their conveyor / our core** — inference only, cheap to
   read the engine; would STEAL not deny.
6. **`can_fire_from` as an out-of-vision sensor** — BC2024 HS winner freed 2/3
   guards with the analogue; one local probe.
7. **Passive damage in the core action radius?** — gates A3's barrier variant;
   the BC2023 anti-spawn-camp patch may or may not be in our engine.
8. **`can_launch` shape** (4- vs 8-way adjacency, reachable vs passable target,
   does a throw consume the thrown bot's cooldown) — gates the whole displace
   family.
9. **Does `self_destruct()` drop `get_builder_bot_cost()`?** — one match.

## (C) MEASURED DEAD — do not rebuild (the arena-time protector)

**Killed on our own field data:** drain-pump / ammo-bait (CI [−1.04,+0.65] on
9.56 base; shots-into-empty score −0.257, the *worst* outcome; died pre-build,
no early carve-out) · forward insertion AS LATE DOCTRINE (4 instruments) ·
SITE forward-siting −6.7pp dose-response · ESCALATE more-defence −7.8pp
(foreign pool, both seats) · HOME −2.0 / FLOOR −0.7 / LOKI-3-anchor +0.0
(self-play nulls — "the next attempt must not be another turret knob") ·
pre-emptive ore denial (dies on a pincer) · interceptor-saturation bait (min
gap 1 for everyone) · per-map killer-tile table (−3.9pp OOS at k=8) · launcher
deletion (+2/240) · thor_r1 / Thor-1-gunline / sporks rushes (home-band turret
pushes, 2/60, zero cores) · "force them to heal" (inverts 2.2:1) ·
barrier-on-standing-bot & 12-barrier lock (probe-refuted; body form survives) ·
bank-as-a-stage · the multistep-plan family (§2) · builder-body-forward
(3% of kill damage).

**Dead by rule (organiser-patched pre-inheritance):** suicide-builder rush
(self_destruct 0 dmg) · cheap-builder swarm (30Ti+20%+50cap; 20th builder
958 Ti) · infinite-heal blob (1Ti/4HP) · two-sentinel one-shot (2×18<40).

**Dead by our ruleset's shape (`transfers: no`):** comms jamming (store is
team-private) · `Creep.pull` (needs consent) · ramming (no collision) ·
drop-into-hazard (no hazard terrain) · cross-match opening book (no
persistence) · the ticket/auction/buffer-pool store idioms (buffered
last-writer-wins) · turret spacing floor (no splash exists anywhere).

**Held on NORMS, not evidence:** deliberate CPU-timeout induction — real and
tournament-deciding, but **banned by name in BASIL / SC2 AI Arena / SSCAIT**;
our league silent. HOLD pending an organiser ruling (Magnus owes one question);
the defensive + incidental halves are free.

## Five things that will bite the builder (carry these)

1. **Pool labels bind every number** — LOKI-3/HOME/FLOOR/SITE are self-play
   (~2× inflation, sign flips); only ESCALATE ran foreign.
2. **No local punisher exists** — every aggression flag on our lineage is
   *unmeasured, not refuted*; this is why the unrated fixture matters.
3. **Friendly fire is real, lanes are shared** — turret hits whatever's on the
   TARGET tile; heal dispatch and payload targeting need a shared
   do-not-target set. (Also what makes A2/B kidnap-into-arc a weapon.)
4. **`get_attackable_tiles()` lies** — ignores occupancy; gunner lines ARE
   blocked by our own material, sentinel lines are not. Lane-check with
   `can_fire_from`.
5. **Any raise escaping `run()` permanently kills the unit** — live raise-sites:
   `get_nearby_tiles(>vision)`, `write_store(negative)`, `rotate()` to current
   facing. Our try/except holds (0/8,664 no-damage deaths); every new offensive
   verb is a new chance to break it.

## Provenance

Doc-mine: opus agent, read-only, whole `docs/research/tactics/` + s24
deliverables + HANDOVER + the two ban docs; every row carries its source
doc + refutation status. Kidnap-into-arc test (§B2): `throws.tsv` (kidnap =
tteam≠bteam) × `dc_deaths` (victim died to enemy turret within K=4), this
lane, 2026-08-09 15:1x. A4/A6 opponent facts from opponent-reaction-atlas +
lunds-insertion-tiles. The C-list consolidates every refutation on the tape;
each is traceable to its named deliverable.
