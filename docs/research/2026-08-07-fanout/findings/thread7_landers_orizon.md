# Thread 7 — LANDERS + ORIZON audits

Read-only replay decode, 2026-08-07. 11 replays (10 new downloads), all self-checks green.
Scripts: `SCRATCH/t7/{audit,detail,gates,extra,idle}.py`; raw per-game dump `SCRATCH/t7/all.json`.
Code references are `bots/_v72e2/main.py` (the current Eir-2 line), by line number.

---

## 0. Two corrections to the brief up front

**(a) The Landers "seat-B" framing is a non-effect.** `d9a67e82` is a five-game series in
which we played seat B in **all five** games — 4 losses and 1 win. There is no seat contrast
to read. The same holds for Orizon: `a72b53f9` is all seat B (3L/2W), `c106d3d2` is all seat A
(3L/2W). Orizon kills us in **both seats** by the identical mechanism, so the seat-B
resolution-order tax is not part of either story.

**(b) Map layout is seed-independent — the map NAME fully determines the grid.**
Verified directly: `jackpot` from `d9a67e82` g4 (seed 102387826) and from `c106d3d2` g2
(seed 316137758) — two different series, two different opponents — have **byte-identical wall
sets (50), ore sets (14) and core anchors** ((0,0) / (14,14)). The platform `mapSeed` is a map
*selector*, not a generator. This is the load-bearing fact for probe-worthiness in §4: an
opponent's per-map opening is reproducible from the map name alone.

---

## 1. ORIZON — class verdict: **gunner-only point-blank core battery** (a fifth class; OTHER)

Not a rush, not a chip-siege, not a grind. Orizon (oppv34, unchanged across our v53 → v56 →
v61) plays a single deterministic script:

1. Spawn **exactly 4 builder bots** at r0–r3. Never spawn again (5th appears only in
   snowflake r32 and fjordgate r208). Builder #1 walks **straight at our core from round 0**
   at 1 tile/round.
2. Build 1–4 harvesters and a short conveyor stub. That is the entire economy — and on
   fjordgate it builds **zero harvesters and delivers zero titanium for 350 rounds**.
3. The moment the walking builder is inside gunner range of our core footprint, plant a
   **gunner**. Then keep planting gunners on ever-closer, ever-better-aligned tiles —
   dsq 16 → 9 → 4 → 2 → 1 — one new gunner per firing line. **It almost never rotates**
   (0–3 rotations per game): a fresh gunner adds DPS, a rotation only redirects.
4. Convert titanium to ammo **almost every round, in 4–20 Ti dribbles** (eider 64 convert
   rounds / 93; jackpot 158/213; drumlin 92/173), holding global titanium at 0–60 all game.
   The whole economy is a pump into gunner shots: 116–207 shots per game against our 1–50.
5. Builders park beside their own gunners and **heal them** (3–16 heals/game), so our 2 Ti
   pecks never win the trade.
6. **Zero sentinels, zero launchers, zero barriers. Ever. In all six games.**

Kill mechanism: two or three gunners at dsq 1–9 from our core footprint, 7 dmg each on a
2-round reload, giving a sustained 7 → 14 → 21 HP/round bleed. Our repair line answers +4,
later +8. The core dies 40–280 rounds after the first shot lands. **These are not fast
kills — they are fast STRIKES followed by an unanswered 60-90 round bleed.**

### Orizon timing table

| our ver | map | seat | turns | 1st gunner (rnd@tile, dsq to our core) | creep sequence (dsq) | killer gunner | 1st fire | core dead | launcher |
|---|---|---|---|---|---|---|---|---|---|
| v61 | eider 28x20 | B | 93 | r7 @(16,9) d9 | 9,16,10,**2**,**1**,5 | #62 (18,8) d2 built r32 | r33 | r92 | none |
| v61 | drumlin 25x25 | B | 173 | r19 @(19,14) d16 | 16,16,**9** | #117 (19,15) d9 built r79 | r89 | r172 | none |
| v61 | snowflake 26x26 | B | 115 | r21 @(19,16) d9 | 9,16,9,**4**,**5** | #124 (20,16) d9 built r49 | r50 | r114 | none |
| v56 | jackpot 16x16 | A | 213 | r21 @(4,1) d9 | 9,**4**,**1**,4,13 | #114 (2,1) d1 built r66 | r67 | r212 | none |
| v56 | fjordgate 10x10 | A | 350 | r1 @(5,4) d5 | 5,5,13,13,5,**9** | #18 (3,6) d9 built r8 | r17 | r349 | none |
| v53 | lighthouse 16x16 | B | 91 | r9 @(11,8) d9 | 9,9,16,20,13,**1**,**2** | #69 (12,10) d1 built r41 | r42 | r90 | none |

Cross-version read: **the same mechanism every single time, v53 → v56 → v61, in both seats.**
Nothing in three of our major revisions changed the shape of the loss — only its length.
Orizon has not adapted; we simply have no answer.

### Money question: is our rush defense not triggering, or overwhelmed? — **Not triggering.**

It fires *once*, in the opening, and is then structurally locked out for the rest of the game.

**Failure 1 (primary): the universal adjacent heal claims every core-adjacent builder's
action for the entire siege, and it sits ABOVE role dispatch.**
`bots/_v72e2/main.py:991-993`:

```python
if ct.get_action_cooldown() == 0 and ct.read_store(SLOT_UNDER) != 0:
    if self._heal_core(ct):
        return
```

`_builder` dispatches roles only at :1064-1071, *after* this. So under an Orizon siege
(SLOT_UNDER latched, core below max HP, builders converged on the footprint) no builder
reaches `_defend` (:1722) and therefore no builder reaches `_try_counterbattery` (:1641).
The only other call site, `_home_defend`:1077, is unreachable for home builders: it is gated
at :1035 on `self.role in ("saboteur", "launchwait")` — forward raiders only.
`_defend`'s own path repeats the same ordering at :1771-1777 (`if shelled and
self._heal_core(ct)` short-circuits before `or self._try_counterbattery(ct)`).

Measured consequence — eider r24→r92, verbatim from the trace: `coreheal+4` on **every single
round**, zero turret builds, titanium climbing 94 → 253 unspent, 24 ammo banked, one shot
fired all game. Our sentinel #18 (built r8 at dsq 4 — the one counterbattery that *did* fire)
died at r11 and was **never replaced for 81 rounds**.

Capability-idle measurement (rounds with our core bleeding, ≥1 builder alive, **zero** turrets
alive):

| game | idle rounds | peak Ti while idle | ammo idle rounds (≥10 ammo, no gun) | first HOME turret |
|---|---|---|---|---|
| eider | 68 / 68 | 253 | 68 | r8 (dies r11) |
| lighthouse | 44 | 53 | 36 | r9, r10 (both die) |
| jackpot v56 | 71 | 76 | 54 | **r192** (killer started r67) |
| meander (Landers) | 55 | 284 | 52 | r6 (dies), next r126 |

**Failure 2: `SLOT_HOME_GUN` is monotone.** It is incremented at :1313, :1699 and :1703 and
**never decremented when the turret dies**. The counterbattery eco-gate at :1650
(`if ct.read_store(SLOT_HOME_GUN) >= 1 and harvesters < ECO_NEED: return False`) therefore
treats a battery that has been rubble for 80 rounds as a live one. The `_core_shelled` waiver
rescues this in principle — but Failure 1 means the code path is never reached anyway.

**Failure 3: turret hunting cannot engage — the round floor is longer than the game.**
`HUNT_MIN_RND = 120` (:215), enforced at :1497. Game lengths: eider 93, snowflake 115,
lighthouse 91. **In three of six Orizon games the hunt system is arithmetically unreachable.**
In the other three the killer gunner opens fire at r17/r67/r89 — 30–100 rounds before the
floor. `HUNT_BAND_DSQ = 41` would have covered every one of these turrets (all dsq 1–9), and
`HUNT_MIN_HEALERS = 2` would have been satisfied (2–5 builders alive at first fire in every
game). **The band and the healer floor are both fine. The clock is the whole problem.**

**Failure 4: builder respawn never fires.** `REPLACE_TI_FLOOR = 250` (:54) ∧
`REPLACE_MIN_RND = 60` (:55), enforced at :684. Max titanium after r60: eider 253 (crosses at
r74 — 60 rounds after our first builder died), drumlin 161, snowflake 63, jackpot 76,
fjordgate 44, lighthouse 43. **The floor is never met in 5 of 6 games**, because Orizon's
siege *is* an economy denial: our bank never gets rich while it is being shot.

**Failure 5: chain medic dead by clock.** `MEDIC_MIN_RND = 150` (:184, used :1930) — dead in
eider/snowflake/lighthouse (91–115 turns).

**Did any Eir-era system engage at all?** Ammo latch: yes, and it is the one that works —
`SLOT_ATK_RND` latches, `ammo_target = 24 if under` (:630), and we duly bank 20–32 ammo. It is
pure dead capital: we have no turret to spend it from. Escort disengage: never triggers (no
escorted forward building survives long enough). Counterbattery: exactly one build per game,
in the opening, before the heal lock closes. **Net: the ammo latch is the only Eir system that
runs, and it banks ammunition for guns that do not exist.**

Secondary failure mode, where we *did* hold a home gun (drumlin r36, snowflake r21): we get
**out-traded**. Their builders heal their gunners (drumlin 16 heals) while ours are 2-Ti
pecking; we lose 3 gunners + 1 sentinel in drumlin, and their killer #117 is planted **on the
exact tile (19,15) where our own gunner #67 had stood**. Our 21–22 shots against their 120–167.

---

## 2. LANDERS — class verdict: **patient grind** (economy strangle by melee builders +
single late execution turret)

Landers (oppv62) is the textbook grind fingerprint, with one twist worth naming: **the
strangle agent is builder bots, not turrets.**

- Landers fields **7–11 live builders, growing over the match** (atoll 7→11, nordkap 5→9,
  jackpot 8→10) against our fixed 3–5 and falling.
- Damage to our economy is overwhelmingly **melee builder pecks**, not gunfire:
  atoll 498 builder hits vs 14 gunner; jackpot 145 vs 17; nordkap 95 vs 49; meander 55 vs 25.
  We lose 38 conveyors on atoll, 18 conveyors + 4 harvesters on nordkap.
- Damage to **our builders** is the opposite — almost all gunner (11/20/33/13 hits) — so the
  two arms are specialised: builders eat the economy, guns eat the hands.
- Their opening turrets are **defensive, at their own base** (atoll r20 sentinel at dsq 225).
- They heal their own core heavily (32/95/94/**253** heals) — a heal-tank.
- **Zero launchers in all five games.**
- The kill is a *single* gunner or sentinel walked to dsq 4–16 of our core, **late**, which
  then chips unanswered for 70–100 rounds.

### Landers timing table (`d9a67e82`, all seat B)

| game | map | turns | 1st EN turret | 1st turret inside dsq 41 | killer | built | 1st fire | core dead | dmg | our heals |
|---|---|---|---|---|---|---|---|---|---|---|
| g1 L | atoll 18x18 | 642 | r20 sent d225 (home) | **r428** sent d40 | sentinel #768 (14,7) d16 | r548 | r549 | r641 | 846 | 85 (+340) from r557 |
| g2 L | meander 25x15 | 243 | r3 sent d16 | r3 | gunner #416 (9,12) d5 | r160 | r164 | r242 | 553 | 183 (+651) |
| g3 L | nordkap 20x26 | 411 | r9 gun d37 | r9 | gunner #456 (11,16) d5 | r332 | r336 | r410 | 504 | **0** |
| g4 L | jackpot 16x16 | 344 | r26 gun d117 | **r253** | gunner #445 (12,14) d4 | r271 | r278 | r343 | 441 | 7 (+26) |
| g5 W | moonrise 21x8 | 207 | r7 gun d9 | r7 | (we won @r207) | — | — | — | — | 161 (+585) |

Atoll is the sharpest one: **we out-delivered them 3990 to 3190 and still lost** to one
sentinel planted at r548.

### Our failure point (Landers)

Not the same as Orizon. The gates that matter here are **manpower**, not the clock — every
killer fires well past `HUNT_MIN_RND = 120` and every killer sits inside `HUNT_BAND_DSQ = 41`.

- **nordkap is the pure case: `healers@first-fire = 0`.** All five of our builders were dead
  by r172; the killer landed at r332. Zero core heals *ever* in that game, 735 Ti unspent at
  the bell, 24 ammo banked, zero turrets alive. `HUNT_MIN_HEALERS = 2` (:148, enforced :1610)
  cannot be satisfied by an empty roster, and neither can the repair line.
- **jackpot is the respawn gate failing:** builders die r242/243/277, killer lands r253 —
  and `REPLACE_TI_FLOOR = 250` is **never** met (max Ti after r60 = 61). No replacement is
  ever legal. We finish with 22 Ti and one turret.
- atoll and meander both satisfy the respawn floor (Ti crosses 250 at r86 / r231) and both
  have exactly 2 healers at first fire — i.e. the current line's hunt would be *eligible*
  there. Those two are the games the Eir machinery might genuinely have changed; nordkap and
  jackpot it could not.
- The `_home_defend` role gate at :1035 bites here too: Landers parks a melee builder at dsq 1
  from our core for 80+ consecutive rounds (meander r20–r100, nordkap r60–r120) eating our
  economy, and only a `saboteur`/`launchwait` unit is allowed to answer it.

---

## 3. Cross-version read (Orizon, v53 → v56 → v61)

Same mechanism every time; no adaptation on their side, no improvement on ours.

| | v53 (lighthouse, B) | v56 (jackpot A / fjordgate A) | v61 (eider/drumlin/snowflake, B) |
|---|---|---|---|
| their opening | 4 bots r0-3, walk at core | identical | identical |
| first gunner | r9, dsq 9 | r21 dsq 9 / r1 dsq 5 | r7/r19/r21, dsq 9-16 |
| creep to dsq ≤2 | r41 | r66 / — | r32 (eider) |
| sentinels/launchers/barriers built | 0 | 0 | 0 |
| our home battery | 2, both dead by ~r20 | 1 @r192 / 3 early, all dead | 1 @r8 dead r11 (eider); 1-3 held (drumlin/snowflake) |
| our counterbattery rebuilds | 0 | 0 | 0 |
| our respawns | 0 | 0 | 2 (eider only, r75/r91) |
| ammo banked, unspendable | 24 | 32 | 24 |

The only thing that moved across three revisions is *how long the bleed takes*.

---

## 4. Probe-worthiness

**Orizon: YES — the strongest probe candidate seen so far, stronger than cad_probe.**

Evidence for determinism: (a) map grids are fixed per map name, proven byte-identical across
seeds and series (§0b); (b) the brief's own observation that lighthouse-91t and drumlin-164t
recur with *identical turn counts* in different series confirms both bots are deterministic
given (map, seat); (c) our own v53 drumlin runs are 164 turns in two series while v61's is 173
— i.e. the divergence is entirely ours, their script is invariant.

What the probe should do, concretely — a frozen `orizon_probe` in `bots/`:

1. **4 builders at r0-3, no further spawns.** Never raise the labour force.
2. Builder #1: nav straight at the enemy core from round 0, ignoring everything.
   Builders #2-#4: 1-3 harvesters + a short conveyor stub, then follow.
3. On arrival, plant a **gunner** on the first legal tile whose facing ray contains an enemy
   core footprint tile. Then, every time titanium allows, plant **another** gunner on the
   next-closest aligned tile. Never rotate. Never build sentinel/launcher/barrier.
4. Park a builder orthogonally adjacent to each gunner and heal it whenever it is damaged.
5. Core: convert titanium to ammo **every round**, `amount = min(ti - small_floor, 20)`.
   Hold no titanium reserve at all.

That probe is worth more than a scoreboard entry: it is the **instrument that tells us whether
a fix to the heal lock actually works**, because the failure it reproduces (our repair line
soaking 100% of builder actions while a point-blank battery outruns it) is exactly the one
Ouroboros also exploits.

**Family note (hypothesis, flagged not proven):** Orizon's signature — gunner-only, no
sentinels/launchers/barriers, deterministic per-map opening, creeping plant sequence — is the
same signature the brief attributes to Ouroboros ("gunner-only creeping picket, deterministic
per-map openings"). The difference may be only the aim point: Orizon aims the creep **at our
core footprint** (dsq 1-9), a picket aims it at a line. If they are one class, then a single
fix retires **two** of the six nemeses, and Ouroboros — the known leak — is the same problem
we have measured six times here. Worth one cheap cross-check before any fix is scoped.

**Landers: NO as a frozen opening probe, YES as an attrition harness.** Its behaviour is
adaptive and map-dependent (turrets at home on atoll/jackpot, forward from r3 on meander), and
the kill round ranges r242-r641 — nothing tight enough to freeze as a fingerprint. What *is*
worth freezing is its **strangle arm** alone: a probe that spawns 8-10 builders and does
nothing but walk them into our economy and melee-peck harvesters and conveyors, never building
a turret. That isolates the one variable Landers actually beats us on — builder count and
economy durability — without the noise of the execution turret, and it would directly
exercise the `REPLACE_TI_FLOOR = 250` gate that failed in jackpot and nordkap.

---

## 5. One-paragraph roll-up of the shared root cause

Both teams win by putting **sustained low damage on our core from inside dsq 41 while our
builders stand next to it**. Our answer to that is a +4 HP/round repair reflex that is wired
*above* every other builder branch (:991), so under exactly the conditions that call for a
counterbattery or a hunt, we spend 100% of our builder actions on heals we cannot win with —
eider is +344 HP against 847 damage; jackpot v56 is +669 against 1169; meander is +651 against
1157. Meanwhile the two systems designed to break a siege are locked behind clocks
(`HUNT_MIN_RND = 120`, `MEDIC_MIN_RND = 150`) that are longer than half these games, and the
system designed to replace the hands that would run them is locked behind a bank floor
(`REPLACE_TI_FLOOR = 250`) that a strangled economy never reaches. Every gate is individually
well-argued in the source comments; the failure is that they are all conditioned on *time* or
*wealth*, and a point-blank battery denies us both.
