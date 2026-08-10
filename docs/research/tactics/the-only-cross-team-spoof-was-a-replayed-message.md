---
tactic: The only documented cross-team deception in Battlecode was a REPLAYED message, and the immunity was a per-game constant
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf
origin: Battlecode 2020 final tournament — Prasici vs Steam Locomotive, reported by The High Ground (4th); immunity idiom from Battlecode 2019 / Smite
evidence: documented (the incident and its observed effect) / inference (the transfer verdict, from our Controller API)
transfers: no
---
WHAT IT IS — **The single instance of one team manufacturing a false belief in another team's
units that exists anywhere in 22 official Battlecode postmortems** (see
[`nobody-in-twenty-two-postmortems-built-a-decoy`](nobody-in-twenty-two-postmortems-built-a-decoy.md)
for the survey that establishes that denominator). It is not a decoy, not a feint and not a
fake build. It is a **replay attack on a shared, unauthenticated broadcast channel**, and it
happened in the final tournament:

> *"Prasici successfully tricked Steam Locomotive's communications by broadcasting the first
> message their seeding bot had sent."*

The effect was observed, named, and macroscopic:

> *"This hilariously caused Steam Locomotive's landscapers to run towards the edge of the map,
> trying to get to where they thought their HQ was."*

(Referents: *"their seeding bot"* and *"their HQ"* are Steam Locomotive's; the message Prasici
broadcast was **Steam Locomotive's own earlier message**, replayed, which is why it parsed —
Prasici did not have to break the encoding, only to echo it.)

**This is the answer to sweep question (D), and it is the most useful part of the file.** The
reporting team was not affected, and says exactly why:

> *"it turns out that it wouldn't have affected us as we made sure to change our communication
> encryption constants right before we submitted."*

(*"us"* is The High Ground. The referent of *"it"* is Prasici's spoof of Steam Locomotive,
described in the preceding sentence.) **The immunity was not cleverness in the moment — it was a
constant that differed from the one the attacker had captured.** Smite had generalised the same
defence a year earlier, deriving the constants from the map so they varied per game rather than
per submission:

> *"These functions used the fuel structure and size of the current map to adjust signals by a
> certain amount, making our robots use different signals each game"*

**So the one working deception in the corpus worked on a stale, replayable, cross-team channel,
and any opponent who rotated their encoding was immune for free.**

WHY IT DOES NOT TRANSFER — **our store is private, which closes the attack completely.** Our 16
integer slots are *private per team*; `read_store(index)` and `write_store(index, value)` take an
index and nothing else, and the Controller API has no cross-team read or write primitive at all.
There is no shared broadcast, nothing to capture, and nothing to replay. This restates the
verdict already reached in [`comms-jamming-and-spoofing`](comms-jamming-and-spoofing.md) from the
general attacks The High Ground names; **what this file adds is the concrete tournament instance,
its observed effect on unit behaviour, and the named immunity** — the three things the earlier
file could not supply because it was working from the paragraph that only describes the attacks
in the abstract.

**The lesson that does survive is a warning, not a tactic.** Prasici's attack worked because
Steam Locomotive's units held a *durable belief* sourced from a channel, and kept acting on it
for many turns while walking in the wrong direction. **We have exactly that structure
internally.** Our store carries durable, absolute claims and is written by whichever unit ran
last (last-writer-wins, one-round buffered); this repo's `local-vision-gate-audit-2026-08-08.md`
names the resulting defect class as *a durable decision gated on an unguarded local-vision
sample*. **Nobody can spoof us — but a single mis-scoped writer of ours reproduces the exact
failure Steam Locomotive suffered, self-inflicted.** That is the same conclusion the jamming file
reached from the other half of the same paragraph, and it is now supported by an observed
in-tournament example of what the failure looks like from the outside: an army walking
confidently to the wrong place.

WHAT WOULD REVIVE IT — one rules change and nothing less: any part of the store becoming
cross-team readable or writable. On that day, re-read this file and
[`comms-jamming-and-spoofing`](comms-jamming-and-spoofing.md) together, and note that the *replay*
form is cheaper than the *forgery* form — Prasici never had to decode anything.

BUILDER HOOK — none against an opponent. The defensive half is not a plank either (it would be
off-programme and there is no attacker). **The one thing worth carrying forward is a hygiene
check on our own store**: any slot whose value survives more than one round should have exactly
one writer, and that writer's position should be constrained relative to what it is claiming to
know. That is a correctness rule, priced in bug-avoidance, not in core_kill_share — the currency
the programme uses — and it is stated here only because this is where the evidence for it landed.
