# archipelago seed 1 seat B — who owns hsd's r732 loss?

**Research-arm decode, 2026-08-08.** Answers the open question left by the
REV-SCOPE ANNOTATION in `docs/research/v85hs-mechanism-read-2026-08-08.md` §A.1
("hsd's residual archipelago-b loss (r732) has an **UNIDENTIFIED owner**").
Measurement and attribution only; no games run, no bot files touched.

> ## VERDICT
>
> **Channel (iii) — THE IDLE RESERVE.** From **r251 to r731** the game is a
> frozen limit cycle in which our core takes **exactly 9 HP/round** (enemy
> gunner `#195` @(21,18) 7 + enemy builder `#3` squatting our heal seat (18,20)
> 2) and heals **exactly 8 HP/round** (two permanently pinned builders, `#6`
> @(20,21) and `#12` @(19,21)), bleeding **−1 HP/round for 480 consecutive
> rounds** — while the other **three of our five builders do nothing at all**
> (`#4` immobile at (9,10) since r36; `#8` and `#10` pacing 1-tile 2-cycles on
> unbuilt ore tiles), **five of eight heal seats stand free**, and a perfect
> 4-round income/spend cycle pins the bank at **8-20 Ti**, two titanium below
> the **22 Ti** harvester that is the only exit.
>
> It is **not** channel (i) recurring (no own or enemy impassable building is
> ever on a seat: 0.00 seat-tile-rounds all game) and **not** channel (ii)
> recurring (no builder of ours is seat-captured off an expansion job; `#6`/`#12`
> were already inert in hsb before H1 recruited them). It is the **same terminal
> pattern as hsb, arriving 455 rounds later at one notch higher staffing**:
> incoming is ~9 HP/round in both games; H1 raised our heal from ~4 to 8; 8 < 9.

| | |
|---|---|
| Primary replay | `scratchpad/archb_decode/archipelago_b_hsd_off.replay26` md5 `a07c277f55819de42df54fed08cee2f5` — **the hse inert-check leg, byte-identical to hsd** per the s16 09:14 verdict (NOISE_OFF, `--tle 0`) |
| Candidate | `bots/_v85hsd/main.py` md5 `4a2aeb50ef8ff63ea55ddc25baca2628` (**4a2aeb50**) = **hsd** = live **v75 "Eir 8"** |
| Opponent / parent | `bots/_v84g/main.py` md5 `cbb0b8b449110f89be9765028fbf8c54` — shipped as v73 "Eir 7", seat A |
| Contrast replay | `h85_archipelago_1_b.replay26` md5 `3632994b7c4426e77ebfec8ab72af10c` (hsb lineage, core dead r277) |
| Outcome decoded | winner **A**, `core_destroyed`, **732 turns**; ours 2,040 Ti mined / 18 banked, theirs 3,610 / 40 |
| Tooling | purpose-built state machine on `tools/replay_census.py` primitives (`scratchpad/archb_decode/decode.py`, `analyse*.py`, `selfcheck.py`); `tools/replay_schema.md` is ground truth |
| Channel discipline | every number below is from `.replay26` wire events. The `fcode` stdout sidecar was read once, for the headline outcome only. Zero `botOutput` stdout records in either game. |

---

## 1. The terminal object: a 480-round frozen limit cycle

The endgame is not a collapse. It is a **perfectly periodic steady state** that
runs for two thirds of the match and ends when the arithmetic runs out.

Per-round HP change of our core, **r252-r731** (480 rounds):

| ΔHP per round | rounds |
|---|---|
| **−1** | **479** (r252-r730, every one) |
| −2 | 1 (r731, the kill round: 2 damage lands, the +8 heal never does) |
| ≥ 0 | **0** |

`hp[251] = 481` (r251 is the last net-positive round, +6), `hp[731] = 0`.
**481 HP lost over 480 rounds, with not one round of net recovery.** The damage
composition is identical in all 479 of the −1 rounds:

```
one  -7  event   (fireTurret (21,18) -> (20,19)   enemy gunner #195)
one  -2  event   (builderAttack A#3 -> (19,20)    enemy builder on our seat (18,20))
two  +4  events  (builderHeal B#6 -> (20,20), builderHeal B#12 -> (19,20))
                                              ------------------------------------
                                              net  -1 HP / round
```

Everything else is frozen too. Positions from **r200 onward** (532 rounds,
end-of-round census):

| unit | tile(s) held | rounds | what it does |
|---|---|---|---|
| **B `#6`** | (20,21) | 531/532 | heals (20,20) **every round** — 683 heals lifetime, 644 on the core |
| **B `#12`** | (19,21) | 531/532 | heals (19,20) **every round** — 611 heals lifetime, 596 on the core |
| **B `#4`** | (9,10) | **532/532** | **nothing. Last action r37, last move r36.** |
| **B `#8`** | (17,8)↔(17,9) | 266/266 | **moves every round, acts never. Last action r108.** (17,9) is an **ore tile** |
| **B `#10`** | (23,17)↔(23,16) | 266/266 | **moves every round, acts never. Last action r35.** (23,17) is an **ore tile** |
| A `#3` | **(18,20) — our heal seat** | 532/532 | attacks (19,20) **every round**; on that tile since **r86** |
| A `#7`, A `#11` | (4,6)/(7,5) area | — | the enemy's two core healers, 564 + 483 heals |
| A `#5`, A `#9` | 2-cycles | — | the enemy's own idle pair — **the livelock is a shared v73 trait, not an hsd regression** |

**Three of our five builders (60% of the army) contribute nothing for the last
~600 rounds**, and two of them burn every single round on a one-tile
oscillation while standing on ore they never harvest.

---

## 2. Causal chain, stated in replay events

1. **r19 — our conveyor `#55` is built on heal seat (20,18)** by `#8`. It
   survives the whole game (20/20 HP at r731). Conveyors are **bot-passable**
   (measured: **2,313 builder-on-conveyor tile-rounds** in this game), so this
   costs us nothing in seats — and it **denies the enemy the seat-planted gunner
   that killed hsb** (see §5). Positive, and worth keeping.
2. **r29, r31 — our sentinel `#64` @(14,18) hits enemy builder `#3` twice for
   18.** `#3` drops to **4/40 HP** and stays there for the remaining **700
   rounds**. It is never touched again.
3. **r36 — our home sentinel `#83` goes up at (18,18), off the ring** (the
   `HS_SEAT_PROTECT` turret gate at `:3258` is armed in hsd, so the ring tile
   (19,18) is refused — channel (i) is still live as a *placement* fact).
   **`#83` dies at r41.** From r41 to the end we hold **no turret within 100
   tiles of our own core**; the only turret we own is the forward sentinel `#85`
   @(9,9), built r37, parked next to the *enemy* core.
4. **r35 / r37 — `#10` and `#4` take their last actions.** `#4` takes its last
   *move* at r36 and is immobile for 695 rounds.
5. **r66 — the enemy throws its saboteur.** Launcher `#29` @(5,7) throws builder
   A `#9` from (4,6) to **(8,11)**, d²=41 — the **only** launcher throw in the
   game (`moveBuilderBot` with d²>1: exactly 1 event). Everything that follows in
   steps 7-9 is that one thrown builder's work. This is the same
   launcher-throw-geometry mechanism §2 of the prior read named on
   `archipelago_1_a`, here pointed at us.
6. **r86 — enemy builder `#3` steps onto our heal seat (18,20) and never
   leaves.** 679 attacks lifetime, **644 of them on core tile (19,20)** =
   **1,288 HP**. We cannot answer it: builder attacks always hit the *building*
   on a tile, never the bot (0 bot-hits in 5,990 builder attacks across the
   prior corpus), so removing `#3` needs a turret — and we have none and cannot
   afford one (step 10).
7. **r101-r153 — the saboteur cuts half our economy, and it is never repaired.**
   `#9` destroys conveyors `#82` @(21,17) r101, `#40` @(20,16) r111, `#92`
   @(21,16) r122, `#47` @(20,17) r132, `#31` @(20,15) r153 (55 builder attacks) —
   the spur carrying harvester `#17` @(19,14). Delivery **source tiles** into our
   core footprint prove the severance exactly:

   | window | via (20,18) — harvester `#17` | via (21,20) — harvester `#24` |
   |---|---|---|
   | r0-99 | **21 stacks** | 21 |
   | r100-199 | **4** | 25 |
   | **r200-731** | **0, for 532 rounds** | 25 per 100 r, unchanged |

   From r~110 we run on **one harvester**: 10 Ti per 4 rounds, which with the 10
   Ti passive is precisely the 20 Ti/4-round budget of step 10. Three conveyors
   at **3 Ti each** would restore it, and the bank touches 20 Ti every fourth
   round. **Not one of them is ever rebuilt in 578 rounds.**
8. **r108 — `#8` takes its last action** (conveyor `#173` @(20,12), an
   unfinished link) — the round after the second conveyor of its own spur died.
   Our **last harvester was built at r11**. Final harvester count **2** (`#17`
   @(19,14), now orphaned, and `#24` @(23,19)) against the parent's **4**.
9. **r133 — that same thrown builder `#9` builds gunner `#195` @(21,18)**, corner-diagonal to our
   core (d²=2 to (20,19)), *off-seat* so no seat logic of ours bears on it.
   It fires **582 times, every shot at (20,19)** = **4,074 HP**, 72% of all
   damage our core ever takes. It is **orthogonally adjacent to two of our
   permanently free heal seats**, (21,19) and (20,18) — 25 HP, 13 builder
   attacks, 26 Ti to grind down. **No unit of ours ever attacks it in 598
   rounds.**
10. **r~200 onward — the liquidity trap closes.** Income and spend lock into a
   4-round cycle (measured r250-r731, identical every cycle):

   ```
   income  10 Ti passive  +  10 Ti (one delivery stack)   =  20 Ti / 4 rounds
   spend    8 Ti heals (2/round)  +  12 Ti convert_ammo    =  20 Ti / 4 rounds
   bank     20 -> 10 -> 8 -> 16 -> 20 ...   min 8, max 20, mean 13.5
   ```

   **The bank never reaches 22 Ti** — the scaled harvester price at 2 live
   harvesters (`floor(1.10 × 20)`). It is **2 Ti short, forever**, which is why
   `#8` and `#10` stand *on* ore tiles for 530 rounds and never build. Every
   turret price at this scale is ≥2× the 20 Ti ceiling, so the counterbattery in
   step 9 is also priced out.
11. **The ammo half of that spend buys nothing.** We convert **2,339 Ti** to
   ammunition (**~60% of the 4-round budget**) to feed sentinel `#85` @(9,9):
   **227 shots × 18 = 4,086 HP on the enemy core — and the enemy heals exactly
   4,086.** Their core finishes at **500/500**. Net effect of our entire
   offensive budget over 732 rounds: **zero**.
12. **r251-r731 — the bleed runs to completion.** 9 in, 8 out, −1/round,
    core dead at **r732**.

**Closing identity (both games):** total core damage − total core heal = **500**
= exactly the core HP pool. hsd: 5,665 − 5,165. hsb: 1,213 − 713.

---

## 3. Quantitative tables

### 3.1 Economy timeline (titanium delivered into the core footprint, per 100 rounds)

| window | A (parent) | **B (hsd)** | our bank at window end | our harvesters | our spawns |
|---|---|---|---|---|---|
| r0-99 | 450 | **420** | 21 | 2 (r9, r11) | 5 (all opening, r0-r4) |
| r100-199 | 500 | **290** | 16 | 2 | 0 |
| r200-299 | 500 | **250** | 16 | 2 | 0 |
| r300-399 | 500 | **250** | 16 | 2 | 0 |
| r400-499 | 500 | **250** | 16 | 2 | 0 |
| r500-599 | 500 | **250** | 16 | 2 | 0 |
| r600-699 | 500 | **250** | 16 | 2 | 0 |
| r700-731 | 160 | **80** | 18 | 2 | 0 |
| **total** | **3,610** | **2,040** | — | **2** | **5** |

Steady-state (r250-r731): delivery **2.49 Ti/round**, ammo conversion **2.99
Ti/round**, bank **8-20 Ti** (mean 13.5). Post-opening spawns: **0** — the
ceiling lift never fires because the bank never affords a 6th builder.

**All of the r200+ delivery arrives through a single tile, (21,20), from a
single harvester** (`#24` @(23,19)): 25 stacks per 100 rounds, i.e. one stack
per 4 rounds, forever. Our other harvester `#17` @(19,14) is alive at 30/30 HP
and orphaned — its route was cut r101-r153 (§2 step 7) and it delivers **0
stacks in the last 532 rounds**. The parent's 500/100 r is two live routes; ours
is one.

### 3.2 Heal vs. incoming DPS at the core

| window | our core: damage | heal HP | HP at end | ratio | enemy core: damage | heal HP | HP at end |
|---|---|---|---|---|---|---|---|
| r0-99 | 327 | 327 | 500 | 1.00 | 540 | 288 | 248 |
| r100-199 | 606 | 590 | 484 | 0.97 | 684 | 796 | 360 |
| r200-299 | 851 | 800 | 433 | 0.94 | 540 | 674 | 494 |
| r300-399 | **900** | **800** | 333 | **0.889** | 540 | 540 | 494 |
| r400-499 | **900** | **800** | 233 | **0.889** | 540 | 536 | 490 |
| r500-599 | **900** | **800** | 133 | **0.889** | 540 | 540 | 490 |
| r600-699 | **900** | **800** | 33 | **0.889** | 540 | 544 | 494 |
| r700-731 | 281 | 248 | **0** | 0.882 | 162 | 168 | 500 |
| **game** | **5,665** | **5,165** | — | **0.912** | 4,086 | 4,086 | 500/500 |

The symmetry is the point: **both teams field exactly two core healers (8
HP/round of capacity).** Theirs is enough because their incoming is 5.4/round;
ours is not because ours is 9.0/round. The 3.6 HP/round gap is *entirely*
builder `#3`'s free melee (1,288 HP) plus the point-blank gunner's higher uptime
— **not** an ammo-efficiency gap (A: 2,584 Ti → 4,305 HP = 1.67 HP/Ti; B: 2,339
Ti → 4,086 HP = 1.75 HP/Ti; we are the *more* efficient shooter).

Bimodal-law placement: **0.912** — inside the 0.86-0.94 gap the prior read
flagged, resolving to **death** because the episode's net damage (500) exactly
consumes the HP buffer. This is the sharpest gap-zone data point in the corpus
so far and it tightens the threshold to **> 0.912**.

### 3.3 Heal-seat ledger (conveyors/splitters correctly treated as **passable**)

Seats of core (19,19): (18,19) (18,20) (19,18) (19,21) (20,18) (20,21) (21,19) (21,20).

| window | free seats (mean) | our bots on seat | enemy bots on seat | seats blocked by an **impassable** building |
|---|---|---|---|---|
| r0-99 | 6.34 | 1.52 | 0.14 | **0.00** |
| r100-199 | 5.17 | 1.83 | 1.00 | **0.00** |
| r200-299 | **5.00** | **2.00** | **1.00** | **0.00** |
| r300-399 | **5.00** | **2.00** | **1.00** | **0.00** |
| r400-499 | **5.00** | **2.00** | **1.00** | **0.00** |
| r500-599 | **5.00** | **2.00** | **1.00** | **0.00** |
| r600-699 | **5.00** | **2.00** | **1.00** | **0.00** |
| r700-731 | 5.06 | 1.94 | 1.00 | **0.00** |

**Five seats free, every round, for 530 rounds, with three idle builders on the
map.** The nearest of them, `#10` @(23,17), is **5 Manhattan steps** from free
seat (21,20). Own-impassable-on-seat is **0 all game** (channel (i)'s garrison
metric is at its floor) and enemy-impassable-on-seat is **0 all game** (the
seat-planted gunner that killed hsb never happens here).

### 3.4 Core damage attribution, whole game

| source | events | HP | share |
|---|---|---|---|
| gunner `#195` @(21,18), r133-r731 | 582 shots × 7 | **4,074** | **71.9%** |
| builder `#3` melee from seat (18,20), r86-r731 | 644 attacks × 2 | **1,288** | **22.7%** |
| gunner `#72` @(17,17), gunner `#118` @(16,20) (both killed r59/r90 by our `#12`) | 33 × 7 | 231 | 4.1% |
| sentinel `#58` @(16,16) (killed r27) | 4 × 18 | 72 | 1.3% |
| **total** | | **5,665** | 100% |

Our own counterbattery **does work when it is affordable and in reach**: `#12`
attacked (16,20) 13 times and (17,17) 4 times, and both of those gunners died.
It simply never happens again after r133.

---

## 4. Where this lives in the source (secondary to the events above)

The three idle builders are never recalled because **every path to the heal ring
is gated on the core being in the walker's own vision (r²=20) and on the walker
holding role 4**:

* `_core_shelled` — `bots/_v85hsd/main.py:3008`. Scans `get_nearby_buildings()`
  for our core; its own docstring says *"Out of vision returns False"*. `#4` is
  at d²=**181** from the core, `#8` at d²=**104**. They are structurally blind
  to the siege.
* `_free_seats` — `:2747`, with the hard `is_in_vision(s)` gate at **`:2768`**:
  a seat we cannot see "counts as NOT free". At d²>20 the list is always empty.
* `_seat_seek_target` — `:2778`; returns `None` on an empty `free` (`:2797`),
  and the seeker cap at **`:2815`**.
* Call sites: `_defend` no-threat fallback `:2289` (guarded by
  `_core_shelled`); the defender come-home walk **`:3463`**, guarded by
  `shelled and self.role_n == 4`; the second come-home `:3687`. **A builder that
  is not role 4, or cannot see home, is never a candidate healer at all.**
* H1's sticky halves, `:2824-2833` — *"a unit standing on a seat stops seeking;
  a walker holds its chosen seat while that seat stays free."* This is what pins
  `#6` and `#12` for 531 rounds and is the reason survival stretched from r277
  to r732. It works. It just recruits **from the same blind, role-gated pool**,
  so it converts 1 healer into 2 and cannot reach 3.
* `HS_SEEK_BAND_DSQ = 20` — `:638`. The recruitment band is one builder vision
  radius.

The 2 Ti harvester lockout is a cost-scale fact, not a code branch: with two
live harvesters `get_harvester_cost()` = `floor(1.10 × 20)` = **22**, and the
4-round bank cycle tops out at **20**.

---

## 5. Contrast with the hsb r277 loss — same pattern, one notch later

| | `h85_archipelago_1_b` (hsb, dead **r277**) | `archipelago_b_hsd_off` (hsd, dead **r732**) |
|---|---|---|
| our builders on a heal seat (steady state, mean) | **0.99** | **2.00** |
| core heal actions / heal HP | 209 / **713** | 1,315 / **5,165** |
| core damage | 1,213 | 5,665 |
| **heal / damage ratio** | **0.588** | **0.912** |
| damage − heal | **500** | **500** |
| incoming DPS in the terminal window | 682 HP / 77 r = **8.9/round** | 900 HP / 100 r = **9.0/round** |
| enemy turret **on** a seat | **gunner @(20,18) from r175** (our conveyor `#55` there died r174) | **never** — `#55` survives to r731; their gunner goes to (21,18), off-seat |
| enemy bots on our seats (steady) | 1.00 (`#3`, plus `#9` for 66 r) | 1.00 (`#3`) |
| our harvesters / delivery | **5** / 1,280 Ti in 277 r | **2** / 2,040 Ti in 732 r |
| our lifetime builders | 6 (one post-opening spawn, `#163`) | 5 |
| `#6` / `#12` | **inert** — last actions r43 / r68 | **the two permanent healers** |

Read the first and last rows together: **H1 rescued exactly two builders from
the v73 livelock and turned them into permanent healers.** That is a real,
measured, positive effect — heal throughput ~4 → 8 HP/round, ratio 0.588 →
0.912, survival +455 rounds. Incoming DPS is **the same ~9/round in both
games**, so the only reason hsd still loses is that **8 < 9**.

**Answer to the framing question: this is the SAME terminal pattern arriving
later, at higher staffing — the v73 convergence signature ("seats free, no
bodies") re-expressed as "seats free, not enough bodies".** It is neither a
recurrence of channel (i) (0.00 impassable-on-seat tile-rounds for either side,
all game) nor of channel (ii) (no builder of ours is captured off an expansion
job; `#6`/`#12` had no expansion job to lose).

*Cascade caveat:* the two replays share map, seed, seat and opponent binary but
diverge early, and the **parent's own line differs between them** (4 harvesters
and 5 builders here vs 5 and 8 there). Cross-game economy deltas are therefore
cascade-affected and should not be attributed to H1 on their own. Every
attribution in §1-§2 is *within* the hsd game.

---

## 6. Contributing channels, ranked

| rank | channel | evidence | HP/round it is worth |
|---|---|---|---|
| **1 (owner)** | **Idle reserve — heal ring staffed at 2 while 3 builders livelock and 5 seats stand free** | §3.3, §1 position census; `#4` immobile 532/532 r, `#8`/`#10` 2-cycling 266/266 r | **+4** (one more healer flips −1 → **+3**) |
| 2 | **Unanswered point-blank gunner `#195` @(21,18)** | 582 shots, all at (20,19), 4,074 HP; adjacent to two free seats; never attacked in 598 rounds | **−7** if removed (26 Ti of builder attacks) |
| 3 | **Invulnerable seat squatter `#3` @(18,20) at 4/40 HP** | 644 core attacks = 1,288 HP; at 4 HP since r31; builder attacks cannot hit bots, and we hold no home turret after r41 (channel (i) residue: gate pushes our r36 sentinel off the ring to (18,18), it dies r41, no rebuild) | **−2** if removed (one gunner shot) |
| 4 | **Severed delivery spur never repaired** | harvester `#17`'s route dies r101-r153 to the saboteur's 55 attacks; source-tile ledger shows (20,18) delivering **0 stacks for the last 532 rounds**; a conveyor costs **3 Ti** against a bank that touches 20 every 4th round | doubles income (2.5 → ~5 Ti/round) |
| 5 | **Liquidity trap: bank capped at 20 Ti vs a 22 Ti harvester** | 4-round cycle 20→10→8→16, r250-r731; last harvester r11; `#8`/`#10` standing *on* unbuilt ore | gates ranks 2-4 |
| 6 | **Zero-yield ammo burn: 2,339 Ti → 4,086 HP → enemy heals 4,086 → net 0** | enemy core finishes 500/500; their heal capacity 8/round against our 5.6/round of sentinel fire | frees ~3 Ti/round, i.e. all of rank 5 |

Ranks 5 and 6 are the same loop seen from two ends: **60% of our income buys an
offensive channel that is provably cancelled 1:1, and that spend is exactly what
holds the bank 2 Ti below the harvester that would end the stalemate.** Rank 4
is the cheapest single fix on the board — 9 Ti of conveyor, affordable in any
4-round cycle from r153 onward, and never attempted.

**Why the owner is rank 1 and not the economy.** Ranks 2-6 are all *sufficient*
fixes, but they are also all things the parent did to us; rank 1 is the only one
that is a property of our own file and is the one the hs plank exists to
control. More decisively: the enemy's core takes 5.4 HP/round and heals 5.4 with
the same two-healer establishment we have. **We lose because our defence is
sized to two healers regardless of what is arriving**, and the arithmetic says a
third body — costing 1 Ti/round out of a 5 Ti/round budget — turns −1 into +3
without touching the economy at all.

---

## 7. Falsifiable predictions — what a fix must change in a re-run replay

State the fix, then the replay signature. All are checkable with
`scratchpad/archb_decode/analyse3.py` on a re-run of the same map/seed/seat with
NOISE_OFF.

**Fix A — conscript a third healer** (relax the `role_n == 4` and/or vision gate
so a builder outside r²=20 can be recalled when the core is bleeding; e.g. a
store-slot "core bleeding" broadcast):

1. `ourBots` on seat, r250+, goes **2.00 → ≥ 3.00**; `free` goes **5.00 → ≤ 4.00**.
2. Core heal HP per 100 r goes **800 → ≥ 1,200**; the per-round ΔHP histogram
   loses its 479 `−1` entries and gains net-positive rounds.
3. Core HP stops declining and returns to 500; the game runs to **r1000**
   (result becomes a tiebreak, which we would **lose** on delivered titanium
   2,040 vs 3,610 unless Fix C also lands — *so Fix A alone converts a loss into
   a different loss*, and that is itself a prediction).
4. **Falsifier:** if staffing reaches 3 and the core still dies, the equilibrium
   is not staffing-bound and this attribution is wrong.

**Fix B — counterbattery the point-blank gunner** (let a seated healer, or any
recalled builder, take (21,19) or (20,18) and grind `#195`; 13 attacks, 26 Ti):

5. `fire_src[(21,18)]` falls from **582** to **< 50**; a `removeEntity` on
   `#195` appears within ~15 rounds of the first attack on (21,18).
6. Incoming drops **9 → 2 HP/round**; core returns to 500 and stays.
7. **Falsifier:** if the enemy simply rebuilds at (21,18) or another
   corner-diagonal and the shot count recovers, the owner is the *absence of a
   home turret* (rank 3 / channel (i)) rather than the idle reserve, and the
   ranking above should be inverted.

**Fix C — stop the zero-yield ammo burn** (gate `convert_ammo` on the forward
sentinel actually out-damaging the target's heal rate):

8. B's lifetime `convert_ammo` falls from **2,339 Ti** toward ~0; bank ceiling
   rises above **22 Ti** within ~10 rounds of the change.
9. A third harvester is built by `#8` or `#10` on the ore tile they are already
   standing on ((17,9) or (23,17)); delivery per 100 r rises from **250**.
10. **Falsifier:** if the bank rises and no harvester follows, `#8`/`#10` are
    livelocked for a reason other than affordability and rank 5 is mis-stated.

**Fix D — repair a severed delivery spur** (a builder that owns a link should
re-queue a destroyed segment of it; 3 conveyors, 9 Ti):

11. The delivery source-tile ledger shows **(20,18) carrying stacks again** after
    r153 — it currently carries **0 for 532 rounds**. Delivery per 100 r goes
    **250 → ~500**, restoring the r0-r99 rate.
12. The bank ceiling rises above 22 Ti on the next cycle and rank 5 unwinds
    without touching `convert_ammo`.
13. **Falsifier:** if the spur is rebuilt and the saboteur `#9` simply re-cuts
    it (it sits at (20,16)/(21,16) all game and has 25 free action-rounds per
    100), then the repair loop is a treadmill and the real requirement is killing
    or walling out `#9` — which folds rank 4 into rank 2.

**Global prediction:** any successful fix **lengthens or draws** this game; none
of them shortens it. **A fix that produces a shorter loss falsifies the whole
model.**

**Prediction that would refute the "new channel" claim:** if a re-run with
`HS_HEAL_DETAIL_ON = False` (H1 and mechanism 2 both off) also reaches ~r732
with the same 9-vs-8 steady state, then the equilibrium is a property of the
parent's v73 defence, not of the plank, and channel (iii) should be renamed as
an inherited v73 trait rather than an hs-family one. The hsb contrast (§5)
argues against this — hsb ran at ~4 HP/round of heal, not 8 — but it is the
clean test.

---

## 8. Self-checks

### 8.1 Parser validation

`core_deliv × 10 == titaniumCollected` — the check `tools/replay_schema.md`
names as the cheapest proof a parser's geometry and update handling are right:

| replay | team | deliveries | ×10 | `titaniumCollected` | |
|---|---|---|---|---|---|
| `archipelago_b_hsd_off` | A | 361 | 3,610 | 3,610 | **OK** |
| `archipelago_b_hsd_off` | B | 204 | 2,040 | 2,040 | **OK** |
| `h85_archipelago_1_b` | A | 185 | 1,850 | 1,850 | **OK** |
| `h85_archipelago_1_b` | B | 128 | 1,280 | 1,280 | **OK** |

**4/4 team-sides, 0 mismatches.** Winner, turn count and win condition match the
run's own stdout (`v84g_off`, core destroyed, turn 732; 40 Ti / 3,610 mined vs
18 / 2,040; 7 units / 24 buildings vs 6 / 17 — all reproduced from the wire).

### 8.2 HP-delta ledger — 0 unexplained events

Every negative `updateHp` matched, in engine order with live positions and the
2×2 core footprints, against the same round's `fireTurret` targets and
`builderAttack` targets:

| replay | negative HP events | fire-only | attack-only | both | **unexplained** |
|---|---|---|---|---|---|
| `archipelago_b_hsd_off` | 1,618 | 285 | 169 | 1,164 | **0** |
| `h85_archipelago_1_b` | 746 | 118 | 418 | 210 | **0** |

Damage magnitudes are exactly **{2, 7, 18}** in both (hsd: 751 / 630 / 237) =
builder attack / gunner / sentinel. Heal magnitudes {2, 3, 4} = the +4 heal
clipped at max HP.

### 8.3 Totals accounted

* **Core damage sums to the attribution table**: 4,074 + 1,288 + 231 + 72 =
  **5,665** = the summed negative deltas on entity `#2`. Turret share by
  magnitude: 615 shots × 7 = 4,305 (= 582 + 21 + 12 by source tile) and 4 × 18 =
  72; builder share 644 × 2 = 1,288.
* **Core HP closes exactly**: 500 (start) − 5,665 (damage) + 5,165 (heal) = **0**
  at r731, and `damage − heal = 500` = the core pool, in both replays.
* **Delivery closes exactly** (§8.1).
* **Ammo closes exactly, both teams.** A: 630 gunner shots × 4 + 4 sentinel
  shots × 10 = **2,560**, banked **24**, converted **2,584** — exact. B: 233
  sentinel shots × 10 = **2,330**, banked **9**, converted **2,339** — exact.
  Fire-source tiles: A = (21,18) 582, (17,17) 27, (16,20) 21, (16,16) 4;
  B = (9,9) 227, (14,18) 5, (18,18) 1. Ammo is a `Player` field, cross-checked
  against the `coreConvertAmmo` stream.
* **Bank cycle closes**: 20 Ti income per 4 rounds (10 passive + one 10-stack
  delivery, measured) against 8 Ti heals + 12 Ti ammo = 20 Ti spend, reproducing
  the observed 20→10→8→16 bank cycle exactly, every cycle, r250-r731.

### 8.4 Bounded unexplained residue

* **Exactly two rounds in r251-r731 depart from the `−7 + −2` composition**, and
  both are accounted: **r251** (damage 2, heal 8, ΔHP **+6** — the last
  net-positive round, which is why the decline window starts at r252) and
  **r731** (damage 2, heal 0, ΔHP **−2** — the kill round; the core reaches 0
  before the healers' actions land). Every one of the 479 rounds in between is
  `−7 + −2 + 2×(+4)` = −1. Unexplained HP across the terminal window: **0**.
* **`placeEntity` re-emissions on a live id** (rotations): **2**, both enemy
  gunners — `#118` @(16,20) at r86 and `#195` @(21,18) at **r731**. Neither
  changes the tile. The r731 one is inside the death round and is not used in
  any count above.
* **Launcher throws** (`moveBuilderBot` with d²>1): **exactly 1** — r66, enemy
  launcher `#29` @(5,7) throwing A `#9` (4,6)→(8,11), d²=41 (§2 step 5b). We own
  no launcher in this game.
* **TLE**: the run was `--tle 0`; **0 `botOutput` records carry the `tled`
  flag** in either replay, so no turn was truncated. The idle builders are idle
  by logic, not by budget.
* **Passability assumption verified rather than assumed**: 2,313 builder-bot
  tile-rounds co-located with a live conveyor prove conveyors/splitters are
  walkable, which is what makes the "5 seats free" ledger in §3.3 correct. An
  earlier pass that counted paved seats as blocked read 1 free seat instead of 5
  and would have inverted the verdict — flagged here for the next decoder.

---

## 9. Handed back

1. **The heal-conscription pool is the lever, not the seat chooser.** Every hs
   revision so far has tuned *which* seat a candidate walks to (`_free_seats`
   ordering, H1's stickiness). This game says the binding constraint is *who is
   a candidate at all*: role 4 plus r²=20 vision. Three builders, five free
   seats, 480 rounds, −1 HP/round.
2. **`convert_ammo` has no yield test.** 2,339 Ti (60% of the steady-state
   budget) bought 4,086 HP that the defender healed 1:1. A cheap guard — only
   convert while the target core's HP is actually trending down — frees the
   entire liquidity trap.
3. **Nothing in the file attacks a turret that is diagonal to our own core.**
   (21,18) is not a seat, so no seat machinery sees it; it is not in a defender's
   melee-threat scan either, because the scan looks for enemy *builders*. 72% of
   all damage we ever took came through that hole.
4. **Nothing in the file repairs a destroyed link segment.** The spur feeding
   harvester `#17` is cut in five places between r101 and r153 and stays cut for
   532 rounds while its own builder stands 10 tiles away doing nothing and a
   conveyor costs 3 Ti. `link_queue` builds a route once; it is never re-derived
   from "this harvester has stopped shipping".
5. **Bimodal law**: this game is the tightest gap-zone point yet — ratio
   **0.912**, death, with net damage exactly equal to the HP pool. The threshold
   is now bracketed **> 0.912** (death) and **≤ 0.93** (`h85_meander_1_a`,
   survival). Recommend restating it as "net damage vs HP buffer", which
   predicts both.
6. **Positive finding worth keeping**: our own conveyor on heal seat (20,18),
   built r19 and never destroyed, is walkable for us and **unbuildable-on for the
   enemy** — it denies exactly the seat-planted gunner that killed hsb at r175.
   `HS_SEAT_BAN_CONVEYORS = False` is doing defensive work the plank never
   claimed credit for.

---

# Addendum (2026-08-08 12:3x): fix-candidate signature check (`_v87ad`, det)

**Deep signature check of the builder's fix candidate against §7's stated
predictions.** The outcome-level result was already known when this was
commissioned; what follows is the *mechanism* audit, which is where the
interesting answer is.

> ## ADDENDUM VERDICT
>
> **The model's outcome prediction is confirmed; its mechanism signature is
> REFUTED.** The core survives — but **not** because heal throughput rose.
> Heal throughput **fell** (800 → ~400 HP/100 r) and seat staffing **fell**
> (2.00 → 1.03-1.94). The fix worked by **subtracting damage, not adding heal**:
> incoming collapsed **9.0 → 4.0 HP/round** when the point-blank gunner at
> (21,18) was **killed at r308 by 13 builder attacks** — the exact cost I
> costed for "Fix B, not built" in §7. Fix A delivered rank 2 of §6 as a side
> effect of rank 1: it put a body on seat **(20,18)**, which is orthogonally
> adjacent to (21,18), and *that* body did the counterbattery. **Right owner,
> right lever, wrong readout.**
>
> Net: **9-in/8-out below the HP cap** becomes **4-in/4-out at the cap**. The
> core sits at 500 HP for **687 of 1,000 rounds**.

| | |
|---|---|
| Baseline | `replay_archive/diag_archb_fix_2026-08-08/archb_base.replay26` — **md5 `a07c277f55819de42df54fed08cee2f5`, `cmp`-clean byte-identical to this document's source game.** Reproduction claim verified at the byte level, not just the JSON level. |
| Candidate | `archb_cand.replay26` — `_v87ad` = hsd + Fix A (store-slot third-healer conscription) + Fix D (spur repair), both ON, seat B |
| Outcome | **r1000, `titanium_collected` tiebreak, A 4,950 / B 3,580.** Our core **survives at 500/500**. |
| Self-checks | `core_deliv × 10 == titaniumCollected` **4/4 team-sides**; HP-delta ledger **0 unexplained** (base 1,618 events, cand 2,597); magnitudes exactly {2, 7, 18} in both |

## A.1 Prediction-by-prediction

| # | §7 prediction | measured on `archb_cand` | verdict |
|---|---|---|---|
| — | **Global falsifier**: a correct fix lengthens or draws, never shortens | **732 → 1000 rounds** | **PASS** |
| 3 | Fix A alone converts a loss into a *different* loss (tiebreak, lost on delivered Ti) | **r1000 tiebreak, 4,950 vs 3,580** | **PASS — called exactly** |
| 3 | Core returns to 500 and stays | **687/1,000 rounds at full 500**; min after r300 = 417, after r400 = **488**; final **500** | **PASS** |
| 2b | ΔHP histogram loses the 479 `−1` entries and gains net-positive rounds | whole-game `−1` count **94** (the baseline had **479 in the terminal window alone**); **86 net-positive rounds** against the baseline's **0** after r251; **760 rounds at Δ=0** | **PASS** |
| **1** | ourBots on seat r250+ **2.00 → ≥3.00** | **1.94 → 1.22 → 1.10 → 1.03 → 1.76**; never above 1.94 | **FAIL** |
| **1** | free seats **5.00 → ≤4.00** | **4.24-5.06**; only r900-999 approaches (4.24) | **FAIL** |
| **2a** | core heal **800 → ≥1,200 HP/100 r** | **382-457 HP/100 r** — *lower* than the baseline | **FAIL** |
| **11a** | (20,18) carries delivery stacks again after the repair | 25 / 24 stacks in r0-199 (baseline: 21 / 4), then **0 for r200-r999**; terminus conveyor `#55` @(20,18) destroyed **r337** (it survived to r731 in the baseline) | **FAIL** |
| 11b | delivery **250 → ~500 /100 r** | 250 flat r200-r699, then **340 / 500 / 540** from r700 — via a **different** terminus, **(20,21)**, not the repaired spur | **PASS, 500 rounds late and by another route** |
| **12** | bank ceiling rises **above 22 Ti** | max is **exactly 22** for r200-r599 (up from 20 — it reaches the harvester price and stops there); **63 / 84 / 104** from r600 | **FAIL to r599, PASS after** |
| 9 | a harvester follows the bank | **11 harvesters, r693-r981** (`#682`, `#750`, `#768`, `#804`, `#814`, `#900`, `#918`, `#927`, `#988`, `#1005`, `#1048`) | **PASS, from r600** |
| **13** | *falsifier*: does saboteur `#9` re-cut the repaired spur (treadmill)? | **YES — the falsifier fires.** `#9` lands **75 attacks** on spur/ring tiles ((23,17) 15, (23,16) 10, (22,17) 10, (21,17) 10, (21,18) 10, (20,17) 10, (20,16) 10). We rebuild (21,18) r845 → **dead r936**; (21,17) r913 → **dead r921**, rebuilt r923. Harvester `#138` @(23,17) built r77 → **dead r126** | **TREADMILL CONFIRMED** |
| B | Fix B *not built* — does the `−1` attacker profile persist and get out-healed? | **No — the attacker is removed.** Gunner `#252` @(21,18) built r168, takes **13 hits × −2 = −26 on 25 HP between r248 and r308**, **destroyed r308**. `fire_src[(21,18)]` **582 → 113**. Attackers: **B `#10` ×9, B `#8` ×4** | **Fix B delivered as a side effect of Fix A** |

## A.2 What actually changed — the damage ledger, not the heal ledger

| | baseline (r251-r731) | candidate (r600-r999) |
|---|---|---|
| incoming, HP/round | **9.0** | **4.0** |
| composition | one −7 (gunner `#195` @(21,18)) + one −2 (builder `#3`) | **two −2** — pure melee, in **398 of 400 rounds** |
| heal applied, HP/round | 8.0 (two seated healers) | **4.0** (one heal action/round) |
| net | **−1.0** | **0.0**, at the 500 HP cap |
| our core damage / heal, whole game | 5,665 / 5,165 (**diff 500 = the pool**) | **4,159 / 4,159 (diff 0)** |
| core damage by channel | gunner 4,074 (72%), melee 1,288 (23%) | **melee 3,114 (75%)**, gunner fire 973 (23%) |

The profile **inverts**. Baseline: a gunner does three quarters of the damage
and melee a quarter. Candidate: the gunner is dead by r308 and melee does three
quarters. Melee is the *cheaper-for-us* channel to survive — 2 HP/round against
a 4 HP/round healer — which is the whole result.

**The chain, in events:** Fix A's broadcast puts `#8` on seat **(20,18)** at
**r169** (baseline: `#8` was livelocked at (17,8) from r108). (20,18) is
orthogonally adjacent to (21,18). `#8` and `#10` grind gunner `#252` from r248,
one attack every 7 rounds, then every round from r304; it dies **r308**. A
replaces it with gunner `#378` @(20,17) at r328 — **d²=4 from the core, not
d²=2** — which lands only **4** shots on our core all game. `#8` then dies on
that seat at **r334**, our conveyor `#55` @(20,18) dies **r337**, and A's builder
`#9` occupies the seat at **r342** and melees for **644** attacks.

## A.3 Three surprises worth carrying

**1. The prediction was framed on a counterfactual that the fix destroyed.**
Predictions 1 and 2a assumed incoming stays at 9 HP/round and we out-heal it.
Instead incoming halved, so **one** healer suffices — and because the core then
sits at 500 HP, `_core_shelled` is **False** for 687 of 1,000 rounds and the
conscription broadcast *switches itself off*. Seat staffing falling to 1.03 is
not the fix failing; it is the fix having succeeded and standing down. **Any
future prediction on this machinery must be stated as a ratio (heal ÷ incoming)
or as "rounds at full HP", never as an absolute heal count.** That is the single
most useful correction this check produced.

**2. Fix C ran itself, and the enemy applied it.** Our zero-yield ammo sink was
destroyed *by the opponent*: gunner `#176` @(8,8) at **r592**, sentinel `#84`
@(9,9) at **r598**. The predicted consequence chain (§7 Fix C, predictions 8-9)
followed immediately and exactly:

| window | bank max | ammo max | harvesters built | delivery /100 r |
|---|---|---|---|---|
| r200-r599 | **22** (pinned at the harvester price) | 5-8 | **0** | **250** |
| r600-r699 | **63** | 24 | 1 (`#682` r693) | 250 |
| r700-r799 | 63 | 24 | 4 | 340 |
| r800-r899 | **84** | 24 | 4 | **500** |
| r900-r999 | **104** | 24 | 2 | **540** |

So the liquidity trap of §2 step 10 is confirmed by removal, from the wrong
side of the board. **Fix C is the highest-value unbuilt item** and this is
direct evidence for it — but see the honest arithmetic in A.4.

**3. The opponent adapted, and the seat we won was lost back.** Enemy bots on
our seats go **1.00 → 2.00**; A's ammo conversion **2,584 → 1,078** while its
builder attacks on our core go **644 → 1,557**. A traded turret fire for melee —
the one channel our defence cannot answer without a turret. Meanwhile our freed
reserve went **raiding** rather than to the ring (`#4` 131 attacks on A's home
conveyors, `#10` 135), destroying A's harvester `#108` and ~10 of its conveyors —
and **8 of our builders died** (baseline: 0). The reserve is no longer idle; it
is now spent on offence with a real casualty rate.

## A.4 Honest arithmetic on the tiebreak

The builder's "+75% delivery" is a **total**, and the game is 37% longer. Per
100 rounds our delivery is **279 → 358, +28%** — A's rate is unchanged
(**493 → 495**), it simply played 268 more rounds. This is the same rate-vs-total
framing artifact §(c) of the parent read flagged on `saga_1_b`; the ship note
should carry the rate.

To win the tiebreak we need to beat 4,950. Counterfactually granting the r800+
rate (500/100 r) from **r300** onward yields ~4,580; from **r200** onward
~4,830. **Fix C alone does not reach the tiebreak on this map/seat** — it closes
most of the gap and leaves ~120-370 Ti. Something also has to cost A delivery,
or the map has to be won on the core instead.

## A.5 What this does to the main document

| claim | status |
|---|---|
| **§Verdict — owner is the idle reserve** | **STANDS, and is strengthened by intervention.** Conscripting the reserve is what removed the gunner and flipped the game. |
| **§6 rank 1 (staffing) vs rank 2 (counterbattery)** | **MERGED.** They are not independent levers: staffing *is* the delivery mechanism for counterbattery, because the free seats are the tiles adjacent to the enemy's gun. The ranking should say so. |
| §6 rank 4 (spur repair) | **DOWNGRADED.** P13's falsifier fired: the repair is a treadmill against a live saboteur. It bought ~100 rounds of the (20,18) terminus and nothing after r200. |
| §6 rank 5-6 (liquidity trap / ammo burn) | **CONFIRMED BY REMOVAL** (A.3 item 2), and promoted to the top unbuilt item. |
| §7 predictions 1, 2a, 11a, 12 | **REFUTED as written** — all four were absolute-magnitude forms of a ratio claim (A.3 item 1). |
| §2 step 9 — gunner @(21,18) is 25 HP / 13 attacks / 26 Ti | **CONFIRMED to the event**: 13 hits, −26, r248-r308, by `#10`×9 and `#8`×4. |
| §8 self-checks | **re-run clean on both new replays**: delivery×10 4/4, HP ledger 0 unexplained in 2,597 + 1,618 events. |
