---
tactic: A failed push is not a zero — it is priced by the RESIDUE it leaves in the defender's base, which keeps costing them after the attacker is dead
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: Battlecode 2020 / confused (2nd place, high-school bracket)
evidence: documented
transfers: partial — ⚠ WE ALREADY SHIP THE PLANK; the value here is the PRICING and a correction
---

## WHAT IT IS — arm D, answered from the attacker's side

Arm D asked what it cost, elsewhere, to have an attack stopped. **confused
report the opposite sign: for the attacker, a stopped attack was still paid.**
Describing why rush was strong in BC2020, in a passage about defending against
it:

> *"This was another advantage of Battlecode 2020 Postmortem 15 rush: even if the
> rush failed, it was still very damaging to recover from the rush if it's even
> halfway successful."*

⚠ **This quote is reproduced with the page furniture it contains.** `Battlecode
2020 Postmortem 15` is a running header injected mid-sentence by the PDF
extraction — the sentence reads *"This was another advantage of rush: even if the
rush failed…"*. Per the index's method note, the furniture is shown rather than
silently spliced out.

**The mechanism is named in the preceding sentences, and it is terrain, not
damage:**

> *"sometimes we managed to defend rush by virtue of having enough landscapers.
> Then after our drones picked off the enemy units, there were many ditches and
> hills left around the HQ that was difficult to maneuver and left a lot of edge
> cases."*

**Referent check.** "our drones" and "our HQ" are confused's — they are the
DEFENDER in this passage, describing what a repelled rush left behind in their
own base. The residue is not enemy units surviving; it is **modified terrain that
outlived every attacking unit** and then cost the defender manoeuvring and code
correctness (*"a lot of edge cases"*). The attacker paid nothing further for it.

So the arm-D pricing is: **the correct unit of account for a push is not
"did it kill" but "what did it leave that the defender must still pay for".**

## WHY IT MIGHT TRANSFER — ⚠ AND THE CHEAPEST NULL WARNING FIRES: WE SHIP THIS

**Grep the incumbent first.** `bots/_v148ferryfirst/raid.py` already implements
exactly this, and its module header states the doctrine in confused's own terms:

> `raid.py:55` — *"barriers deposited on the first action after landing (value
> that outlives the body)"*

with the placement at `raid.py:245` (*"a barrier is placed on the first action"*)
and `raid.py:267-277` sealing a free core-adjacent seat with
`can_build_barrier`. The arithmetic is in the same header (`raid.py:22-25`):
a **barrier is 3 Ti for 30 HP and is bot-impassable; breaking one costs 15
builder pecks at 2 Ti each, i.e. 30 Ti and 15 rounds of a body — a 10:1 exchange
in our favour**, and every round they spend pecking is a round they are not
healing.

**So this file confirms a shipped plank from an independent external source
rather than proposing one.** That is a real result — the library's standing
failure is proposing things we already do — and it is why this is `partial`
rather than `yes`.

**⛔ AND IT CARRIES A CORRECTION THAT LIMITS THE GENERAL FORM.** confused's
residue was *terrain*. Ours is *our own buildings placed in their base*, and our
engine prices those differently in one direction that must not be forgotten:
**cost scale is team-keyed and additive, and destroying an enemy's buildings
LOWERS their scale.** Our barriers are OURS, so they raise OUR scale by +1% each
and do nothing to theirs — the residue is paid for in our own future build costs.
At 3 Ti and +1% a barrier is the cheapest residue the engine offers (a gunner or
sentinel would be +20%), which is *why* the barrier is the right instrument and
a forward turret is not a substitute for it. **Any generalisation of "leave
residue" toward more expensive structures inverts the exchange.**

**EFFECT ON MEDIAN KILL ROUND: NEUTRAL-TO-EARLIER as shipped, because the
residue is laid by a unit that is already there for another reason** — it rides
along on the raid rather than buying a separate trip. That free-ride property is
the same one [`buy-the-escort-out-of-income-not-off-the-critical-path`](buy-the-escort-out-of-income-not-off-the-critical-path.md)
identifies as the general rule, and it is the reason this passes the defence
admission bar. **The open question is whether the barrier's ACTION costs the
raider a MOVE and therefore a round of arrival** — see that file's hook.

## WHAT WOULD KILL IT

* **Demolition helps them.** Any version of "leave residue" that involves
  destroying enemy buildings is an economic *gift* under correction 1, not an
  attack. Residue must be additive (our barrier on their tile), never
  subtractive.
* **The 50-unit team cap and the global scale bound how much residue is free.**
  Barriers are buildings, not units, so they do not touch `MAX_TEAM_UNITS`, but
  each is +1% on the additive factor forever unless destroyed — so the marginal
  barrier gets dearer for every later build we make.
* **confused's evidence is an aside in a postmortem, not a measurement.** They
  give no figure for what the residue cost the defender. `evidence: documented`
  covers the observation; the 10:1 exchange rate quoted above is **ours**, from
  `raid.py`, not theirs, and the two must not be conflated.

## BUILDER HOOK — none new; one measurement worth having

The plank is shipped, so there is nothing to build. The unmeasured quantity is
confused's actual claim: **does our residue cost them anything after our raider
dies?** From the replay corpus, over games where a raider laid barriers at the
enemy ring and was then killed, count enemy builder-actions spent attacking those
barriers in the following N rounds, against the matched control of games where
the raider died before laying any. **That is the first direct price on
"what a failed push still bought"**, it uses only the existing corpus, and it
would tell us whether the 10:1 header arithmetic survives contact with opponents
who may simply route around a barrier instead of breaking it.
