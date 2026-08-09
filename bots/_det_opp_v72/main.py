"""v61 OFFLINE — Replay-routed macro with early counterbattery pressure.

The ladder replays showed that one-hop Launchers and a 60-ammo stockpile were
dead capital.  This branch instead fields five useful builders, connects ore
immediately, and spends ammunition just in time on forward and home gunners.

_v70th variant: TURRET-HUNTING UNDER SIEGE.  _v70mh's converged healers repair
a shelled Core but never silence what is shelling it, so a Sentinel parked
beside our own footprint out-damages four healers indefinitely.  This branch
lets one designated builder per near-Core enemy turret spend its action pecking
that turret instead of healing, but only while the repair line stays manned or
the turret is already nearly dead.  Everything else -- roles, economy, siege
planning, the interceptor and the saboteur -- is bit-for-bit _v70mh.

S4 variant: CHOKEPOINT WALLS ON KNOWN MAPS.  The pool terrain is embedded
(map_grid decoded at init), so on corridor maps the enemy's shortest approach
path is knowable at round 0.  Each builder plans, once at decode time, up to
CHOKE_MAX_TILES barrier sites at the narrowest tile of that path; the
role_n == 1 interceptor builds them during its idle time inside a bounded
round window.  Arithmetic: a barrier is 3 Ti / 30 HP, so clearing one costs a
rusher ~15 builder pecks (2 dmg each) or 5 gunner shots (7 dmg, 4 ammo each),
and the corridor gate guarantees walking around costs a real detour -- tens of
rounds of rush delay for under 10 Ti.  Everything else is bit-for-bit v8.
"""
import math
import random
from collections import deque

from fcode import Direction, EntityType, Environment, Position

DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]
CARDINALS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

MAX_BUILDERS = 5
EARLY_BUILDERS = 5
ECO_CAP = 18
ECO_NEED = 3
# BUILDER RESPAWN-ON-DEATH.  self.n counts builders SPAWNED over the match and
# is never decremented, so on its own it reads every death as the permanent
# loss of one seat.  Measured in the eider 1000-round titanium-race loss: three
# of our five builders were dead by round 413, and we then played 586 rounds on
# two live hands -- harvesters frozen at 10 for 559 rounds and 12,314 titanium
# unspent at the final bell.  The winner ran 16 spawns against 7 deaths and
# sustained 9-13 live builders throughout.
#
# _v69bc tested this together with an economy-scaled raise of the cap itself
# and measured -13 pts.  The lesson taken here is that the REPLACEMENTS were
# right and the early cap raise was not: builder bots are the joint most
# scale-expensive entity (+20% each), so raising the standing target inflates
# the cost curve from the opening onward, before any of it has been earned.
# So the live target stays at MAX_BUILDERS.  Replacements sit strictly on top
# of it and carry two extra gates the base spawns do not have -- a titanium
# floor and a minimum round -- which together leave the opening and the
# cost-scale profile of the first five spawns bit-for-bit untouched, and only
# ever convert genuinely surplus bank into labour.
#
# The Core has no getter for "live builder bots": its vision is r^2=36 while
# builders work far outside it, and the cost scale is one team-wide number
# that cannot be inverted into a count.  get_unit_count() is the only global
# signal and it lumps Core, builders and every turret together -- so we use its
# DROPS rather than its value.  A turret loss therefore also grants a phantom
# builder slot; that overshoot is bounded by REPLACEMENT_MAX and, thanks to the
# titanium floor, is only ever paid for while we are rich.
REPLACEMENT_MAX = 8
REPLACE_TI_FLOOR = 250
REPLACE_MIN_RND = 60
# Round at which a waiting raider stops waiting for an insertion.  One name for
# both the give-up and the re-recruit bound, so the two cannot disagree.
LAUNCH_GIVEUP_RND = 180
# A launchwait unit that has made no launch progress for this many rounds
# stops waiting, whatever the global clock says.  Bounds the waste that
# LAUNCH_GIVEUP_RND only caps at round 180 -- matches decided earlier never
# reached that bound at all.
LAUNCH_STALL_RNDS = 36
# Melee-before-repair for forward saboteurs is only worth it where a hostile
# gun can actually be walked up to.  Measured wall fractions of the 15 pool
# maps: drumlin 0.6%, meander 2.1%, eider 3.9%, hive 5.4%, atoll 5.6%,
# antler 7.1%, fjordgate 10.0%, snowflake 10.4%, nordkap 14.2%, moonrise
# 14.3%, jackpot 19.5%, heart 21.8%, lighthouse 25.0%, saga 28.5%,
# archipelago 30.8%.  1.5% sits in the drumlin/meander gap, the only break
# that isolates the near-wall-free map.
MELEE_FIRST_MAX_WALL_FRAC = 0.015

# SABOTEUR INTERCEPTION.  Measured in the post-heal-reflex rematch against The
# Flotte Experience (1745): a single enemy builder walked our economy from r16
# to r150+, destroying every harvester and conveyor we built, and was never
# once contested.  The melee recall in _builder only reaches bots within
# dist^2 <= 20 of our Core and no role pursues an intruder working farther out.
# Everything inside that radius stays with the existing recall and with the
# role_n == 4 defender's threat chase, so a launch-dropped raider beside the
# Core is never handled twice; the interceptor owns only the band beyond it.
INTRUDER_CORE_DSQ = 20
# Rounds an intruder may stay out of sight before the chase is abandoned.
INTRUDER_FORGET_RNDS = 8
# STALEMATE DISENGAGE (see _guard_target).  25 escort rounds of a building
# that never comes whole ≈ 25 Ti of heals on a 3-20 Ti building -- past its
# replacement price, the escort is paying ransom.  The ban is long because
# the measured stalemates ran 450-820 rounds: re-engaging after a short
# cooloff just resumes the same drain.
ESCORT_STALL_RNDS = 25
ESCORT_BAN_RNDS = 400
# MELEE FUTILITY LEDGER (E4, see _sabotage_prio).  Forensic ghost evidence
# (sporks_g5/fjordgate): one builder spent ~830 rounds and 865 melee swings
# x 2 Ti = 1730 Ti attacking a bait barrier that enemy builders healed 884
# times at 1 Ti / +4 HP -- an 8:1 titanium exchange against us
# (sporks_g2/moonrise similarly: ~710 swings, 4560 HP healed vs 1420 dealt).
# The escort (ESCORT_STALL_RNDS) and hunt (hunt_defer) ledgers already keep
# this score; ordinary melee did not.  8 consecutive no-progress hits is
# 16 Ti for zero net damage -- already past the 3 Ti replacement price of
# the barrier doing the baiting.  The ban is long for the same reason
# ESCORT_BAN_RNDS is: the measured stalemates ran 700-830+ rounds, so a
# short cooloff just resumes the same drain.
MELEE_FUTILE_HITS = 8
MELEE_FUTILE_BAN_RNDS = 300
# Hunt band past Sentinel range, footprint-measured (see _hunt_turret; the
# constant and its two validations -- the CtrlAltDefeat decode and the v79
# jackpot sweep -- are documented at the use site).
HUNT_BAND_DSQ = 41
# Ore step-off wall gate (see _expand; v79's constant, copied with his
# rationale): 80+ walls marks the corridor maps where ore-squatting becomes a
# permanent park.  heart 28x20 has 122; atoll, where squatting is GOOD, 18.
ORE_STEPOFF_MIN_WALLS = 80
# CHOKEPOINT WALLS (S4).  The corridor gate reuses ORE_STEPOFF_MIN_WALLS with
# its rationale unchanged: 80+ walls marks the maps where terrain funnels
# movement, and only there does a wall buy anything -- on open maps a 3 Ti
# barrier is walked around for free and the Ti is dead capital.  In a
# corridor the arithmetic is lopsided: each barrier is 3 Ti / 30 HP, so
# clearing one costs ~15 builder pecks (2 dmg each, one action per round) or
# 5 gunner shots (7 dmg, ceil(30/7) = 5) at 4 ammo apiece = 20 ammo, while
# the detour around it is whatever the corridor denies -- tens of rounds of
# rush delay for <= 9 Ti total.  The window is the rush window: before r30
# every Ti belongs to the first harvesters and links (the same opening-tempo
# lesson MEDIC_MIN_RND was floored on), and past ~r140 rushes are decided
# (HUNT_MIN_RND's measured bound: "a rush is decided before ~r120"), so a
# later wall delays nothing and only feeds the +1%/build cost scale.  The
# reserve keeps the spend from starving the eco bootstrap and the 1 Ti heal
# reflex -- same class of floor as SIEGE_HEAL_RESERVE_TI, sized to roughly
# one harvester (30 Ti) so a wall never displaces the next digger.
CHOKE_MIN_RND = 30
CHOKE_MAX_RND = 140
CHOKE_TI_RESERVE = 30
# Width and cap per the corridor arithmetic above: a passage of width <= 2
# is fully sealed by the choke tile plus at most 2 passable lateral
# neighbors, so 3 tiles (9 Ti) is the whole spend ceiling.
CHOKE_WIDTH_MAX = 2
CHOKE_MAX_TILES = 3

# TURRET-HUNTING UNDER SIEGE.  Measured in the hive core_destroyed@787 loss to
# kladde_probe: enemy Sentinels #354 (built r195 at (6,17)) and #446 (built
# r308 at (4,20), i.e. adjacent to our own Core footprint) fired 133 shots for
# 2,394 damage into a 500 HP Core, while our four converged healers landed 481
# heals for +1,890 HP and still lost the DPS race.  Repair alone cannot win it:
# a Sentinel is -9 HP/round sustained and a healer is +4.
#
# The damning detail is #446.  Our own defensive Sentinel had already ground it
# down to 4/40 HP by r328 -- two builder pecks from dead -- and we then kept a
# living builder at dist^2 = 2 from it for the next 283 rounds without ever
# attacking it once.  That is not an oversight in the melee code but a direct
# consequence of the heal-first ordering under shelling: the universal adjacent
# heal claims the action before any melee branch is reached, so no builder
# action is ever spent on a turret standing next to the Core it is killing.
#
# Scope.  This file already kills UNESCORTED turrets perfectly well wherever
# its melee path happens to face them -- two eider rush Sentinels dead by r100,
# hive #196 ground down in 19 rounds by a single builder -- so the feature is
# not "attack turrets".  The counter-example that draws the boundary is eider
# Sentinel #415: healer-escorted, it absorbed 630 damage and had 630 healed
# back, net zero, a pure titanium sink at 2 Ti per 2 damage.  Hunting an
# escorted FORWARD turret with one or two builders is therefore never worth it,
# and hunting stays inside the near-Core siege band -- INTRUDER_CORE_DSQ, the
# same radius the interceptor already treats as the Core's own business -- and
# never becomes a cross-map recall: a builder not already within
# HUNT_DESIGNATE_DSQ of a turret does not hunt it at all.
#
# Ownership is decided locally and deterministically: among the friendly
# builders within HUNT_DESIGNATE_DSQ of the turret (this unit included), the
# lowest entity id hunts.  No store slot is spent on it, so no builder write
# can clobber the Core's, and there is nothing to reset when the turret dies.
# Vision is not symmetric at that radius (two builders each within sqrt(8) of
# the turret can be dist^2 = 32 apart, past a builder's r^2 = 20 vision), so
# two units on opposite sides can each believe they are lowest; the bound on
# that misread is one extra peck per round, and the healer floor holds anyway.
#
# HUNT_MIN_HEALERS is the safety property that makes the whole thing sound:
# hunting is only ever allowed while at least that many OTHER friendly builders
# are visibly adjacent to the Core, so the repair line never thins to chase a
# gun.  The single exception is HUNT_FINISH_HP, a turret already inside four
# pecks of death, where removing its damage permanently beats four rounds of
# +4 HP by a wide margin -- the #446 case above, four rounds of work for 283
# rounds of silence.
HUNT_DESIGNATE_DSQ = 8
HUNT_MIN_HEALERS = 2
HUNT_FINISH_HP = 8
HUNT_FIRE_TI = 2
# DUEL DISCIPLINE (Piece D).  The melee arithmetic is not close: a builder
# peck is 2 damage a turn, a Gunner answers with 7 at reload 1.  A 40 HP
# builder therefore dies in ~6 rounds while the 25 HP Gunner needs ~13 hits
# to fall, so a LONE builder that opens a duel loses it and trades itself
# 1-for-1 at best.  Two independent replay decodes landed on the same leak
# today: our seat-B death trace has 8 of 11 attack-deaths as a single builder
# pecking a Gunner still sitting at 17-25/25 HP, and Ouroboros -- our worst
# per-team matchup at 1-14 lifetime -- recorded ~76 builder deaths across 13
# games, every single one to gunner fire and not one to melee.  Their whole
# plan is a creeping Gunner picket that farms exactly this duel.
#
# What the same replays say WORKS is volume: fjordgate, where several builders
# peck concurrently, landed 348 hits, ground the picket down, and we win that
# map.  So the rule is not "never melee turrets", it is "never melee one alone
# into a live gun".  The third exemption is the contrapositive of the trap-list
# principle _hunt_turret is already built on -- a turret firing at the Core is
# not firing at its adjacent attacker -- read from the attacker's side: a
# turret whose ray covers MY tile is killing me while I peck it, and one whose
# ray points elsewhere is free damage.  Toggle kept for the ablation matrix.
DUEL_DISCIPLINE_ON = True
# BALLOT DEADLOCK BREAKER.  Measured on the hive seed-1 rerun: the id ballot
# below elected u5 -- the role_n == 1 interceptor, which is role-gated out of
# hunting -- and every eligible unit deferred to it for 175 straight rounds
# (u7 to [5], u10 to [5,7], u206 to [5,7,10]; 481 candidate sightings, zero
# pecks) while the 4/40 HP sentinel shelled the Core to death.  Any local
# designation over visible mates has this failure: role is per-instance state
# other units cannot see, so the ballot sometimes elects a unit that will
# never act, and a siege is static, so "sometimes" means "for the rest of the
# match".  The repair is to defer only while deference is WORKING: if the
# candidate turret's HP has not dropped for this unit's own override window,
# the elected hunter is provably not hunting, and this unit stops honouring
# the ballot.  Windows are staggered by id so overrides fire one at a time --
# the first overrider's pecks resume the HP drop, which re-arms everyone
# else's deference.  An enemy-escorted turret healed as fast as it is pecked
# also reads as "no progress" and pulls in more attackers, which is exactly
# the >= 3 concurrent attackers the eider #415 escort lesson demands.
HUNT_DEFER_BASE = 3
HUNT_DEFER_SPREAD = 4
# CHAIN MEDIC constants (see the heal-in-passing block in _expand).  The
# floor keeps the opening honest: below it every titanium belongs to the
# first harvesters and links, and the medic reflex stays quiet.  Types are
# the economy pipeline only -- turrets/barriers are combat capital with
# their own defense logic, and the Core has the universal heal.
MEDIC_TI_FLOOR = 20
# Round floor, measured by ablation on the flotte_probe guard: with the medic
# live from the opening, fjordgate flipped A-core-kill@297 -> B-core-kill@138
# and lighthouse A-tiebreak@1000 -> B-core-kill@110 (the no-medic ablation
# restores both exactly; the no-surge ablation changes nothing).  An action
# spent patching a pecked conveyor in the opening is also a MOVE not taken
# (builder acting and moving are mutually exclusive per round), and on small
# maps that tempo is the whole game.  The churn the medic exists for is late
# -- the eider melee grind runs r180-999 -- so it keeps every measured gain
# with the opening left alone.  Same class logic as HUNT_MIN_RND.
MEDIC_MIN_RND = 150
MEDIC_TYPES = (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER)
# FARM-RAID MEDIC WINDOW.  MEDIC_MIN_RND assumes "the churn the medic exists
# for is late"; the decoded hive loss to kladde_probe refutes that assumption
# for raided maps.  The farm dies r63-390 -- 4 of 5 harvesters and ALL 28
# conveyors, ~1 conveyor per 10 rounds sustained for 330 rounds -- entirely or
# mostly inside the r0-150 window the medic cannot see, and the game is then
# lost 490-vs-4900 mined on the r1000 titanium tiebreak.  So the window opens
# early, but only for damage the ablation never measured.  The tempo tax that
# flipped fjordgate (A-core-kill@297 -> B-core-kill@138) and lighthouse
# (A-tiebreak@1000 -> B-core-kill@110) came from spending opening actions --
# and therefore opening MOVES -- on cosmetic 1-peck patches.  A raid that is
# actually clearing the farm reads differently: builder pecks are 2 dmg, so
# four accumulated pecks (8 HP down, i.e. a 20-HP conveyor at <= 12) is
# sustained attention on that tile, not a passer-by.  Depth is the
# discriminator; MEDIC_EARLY_MIN_DMG is the whole guard against re-creating
# the measured flips.  MEDIC_EARLY_MIN_RND sits after the bootstrap (first
# links exist, the hive raid starts r63), and MEDIC_EARLY_ON stays a plain
# toggle so the screening matrix can ablate this piece on its own.
MEDIC_EARLY_ON = True
MEDIC_EARLY_MIN_RND = 40
MEDIC_EARLY_MIN_DMG = 8

# LATE LABOR SURGE.  Measured with the chain medic in place, eider seed-1 vs
# kladde_probe: the leak is patched (collected 9390 -> 12720) and the bank
# finishes at 8,957 Ti UNSPENT while we field 8 units against the winner's
# 9-13 live builders all game.  Money stopped being the constraint; hands
# are.  _v69bc already measured the WRONG version of this (-13 pts): raising
# the standing target inflates the +20%/builder cost scale from the opening,
# before it has been earned.  The surge is the respawn lesson applied once
# more: strictly surplus bank, strictly late, bounded.  Both floors must
# hold, so the opening and mid-game spawn curve is bit-for-bit untouched --
# by round 300 every class of game is either decided (rushes), in its siege
# endgame (hunting/healing own the relevant actions), or an economy race, and
# only the last both reaches the Ti floor and profits from more hands.  The
# same gate raises the harvester ceiling: extra hands with nowhere to dig
# would just pave.
SURGE_TI_FLOOR = 1500
SURGE_MIN_RND = 300
SURGE_EXTRA = 5
SURGE_ECO_CAP = 24

# ROUND FLOOR.  Measured on fjordgate (10x10, everything inside the hunt band
# from round 0): as seat B vs band_probe, _v70mh WINS by core kill at r229 --
# its builders storm the enemy Core under the melee paths -- while this file
# without a floor DIES at r153, the same builders pecking 25-HP rush Gunners
# for 2 dmg a round instead.  Hunting exists for the siege classes, and their
# strikes all land late (kladde sentinels r195/r308, Lunds chip sieges
# r150-900), while a rush is decided before ~r120.  Below the floor the
# pre-existing rush machinery owns every action; a rush that morphs into a
# real siege simply meets the hunter when the clock passes it.
HUNT_MIN_RND = 120

# SIEGE SOLVENCY.  Decoded from the same hive core_destroyed@787 loss.  The
# Core's HP plateaued r196-644 while the four converged healers landed 481
# heals, and then healing STOPPED for 300 straight rounds (r300-599) with the
# bank pinned at 0-85 Ti.  Nothing was overspending on defense: the ECONOMY
# rebuild paths -- links, paves, harvester rebuilds, the launcher -- each
# spend down to bare cost with no reserve, so the 1 Ti heals found an empty
# till every round, and the collapse at r649-786 is simply where the enemy's
# ammo recovered against a Core nobody could afford to patch.  Two bodies of
# the same illness: money for HP, and money for hands (see the respawn floor
# in _core -- REPLACE_TI_FLOOR = 250 was unmeetable at a 2-12 Ti bank for 500
# rounds, so dead builders never came back and HUNT_MIN_HEALERS could never
# hold; 0 of 270 builder attacks all match landed within dsq <= 41 of our own
# Core).
#
# 4 converged healers x 1 Ti/round x the 4-round passive-income interval is
# the reserve; it also covers 8 HUNT_FIRE_TI pecks.  The Core's ammo
# conversion already keeps its own under-siege floor of 12 (ti_floor in
# _core) on exactly this reasoning -- this extends the same idea to the
# builder economy paths, and nothing else.
SIEGE_HEAL_RESERVE_TI = 16
# Ablation toggles for the screening matrix; screens flip them.
SIEGE_RESPAWN_ON = True
SIEGE_RESERVE_ON = True
SIEGE_RESPAWN_MIN_RND = 50

# B8 SENSING TIER (ported from v79/v82, off by default until its own screen).
# The headline of the port spec, and the reason this costs nothing: gun_sense
# and b_sense are NOT sensing radii.  Nothing in v79/v82 ever scans past a
# unit's own vision -- the loop in _builder is a bare get_nearby_entities()
# with no dist_sq, i.e. the builder's own r^2=20 disk.  They are
# CLASSIFICATION thresholds measured from OUR CORE ANCHOR, applied to
# sightings the builder already had and was throwing away.  Widening 64->100
# and 16->36 adds zero engine calls and zero new observations; it only decides
# how far from home an already-seen enemy still counts as "we are UNDER
# attack".  The gate is pure dimensions -- area >= 650 and square -- which in
# this pool is exactly archipelago and snowflake (both 26x26=676); the nearest
# maps below the line are drumlin/hive at 625, so there is no near-miss.
# Default OFF so it can be screened on its own leg.
B8_ON = False

# PIECE G -- DECISION NOISE.  A rated game is a pure function of (opponent,
# opp_version, map, our_version, our_seat); mapSeed does not vary it.  Three
# byte-identical replay pairs confirm it round-for-round.  Across 1160 rated
# games there were 48 identical-fingerprint repeats, of which 19 were games we
# had already LOST and lost again the same way -- ~61 Elo at +3.2 per coinflip
# converted -- concentrated on the Ouroboros pairing, which holds seat A
# against us in 13/13 platform matches, so we cannot shake the repeat by seat.
# External-meta precedent: RoboStac (1st, Code Royale) and delineate (1st,
# FC2022) both shipped deliberate decision noise for exactly this reason.
#
# Honest caveats.  Forward EV is small at pool level -- roughly 0.06 Elo/game
# at the historical 4.74% re-pair rate -- and any version bump resets the
# repeat groups anyway.  So this is cheap insurance plus a LOCAL-MEASUREMENT
# effect: per-game entropy breaks the seed-amplification collapse, letting our
# own offline batteries sample distinct games again, at the cost of exact
# paired-seed reproducibility (the property the spawn-dispersion sort below was
# written to preserve).  Default OFF so it is screened on its own leg.
NOISE_ON = False

# PIECE F -- PAVE TRAIL.  The pave in _move lays a conveyor on the tile AHEAD
# (nxt) facing nearest_cardinal(direction toward the Core anchor).
# nearest_cardinal collapses the diagonals (NE->E, SE->E, SW->S, NW->W), so on
# any diagonal approach the facing is pinned to ONE axis while _bfs_direction
# zig-zags across TWO.  Worked example, core anchor (0,0), builder walking
# (5,5)->W->(4,5)->N->(4,4)->W->(3,4)->N->(3,3): the facing is WEST at every
# one of those tiles, so (4,5) outputs to (3,5) and (3,4) outputs to (2,4) --
# neither tile is ever visited.  Every turn of the zig-zag strands a dead
# conveyor head: exactly 50% of the trail on any zig-zag walk.
#
# The price tag is directed connectivity, and it is the largest single number
# in the destroy-doctrine analysis.  docs/v79-analysis.md:178-179: directed-
# connected harvesters are atoll 2, heart 2, jackpot 2, meander 1, against
# 5/5/3/7 ALIVE -- and the delivery rates match the DIRECTED count to the
# decimal on two of three audited maps (atoll 5.00 Ti/rd = exactly two
# harvesters' throughput at directed=2; heart 5.00 the same).  Alive harvesters
# do not predict delivery; directed-connected ones do.  Heart going 2 -> 5
# directed is +3 x 2.5 Ti/rd x ~700 rounds ~= +5,000 Ti/game (upper bound: it
# assumes facing was the only break).
#
# The rule: pave the tile you just LEFT, facing the direction you just MOVED.
# A builder cannot build on its own tile, so "faces where I now stand" puts the
# conveyor BEHIND it and makes its output tile the one it now occupies -- the
# trail's next tile.  The chain then follows the walked path exactly, whatever
# the walk does.  One exception, the TERMINAL clause: at a tile adjacent to the
# footprint the old expression is correct precisely and only there, because
# there it aims into the Core; without it the trail's coreward END would be the
# one dead head, which is the worst possible place for it (it is the delivery
# point).  Net: zero dead heads on a trail that reaches the Core, exactly one
# (at the head) on a trail abandoned mid-walk, versus ~50% of all tiles today.
#
# Tempo is unchanged by construction: today's pave already builds before
# calling can_move, so the build blocks the move, _move returns False and _nav
# charges self.stuck.  The new rule costs the same one round per tile and
# inflates stuck identically -- this is a pure facing change, not a tempo one.
# Re-facing the wrong heads already standing (destroy + rebuild) is a separate
# follow-on and is deliberately NOT here.  Default ON; the ablation matrix
# flips it.
PAVE_TRAIL_ON = True

# DEFEND-ROLE REDUNDANCY.  Measured in the eider loss vs The Flotte Experience:
# the role_n == 4 defender is the ONLY unit that ever calls
# _try_counterbattery, so home turrets are its exclusive capability.  It died
# at round 36 charging a forward gunner and, with MAX_BUILDERS = 5 and no
# respawn, we then built no home turret for the remaining 252 rounds while
# 1124 titanium sat banked.  One designated successor takes the role over when
# the defender stops beating.
#
# The threshold is a compromise, not a proof: the defender writes its beat
# early in its own turn path, but an engine CPU interrupt kills a turn
# outright (it does not resume), so a merely stalled -- not dead -- defender
# also stops beating.  Six missed rounds is accepted as the point where "very
# likely dead" beats "possibly just slow": a live defender would have to lose
# seven consecutive turns to the 10 ms budget to be misread, and the cost of
# that misread is one extra defender, while the cost of missing a real death
# is every home turret for the rest of the match.
DEFEND_BEAT_STALE_RNDS = 6
# Successions before this round are suppressed: the defender is the 5th
# builder and does not exist yet in the opening, so early silence is expected
# rather than evidence of death.
DEFEND_BEAT_MIN_RND = 10

# PIECE H -- ENDGAME SPEND-SWITCH.  Tiebreak order after round 1000 is
# titanium DELIVERED -> harvesters ALIVE -> titanium STORED -> coinflip, so a
# bank held past ~r960 is the one resource that scores nothing: stored Ti only
# breaks a tie that delivered and harvesters both failed to break.  The T4 sim
# over the current line's r1000 losses flips 6/9 (+38.4 Elo equiv), and the
# real atoll case was delivered-TIED and lost by exactly ONE harvester.
#
# Two halves, and they compete for the same bank, so the split is explicit:
#  - CORE half: dump the bank into ammunition in one call (convert_ammo is
#    action-free, once per team per turn, amount uncapped, usable the same
#    turn) -- but only above a two-harvester reserve, and only while a live
#    friendly turret is actually visible to drink it.  Ammo scores in NO
#    tiebreak; converting with no gun standing would trade tiebreak-3 stored
#    titanium for nothing.  With a gun standing, 40 rounds of unrestricted
#    fire is a real shot at the enemy Core, which beats every tiebreak.
#  - BUILDER half: bypass _eco_spendable / _eco_cap and put a harvester on
#    ANY adjacent ore, and stop spending actions on the chain medic and on
#    link building (a link laid at r970 delivers ~nothing; a harvester built
#    at r999 still counts alive at r1000).
# Honest caveat carried from the T2xT4 intersection: several flippable games
# had ZERO builders alive at r960, so the builder half no-ops there -- by
# design, it degrades to the core half alone rather than misfiring.
#
# EIR 5.1: the core half's dump is CAPPED at burnable ammo.  Uncapped it was
# measured converting 14,634 Ti in one call, which is the whole of tiebreak #3
# traded for a magazine no gun can empty in forty rounds -- see the DUMP CAP
# block in _core for the arithmetic.
ENDGAME_SWITCH_ON = True
ENDGAME_RND = 960
# Last scored round (GameConstants.MAX_TURNS; GameConstants is not imported
# here).  Only used to size the endgame dump's remaining-rounds term.
LAST_RND = 1000

SLOT_ROLE_N = 0
SLOT_UNDER = 1
SLOT_ATK_RND = 2
SLOT_ENEMY_CORE = 3
SLOT_HARVESTERS = 4
SLOT_ECO_READY = 5
SLOT_LAUNCHER = 6
SLOT_HOME_GUN = 7
SLOT_DROPPED = 8
SLOT_LINKS_DONE = 9
SLOT_LAUNCH_ID = 10
SLOT_LAUNCH_RND = 11
SLOT_LAUNCHED_ID = 12
# DEFEND-ROLE HEARTBEAT.  Slot 13 was declared but never read or written by any
# ancestor of this file; reclaimed here rather than spending a new one.  Holds
# ``round + 1`` of the last turn the current defender ran, so the value is
# nonzero from round 0 onward and 0 unambiguously means "no defender has ever
# beaten" (the 5th builder does not exist for the first several rounds, and
# promoting on that silence would fire before the defender was ever spawned).
SLOT_DEFEND_BEAT = 13
SLOT_THREAT = 14
SLOT_SIEGE = 15

AMMO_FLOOR = 16
PRIMARY_SENTINEL = True
LAUNCHER_RESERVE = 80

# CPU budget bail-out threshold, in microseconds. Ported from bots/ladder1:
# the engine allows 10 ms CPU per unit per round and interrupts run()
# mid-statement, with no cleanup, if that is exceeded -- wasting the round
# and potentially leaving instance state half-updated. Bailing ourselves at
# 8 ms keeps the skip at a phase boundary this file chooses (always the
# lowest-priority remaining work), instead of the engine choosing.
#
# NOTE: ct.get_cpu_time_elapsed() reads 0 under local `fcode run`, even with
# --tle set (see docs/tooling.md) -- it only moves on ladder hardware. This
# guard is therefore a no-op in every local arena run; it exists for the
# real budget enforced on the platform.
CPU_BUDGET_US = 8000

# Competition-map Core anchors.  Several maps are mirror-symmetric rather than
# 180-degree symmetric, so ``(w-2-x, h-2-y)`` is not generally the enemy Core.
# The fallback keeps the bot usable on an unknown map.
CORE_PAIRS = (
    (18, 18, 2, 14, 14, 2), (26, 26, 3, 22, 21, 2),
    (21, 8, 0, 6, 19, 6), (16, 16, 2, 11, 12, 3),
    (12, 12, 1, 8, 9, 2), (20, 20, 2, 15, 16, 3),
    (25, 25, 2, 20, 21, 3), (16, 16, 0, 0, 14, 14),
    (28, 20, 2, 8, 24, 8), (14, 18, 2, 2, 2, 14),
    (24, 24, 2, 2, 20, 20), (24, 24, 2, 11, 20, 11),
    (16, 12, 4, 5, 10, 5), (22, 22, 2, 17, 18, 3),
    (10, 10, 1, 1, 7, 7), (20, 26, 2, 2, 2, 22),
    (12, 8, 0, 6, 10, 0), (25, 15, 0, 0, 0, 13),
    (21, 21, 2, 2, 2, 17), (11, 16, 0, 0, 9, 0),
    (24, 24, 2, 19, 20, 3),
    # Additional current ladder arenas recovered from submitted match replays.
    (21, 8, 5, 3, 14, 3), (26, 26, 5, 5, 19, 19),
    (10, 10, 2, 2, 6, 6), (16, 16, 3, 3, 11, 11),
    (14, 18, 6, 4, 6, 12), (20, 26, 9, 6, 9, 18),
    # Current weekly rotation, absent from the tables above (found 2026-08-06:
    # without these, known_map_for returns None and _plan_siege is disabled on
    # 5 of the 15 pool maps). eider and heart share dims AND anchors; their
    # terrain lives in EXTRA_MAP_CODES for runtime disambiguation.
    (28, 20, 7, 9, 19, 9), (25, 15, 11, 3, 11, 10),
    (25, 25, 5, 5, 18, 18), (24, 24, 4, 4, 18, 18),
)

# Exact competition terrain, packed three base-3 cells per character
# (empty=0, wall=1, ore=2).  The public map pool is fixed and downloadable;
# knowing its walls prevents greedy bots from walking into dead ends while the
# rotational fallback below still supports unseen maps.
MAP_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0"
MAP_CODES = {
    (18, 18, 2, 14, 14, 2): "AAAAAGAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAANNAAAABJAAAATCAAAASLAAAABJAAAANNAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAAGAAAAA",
    (26, 26, 3, 22, 21, 2): "AAAAGAAACAAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANNNNNBAAAAAAAAAAAAAAAAAAAAAGAACASAACAAAAAAAAAAAAAAAAAAJNNNNNAMNNNNEAAAAAAAAAAAAAAAAAAACAGAACASAAAAAAAAAAAAAAAAAAAAAANNNNNBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAACAASAAAAA",
    (21, 8, 0, 6, 19, 6): "JSBDJCBVKDQDKFDJDADBDBAAAAAJBVJABFJANMKENAADJABDAADCGSDA",
    (16, 16, 2, 11, 12, 3): "AADAAAAJAACGABCAAGDAAAAJAAAAABAAAAAAAMNTAAAAAGNNAAAAAAAABAAAADAAAAJSAAACBSACADAAAAJAAA",
    (12, 12, 1, 8, 9, 2): "AAAGAAGAAAAAAAAAAAAAASBAAJCAAAAAAAAAAAAAAGAAGAAA",
    (20, 20, 2, 15, 16, 3): "AAAAAAAAAAAAYASAAACAAAAAAAAAADAAAAAADAAAAAADAAAAAADAAAJACDAAEJACDAAAJACDJBAJACDAAAJAAAAAAJAAAAAAJAAAAAAJAAAAAAAAAAACAAGAYAAAAAAAAAAAAA",
    (25, 25, 2, 20, 21, 3): "AAAAAAAAJABDJABDAAAAAAAAAAAASAAAAAAAAAAAAABDJABDAAAAAAAAAAAASAAGAACAAAAAAAADJABDJABAAAAAAAAAAAAGAACAAAAAAAAAAACASAAAAAAAAAAAAABDJABDJAAAAAAAAACASAAGAAAAAAAAAAAAJABDJABAAAAAAAAAAAAGAAAAAAAAAAAAJABDJABDAAAAAAAAA",
    (16, 16, 0, 0, 14, 14): "ASBJYAAAABGJJEASAAJAASDADMAJAJABEBEEMAAJCAAAAFAAMJKBKBBDADAMJAJGAADAAGAJEDSABAAAYDAHAA",
    (28, 20, 2, 8, 24, 8): "AAAAAAAAAAAGAAAAGAAAAAAAAAAAAANNNNNBAAAAAAAAAAACBAAAAADGABAAAAAABAAAAAAAAAAAAAAAAAAAAAAGYSAAAAAAGGGGAAAAAAAAAAAAGAAAAAAASADAAAAAADAABAAAAADAAAAAAAAAAAAMNNNNEAAAAAAAAAAAAACAAAACAAAAAAAAAAA",
    (14, 18, 2, 2, 2, 14): "AAAAAASAAAAAACAAAAAAAAAAAAAAAAIAAAAASMNBNNNNJNEAAASAAYAAAAAAAAAAAAAAAAAAASAASAAAAAAA",
    (24, 24, 2, 2, 20, 20): "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJBAAAAAIAASCAAAIAAYCAAAAAAAAAAAAAAAAAAAAAAAAAAJASCABAAJASCABAAAAAAAAAAAAAAAAAAAAAAAAAASIAAYAAASCAAYAAAAAJBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    (24, 24, 2, 11, 20, 11): "AAAAAAAAAAAAAAAAASAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGAAAGAAAAAAGAAAJBAAAAAALTAAAAAAJBAAAAAAJBAAAAAAJBAAAAAAJBAAAAAALTAAAAAAJBAAAGAAAAAAGAAAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAACAAAAAAAAAAAAAAAAA",
    (16, 12, 4, 5, 10, 5): "AAAAAGAAAAYADABSJBMAEABAAJAAAAAAAAAAAABAAJAMAEJBCJADAIAAAAGAAIAA",
    (22, 22, 2, 17, 18, 3): "AAAAAAAAAAAAAGCAAAAAAAAAAAAAAAAAMAAAAAAPBAAAAAAAAEAAAAAAMCAAAAAMAAAAAAPBAAAASAAAAAAAGAAAAAWAAAAAAMAAAAAAOAAAAAAJBAAAAAAAAWAAAAAAMAAAAAAAAAAAAAAAAAAUAAAAAAAAAAAAAA",
    (10, 10, 1, 1, 7, 7): "AAAAAGAAAAAASASAAAGAGAAAAAASAAAAAA",
    (20, 26, 2, 2, 2, 22): "AAAAAAAASAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAGAAAAAAAAAAAAAAAAAAAAGAAACAAASAAAMEMNNJNNBNNEMNNJNNBNNEMNNJNAAACAAAACAASAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAASAAAAAAAAAAAAAAAACAAAAAAAAAAA",
    (12, 8, 0, 6, 10, 0): "NMNAEJMABCJASGCGGSGCABSJAEBMANEN",
    (25, 15, 0, 0, 0, 13): "AAJEAAAAAAA0AAAAAAAAAAAAAAAJEAAAAAAANAAAAGAAMBAAASWRNNNBANNNNNNNANNZONNNAJNAAJEAAAACAANAAAAGAAMBAAAAAAAAAAAAAAA0AAAAAAAMBAAAA",
    (21, 21, 2, 2, 2, 17): "AAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAGAAAAAAAAAAAAAACAGASAAAAAAAANJNQNBNAAAAAAAACAGASAAAAAAAAGAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAACAAAAAAAAAAA",
    (11, 16, 0, 0, 9, 0): "AMBAADAAABAJAJAJABADJAABDAFAVJAADDAAKAAAEAAJBAADB0JJ0ZFJNNA",
    (24, 24, 2, 19, 20, 3): "AAAAAAAAAAAAAAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJNNBAAAAJAABAAAAJYCBAAAAJAAAAAAAAAABAAAAJSIBAAAAJAABAAAAJNNBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGAAAAAAAAAAAAAA",
    # Current weekly rotation (meander, drumlin, saga), encoded from
    # maps/*.map26 with the same packing and round-trip verified.
    (25, 15, 11, 3, 11, 10): "ACCAAAAAAAGAAASAAAGAAAASAACAAAZAAAAAAAEAAACAJAAAAAAAGAAGAAAAAAAAAAAAACAACAAGAABAAAAAAAAAEAAASAAAJIAAASAAAAACAAGAAASAASSAAAAAA",
    (25, 25, 5, 5, 18, 18): "AAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAASAAAAGAAAAUAAAAACAGAAAAAAAAAAACASAAAAAAYAAASAAAACAAJCAADJAAAFAAACAAAGAAAYAAAAAAGAACAAAAAAAAAASAACAAAAGCAAASAAAAGAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAAAAA",
    (24, 24, 4, 4, 18, 18): "ENNBCMAMBNJBAAAACAAAAAAAEADAAMCMEADGJNNMEADAJNNMBAJBYIAABNJBSACAEAESAMAMEAWGAMAMBAACJKDJAASAIGAJBAGYACAABDKBSAAJEAEAGOAMEAEACMAMASACJBNJAAYIJBAJENNBADAMENNBGDAMESEAADAMAAAAAAASAAAAJBNJEAESJNNM",
}

# Some ladder arenas are absent from the downloaded public pool.  Two 26x26
# layouts intentionally share dimensions and Core anchors, so this stays a list
# and is disambiguated from the builder's visible terrain at runtime.
EXTRA_MAP_CODES = (
    ((21, 8, 5, 3, 14, 3), "JABAJABDDDGDDDJAAAAABDAAAAADGAAAAAGAAAUAAAJJAGABBHDDADDP"),
    ((26, 26, 5, 5, 19, 19), "ENNEANNENJEMBJNNKBSAAAAMAMEAEACAAAJBAAAAAAAMAAAGCMAMZBJEGNNENJAMBJNNKNCMYAAAAGEAESGSAAJBJBIAJBJBAGASAJAJAMASADAAAAAJAGAMADADAGASAAEAEASCEAEAAGSGJBJTAAAAYMAOENNEANADMKNNTJEAZNAMAUAAAMAAAAAAAAEAAAACJBJNAMAAAAGAENNEANJEMKNNBJNNKB"),
    ((26, 26, 5, 5, 19, 19), "AAAAAAAAAACAAAAAAGGAJADAAAAAMEANBACAAAAAJBASAAAAGJBAGAAGAAMTAJAAAAJJBAFABAABJSABABADSDSMAABJAAEAASAAAAAASAAAAAASAGAAAAAAGAAAAAAGAAJBADABAMGJGJAABABGDABAABJCAEDAAAADAGNAASAASAAESAAAAGAAEAAAAAACANBJNAAAAAJADASSAAAAAAACAAAAAAAAAA"),
    ((10, 10, 2, 2, 6, 6), "DAFAAAFASBAAABAAAAAABAAAHAJCAAJCJA"),
    ((16, 16, 3, 3, 11, 11), "ENAAJEMBAAEAASNMEASMBNAACAJBAAAMHJAAAAAAACYACAAAAAADSNAAAAEAACAMBNGAJNMHAAJBAANJEAAMKB"),
    ((14, 18, 6, 4, 6, 12), "ABAFAAGABAASJGAAABCAAJAAJADAAAAAASDAAAAAAAAAAAASDAAAAAAAADABAAAJAAAADGAAGDCAGABADAPA"),
    ((20, 26, 9, 6, 9, 18), "NBJAAMEAAAAAAAAAGAAGAAAAAAJADAAJAMEBAAMNTLAAABJADAAPAAAAAAAAAAAAAAJNADASNBAGSAAAGAAUAAACASGAAAAGSAAANBJAAOEAAAAAAAAAAAAABJAASBJYDAAJAMEBAAMNBJAAABAAAAAAAAAAGAAGAAAAAAJNADAANB"),
    # eider and heart (current rotation): same dims and Core anchors, so both
    # live here and known_map_for disambiguates from sensed terrain.
    ((28, 20, 7, 9, 19, 9), "AAACAACAAAGAAAAAAGAAAAAAAAAAAAASAGAAASAAJBJBAACAAJBAMAAAAALTAGECAAAABAAJAAAAAAGICAAAAAAAAAAAAAAAAGGAAAAACAAAAAGAACASCIAACAAAOAAWAAAAAJAAJAAAAAAJADAAAGAAAAAAAAGAAACAGAAAAAAAAAAAAAAAAAAAAAA"),
    ((28, 20, 7, 9, 19, 9), "AAAAAAAAAAAAACSAAAAAAAAAAAAAAAAMAMAAAAAAMBJEAAAAANW0NEAAAJNNBNNEAAANNAANNAAADAAAAABAAAAAAAAAAAABAAAAJAACAAAAAAAGANNBAANNBAMNNBJNNEAJANWSNEJAATANCOBGBALAJBJBATAADAEAEABAASJEAJEGAYAGSGGCGAI"),
)


def enemy_core_for(w, h, own):
    for mw, mh, ax, ay, bx, by in CORE_PAIRS:
        if w != mw or h != mh:
            continue
        if own.x == ax and own.y == ay:
            return Position(bx, by)
        if own.x == bx and own.y == by:
            return Position(ax, ay)
    return Position(max(0, w - 2 - own.x), max(0, h - 2 - own.y))


def known_map_for(w, h, own, ct=None):
    candidates = []
    for (mw, mh, ax, ay, bx, by), code in tuple(MAP_CODES.items()) + EXTRA_MAP_CODES:
        if w != mw or h != mh or (own.x, own.y) not in ((ax, ay), (bx, by)):
            continue
        cells = []
        for ch in code:
            val = MAP_ALPHABET.index(ch)
            for _ in range(3):
                cells.append(val % 3)
                val //= 3
        cells = cells[:w * h]
        candidates.append(tuple(
            "".join(".#o"[cells[y * w + x]] for x in range(w))
            for y in range(h)
        ))
    if not candidates:
        return None
    if len(candidates) == 1 or ct is None:
        return candidates[0]

    # The duplicate 26x26 layouts differ within initial builder vision.  Score
    # every sensed environment tile once; buildings and bots do not affect it.
    sensed = []
    try:
        for tile in ct.get_nearby_tiles():
            env = ct.get_tile_env(tile)
            char = "#" if env == Environment.WALL else ("o" if env == Environment.ORE_TITANIUM else ".")
            sensed.append((tile.x, tile.y, char))
    except Exception:
        return candidates[0]
    return min(candidates, key=lambda grid: sum(grid[y][x] != char for x, y, char in sensed))


def pack_pos(pos):
    return ((pos.x + 1) << 16) | (pos.y + 1)


def unpack_pos(val):
    if not val:
        return None
    return Position((val >> 16) - 1, (val & 0xFFFF) - 1)


def nearest_cardinal(d):
    return {
        Direction.NORTH: Direction.NORTH, Direction.NORTHEAST: Direction.EAST,
        Direction.EAST: Direction.EAST, Direction.SOUTHEAST: Direction.EAST,
        Direction.SOUTH: Direction.SOUTH, Direction.SOUTHWEST: Direction.SOUTH,
        Direction.WEST: Direction.WEST, Direction.NORTHWEST: Direction.WEST,
        Direction.CENTRE: Direction.NORTH,
    }[d]


def ring(origin, r=2):
    out = []
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx or dy:
                out.append(Position(origin.x + dx, origin.y + dy))
    return out


def core_tiles(o):
    return [o, Position(o.x + 1, o.y), Position(o.x, o.y + 1), Position(o.x + 1, o.y + 1)]


def dist_core(pos, o):
    return min(max(abs(pos.x - c.x), abs(pos.y - c.y)) for c in core_tiles(o))


def nearest_core_tile(pos, o):
    # Conveyor outputs are cardinal.  Chebyshev distance can prefer a diagonal
    # Core tile on a tie and rotate the last conveyor away from the receiver.
    return min(core_tiles(o), key=lambda c: abs(pos.x - c.x) + abs(pos.y - c.y))


class Player:
    def __init__(self):
        self.n = 0
        self.team = None
        self.core = None
        self.enemy = None
        self.mw = self.mh = 0
        self.role = "expand"
        self.tgt = None
        self.last = None
        self.stuck = 0
        self.wall = None
        self.ang = 0.0
        self.idx = 0
        self.role_n = 0
        self.link_queue = []
        self.link_source = None
        self.dropped = False
        self.map_grid = None
        self.map_walls = set()
        self.melee_first = False
        # PIECE F trail memory (see PAVE_TRAIL_ON).  Per unit instance, no
        # store slot: only this unit's own _move writes it and only its own
        # pave reads it.  pave_prev is the tile vacated by the last successful
        # move and pave_dir the direction of that move, so the conveyor laid on
        # pave_prev outputs onto the tile the unit now stands on.  pave_rnd is
        # the round the move happened; the pave accepts the pair ONLY at
        # pave_rnd == round - 1, which is exactly the mandated "cleared on any
        # round the unit does not move" invalidation, expressed lazily so it
        # also holds on the paths where _builder returns early, where the unit
        # moved outside _move, and where the turn is cut by the CPU guard.
        self.pave_prev = None
        self.pave_dir = None
        self.pave_rnd = -2
        # B8 sensing tier (see B8_ON).  Hoisted here and set once in
        # _builder's team-init block; v79 recomputes both per visible enemy
        # inside the loop, which is the same value every time.  The defaults
        # are today's literals, so a unit that never reaches the team-init
        # block behaves exactly as before.
        self.gun_sense = 64
        self.b_sense = 16
        self.map_ores = []
        self.ore_cursor = 0
        self.forward_guns = 0
        self.forward_barriers = 0
        self.siege_spot = None
        self.siege_approach = None
        self.siege_direction = None
        self.siege_type = None
        self.last_hp = None

        # Live-builder accounting, Core-only (see _core).  prev_units is the
        # unit count at the previous Core turn; lost_units the running total of
        # its drops over the match, i.e. how many units we know have died.
        self.prev_units = None
        self.lost_units = 0

        # Interception state, per unit instance -- no store slot is spent on
        # it because exactly one builder (role_n == 1) ever reads or writes it.
        self.chase_id = None
        self.chase_pos = None
        self.chase_seen = 0
        # Escort stalemate ledgers (see _guard_target): building id ->
        # consecutive not-whole escort rounds / ban-until round.
        self.escort_watch = {}
        self.escort_ban = {}

        # True while this expander is converging on a shelled Core (see the
        # MULTI-HEALER CONVERGENCE block in _expand).  Per unit instance, no
        # store slot: it is read and written only by its own unit, and only to
        # detect the falling edge so the expand machine gets a clean state back.
        self.converging = False

        # True while this builder owns a near-Core enemy turret (see the
        # TURRET-HUNTING UNDER SIEGE block above and _hunt_turret).  Per unit
        # instance for the same reason self.converging is: read and written only
        # by its own unit, and only to detect the falling edge -- when the
        # turret dies or leaves the band -- so the heal/converge machine gets a
        # clean state back instead of a stale turret tile in self.tgt.
        self.hunting = False

        # Per-turret deference ledger for the ballot deadlock breaker: turret
        # entity id -> [rounds deferred with no HP progress, last seen HP].
        # Same locality argument as self.hunting; pruned in _hunt_turret so it
        # cannot grow past the handful of turrets a siege ever parks near us.
        self.hunt_defer = {}

        # MELEE FUTILITY LEDGER (E4, see _sabotage_prio and the constants
        # block at the top of the file): building id -> [consecutive
        # no-progress hits, last seen HP, banned-until round].  Same
        # locality argument as hunt_defer -- only this unit's own melee
        # chooser reads or writes it -- and pruned in _sabotage_prio against
        # the currently visible building ids so it stays a handful of rows.
        self.melee_futile = {}

        # CHOKEPOINT WALLS (S4), planned once in _builder's map-decode
        # branch: 0-3 barrier sites at the narrowest tile of the enemy's
        # shortest approach path.  Per unit instance (every unit runs in its
        # own interpreter, and all 16 store slots are taken anyway); only
        # the role_n == 1 interceptor ever spends a turn on them.
        self.choke_tiles = []
        # True while the interceptor is walking/building the choke set, so
        # the falling edge can hand a CLEAN tgt/stuck back to the expand
        # machine -- same locality argument and same idiom as
        # self.converging.
        self.choke_active = False

        # Whether we've already reported a CPU-guard trip for this unit to
        # stderr. One line per unit lifetime so a chronically slow unit
        # can't flood the log (ported from bots/ladder1).
        self.reported_cpu = False

        # Whether we've already reported an escaped exception for this unit
        # (ported from bots/ladder1, v1 heritage). One traceback per unit
        # lifetime so a bug that fires every round can't flood stderr or burn
        # the CPU budget formatting tracebacks.
        self.reported_error = False

    def run(self, ct):
        # An exception that escapes run() makes the engine PERMANENTLY delete
        # this unit for the rest of the match. Catching it costs one round's
        # action instead; there is no situation where propagating is better.
        try:
            self._dispatch(ct)
        except Exception:
            if not self.reported_error:
                self.reported_error = True
                import sys
                import traceback
                traceback.print_exc(file=sys.stderr)

    def _dispatch(self, ct):
        e = ct.get_entity_type()
        if e == EntityType.CORE:
            self._core(ct)
        elif e == EntityType.BUILDER_BOT:
            self._builder(ct)
        elif e in (EntityType.GUNNER, EntityType.SENTINEL):
            self._turret(ct)
        elif e == EntityType.LAUNCHER:
            self._launcher(ct)

    def _cpu_exhausted(self, ct):
        """True once this unit's round has used CPU_BUDGET_US of its 10 ms
        budget. Ported from bots/ladder1.

        Callers bail out of remaining lower-priority work when this trips, so
        a round degrades at a boundary this file chooses instead of being
        truncated mid-statement by the engine. Reported once per unit to
        stderr -- print() is captured into the replay, not the console, so
        stderr is the only way to see this locally (see docs/tooling.md).
        """
        if ct.get_cpu_time_elapsed() < CPU_BUDGET_US:
            return False
        if not self.reported_cpu:
            self.reported_cpu = True
            import sys
            print(
                f"CPU-GUARD tripped: round={ct.get_current_round()} "
                f"elapsed_us={ct.get_cpu_time_elapsed()}",
                file=sys.stderr,
            )
        return True

    def _core(self, ct):
        p = ct.get_position()
        w, h = ct.get_map_width(), ct.get_map_height()
        if self.map_grid is None:
            self.map_grid = known_map_for(w, h, p, ct)
        if ct.read_store(SLOT_ENEMY_CORE) == 0:
            ct.write_store(SLOT_ENEMY_CORE, pack_pos(enemy_core_for(w, h, p)))

        under = False
        threat = None
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == ct.get_team():
                continue
            d = p.distance_squared(ct.get_position(eid))
            et = ct.get_entity_type(eid)
            if et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= 64:
                under = True
                threat = ct.get_position(eid)
                ct.write_store(SLOT_THREAT, pack_pos(threat))
                break
            if et == EntityType.BUILDER_BOT and d <= 16:
                under = True
                threat = ct.get_position(eid)
                ct.write_store(SLOT_THREAT, pack_pos(threat))
                break
        rnd = ct.get_current_round()
        hp = ct.get_hp()
        if self.last_hp is not None and hp < self.last_hp:
            under = True
        self.last_hp = hp
        if under:
            ct.write_store(SLOT_UNDER, 1)
            ct.write_store(SLOT_ATK_RND, rnd)
        else:
            last = ct.read_store(SLOT_ATK_RND)
            # Latch 35 -> 50 (borrowed from v79 after the atoll decode): a
            # harasser that parks JUST outside every trigger radius lets a
            # 35-round latch expire between pokes, collapsing the ammo
            # magazine to one sentinel shot while the bank holds thousands
            # (measured: 13 shots fired in 1000 rounds on 2,782 banked Ti).
            under = bool(last and rnd - last < 50)
            ct.write_store(SLOT_UNDER, 1 if under else 0)

        harv = ct.read_store(SLOT_HARVESTERS)
        if harv >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

        ti, ammo = ct.get_global_resources(), ct.get_global_ammo()

        # PIECE H, CORE HALF -- ENDGAME SPEND-SWITCH (see ENDGAME_SWITCH_ON).
        # Past ENDGAME_RND a banked titanium is the only resource on the board
        # that scores nothing: the tiebreak reads delivered, then harvesters
        # alive, then stored, so stored Ti decides only games the first two
        # already tied.  Ammunition scores in no tiebreak either -- which is
        # exactly why this fires ONLY with a live friendly turret in the
        # Core's own sight.  With a gun standing, 40 rounds of unrestricted
        # fire is a live shot at the enemy Core and beats every tiebreak;
        # with nothing to drink it, converting would burn tiebreak-3 stored
        # titanium for zero, so the bank is left alone.
        #
        # convert_ammo is action-free, once per team per turn, uncapped in
        # amount and usable the same turn, so this is one call and it never
        # costs a spawn.  The reserve is two harvesters at current scale, held
        # back for PIECE H's builder half: a harvester built at r999 is still
        # alive at r1000 and outranks stored titanium.  It runs BEFORE the
        # ordinary magazine block and suppresses it for this turn, so the
        # 16-per-turn drip cannot spend the single conversion first.
        #
        # EIR 5.1 DUMP CAP -- TIEBREAK #3 ARITHMETIC.  As shipped this converted
        # the WHOLE bank, measured at a single 14,634-Ti dump at exactly r960
        # (snowflake g2).  That is correct only when tiebreak #1 or #2 decides
        # the game, because ammunition scores in NO tiebreak and stored titanium
        # is #3: in a delivered-tied AND harvesters-tied endgame the uncapped
        # dump hands #3 to the opponent by zeroing our own side of it.  14,634
        # stored beats any bank they can hold; 14,634 converted loses to 1.
        #
        # So convert only what the guns can plausibly BURN before r1000.  A
        # Gunner is 4 Ti a shot on reload 1 (a shot every 2 rounds, 2 Ti/round),
        # a Sentinel 10 on reload 2 (every 3 rounds, 10/3 Ti/round); x1.5 margin
        # for the rounds a target actually presents itself gives
        #   cap = remaining * (3 * gunners + 5 * sentinels)
        # in whole integers.  One Gunner over the last 40 rounds is 120 Ti, one
        # Sentinel 200 -- against a 14,634 bank the rest simply stays stored and
        # keeps scoring.  Capping against the ammo we ALREADY hold rather than
        # dumping a flat amount is what makes it safe to re-evaluate every round
        # from r960 on: as the clock runs down the cap shrinks, so the arm tops
        # the magazine up early and then goes quiet by construction.  The dump
        # still owns ammo policy for the turn whenever it is live, so the
        # ordinary 16-per-turn drip below cannot push the magazine back over the
        # cap it just set.
        endgame_dumped = False
        if ENDGAME_SWITCH_ON and rnd >= ENDGAME_RND:
            guns, sents = self._core_turret_mix(ct)
            if guns or sents:
                endgame_dumped = True
                cap = (LAST_RND - rnd) * (3 * guns + 5 * sents)
                amt = min(ti - 2 * ct.get_harvester_cost(), cap - ammo)
                if amt > 0 and ct.can_convert_ammo(amt):
                    ct.convert_ammo(amt)
                    ti = ct.get_global_resources()
                    ammo = ct.get_global_ammo()

        # Keep only a small working magazine.  Conversion is action-free, so a
        # 60-round stockpile merely starves harvesters and counter-gunners.
        weapons = ct.read_store(SLOT_HOME_GUN)
        atoll_burst_magazine = (
            under and w == 18 and h == 18
            and (p.x, p.y) in ((2, 14), (14, 2))
        )
        hive_magazine = (
            weapons and w == 25 and h == 25
            and (p.x, p.y) in ((2, 20), (21, 3))
        )
        ammo_target = (
            256 if hive_magazine
            else (32 if atoll_burst_magazine else (24 if under else AMMO_FLOOR))
        )
        # Magazine scales with the guns that drink from it (borrowed from
        # v79): a fixed floor was refuted twice here (45.3%, 46.1%), but
        # those raised the target with ZERO turrets too -- the measured
        # failure is the opposite case, dry turrets on a full bank (atoll:
        # 122 Ti converted all match, 2,782 banked, 13 shots).  Four ammo
        # per gunner round is one shot each; 48 caps the magazine at a
        # dozen shots of reserve however many guns exist.
        if weapons:
            mag_cap = 72 if under else 48
            per_gun = 6 if under else 4
            ammo_target = max(ammo_target, min(mag_cap, per_gun * weapons))
        # PEACETIME AMMO FLOOR = HARVESTER RESERVE (E1).  Forensics on the
        # sporks_g2/moonrise ghost (2 of 3 salts lost): after an early
        # harvester wipe the standing-magazine top-up drained 522-739 Ti of
        # ammo over the game -- 13x what we mined in one salt -- pinning the
        # bank below the ~23 Ti scaled harvester rebuild price for 850
        # straight turns while the enemy had ZERO turrets alive;
        # pivot_g1/snowflake likewise burned 1,384 Ti of ammo before t350
        # while harvesters froze at 4 vs the ghost's 8 (a 300-turn-late eco
        # ramp lost by 2,300).  So the weapons-but-peaceful floor rises from
        # 12 to 46 (one scaled harvester + a couple of conveyor links),
        # letting the bank cross the rebuild price instead of being milked to
        # 12 forever.  Under active threat (`under`) nothing changes: sieges
        # keep their 12 floor and the whole magazine logic stays intact.
        ti_floor = 12 if under else (46 if weapons else 52)
        if not endgame_dumped and (under or weapons or harv >= 2) and ammo < ammo_target and ti > ti_floor:
            amt = min(24 if under else 16, ammo_target - ammo, ti - ti_floor)
            if amt >= 4 and ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                # Ammo conversion is action-free; keep evaluating the Core's
                # spawn/build priorities with the updated resource balance.
                ti = ct.get_global_resources()
                ammo = ct.get_global_ammo()

        snowflake_home_b = (
            w == 26 and h == 26 and p.x == 19 and p.y == 19
            and self.map_grid is not None and self.map_grid[0][0] == "."
        )
        nordkap_home_a = w == 20 and h == 26 and p.x == 9 and p.y == 6
        mature_cap = 4 if nordkap_home_a else (6 if snowflake_home_b else MAX_BUILDERS)
        spawn_cap = mature_cap if harv >= 1 else min(EARLY_BUILDERS, mature_cap)
        can_spend_spawn = ti >= ct.get_builder_bot_cost()

        # REPLACEMENT ACCOUNTING (see REPLACEMENT_MAX).  A decrease in the team
        # unit count between two Core turns is a unit that died, and each one
        # buys back one spawn above spawn_cap, REPLACEMENT_MAX for the whole
        # match.  The base spawns are untouched: the second clause is vacuously
        # true while self.n < spawn_cap, so the first five (four on nordkap,
        # six on snowflake) still spawn on exactly the old condition, at the
        # old rounds, against the old cost curve.  Only the ones ABOVE the cap
        # additionally require a healthy bank and a past-opening round.
        units = ct.get_unit_count()
        if self.prev_units is not None and units < self.prev_units:
            self.lost_units += self.prev_units - units
        self.prev_units = units
        spawn_budget = spawn_cap + min(REPLACEMENT_MAX, self.lost_units)
        # LATE LABOR SURGE (see the block by its constants): surplus-bank-only
        # extra seats.  The replacement clause below already demands
        # ti >= REPLACE_TI_FLOOR ∧ rnd >= REPLACE_MIN_RND for any spawn above
        # spawn_cap, which this gate strictly implies.
        if ti >= SURGE_TI_FLOOR and rnd >= SURGE_MIN_RND:
            spawn_budget += SURGE_EXTRA

        # SIEGE RESPAWN FLOOR (see SIEGE_HEAL_RESERVE_TI).  Under siege the
        # bodies ARE the heal line -- HUNT_MIN_HEALERS wants them standing
        # adjacent to the Core -- but that is exactly when REPLACE_TI_FLOOR is
        # least meetable: the decoded hive loss held a 2-12 Ti bank for 500
        # rounds against a 250 floor, so every dead builder stayed dead while
        # REPLACEMENT_MAX seats sat unused.  The third clause spends on a body
        # only out of money the heal line does not need this interval (builder
        # cost + the whole reserve), so bodies never steal heal money, and it
        # rides the same late/under-siege gates as the reserve itself.  `under`
        # is the Core's own fresh computation above, one round newer than the
        # buffered SLOT_UNDER any builder would read.  Base spawns
        # (self.n < spawn_cap) and the surge are untouched.
        if (
            self.n < spawn_budget
            and (
                self.n < spawn_cap
                or (ti >= REPLACE_TI_FLOOR and rnd >= REPLACE_MIN_RND)
                or (
                    SIEGE_RESPAWN_ON
                    and under
                    and rnd >= SIEGE_RESPAWN_MIN_RND
                    and ti >= ct.get_builder_bot_cost() + SIEGE_HEAL_RESERVE_TI
                )
            )
            and can_spend_spawn and ti >= ct.get_builder_bot_cost()
        ):
            cands = ring(p, 2)
            # Dead branch removed: a first-builder enemy-facing sort keyed on
            # SLOT_ENEMY_CORE, written and read in the same round-0 turn, so the
            # buffered store always unpacked None.  Activating it measured 41%.
            # Stable dispersion makes paired offline results reproducible.
            # PIECE G: one re-roll of the dispersion pattern per game, drawn
            # once per match from OS entropy (each game is a fresh interpreter).
            # Within-match stability is preserved -- units still coordinate
            # against a single fixed pattern for the whole match -- while
            # cross-game determinism is deliberately broken, so identical-key
            # ladder games diverge from the first spawn and chaos does the rest.
            # With NOISE_ON False the salt is 0 and the key is arithmetically
            # identical to the pre-Piece-G sort.  No per-turn cost.
            if not hasattr(self, "spawn_salt"):
                self.spawn_salt = random.Random().randrange(97) if NOISE_ON else 0
            cands.sort(key=lambda sp: ((sp.x * 17 + sp.y * 31 + self.n * 13 + self.spawn_salt) % 97, sp.y, sp.x))
            for sp in cands:
                if 0 <= sp.x < w and 0 <= sp.y < h and ct.can_spawn(sp):
                    ct.spawn_builder(sp)
                    self.n += 1
                    return

        # Cores cannot construct turrets; the defender consumes SLOT_THREAT and
        # owns all counterbattery placement.

    def _core_turret_mix(self, ct):
        """PIECE H -- which friendly Gunners/Sentinels are alive to drink ammo?

        Returns (gunners, sentinels).  Non-zero is the shipped live-turret GATE
        on the endgame dump, unchanged; the counts are the Eir 5.1 addition and
        size the dump (see the DUMP CAP block in _core).

        Called from _core only, so no band test is needed: the Core's own
        vision (r^2 = 36) already bounds it to the home cluster, which is where
        every counterbattery and home gun this file builds ends up.  A forward
        siege gun out of Core sight reads zero -- conservative in the right
        direction, since the endgame dump is spending tiebreak-3 stored
        titanium and should only do so on turrets we can actually see standing.
        SLOT_HOME_GUN cannot answer this: it is never decremented, so rubble
        and distant artillery both read as a live gun (see CB_OVER_HEAL_ON).

        Reads the team off the Controller rather than self.team: _core never
        populates self.team (it uses ct.get_team() inline throughout), so the
        cached attribute is None on the Core's own Player instance.
        """
        mine = ct.get_team()
        guns = sents = 0
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) != mine:
                    continue
                et = ct.get_entity_type(bid)
                if et == EntityType.GUNNER:
                    guns += 1
                elif et == EntityType.SENTINEL:
                    sents += 1
            except Exception:
                continue
        return guns, sents

    def _note_friendly_launcher(self, ct):
        if ct.read_store(SLOT_LAUNCHER):
            return
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                ct.write_store(SLOT_LAUNCHER, 1)
                return

    def _sync_harvesters(self, ct):
        if self.core is None:
            return
        p = ct.get_position()
        if p.distance_squared(self.core) > 64:
            return
        live = 0
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.HARVESTER:
                live += 1
        # A builder only sees a local slice of the map.  Never erase the global
        # lower bound merely because distant harvesters are outside its vision.
        if live > ct.read_store(SLOT_HARVESTERS):
            ct.write_store(SLOT_HARVESTERS, live)
        if live >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

    def _eco_spendable(self, ct, cost):
        """Economy funding check, siege-reserved (see SIEGE_HEAL_RESERVE_TI).

        Under siege the ECONOMY paths stop spending the last
        SIEGE_HEAL_RESERVE_TI, so the heal line and the hunt pecks always
        have a till to draw on.  Defense spending is deliberately NOT routed
        through here -- heals, pecks, counterbattery, barriers, the ammo
        conversion and the surge all keep spending to the last titanium,
        because the reserve exists FOR them.

        Both gates are load-bearing.  Sieges land late (the HUNT_MIN_RND
        class logic: kladde sentinels r195/r308, Lunds chip sieges r150-900,
        rushes decided before ~r120), so the round floor conjoined with
        SLOT_UNDER means the reserve can never tax the opening bootstrap --
        the failure the _v70ec reserve/rebuild-cap already measured, gating
        link spending inverted the income bootstrap, collected 9390 -> 3160
        -- nor any rush window.
        """
        ti = ct.get_global_resources()
        if (
            SIEGE_RESERVE_ON
            and ct.read_store(SLOT_UNDER) != 0
            and ct.get_current_round() >= HUNT_MIN_RND
        ):
            return ti >= cost + SIEGE_HEAL_RESERVE_TI
        return ti >= cost

    def _try_build_launcher(self, ct):
        """Only call from defend — claim store first to prevent multi-launcher."""
        if ct.read_store(SLOT_LAUNCHER):
            return False
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                ct.write_store(SLOT_LAUNCHER, 1)
                return False
        if ct.read_store(SLOT_HARVESTERS) < 1:
            return False
        if not self._eco_spendable(ct, ct.get_launcher_cost()):
            return False
        # Claim BEFORE build so later units this round skip
        ct.write_store(SLOT_LAUNCHER, 1)
        p = ct.get_position()
        for d in DIRECTIONS:
            bp = p.add(d)
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_launcher(bp):
                ct.build_launcher(bp)
                return True
        # Build failed — release claim so we retry next turn
        ct.write_store(SLOT_LAUNCHER, 0)
        return False

    def _builder(self, ct):
        p = ct.get_position()
        if self.team is None:
            self.team = ct.get_team()
            self.mw, self.mh = ct.get_map_width(), ct.get_map_height()
            # B8 sensing tier, decided once from dimensions alone -- no store
            # slot, no map decode, so it is safe this early in the turn.
            _big_square = self.mw * self.mh >= 650 and self.mw == self.mh
            self.gun_sense = 100 if (B8_ON and _big_square) else 64
            self.b_sense = 36 if (B8_ON and _big_square) else 16
            self.idx = ct.get_id() & 0xFF
            self.ang = (self.idx % 8) * (math.pi / 4)
            n = ct.read_store(SLOT_ROLE_N)
            self.role_n = n
            small = self.mw * self.mh <= 220
            if n == 0:
                self.role = "saboteur"
            elif n <= 3:
                self.role = "expand"
            elif n == 4:
                self.role = "defend"
            else:
                # Sixth and later builder -- a replacement for a dead unit.
                # Generic expander, deliberately: there is exactly one defend
                # seat (role_n == 4, with the role_n == 2 succession behind it)
                # and one interceptor seat (role_n == 1), and both are
                # single-occupancy by design -- a second defender would double
                # the counterbattery scan and a second interceptor would
                # abandon the economy in pairs.  The generic path is also where
                # the measured shortfall was: not enough hands laying
                # harvesters and conveyors.  This generalises the snowflake
                # role_n == 5 special case in _builder, which is now redundant
                # and left in place only as a no-op.
                self.role = "expand"
            ct.write_store(SLOT_ROLE_N, n + 1)

        if self.core is None:
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                    self.core = ct.get_position(eid)
                    break
        if self.core is None:
            return

        if self.map_grid is None:
            self.map_grid = known_map_for(self.mw, self.mh, self.core, ct)
            if self.map_grid is not None:
                self.map_walls = {
                    (x, y) for y, row in enumerate(self.map_grid)
                    for x, cell in enumerate(row) if cell == "#"
                }
                self.map_ores = [
                    Position(x, y) for y, row in enumerate(self.map_grid)
                    for x, cell in enumerate(row) if cell == "o"
                ]
                # Decided once, from the decoded grid: on an open map the
                # forward gun duel is won by shooting first, not repairing.
                # Unknown map (map_grid None) keeps the repair-first order.
                self.melee_first = (
                    len(self.map_walls) < MELEE_FIRST_MAX_WALL_FRAC * self.mw * self.mh
                )
                # CHOKEPOINT WALLS (S4), planned once per unit right here in
                # the decode branch, from the embedded terrain alone (see the
                # CHOKE_* constants for the 3 Ti -> ~15 pecks / 5 shots /
                # detour arithmetic).  self.enemy is normally still unknown
                # this early -- SLOT_ENEMY_CORE is only written on a live
                # sighting -- but a successful decode proves the anchor pair
                # is embedded: CORE_PAIRS carries every MAP_CODES and
                # EXTRA_MAP_CODES key, so enemy_core_for is exact on any
                # decoded map.  A live sighting, when one exists, still wins.
                if len(self.map_walls) >= ORE_STEPOFF_MIN_WALLS \
                        and not self._cpu_exhausted(ct):
                    ck_enemy = (
                        self.enemy if self.enemy is not None
                        else enemy_core_for(self.mw, self.mh, self.core)
                    )
                    # BFS enemy anchor -> our anchor over the decoded grid.
                    # Walls and both 2x2 Core footprints block; the path runs
                    # between the footprints' passable cardinal neighbors
                    # (the endpoints' neighbors stand in for the endpoints).
                    ck_blocked = set(self.map_walls)
                    ck_blocked.update((c.x, c.y) for c in core_tiles(self.core))
                    ck_blocked.update((c.x, c.y) for c in core_tiles(ck_enemy))
                    ck_parent = {}
                    ck_q = deque()
                    for c in core_tiles(ck_enemy):
                        for d in CARDINALS:
                            n = c.add(d)
                            key = (n.x, n.y)
                            if (
                                0 <= n.x < self.mw and 0 <= n.y < self.mh
                                and key not in ck_blocked and key not in ck_parent
                            ):
                                ck_parent[key] = None
                                ck_q.append(key)
                    ck_goals = set()
                    for c in core_tiles(self.core):
                        for d in CARDINALS:
                            n = c.add(d)
                            key = (n.x, n.y)
                            if (
                                0 <= n.x < self.mw and 0 <= n.y < self.mh
                                and key not in ck_blocked
                            ):
                                ck_goals.add(key)
                    ck_hit = None
                    ck_steps = 0
                    while ck_q:
                        cur = ck_q.popleft()
                        ck_steps += 1
                        # Same step-check pattern as _plan_siege's terrain
                        # flood: nothing has been written to
                        # self.choke_tiles yet, so bailing here leaves it
                        # empty -- a clean no-op, the feature simply stays
                        # off for this unit.
                        if ck_steps % 64 == 0 and self._cpu_exhausted(ct):
                            ck_hit = None
                            break
                        if cur in ck_goals:
                            ck_hit = cur
                            break
                        for d in CARDINALS:
                            n = Position(cur[0], cur[1]).add(d)
                            key = (n.x, n.y)
                            if (
                                key in ck_parent or key in ck_blocked
                                or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                            ):
                                continue
                            ck_parent[key] = cur
                            ck_q.append(key)
                    if ck_hit is not None:
                        ck_path = []
                        cur = ck_hit
                        while cur is not None:
                            ck_path.append(cur)
                            cur = ck_parent[cur]
                        ck_path.reverse()  # enemy side first, ours last
                        ck_on_path = set(ck_path)
                        # NO-WALL ZONES.  Never wall an ore tile (harvester
                        # sites are the economy) nor any tile cardinally
                        # adjacent to EITHER Core footprint: ours are the
                        # conveyor delivery / heal / battery seats (the same
                        # exclusion _try_screen applies), the enemy's are
                        # our own saboteurs' melee seats.
                        ck_ore = {(o.x, o.y) for o in self.map_ores}
                        ck_no = set()
                        for anchor in (self.core, ck_enemy):
                            for c in core_tiles(anchor):
                                for d in CARDINALS:
                                    n = c.add(d)
                                    ck_no.add((n.x, n.y))
                        # Walk the MIDDLE THIRD of the path from the enemy
                        # side: mid-path is where corridors pinch (both
                        # thirds near a Core fan out into its open yard),
                        # and the enemy-most qualifying tile forces the
                        # longest detour.
                        ck_third = len(ck_path) // 3
                        for i in range(ck_third, len(ck_path) - ck_third):
                            tx, ty = ck_path[i]
                            # Corridor width ~= 1 + count of passable
                            # orthogonal neighbors NOT on the path.
                            # Approximation, documented: it is not a true
                            # perpendicular measure -- it also counts
                            # dead-end side pockets and along-path kinks as
                            # width -- so it can only OVER-estimate.  A tile
                            # it calls <= CHOKE_WIDTH_MAX wide really is
                            # sealed by <= CHOKE_MAX_TILES barriers.
                            ck_lat = 0
                            for d in CARDINALS:
                                n = Position(tx, ty).add(d)
                                key = (n.x, n.y)
                                if (
                                    0 <= n.x < self.mw and 0 <= n.y < self.mh
                                    and key not in ck_blocked
                                    and key not in ck_on_path
                                ):
                                    ck_lat += 1
                            if 1 + ck_lat > CHOKE_WIDTH_MAX:
                                continue
                            if (tx, ty) in ck_ore or (tx, ty) in ck_no:
                                continue
                            # First qualifying tile is the choke.  Wall set:
                            # the choke tile plus its passable off-path
                            # lateral neighbors, capped at CHOKE_MAX_TILES,
                            # every tile re-checked against the no-wall
                            # zones above.
                            ck_walls = [Position(tx, ty)]
                            for d in CARDINALS:
                                n = Position(tx, ty).add(d)
                                key = (n.x, n.y)
                                if (
                                    len(ck_walls) < CHOKE_MAX_TILES
                                    and 0 <= n.x < self.mw and 0 <= n.y < self.mh
                                    and key not in ck_blocked
                                    and key not in ck_on_path
                                    and key not in ck_ore and key not in ck_no
                                ):
                                    ck_walls.append(n)
                            self.choke_tiles = ck_walls
                            break

        self._note_friendly_launcher(ct)

        # B8 phase 1b -- nearest-threat write.  The loop below has no break and
        # no ordering, so today the LAST qualifying sighting in iteration order
        # wins SLOT_THREAT.  At gun_sense 64 the candidates are all within 8
        # tiles of home and roughly interchangeable; at 100 a distant,
        # unanswerable sentinel can overwrite a near, actionable one every
        # round.  Store writes are buffered, so no cross-unit priority rule is
        # possible -- the fix has to be per-unit, and it is one list slot and
        # one comparison.  Under B8_ON we publish the sighting with the
        # smallest core-distance; UNDER/ATK_RND still latch on the first
        # qualifier.  With B8_ON off the old last-write-wins path is kept
        # byte-for-byte.
        _threat_best = None
        _threat_best_d = 0
        _threat_seen = False
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            et = ct.get_entity_type(eid)
            ep = ct.get_position(eid)
            if et == EntityType.CORE:
                self.enemy = ep
                ct.write_store(SLOT_ENEMY_CORE, pack_pos(ep))
            d = self.core.distance_squared(ep)
            if (et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= self.gun_sense) or (
                et == EntityType.BUILDER_BOT and d <= self.b_sense
            ):
                ct.write_store(SLOT_UNDER, 1)
                ct.write_store(SLOT_ATK_RND, ct.get_current_round())
                _threat_seen = True
                if B8_ON:
                    if _threat_best is None or d < _threat_best_d:
                        _threat_best, _threat_best_d = ep, d
                else:
                    ct.write_store(SLOT_THREAT, pack_pos(ep))
        if B8_ON and _threat_best is not None:
            ct.write_store(SLOT_THREAT, pack_pos(_threat_best))

        # L2 stale-threat hygiene -- clear a SLOT_THREAT sighting this builder
        # can SEE is gone.  Measured in pivot_g1/snowflake: between t=207 and
        # t=251 the defender built 6 gunners at (7,4)/(6,3)/(5,4) aimed at
        # approach lanes with ZERO enemies near our core -- SLOT_THREAT held a
        # long-dead sighting and the 50-round UNDER latch kept counterbattery
        # alive, converting ~120+ Ti into turrets aimed at nothing while the
        # opponent added harvesters.  Any builder whose vision (r^2=20) covers
        # the stale tile and finds no enemy gunner/sentinel/builder on it
        # writes the slot to 0; the write is buffered, so consumers see the
        # cleared slot one round later.  Gated on `not _threat_seen`: this
        # unit's OWN fresh write above is buffered too, and a trailing 0 would
        # clobber it (read_store still returns last round's stale tile).  Tile
        # getters raise GameError at the vision edge (see _hunt_turret's note),
        # so each is guarded; an unreadable tile counts as occupied -- fail
        # towards keeping the threat, never towards blinding the defender.
        if not _threat_seen:
            _stale = unpack_pos(ct.read_store(SLOT_THREAT))
            if _stale is not None and ct.is_in_vision(_stale):
                _stale_live = False
                try:
                    _tid = ct.get_tile_building_id(_stale)
                    if (
                        _tid is not None
                        and ct.get_team(_tid) != self.team
                        and ct.get_entity_type(_tid) in (
                            EntityType.GUNNER, EntityType.SENTINEL,
                        )
                    ):
                        _stale_live = True
                except Exception:
                    _stale_live = True
                if not _stale_live:
                    try:
                        _bot = ct.get_tile_builder_bot_id(_stale)
                        if _bot is not None and ct.get_team(_bot) != self.team:
                            _stale_live = True
                    except Exception:
                        _stale_live = True
                if not _stale_live:
                    ct.write_store(SLOT_THREAT, 0)


        self.enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        self._sync_harvesters(ct)

        # The Launcher acknowledges the exact bot it threw.  Without this
        # handshake, a short intermediate throw leaves a launch-wait bot trying
        # to walk home, and nearest-bot selection can steal the economy builder.
        if ct.read_store(SLOT_LAUNCHED_ID) == ct.get_id() + 1:
            self.dropped = True
            self.role = "saboteur"
            # PIECE F: a thrown bot's trail memory is arbitrarily far away --
            # it did not walk here.  can_build_conveyor would fail safe on
            # adjacency anyway, but a stale pave_prev burns an engine call
            # every round until the next move overwrites it.
            if PAVE_TRAIL_ON:
                self.pave_prev = None
                self.pave_dir = None
                self.pave_rnd = -2

        rnd = ct.get_current_round()

        # DEFEND-ROLE SUCCESSION.  Placed here, before every role override
        # below, so a promoted unit is indistinguishable from a natural
        # defender for the rest of this turn and every turn after it.
        #
        # Only role_n == 2 may promote: role_n == 1 is the interceptor and
        # role_n == 3 turns saboteur by design, so 2 is the one pure expander
        # that can be spared.  There is deliberately no chain -- if the
        # successor dies too, the capability is lost again; a second hop would
        # cost a third builder on a map where we are already losing units.
        #
        # Exactly-once falls out of the guards themselves: promotion sets
        # role_n = 4, and the `self.role == "expand"` test is false forever
        # after (the promoted unit is "defend"), so the branch cannot re-fire.
        # The role test also excludes the one way a role_n == 2 unit stops
        # expanding on its own -- being thrown by a Launcher, after which it is
        # a dropped saboteur deep in enemy ground and the worst possible
        # candidate to recall as a home defender.
        #
        # beat == 0 means no defender has ever beaten (see SLOT_DEFEND_BEAT):
        # that is the opening, not a death, so it never promotes.  The stored
        # value is round + 1, hence beat - 1 is the round the beat was written.
        if self.role_n == 2 and self.role == "expand" and rnd > DEFEND_BEAT_MIN_RND:
            beat = ct.read_store(SLOT_DEFEND_BEAT)
            if beat and rnd - (beat - 1) > DEFEND_BEAT_STALE_RNDS:
                self.role_n = 4
                self.role = "defend"
                # Hand a CLEAN state to the defend machine, exactly as
                # _intercept's disengage hands one back to _expand: self.tgt
                # still holds an expansion target and self.stuck counted
                # rounds walking to it.  link_queue is positional and survives
                # untouched -- _defend consumes it itself.
                self.tgt = None
                self.stuck = 0
                self.wall = None

        # The heartbeat is keyed on role_n rather than on identity, so the
        # successor takes over writing it the same turn it promotes.  Written
        # unconditionally and this early because every later path in _builder
        # can return before reaching the bottom.
        if self.role_n == 4:
            ct.write_store(SLOT_DEFEND_BEAT, rnd + 1)

        if (
            self.role_n == 3 and self.role == "expand"
            and self.mw == 20 and self.mh == 26
            and (self.core.x, self.core.y) == (9, 6)
        ):
            self.role = "defend"
        replay_snowflake = (
            self.role_n == 3
            and self.mw == 26 and self.mh == 26
            and (self.core.x, self.core.y) in ((5, 5), (19, 19))
            and self.map_grid is not None and self.map_grid[0][0] == "."
        )
        snowflake_attack_now = (
            replay_snowflake
            and (
                (self.core.x == 5 and self.core.y == 5)
                or rnd >= 8
            )
        )
        if self.role == "expand" and snowflake_attack_now:
            self.role = "saboteur"
        # The fourth macro engineer becomes a second attacker once the initial
        # four-harvester shell exists.  Two others continue scaling economy.
        if (
            self.role == "expand" and self.role_n == 3 and not self.link_queue
            and ct.read_store(SLOT_HARVESTERS) >= 4 and rnd >= 12
        ):
            self.role = "saboteur"

        if self.role == "launchwait":
            if self.dropped:
                self.role = "saboteur"
            elif rnd >= 70 and not ct.read_store(SLOT_LAUNCHER) and self.role_n != 5:
                self.role = "saboteur"
            elif rnd >= LAUNCH_GIVEUP_RND:
                self.role = "saboteur"
            elif rnd - getattr(self, "launchwait_rnd", rnd) >= LAUNCH_STALL_RNDS:
                self.role = "saboteur"
                self.launch_block_until = rnd + 12

        # A Launcher that arrives just after the normal waiting cutoff can
        # recruit one of the original insertion roles back from walking duty.
        # The bound matches the give-up above: at 180 the two fought each other
        # every round to r199, which made the give-up dead code entirely.
        if (
            self.role == "saboteur" and not self.dropped and self.role_n >= 3
            and rnd < LAUNCH_GIVEUP_RND and ct.read_store(SLOT_LAUNCHER)
            and ct.read_store(SLOT_DROPPED) < 3
            and rnd >= getattr(self, "launch_block_until", 0)
        ):
            self.role = "launchwait"
            self.launchwait_rnd = rnd

        # Advertise before the emergency home-defense return below.  Otherwise
        # a melee visitor can prevent an already-adjacent waiter from ever
        # becoming visible to the Launcher.
        if self.role == "launchwait":
            self._offer_launch(ct)

        if self.last == p:
            self.stuck += 1
        else:
            self.stuck = 0
            self.wall = None
        self.last = p

        # TURRET HUNT, AHEAD OF THE HEAL.  This is the only interception point
        # the feature needs: the universal adjacent heal immediately below is
        # what claims the action for a converged expander AND for the defender
        # (_defend's own `shelled and _heal_core` branch is belt-and-braces
        # behind it, and _rank2_hold/_home_defend are only reached after it),
        # so sitting one line above it guarantees the hunter check runs before
        # every heal call in the file without touching any of those branches.
        # Deliberately NOT gated on the action cooldown, unlike the heal: a
        # hunter that still has to walk one tile must be able to do that on a
        # round it cannot act, or it would converge back toward the Core on
        # every other round and never arrive.
        #
        # The falling edge mirrors _expand's `converging` reset exactly.
        # _hunt_turret owns self.hunting outright -- it clears it at the top of
        # every call and re-arms it only while it has a live target -- so
        # "was hunting, is not any more" is the turret dying or leaving the
        # band, and self.tgt (a turret tile the heal/expand machines would
        # never have chosen) plus the stuck counters are cleared here, this
        # same turn, before anything downstream reads them.
        was_hunting = self.hunting
        if self._hunt_turret(ct):
            return
        if was_hunting and not self.hunting:
            self.tgt = None
            self.stuck = 0
            self.wall = None

        # UNIVERSAL ADJACENT HEAL.  Measured over three replays vs 1650-1750
        # teams, heals delivered to our own Core: 0, 0, 82 (+328 HP -- and the
        # 82 was the one win, the siege was survived).  The only difference
        # was whether the single role_n == 4 defender happened to be free that
        # round: healing was a role, not a reflex.  Make it proximity work --
        # any builder standing beside the Core repairs it, before any
        # melee/sabotage short-circuit below can claim the action.
        # The gate is deliberately the loose one, SLOT_UNDER != 0, i.e. any
        # threat level including mere spawn-tile proximity noise.  Noise is
        # free here: can_heal() checks "there's actually damage to repair"
        # (docs/reference/official-tutorials.md), so it refuses a full-HP
        # Core and the 1 Ti is only ever spent when HP is genuinely missing.
        # And when HP is missing, 1 Ti for +4 HP outvalues any alternative
        # action taken under fire.  _heal_core walks the 2x2 footprint and
        # lets can_heal() enforce orthogonal adjacency, so a builder that is
        # merely near the Core is unaffected.  _builder is reached only for
        # EntityType.BUILDER_BOT (see _dispatch), so the Core -- a building,
        # which cannot heal -- never takes this path itself.
        if ct.get_action_cooldown() == 0 and ct.read_store(SLOT_UNDER) != 0:
            if self._heal_core(ct):
                return

        # Distance from home is not evidence of a Launcher drop: long economy
        # chains routinely travel farther than nine tiles.  Only the explicit
        # launch handshake above may convert an expander into a dropped raider.

        snowflake_home_b = (
            self.mw == 26 and self.mh == 26
            and self.core.x == 19 and self.core.y == 19
            and self.map_grid is not None and self.map_grid[0][0] == "."
        )
        hive_home_a = (
            self.mw == 25 and self.mh == 25
            and self.core.x == 2 and self.core.y == 20
        )
        if snowflake_home_b and self.role_n == 5 and self.role == "defend":
            self.role = "expand"
        if (
            ct.read_store(SLOT_UNDER)
            and (
                (hive_home_a and self.role_n in (1, 2, 3))
                or (snowflake_home_b and self.role_n == 4)
            )
        ):
            self.link_queue = []
            self._rank2_hold(ct)
            return

        # Keep the proven forward artillery on the three layouts where a
        # melee recall loses more pressure than it saves.  Other layouts may
        # recall a nearby idle raider when builders actually reach the Core.
        keep_artillery_forward = (
            (self.mw == 21 and self.mh == 8 and self.core.x == 5)
            or (
                self.mw == 20 and self.mh == 26
                and (self.core.x, self.core.y) in ((9, 6), (9, 18))
            )
            or (
                self.mw == 14 and self.mh == 18
                and (self.core.x, self.core.y) in ((6, 4), (6, 12))
            )
        )
        if self.role in ("saboteur", "launchwait") and self.core and not keep_artillery_forward and p.distance_squared(self.core) <= 25:
            melee = False
            for eid in ct.get_nearby_entities():
                if ct.get_team(eid) == self.team:
                    continue
                if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                    continue
                if self.core.distance_squared(ct.get_position(eid)) <= 20:
                    melee = True
                    break
            if melee:
                self._home_defend(ct)
                return

        # Phase boundary: everything above this point is sensing/bookkeeping
        # (role/team/core/map setup, launcher handshake, enemy detection,
        # the melee emergency check just above) and every self.* write in it
        # is a standalone assignment, never split across an engine call. If
        # that alone already used the budget, skip this unit's action/move
        # phase below instead of risking a truncation mid-build inside it
        # (siege planning, the counterbattery scan, and BFS nav all live
        # there). Emergency defense above (_rank2_hold, _home_defend) is
        # intentionally NOT gated by this -- it is the highest-priority work
        # a unit does, not the lowest.
        if self._cpu_exhausted(ct):
            return

        if self.role == "defend":
            self._defend(ct)
        elif self.role == "saboteur":
            self._saboteur(ct)
        elif self.role == "launchwait":
            self._launchwait(ct)
        else:
            self._expand(ct)

    def _home_defend(self, ct):
        """All hands: melee attackers, plant sentinel/barrier, heal Core."""
        p = ct.get_position()
        if ct.get_action_cooldown() == 0:
            if self._sabotage_prio(ct):
                pass
            elif self._try_counterbattery(ct):
                pass
            elif self._heal_core(ct):
                pass
        if ct.get_move_cooldown() != 0:
            return
        # Move onto enemy bots near Core
        threat = None
        best = 10**9
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            ep = ct.get_position(eid)
            if self.core.distance_squared(ep) > 36:
                continue
            d = p.distance_squared(ep)
            if d < best:
                best, threat = d, ep
        self.tgt = threat if threat is not None else self.core
        self._nav(ct, pave=False)

    def _rank2_hold(self, ct):
        """Map-gated ranged-battery response: return and repair the Core."""
        if ct.get_action_cooldown() == 0 and self._heal_core(ct):
            return
        if ct.get_move_cooldown() == 0:
            self.tgt = self.core
            self._nav(ct, pave=False)

    def _duel_safe(self, ct, tpos, tid):
        """True if melee-attacking the turret at tpos is a fight we may take.

        Safe iff any of: (a) it is nearly dead (HUNT_FINISH_HP -- finishing
        always pays); (b) a second friendly builder stands adjacent to it
        (volume wins the trade -- fjordgate's 348-hit grind); (c) its
        current firing ray does not cover this builder's tile (a turret
        shelling something else is free to peck -- the same fact
        _hunt_turret already exploits for Core-shelling turrets).
        Unknown/out-of-vision facing reads as UNSAFE.
        """
        if not DUEL_DISCIPLINE_ON:
            return True
        if tid is None:
            return True
        try:
            et = ct.get_entity_type(tid)
        except Exception:
            return False
        # Only guns duel back.  Everything else -- Core, harvester, conveyor,
        # barrier, Launcher -- is a free target and keeps its old priority.
        if et not in (EntityType.GUNNER, EntityType.SENTINEL):
            return True
        # (a) Four pecks or fewer from dead: finishing it always pays.
        try:
            if ct.get_hp(tid) <= HUNT_FINISH_HP:
                return True
        except Exception:
            pass
        # (b) Volume.  Any OTHER friendly builder already orthogonally on it
        # means the grind is shared and the trade flips our way.
        me = ct.get_id()
        for d in CARDINALS:
            n = tpos.add(d)
            if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                continue
            try:
                oid = ct.get_tile_builder_bot_id(n)
            except Exception:
                continue
            if oid is not None and oid != me:
                try:
                    if ct.get_team(oid) == self.team:
                        return True
                except Exception:
                    continue
        # (c) Ray test.  No readable facing (no direction, or out of vision)
        # is the unsafe answer: we cannot prove the gun is pointed away.
        try:
            facing = ct.get_direction(tid)
        except Exception:
            return False
        dx, dy = facing.delta()
        if dx == 0 and dy == 0:
            return True
        p = ct.get_position()
        # Attack radii squared: Gunner 13, Sentinel 32.  Both walks are <= 5
        # tiles, so this stays cheap enough for the hot path.
        rng = 32 if et == EntityType.SENTINEL else 13
        x, y = tpos.x, tpos.y
        while True:
            x += dx
            y += dy
            if not (0 <= x < self.mw and 0 <= y < self.mh):
                return True
            if (x - tpos.x) ** 2 + (y - tpos.y) ** 2 > rng:
                return True
            if x == p.x and y == p.y:
                return False
            if et == EntityType.SENTINEL:
                # The Sentinel line ignores obstacles, so nothing between us
                # can shield the peck -- keep walking to our own tile.
                continue
            n = Position(x, y)
            try:
                blocked = (
                    ct.get_tile_building_id(n) is not None
                    or ct.get_tile_builder_bot_id(n) is not None
                )
            except Exception:
                # Out of vision: assume something stands there and eats the
                # shot.  The Gunner's ray stops before reaching us.
                blocked = True
            if blocked:
                return True

    def _sabotage_prio(self, ct):
        p = ct.get_position()
        rnd = ct.get_current_round()
        # MELEE FUTILITY LEDGER (E4) prune, same idiom as the hunt_defer
        # prune in _hunt_turret: drop rows for ids no longer visible so the
        # dict stays a handful of entries.  A banned bait barrier we are
        # still standing next to remains visible, so its ban survives.
        vis = set(ct.get_nearby_buildings())
        for stale in [b for b in self.melee_futile if b not in vis]:
            del self.melee_futile[stale]
        best, best_p, best_bid = None, 99, None
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            bid = ct.get_tile_building_id(t)
            if bid is None or ct.get_team(bid) == self.team:
                continue
            # MELEE FUTILITY LEDGER (E4, constants at top of file): a target
            # that ate MELEE_FUTILE_HITS consecutive swings with no net HP
            # progress is being healed back as fast as we peck it.  Ghost
            # sporks_g5/fjordgate: 865 swings x 2 Ti = 1730 Ti into one bait
            # barrier healed 884 times at 1 Ti / +4 HP -- an 8:1 exchange
            # against us.  Skip it while banned so the loop falls through to
            # the next-priority target, exactly as the Piece D duel gate
            # below does.
            if self.melee_futile.get(bid, (0, None, 0))[2] > rnd:
                continue
            et = ct.get_entity_type(bid)
            pr = {
                EntityType.GUNNER: 0, EntityType.SENTINEL: 0,
                EntityType.CORE: 1, EntityType.HARVESTER: 2,
                EntityType.LAUNCHER: 3, EntityType.CONVEYOR: 4,
                EntityType.SPLITTER: 4, EntityType.BARRIER: 5,
            }.get(et, 6)
            if et in (EntityType.GUNNER, EntityType.SENTINEL) and not self._duel_safe(ct, t, bid):
                # Piece D: a duel we would lose alone.  Skip the candidate
                # entirely so the loop falls through to the next-best target
                # (Core, harvester, conveyor, ...) instead of trading 1-for-1.
                continue
            if pr < best_p and ct.can_fire(t):
                best_p, best, best_bid = pr, t, bid
        if best is not None:
            ct.fire(best)
            # MELEE FUTILITY LEDGER (E4) update: post-swing HP against the
            # HP recorded after our previous swing.  >= means healed back or
            # unchanged -- no net progress; MELEE_FUTILE_HITS such hits in a
            # row is 16 Ti spent for zero net damage, so ban the id for
            # MELEE_FUTILE_BAN_RNDS and clear the counter.  Any HP drop is
            # real progress and resets the count.  The HP read is guarded
            # like every other out-of-vision getter: on GameError the ledger
            # is left unchanged.
            try:
                hp = ct.get_hp(best_bid)
            except Exception:
                hp = None
            if hp is not None:
                hits, last_hp, ban = self.melee_futile.get(best_bid, [0, None, 0])
                if last_hp is not None and hp >= last_hp:
                    hits += 1
                else:
                    hits = 0
                if hits >= MELEE_FUTILE_HITS:
                    self.melee_futile[best_bid] = [0, hp, rnd + MELEE_FUTILE_BAN_RNDS]
                else:
                    self.melee_futile[best_bid] = [hits, hp, ban]
            return True
        return False

    def _launchwait(self, ct):
        p = ct.get_position()
        mine = ct.get_id() + 1
        chosen = self._offer_launch(ct)
        if ct.get_action_cooldown() == 0:
            if ct.read_store(SLOT_UNDER):
                self._sabotage_prio(ct)

        if ct.get_move_cooldown() != 0:
            return
        if chosen == mine:
            for eid in ct.get_nearby_buildings():
                if ct.get_team(eid) == self.team and ct.get_entity_type(eid) == EntityType.LAUNCHER:
                    # Path to any cardinal pickup cell around the occupied
                    # Launcher tile; only the explicitly claimed raider stages.
                    self.tgt = ct.get_position(eid)
                    self._nav(ct, pave=False)
                    return
        if p.distance_squared(self.core) > 12:
            self.tgt = self.core
        elif self.tgt is None or p == self.tgt or self.stuck >= 2:
            self.ang = (self.ang + 1.1) % (2 * math.pi)
            self.tgt = Position(
                max(0, min(self.core.x + int(2 * math.cos(self.ang)), self.mw - 1)),
                max(0, min(self.core.y + int(2 * math.sin(self.ang)), self.mh - 1)),
            )
        self._nav(ct, pave=False)

    def _offer_launch(self, ct):
        """Claim the single insertion slot and refresh it as a heartbeat."""
        mine = ct.get_id() + 1
        chosen = ct.read_store(SLOT_LAUNCH_ID)
        chosen_rnd = ct.read_store(SLOT_LAUNCH_RND)
        if chosen in (0, mine) or ct.get_current_round() - chosen_rnd > 4:
            ct.write_store(SLOT_LAUNCH_ID, mine)
            ct.write_store(SLOT_LAUNCH_RND, ct.get_current_round())
            return mine
        return chosen

    def _plan_siege(self, ct):
        """Choose a reachable tile whose weapon ray intersects the enemy Core."""
        if self.map_grid is None or self.enemy is None:
            return False
        cap = 3 if self.role_n == 0 else 2
        if self.forward_guns >= cap:
            return False
        if self.forward_guns >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED:
            return False

        # Everything from here on is the expensive part of this function: a
        # full terrain flood plus a nested candidate search below. Nothing
        # has been written to self.siege_* yet (that only happens at the very
        # end, once a candidate is chosen), so bailing here is a clean no-op
        # -- identical in effect to the existing "no candidates found" path.
        if self._cpu_exhausted(ct):
            return False

        turret_type = (
            EntityType.SENTINEL
            if PRIMARY_SENTINEL and self.role_n == 0 and self.forward_guns == 0
            else EntityType.GUNNER
        )
        ranges = (5, 4) if turret_type == EntityType.SENTINEL else (3, 2)
        p = ct.get_position()
        blocked = set(self.map_walls)
        blocked.update((c.x, c.y) for c in core_tiles(self.core))
        blocked.update((c.x, c.y) for c in core_tiles(self.enemy))
        blocked.discard((p.x, p.y))

        # One terrain flood supplies a real route distance to every candidate;
        # this avoids choosing a geometrically close ray on the far side of a wall.
        dist = {(p.x, p.y): 0}
        q = deque([(p.x, p.y)])
        siege_bfs_steps = 0
        while q:
            x, y = q.popleft()
            siege_bfs_steps += 1
            if siege_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                # Abandon planning for this round rather than run the
                # candidate search below on a starved budget. self.siege_*
                # is still untouched, so this is the same clean no-op as
                # the guard above.
                return False
            for d in CARDINALS:
                n = Position(x, y).add(d)
                key = (n.x, n.y)
                if (
                    key in dist or key in blocked
                    or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                ):
                    continue
                dist[key] = dist[(x, y)] + 1
                q.append(key)

        reserved = unpack_pos(ct.read_store(SLOT_SIEGE))
        candidates = []
        seen = set()
        for target in core_tiles(self.enemy):
            for facing in DIRECTIONS:
                unit = Position(0, 0).add(facing)
                max_range = ranges[0] if facing in CARDINALS else ranges[1]
                for ray_len in range(max_range, 0, -1):
                    spot = Position(
                        target.x - unit.x * ray_len,
                        target.y - unit.y * ray_len,
                    )
                    skey = (spot.x, spot.y)
                    if (
                        not (0 <= spot.x < self.mw and 0 <= spot.y < self.mh)
                        or self.map_grid[spot.y][spot.x] != "."
                        or skey in blocked
                        or (
                            self.role_n != 0 and reserved is not None
                            and spot.x == reserved.x and spot.y == reserved.y
                        )
                    ):
                        continue
                    # A wall anywhere before the Core makes a gunner ray inert.
                    if any(
                        (spot.x + unit.x * step, spot.y + unit.y * step) in self.map_walls
                        for step in range(1, ray_len)
                    ):
                        continue
                    if ct.is_in_vision(spot) and ct.get_tile_building_id(spot) is not None:
                        continue
                    # Construction is cardinal-adjacent only.  A diagonal
                    # approach looks close but leaves the engineer idling
                    # forever because every can_build_* call remains false.
                    for ad in CARDINALS:
                        approach = spot.add(ad)
                        akey = (approach.x, approach.y)
                        key = (skey, akey, facing)
                        if (
                            key in seen or akey not in dist
                            or approach == spot
                            or akey in blocked
                        ):
                            continue
                        seen.add(key)
                        # Stand behind or beside the weapon, never in its ray.
                        ray_penalty = 20 if ad == facing else 0
                        terrain_penalty = 2 if self.map_grid[approach.y][approach.x] == "o" else 0
                        candidates.append((
                            dist[akey] + ray_penalty + terrain_penalty,
                            -ray_len, spot.x, spot.y, approach.x, approach.y,
                            spot, approach, facing,
                        ))
        if not candidates:
            return False
        candidates.sort(key=lambda row: row[:6])
        pick = 0 if self.role_n == 0 else min(2, len(candidates) - 1)
        row = candidates[pick]
        self.siege_spot, self.siege_approach, self.siege_direction = row[6:9]
        self.siege_type = turret_type
        return True

    def _try_siege_build(self, ct):
        if self.siege_spot is None and not self._plan_siege(ct):
            return False
        p = ct.get_position()
        spot = self.siege_spot
        if ct.is_in_vision(spot) and ct.get_tile_building_id(spot) is not None:
            self.siege_spot = self.siege_approach = self.siege_direction = self.siege_type = None
            return False
        if max(abs(p.x - spot.x), abs(p.y - spot.y)) > 1 or p == spot:
            return False
        built = False
        if (
            self.siege_type == EntityType.SENTINEL
            and ct.get_global_resources() >= ct.get_sentinel_cost()
            and ct.can_build_sentinel(spot, self.siege_direction)
        ):
            ct.build_sentinel(spot, self.siege_direction)
            built = True
        elif (
            self.siege_type == EntityType.GUNNER
            and ct.get_global_resources() >= ct.get_gunner_cost()
            and ct.can_build_gunner(spot, self.siege_direction)
        ):
            ct.build_gunner(spot, self.siege_direction)
            built = True
        if built:
            self.forward_guns += 1
            ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
            if self.role_n == 0 and self.forward_guns == 1:
                ct.write_store(SLOT_SIEGE, pack_pos(spot))
            self.siege_spot = self.siege_approach = self.siege_direction = self.siege_type = None
            return True
        return False

    def _saboteur(self, ct):
        p = ct.get_position()
        ec = self.enemy or Position(self.mw // 2, self.mh // 2)

        if ct.get_action_cooldown() == 0:
            # Open maps only: melee a mid-map gun before spending the turn on
            # siege repair.  Wall-heavy maps keep the repair-first order.
            if self.melee_first and self._sabotage_prio(ct):
                return
            primary = unpack_pos(ct.read_store(SLOT_SIEGE))
            try:
                can_repair = primary is not None and ct.can_heal(primary)
            except Exception:
                can_repair = False
            if can_repair:
                ct.heal(primary)
                return
            # Persistent ray damage comes before low-value melee.  Once every
            # planned battery tile is occupied, clear hostile guns/economy.
            if self._try_siege_build(ct):
                return
            if not self.melee_first:
                self._sabotage_prio(ct)

        # Action phase over -- _try_siege_build either finishes its build and
        # the matching state update atomically and returns, or changes
        # nothing, so nothing here is half-set. Check before planning the
        # next siege spot and navigating below: both run their own BFS.
        if self._cpu_exhausted(ct):
            return

        if ct.get_move_cooldown() != 0:
            return

        if self.siege_spot is None:
            self._plan_siege(ct)
        if self.siege_approach is not None:
            if self.stuck >= 3:
                self.siege_spot = self.siege_approach = self.siege_direction = self.siege_type = None
                self._plan_siege(ct)
            self.tgt = self.siege_approach or ec
        elif self.forward_guns >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED:
            self.tgt = p
        else:
            self.tgt = ec
        self._nav(ct, pave=False)

    def _eco_cap(self, ct):
        """ECO_CAP, surge-raised under the LATE LABOR SURGE gate (see its
        constants block): strictly-surplus bank, strictly late, so the normal
        harvester ceiling and its +5%/build scale curve are untouched in any
        game the surge does not reach."""
        if (
            ct.get_global_resources() >= SURGE_TI_FLOOR
            and ct.get_current_round() >= SURGE_MIN_RND
        ):
            return SURGE_ECO_CAP
        return ECO_CAP

    def _turret_on_harvester(self, ct, bp, et=None):
        """True if an enemy turret at bp is parked on a friendly HARVESTER
        (the eco-siege trigger; see the TWO HUNT MODES comment in
        _hunt_turret).  Widened from strict orthogonal adjacency to dsq <= 8:
        the decoded jython_g1 saga ghost game shows a gunner two tiles from
        our harvester farming EIGHT rebuild-die cycles (t=774-837) without
        ever qualifying under the adjacency test.  A gunner's range is dsq 13;
        a turret within dsq 8 of a harvester is besieging it, not passing by.
        Tiles near a visible turret can still sit outside our own vision, so
        every lookup fails safe to False."""
        # The widened band only opens past the rush window: ambient early
        # hunting is twice-refuted (eider 8/16 -> 0/16, fjordgate rush), and
        # the measured farming loops run r46-r837.  Strict orthogonal
        # adjacency keeps its any-round trigger (the meander r69 case).
        # GUNNER-ONLY: a 40 HP healer-backed Sentinel is an unwinnable melee
        # grind -- snowflake/175455793-B measured 988 pecks over 265 turns
        # with the economy frozen at 3 harvesters, losing a 1000-turn TI race
        # by 10.  Sentinels keep the strict-adjacency trigger only.
        wide = et != EntityType.SENTINEL and ct.get_current_round() >= 40
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                dsq = dx * dx + dy * dy
                if dsq > 8 or (not wide and dsq > 1):
                    continue
                n = Position(bp.x + dx, bp.y + dy)
                if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                    continue
                try:
                    nid = ct.get_tile_building_id(n)
                except Exception:
                    continue
                if (
                    nid is not None
                    and ct.get_team(nid) == self.team
                    and ct.get_entity_type(nid) == EntityType.HARVESTER
                ):
                    return True
        return False

    def _harvester_site_safe(self, ct, bp):
        """False if a visible enemy GUNNER covers the would-be harvester tile.

        The other half of the jython_g1 lesson: the expander rebuilt the same
        farmed harvester eight times at 20+scaled Ti each, feeding the gunner
        instead of starving it.  Gunner range is dsq 13; building inside it
        is buying the enemy a target.  Two deliberate limits, both from the
        v3 rush_hold regression (24/30 -> 18/30, one lighthouse game at ZERO
        mined over 989 turns): the FIRST harvester is never blocked -- some
        income under fire beats none -- and Sentinels are ignored (range 32
        covers every practical site, so "safety" from one is just eco
        starvation with extra steps).
        """
        if ct.read_store(SLOT_HARVESTERS) < 1:
            return True
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) == self.team:
                    continue
                if ct.get_entity_type(bid) != EntityType.GUNNER:
                    continue
                gp = ct.get_position(bid)
                if gp.distance_squared(bp) > 13:
                    continue
                # RAY, NOT DISC.  A gunner threatens only along its facing
                # line (rotation costs 10 Ti + a cooldown).  The disc version
                # measured -5790 mined on archipelago/428452902-A: one gunner
                # at (10,9) "blocked" three sites a full quadrant apart and
                # froze us at 6 harvesters against 14.  can_fire_from cannot
                # test an EMPTY tile (gunner targets must be occupied), so
                # alignment is computed directly: collinear with the facing
                # (cross product zero) and in front of it (dot positive).
                # Unreadable facing fails safe to unsafe.
                try:
                    fdx, fdy = ct.get_direction(bid).delta()
                except Exception:
                    return False
                ddx, ddy = bp.x - gp.x, bp.y - gp.y
                if ddx * fdy != ddy * fdx or ddx * fdx + ddy * fdy <= 0:
                    continue
                return False
            except Exception:
                continue
        return True

    def _eco_besieged(self, ct):
        """Any visible enemy turret point-blank on a friendly harvester."""
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == self.team:
                continue
            bet = ct.get_entity_type(bid)
            if bet not in (EntityType.GUNNER, EntityType.SENTINEL):
                continue
            if self._turret_on_harvester(ct, ct.get_position(bid), bet):
                return True
        return False

    def _healer_floor(self, ct):
        """HUNT_MIN_HEALERS, scaled down for cornered cores (see the healer
        floor comment in _hunt_turret).  Counts the in-bounds orthogonal
        neighbours of the 2x2 footprint once per call -- eight for an
        interior core, as few as four in a corner -- and demands 2 standing
        healers only when at least six seats exist."""
        seats = 0
        seen = set()
        for c in core_tiles(self.core):
            for d in CARDINALS:
                n = c.add(d)
                if (n.x, n.y) in seen:
                    continue
                seen.add((n.x, n.y))
                if 0 <= n.x < self.mw and 0 <= n.y < self.mh and dist_core(n, self.core) > 0:
                    seats += 1
        return HUNT_MIN_HEALERS if seats >= 6 else 1

    def _heal_core(self, ct):
        for tile in core_tiles(self.core):
            if ct.can_heal(tile):
                ct.heal(tile)
                return True
        return False

    def _core_shelled(self, ct):
        """True only when our Core is visible AND standing below full HP.

        Direct observation rather than the store.  SLOT_UNDER is a proximity
        flag written from several call sites and cannot tell "an enemy is
        loitering near home" from "the Core is being shot"; a Core below its
        max HP is proof of the latter.  Vision is the trap: get_tile_env,
        is_tile_passable and get_tile_building_id all raise GameError for an
        in-bounds tile outside the caller's vision (docs/game-model.md), with
        the same message as an off-map tile, so the anchor Position cannot be
        queried directly.  get_nearby_buildings returns only what is visible,
        so the scan below never raises -- it is exactly the idiom _builder
        already uses to find the Core in the first place.  Out of vision
        returns False, which is the right answer for both callers: a defender
        that cannot see the Core cannot heal it or usefully judge it either.
        """
        for eid in ct.get_nearby_buildings():
            if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                return ct.get_hp(eid) < ct.get_max_hp(eid)
        return False

    def _hunt_turret(self, ct):
        """Peck a near-Core enemy turret instead of healing.  True == turn spent.

        See the TURRET-HUNTING UNDER SIEGE block at the top of this file for
        the measured motivation and for why every one of the gates below is
        there.  Also maintains self.hunting, which _builder reads to detect the
        falling edge; this method is its sole owner, so it is cleared on entry
        and re-armed only while a live target is held.

        Return value is "this turn was spent hunting", NOT "a target exists":
        a hunter that is two tiles out on a round its move cooldown is not zero
        keeps self.hunting set but returns False, so the universal heal below
        can still use the round.  That split is what keeps the state sticky and
        the builder off the converge/hunt oscillation.
        """
        self.hunting = False
        if self.core is None:
            return False
        # Same seats that heal under siege, and only those.  role_n == 1 is the
        # single interceptor and role_n == 0 the siege engineer (role
        # "saboteur"), and both already have their own melee paths; pulling
        # either onto a home turret would cost the capability it exists for.
        if self.role not in ("defend", "expand") or self.role_n == 1:
            return False
        # TWO HUNT MODES (Eir 2).  CORE-SIEGE mode is the shipped v55/Eir
        # behaviour, all gates unchanged: round floor 120, SLOT_UNDER, and
        # direct Core-HP evidence.  ECO-SIEGE mode is new, from the meander
        # r133 loss to Lunds v41: a forward Gunner planted at r69
        # orthogonally beside our harvester killed it at r74 and then farmed
        # every rebuilt conveyor on that link for 60 rounds -- and NEITHER
        # gate could ever answer it: the Core was not bleeding (shelled gate)
        # and the clock was pre-120 (floor).  A turret standing orthogonally
        # adjacent to a friendly HARVESTER is not ambient threat, it is an
        # active point-blank siege of a named asset, and it is huntable at
        # any round with no Core evidence.  STRICT harvester-only adjacency
        # on purpose: conveyor-adjacency would re-open the refuted early
        # ambient hunting on conveyor-dense boards (the eider 8/16 -> 0/16
        # ablation and the fjordgate rush regression both came from exactly
        # that), while a turret parked beside a harvester is unambiguous.
        core_siege = (
            ct.get_current_round() >= HUNT_MIN_RND
            and ct.read_store(SLOT_UNDER) != 0
        )
        # Nothing has been written yet, so bailing here is a clean no-op that
        # degrades to exactly the pre-existing behaviour (heal / converge).
        if self._cpu_exhausted(ct):
            return False
        if core_siege and not self._core_shelled(ct):
            core_siege = False
        eco_mode = not core_siege
        if eco_mode:
            # Only proceed if some visible enemy turret is point-blank on a
            # friendly harvester; the candidate loop re-checks per turret.
            if not self._eco_besieged(ct):
                return False

        p = ct.get_position()
        me = ct.get_id()

        # Candidate turrets: visible enemy Gunners/Sentinels inside the siege
        # band around our Core anchor AND already within our own designation
        # radius.  The second test is not an optimisation -- a builder outside
        # HUNT_DESIGNATE_DSQ is not in the designation set at all, so it could
        # never win the id ballot below -- but it does keep the friendly scan
        # off the wire for every builder that is merely near a shelled Core.
        # ECO-SIEGE designation reach = builder vision (r^2 = 20), not the
        # CORE-SIEGE radius 8.  Measured: jython_g4/archipelago, an enemy
        # Gunner at (7,13) sat at dsq = 4 from our harvester (6,11) for 80
        # turns and killed it, unanswered; sporks_g4/nordkap, sentinels
        # parked beside harvesters unanswered for 143 turns.  Root cause both
        # times: no builder happened to be inside dsq 8 of the turret, so the
        # designation set was EMPTY and nobody ever hunted -- an eco-siege
        # turret sits on a harvester, not among our repair line, so "nobody
        # nearby" is the common case, not the edge case.  Any builder that
        # can SEE the besieging turret can walk to it and peck; the id ballot
        # below uses the same widened radius so exactly one visible builder
        # commits.  CORE-SIEGE keeps radius 8, byte-identical to shipped
        # behaviour (the repair line never thins to chase a gun).
        designate = 20 if eco_mode else HUNT_DESIGNATE_DSQ
        cands = []
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == self.team:
                continue
            bet = ct.get_entity_type(bid)
            if bet not in (EntityType.GUNNER, EntityType.SENTINEL):
                continue
            bp = ct.get_position(bid)
            if eco_mode:
                # ECO-SIEGE: the turret qualifies by what it is doing, not by
                # where it is on the map -- parked on a friendly harvester,
                # at any range from the Core (type-gated in the helper).
                if not self._turret_on_harvester(ct, bp, bet):
                    continue
            else:
                # CORE-SIEGE band, sized past Sentinel range (r^2 = 32),
                # measured to the nearest tile of the 2x2 footprint.
                # Validated twice: the CtrlAltDefeat decode (sentries
                # shelling from dist^2 25-41, outside the old anchor-measured
                # 20) and the v79 jackpot sweep (sentinel at EXACTLY dsq 32
                # on the diagonal, killed our core with 60 unanswered shots
                # while a builder stood orthogonally adjacent to it).
                if min(t.distance_squared(bp) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
                    continue
            if p.distance_squared(bp) > designate:
                continue
            cands.append((ct.get_hp(bid), p.distance_squared(bp), bid, bp))
        if not cands:
            return False
        # Weakest first: a turret one peck from dead is worth strictly more
        # than a fresh one, and it is also the only kind HUNT_FINISH_HP lets a
        # lone builder take on.  Distance and id only break ties, so the order
        # is total and deterministic.
        cands.sort(key=lambda row: row[:3])

        # One pass for both remaining questions -- who else is in the ballot,
        # and whether the repair line is still manned.
        mates = []
        for uid in ct.get_nearby_units():
            if uid == me or ct.get_team(uid) != self.team:
                continue
            if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                continue
            mates.append((uid, ct.get_position(uid)))
        homes = core_tiles(self.core)
        healers = 0
        for _uid, up in mates:
            if any(abs(up.x - c.x) + abs(up.y - c.y) == 1 for c in homes):
                healers += 1

        # Prune ledger entries for turrets no longer in the candidate set, so
        # a turret that died or left the band does not leave a stale row.
        live_bids = {row[2] for row in cands}
        for stale in [b for b in self.hunt_defer if b not in live_bids]:
            del self.hunt_defer[stale]

        for hp, _d, bid, bp in cands:
            # Designation: lowest entity id inside HUNT_DESIGNATE_DSQ of THIS
            # turret wins it.  Anyone lower that we can see takes it from us --
            # but only for as long as the deference provably works.  See the
            # BALLOT DEADLOCK BREAKER block at the top of the file: if the
            # turret's HP has not dropped for our own staggered override
            # window, the elected unit is not actually hunting (or the turret
            # is escort-healed as fast as it is pecked, which wants more
            # attackers anyway), and the ballot stops binding us.
            if any(
                uid < me and up.distance_squared(bp) <= designate
                for uid, up in mates
            ):
                stalled, last_hp = self.hunt_defer.get(bid, [0, None])
                if last_hp is not None and hp < last_hp:
                    stalled = 0
                else:
                    stalled += 1
                self.hunt_defer[bid] = [stalled, hp]
                if stalled <= HUNT_DEFER_BASE + (me % HUNT_DEFER_SPREAD):
                    continue
            else:
                self.hunt_defer.pop(bid, None)
            # Corner cores can't man HUNT_MIN_HEALERS: a corner 2x2 footprint
            # has only 4 in-bounds orthogonal neighbours against an interior
            # core's 8, so demanding 2 standing healers before anyone hunts
            # is unsatisfiable exactly where the core is most cornered.
            # Measured on the v79 jackpot sweep: the healer floor (not the
            # band) kept an adjacent builder from ever pecking the killer
            # sentinel.  The floor scales with the seats that can exist.
            # The healer floor protects the Core's repair line; an eco-siege
            # target has no repair line to protect (the besieged harvester is
            # dead or doomed either way -- killing the gun is the only play).
            if not eco_mode and healers < self._healer_floor(ct) and hp > HUNT_FINISH_HP:
                continue

            if abs(p.x - bp.x) + abs(p.y - bp.y) == 1:
                # Orthogonally adjacent: peck and hold, exactly as _intercept
                # holds its guard tile.  The turn is owned even on a round the
                # peck cannot be paid for or the cooldown forbids it -- the
                # alternative is drifting back toward the Core under the
                # convergence rule and walking the same tile again next round.
                # A turret shelling the Core does not return fire on whatever
                # is standing beside it, so holding here is free.
                self.hunting = True
                if (
                    ct.get_action_cooldown() == 0
                    and ct.get_global_resources() >= HUNT_FIRE_TI
                    and ct.can_fire(bp)
                ):
                    ct.fire(bp)
                return True

            # One to three tiles out.  _nav's BFS treats an enemy turret tile
            # as blocked and therefore aims at its cardinal neighbours, which
            # is precisely the adjacency the peck needs; no special-casing.
            self.hunting = True
            if ct.get_move_cooldown() == 0:
                self.tgt = bp
                self._nav(ct, pave=False)
                return True
            return False
        return False

    def _try_screen(self, ct):
        """Threat-triggered barrier screen: block a shelling Gunner's ray.

        Live 2026-08-07 series: we placed 0 barriers in 25/25 games while the
        five opponents placed 381 and won 23.  A barrier costs 3 Ti and has
        30 HP -- it absorbs 4+ Gunner shots (7 dmg each) or permanently
        blocks the firing line, out-valuing repeated 1 Ti +4 HP Core heals
        against sustained shelling.  Sentinels pierce blockers (see _turret),
        so a known Sentinel threat is skipped; unknown/out-of-vision threats
        get the cheap insurance anyway.

        Placement: the tile on the straight threat->core-tile segment nearest
        the Core that this builder can reach this turn.  Build-if-adjacent
        only -- the defender orbits the footprint, so the near-core segment
        tile is usually in range; walking costs are left to the existing nav.
        """
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None or self.core is None:
            return False
        if ct.get_global_resources() < ct.get_barrier_cost() + 4:
            return False
        # Only a VISIBLE GUNNER justifies a wall: SLOT_THREAT also carries
        # enemy builders (which walk around barriers) and Sentinels (which
        # pierce them), and an out-of-vision threat cannot be classified.
        try:
            tid = ct.get_tile_building_id(threat)
        except Exception:
            return False
        if tid is None or ct.get_entity_type(tid) != EntityType.GUNNER:
            return False
        p = ct.get_position()
        homes = core_tiles(self.core)
        for c in homes:
            dx, dy = c.x - threat.x, c.y - threat.y
            if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
                continue
            steps = max(abs(dx), abs(dy))
            if steps < 2:
                continue
            ux = (dx > 0) - (dx < 0)
            uy = (dy > 0) - (dy < 0)
            for k in range(steps - 1, 0, -1):
                b = Position(threat.x + ux * k, threat.y + uy * k)
                if not (0 <= b.x < self.mw and 0 <= b.y < self.mh):
                    continue
                if (b.x, b.y) in self.map_walls:
                    break
                # NEVER WALL AN ORE TILE: a screen barrier is permanent and
                # an ore tile is a harvester site -- the same lesson the
                # pave ban and choke planner already encode (fjordgate ghost
                # froze 3 of 4 sites under self-laid conveyors).
                if self.map_grid is not None and self.map_grid[b.y][b.x] == "o":
                    continue
                # Core-adjacent cells are conveyor delivery / heal / battery
                # seats; a barrier there can stall the link queue forever.
                if any(abs(b.x - h.x) + abs(b.y - h.y) <= 1 for h in homes):
                    continue
                if abs(p.x - b.x) + abs(p.y - b.y) != 1:
                    continue
                if ct.can_build_barrier(b):
                    ct.build_barrier(b)
                    return True
        return False

    def _heal_screen(self, ct):
        """Repair an adjacent damaged friendly barrier (1 Ti, +4 HP)."""
        p = ct.get_position()
        for d in CARDINALS:
            bp = p.add(d)
            if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(bp)
                if (
                    bid is not None
                    and ct.get_team(bid) == self.team
                    and ct.get_entity_type(bid) == EntityType.BARRIER
                    and ct.can_heal(bp)
                ):
                    ct.heal(bp)
                    return True
            except Exception:
                continue
        return False

    def _try_counterbattery(self, ct):
        """Build only a weapon ray that already contains the reported threat."""
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None:
            return False
        # L2 stale-threat hygiene -- freshness gate.  SLOT_ATK_RND is rewritten
        # every round an enemy is actually sighted (Core scan and _builder scan
        # both stamp it), so a stamp more than 12 rounds old means every
        # scanner has watched empty lanes for 12 straight rounds.  Measured in
        # pivot_g1/snowflake: the defender built 6 gunners against a sighting
        # that was long dead, ~120+ Ti of turrets aimed at nothing.  This
        # suppresses only NEW turret construction against departed threats;
        # the 50-round UNDER latch is deliberately untouched -- it guards the
        # ammo magazine (measured atoll harasser case at its comment).
        if ct.get_current_round() - ct.read_store(SLOT_ATK_RND) > 12:
            return False
        # B8 phase 1b -- reach test.  A Sentinel is r^2=32, so a turret built
        # against our own footprint cannot reach a threat past footprint-dsq
        # ~44: every can_fire_from below returns False and the scan burns its
        # full ~128-256 engine calls for nothing, every defender turn, for up
        # to the 50 rounds the UNDER latch holds.  Widening the sensing tier is
        # exactly what starts publishing threats that far out, so the reach
        # test ships with it.  HUNT_BAND_DSQ = 41 is the already-measured,
        # twice-validated "past Sentinel range, footprint-measured" constant in
        # this file rather than a new number.  Net CPU effect is negative.
        if B8_ON and min(
            t.distance_squared(threat) for t in core_tiles(self.core)
        ) > HUNT_BAND_DSQ:
            return False
        # Mirror of _plan_siege's economy gate: the first emergency battery is
        # free, any further one waits for income.  Ungated, opening threat noise
        # on close-anchor maps buys three fixed-facing Sentinels aimed at
        # transient spawn tiles before the first harvester exists.
        if ct.read_store(SLOT_HOME_GUN) >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED:
            # ...unless the Core is provably BLEEDING.  The gate exists for
            # close-anchor opening noise (transient spawn-tile threats buying
            # three sentinels aimed at nothing), but on meander v79 shelled
            # our base from r7-r9 while this gate held our counterbattery
            # shut until harvester 3 landed at r130 -- we finished with ZERO
            # turrets alive after r299 against his 804 shots.  Real core
            # damage is not noise: _core_shelled is direct HP-bar evidence,
            # the same test every heal path trusts.  (A rich-bank floor on
            # this waiver was tried and refuted: both the CAD insertion and
            # the meander duel open on a still-rich bank, so the floor
            # separated nothing and cost meander games.)
            if not self._core_shelled(ct):
                return False
        p = ct.get_position()
        choices = (
            (
                (EntityType.SENTINEL, ct.get_sentinel_cost()),
                (EntityType.GUNNER, ct.get_gunner_cost()),
            )
            if PRIMARY_SENTINEL else
            (
                (EntityType.GUNNER, ct.get_gunner_cost()),
                (EntityType.SENTINEL, ct.get_sentinel_cost()),
            )
        )
        for turret_type, cost in choices:
            if ct.get_global_resources() < cost:
                continue
            for d in DIRECTIONS:
                # Nothing here is written to self/the store until a build
                # actually succeeds a few lines down, so bailing between
                # candidates is clean. Checked once per `d`, not per
                # `facing` (the innermost loop), to keep the check itself
                # infrequent relative to the up-to-8 engine calls per `d`.
                if self._cpu_exhausted(ct):
                    return False
                bp = p.add(d)
                if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                    continue
                for facing in DIRECTIONS:
                    try:
                        aligned = ct.can_fire_from(bp, facing, turret_type, threat)
                    except Exception:
                        aligned = False
                    if not aligned:
                        continue
                    if turret_type == EntityType.SENTINEL and ct.can_build_sentinel(bp, facing):
                        ct.build_sentinel(bp, facing)
                        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
                        return True
                    if turret_type == EntityType.GUNNER and ct.can_build_gunner(bp, facing):
                        ct.build_gunner(bp, facing)
                        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
                        return True
        return False

    def _try_harvester(self, ct, harv):
        p = ct.get_position()
        for d in DIRECTIONS:
            bp = p.add(d)
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_harvester(bp):
                if not self._harvester_site_safe(ct, bp):
                    continue
                ct.build_harvester(bp)
                ct.write_store(SLOT_HARVESTERS, harv + 1)
                if harv + 1 >= ECO_NEED:
                    ct.write_store(SLOT_ECO_READY, 1)
                if not self.link_queue:
                    self.link_source = bp
                    self.link_queue = self._link_path(ct, bp)
                return True
        return False

    def _defend(self, ct):
        p = ct.get_position()
        hive_bunker = (
            self.mw == 25 and self.mh == 25
            and (self.core.x, self.core.y) == (21, 3)
        )
        if hive_bunker and ct.get_action_cooldown() == 0:
            bp = Position(20, 4)
            bid = ct.get_tile_building_id(bp)
            if abs(p.x - bp.x) + abs(p.y - bp.y) == 1:
                if (
                    bid is not None and ct.get_team(bid) == self.team
                    and ct.get_entity_type(bid) == EntityType.BARRIER
                    and ct.can_heal(bp)
                ):
                    ct.heal(bp)
                    return
                if (
                    bid is None
                    and ct.get_global_resources() >= ct.get_barrier_cost()
                    and ct.can_build_barrier(bp)
                ):
                    ct.build_barrier(bp)
                    return
        under = ct.read_store(SLOT_UNDER) != 0
        # Proven shelling, observed directly off the Core's own HP bar rather
        # than read out of SLOT_UNDER -- see _core_shelled.  Conjoined with
        # `under` so it cannot fire on old unrepaired damage long after the
        # attacker left, and so the scan is skipped entirely on a quiet map.
        shelled = under and self._core_shelled(ct)
        chase_battery = (
            self.mw == 20 and self.mh == 26
            and self.core.x == 9 and self.core.y == 6
        )
        threat = unpack_pos(ct.read_store(SLOT_THREAT)) if under else None
        harv = ct.read_store(SLOT_HARVESTERS)
        ti = ct.get_global_resources()
        # PIECE H, builder half (see ENDGAME_SWITCH_ON).  Tiebreak 2 counts
        # harvesters ALIVE, so in the last forty rounds every economy ceiling
        # and every reserve is dead weight and a link laid now delivers
        # nothing worth the action.
        endgame = ENDGAME_SWITCH_ON and ct.get_current_round() >= ENDGAME_RND

        if ct.get_action_cooldown() == 0:
            defended = False
            if under:
                # HEAL BEATS SABOTAGE UNDER SHELLING.  On heart the defender
                # stood beside both an enemy Gunner and our Core and spent the
                # whole siege pecking the Gunner for 2 dmg a round (25 HP, at
                # 2 Ti a tick) while the Core it was touching took 0 heals.
                # 1 Ti for +4 HP absorbs more of an 18 dmg Sentinel ray than
                # any melee peck returns.  Belt and braces: the universal heal
                # in _builder already fires first for an adjacent builder, so
                # this holds the order if that call site ever moves.
                if shelled and self._heal_core(ct):
                    defended = True
                elif self._try_screen(ct):
                    defended = True
                elif shelled and self._heal_screen(ct):
                    defended = True
                else:
                    defended = (
                        self._sabotage_prio(ct)
                        or self._try_counterbattery(ct)
                    )
                if chase_battery and threat is not None:
                    # On north-side Nordkap the legal battery outranges repair;
                    # spending every action on +4 HP prevents ever reaching it.
                    defended = True
                elif not defended:
                    defended = self._heal_core(ct)
            if not defended:
                if harv < 1 and ti >= ct.get_harvester_cost() and self._try_harvester(ct, harv):
                    return
                # Do not move in a conveyor-build tick: the movement query can
                # still treat the newly placed link as empty and strand us.
                # PIECE H: no new links past ENDGAME_RND -- the action is worth
                # more as a harvester two lines down.
                if not endgame and self.link_queue and ti >= ct.get_conveyor_cost():
                    if self._build_next_link(ct):
                        return
                # Wake the Launcher subsystem: v58's call site, deleted in the
                # v63 rework, restored here. _try_build_launcher() claims
                # SLOT_LAUNCHER before building, so this fires at most once.
                if not endgame and harv >= ECO_NEED and self._try_build_launcher(ct):
                    return
                # PIECE H: _eco_cap is a scale-curve ceiling for a game that
                # still has a future.  At ENDGAME_RND it is dropped outright --
                # any adjacent ore, any bank that covers the (scaled) cost.
                if (endgame or harv < self._eco_cap(ct)) and ti >= ct.get_harvester_cost() and self._try_harvester(ct, harv):
                    return
                if not under:
                    self._heal_core(ct)

        # Action phase is over here and left nothing half-set (every branch
        # above either returns right after its build/heal action or falls
        # through cleanly). Check before the move phase below: every branch
        # of it calls _nav, which runs _bfs_direction -- a BFS over the
        # whole map.
        if self._cpu_exhausted(ct):
            return

        if hive_bunker:
            if ct.get_move_cooldown() == 0:
                self.tgt = Position(20, 3)
                self._nav(ct, pave=False)
            return

        # DEFENDER COMES HOME.  In the meander loss the role_n == 4 defender
        # cycled far-off link/threat tiles for 150 rounds while the Core was
        # shelled to death.  Once the Core is provably losing HP the defender
        # has exactly one job -- stand next to it and heal -- so walking home
        # outranks chasing the threat and outranks finishing a conveyor link.
        # `shelled` requires the Core to be in this builder's own vision
        # (r^2 = 20), so this only fires from within about four tiles of home,
        # which is exactly the range where walking back is feasible anyway.
        if shelled and self.role_n == 4 and ct.get_move_cooldown() == 0 and not any(
            abs(p.x - c.x) + abs(p.y - c.y) == 1 for c in core_tiles(self.core)
        ):
            self.tgt = self.core
            self._nav(ct, pave=False)
            return

        if under and threat is not None and ct.get_move_cooldown() == 0:
            self.tgt = threat
            self._nav(ct, pave=False)
            return

        if self.link_queue:
            if ct.get_action_cooldown() == 0 and self._build_next_link(ct):
                return
            if not self.link_queue:
                return
            if ct.get_move_cooldown() == 0:
                nxt = self.link_queue[0]
                if p.x == nxt.x and p.y == nxt.y:
                    self._step_off_link(ct)
                elif abs(p.x - nxt.x) + abs(p.y - nxt.y) == 1:
                    # Already in build range.  Wait for action/resources instead
                    # of occupying the future conveyor cell; dead-end Core inputs
                    # (notably Vase) can otherwise trap the builder permanently.
                    return
                else:
                    self.tgt = nxt
                    self._nav(ct, pave=False)
            return

        if ct.get_move_cooldown() != 0:
            return
        if p.distance_squared(self.core) > 8:
            self.tgt = self.core
        elif self.tgt is None or p == self.tgt or self.stuck >= 2:
            self.ang = (self.ang + 1.0) % (2 * math.pi)
            self.tgt = Position(
                max(0, min(self.core.x + int(2 * math.cos(self.ang)), self.mw - 1)),
                max(0, min(self.core.y + int(2 * math.sin(self.ang)), self.mh - 1)),
            )
        self._nav(ct, pave=False)

    def _expand(self, ct):
        p = ct.get_position()
        hive_freeze = (
            self.mw == 25 and self.mh == 25
            and (self.core.x, self.core.y) in ((2, 20), (21, 3))
            and ct.read_store(SLOT_HOME_GUN) >= 1
            and ct.get_current_round() >= 42
        )
        if hive_freeze:
            return

        # SABOTEUR INTERCEPTION.  Ranks above ordinary expand work and below
        # everything already decided in _builder -- the universal Core heal,
        # the map-gated _rank2_hold and the near-Core melee recall all return
        # before _expand is ever entered.  Exactly one worker breaks off so the
        # remaining expanders keep the economy running; role_n == 1 is the
        # first expander and never changes role (only role_n == 3 is ever
        # promoted to saboteur), so ownership is stable for the whole match
        # without a store write.  The role_n == 4 defender is untouched.
        if self.role_n == 1:
            if self._intercept(ct):
                return
            # CHOKEPOINT WALLS (S4): the interceptor's IDLE time only -- a
            # live chase above always wins the turn, so interception is
            # untouched.  SELF-PATH RESPECT, verified in _bfs_direction: our
            # own saboteur/launchwait walkers route through it, and it adds
            # every visible BARRIER to its blocked set (the
            # GUNNER/SENTINEL/LAUNCHER/HARVESTER/BARRIER branch) while
            # can_move refuses occupied tiles regardless -- so our own walls
            # reroute our own units automatically.  Ore tiles and tiles
            # cardinally adjacent to either Core footprint were excluded at
            # planning time in _builder's decode branch.
            if self._try_choke_wall(ct):
                return

        has_launch = ct.read_store(SLOT_LAUNCHER) != 0
        harv = ct.read_store(SLOT_HARVESTERS)
        allow_pave = has_launch or harv >= 2
        # PIECE H, builder half (see ENDGAME_SWITCH_ON).  Harvesters alive is
        # tiebreak 2; a conveyor link and a 4 HP patch are worth nothing at all
        # by round 1000, so past ENDGAME_RND this expander spends every action
        # it has on ore and lets the economy ceiling and the siege reserve go.
        endgame = ENDGAME_SWITCH_ON and ct.get_current_round() >= ENDGAME_RND

        if ct.get_action_cooldown() == 0:
            if not endgame and self.link_queue and self._build_next_link(ct):
                return
            if (
                ct.get_global_resources() >= ct.get_harvester_cost()
                if endgame
                else (
                    self._eco_spendable(ct, ct.get_harvester_cost())
                    and harv < self._eco_cap(ct)
                )
            ):
                for d in DIRECTIONS:
                    bp = p.add(d)
                    if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_harvester(bp):
                        if not self._harvester_site_safe(ct, bp):
                            continue
                        ct.build_harvester(bp)
                        ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)
                        if ct.read_store(SLOT_HARVESTERS) >= ECO_NEED:
                            ct.write_store(SLOT_ECO_READY, 1)
                        if not self.link_queue:
                            self.link_source = bp
                            self.link_queue = self._link_path(ct, bp)
                        break
            # CHAIN MEDIC (heal-in-passing).  Measured in the eider 1000-round
            # tiebreak losses to kladde_probe: ~70% of all damage to our
            # economy buildings was enemy BUILDER MELEE -- 376 hits x 2 dmg =
            # 752 HP, clearing ~37 twenty-HP conveyors -- and every cleared
            # tile was stateless-relaid by the next passer-by at 3 Ti plus,
            # decisively, +1% team-wide cost scale PER RELAY.  146 conveyor
            # builds put +146% on everything bought afterwards, which is what
            # pinned the bank under the respawn floor for ~600 rounds (the
            # money->labour chain of the eider diagnosis).  Healing is the
            # counter that costs no scale at all: 1 Ti for +4 HP outpaces a
            # melee peck's 2 dmg per round outright, and can_heal() refuses a
            # full-HP target, so this fires only when something adjacent is
            # genuinely damaged.  Deliberately LAST in the action phase --
            # link tiles and harvesters outvalue a 4 HP patch -- and floored
            # on a small bank so a starving opening never trades its first
            # harvester for a repair.  (The _v70ec reserve/rebuild-cap
            # approach to the same diagnosis was refuted by ablation: gating
            # link spending inverted the income bootstrap, collected 9390 ->
            # 3160.  Repair attacks the churn without touching the
            # bootstrap.)
            # Two windows.  Late (>= MEDIC_MIN_RND) is unchanged: any damage at
            # all.  Early (>= MEDIC_EARLY_MIN_RND) heals ONLY deep damage,
            # >= MEDIC_EARLY_MIN_DMG down -- the tempo tax the MEDIC_MIN_RND
            # ablation measured came from patching cosmetic opening pecks, and
            # the depth floor excludes exactly those while still covering a
            # sustained farm raid.
            # PIECE H: the medic is off past ENDGAME_RND.  A +4 HP patch on a
            # conveyor scores in no tiebreak; the action it costs could have
            # been a harvester, which scores in tiebreak 2.
            rnd_now = ct.get_current_round()
            medic_late = rnd_now >= MEDIC_MIN_RND
            if not endgame and ct.get_global_resources() >= MEDIC_TI_FLOOR and (
                medic_late
                or (MEDIC_EARLY_ON and rnd_now >= MEDIC_EARLY_MIN_RND)
            ):
                for d in CARDINALS:
                    bp = p.add(d)
                    if not (0 <= bp.x < self.mw and 0 <= bp.y < self.mh):
                        continue
                    try:
                        bid = ct.get_tile_building_id(bp)
                        if (
                            bid is not None
                            and ct.get_team(bid) == self.team
                            and ct.get_entity_type(bid) in MEDIC_TYPES
                            and ct.get_hp(bid) <= ct.get_max_hp(bid) - (
                                1 if medic_late else MEDIC_EARLY_MIN_DMG
                            )
                            and ct.can_heal(bp)
                        ):
                            ct.heal(bp)
                            return
                    except Exception:
                        continue

        # Action phase over -- the harvester build above (if any) already
        # wrote SLOT_HARVESTERS and link_queue together with nothing after
        # it in the same branch, so nothing is left half-set. Check before
        # the move phase below, which calls _pick (an ore scan) and _nav
        # (a BFS over the map).
        if self._cpu_exhausted(ct):
            return

        # MULTI-HEALER CONVERGENCE.  One enemy turret chips the Core faster
        # than one healer repairs it: a Sentinel lands 18 damage every second
        # round, about -9/round, against the single role_n == 4 defender's
        # +4/round.  Measured over four Lunds Stallions games, that arithmetic
        # runs 150-900 rounds of the Core bleeding out while idle expanders
        # work the far side of the map and thousands of titanium sit banked.
        # Two or three converged healers deliver +8 to +12/round for 2-3 Ti a
        # round and flip the sign permanently.
        #
        # Only role_n == 2 and the role_n >= 5 replacements converge.  The
        # other seats keep their jobs: role_n == 0 is the siege engineer,
        # role_n == 1 the single interceptor, role_n == 3 turns saboteur, and
        # role_n == 4 already comes home via the identical rule in _defend.
        #
        # PROXIMITY-BOUNDED BY CONSTRUCTION: _core_shelled only answers True
        # when the Core is inside this builder's own vision (r^2 = 20), so
        # only builders already within about four tiles of home ever converge.
        # There is no cross-map recall and none is wanted -- a far expander
        # cannot see the Core, so it never leaves its ore.
        #
        # Conjoined with SLOT_UNDER exactly as _defend's `shelled` is, for the
        # same two reasons: it cannot fire on old unrepaired damage long after
        # the attacker left, and it is the same gate the universal adjacent
        # heal in _builder uses -- converging when that heal would not fire
        # would park a builder next to the Core for nothing.
        #
        # Once adjacent this holds position rather than falling through to the
        # walk-to-ore below: the healing itself is already handled: the
        # universal heal in _builder fires before _expand is entered on every
        # round the action cooldown allows.  Stepping away on the rounds it
        # cannot would cost a round walking back for every round healed.
        if (self.role_n == 2 or self.role_n >= 5) and ct.read_store(SLOT_UNDER) != 0 \
                and self._core_shelled(ct):
            self.converging = True
            if ct.get_move_cooldown() == 0 and not any(
                abs(p.x - c.x) + abs(p.y - c.y) == 1 for c in core_tiles(self.core)
            ):
                self.tgt = self.core
                self._nav(ct, pave=False)
            return
        if self.converging:
            # Falling edge: the Core is whole again (or the siege is over).
            # Hand a CLEAN state back to the expand machine below, exactly as
            # _intercept's disengage does: self.tgt still holds the Core --
            # an unreachable building tile that _pick would never choose --
            # and self.stuck counted rounds of walking home, so both are
            # cleared, forcing a fresh _pick this same turn.  link_queue is
            # positional and survives the interruption untouched.
            self.converging = False
            self.tgt = None
            self.stuck = 0
            self.wall = None

        # CHAIN WATCHDOG (see _chain_dead).  An idle expander with no link
        # work re-links the nearest visibly-dead friendly mine, reusing the
        # existing link machinery wholesale.  8-round per-unit cooldown keeps
        # the scan cheap and lets a failed replan retry instead of orphaning
        # the site.  Duplicate relinks by two units converge harmlessly
        # (occupied tiles pop from the queue).
        if (
            not self.link_queue
            and ct.get_current_round() - getattr(self, 'relink_rnd', -99) >= 8
            and not self._cpu_exhausted(ct)
        ):
            _best = None
            _bestd = 10 ** 9
            for eid in ct.get_nearby_buildings():
                try:
                    if (
                        ct.get_team(eid) != self.team
                        or ct.get_entity_type(eid) != EntityType.HARVESTER
                    ):
                        continue
                    hp_ = ct.get_position(eid)
                except Exception:
                    continue
                if self._chain_dead(ct, hp_):
                    d_ = p.distance_squared(hp_)
                    if d_ < _bestd:
                        _best, _bestd = hp_, d_
            if _best is not None:
                self.relink_rnd = ct.get_current_round()
                _q = self._link_path(ct, _best)
                if _q:
                    self.link_source = _best
                    self.link_queue = _q

        if ct.get_move_cooldown() != 0:
            return
        # ORE STEP-OFF (borrowed from v79 after the heart decode).  Builds
        # are adjacent-only, never own-tile, so a builder standing ON an ore
        # tile is the one unit that can never put a harvester there -- and on
        # heart we parked one builder on tile (5,18) from r160 to r998, left
        # 14 of the map's 28 ore tiles unmined forever, and lost the economy
        # 2.5x.  Wall-dense maps only (his gate, copied): corridors are what
        # turn "standing on ore" from a transient into an 800-round park, and
        # on open maps squatting contested ore is sometimes exactly right
        # (atoll: HIS squatters out-collected us).  Ore is only knowable on
        # decoded maps; map_walls is empty otherwise and the gate stays shut.
        if (
            (
                len(self.map_walls) >= ORE_STEPOFF_MIN_WALLS
                # SCARCE-ORE WIDENING (E2).  fjordgate ghost (sporks_g5, lost
                # all 3 salts 0-120 mined): the one harvester site our pave
                # trail had NOT buried stayed free all game, but the assigned
                # builder pathed ONTO the ore tile in an infinite 3-turn loop
                # (mv->adjacent, mv->onto-ore, pause; 587 moves, zero build
                # actions) while titanium exceeded harvester cost repeatedly
                # -- zero harvester builds in the last 970 turns.  So: also
                # step off when the decoded map has 8 or fewer ore tiles
                # total (fjordgate 6, moonrise 8) -- on scarce-ore maps
                # squatting one site forfeits a meaningful fraction of the
                # map's whole economy.  Atoll, where squatting is GOOD (many
                # ores, contested center), has more and stays untouched.
                # map_ores non-empty keeps this clause shut on undecoded
                # maps, matching the map_walls clause's behavior.
                or (self.map_ores and len(self.map_ores) <= 8)
            )
            and ct.get_tile_env(p) == Environment.ORE_TITANIUM
        ):
            for d in CARDINALS:
                n = p.add(d)
                if (
                    0 <= n.x < self.mw and 0 <= n.y < self.mh
                    and ct.get_tile_env(n) != Environment.ORE_TITANIUM
                    and ct.is_tile_passable(n)
                    and ct.can_move(d)
                ):
                    ct.move(d)
                    self.tgt = None
                    self.stuck = 0
                    return
        if self.link_queue:
            nxt = self.link_queue[0]
            if p.x == nxt.x and p.y == nxt.y:
                self._step_off_link(ct)
            elif abs(p.x - nxt.x) + abs(p.y - nxt.y) == 1:
                return
            else:
                self.tgt = nxt
                self._nav(ct, pave=False)
            return
        if self.tgt is None or p == self.tgt or self.stuck >= 5:
            self.tgt = self._pick(ct)
            self.stuck = 0
            self.wall = None
        if self.tgt is None:
            return
        for d in DIRECTIONS:
            bp = p.add(d)
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh:
                if ct.get_tile_env(bp) == Environment.ORE_TITANIUM and ct.get_tile_building_id(bp) is None:
                    self.tgt = bp
                    break
        self._nav(ct, pave=allow_pave)

    def _find_intruder(self, ct):
        """Nearest visible enemy builder bot operating inside our own half.

        "Our half" is the plain bisector test: closer to our Core than to the
        enemy Core anchor.  Bots within INTRUDER_CORE_DSQ of our Core are
        skipped -- the melee recall in _builder and the defender's threat
        chase already own those, and double-handling them would pull a second
        body onto a target that is already covered.
        """
        p = ct.get_position()
        best, best_d = None, None
        for eid in ct.get_nearby_units():
            if ct.get_team(eid) == self.team:
                continue
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT:
                continue
            ep = ct.get_position(eid)
            dc = self.core.distance_squared(ep)
            if dc <= INTRUDER_CORE_DSQ or dc >= ep.distance_squared(self.enemy):
                continue
            d = p.distance_squared(ep)
            if best_d is None or d < best_d or (d == best_d and eid < best):
                best, best_d = eid, d
        return best

    def _heal_adjacent(self, ct):
        """Repair a damaged friendly building we are standing next to.

        This, not the melee peck, is what actually stops an economy raider:
        builder fire is 2 Ti for 2 damage and only lands on BUILDINGS (a bot
        cannot be attacked at all -- docs/game-model.md), while a heal is
        1 Ti for +4 HP.  Parked between the raider and what it is chipping,
        the interceptor out-repairs it two-to-one on HP and eight-to-one on
        titanium, so the harvester never dies.  can_heal() enforces adjacency,
        cost, and that there is real damage, so this is free when nothing is
        hurt.
        """
        p = ct.get_position()
        for d in CARDINALS:
            t = p.add(d)
            if 0 <= t.x < self.mw and 0 <= t.y < self.mh and ct.can_heal(t):
                ct.heal(t)
                return True
        return False

    def _guard_target(self, ct, tp):
        """The friendly building this raider is working on, if we can see one.

        Standing next to the RAIDER accomplishes nothing -- it cannot be
        damaged and it is usually on the far side of its victim anyway.
        Standing next to its VICTIM turns the chase into a repair escort,
        which the raider cannot win.  Damaged first, then nearest to it.
        """
        best, best_k = None, None
        rnd = ct.get_current_round()
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) != self.team:
                continue
            # STALEMATE DISENGAGE.  Measured in the v79 battery replays: the
            # escort "wins" its stalemate -- +4 heal beats -2 peck -- and
            # that is exactly the trap.  On atoll the raider pecked one
            # sentinel 819 times over r181-999 and the escort healed it 819
            # times: one builder's entire action budget and ~1,100-1,200 Ti
            # (about 20% of match income) spent holding a permanently
            # contested building, three matches out of four (heart: 717
            # pecks on a 3-Ti conveyor; meander: 905 heals on a conveyor
            # inside the enemy kill zone that never delivered a stack).  The
            # raider cannot win the tile, but it converts our escort into a
            # 450-820-round income drain, which is a better trade for it.
            # So the escort keeps score: if a guarded building has not been
            # NET-whole for ESCORT_STALL_RNDS consecutive escort rounds, it
            # is written off for good and the escort goes back to work --
            # losing a 3-20 Ti building outright is strictly cheaper than
            # paying its ransom forever.  Per-unit ledger, same locality
            # argument as hunt_defer.
            if self.escort_ban.get(eid, 0) > rnd:
                continue
            bp = ct.get_position(eid)
            d = bp.distance_squared(tp)
            if d > 4:
                continue
            hp = ct.get_hp(eid)
            if hp < ct.get_max_hp(eid):
                stalled = self.escort_watch.get(eid, 0) + 1
                if stalled >= ESCORT_STALL_RNDS:
                    self.escort_ban[eid] = rnd + ESCORT_BAN_RNDS
                    self.escort_watch.pop(eid, None)
                    continue
                self.escort_watch[eid] = stalled
            else:
                # Whole again: the attacker left or died.  Clean slate.
                self.escort_watch.pop(eid, None)
            k = (0 if hp < ct.get_max_hp(eid) else 1, d, eid)
            if best_k is None or k < best_k:
                best, best_k = bp, k
        return best

    def _intercept(self, ct):
        """Chase the owned intruder.  True when this turn was spent on it."""
        if self.core is None or self.enemy is None:
            return False
        p = ct.get_position()
        rnd = ct.get_current_round()
        eid = self._find_intruder(ct)
        if eid is not None:
            self.chase_id = eid
            self.chase_pos = ct.get_position(eid)
            self.chase_seen = rnd
        elif self.chase_id is None:
            return False
        elif (
            rnd - self.chase_seen >= INTRUDER_FORGET_RNDS
            or p == self.chase_pos
            or (
                ct.is_in_vision(self.chase_pos)
                and ct.get_tile_builder_bot_id(self.chase_pos) is None
            )
        ):
            # The trail went cold, or we can see the last sighting and it is
            # empty -- the raider left our half or died.  (Standing on the
            # tile is checked separately: get_tile_builder_bot_id would return
            # our own id there.)  Drop the chase and hand a CLEAN state back to
            # the expand machine below: self.tgt still holds the intruder's
            # tile and self.stuck counted rounds of chasing, so both are
            # cleared exactly as _expand's own retarget branch clears them,
            # forcing a fresh _pick this same turn.  link_queue is positional
            # and survives the interruption untouched.
            self.chase_id = None
            self.chase_pos = None
            self.tgt = None
            self.stuck = 0
            self.wall = None
            return False
        tp = self.chase_pos
        guard = self._guard_target(ct, tp)
        goal = tp if guard is None else guard
        if abs(p.x - goal.x) + abs(p.y - goal.y) == 1:
            # Orthogonally adjacent: act and hold.  Never nav from here --
            # _bfs_direction would aim at the occupied tile, can_move would
            # refuse it, and _nav's fallbacks would slide us off the target.
            if ct.get_action_cooldown() == 0:
                # Piece D: tbid is None for the usual case (the intruder is a
                # builder bot), which _duel_safe passes straight through -- the
                # gate only ever bites on an enemy Gunner/Sentinel standing on
                # the chased tile, where an unsafe duel falls through to the
                # heal branch below instead of feeding the gun.
                try:
                    tbid = ct.get_tile_building_id(tp)
                except Exception:
                    tbid = None
                if guard is not None and ct.can_heal(guard):
                    ct.heal(guard)
                elif ct.can_fire(tp) and self._duel_safe(ct, tp, tbid):
                    ct.fire(tp)
                else:
                    self._heal_adjacent(ct)
            return True
        if ct.get_move_cooldown() == 0:
            self.tgt = goal
            self._nav(ct, pave=False)
        return True

    def _try_choke_wall(self, ct):
        """CHOKEPOINT WALLS (S4): interceptor idle-time barrier plugs.

        Called only from the role_n == 1 branch of _expand (so it is
        reachable only under run()'s try/except), and only after _intercept
        has declined the turn.  The arithmetic that pays for it: each 3 Ti
        barrier is 30 HP, i.e. ~15 builder pecks (2 dmg each, one action per
        round) or 5 gunner shots (7 dmg, ceil(30/7) = 5) at 4 ammo apiece,
        and the ORE_STEPOFF_MIN_WALLS corridor gate at planning time
        guarantees walking around costs a real detour -- tens of rounds of
        rush delay for <= 9 Ti.  Returns True when the turn was spent on
        choke work; after the tile list empties the interceptor resumes its
        normal _expand duties for the rest of the match.
        """
        rnd = ct.get_current_round()
        live = (
            bool(self.choke_tiles)
            and CHOKE_MIN_RND <= rnd <= CHOKE_MAX_RND
            and ct.get_global_resources() >= ct.get_barrier_cost() + CHOKE_TI_RESERVE
        )
        if live:
            # Pop tiles already built -- or lost to any other building (an
            # enemy turret on the site is a plug we do not fight over).
            # Tile getters raise GameError at the vision edge, so the id
            # read is guarded and attempted only in vision; an unreadable
            # tile is KEPT -- fail toward retrying, never toward re-walling
            # a tile we cannot see.
            kept = []
            for t in self.choke_tiles:
                built = False
                if ct.is_in_vision(t):
                    try:
                        built = ct.get_tile_building_id(t) is not None
                    except Exception:
                        built = False
                if not built:
                    kept.append(t)
            self.choke_tiles = kept
        if not live or not self.choke_tiles:
            if self.choke_active:
                # Falling edge: hand a CLEAN state back to the expand
                # machine, exactly as _intercept's disengage does --
                # self.tgt still holds a choke tile the eco machines would
                # never have chosen, and self.stuck counted rounds walking
                # to it.  link_queue is positional and survives untouched.
                self.choke_active = False
                self.tgt = None
                self.stuck = 0
                self.wall = None
            return False
        self.choke_active = True
        p = ct.get_position()
        site = min(self.choke_tiles, key=lambda t: abs(p.x - t.x) + abs(p.y - t.y))
        md = abs(p.x - site.x) + abs(p.y - site.y)
        if md == 0:
            # Standing ON the site: builds are adjacent-only, never
            # own-tile (the ore step-off lesson), so step off first.  All
            # cardinal neighbors are inside own vision (dist^2 <= 1 < 20),
            # so the passability probe cannot raise here.
            if ct.get_move_cooldown() == 0:
                for d in CARDINALS:
                    n = p.add(d)
                    if (
                        0 <= n.x < self.mw and 0 <= n.y < self.mh
                        and ct.is_tile_passable(n) and ct.can_move(d)
                    ):
                        ct.move(d)
                        break
            return True
        if md == 1:
            # Orthogonally adjacent: build and hold.  Never nav from here --
            # _bfs_direction would aim at the target tile itself and the
            # fallbacks would slide us off it (the _intercept adjacency
            # lesson).
            if ct.get_action_cooldown() == 0 and ct.can_build_barrier(site):
                ct.build_barrier(site)
                # Popped optimistically; store/tile writes land next round,
                # and the vision prune above catches it then anyway.
                self.choke_tiles = [
                    t for t in self.choke_tiles
                    if not (t.x == site.x and t.y == site.y)
                ]
            return True
        if ct.get_move_cooldown() == 0:
            self.tgt = site
            self._nav(ct, pave=False)
        return True

    def _chain_dead(self, ct, hpos):
        """True if this friendly harvester's delivery chain is PROVABLY dead.

        Pivot-forensics (2026-08-08): we out-built Pivot in harvesters 2.2x
        and still ran fewer DELIVERING mines for 600+ turns -- a launcher
        parked on a committed link path, sniped trunk conveyors never
        re-laid, diagonal-only "chains", and _link_path() == [] orphaning a
        site forever.  Every deficit bucket was exactly (their delivering
        mines - ours) x 250 Ti; the win run on the identical tape differed
        only in connectivity (+6,600 swing).  Unknown (out of vision) reads
        as HEALTHY -- this detector only convicts on visible evidence.
        """
        start_pos = start_id = None
        saw_all = True
        for d in CARDINALS:
            n = hpos.add(d)
            if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                continue
            try:
                bid = ct.get_tile_building_id(n)
            except Exception:
                saw_all = False
                continue
            if bid is None:
                continue
            try:
                if (
                    ct.get_team(bid) == self.team
                    and ct.get_entity_type(bid) in (EntityType.CONVEYOR, EntityType.SPLITTER)
                ):
                    start_pos, start_id = n, bid
                    break
            except Exception:
                saw_all = False
        if start_id is None:
            # no orthogonal chain start; convict only on full visibility
            return saw_all
        cur_pos, cur_id = start_pos, start_id
        for _ in range(12):
            try:
                f = ct.get_direction(cur_id)
            except Exception:
                return False
            nxt = cur_pos.add(f)
            if self.core is not None and dist_core(nxt, self.core) == 0:
                return False
            if not (0 <= nxt.x < self.mw and 0 <= nxt.y < self.mh):
                return True
            try:
                nid = ct.get_tile_building_id(nxt)
            except Exception:
                return False
            if nid is None:
                return True
            try:
                net = ct.get_entity_type(nid)
                if ct.get_team(nid) != self.team:
                    return True
            except Exception:
                return False
            if net == EntityType.CORE:
                return False
            if net not in (EntityType.CONVEYOR, EntityType.SPLITTER):
                return True
            cur_pos, cur_id = nxt, nid
        return False

    def _link_path(self, ct, hpos):
        raw_goals = set()
        for c in core_tiles(self.core):
            for d in CARDINALS:
                t = c.add(d)
                if 0 <= t.x < self.mw and 0 <= t.y < self.mh and dist_core(t, self.core) > 0:
                    raw_goals.add((t.x, t.y))
        start = (hpos.x, hpos.y)
        if start in raw_goals or not raw_goals:
            return []

        # On a known pool map, grow one deterministic reverse tree from every
        # valid Core input.  All harvester chains therefore agree on conveyor
        # direction when they merge.  Other ore is reserved for Harvesters.
        if self.map_grid is not None:
            blocked = set(self.map_walls)
            blocked.update((o.x, o.y) for o in self.map_ores if (o.x, o.y) != start)
            for c in core_tiles(self.core):
                blocked.add((c.x, c.y))
            try:
                for eid in ct.get_nearby_buildings():
                    ep = ct.get_position(eid)
                    key = (ep.x, ep.y)
                    et = ct.get_entity_type(eid)
                    if key == start:
                        continue
                    if et == EntityType.CORE:
                        blocked.update((c.x, c.y) for c in core_tiles(ep))
                    elif et not in (EntityType.CONVEYOR, EntityType.SPLITTER):
                        blocked.add(key)
                    elif ct.get_team(eid) != self.team:
                        blocked.add(key)
                    else:
                        # Own conveyor whose OUTFLOW is visibly blocked by a
                        # non-conveyor building is a dead trunk -- merging a
                        # replan into it recreates the fault it bypasses
                        # (the archipelago launcher-on-path case).
                        try:
                            _f = ct.get_direction(eid)
                            _ot = ep.add(_f)
                            _oid = ct.get_tile_building_id(_ot)
                            if _oid is not None and ct.get_entity_type(_oid) not in (
                                EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.CORE,
                            ):
                                blocked.add(key)
                        except Exception:
                            pass
            except Exception:
                pass
            goals = {g for g in raw_goals if g not in blocked}
            parent = {g: None for g in goals}
            q = deque(goals)
            link_bfs_steps = 0
            while q and start not in parent:
                x, y = q.popleft()
                link_bfs_steps += 1
                if link_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                    # `start` is still not in `parent` at this point (if it
                    # were, the while condition above would already be
                    # False), so breaking here falls straight into the
                    # existing "not found" return just below -- the same
                    # path a search that genuinely exhausts the map takes.
                    break
                for d in CARDINALS:
                    n = Position(x, y).add(d)
                    key = (n.x, n.y)
                    if (
                        key in parent or key in blocked
                        or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                    ):
                        continue
                    parent[key] = (x, y)
                    q.append(key)
            if start not in parent:
                return []
            path = []
            cur = start
            while parent[cur] is not None:
                cur = parent[cur]
                path.append(Position(cur[0], cur[1]))
            return path

        # Unknown-map fallback: use every currently sensed wall/building and
        # re-evaluate on future maps rather than requiring a pool lookup.
        goals = raw_goals
        prev = {start: None}
        q = deque([start])
        found = None
        fallback_bfs_steps = 0
        while q:
            x, y = q.popleft()
            fallback_bfs_steps += 1
            if fallback_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                # `found` stays None, which falls straight into the existing
                # "not found" return below -- the same path an exhausted
                # search takes.
                break
            if (x, y) in goals and (x, y) != start:
                found = (x, y)
                break
            for d in CARDINALS:
                n = Position(x, y).add(d)
                key = (n.x, n.y)
                if key in prev or not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                    continue
                if dist_core(n, self.core) == 0:
                    continue
                try:
                    if ct.get_tile_env(n) == Environment.WALL:
                        continue
                except Exception:
                    pass
                try:
                    bid = ct.get_tile_building_id(n)
                except Exception:
                    bid = None
                if bid is not None and key not in goals:
                    try:
                        et = ct.get_entity_type(bid)
                        if et not in (EntityType.CONVEYOR, EntityType.SPLITTER, EntityType.HARVESTER):
                            continue
                    except Exception:
                        continue
                prev[key] = (x, y)
                q.append(key)
        if found is None:
            return []
        path, cur = [], found
        while cur is not None and cur != start:
            path.append(Position(cur[0], cur[1]))
            cur = prev[cur]
        path.reverse()
        return path

    def _build_next_link(self, ct):
        if not self.link_queue or not self._eco_spendable(ct, ct.get_conveyor_cost()):
            return False
        p = ct.get_position()
        while self.link_queue:
            tile = self.link_queue[0]
            # Tile queries are vision-limited.  Walk into build range before
            # inspecting the next planned segment.
            if abs(p.x - tile.x) + abs(p.y - tile.y) > 1:
                return False
            if ct.get_tile_building_id(tile) is not None:
                self.link_queue.pop(0)
                continue
            if p.x == tile.x and p.y == tile.y:
                return False
            break
        if not self.link_queue:
            ct.write_store(SLOT_LINKS_DONE, ct.read_store(SLOT_LINKS_DONE) + 1)
            return False
        tile = self.link_queue[0]
        target = nearest_core_tile(tile, self.core)
        if len(self.link_queue) >= 2:
            f = tile.cardinal_direction_to(self.link_queue[1])
            if f == Direction.CENTRE:
                f = nearest_cardinal(tile.direction_to(target))
        else:
            f = nearest_cardinal(tile.direction_to(target))
        if f == Direction.CENTRE:
            f = Direction.NORTH
        if ct.can_build_conveyor(tile, f):
            ct.build_conveyor(tile, f)
            self.link_queue.pop(0)
            if not self.link_queue:
                ct.write_store(SLOT_LINKS_DONE, ct.read_store(SLOT_LINKS_DONE) + 1)
            return True
        return False

    def _step_off_link(self, ct):
        """Vacate the planned conveyor cell so it can be built next round."""
        p = ct.get_position()
        dirs = []
        if len(self.link_queue) >= 2:
            dirs.append(p.cardinal_direction_to(self.link_queue[1]))
        desired = p.cardinal_direction_to(self.core)
        if desired in CARDINALS:
            i = CARDINALS.index(desired)
            dirs.extend((CARDINALS[(i + 1) % 4], CARDINALS[(i - 1) % 4], desired.opposite()))
        dirs.extend(CARDINALS)
        seen = set()
        for d in dirs:
            if d == Direction.CENTRE or d in seen:
                continue
            seen.add(d)
            if ct.can_move(d):
                ct.move(d)
                return True
        return False

    def _pick(self, ct):
        if self.map_ores and self.role == "expand":
            # Static role partitions avoid four builders racing toward the same
            # deposit.  Each partition starts in our half and eventually sweeps
            # the whole map if the match lasts long enough.
            small = self.mw * self.mh <= 220
            workers = 2 if small else 4
            worker = max(0, self.role_n - 1) % workers
            ordered = sorted(
                self.map_ores,
                key=lambda t: (
                    abs(t.x - self.core.x) + abs(t.y - self.core.y),
                    (t.x * 17 + t.y * 31 + worker * 7) % 97,
                ),
            )
            assigned = ordered[worker::workers] or ordered
            for _ in range(len(assigned)):
                t = assigned[self.ore_cursor % len(assigned)]
                self.ore_cursor += 1
                if ct.is_in_vision(t) and ct.get_tile_building_id(t) is not None:
                    continue
                return t

        ores = [t for t in ct.get_nearby_tiles()
                if ct.get_tile_env(t) == Environment.ORE_TITANIUM and ct.get_tile_building_id(t) is None]
        if ores:
            return min(ores, key=lambda t: dist_core(t, self.core))
        r = 3 + (ct.get_current_round() // 30) + (self.idx % 5)
        self.ang = (self.ang + 0.65) % (2 * math.pi)
        return Position(
            max(0, min(self.core.x + int(r * math.cos(self.ang)), self.mw - 1)),
            max(0, min(self.core.y + int(r * math.sin(self.ang)), self.mh - 1)),
        )

    def _bfs_direction(self, ct, target):
        """Return one exact static-terrain step, with visible units avoided."""
        p = ct.get_position()
        if self.map_grid is None:
            return p.cardinal_direction_to(target)

        blocked = set(self.map_walls)
        if self.core is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.core))
        if self.enemy is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.enemy))
        try:
            for eid in ct.get_nearby_entities():
                if eid == ct.get_id():
                    continue
                et = ct.get_entity_type(eid)
                ep = ct.get_position(eid)
                if et == EntityType.CORE:
                    blocked.update((c.x, c.y) for c in core_tiles(ep))
                elif et in (
                    EntityType.GUNNER, EntityType.SENTINEL, EntityType.LAUNCHER,
                    EntityType.HARVESTER, EntityType.BARRIER,
                ):
                    blocked.add((ep.x, ep.y))
        except Exception:
            pass
        start = (p.x, p.y)
        blocked.discard(start)

        tkey = (target.x, target.y)
        if tkey not in blocked:
            goals = {tkey}
        elif target == self.core or target == self.enemy:
            goals = set()
            for c in core_tiles(target):
                for d in CARDINALS:
                    qpos = c.add(d)
                    key = (qpos.x, qpos.y)
                    if (
                        0 <= qpos.x < self.mw and 0 <= qpos.y < self.mh
                        and dist_core(qpos, target) > 0 and key not in blocked
                    ):
                        goals.add(key)
        else:
            goals = {
                (qpos.x, qpos.y)
                for d in CARDINALS for qpos in (target.add(d),)
                if 0 <= qpos.x < self.mw and 0 <= qpos.y < self.mh
                and (qpos.x, qpos.y) not in blocked
            }
        if start in goals:
            return Direction.CENTRE
        if not goals:
            return p.cardinal_direction_to(target)

        desired = p.cardinal_direction_to(target)
        if desired in CARDINALS:
            i = CARDINALS.index(desired)
            side = 1 if (self.idx & 1) else -1
            order = [
                desired, CARDINALS[(i + side) % 4],
                CARDINALS[(i - side) % 4], desired.opposite(),
            ]
        else:
            order = CARDINALS
        seen = {start}
        q = deque([(p.x, p.y, Direction.CENTRE)])
        nav_bfs_steps = 0
        while q:
            x, y, first = q.popleft()
            nav_bfs_steps += 1
            if nav_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                # Same fallback this function already returns a few lines
                # above (goals empty) and below (search exhausted): one
                # direct cardinal step toward the target. Pure function, no
                # instance state, so bailing here is trivially safe.
                return p.cardinal_direction_to(target)
            for d in order:
                n = Position(x, y).add(d)
                key = (n.x, n.y)
                if (
                    key in seen or key in blocked
                    or not (0 <= n.x < self.mw and 0 <= n.y < self.mh)
                ):
                    continue
                first_step = d if first == Direction.CENTRE else first
                if key in goals:
                    return first_step
                seen.add(key)
                q.append((n.x, n.y, first_step))
        return p.cardinal_direction_to(target)

    def _nav(self, ct, pave=True):
        if self.tgt is None or ct.get_move_cooldown() != 0:
            return
        p = ct.get_position()
        desired = self._bfs_direction(ct, self.tgt)
        if desired == Direction.CENTRE:
            return
        if self._move(ct, desired, pave):
            return
        idx = CARDINALS.index(desired) if desired in CARDINALS else 0
        for d in (CARDINALS[(idx + 1) % 4], CARDINALS[(idx + 3) % 4], desired.opposite()):
            if self._move(ct, d, pave):
                return
        self.stuck += 1

    def _move(self, ct, d, pave=True):
        if d == Direction.CENTRE:
            return False
        p0 = ct.get_position()
        nxt = p0.add(d)
        if not (0 <= nxt.x < self.mw and 0 <= nxt.y < self.mh):
            return False
        # Pave toward core, but still attempt move (don't treat pave-only as success)
        # HIVE EXCLUSION for the trail pave.  Diagnosed on hive seat-A vs
        # kladde_probe (seeds 2/5/9, deterministic): a single walk-direction
        # pave at r22 -- an ore-forager stepping through (4,18) -- faced a
        # dead end, and _build_next_link's "occupied implies correct" skip
        # then routed the (17,17) harvester's trunk chain through it 40
        # rounds later: one fewer DIRECTED harvester forever, collection
        # flatlined at 1080 from r250, core dead r717.  F-off wins the same
        # game r325.  Not a volume effect (both variants build exactly 40
        # conveyors).  On this map the geometry-derived old rule never makes
        # the mistake, so hive falls through to it -- same per-map idiom as
        # hive_freeze/hive_bunker.  The root fix (linker verifies facing and
        # destroy()+rebuilds wrong heads -- destroy is measured free) is the
        # follow-on, not this gate.
        hive_map = self.mw == 25 and self.mh == 25 and self.core is not None \
            and (self.core.x, self.core.y) in ((2, 20), (21, 3))
        if PAVE_TRAIL_ON and not hive_map:
            # PIECE F: pave the tile we just LEFT, facing the direction we just
            # MOVED, so its output tile is the one we now stand on -- the next
            # tile of the same trail.  pave_prev is one cardinal step away by
            # construction and pave_dir is always cardinal (moves are
            # cardinal-only), so both legality preconditions are free.
            pp = self.pave_prev
            if pp is not None and self.pave_rnd != ct.get_current_round() - 1:
                pp = None
            if pave and self.core and pp is not None and ct.get_action_cooldown() == 0 and ct.is_tile_empty(pp):
                # ORE PAVE BAN (E2).  Forensic (sporks_g5/fjordgate ghost,
                # lost all 3 salts with 0-120 mined): after the opening rush
                # killed our harvesters, this very trail laid conveyors
                # directly ON ore tiles (8,1)/(3,9)/(1,8) at t=24/30/57,
                # permanently occupying 3 of the map's 4 harvester sites --
                # the link machinery pops occupied tiles instead of clearing
                # them, so a conveyor on ore blocks the site for the rest of
                # the game.  Never pave ore.  Unreadable env (tile getters
                # raise GameError outside vision) also skips: fail toward
                # not blocking a mine.
                try:
                    pp_is_ore = ct.get_tile_env(pp) == Environment.ORE_TITANIUM
                except Exception:
                    pp_is_ore = True
                if not pp_is_ore and ct.read_store(SLOT_HARVESTERS) >= 1 and self._eco_spendable(ct, ct.get_conveyor_cost()):
                    if dist_core(pp, self.core) > 0:
                        if dist_core(pp, self.core) == 1:
                            # TERMINAL: pp is adjacent to the footprint.  The
                            # old expression is correct here and ONLY here --
                            # it aims into the Core.  The coreward gate cannot
                            # hold on this step (we are leaving), so it is not
                            # applied: this is the trail's delivery point.
                            facing = nearest_cardinal(pp.direction_to(nearest_core_tile(pp, self.core)))
                            coreward_ok = True
                        else:
                            # INTERIOR: output == the tile we now stand on.
                            facing = self.pave_dir
                            coreward_ok = (
                                abs(p0.x - self.core.x) + abs(p0.y - self.core.y)
                                < abs(pp.x - self.core.x) + abs(pp.y - self.core.y)
                            )
                        if coreward_ok and facing is not None and ct.can_build_conveyor(pp, facing):
                            ct.build_conveyor(pp, facing)
        elif pave and self.core and ct.is_tile_empty(nxt) and ct.get_action_cooldown() == 0:
            # ORE PAVE BAN (E2), same rule as the trail branch above: never
            # lay a conveyor on an ore tile (fjordgate ghost: paves ON ore
            # (8,1)/(3,9)/(1,8) at t=24/30/57 froze 3 of 4 harvester sites
            # for the whole game).  Unreadable env = skip the pave.
            try:
                nxt_is_ore = ct.get_tile_env(nxt) == Environment.ORE_TITANIUM
            except Exception:
                nxt_is_ore = True
            if not nxt_is_ore and ct.read_store(SLOT_HARVESTERS) >= 1 and self._eco_spendable(ct, ct.get_conveyor_cost()):
                if dist_core(nxt, self.core) > 0:
                    here = ct.get_position()
                    if abs(nxt.x - self.core.x) + abs(nxt.y - self.core.y) < abs(here.x - self.core.x) + abs(here.y - self.core.y):
                        card = nearest_cardinal(nxt.direction_to(nearest_core_tile(nxt, self.core)))
                        if ct.can_build_conveyor(nxt, card):
                            ct.build_conveyor(nxt, card)
        if ct.can_move(d):
            ct.move(d)
            if PAVE_TRAIL_ON:
                self.pave_prev = p0
                self.pave_dir = d
                self.pave_rnd = ct.get_current_round()
            return True
        return False

    def _turret(self, ct):
        if self.team is None:
            self.team = ct.get_team()
        p = ct.get_position()
        turret_type = ct.get_entity_type()
        enemy_anchor = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        healer_focus = (
            ct.get_map_width() == 26 and ct.get_map_height() == 26
            and enemy_anchor is not None
            and enemy_anchor.x == 5 and enemy_anchor.y == 5
        )
        if turret_type == EntityType.GUNNER:
            tgt = ct.get_gunner_target()
            if tgt is not None and ct.can_fire(tgt):
                bid = ct.get_tile_building_id(tgt)
                bot = ct.get_tile_builder_bot_id(tgt)
                hostile = (
                    (bid is not None and ct.get_team(bid) != self.team)
                    or (bot is not None and ct.get_team(bot) != self.team)
                )
                if hostile:
                    ct.fire(tgt)
                    return

        # Sentinels pierce intervening units; scan their whole line and prefer
        # the Core, then combat units/builders, then economic infrastructure.
        try:
            best = None
            best_prio = 99
            for t in ct.get_attackable_tiles():
                bid = ct.get_tile_building_id(t)
                bot = ct.get_tile_builder_bot_id(t)
                et = None
                if bid is not None and ct.get_team(bid) != self.team:
                    et = ct.get_entity_type(bid)
                elif bot is not None and ct.get_team(bot) != self.team:
                    et = EntityType.BUILDER_BOT
                if et is None or not ct.can_fire(t):
                    continue
                if healer_focus:
                    prio = {
                        EntityType.BUILDER_BOT: 0, EntityType.CORE: 1,
                        EntityType.SENTINEL: 2, EntityType.GUNNER: 3,
                        EntityType.LAUNCHER: 4, EntityType.HARVESTER: 5,
                        EntityType.CONVEYOR: 6, EntityType.SPLITTER: 6,
                        EntityType.BARRIER: 7,
                    }.get(et, 8)
                else:
                    prio = {
                        EntityType.CORE: 0, EntityType.SENTINEL: 1,
                        EntityType.GUNNER: 2, EntityType.BUILDER_BOT: 3,
                        EntityType.LAUNCHER: 4, EntityType.HARVESTER: 5,
                        EntityType.CONVEYOR: 6, EntityType.SPLITTER: 6,
                        EntityType.BARRIER: 7,
                    }.get(et, 8)
                if prio < best_prio:
                    best_prio, best = prio, t
            if best is not None:
                ct.fire(best)
                return
        except Exception:
            pass
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) != self.team and ct.can_fire(ct.get_position(eid)):
                ct.fire(ct.get_position(eid))
                return
        enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        best = 10**9
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            ep = ct.get_position(eid)
            d = p.distance_squared(ep)
            if d < best:
                best, enemy = d, ep
        if enemy is not None and turret_type == EntityType.GUNNER:
            want = p.direction_to(enemy)
            if want != Direction.CENTRE and want != ct.get_direction():
                if ct.can_rotate(want):
                    ct.rotate(want)
                else:
                    card = nearest_cardinal(want)
                    if card != ct.get_direction() and ct.can_rotate(card):
                        ct.rotate(card)

    def _launcher(self, ct):
        if self.team is None:
            self.team = ct.get_team()
        ct.write_store(SLOT_LAUNCHER, 1)
        if self.core is None:
            for eid in ct.get_nearby_buildings():
                if ct.get_entity_type(eid) == EntityType.CORE and ct.get_team(eid) == self.team:
                    self.core = ct.get_position(eid)
                    break
        if self.core is None:
            return
        w, h = ct.get_map_width(), ct.get_map_height()
        dest = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if dest is None:
            dest = Position(max(0, w - 2 - self.core.x), max(0, h - 2 - self.core.y))

        drop_sites = []
        for c in core_tiles(dest):
            for d in CARDINALS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) == 1:
                    drop_sites.append(t)
        for c in core_tiles(dest):
            for d in DIRECTIONS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) == 1:
                    drop_sites.append(t)
        for c in core_tiles(dest):
            for d in DIRECTIONS:
                t = c.add(d)
                if 0 <= t.x < w and 0 <= t.y < h and dist_core(t, dest) > 0:
                    drop_sites.append(t)
        seen, uniq = set(), []
        for s in drop_sites:
            key = (s.x, s.y)
            if key not in seen:
                seen.add(key)
                uniq.append(s)
        drop_sites = uniq

        lp = ct.get_position()
        cands = []
        chosen = ct.read_store(SLOT_LAUNCH_ID)
        chosen_rnd = ct.read_store(SLOT_LAUNCH_RND)
        if chosen and ct.get_current_round() - chosen_rnd > 5:
            ct.write_store(SLOT_LAUNCH_ID, 0)
            chosen = 0
        for eid in ct.get_nearby_entities():
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT or ct.get_team(eid) != self.team:
                continue
            if not chosen or eid + 1 != chosen:
                continue
            bp = ct.get_position(eid)
            if bp.distance_squared(lp) > 49:
                continue
            cands.append((bp.distance_squared(lp), bp))
        cands.sort(key=lambda x: x[0])

        # A Launcher can also remove a hostile bot that walks into its pickup
        # ring. Throw it to the legal tile farthest from our Core.
        enemy_bots = []
        for eid in ct.get_nearby_entities():
            if ct.get_entity_type(eid) != EntityType.BUILDER_BOT or ct.get_team(eid) == self.team:
                continue
            bp = ct.get_position(eid)
            if bp.distance_squared(lp) <= 2:
                enemy_bots.append(bp)
        for bp in enemy_bots:
            exile = []
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx * dx + dy * dy > 26:
                        continue
                    t = Position(lp.x + dx, lp.y + dy)
                    if 0 <= t.x < w and 0 <= t.y < h:
                        exile.append(t)
            exile.sort(key=lambda t: t.distance_squared(self.core), reverse=True)
            for site in exile:
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    return

        for _, bp in cands:
            for site in drop_sites:
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                    ct.write_store(SLOT_LAUNCHED_ID, chosen)
                    ct.write_store(SLOT_LAUNCH_ID, 0)
                    return
            if ct.can_launch(bp, dest):
                ct.launch(bp, dest)
                ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                ct.write_store(SLOT_LAUNCHED_ID, chosen)
                ct.write_store(SLOT_LAUNCH_ID, 0)
                return

            # Most maps are wider than the Launcher's sqrt(26) throw radius.
            # Leap the waiting bot as far toward the enemy as the local terrain
            # permits instead of idling forever on an impossible destination.
            advance = []
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx * dx + dy * dy > 26:
                        continue
                    site = Position(lp.x + dx, lp.y + dy)
                    if 0 <= site.x < w and 0 <= site.y < h:
                        advance.append(site)
            advance.sort(key=lambda t: t.distance_squared(dest))
            for site in advance:
                if site.distance_squared(dest) >= bp.distance_squared(dest):
                    continue
                if ct.can_launch(bp, site):
                    ct.launch(bp, site)
                    ct.write_store(SLOT_DROPPED, ct.read_store(SLOT_DROPPED) + 1)
                    ct.write_store(SLOT_LAUNCHED_ID, chosen)
                    ct.write_store(SLOT_LAUNCH_ID, 0)
                    return
