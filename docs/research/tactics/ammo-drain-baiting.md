---
tactic: Ammo-drain baiting — trade cheap bodies for expensive shots
source: https://screeps.com/forum/topic/2995/best-attack-strategy
origin: Screeps tower drain; Robocode bullet shielding (https://robowiki.net/wiki/Bullet_Shielding)
evidence: anecdotal (community-formalised, widely replicated)
transfers: yes
---
WHAT IT IS — present a cheap target that forces the defender to spend a scarce
combat resource, repeatedly, until the defence is dry. Screeps: "A tower can't
hurt you, if it doesn't have energy" — tank a shot, retreat, heal, repeat, so the
defender spends more refilling than the attacker spends on bodies. Robocode's
version fires 0.1-power bullets to intercept high-power ones until the enemy
disables itself.

WHY IT MIGHT TRANSFER — **better here than in Screeps**, because our ammo is
bought from the same titanium pool as buildings at exactly 1:1 and there is NO
passive ammo income. Every baited sentinel shot is **10 Ti deleted from their
build budget**; a gunner shot is 4. A 3 Ti barrier absorbing a sentinel volley is
roughly a 6.7:1 titanium exchange, and it also consumes the turret's reload.
This lands directly on a measured fact: the six opponents we studied convert
155-441 ammo per game in r200-300. Ammo is their engine, not a side cost.

WHAT WOULD KILL IT — if turret target selection prefers units over buildings, a
barrier will not draw fire at all. Unknown and testable. Also our own cost scale
is global (builder-measured), so barrier spam raises OUR prices too, at +1% each
— the cheapest scaling available, but not free.

BUILDER HOOK — measure whether enemy turrets shoot barriers at all before
anything else. One local game, count `fireTurret` events targeting a barrier
tile. If they do not, the tactic is dead for 3 Ti instead of a build cycle.
