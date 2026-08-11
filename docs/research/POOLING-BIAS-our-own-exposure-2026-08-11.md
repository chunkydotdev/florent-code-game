# OUR OWN EXPOSURE TO THE POOLING BIAS — AND WHY THE OBVIOUS REPAIR IS NOT AVAILABLE

**Research arm, s30, 2026-08-11. Follow-up to sweep 22 (`33c31c2`), which measured
league-wide that pooling a per-opponent statistic across an opponent's versions
overstates expected game share against the version you will actually meet.
Population here: `corpus/league_matches.tsv`, **us-only** (OpenSverige), 599
matches in the 10-day window, matches not games. Our live version: v104.**

**THE SHORT VERSION: the exposure is real and large. The repair — condition every
per-opponent statistic on the opponent's CURRENT version — cannot be executed,
because we have almost no games against most opponents' current versions.**

---

## 1. THE EXPOSURE

**419 of 599 of our matches — 69.9% — were played against a version the opponent
no longer runs.** *(Sweep 22's agent reported 72.6% over its own top-15 cut; two
different populations, same conclusion.)*

**8 of 26 opponents with ≥10 matches: we have ZERO games against their current
version** — Powerpuff Girls, Leviathan, CtrlAltDefeat, Memtrace, Banminary among
them. For those cells, *every* number we hold is about a bot that no longer exists.

## 2. THE REPAIR, ATTEMPTED — AND WHY IT FAILS

Per opponent, our pooled game share against our game share **against their current
version only**:

| opponent | matches | pooled | vs current version | **n at current** | stale share |
|---|---:|---:|---:|---:|---:|
| Lunds Stallions | 45 | 32.0% | 80.0% | **1** | 98% |
| Askar City | 36 | 66.7% | 70.0% | **2** | 94% |
| farming_200s | 22 | 50.9% | 20.0% | **1** | 95% |
| Powered by SmartFridge | — | 47.3% | 60.0% | **1** | 91% |
| Landers | — | 49.2% | 45.7% | 7 | 46% |
| Ouroboros | 32 | 18.8% | 18.1% | 31 | 3% |
| OopsGotYourElo | 29 | 64.1% | 63.6% | 28 | 3% |

**The conditioned estimate is n=1 or n=2 for four of the five LOKI-19 panel
cells.** Lunds reads 80.0% off a single match; farming reads 20.0% off a single
match. **Those are not corrections, they are coin flips**, and the two cells where
the conditioning *is* well-powered (Ouroboros n=31, OopsGotYourElo n=28) are
precisely the two where the opponent has barely changed — 3% stale — so there is
nothing to correct.

**The conditioning is well-powered exactly where it is unnecessary and
unavailable exactly where it matters.**

## 3. ⛔ AND MY OWN US-ONLY NUMBER DOES NOT CONFIRM THE LEAGUE-WIDE ONE — STATED BECAUSE IT WOULD BE EASY TO IMPLY IT DOES

Mean inflation where measurable: **+1.4pp (median +0.5pp)** across 18 opponents —
the *wrong sign* against sweep 22's league-wide **−4.8 to −8.8pp**, and dominated
by noise (Lunds −48.0pp, farming +30.9pp, Bisons +18.6pp, all on n≤8).

**This is not a contradiction and must not be reported as one.** The two cuts are
different estimators on different populations:

| | sweep 22, league-wide | this cut, us-only |
|---|---|---|
| our own version | **frozen inside each block** | **free — v95…v108 all pooled** |
| n per comparison | 4,157 blocks | **1–31 matches** |
| population | all teams, third-party | us only |

**The us-only cut is far too underpowered to confirm OR refute the league-wide
finding, and that is itself the result: we cannot currently measure our own
exposure to this bias on our own data.** The league-wide blocked estimate is the
only instrument that can see it, and it sees it because it has 4,157 blocks and a
frozen reference — neither of which our own record provides.

## 4. WHAT TO DO INSTEAD, GIVEN THE REPAIR IS UNAVAILABLE

1. **Treat every per-opponent statistic in the repo as biased HIGH by a
   known-sign, order-5-to-9pp amount** — direction and significance are what
   replicated, not the magnitude. Do not apply a point correction.
2. **Stop quoting per-opponent shares to one decimal.** A number 70% of whose
   support is a bot that no longer exists does not carry a decimal place.
3. **Prefer cells where the opponent is STABLE**, not cells where our sample is
   large — those are different properties and today they are nearly opposite.
   Ouroboros and OopsGotYourElo (3% stale) are the only two cells in our record
   whose stored statistics currently describe the bot we would meet.
4. **The `oppver` column that would make this cheap is NULL in
   `ladder_games.tsv`.** `league_matches.tsv` and the `replay_archive/*.meta.json`
   sidecars are the only surfaces that carry it. Anything computing a per-opponent
   number off `ladder_games.tsv` is blind to this by construction.

## 5. WHAT THIS IS NOT

Us-only, 10 days, one league, **matches not games**, and no blocking on our own
version. **It measures our EXPOSURE (69.9% stale) reliably and the SIZE of the
resulting bias not at all.** Under `FIXTURE_OF_RECORD: live_unrated` it prioritises
a change in how we compute, and closes nothing.
