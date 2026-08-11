---
tactic: Time a defensive purchase to the opponent's OBSERVED first-attack timing, and accept being caught out once as the price of not paying for it every game
source: http://satirist.org/ai/starcraft/blog/archives/981-opening-timing-data-for-Steamhammer.html
origin: RTS theory / Jay Scott (Steamhammer author), "opening timing data for Steamhammer", 2020
evidence: documented — design proposal, explicitly not yet built
transfers: partial
---

## WHAT IT IS — the only defensive-timing rule in the corpus that names its own failure and accepts it

Jay Scott's design for using recorded opponent timings contains a rule for
static defence that is unusually disciplined about cost:

> *"if we’re going to add static defense (whether written into the opening or in
> reaction to the enemy army size), then we can check records of when the enemy
> first attacked: Don’t build sunks too early."*

and, immediately, the accepted downside:

> *"If a clever enemy notices the vulnerability and attacks early, too bad, but
> then we have a new game record and will know for next time."*

**Referent check.** "sunks" are sunken colonies, Zerg static defence — the
defensive purchase. "the enemy first attacked" is drawn from data he proposes
recording per opponent: *"Also record the timing and army size and composition of
the enemy’s first attack, or maybe its first few attacks, or maybe all of its
major attacks."* So the rule is: **the defensive spend is deferred to just
before the opponent's measured attack, not held from round zero.**

The general form he states for the same data is a relative-tempo rule:

> *"One basic adaptation is to try to always be a little greedier than the enemy,
> to get ahead in economy (except when the enemy is too greedy, then we can
> rush)."*

**And this is a proposal, not a shipped result** — the post opens *"I haven’t
decided whether this is what I’ll do next, still thinking."* No outcome is
reported anywhere for it.

**Why it belongs to this sweep.** The whole corpus's window-purchase doctrine
(sweep 24: [`the-window-purchase-terminates-on-an-event-not-a-round-number`](the-window-purchase-terminates-on-an-event-not-a-round-number.md))
concerns when a defensive purchase *ends*. **This is the only span in the corpus
about when it should BEGIN, and the answer is "as late as their data allows".**
For a 13-round race that is the more valuable half: a defence bought at r0 has
spent 187 rounds of compounding cost by the time it is needed.

## WHY IT MIGHT TRANSFER — against OUR ruleset specifically

**Our numbers make this the exactly-shaped plank for the amended defence
clause.** `PLAY_DEFENCE: not_at_the_kill_s_expense` with
`DEFENCE_ADMISSION_BAR: kill_round_non_regression`, and the scope note that
*"some defence" means surviving the r150-250 window SO OUR OWN KILL LANDS* —
our median kill r174, median death r187, core dies in **46.3%** of all games.
**A defence that is bought at r0 and paid for all game fails the bar almost by
construction; a defence bought at r~165 and paid for over 20 rounds may not.**

**The engine makes deferral genuinely cheap in a way it is not in most games**,
and this is the load-bearing transfer argument:
* **Cost scale is additive and time-independent.** Waiting does not make a
  gunner dearer. A purchase deferred 150 rounds costs the *same* titanium and
  crucially avoids inflating **all** intervening builds of **every** type by
  +20% for those 150 rounds. **Deferring a +20% purchase is worth strictly more
  than the titanium it holds.**
* **Ammo has no passive income and is converted 1:1 on demand**, at most once
  per team per turn and **without using the core's action cooldown**. So a
  turret bought late is not handicapped by an empty ammo bank the way a
  late-teched unit is handicapped elsewhere — the ammo can be converted the same
  turn it is needed. **This removes the usual penalty for late defence.**

**The obstacle is that Jay Scott's data source is closed to us.** His rule reads
*"records"* accumulated across games; our sandbox freezes `time.*` and provides
no cross-match persistence, and the comms store is per-match. **So the
per-opponent form is not buildable.** What remains is the *within-match* form:
defer the defensive purchase until a signal in this game says the attack is
coming.

**EFFECT ON MEDIAN KILL ROUND: PREDICTED EARLIER OR FLAT, and that is the point
of the file.** This does not add defence; it moves defence we already buy from
early to late, releasing early titanium and early scale to the raid. It is the
one shape in which a defensive plank can plausibly *improve* the kill round
rather than merely avoid regressing it — and s30's measurement that
`home-turrets-off` scored 433/1024 and `barrier-seal-off` 399/1024 (both real
negatives, i.e. removing defence COST us) says the defence itself should be
kept, which is precisely the premise this plank needs.

## WHAT WOULD KILL IT

* **The trigger has to fire before the attack lands, and our vision is short.**
  A core sees r²=36 and a builder r²=20. If the first observable of an incoming
  attack arrives *at* the core rather than in front of it, "defer until we see
  it" degenerates into "defer until it is too late", and the deferral is a
  strict loss. **This is the falsifier and it should be checked on the corpus
  before any code is written**: how many rounds of warning does our incumbent
  actually get before a core-damaging attack?
* **No cross-match memory** — the per-opponent version is closed by
  construction, so only the weaker within-match version is available.
* **`can_fire` returns TRUE at 0 ammo** and the check that raises lives in
  `finish_firing_turret`, destroying our own turret. A defence bought late and
  fired before the conversion lands is not a slow defence, it is a **dead**
  one. Any late-purchase plank must convert ammo in the same turn it commits.
* It is a design note with no reported outcome. Weakest evidence class in the
  sweep for the *result*; the *reasoning* is what transfers.

## BUILDER HOOK — smallest thing that would test it

**Measure the warning window first — it is a corpus cut and it can close the
road for free.** Over our own replays, for games where our core took damage,
compute the distribution of rounds between the first round an enemy unit
entered our core's vision and the first round our core took damage. **If the median warning is
under the build-plus-convert latency, this plank is dead and costs nothing to
kill.**

If the window is adequate: the incumbent already carries a `SLOT_UNDER`
under-attack latch and home-turret logic (`doctrine.py:680` records home turrets
as `_try_counterbattery`'s *"exclusive capability"*), so **no new store slot is
needed** — the 16 are fully bound (`doctrine.py:931-961`, `:1166-1170`). The
change is to gate the *purchase* on that existing latch rather than on a round
number or an unconditional opening, and to pair it with a same-turn
`convert_ammo`. Pre-register **median kill round** as the primary and core
survival as the secondary, in that order, per the admission bar.
