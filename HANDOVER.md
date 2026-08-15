# LIVE: **v140 = `bots/_v223sealrepair` "Loki v10"** — md5 c4e563af4730b4c1595c679fc25098e7,
# rating **1724**, rank #23/125, k=54, RULE=held, drawdown −71 from a 1795 peak.
# Baseline/rollback target: v140 itself. ⛔ VERIFY `Active bot:` BEFORE ACTING — and
# **AS A SEPARATE BLOCKING STEP, NOT A LINE ABOVE THE COMMAND.** s43 fired 5 unrated
# accepts with x3r0's v146 active because the check and the firing loop were in one
# non-blocking block: it printed the disqualifying value and the loop ran anyway.
#
# ===== s43 WRAPPED 2026-08-15 ~05:5xZ ON MAGNUS'S CALL. No reboot. =====
#
# ===== WHAT SURVIVES / WHAT DIES =====
# SURVIVE (detached): keeper (corpus/keeper.pid) + elo/match/opp/replay watchers +
#   ship/cpu/holder watch + vps_pull + dashboard (127.0.0.1:8787) + the local corefill
#   (BODYAWR running, NULL5400 queued) + work-server-2 (BODYAWRR, CURFEW=off) +
#   work-server-1 (curfewed 20:55–04:00Z, SELF-RESUMES, SALTREF2 at 1740/5400).
# DIE with this session: nothing of mine is running — 0 decode procs, all agents landed
#   and relayed. **NO WAKE PATH IS ARMED FOR BODYAWR OR NULL5400** — see READS OWED.
#
# ===== READS OWED — nobody is watching these =====
# 1. **BODYAWR** (#63 BODYAWARE, local, 6454/10800 at wrap). LOCK
#    docs/prereg/SCREEN-bodyaware-2026-08-14.md. BAR **51.93** = 50 + MDE(1.00) +
#    hw(0.93), sized off a PRE-SPECIFIED MDE per OB16. ⛔ **THE READ IS GATED: the shard
#    MAY NOT BE SCORED until the pre-fire delivery gate G1/G2/G3 passes** on the
#    scratchpad/c63_probe_s43 harness — the probe that justified the arm is a POPULATION
#    probe on the INCUMBENT, so nobody has yet shown BODYAWARE REDUCES anything.
#    ⛔ **NO LOCAL FIXTURE CAN PRICE ITS CPU** — local replays carry zero exec fields
#    (tle_census reads 0 across 1,649 builder-turns locally, 8,847µs on platform). A
#    local KEEP buys a platform CPU read, NEVER a ship.
# 2. **BODYAWRR** (ws2, 1672/5400) — replication, **REPORT SEPARATELY, DO NOT POOL**
#    (unregistered pooling + a suspected host term).
# 3. **NULL5400** (queued, local) — byte-identical arms (md5-verified all 4 files).
#    Any deviation from 50.0 is a PURE HOST TERM. ⭐ It is a **live dependency of
#    beltsever's BAR**, whose BASE RATE 50.00 is the assumption it tests.
# 4. **SALTREF2** (ws1, 1740/5400, curfewed) — replication of the TLE-suspect null.
#
# ===== DRAFTED, GREEN, NOT STOCKED — and why =====
# * **SCREEN-launchmax** (launcher ceiling probe): T1/T2 deliberately NOT lifted (measured
#   losses: LAUNCH2 44.67 / LAUNCH3 43.73); T3 is a PORT of _v233evict58 (#58, REFUTED
#   live at 0.04 evictions/game); **T4, the pin-first aim, is the only untested throttle.**
#   Its own G1 is a PRE-FIRE gate. Agent's prior: modal outcome is the DROP band.
# * **SCREEN-beltsever**: ⛔ **clause A IS ALREADY SHIPPED** — `raid.py:424 _salt_turn`
#   cuts an adjacent enemy conveyor and barriers the corpse; 96.5% of ALL our builder
#   attacks land on a conveyor, 0.40 kills/game. What survives is **ore-barriering with
#   NO kill** (ore is the only denial target whose function cannot be relocated).
# * **SCREEN-seatscan** (#8): blocked on a NOISE_ON=False dose probe; and
#   **symmetrisation alone is worth zero** by construction.
# * **SCREEN-crashdrive / SCREEN-gunaxabl / SCREEN-sentthreat / SCREEN-finishhp**: read,
#   or DO-NOT-FIRE on their own gates.
#
# ===== THE FOUR THINGS NOT TO INHERIT UNCHECKED (full text in coordination.md) =====
# 1. ⛔ **The `--fire` tier is ADVISORY** — nothing in the firing path passes it. Fix is
#    corefill.sh gating on it; DEFERRED because BODYAWR is live and corefill is its runner.
# 2. **corpus/throws.tsv has THREE TRAPS** (docs/research/CORRECTION-throws-exile-columns-
#    2026-08-15.md): outcome cols are INSERT-only, there is NO version column, and
#    join.tsv covers ~3,770 files vs meta_join's ~44,785. **Two false headlines came out
#    of this table in one hour.** It is now 24 columns (vfate/vlife/vhp).
# 3. **Cross-host dispersion is n=3 and hinges on 0.053pp.** NULL5400 resolves it.
# 4. **#69 rests on ONE opponent** — Leviathan downgraded at wrap (S−E −8.9pp, includes 0).
#
# ===== OPEN WITH MAGNUS (six, none blocking) =====
# stop-loss observability (SLOT FREE fired 6 polls / ~50 min and CLEARED ITSELF while the
# drawdown worsened) · X3R0_SLOT_RULE vs SHIP_SIT_MIN_K (v146 displaced at k=4 vs a floor
# of 8) · **v144 "Loki rc9.1" is ours, newer than v140, never screened** · PROGRAMME rating
# prose · CLAUDE.md anti-sycophancy wording · **CLAUDE.md's local DEFF-0.98 exemption does
# not cover CROSS-HOST pooling.**
#
# ===== QUEUE =====
# **12 of 16 prereg agents returned NOT DRAFTABLE.** Nine closures banked at
# docs/research/CLOSURES-s43-2026-08-15.md — #21 closed at the RULES LEVEL, #51 RE-LABELLED
# from dead-idea to broken-implementation. **The pattern: the four-part admission checks a
# row HAS a mechanism and never that it is STILL TRUE.** Research owns the annotations.
# ⭐ **And Magnus's standing correction (D6): a mechanism-occurrence kill is only valid if
# the rate is a property of the GAME, not of OUR CONFIGURATION.**

## ===== ARCHIVE =====
Everything superseded lives in `HANDOVER-archive.md` (boot-load audit cut 1,
2026-08-13: whole-file boot read ~34k tokens, bound is structural). AT WRAP:
rewrite the top block above and MOVE what it replaces into the archive file.
The top block IS the state; the archive is history.
