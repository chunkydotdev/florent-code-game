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
