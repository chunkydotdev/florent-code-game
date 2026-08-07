# Ladder meta census — 2026-08-07

What strategy class every top team actually runs, and the class mix of the field our bot faces.

Census window: ladder state and replays as of **2026-08-07 ~14:45 local**. Every claim below is
tagged with the opponent version that was live at decode time. Versions on this ladder churn
fast (Pivot shipped twice inside the two-hour window this census covers) — treat any untagged
carry-forward of these numbers as stale.

## 0. Method and sources

All numbers are medians over decoded `.replay26` timelines using
`docs/research/2026-08-07-fanout/toolkit/replay_lib.py` (the validated decoder — it fixes the
signed-`delta`, `placeEntity`-as-update and core-footprint traps that `tools/replay_census.py`
gets wrong).

Three replay pools:

1. **`replay_archive/`** — 40 matches / 196 games passively archived from the whole ladder
   between 10:28 and 12:31 today, with `<matchId>.meta.json` sidecars carrying team names,
   versions and ratings. This is the whole-ladder sample.
2. **Three matches downloaded for thin top-8 teams** — `a796d789-8b1e-43dd-828e-84f66d312e95`
   (Pantheon v36 4-1 Jython v55), `4a29eb3c-51dc-467d-a8c0-ba3140c75f52` (Pantheon v36 3-2
   Pivot v64), `cbc8edf4-2a2e-4aa6-9e8b-7acef6049d80` (Jython v55 5-0 HTTP 418 v65).
3. **Eight of our own recent ladder matches** for the mid-pool teams we actually get matched
   against (listed in §3).

Derived metrics used throughout:

- **First aggression** — the round of the first `HpEvent` with negative delta where the source
  team is this team and the target team is the opponent.
- **Aim distance** — Euclidean distance from that first damaged entity to the *opponent's* core
  (NW footprint corner) and to *this team's own* core. Aim distance ~0 from the opponent's core
  means the first thing they shot was the core itself; a small distance from their own core
  means they shot something that walked into them (defensive).
- **Forward fraction** — where a team plants a turret or barrier, as a fraction of the
  core-to-core separation measured from its own core. 0.5 is midfield; >1.0 is past the enemy core.
- **Damage split** — pooled damage this team dealt to the opponent, bucketed into core /
  economy (harvester, conveyor, splitter, barrier) / military (turrets and builder bots).

Raw data lives in the session scratchpad (`all_profiles.json`, `top8_profiles.json`,
`midpool_profiles.json`, `rows.json`) alongside the profiler `profile.py` and aggregator `agg.py`.

## 1. Ladder state at census time

The ladder has moved since the fan-out brief was written. **Pivot and team lazy are no longer
#1 and #2.** Current top 12 by `fcode ladder`:

| # | Team | Rating | Matches |
|---|---|---|---|
| 1 | Pantheon | 1968 | 854 |
| 2 | sporks | 1960 | 339 |
| 3 | Pivot | 1948 | 598 |
| 4 | not adgato | 1908 | 438 |
| 5 | Jython | 1903 | 673 |
| 6 | team lazy | 1892 | 884 |
| 7 | The Flotte Experience | 1880 | 880 |
| 8 | HTTP 418 | 1860 | 886 |
| 9 | Erebus | 1813 | 895 |
| 10 | Besvikomat | 1791 | 896 |
| 11 | Powered by SmartFridge | 1771 | 861 |
| 12 | kladde chatte tville (och oss) | 1771 | 382 |

We are **#29 at 1545** (245 matches). Critically, the teams the prior research decoded are
**not** in the top 8: Landers is #17 (1680), Ouroboros #23 (1582), Lunds Stallions #26 (1565),
kladde #12 (1771). The top 8 was almost entirely undecoded before this census.

## 2. Per-team classification — top 8

| # | Team (version at decode) | n games | Median rounds | Core-kill share | Harvesters alive @200/500/800 | Turret mix (median built) | First aggression | Damage core/eco/mil | Class |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Pantheon v36** | 15 | 327 | 86% (13/15); 2 to r1000 | 2.5 / 2 / 2 | gun 4, sent 1, lau 1, **barr 12** | r38, aim 3.2 from their core | 40 / 36 / 22 | **Armoured late siege** (new class) |
| 2 | **sporks v2** | 25 | 279 | 88% (22/25); 3 to r1000 | 6 / 9.5 / **13** | gun 3, sent 3, lau 0, barr 4 | r20, aim **6.1 from its OWN core** | 30 / 34 / **35** | **Economy-first + defensive combat** |
| 3 | **Pivot v63→v64** | 11 | 342 | **100% (11/11)**; 0 to r1000 | 8 / 8 / 5 | gun 5, sent 0, lau 0, barr 1 | r12, aim 4.0 | 8 / **70** / 21 | **Strangle / eco-denial gunner siege** |
| 4 | **not adgato v15** | 5 | 423 | 100% (5/5) | 6 / 6 / — | **gun 12**, sent 0, lau 0, barr 3 | r14, aim 6.0 | 14 / **75** / 10 | **Strangle / eco-denial gunner siege** |
| 5 | **Jython v55** | 11 | 342 | 63% (7/11); **4 to r1000, won all 4** | 3.5 / 4 / **8** | gun 9, sent 0, lau 0, **barr 14** | r17, aim 6.1 | **55** / 26 / 17 | **Adaptive: core-kill or economy tiebreak** |
| 6 | **team lazy v88** | 10 | **114.5** | 90% (9/10); 1 to r1000 | 0 / 1 / 0 | gun 4.5, **sent 0, lau 0, barr 0** | r18.5, aim **0.0** | **64** / 28 / 6 | **Point-blank gunner core battery** |
| 7 | **The Flotte Experience v35** | 5 | 190 | 100% (5/5) | 1.5 / 3 / — | gun 6, sent 1, **lau 2** | r30, aim 6.0 | 24 / **68** / 7 | **Strangle / chip-siege** (prior decode confirmed) |
| 8 | **HTTP 418 v65** | 15 | 383 | 66% (10/15); 5 to r1000 | 4.5 / 0 / 0.5 | gun 8, sent 0, lau 0, barr 6 | r14, aim 5.1 | 34 / **55** / 10 | **Gunner picket with fragile economy** |

### 2.1 Pantheon v36 — armoured late siege (a class we had not seen)

Sample: 15 games across three opponents — `27e06fce-0036-4314-8518-3e9b8bed94d8` (vs sporks v2),
`a796d789-8b1e-43dd-828e-84f66d312e95` (vs Jython v55), `4a29eb3c-51dc-467d-a8c0-ba3140c75f52`
(vs Pivot v64).

Pantheon builds a median of **12 barriers per game** (max 51 in `4a29eb3c` game 4) and places
its gunners and sentinels at 0.69 and 0.63 of core separation, reaching 1.27 and 1.02 at the
extreme — i.e. at and past the enemy core. It opens aggression **late**, at r38 median with a
standard deviation of 21.3 rounds, the widest envelope in the top 8. It then kills: **13 of 15
games ended `core_destroyed`**, and it won all nine of its wins in this sample by core kill. It
carries a launcher in most games (first launcher r38 median, r6 at the earliest). Its economy is
thin and deliberately so — median 4 harvesters built, 2 alive at r500, 1740 Ti delivered.

This is a chip-siege that **armours** its forward turret line with barriers rather than replacing
it when it dies, and it wins the long game rather than the fast one. It is neither the Flotte
launcher-siege nor the Orizon point-blank battery, and it currently sits at #1.

### 2.2 sporks v2 — economy-first with a defensive combat line

Sample: 25 games, five distinct top-8 opponents — `27e06fce` (Pantheon v36),
`c96904fa-9afa-4869-961e-ccaebae86a73` (Pivot v63),
`73afd924-f015-4e14-baa8-4089f07f4323` (Flotte v35),
`abb34d36-319d-4c35-bacf-0793bad3c80a` (not adgato v15),
`ed29909b-2553-49fb-beea-8845b31b6ba5` (team lazy v88).

Full detail in §3 — this is the direct answer to the "does anyone play our meta" question.

### 2.3 Pivot v63→v64 — eco-denial gunner siege, and a moving target

Sample: 11 games — `c96904fa` (v63, vs sporks v2), `565979f7-4e5a-4854-a4eb-0a8a4839089c`
(v64, 1 game vs Jython v55), `4a29eb3c` (v64, vs Pantheon v36).

**Seventy percent of Pivot's damage lands on enemy economy** and only 8% on cores, yet **all
eleven decoded games ended `core_destroyed`** — the economy kill is the mechanism and the core
kill is the consequence. Gunner-only (81% of damage from gunners, 18% from builder melee, zero
sentinels or launchers built in 10 of 11 games), planted at 0.67 of core separation. It keeps a
real economy of its own: 9 harvesters built, 8 alive at r200 and r500.

Version churn is the headline operational fact: `c96904fa` at 10:28 is **v63**, `565979f7` at
12:01 and `4a29eb3c` at 12:05 are **v64**, and `fe4f4006-fadf-418d-ab7a-2b9ac53167c0` at 12:35
is back to **v63**. Pivot ships roughly hourly and rolls back.

### 2.4 not adgato v15 — the same class, heavier

Sample: 5 games, `abb34d36-319d-4c35-bacf-0793bad3c80a` (vs sporks v2).

**Twelve gunners built per game**, zero sentinels and zero launchers, 90% of damage from gunners
and **75% of it aimed at enemy economy**. First gunner at r13, first aggression at r14. Ten
harvesters built and 6 alive from r200 through r500, 1950 Ti delivered — a stronger economy than
Pivot's while running the same denial plan. All five games ended `core_destroyed`.

Caveat: one opponent, five games. The class assignment is confident; the timing constants are
one series' worth of evidence.

### 2.5 Jython v55 — adaptive, and the second bot that can win a tiebreak

Sample: 11 games — `a796d789` (vs Pantheon v36), `cbc8edf4-2a2e-4aa6-9e8b-7acef6049d80`
(vs HTTP 418 v65), `565979f7` (vs Pivot v64).

Jython branches hard on the opponent. Against Pantheon it played 3-7 harvesters and lost 4 of 5
by core kill. Against HTTP 418 it went to round 1000 in four of five games and **won every one
of them on `titanium_collected`**, delivering 2220 / 16180 / 3070 / 12350 Ti in those four games
— in `cbc8edf4` game 3 it built **27 harvesters and 169 conveyors**. Overall: 14 barriers and 9
gunners built median, zero sentinels and zero launchers in all 11 games, 55% of damage on cores.

This is the closest thing in the top 8 to a bot that will take the tiebreak when it cannot win
the fight.

### 2.6 team lazy v88 — point-blank gunner core battery (the Orizon class)

Sample: 10 games — `ed29909b-2553-49fb-beea-8845b31b6ba5` (vs sporks v2),
`52426cf4-3489-4fbd-b947-70b325901de6` (vs Jacobs Code v20).

**Gunners supply 100% of its damage.** It built zero sentinels, zero launchers and zero barriers
in all ten games. The first entity it damaged was the enemy core itself in six of ten games
(aim distance 0.0-2.2, standard deviation 0.9 across two different opponents). Gunners planted
at 0.86 of core separation. **Median game length 114.5 rounds**, minimum 58. Against the weaker
opponent (Jacobs Code v20) the profile sharpens further: **86% of damage on the core**, aim
distance 0.0 in 4 of 5 games, median 133 rounds, 5-0.

This is mechanically the same bot family as Orizon v34 (documented in
`findings/thread7_landers_orizon.md`) — gunner-only, no sentinels or launchers or barriers,
creeping plant sequence aimed at the core footprint — but faster and at a 1892 rating rather
than Orizon's mid-pool one. The family hypothesis flagged in thread 7 now has a third member.

### 2.7 The Flotte Experience v35 — chip-siege, prior decode confirmed

Sample: 5 games, `73afd924-f015-4e14-baa8-4089f07f4323` (vs sporks v2).

**Sixty-eight percent of damage on enemy economy**, gunner 81% / sentinel 15%, **2 launchers
built with the first at r9**, zero barriers. Median 190 rounds, all five games `core_destroyed`.
Consistent with the existing Flotte class entry; nothing here contradicts the prior probe spec.

### 2.8 HTTP 418 v65 — gunner picket with a fragile economy

Sample: 15 games — `8cb71ce4-4d21-48b2-bd7d-cb19968adbaa` (vs O(1) v8),
`4d91601b-ed53-4bcf-9bc5-23a837757788` (vs Powered by SmartFridge v33),
`cbc8edf4` (vs Jython v55).

Two faces. In the archived series it scaled to 12.5 harvesters built and 14 alive at r800 with
1315 Ti delivered and won 6 of 10. Against Jython v55 it collapsed: harvesters alive fell to 0
by r300 in the median game, 810 Ti delivered, 0-5. Pooled: 88% of damage from gunners, 55% on
enemy economy, median 8 gunners built and zero sentinels or launchers. Five of fifteen games
reached r1000 and it won only one of them.

## 3. Does any top-8 team run an economy-first / tiebreak-oriented meta like ours?

**Yes — sporks v2, ranked #2 at 1960, and it has the strongest economy in the top 8 by a factor
of two to four.** A partial second case is Jython v55 (§2.5).

Evidence, all from the 25-game sporks v2 sample:

**Real harvester scaling.** Median harvesters *alive* 5 / 6 / 7 / 9.5 / **13** at rounds
100 / 200 / 300 / 500 / 800, from a median of 15 built. Against team lazy v88 (`ed29909b`) it
reached **20 alive at r300, 30 at r500 and 35 at r800**, with 122 conveyors alive at r800; it
built 32 harvesters in game 1 and 35 in game 3 of that series.

**Delivery-focused.** Median 4380 Ti delivered, against Pantheon v36 1740, Pivot 1070, not adgato
v15 1950, Jython v55 2220, HTTP 418 v65 1120 and team lazy v88 415. Peak single games **15880**
(`ed29909b` game 1) and **10910** (`ed29909b` game 3); against Pantheon, 5200 / 5640 / 9510 in
`27e06fce` games 1, 3 and 4.

**Defensive rather than denial-oriented.** The first enemy entity sporks damages sits a median of
**6.1 tiles from sporks' own core and 9.2 from the enemy's** (core separation 17). Against team
lazy the split is 3.6 from its own core versus 17.2 from the enemy's. Only 30% of its damage
lands on enemy cores and 34% on enemy economy; **35% goes to enemy units and turrets** — the
highest defensive share in the top 8. Its 3 median sentinels sit at 0.61 of core separation: a
mid-map screen, not a home ring and not a forward siege.

**It converts to tiebreaks when it must.** Three of 25 games reached r1000 and it won two of them
on `titanium_collected` (`27e06fce` game 1 at 5200 Ti, game 4 at 9510 Ti).

**The important qualifier: sporks does not play *for* the tiebreak.** It wins 88% of its games by
`core_destroyed`. The economy is the engine, not the win condition. And no top-8 team is
denial-free: every one of them lands at least 14% of its damage on enemy cores and every one ends
a majority of games by core kill. The pure tiebreak archetype does not exist at 1860+.

### 3.1 Uncomfortable contrast — our own measured profile

Across the 38 mid-pool games decoded here (OpenSverige **v61-v64**), our own numbers are:

- median **3 harvesters built**, 3 alive at r300, **820 Ti delivered** (sporks 4380, I Stone v13 10280);
- **68% of our damage aimed at enemy cores**, 7% at enemy economy;
- first aggression at **r14 with aim distance 0.0 from the enemy core** — in
  `5eeee19a-91da-4e46-b4d8-5415260f1192` game 2 we built a sentinel at (9,3) and shot the enemy
  core at (14,3) on **round 3**;
- 31 of 38 games ended `core_destroyed`, only 7 reached r1000.

By the same metrics used to classify every other team in this document, **our live bot classifies
as a sentinel core battery with a small economy, not as an economy-first tiebreak bot.** If the
strategy discussion assumes we already play the sporks game, the replays say otherwise.

## 4. Class mix of the field we actually face

The pool we play is **not** the top 8. Over our last 60 ladder matches (300 games, 02:46-12:38
today, our v53 through v64) we played 19 distinct opponents and **none of them was in the top 8**.
Weighted by games rather than by team count:

| Class | Raw share of our 300 games | Share of classified games | Teams (version measured) |
|---|---|---|---|
| **Point-blank core battery** | 33.3% | **44.3%** | Orizon v34 (8.3%), Team 48 v16 (8.3%), 0033 v42 (6.7%), Memtrace v26 (5.0%), Askar City v72 (5.0%) |
| **Creeping gunner picket** | 26.7% | **35.6%** | Ouroboros v8 (10.0%), Lunds Stallions v37 (10.0%), Powerpuff Girls v25 (6.7%) |
| **Economy-first / tiebreak** | 6.7% | **8.9%** | I Stone v13 (6.7%) |
| **All-in rush** | 6.7% | **8.9%** | farming_200s v7 (6.7%) |
| **Patient grind (melee)** | 1.7% | **2.3%** | Jacobs Code v20 (1.7%) |
| *unclassified* | 24.9% | — | gsxWins v16, Leviathan v9, OopsGotYourElo v21, CtrlAltDefeat v107, SingleCore v7, the one piece v38, Kings College Munich v1, Oresund Overflow v30 |

**Point-blank core battery is 44% of our classified matched pool; battery plus picket is 80%.**

### 4.1 Evidence per mid-pool team

Each is a 5-game sample from one of our own recent matches.

| Team (version) | Match id | Result | Key numbers | Class |
|---|---|---|---|---|
| **Team 48 v16** | `bce041d8-e96c-4871-8d6a-c3523af3ac24` | OpenSverige v64 2-3 Team 48 | Gunners supply **100%** of damage; **98% lands on our core**; first damaged target was our core in **5/5 games** (aim distance sd 0.0); gunners at 0.88 of core separation; 940 Ti delivered | Point-blank core battery |
| **I Stone v13** | `77607daf-381a-4999-9f0b-3401b0d89deb` | I Stone 3-2 OpenSverige v64 | **12 harvesters built, 26 alive at r800, 115 conveyors, median 10280 Ti delivered** (40670 in game 2, 33030 in game 3); 20 gunners; 63% of damage on our economy; 2/5 games to r1000, won both on `titanium_collected` | Economy-first / tiebreak |
| **Powerpuff Girls v25** | `aab7e76b-c256-466c-8f05-34f8b7682919` | Powerpuff Girls 4-1 OpenSverige v63 | 12 gunners and 3 sentinels built; **first aggression r7**; damage 33% core / 46% eco / 19% military; 3230 Ti delivered; 5/5 `core_destroyed` | Creeping gunner picket |
| **farming_200s v7** | `dc5c7700-283d-453d-afa4-77b6eddbdccc` | farming_200s 2-3 OpenSverige v63 | **Median 82 rounds**, max 191; no game reaches r200; gunner-only, **99% core damage**, aim distance 0.0 in 4/4 games with damage; gunner at 0.97 of core separation | All-in rush |
| **0033 v42** | `5eeee19a-91da-4e46-b4d8-5415260f1192` | OpenSverige v62 4-1 0033 | Sentinel supplies 83% of damage; **85% on our core**; aim distance 0.0 in 3/5; sentinel at 0.70 of core separation; median 136 rounds | Point-blank core battery, sentinel variant |
| **Memtrace v26** | `c73638a0-d538-425f-acac-f94eec1564db` | OpenSverige v64 3-2 Memtrace | **80% of damage on our core**, eco damage literally zero in 4/5 games; 2 launchers built, first at r5; 41% of damage from melee builder pecks; gunner at 0.96 of core separation | Point-blank core battery, launcher-backed |
| **Lunds Stallions v37** | `7eff22cc-4e92-4b13-80c3-d1984e9d99b5` | Lunds Stallions **5-0** OpenSverige v64 | **Launcher on round 1 in 5/5 games** (sd 0.0); turrets at 0.67/0.87 of core separation; damage 50% core / 27% eco / 21% military; 9 harvesters built, 5 alive at r200 rising to 14.5 at r500; **1810 Ti delivered — below the 2000 economy-first bar** | Creeping gunner picket |
| **Askar City v72** | `3c61b886-4d08-49a9-baed-c12ae050622d` | Askar City 1-4 OpenSverige v61 | **Eco damage exactly 0 in all 5 games**; 864 core damage is the only meaningful component; **zero gunners built**; sentinel at 0.9 of core separation, 0.5 tiles from our core; barriers pushed forward at 0.84 to shield the emplacement | Point-blank core battery, sentinel/barrier variant |

Already-decoded teams in this pool, cited rather than re-decoded: **Ouroboros v8** (10.0% of our
games) — creeping gunner picket, confirmed in the archive at `bab61537-2315-4121-9286-d9447197afc2`
and `22f55a05-bf9d-4040-a851-7444c4e3e6e1` with 21 gunners built, 98% of damage from gunners, aim
distance 11.7 from our core, 7 harvesters and 3380 Ti delivered; **Orizon v34** (8.3%) —
point-blank gunner core battery, six games documented in `findings/thread7_landers_orizon.md`,
most recent series `607ffaeb-4574-4ea0-8e73-f811c976c727`.

### 4.2 Whole-ladder cross-check

An automated pass over all 392 team-games in the passive archive (all rating bands) gives a
consistent shape: point-blank core battery 19.1%, mixed gunner picket 14.3%, economy-first 14.0%,
all-in rush 12.8%, patient grind (melee) 11.5%, eco-denial siege 6.6%, and **21.7% essentially
passive bots** that never deal meaningful damage. The passive bucket is concentrated below 1300
and is not relevant to our band; the classifier is rule-based and noisier than the hand
classifications above, so treat it as a sanity check rather than a result.

### 4.3 Recommended benchmark battery

Roughly **4 point-blank core battery / 3 creeping picket / 1 economy-first / 1 all-in rush** out
of nine probe seats. Point-blank core battery is nearly half of what we play and is the class
behind our worst measured matchups: Ouroboros v8 5-0 (`bab61537`, `14ee02b8-adae-4cc3-99f1-f307b62f6cfe`),
Lunds Stallions v37 5-0 (`7eff22cc`), and Orizon's six documented losses in thread 7.

## 5. Probe-ability ranking

Baseline from `findings/thread1_determinism.md`: the engine is byte-deterministic given (map,
both bot versions, seat) — three replay pairs confirmed round-identical at 227/227, 194/194 and
805/805 rounds. Faithful imitation is therefore bounded only by how scripted the opponent's
*decision function* is, not by engine noise. Measured here as the spread of first-build and
first-aggression rounds across games and maps.

### 5.1 Top 8

| Rank | Team (version) | Opening-timing spread | Verdict |
|---|---|---|---|
| 1 | **team lazy v88** | first turret r2-34 (sd 9.2); **aim distance 0.0-2.2, sd 0.9, over 10 games and 2 opponents** | **Easiest.** Gunner-only, zero sentinels/launchers/barriers in 10/10, constant aim point. Turret timing varies only with walk distance, which is derivable from the map. Freeze it. |
| 2 | **not adgato v15** | first turret **r10-25 (sd 5.4)**, first aggression r11-26 (sd 5.4) — tightest band in the top 8 | **Easy.** Gunner-only (90% of damage), zero sentinels and launchers, 12 gunners median. One constant to tune. |
| 3 | **The Flotte Experience v35** | first turret r5-14 (sd 3.2); launcher first at r9 | **Easy, already spec'd.** Constant kit (gunner + sentinel + launcher, zero barriers). Prior probe spec holds. |
| 4 | **HTTP 418 v65** | first turret r5-18 (sd 5.4) within a series; harvester scale differs 12.5 vs 6 between series | **Medium.** Opening is tight; the economy branch is opponent-conditional. Probe the opening only. |
| 5 | **Jython v55** | first turret r6-49 (sd 12.4) | **Hard.** Branches hard on the opponent — 1 harvester in one game and 27 in another of the same series. Needs two probes (kill-mode and economy-mode) or none. |
| 6 | **Pantheon v36** | first turret r6-48 (sd 16.6), first aggression **r13-95 (sd 21.3)**, barriers 1-51 per game | **Hard.** The widest behavioural envelope in the top 8. A frozen probe would be a caricature. |
| 7 | **sporks v2** | first turret r6-77 (sd 15.9) over 25 games; harvesters built 4 → 35 depending on opponent | **Hardest to imitate, most valuable to study.** The most adaptive bot on the ladder. It has shipped only twice (v2), so what we learn stays true — but a frozen opening tells us nothing about what makes it #2. Study it; do not imitate it. |
| 8 | **Pivot v63→v64** | first turret **r4-110 (sd 21.6 on v63, 37.7 on v64)** | **Do not probe.** Worst variance measured, plus a shelf-life problem: v63 at 10:28 (`c96904fa`), v64 at 12:01 and 12:05 (`565979f7`, `4a29eb3c`), back to v63 at 12:35 (`fe4f4006`). Any Pivot probe is stale within the hour. Track the class, not the bot. |

### 5.2 Mid-pool teams are better probe targets than the top 8

Three teams we actually play are more scripted than anything in the top 8, and they sit in the
two classes that dominate our matched pool:

- **Askar City v72** is the purest script found: **launcher first build at round 1 and conveyor at
  round 3 in 5/5 games**, across maps from 10x10 to 26x26. Map-independent and trivially freezable.
- **Team 48 v16**: aim distance **0.0 in 5/5 games, standard deviation exactly 0**. Its *timing*
  is reactive (first turret r2-12), so freeze its **aim policy**, not a turn script.
- **farming_200s v7**: aim distance **0.0 in 4/4 games with damage**, median 82 rounds. Same
  treatment — freeze the aim policy.
- **Lunds Stallions v37** fixes only its round-1 launcher (5/5, sd 0.0); harvester and turret
  timings vary widely. One fixed turn-1 utility build, adaptive thereafter.

The other mid-pool teams (I Stone v13, Powerpuff Girls v25, 0033 v42, Memtrace v26) show no
constant first-build round for any entity kind beyond the round-0 builder bot.

**Recommendation:** the highest-value probe set is not drawn from the top 8. Team 48 v16 +
farming_200s v7 + Askar City v72, alongside the existing Orizon probe, would cover the
point-blank core battery class that is 44% of our matched games; Lunds Stallions v37 and the
existing Ouroboros work cover the picket class at another 36%.

## 6. Loose ends

- **gsxWins v16, Leviathan v9, OopsGotYourElo v21, CtrlAltDefeat v107 and SingleCore v7** together
  account for 20% of our games and remain unclassified. One match each (25 games) would take the
  classified share from 73% to 93%.
- Sample sizes are honest but small for **not adgato v15** (5 games, one opponent) and **The
  Flotte Experience v35** (5 games, one opponent). Pantheon v36, Jython v55, Pivot v63/v64,
  sporks v2, team lazy v88 and HTTP 418 v65 all have 10-25 games across 2-5 distinct opponents.
- Mid-pool samples are 5 games each against **our own bot only**, so their measured aggression is
  partly a response to our play. The aim-point constants (0.0 aim distance) are robust to that;
  the timing constants are less so.
- Pivot's version churn means the §2.3 numbers pool v63 and v64. They agree on class (eco-denial,
  70% of damage on economy in both) but not on timing.
- The team lazy / Orizon family hypothesis from thread 7 now has a third member and is worth the
  cheap cross-check that thread recommended: if team lazy v88, Orizon v34 and Team 48 v16 are one
  mechanism, one fix retires three opponents at once.

---

*Census performed read-only: `fcode ladder`, `fcode match list`, `fcode match info` and
`fcode match replay` only. No submissions, activations, unrated challenges or arena runs.*
