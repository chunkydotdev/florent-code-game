# CAD suppression MECHANISM — 2026-08-09

Deliverable: `docs/research/cad-suppression-mechanism-2026-08-09.md`

Answers the question the lockout cut left open: after early core damage CAD's
build rate over r14-40 collapses ~7x while it still holds ~4 living builder bots.
**What are those builders doing instead?**

Run order (repo root, against a frozen snapshot dir `$FREEZE`):

    # population + version + seat, from <match>.meta.json -- REUSED UNMODIFIED
    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/population.py \
        replay_archive $FREEZE/cad_population.tsv

    # the per-round builder-turn ledger (~12 s for 225 games / 88k rounds)
    .venv/bin/python docs/research/scripts/cad-suppression-mechanism-2026-08-09/mech_decode.py \
        $FREEZE/cad_population.tsv replay_archive $FREEZE/mech_rounds.tsv

    export PYTHONPATH=docs/research/scripts/cad-suppression-mechanism-2026-08-09
    .venv/bin/python $PYTHONPATH/validate.py   $FREEZE
    .venv/bin/python $PYTHONPATH/analyse.py    $FREEZE
    .venv/bin/python $PYTHONPATH/probe.py      $FREEZE
    .venv/bin/python $PYTHONPATH/decompose.py  $FREEZE

`$FREEZE` must also hold a copy of `corpus/join.tsv` (used only for the seat
reconciliation).

| script | what |
| --- | --- |
| `mech_decode.py` | one row per (game, round): every CAD builder-turn labelled heal_core / heal_bldg / heal_bot / build / attack / thrown / move / died / idle, split by whether the bot started the round on an ORTH8 collar seat; plus collar occupancy, builds by type and by distance, buildings lost, titanium, reconstructed cooldowns, botOutput/TLE |
| `validate.py` | seat reconciliation vs `join.tsv`, all-zero column sweep, lockout-landmark reproduction, first-placeEntity vs BuilderBuild cross-check, ledger partition |
| `analyse.py` | the landmark cells, the ledger, predictions 1-3, the four named alternatives, version and opponent splits. Exports `load/cells/agg/wsum/band_of` for the other two |
| `probe.py` | A seat split, B fixed-cohort recovery trace (prediction 4), C contemporaneous cut by core HP, D invariants |
| `decompose.py` | E shift-share (composition vs rate), F idle-by-cooldown, G geography, H money-matched build rate, I build-site distance, J within-band heal dose-response, K within-match pairing |

Design notes that matter if you re-use this:

- **Landmark only.** CAD's opening is a fixed script, so a within-game
  before/after contrast measures the script. Every cell compares the same
  absolute round window between damaged and undamaged games.
- **The unit is the builder-turn**, and the labels partition it because acting
  and moving are mutually exclusive for a builder bot.
- Traps honoured: first-`placeEntity` builds only; `_s64()` on `updateHp.delta`
  with a printed sign census; throws are `moveBuilderBot` with displacement > 1;
  `botOutput` is never used for within-round ordering; `econ.tsv` is not read.
