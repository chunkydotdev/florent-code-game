# REPLAY STUDY — `kladde chatte tville (och oss)`, the v125–v141 pool, 2026-08-20

**Provenance.** Fresh opus subagent, **no inherited session context beyond the
inputs named here**, hand-commissioned by the research lane s52 (2026-08-20/21)
because `tools/move_miner.py`'s trigger never fires on this opponent — they are
a fast shipper and every version bump resets their coverage before the ≥40-game
threshold is reached. **This is the fast-shipper blind spot, filled by hand.**
**Method:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` (DISCIPLINE);
version-pooling instrument reused verbatim from
`docs/research/REPLAY-STUDY-teamlazy-v253-2026-08-20.md` §4; (map,seat)
instrument from that study's §2.3.
**Inputs:** `corpus/join.tsv`, `corpus/ladder_games.tsv`,
`corpus/league_matches.tsv`, `corpus/events.tsv`, `corpus/builds.tsv`,
`corpus/build_agg.tsv`, `corpus/econ.tsv`, `corpus/throws.tsv`,
`corpus/meta_join.tsv`, `corpus/version_trees.tsv`, `replay_archive/*.replay26`
(**215 kladde files, 0 missing locally**), `tools/corpus/replay_autopsy.py`,
`tools/replay_schema.md`, `docs/research/corpus-howto.md`,
`docs/research/KLADDE-CONVERSION-FAILURE-2026-08-16.md` (the v119-era prior),
`docs/research/REPLAY-STUDY-flotte-v55-2026-08-20.md` (comparison class),
`QUEUE.md`, `HANDOVER.md`, and the read-only trees
`bots/_v488beltbreak2`, `bots/_x3r0v161gungnir`, `bots/_x3r0v162mjolnir`,
`bots/_x3r0v165mjolnirB`, `bots/_x3r0v169mjolnir`.
**Population:** all **215** rated ladder games we have decoded against this
opponent (their v75 → v141). The **POOL** is their **v125+v126+v139+v140+v141 =
45 games / 9 matches**; the comparison era is their **v119 = 110 games /
22 matches**.
**Surface:** rated ladder, us-only archive. No platform calls, no games fired,
no bot edits, nothing committed by this agent.
**Interruptions:** none observed during the measurement passes; every number
below is reproducible from the scripts described inline.

Every claim is tagged **MEASURED** (counted from decoded events) or **EYEBALL**.
**Refuted mechanisms are RETAINED.**

---

## 0. INSTRUMENTS, AND THE CONTROLS RUN BEFORE ANYTHING WAS BELIEVED

**A. The damage ledger self-checks. MEASURED: 430 of 430 core-damage ledgers
report `MATCH`, 0 `MISMATCH`** (`replay_autopsy.py` requires attributed damage
to equal the summed `UpdateHp` deltas on the core id; 215 games × 2 cores).

**B. TRAP 7 (`join.our_team` descends from `winnerSide`) cleared by a
behavioural fingerprint. MEASURED:** per-game launcher builds
(`build_agg.tsv`, metric `build_launcher`): the side `our_team` calls US has >0
launchers and the other side has 0 in **132 of 215 games; 0 contradictions;
83 uninformative** (neither side built one — concentrated in the older eras
where our own launcher use was ~1/game). **They built 0 splitters in 215 of 215
games**, a second one-sided fingerprint.

**C. ⛔ A CORPUS TRAP FOUND IN THIS STUDY AND NOT PREVIOUSLY WRITTEN DOWN:
`league_matches.tsv` CONTAINS THREE TEAMS WHOSE NAME MATCHES `sverige`.**
**MEASURED: `OpenSverige` 1,423 rows, `opensverige - plan B` 1,026,
`OpenSverige - Plan C` 301.** A substring filter on `sverige` pulls **71**
"our" matches against kladde where the true figure is **43**, and the 28 extra
rows carry versions `v29/v69/v70` that read as an implausible version rollback
if you do not notice. Every count below filters on the **exact** string
`OpenSverige`. *(This is the same class as TRAP 4/7/8: a filter that looks
right and silently changes the population.)*

**D. Dead columns avoided.** `econ.tsv`'s `shots` and `deliveries` are
identically zero (traps 5/8) and are not used. Shot counts, where quoted, come
from `build_agg.tsv` metric `shot`.

---

## 1. PREMISE AUDIT — P1, P2, P3 re-derived from `league_matches.tsv`

| premise | verdict | measured |
|---|---|---|
| **P1** "today: 1-4 L, 4-1 W, 1-4 L, 0-5 L across their v140/v141/**v144**" | ⚠ **THREE CORRECTIONS** | Today was **FIVE** matches, not four: `00:52 v140 1-4`, `09:52 v140 0-5`, `13:52 v141 1-4`, `16:12 v141 **4-1**`, `19:32 v141 1-4`. **Games 7-18, not 6-19. Elo −32.05, not ≈−34.** ⛔ **`v144` DOES NOT EXIST.** Their versions today were **v140 → v141 (12:52Z) → v142 (19:52Z) → rolled back to v136 (21:12Z)**. We never met v142 or v136. |
| **P1** "family cumulative since our v162 ≈ −100" | ⚠ **OVERSTATED** | **MEASURED: our v162+ vs kladde = 9 matches, 11-34 in games (24.4%), Elo −76.15.** |
| **P2** "v161 lineage went 2-0 vs kladde; v162 lineage started 0-5" | ⚠ **PARTLY WRONG, and the correction matters** | Our **v161 played exactly ONE match** vs kladde (`10e8755c`, 2026-08-18T09:52Z, **3-2**, +0.20). The two 4-1/3-2 wins just before it were **v159**. The v162-lineage opener **was** 0-5 (`117beb31`, v163 vs their v125, −19.30). |
| **P3** "today's 4-1 is a map/seat draw effect or a their-version effect" | ⛔ **BOTH BRANCHES REFUTED** — see §4.3 | The 4-1 (`9eb06ea6`, 16:12Z) is **their v141 / our v168 / seat A** — *identical* on all three to the 1-4 at 13:52Z (`9d9d2905`). The two matches share two maps and **both flipped**. |

**⭐ AND THE ONE FACT THAT REFRAMES EVERYTHING BELOW (from
`corpus/version_trees.tsv`, the authority):** `v161 = "Gungnir v1 (sprint,
kladde-fixed)" = bots/_x3r0v161gungnir`; `v162 = "Mjolnir v1 (banded opening,
ring claim, endgame)" = bots/_x3r0v162mjolnir`. **These are two different bots
by two different designs, both shipped by the teammate x3r0** — not an
increment. Our own repo line (`bots/_v488beltbreak2` = Sleipnir v2) was
**v158/v159**.

---

## 2. STEP 0 — VERSION POOLING: **POOL v125+v126+v139+v140+v141. THE POOL BREAKS AT v119 → v123/v125, ON 2026-08-19.**

**Method (reused verbatim).** An 11-dimensional THEIR-side profile per game from
`corpus/events.tsv` — first-build round and total count for conveyor, harvester,
gunner, sentinel, barrier, plus builder-bot spawns — median profile per version
group, scale-normalised L1 distance (per-dimension MAD scale computed over all
215 games), permutation null of 3,000 re-splits at the same group sizes.

### 2.1 Adjacent pairs (all our-versions pooled)

| pair | nA | nB | d | null median | null p95 | p | verdict |
|---|---|---|---|---|---|---|---|
| v119 → v125 | 110 | 5 | 0.996 | 0.632 | 1.546 | 0.160 | SAME *(underpowered, n=5)* |
| v125 → v126 | 5 | 10 | 1.010 | 0.899 | 1.608 | 0.373 | SAME |
| v126 → v139 | 10 | 5 | 1.044 | 1.019 | 1.599 | 0.470 | SAME |
| v139 → v140 | 5 | 10 | 0.748 | 0.849 | 1.206 | 0.659 | SAME |
| v140 → v141 | 10 | 15 | 0.426 | 0.634 | 0.972 | 0.887 | SAME |

### 2.2 The powered test, and where it breaks

> **MEASURED. `d(v119, pooled v125-141) = 0.862`, null median 0.286, p95 0.434,
> `p = 0.0000` → DIFFERENT.**

**⚠ Read the two tables together and not separately.** The adjacent pairs are
all n≤15 on one side; the *pooled* comparison is the one with power. **The break
is between v119 and the recent block, and the n=5 v119→v125 cell simply cannot
see it.**

### 2.3 Positive controls — the instrument DOES say "different"

An equivalence instrument that has never returned "different" validates nothing.
**MEASURED, same null, same metric:**

| control | d | p | verdict |
|---|---|---|---|
| v75 vs pooled v125-141 | 2.682 | 0.0000 | DIFFERENT |
| v84 vs pooled v125-141 | 2.116 | 0.0000 | DIFFERENT |
| v97 vs pooled v125-141 | 1.184 | 0.0007 | DIFFERENT |
| v75 vs v119 | 1.952 | 0.0033 | DIFFERENT |
| v84 vs v119 | 1.381 | 0.0013 | DIFFERENT |
| v97 vs v119 | 0.760 | 0.0297 | DIFFERENT |

**Confound control with OUR tree held fixed:** their `v126@our-v162` (n=10) vs
`v140@our-v162` (n=5): **d = 1.231, p = 0.206 → SAME.** The only cell in which
our own version is constant across two of their versions agrees with the pool.

**Second, independent corroboration that the pool is one bot (EYEBALL→MEASURED):**
on **frostgate, seat A, their first sentinel is built at r5 on tile (14,8),
d²=5 from their own core, in FIVE games spanning their v126, v139 and v141 and
our v162, v164 and v168** —
`a7f87ff6…_game_2`, `b30092b8…_game_2`, `63b785aa…_game_2`,
`9d9d2905…_game_3`, `9eb06ea6…_game_2`. A version bump that changed the opening
could not leave a scripted r5 plant byte-identical across three of their
versions.

### 2.4 What actually changed at the break (medians, their side)

| dim | v119 (n=110) | POOL (n=45) |
|---|---|---|
| **first sentinel round** | **r31** | **r11** |
| first sentinel d² to their OWN core | 25 | 16 |
| first barrier round | r148.5 | ~r54–86 |
| **barriers per game** | 5.6 | **14.8** |
| **barriers built on OUR core's ring (d²≤8)** | **0.7/game** | **9.4/game** |
| gunners per game | 2.97 | 2.33 |
| sentinels per game | 7.63 | 6.56 |
| builder spawns | 5 | 5 |

**Dating it against their Elo:** the break lands **2026-08-19** (v123 first seen
07:52Z, v125 12:12Z). Their rating had fallen 1828 (v119, 08-15) → **1736
(v124, 08-19T11:12Z)**, and has since recovered to **1853 (21:12Z today)**.
**So they rebuilt after a 92-point slide, and the rebuilt bot is the one that is
draining us.**

> ### ⇒ **VERDICT: POOL v125/v126/v139/v140/v141 = 45 games / 9 matches. Do NOT pool v119 with it.**
> ⚠ **AND THE POOL IS ALREADY ONE STEP STALE: their ACTIVE version at 21:12Z is
> v136** (rolled back from v142), **against which we have ZERO decoded games.**
> That is the fast-shipper tax and it is why this study is dated, not durable.

---

## 3. Q1 — WHAT KILLS US

### 3.1 One channel, and it is the sentinel — same class as team lazy and Flotte

**MEASURED, POOL (45 games), from the self-checking ledger:**

* **Damage into OUR core: 26,716 HP (594/game) — sentinel 26,352 (98.6%),
  gunner 364 (1.4%), builder melee 0.**
* **Damage into THEIR core: 10,260 HP (228/game) — sentinel 10,260 (100.0%).**

Both sides kill with exactly one weapon. Builder melee contributes **zero** core
damage despite **MEASURED 108.7 builder-attack events per game on their side and
129.0 on ours** — those go into buildings.

### 3.2 The siege clock, with the offset test as the mechanism claim

**MEASURED, POOL:** their sentinels sited **in range of our core (d²≤32)**:
**71 builds, 1.58/game, present in 34 of 45 games, first-in-range median r108.5,
median d² = 18.**

> **⭐ THE MECHANISM CLAIM: their first in-range sentinel → our core's first
> damage, median offset = +1 round; within 0–25 rounds in 26 of 30 games.**

**Anchors (file + round + d²), all POOL, all `core_destroyed` against us:**
`7cb5f911-589b-4cac-a8cf-69b6ec34dd92_game_2` (v141/our v168, valkyrie, seat B)
— in-range sentinel **r37, d²=17**, our core's first damage **r38**, 666 HP
taken, core dead at r639.
`c24dad0e-edee-4f5d-995c-02d30f3b7303_game_5` (v140/our v162, valkyrie) —
**r36 → r37**, d²=16, dead at r207.
`117beb31-9526-4ca2-9209-1ffc53d20935_game_1` (v125/our v163, auroraveil) —
**r28 → r29**, d²=25, dead at r256.
`117beb31-…_game_3` and `c24dad0e-…_game_3` (both royale) — **r40 → r41** and
**r40 → r44**, d²=26 both, dead at **r92 and r94** — the same map, two
different matches, the same clock.
`dd7b26c4-1a78-47a0-8ff4-fb3f8bf05131_game_5` (v140/our v169, icefloe) —
**r87 → r88**, d²=26, dead at r135.

**Control that could have run the other way, and did:** the **same instrument on
the v119 era** returns first-in-range median **r142** with the offset holding in
only **29 of 52** games — i.e. the number moves when the population moves, and
the offset rule is materially tighter now.

### 3.3 The NEW half: a home sentinel by r11

**MEASURED, POOL:** their **first** sentinel is planted at **median r11, median
d² = 16 from their OWN core**, and **27 of 45 games have it by r20** — against
**median r31 / d²=25 / 38 of 110 games by r20** in the v119 era.

This is the plank the other two profiles do not have. **team lazy** builds no
home defence at all (0 launchers, 0 splitters, reactive gunners); **Flotte**
opens with a gunner grind at r20 and holds its sentinel to a r113–116 clock.
**kladde now spends its first sentinel on DENYING OUR RAID, and only later buys
the siege one.**

**Anchors:** `9d9d2905…_game_3` / `9eb06ea6…_game_2` / `a7f87ff6…_game_2` /
`b30092b8…_game_2` / `63b785aa…_game_2` — frostgate, **r5 at (14,8), d²=5 from
their core**, five games, three of their versions.
`7cb5f911…_game_1` (midgard) and `dd7b26c4…_game_2` (midgard) — **r11 at (1,5) /
(26,22), d²=10 / 16**.

### 3.4 ⭐⭐ WHERE OUR KILL STALLS — AND THIS IS THE HEADLINE NUMBER

**MEASURED, "did we ever put one point of damage on their core":**

| era | reach | share (DEFF 1.366) |
|---|---|---|
| their v119 / our v152–v161 (n=110) | **109/110 = 99.1%** | [97.0, 100] |
| POOL v125–141 / our v162–v169 (n=45) | **26/45 = 57.8%** | [40.9, 74.6] |

**Difference 41.3pp against a two-fixture 95% half-width of 13.6pp → EXCLUDES
ZERO.** *(Cluster enumeration in writing: MATCH cluster LIVE — every match
contributes exactly 5 games; OPPONENT cluster DEAD — the stratum is one
opponent; surviving DEFF = rated within-opponent 1.366.)*

Everything downstream follows:

| | v119 era (n=110) | POOL (n=45) |
|---|---|---|
| damage into their core | **942/game** | **228/game** |
| our first damage on their core | **median r34** | **median r147.5** |
| our game share | 52.7% [41.8, 63.6] | **24.4% [9.8, 39.1]** |
| **our core kill by r300 (PROGRAMME primary)** | **47.3%** | **13.3%** |
| our sentinels per game | 11.52 | 5.44 |
| our launchers per game | 1.05 | 4.60 |
| median turns | 224 | 269 |

**Share difference 28.3pp vs a two-fixture half-width of 20.1pp → excludes zero.**

⇒ **They did not get better at killing us (594 vs 346 HP/game into our core is a
real but modest rise). WE STOPPED ARRIVING.** The drain is an offence failure,
not a defence failure — and it is worth stating plainly because
`R1000_IS_DEFEAT` and the r300 bar both read on the half that collapsed.

### 3.5 Attrition ledger (MEASURED, unit deaths per game)

| destroyed | POOL: ours | POOL: theirs | v119: ours | v119: theirs |
|---|---|---|---|---|
| builder bot | 5.8 | 0.6 | 7.2 | 0.1 |
| conveyor | 14.9 | 2.5 | 13.2 | 3.5 |
| harvester | 2.6 | **0.0** | 5.2 | 0.3 |
| **launcher** | **3.8** | 0.0 | 0.3 | 0.0 |
| sentinel | 3.0 | 2.1 | 10.1 | 0.5 |
| barrier | 7.5 | 7.2 | 5.9 | 0.5 |

Two things moved: our **sentinel** deaths fell 10.1 → 3.0 (the v119-era replant
loop documented in `KLADDE-CONVERSION-FAILURE-2026-08-16.md` §1 **is fixed**),
and our **launcher** deaths rose 0.3 → 3.8 as the launcher became our main
forward build. **We swapped one thing that died for another.**

---

## 4. Q2 — THE (map, seat) STRUCTURE: **IT IS NOT THERE IN THE CURRENT POOL, AND THE INSTRUMENT PROVES ITSELF BY FINDING IT IN THE OTHER ERA**

### 4.1 Unanimity test (team-lazy method, verbatim: cells with ≥2 games, 5,000-shuffle permutation of the map label with seat held fixed)

| population | cells ≥2 | unanimous | null median | null p95 | **p** |
|---|---|---|---|---|---|
| **POOL (n=45)** | 11 | 6 (**54.5%**) | 50.0% | 66.7% | **0.322 — NO STRUCTURE** |
| **their v119 (n=110)** | 29 | 14 (**48.3%**) | 18.5% | 31.0% | **0.0000 — STRUCTURED** |
| all 215 kladde games | 37 | 9 (24.3%) | 16.2% | 25.6% | 0.076 |

**This is the control the method needs: the same instrument, on the same
opponent, in the other era, returns a decisive "structured".** So a null in the
POOL is a fact about the POOL, not about the test.

### 4.2 The map class does not transfer across their version break

**MEASURED. Train on v119 (maps with n≥2, share ≥0.6 GOOD / ≤0.4 BAD), test on
POOL:** GOOD **5/19 = 26.3%**, BAD **2/19 = 10.5%**. A 15.8pp gap against a
two-fixture half-width of ~30pp — **nothing.** For contrast the team-lazy study's
equivalent cross-validation ran **76.5% vs 26.7%, excluding zero in both
directions.** **The v119-era "good maps" (ragnarok 4/4, royale 9/10, midgard 7/8)
are now royale 0/3, midgard 2/6, ragnarok 0/1.**

### 4.3 ⭐ TODAY'S 4-1 IS NOT A DRAW EFFECT — three independent ways

1. **The identical-triple control.** `9d9d2905` (13:52Z) and `9eb06ea6`
   (16:12Z) are **their v141, our v168, seat A** — every controllable held
   fixed, 2h20m apart, **1-4 then 4-1**. Seat cannot explain it.
2. **The two shared maps both FLIPPED.** `frostgate` **L@r272 → W@r90**;
   `valkyrie` **W@r189 → L@r261**. If the (map,seat) cell decided the game,
   these are the two games that had to agree.
3. **Leave-one-match-out map prediction ANTI-predicts the 4-1.** Training the
   map class on the other 40 POOL games: of the four wins, **frostgate was BAD
   (0/4 elsewhere)** and **drumlin was BAD (1/3)**; archipelago and nordkap were
   unseen; and the single map the model called GOOD — **valkyrie, 3/5
   elsewhere — is the one game we LOST.**

**What the 4-1 actually differs on is §3.4's variable. MEASURED, the three
v141/our-v168 matches:**

| match | seat | score | damage into their core | into ours | **games where we reached their core** |
|---|---|---|---|---|---|
| 13:52Z `9d9d2905` | A | 1-4 | 205/g | 850/g | **2/5** |
| **16:12Z `9eb06ea6`** | A | **4-1** | **508/g** | **373/g** | **5/5** |
| 19:32Z `7cb5f911` | B | 1-4 | 166/g | 914/g | 3/5 |

⇒ **The 4-1 is the match in which our raid connected in every game.** Whatever
makes that binary flip is the plank; the map draw is not it.

### 4.4 Seat, reported honestly

**MEASURED, POOL: seat A 9/30 (30.0%), seat B 2/15 (13.3%)** — directionally
consistent with the v119 era (A 35/65 = 53.8%, B 23/45 = 51.1%, i.e. **no seat
effect there at all**), but n=15 on seat B makes the POOL split uninterpretable
on its own. **Do not build a seat arm off this.**

---

## 5. Q3 — THE LEAP15 QUESTION: **THE OUTCOME ATTRIBUTION IS NOT DECODABLE (perfect collinearity). THE CODE DIFF IS, AND IT SAYS THE s51 INFERENCE IS FALSE AS WORDED.**

### 5.1 Why outcome attribution is impossible here — MEASURED, not asserted

**Our v162+ games and their v123+ games are the SAME NINE MATCHES.**
`our v162+ vs kladde: 9 matches, 11-34, Elo −76.15` and
`their v123+ vs us: 9 matches, 11-34, Elo −76.15` — **byte-identical
aggregates, because the two version boundaries fall in the same 24 hours.**

The escape hatch was checked and is shut: **MEASURED on `corpus/meta_join.tsv`,
we have ZERO unrated games against any kladde version ≥ v123** (our unrated
coverage against them stops at their v97, plus 25 games at v119). There is no
cell anywhere in the archive where an old our-version meets a new their-version
or vice versa.

> ⇒ **"Our v162-lineage base lacks the leap15 kladde fixes" and "their v123+
> rebuild is stronger" fit the outcome data IDENTICALLY. Neither can be
> preferred on games.** This is the `CLAUDE.md` collinearity hazard (The Bisons
> v4 / our v102) reproduced exactly, and it is why the s51 inference could
> neither be confirmed nor killed by the 4-1.

### 5.2 What IS decodable: the source diff, and it refutes the wording

`bots/_x3r0v161gungnir/doctrine.py` vs `bots/_x3r0v162mjolnir/doctrine.py`,
compared as flag tables (regex over `^[A-Z][A-Z0-9_]{3,}\s*=`):

> **MEASURED: 0 flags removed. 117 flags ADDED (`OPEN_*`, `RING_*`, `END_*`,
> `GD_*`, `KC_*`, `PREFILL_*`) plus three new modules
> (`opening.py`, `ring.py`, `sip.py`, +4,467 lines).
> EXACTLY ONE pre-existing flag changed value:**
> **`RG_CHASE_ON: True → False`** (`_x3r0v162mjolnir/doctrine.py:5889`,
> comment `LEAP16: KILLED AS NOISE, wave 18b`), and it is **still False in
> v165 and v169.**

**The leap15 package has four masters** (`_x3r0v161gungnir/DOCTRINE.md:3454`):
`EB_ON`, `SPR_COLLECT_ON`, `RG_CHASE_ON`, `RG_COVER_UNION_ON`.
**MEASURED across v161/v162/v165/v169: `EB_ON = True`, `SPR_COLLECT_ON = True`,
`RG_COVER_UNION_ON = True` in ALL FOUR trees.** **Three of the four leap15
fixes are still shipped.** Only the gunner re-aim (`RG_CHASE_ON`, FIX 2's
chase half) was turned off.

⇒ **"v162+ lacks the leap15 kladde fixes" is FALSE as stated.** The accurate
statement is: *v162 kept 3 of 4 leap15 masters, dropped the gunner chase, and
bolted on an entirely new opening/ring/endgame system.*

### 5.3 And the "kladde-fixed" label itself was never established on live games

`_x3r0v161gungnir/DOCTRINE.md:3306-3312`, verbatim: *"istones, 0033 and kladde
are 2 cells each and adjudicate nothing… It is 4 cells in total and it is a
smoke signal, not a measurement."* **The v161 submission title says
"kladde-fixed"; the evidence behind it is 4 local mimic cells.** Per
`CLAUDE.md` point 6, a local battery may prioritise a road, never close one —
and a submission NAME is not evidence at all.

### 5.4 The one honest quantitative handle, with its hedge

**RG_CHASE is a HOME-GUNNER re-aim at bodies within d²≤13** (`RG_CHASE_DSQ =
GUNNER_RANGE_DSQ`, `_x3r0v161gungnir/main.py:2661-2705`). Against this opponent
its target would be the builder walking in to plant the siege sentinel.
**But MEASURED: our gunners per game fell 2.04 (v119 era) → 0.71 (POOL)**, so
the subsystem RG_CHASE governs is itself nearly absent from the current build.
**And v161's own smoke measured the chase firing ~1 rotation per game against a
budget of four** (`DOCTRINE.md:3295-3299`). **⇒ RG_CHASE_ON is a NAMEABLE
candidate, not a likely cause. Do not spend a leg on it before §6's P1.**

---

## 6. Q4 — PIECES

*Every piece was grepped against `QUEUE.md` and against the read-only trees
before being written. Adjacent rows checked as instructed: **#40** (pre-seal our
own siege ring), **#41** (forward-sentinel siting d²14-32 + barrier adjacent),
**#59** (enemy launcher pickup envelope), **#79** (plant-and-guard infiltrator),
**#97** (Flotte-class builder cull), **#101** (team-lazy bad-map six).*

### P1 — ⭐⭐ **THE REACH BINARY: WE ARRIVE AT THEIR CORE IN 99.1% OF v119-ERA GAMES AND 57.8% NOW, AND REACH — NOT MAP, NOT SEAT — IS WHAT SEPARATES OUR 4-1 FROM OUR 1-4** *(candidate NEW row)*
**MEASURED** §3.4 and §4.3. 109/110 → 26/45, difference 41.3pp against a
two-fixture half-width of 13.6pp. Within the *same* their-version/our-version/
seat triple, reach 5/5 → 4-1 and reach 2/5 → 1-4.
**Anchors (≥2, file + round):**
`9eb06ea6-cbbe-4e49-8806-cc7cad7ff692_game_2` (frostgate, seat A, **won at
r90**) against `9d9d2905-b104-465a-b650-d9ca32ce753a_game_3` (frostgate, seat A,
**lost at r272**) — same map, same seat, same both-versions, opposite reach ·
`117beb31-…_game_3` (royale, **lost at r92 with zero damage ever put on their
core**) and `9d9d2905-…_game_5` (icefloe, **r1000, zero damage on their core**).
**MEASURED: 19 of 45 POOL games end with our total damage into their core =
exactly 0.**
**Control that could have run the other way:** the identical measurement on the
v119 era returns 1 of 110 — the instrument is not simply reporting "cores are
hard to reach".
**Sketch vs doctrine (<r300 kill):** this IS the r300 bar. Our timely-kill rate
against them fell **47.3% → 13.3%**. Any plank here is offence, not defence, so
`DEFENCE_ADMISSION_BAR` does not bind.
⚠ **Admission caveat:** the row must be phrased as *"diagnose and restore
reach"*, not *"restore v161"* — §5.1 shows the v161-vs-v162 attribution is
un-decidable on games, and §5.2 shows the obvious mechanism (leap15) is mostly
still shipped.

### P2 — ⭐ **THEIR FIRST SENTINEL IS NOW A HOME SENTINEL AT r11 — 20 ROUNDS EARLIER THAN v119 — AND OUR RAID STILL ARRIVES AT r38** *(candidate NEW row; #41's premise, other side of the board)*
**MEASURED:** their first sentinel **median r11, d²=16 from their own core,
≤r20 in 27/45 games** (v119: r31 / d²=25 / 38 of 110). Meanwhile **our first forward
sentinel in range of their core lands median r38.5 across the POOL, in only
32 of 45 games** (`corpus/builds.tsv`, side FORWARD, d²≤32; v119 era: **r45.0
in 106 of 110**). **⇒ their guard now precedes our raid by ~27 rounds where it
used to precede it by ~14, and our raid stopped arriving at all in 13 of 45
games.** *(The gap widened from BOTH ends: their plant moved 20 rounds earlier,
ours 6 rounds earlier.)* **Our forward builds at r≤40 within d²≤40 of
their core: 270 built, 97 killed, median life OF THE KILLED 8 rounds** — against
**14.5 rounds in the v119 era** on the same instrument.
**Anchors:** frostgate **r5 @ (14,8), d²_own=5** in `a7f87ff6…_game_2`,
`b30092b8…_game_2`, `63b785aa…_game_2`, `9d9d2905…_game_3`, `9eb06ea6…_game_2`
(five games, their v126/v139/v141) · midgard **r11 @ (1,5), d²_own=10** in
`7cb5f911…_game_1` and `c24dad0e…_game_4`.
**Control:** the same measurement on THEIR gunners returns median first-build
r45–143 and 2.33/game — the early-plant behaviour is specific to the sentinel,
not a general "they build early" artefact.
**GREP against the incumbent (`bots/_v488beltbreak2/raid.py:684`
`_try_forward_sentinel`):** the siting loop asks only `can_fire_from(...)` and
`can_build_sentinel(...)`. **There is no minimum stand-off, no check whether the
candidate tile is already covered by an enemy sentinel's line, and no adjacent-
tile denial** — exactly #41's proposal, still unbuilt. **This piece supplies the
missing precondition #41 never had: a named opponent who plants the covering
turret BEFORE we arrive, at a scripted round.**

### P3 — **THEY HAVE COPIED THE CORE-RING BARRIER SEAL — 0.7/game → 9.4/game — AND IT IS AN ACCESSORY, NOT A WEAPON** *(⛔ MECHANISM REFUTED TWICE; banked as intelligence + a self-audit)*
**MEASURED, POOL:** their builds at **d²≤8 of OUR core = 421 (9.4/game), of
which 415 are BARRIERS**, present in 37 of 45 games, **median round r192**
(v119 era: 81 total, 0.7/game, in 28 of 110). Distance histogram
`{1:51, 2:174, 4:86, 5:102, 8:8}`. **We do the same to them (`LOKI_BARRIER_SEAL_ON`,
`bots/_v488beltbreak2/doctrine.py:1227`, 15.8 ring builds/game).**
⛔ **REFUTED MECHANISM 1 — SPAWN DENIAL. MEASURED:** on the 20 POOL games with
≥4 of their ring barriers and a clean ±60-round window, **our builder-spawn rate
per 100 rounds is 0.0 before and 0.0 after; it fell in 2 of 20.** Cause: their
4th ring barrier lands at median r192 and **our last builder spawn is at median
r190** — the seal arrives after our core has stopped spawning anyway.
**Placebo (16 games with <4 ring barriers, random pseudo-event): 1.7 → 0.0,
fell in 8 of 16 — i.e. the "drop" is the game clock, not the barriers.**
⛔ **REFUTED MECHANISM 2 — HEAL DENIAL. MEASURED:** our core's healed HP per 100
rounds is **39 (their ring ≥4, n=26) vs 43 (<4, n=19)** — no effect.
**Retained so nobody re-derives either.** What it IS: evidence that this
opponent reads and copies field behaviour (their team name literally ends *"och
oss"* — "and us"), which is a **#95 archetype-classification** datapoint and a
reason to expect our own signature moves back at us.

### P4 — **#101's BAD-MAP-SIX METHOD DOES NOT TRANSPORT TO THIS OPPONENT — MEASURED, so nobody spends a session finding out** *(boundary on an existing row)*
**MEASURED** §4.1–4.2: POOL (map,seat) unanimity **54.5% vs a 50.0% null,
p = 0.322**; v119-trained map class transfers at **26.3% GOOD vs 10.5% BAD**.
The team-lazy cell is near-deterministic (69.6% vs 29.6%, p=0.0000) and
cross-validates in both directions; **this cell is not, in the current pool.**
**Control:** the same test on this opponent's v119 era returns p = 0.0000 — so
the method works and the answer is "no structure *here, now*", not "the method
failed". **Consequence for #101: its one-game regression-test trick is
opponent-specific and must not be generalised to a per-map arm across the
field.**

### P5 — **#59 IS DEAD IN THIS CELL AND #97's PRECONDITION FAILS** *(checked, so nobody spends a leg)*
**MEASURED, POOL:** **they built 0 launchers in 45 of 45 games and 0 splitters
in 215 of 215**; `corpus/throws.tsv` records **0 throws by their side**. **#59
(enemy launcher pickup envelope) buys nothing here.**
**#97 (Flotte builder cull):** their builder spawns are **median 5/game with a
last spawn at median r64**, and they lose **0.6 builders/game** — they neither
cap hard at 4 nor sit un-replaced. **Precondition fails.**
**#79 (plant-and-guard infiltrator):** they build **2.33 gunners + 6.56
sentinels per game**; a dormant infiltrator has a counter here. **Precondition
fails.**

### P6 — **THEY OUT-CONVERT US 2.4:1 ON AMMUNITION AND WE DO NOT** *(diagnostic; feeds #92/#71, not a new row)*
**MEASURED, POOL:** titanium converted to ammunition, **THEM 1,078/game vs US
453/game** (v119 era: 1,275 vs 703). Their sentinel fires 10 ammo/shot; 1,078 Ti
buys ~108 sentinel shots = 1,944 HP, comfortably four cores. **Ours buys ~45.**
This is the same shape the Flotte study found (they out-convert us 5–9×) and the
same shape team lazy shows (816 vs 331). **Three independent opponents, one
asymmetry: we under-fund the only weapon that damages a core.** Grep: our
`AMMO_FLOOR = 16` (`bots/_v488beltbreak2/doctrine.py:963`) is one sentinel shot.

---

## 7. Q5 — PRICING

**All figures MEASURED off `corpus/league_matches.tsv`, both ratings read at the
same clock — the 2026-08-20T21:12:59.641Z pairing.**

**Us (OpenSverige) 1845.4 at v168 · kladde 1853.0 at v136 · gap +7.6 (they are
now ABOVE us).** With `delta = 32 × (S − E)` and `E = 0.489`:

| result | pays |
|---|---|
| 5-0 | **+16.35** |
| 4-1 | +9.95 |
| 3-2 | +3.55 |
| 2-3 | −2.85 |
| 1-4 | −9.25 |
| 0-5 | −15.65 |
| **our current-regime 24.4% share** | **−7.83 per match** |
| our v119-era 52.7% share | +1.22 per match |
| all-time 42.3% (91/215) | −2.10 per match |

**Break-even is a 48.9% game share. We sit at 24.4% [9.8, 39.1] — the upper
bound of the interval is still below break-even.**

**And the exposure is large and rising.** MEASURED, our rated matches per day
against them: **08-13 1/72 · 08-14 2 · 08-15 2 · 08-16 9 · 08-17 9 · 08-18 3 ·
08-19 4 · 08-20 5 of 64 (7.8%).** At today's rate and today's share this cell
alone costs **≈ −39 Elo/day**, and it delivered **−32.05 today** and
**−76.15 across the nine post-break matches.**

**Where the deficit lives — and the answer is "nowhere in particular", which is
itself the finding.** Not maps (§4.2: no transferable class, p=0.322 on
unanimity). Not seat (§4.4: n=15 on seat B, and no seat effect in the 110-game
era). Not one of their versions (per-version shares: v125 0/5, v126 2/10, v139
2/5, v140 1/10, v141 6/15 — all bad, all overlapping). **It lives in the reach
binary of §3.4, which is uniform across every cut I could take.** Break-even
needs **+24.5pp = ~11 more games of 45**; §3.4 says the 19 zero-damage games are
where they are.

---

## 8. REFUTED AND RETAINED

1. ⛔ **Their core-ring barrier seal denies our spawns** — REFUTED, §6/P3, with
   a placebo that reproduces the apparent "drop".
2. ⛔ **Their core-ring barrier seal denies our core healing** — REFUTED, 39 vs
   43 HP/100r.
3. ⛔ **`v144` exists / today was four matches / today was 6-19** — all three
   false, §1.
4. ⛔ **"Our v162+ lacks the leap15 kladde fixes"** — false as worded: 3 of the
   4 leap15 masters are still `True` in v162/v165/v169, §5.2.
5. ⛔ **The (map,seat) determinism found vs team lazy generalises to this
   opponent** — refuted in the current pool (p=0.322) while the same instrument
   fires at p=0.0000 on their v119 era, §4.1.
6. ⛔ **Today's 4-1 is a map or seat draw** — refuted three ways, §4.3;
   leave-one-out map prediction ANTI-predicts it.
7. ⛔ **A substring filter on `sverige` selects our team** — it pools three
   teams and inflates our match count against kladde from 43 to 71, §0/C.

---

## 9. LEDGER ROW (for `move-mining-ledger.tsv`)

```
2026-08-20	kladde chatte tville (och oss)	125	5	docs/research/REPLAY-STUDY-kladde-multiver-2026-08-20.md
2026-08-20	kladde chatte tville (och oss)	126	10	docs/research/REPLAY-STUDY-kladde-multiver-2026-08-20.md
2026-08-20	kladde chatte tville (och oss)	139	5	docs/research/REPLAY-STUDY-kladde-multiver-2026-08-20.md
2026-08-20	kladde chatte tville (och oss)	140	10	docs/research/REPLAY-STUDY-kladde-multiver-2026-08-20.md
2026-08-20	kladde chatte tville (och oss)	141	15	docs/research/REPLAY-STUDY-kladde-multiver-2026-08-20.md
```

*(One row per pooled version, cumulative semantics; `games_covered` sums to the
45-game pool. Their v119 (110 games) is deliberately NOT claimed as covered by
this study — §2 shows it is a different bot, and its own study is
`REPLAY-STUDY-kladde-v119-2026-08-17.md`. **Their currently ACTIVE v136 has 0
decoded games and remains UNCOVERED.**)*

---

## COMMISSIONER'S AMENDMENT — 2026-08-20 ~22:2xZ, research s52 (same session)

The §7 refutation "**v144 does not exist**" is SNAPSHOT-SCOPED and needs its boundary stated: it is true of `corpus/league_matches.tsv` as synced 19:39Z (timeline through v136). Verified off the primary (`fcode match list`, match `95aa5d69`, engine-side field): **kladde's 21:52:59Z match vs us carries `teamBVersion = 144`** — they shipped again after the snapshot. Day sequence is therefore v140→v141→v142→v136→**v144**, and the study's uncovered-active caveat extends to v144 (0 decoded games). The premise correction the agent made (we met only v140/v141 in DECODED games) stands.

## COMMISSIONER'S AMENDMENT 2 — 2026-08-21 s52: "REACH" MEANS DAMAGE, NOT ARRIVAL

The field-debut read (`FIELD-DEBUT-v174-2026-08-21.md`, 25 rated games) corrects this study's mechanism WORDING while confirming its numbers: raiders ARRIVE at d²≤2 of the enemy core in 25/25 field games including every zero-damage game — the collapse this study measured (19/45 games with zero core damage) is an ARRIVAL→CONVERSION failure (builder core-damage 0 HP in 25/25; first siege sentinel r67+ vs their home guard r9), not a transit/navigation failure. §3.4's causal framing should be read through this amendment. The zero-damage rate itself reproduces in the field (kladde cell: reach 3/5 vs 26/45 pre-plank).
