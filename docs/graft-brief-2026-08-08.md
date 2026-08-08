# Graft brief — the merged-line case (for the Magnus/x3r0 conversation)

Prepared by the builder arm, 2026-08-08 morning (session 16). Every claim
below names its source; line numbers are v72 (`bots/opp_v72`, md5 1d2e8045)
unless stated. Deep dives: `docs/research/v72-delta-read-2026-08-08.md`
(line-verified defect list), `docs/research/v72-bleed-cad-family-2026-08-08.md`
(ray/bimodal laws), `docs/research/orekeeper-v69-production-read-2026-08-07.md`
(S1/S2/S4 production evidence).

## 0. The premise: the merge is already running in both directions

- v70 "endgame" contains our **piece H grafted byte-identical** (r960 switch,
  ammo dump, burnable cap, `_core_turret_mix` — comments included). x3r0 took
  our code first; this brief is just the deliberate version of the same
  traffic.
- Our v73 "Eir 7" contains **his E2b ore-pave ban and E1 ammo floor** (plus
  our S1 guard). E2b/E1/E2a/E4 are byte-identical v69→v72, so everything we
  measured on v69's E-series still describes v72.
- Net: each line already runs half the other's best pieces. What follows is
  the remaining half, ranked by measured value.

## 1. What his line still takes from ours (ranked, with honest sizing)

1. **S1 team check — two lines, fixes a measured self-damage loop.**
   `_intercept` :3269-3275 passes `tbid` with no team test; an enemy builder
   parked on his own conveyor makes the interceptor grind that conveyor at
   2 Ti/swing until the chase drops — measured 489 swings / 978 Ti in one
   game, 11% of all v69 melee hit his own buildings (production read S1).
   Our v73 ships the equivalent guard; the fix spec transfers directly.
2. **E2a hoist + gate widening — his mechanism, defeated by his dispatch
   order.** The step-off block sits below the `move_cooldown` early-return
   (:3065 vs :3053), so a saboteur that acts every round never reaches it
   (125/125 on-ore rounds, production read S2). He placed the new chain
   watchdog *above* that same gate — the hoist idiom is already in his file.
   Gate width: the 74-wall seat that cost 4,120-vs-23,310 is still six walls
   short of `ORE_STEPOFF_MIN_WALLS=80`; our measured widening is ore≤12 or
   walls≥70.
3. **Chain-repair economics — fix before an opponent reads his code.**
   The v72 watchdog replans from the harvester end and re-walks the whole
   chain at ~1 tile/round (`_link_path` returns the full route :3514-3519;
   `_build_next_link` pops occupied tiles it never verifies, :3583-3585).
   Against melee-grind opponents (~37 conveyors cleared/game vs kladde, his
   own comment :2903-2922) this converts idle expanders into repair crawls —
   research's top candidate for the v72 bleed vs the 1600+ band, and a
   standing denial row (kill the core-end conveyor of the longest chain,
   repeat). Fix shape from our line: `destroy()` is free and unlimited —
   verify-and-rebuild wrong heads from the break, not the harvester.
4. **Pave-crash guard — one line, modest for him, already banked for us.**
   `is_tile_empty(pp)` :3804 is still outside any try (the E2b try/except he
   added sits eleven lines below on the same variable). Severity asymmetry is
   real and we should not oversell it: in his line `run()` swallows it for a
   one-round action loss; in ours it was a unit-kill class (0-vs-128
   crashes/480 after piece N). It's a free line; take it, don't headline it.
5. **Heal-seat law (mechanism SETTLED by research's re-read — bleed doc §10;
   supersedes the 06:39 refinement).** The bimodal survival law is untouched
   and still the strongest defensive number on the board: heal/dmg ≥0.94 →
   13/13 sieges survived, ≤0.86 → 16/16 died; shortfall 1-3 missing healers,
   not titanium (died with 9,557 banked). But re-measurement of all six
   core-death episodes shows seat AVAILABILITY explains ~0 of that
   shortfall: raw "blocked" 4.8-8.0/8 collapses to 0-1 truly-impassable
   (conveyors/splitters are bot-passable, either team's — 89.3% of our
   episode core-heals fired from ON TOP of a seat conveyor), and the binding
   constraint was BODIES in 101/101 sampled siege rounds (usable seats 7-8
   vs 2.9-5.2 builders in reach, loiterers one move away worth 4.9-11.6
   HP/rnd). Actionable for his line, in lever order: (a) a standing heal
   detail with seat-seeking movement plus the population to staff it — THE
   lever; (b) gate impassable builds on the 8 core-orthogonal tiles —
   insurance (~1 seat in 3/6 episodes); the concrete hole is
   `_try_build_launcher` (his main.py:1144; ours byte-identical) taking the
   first legal adjacent tile from a builder standing beside the core — it
   produced the corpus's most frequent impassable seat blocker (our sentinel
   and an enemy gunner also held seats: placement rule, not
   launcher-specific). Three-line gate. (c) Do NOT ban conveyors from seats
   — forcing that cut delivery 23,930→270 in our test [builder-arm
   in-engine measurement], and 100% of core deliveries in the bleed corpus
   arrive through 2-7 distinct seats/game.
6. **Home-ring discipline vs the snipe-counter class.** Three independent
   teams hard-counter forward snipe deployment (KCM farmed it 9-1; the CAD
   family's reactive counterbattery; Clankers killed our snipe gunner in 6
   shots by r27 for 44 Ti). The cheap counters, measured on the CAD-family
   bleed corpus: tile-aimed fixed-facing home sentinels (uncovered-by-ray
   turrets took 0 shots EVER across 147 turret-games and did 96.6% of
   core-kill damage in the v117 losses), and **deleting rotate() from the
   home ring** (58% of ALL income in the 9 losses went to rotations —
   1,272 rotations / 12,720 Ti — vs 0.5% in wins). Our C1b ring wins 85% at
   wild-median establishment load (17/20, est≤4) — supply-bound at probe
   load, so it's a wild-regime plank, stated as such.
7. **Remaining unfixed list (v72 delta read §UNFIXED, items his call):**
   E4 ledger scope (924/1,190 futile swings land on turrets — outside
   `_sabotage_prio`), enemy-throw handshake gap :1457 (108 enemy throws,
   15 builders lost, 0 adaptation), unknown-map BFS still paves ore
   (:3521-3563), `SLOT_HARVESTERS`/`SLOT_HOME_GUN` monotonic high-water
   (:1112-1113), v71 screen barrier can wall his own trunk under siege
   (delta read FLAG 2).

## 2. What our line still takes from his

1. **A real re-plan (chainwatch's idea, generalized).** Our line's L4
   no-replan defect is the same disease his watchdog half-treats: our
   piece-F pave is the de-facto chain repair, which is why the _v85hs
   conveyor-ban experiment killed delivery. The graft is the *idea* (third
   `_link_path` call site on detected breaks) with his two caps fixed
   (vision-local detection, 12-hop cap) and repair-from-the-break ordering.
2. **Nothing else new at v72.** v71 orescreen is decoded-map-only six lines;
   endgame is our own piece H coming home.

## 3. Do-not-graft list (refuted on our tape — save him the cycles)

- **Defender-side launcher ejection ("Heimdall")** — CAD-family defenders and
  Clankers (439 ejections, income-gated) make it work; our implementation was
  value-negative with an exile-target hole (s15 verdict: PARKED-refuted).
  Needs a redesign, not a copy.
- **Un-gated core heal from r0 (K-as-built)** — 27-31% of builder turns eaten
  mid-fight; the siege gate is load-bearing (s13 ablation).
- **Sporks ammo policy as-ported** — refuted twice; his E1 floor + our cap is
  the surviving shape.

## 4. Slot context (so the conversation starts from the tape)

v73 "Eir 7" holds the slot: 6e base + his E2b/E1 + our S1, holder-parity
49.0 [44.5,53.4]/480 vs v72 accepted on Magnus's climb bet; field guards
kladde 83.3 / ouro 83.3 / band 95.0. Early window (~2 matches): W 3-2
Leviathan v25, **L 0-5 vs 0033 v43** — the 0-5 is under production-read
now (0033 v42 lost 4-1 to our v66 yesterday, then bumped). Rollback to v72
is pre-agreed one-click if the ladder disagrees. _v85hs (heal-seat
protection + staffed heal detail + ceiling lift) is gated locally as the
next candidate; gate results land on the coordination board today.
