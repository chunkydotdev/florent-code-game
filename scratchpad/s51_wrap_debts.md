# s51 WRAP DEBT LIST (tool fixes deferred to wrap per Magnus's absolute rule, s48)

From the side-lane wrap-fix re-drive (docs/research/AUDIT-sidelane-wrapfix-redrive-2026-08-18.md):
1. **D1 (HIGH)** ship_watch stale-baseline refusal bypassable + self-laundering: SHIP_VERSION set
   alone (ship_watch.py:586-590, described at :50 as reporting-only) relabels the dead
   v116/1655.0 baseline as the live holder's, prints net_act src=env, persists the mislabeled
   pair so every later run passes. Behaviour-now: nobody sets SHIP_VERSION without SHIP_BASELINE.
   Fix shape: tag the baseline with the provenance of the NUMBER, not whatever version is in scope.
2. **D3 (MED)** atomicio dot-prefix invisibility claim false for pathlib consumers —
   corpus_sanity.py:594 can parse a half-written temp mid-rewrite (race window only).
3. **D4 (LOW-MED)** .started markers are launch-time (corefill.sh:384) — corefill dying after the
   last launch reads DRAINED/0 PROBLEMS.

Carried from s50 wrap (residuals named there): keeper --stop signal handling · 110 old
non-terminal heartbeats · sync_unrated log filter. Carried from s49 hazard 5: submit_clean
guidance strings still Loki-only while its regex accepts Sleipnir — fix both halves together.

Non-tool notes for the wrap retro: my channel message transposed the two gsxWins δ labels
(record unaffected, side-lane caught); D2 atlas correction applied in-session as a record fix
(commit refs in log).
