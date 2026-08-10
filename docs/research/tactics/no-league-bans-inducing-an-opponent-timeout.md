---
tactic: The organiser ruling that cpu-timeout-induction was held on — nobody bans degrading the OPPONENT BOT
source: https://davechurchill.ca/starcraft/aiide/
origin: AIIDE StarCraft AI Competition rules (2026); SC2 AI Arena (aiarena.net) wiki rules and result taxonomy
evidence: documented
transfers: partial
---

WHAT IT IS — **[[cpu-timeout-induction]] is filed as "BANNED BY NAME in BASIL and
SC2 AI Arena — held pending an organiser ruling". Sweep 11 went and read the
actual rule text, and that characterisation is too strong.** Both competitions
protect the *game engine* and the *ladder infrastructure*. **Neither says
anything about degrading the opposing bot.**

AIIDE's malicious-behaviour clause:

> *"Bots that perform malicious behavior will be disqualified and banned from all
> future contests. This includes but is not limited to: Intentionally crashing
> StarCraft, Installing worms/viruses/malware on the host machine, Malicious
> utilization of resources such as sockets, files, zombie processes, Spamming
> the in-game console."*

**Every item names the host or the game.** "Intentionally crashing StarCraft" is
crashing the shared engine, not the opponent's process.

SC2 AI Arena's general rules:

> *"Bot authors must ensure that their creations are not harming the ladder
> system in any way, including but not limited to:"*

with the relevant list items being *"Slowing down the system on purpose"* and
*"Tampering with the filesystem or memory"* — **the system being protected is the
ladder**, and the only clause that touches match conduct is a must-try-to-win rule:

> *"The uploaded bot should be trying to win its matches"*

**And the same site's result taxonomy treats an opponent's crash or hang as a
normal, Elo-affecting win** (aiarena.net/wiki/ladders/result-types/):

> *"Player 1's bot process crashed. Player 2 is awarded the win."*

> *"Player 1 timed out/hung. Player 2 is awarded the win."*

Those sit under the heading **ELO change**, alongside a standard win. The
infrastructure is built to score it, not to void it.

WHY IT MIGHT TRANSFER — **because we measured an opponent-side compute blow-up
and then parked the tactic on a ruling that does not exist.** Our own numbers
(`docs/research/ammo-and-cpu-2026-08-09.md`): Ouroboros discards **26,356
unit-turns across 85 games** — median 0 per game, mean 310, **max 3,508** —
firing in **44% of games**; Leviathan 4.40%, The Bisons 4.65%; every 1800+ team
and we ourselves sit at **0.00%**. **A conditional compute blow-up in three
opponents is the most exploitable shape a weakness can have.**

Two things this file changes and one it does not:

1. **The precedent is weaker than we recorded.** *"Slowing down the system on
   purpose"* is a ladder-infrastructure clause. Reading it as a prohibition on
   slowing the opponent's bot is an interpretation, not the text. **The library
   should say so.**
2. **The nearest real prohibition points the other way.** AIIDE forbids *"Gas
   walk to get through blocked entrances or ramps"* — exploiting an *engine bug*.
   **Our timeout lever is not an engine bug; it is the opponent's own algorithm
   scaling badly with board state we control.** Nothing in either rule set
   reaches that.
3. **It does not make it a good idea.** See below.

WHAT WOULD KILL IT — and the first two are the ones that should decide it:

1. **OUR organisers have not ruled, and none of this binds them.** AIIDE and
   aiarena are evidence about norms in comparable leagues. **This file must never
   be cited as permission.** The honest summary for the builder is: *the
   published rules elsewhere do not prohibit it, and ours are silent* — which is
   a reason to **ask**, not a reason to ship.
2. **We do not know the trigger.** The whole tactic rests on finding what makes
   Ouroboros' per-turn cost blow up, and we have never identified it. **Until
   there is a named, reproducible trigger there is nothing to build**, and a
   speculative one costs us CPU too, against a 10 ms per-unit budget we
   currently never exceed.
3. **Reputational asymmetry.** We are on a public ladder under a team name.
   A tactic whose entire content is "make their code fail" reads differently
   from a tactic that wins on the board, whatever the rules say. **That is
   Magnus's call and nobody else's.**
4. **It may be worth nothing.** A discarded unit-turn is not a lost game;
   Ouroboros discards a *median of 0* per game and still rates highly. The mean
   is carried by a tail. **Nobody has shown that pushing them into the tail
   changes an outcome.**

BUILDER HOOK — **none. Do not build anything on this file.** The single next
action is a question for Magnus, and it is now a well-posed one rather than a
vague worry:

> *AIIDE bans crashing the game engine and abusing the host; SC2 AI Arena bans
> harming the ladder and awards the win when an opponent crashes or times out.
> Neither prohibits inducing a timeout in the opposing bot. Do we treat that as
> in-bounds here?*

If the answer is yes, the work that follows is **trigger identification**, which
is a corpus question (what board states precede Ouroboros' discard spikes?) and
not a bot change.

Related: [[cpu-timeout-induction]] · [[manner-pylon-and-what-the-rules-permit]] ·
[ammo and CPU](../ammo-and-cpu-2026-08-09.md)

---

> ## ⛔ **THIS FILE'S HEADLINE CLAIM IS NARROWED — 2026-08-10, sweep 21. ONE COMPARABLE LEAGUE DOES BAN IT, BY NAME.**
>
> The title and frontmatter say *"nobody bans degrading the OPPONENT BOT"*, and this
> file's prior reading was that every clause found protects **the engine and the
> ladder**, never the opponent's bot. **That is wrong as a statement about the field.**
>
> **Battlesnake's Code of Conduct lists as unacceptable behaviour:**
> > *"Interference with another persons Battlesnake, including, but not limited to,
> > denial-of-service-attacks or exploiting the Battlesnake engine or API with the
> > intent to interfere with the performance of another persons Battlesnake."*
>
> **The second named example reaches ENGINE-AND-API-LEVEL EXPLOITATION, not merely
> network attack, and the test it applies is INTENT.** That is squarely a prohibition
> on degrading the opponent's bot.
>
> **Two caveats stated with it, because they bound how far the correction goes:**
> Battlesnake competitors **self-host**, which changes what "interference" can mean
> there; and the clause sits in `policies/`, **not in `rules.md`**.
>
> **WHAT THIS DOES AND DOES NOT CHANGE.** It narrows the premise — *"no comparable
> league prohibits this"* — that the `cpu-timeout-induction` **HOLD was partly reasoned
> against.** **The hold itself is unchanged and remains pending an organiser ruling.**
> And the standing caution in this library is now doubly load-bearing: **a tactic no
> other league bans is NOT thereby permitted here. Our organisers' rules govern, and
> ours are SILENT.**
>
> Per-league stance as re-verified by sweep 21: **SSCAIT / BASIL** — no rule on causing
> the opponent's crash; both score it as an ordinary loss for the victim. **AIIDE /
> SC2 AI Arena** — engine and ladder only (this file's prior reading CONFIRMED).
> **Battlesnake** — prohibits it by name (above). **Lux S1/S2, Halite II, Terminal** —
> nothing found either way in the fetched specs. **Ours — silent.**
