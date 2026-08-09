# Multi-step plans: what tactic composition survives contact with the data

**Side research lane (Magnus-commissioned, third session), 2026-08-09.**
**Version tag:** live **v90 "Heimdall 1 (launcher relight)"** (`bots/_v104latch`,
tree `2c6dbc17`), ~1586-1589 @ ~501, rank #28-29. Corpus at commit `a1bd423`
plus keeper-decoded growth (attribution join enlarged to 2,735 archived replays
/ 5,470 team-sides — see method note §1). **Zero replay downloads, zero
platform actions, zero bot edits.**

Inputs: three subagent reports (in this session's scratchpad, relayed here in
full because subagent output dies with the session):
1. **Corpus phase-mining** (opus) — per-round decoder over 2,735 attributed
   replays; validation: predicted core damage (7·gunner + 18·sentinel +
   2·builder shots) vs the dying core's HP stream closes at **median ratio 1.00
   in all four populations**.
2. **External composition sweep** (opus) — all 22 Battlecode postmortems
   2019-2026 full-text, Screeps forum/wiki/Overmind, Terminal, Lux AI,
   academic RTS. Every claim source-graded.
3. **Parts inventory** (sonnet) — every tactic on file as
   precondition→postcondition cards (scratchpad `parts-inventory.md`).

The commissioning question (Magnus): the builder tests 1-2 step tactics —
**do bigger plans exist where a bad tactic becomes a good one as a step?**

---

## 0. TL;DR

1. **The field does NOT run phased plans.** Strict 4-stage ordering
   (econ → ammo bank → forward ratchet → kill wave) holds in **9% of top-tier
   kills** (n=444). What wins is a **permanent siege posture** (deep building
   flat from 300 rounds before the kill), a **~25-round commit burst** that
   re-points existing throughput (total build rate does NOT rise), then a
   **~65-round grind at ~8 net HP/round**.
2. **Nothing outruns the heal cap — concentration-in-time is refuted.**
   Pooled over 640k fire-rounds: healing cancels ~70% of core damage at every
   intensity; net never exceeds ~3.3 HP/round even at 5+ simultaneous
   shooters. **The discriminator is DURATION, not intensity**: top-tier kills
   sustain 59 fire-rounds at 5.0 net vs failed sieges' 28 at 1.6 — same gross
   damage per fire-round (12.9 vs 11.4); what differs is defender healing let
   through (1.4 vs 2.6) and how long the fire survives.
3. **Our specific failure is persistence, not opening.** We open the sharpest
   commit burst of any population (first fire r18 vs TOP's r25, higher damage
   per fire-round), then: our forward gunner lives **25 rounds vs TOP's 50**;
   when it dies **we never replace it 49% of the time** (field 28-36%); and in
   r1000 stalemates our last shot lands **r163 vs the field's r647-719 — we
   idle 837 rounds** while MID-tier teams fire to r966. 65% of our stalled
   sieges end because the shooter died (field: as often ammo-bound).
4. **So the answer to the commissioned question is yes, but the shape is not
   a sequence — it is concurrent maintenance loops** plus, for exactly our
   rating band, one proven insertion opener. Three composites survive grading
   (§4); five popular composition ideas are refuted with data (§5).
5. **Sharpest single number found: bodies are bad bait, buildings are good
   bait.** A barrier costs 3 Ti and ~17 Ti of enemy ammo to remove (**5.6:1**
   for us); a builder costs 30 Ti and ~22 Ti to kill (**0.74:1 — a losing
   trade**). Our 11,895 corpus forward throws were spending 30 Ti bodies at
   negative exchange; that is why no drain ever accumulated.

---

## 1. Method notes a successor needs

- **Attribution enlarged 2.2x** (corpus agent): archived replay filenames are
  `<matchId>_game_N.replay26` and `corpus/league_matches.tsv` carries both
  team names + pre-match ratings for all 27,073 league matches. A
  filename-prefix join attributes 2,735 of 4,231 archived replays (5,470
  sides, 945 top-tier). Reconciliation vs `join.tsv` on the 1,180 shared
  files: **1,180/1,180 agree.** This join is reusable and should probably be
  productised into `corpus/` (builder/research call, not mine).
- Populations: TOP ≥1750 (444 kills), STRONG 1550-1750 (513), MID <1550
  (504), US (388 kills / 1,180 sides). Named coverage 45-125 sides/team.
- **Limit:** `destroy()` of an own building is indistinguishable from an
  enemy kill in `removeEntity` — "destroys own buildings as setup" is a
  **gap, not a null**. Insert-throw rates are lower bounds (corpus trap 3).

## 2. The corpus verdict on phases (Q1-Q4 of the brief)

| hypothesis | verdict | evidence |
|---|---|---|
| 3+-stage ordered plan | **refuted** | strict ordering 9% TOP / 6% STRONG / 3% MID / 1% US |
| ammo-banking stage | **refuted** | conversion flat through run-up, **doubles only AFTER guns fire** — demand-driven |
| forward ratchet stage | **refuted** | deep builds (d²ₑ≤32) flat T−300→T; the outward drift in `late-game-doctrine` is OUR signal, the field's line was always there |
| economy→military handover | **refuted** | build rate flat across commit; harvesters built into the last 25 rounds |
| sacrifice/feeding prep | **null** | winner-side loss curves monotone, peak AFTER first contact; nothing spent up front |
| builder kill-wave | **refuted, inverted** | spawns FALL into the kill window everywhere except US (we alone wave: 0.28→0.97) |
| damage spike at kill | **refuted** | last 5 rounds = 7.3% of damage; median 65 rounds from 90% HP to dead; peak simultaneous attackers median 2 |
| ONE staged element exists | **confirmed, STRONG band only** | own-builder INSERT throws spike **3.5x** in the commit window (0.13→0.46→0.13/25r) — throw in → build gunner → fire. TOP walks instead (0.07) |

**What kills cores:** turrets. Gunner 57.6% / sentinel 39.4% / builder melee
**3.0%** of top-tier kill damage (median builder attacks on a dying core: 0 in
every population). Killing turrets are **built in position at point-blank**
(TOP gunners at median d²=8 from the core, first core shot within 1 round of
being built, then 65 rounds of grind). We invert the mix: 25.9% gunner /
65.1% sentinel, built at the max-range shell (d²=32). **The scarce act in
this game is getting a builder adjacent to a tile within r²≤13 of the enemy
core with 20 Ti and a free action — everything else is maintenance.**

## 3. The siege anatomy — three measured failure modes, all ours

Confound-free cut (same 1,180 games, both sides): opponents ≥1600 field
**3.0 core-shooters / 59 fire-rounds / 46% kill**; we field **1.0 / 28 / 33%**.
Per bleed source it is brutal (Lunds 133 fire-rounds vs our 5 in the same
games). Memtrace inverts (we out-fire 28:9.5) — the deficit is specific to
siege teams, not general weakness.

1. **Shooter survival:** our forward gunner lives 25 rounds vs TOP's 50, dies
   before game end 62% vs 41%. The field suppresses defender healing to 1.4
   HP/fire-round vs the 2.6 we let through — consistent with point-blank
   gunners (cheap 4-ammo shots) clearing the healer screen, the 96-Ti clear
   from `exchange-rates` §3, while our max-range sentinels cannot hit healers
   hiding behind the core.
2. **Replacement:** when our shooter dies we never replace it **49%** of the
   time (field 28-36%). Conditional replace latency (22 rounds) is normal —
   **we stop deciding to, we don't fail to.** This is a state-machine defect,
   not a capability gap.
3. **Walking away:** 60% of our stalled sieges idle ≥200 rounds; last landed
   shot r163 vs MID's r966 in r1000 games. MID-tier teams — weaker than us —
   simply keep firing and reach 152 fire-rounds.

External corroboration (sweep §5.1, BC2026 winner): commits dissolve when
units re-evaluate every turn — *"the report state does not get distracted."*
Our raiders/siege have no non-preemptable committed state.

## 4. The composites that survive grading

### P-A. PERSISTENT SIEGE (field-proven; the data says build this first)
Not a sequence — three **concurrent maintenance loops** over a whole-game
posture:
- **Shooter loop:** builder gets adjacent to r²≤13 of enemy core, builds
  gunner, gunner fires from round 1 of its life; on shooter death → replace
  (the field's 65-round grind is a replacement chain, median shooter life 46).
- **Screen-suppression loop:** point-blank gunners shoot the healer screen
  (only turrets can hit builders); target = let-through healing ≤1.4/fire-round.
- **Supply loop:** demand-driven `convert_ammo` (no banking stage — convert
  as the guns burn; we currently buy 1/12th of Ouroboros's ammo while holding
  MORE titanium).
Steps that measured bad alone become good here: LOKI-3's forward guns died
"outside every heal path we own" — the loops ARE the missing partner
(replacement + our measured-best healing pointed at our own shooter).
**Smallest tests, separable flags:** (a) non-preemptable `COMMITTED` siege
state; (b) replace-on-death rule (attacks failure mode 2 alone — the single
cheapest plank in this document); (c) no-idle rule (a stalled siege re-fires
instead of walking away). Pre-register on: fire-rounds/game (28→toward 59)
and idle-after-last-fire (340→toward 30).

### P-B. DRAIN → SIEGE (novel; arithmetic-backed; nobody in the field runs it)
Stage 1: **barrier sponge** — one builder inside enemy turret range builds a
barrier on the enemy-most adjacent tile every turn; heal-sustain the builder
(tank + 2 healers hold **one** sentinel line indefinitely at titanium profit;
2+ turrets on the tile beats the 16 HP/round heal cap and the bait dies — so
**tile selection is the whole tactic**: `singly_covered_tiles()` from
`get_attackable_tiles_from()` over visible turrets).
Stage 2: siege (P-A) through the exhaustion window — the field's own stalled
sieges are **ammo-bound 37-41%** of the time, so ammo exhaustion is a real,
measured failure state to push opponents into. Their ammo regenerates at
exactly 0; the true bar is their total Ti income (~27.5/round at 10
harvesters), so drain composes with ore-tile denial (early-only part).
Both branches of the bait pay: unshot barriers = a free forward wall that
blocks THEIR gunner lanes while OUR sentinels shoot through it (engine-probe
verified). Documented precedents: BC2019 crusader-flood fuel drain, Screeps
tower-draining, BC2021 Wololo drain-rate math (sweep §2).
**Go/no-go gates, in order:** (1) corpus query — do opponent turrets fire on
buildings at all, per opponent (if unit-only targeting, the family dies
except as lane-blocking); (2) does a coverage-1 fringe exist near top-5
enemy bases; (3) the sponge instrument: **Ti of enemy ammo burned per Ti we
spent — under ~1.5, road closed.**

### P-C. INSERT COMMIT (STRONG-band-proven; this is Loki's vindication)
The one staged element the corpus found: the 1550-1750 band — **exactly the
opponents we bleed to** — spikes own-builder insert throws 3.5x in the commit
window: throw builder in → build gunner point-blank → gunner fires. TOP
walks instead; both feed the same siege. Composes with: early timing
(<r150, per the established survival cliff), the `COMMITTED` state (P-A),
and a healer pair as the survival package. This reframes the builder's
"early insertion + survival package" queue item: **insertion is the opener
of a siege, not a raid** — the payload is a 20 Ti gunner adjacent to the
core, not builder melee (3% of how anyone kills).

### P-D. Reaction-triggered baits (opponent-conditional; atlas-gated)
Against coded opponents a bait triggers a measured rule or nothing. Family:
interceptor saturation (feed their launcher junk so the real insert walks
past — their throw-on-adjacency is measured, ~22 exiles/game vs Ouroboros,
bait returns in median 6 rounds to re-trigger); rotate-thrash (10 Ti + a
blind round per forced gunner rotation, approach the unfaced arc);
panic-build inflation (+20% scale per baited turret — distinct from the
REFUTED "force them to heal", which drains US 2.2:1); fortified honeypot
(exposed harvester covered by launcher interception in our +11-22pp home
band). **Shared gate: one per-opponent reaction atlas from the corpus** —
(a) turrets fire on buildings? (b) build-on-sight + latency, (c)
rotate-on-sight, (d) healer relocation latency, (e) launcher
throw-on-adjacency rate + cooldown. Elo is game-share; 5-of-19 coverage pays.

## 5. Refuted / gated compositions — do not rebuild these

1. **Bank-then-spike (concentration in time):** the heal-race table caps net
   at ~3.3 HP/round at ANY intensity; the field converts ammo on demand.
   Banking titanium is fine (it compresses the commit — no production queue),
   banking AMMO as a stage is not a thing anyone needs.
2. **Grand committed all-in:** no documented abort-of-an-all-in anywhere in
   the sweep; the field sizes commits to be survivable. Favor repeatable
   pulses (a replacement chain IS a repeatable pulse).
3. **Forcing sequences ("threat A so B lands"):** no documented case in any
   competition read, and the corpus shows no second-front structure. A second
   prong's real, documented value is vision/information, not forcing.
4. **Sacrifice-prep (feed units to set up):** corpus null — winner losses
   peak AFTER contact. The scale-deflation variant (self-destruct rear
   builders to cheapen a spawn wave, sweep §4.1) stays alive ONLY as a
   1-match engine probe: does `get_builder_bot_cost()` drop after
   `self_destruct()`? (CLAUDE.md says scale decrements on destroy;
   CLAUDE.md is known-unreliable.)
5. **Builder-body anything forward:** 0.74:1 exchange as bait, 3% of kill
   damage as a weapon. Builders forward are couriers and constructors, never
   payloads.

## 6. Machinery findings for the builder (independent of any plan)

- **Store single-writer audit:** with buffered last-write-wins, any slot
  with multiple writers is a race. Live correctness risk today, and P-A/P-C
  add a plan slot. (Sweep §5.3; Overmind directive pattern = commitment as
  an object with its own removal condition, one writer, stateless readers.)
- **Core-hallucinated rally** (BC2023 No Thoughts): the core writes a fake
  enemy sighting; every unit's existing react-logic executes the commit with
  zero new per-unit code; abort = clear the slot. Cheapest known way to
  synchronize a commit under per-unit execution.
- **`self` persists across units and rounds** — a second memory channel
  beyond the 16 ints (probe: increment a counter in `run()`).
- Cross-reference: gunner lanes are blocked by own bots/buildings and
  `get_attackable_tiles()` lies about it (already in builder queue §2) —
  P-A's point-blank gunners make this bug load-bearing.

## 7. Ranked next actions

1. **Replace-on-death + no-idle flags** (P-A b/c) — attacks the largest
   measured gap (49% never-replace; 837 idle rounds) with the least code.
2. **Corpus query: turret targeting of buildings, per opponent** — gates all
   of P-B and half of P-D. One read, zero downloads.
3. **Engine probes** (1 match each): scale decrement on destroy;
   `can_launch` into an enclosed cell (imprisonment gate, from inventory).
4. **`COMMITTED` state + insert-opener refit of the Loki pipeline** (P-C).
5. **Reaction atlas** (P-D) — one corpus read pricing five tactics.
6. Productise the enlarged filename-prefix attribution join into `corpus/`.
