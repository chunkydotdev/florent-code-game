# PREREG — MAP-CONDITIONAL LIVE TEST (Magnus: "do we have a set of maps where
# it would be most efficient? See if it makes a difference on those,
# otherwise stop testing")

**Committed before any fire.** Builder s37, 2026-08-14. Qualification rule
was stated BEFORE the per-map computation (coordination/session record):
primary ≥55% AND replication ≥52% same map. Results:
* **APPRLAUNCH maps:** antler, drumlin, icefloe, midgard (+glacierkeep as
  declared 5th — replication-strong at 58.6, primary 54.7 a hair under bar).
* **ECORAID maps:** antler, auroraveil, frostgate, royale (+valkyrie as
  declared 5th — 54.4/56.2).

## Design — four legs, upward opponents (relevance), map-pinned via --map
| leg | bot | maps | opponents |
|---|---|---|---|
| MA | v125 incumbent (active, no submit) | APPR set | U1-U5 (upward five) |
| MB | v125 incumbent | ECO set | U1-U5 |
| MC | rc8.4b (_v207apprlaunch) | APPR set | U1-U5, pinned to MA's match ids |
| MD | rc8.5c (_v213ecoraid) | ECO set | U1-U5, pinned to MB's match ids |

Read per the coupling-test METHOD PIN: gap = (candidate − v125) on the SAME
cells and SAME map sets — the map-set confound cancels within each pair.
Counts only, n=25/leg. **DECISION RULE (Magnus's, encoded): if a candidate
beats its matched v125 leg on its own qualifying maps (net matched-cell
count > 0 with the difference visible outside coin-flip territory at n=25,
i.e. ≥ +4 games), the MAP-GATED variant becomes the build (the MAPCODE
pattern: enable the plank's flags only on its qualifying maps). Otherwise
BOTH candidates STOP — no further tests, rows annotated.**
Coupling caveat carried: both planks are incumbent-absent-coupled, so their
SCREENS flatter — this live read is exactly the surface that doesn't.

## Windows
MA/MB: incumbent plays — no activation, any rate window. MC/MD: submit-hold
legs in post-pairing windows, ids copied from this table + MA/MB's minted
anchors, standard leak discipline.
