# ACTIVE PROGRAMME — machine-readable. `tools/gate.py` reads this and refuses off-programme batteries.

Edit this file ONLY on an explicit directive from Magnus. Both arms and every
successor session inherit it. The fields below are parsed; the prose is not.

    LINE: loki
    LINE_DIRS: bots/_v105loki1 bots/_v10?loki* bots/_v1??loki*
    INCUMBENT: bots/_v115dodge
    INCUMBENT_FROZEN: yes
    PRIMARY_CURRENCY: core_kill_share
    SECONDARY_CURRENCY: time_to_core_kill
    WIN_RATE_IS_VERDICT: no
    COMPARE_AGAINST: previous_line_iteration
    KILL_WINDOW_RND: 250

## What this means, in the words of the directive (Magnus, 2026-08-09)

> *"Loki should be our main focus now, leave Eir behind to hold the lines while
> we build something that has a shot at actually ranking high."*
> *"Eir is what, iteration 50+, Loki v1 was never supposed to be shippable...
> we need a lot of iterations to make Loki stand a chance."*
> *"Although Loki is supposed to be an entirely separate bot from Eir."*
> *"We need to find good tricks we can use, poisonings, exploits, manipulations,
> anything that seems to have a shot at killing teams in the first 250 rounds,
> and lean into that hard once we find it."*

**INCUMBENT_FROZEN** — `bots/_v115dodge` (v92) holds the ladder slot and receives
no further planks. It defends the rating; it is not the work.

**LINE: loki** — Loki is a SEPARATE BOT, not a flag on the Eir chassis. Iterations
edit Loki's own tree. Porting Loki features onto Eir is the line-mixing this
directive forbids; `bots/_v116thor` is the last instance and is retired.

**COMPARE_AGAINST: previous_line_iteration** — LOKI-N is measured against
LOKI-(N-1), never against Eir. "Does it beat the incumbent" is the wrong
instrument for a line under development and is what buried LOKI-1 in s22: a v1
was judged against a v46+ line, on a self-play pool, and the road was closed on
the result.

**WIN_RATE_IS_VERDICT: no** — the probe pool is dominated (both arms win 87-90%),
so a win-rate ceiling that high cannot show an edge. Read
**core-kill share** and **time-to-core-kill**. Measured 2026-08-09: LOKI-1 vs v92
was a win-rate NULL (+3.1pp, p=0.22) and a core-kill landslide (91% vs 61% share,
paired sign test p=5.2e-09).

**KILL_WINDOW_RND: 250** — the target is a dead enemy core inside 250 rounds.
Our own tape: before r200 we go 277-148 (65.2%); after r200, 164-363 (31.1%).

## Exit conditions — the only things that end this programme

1. Magnus says so.
2. The Loki curve crosses Eir on the primary currency AND survives a ladder read.

A Loki iteration that measures null does NOT end the programme. That is what an
iteration is.
