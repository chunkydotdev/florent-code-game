# Eir 6 lineage production-read spec (PRE-REGISTRATION, rev 3 → Eir 6e)

**Rev 3, ~21:00: target is now Eir 6e = `bots/_v81e6e` = Eir 6c + piece N**
(one-line `is_in_vision` guard on the pave block's `is_tile_empty(pave_prev)`
— the ancestral launcher-teleport crash bug, measured 0/120 our side vs
22/120 v68's after the fix). 480 slot bar vs opp_v68 running at rev time
(N's 120-leg read: 55.0 [46.1,63.6] vs parent 6c's 46.0). ALL rev-2 checks
below apply unchanged (6e carries 6c's pieces: K'' budgeted trunk repair,
pop floor, 5.1 core-heal semantics, restored I/J/H). ONE CHECK ADDED:

0. **Crash-fix verification (piece N, the ship's actual content)**: in
   production replays where ANY launcher is present (either team), zero
   pave-block GameError diagnostic prints from our units. Baseline: the
   inherited bug affects ~0.1-0.2 units/game on launcher maps; post-fix
   arena measured 0/120. Any recurrence = the guard missed a path.

**Rev 2, 2026-08-07 ~19:38: target is now Eir 6c** after Eir 6b FAILED gate
stage 1 (tape 19:28) and the ablation grid pinned the mechanism (tape
`_v78e6b-ablation`, verified against the tape by this arm): the budget CAP on
siege core-heal was the drag, singular — capped core arm alone reproduces the
band crater (notrunk 56.7), exempting the core restores it (coreexempt band
95.0 [86.3,98.3]); trunk arm exonerated, hint-positive vs rush. K'' =
coreexempt shape, promoted to `bots/_v79e6c` (md5 8aaa91e6..., ast-proven
identical to the measured cell), full gate in progress. Checks below revised
accordingly; original 19:20 pre-registration (written before the 6b worker
landed) preserved in git history.

Version tags (rule 2): our live version at rev 2 was **v67 "wave_ghost"**;
STALENESS FIX ~19:58: live is now **v68 "chokewall"** (x3r0 upload,
auto-activated 19:12 mid-gate; first read commissioned, registry row 19:58) —
6c's stage-2 slot bar is rebased to opp_v68 (clear 50), and if 6c ships, the
"slot context" references below mean v68, not v67. No bot dirs code-read for
this spec —
sources are coordination notes 18:46/19:14/19:16/19:31/19:35, tape rows
`_v78e6b`/`_v78e6b-ablation`/`_v77e6_flooronly` (read directly), and prior
deliverables (v65-production-read, v66-salvage-cad-leg, k-drag-diagnosis
corrected, wave-ghost-first-read, all 2026-08-07). Numbers below are those
sources' measured baselines, not fresh measurements.

## Lineage (what shipping Eir 6c restores and adds)

`_v79e6c` = Eir 5.1 lineage + **K'' budgeted proactive trunk repair** (core
heal reverts to verbatim 5.1 siege semantics — NO cap) + isolation-verified
pop floor + sporks ammo OFF. Because it is our lineage (not the v67 fork), it
RESTORES: I (rotation latch), J (defender counterbattery), H (r960 endgame
switch + v66 dump cap).

## Per-piece production checks

1. **Core heal ≡ 5.1 semantics (NULL check — K'' must NOT change this).** The
   6b lesson on the record: core defense must never be budget-capped in our mix
   (builders budget-dry by r10-27 under rush = the band crater). PASS: core-heal
   distribution/timing indistinguishable from the 5.1 baseline — siege-gated,
   unbounded while under fire. FAIL either direction: capping artifacts (heals
   stopping mid-siege with Ti available), OR regression to the v1 anti-pattern
   (un-gated core-heal from r0, 27-31% of builder turns in fast band losses).
2. **K'' trunk repair — the live novel piece.** Budgeted proactive heals on
   damaged structures OUTSIDE SLOT_UNDER siege windows (replaces v1's dead ≥8
   depth gate). Ablation evidence: exonerated and hint-positive vs rush with
   the trunk arm owning the ledger alone (band 95.0). PASS: trunk-repair events
   present on damaged conveyors in class-relevant matches, budget cap binding
   without starving builder actions. FAIL: repair turns crowding out
   build/attack actions in matched rounds (opportunity-cost check vs baseline).
3. **Pop floor signature.** Isolation evidence: orizon leg 71.7 [59.2,81.5] vs
   baseline 58.3 [45.7,69.9]; konly measured 46.7 on the same leg — floor and K
   moved in OPPOSITE directions on the family instrument. PASS: builder count
   sustained under point-blank pressure; the ~r235-250 zero-population windows
   (konly-era signature) get refilled. Also verify the floor is not expressing as
   harvester-spam runaway (H's builder arm interplay, check 5).
4. **I latch (restored).** PASS: 0 fast rotation flips; known trigger is the
   nordkap chase_battery config (v65 bug: 166 rotations / 50 oscillations /
   1,660 Ti burned). v66 verified the latch under losing pressure — re-confirm
   on the new base.
5. **H + dump cap (carried, twice unverified).** On the first r1000 game: the
   capped dump fires (cap = turrets × rounds-left × shot-cost × 1.5) AND banked
   Ti survives for tiebreak #3 (v65's uncapped 14,634-Ti dump zeroed it; v66
   died at 39 min without an r1000 game; v67 dropped H entirely). Natural
   experiment: OopsGotYourElo is H's designed prey (60% r1000-committed) and we
   have a v67-era 2-3 loss on record (ba007b91) — a restored-H OGE pairing is
   the cleanest read.
6. **J counterbattery (restored).** v65 production distribution was 1/7/11/4/0
   vs baseline exactly-1; positive signature includes r69-class core kills vs
   thin-house battery teams. Check the distribution shape, not exact counts.
7. **Floor-vs-trunk-repair attribution split.** Count trunk-repair heals (K'')
   and rebuild/spawn actions (floor) separately per game. Healthy: floor
   rebuilds under pressure WITHOUT heal monopolization of builder turns (the
   972-heal starvation game is the anti-pattern). This split is what keeps a
   bad K'' from hiding behind a good floor — floor and the original K moved
   opposite on orizon, so production must attribute them separately.
8. **Post-ship constants re-extraction (standing rule).** Deterministic
   opponents re-seed on OUR version: Ouroboros first-gunner rows and CAD opening
   tiles must be re-extracted under the new version before any denial use. All
   v66/v67-era exact-tile rows are presumptively stale the moment Eir 6b
   activates.

## Data plan

Archive-first via the --mine pass (research monitor already watching the 6
recent our-match IDs land); direct downloads only with a declared paced budget.
Class priority for the first replays: point-blank family pairings
(Orizon/Team 48/team lazy/Leviathan — the floor's design class), then
band-class, then OGE (check 5), then any r1000 game (dump cap). Checks 1-2
read from any loss; checks 3/6 need class-relevant opponents.

## Contingency on record (from the ablation's honesty flag)

koff purity control's v63 leg came in 46.7 vs flooronly's 60.0 — overlapping,
filed as n=60 noise (v63 legs carry ~±12 at that n; band control was clean at
91.7). If Eir 6c's fresh gate v63 leg ALSO lands low, that reopens the
question and the contingent decode ASK becomes a **v63-specific** read (why
does the K-line base underperform flooronly on the peer mirror), not the band
census. Both decode shapes are pre-thought; the band census spec lives in the
19:33-era ping and applies to either with the target leg swapped.

## REV 4 (2026-08-08 ~06:2x, research arm) — retargeted to _v84g "graft" (6e + E2b + E1-capped + S1 guard), pre-staged BEFORE the 480 bar lands

Fires on _v84g activating (ship rule or Magnus's field-better/holder-parity
route). Rev 3's checks 1-8 stand for the 6e base; ADD:

9. **E2b in production**: our conveyors-on-ore count = 0 across all archived
   matches (local A/B was 0/1,595 vs control 163; any nonzero = gate/hoist
   regression on unknown maps — check map-decode status per instance).
10. **E1-capped in production**: zero sub-floor peacetime conversions AND no
   ammo starvation under the cap (builder's ablation flag: scaled-to-149
   variant capped; watch turret idle-with-target rounds vs the v69-era
   baseline 0/1,190).
11. **S1 guard**: own-building attack count = 0 (v69-line baseline: 11% of
   melee swings; ours pre-guard measured via _intercept path). Any own-team
   target in a fire() event = guard miss, cite round + chased-raider context.
12. **Bleed-plank baselines for the NEXT worker** (heal-seat/population —
   measure even though _v84g does NOT fix these): (a) heal-seats blocked at
   every core-damage episode (our known habit: median 4/8, p90 8/8); (b)
   spawn total vs the soft ceiling (~cap+8+surge) in any attrition game;
   (c) heal/dmg ratio per siege episode vs the bimodal law (≥0.94 lives,
   ≤0.86 dies) — production replication of the two-arm finding.
13. **Class priority for first replays** (reweighted to the v72 bleed list):
   CAD v117 / kladde v75-76 / Lunds v45 / Ouroboros / Leviathan v25 first,
   then the rev-3 order. The candidate's case IS the bleed classes — the
   read's job is confirming the planks fire against exactly them.

Constants re-extraction (check 8) now triple-due: our-version change AND the
family churn wave (CAD v117, Lunds v45-46?, kladde v75-76 thrash) AND the M1
throw-destination unfreeze from the CAD-arm read.
