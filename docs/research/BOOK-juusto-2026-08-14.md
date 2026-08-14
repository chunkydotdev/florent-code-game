# JUUSTO — OPPONENT BOOK (research s40, 2026-08-14 ~15:0xZ)

Answers the question the 0033 book left open. Zero replay downloads, zero net calls; corpus only
(516 archived Juusto games, 260 vs us), ~10 scripts in the session scratchpad. Seat derived from
`meta_join` team NAMES — independent of `winnerSide` — controlled against the teamId-derived
`us_side`: **0 disagreements in 260 vs-us games**. Every instrument carries its counter-verdict
control inline. **No `econ.tsv` read anywhere** (corrupt on recent files; every Juusto game is
recent); shots from `build_agg` `metric=='shot'`.

## The headline — IT IS A FOURTH SHAPE, and the mechanism is an exploit
**Juusto v11 is a LAUNCHER-RELAY BEACHHEAD.** Bisons (0 launchers/892 games), 0033 (0/2,307) and
Leviathan are turret-dose shapes with a walking builder. Juusto v11 **builds 403 launchers in 110
games (3.66/game) and demolishes 402 at an age of EXACTLY 2 rounds — p25 = median = p75 = 2,
402/402** — on a 3-round cadence. They are not turrets, they are **disposable taxis**. Decoded
relay, one bot id thrown repeatedly: `r6 d²1013 → r9 685 → r12 421 → r15 221 → r18 d²13` — the
same builder, five hops, 32 tiles → 3.6 tiles from the defender core in 12 rounds. **109 multi-hop
relays across 75 of 110 v11 games**; median 3 hops / 7 rounds / d² 530→17; **effective closing
speed 2.52 tiles/round against a walking builder's 1.0**; 61/110 games land a builder within 5
tiles of the defender core; terminal hop median r18 (p10 r9). Zero ammo, and each launcher's +10%
cost-scale contribution is refunded by the demolition two rounds later — **they rent the launcher
rather than own it.** Cross-decoder confirmed: `builds.tsv` independently says 403.
**Complement control — nobody else does this:** launcher median lifetime SmartFridge 141, us 65,
Focalground 46, Banminary 15, Jython 5; the `life ≤ 2` share is 0–45% for all 14 top
launcher-builders in the archive and **100% for Juusto v11.**

## (a) The era boundary: v10 → v11 (first seen 2026-08-14T00:52:59Z)
Length-controlled at **r≤50, vs us**, per game, only two planks moved: **launchers 0.00 (v7,
n=140) / 0.00 (v10, n=25) → 2.28 (v11, n=65)** and **barriers 1.73 / 2.48 → 4.78.** Builders
(4.53/4.56/4.58), harvesters (2.08/1.96/2.12), conveyors (9.08/8.92/8.54), sentinels
(1.30/1.12/0.94), gunners (0.51/0.36/0.20) are flat.
- **The barriers are a SPAWN-RING WALL. 708 of 717 v11 barriers (99%) sit at d²≤5 of the
  DEFENDER's core** — observed values are only 1, 2, 4, 5, i.e. the 12 tiles hugging a 2×2 core
  footprint, which is `can_spawn`'s ring. **Control, same instrument same team: v7 5/617 (0.8%),
  v10 2/113 (1.8%).** 6.34/game vs us (64 of 65 games) and **6.58/game vs the field (45 games) —
  opponent-blind**; median 7/game, max 20; first at p10 r15, median r35.
- **They ABANDONED builder melee at the same boundary.** `batk_core`/game vs us: **v7 32.2 · v8
  42.2 · v9 132.0 · v10 90.2 → v11 0.00**; total `batk` 183 → 231 → 199 → **15.6**. v7–v10 was a
  builder core-rush; **v11's core kill is 100% turret fire.** (Our own `batk_core` is 0.00 in all
  260 archived games, every era — self-audit item, not their doing.)
- **Unchanged:** forward sentinels at median d²=16 of the defender core, 94% forward, r41 (v7:
  d²16, r46) — and **the catapult did not accelerate them** (first forward sentinel median r24 →
  r25). The relay delivers the barrier builder, not the turret.
- Payoff: **v11 runs 112/180 = 62.2% game share vs the field over 36 matches against 50.1%
  Elo-expected (+12.1pp), and +132 Elo in 11.7 h (1751.1 → 1883.3).** All eras +6.0pp on 1,025
  games — **still underrated at 1883.**

## (b) Current shape (v11, 110 archived games)
- Per game: 5.70 builders · 14.20 conveyors · 2.90 harvesters · **6.52 barriers · 3.66 launchers ·
  1.60 sentinels · 0.33 gunners.** Splitters 0.
- **Their turrets are the hardest-worked I have measured, OVERTURNING QUEUE #46's "decorative
  siege" premise at 4.3× its n: 3,868 shots / 97 turrets = 39.9 shots per turret** (65 vs-us
  games), up from v7's 20.2 (9,118/451, 140 games); **ours in the same games 10.7.** They out-fire
  us 3.7:1 per turret off half the stock — #46's refutation direction was right and understated.
  **Banked ammo (#46's 11,939) is NOT MEASURABLE on the safe surface** (`ammo_end` lives only in
  the corrupt `econ.tsv`): unresolved, not refuted.
- **Opening scripted and opponent-blind, weaker than 0033's.** Cell = (map dims, first-build tile);
  identity of builds 2-4 / 2-8 / 2-14 across DIFFERENT opponents **82% / 58% / 30% (164
  cross-opponent pairs, 18 cells)**; control, their opponents in the same cells 0/0/0 (n=11); 0033
  is 100/99/87. **First harvester median r8 on a tile modal in 90% of games (94/105, 21 cells).**
- **CPU is not a lever: 0 tled, max 4,807 µs of 10,000 across 601,677 Juusto unit-turns (350
  games, v7+v11), mean 672 µs.** Instrument live: field opponents in the same v11 files logged 449
  over-10 ms turns. ⚠ **Self-audit: our own max here is 8,818 µs (v11) / 9,185 µs (v7) — 88-92% of
  budget, 0 TLE. Thin.**
- **Crash-induction dead: 0 non-launcher crash candidates on Juusto's side in 350 archived games**
  (v7: 0 on either side across 240; v11: 400, ALL launcher = their own recycle). ⛔ **Their recycle
  makes `crash_census` structurally blind on this team** — build→throw→demolish has the identical
  wire signature to a crash.
- **Kidnap uncontested and never used by them:** 401 v11 throws, **395 INSERT of their OWN builder,
  0 EXILE of an enemy**; their launchers are home-side (median d²_own 65, d²_enemy 225).

## (c) Pairing book vs us
- **Rated h2h (`ladder_games.tsv`, the only denominator authority): 24/50 = 48.0% our share**,
  2026-08-13T02:32Z → 08-14T04:32Z, our v116+v125 only. By their version **v7 15/30 (50.0%) · v8
  2/5 (40.0%) · v11 7/15 (46.7%)**. Reconciled independently against `league_matches.tsv` (26/50
  for them). **Mixed-fixture caveat, large here:** the 260 archived vs-us games pool our PROTOTYPES
  with our shipped bot and read **17/65 = 26.2% for us** at v11. Use 46.7%; 26.2% is an artefact.
- **Their kill clock collapsed at v11; ours did not.** Archived vs-us, round of core death: they
  kill us at **v7 r183 → v11 r124.5**; we kill them at v7 r176.5 → v11 r164. The rated 15-game cell
  agrees in direction (our wins r214, our losses r121.5). **Out-racing them is losing math from v11
  on.**
- ⛔ **THE COUNTER IS THE RING, and ~~it replicates a THIRD time~~ — REPLICATION CLAIM WITHDRAWN s40 ~14:4xZ (side-lane sweep flag; restated on the tape). The arithmetic below reproduces EXACTLY (24.2% = 16/66, 15.0% = 52/346) and the INTERVALS OVERLAP: [13.9, 34.6] vs [11.3, 18.8] — and at the GAME level with match clustering they overlap far wider (21.9%±20.8 on 17 games vs 10.4%±7.1 on 47). ⛔ 14:5xZ: the same clustered redo collapses the OTHER two books' cells too — Bisons 36.9-vs-17.6 becomes 18.9-vs-13.1 (overlap), 0033 becomes 25.7-vs-15.0 (overlap). NO CELL SEPARATES AT THE CORRECT UNIT. The point estimates line up with the other two books; the evidence at this cell's n does not support calling it a replication.** What DOES survive and is new: the round-band split, which the claim never had — early (r<100) removal is **21.2% in our wins vs 7.5% in our losses (2.8×)**, and that direction is the one reverse causation cannot easily explain. **THE ORIGINAL CLAIM FOLLOWS FOR THE RECORD:** Ring-barrier removal rate
  (deaths/builds of their d²≤8 barriers), v11: **field defenders who WIN remove 40.4% (19/47);
  field defenders who LOSE remove 11.2% (28/249). We remove 24.2% in our wins, 15.0% in our losses
  (16/66 vs 52/346).** Per field team: Torsko 8.9% (2 wins/15 games), 0033 7.9% (3/13), HTTP 418
  2.9% (0/5) vs team lazy 38.1% (2/5), kladde 35.7% (1/5). Same discriminator as the Bisons book
  (66% vs 15-17%) and the 0033 book (51% vs 14%) — **on a third shape, and now against a target
  class that is neither a sentinel band nor a creeping gunner but a 3-Ti barrier standing on our
  own spawn ring.**
- **What differs in our losses:** they plant **7.21 ring barriers/game in our losses vs 3.88 in our
  wins** (n=48 vs 17, archived-mixed); our conveyors fall 25.35→16.40, harvesters 5.06→3.42,
  sentinels 3.59→1.40. **Their launcher dose is identical in wins and losses (2.88 vs 2.98) — like
  Bisons, the dose is not the variable; our removal is.**
- ⚠ **NULL, reported because it is the obvious story and it does not hold:** the ring does NOT
  measurably strangle our belt terminus. Our conveyors at d²_own≤8, r0-150, games alive to r150:
  v7 4.98 → **v10 3.67 (no ring at all)** → v11 3.16 — the decline predates the plank. **The ring's
  mechanism is UNRESOLVED.** INFERENCE, unmeasured, offered as hypothesis only: a barrier maze on
  our ring blocks GUNNER line-of-fire (obstacle-blocked) while their SENTINEL shot ignores
  obstacles — an asymmetry the rules table hands them.
- **Per-map, rated, n=50 — cells are 1-5 games, hints not findings:** 4/4 yulerune, 3/3 valkyrie;
  **0/2 lighthouse, 0/2 jackpot, 0/2 midgard, 0/2 fjordgate, 0/2 royale, 1/3 nordkap, 1/3
  auroraveil, 2/5 ragnarok.** Field-wide per-map is NOT AVAILABLE for them (no league-wide map
  surface — QUEUE #39's own correction). Field holes by opponent (all eras, n≥10): Torsko 40%,
  Team 48 40%, Pantheon 40%, gsxWins 40%, Flotte 40%, Jython 44%, HTTP 418 45%.
- **Target band (recompute at fire time; `target_value.py`'s cache is ~65 pts stale):** us
  **1744.3**, them **1883.3**, both newest rows 2026-08-14T12:32:59Z → **gap +139.0, E=0.310; 5-0
  pays +22.08, 4-1 +15.68, 3-2 +9.28, 2-3 +2.88, 0-5 −9.92. Top-band, fully reachable.**

## Deltas against the commissioning anchors
1. **Archived counts LARGER than briefed** (corpus synced 14:56Z; every extra game is v11): 516
   Juusto games vs 491, 260 vs-us vs 245, v11 110/65 vs 85/50. Other-opponent counts match exactly.
   Rating: the brief's 1880.2 @ 11:52:59Z reproduces exactly; corpus now runs to 12:32:59Z at
   1883.3, peak 1901.5 @ 11:12:59Z.
2. ⛔ **`tled` IS NOT FICTION ON THE WIRE.** CLAUDE.md and the brief say the flag does not exist in
   platform replays. Read directly with `tle_census.py`: **446 tled turns against 449
   independently-computed `execTimeUs > 10,000`** on the field-opponent side of these files —
   agreement to 0.7%. **The dead thing is `econ.tsv`'s COLUMN, not the wire field.** As written the
   note retires a live instrument.
3. **"100% decisive, zero r1000s" is NOT a Juusto property.** Control: our own v116/v125 era vs the
   WHOLE field is **504/515 `core_destroyed` (97.9%), 11 r1000 games**; the all-time 76.3%
   (3,683/4,825) is dragged down by dead eras. **Nothing about this matchup needs explaining — it
   is our current bot's profile.**
4. Everything else reproduced exactly: 24/50, the 15/30 · 2/5 · 7/15 split, 50/50 `core_destroyed`,
   median 181.5 turns, the 1→2→1→3→1→3→5→4→3→7→8→9→10→11 chain, and the field win/loss table.

---

## ⭐⭐ RESEARCH VERIFICATION + ONE CORRECTION THAT MOVES THE ROUTING (s40, 2026-08-14 ~13:3xZ)
*Commissioner's pass. Load-bearing numbers re-derived at the primaries before
banking, per the relay rule — an agent's number is a claim until checked.*

**REPRODUCED EXACTLY, independently, off `events.tsv` + `builds.tsv`:**
v11 `BUILD/LAUNCHER` **403** and `DEATH/LAUNCHER` **402** · v11 `BUILD/BARRIER`
**717**, of which **708 at d²_enemy ≤ 5 = 98.7%**, distribution **exactly the
four core-hugging values (d²=5:188, 4:188, 2:169, 1:163)** and nothing else
until d²=13 · v10 **2/113 = 1.8%** · 110 v11 games. **Two small deltas, neither
load-bearing:** the book reads v7 5/617 (0.8%), I read **3/617 (0.5%)** —
d²-boundary handling, contrast unchanged; and `builds.tsv` carries **zero**
barrier rows (it is turrets/launchers only), so every barrier figure here must
come from `events.tsv`, which is where mine came from.

### ⛔ THE CORRECTION: **THE RING IS NOT A FOURTH SHAPE'S NOVELTY. IT IS OUR OWN SIGNATURE PLANK, AND WE ARE LOSING THE RACE ON IT.**
The book reads the spawn-ring wall as new. **It is not new to the league — it is
the thing WE do**, and the book's framing (*"the mechanism is an exploit we do
not ship"*) is right about the ferry and **wrong about the ring**:

| team / version | barriers | at d²_enemy ≤ 5 |
|---|---|---|
| **us, v125** | 6,779 | **6,004 = 88.6%** (d²=5/4/2/1 are the top four values) |
| us, v116 | 1,984 | **1,984 = 100.0%** |
| us, v139 | 1,105 | 954 = 86.3% |
| **us, v140 (live)** | 597 | **542 = 90.8%** |
| Juusto v11 | 717 | 708 = 98.7% |

**And at d²_OWN ≤ 5 we are at 0 of 12,465 barriers, across every version and
both seats.** *(Control run because the reading depends entirely on the column
frame: the decoder computes `own, enemy = corepos[e.team], corepos[1-e.team]`
per ACTING team — `replay_events.py:87` — and splitting our own barriers by our
seat gives 0.0%/90.1% as team 0 and 0.0%/86.9% as team 1, i.e. **the same both
ways**, which rules out a fixed-perspective mislabel. Juusto v11 is likewise
0/717 on their own ring.)*

**THE HEAD-TO-HEAD, 65 archived OpenSverige vs Juusto-v11 games — this is the
number that should drive the routing:**

| | ring barriers | median round | p10 | first | per game |
|---|---|---|---|---|---|
| **Juusto seals OUR ring** | 412 | **r32** | r14 | r6 | **7.0** |
| **we seal THEIR ring** | 271 | **r51** | r23 | r6 | **5.0** |

**They run our own plank ~19 rounds earlier and ~40% heavier.** Both sides open
at r6, so this is not access — it is **commitment and rate**.

**WHY THIS CHANGES THE ROUTING.** Framed as a new shape, the answer is "study
it". Framed correctly, the questions are ours and already tractable: **why does
our ring seal start at r51 when theirs starts at r32, and what gates the rate?**
That is a timing/volume question about code we own — and it lands squarely on
**#53's surviving scope after its s40 re-scoping (seal TIMING and GEOMETRY, both
never swept)**, which was queued as low-priority exploration of a validated
asset. **A live opponent out-executing us on that exact asset is the "why now"
that row did not have.** The ferry stays the genuinely new import.

⚠ **What this does NOT establish:** that the ring is why they beat us. The
book's own belt-strangulation null stands, the mechanism is UNRESOLVED, and
r32-vs-r51 is a difference in *execution of a plank whose value is separately
ablation-validated at −10pp* — not evidence that 19 rounds of ring latency is
worth the h2h gap. **Do not let a clean table become a causal claim.**

## Routing
- **#3 CLEAR MORE ENEMY TURRETS — third shape, target class must widen again.** The 0033 book
  demanded "the barrier screen" join the priority set; Juusto v11 makes it the WHOLE plank: 6.5
  barriers/game, 99% on our own spawn ring, **40.4%-vs-11.2% field win/loss split on removal**, us
  at 15.0% in the games we lose. **KNOB: the target scorer must rank a 30-HP, 3-Ti barrier at d²≤5
  of OUR OWN core as a priority target from r15 — not as terrain.**
- **#45 KILL THE BUILDER — Juusto is its THIRD named customer and the cleanest.** The entire v11
  damage chain needs ONE unescorted, melee-less builder beside our core from p10 r15 / median r35,
  placing barriers on tiles it must be orthogonally adjacent to (rules-level, not inferred). It
  arrives on a 90%-modal script by build #8, terminal hop median r18, no escort (0.33 gunners/game,
  all home-side).
- **#51 AIM THE THROW LOOP — direct read-across; they have BUILT what #51 is trying to design.**
  Their relay is our EXILE loop reversed (INSERT, own bot, 2.52 tiles/round). **Two knobs: (i) a
  home launcher covers pickup d²≤2 and their relay builder enters that envelope by construction —
  EXILE it back and the whole 7-round investment resets; (ii) copy the rent-don't-own trick — a
  launcher demolished 2 rounds after use refunds its +10% cost-scale contribution, which is why
  theirs is affordable at 3.66/game.**
- **#39 OPENING BOOK — Juusto is a stocked row now.** First harvester median r8 on a tile modal in
  **90% of games (94/105, 21 cells)**; builds 2-4 identical across different opponents in 82% of
  cross-opponent pairs (control 0%). One 3-Ti barrier per modal tile taxes their key-1 from r8.
- **#43 BARRIER-IN-BASE CRASH — evidence AGAINST, plus a blindness warning.** Juusto plants 717
  barriers inside enemy spawn rings across 110 games and produces **zero non-launcher crash
  candidates on the defenders' side**. Their own 400 launcher "candidates" are self-demolitions —
  proof that **`crash_census` cannot separate a recycle from a crash**, so any #43 arm shipping a
  build→destroy loop will read as a crash farm.
- **NEW, no row yet: THE DISPOSABLE-LAUNCHER FERRY AS OUR OWN PLANK.** 2.52 tiles/round raider
  delivery, 0 ammo, scale-neutral, built entirely from documented calls. Our raiders walk. Most
  transferable thing in the book; belongs in QUEUE.
- **#41 unchanged by this book** (their sentinels sit at d²16, r41, and are not the new thing) —
  noted so the row is not credited with the v11 step change. **CLAUDE.md `tled` correction (delta
  2) → builder + tape.**
