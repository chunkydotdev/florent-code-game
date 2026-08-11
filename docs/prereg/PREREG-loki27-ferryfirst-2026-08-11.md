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

---

# AMENDMENT 1 — 2026-08-11, ADD-ONLY, WRITTEN BEFORE ANY THROW DECODE

**BLINDNESS DISCLOSURE, precisely.** At the time of writing I HAVE seen the leg's
**win/loss** results (7/25 games, below). I have **NOT** run any throw decode, and
`corpus/throws.tsv` has not been read or refreshed for these five matches. **The
mechanism counts this amendment sizes are unknown to me.**

**RAISED BY THE SIDE LANE, and the defect is mine:** the document sized the bar it
CANNOT resolve (game share, ±20pp, disclosed) and left the bar it CAN resolve —
the mechanism — as a **direction with no threshold and no n**. That is obligation
12, landing on the half of the document that decides the plank's life.

## 1a. THE COMPARATOR IS PINNED — MEASURED, NOT STORED

The original table said `incumbent (corpus) 0.91` while the falsifier said
*"versus v104 on the same cells"*. **Those are different comparators and the
document did not say which binds. THE MEASURED ONE BINDS.**

⇒ **A v104 control arm on the SAME FIVE CELLS is REQUIRED for a verdict.** The
0.91 is pooled over 3,772 games across all opponents and eras and cannot stand in
for five specific teams rated +64..+116 above us — least of all on the axis this
document already flagged as unmeasured (whether these cells' games last long
enough for the launcher to survive to ferry time). **Those two limitations are one
defect and the original listed them apart.**

**If the control arm is not fired, the leg's verdict is INADMISSIBLE, not a
refutation.**

## 1b. THE THRESHOLD, PRE-COMMITTED WHILE THE COUNT IS UNKNOWN

Sizing (side lane's arithmetic, adopted): control 0.91 INSERT/game × 25 games
≈ **22.75 expected, Poisson sd ≈ 4.77**. Against a 25-game control arm the
difference of two counts has sd ≈ **6.75**.

⇒ **INFORMATIVE BAND AT 25v25: the leg can only resolve a rise of ≈ +59%
(≈ 36 vs 23 INSERTs). Throw counts are overdispersed, so +59% is the OPTIMISTIC
end.**

**PRIMARY MECHANISM STATISTIC: the INSERT:EXILE RATIO** (the second falsifier
already preferred it, and it is the one immune to "we simply throw more of
everything").

| outcome | verdict |
|---|---|
| INSERT:EXILE ratio rises by ≥ 2 sd of the difference | **MECHANISM CONFIRMED** |
| ratio falls by ≥ 2 sd | **DEAD** — mechanism runs backwards (the `_v139heal` outcome) |
| **inside the band** | **NO INFORMATION — back to the pool, NOT demoted** |
| INSERT ≈ 0 in BOTH arms | **INADMISSIBLE** — precondition absent |

## 1c. ⛔ THE ORIGINAL FALSIFIER IS WITHDRAWN AND REPLACED

**WITHDRAWN:** *"if INSERT throws/game do NOT rise versus v104 on the same cells,
the plank is DEAD regardless of game share."*

**WHY:** as written, a plank that genuinely lifts ferries **+25%** reads flat at
this n, trips "DEAD", and gets written up as a refuted mechanism. **That is D61 —
a screen calibrated to reject everything short of a huge effect — reproduced on
the bar built to be the honest one, one session after the lesson.** A false
negative here costs a plank nobody hears about again.

**REPLACED BY** the four-way table in 1b: **a null result inside the band returns
the plank to the pool and is NOT a refutation.**

## 1d. WIN RESULT, RECORDED FOR COMPLETENESS AND NOT AS A VERDICT

**7 of 25 games = 28.0%** (kladde 0/5, Big O 2/5, HTTP 418 2/5, Leviathan 2/5,
0033 1/5). Rating-expected share against this band is **37.0% (9.26 games)**;
sd of a 25-game draw is 2.4 games, so the observed sits at **−0.94 σ**.
**INSIDE THE NOISE. This resolves nothing about the plank and is not evidence
against it** — it is recorded so that a later pooled read has the row.

## 1e. LABEL CORRECTION — THIS AMENDMENT IS NOT `ADD-ONLY`, AND THE CLAUSE THAT PERMITS IT

**DISCLOSURE OF MY STATE AT THIS WRITING, which is later than §1a–1d:** I have now
decoded the **TREATMENT** arm's throws (INSERT 13, EXILE 60 over 25 games). I have
**NOT** fired or seen the **CONTROL** arm, which is the comparator every bar in
§1b is written against. **This section changes NO bar, NO threshold and NO
branch** — it corrects a heading and states an argument that was implicit.

**Raised by the side lane, and the correction is theirs on my document.** §1c
WITHDRAWS a falsifier, so `ADD-ONLY` is the wrong label. The s28 rule permits an
amendment that **adds a constraint** *or* **fixes a rule whose inputs do not yet
exist**. This qualifies under the **SECOND** clause — the mechanism counts were
undecoded and `corpus/throws.tsv` unread for these five matches when §1a–1d were
written and committed (`a606cdd`). **That is the clause that legitimises it and I
did not cite it.**

⇒ **AMENDMENT 1 is permitted under the "inputs do not yet exist" clause and
contains one WITHDRAWAL (§1c).**

**AND THE DIRECTION IS THE POINT, because I disclosed seeing 7/25 win/loss before
writing it.** A reader who sees a poor game share followed by a loosened death
condition should ask the obvious question, so the document answers it rather than
leaving it to them. **The two bars moved in OPPOSITE directions:**

* **CONFIRMATION got STRICTER** — from *"RISES"* (any amount satisfies) to
  *"INSERT:EXILE ratio rises by ≥ 2 sd of the difference"*.
* **REFUTATION got LOOSER** — a DEAD branch became NO INFORMATION.

⇒ **The amendment CANNOT flatter this plank into a CONFIRM.** It made confirming
harder and made a null survivable. That is the asymmetry the ADD-only rule exists
to enforce, and it is satisfied in substance even though the label was wrong.
