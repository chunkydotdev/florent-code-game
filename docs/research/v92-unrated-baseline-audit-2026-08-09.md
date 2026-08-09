# Audit of the "4-13" v92 unrated baseline — and the r74 core kill sitting inside it

**Research arm, session 25, 2026-08-09 16:24 CEST (commit `b9394ef`).** Unprompted check, in-lane: the
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

- ~~**It is the fastest core kill on our record**~~ — **CORRECTED BY ME, ~20 minutes after
  publishing, see §6. IT IS NOT.** It is the fastest core kill **against CAD** (ladder best
  vs CAD is r103, n=15). On the ladder overall we have **827 core-kill wins with a median
  of r151**, the fastest at **r58**, and we have killed **Ouroboros at r65**. The corrected
  claim is scoped to CAD and is still worth the autopsy; the unscoped one was wrong.
- It is nevertheless deep inside `KILL_WINDOW_RND: 250` — the PROGRAMME's own window. Of
  the ten unrated games examined across both Ouroboros legs, exactly one landed inside r250
  (the Loki-2b r211). This one is r74.
- **It was produced by v92 — the Eir lineage — not by the Loki line.** The bot the Loki
  programme is trying to beat on `core_kill_share` has already killed a hard-five core
  inside a third of the window.
- **It is against the opponent the campaign plan says NOT to rush.** That plan's table
  reads CAD's objective as *"SURVIVE to r1000"* because we take their tiebreak ~80%. That
  reasoning is about the *tiebreak being winnable*; it is not evidence their core is
  hard to reach. An r74 kill is direct evidence it is reachable, at least on nordkap/a.
- **The replay is ALREADY ON DISK** — `replay_archive/f92f1ca2-19ea-44b7-8ba3-b19e93917e46_game_5.replay26`,
  and all five games of the leg plus the `.meta.json`. **A no-download autopsy of our
  fastest kill AGAINST CAD is available right now** (scope corrected per §6 — it is not
  our fastest kill overall).

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

---

## 6. AMENDMENT, ~20 MINUTES AFTER PUBLISHING — I OVERSTATED §4, AND THE CORRECTION IS A BIGGER FINDING THAN THE THING I CORRECTED

**What I got wrong.** §4 called the r74 CAD kill *"the fastest core kill on our record."*
**It is not.** I had checked it against the ten unrated games in front of me and never
checked it against the ladder — the classic assumed-denominator error this project keeps
logging, committed by me in the same session I caught two of them in other people's work.

**The corrected claim, from the frozen `ladder_games.tsv` (2,715 game rows):**

| | n | median | ≤250 | fastest |
| --- | ---: | ---: | ---: | ---: |
| **all our ladder core-kill wins** | **827** | **r151** | **615 (74.4%)** | **r58** |
| vs Ouroboros | 9 | r95 | 8 | **r65** |
| vs Lunds Stallions | 30 | r150.5 | 27 | r80 |
| vs Kings College Munich | 13 | r132 | 11 | r83 |
| vs CtrlAltDefeat | 15 | r194 | 9 | **r103** |
| vs Powerpuff Girls | 20 | r219.5 | 13 | r115 |

So r74 is **the fastest kill we have against CAD** — the ladder best against them is r103 —
and that scoped claim still makes the autopsy worth running. **The unscoped claim was
wrong and is struck.**

### AND HERE IS WHY THE CORRECTION MATTERS MORE THAN THE ERROR

**When we win by core kill, we ALREADY do it inside r250 — 74.4% of the time, median r151.
And it does not depend on opponent strength:**

| opponent rating at match time (`oppbef`) | our core-kill wins | median | ≤250 | ≤100 | **core_kill_share** |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1600+ | 189 | r161 | 71.4% | 37 | **189/535 = 35.3%** |
| 1550-1599 | 176 | r159 | 74.4% | 48 | 176/675 = 26.1% |
| 1500-1549 | 278 | r137 | 77.0% | 90 | 278/680 = 40.9% |
| <1500 | 184 | r161 | 73.4% | 47 | 184/825 = 22.3% |

**`KILL_WINDOW_RND: 250` is not a binding constraint on us.** It is satisfied in roughly
three of every four core-kill wins we already have, at every rating band including 1600+.
What is scarce is **the kill happening at all** — `core_kill_share` runs 22–41%.

**The sharpest case is Ouroboros, and it bears directly on the live Loki programme:** we
have **9 core-kill wins in 155 ladder games (5.8%)**, and **8 of those 9 are inside r250,
median r95.** Against Ouroboros we are already fast when we kill; we are simply almost
never killing. **A plank that makes an Ouroboros kill FASTER is optimising the dimension
that is already satisfied.** The LOKI-2b verdict's headline — median core-kill turn
198→163 — moves `time_to_core_kill`, the SECONDARY currency, on a dimension where our
median against that opponent was already r95.

**This is data, not a verdict, and re-aiming the programme is Magnus's call, not mine.**
But `PROGRAMME.md` names `core_kill_share` PRIMARY and `time_to_core_kill` SECONDARY, and
the ladder says the primary is where all the missing value is.

**Method note on my own error, recorded because it is the third instance of this family
in two sessions:** I compared a number against the population I had just loaded rather
than the population the claim was about. The corpus was already synced and one
`csv.DictReader` away. **A superlative ("fastest", "most", "never") is a claim about a
denominator, and it must name the denominator in the same sentence or not be made.**
