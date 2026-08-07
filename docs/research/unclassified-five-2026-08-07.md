# The unclassified five — decode (2026-08-07, THREAD 3)

Executes THREAD 3 of `docs/research-brief-2026-08-07b.md` against
`docs/research/2026-08-07-fanout/meta-census.md` §6: classify gsxWins, Leviathan,
OopsGotYourElo, CtrlAltDefeat and SingleCore, merge them into the census §4 pool-mix
table, and finalize the weighted-battery denominators. Read-only throughout: `fcode
match list` / `match info` (unlimited, cheap) + exactly 5 `match replay` game downloads,
paced ≥90s apart, decoded exclusively with
`docs/research/2026-08-07-fanout/toolkit/replay_lib.py`. No bot/submission edits, no
arena runs, no unrated challenges initiated (two already-existing unrated gsxWins games
were read, not created, by this session).

## 0. Method

Mirrors meta-census.md §0's metric definitions exactly (first aggression, aim distance
to opponent/own core NW corner, forward fraction of core-to-core separation, damage
split core/eco/military) — see that section for the precise formulas. One deviation,
forced by the hard download budget: **every team's numbers are two-tier**.

- **Outcome tier** (median rounds, core-kill share, tiebreak count) comes from
  `fcode match info --json` on every recent match for that team — free, no download,
  and typically 10-25 games, a *larger* sample than the census's own typical 5-game
  mid-pool rows.
- **Entity tier** (turret mix, damage split, aim distance, forward fraction, harvester
  curve) comes from the decoded `.replay26` subset only, sized by what the budget
  allowed: Leviathan 5 games (free — already in `replay_archive/`), CtrlAltDefeat 2
  games (2 different maps, spent deliberately to test opening-signature consistency),
  gsxWins / OopsGotYourElo / SingleCore 1 game each.

`replay_archive/` was checked first (`find` + a full scan of every `.meta.json`
sidecar's `teamAName`/`teamBName`): only **Leviathan v9** was already present, in a
non-us match (`Coreflood` vs `Leviathan`, id `0ab86a4e-a8c7-471b-9b3c-55ef0f2cb622`) —
legitimate evidence per the census's own precedent of drawing top-8 classifications
from whole-ladder passive archive matches we weren't a party to. The other four were
not archived despite the brief's hint that SingleCore's `c8479d42` match "likely" was;
it wasn't, and was downloaded fresh (game 3, its exact hinted match).

**Download log** (all `fcode match replay <id> -g <n>`, budget 5/5 used):

| # | Time (UTC) | Match | Game | Gap from previous |
|---|---|---|---|---|
| 1 | 14:11:46 | `a5671738` CtrlAltDefeat v107 vs us, drumlin | 1 | — |
| 2 | 14:13:16 | `ccab0b53` CtrlAltDefeat v107 vs us, meander | 1 | 90s |
| 3 | 14:14:56 | `79f0d5f8` gsxWins v18 vs us, fjordgate | 2 | 100s |
| 4 | 14:16:27 | `db395308` OopsGotYourElo v21 vs us, nordkap | 1 | 91s |
| 5 | 14:18:00 | `c8479d42` SingleCore v7 vs us, atoll | 3 | 93s |

All 5 decoded files passed `replay_lib`'s full self-check battery (`check_all()`):
delivery×10 == titaniumCollected, ammo converted−spent == final, zero unknown
top/turn/update/entity fields, no recycled ids, HP in bounds, winner-vs-dead-core
consistent, and damage attribution **100%** in every file (429/429, 796/796, 73/73,
939/939, 93/93 — the two known traps, signed-`delta` and shooter-less `FireTurret`,
cost nothing here).

## 1. Per-team classification

| Team (version) | Sample (decoded / outcome-only) | Median rounds | Core-kill share | Harvesters @200/500/800 | Turret mix (median built) | First aggression | Damage core/eco/mil | Class |
|---|---|---|---|---|---|---|---|---|
| **Leviathan v9** | 5 / 15 | 64 | 93% (14/15); 1 to r1000 | — / — / — (all games <200r) | gun 5, sent 0, lau 0, barr 0 | r4-33, aim **0.0 in 4/5** | 90 / 1 / 9 | **Point-blank gunner core battery** |
| **CtrlAltDefeat v107** | 2 / 25 | 238 | 96% (24/25); 1 to r1000 | 5 / 8 / — | gun 18.5, sent 0.5, lau **1, 1**, barr 3.5 | r4, r12, aim **0.0 in 2/2** | 43 / 44 / 13 | **Launcher-insertion → eco/core hybrid siege** (confirmed, unchanged) |
| **gsxWins v18** (brief: v16) | 1 / 15 | 122 | **100% (15/15)**; 0 to r1000 | — / — / — (75r game) | gun 0, sent 2, lau 1, barr 0 | r4, aim **0.0** | 100 / 0 / 0 | **Point-blank core battery, sentinel-led** |
| **OopsGotYourElo v21** | 1 / 10 | 1000* | 40% (4/10); **6 to r1000 (60%)** | 5 / 12 / 13 | gun 6, sent 0, lau 0, barr 8 | r25, aim 9.1 opp / **3.2 own** | 96 / 1 / 4 | **Economy-first / tiebreak** (most tiebreak-committed instance measured) |
| **SingleCore v7** | 1 / 10 | 163.5 | 70% (7/10); 3 to r1000 | — / — / — (85r game) | gun 0, sent 3, lau 1, barr 0 | r18, aim **0.0** | 80 / 4 / 16 | **Point-blank core battery, sentinel-led** (lower consistency) |

\* OopsGotYourElo's outcome sample is bimodal, not gradual: rounds were
130/236/300/514/1000/1000/1000/1000/1000/1000 — six hard round-caps and four
resolved fights, nothing in between. The non-tiebreak games alone median ~268.

### 1.1 Leviathan v9 — point-blank gunner core battery

Evidence: `0ab86a4e-a8c7-471b-9b3c-55ef0f2cb622` (5 games, `Coreflood` vs `Leviathan`,
archived) for entity detail; add `745fc6fc-a007-4a0f-adf2-2686ae942d31` and
`c9b79ad3-063e-4075-b6d5-c88c703fdde8` (both vs us, both v9) for the 15-game outcome
sample.

**Gunner-only in all 5 decoded games — zero sentinels, launchers or barriers, every
single game.** Median 5 gunners built. Aim distance is 0.0 from the opponent's core in
4 of 5 games (the fifth, `heart`, hit an enemy gunner first at distance 3.16 — still
effectively at the core). Damage split 90% core / 1% eco / 9% military — the most
core-exclusive split measured in this whole set. Gunners plant at a median **0.93** of
core separation (range 0.5-1.13 — i.e. routinely *past* the opponent's core). Median
rounds is **64 outcome-only / 57 decoded** — faster than team lazy v88's 114.5, the
previous fastest team in the census. Lost its one long game (`archipelago`, 192
rounds) to Coreflood; won the other four in 41-64 rounds each.

This is a clean **fourth member of the team-lazy / Orizon / Team 48 point-blank family**
flagged in census §2.6 and thread 7 (`docs/research/2026-08-07-fanout/findings/thread7_landers_orizon.md`)
— same signature (gunner-only, zero everything else, aim ~0, forward-planted), and the
fastest-resolving instance of it found so far.

### 1.2 CtrlAltDefeat v107 — launcher-insertion, confirmed unchanged

Evidence: decoded `a5671738-b680-4528-9b55-c2df52e46b1d` g1 (drumlin, 25x25, cores
18.4 apart) and `ccab0b53-e7c5-4ab0-a0e0-fae87ff98252` g1 (meander, 25x15, cores 7
apart); outcome sample adds `a7f168d7-2216-4023-9c5c-5ff3a29cff7b`,
`ef87936f-d443-4e61-8966-748307dd5438`, `8de547a8-f2d1-419b-a127-ecad9eb90c78` (all
v107, all vs us, 25 games total).

**Direct answer to the brief's question: yes, v107 still matches the launcher-insertion
class exactly as decoded in the cad_probe era**
(`bots/cad_probe/main.py`, provenance match `e40a6c01`). Both decoded games open
identically: a **launcher built on round 1** adjacent to their own core, then **3
builder bots thrown** (jump-moves of 3.6-6.4 tiles in one round, unreachable by normal
1-tile/round movement) on **rounds 2, 3 and 4 in both games** — exact round-for-round
match to the frozen probe's r2/r3/r4 throw cadence. First damage to the opponent's
core lands at **aim distance 0.0 in both games** (r12 on the wide map, r4 on the tight
one) — a thrown raider melee-pecking the core directly, before either game's first
turret exists. On drumlin the first turret (a sentinel) goes up at **r11** at
core-distance² = 25, opens fire at **r12** — one round later, exactly the probe's
documented "opens fire the round after it was built." On meander the tight 7-tile
core separation means the walk phase is nearly nonexistent and the first plant is a
**gunner at r3** instead — consistent with the probe's own noted map-separation
dependence, not a deviation from it.

What differs from a pure "insertion" read is the mid/late game: a real, funded economy
(12 harvesters / 45-130 conveyors alive, matched or beat our own count by mid-game in
both decoded games) and a large gunner force (18-19 built, split bimodally — roughly
38% planted at 0.08-0.22 of core separation as **home defense**, the rest at
0.29-1.19 as a **forward line**). Pooled damage split is 43% core / 44% eco / 13%
military — the two decoded games individually were 72/12/17 (short game, drumlin) and
32/56/12 (long game, meander), i.e. the longer the siege runs, the more its damage
share shifts from core-chip to economy-starvation. Forced onto the task's class list,
this is a **hybrid: all-in-style melee opener (insertion) into an eco-denial siege**
(the same 44-56% eco-damage shape as Pivot/not adgato in census §2.3-2.4) rather than
a clean fit to any single named class — reported as such rather than forced.

Outcome sample: 96% core-kill (24/25), median 238 rounds (both decoded games, 398 and
760, happened to land above that median — the budget spent on longer, more
information-dense games on purpose). One caveat: the whole-ladder `--team
CtrlAltDefeat` pull (100 matches, any opponent) showed versions 110-113 appearing
3-5 times each alongside 84 v107 entries — possible Pivot-style version churn
elsewhere on the ladder. Every one of our own last-60 ladder matches against them
(2 matches) and every match-info pulled for this thread was v107; track the class,
re-check the version if a v110+ match against us appears.

### 1.3 gsxWins v18 (brief named v16) — point-blank core battery, sentinel-led

Evidence: decoded `79f0d5f8-6ebc-41e0-8c85-e4714f34f6f4` g2 (fjordgate, 10x10);
outcome sample adds `0faf41b6-93de-4e1e-b125-f7611d7b4db2` (v18) and
`2a152b61-bd14-45a9-bc27-fa0d0b4b8702` (v16, ladder, 06:25Z — the version the brief
named).

**Version drift caught in the act**: gsxWins shipped v16→v18 sometime between 06:25Z
and 13:28Z today. Both versions show the identical signature — all 5 v16 games and
all 10 v18 games in the outcome sample ended `core_destroyed` — so the class survives
the ship. **100% core-kill share across all 15 games sampled is the single cleanest
"always ends in a kill" signal of any team measured in this thread or the census
top-8** (Pivot and not adgato also hit 100%, but on n=11 and n=5 respectively).

The one decoded game (a tiny 10x10 map, 75 rounds) shows 2 sentinels built, zero
gunners, first aggression at round 4 with aim distance 0.0 (direct core hit), 100% of
damage on the core. One launcher, one single-raider throw at r4 (dist 4.1) — a token
opening harassment move, not a sustained CAD-style insertion (no repeat throws for the
rest of the game). Both sentinels then camp on fixed tiles and fire on fixed targets
every reload cycle for the whole game — textbook stationary point-blank battery,
matching the 0033 v42 "sentinel variant" sub-class already in census §4.1. Caveat:
n=1 and the smallest possible map size, so the entity-level numbers (forward fraction
0.40, damage split 100/0/0) should be read as illustrative, not as tight constants;
the outcome-tier numbers (100% core-kill, median 122 rounds across varied map sizes:
atoll/fjordgate/lighthouse/snowflake/heart/nordkap/saga/jackpot/moonrise/meander/
hive/antler) are the load-bearing ones.

### 1.4 OopsGotYourElo v21 — economy-first / tiebreak, the most committed case yet

Evidence: decoded `db395308-b0b5-40a6-b407-8ac3f287fa0f` g1 (nordkap, 20x26, 1000
rounds); outcome sample adds `ad08eb70-4926-4d8a-b459-b48ace96f56c`.

**60% of games in the outcome sample (6/10) reach round 1000** — the highest
round-cap rate of any team in the census or this thread (sporks 12%, Jython "4 of 5"
in one series, I Stone 40% in our own portfolio). The decoded game is a win: 13
harvesters alive by r800, 95 conveyors, 13670 Ti delivered vs our 9040, won on
`titanium_collected`. Unlike gsxWins/SingleCore/Leviathan, its first-aggression aim
point sits **closer to its own core (3.16) than the opponent's (9.06)** — the same
defensive-leaning shape census §2.2 measured for sporks v2 ("first enemy entity
sporks damages sits a median of 6.1 tiles from its own core"). An early barrier ring
(8 built, median forward fraction 0.19, first at r10) holds the home line while a
small gunner corps (6 built, bimodal 0.24-0.42 home-guard vs 1.09-1.18 forward) comes
later (r24) and does the actual finishing — 96% of its dealt damage lands on the core
once the fight resolves in its favor, despite the defensive opening.

Head-to-head vs us across the 10-game outcome sample: 5-5, exactly at expectation for
a mid-pool team. This reads as a **more literal instance of "plays for the tiebreak"**
than sporks itself — census §3 explicitly noted sporks "does not play *for* the
tiebreak... wins 88% by core_destroyed"; OopsGotYourElo's split is close to 50/50 and
its round distribution is bimodal (short fight or full grind, nothing between). That's
a mid-pool refinement of the class, not a contradiction of the top-8-specific claim.

### 1.5 SingleCore v7 — point-blank core battery, sentinel-led, lower consistency

Evidence: decoded `c8479d42-f9bb-42b6-9953-adbb7e2103f3` g3 (atoll, 18x18) — the exact
match the brief flagged (SingleCore vs us, 13:27Z); outcome sample adds
`c7dec9d5-f205-4d43-80ac-0610c04d9c1e`.

The decoded game is SingleCore's win: 3 sentinels, zero gunners, first aggression at
r18 (one round after the first sentinel's r17 build — immediate fire-on-plant, same
pattern as CtrlAltDefeat's sentry), aim distance 0.0, 80% of damage on the core.
Sentinels plant at 0.75-0.82 of core separation. One launcher built at r2 near its own
core, but instead of a CAD-style repeated raid it does something narrower and odder: a
single builder bot (id 3) gets thrown/walks out to a forward tile and back on an
**almost exactly period-8 cycle** (rounds 25, 33, 41, 49, 57, 65, 73, 81 — seven
consecutive gaps of 8) for the whole game. Single-game evidence, but if it recurs
that's a highly mechanical, exploitable pattern (see §3).

Outcome sample is less clean than gsxWins': 70% core-kill (7/10), 30% to round 1000
(3/10) — noticeably more variance than the near-monolithic 90-100% seen in the other
point-blank teams. Its wins are uniformly fast (r74-101); losses are a mix of fast
core deaths and two round-1000 tiebreak losses, neither of which was decoded, so
whether those are "the rush failed and it fell back to something else" or genuinely a
different mode is an open question (§4). Classified as point-blank core battery on the
strength of the winning mechanism, flagged explicitly as the weakest-fit / most
hybrid-adjacent of the three sentinel-led point-blank teams found this thread.

## 2. Updated pool-mix table

Census §4 used "our last 60 ladder matches" as of ~14:45 earlier today. Time has moved
on (both our own bot and several opponents have shipped since), so this recomputes
from a **fresh pull of our last 60 ladder matches** (`fcode match list --mine --json`,
paginated by `completedAt` cursor, filtered to `triggeredBy == "ladder"` — unrated
research/portfolio challenges excluded, matching the census's implied scope), covering
**2026-08-07T04:06:19Z to T13:58:19Z**. This is the "finalized" denominator the brief
asked for: current, not a historical snapshot.

| Class | Raw share (of 60) | Share of classified (of 56) | Teams (version, match count) |
|---|---|---|---|
| **Point-blank core battery** | 43.3% | **46.4%** | Orizon v34 (5), 0033 v42 (5), Team 48 v16 (4), Memtrace v26 (3), Askar City v72 (3), **Leviathan v9 (2)**, **gsxWins v18 (2)**, **SingleCore v7 (2)** |
| **Creeping gunner picket** | 26.7% | **28.6%** | Lunds Stallions v37/v41 (7), Ouroboros v8 (5), Powerpuff Girls v23/v25/v26 (4) |
| **Economy-first / tiebreak** | 10.0% | **10.7%** | I Stone v13 (4), **OopsGotYourElo v21 (2)** |
| **All-in rush** | 8.3% | **8.9%** | farming_200s v7 (5) |
| **Launcher-insertion / eco-denial hybrid** *(new row)* | 3.3% | **3.6%** | **CtrlAltDefeat v107 (2)** |
| **Patient grind (melee)** | 1.7% | **1.8%** | Jacobs Code v18 (1) |
| *unclassified* | 6.7% | — | Viktor5776 v1 (1, new — not in the original census), the one piece v38 (1), Kings College Munich v1 (1), Oresund Overflow v30 (1) |

**Classified share: 56/60 = 93.3%** — the brief's target of "73% → 93%" lands almost
exactly on the nose. Bold entries are this thread's five teams (10 matches total: 2
each); the non-bold entries are a fresh recount of census §4's original five classes,
which come to 46 matches now (was 45) — essentially unchanged, all drift within one
match per team (Team 48 5→4, 0033 4→5, Ouroboros 6→5, Lunds 6→7, farming_200s 4→5),
i.e. noise from the trailing-60-match window moving forward ~9 hours, not a
methodology change. **The entire jump from 45/60 to 56/60 classified is this thread's
10 matches**: 8 fold into the three existing classes they match (point-blank +6,
economy-first +2), and CtrlAltDefeat's 2 form the new insertion row.

One genuinely new fact: **Viktor5776** appeared in our last 60 ladder matches (1 game,
v1) and was not in the original census's unclassified-eight list at all — a brand-new
opponent, not previously seen. It is not one of this thread's five and stays
unclassified; flagged for a future thread rather than decoded here (out of scope, and
the budget was fully committed).

**Benchmark-battery implication (census §4.3):** the recommended split was "4
point-blank / 3 creeping / 1 economy-first / 1 all-in rush" out of nine seats. Scaled
to the updated classified-share percentages (46.4/28.6/10.7/8.9/3.6/1.8), point-blank
rounds to 4, creeping to 3, economy-first to 1, all-in to 1 — **unchanged** at 9 seats.
The insertion and patient-grind classes combined are 5.4% of the field, just under
half a seat; a CAD-style insertion representative (`bots/cad_probe` is already frozen
and re-verified current, per §1.2) is the natural 10th seat if the battery grows, not
a seat that should displace one of the current four.

## 3. Probe-ability notes

| Team | Timing spread | Aim-policy constancy | Verdict |
|---|---|---|---|
| **Leviathan v9** | First gunner build r3-32 (5 games) — wide, reactive to map/enemy distance | Kit is a hard constant: gunner-only, zero sentinel/launcher/barrier in 5/5 games; aim 0.0 in 4/5 | **Kit and target frozen, timing isn't.** Freeze "gunner beelines the core," don't freeze a round number. |
| **CtrlAltDefeat v107** | Launcher **r1 in 2/2**, raiders **r2/r3/r4 in 2/2** (exact match across two maps) — the tightest opening of anything in this thread; downstream turret timing scales with map core-separation (a knowable rule, not noise) | Aim distance 0.0 in 2/2; melee-first doctrine constant | **Easiest to probe of the five.** Already frozen once as `bots/cad_probe` and re-verified unchanged today — the r1-r4 opening is safe to keep treating as a hard constant. |
| **gsxWins v18** | First sentinel r3, launcher r2 in the one decoded game; outcome-tier 100% core-kill (n=15) is itself a strong, low-variance signal | Aim 0.0 in the one decoded game | **Promising but under-sampled** — only 1 entity-level game. Recommend a follow-up 5-game batch before freezing a probe; the round-outcome signal (always ends in a kill) is already solid enough to plan around. |
| **OopsGotYourElo v21** | Whole-game outcome is sharply bimodal — resolves under ~520 rounds or goes exactly to 1000, nothing between, across 10 games | First aggression aim leans toward its **own** core (3.2 vs 9.1) — a defensive posture, not a fixed target point | **Hard to probe for a kill timing** (bimodal, not a curve); the useful probe is behavioral — if its early defense holds, expect a full-length grind, not a slow bleed toward a mid-game kill. |
| **SingleCore v7** | Outcome-tier more scattered than the other point-blank teams (70/30 core-kill/tiebreak split, vs 90-100% for the others); one decoded game shows a striking near-exact period-8 shuttle-throw of the same builder (r25/33/41/49/57/65/73/81) | Aim 0.0 in the one decoded (winning) game | **Two different questions.** The rush-kit itself (sentinel-led, aim 0.0) looks probeable on n=1; the period-8 shuttle is a high-value, unverified follow-up (n=1) — if it holds across games it's a very exploitable fixed cadence. |

## 4. Caveats

- **Sample-size asymmetry is real and budget-driven, not a judgment call**: Leviathan
  got a full 5-game decode for free; CtrlAltDefeat got 2 games on 2 maps by design
  (needed to test opening-signature *consistency*, which n=1 cannot show); gsxWins,
  OopsGotYourElo and SingleCore each got exactly 1 decoded game. Every team's
  outcome-tier numbers (median rounds, core-kill share) rest on a larger free
  match-info sample (10-25 games) and are more trustworthy than the entity-tier
  numbers (turret mix, damage split, forward fraction, aim distance), which for three
  of the five teams are a single game's worth of evidence and should be treated as
  illustrative rather than as tight constants — exactly the same caveat the census
  itself applied to not adgato v15 and The Flotte Experience v35 at n=5.
- **OopsGotYourElo and SingleCore's round-1000 games were never decoded** (6/10 and
  3/10 of their outcome samples respectively) — the tiebreak-loss mechanism for
  SingleCore and the full economy-buildout shape for OopsGotYourElo's *losing*
  tiebreak games (it won 4 of 6, lost 2) are inferred from the one game each that was
  decoded, not directly observed in a loss.
- **CtrlAltDefeat's global version footprint (v110-v113) wasn't investigated** beyond
  noting it exists — out of this thread's budget and not needed for the "does v107
  still match cad_probe" question, which is answered directly from matches actually
  played against us.
- **Damage attribution was 100% clean in every decoded file** (no unattributed events,
  no unknown update/entity/turn/top-level fields) — the toolkit's traps list (signed
  `delta`, shooter-less `FireTurret`, `placeEntity`-as-rotation) cost nothing here, and
  no new trap surfaced.
- **Pool-mix recount used a fresh 60-match window**, not the exact same matches the
  census counted (~9 hours later; both our own bot and several opponents shipped in
  between per HANDOVER/spitball). This is the intended reading of "finalize the
  denominators" — current, not historical — but it means the non-bold rows in §2 are
  an independent re-measurement of census §4's teams, not a copy of its numbers; the
  close agreement (within one match per team almost everywhere) is a cross-check
  result, not a given.
- **Viktor5776** surfaced as a genuinely new, unclassified opponent in the fresh
  window and is explicitly out of scope for this thread (not one of the named five;
  budget was fully committed to the five before it was noticed).
