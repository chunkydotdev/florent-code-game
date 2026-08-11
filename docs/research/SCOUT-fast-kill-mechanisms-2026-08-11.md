# SCOUT — what produces a FAST core kill in this league, and do we have it

Side lane, 2026-08-11T08:31:01Z (`date -u`), repo at `3907373`. READ-ONLY commission:
no bot edits, no arena, no unrated/test matches. **No verdict is issued here and no
road is closed** — this is archive statistics, and under the standing rule
(`CLAUDE.md` point 6) archive statistics may PRIORITISE a road but may not RETIRE
one. Everything below is a mechanism with evidence, ranked.

Currency this aims at: `PRIMARY_CURRENCY: kill_speed_score`, `KILL_WINDOW_RND: 250`,
`R1000_IS_DEFEAT: yes`, `PLAY_DEFENCE: never`.

---

## 1. Sampling, coverage, feasibility

**Kill round turned out to be recoverable for the whole archive without decoding
anything.** `corpus/events.tsv` already carries round-stamped `DEATH core` rows
across 17,946 distinct replay files (2.83 M event rows). That made the expensive
plan — decode thousands of `.replay26` — unnecessary for the headline distribution,
and left the decode budget for one targeted question (§6).

| step | n |
|---|---|
| `corpus/meta_join.tsv` rows | 17,588 |
| distinct files in `corpus/events.tsv` | 17,946 |
| files with a `DEATH core` event | 13,705 (1 death: 13,677; 2: 27; 3: 1) |
| games joined to a winner + valid `game_winner_side` | **17,106** |
| — of which THIRD-PARTY (`us_side == none`) | **12,123** |
| — of which OURS (all versions, rated + unrated pooled) | **4,983** |
| league teams with ≥ 80 game-sides (the team-level population) | **71** |
| replays decoded for the melee question (§6) | 934 rows / 930 files, 0 missing, 0 unparseable |

### 1.1 Seat mapping — a trap that would have silently randomised everything

`events.tsv.team` is the **raw wire team index 0/1**; `meta_join.game_winner_side`
is `a`/`b`. **These do not correspond globally** — testing "wire 0 == side a" gives
7,075 agree / 6,338 disagree, i.e. a coinflip, because seats swap between games of
a match. Anything joined on a naive mapping would be noise wearing a result's
costume.

Resolved per-file by anchoring on `corpus/builds.tsv.winner`, which is stated in the
**same wire index** as `events.tsv.team`.

### 1.2 Instrument validation (both directions, as required)

* **Positive/consistency.** The dead core's team must be `1 − winner`:
  **13,660 ok, 3 bad, 14 no-winner.**
* **Negative control on an independent table.** `corpus/throws.tsv` carries `wincond`
  and `rounds` from a separate decoder. Over its 8,235 files:
  `core_destroyed` & has-core-death = 6,717; **not-`core_destroyed` & NO core-death
  = 1,505**; discordant = 13 (0.16%). The detector fires and refuses to fire in the
  right places — a "no core death" is a real tiebreak, not a decoder gap.
* **Round calibration.** `rounds − kill_round`: median 1, p95 1, **max 1** (n=6,706).
  The game ends the round after the core dies, exactly. Kill round is not an estimate.

---

## 2. The kill-round distribution

**Per game.** "Fast" = the winner destroyed a core inside r250 (`KILL_WINDOW_RND`).

| | third-party (n=12,123) | ours, all versions (n=4,983) |
|---|---|---|
| core kill | 75.7% | 85.2% |
| **r1000 tiebreak (= defeat)** | **24.3%** | **14.8%** |
| median kill round | 214 | 179 |
| **kill inside r250, as % of all games** | **44.3%** | **57.3%** |
| kill < r100 | 10.6% | 14.1% |
| r100–149 | 12.4% | 19.6% |
| r150–249 | 21.3% | 23.6% |
| r250–399 | 15.9% | 15.6% |
| r400+ | 15.5% | 12.4% |

Read carefully: the "ours" column pools **both sides of our games and every version
including deliberately crippled probes**, so it flatters nothing but also measures
nothing shippable. The clean read is per-version off `ladder_games.tsv` (rated only,
`cond`/`turns` authoritative there):

| ourver | n | kill% | **kill <250 %** | kill <150 % | median kill |
|---|---|---|---|---|---|
| 104 | 425 | 52.7 | **40.7** | 19.5 | 176 |
| 102 | 390 | 50.0 | 37.2 | 19.7 | 167 |
| 92 (incumbent) | 80 | 35.0 | 27.5 | 12.5 | 174 |
| 80 | 315 | 27.9 | 19.4 | 15.2 | 130 |
| 20 | 110 | 0.0 | 0.0 | 0.0 | — |
| **ALL rated** | **3,670** | **35.0** | **26.1** | **15.9** | **162** |

v104 at 40.7% fast-kill-per-game would sit ~7th of the 71 league teams. Good, not top.

### 2.1 Who kills fast and repeatedly (per-team, per game-side, n ≥ 40)

The interesting shape is **bimodality**: teams that either kill very early or do not
kill at all. Median kill round is the tell.

| team | n | fast<250 per game-side | median kill round | of fast kills, <150 |
|---|---|---|---|---|
| Cookie | 197 | 58.4% | **88** | 107/115 |
| Orizon | 205 | 49.8% | 103 | 80/102 |
| Pantheon | 580 | 43.3% | 201 | 100/251 |
| sporks | 492 | 42.9% | 202 | 98/211 |
| **The Bisons** | 230 | 42.2% | **74** | **94/97** |
| **Banminary** | 300 | 35.0% | **59** | **103/105** |
| Team 48 | 240 | 36.7% | 84 | 74/88 |
| SingleCore | 160 | 29.4% | 83 | 46/47 |
| gsxWins | 250 | 36.0% | 99 | 83/90 |
| Powered by SmartFridge | 1,410 | 33.9% | 144 | 324/478 |
| *(floor)* Kleos / vjg / TKB / Bean counters | 158–298 | 0–1.8% | 509 / — | — |

Banminary's median kill is **round 59** over 105 kills; The Bisons' is **74** over 97.
These are not one-offs, and they are not top-rated teams — exactly the "trick separable
from general strength" the commission asked for.

---

## 3. What precedes a fast kill

Feature window: **the first 40 rounds** (`r0–39`). Chosen because "builds by r100"
is mechanically truncated in a game that ends at r74 — a confound that would
manufacture the finding. With FAST defined as kill ≥ r50, every game in both arms
observed all 40 rounds.

Pooled, third-party, from the **killer's** side:

| feature @r40 | FAST (kill 50–149) | MID (150–249) | SLOW (250+) | **TIEBREAK** |
|---|---|---|---|---|
| n | 2,675 | 2,583 | 3,811 | 5,880 |
| reached enemy half | **0.82** | 0.72 | 0.65 | **0.41** |
| min d² to enemy core | **36.4** | 49.1 | 62.0 | **108.8** |
| forward builds | **2.52** | 2.28 | 1.80 | **1.08** |
| total builds | 22.6 | 26.0 | 24.5 | 26.1 |
| first sentinel (median rnd) | **24** | 50 | 63 | 42 |

**Total build volume is flat and slightly INVERTED.** The mechanism is not "build
more". It is *where* the early builds go.

---

## 4. Controls

### 4.1 Within-team (controls team strength) and within-matchup (controls opponent)

Sign test over strata; each stratum is one team (or one team×opponent pairing)
contributing its own mean difference.

| feature @r40 | FAST vs TIEBREAK, within-team (47 strata) | FAST vs TIEBREAK, within-team×opponent (71 strata) | FAST vs SLOW, within-team (44 strata) |
|---|---|---|---|
| reached enemy half | +0.12, 36/47, **p=0.0003** | +0.19, 43/71, p=0.096 | +0.06, 32/44, **p=0.0037** |
| min d² to enemy core | −28.5, 7/47, **p<0.0001** | −37.6, 20/71, **p=0.0003** | −12.9, 12/44, **p=0.0037** |
| forward builds | +0.57, 39/47, **p<0.0001** | +0.64, 52/71, **p=0.0001** | +0.33, 33/44, **p=0.0013** |
| forward **turrets** | 1.64 vs 0.82, 38/47, **p<0.0001** | 1.82 vs 1.14, 49/71, **p=0.0018** | 1.68 vs 1.03, 32/44, **p=0.0037** |
| sentinels (count) | 26/47, p=0.56 | 32/71, p=0.48 | 21/44, p=0.88 |
| gunners (count) | 23/47, p=1.00 | 32/71, p=0.48 | 19/44, p=0.45 |
| launchers (count) | 9/47, **p<0.0001 (INVERTED)** | 10/71, **p<0.0001 (INVERTED)** | 11/44, **p=0.0013 (INVERTED)** |

**Turret COUNT does not separate; turret SITING does.** That distinction is the whole finding.

### 4.2 The negative case (r1000 games)

Done throughout as the TIEBREAK column — it is the widest-separating arm on every
forward feature and the flattest on build volume.

### 4.3 Reverse causality — is forward presence a CONSEQUENCE of the enemy collapsing?

Tested by pushing the window back to **r30** and the kill to **r100–199** (≥70 rounds
of separation), and by measuring the **opponent's** losses inside the window:

* opponent losses by r30, FAST vs TIEBREAK: 0.91 vs 0.81, 29/54 strata, **p=0.68 (flat)**.
* opponent losses by r30, FAST vs SLOW: 0.75 vs 0.97 — **LOWER in fast games, p=0.0005.**

Fast kills do not follow an opponent already crumbling; if anything less early damage
had happened. This is the strongest available anti-reverse-causality control short of
a live leg. **Caveat, stated honestly:** at the r30 horizon the FAST-vs-SLOW separation
on `fwd` weakens to p=0.40 (it holds vs TIEBREAK, p=0.020). The fast/slow discriminant
lives largely in the r30–r40 band. **The finding is about a narrow window and should
not be quoted as "the first 30 rounds".**

### 4.4 Cross-team dose-response, and the confounds that could have killed it

Team-level, teams with ≥ 80 game-sides (**n = 71 teams**), Spearman against
fast-kill (<150) rate:

| feature @r40 | ρ |
|---|---|
| **forward TURRET fraction** | **+0.784** |
| forward turret count | +0.757 |
| forward-build fraction (any kind) | +0.723 |
| min d² to enemy core | −0.653 |
| sentinels (count) | +0.448 |
| total builds | −0.415 |
| conveyors | −0.395 |
| builder bots | −0.407 |
| gunners (count) | +0.045 |
| **launchers** | **+0.031** |

Partials:

```
fast ~ fwd_turret_frac | fwd_build_frac  = +0.452     <- turret siting dominates
fast ~ fwd_build_frac  | fwd_turret_frac = +0.124        generic forward building
fast ~ fwd_build_frac  | team rating     = +0.685
fast ~ fwd_build_frac  | total builds    = +0.682     <- not a denominator artefact
fast ~ fwd_build_frac  | win rate        = +0.718
fast ~ team rating     | fwd_build_frac  = +0.061     <- rating adds ~nothing on top
```

2×2 on team medians (mean fast-kill rate, [teams]):

| | few early builds | many early builds |
|---|---|---|
| **high forward fraction** | **22.4%** [23] | 12.0% [12] |
| low forward fraction | 4.7% [13] | 5.6% [23] |

A ~4x effect on the forward axis, with a second, smaller effect from *not* spending
the opening on a large conveyor lattice.

---

## 5. The composition finding — guns, not walls

`forward fraction` alone would have been a misleading headline. Breaking the forward
builds down by kind changes the mechanism's meaning entirely:

| forward builds @r40, composition | fwd/game | conveyor | **gunner** | **sentinel** | barrier |
|---|---|---|---|---|---|
| third-party FAST killer (<150) | 2.53 | 13.9% | **41.5%** | **22.7%** | 16.3% |
| third-party SLOW killer (250+) | 1.80 | 16.6% | 36.0% | 11.6% | 28.7% |
| third-party TIEBREAK | 1.08 | 38.1% | 27.6% | 11.0% | 10.1% |
| **US, v104** | 2.62 | 2.7% | **0.3%** | **12.8%** | **81.1%** |
| US, v92 | 0.90 | 18.1% | 21.0% | 57.1% | 0.0% |

The extreme fast-kill teams are each nearly **pure on one turret type, forward**:

```
Cookie                      1.75 fwd/game  100.0% sentinel      fast-kill 54%
Orizon                      3.81 fwd/game  100.0% gunner        fast-kill 39%
Prompt Engineers Anonymous  2.84 fwd/game  100.0% gunner        fast-kill 31%
Team 48                     3.39 fwd/game   96.8% gunner        fast-kill 31%
Banminary                   2.37 fwd/game   86.5% sentinel      fast-kill 34%
The Bisons                  1.66 fwd/game   76.3% sentinel      fast-kill 42% (<250)
```

**And the league supplies its own out-of-sample control.** Two teams have a *high*
forward fraction but a *barrier-heavy* composition — the same profile as ours:

```
HTTP 418    fwdfrac 0.148, 3.86 fwd/game, 48.1% barrier   ->  fast-kill  4.5%
not adgato  fwdfrac 0.146, 3.86 fwd/game, 58.7% barrier   ->  fast-kill  8.8%
```

They sit at the top of the forward-volume table and near the bottom of the fast-kill
table. Composition, not volume, predicts them — and it independently predicts us.

**Independent confirmation on a different table with a different `FORWARD` definition.**
`corpus/builds.tsv` carries a HOME/FORWARD label for turrets over the whole game:

| turret siting, whole game | gunner FORWARD | sentinel FORWARD | launcher FORWARD |
|---|---|---|---|
| third-party FAST killer | **79.3%** (2.64/g) | **81.3%** (1.41/g) | 17.7% (0.37/g) |
| third-party TIEBREAK | 32.4% (**8.14/g**) | 36.8% (1.49/g) | 26.8% (0.55/g) |
| **US (all versions)** | 38.1% (1.30/g) | 57.4% (3.33/g) | 4.1% (0.96/g) |

Note the tiebreak row builds **three times as many gunners as the fast killers** and
sites a third of them forward. Volume up, forward share down, kills gone.

---

## 6. Ruling out the alternative mechanism (delegated decode)

The Bisons kill at median r74 while showing **no** forward-build advantage at r30 —
the shape of a decoder gap, since the event table sees `BUILD`/`DEATH` only and is
blind to builder-bot melee and movement. Delegated a generic third-party
`builderAttack` decode (930 replays, adapted from `tools/peck_read.py`, which is
hardwired to our team id).

Validation reported back: `PECK_READ_SELFTEST: PASS`; the new decoder's own selftest
23/23 with a **mutation test** (widening the core footprint to the visualiser's 3×3
superset flipped it to FAIL, so the selftest can produce the other verdict);
real-replay controls — own-footprint friendly fire **0/200** as required, enemy-core
pecks nonzero in **21/200**; 0 missing files, 0 unresolved attacker attributions.

| bucket | mean core pecks | median | share ≥1 peck | median first peck |
|---|---|---|---|---|
| FAST | 5.00 | **0** | 14.2% | r40 |
| SLOW | 26.76 | **0** | 19.3% | r172 |
| TIE | 52.72 | **0** | 11.8% | r81 |

**Melee is not the population mechanism** — the median game in every bucket has zero,
and FAST is if anything lower than SLOW (the means track exposure time, not aggression).
For the two named teams it is refuted outright: **The Bisons 0 core pecks in 41/41
games, Cookie 0 in 70/70**; a spot-checked Bisons 62-round `core_destroyed` win shows
4 sentinels from r31 and zero builder attacks all game. Their fast kills are
turret-delivered.

**But it is a real minority mechanism for some teams**: `diverge` 19/20 of its FAST
games have ≥1 core peck, `SingleCore` 5/11, `gsxWins` 6/17 — while
`Prompt Engineers Anonymous`, `Team 48`, `Banminary`, `Pantheon`, `Orizon` and
`Powered by SmartFridge` read 0%. Two distinct fast-kill families exist.

---

## 7. RANKED MECHANISMS — and whether we have them

Ranked by (a) effect on kill round, (b) independent teams showing it, (c) do we have it.

### 1. A forward turret in the enemy half, placed by ~round 20-25 — **WE LARGELY LACK IT**

Strongest measured correlate of fast kills anywhere in this corpus.
ρ = **+0.784** across 71 teams; dominates generic forward building
(partial +0.452 vs +0.124); within-team **p<0.0001**; within-team×opponent
**p=0.0018**; confirmed on an independent table (79–81% forward siting vs 32–37%).
Shown by **at least 8 independent teams** with distinct implementations (pure-gunner:
Orizon, Team 48, Prompt Engineers Anonymous; pure-sentinel: Cookie, Banminary,
The Bisons).

The timing gap is the sharpest single statement of where we stand — **first forward
turret**:

```
league FAST killers   median r23   72.8% have one by r40   96.2% ever
league SLOW killers   median r40   47.7% by r40            96.1% ever
league TIEBREAK       median r43   22.1% by r40            46.0% ever
Cookie                median r14   81.3% by r40
Banminary             median r16   93.2% by r40
Orizon / PEA          median r19   98.8% by r40
--------------------------------------------------------------------
US v104               median r49   34.0% by r40            84.3% ever
US v107               median r73   14.8% by r40            80.9% ever
US v92                median r22   54.7% by r40            71.8% ever
```

We build forward turrets in most games — **26 rounds later than the fast-kill field**,
and by r40 we are below even the league's SLOW-killer profile. Forward turrets per
game by r40: **us 0.34–0.44, league fast killers 1.62, league tiebreakers 0.42.**
On this axis our current bot is at the league's *tiebreak* level.

### 2. Forward composition: guns rather than walls — **WE HAVE THE INVERSE**

Fast killers' forward builds are 64% turrets / 16% barrier. **v104's are 81% barrier
/ 13% turret.** The only two league teams with our composition (HTTP 418, not adgato)
have top-decile forward volume and bottom-decile fast kills. This is a composition
difference, not an effort difference: v104 already puts **2.62 forward builds/game**
down, more than the fast-kill field's 2.53 — they are just almost all barriers.
Independently visible: our gunners are 38.1% forward at 1.30/game, against 79.3% at
2.64/game.

### 3. Small early build budget, not a conveyor lattice — **WE DO NOT HAVE IT**

ρ(total builds) = −0.415, ρ(conveyors) = −0.395; partial on forward fraction −0.267.
2×2: high-forward × low-build = 22.4% fast vs high-forward × high-build = 12.0%.
Cookie (6.7 builds by r40) and Prompt Engineers Anonymous (7.9) are the two lowest and
two of the highest fast-kill rates. **Our v104 sits at 23.7, the league median (23.4).**
Weakest of the three and partly collinear with #1.

### Also measured, reported because it is load-bearing elsewhere

**Early sentinel TIMING — we already have it, and it is not the lever.** First
sentinel median r23 in fast kills vs r42 in tiebreaks; cross-team ρ=+0.448. But
sentinel *count* fails every within-team test (p=0.88 / 0.56), so it is a team-level
trait rather than a within-team lever, and its cross-team signal is plausibly the
siting effect wearing a timing costume. v104's first sentinel is median **r23 in 96%**
of games — league-leading. **We have the timing and lack the siting.**

**Launchers show no fast-kill signal in the archive.** ρ = **+0.031** (n=71 teams);
within-team sign tests **invert** (p<0.0001 — most teams build *fewer* launchers in
their own fast games); fast killers site launchers 17.7% forward at 0.37/game, while
**we build 0.96/game at 4.1% forward** — the largest single divergence between us and
the fast-kill field. **THIS IS NOT A REFUTATION OF THE KIDNAP LINE AND MUST NOT BE
QUOTED AS ONE.** It is archive statistics over other teams' launcher usage, which is
not LOKI-14's mechanism; under `CLAUDE.md` point 6 only a live leg can close that
road. What it does say is that *the league's fast kills are not currently being
delivered by launchers by anyone*, which is a prioritisation datum.

---

## 8. LIMITS — and the biggest threat to the finding

1. **⛔ OUR OWN VERSION HISTORY POINTS THE OTHER WAY. This is the strongest
   disconfirming evidence in the document and it is ours.**

   ```
   ver   n     fwd turrets/g @r40   fwd barriers/g @r40   fast-kill <150 %
   92    117          0.70                 0.00                 11.1
   104  1610          0.34                 2.12                 22.3
   107   115          0.15                 2.14                 31.3
   ```

   Our fast-kill rate roughly **tripled** while forward turrets by r40 **fell by
   more than half** and barriers went 0 → 2.1. v107 has our *worst* forward-turret
   number and our *best* fast-kill rate. If mechanism #1 were the dominant causal
   channel for us, this should not look like this. Competing readings, none settled
   here: the forward-barrier plank may deliver the same tempo by a different channel;
   the v102+ generation may have improved for reasons orthogonal to siting; or the
   league-wide correlation may not transfer to our chassis. **A leg aimed at
   mechanism #1 must carry this table in its prereg and treat it as the falsifier's
   home ground.** n for v107 is 115 and for v92 is 117 — both small, and each is a
   different opponent era.

2. **Nothing here was tested in a live game.** Per `CLAUDE.md` point 6, no road is
   closed and no plank is proposed. All of §7 is a queue-ordering claim.

3. **Cross-team correlations are over 71 TEAMS, not 12,123 games.** The effective n
   for every ρ in §4.4 is 71. Within-team and within-matchup sign tests are the
   load-bearing statistics; the ρ values are descriptive.

4. **The instrument sees `BUILD` and `DEATH` only.** It is blind to builder-bot
   movement, attacks (§6 covers attacks separately for a 930-file sample only),
   heals, rotations, and turret fire. A mechanism expressed purely through movement
   would be invisible and would present exactly as The Bisons first did.

5. **The window is narrow.** The FAST-vs-SLOW separation is strong at r40 and weak
   at r30 (p=0.40). Do not restate this as "the opening 30 rounds".

6. **Opponent versions are not pinned** (`ladder_games.tsv.oppver` is null for large
   blocks; the standing warning applies). A team's fast-kill rate pools all its own
   versions across the whole archive period; "Cookie kills fast" may be one Cookie
   build among several.

7. **Our own rows pool rated with unrated**, i.e. shipped bots with prototypes —
   the documented `meta_join` hazard. Per-version numbers in §2 come from
   `ladder_games.tsv` (rated only) for that reason; the r40 feature tables in §5/§7
   necessarily use `meta_join` and inherit the pooling.

8. **Our opponent pool ≠ the league-wide pool.** Comparing v104's 40.7% against the
   per-team table in §2.1 compares two different opponent mixes.

9. **`fwdfrac` uses "closer to the enemy core than to own core"** as its half-map
   test; `builds.tsv`'s independent HOME/FORWARD label agrees directionally (§5) but
   is not the identical definition.

10. **27 files carry 2 core deaths and 1 carries 3**; these were excluded from
    per-file kill-round statistics rather than adjudicated.

---

## Reproduction

Scripts are scratchpad-only and were not committed (side-lane constraint):
`fk_master.py` (seat anchor + validation), `fk2.py` (negative control),
`fk3.py`–`fk4.py` (distributions), `fk6.py` (r30/r40 features), `fk8.py`–`fk10.py`
(within-team / within-matchup contrasts), `fk12.py`–`fk15.py` (dose-response,
partials, 2×2), `fk16.py`–`fk19.py` (composition, siting, timing), `melee_read.py`
(§6 decoder). All read `corpus/events.tsv`, `corpus/builds.tsv`,
`corpus/meta_join.tsv`, `corpus/throws.tsv`, `corpus/ladder_games.tsv` and
`replay_archive/`; none write to the repo.
