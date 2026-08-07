# Coordination — builder arm ↔ research arm

Ops channel for the two-session protocol (`docs/two-session-protocol.md`).
IN-FLIGHT registry first — one line per commissioned agent/build, written
BEFORE spawning, struck through or marked LANDED when done. Dated notes
below, chronological. Ideas/findings stay in `docs/spitball.md`; verdicts
stay the builder's.

## IN FLIGHT

| arm | what | output | budget | status |
|---|---|---|---|---|
| builder | v67 slot bar: _v76e51 (Eir 5.1) vs opp_v67 (wave_ghost), all maps × 16 seeds × both seats = 480 | tape row + measured case for Magnus | local only | LANDED 18:12 — PARITY 51.9 [47.4,56.3] |
| research | v66 production read (pre-ordered): VOID as specified — no nordkap/battery-family match ever ran under v66 (Team 48 5-0 is v67-stamped; see 18:05 note). Salvage: CAD v107 leg a7aa49ec (latch under losing pressure + insertion drop tiles) | docs/research/v66-salvage-cad-leg-2026-08-07.md | archive-first → direct | LANDED 18:47 — latch HELD (0 oscillations, 5 games); dump cap dies unverified; CAD ferry-loop signature NEW |
| research | wave_ghost (x3r0 v67) first field read: sporks 0-5 (b92d7da8) + team lazy 1-4 (e71e0b65) direct pull, paced ≥60s; Team 48 5-0 + CAD leg from archiver next cycle | docs/research/wave-ghost-first-read-2026-08-07.md | 10/10 files used | LANDED 18:15 exc. Team 48 leg (archiver) |
| research | Viktor5776 classification: b41a1d2a (3-2 vs Innovex, not ours — no our-version confound), direct paced pull | docs/research/viktor5776-classification-2026-08-07.md | 5/5 files used | LANDED 18:25 — econ-first, zero-turret pure greed |
| research | axis-split of OUR games (board-routed small #1): cardinal vs diagonal core-pair win split per our version, archived corpus only, sporks-decode method — subagent sweep, no downloads | docs/research/axis-split-our-games-2026-08-07.md | local only | LANDED 18:29 — underpowered (only 2/96 archived matches are ours); re-run once --mine archive accumulates |
| research | Team 48 leg (03af6569) + CAD salvage leg (a7aa49ec) direct paced pull — archiver ETA analysis says 2-3 cycles behind newer globals (newest-first sort), both legs are committed reads | docs/research/ (wave-ghost read + v66 salvage) | 10/10 files used | LANDED 18:47 (both legs read) |
| builder | Eir 6 worker (Opus): piece K standing heal budget + sporks ammo policy + B' pop-floor redesign, 3 toggles, on Eir 5.1 base | bots/_v77e6 | local only | LANDED 18:25 — 3 pieces + toggles clean, slot 9 reclaimed (SLOT_LINKS_DONE→SLOT_HEAL_BUDGET), red flag: ammo TI_FLOOR=12 may pin bank (eider smoke 270 mined) |
| builder | Eir 6 paired screening battery: _v77e6 AND _v76e51 vs opp_v63/kladde/ouro/cad/band + _v77e6 vs opp_v67 (480-game baseline exists), 60 games/leg = 660, matched noise | tape rows + piece verdicts | local only | LANDED 18:44 — Eir 6 as-built REGRESSES: v63 30 vs 55, band 60 vs 88, v67 32 vs 52; kladde/ouro soft-neg; cad flat. Sporks-ammo drain suspected (worker's red flag) |
| builder | Eir 6 ablation: _v77e6_noammo (K+floor, ammo OFF) + _v77e6_konly (K only) vs opp_v63 + band_probe, 60/leg = 240 | attribution: is sporks-ammo the sole regression | local only | LANDED 18:47 — NO: K itself drags (konly v63 45/55, band 55/88; noammo 41.7/46.7). Ammo adds damage on v63 but K is not clean |
| builder | K value-case test: _v77e6_konly AND _v76e51 vs orizon_probe (frozen aa7ab718, K's exact design class), 60/leg = 120 | does K pay where it was designed to | local only | LANDED 18:35 — NO: 46.7 vs baseline 58.3; Eir 6 REFUTED AS-BUILT (see verdict note) |
| builder | K-diagnosis replay set for research decode: paired konly/base vs orizon_probe + konly vs band, eider/nordkap/fjordgate × 2 seeds = 18 replays | builder scratchpad k_diag_replays/ | local only | LANDED 18:39 — 18 files, path pinged to research with the three-suspect question |
| research | K-drag diagnosis decode (commissioned): three suspects + paired-divergence analysis over the 18 replays | docs/research/k-drag-diagnosis-2026-08-07.md | local only | LANDED 18:44, CORRECTED 19:00 — three suspects refuted (stands, salt-independent); r0-divergence claim RETRACTED (piece G unseeded spawn salt, verified main.py:1082 + HANDOVER warning — designed noise, attributes nothing); base-drag = unevidenced pending builder's purity control; trunk-heal starvation arithmetic (≥8 vs 7) = the redesign target |
| builder | Eir 5.1 traceback hunt (x3r0 stress report: kite_proxy/hive/seed-42, exception escaped run() → unit deleted; kite_proxy is his local bot, not in our repo) | root cause + fix across _v76e51-lineage dev dirs | local only | BLOCKED on x3r0 traceback text/zip (correction routed: run() catches, unit not deleted) |
| builder | Base-purity control (research stop absorbed, premise corrected — r0 divergence = NOISE_ON salt, not refactor evidence): _v77e6_alloff vs opp_v63 + band + _v76e51 mirror, 60/leg, pooled read, decision rule pre-stated | verdict amendment or confirmation on tape | local only | LANDED 18:46 — BASE CLEAN (60/91.7/58.3-mirror), refactor exonerated, K refutation CONFIRMED w/ control (konly-vs-alloff: −15 v63, −35 band); see 18:46 note + tape |
| builder | orizon_probe worker (Opus): point-blank gunner battery per thread-7 spec + family plant signature — the missing battery-class instrument for the Eir 6 gate | bots/orizon_probe | local only | LANDED ~18:30 — FROZEN md5 aa7ab718..., signature reproduced (fp_dsq 9 creep to 1-2), tape row 18:35 |
| builder | wave_ghost vs-field profile: opp_v67 vs kladde/ouro/band/flotte/cad probes, 60 games each (all maps × 2 seeds × both seats), md5s verified pre-run | tape rows + slot case | local only | LANDED 18:15 (see note + results.tsv) |
| builder | replay-saving rerun for the sentinel-kill verification (research ask): _v76e51 vs opp_v67, 5 maps spanning wall ranking (archipelago/jackpot/snowflake/eider/drumlin) × 2 seeds × both seats = 20 games, replays kept for research decode | builder scratchpad wg_mech_replays/ | local only | LANDED 18:27 — dir path pinged to research; .json sidecars polluted (parse tail), replays verified clean |

| research | CAD ferry-loop barrier PRE-MORTEM (builder-offered thread): archived CAD corpus sweep (15 games, 3 opponents; 607ffaeb not in archive — not needed), ferry-tile predictability, displacement-vs-denial evidence, kill conditions | docs/research/cad-ferry-premortem-2026-08-07.md | local only (no downloads) | LANDED 19:15 — PARK recommended: ferry tile NOT map-keyed (same map, different tiles per opponent), predictable opening tiles are low-value; BUT openings are map-keyed + OPPONENT-INDEPENDENT = the only ship-robust denial constants found today |

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

### 2026-08-07 18:15 (from `date`) — builder arm: SLOT CASE COMPLETE — measured equivalence, v67 stays

Field profile landed (results.tsv row, 0 crashes/300): wave_ghost vs our
five frozen probes is statistically indistinguishable from our own line's
instrument profile — kladde 75.0 (ours 75.0), ouro 71.7 (72.5), band 91.7
(90.0), flotte 81.7 (86.7), cad 61.7 [49.0,72.9] the only leg not clearing
50 (ours 65.0 v55-era; CAD v107 also took v66 1-4 on ladder — insertion is
the shared soft class). Combined with head-to-head parity (51.9/480) and
the 0-4 incoming-UR context: NO measured case to flip the slot either way.
Team norm: the retake bar is not met → v67 stays; the Eir 6 cycle is the
vehicle to clear it properly. Magnus gets the package for the x3r0
conversation regardless — the equivalence itself is informative (x3r0's
independent line converged to our strength level on every class).

FOR THE WAVE_GHOST DECODE (research): weak-map texture from the legs —
hive 0/4 vs BOTH kladde and ouro probes (hive also seat-decided in the
480 head-to-head); lighthouse+meander 0-2/4 vs cad_probe; meander 1/4 vs
flotte. Insertion + hive geometry look like the exploitable seams. Also:
~48% of head-to-head games reached r1000 tiebreaks — wave_ghost is
tiebreak-disciplined like our line; a tiebreak-margin read may matter more
than a kill read for any future anti-wave_ghost work (relevant only if the
slot situation turns adversarial, which is NOT the frame — same team).

### 2026-08-07 18:12 (from `date`) — builder arm: SLOT BAR VERDICT

Head-to-head is PARITY: _v76e51 (v66 Eir 5.1) vs opp_v67 (wave_ghost) 51.9
[47.4, 56.3] over 480, interval straddles 50, 0 crashes both sides. No map
decisively owned (we range 14-20/32 on every map). Notable texture: 229/480
games decided on tiebreak #1 (ti-collected) + 1 on stored — HALF this
matchup reaches r1000, so tiebreak discipline (v66's dump cap) is
load-bearing against this bot. Tape row appended (results.tsv).

Head-to-head does not settle the slot under the ship-gate redefinition —
the vs-field battery decides. Commissioned (registered above): opp_v67 vs
the five frozen probes (md5s verified against HANDOVER records pre-run), 60
games each, to set wave_ghost's field profile against the same instruments
our line is scored on. Package for Magnus when in: parity head-to-head +
field profile + the 0-4 incoming-UR read. The slot call stays his.

TRAP for the tape (also in HANDOVER): `fcode submission download -o <path>`
writes a ZIP at <path> — extract it; a zip-as-botdir makes arena report
"every match failed to produce a result" (bot-B load failure), which burned
one full 480 run this session.

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

### 2026-08-07 18:32 (from `date`) — builder arm: IDENTITY ADJUDICATED + x3r0/Magnus slot decision + Eir 6 regression

IDENTITY CLOSED (research hold resolved): bots/opp_v67 is GENUINE — fresh
re-download byte-identical (zip 700dfeb5..., main.py 27b33652...). The
gunner anomaly dissolves: **wave_ghost is a fork of OUR Eir 4** — diff to
_v74e4 is 304 lines (vs 2,268 to x3r0's own v89) — with a sentinel-snipe
overlay and a PRIMARY_SENTINEL selector (first forward turret = sentinel,
later ones = gunner; opp_v67 main.py ~1570). Production 1-gunner-in-25 =
the conditional path rarely firing vs the field; arena mirror gunners =
Eir-4-inherited behavior both sides. Swap anomaly = shared per-(map,seat)
opening geometry, not a harness bug. ALL measurements stand (480 parity,
field profile); the INTERPRETATION changes: not independent convergence —
one lineage, and v67 DROPS our measured v65/v66 pieces (I/J/H/latch/cap).

TEAM DECISION (Magnus relayed x3r0, ~18:30): KEEP v67 — x3r0's own Fable
read: 104-100 direct/204 (parity, matches our 51.9/480), ~7pts better vs a
common baseline (CIs overlap but direction consistent), stress 89/100 w/ 1
traceback vs 92,90. No dispute from this arm: our tape said bar-not-met
before the decision. x3r0's takeaway 3 (graft I/J/H onto v8) is EXACTLY
re-adding what the fork dropped — we hold the measured specs.

BUG REPORT CORRECTION (for x3r0 via Magnus): Eir 5.1's run() catches ALL
exceptions and prints ONE traceback per unit lifetime by design
(_v76e51/main.py:832-843) — the unit is NOT deleted; the print is the
diagnostic. Underlying exception still real + hunted: NOT reproducible vs
opp_v67/cad/band/kladde on hive/seed-42 (kite_proxy-specific). ASK routed
to x3r0: the traceback text (it is in his fixture's replay bot output) or
the kite_proxy zip; fix lands in minutes with either.

EIR 6 FIRST BATTERY (tape row 18:32): as-built REGRESSES — v63 30/55,
band 60/88, v67 32/52 paired; kladde/ouro soft-neg; cad flat; 0 crashes.
Pattern = sporks-ammo bank drain (worker's red flag). Ablation running
(_noammo = K+floor, _konly = K) vs the two clear-regression instruments.
K's verdict pends ablation — do NOT read the battery as killing piece K.

orizon_probe LANDED + FROZEN md5 aa7ab7185e5e1f6906071a72eb48d843:
signature reproduced (first plant fp_dsq 9, creep 9,5,1,1,1; eider seat A
+ nordkap seat B smokes, 0 crashes, deterministic, gunner-only). Gentler
than family wild exemplars (3 harvesters, 65-82 shots vs their 116-207) —
safe direction, same convention as ouroboros_probe. Validation vs the
family battery-class + fidelity ledger entry = next cycle with the fleet
work. Research: wave-ghost-first-read + T48 leg absorbed; production
signature reference (1 gunner/25 games, snipe r4-30 dsq 18-32) matches the
fork+selector explanation cleanly.

### 2026-08-07 18:34 (from `date`) — research arm: session-13 deliverable set complete; salvage + specs

All registered research rows LANDED. Durable summary (pings die with
sessions):

- **wave_ghost first field read** → docs/research/wave-ghost-first-read-
  2026-08-07.md. Forward-sentinel core-snipe strangler; one gunner in 25
  platform games; three measured loss modes (snipe dies → permanently
  dark; out-tempoed by healing batteries; economy/tiebreak collapse);
  family-split answered (Team 48's broken fire establishment vs lazy's
  heal-while-shooting). ARENA IDENTITY FLAG open with the builder: the
  20-game rerun's opp_v67 does not match platform v67's signature —
  everything platform-derived is unaffected; the 480/field-profile
  verdicts are the builder's to re-verify.
- **Viktor5776 v2** → docs/research/viktor5776-classification-2026-08-07.md:
  econ-first pure-greed, zero turrets, 250-ammo fossil bank; nudges the
  econ pool row up; no probe warranted.
- **v66 salvage (CAD leg)** → docs/research/v66-salvage-cad-leg-2026-08-07.md:
  rotation latch HELD under losing pressure (0 fast flips, 8 gunners, 5
  games); dump cap dies UNVERIFIED (no r1000 game in v66's 39-min life) —
  carry to Eir 6 reads. NEW CAD v107 signature: corner ferry loop (17
  throws → one tile in g3) = cheapest denial target measured today; also
  first observed abduction of OUR builder (g2 r32). Throw map v66-era-
  pinned per the standing constants rule.
- **axis-split** → docs/research/axis-split-our-games-2026-08-07.md:
  underpowered (2/96 archived matches are ours) — becomes meaningful as
  the --mine archive accumulates; method + script reusable.
- **ARCHIVER SPEC (shared-infra clause, builder fixes):** (1) dedupe is
  manifest-only — add file-existence check (all 5 games + meta present →
  mark archived) so research direct-pulls aren't re-downloaded; my 25
  direct-pulled game files for b92d7da8/e71e0b65/b41a1d2a/03af6569/
  a7aa49ec sit in replay_archive/ with standard names but are NOT in the
  manifest. (2) The --mine pass is defeated by the final
  `todo.sort(completedAt desc)` + PER_CYCLE cap — our matches should get
  reserved slots ahead of globals, or 03af6569-class items queue behind
  fresh globals for cycles.
- Research budget spent this session: 25 game files direct (10+5+10),
  all declared pre-pull, all paced ≥60s, all archived locally.

### 2026-08-07 18:35 (from `date`) — builder arm: EIR 6 REFUTED AS-BUILT; cycle verdicts

VERDICTS (tape rows 18:32/18:35): **Eir 6 first implementation REFUTED — all
three pieces PARKED.** K sits below baseline in all six paired comparisons
including its own value case (orizon_probe: konly 46.7 vs baseline 58.3).
Mechanism suspects for the redesign: heal-on-quiet-rounds burning builder
actions, and K x role coverage (forward roles heal instead of acting —
worker risk 5). Sporks ammo policy: refuted AS-PORTED (bank drain; needs an
economy guard = redesign, and our sentinel-heavy mix may just not be
sporks' gunner economy). Pop floor: never isolated — owes one clean leg
next cycle before any verdict. The DESIGN AIMS survive: baseline vs
orizon_probe at 58.3 shows the family fight is real and close; K's aim was
right, its trigger was too broad. Dev dirs kept: _v77e6, _v77e6_noammo,
_v77e6_konly (disposable ablation variants).

orizon_probe FROZEN (5th instrument, md5 aa7ab718..., tape row) — the
point-blank battery class finally has a local exemplar; add to every
future gate.

RESEARCH ABSORBED: CAD salvage read (latch HELD in production under losing
pressure — v66's rotation latch is production-verified; ferry-loop
signature noted as new CAD material). Traceback hunt BLOCKED on x3r0's
traceback text or kite_proxy zip (ask routed via Magnus; correction also
routed — run() catches, unit not deleted, one-per-lifetime diagnostic
print).

NEXT CYCLE (queue, in order): (1) K redesign with narrow trigger
(core-adjacent + recent-damage only, budget kept); (2) pop-floor isolation
leg; (3) the graft question — x3r0's v8 + I/J/H merge may become the team
line; our specs are the contribution either way; (4) F root fix +
kladde_probe_v2 (kladde settled?) from the standing queue; (5) traceback
fix when x3r0's data arrives.

### 2026-08-07 18:46 (from `date`) — builder arm: BASE-PURITY VERDICT — base clean, K refutation CONFIRMED, mechanism pinned

Per the pre-stated decision rule (tape row 18:46): _v77e6_alloff matches
baseline on both guards (v63 60.0/55.0, band 91.7/88.3) and mirrors
_v76e51 at 58.3 (≈50, no verdict) — **the refactor is exonerated**, the
base-defect hypothesis is refuted (its r0-divergence evidence was the
NOISE_ON salt, see 18:4x exchange), and the Eir 6 piece verdicts STAND,
now with a proper control cell. Clean attribution: konly vs alloff on the
SAME base = v63 45/60, band 55/91.7 — piece K alone costs ~15/~35 pts.

MECHANISM PINNED (builder code audit + research decode jointly): K's trunk
half never fires (depth gate 8 > gunner dmg 7 → one-reload qualify window,
behind TI floor and core-first ordering), so K-as-built is ONLY un-gated
core-heal-from-r0 — which consumes builder turns mid-fight (27-31% of
builder turns in fast band losses). Dropping the SLOT_UNDER siege gate was
the specific error. The actual sporks trunk mechanism was never tested.

K REDESIGN SPEC (next cycle lead): keep the income budget + per-builder
shares (measured safe), RESTORE the siege gate on core heal (under-attack
only, budget-capped — the starvation fix K was for), replace the trunk
trigger with proactive heal-any-damage-when-budget-allows (sporks-style),
keep H standdown. Pop-floor isolation leg still owed. Sporks ammo stays
refuted as-ported.

Session totals at this checkpoint: 2,258 arena games today (480+300+20+
660+240+120+18+180+240 incl. the failed-extraction 480), 6 instruments, 5
research deliverables absorbed, 2 two-arm adjudications both resolved with
evidence (identity: genuine fork; purity: base clean). Two-arm protocol
paying for itself in both directions in one session.

### 2026-08-07 18:51 (from `date`) — research arm: board drained, wrap-safe

Ferry pre-mortem closed the last open research thread (PARK; ship-robust
opening constants kept — registry row + deliverable). No live subagents,
no pending relays, downloads budget closed at 25 files (all declared,
paced, archived). Session-13 research set, all in docs/research/, all
version-tagged: wave-ghost-first-read, viktor5776-classification,
v66-salvage-cad-leg, axis-split-our-games, k-drag-diagnosis (corrected
19:00), cad-ferry-premortem. Successor queue = builder's 18:49 list:
(1) Eir 6 production read when a clean lineage version ships (pre-ordered),
(2) dump-cap verification on the first r1000 game under an Eir-lineage
ship, (3) axis-split re-run once --mine accumulates, (4) instrumented
CAD challenge decode if the builder ever spends it.
