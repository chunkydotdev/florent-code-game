# V152 DIFF INVENTORY — chassis + patch, not fork (builder s46, opus agent, 2026-08-16)

**PROVENANCE: builder-commissioned opus diff-mining of `bots/_x3r0v152` vs
`bots/_v223sealrepair`, Magnus's direct question ("What is v152 doing? Can we
use it and combine it with our experiments?"). Full agent report in the s46
transcript; this doc is the banked inventory.**

**⛔ MAGNUS'S EVIDENCE CAVEAT, RECORDED AT BANK TIME (2026-08-16 ~12:3xZ,
verbatim): "He only runs n=600 vs who knows what, so take his measurements
with a grain of salt."** Every magnitude below that cites x3r0's own analysis
(loki_analysis.md / turbo_identity.py — NEITHER FILE EXISTS IN THIS REPO) is
his-instrument, his-n, his-opponent-pool. Mechanisms were verified HERE
(file:line reads, AST diff, dead-slot check); magnitudes were NOT re-derived.
Research is re-deriving the re-derivable ones on our corpus.

## THE STRUCTURAL FACT
v152 = v140 (`_v223sealrepair`) + one patch: +1,014/−302 lines; doctrine.py a
pure append at :1684; AST module-declaration diff: only-in-v152 = 33,
only-in-v140 = 0, different-value = 0; his tree staged 13 min after our
files' mtimes. LOKI_QUIET_ON, barrier-seal, forward siting, the orphan-belt
and replant bugs are INHERITED v140 behaviours, not his.

## FAMILY A — "LOKI-TURBO" (CPU/navigation rewrite; effectively atomic via A2)
A1 delta tables (doctrine:1713-17) · A2 padded flat byte-grid (eco:563-651) ·
A3 _bfs_direction on the flat grid (eco:1123-1300) ⚠ behaviour changes:
off-map short-circuit + mid-flood CPU probe replaced by up-front check &
4096-node budget — REMOVES THE MID-FLOOD TRUNCATION behind #44's 87%-of-
ceiling quality tax and #63's 3.3× locks · A4 _link_path likewise
(eco:654-760) · A5 map-decode memo (eco:104-124, portable) · A6 str.find
wall/ore scan (main:462-482, portable) · A7 closed-form core distance
(eco:176-260, portable) · A8 static caches incl. the per-round launcher
throw-site rebuild (portable) · A9 hoisted literals (portable).

## FAMILY B — "turbo4" (6 toggled doctrine fixes, all portable)
B1 ghost-magazine brake (SLOT_FWD_GUN counts rubble; rubble buys ammo;
brake = magazine that hasn't fallen in 12 rounds) · B2 burn cap · B3
seat-first while shelled (chase branch sat above the heal-seat branch) ·
B4 chase-break (tile-set ≤2 over 6 rounds = lockstep) · B5 bleed beacon —
core republishes its damage on slot 9, VERIFIED DEAD in both trees (one
writer main:276, zero readers) · B6 converge seat-1 admission past 40 dmg.

## RANKING (plausible share × port cost)
1. A2+A3+A4 (the navigation rewrite — a QUALITY story, not a CPU story).
2. B1+B2 (ammo pair; his decoded worst-case 86% of collected Ti converted).
3. B5+B3. 4. A5-A9. 5. B4, B6 (ride with partners).

## THE PLAN (Magnus: "we have a path forward, lets go!")
* stack.py BASE STAYS at _v223sealrepair (documented ancestor trap; v152
  forks FROM v223 so plank rows pointing at _x3r0v152 are ancestor-correct).
* ARM A: turbo4-only tree (_v427turbo4) — zero CPU change, the half no
  fixture bias can explain. ARM B: turbo × bodyaware HAND-PORT (~20 lines:
  both rewrite _bfs_direction; carry a bodies bytearray through the flat
  template, two passes) — the named SUPER-additivity bet: bodyaware doubles
  the flood cost, turbo removes the truncation eating its value on the maps
  where it should help most. ARM C: full stack + #76, only if A and B read
  positive. All vs v140 (benchmark ruling).
* SHARED BUGS (byte-identical both trees, additive on any chassis): #73
  belt-cut, #75 orphan-belt facing, #76 replant (fix built: _v330sentban).

## TLE/HOST CAVEAT ON THE 57.02 CALIBRATION
v152 is the lighter arm; contention flatters it (TLE-FIXTURE-EXPOSURE doc).
ANSWERED for our shard: ws2 alone, 6 runners on 6 cores, 0 NOWINNER — the
bias's precondition was removed by design. Host provenance travels with the
number.

## B1 RE-DERIVATION ON OUR CORPUS (research 12:31Z; recorded here 2026-08-16T12:33:47Z so the
## inventory's his-instrument caveat resolves for this unit)
Ghost-magazine is REAL as a phenomenon on our 10,231 games (31.51% of
ammo-holding rounds have zero turrets) but NULL as a lever: conversion-waste
share 5.29% for us vs 5.03% field (tie, tail-driven, median 24 Ti/game), and
v152's own idle rate is FLAT vs v151 (31.4→31.1%) — the brake did not move
the metric it targets. ⇒ B1 rides the ported arms UNATTRIBUTED-BY-DESIGN
(BARS rows amended pre-start); it is never reported as tested unless a
dedicated one-toggle ablation runs. Magnus's grain-of-salt caveat: vindicated
on the first unit anyone re-derived.
