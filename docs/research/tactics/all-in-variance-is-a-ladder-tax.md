---
tactic: FAILURE MODE — top teams reverse-engineer a working all-in and DISCARD it, because ladder rating pays for consistency
source: https://battlecode.org/assets/files/postmortem-2025-om-nom.pdf
origin: Battlecode 2025 / om nom (finalists); BC2019 Oak's Last Disciple; Halite II rooklift and Shummie; Liquipedia SC2/BW
evidence: documented
transfers: yes
---
WHAT IT IS — The recurring senior-team verdict on all-ins is not "it doesn't
work". It is "it works, and we still cut it."

**BC2025 om nom**, about the strategy of the team then leading the ladder:
> *"We spent a long time reverse engineering his rush, only to discard it last
> minute – when it worked, it was extremely effective, but when it didn't, we were
> almost guaranteed to lose."*

**BC2019 Oak's Last Disciple**, on mirror aggression:
> *"When facing other cheesy bots, it is literally a coin toss who gets the
> contested clusters. In Battlecode, experience has told me that consistency is
> really valuable."*

**Halite II Shummie (3rd place)**:
> *"If both bots rushed, then it was likely they'll kill / stall each other and the
> other two players who didn't rush would win."*
> *"I think rushing is a broken game design that basically reduces the game to a
> coinflip."*

**Halite II rooklift**, whose rush bot went 1279-176 in 2-player rush games, still
refused it in multiplayer:
> *"if I rush my opponent, and he defends adequately, we are likely to get 3rd and
> 4th"* … *"I never rush in 4 player games."*

**Liquipedia SC2/BW** state the shape as a definition:
> *"In StarCraft terms, this means committing to a single attack which can yield a
> huge gain, but if it fails you are either 1) very far behind or 2) out of the
> game."*
Referent: "this" = going All-in, defined in the two preceding sentences by
analogy to poker.
> *"Cheese relies so much on this attack that if the player fails to inflict
> crippling damage or win the game outright, they will be economically behind to a
> large degree."*
Referent: "this attack" = the attack traded for economic progress, named in the
sentence immediately before.

WHY IT MATTERS HERE — And this is the one place where our own project doctrine
partly **disarms** the objection, so it should be read carefully rather than as a
veto.

Against: our ladder is Elo, we have a stop-loss slot rule (*arms at ≥8, net ≤ −21
frees the slot*), and a high-variance bot burns slot time. Our tiebreak chain
means a failed strike loses the game it was in *and* concedes cumulative delivered
titanium — a double debit that om nom's *"almost guaranteed to lose"* describes
exactly.

For: **rooklift's and Shummie's variance arguments are specifically
multi-player** — both are about finishing 3rd/4th while two non-rushers farm.
Florent is **1v1**. There is no third party to profit from a mutual all-in, so the
strongest quantitative variance objection in the packet does not transfer. What
survives is the 1v1 form: Oak's coin-toss (rush vs rush) and om nom's binary
outcome — both real, neither multiplayer-dependent.

Also for: `PROGRAMME.md` sets `WIN_RATE_IS_VERDICT: no` and
`INCUMBENT_FROZEN: yes`. The rating is defended by a separate frozen bot; Loki is
not risking the slot while it develops. **The variance tax the sources describe is
a tax on the ladder slot, and the programme has already paid for insulation from
it.** That is a genuine and non-obvious answer to the strongest objection in this
sweep, and it is Magnus's design, not a rationalisation.

WHAT WOULD KILL IT — The insulation ends at promotion. The moment a Loki iteration
is proposed for the slot, om nom's verdict applies in full and the right
instrument is not mean win rate but the **variance** of the per-opponent result —
a bot that goes 10-0 / 0-10 against alternating opponents has the same mean as one
that goes 5-5 everywhere and is worth much less on a ladder. Our standing
`benchmark vs field, not self` rule already demands the class-weighted battery;
this adds that the battery should be read **per opponent class**, not pooled.

BUILDER HOOK — When a LOKI iteration is first measured, report core-kill share
**with its dispersion across opponents**, not just its mean. If the kill share is
bimodal by opponent, that is the om nom signature, and the correct response is to
find the discriminating feature and put it in `should_strike()` — turning the
variance into a condition — rather than to average over it.
