---
tactic: two opposite answers to "my ladder presence leaks my bot" — be a moving target, or ship less often
source: http://satirist.org/ai/starcraft/blog/archives/1061-AIST-S4-prep.html · http://satirist.org/ai/starcraft/blog/archives/186-win-ruthlessly-like-LetaBot-and-ZZZKBot.html · http://satirist.org/ai/starcraft/blog/archives/955-Steamhammer-3.1-early-returns.html · http://satirist.org/ai/starcraft/blog/archives/757-beating-SAIDA.html
origin: Jay Scott (Steamhammer), Igor Dimitrijevic (Iron), Dan Gant (PurpleWave), 2016–2021
evidence: anecdotal — every item is a first-person statement of intent or a recommendation; NOT ONE was measured against the alternative
transfers: partial
---
WHAT IT IS — BW bot authors reasoned explicitly about their continuously-visible ladder
presence as an information leak, and converged on **two opposite counter-moves**, neither
ever tested against the other.

**CHURN — be a moving target** (`pflat/1061-AIST-S4-prep.flat`):
> "I haven't been posting about Steamhammer progress because I'm preparing (ssh! it's a
> secret!) Secret Improvements. When the list of participants is announced, I expect I'll
> make special arrangements for some of them. Steamhammer should be a moving target so that
> the same doesn't happen to it."

*(Referent of "the same": opponents making **their** special arrangements against
Steamhammer.)*

**FREEZE — ship less often so you are a less attractive target**
(`pflat/186-win-ruthlessly-like-LetaBot-and-ZZZKBot.flat`, Igor Dimitrijevic, author of
Iron):
> "Also, it should be noted that, in the tournament of chaos and chance, some bots are more
> likely to be targeted: the strongest ones, the ones that are easy to test locally, and the
> ones that are updated often during the year. Some bot authors may thus decide to update
> their bots less often."

**AND A THIRD, MORE INTERESTING MOVE — ship a deliberately weakened version**
(`pflat/955-Steamhammer-3.1-early-returns.flat`):
> "The games become public, and nothing else. If you worry that the games themselves may
> give away your secrets (other bots might use the ladder as training data), you can work
> around that too: Deliberately weaken your strategy. You'll still test correctness and
> adherence to the time limits, but you don't test your strength so you don't give away
> your true weaknesses to others."

*(This is a recommendation, not a reported act. Referent: "the ladder" is the StarCraft AI
Ladder used as an AIIDE dress rehearsal; the stated purpose of the weakened version is to
test correctness and time limits while withholding strength.)*

**THE LEAK WAS REAL — a rival built a counter from a specific named opponent's public
output and said so** (`pflat/757-beating-SAIDA.flat`, Dan Gant, author of PurpleWave):
> "Part of the motivation for my approach to PurpleWave's PvT in SSCAIT was observing that
> SAIDA's code was oriented around supporting the particular style of play it demonstrated
> in AIIDE. In particular, what stood out was the absence of a general-purpose combat
> simulator."

— and another author kept a standing exploit ledger on that same rival: *"I've been tracking
SAIDA exploits in a spreadsheet. We are up to about 10 per matchup (about half of which have
been tried) 1/3 of which have had some success."* Both are **first-person accounts of intent
and design; neither shows games or rates**, so the counter-building is documented and its
*effect* is not.

WHY IT MIGHT TRANSFER — it corroborates the local fact from an independent field: **every
BW author who reasoned about leakage reasoned about continuously-visible LADDER presence,
never about private test games.** That matches our measurement that a bot holding the slot
publishes itself at ~6 games/hour while a 5-game unrated leg shows itself five times. The
useful residue is the **menu**: churn, freeze, and weakened-decoy are the three moves the
field actually considered, and knowing the menu is worth more than any one item on it.

WHAT WOULD KILL IT — **all three are DEFENSIVE, and `NEVER PLAY DEFENCE` governs.** More
practically, all three are unavailable or off-currency here:
* **Churn** costs a submission per iteration, and on this platform submitting **is**
  shipping (auto-activation). We cannot churn cheaply.
* **Freeze** is directly contradicted by our own measurement: a frozen bot loses **8.00pp of
  game share per opponent version generation** (`block-on-opponent-version-not-opponent-id.md`).
  Standing still to avoid being scouted is paying a known cost to avoid an unmeasured one.
* **Weakened-decoy** would put a deliberately worse bot on the *rated* ladder, where the
  rating is the thing we are trying to move. In BW the dress-rehearsal ladder was separate
  from the tournament that counted; **for us there is no such separation.**

And the premise is unestablished here: **that we are published is a rules fact; that any
rival acts on it is an inference with zero support in our archive**
(`our-shipped-bot-is-a-published-pure-policy.md`). Two attested moves pointing in opposite
directions, neither measured, is a menu — not a prescription.

BUILDER HOOK — none. **Do not spend a leg on any of the three.** File it so the next session
does not rediscover the menu and mistake its existence for evidence. If the underlying
question is ever tested, note the one asymmetry worth exploiting first: SAIDA adapted to a
new opponent strategy **without shipping a new version at all**, because its change lived in
a learning file — a channel that does not exist in our league (see
`a-version-bump-is-the-only-behaviour-channel-here.md`).
