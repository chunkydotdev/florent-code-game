# PREREG — LIVE-UNRATED BASELINE for v102 (LOKI-8), under the new currency

**Committed BEFORE any leg is created.** Two-clock standard: this file's git
author time must precede every leg's platform `createdAt`.

Line `loki`. **No treatment.** This is the CONTROL every trick leg from now on
is measured against, and it exists because Magnus's 2026-08-10 directive changed
what counts as a win — every banked figure we have was scored under the old one.

## Why a baseline leg is the first thing fired

`FIXTURE_OF_RECORD: live_unrated` is new. **We have no live-team measurement of
the live bot under the new definition of a win.** Our arena is self-authored and
lies in a known direction (s26 D21); our ladder tape records wins and losses but
not *how* they ended against *whom*. Firing a trick prototype first would give a
treatment number with nothing legitimate to subtract.

**Cost: ZERO rated exposure.** v102 is already the active submission, so these
legs use the bot the ladder is already playing. Nothing is activated, nothing is
risked. This is the one leg in the programme that is free, which is the reason
it goes first rather than the reason it is worth doing.

## Opponents — six teams, chosen before firing and listed so the set cannot grow

Bracketed around us (OpenSverige, 1599, rank 28) so the sample is the field we
actually meet, not the field we would like to beat:

| team | rating | rank | team id |
|---|---|---|---|
| The Bisons | 1626 | 25 | f670dfed-dfee-421b-8c01-a67b8a278ce3 |
| I Stone | 1617 | 26 | bfbb9a68-b37a-4a61-b0ea-d36369c8f65a |
| Leviathan | 1603 | 27 | 26286680-d861-4f9e-9073-a6201bd48d3b |
| gsxWins | 1594 | 30 | ebd8d82a-7365-4ccb-af0b-defea3a1ac4d |
| CtrlAltDefeat | 1581 | 31 | 74e43df6-bad7-474b-8e37-0ea44a2c80f1 |
| Ouroboros | 1578 | 32 | a5631594-3000-457e-890d-29d547f9de93 |

Five games each = **30 games**. Two of these teams (CtrlAltDefeat, Ouroboros)
have hand-built imitations in `bots/*_probe`, which makes them the first honest
opportunity to ask **how wrong our imitation of a specific team is** — that
comparison is recorded as a secondary and is not a bar.

## What is measured — the currency, stated before the data exists

**PRIMARY: `r1000_rate` — the share of games reaching round 1000.** Under
`R1000_IS_DEFEAT: yes` this is a LOSS RATE, and it counts games we *win* on
tiebreak as losses. Reported with a Wilson interval on n=30.

**PRIMARY: `core_kill_share`** — share of games ending `core_destroyed` in our
favour, and the same for theirs. `PROGRAMME.md` currency, unchanged.

**SECONDARY, reported and never substituted for the above:** median and
distribution of **time-to-core-kill** for the games we win by kill, against the
`KILL_WINDOW_RND: 250` bar; per-opponent split.

## Bars

**There is no pass/fail bar, because a baseline cannot fail.** What is
pre-committed is the USE: these six numbers become the denominator and the
control for the trick legs that follow, and **no later leg may silently swap in
a different control population.**

Two things I am pre-registering so they cannot be discovered as convenient:

* **`r1000_rate` on the ladder tape is ~7% for v102** (8 of 115 attributed
  games, s26 research). **If the live-unrated rate lands far from that, the two
  populations are not interchangeable and I will say so before using either.**
* **If our own core dies in a materially larger share of these games than the
  ladder tape suggests, the unrated pool is harder than the ladder pool** — a
  bias that would flatter every future trick leg's control arm. Checked here,
  once, while it is free to check.

## Falsifier for the FIXTURE claim itself

The directive asserts live teams *"beat our own calculations every time."* This
leg can embarrass that: if the six live opponents produce roughly what our probe
arena produces on the same metrics, then the fixture upgrade bought less than
claimed. **I will report that outcome if it occurs** rather than banking the
fixture change on its own authority.

## What this leg does NOT do

It tests no trick, changes no bot, and is not evidence for or against any plank.
It is a ruler, cut before the thing it measures.

---

## ADDENDUM — **METHOD CORRECTION FROM MAGNUS, AFTER THE FIRST 25 GAMES FIRED**

> *"Previously we ran tests against opponents but for 5 specific maps until
> something interesting happened on those, and sometimes we rotated the maps
> when we wanted to try something else."*

**He is right and the leg I just fired is defective as a control.** I omitted
`--map`, so the platform chose 5 random maps PER MATCH. The 25 games span
**13 distinct maps**, and no two opponents played the same set. Consequences,
stated plainly rather than buried:

* **This leg is a FIELD READ, not a paired control.** A later treatment leg with
  its own random maps would differ from it by map as much as by treatment, and
  map is the dominant term here — our kill turns range 99-524 and track map size.
* **It is not worthless** — the aggregate rates below are real and were measured
  on real opponents. It just cannot be the denominator the prereg promised.
* **It cost nothing** (v102 was already active), so the correction is cheap.

**THE TESTBED IS NOW PINNED**, and every leg from here uses it unless a rotation
is recorded as a deliberate act:

    MAPS (fixed, size-ordered so kill-distance is a controlled axis):
      fjordgate 10x10 · jackpot 16x16 · atoll 18x18 · saga 24x24 · snowflake 26x26

    PANEL (fixed): The Bisons 1626 · I Stone 1617 · Leviathan 1603 ·
                   gsxWins 1594 · CtrlAltDefeat 1581

    ONE LEG = 5 opponents x 5 pinned maps = 25 games = ONE 10-minute window,
    because the platform enforces **max 5 test/unrated matches per 10 minutes**.

Residual confound left on the record: `mapSeed` still varies per game, so the
pinning controls terrain but not spawn seed.

## RESULT OF THE UNPINNED BASELINE (n=25, 5 live teams, v102)

| metric | value | note |
|---|---|---|
| wins | 14/25 = 56.0% | not a verdict (PROGRAMME) |
| **r1000 rate (= DEFEAT rate)** | **0/25 = 0.0%** | **95% CI 0-13.3%** |
| core_destroyed | 25/25 = 100% | every game ended in a dead core |
| our core-kill share | 14/25 = 56.0% | primary currency |
| our kills inside 250 rounds | 10/14 | median 151, range 99-524 |
| THEIR kills against us | 11, median 162 | range 49-393 |

**THE PRE-REGISTERED CHECK CAME OUT DIFFERENT AND THAT IS THE POINT.** The
prereg predicted ~7% r1000 from the ladder tape. **Live-unrated gave 0/25.** The
two populations are not interchangeable, as pre-committed — and the direction is
favourable: against real teams our games are decisive, so `R1000_IS_DEFEAT` is
currently costing us almost nothing. **The bottleneck is not that we stall to
r1000; it is that we lose the kill race 11 times in 25.**

**THE SURPRISE, recorded before it is explained away (directive point 4):**
**The Bisons beat us 4-1 and killed our core in 74, 66, 92 and 49 turns.** That
is our own sub-250 doctrine executed on us, roughly twice as fast as we execute
it. They are rank 25, 27 points above us. **A live opponent already does the
thing this programme is trying to learn**, and their replays are downloadable.
