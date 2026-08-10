# THE LEAGUE-WIDE FAST-KILL MECHANISM — and it reduces to one number

**Side lane, 2026-08-10 06:1x CEST.** Opus subagent, read-only, on the decoded
corpus. **No verdicts and no planks here** — planks are the builder's, mechanism
follow-up is the research arm's. This banks a measurement before the session that
produced it ends.

**Population: 9,874 attributed replays** — **7,421 THIRD-PARTY** (we are absent),
2,453 ours, 160 related (excluded after §A). 71 distinct teams. Archive
`manifest.json` git_sha `3a60dd1`, built 2026-08-10T04:00:29Z.

## THE INSTRUMENT WAS VALIDATED IN BOTH DIRECTIONS BEFORE ANY UNKNOWN CELL

- **Published cell reproduced to the digit:** `core-kill-incidence-cut-2026-08-09.md`'s
  *"827 core-kill wins, median r151, 74.4% inside r250"* → **827, median 151,
  74.365%** on the first 2,715 rows of `ladder_games.tsv`.
- **Both branches shown able to fire:** of 1,855 ladder-joined replays, **1,362/1,362**
  `core_destroyed` games have a core-death event and **the 493 non-kill games have
  zero** — a check that can come out the other way. `platform turns == replay_round + 1`
  in 1,362/1,362, so all rounds below are on the platform convention.
- **Side mapping discriminates:** in-replay team index 0 == side A predicts the
  platform winner side **7,287/7,287 = 100.0%**; the reversed hypothesis gives 0%.
- **A FAILED reproduction, reported rather than buried:** the same doc's *"earliest
  core kill anywhere is round 61"* does **not** reproduce — `join.tsv` sorts by
  filename, not append order. Today's earliest is **r44**, and `ladder_games.tsv`
  already held 19 kills faster than r61. A population difference, not an
  instrument failure, but **that doc's "zero survival censoring at T=50" defence
  is weaker than stated.**

---

## 1. THE MECHANISM IS ONE NUMBER: d²(TURRET → ENEMY CORE)

Median squared distance from the planted turret to the **enemy** core, over all
sub-100 kills:

| killer | n≤100 | builds/game before the kill | d²(sentinel→core) | d²(gunner→core) |
|---|---:|---|---:|---:|
| Cookie | 58 | **buil4.0 sent2.3 harv1.1 conv0.4** | **8** | — |
| Prompt Engineers Anon. | 45 | **buil5.0 gunn3.1 — nothing else at all** | — | **10** |
| Banminary | 75 | conv6.6 buil2.6 sent2.5 harv1.8 laun0.9 | 25 | 4 |
| Mimercraft | 36 | conv6.1 sent3.0 buil2.7 harv1.3 | 17 | 7 |
| The Bisons | 54 | conv11.2 buil3.9 sent3.4 harv2.9 | 25 | 9 |
| Team 48 | 63 | conv9.4 buil4.0 gunn3.9 harv2.8 | — | 10 |
| Powered by SmartFridge | 104 | conv16.9 gunn3.6 buil3.4 harv3.3 | 25 | **8** |
| SingleCore | 26 | conv11.7 buil4.0 harv2.9 sent2.3 | 25 | 13 |
| **OpenSverige (us)** | **155** | conv17.7 buil5.1 harv3.2 sent1.3 gunn0.6 | **32** | **16** |

**Sentinel range is r²=32; gunner range is r²=13.** The fast killers plant
*inside* range — Cookie at d²=8 is 2.8 tiles from the core. **We plant at d²=32,
exactly at the sentinel's edge, and at d²=16 on gunners.**

> **THE SINGLE HIGHEST-VALUE THING TO CHECK, flagged as a lead and NOT asserted:**
> **d²=16 is outside gunner range (r²=13).** If that median is right, the typical
> forward gunner we build cannot reach the core it was built to shoot. It is a
> median, so half our plants are further still. **This wants an engine/replay
> confirmation before anyone builds on it** — it is exactly the kind of number
> that is true of one measurement and not of the bot. Engine probes are the
> builder's.

**Why "inside range" is the whole trick, arithmetically:** 3 sentinels × 18 dmg ×
1 shot per 2 rounds = **27 dmg/round → a 500 HP core in ~19 rounds of fire**, at
10 ammo/shot ≈ **280 Ti of ammunition, inside the 500 Ti starting bank.**
**Nothing else has to be built.**

**LAUNCHER THROWS ARE NOT THE MECHANISM.** Cookie (58 sub-100 kills), The Bisons
(56), Big O (52) and Prompt Engineers Anonymous (45) have **zero** throws in the
corpus — and they appear in `throws.tsv` (4,599 files covered), so that is a
covered zero, not missing data. **A builder bot walks and plants.**

## 2. TWO TEAMS KILL FAST WITH NO ECONOMY WHATSOEVER

**Prompt Engineers Anonymous: `buil5.0 gunn3.1` and nothing else, ever** — no
conveyor, no harvester, in 45 sub-100 kill games. **Cookie: `buil4.0 sent2.3`,
0.4 conveyors/game.** Under `R1000_IS_DEFEAT: yes` these are the existence proof
that the economic plank can be abandoned outright rather than merely demoted.

For contrast, our own profile is **conv17.7 buil5.1 harv3.2** — we build the most
economy of any bot in the table and plant the furthest out.

## 3. THE FAST KILLERS ARE DETERMINISTIC — AND THAT IS THE DIRTY TRICK

§C rows 16/17 and 18/19 are **distinct files, distinct md5s, distinct match ids,
hours apart** — with **identical build order and identical kill round.** The same
matchup on the same map replays byte-for-byte.

**A rush is a scripted opening, and a scripted opening is pre-emptable.** The
plant tile is knowable in advance; a barrier costs **3 Ti** and walls cannot be
built on. This is the "play the players" mandate with a measured target list
rather than a hypothesis. **Banminary alone owns 14 of the 25 fastest kills in
the corpus**, with a near-invariant signature: **3 sentinels + 1 builder + 1
launcher + 1 gunner, zero-to-negligible conveyors, no harvesters, done by r29–39.**

## 4. WHO RUSHES, AND WHO ONLY GRINDS (third-party only, denominators = that team's games)

| team | games | ≤250 | **≤100** |
|---|---:|---:|---:|
| Team 48 | 110 | 44.5% | **36.4%** |
| Banminary | 185 | 34.6% | **33.0%** |
| SingleCore | 85 | 34.1% | **29.4%** |
| The Bisons | 135 | 37.0% | **28.9%** |
| Cookie | 210 | 40.5% | **27.6%** |
| Big O | 185 | 41.6% | **26.5%** |
| *— grinders —* | | | |
| The Flotte Experience | 265 | 40.8% | **0.4%** |
| Pantheon | 385 | 38.4% | **1.6%** |
| **OpenSverige (all eras)** | 2,453 | 25.1% | **6.3%** |

**League median sub-250 kill rate = 20.0%** (71 teams, ≥40 games). **≤250 and
≤100 are nearly orthogonal:** Flotte/Pantheon kill 38–41% inside r250 and almost
never before r100. **Eight teams have ZERO sub-250 kills across 145–245 games
each** — fast-kill capability is concentrated in ~12 of 71 teams.

## 5. FRAGILITY vs MATCHUP — cleanly separable, and it names live-unrated targets

| victim | games | lost ≤250 | **distinct killers / opponents faced** |
|---|---:|---:|---|
| gsxWins | 275 | 37.8% | **19 / 19** |
| Banminary | 285 | 37.2% | **18 / 18** |
| kladde chatte tville… | 445 | 26.1% | **26 / 27** |
| Powerpuff Girls | 531 | 27.7% | **24 / 28** |
| TKB | 245 | 21.6% | **4 / 11 — 89% is Cookie alone** |
| 1337 | 160 | 21.9% | 7 / 16 — 51% Prompt Engineers Anon. |
| Team 48 | 245 | 42.0% | 9 / 13 — **70% is us** |
| **OpenSverige (us)** | 2,453 | **20.2%** | **38 / 43** |

**Structurally fragile** (dies fast to nearly everyone who tries): gsxWins,
Banminary, kladde chatte tville, Powerpuff Girls. **Pure matchups** (one bot's key
fitting one lock): TKB/Cookie, 1337/PEA, Team 48/us. **We are middling-fragile and
it is spread, not a matchup** — 38 of 43 opponents have killed our core inside
r250, none accounting for more than 8%.

Note **Banminary is simultaneously the corpus's most prolific fast killer and one
of its most fragile victims** — all-in rush with no defence.

## 6. MAP AREA IS A NULL; MAP IDENTITY IS A 3× EFFECT

| area band | games | ≤250 | ≤100 |
|---|---:|---:|---:|
| ≤200 | 1,270 | 40.7% | 9.2% |
| 201–400 | 3,279 | 43.5% | 10.7% |
| 401–550 | 669 | 45.6% | 11.2% |
| >550 | 4,656 | 43.3% | 11.1% |

**A 4× area range moves sub-250 by 5 points and sub-100 by 2 — and larger maps
are marginally FASTER.** This is the opposite of "small map = rush map".
**It also independently corroborates this lane's `AUDIT-baseline-read` finding
that kill turn does not track map size**, on 9,874 games rather than 25.

But map **identity** is large, and it survives a time control (2026-08-04…08-06
overlap window only): MAIN pool 565 games **7.3%** sub-100 vs ROTATIONAL pool 770
games **20.8%** — **~3× on sub-100, only ~1.1× on sub-250.** Geometry changes *how
fast* a kill lands, barely *whether* one lands. **This also explains away the
apparent league-wide decline in sub-100 killing: it is the rotational pool leaving
the schedule, not the field slowing down.**

Suppressors: **vase** (20.5%/2.3%), **saga** (33.9%/5.4%), **heart** (35.6%/2.7%).
Rush maps in the current main pool: atoll 8.3%, snowflake 7.9%, hive 6.6%,
fjordgate 6.5%.

## 7. SURPRISES, recorded before being explained away

1. **Our archive is NOT biased on kill timing** — third-party 71.6% kill / r212
   median / 10.7% sub-100 versus ours 76.0% / r205 / **10.7%**. The us-sample trap
   does not bite on this question, which is unusual enough to record.
2. **Map area null, map identity 3×** — whatever makes a rush map is not size.
   Core separation, wall channels or ore placement, none of which the corpus
   stores per map.
3. **A LEAD, EXPLICITLY NOT A FINDING (n=310, one version, selected opponents):**
   in the v102 era opponents kill our core inside r100 in **38/310 = 12.3%** vs
   **70/2,143 = 3.3%** in the Eir era — **but this is confounded on purpose**,
   because the v102 unrated pool was deliberately loaded with rushers (Bisons 12
   of the 38, Banminary 9). The uncofounded half: **our own sub-100 rate fell
   6.7% → 3.5%** while sub-250 rose 23.3% → 37.7%. **v102 traded rush for grind,
   in a field where a third of the top killers rush.**

## 8. INSTRUMENT GAP TO FILE (builder-owned, `tools/`)

**`meta_join.tsv` has no `map` column**, and `events.tsv` stores only `mw`/`mh`,
which are ambiguous — (26,26) is archipelago *or* snowflake *or* aurora; (16,16)
is jackpot *or* lighthouse *or* crossfire. §6's named-map cut therefore runs on
3,705 six-team games instead of 9,874. `league_games.py` already fetches map name
for the teams it covers; **adding `map` to `meta_attrib.py` unlocks map cuts on
all 10k files.**
