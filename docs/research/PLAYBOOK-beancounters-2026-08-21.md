# PLAYBOOK — **Bean counters**: the definitive scouting book

**Rank 1. Team id `47803c19-e264-4492-bd62-fbdd58cfd7e6`.**
**The live opponent is `v68`.** It shipped **2026-08-21T07:12:59Z** and has taken
**every rated match since**: 29 decided matches, 29 wins, 84.8% of 145 rated
games, +141.3 rating (2153.1 → 2294.4) [STUDY §4.1]. **v47 is history** — its
last rated match was **04:12:59Z the same morning** [STUDY §2]. This book leads
with v68 and uses v47 as the deep background that explains where v68 came from.

**Commissioned by Magnus, principal, 2026-08-21** — *"every small tactics they
use and every grandiose scheme"*, amplified to *"The more detailed we can do it
the better."* This is the merge of the two era deep-watches into one book in one
voice. Merged **2026-08-21T16:1xZ** (`date -u`, in-shell); repo HEAD at merge
time **`a3b904127`** (2026-08-21T18:12:24+02:00).

---

## TABLE OF CONTENTS

| § | what is in it |
|---|---|
| **§0** | Provenance, sources, and the labelling discipline |
| **§1** | **WHO THEY ARE — the current v68 bot, in one page** |
| **§2** | The kill arc, phase by phase (v68 measured; v47 alongside) |
| **§3** | **The small-tactics catalog — 25 entries**, each with the sharpest number, round anchors + game id, the v47→v68 evolution, and a counter note |
| **§4** | The grandiose schemes — the tourniquet, the nest, the drip, the four-way division of labour, and the branches that do not exist |
| **§5** | Where it bends — ranked, with the caveat welded to each |
| **§6** | **What we copy for the SKALMAN line** — the spec, and the vulnerability ledger our own cage bot must not inherit |
| **§7** | Watch-along index — every cited game, replay path, and viewer line |
| **§8** | Caveats, merged and kept intact |
| **§9** | Conflicts between the two parts, and how each was resolved |
| **§10** | Probe index |

---

## §0 PROVENANCE

**Three source documents, all banked and committed, all cited rather than
re-derived:**

| tag | file | what it is |
|---|---|---|
| **[V68]** | `docs/research/PLAYBOOK-beancounters-PART-v68-2026-08-21.md` | 1,060 lines. The CURRENT doctrine, watched at decode level: 5 matches / 25 games narrated, cross-cuts over **112 archived v68 games** with a mirror control on every one |
| **[V47]** | `docs/research/PLAYBOOK-beancounters-PART-v47-2026-08-21.md` | 1,337 lines. The classic doctrine, watched: 5 games narrated, catalog measured over **1,235 archived v47 games** |
| **[STUDY]** | `docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md` | 942 lines. The statistical base (s53). **Cited, never re-derived here.** |

**Labelling discipline, carried through the merge unchanged.**
**MEASURED** = decoded off the replay bytes by a named probe with a named
denominator. **EYEBALL** = read off a rendered board or a tape by a human, no
control. **INFERENCE** = a causal reading. **A merge does not upgrade a label.**
Where a part carried something as EYEBALL it is still EYEBALL here, and it says
so on the line — the whole point of merging in one voice is that the reader
cannot tell from the prose which part a sentence came from, so the label has to
carry the weight instead.

**Every number keeps its subject.** Denominator, population, era and fixture
travel with the figure, inline, per the house rule. Two populations recur and
they are not interchangeable:

* **the v68 cross-cut set** — **112 archived v68 games**, ~90% unrated
  challenges [V68 §12.1];
* **the v47 cross-cut set** — **1,235 archived v47 games**, 1,115 unrated / 120
  ladder, 2026-08-16T19:30Z .. 2026-08-21T04:21Z [V47 §11.2].

Unrated pools PROTOTYPES on the challenger side, so every "them vs the field"
share in this book **overstates them relative to their rated record** (v47:
69.4% archived game share against **51.2% rated**, n=1,570 [STUDY §8.1]). The
comparison to quote is always the **internal ratio** — them against the
opponents they actually faced in those same games, produced by one code path
with the team index swapped — never a cross-fixture difference against our own
numbers.

**No half-width in this book carries the cluster DEFF correction**, because
every cell here is a point estimate or a within-game count rather than an
interval. Any cell promoted to a bar must first be restated with CLAUDE.md's
DEFF (1.833 unrated / 1.529 rated). §8 names the two cells most at risk.

**Nothing was fired, submitted or committed to produce this merge.** No edits to
`QUEUE.md`, `bots/`, `tools/`, `corpus/`, or to either source part. One command
was executed: `tools/replay_view.py` on one archived replay, to confirm the
watch-along pattern in §7 actually runs (it printed
`scratchpad/replay_view/3bf73ae7-…_game_3.html` and opened no browser).



## §1 WHO THEY ARE — the current bot, in one page

**Bean counters v68 is a four-man siege crew that walks a gun to your front door
and then bricks up the door.** There is no rush, no swarm, no economy race in the
sense we usually mean it, and — this is the part that catches people — **almost
no reaction to you at all**. The plan is a function of the map, fixed before you
move, and it runs the same whether they are winning or losing.

**The crew is four builder bots, spawned on rounds 0, 1, 2 and 3, and there is
never a fifth.** MEASURED: exactly four in **104 of 112 archived v68 games**, and
the fourth lands on round 3 with **p10 = p90 = 3** [V68 §4]. They take four fixed
jobs and hold them for the whole game — a **home keeper** that lays the belt and
never leaves the home quadrant, a **cage walker** that marches to your core and
walks a lap around it dropping barriers, an **ore denier** that chews your
harvesters and then bricks the ore tile so you cannot rebuild them, and a **siege
engineer** that plants the sentinel. In one watched game all four were still
alive at the kill, having built 45 things between them and lost nothing
[V68 §3.2]. In the median **v47** game — same doctrine, older engine room — **one
single builder places every barrier on your core ring and another never comes
near you at all** (median top-share **1.000**, n=924 games) [V47 §7.1].

**The kill chain is economy → ammunition → turrets, and every link is deliberately
thin.** They lay a big tidy *terminated* belt at home (43 conveyors, 9 harvesters
a game; **83% of their surviving harvesters have a directed path into their own
core** against our 58.8% [STUDY §1]). They convert titanium to ammunition in
**67 separate small calls a game (median, p90 102)**, and **97.3% of 8,278
converts are an exact sum of 4s and 10s** — the precise cost of the shots they
are about to fire [V68 §2.2]. They never bank: **peak ammunition ever held,
median 26**, about two sentinel shots. Their end-of-game titanium averages
**137 Ti** [STUDY §5.5]. Every round they are funding the next round's shots and
nothing else.

**Then two verbs kill you.** *Verb one — the cage.* Your core is a 2×2 block with
exactly eight orthogonal neighbours, and those eight tiles are the only places a
conveyor can deliver into it and the only places it can spawn a builder. They put
barriers on those eight tiles. When the seal completes, the victim's harvester
connectivity falls **78.6% → 8.7%** and median collection falls 975 → 170
[STUDY §1]. *Verb two — the gun on the doorstep.* **First forward turret at
median round 34, first turret within d² ≤ 13 of your core at median round 41,
first ring tile taken at median round 52** [V68 §4]. On v68 the gun arrives
**before** the cage — the barriers go up on the tiles their own guns have just
cleared, one round after each conveyor dies [V68 §3.1].

**What v68 changed from v47, with the opponent held fixed** [STUDY §4.2]: they
**deleted the harvester raid** (builder attacks on enemy harvesters 128.5 → 19.9
a game), **quadrupled gunner rotations** (2.0 → 8.1), and **moved the gunners
from home to your core** (28.7% → **77.9%** built in the enemy's half; sentinels
at d² ≤ 13 of your core 23.9% → **53.3%**). Median kill moved **146 → 131**, kill
share **67.5% → 88.9%**, and **games reaching round 1000 went to 0.0%**. The
economy and the ring are unchanged — that is the stable spine across v47, v64 and
v68. **The raid did not get faster; it was deleted, and the walk to your door
replaced it.**

**And they are terrifying at one defensive verb we are merely average at.** Bean
counters destroy **79.7% ± 2.2** of the forward turrets planted in their half
(n=1,131 games, 5,803 turrets) while the opponents they face manage 33.5% — a
**2.4× internal ratio**. We destroy **42.8% ± 3.3** and the opponents we face
manage 43.3% — **exactly average** [STUDY §6.2]. Their home turrets live a median
**72 rounds against the field's 13** [V47 §6.9].

**Where they are soft.** They build **zero launchers — 0 in 1,385 games** — and
have no counter-throw and no re-plan: one of our launchers put a v68 builder in a
five-round throw cycle and held it there for **37 rounds, 8 throws, same
destination tile every time**, 25% of their entire workforce removed for 20 Ti
[V68 §5.1]. **A sentinel cannot rotate** — an engine rule, confirmed at
**1,125 of 1,125 measured facing changes being gunners** — so a forward sentinel
is a fixed-axis gun, blind to anything off its line; Pantheon killed one in **9
rounds** by standing 2 tiles off its axis and the killer lived 49 [V68 §3.4].
**They get worse as the map gets bigger**: against Pantheon, **SMALL 13/13 =
100%, MID 11/15 = 73%, BIG 6/12 = 50%** [V68 §3.5]. And their whole kill chain
runs through one belt they will repair forever and never defend — v47 lost a
rated game 0-5 to **one 20 Ti gunner planted on their delivery face at round 60**
that fired 94 shots into two conveyor tiles while they rebuilt one of them
**sixteen times and fired zero shots back** [V47 §5.1].

**Our own record against them is 0 of 15 games** — their v47 twice and their v68
once, three different builds of ours [STUDY §2]. Wilson 95% upper bound on our
true share: **20.4%**. Thin, and unambiguous.



## §2 THE KILL ARC, PHASE BY PHASE

The arc is the same in both eras. What moved between them is *which phase carries
the kill*. Read the table as the live book and the v47 column as where it came
from.

### 2.1 The measured landmark clock — **MEASURED, 112 archived v68 games**

First-occurrence round of each landmark on Bean counters' side, median (p10 /
p90) [V68 §4]:

| phase | landmark | **median round** | p10 | p90 | coverage |
|---|---|---|---|---|---|
| **I. THE LEVY** | first builder bot | **0** | 0 | 0 | 112/112 |
| | **fourth builder bot** | **3** | **3** | **3** | 112/112 |
| **II. THE BELT** | first conveyor | 2 | 1 | 6 | 112/112 |
| | first harvester | **5** | 3 | 12 | 112/112 |
| **III. THE MARCH** | first barrier, anywhere | 33 | 14 | 56 | 112/112 |
| | **first FORWARD turret** (nearer your core than theirs) | **34** | 16 | 49 | 111/112 |
| | first gunner | 36 | 14 | 56 | 109/112 |
| | **first turret at d² ≤ 13 of your core** | **41** | 21 | 65 | 111/112 |
| | first sentinel | 46 | 15 | **115** | 108/112 |
| **IV. THE CAGE** | first tile taken on YOUR core ring | **52** | 31 | 80 | 108/112 |
| **V. THE KILL** | **your core dies** (games they win, n=98) | **131** | 98 | 234 | 87.5% of games |
| | game length, all games | 139 | 101 | 311 | 112 |

⭐ **The r131 median reproduces [STUDY §4.2]'s 131 exactly, on a different game
set (112 archived vs their frozen 90) with a different decoder.** A free
cross-check, and it passed.

### 2.2 The phases, narrated — and what each one was in the v47 era

**P0 — THE LEVY, r0–r3.** The core spawns four builders, one per round, and then
never spawns another. v47 averaged **4.38 builders a game** over 1,235 games
against their opponents' 5.81 [V47 §7.1]; v68 tightened it to **4.07**, exactly
four in 104 of 112 games [STUDY §4.2, V68 §4]. **Watch it in G-D**: bot4 `(15,10)`
r0, bot6 `(15,9)` r1, bot8 `(16,11)` r2, bot11 `(15,10)` r3 [V47 §2.2] — and note
the spawn tiles are their **own** ring, with the west pair facing the enemy.

**P1 — DEPART, r0 onward, concurrent with everything else.** The siege builder
walks the instant it exists and **builds nothing on the way**. In G-D its first
act of the game is a barrier on `(4,10)` — a ring tile of the *enemy* core, 11
tiles from where it was born — at **round 11**. Ten cardinal steps in r1..r10,
build on r11. **First cage round = walk distance + 1, to the round** [V47 §2.3].
This is the structural fact of the whole doctrine: **there is no stimulus to
bait.**

**P1′ — THE BELT, r2–r40, in parallel.** Conveyors are laid **outward-in**, every
one facing the next tile in a chain that terminates on their own core footprint;
nothing is ever built facing away [V47 §2.2]. First harvester at median r5 (p90
12) [V68 §4]. In v68's match A game 5 the whole economy is finished by r15 and
two of the four builders are already nine tiles from home [V68 §3.1].

**P2 — THE MARCH (v68) / THE CAGE OPENS (v47).** ⭐ **This is where the two eras
genuinely differ and it is the single most important structural change in the
book.**
* **v47** opened with the cage: median round of first ring build **35**
  [STUDY §6.2], mean 49.9 [V47 §6.3], and 99.4% of first cage tiles are a
  **barrier** (1,173/1,180 games with any ring build; 7 gunners).
* **v68** opens with the **gun**: first forward turret r34, first turret inside
  d² ≤ 13 of your core r41 — and the **first ring tile arrives at r52**, *after*
  both [V68 §4]. **The cage got later while the kill got faster.**

The mechanism, watched: in v68 the ring tiles are taken **as the forward guns
clear them**. A conveyor on a ring tile dies to gunner fire; a barrier goes onto
that tile the next round. Match A game 5 shows it **seven times in one game**
[V68 §3.1]. **The guns open the ring; the barriers keep it open.**

**P3 — THE RAID + ORE CAP.** In v47 this was a whole job: **128.5 builder attacks
on enemy harvesters per game**, ten-attack doses per target, and **80.3% of the
ore tiles it cleared were barriered within 3 rounds** against a **1.0% placebo**
on a different ore tile in the same window [V47 §6.1]. In **v68 the raid is cut
to 19.9 attacks a game** [STUDY §4.2] — **but the ore capping is not cut at all**
(§3, T10). The chewing that remains is aimed and cheap; the melee budget went
into the walk.

**P4 — EVICT.** Whatever of yours stands on your own eight ring tiles gets a
ten-attack dose (2 damage each into a 20 HP conveyor) and then a barrier
**1.08 rounds after the corpse**, 67.4% of 2,699 evictions capped within 3 rounds
[V47 §6.2]. Watched four-for-four at exactly +1 round on **our own** ring in G-C
(r99→r100, r111→r112, r123→r124, r134→r135) [V47 §4.3].

**P5 — THE NEST.** v47 planted sentinels in the **d² 14–32 band** — inside
sentinel reach (r²=32), outside every gunner's (r²=13) — median distance exactly
**25** [STUDY §3.5], and shelled them with its own barriers built 1–4 rounds
*before* the gun, legally, because a sentinel's line ignores obstacles
[V47 §2.5]. **v68 abandoned that caution: 53.3% of its sentinels are at d² ≤ 13
of your core, and "walks onto the core" is literal — `d² = 1` means the sentinel
is standing ON one of your eight ring tiles** [V68 §6]. It still knows the band
trick when it wants it: in match A game 5 the sentinel goes on `(17,15)`, where
`(17,15) → (21,11)` is **d² = 32 exactly** — maximum range, on the diagonal,
aimed at the core's NW corner — and opens fire on **round 33** [V68 §3.1].

**P6 — THE DRIP, from the round the first turret exists to the end.** `convert_ammo`
of exactly the next shots' cost, every round or two, forever, no bank. See §3 T20.

**P7 — THE GRIND, to the end.** **92.6% of 45,262 v47 sentinel shots land on an
enemy core footprint tile, and 46.5% of those are fired straight through one of
your own buildings** [V47 §6.4]. Meanwhile the home guns sweep anything you plant
in their half at 79.7% [STUDY §6.2].

⚠ **The phases run in PARALLEL, not in sequence.** That is the entire point of
the four-way specialisation: the belt, the walk, the raid and the nest all
progress on the same rounds because they are four different bots.

### 2.3 What the 15-round speedup actually bought (146 → 131)

**Phase III is where the whole difference lives** [V68 §4]. v47 sent its builders
into the enemy *economy*; v68 sends the same builders down a corridor and spends
the time putting a gun **on the core**. The budget moved from melee to walking,
and the ammunition bill rose to pay for it (530 → **650 Ti a game** converted
[STUDY §4.2]).



## §3 THE SMALL-TACTICS CATALOG

**Twenty-five entries. Each one gives: what it is · the sharpest measured number
with its denominator · the round anchors and the game to watch it in · how it
changed from v47 to v68 · and the COUNTER note — the habit or blindness a plank
could lean on.**

⚠ **Counter notes are notes for a prereg author, not admitted planks.** Nothing
in this section has been tested in a live game, and per CLAUDE.md point 6 none of
it opens or closes a road until it has been.

**Game tags** (full ids, paths and viewer lines in §7):

| tag | era | game | fixture |
|---|---|---|---|
| **A** | v68 | `0798229c…` Pantheon v105, 3-2 | RATED 11:32:59Z — their closest call |
| **B** | v68 | `05d99bef…` HTTP 418 v124, 5-0 | RATED 13:51:10Z |
| **C** | v68 | `32b80f90…` OpenSverige v175 (**us**), 0-5 | unrated 08:11:52Z |
| **D** | v68 | `07bdf19b…` Leviathan v91, 4-1 | RATED 14:01:10Z |
| **M1 / M2** | v68 | `74a8f527…` g5 (Leviathan, RATED) · `487a97fe…` g4 (kladde chatte tville, unrated) | the two meat-grinder games |
| **G-A / G-B** | v47 | `02c59670…` g1 / g3, Pivot v236, **0-5** | **RATED** 03:32:59Z — the collapse |
| **G-C** | v47 | `4c901c39…` g4, OpenSverige v162 (**us**) | unrated 2026-08-18 |
| **G-D** | v47 | `3bf73ae7…` g3, Part-timers, kill **r60** | unrated — their fastest of 1,235 games |
| **G-E** | v47 | `9ee3a878…` g3, 0033, 30×30, kill r102 | unrated |
| **TH** | v47 | `008b7e55…` g5, Torsko | unrated — the thrash oscillation |

---

### T1 — FOUR BUILDERS, ROUNDS 0–3, AND NEVER A FIFTH

**What.** The core spawns one builder per round for four rounds and then stops
for the rest of the game, whatever happens.
**Sharpest number.** **Exactly four in 104 of 112 archived v68 games** (7 spawn
five, 1 spawns six), and **the fourth lands on round 3 with p10 = p90 = 3**
[V68 §4]. Pooled means: v47 **4.38**/game (n=1,235) against their opponents'
**5.81**; v68 **4.07** [V47 §7.1, STUDY §4.2].
**Watch.** G-D r0–r3 (bot4/bot6/bot8/bot11). A r0–r3 (#3, #5, #9, #13) — and
Pantheon spawns five in the same game, adding **#39 at r12** [V68 §3.1].
**v47 → v68.** Unchanged; if anything tighter. **This is spine, not fashion.**
**COUNTER.** Their workforce is a **known, enumerable, four-element set whose
spawn rounds are 0, 1, 2, 3**. Every denial arithmetic against them divides by
four, not by an unknown. It also means **T23's displacement removes 25% of the
labour force per throw** and nothing regenerates.

### T2 — FOUR FIXED JOBS, HELD ALL GAME

**What.** The four bots take non-overlapping roles and do not swap while all four
are alive: **HOME KEEPER**, **CAGE WALKER**, **ORE DENIER / RAIDER**, **SIEGE
ENGINEER**.
**Sharpest number.** In the median v47 game (n=924 games with ≥4 ring barriers)
**one single builder places every barrier on your ring — median top-share
1.000** (field 0.857), spends **84.8%** of its actions within d² ≤ 9 of your core
(field 66.7%), while another builder's forward share is **0.000** [V47 §7.1].
**Watch.** A, game 5, all four id-tracked end to end, **zero deaths, zero
replacements, 1 ambiguous attribution of 45 builds** [V68 §3.2]:

| bot | spawn | what it is | its ledger |
|---|---|---|---|
| **#3** | (0,10) r0 | **HOME KEEPER** — never leaves the home quadrant | 7 conveyor, 1 harvester (0,8); rebuilds (3,12) three times (r30/r34/r106); batk 3, heal 4 |
| **#5** | (1,13) r1 | **CAGE WALKER** | home belt to r15, corridor march, forward gunner (20,13) r36, clockwise lap, 6 ring + 2 ore barriers; batk 19 |
| **#9** | (3,11) r2 | **ORE DENIER / raider** | 2 harvesters, 1 gunner (6,14), **6 barriers, all on ORE**; batk 30 — the melee bot |
| **#13** | (3,12) r3 | **SIEGE ENGINEER** | 5 conveyor, **the sentinel (17,15)**, 3 ring barriers; batk 0, heals its own barrier (20,11) five times r63–r67 |

**v47 → v68.** The role *names* shift with the doctrine: v47's four were siege
engineer / raider / **nest builder** / home economist-repairman [V47 §7.2]; v68's
are home keeper / **cage walker** / **ore denier** / siege engineer. **The
division of labour is identical; the middle two jobs were re-pointed from the
enemy economy to the enemy doorstep.**
**EYEBALL, retained as such:** in both v47 games the siege engineer is
identifiable **by its spawn tile** — the ring tile of their own core that faces
the enemy (G-D `(15,10)`, enemy due west; G-E `(4,14)`, enemy due east)
[V47 §7.2]. Two games. The population version (the 1.000 top-share) is MEASURED;
the spawn-tile rule is not.
**COUNTER.** The job is a better target than the body. **Killing a builder that
has already done ≥3 siege acts buys a median 11 rounds of cage progress and a
12.9% chance the cage stops permanently** (n=93 deaths over 1,235 v47 games; 81
of 81 successors are one of the three survivors walking over, only 3 of 81 a
fresh spawn) [V47 §7.3]. ⚠ It dies unprompted only **0.075 times a game** — this
is a window you must *make*.

### T3 — THE BELT: OUTWARD-IN, ALWAYS TERMINATED

**What.** Conveyors laid from the far end inward, every facing pointing at the
next tile of a chain that ends on their own core footprint.
**Sharpest number.** **83% of their harvesters alive at the end have a directed
path into their own core**; ours, on the last comparable cut, **58.8%**
[STUDY §1]. 43 conveyors and 9 harvesters a game (v47); 6.53 harvesters on v68.
**Watch.** G-D r2/r4/r5/r8 — facings `E,E,N,N`, **nothing ever built facing
away** [V47 §2.2]. `(14,9)` E is built at r2, *before* `(15,9)` E at r4, which is
the tile that actually touches the core.
**v47 → v68.** Unchanged spine. Harvester count drifts down slightly (8.86 →
6.53) as the melee budget moved [STUDY §4.2].
**COUNTER.** A terminated belt is a **single-failure-mode** belt. See T24 — cut
it once and the whole kill chain downstream (ammo, then turrets) starves, and
they have no branch that treats the cut as a *turret* problem.

### T4 — THE CAGE HAS NO TRIGGER: `walk distance + 1`

**What.** The first barrier on your core ring is scheduled at spawn. Nothing you
do moves it except distance and occupancy.
**Sharpest number.** G-D: bot4 spawns `(15,10)` r0, needs to stand on `(5,10)` to
build on `(4,10)`, ten cardinal steps r1..r10, **builds at r11 — the walk
distance, exactly** [V47 §2.3]. At population scale the same signature: median
first ring build **r11 / r20 / r34** for near (d²<150) / mid (150–350) / far
(d²≥350) core separation, at an **empty** victim ring (n=25/40/84) [V47 §6.3].
**v47 → v68.** The *mechanism* survives; the *schedule* moved. v47's median first
ring build was **r35** [STUDY §6.2]; v68's median first ENEMY ring tile is **r52**
[V68 §4]. ⚠ **Two probes, two denominators, direction-only** (§9 conflict 7).
**COUNTER.** **The tile is predictable from geometry alone before the game
starts**, and there is no reactive branch to stay under or bait. Combined with
[STUDY §5.1]'s 95.4% opening determinism (21 of 30 exact map×seat cells 100%
identical, v47), **their first ~11 rounds are a lookup, not a decision.** ⚠ The
v68 determinism cells are too small (4.6 games/cell) to confirm the table
survived the version bump — **re-derive before firing anything that depends on
it.**

### T5 — CAGE FACE SELECTION: NEAREST **EMPTY** TILE FIRST, NEVER THE FAR SIDE

**What.** They take whichever ring tile is unoccupied and closest, and come back
for the occupied ones later by eviction (T8).
**Sharpest number** (n=1,180 v47 games with any ring build) [V47 §6.3]:

| first cage tile, by face | Bean counters | field |
|---|---|---|
| the face pointing at them (APPROACH) | 542 (45.9%) | 421 (47.4%) |
| a side face (FLANK) | 607 (51.4%) | 373 (41.9%) |
| **the far face (OPPOSITE)** | **31 (2.6%)** | 95 (10.7%) |
| **first cage tile is a BARRIER** | **99.4%** (1,173/1,180) | — |

**Watch.** G-D: the victim's delivery conveyors stood on its **north** face from
r13; BC took the **east** face first (`(4,10)` r11, `(4,9)` r13) because those
were empty, and only came back for the belt-entry tiles third and fourth, by
eviction (r32, r44) [V47 §2.3]. G-C: their first cage tile on **us** was `(8,2)`,
the **west** face — not the south face they were approaching from [V47 §4.3].
**v47 → v68.** Same rule, executed with a lap instead of a shuttle (T6).
**COUNTER.** ⭐ **Occupying your own ring is the measured defensive lever, and it
is measured with the distance confound controlled** [V47 §6.3]: holding **5+ of
your own 8 ring tiles at r30** pushes their first cage build from r11→**r26**
(near), r20→**r43** (mid), r34→**r65** (far), and their **median melee attacks on
your ring tiles rise from 0 to 40–62**. ⚠ Observational, not experimental — a
team that collars its ring is a better team in other ways. **The melee column is
the part that is not confoundable.**

### T6 — THE CAGE BY CIRCUMNAVIGATION (v68's execution)

**What.** One bot walks a full lap around your core dropping a barrier on each
ring tile as it passes, while the second covers the two far faces from the inside
lane. Two bots, two lanes, opposite sides.
**Sharpest number / anchor.** A game 5, bot #5's path from r35:
`(20,14) → (21,14) → (22,14) → (23,14) → (23,13) → (23,12) → (23,11) → (23,10) →
(22,10) → (21,10)` — a clockwise lap — while #13 covers `(20,11)`/`(20,12)`
[V68 §3.1]. **Seven of eight ring tiles taken between r40 and r62.**
**v47 → v68.** v47's siege engineer shuttled to one face and evicted; v68 laps.
**INFERENCE** on why: v68's guns clear tiles faster than one bot can evict them,
so the bottleneck moved from *clearing* to *walking*.
**COUNTER.** A lap is a **predictable path**, one tile per round, on tiles
adjacent to your own core — i.e. inside your own vision and inside your own
builders' melee reach, for a dozen consecutive rounds. It is also the perfect
launcher pickup window (T23).

### T7 — THE CAGE IS BUILT AS THE GUNS CLEAR IT

**What.** In v68 a ring barrier goes up on the round *after* a conveyor on that
tile dies to their own gunner fire. The guns open the ring; the barriers keep it
open.
**Sharpest number / anchor.** A game 5, **seven ring tiles, every one built the
round after a death on it** [V68 §3.1]:

| round | event |
|---|---|
| r39 | Pantheon conveyor #15 on **(22,13)** dies to gunner #114 firing E |
| **r40** | BC barrier **(22,13)** by #5 from (22,14) — ring 1/8. #114 rotates E→N |
| r43 | Pantheon conveyor #104 on **(20,11)** dies (gunner #114 firing N) |
| **r44** | BC barrier **(20,11)** by #13 from (19,11) — ring 2/8. #114 rotates N→SE |
| r51 → **r52** | conveyor on (22,10) dies → BC barrier **(22,10)** — **killed by Pantheon r53** |
| **r53** | BC barrier **(21,10)** — ring 3/8 |
| **r55** | **(22,10)** again — killed r60 |
| **r57 / r59** | **(23,12)** ring 5/8 · **(23,11)** ring 6/8 |
| **r61** | **(20,12)** |
| **r62** | **(22,10)** a **third** time — ring 7/8, and it holds to the end |

Note `(21,13)` — **the 8th tile was never sealed and the game was over anyway.**
**v47 → v68.** In v47 the clearing verb was **builder melee** (T8, ten attacks per
tile); in v68 it is **gunner fire**, and the melee budget dropped 70.7 → 15.6
attacks on enemy conveyors per game [STUDY §4.2].
**COUNTER.** The ring tile they want next is **the one their gunner is currently
pointed at**. Their gunner's facing is readable from the engine (`get_direction`)
and their rotation is a re-aim, not a patrol (T17) — **so their next cage tile is
telegraphed one to three rounds ahead.**

### T8 — THE EVICTION METRONOME: TEN ATTACKS, THEN A BARRIER AT +1 ROUND

**What.** A builder attack does 2 damage for 2 Ti; a conveyor has 20 HP. They
apply exactly ten, on consecutive rounds, and barrier the corpse the next round.
**Sharpest number.** **67.4% of 2,699 evictions capped within 3 rounds, mean
latency 1.08 rounds** — field 38.6% at 1.50 (v47, n=1,235 games) [V47 §6.2].
**Watch — and it is four-for-four on OUR ring** [V47 §4.3]:

```
tile      melee window     dies   their barrier
(8,2)     r91 .. r98       r99    r100    <- +1
(10,0)    r102 .. r110     r111   r112    <- +1
(9,0)     r114 .. r122     r123   r124    <- +1
(8,1)     r125 .. r133     r134   r135    <- +1
```
G-D two-for-two (r31→r32, r43→r44); G-E two-for-two (r37→r38, r49→r50).
**v47 → v68.** The dose survives — A game 5 shows **15 consecutive attacks** on
each of three enemy *harvesters* (30 HP, so 15 doses) at r62–r76, r64–r78,
r97–r111 [V68 §3.1] — but the *volume* collapsed with the raid (T10).
**COUNTER.** ⭐ **This is a one-round window on a known tile, ~1,800 times across
1,235 games.** Anything of ours that re-occupies that tile inside one round
denies the seal permanently — **our 3 Ti barrier is exactly as good as theirs.**
The field currently converts **0.8%** of the equivalent openings (T22).

### T9 — THE OVERSHOOT ATTACK

**What.** The last `builderAttack` of a chew series lands on the round the target
has already died — an attack on an empty tile. The engine permits it and charges
2 Ti.
**Sharpest number / anchor.** **MEASURED three times in one game** (A game 5,
r76, r78, and the (12,6) series ending r112); the tape prints it as
`BATK t0 #N -> (x, y) none` [V68 §3.1].
**v47 → v68.** Observed in the v68 watch. Not separately measured on v47.
**COUNTER.** 2 Ti a time — a rounding error, and **worth naming only as a tell**:
it means their melee loop is a fixed dose counter, not an HP check. **INFERENCE:
a target whose HP they cannot read correctly (one being healed) will absorb the
full dose and survive** — which is exactly what T18 shows happening to their
turret fire.

### T10 — ORE-TILE DENIAL: KILL THE HARVESTER, TAKE THE TILE FOREVER

**What.** When an enemy harvester on tile T dies, they put a 3 Ti barrier on T. A
barrier on ore makes `can_build_harvester` false there forever, short of
destroying it. **A temporary kill becomes permanent denial.**
**Sharpest numbers — two eras, two windows, both MEASURED, and they must not be
mixed** (§9 conflict 1):

| | **v68** (112 archived games, 30-round window) | **v47** (1,235 archived games, 3-round window) |
|---|---|---|
| enemy harvester deaths counted | 200 | 2,862 (on ore) |
| **tile barriered by them** | **185 = 92.5%** | **2,298 = 80.3%** |
| median latency, death → barrier | **1 round** (p90 15, min 0) | mean **1.08 rounds** |
| the same measurement on their opponents | 11/49 = **22.4%** | 1,231/2,812 = **43.8%** |
| **PLACEBO — a *different* ore tile barriered in the same window** | not run | **28 = 1.0%** (field 0.1%) |
| source | [V68 §1] | [V47 §6.1] |

⭐ **The v47 placebo is the guard that makes this causal rather than ambient: 80.3%
against a 1.0% base rate from the identical code path — 80×.**
**And it is doctrine, not a v68 novelty — CONTROL RUN.** The v68 probe was
re-run on **150 randomly-sampled archived v47 games**: **35.9% of barriers on ore
(994/2,770), 90.6% of harvester kills covered within 30 rounds (317/350), median
latency 1 round** [V68 §1]. ⇒ **v47 and v68 are the same on this plank.**
**Watch.** G-D r45 (harvester on `(6,10)` dies → barrier **the same round**);
G-E r45→r46; G-C r38→r39 (**our** harvester on `(6,7)`); A game 5 r76→**r77**
`(13,11)`, r78→**r79** `(23,8)`, r111→**r112** `(12,6)` [V47 §2.7/§3.5/§4.2,
V68 §3.1].
**v47 → v68.** **Unchanged.** This is the plank that survived the raid being
deleted — they chew far less and cap just as reliably.
**COUNTER / COPY.** This is a **COPY**, not a counter, and it is the best-evidenced
item in the book — see §6 COPY 1. **The trigger is map-free** (*when an enemy
harvester on tile T dies, barrier T*) and **we run it at 0.0%: literally 0 of
1,381 barriers on an ore tile across 150 of our own recent v175–v177 games**,
while our opponents manage **7.2%** in those same games [V68 §1]. The probe is
not blind on our fixture — it reads 85/1,180 for the opponents there — **so the
zero is ours, not the instrument's.**

### T11 — PRE-EMPTIVE ORE DENIAL, AND THE BARRIER-TO-HARVESTER LAND GRAB

**What.** Two thirds of their ore barriers are not reactive at all: they go on ore
**nobody has harvested yet**. And on contested centre ore they hold the tile with
3 Ti of barrier and later convert it into their own 20 Ti harvester.
**Sharpest number.** **491 of their 784 ore barriers (62.6%) sit on tiles that
never held a harvester**, at a **median round 66** (v68, 112 games) [V68 §1]. On
v47: **6,178 barriers on ore with no preceding enemy harvester death**, against
the field's 587 [V47 §6.1].
**Watch — the land grab, G-C** [V47 §4.2]:
```
r29  BARRIER on (9,9)     <- contested centre ore, nobody's harvester yet
r32  BARRIER on (10,10)
r60  BARRIER on (10,9)
r80  they build their OWN harvester on (9,10)
r89  they DESTROY their own barrier on (9,9) and build a HARVESTER on it
r102 they DESTROY their own barrier on (10,9) and build a HARVESTER on it
```
**MEASURED** on the sequence; **EYEBALL** on the intent.
**Geography, v68** [V68 §1]: of their 784 ore barriers, **559 land in the enemy's
half**, 201 in their own, 24 on the midline — against the opponents' 49/1/10.
**v47 → v68.** Same habit, same share of their barrier budget.
**COUNTER.** `destroy` is free, unlimited and has no cooldown — **so their own
barriers cost them nothing to remove and cost us a full builder-turn plus 3 Ti to
place.** A tile they have barriered pre-emptively is a tile they intend to
harvest later; **denying it is denying a future harvester, not a present one**,
and under `R1000_IS_DEFEAT` that channel is off-currency for us except as
"opens the lane" (§6, COPY 1's PROGRAMME rider).

### T12 — THE NEST: BARRIERS FIRST, GUNS SECOND, INSIDE THE SHELL

**What.** The forward sentinel site is prepared with their own barriers **1–4
rounds before the gun arrives**, including barriers standing **inside the
sentinel's own firing line** — legal, because a sentinel's line ignores obstacles.
A gunner nest built this way would shoot its own wall.
**Sharpest number / anchor.** G-D [V47 §2.5]:
```
r26  barrier (4,15)
r29  barrier (3,14)          <- directly NORTH of (3,15), i.e. IN the firing line
r30  SENTINEL (2,15) facing NORTH   d² to the nearest victim footprint tile = 25
r32  SENTINEL (3,15) facing NORTH   d² = 25
```
**INFERENCE: the barrier shell is deliberate and it is priced on a rule that
applies to sentinels only.**
**v47 → v68.** The band discipline loosened hard (T14) but the shell habit is
visible in v68's ring work too — the barriers that hold the ring double as cover
for a sentinel standing on it.
**COUNTER.** ⭐ **A barrier appearing in the d² 14–32 band of our core is a 1–4
round warning that a sentinel is coming to that spot** [V47 §9 C4]. Tile denial
*before* the plant is the answer; cover is not (T15).

### T13 — THE MAX-RANGE DIAGONAL SENTINEL

**What.** Site the sentinel at exactly d² = 32 — sentinel maximum range — on the
diagonal, aimed at a core footprint corner, so it shoots through the whole map
and nothing in the defender's arsenal reaches back except another sentinel.
**Sharpest number / anchor.** A game 5: sentinel on **(17,15)**, core at
**(21,11)**; `dx = +4, dy = −4`, **d² = 32 exactly**, built facing **NE**, opens
fire **r33**, first shot `(17,15)->(21,11) core#2`, **never seriously contested**,
core dies r114 [V68 §3.1].
**And the tile is reached by a two-bot handoff** (T-anchor, same game): #5 leads
down corridor row 15 with #13 exactly one tile behind for fifteen rounds
(r19–r31, neither building anything); at **r32 #5 steps off (17,15) to (17,14)
and #13, standing on (16,15), builds the sentinel on the vacated tile the same
round.** Orthogonal adjacency is the build rule, so the trailer can only build
onto a tile it is beside — **the leader's job is to have walked it and left.**
MEASURED on ids and rounds; **EYEBALL on the intent** — two bots on one corridor
is not yet shown to be a rule.
**v47 → v68.** v47's median sentinel distance was **25** [STUDY §3.5] — inside
the band, comfortably. **v68 uses both extremes**: d²=32 when the map allows a
clean diagonal, d²=1 when it does not (T14).
**COUNTER.** At d²=32 nothing but another sentinel answers it, and **it cannot
rotate** (T16) — so a gun placed off its axis is fighting something that
physically cannot shoot back. That is the Pantheon counter, and it worked
(§5 item 2).

### T14 — THE POINT-BLANK SENTINEL: STANDING **ON** YOUR RING

**What.** v68 walks the sentinel onto the eight tiles the barriers are supposed to
occupy. `d² = 1` means it is standing on a ring tile of your core.
**Sharpest number.** **53.3% of v68 sentinels are built at d² ≤ 13 of the enemy
core, against v47's 23.9%** [STUDY §4.2]. In match B alone, **six of nine
sentinels and twelve of twenty-nine gunners sit at d² ≤ 10**, counted off the
per-game geometry table [V68 §6]:

| game | map | BC sentinels (round, tile, **d² to enemy core**) |
|---|---|---|
| 1 | 22×22 | r51 (5,6) **25** |
| 2 | 26×12 | **r79 (0,8) d²=8** · **r96 (1,8) d²=5** |
| 3 | 20×20 | r24 (6,5) 18 · **r86 (4,1) d²=1** |
| 4 | 20×20 | r79 (9,5) **9** · r167 (5,6) 32 |
| 5 | 24×24 | **r42 (2,10) d²=1** · **r100 (3,14) d²=5** |

**Watch it kill us.** C game 5: **r54 sentinel at (17,4), d² = 1 from our core
footprint — point blank, on our ring tile**; second at r72 (12,2) d²=25; third at
r99 (16,4) d²=2; **our core dies r103** [V68 §5].
⛔ **A guess made and then checked, kept in place.** The first reading was *"the
r54 sentinel alone accounts for the kill clock — 500 HP ÷ 9 HP/round ≈ 55 rounds,
r54 + 49 = r103"*. **The arithmetic fits and the tape says it is wrong.**
Counting the actual `FireTurret` events landing on our core:
```
 sentinel #163 (17,4)  d²=1   25 shots, r55 -> r103  = 450 dmg
 sentinel #195 (12,2)  d²=25  13 shots               = 234 dmg
 sentinel #245 (16,4)  d²=2    2 shots               =  36 dmg
 gunners: ZERO shots at our core. builder attacks on our core: ZERO.
                                          total 720 dmg on a 500 HP core
```
**It is the NEST, not the first gun — #163 is 62% of it** — and the surplus over
500 is our own core healing [V68 §5]. What survives is [STUDY §5.7]: **every
point of damage to our core came from sentinel fire.** *A "fits the clock"
coincidence is exactly the kind of number that gets published; the discriminator
was counting the events.*
**v47 → v68.** **This is the doctrine's biggest behavioural change after the raid
deletion.** v47 stood outside gunner reach on purpose; v68 walks onto the
doorstep — and it works because the ring is cleared first (T7) and the home gun
sweeps the answer (T19).
**COUNTER.** ⚠ **Do not copy the point-blank plant without the clearance verb
that makes it survivable** (§6, COPY 5). Their own v47 numbers say close plants
die 30% faster: median forward-turret life **20 rounds at d² ≤ 13** against **26
in the d² 14–32 band** [V47 §6.9].

### T15 — THE SENTINEL SHOOTS THROUGH YOUR OWN COLLAR

**What.** A sentinel's single-tile line ignores obstacles. Filling your own eight
ring tiles with your own conveyors blocks their **barriers**; it does nothing to
their **guns**.
**Sharpest number.** v47, n=1,235 games [V47 §6.4]:

| sentinel fire | Bean counters | field |
|---|---|---|
| total sentinel shots | 45,262 | 14,579 |
| **landing on an enemy CORE footprint tile** | **41,911 = 92.6%** | 9,726 = 66.7% |
| passing through ≥1 **enemy** building on the line | 20,533 = 45.4% | 4,724 = 32.4% |
| **core shots fired through enemy cover** | **19,493 = 46.5% of core shots** | 3,954 = 40.7% |

**Watch.** G-C: their sentinel on `(12,2)` fires WEST at core tile `(9,2)` from
r90; the line runs `(11,2) → (10,2) → (9,2)` and **`(11,2)` held OUR OWN CONVEYOR
until r120 — it shot straight through it for thirty rounds** [V47 §4.4]. G-E:
sentinel `(24,14)` facing E hits `(26,14)` through 0033's ring conveyor on
`(25,14)` [V47 §3.2].
**v47 → v68.** Not re-measured on v68; the engine rule is unchanged and v68 fires
36.7 sentinel shots a game, identical to v47 [STUDY §4.2].
**COUNTER.** **Cover is not cover.** Only killing the sentinel, or denying the
tile before the plant (T12), stops the damage. This is the single most expensive
misconception a cage-bot author can hold.

### T16 — A SENTINEL CANNOT ROTATE (engine rule) — AND THEY ARE SLOW TO REPLACE ONE

**What.** `can_rotate` / `rotate` are **gunner-only** (10 Ti + cooldown 1;
CLAUDE.md Controller reference). A forward sentinel is therefore a **fixed-facing
gun aimed at one line, permanently blind to everything off it**, whose only
recourse when attacked from the side is to be rebuilt somewhere else.
**Sharpest number.** **MEASURED confirmation: of 1,125 facing changes across 112
v68 games — 919 Bean counters, 206 opponents — ALL 1,125 are gunners. Zero
sentinels. Zero conveyors.** [V68 §3.4]
**And the replacement is slow.** v68 builds **2.04 sentinels a game**, first at
**median r46** (p10 15, p90 115), **median 42 rounds between consecutive sentinel
builds**, and the ones that die live a **median of 12 rounds** (p10 7)
[V68 §3.4]. [STUDY §5.4] measures the same latency from the other side: v68
sentinel replacement **median 33 rounds, p90 111** (n=44 deaths). **Break the
sentinel and the siege stops for a third of a game.**
**Watch — the whole mechanism in one sequence, A game 4, 30×30** [V68 §3.4]:
```
r28  BC sentinel #108 at (21,14) facing E   -- d²=25, the classic standoff tile
r29  Pantheon gunner (22,14) facing W       -- head-on into the line. DIES r31, age 2
r32  Pantheon sentinel #120 at (21,16) facing N -- TWO TILES SOUTH, i.e. OFF THE AXIS
r37  BC's #108 DIES, age 9.  Pantheon's #120 lives to r81 -- 49 rounds
r37-r127  BC has NO sentinel for ninety rounds
r128 BC's second sentinel, (23,17) -- 100 rounds after the first died
r143 BC's CORE DIES
```
**Pantheon did not duel the sentinel; it stood beside the sentinel's line.**
**v47 → v68.** v47 replaced a dead forward sentinel in a **median 12 rounds (p90
78)**, 16% never; v68 stretched to **median 33 (p90 111)** [STUDY §5.4]. **v68 is
strictly more brittle on this axis than v47 was.**
**COUNTER.** ⭐ **Flank it, do not duel it** — §6 COPY 2. And note the disappointing
half honestly: **killing their first forward sentinel moves them from 63/65 wins
(97%) to 35/43 (81%)** — worth ~16pp and **nowhere near sufficient** [V68 §7].

### T17 — ROTATION IS TARGET EXHAUSTION, NOT PATROL

**What.** Their gunners rotate the instant the last thing on the current line
dies, and fire again immediately. It is a demolition walk, not a sweep.
**Sharpest number.** **MEASURED, 919 BC rotations over 112 v68 games**, mirror
control on the same code path [V68 §2.1]:

| | **BC v68** (919) | **opponents, same games** (206) |
|---|---|---|
| the turret had already FIRED from that tile before rotating | **97%** | 87% |
| **its last target DIED within 3 rounds of the rotate** | **64%** | 47% |
| its last target was still ALIVE | 17% | 17% |
| **fires again within 3 rounds of the rotate** | **91%** | 68% |
| median rounds from the rotate to the next shot | **1** | 1 |
| median rounds since its last shot before the rotate | 1 (**p90 6**) | 1 (**p90 31**) |

**The sharpest cell is the p90: 6 rounds for Bean counters against 31 for the
field. Their guns rotate while still hot; the field's rotate after going cold.**
**Watch the ladder, G-C** — a gunner eating its way to our core, one facing at a
time, **rotating 1–2 rounds after each line empties, three times, and never
rotating away** [V47 §4.4]:

| round | facing | target | outcome |
|---|---|---|---|
| r97 | SW | `(10,4)` our home launcher | 5 shots, dies **r102** |
| r103 | SW | `(9,5)` | dies r105 |
| **r106** | **SW→W** | `(10,3)` our ring conveyor | dies r109, then `(9,3)` r116 |
| **r117** | **W→N** | `(11,2)` our ring conveyor | dies r120, then `(11,1)` r123 |
| **r125** | **N→NW** | **`(10,2)` — OUR CORE**, 7 damage a round, to the end | |

**Price it.** 8.1 rotations × 10 Ti ≈ **81 Ti a game in aiming fees** — four
harvesters' worth, spent purely on turning the barrel [V68 §2.1].
**v47 → v68.** **Quadrupled: 2.0 → 8.1 rotations a game**, and it survives the
matched-opponent control (vs Part-timers, 1.44 → 5.72) [STUDY §4.2]. **They are
buying more of this verb, not less.**
**COUNTER.** The rotation is a **published intention**: the gun turns toward
whatever it will kill next, one round before it shoots it. **INFERENCE:** a bot
that reads enemy gunner facings each round gets a one-round warning on which of
its buildings dies next — which is also the tell for their next cage tile (T7).

### T18 — THEY DO NOT LET GO OF A TARGET

**What.** A gunner that acquires a target keeps firing at it for as long as it
exists, including when the target is being healed faster than the gun can damage
it.
**Sharpest number.** v47, n=1,235 games [V47 §6.7]:

| runs of ≥10 consecutive rounds of one turret firing one tile | Bean counters | field |
|---|---|---|
| number of such runs | 468 | 1,119 |
| total rounds spent inside them | **11,780** | 24,356 |
| **…where the target was being HEALED during the run** | **407 = 87.0%** | 329 = 29.4% |

**Watch, G-E** [V47 §3.3]:
```
r22  0033 plants a SENTINEL on (11,14)
r23  BC plants a GUNNER on (11,15), adjacent, facing N, straight at it
r24..r61  BC fires at (11,14) on EVERY round -- 38 consecutive rounds
          0033 heals it TWICE per round (+8 HP) against 7 damage
r58  0033's titanium hits 0.  The heals stop.
r61  the sentinel finally dies.
```
**38 rounds × 4 ammo = 152 Ti of ammunition to kill one turret that was being
out-healed by 1 HP a round.** BC never rotated that gunner and never gave up.
⚠ **Part of the 87% vs 29% split is a base-rate artefact** — the teams they face
heal ~140 times a game and they heal ~21 [STUDY §3.6], so their targets are
simply more likely to be healed. **The non-artefactual half is the 11,780 rounds
and the v47 rotation rate of 2.0.**
**v47 → v68.** ⚠ **Partly obsoleted, and this is a real tension in the book
(§9 conflict 4).** T17 shows v68 rotating on target *death* 64% of the time and
firing again within 3 rounds 91% of the time — a bot that quadrupled its
re-aiming is by construction less prone to lock. **The lock measurement is v47's
and has NOT been re-run on v68.** Treat "a healed decoy pins a gunner forever" as
**v47-era, direction unknown on the live bot.**
**COUNTER.** A healed decoy in a home gunner's line, plus one builder healing it,
is the cheapest possible test of whether the lock survived — **and it is a leg,
not a plank.**

### T19 — ONE HOME GUNNER, ALWAYS: THE RING SWEEPER AND THE DOORSTEP ANSWER

**What.** Every game carries at least one gunner sitting deep in their own base,
built early, whose whole job is deleting turrets other people plant in their half.
**Sharpest number.** **They destroy 79.7% ± 2.2 of the forward turrets planted in
their half (n=1,131 games, 5,803 turrets) while the opponents they face manage
33.5% — a 2.4× internal ratio. We destroy 42.8% ± 3.3 against our own field's
43.3%** [STUDY §6.2]. Their **home turrets live a median 72 rounds against the
field's 13** [V47 §6.9].
**The verb resolves into two halves** (v47, n=1,235) [V47 §6.6]:

| | Bean counters | field |
|---|---|---|
| forward turrets planted against them | 6,162 | 3,881 |
| **ever shot at by the defender** | **61.9%** | 42.2% |
| mean rounds from plant to first shot | **12.6** | 15.8 |
| answered by a counter-turret on an orthogonally **adjacent** tile within 3 rounds | 344 | 291 |
| mean lag of that counter-plant | **1.18 rounds** | 0.96 |
| **…and the answered turret dies within 15 rounds** | **300/344 = 87.2%** | 205/291 = 70.4% |

**Watch, G-C r5 — a ZERO-round answer** [V47 §4.1]:
```
r5   WE plant a launcher on (11,15)   d²=8 from THEIR core
r5   THEY plant a GUNNER on (11,16) facing N, aimed at it, THE SAME ROUND
r6..r10  it fires every round.  30 HP / 7 dmg = 5 shots
r10  our forward launcher dies, age 5, having thrown nothing
```
**INFERENCE, and the alternative is not excluded:** a same-round answer is
consistent with a reaction (their builder acts later in the round order) **and**
with a pre-planned gunner that happened to land there. The 1-round version in
G-E and the population mean of 1.18 make the reactive reading much more likely;
**no replay can show the branch.**
**v47 → v68.** The home gun **survived the forward migration**: in every game of
match B there is a gunner at d² **197 / 205 / 193 / 325** from the enemy core —
i.e. sitting in their own base, built **r14–r36** — alongside three-to-nine
forward guns [V68 §6]. **One home gun, three-to-nine forward.**
**COUNTER.** **The 38.1% they never shoot at is the window** — and the adjacent
counter-plant is a *turret* answer costing a builder-turn and 20–30 Ti, so **when
their titanium is low it does not happen**: in G-A after r175 they held 0–11 Ti
and answered nothing for 150 rounds [V47 §9 C6]. **Starve them first, then
plant.** This is also the verb *we* most need to copy (§6 COPY 6).

### T20 — THE AMMUNITION DRIP: JUST-IN-TIME, QUANTISED TO THE SHOT

**What.** The core converts titanium to ammunition in many tiny calls, each equal
to the exact cost of the shots the live turrets are about to fire. There is no
opening bank and no reserve, ever.
**Sharpest numbers.** v68, 112 games, mirror control [V68 §2.2]:

| | **BC v68** | **opponents, same games** |
|---|---|---|
| `convert_ammo` calls per game (median) | **67** (p90 102) | 23.5 |
| **round of the FIRST convert (median)** | **27.5** (p10 11) | **1.0** (p10 0) |
| **peak ammo balance ever held** (median / p90 / max) | **26 / 34 / 42** | 30 / **184** / 184 |
| converted Ti minus shot cost, whole game (median) | **+10** (p10 +2) | +10 (p90 **+90**) |
| **convert amount is an exact sum of 4s and 10s** | **8,054 / 8,278 = 97.3%** | 2,011 / 3,755 = **53.6%** |

v47, 69,417 calls over 1,235 games: **98.0% fit `4·live_gunners + 10·live_sentinels`
or one of its components; the field misses the lattice on 21.9% of 60,498 calls**
[V47 §6.8].
**Watch the rhythm change as turrets arrive and die, G-E** [V47 §3.4]:
```
r24 .. r51   4 Ti EVERY ROUND, 28 calls in a row      <- one gunner, reload 1
r52 .. r62   14 / 14 / 4 / 14 / 4 / 14 / 4 ...        <- gunner + one sentinel (reload 2)
r68 .. r100  20 every 2-4 rounds                      <- two sentinels
                                                          55 calls, 516 Ti
```
`4 = one gunner shot · 10 = one sentinel · 14 = 4+10 · 20 = 10+10 · 24 = 10+10+4`.
G-D: first call at **r21 — the round the first sentinel went on the board** — then
flat `20 every two rounds` from r49, exactly two sentinels on a reload-2 cadence;
balance oscillates 0–30 all game; 14 calls, 290 Ti [V47 §2.6]. In A game 5:
**558 Ti converted against 554 Ti of shots — a residual of exactly one gunner
shot — and 33 of their 58 converts exactly equal the NEXT round's bill**
[V68 §2.2].
**Contrast, and it is embarrassing:** in G-C **we** made **8 calls, 36 Ti, for
the entire game**; they made 58 calls, 608 Ti [V47 §4.5]. Part-timers converted
**92 Ti in one call at r0** and never fired a shot [V47 §2.6].
**v47 → v68.** Same rule, **more of it**: 530 → 650 Ti a game, 56 → 67 calls
[STUDY §4.2, V68 §2.2].
⛔ **A TRAP, WRITTEN AND THEN CAUGHT, KEPT IN PLACE.** The first draft of this
called the convert series *"a free read on their intent, one round early"* — a
+10 announces a sentinel shot next round, a +14 a sentinel and a gunner. **That
is true of the REPLAY and false of the GAME.** `CoreConvertAmmo` is a replay
event; the `Controller` exposes `get_global_ammo()` for **our own** balance and
has **no getter for the opponent's ammo or converts at all**. **It is a scouting
instrument for the analyst, not an in-match signal — nothing in `bots/` can
subscribe to it** [V68 §2.2].
**COUNTER.** What *is* actionable is the same fact from the other side: **their
ammunition cushion is ~2 sentinel shots deep and their bank is nearly empty
(mean end bank 137 Ti on v68** [STUDY §5.5]**).** **INFERENCE, untested:** a burst
of cost they must answer with titanium — repairs, rebuilt barriers, a forced
rotation — competes directly with the next round's shots, because the shots are
funded a round at a time. **A hypothesis a leg could test; not a measurement.**

### T21 — THE MEAT GRINDER: RE-SEEDING A TURRET ONTO A TILE THAT HAS KILLED THIRTY

**What.** Their forward-turret siting scores a tile by geometry and carries no
memory that the tile has killed everything ever put on it.
**Sharpest number.** MEASURED, 112 archived v68 games: they built 780 turrets on
701 distinct tiles; **79 of those builds are a rebuild on a tile where one of
their own turrets had already died**, median rebuild latency **4 rounds** (p10 1)
[V68 §8]. **And the tail is not a tail:**

| game | map | tile | **d² to the ENEMY core** | **turret builds on that ONE tile** | lifespan of each | span |
|---|---|---|---|---|---|---|
| **M1** (r418, **BC won**) | 12×12 | **(0,0)** | **2** | **31 gunners** | **every single one lived exactly 1 round** | r125 → r298 |
| **M2** (r213, **BC lost**) | 20×20 | **(16,15)** | **4** | **30 gunners** | 2–3 rounds each | r29 → r192 |

**Thirty-one gunners onto one tile, each dying the round after it is built, for
173 rounds.** At mid-game scale a gunner is 30–45 Ti ⇒ on the order of **1,000+
titanium into a single tile**, and in M2 they lost the game while doing it.
⛔ **THE HONEST CORRECTION, and it comes from the other part** (§9 conflict 5).
The v47 watch formed the same hypothesis — *"they re-plant onto tiles where their
own turret just died, that is the defect"* — and **refuted it at population
scale: BC re-plants on a tile where it already lost a turret 566 times in 1,235
games (0.46/game); their opponents in the same games do it 1,005 times
(0.81/game). BC does it LESS than the field** [V47 §5.2]. **The v68 §8 cell has
no mirror control.** ⇒ **The merged reading: same-tile re-seeding is a
league-wide pathology whose most extreme instances happen to be theirs. It is not
a Bean-counters differentiator.**
**v47 → v68.** Rate not comparable across the two probes (different definitions,
different eras: 0.46/game v47 vs 79/112 = 0.71/game v68). **Direction unknown.**
**COUNTER.** ⚠ n = 79 events across 112 games, of which **two tiles account for
61**; only 2.9% of their turret tiles are built on more than once. **What is
cheap to test is whether the behaviour is TRIGGERABLE** — does a reliably-covered
tile near our core reproduce it? **That is a leg, not a conclusion.** [STUDY §5.4]
concluded *"break the guns, not the belt"*; this would sharpen it to *"break the
guns on a tile they will re-seed, and they will keep paying"* — **if** it
reproduces.

### T22 — THEIR SEAL LEAKS, AND THEY CUT THE HOLE THEMSELVES

**What.** A builder cannot stand on a tile holding a building, **including its
own**. So the tile their siege bot most wants to stand on is the tile it just
sealed — and it destroys its own barrier to walk through.
**Sharpest number.** v47 ring barriers the attacker placed and lost, n=1,235
games [V47 §6.5]:

| | Bean counters | field |
|---|---|---|
| killed by the defender (melee or fire) | 1,506 | 167 |
| **disappeared with no attack and no shot on them** | **4,323** | 66 |
| …an own builder steps onto the tile within 1 round | 1,425 (33%) | 43 |
| …replaced by their own conveyor within 5 rounds | 2,524 (58%) | 1 |
| **…and the DEFENDER retook the tile within 5 rounds** | **34 = 0.8%** | 5 |

⇒ **74% of the seal tiles they lose, they demolish themselves — and the league
converts 0.8% of those 4,323 openings. That is ~3.5 uncontested reopenings of the
seal per game that nobody takes.**
**Watch, G-E r50–r60** [V47 §3.1]:
```
r50  BC barrier (25,15) built by bot12
r52  it DIES, and bot12 MOVES (24,15) -> (25,15) the same round
r54  BC rebuilds it            r55  destroys it again, bot12 moves on
r56  BC destroys its own (25,14), bot12 moves onto it
r57  rebuild (25,15)           r59  destroy (25,15) again
r60  0033 REBUILDS ITS OWN CONVEYOR on (25,15)   <- the victim retakes the tile
```
**Related pathology — the build/destroy thrash.** Tiles built on **five or more
times by the same team in one game**: BC 639 (0.52/game) against the field's 221
(0.18/game), **12,368 builds spent on them, worst single tile 893 builds in one
game** [V47 §6.10]. In **TH** a ring tile enters a **two-round barrier ↔ conveyor
oscillation running from r379 past r407** — the seal subroutine and the belt
subroutine fighting over the same tile, each undoing the other, at ~6 Ti and a
builder-turn per cycle.
**v47 → v68.** Not re-measured on v68. **The engine constraint that causes it is
unchanged**, and v68's circumnavigation walk (T6) puts a bot on ring tiles just
as often — **INFERENCE: it is still there.**
**COUNTER.** ⭐ **The cheapest row in the whole book, and nobody in the league is
taking it.** A builder parked on our own ring that rebuilds into any gap **the
same round** converts most of ~3.5 openings a game into a permanent denial —
because **our 3 Ti barrier on that tile is as good as theirs**, and it is the
tile they cannot re-seal without another ten-attack eviction (T8).

### T23 — ZERO LAUNCHERS, ZERO THROWS, ZERO COUNTER-THROW

**What.** They have never built a launcher, have no throw, and have no code path
that has ever had to survive being thrown.
**Sharpest number.** **0 launchers in 1,385 games** [STUDY §3.9]; **0 launchers
in the 112 archived v68 games** [V68 §5.1].
**⭐ And we accidentally ran the best experiment in the slate.** C game 2 (26×12,
BC core (2,5), ours (22,5)); our launcher **#137 built at (1,7) on r52, 20 Ti,
once** [V68 §5.1]:
```
 r54   THROW  BC builder #8  (2,8) -> (0,11)
 r55-58 #8 walks (0,11)->(0,10)->(0,9)->(1,9)->(2,9)
 r59   #8 steps back onto (2,8)  ->  THROW  (2,8) -> (0,11)
 r64  THROW   r69  THROW   r74  THROW   r79  THROW   r84  THROW   r91  THROW
```
**Eight throws, r54 → r91, cycle length median 5 rounds (p10 5, p90 7), the SAME
destination tile (0,11) all eight times, and the SAME five-tile return route on
seven of eight.** Their builder never varied the plan, never routed around the
launcher, and **never attacked it**.
**Census: a Bean counters builder has been thrown exactly EIGHT times in 112
archived v68 games — all eight are these, in our match. Nobody else in the league
has thrown one.**
⛔ **The border-crash channel did NOT fire, and that is consistent with the banked
evidence.** `(0,11)` is a west-border tile; their builder survived all eight
throws. [STUDY §3.9]: of 162 kidnaps of a Bean counters builder across the
archive, **95 landed on a border tile and 1 died**, against a 2.2% field baseline.
**Stop expecting the crash; start using the displacement.**
⭐ **THIS REOPENS A ROAD [STUDY §3.8] CLOSED.** That section retired *"kill their
four builders"* because they lose only 0.42 builders a game and replace 91% of
them within a median of 2 rounds. **But a thrown builder is not a dead builder —
so no replacement is triggered at all.** One 20 Ti launcher removed **25% of
their entire workforce for 37 rounds**, zero further spend, zero risk.
**Denial by displacement is not the same road as denial by killing, and the data
that closed the second says nothing about the first.**
**v47 → v68.** Zero in both eras, and the v47 side adds the price of the
alternative: killing the siege bot buys **11 rounds and a 12.9% permanent stop**
(T2). **Displacement's ceiling is higher and its cost is lower.**
**COUNTER.** ⚠ **HONEST n: one loop, one game, one builder — a mechanism
demonstration, not a rate.** What it justifies is a pre-registered leg (§6
COPY 3), not a shipped plank.

### T24 — NO REMOVAL LOOP FOR A GUN ON THEIR OWN BELT

**What.** Their kill chain is **economy → ammunition → turrets**. They have a
repair loop for a belt being shot and **no branch that treats the thing shooting
it as a building they could remove**.
**Sharpest number / anchor — G-A, the RATED 0-5 against Pivot** [V47 §5.1]:
* Pivot planted **one 20 Ti gunner on `(7,2)`, their delivery face, at round 60**.
  It fired **86 shots at `(5,2)` and 8 at `(4,2)` and nothing else, ever**, and
  lived 98 rounds.
* **Bean counters rebuilt `(5,2)` SIXTEEN TIMES** — the tape reads
  `BC-c(5,2)` r78, r84, r90, r96, r102, r108… / `BC+c(5,2)/W` r79, r85, r91, r97,
  r103, r109… — **one rebuild per six rounds, into a gun that never moved.**
* ⛔ **The gun was inside their own gunner's reach the whole time.** `(7,2)` is
  d² = 8 from their gunner at `(5,4)` and d² = 5 from `(5,1)`, both well inside
  r²=13. **They rotated `(5,4)` to face it at r60 and then fired ZERO shots from
  it for the remaining 269 rounds.**
* **Whole-game fire ledger: Bean counters 70 shots, all turrets, all 329 rounds.
  Pivot 201. Pivot's single gunner on `(7,2)` fired 94 — more than Bean counters'
  entire team all game.** BC finished with **both home gunners alive, 12 banked
  ammunition, and a core at −15 HP.**
* **`titanium_collected` frozen at 1,480 for 128 rounds while four harvesters and
  eighteen conveyors sat alive on a severed belt** — CLAUDE.md's *"a harvester
  with no route home is worth zero, forever"*, on the rank-1 bot.
**v47 → v68 — DOES IT SURVIVE?** ⚠ **Not directly measured on v68, and this is
the most consequential open question in the book.** Two things are known: (a) the
v68 gunner migration takes guns **away** from home (28.7% → 77.9% built forward)
and the builder-melee-at-home budget fell 70.7 → 15.6 attacks on conveyors
[STUDY §4.2] — **INFERENCE: fewer defenders for the belt, not more**; (b) **the
same collapse shape is visible in the v68 era**, in **D game 1** (30×30, BC core
dies r272): BC builds **1 gunner (r23) and 1 sentinel (r33), both point-blank,
both gone by the midgame, and then never builds another turret in 240 remaining
rounds**, while Leviathan seals BC's ring **1/8 r67 → 8/8 r91** and holds it for
181 rounds; **BC collects 240 Ti in the whole game against Leviathan's 2,280**
[V68 §7]. **Same chain, same order, different opponent, new version.**
**COUNTER.** ⭐ **The biggest single item in the book, and it is still only two
watched games plus one v68-era analogue.** ⚠ The population version — *"do they
answer a gun on their belt?"* — **is measured by neither part** and should be
before anything is built on it (§6 COPY 4, and §8 caveat 6).

### T25 — NO "AM I WINNING?" GATE, AND NO PLAN B

**What.** The branches fire on their own triggers regardless of game state, and
when the cage fails there is no alternative doctrine to fall back on.
**Sharpest number / anchors.**
* **The ore branch has no losing gate.** A game 2, a game **they lose at r116**:
  Pantheon's harvester tile `(7,10)` is killed at r96 and BC barriers it at
  **r97** (dies r98, age 1), **r101** (dies r111), **r113** — **three barriers on
  one ore tile in seventeen rounds while losing** [V68 §3.3].
* **No branch when caging fails.** G-B: the seal stalls at 4/8 at r59 and they
  keep the same four jobs running for **391 more rounds**, planting **fourteen
  forward turrets into an opponent answering them adjacently and losing thirteen
  at a median age of seven** [V47 §5.2/§8]. By r243 Pivot is answering **in the
  same round, five times in a row**.
* **And they will feed a killing tile.** A game 2, 16×16: **BC built zero
  sentinels in 117 rounds** and fought with eight gunners — three of them onto
  **the same tile (10,12)** at r18 (died r24), r25 (died r27), r29 (died r31),
  ~60+ Ti at scale for six rounds of life, into a tile already covered by
  Pantheon guns at (9,11) and (11,11) [V68 §3.3].
**v47 → v68.** Unchanged. **This is the deepest structural property of the bot
and the one least likely to be patched by a version bump**, because it is an
absence rather than a behaviour.
**COUNTER.** Every counter in this book gets to assume **they will not adapt
inside the game**. Their opening is a lookup (T4), their cage has no stimulus
(T4), their ore branch has no state gate, and their recovery is "do the same
thing again". ⚠ **The one thing that DOES adapt across games is their shipping
ladder — v47 → v64 → v66 → v68 in a single morning** [STUDY §2]. **Plan against
the bot; expect the author.**



## §4 THE GRANDIOSE SCHEMES

Five schemes. The first four are things they *do*; the fifth is a thing they
*are not* — and it is as load-bearing as the others.

### SCHEME 1 — THE TOURNIQUET

**A core is a 2×2 block with exactly eight orthogonal neighbours. Those eight
tiles are the only places a conveyor can stand and deliver titanium into it, and
the only places the core can spawn a builder bot.** Bean counters put a 3 Ti
building on those eight tiles. That is the whole idea, and it is the cheapest
war-winning move in the game.

**The dose curve, MEASURED** [STUDY §1]: at a full seal the victim's directed
harvester→core connectivity falls **78.6% → 8.7%** and median titanium collected
falls **975 → 170**. v47 put **55.5% of every barrier it built** on precisely
those eight tiles, occupying a median of **five of eight** and sealing all eight
in **22.3%** of games [STUDY §6.2].

**Execution differs by era.** v47 evicted its way in with builder melee (T8),
face by face, nearest-empty-first (T5), and its median first ring build was r35.
v68 lets its own guns clear the tiles and walks a lap dropping barriers behind
them (T6, T7), first ring tile at median r52 — **later, and against a corpse
rather than a live conveyor.**

**It works in both directions and that is the counter-doctrine the field has
already validated** [STUDY §5.2]: when an opponent seals Bean counters' ring,
**their own connectivity falls 87.6% → 34.9%** and their median collection halves.
O(1) achieves a full seal in 58% of its games against them and takes 54% of them;
DinooniD seals a median 7/8 and takes 50%; HTTP 418 seals 7/8 and took **70%** of
its 20 games against v47. **Part-timers, who build 0.05 barriers a game and never
seal, lose 94.2%.**

⚠ **And the tourniquet's own currency is off-currency for us.** Under
`R1000_IS_DEFEAT`, starving an opponent's `titanium_collected` scores nothing by
itself. It is admissible only as **"it opens the lane"** — a starved opponent
buys fewer turrets, and fewer turrets is what lets our gun live long enough to
kill the core [STUDY §8.9]. **Say it that way in any prereg or it is off-programme.**

### SCHEME 2 — THE NEST: A BATTERY PARKED OUTSIDE THE ANSWER

A sentinel shoots **5.66 tiles** (r²=32), does **18 damage**, reloads 2, and its
single-tile line **ignores obstacles**. A gunner shoots **3.6 tiles** (r²=13),
does 7, and is blocked. The whole v47 nest doctrine lives in that gap: **plant in
the d² 14–32 band — inside sentinel reach, outside every gunner's — behind your
own barrier shell, and shoot the core through everything the defender owns.**

* **Where:** 92% of v47 sentinels in the enemy's half at a **median d² of 25**
  [STUDY §3.5]; the band is worth **+30% of a turret's life** (median 26 rounds
  against 20 for plants inside gunner reach) [V47 §6.9].
* **What it shoots:** **92.6% of 45,262 sentinel shots at an enemy core footprint
  tile, 46.5% of those through the defender's own buildings** (T15).
* **How it is prepared:** barriers 1–4 rounds before the gun, some of them
  *inside* the firing line, legal only because sentinels ignore obstacles (T12).

**v68 tore up the caution and kept the geometry.** It uses **both extremes** —
d² = 32 exactly, on the diagonal, opening fire on r33 (T13), or **d² = 1,
standing on your ring** (T14) — and **53.3% of its sentinels are now inside
gunner reach against v47's 23.9%** [STUDY §4.2]. **It gets away with it because
the ring is cleared first and the home gun sweeps the answer.** Where that
support is missing — a big map, an escort strung out — the forward sentinel dies
in 9 rounds and is not replaced for 90 (T16, §5 item 2).

### SCHEME 3 — THE DRIP: FUNDING THE KILL ONE ROUND AT A TIME

They never bank ammunition. **67 conversions a game, each the exact cost of the
next shots, 97.3% of 8,278 amounts an exact sum of 4s and 10s, peak balance held
median 26** (T20). The first convert lands at **median round 27.5 — the round
their first turret exists** — not at r0.

**Read as a design choice this is elegant and brittle in equal measure.** Elegant:
no titanium is idle, every conversion is a shot that will actually be fired, and
a turret that dies costs them nothing in stranded ammo. Brittle: **the ammunition
supply and the titanium supply are the same tap**, so anything that forces
titanium spending competes with the next round's shots, and **anything that cuts
the belt disarms the guns two links downstream** (SCHEME 5 / T24). Their mean
end-of-game bank is **137 Ti (v68) / 186 (v47)** [STUDY §5.5] — **they spend to
the floor by construction.**

### SCHEME 4 — THE DIVISION OF LABOUR

Four bots, four jobs, no swapping while all four live (T1, T2). **This is what
makes the phases run in parallel rather than in sequence**, and it is why their
kill lands at median r131 with an economy that is also finished by r15.

The cost of the design is that **each job is one bot deep**. The population
numbers say the crew is resilient to *death* — 0.42 builder deaths a game, 91%
replaced in a median 2 rounds [STUDY §3.8] — but **the job takes eleven rounds to
resume, because someone has to walk there, and 12.9% of the time it never
resumes** (T2). And it is *not* resilient to **displacement**: a thrown builder
is alive, so nothing is replaced, and the job simply stops for as long as the
throw cycle runs (T23).

### SCHEME 5 — THE BRANCHES THAT DO NOT EXIST

**This is a scheme by absence, and it is where every game they lose is decided.**

1. **No branch that treats a gun on their own belt as a turret problem.** They
   repair the conveyor, forever, and do not shoot the gun — even when the gun is
   inside their own gunner's reach and that gunner is already facing it (T24).
2. **No "am I losing?" gate.** The ore branch fires three times in seventeen
   rounds in a game they lose at r116 (T25).
3. **No plan B when the cage stalls.** G-B: 391 rounds of the same four jobs and
   fourteen forward turrets fed into an adjacent-answering opponent (T25).
4. **No counter-throw, no re-plan after displacement** (T23).
5. **No memory that a tile has killed everything put on it** (T21) — with the
   honest caveat that the field does this *more* than they do.
6. **No rotation on a sentinel** — an engine rule, not a design choice, but they
   have no re-site rule to compensate and their replacement latency is a median
   33–42 rounds (T16).

⇒ **The doctrine is a very good opening and a very good midgame with no error
recovery.** Everything in §5 is a way of forcing an error it cannot recover from.



## §5 WHERE IT BENDS

Ranked by (measured size × our ability to act on it × how cheap the test is).
**Every item carries its caveat on the same line, because these are the cells
most likely to be lifted out of context.**

### 1. BIG MAPS — the biggest single crack, and it survives holding the opponent fixed

**MEASURED, 112 archived v68 games, banded by map area** [V68 §3.5]:

| map band | n games | **BC game wins** | median game length | gunners/game | **median max enemy-ring tiles held** |
|---|---|---|---|---|---|
| **SMALL** (≤18×18, area ≤324) | 38 | **38 (100%)** | 133.5 | 5.76 | **7 of 8** |
| **MID** (20×20 … 24×24) | 49 | 43 (88%) | 139 | 4.51 | 5 of 8 |
| **BIG** (>576: 26×12, 28×18, 25×25, 30×30) | 25 | **17 (68%)** | 143 | 4.44 | 5 of 8 |

⭐ **And the gradient survives holding the opponent fixed** — the control that
matters, because map draw and opponent are entangled in this pool:

| opponent | SMALL | MID | BIG |
|---|---|---|---|
| **Pantheon** (40 games) | **13/13 = 100%** | 11/15 = 73% | **6/12 = 50%** |
| Part-timers (25) | 5/5 | 13/13 | 7/7 — 100% everywhere |
| Ouroboros (11) | 6/6 | 5/5 | — |
| HTTP 418 (archived, 4) | — | 4/4 | — |

**Against a competent opponent, Bean counters v68 wins every small-map game and
half the big-map games.** Part-timers is the control that shows the gradient is
not about the map alone — a weak opponent loses everywhere.

**INFERENCE on why, and every clause of it was watched in A game 4:** on a big
map the walk to the enemy core is 10–15 rounds longer, so the first sentinel
lands later; the standoff tile is further from the escort, so it is easier to
flank off-axis; **the sentinel cannot rotate to answer**; the replacement takes a
median 33–42 rounds; and the ring seal tops out at 5/8 instead of 7/8 because the
two cage bots are strung out over more ground. **Space is what the doctrine
cannot buy.**

⚠ **CAVEAT:** these 112 games are **~90% unrated challenges** and the map bands
are **not balanced across opponents**. **Quote the within-Pantheon row.**

### 2. THE UNROTATABLE SENTINEL, FLANKED OFF-AXIS

Pantheon killed a forward sentinel in **9 rounds** by placing its own sentinel
**2 tiles off the victim's firing line**; the killer lived **49** (T16, A game 4).
**A sentinel cannot rotate — 1,125 of 1,125 measured facing changes are gunners.**
Break it and the siege stops for a **median 33–42 rounds (p90 111)**; in A game 4
the gap was **91 rounds** on a 30×30 and they lost the game.

⚠ **CAVEAT, two parts.** The engine rule is safe; **the counter itself is n = 1
watched instance.** And the payoff is bounded: **killing their FIRST forward
sentinel moves them only 97% → 81%** (63/65 → 35/43 wins) [V68 §7]. **Necessary,
nowhere near sufficient.**

### 3. SEAL THEIR RING BACK — and the threshold is SIX TILES

**MEASURED across all 112 archived v68 games, banded by the most ring tiles the
OPPONENT ever held on Bean counters** [V68 §7]:

| opponent's seal on BC's ring | n games | **BC wins** | median BC `ti_collected` | median game length |
|---|---|---|---|---|
| 0–3 of 8 | 71 | **68 (96%)** | 1,280 | 125 |
| 4–5 of 8 | 19 | **19 (100%)** | 1,540 | 139 |
| **6–7 of 8** | 17 | **8 (47%)** | 1,340 | 179 |
| **8 of 8** | 5 | 3 (60%) | 1,330 | 386 |
| **pooled ≥6/8** | **22** | **11 (50%)** | — | — |

**The discontinuity is at SIX TILES. Below it they win 87 of 90 (96.7%); at six
or more they win 11 of 22 (50%).** Watch it happen in **D game 1**: Leviathan
goes 1/8 at r67 → 8/8 at **r91**, twenty-four rounds from first tile to full
seal, holds it for 181 rounds, and BC's core dies at r272 with 240 Ti collected
[V68 §7].

⚠⚠ **CAVEAT, and it is not dressed up: THIS IS CORRELATIONAL.** Games where an
opponent reaches 6/8 also ran longer (median 179/386 vs 125) — more rounds is
more chance to seal — and are plausibly games Bean counters were already losing
for other reasons. **Reverse causation is entirely live.** What the cell
licenses is *"the seal-back is the shape that shows up in every game they lose"*,
which is what [STUDY §5.2] found by a different route (O(1) seals 8/8 in 58% of
games and takes 54%). **It does not license a causal dose curve, and a leg would
have to establish one.**

### 4. THE DISPLACEMENT LOOP

One 20 Ti launcher held one of their four builders in a **5-round throw cycle for
37 rounds, 8 throws, same destination tile every time, same return route 7 of 8
times**, and they never attacked the launcher (T23). **25% of their workforce, for
one build.**

⚠ **CAVEAT: n = 1 loop, 1 game, 1 builder — a mechanism demonstration, not a
rate.** And **the CRASH channel did NOT fire**: their builder survived all eight
border throws, consistent with [STUDY §3.9]'s 1 death in 95 border exiles.

### 5. THE PIVOT COLLAPSE — the v47 cautionary tale, and what of it survives into v68

**The tale.** On the RATED ladder at 03:32:59Z on 2026-08-21 — v47's
second-to-last day as incumbent — **Bean counters lost 0-5 to Pivot v236, rating
2054.74, −10.25** [V47 §5]. Four of five games ended with their **core physically
destroyed**; the fifth was an r1000 tiebreak they also lost. **Pivot's core
finished 500/500 in all five.**

| game | map | rounds | condition | BC collected | Pivot collected | BC core |
|---|---|---|---|---|---|---|
| **g1 (G-A)** | 30×30 | 329 | `core_destroyed` | 1,480 | 3,340 | **destroyed** |
| g2 | 20×20 | 1000 | `titanium_collected` | 10,780 | 13,390 | survived at 300/500 |
| **g3 (G-B)** | 20×26 | 450 | `core_destroyed` | 2,810 | 4,530 | **destroyed** |
| g4 | 30×30 | 221 | `core_destroyed` | 620 | 2,070 | **destroyed** |
| g5 | 30×30 | 160 | `core_destroyed` | 400 | 1,390 | **destroyed** |

⚠ **The 500/500 is the FINAL number, not a damage claim.** In g1 their sentinels
took Pivot's core from 500 down to **284 by round 100** and **Pivot healed all of
it back**. **The siege connected and was simply out-repaired.**

**The four things Pivot did that the doctrine could not answer** [V47 §5.3]:
1. **GUNS ON THE BELT, NOT ON THE CORE.** 94 of Pivot's shots went into two
   conveyor tiles. Their kill chain is economy → ammo → turrets; **severing the
   first link disarms the last** (T24).
2. **ANSWERED EVERY FORWARD TURRET ADJACENTLY, IN VOLUME, AND WON THE TRADE.**
   G-B: 32 Pivot turret plants against 14 BC plants; **BC's median forward-turret
   life 7 rounds**; a 20 Ti gunner deleting a 30 Ti sentinel, fourteen times, with
   nothing changed between attempts.
3. **OUT-HEALED THE SIEGE.** Pivot heals ~307 times a game on its own buildings
   against Bean counters' 20.6 [STUDY §4.3].
4. **DENIED THE CAGE BY OCCUPYING ITS OWN RING FIRST.** G-B r119: Pivot fills its
   four remaining ring tiles with its own conveyors; the seal freezes at 4/8 for
   **331 rounds**. Cross-game the same move is worth **+20–30 rounds of delay**
   on the first cage build (T5).

**The heal arithmetic — the exact reason the siege lost, and it is an ENGINE
fact, not an inference** [V47 §5.4]:

| action | cost | effect | **Ti per HP** |
|---|---|---|---|
| `heal` (builder) | 1 Ti | +4 HP | **0.25** |
| sentinel shot | 10 ammo = 10 Ti (convert is 1:1) | 18 damage | **0.56** |
| gunner shot | 4 ammo = 4 Ti | 7 damage | **0.57** |

⇒ **Repairing a core is 2.2× cheaper per hit point than shooting one.** In G-A
Bean counters landed **35 sentinel shots = 630 damage** on Pivot's core; Pivot
healed **158 times = +630 HP, exactly**; low point **74/500 at round 161**; **Bean
counters healed their own core 0 times all game.**

⚠ **THE HONEST LIMIT, and it is why this is not a free lunch.** Heal throughput
is capped by builder-turns at 4 HP per builder per round. **Pivot's actual heal
rate in G-A was 0.48 heals a round** — it only *matched* the incoming 1.9 HP/round
because **Pivot had already killed the turrets**, holding BC's whole-game output
to 35 shots. In G-C, against three live BC turrets doing ~21.5 HP a round, **our**
core repair ran at 6.7 HP/round and covered **less than a third**. **The heal race
is winnable only AFTER turret suppression, never instead of it.**

**What Pivot did NOT do, and it matters: it never caged.** 0 of 8 on Bean
counters' ring across all 450 rounds of G-B. ⇒ **There are two working counters
against v47** — *guns on the belt plus heals* (Pivot) and *mirror the tourniquet*
(O(1), DinooniD, HTTP 418) — **and only one of them is on this slate.**

**⇒ WHAT SURVIVES INTO v68 — the merge's reading, stated with its label.**
* **MEASURED, and it points the wrong way for them:** v68 moved its gunners from
  home to the enemy core (28.7% → **77.9%** forward) and cut builder attacks on
  enemy conveyors 70.7 → 15.6 [STUDY §4.2]. **INFERENCE: there is LESS at home to
  answer a gun on the belt than there was in v47, not more.**
* **MEASURED, and it is the strongest evidence available:** **the same collapse
  shape occurs in the v68 era** — **D game 1**, where BC buys one gunner (r23)
  and one sentinel (r33), both point-blank, loses both by the midgame, **never
  builds another turret in 240 remaining rounds**, is sealed 8/8 by r91, and dies
  at r272 having collected 240 Ti to Leviathan's 2,280 [V68 §7]. **Economy
  severed → ammunition starved → no turrets → dead core**, exactly as in G-A.
* ⚠ **What is NOT measured, by either part: the population question "do they
  answer a gun on their belt?"** [V47 §9 C9] flags it explicitly as unmeasured at
  n=2 games. **The v68 part does not measure it either.** ⇒ **This is the single
  highest-value unclosed measurement in the book** (§8 caveat 6).
* **And one v47-era counter is already dead against v68:** HTTP 418 — the team
  that beat v47 **70% of the time** and the only counter in the field that builds
  launchers — **took zero games off v68 in match B, 5-0** [V68 §6, STUDY §4.3].

### 6. THE COUNTER-SEAL THRESHOLD AND ITS COMPANION — what actually correlates with them losing

Putting items 3 and 5 together, the shapes present in **every** Bean counters
loss on record are:
* the opponent holds **≥6 of their 8 ring tiles** (v68 era, 50% of such games);
* **or** the opponent kills their forward guns faster than they replace them and
  heals through the residue (v47 era, Pivot; v68 era, Pantheon on big maps);
* **and in the worst cases both**, which is D game 1.

⚠ **Neither is established as causal.** Item 3's threshold is correlational by
its own admission; item 5's mechanism is watched in three games. **What the pair
licenses is a target shape for a leg, not a plank.**

### 7. THE MEAT GRINDER

They will re-seed a killed turret onto the same tile — **31 times, one round of
life each, 173 rounds, 1,000+ titanium** (T21). ⚠ **CAVEAT: rare (2.9% of their
turret tiles), two tiles account for 61 of 79 events, no mirror control on the
v68 cell, and the v47 population check says they do this LESS than the field
(0.46 vs 0.81 a game).** The question worth a leg is whether it is **TRIGGERABLE**,
not whether it is a differentiator.

### 8. SMALL MAPS KILL THE STANDOFF — and they know it

On 16×16 in A game 2 they built **zero sentinels in 117 rounds** and fought with
eight gunners; on a board that small there is barely a tile both inside sentinel
reach (r²≤32) and outside a defending gunner's (r²>13). ⚠ **CAVEAT: n = 1 game
for the zero-sentinel behaviour.** The 112-game version of the same effect is the
gunners-per-game rise on small maps: **5.76 vs 4.44** (item 1's table).

**And note the irony: small maps are where they are strongest (38/38).** The
standoff dies and they win anyway, because the walk is short and the cage
completes at 7/8.



## §6 WHAT WE COPY FOR THE SKALMAN LINE

**Why this section exists.** `PROGRAMME.md` declared a new line on 2026-08-21:
**`NEXT_LINE: skalman`, `NEXT_LINE_DOCTRINE: beancounters_replication_then_amplify`,
`NEXT_LINE_BENCHMARK: bots/_v542wave`** — Magnus, verbatim: *build our own version
of the Bean counters tactics; basics first, then amplify our specialities.* Phase
1 is **replicate the measured basics properly**; phase 2 is **amplify with our own
toolbox once the basics measure at parity**. `R1000_IS_DEFEAT` survives the line
change under the same directive: *"We play to destroy their cores"* — the cage,
the belt and the nest are means; **core destruction is the end.**

**This section is the bridge.** It is written as a spec a builder can implement
against, plus a **vulnerability ledger** — the failure modes measured in this book
that our own cage bot must not inherit.

⚠ **Nothing here is admitted. No QUEUE row was written by this merge, no bot file
touched, nothing fired.** Each COPY names what is owed before a prereg.

---

### 6.0 THE ONE-LINE READING OF THE WHOLE BOOK, FOR SKALMAN

> **A seal without a gun is a blockade; a gun without a seal is a kill.**
> — the plainest reading of C game 5, where we took 4 of their 8 ring tiles by
> round 22 and built **zero turrets in four of five games**, while they walked a
> sentinel onto our doorstep and killed us at r103 [V68 §5].

**We already build the cage harder and earlier than they do** — 75.4% of our
barriers land on the enemy ring against their 55.5%, median first ring build r12
against their r35 — **and we complete it less often: 12.0% full seal against
their 22.3%** (v177 alone: 25.6%, n=180) [STUDY §6.2]. ⇒ **For SKALMAN the cage is
not the thing to copy. The thing to copy is everything that turns a cage into a
kill.**

---

### COPY 1 — **ORE-TILE DENIAL.** The cheapest and best-evidenced item in the book

**The trigger is map-free and needs no scouting:**

> **when an enemy harvester on tile T dies, build a barrier on T.**

**Their numbers:** 92.5% coverage at median 1-round latency (v68, n=200 kills);
80.3% within 3 rounds against a **1.0% placebo** (v47, n=2,862) — **both eras,
unchanged** (T10). Plus the pre-emptive half: **62.6% of their ore barriers go on
ore nobody has harvested, median round 66**, and **559 of 784 in the enemy's
half** (T11).

**Our number: ZERO. 0 of 1,381 barriers on an ore tile across 150 of our recent
v175–v177 games**, while our opponents manage 7.2% in the same games [V68 §1].
**Two independent instruments agree:** the behavioural census above, and
[STUDY §6.1]'s file:line GREP of `bots/_v542wave/{main,doctrine,eco,raid,siege}.py`
— *"no such branch exists"*. **INFERENCE: our tree treats ore as
reserved-for-harvesters and filters it out of barrier candidate tiles. That is a
one-predicate change, not a feature.**

⭐ **This also retires [STUDY §6.3 CANDIDATE C]'s hold reason.** CANDIDATE C
(OPENDENY) was held because the evidence was per-(map, seat) and *"turning it
into a plank needs a map-free trigger that this study has not measured"*. **The
trigger above is map-free, it is specified, and its base rate is measured at 92.5%
across 112 games on the rank-1 bot.** The hold reason is gone; the road is open
for a prereg.

**Owed before the prereg:** `tools/target_value.py` (one line: `TARGET BAND: …
reachable YES/NO`); a GREP of the incumbent's barrier-tile filter for the ore
exclusion; a hot-turn cost stamp against the ~1,200 µs GRAND margin.
⚠ **PROGRAMME rider:** its only direct channel is the opponent's
`titanium_collected`, **off-currency** under `R1000_IS_DEFEAT`. **It must be
argued as "opens the lane"** — a starved opponent buys fewer turrets, and fewer
turrets is what lets our gun live — **not as economy. This book does not make
that argument; a prereg must.**

---

### COPY 2 — **FLANK THE SENTINEL, DO NOT DUEL IT**

**A sentinel cannot rotate.** Any turret we place **off a forward sentinel's
firing ray** is fighting something that physically cannot shoot back. Pantheon did
it at 2 tiles' offset and won a **49-vs-9-round trade** (T16).

**We already have the code path** — `_door_turret` (`main.py:1653-1744`),
`FS_DOOR_TYPES`, `FS_DOOR_DSQ = 40` [STUDY §6.1]. **What it may lack is the AXIS
term.** [STUDY §6.1] records `FS_SENTINEL_GUNAXIS_PENALTY = 64`
(`doctrine.py:2527`, `siege.py:6160-6161`) for placing **our** sentinels off an
**enemy gunner's** axis; **the mirror — place our answer off THEIR sentinel's
axis — is the thing to grep for.**

⚠ **Overlap owed:** this is adjacent to [STUDY §6.3 CANDIDATE A DOORWIDE] and to
the futility-dropped NESTSHOT/NESTSHOT2 ground (45.75 @ n=1012,
`BARE-STRATIFIED-SWEEP-2026-08-14.md:14`). **Research must state in writing how
the axis term differs from those before either is admitted.**

---

### COPY 3 — **DISPLACEMENT, NOT DECAPITATION**

We already ship launchers and `_fs_evict` (`siege.py:6684-6759`, `FS_EVICT_ON`).
What C game 2 shows is that **a launcher parked on their APPROACH tile — not
their core — recycles the same builder every 5 rounds forever**, because a
displaced builder is alive and therefore **never replaced** (T23).

**We have exactly four targets to choose from and their spawn rounds are 0, 1, 2,
3.** The best target is the **cage walker / siege engineer** — the one bot that
stands adjacent to our core from r35 onward, escortless, and whose job is
resumed only after a median 11 rounds of somebody walking there (T2).
⚠ **n = 1 loop. This is a leg, not a plank.** Pre-register the throw-destination
read off the wire (engine-side positions), **never off our own stdout** — platform
replays strip it (CLAUDE.md, s28).

---

### COPY 4 — **THE BELT-GUN, AND THE BRANCH THAT ANSWERS IT** *(both directions)*

**Offensively:** one 20 Ti gunner on their delivery face took a rated 5-0 off
v47, and the same shape recurs against v68 in D game 1 (T24, §5 item 5).
⚠ **The population question — do they answer it? — is measured by neither part.
Measure it before building on it.** It is cheap: the decoder exists, the metric is
per-game, and no games need firing.

**Defensively, and this is the SKALMAN half:** whatever we build must **not
inherit the defect**. A belt tile being shot repeatedly is a **turret problem**,
not a repair problem. The rule to encode: *if a tile of ours has been rebuilt
N times and keeps dying, stop rebuilding and locate the shooter.* Their sixteen
rebuilds at 6-round intervals into a stationary gun **inside their own gunner's
reach, with that gunner already facing it and zero shots fired**, is the single
most expensive bug in this book (T24).

---

### COPY 5 — **THE NEST SITING RULE, AND ITS DEPENDENCY**

**The band:** d² 14–32 from the enemy core footprint — inside sentinel reach
(r²=32), outside every gunner's (r²=13). **Worth a measured +30% of turret life:
median 26 rounds against 20 inside gunner reach** (v47, n=2,192 vs 1,354)
[V47 §6.9]. **The extreme case is d² = 32 exactly, on a diagonal, aimed at a
footprint corner** (T13) — maximum range, nothing but another sentinel answers.

**Prepare it with barriers 1–4 rounds before the gun, including inside the firing
line** — legal because sentinels ignore obstacles (T12).

⚠⚠ **AND THE DEPENDENCY, because the two eras prescribe OPPOSITE things and
copying the wrong one is a real risk.** v47 said *stay in the band*; v68 says
*walk onto the ring* (53.3% at d² ≤ 13, `d² = 1` three times in the watched
slate). **v68 gets away with it only because (a) its own guns clear the ring
first (T7) and (b) a home gun sweeps the answer at 79.7% (T19).** **Do not copy
the point-blank plant without the clearance verb** — their own v47 data says
close plants die 30% faster, and A game 4 shows what a forward sentinel without
support is worth: **9 rounds.**

**SKALMAN's default should therefore be: band-first, point-blank only once
ring-clearance is measuring at parity.**

---

### COPY 6 — **HOME-RING TURRET CLEARANCE.** The verb where we are measurably average

**Their 79.7% ± 2.2 against their own field's 33.5% (2.4×). Ours 42.8% ± 3.3
against our field's 43.3% (1.0×)** [STUDY §6.2]. **This is the one verb where the
rank-1 team is exceptional relative to its own field and we are exactly average
relative to ours**, on n≈1,000 games each side, **and the code path already
exists** (`_door_turret`), so the change is a constant rather than a feature.

The verb resolves into two halves worth implementing separately (T19): **(a) shoot
at what gets planted — they shoot at 61.9% against the field's 42.2%; (b) when
they plant an adjacent counter-turret, it kills at 87.2% against 70.4%.**

⚠ **PROGRAMME:** a defensive verb ⇒ carries **`DEFENCE_ADMISSION_BAR`'s r300
timely-kill non-regression as the primary**. And per CLAUDE.md's direction clause,
a "no significant rise in kill round" null must be **restated as an exclusion**
(the CI excludes the regression bar) before any DEFF correction is applied.
**HOT-TURN RIDER: adds** — widening the candidate scan enlarges a per-turn loop on
the home-defence path; stamp it.

---

### COPY 7 — **THE DRIP CLOCK.** A spec, not an aspiration

`PROGRAMME.md` names the drip as SKALMAN's funding rhythm — *"the clock = the
drip-convert rhythm"* — and explicitly **cancels the v544 stall-and-bank
governor** because *"the new doctrine's funding rhythm is the drip, not the
burst-bank."* Here is the measured spec (T20):

```
EVERY ROUND, at the core:
    need = 4 * (live gunners that will fire next round)
         + 10 * (live sentinels that will fire next round)
    if need > current_ammo and can_convert_ammo(need - current_ammo):
        convert_ammo(need - current_ammo)
```
**Calibration targets, from them:**
* **first convert on the round the first turret exists** — median **r27.5**
  (p10 11) on v68; **r21** in G-D, the round the first sentinel landed;
  **never at r0** (that is what the field does: median r1.0, p10 0);
* **~67 calls a game** (p90 102), 650 Ti total on v68 / 530 on v47;
* **peak balance held ≈ 26** (p90 34) — **about two sentinel shots. Never bank.**
* **97.3% of amounts should be exact sums of 4s and 10s.** That share is itself
  the acceptance test: **a drip implementation that does not produce a 4/10
  lattice is not implementing the drip.**

**Our contrast, so the size of the change is honest: in G-C we made 8 calls
totalling 36 Ti for an entire game** while they made 58 calls totalling 608
[V47 §4.5].

⚠ **Do NOT build the reverse — reading THEIR converts as an in-match signal.**
`CoreConvertAmmo` is a replay event; there is no `Controller` getter for an
opponent's ammunition or conversions. **It is a scouting instrument only** (T20's
trap block).

---

### COPY 8 — **THE FOUR-BUILDER CAP AND THE ROLE ASSIGNMENT**

**Cap the workforce at four, spawned r0–r3, and give each a fixed job for the
whole game.** Measured target (T1, T2): exactly 4 in 104/112 games, fourth at r3
(p10 = p90 = 3), median top-share of ring barriers by one bot **1.000**, and in
the modal game **zero deaths and zero replacements**.

Roles, in v68's shape:

| role | what it does | how to recognise it on the wire |
|---|---|---|
| **HOME KEEPER** | belt + harvesters, then repairs and re-lays killed belt tiles; never leaves the home quadrant | forward-action share **0.000** |
| **CAGE WALKER** | corridor march → forward gunner → clockwise lap of the enemy core dropping a barrier per ring tile | places most ring barriers; high batk |
| **ORE DENIER** | chews enemy harvesters, barriers the ore tile, pre-empts unharvested ore | highest melee count; **every barrier on ore** |
| **SIEGE ENGINEER** | lays the long belt, walks as trailer, plants the sentinel, holds the far ring faces | batk 0; the sentinel build is its signature |

⚠ **EYEBALL, retained:** the v47 watch found the siege engineer identifiable by
its **spawn tile** — the ring tile of their own core facing the enemy — in two
games. **Not measured. Do not encode it as a rule without measuring it.**

**And the ordering trick, worth copying on its own:** the **two-bot column with a
tile handoff** — leader walks the corridor, trailer follows exactly one tile
behind, leader steps off the target tile and the trailer builds onto it **the
same round** (T13). It costs nothing but ordering and puts the turret one round
earlier than a single bot that must walk-then-build. ⚠ **EYEBALL on the intent;
rounds and ids are MEASURED.**

---

### COPY 9 — **CAGE GEOMETRY AND ORDER**

Not *whether* to cage — we already do — but *how they order it*:

1. **Take the nearest EMPTY ring tile first; come back for occupied ones by
   eviction.** 99.4% of first cage tiles are a **barrier**; the far face is
   chosen **2.6%** of the time (field 10.7%) (T5).
2. **Build the barrier the round AFTER the tile clears** — mean latency **1.08
   rounds**, 67.4% within 3 (T8). The dose is **ten builder attacks** into a
   20 HP conveyor; **fifteen** into a 30 HP harvester.
3. **In the v68 form, let the guns do the clearing** and follow them around the
   ring (T7) — seven tiles in twenty-two rounds in A game 5.
4. **Walk a lap, do not shuttle** (T6), with the second bot covering the two far
   faces from the inside lane.
5. **Accept 7 of 8.** They killed Pantheon at r114 with `(21,13)` never sealed.
   **The eighth tile is not the plank; the gun is.**

---

### 6.9 ⛔ THE VULNERABILITY LEDGER — what SKALMAN must **not** inherit

**Every row is a measured failure of the doctrine we are replicating. A
replication that copies the strengths and the weaknesses has copied a bot that
loses to Pivot 0-5 on the rated ladder.**

| # | the defect, as measured | anchor | what SKALMAN must do instead |
|---|---|---|---|
| **V1** | **No removal loop for a gun on our own belt.** 16 rebuilds of one conveyor into a stationary gun that was inside their own gunner's reach; **70 shots fired all game to Pivot's 201** | T24, G-A | A tile rebuilt N times without surviving escalates to a **turret-removal** task (melee or fire), not another rebuild |
| **V2** | **Self-inflicted seal holes: 74% of the ring barriers they lose, they demolish themselves** — a builder cannot stand on its own building. **The league retakes 0.8%**; that is ~3.5 free reopenings a game | T22, G-E r50–r60 | Plan the walk so the seal closes **behind** the bot; if a hole must be cut, rebuild it the **same round**; never let the belt subroutine and the seal subroutine own the same tile (the TH oscillation) |
| **V3** | **The unrotatable sentinel with no re-site rule.** Killed in 9 rounds by an off-axis gun; replaced after a median **33–42 rounds**, p90 111; one watched **90-round** hole | T16, A game 4 | Budget a **replacement latency target** and treat a dead forward sentinel as an immediate re-site decision, not a queue item. Prefer the band (COPY 5) unless clearance is at parity |
| **V4** | **No memory that a tile has killed everything put on it** — 31 gunners onto (0,0), each living one round | T21 | Per-tile death memory on turret siting. ⚠ Note the honest caveat: they do this **less** than the field, so this is hygiene, not a differentiator |
| **V5** | **No "am I losing?" gate** — three ore barriers in 17 rounds in a game lost at r116 | T25, A game 2 | Branches that spend builder-turns on denial must yield to survival/kill branches when the core is under fire |
| **V6** | **No launcher, no counter-throw, no re-plan after displacement** — 8 throws, same destination, same return route | T23, C game 2 | We already ship launchers and `_fs_evict`; **keep them**, and add the defensive half: a builder that finds itself off-plan must **re-plan from its actual position**, never resume a cached route |
| **V7** | **Target lock with no give-up rule** — 38 rounds, 152 Ti of ammunition, on a target being healed +8/round against 7 damage | T18, G-E | If a target's HP is not trending down over N rounds, rotate or retarget. ⚠ v47-era; v68's quadrupled rotation may already fix it (§9 conflict 4) |
| **V8** | **Build/destroy thrash: 0.52 tiles/game rebuilt ≥5 times, worst 893 builds on one tile**; a 2-round barrier↔conveyor oscillation running 28+ rounds | T22, TH | Arbitrate tile ownership between subroutines explicitly |
| **V9** | **No plan B when the cage stalls** — 391 rounds of the same four jobs, 14 forward turrets fed to an adjacent-answering opponent at a median age of 7 | T25, G-B | A stall detector: if the seal has not advanced in N rounds and forward turret lifetime is below M, change doctrine rather than repeat |
| **V10** | **Spend to the floor** — mean end bank 137 Ti (v68) / 186 (v47); ammunition cushion ~2 sentinel shots | T20, [STUDY §5.5] | This one is a **trade-off, not a bug** — the drip is why nothing is idle. But keep a named floor so a cost-scale shock or a burst of repairs cannot silently cancel the next round's shots |
| **V11** | **Degrades with map size** — vs Pantheon: SMALL 100%, MID 73%, **BIG 50%** | §5 item 1 | The walk is what scales badly. A big-map branch (earlier departure, a second siege bot, or a longer-range opening) is the explicit gap. ⚠ 90% unrated pool; quote the within-Pantheon row |
| **V12** | **The whole kill chain is serial: economy → ammunition → turrets.** Cut link 1 and link 3 disarms two rounds later | SCHEME 3, T24 | Either shorten the chain (a reserve that survives a belt cut) or defend link 1 as if it were the core — **V1 is the same defect seen from the other end** |

---

### 6.10 DO NOT COPY — already ours, or refuted

* **The ring cage itself.** We ship it (`LOKI_BARRIER_SEAL_ON`, `doctrine.py:1227`),
  target it harder (75.4% vs 55.5%) and start earlier (r12 vs r35).
  **Our gap is completion, not adoption** [STUDY §6.1/§6.2].
* **CPU denial.** 3 timeouts in 1,825,401 v47 unit-turns; **0 TLEs in 90,930 v68
  unit-turns** [STUDY §3.7, V68 §11]. **Dead. Do not spend a leg.**
* **Border crash-induction against them specifically.** Their builder survived all
  8 border throws in our own match, on top of [STUDY §3.9]'s 1 death in 95 border
  exiles. **Not demonstrated, not excluded, n too small to be either.**
* **"Kill their four builders."** 0.42 deaths a game, 91% replaced in a median 2
  rounds [STUDY §3.8]. **But see COPY 3 — displacing is a different verb and that
  refutation does not reach it.**



## §7 WATCH-ALONG INDEX — every cited game, with a line you can paste

**`tools/replay_view.py` renders a `.replay26` to a self-contained HTML page with
a round slider and click-to-drop numbered tile markers, writes it under repo-root
`scratchpad/replay_view/`, prints the path, and NEVER opens a browser** — open the
printed path yourself.

⚠ **IT IS NOT AN INSTRUMENT** (its own docstring says so, verbatim: *"THIS VIEWER
IS NOT AN INSTRUMENT… nothing in it is measured against a control"*). **No number
anywhere in this book is cited from a rendered picture.** Note also that it draws
map, entities and HP bars only — **attacks and turret fire are not drawn as
beams**; they show up as the target's HP bar dropping.

**PATTERN SPOT-CHECKED FOR THIS MERGE.** `--help` read, and one line actually
executed: `.venv/bin/python tools/replay_view.py replay_archive/3bf73ae7-…_game_3.replay26`
printed `…/scratchpad/replay_view/3bf73ae7-2da3-4dc3-bd2b-5ce265d702a2_game_3.html`
and opened nothing. **Every `.replay26` path listed below was existence-checked on
disk at merge time.**

### 7.1 The v68 era — the LIVE opponent

| tag | match id | when (UTC) | opponent | score | source |
|---|---|---|---|---|---|
| **A** | `0798229c-f30b-4db3-9102-52c421880cb8` | 11:32:59Z **RATED** | **Pantheon v105** | **3-2** — their closest call, and **a 3-2 that COST them rating** (`eloDeltaA = −1.553` at a 106-point gap) | pulled → `scratchpad/s53_beanwatch68_replays/` |
| **B** | `05d99bef-68a5-487d-9657-33147216921f` | 13:51:10Z **RATED** | **HTTP 418 v124** | 5-0 (`eloDeltaA = −6.374`) | `replay_archive/` |
| **C** | `32b80f90-9ac4-4c4e-9d80-528b785e5526` | 08:11:52Z unrated | **OpenSverige v175 — US** | **0-5** | `replay_archive/` |
| **D** | `07bdf19b-c22d-45e2-8a2c-6f587195cda7` | 14:01:10Z **RATED** | **Leviathan v91** | 4-1 | pulled → `scratchpad/s53_beanwatch68_replays/` |
| **M1** | `74a8f527-1d4b-4461-894a-88600dca9bb7` | 15:31:10Z **RATED** | Leviathan v91 | 3-2 BC | `replay_archive/` |
| **M2** | `487a97fe-d96f-44c3-bb55-f92677e2a619` | 11:18Z unrated | kladde chatte tville (och oss) v172 | 4-1 BC | `replay_archive/` |

```bash
# A g5 -- THE CLEANEST EXECUTION IN THE BOOK. 24x24 maze, kill at r114.
#   watch (17,15) from r32 (the handoff + the d^2=32 sentinel) and the ring r40-r62
.venv/bin/python tools/replay_view.py \
  scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_5.replay26

# A g2 -- 16x16, THEY LOSE at r116. Zero sentinels in 117 rounds; three gunners fed
#   to the same covered tile (10,12) at r18/r25/r29
.venv/bin/python tools/replay_view.py \
  scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_2.replay26

# A g4 -- 30x30, THEY LOSE at r143. The off-axis sentinel counter at r32 and the
#   90-round sentinel gap that follows
.venv/bin/python tools/replay_view.py \
  scratchpad/s53_beanwatch68_replays/0798229c-f30b-4db3-9102-52c421880cb8_game_4.replay26

# B g1 -- the HTTP 418 sweep (the team that beat v47 70% of the time, swept 5-0)
.venv/bin/python tools/replay_view.py \
  replay_archive/05d99bef-68a5-487d-9657-33147216921f_game_1.replay26

# C g5 -- WHAT IT DOES TO US. Point-blank sentinel at (17,4) r54, our core dies r103
.venv/bin/python tools/replay_view.py \
  replay_archive/32b80f90-9ac4-4c4e-9d80-528b785e5526_game_5.replay26

# C g2 -- THE DISPLACEMENT LOOP. Our launcher (1,7) r52; watch their builder #8
#   get thrown to (0,11) eight times, r54 -> r91
.venv/bin/python tools/replay_view.py \
  replay_archive/32b80f90-9ac4-4c4e-9d80-528b785e5526_game_2.replay26

# D g1 -- THE v68-ERA COLLAPSE. 30x30; Leviathan seals 1/8 r67 -> 8/8 r91 and holds
#   181 rounds; BC's core dies r272 with 240 Ti collected
.venv/bin/python tools/replay_view.py \
  scratchpad/s53_beanwatch68_replays/07bdf19b-c22d-45e2-8a2c-6f587195cda7_game_1.replay26

# M1 -- THE MEAT GRINDER, 12x12: 31 gunners onto (0,0), r125 -> r298, one round each
.venv/bin/python tools/replay_view.py \
  replay_archive/74a8f527-1d4b-4461-894a-88600dca9bb7_game_5.replay26

# M2 -- THE MEAT GRINDER, 20x20: 30 gunners onto (16,15), r29 -> r192, BC LOSES
.venv/bin/python tools/replay_view.py \
  replay_archive/487a97fe-d96f-44c3-bb55-f92677e2a619_game_4.replay26
```

⚠ **M1 and M2 game numbers were resolved BY THIS MERGE, not by the source part.**
[V68 §8] cites the match ids without a game number. Resolved from two independent
columns: `corpus/meta_join.tsv` `game_winner_side` (M1: BC = teamB, they won ⇒
games 1/2/5; M2: BC = teamA, they lost ⇒ game 4) intersected with
`corpus/econ.tsv` round bands (M1 r300+ ⇒ games 3/4/5; M2 r200-300 ⇒ games 4/5).
**M1 = game 5, M2 = game 4, unambiguous on both columns. Map size was not
independently verified** — if the board you open is not 12×12 / 20×20, the
resolution is wrong and the other candidate games are listed above.

### 7.2 The v47 era — the background

| tag | match id | fixture | opponent | why it is on the slate |
|---|---|---|---|---|
| **G-A** | `02c59670-cc8c-4528-a4ec-09ab0f85a0da` g1 | **RATED** 03:32:59.724Z | **Pivot v236** | the **0-5 collapse**; belt amputation, 16 rebuilds, 70 shots all game |
| **G-B** | same match, g3 | **RATED** | Pivot v236 | 450 rounds; **14 recovery attempts, 13 deaths, median life 7** |
| **G-C** | `4c901c39-79dd-45dc-a5ae-06db6f5e3a25` g4 | unrated 2026-08-18T17:30:40Z | **OpenSverige v162 — US** | what they did to us tile by tile; our core dies r137 |
| **G-D** | `3bf73ae7-2da3-4dc3-bd2b-5ce265d702a2` g3 | unrated | Part-timers | **their fastest kill in 1,235 games — r60.** The doctrine with the friction removed |
| **G-E** | `9ee3a878-7909-4772-ba8c-e521fb5408c2` g3 | unrated | 0033, 30×30 | the full arc against a real economy; kill r102 |
| **TH** | `008b7e55-6f64-43e2-8fd4-814f7ef3e027` g5 | unrated 2026-08-17 (vs Torsko v80) | — | the **barrier ↔ conveyor oscillation**, r379 past r407 |

```bash
# G-A -- THE RATED 0-5 vs Pivot, game 1. Watch (5,2) from round 60 onward.
.venv/bin/python tools/replay_view.py \
  scratchpad/s53_beanwatch47_replays/02c59670-cc8c-4528-a4ec-09ab0f85a0da_game_1.replay26

# G-B -- same match, game 3. The 400-round turret attrition; watch r243-r275,
#   where Pivot answers in the SAME round five times in a row.
.venv/bin/python tools/replay_view.py \
  scratchpad/s53_beanwatch47_replays/02c59670-cc8c-4528-a4ec-09ab0f85a0da_game_3.replay26

# G-C -- what they do to US (our v162). Watch our ring (9,1) from r90:
#   four evictions, four barriers, each at exactly +1 round.
.venv/bin/python tools/replay_view.py \
  replay_archive/4c901c39-79dd-45dc-a5ae-06db6f5e3a25_game_4.replay26

# G-D -- their fastest kill in 1,235 games, r60. The whole doctrine on one screen.
#   Watch bot4 walk from (15,10) at r0 and build on (4,10) at r11.
.venv/bin/python tools/replay_view.py \
  replay_archive/3bf73ae7-2da3-4dc3-bd2b-5ce265d702a2_game_3.replay26

# G-E -- the full arc vs 0033 on 30x30. Watch (25,14)/(25,15) from r28 for the
#   eviction metronome, then r50-r60 for them cutting their own seal open.
.venv/bin/python tools/replay_view.py \
  replay_archive/9ee3a878-7909-4772-ba8c-e521fb5408c2_game_3.replay26

# TH -- the build/destroy thrash. Watch one ring tile from r379.
.venv/bin/python tools/replay_view.py \
  replay_archive/008b7e55-6f64-43e2-8fd4-814f7ef3e027_game_5.replay26
```

### 7.3 The text tapes — what the two parts were actually written from

```bash
# v47 watch: whole-game narrative, both sides interleaved
.venv/bin/python scratchpad/s53_beanwatch47_watch.py <replay> --bc <0|1> --all
.venv/bin/python scratchpad/s53_beanwatch47_watch.py <replay> --bc 0 --tape --from 60 --to 160
#   --bc per slate game:  G-A 0 · G-B 0 · G-C 1 · G-D 1 · G-E 0

# v68 watch: per-round labelled event tape
#   BUILD / ROT / REEMIT / MOVE / THROW / DIE / FIRE / BATK / BHEAL / AMMO / STACK-STATE / RING
.venv/bin/python scratchpad/s53_beanwatch68_tape.py <replay> [--only ...] [--from N --to N] [--map] [--summary]
```

⚠ **Two of the v68 matches (A and D) and both Pivot games were fetched with
`fcode match replay` because the archiver had not reached them.** They live in
`scratchpad/s53_beanwatch68_replays/` and `scratchpad/s53_beanwatch47_replays/`,
deliberately **not** in `replay_archive/`, so the keeper daemon's `decoded.txt`
ledger is untouched. **They are therefore NOT in `corpus/`** — a re-run of the
112-game or 1,235-game cross-cuts will not include them. **They contribute
narrative, not statistics.**



## §8 CAVEATS, MERGED AND KEPT INTACT

Both parts' caveat blocks, merged into one honest section. **Nothing was dropped
in the merge; where two caveats said the same thing they were fused and both
denominators kept.**

1. **POPULATION — and the two eras have different ones.** The v68 cross-cuts are
   **112 archived v68 games, ~90% unrated challenges**; the v47 cross-cuts are
   **1,235 archived v47 games, 1,115 unrated / 120 ladder**. **Unrated pools
   PROTOTYPES on the challenger side**, so every "them vs the field" share here
   overstates them relative to their rated record (v47: 69.4% archived against
   **51.2% rated**, n=1,570). **Quote each fixture's INTERNAL ratio** — them
   against the opponents they faced in those same games — never a cross-fixture
   difference against our numbers. The five v68 matches watched game-by-game are
   **four rated + one unrated (C, ours)**; the two v47 Pivot games are **rated**.

2. **CLUSTERING, AND NO DEFF IS APPLIED ANYWHERE IN THIS BOOK.** Games cluster in
   matches (5 per match) and in opponents. Every cell here is a point estimate or
   a within-game count, not an interval, so no half-width carries the correction.
   **Any cell promoted to a bar must first be restated with CLAUDE.md's DEFF
   (1.833 unrated / 1.529 rated).** **The three cells most at risk of being
   over-read: §5 item 1's map gradient, §5 item 3's 6/8 threshold, and T19's
   79.7%-vs-42.8% clearance comparison** (which crosses two fixtures and must be
   read as two internal ratios).

3. **THE 6/8 SEAL THRESHOLD IS CORRELATIONAL.** Longer games, and plausibly
   already-losing games, both push the seal count up. Stated at §5 item 3 and
   repeated here because it is the cell most likely to be lifted out of context.

4. **v68 IS UNDER A DAY OLD.** 112 archived games, ~30 rated matches, seven hours
   of rated history at the time of the watch. **Several cells rest on n = 1
   game** and say so inline: the 8-throw displacement loop, the two meat-grinder
   tiles, the zero-sentinel small-map game, the off-axis sentinel counter.

5. **EYEBALL ITEMS, LISTED SO NOBODY LAUNDERS ONE.** These are read off a tape or
   a board by a human without a control, and the merge did **not** upgrade any of
   them: the two-bot column handoff's *intent* (T13, COPY 8); the siege engineer's
   **spawn-tile** identification rule (T2, COPY 8); the centre-ore barrier→harvester
   **land grab** as intent (T11 — the sequence itself is MEASURED); the mis-sited
   turret self-correction in G-D r20–r21 (V47 §2.4). **Their round anchors and
   entity ids are MEASURED; the causal sentence attached to them is not.**

6. ⛔ **THE BIGGEST UNMEASURED CELL IN THE BOOK: "do they answer a gun on their
   own belt?"** [V47 §9 C9] flags it explicitly — **n = 2 watched games** — and
   **the v68 part does not measure it either.** T24 and §5 item 5 are built on
   two v47 games plus one v68-era analogue (D game 1). **The population version
   should be measured before anything is built on it.** It is cheap: the decoder
   exists, the metric is per-game, no games need firing.

7. **BUILD ATTRIBUTION TO A SPECIFIC BUILDER IS POSITIONAL** — the only friendly
   builder orthogonally adjacent to the built tile that round. **Ambiguity is
   reported, never guessed (1 of 45 in A game 5).** The v47 side additionally
   matched `BuilderBuild` field 16 to the round's `placeEntity`, and its GUARD A
   confirmed the unattributed residual is exactly the core spawns and nothing
   else.

8. **TURRET / BUILDING / ORE MATCHING IS POSITIONAL** — a death on a tile paired
   with a later build on the same tile, kind + tile + later round, **not by entity
   id**. Rebuilds on one tile blur a pairing. The effect is symmetric across the
   BC and field columns, **but T22 shows rebuilding is more common on the BC
   side, so T10 and T8 may be slightly generous to Bean counters.**

9. **FIRE ATTRIBUTION RESOLVES SHOOTER AND TARGET BY TILE OCCUPANCY AT ROUND
   START**, per `tools/replay_schema.md`'s `FireTurret` ordering trap. Targets that
   die earlier in the same round therefore read as blank rather than as whatever
   moved onto the tile — deliberate.

10. **`print()` IS STRIPPED FROM PLATFORM REPLAYS** (CLAUDE.md, s28 correction).
    No arm tag, internal state flag or target list is readable. **Every "trigger"
    sentence in this book is an INFERENCE from engine-side facts — position,
    round, event order — and is labelled.**

11. **TWO REFUTED HYPOTHESES ARE RETAINED IN PLACE, NOT DELETED.** (a) *"They
    re-plant turrets onto tiles where their own turret just died — that is the
    defect"* — refuted at population scale, BC 0.46/game vs the field's 0.81
    (T21). (b) *"The r54 point-blank sentinel alone accounts for the kill clock"*
    — the arithmetic fitted and the event count says otherwise (T14). **A third
    trap is retained un-refuted but re-scoped: the ammunition convert series is a
    scouting instrument, not an in-match signal** (T20).

12. **`replay_view.py` IS NOT AN INSTRUMENT** and nothing in this book is sourced
    from a rendered picture (§7).

13. **THE TWO PIVOT GAMES ARE ONE MATCH.** G-A and G-B share an opponent, an
    opponent version, and one twenty-minute slice of the ladder. **Two draws from
    one cluster, not two independent observations.** And [STUDY §4.3]'s fixture
    caveat is load-bearing on Pivot specifically: **300 archived games means Pivot
    has been drilling against them with prototypes** — *"Pivot beats them 61%"* is
    a prototype-vs-shipped comparison. It tells us the **shape** of the counter,
    not its rated strength.

14. **THE `titanium_collected` CHANNEL IS OFF-CURRENCY FOR US.** Under
    `R1000_IS_DEFEAT`, denying their economy scores nothing by itself; it is
    admissible only as *"opens the lane"*. Every economy number in this book is a
    **thermometer**, not a target (§4 SCHEME 1, §6 COPY 1).

15. **NOTHING WAS FIRED, SUBMITTED OR COMMITTED** — by either part or by this
    merge. No matches, no submissions, no edits to `QUEUE.md`, `bots/`, `tools/`,
    `corpus/`, any ledger, or to either source part. The only files written
    outside `scratchpad/` are the two parts and this book. One read-only command
    ran for this merge: the `replay_view.py` spot-check in §7.



## §9 CONFLICTS BETWEEN THE TWO PARTS, AND HOW EACH WAS RESOLVED

**Nine points where the two parts disagreed, appeared to disagree, or where one
was stale. Each is recorded with the resolution rule applied — the live book
prefers the v68 read, but only after checking that the disagreement is real.**

**1. ORE DENIAL — 80.3% vs 92.5%. NOT A CONFLICT: DIFFERENT WINDOWS.**
[V47 §6.1] measures **80.3% within 3 rounds** (n=2,862 harvester deaths on ore,
1,235 games) with a **1.0% placebo**. [V68 §1] measures **92.5% within 30 rounds**
(n=200, 112 games) with a mirror control. Different windows, different eras,
different denominators. ⇒ **Both printed, windows stated inline (T10). Neither
number was averaged, rounded together, or allowed to stand without its window.**

**2. THE v68 PART'S NOTE THAT THE v47 PART "DOES NOT CARRY THIS PLANK" IS STALE.**
[V68 §1] contains a merge note saying a grep of the sibling *"returns only
map-legend and belt lines"*, read **at 805 lines**. The **final** v47 part is
**1,337 lines** and carries ore capping as **§2.7, §3.5, §4.2 and §6.1**, with a
**placebo control the v68 probe does not have**. ⇒ **The note is corrected in this
book. Both parts carry the plank; the v47 placebo cell is the stronger causal
evidence and is printed first in T10.** *(The v68 part's separate v47 CONTROL RUN
— 150 sampled v47 games, 90.6% at 30 rounds — is retained as the cross-era
consistency check it was intended to be.)*

**3. THE STUDY'S §6.1 GREP vs THE v68 PART'S CENSUS ON OUR OWN ORE BEHAVIOUR —
AGREEMENT, NOT CONFLICT, AND WORTH NAMING.** [STUDY §6.1] says *"barrier on an
enemy ORE tile — NO, no such branch exists"* by file:line GREP of
`bots/_v542wave`; [V68 §1] measures **0 of 1,381** of our barriers on ore across
150 archived games of ours. ⇒ **Two independent instruments, code and behaviour,
same answer. Recorded as a two-instrument confirmation in COPY 1** rather than as
one claim repeated.

**4. TARGET LOCK (v47) vs QUADRUPLED ROTATION (v68) — A REAL TENSION, RESOLVED BY
SCOPE.** [V47 §6.7] measures a bot that **does not let go**: 468 fire-runs of ≥10
consecutive rounds, 87% onto healed targets, at 2.0 rotations a game. [V68 §2.1]
measures a bot that **re-aims constantly**: 8.1 rotations a game, 64% following
the target's death within 3 rounds, 91% firing again within 3. **These describe
different behaviour, and the lock has NOT been re-measured on v68.** ⇒ **T18 is
labelled v47-era with direction unknown on the live bot**, and the "healed decoy"
counter is demoted from a counter-note to **a cheap test** (and appears in the
vulnerability ledger as **V7** with the same hedge).

**5. THE MEAT GRINDER — THE v68 PART FOUND IT, THE v47 PART ALREADY REFUTED IT.**
[V68 §8] presents same-tile turret re-seeding as a striking pathology (79 rebuild
events / 112 games; two tiles account for 61) **with no mirror control**.
[V47 §5.2] formed the same hypothesis while watching G-B and then **refuted it at
population scale: BC 566 re-plants in 1,235 games (0.46/game) against their
opponents' 1,005 (0.81/game) — they do it LESS than the field.** ⇒ **Resolved
toward the v47 refutation, because it is the one with a control.** T21 keeps the
spectacular instances (they are real and they are theirs) and **downgrades the
claim from "a Bean counters differentiator" to "a league-wide pathology whose
worst instances are theirs"**, with the missing mirror named as the gap and the
non-comparability of the two rates (0.46 vs 0.71/game, different definitions and
eras) stated.

**6. WHICH COUNTER ACTUALLY WORKS — "GUNS ON THE BELT" vs "SEAL THEM BACK".**
[V47 §5.3] says the counter that beat v47 on the rated ladder is **guns on the
belt plus heals**, and notes *"Pivot never caged — 0 of 8 in 450 rounds"*.
[V68 §7] finds the correlate of v68 losses is **the seal-back at a ≥6/8
threshold**. [STUDY §4.3] says the three teams that beat v47 all do **at least one
of** (seal back) or (out-heal). ⇒ **Not a conflict: there are two working
counter-shapes, and the parts each watched one.** Merged into §5 items 3 and 5,
with §5 item 6 stating the pair explicitly and flagging that **neither is
established as causal.**

**7. WHEN THE CAGE OPENS — r35 (v47) vs r52 (v68). A REAL AND INTERESTING
DIFFERENCE, KEPT AS DIRECTION-ONLY.** [STUDY §6.2] gives v47's median first ring
build as **r35** (mean 49.9 in [V47 §6.3]); [V68 §4] gives v68's median first
enemy-ring tile as **r52** (p10 31, p90 80). **The cage got LATER while the kill
got FASTER (146 → 131).** ⇒ **Kept, and made a headline of §2.2 P2**, because it
is the structural signature of the v47→v68 change: **the gun became the opener
and the cage became the follow-through.** ⚠ **Flagged direction-only** — two
probes, two denominators (1,235 vs 112 archived games), no matched-opponent
control on this particular cell.

**8. THE NEST BAND — v47 SAYS d²14–32, v68 SAYS d²≤13. OPPOSITE PRESCRIPTIONS,
BOTH TRUE OF THEIR ERA.** [V47 §6.9] measures the band as worth **+30% of turret
life** (26 vs 20 rounds); [STUDY §4.2] measures v68 at **53.3% of sentinels inside
d²≤13** and [V68 §6] watches them stand on the ring at `d²=1`. ⇒ **The live book
reports v68's behaviour as the description of the opponent (T14) and keeps v47's
band number as the PRESCRIPTION for us (COPY 5), with the dependency stated: v68
survives point-blank only because its guns clear the ring first and its home gun
sweeps the answer at 79.7%.** **This is the one place where "prefer the v68 read"
would have produced bad advice, and it is called out as such.**

**9. GAME NUMBERS MISSING FROM THE v68 MEAT-GRINDER CITATIONS.** [V68 §8] cites
`74a8f527…` and `487a97fe…` by match id only. **Resolved by this merge** from two
independent corpus columns (§7.1's note): **M1 = game 5, M2 = game 4**, with the
map-size check named as not independently verified and the alternative candidates
listed.

---

## §10 PROBE INDEX

**All probes are read-only and live in `scratchpad/`. None were re-run by this
merge; they are indexed so the numbers above can be reproduced.**

### v68 era (`scratchpad/s53_beanwatch68_*`)

| file | what it does |
|---|---|
| `s53_beanwatch68_tape.py` | the per-round event tape (`BUILD / ROT / REEMIT / MOVE / THROW / DIE / FIRE / BATK / BHEAL / AMMO / STACK-STATE / RING`); `--only`, `--from/--to`, `--map`, `--summary` |
| `s53_beanwatch68_roles.py` | per-builder role trace with positional build attribution |
| `s53_beanwatch68_oredeny.py` / `_oredeny2.py` | ore-tile denial + kill→barrier latency, with mirror control; `_oredeny2` splits by map half |
| `s53_beanwatch68_rot.py` | rotation-stimulus probe, with mirror control |
| `s53_beanwatch68_ammo.py` / `_ammo2.py` | convert-to-fire and just-in-time ammo, with mirror control |
| `s53_beanwatch68_retile.py` | same-tile rebuild / meat-grinder probe |
| `s53_beanwatch68_v68files.tsv` | the 112 archived v68 games (file, BC side, opponent) |
| `s53_beanwatch68_v47sample.tsv` | 150 random archived v47 games — the ore-denial cross-era control |
| `s53_beanwatch68_oursample.tsv` | 150 of our own v175–v177 games — the zero-ore control |
| `s53_beanwatch68_replays/` | matches A and D, pulled read-only from the platform |

### v47 era (`scratchpad/s53_beanwatch47_*`)

| file | what it does |
|---|---|
| `s53_beanwatch47_tape.py` | per-round tape incl. `BuilderBuild` field-16 attribution, `builderAttack`/`builderHeal` with target-owner classification, `coreConvertAmmo`, `fireTurret` with shooter resolved by tile, and an **8-tile ring occupancy snapshot for both cores every round** |
| `s53_beanwatch47_watch.py` | renders that tape as a narrative: ASCII map, turret ledger, ammo series, ring timeline, per-builder role trace, full round tape |
| `s53_beanwatch47_guard.py` | **the guard suite** — GUARD A build attribution, GUARD B geometry with a live complement (`+5,+5` footprint shift returns 340/0 instead of 1480/1480), GUARD C mirror |
| `s53_beanwatch47_census.py` / `_census2.py` / `_census3.py` | the §6 population catalog |
| `s53_beanwatch47_orecap.py` · `_roles.py` · `_takeover.py` · `_collar.py` | ore capping + placebo · role specialisation · siege-job takeover after a death · own-ring collar effect |
| `s53_beanwatch47_replays/` | the two Pivot games, pulled read-only from the platform |

### Study probes (`scratchpad/s53_bean_*`)

`s53_bean_ourseal.py` — our own seal attainment and forward-turret clearance over
1,115 archived v168–v177 games, same instrument with the team index changed
[STUDY §6.2].

### The instrument controls that were actually run — why these numbers are quotable

* **Cross-decoder agreement (v68).** On `05d99bef…_game_1.replay26` the tape emits
  **111 BUILD events, t0=56 / t1=55**; `corpus/events.tsv`, written months earlier
  by a different decoder, holds **111 BUILD rows for the same file with the same
  split**. The `placeEntity`-on-rotate trap is guarded — a re-emit for a known id
  becomes `ROT`/`REEMIT`, never `BUILD`.
* **Mutation test on the ore flag (v68).** The tape marks every harvester build
  ` ORE` / ` !!NOT-ORE`; on that file it reads **9 ORE / 0 NOT-ORE** — which alone
  proves nothing, because **a constant column validates anything**. Mutating
  `envat()` to `return 0` flips it to **0 ORE / 9 NOT-ORE**. **The branch fires
  both ways.**
* **Side-index positive control (v68), run in both directions.** `teamA` in
  `corpus/league_matches.tsv` ⇒ replay team 0, checked on **15 games across three
  matches with different A/B assignments**: A (BC = A) reads t0,t1,t0,t1,t0 = 3-2
  for t0 matching `scoreA=3`; B (BC = **B**) reads t1 five times matching
  `scoreB=5`; C (BC = A, us = B) reads t0 five times matching our recorded 0-5.
  **A decoder with the sides backwards would have failed B and C in opposite
  directions.**
* **GUARD B end-to-end geometry with a live complement (v47).**
  `DistributeResources` landing on a core footprint × 10 must equal that team's
  final `titaniumCollected`: G-A reads BC **1480 == 1480**, Pivot **3340 == 3340**;
  **the same count with the footprint deliberately shifted `(+5,+5)` returns
  340 / 0** — the check *can* fail, and does, when the geometry is wrong.
* **Mirror controls throughout.** Every per-side counter in both parts is produced
  by **one code path with the team index swapped**, so every "field" column is the
  same measurement on the opponents in the same games.

---

*End of book. The two source parts remain unmodified at
`docs/research/PLAYBOOK-beancounters-PART-v47-2026-08-21.md` and
`docs/research/PLAYBOOK-beancounters-PART-v68-2026-08-21.md`; the statistical base
is `docs/research/REPLAY-STUDY-beancounters-v47v68-2026-08-21.md`.*

