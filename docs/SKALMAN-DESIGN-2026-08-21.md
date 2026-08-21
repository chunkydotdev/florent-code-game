# SKALMAN v1 — FOUNDING DESIGN (builder, s54)

**Written:** 2026-08-21T16:48:18Z (`date -u`, in-shell). **HEAD at write:** `d9975f611`.
**Authority chain:** Magnus's line directive (coordination tail ~15:5xZ, s53) → `PROGRAMME.md`
NEW LINE block (`NEXT_LINE: skalman`, doctrine `beancounters_replication_then_amplify`,
benchmark `bots/_v542wave` FROZEN) → `PLAYBOOK-beancounters-2026-08-21.md` §6 (the copy-spec)
→ the Magnus-ratified architecture note (HANDOVER s53 top block). This doc is the builder's
operational design; it binds the v1 build and ANSWERS the chassis questions the queue re-scope's
⚠ rows settle on. Research ratifies queue classifications against it.

## 1. ARCHITECTURE (ratified s53, restated operationally)

* **Player logic FROM SCRATCH, ~1.5k lines, per-verb attributable**: every doctrine verb lives
  behind its own module-level flag (`SK_ORE_DENY`, `SK_CAGE`, `SK_DRIP`, `SK_NEST`, `SK_DOOR`,
  `SK_BELT`, `SK_ROLES`) so ablation identities are one-flag cheap and every fidelity metric
  maps to exactly one flag. Tree: `bots/_v600skalman1/` (side-lane flag s54, verified:
  `_skalman_v1` matches no LINE_DIRS pattern and gate.py would refuse every battery on it —
  the s31/s46 defect class; `_v600skalman1` fnmatch-passes `_v[2-9]??*`, keeps the version
  convention, needs no PROGRAMME edit. Skalman iterations continue v600, v601, …).
* **Curated imports VERBATIM from `bots/_v542wave`** (boundaries per
  `SKALMAN-IMPORT-MANIFEST` when it lands): MAPTRUST/known_map_for (+F1/F2 insurance) ·
  bounds discipline · displacement guards (re-plan-from-actual-position) · the exception
  wrapper · store idioms · cardinal pathing. Anything the manifest marks NEEDS-CUT is cut at
  the marked line, REWRITE-ADVISED items are rewritten in the from-scratch half.
* **Benchmark discipline** (side-lane watch, acknowledged): iteration screens run vs the
  PREVIOUS Skalman iteration (v1 screens vs the four-verb ablation of itself); `_v542wave`
  is read ONLY for "has the new doctrine caught the old line". Bar-2 (53.3, anchor-upper)
  governs any ship; nothing here ships without Magnus.

## 2. PHASE-1 SCOPE — the nine COPYs, prioritised

Phase-1 verdicts are REPLICATION FIDELITY vs the study's mechanism numbers (instrument:
`tools/skalman_fidelity.py`, both-ways driven), NOT game share. Build order inside v1:

1. **CHASSIS = COPY 8**: four builders, r0-r3, fixed roles all game (HOME KEEPER / CAGE
   WALKER / ORE DENIER / SIEGE ENGINEER), never a fifth (target: 4 in ~93% of games,
   modal zero deaths). The two-bot column handoff (leader steps off, trailer builds same
   round) is in scope — it is ordering, not a feature.
2. **BELT = COPY part of chassis**: outward-in, ALWAYS terminated, planned globally (not
   per-harvester — the #78 defect). Fidelity target: harvester→core connectivity 83%
   (ours today: 58.8%).
3. **DRIP = COPY 7**: the exact spec as written (need-based, quantised to the shot).
   Acceptance: ≥97.3% of amounts on the 4/10 lattice, peak ≈26, first convert on
   first-turret round (median ~r27.5, NEVER r0), ~67 calls/game. Named floor per V10:
   keep `SK_AMMO_FLOOR` (default small, e.g. one sentinel shot) so a cost shock cannot
   cancel next round's shots.
4. **CAGE = COPY 9** (we ship the cage; copy the ORDER): nearest-EMPTY-first, barrier
   +1 round after clear, guns clear the ring and barriers follow (the v68 form), walk a
   lap not a shuttle, accept 7-of-8. Completion is the gap (12.0%→22.3% target).
5. **ORE DENIAL = COPY 1**: harvester-death→barrier-on-T (target 92.5% @ 1-round median)
   + the pre-emptive half (enemy-half unharvested ore, ~r66). PROGRAMME rider carried:
   argued as opens-the-lane, never as economy.
6. **NEST = COPY 5**: band-first (d²14-32 from enemy core footprint, diagonal-max d²=32
   preferred), barriers 1-4 rounds before the gun including inside the firing line.
   **Point-blank plants are OFF in v1** (the §6 dependency: no point-blank until
   ring-clearance measures at parity).
7. **RING CLEARANCE = COPY 6 + COPY 2**: the door verb — shoot what gets planted
   (target 61.9%), kill adjacent counter-turrets (target 87.2%), and site answers OFF
   the enemy sentinel's axis (the mirror of GUNAXIS). DOORWAVE's readout feeds this verb.
8. **BELT-GUN DEFENCE = COPY 4 defensive half + ledger V1**: a tile rebuilt N times
   (default 3) without surviving escalates to turret-location + removal, never rebuild #4.
9. **DISPLACEMENT = COPY 3 deferred** (n=1 loop, a leg not a plank — phase 2).

## 3. THE CHASSIS CALLS (what the ⚠ queue rows settle on)

* **Forward raiders: NO.** The rush raider class is sunset. Forward bodies in v1 are the
  CAGE WALKER, ORE DENIER and SIEGE ENGINEER — role-fixed, continuously acting, never a
  raid lifecycle. (Settles #2's raid-path premise → re-anchor on the cage-walker path;
  #30/#48 raid-station/parked-raider → no picker exists in v1; #39's raider-targeting-prior
  half → split off dead, the barrier half survives.)
* **Ferry: NO in v1.** Zero launchers in the phase-1 tree (Bean counters' shape; the
  fidelity instrument has no launcher metric). (Settles #103: the ferry registration
  dissolves for the Skalman tree — survives only as a v177-holder question.)
* **Raid-station picker: NO.** Fixed role destinations replace scoring. (Settles #30's
  vehicle; its enemy-sentinel-ray avoidance survives as an input to nest/walk siting.)
* **Dormant guard: NO.** (Settles #79 as written; the nest's staffing is the siege
  engineer, continuously acting.)
* **Launchers overall: phase 2.** The home-launcher holder-defence block (#105-108) is
  v177's business while it holds the slot, not the Skalman tree's. The V6 lesson is
  covered in v1 by the imported displacement guard (re-plan from actual position);
  counter-throw waits for amplify.
* **Kill chain: strangle-then-KILL** (Magnus's ruling verbatim: "We play to destroy their
  cores"). The cage/belt/nest are means. V9's "instead" column is in scope for v1: a
  stall detector — seal not advanced in N rounds AND forward turret lifetime < M ⇒
  switch doctrine branch (v1's plan B: shift the nest to the band's far quadrant and
  re-route the walker; crude is fine, absent is not).

## 4. THE VULNERABILITY LEDGER AS REQUIREMENTS (V1-V12 → build rules)

V1 rebuild-escalation (§2 item 8) · V2 seal closes BEHIND the walker; belt and seal
subroutines NEVER own the same tile (single tile-owner arbiter, the V8 fix, one map:
tile→owning verb) · V3 dead forward sentinel = immediate re-site decision with latency
budget (target < their median 33-42) · V4 per-tile death memory on turret siting (hygiene) ·
V5 denial verbs yield to survival/kill when core under fire · V6 imported displacement
guard · V7 target-HP-trend give-up rule (N rounds not trending down ⇒ retarget) · V9 stall
detector (§3) · V10 named ammo floor (§2.3) · V11 big-map branch is an EXPLICIT GAP in v1
— noted, not built; the fidelity readout stratifies by map size so the gap is measured ·
V12 the serial chain is accepted in v1 (BC's own shape); defended by V1's escalation rule.

## 5. WHAT v1 DOES NOT CONTAIN (so nobody greps for it)

No launchers · no ferry · no rush opening (`LOKI2_RUSH_ON` class) · no burst-bank funding
(v544 governor CANCELLED by PROGRAMME) · no point-blank sentinel plants · no crash/kidnap
toolbox (phase-2 amplify candidates, each behind its own prereg) · no CPU-denial anything
(refuted, do-not-copy) · no tiebreak-turtle branch (R1000_IS_DEFEAT).

## 6. ACCEPTANCE — what "founded" means for v1

1. `tools/skalman_fidelity.py` selftest green (both populations, both verdicts, per metric).
2. `bots/_skalman_v1` plays full local games without unit deaths by exception (the wrapper
   imported and driven: a forced-raise harness cell shows the unit survives).
3. Fidelity read on a local self-battery (v1 vs `_v542wave`, n small, NOT a verdict):
   every §2 metric within its named band or the miss attributed per-verb.
4. Per-verb ablation identity: each SK_* flag off reproduces the no-verb signature on its
   own metric (the fidelity instrument is the detector).
5. NO game-share claim of any kind in v1's founding report. The first currency read comes
   later, vs previous-iteration, under a prereg.

*Store-slot allocation and the entry-point skeleton follow the import manifest (landing);
they will be appended as §7 before the build agent is briefed.*
