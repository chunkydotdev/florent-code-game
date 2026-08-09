# r74 autopsy: CAD dies to our own standard line IF the first core shot lands by ~r13 — after which CAD never builds again

**Side lane, 2026-08-09 17:4x CEST.** Autopsy of `f92f1ca2` game 5 (unrated,
nordkap, us seat a, **our only win of that 1-4 match**): CAD core dead at
**r73** (0-indexed; the "r74" of earlier notes). One opus subagent, zero
downloads, replay + corpus already on disk. **Mechanism language only — no
verdict; verdicts are the builder's.**

**Version tag:** us v92 (`bots/_v115dodge` tree); CAD **v124** (unrated meta —
the four ladder control games are oppver=None, so CAD version drift between
controls and this game cannot be excluded; mitigated by their opening being
behaviourally identical in all five observed nordkap games). Decoders: reused
`tools/replay_census.py` wire primitives + the seat-census Update-field map
(all four corpus traps honoured); damage accounting closes exactly
(28×18 + 21×7 = 651 = 500 HP + 136 healed + 15 overkill); events.tsv
reconciles exactly with the independent decode.

## The kill in one paragraph

Our **standard** fast line — builder walks the shared core column, plants
sentinel at **(10,13)** (v92's signature nordkap seat-a tile: 37 prior ≤r30
plants there in ladder games) — landed at **r11, first shot r12**. From that
round CAD **never executed another build action for the remaining 62 rounds**,
with 30–92 Ti in hand and **195 ammo banked and never fired again** after
their opening gunner died at r7. Their collar heal is a scripted
single-healer rotation capped at 4 HP/round with gaps; against 9 HP/round of
sentinel damage the arithmetic is deterministic: **500 HP → dead in ~60–70
rounds → r73, as observed.** A gunner added at r46 (on (10,15) — the very
tile CAD used for its own counter-gunner in the ladder comparable) trimmed
the tail: final attribution sentinel 504 HP (77%), gunner 147 (23%), our core
took **zero damage all game**, CAD collected **zero titanium all game**.

## Why this game and not the four before it — the control group

Our prior nordkap-vs-CAD plants landed at **r15, r19, r21** — every one met a
CAD **counter-gunner built r16–25** and died within 13–17 rounds, and CAD's
economy completed (conveyor chain finished r13–31, thousands of Ti) and
ground us down (losses r208–559). In the exact seat-a ladder mirror
(`70cb1415` game 3, our v80): CAD counter-built at **r16**, killed our
(10,13) plant by r28, won at r559. **The single variable that flipped in game
5 is plant round: r11 vs r15+.** After first core damage, CAD demonstrably
stops building (game 5: 0 builds r12–73; consistent with the r16 knife-edge
in the control). Their opening script is byte-identical across all five
observed nordkap games: convert 8/8/8 then **all-in 187-Ti ammo dump r4**,
launcher r1 + 4 throws, gunner planted r3, launcher removed r6 (non-damage,
same round every game) — which leaves them at ~66 Ti with an economy that
needs until r13–31 to come online. **The window is theirs by construction;
the question is only whether our first shot beats it.**

Same-day, same-versions contrast (games 1–4, diagonal-core maps): our early
plant lands 3–13 hits and dies to rebuilt gunners; CAD collects 3,300–11,180
Ti and wins at r286/447/644/700. On nordkap's shared-column geometry (11-tile
core gap, mid-map ore on the column, plant tile d²≤32 from their footprint
and walkable by ~r10) the plant simply arrives before the window shuts.

## CAD failure modes observed directly (game 5)

1. **Build paralysis:** zero build actions r12–73 despite affordable rebuilds
   (~24 Ti gunner vs 30–92 on hand).
2. **Ammo freeze:** 195 banked from r10 to game end; no turret ever rebuilt
   to spend it.
3. **Single-healer collar:** exactly one active healer at a time, scripted
   "heal ×4 then step" orbit (three bots traced verbatim), ≤4 HP/round with
   unhealed gaps — vs 9–16 incoming.
4. **No counter-attack:** a CAD builder stood orthogonally adjacent to the
   killing sentinel three separate rounds and never attacked it; another
   walked the map perimeter for 70 rounds doing nothing.
5. **Not CPU/crash:** 0 TLEs, 0 tracebacks, both teams, all five games; no
   unexplained unit loss; spawns unblocked.

## Entity-id turn order — verified in this replay, and it mattered

The within-round stream is id-ascending (INDEX engine fact confirmed here
independently). The decisive race: at r3 our core (**id 1** — seat a holds
it) spawned bot#9 before CAD's builder built gunner#10, so at r4 the fresh
sentinel#12 body-blocked gunner#10's first-ever shot (it hit the 40 HP
sentinel, not our core tile). Seat a wins every same-round creation race by
construction. **Salt/luck component: minimal** — no coinflip-shaped event
found; CAD's opening is deterministic to the tile.

## The pre-registrable prediction (for the builder; ready for a leg prereg)

Conditions: nordkap (or any map with a d²≤32 plant tile walkable by ~r10),
either seat for range (seat a additionally holds core id 1), kill their r3
rush gunner promptly (lane-block sentinel + builder attacks did it by r7 at
zero core damage — also standard v92 behaviour).

- **First core shot ≤ r13** → CAD executes zero build actions thereafter,
  single-healer collar ≤4 HP/round, **core kill ~r70–85 even sentinel-only**.
- **First core shot ≥ r16** → the plant dies ~r28–37 to a counter-gunner and
  the game reverts to their r200+ grind.

This is an **ARRIVAL mechanism, not a speed mechanism** — it moves
core_kill_share vs CAD (ladder: their best-case death vs us r103, median
r194; we'd previously never beaten them on nordkap, 0-4). It is also the
sweep-14 shape: a **trigger, not a dial** — commit to the fast plant when the
geometry qualifies, not unconditionally.

## Adversarial review owed before this becomes a build input

Per the side-lane loop: the lockout hypothesis ("core damage locks CAD's
build branch") is fitted to one game plus one knife-edge control. The
population-level discriminating cut, runnable from the corpus without firing
anything: **across all archived CAD games, first-core-damage round vs CAD
build actions after it** — if the lockout is real, early-damage games show
the paralysis league-wide; if CAD builds fine after early damage elsewhere,
the game-5 paralysis needs another cause. Commissioned from research.

## Could not determine

Launcher r6 removal cause (scripted, not combat — but self-destruct vs
destroy unreadable); CAD's internal gate for the paralysis (intent is not in
a replay — the cut above and/or a test leg falsifies it); no botOutput from
either side; why v92 planted r11 where v80 planted r15 (needs bot-source
diffing, out of scope); CAD version drift between controls and game 5.

## Provenance

Subagent scratch scripts (autopsy.py, trace.py) died with the session by
design; everything they produced is restatable from `tools/replay_census.py`
+ the seat-census field map against the archived replay. Corpus rows:
events.tsv 39 BUILD + 3 DEATH for game 5, reconciled exactly.
