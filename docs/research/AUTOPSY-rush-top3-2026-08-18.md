# RUSH AUTOPSY — the three biggest issues, ranked by attributable cost (s51, 2026-08-18)

*Banked by the builder s51 from the opus autopsy agent (Magnus directive: "figure out the three
biggest issues in our rush"). Fixture: fresh 30-game instrumented v515-fired grid WITH replays
(+ a second 30-game MAGTRACE grid), vs `_v488beltbreak2`; 0 tracebacks; every rate n=30 one-draw
unless cross-checked against the powered n=630 tape (which it is, and agrees where it matters:
median kill round 222 vs 223.5). Seven instrument guards all driven both ways, incl. a
core-HP-identity guard that FAILED first (diagnosing real overshoot semantics) and a classifier
guarded on two documented prior-session games + a mutation. Artifacts:
`scratchpad/s51_rush_autopsy/` (17MB: replays, per-round tapes, ledgers, classifiers).*

## THE ORGANISING FACT
**Every point of core damage in all 60 games, both directions, is sentinel damage** (UpdateHp
ledger: −18 only; zero gunner −7, zero peck −2 on any core). The rush IS one forward sentinel,
its funding, and its lifetime; everything else is logistics. **And in 11 of the 12 failed
sieges the defender's heal-back was EXACTLY 100.0% of everything we landed** (12,650 dealt /
12,650 healed). One sentinel's ceiling is 9.0 HP/round; measured enemy heal rates run
0.00-9.21. That comparison is the whole game. Won-game carrier: "kill before the healers
organise" (9/10 kills faced heal ≤3.48; funded-share 0.72 in kills vs 0.40 in non-kills).
⚠ Firing EARLIER is not the carrier — failed sieges open sooner (r82 vs r111): fire below the
heal rate feeds the healer and warns the defender.

## TOP 3 BY FLIP CEILING (offence-axis classes: KILLED 10 · NO_TURRET 7 · HEAL_OUTRUN 7 · MAG_STARVED 6)

### #1 — THE SIEGE MAGAZINE IS VISION-GATED AND UNARMED UNDER A LIVE, FIRING TURRET (+6/30 ceiling)
The Core arms the 300-ammo siege magazine only in phases SEALED/KILL (`main.py:503`), and the
phase is computed from `_fs_live_sentinels` (`siege.py:2585`) — **the raider's builder-vision
(r²=20) count**. With a sentinel of ours demonstrably hitting their core, no living builder of
ours is within vision in **63.4% of 6,094 rounds** (whole-map control: 0.0% — decode sound).
Joined to MAGTRACE: magazine armed 21.2% of core-hitting-sentinel rounds; ammo <10 in 78.3%;
**median ammo 5 with a turret firing vs 20 with nothing to shoot**. Phase ledger: RING
(unarmed) 64.5% · KILL_OPEN (excluded) 11.9% — the v515 report's "magazine/phase gap" was the
11.9%, not the 64.5%. Exemplar: midgard_s1_A bank pinned at exactly 80 Ti for 57 rounds, ammo
4, enemy core 500→158, turret died with 80 unspent. Ceiling honestly bounded: all 6
MAG_STARVED games clear at funded 9.0 vs their measured heals — +6/30 kills (+20pp), biased
optimistic 3 named ways. Fix shape: team-global sentinel accounting (published at build on a
store slot), not any unit's vision.

### #2 — 7/30 GAMES NEVER BUY A FORWARD SENTINEL AT ALL (+2-3)
`FS SENTINEL` fires 0× while `FS ARRIVE` fires 1-8×. Three gates compose; the geometric one:
`_fs_try_sentinel` scores only the 4 tiles adjacent to the raider's current tile
(`siege.py:2828`), minus ring tiles (OFFRING), veto, and can_fire_from — the raider lives ON
the ring, so its own hand excludes its candidates. atoll_s1_A: bank 90-116, gate open at r180,
7 sentinels built, 0 forward, r1000 loss. Same reach-class defect as the evictor (v515
surprise 5) — purchase-side this time.

### #3 — EXACTLY ONE SIEGE SENTINEL, EVER, VS HEALS AT UP TO 9.21 HP/ROUND (+2-3, requires survivability too)
0 concurrent core-hitting sentinels in 6,094 rounds despite FS_SENTINEL_MAX=2. HEAL_OUTRUN's
seven games had FUNDED turrets (0.93-1.00) netting 0.00 in six — not fixable by #1. The second
sentinel is arithmetically unreachable: it prices at **≈124 Ti at live scale**, the rebuy gate
demands ≈152, the median bank under a standing sentinel is **15 Ti**. midgard sentinel median
life 15 rounds (vs glacierkeep 236) — midgard-B is a scripted loss (two seeds, byte-different
replays, identical outcomes).

## ⛔⛔ THE SHARED ROOT — MAGNUS'S TEARDOWN RULE NEVER FIRES IN PRODUCTION
Build accounting, 30 games: **launchers are the largest line item — 295 built (9.8/game),
24,371 Ti, 29.3% of all spend, 2.8× the entire sentinel budget — with 224 HOPBUILDs against
217 THROWs: ONE throw each, then they stand forever. 29,674 launcher life-rounds, 0 shots.**
The probe's relay tears a launcher down after BOTH riders pass (Magnus's rule) and refunds the
+10% scale — engine-confirmed 190↔200 in the probe. **The fired config has ONE rider (crew
off), the both-riders condition never satisfies, teardown never fires**, and the standing
lattice adds +0.98 scale/game — which is exactly what prices the sentinel at 124, pushes the
magazine floor (128) and rebuy floor (152) past a 15-Ti bank, and starves #1 and #3.
Ammunition: 68.0% of all converted ammo was spent by turrets that never touched the enemy core
(NOT a recommendation to disable home turrets — s30 measured that a real negative; it is a
sizing fact).

## HEAL ECONOMICS (the strategic frame — connects to Magnus's gunner-cripple instinct)
Heal is 4 HP/Ti; sentinel damage is 1.8 dmg/Ti — the defender out-exchanges us >2:1 at equal
income. Out-DPSing an organised healer is economically losing; the three winning shapes are
(a) kill before healers organise (the current carrier), (b) overwhelm briefly with 2× DPS
(needs #3 + survivability), (c) **cut the income that pays for heals — the gunner-cripple
plank as the sentinel's ENABLER, not its rival** (GUNNER-FIRST/MODESWITCH, already queued).

## Powered-tape cross-checks
33% of our 272 powered kills land after r300 (the starved-grind tail #1 predicts). v515's
unattributed regressions are DEATH-RATE rises (glacierkeep deaths 7.1→15.9%, nordkap
34.9→42.9%). midgard powered: 22.2% kills / 72.2% deaths.

## Builder routing (s51): v516 = the tight high-ceiling set
1. **RELAY TEARDOWN for single-rider chains** (the shared root; probe semantics restored:
   rider passed ⇒ teardown ⇒ scale refund; verify scale trace flattens and sentinel price
   drops from ~124).
2. **Team-global sentinel accounting** for the phase/magazine (store-slot published at build;
   kills the 63.4% vision blindness).
3. **Sentinel-purchase reach** (same fix class as v515's evictor reach, purchase-side).
Deferred to v517+: fire-discipline (hold-until-net-positive), second-sentinel economics,
GUNNER-FIRST + MODESWITCH stacking. Each with mutants; n≥450 concurrent-block headline.

---
*⛔ DATED CORRECTION (s51, v516 build, same session): the SHARED-ROOT section's sizing is
WRONG. Re-measured against the same replays with a tile+round join: 219/224 hop links tear
down within 20 rounds (median life 1) — the fired config's single-rider throw IS the teardown
trigger (relay=False ⇒ hold=False). The long-lived launchers are ring evictors (standing is
their job) + the chassis home-launcher line; the real defect was a small one (fs_ferry_seen
gate above the TTL, fixed in v516) worth ~7pp of scale share, and the sentinel priced at ~86
(not 124) at purchase time, with LIVE BUILDER BOTS (~100pp of the 188pp scale excess) the
dominant term, launchers ~4%. The #1 magazine finding STANDS (v516 mutant reproduces its
digits exactly); the launcher-budget framing does not. See
BUILD-REPORT-v516teardown-2026-08-18.md finding 1.*
