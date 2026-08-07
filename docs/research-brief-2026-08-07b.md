# Research brief #2 — post-Eir-4 cycle (2026-08-07 evening)

For the researcher session: read this file top to bottom, then execute it.
Same rules as docs/research-brief-2026-08-07.md (read its HARD RULES section
verbatim — they apply unchanged): read-only, no arena/submissions/unrated,
findings append to docs/spitball.md + files to your scratchpad findings/ (the
main session harvests before you close), version-tag every claim, HOT items
messaged to the main session directly.

ORIENT: HANDOVER.md (session-12 block), docs/research/2026-08-07-fanout/
meta-census.md (the seed document for every thread below), your predecessor's
toolkit at docs/research/2026-08-07-fanout/toolkit/ (replay_lib.py — use it),
replay_archive/ at repo root (passively collected ladder replays + meta.json
sidecars — check before downloading).

Context since the last brief: Eir 4 (v64) shipped and live (six pieces; see
HANDOVER). Ship gate redefined: class-weighted vs-field battery. The census
found: 44% of our matched pool is point-blank core battery, 36% creeping
picket; sporks (#2, 1960) is the only top-8 team running our economy meta —
correctly; our own live bot's production profile classifies as a sentinel core
battery with a small economy (the identity gap).

## Threads, in priority order

1. **SPORKS SCREEN DECODE (the priority).** sporks v2 is our meta played
   correctly: 15-35 harvesters alive, 4380 median Ti delivered, the top 8's
   highest defensive damage share (35% on enemy units/turrets) via a mid-map
   sentinel screen at 0.61 of core separation — and still 88% core-kill wins.
   Census verdict: "study it, do not imitate it." Deliverable = the MECHANISM:
   the screen's positioning rule, sentinel count/facing policy, what triggers
   advance/retreat, how the economy scales behind it, how it survives the
   farm-death window that kills ours, and how it transitions from screen to
   core kill. 25 games with match ids are cited in the census §2.2/§3; decode
   DEEP (a few games exhaustively) rather than wide. Output feeds the piece
   roadmap directly — sporks is the existence proof for the survivability arc.
2. **ORIZON FAMILY CROSS-CHECK (cheap, high leverage).** team lazy v88 (1892),
   Orizon v34, Team 48 v16 — plus possibly Askar City v72's sentinel-and-
   barrier variant — may be one code family (gunner-only/zero-everything-else,
   aim-dsq ~0, creeping plants; census §2.6, §5.2 + thread-7 findings).
   Compare decision functions across the cited replays: plant-distance
   progression, target priority, ammo cadence, response to being pecked. If
   one mechanism, one counter retires three-plus opponents. State explicitly
   which shipped/queued pieces (D duel discipline, J heal-dispatch reorder,
   B' population floor) the family's kill chain does and does not route
   through.
3. **THE UNCLASSIFIED FIVE.** gsxWins v16, Leviathan v9, OopsGotYourElo v21,
   CtrlAltDefeat v107, SingleCore v7 = 20% of our matched games (census §6).
   One match each (25 games), census method (aim policy, damage split, win
   conditions, timing spreads): closes classification from 73% to 93% and
   finalizes the weighted-battery denominators.

## Close-out

Spitball append under a dated header, completeness pass with an explicit
not-run list, files harvestable in findings/. If a thread's evidence
contradicts the census, the CORRECTION is the deliverable — same rule as
always.
