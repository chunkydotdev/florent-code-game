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

> # ⚠ HEADLINE CORRECTED BY THE RESEARCH ARM'S AUTOPSY (`be497c6`) — READ THIS FIRST
>
> **My framing below — "fast killers plant INSIDE range, we plant at the edge" —
> is WRONG IN DIRECTION for sentinels, and the truth is a better trick.** Research
> instrumented every Bisons sentinel in all five games (`bisons-fast-kill-autopsy-2026-08-10.md`):
>
> **They plant at MAXIMUM STANDOFF, on a cardinal line.** Chebyshev distance to
> our core is *"only ever 5, 4 or 2 — never 1, never 3, never diagonal"*, **modal
> placement Chebyshev 5** — the furthest tile from which a sentinel can still
> connect. Our own sentinels in those same games sit at **Chebyshev 1 and 2**.
> **They stand further away than we do, not closer.**
>
> **And max standoff is the whole point, because it buys INVULNERABILITY:** a
> sentinel's line shot **ignores obstacles** and reaches r²=32, while a builder
> bot's attack requires **orthogonal adjacency**. At Chebyshev 5 nothing of ours
> can reach them — research's words: *"three out-of-reach sentinels killed our
> core."* 100% of their damage in all five games was sentinel fire; **zero builder
> melee.** 3 sentinels × 18 dmg / 2 rounds = **27 HP/round → 500 HP in 18.5
> rounds.**
>
> **This also explains the map-size flatness better than anything above:
> standoff is 5 tiles regardless of map size.** Only the walk-in scales, and they
> complete it by r29–31 anyway.
>
> **What my table below still contributes** is league-wide breadth (9,874 games vs
> their 5) and the *gunner* rows, which the autopsy does not cover. **What it must
> not be read for is the "inside vs edge" story** — my d² figures conflate
> cardinally-aligned with unaligned placements, and a sentinel's single-tile-wide
> line shot only connects when aligned. **Alignment, not distance, is the variable
> I missed.** The basis query below is still live and still worth having.

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

> # ⚠⚠ RESOLVED, AND MY HEADLINE IS RETRACTED. THE BASIS WAS THE ARTEFACT.
>
> The research arm's objection was correct and decisive. **The extractor measured
> distance to a SINGLE ANCHOR TILE with no 2×2 accounting** — `tools/corpus/replay_events.py:65,69,87-90`,
> where the replay's map header stores the core as one `Position` and `d2_enemy`
> silently inherits it.
>
> **The footprint was then established empirically, three independent ways, and the
> anchor is the NW tile:** buildings are never placed on core tiles, leaving a clean
> 2×2 hole at {(0,0),(+1,0),(0,+1),(+1,+1)} with **1 exception in 19,005 placements**;
> the builder spawn ring is exactly that block's collar; and core anchors reach x=0
> but never exceed w−2, an asymmetry only a +x/+y footprint produces. **So the anchor
> basis OVERSTATES distance for every plant approaching from the east or south — a
> directional bias, not a constant offset.**
>
> ### THE CLAIM I PUBLISHED IS DEAD. RETRACTED IN FULL.
> **"We are the only high-volume bot whose turrets sit at the edge of or outside
> their firing envelope" is REFUTED.** On the basis the engine actually uses:
> - **Our median forward GUNNER plant: d²=9 on the tile basis — INSIDE r²=13.**
>   It read 16 (outside) on the anchor basis. **The verdict inverts.** Share of our
>   gunner plants in range: **44.2% → 91.6%.**
> - **Our median forward SENTINEL plant: d²=25 — INSIDE r²=32.** It read exactly 32
>   (the edge) on the anchor basis. Share in range: **56.1% → 84.3%.**
>
> **No engine probe is needed and none should be spent.** The footprint is settled
> from the corpus at 19,005:1 and the recomputation is done.
>
> ### WHAT SURVIVES, AND IT IS THE PART THAT MATTERED
> **The ranking is IDENTICAL on both bases.** Sentinel medians order
> `Cookie < Mimercraft < Banminary < Bisons < Big O < SingleCore < OpenSverige` on
> anchor *and* on nearest-tile. **We are last — furthest from the enemy core — on
> both bases, for both turret types.** Cookie is closest on both (d²=8 → **4**, one
> tile of gap from the footprint).
>
> | claim | status |
> |---|---|
> | "our forward turrets can't reach the core" | **DEAD — anchor artefact** |
> | "fast killers plant closer than we do" | **SURVIVES**, identical ranking both bases |
> | "a sub-100 kill is a forward turret in range of the enemy core" | **SURVIVES and strengthens** — rushers go from 71–96% to **100% in-range** |
> | "Cookie plants effectively on top of the core" | **STRENGTHENS** — d²=4 |
>
> **The lever is HOW CLOSE and HOW MANY, not "are they in range at all".** Our
> sentinels average **1.3/game at d²=25**; Cookie's **2.3/game at d²=4**;
> Banminary's **2.5/game at d²=16**.
>
> **Residual caveat that cuts the other way:** gunners are line-of-sight and
> blocked by obstacles (sentinels are not), and the corpus stores no per-plant
> line of sight — so **91.6% is an UPPER BOUND** on our gunners' effective
> coverage. The sentinel figure of 84.3% has no such caveat.
>
> ### CORPUS DEFECT TO FILE (builder owns `tools/`)
> **`replay_events.py:65,69,87-90` computes `d2_own`/`d2_enemy` against a single
> core anchor with no 2×2 correction. EVERY published number sourced from those two
> columns carries the same directional bias.** Same class as the s26 trap set: **a
> column whose NAME promises a semantic its CONTENT does not carry** — `d2_enemy`
> says "distance to the enemy core" and means "distance to the enemy core's
> north-west tile".
>
> ### ⚠ AND AN APPARENT CONFLICT WITH THE BISONS AUTOPSY — FLAGGED, NOT RESOLVED
> The autopsy (`be497c6`) reports Bisons sentinels at **modal Chebyshev 5** and
> **ours at Chebyshev 1 and 2** in those five games. This cut reports Bisons
> sentinel median **d²=16 (Chebyshev 4)** and **ours at d²=25 (Chebyshev 5)** — i.e.
> *we* plant further. **Both cannot describe the same quantity.**
> **The likeliest reconciliation, offered as the discriminating question and NOT as
> an answer: the autopsy's "our Chebyshev 1–2" may be distance to OUR OWN core —
> home defensive sentinels — while this cut measures distance to the ENEMY core on
> games we WON.** Different subject, different population (5 losses vs 198 plants in
> sub-100 wins). **If that is it, the two findings are consistent and the combined
> story is sharper than either: they build FORWARD sentinels, we build HOME ones.**
> Whoever owns the autopsy should state which core its Chebyshev column measures
> from. **This is exactly the wrong-subject family, so it gets checked rather than
> assumed.**

> ### ⚠ (superseded, kept for the record) MEASUREMENT BASIS WAS UNSTATED
> **The core is 2×2, so "d²(turret → enemy core)" is ambiguous exactly where it
> decides the verdict** (research arm, and the objection is load-bearing):
> distance to the core's **centre/anchor tile** versus to the **nearest of its
> four occupied tiles** differ by up to ~1 tile per axis. **A gunner at d²=16 to
> centre can be at d²≈9 to nearest tile — comfortably INSIDE r²=13. Same number,
> opposite conclusion.** The engine's own predicates (`can_fire`,
> `get_attackable_tiles`) operate on TILES, so nearest-occupied-tile is the basis
> that decides "in range".
> **It cuts both ways:** if the extractor used nearest-tile throughout, the
> comparison stands AND the out-of-range reading is real; if it used centre, all
> rows shift together and the *ranking* may survive while the *absolute range
> verdict* does not. **Query sent back to the agent; both columns to be published
> side by side.** Until then the ranking claim is provisional and the
> in-range/out-of-range claim is NOT established.

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
