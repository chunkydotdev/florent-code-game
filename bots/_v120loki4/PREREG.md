# LOKI-4 (v120) — the committed opening OFF. Unrated leg, NOT a ship.

version: unrated probe only. **The slot returns to v94 immediately after.**
dev_dir: bots/_v120loki4
line: loki (PROGRAMME.md). **COMPARE_AGAINST `_det_v118loki2b`** — previous line
  iteration. Single-flag change: `LOKI2_RUSH_ON = False`. `main.py`, `raid.py`,
  `eco.py` are byte-identical to the parent (verified by diff), so this is a
  clean ablation and every delta is attributable to that one flag.

produces: **CORE-KILL SHARE.** Offline, turning the committed opening off raises
  `core_kill_share` against both foreign probes that have measurement headroom:
  orizon ALL −15.6pp for the rush (sign p=0.0201), cad ALL −18.9pp (p=0.0033),
  concentrated on SHORT maps (−35.4pp p=0.0005 / −22.9pp p=0.0192), LONG band
  null in both. 360 paired deterministic games, 0 tracebacks, gate CLEARED with
  control equivalence identical 12/12.
  Full result: `docs/RESULT-rush-map-interaction-2026-08-09.md`.

falsifier: **zero core-kill wins on the leg**, or a core-kill share at or below
  the same fixture's rush-ON baseline. Because the offline effect is
  concentrated on SHORT maps, a leg drawn entirely on LONG maps cannot refute
  and I will say so rather than read it.

treatment_occurrence: **TRIVIALLY 100% AND VERIFIED BY CONSTRUCTION.** The
  treatment is the ABSENCE of a behaviour, so there is no occurrence to miss —
  `LOKI2_RUSH_ON = False` is read at both call sites (`main.py:324` seat
  assignment, `raid.py:383` harvester prerequisite and bank floor) on every
  relevant turn. This is the opposite situation to LOKI-3, which failed its
  occurrence bar at 16.7%, and to LOKI-2, which delivered one turret of three.

S5_unrated: **THIS IS the unrated read**, per Magnus's standing directive
  2026-08-09 — *"test theories using unrated games between ladder games."*
  n is whatever the leg returns (typically 5). **Recorded NOT-REFUTED at n=5,
  never `pass`** — at that n only a gross effect is detectable, and the offline
  evidence is what carries the claim, not the leg.

## WHAT WOULD MAKE ME WRONG, WRITTEN BEFORE THE LEG

- **Effect SIZE is not established.** Both offline legs flagged **LOW
  REPLICATION — 90 pairs collapsing to 42/43 distinct shapes.** The paired sign
  tests are the robust part; the percentage-point deltas are not, and I will not
  quote them as an expected ladder gain.
- **Two probes are not the ladder.** Published amputation work puts ~2×
  inflation on proxy results and reports outright sign flips. This leg exists
  precisely because the proxies cannot settle it.
- **Band is confounded with map identity**, not merely core-to-core distance.
- **The mechanism is a story, not a finding.** "On short maps the tempo was
  already there, so waiving the harvester prerequisite and cutting the bank
  floor pays the economy and receives nothing" is coherent and **untested**.
- **This removes a plank that PASSED**, on a currency it was never verdicted
  against. LOKI-2's opening was banked on `time_to_core_kill` (198 → 163) — the
  secondary, and on a dimension the ladder says was never the bottleneck
  (74.4% of our core-kill wins are already inside r250). **If this leg and the
  offline result disagree, the offline result is the one that is only two
  probes deep, and I will not resolve the tie in my own favour.**
- **Seat/map confound on any unrated comparison**: unrated flips seats. If this
  leg draws the opposite seat to its comparison baseline, the delta is
  seat-confounded and I will report it as such rather than read it.
