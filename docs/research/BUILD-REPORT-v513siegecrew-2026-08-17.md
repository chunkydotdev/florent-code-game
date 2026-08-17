# BUILD REPORT — `bots/_v513siegecrew` (autopsy-driven: door response, belt, magazine, salt gate), s50 2026-08-17

*Banked by the builder s50 from the opus build agent. The largest iteration of the day: eight
changes folding Magnus's two direct rules and every ranked defect in
`AUTOPSY-v512-three-maps-2026-08-17.md`. Parent `_v512ringladder` (frozen, untouched); master
flag `LOKI_FS_CREW` @ doctrine.py:2594, False reproduces the parent. Diff vs parent: doctrine
+263, siege +383, main +309/-15, eco +58/-4, raid untouched. 0 tracebacks in 670 grid games + 165 mechanism/demo games.*

## HEADLINE — 5 maps × 6 reps × 3 pooled blocks = n=90/arm, paired seeds, vs `_v488beltbreak2`, local `--tle 10`, FIRED config (FS_LOG/FS_DRAW off)

| | **v513 (ship)** | v512 parent |
|---|---|---|
| WINS | **49/90 (54.4%)** | 13/90 (14.4%) |
| our core-kills | **41** | 13 |
| **kills ≤ r300 (ITT, the DEFENCE_ADMISSION_BAR primary)** | **24/90 (26.7%)** | 8/90 (8.9%) |
| our core destroyed | **39/90 (43.3%)** | 68/90 (75.6%) |
| r1000 (programme defeats) | 10/90 | 9/90 |
| **`titanium_collected` = 0** | **4/90 (4.4%)** | 46/90 (51.1%) |
| median titanium collected | **565** | 0 |
| median kill round | 281 | 241 |
| tracebacks | 0 | 0 |

Per block (5 maps × 6 reps each, independent seed sets): **15 · 17 · 17 wins**, k≤300 **11 · 6
· 7**, tic-zero **1 · 1 · 2** — the direction is the same in all three.

**The timely-kill rate ROSE 8.9% → 26.7%**, so the kill-round bar is cleared on its primary
(ITT) form, and the median kill round stays under 300. ⚠ The median kill round did rise
(241 → 281) and it is **collider-conditioned**: v513 has three times as many kills, so its
median includes kills v512 simply never got. Blocks straddle it (214 / 414 / 291), so the
median is not stable at this n either.

## THE EIGHT CHANGES — files:lines, and what each one is answering

| | change | where | autopsy defect |
|---|---|---|---|
| A | **sentinel + magazine only AFTER the salt** | `siege.py:1936` `_fs_salt_ok`, gate in `_fs_sentinel_ok:1966`; core side `main.py:478` (arming) | #3 (fire is 1:1 heal-cancelled pre-seal) |
| B | **door-turret response** | `main.py:1030` `_door_turret`, `:1085` `_door_turret_turn`, hook `:1014` | **#1** (0 of 40 attacked) |
| C | **belt last link + eco lifeline** | `eco.py:371` `_eco_spendable(essential=)`, `:997` `_build_next_link`, `:1093` `_l4_repair` | #2 (tic=0 ⟺ no core-adjacent link) |
| D | **second body (support raider)** | `siege.py:1192` `_fs_supp_turn`, `:1250` `_fs_supp_walk`; roster `main.py:832`, appointment `:981` | #6/#9 (coverage, one-body contention) |
| E | **rung-2 seal-wait exemption** | `siege.py:1478-1520` (`_fs_try_evict_launcher` support gate) | #8 (0 evictions in 19/24) |
| F | **the magazine, traced** | `main.py:519-560` (KILL floor), `:656` (`amt >= 1`) | #4 (73.9% of live-sentinel rounds dry) |
| G | **replacement on dedicated bits + dodge rework** | `siege.py:191/205` crew beats, `:223` `_raid_seat_take`, `:899` `_fs_hit_mark`, `:1298` `_fs_try_retreat`, veto in `_fs_stand_target:1490` | #5 (23 deaths, dodge saved 0) |
| H | **purposeful spawns** | `main.py:743` (spawn sort), `:775` `_spawn_ore_anchor` | Magnus, polish |

## ⭐ ENGINE FACT, PROBED AND DRIVEN BOTH WAYS — **A STORE SLOT IS AN UNSIGNED 32-BIT INTEGER**
`scratchpad/v513_build/probe_store`, one local game, six values: `2**30|12345` and
`2**31|999` **round-trip exactly**; `2**40`, `2**62`, `2**63-1` and **`-5`** all raise
`OverflowError: out of range integral type conversion attempted`. So the usable range is
`0 .. 2**32-1`, **a negative write RAISES**, and an uncaught OverflowError destroys the unit
for the rest of the match. This is what made G's fix possible: `SLOT_RAID_N`'s counter tops out
at LOKI_MAX_BUILDERS = 11 and uses 4 of its 32 bits, so the crew's two heartbeats now live in
bits 8-29 as **absolute** round numbers (MAX_TURNS 1000 < 2047) — no modular-wrap window in
which a dead body reads as alive. **ROUTE TO ATLAS at wrap.**

## PER-CHANGE VERIFICATION — every guard driven both ways
Mechanism arms: 5 maps × 3 reps = 15 games each, logging build, ship flag set.
⛔ **THE NOISE FLOOR IS MEASURED, NOT ASSUMED: `FS_CREW_EVICT_NOWAIT=False` is INERT in the ship
config (its only consumer is the support body, which is off) and it still moved the evictor
count 9 → 5.** So on these counters **only zero-vs-nonzero contrasts are readable**; ratios are
not. That mutant is this table's placebo.

| claim | ON | mutant OFF | verdict |
|---|---|---|---|
| A: no sentinel before the salt | **0** pre-seal sentinels | `salt_off` **14**, `crewflag_off` **10** | ✅ |
| B: door turrets are attacked | **152** pecks (n=15); 11/30 games have one (logged n=30) | `door_off` **0**, `crewflag_off` **0** | ✅ (v512 baseline: 0 of 40) |
| C: the belt reaches the core | tic=0 in **1/15** | `belt_off` **5/15**, `crewflag_off` **9/15** | ✅ |
| F: magazine | **0 of 32** live-sentinel STAT rounds under one shot (**0.0%**) | v512 autopsy: **73.9%** | ✅ |
| G: prestand veto | 54 dodges | `prestand_off` **160** | ✅ direction |
| G: HP-floor retreat | 4 retreats | `retreat_off` **0** | ✅ |
| D: crew | 0 promotions | `crew_var` **39** | ✅ mechanism present |
| ladder priority inversions | **0 of 804 logged rung firings** (in-bot `_fs_rung` falsifier) | — | ✅ |
| tracebacks | **0** across every arm (670 grid + 165 mechanism/demo games) | — | ✅ |

**Flag-off spot-check.** Byte-identical outcome comparison is IMPOSSIBLE here — NOISE_ON seeds
an unseeded spawn salt, so a local game is one draw (s50 one-draw law). Verified two ways
instead: (1) **structurally** — every new branch is behind `LOKI_FS_CREW`, and with it False
`_eco_spendable`, `_l4_repair`, `_build_next_link`, `_fs_stand_target`, `_fs_threat_tiles`,
`_fs_try_retreat`, `_fs_salt_ok`, `_fs_try_evict_launcher`, `_raid_seat_take` and every core
clause reduce to the parent's expressions; (2) **behaviourally**, n=60 paired on the parent's
own seeds: flag-off 12 wins / 44 core deaths / 27 tic-zero against v512's 9 / 46 / 30 — inside
the documented same-bot swing.

## ⛔⛔ DEVIATION 1, AND IT IS THE BIG ONE: **THE SECOND BODY SHIPS OFF (`FS_CREW_ON = False`)**
Built exactly as specified, measured, and it **LOST on every column** — same fixture, same
seeds, fired config:

| arm (n=90/arm, 3 blocks) | wins | kills | ≤r300 | our core died | tic=0 | median collected |
|---|---|---|---|---|---|---|
| `FS_CREW_ON = False` (ships) | **49 (54.4%)** | **41** | **24** | **39** | **4** | **565** |
| `FS_CREW_ON = True` (spec default) | 35 (38.9%) | 29 | 12 | 48 | 12 | 380 |

Per-block wins, ship vs crew-on: **15 v 11 · 17 v 13 · 17 v 11** — the direction repeats in
all three blocks.
⭐ **AND THE OBVIOUS MECHANISM WAS TESTED AND ACQUITTED.** First suspicion: the support's BODY
DENIAL publishes `FS_PH_SEALED` while it merely stands on a seat, arming the 300-ammunition
target on an unbarriered collar. Run with `FS_CREW_DENY_SEAT=False` (support never occupies a
seat, everything else identical, n=60): **24 wins / 20 kills / 31 core deaths — indistinguishable
from the full crew.** It is not the denial; it is the second body. The likeliest remaining
reading is the one these games cannot prove: a fourth opening builder and its launcher are
bought out of the same bank the collar, the belt and the sentinel come out of, and the economy
column moves with it (median collected 380 with the crew, 640 without).
⚠ 15.6pp at n=90/arm is around the edge of the 95% interval (half-width ≈14.5pp at this base
rate, local DEFF ≈ 0.98) — a DIRECTION on every column, not a significance claim. **The code
stays behind the flag** with E's funding exemption (inert while D is off), for a fixture that
could reverse it.

## ⛔ THE SENTINEL STALL, MEASURED AS MAGNUS ASKED
Magnus's rule ships strict. The stall it was warned about is **real but no longer fatal**:
**a sentinel is bought in 8 of 30 logged ship-config games (27%)**, because closure and
affordability are separate events — glacierkeep seed 7301 closed the collar at r180 holding 44
titanium (a few short), the grace expired, one seat re-opened, and at r800 the bot stood on
`orth 1` with **110 titanium and 300 ammunition and no turret**. The flagged-off fallback is
built and measured: `FS_SALT_LATCH = True` (gate becomes "the collar HAS BEEN complete")
scored **8 wins / 15 against the strict rule's 9 / 15 — no gain**, so the strict rule ships and
the variant stays off. **The kill now mostly comes from elsewhere**: 40 core-kills at n=90 with
a sentinel in ~a quarter of games says the collar plus the economy plus the home defence are
carrying it.

## Other deviations
* **`FS_RETREAT_HEAL_HP` was cut.** The first form ("retreat and wait to heal") is a treadmill —
  nothing heals a body at the enemy ring, so it walked out of `FS_RING_HOLD_DSQ`, the turn
  dropped to the FERRY branch, the ferry threw it back, and the phase log read `1,2,1,2` for
  four hundred rounds (glacierkeep seed 7301, caught on the first smoke run). What ships is ONE
  step off a COVERED tile while low, only when a strictly-safer neighbour exists inside the ring.
* **The prestand blacklist is a veto with a fallback, not an absolute veto** — an absolute one
  refuses the only station beside the last seat and stops the collar dead, which is the exact
  state the measured nordkap death-loop was in (`need 1`, bank open).
* **H ships ON but cannot be shown not to regress at this n**: spawn-purpose-off scored 52/90
  against 48/90, and the per-block direction straddles (18 v 17 · 13 v 21 · 17 v 14). No stable
  effect either way; the mechanism (a re-sort of the same `can_spawn`-filtered candidate list)
  is verified.
* **`convert_ammo`'s minimum drops from 4 to 1 while the siege is live** (the 4-titanium floor
  blocked 19% of conversion rounds on the diagnostic's instrumented atoll game).

## Surprises (verbatim where they came from a measurement)
1. ⛔⛔ **`titanium_collected` = 0 WAS A DEADLOCK BETWEEN TWO OF OUR OWN RESERVES, NEITHER OF
   WHICH HAD EVER BEEN CHECKED AGAINST THE OTHER.** `_eco_spendable` withholds `8×barrier + 6`
   from the economy; the KILL-phase magazine drains the bank to `8×barrier`. **The economy's bar
   sat EXACTLY 6 titanium above the level the core drained to, permanently.** 2,653 of 2,809
   eco-spend denials (94.4%) had a raw bank that covered the cost; glacierkeep_g5 printed
   `ti=56 res=62 cost=7` **1,284 times** and delivered nothing in 447 rounds. The parent's
   comments reason at length about "two reserves that can meet on the same bank deadlock" and
   check the core's floor against `_fs_seal_ok` — **they never check it against the ECONOMY's.**
2. ⭐ **THE SIEGE PHASE ARRIVES IN THE OPENING, NOT THE MIDGAME**: FS_PH_RING first seen r6-12
   and FS_PH_KILL **r8-14**. Every clause in that block is commented as if it governs a
   mid-siege bank; it governs the belt.
3. ⛔ **THE MAGAZINE LOCK IS A SHAPE, NOT A CONSTANT — WHICH IS WHY TWO RE-TUNES FAILED.**
   `convert_ammo` is the only consumer of surplus in that state, so **the bank equilibrates to
   exactly `ti_floor` and stays there**: measured median bank across all 24 autopsy games = 48.0
   = `8 × barrier` at the modal live scale, and `ti > ti_floor` was False in 74-84% of KILL
   rounds on three instrumented re-runs. Any constant reproduces it.
4. ⛔ **THE OLD DODGE DID NOT MERELY FAIL — IT CANNIBALISED THE SEAL.** nordkap trace: DODGE
   (10,9)→(10,8) at r200, 203, 205, 207, 209, 213 with the walker putting the body back between
   every one; HP 40→33→26→8→1; **25 dodge-rounds against 3 productive ones in 65**, at `need 1`
   with the bank open. The blacklist existed but was a **sort key, not a veto**.
5. ⭐ **A SENTINEL RAY IS PERMANENT INFORMATION AND WE THREW IT AWAY EVERY 5 ROUNDS.** Sentinels
   cannot rotate (only gunners can), 22 of 23 fatal tiles were on a previously-seen ray of the
   turret that fired, and 20 of 23 deaths were on a tile the body had LEFT and walked back onto.
6. ⛔ **REPLACEMENT: WE FIXED THE COVERAGE AND MADE THE LATENCY WORSE.** Forced-death test
   (raider self-destructs at r60, 4 reps × 5 maps, both trees instrumented identically):
   **v513 replaces in 10 of 14 (71%), median 90 rounds, 0 within 15**; **v512 replaces in 8 of
   16 (50%), median 13 rounds, 5 within 15.** The dedicated bits do what they were for — the
   successor door no longer stays shut while a chassis raider holds the ring — but the binding
   constraint turns out to be **funding a new body (60-100 Ti at live scale plus a 60 Ti spawn
   reserve)**, not noticing the death. **Magnus's ~15-round cap is NOT met.** The cheap fix
   (convert a live eco builder) is exactly what deviation 1 measured as costing 14pp, so it is
   NOT applied blind — it is the top open item.

## Demos (local, gitignored)
* **`demos/DEMO-drakkarfjord-siegecrew-FASTKILL.replay26`** — best end-to-end: ferry lands r11,
  eight orthogonals sealed by r35, `FS_PH_SEALED` r82, **sentinel bought r85 (post-salt, the rule
  visible in the log), WIN by core kill r125.**
* **`demos/DEMO-glacierkeep-siegecrew-DOORKILL.replay26`** — the door response, legibly: **three
  home builders (ids 8, 16, 5) converge on the same enemy turret at (15,8) from r31 to r44** —
  the two-pecker convergence — while the raider seals; `orth 0` by r60, sentinel up by r140,
  **WIN by core kill r204.**

## Open items
1. **Replacement latency (median 90 rounds).** Needs a funding answer, not a detection one.
2. **The sentinel stall (a turret in 27% of games).** Strict gate is Magnus's; the latch variant
   is built, measured at no gain, and off.
3. **CPU is still unmeasured locally** (`get_cpu_time_elapsed` is a stub). v513 adds a per-round
   `get_nearby_buildings` + `can_fire_from` scan for home builders (change B) and set operations
   in the stand-tile chooser — a platform `match test` is required before any ship.
4. `FS_CREW_CONVERT` (the 3+convert opening variant) is built and **never measured** — it was
   made moot when the crew itself went off.
5. The residual belt defect the diagnostic found and this build did NOT fix: `_wire_tick`
   overwrites `link_queue` wholesale on each new harvester, orphaning dead heads. Shared with
   the control, so it is not the FS discriminator, but it is still there.
