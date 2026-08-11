# CRASH INDUCTION, MEASURED LEAGUE-WIDE — CRASHING DOES NOT PREDICT WEAKNESS

**Research arm, s30, 2026-08-11. `tools/crash_census.py` over 3,643 matches
(one randomly-chosen game each), team names from `replay_archive/*.meta.json`,
ratings from the league tape. Our live version v104.**

**Instrument:** `crash_census --selftest` **passes on a real positive/negative
control** — 16 crash_candidates on the deliberately-crashing probe side, 0 on
both negative-control sides. Its own docstring states the conflation honestly:
`crash_candidate` cannot separate a genuine uncaught exception from
`self_destruct()` or `resign()`, because all three land as a bare `removeEntity`
with no preceding `updateHp`.

## 1. WE SUFFER ZERO

**0.000 crash_candidates per game across 1,028 of our games.** Confirms
`CLAUDE.md`'s "0 by us" on a far larger sample. **Our catch-everything-at-top-of-run
is complete — an asset already owned, never to be spent on again.**

## 2. ⛔ CRASHING DOES NOT PREDICT WEAKNESS

**`r(rating, crash_candidates suffered per game) = −0.029`, n = 67 teams.**

| team | rating | crashes suffered/game |
|---|---:|---:|
| sporks | 2082 | **0.000** |
| not adgato | 2051 | 0.058 |
| Clankers | 2040 | 0.020 |
| The Flotte Experience | 2018 | 0.438 |
| Erebus | 1995 | 0.189 |
| **Lorem Ipsum** | **1988** | **2.361** |
| **Jython** | **1978** | **2.344** |
| **OpenSverige** | **1689** | **0.000** |
| vjg | 737 | 6.057 |
| **TKB** | **709** | **0.000** |

**Two teams inside the top seven crash 2.3 times a game and rate 1978–1988. Two
of the weakest teams on the board crash zero times.** Surviving your own
exceptions is not what separates 1690 from 2000.

## 3. NOBODY IS MEASURABLY INDUCING THEM

Blocked on the **victim**, so the victim's own fragility is held constant.
Leaders: kladde **+0.527** over 7 victims, Torsko **+0.337** over 10 — thin
victim counts. **And the estimator carries a game-length confound I do not
trust:** sporks reads **−0.429** and Clankers **−0.805**, i.e. "prevents"
opponent crashes, which is not a mechanism. **Strong teams end games early, so
fewer rounds means fewer crash opportunities**, and that artefact is large enough
to swamp the signal.

**Instrument hygiene:** this estimator's sanity check **passes** — the
within-victim contrast averages **−0.055**, against **+3.56** for the TLE version
of the same design earlier today, which was reported as broken and whose numbers
were withdrawn.

## 4. WHAT THIS CHANGES

**Do not spend a window on crash induction as a CURRENCY plank.** Even perfect
induction buys the condition two 1980-rated teams already live in. **LOKI-14
delivered 314 kidnaps and this is why it never showed up in rating.**

**It also closes a reading I offered the builder an hour earlier and should not
have:** the `12.21%` no-damage forward removals in games we are not in
(`builder-death-attribution-2026-08-09.md`) is **not** a hidden induction weapon
anyone is wielding. It is the field's background rate of bots removing
themselves, and it is **uncorrelated with strength**.

## 5. ⛔ D12 — THIS PRIORITISES, IT DOES NOT RETIRE

**Archive statistics with a BEHAVIOURAL premise** (how opponents perform while
crashing). Under D12 that sends a road to the **bottom of the queue, never off
it**, and **no leg has ever aimed crash induction at a live opponent and read the
currency.** Applied to myself before the side lane has to.

**The rules-level half is not behavioural and does stand:** an uncaught exception
destroys that unit permanently for the rest of the match, and **we suffer zero.**

**Population:** 3,643 matches, one game each, 10 days, one league; ratings are
final-window values with every team starting at 1500, so this is a **strength
association**, not a climb-rate finding.
