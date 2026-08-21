# DIFF STUDY — x3r0 v165B(w35) → v169(w37), and the drakkarfjord/glacierkeep craters

**Provenance.** Fresh opus research agent, commissioned by the BUILDER arm s52 as the
release-critical diff study (the builder's own words in `docs/coordination.md`
2026-08-20T21:07:52Z: *"a v169-vs-v165 diff study (what w37 changed; why
drakkarfjord/glacierkeep flipped) is the natural next commission"*). No inherited
session context. Started 2026-08-21T02:35:28Z; repo HEAD `181f46b12` (2026-08-21
04:34:45 +0200). Archive/local-file analysis only — **no platform calls, no games
fired, no bot edits.**

**Inputs, exactly these:**
| what | path |
|---|---|
| v169 screen tape (2700 rows, 3 arms × 900) | `scratchpad/s52_hvh169/out/results.tsv` |
| v169 screen replays (2700) | `scratchpad/s52_hvh169/out/rep/` |
| v165B screen tape, v533home arm | `scratchpad/s52_hvh/out/_v533home.tsv` |
| v165B screen tape, v534maptrust arm | `scratchpad/s52_hvh/out/_v534maptrust.tsv` |
| s51 v165B screen, v525flip arm | `scratchpad/s51_vs_holder/head_vs_v165.tsv` |
| us-vs-incumbent full pools (5400 ea.) | `scratchpad/overnight/{V529POOL,HOMEPOOL,V535POOL}.tsv` |
| holder trees | `bots/_x3r0v165mjolnirB` (w35), `bots/_x3r0v169mjolnir` (w37) |
| our arms (read-only) | `bots/_v534maptrust`, `bots/_v529merge`, `bots/_v533home` |
| decode method reuse | `scratchpad/s51_ring/ringtape.py`, `scratchpad/s51_closure_autopsy/` |

`scratchpad/s52_hvh169/out_VOID_zip_era/` was **not read** (quarantined by the builder).

**DEFF.** Local screens are balanced-by-construction; pair-weighted DEFF ≈ 0.98
(s39 audit), so naive intervals are used throughout and are marginally conservative.
Where the two screens share an identical (map, seed, seat) cell grid, the **paired
(McNemar) test is used instead** — it is both the correct and the more powerful
instrument here, and it is what changes the headline.

---

## HEADLINE (read this if you read nothing else)

1. **w37 is THREE live behaviour changes, all in the SIEGE-RESPONSE / FORWARD-TURRET
   subsystem, plus one belt arm switched OFF.** Two further waves (EXIT_GUARD, STICK)
   are shipped with their master flags **False** and are inert code.
2. ⛔ **THE CRATERS PREDATE w37 AND ARE NOT ITS DOING.** Measured, same tree
   (`v533home`), same 900-cell grid: drakkarfjord **15/60 vs v165B → 16/60 vs v169**;
   glacierkeep **13/60 → 11/60**. `v534maptrust`: drakkarfjord **15/60 → 17/60**;
   glacierkeep **11/60 → 15/60**. The craters are a property of **the Mjolnir line as
   a family on these two maps**, not of the w35→w37 iteration.
3. ⛔ **THE "~4pp IN ONE DAY" DELTA DOES NOT SURVIVE A PAIRED TEST ACROSS BOTH ARMS.**
   The two screens share all 900 (map, seed, seat) cells. McNemar:
   `v533home` net −35 games, **z = −1.93 (p ≈ 0.054)**; `v534maptrust` net **−3 games,
   z = −0.17 (p = 0.86)**. Pooled over both arms: net −38 of 658 discordant cells,
   **z = −1.48, p = 0.14**. w37's measured cost to our line is **−2.11pp [95% CI
   roughly −5.4 … +1.1]**, i.e. **consistent with zero**. The 4pp figure is one arm
   at marginal significance; the second arm, on the identical grid, reads flat.
4. ⇒ **Q3 VERDICT: SEPARATE STORIES, and the commission's welding of them is refuted.**
   The diff is real and is aimed squarely at our siege; the craters are older than the
   diff and must be attacked as their own problem.

---

## Q1 — SOURCE DIFF v165B (w35) → v169 (w37)

### Files

| file | md5 changed? | +lines | −lines |
|---|---|---|---|
| `main.py` | **yes** | 103 | 1 |
| `doctrine.py` | **yes** | 349 | 1 |
| `eco.py` | **yes** | 76 | 0 |
| `raid.py` | **yes** | 217 | 6 |
| `opening.py` | no (`6e9a0b91…` both) | — | — |
| `ring.py` | no (`8eaa5ed0…` both) | — | — |
| `sip.py` | no (`9e7ab2c5…` both) | — | — |

**745 added, 8 removed — almost purely additive and flag-gated.** `DOCTRINE.md` grew
234 KB → 252 KB (prose only). `PROVENANCE.md` exists in the v165B tree and not in v169.

⭐ **`ring.py` IS BYTE-IDENTICAL.** The ring/claim machinery the s51 study
(`docs/research/RING-ENGAGEMENT-mjolnir-2026-08-20.md`) characterised did not move in
w37. Any "their ring line got better" story is refuted at the source level.

### The five arms, and which are LIVE

| # | wave / name | master flag in v169 | in v165B | subsystem | live? |
|---|---|---|---|---|---|
| 1 | **WAVE 37 PLANK RANK** | `RANK_ON = True` | absent | **siege response (counter-battery)** | **LIVE, NEW** |
| 2 | **WAVE 32 FIX 1 TUBE_REPLACE** | `TUBE_REPLACE_ON = True` | absent | **forward-turret economy (their siege)** | **LIVE, NEW** |
| 3 | **WAVE 31 RESTORE** | `RESTORE_HOLE_ON = True → **False**` | `True` | **belt (their own repair detour)** | **LIVE, a REMOVAL** |
| 4 | WAVE 32 FIX 2 EXIT_GUARD | `EXIT_GUARD_ON = False` | absent | self-blocking / build refusal | inert |
| 5 | WAVE 32 FIX 3 STICK | `STICK_ON = False` | absent | ring-12 collar re-seal | inert |

Arms 4 and 5 ship as dead code: 12 instrumented call sites in `raid.py`
(`salt_corpse`, `salt_deny`, `collar_brick`, `seat_seal`, `fwd_gunner`, `fwd_nest`,
`fwd_post`, `sge_screen`, `tw_launcher`, `tw_gunner`, `cg_ferry`, `cg_post`) all read
`if self._exit_refuse(...)` and `_exit_refuse` returns `False` on its head guard.
`self.stick_n = 0` is initialised in `main.py` unconditionally but can only increment
under `STICK_ON`. **Do not build a counter to either — they are not running.**

### Arm 1 — WAVE 37 PLANK RANK (the one aimed at us)

**What it does.** Their counter-battery routine `_try_counterbattery` was previously
reachable only by the single `role == "defend"` body (`LOKI_DEFEND_SEAT = 4`, and *"a
dead defender is never replaced"*), sitting at the **bottom** of `_builder`'s job
ladder under SAP, SEATHOLD, REPAIR, SIPHON and the whole role split. w37 inserts a new
rung, `_rank_cb`, high in `main.py`'s ladder:

```
main.py:  ... heal / OPENING / RING refill / RING evict ...
+         if RANK_ON and ct.get_action_cooldown() == 0:
+             self._rank_cb(ct, rnd)                        # <-- NEW RUNG
          if RING_ON and BELT_EVICT_ON and ct.get_action_cooldown() == 0:
              if self._belt_evict(ct, rnd): return          # (de-nested to make room)
```

so **any** builder inside their home band may now buy the answering turret.

**Their own stated numbers for the defect** (`doctrine.py`, WAVE 37 block, citing
`results/wave35/SCREEN_P1B.md` and `results/wave36/SCREEN_YARD.md`): over **925
instrumented "P1-state" rounds** (a live besieger inside `HUNT_BAND_DSQ` of their core
with no home turret answering), the CB gate opened on 63, `_try_counterbattery` was
**reached on ~3 %**, `_defend` entered on 33, the buy loop on 22, and **two gunners
were bought in thirty games.** They also cite `TEST_V167.md` defect #2: *"`their_ge2`
(they hold ≥ 2 forward tubes) separates 16 % wins from 63 %"* — **`their_ge2` is US.
This arm exists because our two-forward-tube siege is their measured loss condition.**

**Constants (all new):**

| constant | value | meaning |
|---|---|---|
| `RANK_ON` | `True` | master |
| `RANK_BODIES` | `1` | one elevated body per round |
| `RANK_HOME_DSQ` | `HUNT_BAND_DSQ` = **41** | "home body" band, r² |
| `RANK_TURRET_ONLY_ON` | `True` | requires a **live GUNNER or SENTINEL read on the threat tile this round** |
| `RANK_LOG` | `False` | off in competition |

**Three exploitable properties, read off their source:**

* **The trigger is `RANK_TURRET_ONLY_ON` — a live GUNNER/SENTINEL standing on the
  `_cb_target` tile, re-derived every round.** `doctrine.py`: *"There is no latch and
  no memory: every term is re-derived from this round's sighting, so the round the
  besieger dies or a home gun starts bearing, the elevation stops."* A **builder-bot**
  or a **ghost** target buys nothing (`_cb_target`'s own docstring: `SLOT_THREAT` named
  a tile holding no enemy at all on 893 ladder-loss rounds; wave 34 classified 2 502
  targets as GUNNER 516 / BUILDER_BOT 772 / None 247).
* **Election, not a comm claim.** `_rank_elect` defers to any friendly builder it can
  **see** that is also in the band and strictly closer to the threat, ties by entity
  id. Builder vision is r² = 20 and the band is r² = 41, so **two bodies at opposite
  edges of the band cannot see each other** — their own comment names this residue and
  closes it only "one layer down", via `_live_home_gun` seeing the first body's turret.
* **`self._f0_plug` (THE PLUG RULE) refuses the elevation for a body on OUR ring**, and
  `self._home_gun_bears(ct, target)` shuts it entirely once one of their home turrets
  bears on the target.

### Arm 2 — WAVE 32 FIX 1 TUBE_REPLACE (their forward siege against us)

Their forward sentinel ("tube") was replaced almost never after the last one died:
their measurement is **3 247 zero-tube rounds a corpus (130/game), 14 of 25 games
ending with none alive, mean dead tail 120 rounds.** Cause, per their own text: the
`SIEGE_MASS_ON` discount was gated `n >= 1`, so it could cheapen tube 2 and 3 but
**never the replacement of a dead last tube.**

| constant | old (effective) | new (replacement state only) |
|---|---|---|
| bank floor | `LOKI_FWD_TI_FLOOR` = **40** | `TUBE_REPLACE_TI_FLOOR` = `SIEGE_MASS_TI_FLOOR` = **6** |
| harvester floor | `LOKI_FWD_MIN_HARV` = **2** | `TUBE_REPLACE_MIN_HARV` = **1** |
| `TUBE_REPLACE_HARV_ON` | — | `True` (separately ablatable) |
| `TUBE_REPLACE_LOG` | — | `False` |

Gate `_tube_replace_ok(ct, E, live)` requires **both**: `live == 0` (a literal integer
zero from `_live_fwd_guns`, which returns `None` when blind — fail-closed) **and**
`read_store(SLOT_FWD_GUN) >= 1` (monotone "one ever existed"). Applied at **two**
sites: the build gate in `_try_forward_sentinel`, and the nest-**walk** gate in
`_t5_nest_walk_target` (so the raider is not released to build and then refused the
walk). One-directional: `ti_floor` only ever moves **down**.

⇒ **Net effect on us: after we kill their forward tube, they rebuild it at a 6-Ti bank
floor instead of a 40-Ti one, and with one harvester instead of two.** Their siege
should now be far more persistent through our counter-fire.

### Arm 3 — WAVE 31 RESTORE turned OFF (`RESTORE_HOLE_ON: True → False`)

The only **removal** in the diff. It was their belt-hole repair detour —
`RESTORE_HOLE_STEPS = 6` Manhattan reach, worst case 18 Ti of conveyor per body,
justified in-tree against *"a belt uptime of 6-7 % in the games this plank exists
for"*. w37 stands it down. **Classification: BELT.** No new constant; the six
`RESTORE_HOLE_*` numbers are unchanged and now unreachable.

**Subsystem tally: siege response ×1 (new, aimed at our forward tubes), forward-turret
economy ×1 (new, makes their siege persistent), belt ×1 (removal). Ring: UNCHANGED.
Launcher: UNCHANGED. Targeting: UNCHANGED.**

---

## Q2 — THE CRATERS

### The tape, per map, per arm (`scratchpad/s52_hvh169/out/results.tsv`, n = 900/arm)

| map | v534maptrust | v529merge | v533home | POOL (n=180) |
|---|---|---|---|---|
| antler | 37/60 62% | 26/60 43% | 31/60 52% | 52.2% |
| archipelago | 20/60 33% | 27/60 45% | 20/60 33% | 37.2% |
| auroraveil | 31/60 52% | 35/60 58% | 33/60 55% | 55.0% |
| **drakkarfjord** | **17/60 28%** | 35/60 58% | **16/60 27%** | **37.8%** |
| drumlin | 35/60 58% | 21/60 35% | 32/60 53% | 48.9% |
| fjordgate | 35/60 58% | 29/60 48% | 31/60 52% | 52.8% |
| frostgate | 50/60 83% | 46/60 77% | 45/60 75% | 78.3% |
| **glacierkeep** | **15/60 25%** | **7/60 12%** | **11/60 18%** | **18.3%** |
| icefloe | 22/60 37% | 5/60 8% | 29/60 48% | 31.1% |
| midgard | 17/60 28% | 36/60 60% | 12/60 20% | 36.1% |
| nordkap | 41/60 68% | 40/60 67% | 42/60 70% | 68.3% |
| **ragnarok** | **60/60 100%** | **60/60 100%** | **60/60 100%** | **100.0%** |
| royale | 39/60 65% | 55/60 92% | 53/60 88% | 81.7% |
| valkyrie | 21/60 35% | 31/60 52% | 21/60 35% | 40.6% |
| yulerune | 30/60 50% | 3/60 5% | 18/60 30% | 28.3% |
| **TOTAL** | **470 52.22%** | **456 50.67%** | **454 50.44%** | 51.11% |

⚠ **CORRECTION TO THE COMMISSION'S FRAMING #1 — "drakkarfjord and glacierkeep are
craters" is only half true, and the halves are different objects.**
* **glacierkeep is a UNIVERSAL crater**: 25 % / 12 % / 18 % across all three arms
  (33/180 pooled, 18.3 %). Arm-independent ⇒ a property of the matchup.
* **drakkarfjord is ARM-DEPENDENT**: v529merge reads **35/60 (58 %)** there while
  v534maptrust reads 17/60 and v533home 16/60. Per-cell hw at n=60 is ±12.6pp; the
  v529–v534 gap is **+30pp**, roughly 2.4 half-widths — **outside noise**. Whatever
  v529merge carries and the two "home" arms do not, it is worth 30pp on drakkarfjord.
* **Two further craters the commission did not name and which are as large:**
  **yulerune** (v529merge 3/60 = 5 %, vs v534maptrust 30/60 = 50 % — a **45pp**
  arm split) and **icefloe** (v529merge 5/60 = 8 % vs v533home 29/60 = 48 %). Both
  are v529merge-specific and both are bigger than the drakkarfjord gap.

### The within-map controls, and they are decisive

**Control A — ragnarok 60/60/60 (180/180).** Our arms beat the Mjolnir line on
ragnarok **without a single loss in 180 games across both holder generations**, while
reading only **56-67 % against our own incumbent `_v488beltbreak2`** on the same map.
The relation is **inverted**: ragnarok is a *mediocre* map for us vs the incumbent and
a *perfect* one vs Mjolnir. The instrument can therefore produce the other verdict at
maximum amplitude, and map difficulty for *us* is not what the crater measures.

**Control B — us vs the incumbent, same maps** (`scratchpad/overnight/*POOL.tsv`,
n = 5400/arm, treatment `T` = our arm, control = `bots/_v488beltbreak2`):

| map | V529POOL (v529merge) | HOMEPOOL (v533home) | V535POOL (v535cornergate) | …vs **Mjolnir** (pooled 180) |
|---|---|---|---|---|
| **drakkarfjord** | 326/360 **91 %** | 355/360 **99 %** | 355/360 **99 %** | **37.8 %** |
| **glacierkeep** | 311/360 **86 %** | 317/360 **88 %** | 316/360 **88 %** | **18.3 %** |
| ragnarok | 241/360 67 % | 205/360 57 % | 200/360 56 % | **100.0 %** |
| archipelago | 154/360 43 % | 58/360 16 % | 168/360 47 % | 37.2 % |
| valkyrie | 172/360 48 % | 173/360 48 % | 165/360 46 % | 40.6 % |
| pool total | **72.57 %** | **66.44 %** | **68.83 %** | 51.11 % |

⇒ **The commission's 80-98 % claim is confirmed and is if anything understated
(86-99 %).** drakkarfjord and glacierkeep are two of our three strongest maps against
our own incumbent and two of our three weakest against Mjolnir. **That swing —
−61pp on drakkarfjord, −68pp on glacierkeep — is an OPPONENT effect, not a map
effect, and it is the largest single structure in the whole tape.**

### Crater stability across the holder generation — the w37 control

Same tree, same 900-cell grid, only the opponent version differs:

| map | v533home vs **v165B** | v533home vs **v169** | Δ | v534maptrust vs **v165B** | v534maptrust vs **v169** | Δ |
|---|---|---|---|---|---|---|
| **drakkarfjord** | 15/60 25 % | 16/60 27 % | **+1** | 15/60 25 % | 17/60 28 % | **+2** |
| **glacierkeep** | 13/60 22 % | 11/60 18 % | **−2** | 11/60 18 % | 15/60 25 % | **+4** |
| ragnarok | 60/60 | 60/60 | 0 | 60/60 | 60/60 | 0 |
| valkyrie | 33/60 | 21/60 | −12 | 19/60 | 21/60 | +2 |
| yulerune | 28/60 | 18/60 | −10 | 25/60 | 30/60 | +5 |
| royale | 44/60 | 53/60 | +9 | 47/60 | 39/60 | −8 |
| icefloe | 34/60 | 29/60 | −5 | 35/60 | 22/60 | −13 |
| archipelago | 28/60 | 20/60 | −8 | 24/60 | 20/60 | −4 |
| midgard | 17/60 | 12/60 | −5 | 15/60 | 17/60 | +2 |
| auroraveil | 25/60 | 33/60 | +8 | 22/60 | 31/60 | +9 |
| **TOTAL** | **489 (54.33 %)** | **454 (50.44 %)** | **−35** | **473 (52.56 %)** | **470 (52.22 %)** | **−3** |

⛔ **The two crater cells move by −2 … +4 games out of 60 — i.e. nothing.** Every cell
that moved materially (valkyrie, yulerune, royale, icefloe) **moved in OPPOSITE
DIRECTIONS in the two arms**, which is the signature of seed noise at ±12.6pp/cell, not
of a code change. **The craters are not a w37 phenomenon. They are how the Mjolnir
family has always played these two maps against us.**

### Historical depth — third independent arm on the v165B anchor

`scratchpad/s51_vs_holder/head_vs_v165.tsv` (`_v525flip` vs v165B, n = 900, 46.56 %
overall) reads **glacierkeep 16/60 (27 %)** — the crater again, in a fourth arm on a
different day. It reads **drakkarfjord 33/60 (55 %)**, matching v529merge rather than
the home arms — **so drakkarfjord tracks the ARM lineage (v525flip/v529merge ≈ 55-58 %,
v533home/v534maptrust ≈ 25-28 %) and glacierkeep tracks nothing but the opponent.**
Two different problems wearing the same word.

---

## Q3 — ATTRIBUTION

### Does the ~4pp day-delta survive?

The two screens (`s52_hvh` vs v165B, `s52_hvh169` vs v169) share **all 900
(map, seed, seat) cells** — verified: `|A ∩ B| = 900` for both arms. Paired McNemar:

| arm | lost-vs-v169-only | won-vs-v169-only | net | **z** | p (2-sided) |
|---|---|---|---|---|---|
| v533home | 182 | 147 | **−35** | **−1.93** | ≈ 0.054 |
| v534maptrust | 166 | 163 | **−3** | **−0.17** | 0.86 |
| **pooled** | 348 | 310 | **−38** | **−1.48** | **0.14** |

⛔ **The claim "x3r0's w35→w37 iteration bought ~4pp against our line inside one day"
is NOT SUPPORTED.** It rests on the v533home arm alone (−3.89pp, p ≈ 0.054, i.e. it
does not clear 0.05 even unadjusted for having picked the larger of two arms), and the
v534maptrust arm measured on the identical grid reads **−0.33pp**. Pooled over 1 800
cells the point estimate is **−2.11pp** and the interval covers zero.

**Not a claim that w37 is harmless** — the arms are aimed at our siege and the pooled
sign is negative. It is a claim that **this tape cannot resolve w37's effect**, and
that a release decision must not be built on the 4pp number.

*(Note on power: 658 of 1 800 paired cells are discordant, i.e. **36.6 % of cells flip
outcome** between the two screens. Some of that is w37; the rest is the chaotic
sensitivity of a 1 000-round game to any behavioural perturbation. Either way it is
the reason the paired test is barely more powerful than the unpaired one here.)*

### Is any Q1 change PRESENT IN the crater mechanism?

**No, and the geometry of the evidence forecloses it:**

1. **Temporal.** Both craters read the same against w35 as against w37 (table above).
   A mechanism introduced in w37 cannot explain a deficit that was already there in w35.
2. **Structural.** The two live w37 arms (RANK, TUBE_REPLACE) are both **siege-response
   / forward-turret** arms. If either were the crater mechanism, glacierkeep and
   drakkarfjord should have *degraded* from v165B to v169. They did not (−2 … +4 games).
3. **Source-level.** `ring.py` is **byte-identical** across the two trees, so the
   "their ring line eats our siege" hypothesis in the builder's banked note has **no
   w37 code change behind it at all**. If their ring eats our siege on these maps, it
   has been doing so since at least w35 and probably far earlier.

⇒ **VERDICT: SEPARATE STORIES.** The w37 diff is real, well-documented, and aimed
precisely at the two-forward-tube siege that is our win condition against them
(`their_ge2` separates their 16 % from their 63 %). The craters are older, larger
(−61 / −68pp against the same maps' incumbent baseline), and mechanically unexplained
by anything in this diff. **Do not weld them. Do not spend the v536 port on w37
counters and expect the craters to move.**

---

---

## Q2 (continued) — THE CRATER MECHANISM, FROM THE REPLAYS

### Step 1 — the craters are an ECONOMY failure, and the tape says so on its own columns

`ours_mined` / `opp_mined` in the screen tape are `titanium_collected`, i.e.
**delivery to the core** (CLAUDE.md, engine-probed). Pooled over all three arms, n=180/map:

| map | win% | **our games with ZERO delivery** | **their games with ZERO delivery** | med ours | med theirs |
|---|---|---|---|---|---|
| **glacierkeep** | 18 % | **89 %** | 19 % | **0** | 1 090 |
| **drakkarfjord** | 38 % | **52 %** | 36 % | **0** | 290 |
| yulerune | 28 % | 26 % | 1 % | 360 | 1 250 |
| icefloe | 31 % | 23 % | 5 % | 910 | 1 280 |
| auroraveil | 55 % | 37 % | 40 % | 355 | 340 |
| ragnarok | **100 %** | 0 % | 0 % | 570 | 230 |
| frostgate | 78 % | 0 % | 0 % | 785 | 170 |
| royale | 82 % | 0 % | 7 % | 3 025 | 960 |

**Truncation-normalised** (Ti delivered per 100 rounds, median per game — immune to
"we killed them early so they had no time"): **delivery-rate asymmetry vs win rate is
Spearman ρ = 0.925 across the 15 maps.** drakkarfjord and glacierkeep are the only two
maps where our normalised rate is **0.0**.

**Collider-free cut — TIEBREAK GAMES ONLY** (both cores alive at r1000: no truncation,
no end-state artifact). glacierkeep, n = 38: **our zero-delivery rate 97 %, theirs
24 %; median ours 0, theirs 1 720.** In games that ran the full thousand rounds we
delivered nothing at all in 97 % of them.

### Step 2 — it is NOT a cut belt. Our conveyors are not being destroyed.

Median over 15 v534maptrust seat-A games per map:

| map | our conveyors built | alive at end | **our conveyor loss** | their barriers built | our harvesters alive |
|---|---|---|---|---|---|
| glacierkeep | 34 | 34 | **0 %** | 10 | 4 |
| drakkarfjord | 9 | 9 | **0 %** | 10 | 2 |
| frostgate | 12 | 7 | 42 % | 7 | 3 |
| royale | 45 | 44 | 2 % | 2 | 8 |

⇒ On the craters we build a belt, **keep every tile of it**, keep our harvesters
alive, and deliver zero. **The belt is not cut. It never CONNECTS.**

### Step 3 — the missing tile is our own Core's delivery socket, and they own it

Hand-rendered board, `v534maptrust_glacierkeep_s10_A.replay26`, r1000, our core at
(14,2) (uppercase = ours, lowercase = theirs, `*` ore, `#` wall):

```
 1 ##..#........bbb.........#..##
 2 #..HCCCCCCCCCb@.b.........*..#     <- our belt runs (4,2)..(12,2); (13,2) is THEIR barrier
 3 ..*##........b..b........##*..
 4 ##.#.........B.bb.........#.##
 ...
 5 ..............l...............     <- (14,5) THEIR launcher
 6 ..............C...............     <- our northbound trunk stops here
 7 .............UC...............
 8 ......HCCCCCCCC........*......     <- harvester (6,8), belt east then north
```

Our harvester at (3,2) feeds nine conveyors east to (12,2). **(13,2) — the one tile
that touches our core — is their barrier.** The second trunk from (6,8) climbs
column 14 and stops at (14,6): **(14,5) is their launcher.** Seven of our eight core
sockets are held by their buildings. We hold **zero**. Delivery: 0.

### Step 4 — quantified across all 2 700 games, with its mirror

Two purpose-built instruments, both banked under `scratchpad/s52_diffstudy/`:
* **`ringplug.py`** — end-of-game occupancy of the 8 tiles orthogonally adjacent to a
  team's 2×2 core footprint, computed **identically for both teams** so every number
  carries its own mirror control.
* **`ringtime.py`** — an **independent second walk** of the turn stream giving the
  same quantity per round: first enemy plug, first own relay seat, sealed fraction.

**INSTRUMENT VALIDATION (three guards, each able to return the other verdict):**
1. **Positive control, hand-computed.** On `glacierkeep_s10_A` the board above was
   counted by hand to 7 plugged / 1 free. `ringplug.py` returned **plug 7, free 1**.
2. **Negative / other-verdict control.** On `ragnarok_s10_A` the same code returns
   **our plug 3, our own-relay 2, their plug 6, their own-relay 0** — the sign flips
   and the column is not constant.
3. **Mutation control.** Shifting the ring anchor by (+5,+5) drops every plug count to
   **0** on all three test replays (true anchor: 7/6, 8/0, 3/6). The measurement is
   anchored to the real core ring, not to generic map clutter.
4. **Cross-check.** `ringtime.py`'s independent walk agrees with `ringplug.py` on the
   shared quantity (s10: plugmax 7 vs plug_end 7; own1_r −1 vs own_end 0).

**Ring state at end of game, n = 180/map, our side and theirs:**

| map | win% | our ring plugged (of 8) | **their** ring plugged | asym | our OWN relay seats | our ring FULLY sealed |
|---|---|---|---|---|---|---|
| **glacierkeep** | 18 | **6.84** | 2.26 | **−4.58** | **0.14** | **29 %** |
| **yulerune** | 28 | 5.75 | 2.52 | −3.23 | 1.01 | 18 % |
| **drakkarfjord** | 38 | **6.56** | 4.72 | −1.84 | **0.46** | **37 %** |
| icefloe | 31 | 3.23 | 2.07 | −1.17 | 1.17 | 1 % |
| auroraveil | 55 | 3.56 | 2.92 | −0.64 | 0.64 | 2 % |
| nordkap | 68 | 4.43 | 5.17 | +0.74 | 1.91 | 0 % |
| frostgate | 78 | 5.67 | 6.56 | +0.89 | 1.53 | 4 % |
| royale | 82 | 0.79 | 3.09 | +2.30 | **4.49** | 0 % |
| **ragnarok** | **100** | **1.61** | **5.37** | **+3.76** | 1.54 | 0 % |

**Ring-plug asymmetry vs win rate: Spearman ρ = 0.925 (n = 15 maps).** "Fully sealed"
= zero free sockets **and** zero own relay sockets, i.e. the belt is mechanically
unable to terminate.

**DOSE-RESPONSE, within the crater maps only** (glacierkeep + drakkarfjord, n = 360):

| our usable sockets at end (free + own relay) | n | **delivered anything** | **win%** |
|---|---|---|---|
| **0** | 119 | **0 %** | **9 %** |
| 1 | 117 | 32 % | 26 % |
| 2 | 58 | 33 % | 19 % |
| 3 | 36 | 67 % | **75 %** |
| 4+ | 30 | 83 % | **73 %** |

Monotone in win rate, and the 0-socket cell is a **hard zero on delivery: 0 of 119.**

### Step 5 — ⭐ THE MECHANISM IS A RACE, AND WE LOSE IT ON A CLOCK

`ringtime.py`, medians over n = 180/map:

| map | nearest ore (Manhattan) | win% | **WE first own a socket** | **we NEVER do** | **THEY first own a socket** | they first plug ours |
|---|---|---|---|---|---|---|
| frostgate | 3 | 78 | r2 | 0 % | **r2** | r23 |
| ragnarok | 3 | 100 | r4 | 0 % | **r2** | r29 |
| royale | 6 | 82 | r4 | 0 % | **r2** | r161 |
| icefloe | 7 | 31 | r7 | 11 % | **r2** | r12 |
| auroraveil | 7 | 55 | r26 | **36 %** | **r2** | r17 |
| **drakkarfjord** | **10** | 38 | **r23** | **52 %** | **r2** | **r16** |
| **glacierkeep** | **11** | 18 | **r230** | **86 %** | **r2** | **r13** |

⭐ **MJOLNIR PUTS A CONVEYOR ON ITS OWN CORE SOCKET AT ROUND 2 ON 15 MAPS OUT OF 15,
UNCONDITIONALLY.** We do it at r2–r8 when the ore is close, at **r23 on drakkarfjord**,
at **r230 on glacierkeep**, and **not at all in 86 % of glacierkeep games**.

**And the build order is why.** Median round / median Manhattan distance-from-own-core
of the 1st…6th relay each side lays (8 games per map, seat A):

| map | ours #1 | ours #2 | ours #3 | | theirs #1 | theirs #2 | theirs #3 |
|---|---|---|---|---|---|---|---|
| **glacierkeep** | **r14 / d10** | r16 / d11 | r18 / d9 | | **r2 / d2** | r3 / d2 | r29 / d10 |
| **drakkarfjord** | **r10 / d8** | r12 / d9 | r13 / d7 | | **r2 / d2** | r3 / d2 | r12 / d8 |
| ragnarok | r6 / d2 | r8 / d3 | r18 / d3 | | r2 / d2 | r3 / d2 | r5 / d3 |
| royale | r4 / d2 | r6 / d3 | r8 / d4 | | r2 / d2 | r3 / d2 | r4 / d3 |
| frostgate | r2 / d2 | r4 / d3 | r6 / d2 | | r2 / d2 | r3 / d2 | r4 / d3 |

⇒ **WE LAY THE TRUNK ORE-END-FIRST; THEY LAY IT CORE-END-FIRST.** Their first two tiles
are always the two core sockets, *then* the long haul. Ours start where the harvester
is. On a short-haul map that costs nothing — we reach the socket by r2–r8 anyway. **On
a long-haul map (nearest ore 10–11) the socket is the LAST tile we would place, and
Mjolnir's collar barriers arrive on it at r13–r16.** We then spend the rest of the game
laying a belt (34 conveyors on glacierkeep, none of them lost) into a door that is
already bricked.

**Q2 ANSWER, four sentences:** On drakkarfjord and glacierkeep our belt is never cut —
it is never *connected*: our conveyors survive at 0 % loss and our harvesters live, but
Mjolnir's collar barriers hold 6.6–6.8 of our core's 8 delivery sockets and we hold
0.14–0.46, so 89 % (glacierkeep) and 52 % (drakkarfjord) of our games end with
`titanium_collected = 0`. The cause is a **build-order race we lose on a clock**: they
claim their own socket at **r2 on 15/15 maps**, we claim ours at **r23 / r230** because
we lay the trunk from the ore inward and these are the only two pool maps with nearest
ore at 10–11 tiles, so the socket is the last tile we would place and their first plug
lands at r13–r16. **Within-map controls confirm the direction rather than a map-difficulty
story: on ragnarok we win 180/180 while doing the same thing to THEM (+3.76 plug
asymmetry, their belt zeroed), and on glacierkeep against our own incumbent
`_v488beltbreak2` the SAME v533home tree delivers a median 230 with an 18 % zero-rate and
wins 51/60 (85 %) — the incumbent simply never contests the socket.** The dose is
monotone and mechanical: 0 usable sockets ⇒ 0 of 119 games delivered anything and 9 %
won; 3+ sockets ⇒ 67–83 % delivered and 73–75 % won.

---

## Q3 (continued) — ATTRIBUTION, WITH DOSE

**The Q1 changes are absent from the Q2 mechanism, on four independent grounds:**

1. **The mechanism is a COLLAR/BARRIER arm on our ring; `ring.py` is byte-identical
   across w35 and w37**, and the collar code in `raid.py::_collar_act` changed only
   under `STICK_ON`, which **ships False**.
2. **Both live w37 arms (RANK, TUBE_REPLACE) are siege-response / forward-turret arms.**
   Neither touches belt, collar or barrier placement. The one w37 change that *is*
   belt-adjacent — `RESTORE_HOLE_ON: True → False` — is a **removal of one of their own
   repair behaviours**, which if anything should have helped us.
3. **Temporal:** the crater cells and the zero-delivery signature are **identical**
   against w35 and w37. `v533home` on glacierkeep: our-zero-delivery **92 % (v165B) →
   89 % (v169)**; drakkarfjord **52 % → 52 %**. Same tree, same 900-cell grid.
4. **The ~4pp delta itself does not survive the paired test** (§Q3 above: pooled
   z = −1.48, p = 0.14).

### The dose evidence that DOES exist — an arm-controlled natural experiment

`v529merge` carries a **socket-claim regression** that the other two arms do not:

| map | v534maptrust never-claims / win | v529merge never-claims / win | v533home never-claims / win |
|---|---|---|---|
| **yulerune** | **0 % / 50 %** | **68 % / 5 %** | **0 % / 30 %** |
| **icefloe** | **0 % / 37 %** | **33 % / 8 %** | **0 % / 48 %** |
| glacierkeep | 83 % / 25 % | 83 % / 12 % | 90 % / 18 % |
| drakkarfjord | 50 % / 28 % | 50 % / 58 % | 57 % / 27 % |
| midgard | 0 % / 28 % | 0 % / 60 % | 0 % / 20 % |

**Restricted to the identical (map, seed, seat) cells where v534maptrust claims a socket
and v529merge never does — same map, same seed, same seat, same opponent version:**

| map | n cells | v534maptrust wins | v529merge wins | reverse cells |
|---|---|---|---|---|
| yulerune | 41 | **21 (51 %)** | **1 (2 %)** | 0 |
| icefloe | 20 | **8 (40 %)** | **0 (0 %)** | 0 |
| **combined** | **61** | **29** | **1** | **0** |

McNemar on the 30 discordant pairs: **z = 5.11, p ≈ 3 × 10⁻⁷.** And the two arms are at
**overall parity** (52.22 vs 50.67), so this is not "the better arm wins".

**Master dose table, all 2 700 games vs v169:**

| round we first own a core socket | n | **win %** | delivered anything |
|---|---|---|---|
| ≤ r10 | 1 729 | **59.5 % [±2.3]** | 99.4 % |
| r11–r100 | 551 | 53.7 % [±4.2] | 96.7 % |
| > r100 | 46 | 19.6 % [±11.5] | 71.7 % |
| **NEVER** | **374** | **12.6 % [±3.4]** | **0.0 %** |

⚠ **HONEST LIMIT ON THIS EVIDENCE.** The socket claim is **not randomised**; these are
observational splits, and `v529merge` differs from `v534maptrust` in more than socket
behaviour, so the arm contrast identifies a **mediator**, not an intervention. What
raises it above correlation: (a) the state is **determined by map geometry fixed before
the game starts** (nearest-ore distance 10–11 on exactly the two worst maps); (b) the
mirror shows the state is **achievable on those very maps** — Mjolnir reaches it at r2
on 15/15 including both craters; (c) the dose is **monotone with a mechanical hard
zero** (no socket ⇒ no delivery is a rule of the engine, not a statistic); (d) the arm
contrast is within-map, within-seed, within-seat, within-opponent, with **zero reverse
cells**. It still needs a fired A/B to become a refutation (point 6 of the directive).

### VERDICT

> **SEPARATE STORIES — and the commission's welding of them is refuted at the source
> level.** w37 is a real, well-aimed siege-response iteration whose measured cost to our
> line is **−2.11pp, CI covering zero**. The craters are older, an order of magnitude
> larger, and are an **economy/build-order** failure of OUR opening on long-haul maps
> against a collar arm that has been in the Mjolnir tree since at least w35.
> **Do not spend the v536 port on w37 counters and expect the craters to move.**

---

## Q4 — RECOVERY CONSTRAINTS FOR THE v536 PORT

### The recovery ceiling, per arm

Moving every NEVER-claim game to the observed ≤r10 win rate (an **upper bound**, since
some of those games are lost for other reasons):

| arm | base | NEVER-claim games | their win% | ≤r10 win% | **ceiling** | gain |
|---|---|---|---|---|---|---|
| v534maptrust | 52.22 | 101 (11.2 %) | 19.8 % | 58.8 % | **56.60 %** | +4.38pp |
| v529merge | 50.67 | 163 (18.1 %) | 8.0 % | 64.1 % | **60.82 %** | +10.16pp |
| v533home | 50.44 | 110 (12.2 %) | 12.7 % | 57.3 % | **55.89 %** | +5.44pp |

At n = 900 the half-width is ±3.27pp. A v534maptrust at its ceiling 56.60 reads
**[53.3, 59.9] — CI excludes 50, RELEASE BAR (1) MET.** Even at **half** the ceiling
(54.41 ⇒ [51.1, 57.7]) the bar still clears; the plank stops being sufficient on its
own below roughly **+1.1pp of realised gain** (53.3 ⇒ [50.0, 56.6]). ⇒ **This one plank
carries the release bar if it realises a quarter of its ceiling or better.**

**Where the recoverable games live** (home arms): glacierkeep 50–54, drakkarfjord 30–34,
auroraveil 21–22 — **three maps hold 100 % of them.** `v529merge` adds yulerune 41 and
icefloe 20.

### Constraints and directions, one line each

1. **CLAIM ONE OWN CORE-RING SOCKET BY r4, UNCONDITIONALLY, ON EVERY MAP** — not gated
   on ore distance, not gated on a harvester existing, not gated on a route being
   planned. Cost is one conveyor (3 Ti at scale 1.0). This is the whole plank.
2. **BUILD THE TRUNK CORE-OUTWARD, NOT ORE-INWARD** — measured: our first relay lands
   at d10/r14 (glacierkeep) and d8/r10 (drakkarfjord) while theirs lands at d2/r2 on
   every map in the pool. The socket must be the FIRST tile of the trunk, not the last.
3. **PREVENTION, NEVER EVICTION — do not spend the fix on clearing their plug.** Their
   barrier is 30 HP = 15 builder pecks at 2 Ti = 30 Ti and 15 builder-turns per socket;
   claiming first is 3 Ti and one turn, a **10× price difference**. This also keeps the
   plank clear of the s51 banked constraint against deepening the collar tar-pit
   (`docs/research/AUTOPSY-crater-vs-sweep-2026-08-20.md`), which governs THEIR ring —
   this plank touches only OUR OWN ring, so there is no PLUG-RULE exposure and no
   forward-body recall.
4. **CLAIM TWO SOCKETS ON DIFFERENT SIDES, NOT ONE** — their plug reaches 6–7 of our 8
   sockets, a conveyor is 20 HP and a peck is 2 damage, and the arms that do best hold
   several (royale: 4.49 own relay seats, 82 % win; glacierkeep: 0.14, 18 % win).
   ⚠ **Bounded at two:** the core spawns builders on adjacent tiles, so do not starve
   the spawn ring.
5. **FIX `v529merge`'s SOCKET REGRESSION BEFORE ANYTHING ELSE — it is free points.**
   It never claims a socket in 68 % of yulerune and 33 % of icefloe games where the
   other two arms claim at r2 in 100 % of them, costing **45pp and 40pp** on those maps.
   If v536 ports from v529merge, port the socket behaviour from v534maptrust/v533home.
6. **AURORAVEIL IS THE BUILT-IN FALSIFIER CELL, NOT A BONUS** — it is a third latent
   crater (36 % never-claim across ALL arms, nearest ore 7) at only 55 % win. A correct
   fix must move auroraveil's never-rate to ~0 as well; **if it fixes glacierkeep and
   leaves auroraveil at 36 %, the mechanism story is wrong** and the leg should be read
   as a null on mechanism regardless of the win column.
7. **DO NOT WELD THIS TO A w37 COUNTER** — RANK and TUBE_REPLACE are a separate,
   smaller, statistically unresolved item (§Q3). Sequence the socket plank first; it is
   the larger effect, it is ours to control, and it is opponent-independent.
8. **IF A w37 COUNTER IS LATER WANTED, the trigger is named and narrow:** `RANK_ON`
   fires only when `_enemy_type_at` reads a **live GUNNER or SENTINEL** on the threat
   tile **this round**, inside `RANK_HOME_DSQ = 41`, with **no latch and no memory**,
   capped at one body by a **vision-based election** whose own documented residue is
   that two bodies at opposite edges of an r²=41 band (builder vision r²=20) cannot see
   each other. `EXIT_GUARD_ON` and `STICK_ON` are **False** — build no counter to those.

### The cheapest discriminating test (do NOT re-run 900)

**Gate 1 — MECHANISM, n = 60, one map.** glacierkeep × 30 seeds × 2 seats. The readout
is **not** win rate (hw ±12.6pp at n = 60, useless) but **`never-claims-a-socket %`**,
which is **83–90 % in control and must fall to ~0**. At n = 60 that is a >10σ move and
resolves in one battery. Instrument already built and validated:
`scratchpad/s52_diffstudy/ringtime.py` (column `a_own1_r`/`b_own1_r`; `never` = −1).
**Falsifier: never% stays above 40 %, or `deliv>0` fails to rise from 11 %.**

**Gate 2 — CURRENCY, n = 180/arm, three maps.** glacierkeep + drakkarfjord +
auroraveil × 30 seeds × 2 seats. These three maps hold **100 % of the recoverable
games** for both home arms and the pooled control rate is **37.0 %** (200/540); the
ceiling is ~59 %, hw at n = 180 is ±7.3pp, so a real effect clears comfortably while
the 900-game screen is not yet spent. Add yulerune + icefloe (n = 300) only when
testing a `v529merge`-derived tree.

**Gate 3 — the release bar.** Only then re-run the full 900/arm vs
`bots/_x3r0v169mjolnir`. Gates 1+2 cost **240 of the 900 games** and answer the
mechanism question the screen cannot.

---

## WHAT REFUTED THE COMMISSION'S FRAMING

1. ⛔ **"x3r0's w35→w37 iteration bought ~4pp against our line inside one day."** Not
   supported on a paired test across both arms that have both screens: v533home −3.89pp
   (z = −1.93, p ≈ 0.054), **v534maptrust −0.33pp (z = −0.17)**, pooled −2.11pp
   (z = −1.48, p = 0.14). The banked figure used one arm.
2. ⛔ **"drakkarfjord 17/60 and glacierkeep 15/60 are CRATERS"** — two different
   objects. glacierkeep is **universal** (25/12/18 % across arms); drakkarfjord is
   **arm-dependent** (v529merge reads **58 %** there, +30pp over the home arms, ≈2.4
   per-cell half-widths). And **two unnamed craters are as large**: yulerune
   (v529merge 5 % vs v534maptrust 50 %) and icefloe (8 % vs 48 %).
3. ⛔ **"their ring line eats our siege."** `ring.py` is **byte-identical** in w35 and
   w37, and the channel is not siege — it is **economy**: our conveyor loss rate on
   glacierkeep is **0 %**, our harvesters live, and we deliver **nothing** because their
   *collar barriers* own our core's delivery sockets. Siege is not the mechanism and
   the ring code did not change.
4. ⚠ **"the corners leak plausibly binds here too — v535 may recover these cells."**
   Not visible on the evidence available: `V535POOL` reads glacierkeep **316/360 (88 %)**
   and drakkarfjord **355/360 (99 %)** against the incumbent — **identical to `HOMEPOOL`
   (317/360, 355/360)**. The corners gate moved neither crater map on that denominator.
   *(Not a refutation of v535 vs v169, which is unmeasured — no v535 arm in this screen.)*
5. ⭐ **A SURPRISE, written before it was explained:** the crater maps are not maps we
   are bad at. Against our own incumbent they are our **1st and 3rd strongest** maps
   (91–99 % and 86–88 %) while ragnarok — where we go **180/180 against Mjolnir** — is
   one of our **weakest** (56–67 %). The two rankings are close to inverted, which is
   why "map difficulty" was never the right frame and why the within-map opponent
   controls were the decisive instrument.

---

## ARTEFACTS PRODUCED (not committed)

| path | what |
|---|---|
| `scratchpad/s52_diffstudy/census.tsv` | `tools/replay_census.py` over all 2 700 replays |
| `scratchpad/s52_diffstudy/ringplug.py` | NEW — end-state core-ring socket occupancy, both teams |
| `scratchpad/s52_diffstudy/ring.tsv` | its output, 2 700 rows |
| `scratchpad/s52_diffstudy/ringtime.py` | NEW — per-round ring timeline (independent second walk) |
| `scratchpad/s52_diffstudy/ringtime.tsv` | its output, 2 700 rows |

Both new instruments carry the four validation guards recorded in §Q2 Step 4.

