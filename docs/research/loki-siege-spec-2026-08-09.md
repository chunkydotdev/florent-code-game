# LOKI-SIEGE: a buildable refit spec, to the flag level

**Side research lane (Magnus-commissioned), 2026-08-09. PROPOSAL — the builder
owns the verdicts, the queue, and every line of code; this document is a spec
with pre-registered instruments, per the research remit.**
**Version tag:** live v90 (`bots/_v104latch`, tree `2c6dbc17`). Evidence base:
`docs/research/multistep-plans-2026-08-09.md` (this lane's corpus/external/parts
synthesis — read it first; nothing here stands without it).

## 0. What this is

Loki's mandate is the r200-300 conversion ratio vs strong opponents (0.52,
declining). The corpus read located our deficit with unusual precision, and it
is NOT the opening: **we start sieges earlier and harder than the top tier and
then fail to sustain them.** Same-games cut: opponents ≥1600 field 3.0
core-shooters / 59 fire-rounds / 46% kill; we field 1.0 / 28 / 33%. Three
measured failure modes: shooter life 25r vs TOP 50r; never-replaced after death
49% vs 28-36%; idle-after-last-fire 340r vs TOP 23r.

This spec = five separable flags that convert the existing Loki machinery from
"raid" to "persistent siege". No new doctrine road: the insertion pipeline,
the healing engine, and the turret code all exist; the flags re-point them.

## 1. Architecture constraints (inherited, non-negotiable)

- Fork `_v103split` chassis (or the current descendant the builder prefers);
  new logic in ONE module (`raid.py`/`siege.py`) so it ablates as a unit.
  Economy bit-for-bit (thor_r1 is why). Byte-identical with master flag OFF.
- Every siege unit's run() wrapped: blanket try/except (uncaught = permanent
  unit death) + CPU guard (10ms; the chassis turret scan already guards).
- **The store is FULL (16/16, slot 6 = heartbeat).** ~~Probe `self`
  persistence~~ — **ANSWERED by the research arm (2026-08-09,
  `store-semantics-2026-08-09.md`): `self` does NOT persist across units;
  each unit gets its own `Player` instance** (their sentinel probe silently
  no-oped on exactly this). So: shared siege state MUST go through the store
  — pack into a reclaimed slot (2 bytes target xy, 4 bits state, writer =
  core only). Store semantics per the same doc: buffered to next round,
  last-writer-wins, **unsigned 32-bit [0, 2^32−1]; writing a negative raises
  OverflowError, which permanently destroys the unit** — clamp before every
  write. Per-unit persistent state (e.g. COMMITTED flags) is fine in `self`
  keyed implicitly by the unit's own instance. **Single-writer rule for every
  shared slot** — multi-writer under last-write-wins is a race (live risk
  today).

## 2. The five flags

### S1 — COMMITTED state (non-preemptable siege FSM)
Siege units get exactly two states. APPROACH: preemptable, normal priorities
apply. COMMITTED: entered on reaching staging (adjacent to a tile within
r²≤13 of the enemy core, or on insert landing); may ONLY move-toward-target,
build the payload turret, attack the screen, or heal the shooter — never
re-evaluate economy/defence tasks. Evidence: BC2026 winner's FSM ("the report
state does not get distracted"); our raiders provably drift (idle 837r).
Exit conditions are dumb thresholds, never plan-quality estimates (sweep
§5.5): unit HP < 12, or round > commit_round + W, or core order cleared.

### S2 — REPLACE-ON-DEATH (the cheapest plank on the board)
Rule: while an enemy core is known and round < 950, a dead forward shooter
creates a build order for the nearest COMMITTED builder: rebuild the gunner
on/near the same tile. Target metric moves 49% never-replaced → field's
28-36%. Our conditional replace latency (22r) is already normal — this flag
adds a decision, not a capability. The field's 65-round grind IS a
replacement chain (median shooter life 46r); we currently run chain length 1.

### S3 — NO-IDLE (a stalled siege re-fires or rebuilds, never walks away)
If no shot has landed on the enemy core for W2 rounds AND we have ≥1 living
forward shooter or ≥1 COMMITTED builder in range: force re-fire/rebuild.
Baseline: 60% of our stalled sieges idle ≥200r; last shot r163 vs MID's r966
in r1000 games. MID-tier teams — weaker than us — out-persist us on this one
behavior. Guard: respects the hazard-table warning by NOT extending games
passively — the flag fires guns, it does not wait.

### S4 — SCREEN SUPPRESSION (gunner target priority)
Payload turret is a GUNNER built point-blank (target tile within r²≤13 of the
core, field median d²=8), NOT a max-range sentinel (our current d²=32 habit).
Two reasons, both measured: gunner = 57.6% of top-tier kill damage vs our
25.9%; and only turrets can hit builders — the point-blank gunner shoots the
healer screen first (priority: enemy builder adjacent to their core > core
tile), which is the 96-Ti clear vs the 780-2,500-Ti grind-through. TOP lets
through 1.4 HP heal per fire-round; we let through 2.6 — this flag is the
mechanism aimed at that number. NOTE the known engine trap: gunner lines are
blocked by own bots/buildings and `get_attackable_tiles()` lies about it —
siting must lane-check with `can_fire_from`, not the pattern getter.
**Sentinel-payload alternative (research-arm probe, same day): sentinel lines
pass through our own bots AND buildings (verified with a landed 18-dmg shot),
so a sentinel payload sidesteps the lane bug entirely.** Costing: gunner
clears a 40 HP healer for 24 ammo vs sentinel's 30, and gunner is 57.6% of
top-tier kill damage — but a mis-sited gunner fires zero shots. Recommend:
gunner where a `can_fire_from`-verified clear lane exists at build time,
sentinel otherwise; instrument M6 tracks the realized mix.
**Shell-matched survival (this lane's cut, answering the research arm's
siting question): the persistence gap is NOT a siting-mix artifact within
core-shooters — at the SAME point-blank shell (d²≤13) TOP shooters live 47r
vs ours 25r, and our death rate is 62-63% in EVERY shell vs TOP's 37-42%.
Siting explains where home turrets survive (research arm's result); it does
not explain away the forward support/replacement deficit. Both planks stand.**

### S5 — DEMAND AMMO (no banking stage)
Maintain ammo ≥ (next 2 rounds of planned shots) via same-turn convert_ammo;
convert MORE only while guns are actually firing. Field conversion doubles
only AFTER first core contact — demand-driven is the measured winning
pattern. We hold more Ti than every opponent at r200-300 while buying 1/12th
of Ouroboros's ammo; the titanium is already there.

### Optional opener — S6 INSERT (only after S1-S5 measure)
The STRONG band (our bleed sources) proves insert→gunner→fire, spiking 3.5x
in commit windows; TOP walks instead. So insertion is an ACCELERANT of a
working siege, not a fix for a broken one: sequence S1-S5 first (walking
reaches the same siege), then S6 re-points the existing `_launcher` insertion
(<r150 only, per the survival cliff; generic drop-site derivation per the
Lunds warning) with the landing builder entering COMMITTED directly.
Payload = gunner, never builder melee (3% of anyone's kill damage).

## 3. Pre-registered instruments (mechanism first, field second)

Per the LOKI-3 lesson (mechanism moved 16x, field +0.0pp): mechanism metrics
protect attribution, the class-weighted field battery decides shipping
(ship-gate rules unchanged, builder's call throughout).

| # | metric | baseline | direction | flag |
|---|---|---|---|---|
| M1 | fire-rounds/game (sieges) | 28 | → 45+ | S2+S3 |
| M2 | never-replaced after shooter death | 49% | → ≤35% | S2 |
| M3 | idle-after-last-fire (stalled sieges) | 340r | → ≤60r | S3 |
| M4 | let-through healing / fire-round | 2.6 | → ≤2.0 | S4 |
| M5 | median forward-shooter life | 25r | → 40r+ | S1+S4 |
| M6 | gunner share of our core damage | 25.9% | rise | S4 |
| F | r200-300 hazard ratio vs ≥1550 | 0.52 | > 1.0 | all |
| M7 | our heal-cancellation vs 3+ attackers on OUR core | 27-33% | rise toward field's 50-65% | D1 |

### D1 (defensive companion, added after the research arm's separation cut)
Their besieged-side split: we out-cancel the field ~2:1 against a single
attacker (57-66% vs 32-36% — best in corpus, do NOT touch single-attacker
behaviour) but collapse to 27-33% against 3+ while the field rises to 50-65%.
**The deficit is heal-detail SCALING, not heal volume** — a fixed detail
saturates the ~16 HP/round adjacency cap. D1: scale healers assigned to a
besieged core with the observed attacker count (2 attackers → 2-3 healers on
adjacent tiles + core-footprint stacking per the 8 HP/Ti rule; 3+ → full
4-tile detail). Loki must not bleed at home while it sieges — and the same
cut says the field's cores are 2.7× more killable by OUR 3-shooter chain
regardless of map, which strengthens S2's replacement-chain sizing toward 3
concurrent shooters where unit budget allows.
**GATE (research arm's confound, correct): the 3+ collapse could be "already
lost, builders dead" rather than "detail too small." Cut in flight in the
side lane (live builders adjacent to the besieged core in 3+-attacker
rounds). D1 waits on it; S1-S5 do not.**

Falsifier logic: if M1-M3 move and F does not, persistence was not the
binding constraint and this lane's synthesis is wrong on our deficit; if M4
refuses to move while S4 is on, the screen is not clearable by point-blank
gunners and the drain family (P-B) rises in priority.

## 4. Probes the builder should run BEFORE building (minutes each)

1. ~~`self`-persistence probe~~ — ANSWERED, no probe needed (§1): `self` is
   per-unit; shared state goes through the store.
2. Scale-decrement probe: `get_builder_bot_cost()` before/after a
   `self_destruct()` — CLAUDE.md says scale decrements on destroy;
   CLAUDE.md is known-unreliable. Gates the S6 wave-costing math and the
   (parked) scale-sacrifice idea.
3. (Unrelated to this spec but 12 Ti: `can_launch` into an enclosed cell —
   gates imprisonment from the parts inventory.)

## 5. What this spec deliberately does NOT do

No forward turret WALLS (LOKI-3's +0.0pp stands — a shooter chain is not a
wall); no ammo banking; no builder-melee finish; no all-in commit (no
documented abort exists anywhere — the chain is a repeatable pulse, sized to
lose a 20 Ti gunner per link, survivable by construction); no drain/bait
stages yet (gated on the reaction atlas in flight — if opponent turrets shoot
buildings, P-B composes with this siege later as a separate flag family).
