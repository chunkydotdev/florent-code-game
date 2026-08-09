---
tactic: Displace, don't kill — killing an enemy builder REFUNDS their cost scale
source: https://forum.codingame.com/t/spring-challenge-2022-feedbacks-strategies/195736
origin: CodinGame Spring Challenge 2022 "Spider Attack", Legend-league defensive play (Dapps, Dscarts)
evidence: documented (the principle) / inference (the application to our cost-scale rule)
transfers: yes
---

WHAT IT IS — In CodinGame Spring 2022, heroes were **unkillable**, so the entire
Legend league was forced to discover the value of wasted enemy turns. The counter
to the dominant "wind cannon" was not to kill the cannoneer but to *move* it —
Dapps: *"if they couldn't [intercept], wind heroes away from the sweet spot."*

WHY IT MIGHT TRANSFER — **In our ruleset killing is possible but actively bad, and
the rule that makes it bad is one we already have written down.**

> *"Cost scaling: every buildable entity's cost is floor(scale × base_cost) …
> builder bots/gunners/sentinels +20% each — **destroying an entity removes its
> contribution.**"*

So killing an enemy builder:
- **makes their next builder cheaper** (removes its +20% from their scale), and
- **frees one of their 50 unit slots**, and
- costs us **24-30 Ti** of converted ammo to do (40 HP = 3 sentinel or 6 gunner shots).

Throwing that same builder costs **0 ammo and 0 titanium**, refunds them nothing,
and leaves a **standing tax on their entire build order** for the rest of the match.

**The rate-limit argument is the sharper half, and it is the one fragment that
survives from the otherwise-untransferable wololo-2021 plan** (see
[sweep 2](2026-08-09-sweep-2.md)): `MAX_TEAM_UNITS = 50` and the core spawning **at
most one builder bot per turn** mean the enemy's builder count is rate-limited by
**turns, not titanium**. A core-turn is not purchasable. So:

- attacks that **remove** builders attack a resource they cannot buy — but they
  also hand back the scale refund;
- attacks that merely make them **spend titanium healing subsidise them**, because
  heal is 4.00 HP/Ti against our best damage at 1.80 HP/Ti;
- attacks that **waste their builders' turns** cost them the one thing they cannot
  buy and refund them nothing. **That is the uniquely favourable quadrant.**

WHAT WOULD KILL IT — Dscarts' caveat transfers directly: *"a persistent canoneer
would drain my mana like this very quickly and most of the time succeed anyway."*
A persistent attacker beats a reactive defender on **tempo**, even when the
defender's action is titanium-free. If they send builders faster than we can throw
them, we lose the exchange on turns despite winning it on resources.

**Honest evidence label.** I found **no sourced case of a team throwing an enemy
unit purely to waste its turns and measuring that against killing it.** The closest
precedents are CodinGame's displacement-in-a-game-with-no-kills, and Battlecode
2020's drone harass — where the throw *was* the kill (into water). **The arithmetic
above is the evidence here, not the literature.** Treat it accordingly.

BUILDER HOOK — **Corpus query, no bot change, and it is a real number we do not
have:** what *is* our opponents' builder cost scale at rounds 100 / 200 / 400?
`get_scale_percent()` is per-team and not in the replay, but builder BUILD events
are in `events.tsv` — count cumulative builder builds per team per round band and
reconstruct the multiplier. **If the field runs 5+ builders, every kill we
currently score is handing them a discount**, and that number is the argument for
flipping from kill-priority to throw-priority.

Related: [[launcher-defensive-interception]] · [[throw-into-prebuilt-cell]] ·
[sweep 3](2026-08-09-sweep-3.md) · [exchange rates](../exchange-rates-2026-08-09.md)
