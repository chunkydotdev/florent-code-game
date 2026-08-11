---
tactic: Three independent teams REMOVED or weakened their withdrawal rule and reported it as an improvement — the falsifier arm came back loaded
source: https://battlecode.org/assets/files/postmortem-2025-spaark.pdf
origin: Battlecode 2025 SPAARK and The Kragle; Battlecode 2023 don't @ me
evidence: documented
transfers: partial
---

## WHAT IT IS

The brief for this sweep warned that finding only leave-faster material would
mean the sweep had not been run hard enough. **The opposite happened: the
strongest measured statements in the whole sweep run the other way.**

**1. SPAARK (BC2025) made retreating harder and reported a large win.** In their
list of late changes:

> *"Don't retreat unless you are close to the tower"*
> *"Surprisingly, this won against old bots by a very large margin"*

**Referent check.** This is item 3, and the second line is its sub-point (a),
under a heading reading *"Some small last-minute optimizations we did:"*. "the
tower" is the paint tower a robot retreats to for refill. **The term `old bots`
is not defined in the source** — the surrounding paragraph compares the current build
against the team's own earlier bot (*"Initially, it had a meager 25% winrate
against SPAARK"*), so I read it as a **self-play A/B**. That reading is mine, not
the source's. If it is right, this library holds that self-play inflates effects ~2x
([`self-play-inflates-the-effect-by-about-2x`](self-play-inflates-the-effect-by-about-2x.md))
and has the wrong population
([`self-play-ab-has-the-wrong-population`](self-play-ab-has-the-wrong-population.md)).
The direction survives that discount; **the magnitude ("very large margin") does
not travel.** The same list also loosens the *other* side —
*"Bots refill if they pass by a tower that has paint in it, even if they are
almost full"* — i.e. **refuel opportunistically en route, never as an errand.**

**2. The Kragle (BC2025) discovered the whole round-trip was optional by watching
other teams.**

> *"Our robots would spend about half of their lifetime traveling back to towers and waiting around towers for paint."*
> *"no other team bothered having their bots refill on paint"*
> *"It cuts down on robot idle time, and allows robots to perform longer tasks at the cost of chips. You would only really want to preserve high-value robots, which was just the splashers."*

**Referent check.** "It" is the change of not refilling — the preceding sentence
reads *"This was such an obvious improvement:"*. The trade is stated explicitly:
**pay currency to replace the unit rather than pay TIME to preserve it**, and the
exception is named — only high-value units are worth preserving.

**⛔ AND THE CAVEAT IS IN THE VERY NEXT SENTENCE, WHICH MUST TRAVEL WITH THE
QUOTE:** *"This change came way too late in the competition and was a stark
reminder to pay careful attention to other team's strategies."* **So the Kragle
did NOT measure this change in their results — it is a field observation about
what every other team was doing plus an argument, not an ablation.** The
load-bearing evidence in item 2 is therefore *"no other team bothered having
their bots refill on paint"* — a **census of the field**, which is the stronger
half anyway and does not depend on the Kragle's own outcome.

**3. don't @ me (BC2023) considered a withdrawal-to-heal rule and cut it.**

> *"we decided that the value we were getting from the island heal was too low and we would rather have the map presence that the launcher presente, even if it was low health."*

(They later reinstated it *after the organisers buffed healing values* — the
decision tracked the exchange rate, not a doctrine. That reversal is the honest
caveat and it is quoted in
[`the-withdrawal-predicate-needs-a-destination-clause`](the-withdrawal-predicate-needs-a-destination-clause.md).)

## WHY IT MIGHT TRANSFER

The Kragle's arithmetic is the one that ports, and it ports **harder for us than
for them**, because our replacement cost is unusually visible:

* A builder bot is **30 Ti base**, and the core spawns **at most one per turn**.
  So the price of "let it die and rebuild" is 30 Ti *and one core action*, not
  30 Ti.
* **But destruction refunds the scale contribution.** A builder bot is a **+20%**
  entity on the single global additive factor, so a dead raider makes *every*
  subsequent build of *every* type cheaper. Preserving a raider is, in scale
  terms, **paying to keep our own prices high** — the exact inversion this repo
  already recorded for enemy demolition
  (`../engine-guard-matrix-exploit-hunt-2026-08-10.md`).
* `MAX_TEAM_UNITS = 50` is the counter-argument only when we are actually at the
  cap.

**Under `R1000_IS_DEFEAT` and `PLAY_DEFENCE: never`, "preserve the raider" needs
an affirmative case and it does not have one.**

## WHAT WOULD KILL IT

* **All three are Battlecode-2025-era paint economies or a healing meta.** The
  Kragle's trade is *chips for turns*; ours would be *titanium and a core spawn
  for turns*, and the core spawn is a genuinely scarcer good than chips were.
* **SPAARK's "very large margin" is self-play.** Do not quote it as a field
  result.
* The Kragle finished ~27th at the US Qualifier by their own account; SPAARK's
  quoted change is undated relative to their final placing. **Neither is a
  champion's ablation**, and the library's strongest precedent for a real one
  (Stone & Veloso 1999) is in the opposite domain.

## BUILDER HOOK

The cheap version is a **deletion, not a feature**: remove the raider's
return-home arm entirely for one leg and let raiders die forward, then read
forward structures placed per builder spawned. **Pre-register the falsifier:
builders lost per forward build is EXPECTED to rise — the plank fails only if
forward structures per core-spawn does not.**

## ⛔ CAVEAT APPENDED 2026-08-11 (s32, research arm) — THIS FILE REASONS ON A RETIRED PROGRAMME FIELD
This file cites **`PLAY_DEFENCE: never`**. That field was amended the same day and now reads
**`PLAY_DEFENCE: not_at_the_kill_s_expense`** with **`DEFENCE_ADMISSION_BAR: kill_round_non_regression`**
(`PROGRAMME.md:19-20`). **A defensive tactic is now ADMISSIBLE IFF it does not slow the kill** — it carries a
kill-round non-regression bar beside its survival bar, and is off-programme only if MEDIAN KILL ROUND RISES.
**"Defensive, therefore off-programme" is no longer a valid closure reason.**
**Scope, unchanged:** this licenses surviving the **r150-250 window so our own kill lands** (median kill 174,
median death 187, core dies in 46.3% of games). It does **NOT** license surviving to r1000 —
**`R1000_IS_DEFEAT: yes` still governs.**
**WHAT THIS DOES AND DOES NOT DO TO THIS FILE:** Line 83 — "Under `R1000_IS_DEFEAT` and
`PLAY_DEFENCE: never`, 'preserve the raider' needs an affirmative case and it does not have
one." — is the file's stated reason, in its WHY IT MIGHT TRANSFER section, for treating "delete
the raider's return-home arm entirely" as having no real counter-argument. `R1000_IS_DEFEAT` is
unchanged and still applies. But `PLAY_DEFENCE: never` is retired, and "preserve the raider" now
DOES have a possible affirmative case: `DEFENCE_ADMISSION_BAR` admits a survival move that does
not raise median kill round. This is the clearest case in this batch where voiding the premise
removes the file's stated justification for its own BUILDER HOOK. The pre-registered falsifier
in that hook ("builders lost per forward build is EXPECTED to rise — the plank fails only if
forward structures per core-spawn does not") is itself unaffected and remains a correct test,
but any leg run on it should now also check kill-round non-regression, since "preserve the
raider" is a live alternative rather than a foreclosed one.
**STATUS:** CLOSURE VOIDED — the stated reason for foreclosing "preserve the raider" as a
counter-argument is retired; the road returns to the queue for a live test, and any future leg
on this file's plank should carry a kill-round check alongside its forward-structures-per-spawn
falsifier.
**NOT REOPENED BY THIS CAVEAT.** Voiding a closure reason does not revive the road; it returns it to the queue
for a live test. Under `docs/research/PROGRAMME-drift-watch-2026-08-09.md` D12 an archive-sourced closure cannot
retire a road, and this caveat cannot restore one.
