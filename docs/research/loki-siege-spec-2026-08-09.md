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

## 0.5 Relation to the four-plank refutation (builder, 10:31 — read theirs first)

The builder's four planks and this spec do not overlap, and the SITE result
is the strongest external evidence FOR this spec's core flag:
- **What the four planks turned:** count (FLOOR, −0.7pp), ammo price (HOME,
  −2.0pp), anchor location (LOKI-3, +0.0pp), and forward REMOVAL (SITE,
  −6.7pp with dose-response). **None tested persistence** — replacement,
  commitment, or idle behaviour. S1-S3 are decision-layer flags, not turret
  knobs; "the next attempt must not be another turret knob" and this spec
  agree.
- **SITE's dose-response prices the forward programme causally in OUR OWN
  bot:** removing it costs win rate in proportion to how much is removed.
  S2 (replace-on-death) INCREASES the dose of exactly the programme whose
  removal showed proportional harm — it re-adds a unit of something SITE
  just measured as valuable, at the site where it was already earning.
  Applying the builder's own new rule ("what does this thing produce, and
  have I measured that?"): a forward shooter produces fire-rounds; SITE
  measured their removal as harmful; the same-games cut ties fire-rounds
  (28 vs 59) to kill rate (33% vs 46%).
- **The builder's caution stands on S4/S6:** "add support and go forward" as
  a NEW road is the composite rescue in a new costume — noted as live
  hypothesis, not queue item, and this spec defers to that: S2/S3 extend
  the EXISTING forward programme (replace what dies where it died, keep
  firing); they open no new road and move no anchor. S4's payload-type and
  screen-priority choices and S6's insertion opener are the parts nearest
  the closed road and should be sequenced last, behind S2/S3's read.
- M5 ("median shooter life → 40r+") is now the wrong framing per SITE's
  lesson (survival is not the objective): **M5 is DEMOTED to a diagnostic;
  M1 (fire-rounds) and F carry the verdict weight.**

## 0.6 THE r250 WALL — four instruments, one window (joint synthesis with the
research arm, 2026-08-09 afternoon)

Four independently-built instruments, none designed to agree, locate our
failure in the same 250-round window (r251-500):
1. **Core-guard growth stops** — detail matches our opponents' before r250
   (2.24 vs 2.30), then they grow to 3.53 and we hold 2.46
   (`besieged-core-confound`).
2. **Forward posture collapses** — the established r150+ divergence in
   forward share and shooter replacement (phase-mining; `late-game-doctrine`).
3. **Core-death hazard inverts** — conditional kill share turns against us
   55% → 72% across the same span (research arm's hazard curve).
4. **Live turret count flatlines** — the field keeps adding (11.42
   turrets+launchers/game to our 5.15, 2.22×, research-arm verified) while
   ours stops.
The common shape: **our bot stops reinforcing — everywhere at once — around
r250, while holding more titanium than every measured opponent.** S2/S3/D1
are all instances of one rule: KEEP SPENDING ON PRESENCE AFTER r250. Why the
bot stops is not yet located in code (hypothesis, not finding — a build-
priority freeze, a reserve floor, or an emergent budget artifact are all
open); locating it is the highest-value code-read on the board and belongs
to whoever opens the source next.

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

### S2 — REPLACE-ON-FIRING-DEATH (respecified after the research arm's
boundary adjudication — the unconditional version is WITHDRAWN)
Unconditional replace-on-death collapses into the refuted PRODUCTION axis
(steady-state it just raises live count, FLOOR measured −0.7pp): "a turret
that is always replaced is a turret that is always there." The surviving
form conditions on DEMONSTRATED PRODUCTIVITY: **replace a shooter only if it
landed a shot within the last K rounds before dying (K≈10, ablatable) — and
rebuild it on/near the tile where it was earning.** That is conditional on
output, not count — the objective function the SITE lesson demands. While an
enemy core is known and round < 950, a firing shooter's death creates a
build order for the nearest COMMITTED builder. Target: 49% never-replaced →
field's 28-36% *among productive shooters*. The field's 65-round grind IS a
replacement chain (median shooter life 46r); we run chain length 1.
Research-arm adjudication on the boundary (2026-08-09): S3 is cleanly
outside "no more turret knobs" (changes what an existing turret does with
time, touches none of count/placement/price); S2 is outside ONLY in this
conditional form. Builder owns the final call.

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

### ATLAS GATES RESOLVED (2026-08-09, `opponent-reaction-atlas-2026-08-09.md`)
- **The drain pump is ALREADY HAPPENING inadvertently and works**: 97.9-99.4%
  of opponent shots on a heavily-absorbing building of ours overlap a heal on
  that tile — they keep firing at structures whose HP is not dropping. Extreme
  case: one Ouroboros gunner put **677 shots = 2,708 Ti of ammo into a single
  healed 3-Ti conveyor**. Powerpuff 634, OopsGotYourElo 531, Leviathan 446,
  Lunds 428, KCM 427. Deliberate bait-siting (P-B) is live vs these seven+;
  **dead vs Memtrace, Team 48, Askar, Banminary, Bisons, gsxWins, Focalground**
  (1-7% non-core building shots — nothing of ours is ever in their line).
- **Interceptor-saturation bait is DEAD**: observed min inter-throw gap is
  1 round for every throwing opponent — launch cooldown 1, no capacity to
  saturate.
- **Insertion is UNCONTESTED against 6 of 9 priority opponents**: Ouroboros,
  Powerpuff, Leviathan, Orizon build no launchers; KCM and CtrlAltDefeat
  never throw enemy bots (0 across 170 sides). Contested (near-deterministic
  interception, latency 0-1) vs Memtrace 92.7%, Lunds 98.6%, OopsGotYourElo
  74.7%, Focalground 87.4% — S6 should be opponent-gated accordingly.
- **Five teams NEVER rotate a gunner** (Memtrace, OopsGotYourElo, Team 48,
  Bisons, gsxWins) — off-axis approach lanes are permanently safe vs them.
  Rotate-on-sight is sharp vs Ouroboros (3.8x), I Stone (6.8x), KCM.
- **Healer response splits the field**: CtrlAltDefeat median 38.5r latency,
  Team 48 70.5r/17% response, The Bisons never heals — siege pressure vs
  these compounds; Memtrace/Askar/0033 patch in 0-1 rounds.
- Caveat: quantitative columns drift across opponent versions (Powerpuff
  spans 10); qualitative gates (never-rotates, zero-enemy-throws) hold in
  every version observed. Build-on-sight is UNMEASURED (instrument failure,
  honestly flagged), not null.
- **DRAIN PUMP REFUTED (`drain-discriminator-2026-08-09.md`) — DO NOT BUILD
  BAIT.** The discriminating cuts ran (598 games, 7 building-shooters):
  (a) the economy channel is a POWERED NULL — their income delta −2%, CI
  excludes any drain above ~11%; they do not shoot more per round when
  offered bait (they spend LESS ammo); the theoretical ceiling of the whole
  pump is 0.49 Ti/rd = 5.1% of their income. (b) The win association is
  real (+0.199 length-controlled) but NON-DIAGNOSTIC — the placebo kills it:
  shots into EMPTY tiles (purest enemy waste) predict our WORST outcomes
  (−0.257), so the instrument ranks "our material alive and forward", not
  baiting. (c) The 18× asymmetry: high absorbed-share adds +37% to OUR
  ti_coll/rd and ~nothing to theirs. **The surviving effect is HEALED share
  at fixed volume (+7pp win, p=0.045, via +1.69 Ti/rd to OUR economy):
  pipeline UPTIME — "heal what you already built", never "build things to
  be shot." Cheap-absorber composition buys nothing (+0.016, CI spans 0).**
  Any resulting build is a pipeline-heal-uptime rule priced on OUR
  ti_coll/round — and it may already largely exist in the Eir healing engine;
  a code-read of conveyor-heal coverage beats a new flag.
- destroy() closure (research arm + builder, independently verified):
  **zero call sites in our live bots — OUR removeEntity events are all
  enemy kills.** The owner-demolition label only bites on FIELD survival
  figures, asymmetrically (if they self-demolish, their true survival is
  higher than measured).

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
**GATE RESOLVED (`besieged-core-confound-2026-08-09.md`, decoder validated on
7 independent checks): "already lost" REFUTED (5.02 live builders at 3+
attackers, 0.9% zero-builder rounds); "mispositioned" REFUTED (our adjacency
2.68 BEATS field 2.49 and TOP 1.99; utilisation on the field's curve; no
per-builder efficiency deficit at fixed adjacency and damage). What survives
is DETAIL SIZE against a heavier load: full cancellation of our 23.05
dmg/round needs ~5.8 adjacent healers, we run 2.68 at 85% of its own cap
with headroom available (≥1 spare live builder in 91.3% of 3+ rounds, ≥2 in
63.8%). D1 IS UNBLOCKED and now precise:**
- **Corrected cap: a 2x2 core has EIGHT ring tiles → 32 HP/round ceiling,
  not 16.** (The 16 figure is the single-tile cap for 1x1 buildings.)
- Target: grow the core guard with observed attacker count — 3+ attackers →
  4-5 adjacent healers (the ≥1600-rated opponents run a hard-coded FIVE-healer
  guard, 73.6% of their 3+ rounds at exactly adj 5 — an existence proof).
- The when: the gap opens ENTIRELY at r251-500 (before r250 our detail
  matches our opponents' 2.24 vs 2.30; in r251-500 they grow to 3.53, we stay
  2.46) — same window as the forward-posture collapse. Reinforce the guard as
  a function of round/threat, not as a fixed opening allocation.
- Caveat that bounds the win: detail size is dominant but not sole —
  incoming damage matters (Leviathan cancels 61.5% with a SMALLER detail by
  absorbing only 13.6 dmg/round), and the opponent 3+ cell rests on ~50 long
  games from five teams.
- SCOPE correction inherited by the offensive math too: "the field scales
  its detail" was an opponents-of-ours artifact — the BROAD field does NOT
  (34.6% cancel at 3+; TOP 31.5%, both WORSE than our 39.4%). For S2/S4 this
  is good news: a 3-shooter chain against most of the ladder faces a
  defence that does not scale back.

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
