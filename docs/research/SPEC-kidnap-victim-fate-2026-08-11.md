# SPEC — KIDNAP VICTIM FATE: read the 36,275 doses we already have before buying more

**Written 2026-08-11 (s32, research) in answer to Magnus: *"does that mean we need
to do some live testing of the kidnap tactic on unrated ladder to see if it holds?"***

**Format is a SPEC deliberately.** The s32 adversarial audit found that in this
repo **`SPEC-*` documents get built and ANALYSIS documents mostly do not** —
`SPEC-kill-speed-score` → `PROGRAMME.md:304` + `tools/score.py`;
`SPEC-match-initiative-ledger` → `tools/match_ledger.py`; `SPEC-mutation-harness`
→ `tools/ring_read.py`. **The format predicted consumption better than the quality
did.** This is a build order, not a survey.

---

## THE ANSWER IN ONE LINE

**Yes — but not first, because we have 36,275 doses already banked and have never
read what happened to a single victim.**

## 1. THE NUMBER THAT DECIDES THE SEQUENCING

Measured by me on `corpus/throws.tsv` joined to `meta_join.us_side`
(**us-only, not field-pooled**):

| population | throws | victim fate recorded? |
|---|---:|---|
| **our throws of ENEMY builder bots** | **36,275** | ⛔ **`life = -1` (sentinel) in 36,275 of 36,275** |
| our throws of our OWN bots | 3,656 | ✅ populated (3,133 lived >3 rnds, 523 ≤3) |

**The outcome column EXISTS, is POPULATED for our own units, and is a SENTINEL for
exactly the population the plank is about.** The decoder tracks a thrown unit it
owns and gives up on one it does not.

⇒ **We have ~115× the dose of the LOKI-14 leg (36,275 vs 314) sitting in the
archive, and zero read-out.** Buying more dose before reading the dose we own is
the most expensive way to answer this question.

## 2. AND THE ARCHIVE EVIDENCE AGAINST THE PLANK IS WEAKER THAN THE QUEUE IMPLIES

I amended `QUEUE.md` #5 earlier tonight to withdraw *"highest ceiling on the
board."* **That withdrawal stands, but the evidence behind it does NOT measure the
causal quantity, and I am recording that against my own amendment:**

* **`CRASH-INDUCTION-league-wide` §2, `r(rating, crashes suffered/game) = −0.029`,
  n = 67 TEAMS — an ACROSS-TEAM correlation.** It asks *"do crash-prone teams rate
  lower?"* It does **not** ask *"does making a team crash hurt it?"* A team can be
  strong-and-buggy; those are different questions and only the second is the plank.
* **§3's within-victim estimator — the one that WOULD address causality — is
  distrusted by its own author:** sporks reads **−0.429** and Clankers **−0.805**,
  i.e. *"prevents"* opponent crashes, which is not a mechanism. **Strong teams end
  games early ⇒ fewer rounds ⇒ fewer crash opportunities**, a confound the author
  says is *"large enough to swamp the signal."*

⇒ **Neither section measures the causal effect.** Under rule 6 (*a refutation
without live-game backing is a hypothesis*) and the doc's own §5 (D12: behavioural
premise ⇒ bottom of queue, **never off it**), the road is **prioritised down, not
closed** — and it stays that way until something reads victim fate.

## 3. ⛔ AND "KIDNAP" IS NOT ONE PLANK — THE ARCHIVE IS ALL THE *OTHER* CHANNEL

**All 36,275 enemy throws are `kind = EXILE`** — ejecting an enemy builder off a
station. **Zero are the border-throw crash induction of `bots/_v131loki14`.**
The launcher throw has at least three payoff channels and they are not the same
plank:

| channel | mechanism | evidence we hold |
|---|---|---|
| **CRASH** | throw to a map-border tile → their code queries off-map → raises → **engine destroys the unit permanently** | LOKI-14's 314 throws; no rating read |
| **DISPLACEMENT** | victim is moved off its cached plan; their state goes stale | **36,275 throws, ZERO read-out** |
| **TEMPO** | victim loses N rounds of work walking back | never separated from displacement |

**The `titanium_collected`-style error to avoid here is treating a finding about
the CRASH channel as a finding about kidnap.** The 36,275 are the displacement
channel and nothing in the repo has ever scored them.

## 4. THE BUILD — one reader, then a decision

**INSTRUMENT.** Populate victim fate for enemy throws. The engine-side fact is an
**entity-removal event with no preceding damage event** — the same signal
`tools/crash_census.py` already reads, which is why this is a join and not a new
decoder. **Never our own `print()`**: stdout is stripped from platform replays
(0 of 30,664 `BotOutput` events).

Per enemy throw, emit: `rounds_survived_after_throw`, `removed_without_damage`
(bool), `d2_to_border_after`, and `victim_team_version`.

**THE COMPARISON, and it must be matched or it measures map geometry:** thrown
enemy builders vs **enemy builders on the same map, same round band, same distance
from their core, not thrown**. An unmatched contrast will report that bots near
borders die more, which is true and not the plank.

**DECISION RULE, pre-committed here before the reader runs:**
* **Elevated removal-without-damage in the thrown arm ⇒ the displacement channel
  pays and a LIVE LEG IS JUSTIFIED**, aimed at the reachable band (below).
* **No elevation at n = 36,275 ⇒ the displacement channel is dead at any dose a
  leg could deliver**, and #5 drops below #7. **That is a real close and it costs
  zero rated matches.**
* **`life` cannot be reconstructed for enemy units at all ⇒ say so and stop** —
  then, and only then, the live leg is the cheapest remaining instrument.

## 5. IF IT GOES LIVE — the gate, run now so it is not run after

`tools/target_value.py --band`, at our 1669, **16 teams reachable (us−80..us+125)**:
Leviathan +124 (**5-0 pays +21.48**), HTTP 418 +113 (+21.03), Big O +89 (+20.00),
0033 +63 (+18.89), SmartFridge/Bisons +41 (+17.9), down to gsxWins −77 (+12.50).

> **TARGET BAND: reachable band at 1669, gaps −77..+124, win pays +12.50..+21.48,
> reachable YES.**

⭐ **This is the opposite of the s28 crash leg, and that is the point.** That leg
was aimed at four teams **550–860 points below us** where a perfect result paid
**under 5 rating points**. The band above pays **14–85× more per win**. The
question is worth answering *now* in a way it was not then.

**⛔ AND THE PREREG MUST PREDICT A RATING / GAME-SHARE EFFECT, NOT A DOSE.** The
dose is the one thing already demonstrated — 314 kidnaps in LOKI-14, 36,275 in the
archive. **A leg that proves we can throw enemy builders proves something we have
known 36,275 times.**

## 6. WHAT THIS SPEC DOES NOT CLAIM

* It does **not** reopen crash induction as high-ceiling. #5's withdrawal stands.
* It does **not** assert the displacement channel works. It asserts it is
  **unmeasured**, which is a different and cheaper thing to fix.
* A `removed_without_damage` elevation is **association**, not proof of induction —
  it needs the matched control in §4 and, per rule 6, a live leg before any road is
  CLOSED on it.

---

# ⛔⛔ RETRACTION — 2026-08-11T20:2xZ. THE CLOSURE THIS SPEC AUTHORISED WAS WRONG, AND CORRECTING IT REVERSES THE SIGN.

**Flagged by the SIDE LANE. Confirmed by me against my own published result.**

**THE DEFECT — immortal-time bias.** A victim must be **alive at round R to be
thrown**, and *"alive"* includes *"has not yet been removed undamaged"*, **which
is the outcome.** The thrown arm was therefore conditioned on not having crashed;
controls were clocked from **birth** and were not. **The thrown group was depleted
of crash-prone bots BY CONSTRUCTION — in exactly the direction of the finding.**
Compounding it, the outcome was a **lifetime** property, so a victim's entire
pre-throw life sat inside the outcome window, a period during which the throw
cannot have caused anything.

**AND MY SELFTEST COULD NOT CATCH IT.** Every fixture row carried identical
timing in both arms, so **exposure and selection were equal by construction.**
The test asserted the estimator *separates an effect from no effect* — which it
did — and never that it is **unbiased when the arms differ in exposure**, which is
the clause the closure actually rested on. **The clause no assertion touches is
where the defect was.**

**CORRECTED — risk-set matching**, controls = enemy builders alive and not-yet-
removed at R, outcome = removed-undamaged strictly **after** R, one clock for both
arms. All 5,398 of our games:

| estimator | THROWN | CONTROL | delta |
|---|---|---|---|
| **naive (published, biased)** | 5/3,724 = 0.134% | 10/4,668 = 0.214% | **−0.080pp** |
| **risk-set (correct)** | **17/3,844 = 0.442%** | **13/7,341 = 0.177%** | **+0.265pp** |

**95% CI [+0.034, +0.496]pp · z = 2.25 · ratio 2.50×.**

⇒ **THE DISPLACEMENT CHANNEL IS NOT CLOSED. It is WEAKLY POSITIVE — thrown enemy
builders vanish undamaged at ~2.5× the rate of matched controls.**

⚠ **AND IT IS NOT CONFIRMED EITHER, which matters as much as the reversal.**
**17 and 13 events.** z = 2.25 on an interval that nearly touches zero.
`no_damage_removal` still conflates an uncaught exception with `self_destruct()`
(~40% of no-damage removals in `crash_census`'s own 40-file sample). **This is a
PRIORITISING signal, not a result.**

**THE SELFTEST NOW DRIVES THE BIAS ITSELF** — cell 2 builds a true-effect-ZERO
fixture where victims are alive-at-r50 by construction and controls are watched
from birth: **naive reads −50.00pp, risk-set reads +0.00pp.** The estimator that
produced the retracted number now **fails a test the shipped one passes.**

**WHAT SURVIVES UNCHANGED:** the **2.62% structural bound** (360 of 13,743
enemy-builder removals are no-damage at all) — it bounds the road regardless of
the contrast, and it was the most valuable number here. And the **scope**: all
9,372 archived throws are `EXILE`, so the **border-throw** mechanism is still
untested.

**PROCESS NOTE, because this is the second time today the pattern held.** A number
crossed out of a research document and into `QUEUE.md` as a closure within
minutes, and the defect was in the *estimator*, not the arithmetic — which the
verification I ran (controls, selftest, matched strata) was not built to see. **A
closure deserves a harder read than a finding, and I gave it the same one.**
