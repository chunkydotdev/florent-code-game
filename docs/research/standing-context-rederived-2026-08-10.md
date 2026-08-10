# The rest of the standing context, re-derived on the current bot

**Research arm, 2026-08-10 (s26).** Companion to `prior-tracing-2026-08-10.md`, which re-ran
**four** of the `tactics/INDEX.md` §"Standing context a sweep should know" instruments on the
v102 subset and found all four inverted. **This document does the remaining measurable claims
in that section.** Measure-and-report only — **nothing here edits or retracts any other
document.**

---

## 0. POPULATIONS, SUBJECTS, DENOMINATORS AND FIXTURES — stated once, because every row below
inherits them

**Corpus:** `corpus/` at manifest `2f0649c`-lineage, synced state of 2026-08-10 02:24
(`archive_replays` per `manifest.json`; 4,240 distinct files appear in `throws.tsv`).
**Zero downloads. Zero arena. Zero bot edits.**

**How "us" and "our version" are established — and it is NOT winner-derived.** TRAP 7 says
`ladder_games.seat`, `meta_join.us_side`, `join.our_team` and `ladder_games.won` all descend
from `winnerSide`, so cross-checking them is circular. **This document takes our side from
`meta_join.teamAName` / `teamBName == 'OpenSverige'`** — a team *name*, which no winner field
feeds — and our version from the matching `teamAVersion` / `teamBVersion`.

Two independent checks that this is the right seat:

```
name-derived us_idx == join.our_team :  1,740 / 1,740  = 100.0000%
behavioural  : v102 US builder attacks = 0 over 160 games ; v102 THEM = 9,408
               (LOKI-8's silenced melee — the bot's own fingerprint, TRAP 7's recommended check)
               Eir US builder attacks = 357,834, so the zero is a v102 property, not a decoder bug.
```

**Three populations are used, and they are not the same thing:**

| name | what it is | n (Eir ≤v101) | n (v102) |
|---|---|---|---|
| **LADDER POPULATION** — `ladder_games.tsv` | every rated ladder game we have metadata for, archived or not | 2,850 | 160 |
| **JOIN VIEW** — `join.tsv` ∩ `meta_join.tsv` | ladder games whose replay is archived **and** attributed. **A VIEW, not a population** — it excludes ladder games whose replay was never archived or never attributed (**1,270 Eir games**; **0 v102 games — v102 archive coverage is complete**, which is why the JOIN VIEW and the LADDER POPULATION return bit-identical v102 numbers in §2) | 1,580 | 160 |
| **ARCHIVE-WIDE** — all decoded replays | every archived replay, all teams, including matches we are not in (~70% of `throws.tsv`) | 4,240 files | — |

**Fixture:** rated ladder only, except where ARCHIVE-WIDE is named. **The two eras do not face
the same field**: v102's opponents are stronger (**90.6% rated ≥1550, mean 1591** against Eir's
**66.8%, mean 1576**). Every headline below was therefore **re-run on a common-opponent matched
fixture** (the 15 opponents v102 has actually played; Eir n=1,215 / v102 n=160) — §4. **The
matched fixture moves nothing by more than 1.5pp.** Where composition could matter it is the
opponent-mix that *understates* v102, since v102 plays a harder field.

**The brief's stated denominators are stale.** It says *"~1,580 Eir games vs ~130 LOKI-8"*.
The corpus has grown: **160 v102 ladder games, 180 v102 side-games in `meta_join`**. That is
23% more v102 than the companion cut had, and it is why two of its bands (r0-150, r151-300)
now carry usable n.

---

## 1. THE CLASSIFICATION TABLE

**HOLDS 5 · INVERTS 4 · STRENGTHENS 1 · WEAKENS 1 · NOT REPRODUCIBLE 1 · NO DENOMINATOR 4
(as sub-rows)** over 12 measurable claims.

| # | claim (as the section states it) | published | **Eir control** (does my instrument match theirs?) | **v102** | class |
|---|---|---|---|---|---|
| 1 | *"Conditional on a core kill, the chance it is ours rises 29% → 55% → 72% → 76%"* | 29 / 55 / 72 / 76 · n=293/259/221/104 | **31.5 / 53.7 / 72.5 / 76.9** · n=372/341/273/117 · **reproduces** | **41.2 / 37.5 / 55.6 / 75.0** · n=**51/72/18/8** | **INVERTS** (bands 1-2); bands 3-4 **NO DENOMINATOR** |
| 2 | *"We win the opening and we win the clock; we die in the middle."* | — | opening 68.5% (n=372) · middle 46.3% (n=341) · clock 56.4% (n=477, 30.2% of games reach it) | opening **58.8%** (n=51, p=0.17) · middle **62.5%** (n=72, **p=0.013**) · clock **9.1%** (n=**11**, only **6.9%** of games reach it) | **INVERTS** on the middle; **WEAKENS** on the opening; clock **NO DENOMINATOR** |
| 3 | *"Only 12% of top-tier kills land by r100; median kill round r296."* | 12% · r296 | clf C **9.9% · r289** (n=635); clf B **7.5% · r316** (n=478) · **reproduces** | clf C **22.6% · r198** (n=53); clf B **20.7% · r202** (n=58) · **p=0.0009** | **INVERTS** |
| 4 | *"Late offensive insertion is refuted — 2.34% of forward throws at r200+ ever land a single attack on the enemy core."* | 2.34% · 1,914 files | ARCHIVE-WIDE (the published population) is now **1.11%** · n=25,357 throws / 4,240 files. **Level not reproducible; the archive tripled.** | our own r200+ INSERTs: Eir **1/41 = 2.44%**, v102 **0/30** | **HOLDS as a negative** · the *figure* **NOT REPRODUCIBLE** · our-side v102 **NO DENOMINATOR** · **SUBJECT ERROR, see §3** |
| 5 | *"raider survival collapses 43 → 6 rounds at exactly r150"* (one of the five r150 instruments) | 43 → 6 | ARCHIVE-WIDE **35 → 7 → 7 → 6** · n=12,555/3,010/5,178/20,179 · **shape reproduces, level does not** | our own: Eir **73 → 75 → 7 → 9** (n=553/39/17/24) — **our cliff is at r200, not r150**; v102 **89 → 14 → 25 → 183** (n=90/8/16/14) | ARCHIVE-WIDE **HOLDS** · **SUBJECT ERROR** · v102 **NO DENOMINATOR** |
| 6 | *"We run a damage-to-repair ratio of 1.11:1 against the field's 2.79:1."* | 1.11 : 2.79 | **1.05 : 2.76** · n=1,580 games · **reproduces** | **1.17 : 4.30** · n=160 games | **HOLDS** (ours); field side **STRENGTHENS** |
| 7 | *"Healing is 4.00 HP/Ti and the best damage source is 1.80 HP/Ti → the defender wins a titanium-symmetric attrition race 2.2:1"* | 2.2 : 1 (a **bound**) | our **realised** damage efficiency **1.51 HP/Ti → 2.65:1** (149,986 shots, 1,265,858 ammo-Ti, 357,834 builder attacks) | our realised **1.79 HP/Ti → 2.24:1** (8,877 shots, 89,285 ammo-Ti, **0** builder attacks) | rules half is an **engine constant**; realised half **STRENGTHENS to the bound** |
| 8 | *"We heal 1.75× more than the field and buy 0.61× as much ammunition."* | 1.75× / 0.61× | **1.75× / 0.57×** · n=1,580 · **reproduces** | **1.92× / 0.56×** · n=160 | **HOLDS** |
| 9 | *"Our opening is a near-constant — CV 0.09 vs the field's 0.26"* (builder bots built, r0-50) | 0.09 / 0.26 (2.74×) | **0.09 / 0.26 (2.77×)** · n=1,580 games · **exact reproduction** | **0.09 / 0.30 (3.51×)** · n=160 games | **HOLDS** — the strongest survivor in the section |
| 10 | *"we already out-build the field on conveyors (+13) and under-build turrets (−3, leading in only 20.1% of games)"* | +13 / 71.7% · −3 / 20.1% | **+11.6 / 75.3%** · **−1.8 / 22.5%** · n=1,580 paired games · **reproduces** | **+15.8 / 85.0%** · **−1.1 / 25.6%** · n=160 paired games | **HOLDS** (conveyor lead widens) |
| 11 | *"Before r150 we place turrets almost identically to them (41% forward vs 38%). The divergence begins at r150: they push turrets outward, we pull them home."* | 41 / 38, then them-out / us-home | r0-150 US **38.4%** / THEM **43.0%**; then US **32.7 → 31.6 → 19.5**, THEM **54.2 → 52.3 → 53.5** · n=5,616/8,486 builds r0-150 · **reproduces** | US **35.8 → 55.6 → 70.6 → 83.3**; THEM **44.6 → 65.8 → 22.6 → 40.9** · n=611/126/153/360 US builds | **INVERTS** |
| 12 | *"US 97.7 shots/game against the field's 258.5"* (`corpus-howto.md` §trap 5) | 97.7 / 258.5 | **94.9 / 262.8** per game; **18.9 / 52.4** per 100 rounds lived · n=1,580 games · **reproduces** | **55.5 / 195.4** per game; **20.0 / 70.4** per 100 rounds lived · n=160 games | **HOLDS per round** — our fire rate is unchanged; the field's rose 34% |

**Not classified because they cannot drift** (engine constants and rules facts, as the brief
directs): the 4.00 / 1.80 / 1.75 / 1.00 HP-per-titanium table itself; the heal-stacking cap of
2 entities → 8.00 HP/Ti; store semantics (buffered, last-writer-wins, unsigned-32 range);
sentinel-through-friendlies; spawn ring = Chebyshev-1; unit turn order = global entity-id
ascending and its four consequences; `MAX_TEAM_UNITS`; harvester/`+20%` cost-scaling arithmetic.

---

## 2. THE ONES THAT CHANGED, RANKED BY HOW LOAD-BEARING THEY ARE

### #1 — **"EVERYTHING ABOUT US BREAKS AT r150" NOW HAS ZERO OF ITS FIVE INSTRUMENTS LEFT**

The section names five independent instruments for the r150 break. The companion cut killed
three. **This document accounts for the other two, and the count is now complete:**

| the five instruments | status on v102 |
|---|---|
| ammo conversion | **INVERTED** (companion: 209 → 300 → 253 → 135 Ti/100rd; converts 43% *more* after r150) |
| turret production | **INVERTED** (companion: r200-300 us 2.15 vs field 1.18 — reproduced independently here, §4) |
| conversion ratio / titanium banking | **INVERTED** (companion: Ti held r200-300 us 96 vs field 210) |
| **forward placement** | **INVERTED — this document.** After r150 v102 pushes turrets *forward* (55.6% → 70.6% → 83.3%) while the field pulls them home (65.8% → 22.6% → 40.9%). Eir did the exact opposite in both roles. |
| **raider survival 43 → 6** | **NO DENOMINATOR on our own line** (n=8/16/14 throws per band after r150) — and on the Eir line the instrument **never showed an r150 cliff for us at all**: our own median raider life is 73 → 75 → 7 → 9. **The r150 boundary in this instrument is an ARCHIVE-WIDE fact that was attributed to us.** |

**So the sentence "five independent instruments agree" is now: four inverted, one that was
never measuring us.** The forward-placement inversion is the sharpest of the four because it
reverses a *doctrinal* description, not a level: *"they push turrets outward, we pull them
home"* is, on the current line, **exactly backwards** — and it is a direct read on `THE FORWARD
ROAD IS CLOSED`, since v102 is now planting 83.3% of its late turrets forward. Read together
with the companion's finding that v102 FAR-turret 50-round survival is **11.6%** (n=361), the
current bot is doing the thing the doctrine calls closed, and losing those turrets.

### #2 — **"WE DIE IN THE MIDDLE" IS THE ONLY CLAUSE WITH A v102 DENOMINATOR, AND IT FLIPS**

```
core-decided games, our win rate            Eir                v102
r0-150                                   68.5% (n=372)     58.8% (n=51)   p=0.17
r151-300                                 46.3% (n=341)     62.5% (n=72)   p=0.013   <- flip
r301-600                                 27.5% (n=273)     44.4% (n=18)   NO DENOMINATOR
r601-999                                 23.1% (n=117)     25.0% (n= 8)   NO DENOMINATOR
r1000 (share of games / win rate)   30.2% / 56.4% (n=477)  6.9% / 9.1% (n=11)
```

The three-clause sentence resolves as: **middle INVERTS** (the one well-powered band), **opening
WEAKENS but not significantly**, **clock has no denominator** — 11 games, 1 won. And the
*reach* rate is itself a finding with power behind it: at the Eir rate, 160 v102 games should
have produced ~48 games at r1000; **11 did.**

**Method rule 7 check, and it is the honest limit on this row.** Per opponent with n≥5 in the
v102 r151-300 band, the flip is **up in 5, down in 3, unchanged in 1** (of 9): Powerpuff Girls
57.1→85.7, CtrlAltDefeat 25.7→83.3, Team 48 75.0→100.0, Askar City 54.2→57.1, Leviathan
50.0→60.0 against farming_200s 42.9→27.3, OopsGotYourElo 62.5→50.0, gsxWins 71.4→50.0.
**Every per-opponent cell is n=5-11.** The pooled flip survives common-opponent matching (§4)
but it is **not** reproduced opponent-by-opponent, and that should be said out loud.

### #3 — **"THE FIELD DOES NOT RUSH" DOES NOT DESCRIBE WHAT THE FIELD DOES TO THE CURRENT BOT**

```
opponent >=1550, kills THEY land on US        Eir                v102
classifier B (name+version)      median r316, 7.5% by r100 (n=478)   median r202, 20.7% by r100 (n=58)   p=0.0009
classifier C (name)              median r289, 9.9% by r100 (n=635)   median r198, 22.6% by r100 (n=53)
our own kills, median round               r168 (n=329)                r178 (n=77)
```

Both classifiers agree and the by-r100 shift is significant at n=58. **Against v102 the strong
field kills ~110 rounds earlier and lands two and a half times as many kills inside r100.**

**But the instrument is a matchup property, not a field property** — `prior-tracing` row 6
already flags this, and my numbers are the demonstration: the *same* opponents killing a
*different* bot of ours produce a different "field clock". `field-baselines-third-party` §2-3
gives the genuinely third-party figure (**r229** matched) and instructs that the pair be quoted
as *"r283 vs r229"*. **The 12%-by-r100 clause, which is third-party confirmed at 13% (N=2,257),
is the half that is safe to keep; the median clause should not be quoted at all.**

### #4 — **THE 2.2:1 DEFENDER'S EDGE IS NOW OUR ACTUAL EDGE, NOT A BOUND WE MISSED**

The `4.00 / 1.80 → 2.2:1` arithmetic is a rules fact and cannot drift. What drifts is **which
damage channels we pay for**, and it moved a long way:

```
                     shots     ammo-Ti    builder atks   ammo/shot   realised HP/Ti   heal edge
Eir   US            149,986  1,265,858       357,834        8.44          1.51          2.65:1
Eir   THEM          415,154  2,215,731       242,747        5.34          1.63          2.45:1
v102  US              8,877     89,285             0       10.06          1.79          2.24:1
v102  THEM           31,267    160,786         9,408        5.14          1.69          2.37:1
```

*(Mix solved from the identity `shots = g+s`, `ammo = 4g+10s`, damage `= 7g+18s`; builder
attacks enter at 1.00 HP/Ti. Only identified where 4 ≤ ammo/shot ≤ 10, which all four rows
satisfy.)*

**v102 is a pure-sentinel spender with zero melee — ammo/shot 10.06 — so it realises 1.79 of
the theoretical best 1.80 HP/Ti.** Eir realised 1.51, because a third of its titanium-to-damage
went through 1.00 HP/Ti builder attacks. **The standing sentence "we run 1.11:1 against the
field's 2.79:1" survives (1.17 vs 4.30) — but its *implication*, that we are the ones spending
inefficiently, is now false in the channel sense: on a per-titanium basis our damage is the
most efficient on the board and the field's is 1.69.** What we do less of is *spend at all*
(§1 row 12: 20.0 shots per 100 rounds against 70.4).

---

## 3. TWO PUBLISHED CLAIMS WHOSE SUBJECT IS NOT WHO THE SECTION SAYS IT IS

**Both are the `2.68 healers` failure family — a true figure attached to the wrong referent —
and neither is an era problem.**

1. **`"Late offensive insertion is refuted FOR US — 2.34% of forward throws at r200+"`.** The
   published 2.34% is computed over **all 11,895 INSERT throws in all 1,914 then-archived
   replays, every team** (`late-game-doctrine` §1: the whole four-band table is field-wide).
   **It is not our bot's number.** Our own r200+ INSERTs number **41 in the entire Eir era and
   30 on v102** — the companion cut's "1 of 42 / 0 of 27" is that tiny estimand, not this claim.
   **Re-running the published estimand today gives 1.11% (n=25,357 throws, 4,240 files):** the
   conclusion is unchanged and if anything stronger, but **the number 2.34% is no longer
   reproducible**, because the archive tripled and the composition changed.
2. **`"raider survival collapses 43 → 6 rounds at exactly r150"`, listed as one of the five
   instruments for "everything about US breaks at r150".** Also field-wide. **On our own Eir
   throws there is no r150 cliff: 73 → 75 → 7 → 9 rounds.** Our collapse, such as it is, is at
   **r200**, and rests on n=17. **This instrument has never supported the sentence it is cited
   under.**

---

## 4. CONTROLS AND CROSS-CHECKS THAT WOULD HAVE CAUGHT ME

**(a) Instrument-match control against the companion cut.** Before trusting any new number I
re-ran two of the companion's four on my own code path. Exact agreement:

```
turrets built r200-300, per game reaching r200   Eir US 0.64 / THEM 2.22 (n=1,077)
                                                v102 US 2.15 / THEM 1.18 (n=71)
titanium held at end of r200-300                 Eir US 506.1 / THEM 348.2
                                                v102 US  95.7 / THEM 209.5
```

Identical to `prior-tracing` §2 to the digit. **My decoder is theirs.**

**(b) Common-opponent matched fixture** (15 opponents; Eir n=1,215, v102 n=160), because v102
faces a stronger field:

```
core-decided win rate     Eir pooled -> matched      v102
r0-150                       68.5% -> 70.0%          58.8%
r151-300                     46.3% -> 47.9%          62.5%
r301-600                     27.5% -> 29.5%          44.4%
r1000 share                  30.2% -> 30.2%           6.9%
forward turret share r200-300 US   31.6% -> 29.0%     70.6%
forward turret share r300+  US     19.5% -> 19.9%     83.3%
```

**Matching moves nothing by more than 1.5pp.** Composition is not the explanation for any
headline in §2.

**(c) The complement-group control that TRAP 8 exists to enforce.** `econ.deliveries` is not
used anywhere in this document, and `econ.shots` is not either — every shot figure comes from
`build_agg.metric == 'shot'`. Spot-check re-run today: over **all 55,018 rows** of
`econ.tsv`, `deliveries` sums to **0** and `shots` sums to **0** — exactly as TRAP 5/8 state,
still unfixed.

---

## 5. WHAT I COULD NOT MEASURE, WITH THE n

- **Hazard bands r301-600 and r601-999 on v102** — n=18 and n=8 core-decided games. Reported in
  the table for completeness and **classified NO DENOMINATOR**. The monotone-rise shape cannot
  be tested on v102 at all; only its first two bands have n.
- **"we win the clock", 57.2%** — v102 reaches r1000 in **11 of 160 games** and won **1**. The
  companion said this at n=9; the corpus has grown and it is still no number.
- **Our own late-insertion rate on v102** — **0 of 30** r200+ INSERT throws landed a core
  attack. A zero on n=30 is consistent with any true rate below ~10% and cannot distinguish
  "worse than Eir's 2.44%" from "the same".
- **Our own raider survival by band on v102** — n=8 / 16 / 14 throws in the three post-r150
  bands. The r300+ median of 183 rounds rests on **14 throws** and should not be quoted.
- **Per-opponent decomposition of the middle-game flip** — every cell is n=5-11 (§2 #2). The
  pooled result is well-powered; the per-opponent reproduction is not.
- **`"2.13 adjacent builders at 3+ attackers, 1.57 at 1, N=28,277"`** (the corrected
  sentinel-file staffing figure) — **not attempted.** It needs per-round tile-adjacency, which
  no committed corpus table carries (`corpus-howto`: per-round positions are not extracted).
  It is also a statement about *opponents'* defence, so it is not era-exposed in the way the
  rows above are.
- **The `+11.4 / +16.6 / +22.3pp` home-defence gap** — already re-derived by the companion
  (Eir +16.3pp, v102 −10.0pp, n=439/520). Not repeated here.

---

## 6. ONE-LINE SUMMARY FOR THE SECTION ITSELF

**Of twelve measurable standing claims: four invert, one weakens, five hold, one strengthens,
and one is no longer reproducible at its published level.** The survivors are all *structural*
— our opening constancy (CV 0.09, exact), our conveyor lead, our heal-to-ammo split, our
per-round fire deficit. **Everything that inverted is a claim about what we do after r150**:
turret production, titanium banking, ammo conversion, forward placement, and who dies in the
middle. **The section's opening description of the early game is still accurate. Its entire
account of our middle game describes a bot we stopped fielding.**
