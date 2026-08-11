---
tactic: MEASURED NEGATIVE — the tempo/robustness trade at the margin has never been measured in this field; the vocabulary to state it barely exists
source: 65 primary documents / 222,488 words (22 Battlecode postmortems 2019-2026, XSquare guide, 13 Jay Scott posts, 6 Halite II/III postmortems, 4 CodinGame postmortems, Screeps/Terminal/RTS theory)
origin: sweep 25 term census, 2026-08-11
evidence: documented
transfers: no
---

## WHAT IT IS — arm B's second answer, and it is a hard negative

Sweep 24 established that **nobody in the field has ever measured the kill
round** ([`nobody-in-the-field-has-ever-measured-the-kill-round`](nobody-in-the-field-has-ever-measured-the-kill-round.md)),
on 41 documents / 166,155 words. Sweep 25 re-ran that census on a corpus **58%
larger** and asked the sharper question: not "did anyone measure duration" but
**"did anyone measure the TRADE — what a robustness purchase cost in arrival
time"?**

**Census over 65 files / 222,488 words. Literal `grep -F`, case-insensitive:**

| phrasing | hits |
|---|---:|
| `kill round`, `kill time`, `time to win`, `rounds to win`, `turns to win` | **0** |
| `game length`, `how long the game`, `shorter game`, `average game`, `median round` | **0** |
| `won faster`, `win faster`, `faster win`, `ended sooner` | **0** |
| `tempo cost`, `cost in tempo`, `tempo gain`, `traded tempo`, `tempo versus`, `tempo vs` | **0** |
| `speed versus`, `speed vs safety` | **0** |
| `delayed our attack`, `delay our attack`, `delay the attack`, `slowed our attack`, `slow our attack`, `delaying the attack` | **0** |
| `game duration` | 1 |

**The single `game duration` hit is not a counterexample and must not be quoted
as one.** It is CodinGame Fall 2020 / pb4, describing a *simulation horizon*:
> *"Play 22 turns (typical mid- and end-game duration in a normal game) and
> record the number of points gathered by the player."*
That is the length of a rollout inside a search, not a measured outcome of a
shipped change. Reported here because an unexplained "1" in a table of zeros
invites exactly the reconstruction this library keeps having to correct.

**And the negative has a positive edge that locates the whole finding.** Only
four spans in the entire corpus treat *delay* as a quantity to be protected:

| phrasing | hits | where |
|---|---:|---|
| `critical path` | 1 | `jayscott-fastlurker-1` |
| `no delay` | 1 | `jayscott-fastlurker-1` |
| `without delaying` | 2 | `jayscott-fastlurker-1`, `jayscott-fastlurker-3` |

**All four are one author, in one three-post series, about one build order** —
and that series is the subject of
[`buy-the-escort-out-of-income-not-off-the-critical-path`](buy-the-escort-out-of-income-not-off-the-critical-path.md).
Outside it, no document in the field contains a sentence in which adding a
defensive or supporting unit is priced in time.

**Meanwhile the field measures constantly.** `scrim` 120 · `tested` 28 ·
`winrate` 20 · `win rate` 11 · `AB test` 7. A/B testing is routine and
well-instrumented (BC2025 Just Woke Up ran an automated all-map harness). **The
outcome variable is always the win rate.** So this is not a field that lacks
measurement discipline — it is a field in which *arrival time was never a
dependent variable*, because in every one of these games the win condition is
either a score at a fixed horizon or a kill with no deadline attached to it.

## WHY IT DOES NOT TRANSFER

There is nothing to port. **No constant, no threshold, no exchange rate, and no
worked example of the trade exists anywhere in the corpus.** Filed as
`transfers: no` under the index rule that a recorded negative stops the next
session chasing it.

Its practical value is a warning about our own instruments, and it is the same
warning sweep 24 issued with one more turn of the screw: **`PROGRAMME.md`'s
`DEFENCE_ADMISSION_BAR: kill_round_non_regression` is a bar this field has never
run, on a quantity this field has never recorded.** Every number we will produce
against it is ours alone, on our own denominators, with no external calibration
available at any price. Sweep 24's corollary stands unchanged and applies here
verbatim: a kill-round bar read on `bots/*_probe` inherits the fixture defect,
because a probe we wrote does not intercept the way the ladder does.

**EFFECT ON MEDIAN KILL ROUND: none — this file proposes no change.**

## WHAT WOULD KILL IT

* A postmortem outside this corpus that reports time-to-win as an outcome. The
  most likely home is a league whose win condition carries an explicit deadline
  (our own `KILL_WINDOW_RND: 250` shape). **Liquipedia's `Timing Attack` and
  `All-in` articles were NOT read** — the fetch was blocked by a Cloudflare
  rate limit whose own page instructed automated agents to stop, and the
  download agent complied. **That is a real hole in this census and it sits
  exactly where a counterexample would live.** Anyone re-running arm B should
  get those two articles by hand first.
* Released source rather than prose: a bot whose config exposes a tuned
  attack-timing constant is evidence of the trade even if no postmortem discusses
  it. This census read documents, not repositories.

## BUILDER HOOK

None — this is a closure, not a plank. **It does have one instrument
consequence:** since no external calibration exists, the kill-round bar needs
its estimator named in the pre-registration *before* the leg
(median vs mean vs share-inside-r250 will not agree), or it can be met and
missed by choosing one afterwards. That is the index's own standing lesson from
sweep 22's magnitude spread, arriving in a new place.
