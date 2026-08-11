# PREREG — LOKI-27 "FERRY FIRST": a fresh ferry request outranks a home exile

**Arm:** builder, s31, 2026-08-11. **Committed BEFORE leg creation** (two-clock
standard: this file's git author time vs the platform `createdAt` of the first
unrated match).

**Bot:** `bots/_v148ferryfirst`. **Control / incumbent:** `bots/_v130loki13` = v104.

---

## TARGET BAND (gate run BEFORE this document — `tools/target_value.py --band`)

**TARGET BAND: kladde chatte tville (+116), Big O (+96), HTTP 418 (+94),
Leviathan (+92), 0033 (+64); gaps +64..+116; win pays +18.91..+21.16;
reachable YES.**

All five sit inside the reachable band (`us-80..us+125` at our 1672) and are the
five highest-paying opponents in it. This is the opposite of s28's failure, where
a flawless leg was aimed at four teams 550–860 points below us and a perfect
result paid under 5 rating points.

## THE PLANK

`raid.py` evaluates EXILE (throw an enemy builder away from our launcher) before
FERRY (throw our own raider into the enemy half), and **EXILE returns on
success**. So one enemy builder wandering within d²≤2 of our launcher pre-empts
ferrying a raider forward — every time both are available.

**EXILE is home defence. FERRY is delivery into the enemy half.**
`PROGRAMME.md: PLAY_DEFENCE: never` says which should win, and in the incumbent
the defensive one was winning. The diff adds a `ferry_pending` test and a
`continue` past the exile branch when a fresh ferry request exists.

**Corpus scale of the inversion:** 34,703 EXILE throws by us against 3,434
INSERTs — 10:1 toward ejection, 0.91 ferries per game over 3,772 games.

## WHY THIS ONE, AND THE PART THAT IS NOT IN ITS FAVOUR

Selected from three surviving candidates (best-fit 524/1024, cap6 519/1024,
ferry-first 518/1024 in s30's self-play screen). **All three are INSIDE the
informative band (≤480 or ≥543) — so the screen did NOT establish any of them is
better, and I am not claiming it did.** Ferry-first was chosen on three grounds
that are not its point estimate:

1. **Largest seat-A signal** — 304/512 = 59.4% seat A vs 214/512 = 41.8% seat B.
   ⚠ **This is currently UNINTERPRETABLE**: all eight s30 arms won more from seat
   A, which is the signature of a fixture asymmetry. A 4,096-game null is running
   to discriminate. **If the null shows an ~+8pp seat effect, this reason
   evaporates** and only 2 and 3 below survive. Written down before the null
   lands so it cannot be retro-fitted.
2. **Programme alignment** — it removes a defensive branch that pre-empts an
   offensive one. On-line under `PLAY_DEFENCE: never`.
3. **Cheapest mechanism dose** — throw type is on the wire and already decoded.

**Selection effect, stated up front:** these are the top of nine screened arms,
so the point estimate is biased upward by the max-of-nine. I do NOT expect
+0.6pp on the ladder.

## PRIMARY BAR — and it is denominated in the primary currency

**`PRIMARY_CURRENCY: game_share`.** Bar: **game share across the 25 unrated games
vs v104's game share against the same five cells.**

⛔ **THIS LEG CANNOT RESOLVE GAME SHARE AND I AM SAYING SO BEFORE FIRING.**
25 games has an MDE of roughly ±20pp. Per the booted rule — *"STOP CALLING
UNDERPOWERED LEGS… a 25-game window is a DOSE AND MECHANISM probe"* — **this leg
is registered as a DOSE AND MECHANISM probe, not a currency read.** Game share is
recorded, and a currency verdict requires pooling further windows.

## THE MECHANISM BAR — THIS is what the leg resolves

Decoded from the leg's own replays via `tools/corpus/replay_throws.py`:

| quantity | incumbent (corpus) | prediction if the plank works |
|---|---:|---|
| INSERT (ferry) throws / game | 0.91 | **RISES** |
| EXILE throws / game | ~9.2 | falls or holds |
| INSERT : EXILE ratio | 1 : 10.1 | **shifts toward INSERT** |

**FALSIFIER (pre-registered, and it is the one that killed the heal arm):**
**if INSERT throws/game do NOT rise versus v104 on the same cells, the plank is
DEAD regardless of game share.** A positive point estimate is not a mechanism —
`_v139heal` was the joint-top arm at 524/1024 and its dose check showed it healing
3.5× MORE than the control it was supposed to cut.

**SECOND FALSIFIER — the LOKI-25 guard:** if INSERT rises **only** because total
throws rose (i.e. we simply throw more of everything), that is buying the
numerator. The INSERT:EXILE **ratio** must move, not just the count.

## PRECONDITION ADMISSION — checked per cell, per the s29 rule

The rule: *a panel is admitted FOR A MECHANISM; measure that mechanism's
PRECONDITION per cell before firing.*

**This plank's precondition is OUR OWN behaviour, not the opponent's** — it fires
whenever we hold a launcher and a raider has a fresh ferry request. That is
unlike LOKI-19, whose precondition was enemy arrival rate and where only one of
four admitted cells delivered the premise.

⚠ **What I have NOT checked and am recording as a limitation:** whether these
five cells' games last long enough, and pressure us little enough, for the
launcher to survive to ferry time. **Admission on that axis is unmeasured.** If
INSERT reads ~0 in BOTH arms, this leg measured nothing and the correct verdict
is INADMISSIBLE, not a refutation.

## PROCEDURE — the rated-cost controls

* Fire **just after an observed pairing**. Cadence re-derived from the last 14
  ladder rows this session, **not taken from any doc**: 14/14 at `:12:59`,
  `:32:59`, `:52:59`. Firing after the 12:32:59 pairing.
* `tools/unrated_run.sh` only — never a hand-rolled runner (its outfile must match
  `scratchpad/arm_*.txt` or `rate_budget.py` cannot attribute the spend).
* **Budget the leg at ~−8 Elo per leaked rated match**, not at zero. The measured
  cost of an arm rotation is −24.67 Elo across 3 leaked matches.
* Holder restored to **v104** and confirmed on the `Active bot:` line, never on
  `$?`.
* Rate limit: **5 test/unrated matches per 20 minutes**, rejections count.

## WHAT WOULD MAKE ME DROP THIS PLANK

* INSERT throws/game flat or down → **DEAD** (primary mechanism falsifier).
* INSERT up but INSERT:EXILE ratio flat → **DEAD** (bought the numerator).
* INSERT ~0 in both arms → **INADMISSIBLE** (precondition absent), not refuted.
* Any uncaught exception / unit destruction attributable to the diff → **DEAD**.
