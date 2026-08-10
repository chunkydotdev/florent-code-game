---
tactic: (C) NORMS CORRECTION — the library records "no league bans degrading the OPPONENT BOT". One does, by name, in its Code of Conduct, and the clause explicitly reaches in-API exploitation
source: https://raw.githubusercontent.com/BattlesnakeOfficial/docs/main/docs/policies/02-conduct.md
origin: Battlesnake (battlesnake.com) Code of Conduct, as published in the official docs repo `BattlesnakeOfficial/docs`, branch `main`
evidence: documented
transfers: no — it is a NORMS datapoint about another league, never permission and never a tactic. Filed because it corrects one of ours.
---

WHAT IT IS — [`no-league-bans-inducing-an-opponent-timeout`](no-league-bans-inducing-an-opponent-timeout.md)
concluded, after reading AIIDE and SC2 AI Arena, that the rules found protect *the game
engine* and *the ladder infrastructure* and — quoting that file verbatim —
**"Neither says anything about degrading the opposing bot."**
That is accurate about those two competitions. **It is not true of the
comparable-league field as a whole.** Battlesnake's Code of Conduct lists, under
*"Examples of unacceptable behavior include:"*:

> *"Interference with another persons Battlesnake, including, but not limited to, denial-of-service-attacks or exploiting the Battlesnake engine or API with the intent to interfere with the performance of another persons Battlesnake."*

*(Verbatim, including the missing apostrophe in "persons", from the official docs repo.
The referent of "another persons Battlesnake" is the opposing competitor's bot — the list
this bullet sits in is a conduct list whose other items are harassment, doxxing and
personal attacks, i.e. things done to other PEOPLE, and this bullet is the one that
extends that to their bot.)*

**Two features of the clause matter and are easy to lose:**

1. **It is not only a network-attack clause.** Denial-of-service is named as an *example*
   (*"including, but not limited to"*), and the second named example is
   *"exploiting the Battlesnake engine or API with the intent to interfere with the
   performance of another persons Battlesnake"* — **engine-and-API-level exploitation, in
   the same sentence, at the same prohibited status.** That is the closest published
   analogue to "make their code fail on the board".
2. **The test is INTENT, not mechanism.** The clause turns on *"with the intent to
   interfere"*. Under a rule shaped like this one, the Steamhammer finding
   ([`a-crash-is-recorded-as-a-win-so-learners-converge-on-it`](a-crash-is-recorded-as-a-win-so-learners-converge-on-it.md))
   — a bandit that converges on a crash-inducing plan with no such module written — would
   land on the permitted side, and a hand-coded "make them throw" plank on the prohibited
   side, for identical board behaviour.

**Battlesnake also has a structural reason to legislate this that we do not share:** its
competitors host their own HTTP servers and the engine calls out to them, so "interfering
with another person's Battlesnake" is partly a statement about someone else's *machine*.
**That materially weakens the analogy and must be stated whenever this file is cited.**
It does not erase the second example, which is about the engine and API.

WHY IT MIGHT TRANSFER — it does not transfer as a tactic. It transfers as a correction:

- **The premise "nobody prohibits it" was doing work in our hold reasoning, and it is now
  one counter-example weaker.** The accurate cross-league summary after sweep 21 is: *AIIDE
  and SC2 AI Arena protect the engine and the ladder and are silent on the opposing bot;
  SSCAIT and BASIL score an opponent's crash as an ordinary win with Elo; **Battlesnake
  prohibits interfering with another person's bot by name, including via the engine or
  API**; our organisers are silent.* **A split field, not a clear field.**
- **It sharpens the question for Magnus** rather than answering it. The question is no
  longer whether anyone bans it — someone does — but which of these leagues ours most
  resembles. Ours resembles Battlecode (shared engine, uploaded code, no self-hosting), and
  Battlecode's published rules were not found to address it either way.

WHAT WOULD KILL IT — as a reason to change our behaviour, several things:

- **A Code of Conduct is not a game rule.** This is in `docs/policies/`, alongside the
  diversity statement and the terms of service, not in `docs/rules.md`. It is enforced by
  community leaders, not by the engine. **Someone arguing it is "not really a competition
  rule" has a point worth hearing.**
- **The self-hosting asymmetry above.** If a reader concludes only "they banned DDoSing a
  web server", the clause's second example is being dropped, and if a reader concludes
  "leagues ban crash induction", one league's conduct policy is being over-generalised.
  **Both readings are wrong; quote the sentence.**
- **None of it binds our organisers.** The library's standing rule holds in both
  directions: another league's ban is not our ban, exactly as another league's silence was
  never our permission.

BUILDER HOOK — **none, and deliberately none.** The single action is that the open question
already queued for Magnus should be re-posed with this in it: *one comparable league
prohibits interfering with an opponent's bot including via the engine or API; two Brood War
ladders award the win when an opponent crashes; ours is silent — where do we stand?*

Related: [`no-league-bans-inducing-an-opponent-timeout`](no-league-bans-inducing-an-opponent-timeout.md) ·
[`cpu-timeout-induction`](cpu-timeout-induction.md) ·
[`manner-pylon-and-what-the-rules-permit`](manner-pylon-and-what-the-rules-permit.md)
