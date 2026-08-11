# AMMO POLICY, LEAGUE-WIDE — A SETTLED AXIS, NOT A LIVE ONE

**Research arm, s30, 2026-08-11. Commissioned by the builder arm as the
OPPONENT-SIDE half of their ammo-starvation hypothesis; their half (our own
per-sentinel idle-gap histogram) is a separate instrument and is the one that can
answer the starvation question. Our live version: v104, rating 1689.**

**Population: 17,268 archived games across 3,484 matches — 12,425 of them
THIRD-PARTY games between other teams, 72 teams with ≥40 games and a rating
trajectory. League-wide, not us-only, not an echo loop.**

**⛔ THE BUILDER'S HYPOTHESIS IS HELD UNCONFIRMED THROUGHOUT.** It is an inference
from a rules table plus two dose measurements with no live test. Nothing below
confirms it, and a flat league-wide result is **not** evidence that their idle-gap
histogram will be flat — different question, different instrument.

---

## 1. THE INSTRUMENT NEEDS NO SEAT INFERENCE

`CoreConvertAmmo{team = 1, amount = 2}` (update field 14) **carries the team**, so
the join failure that returned *"0 EXILE throws of 185,695"* on the builder's first
run cannot occur on this path. `scratchpad/ammo_read.py`, 3 forced-answer selftest
cells — no conversions → **empty, not zero-filled**; totals and first-round timing
per team; **the team field made load-bearing by booking identical amounts to the
other team**. Mutation `conv[t] → conv[0]` fails cells B and C.

**Shot attribution measured, not assumed: `FireTurret` carries no id and no team,
so shots are attributed by matching `from` against tracked turret positions.
Sampled over 60 games: 15,749 of 15,749 = 100.0% attributed.** The instrument is
not silently dropping shots.

## 2. THE ANSWER: AMMO CONVERSION IS SETTLED

| question | answer |
|---|---|
| do the strong convert more? | **r(rating, Ti→ammo per game) = +0.153** |
| do the strong convert earlier? | **r(rating, median round of first conversion) = +0.096** |
| does anyone skip it? | **no — ~100% of teams convert in ~100% of their games** |
| when? | **median first conversion: round 0** |

**Every team already does this, from the first round, and how much they do it
barely tracks strength.** The disconfirming case is decisive: **Tim Tam converts
2,863 Ti/game — by far the highest on the board — and is rated 960.** Erebus at
1995 converts 994; Clankers at 2040 converts 512.

**⇒ Ammo POLICY is not an axis of play in this league. It is a solved opening
move.** A plank whose mechanism is "convert more/earlier" has no headroom.

*(This does not touch farming_200s v13 raising shots/round 0.95 → 1.15 at
identical turret count. That is a FIRE-RATE change, and §3 is where fire rate
lives.)*

## 3. THE ONE US-SPECIFIC ANOMALY, AND IT IS REAL

| | us | league median |
|---|---:|---:|
| turrets built per game | **12.6** | 11.3 |
| **turret shots per game** | **67** | **135** |
| Ti→ammo per game | 616 | 758 |
| **shots per turret** | **5.34** | **12.89** |

**We build slightly MORE turrets than the median team and fire HALF the median
number of shots. Rank 61 of 72 on shots per turret.**

**⛔ AND I CANNOT TELL YOU WHY, WHICH IS THE HONEST STATE.** The candidates the
builder named — ammo, reload, target availability — are not separable in this cut.
Converting 616 Ti for 67 shots is ~9.2 Ti/shot, about one sentinel shot's worth,
which is equally consistent with *"we convert only what we spend"* and with
*"we spend only what we convert."* **The idle-gap histogram separates them; this
does not.**

## 4. ⚠ ONE NUMBER THAT LOOKS LIKE A FINDING AND IS AN ARTEFACT

**`r(rating, shots per turret) = −0.351`** — weak teams fire *more* per turret.

**Do not read this as a finding.** It is a ratio whose denominator varies ~100×
across the league: TKB builds **0.3** turrets/game, Jython builds **26.1**. A team
with one turret in a long game racks up shots per turret; a team with 26 spreads
them. `r(rating, turrets per game) = +0.094`. **Compositional artefact, recorded so
nobody else derives it and reports it.**

And note the spread inside the top ten alone — sporks 6.39, Erebus 20.52 — **a 3×
range among teams within 90 rating points of each other. There is no "right"
shots-per-turret level to aim at.**

## 5. WHAT THIS CLOSES AND WHAT IT DOES NOT

**Prioritises down:** any plank whose mechanism is converting more titanium to
ammunition, or converting it earlier. The league solved that in round 0.

**Does NOT close:** the builder's starvation hypothesis for *our* bot, which is
about whether our turrets **idle**, not about how much we convert. **§3 says we
fire half the median while building more than the median — that anomaly is real
and its cause is open.**

**Population caveats:** 10 days, one league, one window; ratings are final-window
values and **every team starts at 1500 here, so "fastest climber" and "current
rating" are the same ordering — this is a STRENGTH association and is reported as
one, not as a climb-rate finding.** Under `FIXTURE_OF_RECORD: live_unrated` this
prioritises; it closes nothing on its own.
