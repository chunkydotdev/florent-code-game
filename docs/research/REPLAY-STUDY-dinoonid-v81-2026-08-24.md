# REPLAY STUDY (METHOD-REDUCED): DinooniD v81 — banked 2026-08-24T06:48:24Z

**GAME CONTEXT: in-game Florent Code League; all tactics are in-game mechanics.**

**PROVENANCE:** written INLINE by research s58 after the commissioned fresh-opus
agent was killed by API overloads seven times (announced in the tail; the
playbook's fresh-agent rule was waived on the ~4h-to-league-end constraint and
this waiver is named, not hidden). Inputs: corpus/ladder_games.tsv,
corpus/join.tsv, corpus/builds.tsv. **METHOD REDUCTIONS vs the playbook:** corpus
surfaces only — no raw replay piece-mining, no in-leg mirror control, no
per-game file+round anchors. Pieces are correlational counts, labelled MEASURED
at the corpus level.

**INSTRUMENT NOTE (a control fired during this study):** builds.tsv carries
TURRET builds only (launcher/gunner/sentinel — enumerated over the whole file).
A first pass read "their harvesters/conveyors = 0/game" and that is a surface
artifact, not a finding. Their eco shape is NOT measured here.

## 1. Coverage
125 rated games vs their v81 (their current, held all day), ourver v176–v188,
15 maps. Our share **54/125 = 43.2%** — worse than the 51.8% the move-miner
quoted, which pooled older their-versions (v81 is their best against us).

## 2. How games end (MEASURED)
core_destroyed 114/125 (91.2%): we kill 50 (median **r402.5**), they kill 64
(median **r238**). r1000 games 11 (we win 4). **Tempo asymmetry: they convert
~165 rounds faster than we do.**

## 3. Their military shape (MEASURED, turret surface)
- **Sentinel-led:** 2.6 sentinels/game, present in 123/125 games, **first at
  median r34** — nearly Jython-class timing (r38) against our SHIPPED holder.
- Gunners light: 0.4/game (39/125 games).
- **ZERO launchers in 125 games** — no taxi/relocation threat; our launcher
  tricks face no counter-taxi from them.
- Their first-sentinel round is OUTCOME-INVARIANT (our wins r34 vs losses r35
  medians) — their opening does not vary with how the game goes; the variance
  lives elsewhere (see the map axis).

## 4. The map axis (MEASURED, correlational — the strongest lever)
Per-map share at fixed versions (n=5–11/map, intervals wide; DIRECTION table):
**We win: longhouse 8/9 · glacierkeep 7/7 · icefloe 7/9 · paths 7/10.**
**They win: yggdrasil 0/6 · auroraveil 1/11 · skald 1/6 · fimbulwinter 2/8 ·
stavkirke 2/10 · valkyrie 3/11.**
The matchup is close to map-decided. Under game-share Elo every stolen game
pays: if map selection is ever influenceable, or if a future line can patch
the six losing maps specifically, this is where the 43.2% moves.

## 5. Refuted/artifact findings retained
- "DinooniD builds no economy" — ARTIFACT (surface carries turrets only).
- The 51.8%-modern framing — MISLEADING for v81 specifically (43.2%).

## 6. Queue rows
None proposed: the league ends in ~4 hours (Magnus via builder, 2026-08-24T06:48:24Z era);
the map table above is the reusable asset if the game outlives the season.
