# REPLAY STUDY — `kladde chatte tville (och oss)` **v173**, 2026-08-22

**Provenance.** Fresh replay-study subagent, no inherited session context beyond
the named inputs. Commissioned by RESEARCH s54 at ~07:1xZ on a `move_miner`
FIRING (`scratchpad/s54_kladde_commission.md`, opened).
**Method:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` (the DISCIPLINE
block: MEASURED/EYEBALL labels, a control that must run the other way per
mechanism, retained refutations, the IN-LEG MIRROR CONTROL, ≥2 anchors per
piece). Duplicate-content check per
`docs/research/CUT-116-beltgun-answer-2026-08-21.md` §1.7 (opened).
**Inputs:** `corpus/meta_join.tsv`, `corpus/ladder_games.tsv`,
`corpus/league_matches.tsv`, `corpus/throws.tsv`, `docs/research/corpus-howto.md`,
`tools/replay_schema.md`, `tools/replay_census.py` (primitives),
`tools/corpus/replay_autopsy.py` (attribution rule), and 160 `.replay26` files.
**Priors read and cited as HISTORY, never as current doctrine:**
`docs/research/REPLAY-STUDY-kladde-v119-2026-08-17.md`,
`docs/research/REPLAY-STUDY-kladde-multiver-2026-08-20.md` (their v125–v141),
`docs/research/move-mining-ledger.tsv` rows 5, 18–22.
**Decoders:** `scratchpad/s54_klad_lib.py` (event walker over the census
primitives — rotation-re-emit guard, never-popped registry, signed 64-bit HP
deltas), `scratchpad/s54_klad_autopsy.py` (self-checking core-damage ledger),
`scratchpad/s54_klad_pool.py` (frozen pool).
**Platform writes: none.** Reads: `fcode match replay` × 11 (archive-first,
paced 2 s), no matches fired, no submission, no activation.
**Clock:** all times UTC from `date` in-shell. Pool **FROZEN 2026-08-22
07:16:25Z** (the corpus keeper is live and was appending under the analysis;
every number below is computed on the frozen list). Repo HEAD at write time
`aaf629c0d`.

---

## 0. THE POOL, AND WHAT IT IS NOT

| | games | matches | surface |
|---|---|---|---|
| **POOL A** — archived kladde-v173 games at the freeze | 105 | 21 | 60 unrated (5 of them our own challenges) + 45 rated |
| **POOL B** — 11 matches pulled by hand from opponents that BEAT v173 | 55 | 11 | rated ladder |
| **TOTAL** | **160** | **32** | **100 rated / 60 unrated** |

Opponents: OpenSverige 45, Erebus 25, Leviathan 15, The Flotte Experience 15,
Clankers 10, not adgato 10, ph 10, HTTP 418 10, O(1) 5, Jython 5, Lorem Ipsum 5,
sporks 5.

⚠ **THE POOL IS NOT A SAMPLE OF THEIR LADDER.** Kladde's game share **inside this
pool is 88/160 = 55%**; their **true v173 league-wide share is 279/256 = 52.1%
over 108 matches** (`corpus/league_matches.tsv`, all teams, 2026-08-21T11:32Z →
2026-08-22T07:01Z). Pool A over-weights us (45 of 105) where they are near
perfect; Pool B was **selected on their losses on purpose**, to answer Q2. Every
per-opponent cell below carries its own n; **no pooled win rate in this document
is an estimate of their ladder strength.** The league-wide row is.

**Kladde's side index is derived from `teamAName` in the platform metadata, never
from any winner-derived field** (`corpus-howto.md` TRAP 7). The exact string
`kladde chatte tville (och oss)` is used — and per the s52 study's TRAP C the
exact string `OpenSverige` is used for us (`opensverige - plan B` and
`OpenSverige - Plan C` are different teams and are excluded).

---

## 1. INSTRUMENTS — EVERY CONTROL RUN BEFORE ANYTHING WAS BELIEVED

### 1.1 KNOWN-CELL VALIDATION (commission bar: reproduce a recorded fact first)

Own decode path vs `corpus/ladder_games.tsv` on our three archived rated matches
against v173 — **turns, `win_condition` and the winning seat, per game**:

```
4bb7637f g1..g5   904/1000/127/293/216   core_destroyed ×4, titanium_collected ×1   won=0 ×5
31a830c5 g1..g5   283/153/286/446/561    core_destroyed ×5                          won=0 ×5
035db72a g1..g5   613/186/332/638/287    core_destroyed ×5                          won=0,1,0,0,0
                                            15 of 15 cells EXACT, 0 mismatches
```
The single **win** in the block (`035db72a` g2) flips the decoded seat correctly,
so the check discriminates in both directions rather than only confirming losses.

### 1.2 THE DAMAGE LEDGER SELF-CHECKS

`s54_klad_autopsy.py` requires attributed damage (FireTurret / BuilderAttack
resolved against **round-start** occupancy, per `tools/replay_schema.md`'s
FireTurret ordering trap) to equal the summed negative `UpdateHp` deltas on the
core id. **MEASURED: 144 of 144 core kills report exact match, 0 mismatches**
(79 kills by kladde + 65 kills of kladde).

### 1.3 IN-LEG MIRROR CONTROL (playbook, s53 addition)

Every geometry/latency instrument below was run **side-swapped on the same
files**. It is not decoration — §4's headline is precisely what the swap
returned. Two sanity properties held: conveyors sit near their builder's OWN
core on both sides (median d² 26 kladde / 29 opponent) while barriers sit near
the ENEMY core on both sides — i.e. the side assignment is behaviourally
consistent and is not a mirror of itself.

### 1.4 DUPLICATE-CONTENT SHARE (CUT-116 §1.7) — **0.0%, on a validated instrument**

Fingerprint = kladde's full gameplay event stream (builds, moves, builder
verbs, ammo converts, deaths) + map + game length, SHA-1.

```
FULL gameplay fingerprint (both sides, BotOutput excluded)  160 -> 160 distinct   0 dup (0.0%)
KLADDE-ONLY whole-game fingerprint                          160 -> 160 distinct   0 dup (0.0%)
```

**CONTROLS, because a zero that cannot be non-zero is not a measurement:**
* degenerate fingerprint (game length alone): 160 → 124 distinct, **36 duplicates
  (22.5%)** — the pipeline *can* emit duplicates;
* same file decoded twice → identical fingerprint (True);
* side-swapped fingerprint of the same file → different (True).

⭐ **BUT THE HONEST NUMBER IS NOT THE ONLY NUMBER, AND THE NEAR-DUPLICATE IS
REAL.** 24 `(map, opponent, opponent-version)` cells hold 2–4 games; all have
distinct fingerprints and distinct lengths (e.g. three games on one map vs our
v177 ran **301 / 297 / 299** rounds). **Diffing one such pair event-by-event
shows why: `4bb7637f_game_3` and `73e920b9_game_4` (same map, both vs our v177)
differ ONLY in our team's builder paths and in `BotOutput.execTimeUs`; kladde's
first 60 rounds are byte-identical, both plant the killing sentinel at (15,22) on
**r35**, both cores die on **r127**.** ⇒ **the non-determinism in this pool is
OURS, not theirs** (INFERENCE from one fully-diffed pair + the 22.5% length
control; MEASURED part = the diff). Treat any per-game bar computed on the
vs-us cells as carrying pseudo-replication that the 0.0% figure does not capture.

### 1.5 CORPUS TRAPS AVOIDED

`econ.tsv`'s `shots` and `deliveries` (TRAPS 5/8, both identically zero) are not
used; delivery is read from `Player.titaniumCollected` (schema field 4).
`meta_join` is used for FILE→match→team attribution only, never for a rated
win-rate denominator; the rated denominators come from `league_matches.tsv` and
`ladder_games.tsv`.

---

## 2. PREMISE AUDIT

### 2.1 Q3d(a) — *"is v173 continuous with their v147–v172 sprint?"* **VERIFIED — POOLABLE.**

13-dimensional their-side profile per game (count + first-build round for
conveyor / harvester / gunner / sentinel / barrier, builder spawns, barriers on
the enemy core's 8-tile spawn ring, forward sentinels), MAD-scaled L1 between
group medians (MAD floored at 1.0), permutation null of 3,000 re-splits at the
same group sizes. **Opponent held fixed at OpenSverige** so the comparison is not
a comparison of who they played.

| comparison | nA | nB | d | null med | null p95 | p | verdict |
|---|---|---|---|---|---|---|---|
| **v147+v168+v171 (sprint) vs v173** | 30 | 45 | **0.357** | 0.380 | 0.672 | **0.585** | **SAME** |
| v171 vs v173 | 20 | 45 | 0.344 | 0.367 | 0.710 | 0.565 | SAME |
| v119 vs v173 *(control)* | 170 | 45 | 1.339 | 0.232 | 0.376 | 0.0000 | DIFFERENT |
| v97 vs v173 *(control)* | 51 | 45 | 1.384 | 0.406 | 0.671 | 0.0000 | DIFFERENT |
| v97 vs v119 *(control)* | 51 | 170 | 0.526 | 0.237 | 0.380 | 0.0017 | DIFFERENT |
| v119 vs sprint *(control)* | 170 | 30 | 1.333 | 0.268 | 0.443 | 0.0000 | DIFFERENT |

**Four positive controls fire.** What moved at the v119 break, and has NOT moved
since (medians, vs-us games only):

| dim | v97 (51) | v119 (170) | sprint v147–171 (30) | **v173 (45)** |
|---|---|---|---|---|
| first sentinel round | 31 | 28.5 | **11** | **11** |
| barriers / game | 1 | 3 | **22.5** | **18** |
| first barrier round | 128 | 136.5 | **29.5** | **27** |
| barriers on OUR core's spawn ring | 0 | 0 | **7.5** | **7** |
| conveyors / game | 35 | 45.5 | 45.5 | 46 |
| builder spawns | 4 | 5 | 5 | 5 |

⇒ **The v173 doctrine is the v125–v141 rebuild, unchanged in kind.** The s52
study's numbers for that block (first sentinel r11, 14.8 barriers, 9.4 ring
barriers/game) reproduce here at r11 / 18 / 7. **Pooling v147→v173 for DOCTRINE
claims is legitimate; every headline number below is nevertheless v173-only, as
commissioned.**

### 2.2 Q3d(b) — *"repo claims about kladde describe OLDER versions"* — **VERIFIED, and the ledger says which.**

`move-mining-ledger.tsv` rows cover their **v119** (2026-08-17, 65 games) and
**v125/v126/v139/v140/v141** (2026-08-20). §2.1's controls put v119 on the far
side of a measured doctrine break from v173 (p=0.0000). `_v468kladturbo` and the
KLADDEDOSE prereg record predate that break. **Cite them as history. This
document is the only v173 read.**

### 2.3 THE COMMISSION'S "VERIFIED FACTS" — three corrections

**(i) "their current version IS v173, 18h stable."** MOSTLY RIGHT, with a fact
that matters for pinning. v173 is the holder from **2026-08-21T11:32:59Z** to the
freeze (19.5 h, 108 matches) — but the window is **not clean**: it contains
**8 interleaved matches on other versions** — v174 ×1 and v175 ×5 at
17:01–17:51Z on 08-21, v176 ×1 at 05:21Z and v177 ×2 at 06:11–06:21Z on 08-22 —
each returning to v173 immediately after. **That is a submit→fire→rollback
signature, i.e. they run prototype legs on the live slot exactly as we do.**
⇒ **Any future leg against them MUST pin (`fcode match unrated <team> --match
<past_match_id>`), and any analysis cell must filter on their per-match version
rather than on a time window.**

**(ii) "seven 0-5/1-4 sweeps across FOUR of our lineages in ~24h."** UNDERCOUNTED
and mis-attributed. In the 24 h to the freeze there are **13 matches against
them, and all 13 are 0-5 or 1-4**: 5 rated + 8 unrated, **4 games won of 65,
game share 0.062**. Our lineages were **v174, v175, v176, v177** (four — but the
commission listed `v173` as one of ours; v173 is THEIRS, and v175 was omitted).
**Their versions across those 13 were v171 (4 matches) and v173 (9)**, so only
the v176/v177 matches met v173.

**(iii) "the mid-tape v179 also lost but n=1."** **NOT FOUND.** Our v179 held the
slot 05:01–06:01Z on 08-22 and was paired with lingling_40h, 0033, Erebus,
gsxWins, The Flotte Experience, TRRR, Besvikomat — **no kladde pairing exists in
that hour** in `league_matches.tsv` or `meta_join.tsv` at the freeze. Not
refuted (an un-ingested row could exist); **not evidenced.**

**(iv) The framing itself needs one correction, and it is the most important
sentence in this study.** kladde v173 is **not** a bot that beats everyone:

| population | kladde game share |
|---|---|
| **v173, league-wide, 108 matches** | **279–256 = 0.521** |
| **v147–v173 block, league-wide, 130 matches** | **377–328 = 0.535** |
| **v147–v173 vs OpenSverige, 7 matches** | **33–2 = 0.943** |

Their next-best matchup in that block is Besvikomat at 0.800 (n=5 games, 1
match), then Focalground 0.760 (n=50) and team lazy 0.750 (n=20); at the other
end **nine teams hold them under 0.44** (HTTP 418 .200, ph .267, farming_200s
.350, Leviathan .356, Flotte .386, not adgato .400, Pivot .400, Erebus .429,
sporks .433). ⇒ **This is not a strong opponent. It is OUR worst matchup on the
ladder — 14.3 share-points clear of their next-best team, and 18.3 clear of the
next-best with a real denominator.**

---

## 3. Q1 — HOW THEY ZERO US

### 3.1 One channel, and it is the sentinel. **MEASURED.**

Damage into the losing core, from the self-checking ledger, whole pool:

| | sentinel | gunner | builder attack |
|---|---|---|---|
| **dealt BY kladde** (79 kills) | **59,058 (98.3%)** | 1,001 (1.7%) | 8 (0.0%) |
| dealt TO kladde (65 kills) | 39,780 (80.1%) | 9,702 (19.5%) | 210 (0.4%) |
| **dealt by kladde to OUR core** (39 kills, vs-us only) | **29,610 (99.0%)** | 294 (1.0%) | 8 (0.0%) |

**There is no second channel.** Nothing they do with builders, launchers or
economy puts meaningful damage on a core. Sentinel: r²=32, dmg 18, reload 2,
**and its line ignores obstacles** (CLAUDE.md entity table) — 9 HP/round from
outside gunner range, through anything.

### 3.2 The mechanism: **ONE FORWARD SENTINEL, PLANTED AND NEVER ANSWERED.**

**MEASURED, whole pool:** their first sentinel goes up at **median r28, d²=25
from their OWN core** (vs us: **r11, d²=17**) — that is the home counter-battery,
not the kill. The kill is the **first sentinel sited within d²≤50 of the ENEMY
core: median r112 (p10 = r39), present in 125 of 160 games.**

**Kill-arc anchors — three sweeps, three of our lineages, opened:**

| file / game | our ver | surface | map | mechanism, round by round |
|---|---|---|---|---|
| `4bb7637f-…_game_3` | v177 | rated | 30×30, cores (14,2)/(14,26) | conveyor r1 · harvester r21 · home gunner r12 · **sentinel #1 r26 at (16,13)** (d²=173, dies r81) · **sentinel #2 r35 at (15,22), d²=17 from our core** · first core hit **r36** · 46 shots × 18 = **828 dmg into a 500-HP core** · dead **r127**. **We built 0 turrets. That sentinel was never fired on and never died.** |
| `31a830c5-…_game_2` | v176 | rated | 20×20, cores (9,17)/(9,1) | sentinels r26 (11,9) and r30 (8,9) creep forward · **r93 sentinel at (5,6), d²=41** · first core hit **r94** · 540 dmg · dead **r153** · **5 ring barriers on our core at r21/24/68/93/146** · our builds: 6 builders, 3 launchers, 13 conveyors, **0 turrets**. |
| `7c3e9ae0-…_game_1` | v177 | unrated | 20×20, cores (9,17)/(9,1) | sentinel r7 at (10,13) dies r83 (it did its home job) · **r84 sentinel at (10,6), d²=26** · first hit **r85** · r113 second at (9,7) · 756 dmg · dead **r158** · **8 of 12 barriers on our core ring, r19–r86** · our builds: 5 builders, **9 launchers**, 16 conveyors, **0 turrets**. |
| `035db72a-…_game_3` | v176 | rated | 16×16 | the slow version: home sentinels r6/r38/r48, then **r196 (11,6) d²=41 and r233 (9,5) d²=20** · first hit r197 · 666 dmg · dead **r332** · 19 of 32 barriers on our ring. Here we DID build 7 turrets — and **every forward one of ours died** (see §4). |

**Creep is measurable, not eyeballed. MEASURED, sentinel build distance to the
enemy core as a fraction of the core-to-core d², by build round:**

| build band | n | median d² to enemy core | median as fraction of core-to-core d² |
|---|---|---|---|
| r0–50 | 208 | 173 | 0.677 |
| r50–100 | 133 | 101 | 0.374 |
| r100–150 | 108 | 120 | 0.345 |
| r150–200 | 87 | 85 | 0.321 |
| r200–300 | 136 | **43** | **0.163** |
| r300+ | 293 | 61 | 0.184 |

⇒ **a monotone walk from their half of the map to our doorstep.** The sentinel
that lands inside d²≈32 of a core is the one that ends the game.

### 3.3 The barrier ring on the ENEMY core — **MEASURED, and its purpose is NOT what it looks like**

Offsets of kladde barriers from the enemy core's NW corner (footprint =
(0,0),(1,0),(0,1),(1,1)), whole pool, 2,058 barriers inside a ±4 box:

```
        dx=-1    dx=0    dx=1    dx=2
dy=-1     41     110     110      41
dy= 0    190       -       -     136
dy= 1    160       -       -     137
dy= 2     37     185     163      22
```

**MEASURED: 3,343 kladde barriers over 160 games (20.9/game); 46.5% of them are
built within d²≤8 of the ENEMY core; median round of the first ring barrier =
r39; ≥1 ring tile taken in 147 of 160 games.** The pattern is exactly the 8
orthogonal spawn/adjacency tiles plus the 4 diagonals.

**Association with the outcome (MEASURED, INFERENCE on the direction):**

| ring tiles kladde took | n | kladde win % | median ENEMY `titanium_collected` | median enemy conveyors placed on those tiles |
|---|---|---|---|---|
| 0 | 13 | **0%** | 4,020 | 8.0 |
| 1 | 10 | 30% | 1,125 | 5.5 |
| 2 | 8 | 12% | 1,105 | 5.0 |
| 3 | 12 | 42% | 1,720 | 7.0 |
| **4+** | **117** | **68%** | **890** | 4.0 |

**⛔ TWO MECHANISMS FOR THIS RING ARE REFUTED HERE AND ARE RETAINED SO NOBODY
RE-DERIVES THEM:**

1. **It is NOT a spawn lock.** A full ring (all passable spawn tiles held
   simultaneously) occurs in only **7 of 88 kladde wins (8%) and 9 of 72 losses
   (12%)** — **more common in their losses**. And enemy builder spawns per 100
   rounds barely move with ring occupancy: **2.53 (0 tiles) → 1.91 (4+)**. The
   barrier-form spawn lock stays closed.
2. **It is NOT an anti-heal collar.** Enemy heal actions targeting their own core
   footprint, by ring occupancy: **6 / 14 / 20 / 62 / 23** — non-monotone, no
   signal.

**What survives is the delivery aperture (INFERENCE, from the table above):** the
ring tiles are where the last conveyor into a core must sit, enemy conveyors
placed there fall 8 → 4, and enemy `titanium_collected` falls 4,020 → 890. Under
`R1000_IS_DEFEAT` that is worth little to us directly — but it is how they take
the 10% of games that reach r1000 (16 of 160, 4 of them against us) **without
ever damaging a core**: `99bb733a_game_2` is the clean anchor — 6 of 8 ring tiles
taken r36–r114, **zero damage to our core in 1,000 rounds**, kladde wins on
`titanium_collected`.

---

## 4. Q2 — WHERE THE DOCTRINE CRACKS

### 4.1 ⭐⭐ THE MIRROR CONTROL IS THE ANSWER: **THEY ANSWER A FORWARD TURRET IN 1 ROUND. WE ANSWER IN 14, AND USUALLY NOT AT ALL.**

Definition: a *forward turret* is a gunner or sentinel built within d²≤50 of the
opposing core. *Answered* = the defending side lands ≥1 damage event on it.
Both directions computed by the **same function on the same files**.

| direction | n forward turrets | answered | median latency | killed | median life |
|---|---|---|---|---|---|
| **kladde's forward turrets → answered by US** | **164** | **26%** | **14 rounds** | **27%** | **38 rounds** |
| **our forward turrets → answered by KLADDE** | **81** | **96%** | **1 round** | **94%** | **6 rounds** |
| kladde's forward turrets → answered by the field (all 12 opps) | 437 | 40% | 8 | 41% | 33 |
| all opponents' forward turrets → answered by kladde | 898 | 60% | 3 | **78%** | 8 |

**Answer-rate difference against us: 70pp, two-fixture 95% half-width 15.7pp
(DEFF 1.434 unrated-mixed / 1.366 rated) → EXCLUDES ZERO.**
*(Cluster enumeration in writing: MATCH cluster LIVE — 5 games per match;
OPPONENT cluster DEAD — the comparison is within one opponent pair; surviving
DEFF = within-opponent.)*

**How they answer that fast. MEASURED:** across 543 answered forward turrets, the
**median age of kladde's responder at the moment it fires is 2 rounds**, and 39%
of responders are older than 10 rounds. Responder type: sentinel 235, gunner 226,
builder attack 82. ⇒ **They build a counter-battery ON TOP of your new turret
within ~2 rounds** — it is not a standing garrison, it is a reflex. (INFERENCE on
"reflex"; MEASURED part is the responder-age distribution.)

### 4.2 The crack, per opponent — **kill their forward sentinel, or die**

| opponent | games | kladde win% | kladde sentinels built | **killed** | median forward-sentinel life |
|---|---|---|---|---|---|
| ph | 10 | **10%** | 87 | **85%** | 13 |
| The Flotte Experience | 15 | **13%** | 59 | **83%** | 30 |
| sporks | 5 | **0%** | 26 | 69% | 56 |
| HTTP 418 | 10 | **20%** | 61 | 69% | 11 |
| Jython | 5 | 40% | 22 | 86% | 78 |
| O(1) | 5 | 60% | 39 | 64% | 58 |
| Erebus | 25 | 72% | 153 | 56% | 16 |
| Clankers | 10 | 70% | 103 | 58% | 41 |
| Leviathan | 15 | 33% | 62 | 40% | 32 |
| **OpenSverige** | **45** | **96%** | **294** | **46%** | **38** |
| not adgato | 10 | 20% | 25 | 20% | — |

Kill rate alone is not monotone (Jython 86%/40%, O(1) 64%/60%) — **the sharper
variable is whether you ever reach their core at all.**

### 4.3 ⭐ THE HEADLINE INDICTMENT: **WE DO NOT ARRIVE.**

*"Did we ever put one point of damage on kladde's core?"* — MEASURED, whole pool:

| opponent | games | reached their core | median round of first damage | median total damage into their core |
|---|---|---|---|---|
| Lorem Ipsum | 5 | **100%** | r41 | 1,053 |
| not adgato | 10 | **100%** | **r39** | 558 |
| The Flotte Experience | 15 | 93% | r124 | 675 |
| ph | 10 | 90% | r243 | 652 |
| HTTP 418 | 10 | 90% | r57 | 647 |
| Erebus | 25 | 84% | **r31** | 434 |
| sporks / O(1) / Jython | 5 each | 80% | r91–154 | ~500–594 |
| Leviathan | 15 | 53% | r229 | 18 |
| **OpenSverige** | **45** | **31%** | r134 | **0** |
| Clankers | 10 | 30% | r417 | 0 |
| **ALL** | 160 | **66%** | — | — |

**Us 14/45 = 31.1% vs the six Pool-B opponents (not adgato, Flotte, ph, HTTP 418,
sporks, Leviathan — all of whom hold kladde under 0.44 league-wide) → 54/65 =
83.1%. Difference 52.0pp against a two-fixture 95% half-width of 21.9pp →
EXCLUDES ZERO.** The s52 study measured this at **57.8%** for their v125–v141 block. **It
has fallen to 31%.**

⇒ **This is not a defence failure. It is the same offence failure the s52 study
banked, one era later and worse.**

### 4.4 The two shapes that actually beat them, with anchors

**SHAPE 1 — the r30 four-sentinel core rush (`not adgato` v25; kladde 8–12 in the
block, and 2–8 in the pool).** MEASURED across three opened games:

| file | map | adgato builds | the arc |
|---|---|---|---|
| `377d2b7f-…_game_4` | 20×20, d²=452 apart | **1 builder bot, 4 sentinels, nothing else** | sentinels **r30 (0,3) d²=8 · r32 (0,2) d²=5 · r34 (1,0) d²=2 · r35 (0,1) d²=4** — all on kladde's doorstep · first hit r31 · 558 dmg · kladde core dead **r49** |
| `5829e6b5-…_game_2` | 18×18 | 1 builder, 4 sentinels r29–r33 | dead **r49** |
| `377d2b7f-…_game_5` | 20×20 | 1 builder, 4 sentinels r30–r34 | dead **r50** |

Kladde's kill rounds against not adgato: **49, 49, 50, 54, 62, 69, 78, 81** —
median **r58**. Kladde's answer machinery *fires* (56% answered, latency r4) and
**still only kills 20% of them** — four sentinels at 4×18/2 = **36 HP/round**
delete a 500-HP core in ~15 rounds, faster than a 2-round reflex can reply.
**Their reflex is a per-turret reflex; it does not scale to a simultaneous
battery.** (INFERENCE; MEASURED inputs: 36 HP/round arithmetic from the entity
table, the 20% kill rate, the r49 kill rounds.)

**SHAPE 2 — gunner counter-battery at their core (`The Flotte Experience` v55,
`ph`, `HTTP 418`).** MEASURED: Flotte plants **5–7 gunners from r22**, 9 of 9 of
them within d²≤50 of kladde's core in `7e0a295c_game_2` (first at **r22, (13,12),
d²=17**); kladde's only sentinel there (r28) **dies at r49**; kladde core dead
r160. ph runs the same with 4 gunners from **r9–r18** plus a heavy belt, and
kills 85% of kladde's sentinels. **Median opponent gunners per game: Flotte 6,
ph 6.5, Lorem Ipsum 8, Erebus 6 — against OUR median of 1.**

### 4.5 ⛔ WHAT DOES NOT WORK, MEASURED ON LIVE GAMES (road closures, point 6 satisfied)

* **THE LAUNCHER LINE IS INERT AGAINST THEM.** In our 45 v173 games
  (`corpus/throws.tsv`, whose decoder is the corpus's own): **531 throws, of which
  251 are kidnaps of kladde builders, 84 "reached", and the total core damage
  attributable to all of them is ZERO** (`core_atk` sums to 0 over 531 rows).
  Median 7 launchers/game against 1 turret.
* **CRASH-INDUCTION DOES NOT WORK ON THEM.** Of the 251 kidnaps, **106 were thrown
  to a border tile and only 8 victims died** (163 RETHROWN, 80 alive at end).
  Their code survives an off-map neighbourhood. ⇒ **Kladde is guarded; spend the
  border-throw budget elsewhere.**
* **THEY CANNOT BE KIDNAPPED BACK, EITHER — AND THEY NEVER TRY.** **MEASURED:
  0 launchers and 0 splitters in 160 of 160 games** (builds: 8,388 conveyors,
  3,343 barriers, 965 sentinels, 830 harvesters, 759 builder bots, 417 gunners,
  **0 launchers, 0 splitters**). Their kidnap risk to us is exactly zero.
* **THE BARRIER-FORM SPAWN LOCK and the ANTI-HEAL COLLAR** — refuted in §3.3,
  retained.

---

## 5. Q3 — PLAY-THE-PLAYERS TABLE (kladde v173, 160 games, freeze 07:16:25Z)

| quantity | value | denominator / caveat |
|---|---|---|
| **League-wide game share, v173** | **0.521 (279–256)** | 108 matches, all opponents, `league_matches.tsv` |
| **Game share vs OpenSverige, v147–v173** | **0.943 (33–2)** | 7 matches; **their best matchup on the ladder** |
| Wins that are core kills | **90%** (79/88) | pool |
| **Median kill round** | **r301** | 79 kills; ≤r300 = 48%, ≤r200 = 23% |
| **Timely-kill rate (core kill by r300 / ALL games)** | **23.8%** | 38/160 — the PROGRAMME primary, computed for them |
| — same, vs us | **49%** (22/45), median kill r297 | they kill us twice as reliably as they kill the field |
| **r1000 share** | **10.0%** (16/160) | 4 of them vs us |
| First conveyor | **r1** | 160/160 |
| First harvester | **r9** (r7 vs us) | 158/160 |
| **First sentinel (home guard)** | **r28, d²=25 from their own core** (vs us **r11, d²=17**) | 159/160 |
| **First FORWARD sentinel (d²≤50 of enemy core)** | **r112 (p10 = r39)** | 125/160 |
| First barrier | **r26**; first ring barrier **r39** | 147/160 games take ≥1 ring tile |
| Builds / game | conveyor **52.4** · barrier **20.9** · sentinel **6.0** · harvester **5.2** · builder bot **4.7** · gunner **2.6** · **launcher 0** · **splitter 0** | 160 games |
| — vs us | conveyor 50.2 · barrier 25.2 · sentinel 6.5 · harvester 5.6 · builder 4.9 · gunner 3.0 | 45 games |
| **Reaction latency to a forward turret at their core** | **median 1 round vs us / 3 rounds league-wide; 94% / 78% killed** | 81 / 898 turrets |
| Their exposure to the same stimulus | answered **26%** by us, median **14 rounds**, **27%** killed | 164 turrets |
| Responder age when it fires | **median 2 rounds old** | 543 answered turrets |
| **Deterministic-opening share** | r0–10 identical in **46.2%** of pairs; r0–30 **11.2%**; r0–100 **1.2%** | fingerprint §1.4 |
| Same map, DIFFERENT opponent: first divergence | **median r8** | 378 pairs — **their opening is reactive, not scripted** |
| Same map, SAME opponent+version: first divergence | **median r27** | 24 pairs; the residual is OUR jitter (§1.4) |
| **Version churn** | 8 prototype matches inside the 19.5 h v173 window (v174/v175/v176/v177), each rolled back | **PIN THEIR VERSION** |

---

## 6. Q4 — THE SKALMAN READ

Stated as *supported-by-data*, not as prescription. The incumbent context read
before writing this section: `HANDOVER.md` s53 block — v176 "Mjolnir rotfix w77"
holds, v177 = `bots/_v542wave` (the rush line's peak, frozen benchmark), and
**Skalman is the new line: Bean-counters replication = cage + eco-denial.**

**S1. THE CAGE/ECO-DENIAL HALF OF SKALMAN IS NOT WHAT LOSES TO THEM — BUT IT IS
NOT WHAT BEATS THEM EITHER.** Kladde v173 **already runs a cage** (20.9 barriers
a game, 46.5% of them on the enemy core's ring, from r39) and **already runs
eco-denial** (enemy `titanium_collected` 4,020 → 890 as the ring fills), and
their ring does **not** function as a spawn lock or an anti-heal collar (§3.3,
both refuted). A Skalman that brings the same two verbs to this matchup is
bringing their own game, into a `titanium_collected` tiebreak that
`R1000_IS_DEFEAT` says we do not want, against a bot that reaches r1000 in 10%
of its games and wins those without touching a core.

**S2. THE ONE VERB OF THEIRS THAT BEATS A CAGE IS THE OBSTACLE-IMMUNE SENTINEL,
AND A CAGE HAS NO ANSWER TO IT BY CONSTRUCTION.** A barrier collar stops bodies
and blocks gunner lines; **a sentinel line ignores obstacles** (CLAUDE.md entity
table) and fires from d²≤32. 98.3% of their core damage arrives through exactly
that immunity. ⇒ **Any Skalman phase-1 fidelity target that is denominated in
barriers, collars or belt connectivity is orthogonal to this matchup.** Barriers
do not stop the thing that kills us. (INFERENCE on "by construction"; the 98.3%
and the r²=32 are MEASURED / rules-level.)

**S3. WHAT THE DATA SUPPORTS AS THE COUNTER-SHAPE — TWO OPTIONS, BOTH ON-PROGRAMME.**

* **(a) ANSWER THE FORWARD SENTINEL.** The single variable that separates the
  six Pool-B teams from us is a 70pp gap in forward-turret answer
  rate (§4.1, excludes zero). The cheapest instrument is a **standing gunner
  counter-battery near our own core**: Flotte/ph/Lorem Ipsum field 6–8 gunners a
  game; we field 1. A gunner is 20 Ti base and 4 ammo a shot, and 7 dmg × 2 hits
  kills a 25-HP gunner / 3 kills a 40-HP sentinel. **Non-regression check owed
  before this is admitted:** `home-turrets-off` measured **433/1024** at s30, i.e.
  home turrets already pay; this would be an increase in dose, not a new plank.
* **(b) OUTRUN THE REFLEX WITH A SIMULTANEOUS BATTERY.** `not adgato` v25 spends
  its whole opening on **one builder bot and four sentinels planted at d²≤8 of
  kladde's core between r29 and r35**, and kills them at **r49–r81, median r58**,
  in the teeth of a working 2-round reflex, because **36 HP/round beats a
  per-turret answer**. This is the most on-programme result in the study: a
  sub-r100 core kill, three anchored games, and it is *not* the two-raider rush
  we just retired — it is a **turret** rush that builds no economy at all.

**S4. WHAT SKALMAN MUST NOT INHERIT FROM THE RUSH LINE.** The launcher is inert
here: **531 throws, 251 kidnaps, 0 core damage, 106 border throws and 8 kills**
(§4.5). Every one of those throws is a builder-turn and a +10% scale tick that
did not buy a turret. **If Skalman keeps a launcher verb, this matchup is the
case that says gate it off.**

**S5. THE MEASUREMENT SKALMAN OWES ITSELF.** Everything above says our loss is an
**offence** failure — 31% reach, median 0 damage into their core, median first
damage r134 when the teams that beat them arrive at r31–r57. **The bar to carry
into any Skalman leg against kladde is `REACH` (share of games with ≥1 point of
damage on their core) and `FIRST-DAMAGE ROUND`, not game share** — game share is
too coarse to move at n≤45 and both of these have already excluded zero once.

---

## 7. WHAT THIS STUDY DID NOT ANSWER

* **Why we answer only 26% of their forward turrets** — vision, target selection
  or ammo starvation are all consistent with the trace; the discriminator is our
  own code, not their replays.
* **Whether the barrier ring is deliberately an aperture block** — the
  `titanium_collected` association is confounded with game length and outcome and
  is labelled INFERENCE throughout.
* **Their behaviour against Bean counters / 0033 / Ouroboros** — no matches exist
  in the block; the rating bands do not overlap.
* **Pool B is selected on their losses.** It answers "where does it crack", and
  it may not be used for any rate that is meant to describe their ladder.

---

## Ledger row (for `docs/research/move-mining-ledger.tsv`, research to admit)

```
2026-08-22	kladde chatte tville (och oss)	173	160	docs/research/REPLAY-STUDY-kladde-v173-2026-08-22.md
```
