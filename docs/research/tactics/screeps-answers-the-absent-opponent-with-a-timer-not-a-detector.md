---
tactic: (A/B) The one league where a passive opponent PERSISTS handles it with an engine timer, not with bot-side detection — and its players say the timer is for absentees, not for attacks
source: https://docs.screeps.com/control.html
origin: Screeps (persistent MMO strategy sandbox); official docs `control.html` and `cpu-limit.html`, the community wiki (wiki.screepspl.us/CPU/), and the official forum PvP discussion thread 473
evidence: documented
transfers: partial
---

WHAT IT IS — Screeps is the only surveyed league structurally like ours on this question:
**a failed or absent player is not ejected, frozen or scored out. Their colony just sits
there and the world keeps running.** It is also the only one where "the opponent is not
acting" is a routine, discussed condition — because the players are humans who go away:

> forum, PvP game discussion: *"A lot of Screeps players only check their colonies once a week."*

**And the league's answer is an engine timer, not a detector.** A controller that is not
upgraded decays, and the docs state the terminal condition:

> *"As soon as its level reaches 0, a Controller becomes neutral, and another player can reclaim it."*

The docs also expose an action that accelerates it — *"You can attack another player's
controller downgrade timer by applying attackController on it."* (the source renders the
apostrophe as `&#39;`). **A player in the same forum thread states the doctrine plainly,
and it is the sentence that matters most here:**

> *"Downgrade is good for inactive players, not for attacking."*

*(Referent: "downgrade" is the controller-downgrade mechanic under discussion in that
thread, and the speaker is contrasting it with an alternative "block counter" proposal for
contested rooms. The claim is that the decay mechanic is how the game reclaims ABSENTEE
territory, and that it is the wrong instrument for beating an opponent who is present.)*

**The bot-side failure mode is documented too, and it is a soft one** — Screeps meters CPU
with a bucket:

> official docs: *"after 100 ms execution of your script will be terminated even if it has not accomplished some work yet."*

> community wiki: *"If the bucket reaches 0, and CPU usage is above limits, script execution halts."*

**Halts for that tick.** Creeps do not die; they stand still. So a CPU-starved Screeps
player looks, from the outside, exactly like an absent one.

**What this sweep did NOT find, having looked:** no Screeps doc, wiki page or forum thread
was located in which a bot algorithmically *detects* that an opposing player is
out-of-CPU, crashed or offline and changes plan on it. The condition is discussed by
humans; the response is human. **Absence of evidence after a targeted search — recorded as
such, not as proof.**

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **The structural match is real and it is the reason to file this.** Ours is the other
  engine where failure persists without adjudication, and Screeps' answer — *let a timer
  claim what nobody is defending* — has a direct analogue: **an enemy area that stops being
  contested becomes ours to build in, and we do not have to prove why.** That is
  on-programme when it means planting forward and pressing the core faster.
- **The negative half is the more useful half.** A league that has lived with absent
  opponents for a decade never built the detector. Its most experienced players say the
  mechanic that handles absentees is *"not for attacking"* — i.e. **the absentee case and
  the combat case were deliberately kept apart.** For us that is an argument that a
  "the enemy has gone quiet" branch should change what we BUILD (claim the space), not what
  we FIGHT (commit the army), because the first is safe when the diagnosis is wrong and the
  second is not.
- **The CPU-starvation signature is the same shape as ours.** Screeps' halt is per-tick and
  recoverable, exactly like our 10 ms discard. **In both engines, "did nothing this turn"
  is a weak, non-absorbing signal** and needs many observations before it means anything —
  unlike our exception failure, which is absorbing and needs one.

WHAT WOULD KILL IT —

- **The analogy leaks at the most important joint: in Screeps the absent thing is a HUMAN,
  and the bot keeps running.** A "once a week" player still has creeps harvesting and
  towers firing. That is not our failure state at all. **Anyone importing "the opponent is
  asleep" from Screeps is importing a condition our engine cannot produce.**
- **Persistence changes the economics completely.** Screeps rooms are held for weeks and
  the downgrade timers run to 150,000 ticks at RCL 8. We have 1000 rounds and want the core
  dead by 250. **A decay-timer doctrine has no room to operate on our clock**, so only the
  qualitative lesson (claim space, do not commit force) survives the transfer.
- **The forum quotes are individual players in a design argument, not organisers.**
  The thread is a proposal discussion; the *"not for attacking"* line is one competitor's
  position, contested in the same thread.

BUILDER HOOK — none as a plank; **one framing to carry into any future detector spec:**
if we ever branch on "the enemy appears to have stopped", the branch should be a BUILD
decision (take the contested tile, extend the plant, run the route through space they have
stopped contesting) and never a commit-the-force decision. **That way a false positive
costs titanium and a builder-turn, not the push** — which is the failure mode
[`the-crash-win-contaminates-your-measurement-of-the-opponent`](the-crash-win-contaminates-your-measurement-of-the-opponent.md)
says we are most likely to hit.

Related: [`every-other-league-resolves-the-failure-and-ours-does-not`](every-other-league-resolves-the-failure-and-ours-does-not.md) ·
[`retake-the-vacated-tile`](retake-the-vacated-tile.md) ·
[`turtling-persists-because-nobody-punishes-it`](turtling-persists-because-nobody-punishes-it.md)
