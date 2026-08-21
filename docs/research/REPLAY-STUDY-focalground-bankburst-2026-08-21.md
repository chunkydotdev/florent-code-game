# REPLAY STUDY — Focalground's BANK → SENTINEL-BURST, and what it costs us

**PROVENANCE.** Fresh opus replay-study agent, research lane s52, 2026-08-21.
No inherited session context beyond the named inputs. **MAGNUS COMMISSION,
relayed via the builder, verbatim:** *"focalground has an interesting tactic,
they build their economy and store Ti to then go for the kill and build multiple
sentinels at some point when they have enough economy built up. Can we analyze
what they're doing?"*
**Method:** `docs/research/PLAYBOOK-move-mining-2026-08-16.md` (DISCIPLINE
section). Version-equivalence method borrowed from
`REPLAY-STUDY-teamlazy-v253-2026-08-20.md` §4.
**Inputs:** `corpus/league_matches.tsv` (their version timeline),
`corpus/meta_join.tsv` (replay↔version join; **archived subset**, read
2026-08-21 — it is live-appended, the v32 count moved 75→80 during this study),
`corpus/ladder_games.tsv` (our RATED denominator), `corpus/wincond.tsv`
(league-wide kill-round profiles), `replay_archive/`, `tools/replay_schema.md`,
`tools/replay_census.py` primitives, `bots/_v537socket/` (live tree, read-only),
`QUEUE.md` rows #71/#80.
**New decoders written for this study** (scratchpad, not committed):
`fg_trace.py` (per-round `UpdatePlayers` titanium/ammo + `CoreConvertAmmo` +
placeEntity/removeEntity), `fg_summarise.py`, `fg_trigger.py`, `fg_approach.py`
(replays `moveBuilderBot` to track builder positions), `fg_ammo.py`,
`fg_equiv.py`.
⚠ **Parser provenance:** three wrapper levels were wrong on the first pass
(`PlaceEntity.entity`, `UpdatePlayers.players`, and a `cores` key type) and each
was caught by an output that could not be true (`team=0 kind=None` for 160/160
builds; `d²(sentinel, own core) == d²(sentinel, enemy core)` in every game).
The end-to-end sanity check that the parse is sound: **`titaniumCollected`
tracks `distributeResources`-to-core exactly** per `replay_census.py`'s own
documented 56/56 check, and our FG win rates decoded off replays reproduce
`ladder_games.tsv` cell-for-cell (v18 ladder 6/15 = 40%, decoded 40%).

---

## 0. GROUND AND VERSION DISCIPLINE

Their timeline from `corpus/league_matches.tsv` (1,093 match rows, all
league-wide): **v1 → v32, current version v32 from 2026-08-20T21:32:59Z**,
29 match rows on v32 by 2026-08-21T06:52Z.

**We have never met v32.** Our 155 RATED games span their v1–v20
(`ladder_games.tsv`, `opp = Focalground`): v1 5 · v4 10 · v5 5 · v10 50 · v11 55
· v18 15 · v19 10 · v20 5. The current-version read therefore rests on
**third-party archived replays: 80 v32 games** (60 unrated challenges + 15
ladder + 5, opponents Erebus 20 · DinooniD 20 · kladde 15 · lingling_40h 10 ·
ph 5 · O(1) 5).

### 0.1 Version pooling — **DO NOT POOL v32. Report it alone.** *(MEASURED)*

11-dim build profile (n_conveyor, first/n_harvester, first/n_gunner,
first/n_sentinel, n_barrier, n_builder, ti_max, ti_max_round), median profile per
group, scale-normalised L1, permutation null 3,000 re-splits, **opponent held
fixed**:

| comparison | n/n | d | null med | p | verdict |
|---|---|---|---|---|---|
| v32 vs v22 @Erebus | 20/15 | 0.536 | 0.353 | 0.020 | DIFFERENT |
| v32 vs v20 @Erebus | 20/10 | 0.545 | 0.221 | 0.001 | DIFFERENT |
| v32 vs v19 @Erebus | 20/10 | 0.737 | 0.288 | 0.000 | DIFFERENT |
| v32 vs v18 @Erebus | 20/30 | 0.568 | 0.203 | 0.000 | DIFFERENT |
| v32 vs v22 @DinooniD | 20/15 | 0.634 | 0.388 | 0.022 | DIFFERENT |
| v32 vs v18+v20 @lingling | 10/10 | 0.469 | 0.307 | 0.023 | DIFFERENT |
| **CONTROL** v11 vs v14 @Torsko | 50/20 | 9.881 | 0.166 | 0.000 | DIFFERENT |
| **CONTROL** v14 vs v18/20/22 @Torsko | 20/15 | 1.488 | 0.256 | 0.001 | DIFFERENT |
| **NEG CONTROL** v32@Erebus split in half | 10/10 | 4.835 | 1.930 | 0.166 | **SAME** |

**The instrument returns both verdicts** — SAME on a same-version split, DIFFERENT
on a known era boundary. ⇒ **v32 is its own bot.** Every v32 number below is
labelled `v32 n=80`; the **v17–v32 "bank-burst family"** (n=390 archived games) is
quoted separately as context, never merged into a v32 figure.
⚠ Raw `d` is **not** comparable across rows (different pools, different scale
vectors). The ordering that *is* readable is `d / null-median`: v32-vs-recent
1.5–2.8×, era boundary 5.8–59×.

### 0.2 THE ERA MAP — they have had three bots, and only the third is the one Magnus saw

Medians per version, all opponents, archived (`n` = games):

| ver | n | win% | 1st sentinel | Ti peak (round) | peak ammo | kill% | med kill round |
|---|---|---|---|---|---|---|---|
| v10 | 200 | 57.0 | r214 | 1004 (r175) | 60 | 56.0 | r238 |
| v11 | 402 | 44.3 | r216 | 1004 (r174) | 60 | 42.0 | r240 |
| **v12–v15** | 235 | 53–94 | r118–208 | **6,056–12,603 (r999)** | 12–18 | **0.0** | — |
| v18 | 130 | 62.3 | r125 | 838 (r120) | 24 | 62.3 | r171 |
| v19 | 65 | 83.1 | r121 | 814 (r139) | 24 | 83.1 | r184 |
| v20 | 30 | 76.7 | r120 | 842 (r142) | 24 | 76.7 | r170 |
| v22 | 55 | 74.5 | r146 | 824 (r139) | 24 | 72.7 | r174 |
| **v32** | **80** | **58.7** | **r106** | **829 (r132)** | **34** | **58.7** | **r176** |

**v12–v15 were a pure r1000 hoarder** (0 core kills in 235 games, banks of
6k–12.6k Ti at r999). **They abandoned it.** v17 onward is the bank-burst bot,
and across it the burst has moved steadily **earlier** — v18 r125 → v32 r106.

---

## 1. Q1 — THE BANK CURVE AND THE TRIGGER

### 1.1 The shape *(MEASURED, v32 n=80)*

⛔ **NOT A SLOWLY-FILLING RESERVOIR — A LATE SPIKE.** The naive reading (bank
rises steadily to ~830) is **wrong and I checked it**: the *cross-sectional*
median bank at fixed rounds is **r0 470 · r25 224 · r50 355 · r75 446 · r100 450
· r125 442 · r150 490 · r200 515** (v32, n=80 falling to 37), and only
**22/76 = 29%** of games have Ti non-decreasing across r25≤r50≤r75≤r100. They
spend continuously through the opening; the 829 figure is a **per-game maximum**,
and per-game maxima at different rounds do not make a plateau.

**The curve only appears when it is aligned to the burst** (v32, n=63, medians at
offsets from the first sentinel):

| offset | −40 | −30 | −20 | −10 | −5 | −2 | **0** | +2 | +10 | +20 | +40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **median Ti** | 370 | 466 | 542 | 668 | 723 | 723 | **671** | 614 | 468 | 409 | 338 |

⇒ **the bank roughly doubles in the 40 rounds immediately before the sentinel and
drains for the 40 after.** Mechanically that is eco spend saturating — once the
conveyor farm is built there is nothing left to buy, income keeps arriving, and
the bank crosses the threshold within ~40 rounds. They **spend nothing on
turrets** meanwhile: median 5 harvesters, 40 conveyors, 3 barriers, **0
gunners** per v32 game.

### 1.2 **VERDICT: A TITANIUM THRESHOLD NEAR 750–800, NOT A ROUND.** *(MEASURED)*

Defining the **BURST** as the *salvo* — the first round from which ≥2 sentinels
are placed inside a 12-round window (52 of 80 v32 games have one) — the
commission's requested discriminating cut:

| quantity at the burst | n | median | sd | **CV** | IQR |
|---|---|---|---|---|---|
| **round** | 52 | 147 | 117.3 | **0.681** | 93 … 214 |
| **titanium** | 52 | **831** | 229.2 | **0.261** | **813 … 884** |

> **The Ti-at-burst CV is 2.6× tighter than the round-at-burst CV.**
> Round-fixed is refuted: the salvo round spans r50 → r675.

Corroboration, four independent ways:

1. **Correlation.** `corr(salvo round, round Ti first crosses 800) = **0.845**`
   (n=40). Both alternatives die on the same cut:
   `corr(salvo, round of FG's first own-unit loss) = **0.038**` (n=52) and
   `corr(salvo, round the enemy first builds within d²≤50 of FG's core) = **−0.11**`
   (n=48). ⇒ **opponent-state-conditional is REFUTED.**
2. **Lag.** Median `salvo − (round Ti crosses 800)` = **+3 rounds**; 55% of games
   fire within [−5, +15] of the crossing. The same lag is +7.5 at T=750, +17 at
   T=700, +38 at T=500 — **monotone, and it bottoms out at 750–800.**
3. **The necessity cut, which is the control that must come out the other way.**
   Of 13 v32 games whose bank **never reaches 600 Ti, 0 produce a salvo.** Of the
   67 that do, 52 (78%) salvo. At T=700: 1/20 vs 51/60.
   ⇒ **reaching the bank is near-necessary for the burst.**
4. **The clump.** 23 of 58 first-sentinel Ti readings fall in the 40-Ti-wide band
   [790, 848].

⚠ **HONEST RESIDUAL.** The threshold is not a clean step: 15 of 63 v32 games place
a **first** sentinel at Ti < 400. Those are mostly single sentinels that never
become a salvo (P(kill | no salvo) = 0.00 at v32) — a reactive/defensive
placement that the salvo definition correctly separates. The `first_sentinel`
CV is 0.408; the `salvo` CV is 0.261. **Read the salvo, not the first sentinel.**

⚠ **Sampling caveat:** the Ti series is decoded at every round but the
crossing-round search in the trigger dump samples every 5th round, so all
"crossing" rounds carry ±2 rounds of quantisation. It cannot move a +3 median
lag past the ±5 band.

---

## 2. Q2 — THE BURST

### 2.1 It is a **FORWARD SIEGE**, not a home battery *(MEASURED, v32 n=80)*

| | v32 (n=63 games w/ sentinel, 314 sentinels) | v18–22 (n=242, 848 sentinels) |
|---|---|---|
| median d² sentinel → **ENEMY** core | **22** | **13** |
| share within sentinel range (d²≤32) of the enemy core | **67%** | **84%** |
| share within d²≤13 of the enemy core | 41% | 60% |
| median d² sentinel → **own** core | **331** | 256 |
| share within d²≤32 of own core | **7%** | 7% |
| games with ≥1 turret within d²≤100 of the enemy core | **60/63** | 238/285 |
| sentinels per game | med 4 (IQR 3–5) | med 3 (IQR 2–4) |

They walk a builder across the map and plant sentinels **inside their own firing
range of the opponent's core**. Sentinel: 18 dmg, reload 2, line shot that
**ignores obstacles** — so a barrier seal does not stop it.

### 2.2 The kill arithmetic checks out *(MEASURED + mechanism)*

Two sentinels alternating at 18 dmg / reload 2 = **18 HP/round** → a 500-HP core
in **~28 rounds**. **Observed rounds from first sentinel to enemy core death:
median 30 (v32, n=48 kills), median 29 (v18–22, n=201).** Total titanium
converted to ammunition per game: **median 384 Ti (v32)** against the 280 ammo a
naked 500-HP core costs at 10 ammo/sentinel-shot.

### 2.3 ⛔ **THE CONVERT SPIKE IS NOT AN EARLY TELL. IT IS A LATE ONE, AND IT IS INVISIBLE.** *(MEASURED — this REFUTES the commission's stated sub-hypothesis)*

The commission expected *"they must convert a large bank 1:1 near the burst"*.
**They do not bank ammunition at all.** Ammo balance and cumulative converts
aligned to the first sentinel (v32, n=63; median across games):

| offset from 1st sentinel | −20 | −10 | −5 | −2 | **0** | **+2** | +5 | +10 | +20 | +40 |
|---|---|---|---|---|---|---|---|---|---|---|
| **ammo balance** | 0 | 0 | 0 | 0 | **0** | 14 | 4 | 14 | 16 | 14 |
| **cumulative Ti converted** | 0 | 0 | 0 | 0 | **0** | **24** | 50 | 100 | 144 | 284 |
| **P(a convert happens this round)** | 2% | 2% | 5% | 6% | 8% | **98%** | 30% | 56% | 41% | 16% |

> **Median titanium converted to ammo BEFORE the first sentinel: 0 (share of
> total: 0.00).** The convert engine switches on **+2 rounds AFTER** the sentinel
> is already standing, in **10–20 Ti chunks, median 24 converts per game**.
> **Peak ammo balance ever held: median 34, IQR 28–44; 0 of 63 games ever hold
> 100 ammo; 0 of 242 v18–22 games do either.**

⇒ **WARNING GIVEN BY THE CONVERT CURVE TO A LIVE OPPONENT: ZERO ROUNDS** — and
it would be zero anyway, because **the Controller exposes `get_global_ammo()` for
your own team only**; there is no enemy-resource getter. The bank and the
converts are *both* unobservable. **The only observable tell is physical.**

### 2.4 The observable tell, and its lead time *(MEASURED, v32 n=63)*

Replaying `moveBuilderBot`, the round an FG builder first comes within d² of the
**enemy** core versus the round the first sentinel lands:

| proximity | games | **median warning (rounds)** | IQR | min | negative |
|---|---|---|---|---|---|
| d² ≤ 100 | 63/63 | **68** | 43 … 124 | 14 | 0 |
| d² ≤ 32 | 63/63 | **58** | 33 … 119 | 7 | **0** |
| d² ≤ 8 | 63/63 | 47 | 25 … 105 | −17 | 6 |

**And it is a camp, not a fly-by:** occupancy of the window
[first arrival at d²≤32, first sentinel] with an FG builder present is
**median 0.81** (IQR 0.59–1.00, >50% in 81% of games), and the **longest
unbroken camp before the first sentinel is median 30 consecutive rounds**
(IQR 18–54).

> **CONTROL THAT COMES OUT THE OTHER WAY:** the same camp measure on **their
> v11** (n=402) reads **median 6 rounds, 39% of games ≥15 rounds**, against v32's
> **30 / 76%**. **And a second control separates the two claims:** their **v14**
> (the hoarder era) camps *more* (median 47) but builds a forward sentinel in only
> **49/135 = 36%** of games, versus v32 **55/80 = 69%** and v18–22 **238/285 =
> 83%**. ⇒ **camping is necessary but not sufficient; the forward sentinel is the
> plank.**

---

## 3. Q3 — WHAT DEFENDS THE BANK PHASE, AND **DOES RUSHING BEAT THE CLOCK?**

### 3.1 Almost nothing defends it *(MEASURED, v32 n=80)*

* **First turret within d²≤40 of their own core: present in only 30/80 games,
  median round 97.** In 50/80 games their core has no turret cover at all.
* **First barrier: 64/80 games, median round 59.** Barriers and distance are the
  whole defence.
* Median **0 gunners** built per game at v32.

### 3.2 **VERDICT: RUSHING BEATS THE CLOCK — AND ALMOST NOBODY IN THE LEAGUE CAN DO IT.** *(MEASURED)*

Rush class defined independently of Focalground: per-team share of archived games
won by `core_destroyed` **by r150**, from `corpus/wincond.tsv` × `meta_join`
(league-wide, teams with ≥60 games). RUSH = ≥25% (The Bisons 49.1%, diverge 40.8%,
Orizon 39.1%, Banminary 29.7%, farming_200s 26.2%, lingling_40h 25.3%, …);
SLOW = <12%. **We are at 18.7% over 9,101 archived game-sides, median kill r166 —
MID, not RUSH.**

**The clock itself** (FG v17–v32 family, n=390 archived games, all opponents):

| | share |
|---|---|
| FG's first sentinel up by **r120** | **43%** of ALL games (v32: 51%) |
| FG's first sentinel up by r150 | 56% (v32: 59%) |
| **Any opponent kills FG's core by r150** | **22/390 = 5.6%** (v32: **2/80 = 2.5%**) |
| Opponent kills FG's core at all | 124/390 = 32% (median r221) |

⇒ **the window is r0–r120 and the field converts it 5.6% of the time.**
Best in the field at it: **HTTP 418 30% (n=10)**, then **OpenSverige 15.6%
(n=45 archived family games)** — we are second, on a bigger sample than the
leader.

**The mechanism cut — pressure genuinely starves the trigger** (v18–v32 pooled,
n=365, split on whether an enemy builder reached d²≤32 of FG's core by r60):

| | n | reached salvo | median salvo | peak bank | ever ≥800 Ti | FG win% |
|---|---|---|---|---|---|---|
| EARLY PRESSURE | 330 | **65%** | **r151** | 793 | **48%** | **67%** |
| no early pressure | 35 | 91% | r106 | 891 | 80% | 86% |

⚠ **CONFOUND, stated because it is load-bearing:** 330/365 games have early
pressure — it is the field norm, so the 35-game comparison group is
self-selected for passivity, and the FG-win gap (67 vs 86) mixes "pressure works"
with "weak opponents don't pressure". The **dose** version de-confounds it
partially by conditioning on damage actually done — FG economy units (conveyor +
harvester + builder) destroyed before r100:

| FG econ units lost by r100 | n | salvo% | med salvo | peak bank | ever ≥800 | **FG win%** |
|---|---|---|---|---|---|---|
| 0–2 | 95 | 79% | r138 | 874 | 65% | **86%** |
| 3–9 | 136 | 63% | r154 | 774 | 38% | **60%** |
| 10+ | 134 | 63% | r131 | 806 | 54% | **64%** |

> **Killing ≥3 of their economy units before r100 cuts their win rate 86% → ~62%
> and their ever-reach-800 rate 65% → 38–54%. The marginal return SATURATES after
> ~3 — going to 10+ buys nothing further.** That is a cheap, bounded prescription:
> **three kills by r100, then stop paying for harassment and spend on the kill.**

---

## 4. Q4 — VS US

### 4.1 ⭐ **WE DIE TO THE BURST. WE HAVE NEVER DIED BEFORE IT.** *(MEASURED)*

Across **all 155 RATED games** (and all 85 unrated) vs Focalground v1–v20:

> **Games in which OUR core was destroyed before their first sentinel was
> placed: 0 of 155.**
> **Games in which our core was destroyed and they never built a sentinel: 0.**

Every loss to Focalground is a loss to the forward sentinel siege. There is no
other channel.

### 4.2 The rated record, with corrected intervals

`ladder_games.tsv`, opp = Focalground, **RATED only**, DEFF = 1.366
(within-opponent, rated surface):

| their ver | our ver(s) | games | our share | 95% CI (DEFF-corrected) |
|---|---|---|---|---|
| v10 | v104 | 50 | 42.0% | [26.0, 58.0] |
| v11 | v112–v125 | 55 | 47.3% | [31.9, 62.7] |
| **v10+v11** | v104–v125 | **105** | **44.8%** | **[33.6, 55.9]** |
| v18 | v161–v162 | 15 | 40.0% | [11.0, 69.0] |
| v19 | v162–v163 | 10 | 20.0% | [0.0, 49.0] |
| v20 | v164 | 5 | 20.0% | — |
| **v18+v19+v20** | v161–v164 | **30** | **30.0%** | **[10.8, 49.2]** |
| **ALL** | | **155** | **41.9%** | |

**Two-fixture comparison of the slide** (p̄ = 0.415, DEFF 1.366 both arms):
Δ = 44.8 − 30.0 = **14.8pp, half-width 23.4pp** ⇒ **the slide is NOT established
at 95%.** It is a real point estimate on a sample too small to separate from
noise. ⚠ Restated as an exclusion per the direction clause: this cut **cannot
exclude** a slide of up to 38pp either.

### 4.3 Both branches are real, and they compound *(MEASURED, with n)*

**BRANCH A — THEIR VERSIONS CHANGED, AND IT IS NOT ABOUT US.** Median round of
their first sentinel, **excluding all OpenSverige games** (the control that
removes any reaction-to-us story):

| their ver | v10 | v11 | v14 | v18 | v19 | v20 | v22 | **v32** |
|---|---|---|---|---|---|---|---|---|
| n (non-us) | 94 | 154 | 65 | 89 | 46 | 22 | 46 | **63** |
| median 1st sentinel | **r226** | r220 | r177 | **r126** | r142 | r118 | r146 | **r106** |

> **Their burst moved ~100 rounds earlier, league-wide, on a population that
> contains none of our games.** Against us specifically it moved r189 (v10–v11,
> n=59 sentinel games of 105) → **r114** (v18–v20, n=24 of 30).

**BRANCH B — OUR TREE GOT SLOWER OVER THE SAME SPAN.** Our RATED record vs **all**
opponents, `ladder_games.tsv`:

| our ver | games | kill% | **kill ≤ r300%** | median kill round |
|---|---|---|---|---|
| v104 | 510 | 50.8 | **43.1** | r172 |
| v125 | 305 | 55.1 | 45.6 | r176 |
| v152 | 360 | 52.5 | 43.3 | r178 |
| v161 | 185 | 54.1 | **37.8** | **r210** |
| v162 | 415 | 48.2 | 38.3 | r196 |
| v168 | 250 | 52.8 | **36.0** | **r227** |

> **Our timely-kill rate drifted 43% → 36% and our median kill round r172 → r227
> across exactly the versions that met their v18–v20.**

**THE RACE, in one line.** At *their* v10 / *our* v104: their sentinel r226 vs our
kill r172 — **we led by ~54 rounds**. At their v32 / our v168: their sentinel
r106 vs our kill r227 — **they lead by ~121 rounds.** A ~175-round swing, of
which **~120 is theirs and ~55 is ours.**

Head-to-head confirmation, rated only:

| | n | our share | we kill their core | median our-kill | their 1st sentinel | **we beat the sentinel** |
|---|---|---|---|---|---|---|
| their v10–v11 | 105 | 44.8% | 45/105 (43%) | r159 | r189 | **44/105 = 42%** |
| their v18–v20 | 30 | 30.0% | 8/30 (27%) | r125 | r114 | **6/30 = 20%** |

⚠ The r159 → r125 drop in our median landed-kill round is **survivorship**: only
the fastest of our kills still land inside their shortened window. It is not
evidence that we got faster — 4.3 Branch B shows the opposite league-wide.

---

## 5. Q5 — THE STEALABLE FORM: A RE-SPEC SKETCH FOR QUEUE #80

### 5.1 What the incumbent does today *(GREPPED against the LIVE tree `bots/_v537socket/`)*

| | value | site | status |
|---|---|---|---|
| `SURGE_TI_FLOOR` | **1500** | `doctrine.py:402` | fires 0/1,243 v140 game-sides before r250 (`#80` precondition) |
| `SURGE_MIN_RND` | **300** | `doctrine.py:403` | past the `DEFENCE_ADMISSION_BAR` |
| `SURGE_EXTRA` | 5 | `doctrine.py:404` | **dead code — no consumer** |
| `SURGE_ECO_CAP` | 24 | `doctrine.py:405` | only consumer, `eco.py` — buys **eco hands** |
| `LOKI_SURPLUS_TI` / `LOKI_RICH_TI` | 260 / 700 | `doctrine.py:1197,1199` | opening-endowment trigger / effectively dead |
| `AMMO_FLOOR` | **16** | `doctrine.py:963` | reactive drip |
| ammo target ladder | 24 under siege · min(48, 4×weapons) · min(120, 40+20×fwd_guns) | `main.py:536–543` | **capped, demand-driven** |
| convert site | `main.py:1043–1055`, chunked, gated on `ti > ti_floor` | | |

⇒ **We already convert in small just-in-time chunks — the same shape Focalground
uses.** What we do not have is (a) a bank that ever reaches a burst threshold
(our median peak bank is **470 = the opening endowment**, per `#80`'s own
precondition), and (b) any **bank-triggered OFFENSIVE** spend: the surge buys
farm labour, at r300, on a floor nobody reaches.

### 5.2 ⛔ The part of Focalground's plank we **cannot** steal

**Their trigger is 750–800 Ti and we structurally never get there.** `#80`'s
precondition measured 0/1,243 v140 sides ever holding 1500 before r250, median
peak bank 470, and the field context there is the same for Erebus (454), The
Bisons (438), kladde (470). **Focalground is the outlier that actually banks
800+** — and it costs them r106–r147 of doing nothing offensive. **Copying the
threshold means copying the delay, and a burst that fires at r147 lands its kill
at r177 (their median +30) which is fine — but only if the bank arrives on time,
and ours does not.**

### 5.3 The re-spec sketch *(≤4 sentences, as commissioned)*

> **Re-spec #80 as BANK-TRIGGERED FORWARD SIEGE HARDWARE, not eco labour:
> replace `SURGE_TI_FLOOR = 1500 ∧ rnd ≥ 300` with an EDGE-triggered
> `ti ≥ ~200` (the harassment doc's menu: fires 25.6%, median first crossing
> r67, and MUST be edge-based since only 10.3% sustain it ten rounds) with the
> round gate deleted, and give it a KILL-HARDWARE consumer — fund a
> SENTINEL PAIR at d² ≤ 32 of the enemy core, which is Focalground's whole plank
> and which our siege lane already has the raider machinery to place.**
> **Price it against KILL_TARGET r180 using their own measured constant: first
> sentinel → enemy core death is median 30 rounds (n=48 v32, n=201 v18–22), so a
> pair landing at r150 kills at ~r180 — on-programme; a pair that has to wait for
> 800 Ti lands at their r147 median and only works because they bank, which we do
> not, so the arm is the PAIR + the just-in-time 10–20 Ti convert drip, at OUR
> bank, NOT their threshold.**
> **The two sentinels are the load-bearing number, not four: P(FG kills | salvo of
> ≥2 within 12 rounds) = 0.92 vs P(kill | single sentinel or none) = 0.00 at v32
> (n=52 / 28) — ⚠ a collider (losing the game prevents the salvo), so read it as
> "their kill channel IS the pair", not as a causal effect size.**
> **Turtle-to-r400 is not on the table and this sketch never approaches it: the
> trigger is a bank we cross at median r67, and `R1000_IS_DEFEAT` bites their
> v12–v15 hoarder era, which scored 0 core kills in 235 games and which they
> themselves abandoned.**

⭐ **ONE SPEC DETAIL THAT FALLS OUT OF §1.1 AND IS WORTH MORE THAN THE THRESHOLD
ITSELF:** their bank does not fill slowly — it **doubles in the 40 rounds before
the burst**, because eco spend saturates while income continues. ⇒ **the
implementable proxy for "the bank is ready" is not a Ti level at all, it is
`no eco build placed for N rounds AND income still arriving`** — a state we can
detect at OUR bank size, at r60–r100, without ever holding 800 Ti. That is the
version of the trigger that survives the fact that we never bank what they bank.

**Relation to #71** (*fund the collar before the kill window*): #71 asks for the
same gate change on the **same constants** and this study supplies the missing
half — **what to spend it on.** #71 says "make the surge gate kill-conditional";
Focalground's evidence says the *consumer* matters more than the gate, because
`#80`'s precondition already proved moving the gate alone changes the fire rate
by **0.00pp**. ⇒ **the two rows should be merged, or #80 explicitly scoped to the
CONSUMER and #71 to the GATE.**

---

## 6. REFUTED-AND-RETAINED (do not re-derive)

1. ⛔ **"The ammo convert spike is the earliest tell."** REFUTED. Median Ti
   converted before the first sentinel = **0**; the convert engine starts at
   **+2 rounds after** the sentinel (98% of games); peak ammo balance median 34,
   **0/63 games ever hold 100 ammo**. Warning to an opponent: **zero rounds** —
   and moot regardless, since `get_global_ammo()` reads own-team only.
2. ⛔ **"The burst is round-scheduled."** REFUTED. Salvo round CV **0.681**
   (r50–r675) vs Ti-at-salvo CV **0.261**.
3. ⛔ **"The burst is opponent-state-conditional."** REFUTED.
   `corr(salvo, first own loss) = 0.038` (n=52);
   `corr(salvo, enemy build near own core) = −0.11` (n=48);
   vs `corr(salvo, Ti crosses 800) = 0.845` (n=40).
4. ⛔ **"They bank Ti for the tiebreak."** REFUTED for the CURRENT bot — but
   **TRUE of v12–v15**, which banked 6k–12.6k Ti to r999 and scored **0 core
   kills in 235 games**. They abandoned it at v17. *(A ready-made argument that
   `R1000_IS_DEFEAT` is also the field's own conclusion.)*
5. ⛔ **"They defend the bank phase."** REFUTED. Home turret in only **30/80**
   v32 games (median r97); median **0 gunners**; 93% of their sentinels sit
   further than d²=32 from their **own** core.
6. ⛔ **"v32 pools with v18–v22."** REFUTED at p ≤ 0.023 on six opponent-held-fixed
   comparisons, with a negative control returning SAME. Numbers must be
   version-labelled.
7. ⛔ **"Camping a builder near the enemy core is the burst signature."**
   REFUTED as sufficient — their **v14** camps *more* (median 47 rounds) and
   forward-sentinels *less* (36% vs 69%). The **forward sentinel** is the plank;
   the camp is only its lead indicator.
8. ⚠ **NOT refuted, flagged as a collider:** P(FG win | salvo) = 0.92 vs
   P(FG win | no salvo) = 0.00 (v32, n=52/28). Losing early prevents the salvo,
   so this is descriptive of their win channel, not a causal effect size.

---

## 7. SURPRISES, WRITTEN DOWN BEFORE BEING EXPLAINED AWAY

* **They hold ZERO ammunition for the entire buildup.** A bot planning a
  sentinel siege converts nothing until the sentinel is standing. If their
  builder is killed at d²≤8 of our core on the round it places sentinel #1, they
  have **0 ammo and 800 Ti** and their whole game is idle titanium.
* **Focalground v32 beats RUSH-class opponents (90%, n=10) better than
  SLOW-class ones (40%, n=20).** Confounded by opponent strength and thin, so it
  is reported, not banked — but it runs against the "rush them" intuition and
  deserves a look before we lean on it.
* **v32's win rate (58.7%) is LOWER than v19/v20/v22 (83/77/75%)** despite the
  earliest burst yet (r106) — their last three versions may be a regression.
  Denominator caveat: the opponent mixes differ (v32 faces Erebus/DinooniD/kladde;
  v19 faced 0033/OpenSverige/Banminary), so this is **not** a like-for-like cut.

---

## 8. LEDGER ROWS (`move-mining-ledger.tsv`)

```
2026-08-21	Focalground	32	80	docs/research/REPLAY-STUDY-focalground-bankburst-2026-08-21.md
2026-08-21	Focalground	18,19,20,21,22	285	docs/research/REPLAY-STUDY-focalground-bankburst-2026-08-21.md
2026-08-21	Focalground	11,14	537	docs/research/REPLAY-STUDY-focalground-bankburst-2026-08-21.md
```

*(Rows 2 and 3 are CONTROL coverage — the family context and the era-boundary
positive controls — not primary study targets. v32 is the primary, n=80 archived
games / 0 of them ours.)*
