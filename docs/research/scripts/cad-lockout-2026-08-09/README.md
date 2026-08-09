# CAD lockout population test — 2026-08-09

Deliverable: `docs/research/cad-lockout-population-test-2026-08-09.md`

Run order (from repo root, against a frozen copy of the corpus + the archive):

    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/population.py replay_archive $FREEZE/cad_population.tsv
    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/decode.py     $FREEZE/cad_population.tsv replay_archive $FREEZE/cad_rounds.tsv
    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/outcome.py    $FREEZE/cad_population.tsv replay_archive $FREEZE/cad_outcome.tsv
    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/analyse.py    $FREEZE
    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/latch.py      $FREEZE
    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/opening.py    $FREEZE
    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/moneycut.py   $FREEZE
    .venv/bin/python docs/research/scripts/cad-lockout-2026-08-09/legcheck.py   $FREEZE

$FREEZE must also contain a copy of corpus/join.tsv (used only for the seat
cross-validation and for map names).

- population.py  CAD games + seat + VERSION from <match>.meta.json (220 games,
                 44 matches, 115 of them CAD vs third parties)
- decode.py      per-(game,round) damage / builds / bots / money / ammo / launchers
- outcome.py     winner, win condition, round count, map identity hash
- analyse.py     the landmark comparison, bands, confound cuts, opening invariants
- latch.py       the permanent-latch signature + the money confound
- opening.py     r6 launcher self-destruct and r4 ammo dump, map x version
- moneycut.py    the decisive dump-map vs no-dump-map natural experiment
- legcheck.py    does early core damage convert into a kill

analyse.py exports summarise()/band_of()/win() and is imported by the other four.
