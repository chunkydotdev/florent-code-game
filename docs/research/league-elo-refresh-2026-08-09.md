# League Elo refresh + per-team trajectories — and a correction to my own interim

**Research arm, session 25, 2026-08-09 19:44 CEST (from `date`).** Commissioned by the side lane off
Magnus's question *"don't we have everyone's Elo?"* — we do, but the table was stale.

**Source: the free `match list --team` channel only, 116 teams, 278 s, zero replay
downloads.** `corpus/league_matches.tsv` rebuilt: **29,680 unique ladder matches**,
newest row **2026-08-09T17:32:43Z = 19:32 CEST** (11 minutes old at completion), against
the previous table's newest of **05:12:43Z** — **12.4 hours stale**, as corrected.

---

## 0. CORRECTION TO MY OWN INTERIM, BEFORE ANYTHING ELSE

**While the sweep was running I reported "the league has 116 teams, not 71 — the stale
table was missing 45 teams entirely, so every field statement today was made on ~61% of
the league." THAT IS WRONG.**

**116 teams are REGISTERED. 44 of them have played ZERO games** (`rating 0 played 0` —
`old`, `Hrsi`, `3D`, `Viterbi`, `Deploy`, `john3:16`, `bot4bot`, `PixelBotics`, …).
**Active teams: 72.** The previous table carried **71**. **The roster grew by ONE active
team, not 45, and the old table covered 98.6% of active teams, not 61%.**

I read a registration count as a participation count — **the assumed-denominator error, my
third of the day**, after the r74 superlative and the staleness figure. The pattern in all
three is identical: **a count was available, I did not ask what it counted.**

**What survives from that interim:** the roster *is* a second staleness axis, and a
timestamp cannot reveal it. That point stands; the magnitude I attached to it does not.

## 1. THE FIELD, TOP OF TABLE

| # | team | Elo now | Δ today | games today |
| ---: | --- | ---: | ---: | ---: |
| 1 | sporks | **2102.2** | +20.2 | 105 |
| 2 | Clankers | **2040.6** | **+105.0** | 106 |
| 3 | not adgato | **2000.2** | **+106.7** | 106 |
| 4 | Pivot | 1976.9 | +34.3 | 106 |
| 5 | Pantheon | 1966.0 | −38.8 | 105 |
| 6 | Lorem Ipsum | 1955.4 | −14.5 | 105 |
| 7 | Jython | 1951.5 | +3.2 | 106 |
| 8 | Erebus | 1936.9 | +33.7 | 105 |

**The league plays ~105 ladder games per team per day**, so daily movement of ±100 Elo is
normal at the top and a single-day delta is not a small-sample artifact.

## 2. ORIZON — the side lane's observation is CONFIRMED, and their figure was exact

**Orizon: 1396.2 now. −70.3 since the stale snapshot (05:12Z), over 73 games. −37.3 since
midnight, over 105.** The side lane relayed *"shed ~70+ Elo since the snapshot"* — **that
is right to the decimal band, and my "12.4h" correction did not disturb it.**
**Below 1400 confirmed.**

**The fall is DIFFUSE, not a single matchup.** Today's Elo contribution by opponent, worst
six: Oresund Overflow **−43.18**, diverge −34.42, Klarum −24.43, the one piece −18.20,
LingLing40 −16.34, Memtrace −13.37. **No single opponent explains it** — the sum of the
worst six exceeds the day's net, i.e. it is a broad decline partly offset elsewhere.
**"Who they were playing when they fell" is not "who caused it", and I am not claiming
the latter.**

## 3. THE FIXTURE AND HARD-FIVE TEAMS

| team | Elo now | Δ since snapshot | Δ today |
| --- | ---: | ---: | ---: |
| **OpenSverige (us)** | **1603.6** | **+48.6** | **+53.7** |
| gsxWins | 1634.5 | — | +7.6 |
| Powerpuff Girls | 1622.1 | — | +16.5 |
| CtrlAltDefeat | 1602.8 | −6.6 | −23.2 |
| Lunds Stallions | 1567.6 | +52.0 | +31.7 |
| Kings College Munich | 1555.7 | — | **−63.0** |
| Ouroboros | **1542.0** | +33.2 | −27.6 |
| **Orizon** | **1396.2** | **−70.3** | −37.3 |

**Fixture consequence, stated as data:** **Orizon at 1396 is ~208 Elo below us** and,
per the side lane, has left our matchmaking bracket. **Ouroboros at 1542 is now 62 below
us**; CAD is level (1602.8 vs our 1603.6).

## 4. SHARPEST MOVERS SINCE THE SNAPSHOT (12.4 h, ~73 games each)

**Falls:** Hiver01 −131.0 · Kleos −94.5 · The Bisons −70.7 · **Orizon −70.3** · HTTP 418
−64.8 · Cookie −64.7
**Climbs:** diverge **+131.7** · not adgato +101.3 · Erebus +63.8 · LingLing40 +58.0 ·
Clankers +57.4 · Lunds Stallions +52.0

## 5. METHOD AND LIMITS

Trajectories come from **`ratingABefore`/`ratingBBefore`** per match — the at-match field
that reconciles against `eloDelta`. **`teamARating`/`teamBRating` are LIVE JOINS**
(CLI trap 2) and are never used. Script:
`docs/research/scripts/elo-trajectory-2026-08-09/elo_traj.py`.

- **The rating history is recoverable from rows we already had** — we were never limited
  to the latest state, only to the latest *pull*. A dated-snapshot cadence would still be
  better, because it also captures **roster** change, which no row timestamp reveals.
- **"Δ today" is measured from 2026-08-09T00:00:00Z**, "Δ since snapshot" from the previous
  table's last row (05:12:43Z). Both stated rather than implied.
- **Per-opponent Elo attribution is contribution, not causation.**
