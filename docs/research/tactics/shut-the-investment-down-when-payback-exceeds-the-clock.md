---
tactic: SHUT THE INVESTMENT DOWN WHEN ITS PAYBACK PERIOD EXCEEDS THE REMAINING CLOCK — a hard economic off-switch on a turn number, derived from payback arithmetic rather than chosen
source: https://www.kaggle.com/competitions/lux-ai-season-2/writeups/philipp-kostuch-some-notes-on-a-pure-logic-approac
origin: Lux AI Challenge Season 2 (2023) / Philipp Kostuch, 6th place, pure-logic bot
evidence: documented
transfers: yes
---
⚠ **TIER 2.** Read through a text proxy, **not diffed against Kaggle's original
HTML**. The string verifies verbatim against the local bytes.

WHAT IT IS — A 6th-place bot switches off an entire production line at a fixed turn,
and states the arithmetic that produced the number:

> *"Ore production shuts down at 650 (as payback is 250 turns and I want max available power at 850 when the main attack starts)"*

Three things are in that parenthesis and all three matter.

**The number is derived, not tuned.** 650 = 900 − 250, where 250 is the payback period
of the investment and ~900 is the effective horizon. He is not guessing a good turn to
stop; he is refusing every investment that cannot return before the game ends.

**It is a clock used as a DISARM trigger, not an ARM trigger.** This is precisely the
distinction 17A extracted when it falsified sweep 15's "no winning bot branches on a
round number": *a clock is a poor ARMING trigger and a good DEADLINE/DISARM trigger.*
Philipp's clock does not start an attack; it stops a habit that has no natural exit.
That is a **fourth independent instance** of the corrected rule, and it is the cleanest
one in the library because the author shows his working.

**The freed resource is retargeted, not banked** — *"I want max available power at 850
when the main attack starts"*. The shutdown exists to fund the attack. An off-switch
with no downstream consumer is just hoarding.

WHY IT MIGHT TRANSFER — This is the most directly buildable item in the Lux haul, and
it is buildable because it needs no new sensing, no opponent model and no map
analysis — only `get_current_round()`, the cost getters, and arithmetic we can do
offline.

Our economic investments have computable payback periods:

- A **harvester** costs `get_harvester_cost()` and emits a 10-stack every 4 rounds,
  plus transport latency down the conveyor line. Its payback is short — but the
  denominator is the *scaled* cost, and our scale is **ONE GLOBAL ADDITIVE FACTOR that
  every build feeds**, so late harvesters are dear in a way base costs hide.
- A **conveyor** at 3 Ti base pays back only via the stacks that traverse it, so a line
  extension's payback is the marginal delivery rate it unlocks times the rounds
  remaining.

**And our horizon is unusually well defined**: 1000 rounds, fixed, known to every unit
via `get_current_round()`. Philipp had to estimate his effective horizon. We do not.

The library's standing complaint is the exact failure this rule fixes. **We bank and
do not spend**; we *"end r200-300 holding more titanium than Ouroboros while buying a
twelfth as much ammunition"*; and our economy *"is not our constraint at all"* (sweep
8). A bot that keeps buying economy past the point where economy can return is
converting titanium into a number that no longer compounds. **A payback gate is the
principled version of the "stop building conveyors" instinct** — it names the round on
which each category stops being worth buying, and it names it from arithmetic rather
than from a vibe.

The interaction with our tiebreak keys is favourable and worth stating. Key 1 is
`most titanium collected` and is **cumulative**, so a harvester built at r900 still
contributes ~25 stacks to key 1 before the horizon — the payback gate for *key-1
purposes* is later than the gate for *capability* purposes. Those are two different
gates with two different numbers, and conflating them is the obvious way to build this
wrong.

WHAT WOULD KILL IT — Four things, in descending order of likelihood:

1. **Our payback periods may be so short that the gate never binds.** A harvester
   returning 10 Ti every 4 rounds pays back a ~20-40 Ti cost in tens of rounds, not
   250. If every category's payback is under 50 rounds, the gate fires at r950 and
   changes nothing. **This is a spreadsheet question and should be answered before any
   code is written.** Sweep 8 already found that cost scaling *"never binds on
   harvesters"*, which is evidence in this direction.
2. **The freed titanium needs a consumer.** Philipp's shutdown funded an attack. If we
   shut down economy and the titanium sits in the bank, we have made key 3 larger and
   nothing else — and the library's measured problem is that we already do that.
   **This tactic is worthless without a spending plan and actively harmful with a bad
   one.**
3. **Key 1 is cumulative**, so the naive gate — stop buying economy at round X — has a
   direct cost in the tiebreak we currently win 57.2% of. The gate must be computed
   against key-1 contribution, not against capability, or it trades our best road away.
4. It is one competitor's design at 6th place, with no ablation and no measurement of
   what the rule was worth.

BUILDER HOOK — Offline first, and it is genuinely small: **compute the payback period
of each buildable category at realistic mid-game scale values, and plot the round after
which each stops returning before r1000** — once for capability and once for key-1
contribution. If any category's capability gate lands before r800, that is a live
purchase rule with a derived constant and a named consumer. If they all land after
r950, this file is a `no` and one line in the summary records why nobody should look
again.
