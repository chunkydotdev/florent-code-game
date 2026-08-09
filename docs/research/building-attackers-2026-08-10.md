# Which league opponents attack non-core buildings — and which make a usable fixture

**Session 27, research arm, 2026-08-10.**
**FIXTURE CROSSING, STATED UP FRONT: every number below is a PLATFORM cut
(ladder + unrated, 8,663 archived replays). Its output is a list of candidates
for the ARENA pool. Platform behaviour is evidence about, not proof of, arena
behaviour** — and the transfer step is not "acquire the opponent", it is "write a
probe", because we have replays and never source (`docs/tooling.md:389-396`).

Instrument: `scratchpad/aim.py` (this session, not committed — see §9 to rebuild).
Attribution: `corpus/meta_join.tsv`, both team names, 8,234 of 8,663 files (95.0%).

---

**REFRAMED MID-RUN.** The blocker was solved by another route: the builder arm's
synthetic `razer_probe` produces **339 building attacks and 13 building deaths per
game** where the old pool produced zero. So the first question this cut answers is
no longer "which opponent do we need" but **"is 339/13 a threat model that
exists?"** — §1. The shortlist survives as the second finding — §2.

---

## 0. THE HEADLINE IS AN INVERSION OF THE BRIEF'S PREMISE

The brief asked which opponents attack non-core buildings, on the assumption
that such an opponent is scarce and its absence is a prerequisite blocking nine
tactics-library items.

**Building-attacking opponents are not scarce. They are the norm.**

> **LEAGUE DISTRIBUTION** — non-core share of all enemy-directed attack events
> (turret fire + builder attack pooled), **67 teams, FIELD scope = third-party
> platform matches, neither side is us** (teams with ≥40 games AND ≥2,000
> enemy-directed attack events; the ≥40-games-only filter used in §1 admits 71):
> **min 0.0% · p10 17.0% · p25 40.4% · MEDIAN 59.1% · p75 74.2% · p90 91.8% · max 100.0%.**
> **66 of 67 teams sit above the probe family's 0.17% floor. 61 of 67 are above 10%.
> 44 of 67 put the MAJORITY of their attack events on non-core buildings.**

And the corroborating fact from our own side of the same corpus:

> **OpenSverige loses 46.9% of every turret it builds on the platform
> — 5,599 of 11,947 turrets, over 2,313 games (ladder + unrated).**
> Econ: 39,591 of 149,431 (26.5%). Barriers: 2,000 of 3,041 (65.8%).

The arena's "100.0% survival at every horizon" is not a fact about our sentinels.
**It is a fact about our probe pool.** The defensive planks are not unmeasurable;
they are unmeasurable *in the arena*, and they already have a live field instrument.

### 0.1 The cause is in our own source, not in the league

`bots/orizon_probe/main.py:1157` and four siblings:

```python
choice = best_core or best_any     # core strictly preferred; a building is
                                   # only ever shot when NO core is in range
```

`grep -l "best_core or best_any" bots/*/main.py` returns **five of our nine
opponent-imitation probes**: `flotte_probe`, `band_probe`, `kladde_probe`,
`cad_probe`, `orizon_probe`. `ouroboros_probe:1053` is a hand-written variant of
the same ordering ("enemy BUILDER BOT first, then the enemy Core, then their
economy").

**The 99.83%-at-core is a copy-pasted target-selection shortcut we authored.** It
was never a measurement of the field, and the field does not resemble it. The
prerequisite is one line per probe plus a model to write it against — not an
opponent acquisition.

---

## 1. CALIBRATING `razer_probe` AGAINST THE LEAGUE — in range on volume, OUT of range on lethality

**The reassuring half first: 339 building attacks per game is not off the scale.**
The league median is 114 and the max is 855. The worry in the reframe — "if the
whole league sits nearer 3 than 339" — is not what the data says.

### 1.1 STATE THE DENOMINATOR (both of them)

Two figures, and I divided by a **counted** denominator in each case, not an
assumed capacity:

- **building attack events / game** = (turret shots whose round-start target tile
  held an enemy non-core building) + (builder attacks on the same), summed for
  **one team-side**, ÷ **the number of archived games that team-side appeared in**
  (a counted file list, 40–675 games per team).
- **enemy non-core buildings killed / game** = `removeEntity` count of the
  **opponent's** non-core buildings ÷ the same game count.

**Both are per-game, per-team-side, one direction only.** If the builder arm's
339/13 counts both sides, or counts attempted `fire()` calls rather than shots
that landed on a building tile, or counts damage events rather than attack
events, **the comparison below is invalid and I cannot detect that from here.**
The definitions above are stated precisely so they can be checked against
`razer_probe`'s instrumentation before anyone acts on §1.3.

### 1.2 WHERE THE PROBE SITS

**FIELD scope — 71 teams, third-party platform matches, neither side is us:**

| statistic | min | p10 | p25 | **median** | p75 | p90 | max | **probe** | **percentile** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| building attacks / game | 0 | 9 | 29 | **114** | 161 | 252 | 855 | **339** | **p93** (5 of 71 above) |
| enemy buildings killed / game | 1.1 | 4.5 | 6.7 | **10.6** | 17.6 | 26.7 | 55.1 | **13** | **p58** (30 of 71 above) |

**VS-US scope — 24 teams, the same opponents attacking OUR buildings** (the
scope-matched comparison if 339 was measured against our bot):

| statistic | min | p25 | **median** | p75 | p90 | max | **probe** | **percentile** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| building attacks / game | 2 | 21 | **130** | 218 | 235 | 995 | **339** | **p92** |
| our buildings killed / game | 0.1 | 3.4 | **9.4** | 21.3 | 28.6 | 70.5 | **13** | **p67** |

**Both scopes agree.** The probe is a high-aggression but not unprecedented
attacker on volume, and an unremarkable one on outcome.

### 1.3 THE WARNING: the probe pokes like a p93 team and kills like a p58 team

`339 / 13` = **26 attack events per building destroyed.** No real team is
anywhere near that ratio:

| team | attacks/game | kills/game | attacks per kill |
|---|---:|---:|---:|
| **`razer_probe`** | **339** | **13** | **26.1** |
| league median (FIELD) | 114 | 10.6 | **~11** |
| league median (VS-US) | 130 | 9.4 | **9.5** |
| Powerpuff Girls | 252 | 32.8 | 7.7 |
| ph | 370 | 35.1 | 10.5 |
| Jython | 283 | 34.0 | 8.3 |
| Besvikomat | 613 | 54.9 | 11.2 |
| Kleos | 855 | 55.1 | 15.5 |
| Ouroboros | 138 | 34.1 | **4.0** |
| observed range, all 71 teams | | | **3.4 – 37.4** |

**A real team that swings 339 times per game destroys 30–40 buildings, not 13.**
The probe's attack volume is calibrated to the league's top decile while its
lethality is calibrated to the league's middle. It spreads damage instead of
concentrating it — plausibly attacking whatever is adjacent rather than
finishing a target.

**Why this matters and is not pedantry: the error has a DIRECTION, and it
systematically flatters exactly the treatment family it was built to test.**
Heal costs 1 Ti for +4 HP; a builder attack costs 2 Ti for 2 damage. Against an
attacker that needs 26 swings per kill, a repair or heal line comfortably
out-paces the incoming damage and will read as a strong plank. Against Ouroboros
at **4.0 swings per kill** — a real, live, currently-ladder opponent we already
lose to 83% of the time — the same line is overwhelmed. **A survivability plank
tuned green on `razer_probe` may be measuring its own best case.**

**So: `razer_probe` unblocks measurement, and it should be trusted for
"does the treatment do anything at all" and NOT for "how much".** It is a
detection fixture, not a calibration fixture. The concrete fix is cheap — raise
lethality, not volume: fewer targets, finished. Landing at ~150 attacks and
~15 kills per game would put it at the league median on both axes instead of
splitting p93/p58.

---

## 2. THE SHORTLIST

Ranked on the intersection the brief asked for: **resolving AND building-attacking**.
`turLoss%` is the fraction of turrets *we* built that were removed in games
against that team — the most direct available read of "would a survivability
treatment have an event to act on". **LADDER games only** (unrated split out in
§5; the four Tier-1 entries have zero unrated games, so no fixture mixing).

### Tier 1 — COUNTERBATTERY. Exercises turret/sentinel survivability, screening, ablative armour.

| # | Team | ladder n | our WR | our turLoss% | our econLoss% | median turLoss/game | games w/ 0 turret loss | v (24h) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **1** | **Leviathan** | **105** | **54.3%** | **69.9%** (536/767) | **7.8%** | 70.7% | **2%** | live |
| 2 | OopsGotYourElo | 120 | 65.8% | 45.9% (403/878) | 5.1% | 42.9% | 11% | live |
| 3 | Orizon | 25 | 64.0% | 52.0% (78/150) | 12.6% | 33.3% | 10% | live |
| 4 | Memtrace | 85 | 62.4% | 14.2% (57/402) | 4.7% | 0.0% | 52% | live |

**Leviathan is the fixture.** It is the only team in the league that is
simultaneously (a) maximally resolving — 54.3% over 105 games is as close to a
coinflip as the ladder offers, (b) turret-selective rather than
economy-selective — it removes 70% of our turrets while touching only 7.8% of our
conveyors, and (c) high-n on pure ladder. **98% of games against it lose at least
one turret.** Its field-scope attacks-per-available-target ratio is turret:econ
= **6.31**, 4th highest in the league among teams with meaningful volume.

Caveats on the rest of Tier 1: **OopsGotYourElo at 65.8% is at the upper edge of
resolving** and one good version bump puts it past the saturation bar.
**Orizon's ladder n is 25 games / 150 turrets** — at that n the 52.0% figure
moves ±8 points on a dozen turrets, and its unrated arm reads 37.4% at WR 80.0%,
i.e. it is drifting into saturation. **Memtrace is turret-selective but low-volume**
(14.2% loss, half its games lose nothing) — it discriminates weakly.

### Tier 2 — ECONOMIC DENIAL. Exercises conveyor redundancy, chain re-route, harvester repair, rebuild latency.

| # | Team | ladder n | our WR | our turLoss% | our econLoss% | note |
|---|---|---:|---:|---:|---:|---|
| **1** | **Powerpuff Girls** | **140** | **38.6%** | **72.1%** | **50.4%** | hits BOTH layers hardest; broadest single fixture |
| 2 | Ouroboros | 105 | **17.1%** | 75.8% | 54.4% | most hostile in the league; resolving in the *losing* direction |
| 3 | Lunds Stallions | 145 | 32.4% | 66.9% | 36.0% | |
| 4 | Kings College Munich | 135 | 31.1% | 47.7% | 22.0% | |
| 5 | CtrlAltDefeat | 110 | 36.4% | 42.2% | 18.4% | |

**Powerpuff Girls is the second fixture** if only two are added: it is the only
team that puts >70% turret loss *and* >50% econ loss on us at n=140, so one
fixture covers both treatment families. **Ouroboros at 17.1% is the largest
headroom on the ladder** and is not saturated in the useless direction — a
treatment that moves it from 17% to 25% is worth more Elo than anything Tier 1
can pay.

### Negative controls — real teams that behave like our current probes

These matter: **a pool that accidentally selects from this group reproduces the
clean null.** Use them as the control arm, never as the treatment arm.

| Team | our turLoss% | field non-core share | note |
|---|---:|---:|---|
| Team 48 | **0.3%** (1 of 307, 115 games) | 8.2% | the arena pool in league form |
| Albert And Einstein | — | **0.00%** (10,765 events, 145 games) | the only real team at the probe floor |
| The Bisons | 7.0% | 5.5% | |
| diverge | 17.0% | 6.7% | 83.8% of its few non-core hits are turrets |
| Atlas | — | 6.0% | |

---

## 3. OPPORTUNITY NORMALISATION — done, and it does NOT bind

The brief called this "the single most important methodological requirement".
I ran it and **it turns out not to be the discriminator here**, which is worth
saying plainly rather than dressing up.

Every shot is tagged with whether ≥1 enemy non-core building stood within the
firing turret's own attack radius (gunner r²=13, sentinel r²=32) at round start.
**That share is above 90% for 55 of 67 teams and above 73% for 61 of 67.** Almost
everybody gets contact; conditioning on it barely reorders the table
(`NC%` vs `NC|opp%` differ by <2 points for most teams).

The exceptions are real and the brief was right that they need the opposite
treatment. **These teams' low turret-fire building rates are NOT evidence of
building-blindness** — their turrets simply never reach enemy buildings:

| Team | opportunity share | field games |
|---|---:|---:|
| Troupe | 36.6% | 200 |
| Ship Happens | 38.2% | 105 |
| S | 44.5% | 180 |
| TKB | 55.8% | 195 |
| ArjunWorks | 59.2% | 180 |
| StarTrekker | 61.2% | 190 |

None of them are on the shortlist, and none of them should be — a fixture whose
turrets never make contact cannot exercise a survivability treatment either.

Builder-bot contact was measured separately (bot-rounds with an enemy non-core
building orthogonally adjacent): 5.8%–58.6% across the league, 20.5% for us.
It correlates with the turret opportunity share and changes no ranking.

---

## 4. SATURATION CROSS

The brief's rule — a 95% win rate makes a fixture useless however enthusiastically
it attacks buildings — bites exactly once, and in the direction nobody expected.

Sorted by how hard they hit our buildings, the top of the league is *also* where
our win rate is worst. **The building-attacking teams and the teams we lose to
are the same teams.** Powerpuff Girls 38.6%, Ouroboros 17.1%, Lunds Stallions
32.4%, Kings College Munich 31.1%, CtrlAltDefeat 36.4% — all Tier 2, all
resolving, none saturated. That is not a coincidence to be normalised away; it is
the finding. We are losing to teams whose defining behaviour our arena cannot
simulate.

Excluded for saturation: **Banminary (82.5%, n=80)** despite 35.4% turret loss;
**The Bisons (77.1%)**; **Askar City (68.4%)** is borderline and only 19.1%
turret loss anyway. **Orizon (64.0% ladder / 80.0% unrated)** is flagged as
drifting toward the bar.

---

## 5. TARGET-TYPE BREAKDOWN — and the confound that actually bit

**Whole-archive event census, 8,663 platform replays:**

| channel | events | core | turret | econ | barrier | bot | own-side | empty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| turret fire | 2,524,810 | 48.83% | 7.23% | 19.55% | 2.91% | 10.12% | 5.13% | 6.24% |
| builder attack | 2,372,822 | 17.32% | 17.72% | **59.82%** | 3.81% | — | 0.97% | 0.35% |

**The builder-attack channel carries the majority of all building damage in this
league and is almost entirely non-core (81.4%).** Any fixture design that models
only turret fire models the smaller half of the problem.

### The confound: target-type share measured against US is not a property of the opponent

**We build 149,431 econ pieces and 11,947 turrets — a 12.5:1 ratio.** An opponent
that picks the nearest enemy building will therefore *look* like an economic
denier when measured in our games, regardless of preference. Same team, same
window, two scopes:

| Team | turret share of non-core hits, FIELD | turret share, VS US |
|---|---:|---:|
| Lunds Stallions | **64.7%** | 20.0% |
| CtrlAltDefeat | **55.8%** | 13.1% |
| Kings College Munich | 40.1% | 10.7% |
| Leviathan | 61.8% | 54.5% |

**This is the requirement that actually mattered, and it is requirement 4, not requirement 2.** Correcting it is what promotes Leviathan (which stays
turret-selective in both scopes, so its preference is real) over Lunds Stallions
(whose apparent counterbattery is our build mix talking).

The clean version normalises by the victim's own supply — attack events on a
class ÷ count of that class the victim ever built. FIELD scope, turret:econ ratio:
**Hugging Farce 135.3 · diverge 57.6 · Team 48 29.0 · PromptNPray 16.0 ·
Torsko 13.3 · 1337 11.5 · Prompt Engineers Anonymous 10.0 · Focalground 7.8 ·
Orizon 6.5 · Memtrace 6.5 · Leviathan 6.3 · team lazy 5.5**. Most of those have
tiny absolute volume; **Leviathan is the highest-ratio team that also has the
volume and the win-rate position to be a fixture.**

**Which treatment each tier exercises:**
- **Counterbattery (Tier 1)** → forward-sentinel survival, turret screening,
  ablative barriers in front of turrets, turret repair/heal lines, re-siting
  under fire. These are the nine gated items.
- **Economic denial (Tier 2)** → conveyor redundancy and re-route, harvester
  repair, rebuild latency, chain-break detection, barrier screening of the lane.
  **Different treatments. Both satisfy the prerequisite; neither substitutes.**

---

## 6. LADDER vs UNRATED, and reachability

`triggeredBy` splits our 2,313 attributed games into **1,685 ladder / 628 unrated**.
The split matters — Ouroboros reads 17.1% WR / 75.8% turret loss on ladder and
40.0% / 59.2% on unrated, because unrated is where we run experiments. **Every
figure in §1 is ladder-only.** Leviathan, OopsGotYourElo, Memtrace, Banminary,
The Bisons and diverge have zero unrated games; sporks is unrated-only (35 games,
WR 11.4%, turret loss 54.5%) and is therefore excluded from the ladder shortlist.

**On "reachable as an unrated fixture" — the brief's reachability question is the
wrong one, and this is the most actionable correction in the document.**

`fcode match unrated OPPONENT_ID` needs no acceptance from the opponent and is
rate-limited to 5 per 10 minutes (`docs/fcode-cli.md:330-352, :394-401`). All 72
league teams played 143–144 matches in the last 24h — the ladder is a fixed
round-robin, so **every candidate is equally and trivially reachable.** Reachability
does not discriminate between them.

**But `fcode match unrated` always runs our currently-ACTIVE submission**
(`docs/fcode-cli.md:340-350`). It has no own-side selector. **Testing a candidate
treatment on unrated therefore requires shipping that candidate to the ladder
first — which is the thing the arena exists to avoid.** Unrated is a
*confirmation* channel for an already-shipped bot, never a treatment-testing
fixture.

So the concrete path, **updated for `razer_probe` already existing**:

1. **Re-tune `razer_probe` for lethality, not volume** (§1.3) — target ~150
   attacks / ~15 kills per game, the league median on both axes, instead of the
   current p93/p58 split. This is the highest-value single change and it costs
   nothing to try.
2. **Fix the five probes that hard-code `best_core or best_any`** so the *rest*
   of the pool stops sitting at the 0.17% floor. `razer_probe` alone makes the
   pool bimodal — one building-attacker and eight core-rushers — and a
   class-weighted battery over that mix still reports mostly-null.
3. **Add a Leviathan-shaped counterbattery probe** (72 attacks/game of which 45
   land on turrets, 5.5 turret kills/game, 6.0 attacks per kill). It is the
   turret-selective end of the league and `razer_probe`'s profile does not
   cover it.
4. **Add a Powerpuff-Girls-shaped probe** for the economic-denial family (252
   attacks/game, 32.8 kills, 7.7 per kill) — the highest-damage real profile.
5. **Keep a Team-48-shaped probe as the explicit control arm** — it is the real
   league team that reproduces the old null (2 attacks/game against us, 0.4
   buildings killed), and having it named stops the null from being mistaken
   for a treatment failure again.
6. Use unrated vs Leviathan to confirm the shipped result, not to select it.

---

## 7. WHAT I COULD NOT MEASURE

**The single biggest one: I cannot attribute a removal to a killer.** `removeEntity`
carries an id and nothing else. Every `turLoss%` in §2 is "turrets of ours that
died in games against team X", which pools enemy turret fire, enemy builder
attacks, and **our own `destroy()` / `self_destruct()` calls** — free, uncapped,
and something our bot does deliberately.

I can bound it, and the bound is tight: **our turret loss against Team 48 is
0.3% (1 of 307 over 115 games) and against Focalground 1.1%.** Self-inflicted
removal would be a floor present against every opponent, so **self-destroy
contributes at most ~0.3 percentage points** of the 46.9% pooled figure. The
loss rates are enemy-caused. The two independent channels also agree
directionally: Team 48 attacks non-core at 1.22% of shots and costs us 0.3% of
turrets; Leviathan attacks at 36.2% and costs us 69.9%.

Also unmeasured:

- **6.24% of turret shots (157,475) resolve to an empty tile** at round start —
  a bot that moved mid-round, per the FireTurret ordering trap. Unclassified,
  not assigned.
- **Version drift.** Each team's row pools every archived version of that team.
  A team's *current* submission may not attack buildings the way its history
  does. Leviathan's 105 games span multiple versions and I did not split them —
  at n=105 a per-version split has no power.
- **Ladder → arena transfer.** Stated at the top and worth repeating:
  `ouroboros_probe` is already documented as **86 Elo over-confident** against
  its real class (`HANDOVER.md:232-241`). A Leviathan probe will be wrong too;
  what it will not be is 0.17%-at-core.
- **I could not reproduce the 99.83% figure.** See §8.1.

---

## 8. THE INSTRUMENT, AND ITS FAILURE TESTS

`FireTurret{from,to}` and `BuilderAttack{id,target}` resolved against
**round-start occupancy**, never event-order occupancy (schema.md's ordering
trap). Damage-target law applied: turret fire hits the UNIT on the tile if one is
present, else the BUILDING.

**Teeth, per guard, per branch:**

1. **Corrupt-input alarms** (`aim.py --selftest`): truncation → raises;
   200 random byte-flips → counts move; **`ATTACK_R2` forced to 0 → opportunity
   count collapses 178→0**, proving the opportunity branch actually reads the
   radius rather than decorating the output. All three ALARM.
2. **HP-ledger validation with a placebo complement**, 22 replays, 7,822 shots:
   the entity on the recorded target tile takes damage that round **99.42%** of
   the time. **A placebo — a different enemy entity also inside the shooter's
   radius that round — reads 68.7%.** Per class the discrimination is what
   matters: barrier 1.000/0.000, gunner 1.000/0.087, harvester 1.000/0.014,
   conveyor 0.919/0.038, builder bot 0.973/0.016. **The placebo is high (0.935)
   for `core` alone** — cores are damaged nearly every round anyway, so this
   instrument has almost no discriminating power for core hits specifically and
   full power for exactly the non-core classes the shortlist rests on.
3. **Attribution branch, ours vs third-party separately.** OpenSverige rows
   leaking into FIELD scope: **0**. Seat check: the same team computed from seat
   A and seat B rows separately, mean gap **3.06 points** against a between-team
   spread of 0–100 (Albert And Einstein reads 0.00% on both seats; Tyvrets 89.7
   vs 82.6). A broken name↔seat map would pull every team to the league mean of
   59.1%; nothing does.
4. **No dead columns.** `sh_unknown_src` = 0 of 2.5M; `batk_empty` = 0.35%;
   every bucket is populated and none is constant.
5. **Per-team spread checked before every aggregate quoted** (rule 4). Per-game
   medians and quartiles are in the working set: e.g. Powerpuff Girls median
   66.8% (p25 45.6 / p75 77.8), 100% of games above 5%; I Stone has the same
   28.4% pooled rate but a **median of 0.0%** and only 44% of games above 5% —
   a bimodal team whose pooled number describes no actual game. **I Stone is
   excluded from the shortlist for that reason,** not for its rate.

### 8.1 I could not reproduce the 99.83%-at-core probe figure

Running this same decoder over the 24 arena replays on disk
(`scratchpad/loki2mech/`, `scratchpad/cpu/replays/` — `ouroboros_probe` and
`kladde_probe`, 8,325 turret shots) gives **46.1% core / 38.5% non-core / 10.8%
bots pooled across both sides**, and per-file the probe side is 87.8%, 76.6%,
70.0%, 57.6% non-core in several games. `builderAttack` is **not** zero in these
arena replays (13,056 events) contrary to TRAP 7.

**This is a 24-file cut of a different and much smaller population than the
480-game measurement, and I am not claiming it refutes 99.83%.** But the two do
not sit comfortably together, the probe pool used for the 480 games included
probes I did not sample (`rush_probe`, `cad_probe`, `band_probe`, `razer_probe`,
`clanker_probe`, `flotte_probe`, `orizon_probe`), and **TRAP 7 as written is
false for at least these 24 files.** Both deserve a look before the 99.83% is
quoted again.

---

## 9. REBUILDING THIS

The decoder is a session scratch script (`aim.py`, ~330 lines, stdlib +
`tools/replay_census.py` helpers). It emits one row per (file, team) with shot
target classes, builder-attack target classes, opportunity counts, bot-round
contact, and per-class build/death counts. Full archive in **~90s across 8
shards**, 8,663 files, **0 errors**.

If it is worth keeping it belongs at `tools/corpus/replay_aim.py` behind
`sync.py`, since the corpus is placement-oriented and has no attack-target table
at all. **Filed as a follow-up rather than done here** — this brief authorised
one deliverable, and adding a decoder to the corpus requires announcing a
3-minute archive pass.
