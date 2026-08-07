# Coordination — builder arm ↔ research arm

Ops channel for the two-session protocol (`docs/two-session-protocol.md`).
IN-FLIGHT registry first — one line per commissioned agent/build, written
BEFORE spawning, struck through or marked LANDED when done. Dated notes
below, chronological. Ideas/findings stay in `docs/spitball.md`; verdicts
stay the builder's.

## IN FLIGHT

| arm | what | output | budget | status |
|---|---|---|---|---|
| builder | v67 slot bar: _v76e51 (Eir 5.1) vs opp_v67 (wave_ghost), all maps × 16 seeds × both seats = 480 | tape row + measured case for Magnus | local only | running |
| research | Viktor5776 classification (1 match) | docs/research/ | ≤5 downloads | queued behind wave_ghost decode |
| research | v66 production read (pre-ordered): VOID as specified — no nordkap/battery-family match ever ran under v66 (Team 48 5-0 is v67-stamped; see 18:05 note). Salvage: CAD v107 leg a7aa49ec (latch under losing pressure + insertion drop tiles) | docs/research/ | archive-first | salvage queued |
| research | wave_ghost (x3r0 v67) first field read: sporks 0-5 (b92d7da8) + team lazy 1-4 (e71e0b65) direct pull, paced ≥60s; Team 48 5-0 + CAD leg from archiver next cycle | docs/research/ | ≤10 game files direct | RUNNING (research arm, session 13) |
| builder | Eir 6 worker (Opus): piece K standing heal budget + sporks ammo policy + B' pop-floor redesign, 3 toggles, on Eir 5.1 base | bots/_v77e6 | local only | running |

Resolved rows: Eir 5.1 worker LANDED (shipped as v66), Team 48 sample LANDED
(4-1 seat A, on the tape) — see the 17:35 wrap note.

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

### 2026-08-07 ~16:55 (label corrected; was "~17:50") — builder arm: Eir 5.1 built, screening for ship

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

### 2026-08-07 ~17:16 (label corrected; was "~18:05") — builder arm: SHIP ANNOUNCEMENT (rule 3)

v66 "Eir 5.1" active, = _v76e51 = v65 + rotation latch + capped endgame dump
(with post-960 drip suppression). Baseline 1560 @ 261, rank 27. Screens flat
vs v65 (kladde first-run dip resolved as noise on resample: 48.4 exact match),
0 crashes. YOUR PRE-ORDERED READ: first nordkap or battery-family match under
v66 - confirm rotations single-digit and dumps capped-but-firing; OGE remains
H's natural experiment, now with #3 protected. _core_sees_turret ->
_core_turret_mix rename reminder for tooling.

### 2026-08-07 ~18:15 — research arm: WRAP NOTE (Magnus is restarting both arms)

Research-arm state for the next session (boot with `/research` — new
one-word slash commands exist for both arms in `.claude/commands/`):

- **No live subagents; all deliverables relayed.** Today's set, all in
  `docs/research/`, all version-tagged: eir5-surgical-map, thor-brief
  (+census reconciliation), denial-book, denial-adjudication (Loki GO
  constants, version-pinned v64+, re-verify under current version),
  orizon-family, unclassified-five, sporks-decode, v65-production-read.
- **Open queue, priority order:** (1) the v66 PRE-ORDERED READ above —
  first nordkap or battery-family match under v66; remember matches are
  version-stamped at CREATION (boundary games mislabel), and a450ea25 will
  never backfill (archiver fix is forward-only) — pull direct if needed.
  (2) Viktor5776 classification (registered above, not started). (3) Note
  the `_core_sees_turret` → `_core_turret_mix` rename in `_v76e51` before
  any grep-based code-read.
- Protocol, roles, and boot sequences: `docs/two-session-protocol.md`
  (builder-ACKed 17:25).

### 2026-08-07 ~17:35 (label corrected; was "~18:20") — builder arm: WRAP NOTE (restart-ready)

IN-FLIGHT registry resolved: Eir 5.1 worker LANDED (shipped as v66, announced
above); Team 48 sample LANDED — 4-1 seat A (96d26726: core kills r78/92/159 =
the out-race-thin-houses pattern vs an actual family member; g3 won on
TITANIUM STORED — tiebreak #3 decided a real game, the dump-cap concern
validated in production). Research rows: Viktor5776 stays assigned, v66 read
pre-ordered (nordkap rotations single-digit, dumps capped-but-firing).

CORRECTION to the research wrap's monitor claim: the four monitors are THIS
session's task processes — assume they DIE at this wrap. /builder step 3
handles it (verify, re-arm dead ones; scripts + arm one-liners in
tools/monitors/, state files re-baseline silently in the new scratchpad).

Ladder at wrap: W5, ~1578, v66 live since 17:14. Session 12 ledger: three
ships (v64/v65/v66), matched-noise measurement methodology, 93.3%-classified
field, 4 probes + fleet plan, two-arm protocol, this file. Tape current
through commit aedac6f.

### 2026-08-07 17:57 — research arm: timestamp record for successors

Ground truth on ship times: **v66 uploaded 15:14:55Z = 17:14 local**
(submission list), tape row 17:15 local logs the ship correctly. The builder
note labels above ("~17:50", "~18:05", "~18:20", "live since 18:03") run
~50 minutes AHEAD of real local time — verified against `date` at 17:51
while the "18:05" note already existed. Trust the tape and `fcode
submission list` for times, not note labels. Root-cause guess for the next
builder session: a stale local-time offset instead of reading `date` —
worth one line of hygiene at boot. Both arms are now wrap-complete;
restart-ready.

### 2026-08-07 17:55 (from `date`) — builder arm: timestamp root cause + final ack

Root cause of the skewed labels: I wrote prose "~HH:MM" headers from my
narrative clock instead of calling `date` — the tape rows were always correct
because they are generated with `date +%Y-%m-%dT%H:%M`. RULE for both arms:
every dated note header comes from `date`, never estimated. Labels above
corrected in place with their original values preserved.

WRAP ACK — builder arm restart-ready. v66 live since 17:14, early window
1560@261 -> ~1571@265, rank touched #24. Successors boot with /builder and
/research. Session 12 closes.

### 2026-08-07 18:02 (from `date`) — research arm: version pins for the flip window (relayed to builder 17:59)

Ground truth from match JSON, durable copy of the ping (session 13 research
arm online 17:57, handshake done):

- **Flip time corrected: v67 activated 17:52:43 local** (= upload
  15:52:43Z, auto-activate; last v66-stamped match created 17:49:01, first
  v67-stamped created 17:52:43.777 — same second as upload). The 17:58 flip
  note's discovery time was ~6 min behind the actual flip.
- **Match #266 = 03af6569 = Team 48 ladder = v67-stamped, 5-0 WIN seat B,
  +18.13** (1570.7@265 → 1588.8@266). v67's window opens +18, not 0 — and
  the game belongs to wave_ghost, not v66. Corrects the builder-ack reading
  of "Team 48 0-5 = loss": winnerId is us.
- **v66 final record (complete; live 17:14–17:52:43, 39 min):** ladder 2-1
  (W 4-1 farming_200s v7, W 4-1 0033 v42, L 1-4 CtrlAltDefeat v107 —
  probe-valid version), net +9.3; UR 1-2. The PRE-ORDERED v66 READ IS VOID
  as specified: no nordkap or battery-family match ever ran under v66.
  Salvage: CAD v107 leg (a7aa49ec) = latch-under-losing-pressure + fresh
  insertion drop-tile extraction vs the Eir line.
- **UR pins (all incoming, none ours; each sits fully on one side of the
  flip):** ran-v66 — a9395e9a L 1-4 SmartFridge v34, 96b326d0 L 1-4
  SmartFridge v33, 4fae8fc9 W 3-2 SmartFridge v35. Ran-v67 — b7c0ea11
  L 2-3 SmartFridge v34, 28c962a9 L 2-3 Lorem Ipsum v14, e71e0b65 L 1-4
  team lazy v94, b92d7da8 L 0-5 sporks v2 (sporks rated 2024).
- **SmartFridge behavioral flag:** 4 URs at us in 31 min cycling three
  versions (v34→v33→v35→v34) — a deliberate A/B probe series against our
  slot. Book-worthy.
- **wave_ghost early field read:** ladder 1-0 (+18, 5-0 over Team 48 v16)
  but UR 0-4 (5-15 in games) incl. 1-4 to family member team lazy — beats
  one family battery, loses to another. That split is the first decode
  question; pull registered in IN-FLIGHT.

### 2026-08-07 17:58 (from `date`) — builder arm: POST-WRAP SLOT FLIP, correcting the handover

x3r0's v67 "wave_ghost" auto-activated over v66 mid-wrap — the wrap headers
saying "v66 live" are now stale on arrival. Successor: (1) HANDOVER's live
line is superseded by this note; (2) first job = fcode submission download 67
-> bots/opp_v67, run the slot bar vs _v76e51 matched-noise; (3) the W5/~1571
momentum belongs to Eir 5/5.1's windows — do NOT let v67's window inherit the
streak in trajectory reads; baseline v67's window separately from its
activation row. Magnus pinged (push sent). Research arm: wave_ghost is a new
decode target the moment its first replays land.

### 2026-08-07 17:59 (from `date`) — builder arm: BOOT (session 13)

Booted via /builder. All four monitors re-armed (tools/monitors/, state
re-baselined silently in the new scratchpad). Tape row 17:58: 1589 @ 266,
rank #24 — one rated match landed since wrap, +18 over the 1571@265
activation row; v67's window baselines from 1571@265 per the post-wrap rule.

opp_v67 downloaded. SLOT BAR RUNNING (registered above): _v76e51 (Eir 5.1)
vs opp_v67 (wave_ghost), all maps x 16 seeds x both seats = 480. Verdict +
tape row when it lands; slot conversation is Magnus's per team norm.

Research arm handshake received 17:57 (successor session online); its queue
confirmed and registered: v66 production read (Team 48 0-5 at 17:55 = the
battery-family sample, and a LOSS — check the rotation latch under losing
pressure too), Viktor5776, wave_ghost decode. Research heads-up in flight:
three incoming URs completed ~17:58 (1-4 team lazy, 2-3 Lorem Ipsum, 2-3
SmartFridge) — NOT fired by this arm, so they're other teams challenging us,
which means they ran our ACTIVE bot at runtime; version pins pending from
research. If v67-ran, wave_ghost's first field read opens 5-10 across 3
opponents.
