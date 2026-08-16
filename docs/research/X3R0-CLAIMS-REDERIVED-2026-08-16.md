# x3r0's two corpus claims, re-derived on OUR decoded corpus

**Research arm, s45, 2026-08-16. Clock: analysis run `2026-08-16T12:09Z`–`12:26Z`
(`date -u`), repo at `aea8835e`, corpus `manifest.json` `built_utc
2026-08-16T09:26:55Z` over `archive_replays = 53,227`.**

Read-only exercise. No bot, `PROGRAMME.md`, `HANDOVER.md`, `results.tsv` or
`QUEUE.md` was touched. Nothing here is a verdict; it is a measurement and a
prioritisation claim.

---

## 0. What was being checked, and why it needed checking

Our current ladder holder **v152** is our chassis plus a patch by **x3r0**. The
patch's stated evidence is in `bots/_x3r0v152/doctrine.py:1720-1770`
(the `LOKI-TURBO4` block) and rests on two corpus figures produced by
**instruments that do not exist in this repo** (`loki_analysis.md`,
`turbo_identity.py`; the directory he cites, `replays/ladder_ours/`, is also
absent — `ls` returns nothing). His population is stated in his own text:
**35 v151 ladder games.**

> **CLAIM A.** *"Corpus: 1,056 rounds across the 35 games holding >= 10 ammo
> with NO live turret (worst hold 60)."*
>
> **CLAIM B.** *"Corpus: 1,251 of 5,150 damaged-core rounds (24%) had a free
> heal seat, >= 1 Ti banked and one of our builders within d^2 <= 25 of the
> Core, with nobody standing on a seat."*

**The mechanisms are verified here** (the ghost-magazine path and the
`heal_seats` geometry are both readable in the shipped source). **The
magnitudes were not.** This document measures both on our own corpus.

**These are not reproduction attempts.** We do not have his 35 files or his
code. We restate each claim as a quantity our tapes can carry, define it, and
measure it — and we do it against a control that must come out the other way.

---

## 1. Why the corpus tapes could not answer this, and what was built instead

**Neither claim is answerable from `corpus/*.tsv`,** and the missing columns are
specific:

| need | tape | verdict |
| --- | --- | --- |
| per-round team **ammo balance** | `econ.tsv` has `ammo_end` and `ammo_converted` **per file × team × round-BAND** (4 bands) | **too coarse** — a claim counted in ROUNDS cannot be built from 4 band aggregates |
| per-round **living turret count** | `builds.tsv`/`events.tsv` carry the build event; `removeEntity` is not in any tape | **absent** — no death stream, so "alive now" is not derivable |
| per-round **core HP** | nothing | **absent** (`corpus-howto.md`: *"per-round titanium, ammo balances and cooldowns are in `updatePlayers` but are not extracted here"*) |
| per-round **builder positions** | `throws.tsv` has throw endpoints only, and is a known trap (INSERT-only outcomes, no version column) | **absent** |

⇒ A decoder was written for this question
(`tools/x3r0_measure.py` — ⭐ **RECOVERED AND COMMITTED 2026-08-16 ~12:0xZ by the research lane: it was written to the SESSION scratchpad, which DIES WITH THE SESSION. A published finding whose instrument evaporates is unreproducible by construction, and this doc's own numbers rest on it. 349 lines, now in `tools/`, with the pre-declared expectation cells at `docs/research/X3R0-EXPECTATIONS-2026-08-16.md` so a successor can check what was predicted BEFORE the read.** The original citation honestly said 'not committed'; the defect is that saying so does not preserve it — it reads
`updatePlayers` field 7 for ammo, field 1 for titanium; `placeEntity`/
`removeEntity` for the live-entity set; `updateHp` for core HP; `builderHeal`
for heals; `coreConvertAmmo` for conversions). Schema per
`tools/replay_schema.md`. The known decoder traps were respected: rotation
re-emits are deduplicated on entity id, and `updateHp.delta` is read as a
**64-bit two's-complement** varint.

---

## 2. Population and enumeration rule — stated in full, because a count is only as wide as its enumeration

**Rule.** Every row of `corpus/meta_join.tsv` where `teamAName` or `teamBName`
is literally `OpenSverige`, whose `file` exists in `replay_archive/`. **10,231
of 10,231 such rows had their replay on disk; 0 were dropped; 0 decode errors,
0 skips** (`grep ERR|SKIP` over all worker stderr = 0). One row per game, two
sides decoded per game ⇒ **20,462 side-rows.**

* **Surface split**, by joining `match` against the two authoritative tapes:
  **RATED = 4,185 games** (match id in `ladder_games.tsv`),
  **UNRATED = 6,046 games** (match id in `unrated_games.tsv`). No row fell
  outside those two sets. `meta_join` is used here **only for seat and version
  attribution, never as a rated denominator** — the rated denominator is
  `ladder_games.tsv`, per the standing rule.
* **Time window:** `completedAt` from **2026-08-07T11:31:55Z** to
  **2026-08-16T09:19:42Z** (10,231 of 10,231 rows carry a timestamp).
* **Our versions present:** 76 distinct, headed by v104 (1,795 games),
  v125 (1,310), v140 (1,143), v102 (650), **v152 (305)**, **v151 (55)**.
* **Opponents:** 58 distinct, top six SmartFridge 630, Leviathan 585,
  gsxWins 485, 0033 471, Lunds Stallions 457, The Bisons 445.

**Seat attribution is independent of `winnerSide`.** TRAP 7 warns that
`join.our_team`, `meta_join.us_side` and `ladder_games.won` all descend from
`winnerSide`. This cut derives our seat from the **team NAME** on the A/B side,
which does not. Cross-check against `join.our_team`: **4,185 of 4,185 agree, 0
mismatches** — so the winner-derived seat happens to be right on this
population, and this cut does not depend on it either way.

---

## 3. Operational definitions

Every quantity is evaluated on the **end-of-round state** of round *r*, for
*rounds 0…N−1* of the replay (`turns[i]` IS round `i`).

### CLAIM A — "holding ammo with no live turret"

* **holding ammo** = the team's `Player.ammo` after the last `updatePlayers` of
  that round is **≥ 10** (x3r0's own threshold). A looser `> 0` form is
  reported alongside.
* **no live turret** = **zero living GUNNERs and zero living SENTINELs** of that
  team. **Launchers are excluded** — they consume no ammunition, so a launcher
  cannot make held ammo useful.
* **Denominator = ammo-holding rounds** (rounds with ammo ≥ 10), not all rounds.
  The all-rounds form is also reported, since a rate needs its denominator named.
* Split, added because it changes the plank: **BEFORE the team's first turret is
  ever built** (banking ahead of a gun — arguably intentional) vs **AFTER every
  turret it built has died** (x3r0's ghost magazine — pure waste).

### CLAIM B — "a damaged-core round with an empty heal seat"

* **damaged-core round** = that team's core is **alive** and its HP is
  **< 500** (`CORE_MAX_HP`) at end of round. HP is tracked from 500 through
  every signed `updateHp` delta addressed to the core's id.
* **heal seats** = the **8 orthogonal neighbours of the 2×2 core footprint**,
  in-bounds — byte-for-byte the set `bots/_x3r0v152/eco.py:271 heal_seats()`
  computes, i.e. exactly the tiles a builder may heal the core from.
* **a seat is FREE** = in-bounds, terrain ≠ WALL, and no building **and** no
  builder bot of **either** team standing on it.
* **`x3r0 cell`** — his full conjunction, reproduced term for term:
  *(≥1 free seat) AND (team titanium ≥ 1) AND (a friendly builder within
  d² ≤ 25 of the core anchor) AND (no friendly builder standing on ANY seat).*
* Two weaker readings are reported separately because **the phrase "an empty
  heal seat" is ambiguous and the two readings differ by 6×**:
  **(i) no friendly builder on ANY seat** (no hand available to heal) and
  **(ii) at least one seat free and standable** (the literal reading).
* **`no heal landed`** = no `builderHeal` from that team targeted a core
  footprint tile that round. This is the outcome the seat is a proxy for.

---

## 4. Instrument controls — each one had to be able to come out the other way

| # | control | result |
| --- | --- | --- |
| **C1** | core HP must never exceed 500; a sign error in the two's-complement decode shows up here | **0 of 20,462 side-rows** have any round with HP > 500 |
| **C2** | `ammo≥10 & 0 turrets` + `ammo≥10 & ≥1 turret` must **partition** the ammo-holding rounds | **0 violations / 20,462** (loose `>0` form: 0 violations) |
| **C3** | `no-seat-bot` + `seat-bot` must partition damaged-core rounds | **0 violations / 20,462** |
| **C4** | HP tracker must **discriminate**: our final core HP in games we LOST vs WON | **54.3 (n=5,227) vs 439.2 (n=5,004)**; mirror on their side **49.0 vs 425.3**. A stuck tracker would read 500/500 |
| **C5** | entity-id **resurrection** would silently hide a rebuilt turret and inflate Claim A | **0 of 50,068 placeEntity events across 400 randomly-sampled replays** place an id that had been removed |
| **C6** | negative: games where we built **0 turrets ever** must show `ammo≥10 & ≥1 turret` = **0** | **250 such games, sum = 0.** Positive arm: the other 9,981 games sum to 1,658,545 |
| **C7** | the heal detector must fire: US core-heal rounds must be > 0 | **935,734 rounds, in 7,395 of 10,231 games** |
| **C8** | seat derivation independent of `winnerSide` (TRAP 7) | **4,185/4,185 agree with `join.our_team`, 0 mismatches** |

**The THEM side of every game is carried through the whole analysis as the
substantive control** — same decoder, same rounds, same maps, opposite team.
It comes out **materially different on both claims** (§5, §6), so neither cell
is a constant column.

**Interval method.** Games are not independent. Rather than import the
project's DEFF constants — they were measured on a **per-game win indicator**,
not on a round-level rate — clustering is measured directly here by a
**cluster bootstrap (1,000 resamples)**. Both live clusters were enumerated:
**MATCH** (5 games share a match; the stratum holds all 5 ⇒ live) and
**OPPONENT** (a stratum holds many matches vs one opponent ⇒ live). Intervals
are given **both ways**; the opponent-clustered one is the conservative
reading, and with only 58 opponents it is 4-8× wider. **Quote the
opponent-clustered interval when the claim is about the field.**

---

## 5. CLAIM A — **REPLICATES as a phenomenon; the magnitude is ours, not his; the ECONOMIC cost is small and we are NOT worse than the field**

### 5.1 The rate

**Population: our 10,231 games, 2026-08-07 → 2026-08-16, 58 opponents.**

| cut | idle rounds / ammo-holding rounds | rate | 95% CI (match-clust.) | 95% CI (opponent-clust.) |
| --- | --- | --- | --- | --- |
| **US, all** | 763,160 / 2,421,705 | **31.51%** | [30.22, 32.85] | **[26.73, 36.70]** |
| US, RATED (4,185 games) | 372,531 / 1,172,606 | 31.77% | [29.76, 33.76] | — |
| US, UNRATED (6,046 games) | 390,629 / 1,249,099 | 31.27% | [29.65, 32.88] | — |
| **THEM, all (CONTROL)** | 445,857 / 2,116,208 | **21.07%** | [19.86, 22.34] | — |
| THEM, RATED | 196,997 / 1,011,586 | 19.47% | [17.65, 21.53] | — |

**PREDICTION HELD.** It was declared before the run
(`scratchpad/EXPECTATIONS.md`, items 1-3) that the US share would land 20-50%
and that **US > THEM**. Both held: 31.5% vs 21.1%, and the two surfaces agree
to within half a point.

**On his headline number.** 1,056 rounds is a **count**, and a count carries its
population. Ours is 763,160 idle rounds — **722× his**, over **292× his games.**
Per game: **74.6 for us against his 30.2.** On **v151 alone** — his own bot
version, 55 games in our corpus — we count **2,676** idle rounds (48.7/game);
restricting to **v151 RATED only (30 games)** gives **1,530**, of which **336**
are strictly *after every turret died*. **His 1,056 sits inside that bracket,**
so his figure is consistent with ours under a definition somewhere between the
two — but his 35 files are not ours and this is not a reproduction.

### 5.2 The split that changes the plank

| cut | idle rounds | BEFORE first turret | AFTER all turrets died |
| --- | --- | --- | --- |
| US all | 763,160 | 251,921 (33.0%) | **511,239 (67.0%)** |
| US rated | 372,531 | 84,754 (22.8%) | **287,777 (77.2%)** |
| **THEM (CONTROL)** | 445,857 | **236,409 (53.0%)** | 209,448 (47.0%) |

**Two-thirds of our idle rounds are the ghost-magazine case** (a gun existed, it
died, the magazine stayed), against **47% for the field**. His diagnosis of the
*mechanism* is supported by our corpus: **we are more post-mortem than the field
is, and the field is more pre-emptive.**

### 5.3 ⚠ THE SURPRISE — the rate says we are worse, the CURRENCY says we are not

Flagged before explaining: **the two metrics disagree in direction.**

| | US | THEM |
| --- | --- | --- |
| idle **rate** | **31.5%** (worse) | 21.1% |
| Ti converted to ammo while **zero turrets alive** | **30.8 Ti/game** (better) | **45.8 Ti/game** |
| the same as a **share of all our ammo conversion** | **5.29%** | **5.03%** |
| total ammo conversion | 581 Ti/game | 910 Ti/game |

**Ranked on titanium — which is what the game pays in — we waste 33% LESS per
game than the field, and the SHARE of conversion wasted is a statistical tie
(5.29% vs 5.03%).** The rate gap exists mostly because the field converts far
more overall, so its idle balance is a smaller fraction of a bigger habit.

**The distribution is extremely skewed and the mean is not the story.**
Per-game titanium converted with zero turrets alive: **median 24 · p90 56 ·
p99 180 · max 1,419**; only **202 of 10,231 games (2.0%)** exceed 100 Ti. The
worst single case in the corpus is
`1b24e13c-dea9-4070-940b-ed3d0f9a3dc4_game_4` — an r1000 game where we converted
**7,804 Ti**, built 3 turrets, and at peak held **7,300 ammunition with every
turret dead.** **That is x3r0's mechanism at full extension and it is real.**

**⇒ VERDICT ON A: the phenomenon is confirmed on our corpus and its mechanism
is confirmed. Its VALUE is a 2%-of-games tail, not a 31%-of-rounds body.** A
brake that only trims the median game recovers ~24 Ti; a brake that catches the
tail recovers hundreds. **T4's design — a magazine that has not FALLEN in 12
rounds — is aimed at the tail, which is the right target.**

### 5.4 Did the v152 patch move its own dial? ⚠ Observational, not a leg

| version | games | idle rate | Ti conv @ 0 turrets / game |
| --- | --- | --- | --- |
| v140 | 1,143 | 32.6% | 34.7 |
| v151 (pre-patch, his target) | 55 | 31.4% | 29.0 |
| **v152 (post-patch, holder)** | **305** | **31.1%** | **26.9** |
| v154 | 100 | 39.5% | 38.6 |

**The idle RATE did not move (31.4% → 31.1%).** The titanium figure moved a
little (29.0 → 26.9, −7%; −22% against v140's 34.7). ⛔ **This is a
version-to-version observational contrast across different opponents, eras and
map rotations — it is NOT a matched leg and cannot carry a verdict on the
patch.** It is a flag: **the patch's own target metric barely moved on the
surface where it now lives**, and someone should check that `T4_AMMO_IDLE_ON`
is firing at all before more is built on top of it.

---

## 6. CLAIM B — **CONTRADICTED at his magnitude on our corpus — and the same cell measures 20.8% on the FIELD, which is where the value is**

### 6.1 The cell, his definition, term for term

**Population: our 10,231 games; 1,100,957 US damaged-core rounds.**

| cut | x3r0 cell / damaged-core rounds | rate | 95% CI (match) | 95% CI (opponent) |
| --- | --- | --- | --- | --- |
| **US, all** | 87,946 / 1,100,957 | **7.99%** | [7.49, 8.55] | **[6.36, 9.84]** |
| US, RATED | 35,309 / 456,084 | 7.74% | [6.96, 8.62] | — |
| US, UNRATED | 52,637 / 644,873 | 8.16% | [7.56, 8.81] | — |
| **US, v151 only (his version, 55 games)** | 369 / 4,330 | **8.5%** | — | — |
| US, v152 (holder, 305 games) | 2,040 / 24,881 | 8.2% | — | — |
| **THEM, all (CONTROL)** | 288,686 / 1,388,853 | **20.79%** | [19.50, 22.12] | — |

**His figure is 24%. Ours is 8.0% overall and 8.5% on his own bot version.**
⇒ **CONTRADICTED — by a factor of ~2.8, and the disagreement survives on the
narrowest cut we can make toward his (v151, 55 games).**

**His denominator does not match ours either, and that is the likely
explanation:** he reports **5,150 damaged-core rounds over 35 games = 147/game**;
our v151 games read **4,330 over 55 = 78.7/game**. **His cut carries roughly
twice the core-bleed density of our v151 population** — consistent with a
subset selected around a loss (his worked example is a `core_destroyed` loss at
r96). A siege-heavy subsample would inflate exactly this cell. **It is a
population difference, not necessarily an error** — but the number is not
general, and it was used as though it were.

### 6.2 The two readings of "an empty heal seat" differ by 6×, and neither is 24%

| reading, US, all 1,100,957 damaged-core rounds | rate |
| --- | --- |
| **(i) no friendly builder on ANY of the 8 seats** ("no hand available") | **15.61%** [12.32, 19.80] opp-clust. |
| complement (a builder IS seated) — **CONTROL, must sum to 100%** | **84.39%** ✓ |
| **(ii) ≥1 seat free and standable** (the literal reading) | **90.32%** |
| a friendly builder within d² ≤ 25 of the core | 93.50% |
| team titanium ≥ 1 | 98.21% |

**PREDICTION PARTLY WRONG, recorded before the run.** Expectation 6 said the
no-hand reading would be **>50%**; it is **15.6%** — our bot staffs the seat far
better than predicted. Expectation 7 said the literal reading would be **LOW**
because our own seal fills the seats; it is **90.3%** — the smoke-sample game
that produced that guess was an outlier (an opponent had barrier-walled all
eight of our seats). **Both expectations were wrong in the direction of "we are
better at this than assumed", which is worth recording because it is the
direction that argues against building the plank.**

**The binding term in his conjunction is the seat-staffing one** (15.6%), not
titanium (98.2%) or proximity (93.5%) — so his cell is essentially
"no-hand-on-seat, minus the cases where no seat was free". Confirmed
arithmetically: 15.61% → 7.99%.

### 6.3 ⭐ THE CONTROL IS THE FINDING — his defect is a FIELD property, at his magnitude, and we are 2.6× better than the field at it

| all 10,231 games, both sides | US | THEM |
| --- | --- | --- |
| damaged-core rounds | 1,100,957 | 1,388,853 |
| **no friendly builder on ANY heal seat** | **15.6%** | **39.8%** |
| **NO heal landed on the bleeding core that round** | **21.0%** | **55.8%** |
| a heal DID land | **79.0%** | 44.2% |
| **x3r0 cell** | **8.0%** | **20.8%** |

**The field's number on x3r0's own cell is 20.8% — within touching distance of
his 24%.** He measured a real defect; our corpus says it is **mostly theirs**.

Seat-rounds during damaged-core rounds, by what occupies the seat:

| | free | our own building | a builder bot | wall / **enemy building** |
| --- | --- | --- | --- | --- |
| US (8,609,100 seat-rounds) | 44.4% | 26.1% | 18.7% | **10.8%** |
| THEM (10,703,800) | 30.3% | 32.1% | 12.7% | **25.0%** |

**Our raid layer is already denying their seats at more than twice the rate they
deny ours** (25.0% vs 10.8% — `bots/_x3r0v152/raid.py:105` runs `heal_seats` on
the ENEMY anchor, which is exactly this). The asymmetry in §6.3 is therefore
partly a thing we already cause.

### 6.4 A self-inflicted cost that has already been mostly paid

**26.1% of our own seat-rounds during a bleed are blocked by OUR OWN building.**
By version:

| version | games | own-building share of seat-rounds |
| --- | --- | --- |
| v102 | 650 | **43.7%** |
| v116 | 380 | 17.7% |
| v125 | 1,310 | 16.5% |
| v140 | 1,143 | 16.4% |
| v146 | 75 | **8.9%** |
| v151 | 55 | 15.7% |
| **v152** | **305** | **17.8%** |

`HS_SEAT_PROTECT_ON` / `HS_SEAT_BAN_CONVEYORS` already exist in the shipped
`eco.py` and the big win (43.7% → ~16%) happened between v102 and v116. **v152
is not the best version on this dial; v146 is, at 8.9%.** Worth one grep before
anyone re-invents seat protection.

---

## 7. What this suggests, and what it does not

**PLANK WE ALREADY HAVE (do not re-buy):** ammo-idle braking (`T4_AMMO_IDLE_*`
ships in v152), heal-seat protection from our own paving (`HS_SEAT_PROTECT_ON`),
enemy-seat denial (`raid.py` runs `heal_seats` on the enemy anchor). All three
are in the holder. §5.4 and §6.4 say the first has not visibly moved its dial
and the second is not at its own best-measured setting — those are **audits**,
not new planks.

**⭐ THE ONE THING HERE THAT IS NOT ALREADY A PLANK — and it comes from the
CONTROL, not from either claim:**

> **A BLEEDING ENEMY CORE GOES UNHEALED 2.7× AS OFTEN AS A BLEEDING CORE OF
> OURS.** Across 1,388,853 enemy damaged-core rounds
> (10,231 games, 58 opponents, 2026-08-07→16), **55.8% saw no heal land on the
> bleeding core**, against **21.0%** of our own 1,100,957. **They leave no
> builder on any heal seat in 39.8% of those rounds, against our 15.6%.**

If that holds up as a *causal* statement it prices a real doctrinal choice:
**sustained chip damage on the enemy core is far more durable than symmetric
reasoning assumes, and burst is worth less than it looks** — an enemy core taken
to 60% tends to STAY there, while ours gets healed back. It bears directly on
`R1000_IS_DEFEAT` and on whether a raid should peck-and-hold or wait to
alpha-strike.

⛔ **THREE REASONS IT IS A HYPOTHESIS AND NOT A ROAD.**
1. **It is observational and confounded by us.** We deny 25.0% of their seats
   against their 10.8% of ours; part of the 55.8% is our own seal, not their
   incompetence, and this cut cannot separate them.
2. **Per point 6 of the standing directive, a road opens or closes on live-game
   evidence.** The discriminating test is cheap and is an unrated leg: pin an
   opponent, run a chip arm against a burst arm, and read **core-HP recovery
   after damage** off the replay — the decoder for that already exists in this
   session's scratchpad and can be committed if the leg is called.
3. **Run `tools/target_value.py` first.** No target band was computed for this
   and the standing rule is that the number is written down before the work.

**AND ONE MORE, smaller:** the smoke sample turned up an opponent (`Juusto`,
v11) who had **barrier-sealed all eight of our heal seats** by end of game
(`003ef20d…_game_1`). That is our own LOKI-1 doctrine being used against us. It
is a single game and is recorded as an observation, not a rate.

---

## 8. Verdict table

| claim | our operational form | our number (population) | supported? |
| --- | --- | --- | --- |
| **A** "1,056 rounds holding ammo with no live turret" (35 games) | rounds with team ammo ≥ 10 and zero living gunner+sentinel, over ammo-holding rounds | **763,160 / 2,421,705 = 31.51%** [26.73, 36.70] opp-clustered; 74.6 idle rounds/game — **10,231 games, rated+unrated, 2026-08-07→16, 58 opponents** | **SUPPORTED as a phenomenon and as a mechanism** (67% of it is post-turret-death). ⚠ **Its VALUE is not: 30.8 Ti/game, 5.29% of our conversion, and the field is WORSE in titanium (45.8 Ti/game). Tail-driven — 2.0% of games exceed 100 Ti, max 1,419.** |
| **B** "24% of damaged-core rounds had an empty heal seat" (35 games) | his exact conjunction: ≥1 free seat AND Ti ≥ 1 AND a builder within d²≤25 AND nobody on a seat, over damaged-core rounds | **87,946 / 1,100,957 = 7.99%** [6.36, 9.84] opp-clustered; **8.5% on v151 alone**, his own version — same population as above | **CONTRADICTED at his magnitude (~2.8× lower).** His damaged-round density is 2× ours (147/game vs 78.7), consistent with a siege-selected subset. **⭐ The same cell reads 20.79% on the FIELD — his number describes our OPPONENTS, not us.** |

**Neither claim was wrong about a mechanism. Claim A's mechanism is real and its
price is small except in a 2% tail. Claim B's number does not survive contact
with our population — and its control is worth more than the claim was.**
