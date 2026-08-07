# Handover — session 11 start (written 2026-08-07 morning, end of the session-10 marathon)

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
