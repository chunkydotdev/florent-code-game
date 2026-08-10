---
tactic: Most deception does not work on bots — the one form that does is exploiting an overreaction, and the fake attack must be able to CONVERT
source: http://satirist.org/ai/starcraft/blog/archives/627-exploiting-overreactions.html
origin: Jay Scott's StarCraft AI blog, 2018-08-03, on the SSCAIT bot "5 Pool"; human-play cost condition from Liquipedia (StarCraft) "Threat"
evidence: documented (the mechanism and the bot's standing) / anecdotal (the payoff — no controlled measurement exists)
transfers: partial
---
WHAT IT IS — **The scoping law for this entire sweep, written by the person who has watched more
bot-vs-bot StarCraft than anyone, and it is bad news for eight of the ten ideas anyone will
propose:**

> *"Most forms of deception do not work against bots, because bots are not smart enough to fall
> for them. Exploitation of overreactions is a form of deception that often does work, at least
> against bots that react at all."*

(Written in the context of Locutus building decoy pylons in Iron's base; *"them"* = the forms of
deception; the referent of *"bots"* throughout is competition StarCraft bots on SSCAIT, not human
players.) **A bot has no ego to bait, no morale to break, and no memory of being fooled. What it
does have is a reaction function, and reaction functions can be badly tuned.**

**The one documented working feint in bot competition is 5 Pool's, and its structure is the whole
lesson.** It is not a decoy — it is a real attack that is *abandoned* once it has bought the
overreaction:

> *"It opens with 5 pool as its name says, you see the rush coming, you are completely safe—but
> there is no stream of zerglings looking for a way to break in. After a handful of zerglings to
> scare your bot into reacting, 5 Pool switched into drones and tech while you unnecessarily
> built up your forces to safely move out."*

> *"Somehow your reaction to being rushed set you further back than playing 5 pool set your enemy
> back!"*

And the standing, which is the only quantitative anchor the source offers:

> *"The bot 5 Pool exploited the fact that most opponents either didn't react and lost, or
> overreacted and fell behind. Exploiting overreaction is a fancier trick, but it is also easier
> to code than to defend against, and 5 Pool ranked high."*

**Note what 5 Pool did NOT do: it did not build a fake thing. It built a real, cheap, genuinely
threatening thing, showed it, and then spent the tempo elsewhere.** The threat was true at the
moment it was shown; only the *follow-through* was a lie.

**The cost condition, from human theory, is the mirror of this.** Liquipedia's *Threat* article
describes the fake threat as investing *"the absolute minimum into the threat"* with *"no real
ability to inflict damage should your opponent fail to counter it"*, and states the failure
condition exactly:

> *"A disadvantage is that it relies on you correctly judging your opponents meta-game level. If
> they are too weak to understand that they "cannot" do certain things while a threat is present
> then you are unable to punish them for their mistake and your bluff is called."*

(*"they"* / *"your opponent"* here is a human StarCraft opponent; the *"meta-game level"* is that
opponent's strategic sophistication.) **Two independent sources, one about bots and one about
humans, converge on the same condition: the value of a bluff is created by the victim's
competence, not by the bluffer's cleverness.**

WHY IT MIGHT TRANSFER — **because the programme's whole thesis is that our field over-reacts, and
this file names the shape the provocation must have.** Loki wants a dead core inside 250 rounds;
5 Pool's structure says the correct opening is one that is **genuinely lethal if ignored** and
**convertible if answered**. That is not a decoy plank — it is a *conversion* plank, and it is
strictly easier for us than for 5 Pool, because our `destroy()` is free, uses no action cooldown,
is unlimited per turn, and returns the destroyed building's contribution to the global cost scale.
**We can un-buy a threat that has done its work.**

Our library has independently arrived at the same doctrine from a different league — wololo taxing
a defensive reflex that fires *"regardless of whether it would work for them or not"*
([`their-defensive-reflex-fires-unconditionally`](their-defensive-reflex-fires-unconditionally.md)).
**Jay Scott is the second, independent statement of that mechanism, and he generalises it: the
overreaction is the only exploitable surface a bot has.** The in-base machinery and the AIIDE
legality ruling live in
[`manner-pylon-and-what-the-rules-permit`](manner-pylon-and-what-the-rules-permit.md); this file
is the doctrine layer, not a second copy of that plank.

WHAT WOULD KILL IT — **three things, and the first is measured against us already.**

1. **An opponent that under-reacts is immune, and ours may be.** Jay Scott's dichotomy is
   *"didn't react and lost, or overreacted and fell behind"* — our own reaction atlas puts
   Ouroboros at a **median 8-round heal latency**, which the manner-pylon file already flags as
   looking like under-reaction. **Against a slow reactor, a feint is a donated tempo.**
2. **A feint that cannot convert is just a bad attack.** 5 Pool's edge came from switching to
   *"drones and tech"*. Our equivalent — recovering the titanium and the cost-scale contribution
   — exists, but the *builder-turns* spent placing and removing do not come back
   ([`the-decoy-is-not-priced-in-titanium-it-is-priced-in-builder-turns`](the-decoy-is-not-priced-in-titanium-it-is-priced-in-builder-turns.md)).
3. **There is no controlled measurement anywhere.** *"5 Pool ranked high"* is a ladder standing,
   not an ablation. See
   [`the-only-number-anyone-has-on-opponent-modelling-is-a-null`](the-only-number-anyone-has-on-opponent-modelling-is-a-null.md).

BUILDER HOOK — **do not build a fake. Build a real opening that is cheap to abandon, and measure
the abandonment.** Concretely: the sentinel-rush opening already in the programme *is* the 5 Pool
shape if it gains one branch — **if the enemy's answer to the first forward sentinel exceeds a
threshold (N builder-turns diverted, or a defensive turret bought), `destroy()` the plant, bank
the scale refund, and convert the freed titanium into the second push.** Falsifier: if
core_kill_share does not move and time_to_core_kill worsens, the field is under-reacting and
Jay Scott's precondition (*"bots that react at all"*) does not hold for our pool — which is a
clean, one-leg kill for the whole deception family.
