# REPLAY STUDY — team **O(1)**, current line **v37** (2026-08-21)

**Provenance**
* **Agent:** move-mining replay-study agent, session s53, 2026-08-21. UTC clock
  from `date -u` in-shell at commission: `Fri 21 Aug 2026 15:24:50 UTC`.
* **Commission:** direct question from Magnus — *"study the team O(1), what kind
  of bot are they running?"* Team id `7419695b-3b8f-4a50-8cce-e545b086c670`.
* **Method:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` (incl. the
  in-leg mirror control) + `docs/research/corpus-howto.md`.
* **Inputs (archive-first):** `corpus/league_matches.tsv` (1,464 of their rated
  ladder matches), `corpus/meta_join.tsv` (3,285 of their archived games),
  `corpus/events.tsv`, `corpus/econ.tsv`, `corpus/throws.tsv`,
  `corpus/wincond.tsv`.
* **Live pull, read-only, noted:** `fcode match replay` for 37 match ids =
  **185 replay files** covering every completed **rated** O(1) match of
  2026-08-21 (v34, v35, v36, v37, v38) — none of which were in the archive.
  Decoded locally with the repo's own `tools/corpus/replay_events.py` and
  `replay_econ.py`. No matches fired, nothing committed but this file.
* **⚠ FIXTURE LIMIT, stated once and true of every number below:** we have
  **ZERO rated ladder games against O(1), ever** (`corpus/ladder_games.tsv` has
  no rows for them). **This is their record against the FIELD, not against us.**

---

## §1 — THE PLAIN-LANGUAGE ANSWER (read this in one minute)

**O(1) is a siege bot that wins the race to your core and then can't finish.**

Every game they open identically: three builder bots and two conveyors in the
first four rounds, first harvester on round 7 — *on the same tile every time*.
Then one or two builders walk across the map and, in **93% of games**, plant
structures on the tiles **touching your core** by about **round 50**. There they
build a wall: **six barriers ringing your core**, a handful of **gunners**, and
they start chewing — their builders melee your buildings **1.8× as often as the
field does**, and they shoot **less** than the field. That grind takes them a
**median of 228 more rounds**. Median kill round on the current line: **r266**.
They kill **nothing** before r100 and **2.7%** of games by r150.

**Three things define them, and all three are exploitable.**

1. **They do not defend their own core.** When an enemy turret is planted next
   to their core, the field answers in a median of **10 rounds**; O(1) takes
   **27** — a cluster-bootstrapped **+18-round gap (95% CI [+6, +30])**. Fewer
   than half of them ever answer at all. And when they *do* answer, **39% of
   what they build is a barrier** — a wall that cannot shoot back — against
   **4%** for the field.
2. **They have never built a launcher.** Zero in **3,465 distinct games** across
   every version we hold (v8-v38), against **2,633** built by their opponents in
   those same games. They have also never *thrown* anybody. Meanwhile their own
   builders are the most-thrown bodies in the corpus — **18.3 throws per game**
   against the field's **5.6** in the same games, the same body picked up a mean
   of **4.6 times** (max 84).
3. **They are engineering-clean and it is their name.** **Zero CPU timeouts** in
   the 185 rated games we pulled, against **3,862** for their opponents in the
   same games. They do not crash when thrown to a map border either (7,771
   border throws, 0.7% death — *lower* than their non-border rate). The
   crash-induction road is **closed** against this team. The doctrine road is
   wide open.

**And they are not a fast riser — they are a fallen bot climbing back.** They
peaked at **rating 2152 on 2026-08-19 with v28**. v29 lost them **−68.9 Elo over
93 matches** (2112 → 1982). v30 through v35 were failed patches, every one net
negative. **v37 is the recovery attempt and it is going well for them so far**
(+58.4 Elo in 14 matches, 1934 → 1980) — but at n=14 matches that is not
separable from v34 (52.9% ± 14.5pp vs 45.7% ± 14.6pp game share, rated
DEFF 1.529). The ten versions in 24 hours are a team in trouble iterating hard.

**What killed the v28 peak is visible in the decode.** v28 healed **95.4 times
per 100 game-rounds** — 2.07× the field — and leaned on **sentinels** (554 of 610
games, median r60). The current line heals **44.8** (= field parity, 1.00×) and
has swapped sentinels for **gunners**. **They removed the two planks that made
the bunker survivable and their rating fell ~180 points.**

**For us:** the bot that beats O(1) 5-0 is **not adgato v25**, which builds
**five things all game** — one builder and four sentinels planted at O(1)'s core
at r30-43 — and kills at **median r52**. That is our own doctrine. **O(1) is a
favourable pairing for a rush line, not a threat**, and their existence is
evidence *for* the builder's ranked pivot option 1 (fast-sentinel conversion) and
*against* the slow-attrition family.

---

## §2 — POPULATION, VERSION STRATA, AND THE INSTRUMENT

### 2.1 Version churn — the commissioned premise, re-derived

Their rated-ladder tape (`corpus/league_matches.tsv`, all 1,464 matches):

| ver | matches | games | game share | net Elo | Elo/match | window (UTC) | rating |
|---|---|---|---|---|---|---|---|
| v24 | 91 | 455 | 52.3% | +26.2 | +0.29 | 08-15 15:32 → 08-16 21:32 | 2046→2066 |
| v25 | 54 | 270 | 51.1% | −29.0 | −0.54 | 08-16 21:52 → 08-17 15:32 | 2066→2029 |
| v26 | 16 | 80 | 52.5% | +21.4 | +1.34 | 08-17 15:52 → 20:52 | 2033→2062 |
| v27 | 5 | 25 | 60.0% | +0.4 | +0.08 | 08-17 21:12 → 22:32 | 2057→2048 |
| **v28** | **123** | **615** | **55.4%** | **+56.9** | **+0.46** | 08-17 22:52 → 08-19 15:32 | **2055→2123 (PEAK 2152)** |
| **v29** | **93** | **465** | **47.5%** | **−68.9** | **−0.74** | 08-19 15:52 → 08-21 01:52 | **2112→1982** |
| v30 | 1 | 5 | 20.0% | −5.9 | −5.86 | 08-20 15:12 | 2086 |
| v31 | 6 | 30 | 26.7% | −35.2 | −5.86 | 08-20 21:52 → 23:32 | 2035→2009 |
| v32 | 2 | 10 | 10.0% | −21.5 | −10.73 | 08-20 23:52 → 08-21 00:32 | 2002→1993 |
| v33 | 8 | 40 | 47.5% | −0.0 | −0.00 | 08-21 00:52 → 04:12 | 1984→1990 |
| v34 | 14 | 70 | 45.7% | −20.0 | −1.43 | 08-21 04:32 → 08:52 | 1980→1971 |
| v35 | 7 | 35 | 37.1% | −29.5 | −4.21 | 08-21 09:12 → 11:12 | 1960→1930 |
| v36 | 1 | 5 | 60.0% | +3.0 | +3.01 | 08-21 11:32 | 1931 |
| **v37** | **14** | **70** | **52.9%** | **+58.4** | **+4.17** | **08-21 12:01 → 14:21** | **1934→1980** |
| v38 | 1 | 5 | 0.0% | −18.6 | −18.58 | 08-21 12:21 | 1945 |

**MEASURED.** Population: all rated ladder matches in `league_matches.tsv` with
a non-null `eloDelta`; game share = their games won ÷ games played.

**CORRECTIONS TO THE COMMISSIONING PREMISE, both MEASURED:**
* **"Fast riser" is the wrong shape.** They are **−172 from their 2152 peak of
  two days ago**. The +36 within hours is the **v37 rebound off a 1926 trough at
  12:31Z**, not a climb into new territory.
* **The version interleaving is a rated-ladder artefact of when each submission
  was live**, not concurrency: every version's rated window is **contiguous and
  non-overlapping** except the single v38 match at 12:21 sitting inside v37's
  12:01→14:21 run — i.e. **they shipped v38, lost 0-5 to not adgato, and rolled
  back to v37 within ten minutes.** The v36 match at 11:32 is the same shape.
  **INFERENCE:** they run the same submit→observe→rollback loop we do.

### 2.2 They test at enormous volume on unrated

Of 3,285 archived O(1) games, **2,835 are `triggeredBy: unrated`** across **567
distinct unrated matches**; only **450 games / 90 matches** are ladder. v28 alone
carries **565 archived unrated games**. **MEASURED** (`corpus/meta_join.tsv`,
`triggeredBy` column; cross-checked: 0 of 567 unrated match ids appear in
`league_matches.tsv`, 90 of 90 ladder ones do).
**INFERENCE:** an iteration mill like ours. Their prototypes therefore pool into
the unrated numbers — the same prototype-vs-shipped hazard the CLAUDE.md corpus
rule names. **Every headline number in §3 is given on the RATED cut where the
rated cut exists.**

### 2.3 Instrument validation — three checks, each with a group that runs the other way

1. **Team A = replay team index 0.** Predicting `wincond.tsv`'s in-replay
   `winner` from `meta_join`'s `game_winner_side`: **44,270 of 44,270 agree, 0
   disagree.** Every join below rests on this.
2. **Core-death instrument.** `corpus/wincond.tsv` covers only 1,285 of the 3,285
   O(1) files (it is stale past v22), so outcomes were re-derived from
   `events.tsv` core-`DEATH` rows. Against the 1,285 overlap:
   **1,171 of 1,171 `core_destroyed` games agree on the winner**, `turns` −
   death round is the constant **+1** in 1,171 of 1,171, and — **the control** —
   **114 of 114 non-kill games have no core-death row at all.** The instrument
   discriminates.
3. **Reconciliation against the platform.** My replay-derived v37 rated tally is
   34W/33L/3-tiebreak = 48.6%; `league_matches` scoreA/scoreB says **52.9%**. The
   gap is exactly the **3 r1000 games my instrument correctly abstains on** and
   the platform resolves by tiebreak: 34+3 = 37/70 = 52.9%. **Exact.**
4. **Known-dead columns avoided:** `econ.tsv.deliveries` is still identically 0
   (462,708 rows, sum 0 — re-verified here) and is not used. `econ.tsv.shots` IS
   now populated post-v2-rebuild (sum 20,488,051) and is used.

---

## §3 — DOCTRINE PROFILE: v37 (with the v28→v37 arc)

### 3.1 Opening build order — near-total determinism

Modal first-six-build sequence, O(1) side, archived games:

| ver | n | modal sequence | share |
|---|---|---|---|
| v37 | 40 | `builder_bot builder_bot conveyor builder_bot conveyor builder_bot` | **38/40 (95%)** |
| v38 | 30 | same | 29/30 (97%) |
| v35 | 45 | same | 42/45 (93%) |
| v34 | 35 | same | 27/35 (77%) |
| v28 | 610 | same | 522/610 (86%) |

**MEASURED.** The opening has not changed across the entire churn. Median rounds:
build #1 r0, #2 r1, #3 r1, #4 r2, #5 r2, #6 r3 — i.e. **three builder bots and two
conveyors are down by round 3.**

First-of-kind, v37 (n=40 archived):

| kind | games | median round |
|---|---|---|
| harvester | **40/40** | **r7** |
| gunner | 35/40 | r28 |
| barrier | 38/40 | r27 |
| sentinel | 24/40 | r86 |
| **launcher** | **0/40** | — |
| **splitter** | **0/40** | — |

### 3.2 Tile-level determinism — the pre-emption surface

On the 185 live-pulled rated games, maps were fingerprinted by (w, h, md5 of the
tile grid) and cells keyed by **(map, O(1)'s own core position)** so seat is held
fixed. Cells with n≥3:

| build | modal-tile share, **O(1)** | modal-tile share, **field control (same cells)** | median round |
|---|---|---|---|
| harvester #1 | **164/166 = 99%** | 115/158 = 73% | r7 |
| harvester #2 | 152/166 = 92% | — | r9 |
| harvester #3 | 141/163 = 87% | — | r12 |
| harvester #4 | 107/150 = 71% | — | r21 |
| harvester #5 | 79/121 = 65% | — | r38 |
| conveyor #5 | 118/166 = 71% | — | r9 |
| conveyor #20 | 67/148 = 45% | — | r28 |
| **first turret** | **59/161 = 37%** | 43/164 = 26% | — |

**MEASURED, with the mirror control (their opponents, identical decoder, same map
cells) reading 73% where they read 99%.** Their **economy plan is a fixed
per-map script**; their **turret siting is not** (37%).

### 3.3 Economy shape — flat, mid-sized, and not the point

Length-controlled (builds in r0-100, games lasting ≥120 rounds), maps of all
sizes, archived:

| ver | side | n | builder | conveyor | harvester | barrier | gunner | sentinel |
|---|---|---|---|---|---|---|---|---|
| v28 | O(1) | 448 | 6.16 | 29.27 | 4.87 | 7.09 | 1.31 | 0.95 |
| v28 | opp | 448 | 4.79 | 25.07 | 5.19 | 2.87 | 2.66 | 0.80 |
| v34 | O(1) | 34 | 5.97 | 26.65 | 4.62 | 6.00 | 2.85 | 0.35 |
| v35 | O(1) | 41 | 5.61 | 30.24 | 5.02 | 4.78 | 2.20 | 0.66 |
| **v37** | **O(1)** | **38** | **5.37** | **23.39** | **4.79** | **4.66** | **2.32** | **0.39** |
| v37 | opp | 38 | 5.66 | 33.50 | 4.66 | 4.45 | 2.39 | 0.63 |

**MEASURED.** **Harvester count is invariant at ~4.8 in r0-100 across every
version** — the economy plank is the one thing they have never touched. What
moved v28→v37: conveyors **−20%**, barriers **−34%**, sentinels **−59%**, gunners
**+77%**, builders **−13%**.

**They are not an economy-conversion bot.** Their r1000 rate on the rated v36+v37
cut is **4.0% (3 of 75)**; on the ladder-only archived cut it runs 0–15% by
version. They do not play for the tiebreak.

### 3.4 Ammunition and the melee habit — per 100 game-rounds

Length-normalised (divided by kill round, or by 1000 for r1000 games):

| era | side | games | heals | **attacks** | gunShots | sentShots | ammoConv | TLE |
|---|---|---|---|---|---|---|---|---|
| v28-29 | **O(1)** | 890 | **95.4** | 59.9 | 9.7 | 20.3 | 261.2 | **0.00** |
| v28-29 | field | 890 | 46.0 | 43.6 | 41.4 | 12.5 | 312.4 | 1.46 |
| v32-35 | **O(1)** | 220 | 49.7 | 84.3 | 14.6 | 12.7 | 193.0 | **0.02** |
| v32-35 | field | 220 | 52.7 | 45.5 | 21.6 | 14.7 | 240.7 | 6.90 |
| **v37-38** | **O(1)** | **70** | **44.8** | **93.6** | 14.2 | 8.9 | **154.4** | **0.00** |
| v37-38 | field | 70 | 44.6 | 53.2 | 29.4 | 11.7 | 241.5 | 0.31 |

**MEASURED** (`corpus/econ.tsv`, `heals`/`attacks`/`shots_*`/`ammo_converted`/
`tled` summed across bands per team-game).

Three readings, all MEASURED, the causal joins flagged:
* **The heal plank was deleted between v29 and v32.** 95.4 → 49.7 → 44.8 per 100
  rounds; field parity is ~45-53 throughout. At v28 they healed **2.07× the
  field**; now **1.00×**. **INFERENCE:** the barrier bunker was heal-sustained,
  and removing the sustain is what turned a 110-round conversion into a
  184-round one (§3.5).
* **Melee is rising and is their real weapon.** 59.9 → 84.3 → **93.6** attacks per
  100 rounds, against a field that sits at 43.6-53.2. At 2 dmg per attack that is
  ~187 damage per 100 rounds delivered by builders — **more than their turrets
  deliver.**
* **Ammunition spend fell 41%** (261 → 154 per 100 rounds) while the field held at
  ~240. They are converting titanium into ammunition at **64% of the field rate.**

### 3.5 Kill mechanism — arrival-first, conversion-last

**Structures the KILLER had planted within d²≤40 of the victim core, at the moment
the core died** (archived games, all map sizes):

| era | killer | n | gunner | sentinel | barrier | conveyor | median first arrival | **median siege length** | bots lost at core | **games with NO siege** |
|---|---|---|---|---|---|---|---|---|---|---|
| v28-29 | **O(1)** | 610 | 1.07 | 2.21 | 8.99 | 0.99 | r33 | **110** | 0.25 | **0.0%** |
| v28-29 | field | 255 | 4.82 | 1.96 | 5.75 | 1.70 | r29 | 211 | 0.04 | 0.0% |
| v33-38 | **O(1)** | 104 | 5.44 | 1.89 | 9.55 | 0.25 | r36 | **184** | 0.63 | **0.0%** |
| v33-38 | field | 111 | 2.55 | 2.25 | 9.32 | 3.58 | r33 | 181 | 0.42 | 0.0% |

**MEASURED. In 714 of 714 of their core kills, they had structures planted at the
victim's core first.** There is no other kill mode. **The siege is the bot.**

**Arrival — the thing they are best in the league at.** Round of their first
structure with d²≤8 of the enemy core (maps ≥18×18):

| era | side | games | arrived | p10 | median | p90 |
|---|---|---|---|---|---|---|
| v28-29 | **O(1)** | 766 | **743 (97%)** | r23 | r49 | r102 |
| v28-29 | field | 766 | 539 (70%) | r13 | r42 | r91 |
| v33-38 | **O(1)** | 180 | **167 (93%)** | r28 | r52 | r120 |
| v33-38 | field | 180 | 155 (86%) | r30 | r52 | r162 |

**They get to your core in 93% of games and convert 44% of them.** That is the
whole diagnosis in one line.

**Barrier ring at the enemy core** (maps ≥18×18, d²≤8 = the tiles touching the
2×2 footprint):

| era | side | games | barriers | ring/game | **P(any ring barrier)** |
|---|---|---|---|---|---|
| v28-29 | **O(1)** | 766 | 8,222 | **6.10** | **97.0%** |
| v28-29 | field | 766 | 3,193 | 2.24 | 44.3% |
| v33-38 | **O(1)** | 180 | 1,842 | **6.24** | **90.6%** |
| v33-38 | field | 180 | 1,666 | 4.61 | 76.1% |

**MEASURED, control runs the other way.** ⚠ The field has been catching up on
this — 44.3% → 76.1% between eras. **Ring-barriering the enemy core is becoming
the league meta, not an O(1) signature.** It remains their signature in *rate*
(90.6%) and in *timing* (§3.6).

### 3.6 REFUTED HERE — the ring is not a spawn lock

**Retained so nobody re-derives it, and it bears on our own six-roads
"barrier-form spawn lock" entry.**

Seal event = the besieger's **3rd** barrier standing at d²≤8 of the victim core.
Test = victim's builder-bot spawns per round in the 30 rounds after vs the 30
before. Placebo = the same before/after at r60 in games where no seal ever forms.

| besieger | sealed n | median seal round | victim spawns/rnd before → after | **placebo (never sealed) before → after** |
|---|---|---|---|---|
| **O(1)** | 673 | r65 | 0.0087 → 0.0038 (**−56%**) | 0.0112 → 0.0074 (**−34%**) |
| field (mirror control) | 266 | r81 | 0.0138 → 0.0108 (**−22%**) | 0.0155 → 0.0171 (**+10%**) |

**The placebo does the work.** Spawn rate declines ~34% over that window with no
seal at all. Net of placebo the seal buys roughly **−22pp** (O(1) besieging) to
**−32pp** (field besieging O(1)) — **a tax, not a lock. The victim keeps
spawning.** **REFUTED: "a barrier ring at the enemy core denies spawns."** It
slows them by roughly a fifth to a third.

### 3.7 Kill-clock CDF — v36+v37 RATED (n=75 games, 15 matches, live pull)

| by round | **O(1) has killed** | **O(1)'s core is dead** |
|---|---|---|
| r100 | **0.0%** | 1.3% |
| r150 | **2.7%** | 12.0% |
| r200 | 12.0% | 18.7% |
| r250 | 22.7% | 32.0% |
| **r300** | **34.7%** | 36.0% |
| r400 | 41.3% | 41.3% |
| r500 | 46.7% | 44.0% |
| r1000 | 49.3% | 46.7% |
| **r1000 draws** | **4.0%** | |

Median kill r265 (r266 on the v37-only cut, n=70); median own-core death r228.
**DEFF-corrected half-width at
n=75, rated DEFF 1.529: ±14.0pp — quote these as shape, not as precision.**

**They are behind the clock until ~r280.** Their core dies before they kill in
every band up to r300. **INFERENCE:** the v29→v37 drawdown is a clock problem, not
a win-rate problem — on the ladder-only archived fixture, v28's median kill was
**r182** and v29's **r159**, against v37's **r266**.

Per-opponent, v36+v37 rated (n=70/14 matches — every cell is n=5 or n=10, quoted
for texture only, not as a book):

| opponent | ver | n | share | med kill | med death | deaths ≤ r150 |
|---|---|---|---|---|---|---|
| HTTP 418 | v124 | 10 | 30.0% | r217 | r136 | 3 |
| sporks | v29 | 10 | 40.0% | r273 | r174 | 3 |
| Lorem Ipsum | v48 | 10 | 40.0% | r234 | r191 | 1 |
| Pivot | v240/241 | 10 | 10.0% | r401 | r236-242 | 2 |
| ph | v82 | 5 | 40.0% | r414 | r244 | 0 |
| Leviathan | v91 | 5 | 60.0% | r300 | r386 | 0 |
| kladde | v173 | 5 | 60.0% | r232 | r392 | 0 |
| lingling_40h | v86 | 5 | 80.0% | r232 | r226 | 0 |
| Focalground | v32 | 5 | 80.0% | r206 | r182 | 0 |
| Clankers | v31 | 5 | 80.0% | r368 | — | 0 |
| The Flotte Experience | v55 | 5 | 100.0% | r249 | — | 0 |

### 3.8 Defensive verbs under pressure — the headline weakness

Siege onset = the **enemy's** first gunner/sentinel built within d²≤40 of **their**
core. Response = their first gunner/sentinel/barrier built within d²≤25 of their
**own** core after that round. Maps ≥18×18. Mirror control = identical
computation, sides swapped, same files, same decoder.

| era | side | sieged games | **P(home defence within 10r)** | **median latency (responders)** |
|---|---|---|---|---|
| v28-29 | **O(1)** | 651 | **7.7% ± 2.8pp** | **27r** |
| v28-29 | field | 729 | **20.7% ± 4.0pp** | **11r** |
| v33-38 | **O(1)** | 148 | 20.9% ± 8.9pp | **27r** |
| v33-38 | field | 156 | 32.1% ± 9.9pp | **10r** |

Intervals are DEFF-corrected at 1.833 (unrated pool). **The v28-29 proportions do
not overlap; the v33-38 proportions DO** — at n=148/156 the *rate* difference is
not resolved on the current line and I am not claiming it.

**The LATENCY difference is resolved, on both eras independently:**

```
cluster-bootstrap by MATCH, 4,000 reps, median-difference statistic
  v33-38 (current line): 42 matches, O(1) n=88 med 27r, field n=96 med 10r
                         difference +18r   95% CI [+6, +30]
  v28-29 (peak era)    : 150 matches, O(1) n=153 med 27r, field n=316 med 11r
                         difference +17r   95% CI [+7, +31]
```

**MEASURED, excludes zero, replicated on an independent era.** Their median
answer to a turret planted at their core arrives **27 rounds later** — 4 sentinels
at 18 dmg on a 2-round reload deliver ~36 dmg/round; a 500-HP core dies in ~14.

**And the composition of the answer is worse than its timing.** Kind mix of
post-siege home builds:

| era | side | mix | **barrier share** |
|---|---|---|---|
| v28-29 | **O(1)** | barrier 705, sentinel 90 | **88.7%** |
| v28-29 | field | gunner 381, sentinel 203, barrier 50 | 7.9% |
| v37-38 | **O(1)** | gunner 33, sentinel 12, barrier 29 | **39.2%** |
| v37-38 | field | gunner 62, sentinel 27, barrier 4 | 4.3% |

**They answer a siege with walls.** **CONTROL that must run the other way, and it
is already established in this repo:** a barrier plugs a **gunner** (line shot,
blocked by obstacles) and does **nothing** to a **sentinel** (`CLAUDE.md` entity
table: *"single-tile-wide line shot that ignores obstacles (unlike Gunner)"*; the
0033 study measured the plug at 1.6 vs 6.6). **So O(1)'s defensive reflex is
literally inert against the exact weapon that beat them 0-5.**

### 3.9 Launcher / throw usage — the emptiest column in the study

| measure | O(1) | field (mirror, same games) |
|---|---|---|
| launchers built, **all 3,285 archived games, every version v8-v38** | **0** | **2,335** |
| launchers built, 185 live-pulled rated games (v34-v38) | **0** | **298** |
| throws **made**, all 3,285 archived games | **0 rows** | 35,447 rows |
| throws **received**, v33-38 (61 games with throws) | **18.3 / game** | **5.6 / game** (80 games) |
| mean throws per victim body, v33-38 | **4.60** (max 84) | **1.94** (max 28) |
| mean throws per victim body, older | 14.31 (max 380) | 8.66 |

**MEASURED** (`corpus/throws.tsv`; `tteam` = thrower team index, `bteam` = body's
team index, joined through the validated A=0 mapping). **They have never thrown
anybody and they have never built the tool to.** Their builders are picked up
**3.3× as often as the field's in the same games** and re-picked-up **2.4× as
often per body** — i.e. **their pathing walks the same body back into the same
launcher, repeatedly, and nothing in their code learns.**

### 3.10 REFUTED HERE — the border-crash road is closed against O(1)

| victim | border? | throws | RETHROWN | ALIVE_END | **DIED** |
|---|---|---|---|---|---|
| O(1) | yes | **7,771** | 94.9% | 4.4% | **0.7%** |
| O(1) | no | 19,411 | 91.2% | 7.1% | 1.8% |
| field | yes | 1,303 | 96.2% | 3.7% | 0.2% |
| field | no | 6,962 | 84.0% | 14.1% | 1.9% |

**MEASURED.** O(1) bodies thrown to a map-border tile die at **0.7%**, which is
**lower** than their non-border rate of 1.8% — **the opposite of a crash
signature**, on n=7,771 border throws. Combined with **0 CPU timeouts** in the 185
rated games (against 3,862 for their opponents; 770 lifetime across all 3,285
archived games, none on the current line), **O(1) is the most exception-hardened
opponent this corpus contains. Do not spend a leg on crash-induction against
them.** The name is earned.

---

## §4 — TAXONOMY: they are a FOURTH SHAPE

**RELAYED FRAME, labelled as such and not a repo fact:** the builder's pivot
analysis (`docs/coordination.md`, 2026-08-21T15:25:15Z) groups top-ladder
doctrines into **fast-turret rush / large-economy conversion / engine-cadence**.

**O(1) fits none of the three, and forcing the fit loses the actionable part.**

| family | test | O(1) |
|---|---|---|
| fast-turret rush | kills early | **NO.** 0.0% of kills by r100, 2.7% by r150, median r266 |
| economy conversion | plays for the tiebreak cascade | **NO.** r1000 rate 4.0%; harvesters flat at 4.8/100r since v28; ammo spend 64% of field |
| engine-cadence | wins on build throughput | **NO.** 23.9 builds/100r vs field 31.2 at v37-38 — they build *less* than the field |

**PROPOSED FOURTH SHAPE — "ARRIVAL-FIRST ATTRITION SIEGE".** Its defining
signature, and each element is measured above:

1. **Arrive early, in almost every game** — structures on the tiles touching the
   enemy core in **93%** of games by median **r52** (field 86% / r52; at v28-29
   they were 97% vs the field's 70%).
2. **Wall the target, don't shoot it** — 6.2 barriers ringing the enemy core,
   1.3:1 barrier-to-turret in the siege stack.
3. **Kill with bodies, not ammunition** — 93.6 builder attacks per 100 rounds
   (1.8× field) against 23.1 turret shots (0.6× field).
4. **Spend nothing on home defence** — 0.66 home barriers and 1.03 home turrets
   per game at v37 against 6.66 and 5.59 forward.
5. **Convert slowly** — 184 median rounds from arrival to kill.

**This is a coherent doctrine, it reached 2152 with a heal-sustained
sentinel-flavoured version of itself, and the current line has broken it** by
removing the heal sustain and the sentinels. **It is a cautionary case for the
attrition family, not a template.**

**FEEDS THE PIVOT DECISION DIRECTLY:** the builder's ranked option 1 is
fast-sentinel conversion. **O(1) is the counter-example that prices it.** They
demonstrate that *arrival is cheap and conversion is everything* — they win the
race to the core more reliably than anyone in the corpus and it is worth ~1950
Elo, while the bot that arrives **later** (r30-43) with four sentinels and no
economy at all beats them **5-0**. **Arrival is not the scarce good. Delivered
damage per round at the core is.**

---

## §5 — THE ANTI-RUSH FAILURE: not adgato v25 5-0, match `7584fe46-0824-4427-a012-56d03668baf0` (12:21Z)

Not in the archive; **pulled live** (`fcode match replay`, read-only) and decoded
with `tools/corpus/replay_events.py`. O(1) is team B = replay index 1, `v38`;
not adgato is team A = index 0, `v25`. Rating 1944.9 → **−18.58**.

**All five games decoded. This is what happened, per game:**

| game | map | **not adgato TOTAL builds** | their builds at O(1)'s core | **O(1) core dies** | **O(1) home defensive builds, whole game** |
|---|---|---|---|---|---|
| 1 | 24×24 | **5** | 4 sentinels r43,44,46,48 (d²=25,37,16,9) | **r60** | **1** (gunner r29) |
| 2 | 22×22 | **5** | 4 sentinels r35,36,37,39 (d²=5,13,13,8) | **r52** | **1** (gunner r25) |
| 3 | 30×30 | **6** | 4 sentinels + 1 launcher r30-35 (d²=10-26) | **r49** | **0** |
| 4 | 20×20 | **5** | 4 sentinels r34,36,37,38 (d²=5,8,2,4) | **r57** | **2** (gunner r26, sentinel r36) |
| 5 | 24×24 | **6** | 5 sentinels r33-43 (d²=2-25) | **r48** | **0** |

**not adgato builds FIVE OR SIX THINGS ALL GAME:** one builder bot at r0, then
four or five sentinels planted at O(1)'s core between r30 and r48. No harvester,
no conveyor, no barrier, no economy. **Kill in 12-19 rounds from the first
sentinel.**

**O(1)'s behaviour after siege onset, tile by tile, is the whole answer.** Every
build they made from the moment the first enemy sentinel landed, classified by
location:

* **Game 1** (onset r43, dead r60): `r43 barrier FWD@enemy` · `r44 conveyor mid` ·
  `r46 conveyor mid` · `r46 barrier FWD@enemy` · `r48 conveyor mid` ·
  `r50 builder HOME` · `r50 conveyor HOME` · `r50 barrier FWD@enemy` ·
  `r53 barrier FWD@enemy` · `r55 builder HOME`.
* **Game 2** (onset r35, dead r52): `r36 barrier FWD` · `r37 harvester mid` ·
  `r37 barrier FWD` · then **seven consecutive conveyors r39,41,43,45,47,49,51** —
  **they extended their belt for thirteen straight rounds while their core was
  being shot down.**
* **Game 4** (onset r34, dead r57): one home sentinel at r36 — **the only
  genuinely defensive act in the entire match** — then **six more barriers, all at
  d²≤5 of not adgato's core**, r38 through r52.
* **Game 5** (onset r33, dead r48): six barriers, every one at d²=1-5 of not
  adgato's core, plus a harvester at r46 and a conveyor at r48.

**MEASURED, from the decoded event stream of all five games.** ⚠ n=5 games,
one match, one opponent version — this is the **worked mechanism**, and its
population-level backing is §3.8's +18-round latency on 42 matches.

**HOW THE TOP-HALF FAST RISER FAILS AGAINST THE RUSH CLASS — three joints, each
grounded:**

1. **The threat arrives inside their blindness window and they never look.** They
   answer a home siege in a median of 27 rounds (§3.8); not adgato kills in 12-19.
   **The race is over before their response function fires.** In 2 of 5 games it
   never fired at all.
2. **Their one home turret cannot reach the besiegers, by construction.** They
   build a **gunner** at home (r25-29, games 1/2/4), attack r²=**13**. The
   sentinels sat at d²=9, 13, 16, 25, 37 from the core. **Three of the four are
   outside gunner range before anyone moves.** Sentinel range is r²=32 — **they
   are out-ranged by a factor of 2.5 and it is a static property of the two
   entity types, not a tactical error.**
3. **Their defensive reflex is a wall, and the weapon ignores walls.** 39.2% of
   their post-siege home builds are barriers (§3.8). **Sentinel line shots ignore
   obstacles.** A barrier answer to a sentinel siege converts titanium into
   nothing at all.

**AND THE FOURTH, WHICH IS THE ONE WE SHOULD TAKE:** O(1) **arrived at not
adgato's core FIRST in 4 of the 5 games** (r24, r28, r29, r30 vs not adgato's
r30-43), and built 8-9 structures there, and still lost 0-5. **Arriving first is
worth nothing without delivered damage per round.** That is the same sentence as
§4's conclusion, arrived at from a completely different direction.

**FOR OUR ANTI-RUSH ROWS #105-108:** the anti-rush question those rows ask is
answered here from the *defender's* side. **What loses to a 4-sentinel core rush
is: a home turret chosen for cost rather than range, a defensive reflex that
builds HP instead of damage, and a response latency longer than the kill.**
Any anti-rush plank of ours that does not fix all three of those is fixing the
wrong one.

---

## §6 — EXPLOITABLE HABITS, RANKED (play-the-players)

Ranked by **expected value against this opponent** = (size of the opening) ×
(confidence in the measurement) × (whether we already have the tool).

### #1 — **THE 27-ROUND HOME BLINDNESS WINDOW** · MEASURED, CI excludes zero, replicated across eras
Their median answer to a turret planted at their core is **+18 rounds slower than
the field, 95% CI [+6, +30]** (42 matches current line; +17 [+7,+31] on 150
matches of the peak era), and **fewer than half ever answer**. Composition makes
it worse: **39% of their answer is barriers** vs the field's 4%, and barriers are
inert against sentinels.
**HOW WE TAKE IT:** plant **sentinels**, not gunners, at r²≤32 from their core —
outside their home gunner's r²=13 — and expect ~27 unanswered rounds. Four
sentinels = ~36 dmg/round = a 500-HP core in ~14. **We already ship this**
(`bots/_v542wave/main.py:1898-1931` prefers SENTINEL before GUNNER in the forward
turret choice; `bots/_v542wave/siege.py:6147-6182` plants forward sentinels;
`doctrine.py:2213` records the intent verbatim: *"that shoots the core to kill,
preferrably two sentinels"*). **This is not a new plank — it is a reason to expect
our incumbent to do well against them.**

### #2 — **THEY HAVE NO LAUNCHER AND ARE THE MOST FERRY-ABLE BODY IN THE CORPUS** · MEASURED
**0 launchers built and 0 throws made in 3,465 distinct games.** Their bodies are thrown
**18.3×/game vs the field's 5.6×** in the same games, **4.60 throws per body**
(max 84). **They cannot throw ours back and their pathing re-enters the same
launcher.**
**HOW WE TAKE IT:** our kidnap plank (`bots/_v542wave/raid.py:1415-1448`,
`siege.py:6446-6455`) is uncontested here. ⛔ **Do NOT aim it at the map border** —
§3.10 shows they do not crash (0.7% death on 7,771 border throws, *lower* than
their baseline). Aim it at **displacement value**: throw the besieging or
belt-laying body far from its plan.

### #3 — **THE ECONOMY SCRIPT IS A FIXED PER-MAP TABLE** · MEASURED
First harvester on the **same tile in 164 of 166 repeated (map, seat) games
(99%)** against a **73%** field control in the identical cells; harvesters #2/#3
at 92%/87%, at r9/r12; conveyor #5 at 71% (r9).
**HOW WE TAKE IT:** ⚠ harvesters #1-#3 land on **their** side of the map at r7-r12
and are **not reachable** by us in time — the determinism is real but the early
tiles are not a pre-emption surface. **Harvesters #4 and #5 (r21/r38, 71%/65%
modal) are the reachable ones**, and a 3 Ti barrier on an ore tile makes
`can_build_harvester` false permanently (builder-probed 2026-08-09, cited in
`tools/corpus/replay_events.py`'s own docstring). **Off-programme under
`R1000_IS_DEFEAT`** — this attacks their economy, which is instrumental, not
scoring. **Listed for completeness and ranked below the two above deliberately.**

### #4 — **THEIR FORWARD SIEGE IS SLOW AND SITS IN OUR TERRITORY FOR ~184 ROUNDS** · MEASURED
They arrive at r52 median and take 184 more rounds to convert. That is **184
rounds of their builder bodies and 6.2 barriers parked next to our core**, and
during that time they have spent ~10 forward builds and are running at 64% of the
field's ammunition rate.
**HOW WE TAKE IT:** ⚠ **This one is a hypothesis, not a finding.** It looks like a
free kill-window for a counter-attack, but our own doctrine already says
demolition **lowers their cost scale and helps them** (`CLAUDE.md` guard-matrix
sweep). Whether killing the parked siege beats ignoring it is **untested** and
would need a leg.

### #5 — **REFUTED, RETAINED: crash-induction** · MEASURED
0 CPU timeouts on the current line (185 rated games; 3,862 for their opponents in
the same games), 0.7% death rate on 7,771 border throws. **The road is closed
against this team.** Spend the leg elsewhere.

### #6 — **REFUTED, RETAINED: the barrier ring is not a spawn lock** · MEASURED with placebo
−56% raw looks decisive until the never-sealed placebo reads −34% (§3.6). Net
effect ~−22 to −32pp. **A tax, not a lock.** Bears directly on our own six-roads
"barrier-form spawn lock" entry.

### NOT AN EXPLOIT, BUT THE MOST DECISION-RELEVANT LINE IN THIS DOCUMENT
**O(1) is a favourable pairing for a rush line.** Their core is dead by r150 in
**12.0%** of their rated games and by r200 in **18.7%**, while they kill **nothing**
by r100 and **2.7%** by r150 — and the bot that swept them 5-0 does exactly what
we do, with five buildings. **We have never played them. That is the gap to
close.**

---

## §7 — QUEUE-ROW CANDIDATES (research admission gate: four parts + GREP vs `bots/_v542wave`)

**Only one candidate clears the gate. The other two are recorded as declined,
with the reason, per the playbook's "a piece that cannot name what the incumbent
currently does is not admissible yet".**

### CANDIDATE A — **ADMIT: pinned unrated calibration leg vs O(1) v37**
* **PLANK:** none — this is a *fixture* row, not a bot change.
* **MECHANISM:** we hold **zero** games against a **1980-rated team in our own
  pairing band** whose doctrine we now have a full profile of, and whose measured
  weaknesses (§6 #1, #2) map onto planks we already ship. The profile predicts we
  should beat them; **the profile is built entirely on their games against
  OTHERS** and CLAUDE.md rule 6 says a claim without live-game backing is a
  hypothesis.
* **BAR:** ≥5 pinned matches (`fcode match unrated <O(1) id> --match <a v37
  match id>`, per `docs/fcode-cli.md:330` and the s36 pinning spec) against our
  active holder. **Treatment bar:** our game share ≥ 55% AND median kill round
  ≤ r250. **Falsifier:** game share ≤ 45%, or their median home-defence latency
  against *us* measured under 15 rounds (i.e. §3.8 does not transfer).
* **GREP vs `bots/_v542wave`:** no change requested; the incumbent's relevant
  behaviours are `main.py:1898-1931` (sentinel-first forward turret),
  `siege.py:6147-6182` (forward sentinel plant), `raid.py:1415-1448` (kidnap).
  All present. **Nothing is being re-invented.**
* **COST:** free (unrated), 5 matches = one 20-minute rate-limit window.
* ⚠ **PINNING NOTE:** pin the treatment leg (`--match`), because their version
  churn is **10 versions in 24h** — an unpinned leg against this team is
  guaranteed to straddle versions.

### CANDIDATE B — **DECLINED: enemy-ore denial barrier**
Their harvesters #4/#5 are 71%/65% modal at r21/r38, and `grep` confirms the
incumbent never barriers an **enemy** ore tile (`bots/_v542wave/eco.py` reads
`Environment.ORE_TITANIUM` only for our own build siting, lines 425, 1778, 2035,
2621, 2634, 2674, 2701; `_siphon_deny` at `eco.py:2404` is about enemy conveyors
touching **our** harvesters, a different thing). **So the gap is real.**
**Declined because it is off-programme:** it attacks `titanium_collected`, which
`R1000_IS_DEFEAT` retired as currency. **File it if the tiebreak ever returns.**

### CANDIDATE C — **DECLINED: "hold the forward emplacement against non-responders"**
Tempting from §3.8, but the incumbent already sites and re-seats forward turrets
adaptively (`FS_RING_SITE_ON` at `doctrine.py:2427`, measured at 48.4% strict /
58.5% deny-mode intercept) and already models the seal's provocation cost
(`doctrine.py:2497`: *"a FULL 12-seal PROVOKES: median 9…"*). **A row that cannot
say what would change is not admissible.** Revisit after Candidate A produces
live data on whether they answer *us* the way they answer the field.

---

## §8 — LEDGER ROWS (drafted for `docs/research/move-mining-ledger.tsv`; NOT written by me)

Format read from the file header: `date  opp  oppver  games_covered  doc`.
Two rows, because the study covers the current line and the peak-era contrast on
materially different denominators.

```
2026-08-21	O(1)	34,35,36,37,38	330	docs/research/REPLAY-STUDY-o1-v37-2026-08-21.md
2026-08-21	O(1)	28,29,33	960	docs/research/REPLAY-STUDY-o1-v37-2026-08-21.md
```

**Denominators, computed not estimated:** row 1 = 185 live-pulled rated games
(v34-v38) ∪ 150 archived current-line games (v34 35 + v35 45 + v37 40 + v38 30);
**overlap by filename = 5** (v37's only archived ladder match, which the pull also
fetched) ⇒ **330 distinct games**. Row 2 = archived v28 610 + v29 280 + v33 70 =
**960 games**. **Total distinct games read for this study: 1,290.**

---

## §9 — CAVEATS, KEPT INTACT

1. **No games against us, ever.** Every behavioural number is O(1) versus the
   field. **§3.8's latency and §3.9's throw rates could both change against a bot
   that presses them differently.** Candidate A exists to close this.
2. **The archived cut pools their prototypes.** 2,835 of 3,285 archived games are
   unrated, i.e. **their test legs**. Where a rated cut exists (§2.1, §3.7, the
   per-opponent table, §3.2's determinism) it is used and labelled; where it does
   not (§3.3-§3.6, §3.8-§3.10) the number is archive-pooled and says so.
3. **n is small on the current line.** v37 rated is **70 games / 14 matches**;
   DEFF-corrected half-width at that n is **±14.0pp** on any proportion. **Two
   claims explicitly did NOT resolve and are reported as unresolved:** the
   home-defence *rate* difference at v33-38 (20.9% ± 8.9 vs 32.1% ± 9.9, CIs
   overlap) and the map-size effect (small maps 31-38% share, n=13-16, ±31-36pp —
   **worthless, do not quote it**).
4. **v37 vs v34 is not separable.** 52.9% ± 14.5pp vs 45.7% ± 14.6pp. The +58.4
   Elo in 14 matches is real money on the ladder and **not** evidence that v37 is
   a better bot than v34.
5. **DEFF applied per the CLAUDE.md procedure, clusters enumerated.** MATCH
   cluster: live in every cut here (multiple games per match in every
   population) — not removed. OPPONENT cluster: live (several matches per
   opponent). Both live ⇒ **pooled constants used: 1.529 rated, 1.833 unrated.**
   The §3.8 latency claim is stated as an **exclusion** (CI excludes zero) before
   the correction is applied, per the direction clause.
6. **`econ.tsv.deliveries` is still identically zero** (462,708 rows, sum 0,
   re-verified) and no claim here rests on it. `econ.tsv.shots` IS populated
   post-v2-rebuild and is used.
7. **Live pull noted:** 185 replay files downloaded via `fcode match replay`
   (READ-ONLY per `docs/fcode-cli.md:130`). No matches created, no submission
   touched, nothing committed outside this document. Working files are under
   `scratchpad/s53_o1_*`.
8. **The three-family taxonomy in §4 is a RELAYED FRAME from the builder's pivot
   note**, not an independently established repo fact; only the measurements
   against it are mine.
