# Handover — updated mid-session 11 (2026-08-07, after the v55 ship and the team slot event)

## Session 11 headline state (prepend; original session-11-start notes below still valid)

- **v55 "v70-medic-surge" (`bots/_v70cm`) shipped clean** (kladde 71.2→81.9, opp_v50
  59.2→66.5, guards flat, 0 crashes/1920) — then **x3r0 activated v56 ("v79-lsq-eco…")
  over it** ~06:43Z. Team norm: our line retakes the slot only by beating v79 locally.
- **v55 vs v79 = 53.1 [48.7,57.5] over 480 — parity, bar NOT met.** But the map
  portfolio is near-complementary: v55 sweeps antler/fjordgate/hive/nordkap 32-0
  (+saga/lighthouse majorities), v79 sweeps atoll/heart/jackpot/meander 32-0, 5 maps
  seat-coinflip. AND v55 covers the CtrlAltDefeat insertion class (65.0 vs cad_probe)
  which v79 bleeds to (43.3). Slot decision = Magnus/team judgment; package on the tape.
- **CtrlAltDefeat insertion class decoded** (0-5 ladder loss e40a6c01 under v55, 5 games):
  Launcher r1, 2-3 thrown raiders, sentry ~r11 at core-dsq 10-41, kill median r361.
  Three gaps: hunt band too small (sentinel range 32 > band 20), hunt floor r120,
  population collapse (respawn floor unmeetable at 2-12 Ti banks). **`bots/cad_probe`
  frozen (md5 6d0e955f96de1f0d11f93db573ade458)** — harsher than the original.
- **`bots/_v70cg` = dev branch, NOT shipped** (failed its gate: cad_probe 63.3 vs v55's
  65.0, kladde flat-redistributed). Contains ablation-tested pieces to re-earn their
  place: interceptor BODY-BLOCK (Magnus-scouted: stand in the raider's doorway —
  builders are mutually impassable and can't attack units), siege-mode respawn +
  converter/spawner reserve agreement, hunt band widened to core-footprint dsq≤41.
  REFUTED en route: early-hunt waiver (eider 8/16→0/16), `_v70ec` labor reserve
  (bootstrap inversion), ore-barrier/steal as hive flips (denial works — halves their
  collection — but our own farm survival binds; `_v70sm`/`_v70st` parked).
- **Elo is GAME-SHARE: Δ=32×(games_won/5−E), zero-residual fit** — margin is nearly
  everything, per-game win rate is the ladder currency, one stolen game vs top teams is
  net-positive. Strategic frame in this file corrected accordingly (§ below).
- **Seed amplification trap (game-model.md):** local seeds vary games weakly; a
  seat-decided per-map row ≈ 2 distinct games, not 2×seeds. Weigh pooled rates +
  mechanism, not per-map swings.
- **Cost scale is team-wide** (one multiplier, per-type increments) — twice confirmed;
  the organisers' per-category table is wrong. Conveyor churn = +1%/relay on EVERYTHING.
- Magnus directives this session: **unreasonable variants** (try low-prior exploits) and
  **"play the players"** (exploit measured opponent habits; both in auto-memory).
- Instruments now: band/flotte/kladde probes + **cad_probe** + opp_v50 + **opp_v56**
  (x3r0's v79, downloaded via `fcode submission download 56` — teammate submissions ARE
  locally obtainable; keep opp_v56 as the slot bar).

# Original session-11-start handover (written 2026-08-07 morning, end of the session-10 marathon)

Start here → [docs/game-model.md](docs/game-model.md) → [docs/strategy-log.md](docs/strategy-log.md)
→ [docs/opponents.md](docs/opponents.md). Full session-10 history: git log of this file.

## Where the ladder stands

**Live: platform v54 "v70-respawn-convergence" (= `bots/_v70mh`), activated 2026-08-07
~08:05 at 1550 @ 197 matches, rank #27, Gold.** Trajectory context: the account went
1383/#40 → peak 1597/#24 → ~1550/#27 across sessions 9-10 (+167 net). Predecessors: v53
(`_v68si`) finished 28-26, +43 net, formal KEEP verdict at its 20-match checkpoint. All
baselines and the formal verdict are rows in `elo_history.tsv`.

**v54's ship case (Magnus-approved trade):** flotte_probe 93.3% [89.4, 95.9] vs live
86.7% (+6.6, the wild chip-siege class that was draining the ladder), band 93.3%, kladde
71.2% flat, guards green, 0 crashes in 1200 — accepted a ~4-pt overlapping dip vs
opp_v50 (63.3 → 59.2) because that's a teammate proxy we never face rated, while the
ladder pool looks like the probes. **Before-legs for the production A/B were queued at
ship time** (Lunds eider/hive/jackpot/meander/drumlin; Flotte meander/eider/hive/
lighthouse/atoll — match ids 76282b6e…, 168e6e3b…); check their results FIRST at session
start: flipped games = the convergence working in production.

## What v54 contains (lineage: v53 = `_v68si` → +2 gated keeps)

1. **Builder respawn-on-death** (`_v70rp`): `self.n` was a lifetime spawn counter — a
   dead builder never freed its seat (measured: 586 rounds on 2 live builders, 12,314
   Ti unspent). Replacements refill to the live target of 5, gated ti≥250 ∧ rnd≥60 so
   the opening/cost-scale is untouched (the lesson of `_v69bc`'s -13pt cap-raise).
2. **Multi-healer convergence** (`_v70mh`): role-2 and role-5+ expanders within vision
   of a damaged core converge and heal (+8..+12/rnd vs a chip siege's -9). Proximity-
   bounded by construction (r²=20 vision). Flat vs kladde_probe's 2-3-sentinel barrage
   — healing can't outpace that; see open problems.

## The class model (the big intellectual asset — see strategy-log sessions 10.x)

Opponents beat us in three decoded classes, each with a frozen replay-extracted probe:

| class | probe (md5) | v54 score | wild exemplars |
| --- | --- | --- | --- |
| all-in rush | band_probe (33cd3c14…) | 93.3% | Banminary, Team 48 (map-dep) |
| strangle + chip siege | flotte_probe (ff968416…) | **93.3%** | Flotte, LUNDS, Powerpuff |
| patient grind | kladde_probe (42fa9f50…) | **71.2% — open front** | kladde, sporks, Ouroboros? |

**"Counter-battery blindness"** (Lunds audit, 10 games decoded) unified the middle
class: one infiltrator plants one turret near our core and chips for 150-900 rounds
while we bank 1,165-8,093 Ti unspent. v54's convergence fixes the single-turret
arithmetic. STILL OPEN: multi-turret barrages (kladde_probe eider/hive 0/16), the
single-slot SLOT_THREAT (can't track 2 threats), and turret-hunting (turrets are
BUILDINGS — builders can attack them 2dmg/2Ti; a turret shelling the core does not
shoot back at its attacker; never implemented, ranked next).

## Strategic frame (Magnus + Fable, 2026-08-07, at ~1550-1600; CORRECTED same day)

**MEASURED (session 11, 100-match zero-residual fit): Δ = 32 × (games_won/5 − E),
E = 1/(1+10^((R_opp−R_us)/400)).** The platform scores GAME SHARE, not match outcome —
the original "margin is free / map-majority" frame was wrong. Every individual game is
worth ±6.4 Elo; there is no flip point at 3 games. **The ladder currency is per-game
win rate — exactly what the local arena's Wilson gate measures.** Priorities that
follow: (1) class fixes over per-team fixes (one map row moves against many teams) —
unchanged; (2) near-rating nemeses still the best Elo/effort (E≈0.5 maximizes leverage:
Lunds ✓ flipped by v54, Ouroboros, Landers, Orizon), BUT blowout-loss reduction pays
against anyone in-band, and vs top-8 teams stealing a single game per match is already
net-positive (vs Flotte E≈0.17: 0-5 = −5.4, 1-4 = +1.0) — one-map specialization
against the top is profitable, not vanity; (3) 2-3 and r1000-tiebreak losses remain
the flip-candidates list, and every game dragged to a winnable tiebreak pays a full
+6.4 (strengthens the starvation track).

## The queue

1. **Read the v54 before/after rematches** (ids above) — they decide whether the
   convergence claim holds in production and calibrate everything after.
2. **Turret-hunting** (`_v70th` design): role-split so converged units beside the core
   heal while defender/replacements attack the visible siege turret. Pre-mortem it
   against the kladde_probe eider losses FIRST (retro rule below): are hunters in
   range when the strike lands? If not, the change is flat by geometry like mh was.
3. **Grind residual** (kladde_probe eider/hive 0/16): mechanism NOT fully decoded —
   the strike is 2-3 staggered sentinels; neither labor (rp) nor healing (mh) moved
   it. Diagnose the actual binding constraint from a captured replay before any build.
4. **Nemesis ladder audits:** LUNDS 0-5 lifetime (worsening; the chip class — v54 may
   already fix), Ouroboros 0-4 (likely grind class), Landers, Orizon. Powerpuff and
   I Stone were broken during the night (map-draw dependent).
5. **opp_v50 dip watch:** if v54's ladder trajectory disappoints, the -4 vs the x3r0
   proxy is the first suspect — per-map rows in `mh_v50_full.txt` (session-10
   scratchpad, regenerate if gone).
6. Weekly rotation watch unchanged (15 maps, all local, census at session start).

## Operating notes (updated with the session-10 retro — Magnus signed off)

- **Two-tier, flat:** Fable inline on design/verdicts/measurement; single Opus workers
  implement; single Sonnet readers audit/analyze. Subagents NEVER measure. One gated
  change at a time; results.tsv single-writer.
- **RETRO FIX 1 — map-targeted screens first:** 32-match runs on the 2-3 target maps
  (seconds) before any full 240; full batteries only for keeps/ships.
- **RETRO FIX 2 — pre-mortem variants:** before commissioning an implementation, ask
  an analyst whether the proposed mechanism is BINDING in the actual losing replays
  (four trace-proven-but-game-flat variants in one night taught this).
- **RETRO FIX 3 — threshold the monitors:** the appending Elo logger runs silent;
  wake the session only on new submission, |Δrating| > 25, or a 4+ streak. Re-arm
  BOTH monitors at session start (Elo/submission logger 5-min; match watcher 2-min);
  exactly one appending logger at a time.
- **Ship policy:** local-battery-clean ships (Magnus, session 10); bar = improvement
  on a primary instrument, no clear regressions, guards green, 0 crashes; judgment
  trades (like v54's) get Magnus's call when present. Baseline row at every
  activation; rolling ~20-match trajectory check; rollback on clear unconfounded
  decline. Submissions: `fcode submit bots/<dir>` works from any path and
  AUTO-ACTIVATES; `bots/v*` freeze-copies are Magnus-only (harness-enforced).
- **Unrated matches:** CLI `fcode match unrated <team-id> --map X` (×5); (team,map)
  pairs are deterministic — one sample each, rerun only as before/after across a ship.
  They always run the ACTIVE bot. Rate limit ~5/10min shared.
- **Replay tooling:** tools/replay_census.py + tools/replay_schema.md decode
  .replay26. Session scratchpads DIE with the session — the decoder scripts
  (timeline.py, report_gen.py, econ_curve.py, seat_check.py) must be regenerated from
  replay_census.py by a fresh analyst; budget ~10 min for that on first use. Prefer
  fresh Sonnet analysts + scripts over resuming one long-lived analyst agent.
- SPRT (tools/sprt.py) for screens/discards; fixed-480 for ship gates. The
  identical-per-map-rows fingerprint = the edit didn't change the games (dead branch
  or non-binding mechanism) — caught three such cases; check it reflexively.
- `results.tsv` untracked append-only; `elo_history.tsv` tracked. No git remote.

## Where things live

| path | what |
| --- | --- |
| **`bots/_v70mh`** | **live v54** (= `_v70rp` + convergence) |
| `bots/_v70rp` | respawn-on-death alone (HOLD, clean) |
| `bots/_v69clean` | pre-v70 family head (v53 + succession + dead-branch removal) |
| `bots/_v68si` | live v53 content |
| `bots/band_probe` / `flotte_probe` / `kladde_probe` | the instrument triad, frozen, md5s above |
| `bots/opp_v50` | x3r0's newest (proxy gate; know its -4 caveat) |
| `bots/opp_v49` / `opp_v45` / `opp_v39` / `starter` / `rush_probe_fast` | older references/guards |
| `tools/sprt.py` | SPRT screening gate |
| discarded, kept for reference | `_v69pp` `_v69bc` `_v69dr`(inert-held) `_v67hg*` `_v66eq*` `_v66mA` |

## Traps (session-10 additions to the standing list)

- Store writes buffer one round AND last-write-wins within a round (core first,
  builders after) — a same-round read-back is always stale, and an unguarded builder
  write clobbers a core escalation every round. Guard pattern: write only when the
  stale read is 0.
- Builders cannot attack UNITS, only buildings. Turrets are buildings.
- A turret firing at the core is not firing at its adjacent attacker.
- get_unit_count() lumps core+builders+turrets — use its DROPS, not its value.
- can_heal() refuses a full-HP target, so heal-reflex gates can be loose.
- Probes can be HARDER than their wild exemplars (kladde_probe's 3-sentinel strike vs
  wild kladde's 2) — a flat probe result doesn't kill a wild-pattern fix; weigh both.
- fcode run syntax: map path is POSITIONAL (`fcode run A B maps/x.map26 --seed N`).
