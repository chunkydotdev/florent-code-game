---
tactic: (A) The only league that PUBLISHES the failure signature — Battlesnake documents exactly what a timed-out bot does next, which makes the failed opponent's move deterministically knowable
source: https://raw.githubusercontent.com/BattlesnakeOfficial/docs/main/docs/api/01-introduction.md
origin: Battlesnake official API documentation (`BattlesnakeOfficial/docs`, branch `main`), section "Response Error Handling"
evidence: documented
transfers: no — our engine emits no substitute action, so there is no analogous signature. Filed with what would change that.
---

WHAT IT IS — Battlesnake is the one surveyed league that not only tolerates a failed bot
mid-game but **specifies, in the public API docs, exactly what the engine will do on its
behalf**:

> *"Any invalid responses will be treated as errors by the game engine, and your Battlesnake's next move will be chosen for you - even if that means certain elimination."*

> *"**An error on the first move of a game** will move your Battlesnake `up` by default. This value is hardcoded into the game engine with no particular meaning behind it."*

> *"**Errors on subsequent turns** will repeat your previous move. For example, if your Battlesnake successfully moves `right` on turn N, a timeout on turn N+1 will result in your Battlesnake moving `right` again. This applies even if the game engine chose your move for you on the previous turn due to an error."*

*(Bold and backticks are the source's markdown, preserved. The three sentences are
consecutive in the "Response Error Handling" section; "your Battlesnake" in the docs
addresses the reader's own bot, but the rule is symmetric and describes every bot in the
game, which is what makes it an opponent-side observable.)*

**What that gives a competitor, in principle:** a timed-out opponent is a snake moving in a
fixed direction, and the *third* sentence makes the state absorbing — an errored turn does
not reset the reference move, so a snake that fails once and keeps failing walks in a
straight line until it dies. **The failed opponent is not merely detectable, it is exactly
predictable**, and the docs say the engine will drive it into *"certain elimination"*
without help from anyone.

**But note what this sweep did NOT find.** No Battlesnake competitor writeup was located
that says they built a detector on this, measured a gain from it, or changed behaviour on
it. **The rule is documented; its exploitation is not.** Treat the second half as absent
evidence, not as a claim.

WHY IT MIGHT TRANSFER — against OUR ruleset, honestly: **it does not, and the reason is
worth writing down because it is the cleanest statement of our own engine's shape.**

- **Battlesnake substitutes an action; our engine substitutes nothing.** A unit whose
  `run()` raises is destroyed outright, and a unit that exceeds 10 ms simply has that turn
  discarded — no default move, no repeat, no facing change. **There is no engine-authored
  behaviour to recognise.** The signature that exists here is *absence*, not *repetition*.
- **Our closest analogue is weaker in exactly the way that matters.** A hung enemy builder
  looks like a builder standing still — which is also what a builder on cooldown, a builder
  waiting for titanium, and a builder deliberately holding a tile look like. Battlesnake's
  signature is unambiguous because the engine authored it; ours would be a guess about
  someone else's policy.
- **One thing does carry over: the ABSORBING property is the valuable part, not the
  direction.** Battlesnake's rule is exploitable because the failure state never
  self-corrects. **Our exception failure has the same property and is stronger** — the unit
  is gone for the whole match, so a detector that fires once never needs to re-check. A
  detector built on our CPU-overrun failure would have the opposite property (the unit is
  fine next round) and would need re-confirmation every time.

WHAT WOULD KILL IT — it is already `transfers: no`; here is what would change that:

- **An engine probe showing our engine takes ANY default action on behalf of a unit whose
  turn was discarded or whose `run()` raised.** Our reference says it does not, and our own
  probe (`bots/_probe_oov_raw`, cited in the library) measured units disappearing rather
  than defaulting. **If a probe found a default facing, a retained order, or any residual
  behaviour, this file flips from `no` to `partial` immediately.**
- **A Battlesnake competitor writeup that actually exploits the repeat rule.** That would
  turn the exploitation half from absent to documented and would tell us what the gain
  looks like when the signature IS clean — a useful upper bound on ours.

BUILDER HOOK — none as a plank. **One probe, and it is cheap:** in an unrated leg, have a
single expendable builder deliberately raise inside `run()` on a chosen round and log, from
another unit's vision, what the engine reports at that tile on the following rounds — id
present or absent, any residual facing, any action. That settles whether our failure state
has *any* observable other than absence, which is the premise every detector in this sweep
would rest on. **Pre-register it (bar + falsifier) before the leg, per the iteration mill.**

Related: [`every-other-league-resolves-the-failure-and-ours-does-not`](every-other-league-resolves-the-failure-and-ours-does-not.md) ·
[`remembered-and-checked-gone-is-a-third-value`](remembered-and-checked-gone-is-a-third-value.md) ·
[`the-stuck-counter-is-the-universal-primitive`](the-stuck-counter-is-the-universal-primitive.md)
