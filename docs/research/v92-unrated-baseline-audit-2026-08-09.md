# Audit of the "4-13" v92 unrated baseline — and the r74 core kill sitting inside it

**Research arm, session 25, 2026-08-09 ~16:45 CEST.** Unprompted check, in-lane: the
`4-13 vs the five hard teams` line is now, by the builder's own words at
`docs/coordination.md:16805-16809`, *"the denominator LOKI deltas get measured against
from here."* A denominator that load-bearing gets verified against primary source before
anything is measured against it.

**Version tag.** Live slot **v94** = `bots/_v115dodge`, treehash `6ae6871c`. The audited
baseline is **v92**; the probe leg is **v93** = `bots/_v118loki2b`.
**Source: the free channel only** — `fcode match list --type unrated --mine --limit 60
--json` (60 matches returned) and `fcode match info --json` on four match ids.
**Zero replay downloads.** No corpus file was used; the corpus cannot see unrated games.

---

## 1. THE NUMBER RECONCILES EXACTLY

Reconstructed independently from the platform, then checked against the record:
Ouroboros 1-4, CAD 1-4, KCM 1-3, Lunds 1-1, Powerpuff 0-1 → **4 wins, 13 losses.**
Matches `coordination.md:16806` verbatim, per opponent. **The number is right.**

## 2. BUT IT IS 17 GAMES FROM LEGS OF 5 / 5 / 4 / 2 / 1 — AND THAT IS BY CONSTRUCTION

`mapConfig` length per leg, from `match info`:

| opponent | match | maps in leg | our score | core-decided |
| --- | --- | ---: | --- | ---: |
| CtrlAltDefeat | `f92f1ca2` | 5 | 1-4 | **5/5** |
| Ouroboros | `3c6d91d2` | 5 | 1-4 | 3/5 |
| Kings College Munich | `f90d003f` | 4 | 1-3 | 3/4 |
| Lunds Stallions | `d6c71870` | 2 | 1-1 | 1/2 |
| Powerpuff Girls | `42fcf8ce` | 1 | 0-1 | 0/1 |

All five are `status: complete` with `errorMessage: null` — the short legs were **fired
short**, not truncated by failure. (The campaign plan itself flags the cause at
`unrated-campaign-plan-2026-08-09.md:70`: the rate limit is 5 unrated per 10 minutes, and
six legs went out inside five minutes.)

**Consequence, and it is the whole reason to write this down: `4-13` is game-pooled, not
opponent-equal-weighted.** Ouroboros and CAD carry **29% of the denominator each**;
Powerpuff carries **6%**. Any future "LOKI delta vs the baseline" that treats the five
teams as five comparable cells is weighting a 1-game leg equally with a 5-game one. **Say
the per-opponent Ns, or compare per-opponent.**

## 3. THE 3/5 → 5/5 "CORE-DECIDED MIX" IS NOT SIGNIFICANT, AND v92 ALONE ALREADY PRODUCES 5/5

The side lane's cleanest surviving datum from the Loki-2b leg is that the win-condition
mix moved **3/5 → 5/5 core-decided** at fixed opponent (Ouroboros). Two checks:

**(a) Fisher's exact test on that 2×2: one-sided p = 0.2222, two-sided p = 0.4444.**
Five games against five games on a binary outcome cannot reach significance from this
gap. It is a direction, not a result.

**(b) At FIXED bot version v92, in the SAME 13:20–13:25Z batch, core-decided share runs
the full range across opponents:**

| opponent | core-decided | share |
| --- | ---: | ---: |
| CtrlAltDefeat | 5/5 | **100.0%** |
| Kings College Munich | 3/4 | 75.0% |
| Ouroboros | 3/5 | 60.0% |
| Lunds Stallions | 1/2 | 50.0% |
| Powerpuff Girls | 0/1 | 0.0% |
| **pooled** | **12/17** | **70.6%** |

**So "5/5 core-decided" is not a Loki-2b signature — v92 produces it against CAD.** The
statistic is dominated by opponent identity. The Ouroboros-vs-Ouroboros comparison is
still the right one to make (same opponent both legs), so this does not destroy the
datum; it sizes it. **The between-opponent spread at fixed version is 0%→100%, which is
wider than the 60%→100% the probe is being read for.**

## 4. THE FINDING NOBODY HAS PICKED UP: **v92 KILLED CAD'S CORE AT ROUND 74**

`f92f1ca2` game 5, **nordkap**, we are seat **a**, `winCondition: core_destroyed`,
`turnsPlayed: 74`, **`resignMessage: null`** — checked, so it is a real kill and not a
crash or a forfeit.

Why this matters more than the leg it sits in:

- **It is the fastest core kill on our record, and it is deep inside `KILL_WINDOW_RND:
  250`** — the PROGRAMME's own window. Of the ten unrated games examined across both
  Ouroboros legs, exactly one landed inside r250 (the Loki-2b r211). This one is r74.
- **It was produced by v92 — the Eir lineage — not by the Loki line.** The bot the Loki
  programme is trying to beat on `core_kill_share` has already killed a hard-five core
  inside a third of the window.
- **It is against the opponent the campaign plan says NOT to rush.** That plan's table
  reads CAD's objective as *"SURVIVE to r1000"* because we take their tiebreak ~80%. That
  reasoning is about the *tiebreak being winnable*; it is not evidence their core is
  hard to reach. An r74 kill is direct evidence it is reachable, at least on nordkap/a.
- **The replay is ALREADY ON DISK** — `replay_archive/f92f1ca2-19ea-44b7-8ba3-b19e93917e46_game_5.replay26`,
  and all five games of the leg plus the `.meta.json`. **A no-download autopsy of the
  single fastest kill we have is available right now.** Given that the whole programme is
  `core_kill_share` + `time_to_core_kill` inside r250, this is the highest-value
  unopened replay in the archive.

**What it is not.** n=1, unrated, one map, one seat. It does not say CAD is rushable in
general and it is not a proposal to re-aim the campaign. It says one specific thing:
**the r250 window is demonstrably reachable against a hard-five opponent by the bot we
already have**, and we found that out by auditing a denominator rather than by building
anything.

## 5. LIMITS

- Unrated legs are not a random sample of anything: opponents, maps and leg lengths were
  all chosen by us, and `match unrated` always plays **our currently active submission**
  against **their currently active** one, so opponent version is whatever they had live.
- `match info --json` reports the opponent's version as `null` (CLI trap 3, re-confirmed
  on all four legs); opponent versions here come from `match list --json`.
- Win conditions and turn counts are the platform's own fields. **The r74 game's
  mechanism has not been decoded** — this document establishes that it happened and that
  the replay is local, nothing about how.
- The 60-match `match list` window covers 2026-08-08T02:50Z onward; earlier unrated legs,
  if any, are not included.
