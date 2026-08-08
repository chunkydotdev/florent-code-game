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

# RIDE-ALONG 2 (Eir 6) -- BUILDER POPULATION FLOOR, sporks mechanism #7.
# Decoded across 25 sporks games: five builders at rounds 0,1,2,3,4 in 25/25,
# and 9 of its 10 LOSSES never spawned a sixth -- i.e. the floor is a hard
# structural property and expansion above it happens only when income has
# actually been realised.  Our own B' is aimed at the same symptom with the
# wrong constant: REPLACE_TI_FLOOR = 250 is unmeetable exactly when it is
# needed (the decoded hive loss held a 2-12 Ti bank for 500 rounds), so a
# population crash never refills -- the eider race lost 586 rounds on two live
# hands, and the hive siege could never hold HUNT_MIN_HEALERS.
#
# Two clauses, deliberately split:
#  - REFILL to the floor: no titanium floor, no round floor.  A body costs the
#    scaled builder cost and nothing else, and a bank that cannot afford one
#    body cannot afford anything else either, so the bank read is the only
#    gate.  The floor is min(POP_FLOOR, spawn_cap) so the two measured map
#    caps (nordkap 4, snowflake 6) still own their own numbers.
#  - EXPANSION above the floor: gated on the estimated delivered-Ti RATE
#    rather than on a bank threshold, which is sporks' rule.  A bank threshold
#    passes on a hoard that a strangled economy will never rebuild; a rate
#    threshold passes only while harvesters are actually running.  The opening
#    round floor is kept here (and only here) because a builder is the joint
#    most scale-expensive entity at +20% and inflating that curve early is the
#    measured _v69bc failure (-13 pts).
#
# The Core cannot count live builders (see the REPLACEMENT ACCOUNTING block
# below); _live_builders takes the best of two cheap LOWER bounds instead.
#
# ON as of Eir 6b.  Isolated on its own leg after the Eir 6 refutation and
# measured CLEAN: vs opp_v63 60.0 (the all-off control exactly), vs band_probe
# 88.3 (baseline exactly) and vs orizon_probe 71.7 against a 58.3 baseline,
# i.e. +13.4 on the rush family this floor was aimed at, with 0 crashes in 180
# games.  It rides along with K' by the pre-stated decision rule; the toggle
# stays live so the ablation matrix can still lift it out.
POP_FLOOR_ON = True
POP_FLOOR = 5
# Estimated delivered titanium per round required before spawning ABOVE the
# floor.  See the INCOME METER in _core for how the estimate is built; at the
# metered half-rate this is roughly "five harvesters are running".
POP_EXPAND_TI_RATE = 8
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
# Hunt band past Sentinel range, footprint-measured (see _hunt_turret; the
# constant and its two validations -- the CtrlAltDefeat decode and the v79
# jackpot sweep -- are documented at the use site).
HUNT_BAND_DSQ = 41
# Ore step-off wall gate (see _expand; v79's constant, copied with his
# rationale): 80+ walls marks the corridor maps where ore-squatting becomes a
# permanent park.  heart 28x20 has 122; atoll, where squatting is GOOD, 18.
ORE_STEPOFF_MIN_WALLS = 80

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

# PIECE K' -- BUDGETED CORE HEAL (SIEGE-GATED) + STANDING TRUNK REPAIR.
# Piece J's heal-dispatch reorder is the right mechanism at the wrong scope,
# and BOTH halves of that are measured.
#
# Too NARROW, from the sporks decode.  sporks holds its Core at 500 HP through
# point-blank sieges by healing continuously as an income LINE ITEM: ed29909b
# g1 is 723 heal actions = 723 Ti = 4.6% of the 15,880 Ti it delivered, Core
# restored 369 -> 500 and held there for 328 rounds, win.  The contrast game in
# the same series against the identical opponent, ed29909b g4: ZERO heal
# actions, Core 500 -> 178 -> dead at r63.  Pooled: wins median 290 heal
# actions and Core-minimum 378 HP, losses 84 and 0.  Against our own pool this
# is the structural answer to the Orizon / team lazy / Team 48 / Leviathan
# family, which kills in r64-119 and therefore outruns every round-gated
# defense this file has (HUNT_MIN_RND 120, MEDIC_MIN_RND 150, and the medic's
# own early window at 40).  So K's TRUNK repair runs from round 0 and for
# every role, not only for expanders -- conveyors, splitters and harvesters
# standing beside the healer, on top of the Core heal this file already had.
#
# Too WIDE, from our own production tape.  v65 antler g4: 972 heal actions in
# one game with builders demonstrably alive, and piece H's endgame harvester
# arm NEVER fired in any of three r1000 games -- because the heal at the top of
# _builder returns before role dispatch is ever reached, so an unbudgeted
# heal-priority silently claims every builder action for the whole siege.  An
# absolute priority is not a policy; a budget is.
#
# The budget.  1 Ti per heal action, capped at K_HEAL_RATE_PCT of estimated
# cumulative income plus a K_HEAL_BASE_GRANT seed so an r64 siege is never
# budget-blocked before any income exists.  5% is sporks' measured 4.6%,
# rounded to the nearest whole percent.  UNDER budget the heal keeps piece J's
# priority (it claims the turn, above role dispatch).  OVER budget it claims
# nothing and dispatch proceeds normally -- which is precisely the 972-heal
# failure mode, made impossible rather than merely discouraged.
#
# Accounting is PER UNIT, not team-wide, and that is deliberate: store writes
# are buffered one round and last-write-wins WITHIN a round, so N concurrent
# healers incrementing one slot would advance it by 1, not by N, and the
# ledger would under-count exactly when the heal line is thickest -- i.e. it
# would fail open, in the direction of the bug being fixed.  Instead the Core
# (a single writer, no contention possible) publishes the income-proportional
# part of the TEAM budget, and each builder spends at most its own
# 1/K_HEAL_SHARES share of it, tracked in plain instance state that no other
# unit can corrupt.  A seat that never heals leaves its share unspent, so the
# team total errs low -- the safe direction for a cap.
#
# Only the heals taken by K's own priority block are charged to the ledger.
# _expand's chain medic and _defend's heal fallbacks are deliberately outside
# it: both are already ordered LAST in their action phase and so cannot
# pre-empt higher-value work, which is the only thing the budget exists to
# bound.
#
# WHAT K v1 GOT WRONG (Eir 6, measured and refuted; this file is the redesign).
# Two independent errors, one per half, and they are opposites -- the Core half
# fired far too often and the trunk half never fired at all.
#
#  1. THE CORE HALF DROPPED THE SIEGE GATE.  v1 read "sporks heals as an income
#     line item" as a licence to delete Eir 5.1's SLOT_UNDER gate on the Core
#     heal outright, and that single deletion is the whole refutation: builders
#     spent 27-31% of their turns, from round 0 onward, healing an undamaged or
#     barely-scratched Core instead of acting -- ~15 pts vs opp_v63 and ~35 pts
#     vs band_probe.  can_heal() refusing a FULL-HP Core is not the safety
#     property v1 assumed it was: a Core one peck down is "damaged", and an
#     absolute-priority block then buys +4 HP that nothing is threatening with a
#     turn that had real work in it.  So the gate is restored here exactly as
#     Eir 5.1 shipped it (SLOT_UNDER != 0, the 50-round latch).  What makes the
#     restoration safe -- and this is the whole reason v1 dropped it -- is that
#     the 972-heal starvation the gate was blamed for is now bounded by the
#     BUDGET instead.  The gate and the cap are independent guards on different
#     failures (wrong ROUNDS vs wrong VOLUME); v1 traded a working guard for a
#     new one where it should have stacked them.
#  2. THE TRUNK HALF NEVER FIRED, in any game.  v1 qualified a structure only at
#     MEDIC_EARLY_MIN_DMG = 8 damage or deeper before MEDIC_MIN_RND, borrowing
#     the chain medic's depth discriminator.  But the raiders that matter chip
#     in 2s (a builder peck) and 7s (a gunner, reload 1) into 20-HP conveyors,
#     so a tile is essentially never at rest inside that window -- it is above
#     the bar or it is rubble.  Dead code.  K' replaces the depth gate with the
#     sporks rule it was meant to encode: repair ANY damaged trunk building we
#     are standing beside, while our own budget share allows.  Loose is safe
#     here in a way it is NOT for the Core, because the budget is the bound and
#     because the tempo tax the depth gate was written against (the fjordgate
#     and lighthouse opening flips) was measured on the UNBUDGETED chain medic;
#     every trunk heal K' takes is charged to the same K_HEAL_SHARES ledger and
#     stops dead when that share is spent.
K_HEAL_BUDGET_ON = True
K_HEAL_BASE_GRANT = 30
K_HEAL_RATE_PCT = 5
K_HEAL_SHARES = MAX_BUILDERS
# Quarter-titanium per round credited to the income meter for each harvester
# in SLOT_HARVESTERS.  A connected harvester delivers a 10-stack every 4
# rounds, i.e. 10 quarter-Ti per round; this credits HALF of that because
# SLOT_HARVESTERS is a monotone high-water mark of harvesters BUILT and the
# v79 directed-connectivity audit found only a fraction of live harvesters
# actually delivering (atoll 2 of 5, heart 2 of 5, jackpot 2 of 3, meander 1
# of 7 -- docs/v79-analysis.md:178-179).  Over-crediting income would inflate
# the cap, which is the one direction a safety cap must not err in.
K_HEAL_HARV_Q = 5

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
NOISE_ON = True

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

# PIECE I -- ROTATION DISCIPLINE.  _turret's idle tail rotates a Gunner toward
# the nearest visible enemy on a bare 45-degree bearing: no ray check
# (can_fire_from is never called in _turret today), no memory of the previous
# target, no cost awareness.  Measured over 8 games: 446 rotations = 4,460 Ti,
# worst case 3,250 Ti = 56.5% of that game's whole income (a5671738 g1,
# drumlin, 325 rotations), and 146 A->B->A reversals on ONE gunner
# (8ed4d332 g4).  Every rotate is 10 Ti competing directly with the heal line
# and the respawn floor AND sets action cooldown 1, i.e. it also cancels the
# shot it was supposedly aiming.
#
# Three rules, all of them cheap:
#  1. RAY CHECK.  Rotate only if can_fire_from(p, want, GUNNER, target) is
#     True for the candidate facing AND False for the CURRENT one (already
#     covered => the rotation buys nothing).  can_fire_from ignores ammo and
#     cooldown by contract, which is exactly the question being asked here.
#  2. HYSTERESIS.  self.rot_tgt holds the tile we are currently aimed at; a
#     new candidate has to be 3x closer in dsq to steal the facing.  This is
#     what kills the A->B->A reversals -- two enemies at similar range can no
#     longer trade the gunner back and forth every round.
#  3. NO CHASING BUILDERS PAST RANGE.  Builder bots move every round and
#     outrun a facing by construction; they are the drumlin thrash source.
#     They are only considered inside gunner attack range r^2 <= 13, where
#     rule 1 can still land a real shot.
# Rotating toward the stored enemy-Core bearing when nothing is visible stays
# exempt from rule 1 (the anchor is far past r^2=13, so a ray check would
# simply delete the behaviour): it is self-limiting instead -- p and the
# anchor are both fixed, so `want` is a constant and the second call already
# finds want == current.  At most one such rotation per gunner lifetime.
ROTATE_DISCIPLINE_ON = True
# Gunner vision/attack radius squared (GameConstants is not imported here).
GUNNER_RANGE_DSQ = 13

# ROTATION LATCH (Eir 5.1 hotfix).  Piece I as shipped in v65 was VERIFIED in 9
# of 10 production games -- 2 / 5 / 0 / 0 rotations vs Memtrace v27, 0 / 0 / 3 /
# 0 / 0 vs Ouroboros v8 -- and blew up in exactly one configuration: nordkap g3,
# the `chase_battery` map special case (20x26, home Core (9,6)).  166 rotations
# with 50 A->B->A reversals = 1,660 Ti burned in a game we lost on
# titanium_collected, and the burn also starved piece H: the bank at r960 was
# 243 against a 14,634 dump in the healthy game.
#
# Mechanism, from the code: rules 1-3 all pass, every round, honestly.  A gunner
# sees r^2 = 13, so under chase_battery two enemies sit inside the ring and BOTH
# land a ray.  The hysteresis latch that is supposed to settle that contest is
# keyed on a TILE (self.rot_tgt) whose liveness is tested with _hostile_at -- so
# the instant the held enemy is a builder bot that steps one tile, the latch
# reads "not live", drops for free, and the rival takes the facing.  Next round
# the first one steps back and takes it back.  Rule 2 never sees a contest at
# all: from its side each flip is a first acquisition.
#
# The fix is a TIME latch, which does not care why the tile went stale.  After
# any rotation this gunner refuses to rotate again for ROTATE_COOLDOWN_RNDS
# rounds unless BOTH
#   (a) the facing it just bought has no hostile left in its line at all, and
#   (b) the new candidate beats the target it bought by rule 2's own 3x dsq
#       margin -- measured against self.rot_lock_d, a number, instead of against
#       a tile that a moving enemy can invalidate;
# and inside that window it never rotates straight back onto the facing it just
# left (self.rot_prev_dir), which is the A->B->A edge itself.  The idle
# Core-bearing re-aim at the bottom of _idle_rotate is suppressed outright in
# the window for the same reason: it buys no shot this turn and it is the free
# way for a gunner to walk its facing back off a real target.
#
# 8 rounds is four gunner shot cycles (reload 1, plus the cooldown 1 the rotate
# itself costs) -- long enough that a facing worth 10 Ti has fired from twice,
# short enough that a genuine breakthrough is still answered inside a siege.
# Worst case the latch costs a gunner ~8 idle rounds; nordkap g3 says the
# uncapped alternative costs 1,660 Ti.
ROTATE_COOLDOWN_RNDS = 8

# PIECE J -- COUNTERBATTERY OVER HEAL, DEFENDER-SCOPED.  Against a POINT-BLANK
# battery (Orizon class, Ouroboros endgame) the defender locks up: piece D's
# _duel_safe correctly refuses the melee duel, _hunt_turret therefore
# disengages, and the universal adjacent heal in _builder (and its
# belt-and-braces twin, heal-first-under-shelling in _defend) then claims the
# defender's action EVERY round -- so _try_counterbattery, the only call site
# in the file that can buy the turret that would return fire, is unreachable
# for the whole siege.  The defender heals +4/round into 18-25 dmg/round and
# loses slowly and predictably.
#
# The exemption is deliberately NARROW.  Heal-first is MEASURED-CORRECT for
# the chip class once a home gun already stands (the heart decode), and Eir 4
# already fixed the two worst consequences (hunt interception above the heal,
# defend-role succession), so this is scoped to the one state where healing
# provably cannot win: the role_n == 4 defender ONLY, with a threat in band,
# NO live home turret, and enough bank to buy a Sentinel without touching
# SIEGE_HEAL_RESERVE_TI.  Every other builder keeps healing -- convergence is
# still supplying +8..12/round while the defender spends its action on the
# gun -- and one in-ray turret flips the arithmetic and ends the exemption.
#
# The "no live home turret" test is a defender-LOCAL scan, not SLOT_HOME_GUN.
# That counter is incremented in three places (including _try_siege_build's
# FORWARD gun at the ENEMY core), never decremented, so it reads 1 for a
# distant siege gun and for rubble alike -- i.e. exactly wrong for a gate that
# means "home defense exists".  A store-decrement scheme is not an option:
# writes are next-round visible and last-write-wins, so concurrent builder
# decrements corrupt.  The live scan costs ~a dozen engine calls on defender
# turns and is always current.  The same substitution defuses _expand's
# hive_freeze, which froze the hive economy on both seats off the same
# monotone counter.
CB_OVER_HEAL_ON = True

# PIECE C1 -- HOME SENTINEL RING.  Counter to the launcher-insertion class
# (CtrlAltDefeat family; Kings College Munich is the measured exemplar, 9-1
# against us -- docs/research/kings-college-classification-2026-08-07.md
# sections 3.3 and 5-C1).
#
# The predictor is one line of that decode: count THEIR turrets ESTABLISHED
# within footprint-dsq 36 of OUR Core.  Three or more, we lost all nine games;
# the single game where they got exactly one -- killed on r19 by a home
# Sentinel already standing in its ray -- we won on the r1000 tiebreak, and it
# is the only game we have ever taken off them.  The arithmetic behind it: a
# Sentinel is 18 dmg on reload 2 at r^2 = 32, so it TWO-SHOTS the 25 HP gunner
# that is their entire offence and three-shots a 30 HP launcher or harvester.
# Our FORWARD sentinels, by contrast, live a measured median of 15 rounds
# against their counter-gunner and land 54-162 damage on a 500 HP Core -- i.e.
# arithmetically incapable of the kill they are built for.
#
# What was missing was never the turret, it was the WALK.  _try_counterbattery
# builds only when the defender ALREADY STANDS orthogonally beside a tile whose
# ray happens to contain the threat; nothing in this file moved a builder TO a
# firing position.  _plan_homering is that planner, modelled on _plan_siege --
# which is the ENEMY-core sibling and is left bit-for-bit alone.  The
# duplication is deliberate: the forward snipe is a separately gated piece and
# the two must stay ablatable apart.
#
# Ring semantics, each measured or arithmetic rather than tuned:
#  - COVERAGE DEDUP.  One turret per live threat: if a live home turret's
#    CURRENT facing already covers the threat tile, a second one buys no extra
#    shots at it and only moves the cost scale.
#  - RING CAP 3.  Their established forward battery tops out at 3 in the
#    corpus, and cost scale is ONE team-wide multiplier (+20% per Sentinel), so
#    an uncapped ring taxes the very economy that won the one game we won.
#  - LIVE COUNTING ONLY -- the piece-J lesson.  SLOT_HOME_GUN is monotone, is
#    incremented by the saboteur's FORWARD gun at the ENEMY Core, and counts
#    rubble forever, so it cannot answer "how many home turrets stand".  Its
#    increments are kept for compatibility; nothing in this piece reads it.
#  - THREAT LIVENESS.  SLOT_THREAT is a tile, not an entity handle, and no
#    writer clears it when its occupant dies (the UNDER latch decays on 50
#    rounds), so a visible-and-empty threat tile buys nothing.
HOME_RING_CAP = 3
# Return-fire penalty, in BFS steps, on a firing position that sits inside a
# live GUNNER threat's own range (GUNNER_RANGE_DSQ = 13).  Their answer to a
# turret is a counter-gunner at d^2 = 2-9, which is also how our forward
# engineers die.  A SENTINEL threat outranges anything we can build (r^2 = 32
# both ways), so no penalty can separate spots against one and none is
# applied.  8 is deliberately below the 20 the in-own-ray penalty carries:
# taking return fire is a cost, standing in our own line is a broken build.
HOME_RING_RETFIRE_PEN = 8
# APPROACH LANE, footprint-dsq.  The tiles an insertion actually plants on --
# the ray-coverage decode (docs/research/kcm-win-c1-validation-2026-08-07.md)
# re-specified this whole piece around them: of 23 enemy turrets that reached
# our home band, the 8 that lay on a reachable friendly firing ray died 8/8 and
# the 15 that did not took ZERO turret shots, 15/15 -- perfect separation, where
# radius-and-count went 3/5 and is refuted in both directions.  9 is that
# decode's own number.
#
# The consequence for PLACEMENT, and the reason lane coverage is ranked above
# walking distance in _plan_homering: a SENTINEL CANNOT BE RE-AIMED.  rotate()
# is gunner-only, and the decode found 0 direction changes on any sentinel in
# 277 turret re-emissions, so a sentinel faced at today's threat tile becomes
# dead weight the round that threat dies.  A facing that also sweeps the
# approach lane keeps earning.  Re-aiming by destroy() + rebuild is
# evidence-plausible and deliberately OUT OF SCOPE here -- every rebuild pays
# the team-wide cost scale again, which makes it its own gated piece.
HOME_RING_LANE_DSQ = 9
C1_HOME_RING_ON = True

# PIECE C1b, MECHANISM A -- INSERTION-CLASS ARMING GATE.  C1 as shipped runs
# the ring against EVERY opponent, and the _v82c1 gate row measured the price:
# the mechanism was 8/8 lethal where it fired, but the leg against the
# non-insertion slot holder (opp_v69) came in at 41.7 against the parent
# lineage's 52.5 -- i.e. the ring is a tax on the games it was never built for.
# The fix is not a weaker ring, it is a ring that does not exist until an
# insertion has been SEEN.
#
# The wild calibration this is sized against
# (docs/research/kcm-wild-establishment-rates-2026-08-07.md, 30 games / 2
# corpora): the insertion class is identifiable at round 1 in 25/25 games, but
# the near-core threat's own arrival is median r12, p75 r29, p90 r93, max r156,
# and 8% of games never get one at all.  So the capacity this gate opens must
# be LATENT -- arming spends no titanium and builds nothing; it only permits
# the ring to answer a threat that has actually arrived.
#
# TWO SIGNATURES, either of which arms for the rest of the game:
#  1. EARLY RAIDER -- an enemy BUILDER_BOT at footprint-dsq <= 64 of our Core
#     before round 30 THAT CANNOT HAVE WALKED THERE.  Radius-and-clock alone
#     was measured refuted on the first smoke pass: opp_v63, a non-insertion
#     opponent, tripped it in 12 of 12 games (its own early saboteur, fp-dsq
#     16-61 by rounds 3-29) -- and on meander at round 3 / fp-dsq 26, which is
#     numerically inside the insertion band.  Distance-and-time do not separate
#     the classes; the THROW does, and the throw is the class.
#
#     The test is a travel budget.  A builder bot moves one CARDINAL step per
#     round at best, and the earliest one can exist is spawned adjacent to its
#     own Core footprint on round 0, so at round R nothing that walked is more
#     than R + 1 Manhattan steps from the enemy footprint.  Past that budget it
#     was carried, and a launcher ferry into our home band IS the insertion
#     class.  Deliberately the MOST PERMISSIVE walk model (1 tile/round, spawn
#     on round 0): every assumption is tilted toward calling an arrival a walk,
#     so the gate errs toward the parent lineage.
#
#     The enemy anchor is SLOT_ENEMY_CORE, or enemy_core_for's symmetry guess
#     before anyone has seen their Core -- a wrong anchor moves the budget, not
#     the shape of the test, and the fallback is the same one the Core itself
#     publishes on round 0.
#
#     Round 30 stays as the outer clock: past it the budget is so large that
#     only a map-crossing throw could beat it, and a genuine late insertion is
#     caught by signature 2 when its turret lands anyway.
#  2. TURRET ARRIVAL -- an enemy GUNNER or SENTINEL at footprint-dsq <= 36, any
#     round.  This is the decode's own establishment predicate, so it arms on
#     the thing the ring exists to kill regardless of how it got there -- which
#     is also why a forward-snipe deployment that parks a gun in our home band
#     CORRECTLY arms us: at that point we are the one being established on.
#
# DIVERGENCE, accepted and documented: arming is a PER-UNIT flag derived from
# that unit's OWN observation.  There is no shared channel for it -- all 16
# store slots are assigned, and the two that fire on attacks cannot carry it:
# SLOT_UNDER is written 0 by the Core when its 50-round latch decays (so it
# cannot latch anything for the game) and SLOT_ATK_RND is consumed as an
# arithmetic round number by that same decay.  SLOT_HOME_GUN has a live reader
# in _core (_live_builders' weapons term), so its high bits are not free
# either.  The consequence: different units arm on different rounds, and a
# defender whose own vision (r^2 = 20) never contained the raider stays unarmed
# while a builder that saw it does not.  It errs toward the parent lineage,
# which is the safe side of this particular trade.
C1B_ARMING_GATE_ON = True
C1B_ARM_RAIDER_DSQ = 64
C1B_ARM_RAIDER_RND = 30
# SIGNATURE 2's radius; set to -1 to ABLATE signature 2 and arm on the throw
# alone.  Smoke-measured 2026-08-07, 12 games each over heart / lighthouse /
# nordkap / snowflake / meander / atoll x 2 seeds: signature 1 alone armed
# 12/12 vs cad_probe (rounds 3-8) and 0/12 vs opp_v63, i.e. PERFECT separation
# on this pair.  With signature 2 live, opp_v63 arms in 10/12 -- always on a
# real enemy Sentinel or Gunner established at fp-dsq 5-34 of our footprint,
# median round ~30 (range 4-96, 2/12 never), which is the shipped definition
# behaving correctly rather than a false positive: v63 forward-snipes, and a
# turret at our door is what the ring exists for.  Whether the ring should
# answer a forward snipe at all is a VERDICT, not an implementation choice --
# left armed as specified, one constant away from the alternative.
# Builder verdict on the worker's ranked flag #1: -1 = signature 2 OFF.
# Sig 2 armed vs opp_v63 in 14/16 smoke games (median r29) -- the ring's
# economics are exactly what taxed the C1 v69 leg, and the UNARMED path
# already answers a parked forward snipe with the parent's single-gun
# counterbattery.  Sig 1 alone measured 12/12 cad r3-8 / 0/12 v63 --
# perfect class separation; the ring stays reserved for insertion games.
C1B_ARM_TURRET_DSQ = -1

# PIECE C1b, MECHANISM B -- COVERAGE SUPPLY (second responder).  The other
# half of the _v82c1 gate row: coverage was SUPPLY-BOUND.  18 of 60 games were
# ZERO-covered against 6.9 establishments per game, because the answering side
# is one role-4 defender holding one plan against one SLOT_THREAT tile, and
# that defender is also the unit the heal line, the link queue and
# _sabotage_prio compete for.  The wild simultaneity budget says the common
# case needs two hands, not seven: max simultaneous alive at fp-dsq <= 36 is
# median 2 (max 7, and the 7 is a 10x10 radius-cut artifact).  So this adds
# exactly ONE more responder, never a squad.
#
# The trigger is the SECOND threat, identified locally with no new channel: an
# established enemy turret in the band whose tile is NOT the published
# SLOT_THREAT is by construction one the defender is not planning against,
# since the defender's plan is justified by SLOT_THREAT and dies with it.  The
# equal-tile case is admitted only when SLOT_DEFEND_BEAT says no defender has
# beaten for C1B_SUPPLY_BEAT_STALE rounds (or has never beaten at all, which is
# the opening, before the fifth builder exists -- exactly the window an r2-r5
# insertion lands in).
#
# ELECTION, and its accepted imperfection: there is no channel to appoint the
# helper, so each candidate elects itself iff no friendly builder it can SEE
# stands strictly closer to the threat (ties to the lower entity id), skipping
# any competitor that stands closer to SLOT_THREAT than to this threat -- that
# hand is the defender's threat's business.  Vision is per-unit, so two helpers
# on opposite sides of a wall can both elect.  That race is bounded, not
# prevented: _home_ring_check runs immediately before the build on the losing
# unit's next action and aborts on the turret that now covers, and HOME_RING_CAP
# still caps the ring at 3 live.  A wasted walk is acceptable; wasted titanium
# is not, and only the build spends.
C1B_SUPPLY_ON = True
# Establishment band -- the decode's own predictor radius, footprint-measured.
C1B_SUPPLY_BAND_DSQ = 36
# How far from home a builder may be and still be recruited.  The same 64 the
# raider signature uses: past eight tiles it is an economy hand, not a reserve.
C1B_SUPPLY_HOME_DSQ = 64
# Rounds of defender silence that admit the helper onto the PUBLISHED threat.
# Deliberately below DEFEND_BEAT_STALE_RNDS (6, the succession threshold): the
# helper is a one-round-reversible answer to a stalled defender, promotion is
# not, so it may fire earlier and on weaker evidence.
C1B_SUPPLY_BEAT_STALE = 4

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
# PIECE K heal budget, in whole titanium: the income-proportional part only
# (the K_HEAL_BASE_GRANT seed is added builder-side, so round 0 works despite
# the one-round write buffer).  Slot 9 was SLOT_LINKS_DONE, which every
# ancestor of this file incremented in _build_next_link and NO caller ever
# read -- provably dead, so it is reclaimed here rather than spending the last
# free slot.  The two dead increments are deleted with it; see _build_next_link.
# Single writer by construction: only the Core writes this slot, so the
# last-write-wins hazard that rules out a team-wide heal LEDGER (see
# K_HEAL_BUDGET_ON) does not apply to the budget itself.
SLOT_HEAL_BUDGET = 9
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

# RIDE-ALONG 1 (Eir 6) -- SPORKS AMMO POLICY, mechanism #1 of the decode and
# its top portability recommendation: a standalone core-side policy with no
# dependency on sporks' land-grab architecture, measured across 25 games with
# standard deviation 0 on the opening constant.
#
# The three numbers, pooled over 2,622 conversions and 18,947 Ti:
#  - convert_ammo(17) on round 0 in 25 of 25 games (their 25/25 opening, sd 0).
#  - HARD CAP 60: maximum ammunition held is exactly 60 in 24 of 25 games,
#    pooled median holding 54.
#  - TOP-UP 4: 1,311 of 2,622 calls are size 4, i.e. exactly one gunner shot at
#    a time.  Median titanium HELD is 97 against median ammo held 54 -- the
#    bank stays empty and the magazine stays full.
# The cadence separates wins from losses on its own: median 1,142 Ti converted
# and 170 convert_ammo calls in wins, 125 and 13 in losses; per-round
# conversion rate 0.18-0.64 calls/round in wins against 0.04-0.21 in losses.
# Ammo at 46-56 is also the trigger at 11 of 12 of sporks' core kills.
#
# What this REPLACES, and why they cannot coexist: the block it supersedes in
# _core runs a 16-per-turn drip toward a target of 16 (AMMO_FLOOR) / 24 under
# siege / 4-per-gun up to 48 / 32 on the atoll burst case / 256 on the hive
# case.  Two policies bidding for one action-free conversion per team per turn
# would simply mean whichever ran first won, so the toggle switches between
# them outright rather than layering.
#
# Note on OUR mix: sporks fires gunners at 4 ammo a shot, we are
# sentinel-heavy at 10, so a cap of 60 is six sentinel shots against sporks'
# fifteen gunner shots and a 4/round top-up trails one firing sentinel
# (10/3 per round).  The measured constants are ported as measured and left
# named so the screening battery can retune them for the heavier shot cost.
#
# The policy governs rounds 0..ENDGAME_RND-1 ONLY.  From ENDGAME_RND the
# piece-H dump, its tiebreak-#3 cap and its drip suppression own ammunition
# outright and are left bit-for-bit alone.
#
# OFF as of Eir 6b: measured-refuted as ported.  The cadence that keeps sporks'
# magazine full drains OUR bank instead, because our mix is sentinel-heavy (10
# ammo a shot against their 4) and a 4/round top-up therefore trails a single
# firing sentinel while still charging the till every round.  The code stays in
# place, untouched and toggled off, so a retune of the four constants for the
# heavier shot cost can be screened on its own leg later; with the toggle off
# the Eir 5.1 working-magazine block below owns ammunition bit-for-bit.
SPORKS_AMMO_ON = False
SPORKS_AMMO_OPEN = 17
SPORKS_AMMO_CAP = 60
SPORKS_AMMO_TOPUP = 4
# Bank floor the top-up will not spend through.  Same number as the existing
# under-siege ti_floor in _core: it is the till the heal line and the hunt
# pecks draw on, and a 4 Ti top-up is never worth emptying it.
SPORKS_AMMO_TI_FLOOR = 12

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


def fp_dsq(pos, o):
    """Footprint-dsq: min squared distance from pos to the 2x2 Core at o.

    Numerically identical to the ``min(t.distance_squared(pos) for t in
    core_tiles(o))`` idiom used everywhere else in this file -- the footprint is
    a product set {o.x, o.x+1} x {o.y, o.y+1}, so the minimum separates per
    axis -- but without four Position constructions and four method calls.
    PIECE C1b calls it once per visible ENEMY entity inside the sensing loop
    that already runs every round, so the difference is the whole cost of the
    arming gate's unarmed state.
    """
    dx = pos.x - o.x
    dy = pos.y - o.y
    if dx > 1:
        dx -= 1
    elif dx > 0:
        dx = 0
    if dy > 1:
        dy -= 1
    elif dy > 0:
        dy = 0
    return dx * dx + dy * dy


def fp_man(pos, o):
    """Footprint MANHATTAN distance -- the walk-feasibility metric.

    Builder bots move one CARDINAL step at a time, so Manhattan (not Chebyshev,
    not euclidean) is the number of rounds a walk from the 2x2 Core at o to pos
    can possibly take at best.  Same product-set separation as fp_dsq.
    """
    dx = pos.x - o.x
    dy = pos.y - o.y
    if dx > 1:
        dx -= 1
    elif dx > 0:
        dx = 0
    if dy > 1:
        dy -= 1
    elif dy > 0:
        dy = 0
    return (dx if dx >= 0 else -dx) + (dy if dy >= 0 else -dy)


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
        # PIECE C1 home-ring plan (see HOME_RING_CAP).  Per unit instance, on
        # the same argument as the siege plan beside it: only the role_n == 4
        # defender that made the plan ever reads it, so no store slot is spent.
        # homering_threat is the SLOT_THREAT tile the plan was made against --
        # a plan may not outlive the threat that justified it.
        self.homering_spot = None
        self.homering_approach = None
        self.homering_direction = None
        self.homering_type = None
        self.homering_threat = None
        # PIECE C1b -- arming state and the helper's claim (see
        # C1B_ARMING_GATE_ON / C1B_SUPPLY_ON).  Both per unit instance and
        # neither shareable: see the divergence note in the arming block for
        # why no store slot can carry the armed bit.  c1b_armed is one-way --
        # nothing ever clears it, because a game that has shown an insertion
        # signature does not stop being that game.  c1b_threat is the tile this
        # helper claimed; while it is set it OVERRIDES SLOT_THREAT for the ring
        # planner (see _homering_target), so the defender and the helper can
        # hold plans against two different threats at once.
        self.c1b_armed = False
        self.c1b_threat = None
        self.last_hp = None

        # Live-builder accounting, Core-only (see _core).  prev_units is the
        # unit count at the previous Core turn; lost_units the running total of
        # its drops over the match, i.e. how many units we know have died.
        self.prev_units = None
        self.lost_units = 0

        # INCOME METER, Core-only (see the meter block in _core).  Cumulative
        # estimated income in QUARTER-titanium, so passive (10 Ti / 4 rounds)
        # and harvester output (a 10-stack / 4 rounds) are both exact integers
        # per round and no float ever enters the hot path.  The Core is a
        # single unit with a persistent Player instance, so this integrates
        # cleanly without a store slot; only the derived budget is published.
        self.income_q = 0

        # PIECE K heal ledger, per builder instance (see K_HEAL_BUDGET_ON for
        # why this is NOT a team-wide store counter).  Counts heal actions this
        # unit has taken from K's priority block; each is 1 Ti.
        self.heal_spent = 0

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

        # PIECE I rotation memory (see ROTATE_DISCIPLINE_ON).  The tile this
        # Gunner is currently aimed at, so the hysteresis rule has something to
        # compare a new candidate against.  Per unit instance, no store slot:
        # only this turret's own _idle_rotate reads or writes it, and a stale
        # value fails the liveness test below rather than misleading anyone.
        self.rot_tgt = None

        # Rotation latch (see ROTATE_COOLDOWN_RNDS).  rot_rnd is the round this
        # gunner last PAID for a rotation, rot_prev_dir the facing it left, and
        # rot_lock_d the dsq of the target it bought.  rot_lock_d is the stable
        # yardstick the in-window hysteresis compares against: rot_tgt above is
        # a tile, and a tile goes stale the moment the enemy standing on it
        # takes a step, which is exactly how the nordkap oscillation gets in.
        # Same per-unit-instance argument as rot_tgt -- one Player per unit, so
        # a latch here is this gunner's own and never gags the others.
        self.rot_rnd = -10 ** 9
        self.rot_prev_dir = None
        self.rot_lock_d = 10 ** 9

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

        # INCOME METER (feeds PIECE K's heal budget and RIDE-ALONG 2's
        # expansion gate).  There is no engine getter for delivered titanium,
        # and the bank cannot stand in for one: deliveries and spends land
        # between two Core turns, so a bank delta nets them against each other
        # and reads 0 on a round that earned 30 and spent 30.  What IS knowable
        # cheaply is the PIPELINE, and it is the same arithmetic the tiebreak
        # cares about -- passive income is 10 Ti every 4 rounds and every
        # connected harvester adds a 10-stack on the same 4-round cadence.  In
        # quarter-titanium that is a flat +10 per round plus K_HEAL_HARV_Q per
        # harvester per round, integrated by the one unit that runs every round
        # and has no writer to race with.
        #
        # Two documented biases, both deliberate: SLOT_HARVESTERS is a monotone
        # high-water mark of harvesters BUILT (a dead harvester never
        # decrements it), and not every built harvester is directed-connected
        # to the Core -- so K_HEAL_HARV_Q credits half the nominal rate to
        # absorb both.  Cost is one multiply-add per Core turn.
        self.income_q += 10 + K_HEAL_HARV_Q * harv
        income_ti = self.income_q // 4
        if K_HEAL_BUDGET_ON:
            ct.write_store(SLOT_HEAL_BUDGET, income_ti * K_HEAL_RATE_PCT // 100)

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

        # SLOT_HOME_GUN is a monotone count of turrets this team has ever
        # built.  Hoisted above the ammo branch because RIDE-ALONG 2's
        # live-builder bound reads it too, whichever ammo policy is in force.
        weapons = ct.read_store(SLOT_HOME_GUN)

        # RIDE-ALONG 1 -- SPORKS AMMO POLICY (see SPORKS_AMMO_ON).  Owns
        # ammunition for rounds 0..ENDGAME_RND-1 and replaces the working-
        # magazine block below outright: convert_ammo is once per team per
        # turn, so two policies would only mean "whichever ran first wins".
        # From ENDGAME_RND the piece-H dump and its tiebreak-#3 drip
        # suppression own the resource and this arm stands down, leaving that
        # window bit-for-bit as Eir 5.1 shipped it.
        sporks_ammo = SPORKS_AMMO_ON and not (
            ENDGAME_SWITCH_ON and rnd >= ENDGAME_RND
        )
        if sporks_ammo:
            # Round 0: the measured opening, 25 of 25 games, sd 0.  It is paid
            # out of the 500 Ti starting bank and cannot disturb the opening
            # spawn curve -- the five builders cost ~222 Ti at scale and ti is
            # re-read below before can_spend_spawn is computed.
            #
            # Thereafter: top the magazine toward the cap in one-shot
            # increments and leave the rest of the bank to the economy.  The
            # top-up only fires while ammo is BELOW the cap, so a magazine
            # nobody is firing costs nothing at all after the first fill --
            # total lifetime spend is (ammo actually burned) + the cap, not
            # SPORKS_AMMO_TOPUP per round.
            want = SPORKS_AMMO_OPEN if rnd == 0 else SPORKS_AMMO_TOPUP
            amt = min(want, SPORKS_AMMO_CAP - ammo, ti - SPORKS_AMMO_TI_FLOOR)
            if amt > 0 and ct.can_convert_ammo(amt):
                ct.convert_ammo(amt)
                # Ammo conversion is action-free; keep evaluating the Core's
                # spawn/build priorities with the updated resource balance.
                ti = ct.get_global_resources()
                ammo = ct.get_global_ammo()
        else:
            # Keep only a small working magazine.  Conversion is action-free,
            # so a 60-round stockpile merely starves harvesters and
            # counter-gunners.
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
                ammo_target = max(ammo_target, min(48, 4 * weapons))
            ti_floor = 12 if (under or weapons) else 52
            if not endgame_dumped and (under or weapons or harv >= 2) and ammo < ammo_target and ti > ti_floor:
                amt = min(16, ammo_target - ammo, ti - ti_floor)
                if amt >= 4 and ct.can_convert_ammo(amt):
                    ct.convert_ammo(amt)
                    # Ammo conversion is action-free; keep evaluating the
                    # Core's spawn/build priorities with the updated balance.
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
        #
        # RIDE-ALONG 2 -- POPULATION FLOOR (see POP_FLOOR_ON).  When on, the
        # bank-threshold clause is REPLACED, not supplemented: a refill up to
        # the floor asks only whether the bank covers one scaled body, and a
        # spawn above the floor asks about the delivered-Ti RATE instead of the
        # bank.  The siege clause below stays exactly as it is -- it is strictly
        # more permissive in its own window (it fires above the floor too) and
        # deleting it would lose a shipped, measured behaviour.  REPLACEMENT_MAX
        # and the surge still bound total lifetime spawns through spawn_budget.
        pop_floor = min(POP_FLOOR, spawn_cap) if POP_FLOOR_ON else 0
        pop_refill = POP_FLOOR_ON and self._live_builders(ct, units, weapons) < pop_floor
        pop_expand = (
            POP_FLOOR_ON
            and rnd >= REPLACE_MIN_RND
            and 10 + K_HEAL_HARV_Q * harv >= 4 * POP_EXPAND_TI_RATE
        )
        if (
            self.n < spawn_budget
            and (
                self.n < spawn_cap
                or (
                    (pop_refill or pop_expand) if POP_FLOOR_ON
                    else (ti >= REPLACE_TI_FLOOR and rnd >= REPLACE_MIN_RND)
                )
                or (
                    SIEGE_RESPAWN_ON
                    and under
                    and rnd >= HUNT_MIN_RND
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

    def _live_builders(self, ct, units, weapons):
        """RIDE-ALONG 2 -- best cheap LOWER bound on our live builder count.

        The engine gives the Core no way to count builder bots: its vision is
        r^2 = 36 while builders work far outside it, get_unit_count() lumps
        Core, builders and every turret into one number, and the cost scale is
        a single team-wide float that cannot be inverted into a count.  Two
        independent lower bounds are available for a handful of engine calls,
        and the larger of the two is taken because both err the same way:

          (a) spawned minus deaths.  self.n counts builders spawned; lost_units
              counts ALL unit deaths, turrets included, so every turret we lose
              is charged to this bound as a phantom builder death.
          (b) units minus everything that is not a builder.  A "unit" is the
              Core, a builder, a Gunner, a Sentinel or a Launcher, so
              units - 1 - turrets - launcher is exact IF the turret count is
              exact; SLOT_HOME_GUN is monotone (never decremented, rubble still
              counts), so this bound is also depressed, by turret DEATHS.

        Under-reporting means over-spawning, bounded three ways: by pop_floor
        itself (each spawn raises bound (a) by one, so the refill closes), by
        spawn_budget = spawn_cap + REPLACEMENT_MAX above it, and by the bank.
        Over-reporting is the dangerous direction and neither bound can do it.
        """
        by_deaths = self.n - self.lost_units
        by_census = units - 1 - weapons - (1 if ct.read_store(SLOT_LAUNCHER) else 0)
        return max(0, by_deaths, by_census)

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
        # PIECE C1b, MECHANISM A -- the arming scan, piggybacked on the loop
        # below rather than added beside it: no new engine call, no second
        # iteration over nearby entities.  Once armed the whole thing collapses
        # to one False test per visible enemy, which is the "unarmed costs
        # nothing" requirement met from the other side too -- an unarmed unit
        # pays one fp_dsq (six integer ops, no engine call) per visible enemy.
        # The round is read once here instead of per entity; `rnd` proper is
        # not bound until after this loop.
        _arm_scan = C1B_ARMING_GATE_ON and not self.c1b_armed
        _arm_rnd = ct.get_current_round() if _arm_scan else 0
        # Signature 1's walk-feasibility term (see C1B_ARM_RAIDER_RND).  The
        # enemy anchor is last round's store value, or the symmetry guess the
        # Core itself publishes from -- both are available before any enemy
        # Core has ever been seen, and neither costs an engine call.
        _arm_ecore = None
        if _arm_scan:
            _arm_ecore = self.enemy
            if _arm_ecore is None:
                _arm_ecore = enemy_core_for(self.mw, self.mh, self.core)
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            et = ct.get_entity_type(eid)
            ep = ct.get_position(eid)
            if et == EntityType.CORE:
                self.enemy = ep
                ct.write_store(SLOT_ENEMY_CORE, pack_pos(ep))
            if _arm_scan:
                if et in (EntityType.GUNNER, EntityType.SENTINEL):
                    # SIGNATURE 2 -- turret arrival, any round.
                    if fp_dsq(ep, self.core) <= C1B_ARM_TURRET_DSQ:
                        self.c1b_armed = True
                        _arm_scan = False
                elif (
                    et == EntityType.BUILDER_BOT
                    and _arm_rnd < C1B_ARM_RAIDER_RND
                    and fp_dsq(ep, self.core) <= C1B_ARM_RAIDER_DSQ
                    and fp_man(ep, _arm_ecore) > _arm_rnd + 1
                ):
                    # SIGNATURE 1 -- early raider, and it must have been THROWN
                    # (see C1B_ARM_RAIDER_RND for the walk-feasibility test).
                    self.c1b_armed = True
                    _arm_scan = False
            d = self.core.distance_squared(ep)
            if (et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= self.gun_sense) or (
                et == EntityType.BUILDER_BOT and d <= self.b_sense
            ):
                ct.write_store(SLOT_UNDER, 1)
                ct.write_store(SLOT_ATK_RND, ct.get_current_round())
                if B8_ON:
                    if _threat_best is None or d < _threat_best_d:
                        _threat_best, _threat_best_d = ep, d
                else:
                    ct.write_store(SLOT_THREAT, pack_pos(ep))
        if B8_ON and _threat_best is not None:
            ct.write_store(SLOT_THREAT, pack_pos(_threat_best))

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

        # PIECE C1b -- a claim belongs to an ELIGIBLE helper only, and this is
        # the first line past every role override above, so the release happens
        # on the same turn eligibility is lost.  It cannot be left to
        # _c1b_supply's own gate: the melee recall (_home_defend), the rank-2
        # hold and the universal heal all return out of _builder before supply
        # is ever reached, so a role_n == 3 expander that turns saboteur at r12
        # would carry its claim -- and, through _homering_target, keep
        # overriding SLOT_THREAT -- for the rest of the game.  One attribute
        # test on the path where nothing is held.
        if C1B_SUPPLY_ON and self.c1b_threat is not None and (
            self.role != "expand" or self.role_n in (0, 4)
        ):
            self._c1b_drop()

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
        # PIECE J exempts exactly one caller from this heal: the role_n == 4
        # defender, while a threat sits in the home band with no live home
        # turret and the bank can afford the gun.  It is not skipping the heal
        # so much as deferring it one frame -- _defend's action phase still
        # falls back to _heal_core when the counterbattery cannot build -- so
        # nothing is lost on the rounds the exemption cannot be used.
        #
        # PIECE K'' adds a TRUNK arm beside this Core heal; the spend cap
        # (K_HEAL_BUDGET_ON) bounds the TRUNK ARM ONLY.  Three properties:
        #  1. THE SLOT_UNDER GATE STAYS ON THE CORE HEAL.  K v1 deleted it and
        #     was refuted for it -- 27-31% of builder turns spent topping up an
        #     unthreatened Core, ~15 pts vs opp_v63 and ~35 vs band_probe.
        #     can_heal() refusing a full-HP Core does not stand in for the
        #     gate: a Core one peck down is "damaged" and the priority block
        #     will then claim the turn for it on a quiet round.  The latch is
        #     the loose one (any threat level, 50-round decay), so a real siege
        #     is never gated out; it only excludes the peacetime rounds.
        #  2. THE TRUNK ARM IS *NOT* SIEGE-GATED, deliberately and asymmetrically
        #     so.  Its target is the farm raider that never comes near the Core
        #     at all -- the hive tape is ~1 conveyor per 10 rounds for 330
        #     rounds, entirely outside SLOT_UNDER -- and unlike the Core heal it
        #     has no "nothing is threatening this" failure case: a damaged
        #     conveyor is standing evidence that something already hit it.  It
        #     is the budget, not a round floor or a damage depth, that bounds
        #     it; v1's depth gate made this arm dead code in every game.
        #  3. THE CORE HEAL IS EXEMPT FROM THE CAP -- exact Eir 5.1 semantics,
        #     unbounded under siege, no ledger interaction.  K' (the capped
        #     variant) was refuted for the cap: builders went budget-dry by
        #     r10-27 under rush while the Core was still shelled -- ablation
        #     grid 2026-08-07: capped core arm ALONE scored band 56.7 where
        #     this exempt shape scores 95.0 and the K-off control 91.7.  The
        #     972-heal starvation case (v65 antler, Core heal starving piece
        #     H's r1000 arm) is thereby NOT fixed here -- it is 5.1's shipped
        #     behavior, retained knowingly; an ENDGAME_RND standdown on the
        #     Core arm is the parked follow-up candidate, not a ride-along.
        # With K off the original two lines run unchanged.
        if ct.get_action_cooldown() == 0:
            if K_HEAL_BUDGET_ON:
                # Piece J's exemption is left in EXACTLY its shipped state
                # space: it only ever ran while SLOT_UNDER was latched, so it
                # is asked only then here too.  That also keeps its ~dozen-call
                # live-gun scan off the rounds only the trunk arm visits.  When
                # it fires, the whole block stands down -- the defender needs
                # the turn to reach _try_counterbattery, and a trunk patch
                # would take it just as surely as the Core heal would.
                under = ct.read_store(SLOT_UNDER) != 0
                cb = under and self._cb_over_heal(ct)
                if under and not cb and self._heal_core(ct):
                    return
                if not cb and self._heal_budget_left(ct) > 0:
                    if self._heal_trunk(ct):
                        self.heal_spent += 1
                        return
            elif ct.read_store(SLOT_UNDER) != 0:
                if not self._cb_over_heal(ct) and self._heal_core(ct):
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

        # PIECE C1b, MECHANISM B -- the second responder, taken BELOW the CPU
        # guard (it plans a BFS, unlike the melee emergency above) and ABOVE
        # dispatch, so a recruited expander answers instead of laying its next
        # conveyor and is handed straight back the round it stops answering.
        # No role is written, so there is no lock to release: _c1b_supply
        # returning False falls through to exactly the dispatch below.
        if self._c1b_supply(ct):
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
        best, best_p = None, 99
        for d in CARDINALS:
            t = p.add(d)
            if not (0 <= t.x < self.mw and 0 <= t.y < self.mh):
                continue
            bid = ct.get_tile_building_id(t)
            if bid is None or ct.get_team(bid) == self.team:
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
                best_p, best = pr, t
        if best is not None:
            ct.fire(best)
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

    def _turret_on_harvester(self, ct, bp):
        """True if an enemy turret at bp stands orthogonally adjacent to a
        friendly HARVESTER (the eco-siege trigger; see the TWO HUNT MODES
        comment in _hunt_turret).  Neighbours of a visible turret can still
        sit outside our own vision, so every lookup fails safe to False."""
        for d in CARDINALS:
            n = bp.add(d)
            if not (0 <= n.x < self.mw and 0 <= n.y < self.mh):
                continue
            try:
                nid = ct.get_tile_building_id(n)
                if (
                    nid is not None
                    and ct.get_team(nid) == self.team
                    and ct.get_entity_type(nid) == EntityType.HARVESTER
                ):
                    return True
            except Exception:
                continue
        return False

    def _eco_besieged(self, ct):
        """Any visible enemy turret point-blank on a friendly harvester."""
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == self.team:
                continue
            if ct.get_entity_type(bid) not in (EntityType.GUNNER, EntityType.SENTINEL):
                continue
            if self._turret_on_harvester(ct, ct.get_position(bid)):
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

    def _heal_budget_left(self, ct):
        """PIECE K -- heal actions this unit may still take (see
        K_HEAL_BUDGET_ON).

        The Core publishes the income-proportional part of the TEAM budget in
        whole titanium; K_HEAL_BASE_GRANT is added here rather than there so
        the seed is available on round 0, when the buffered store still reads
        0 for a slot the Core writes this very round.  Each unit spends at most
        its own share, which is what makes the ledger safe without a team-wide
        counter no store slot can hold correctly.
        """
        allowance = (K_HEAL_BASE_GRANT + ct.read_store(SLOT_HEAL_BUDGET)) // K_HEAL_SHARES
        return allowance - self.heal_spent

    def _heal_trunk(self, ct):
        """PIECE K' -- repair a damaged economy building we are standing beside.

        The same repair _expand's chain medic performs, promoted out of the
        bottom of one role's action phase into the standing priority line,
        opened to round 0 and to every role, and paid for out of the caller's
        K_HEAL_SHARES budget rather than out of tempo.  Three of the medic's
        four gates are carried over; the fourth is the one K v1 died of.

         - MEDIC_TYPES only.  Turrets and barriers are combat capital with
           their own defense logic; the Core has its own heal above this one.
         - MEDIC_TI_FLOOR.  Below it every titanium belongs to the first
           harvesters and links.  This is a BANK gate, not a damage gate, and
           it stays: a 1 Ti heal taken out of a 19 Ti till is one nineteenth of
           the next conveyor, and the trunk we are patching is worthless
           without the links that bank buys.
         - PIECE H.  Past ENDGAME_RND a +4 HP patch scores in no tiebreak and
           the action is worth more as a harvester (tiebreak 2), so the trunk
           arm stands down exactly as _expand's medic already does.
         - NO DEPTH DISCRIMINATOR.  v1 required MEDIC_EARLY_MIN_DMG = 8 damage
           before MEDIC_MIN_RND and measured ZERO firings across the screening
           battery: the chip rates in this game are 2 (builder peck) and 7
           (gunner, reload 1) against a 20-HP conveyor, so a raided tile passes
           through that window rather than resting in it.  K' asks only
           "damaged at all", which is also all can_heal() itself asks, and
           leans on the budget for the bound the depth gate was supposed to
           provide.  The explicit HP compare is kept ahead of can_heal() purely
           as the cheap short-circuit -- two getters instead of a legality
           check -- and is deliberately identical in meaning to it.
        """
        rnd = ct.get_current_round()
        if ENDGAME_SWITCH_ON and rnd >= ENDGAME_RND:
            return False
        if ct.get_global_resources() < MEDIC_TI_FLOOR:
            return False
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
                    and ct.get_entity_type(bid) in MEDIC_TYPES
                    and ct.get_hp(bid) < ct.get_max_hp(bid)
                    and ct.can_heal(bp)
                ):
                    ct.heal(bp)
                    return True
            except Exception:
                continue
        return False

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

    def _live_home_gun(self, ct):
        """PIECE J -- is a friendly turret standing in the home band RIGHT NOW?

        The live replacement for `ct.read_store(SLOT_HOME_GUN) >= 1` at the two
        gates that mean "home defense exists" (see CB_OVER_HEAL_ON).  That
        counter is incremented at three sites, one of them the saboteur's
        FORWARD gun at the enemy Core, and never decremented, so it answers
        "did we ever build a turret anywhere" -- rubble and distant artillery
        both read as home defense.  This asks the question the gates actually
        want, off live observation, using the band constant those gates already
        share (HUNT_BAND_DSQ = 41, footprint-measured, twice validated).

        Vision-bounded by construction: get_nearby_buildings returns only what
        this unit can see, so it is only meaningful for a unit standing near
        home -- which is exactly who calls it.  A caller far from the Core gets
        False, i.e. "no home gun I can vouch for", which is the conservative
        answer for both call sites.
        """
        if self.core is None:
            return False
        tiles = core_tiles(self.core)
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) != self.team:
                    continue
                if ct.get_entity_type(bid) not in (EntityType.GUNNER, EntityType.SENTINEL):
                    continue
                bp = ct.get_position(bid)
                if min(t.distance_squared(bp) for t in tiles) <= HUNT_BAND_DSQ:
                    return True
            except Exception:
                continue
        return False

    def _cb_over_heal(self, ct):
        """PIECE J -- may THIS builder skip a heal to buy a counterbattery?

        True only in the one state where healing provably cannot win: the
        role_n == 4 defender, a threat inside the home band, no live home
        turret, and a bank that can pay for a Sentinel without touching
        SIEGE_HEAL_RESERVE_TI.  See CB_OVER_HEAL_ON for why every clause is
        load-bearing and why this is not a blanket heal/dispatch reorder.

        Ordered cheapest-first: two store reads, then a bank read, and only
        then the ~dozen-call live scan, so a defender that fails any earlier
        clause never pays for the scan.
        """
        if not CB_OVER_HEAL_ON or self.role_n != 4 or self.core is None:
            return False
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None:
            return False
        # The same reach test _try_counterbattery uses: past this band no
        # turret we could build against our own footprint reaches the threat,
        # so skipping the heal would buy literally nothing.
        if min(t.distance_squared(threat) for t in core_tiles(self.core)) > HUNT_BAND_DSQ:
            return False
        if ct.get_global_resources() < ct.get_sentinel_cost() + SIEGE_HEAL_RESERVE_TI:
            return False
        return not self._live_home_gun(ct)

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
        cands = []
        for bid in ct.get_nearby_buildings():
            if ct.get_team(bid) == self.team:
                continue
            if ct.get_entity_type(bid) not in (EntityType.GUNNER, EntityType.SENTINEL):
                continue
            bp = ct.get_position(bid)
            if eco_mode:
                # ECO-SIEGE: the turret qualifies by what it is doing, not by
                # where it is on the map -- orthogonally adjacent to a
                # friendly harvester, at any range from the Core.
                if not self._turret_on_harvester(ct, bp):
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
            if p.distance_squared(bp) > HUNT_DESIGNATE_DSQ:
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
                uid < me and up.distance_squared(bp) <= HUNT_DESIGNATE_DSQ
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

    def _try_counterbattery(self, ct):
        """Build only a weapon ray that already contains the reported threat."""
        threat = unpack_pos(ct.read_store(SLOT_THREAT))
        if threat is None:
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
        # PIECE C1 -- ring semantics, asked here and NOT after the bootstrap
        # gate: a threat that is already dead, or already inside a standing
        # turret's ray, wants no second turret at any harvester count or bank.
        # This is also the gate the walk-to-position planner asks, so the two
        # can never disagree about whether the ring is full.  home_gun below is
        # this scan's own count, which makes the bootstrap gate's question
        # ("a home gun already stands", i.e. _live_home_gun) free rather than a
        # second dozen-call scan.
        # PIECE C1b: unarmed, this whole block is skipped and home_gun stays
        # None, which routes the bootstrap gate below into the parent lineage's
        # own expression byte-for-byte -- see _ring_armed.
        home_gun = None
        if C1_HOME_RING_ON and self._ring_armed():
            ring_blocked, ring_live = self._home_ring_check(ct, threat)
            if ring_blocked:
                return False
            home_gun = ring_live >= 1
        # Mirror of _plan_siege's economy gate: the first emergency battery is
        # free, any further one waits for income.  Ungated, opening threat noise
        # on close-anchor maps buys three fixed-facing Sentinels aimed at
        # transient spawn tiles before the first harvester exists.
        # PIECE J: "a home gun already stands" is what this gate means, so it
        # asks the live scan rather than the monotone SLOT_HOME_GUN counter,
        # which also counts the saboteur's forward gun at the ENEMY core and
        # counts rubble forever.  Harvester test first -- it is a store read,
        # the scan is a dozen engine calls.
        if ct.read_store(SLOT_HARVESTERS) < ECO_NEED and (
            home_gun if home_gun is not None
            else self._live_home_gun(ct) if CB_OVER_HEAL_ON
            else ct.read_store(SLOT_HOME_GUN) >= 1
        ):
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
        # PIECE C1, ray-coverage amendment: a held ring plan carries the
        # lane-scored (spot, facing, type).  The neighbour scan below builds
        # the FIRST enum-order facing that covers the threat, which is how
        # every smoke-run ring turret got placed while the planner's facing
        # never reached the board.  Spend the plan first whenever this
        # builder stands beside its spot; the scan remains the fallback for
        # planless builders (melee emergencies via _home_defend), and the
        # held-plan gate keeps them off the planner's BFS.
        # PIECE C1b: the held-plan spend is gated too, so an UNARMED unit that
        # somehow still carried a plan (it cannot -- the planner is gated as
        # well -- but the invariant is cheap) never reaches the planner path.
        if (
            C1_HOME_RING_ON
            and self._ring_armed()
            and self.homering_spot is not None
            and self._try_homering_build(ct)
        ):
            return True
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
                        # PIECE C1: this turret answers the same threat any
                        # held plan was made against, so the plan is spent.
                        self._clear_homering()
                        return True
                    if turret_type == EntityType.GUNNER and ct.can_build_gunner(bp, facing):
                        ct.build_gunner(bp, facing)
                        ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
                        self._clear_homering()
                        return True
        return False

    def _ring_armed(self):
        """PIECE C1b, MECHANISM A -- may the C1 ring machinery run at all?

        Two attribute reads and no engine call, which is the point: with the
        gate on and no insertion seen, every ring gate in this file answers
        here and the planner, the walk and the ring scans are never reached, so
        a non-insertion opponent plays the parent lineage.  With the gate off
        this is a constant True and the file is _v82c1 exactly.
        """
        return self.c1b_armed or not C1B_ARMING_GATE_ON

    def _homering_target(self, ct):
        """The tile the ring planner is currently aimed at.

        SLOT_THREAT for the role-4 defender, exactly as C1 shipped it, EXCEPT
        while a PIECE C1b helper holds a claim of its own -- see C1B_SUPPLY_ON.
        The override is per unit instance, so the two never see each other's
        target and the defender's plan is untouched by the helper's existence.
        With C1B_SUPPLY_ON off (or no claim held) this is the shipped read.
        """
        if C1B_SUPPLY_ON and self.c1b_threat is not None:
            return self.c1b_threat
        return unpack_pos(ct.read_store(SLOT_THREAT))

    def _c1b_drop(self):
        """PIECE C1b -- release the helper's claim and hand back a clean state.

        The claim and the plan it justified die together, and self.tgt/self.stuck
        are reset for the same reason the defend-role succession resets them:
        the expand machine below is about to be handed this unit back and a
        stale walk target is how a released helper oscillates.  No role was ever
        changed, so there is nothing to unlock -- normal dispatch resumes on the
        next line of _builder.
        """
        if self.c1b_threat is not None:
            self.c1b_threat = None
            self._clear_homering()
            self.tgt = None
            self.stuck = 0

    def _c1b_find(self, ct):
        """PIECE C1b -- nearest UNCOVERED, ANSWERABLE established enemy turret.

        One pass over get_nearby_buildings collects both sides -- our live home
        turrets (the HUNT_BAND_DSQ band _home_ring_state uses, so the two agree
        about what "a home turret" is) and the enemy turrets established inside
        C1B_SUPPLY_BAND_DSQ -- and coverage is then decided from that list with
        one can_fire_from per (our turret, their turret) pair, stopping at the
        first candidate that qualifies.

        Coverage is tested HERE and not left to the pre-build _home_ring_check
        alone, because that check knows only the one tile it is handed: with a
        covered turret nearest and an uncovered one behind it, a coverage-blind
        find would re-elect the covered one every round and the uncovered one --
        the only kind the decode says ever dies -- would never be answered.
        The pre-build check stays as the race abort; this is the selector.

        ANSWERABLE, folded into the same loop for the same reason: the nearest
        uncovered turret may be the published SLOT_THREAT with a live defender
        already planning against it, and rejecting the whole round on that would
        hide the second threat this mechanism exists for.  Two admitting cases,
        both off existing signals (see C1B_SUPPLY_ON): the tile is not
        SLOT_THREAT, so no defender plan can be aimed at it; or no defender has
        beaten for C1B_SUPPLY_BEAT_STALE rounds.  beat == 0 is the opening --
        the fifth builder does not exist yet -- and counts as silence, which is
        exactly the r2-r5 window an insertion lands in.  The stored value is
        round + 1, hence beat - 1 (see SLOT_DEFEND_BEAT).

        Vision-bounded by construction, which is correct for a responder: a
        threat this unit cannot see is not one it can be the nearest hand to.
        """
        tiles = core_tiles(self.core)
        p = ct.get_position()
        ours = []
        foes = []
        for bid in ct.get_nearby_buildings():
            try:
                et = ct.get_entity_type(bid)
                if et not in (EntityType.GUNNER, EntityType.SENTINEL):
                    continue
                bp = ct.get_position(bid)
                near = min(t.distance_squared(bp) for t in tiles)
                if ct.get_team(bid) == self.team:
                    if near <= HUNT_BAND_DSQ:
                        ours.append((bp, ct.get_direction(bid), et))
                elif near <= C1B_SUPPLY_BAND_DSQ:
                    foes.append((p.distance_squared(bp), bp))
            except Exception:
                continue
        if not foes:
            return None
        # The ring is already at capacity, so nothing here is answerable at any
        # coverage -- the same HOME_RING_CAP the defender's gate enforces.
        if len(ours) >= HOME_RING_CAP:
            return None
        slot_t = unpack_pos(ct.read_store(SLOT_THREAT))
        beat = ct.read_store(SLOT_DEFEND_BEAT)
        defender_silent = (
            beat == 0
            or ct.get_current_round() - (beat - 1) >= C1B_SUPPLY_BEAT_STALE
        )
        foes.sort()
        for _d, bp in foes:
            if not defender_silent and slot_t is not None \
                    and slot_t.x == bp.x and slot_t.y == bp.y:
                continue
            covered = False
            for op, od, oet in ours:
                try:
                    if ct.can_fire_from(op, od, oet, bp):
                        covered = True
                        break
                except Exception:
                    continue
            if not covered:
                return bp
        return None

    def _c1b_elected(self, ct, threat):
        """PIECE C1b -- am I the one hand this threat gets?  (See C1B_SUPPLY_ON.)

        Nearest-wins with a lower-id tiebreak, over the friendly builders this
        unit can SEE, skipping any competitor that stands closer to the
        published SLOT_THREAT than to this threat -- that one is the defender's
        threat's business and must not veto this one.  Role is not observable
        across units, so a saboteur or the defender itself can win the election
        and answer nothing; the election re-runs every round as they move, and
        the failure mode is a missed round, not a wasted build.
        """
        me = ct.get_id()
        p = ct.get_position()
        mine = p.distance_squared(threat)
        slot_t = unpack_pos(ct.read_store(SLOT_THREAT))
        for uid in ct.get_nearby_units():
            try:
                if uid == me or ct.get_team(uid) != self.team:
                    continue
                if ct.get_entity_type(uid) != EntityType.BUILDER_BOT:
                    continue
                up = ct.get_position(uid)
                d = up.distance_squared(threat)
                if slot_t is not None and up.distance_squared(slot_t) < d:
                    continue
                if d < mine or (d == mine and uid < me):
                    return False
            except Exception:
                continue
        return True

    def _c1b_supply(self, ct):
        """PIECE C1b, MECHANISM B -- the second responder's whole turn.

        True == this unit's turn is spent here; False hands it straight back to
        normal dispatch with no state held (see _c1b_drop).  Ordered
        cheapest-first throughout: three attribute tests, then a store read,
        then the band arithmetic, and only then the two scans and the planner.

        SLOT_UNDER is the outer cheap gate.  An established turret at fp-dsq
        <= 36 is at Core-anchor dsq <= 62 by construction, i.e. inside the
        gun_sense 64 that the same sensing loop publishes UNDER from, so the
        gate costs at most the one round the write buffer delays -- and it
        keeps both scans off every quiet round of every quiet game.
        """
        if not (C1B_SUPPLY_ON and self._ring_armed()):
            return False
        if self.role != "expand" or self.role_n in (0, 4) or self.core is None:
            # A helper can become INELIGIBLE while holding a claim -- the
            # defend-role succession promotes a role_n == 2 expander to
            # role_n == 4, and a Launcher throw turns one into a saboteur.
            # Dropping here is load-bearing, not tidiness: a retained claim
            # keeps overriding _homering_target for the rest of the game, so a
            # promoted defender would plan its ring against a tile it inherited
            # instead of against SLOT_THREAT.  Measured on opp_v69/heart.
            self._c1b_drop()
            return False
        if ct.read_store(SLOT_UNDER) == 0:
            self._c1b_drop()
            return False
        p = ct.get_position()
        if fp_dsq(p, self.core) > C1B_SUPPLY_HOME_DSQ:
            self._c1b_drop()
            return False
        threat = self.c1b_threat
        if threat is None:
            threat = self._c1b_find(ct)
            if threat is None:
                return False
            if not self._c1b_elected(ct, threat):
                return False
        # THE RACE ABORT, and it is the existing coverage dedup rather than a
        # new one: _home_ring_check answers "threat dead, already covered by a
        # live home turret, or ring at HOME_RING_CAP" off a live scan, and it
        # runs on THIS turn immediately before the build below.  Two helpers
        # that both elected therefore cost one wasted walk, never a second
        # turret -- the loser sees the winner's turret covering and drops.
        blocked, _live = self._home_ring_check(ct, threat)
        if blocked:
            self._c1b_drop()
            return False
        self.c1b_threat = threat
        if ct.get_action_cooldown() == 0 and self._try_homering_build(ct):
            self._c1b_drop()
            return True
        if ct.get_move_cooldown() == 0:
            # The plan is made HERE as well as in the action phase, and that is
            # not redundancy: _try_homering_build above only runs on a zero
            # action cooldown, so a helper that just built a conveyor would
            # otherwise hold a claim with no route for the rounds its action is
            # on cooldown.  Same three lines, same order and the same
            # stuck-replan discipline the defender's own walk block carries.
            if not self._homering_plan_valid(ct):
                self._clear_homering()
            if self.homering_approach is None:
                self._plan_homering(ct)
            elif self.stuck >= 3:
                self._clear_homering()
                self._plan_homering(ct)
            ap = self.homering_approach
            if ap is not None:
                if p.x == ap.x and p.y == ap.y:
                    # Hold the seat: the build is an ACTION and this round's was
                    # spent or unaffordable, so vacating would only cost the walk
                    # back.  Same idiom the defender's own walk block uses.
                    return True
                self.tgt = ap
                self._nav(ct, pave=False)
                return True
        return False

    def _threat_live(self, ct, threat):
        """PIECE C1 -- False only when the threat tile is VISIBLE and empty.

        SLOT_THREAT is a tile, not an entity handle, and no writer clears it
        when its occupant dies; the UNDER latch decays on 50 rounds, so a
        defender can otherwise plan, walk and build against a turret that was
        killed thirty rounds ago.  Out of vision returns True: "I cannot see
        it" is not evidence of death, and _hostile_at's except arm reads an
        unseeable tile as not-hostile, which alone would cancel every plan the
        moment the defender steps out of sight of the threat.  Read-only -- no
        new writer on SLOT_THREAT, whose single publisher stays the sensing
        block in _builder (and the Core's own).
        """
        try:
            if not ct.is_in_vision(threat):
                return True
        except Exception:
            return True
        return self._hostile_at(ct, threat)

    def _home_ring_state(self, ct, threat):
        """PIECE C1 -- (live home turrets, threat already in one of their rays).

        LIVE local scan, never SLOT_HOME_GUN -- see the HOME SENTINEL RING
        block for why that counter cannot answer either question.  The band is
        HUNT_BAND_DSQ (41, footprint-measured), the constant every other home
        gate in this file already shares; the decode states its predictor at
        36 and 41 is its validated neighbour rather than a new number.
        Vision-bounded by construction (get_nearby_buildings returns only what
        this unit sees), so a defender out in the field undercounts -- which
        errs toward one turret too many, not toward a ring that never answers.
        """
        tiles = core_tiles(self.core)
        live = 0
        covered = False
        for bid in ct.get_nearby_buildings():
            try:
                if ct.get_team(bid) != self.team:
                    continue
                et = ct.get_entity_type(bid)
                if et not in (EntityType.GUNNER, EntityType.SENTINEL):
                    continue
                bp = ct.get_position(bid)
                if min(t.distance_squared(bp) for t in tiles) > HUNT_BAND_DSQ:
                    continue
                live += 1
                if not covered and ct.can_fire_from(bp, ct.get_direction(bid), et, threat):
                    covered = True
            except Exception:
                continue
        return live, covered

    def _home_ring_check(self, ct, threat):
        """PIECE C1 -- (no new home turret wanted, live home turret count).

        The one gate both the immediate build (_try_counterbattery) and the
        walk-to-position planner (_plan_homering) ask.  Ordered cheapest-first:
        the liveness test is two engine calls, the ring scan is a dozen.  The
        count travels back with the verdict so neither caller pays for a second
        scan to answer the bootstrap gate's "a home gun already stands".
        """
        if not self._threat_live(ct, threat):
            return True, 0
        live, covered = self._home_ring_state(ct, threat)
        return (covered or live >= HOME_RING_CAP), live

    def _clear_homering(self):
        """PIECE C1 -- drop the held home-ring plan (see HOME_RING_CAP)."""
        self.homering_spot = None
        self.homering_approach = None
        self.homering_direction = None
        self.homering_type = None
        self.homering_threat = None

    def _homering_plan_valid(self, ct):
        """PIECE C1 -- may the held plan still be walked to?

        A plan is justified by one specific threat tile, so it dies with it:
        SLOT_THREAT moving to another attacker, or the old occupant dying in
        view, both invalidate the geometry that chose the spot and the facing.
        No held plan is trivially valid -- there is nothing to invalidate.
        """
        if self.homering_spot is None:
            return True
        # PIECE C1b: the helper's claim stands in for SLOT_THREAT while it holds
        # one, so its plan is validated against the threat it was actually made
        # against.  Identical read for the defender and with C1B_SUPPLY_ON off.
        t = self._homering_target(ct)
        if t is None or self.homering_threat is None:
            return False
        if t.x != self.homering_threat.x or t.y != self.homering_threat.y:
            return False
        return self._threat_live(ct, t)

    def _plan_homering(self, ct):
        """PIECE C1 -- choose a reachable tile whose ray covers the THREAT.

        The home-side sibling of _plan_siege: the same machinery (ray
        arithmetic backwards off the target, ONE terrain flood so the chosen
        ray is a real route and not a geometrically close tile behind a wall,
        cardinal approach tiles because construction is cardinal-adjacent
        only, and the same two CPU guards), aimed at the current SLOT_THREAT
        tile instead of at the enemy Core.  It is deliberately a sibling and
        not a refactor: the forward snipe is a separately gated piece and
        ablation purity beats DRY here.

        The three differences from the siege planner, each with its reason:
         - can_fire_from is the qualifier instead of a hand-rolled wall test.
           A Sentinel's line IGNORES obstacles, so the siege planner's "a wall
           anywhere before the target" rejection would throw away exactly the
           spots this piece exists to find.  It is the same predicate
           _try_counterbattery already trusts for this question.
         - a return-fire penalty (see HOME_RING_RETFIRE_PEN).
         - APPROACH-LANE COVERAGE ranked above distance (see HOME_RING_LANE_DSQ
           and the ranking comment at the sort).
         - a small pull toward our own Core, so a tie between two firing
           positions breaks toward the one inside the ring, where the heal
           line and the Core's own vision already are, rather than out in the
           field where nothing repairs it.

        Nothing is written to self.homering_* until a candidate is chosen at
        the very end, so every bail below is a clean no-op -- identical in
        effect to the "no candidates found" path.
        """
        if (
            not C1_HOME_RING_ON or not self._ring_armed()
            or self.map_grid is None or self.core is None
        ):
            return False
        threat = self._homering_target(ct)
        if threat is None:
            return False
        tiles = core_tiles(self.core)
        # The same reach test _try_counterbattery and _cb_over_heal share: past
        # this band no turret built against our own footprint reaches the
        # threat, so every can_fire_from below would return False.
        if min(t.distance_squared(threat) for t in tiles) > HUNT_BAND_DSQ:
            return False
        ring_blocked, ring_live = self._home_ring_check(ct, threat)
        if ring_blocked:
            return False
        # The bootstrap protection the immediate build carries, unchanged in
        # meaning: the first emergency turret is free, a second one waits for
        # income unless the Core is provably bleeding.
        if (
            ring_live >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED
            and not self._core_shelled(ct)
        ):
            return False
        # Type is decided at PLAN time because it sets the ray lengths below.
        # Same order _try_counterbattery uses; the first AFFORDABLE type wins,
        # and a bank that affords neither plans nothing rather than walking a
        # defender away from the heal line for a turret it cannot buy.
        turret_type = None
        for et, cost in (
            (
                (EntityType.SENTINEL, ct.get_sentinel_cost()),
                (EntityType.GUNNER, ct.get_gunner_cost()),
            )
            if PRIMARY_SENTINEL else
            (
                (EntityType.GUNNER, ct.get_gunner_cost()),
                (EntityType.SENTINEL, ct.get_sentinel_cost()),
            )
        ):
            if ct.get_global_resources() >= cost:
                turret_type = et
                break
        if turret_type is None:
            return False
        # Everything below is the expensive part: a full terrain flood plus a
        # nested candidate search.
        if self._cpu_exhausted(ct):
            return False

        ranges = (5, 4) if turret_type == EntityType.SENTINEL else (3, 2)
        p = ct.get_position()
        blocked = set(self.map_walls)
        blocked.update((c.x, c.y) for c in tiles)
        if self.enemy is not None:
            blocked.update((c.x, c.y) for c in core_tiles(self.enemy))
        # The threat's own tile is occupied by the thing we are shooting at:
        # never a spot, never a route.
        blocked.add((threat.x, threat.y))
        blocked.discard((p.x, p.y))

        dist = {(p.x, p.y): 0}
        q = deque([(p.x, p.y)])
        ring_bfs_steps = 0
        while q:
            x, y = q.popleft()
            ring_bfs_steps += 1
            if ring_bfs_steps % 64 == 0 and self._cpu_exhausted(ct):
                # Abandon planning for this round rather than run the candidate
                # search on a starved budget.  self.homering_* is untouched.
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

        # Return fire is a GUNNER problem only, and only for a threat we can
        # actually identify: a Sentinel outranges every spot equally, so a
        # penalty against one would separate nothing.  Unknown reads as no
        # penalty rather than as a gunner -- the alternative pushes every
        # candidate out of Sentinel range of a threat we cannot even see.
        retfire = False
        try:
            if ct.is_in_vision(threat):
                tid = ct.get_tile_building_id(threat)
                retfire = (
                    tid is not None and ct.get_team(tid) != self.team
                    and ct.get_entity_type(tid) == EntityType.GUNNER
                )
        except Exception:
            retfire = False

        # THE APPROACH LANE (see HOME_RING_LANE_DSQ).  Every in-bounds,
        # non-wall tile off the Core footprint out to footprint-dsq
        # HOME_RING_LANE_DSQ -- the tiles an insertion actually plants on.  Built
        # once per plan off a bounding box rather than a map sweep: at dsq 9 the
        # box is 8x8 around a 2x2 footprint, so this is ~64 pure-Python tests
        # and no engine calls.
        lane = set()
        for ly in range(self.core.y - 3, self.core.y + 5):
            if not (0 <= ly < self.mh):
                continue
            for lx in range(self.core.x - 3, self.core.x + 5):
                if not (0 <= lx < self.mw) or (lx, ly) in self.map_walls:
                    continue
                d = min((lx - t.x) ** 2 + (ly - t.y) ** 2 for t in tiles)
                if 0 < d <= HOME_RING_LANE_DSQ:
                    lane.add((lx, ly))

        candidates = []
        seen = set()
        for facing in DIRECTIONS:
            unit = Position(0, 0).add(facing)
            max_range = ranges[0] if facing in CARDINALS else ranges[1]
            for ray_len in range(max_range, 0, -1):
                spot = Position(
                    threat.x - unit.x * ray_len,
                    threat.y - unit.y * ray_len,
                )
                skey = (spot.x, spot.y)
                if (
                    not (0 <= spot.x < self.mw and 0 <= spot.y < self.mh)
                    or self.map_grid[spot.y][spot.x] != "."
                    or skey in blocked
                ):
                    continue
                if ct.is_in_vision(spot) and ct.get_tile_building_id(spot) is not None:
                    continue
                try:
                    if not ct.can_fire_from(spot, facing, turret_type, threat):
                        continue
                except Exception:
                    continue
                # Standing coverage of the approach lane, counted over the raw
                # ray (which is what get_attackable_tiles_from would return --
                # the full line to max range, walls included -- so it is derived
                # here for free instead of bought with an engine call).
                lane_cover = sum(
                    1 for step in range(1, max_range + 1)
                    if (spot.x + unit.x * step, spot.y + unit.y * step) in lane
                )
                home_pull = min(t.distance_squared(spot) for t in tiles) // 8
                fire_penalty = (
                    HOME_RING_RETFIRE_PEN
                    if retfire and spot.distance_squared(threat) <= GUNNER_RANGE_DSQ
                    else 0
                )
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
                    # HOME GROUND IS NOT EMPTY GROUND, and this is the one
                    # place the siege sibling's assumptions do not carry over.
                    # `dist` is a TERRAIN flood: it knows walls and the two
                    # Core footprints and nothing else, which is fine out in
                    # the field the saboteur walks but wrong here, where our
                    # own conveyor trunk and harvesters carpet the approach
                    # tiles.  Measured on lighthouse: an occupied approach put
                    # the defender in a two-tile A-B-A oscillation for the rest
                    # of the siege, replanning the identical unreachable spot
                    # every round.  is_tile_passable answers for buildings AND
                    # for a bot already standing there, and out-of-vision is
                    # left to the terrain flood rather than guessed at.
                    if ct.is_in_vision(approach) and not ct.is_tile_passable(approach):
                        continue
                    # Stand behind or beside the weapon, never in its ray.
                    ray_penalty = 20 if ad == facing else 0
                    terrain_penalty = 2 if self.map_grid[approach.y][approach.x] == "o" else 0
                    candidates.append((
                        -lane_cover,
                        dist[akey] + ray_penalty + terrain_penalty
                        + fire_penalty + home_pull,
                        -ray_len, spot.x, spot.y, approach.x, approach.y,
                        spot, approach, facing,
                    ))
        if not candidates:
            return False
        # RANKING (amended off the ray-coverage decode, 2026-08-07): covering
        # the CURRENT threat is mandatory -- can_fire_from above is a filter,
        # not a term -- and lane coverage outranks walking distance, because a
        # SENTINEL CANNOT BE RE-AIMED (rotate() is gunner-only; 0 direction
        # changes on any sentinel across 277 re-emissions).  A facing chosen for
        # today's threat tile alone is dead weight the round that threat dies,
        # while a facing that also crosses the approach lane keeps paying for
        # the rest of the game.  The measured predicate it is proxying: turrets
        # on a reachable friendly ray died 8/8, uncovered ones took zero turret
        # shots 15/15.
        candidates.sort(key=lambda row: row[:7])
        row = candidates[0]
        self.homering_spot, self.homering_approach, self.homering_direction = row[7:10]
        self.homering_type = turret_type
        self.homering_threat = threat
        return True

    def _try_homering_build(self, ct):
        """PIECE C1 -- build the planned ring turret once we stand beside it.

        Mirror of _try_siege_build: the same occupancy invalidation, the same
        cost-then-can_build gating, and the same atomic clear-on-build so no
        caller can ever see a half-spent plan.  It does NOT touch
        self.forward_guns -- that counter caps the FORWARD battery at the enemy
        Core and a home ring turret is not one of those.
        """
        if not C1_HOME_RING_ON or not self._ring_armed():
            return False
        if not self._homering_plan_valid(ct):
            self._clear_homering()
        if self.homering_spot is None and not self._plan_homering(ct):
            return False
        p = ct.get_position()
        spot = self.homering_spot
        if ct.is_in_vision(spot) and ct.get_tile_building_id(spot) is not None:
            self._clear_homering()
            return False
        if max(abs(p.x - spot.x), abs(p.y - spot.y)) > 1 or p == spot:
            return False
        built = False
        if (
            self.homering_type == EntityType.SENTINEL
            and ct.get_global_resources() >= ct.get_sentinel_cost()
            and ct.can_build_sentinel(spot, self.homering_direction)
        ):
            ct.build_sentinel(spot, self.homering_direction)
            built = True
        elif (
            self.homering_type == EntityType.GUNNER
            and ct.get_global_resources() >= ct.get_gunner_cost()
            and ct.can_build_gunner(spot, self.homering_direction)
        ):
            ct.build_gunner(spot, self.homering_direction)
            built = True
        if built:
            # Kept for compatibility with the counter's remaining readers
            # (_core_turret_mix's fallback and the CB_OVER_HEAL_ON=False path);
            # nothing in this piece gates on it -- see the HOME RING block.
            ct.write_store(SLOT_HOME_GUN, ct.read_store(SLOT_HOME_GUN) + 1)
            self._clear_homering()
            return True
        return False

    def _try_harvester(self, ct, harv):
        p = ct.get_position()
        for d in DIRECTIONS:
            bp = p.add(d)
            if 0 <= bp.x < self.mw and 0 <= bp.y < self.mh and ct.can_build_harvester(bp):
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
                # PIECE J: same narrow defender exemption as the universal heal
                # above -- with no home gun standing and a battery in band, +4
                # HP a round against 18-25 loses on arithmetic, so the action
                # goes to _try_counterbattery below and the heal fallback at
                # the bottom of this block still catches the rounds it fails.
                if shelled and not self._cb_over_heal(ct) and self._heal_core(ct):
                    defended = True
                else:
                    defended = (
                        self._sabotage_prio(ct)
                        or self._try_counterbattery(ct)
                        # PIECE C1: the immediate build above only fires when
                        # this builder ALREADY stands beside a tile whose ray
                        # holds the threat.  This is the walk case -- it builds
                        # if we have arrived, and otherwise makes the plan the
                        # move phase below walks to.  Defender seat only: the
                        # all-hands melee path (_home_defend) keeps the
                        # immediate build alone, since a raider already in the
                        # footprint is not a problem a five-round walk solves.
                        or (self.role_n == 4 and self._try_homering_build(ct))
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

        # PIECE C1 -- WALK TO THE FIRING POSITION.  Ordered ABOVE "defender
        # comes home" deliberately, and the ordering is the whole piece: that
        # rule sends a shelled defender back to the Core to heal, and +4 HP a
        # round against an 18-25 dmg battery is the losing side of the exact
        # arithmetic piece J already measured.  Placing this below it instead
        # would also OSCILLATE -- step out to the firing seat, be dragged home
        # next round for not touching the footprint, forever.
        #
        # It is self-limiting rather than a blanket override.  A plan exists
        # only while the threat is live, NO live home turret already covers it,
        # the ring is under cap and the bank affords the turret (see
        # _plan_homering's gate), so the heal rule takes the defender straight
        # back the moment the ring answers; and the action phase above still
        # heals on every round the walk cannot build.  Standing ON the approach
        # holds the seat -- the same "already in build range, wait for the
        # action instead of vacating" idiom the link queue below uses -- but
        # only while we can still pay for the turret; going broke drops the
        # plan and hands the round back to the heal line.
        # Same stuck-replan discipline the saboteur applies to the siege plan.
        # PIECE C1b: _ring_armed first -- it is two attribute reads, and unarmed
        # this is the only cost the whole walk block carries.
        if (
            C1_HOME_RING_ON and self._ring_armed()
            and self.role_n == 4 and under
            and ct.get_move_cooldown() == 0
        ):
            if not self._homering_plan_valid(ct):
                self._clear_homering()
            if self.homering_approach is None:
                self._plan_homering(ct)
            elif self.stuck >= 3:
                self._clear_homering()
                self._plan_homering(ct)
            ap = self.homering_approach
            if ap is not None:
                if p.x == ap.x and p.y == ap.y:
                    cost = (
                        ct.get_sentinel_cost()
                        if self.homering_type == EntityType.SENTINEL
                        else ct.get_gunner_cost()
                    )
                    if ct.get_global_resources() >= cost:
                        return
                    self._clear_homering()
                else:
                    self.tgt = ap
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
        # PIECE J, second half of the gun-counter fix: this freeze returns
        # _expand unconditionally on hive, BOTH seats, for the rest of the
        # match once the gun clause holds -- the confirmed economy self-freeze
        # against picket classes, and via _try_siege_build's increment it can
        # arm off our OWN forward gun at the enemy Core.  The live scan asks
        # the intended question ("a home turret is standing here"); the two
        # cheap tests are ordered ahead of it so the scan only runs on hive,
        # past round 42.
        hive_freeze = (
            self.mw == 25 and self.mh == 25
            and (self.core.x, self.core.y) in ((2, 20), (21, 3))
            and ct.get_current_round() >= 42
            and (
                self._live_home_gun(ct) if CB_OVER_HEAL_ON
                else ct.read_store(SLOT_HOME_GUN) >= 1
            )
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
        if self.role_n == 1 and self._intercept(ct):
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
            len(self.map_walls) >= ORE_STEPOFF_MIN_WALLS
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
            # Slot 9's "links done" counter was incremented here and below and
            # read nowhere in the file; the slot now carries PIECE K's heal
            # budget (see SLOT_HEAL_BUDGET), so the two dead writes are gone.
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
            # PIECE N (Eir 6e): pave_prev is one step away BY CONSTRUCTION only
            # until a Launcher throw teleports this builder between turns --
            # then pp can sit outside vision and is_tile_empty(pp) raises
            # GameError, aborting the whole dispatch (measured: every
            # "crash" in the 6d race v68 legs, both sides, was exactly
            # this line; also x3r0's kite_proxy stress traceback with high
            # confidence).  The guard skips the pave, never the move.
            if pave and self.core and pp is not None and ct.get_action_cooldown() == 0 \
                    and ct.is_in_vision(pp) and ct.is_tile_empty(pp):
                if ct.read_store(SLOT_HARVESTERS) >= 1 and self._eco_spendable(ct, ct.get_conveyor_cost()):
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
            if ct.read_store(SLOT_HARVESTERS) >= 1 and self._eco_spendable(ct, ct.get_conveyor_cost()):
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
        # IDLE ROTATION.  Nothing was firable this turn; a Gunner may re-aim.
        # PIECE I replaces the bare nearest-bearing rotate below -- see
        # ROTATE_DISCIPLINE_ON for the 4,460 Ti / 8 games measurement.  The
        # legacy tail is kept verbatim behind the toggle so the ablation grid
        # measures exactly this change and nothing else.  For a Sentinel both
        # paths are no-ops (the old one computed `enemy` and then failed the
        # GUNNER test), so the early return costs nothing.
        if ROTATE_DISCIPLINE_ON:
            self._idle_rotate(ct, p, turret_type)
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

    def _ray_lands(self, ct, p, facing, target):
        """Would a Gunner at p facing `facing` have `target` in its line?

        can_fire_from is the hypothetical-turret predicate and ignores ammo and
        cooldown by contract, which is exactly the question the rotation
        decision asks: not "can I shoot right now" but "is this facing worth 10
        Ti and the next shot".  Fails safe to False -- a facing we cannot
        evaluate is a facing we do not pay for.
        """
        try:
            return bool(ct.can_fire_from(p, facing, EntityType.GUNNER, target))
        except Exception:
            return False

    def _hostile_at(self, ct, pos):
        """True if an enemy building or builder bot stands on pos, seen now.

        Out-of-vision tiles raise on the tile getters, so the except arm is the
        answer for a target that has walked out of sight: not live, drop the
        hysteresis latch.
        """
        try:
            bid = ct.get_tile_building_id(pos)
            if bid is not None and ct.get_team(bid) != self.team:
                return True
            bot = ct.get_tile_builder_bot_id(pos)
            return bot is not None and ct.get_team(bot) != self.team
        except Exception:
            return False

    def _facing_has_target(self, ct):
        """Does this Gunner's CURRENT facing still hold a hostile it could shoot?

        Half of the rotation latch's escape clause (see ROTATE_COOLDOWN_RNDS).
        Asked with the same predicate _turret opens with: get_gunner_target is
        the nearest targetable tile in the facing line and will happily hand
        back one of our own buildings, so the tile has to be team-checked before
        it counts.  Reaching _idle_rotate at all means no shot went out this
        turn -- dry magazine or cooldown, since the fire path returns on
        success -- and neither of those is a reason to pay 10 Ti to aim
        somewhere else.  Fails safe to True: a facing we cannot evaluate is a
        facing we do not pay to leave.
        """
        try:
            t = ct.get_gunner_target()
            if t is None:
                return False
            bid = ct.get_tile_building_id(t)
            if bid is not None and ct.get_team(bid) != self.team:
                return True
            bot = ct.get_tile_builder_bot_id(t)
            return bot is not None and ct.get_team(bot) != self.team
        except Exception:
            return True

    def _rotate_allowed(self, ct, p, want, tgt):
        """ROTATION LATCH -- may this Gunner pay for a rotation this round?

        See ROTATE_COOLDOWN_RNDS for the nordkap g3 numbers this exists to stop.
        Outside the window every rotation rules 1-3 approved goes through
        exactly as v65 shipped it, which is what keeps the nine clean production
        games clean.  Inside it, a facing costs 10 Ti only if it is both
        unproductive now and strictly beaten by rule 2's own 3x dsq margin --
        and never if it is the facing we just paid to leave.
        """
        if ct.get_current_round() - self.rot_rnd >= ROTATE_COOLDOWN_RNDS:
            return True
        # The A->B->A edge, refused by name.
        if want == self.rot_prev_dir:
            return False
        if self._facing_has_target(ct):
            return False
        return p.distance_squared(tgt) * 3 <= self.rot_lock_d

    def _idle_rotate(self, ct, p, turret_type):
        """PIECE I -- disciplined idle re-aim for a Gunner.  See
        ROTATE_DISCIPLINE_ON for the measurement and the three rules, and
        ROTATE_COOLDOWN_RNDS for the Eir 5.1 latch layered over them."""
        if turret_type != EntityType.GUNNER:
            return
        cur = ct.get_direction()

        # Rule 3: builder bots only count inside gunner attack range.  Past it
        # they cannot be shot this turn anyway and they will have moved before
        # the rotation cooldown clears -- that is the drumlin thrash, 325
        # rotations in one game, in one line.
        cand, cand_d = None, 10**9
        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            ep = ct.get_position(eid)
            d = p.distance_squared(ep)
            if d >= cand_d:
                continue
            if (
                ct.get_entity_type(eid) == EntityType.BUILDER_BOT
                and d > GUNNER_RANGE_DSQ
            ):
                continue
            cand, cand_d = ep, d

        # Rule 2: hysteresis.  Hold the current aim point while it is still a
        # live hostile; a rival has to be 3x closer in dsq to take the facing.
        tgt = cand
        prev = self.rot_tgt
        if prev is not None and self._hostile_at(ct, prev):
            prev_d = p.distance_squared(prev)
            if cand is None or cand_d * 3 > prev_d:
                tgt = prev

        if tgt is not None:
            self.rot_tgt = tgt
            # Rule 1: pay only for a facing that actually lands the ray, and
            # only when the facing we already have does not.
            if self._ray_lands(ct, p, cur, tgt):
                return
            want = p.direction_to(tgt)
            if want == Direction.CENTRE:
                return
            if not self._ray_lands(ct, p, want, tgt):
                # The legacy tail's cardinal fallback, kept but now also
                # ray-checked.  Skipped when the bearing is already cardinal:
                # nearest_cardinal would hand back the same facing we just
                # rejected, for a second engine call and the same answer.
                if want.is_cardinal():
                    return
                want = nearest_cardinal(want)
                if not self._ray_lands(ct, p, want, tgt):
                    return
            if want != cur and ct.can_rotate(want):
                # Eir 5.1 latch (see ROTATE_COOLDOWN_RNDS).  Last gate before
                # the 10 Ti leaves; can_rotate is asked first because it is the
                # cheaper refusal and keeps the latch state honest -- rot_rnd
                # must only ever record a rotation that actually happened.
                if not self._rotate_allowed(ct, p, want, tgt):
                    return
                self.rot_rnd = ct.get_current_round()
                self.rot_prev_dir = cur
                self.rot_lock_d = p.distance_squared(tgt)
                ct.rotate(want)
            return

        # Nothing hostile in sight: fall back to the stored enemy-Core bearing.
        # Exempt from rule 1 by design (the anchor is far past r^2=13) and
        # self-limiting instead: p and the anchor are both fixed, so after this
        # fires once `want` equals the facing and it never fires again.
        self.rot_tgt = None
        # ...  but NOT exempt from the Eir 5.1 latch.  Self-limiting only holds
        # while the facing stays put; a gunner that answered a real target last
        # round and sees the ring empty this round would otherwise pay 10 Ti to
        # walk straight back to the anchor bearing, and pay again when the enemy
        # steps back into vision.  In the window the idle re-aim is the cheapest
        # thing to give up -- it buys no shot this turn either way.
        if ct.get_current_round() - self.rot_rnd < ROTATE_COOLDOWN_RNDS:
            return
        anchor = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        if anchor is None:
            return
        want = p.direction_to(anchor)
        if want != Direction.CENTRE and want != cur and ct.can_rotate(want):
            self.rot_rnd = ct.get_current_round()
            self.rot_prev_dir = cur
            # No target bought, so no yardstick to defend: leave rot_lock_d
            # wide open and let a real hostile take the facing on clause (a)
            # alone rather than gating it behind a dsq it cannot beat.
            self.rot_lock_d = 10 ** 9
            ct.rotate(want)

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
