# ⭐⭐ LIVE AT s44 WRAP (2026-08-15T16:0xZ): **v151 "Loki v10 turbo (CPU)", uploaded by
# x3r0 15:54 and ACTIVE.** Rating **1707** on the newest tape row (1720 → 1707).
# **WE SHIPPED NOTHING TODAY — zero submissions, zero activations. The no-ship rule held.**
# Per Magnus, *"If x3r0 launches a new bot it stays"* — so v151 stays. Do not roll it back.
#
# ⛔⛔ **AND THE CONTROL HAS DIVERGED FROM THE LIVE BOT. READ THIS BEFORE ANY VERDICT.**
# Magnus, s44: *"Everything needs to beat 140, nothing else matters."*  v140 =
# `bots/_v223sealrepair` and **every one of our 88 live queue rows is scored against it**
# (audited clean, `control_pin.py --audit`). **But v151 is v140 PLUS the CPU cleanup** —
# three pure-waste removals (`_sabotage_prio` short-circuit, `_expand` CARDINALS,
# `LOKI_L4_LOG` off), det-verified 100/100 identical at `--tle 0`. **I reverted that
# cleanup LOCALLY twice today because it moved the control under 31 queued arms; x3r0
# then shipped it.** ⇒ **"beat v140" and "beat what is live" are no longer the same
# instruction, and Magnus's ruling names v140.** Follow v140 until he says otherwise, and
# put this divergence in front of him early.
#
# ⛔ THE HONEST CEILING TODAY IS **55.4% against v140**, not 65%. Anything on a board
# reading 59-73% is scored against an OLDER control and **sorts high because it is scored
# against a weaker bot** (SALTIDLE2 64.57% vs v116, MAPCODE 73.27% vs another arm's
# TREATMENT). I quoted three of those to Magnus as leaders before he caught it. The v140
# leaders are: **MIX281mix4 55.41% · MIX282mix5 55.34% · MIX280mix4 54.92% ·
# MIX284mix3 54.90% · AWRLNCH 53.95% · BODYAWR 53.70% (n=10,800)** — four of the six are
# the COMBINATION arms, which is Magnus's thesis holding at +5.4pp, not +15.
#
# --- the block below is the 11:39Z state, kept for its still-live warnings ---
# LIVE: **v140 = `bots/_v223sealrepair` "Loki v10"** — md5 c4e563af4730b4c1595c679fc25098e7,
# rating **1686 (GOLD — demoted out of Emerald)**, k=71, **RULE=SLOT FREE**, both SPRT
# arms **BLEED**, net5 −27.0. Read at 2026-08-15T11:39Z.
# ⛔ **THIS NUMBER IS A CACHE AND IT WAS STALE WITHIN EIGHT MINUTES OF BEING WRITTEN**
# — I wrote 1696 at 11:31Z and it read 1686 at 11:39Z, mid-edit. **DO NOT TRUST THE
# DIGITS ON THIS LINE. RE-READ BEFORE ACTING:**
#     `.venv/bin/fcode status | grep "Active bot:"`   and   `tail -1 corpus/ship_watch.log`
# The DIRECTION (falling, stop-loss firing, slot frozen by rule) is what this line is
# for; the value is illustrative only. This is the open stop-loss-observability item
# (below) demonstrating itself: prose cannot hold a moving number, which is why the
# fix asked for is a LATCHED FIELD rather than a better habit.
# ⛔⛔ **THE STOP-LOSS HAS BEEN FIRING SINCE 08:42Z AND WE ARE CORRECTLY DOING NOTHING.**
# Magnus, s44 08:11Z: *"we do not put a new bot in the slot, i want to see how much of a
# better bot we can build"* and *"If x3r0 launches a new bot it stays, we don't touch
# active bot today."* **His rule supersedes `slot_rule`; the SLOT FREE rows are the
# EXPECTED COST of the freeze, not a breach.** `X3R0_SLOT_RULE` is SUSPENDED for the
# session (`PROGRAMME.md` deliberately NOT edited — a today-rule lives in the tape, not
# in a parsed field, or tomorrow inherits a suspension nobody meant to make permanent).
# ⚠ **THREE DIFFERENT DRAWDOWN NUMBERS AND ONLY ONE IS THE FREEZE'S PRICE — do not
# quote the biggest.** −99 is from an ALL-TIME peak set under a different opponent mix;
# −52 is same-day from 07:02; **the freeze can only be charged for what happened after
# it was set at 08:11Z, which is 1739 → 1696 = −43.** Magnus was shown the number and
# said *"Its okay, focus on grinding."*
# ⛔ **AND NOTHING HERE IS AN ARGUMENT TO SHIP.** No arm is screened, the grinder has
# produced no verdict, and *"the rating is falling"* is not evidence that any particular
# replacement is better.
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
# 4. ⭐ **SALTREF2 — COMPLETE AND READ AT WRAP. THE NULL DID NOT REPLICATE.**
#    ws1 n=5400 **51.7778%** [50.46, 53.10] vs the A1 locked interval **[47.24, 50.98]**
#    and the original's 49.1111% [47.79, 50.43] — **the two CIs DO NOT OVERLAP.**
#    Same host, same arms, same n; ONE change: WORKERS 40→10 on ncpu=16. **The direction
#    was PRE-REGISTERED** ("TLE bias under contention runs toward the null for a
#    work-adding treatment") and met at +2.67pp. ⇒ **#48 rung (b)'s bank REOPENS.**
#    ⛔ NOT a KEEP: the clean read excludes 50, but the REREG registered a REPLICATION
#    verdict, not a treatment bar — promoting it needs its own bar + MDE (OB16).
#    ⚠ **THE 40-on-16 EXPOSURE TABLE MUST BE RE-READ**: v142/v143/SEALREPAIRR were
#    assessed as flattered-but-surviving BEFORE a same-host re-run moved a number 2.67pp.
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
# ⛔ ===== A BOOTED RULE IS BOUNDED: "UNRATED POOLS PROTOTYPES" IS A TENDENCY =====
# CLAUDE.md's two-corpus-surfaces block says "unrated pools PROTOTYPES, ladder pools
# SHIPPED BOTS". **VERIFIED FALSE AS A GUARANTEE, from one primary: v125 has 305 LADDER
# games and 880 UNRATED games in meta_join.** 305 rated games is proof it HELD THE SLOT
# — a prototype cannot play ladder — so a SHIPPED version played 880 unrated games, 74%
# of its archived record. ⇒ **THE FIXTURE DOES NOT DETERMINE THE TREE.**
# ⚠ BOUNDED, not voided: the objection stands wherever prototypes ARE pooled; what is
# dead is treating the SURFACE as PROOF of the tree. **An unrated cut naming a version
# checks `version_trees.tsv`, never infers from the fixture.**
#
# ⛔ ===== BEFORE YOU USE RESEARCH'S FIRE ORDER: ITS PAYOUTS ARE ~51 POINTS STALE =====
# Every band figure in the s43 fire order (16 admissible teams, 0033 at +18.93,
# LingLing40 at +16.84, Juusto at +21.07) is priced off a holder read of **1775 taken
# at 20:45Z**. We closed at **1724**. ⇒ **the quoted payouts are OVERSTATED and band
# MEMBERSHIP HAS CHANGED FOR JUUSTO — determined, not uncertain.** Verified live at wrap:
#     ours 1724 · BAND_HI = us+125 = 1849
#     Juusto LIVE (`fcode team search`) **1857** -> gap **+133** -> **OUTSIDE by 8**
# ⛔⛔ **AND THE TOOL BUILT TO ANSWER THIS GETS IT WRONG, IN THE ADMITTING DIRECTION:**
# `target_value --band` prices Juusto off a CACHED **1848** and reports **+124, INSIDE
# by 1, pays +21.50.** It would admit a target that is out. The side lane's flag used a
# stale **1883** and said OUTSIDE by 34 — also wrong, the other way.
# **Three ratings, three verdicts; only the live read governs.**
# ⇒ ⛔ **`LEG-juustopin` IS LOCKED AND AWAITING A RE-FIRE, AND AS OF THIS WRAP THAT
# RE-FIRE WOULD BE OFF-PROGRAMME BY THE TARGET GATE.** Re-derive from `fcode team
# search` on BOTH sides before firing — never from `target_value`'s cached opponent
# column. This is CLAUDE.md's own Leviathan worked example running its full course
# inside one session: flagged one point inside at ~04:30Z, closed outside.
# artefact most likely to be picked up cold, and `target_value` additionally prices
# opponents off a CACHED rating.
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

---

# s44 WRAP (2026-08-15T16:05:11Z) — WHAT IS IN FLIGHT AND WHAT WATCHES IT

## RUNNING RIGHT NOW
* **local: 8 corefill shards**, 58 unstarted rows, load ~11-15 (ceiling 11, so guard 3
  holds launches near-permanently — that is normal, 8 shards x 2 games ~= 1.8x on 10 cores,
  and **measured NOT to bias results**: within-shard high-vs-low load = **-0.38pp
  [-1.37,+0.62]** across 22 shards / 505k rows).
* **ws1 (10 workers)** and **ws2 (6 workers)** both alive. Fleet: 26 QUEUED, 3 CLAIMED.
* **`auto_gate.py --apply` loops every 600s** -> `scratchpad/auto_gate.log`.
  Kill switch: `touch scratchpad/AUTOGATE_STOP`.

## THE STOP RULE (Magnus s44, verbatim: "above 51% at 1000 and at 2700 n")
`TREND-FLOOR`: stop if the PREFIX share at n=1000 or n=2700 is < 51.0%. **Prefix, not
current share — the current share would be ~400 looks at a random walk.** Exemptions:
nulls (structural md5), ablation `le` bars, n<400. Catastrophe (CI hi < 45) still fires.
**`--apply` acts on LOCAL shards only**; remote is report-only — cancel remotely with
`orchestrate.sh cancel <host> <SHARD> "<reason>"` (needs `kill` first).
Stopped today: CATRND1 (4,621 rows), LNCHERLY (1,481).

## GUARDS ADDED TODAY — all driven to BOTH verdicts
* `tools/control_pin.py` — control-tree hash pin. **corefill guard 5 REFUSES to launch
  when the control moved.** `--pin` to re-record (deliberately, after re-basing —
  **never to silence it**). ⚠ LOCAL ONLY; remote rsync snapshots unverified against it.
* **corefill guard 6** — refuses any live row whose control is not the incumbent.
* `orchestrate.sh cancel` — the per-shard remote cancel that did not exist.
* `tools/rebase_arm.py` — 3-way rebase with declared-and-consumed checks.

## OPEN, IN PRIORITY ORDER
1. ⛔ **The v140-vs-v151 divergence above.** Magnus's call.
2. **6 rebased arms queued but never started**: F320SIEGELA, F321LAUNCH0, F322IDLEPEC,
   F323PAVEFIR, F324OSCK4, F325OSCK6 + F326SIEGEFU. All on the v140 base, bars registered.
3. ⚠ **F320 cannot deliver its dose** — the plank waives `LAUNCHER_RESERVE` but
   `_eco_spendable` still adds `SIEGE_HEAL_RESERVE_TI=16` under the same condition, so
   the bar is cost+16 not cost+0 against a sieged bank of 1-44 Ti. **It already nulled
   once for this.** `_v326siegefull` was built to fix it — **VERIFY the fix took before
   trusting it; I stopped that agent mid-flight.**
4. **F232SEALTEM on ws1 reads 44.52%** (prefix@1000 45.2) — below floor, needs a manual
   remote cancel.
5. `tools/stack.py` **ancestor trap**: it passes BASE as BOTH the merge seed AND the
   ancestor (`:97`), so any arm forked before v223 merges as though the chassis delta
   were a deletion. **Correct today only by luck.** A sentinel-survival guard was
   specified and NOT built.
6. `claim_check.py` fires on `control_pin.py` — selftest run, **record not written**.
7. **`FIXTURE_OF_RECORD: live_unrated` at 0% for the second session running.**

## THE WAKE PATH — READ THIS
**Monitors that survive this session:** the four watchers + keeper, `gate_watch` (600s),
**`auto_gate --apply` (600s)**, corefill (deadline 12h from 15:40Z), both remote workers.
**Nothing wakes a human.** `auto_gate` stops local shards automatically; **remote shards
below the floor will run to 5400 unless someone cancels them by hand.**
⛔ **AND "AGENT COMPLETED" IS NOT "AGENT STOPPED"** — one subagent ran 92 minutes past its
completion notification, survived `pkill` and `TaskStop`, and committed on top of a
revert. **Check `ps` for live children before believing a notification.**

## INHERITED FROM THE SIDE LANE AT ITS WRAP (2026-08-15T16:06:17Z) — both now BUILDER-owned
8. **`prereg_check --fire` runs on ZERO firing paths.** OB13, OB17 and the
   METRIC_WINDOW checks bind **only** behind that flag, so **its entire coverage today
   was one person typing it at certification.** Not "untested" — *unreached*. Same class
   as the control-pin md5 that nothing consumed, and as `auto_gate` sitting inert until
   14:0xZ. **Wire it into the firing path or the checks are decoration.**
9. **Nothing measures LOCAL TLE under contention.** `cpu_watch` reads archived
   **PLATFORM** replays (it reported `worst our-max 8847µs — OK` all session, about a
   different machine); local replays carry **no exec fields at all**; `corefill` is
   **guarded at launch, unguarded in flight** (`worker.sh:277` holds mid-shard, corefill
   has no equivalent). ⇒ **Not urgent — measured today at −0.38pp [−1.37,+0.62] within-shard
   across 22 shards / 505k rows, so contention is not demonstrably biasing us.** But it is
   **the first thing to check if a LOCAL and a REMOTE read ever disagree on the same plank.**

## ⚠ HOLDER READ — TWO LANES DISAGREED AT WRAP, AND THE STALE ONE LOOKED HEALTHY
Side lane wrapped reporting **"holder v140 at 1720, rank #23"**; `fcode status` at
16:05:47Z reads **v151, 1707, Emerald, #23 of 126**. **Both were right when taken.**
The side lane read `corpus/ship_watch.log`'s newest row (15:52:33Z, `v140 … RULE=held`)
and **x3r0 activated v151 at ~15:54** — so the monitor line predates the change by two
minutes. ⇒ **`ship_watch` will keep naming v140 as the thing it is guarding until it
re-polls, and its RULE/SPRT columns are computed for a version that no longer holds the
slot.** The row carries `tape_age_min` so it is not blind — **but a two-minute-old row and
a live one are byte-identical apart from that field.** Read `fcode status` for the holder;
use `ship_watch` for the trend.
