---
tactic: The worker-fortified turret — workers keep the gun alive, the gun keeps the workers alive
source: https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf
origin: Battlecode 2020 / Java Best Waifu (1st overall); independently corroborated by Battlecode 2020 / The High Ground (4th) and by Liquipedia StarCraft Brood War
evidence: documented
transfers: yes
---

WHAT IT IS — **not "workers repair defence" as a chore, but a two-part cell that
is unbreakable from either side alone.** Java Best Waifu, who won Battlecode
2020, describe running into it in the semi-final against smite and record it as
the one thing that would have beaten them:

> "If they managed to complete their cookie we were doomed because there was no
> way of penetrating it: a full army of landscapers would keep the Net Guns
> alive, and we could not drown their Landscapers because of the Net Guns."

and again, in their own rule-change suggestions at the end of the document:

> "if several landscapers were surrounding a net gun it was almost impossible to
> destroy unless you crunch it with Drones."

The structure of the argument is a closed loop: *the workers out-repair the
damage on the gun, and the gun kills the only unit type that could remove the
workers.* Neither half works alone. The High Ground record the same loop from the
attacking side, and note the enemy paying a *strategic* price to maintain it —

> "Kryptonite prioritized surrounding their own net gun over destroying our HQ,
> which often led to extended standoffs as we were unable to build drones and
> unable to bury their net gun."

Brood War's version is the SCV-repaired bunker, where the wiki states the same
mutual dependency plainly: the bunker "can be repaired by SCVs, allowing the life
of the Bunker to be significantly extended; the more SCVs working, the faster the
rate of repair."

WHY IT MIGHT TRANSFER — **because our 1,130-replay death-attribution says the
field is already running this cell and we are not.** In their own home band,
32.3% of the field's builder deaths are next to their own turret (lift **5.04**);
ours are 2.7% (lift 1.00). Forward, it is 42.2% against our 7.7%. Read through
Java Best Waifu, those are not workers being caught out of position — **that is
the signature of a maintained gun**, and the lift says it is where their workers
*choose* to stand.

Our ruleset closes the loop harder than Battlecode 2020's did:

- **Builder attacks cannot damage builder bots at all** (project CLAUDE.md;
  `heal-arithmetic`). So a healer standing next to our turret is *categorically*
  immune to the enemy's workers — not merely hard to kill, but untargetable.
- **The only thing that can remove that healer is an enemy turret** — and an
  enemy turret in our base is the thing our own turret is there to shoot.
- The break-even is small: **two healers (8 HP/rd) strictly out-heal one enemy
  gunner (7 HP/rd)**, and two healers holding two of a turret's four orthogonal
  tiles cap enemy builder chip at 4 HP/rd against 8 HP/rd of repair. See
  [[marginal-healers-per-structure]] for the table.

That reframes our own measurement. We have four times tested "build more turrets"
and every knob came back neutral-to-negative. **This file says the turret was
never the unit of account — the cell is.** An unattended gunner is a 25 HP
building that any two enemy builders erase for 25 Ti of chip; a gunner with two
healers is an object the enemy cannot remove with builders at any price.

WHAT WOULD KILL IT — and one of these is close to fatal:

1. **The sentinel is the counter and it is in everyone's build list.** A sentinel
   does 9 HP/rd and its line "is never blocked by walls or units in the way"
   (official docs). Three healers are needed just to break even against one, four
   against a gunner+sentinel pair — at which point the cell consumes all four
   orthogonal tiles and four builder-turns per round, forever. **A cell is only
   cheap against attackers who cannot outrange it.**
2. **Opportunity cost against tiebreak #1.** Builders pinned to a turret deliver
   no titanium, and cumulative titanium delivered is the first tiebreak in the
   353 games that reach r1000, which we currently win 57.2% of. This tactic
   spends the asset we win on.
3. **Battlecode 2020's landscapers were doing double duty** — the same unit that
   repaired the net gun was also burying the enemy HQ and terraforming. Our
   healer does exactly one thing per turn and cannot even move that round
   ("acting or moving is mutually exclusive per round"). The Battlecode cell was
   nearly free; ours is not.
4. **Cost scale.** Gunners and sentinels are **+20% per build** — the harshest
   tier in the game. Any doctrine that answers "we lose turrets to chip" with
   "build another" is paying the worst scaling in the ruleset, which is precisely
   the argument for repair over replacement.

BUILDER HOOK — **do not build a new turret; keep the one we have.** The smallest
version needs no new turret production at all, which matters because turret
production is the knob that has already been refuted four ways:

> When a friendly **gunner or sentinel** in a builder's r²=20 vision has
> `hp < max_hp` and at least one enemy entity adjacent to it, and we can put
> `ceil(incoming/4)` builders on its orthogonal tiles, hold them there and heal
> until `hp == max_hp`; then release. Otherwise do not start.

Two measurements decide whether it is worth more than the predicate in
[[marginal-healers-per-structure]]:

1. **What actually kills our turrets?** If our gunners die mostly to *enemy
   builder chip* the cell is decisive (chip is exactly what two healers cancel).
   If they die mostly to sentinel fire, the cell is a losing race and this file
   is a filed negative.
2. **How long does a field turret survive with workers adjacent versus without?**
   We have the attribution corpus to compute the field's own side of it, and
   their 5.04 lift is only evidence of the cell if their turrets are also
   outliving ours.

Related: [[marginal-healers-per-structure]] · [[heal-cap-and-timeout]] ·
[[fortify-on-idle]] · [[sentinel-file-stacking]]
