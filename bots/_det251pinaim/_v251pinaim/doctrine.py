"""doctrine.py -- every tunable constant and doctrine flag, and the rationale
that earned it.

SPLIT OUT 2026-08-09 (s21) from a 5,100-line main.py.  Nothing here changed:
these are the SAME LINES in the SAME ORDER, moved wholesale.  The split is
proved behaviour-preserving by a det identity leg (0 flips) against the parent
rather than argued -- see the tape row for _v103split.

WHY THIS FILE EXISTS.  Flag ablation is this project's primary method, and the
flags were scattered through a thousand lines of prose -- HIVE_FREEZE_ON at 807,
PRIMARY_SENTINEL at 978, SPORKS_AMMO_ON at 1070.  Finding the two flags that
turned out to be ONE decision (the Thor gunline pairing) took three greps.  That
grep was the cost of not splitting and it was paid every session.

RULE FOR ANYONE ADDING A FLAG: it goes HERE, with its rationale comment and with
the measurement that justified it.  A flag whose comment does not say what was
measured is a flag nobody can ever retire.
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

# PIECE S1 -- OWN-BUILDING FIRE GUARD (see _intercept's adjacent branch).
#
# A builder bot's fire() hits whatever stands on the target TILE, and a tile
# holds a building and a bot at the same time.  The chase targets the enemy
# BUILDER, so the moment that builder walks onto one of our own conveyors --
# which is most of what it is here to destroy -- the adjacent branch fires into
# our own infrastructure: 2 Ti a swing, 2 damage a swing, for as long as the
# chase keeps us pinned beside it.  The chain medic then heals the same
# conveyor back at 1 Ti a patch, so the pair can run indefinitely with both
# arms convinced they are working.
#
# The defect is ancestral, not ours alone: research root-caused the identical
# branch in the teammate lineage's _intercept and measured 489 swings / 978 Ti
# burned on own buildings in a single game there.
#
# The fix is a team test, nothing more.  When the tile carries a building of
# OURS the fire is skipped and the turn falls through to the existing heal
# branch -- so the interceptor still holds station, still keeps the intruder
# pinned, and now spends the turn repairing the thing it was shooting.  The
# chase, the guard-escort branch and _duel_safe are all untouched: an ENEMY
# building on the tile still gets hit exactly as before, and an empty tile
# (the ordinary case, tbid None) is unchanged.
S1_INTERCEPT_GUARD_ON = True
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
# LOKI-13 (2026-08-10): ECONOMY SUPPRESSION, one constant.
# The pave trail drops a conveyor on the tile a builder just vacated, every
# move, uncapped -- ECO_CAP gates HARVESTERS only (eco.py `harv < _eco_cap`),
# so nothing bounds this stream at all. Live-measured on the pinned testbed:
# WE BUILD 38.20 CONVEYORS PER GAME. The Bisons build ~11. Cookie runs 0.42
# conveyors and 1.13 sentinels per whole game and kills inside r100 in 27.6% of
# its games; Prompt Engineers Anonymous runs 0 conveyors, 0 harvesters and 0
# sentinels EVER across 230 games.
# And LOKI-11 already showed half this dose is FREE: it cut conveyors to 20.92
# and harvesters to 3.12, lost 39% fewer of our own units, and its core-kill
# share did not get worse (52.0% vs 36.0%, a null at n=25 but certainly not a
# regression). This plank asks where the other half breaks.
# Under R1000_IS_DEFEAT the titanium this buys does not score. It only ever
# funds the kill, and 38 conveyors is not funding a kill at r32.
PAVE_TRAIL_ON = False

# PIECE E2B -- ORE PAVE BAN (grafted from the teammate lineage, x3r0 v69
# "orekeeper"; the mechanism is ported, the code is ours).
#
# Harvesters may ONLY be built on ore, and a building occupies its tile until
# something destroys it, so a conveyor laid on an ore tile does not cost a
# conveyor -- it costs that harvester site for the rest of the match.  Our own
# link machinery makes the loss permanent rather than transient:
# _build_next_link treats an occupied tile as a completed one
# (get_tile_building_id(tile) is not None -> pop, :3499-3501), so the site is
# never cleared and never re-routed.
#
# OUR line has the defect.  PIECE F paves the tile just LEFT with no terrain
# test at all (this function, below), and the piece-F rationale block above
# says outright that the trail is what covers ore.  The teammate forensics on
# the same ancestral code name the tiles: on fjordgate the trail laid
# conveyors on (8,1)/(3,9)/(1,8) at t=24/30/57, burying 3 of that map's 4
# harvester sites while an opening rush had just killed the harvesters that
# would have paid for the game.
#
# Measured in HIS production corpus, not just argued: 0 ore-paves in 725
# opportunities with the ban on, against 10/725 on the matched control
# (docs/research/orekeeper-v69-production-read-2026-08-07.md, prediction 2).
# That is the whole evidence for taking it -- the piece is a pure loss-
# avoidance gate with no upside claim attached.
#
# Scope: the two PAVE sites only (trail tile and next-step tile).  The
# deliberate linker is NOT gated here -- on a decoded map _link_path already
# blocks every ore tile in its BFS (:3386), so links route around ore by
# construction.  The undecoded-map fallback BFS does NOT block ore and is a
# standing red flag, called out at that site and left for its own piece: a
# planner change is not a pave change.
#
# Fail closed.  A tile we cannot read is treated as ore and the pave is
# skipped: not paving costs one conveyor of trail, paving a mine costs the
# mine.  The MOVE is never skipped, only the pave.
E2B_ORE_PAVE_BAN_ON = True

# PLANK HS -- HEAL SEATS: PROTECT THEM, STAFF THEM, AND KEEP BODIES COMING.
#
# The Core is a 2x2 footprint and its eight orthogonal neighbours -- the SEATS
# -- are the only tiles a builder can heal a Core tile from.  Each staffed seat
# is +4 HP/round for 1 Ti.  Eight staffed seats is 32 HP/round, above every
# siege DPS in the two decode corpora (max measured 23.22).
#
# THE LAW, found independently by both arms of the 2026-08-08 bleed decode
# (docs/research/v72-bleed-nonfamily-2026-08-08.md L1/L2 and
# docs/research/v72-bleed-cad-family-2026-08-08.md): heal/damage >= 0.94 -> the
# Core survives, 13 of 13; <= 0.86 -> it dies, 16 of 16; nothing in between.
# In the five closest losses the shortfall is 4.2-5.2 HP/round -- EXACTLY ONE
# MISSING HEALER -- while the bank sits idle (one game died holding 9,557 Ti).
# Three separate things produce that one missing healer, so this plank is three
# independently toggled mechanisms rather than one:
#
#  1. SEAT PROTECTION (HS_SEAT_PROTECT_ON).  Our own buildings stand on the
#     seats.  Measured on OUR line, not just v72's: median 4 of 8 seats carrying
#     an own building at game end, p90 8 of 8, 81 of 120 games at 4 or more.
#     Delivery cannot be banned outright -- titanium only enters the Core from a
#     conveyor whose output faces a Core tile, and every such conveyor stands on
#     a seat -- so exactly HS_DELIVERY_SEATS seats are reserved for delivery and
#     the rest are a permanent no-build zone for us.
#
#  2. HEAL DETAIL (HS_HEAL_DETAIL_ON).  Under shelling the file's existing
#     defense paths already walk builders home; what they aim at is "any tile
#     orthogonally adjacent to the footprint", which _bfs_direction happily
#     satisfies with a seat that is already taken.  This aims them at a FREE
#     seat instead.  It adds no role, no budget and no new call site -- it is a
#     movement preference inside paths that already exist.
#
#  3. CEILING LIFT (POP_CEILING_LIFT_ON).  See its own block below.
#
# RED FLAG, STATED HERE BECAUSE IT BOUNDS MECHANISM 1'S UPSIDE.  Conveyors and
# splitters are BOT-PASSABLE in this engine (docs/game-model.md: "Conveyors and
# Splitters are bot-passable -- you can walk on them (yours or the enemy's)";
# impassable is WALL, another builder bot, Harvester, Barrier, turret, Core).
# So a PAVED seat does not actually deny a healer the seat -- a builder can
# stand on the conveyor and heal.  Only a Harvester, a Barrier or a turret on a
# seat blocks it permanently.  The decode measured "seats carrying an own
# building" without separating the two, so the conveyor half of the correlation
# is confounded -- and the smoke census on this branch settled it against the
# conveyors (see HS_SEAT_BAN_CONVEYORS, now OFF by default, with the numbers).
# What mechanism 1 therefore actually ships is the impassable half: no turret,
# no harvester and no barrier of ours ever stands on a seat we did not reserve
# for delivery.  That is a rarer event than the decode's headline suggests and
# a correspondingly smaller prize; it is also the only half the game model
# supports, and it costs nothing when it does not fire.
HS_SEAT_PROTECT_ON = True
# How many seats stay open for delivery.  Two, not one: a single input is a
# single point of failure for the whole economy and the decode's own
# prescription is "at most 1-2".
HS_DELIVERY_SEATS = 2
# Does the ban also cover conveyors -- the two pave sites, the link planner's
# goals and the link builder?  Turrets, harvesters and barriers are banned under
# HS_SEAT_PROTECT_ON whatever this says.
#
# OFF, and MEASURED off rather than argued off (smoke, 2026-08-08).  Two
# results, both from the seat census probe on this branch:
#
#  1. The premise is false for conveyors.  On eider seat B the base reaches
#     pav = 8 of 8 seats carrying our OWN conveyors and the census reads
#     free = 8 of 8 in the same round, repeatedly, from r491 to r971 -- the
#     engine agrees with docs/game-model.md that a conveyor is bot-passable, so
#     a fully paved seat ring costs ZERO heal capacity.  Across the whole
#     baseline battery the seats our own buildings sit on are conveyors almost
#     to the last tile (imp ~ 0.05 of 8), so the "median 4 of 8 blocked"
#     headline is measuring tiles that were never blocking anything.
#  2. The cost is severe.  With the conveyor ban ON, eider seat B delivered
#     270 Ti against the base's 23,930 on the identical paired game (250 vs
#     22,360 on the second seed).  Cause: the PIECE F trail pave is this file's
#     de-facto link REPAIR mechanism -- nothing re-plans a chain once its head
#     is destroyed (the known L4 defect) -- and its terminal branch reconnects
#     the Core from whichever seat a builder happens to walk past.  Cutting the
#     terminals from 8 to 2 removed six of the eight chances to reconnect, and
#     the census shows pav going 2 -> 0 by r150 and never recovering.
#
# Left in as a switch rather than deleted because the ablation is one flip and
# the measurement above is worth being able to reproduce.
HS_SEAT_BAN_CONVEYORS = False
# How many of the nearest ore tiles vote on which side of the footprint the
# delivery seats sit.  Six is about two harvester clusters -- enough to point at
# the field the trunk chain will actually come from, few enough that ore on the
# enemy's side of the map never drags the choice.
HS_ORE_SAMPLE = 6
HS_HEAL_DETAIL_ON = True
# Band around the footprint inside which a visible friendly builder counts as a
# rival seat-seeker for the cap.  The builder vision radius squared, so the
# count covers exactly the ground this unit can actually see.
HS_SEEK_BAND_DSQ = 20

# PLANK HS, MECHANISM 3 -- POPULATION CEILING LIFT.
#
# RIDE-ALONG 2's POP_FLOOR refill (see POP_FLOOR_ON) is bank-gated and nothing
# else by design: a body costs one scaled builder and a bank that cannot afford
# one cannot afford anything.  But the refill clause sits UNDER the lifetime
# bound `self.n < spawn_budget`, and spawn_budget is spawn_cap plus at most
# REPLACEMENT_MAX(8) plus the surge -- so once replacements are exhausted the
# floor stops refilling however poor the population is and however rich the
# bank.  v72 has the hard version of the same bug (a flat 18-spawn lifetime
# ceiling) and the decode caught it dying with a heal line of ZERO builders and
# 8,298-9,982 Ti banked; ours is the soft version of it.
#
# The lift is narrow: ONLY the refill-to-floor path bypasses the lifetime bound.
# Everything above the floor -- expansion, replacement, surge -- still asks
# spawn_budget exactly as it does today, so spawn_cap/surge/replacement
# semantics are unchanged and a quiet game (population at the floor) spawns not
# one extra body.  Each body this buys is worth +4 HP/round on a seat, which is
# the unit the law above says we are short by.
POP_CEILING_LIFT_ON = True

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

# PIECE HF -- the hive economy self-freeze in _expand (2026-08-08, s20).
#
# WHAT IT DOES WHEN True (the v80 behaviour): past round 42, on hive only, with
# a live home gun standing, _expand returns UNCONDITIONALLY for the rest of the
# match.  Harvester expansion, link building and the chain medic all stop and
# never resume -- the clause has no exit.
#
# WHY IT IS OFF HERE.  Two independent measurements, taken by different arms
# from different data, describe the same defect:
#   - our own tape, 2026-08-08 19:16: "hive_freeze = measured LIVE defect,
#     2.1x delivered Ti on hive seat A".  v84 shipped HIVE_FREEZE_ON = False
#     for exactly this reason; the v86 fork and this v80 rollback both lost it.
#   - the hive replay decode, same day, 34 games and no knowledge of this code:
#     our harvesters plateau at 3 of a 6 cap "by r50 and never resume", 0% of
#     them die (n=25), and our turret production falls to 1/game against their
#     7.  The freeze arms at r >= 42.  That is the plateau, and the round
#     matches.
# It was invisible for its whole life because it flips ZERO outcomes against a
# deterministic opponent -- it costs delivered titanium, which no flip-counting
# leg this project ran before today could see.
#
# The clause is a defensive response to picket classes, so removing it is not
# free by assumption: it must be measured, not argued.  Kept as a flag so the
# removal stays ablatable and det-testable in both directions.
HIVE_FREEZE_ON = False

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

# --- SIPHON HYGIENE ---------------------------------------------------------
# STEP 0, MEASURED HERE (instrumented probe game, hand-built 10x10 map: one
# harvester of OURS on (4,4); the opponent plants a conveyor on (5,4) -- its
# EAST cardinal neighbour -- wired all the way back to THEIR core at r15; our
# own chain is deliberately withheld until r209):
#   * r16-r209, enemy belt the ONLY acceptor: 49 of 49 stacks banked by the
#     enemy.  A 100% giveaway, from a harvester that was ours the whole match.
#   * r209-r1000, one friendly and one enemy acceptor: 99 friendly / 98 enemy,
#     strictly alternating every 4 rounds, not one exception in 800 rounds.
#   * Final credit 990 (us) / 1470 (them) off that single harvester.
# So the engine's output rule is ROUND-ROBIN LEAST-RECENTLY-USED over the four
# cardinal neighbours and it DOES NOT LOOK AT TEAM.  (Consistent with
# game-model.md's harvester section and with its measured engine-side
# nondeterminism note -- a tie between "two valid adjacent acceptors, one per
# team" is only a tie at all if team is not a tiebreaker.)
#
# Two consequences, and they are the whole design of this piece:
#  (a) WIRING DOES NOT PREEMPT.  A friendly belt HALVES the drain; it never
#      stops it.  It is still worth having -- half of an orphan's output is
#      the difference between a harvester that pays us nothing and one that
#      pays us 1.25 Ti/round -- but it is not the fix.
#  (b) REMOVING THE ENEMY BELT IS THE ONLY FULL STOP.  A conveyor is 20 HP and
#      a builder peck is 2 Ti for 2 damage: ten swings, 20 Ti, against a
#      measured ~2.5 Ti/round drain that otherwise runs for hundreds of
#      rounds.  The trade pays back in about eight rounds.
# Wild measurement this answers (rated v75 corpus, 60 games): 4.41% of every
# stack we mined was banked by the ENEMY core, 81% of that volume through
# exactly this adjacency shape, worst game 58.5%.
#
# WIRE arm.  A harvester built by a builder that already had a chain in flight
# used to be planned by NOBODY -- the old code planned a path only when
# link_queue was empty -- which is precisely the orphan the wild measurement
# found.  The fix is a per-builder pending list, not an immediate first link:
# a lone stub conveyor is a DEAD END, it accepts exactly one stack and then
# blocks forever (game-model.md: a dead-end chain delivers zero over 990
# measured rounds), so abandoning a half-built chain to place one link would
# leave two harvesters delivering nothing instead of one.  The pending
# harvester is planned the moment the in-flight chain finishes, or after
# SIPHON_WIRE_RNDS if that chain is evidently stuck.
SIPHON_WIRE_ON = True
# Rounds a pending harvester waits for the in-flight chain before preempting
# it.  Three harvester output cycles: long enough that a normal chain (built
# as the builder walks it) finishes first, short enough that a wedged queue
# cannot orphan the new harvester for the rest of the match.
SIPHON_WIRE_RNDS = 12
# Most harvesters one builder may have waiting to be wired.  A builder that is
# this far ahead of its own chain is not the unit to fix it.
SIPHON_WIRE_QUEUE = 3
#
# DENY arm.  An enemy conveyor/splitter orthogonally touching one of OUR
# harvesters is a standing 2.5 Ti/round tap; the nearest expander goes and
# pecks it down.  Ranked BELOW every survival/heal duty and below this
# builder's own build actions, ABOVE walking off to new ore.
SIPHON_DENY_ON = True
# Titanium one peck costs (same price as HUNT_FIRE_TI; kept separate so the
# deny arm can be re-priced without touching the turret hunt).
SIPHON_FIRE_TI = 2
# Rounds between full scans while no target is held, offset per unit.  The
# scan walks get_nearby_buildings, so it is not free; a few rounds of
# detection latency against a drain measured in hundreds of rounds is not
# worth paying for every turn.
SIPHON_SCAN_EVERY = 4
# Rounds one builder may grind a single siphon belt before writing it off.
# Ten swings kill a whole conveyor outright, so anything past this means it is
# being healed faster than we peck -- the ESCORT_STALL_RNDS ransom trap, and
# the same answer: stop paying.
SIPHON_MAX_RNDS = 24
# How long a written-off (or provably dangerous) siphon tile stays off the
# list.  Per unit, same locality argument as escort_ban.
SIPHON_BAN_RNDS = 200

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

# PIECE E1 -- PEACETIME AMMO FLOOR = HARVESTER RESERVE (grafted from the
# teammate lineage, x3r0 v69 "orekeeper"; mechanism ported, expressed here
# against the live cost getter rather than his literal).
#
# The working-magazine drip in _core spends up to 16 Ti a turn into ammunition
# and refuses to spend below ti_floor, which is 12 the moment ANY turret has
# ever been built (`weapons` is a monotone count -- a dead turret never
# decrements it).  Ammunition scores in no tiebreak; a harvester scores in two
# (delivered, then harvesters alive).  So the standing top-up, left alone,
# holds the bank at 12 -- and a scaled harvester costs ~23 and rising.  The
# failure is not "we bought ammo we did not need", it is that the bank can
# never again cross the price of the ONE building that restarts income, so an
# early harvester wipe becomes permanent while a trickle of ammo drains into a
# magazine nothing is firing.
#
# Teammate forensics on the shared ancestor: after a harvester wipe the top-up
# drained 522-739 Ti over a game -- 13x what that game mined -- pinning the
# bank under the rebuild price for 850 straight turns against an opponent with
# zero turrets alive.  Measured in his production corpus: 0 violations across
# 1190 conversions with the floor on, against 55/679 on the matched control
# (docs/research/orekeeper-v69-production-read-2026-08-07.md, prediction 5).
#
# The reserve is priced off get_harvester_cost() rather than his literal 46,
# because harvesters scale +5% each and a fixed number stops covering the
# rebuild exactly when we have most to rebuild.  The margin is what wires the
# rebuilt harvester back to the chain; at the ~23 Ti scaled price his forensics
# quote it reproduces his 46 exactly, which is the number the 0/1190 was
# measured on.
#
# Two boundaries, both deliberate:
#  - UNDER SIEGE NOTHING CHANGES.  With `under` latched the drip keeps its 12
#    floor and its full magazine target: a gun that cannot fire during the
#    assault does not get to spend the bank on a harvester it will not live to
#    build.  The floor is a PEACETIME reserve only.
#  - PIECE H IS UPSTREAM AND UNAFFECTED.  The endgame dump runs before this
#    block and sets endgame_dumped, which switches the drip off entirely, so
#    from ENDGAME_RND the dump still converts against its own two-harvester
#    reserve and this floor cannot hold it back.
E1_AMMO_FLOOR_ON = True
E1_HARV_RESERVE_MARGIN = 23
# Builder verdict on the worker's ranked flag #1, ablation-confirmed: the
# UNCAPPED floor (get_harvester_cost() reaches 126 at our harvester counts)
# owned the snowflake/lighthouse seat-A deterministic flips vs opp_v72 --
# ammo starved exactly where the forward sentinel needs the early magazine.
# Capping the harvester term at v69's measured price reproduces his flat 46,
# the number the 0/1190 forensics actually validated.
E1_RESERVE_CAP = 23

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
    # ============ 2026-08-13 POOL ROTATION (s36): the 10 NEW maps ============
    # Encoded by tools/map_encode.py (COMMITTED this time; the weekly-rotation
    # encoder never was). Selftest reproduces 5 old-pool entries byte-for-byte.
    # TWO COLLISION PAIRS share dims+anchors and rely on the sensed-terrain
    # disambiguation that already serves eider/heart and the two 26x26s:
    #   midgard/ragnarok (30,30,2,2,26,26) - frostgate/yulerune (20,20,2,9,16,9).
    # No key equals any pre-existing entry, so behaviour on every previously
    # known map is unchanged BY CONSTRUCTION (exact-key candidate filter).
    ((20, 20, 9, 1, 9, 17), "AAAAAAAAAAAAASAAAAAGAAAAAAJBMEJNABMNBNNAACAAAGAASAACAMEANBJNAAAIAAAAASCAAMEANBJNAACAGAASAAAACAMNBNNAEJNANBDAAAAAASAAAAAGAAAAAAAAAAAAAA"),  # auroraveil
    ((30, 30, 2, 24, 26, 4), "AABBAAAAAAAABBAAAAAASAAAAAAAAAAABTAAAAAAAABNBAAAAAAANBBAAAAAAAABACAAAAAGAABAAAAAAAABNEAAAAAAANEDAAAASAAADDCAAAAAAAAAAAAAAAAADMAAAAAAAAMAASAAAAAAAAAASAACAAAAAAAAAACAAEAAAAAAAAEDAAAAAAAAAAAAAAAAASDDAAACAAAADMNAAAAAAAMNJAAAAAAAAJAAGAAAAASAJAAAAAAAAJJNAAAAAAAJNJAAAAAAAALJAAAAAAAAAAACAAAAAAJJAAAAAAAAJJAA"),  # drakkarfjord
    ((20, 20, 2, 9, 16, 9), "NBAAAMNNAAAANEAAAAAJBAAAAADACAASAAGANBSAAAJNAAAAAJBAAAAAAAAAAAU0GAAASYICAAAAAAAAAAAAAAAAAJBAAAGANBSAAGJNACJAAAAAAEAAAAAJNBAAAMNNAAAANB"),  # frostgate
    ((30, 30, 14, 2, 14, 26), "NDAAAAAADNEDAAAAAADMBCAAAAAASJSEAAAAAAMCEBAAAAAAJMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAEMAAAAAAAJAABAAAAAAJAABAAASAACSCSAACSAACSCSAACAAAJAABAAAAAAJAABAAAAAAAEMAAAAAAAAAAAAAAAAAAAAAAAAAACAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAAAAAAJMSEAAAAAAMCBCAAAAAASJEDAAAAAADMNDAAAAAADN"),  # glacierkeep
    ((20, 20, 1, 16, 17, 2), "AAAAAAACSAAAAAAJBAAAAEDSAASAAAAAAAAAAMAAAGACDAAMAAAEAAMAAUSAGDAEAAAAAJBJSAGGCAMAAJBAAMAAJACSAAAMAAAAAAAAAAGAAGJJBAAAAEAAAAAAGACAAAAAAA"),  # icefloe
    ((30, 30, 2, 2, 26, 26), "AAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAASAAAAAAADABAAAAAAADABAAAAAASDABAAAAAAAMEAAAAAAAAAAJEAAAAAACGAAAAAAAAMBMEMEAAASAJDAADAAAAAJDAADAAAAAJDAADAAAAAAASCAAAAAAAASCAAAAAAADAADBAAAAADAADBAAAAADAADBACAAAMEMEJEAAAAAAAAGSAAAAAAMBAAAAAAAAAAMEAAAAAAAJADCAAAAAAJADAAAAAAAJADAAAAAAACAAAAAAAAAASAAAAAAAAAAAAAAAAAAAAAA"),  # midgard
    ((30, 30, 2, 2, 26, 26), "AAAAAAAAAAAAAAAAAAAAAAOAAAAAAAADDADAJBAAJAAADAAAMAAGAEAAAAAAAAABAMAJAAAABAAJAJACJBAAJBAJAAABAJAAMAADAAAAAADAAAAJBAAADAAAAAAANEAEEAJJAAZRBDAGAASAYIAAAAAAAAYIACAAGADJZRAABBAMMAMNAAAAAAADAAAJBAAAADAAAAAADAAEAABAJAAABAJBAAJBSABABAAJAAAABAEAJAAAAAAAAAMAGAAEAAADAAABAAJBADADDAAAAAAAAWAAAAAAAAAAAAAAAAAAAAAA"),  # ragnarok
    ((20, 20, 9, 16, 9, 2), "AAAAAAAAAAAAAAIAAASCSCAAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAMEMNNJNBBBADDMJJAABBNEMNNJNAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAAIAIAAASCAAAAAAAAAAAAAA"),  # royale
    ((30, 30, 2, 14, 26, 14), "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAJBAACAAAAADDAAAAAAAABJAAAAAAAJAABAAASAADAADAACAAAEAAMAAAAAJCAASBAAAAAAAAAAAAAAKAAAAKAAAMDAAAADEAADAAAAAADAAABSAACJAAAABSAACJAAADAAAAAADAAMDAAAADEAAAKAAAAKAAAAAAAAAAAAAGJBAAJBGAAAAEAAMAAASAADAADAACAAAJAABAAAAAAABJAAAAAAAADDAAAAAASAJBACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),  # valkyrie
    ((20, 20, 2, 9, 16, 9), "AAAAAAAAAAAAAACAYAAAAPAAJCAAJAABAAAJADAAAALJGAAAAJBAAAAAMAAAAAAEAAAAAJBAAAAAMAAAAAAEAAAASDDCAAAJADAAAABADAAAFAAVAAAAYAACAAAAAAAAAAAAAA"),  # yulerune
)


# ============================================================================
# LOKI-1 ADDITIONS (v105).  Everything above this line is _v103split's
# doctrine.py, copied verbatim so the ported economy behaves identically.
# Everything below belongs to the raid layer and to the spawn policy that
# feeds it.  Slot aliases reuse indices whose _v103split owners (the capped
# launch pipeline, the siege reservation) LOKI-1 deliberately does not have.
# ============================================================================

# --- comm slots, LOKI names ------------------------------------------------
SLOT_FWD_GUN = 8        # was SLOT_DROPPED: monotone count of forward sentinels
SLOT_FERRY_ID = 10      # was SLOT_LAUNCH_ID: raider id+1 asking for a hop
SLOT_FERRY_RND = 11     # was SLOT_LAUNCH_RND: round that request was written
SLOT_RAID_N = 12        # was SLOT_LAUNCHED_ID: raider seats issued (monotone)
SLOT_RAID_LIVE = 15     # was SLOT_SIEGE: raiders that reported in last round

# --- population ------------------------------------------------------------
# The raid is a consumable.  _v103split banks titanium it never spends (an
# atoll game closed on 2,782 stored); LOKI-1 turns surplus bank into bodies,
# because a body at the enemy ring is the only thing that raises the r200-300
# hazard and stored titanium is tiebreak #3.
LOKI_BASE_BUILDERS = 5      # the opening five, unconditional (as _v103split)
LOKI_MAX_BUILDERS = 11      # hard lifetime ceiling on spawns
LOKI_SURPLUS_TI = 260       # bank above which extra bodies are bought
LOKI_SURPLUS_EXTRA = 3      # extra seats bought by a surplus bank
LOKI_RICH_TI = 700          # bank above which we buy the rest
LOKI_RICH_EXTRA = 3
LOKI_SPAWN_RESERVE = 60     # never spend the last 60 Ti on a body

# --- raid roster -----------------------------------------------------------
# Which builder seats go forward.  Seat 0 leaves at once (it is the seat
# _v103split also sends forward), seats 1-2 are the economy, seat 3 joins the
# raid once the harvester floor is met, seat 4 is the single home defender,
# and every replacement from 5 on is a raider.  There is NO round cutoff
# anywhere in this file -- that defect is the whole reason LOKI-1 exists.
LOKI_ECO_SEATS = (1, 2, 3)
LOKI_DEFEND_SEAT = 4
LOKI_LATE_RAID_SEAT = 3

# --- the collar ------------------------------------------------------------
# A 2x2 Core has exactly 12 ring tiles: 8 orthogonal SEATS and 4 diagonal
# CORNERS.  The 8 seats are the only tiles a builder can heal the Core from
# and the only tiles a conveyor can deliver into it from (docs/game-model.md;
# _v103split's own heal_seats docstring says the same).  Sealing them is
# therefore an economic AND a medical kill:
#   * heal is 0.25 Ti/HP against ~0.56 for any attacker, so a siege that does
#     not out-heal the defender never converts -- measured, 28 to 1206 raw
#     hits to kill one 500 HP Core.  Deny the seats and the ratio is ours.
#   * a barrier is 3 Ti / 30 HP; breaking one costs 15 builder pecks at 2 Ti
#     each = 30 Ti.  The exchange is 10:1 in our favour and every round they
#     spend pecking is a round they are not healing.
# A raider standing on a CORNER is orthogonally adjacent to exactly the two
# SEATS beside it, so four corner raiders can seal all eight seats.
LOKI_BARRIER_SEAL_ON = True
LOKI_SEAL_TI_FLOOR = 0     # keep a peck's worth of change in the bank
LOKI_PECK_TI_FLOOR = 4      # a peck is 2 Ti; below this, hold instead

# --- forward sentinel ------------------------------------------------------
# The barrier collar blocks LOS, so a GUNNER ray dies on our own wall.  The
# Sentinel line ignores obstacles, which makes it the only turret compatible
# with the collar -- it shoots THROUGH the seal into the Core.  18 dmg on a
# 2-round reload is 6 HP/round against a defender who can no longer heal.
LOKI_FWD_SENTINEL_ON = True
LOKI_FWD_GUN_CAP = 3        # forward sentinels alive at once (soft, monotone)

# --- LOKI-2b: THE CAP COUNTS RUBBLE -----------------------------------------
# `SLOT_FWD_GUN` is written ONLY as `read + 1` (raid.py) and is never
# decremented, so the comment above is exact and the consequence is not soft at
# all: it counts every forward sentinel we have EVER built, alive or dead.
# Three destroyed turrets close the forward-sentinel arm PERMANENTLY for the
# rest of the match.
#
# MEASURED, LOKI-2 smoke: on nordkap/kladde the control planted 3 forward
# sentinels and the variant planted 1 -- and the variant's single plant came at
# r8 against the control's r78. The rush arm reaches the enemy sooner, spends
# the cap sooner, loses those turrets sooner, and is then locked out for good.
# **So the rush made the cap bind HARDER, and the plank could not buy the thing
# it exists to buy.** The corpus recipe is 3 turrets by r22 (190 sub-r80 games,
# 99.3% of early core kills are turret fire); LOKI-2 delivered "1 turret, ~100
# rounds sooner", which is a different and much weaker claim.
#
# THE FIX IS A LIVE CENSUS, NOT A BIGGER NUMBER. Raising the cap would just
# raise the ceiling on rubble. A raider standing at the ring can SEE the
# forward turrets (builder vision r^2=20 covers the siege band), so it counts
# the live ones and publishes that; the Core cannot -- its own vision is r^2=36
# and forward turrets sit outside it, which is why the monotone counter existed.
# Last-writer-wins on the slot is acceptable here: every raider that can see the
# band computes the same census, and a raider that cannot see it does not write.
LOKI2B_LIVE_CAP_ON = True
LOKI2B_CENSUS_DSQ = 50      # count friendly sentinels within this of the enemy Core
LOKI_FWD_TI_FLOOR = 40      # bank left after paying for one
LOKI_FWD_MIN_HARV = 2       # do not open the siege before the economy exists

# --- launcher ferry --------------------------------------------------------
# _v103split gated insertion four ways (one staged raider, three per match,
# off entirely from r180).  LOKI-1 keeps NONE of those.  Instead the ferry is
# opportunistic and stateless: a raider never waits for a launcher (waiting
# spends the one resource the hazard table says is theirs, not ours); it walks,
# and if its walk happens to take it through the pickup ring the launcher
# flings it forward.  A throw is only made when it strictly shortens the
# raider's distance to the enemy Core.
LOKI_FERRY_ON = True
LOKI_FERRY_STALE_RNDS = 3

# --- exile hardening -------------------------------------------------------
# A launcher picks up any adjacent builder from EITHER team at d^2 <= 2, so a
# lone raider beside a defended Core is food (docs/tooling.md: every long-game
# throw loop examined was the DEFENDER disposing of the attacker's raiders).
# Three answers, all in raid.py: value is deposited as BARRIERS which survive
# the raider being thrown; a station covered by a visible enemy launcher is
# deprioritised; and a raider that detects it was teleported re-enters the
# ring at a different station instead of walking back into the same pickup.
LOKI_EXILE_PENALTY = 24     # station score penalty for a covering launcher
LOKI_TELEPORT_DSQ = 4       # position jump per turn that proves a throw

# --- LOKI-PINAIM (v251): PIN INSTEAD OF EJECT ------------------------------
# The EXILE branch throws the victim to the site FARTHEST FROM OUR OWN CORE.
# At a home launcher that is self-defeating: the throw hands the victim its
# safety AND removes it from our pickup ring, so the launcher has nothing to
# throw next round and the intruder simply walks back.
# THE ENGINE FACTS THIS TRADES ON, all verified:
#   * a launcher can throw EVERY ROUND (LAUNCHER_FIRE_COOLDOWN = 1, cooldowns
#     decrement at end of round) and the throw costs 0 ammo;
#   * pickup is d^2 <= 2 from the launcher, i.e. the full 8-neighbourhood;
#   * a builder bot's attack is ORTHOGONAL-ONLY, so a victim parked at
#     d^2 == 2 (a DIAGONAL of the launcher) cannot hit the launcher back,
#     while one at d^2 == 1 can.
# ⇒ aim the throw at a diagonal of the launcher and the intruder is pinned:
# picked up again next round, and every round after, for free, forever, while
# never getting an action that reaches us.  The victim keeps its move cooldown
# and escapes a landing tile 96.4% of the time within one round -- which is
# why this is priced as DISPLACEMENT-EVERY-ROUND and not as a kill.
# Falls back to the parent's farthest-from-our-core aim when no pin site is
# legal, so the worst case is exactly the parent.
LOKI_PINAIM_ON = True

# --- raid navigation -------------------------------------------------------
LOKI_RAID_RESCAN = 6        # rounds between full station rescans
LOKI_APPROACH_DSQ = 100     # inside this the raider stops paving/exploring


# ============================================================================
# LOKI-1 RE-AIM (mid-build doctrine change).  The brief this bot was started
# against told me to remove LAUNCH_GIVEUP_RND and target r200-300.  Two
# instruments then refuted that premise:
#   * the clock-unblocking ablation measured 49.4%, CI [42.2, 56.7], n=180 --
#     no effect at all;
#   * 11,895 genuine forward throws show median raider life after the throw
#     collapsing 43 -> 6 rounds at exactly r150, and only 2.34% of r200+
#     throws ever landing a single attack on the enemy Core.
# What survived is the other half of the same corpus: of 528 raiders that DID
# land attacks, 25 produced half of all 40,114 attacks and 319 were on the
# winning team.  So the scarce resource is not the throw and not the timing --
# it is SURVIVAL AT THE DESTINATION, and it is only purchasable early.
#
# LOKI-1 therefore separates two things the incumbent conflated:
#   COLD INSERTION -- sending a fresh body on a long walk into undamaged
#   defences.  Time-limited, because the measurement says it stops working.
#   FOOTHOLD REINFORCEMENT -- feeding a position we already hold (a live
#   barrier collar, a live forward Sentinel, a raider still acting at the
#   ring).  NOT time-limited, because "established" is exactly the state the
#   winning 319 were in.
# ============================================================================

LOKI_COLD_INSERT_RND = 150   # cold insertions stop here; footholds never do
LOKI_FOOTHOLD_STALE = 15     # rounds a foothold heartbeat stays credible
LOKI_ESTABLISH_DSQ = 40      # inside this of an enemy Core tile == established
LOKI_BUDDY_HEAL_GAP = 8      # heal an adjacent raider this many HP below max


# ============================================================================
# LOKI-2 (v117) -- THE COMMITTED OPENING.  One flag, LOKI2_RUSH_ON.
#
# This is NOT a new doctrine.  It is committing to the opening LOKI-1 already
# half-runs, because the corpus says the opening IS the game and we are
# playing it slowly.
#
# WHAT THE CORPUS SAYS.  Over 1,269 real early Core kills (<= r300),
# 99.3% of them are TURRET FIRE -- not builder pecks, not starvation.  The
# fastest killers in the league all run the same shape, a SENTINEL RUSH, and
# the sub-r80 recipe over 190 games is THREE TURRETS PLANTED BY r22 (p25 is
# r11).  The named specialists, by median kill round:
#     Banminary   r52   sentinel-heavy, plants r17 at d^2 = 18
#     Big O       r63   pure sentinel,  plants r14
#     Team 48     r74
#     Cookie      r88
#
# WHERE WE ALREADY STAND.  We are the league's #1 early killer BY VOLUME --
# 309 early kills, 48 of them sub-r80 -- and we are slow and thin about it:
# ONE turret per game against their two or three, planted at d^2 = 32 against
# Banminary's 18, median kill r91 against Banminary's r52.  We have the
# mechanism and we under-commit it.
#
# THE RULE ARITHMETIC.  A Sentinel is 18 damage on a 2-round reload = 9 HP per
# round each; three of them are 27 HP/round, and 500 HP of Core falls in ~19
# rounds of sustained fire (~28 rounds at the conservative 18 dmg/round the
# brief costs it at, i.e. allowing for reload desync and misses).  A Sentinel
# also IGNORES OBSTACLES -- it shoots through our own barrier collar, which a
# Gunner cannot -- and it outranges a Gunner (r^2 = 32 against 13).  Three of
# them is the whole kill.  LOKI_FWD_GUN_CAP is already 3 and is left alone:
# 3 is the specialists' number, so the cap was never the problem.
#
# THE THREE GATES THIS FLAG LIFTS, in order of how much delay each one buys:
#
#   1. THE HARVESTER PREREQUISITE.  _try_forward_sentinel refuses to plant
#      until SLOT_HARVESTERS >= LOKI_FWD_MIN_HARV (= 2), on the LOKI-1
#      reasoning "do not open the siege before the economy exists".  That
#      reasoning is right for a SIEGE -- a grinding r150+ collar that has to
#      be fed for hundreds of rounds -- and wrong for a RUSH, which is over
#      before the economy would have mattered.  It is also the single biggest
#      source of delay: it structurally forbids the r14-r22 plant every
#      specialist makes.  Inside the window the prerequisite is WAIVED (0).
#
#   2. THE BANK FLOOR.  LOKI_FWD_TI_FLOOR = 40 Ti must remain after paying
#      for the Sentinel.  At r20 this is not usually binding -- we open on
#      500 Ti and a Sentinel is 30 base -- but it becomes binding exactly
#      when we are buying the SECOND and THIRD one on the same opening bank,
#      which is the case this plank exists to create.  Inside the window the
#      floor drops to a token 8 Ti (one barrier plus change), because a
#      banked 40 Ti that buys nothing is tiebreak #3 and a third Sentinel is
#      the game.
#
#   3. THE ROSTER.  LOKI-1 sends ONE body at the opening: seat 0 leaves at
#      once, LOKI_ECO_SEATS = (1, 2, 3) are the economy (seat 3 joins the
#      raid later, state-gated), seat 4 is the home defender.  Three turrets
#      planted by r22 needs more than one pair of hands -- one builder can
#      only act once per round and has to walk between sites.  Inside the
#      window seats in LOKI2_RUSH_SEATS leave AT ONCE.
#
# WHY A WINDOW AND NOT A REWRITE.  LOKI2_RUSH_RND bounds every one of the
# three lifts to the committed opening.  Past it the bot is LOKI-1 exactly:
# the harvester prerequisite, the 40 Ti floor and the (1, 2, 3) economy seats
# all come back, because the LOKI-1 reasoning behind them is sound for the
# long game the corpus says we are currently losing.  r60 is set past the
# slowest named specialist's median kill (Big O, r63 -- so it covers the plant
# and the walk, not the kill) and well short of LOKI_COLD_INSERT_RND = 150.
#
# The override is applied AT THE POINT OF USE.  LOKI_ECO_SEATS is deliberately
# NOT mutated: it is a doctrine constant read by role assignment, and a bot
# whose constants change under it cannot be reasoned about or ablated.
# ============================================================================

# LOKI-4 (v120): OFF, on replicated adverse evidence against the PRIMARY currency.
# Measured 2026-08-09, paired deterministic, 360 games, 0 tracebacks, gate
# CLEARED 12/12, against the two probes with headroom (the saturated ones cannot
# measure anything -- clanker 96.7%, ouroboros 93.3%):
#     orizon  core_kill_share ALL -15.6pp  sign p=0.0201   SHORT -35.4pp p=0.0005
#     cad     core_kill_share ALL -18.9pp  sign p=0.0033   SHORT -22.9pp p=0.0192
#   LONG band null in both (p=0.51, p=0.15).
# I predicted the opposite in the prereg -- help on SHORT, harm on LONG -- and
# the harm is concentrated exactly where I predicted benefit. See
# docs/RESULT-rush-map-interaction-2026-08-09.md.
# The rush waives the harvester prerequisite and cuts the bank floor 40 -> 8 to
# buy tempo. On short maps the tempo was already there, so it pays the economy
# and receives nothing. That mechanism story is UNTESTED and is not the reason
# this flag is False; the replicated measurement is.
LOKI2_RUSH_ON = False
LOKI2_RUSH_RND = 60        # the committed-opening window
LOKI2_RUSH_MIN_HARV = 0    # inside the window, the harvester prerequisite is waived
LOKI2_RUSH_TI_FLOOR = 8    # inside the window, bank floor after paying for a sentinel
LOKI2_RUSH_SEATS = (0, 1)  # seats that leave for the raid AT ONCE, not just seat 0


# ============================================================================
# LOKI-6 (v122) -- THE ARRIVAL DEFECTS. Three fixes, one currency.
#
# The ladder says INCIDENCE is what is scarce, not speed: 74.4% of our
# core-kill wins are ALREADY inside r250 and that holds at 1600+, while against
# Ouroboros we get a kill in 9 of 155 games (5.8%). When we arrive we kill fast.
# We almost never arrive. A code read of this tree found three reasons that are
# defects rather than choices, and this iteration fixes exactly those three.
#
# 1. THE STALL DETECTOR COUNTS PRODUCTIVE WORK AS BEING STUCK. `self.stuck` is
#    incremented from TWO unrelated sources: genuine nav failure, and every
#    round the unit's position is unchanged -- which includes every round a
#    raider PRODUCTIVELY ACTED (pecked, sealed, healed, planted a sentinel),
#    because acting and moving are mutually exclusive by the rules. So a raider
#    that works at the ring for 8 rounds arrives at the stall test already at
#    the threshold, and the FIRST real navigation failure after that trips a
#    120-round station ban. LOKI6_STALL_SEPARATE gives navigation its own
#    counter.
#
# 2. THE PAUSE SILENCES THE HEARTBEAT THAT KEEPS THE WHOLE TEAM'S WINDOW OPEN.
#    `_raid` returns on `rnd < raid_pause_until` BEFORE the SLOT_RAID_LIVE
#    write. A paused raider SITTING AT THE RING therefore stops publishing the
#    foothold heartbeat; after LOKI_FOOTHOLD_STALE (15) rounds of silence every
#    other raider stands down via the cold-insert gate, and past r150 that is
#    PERMANENT for the rest of the match -- re-opening needs a heartbeat, and
#    only a raider already at the ring can write one. LOKI6_BEAT_BEFORE_PAUSE
#    publishes first and pauses second: a body that IS established is a
#    foothold whether or not its own navigation is paused.
#
# 3. SLOT_LAUNCHER IS A ONE-WAY LATCH. Set to 1 on build and re-asserted every
#    turn by a living launcher, but cleared ONLY on a failed build -- never on
#    death. Lose the launcher and `_try_build_launcher` returns False forever:
#    the ferry and our cheapest home defence are gone for the match. Same shape
#    as the SLOT_FWD_GUN rubble counter that LOKI-2b had to fix.
#    LOKI6_LAUNCHER_RELEASE lets the Core clear the slot when it can see the
#    launcher is gone.
#
# NONE of these changes what the bot TRIES to do. They remove three ways it
# stops being allowed to try.
# ============================================================================

LOKI6_STALL_SEPARATE = True     # navigation stalls get their own counter
LOKI6_BEAT_BEFORE_PAUSE = True  # publish the foothold heartbeat, then pause
LOKI6_LAUNCHER_RELEASE = True   # clear SLOT_LAUNCHER when the launcher is dead


# ============================================================================
# LOKI-7 (v123) = LOKI-6's arrival fixes + LOKI-QUIET's silenced builder melee.
#
# The two changes are independent and both measured well on the same fixture:
#   LOKI-QUIET (v96)  12-3, core_kill_share 12/15 = 80%   (p=0.025 vs Eir's 33%)
#   LOKI-6     (v97)   7-3, core_kill_share  7/10 = 70%   (fixture incomplete)
#   LOKI-4     (v95)   8-7, core_kill_share  8/15 = 53%
#   v94 Eir           11-4, core_kill_share  5/15 = 33%
#
# WHY THEY SHOULD COMPOSE, and it is one mechanism, not two. Acting and moving
# are MUTUALLY EXCLUSIVE for a builder bot. Every peck, siphon hit and
# counterbattery swing therefore costs that raider its move for the round --
# and the ladder says ARRIVAL is the scarce quantity, not damage. LOKI-QUIET
# removes the actions that were buying nothing (it went 3-2 against CAD landing
# ZERO builder attacks, so the melee was never load-bearing); LOKI-6 removes
# three ways the bot is forbidden from raiding at all. Both hand rounds back to
# movement. Combining them should not double-count, because they free
# DIFFERENT rounds: quiet frees rounds the raider spent acting, LOKI-6 frees
# rounds it spent stood down.
#
# HONEST RISK: quiet also silences the SIPHON, which is real income, and
# LOKI-6's launcher release can pay 20 Ti + 10% scale to rebuild a launcher
# that dies again. Two economy leaks stacked on one bot. If LOKI-7 measures
# BELOW both parents, that interaction is the first place to look.
# ============================================================================

LOKI_QUIET_ON = True     # no builder melee: no core peck, no siphon hit, no counterbattery


# ============================================================================
# LOKI-8 (v124) -- RAIDERS STOP GOING HOME. The next removal in the same family.
#
# Every winning change on this line has been a REMOVAL that hands rounds back
# to MOVEMENT, because acting and moving are mutually exclusive for a builder
# bot and the ladder says ARRIVAL is the scarce quantity (74.4% of our
# core-kill wins are already inside r250; vs Ouroboros we arrive in 5.8% of
# games). Measured on one fixture, n=15 each, 3 real opponents:
#     v94 Eir 33.3%  ->  LOKI-4 53.3%  ->  LOKI-5 80.0%  ->  LOKI-7 86.7%
#
# Two paths in main.py still pull a RAIDER back to the home core, and both
# spend the round that raider needed to walk:
#
#   1. THE UNIVERSAL ADJACENT HEAL. Any builder within dsq 25 of a damaged
#      Core heals it and RETURNS -- before _raid is ever called. Research
#      measured the size of this directly: a builder beside a DAMAGED core
#      moves on 15.5% of rounds against 68.3% at full HP (n=143,812), with the
#      opponent control at -0.152, so it is our code and not the game. It is
#      NOT a defect -- it is the price of the heal, charged by the engine --
#      but a RAIDER is the one body whose job is not to be here.
#   2. THE MELEE RECALL, which is already raiders-only. Its recorded
#      justification covers excluding EXPANDERS (an earlier revision recalled
#      them and the trunk chain stalled at r16 with 0 titanium delivered). It
#      has never carried evidence FOR the raider half.
#
# LOKI-8 exempts role == "raid" from both. THE CORE IS STILL HEALED: expanders
# (LOKI_ECO_SEATS) and the dedicated defender keep both paths, and they are the
# bodies whose job is to be in the home band.
#
# HOW THIS LOSES, and it is a real risk rather than a formality: SLOT_UNDER
# latches for 50 rounds off any enemy turret near our Core, so against a
# shelling opponent this removes our raiders from home defence for long
# stretches. If LOKI-8 drops on WIN RATE while holding core-kill share, that
# trade is what happened -- and win rate is not the verdict, but a bot that
# loses its own core faster kills fewer of theirs in the end.
# ============================================================================

LOKI8_RAIDERS_STAY_OUT = True    # raiders exempt from the home heal + melee recall


# LOKI-25: penalty for a raid station sitting on a live enemy gunner's ray.
# Same units as LOKI_EXILE_PENALTY, which is the launcher-adjacency penalty.
LOKI_GUNAXIS_PENALTY = 8

# LOKI-42: do not build a launcher before this round. Swept, not guessed.
LAUNCHER_MIN_RND = 160


# ============================================================================
# LOKI-SALT (v178) -- CUT THEIR BELT, THEN SALT THE TILE.
#
# Two behaviours that only pay together, both inside the raid layer and both
# inside the ENEMY half.
#
# (a) CONVEYOR-MELEE CARVE-OUT.  LOKI_QUIET_ON above silences ALL builder
#     melee and that was a measured win -- acting and moving are mutually
#     exclusive for a builder and ARRIVAL is the scarce quantity, so pecking a
#     500 HP Core for 2 damage a round was buying nothing at the price of a
#     step.  It stays on.  What this arm adds is one exemption: an enemy
#     CONVEYOR or SPLITTER is 20 HP = ten pecks, and the tenth peck severs a
#     whole delivery chain.  That is a target where 2 damage a round finishes,
#     which is exactly the property the Core lacks.
#
# (b) SALT THE TILE.  Measured 2026-08-12: the field REPAIRS 40.5% of cut
#     conveyors at a median latency of 4 rounds, so a bare cut is undone in
#     about four rounds and the melee above would be a gift of tempo.  A
#     BARRIER on the dead tile is 3 Ti / 30 HP; clearing it costs them 15
#     builder pecks = 30 Ti and 15 builder-turns.  The barrier is what makes
#     the cut stick, and neither half is worth shipping without the other.
#
# ORDERING, and it is a programme requirement not a taste: PROGRAMME.md carries
# DEFENCE_ADMISSION_BAR: kill_round_non_regression.  Both behaviours sit BELOW
# the forward-sentinel attempt and BELOW the seat seal in _raid_act, so a round
# that could plant a Sentinel or seal a heal seat always does that instead.
# The salt block is the LAST thing a raider tries, after the buddy heal and the
# collar repair -- it spends only rounds the parent spent doing nothing.
#
# HOW THIS LOSES: every peck is a step not taken, and the carve-out re-opens
# the exact leak LOKI-QUIET closed.  If median kill round RISES, the trade is
# that a raider stopped ten rounds short of the ring to saw through a belt.
# The per-unit cap and the enemy-half restriction bound it; the kill-round bar
# decides it.
# ============================================================================

LOKI_SALTIDLE_ON = True      # master flag: False == the v169 parent, exactly
LOKI_SALTIDLE_LOG = False    # funnel tag "S48 <uid> reach open fire"
LOKI_SALTIDLE_DOWNSTREAM = True   # prefer the cut nearer their Core, free tiebreak
LOKI_SALT_LOG = False        # _v178salt's own SALT tags

LOKI_SALT_TI_FLOOR = 12      # bank floor for a salt barrier (matches LOKI_SEAL_TI_FLOOR)
LOKI_SALT_MAX_PER_UNIT = 4   # total barriers one raider may salt in its life
LOKI_SALT_BLOCK_ON = True    # also barrier an empty tile adjacent to a live belt
LOKI_SALT_BLOCK_MAX = 2      # of the cap above, at most this many are pre-emptive
LOKI_SALT_MEMORY = 8         # rounds a "an enemy belt piece stood here" mark lives
LOKI_SALT_CUT_MAX = 40       # per-unit peck budget on enemy belt (2 Ti each)


# ============================================================================
# LOKI-48 -- SALT, GATED ON AN IDLE RAIDER  (arm _v187saltidle)
#
# THIS IS A REVIVAL WITH THE DIAGNOSED CAUSE REMOVED, not a re-run.
# _v178salt went live on 2026-08-12 over 25 games against 5 opponents.  Its
# MECHANISM was confirmed: 20 of 20 corpse-salts landed on a tile that same
# raider had pecked to <=2 HP, median latency 1 round, and it dosed 6.68
# barriers/game against a 3.48-3.72 three-arm baseline.  It FAILED on the one
# bar that matters -- 13 kills at median r179 against a pooled r129,
# Mann-Whitney p=0.008, outside the bootstrapped 90% band.
#
# THE CAUSE WAS PRICED AT THE TIME AND IS NOT IN DISPUTE.  Cutting a 20 HP
# conveyor is ~10 raider ACTIONS; a builder may act OR move, never both; this
# line wins on ARRIVAL.  Salt bought denial with the only currency the collar
# cannot spare.  The verdict carried its own revival condition, written before
# this arm existed: "any revival must buy the denial WITHOUT spending raider
# actions -- e.g. salting only while a raider is already action-idle (25.76% of
# builder-rounds)."  Magnus then described the same case from a live replay
# unprompted: a builder standing ON their conveyor with nothing better to do,
# one cut and one barrier from severing a harvesting path permanently.
#
# WHAT CHANGED IS EXACTLY ONE THING: the gate.  The mechanism, the corpse
# memory, the enemy-half test, the caps and the ordering are _v178salt's,
# untouched -- 20/20 precision is not worth trading.  What is new is that being
# LAST IN _raid_act was never the right test.  Last-in-the-action-ranking only
# proves no better ACTION existed; the parent's answer to "no action" is to
# WALK, and `return True` cancelled the walk.  `_salt_idle_ok` reproduces the
# parent's own movement decision and permits salt only where that decision was
# already "stand still".
#
# THE READ.  Dose is EXPECTED TO FALL against 6.68/game -- that is the plank
# working, not failing.  The number this arm lives or dies on is MEDIAN KILL
# ROUND against the parent.  Materially cheaper: the plank is revived.  Still
# regressing: the idle-gate hypothesis is wrong and salt is dead for good.
# ============================================================================


# ============================================================================
# LOKI-L4 (v177) -- TRUNK REPAIR. The first deliberate reconnection this line
# has ever had.
#
# THE DEFECT, named in this file at HS_SEAT_BAN_CONVEYORS above and never
# fixed: "nothing re-plans a chain once its head is destroyed (the known L4
# defect)". `_link_path` plans one route when a harvester is built and
# `_build_next_link` pops each tile as it lays it; after the queue drains there
# is no planner left. A single conveyor pecked out of the middle of a finished
# trunk therefore stops that trunk for the rest of the match.
#
# THE SIZE OF IT, measured 2026-08-12 off 415 rated games against a
# 21,587-replay field control. We are cut at the field's rate -- 14.4% of our
# conveyor builds against 15.0% -- so being cut is normal and not a defect. The
# defect is the repair rate: 6.8% of our cut conveyors are relaid on the same
# tile inside 50 rounds, against 40.5% for the field and 50.3% among the very
# teams we play. And it has worsened monotonically by version:
#     v64-94 ~17-34%  ->  v102 14.3%  ->  v104 9.4%  ->  v112 5.6%
#     ->  v114 6.4%  ->  v115 9.6%
# consistent with the removal planks (LOKI-QUIET, LOKI-8) having deleted the
# loitering that used to cause ACCIDENTAL repair. On this branch there is not
# even that left: PAVE_TRAIL_ON is False, so the PIECE F trail -- this line's
# de-facto link repair -- never fires at all.
#
# WHAT THIS BUYS UNDER R1000_IS_DEFEAT, stated plainly because titanium does
# not score: a severed trunk is not a lost tiebreak, it is a bank that stops
# paying for bodies, ammunition and the forward sentinel. Economy is
# instrumental -- it buys the kill -- and a trunk that delivers nothing from
# r80 onward is a raid that runs out of titanium at r200.
#
# THE TEST IS STATELESS, LOCAL AND CANNOT RUN AWAY. See `EcoMixin._l4_repair`
# for the rule; the short version is that a tile is only repaired when there is
# already chain on BOTH sides of it, which makes it a HOLE rather than a HEAD.
# Extending a dead head toward the Core is the pave trail, and LOKI-13 measured
# that off at 38.20 conveyors per game against The Bisons' ~11.
#
# ⚠ AND THE FIRST BUILD OF IT WAS WRONG, CAUGHT BY COUNTING THE OUTPUT RATHER
# THAN READING THE LOOP. With "any adjacent harvester" as the upstream side,
# 36 of 55 repairs across 15 local games were a SECOND route for a harvester
# that already had one -- 3 Ti and +1% scale each, for zero throughput, because
# a harvester emits one stack per 4 rounds however many acceptors surround it.
# The harvester half is now gated on STARVATION (`_l4_harvester_starved`).
# A second thing the count said, and it changes what this plank IS: of the
# repairs the belt half fired on, only 1 tile had ever HELD a conveyor. The
# rest are DEAD HEADS -- chains this bot abandoned mid-walk, which
# `_build_next_link` never revisits because it pops its queue as it lays it.
# So the L4 defect has TWO halves and only one of them is the enemy's doing.
# ============================================================================

LOKI_L4_REPAIR_ON = True        # the whole plank; False == the parent exactly
# Only repair holes on our own side of the map. A stood-down raider calls
# _expand wherever it happens to be standing (raid.py:149,163), and a builder
# bot's action and its move are mutually exclusive -- the doctrine of this
# whole line is that ARRIVAL is the scarce quantity. A raider spending its
# round relaying 3 Ti of belt under the enemy's guns is the trade LOKI-QUIET
# and LOKI-8 were built to stop.
LOKI_L4_OWN_HALF_ONLY = True
# Instrumentation only: one print per repair, into the replay. OFF by default
# so a battery does not pay for it. Platform-downloaded replays strip stdout,
# so this is a LOCAL instrument and nothing may be read off a live leg with it.
# ON in this tree (v215): the dose tag "L4R45" is how this port is verified.
LOKI_L4_LOG = True
