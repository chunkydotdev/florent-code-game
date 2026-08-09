# Side-lane decoders (2026-08-09) — preserved at session wrap

Validated replay decoders from the third-lane session, preserved so a
successor doesn't rebuild them (~hours of agent work each, all validated
against independent streams). All read-only over `replay_archive/` +
`corpus/`; all run in ~20-40s over the full 2,735-file attributed set with
the repo venv. Attribution join: replay filename prefix `<matchId>_game_N`
→ `corpus/league_matches.tsv` (reconciled 1,180/1,180 vs join.tsv; seat
direction verified 495/495 on sweep matches).

- `rx_decode.py` — per-shot event decoder: fireTurret with shooter AND
  target-tile classification, builderAttack, rotations (direction-changing
  placeEntity re-emits, gunner-only verified), heal overlap per target.
  Validation: shot counts agree 5,470/5,470 sides with the independent
  phase-mining decoder. Fed: opponent-reaction-atlas, drain-discriminator.
- `bb_decode.py` — builder-bot position tracker (spawn/move/death/throw)
  + core-ring adjacency + heal attribution. Validation: 7 checks incl.
  heal×4HP vs UpdateHp stream (median ratio 0.9941, 0 sides >1.0),
  builds−deaths identity 5,470/5,470, throws match corpus/throws.tsv on
  all 1,313 shared files. Fed: besieged-core-confound.
- `dc_decode.py` — death-cause attribution (damage events → killer type/
  position; no-damage residual). Validation: death-round damage == HP loss
  99.45%; lifetime ≥40 HP 19,993/19,993. Fed: builder-death-attribution.
  TRAP it handles: shots are emitted AFTER the victim's removeEntity in
  the round stream; UpdateHp is two's-complement varint.
- `rx_analyse.py`, `build.py` — the atlas and drain-cut aggregation layers
  (per-opponent tables; absorbed-share game table). Kept as worked examples
  of the strata/controls used.

Method notes and full results: each deliverable's provenance section
(`opponent-reaction-atlas`, `besieged-core-confound`,
`builder-death-attribution`, `drain-discriminator`, all `-2026-08-09.md`).
The corpus-howto traps still bind. If the research arm productises the
attribution join into `corpus/`, these should be re-pointed at it.
