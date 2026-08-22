# DIAG — the siteless-state decomposition (s55 builder, 2026-08-22)

**Question (HANDOVER s54, successor queue #2):** decompose the engineer's siteless rounds
(v620's NOSITE 648 of 1,991 engineer-rounds = 32.5%, read as "9.7 siting refusals per
tube purchase") into post-plant hold vs watchdog-clear vs travel, with a state-anchored
instrument honestly labelled.

**Answer: the decomposition question was mis-posed by BOTH prior sessions. The 648
NOSITE rounds are none of those three things. They are genuine same-round siting
refusals, and they are 100% concentrated in 2 of the 30 F1 cells — two terminal
band-exhaustion tails on crater-class maps, both defeats.**

## The two corrections to the record (error directions stated, s29 rule)

* **v620 ("site-limited, 9.7 refusals per purchase") — the COUNTER was right, the
  FRAMING was wrong.** The refusals are real refusals (the print sits at
  probe2_ctrl/sk_roles.py:5486, strictly after a same-round `_pick_nest` attempt
  returned None — verified in the applied patch, not the generator). But "site-limited"
  as a property of the CHASSIS was wrong: **28 of 30 cells have ZERO refusal rounds**
  (`scratchpad/s54_v620/q_ctrl_f1/*.log`, grep NOSITE). A mean over a partition whose
  mass sits in 2 cells described no cell. Direction: flattering toward a buildable
  global lever.
* **v621 ("the band scan NEVER refuses; `_pick_nest` succeeds whenever invoked; NOSITE
  was a state counter, post-plant holds and travel included") — WRONG ON BOTH HALVES.**
  Its 10-game probe set did not include icefloe at all and ran paths on seat B; the
  phenomenon lives in icefloe_seatB and paths_seatA. The scan refuses 383+265 times
  there. And the counter characterization was wrong: the anchor is post-pick, so
  post-plant holds (the separate HOLD branch, 1,126) and travel (site set) never reach
  it. **The class: a refutation generalized from cells that lack the phenomenon's
  precondition — the same family as the s29 panel-precondition rule, landed on our own
  fixture.** Direction: flattering toward "question closed, nothing to build".

## The mechanism, clause-exact (s55 rerun of the two cells with v621's per-clause
instrument — the instrument itself was already forced-fire validated in s54)

Known-cell validation: both games replicate the v620 control cells exactly — winner,
turn (opp r698 / opp r1000-tiebreak), and refusal count (383 / 265 == the NOSITE
counts, 1:1 per round). Fixture: F1 (opp_v542wave_noiseoff), seed 7, deterministic.
Logs: `scratchpad/s55_siteless/`.

The scan window is 16×16 = 256 tiles around the enemy core; per-round clause kills
(stable across each tail, so quoted per round; populations sum to 256):

| cell | rounds | taken | oob | band | wall | face | bad | memo | gap | **cand** |
|---|---|---|---|---|---|---|---|---|---|---|
| icefloe_seatB (r284→697) | 383 | 0 | 146 | 84 | 5 | 12 | 8→9 | 1→0 | 0 | **0** |
| paths_seatA (r442→1000) | 265 | 1 | 96 | 120 | 12 | 8 | 11→14 | ~2 | **8** | **0** |

* **icefloe_seatB** — siting the FIRST tube after one tube death (deaths=1: a tube DID
  stand earlier, so the band was viable once). Geometric stock is ~26 in-band non-oob
  tiles; the face requirement kills 12, permanent `nest_bad` bans 8-9, walls 5, memo ~1
  → zero candidates for 400+ consecutive rounds. Core lost r698.
* **paths_seatA** — siting the SECOND tube. Stock ~40; walls 12, `nest_bad` 11→14,
  face 8, **pair-gap 8**, memo ~2 → zero for 265 rounds. r1000 tiebreak = defeat.

## The levers this names (and one it kills)

1. **THE GAP-RELAX IS DEAD CODE IN THE SHIPPED CONFIGURATION.** The v613 retry
   (sk_roles.py:5722) requires `SK_TUBE_FLOOR and SK_TUBE_GAP_RELAX and taken`;
   the shipped head has `SK_TUBE_FLOOR = False` (sk_maps.py:2050), so the relax can
   never arm — while on paths_seatA it had up to 8 gap-blocked candidates recoverable
   EVERY round for 265 rounds. Un-welding the relax from the floor flag is a one-line
   plank with a guaranteed exact-identity-off ablation. (v622 candidate 1.)
2. **Band exhaustion with taken=0 has no fallback at all** (icefloe class). Candidate:
   a last-resort point-blank retry (lo=2) gated STRICTLY on cand=0 — the v1 point-blank
   ban ("close plants die 30% faster") priced point-blank against in-band plants;
   on an exhausted band the alternative is ZERO tubes forever, which is what r698/r1000
   actually paid. Whether icefloe even has point-blank stock is unknown — the fixture
   answers. (v622 candidate 2.)
3. **`nest_bad` is permanent by design on possibly-transient refutations** — a site
   ban earned while an enemy body blocked the walk outlives the blocker. Bigger
   surgery; NOT built this wave, parked with this anchor.
4. **KILLED: any global "reduce siting refusals" lever** (the v620 framing). 28/30
   cells have zero refusals; a global lever optimizes cells that do not have the
   problem.

## Honest labels

Counts are per engineer-round on the 30-cell deterministic F1 fixture (NOISE_OFF
_v542wave copy, fixed maps/seats, seed inert) — a screen for ATTRIBUTION, not a level;
no game-share claim is made here. The 2 hot cells are crater-class maps (field: icefloe
23.06 / paths 28.06 our share, s53 table) — fixing them speaks to the line's worst
terrain, but the currency price of any fix is a powered read's job, not this one's.

Both instruments in this chain were driven both ways before any number was trusted
(mkprobe2's partition: v620 record; the per-clause scan instrument: s54's forced-fire
mutant, `scratchpad/s54_v621/mutant.err`).
