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
## new maps) → v125 pure-data fix shipped, GRAND class now our strongest
## (65.4% rated, was 25%) → R1000_IS_DEFEAT reverted UNCONDITIONAL (Magnus:
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
