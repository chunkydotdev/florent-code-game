# wave_ghost (v67) first field read — 2026-08-07

**Version tags (rule 2):** our live slot = **v67 "wave_ghost" (x3r0's bot, NOT
the Eir line)**, active since 17:52:43 local (auto-activate on upload; pinned
via match-stamp boundary 17:49:01→17:52:43.777). No bot dirs code-read — this
is a pure replay decode; `bots/opp_v67` (builder's extraction) untouched by
this arm. Opponent versions cited inline. Decoded by the research arm,
session 13, from matches: b7c0ea11 (SmartFridge v34, UR L 2-3),
b92d7da8 (sporks v2, UR L 0-5), e71e0b65 (team lazy v94, UR L 1-4),
03af6569 (Team 48 v16, ladder W 5-0). All four ran under v67 (each match's
created+completed interval sits entirely post-flip).

## Headline

wave_ghost is a **forward-sentinel core-snipe strangler**: it rushes a
sentinel onto a tile within attack range (dsq ≤ 32, usually 25-32) of the
ENEMY core as early as round 4-17, then drip-converts titanium→ammo
hand-to-mouth (~10 per fire cycle, bank ≈ 0-24) and chips the enemy core
18 dmg / 2 rounds through walls for the entire game. Sentinel shots ignore
obstacles — hence "ghost". It built ONE gunner across all 25 platform games
read (g1 vs Team 48; zero in the other 24), keeps essentially no ammo
reserve, and runs a small, fragile conveyor economy.

**It is one-trick: kill the first sentinel and wave_ghost goes permanently
dark.** In all 5 sporks games the forward sentinel died 3-17 rounds after
placement; wave_ghost's last turret shot of the *entire game* came at
r11/r36/r68/r78/r95 in games lasting 204-1000 rounds. It re-attempted a
snipe sentinel exactly once across those five games (a defensive tile,
dsq 317 — wrong tile, died anyway).

## Field record under v67 (all of it, as of 18:10)

| match | opp (ver) | type | result | mode |
|---|---|---|---|---|
| 03af6569 | Team 48 v16 (family battery) | ladder | **W 5-0** (+18.1) | snipe survived 5/5 games, core kills r84-277; T48 fire establishment broken (0 shots in g1) |
| b7c0ea11 | SmartFridge v34 | UR (incoming) | L 2-3 | won the two LONG games (496, 439 rnd strangles); lost both sub-75-rnd games + a 245-rnd scale-out |
| 28c962a9 | Lorem Ipsum v14 | UR (incoming) | L 2-3 | not downloaded (budget) |
| e71e0b65 | team lazy v94 (family battery) | UR (incoming) | L 1-4 | see below |
| b92d7da8 | sporks v2 (2024-rated) | UR (incoming) | L 0-5 | sentinel killed early ×5; 2 econ-tiebreak losses (91 vs 2,467 stacks delivered), 3 core losses |

Ladder 1-0, incoming URs 0-4 (5-15 in games).

## Mechanism detail (evidence)

- **Snipe tile choice:** first sentinel dsq to enemy-core footprint = 32,
  25, 32, 25, 32, 25 across six independent maps — always inside the
  r²=32 line, planted r4-r17. On the 16×16 (g5 SmartFridge) it stood at
  (8,8) vs core (3,3): the geometric center tile.
- **Ammo policy:** never converts at r0. First convert r5-10, amounts
  16-24, then continuous ~9-avg drips (236 converts in one 496-rnd game,
  2,121 total). Peak bank in a healthy game: 6-24. Contrast SmartFridge
  (120@r0 every game) and sporks (17@r0/cap 60/top-up 4 — **unchanged
  from our sporks decode; their v2 still runs the exact constants** the
  Eir 6 worker is adopting).
- **Win mode:** if the snipe sentinel survives, the strangle wins long
  games — SmartFridge g1: sentinel born r7, survived 496 rnds, 212 fires,
  enemy core dead r495. g4 same shape (439 rnds, 123 fires).
- **Loss mode 1 (snipe dies):** no rebuild, no plan B. Post-death behavior
  is incoherent: converts either freeze (bank flatlines at 24) or continue
  with zero turrets alive (sporks g4: banked 256 ammo it could never fire —
  ~296 Ti burned into unusable ammo; ammo has no conversion back).
- **Loss mode 2 (economy fails):** chain-wiring is buggy. SmartFridge g5
  (16×16): 4 harvesters built, **0 connected — all orphans**, 0 Ti
  collected, 2 ammo total, its surviving sentinel fired twice in 65
  rounds. Worst on small maps; across 20 games its connected-chain rate is
  far below either opponent's.
- **Loss mode 3 (tiebreak):** its stack delivery is negligible (91 vs
  2,467; 301 vs 1,423 in the sporks r1000 games). Any r1000 game vs a
  functioning economy is an auto-loss on tiebreak #1.
- **No gunners, minimal barriers:** local defense is the forward sentinel
  itself plus terrain. Fast rushes reach the core with nothing in the way
  (SmartFridge killed it r65/r70 in its two fast games).

## Why it 5-0s Team 48 but loses 1-4 to team lazy (both family batteries)

ANSWERED, both legs read (03af6569 all 5 games + e71e0b65 all 5). The
split is line-of-sight economics + heal discipline, not family identity:

- **Team 48 v16 (0-5 swept):** our snipe sentinel survived ALL FIVE games
  (born r5-30, died never) and killed their core in r84-277. Team 48's
  battery barely establishes fire — g1: ZERO shots all game (20 ammo
  converted at r3, never spent); g2: battery dead by r117 of 277; g5:
  first fire r36. Its gunner lines are terrain-blocked exactly where our
  ghost shot isn't, it runs its bank at 2-53, and it NEVER heals its
  core, so even the half-duty chip (~5-9 HP/rnd) beats it. In the clean
  games the strangle killed in 85-117 rounds — its fastest kills anywhere
  in this read.
- **team lazy v94 (1-4):** same mechanism, opposite outcome — lazy keeps
  a firing battery alive (105-673 shots/game) AND heals through the chip,
  so the sentinel's survival is irrelevant on open maps.

Consequence for the family model: the family counter-math (J + ammo-sink
+ race) is unaffected, but wave_ghost's +18 ladder win generalizes only
to the family's bottom (Team 48-grade fire establishment), not to
lazy/Leviathan-grade members.

## SmartFridge behavioral entry (builder ask)

SmartFridge (1732, 882 matches) fired **four incoming URs at our slot in 31
minutes (17:27→17:58) cycling three of their versions: v34 → v33 → v35 →
v34**. That is a deliberate A/B probe series against whatever we have live —
they collected v66 data on three variants, then re-probed v34 the minute
the slot flipped to v67. Treat them as an adaptive opponent tuning
specifically against our slot; expect their next activation to be fitted to
whichever of v66/v67 survives the slot conversation. (Their own shape, from
the 5 games read: 120-ammo bank at r0, gunner-led with launcher-heavy
late-game scale-out — 10 builders/30 conveyors/5 launchers in their 245-rnd
win.)

## Slot-conversation relevance (research view, no verdict — that's the builder's)

- wave_ghost's UR record vs strong opposition is 0-4 with a mechanism-level
  explanation (one-trick + dead-man switch), while its +18 ladder win is
  vs the family's weakest member. The builder's 480-game slot bar
  (matched-noise, _v76e51 vs opp_v67) is the measurement; this read
  explains the *mechanism* behind whatever number it produces.
- Eir 5.1's J counterbattery exists precisely to kill exposed enemy
  turrets; a 40-HP sentinel parked at a known dsq≤32 tile at r7 is J's
  ideal prey. The builder's single verification game (Eir 5.1 core-killed
  wave_ghost r209 on eider) is consistent.
- If wave_ghost keeps the slot anyway: its ladder results will hinge on how
  much of the pool can kill one forward sentinel early. Pool mix says
  point-blank 46.4% + picket 28.6% — the picket class (turret walls) walks
  into the strangle and may feed it; the family's faster members
  (Leviathan median 64 rnds) likely out-race it.

### Reconciliation with the builder's measurements (18:12-18:15 notes)

The builder's slot bar (parity 51.9/480 vs Eir 5.1) and vs-field profile
(equivalent on kladde/ouro/band/flotte, **cad 61.7 = only leg not clearing
50**) landed after this read started; mechanism and measurement agree:

- **Insertion softness is mechanism-predicted**: no gunners, no local
  defense, no ammo bank — a thrown raider lands beside the core with
  nothing in the way. CAD v107 beat v66 1-4 AND is wave_ghost's weakest
  instrument leg; insertion is the shared soft class of both our lines.
- **Terrain-niche hypothesis: REFUTED as a driver of the Eir matchup**
  (builder's per-map correlation over the 480: r(wall% vs our wins) =
  0.027, r(area) = 0.042, r(core sep) = −0.093 — no split; caveat 32
  games/map hides weak effects, but a niche-dominates split would show).
  The niche claim survives only where it was observed: vs opponents that
  neither kill the sentinel nor out-tempo it (lazy g4, SmartFridge g1/g4).
  Builder's reconciliation hypothesis, primary-evidence check pending: J
  kills the 40-HP sentinel at its predictable r4-17 plant tile on every
  map class, the niche never activates, and the matchup collapses to
  economy/tiebreak grind (fits 229/480 tiebreak-decided). Arena discards
  replays (`--replay /dev/null`), so confirming sentinel death rounds
  needs a small replay-saving re-run — spec'd to the builder.
- **ARENA ARTIFACT IDENTITY: RESOLVED (builder, ~18:35-18:45).** The
  flag this section originally raised (arena "wave_ghost" gunnering in
  ~9/20 games vs 1-in-25 on the platform; identical seat-A openings
  across the AB/BA swap) is explained: opp_v67 is GENUINE (fresh
  re-download byte-identical) and **wave_ghost is a fork of OUR Eir 4**
  — 304 diff lines to `_v74e4` vs 2,268 to x3r0's own v89. The
  zero-gunner platform signature is a PRIMARY_SENTINEL selector in the
  fork (first forward turret is a sentinel, later ones gunners, ~l.1570)
  — a conditional path that expresses differently against an Eir mirror
  than against the field. The swap anomaly is shared per-(map,seat)
  opening geometry — one lineage. All measurements stand; the
  interpretation of the field profile flips from "independent
  convergence" to "our lineage minus v65/v66 pieces plus the snipe
  overlay". Sentinel-kill-everywhere remains unconfirmed as the parity
  mechanism; at face value the arena batch favors "strangle too slow vs
  a healing peer economy" (wg-side first sentinels survived most
  archipelago/jackpot/snowflake games). Team decision (Magnus/x3r0):
  v67 keeps the slot; x3r0 grafts I/J/H onto his line next.
- **Tiebreak scoping correction to loss mode 3**: vs our line ~48% of
  head-to-head games reached r1000 and wave_ghost held parity — it IS
  tiebreak-disciplined against a peer economy. The tiebreak auto-loss
  observed vs sporks is conditional on being economically strangled, not
  universal. v66's dump cap being load-bearing in half the head-to-head
  games independently validates the Eir 5.1 tiebreak work.

## Open items

- team lazy 1-4 read: fills the family-split question (this file, below).
- Team 48 5-0 read: from archiver (~18:28 cycle).
- Lorem Ipsum 2-3: NOT read (budget); queue only if the lazy/Team 48 split
  leaves the family question open.
- Handed to builder: none of this gates the slot bar; the SmartFridge
  adaptive-probe flag may deserve a book entry.

## team lazy 1-4 (e71e0b65, all 5 games read — we are seat A here)

lazy's counter is not to kill the sentinel — **in 4 of 5 games our snipe
sentinel survived (or was replaced) and lazy simply won the shot-tempo
race**: 105 / 255 / 502 / 673 gunner fires per game vs wave_ghost's
11-42 sentinel fires. The drip-ammo economy runs the sentinel at ~50-60%
duty cycle, so the chip lands ~5 HP/round — one heal action (+4) nearly
cancels it, and lazy heals while shooting. Kills came at r61/128/152/545.
lazy's own signature, for the book: **convert 12 @ r0**, continuous drip
top-ups (up to 454 converts/game, 2,700 total), gunner-battery finish.

**The exception is the win, and it defines wave_ghost's niche.** g4,
10×10, heavy walls, 623 rounds: lazy fired 502 shots and could not finish
— gunner lines are blocked by terrain on a cramped map, while the ghost
sentinel shoots through it. wave_ghost heal-tanked (both economies were
degenerate — 0 connected chains on either side), then planted a SECOND
sentinel point-blank (dsq 4) at r300 and ground the core down over 300
rounds. wave_ghost beats a family battery only where terrain blocks
gunner sightlines and the game goes very long.

**Family-split verdict (lazy leg):** a healthy family battery does not
need to answer the snipe at all on open maps; the strangle's DPS is below
heal tempo. Why Team 48 v16 nevertheless lost 0-5 remains the open leg —
expected answers: slower battery stand-up, no core-heal discipline, or
sentinel-first target priority walking into the snipe. Confirm from
03af6569 when the archiver lands it.
