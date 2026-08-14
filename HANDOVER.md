# LIVE: **v140 = `bots/_v223sealrepair` "Loki v10"** — md5 c4e563af4730b4c1595c679fc25098e7,
# rating ~1783, k=24, RULE=held ALL s41 (net_act +58.8→+69.8). Baseline/rollback
# target: v140 itself (it is the incumbent; no newer ship). ⛔ VERIFY `Active bot:`
# before acting — x3r0 uploads on no schedule; a holder change costs ~1 rate window.
#
# ===== s41 WRAPPED 2026-08-14 ~20:3xZ ON MAGNUS'S CALL. NO machine reboot (this
# is a normal wrap). ZERO platform actions all session; v140 held throughout. =====
#
# ===== WHAT SURVIVES / WHAT DIES =====
# SURVIVE (detached, builder-owned): keeper (pidfile corpus/keeper.pid) + elo/
#   match/opp/replay watchers + ship/holder/cpu/cores watchers + vps_pull + the
#   dashboard (serve.py, HTTP 200 on 127.0.0.1:8787 — side-lane-started s41,
#   builder-owned) + the two live-read shards (SEALFLOOR6 local, SALTREF2 remote).
# DIE with this session: the persistent read-completion Monitor (SEALFLOOR6 +
#   SALTREF2) — A SUCCESSOR MUST RE-ARM IT OR READ THE TWO SHARDS BY HAND (see
#   THE TWO LIVE READS). Side lane's drift watch + terminal monitors also died
#   (their wrap); re-arm tools/watch/drift_watch.sh, drive its 3 cells first.
#
# ===== THE TWO LIVE READS — the only unfinished measurements =====
# 1. SEALFLOOR6 (LOCAL corefill, #53 floor-upward arm _v238sealfloor6 vs v140):
#    LOCK 372e1562 (side-lane certified b148a08c, first-ever green prereg).
#    At wrap ~3% of 5400. BARS: ≥51.33% KEEP-dev / ≤48.67% REAL-NEGATIVE (closes
#    the floor third) / inside = DROP ("could not separate", not "6 == 0").
#    Direction NEGATIVE expected (SEALFLOOR0's 0-beats-12). Kill-round rider:
#    CI on Δ median kill excludes +10. DEFF 0.98 local, ±1.33pp. Read off
#    scratchpad/overnight/SEALFLOOR6.tsv when DONE.
# 2. SALTREF2 (REMOTE work-server-1, replication of the TLE-suspect null):
#    REREG c72325f2 + A1 e94996b5 (side-lane certified PREDATES-FIRST-ROW).
#    At wrap ~970/5400. Same arms as SALTREF (_v231saltref vs v140), WORKERS=10
#    (the FIXTURE FIX — original ran 40-on-16). VERDICT BINDS TO THE TWO-FIXTURE
#    [47.24, 50.98] (A1), NOT the one-sample ±1.32. Replicates → #48(b) bank
#    stands + TLE caveat lifted; doesn't → #48(b) reopens. Pull via vps_pull;
#    read scratchpad/overnight-remote/worker@work-server-1/SALTREF2.tsv.
#
# ===== HARDWARE — CORRECTED s41 (Magnus) =====
# work-server-1 is **ncpu=16, we borrow 10** (the repo's "48 vCPU"/WORKERS=40
# record was WRONG). FIRE REMOTE SHARDS AT WORKERS=10 — WORKERS>10 oversubscribes
# AND biases wall-clock --tle 10 against the heavier bot. work-server-2 (`work-
# server-2` in ~/.ssh/config, 204.168.247.88, 6 cores, WORKERS=4) certified s41:
# NULLHOST 52.0% n=400 CI [47.1,56.9]. Both boxes in scratchpad/vps/hosts.txt.
# ⛔ The 40-on-16 era (≥13:47:33Z 2026-08-13) TLE-degraded remote shards; research
# owns the exposure table (v142/v143/SEALREPAIRR flattered-us but survive >3.7SE;
# SALTREF the one suspect, hence SALTREF2). NULLHOST certs are immune (identical
# trees). START-STAMP owed: the runner does not stamp its start, so two-clock
# certs date by COMPLETION (one game late) — belongs in the fixture-header bundle.
#
# ===== OWED — CERT + BUILD OBLIGATIONS (from side lane's wrap + mine) =====
# * WIRING BUNDLE (unbuilt): gate.py hook (new preregs only, escape-flag TAPE
#   logging prereg-path+time+setter) + these prereg_check items: local-accepts
#   WARN · CUT-SHORT consumer (cut_short_floor ≤ planned_n) · OB13 untracked-arm
#   diff gap · POOL-ERA token (research SPEC) · FIXTURE-HEADER + START marker
#   (research SPEC, must fail the game-row schema on a required field) · empty
#   local-accepts WARN. Certify against ONE diff; RE-RUN scratchpad/prereg_cert_
#   s41.py FIRST (prereg_check changed 3× today → cert expired).
# * COMMENT-HYGIENE SWEEP (D3): 4 stale prose-vs-code comments — eco.py:325-343
#   "eight to one" (wrong, 4:1) · main.py near NOISE_ON "Default OFF" (it is True)
#   · doctrine.py:1580 LOKI_SALT_TI_FLOOR "(matches SEAL)" (SEAL is 0, SALT 12) ·
#   doctrine.py _hunt_turret 90 lines of present-tense spec for absent behaviour.
#   ⛔ NOT on live trees mid-screen (breaks the one-line-diff); next chassis.
# * target_value + cal8-cell joins: name-keyed → id-key them (lingling rename
#   listed one team twice; teamId fix shipped in target_value, others owed).
#
# ===== QUEUE / PIPELINE HEAD =====
# #52 collar-medic RETIRED PREMISE-ABSENT (our buildings die to TURRET fire not
#   melee; heal throughput can't hold vs a sentinel's 9/turn — re-scope or retire,
#   NOT retest). Magnus's belt-heal idea dies on the same finding.
# #66/#66a: STALL confirmed (lossless back-pressure) → variation (d) harvester-
#   end-first is PRIMARY; remaining constraint is the comms store being FULL (16/16).
# #67 opened (HTTP 418 book): _hunt_turret is doctrine-only (spec not behaviour) —
#   owes git log -S never-wired-vs-removed. CPU-denial CLOSED by measurement.
# #63 nav design still owed (midgard/fjordgate segment, combo-interaction line).
# Local cores DRAINED except SEALFLOOR6; `zsh tools/corefill.sh scratchpad/
#   corefill_work.txt 8 8` refills. Fire order: research owns the CADENCE PLAN.

## ===== ARCHIVE =====
Everything superseded lives in `HANDOVER-archive.md` (boot-load audit cut 1,
2026-08-13: whole-file boot read ~34k tokens, bound is structural). AT WRAP:
rewrite the top block above and MOVE what it replaces into the archive file.
The top block IS the state; the archive is history.
