# Eir 5 (v65) — first production mechanism read (2026-08-07 ~17:00)

Research arm. Decoded both class-relevant matches from v65's first six rated
completions (window 4-2 overall): a450ea25 vs Memtrace v27 (point-blank
battery, seat A, 3-2 W) and 071cd20c vs Ouroboros v8 (creeping picket, seat
B, 0-5 L). Toolkit decode, all self-checks implicit in replay_lib. Pre-ship
baselines from the tape: piece I — up to 325 rotations/game, 146 A→B→A;
piece J — counterbattery fires exactly once per game; piece H — 2,700+ Ti
inert at r960.

## Verdicts per piece

**J (defender counterbattery unlock): VERIFIED WORKING.** Counterbattery
builds per game vs Memtrace: 1 / 7 / 11 / 4 / 0 (baseline: ≤1). Under real
pressure (nordkap g3: 14 enemy turrets inside band-41) we answered with 11.
vs Ouroboros: 1-3 per game — it fires, see the leak note below.

**I (rotation discipline): VERIFIED except ONE configuration.** Rotations
per game vs Memtrace: 2 / 5 / **166** / 0 / 0; vs Ouroboros: 0 / 0 / 3 / 0 /
0. The clean games confirm the fix. The exception is **nordkap g3 — the
`chase_battery` map special-case** (20x26, core (9,6)): 166 rotations, 50
A→B→A oscillations = **1,660 Ti burned in a game we lost on
titanium_collected** — plausibly game-deciding, and it also starved piece H
(bank at r960 was ~243). Hypothesis for the builder: discipline's ray-check
and the chase-battery targeting interact — two alternating targets both
passing `can_fire_from` defeats the hysteresis. One-game bug hunt, high
value.

**H (r960 endgame switch): CORE ARM VERIFIED, BUILDER ARM NOT FIRING.**
- Convert: **single 14,634-Ti bank conversion at exactly r960** (snowflake
  g2, won) — the terminal dump works; g3 converted only 243 (bank starved by
  the rotation burn above).
- Harvester spam: **zero endgame harvesters in all three r1000 games**, with
  builders demonstrably alive (antler g4: 972 heal actions). The heal
  priority claims every action under sustained chip pressure — the sporks
  lesson (heal as a ~5% budget, not an absolute priority) showing up in
  production; piece K's case, now measured.
- Fire-all: 0 shots after r960 in all three — line-of-fire binds, exactly as
  T12 found; ammo without a target in range is inert.
- **Design note found in the data:** converting the whole bank zeroes
  tiebreak #3 (titanium_stored). Harmless when #1 decides (g2), but in a
  delivered-tied + harvesters-tied endgame H as shipped would flip tiebreak
  #3 AGAINST us. Re-check the T4 sim's 6/9 flip accounting with #3 in mind,
  and consider withholding the dump unless a target exists or #2 spam
  succeeded.

## The Ouroboros leak survives v65 — and reframes what fixes it

0-5 as seat B (their seat lock holds; coreMin ≤ 0 in three games). J fires
but is outnumbered: their turret counts near/all per game — 11/24, 37/42,
7/27, 13/23, 6/6. Two or three counterbatteries against a 20-40-turret
picket swarm is a droplet. Confirms the Thor-brief staging: this class needs
the Stage-3 race / denial / economy-as-armor, not more counterbattery.
Contrast the Memtrace result: **two round-69 core kills** (eider g1,
archipelago g5, taking 216/0 damage) — against thin-house battery teams our
forward siege wins the race outright. Ouroboros is the thick-house variant.

## Denial constants: v64 rows are ALREADY STALE under v65 (adjudicator's
caveat confirmed within the hour)

Fresh meander observation (071cd20c g2): Ouroboros first gunner **r8
@(8,6)** fp_dsq 25 — matches neither the v64-era book row nor session-12's.
Our v65 changed early-game dynamics; their deterministic queue shifted
again. Consequence for Loki, now confirmed twice: exact-tile constants are
version-fragile. Either (a) re-extract the table after every ship from the
first fresh replays (cheap, automatable off the archive), or (b) design
denial version-robustly — deny approach REGIONS / the historically-stable
home-picket geometry rather than exact tiles. Fjordgate remains the
tightest race (their gunner r2 @(4,6) dsq 4 → core dead r151).

## Infrastructure gap found en route

The replay archiver missed a450ea25 entirely: it harvests the GLOBAL match
list (limit 100) at only 8 matches per 30-min cycle — it cannot keep up
with ladder throughput and gives our own matches no priority. One-line fix
spec: add a `--mine` pass first each cycle (our matches are the A/B-read
corpus; the global harvest can keep the leftover budget). Until then,
research pulls our own replays directly (2s-paced) as done here.

## Bottom line

Two of three pieces verified in production (J fully; I in 9 of 10 games); H
is half-alive (core arm yes, builder arm starved by heal priority). One
config bug (I × chase_battery), one design gap (H × tiebreak #3), one
strategic confirmation (Ouroboros needs Stage 3, not more counterbattery),
one process rule (denial tables expire with OUR ships). v65 window 4-2 with
the Lunds seat-B cell moving for the first time (0-5 → 2-3 vs their v42).
