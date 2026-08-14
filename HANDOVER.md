# LIVE: **v140 = `bots/_v223sealrepair` "Loki v10"** — rating ~1795, k=20,
# RULE=held all s40. ⛔ VERIFY `Active bot:` before acting (x3r0 uploads on no
# schedule; a holder change costs ~1 rate window ~15-20 min later).
#
# ===== s40 WRAPPED 2026-08-14 ~19:0xZ ON MAGNUS'S CALL — MACHINE REBOOT (A
# REAL ONE; s39's wrap said reboot and none happened — this one Magnus is
# executing himself). EVERYTHING DIES: keeper, elo/match/opp/replay watchers,
# vps_pull, dash, corefill loop wrappers, side-lane drift watch, CAL-8 runner
# (STOP-yielded cleanly). Zero rated exposure in s40; no submit, no activation.
#
# ===== POST-REBOOT BOOT LIST =====
# 1. Re-arm keeper + 4 watchers per tools/monitors/ docstrings (the s39-era
#    invocations are in ps history / the monitors' own headers).
# 2. Re-arm vps_pull: nohup bash tools/monitors/vps_pull.sh >> corpus/vps_pull.log 2>&1 &
#    (remote box IDLE — all 6 shards COMPLETE and pulled; SALTREF verdict banked.)
# 3. ⛔ COREFILL STAYS PAUSED: scratchpad/COREFILL_STOP is MAGNUS'S deliberate
#    pause (s40 ~18:33Z), NOT a crash. Ask him before rm. Loop wrappers need
#    relaunch after reboot even to resume.
# 4. Side lane re-arms its own drift watch (their charter).
# 5. Dashboard (shared infra, builder-owned since s41): nohup .venv/bin/python
#    tools/dash/serve.py >> scratchpad/dash_serve.log 2>&1 &  — verify with
#    curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8787/  (NOT ps).
# ⛔ s41 HARDWARE CORRECTION (Magnus): work-server-1 is ncpu=16, WE BORROW 10 —
#    the repo's "48 vCPU"/WORKERS=40 record was wrong; WORKERS>10 oversubscribes
#    a shared box AND biases wall-clock --tle 10 against the heavier bot. Fire
#    remote shards at WORKERS=10. work-server-2 (6 cores, WORKERS=4) certified
#    s41: NULLHOST 52.0% n=400 in [45.1,54.9]. Retro on 40-on-16-era numbers:
#    research owns it (s42).
# ⚠ s41: team 86d0b484 RENAMED LingLing40 -> lingling_40h ~12:00Z 2026-08-14.
#    NAMES ARE NOT KEYS — name-keyed joins (target_value, cell matching) split
#    or drop a team on rename; key on teamId.
#
# ===== CAL-8 — EXACT STATE + STANDING PRE-LOOK DECISIONS (do NOT re-open) =====
# State: 13 ACCEPTS / 65 GAMES. DERIVE, never inherit (s40's own bug):
#   awk -F'\t' '$3=="ACCEPT"' scratchpad/panel_cal8_fires.tsv | wc -l
#   (cross-check: scratchpad/panel_cal8_pointer.txt; matchId rows in meta_join)
# BELOW the 75-game floor -> NOT READABLE. NO LOOK HAS OCCURRED (both lanes on
# record). Standing decisions, all typed pre-look on the tape:
#   * RESUME to BOUNDARY=15 accepts (31c5606): rm scratchpad/PANEL_CAL8_STOP,
#     then BOUNDARY=15 zsh tools/panel_cal8.sh (nohup, log to scratchpad/) —
#     the ARMED echo prints the armed boundary to the fires tape at launch.
#   * READ with scratchpad/cal8_read.py (research-built, side-lane certified
#     df54ea7; REFUSES below floor; P4 = six-cell SIGN test, pre-filter alpha
#     0.109 — may NOT be upgraded in any write-up; reference pinned v125-only
#     n=155/88 and the tool asserts it).
#   * After the read, CAL-8 rows are SPENT like CAL-7's 110 — no pooling, no
#     top-up (that is the declined look in two steps).
#   * ⚠ Research's s41 boundary tripwire: DO NOT re-arm as written — match the
#     terminal ROWS the runner actually writes (incl. 'PANEL-CAL-8: STOP') and
#     check the CHILD pid, not a pgrep -f pattern (matches the wrapper).
#     CORRECTED per research's own amendment: the monitor DID fire ~4 min late
#     (latency, not silence); only the STOP-yield pattern was a true miss, and
#     the runner-death branch backstopped it.
#   * The read needs NO lane context: cal8_read.py refuses below 75 itself
#     (exit 2), reference fixed+certified df54ea7 (v125-only n=155 — NOT the
#     era-rated table), P4 = six-cell sign test alpha 0.109, non-upgradable.
#     A successor needs the two accepts and nothing else.
# Fire order (research eddea1f): Window 2 HELD pending the P4 read; the
# critical path is REGISTRATIONS, not builds (zero unfired live preregs with
# built arms). FIRE NOTHING until the read.
#
# ===== FILES LEFT BY DYING AGENTS — VERIFY STATE BEFORE TRUSTING =====
# * tools/prereg_check.py — DRAFT, UNCERTIFIED (opus agent died at wrap; spec
#   doc may be missing). Token scope accreted from 3 sources, all in the s40
#   tail: ~15 obligations + side lane's 6 (bar-null, computed Ob-13
#   intersection, reference-side floor, estimator+cluster, planned-n+cut-short,
#   add-only amendments) + PROVENANCE + DOSE (both-verdicts). Side lane owes
#   forced-fail certification; wiring verdict is the builder's. NOT wired.
# * bots/_v232collarmedic — #52 collar-medic arm (dispatch/stay the heal
#   exchange; economics stated at 4:1 NOT the source comment's wrong 8:1).
#   Agent died mid-task: dose probe state UNKNOWN — re-run it (vs
#   _probe_creeper, flag-off mutation must return to control) before any
#   screen. No fire claim; sits pending its prereg (fresh opus agent per the
#   new rule, both charters).
# * Research orphans (their s41 wrap, same hour): check working tree for
#   docs/research/SHORT-TIEBREAK-ANOMALY-2026-08-14.md (archipelago r140/146
#   titanium_collected wins — possible new win path or platform truncation)
#   and docs/research/BOOK-http418-v103-2026-08-14.md.
#
# ===== RULES MINTED s40 (all committed) =====
# Fresh-opus-subagent-per-prereg + lane-ratifies-lock (Magnus; BOTH charters) ·
# PROVENANCE token · DOSE token (probe gates screen, both verdicts) · armed
# values echo to the surface where they bind (panel_cal8 ARMED row) · numbers
# crossing session boundaries are re-derived before decisions consume them ·
# corpus_sanity TRAP 8 fixed (comment-headed TSVs; ragged-row alarm).
# X3R0_SLOT_RULE cost measured for the first time: −74.60 Elo over v134-v139
# (research RATED-DAY-DECODE) — price the rule in Elo at next PROGRAMME touch;
# also owed there: kill/death race is 178/182 (four rounds), not 174/187.
#
# ===== QUEUE/PIPELINE HEAD =====
# Registrations first (eddea1f). Then: #52 arm awaits prereg + probe re-run ·
# #48 rung (b) NULL banked (SALTREF 49.11@5400), rung (c) never screened ·
# #53 re-scoped (floor upward arm cheapest) · #63 nav design still owed
# (shares midgard/fjordgate segment with SPAWNPOCKET — second prereg owes the
# combo-interaction line).

## ===== ARCHIVE =====
Everything superseded lives in `HANDOVER-archive.md` (boot-load audit cut 1,
2026-08-13: whole-file boot read ~34k tokens, bound is structural). AT WRAP:
rewrite the top block above and MOVE what it replaces into the archive file.
The top block IS the state; the archive is history.
