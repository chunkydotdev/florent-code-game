# CAD ferry-loop barrier pre-mortem — 2026-08-07

> **STALENESS FLAG (s14, ~21:15): the entire CAD family moved versions
> tonight** — CAD v107→v115, Lunds v42→v43, KCM 7→1, Powerpuff 26→18.
> Historical analysis in this doc (era-internal reads, identity matches
> against v107-era replays) stands; every FORWARD-LOOKING v107-era claim
> (exact opening/throw constants, probe-fidelity assumptions, calibration
> values) is SUSPECT until re-frozen against the new versions per the
> standing constants rule.

**Version tags (rule 2):** target = CtrlAltDefeat **v107** (probe-valid
era; validity rule: check their version, they flip v107↔v112). Evidence =
15 archived games across THREE opponents: b10cce55 (vs Lunds Stallions
v42), cdbd5b52 (vs gsxWins v18), a7aa49ec (vs our v66). Local corpus
only, no downloads. Our live slot at read time: v67 wave_ghost. Research
arm, session 13. Candidate under pre-mortem: "one 3-Ti barrier on the
ferry tile breaks a 600-round harass loop" (my v66-salvage find).

## Evidence findings

1. **Opening throws (r2-6) are map-keyed and OPPONENT-INDEPENDENT.**
   Exact sequences reproduce byte-for-byte across different opponents on
   the same map: `(13,13),(13,13),(14,19)` vs Lunds AND gsxWins AND us
   (25×25, cores (5,5)/(18,18), 4 walls); `(9,8),(9,8),(12,0)` vs Lunds
   AND gsxWins (18×18); `(15,8),(15,8),(23,8)` vs gsxWins AND us (25×25
   variant). This is the only denial table measured today that is robust
   to OUR ships (unlike the Ouroboros rows, which expire because our
   builder deaths perturb their queue — CAD's openings don't read the
   opponent at all).
2. **The ferry loop is general v107 long-game behavior** — a ≥3-repeat
   ferry tile appears in 6 of the 7 games lasting 390+ rounds, vs every
   opponent (21× (12,10) vs Lunds; 28× (10,12) vs gsxWins-map game; 17×
   (1,0) + 2× (1,13) vs us). Short games (<270 rnds) show opening throws
   only.
3. **KILL FINDING: the ferry tile is NOT map-keyed.** Same map (the
   25×25/4-wall (13,13)-opening map), two different games: ferry =
   (12,10) vs Lunds, ferry = (1,0) vs us. The ferry destination depends
   on game state/opponent, so it is NOT predictable pre-game — only
   observable after the loop starts (~r40-105). Tiles are also not
   corner-seeking as my n=2 guess had it ((12,10), (10,12), (13,5) are
   interior).

## Kill conditions (the pre-mortem verdict hangs on these)

- **K1 — ferry tile unpredictable pre-game (CONFIRMED, finding 3):** the
  cheap version of the play (hardcoded pre-placed barrier) is dead. Only
  a REACTIVE version survives: detect ≥2 repeat throws in-game, walk a
  builder there, build. That costs a builder round-trip mid-game and
  lands ~r60+ at best.
- **K2 — re-target fallback UNTESTED:** `can_launch` requires a passable
  target; a barrier forces their selector to... unknown. If v107 picks
  the next passable tile, a barrier displaces rather than denies (~zero
  value). No observational case of a blocked ferry tile exists in the
  corpus. cad_probe replays decoded behavior and does NOT model
  re-targeting, so an arena leg vs the probe cannot answer this — only
  an instrumented unrated challenge vs real CAD (builder/rate-budget) or
  a natural ladder game where terrain happens to block the tile.
- **K3 — the predictable half targets low-value tiles:** opening throws
  are mid-map STAGING on large maps (dsq ~100+ from our core) — ring
  denial does nothing there. They go core-ring-deep only on small maps
  (a7aa49ec g1: dsq 5-17), and that game we WON anyway — deep inserters
  died to ordinary core-adjacent defense. Denial there hardens a game
  the Eir line already wins.
- **K4 — version flip:** any investment is void while CAD sits on v112
  (validity rule stands).
- **K5 — outcome coupling is weak:** CAD's biggest measured ferry (28
  throws) happened in a game CAD LOST; ferry presence does not cleanly
  predict CAD wins, so breaking it has unproven leverage.

## Recommendation (research view; verdict is the builder's)

**PARK the barrier play.** The candidate as originally framed ("cheapest
denial on the board") does not survive its pre-mortem: the predictable
tiles are low-value (K3), the valuable tile is unpredictable (K1), and
the deny-vs-displace question is untestable without spending platform
budget (K2). What DOES survive:

1. The **map-keyed opening table** (finding 1) is real, robust
   intelligence — worth keeping as constants for any future anti-CAD
   work precisely because it survives our ships. Extraction is one
   script-run per map as archive coverage grows.
2. If Loki investment vs CAD is wanted anyway, the test that unlocks it
   is ONE instrumented unrated challenge with barriers pre-placed on the
   current map's opening tiles + a reactive ferry blocker — a single
   game answers K2 for both throw classes. Spec available on request;
   the challenge spend is the builder's call.
3. The launcher-abduction precedent (v66-salvage read) stands unchanged
   as a constraint on any anti-CAD builder routing.

## ADDENDUM (session 14, ~21:05) — ferry-loop ATTRIBUTION RE-CHECK FLAGGED

The KCM classification read (docs/research/kings-college-classification-
2026-08-07.md, anomaly 1) found that in every KCM game with a long
repeat-throw loop, the throwing launcher belongs to the OPPONENT — KCM's
own launcher is self-destroyed at r6 in 25/25 games, and CAD v107 shows the
same build-then-destroy-at-r6 pattern in a 582-round game. This raises the
possibility that this pre-mortem's "≥3-repeat ferry tile in 6 of 7 long
games" measured the DEFENDER recycling the attacker's raiders, not a CAD
ferry mechanism — which would invert the K1/K2 deny-vs-displace framing
(nothing of CAD's to deny). The PARK verdict is unaffected (it was already
park). RE-CHECK before any future investment in this line: re-run launcher
attribution (owner team of the throwing launcher id) on a7aa49ec/b10cce55/
cdbd5b52. The map-keyed opponent-independent OPENING constants (launcher
tile, r2-r4 throw targets) are unaffected — those are measured from the
opening table, not the loops.

### Re-check resolution (session 14)

All three named files exist locally (a7aa49ec-3456-4f88-bc4a-9cea2e07164b,
b10cce55-ba4d-4b5c-afc4-ce30b4c197a9, cdbd5b52-3638-4e99-bc99-9fe0f7163906,
5 games each = 15 games total, matching the premortem's stated corpus). CAD
is team B in all three (b10cce55/cdbd5b52 meta.json; a7aa49ec has no
meta.json on disk, but team-B identity is corroborated independently: its
r1-built, r6-destroyed launcher throws the exact byte-identical opening
tiles the premortem's finding 1 already attributed to CAD, e.g.
`(13,13),(13,13),(14,19)` on the 25×25 map in a7aa49ec g3/g5).

**Method correction, load-bearing:** launcher throws do **not** emit a
`FireTurret` update (that field is gunner/sentinel shots only — every
launcher's attributed-fire count came back 0 on a first pass). A throw is
visible only as a `moveBuilderBot` whose `to` is more than one tile from
`frm` (builder bots otherwise only take single cardinal steps, so any
`distance_sq > 1` move is a throw). The thrower is whichever launcher is
alive and orthogonally adjacent to the bot's pre-throw tile that round —
unambiguous in every case in this corpus (only one candidate launcher was
ever in range at a time). Script: `ferry_launcher_attrib2.py` in the
session-14 scratchpad, built on `docs/research/2026-08-07-fanout/toolkit/
replay_lib.py`.

**Family signature (CAD's own launcher):** built r1, destroyed r6 by its
own team, in **13 of 15 games**. The two exceptions are cdbd5b52 g3 and g5
(both <110-round games CAD won or lost fast) — CAD never placed a launcher
at all there (built gunners/a sentinel instead); confirmed by the entity
build log, not a parser gap. In every one of the 13 games where it exists,
CAD's launcher fires **exactly its known opening throws (2-4, r2-r4) and
nothing else** — 100% of its throws move CAD's **own** builder bots
(ferrying), 0% touch an enemy bot. It never survives past r6, so it is
structurally incapable of producing any throw after that round.

**The long-game repeat-throw loop, every instance, belongs to the
defender's launcher — not CAD's:**

| Match (opp) | Game | Rounds | Defender launcher | Built→destroyed | Throws (own / CAD-enemy) | Target tile(s) | Matches premortem's finding-2 number |
|---|---|---|---|---|---|---|---|
| a7aa49ec (us, v66) | g3 | 672 | #30, team A (us) | r11→r518 | 3 own (r2-4, opening) + **17 enemy** | (1,0) | "17× (1,0) vs us" — exact |
| a7aa49ec (us, v66) | g5 | 803 | #29, team A (us) | r15→alive | 0 own + **2 enemy** (sub-3 threshold) | (1,13) | "2× (1,13) vs us" — exact |
| b10cce55 (Lunds v42) | g1 | 476 | #7, team A (Lunds) | r1→r430 | 1 own (r3) + **21 enemy** | (12,10) | "21× (12,10) vs Lunds" — exact |
| b10cce55 (Lunds v42) | g3 | 407 | #7, team A (Lunds) | r1→r254 | 1 own (r3) + 6 enemy | (12,10)×5, (13,8)×1 | — |
| b10cce55 (Lunds v42) | g4 | 814 | #7, team A (Lunds) | r1→alive | 2 own (r3,155) + **28 enemy** | (10,12) | "28× (10,12) vs gsxWins-map game" — exact (same 18×18 map layout, played vs Lunds) |
| b10cce55 (Lunds v42) | g5 | 1000 | #7, team A (Lunds) | r1→alive | 1 own (r4) + 4 enemy | (13,5) | — |
| b10cce55 (Lunds v42) | g2 | 362 | #7, team A (Lunds) | r1→r309 | 1 own (r3) + 2 enemy (sub-3, medium game) | (5,7) | — |
| cdbd5b52 (gsxWins v18) | g1/g2/g4/g5 | 69-109 | gsxWins launcher | r1-2→alive | 3-5 own, **0 enemy** | — | short games (<270r): opening throws only, no loop develops — consistent with premortem's own note |

Every "enemy" throw above moves a **CAD (team B) builder bot** — always
`kind=builder_bot`, always landing multiple tiles from its pre-throw tile,
i.e. the defending team's launcher (built r1-2 like CAD's, but **kept
alive** instead of self-destroyed) is picking up CAD's inserted raiders and
throwing them off to a fixed corner/edge tile. In every long game (a7aa49ec
g3, b10cce55 g1/g3/g4/g5) this is the entire content of the "≥3-repeat
ferry tile" signal the premortem measured. CAD's own r1 launcher is dead by
r6 and never touches an enemy bot in any of the 15 games — there is nothing
of CAD's being ferried to that tile; it is the defender's discard pile for
CAD's raiders. gsxWins (cdbd5b52) never reaches this phase only because
every game there ended before r110 — its own launcher shows the identical
"build r1-2, keep alive, self-ferry at opening" shape as Lunds and us, just
without a long enough game to demonstrate the recycling phase.

**Kill-condition consequences:** K2 ("does a barrier displace or deny?")
was already the untested blocker; this re-check makes it moot for the
loop-tile case specifically — a barrier on (1,0)/(12,10)/(10,12)/etc. would
not deny CAD anything, it would obstruct **our own/the defender's own**
launcher's disposal throws of already-neutralized raiders. K3/K5 (low-value
predictable tiles, weak outcome coupling) stand as written and now have one
more reason: the "valuable" unpredictable tile the K1 reactive-blocker
would chase is not a CAD asset at all.

**Verdict: INVERTS.** The pre-mortem's finding-2 framing ("CAD ferry loop,
deny the tile") is backwards for every long game in this corpus: the
repeat-throw launcher is the defender's, not CAD's, and it is disposing of
CAD's inserted builders rather than ferrying CAD's own. The PARK verdict on
the barrier play is unaffected (it was already parked on other grounds) and
this closes the RE-CHECK cleanly: the map-keyed OPENING throw table
(finding 1) remains real, opponent-independent CAD intelligence and is
untouched by this correction.
