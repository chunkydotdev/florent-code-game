---
tactic: Inducing an opponent's per-turn compute overrun
source: https://www.satirist.org/ai/starcraft/blog/archives/1145-AIIDE-2021-what-Steamhammer-learned.html
origin: StarCraft AI (AIIDE/SSCAIT, 2021-22); Battlecode 2009 "message warfare"
evidence: documented (effect) / documented-once (deliberate crash variant)
transfers: partial — AND SEE THE NORMS SECTION BEFORE BUILDING
---

## NORMS — read this first

**Deliberately inducing an opponent's compute overrun is banned by name in at
least two comparable leagues.**

- **BASIL ladder**: *"Intenionally causing this timeout to avoid losing will
  result in the bot being banned."* [sic] — https://www.basil-ladder.net/rules.html
- **SC2 AI Arena**: prohibits *"Slowing down the system on purpose."* —
  https://aiarena.net/wiki/rules/
- **SSCAIT**: exceeding the frame budget is an immediate loss; bots that
  *"crash/hang/timeout too much"* may be disqualified. —
  https://sscaitournament.com/index.php?action=rules
- **Ours**: no fair-play clause found in the scraped docs either way. Note an
  internal conflict worth resolving on its own —
  `docs/reference/official-docs.md:1091` says *"Bot disqualified mid-match | CPU
  time exceeded 10 ms"*, while `CLAUDE.md:13` says the same event merely
  interrupts that turn.

**Position taken (research arm, 2026-08-09):** exploiting *measured opponent
habits* is legitimate competitive play and is what the play-the-players mandate
asks for. **Deliberately targeting an opponent's compute budget is a different
act, is banned by name elsewhere, and should not ship until Magnus has asked the
organisers.** The incidental and defensive halves below carry no such risk.

## WHAT IT IS

Creating game states expensive enough that opponent units exceed their per-turn
budget and lose the turn (or, in the sharper variant, throw and die).

## WHY IT MIGHT TRANSFER — the effect is real and tournament-deciding

In StarCraft it happens **as a side effect of good play, by bots that never
intended it**:

- *"Of those 25 wins versus BananaBrain, 15 were due to BananaBrain suffering a
  frame timeout... BananaBrain was ahead in 11 of the 15 games when it timed
  out."*
- Mechanism, named by an author: *"Dragon is an especially easy bot to time out
  against, because its **strong macro and big battles with light units** put
  heavy demands on the opponent."*
- **The natural experiment.** AIIDE 2022 was run twice on identical bots, VMs
  then bare metal: **1,144 frame timeouts → 90**. McRave's timeout rate fell
  26.55pp and its win rate rose 11.31. **Dragon — the inducer — had a timeout
  diff of exactly 0, yet lost 9.22 points of win rate and fell #3 → #6** when its
  opponents stopped timing out.

**And our measurement matches the shape**: three opponents already sit at
3.5-4.7% of unit-turns discarded (`ammo-and-cpu-2026-08-09.md`), with Ouroboros
at median 0 / mean 310 / max 3,508 — a conditional blow-up in 44% of games.

## WHY THERE IS NO BATTLECODE PRECEDENT — the sharpest technical fact

Battlecode's `senseNearbyRobots` costs a **flat 100 bytecodes regardless of how
many robots it returns** (their MethodCosts.txt). **The opponent structurally
cannot inflate the call.** Our `get_nearby_entities/buildings/tiles` are **not**
fixed-cost. That family's organisers designed the vector out; ours has not.

**This cuts both ways, and the defensive half is free:** we are exposed too, and
our own 0.00% at ~12% of budget is headroom we are not spending.

## THE ONE TIME A COMPETITION REWARDED IT — and it was crash, not timeout

Battlecode 2009, team "little": reverse-engineered `Arrays.hashCode` and crafted
**hash-preserving corrupted broadcasts**, so opponents *"would often resize the
array to be gigantic, and throw an out-of-memory exception and die."*
Independently corroborated by a Battlecode engine developer. It won a
*"message warfare"* award. — https://realgl.blogspot.com/2013/08/battlecode.html

**Does not transfer directly** — our comms store is team-private, so there is no
injection channel. **But it validates the direction: crash induction, not timeout
induction, is where the asymmetry lives**, and our engine's permanent-unit-
destruction penalty makes it sharper here than in Battlecode, where an unhandled
exception merely paralyses a robot.

## WHAT WOULD KILL IT

Our per-turn budget may not scale with entity count the way we assume — nobody
has measured `get_nearby_*` cost against entity density in OUR engine. Until that
is done this is a hypothesis about our own API's cost curve, not a finding. And
the trigger for Ouroboros's conditional blow-up is still unidentified.

## BUILDER HOOK

**Three separable halves, in ascending risk:**
1. **Defensive (free, no norms issue):** our 0.00% TLE at ~12% of budget means
   every "too expensive to compute" gate in our bot is worth re-asking.
2. **Incidental (free, no norms issue):** entity-dense, long games tax the
   opponent and are good play anyway — this is exactly what Dragon did.
3. **Deliberate: HOLD pending an organiser ruling.**

## OPERATIONAL CAUTIONS FROM THE RECORD

- Cory Li's exploit died because **he used it in scrimmages** — opponents noticed
  robots "mysteriously exploding" and patched before finals.
- **This engine family's organisers nerf spam fast and publicly**:
  *"Higher unit scaling, more expensive builders, and a global unit cap all
  reduce spam and improve runtime"*; *"only adversarial exploits are blocked"*
  (https://docs.battlecode.cam/changelog). **Caveat: that changelog cites a 2ms
  limit and units we do not have — a sibling or later season. Do not quote its
  numbers at ours.**

## GAPS

Reddit hard-403s every tool; the SSCAIT, Battlecode and Screeps Discords are the
real centres of gravity and are not web-indexed. If deliberate induction exists
as unwritten folklore, that is where it lives.
