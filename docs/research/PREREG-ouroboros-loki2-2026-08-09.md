# PRE-REGISTRATION (LOCKED): Ouroboros × Loki-2, before the build

**Side lane, 2026-08-09 15:37 CEST. This is a pre-registration committed to the
repo BEFORE Loki-2 is built or fired, so the prediction cannot be reconstructed
post-hoc — by anyone, through any compaction. If a later doc restates the
prediction differently, THIS commit is the record. The whole loss-autopsy loop
is only valid if the flip list is locked before results exist; a message
promise is not locked (it lives in a context that compacts), a committed file
is.**

## The claim being tested

Loki-2 (the early rush), shipped ALONE, against Ouroboros, on the maps below.

## The baseline, frozen (our current lineage, `corpus/ladder_games.tsv`)

Per (map, seat) win rate vs Ouroboros — **every cell is 0%**, so the prediction
is unusually clean (any single win is signal):

| map | seat a | seat b |
| --- | --- | --- |
| lighthouse | 0/8 | 0/5 |
| atoll | 0/11 | 0/3 |
| eider | 0/6 | 0/4 |
| drumlin | 0/5 | 0/3 |
| hive | 0/5 | 0/2 |
| saga | 0/11 | 0/6 |

Overall vs Ouroboros: **15.3% (23/150)**; core-decided **9/86 = 10%** (they
kill us 77, we kill them 9); tiebreak **14/64 = 22%**.

## The pre-registered prediction (FALSIFIABLE)

1. **Primary:** on {lighthouse, atoll, eider, drumlin, hive}, Loki-2 converts
   core-losses into **core-kill wins** — i.e. the win condition of a flipped
   game is `core_destroyed` in OUR favour, not a tiebreak steal. The baseline
   core-win rate on these maps is ~0%, so **≥3 core-kill wins in a 10-game
   unrated leg is a flip signal** (recorded `NOT-REFUTED (n=10)`, never `pass`).
2. **Mechanism, also pre-registered:** the flip comes from **us killing their
   core earlier than r369** (their measured grind-kill round). A win where their
   core dies late or on tiebreak is NOT the predicted mechanism and must be
   labelled as an off-prediction win.
3. **Seat:** unrated flips seats — record each leg's seat and compare to the
   matching seat baseline above (all 0%, so either seat is clean).
4. **The combination fork:** if Loki-2 alone does NOT reach the bar, the
   pre-registered next step is **Loki-2 + A3 spawn-ring** (deny their
   point-blank gunner grind while the rush lands), re-run on the same maps. A
   flip only after adding A3 is the measured proof the combination was needed.

## What would REFUTE

- <3 core-kill wins across a 10-game leg on the 0%-maps → the rush does not beat
  Ouroboros's gunner grind; do not ship it vs them, autopsy why (did the rush
  land and get out-healed? did it not land? — the decoders answer which).
- Wins that are all tiebreak steals, not core kills → something else changed,
  not the predicted mechanism; the prediction is not confirmed even if the win
  rate moves.

## Provenance & authority

Baselines: `corpus/ladder_games.tsv`, per-(map,seat), verified this lane.
Mechanism (r369 grind, pure-gunner cause, uncontested rush) from the Ouroboros
autopsy in `unrated-campaign-plan-2026-08-09.md`. Firing is builder-only; this
lane owns this pre-registration. **Amendments to this file after the first
unrated leg runs are prohibited — append a new dated result doc instead.**
