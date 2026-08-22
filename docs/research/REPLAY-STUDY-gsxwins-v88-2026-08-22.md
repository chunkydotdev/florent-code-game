# REPLAY STUDY — `gsxWins` **v88**, 2026-08-22

**Provenance.** Fresh replay-study subagent, no inherited session context beyond
the named inputs. Commissioned by RESEARCH s55 at ~10:0xZ on a `move_miner`
FIRING (`scratchpad/s55_gsxwins_commission.md`, opened and executed as written).
**Method:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` (the DISCIPLINE
block: MEASURED/EYEBALL labels, a control that must run the other way per
mechanism, retained refutations, the IN-LEG MIRROR CONTROL, ≥2 anchors per
piece). Duplicate-content check per
`docs/research/CUT-116-beltgun-answer-2026-08-21.md` §1.7 (opened).
**Inputs:** `corpus/meta_join.tsv`, `corpus/ladder_games.tsv`,
`corpus/league_matches.tsv`, `corpus/throws.tsv`,
`docs/research/corpus-howto.md`, `tools/replay_census.py` (primitives),
`tools/corpus/replay_autopsy.py` (attribution rule), 100 `.replay26` files.
**Shape and comparison point:** `docs/research/REPLAY-STUDY-kladde-v173-2026-08-22.md`
— every latency/answer number below is computed by the SAME definition so the two
studies are directly comparable.
**Decoders:** reused from s54 rather than re-written —
`scratchpad/s54_klad_lib.py` (event walker over the census primitives: rotate
re-emit guard, never-popped registry, signed 64-bit HP deltas) and
`scratchpad/s54_klad_autopsy.py` (self-checking core-damage ledger). New this
session: `scratchpad/s55_gsx_pool.py` (frozen pool), `scratchpad/s55_gsx_main.py`
(per-game pass), `scratchpad/s55_fwd.py` (forward-turret answer latency, both
directions, one function), `scratchpad/s55_fp.py` (content fingerprints).
**Platform writes: none.** Reads: `fcode match replay` × 8 matches (40 games),
archive-first, paced 2 s, declared budget ≤ 8 matches and not exceeded; no
matches fired, no submission, no activation. No queue / bot / `coordination.md`
edits, no commits.
**Clock:** all times UTC from `date` in-shell. Pool **FROZEN 2026-08-22
09:56:10Z** (corpus keeper is live and appending under the analysis; every number
below is computed on the frozen list). Pool-B downloads completed 09:57:14Z.
Repo HEAD at write time `031209d1f`.

---

## 0. THE POOL, AND WHAT IT IS NOT

| | games | matches | surface |
|---|---|---|---|
| **POOL A** — archived gsxWins-v88 games at the freeze | 60 | 12 | 45 rated + 15 unrated |
| **POOL B** — 8 matches pulled by hand from opponents that BEAT v88 | 40 | 8 | rated ladder |
| **TOTAL** | **100** | **20** | **85 rated / 15 unrated** |

Opponents: OpenSverige 30, Ouroboros 10, kladde 10, Lorem Ipsum 10, 0033 5,
Atlas 5, Focalground 5, TRRR 5, Jython 5, Leviathan 5, Erebus 5, Flotte 5.

⚠ **THE POOL IS NOT A SAMPLE OF THEIR LADDER.** gsxWins' game share **inside this
pool is 45/100**; their **true v88 league-wide share is 155–155 = 0.500 over 62
matches** (`corpus/league_matches.tsv`, all teams, 2026-08-21T23:31:10Z →
2026-08-22T09:41:10Z). Pool A over-weights us (30 of 60) where they are near
perfect; Pool B was **selected on their losses on purpose**, to answer Q2. Every
per-opponent cell below carries its own n; **no pooled win rate in this document
is an estimate of their ladder strength.** The league-wide row is.

gsxWins' side index is derived from `teamAName` in the platform metadata, never
from any winner-derived field (`corpus-howto.md` TRAP 7). The exact string
`gsxWins` is used, and the exact string `OpenSverige` for us.

---

## 1. INSTRUMENTS — EVERY CONTROL RUN BEFORE ANYTHING WAS BELIEVED

### 1.1 KNOWN-CELL VALIDATION (commission bar: reproduce a recorded fact first)

Own decode path vs `corpus/ladder_games.tsv` on our six archived rated matches
against v88 — **turns, `win_condition` and whether WE won, per game**:

```
06a47ce9 · 26fa2f6c · 2d6031f6 · 3076ae8e · f6e8c637 · f716af2d
30 games x 3 fields = 90 of 90 cells EXACT, 0 mismatches
```

**It discriminates in both directions rather than only confirming losses:** the
30 cells contain **5 wins and 25 losses**, **2 distinct win conditions**
(`core_destroyed` 26, `titanium_collected` 4) and turns spanning **104 … 1000**.
A decoder that got the seat backwards, or that read the winner off a
winner-derived field, fails on the 5 wins.

### 1.2 THE DAMAGE LEDGER SELF-CHECKS

`s54_klad_autopsy.py` requires attributed damage (FireTurret / BuilderAttack
resolved against **round-start** occupancy) to equal the summed negative
`UpdateHp` deltas on the core id. **MEASURED: 151 of 154 non-empty core ledgers
match exactly; 3 mismatch, all in the SAME direction (attributed > true) and all
by exactly 18 or 36 — one or two sentinel shots.** ⇒ overkill on the killing
round, where the engine clamps the HP delta at the core's remaining HP.
**REPORTED, not hidden**; it biases attributed damage upward by ≤ 0.2 % of the
pooled total and cannot move any conclusion here.

### 1.3 AN INSTRUMENT BUG FOUND AND FIXED, WITH ITS SIZE

The first version of `s55_fwd.py` keyed forward turrets `tile → single id`. A
tile can host SEVERAL turrets over a game (build → die → rebuild), and every
answer landed on an earlier occupant was silently dropped. **MEASURED: 59 of
Leviathan's 98 forward turrets share a tile with another**, and the bug read
Leviathan's answer rate as **8.2 %** where the fixed instrument reads **21.4 %**.
Our own cell moved only 88.2 % → 90.2 % (1 duplicate tile in 51). **Every number
in this document is post-fix.** The tell that exposed it was a
**removed-without-ever-being-answered** count that the fixed instrument drives to
zero on both of the cells that matter (below).

### 1.4 IN-LEG MIRROR CONTROL (playbook, s53 addition)

Every geometry / latency instrument below is run **side-swapped on the same
files by the same function**. Two sanity properties held, i.e. the side
assignment is behaviourally consistent and not a mirror of itself:

```
conveyors sit near their builder's OWN core on both sides   median d2  17 gsx / 26 opponent
barriers  sit near the ENEMY core on both sides             median d2   5 gsx /  5 opponent
```

And the free positive control the swap buys: **`removed` vs `answered` are
independent columns and both verdicts occur.** gsxWins' forward turrets are
*removed-with-no-damage-ever-recorded* in **0 of 429**; ours in **0 of 51**;
**Leviathan's in 67 of 98** (they recycle their own turrets with the free
`destroy()`). A column that only ever said "combat death" would be unchecked;
this one says both.

### 1.5 DUPLICATE-CONTENT SHARE (CUT-116 §1.7) — **1.0 %, on a validated instrument**

Fingerprint = full gameplay event stream (builds, moves, builder verbs, ammo
converts, deaths, fires) + map dims + game length, SHA-1; `BotOutput` excluded.

```
FULL gameplay fingerprint (both sides)   100 -> 99 distinct   1 dup (1.0%)
GSX-ONLY whole-game fingerprint          100 -> 99 distinct   1 dup (1.0%)
```

The duplicate pair is **`7437cb82…_game_3` and `dda6a69a…_game_4`** — the same
Ouroboros content reached us twice (one unrated challenge at their v119, one
ladder match at their v118). **CONTROLS, because a near-zero that cannot be
non-zero is not a measurement:** degenerate fingerprint (map + length only)
→ 100 → 89 distinct, **11 duplicates (11.0 %)**; same file decoded twice →
identical (True); side-swapped fingerprint of the same file → different (True).

### 1.6 CORPUS TRAPS AVOIDED

`econ.tsv`'s `shots` and `deliveries` (TRAPS 5/8, both identically zero) are not
used; titanium collected is read from `Player` field 4 in the replay.
`meta_join` is used for FILE→match→team attribution only, never for a rated
win-rate denominator; rated denominators come from `league_matches.tsv` and
`ladder_games.tsv`. `ladder_games.seat` (TRAP 7) is never read.

### 1.7 CLUSTER ENUMERATION, IN WRITING (per the DEFF procedure)

Named clusters in this data: **MATCH** — LIVE (5 games per match, verified: games
per match = exactly 5 for all 20 matches). **OPPONENT** — DEAD for the two
headline comparisons, which are within one opponent pair (us vs gsxWins), LIVE
for any pooled field number, which is why no pooled field number carries an
interval here. **MAP** — LIVE across matches (15 distinct maps over 100 games);
handled by clustering at MATCH, which strictly contains it for the 5-game
within-match set. **CONTENT-DUPLICATE** — measured at 1.0 % (§1.5), one pair,
below the resolution of anything claimed.
⇒ **Both headline intervals below are MATCH-cluster bootstraps (20,000 resamples
of whole matches), not DEFF-scaled turret counts.** The DEFF-1.366 turret-level
form is quoted alongside as a floor and is **narrower**, i.e. the bootstrap is
the conservative one. Both are EXCLUSION claims (a difference excludes zero), so
the direction rule is satisfied without restatement.

---

## 2. PREMISE AUDIT

### 2.1 Q3d(a) — *"is v88 continuous with earlier gsxWins versions?"* **VERIFIED, and the break is at v53→v65, not at v88.**

13-dimensional their-side profile per game (count + first-build round for
conveyor / harvester / gunner / sentinel / barrier, builder spawns, barriers on
the enemy core's 8-tile spawn ring, turrets planted at d²≤13 of the enemy core),
MAD-scaled L1 between group medians (MAD floored at 1.0), permutation null of
3,000 re-splits at the same group sizes. **Opponent held fixed at OpenSverige**
so the comparison is not a comparison of who they played.

| comparison | nA | nB | d | null med | null p95 | p | verdict |
|---|---|---|---|---|---|---|---|
| **v87 vs v88** | 20 | 30 | 0.252 | 0.405 | 0.608 | **0.952** | **SAME** |
| **v65 vs v88** | 60 | 30 | 0.350 | 0.399 | 0.569 | **0.710** | **SAME** |
| v53 vs v88 *(control)* | 30 | 30 | 0.597 | 0.330 | 0.545 | **0.024** | DIFFERENT |
| v53 vs v65 *(control)* | 30 | 60 | 0.493 | 0.298 | 0.482 | **0.039** | DIFFERENT |

Medians, vs-us games only:

| dim | v53 (30) | v65 (60) | v87 (20) | **v88 (30)** |
|---|---|---|---|---|
| gunners / game | 3 | 6 | 6.5 | **6** |
| sentinels / game | 2 | 2 | 2 | **2** |
| first gunner round | 10 | 11 | 10 | **13.5** |
| first sentinel round | 73.5 | 122 | 114 | **76** |
| barriers / game | 6.5 | 10 | 8.5 | **9** |
| barriers on OUR core's spawn ring | 6 | 7 | 7 | **7** |
| builder bots / game | 5 | 6 | 8 | **7** |

⇒ **v88 is the v65 doctrine, unchanged in kind, since 2026-08-18T01:32:59Z.**
Pooling **v65→v88 for DOCTRINE claims is legitimate; every headline number below
is nevertheless v88-only, as commissioned.** Our share against that whole block:
**22–88 games = 0.200 over 22 matches** — which is where the commission's "20.0 %
modern" comes from; **v88 alone is 5–30 = 0.167 over 6 matches.**

### 2.2 Q3d(b) — *"gsxWins is a launcher-family bot (r≤2 launcher, 100 % of games)"* — ⛔ **REFUTED FOR v88, AND THE DATE IT DIED IS MEASURED.**

**MEASURED, 15-game random samples per version, plus the full v88 pool:**

```
v22  15 games sampled   23 launchers   15/15 games with >=1 launcher   <- the note's era (2026-08-08)
v39  15 games sampled    0 launchers    0/15
v46  15 games sampled    0 launchers    0/15
v53  15 games sampled    0 launchers    0/15
v65  15 games sampled    0 launchers    0/15
v87  15 games sampled    0 launchers    0/15
v88  ALL 100 pool games   0 launchers    0/100     (and 0 splitters in 100/100)
```

⇒ **The repo's launcher-family label was TRUE at v22 and has been dead since at
least v39 (2026-08-14).** It is 8 days and ~6 versions stale and must not be
cited as current doctrine. **gsxWins v88 cannot kidnap us. Their kidnap risk to
us is exactly zero.**

### 2.3 THE COMMISSION'S "VERIFIED FACTS" — confirmed, with two numeric corrections

**(i) "their current version IS v88."** CONFIRMED and **the window is CLEAN** —
**62 of 62 ladder matches since 2026-08-21T23:31:10Z are v88**, zero interleaved
prototype versions. This is the opposite of kladde v173 (8 prototype interleaves
in 19.5 h). ⇒ **A pinned leg against gsxWins is cheap right now; a time-window
filter happens to be safe on this holder, but pin anyway.**

**(ii) "our rated record vs v88 TODAY: 2-3, 0-5, 1-4, 0-5, 1-4, 1-4 = 5/30."**
**EXACT.** Reproduced game-for-game from `ladder_games.tsv` and independently
from the replays (§1.1). The 0-5 attributed to v179 is `f6e8c637` (05:31:10Z) —
confirmed, our v179 met v88 once and was swept.

**(iii) "their rating ~1869, gap +38, a 5-0 pays +17.56."** **STALE BY ~15 Elo.**
At the last pairing in the tape (09:41:10Z): **gsxWins 1854.04, OpenSverige
1823.96, gap +30.09**, so a 5-0 pays **+17.38** and a 0-5 costs **−14.62**. Same
order, same conclusion — the target is reachable and worth a leg.

**(iv) The framing needs the same correction the kladde study needed, and it is
the most important sentence in this study.** gsxWins v88 is **not** a bot that
beats everyone:

| population | gsxWins game share |
|---|---|
| **v88, league-wide, 62 matches** | **155–155 = 0.500** |
| **v88 vs OpenSverige, 6 matches** | **25–5 = 0.833** |
| **v65→v88 block vs OpenSverige, 22 matches** | **88–22 = 0.800** |

Their next-best matchup on v88 is **0033 at 0.867 (n=15 games, 3 matches)** and
then **Focalground 0.650 (n=20)**; at the other end **kladde .200, Lorem Ipsum
.200, Jython .200, Leviathan .300, Erebus .360, Flotte .400, Ouroboros .400**.
⇒ **This is an exactly average ladder bot that happens to be our second-worst
matchup.** 0033's cell is n=15 with no real denominator; **against every opponent
with ≥20 games, we are their best result on the ladder.**

---

## 3. Q1 — HOW THEY BEAT MJOLNIR

### 3.1 It is **NOT** one channel, and that is the answer to the commission's question. **MEASURED.**

Damage into the losing core, from the self-checking ledger:

| | sentinel | gunner | builder attack |
|---|---|---|---|
| **dealt BY gsxWins** (42 kills) | **36,702 (84.6 %)** | 4,151 (9.6 %) | **2,520 (5.8 %)** |
| dealt TO gsxWins (46 kills) | 25,920 (80.7 %) | 5,614 (17.5 %) | 578 (1.8 %) |
| **dealt by gsxWins to OUR core** (23 kills) | **13,698 (71.5 %)** | **3,661 (19.1 %)** | **1,802 (9.4 %)** |

**Dominant channel PER GAME, across the 87 games where they put ≥1 point on an
enemy core: sentinel 53, builder melee 24, gunner 10.** ⇒ **kladde's kill is one
obstacle-immune sentinel and nothing else (98.3 % / no second channel). gsxWins'
is a COUSIN, not the same class: sentinel-led but genuinely three-channel, and
in 24 of 87 games the CORE IS KILLED BY BUILDER BOTS PUNCHING IT.**

### 3.2 The invariant is not the weapon. It is **AN EMPLACEMENT PARKED ON THE DOORSTEP THAT WE NEVER REMOVE.**

**MEASURED, whole pool:** their first gunner goes up at **median r9, d²=17 from
their OWN core** — a home guard, not the kill. From ~r30 onward every turret is
planted essentially **on the enemy core**, and it is a **step, not a creep**:

| build band | gunner n | median d²-to-enemy-core as a fraction of core-to-core d² | sentinel n | same fraction |
|---|---|---|---|---|
| r0–30 | 108 | 0.755 *(their own half)* | 24 | 0.646 |
| r30–80 | 131 | **0.062** | 34 | **0.018** |
| r80–150 | 130 | **0.062** | 35 | **0.020** |
| r150+ | 231 | **0.103** | 72 | **0.031** |

Absolute: **across all 100 games the median damaging sentinel sits at
d² = 10 from the victim core's NW tile, the median damaging gunner at d² = 4, and
the median top-damage emplacement of ANY kind at d² = 5 (d² = 6.5 vs us).** kladde's kill sentinel sits at d² ≤ 32–50 and shoots through walls;
**gsxWins walks up and shoots point-blank.**

**Kill-arc anchors — four of today's/overnight's sweeps, three channels, both of
our lineages, all opened:**

| file / game | our ver | map, cores | mechanism, round by round |
|---|---|---|---|
| `06a47ce9-…_game_4` (5–0) | v176 | 30×30, gsx (2,2) / us (26,26) | home gunner r10 (5,5) · **sentinel r72 at (28,24), d²=8 from our core — NEVER DIES** · first core hit **r73** · gunner r77 at (27,25), **d²=2 — NEVER DIES** · 522 + 231 dmg · core dead **r129**. Our builds: **8 launchers, 2 sentinels, 0 gunners**; our ferry chain built-and-destroyed a launcher every 2 rounds from r1 to r9. |
| `06a47ce9-…_game_3` (5–0) | v176 | 20×20, gsx (1,16) / us (17,2) | home gunner r7 · **gunner r45 at (16,3), d²=2 from our core — never dies — 742 dmg from r78 to r183** · gunner r46 (15,4) d²=8, r84 (14,3) d²=10, r102, r135, r151 · core dead **r183**. **A 20-Ti gunner killed a 500-HP core alone.** |
| `f6e8c637-…_game_1` (5–0, the v179 leg) | **v179** | 20×20, gsx (16,17) / us (2,1) | **sentinel r44 at (5,0), d²=10 — 720 dmg r45–r123, dies r124** · **gunner r71 at (1,3), d²=5** — killed r73, **rebuilt on the same tile r125, killed r135, rebuilt AGAIN r167 — 504 dmg r192–r263** · core dead **r263**. **The tile matters, not the unit: they re-buy the same square three times.** |
| `26fa2f6c-…_game_4` (4–1) | v176 | 30×30, gsx (14,2) / us (14,26) | **NO TURRET TOUCHES OUR CORE.** Two builder bots stand at **(13,26) d²=1 and (13,27) d²=2** and punch: **250 + 250 dmg from r95 to r220.** Their gunners at r50/r51/r87 sit at d²=9/5/5 and never die. Core dead **r220**. Our builds: **4 launchers, 0 turrets.** |
| `f716af2d-…_game_5` (4–1) | v176 | 16×16, gsx (7,1) / us (7,13) | **ONE builder bot at (8,12), d²=2, from r47 to r473 — 504 damage, alone.** Core dead **r473**. |

**The immortality is real but it is SYMMETRIC and therefore not the asymmetry.**
MEASURED: the top-damage emplacement survives to the end of the game in **59/87
(67.8 %)** of their attacks and **47/67 (70.1 %)** of attacks on them. What is
**not** symmetric is where it stands (d² 5 vs 13) and whether it exists at all
(§4).

### 3.3 The barrier ring on the ENEMY core — present, and its mechanism is the one kladde's was

**MEASURED: gsxWins builds 957 barriers over 100 games and the MEDIAN one sits at
d² = 5 from the ENEMY core — this is not a home wall, it is a collar. 578 of the
957 fall inside the (−1…2)² box around the enemy core's NW footprint tile; ≥1
barrier at d²≤2 of the core in 89 of 100 games (88 of 100 take one of the 8
orthogonal ring tiles); median round of the first one r41.** The offset histogram
is **the 8 orthogonal spawn tiles and almost nothing else** — the four diagonals
total 21 placements against 557 on the orthogonals:

```
        dx=-1    dx=0    dx=1    dx=2
dy=-1      8      83      76       9
dy= 0     77       -       -      58
dy= 1     62       -       -      59
dy= 2      2      73      69       2
```

| ring tiles gsx took | n | gsx win % | median ENEMY `titanium_collected` | enemy builder spawns / 100 r |
|---|---|---|---|---|
| 0 | 12 | 25 % | 2,620 | 2.33 |
| 1–2 | 14 | 7 % | 3,005 | 2.29 |
| 3–4 | 15 | 53 % | 1,340 | 2.45 |
| **5+** | **59** | **56 %** | **540** | **1.90** |

**⛔ THE SPAWN-LOCK MECHANISM IS REFUTED HERE TOO AND IS RETAINED SO NOBODY
RE-DERIVES IT:** enemy builder spawns per 100 rounds move only 2.33 → 1.90 as the
ring fills, i.e. the ring does **not** stop them spawning. What survives is the
**delivery aperture** (INFERENCE, from the table; MEASURED part is the two
columns): enemy `titanium_collected` collapses 2,620 → 540. Under
`R1000_IS_DEFEAT` that is worth little to us directly — it is how they take the
12 % of games that reach r1000. **This replicates the kladde v173 finding on an
independent bot, which is the first time this project has seen the same ring
mechanism twice.**

### 3.4 Their answer machinery is a **GARRISON**, not kladde's **REFLEX** — MEASURED, and the two studies now separate cleanly

Across 235 answered forward turrets, the **median age of gsxWins' responder at
the moment it fires is 64 rounds**, and **79 % of responders are older than 10
rounds**. Responder type: **builder 138, gunner 75, sentinel 22.**

kladde, same instrument, same definition: **median responder age 2 rounds**,
responder type sentinel 235 / gunner 226 / builder 82.

⇒ **kladde builds a fresh counter-battery on top of your new turret within ~2
rounds. gsxWins already has a standing gunner screen and a builder next to it,
and walks the builder over.** (INFERENCE on the words "reflex" / "garrison";
MEASURED part is the responder-age distribution and the type split.)

---

## 4. Q2 — WHERE v88 CRACKS

### 4.1 ⭐⭐ THE ANSWER-LATENCY AXIS, MEASURED THE SAME WAY AS THE KLADDE STUDY

Definition (identical to `REPLAY-STUDY-kladde-v173-2026-08-22.md` §4.1): a
*forward turret* is a gunner or sentinel built within d²≤50 of the opposing core.
*Answered* = the defending side lands ≥1 damage event on it. Both directions
computed by the **same function on the same files**.

| direction | n forward turrets | answered | median latency | removed | **answered-then-removed** | median life |
|---|---|---|---|---|---|---|
| **gsxWins' forward turrets → answered by US** | **147** | **53.1 %** | **4.5 rounds** | 40.8 % | **40.8 %** | **36 rounds** |
| **our forward turrets → answered by gsxWins** | **51** | **90.2 %** | **3.0 rounds** | 72.5 % | **72.5 %** | **10 rounds** |
| gsxWins' forward turrets → answered by the field (11 opps) | 429 | 62.2 % | 5 | 56.2 % | 56.2 % | 27 |
| all opponents' forward turrets → answered by gsxWins | 430 | 54.7 % | 4 | 62.6 % | 41.2 % | 18 |

**Answer-rate difference against us: 37.1 pp.
MATCH-cluster bootstrap 95 % CI (20,000 resamples, 6 matches per arm):
[+23.7 pp, +51.8 pp] → EXCLUDES ZERO.** *(The DEFF-1.366 turret-level
two-fixture half-width is 18.0 pp — narrower, quoted only as a floor; the
bootstrap is the number to cite.)*

**⭐ SIDE BY SIDE WITH KLADDE, WHICH IS THE POINT OF MEASURING IT THE SAME WAY:**

| | answers OUR forward turret | we answer THEIRS |
|---|---|---|
| **kladde v173** | **96 % in 1 round**, 94 % removed, life 6 | **26 % in 14 rounds**, 27 % removed, life 38 |
| **gsxWins v88** | **90 % in 3 rounds**, 73 % removed, life 10 | **53 % in 4.5 rounds**, 41 % removed, life 36 |

⇒ **The asymmetry is real against both, and it is SMALLER against gsxWins —
we answer them twice as often and three times faster than we answer kladde.**
Our answer machinery is not the binding constraint in this matchup. The next
section is.

### 4.2 ⭐⭐ THE BINDING CONSTRAINT IS **SENTINEL-ROUNDS ON TARGET**, AND WE DELIVER NINE

Define *on-target turret-rounds* = rounds a turret is alive **and** within its
own firing range of the nearest enemy-core footprint tile (sentinel d²≤32, gunner
d²≤13). Computed by the same function on both sides.

| | median sentinel-rounds on target | median gunner-rounds on target |
|---|---|---|
| **US → gsxWins' core** (30 games) | **9** | **0** |
| **the field → gsxWins' core** (70 games) | **76** | 0 |
| gsxWins → our core (30 games) | 56 | **105** |
| gsxWins → the field's cores (70 games) | 6 | 28 |

And it is monotone where it matters (all 100 games, MEASURED; INFERENCE on the
causal reading):

| opponent sentinel-rounds on target | n | **gsxWins' core killed** | our share of the cell |
|---|---|---|---|
| 0 | 27 | **3.7 %** | 11/27 |
| 1–50 | 22 | 31.8 % | 11/22 |
| **51–200** | **37** | **86.5 %** | 4/37 |
| 200+ | 14 | 42.9 % | 4/14 |

*(The 200+ cell falls back because those are long games where the defender heals
through a lone sentinel — 3076ae8e g1 is the clean anchor in the mirror: their
sentinel at (7,16) put **5,454 damage** into our 500-HP core over ~930 rounds and
we healed through all of it, then lost the game on `titanium_collected`.)*

**22 of our 30 games sit in the two bottom cells.** That is the crack, stated as
a quantity we control.

### 4.3 THE HEADLINE INDICTMENT: **WE DO NOT ARRIVE — AND WHEN WE DO ARRIVE, WE DON'T HIT**

*"Did we ever put one point of damage on gsxWins' core?"* — MEASURED, whole pool:

| opponent | games | reached their core | median round of first damage | median total damage into their core | gsx win % |
|---|---|---|---|---|---|
| kladde | 10 | **100 %** | r216.5 | 504 | 0 % |
| 0033 / Jython / Erebus / Flotte / Atlas | 5 each | **100 %** | r31–r124 | 281–621 | 0–40 % |
| Lorem Ipsum | 10 | 90 % | **r24** | **1,015** | 20 % |
| Leviathan | 5 | 80 % | r206 | 504 | 20 % |
| Ouroboros | 10 | 60 % | r64 | 567 | 40 % |
| Focalground | 5 | 40 % | r117 | 0 | 60 % |
| **OpenSverige** | **30** | **36.7 %** | r11 | **0** | **83.3 %** |
| TRRR | 5 | **0 %** | — | 0 | 80 % |

**Us 36.7 % vs the six Pool-B crack opponents 95.0 % → difference 58.3 pp,
MATCH-cluster bootstrap 95 % CI [+45.8 pp, +70.8 pp] → EXCLUDES ZERO.**
*(Pool B is selected on their losses; the claim is about REACH, which is a
property of the challenger's offence, but the cell selection still inflates it —
read the interval as a bound on "the teams that beat them arrive and we don't",
not as a field average.)*

**⭐⭐ AND THE SECOND HALF IS WORSE THAN THE FIRST, BECAUSE WE *DO* GET THERE.**
MEASURED, orthogonal adjacency to the enemy core (the tile from which
`can_fire` / builder attack is legal):

| | games with ≥1 builder-round orthogonally adjacent to the enemy core | median builder-ROUNDS spent there | **games with ≥1 builder attack ON the core** |
|---|---|---|---|
| **US → gsxWins** (30) | **28 / 30** | **219** | **0 / 30** |
| gsxWins → us (30) | 25 / 30 | 24.5 | **13 / 30** |
| gsxWins → field (70) | 69 / 70 | 41.5 | 37 / 70 |
| field → gsxWins (70) | 57 / 70 | 15 | 9 / 70 |

**Our builders stand next to gsxWins' core for a median of 219 rounds a game and
attack it ZERO times in 30 of 30 games.** And it is not that our melee is off —
**we issue 115 builder attacks per game; they land on barriers (48.5 %),
conveyors (32.0 %), gunners (11.1 %), sentinels (3.8 %) and empty tiles (4.7 %).
Enemy core: 0.0 %, 0 of 3,459.** The control that makes the zero mean something:
**gsxWins directs 9.2 % of its 21,712 builder attacks at the enemy core (1,999
attacks = 3,998 damage); the rest of the field directs 5.7 % of 6,210.** The
instrument fires on two independent populations and reads exactly zero on ours.

**Worked anchor, opened: `f716af2d_game_4`.** Our builder #4 is ferried to (1,5),
orthogonally adjacent to their core tile (2,5). It lives 185 adjacent rounds. It
attacks **(2,4)** four times (r11–r14 — the tile *north* of the core, a
conveyor), then **(1,7)** thirty-one times (r22–r68 — a barrier), then heals
r116–r128. **It never once targets (2,5).** (MEASURED per-event; INFERENCE that
this is target-selection precedence rather than a legality problem — the legality
is settled by gsxWins doing it 1,999 times from the same geometry.)

⇒ **In this matchup our offence failure is not "we cannot reach". It is "we reach
and then do something else."** At 2 Ti per attack, 219 adjacent rounds is **438
damage for 438 Ti** — most of a 500-HP core, on a resource line where we bank a
median of 670 collected.

### 4.4 The two shapes that actually beat them, with anchors

**SHAPE 1 — the early max-range sentinel that is never contested
(`Lorem Ipsum` v57; gsx 4–16 in the block, 2–8 in the pool).** MEASURED:
`3c91a2b2_game_4` (12×12, gsx core (1,1)): **sentinel planted r8 at (6,6) — d²=32
to the nearest core footprint tile, i.e. EXACTLY maximum sentinel range — never
answered, never removed, 1,674 damage from r9 to r251.** gsxWins built **zero
turrets** all game. Second anchor `0a389ace_game_3` (20×20): sentinels r41 (1,0)
d²=2 and r49 (2,0) d²=1, both never removed, 558 + 198 dmg, gsx core dead
**r112**.

**SHAPE 2 — the gunner staircase that walks in under the screen
(`Erebus` v180/v181, `kladde` v173).** MEASURED: `2bb034d1_game_2` (16×16) —
Erebus plants **11 gunners between r11 and r142**, losing most of them (r18, r26,
r26, r63, r64, r64, r109, r126, r136, r153) but each one nearer, until **r150 and
r155 sentinels at d²=10 and d²=8 finish the core at r180**. `a9985298_game_4` —
kladde plants sentinels at r97/r107 at d²=37/36 and takes the core at **r136**.
**Attrition through the screen works; it costs a dozen turrets.**

**What the two shapes share, and it is the single actionable sentence:
gsxWins' answer is a GUNNER screen (r²=13, obstacle-BLOCKED). A sentinel sitting
at d² 14–32 of their core is outside that screen's reach and inside its own.**
⚠ **HEDGE, because the direct test does not fully support the clean version:**
early (<r60) opponent sentinels in that d² 14–32 band are still answered 28/33
and removed 25/33 — gsxWins *can* walk a builder or a new gunner out to them.
**What the band buys is TIME, not immunity**, and time is what §4.2 says the
account is short of.

### 4.5 ⛔ WHAT DOES NOT WORK, MEASURED ON LIVE GAMES (road closures, point 6 satisfied)

* **THE LAUNCHER LINE IS INERT AGAINST THEM — the same verdict the kladde study
  reached, on a different bot.** In our 30 v88 games (`corpus/throws.tsv`, the
  corpus's own decoder, 27 of 30 files covered): **795 throws — 673 kidnaps of
  gsxWins builders and 122 self-inserts. Total core damage attributable to any
  thrown bot: ZERO** (`core_atk` sums to 0 over all 795 rows). 37 of 122
  self-inserts "reached". Median 4 launchers per game against a median of **1**
  turret.
* **CRASH-INDUCTION DOES NOT WORK ON THEM — MEASURED, with the positive control
  that makes the zero mean something.** Of 673 kidnaps, **57 were thrown to a
  border tile; 9 of those victims eventually died, and 0 of the 42 total dead
  victims carry the crash signature** (`vfate=DIED` with `vhp=0`, i.e. removed
  with no HP event in the tracked window). **Corpus-wide the same instrument
  reads 701 of 17,052 = 4.1 %**, so it CAN return the other verdict.
  **Median life after the throw among the dead is 41.5 rounds and NONE died
  within 1 round** — these are ordinary later combat deaths, not unhandled
  exceptions. ⇒ **gsxWins' code survives an off-map neighbourhood; spend the
  border-throw budget elsewhere.**
  ⚠ **n = 42 dead victims. A 0/42 is consistent with a true rate up to ~7 %
  at 95 %; it excludes a HIGH rate, not a small one.**
* **THEY CANNOT BE KIDNAPPED BACK, AND THEY NEVER TRY** — 0 launchers and 0
  splitters in 100 of 100 games (§2.2).
* **THE BARRIER-FORM SPAWN LOCK** — refuted again in §3.3, retained.
* **DESTROYING THEIR FORWARD TURRETS IS NOT THE LEVER.** Their forward-turret
  removal rate against us (72.5 %) is already close to their rate against the
  field (56.2 %), and the per-opponent kill rate is not monotone with outcome
  (Atlas removes 94.3 % of gsxWins' forward turrets and still loses 3–2). The
  monotone variable is §4.2's on-target turret-rounds, ours.

---

## 5. Q3 — PLAY-THE-PLAYERS TABLE (gsxWins v88, 100 games, freeze 09:56:10Z)

| quantity | value | denominator / caveat |
|---|---|---|
| **League-wide game share, v88** | **0.500 (155–155)** | 62 matches, all opponents, `league_matches.tsv` |
| **Game share vs OpenSverige, v88** | **0.833 (25–5)** | 6 matches; **their best matchup with a real denominator** |
| — same, v65→v88 block | **0.800 (88–22)** | 22 matches |
| Rating at the last pairing (09:41:10Z) | **1854.04** vs our 1823.96, gap **+30.09** | a 5-0 pays **+17.38**, a 0-5 costs −14.62 |
| Wins that are core kills | **93 %** (42/45) | pool |
| **Median kill round** | **r218.5** | 42 kills; ≤r300 = 74 %, ≤r200 = 33 % |
| **Timely-kill rate (core kill by r300 / ALL games)** | **31.0 %** | 31/100 — the PROGRAMME primary, computed for them |
| — same, vs us | **60.0 %** (18/30), median kill **r236** | they kill us twice as reliably as they kill the field |
| **r1000 share** | **12.0 %** (12/100) | 4 of them vs us; they won 3 of the 12 |
| **Deterministic opening** | **builder bot at r0, r1 and r2 in 100 / 100 games** | 3 spawns in the first 3 rounds; only variation is whether the first conveyor lands r1 or r2 |
| First conveyor | **r2** | 100/100 |
| First harvester | **r14.5** (r14 vs us) | 100/100 |
| **First gunner (home guard)** | **r9, d²=17 from their OWN core** | 97/100 |
| First sentinel | **r70** (r60 vs us) | 66/100 — **34 of 100 games contain no gsxWins sentinel at all** |
| First barrier | r37 (99/100 games); **first barrier at d²≤2 of the enemy core r41** | 89/100 games at d²≤2; **88/100 take ≥1 of the 8 ORTHOGONAL ring tiles** |
| First turret planted at d²≤13 of the ENEMY core | **r64** (r73 vs us), in **85 %** of games (90 % vs us) | median 2.5 such turrets/game (3 vs us) |
| Builds / game (median) | conveyor **29** · barrier **8** · **gunner 5** · harvester **4** · builder bot **6** · sentinel **1** · **launcher 0** · **splitter 0** | 100 games |
| — vs us | conveyor 25 · barrier 9 · **gunner 6** · harvester 4 · builder 7 · sentinel 2 | 30 games |
| Shots / game | **gunner 76.2, sentinel 30.2** | vs OUR 8.9 / 57.7 and the field's 74.5 / 43.4 |
| Ammo converted / game | 692 Ti | vs our 763 |
| Builder attacks / game | **217** — of which **9.2 % target the enemy CORE** | vs our 115 with **0.0 %** on the core |
| **Reaction latency to a forward turret at their core** | **median 4 rounds league-wide / 3 rounds vs us; 41 % / 73 % removed after an answer** | 430 / 51 turrets |
| Their exposure to the same stimulus | answered **53.1 %** by us, median **4.5 rounds**, **40.8 %** removed | 147 turrets |
| **Responder age when it fires** | **median 64 rounds old; 79 % older than 10 rounds; responder is a BUILDER 59 % of the time** | 235 answered turrets — **a garrison, not kladde's 2-round reflex** |
| **Crash-class susceptibility** | **0 of 42 kidnapped-and-dead builders show the crash signature** (corpus baseline 4.1 %) | 673 kidnaps, 57 border throws |
| **Version churn** | **62 of 62 matches on v88** since 2026-08-21T23:31:10Z — no prototype interleave | pin anyway (`--match <past_match_id>`) |
| Duplicate-content share in this pool | **1.0 %** (1 pair) | §1.5 |

---

## 6. Q4 — THE SKALMAN READ

Stated as *supported-by-data*, not as prescription. Incumbent context read before
writing: `HANDOVER.md` s54 block — v176 "Mjolnir rotfix w77" and v179 hold the
recent slots, `_v542wave` is the frozen rush benchmark, and **Skalman is the new
line: Bean-counters replication = cage + eco-denial.**

**S1. THE CAGE HALF OF SKALMAN IS gsxWins' OWN GAME, AND THEY ALREADY RUN IT
BETTER THAN THE DOCTRINE PREDICTS.** They put ≥1 barrier on the enemy core's
orthogonal spawn ring in **88 of 100 games from a median r41**, and the ring is **the 8
orthogonal tiles and nothing else** (21 diagonal placements against 557
orthogonal). Enemy `titanium_collected` collapses **2,620 → 540** as it fills.
**And it is NOT a spawn lock** — enemy builder spawns move only 2.33 → 1.90 per
100 rounds. ⇒ **A Skalman that brings a cage to this matchup brings their game,
into a `titanium_collected` tiebreak that `R1000_IS_DEFEAT` says we do not want,
against a bot that reaches r1000 in 12 % of its games.** This is the second
independent bot on which the ring-as-spawn-lock reading has now failed; treat it
as closed for cage design.

**S2. THE VERB OF THEIRS THAT BEATS A CAGE IS THE POINT-BLANK EMPLACEMENT, AND A
COLLAR DOES NOT STOP IT.** 84.6 % of their core damage is sentinel (line ignores
obstacles, rules-level) and a further **5.8 % is a builder bot standing on the
collar's own tile and punching** — `f716af2d_game_5` is one builder, 504 damage,
alone. **A barrier collar is a body-blocker; two of their three channels do not
need a body-free lane.** (INFERENCE on "does not stop it"; MEASURED inputs are
the channel split and the two builder-kill anchors.)

**S3. WHAT THE DATA SUPPORTS AS THE COUNTER-SHAPE — one plank, and it is
embarrassingly cheap.**

* **(a) ⭐ MAKE THE ADJACENT BUILDER PECK THE CORE.** We already put a builder
  orthogonally adjacent to their core in **28 of 30 games for a median 219 rounds
  a game**, and it attacks the core **0 times in 30 of 30 games** while issuing
  115 attacks a game at barriers and conveyors. gsxWins does the same thing with
  9.2 % of its attacks; the field with 5.7 %. **This is a target-precedence
  change, not a new plank, and its ceiling in this matchup is ~438 damage for
  ~438 Ti out of a median 670 collected.** ⚠ **ADMISSION GATE OWED:** GREP the
  incumbent first — the s55 builder must state what Mjolnir's builder-attack
  target order currently is and why the core is not in it; a reason may exist
  (attacking a 500-HP core is a poor Ti rate against most opponents), in which
  case the plank is *conditional* peck (peck when adjacent to a core and no
  cheaper target is in reach), not unconditional.
* **(b) BUY SENTINEL-ROUNDS ON TARGET, NOT LAUNCHER THROWS.** §4.2's monotone
  table is the bar: 0 → 3.7 %, 51–200 → **86.5 %** of their cores dead. We buy a
  median of **9**; the field buys **76**. Every launcher in `06a47ce9_game_4`
  (8 built, 7 destroyed within 2 rounds each) is a builder-turn and a +10 % scale
  tick that did not buy a sentinel. **The two anchored shapes that beat them
  (§4.4) both spend that budget on turrets planted between r8 and r49.**

**S4. WHAT SKALMAN MUST NOT INHERIT FROM THE RUSH LINE.** 795 throws, 673
kidnaps, **0 core damage**, 57 border throws, **0 crash-signature deaths**
(§4.5). Against gsxWins the launcher verb pays nothing and costs scale. **If
Skalman keeps a launcher verb, this matchup joins kladde as the second case that
says gate it off.**

**S5. THE MEASUREMENT SKALMAN OWES ITSELF.** Game share is too coarse to move at
n≤30 against them. **Carry two bars into any leg: `SENTINEL-ROUNDS ON TARGET`
(§4.2 — median 9 for us, 76 for the field, and it predicts their core dying) and
`CORE-DIRECTED BUILDER ATTACKS` (§4.3 — 0 for us, 1,999 for them).** Both have
already excluded zero once, both are counted from the replay without any
platform call, and both are properties of OUR code, so a leg can move them
deterministically.

**S6. AND THE TARGET-VALUE LINE, SO IT IS WRITTEN BEFORE THE WORK:**
`TARGET BAND: gsxWins v88, gap +30.09 (1854.04 vs 1823.96 at 09:41:10Z), win
pays +17.38, reachable YES.` Two of our three losing conditions above are our own
code, not theirs.

---

## 7. WHAT THIS STUDY DID NOT ANSWER

* **Why Mjolnir's builder never targets an adjacent core.** The discriminator is
  our own code, not their replays. §4.3 establishes the fact and the legality;
  the reason is a GREP away and was out of scope for a replay study.
* **Whether the d² 14–32 "outside the gunner screen" band is a real refuge.** The
  anchors say yes (`3c91a2b2_game_4`: 1,674 damage from d²=32, unanswered for 243
  rounds); the pooled rate says early sentinels in that band are still answered
  28/33. **Unresolved, and flagged rather than smoothed over.**
* **Their behaviour against 0033 / Bean counters.** 0033 appears at n=15 games
  with gsxWins at 0.867 — no denominator worth a claim.
* **Pool B is selected on their losses.** It answers "where does it crack" and
  may not be used for any rate meant to describe their ladder.
* **The 3 autopsy mismatches (§1.2)** are consistent with kill-round overkill but
  were not individually opened.

---

## Ledger row (for `docs/research/move-mining-ledger.tsv`, research to admit)

```
2026-08-22	gsxWins	88	100	docs/research/REPLAY-STUDY-gsxwins-v88-2026-08-22.md
```
