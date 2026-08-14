# LIVE: **v140 = `bots/_v223sealrepair` "Loki v10"** (mapfix + sealfloor0 +
# l4repair) — shipped 2026-08-14 11:37Z, screen 60.26±2.8@n=1223, rated era
# k=1 net +16.1 (5-0 arsonist duck), SHIP_SIT arms at k>=8. Baseline 1734 @
# 962 at ship. ROLLBACK: v139 (`_v218mapfix`), deeper v125 (`_v197mapcode`).
# ⛔ VERIFY `Active bot:` BEFORE ACTING — x3r0 made 4 unannounced slot moves
# on 2026-08-14 (all taped); his v141 analysis was delivered on his request.

## ===== ⛔ FIRST: WHAT DIES WITH s38 — RE-ARM BEFORE TRUSTING ANYTHING =====
##  1. **gate_watch loop** (`zsh tools/monitors/gate_watch.sh` as a waking
##     session task; ledger scratchpad/gate_watch_state.txt is CURRENT).
##     ⛔ D4 (retro): the manual re-arm step FAILED under ship-flow once
##     today (OSCLOCK2 dropped 45 min late) — build the self-re-arming
##     version before trusting yourself more than s38 did.
##     PENDING GATES/FINALS: MAPFIX2 final (~2160, replication of the v139
##     ship read, was 57.5 tracking above parent) · SEALFLOOR0 final
##     (~55, then D26 pool w/ remote SEALFLOOR0R) · SEALREPAIR (the SHIP's
##     confirmation screen, was 60.3@1223) · L4REPAIR2 (54.3@3023) ·
##     AIMTHROW2 · MAPSALT (x3r0's salt table on v140) · NESTSHOT (#3
##     one-gate arm) · V141VS140 (benchmark answering x3r0's 81.7% claim).
##  2. **holder_watch** (`EXPECT=v140 zsh tools/monitors/holder_watch.sh`).
##  3. **vps_pull loop** (`bash tools/monitors/vps_pull.sh >> corpus/
##     vps_pull.log`) — without it remote rows go stale (dashboard shows
##     pull-age honestly). Remote worker itself SURVIVES: work-server-1,
##     curfew 20:55-04:00 UTC in-worker, SEALFLOOR0R filling (was 53.3).
##  4. **CAL-6 panel runner** (INCUMBENT=140, cal6 PTR/OUT — resumes from
##     its pointer). ⭐ STANDING PANEL RULE (research, inherited trigger):
##     on ANY new holder, CAL-(N+1) fires from the CAL-6 template ONLY
##     after BOTH (a) the holder has held >=40 min (two pairing cycles)
##     AND (b) the tree is identified — prereg before first leg. The
##     panel budget must not idle once both read true.
##  4b. ⛔ CORPUS CAVEAT (research s39; NARROWED s40 13:3xZ): econ.tsv is
##     CORRUPT for v55+-era decodes (dead turns/cpu/ti_collected COLUMN
##     VALUES) — no econ.tsv-denominated reads until the re-decoder ships;
##     build_agg verified unaffected. ⭐ RETRACTED: `tled` is NOT fiction —
##     the wire field is real (botOutput field 4, cross-validated 446 vs 449
##     execTimeUs>10ms). Only the COLUMN is corrupt; fix in flight (s39).
##  5. QUEUE: #14 destination arm (OSCLOCK2's successor — freed-into-
##     idleness strengthened by its 46.4 drop) · #41 siting/facing (the
##     other #3 leg) · MAPSALT local re-sweep if its screen is flat ·
##     scout tier (Magnus-approved in principle, unfired) · fcode 2.3.8
##     upgrade boundary checklist (taped 2026-08-14, incl. --mark 0 on 11
##     call sites + maps/ valkyrie sync).
## ===== THE NIGHT IN ONE PARAGRAPH =====
## Ship bar raised (Magnus) -> s36 slate finals typed (UNDERECO only above-
## band single; COMBO 52.30; ECORAID fix 53.22 best) -> rc8.3/8.4/8.5 live
## legs, ECORAID's leg-1 14/25 REVERSED by the pre-declared pooled n=50
## (23/50 vs control 48% - NO live support, packet correctly not assembled)
## -> the divergence became the COUPLING TEST (Magnus): falsified-as-
## universal on salt, refinement (field-universal vs incumbent-absent
## behaviour) 7/7 retrodictive, prospective probes GBNS/L4REPAIR/SEATREL
## screening with registered predictions -> behaviour-fixture library (2
## bricks calibrated; salt-preempts-repair banked) -> deepening lane stocked
## (#52 collar medic, #53 seal sweep) -> map-conditional test designed
## (qualifying map sets confirmed both candidates, 4 legs, half fired) ->
## x3r0's v134 live + analyzed (v125+17 knobs, r0 trigger flag, courtesy
## battery queued).

## ===== THE QUEUE, IN PRIORITY ORDER =====
##  1. **Type gates/finals as corefill lands:** ECORAID2 (~53.4, finishing),
##     GBNS (marginal 49, GATE-2700 will likely drop), SEATREL (the coupling
##     test's decoupled probe — its final + live transfer prediction is the
##     TEST), X3R0V134 (courtesy battery, gates apply).
##  2. **Resume MB/MC/MD when v125 returns** (item 2 above) -> map-gated-or-
##     stop decision.
##  3. **Upward-baseline read** (25 games fired 05:47, ids in prereg) — v125
##     vs Erebus/HTTP418/0033/farming/kladde; the design brief for the
##     bigger-significance candidate (camp class) hangs on it.
##  4. **Coupling-test prospective reads** as GBNS/L4REPAIR/SEATREL final +
##     get live legs (predictions registered in TEST-coupling-hypothesis).
##  5. **Deepening lane:** #52 collar medic (fixture library customer #1),
##     #48(b) salt-refresh, #53 seal sweep. Screen-trustworthy classes.
##  6. **#51 throw-loop** (serial-victim, emergent) — D17 classification in
##     its prereg when built.
## ⛔ Queue: 30+ unblocked; ALWAYS_BE_RUNNING governs cores; the live budget
## is planned like cores now (research fire orders + leg preregs).

# LIVE: **v125 = `bots/_v197mapcode`** = **"Loki v8"** — shipped 10:16Z (s36, Magnus's call).
# ⛔ **VERIFY WITH `fcode status | grep 'Active bot:'` BEFORE ACTING ON THIS LINE.**
# At wrap 16:4xZ: **rating 1752 (Emerald), k=18, net5 +50, ZERO drawdown since
# activation (1662→1752, first zero-drawdown break-in on record).** k=8 look
# TAKEN (HOLD, certified) and SPENT — no rated reads without a new schedule.
# ROLLBACK: `bots/_v187saltidle_f` (v123); deeper `bots/_v178salt` (v122).
# Slot rule armed+held; fa_union prints on the ship_watch line.

## ===== ⛔ FIRST: WHAT DIED WITH s36 — RE-ARM BEFORE TRUSTING THE SCHEDULE =====
##  1. **THE INTERIM/FINAL LOOK WATCHER (session Monitor) IS DEAD.** Five arms
##     finish tonight UNWATCHED: UNDERECO (~70%→5400), DIGOUT (~73%), TWORAID
##     (~64%), STANDOFF (~43%), COMBO (~8%). **Final look = O'Brien-Fleming
##     final band 48.66–51.34 at n=5400** (all past their interims, all inside
##     when last checked except none outside). Re-arm: watch corefill_status
##     for DONE, then type the final via overnight_read (class lines included).
##     Durable fix queued as D2: auto-stop inside corefill.
##  2. **THE CAL-3 PANEL RUNNER IS DEAD** (it was a session background task).
##     Re-launch: \`INCUMBENT=125 OUT=scratchpad/panel_cal3_fires.tsv
##     PTR=scratchpad/panel_cal3_pointer.txt zsh tools/panel_cal1.sh\` —
##     pointer/fires persist, cells are CAL-3 (fire order #3 @63d45eb).
##  3. **THE VPS PREP AGENT DIED MID-BUILD** (tools/vps/ worker+orchestrator;
##     spec in the s36 tail note ~15:0xZ + the killed git-agent design).
##     Respawn from the registered brief when wanted; nothing committed.
## SURVIVES: keeper (pid 50733) · elo/match/opp/replay watchers · cpu_watch
## loop (pid 18613, 30-min) · dash server :8787 · corefill filler + 5 shards.

## ===== THE DAY IN ONE PARAGRAPH (details in the s36 coordination blocks) =====
## Map rotation crisis → root cause MAP_CODES (builders livelocked on all 10
## new maps) → v125 pure-data fix shipped, GRAND-class kill RESTORED (0/14
## livelock signature gone — categorical; rated MAGNITUDE unresolved at n=34,
## Δ+40.4pp vs DEFF-corrected ±43.5pp half-width, DEFF sweep 2026-08-14)
## → R1000_IS_DEFEAT reverted UNCONDITIONAL (Magnus:
## offensive team) → two opponent classes profiled to the bone (5 books) →
## tri-arm live panel (Magnus's design, --match version-pinned): TWORAID dose
## MET (#42 closed on travel seriality), UNDERECO falsifier NOT FIRED with the
## CONTROL demonstrating the income-lock defect (86 post-chronic rounds) →
## CAL-2 n=150: all six cells above then-rating expectation → COMBO (v9
## candidate: UNDERECO+TWORAID+DIGOUT) filling.

## ===== THE QUEUE, IN PRIORITY ORDER =====
##  1. **Type tonight's five finals as they land** (item 1 above), then the
##     **v9 (COMBO) read**: gated on singles' finals; attribution vs best
##     ingredient, not just control. Ship recommendation to Magnus fully
##     priced — no urgency while v125 climbs at +50/5.
##  2. **#45 KILL THE BUILDER, NOT THE LADDER** — build-first pick (two teams
##     walk point-blank gunner ladders with 1-2 round refunds; the 40 HP
##     feeder is never targeted). Composes with #40 + launcher eviction.
##  3. **Econ rebuild** (research's fireTurret decoder fix @d62753c is in).
##     ⛔ UNTIL REBUILT: shots columns populate for NEW decodes only, so any
##     cut over HISTORY silently mixes a working column with a dead one — the
##     worst shape there is (research's carry). History reads use build_agg
##     metric=='shot'. Run the rebuild when load allows.
##  4. **VPS worker** (item 3 above) — 48-vCPU server incoming; night-one
##     slate = NULLHOST cert then the v9 attribution matrix (4×5400).
##  5. QUEUE.md: 31 unblocked, all grepped against _v197mapcode.
## ⛔ fcode 2.3.6→2.3.7 upgrade ONLY at a shard boundary (pooling hazard).

## ===== ARCHIVE =====
Everything superseded lives in `HANDOVER-archive.md` (boot-load audit cut 1,
executed 2026-08-13: a whole-file boot read measured ~34k tokens and regrew
after a one-time trim, so the bound is structural now). AT WRAP: rewrite the
top block above and MOVE what it replaces into the archive file — do not let
this file grow back. The top block IS the state; the archive is history.
