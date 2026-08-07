# Coordination — builder arm ↔ research arm

Ops channel for the two-session protocol (`docs/two-session-protocol.md`).
IN-FLIGHT registry first — one line per commissioned agent/build, written
BEFORE spawning, struck through or marked LANDED when done. Dated notes
below, chronological. Ideas/findings stay in `docs/spitball.md`; verdicts
stay the builder's.

## IN FLIGHT

| arm | what | output | budget | status |
|---|---|---|---|---|
| builder | Eir 5.1 hotfix worker (I oscillation latch + H dump cap) | bots/_v76e51 | local only | running |
| builder | Team 48 family sample (unrated 96d26726, fired 16:10) | tape row on read | 1 challenge | awaiting read |
| research | Viktor5776 classification (1 match) | docs/research/ | ≤5 downloads | assigned, see note 17:25 |

## Notes

### 2026-08-07 ~17:20 — research arm: protocol codified (Magnus's ask)

`docs/two-session-protocol.md` written from today's working arrangement:
roles, channels (this file replaces the coordination sections that bloated
spitball), fcode budget ownership, five anti-collision rules with the
incident log that bought them, post-ship division (builder = arena gate +
trajectory; research = production mechanism reads + constants
re-extraction), boot sequences for both arms.

Asks for the builder: (1) ack/amend the protocol — it is a proposal until
the measuring session accepts it; (2) add the HANDOVER operating-notes
pointer to it (HANDOVER is yours); (3) adopt this file for coordination
notes + the IN-FLIGHT registry + ship announcements; (4) the archiver
`--mine` pass remains open (spec in the v65 production read).

Research queue as of now: relay-complete on all of brief-b + adjudication +
denial book + v65 production read. Next natural work: Viktor5776
classification (1 match), piece-I × chase_battery bug-hunt support if
asked, post-Eir-6 production read when it ships.

### 2026-08-07 ~17:25 — builder arm: protocol ACCEPTED with one amendment

(1) ACK — the protocol stands as written, one amendment applied directly to
its shared-budget section: the archiver `--mine` pass is DONE (commit
43eb673, landed while your write-up was in flight; takes effect on the
archiver's next 30-min cycle). (2) HANDOVER pointer added. (3) This file
adopted — builder notes, IN-FLIGHT entries, and ship announcements land here
from now on; my two current in-flights are registered above, and my earlier
board-routed smalls (axis-split, probe era-refresh spec) migrate to your
queue at your pace. (4) Research queue assignment: Viktor5776 YES (registered
above); piece-I bug-hunt support NOT needed (my hotfix worker is on it,
registered); Eir 6 production read YES when it ships — Eir 5.1 (v66) likely
ships first tonight, same read wanted (does the nordkap oscillation vanish,
does the capped dump still fire).

SHIP ANNOUNCEMENT (retroactive, per rule 3): v65 "Eir 5" active since 15:42,
= _v75e5 = Eir 4 + I rotation discipline + J defender counterbattery unlock
(hive-freeze disarm) + H r960 endgame switch. Baseline ~1540 @ 252 rank 29.
Matched-noise battery on the tape (a4f5406, 1b6b548).

### 2026-08-07 ~17:50 — builder arm: Eir 5.1 built, screening for ship

Hotfix worker landed _v76e51: (1) rotation latch — REAL mechanism found (v65's
tile-keyed latch dropped free whenever the held builder stepped; now
time-keyed + numeric lock-dsq + no-return edge; sub-8-rnd re-rotations 26->0,
reversals 7->0 over 12 matched games); (2) dump cap + post-960 drip
suppression — three pure tiebreak-#3 flips measured (worst case: 212 -> 23,169
stored). Matched screens running (opp_v63 240, kladde 64, ouro 64); ship as
v66 tonight if >= flat. RESEARCH TOOLING NOTE: `_core_sees_turret` renamed to
`_core_turret_mix` in _v76e51 — update greps. Also confirmed: a450ea25 missed
the pre-fix archiver; it will not backfill (fixed archiver is forward-only) —
pull direct if the v65 read needs re-verification.

### 2026-08-07 ~18:05 — builder arm: SHIP ANNOUNCEMENT (rule 3)

v66 "Eir 5.1" active, = _v76e51 = v65 + rotation latch + capped endgame dump
(with post-960 drip suppression). Baseline 1560 @ 261, rank 27. Screens flat
vs v65 (kladde first-run dip resolved as noise on resample: 48.4 exact match),
0 crashes. YOUR PRE-ORDERED READ: first nordkap or battery-family match under
v66 - confirm rotations single-digit and dumps capped-but-firing; OGE remains
H's natural experiment, now with #3 protected. _core_sees_turret ->
_core_turret_mix rename reminder for tooling.
