---
tactic: Strike LATE inside the window — the anti-rush reflex is tuned to the early clock and expires
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020 / Kryptonite (HS champions), as described by their strongest opponent Java Best Waifu
evidence: documented
transfers: yes
---
WHAT IT IS — Java Best Waifu were the team that **solved** the BC2020 rush meta by
building a defensive interceptor early. They say so, verbatim:

> *"rush bots have a hard time trying to get their rush Miner close to our HQ
> because we started building Drones really early"*

One team beat that anti-rush anyway, and they name the reason — the attacker
moved the clock:

> *"our bot assumed that we could produce units at a better pace than the enemy
> since we are investing in economy while they sacrificed an early worker trying
> to rush. However, Kryptonite rushed relatively late"* … *"stacked a lot of soup
> in between, and then spent immediately all that soup to build Net Guns and
> Landscapers"*

The anti-rush was not beaten by more attackers. It was beaten by **arriving after
the defensive assumption had already been priced in**, with a banked treasury.

WHY IT MIGHT TRANSFER — Very strongly, and it is the most important scheduling
result in this sweep for `KILL_WINDOW_RND: 250`. **The window is 250 rounds; it is
not an instruction to attack at round 20.** Our ammo economy makes the banking
half unusually clean: `convert_ammo` is 1:1, at most once per team per turn,
usable the same turn, and **does not consume the core's action cooldown** — so a
core can bank titanium for 150 rounds while still spawning a builder every turn,
then convert in bulk. Sweep 2 filed the banking half (`Bank the economy, then
alpha-strike`); this file supplies the *timing* argument that makes it a Loki
plank rather than a general principle: the defender's readiness is not constant
over the window, and the field's readiness is measurably concentrated early
(the field's own kills are 12% by r100, median r296 — their guard is up when
their own clock says it should be).

Arithmetic that makes a late strike affordable, and it is MY arithmetic, not
sourced — label it inference. Core 500 HP. A sentinel is 18 dmg on reload 2 =
9 HP/round for 5 Ti/round of ammo. Against the field's measured 2.68 healers
(~10.7 HP/round) the net rates are: N=2 → 7.3 HP/rd, ~68 rounds, ~680 Ti of ammo;
N=3 → 16.3 HP/rd, ~31 rounds, ~465 Ti; N=4 → 25.3 HP/rd, ~20 rounds, ~400 Ti.
**Because the heal is a per-ROUND tax, total ammo spent falls as the kill window
shortens** — concentration is cheaper in ammo, not just faster. Banking to afford
N=4 at once therefore costs strictly less than trickling N=2 from round 40.

WHAT WOULD KILL IT — Banking is visible. Java Best Waifu had 150+ rounds of
warning and still lost only because their single interceptor missed; a defender
who reads a stalled build and pre-places turrets converts our bank into their
positioning time. Second: banking titanium is not free here — tiebreak key #1 is
**cumulative titanium delivered**, an integral over time, so a long bank concedes
the tiebreak we currently win (353 games reached r1000; we won 57.2%). A late
strike that misses gives up both the kill and the clock.

BUILDER HOOK — No new units. One scheduling constant: the round at which
accumulated titanium is converted and committed. Sweep it as a parameter
(r80 / r120 / r160 / r200) on core-kill share and time-to-core-kill against
LOKI-(N-1). This is the cheapest high-information knob the programme has.
