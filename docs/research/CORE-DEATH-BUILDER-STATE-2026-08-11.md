# ⭐ WHEN OUR CORE DIES, OUR BUILDERS ARE ALIVE AND AT HOME — THE "SURVIVAL PLANK IN OFFENSIVE CLOTHING" THESIS FAILS

**Research arm, s31, 2026-08-11.** Commissioned by the side lane, who reconciled
three facts into a hypothesis and **explicitly pre-registered both branches** and
asked not to be measured inside their own frame.

**THE HYPOTHESIS (theirs, labelled by them as hypothesis-only):** we out-kill every
band — median kill round 174 vs 205 above us — but die 24 rounds earlier than the
band above (187 vs 211), and 98.3% of our losses are core-destroyed. **⇒ "We may
die at 187 because the units that would have been home are already thrown away
forward."**

**THEIR PRE-REGISTERED DISCRIMINATOR:** *"when our core dies at ~187, where were our
builders at 150–187, and how many were alive? If forward and dead, the thesis
holds. If home and alive, the thesis is wrong and forward efficiency costs us
nothing on the currency."*

## THE MEASUREMENT

Population: **our 4,504 archived games with exactly one core death.** Instrument:
`corpus/events.tsv`, builder `BUILD`/`DEATH`, with the `d2_enemy < d2_own` flag
taken on the death row. Side keyed on `teamAId`/`teamBId`.

| | LOSS (our core destroyed) | WIN (their core destroyed) |
|---|---:|---:|
| games | 2,304 | 2,200 |
| decisive round T, median | 201 | 165 |
| **OUR builders ALIVE at T−1, median** | **5.0** | **5.0** |
| OUR builders alive at T−1, mean | **4.43** | **5.20** |
| our builder deaths in [T−40, T), mean | **0.38** | 0.24 |
| of those, FORWARD | 16.8% | 56.4% |

## ⇒ THE CLEAN RESULT: THE BUILDERS ARE NOT ABSENT

**The thesis requires them to be GONE. They are standing there** — median 5 alive,
mean 4.43, against 5.20 in wins, a difference of **0.78 builders**. And they are
barely dying in the run-up: **0.38 builder deaths across the entire 40 rounds
before our core falls.**

**⇒ On the side lane's own pre-registered branch: THE THESIS IS WRONG, and forward
efficiency is a real inefficiency that costs us nothing on the currency.**

**The one bias in the comparison runs IN FAVOUR of the thesis and it still fails.**
Losses run later (median T 201 vs 165), giving more rounds to accumulate builders,
which should inflate the loss-side alive count relative to wins. It does not rescue it.

## ⛔ THE CONFOUNDED HALF — STRUCK, NOT USED

**The 16.8% vs 56.4% forward-death split is close to TAUTOLOGICAL** and must not be
quoted as evidence. In games we lose the fighting is at our base, so deaths are at
home; in games we win it is at theirs, so deaths are forward. **It mostly restates
who was winning.**

**Its one legitimate use is as the built-in control:** a 39.6pp swing in the
expected direction proves the instrument **discriminates** rather than returning a
constant column — this cut can produce the other verdict.

## WHAT THIS DOES NOT SETTLE

* **"Alive but forward and unable to return" is NOT excluded.** This cut measures
  that the builders *existed*, not *where they stood*. The surviving route for the
  thesis is per-round positions (the dwell decoder, ~20 min). **Unrun, offered.**
* The forward-share rows use only games with ≥1 builder death in the window
  (567 loss / 391 win) — a selected subset. **The alive-count uses all 4,504 and
  is the load-bearing number.**
* **No causal claim.** *(INFERENCE is not even reached here: this is a refutation of
  a stated precondition, not an account of why our core dies.)*

## HOW IT SITS WITH THE REST OF THE s31 BOARD

`QUEUE-forward-efficiency-2026-08-11.md` (as corrected): forward hazard is a **flat
~3.5× multiplier in every round band**, and **tile exposure explains at most 1.53×
of 3.47×.**

**⇒ Forward losses are real, constant across the game, and — on this cut — not what
kills our core.** The ~2.3× of hazard unexplained by where we stand remains the
open question, and it is not answered by this document.

## METHOD NOTE — WHY THE FRAME DISCIPLINE MATTERED

The side lane asked not to hand a frame that then gets measured inside. **This cut
tested whether builders were ABSENT — the mechanism's actual requirement — rather
than whether forward play CORRELATES with losing.** The latter is what the data
answers most eagerly, in the thesis's favour, and it means nothing. **The
tautological 39.6pp split is precisely what would have been published had the frame
been taken.**
