# v5 — What fraction of our Elo bleed has a valid instrument?

**Date:** 2026-08-08 · **Measured by: the research arm** (session `284161ab`),
scoped jointly from this series' queue. Primary deliverable:
`docs/research/v5-instrument-coverage-2026-08-08.md` (committed).
**Data:** 176 rated matches, archive-only, zero downloads.
Recorded here because it answers the question v1 raised and could not.

---

## Answer

**0.0%.** Not thin — zero.

> **DENOMINATOR SUPERSEDED — not provisional (research arm session 20).** The
> gross bleed was recorded here as **−493**; the correct figure is **−667**, and
> it is settled, not pending. Restated: **Lunds 20.3%** (was 27.5%),
> **Ouroboros 18.5%** (was 25.0%); other rows scale by ≈0.74. **The 0.0%
> coverage headline is unaffected** — it counts valid instruments, not shares.
>
> **But Elo is the wrong denominator for this question altogether**, and the
> reason is this series' own v1 fault reappearing one level up. The ladder
> splits into two regimes: **opponents ≥1550 → n=350, we win 38.9%; opponents
> <1550 → n=150, we win 71.3%.** Our headline 48.6% is carried entirely by the
> weak band. **Pooling across heterogeneous strata yields a number that
> describes neither** — structurally identical to `arena.py` pooling win rate
> across maps whose difficulty differs (v1 §1), and to the pooled-vs-blocked
> question that opened this whole series. Same fault, two altitudes, found
> independently at each. Score against the ≥1550 regime, or report both.

Net Elo is +8, and that nets a **−667 gross bleed** (superseded from −493) which
is extraordinarily concentrated in a handful of opponents:

| bleed source | share *(orig. denom. −493)* | instrument | status |
|---|--:|---|---|
| Lunds | 27.5% → **20.3%** | — | **none has ever existed** |
| Ouroboros | 25.0% → **18.5%** | `ouroboros_probe` | **retired** (drop-probe law) |
| Kings College Munich | 17.9% *(pending restatement)* | — | **none has ever existed** |
| CtrlAltDefeat | 11.6% *(pending)* | `cad_probe` | **disclaimed** (P6-widened) |
| Powerpuff / arsonist duck | 11.2% *(pending)* | — | none exist |
| kladde | 3.1% *(pending)* | `kladde_probe` | **invalid** (~70pt gap, composition never faithful) |

**And the two instruments that *are* valid point at opponents we beat:**
`orizon_probe` → Orizon, where we are **+4.8**; `band_probe` (rush-mode only)
→ Banminary, where we are **+78.7**.

## Why this composes with v1 rather than replacing it

v1 said the local gate has **19% power**. This says the population it measures
at 19% power contributes **~0%** of our losses. Both faults are live
simultaneously and they multiply:

> **An instrument can be perfectly powered and still uninformative if it
> measures the wrong population.** Fixing the power of a battery aimed at
> opponents we already beat buys precision about a question that does not
> decide matches.

This is a sharper answer to v2's question than "underpowered" was. v2 asked
whether the local gate predicts ladder Elo and could not answer at n=4. v5
supplies the mechanism a null would have had: the gate and the ladder are
scoring different populations.

## The finding under the finding

> **CORRECTION (author, against my own paragraph, before it reached Magnus).**
> I first wrote that the fleet "was built against the teams we were already
> beating or could most easily replicate" — a selection pathology. **That is
> false, and the probes' own provenance headers refute it.** Checked directly:
>
> - `band_probe` — 1711-rated Banminary, *"which core-killed our live bot on round 42"*
> - `kladde_probe` — 1718-rated kladde, *"which beat our live v51 by grinding it down over r381 and r284"*
> - `flotte_probe` — 1776-rated Flotte, *"which beat our live v7 on meander"*
> - `cad_probe` — *"from the 0-5 ladder sweep against team [CAD]… lost by `core_destroyed`"*
>
> Every one was replay-extracted **from a loss, against a team rated above us
> at the time.** They were built at the sharp end. My framing inverted the
> facts. (Raised by the research arm; verified here against `bots/*/main.py`.)

**The real model has two mechanisms, and only one of them is a failure**
(research arm's):

1. **Obsoleted by success** — `band_probe` was extracted from a game where
   Banminary core-killed us at round 42. We are now **+78.7 and 27-8** against
   them. The probe worked, the class got fixed, and it now points at a solved
   problem. `orizon_probe` is partly the same (+4.8). **An instrument obsoleted
   by its own effect is not a defect.**
2. **Drifted** — `cad_probe`, `kladde_probe`, `flotte_probe`. Target still
   bleeding, instrument no longer resembles it. CAD is still **−57.0** to us
   while its probe is disclaimed. This half *is* a failure.

**This inverts how the 0.0% headline should be read.** It is not an indictment
of negligence. Part of that zero is the fleet having *worked*; part is drift;
and the never-instrumented 51% (Lunds, KCM, arsonist duck) is a genuine gap
whose cause — neglect versus those teams only recently entering the bleed table
— **the archive cannot fully decide.** Research ran it; the result splits:

| never-instrumented | share | verdict |
|---|--:|---|
| Lunds + KCM | ~45% | **leans coverage, unproven** |
| arsonist duck | ~6% | **cleanly cadence** (first appears 08-08, after every probe was built) |

Lunds and KCM were already bleeding us on **08-07** — the same day
kladde/cad/orizon were extracted — at −52 and −54, comparable to CAD's −37 that
day. On the visible portion they were *contemporaneously* among the worst and
did not get instruments. **But this must not be banked:** the day-1 windows are
4-6 matches (sd ≈ 20 Elo, so those dailies are barely distinguishable), and the
decision to build kladde/cad/orizon rested on evidence from *before the archive
exists*. Lunds may simply not have surfaced in what the team was looking at.

**The structural finding is the more useful output, and it is series rule 5:**
the replay archiver was a session-12 decision, so the corpus has a hard floor
around 2026-08-07 midday. Verified independently: the oldest archived file is
7 Aug 12:31, and `band_probe`/`flotte_probe` were built 08-06 — entirely outside
the corpus. **Unlike the parser faults, this produces no wrong number.** It
answers a narrower question than the one asked, with full confidence, and will
silently truncate any future "when did X start" study the same way.

**The remedy therefore is not "name the hard target in advance"** — they did
that. It is:

> **The bleed table is the aiming spec, and it moves. Instruments need periodic
> re-aiming at the *current* table, and a probe that starts working is on a
> clock.**

Falsifiable, and it should be stated before we build anything: **if a Lunds
instrument works, it will obsolete itself for exactly the same reason — and
that will be success, not failure.** Anyone auditing the fleet later should
expect to find retired instruments and count them as wins.

What *does* survive from my original paragraph is A4, which is a separate and
still-live fault: the fleet was extracted from replays of the opponents it then
scores, and re-frozen when it drifted, so it is a holdout constructed from the
test distribution and periodically refitted to it. Blum & Hardt assumes a fixed
independent holdout. That remains true regardless of aiming quality.

## Consequence

> **CHALLENGE RAISED AND WITHDRAWN, 22:23 → 22:4x — the recommendation stands.**
> The research arm (session 20) proposed that the builder's
> `ladder-wide-census-THE-GAP` row (top tier core-kills at **97%, median 232
> turns**; we manage **72% / 28%-to-r1000**) might make a per-opponent
> instrument programme the wrong **shape** rather than the wrong order. I rated
> that as probably right and flagged it here rather than defend my own ranking.
>
> **They then ran it and their own data refuted them**, and they withdrew it
> unprompted: across 500 games (API only), **Lunds + KCM + Ouroboros +
> CtrlAltDefeat carry 49.0% of all 196 of our core-kill losses** — the same four
> names that carry the Elo bleed. **THE GAP and the per-opponent programme are
> one finding at two altitudes, not competitors.**
>
> What THE GAP legitimately changes is **the outcome variable, not the target**:
> score these instruments on **kill-game win rate**, not Elo. Room to move is
> real — Ouroboros 2/22, KCM 7/33, Lunds 11/41, CAD 9/29.

**Building a Lunds instrument outranks every plank in the queue.** 27.5% of
bleed, 0 wins in 17, and tonight's decode already names two mechanisms — so the
expensive part (decoding) is partly done.

**KCM at 17.9% is completely undecoded** — no probe, no first-read, nothing.
Highest-value blank space on the board.

**Ouroboros is different in kind:** instrument-blocked by a *measured law*
(drop-probe), not by neglect. The retired probe failed because **behavioural
fidelity did not predict outcomes** — so the replacement is not "a better
replica", it is something that captures whatever the replica missed. Calling it
"another probe" invites repeating the refuted approach, and the word choice
matters more than it looks.

Note how this interacts with A7b: we just took the deterministic opponent pool
from 1 to 6 and the det ceiling from 30 to 180 — but all six are our own
teammate lineage. **180 more observations of ourselves does nothing for a −493
bleed concentrated in four opponents we cannot instrument.** The cheap axis and
the valuable axis are different axes.

## Limits, stated by the author

Per-match Elo sd ≈ **9.25** (v3), so tail rows at n≤4 are "present", not
"measured". The top-four concentration over 57 matches is robust; the tail
ordering is not.
