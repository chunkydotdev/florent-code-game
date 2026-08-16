# ⭐⭐⭐ FIRST: `.venv/bin/python tools/now.py` — the holder comes from fcode status,
# NEVER from a poller or from any line below (this block is a CACHE; it has gone
# stale inside eight minutes before). Then coordination.md tail since the last
# wrap marker. Then the three boot checks.

# ===== s45 WRAP (builder, 2026-08-16T07:39:41Z; Magnus: "then we wrap up") =====

## LIVE (read at wrap; RE-READ before acting)
* HOLDER: **v152 "Loki turbo4 (ammo/heal fix)" — x3r0's, rating ~1787, #19 Emerald.**
  Per standing rule it stays; displacement is governed by X3R0_SLOT_RULE (below).
* CONTROL: **bots/_v223sealrepair (v140)** — Magnus re-affirmed TODAY, verbatim: "lets
  keep benchmark toward v140". Every queued row scores against it. main.py md5
  91d7a4c8dab777a25c83ce2bc470e02c.
* **⭐ AIMING POINT (Magnus, s46 2026-08-16T08:2xZ, verbatim): "Honestly, I'm quite confident
  we will need to score 70% winrate against v140 to have any shot at the top at all, 60% is
  just a step in the right direction."** And v140 stays the benchmark permanently ("If we
  move our benchmark bot all the time all our experiments end up unusable"). Consequence:
  weight mechanism-level ceilings over +1-2pp tuning — the composition operator paid +1.3pp
  once and went flat (s46 audit).
* **SLOT PIPELINE (all three rulings TODAY, encoded in PROGRAMME.md):** (1) an arm must
  MEASURE >= 60.0% vs v140 with +-2pp half-width, 60 mid-span (precision reading —
  58-59.9 does NOT qualify); (2) then head-to-head vs the CURRENT holder's staged
  artifact; (3) beats it => switch. Board shipping baseline: **53.50%** (55.24 is a max
  over 23 arms — winner's curse ~+1.7pp). **Gap to the bar: +6.5pp.**
* DEFENCE_ADMISSION_BAR re-priced to the r300 boundary (Magnus) and scored on **ITT
  RMST₃₀₀ non-regression** (four-case control matrix in PROGRAMME.md). Kill-round
  narrative note: the "55-class kills +17-43 later" story was a CONDITIONING ARTEFACT —
  on RMST the leaders are FLAT and **bodyaware/AWRLNCH are FASTER (−6.84/−6.43 rounds,
  paired CIs)**. ⛔ The PAIRED interval form does NOT transfer to live legs (separate
  matches there: two-sample + own measured DEFF).

## ⭐ LEG-fieldcal IS LIVE ACROSS THIS SEAM (prereg LOCKED 43d9035f, cert
## CERT-LEG-fieldcal-2026-08-16.md, clock2 2026-08-16T06:25:40.381Z, gap +26m39s)
* **WHAT: BODYAWR (v154 'Loki rc10.1') vs v140, 10 PINNED opponents, sign-test primary,
  600 games/arm, TWO-SESSION by registration. A successor reading a half-filled tape
  without this paragraph would read a stopped leg — it is RUNNING.**
* **STATE = scratchpad/fieldcal_state.tsv** (round, per-(arm,cell) accepts, clock2,
  blind streak). At wrap: ~25 accepts (A: Juusto 5, not_adgato 5, Erebus 5; B: Juusto 5
  + Erebus in flight), ZERO leaks through 5 flips, leg-attributable Elo 0.00.
* **RUNNER: tools/fieldcal_scheduler.sh — detached to nohup at wrap (survives all
  sessions).** Self-guarding: per-flip LEAK CHECK (halts on any arm-played rated
  pairing), Elo tripwire −40 ARM-ATTRIBUTED ONLY (platform fallback when the archive is
  stale; BLIND never reads clear; 3 double-blind strikes stop for a human), heartbeats
  every 120s during waits, holder restored inside every invocation.
  STOP: touch scratchpad/FIELDCAL_HALT (never kill -9 — see unrated_run.sh's trap note).
  RESUME: zsh tools/fieldcal_scheduler.sh (state-file resume; nohup it).
* **READOUT IS RESEARCH'S, at the pooling point: each arm >=12 accepts on >=8 cells.**
  Impotence clause is BAR-LEVEL: a pooled null is EXPECTED and must never be read as
  refuting the local finding. Report the window-total Elo BESIDE the arm-attributed sum.

## RUNNING / QUEUED (fleet)
* **local:** eco batch (Magnus's directive) ECOSIPH/ECOSIPC/ECOPAVE/ECOSCK4/ECOSCK6
  (~n=60-110 each) + G401g5 (52.85, 87%) + G414/G415. Then queued: **SEATSPAWN,
  SEATFULL** (the seat-bug rungs), **RUSH72** (#72 reopen). auto_gate --apply loops.
* **ws2 (6 cores):** ECO REPLICATIONS (ECOSIPHR at ~3.8k already, then SIPCR/PAVER/
  SCK4R/SCK6R). REPORT SEPARATELY, NEVER POOL cross-host.
* **ws1 (10 cores, REVIVED today):** G406-G413 combos (moved from local, no dupes).
  Its old STALE "RUNNING" rows (CATRND1, F200SIEGELA, F254COLLARS, LNCHERLY) are
  PRE-SHUTDOWN FOSSILS — dead, partials already read where usable.
* **⛔ FIVE LOCAL SHARDS DIED 06:30-06:53 under the load spike:** G402/G403/G404/G405
  and **V140VS152 — which SELF-ABORTED CORRECTLY at 4/234 NOWINNER (fixture-broken
  guard)**. v152 is a CPU-tuned tree; wall-clock TLE under contention corrupts.
  **SUCCESSOR TASK 1: re-queue the V140VS152 calibration ON ws2** (proper allocation)
  after the eco replications — it is LOAD-BEARING for the 60±2 procedure (gate-1-vs-
  gate-2 distance) and research holds its readout. Re-add G402-405 locally when load
  permits (rows kept; new ids, fresh seeds, one-way rule).

## THE SEAT SEAM (⛔ re-labelled s46: a CORRECTNESS lead, NOT a path to 60 — research's own
## ceiling estimate is board 55.24 → ~58.4 at best, coordination tail s45; the s46 audit
## flagged this header as contradicting its source doc)
+6.28pp seat effect on byte-identical self-play (z=16.24) is OUR CODE; the spawn-ring
hash (main.py:289, absolute coords) carries +4.84pp of it. Fix rungs queued (SEATSPAWN
= spawn only; SEATFULL = all 6 fixable sites, 36/36 equivariance checks, one toggle).
Full site list + fix sketches: docs/research/EQUIVARIANCE-SWEEP-2026-08-16.md.
⛔ Map/seat-CONDITIONAL selection is a CLOSED ROAD (CV ceiling ~59 + x3r0's own router
construct read 31.4% on the ladder and was reverted — local validation of selection
schemes has failed its only external test). The FIX, not a scheme.

## OWED / OPEN (priority order)
1. Eco batch readouts (local + ws2 replications) — Magnus's stated priority.
2. V140VS152 re-queue on ws2 (task 1 above).
3. Seat rung readouts vs research's +6.28 baseline (their read).
4. LEG-fieldcal pooling readout at the pooling point (research's).
5. RUSH72 readout (#72 reopen — mechanism metrics named in its BARS row).
6. BODYAWR G1/G2/G3 delivery-gate scoring is STILL OWED (vintage-A falsifier governs
   it, reads −2 rounds = does NOT fire; the arrival premise behind the gate was
   corrected by research — score it against its OWN locked doc, not the new bar).
7. prereg_check --fire still runs on zero firing paths (inherited, unchanged).
8. stack.py ancestor trap (inherited, unchanged). AGENTS.md regeneration mechanism
   unknown (stale vintage-A text at :400-402).

## WAKE PATH
**Survives this session:** 4 watchers + keeper + watchdog(launchd) + auto_gate --apply
+ gate_watch + dashboard (8787, RESTARTED today — /replays live) + corefill + both
remote workers + **the detached fieldcal scheduler**. **Dies with s45:** my log Monitor
on the scheduler (the log persists; nothing ALERTS a human on the leg — it self-halts
safe instead). Side lane's monitors die with THEIR session — their flip-watching was
never load-bearing after the leak check landed. **Nothing wakes a human anywhere.**

## NEW TOOLING TODAY (all selftested, all pushed)
replay viewer: tools/replay_view.py + dashboard /replays (Magnus's ask — click-to-mark,
round scrubber). fieldcal_scheduler.sh (the leg driver). gate.py --selftest (13 cells;
its zero-coverage gap is closed). orchestrate.sh logs <host>. unrated_run.sh UNPINNED_OK
guard + trap operator-note. queue_check ellipsis on all 5 truncation sites. auto_gate
fired_on column. ⛔ orchestrate.sh is BASH — zsh invocation breaks push's word-split.


## ===== ARCHIVE =====
Everything superseded lives in `HANDOVER-archive.md` (boot-load audit cut 1,
2026-08-13: whole-file boot read ~34k tokens, bound is structural). AT WRAP:
rewrite the top block above and MOVE what it replaces into the archive file.
The top block IS the state; the archive is history.

---
