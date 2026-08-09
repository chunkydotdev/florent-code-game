# Per-opponent reaction atlas (side lane deliverable)

**Side research lane, 2026-08-09. Version tag: live v90, corpus attribution
join 2,735 replays (validated 495/495 winner-field, 5,470/5,470 shot-count
reconciliation vs the independent phase-mining decoder). Opponent side of
games vs OpenSverige. Scripts + raw event tables in the side-lane session
scratchpad (rx_decode.py etc.); per-version drift cuts included below —
quantitative columns MOVE across opponent versions, qualitative gates hold.**


**Built 2026-08-09, research arm, read-only.** Scripts: `rx_decode.py` (event
decoder, 2,735 attributed replays, 30 s with 8 workers), `rx_analyse.py`,
`rx_drift.py`, `rx_report.py`, all in this scratchpad. Raw event tables in
`rx/`. **Everything below is the OPPONENT side of games against OpenSverige**
unless stated; `atlas_all.txt` carries the same cuts over all attributed games
of those teams (larger n, mixed opposition).

## Provenance and validation

* Attribution: replay filename `<matchId>_game_N.replay26` prefix-joined to
  `corpus/league_matches.tsv` -> 2,735 of 4,247 archived replays. Direction of
  the seat mapping (teamA == replay team 0) **reconciled**: over 495 games from
  5-0 / 0-5 sweep matches, the replay's own `winner` field agrees with the
  metadata winner **495/495**.
* Shot counts **reconciled against the prior agent's independently written
  decoder**: 5,470 of 5,470 (file, team) sides agree exactly, 808,509 shots
  total. This is the same check style the corpus how-to demands.
* Rotation detection validated by the game rules: `rotate()` is gunner-only.
  Across the whole corpus there are **69,220 direction-changing `placeEntity`
  re-emits and every single one is a gunner** - zero sentinels, zero conveyors,
  zero splitters. Independent confirmation that "direction-changed re-emit" ==
  "rotate()".
* Trap 1 (rotate re-emits `placeEntity`) and trap 3 (throws are jump-moves, both
  launchers in range -> dropped) honoured.

## Cross-opponent summary

| opponent | sides | vers | shots n | %bldg | %noncore-bldg | %bot | %empty | persist: %big-absorb-shots on healed / max absorb | defbuild rr (n) | rot/1k gr, %near vs base | heal %resp, med lat, spawn% | launcher: enemy throws, %thrown<=3r, med lat, min gap | siege %repl, med idle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ouroboros | 85 | 1 | 52380 | 67.0 | 44.8 | 19.3 | 11.6 | 99.3% (66 bldgs) / 677 | 1.2 (n=1471) | 17.7, 89.2% vs 23.7% | 79.3%, 8, 4.0% | 0, n/a% (n=0), n/a, n/a | 29.3%, 39.0 |
| Kings College Munich | 95 | 2 | 27455 | 72.0 | 31.4 | 19.3 | 8.6 | 98.5% (31 bldgs) / 427 | 1.2 (n=1302) | 3.6, 99.4% vs 41.6% | 66.1%, 27.0, 27.2% | 0, n/a% (n=0), n/a, 1 | 32.3%, 13.0 |
| Lunds Stallions | 115 | 5 | 51964 | 76.7 | 26.1 | 14.9 | 8.2 | 99.4% (46 bldgs) / 428 | 1.2 (n=1178) | 18.4, 87.6% vs 45.1% | 70.5%, 9, 19.1% | 1720, 98.6% (n=1760), 1.0, 1 | 34.4%, 11 |
| Memtrace | 70 | 4 | 8759 | 85.7 | 5.1 | 8.4 | 1.4 | n/a% (0 bldgs) / 7 | 1.1 (n=219) | 0.0, n/a% vs 92.2% | 31.5%, 1, 14.6% | 8734, 92.7% (n=9426), 0, 1 | 43.1%, 1 |
| CtrlAltDefeat | 75 | 5 | 23150 | 75.3 | 29.2 | 17.4 | 7.3 | 98.2% (32 bldgs) / 258 | 1.1 (n=1064) | 11.2, 97.5% vs 42.3% | 64.5%, 38.5, 37.8% | 0, 0.0% (n=1), n/a, 1 | 33.6%, 5.5 |
| Powerpuff Girls | 85 | 10 | 42107 | 68.9 | 42.7 | 19.4 | 11.2 | 97.9% (70 bldgs) / 634 | 1.0 (n=1957) | 11.8, 95.9% vs 35.7% | 73.8%, 4, 6.3% | 0, n/a% (n=0), n/a, n/a | 22.2%, 139 |
| Leviathan | 75 | 6 | 15178 | 91.4 | 27.5 | 3.9 | 4.7 | 99.0% (14 bldgs) / 446 | 1.1 (n=1349) | 11.8, 99.3% vs 95.6% | 43.8%, 8, 8.1% | 0, n/a% (n=0), n/a, n/a | 61.9%, 3.0 |
| Orizon | 25 | 1 | 7831 | 80.9 | 31.3 | 12.7 | 6.4 | 99.2% (14 bldgs) / 318 | 1.0 (n=205) | 2.7, 91.9% vs 46.2% | 49.2%, 3, 20.4% | 0, n/a% (n=0), n/a, n/a | 38.2%, 2.0 |
| OopsGotYourElo | 75 | 1 | 19905 | 84.5 | 40.3 | 10.7 | 4.9 | 99.4% (34 bldgs) / 531 | 1.1 (n=693) | 0.0, n/a% vs 61.7% | 79.2%, 5, 5.7% | 858, 74.7% (n=1149), 1.0, 1 | 18.9%, 18.5 |
| Team 48 | 85 | 1 | 10728 | 95.8 | 1.5 | 3.4 | 0.8 | n/a% (0 bldgs) / 8 | 1.0 (n=116) | 0.0, n/a% vs 89.1% | 17.3%, 70.5, 24.5% | 0, n/a% (n=0), n/a, 1 | 17.2%, 1 |
| Askar City | 65 | 2 | 3657 | 92.5 | 6.7 | 6.6 | 0.7 | n/a% (0 bldgs) / 10 | 1.0 (n=53) | 1.0, 100.0% vs 83.3% | 43.5%, 0.0, 10.3% | 27, 65.9% (n=41), 1, 1 | 17.6%, 1.0 |
| Banminary | 50 | 3 | 3403 | 90.1 | 3.5 | 9.0 | 0.9 | n/a% (0 bldgs) / 7 | 1.0 (n=159) | 155.6, 95.5% vs 84.2% | 56.5%, 6, 14.1% | 0, 0.0% (n=32), n/a, 1 | 16.2%, 10.0 |
| 0033 | 45 | 2 | 3759 | 87.8 | 21.6 | 7.4 | 4.3 | 100.0% (2 bldgs) / 27 | 1.1 (n=157) | 8.5, 96.8% vs 69.3% | 60.0%, 1, 7.3% | 0, n/a% (n=0), n/a, n/a | 14.3%, 2 |
| I Stone | 40 | 6 | 7898 | 78.7 | 30.1 | 12.0 | 8.2 | 99.3% (2 bldgs) / 672 | 1.1 (n=448) | 6.2, 94.2% vs 13.9% | 38.7%, 1.0, 9.5% | 0, n/a% (n=0), n/a, n/a | 56.5%, 25 |
| opensverige - plan B | 25 | 4 | 3792 | 90.3 | 5.3 | 8.1 | 1.3 | 80.0% (1 bldgs) / 25 | 1.1 (n=47) | 41.7, 97.0% vs 70.6% | 64.8%, 5, 10.4% | 375, 100.0% (n=375), 1, 1 | 25.0%, 2.0 |
| The Bisons | 20 | 1 | 2376 | 90.8 | 3.1 | 8.1 | 1.1 | n/a% (0 bldgs) / 7 | 1.0 (n=60) | 0.0, n/a% vs 89.2% | 0.0%, n/a, n/a% | 0, n/a% (n=0), n/a, n/a | 37.8%, 1.0 |
| farming_200s | 20 | 3 | 2859 | 96.4 | 6.4 | 2.1 | 1.5 | 95.0% (1 bldgs) / 20 | 1.0 (n=183) | 8.3, 87.2% vs 87.1% | 9.5%, 2, 0.0% | 0, n/a% (n=0), n/a, n/a | 80.6%, 1 |
| Focalground | 20 | 3 | 584 | 100.0 | 0.0 | 0.0 | 0.0 | n/a% (0 bldgs) / 0 | 1.2 (n=65) | 0.0, n/a% vs n/a% | 67.0%, 0, 6.3% | 1031, 87.4% (n=1180), 0, 1 | 0.0%, 0 |
| gsxWins | 20 | 1 | 2893 | 99.3 | 1.1 | 0.5 | 0.2 | n/a% (0 bldgs) / 19 | 1.1 (n=30) | 0.0, n/a% vs 93.3% | 72.4%, 1, 14.1% | 27, 100.0% (n=27), 0, 1 | 0.0%, 1.0 |

### How to read the columns

| column | meaning | proxy? |
| --- | --- | --- |
| `%bldg / %noncore-bldg / %bot / %empty` | class of the tile the `fireTurret` `to` landed on, from live tile state at event time | **what got hit, not what was aimed at** - a gunner shot is stopped by the first obstacle, so this is a joint function of their targeting AND our building placement. That is the right quantity for drain-bait (it prices what a body in the line absorbs) but it is NOT evidence of intent. |
| `persist: %big-absorb-shots on healed / max absorb` | of shots landing on a non-core building that absorbed >=20 shots in its life, the share that fell within +/-2 rounds of a heal on that tile; and the largest number of shots a single non-core building ever absorbed | direct, but the +/-2-round heal window is a proxy for "HP is not dropping" |
| `defbuild rr` | case-crossover: enemy-bot-rounds within d2<=13 of the build tile in r-20..r-1 vs the SAME tile in r-60..r-41 | **weak instrument, see caveat below** |
| `rot/1k gr, %near vs base` | rotations per 1,000 gunner-alive-rounds; share of rotations with our bot within d2<=13 in the last 3 rounds vs the share of all gunner-rounds with our bot that close | direct and strong |
| `heal %resp, med lat, spawn%` | of first-damage-on-a-building events, share ever followed by a heal within d2<=4; median round gap; share of responses where the healer was born AFTER the damage | direct |
| `launcher` | enemy-bot throws; share of enemy-bot adjacency episodes (d2<=2 at end of round) followed by a throw of that bot within 3 rounds; median latency; smallest inter-throw gap for a launcher that was the ONLY launcher in range | direct; ambiguous-attribution throws excluded |
| `siege %repl, med idle` | share of core-shooter deaths followed within 20 rounds by a new shooter born at d2<=25; median rounds between a shooter's last shot and its death (or game end) | direct |

## The headline: drain-bait is LIVE against everyone except the launcher bots

**Non-core buildings absorbing enemy turret fire, per game, vs OpenSverige:**

```
team                     games nonCoreShots/g bldgs>=20sh/g maxAbsorb  %shots_on_healed  %bigshots_healed
Ouroboros                   85          276.2          0.78       677              64.8              99.3
Kings College Munich        95           90.7          0.33       427              64.3              98.5
Lunds Stallions            115          117.9          0.40       428              55.5              99.4
Memtrace                    70            6.4          0.00         7              39.8               0.0
CtrlAltDefeat               75           90.3          0.43       258              68.6              98.2
Powerpuff Girls             85          211.7          0.82       634              67.7              97.9
Leviathan                   75           55.6          0.19       446              58.9              99.0
Orizon                      25           97.9          0.56       318              71.7              99.2
OopsGotYourElo              75          106.9          0.45       531              85.7              99.4
Team 48                     85            1.8          0.00         8              36.9               0.0
Askar City                  65            3.8          0.00        10              13.0               0.0
Banminary                   50            2.4          0.00         7              12.7               0.0
0033                        45           18.0          0.04        27              38.4             100.0
I Stone                     40           59.4          0.05       672              59.3              99.3
opensverige - plan B        25            8.0          0.04        25              52.2              80.0
The Bisons                  20            3.7          0.00         7              59.5               0.0
farming_200s                20            9.1          0.05        20              36.3              95.0
Focalground                 20            0.0          0.00         0               0.0               0.0
gsxWins                     20            1.6          0.00        19              90.9               0.0
```

Read the `%bigshots_healed` column. For every opponent that puts >=50 shots per
game into our non-core buildings, **97.9-99.4% of the shots that landed on a
heavily-absorbing building fell within +/-2 rounds of a heal on that tile.**
They do not re-target when the HP stops dropping. The single worst case is a
**Ouroboros gunner line that put 677 shots into ONE of our conveyors**
(2,708 ammo = 2,708 Ti at 1:1 conversion, against a 3 Ti conveyor plus heal
upkeep). Powerpuff 634, OopsGotYourElo 531, Leviathan 446, Lunds 428, KCM 427.

**Barrier bait specifically** is under-observed because we rarely place barriers
in their lines - but where it happened, every opponent that shot one shot it
**a median of 4 times** (Ouroboros n=29, KCM n=30, Powerpuff n=150, Lunds n=23,
CtrlAltDefeat n=9, Leviathan n=5, Orizon n=6, OopsGotYourElo n=14, Team 48
n=13, Askar n=6). Median 4 shots on a 30 HP barrier is exactly the 7-dmg gunner
killing it - i.e. **they shoot it dead rather than shoot past it**. n is small
per opponent; flag as suggestive, not settled.

**Where barrier bait is DEAD**: Memtrace (5.1% non-core building shots, max
absorb 7), Team 48 (1.5%, max 8), Askar City (6.7%, max 10), Banminary (3.5%,
max 7), The Bisons (3.1%, max 7), gsxWins (1.1%), Focalground (0.0% -
584 shots, every one on the core). These teams' turrets sit with a clear line
to the core; nothing of ours is ever in the way, and nothing of ours ever
absorbs meaningfully.

Full per-target-kind absorb table:

```
team                    kind       nbldg   shots   mean  med  p90   max run_mean run_max
Ouroboros               conveyor    4224   20612    4.9    2    5   677      4.2     677
Ouroboros               harvester    170    1453    8.5    4    8   622      7.5     622
Ouroboros               barrier       29     115    4.0    4    4     5      3.0       4
Ouroboros               gunner        93     299    3.2    3    4     8      2.6       6
Ouroboros               sentinel     142     844    5.9    5   11    18      3.9      13
Ouroboros               launcher      39     156    4.0    4    4     4      2.9       4
Ouroboros               core          61   11592  190.0  136  330   833     31.1     655

Kings College Munich    conveyor    1291    6459    5.0    2    7   427      4.4     427
Kings College Munich    harvester     81     506    6.2    4   11    26      5.2      26
Kings College Munich    barrier       30     143    4.8    4    8    12      4.2      12
Kings College Munich    gunner       145     544    3.8    3    6    43      2.9      38
Kings College Munich    sentinel     112     786    7.0    5   11    39      5.5      39
Kings College Munich    launcher      46     181    3.9    4    4     4      3.6       4
Kings College Munich    core          90   11155  123.9   97  262   638     30.2     340

Lunds Stallions         conveyor    2530    9913    3.9    2    5   428      3.6     428
Lunds Stallions         harvester    436    2531    5.8    4    8    74      5.4      74
Lunds Stallions         barrier       23     125    5.4    4    6    30      4.0      30
Lunds Stallions         gunner       130     347    2.7    3    3     6      2.4       6
Lunds Stallions         sentinel     121     522    4.3    4    5    11      3.6      11
Lunds Stallions         launcher      30     118    3.9    4    4     4      3.9       4
Lunds Stallions         core         108   26324  243.7  176  518  1500     60.7     917

Memtrace                conveyor     156     313    2.0    2    2     6      1.9       6
Memtrace                harvester     16      39    2.4    2    3     7      2.4       7
Memtrace                gunner        25      53    2.1    2    2     5      2.1       5
Memtrace                sentinel       8      30    3.8    4    5     5      3.0       5
Memtrace                core          44    7058  160.4   35  341  1593     50.8     907

CtrlAltDefeat           conveyor     890    5045    5.7    3    7   258      5.1     258
CtrlAltDefeat           harvester     81     583    7.2    5    9    71      5.8      71
CtrlAltDefeat           barrier        9      35    3.9    4   11    11      2.9       8
CtrlAltDefeat           gunner       132     367    2.8    3    3     6      2.4       6
CtrlAltDefeat           sentinel      67     604    9.0    5   11   160      7.8     102
CtrlAltDefeat           launcher      36     136    3.8    4    4     4      3.4       4
CtrlAltDefeat           core          72   10657  148.0  102  308  1017     30.7     335

Powerpuff Girls         conveyor    2968   14196    4.8    2    5   634      4.2     634
Powerpuff Girls         harvester    321    1864    5.8    4    8    67      5.1      59
Powerpuff Girls         barrier      150     921    6.1    5    8    12      6.0      12
Powerpuff Girls         gunner       126     345    2.7    3    3    11      2.3      11
Powerpuff Girls         sentinel     124     600    4.8    5    9    19      3.4      13
Powerpuff Girls         launcher      18      65    3.6    4    4     4      3.2       4
Powerpuff Girls         core          46   11031  239.8  130  654   991     79.9     598

Leviathan               conveyor     383    2193    5.7    2    5   446      5.3     446
Leviathan               harvester      6      36    6.0    4   11    11      6.0      11
Leviathan               barrier        5      15    3.0    4    4     4      3.0       4
Leviathan               gunner       239    1020    4.3    3    6   123      2.6      72
Leviathan               sentinel     123     801    6.5    5   11    29      5.1      27
Leviathan               launcher      24     102    4.2    4    4    12      3.5       8
Leviathan               core          65    9705  149.3   85  417   881     23.6     364

Orizon                  conveyor     262    2025    7.7    3    8   318      7.0     318
Orizon                  barrier        6      24    4.0    4    4     4      2.7       4
Orizon                  gunner        33      96    2.9    3    3     3      2.4       3
Orizon                  sentinel      49     270    5.5    5   11    13      3.6      11
Orizon                  core          25    3891  155.6  120  280   681     29.3     579

OopsGotYourElo          conveyor     409    6807   16.6    5   14   531     15.3     531
OopsGotYourElo          harvester      7      87   12.4    7   47    47      8.7      27
OopsGotYourElo          barrier       14      61    4.4    4    6     8      4.4       8
OopsGotYourElo          gunner       156     452    2.9    3    3     3      2.5       3
OopsGotYourElo          sentinel      98     601    6.1    5   11    22      4.8      22
OopsGotYourElo          core          47    8796  187.1  102  491  1654     59.8     712

Team 48                 conveyor      30      76    2.5    2    4     8      2.4       8
Team 48                 barrier       13      66    5.1    4    8     8      5.1       8
Team 48                 sentinel       5      11    2.2    2    4     4      2.2       4
Team 48                 core          82   10116  123.4  102  206   346     30.7     258

Askar City              conveyor      83     170    2.0    2    2    10      2.0      10
Askar City              harvester      5       9    1.8    2    2     2      1.8       2
Askar City              barrier        6      29    4.8    4    8     8      4.8       8
Askar City              sentinel      13      34    2.6    3    3     5      2.4       3
Askar City              core          55    3136   57.0   40  109   287     25.3     281

Banminary               conveyor      33      74    2.2    2    3     7      2.0       7
Banminary               harvester      6      18    3.0    2    6     6      2.6       4
Banminary               core          50    2948   59.0   46  107   215     15.4      86

0033                    conveyor     131     310    2.4    2    3    19      2.2      19
0033                    harvester     19      85    4.5    3    8    27      4.0      27
0033                    gunner        37     100    2.7    3    3     3      2.6       3
0033                    sentinel      51     291    5.7    5    9    26      4.3      26
0033                    launcher       6      18    3.0    3    4     4      3.0       4
0033                    core          35    2488   71.1   51  199   262     25.1     260

I Stone                 conveyor     416    1828    4.4    2    5   672      3.6     590
I Stone                 harvester     72     329    4.6    4    7    12      3.0      12
I Stone                 gunner        32      90    2.8    3    3     8      2.2       8
I Stone                 sentinel      23     111    4.8    4    6    11      3.6      11
I Stone                 core          29    3838  132.3   59  459   488     35.2     488

opensverige - plan B    conveyor      43     149    3.5    2    8    25      3.1      25
opensverige - plan B    gunner         5       8    1.6    2    2     2      1.6       2
opensverige - plan B    sentinel      11      42    3.8    4    5     5      2.8       5
opensverige - plan B    core          24    3222  134.2   88  457   486     57.5     486

The Bisons              conveyor      21      58    2.8    2    5     5      2.6       5
The Bisons              core          20    2084  104.2   54  412   494     27.4     254

farming_200s            conveyor      43     154    3.6    2    6    20      3.3      20
farming_200s            core          18    2574  143.0  109  332   596     14.5     327

Focalground             core          12     584   48.7   37   67   128     16.7     128

gsxWins                 core          20    2840  142.0   88  524   661     48.1     405

```

## Column-by-column caveats

1. **Turret target class** - solid n everywhere (>=2,376 shots per opponent in
   the summary table). The `to` field is the tile the shot resolved on. Treat
   it as "what a body in the line absorbs", not "what they chose".
2. **Build-on-sight - NEAR-NULL, DO NOT ACT ON IT.** Rate ratios sit at
   1.0-1.2 with the naive place-permutation control at 78-100% and the
   case-crossover control barely below the case window. The reason is
   power, not absence of an effect: our bots roam the whole map, so "an enemy
   bot was within d2<=32 in the last 20 rounds" is true for 76-100% of
   *every* candidate tile at *every* time. **This instrument cannot separate
   reaction from ambient presence, and I am reporting it as unmeasured rather
   than as a null.** A sharper design would need first-ever-arrival-per-flank
   events on maps where a flank is genuinely never visited; the corpus has few.
3. **Rotate-on-sight - measurable and sharp.** See the per-opponent section.
4. **Healer relocation** - solid n (299-1,584 first-damage triggers per
   opponent). One caveat: the trigger is the FIRST damage on a given building,
   so repeat damage on the same building is not re-counted, and "responded" is
   right-censored by game length.
5. **Launcher trigger** - adjacency is sampled at END of round, so a bot that
   walks in and is thrown in the same round is invisible to the episode counter;
   those throws are added back as latency-0 episodes. Inter-throw gaps use only
   throws where exactly one launcher of either team was within d2<=2, so the
   cooldown estimate is not contaminated by multi-launcher batteries.
6. **Siege persistence** - "idle after last fire" is measured here (the prior
   `shooters.tsv` had no last-shot column, so this is new, not a re-cut).

## Version drift

```
Ouroboros: single version (['8']) - no drift risk
Kings College Munich:
   v   1 sides= 50 shots= 10369 bldg%= 75.3 nonCoreBldg%= 20.1 bot%= 17.5 rot/1kgr=   3.0 heal_resp%= 69.0 heal_lat_med=17.0 adj_n=0 thrown3%=None
   v   8 sides= 45 shots= 17086 bldg%= 70.1 nonCoreBldg%= 38.3 bot%= 20.5 rot/1kgr=   4.0 heal_resp%= 62.4 heal_lat_med=35.0 adj_n=0 thrown3%=None
Lunds Stallions:
   v  44 sides= 70 shots= 34829 bldg%= 75.8 nonCoreBldg%= 23.6 bot%= 16.2 rot/1kgr=  20.9 heal_resp%= 72.2 heal_lat_med=11.0 adj_n=648 thrown3%=99.38271604938272
   v  42 sides= 20 shots=  7274 bldg%= 75.6 nonCoreBldg%= 37.8 bot%= 14.2 rot/1kgr=  14.1 heal_resp%= 68.1 heal_lat_med=11 adj_n=358 thrown3%=100.0
   v  45 sides= 15 shots=  6863 bldg%= 84.2 nonCoreBldg%= 23.3 bot%=  9.7 rot/1kgr=  14.6 heal_resp%= 74.6 heal_lat_med=1.0 adj_n=728 thrown3%=97.25274725274726
   v  37 sides=  5 shots=  1835 bldg%= 69.0 nonCoreBldg%= 41.4 bot%= 14.9 rot/1kgr=  12.3 heal_resp%= 59.6 heal_lat_med=8.5 adj_n=17 thrown3%=100.0
   v  50 sides=  5 shots=  1163 bldg%= 79.7 nonCoreBldg%= 19.3 bot%= 12.9 rot/1kgr=  32.4 heal_resp%= 57.1 heal_lat_med=5.5 adj_n=9 thrown3%=100.0
Memtrace:
   v  33 sides= 35 shots=  3127 bldg%= 81.7 nonCoreBldg%=  6.4 bot%= 11.0 rot/1kgr=   0.0 heal_resp%= 18.4 heal_lat_med=33 adj_n=5860 thrown3%=99.50511945392492
   v  36 sides= 25 shots=  4892 bldg%= 89.2 nonCoreBldg%=  2.1 bot%=  5.6 rot/1kgr=   0.0 heal_resp%= 48.3 heal_lat_med=0 adj_n=2733 thrown3%=89.49871935601902
   v  34 sides=  5 shots=   440 bldg%= 90.5 nonCoreBldg%=  4.1 bot%=  4.8 rot/1kgr=   0.0 heal_resp%= 32.1 heal_lat_med=63 adj_n=684 thrown3%=66.95906432748538
   v  27 sides=  5 shots=   300 bldg%= 62.7 nonCoreBldg%= 41.3 bot%= 31.7 rot/1kgr=   0.0 heal_resp%= 34.8 heal_lat_med=6.0 adj_n=149 thrown3%=0.0
CtrlAltDefeat:
   v 117 sides= 35 shots=  9820 bldg%= 69.7 nonCoreBldg%= 26.4 bot%= 21.5 rot/1kgr=   4.5 heal_resp%= 61.2 heal_lat_med=38 adj_n=0 thrown3%=None
   v 107 sides= 20 shots=  6220 bldg%= 86.9 nonCoreBldg%= 24.2 bot%=  9.2 rot/1kgr=  19.6 heal_resp%= 68.5 heal_lat_med=58 adj_n=1 thrown3%=0.0
   v 116 sides= 10 shots=  1973 bldg%= 75.4 nonCoreBldg%= 19.1 bot%= 17.6 rot/1kgr=  53.9 heal_resp%= 78.5 heal_lat_med=31.5 adj_n=0 thrown3%=None
   v 120 sides=  5 shots=  2399 bldg%= 80.2 nonCoreBldg%= 40.9 bot%= 12.9 rot/1kgr=   5.1 heal_resp%= 61.7 heal_lat_med=31.5 adj_n=0 thrown3%=None
   v 118 sides=  5 shots=  2738 bldg%= 64.2 nonCoreBldg%= 48.1 bot%= 24.8 rot/1kgr=   1.9 heal_resp%= 51.3 heal_lat_med=30.5 adj_n=0 thrown3%=None
Powerpuff Girls:
   v  46 sides= 20 shots= 16656 bldg%= 70.4 nonCoreBldg%= 47.9 bot%= 18.3 rot/1kgr=  10.2 heal_resp%= 73.8 heal_lat_med=8.0 adj_n=0 thrown3%=None
   v  35 sides= 15 shots=  6938 bldg%= 76.9 nonCoreBldg%= 37.8 bot%= 14.4 rot/1kgr=  12.3 heal_resp%= 74.0 heal_lat_med=4.0 adj_n=0 thrown3%=None
   v  18 sides= 15 shots=  3212 bldg%= 76.1 nonCoreBldg%= 45.9 bot%= 15.0 rot/1kgr=   6.6 heal_resp%= 78.1 heal_lat_med=7.0 adj_n=0 thrown3%=None
   v  45 sides=  5 shots=  3016 bldg%= 58.1 nonCoreBldg%= 36.5 bot%= 27.6 rot/1kgr=  15.0 heal_resp%= 61.9 heal_lat_med=16.0 adj_n=0 thrown3%=None
   v  21 sides=  5 shots=   760 bldg%= 78.6 nonCoreBldg%= 41.4 bot%= 12.2 rot/1kgr=   9.7 heal_resp%= 79.8 heal_lat_med=1 adj_n=0 thrown3%=None
   v  26 sides=  5 shots=   600 bldg%= 70.5 nonCoreBldg%= 46.5 bot%= 16.2 rot/1kgr=  16.3 heal_resp%= 57.1 heal_lat_med=2.0 adj_n=0 thrown3%=None
   v  23 sides=  5 shots=  1034 bldg%= 57.0 nonCoreBldg%= 52.6 bot%= 21.4 rot/1kgr=  13.0 heal_resp%= 71.4 heal_lat_med=7.0 adj_n=0 thrown3%=None
   v  42 sides=  5 shots=  3910 bldg%= 62.0 nonCoreBldg%= 52.5 bot%= 24.2 rot/1kgr=  22.5 heal_resp%= 75.9 heal_lat_med=2 adj_n=0 thrown3%=None
   v  40 sides=  5 shots=  3017 bldg%= 67.6 nonCoreBldg%= 23.1 bot%= 21.7 rot/1kgr=   9.4 heal_resp%= 68.8 heal_lat_med=4 adj_n=0 thrown3%=None
   v  48 sides=  5 shots=  2964 bldg%= 57.1 nonCoreBldg%= 31.3 bot%= 26.6 rot/1kgr=  14.3 heal_resp%= 80.0 heal_lat_med=8.0 adj_n=0 thrown3%=None
Leviathan:
   v  25 sides= 30 shots=  9065 bldg%= 92.7 nonCoreBldg%= 19.4 bot%=  4.3 rot/1kgr=  10.6 heal_resp%= 36.7 heal_lat_med=10.0 adj_n=0 thrown3%=None
   v  35 sides= 20 shots=  3109 bldg%= 89.7 nonCoreBldg%= 29.1 bot%=  3.6 rot/1kgr=  19.6 heal_resp%= 52.3 heal_lat_med=4.0 adj_n=0 thrown3%=None
   v  32 sides= 10 shots=  1530 bldg%= 91.4 nonCoreBldg%= 41.4 bot%=  2.9 rot/1kgr=   2.4 heal_resp%= 44.0 heal_lat_med=7.0 adj_n=0 thrown3%=None
   v  34 sides=  5 shots=   549 bldg%= 84.7 nonCoreBldg%= 46.6 bot%=  2.4 rot/1kgr=  35.4 heal_resp%= 63.8 heal_lat_med=5.0 adj_n=0 thrown3%=None
   v  27 sides=  5 shots=   317 bldg%= 78.2 nonCoreBldg%= 47.6 bot%= 10.7 rot/1kgr=  13.5 heal_resp%= 32.1 heal_lat_med=9 adj_n=0 thrown3%=None
   v  33 sides=  5 shots=   608 bldg%= 93.1 nonCoreBldg%= 75.5 bot%=  0.0 rot/1kgr=   6.1 heal_resp%= 48.8 heal_lat_med=27.5 adj_n=0 thrown3%=None
Orizon: single version (['34']) - no drift risk
OopsGotYourElo: single version (['21']) - no drift risk
```

The qualitative gates hold across versions: **Memtrace never rotates in ANY of
its four versions**; Ouroboros/KCM/CtrlAltDefeat/Powerpuff/Leviathan/Orizon
throw **zero** enemy builders in every version; building-shot share stays in
57-93% for everyone. The quantitative columns drift a lot - Memtrace's
throw-on-adjacency runs 99.5% (v33) / 89.5% (v36) / 67% (v34) / 0% (v27, n=149,
old); CtrlAltDefeat's rotation rate runs 1.9-53.9 per 1k gunner-rounds across
five versions. **Do not quote a per-opponent number to two digits without
naming the version mix.**

## Per-opponent detail

```
# scope: vs OpenSverige only

## Ouroboros   sides=85  versions={'8': 85}
  SHOTS n=52380  bot=19.3127147766323  bldg=66.95494463535701  empty=11.62848415425735  own=2.1038564337533407  oor=0
   bldg split: core=11592 barrier=115 conveyor=20612 splitter=0 harvester=1453 gunner=299 sentinel=844 launcher=156
   gunner: n=52380 bot=19.3% bldg=67.0% (non-core 44.8%) empty=11.6%
  SHOTS-ON-HEALED-BLDG 17667/35071 = 50.37495366542157
  DEFBUILD[all] n=1755 sighted20=85.7% permctrl=78.7% ratio=1.09 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1471: d2<=13 10.42 vs 8.95 rr=1.16 | d2<=32 14.20 vs 13.32 rr=1.07
  DEFBUILD[turret] n=1755 sighted20=85.7% permctrl=78.7% ratio=1.09 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1471: d2<=13 10.42 vs 8.95 rr=1.16 | d2<=32 14.20 vs 13.32 rr=1.07
  ROT n=7995 with_enemy_near(3r,d2<=13)=89.18073796122576 | baseline gunner-rounds-with-enemy-near=23.67671676955917 (gunner-rounds=451604) | rot per 1k gunner-rounds=17.7
  HEAL trig=1381 responded=79.29036929761043 lat_med=8 lat_p25/75=1/27 modes={'already': 664, 'walked': 387, 'none': 286, 'spawned': 44}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=0 throws=0 (enemy 0 / own 0) | inter-throw n=0 min=None p10=None med=None
  SIEGE shooters=1448 deaths=542 replaced<=20r&d2<=25=29.33579335793358 idle_after_last_fire_med=39.0

## Kings College Munich   sides=95  versions={'8': 45, '1': 50}
  SHOTS n=27455  bot=19.329812420324167  bldg=72.02331087233655  empty=8.646876707339283  own=0.0  oor=0
   bldg split: core=11155 barrier=143 conveyor=6459 splitter=0 harvester=506 gunner=544 sentinel=786 launcher=181
   gunner: n=21957 bot=23.8% bldg=65.4% (non-core 38.9%) empty=10.8%
   sentinel: n=5498 bot=1.6% bldg=98.4% (non-core 1.4%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 11647/19774 = 58.90057651461515
  DEFBUILD[all] n=1636 sighted20=96.1% permctrl=85.0% ratio=1.13 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1302: d2<=13 14.02 vs 11.86 rr=1.18 | d2<=32 17.51 vs 16.10 rr=1.09
  DEFBUILD[turret] n=1454 sighted20=97.9% permctrl=86.9% ratio=1.13 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1121: d2<=13 14.66 vs 11.96 rr=1.23 | d2<=32 17.96 vs 16.15 rr=1.11
  DEFBUILD[barrier] n=182 sighted20=81.9% permctrl=69.8% ratio=1.17 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=181: d2<=13 10.06 vs 11.27 rr=0.89 | d2<=32 14.75 vs 15.81 rr=0.93
  ROT n=1204 with_enemy_near(3r,d2<=13)=99.4186046511628 | baseline gunner-rounds-with-enemy-near=41.632643222379244 (gunner-rounds=331879) | rot per 1k gunner-rounds=3.6
  HEAL trig=1498 responded=66.08811748998664 lat_med=27.0 lat_p25/75=4/92 modes={'none': 508, 'spawned': 269, 'already': 563, 'walked': 158}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=72 throws=161 (enemy 0 / own 161) | inter-throw n=89 min=1 p10=1 med=1
  SIEGE shooters=1256 deaths=458 replaced<=20r&d2<=25=32.314410480349345 idle_after_last_fire_med=13.0

## Lunds Stallions   sides=115  versions={'42': 20, '45': 15, '44': 70, '37': 5, '50': 5}
  SHOTS n=51964  bot=14.933415441459472  bldg=76.7454391501809  empty=8.209529674389962  own=0.11161573396967131  oor=0
   bldg split: core=26324 barrier=125 conveyor=9913 splitter=0 harvester=2531 gunner=347 sentinel=522 launcher=118
   gunner: n=46564 bot=14.6% bldg=76.1% (non-core 28.7%) empty=9.2%
   sentinel: n=5400 bot=17.8% bldg=82.2% (non-core 3.8%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 15281/39880 = 38.31745235707121
  DEFBUILD[all] n=1524 sighted20=91.9% permctrl=85.6% ratio=1.07 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1178: d2<=13 13.20 vs 10.75 rr=1.23 | d2<=32 16.38 vs 14.38 rr=1.14
  DEFBUILD[turret] n=1524 sighted20=91.9% permctrl=85.6% ratio=1.07 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1178: d2<=13 13.20 vs 10.75 rr=1.23 | d2<=32 16.38 vs 14.38 rr=1.14
  ROT n=3269 with_enemy_near(3r,d2<=13)=87.58029978586724 | baseline gunner-rounds-with-enemy-near=45.10883670544691 (gunner-rounds=177238) | rot per 1k gunner-rounds=18.4
  HEAL trig=1346 responded=70.50520059435364 lat_med=9 lat_p25/75=1/55 modes={'none': 397, 'spawned': 181, 'already': 557, 'walked': 211}
  LAUNCH adj_eps=1760 thrown<=3r=98.63636363636364 lat_med=1.0 | launchers=115 throws=1993 (enemy 1720 / own 273) | inter-throw n=1882 min=1 p10=1 med=4.0
  SIEGE shooters=1411 deaths=855 replaced<=20r&d2<=25=34.3859649122807 idle_after_last_fire_med=11

## Memtrace   sides=70  versions={'36': 25, '33': 35, '34': 5, '27': 5}
  SHOTS n=8759  bot=8.379952049320698  bldg=85.68329718004338  empty=1.3700194086082886  own=4.566731362027629  oor=0
   bldg split: core=7058 barrier=6 conveyor=313 splitter=0 harvester=39 gunner=53 sentinel=30 launcher=6
   gunner: n=7855 bot=3.2% bldg=90.3% (non-core 0.4%) empty=1.5%
   sentinel: n=904 bot=53.0% bldg=45.8% (non-core 45.8%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 1093/7505 = 14.563624250499666
  DEFBUILD[all] n=328 sighted20=75.6% permctrl=77.1% ratio=0.98 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=219: d2<=13 14.03 vs 13.00 rr=1.08 | d2<=32 15.35 vs 14.75 rr=1.04
  DEFBUILD[turret] n=319 sighted20=76.8% permctrl=78.4% ratio=0.98 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=212: d2<=13 14.30 vs 13.30 rr=1.08 | d2<=32 15.67 vs 15.05 rr=1.04
  DEFBUILD[barrier] n=9 sighted20=33.3% permctrl=33.3% ratio=1.00 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=7: d2<=13 5.71 vs 4.14 rr=1.38 | d2<=32 5.71 vs 5.71 rr=1.00
  ROT n=0 with_enemy_near(3r,d2<=13)=None | baseline gunner-rounds-with-enemy-near=92.21919841662543 (gunner-rounds=8084) | rot per 1k gunner-rounds=0.0
  HEAL trig=498 responded=31.526104417670684 lat_med=1 lat_p25/75=0/24 modes={'none': 341, 'walked': 17, 'already': 117, 'spawned': 23}
  LAUNCH adj_eps=9426 thrown<=3r=92.66921281561638 lat_med=0 | launchers=203 throws=10103 (enemy 8734 / own 1369) | inter-throw n=9464 min=1 p10=1 med=3.0
  SIEGE shooters=213 deaths=116 replaced<=20r&d2<=25=43.10344827586207 idle_after_last_fire_med=1

## CtrlAltDefeat   sides=75  versions={'117': 35, '116': 10, '107': 20, '120': 5, '118': 5}
  SHOTS n=23150  bot=17.37365010799136  bldg=75.27861771058315  empty=7.347732181425486  own=0.0  oor=0
   bldg split: core=10657 barrier=35 conveyor=5045 splitter=0 harvester=583 gunner=367 sentinel=604 launcher=136
   gunner: n=18570 bot=21.5% bldg=69.3% (non-core 36.1%) empty=9.2%
   sentinel: n=4580 bot=0.7% bldg=99.3% (non-core 1.4%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 10360/17427 = 59.447983014862
  DEFBUILD[all] n=1289 sighted20=96.6% permctrl=87.2% ratio=1.11 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1064: d2<=13 14.67 vs 12.97 rr=1.13 | d2<=32 17.97 vs 16.93 rr=1.06
  DEFBUILD[turret] n=1105 sighted20=98.6% permctrl=88.8% ratio=1.11 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=882: d2<=13 15.62 vs 13.27 rr=1.18 | d2<=32 18.51 vs 17.13 rr=1.08
  DEFBUILD[barrier] n=184 sighted20=84.8% permctrl=77.7% ratio=1.09 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=182: d2<=13 10.05 vs 11.51 rr=0.87 | d2<=32 15.35 vs 15.96 rr=0.96
  ROT n=2343 with_enemy_near(3r,d2<=13)=97.48186086214255 | baseline gunner-rounds-with-enemy-near=42.28329406377885 (gunner-rounds=209662) | rot per 1k gunner-rounds=11.2
  HEAL trig=1306 responded=64.47166921898928 lat_med=38.5 lat_p25/75=8/140 modes={'spawned': 318, 'none': 464, 'walked': 139, 'already': 385}
  LAUNCH adj_eps=1 thrown<=3r=0.0 lat_med=None | launchers=71 throws=171 (enemy 0 / own 171) | inter-throw n=100 min=1 p10=1 med=1.0
  SIEGE shooters=954 deaths=444 replaced<=20r&d2<=25=33.55855855855856 idle_after_last_fire_med=5.5

## Powerpuff Girls   sides=85  versions={'35': 15, '45': 5, '21': 5, '46': 20, '26': 5, '18': 15, '23': 5, '42': 5, '40': 5, '48': 5}
  SHOTS n=42107  bot=19.40057472629254  bldg=68.92440686821669  empty=11.162039565867907  own=0.5129788396228656  oor=0
   bldg split: core=11031 barrier=921 conveyor=14196 splitter=0 harvester=1864 gunner=345 sentinel=600 launcher=65
   gunner: n=33686 bot=23.2% bldg=62.2% (non-core 52.1%) empty=14.0%
   sentinel: n=8421 bot=4.2% bldg=95.8% (non-core 5.0%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 19366/29022 = 66.72868858107643
  DEFBUILD[all] n=2216 sighted20=86.0% permctrl=81.0% ratio=1.06 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1957: d2<=13 11.36 vs 10.98 rr=1.03 | d2<=32 15.10 vs 14.96 rr=1.01
  DEFBUILD[turret] n=1483 sighted20=89.1% permctrl=83.2% ratio=1.07 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1232: d2<=13 12.13 vs 11.17 rr=1.09 | d2<=32 15.76 vs 15.30 rr=1.03
  DEFBUILD[barrier] n=733 sighted20=79.7% permctrl=76.7% ratio=1.04 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=725: d2<=13 10.04 vs 10.65 rr=0.94 | d2<=32 13.98 vs 14.37 rr=0.97
  ROT n=6267 with_enemy_near(3r,d2<=13)=95.93106749640977 | baseline gunner-rounds-with-enemy-near=35.68989828723984 (gunner-rounds=531890) | rot per 1k gunner-rounds=11.8
  HEAL trig=1185 responded=73.83966244725738 lat_med=4 lat_p25/75=1/26 modes={'none': 310, 'walked': 187, 'already': 633, 'spawned': 55}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=0 throws=0 (enemy 0 / own 0) | inter-throw n=0 min=None p10=None med=None
  SIEGE shooters=1201 deaths=189 replaced<=20r&d2<=25=22.22222222222222 idle_after_last_fire_med=139

## Leviathan   sides=75  versions={'34': 5, '25': 30, '35': 20, '27': 5, '32': 10, '33': 5}
  SHOTS n=15178  bot=3.9135590986954805  bldg=91.39544076953486  empty=4.691000131769667  own=0.0  oor=0
   bldg split: core=9705 barrier=15 conveyor=2193 splitter=0 harvester=36 gunner=1020 sentinel=801 launcher=102
   gunner: n=11824 bot=4.9% bldg=89.1% (non-core 34.9%) empty=6.0%
   sentinel: n=3354 bot=0.4% bldg=99.6% (non-core 1.2%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 6739/13872 = 48.57987312572088
  DEFBUILD[all] n=1660 sighted20=98.2% permctrl=97.5% ratio=1.01 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1349: d2<=13 18.38 vs 17.44 rr=1.05 | d2<=32 19.35 vs 19.07 rr=1.01
  DEFBUILD[turret] n=1453 sighted20=99.7% permctrl=98.1% ratio=1.02 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=1174: d2<=13 18.63 vs 17.95 rr=1.04 | d2<=32 19.68 vs 19.42 rr=1.01
  DEFBUILD[barrier] n=207 sighted20=87.9% permctrl=93.7% ratio=0.94 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=175: d2<=13 16.73 vs 14.02 rr=1.19 | d2<=32 17.12 vs 16.70 rr=1.02
  ROT n=300 with_enemy_near(3r,d2<=13)=99.33333333333333 | baseline gunner-rounds-with-enemy-near=95.56257402289775 (gunner-rounds=25330) | rot per 1k gunner-rounds=11.8
  HEAL trig=1432 responded=43.78491620111732 lat_med=8 lat_p25/75=1/57 modes={'already': 477, 'walked': 99, 'none': 805, 'spawned': 51}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=0 throws=0 (enemy 0 / own 0) | inter-throw n=0 min=None p10=None med=None
  SIEGE shooters=1086 deaths=942 replaced<=20r&d2<=25=61.8895966029724 idle_after_last_fire_med=3.0

## Orizon   sides=25  versions={'34': 25}
  SHOTS n=7831  bot=12.667603115821734  bldg=80.94751628144553  empty=6.3848806027327285  own=0.0  oor=0
   bldg split: core=3891 barrier=24 conveyor=2025 splitter=0 harvester=17 gunner=96 sentinel=270 launcher=16
   gunner: n=7831 bot=12.7% bldg=80.9% (non-core 31.3%) empty=6.4%
  SHOTS-ON-HEALED-BLDG 2984/6339 = 47.07367092601357
  DEFBUILD[all] n=340 sighted20=95.0% permctrl=88.8% ratio=1.07 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=205: d2<=13 15.60 vs 16.39 rr=0.95 | d2<=32 18.10 vs 18.59 rr=0.97
  DEFBUILD[turret] n=311 sighted20=94.5% permctrl=87.8% ratio=1.08 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=176: d2<=13 15.61 vs 16.38 rr=0.95 | d2<=32 18.09 vs 18.60 rr=0.97
  DEFBUILD[barrier] n=29 sighted20=100.0% permctrl=100.0% ratio=1.00 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=29: d2<=13 15.48 vs 16.48 rr=0.94 | d2<=32 18.17 vs 18.52 rr=0.98
  ROT n=136 with_enemy_near(3r,d2<=13)=91.91176470588235 | baseline gunner-rounds-with-enemy-near=46.242543139688514 (gunner-rounds=49954) | rot per 1k gunner-rounds=2.7
  HEAL trig=299 responded=49.163879598662206 lat_med=3 lat_p25/75=1/64 modes={'already': 100, 'none': 152, 'walked': 17, 'spawned': 30}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=0 throws=0 (enemy 0 / own 0) | inter-throw n=0 min=None p10=None med=None
  SIEGE shooters=270 deaths=173 replaced<=20r&d2<=25=38.15028901734104 idle_after_last_fire_med=2.0

## OopsGotYourElo   sides=75  versions={'21': 75}
  SHOTS n=19905  bot=10.6706857573474  bldg=84.46119065561416  empty=4.868123587038433  own=0.0  oor=0
   bldg split: core=8796 barrier=61 conveyor=6807 splitter=0 harvester=87 gunner=452 sentinel=601 launcher=8
   gunner: n=19905 bot=10.7% bldg=84.5% (non-core 40.3%) empty=4.9%
  SHOTS-ON-HEALED-BLDG 10484/16812 = 62.36021889126814
  DEFBUILD[all] n=1022 sighted20=91.7% permctrl=89.1% ratio=1.03 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=693: d2<=13 15.24 vs 14.22 rr=1.07 | d2<=32 17.75 vs 16.91 rr=1.05
  DEFBUILD[turret] n=550 sighted20=97.8% permctrl=91.5% ratio=1.07 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=431: d2<=13 16.56 vs 15.13 rr=1.09 | d2<=32 18.71 vs 17.36 rr=1.08
  DEFBUILD[barrier] n=472 sighted20=84.5% permctrl=86.4% ratio=0.98 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=262: d2<=13 13.08 vs 12.71 rr=1.03 | d2<=32 16.17 vs 16.16 rr=1.00
  ROT n=0 with_enemy_near(3r,d2<=13)=None | baseline gunner-rounds-with-enemy-near=61.68193488446438 (gunner-rounds=200198) | rot per 1k gunner-rounds=0.0
  HEAL trig=1584 responded=79.22979797979798 lat_med=5 lat_p25/75=1/33 modes={'already': 896, 'none': 329, 'walked': 288, 'spawned': 71}
  LAUNCH adj_eps=1149 thrown<=3r=74.67362924281984 lat_med=1.0 | launchers=37 throws=897 (enemy 858 / own 39) | inter-throw n=860 min=1 p10=1 med=2.0
  SIEGE shooters=446 deaths=227 replaced<=20r&d2<=25=18.94273127753304 idle_after_last_fire_med=18.5

## Team 48   sides=85  versions={'16': 85}
  SHOTS n=10728  bot=3.4395973154362416  bldg=95.75876211782251  empty=0.8016405667412378  own=0.0  oor=0
   bldg split: core=10116 barrier=66 conveyor=76 splitter=0 harvester=0 gunner=0 sentinel=11 launcher=4
   gunner: n=10728 bot=3.4% bldg=95.8% (non-core 1.5%) empty=0.8%
  SHOTS-ON-HEALED-BLDG 3260/10273 = 31.733670787501218
  DEFBUILD[all] n=384 sighted20=100.0% permctrl=100.0% ratio=1.00 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=116: d2<=13 17.67 vs 18.22 rr=0.97 | d2<=32 20.00 vs 19.97 rr=1.00
  DEFBUILD[turret] n=384 sighted20=100.0% permctrl=100.0% ratio=1.00 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=116: d2<=13 17.67 vs 18.22 rr=0.97 | d2<=32 20.00 vs 19.97 rr=1.00
  ROT n=0 with_enemy_near(3r,d2<=13)=None | baseline gunner-rounds-with-enemy-near=89.10091743119266 (gunner-rounds=24525) | rot per 1k gunner-rounds=0.0
  HEAL trig=612 responded=17.320261437908496 lat_med=70.5 lat_p25/75=2/184 modes={'none': 506, 'already': 66, 'spawned': 26, 'walked': 14}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=17 throws=37 (enemy 0 / own 37) | inter-throw n=20 min=1 p10=1 med=8.0
  SIEGE shooters=325 deaths=134 replaced<=20r&d2<=25=17.16417910447761 idle_after_last_fire_med=1

## Askar City   sides=65  versions={'73': 50, '75': 15}
  SHOTS n=3657  bot=6.61744599398414  bldg=92.4801750068362  empty=0.6836204539239814  own=0.21875854525567404  oor=0
   bldg split: core=3136 barrier=29 conveyor=170 splitter=0 harvester=9 gunner=0 sentinel=34 launcher=4
   gunner: n=1273 bot=5.5% bldg=92.4% (non-core 5.7%) empty=2.0%
   sentinel: n=2384 bot=7.2% bldg=92.5% (non-core 7.3%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 1524/3382 = 45.062093435836786
  DEFBUILD[all] n=176 sighted20=94.3% permctrl=93.8% ratio=1.01 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=53: d2<=13 13.51 vs 13.06 rr=1.03 | d2<=32 16.28 vs 15.92 rr=1.02
  DEFBUILD[turret] n=141 sighted20=97.2% permctrl=97.2% ratio=1.00 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=34: d2<=13 14.03 vs 13.82 rr=1.01 | d2<=32 17.91 vs 17.44 rr=1.03
  DEFBUILD[barrier] n=35 sighted20=82.9% permctrl=80.0% ratio=1.04 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=19: d2<=13 12.58 vs 11.68 rr=1.08 | d2<=32 13.37 vs 13.21 rr=1.01
  ROT n=8 with_enemy_near(3r,d2<=13)=100.0 | baseline gunner-rounds-with-enemy-near=83.29414838035528 (gunner-rounds=7656) | rot per 1k gunner-rounds=1.0
  HEAL trig=400 responded=43.5 lat_med=0.0 lat_p25/75=0/4 modes={'none': 226, 'spawned': 18, 'already': 135, 'walked': 21}
  LAUNCH adj_eps=41 thrown<=3r=65.85365853658537 lat_med=1 | launchers=44 throws=158 (enemy 27 / own 131) | inter-throw n=117 min=1 p10=1 med=6
  SIEGE shooters=132 deaths=68 replaced<=20r&d2<=25=17.647058823529413 idle_after_last_fire_med=1.0

## Banminary   sides=50  versions={'42': 15, '39': 5, '41': 30}
  SHOTS n=3403  bot=8.962679988245666  bldg=90.09697325888922  empty=0.940346752865119  own=0.0  oor=0
   bldg split: core=2948 barrier=6 conveyor=74 splitter=0 harvester=18 gunner=1 sentinel=10 launcher=9
   gunner: n=946 bot=2.1% bldg=94.5% (non-core 12.3%) empty=3.4%
   sentinel: n=2457 bot=11.6% bldg=88.4% (non-core 0.1%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 951/3066 = 31.01761252446184
  DEFBUILD[all] n=297 sighted20=98.3% permctrl=97.0% ratio=1.01 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=159: d2<=13 17.14 vs 17.05 rr=1.01 | d2<=32 19.33 vs 19.30 rr=1.00
  DEFBUILD[turret] n=297 sighted20=98.3% permctrl=97.0% ratio=1.01 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=159: d2<=13 17.14 vs 17.05 rr=1.01 | d2<=32 19.33 vs 19.30 rr=1.00
  ROT n=2435 with_enemy_near(3r,d2<=13)=95.52361396303901 | baseline gunner-rounds-with-enemy-near=84.22700837221193 (gunner-rounds=15647) | rot per 1k gunner-rounds=155.6
  HEAL trig=490 responded=56.53061224489796 lat_med=6 lat_p25/75=1/28 modes={'none': 213, 'spawned': 39, 'walked': 59, 'already': 179}
  LAUNCH adj_eps=32 thrown<=3r=0.0 lat_med=None | launchers=40 throws=47 (enemy 0 / own 47) | inter-throw n=8 min=1 p10=1 med=2.5
  SIEGE shooters=220 deaths=117 replaced<=20r&d2<=25=16.23931623931624 idle_after_last_fire_med=10.0

## 0033   sides=45  versions={'42': 20, '43': 25}
  SHOTS n=3759  bot=7.4487895716946  bldg=87.78930566640064  empty=4.256451183825486  own=0.5054535780792764  oor=0
   bldg split: core=2488 barrier=8 conveyor=310 splitter=0 harvester=85 gunner=100 sentinel=291 launcher=18
   gunner: n=1129 bot=21.7% bldg=62.4% (non-core 54.4%) empty=14.2%
   sentinel: n=2630 bot=1.3% bldg=98.7% (non-core 7.5%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 2031/3300 = 61.54545454545455
  DEFBUILD[all] n=284 sighted20=99.6% permctrl=97.2% ratio=1.03 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=157: d2<=13 16.78 vs 15.54 rr=1.08 | d2<=32 19.20 vs 18.41 rr=1.04
  DEFBUILD[turret] n=208 sighted20=99.5% permctrl=96.6% ratio=1.03 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=96: d2<=13 16.17 vs 15.34 rr=1.05 | d2<=32 18.84 vs 18.40 rr=1.02
  DEFBUILD[barrier] n=76 sighted20=100.0% permctrl=98.7% ratio=1.01 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=61: d2<=13 17.74 vs 15.85 rr=1.12 | d2<=32 19.75 vs 18.44 rr=1.07
  ROT n=95 with_enemy_near(3r,d2<=13)=96.84210526315789 | baseline gunner-rounds-with-enemy-near=69.29973998027437 (gunner-rounds=11153) | rot per 1k gunner-rounds=8.5
  HEAL trig=412 responded=59.95145631067961 lat_med=1 lat_p25/75=0/15 modes={'none': 165, 'spawned': 18, 'already': 165, 'walked': 64}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=0 throws=0 (enemy 0 / own 0) | inter-throw n=0 min=None p10=None med=None
  SIEGE shooters=187 deaths=70 replaced<=20r&d2<=25=14.285714285714286 idle_after_last_fire_med=2

## I Stone   sides=40  versions={'19': 10, '18': 5, '17': 5, '22': 5, '13': 10, '14': 5}
  SHOTS n=7898  bot=11.977715877437326  bldg=78.65282349962015  empty=8.204608761711826  own=1.1648518612306913  oor=0
   bldg split: core=3838 barrier=12 conveyor=1828 splitter=0 harvester=329 gunner=90 sentinel=111 launcher=4
   gunner: n=4090 bot=22.5% bldg=59.4% (non-core 57.6%) empty=15.8%
   sentinel: n=3808 bot=0.7% bldg=99.3% (non-core 0.5%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 3948/6212 = 63.55441081777205
  DEFBUILD[all] n=621 sighted20=90.8% permctrl=86.2% ratio=1.05 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=448: d2<=13 14.91 vs 13.69 rr=1.09 | d2<=32 16.99 vs 16.39 rr=1.04
  DEFBUILD[turret] n=484 sighted20=88.8% permctrl=83.9% ratio=1.06 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=368: d2<=13 14.60 vs 13.01 rr=1.12 | d2<=32 16.60 vs 15.80 rr=1.05
  DEFBUILD[barrier] n=137 sighted20=97.8% permctrl=94.2% ratio=1.04 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=80: d2<=13 16.35 vs 16.81 rr=0.97 | d2<=32 18.82 vs 19.14 rr=0.98
  ROT n=924 with_enemy_near(3r,d2<=13)=94.15584415584415 | baseline gunner-rounds-with-enemy-near=13.917456925337252 (gunner-rounds=149740) | rot per 1k gunner-rounds=6.2
  HEAL trig=682 responded=38.70967741935484 lat_med=1.0 lat_p25/75=1/13 modes={'none': 418, 'already': 236, 'spawned': 25, 'walked': 3}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=0 throws=0 (enemy 0 / own 0) | inter-throw n=0 min=None p10=None med=None
  SIEGE shooters=323 deaths=131 replaced<=20r&d2<=25=56.48854961832061 idle_after_last_fire_med=25

## opensverige - plan B   sides=25  versions={'4': 10, '3': 5, '6': 5, '7': 5}
  SHOTS n=3792  bot=8.095991561181435  bldg=90.26898734177215  empty=1.3185654008438819  own=0.31645569620253167  oor=0
   bldg split: core=3222 barrier=0 conveyor=149 splitter=0 harvester=2 gunner=8 sentinel=42 launcher=0
   gunner: n=945 bot=18.3% bldg=75.2% (non-core 14.9%) empty=5.3%
   sentinel: n=2847 bot=4.7% bldg=95.3% (non-core 2.1%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 2381/3423 = 69.55886649138183
  DEFBUILD[all] n=91 sighted20=97.8% permctrl=89.0% ratio=1.10 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=47: d2<=13 17.57 vs 16.04 rr=1.10 | d2<=32 18.91 vs 17.60 rr=1.07
  DEFBUILD[turret] n=87 sighted20=100.0% permctrl=88.5% ratio=1.13 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=45: d2<=13 17.47 vs 16.31 rr=1.07 | d2<=32 18.87 vs 17.49 rr=1.08
  DEFBUILD[barrier] n=4 sighted20=50.0% permctrl=100.0% ratio=0.50 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=2: d2<=13 20.00 vs 10.00 rr=2.00 | d2<=32 20.00 vs 20.00 rr=1.00
  ROT n=134 with_enemy_near(3r,d2<=13)=97.01492537313433 | baseline gunner-rounds-with-enemy-near=70.60653188180405 (gunner-rounds=3215) | rot per 1k gunner-rounds=41.7
  HEAL trig=310 responded=64.83870967741936 lat_med=5 lat_p25/75=1/46 modes={'already': 138, 'none': 109, 'walked': 42, 'spawned': 21}
  LAUNCH adj_eps=375 thrown<=3r=100.0 lat_med=1 | launchers=18 throws=382 (enemy 375 / own 7) | inter-throw n=372 min=1 p10=2 med=2.0
  SIEGE shooters=86 deaths=40 replaced<=20r&d2<=25=25.0 idle_after_last_fire_med=2.0

## The Bisons   sides=20  versions={'2': 20}
  SHOTS n=2376  bot=8.080808080808081  bldg=90.82491582491582  empty=1.0942760942760943  own=0.0  oor=0
   bldg split: core=2084 barrier=0 conveyor=58 splitter=0 harvester=0 gunner=3 sentinel=13 launcher=0
   gunner: n=1074 bot=11.7% bldg=85.8% (non-core 3.4%) empty=2.4%
   sentinel: n=1302 bot=5.1% bldg=94.9% (non-core 2.8%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 1166/2158 = 54.031510658016686
  DEFBUILD[all] n=132 sighted20=96.2% permctrl=98.5% ratio=0.98 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=60: d2<=13 19.72 vs 19.87 rr=0.99 | d2<=32 20.00 vs 20.00 rr=1.00
  DEFBUILD[turret] n=132 sighted20=96.2% permctrl=98.5% ratio=0.98 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=60: d2<=13 19.72 vs 19.87 rr=0.99 | d2<=32 20.00 vs 20.00 rr=1.00
  ROT n=0 with_enemy_near(3r,d2<=13)=None | baseline gunner-rounds-with-enemy-near=89.20134983127109 (gunner-rounds=2667) | rot per 1k gunner-rounds=0.0
  HEAL trig=116 responded=0.0 lat_med=None lat_p25/75=None/None modes={'none': 116}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=0 throws=0 (enemy 0 / own 0) | inter-throw n=0 min=None p10=None med=None
  SIEGE shooters=80 deaths=37 replaced<=20r&d2<=25=37.83783783783784 idle_after_last_fire_med=1.0

## farming_200s   sides=20  versions={'9': 5, '8': 5, '7': 10}
  SHOTS n=2859  bot=2.0636586218957675  bldg=96.39734172787688  empty=1.5389996502273522  own=0.0  oor=0
   bldg split: core=2574 barrier=0 conveyor=154 splitter=0 harvester=6 gunner=0 sentinel=14 launcher=8
   gunner: n=2859 bot=2.1% bldg=96.4% (non-core 6.4%) empty=1.5%
  SHOTS-ON-HEALED-BLDG 874/2756 = 31.712626995645863
  DEFBUILD[all] n=230 sighted20=100.0% permctrl=100.0% ratio=1.00 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=183: d2<=13 19.82 vs 19.90 rr=1.00 | d2<=32 20.00 vs 20.00 rr=1.00
  DEFBUILD[turret] n=230 sighted20=100.0% permctrl=100.0% ratio=1.00 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=183: d2<=13 19.82 vs 19.90 rr=1.00 | d2<=32 20.00 vs 20.00 rr=1.00
  ROT n=47 with_enemy_near(3r,d2<=13)=87.23404255319149 | baseline gunner-rounds-with-enemy-near=87.11376404494382 (gunner-rounds=5696) | rot per 1k gunner-rounds=8.3
  HEAL trig=243 responded=9.465020576131687 lat_med=2 lat_p25/75=0/19 modes={'walked': 2, 'already': 21, 'none': 220}
  LAUNCH adj_eps=0 thrown<=3r=None lat_med=None | launchers=0 throws=0 (enemy 0 / own 0) | inter-throw n=0 min=None p10=None med=None
  SIEGE shooters=185 deaths=160 replaced<=20r&d2<=25=80.625 idle_after_last_fire_med=1

## Focalground   sides=20  versions={'4': 10, '1': 5, '5': 5}
  SHOTS n=584  bot=0.0  bldg=100.0  empty=0.0  own=0.0  oor=0
   bldg split: core=584 barrier=0 conveyor=0 splitter=0 harvester=0 gunner=0 sentinel=0 launcher=0
   sentinel: n=584 bot=0.0% bldg=100.0% (non-core 0.0%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 222/584 = 38.013698630136986
  DEFBUILD[all] n=79 sighted20=82.3% permctrl=82.3% ratio=1.00 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=65: d2<=13 9.26 vs 7.98 rr=1.16 | d2<=32 14.35 vs 13.23 rr=1.08
  DEFBUILD[turret] n=35 sighted20=97.1% permctrl=82.9% ratio=1.17 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=35: d2<=13 12.11 vs 11.69 rr=1.04 | d2<=32 17.60 vs 17.57 rr=1.00
  DEFBUILD[barrier] n=44 sighted20=70.5% permctrl=81.8% ratio=0.86 lat_med=1
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=30: d2<=13 5.93 vs 3.67 rr=1.62 | d2<=32 10.57 vs 8.17 rr=1.29
  ROT n=0 with_enemy_near(3r,d2<=13)=None | baseline gunner-rounds-with-enemy-near=None (gunner-rounds=0) | rot per 1k gunner-rounds=0.0
  HEAL trig=452 responded=67.03539823008849 lat_med=0 lat_p25/75=0/10 modes={'spawned': 19, 'already': 250, 'none': 149, 'walked': 34}
  LAUNCH adj_eps=1180 thrown<=3r=87.37288135593221 lat_med=0 | launchers=136 throws=1031 (enemy 1031 / own 0) | inter-throw n=936 min=1 p10=3 med=4.0
  SIEGE shooters=35 deaths=1 replaced<=20r&d2<=25=0.0 idle_after_last_fire_med=0

## gsxWins   sides=20  versions={'22': 20}
  SHOTS n=2893  bot=0.5184929139301763  bldg=99.30867611475976  empty=0.17283097131005876  own=0.0  oor=0
   bldg split: core=2840 barrier=0 conveyor=0 splitter=0 harvester=0 gunner=3 sentinel=30 launcher=0
   gunner: n=1289 bot=1.2% bldg=98.4% (non-core 2.6%) empty=0.4%
   sentinel: n=1604 bot=0.0% bldg=100.0% (non-core 0.0%) empty=0.0%
  SHOTS-ON-HEALED-BLDG 1808/2873 = 62.930734423947094
  DEFBUILD[all] n=98 sighted20=100.0% permctrl=99.0% ratio=1.01 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=30: d2<=13 18.23 vs 16.10 rr=1.13 | d2<=32 20.00 vs 20.00 rr=1.00
  DEFBUILD[turret] n=62 sighted20=100.0% permctrl=98.4% ratio=1.02 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=8: d2<=13 16.62 vs 18.75 rr=0.89 | d2<=32 20.00 vs 20.00 rr=1.00
  DEFBUILD[barrier] n=36 sighted20=100.0% permctrl=100.0% ratio=1.00 lat_med=1.0
    case-crossover (same tile, r-20..r-1 vs r-60..r-41), n=22: d2<=13 18.82 vs 15.14 rr=1.24 | d2<=32 20.00 vs 20.00 rr=1.00
  ROT n=0 with_enemy_near(3r,d2<=13)=None | baseline gunner-rounds-with-enemy-near=93.31855604813173 (gunner-rounds=3158) | rot per 1k gunner-rounds=0.0
  HEAL trig=98 responded=72.44897959183673 lat_med=1 lat_p25/75=0/13 modes={'none': 27, 'already': 54, 'spawned': 10, 'walked': 7}
  LAUNCH adj_eps=27 thrown<=3r=100.0 lat_med=0 | launchers=26 throws=85 (enemy 27 / own 58) | inter-throw n=60 min=1 p10=1 med=8.0
  SIEGE shooters=62 deaths=30 replaced<=20r&d2<=25=0.0 idle_after_last_fire_med=1.0

```
