# WHY WE LOSE TO `kladde chatte tville (och oss)` — the mechanism behind the r322–r746 shutout

**Written:** `2026-08-16T08:30:49Z` (`date -u`, same shell call as the final queries).
**Repo HEAD at write time:** `97669852` (`2026-08-16T10:28:51+02:00` = `08:28:51Z`).
**Lane:** research arm, read-only. No bot edited, no match fired, no verdict written.
**Predecessor:** `docs/research/RATED-DAY-DECODE-2026-08-16.md` — its §4.1 and §6.1 pose the
question this file answers. Nothing in it is re-derived here.

---

## 0. THE ANSWER IN FIVE LINES

**It is not a conversion failure. It is a TOTAL failure to damage them at all, sustained for
300–750 rounds by a build loop with no brake.**

1. Against kladde we lose **~17 entities for every 1 of theirs** (r300+ rated games, n=9:
   we lose 78/game, they lose 4.6/game). Against everyone else the exchange is ~1.4:1.
2. Our whole offensive output is one **forward sentinel**, planted a median 3.6 tiles from
   their core. Against kladde it dies in a **median 6 rounds, 99% of the time**.
3. We rebuild it **20.8 times per game** (25.8 in the 05:52 shutout) — and **73% of those
   plants are replants onto a tile where a previous one already died**, at a median gap of
   **9 rounds**. One game put **50 sentinels on the single tile (16,1)**.
4. There is **no attrition memory anywhere in that path**. `LOKI2B_LIVE_CAP_ON` replaced the
   old monotone rubble counter with a **live census of sentinels alive** — so a sentinel that
   dies in 6 rounds frees the cap in 6 rounds, forever.
5. We survive to r322–746 only because kladde does not rush. Our alive-unit count is **pinned
   at 7–8 for the entire game** while theirs compounds **8 → 26**. Then their accumulated
   firepower reaches our core.

**Structural, not tuning.** Six independent mechanism signatures all replicate out-of-sample on
**111 unrated games spanning six kladde versions (v80–v97) and eight of ours (v85–v143)**. This
is not a v119 counter and not a today artefact.

---

## 1. INSTRUMENTS, FREEZE, AND WHAT WAS EXCLUDED

### 1.1 Freeze

`corpus/ladder_games.tsv` **changed under me mid-analysis** (5,471 → 5,481 rows; mtime moved to
`08:18:44Z` while I was querying) — the corpus keeper is live. Every number below is therefore
computed from a **frozen snapshot** taken at `2026-08-16T08:20:27Z`
(`scratchpad/ladder_games.FROZEN.tsv`, `scratchpad/meta_join.FROZEN.tsv`).

| tape | mtime (UTC) | use |
| --- | --- | --- |
| `ladder_games.tsv` (frozen) | 08:18:44Z | rated per-game outcomes, the only rated denominator |
| `meta_join.tsv` (frozen) | 07:56:52Z | replay file → seat |
| `events.tsv` | 07:53:06Z | per-entity BUILD/DEATH with round, team, tile, d²-to-both-cores |
| `build_agg.tsv` | 07:55:00Z | per file × team × band counters (`shot`, `batk`, `build_*`) |
| `econ.tsv` | 07:53:49Z | `heals`, `ammo_converted`, `ti_*_end`, `tled` |
| `unrated_games.tsv` | 08:22Z | unrated per-game `cond`/`turns`, read off the replay binary |

**Replay-derived tapes lag `ladder_games` by ~25 minutes.** 10 rated games of 2026-08-16
(the `07:52:59Z` match vs 0033 and one more) have metadata but no decoded replay; they are
**dropped from every cell** and the drop is printed by the group builder. Denominators below are
post-drop.

### 1.2 ⛔ LIVE-LEG EXCLUSION — `LEG-fieldcal-2026-08-16`, and it cost me the whole unrated v119 cell

`docs/prereg/LEG-fieldcal-2026-08-16.md` is LOCKED and LIVE. Its ten pinned cells, read off the
prereg's own `CELLS:` line rather than assumed: **Juusto v13 · not adgato v23 · Erebus v119 ·
kladde chatte tville v119 · gsxWins v46 · 0033 v57 · lingling_40h v61 · HTTP 418 v103 ·
The Bisons v9 · farming_200s v15.** Clock 2 = `2026-08-16T06:25:40.381Z`.

Rule applied: **every unrated row whose opponent is a panel cell and whose `createdAt` ≥ clock 2
is excluded.**

```
unrated rows total                       5,956
EXCLUDED as live-leg cells                 155   Erebus 50 · Juusto 50 · not adgato 25
                                                 · kladde 25 · 0033 5
kept                                     5,801
```

**All 25 unrated kladde rows of 2026-08-16 are post-clock2 and all 25 are excluded.** They are
the `v140 vs v119` games the addendum pointed at. **The unrated surface adds ZERO games on
kladde v119** and I did not look at their outcomes.

**What the unrated surface DID give me is better than that cell would have been:** 111
**pre-clock2** kladde games from 2026-08-08 → 2026-08-14, across **six kladde versions and eight
of ours**. That is the out-of-sample replication in §5, and it is a stronger instrument than 25
same-version games would have been.

### 1.3 Controls run before any number was trusted

| # | check | expectation stated FIRST | result |
| --- | --- | --- | --- |
| **S1** | seat mapping: `meta_join.us_side` must be derived from TEAM NAMES, not from `winnerSide` (TRAP 7) | if it is name-derived, `us_side` agrees with "which seat is OpenSverige" in 100% of rows | **10,061 rows, 0 mismatches** |
| **S2** | replay team index ↔ platform side | `team 0 ↔ side a` consistently, or the mapping is unusable | **(0,a) 2,120 · (1,b) 2,040 · 0 crossings, n=4,160** |
| **S3** | **behavioural** seat control (TRAP 7 says name/winner cross-checks are circular; a bot fingerprint is not) — our line's builders essentially never melee an enemy core | `batk_core` ≈ 0 on OUR side, large on theirs; a flipped seat inverts it | rated groups: **US 0, THEM 3,415 over 400 files**; unrated groups: **US 47, THEM 6,791 over 2,021 files (0.7%)**. Fires in one direction only. ✔ |
| **S4** | `batk_core` is not a dead column (the constant-column trap) | must be non-constant corpus-wide | **20,264 rows, all non-zero, values 1…100+** — live, and its zero in our cells is a genuine absence of rows, not a dead field |
| **S5** | `econ.heals` is not a dead column | must vary across cells | **varies 64 → 566 per game across groups** ✔ |
| **S6** | decoder control on the headline: 50 sentinel BUILDs on one tile must be 50 distinct entities, not `placeEntity` re-emission (TRAP 1) | if real, DEATH events at that tile ≈ BUILD events | **tile (16,1): builds 50, deaths 49** (one alive at the final bell) ✔ |
| **S7** | is the replant treadmill a *kladde* signature or merely a *losing* signature? | if merely "losing", long LOSSES to other opponents show it too | **they do not** — see §4.3. Control comes out the other way. |
| **S8** | is "the shooter was invisible" the reason we plant badly? | I expected a large 21–32 d² blind band (builder vision r²=20 < sentinel range r²=32) | ⛔ **REFUTED: 95% of our forward plants vs kladde have a live enemy sentinel at d² ≤ 20 — visible.** Blind band = 1%. My hypothesis, killed by its own cell. Reported in §6. |
| **S9** | damage ledger closes (delivered ≈ absorbed-by-heals + entities-lost) | residual small in EVERY group, or the damage model is wrong | residual **+201 / +105 / +282 / +75 / −6** HP per game across the five groups — closes within ~10% everywhere ✔ |

**Traps respected:** `throws.tsv` is **not used anywhere in this document** (its outcome columns
are `INSERT`-only, it has no version column). `join.tsv` is not used as a denominator. `meta_join`
is used ONLY as a file→seat map, never as a rated denominator — every rated share comes from
`ladder_games.tsv`. `econ.tsv`'s dead `shots`/`deliveries` columns are not read; shot counts come
from `build_agg.tsv metric == 'shot'`.

---

## 2. THE THREE GROUPS

All rated cells are **v152 in 100% of games** (verified: distinct `ourver` = {152}).

| group | definition | n games | matches | our share | median turns |
| --- | --- | --- | --- | --- | --- |
| **A — kladde** | `kladde chatte tville (och oss)` v119, 2026-08-16 rated | **15** | 3 | **0.200** | 335 |
| **A′ — the 05:52 shutout** | the single 0/5 inside A | **5** | 1 | **0.000** | 349 |
| **B — the rush shutout teams** | `0033` v57 + `gsxWins` v46, same day | **30** | 6 | **0.233** | 222 |
| **C — everyone else** | the other 8 opponents, same day | **70** | 14 | **0.671** | 166 |
| A15 — kladde, 2026-08-15 rated | v94 + v119 | 10 | 2 | 0.500 | 256 |
| C15 — rest, 2026-08-15 rated | 16 opponents | 275 | 55 | 0.564 | 185 |

**Length is the first confound and it is controlled everywhere below.** A's median game is
**2.0× longer** than C's, so raw per-game counts are not comparable. Every headline is given
either **length-normalised (per 100 rounds)** or **restricted to games reaching r300**.

### 2.1 Clustering — enumerated and verified for the A-vs-C share

Per `CLAUDE.md`'s procedure, not a lookup.

* **MATCH cluster.** Can the A stratum hold >1 game of one match? **VERIFIED: exactly 5 games per
  match in all 3 A matches and all 14 C matches.** LIVE on both sides.
* **OPPONENT cluster.** A holds exactly one opponent ⇒ **DEAD for A**. C holds eight opponents,
  six of them with ≥2 matches ⇒ **LIVE for C**.
* ⇒ **within-opponent rated DEFF 1.366 on the A term; pooled rated DEFF 1.529 on the C term.**

```
A vs C, 2026-08-16 rated:   0.200 (3/15)  vs  0.671 (47/70)
  p̄ = 0.5882
  hw95 = 1.96*sqrt( p̄(1-p̄) * (1.366/15 + 1.529/70) ) = 0.3241
  difference = -0.4710   ->  EXCLUDES ZERO
```

**Direction check.** This is an **EXCLUSION** claim (the interval excludes a zero gap), so DEFF
widening makes it *harder*, which is the safe direction. No fail-to-exclude claim is banked
anywhere in this document without being restated first.

**⚠ The A-vs-C split is post hoc** and `RATED-DAY-DECODE`'s Control E already priced that
(68/300 random 3-opponent groupings also exclude zero). **The evidence in this file is not the
share gap — it is the mechanism, which is visible at n=5 and replicates at n=111.**

---

## 3. WHAT ACTUALLY HAPPENS — the entity ledger

**Population: rated games reaching r300, v152, 2026-08-16.** Built / died per game, from
`events.tsv` BUILD/DEATH pairs.

| group | side | builder_bot | sentinel | gunner | harvester | conveyor | barrier | **total lost / game** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **A kladde** (n=9) | **US** | 14.0 / **11.2** | 22.2 / **21.2** | 0.4 / 0.3 | 12.2 / **8.4** | 65.6 / 28.1 | 12.9 / **8.7** | **78.0** |
| | **THEM** | 5.8 / **0.4** | 13.9 / **0.9** | 4.0 / 0.2 | 6.8 / **0.0** | 59.9 / **1.4** | 11.6 / 1.9 | **4.6** |
| **A′ 05:52** (n=5) | US | 12.4 / 8.8 | 26.2 / **25.4** | 0 / 0 | 12.2 / 8.0 | 57.4 / 17.6 | 16.6 / 13.2 | **88.0** |
| | THEM | 4.8 / **0.0** | 12.4 / **0.6** | 4.6 / **0.0** | 6.4 / **0.0** | 57.2 / **0.8** | 6.6 / **0.0** | **1.4** |
| **B rush** (n=9) | US | 8.9 / 2.1 | 7.1 / 4.9 | 1.6 / 0.9 | 6.4 / 1.7 | 39.9 / 16.6 | 7.0 / 1.0 | 27.3 |
| | THEM | 10.6 / 5.3 | 2.6 / 0.9 | 6.7 / 1.3 | 7.3 / 0.0 | 69.7 / 9.9 | 12.1 / 3.6 | 21.0 |
| **C rest** (n=8) | US | 9.2 / 2.7 | 6.7 / 2.0 | 1.1 / 0.3 | 6.7 / 1.3 | 37.9 / 7.2 | 11.6 / 6.2 | 19.7 |
| | THEM | 10.0 / 4.9 | 2.0 / 0.8 | 3.3 / 1.3 | 6.0 / 0.2 | 34.6 / 2.7 | 2.8 / 1.4 | 15.3 |
| C15 rest 08-15 (n=59) | US | 8.2 / 2.4 | 5.3 / 3.2 | 1.0 / 0.2 | 6.9 / 2.3 | 37.7 / 8.6 | 8.9 / 3.5 | 20.2 |
| | THEM | 9.0 / 2.7 | 3.2 / 1.3 | 2.8 / 0.8 | 6.3 / 0.3 | 53.4 / 5.6 | 4.4 / 1.0 | 10.7 |

**Read the 05:52 row again. Across five games of 322–746 rounds, kladde lost 1.4 entities per
game — 0.6 of a sentinel and 0.8 of a conveyor. Nothing else of theirs died at all.** We lost 88.

**Length-normalised, per 100 rounds of game, all 11 opponents of 2026-08-16 rated:**

| opponent (their ver) | n | share | med turns | our fwd sentinels /100r | their sentinels /100r | **our HP lost /100r** | **their HP lost /100r** | **exchange** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **kladde v119** | 15 | 0.20 | 335 | **3.55** | 2.78 | **507** | **53** | **9.5 : 1** |
| 0033 v57 | 15 | 0.20 | 235 | 0.79 | 0.65 | 254 | 105 | 2.4 |
| gsxWins v46 | 15 | 0.27 | 210 | 0.75 | 1.17 | 233 | 144 | 1.6 |
| not adgato v23 | 10 | 0.40 | 174 | 0.70 | 0.29 | 309 | 211 | 1.5 |
| HTTP 418 v103 | 15 | 0.53 | 215 | 0.82 | 0.45 | 238 | 193 | 1.2 |
| Juusto v13 | 5 | 0.60 | 133 | 0.88 | 0.55 | 176 | 241 | 0.7 |
| lingling_40h v61 | 15 | 0.67 | 156 | 1.08 | 0.92 | 176 | 258 | 0.7 |
| Coreflood v89 | 5 | 0.80 | 241 | 1.72 | 1.39 | 222 | 238 | 0.9 |
| The Bisons v9 | 10 | 0.80 | 98 | 0.84 | 2.66 | 102 | 344 | 0.3 |
| Well have a look v9 | 5 | 1.00 | 157 | 2.67 | 0.82 | 119 | 282 | 0.4 |
| team lazy v231 | 5 | 1.00 | 192 | 1.23 | 0.58 | 263 | 416 | 0.6 |

**The exchange ratio is monotone-ish with game share across all eleven cells and kladde is 4×
worse than the next-worst.** Their 53 HP lost per 100 rounds is the lowest number on the board by
a factor of two.

**⚠ Neither "sentinel-heavy" nor "high replant" alone identifies kladde.** The Bisons run
**more** sentinels per round (2.66) and we beat them 8/10; "Well have a look" draws **2.67**
forward plants per 100 rounds from us and we beat them 5/5. **The discriminating pair is
high replant rate AND near-zero enemy attrition**, and that combination is unique to kladde among
today's eleven opponents.

---

## 4. THE MECHANISM

### 4.1 Our single weapon is a forward sentinel, and against kladde it never survives

`batk_core` is **0 for us in 400 of 400 archived rated games** (§1.3 S3/S4) — our line does not
melee cores. **Our only kill vector is turret fire.** `raid.py:31`: *"The damage itself then comes
from a forward SENTINEL."*

Forward = planted nearer their core than ours (`d2_enemy < d2_own`). Placement quality is fine:
median `d²` to their core is **13 (3.6 tiles)** and **98% are inside sentinel range (r² = 32)**.

| group (r300+) | our fwd sentinels / game | **% that die** | **median lifetime** |
| --- | --- | --- | --- |
| **A kladde** (n=9) | **20.8** | **99%** | **6 rounds** |
| **A′ 05:52** (n=5) | **25.8** | **98%** | **6 rounds** |
| B rush (n=9) | 3.8 | 88% | 13 |
| C rest 08-16 (n=8) | 3.4 | 56% | 5 |
| C15 rest 08-15 (n=59) | 3.6 | 73% | 6 |

**The lifetime is the same 6 rounds everywhere. What differs is the VOLUME — 5.7× — and the
RETURN.** A sentinel that lives 6 rounds at reload 2 fires ~3 times for 54 damage. We buy that
21–26 times a game.

Meanwhile **their home sentinel wall — 8.7 per game — has a death count of ZERO** in the r300+
kladde games, and their forward sentinels die 17% of the time.

### 4.2 The replant loop, and the tile it loops on

| group (r300+) | fwd plants | distinct tiles | **% replants** | **median gap between replants on a tile** |
| --- | --- | --- | --- | --- |
| **A kladde** (n=9) | 187 | 50 | **73%** | **9 rounds** |
| **A′ 05:52** (n=5) | 129 | 33 | **74%** | **10 rounds** |
| B rush (n=9) | 34 | 17 | 50% | 32 |
| C rest 08-16 (n=8) | 27 | 19 | 30% | 74 |
| C15 rest 08-15 (n=59) | 213 | 133 | 38% | 9 |

**Game by game, the 05:52 shutout:**

```
icefloe       746 rounds   60 fwd sentinels,  8 distinct tiles   -> (16,1) x50   (builds 50 / deaths 49)
drakkarfjord  349 rounds   29 fwd sentinels,  3 distinct tiles   -> (29,6) x27
valkyrie      374 rounds   19 fwd sentinels,  9 distinct tiles   -> (22,18) x8
yulerune      346 rounds   13 fwd sentinels, 11 distinct tiles   -> (19,11) x3
auroraveil    322 rounds    8 fwd sentinels,  2 distinct tiles   -> (12,19) x7
```

**Fifty sentinels on tile (16,1), from r105 to the final bell, one every ~9 rounds.** At the
derived cost scale in those games (~270–320%, §4.4) a sentinel costs ~80–95 Ti, so that one tile
consumed **roughly 4,000–4,500 Ti** against a lifetime income of ~6,200 (500 start + 3,870
collected + ~1,860 passive over 746 rounds). **The majority of everything we earned in that game
went onto one tile.**

### 4.3 CONTROL — is this a "kladde" signature or just a "losing" signature? (S7)

The obvious alternative is that long losses always look like this. **They do not.**

| cell | n | fwd plants | **% replants** | median gap |
| --- | --- | --- | --- | --- |
| **A kladde, LOST, r300+** | 9 | 187 | **73%** | **9** |
| C15 rest, **LOST**, r300+ | 30 | 63 | **19%** | 64 |
| C15 rest, **WON**, r300+ | 29 | 150 | 45% | 8 |
| B rush, LOST, r300+ | 7 | 24 | 50% | 34 |
| C rest 08-16, LOST, r300+ | 2 | 6 | 17% | 15 |

**A long LOSS to a non-kladde opponent shows 19% replants at a 64-round gap.** And 45% replants
at an 8-round gap appears in games we **WIN** — because there the replanting works and the core
falls. The treadmill is not the shape of losing; it is the shape of *pushing a lever that does
nothing*.

**Within kladde, the same split:** the 3 games we won used **5.3** forward sentinels at **31%**
replants and ended at median r197; the 12 we lost used **16.8** at **72%** and ran to median r348.
⚠ **That last comparison is a collider** — losses are longer, so they mechanically hold more
plants. It is reported because it is consistent, not because it is evidence; the
length-normalised table in §3 is the non-collider form.

### 4.4 Why we survive to r322 and then lose: we never accumulate, they always do

Derived cost scale (100 + sum of contributions of entities alive: conveyor/splitter/barrier +1,
harvester +5, launcher +10, builder/gunner/sentinel +20) and alive UNIT count (core + builders +
turrets, the `MAX_TEAM_UNITS` population). Median over games reaching each round, r300+ games only.

```
A kladde (n=9)
  US     r50 269%/7u   r100 307%/7u   r150 304%/8u   r200 314%/7u   r250 324%/8u
         r300 311%/7u  r400 312%/8u   r500 277%/7u   r700 266%/7u
  THEM   r50 295%/8u   r100 366%/10u  r150 403%/13u  r200 464%/14u  r250 500%/16u
         r300 522%/18u r400 602%/22u  r500 644%/24u  r700 691%/26u

C15 rest (n=59)   US flat 264->296% / 7-8u      THEM flat 261->374% / 7-10u
```

**Our unit count is pinned at 7–8 for seven hundred rounds. Theirs triples.** Everything we earn
is spent replacing what just died; nothing compounds. That is what "surviving to r746" actually
means here — not a stalemate, a treadmill that ends when their accumulation crosses our core.

### 4.5 Where the damage goes — the ledger closes, and it closes on THEIR HEALS

Per game, r300+ games. Turret damage estimated by splitting `build_agg.shot` against
`econ.ammo_converted` at 10 ammo/sentinel-shot and 4/gunner-shot; builder attacks at 2 dmg.
Entity-loss HP from `events.tsv` DEATH × published max HP. Heals at +4 HP each (`econ.heals`).

| group | side | shots | ammo conv. | turret dmg | batk dmg | **opp heals (HP)** | **opp entity HP lost** | residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **A kladde** | **US** | 103 | 1,262 | 1,850 | 72 | **1,577** | **144** | +201 |
| | THEM | **322** | **2,246** | 4,009 | 303 | 990 | 2,774 | +548 |
| **A′ 05:52** | **US** | 112 | 1,174 | 2,016 | 63 | **1,934** | **40** | +105 |
| | THEM | 315 | 2,272 | 4,060 | 233 | 930 | 2,856 | +507 |
| B rush | US | 144 | 1,441 | 2,082 | 154 | 1,312 | 642 | +282 |
| C rest 08-16 | US | 92 | 867 | 1,532 | 88 | 754 | 791 | +75 |
| C15 rest | US | 115 | 1,054 | 1,867 | 110 | 1,430 | 553 | −6 |

**Control S9: the residual is small in every group, so the damage model is coherent and the
absorption term is real rather than a modelling artefact.**

Three things fall out:

1. **They out-shoot us 3:1** (322 vs 103 shots/game; 2,246 vs 1,262 ammo converted). Our shot
   count is limited by **sentinel lifetime**, not by ammo — we end games holding ~60 ammo and
   ~140 Ti.
2. **Their heal engine absorbs 82% of our damage against kladde and 93% in the 05:52 shutout**
   (1,577 of 1,922; 1,934 of 2,079). Heals per game: **theirs 394 mean / 273 median, ours 247 /
   133.** In the icefloe game they healed **1,205 times** and we healed 591.
3. ⚠ **Heal absorption is high everywhere in long games** (C15: 1,430 of 1,977 = 72%). It is
   therefore **not** kladde's unique property, and I am not claiming it is. The kladde-specific
   part is the pairing: *they absorb more* **and** *we lose 3.6× more of our own stuff*, so the
   residual attrition is 144 HP instead of 553.

**This answers a question `QUEUE.md #32` explicitly left open** — *"AMMO STARVATION, HEALING
(theirs, not ours) and ENEMY TARGET-PRIORITY are all UNTESTED… The healing hypothesis in
particular is not answerable on this corpus: `events.tsv` has no heal verb."* **`econ.tsv` has a
live `heals` column** (control S5), and the ledger closes on it. **Ammo starvation is ruled out
for us** (we end with ammo banked). **Healing is real and large.** Enemy target-priority remains
untested.

### 4.6 Our builders die at 72–80% and theirs do not die at all

| group | our builders built / died | their builders built / died |
| --- | --- | --- |
| **A kladde, r300+** | 14.0 / 11.2 = **80%** | 5.8 / 0.4 = **8%** |
| A′ 05:52 | 12.4 / 8.8 = 71% | 4.8 / 0.0 = **0%** |
| B rush, r300+ | 8.9 / 2.1 = 24% | 10.6 / 5.3 = 51% |
| C rest 08-16, r300+ | 10.4 / 3.0 = 29% | 11.3 / 5.5 = 49% |
| C15 rest, r300+ | 8.2 / 2.4 = 29% | 9.0 / 2.7 = 30% |

Against every other opponent builder attrition is roughly **symmetric**. Against kladde it is
**10:1 against us**. This is the second-order driver of §4.5: a heal needs a *living builder
adjacent to the target*, so when our builders die our heal rate collapses (990 HP absorbed vs
their 1,577) while theirs does not.

And our collar dies with them: **our barriers 12.9 built / 8.7 destroyed (67%)** against
**theirs 11.6 / 1.9 (16%)**. `raid.py`'s thesis — *"sealed, the defender's heal rate is ZERO and
every point of damage becomes permanent"* — **is exactly the thing that fails here. The seal
never holds, so their heal rate is never zero, so no damage is ever permanent.**

---

## 5. ⭐ OUT-OF-SAMPLE REPLICATION — 111 unrated games, six kladde versions, eight of ours

Pre-clock2 only (§1.2). Matched control = unrated games against **other** opponents on the same
days and with the same `ourver` values, n = 1,910.

| cell | n | share | med turns | fwd sent /100r | replant % | our HP lost /100r | their HP lost /100r | exch. | our builder death % | their builder death % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **kladde, all pre-clock2 versions** | **111** | **0.324** | 259 | **2.79** | **61%** | **547** | **92** | **5.9** | **69%** | **14%** |
| … kladde v80 (08-08) | 5 | 0.000 | 288 | 0.22 | 0% | 404 | 153 | 2.6 | 48% | 32% |
| … kladde v86 (08-10/11) | 40 | 0.400 | 270 | 3.10 | 64% | 533 | 105 | 5.1 | 69% | 21% |
| … kladde v87 | 15 | 0.200 | 351 | 2.94 | 77% | 491 | 53 | 9.3 | 78% | 12% |
| … kladde v90 | 5 | 0.200 | 241 | 5.45 | 66% | 867 | 44 | 19.8 | 69% | 3% |
| … kladde v91 | 10 | 0.000 | 260 | 2.34 | 55% | 710 | 9 | 75.4 | 77% | 5% |
| … kladde v97 (08-14) | 36 | 0.444 | 194 | 2.37 | 43% | 525 | 130 | 4.0 | 62% | 3% |
| **matched control (other opponents)** | **1,910** | **0.485** | 170 | **1.11** | **45%** | **236** | **163** | **1.4** | **23%** | **23%** |

```
share: kladde 36/111 = 0.324  vs  control 927/1910 = 0.485
  clusters: MATCH live both sides (5 games/match); OPPONENT dead for kladde, live for control
  hw95 = 1.96*sqrt( p̄(1-p̄) * (1.434/111 + 1.833/1910) ) = 0.1153
  difference = -0.1610   ->  EXCLUDES ZERO
```

**Every one of the six signatures replicates**: replant rate, forward-plant volume, our HP-loss
rate, their HP-loss rate, the exchange ratio, and the builder-death asymmetry. Across **six
kladde builds spanning 2026-08-08 → 2026-08-14** and **eight of our builds (v85, v104, v112, v125,
v136, v138, v140, v141, v143)**.

⇒ **Kladde is not a v119 counter and this is not a today artefact. It is a persistent structural
matchup that has survived seventeen of their ships and eight of ours.** Combined rated + unrated
lifetime record against them: **27/80 rated + 36/111 unrated = 63/191 = 0.330.**

**⚠ Caveats that bind:** the unrated pool mixes our prototypes with our shipped bots (that is
what `unrated` is), and the per-version cells at n=5–15 are decorative on their own. The
load-bearing statement is the **pooled 111 vs 1,910 contrast**, not any single row.

---

## 6. WHAT I EXPECTED AND GOT WRONG

**S8, stated before the cell was run, and refuted by it.** I predicted the plant sites would sit
in a *blind band*: a builder sees r² = 20, a sentinel shoots r² = 32 and ignores obstacles, so I
expected many plants to be inside a ray whose shooter the raider could not see — which would have
made any vision-based avoidance model structurally useless.

```
Nearest LIVE enemy sentinel at the moment we plant a forward sentinel (r300+ games):
                        <=20 (visible)   21-32 (BLIND BAND)   >32   none alive
  A kladde   n=187          95%                 1%             1%       3%
  B rush     n= 34          41%                15%            15%      29%
  C 08-16    n= 27          26%                 0%             7%      67%
  C15 08-15  n=213          51%                 1%            13%      35%
```

**Refuted. 95% of our kladde plants have a live enemy sentinel within builder vision.** The
information needed to refuse the site is *available* and we do not look at it. This makes
`QUEUE.md #32`'s proposed remedy (refuse a build site inside the union of their rays) **better
supported than it was**, and it kills my own cuter hypothesis. Recorded here rather than dropped.

**A second surprise, characterisation not check** (I could not have stated an expectation): the
plants are not spread thinly over a hostile band. They are **concentrated on one tile per game**
— 8 distinct tiles for 60 plants on icefloe, 3 for 29 on drakkarfjord. Whatever `can_fire_from`
plus `can_build_sentinel` selects, it is deterministic enough to return the same answer fifty
times in a row.

---

## 7. THE CODE PATH, READ

`bots/_v223sealrepair/raid.py:636 _try_forward_sentinel`. Gates, in order:

```
LOKI_FWD_SENTINEL_ON            True
live cap                        LOKI2B_LIVE_CAP_ON=True -> _live_fwd_guns() counts LIVE friendly
                                sentinels within d^2<=50 of the enemy core; refuse if >= 3
harvester prerequisite          SLOT_HARVESTERS >= 2
bank floor                      resources >= sentinel_cost + 40
proximity                       raider within d^2 50 of a core tile
site choice                     for each of 4 cardinal neighbours, for each core tile:
                                  can_fire_from(bp, facing, SENTINEL, target) and
                                  can_build_sentinel(bp, facing)  ->  BUILD, return
```

**There is no attrition term anywhere in it.** No memory of previous plants, no count of losses,
no per-tile record. `LOKI_FWD_GUN_CAP = 3` is now a **live census**: `doctrine.py:1236-1258`
documents that the old `SLOT_FWD_GUN` monotone counter was a bug (*"Three destroyed turrets close
the forward-sentinel arm PERMANENTLY"*) and LOKI-2b replaced it with a count of what is alive.

**That fix is correct and it created the opposite failure.** A cap on *simultaneously alive*
turrets, applied to turrets that die in 6 rounds, frees itself every 6 rounds forever. The
observed replant gap is **9 rounds** — the cap plus one build cycle. **The tree now has no brake
of any kind in this path, and the doctrine block that removed the old one anticipated only the
lockout failure, not the runaway one.**

For contrast, the raid-station scorer *does* have exactly the mechanism this path lacks:
`self.raid_ban` (`main.py:87`, written at `raid.py:179,223`, read at `raid.py:784`) — a
tile-keyed dict with round expiry. **The pattern exists in the tree, twenty lines away, and is
not applied to the build site.**

⚠ **Feasibility constraint the builder must price:** the comments at `main.py:95,101` say the raid
state is **per unit**, and our raiders die at 72–80% against kladde, so an instance-dict memory
partly dies with its owner. All 16 store slots are allocated (`doctrine.py:931-961` + the
LOKI re-pointings at `:1184-1188`), so a team-wide memory needs a repack, not a free slot.
`pack_pos` (`eco.py:87`) already packs a tile into an int.

---

## 8. LIMITS

* **n is small on the rated side.** A = 15 games / 3 matches; A′ = 5 games / 1 match; the r300+
  restriction cuts A to 9. Nothing here is a share claim at that n — the share claim is the
  111-vs-1,910 unrated contrast in §5, and even that pools six of their versions.
* **Us-only.** Every figure is OpenSverige's own record against kladde. None of it says anything
  about how the rest of the league fares against them. *(I did not compute kladde's league-wide
  `S − E` from `league_matches.tsv`: the brief itself notes that instrument is centred at zero by
  construction and is blind to an us-specific counter — and §5 has already answered the "is v119
  new?" question directly and negatively, across six of their versions.)*
* **The damage ledger is a model**, not a measurement: shot type is inferred from the ammo
  identity, heals are counted at +4 with no overheal correction, and entity HP is nominal max.
  Control S9 shows it closes; it does not show every term is individually right.
* **All 25 unrated kladde v119 games of today were excluded** as live-leg cells and were not read.
* **Enemy target-priority is untested** and would produce part of the same signature.
* **No verdict, no bar, no ship claim.** Attribution and bars are the builder's.

---

*Research arm, read-only, 2026-08-16T08:30:49Z. One file written; one QUEUE row appended.*
