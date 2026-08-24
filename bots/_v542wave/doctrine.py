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
    # --- s58 SECOND ROTATION (2026-08-24 ~11:0xZ, mid-ship): the pool
    # rotated AGAIN to 15 all-new maps; encoded within minutes of the
    # rotation — the expiry class from BUILD-REPORT-wave-catalogue, caught
    # live this time. ---------------------------------------------------
    ((28, 24, 2, 1, 2, 21), "AAAAAAAAAAAAGAAACAAAAAAAAAAAAAAAAAAAAAAJNAAJNAACABAAAABGAADA0CADAAAJAYIAJAAAABAAAABAAAMEAAMEAAAAAAAAAAJNNBAEAJNANNEAMAANBAAAAAAAAAAAANBAANBAAADAAAADAAAJAYIAJAAAABS0AABAGADAAAADSAAJNAAJNAAAAAAAAAAAAAAAAAAAAAAAGAAACAAAAAAAAAAA"),  # bergen [s58 ROTATION 2 encode, selftest-passed]
    ((30, 30, 1, 14, 27, 14), "AAAANNAAAAMNNBNNMNAIMIABNNVPAHVAABNNVPAAVMBBNNVPAADDAANNMMAADDAANNAAAADDAANNAAMEMEAANNAAVFAAAANNAAMEAAAANNAAAAAAAANNAAAAAAAANNAAAAAANBNNJNAAAAHANNAPAAAAHANNAPAAAANBNNJNAAAAAANNAAAAAAAANNAAAAAAAANNAAAAMEAANNAAAAVFAANNAAMEMEAANNAADDAAAANNAADDAAEENNAADDAAHFNNJJEFAAHFNNJAAFPAHFNNJAYEYANENNJNNEAAAANNAAAA"),  # copenhagen [s58 ROTATION 2 encode, selftest-passed]
    ((28, 28, 2, 1, 24, 25), "AAAAAAAAAAAASAAAAAAAAACAMEAAAANAAJNAAAAMBAANBAAAJEAAAEAAAGAAJBMAAAMEAAEJBAALNAAMSCAAGNBAJBAJEAADAAEAANAAMAAMAAMBAJBAJNSCAAAEAANBICAAUCNBAJBAAAIMEAAEAANAAMAAMAAMBAJBAJAAJEAAEAANTAAAIMAAMECAAEJBAJNAAAMAEAASAAAJBAAJEAAAANBAANAAAAMEAAMBAAAJNAACAAAAAAAAGAAAAAAAAAAAAA"),  # gothenburg [s58 ROTATION 2 encode, selftest-passed]
    ((30, 30, 14, 27, 14, 1), "AAAAAAAAAAAAPAAAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMEMEAAAAAJBAAJBAAAAVJEMBFAAAAHDAADPAAAABBEMJJAAAJJJAABBBAAJDDMEDDBAAJDBBJJDBAAJXKJBKXBANNNKVFKNNNNNNKVFKNNNAJXKJBKXBAAJDBBJJDBAAJDDMEDDBAAJJJAABBBAAABBEMJJAAAAHDAADPAAAAVJEMBFAAAAJBAAJBAAAAAMEMEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPAAAAHAAAAAAAAAAAA"),  # helsinki [s58 ROTATION 2 encode, selftest-passed]
    ((20, 12, 1, 4, 17, 4), "AAAAAAAIAAAAYAJBAAEAAMAAJBAAASCAAAAAYAAAAAAIAAAAASCAAAJBAAEAAMAAJBAIAAAAYAAAAAAA"),  # mariehamn [s58 ROTATION 2 encode, selftest-passed]
    ((18, 18, 1, 1, 1, 15), "AAAAAAAACACCAAAAAAAAAAAANEMEMNDDDDDDGDVFDGDDVFDDAAAAAAAAAAAADDVFDDGDVFDGDDDDDDNEMEMNAAAAAAAAAAAAAACACCAAAAAA"),  # nuuk [s58 ROTATION 2 encode, selftest-passed]
    ((26, 20, 1, 9, 23, 9), "AAAAAAAAACBBAAJJSAJJAAADDAADDAAABBAABBAAJJAAJAAAAADAAVAAAASBAABAAAAJAAAJA0CDAAAADS0ABAAAABYIJAAAAJA0CDAAADAAAAABAAHAAAAPAAJAAAAADAADDAAABBAABBAAJJAAJJAAADDAGDDAAABBCAAAAAAAAA"),  # odense [s58 ROTATION 2 encode, selftest-passed]
    ((30, 30, 2, 26, 26, 2), "NBAAAAAAAANESCAASCAANNSCAAJBAANKBAAAAAAAMKEAAJAAAAJNNAAABAAAANNBAADAAAAMKEAAJAAAYJKNAAABAHYANKBAADAHAAMKEAFJAAAAJNNAPABAAAANNBSADAAAAMNEAAAAAAAJNNAAAAAAAANNBAAAAAAAMNEAAAADACJNNAAAAJAHANNBAAAABVAMKEAAPADAAJKNAIPAJAAANKBIAAABAAMKEAAAADAAJNNAAAAJAAANNBAAAABAAMKEAAAAAAAJKNAAJBAASCNNAASCAASCMNAAAAAAAAJN"),  # oslo [s58 ROTATION 2 encode, selftest-passed]
    ((20, 20, 2, 1, 2, 17), "AAAAAAAAAAAACAAAAASAAAAAAAJJNEMNBBADAJAAAAT0DAAGJYIBGAADAJAANBBADMNNJAABNBADAJAASAT0DSAAJYIBAAADAJAABNNJNEDAAAAAAAAAAASAAAAAAGAAAAAAAA"),  # reykjavik [s58 ROTATION 2 encode, selftest-passed]
    ((24, 20, 1, 9, 21, 9), "AAAAAAAAYAAAAAAIANBEMJNAAAVDDFAAMADDDDAEMGDAADGEAMDEMDEAAMAEMAEAAMGEMGEAAMAEMAEAAMAEMAEAAMGEMGEAAMAEMAEAAMDEMDEAMGDAADGEMADDDDAEAAVDDFAAANBEMJNAYAAAAAAIAAAAAAAA"),  # stavanger [s58 ROTATION 2 encode, selftest-passed]
    ((30, 30, 4, 1, 4, 27), "AAAAAAAAAAAAAGAASAAAAAAGAASAAAAAAAAAAAAAJNNAAANBAAAAJAAANBAAGAJAAAAAAAGAJAJNAAAAAAJAJNAAAAJNNEAAAAAAAAADAAS0AAAAADAAS0AAAAADAAMBAAAAAAAAMBAANBANBJNAMNNBANBJNAMNAAAAAAMBAAAAADAAMBAAAAADAAS0AAAAADAAS0AAJNNEAAAAAAAAJAJNAAAAGAJAJNAAAAGAJAAAAAAAAAJAAANBAAJNNAAANBAAAAAAAAAAAAAAAGAASAAAAAAGAASAAAAAAAAAAAAA"),  # stockholm [s58 ROTATION 2 encode, selftest-passed]
    ((24, 24, 3, 1, 19, 21), "AAAAAAAAAAAAAAAAAAAAGAAAAAAAGAAAAAAAAASAAJNAAAAAAJNAAASAAAAAAAAAGAAAAAAAGAAANBAAAAAANBAAAAAAAAAAAAAAAAAAAAJNAAAAAAJNAAAGAAAAAAAGAAAAAAAAACAAANBAAAAAANBAACAAAAAAAAAGAAAAAAAGAAAAAAAAAAAAAAAAAAAA"),  # tampere [s58 ROTATION 2 encode, selftest-passed]
    ((18, 18, 1, 1, 15, 15), "AAAAAAAASACAAASAAAAAAASAAEAASAAEAAAAGAAIAAGAAIAEAAAAAEMAAAAAMAYAAGAAYAAGAAAAMAACAAMAACAAAAAAACAAASACAAAAAAAA"),  # torshavn [s58 ROTATION 2 encode, selftest-passed]
    ((26, 22, 1, 10, 23, 10), "AAAAAAAAAIAAAAAAYAMBAAAANAANAAAAJEAAAAAAAAAAAJBAAEAAAAMAIJBAACAESCMASAAJBAAEAAAAMAAJBAAAADAADAAAAABAABAAAAMAAJBAAAAEAAMAASAJBYAEAGAAMAIJBAAAAEAAMAAAAAAAAAAAANAAAAJEAJEAAAAMBSCAAAAAAIAAAAAAAAA"),  # trondheim [s58 ROTATION 2 encode, selftest-passed]
    ((22, 22, 1, 10, 19, 10), "AAAAAAASCAAAASCMEAAANBAJAAADAAABAAJAAADJNABAAJABBDASABVFJACADJRABAAJABBDAAABAAJAAADAAABAAJABBDAAABDDJAACDJRABGAJAZBDAAABMEJAAADAAABAAJAAADAANBAAJNAIAAAAAIAAAAAAAA"),  # uppsala [s58 ROTATION 2 encode, selftest-passed]
    # --- s58: the CURRENT 15-map pool (was fully uncatalogued in this tree —
    # known_map_for returned None on every live map, killing the ore
    # partition AND all pathfinding; the s36 livelock class, re-measured on
    # bifrost as 350-round 2-cycles pinning the harvester ratchet at 1) ----
    ((20, 20, 9, 1, 9, 17), "AAAAAAAAAAAAASAAAAAGAAAAAAJBMEJNABMNBNNAACAAAGAASAACAMEANBJNAAAIAAAAASCAAMEANBJNAACAGAASAAAACAMNBNNAEJNANBDAAAAAASAAAAAGAAAAAAAAAAAAAA"),  # auroraveil [s58 pool encode, map_encode.py selftest-passed]
    ((26, 12, 2, 5, 22, 5), "AAAAAAAAACAAIYAASAJNAAAMEAAADAAABAAAABSCJAAAAJAYADAAAADAIABAAAABSCJAAAAJAAADAAAMEAAANBACAAIYAASAAAAAAAAA"),  # bifrost [s58 pool encode, map_encode.py selftest-passed]
    ((20, 20, 2, 1, 16, 17), "AAAMAMAAAMAMAAAAEAEAAAMAJBCAAEAMASMAAAMAAEAIAEAGJBJBAACMAMACAAAEAAAAAJBAAACMAMACAAEAESAJBSCJBAMAAAMGAMAJBAACEAMAAAJBJBAAAMAMAAAMAMAAAA"),  # fimbulwinter [s58 pool encode, map_encode.py selftest-passed]
    ((30, 30, 14, 2, 14, 26), "NDAAAAAADNEDAAAAAADMBCAAAAAASJSEAAAAAAMCEBAAAAAAJMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAEMAAAAAAAJAABAAAAAAJAABAAASAACSCSAACSAACSCSAACAAAJAABAAAAAAJAABAAAAAAAEMAAAAAAAAAAAAAAAAAAAAAAAAAACAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAAAAAAJMSEAAAAAAMCBCAAAAAASJEDAAAAAADMNDAAAAAADN"),  # glacierkeep [s58 pool encode, map_encode.py selftest-passed]
    ((18, 18, 2, 8, 14, 8), "AAAAAAGAMEAGAMBJEAAMBJEAAMBJEASAAAACAAYIAAAAMEAAAAMEAAAAMEAAAAMEAAAAYIAASAAAACAMBJEAAMBJEAAMBJEAGAMEAGAAAAAA"),  # helheim [s58 pool encode, map_encode.py selftest-passed]
    ((12, 12, 1, 1, 9, 9), "AAAAAACSAAAAAJBAAMAAGAAAAAAGAAEAAJBAAAAACSAAAAAA"),  # holmgang [s58 pool encode, map_encode.py selftest-passed]
    ((20, 20, 1, 16, 17, 2), "AAAAAAACSAAAAAAJBAAAAEDSAASAAAAAAAAAAMAAAGACDAAMAAAEAAMAAUSAGDAEAAAAAJBJSAGGCAMAAJBAAMAAJACSAAAMAAAAAAAAAAGAAGJJBAAAAEAAAAAAGACAAAAAAA"),  # icefloe [s58 pool encode, map_encode.py selftest-passed]
    ((24, 24, 4, 4, 18, 18), "AAAAAAAAAAAAAAAAAAAMEAYAAAAAAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAJEAAAAAAJEAAAAAAJEAAAGAAAYIAAAAAAYIAAAGAAAMBAAAAAAMBAAAAAAMBAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAIAMEAAAAAAAAAAAAAAAAAAA"),  # jotunheim [s58 pool encode, map_encode.py selftest-passed]
    ((28, 18, 2, 8, 24, 8), "AAAAAAAAAACAAAAAASAJNNBAMNNAAGADAJASAAAAJAABAAAAAABIDAAAAAADYJAAAAAAJAABAAAAAABADAAAAAADAJAAAAAAJAABAAAAAABADAAAAAADYJAAAAAAJSCBAAAACABADAGAANNEAJNNBACAAAAAASAAAAAAAAAA"),  # longhouse [s58 pool encode, map_encode.py selftest-passed]
    ((30, 30, 2, 2, 26, 26), "AAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAASAAAAAAADABAAAAAAADABAAAAAASDABAAAAAAAMEAAAAAAAAAAJEAAAAAACGAAAAAAAAMBMEMEAAASAJDAADAAAAAJDAADAAAAAJDAADAAAAAAASCAAAAAAAASCAAAAAAADAADBAAAAADAADBAAAAADAADBACAAAMEMEJEAAAAAAAAGSAAAAAAMBAAAAAAAAAAMEAAAAAAAJADCAAAAAAJADAAAAAAAJADAAAAAAACAAAAAAAAAASAAAAAAAAAAAAAAAAAAAAAA"),  # midgard [s58 pool encode, map_encode.py selftest-passed]
    ((24, 24, 1, 11, 21, 11), "MKENNMKEVKFZRVKFDKDBJDKDDKAAAAKDDAAAAAADAAAMEAAAAAMWOEAABMEAAMEJCDAAAADSBAAMEAAJAJNEMNBAAAAPHAAAAAAPHAAAAJNEMNBAAAAMEAAABEAAAAMJCMEAAMESBAMWOEAJAAAMEAAADAAAAAADDKAAAAKDDKDBJDKDVKFZRVKFMKENNMKE"),  # paths [s58 pool encode, map_encode.py selftest-passed]
    ((16, 16, 7, 1, 7, 13), "AAAAAAAAAAAACAGAAAAAAAEAAMAMAIJBAAYAASAAAACCAAAGAAYAAAESCMAMAAJBAAAAAASAACAAAAAAAAAAAA"),  # skald [s58 pool encode, map_encode.py selftest-passed]
    ((22, 22, 9, 2, 9, 18), "AAAAAAAACAAAASAAAAAAAAAAAAAAAASAAAACAMNBAMNBJAAAAADABJNNBJADABADABJAD0LADABAAAAJADAAAAABJAD0LADABJAABJADANNEABJAAAAADANNAANNAACAAAGAAAAAAAAAAAAAAAAGAAAAACAAAAAAAA"),  # stavkirke [s58 pool encode, map_encode.py selftest-passed]
    ((30, 30, 2, 14, 26, 14), "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAJBAACAAAAADDAAAAAAAABJAAAAAAAJAABAAASAADAADAACAAAEAAMAAAAAJCAASBAAAAAAAAAAAAAAKAAAAKAAAMDAAAADEAADAAAAAADAAABSAACJAAAABSAACJAAADAAAAAADAAMDAAAADEAAAKAAAAKAAAAAAAAAAAAAGJBAAJBGAAAAEAAMAAASAADAADAACAAAJAABAAAAAAABJAAAAAAAADDAAAAAASAJBACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),  # valkyrie [s58 pool encode, map_encode.py selftest-passed]
    ((30, 30, 3, 3, 25, 25), "AAAAAAAAAAAAAMNNBAAAAAAAAAAAAAAAAAAAAAAAAAAJAAAAAAAAAJAAAEAAAAJNBAAEAAAAJUBAAAAAGBJABAAASAABJUBAAAAAABJKBAAAAAABAAAAAAAAATAAAAJNNBABAAAAAAAAAAAAYIAAAAAAAAYIAAAAAAAAAAAAJAJNNBAAAALAAAAAAAAAJAAAAAAJKBJAAAAAAJUBJAACAAAJABJGAAAAAJUBAAAAMAAJNBAAAAMAAABAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAJNNEAAAAAAAAAAAAA"),  # yggdrasil [s58 pool encode, map_encode.py selftest-passed]
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

# ===========================================================================
# LOKI-BELTBREAK (s48) -- THE FORWARD ECONOMY-SHREDDER GUNNER.
#
# WHAT THIS TREE ADDS, IN ONE SENTENCE: a code path that can plant a GUNNER on
# a tile in the d^2 20-100 annulus of the ENEMY Core, aimed at a belt or
# harvester tile that EXISTS RIGHT NOW.  The base tree has no such path.
#
# THE MEASURED BASIS (cited, not re-derived --
# docs/research/REPLAY-STUDY-offensive-gunner-2026-08-17.md, commit ed03edc3):
#
#  * THE ANNULUS IS AN IDENTITY, NOT A CORRELATION.  Across 3,662 current-
#    version in-band gunners on six teams the share of shots at the enemy CORE
#    is 0.000 -- a gunner reaches r^2=13 (3 tiles); past ~4.5 tiles it cannot
#    reach the core, so everything it CAN shoot is economy.  Excess belt-kills
#    per gunner peak at d^2 20-30, hold to d^2<100, are zero by 170.  (Study
#    §3.6, research's placement gradient.)
#  * WE HAVE NO SUCH PATH.  `raid.py:688 tiles = core_tiles(E)` plus the
#    `d^2 <= 32` filter plus the pre-scan bail `dsq_core(p, E) > 50` means the
#    raider must WALK TO the core footprint before any forward plant is legal,
#    and since v102 every gunner call site in the tree is `_try_counterbattery`
#    -- home defence keyed to HUNT_BAND_DSQ=41 of OUR OWN core.  (Study §5.1.)
#  * THE GUNNER IS THE RIGHT TURRET FOR A 20-HP TARGET: conveyor/splitter costs
#    3 gunner shots = 12 ammo against a sentinel's 2 shots = 20 ammo (0.60x),
#    and the gunner is 20 Ti against 30.  It is the WRONG turret for a core
#    (288 ammo vs 280 at 1.6x less reach).  (Study §6.)
#
# THE v94 FAILURE THIS MUST MAKE IMPOSSIBLE BY CONSTRUCTION.  `_v115dodge`'s
# `_plan_siege` scored a tile by whether its ray reached where the enemy core
# IS, rejecting a ray only if it crossed a STATIC MAP WALL -- no live-target
# predicate at all.  Measured off the replays without seeing that code: econ on
# the chosen ray 0.09 against a RANDOM ray 0.11 (i.e. BELOW random), 51.7% of
# gunners built with nothing in range, 7.9% never firing.  ⇒ EVERY plant here
# is gated on `can_fire_from(bp, facing, GUNNER, t)` where `t` is a live enemy
# entity read out of THIS builder's vision this round.  A tile scoring 0 is
# rejected.  There is no geometric fallback and no "where belt should be".
#
# WHY IT DOES NOT RE-OPEN THE v102 ARGUMENT.  `_v105loki1/raid.py:32-37` and
# LOKI_BARRIER_SEAL_ON's block above are correct: our own barrier collar blocks
# a gunner ray, so a gunner planted to shoot the CORE THROUGH our collar is
# shooting our own barriers.  BELTBREAK never shoots the core and never sits
# behind the collar -- the collar is on the enemy ring (d^2 ~2-8) and the band
# starts at d^2=20.  The ray is additionally checked for OUR OWN buildings tile
# by tile (`_bb_ray_clear`), belt-and-braces over the engine's own LOS.
#
# TARGET LADDER (study §7.2, which is the §6 ammo table restated):
#   HARVESTER 100 > CONVEYOR/SPLITTER 40 > (everything else 0 for SITING).
#   CORE scores ZERO -- that is the single biggest correction to v94, 52.8% of
#   whose gunner shots went at cores.  BARRIER scores ZERO for siting and is
#   HELD FIRE on for shooting: barriers are the measured 34.1% ammo leak.
#
# ROTATION: AT MOST ONE PER GUNNER, EVER.  Field median is ZERO rotations per
# gunner (Pantheon 0.65 mean, O(1) 0.17); our v94 burned 4.32 rotations x 10 Ti
# = ~43 Ti/gunner with 62.6% of facing segments firing zero shots, and GUNPIN's
# rotate-thrash arm read 44.27.  LOKI_BELTBREAK_MAX_ROT = 1 makes an A->B->A
# oscillation impossible by construction rather than by cooldown tuning.
# ⇒ Deliberately NOT the GUNPINA (`LOKI_GUNNER_HOLDFIRE`) design, which held
# fire and never re-aimed at all: that solo read negative on the v140 base, and
# for a gunner planted deep in enemy territory, idling aimed at a barrier for
# the rest of the match is the one outcome worse than paying 10 Ti once.
#
# THE TIMING FLAG IS THE REGISTERED CONTRAST, AND IT IS ONE INTEGER.
# LOKI_BELTBREAK_EARLY picks WHICH ROUND THE PLANT GATE OPENS and changes
# nothing else -- same siting rule, same cap, same funding, same fire policy:
#     EARLY (True)  -> plants legal from LOKI_BELTBREAK_RND      = 25
#     LATE  (False) -> plants legal from LOKI_BELTBREAK_LATE_RND = 70
# 25 vs 70 is the study's own leg: *"move our first plant ~45 rounds earlier"*
# (§7.1), EARLY sitting in the executor band (ph median 21, not adgato 13,
# field median first in-band plant r37) against our version-stable r56-85.
# ⚠ READ THIS AS AN OPENING ROUND, NOT A WINDOW THAT CLOSES, AND THE REASON IS
# GEOMETRIC: our median forward ARRIVAL is r31 (FORWARD-ARRIVAL-BASELINE), so
# an arm gated `rnd <= 25` would be empty by construction for most maps -- it
# would measure "we cannot walk there in 25 rounds", not "an early plant pays".
# Demonstrated, not assumed: see the s48 demo note in the build report.
#
# ⛔ THE CAP HAZARD, AND WHAT THIS PLANK DID ABOUT IT.  LOKI_FWD_GUN_CAP counts
# `SLOT_FWD_GUN`, which is written ONLY as `read + 1` and never decremented --
# i.e. it counts RUBBLE, and three dead forward turrets close that arm for the
# match unless LOKI2B_LIVE_CAP_ON's census is what is actually deciding.
# BELTBREAK DOES NOT TOUCH THAT COUNTER AT ALL.  Its own cap is a LIVE CENSUS
# of friendly GUNNERs standing in the annulus (`_live_beltbreak_guns`), so
# rubble cannot close this arm, and `_live_fwd_guns` counts only SENTINELs so
# the sentinel arm cannot see a beltbreak gunner either.  The two arms share no
# counter and no slot.
#
# ===========================================================================
# LOKI-BELTBREAK2 (s48) -- THE DOSE ITERATION.  ONE INTEGER: 25 -> 10.
#
# THE ONLY EXECUTABLE DIFFERENCE FROM `_v480beltbreak` IS THE LINE BELOW.
# `LOKI_BELTBREAK_RND = 10` replaces 25.  Everything else in this tree --
# doctrine, main, raid, eco -- is byte-identical to the parent.  Setting this
# constant back to 25 restores the parent's behaviour EXACTLY, which is the
# flag-off control for this arm (there is no new flag to add: the parent
# already made this integer the registered dose knob).
#
# WHY THE TIMING AXIS AND NOT THE OTHER THREE.  Measured, s48, on the LOCAL
# 15-map pool at --tle 10 with `bots/_v468kladturbo` as opponent, treatment in
# seat A, 8 seeds x 15 maps = 120 games PER ARM, one common seed set.  The dose
# is counted ENGINE-SIDE off the replays: a SHREDDER is a friendly GUNNER whose
# first `placeEntity` (rotation re-emits skipped) lands at d^2 20..100 of the
# ENEMY core AND d^2 > HUNT_BAND_DSQ(41) of OUR OWN core -- the second clause
# is what separates this weapon from a home counter-battery gunner that
# satisfies the annulus as pure geometry on a small map, and from the
# core-adjacent forward SENTINEL path, which is a different weapon on a
# different counter (`SLOT_FWD_GUN`) and cannot be a GUNNER at all.
#
#   arm            RND  shredders/game  zero-shredder games  med plant rnd  shots/shredder
#   parent          25       1.358           48/120 = 40.0%        45            22.4
#   this arm        10       1.450           34/120 = 28.3%        38            31.0
#   (probe)         15       1.433           37/120 = 30.8%        38            25.2
#   (probe)          1       1.550           29/120 = 24.2%        36.5          33.4
#   (probe) CAP 2->3 25      1.358           51/120 = 42.5%        48            21.9
#
# ⭐ REPRODUCED ON A SECOND, LARGER, BOTH-SEATS FIXTURE (fresh seeds
# 930000-930005, 15 maps x 2 seats = 180 games PER ARM, --tle 10):
# shredders/game 1.122 -> 1.444 (+28.7%), zero-shredder games 48.3% -> 28.3%,
# median plant round 49.5 -> 40.0, plants in the newly-legal r10-24 window
# 0/202 -> 66/260, never-fired 3.5% -> 1.5%, planted-then-died 21.8% -> 18.8%.
# Dose rose on 10 of 15 maps, fell on 3, was flat on 2.
# ⚠ AND THE ONE NUMBER THAT DID NOT REPRODUCE, SAID HERE BECAUSE THE TABLE
# ABOVE IS THE FLATTERING VERSION: shots/shredder read 22.4 -> 31.0 on the
# seat-A 120-game sweep and 25.7 -> 24.7 (i.e. FLAT) on this larger both-seats
# battery.  Treat the +38% as seed-set noise and the honest claim as: this arm
# buys ~29% MORE shredders each doing the SAME work, not better shredders.
#
# ⛔ RAISING THE CAP IS A MEASURED NULL ON DOSE, NOT AN ARGUMENT ABOUT ONE.
# `LOKI_BELTBREAK_CAP = 2 -> 3` moved shredders/game by 0.000 on the common
# seed set (1.358 both), raised the median plant round the WRONG WAY (45 -> 48),
# and left shots/shredder flat (22.4 -> 21.9) -- while it would have bought a
# permanent +20% on the ONE GLOBAL ADDITIVE cost-scale factor per extra gunner.
# The funnel says why: an instrumented copy of the parent (unrate-limited
# refusal counters, 30 games) refuses on `CAP` 6.6 times per game against
# `TI` 638 -- the cap is not what is stopping the third shredder, the bank is.
# And the magazine is sized for two: LOKI_BELTBREAK_AMMO = 24 is exactly two
# 12-ammo belt kills (gunner 4 ammo/shot, 7 dmg, 20-HP conveyor = 3 shots), so
# a third gunner under an unchanged magazine cannot complete one kill.  That is
# a null with extra cost, and it would have read on the tape as "more
# shredders do not pay".
#
# ⛔ AND THE GATE SATURATES AT ~10, WHICH IS WHY THIS IS NOT `RND = 1`.
# Below ~10 the binding constraint stops being the gate and becomes ARRIVAL
# (our median forward arrival is r31).  Plants in the newly-legal window:
# RND=10 puts 46 of 174 shredders (26.4%) at r10-24, a region the parent
# reaches 0 of 163 times BY CONSTRUCTION.  Dropping the gate the rest of the
# way to 1 adds only 8 of 186 (4.3%) at r<10 and moves the median plant round
# 38 -> 36.5 -- i.e. nine more rounds of gate removal buy nearly nothing, while
# they are the nine rounds where a +20% scale contribution compounds through
# every harvester and conveyor built for the remaining ~990 rounds.  10 keeps a
# nonzero opening guard AND captures essentially the whole available gain.
#
# ⭐ DIRECTION ON THE REGISTERED `TW` HAZARD: SAFE.  An arm that DELAYS our
# first visible turret re-enables the opponent weapon that is gated on never
# having seen one (x3r0's Odin).  This arm moves the first forward turret
# EARLIER (median 45 -> 38, and 26.4% of plants now land before r25), so it
# moves that hazard in the safe direction.  The LATE twin (`RND = 70`,
# `_v483beltbreaklate`, floor-stopped at 47.39) moved it the unsafe way.
#
# WHAT THIS ARM DOES *NOT* CLAIM.  120 games per arm cannot read game share
# (+-9pp) and cannot read the DEFENCE_ADMISSION_BAR timely-kill rate; nothing
# above is a currency read and no number here is a bar.  The currency claim
# this dose extrapolates is the PARENT's, at n=3053: EARLY(25) 52.90%
# [51.13, 54.67] against the LATE(70) twin's 47.39 floor-stop -- a steep
# monotone gradient in the earlier direction, which is the only powered dose
# measurement this plank has.  ⚠ THE ONE LOCAL COUNTER-SIGNAL, STATED BECAUSE
# IT IS UNFLATTERING: at n=120 the r1000 share read 0.117 (parent) vs 0.150
# (this arm) and the treatment timely-kill rate 0.367 vs 0.300.  Both are well
# inside noise at that n (+-7pp and +-9pp), both are NON-MONOTONE across the
# four RND probes (r1000: 25->.117, 15->.133, 10->.150, 1->.125), and neither
# is resolvable locally -- but they point the wrong way and the powered leg is
# where that gets settled, not here.
# ===========================================================================
LOKI_BELTBREAK_ON = True        # master switch; False == _v468kladturbo exactly
LOKI_BELTBREAK_EARLY = True     # the registered timing arm (see above)
LOKI_BELTBREAK_RND = 10         # EARLY arm: plant gate opens at this round.
                                # ⭐ THE DOSE.  Parent `_v480beltbreak` has 25;
                                # set it back to 25 and this tree IS the parent.
LOKI_BELTBREAK_LATE_RND = 70    # LATE  arm: plant gate opens at this round
LOKI_BELTBREAK_DSQ_LO = 20      # the productive annulus, inner edge (d^2)
LOKI_BELTBREAK_DSQ_HI = 100     # the productive annulus, outer edge (d^2)
LOKI_BELTBREAK_CAP = 2          # live beltbreak gunners at once (study MAX_LIVE_FWD_GUN)
LOKI_BELTBREAK_MIN_HARV = 1     # one harvester, not LOKI_FWD_MIN_HARV's two:
                                # a 20-Ti gunner is not a 30-Ti sentinel and the
                                # opening bank pays for it outright.
LOKI_BELTBREAK_AMMO = 24        # two 12-ammo kill cycles held for the gunner
LOKI_BELTBREAK_TI_FLOOR = 40    # reserve left after paying, WHEN NOT PRIORITY
LOKI_BELTBREAK_STALE = 3        # heartbeat rounds before the Core stops funding
LOKI_BELTBREAK_MAX_ROT = 1      # rotations per gunner PER LIFE.  Hard cap.
LOKI_BELTBREAK_MAX_TGT = 12     # siting targets considered, nearest first (CPU)
LOKI_BELTBREAK_LOG = True       # LOCAL demo instrument; print() is stripped from
                                # platform replays (see CLAUDE.md), so nothing
                                # may ever be read off a live leg with this.

# SLOT 13 was SLOT_DEFEND_BEAT in the pre-LOKI store map and is READ AND
# WRITTEN BY NOTHING in this tree (verified: `grep SLOT_DEFEND_BEAT` returns
# only its definition).  It is the beltbreak heartbeat: the round+1 in which
# some beltbreak gunner last had a live target, or in which a raider planted
# one.  It is NOT a count and NOT monotone -- it goes stale on its own, which
# is exactly what SLOT_FWD_GUN's ghost magazine could not do.
SLOT_BELTBREAK = 13

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


# ============================================================================
# LOKI-TURBO -- CPU tables.  NOT doctrine: no constant below changes a single
# decision this bot makes.  They exist because Position.add() rebuilds a
# nine-entry dict inside Direction.delta() on EVERY call and measures 1.35 us
# against 0.08 us for the same arithmetic on raw ints (measured 2026-08-15,
# 200k iterations, this desktop).  _bfs_direction alone called it ~3,600 times
# per invocation on a 30x30 map, which is the whole of the 3.5-5.7 ms flood
# that loki_analysis.md 5.2 blames for the 61% builder TLE rate on the server.
#
# DELTA           -- Direction -> (dx, dy), for the 8-way and get_direction()
#                    call sites where the direction is a runtime value.
# CARD_DELTAS     -- (dx, dy) in exactly CARDINALS order (N, E, S, W), so an
#                    index into one is an index into the other.
# DIR_DELTAS      -- (dx, dy) in exactly DIRECTIONS order.
# CARD_OPPOSITE   -- index of the opposite cardinal, i.e. CARDINALS[(i+2)%4];
#                    identical to Direction.opposite() restricted to cardinals.
# NAV_NODE_BUDGET -- hard cap on nodes expanded by one _bfs_direction flood.
#                    A flood visits each passable tile at most once, so on the
#                    largest pool map (30x30 = 900 tiles) it CANNOT fire; it is
#                    a bound for a hypothetical future map, replacing the old
#                    wall-clock probe every 64 steps (time is frozen in the
#                    sandbox, so a self-timer is not available either way).
# ============================================================================

DELTA = {d: d.delta() for d in Direction}
CARD_DELTAS = tuple(DELTA[d] for d in CARDINALS)
DIR_DELTAS = tuple(DELTA[d] for d in DIRECTIONS)
CARD_OPPOSITE = (2, 3, 0, 1)
NAV_NODE_BUDGET = 4096


# ============================================================================
# LOKI-TURBO4 (2026-08-15) -- THE CORE DIED WITH FOUR EMPTY HEAL SEATS AND A
# MAGAZINE NOBODY COULD FIRE.
#
# Decode of `replays/ladder_ours/a9a84d67-058b..._game_2.replay26` (frostgate,
# we are A = loki_turbo v151, lost core_destroyed @ r96), cross-checked against
# all 35 v151 ladder games in that directory:
#
#  1. GHOST MAGAZINE.  `SLOT_FWD_GUN` and `SLOT_HOME_GUN` are written only as
#     `read + 1` and are NEVER decremented, so `weapons = home + fwd` counts
#     rubble.  In the decoded game slot 8 reads 1 from r16 to the end while our
#     only Sentinel (#52) died at r38.  With `fwd_guns = 1` the Core's target is
#     `min(120, 40 + 20*fwd) = 60`, so it converted 16 Ti on each of r17, r18,
#     r19, r20 -- 146 Ti over the match against 170 Ti COLLECTED IN THE WHOLE
#     GAME (86%) -- and 27-36 of that ammunition then sat unusable from r38 to
#     r96 with zero turrets alive.  Corpus: **1,056 rounds across the 35 games
#     holding >= 10 ammo with NO live turret (worst hold 60)**, and **8 of 35
#     games converted more titanium than they ever mined -- all 8 are losses.**
#     `weapons` truthy also drops `ti_floor` from 52 to 12, so ghost turrets
#     unlock exactly the drain E1_AMMO_FLOOR was written to stop.
#
#  2. THE DEFENDER CHASES A BUILDER IT CANNOT TOUCH.  engine_mechanics.md E:
#     `can_fire(tile_with_enemy_builder_bot)` is **False, always** -- builders
#     cannot attack builders.  `_nearest_home_intruder` looks for
#     `EntityType.BUILDER_BOT` and nothing else, and its branch in `_defend`
#     sits ABOVE the `_core_shelled -> _seat_seek_target` branch.  In the
#     decoded game our defender #14 and enemy builder #13 two-cycled in
#     lockstep -- #14 (0,8)<->(0,9), #13 (1,7)<->(1,8) -- for 46 CONSECUTIVE
#     ROUNDS, r51 to r96, spending its move every round on a chase that cannot
#     resolve, while the Core went 403 -> 0 and FOUR heal seats stood empty.
#     Zero heal actions in the entire game.  Corpus: **1,880 damaged-core
#     rounds show a two-tile lockstep inside the home band, 1,605 of them in
#     losses.**
#
#  3. NOBODY IS ELIGIBLE TO CONVERGE.  Multi-healer convergence (eco.py
#     `_expand`) is gated `role_n >= 2`.  The roster is seat 0 raid, seats 1-3
#     expand (seat 3 defects to the raid at harv >= ECO_NEED), seat 4 defend,
#     seat 5+ raid -- so in a six-builder game the ONLY eligible converger is
#     seat 2.  In the decoded game seat 1 (#5) sat at (3,7), d^2 = 5 from the
#     Core with the Core visibly bleeding, and was excluded by the gate; seat 2
#     (#8) sat at (4,4), d^2 = 29 -- and a builder's vision is r^2 = 20
#     (engine_mechanics.md J), so `_core_shelled` could not SEE the Core and
#     answered False for the whole siege.  Corpus: **1,251 of 5,150
#     damaged-core rounds (24%) had a free heal seat, >= 1 Ti banked and one of
#     our builders within d^2 <= 25 of the Core, with nobody standing on a
#     seat.**
#
# REFUTED on the way: healing is NOT reserve-gated.  `_heal_core` calls
# `ct.can_heal()` directly and a heal is 1 Ti; `SIEGE_HEAL_RESERVE_TI` gates
# `_eco_spendable` and `_cb_over_heal` only.  The decoded game never held less
# than 2 Ti.  The bank was never the reason we did not heal.
# ============================================================================

# --- 1. ghost magazine ------------------------------------------------------
# The Core cannot see a forward Sentinel (core vision r^2 = 36, the collar is
# at the enemy ring) and `SLOT_FWD_GUN` cannot be trusted, so do not try to
# census the turrets: census the AMMUNITION, which is a global the Core reads
# for free.  A live turret with a target burns 4-10 ammo every 1-3 rounds; a
# magazine that has not fallen in T4_AMMO_IDLE_RNDS rounds is not being fired
# by anything, whatever the comm store believes.  Self-clearing: the counter
# resets on the first shot, so a turret that is merely out of range this minute
# gets its magazine back the moment it engages.
T4_AMMO_IDLE_ON = True
T4_AMMO_IDLE_RNDS = 12      # rounds of a non-falling magazine before the brake
T4_AMMO_IDLE_MIN = 16       # ...and only while at least this much is held
# With the brake on we drop to the UNARMED policy for one round: the floor
# `ammo_target` (AMMO_FLOOR / 24 under attack) and the unarmed `ti_floor`, which
# is where E1_AMMO_FLOOR's harvester reserve lives.
#
# Independent of the brake: never bank more magazine than the guns we think we
# own could burn in T4_BURN_RNDS rounds.  A Sentinel is 10 ammo on a 2-round
# reload (3.3/round) and a Gunner 4 on a 1-round reload; 4 ammo/round/turret is
# the generous side of both.  This is the "cap conversion at ten rounds of
# fire" rule and it binds the fwd-Sentinel floor (60 for one turret) down to 40.
T4_BURN_CAP_ON = True
T4_BURN_RNDS = 10
T4_AMMO_PER_RND = 4

# --- 2. the chase that cannot resolve ---------------------------------------
# Builders cannot attack builders, so while the Core is BLEEDING an intruding
# builder is worth exactly one thing to us: it might be standing on a heal
# seat.  Chasing it is strictly dominated by taking a free seat (+4 HP/round for
# 1 Ti against 0 for 1 move).  Seat first, chase second, and only while the Core
# is provably damaged -- at full HP the chase is still our cheapest disruption
# and this plank leaves it alone.
T4_SEAT_FIRST_ON = True
# Belt and braces for the full-HP case: a chase whose net displacement is zero
# over T4_CHASE_MAX_RNDS rounds is a lockstep, not a pursuit.  Drop intruder
# targeting for T4_CHASE_COOLDOWN rounds and let the rest of `_defend` run.
T4_CHASE_BREAK_ON = True
T4_CHASE_MAX_RNDS = 6
T4_CHASE_COOLDOWN = 20

# --- 3. who may converge, and who can see ------------------------------------
# Seat 1 owns the trunk chain and an earlier revision that recalled the whole
# economy "stalled the chain at r16 and finished with 0 titanium delivered", so
# it is NOT admitted on a scratch: it joins only once the Core has lost
# T4_SEAT1_MIN_DMG, which is four Sentinel shots -- past any opening poke and
# well inside the window where THE LAW (heal/damage >= 0.94 survives, <= 0.86
# dies) is still winnable.
T4_CONVERGE_SEAT1_ON = True
T4_SEAT1_MIN_DMG = 40
# A builder's vision is r^2 = 20, so `_core_shelled` is blind at the range the
# economy actually works at.  The Core publishes its own damage in slot 9 --
# SLOT_HEAL_BUDGET, which loki_analysis.md 1.3 records as written every round
# and read by nobody, i.e. provably dead -- and `_core_shelled` falls back to
# the beacon when the Core is out of vision.  Cheaper than a scan and it costs
# no slot: the K_HEAL_BUDGET write it replaces was dead code.
T4_BLEED_BEACON_ON = True
T4_BLEED_MIN = 8            # damage below which the beacon reads "not shelled"
T4_BEACON_BAND_DSQ = 64     # the beacon only recalls bodies inside eight tiles

# ============================================================================
# LOKI-SAMESTOP (QUEUE #50) -- harvester + first outbound conveyor from ONE
# builder stop. Magnus's kladde observation, corrected by research's own-
# corpus measurement (cite in code as "research #50 cut"): winning eco teams
# place a harvester AND its first outbound conveyor from a SINGLE builder
# stop -- lingling 98% of double-builds are conveyor+harvester kind-pairs,
# kladde 35%, US only 7% -- and their geometry is a STRAIGHT LINE (ore O --
# stand T -- route R, O and R on opposite sides of T, d^2(O,R)=4) where ours
# corner-turns 78% of the time (d^2=2). Delivery is the currency
# (titanium_collected counts DELIVERY to the Core, not emission -- see
# CLAUDE.md), so a harvester whose first link waits an extra round for the
# builder to walk away and back is a round of throughput lost for nothing.
#
# THE MECHANISM, because this does not invent a parallel router (research
# #50 cut, step 3c). _link_path(ct, O) already returns the trunk's planned
# route home as a list of tiles; by construction its first element plan[0]
# is orthogonally adjacent to O, and its second element plan[1] (when
# present) is orthogonally adjacent to plan[0] -- a grid/BFS fact, not new
# code. STOP-TILE PREFERENCE (eco.py _samestop_stand_pref) steers the
# builder to STAND on plan[0] itself instead of an arbitrary neighbour of O;
# SAME-STOP SECOND BUILD (_samestop_arm / _samestop_fire) then places
# plan[1] the very next round, without moving, because it is already
# adjacent to plan[0]. plan[0] itself is left EMPTY at that point (the
# builder is standing on it) -- it becomes a HOLE with a feeder (the
# harvester at O) on one side and an acceptor (the conveyor at plan[1]) on
# the other, exactly _l4_repair's HOLE condition, so the existing L4
# machinery fills it in once this builder steps off. SCALE-NEUTRAL BY
# CONSTRUCTION: this arm never adds, removes or reorders a link in the plan
# it reads -- only WHEN plan[0] and plan[1] go up, and FROM WHERE.
#
# SCOPE: only the FIRST harvester of a builder's wiring job (self.link_queue
# empty at build time) is armed -- a harvester queued behind others via
# SIPHON_WIRE's wire_pending defers its real route to _wire_tick, later and
# on a possibly different snapshot, and arming against an early guess there
# would risk building R against a route _wire_tick later replaces. Out of
# scope by construction, not an oversight.
#
# ⛔ DOES NOT TOUCH PAVE_TRAIL_ON (False above) -- that mechanism is one
# structure per MOVE; this one is per STOP, a different cadence entirely.
# ============================================================================

LOKI_SAMESTOP_ON = True         # the whole plank; False == the parent exactly
# Instrumentation only: one print per same-stop build, into the replay. Local
# instrument only (platform replays strip stdout -- see the Controller API
# note above on print()). Dose tag "SS50".
LOKI_SAMESTOP_LOG = True

# ---- composed by tools/stack.py from: turbo (_x3r0v152), bodyaware (_v242bodyaware), samestop (_v464samestop)
# ---- hand-merged by builder s46 from: turbo (_x3r0v152), bodyaware (_v242bodyaware) — _bfs_direction flat-grid two-pass
# NOT produced by tools/stack.py: the two planks both REWRITE _bfs_direction, so
# stack.py's whole-statement AST merge cannot express this one.  The marker line
# above uses stack.py's literal phrasing on purpose -- tools/dash/serve.py
# (_COMPOSED_FROM_RE) and tools/auto_gate.py (combo_of) both require it verbatim,
# and a hand-merge that reads as a SOLO would be scored against the wrong bar.


# ============================================================================
# LOKI-FERRY-SIEGE (s50, 2026-08-17) -- THE SELF-FERRY SIEGE RAIDER.
#
# One plank, four moves, all of them already measured on the ENGINE
# (docs/research/PROBE-DOSSIER-ferry-siege-2026-08-17.md, probes P1-P5) and
# all of them already observed at 2174 Elo in an opponent's replays
# (REPLAY-STUDY-jython-inspiration / -wider, 2026-08-17):
#
#   1. FERRY.  The raider builds a LAUNCHER on its own forward tile; next
#      round that launcher throws the raider ~5 tiles forward and then calls
#      `self_destruct()` as the last statement of its own run().  Cycle = 2
#      rounds, ~3 tiles/round, 3x walking (P2).  The self-destruct returns the
#      +10% scale contribution the SAME round (P1: treatment held
#      get_launcher_cost() flat at 30 while the persist control climbed
#      30->32->34->36), so the chain costs ~20 Ti/hop and NOTHING in scale.
#   2. SEAL.  Barrier the enemy core's 12-tile adjacency ring.  The 8
#      ORTHOGONAL seats are the only tiles a builder can heal that core from
#      (P3: is_tile_passable/empty/can_move all False on 1,996 of 1,996
#      footprint readings) and the 12 tiles are exactly its legal spawn set
#      (P3: 12 -> 0 legal spawn targets by r37, 0 for the remaining 963
#      rounds).  ⚠ BINARY: a PARTIAL >=10/12 seal INVERTS the heal rate
#      (0.0100 -> 0.0681/round over Jython's 60-game record) -- so we do not
#      place the FIRST barrier until the bank pays for ALL of them.
#   3. EVICT.  One launcher parked ON the ring throws arriving enemy builders
#      away, 0 ammo, +1 cooldown, re-throwable every round (P4: 248 throws;
#      defender-in-envelope 25.1% treatment vs 100.0% control -- the throw
#      removes them 74.9% of the time).  SITING IS THE WHOLE GAME: the same
#      plant on fixed ring indices read 0 evictions in 1,000 rounds, and the
#      `cov` score took it to 248.
#   4. KILL.  An ALIGNED forward SENTINEL.  95.2% of all enemy-core damage
#      across Jython's 60 games; 0/37 core kills without one in range.  A
#      sentinel ray ignores obstacles, so it shoots THROUGH our own collar; a
#      gunner ray does not.  A MIS-aligned sentinel contributes literally
#      zero (Jython g1's (29,24): one shot in 60 rounds while its twin did all
#      504) -- hence can_fire_from() before every build, never after.
#
# WHAT WE ADD THAT THE 2174-RATED IMPLEMENTATION DOES NOT HAVE (its four
# measured defects, each one an edge rather than a guess):
#   * a TEAM FILTER on eviction pickup.  can_launch has no team check;
#     Jython's ring launcher kidnapped its OWN raider 57 times in one game and
#     its ring finished 7/12.  The two games with <=3 own-throws sealed 12/12.
#   * a SMALL-MAP / NO-ROUTE GATE.  On fjordgate (10x10, cores d^2=32) every
#     leg of the plank inverted and they lost a 337-round slugfest.
#   * a RAIDER REPLACEMENT.  One raider, 60/60 games, no replacement ever --
#     the single point of failure.  (Double-sourced: Erebus v143 lost 69
#     rounds of offence to the same defect, AUTOPSY 2026-08-17 Finding 6.)
#   * a DUMP-TILE OWN-CORE GUARD.  Their dump tile maximises range from the
#     LAUNCHER, so on a small map 10 of 13 dumps landed inside d^2<=8 of their
#     OWN core -- they air-dropped the enemy siege team onto their doorstep.
#
# ⛔ BOUNDS.  `is_in_vision()` IS NOT A BOUNDS GUARD (probe surprise 1,
# measured on atoll: is_in_vision(-1,14) == True and the next get_tile_* on it
# raises).  This plank operates at map edges BY DESIGN, so every computed
# position is bounds-checked explicitly before any get_tile_* touches it.
#
# ⛔ NO CODE AFTER self_destruct().  It never returns and raises nothing
# catchable -- the sandbox AST validator rejects `finally:`, `except
# BaseException` and `except SystemExit` at load (probe surprise 2).
#
# ⛔ MODULE STATE IS NOT SHARED BETWEEN UNITS (probe surprise 3): the 16-slot
# store is the only channel and it is buffered one round.  Every slot 0-15 is
# already spoken for in this tree, so the plank SHARES SLOT_RAID_LIVE by
# bitfield -- see SLOT_FS below.
# ============================================================================

LOKI_FERRY_SIEGE_ON = True   # master flag.  False == _v488beltbreak2 exactly.

# ============================================================================
# LOKI-FS-SEAL-ONLY (s50, 2026-08-17) -- Magnus, verbatim: "Try another version
# where the offensive builder ONLY builds barriers around the enemy core."
#
# THE DEFECT THIS SUB-FLAG PROBES.  v510's orthogonal-8 closed 0 of 13 local
# games (best 7/8, glacierkeep + nordkap) while the SAME ONE BODY was also
# buying eviction launchers, siting sentinels, pecking enemy buildings off ring
# tiles and repairing its own collar.  A builder gets ONE action a round and
# acting blocks moving, so every one of those is a round the collar does not
# close.  Under this flag the raider's at-ring action set is exactly one verb:
# BUILD A BARRIER (which subsumes REBUILD -- the census re-reads denial every
# round, so a pecked-open tile simply reappears in `needed`).
#
# WHAT IS *NOT* TOUCHED, and it is deliberate:
#   * THE FERRY CHAIN.  build-launcher / throw / self-destruct is how the body
#     GETS to the ring; it is TRANSPORT, not at-ring building, and it is in
#     Magnus's original spec.
#   * the small-map / no-route gate, raider replacement, the 3-builder opening,
#     bounds hygiene, indicators.
#   * THE CHASSIS.  Core, home turrets, eco, ammunition and the chassis's own
#     forward-sentinel path all run unchanged.  Only the RAIDER's verb list
#     shrinks -- this is not "the bot stops buying turrets", it is "the ONE
#     ferried body stops doing anything but barriers".
#
# ⚠ REGISTERED DEVIATION FROM v510: THE DIAGONALS ARE NO LONGER DEFERRED TO THE
# KILL WINDOW.  v510 held the 4 diagonals back until a live sentinel plus banked
# ammunition existed (FS_DIAG_DEFER), because a full 12-seal PROVOKES -- median
# 9 rounds to being broken against 56 for a >=8 partial (FIELD-SIEGE-RESPONSE-
# 2026-08-17).  Under seal-only there IS no raider-built kill asset to wait for,
# so that gate would defer the diagonals FOREVER and the body would idle on the
# park seat with a full bank.  Instead the diagonals open the moment every
# orthogonal seat except the park seat is denied.  ⛔ THIS IMPORTS THE FULL-12
# PROVOCATION HAZARD and the prereg must price it: the treatment now spends its
# spare actions on the four tiles the field breaks fastest.
# ============================================================================
LOKI_FS_SEAL_ONLY = True    # False reproduces _v510ferrysiege exactly.

# ⭐ THE ONE NON-BARRIER ACTION SEAL-ONLY KEEPS.  Three of midgard's eight
# orthogonal seats carry the DEFENDER'S OWN CONVEYORS before we arrive, so with
# clearing fully off the collar cannot close on that map at any bank.  Clearing
# is therefore a PRECONDITION of sealing, not a rival to it -- but it is capped
# per tile so a defended seat cannot eat the match (v510 spent 30 rounds and
# 60 Ti pecking three conveyors at 2 damage a peck).  A conveyor is 20 HP = ten
# pecks; eight buys most of one and then defers.
FS_CLEAR_MAX_PECKS = 8
# ⭐ Stand-tile blacklist.  `_fs_gun_axis` covered GUNNERS only and v510 lost
# three units on one tile to one turret.  A sentinel ray ignores obstacles, so
# unlike a gunner's it cannot be blocked by our own collar -- avoiding the tile
# is the only answer available.
FS_AVOID_TURRET_AXIS = True

# ============================================================================
# LOKI-FS-RING-LADDER (s50, 2026-08-17) -- Magnus's iteration 3, verbatim:
#
#   "on the sealonly we got to the other side and died instantly, if a sentinel
#    starts shooting the builder we need to move it.  Also priority when it gets
#    to the other side: 1. barriers on empty spots, 2. Launcher to launch away
#    enemy builders from their core, 3. peck conveyors at their core and replace
#    with barriers, 4. sentinels parked just outside the ring of barriers and
#    that shoots the core to kill, preferrably two sentinels."
#
# TWO CHANGES ON TOP OF `_v511sealonly`, and neither of them re-opens v510's
# defect (one body doing five jobs at once).  v511 collapsed the raider's verb
# set to ONE (barrier) and that bought the first closures this line has ever
# had -- 9/30 orthogonal-8 closures against v510's 3/30, 2,069 rounds held at
# full seal against 104.  What it could not do is FINISH: the collar closes and
# then nothing kills the core, and on the maps where the defender's own belt
# squats three of the eight seats it never closes at all.  So the verbs come
# back -- but as a STRICT PRIORITY LADDER with one action per round, not as a
# menu the body picks from.  The ladder is Magnus's, in his order, and its
# discipline is the part that makes it different from v510: a lower rung fires
# only when NO higher rung is currently actionable.
#
#   0. DODGE      -- outranks every rung (change A, below)
#   1. BARRIER    an empty ring seat        (v511, unchanged)
#   2. EVICTOR    one launcher, cov-sited   (v510 subsystem, re-enabled)
#   3. CLEAR      peck an enemy conveyor off a seat, then barrier it
#   4. SENTINEL   two, parked OUTSIDE the ring, aligned on the core
#
# ⭐ A. THE REACTIVE DODGE, AND IT IS A SURVIVAL RULE, NOT AN OPTIMISATION.
# AUTOPSY-v510-demo-midgard-2026-08-17 mistake 2: the raider ran at <=8 HP for
# 222 rounds, then stepped onto (24,25) -- a tile the enemy sentinel at (27,22)
# had fired on at r253, r255, r260 and r264 -- and died there; a SECOND body of
# ours died on the same tile 20 rounds later.  Three units, one tile, one
# turret.  A gunner/sentinel shot is a SINGLE-TILE-WIDE LINE, so ONE
# perpendicular cardinal step breaks it, and the engine's own
# `get_attackable_tiles_from()` says exactly which tiles are on it.
# ⛔ THE TRIGGER IS "TAKING FIRE", NOT "IN DANGER": HP fell since our last turn,
# or a LOCATED enemy turret's line covers the tile we are standing on.  A tile
# is remembered as covered for FS_DODGE_MEMORY rounds after we last saw the
# turret, so a dodge cannot step straight back onto the ray it just left the
# moment the turret leaves vision.
# This COMPOSES with v511's static stand-tile blacklist rather than replacing
# it: the blacklist is a PREFERENCE applied when choosing where to walk (it
# avoids known-shot tiles proactively and can be overridden when a needed tile
# has no off-ray station), the dodge is a REACTION that outranks every action
# the moment we are actually being hit.
LOKI_FS_RING_LADDER = True   # False reproduces _v511sealonly exactly.
FS_DODGE_ON = True           # change A on its own sub-switch, so the
                             # die-in-place pattern can be driven back.
FS_DODGE_MEMORY = 5          # rounds a turret's line stays blacklisted after
                             # the turret was last seen.
# ⛔ DEFAULT **OFF**, AND THE MEASUREMENT IS WHY -- READ IT BEFORE FLIPPING IT.
# The build spec named TWO triggers: "HP dropped since last round, OR a located
# enemy turret's attack line covers its current tile".  The second is Magnus's
# own case ("if a sentinel starts shooting the builder") and it is unambiguously
# good.  The FIRST one cannot do what it is for: if no known ray covers us the
# shooter is unlocated BY CONSTRUCTION, so there is no line to break -- the step
# is a coin flip that costs a round and, when we were standing on a ring tile,
# hands back a heal seat our body was denying.
# POOLED 60-GAME ARMS (2 x 5 maps x 6 reps each, same fixture, same day):
#         raider deaths   ring body-rounds at <=10 HP   wins    kills by r300
#   ON        93                  10.8%                 15/60       8/60
#   OFF       75                   5.9%                 17/60      10/60
# Every column favours OFF and the direction was already visible in all four
# single-30 arms.  The trigger is KEPT as a switch (with its own ring-seat guard
# in `_fs_try_dodge`) because it is in the spec and a different fixture could
# reverse it -- but it ships off.
FS_DODGE_ON_HIT = False

# --- rung 2: the eviction launcher ------------------------------------------
# ⭐ ONE, not two, and it is Ti-gated ABOVE the remaining collar.  v510 ran two
# and the autopsy's honourable mention is why the count is not the lever: 119
# throws, 117 of them the identical 4-tile hop recycling the same two bots, and
# a launcher whose d^2<=2 pickup ring could not reach the tile 51 of 59 heals
# came from.  Siting (`cov` over OBSERVED healer positions) is the whole game,
# and a second launcher bought out of the barrier budget is a seat that does not
# close.  The seal is rung 1 for a reason; the evictor may only spend surplus
# above every barrier still owed.
FS_LADDER_EVICT_MAX = 1

# --- rung 3: clear-then-seal -------------------------------------------------
# ⭐ THE ANSWER TO THE BELT-ON-SEATS MAP, and it is Magnus's: clear and then
# seal, not a map gate.  Midgard puts the defender's own delivery conveyors on
# 3 of the 8 orthogonal seats before we arrive and v511 closed 0 of 6 games
# there.  A conveyor is 20 HP = ten 2-damage pecks.  v511 capped pecks at 8 PER
# TILE FOR THE MATCH, which cannot finish one: the cap is now per VISIT -- the
# budget refills once the raider has been away from that tile for
# FS_CLEAR_REVISIT rounds, so the raider pecks, defers to real work, and RETURNS
# until the seat is clear.  A seat that clears then jumps the build queue for
# FS_CLEAR_HOLD rounds so the barrier lands before the defender rebuilds.
FS_CLEAR_REVISIT = 4        # rounds away from a tile before its budget refills
FS_CLEAR_HOLD = 3           # rounds a just-cleared seat holds queue priority
# ⛔ AND THE REFILL IS COUNTED, OR "RETURN UNTIL CLEARED" IS A TREADMILL WITH
# EXTRA STEPS.  The pre-autopsy seal-only build degenerated into exactly that
# (226 barriers, 221 of them on ONE contested tile, bank stalled, r1000 loss),
# and an uncapped peck budget that refills every four rounds can do the same
# thing with pecks.  Four visits is 32 pecks = 64 damage against a 20 HP
# conveyor -- enough to beat a defender healing it at +4 -- after which the seat
# is scored permanently blocked and the collar finishes without it.
FS_CLEAR_MAX_VISITS = 4

# --- rung 4: the two sentinels ----------------------------------------------
# ⭐ OUTSIDE THE RING, NOT ON IT.  A sentinel ON a ring seat is a barrier that
# costs 10x as much and dies to the same pecking; the ring is the collar's job.
# A sentinel ray IGNORES OBSTACLES, so a turret one tile outside the collar
# shoots the core straight through our own barriers -- that is the whole reason
# the kill asset is a sentinel and not a gunner.
FS_SENTINEL_OFFRING = True
# ⭐ AND THE SECOND ONE STANDS ON A DIFFERENT SIDE.  Not for coverage -- one
# aligned ray is enough -- but for REDUNDANCY: the field kills 52.3% of forward
# sentinels at a median age of 8 rounds, 80% of them to turret fire, and a
# defender that has solved one ray has solved both if they share it.  Jython's
# two-sentinel game killed at r114 against r140-r184 for the one-sentinel ones.
FS_SENTINEL_SIDE_PENALTY = 24     # d^2 units off the standoff score
# ============================================================================

# --- the shared store slot ---------------------------------------------------
# SLOT_RAID_LIVE already carries "some raider was acting at the enemy ring in
# round N" as N+1, read by exactly one function (`_foothold_live`) and written
# by exactly two (`_raid`).  The ferry-siege beat is the SAME fact about the
# SAME kind of body, so it lives in the same low bits and the plank's two extra
# fields sit above them.  With LOKI_FERRY_SIEGE_ON = False not one bit of this
# layout is read or written and the slot is a plain integer again.
SLOT_FS = SLOT_RAID_LIVE
FS_BEAT_MASK = 0x7FF          # bits  0-10: round + 1  (MAX_TURNS=1000 < 2047)
FS_PHASE_SHIFT = 11           # bits 11-13: phase, below
FS_PHASE_MASK = 0x7
FS_RID_SHIFT = 14             # bits 14-29: raider entity id + 1

FS_PH_NONE = 0        # no ferry-siege raider has reported yet
FS_PH_FERRY = 1       # a raider is in transit
FS_PH_RING = 2        # a raider is AT the enemy ring
FS_PH_SEALED = 3      # every orthogonal heal seat is denied
FS_PH_KILL = 4        # an aligned forward sentinel exists
FS_PH_DEGRADE = 7     # the gate refused, or the ferry found no route

# --- B. the small-map / no-route gate ---------------------------------------
# fjordgate is 10x10 with cores at d^2=32 and it is the game Jython LOST: the
# ferry buys no tempo (one throw at r2 puts the raider adjacent), the raider
# dies to an enemy army that is already home, and the barriers are contested
# rather than built once.  jackpot is the other refusal: the probe's ferry
# NEVER arrived there on any hop budget (P2, 8 maps tried).
FS_MIN_CORE_DSQ = 72        # cores closer than this: play the incumbent raid
FS_MIN_MAP_DIM = 12         # ...same if the board's larger side is under this
FS_NOPROG_RNDS = 30         # rounds of zero ferry progress before degrading

# ⛔ THE CLOSURE-BASED MAP SKIP SET (research, s50:
# docs/research/BELT-ON-SEATS-SURVEY-2026-08-17.md, 124,536 core-sides).  These
# are maps where the FIELD's sealers close the ring at or near zero -- lighthouse
# is a HARD ZERO (0 of 347 observed closures) -- so a collar plank spends its
# whole game on a ring that does not close, which is a r1000 stall, which is a
# defeat.  The existing dimension/distance gate does not catch them: they are
# ordinary-sized boards whose TERRAIN is the problem.
# ⭐ MIDGARD IS DELIBERATELY **NOT** HERE.  Field sealers close it 18.4% of the
# time, and v511's 0/6 has P ~ 30% under that rate -- consistent with the field,
# not evidence against the map.  A gate fitted to our own six games would have
# closed the one map Magnus keeps watching.
# THE SIGNATURE is (width, height, the two core anchors sorted) -- no map name
# is available to a bot.  snowflake and archipelago share a signature and are
# both in the set, so the collision is harmless.
FS_MAP_SKIP_ON = True
FS_MAP_SKIP = frozenset((
    (16, 16, (3, 3), (11, 11)),        # lighthouse -- 0/347 field closures
    (24, 24, (4, 4), (18, 18)),        # saga
    (21, 8, (5, 3), (14, 3)),          # moonrise
    (28, 20, (7, 9), (19, 9)),         # heart
    (26, 26, (5, 5), (19, 19)),        # snowflake AND archipelago
))

# --- A. the opening ----------------------------------------------------------
# Jython spawns exactly three at r0/r1/r2 in 60/60 games (median builders by
# r30 = 3, against 5 for its opponents) and the r0 bot is the raider in all of
# them.  Spawning resumes the incumbent curve the moment the raider reaches the
# ring, so the economy that has to buy 280-560 ammunition is not starved.
FS_OPEN_BUILDERS = 3        # r0/r1/r2, then stop
FS_MAX_REPLACE = 2          # raider replacements over the whole match
FS_BEAT_STALE = 12          # rounds without a beat before the raider is dead
FS_PANIC_DMG = 24           # core damage that re-opens spawning regardless

# --- C. the ferry ------------------------------------------------------------
FS_HOP_DSQ = 26             # throw range from the launcher (engine constant)
FS_LAUNCHER_TTL = 4         # rounds a ferry launcher may fail to throw before
                            # it self-destructs anyway (refunds its +10%)
FS_LAUNCHER_TI_FLOOR = 6    # bank left after paying for a ferry launcher
FS_HOP_STEP_ON = True       # on the throw round the raider may still step one
                            # tile forward IF that keeps it inside the
                            # launcher's d^2<=2 pickup envelope -- free tempo,
                            # and the pickup is re-checked by can_launch anyway

# --- D. the ring -------------------------------------------------------------
FS_RING_HOLD_DSQ = 50       # ⛔ ONCE AT THE RING, STAY IN RING MODE.  Measured
                            # on the first integrated midgard run: the raider
                            # walked from (26,25) round the collar to (28,23),
                            # crossed FS_RING_DSQ going OUT, fell back into the
                            # ferry branch and threw ITSELF off the ring it had
                            # just reached.  Arrival is a LATCH, not a test.
FS_RING_DSQ = 8             # dsq_core(raider, enemy) at or under this == AT the
                            # ring.  Also the launcher ROLE GATE: any launcher
                            # of ours this close to their core is EVICTION-ONLY
                            # and never ferries (the probe's integrated run
                            # threw our own sealer -- this exact bug).
FS_EVICT_ON = True
FS_EVICT_TI_FLOOR = 12      # bank left after paying for an eviction launcher
# ⭐ TWO, AND THE SECOND IS WORTH MORE THAN THE FIRST (EVICTION-GEOMETRY-
# siege-ring-2026-08-17, 11,897 siege episodes / 1,116,056 on-core heal events):
# ONE adaptively-sited launcher intercepts 48.4% strict / 58.5% deny-mode and
# tops out there; TWO reach 70.5% / 86.5%.  The second's marginal gain
# (+22 to +38.8pp) EXCEEDS the first's gain over blind siting.  So the second
# is DEFAULT-ON and carries only a Ti-sufficiency condition -- the seal and the
# sentinel are still paid first, because the sentinel is the only thing that
# ever wins.
FS_EVICT_MAX = 2
FS_EVICT_SECTOR_DSQ = 32    # radius in which an enemy builder is a defender
# ⭐ SITING IS REACTIVE, NOT FIXED (same study).  Fixed a-priori best tile =
# 29.0% interception; watching 5 heals in THIS siege = 48.4%.  The pooled
# heal-tile distribution is nearly FLAT (max cell 14.58% vs 12.5% uniform), yet
# per-episode traffic is CONCENTRATED (busiest tile median 55.6%, median 3
# distinct tiles) -- the flatness is a normalisation artefact, which is exactly
# why reactive beats fixed by ~19pp.  And healers CAMP: 88.6% are already
# standing on their heal tile ten rounds before the heal, so there is no
# approach lane to intercept -- an eviction launcher is a remover of SQUATTERS.
FS_HEALER_MIN_OBS = 5       # healer-on-a-seat sightings before we site
FS_RING_SITE_ON = True      # ⭐ DENY MODE, +13-17pp over shell siting: a
                            # launcher ON a ring tile removes that tile from the
                            # heal set AND from the delivery set (1,524,857 of
                            # 1,524,857 deliveries into a footprint originate on
                            # the 8 orthogonals) AND from the spawn set
                            # (59,121/59,121 spawns land on the 12-ring).
FS_DUMP_MIN_OWN_DSQ = 100   # never dump an evictee this close to OUR core
                            # (Jython's §4.2 defect: 10 of 13 dumps at d^2<=8)
# ⭐ THE DUMP RULE IS WORTH MORE THAN THE LAUNCHER COUNT (same study, 12,652
# real displacement events): thrown >5.5 tiles, 33.4% ever return, median walk-
# back 33 rounds; thrown 3.5-5.5 tiles -- which is what "farthest site from the
# LAUNCHER" produces -- 58.7% return, median 11 rounds.  Same launcher, ~3x the
# dwell.  A >=6-tile dump is legal from 54-86% of candidate placements on real
# maps, so this is a preference tier with a fallback, not a hard gate.
FS_DUMP_FAR_DSQ = 36        # 6 tiles, squared

# --- E. the seal -------------------------------------------------------------
# BINARY.  Do not place barrier #1 until the bank pays for the whole ring plus
# the sentinel that has to finish the game.  A >=10/12 seal measured a HIGHER
# defender heal rate than no seal at all.
FS_SEAL_ON = True
FS_SEAL_MARGIN = 6          # slack on top of (remaining barriers + sentinel)
# ⭐ NW FIRST.  The spawn set is EXACTLY the 12-tile ring (59,121/59,121
# spawns, 100.0000%) and it carries a 20.28% NW-corner bias -- 1.7x the next
# tile, 2.4x uniform.  That is the field's own `for d in Direction` iteration
# order showing through, not a threat response ("besieged cores spawn away from
# the attacker" is REFUTED at <=1.5pp per side).  Sealing the north/west seats
# first pre-empts a fifth of their spawns during the seal race.  A PREFERENCE:
# the keep-your-route-open constraint (park seat + BFS around our own barriers)
# still outranks it.
FS_SEAL_NW_FIRST = True
# ⛔ THE COLLAR GETS A CLAIM ON THE BANK, OR THE BINARY GATE NEVER OPENS.
# Measured on the midgard integration run: the raider reached the ring at r13,
# placed ONE barrier, and then sat on a corner for fourteen rounds with the bank
# oscillating between 3 and 45 titanium while the economy spent every arrival --
# the whole remaining collar cost 42 and the bank crossed it twice, briefly, on
# rounds the raider's action was already committed.  A gate that says "wait
# until you can finish" needs someone to stop spending, or it just means never.
# This is the AUTOPSY's lever L3 pointed the other way: there, out-of-band eco
# spending drained the bank while our own core was being shelled; here it drains
# it while our own siege is one barrier from closing.  Reserved only from the
# round the raider is AT the ring, so the opening economy is untouched.
FS_COLLAR_RESERVE_ON = True
# ⛔ AND THE CORE IS THE BIGGEST SPENDER OF ALL.  A body costs floor(scale x 30)
# and our scale runs 2.6-3.5, so ONE spawn is 78-105 titanium -- more than the
# entire collar.  The same run: bank 50 at r15, zero at r16, one builder richer
# and the seal still at 1/8.  The collar reserve therefore binds the spawn gate
# too, from the round the raider is at the ring.
FS_SPAWN_RESERVE_ON = True
# ⛔ AND THE ONE PLACE THE QUIET DOCTRINE MUST NOT REACH.  LOKI_QUIET_ON silences
# every builder melee, which is right for core-pecking (2 damage a round loses
# to one builder healing +4) and wrong for exactly one target: an ENEMY BUILDING
# STANDING ON A RING TILE.  That tile is a permanent hole in the heal set and no
# barrier can ever be placed on it while the building lives, so the collar can
# never close.  A conveyor is 20 HP -- ten pecks -- and killing it also takes
# their delivery, since every delivery into a footprint comes through these same
# eight tiles.  Narrow by construction: the target must be on a tile the seal
# needs.
FS_CLEAR_RING_ON = True
# A CONTESTED TILE IS NOT A REASON TO STOP SEALING THE OTHERS.  Same run: the
# defender pecked our near-face barrier down every ~8 rounds (30 HP / 2 dmg per
# peck) and the NW-first ordering re-selected that one tile every time -- 16 of
# 22 barriers went onto TWO tiles while three seats and two corners were never
# touched at all.  After this many rebuilds a tile keeps its place in `needed`
# but goes to the BACK of it, so the ring finishes and the contested tile is
# retried once there is nothing else to do.
FS_REBUILD_MAX = 3
# ⭐ THE DIAGONALS WAIT (FIELD-SIEGE-RESPONSE-2026-08-17, 16,604 replays / 85
# teams).  The 8 ORTHOGONALS are the entire heal set, so closing them alone
# already satisfies the binary-seal law and zeroes the defender's repair.  The 4
# DIAGONALS buy only SPAWN denial -- and a FULL 12-seal PROVOKES: median 9
# rounds to being broken, against 56 for a >=8 partial (66% of which held to the
# end of the game).  So the orthogonals go up early and the diagonals go up only
# once the kill window is actually open (a live sentinel plus banked ammunition),
# when provoking a break no longer costs us the siege.
# THE ONE EXCEPTION is the NW diagonal at (E.x-1, E.y-1): 19.6% of all spawns
# land on it -- the same `for d in Direction` iteration order that produces the
# 20.28% NW-corner bias -- so it is worth its provocation from the start.
FS_DIAG_DEFER = True
FS_AMMO_KILL_MIN = 120      # ammunition that counts as "the kill window is open"

FS_PARK_ON = True           # park the body on the last orthogonal seat instead
                            # of barriering it: a body denies spawn identically
                            # (P3) and keeps a heal-denied peck station

# --- F. the kill -------------------------------------------------------------
FS_SENTINEL_MAX = 2         # two aligned sentinels double the rate: Jython g5's
                            # second at r96 turned a ~r140 kill into r114
FS_SENTINEL_TI_FLOOR = 4    # bank left after paying for one
# ⭐ SITE BY STANDOFF, NOT BY PROXIMITY (same study).  The forward sentinel is
# the most-punished object in the siege zone: median 8-round life, 52.3% killed,
# **80% of those by TURRET fire**.  HP is not a lever (40 HP against 7 and 18
# damage shots); LOS and DISTANCE are.  So among aligned sites inside d^2<=32 we
# take the FARTHEST, not the nearest, and we penalise any site standing on a
# visible enemy GUNNER's ray -- a gunner shot dies on any interposed body, so
# our own collar shields us from those, while nothing shields against an enemy
# SENTINEL.  ⚠ This REVERSES the "prefer close, their median is d^2=9" reading
# taken from Jython's replays: that number is where their SURVIVING sentinels
# stood, which is a survivorship cut, not a siting rule.
FS_SENTINEL_FAR_FIRST = True
FS_SENTINEL_GUNAXIS_PENALTY = 64   # in d^2 units of the standoff score
# ⛔ THE FIRST SENTINEL DOES NOT WAIT FOR THE SEAL, AND THE FIELD SAYS SO.
# Jython's phase medians over 60 games: r9 first ring build, r28 6/12 ring,
# **r38 first sentinel**, r52 10/12 ring -- the turret goes up with the ring
# barely half built.  The first integrated midgard run gated it on a COMPLETE
# orthogonal seal against a defender who pecked the near face open every eight
# rounds: the seal never closed, the sentinel was never bought, and a plank with
# no damage source is a 1000-round stall, which is a defeat.
# What protects the seal instead is a RESERVE, not an ordering: the first
# sentinel may only be bought out of a bank that still pays for every remaining
# barrier afterwards.  The SECOND one still waits for the orthogonals, because
# by then the reserve argument is spent and the marginal shot is worth less than
# a closed collar.
FS_SENTINEL_EARLY = True
FS_SENTINEL_RND = 30        # ...and if the ring is still open at this round the
                            # sentinel JUMPS THE QUEUE.  A contested near face
                            # can keep `needed` non-empty forever (measured: the
                            # defender pecked one seat open every ~8 rounds), and
                            # "seal first, always" then means "never buy the only
                            # thing that wins".  Jython's median first sentinel is
                            # r38 with the ring at 6/12; 30 is that, minus the
                            # rounds our ferry saves over theirs.
FS_AMMO_TARGET = 300        # 28 shots x 10 is the arithmetic floor for 500 HP;
                            # 300 with a working belt gave the fastest observed
                            # kill (r114), 280 exactly gave the slowest (r184,
                            # cadence degraded to one shot per 4 rounds)
FS_AMMO_CHUNK = 30          # per-round conversion cap while the siege is live
                            # (burn is 5/round per sentinel; stay ahead of it)
FS_AMMO_TI_FLOOR = 8        # bank left after a siege conversion

# --- H. hygiene / instrumentation -------------------------------------------
FS_DRAW_ON = False          # replay indicators: hop paths, seal tiles, the
                            # sentinel site and its ray, eviction throws.
                            # Magnus WATCHES this replay -- it is the demo.
FS_LOG = False              # LOCAL demo instrument, STDERR only.  Never print():
                            # platform replays strip stdout in 30,664 of 30,664
                            # BotOutput events (measured s28), so a plank that
                            # plans to read its own tag out of a live replay is
                            # planning on an instrument that does not exist.
                            # Tags: PHASE / HOPBUILD / THROW / SEAL / SENTINEL /
                            # EVICTOR / EVICT / DEGRADE / STAT.


# ============================================================================
# LOKI-FS-CREW (v513, s50 2026-08-17) -- the siege gets a CREW, the collar gets
# paid for before the magazine, and the home crew stops ignoring the turret
# that is killing us.
#
# THIS BLOCK EXISTS BECAUSE OF ONE DOCUMENT: the 24-game v512 autopsy
# (docs/research/AUTOPSY-v512-three-maps-2026-08-17.md).  Every sub-flag below
# is a numbered defect from its ranked list, in its measured-cost order, and
# each one carries the number that put it there.  `LOKI_FS_CREW = False`
# reproduces `_v488beltbreak2`-vs-`_v512ringladder` byte-for-byte behaviour.
#
#   A  FS_SALT_GATE            Magnus's rule: no sentinel, no magazine, before
#                              the salt is down (autopsy #3: pre-seal fire is
#                              1:1 heal-cancelled, 8 games EXACT to the HP)
#   B  FS_HOME_TURRET_RESPONSE autopsy #1 -- 0 of 40 door sentinels attacked
#   C  FS_BELT_LASTLINK        autopsy #2 -- tic = 0 <=> no core-adjacent link
#   D  FS_CREW_ON              autopsy #6/#9 -- one body, 0.26-0.67 coverage
#   E  FS_CREW_EVICT_NOWAIT    autopsy #8 -- 0 evictions in 19 of 24 games
#   F  FS_MAG_*                autopsy #4 -- 73.9% of live-sentinel rounds
#                              under one shot WITH >=10 Ti in hand
#   G  FS_CREW beats + dodge   autopsy #5 -- 23 deaths, dodge prevented 0
#   H  FS_SPAWN_PURPOSE        Magnus-requested polish (measured worth ~2 rnds)
# ============================================================================

LOKI_FS_CREW = True          # False reproduces _v512ringladder exactly.

# --- A. SENTINEL AFTER SALT (Magnus, direct, binding) ------------------------
# ⭐ THE RULE, VERBATIM IN EFFECT: the rung-4 sentinel purchase AND the Core's
# siege ammunition conversion are both HARD-GATED on the orthogonal-8 seal
# being COMPLETE (every seat denied by our barrier, our body, or our launcher).
# Two reasons on record, one economic and one measured:
#   * the eco builders need the early bank -- harvesters and the conveyor line
#     are what pay for everything later, and a magazine bought at r30 is bought
#     out of the belt;
#   * pre-seal sentinel fire NETS ZERO.  Autopsy #3: 19,152 damage dealt to
#     enemy cores, 16,962 healed straight back (88.6%); in 13 of the 21 games
#     with any damage at all the cancellation is >=99%, and in EIGHT it is
#     exact to the hit point (1,530 dealt / 1,530 healed over 85 shots and 320
#     rounds).  Ammunition spent before the healer is locked out is ammunition
#     spent on nothing.
# ⛔ THE GATE IS ON THE PURCHASE, NOT ON THE TURRET.  Once a sentinel is BUILT
# it stays and keeps firing whatever the collar does afterwards -- a turret
# already paid for is a sunk asset and pulling its magazine would repeat the
# v510 lock we are here to remove.
FS_SALT_GATE = True
# ⭐ AND A GRACE WINDOW, because Magnus asked for TWO sentinels and a sealed
# collar is not a static object: the defender pecks a seat open, our own body
# steps off one to walk, and `orth_open` flickers.  A second purchase that was
# legal the round the collar closed stays legal for this many rounds after it
# re-opens, which is enough for the walk-and-build round pair without letting a
# collar that has genuinely collapsed fund turrets for ever.
FS_SALT_GRACE = 8
# ⛔ THE FLAGGED-OFF FALLBACK, AND IT SHIPS OFF BECAUSE MAGNUS'S RULE SHIPS AS
# STATED.  The stall this exists for is real and was measured on the first
# v513 smoke run (glacierkeep seed 7301): the collar closed at r180 with a bank
# of 44 -- a titanium or two short of a sentinel -- the grace expired, the
# defender re-opened one seat, and at r800 the bot was standing on `orth 1`
# holding 110 titanium and 300 ammunition WITH NO TURRET TO FIRE IT.  Closure
# and affordability are separate events and nothing makes them coincide.
# With FS_SALT_LATCH the gate becomes "the collar HAS BEEN complete", which is
# still Magnus's economic argument (the eco keeps the whole opening) without
# requiring the two events to land in the same eight rounds.  It is a VARIANT
# and it is measured separately; the default is the strict rule.
FS_SALT_LATCH = False

# --- B. THE DOOR-SENTINEL RESPONSE (autopsy #1: the measured killer) ---------
# ⛔⛔ THE NUMBER THAT BUILT THIS FLAG: **100% of the 1,202 damage events on our
# core across 24 games came from enemy turrets planted NEARER OUR CORE THAN
# THEIRS** (d^2 4-37 from us).  Forty such plants.  **Our builders attacked
# ZERO of them** and 38 of 40 survived to the end of the game.  Median warning
# between the plant and our core's death: 56 rounds (min 28) -- a sentinel is
# 40 HP, two builders pecking at 2 damage each kill it in ten rounds, and the
# titanium was in the bank every time.  Our 241 builder attacks that grid went
# to conveyors (185), enemy builders (23) and sentinels on THEIR ring (19).
#
# ⭐ THIS DELIBERATELY PIERCES LOKI_QUIET_ON, FOR EXACTLY ONE TARGET CLASS.
# The quiet doctrine ("no builder melee") was a measured win because pecking a
# 500 HP core at 2 damage a round buys nothing at the price of a step.  A 40 HP
# sentinel is the opposite object: 2 damage a round FINISHES it, which is the
# same property that earned the conveyor-melee carve-out (doctrine.py:1744) and
# FS_CLEAR_RING_ON their exemptions.  The carve-out is the narrowest that can
# work: enemy TURRETS ONLY, inside FS_DOOR_DSQ of OUR OWN core, home crew only
# (the ferried raider never comes home for anything).
FS_HOME_TURRET_RESPONSE = True
FS_DOOR_DSQ = 40            # d^2 from OUR core inside which an enemy turret is
                            # a "door" turret.  The autopsy's plants span 4-37;
                            # 40 covers them with one tile of margin and stops
                            # well short of the midfield.
FS_DOOR_TI_FLOOR = 6        # a peck is 2 Ti; never spend the last of the bank
FS_DOOR_MAX_RNDS = 40       # rounds one body will chase one door turret before
                            # it goes back to the economy (anti-treadmill: the
                            # kill needs ten rounds of pecking, not forty)
FS_DOOR_TYPES = frozenset((EntityType.GUNNER, EntityType.SENTINEL,
                           EntityType.LAUNCHER))

# --- C. THE BELT'S LAST LINK (autopsy #2) ------------------------------------
# PERFECT SEPARATION, 24 of 24 GAMES: `titanium_collected` > 0 if and only if a
# conveyor of ours stands adjacent to our own core footprint (13/13 with, 0/11
# without).  In 8 of the 11 zero games the belt TERMINUS sat at Manhattan 2 --
# ONE 3-titanium link short -- and the stacks jammed at the dead end
# (glacierkeep_g5: 9 stacks in, 0 delivered, 447 rounds).  Not attrition:
# harvesters died at 6% and conveyors at 7% in the same games.
#
# ⛔⛔ THE ROOT CAUSE, AND IT IS NOT WHERE ANYONE LOOKED (s50 diagnostic, 9
# local games).  Not attrition, not role dispatch, not the siting rule: TWO
# TITANIUM RESERVES THAT HAD NEVER BEEN CHECKED AGAINST EACH OTHER.
# `eco.py:_eco_spendable` withholds `8*barrier + FS_SEAL_MARGIN` from the
# economy while the siege is live; `main.py`'s KILL-phase magazine drains the
# bank to `8*barrier`.  The economy's bar sits EXACTLY FS_SEAL_MARGIN = 6
# titanium above the level the Core drains to -- permanently insolvent, and no
# conveyor affordable again for the rest of the match.  2,653 of 2,809 eco-spend
# denials (94.4%) had a raw bank that covered the cost; glacierkeep_g5 printed
# `ti=56 res=62 cost=7` 1,284 times and delivered nothing in 447 rounds, while
# the same fixture with the reserve off built 11 harvesters and 106 links and
# collected 470.  The comments at main.py:571-577 reason at length about "two
# reserves that can meet on the same bank deadlock" and check the Core's floor
# against `_fs_seal_ok` -- they never check it against the ECONOMY's.
# ⭐ AND THE PHASE ARRIVES IN THE OPENING, NOT THE MIDGAME: FS_PH_RING is first
# seen at r6-12 and FS_PH_KILL at r8-14, so every clause in that block is
# commented as if it governs a mid-siege bank and actually governs the belt.
FS_BELT_LASTLINK = True
FS_ECO_LIFELINE = 24        # titanium the economy keeps under ANY siege
                            # reserve: one conveyor plus one harvester's change
FS_ECO_HEADROOM = 8         # ⛔ NO LONGER ADDED TO THE CORE'S FLOOR, and the
                            # reason is the equilibrium the F diagnostic found:
                            # `convert_ammo` is the only consumer of surplus in
                            # the KILL state, so the bank settles at EXACTLY the
                            # floor and any raised floor is a raised bank that
                            # never converts.  The economy is protected from
                            # BELOW instead, by the lifeline above.  Kept as a
                            # named quantity because the invariant it expresses
                            # -- the two reserves must not be able to meet --
                            # is what the deadlock taught, and a future floor
                            # that is not equilibrium-bound should use it.

# --- D. THE SECOND BODY (autopsy #6 and #9) ----------------------------------
# ⛔ THE COVERAGE FINDING IS WHAT PRICES THIS, NOT "more is better".  40.9% of
# the enemy's on-core heals came from seats WE NEVER BARRIERED ONCE and a
# further 37.6% from seats we had not reached yet; seat-heal concentration ran
# 0.26-0.67, i.e. the leak is spread over the ring rather than parked on one
# tile.  The midgard park-seat fix does not transfer to a spread leak: what
# does is COVERAGE AND SPEED, and one body with one action a round has neither
# (the v512 raider logged 9 action-rounds out of 48 alive on nordkap_g1, 14 of
# 129 on glacierkeep_g5).  Two bodies with SPLIT VERB SETS keep the ladder's
# discipline -- the thing that made v511/v512 work -- while doubling the tiles
# under our hands.
#   SEALER  (seat 0): rungs 1 and 3 only.  v511's discipline, untouched.
#   SUPPORT (seat 3): rung 2 (the evictor), the dodge, body-denial of the seat
#                     the sealer is furthest from, and rung 4 AFTER the salt.
# ⛔⛔ SHIPS **OFF**, AND THE MEASUREMENT IS WHY -- READ IT BEFORE FLIPPING IT.
# The coverage argument above is sound and the second body still LOST, on every
# column, on the same fixture as the rest of this build (5 maps x 6 reps x 2
# pooled blocks = 60 games per arm vs `_v488beltbreak2`, local --tle 10, fired
# config, identical seeds):
#       arm            wins        kills   kill<=r300   our core died   tic=0
#   FS_CREW_ON=True   24/60 (40.0%)   20    9 (15.0%)   31 (51.7%)        7
#   FS_CREW_ON=False  32/60 (53.3%)   25   13 (21.7%)   25 (41.7%)        3
# ⭐ AND THE OBVIOUS MECHANISM WAS TESTED AND ACQUITTED.  The first suspicion
# was the support's BODY DENIAL -- a body standing on a ring seat publishes
# FS_PH_SEALED for as long as it stands there, which arms the Core's
# 300-ammunition target on a collar that is not barriered.  Run with
# FS_CREW_DENY_SEAT = False (support never occupies a seat, everything else
# identical, same 60 games): 24/60 wins, 20 kills, 31 core deaths -- INDISTIN-
# GUISHABLE from the full crew.  It is not the denial; it is the second body.
# The likeliest remaining reading is the one this line cannot prove: a fourth
# opening builder and its launcher are bought out of the same bank the collar,
# the belt and the sentinel are bought out of, and the eco column moves with it
# (median titanium collected 370 with the crew, 660 without).
# ⚠ 13.3pp at n=60/arm is INSIDE the 95% interval (half-width ~17.9pp at this
# base rate), so this is a DIRECTION on every column, not a significance claim.
# The code stays, behind the flag, for a fixture that could reverse it.
FS_CREW_ON = False
FS_CREW_SEAT = 3            # the roster seat that becomes the support raider
FS_CREW_OPEN_BUILDERS = 4   # the opening: 2 eco + sealer + support
# ⛔ THE FLAGGED VARIANT, DEFAULT OFF: keep the 3-builder opening and convert
# the seat-3 body to support only once the sealer reports AT THE RING.  Cheaper
# in the opening, slower to cover; shipped off so the default is the one the
# autopsy's coverage number argues for, and measurable against it.
# ⭐ AND THE SUPPORT'S BODY-DENIAL IS ITS OWN SWITCH, because it is the half of
# the support that can hurt: a body standing on a ring seat makes the census
# read `orth_open == 0` for as long as it stands there, which publishes
# FS_PH_SEALED, which arms the Core's 300-ammunition target (change A) on a
# collar that is not actually barriered -- so a transient body-seal can convert
# the barrier budget into ammunition and then walk away.
FS_CREW_DENY_SEAT = True
FS_CREW_CONVERT = False
FS_CREW_CONVERT_RND = 12    # ...and if converting, not before this round

# --- E. THE RUNG-2 SEAL-WAIT EXEMPTION (autopsy #8) --------------------------
# EVICTION FIRED **ZERO TIMES IN 19 OF 24 GAMES**.  Two gates did it: the
# ladder's `_fs_seal_pending` wait (correct for a body that is SEALING -- a
# launcher bought out of the barrier budget is a seat that never closes) and
# the healer-observation minimum.  Neither applies to a body that never places
# a barrier: the support's launcher cannot cost a seat it was never going to
# build.  Per P6 (enemy bodies block barriers, 40/40) eviction is a formal
# PRECONDITION of sealing on body-held seats, so a support that cannot buy a
# launcher makes those seats unsealable BY CONSTRUCTION.
# The support's own gate: the launcher, plus whatever the collar still owes
# MINUS what our income puts back in the bank inside ~8 rounds.
FS_CREW_EVICT_NOWAIT = True
FS_CREW_EVICT_RECOVER = 8   # rounds of income the support may borrow against
FS_CREW_HEALER_MIN_OBS = 3  # the support sites on 3 sightings, not 5: it has
                            # nothing else to spend the round on

# --- F. THE MAGAZINE, FOR THE THIRD TIME -- AND THIS TIME THE BLOCKER --------
# 3,495 of 4,519 live-sentinel rounds under one shot of ammunition; in 3,340
# (73.9%) we were simultaneously holding >=10 unconverted titanium.  Two
# rewrites re-tuned constants and neither read the arithmetic.  Under A the
# collar is CLOSED before a sentinel can exist, so the KILL-phase reserve no
# longer has eight barriers to hold back -- only a repair allowance.
FS_MAG_REPAIR_BARRIERS = 2  # barriers' worth held back at KILL for repairs
FS_MAG_TRACE = False        # stderr MAG lines (local instrument only)

# --- G. REPLACEMENT ON DEDICATED BITS, AND THE DODGE REWORKED ----------------
# ⛔ THE REPLACEMENT DEFECT IS A SHARED-SLOT DEFECT (siege.py:136, v511): the FS
# heartbeat rides SLOT_RAID_LIVE's low bits, which raid.py:174/:191 refresh for
# ANY established body of ours -- so the successor door stays shut exactly when
# another body is at the ring, which is the contested case where a replacement
# is worth most.  Backwards by construction, and unfixable inside that slot
# because turn order is entity-id ascending and the FS raider is the r0 spawn,
# so it can never write last.
#
# ⭐ THE FIX IS A SLOT WITH ROOM, AND WE MEASURED THE ROOM.  ENGINE PROBE,
# s50 2026-08-17 (`scratchpad/v513_build/probe_store`, one local game):
# **A STORE SLOT IS AN UNSIGNED 32-BIT INTEGER.**  `write_store(0, 2**31 | 999)`
# round-trips EXACTLY; `2**40`, `2**62`, `2**63-1` and **-5** all raise
# `OverflowError: out of range integral type conversion attempted` -- so the
# usable range is 0 .. 2**32-1 and A NEGATIVE WRITE RAISES (which, uncaught,
# destroys the unit permanently).  Driven both ways in one run: 2 of 6 values
# accepted, 4 rejected, and the accepted ones read back byte-identical.
# SLOT_RAID_N holds a monotone counter of raider seats issued whose ceiling is
# LOKI_MAX_BUILDERS = 11, i.e. it uses 4 of its 32 bits.  The crew's two
# heartbeats live in the other 24 with ABSOLUTE round numbers (11 bits, and
# MAX_TURNS = 1000 < 2047), so there is no modular-wrap window in which a dead
# body reads as alive -- the failure mode a 6-bit or 8-bit beat would have
# reintroduced.
FS_CREW_SLOT = SLOT_RAID_N
FS_RAIDN_MASK = 0xFF        # bits 0-7:   the incumbent raider-seat counter
FS_CREW_SEAL_SHIFT = 8      # bits 8-18:  SEALER beat, round + 1
FS_CREW_SUPP_SHIFT = 19     # bits 19-29: SUPPORT beat, round + 1
FS_CREW_BEAT_MASK = 0x7FF
FS_CREW_STALE = 6           # rounds without a crew beat before that seat is
                            # scored dead.  The cap Magnus set is ~15 rounds
                            # from death to a body engaging; 6 to notice plus
                            # the spawn and the first hop fits inside it.

# ⛔ THE DODGE PREVENTED NOTHING -- 23 raider deaths, ALL to enemy turrets (20
# sentinel, 3 gunner), 0 saved.  The reactive step is kept (it costs nothing on
# the rounds it does not fire) but the weight moves to the two things the death
# data supports: never STANDING on a known ray in the first place, and getting
# a nearly-dead body out of range instead of letting it finish its lap.
FS_PRESTAND_AVOID = True    # the stand-tile blacklist becomes a VETO, not a
                            # preference, whenever an off-ray station exists
FS_RETREAT_ON = True
FS_RETREAT_HP = 14          # at or under this, ONE step off a covered tile
                            # rather than take the next 18-damage shot.  20 of
                            # the 23 measured deaths sat at exactly 4 HP for
                            # two to four rounds before the fatal shot -- there
                            # was time to move, every time.
# ⛔ THERE IS NO "RETREAT AND HEAL" STATE, AND THE FIRST SMOKE RUN IS WHY.
# Nothing heals a body at the enemy ring, so a retreat that waits for HP walks
# out of FS_RING_HOLD_DSQ, hands the turn to the FERRY branch, gets thrown back
# in, and reads `PHASE 1,2,1,2` for four hundred rounds (glacierkeep seed 7301,
# measured before this was cut).  The rule that ships is ONE step off a COVERED
# tile, taken only while low, and only when a strictly-safer neighbour exists
# inside the ring hold radius.

# --- H. PURPOSEFUL SPAWNS (Magnus, small and cheap) --------------------------
# MEASURED FIRST, then shipped as polish: the raider's spawn seat costs ~1 walk
# tile (the ferry absorbs it) and an eco body's costs +2.43 mean tiles -- NOT
# the +10.5 of the old chassis, so OPENFAST's number does not transfer here.
# Worth ~1-2 rounds; the bar is "does not regress".
FS_SPAWN_PURPOSE = True


# =============================================================================
# LOKI-FS-V514 -- FERRYCREW.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v513siegecrew` (frozen).  LOKI_FS_V514 = False reproduces it
# exactly -- every new branch in main.py / siege.py / eco.py / raid.py is
# guarded by this flag or by one of the four sub-flags below.
#
# WHAT PUT THIS BUILD HERE, in one line per source:
#   * MAGNUS RULING 1 (coordination.md 2026-08-18T04:02:40Z, verbatim intent):
#     "1. build barriers, 2. build launchers to keep healers + enemy builders
#     away from their core, 3. build sentinels and finish the core."
#   * MAGNUS RULING 2 (coordination.md 2026-08-18T04:07:19Z, verbatim):
#     "We can allow the first sentry as soon as 2 harvestors are built and
#     connected, otherwise we cannot sustain them. So prio is build barriers
#     until two harvestors, then get one sentry up. If it is killed make sure
#     to get a sentry up somewhere else outside the line of enemy turrets."
#     ⇒ this SUPERSEDES v513's change A (sentinel-after-salt, strict).  The
#     s50 record of the strict rule -- a sentinel in 8 of 30 games (27%), the
#     FS_SALT_LATCH variant measured at 8/15 against 9/15 -- moves to directive
#     history; the code stays behind FS_SALT_GATE for the flag-off path.
#   * AUTOPSY-evict-v513-fired-2026-08-18.md: eviction fires 0x in 17/30 fired
#     games; the binding gates are the healer-observation minimum (49.2% of
#     blocked rounds) and the collar-first funding floor (47.8%); the seal-wait
#     the v514 spec first blamed is ACQUITTED at 0.5%.  `:1819` counts a
#     re-roled FERRY launcher as the live evictor and suppresses rung 2 in 4 of
#     13 throwing games (all midgard).
#   * AUTOPSY-closure-atoll-midgard-2026-08-18.md: atoll 0/6 and midgard 0/6
#     never close the collar and are the two losing maps; the binding seats are
#     ENEMY BUILDINGS on heal seats (ore at chebyshev d=2/d=3 of their core
#     forces their delivery belt onto the seats), which a launcher cannot
#     throw; a purpose-sited evictor reaches 4 of 8 seats where the actual
#     rung-2 evictors reach 1-2; the ferry's terminal hop lands at dsq_core=13
#     on midgard-B in 5/6 games, costing 64-173 rounds of arrival.
#   * PROBE-REPORT-doubleferry-2026-08-18.md: the relay works (both bodies at
#     the ring with a 1-round gap in 26/30, scale refund engine-confirmed
#     190<->200), and the r197 defect was a LOST UPDATE on a buffered store
#     slot with two writers -- higher entity id wins, silently.
LOKI_FS_V514 = True         # master.  False == `bots/_v513siegecrew`.

# --- A.  THE SENTINEL GATE: 2 HARVESTERS BUILT AND CONNECTED ----------------
FS_V514_ECOGATE = True
# ⛔ "CONNECTED" IS NOT "EXISTS", AND THE PROJECT HAS THE MEASUREMENT THAT
# SAYS SO.  CLAUDE.md, engine-probed: one harvester built at r2, alive all
# game, ~250 stacks' worth emitted, NO conveyor ever built -> titanium_collected
# = 0.  A harvester with no route home is worth zero, forever.  So the gate
# reads a DELIVERY fact, not a build count.
#
# THE DETECTOR, and its failure mode is stated in the build report:
#   conn  := SLOT_HARVESTERS >= FS_SENT_HARV_MIN  AND  a MOUTH exists
#   mouth := a friendly CONVEYOR orthogonally adjacent to our own 2x2 core
#            footprint whose FACING points at a core tile (or a friendly
#            SPLITTER on such a tile -- a splitter rotates its output and one
#            of the three directions is the core).
#   deliv := that mouth has been seen HOLDING a titanium stack at least once
#            (get_stored_resource_id() is not None).  A stack sits on a
#            conveyor for a full round before end-of-round distribution moves
#            it, so a Core that polls every round cannot miss a delivering
#            belt for long.
# `mouth` is v513's own measured predicate for the thing we cannot read
# directly: BUILD REPORT change C, "perfect separation over 24 games --
# titanium_collected > 0 if and only if a conveyor of ours stands beside our
# own core footprint".  `deliv` is the stronger, causal form of the same read.
# ⛔ KNOWN FAILURE MODE (v513 open item 5, NOT fixed here): `_wire_tick`
# overwrites `link_queue` wholesale when a new harvester is built, orphaning a
# dead head -- so two harvesters plus one delivering mouth does NOT prove BOTH
# harvesters are routed.  The gate is therefore "two harvesters exist and the
# belt demonstrably delivers", which is weaker than "two routed harvesters"
# and stronger than "two harvesters exist".  It errs toward opening the gate.
FS_SENT_HARV_MIN = 2        # Magnus's number, verbatim
FS_SENT_DELIV_REQ = True    # require the delivery sighting, not just topology
FS_ECO_SLOT = SLOT_ECO_READY
# ⭐ SLOT 5 WAS DEAD.  `SLOT_ECO_READY` is written by three sites in the parent
# (main.py:345, eco.py:589, eco.py:1765) and READ BY NOBODY -- grepped in the
# frozen tree, 3 writes, 0 reads.  Under LOKI_FS_V514 those three writes are
# suppressed and the slot becomes the CORE'S OWN eco-gate word with EXACTLY ONE
# WRITER, which is the discipline the double-ferry probe's r197 defect bought.
FS_ECO_BIT_CONN = 1 << 0
FS_ECO_BIT_DELIV = 1 << 1
FS_ECO_RND_SHIFT = 2        # bits 2-12: round the gate first latched, + 1
FS_ECO_RND_MASK = 0x7FF
FS_ECO_HARV_SHIFT = 13      # bits 13-17: harvester count at latch (cap 31)
FS_ECO_LOG = False          # stderr ECO514 lines (local instrument only)

# --- B.  RESITE-ON-DEATH ----------------------------------------------------
FS_V514_RESITE = True
# ⭐ A SENTINEL RAY IS PERMANENT INFORMATION (s50 surprise 5): sentinels cannot
# rotate -- only gunners can, for 10 Ti and a cooldown -- and 22 of 23 fatal
# tiles were on a previously-seen ray of the turret that fired.  v513 threw
# that away every FS_DODGE_MEMORY rounds.  Here an enemy SENTINEL ray is
# remembered for the whole match and vetoes a sentinel site; an enemy GUNNER
# line is remembered too but only PENALISED, because it can rotate.
FS_RAY_MEM_HARD = True      # sentinel rays never expire
FS_RAY_GUN_MEM = 60         # rounds a remembered gunner line still scores down
FS_SENT_RAY_PENALTY = 4096  # soft weight before we have lost a sentinel; after
                            # the first loss the sentinel-ray veto is HARD
FS_SENT_DEADSITE_VETO = 2   # d^2 around a tile where a sentinel of ours died:
                            # never rebuild inside it once one has been lost
FS_SENT_BUY_MAX = 4         # total sentinel PURCHASES over the match (bank
                            # guard, read off SLOT_FWD_GUN which is monotone).
                            # NOT 1: Magnus asked for a replacement, and
                            # FS_SENTINEL_MAX still caps the LIVE count at 2.
FS_SENT_REBUY_TI = 24       # extra bank required for a purchase after the
                            # first, so a rebuy cannot eat the collar

# --- C.  LAUNCHER-DENIAL SITING ---------------------------------------------
FS_V514_DENYSITE = True
# ⭐ MAGNUS'S PRIORITY 2, ENCODED AS A SITING OBJECTIVE.  The closure autopsy
# measured the ceiling and the actual: a purpose-sited evictor's d^2<=2 pickup
# envelope can reach 4 of the 8 heal seats (max over legal tiles, identical on
# all five grid maps); the rung-2 evictors we actually build reach 1-2.  The
# seats that matter are the ones a BARRIER CAN NEVER TAKE -- an enemy building
# (their delivery belt) sits on them and `can_build_barrier` refuses forever.
# A healer can STAND on that belt and heal (conveyors are bot-passable, engine
# fact, 33.5% of throws land on them), which is exactly Magnus's sentence.  So:
#   * siting scores UNBARRIERABLE-SEAT COVERAGE ABOVE observed-healer coverage;
#   * a candidate that covers such a seat BYPASSES the healer-observation
#     minimum, which the eviction autopsy measured binding 49.2% of blocked
#     rounds (on drakkarfjord/glacierkeep the raider spends its ENTIRE at-ring
#     life at obs<5 and the evictor is never even priced);
#   * a covered unbarrierable seat counts DENIED in the collar census, so the
#     collar can complete on a belted map -- atoll and midgard closed 0 of 12
#     in the fired v513 arm.  ⛔ ONLY unbarrierable seats: a seat we could
#     barrier is still rung 1's, and counting coverage there would stop us
#     sealing it.
FS_DENY_SEAT_CENSUS = True  # a covered unbarrierable seat counts denied
FS_DENY_OBS_BYPASS = True   # such coverage bypasses FS_HEALER_MIN_OBS
# ⛔ `:1819` -- THE FERRY THAT ATE THE EVICTOR SLOT.  `_fs_live_evictors`
# counts ANY friendly launcher inside FS_RING_DSQ, and a ferry link that
# happens to terminate there counts as the one allowed evictor forever (4 of 13
# throwing games, all midgard).  The discriminator is measured, not tagged:
# in-ring FERRY launchers cover 0 of 8 heal seats in 12 of 12 observed cases
# (they land on the outer diagonal), so a launcher whose own pickup envelope
# covers NO heal seat is not an evictor and does not occupy the slot.
FS_EVICT_ROLED_ONLY = True

# --- D.  THE RELAY FERRY (ported from the s51 double-ferry probe) ------------
FS_V514_RELAY = True
# ⭐ TERMINAL HOP MUST LAND IN THE RING.  Ported first because it is the only
# part of D that is live in the FIRED config (FS_CREW_ON ships False, so there
# is one body and nothing to relay).  Measured: the midgard-B chain terminates
# at dsq_core = 13 in 5 of 6 games, outside FS_RING_DSQ = 8, the walk-in then
# fails and arrival slips to r78/123/187 -- 64 to 173 rounds.
FS_HOP_RING_FIRST = True
# The two-rider relay, Magnus's rule (probe report): "both builders need to be
# launched before the launcher can be destroyed and a new launcher can be
# built."  ONE launcher per hop, two throws on consecutive rounds, teardown by
# self_destruct (after a hop both bodies are five tiles away, so destroy() --
# which needs an orthogonally adjacent allied builder -- is unavailable).
# Inert while FS_CREW_ON is False.
FS_RELAY_ON = True
FS_RELAY_TTL = 3            # rounds a relay link waits for its second rider
FS_MUSTER_DSQ = 4           # body 2 this close to the lead == mustered
FS_MUSTER_WAIT = 8          # ...and the lead goes alone after this many rounds
FS_RELAY_PATIENCE = 6       # rounds body 2 rides with no throw before it gives
                            # up and buys its own chain (the safe degrade)
# ⛔ ONE WRITER PER SLOT.  The probe's r197 root cause: two units writing one
# buffered slot in the same round both read LAST round's word and the higher
# entity id wins silently.  Body 2 publishes into its OWN slot.
# ⚠ DEVIATION FROM THE PROBE, and it is forced by slot arithmetic: the probe
# freed slot 10 by turning the chassis home-ferry OFF.  This build keeps
# LOKI_FERRY_ON as the chassis has it (True), so slot 10 is only free in the
# crew-ON configuration -- where the home ferry is stood down by the derived
# gate below instead of by the flag.  In the FIRED config (crew off) nothing
# changes: FERRY_HOME_ON is True and slot 10 is the chassis's, exactly as in
# v513.
FS_SUPP_SLOT = SLOT_FERRY_ID
FERRY_HOME_ON = LOKI_FERRY_ON and not (LOKI_FS_V514 and FS_V514_RELAY
                                       and LOKI_FS_CREW and FS_CREW_ON)
# ⛔ DO NOT RE-TRY THE LEAD-FOLLOW VARIANT.  The probe measured it NEGATIVE
# (n=6: body 2 occupies the lead's forward build tile, two-throw links 2 -> 0)
# and reverted it -- `scratchpad/s51_doubleferry/VARIANT-lead-follow.patch`.
# The midgard first-envelope residual is KNOWN and stays open.

# --- verification instruments (OFF in every shipped configuration) ----------
FS_PROBE_SENT_SUICIDE = False   # a forward sentinel of ours self-destructs at
                                # FS_PROBE_SENT_RND, to drive change B's
                                # resite path on demand.  Change-B mechanism
                                # arm only.
FS_PROBE_SENT_RND = 1
FS_SENT_GATE_BYPASS = False     # change-A mutant: the CONSUMER ignores the
                                # gate while the CORE keeps publishing it
                                # truthfully, so "sentinels bought before the
                                # condition was met" is countable on the same
                                # instrument in both arms.
# BUILDER DEFAULT, FLAGGED FOR MAGNUS'S VETO (coordination.md 2026-08-18
# T04:07:19Z): the KILL magazine follows the SAME gate as the sentinel it
# feeds.  False keeps v513's salt rule for the AMMUNITION only, leaving the
# turret on Magnus's new gate -- the two are separable and are measured
# separately in the build report.
# ⛔ SET **False** ON EVIDENCE, NOT ON PREFERENCE, AND THE MEASUREMENT IS
# HERE SO MAGNUS CAN OVERRIDE IT WITH THE NUMBER IN FRONT OF HIM.  With the
# magazine coupled to the new gate the plank scored 27/60 wins; with the
# magazine left on v513's salt rule and ONLY the turret moved to Magnus's
# gate it scored 32/60, on the same seeds, everything else identical
# (`onlyA2` vs `onlyA_magoff`, blocks A+B, vs _v488beltbreak2, local --tle 10).
# The measured same-config swing on this fixture is ~4 games in 60, so this is
# a DIRECTION, not a significance claim.  MECHANISM, and it is the one v513's
# change A was built around: FS_PH_KILL drops the Core's titanium floor to two
# barriers' worth, and under ruling 2 that state now begins at r35-50 with the
# collar still open -- so the Core converts the collar's own bank into
# ammunition for a turret whose fire the v512 autopsy measured netting ZERO
# before the heal seats are shut (19,152 dealt, 16,962 healed straight back).
FS_V514_MAGGATE = False

# ⭐ v514: A SIXTH PHASE, AND IT EXISTS TO KEEP TWO FACTS APART THAT v513
# CONFLATED.  FS_PH_KILL means "a sentinel of ours is standing"; under Magnus
# ruling 2 that can now happen with the collar still OPEN, and the Core's
# magazine branches all keyed on FS_PH_KILL as if it implied a closed collar
# (it did in v513, because the salt gate was the only door to a turret).
# Phase 5 = sentinel standing, collar NOT yet closed once.  The salt predicate
# `_fs_salt_ok` reads 3..4 and so is unaffected by construction.
FS_PH_KILL_OPEN = 5

# ⭐⭐ v522: A SEVENTH PHASE, AND IT IS THE LAST FREE CODE IN THE FIELD.
# FS_PHASE_MASK is 3 bits (0-7); 0-5 are taken above and 7 is FS_PH_DEGRADE, so
# 6 is the only value left and this build spends it.
# MEANING: a forward turret of ours is alive AND the collar reads open THIS
# ROUND AND closure is NEAR -- i.e. FS_PH_KILL_OPEN with the extra fact the
# Core cannot see for itself.  It is a strict REFINEMENT of 5, never a new
# state: every round that publishes 6 would have published 5 under the parent.
# ⛔⛔ AND THAT IS WHY THE BLAST RADIUS IS AUDITABLE RATHER THAN ARGUED.  Every
# consumer of this channel in the tree was enumerated (9 sites) and 5 and 6 are
# BEHAVIOURALLY IDENTICAL at all of them in the fired configuration:
#   eco.py:408, main.py:599/615/617/1026, siege.py:4236 are range tests bounded
#     ABOVE by FS_PH_KILL = 4, which both 5 and 6 fail;
#   main.py:860 tests == FS_PH_SEALED, which both fail;
#   main.py:766 tests `not in (SEALED, KILL)`, which both pass;
#   main.py:612 (`RING <= ph <= KILL_OPEN`) and main.py:671 (`ph == KILL_OPEN`)
#     are the only two sites that separate them, and BOTH sit behind
#     FS_V514_MAGGATE, which ships False.  They are extended under the v522
#     guard anyway so an arm that turns MAGGATE on does not read a silent
#     semantic change.
# ⭐ THE ASSERTION, NOT THE ARGUMENT: `FS_V522_PHASE_ONLY` is a shipped mutant
# that publishes 6 and NEVER raises the floor.  If the enumeration above is
# right, that arm is BYTE-IDENTICAL to the parent.  It is measured, not
# asserted -- see the build report's channel-substitution control.
FS_PH_KILL_NEAR = 6


# =============================================================================
# LOKI-FS-V515 -- ECOSALT.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v514ferrycrew` (frozen).  LOKI_FS_V515 = False reproduces it
# exactly -- every new branch in siege.py is guarded by this flag or by one of
# the three sub-flags below, and the one doctrine DEFAULT this build changes is
# re-derived from the same flag at the bottom of this block.
#
# WHAT PUT THIS BUILD HERE -- all three changes are direct consequences of the
# v514 build report (docs/research/BUILD-REPORT-v514ferrycrew-2026-08-18.md):
#   1  FS_V515_DOOR_OFF   report finding 2: the door-turret response is the
#                         gated-map crater (archipelago v513 13/36 -> door-off
#                         26/36, exact recovery) AND costs v514 the siege grid
#                         (36/90 -> 53/90 with door-off, +18.9pp, outside the
#                         14.6pp interval).
#   2  FS_V515_GATE_OR    report finding 1 / surprise 3: the conn2 gate is
#                         satisfied at r7-24 on 4 of 5 maps, so change A as
#                         encoded REMOVES the turret gate rather than re-timing
#                         it (A-only 23/60 vs control 37/60).  The lever named
#                         in the report is "a real bar (harvester min / round
#                         floor / delivery count)" -- this is the round floor,
#                         disjoined with v513's salt rule so the closing maps
#                         keep the v513/parent-door-off purchase timing.
#   3  FS_V515_REACH      report surprise 4: `_fs_try_evict_launcher` scores
#                         only the <=4 tiles orthogonally adjacent to wherever
#                         the raider happens to stand, so NO siting objective
#                         can reach the measured 4-seat coverage ceiling
#                         (parent measured evictors at 1 of 4).  Reach bug, not
#                         preference bug -- the fix is in `_fs_stand_target`.
LOKI_FS_V515 = True         # master.  False == `bots/_v514ferrycrew`.

# --- 1.  THE DOOR-TURRET RESPONSE SHIPS OFF ---------------------------------
# ⭐ A CONFIG DEFAULT CHANGE, NOT A CODE DELETION.  `_door_turret_turn` and
# `_door_turret` are untouched and come back with one flag, because the
# evidence that turned this off is a DOUBLE measurement on ONE chassis pair and
# both halves carry the same fixture caveat: every game in both was played
# against `_v488beltbreak2`, our own bot, so "the field plants door turrets and
# we should ignore them" is NOT what was measured.  What was measured is that
# on this fixture the response costs games in two independent grids.
#   * gated (archipelago, plank never runs), n=36/arm, same seeds, vs
#     `_v468kladturbo`: v513 13/36 -> v513+door-off 26/36 (+36pp, exact
#     recovery of the v512 number, digit for digit).
#   * siege (5 maps x 6 reps x 3 blocks), n=90/arm, paired seeds, vs
#     `_v488beltbreak2`: v514 36/90 -> v514+door-off 53/90 (+18.9pp, outside
#     the 14.6pp half-width).  The PARENT chassis is indifferent there (51->50)
#     -- so the interaction is real and its mechanism is still a guess (report
#     surprise 2: door pecks spend home actions and 2 Ti/peck out of a bank the
#     earlier turret has already tightened).
FS_V515_DOOR_OFF = True

# --- 2.  THE SENTINEL GATE BECOMES A DISJUNCTION ----------------------------
# ⭐ salt-complete  OR  (conn2 AND round >= FS_SENT_RND_FLOOR).
# Neither half is new; what is new is that they are OR-ed and that the eco half
# carries a round floor.  Read the two halves as the two map families the
# parent's two measurements separate:
#   * WHERE THE COLLAR CLOSES (glacierkeep, drakkarfjord, nordkap) the salt
#     disjunct fires first and the purchase timing is v513's -- which is the
#     timing the parent-with-door-off config scored 53/90 with.  The eco
#     disjunct cannot pull it EARLIER than the floor, so the r7-24 opening the
#     report measured is removed on exactly the maps where it was a regression.
#   * WHERE THE COLLAR NEVER CLOSES (atoll, midgard: their ore sits at
#     chebyshev d=2/d=3 of their core, so their delivery belt terminates ON the
#     heal seats and `can_build_barrier` refuses those seats forever --
#     AUTOPSY-closure-atoll-midgard-2026-08-18) the salt disjunct never fires
#     and v513 bought ZERO sentinels in 12 of 12 games.  The eco disjunct is
#     what puts a turret on those maps at all; the floor is what stops it being
#     bought out of the opening belt.
# ⛔ THE FLOOR IS A TIMING BAR, NOT A QUALITY BAR.  It does not make the conn2
# detector any stronger -- the `_wire_tick` orphan defect (v513 open item 5) is
# untouched and the detector still errs toward opening.  It buys the economy
# the opening it was measured to need and nothing else.
FS_V515_GATE_OR = True
# ⛔ 60 IS DERIVED FROM THE PARENT'S OWN MEASUREMENT, NOT PICKED.  The report
# measured the conn2 condition satisfied at r7-24 on 4 of 5 maps and the
# resulting configuration at -14/60 against its control; the parent's own
# median kill round with the door off is 233 and its k<=r300 rate is 27/90, so
# a floor has to sit far enough past the belt-building window to stop the
# opening being converted into a turret and far enough short of the kill window
# to still be a turret in time.  r60 is ~2.5x the latest observed conn2 latch
# and ~1/4 of the door-off median kill.  It is a FIRST SETTING with a mutant
# (FS_SENT_RND_FLOOR = 0 reproduces v514's early buying) and it is not tuned.
FS_SENT_RND_FLOOR = 60
FS_GATE_LOG = False         # stderr GATE515 lines (local instrument only)

# --- 3.  THE EVICTOR'S REACH ------------------------------------------------
# ⛔⛔ THE BUG, VERBATIM FROM THE PARENT REPORT (surprise 4): "the evictor can
# only ever SEE 4 tiles -- `_fs_try_evict_launcher` scores only the tiles
# orthogonally adjacent to wherever the raider stands; no siting objective
# reaches the 4-seat ceiling until `_fs_stand_target` prefers stations whose
# neighbour is the max-coverage tile."  v514 change C added the OBJECTIVE
# (`ucov`, unbarrierable-seat coverage) and the objective is correct; it was
# being maximised over a 4-element candidate set the walker chose for entirely
# unrelated reasons (nearest needed barrier seat).  Measured consequence:
# evictors at ucov 1 in 3 of 9, never 2+, against a ceiling of 4.
# ⭐ THE FIX IS A PREFERENCE TERM IN THE WALKER, NOT A VETO, and the reason is
# the v513 prestand lesson written into `_fs_stand_target` itself: an ABSOLUTE
# veto on stand tiles stalls the collar (change G's blacklist had to fall back
# to the incumbent preference for exactly this reason, and the v510 "contested
# near face keeps `needed` non-empty for ever" failure is the same shape).  So
# the term is ranked BELOW the existing turret-ray avoidance and ABOVE raw
# distance: a station that puts the best evictor tile under our hand wins ties
# and near-ties, and a station that does not is still walked to when it is the
# only thing sealing the collar.
# ⛔ AND IT IS SCORED ONLY WHILE AN EVICTOR IS ACTUALLY WANTED.  If the slot is
# already filled, or there is nothing unbarrierable to cover, the term is
# identically zero and the walker is the parent's byte for byte.
FS_V515_REACH = True
FS_REACH_RECHECK = 8        # rounds between recomputations of the best evictor
                            # tile (a full legal-tile scan of the ring is the
                            # only expensive read this build adds; the seat
                            # occupancy it depends on changes on the scale of
                            # tens of rounds, not every round)
FS_REACH_PATIENCE = 24      # rounds the walker will keep preferring the SAME
                            # reach station with no evictor bought before the
                            # term drops and the parent's nearest-first sweep
                            # resumes.  The one stall this preference can cause
                            # that the parent's key cannot is an unreachable
                            # station; this is its bound.
FS_REACH_LOG = False        # stderr REACH515 lines (local instrument only)

# --- the one DEFAULT this build changes, and WHERE it is evaluated -----------
# ⛔⛔ THIS WAS A DOCTRINE-LEVEL `if LOKI_FS_V515 and FS_V515_DOOR_OFF:
# FS_HOME_TURRET_RESPONSE = False` AND THAT ENCODING IS BROKEN BY THIS REPO'S
# OWN ARM MECHANISM.  `mkarm.sh` APPENDS overrides to the END of doctrine.py,
# so an arm that sets `LOKI_FS_V515 = False` sets it AFTER the `if` has already
# run with the master True -- the code paths turned off and the door stayed
# off, i.e. THE MASTER FLAG DID NOT REPRODUCE THE PARENT.  Caught by the
# flag-off audit (the flag-off arm read 146/270 where an unmodified copy of the
# parent tree read 113/270 on the same seeds), not by inspection.
# ⇒ THE DECISION IS EVALUATED AT THE READ SITE (`main.py:_door_turret_turn`),
# where both flags are read at RUN time and no assignment order can strand it.
# `FS_HOME_TURRET_RESPONSE` keeps the parent's value here so that reading this
# constant anywhere still reports what v513 shipped.
FS_DOOR_RESPONSE_ON = None      # placeholder: see main.py, evaluated per call

# --- verification instruments (OFF in every shipped configuration) ----------
FS_V515_REACH_PROBE = False     # log the best-evictor-tile scan every recheck
                                # even when no evictor is wanted, so the ceiling
                                # is countable in both arms of the reach leg.


# =============================================================================
# LOKI-FS-V516 -- TEARDOWN.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v515ecosalt` (frozen, md5 in
# `scratchpad/s51_v516_build/PARENT_FREEZE.md5`).  LOKI_FS_V516 = False
# reproduces it: every new branch is guarded by this flag AND its own sub-flag,
# and NO doctrine-level derived default reads any of them (v515 finding 3 --
# `mkarm.sh` appends arm overrides AFTER the module body has run, so a
# module-level `if LOKI_FS_V516: X = ...` is evaluated against the WRONG flag
# value in every arm).  Everything conditional is evaluated at the READ SITE.
#
# ROUTING: `docs/research/AUTOPSY-rush-top3-2026-08-18.md` ("Builder routing
# (s51)"), three changes.
#
# ⛔⛔ CHANGE 1'S PREMISE IS REFUTED BY ITS OWN FIXTURE, AND THE FIX IS
# RETARGETED RATHER THAN DROPPED.  The autopsy read "295 launchers stand
# forever after ONE throw ... the both-riders condition never satisfies,
# teardown never fires".  Re-measured on the autopsy's own 30 replays
# (`scratchpad/s51_v516_build/launcher_census.py`, and the HOPBUILD join in the
# build report):
#   * 224 HOPBUILD events, of which **219 tore down inside 20 rounds (median
#     life 1 round)**.  In the FIRED config `relay` is False (it is ANDed with
#     FS_CREW_ON, which is False), so `hold` is False and the launcher
#     self-destructs on the throw round.  THE RELAY TEARDOWN FIRES 219/224.
#   * The standing lattice is 71 launchers with life >= 20, of which only 5
#     sit on a HOPBUILD tile.  **66 of 71 were never built by `_fs_build_ferry`
#     at all** -- 14 are ring EVICTORS (standing is their job) and the rest are
#     the CHASSIS home-launcher path (`main.py`, LOKI-42) rebuilt forward by a
#     roaming builder under the LOKI6_LAUNCHER_RELEASE latch: two games reach
#     16 and 22 live launchers.
#   * And the scale claim does not survive either.  Live-scale decomposition at
#     the round the first forward sentinel is bought (n=24 of 30 games,
#     `scale_decomp.py`): median scale 288% => sentinel price 86 Ti, not 124,
#     and the launcher share of that is a median of **10pp of 188pp of excess
#     (5.3%)**; LIVE BUILDER BOTS are 100pp.  Launchers only dominate at END of
#     game (mean 21.3pp, driven by a 2-game tail at 160 and 220pp).
# ⇒ Change 1 ships as TWO parts: (a) the relay hold generalised off FS_CREW_ON
# (correct semantics, a behavioural no-op in the fired config -- it is what the
# mandate asked for and it is honest that it changes nothing here), and (b) an
# IDLE-FORWARD teardown that reaches the population that is actually standing.
# Part (b) is the one with a measurable target.

LOKI_FS_V516 = True

# --- 1. TEARDOWN -------------------------------------------------------------
FS_V516_TEARDOWN = True

# (a) THE GENERALISED HOLD.  "A relay launcher tears down once ALL its expected
# riders have passed", where expected riders = the live published crew bodies
# (1 in the fired config, 2 with the crew on).  The parent ANDs the hold with
# `relay`, i.e. with FS_CREW_ON, so with one rider the hold is never taken and
# the launcher tears down on the throw -- which is the behaviour we want and
# already have.  What the parent CANNOT do is hold for two riders when the crew
# is on without also holding when it is off; this form is the same predicate
# with the crew term removed, so it is correct in both configurations.
FS_V516_HOLD_GENERAL = True

# (b) THE IDLE-FORWARD TEARDOWN -- the measured defect.
# `_fs_ferry_launcher` returns False before its TTL check for any launcher that
# has never had a rider under its hand (`if not self.fs_ferry_seen: return
# False`), so a hop link whose rider died, AND every forward chassis launcher,
# is unreachable by the ferry TTL and plays the home doctrine for the rest of
# the match.  A launcher of ours that is FORWARD (outside our own core's
# neighbourhood), OUTSIDE the enemy ring (ring launchers are evictors and
# standing is their job -- the mandate's named regression watch), and has
# thrown NOTHING for FS_V516_IDLE_TTL rounds, self-destructs and refunds its
# +10%.
# ⚠ THE THROW CLOCK COUNTS BOTH KINDS OF THROW -- ferry hops and home-doctrine
# EXILES -- so an evictor-by-accident that is doing useful work is never torn
# down.  A launcher that has thrown once and then idled 40 rounds is not doing
# that work any more.
FS_V516_IDLE_ON = True
FS_V516_IDLE_TTL = 40       # rounds since the last throw (or since birth) that
                            # a forward, non-ring launcher may idle.  Sized off
                            # the census: the 66 standing chassis launchers sat
                            # a median 170 rounds doing nothing, and the ferry's
                            # own links live 1 round, so any value in 10..80
                            # separates them.  40 is deliberately generous --
                            # the failure mode of a short value is deleting a
                            # link the round before its rider arrives.
FS_V516_IDLE_OWN_DSQ = 40   # ...and only beyond this d^2 of OUR OWN core, so
                            # the home-defence launcher LOKI-42 buys (and s30
                            # measured removing home defence as a REAL NEGATIVE)
                            # is never in scope.

# (c) FERRY_HOME_ON MOVED TO THE READ SITE.  This is the second live instance
# of the v515 finding-3 hazard: `FERRY_HOME_ON` above is a module-level derived
# default reading FS_CREW_ON, so an arm that appends `FS_CREW_ON = True` gets
# FERRY_HOME_ON = True as well and slot 10 then has TWO writers -- the r197
# lost-update class, empirically confirmed COLLISION:True at the 06:24Z
# pre-flight.  The constant above KEEPS the parent's value so that reading it
# still reports what v515 shipped; `raid.py` calls `_ferry_home_on()` instead.
FS_V516_FERRY_READSITE = True

# --- 2. GLOBALSENT: team-global sentinel liveness ----------------------------
FS_V516_GLOBALSENT = True
# ⛔⛔ THE ENGINE FORBIDS THE MANDATE'S FIRST DESIGN, MEASURED BEFORE BUILDING.
# The spec was "the Core verifies liveness each round via get_hp(id) on the
# published ids -- CHECK on the engine".  Probe
# (`scratchpad/s51_v516_build/probe_gethp/`, one nordkap game, 478 probes with
# a positive control in the same tape):
#     r2   rid 3  dsq 4   invision 1  hp 40   exc ''          <- POSITIVE
#     r3+  rid 3  dsq -1  invision -1 hp None exc POS:GameError|HP:GameError
#   471 of 471 out-of-vision probes raised; 434 PROBEDEAD probes on a destroyed
#   id raised identically.
# ⇒ **`get_hp(id)` AND `get_position(id)` RAISE GameError FOR ANY ENTITY
# OUTSIDE THE CALLER'S VISION, AND THE ERROR IS INDISTINGUISHABLE FROM THE ONE
# A DESTROYED ID GIVES.**  There is no id-based liveness channel in this
# engine.  (This also re-prices every "publish the id and let someone else
# check it" design in the backlog.)
# ⇒ SO THE SENTINEL PUBLISHES ITS OWN LIVENESS.  A turret is a unit: `run()` is
# called for it every round it lives, and it stops the round it dies.  A
# forward siege sentinel writes the current round into a dedicated beat field;
# the Core and the raider read the beat's AGE.
# ⛔ WHY A BEAT AND NOT A COUNT, and it is the one-writer rule, not laziness:
# two sentinels writing the SAME slot in the SAME round is a lost update (the
# probe's r197 class).  A BEAT is collision-safe because both writers write the
# IDENTICAL value, so it does not matter which one lands.  A COUNT is not.
# The beat therefore answers ">= 1 live forward sentinel" exactly and says
# nothing about 2 -- which is all the phase machine and the magazine need, and
# it deliberately cannot inflate the purchase cap (`>= FS_SENTINEL_MAX`, 2).
# ⛔ THE FIELD LIVES IN SLOT_ROLE_N's HIGH BITS.  Slot 0 has exactly one reader
# (`main.py:853`) and one writer (`main.py:855`), both on the builder's
# first-turn role claim, and the value is a small monotone spawn counter.  Bits
# 0-9 keep it (0..1023, against ~10 spawns a game); bits 10-20 carry round+1.
# Both writers preserve the other's field; the only loss is a role claim and a
# sentinel beat in the SAME round, which costs one round of beat (republished
# next round) or one seat number.
SLOT_SENT_BEAT = SLOT_ROLE_N
FS_ROLE_N_MASK = 0x3FF          # bits 0-9: the role counter, unchanged
FS_SENT_BEAT_SHIFT = 10         # bits 10-20: round + 1
FS_SENT_BEAT_MASK = 0x7FF
FS_SENT_BEAT_STALE = 3      # rounds a beat may age before the sentinel counts
                            # as dead.  A sentinel runs EVERY round, and the
                            # store is buffered by exactly one, so a live one is
                            # never older than 1; 3 is two rounds of slack for a
                            # CPU-timeout turn.
FS_SENT_BEAT_DSQ = 40       # a sentinel beats only if it is within this d^2 of
                            # the ENEMY core -- the same "forward" test
                            # `_fs_live_sentinels` uses, so the global count and
                            # the vision count mean the same thing.
FS_GLOBALSENT_LOG = False   # stderr SENTBEAT lines (local instrument only)

# --- 3. SENTREACH: the sentinel-purchase reach -------------------------------
FS_V516_SENTREACH = True
# `_fs_try_sentinel` scores the <=4 tiles orthogonally adjacent to the raider,
# and the raider stands ON the ring, where FS_SENTINEL_OFFRING excludes its own
# neighbours -- 7 of 30 games never buy a forward sentinel with the gate open
# and the bank full (autopsy #2).  Same fix class as v515 change 3, purchase
# side: scan every off-ring tile in sentinel range for a site that is legal and
# `can_fire_from`-valid on a core tile, and make the stations of the best such
# site a WALKER PREFERENCE.
# ⛔ PREFERENCE, NOT VETO, and with an expiry -- for exactly the reasons written
# into `_fs_stand_target` for v513 change G and v515 change 3: an absolute veto
# leaves the body with nowhere to stand, and an unreachable station would be
# re-selected for ever.
# ⛔ LEGALITY IS APPROXIMATE, deliberately: `can_build_sentinel` needs
# orthogonal adjacency to the asking body and is False for every tile this scan
# is about.  `can_fire_from` is position-only by contract and IS used -- it is
# the expensive half and the one that actually decides.
FS_SENT_REACH_RECHECK = 12  # rounds between recomputations (the scan costs
                            # engine calls; a ring does not move)
FS_SENT_REACH_PATIENCE = 24 # rounds the walker keeps preferring the SAME site
                            # with no sentinel bought, then drops the term
FS_SENT_REACH_MAX_TILES = 48    # CPU bound on the scan, nearest-first
FS_SENT_REACH_CPU_US = 6000     # ...and a hard abort if the turn is already
                                # this deep into its 10 ms budget
FS_SENT_REACH_LOG = False   # stderr SREACH516 lines (local instrument only)
FS_TEARDOWN_LOG = False     # stderr IDLETEAR516 lines (local instrument only)


# =============================================================================
# LOKI-FS-V517 -- FIRE DISCIPLINE + THE TWIN.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v516teardown` (frozen, md5 in
# `scratchpad/s51_v517_build/PARENT_FREEZE.md5`).  LOKI_FS_V517 = False
# reproduces it: every new branch is guarded by this flag AND its own sub-flag,
# and NO doctrine-level derived default reads any of them (v515 finding 3 --
# `mkarm.sh` appends arm overrides AFTER the module body has run, so a
# module-level `if LOKI_FS_V517: X = ...` is evaluated against the WRONG flag
# value in every arm).  Everything conditional is evaluated at the READ SITE.
#
# ROUTING: `docs/research/AUTOPSY-rush-top3-2026-08-18.md` (deferred-to-v517
# line: "fire-discipline (hold-until-net-positive), second-sentinel economics")
# plus its DATED CORRECTION, and `BUILD-REPORT-v516teardown-2026-08-18.md`.
#
# ⭐ THE TWO CHANGES ARE ONE MECHANISM: fire discipline FUNDS the twin.
#   * The autopsy measured heal-back at EXACTLY 100.0% in 11 of 12 failed
#     sieges (12,650 dealt / 12,650 healed).  One sentinel's ceiling is 9.0
#     HP/round; measured enemy heal rates run 0.00-9.21.  In that state every
#     10 ammo is spent on nothing, and `HEAL_OUTRUN`'s seven games had FUNDED
#     turrets (0.93-1.00 funded share) netting 0.00 -- v516's GLOBALSENT fix
#     (funding 0.249 -> 0.421) cannot reach them, by construction.
#   * TWO aligned sentinels are 18 HP/round, which is above every heal rate
#     ever measured on this field (max 9.21).  The autopsy priced the second at
#     ~124 Ti against a 15-Ti median bank; the v516 build report RE-priced it
#     at ~86-90 at the live scale of the purchase round.  Ammunition held back
#     during a heal-matched state is the only bank that provably accumulates.
# ⇒ hold the fire that nets zero, spend the saved bank on the twin, then fire
#   both unconditionally.
#
# ⛔ THE CARRIER IS PRESERVED BY AN EXPLICIT EXCEPTION.  The autopsy's won-game
# carrier is "kill BEFORE the healers organise" (9/10 kills faced heal <= 3.48)
# and the failed sieges opened EARLIER (r82 vs r111), i.e. firing early is not
# the carrier and firing into an ORGANISED healer is what feeds it.  So the
# discipline may never touch the fresh-contact window: a verdict does not exist
# until FS_V517_NET_W core shots have been taken, and `v517_shots` is a
# monotone per-body counter that the hold predicate tests directly.  The
# violation counter (`FIREDISC517 ... viol`) must read 0 in every game.

LOKI_FS_V517 = True

# --- 1. FIREDISC: net-damage tracking + hold ---------------------------------
FS_V517_FIREDISC = True
FS_V517_NET_W = 4           # core shots in the assessment window.  A sentinel
                            # reloads in 2, so 4 shots span >= 12 rounds -- long
                            # enough for a heal cycle to answer, short enough
                            # that a defender who stops healing is noticed.
FS_V517_NET_EPS = 2         # HP of NET core damage over the window at or below
                            # which the state is "heal-matched".  The autopsy's
                            # signature is EXACTLY 0 (100.0% heal-back in 11/12);
                            # 2 is one round of slack for a sample taken between
                            # a shot and a heal.
FS_V517_HOLD_TTL = 24       # rounds a hold may last before the window RESETS and
                            # the sentinel re-probes with a fresh W shots.
                            # ⛔ WITHOUT THIS THE HOLD IS ABSORBING: a held
                            # sentinel deals no damage, so the window can never
                            # improve on its own and a defender who dies or
                            # stops healing would never be noticed.  The cost is
                            # W shots per TTL (40 ammo / 24 rounds) against
                            # ~8 shots per 24 rounds unheld -- a ~50% ammo cut in
                            # the held state, not a shutdown.
FS_V517_NET_STALE = 3       # rounds a published verdict / peer beat may age.
                            # Same slack as FS_SENT_BEAT_STALE and for the same
                            # reason (buffered store + one CPU-timeout turn).
FS_V517_FIREDISC_LOG = False    # stderr FIREDISC517 / NETDMG517 lines

# ⛔⛔ THE STORE SLOT IS 32 BITS UNSIGNED -- ENGINE-PROBED BEFORE THE PACKING WAS
# CHOSEN (`scratchpad/s51_v517_build/probe_store/`, one nordkap game, positive
# control 12345 exact in the same tape):
#     wrote 4294967295 (2**32-1)  read 4294967295  match 1
#     wrote 4294967296 .. 2**63   WRITE:OverflowError
#     wrote -1, -2**31, -2**63    WRITE:OverflowError
# ⇒ a slot holds 0 .. 2**32-1 and **`write_store` RAISES OverflowError on any
# negative value or anything past 2**32-1** -- and an escaping exception
# destroys the unit permanently.  Every packed field below is unsigned and the
# composed word is bounded by construction.
#
# THE PACKING OF SLOT_SENT_BEAT (= SLOT_ROLE_N), now full to the bit:
#     bits  0-9   role counter          (v105, unchanged)
#     bits 10-20  beat1 = round+1       (v516 GLOBALSENT, unchanged)
#     bits 21-24  PEER stamp            (v517: ">= 2 forward sentinels alive")
#     bits 25-28  VERDICT stamp         (v517: the net-damage publish clock)
#     bits 29-31  NETCODE               (v517: the bucketed net reading)
# ⛔ THE TWO v517 STAMPS ARE MOD-15, NOT round+1, BECAUSE THE BITS RAN OUT.
# 21 bits are already committed above and 11 remain.  A mod-15 stamp answers
# "how old is this" exactly for ages < 15, which is all a STALE = 3 test needs;
# it is stored as (round % 15) + 1 so that 0 still means "never written".
FS_V517_PEER_SHIFT = 21
FS_V517_VERDICT_SHIFT = 25
FS_V517_STAMP_MASK = 0xF
FS_V517_STAMP_MOD = 15
FS_V517_NETCODE_SHIFT = 29
FS_V517_NETCODE_MASK = 0x7
# NETCODE buckets: 0 = no verdict yet, 1 = HELD (net <= FS_V517_NET_EPS), and
# 2..7 = net damage over the window, log-bucketed.  The value is published so
# the channel can be JOINED TO THE REPLAY's own core-HP deltas rather than
# believed; the consumer on the raid side reads only `== 1`.
FS_V517_CODE_HELD = 1
FS_V517_NET_BUCKETS = (4, 12, 24, 48, 96)   # upper edges for codes 2..6; 7 = more

# --- 2. TWIN: the second forward sentinel ------------------------------------
FS_V517_TWIN = True
# In the HOLD state -- and only there -- the rebuy gates relax.  The
# justification is not "we want a second turret", it is that the bank is
# PROVABLY ACCUMULATING: the magazine is armed (v516 GLOBALSENT keeps it armed
# under a live sentinel) and the only consumer of that ammunition is holding
# its fire, so titanium that would have become spent ammunition is sitting in
# the bank.  Outside the hold state every parent gate is untouched.
FS_V517_TWIN_TI_FLOOR = 0   # replaces FS_SENTINEL_TI_FLOOR (4) while holding
FS_V517_TWIN_REBUY_TI = 0   # replaces FS_SENT_REBUY_TI (24) while holding
FS_V517_TWIN_NEEDED_CAP = 2 # ...and the `len(needed) * barrier_cost` reserve in
                            # `_fs_sentinel_ok` is capped at this many barriers
                            # while holding.  Same argument as v513 change F's
                            # FS_MAG_REPAIR_BARRIERS: a sentinel is only
                            # standing at all once the collar was CLOSED, so
                            # what the collar still owes at that point is a
                            # REPAIR allowance, not a fresh eight-seat ring.
# ⛔ WHAT IS **NOT** RELAXED, deliberately: FS_SENTINEL_MAX (2 live),
# FS_SENT_BUY_MAX (4 purchases/match), the salt / eco gate disjunction, the
# v514 site veto (dead-site + enemy sentinel rays -- "resite off rays", still
# shipping), and the ladder ordering.  The plank buys the SECOND turret sooner;
# it does not buy more of them, and it does not put one back on a ray we have
# already lost one to.
FS_V517_TWIN_LOG = False    # stderr TWIN517 lines (local instrument only)

# (2b) ⛔⛔ THE FUNDING LINK, AND IT IS A MEASURED ADDITION, NOT A DESIGNED ONE.
# The mandate's premise for change 2 is "the savings buy the second sentinel --
# the bank is provably accumulating".  MEASURED ON THE FIRST v517 SMOKE GRID
# (30 games, `scratchpad/s51_v517_build/smokegrid/`), IT IS NOT:
#     TWINGATE517 207..231  atring 1 live 1  ti 16  ammo 0/12/8/4  cost 80
# titanium is PINNED AT 16 for twenty-five consecutive rounds of a live hold,
# while ammunition cycles 12->8->4->0 (other turrets burning it at 4/shot).
# The bank does not accumulate because the Core, with the magazine armed by
# v516 GLOBALSENT, converts every titanium above `ti_floor` into ammunition --
# and `main.py`'s EXISTING second-sentinel hold-back (v513, "Magnus asked for
# TWO sentinels and rung 4 buys the second out of this bank") is gated on
# `ammo >= FS_AMMO_TARGET // 2`, i.e. 150, which a starved magazine never
# reaches.  ⇒ FIRE DISCIPLINE WITHOUT THIS CLAUSE SAVES AMMUNITION AND FUNDS
# NOTHING.
# The clause: while a forward sentinel is HOLDING, the existing hold-back
# engages regardless of the ammunition level.  The precondition it drops
# ("don't starve the magazine") is exactly the one a holding turret cannot
# violate -- it is not spending the magazine.  Everything else about that
# hold-back is untouched, including its own `SLOT_FWD_GUN < FS_SENTINEL_MAX`
# cap, which is what stops it banking for a third turret.
FS_V517_TWINBANK = True
FS_V517_BANK_TTL = 30       # rounds the Core keeps banking after the last
                            # observed hold.  ⛔ A LATCH, NOT A LEVEL TEST: the
                            # HOLD_TTL re-probe clears the verdict for the W
                            # shots it takes to re-measure, and without the
                            # latch the Core would spend the part-built bank
                            # into the magazine on every probe and never reach
                            # the sentinel's price.  30 comfortably spans a
                            # 4-shot probe at reload 2.
FS_V517_BANK_LOG = False    # stderr TWINBANK517 lines (local instrument only)


# =============================================================================
# LOKI-FS-V518 -- FAST SENTINEL.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v517twin` (frozen, md5 in
# `scratchpad/s51_v518_build/PARENT_FREEZE.md5`).  LOKI_FS_V518 = False
# reproduces it: every new branch is guarded by this flag AND its own sub-flag,
# read at the READ SITE.  ⛔ NO DOCTRINE-LEVEL DERIVED DEFAULT MAY READ ANY OF
# THESE FLAGS -- `mkarm.sh` appends arm overrides AFTER the module body has run,
# so a module-level `if LOKI_FS_V518: X = ...` is evaluated against the WRONG
# flag value in every arm (v515 finding 3, re-verified by the v517 AST scan).
#
# ROUTING: the v517 build report's phase budget, which is the only place a
# shipped plank has ever named the binding constraint numerically:
#
#     spawn -> arrive   8 rounds
#     arrive -> SENT   81 rounds   <- IDENTICAL in all three v517 arms
#     sent -> funded    0 rounds   <- closed by v516, nothing left to give
#     funded -> kill   87-101 rounds
#
# 81 rounds is 45% of the whole `KILL_TARGET` budget (median kill <= r180) and
# `PROGRAMME.md`'s phase budget wants the first FUNDED turret at <= r75 against
# a measured median of r88-89.  Kills-by-r200 has read a flat 16-19% in every
# arm this line has ever measured.  This build attacks THAT gap and nothing
# else.

LOKI_FS_V518 = True

# --- 1.  THE ROUND FLOOR IS AN ARM, NOT A GUESS ------------------------------
# ⛔ NO NEW FLAG.  `FS_SENT_RND_FLOOR` (v515, = 60) stays exactly where it is
# and keeps its shipped value in this tree; the three-point dose-response
# {60, 45, 30} is run as three CONCURRENT HEADLINE ARMS that override the
# constant, and the build picks NOTHING.  Writing the sweep as a flag would
# make the report's centrepiece a property of this file rather than of the
# fixture.
#
# WHY A SWEEP IS ADMISSIBLE AT ALL, given that v514's floor-0 mutant bought at
# r7-24 and scored -14/60: the v514 regression was measured against the
# ALWAYS-OPEN eco gate (conn2 alone, satisfied at r7-24 on 4 of 5 maps).  The
# gate this floor sits under today is v515's DISJUNCTION --
#     salt-complete  OR  (conn2 AND round >= FS_SENT_RND_FLOOR)
# -- so lowering the floor can only open the purchase WHERE conn2 ALREADY
# HOLDS, i.e. two connected harvesters with delivery evidence.  That is the
# economy guard Magnus's ruling 2 asked for, and it is the thing v514 did not
# have.  The failure mode to avoid is TURRET-BEFORE-ECONOMY, not turret-early:
# v513's salt path bought at r72-85 and won.
# ⛔ AND THE FLOOR IS NOT KNOWN TO BE THE BINDING TERM.  The decomposition in
# section 2 measures how much of the 81 rounds is gate-wait at all; a floor
# sweep that moves nothing is a real answer and closes the road.

# --- 2.  ARRIVAL-PATH TURRET SITING (`FS_V518_EARLYSITE`) --------------------
# THE KNOWN CONTRIBUTOR, from the rush autopsy (#2) and v516 change 3: the
# raider seals first and only ever considers turret sites that happen to be
# under its own hand.  Two halves, both under this one sub-flag:
#
#   (a) PRIORITY.  Once the gate is open and NO forward sentinel is alive, the
#       first sentinel purchase is attempted BEFORE rung 1 (barrier) instead of
#       at rung 4.  The displacement is bounded by construction: the clause can
#       only fire on a round where the purchase SUCCEEDS (afterwards a sentinel
#       is live and the clause is shut), so it costs AT MOST ONE barrier-round
#       per game.
#       ⛔ AND IT CANNOT STRAND THE COLLAR.  `_fs_sentinel_ok` already reserves
#       `len(needed) * barrier_cost + sentinel_cost` before it returns True, so
#       a purchase taken here is one the collar was already paid for.  What is
#       skipped is the WAIT (`_fs_seal_pending`), not the funding.
#   (b) SITING.  While the same condition holds, v516's sentinel-reach walker
#       term outranks v515's evictor-reach term instead of sitting below it.
#       Both remain PREFERENCES with their existing patience timers; only the
#       tuple order changes, and only while zero forward sentinels are alive.
#
# ⚠⚠ DOCTRINE COLLISION, FLAGGED AND NOT RESOLVED BY THIS BUILD.  Magnus's
# PRIORITY RULING 1 ordered the COLLAR sequence barriers -> launchers ->
# sentinels, and `_fs_ladder_turn`'s docstring calls rung 4 "bottom of the
# ladder BY DESIGN".  Magnus's `KILL_TARGET` ruling (2026-08-18, s51) POST-DATES
# it and puts the first funded turret at <= r75.  Those two cannot both bind on
# the round the gate opens.  This build encodes sentinel-first-once-gate-open,
# reports the cost to the collar, and asks the lane to route the tension --
# it does not claim the ruling was superseded.
FS_V518_EARLYSITE = True
FS_V518_EARLY_MAX_LIVE = 0  # the clause is for the FIRST forward sentinel only.
                            # 0 = only while none is alive.  The twin keeps
                            # rung 4 and the v517 hold gates, untouched.
FS_V518_EARLY_REACH_FIRST = True    # half (b): promote the sentinel-reach
                                    # walker term above the evictor-reach term
                                    # while zero forward sentinels are alive
FS_V518_EARLY_LOG = False   # stderr EARLY518 lines (local instrument only)

# --- 3.  THE TWIN RESERVE (`FS_V518_TWINRES`) -------------------------------
# v517's measured blocker, verbatim from its report: "0 of 80 sentinel
# purchases across the four 30-game mech arms" were made under a hold, and in
# the one reachable window "the bank reads `ti 8..24` against `cost 78..86` for
# the whole 225 rounds".  v517's own `FS_V517_TWINBANK` stops the CORE
# converting the surplus to ammunition and the bank still did not reach the
# price.
#
# ⭐ AND THERE IS AN ARITHMETIC DEFECT IN THAT RESERVE, VISIBLE WITHOUT A GAME:
# `FS_V517_TWINBANK` holds `ti_floor >= sentinel_cost + FS_SENTINEL_TI_FLOOR`
# (= sen + 4), while the PURCHASE that reserve exists to fund demands, under a
# hold, `ti >= min(len(needed), FS_V517_TWIN_NEEDED_CAP) * barrier_cost +
# sentinel_cost + FS_V517_TWIN_TI_FLOOR` (= sen + 2*bar, and bar is 8-9 at the
# live 2.8x scale).  ⇒ THE CORE'S RESERVE EQUILIBRATES THE BANK ~12-14 Ti BELOW
# THE BAR THE PURCHASE WILL TEST.  A reserve set under the purchase price funds
# nothing however long it is held.
# ⭐ AND A SECOND DEFECT, IN THE LIVENESS TERM: `FS_V517_TWINBANK` is gated on
# `read_store(SLOT_FWD_GUN) < FS_SENTINEL_MAX`, and `SLOT_FWD_GUN` is a MONOTONE
# count of sentinels EVER BOUGHT that is never decremented (doctrine says so at
# its own definition).  A team that has bought two and lost one reads 2 and can
# never reserve for the replacement -- which is exactly the state v514 change B
# (resite-on-death) exists to handle.  This reserve reads LIVENESS instead:
# the v516 beat (>= 1 alive) minus the v517 peer stamp (>= 2 alive).
#
# WHAT SHIPS: while the FIREDISC hold verdict is published AND exactly one
# forward sentinel is alive, the Core reserves the PURCHASE'S OWN BAR plus a
# margin from ammunition conversion.  BOUNDED, NOT A FREEZE:
#   * it is a ti_floor on `convert_ammo` only -- no other consumer is touched;
#   * `E1_AMMO_FLOOR` / the harvester reserve and every other floor still apply
#     (this term enters through `max()`, so it can only ever RAISE the floor,
#     never lower somebody else's);
#   * it caps at `sentinel_cost + cap*barrier_cost + margin` -- it does not
#     scale with anything;
#   * it RELEASES on (twin built) OR (hold cleared for FS_V518_RES_TTL rounds).
FS_V518_TWINRES = True
FS_V518_RES_MARGIN = 6      # slack above the purchase bar.  The bar is tested
                            # by the RAIDER on its own turn, after the Core has
                            # already run this round, so the bank has to clear
                            # it with room for one barrier the sealer may place
                            # in between.
FS_V518_RES_TTL = 30        # rounds the reserve survives the last published
                            # hold.  Same value and same reason as
                            # FS_V517_BANK_TTL: the HOLD_TTL re-probe clears the
                            # verdict for the shots it takes to re-measure, and
                            # a reserve that released on every probe would
                            # convert the part-built bank and never arrive.
FS_V518_RES_LOG = False     # stderr TWINRES518 lines (local instrument only)

# --- INSTRUMENTS.  OFF in every shipped configuration ------------------------
# ⛔ THESE ARE MEASUREMENT, NOT BEHAVIOUR.  Every one of them is a `print` to
# stderr inside a flag test that is False in the shipped tree, and none of them
# is read by any decision.
FS_V518_GAPLOG = False      # GAP518: one line per ring round from the raider,
                            # carrying WHY no forward sentinel was bought.  This
                            # is the decomposition of the 81-round gap into
                            # gate-wait / funding-wait / siting-wait /
                            # raider-busy, and it is the BEFORE baseline that
                            # change 2's mutant is read against.
FS_V518_TIWATCH = False     # TIWATCH518: one line per round from the CORE with
                            # (ti, ammo, scale).  ⭐ THE SCALE COLUMN IS THE
                            # ATTRIBUTION: every build adds a KNOWN additive
                            # increment to the one global team scale factor
                            # (barrier/conveyor/splitter +1%, harvester +5%,
                            # launcher +10%, builder bot/gunner/sentinel +20%),
                            # so the round-over-round scale delta says WHAT was
                            # built out of the bank without instrumenting every
                            # build site in three modules.

# --- 2(c).  ⛔⛔ THE BASELINE REFUTES THE MANDATE'S PREMISE FOR CHANGE 2, AND
# --- THEN REFUTES ITS OWN RETARGET.  NOTHING SHIPS HERE; THE NUMBERS DO. ------
# The mandate routed change 2 off the rush autopsy's #2: "the raider seals
# first and only considers turret sites under its own hand late".  The GAP518
# decomposition (30 instrumented games, PARENT behaviour with the instruments
# on; `scratchpad/s51_v518_build/GAPDECOMP_BEFORE.txt`) buckets every round of
# the `arrive -> sent` window by the FIRST reason no forward sentinel was
# bought.  On the 18 games that bought one (2,435 window rounds, median window
# 74.5 rounds):
#
#     NOBODY  50.4%   no raider of ours was taking a ring turn at all
#     GATE    25.7%   neither disjunct of the v515 sentinel gate was open
#     FUND    18.9%   a disjunct WAS open and the money test refused
#     DODGE    3.7%   the round went to the dodge
#     SITE     0.8%   no legal aligned site under the body's hand
#     BUSY1 + BUSYW + BUSY23   0.3%   -- SEVEN ROUNDS IN 2,435
#
# ⇒ **THE COLLAR IS NOT WHAT DELAYS THE TURRET.  Priority contention is 0.3% of
# the gap and siting is 0.8%.  Changes 2(a) and 2(b) as mandated address 1.1% of
# the thing they were built to move.**  They still ship -- bounded, sub-flagged,
# mutant-driven, and a measured null on a 1.1% ceiling closes a road the autopsy
# left open -- but the report must not read as though they were the plank.
#
# ⛔ AND THE OBVIOUS RETARGET WAS BUILT, PRICED AND DROPPED BEFORE IT SHIPPED.
# `FUND` is `_fs_sentinel_ok`'s reserve, `ti >= len(needed)*bar + sen + floor`,
# and v517 already carries the device that would cap it
# (`FS_V517_TWIN_NEEDED_CAP = 2`, for the twin).  Priced against the 1,653 FUND
# rounds in the same tape, replaying the reserve test at each capped value:
#
#     cap 8 (parent)  passes    0 / 1653 FUND rounds   0.0%
#     cap 4                    24 / 1653               1.5%
#     cap 3                    34 / 1653               2.1%
#     cap 2                    56 / 1653               3.4%
#     cap 1                    92 / 1653               5.6%
#     cap 0 (no collar term)  169 / 1653              10.2%
#
# ⇒ **EVEN DELETING THE COLLAR RESERVE ENTIRELY RECOVERS 10.2% OF `FUND`, i.e.
# 1.9% of the gap.**  Median bank across FUND rounds is 41 Ti against a median
# sentinel price of 79: the blocker is that WE DO NOT HAVE THE TURRET\'S PRICE,
# not that the collar is holding it.  A cap flag was written into this file and
# removed again rather than shipped, because a plank measured at 0.4% of its
# target before it runs is a plank that spends an arm to confirm arithmetic.
#
# ⭐ WHAT THIS LEAVES, and it is why change 1 is the centrepiece and not a
# garnish: `GATE` (25.7%) is the largest ADDRESSABLE term and
# `FS_SENT_RND_FLOOR` is the only constant in it that has never been swept.
# `NOBODY` (50.4%) is bigger still and is v517 open item 1 -- the raider's
# life -- which no purchase-side change in this family can reach.


# =============================================================================
# LOKI-FS-V519 -- THE CRIPPLE PAIR.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v518fastsent` (frozen, md5 in
# `scratchpad/s51_v519_build/PARENT_FREEZE.md5`).  LOKI_FS_V519 = False
# reproduces it: every new branch is guarded by this flag AND its own sub-flag,
# read at the READ SITE.  ⛔ NO DOCTRINE-LEVEL DERIVED DEFAULT MAY READ ANY OF
# THESE FLAGS -- `mkarm.sh` appends arm overrides AFTER the module body has run,
# so a module-level `if LOKI_FS_V519: X = ...` is evaluated against the WRONG
# flag value in every arm (v515 finding 3; re-verified by the v518 and v519 AST
# scans, which must both read `v519 derived defaults: 0`).
#
# ROUTING -- and it is the first build in this line routed off a MEASURED
# binding constraint rather than a suspected one.  v518's phase budget, n=450
# per arm, four arms:
#
#     spawn -> arrive    8 rounds  (all arms)
#     arrive -> sent    82 -> 64   MOVED, by 18 rounds, by the floor sweep
#     sent -> funded     0 rounds  (closed by v516)
#     funded -> kill    97 -> 112  GREW, and ate the whole gain
#
# ⇒ the kill clock is not turret timing, funding or siting.  It is
# `funded -> kill`, and the rush autopsy prices that exchange: HEAL IS
# 4 HP/Ti FOR THEM, SENTINEL DAMAGE IS 1.8 dmg/Ti FOR US -- better than 2:1
# against us at equal income, with heal-back measured at EXACTLY 100.0% of
# everything we landed in 11 of 12 failed sieges.  Out-DPSing an organised
# healer is economically losing.  The autopsy names three shapes that beat it
# and only one has never been built: CUT THE INCOME THAT PAYS FOR THE HEALS.
# Both changes here are that one shape.

LOKI_FS_V519 = True

# --- 1.  GUNNER-FIRST / PLANT-ON-THE-WAY (`FS_V519_GUNFIRST`) ----------------
# MAGNUS, s51 ~05:07Z, verbatim intent: "maybe there's some scenario where we
# can cripple them hard by an early gunner ... while the offensive builders go
# and set up barriers around their core after the gunner is placed."
#
# THE MECHANISM ALREADY EXISTS AND IS STARVED, NOT MISSING.  `LOKI_BELTBREAK_ON`
# is True in this tree, the plant gate opens at `LOKI_BELTBREAK_RND = 10`, and
# `_try_beltbreak_gunner` (raid.py) carries the whole siting ladder: the d^2
# 20-100 annulus on the BUILD TILE, the live-target gate (`can_fire_from` plus
# an explicit friendly-ray walk), the harvester-over-belt value ladder, the live
# census cap.  ⛔ NONE OF IT IS REACHABLE FROM THE SIEGE PATH: step 3b lives in
# `_raid_act`, and a ferry-siege body never runs `_raid` at all until the plank
# DEGRADES.  Measured consequence (s51 beltbreak-timing census, 30 fired
# replays): gunners appear in 25/30 games but the FIRST PLANT lands at r36-75 on
# siege maps against a gate that opened at r10, while nordkap -- where the ferry
# route happens to loiter -- coexists at r11-17.
#
# THE CHANGE IS **WHEN AND WHO, NEVER WHAT**.  The ferry chain crosses the
# annulus at ~r5-9 on its way to the ring.  This clause lets a ferrying body
# spend ONE action on `_try_beltbreak_gunner` while it is standing there, then
# continue.  The siting ladder, the target ladder, the funding waiver and every
# refusal counter are the SAME CODE, called from a second place.  A fork would
# have been a second plank to verify; this is one call site.
#
# ⛔ COST, STATED HONESTLY: a builder that acts cannot move in the same round
# (engine rule), so a plant taken while no ferry launcher is beside us costs the
# chain exactly one hop.  A plant taken while a launcher IS beside us costs
# NOTHING -- the launcher acts later in the round (turn order is entity-id
# ascending and it is younger) and throws us anyway; only `_fs_hop_step`'s free
# tile of progress is skipped.
FS_V519_GUNFIRST = True
FS_V519_GF_MIN_RND = 3      # ⭐ THE ROUND FLOOR FOR A FERRY PLANT, and it is a
                            # v519 constant rather than LOKI_BELTBREAK_RND
                            # because the BEFORE tape says the two do not
                            # overlap.  `GFBUDGET.txt`, 10 instrumented games,
                            # every ferry round r0-r40 with the body's d^2 to
                            # the enemy core: THE CHAIN CROSSES THE ANNULUS AT
                            # r1-r10 AND THE GATE OPENS AT r10, so on atoll
                            # (in band r3-r4), glacierkeep (r5-r6) and nordkap
                            # (r1-r2) the body is already at the ring before a
                            # plant is legal.  Only drakkarfjord (r9-r10) and
                            # midgard (r9-r10) reach the gate in band.  Moving
                            # the round IS the "when" this change is scoped to;
                            # `_try_beltbreak_gunner` takes it as `rnd_floor`
                            # and changes nothing else.  Swept as a mechanism
                            # arm at {3, 10}.
FS_V519_GF_MAX_RND = 40     # "on the way" is a bounded clause.  Past this round
                            # the ferry body is no longer crossing the annulus
                            # on its way in -- it is either at the ring or lost,
                            # and a late ferry plant would be the r36-75
                            # behaviour this change exists to replace, not fix.
FS_V519_GF_MAX_PLANTS = 1   # per BODY, per match.  The live census in
                            # `_live_beltbreak_guns` already caps the TEAM at
                            # LOKI_BELTBREAK_CAP=2; this stops one ferry body
                            # from spending hop after hop on replants and never
                            # arriving.
FS_V519_GF_TI_FLOOR = 75    # ⭐ THE BUDGET GUARD, and its value is MEASURED,
                            # not chosen: `scratchpad/s51_v519_build/GFBUDGET.txt`
                            # is a 10-game instrumented tape (GUNFIRST off,
                            # GF519 log on) of every ferry round r0-r40 -- the
                            # bank, the launcher price and the barrier price the
                            # ferry and the first collar actually need.  The
                            # floor is what must remain AFTER the gunner is
                            # paid: ONE MORE FERRY LINK (median launcher price
                            # on the crossing 34-38 Ti) PLUS THE FIRST COLLAR
                            # (8 heal seats x a barrier at 5-6 Ti = 40-48), i.e.
                            # 75.  ⚠ Measured NON-BINDING on the crossing: the
                            # bank at every in-band ferry round of the BEFORE
                            # tape is 101-339 Ti against a gunner at 32-40, so
                            # this guard is a rail and not a dose.  It is driven
                            # to the other verdict by a mutant arm (floor 400)
                            # rather than asserted.
FS_V519_GF_LOG = False      # GF519: one stderr line per ferry round with the
                            # bank, the prices and the band test.  This is the
                            # BEFORE instrument -- it is independent of
                            # FS_V519_GUNFIRST so the same tape can be taken
                            # with the behaviour off.

# --- 2.  MODESWITCH (`FS_V519_MODESWITCH`) -----------------------------------
# MAGNUS, s51 ~05:01Z: "either early sentries for a quick core rush or gunners
# to cripple their economy ... This sounds like different variants we should
# test."
#
# On a REGISTERED list of boards the siege plank stands down entirely and the
# chassis plays its own beltbreak+home game -- exactly the state `FS_MAP_SKIP`
# already produces on a GATED board, reached through the same predicate, so no
# new stand-down path exists to verify.
#
# ⭐ THE LIST IS DERIVED, NOT PICKED (`docs/research/MAPSEG-gunner-vs-rush-2026-08-18.md`,
# banked s51 from the BELTBREAK2 n=5400 and SIEGECREW n=1257 tapes, within-tape
# overperformance vs each tape's own pooled mean so the two controls never meet):
#
#     map        gunner-mode dpp (+/-5.16)   rush-mode dpp (+/-10.7)   quadrant
#     midgard         +20.24                    -29.24                 GUNNER
#     yulerune         +7.46                    -36.07                 GUNNER
#     glacierkeep     -28.65                    +38.61                 RUSH
#     ragnarok         -8.93                    +11.23                 RUSH
#
# ⛔ THE ADMISSION RULE, and it is what keeps this from being a fit: a cell
# enters only if it clears its tape's pooled mean by MORE THAN ONE HALF-WIDTH ON
# BOTH AXES.  {midgard, yulerune} clear by >2 half-widths on both.  Everything
# else -- including the rush-good cells, which are already rush -- stays where it
# is.  ⛔ ORE DISTANCE WAS TESTED AS THE SELECTOR AND REFUTED: all three
# gunner-good maps sit at ore-chebyshev 3 and so do three NEUTRALs, so dist=3 is
# a contested bucket and not a discriminator.  The selector keys on MEASURED
# CELLS.
#
# THE SIGNATURE is the one `FS_MAP_SKIP` uses -- (width, height, the two core
# anchors sorted) -- because no map name reaches a bot.  Read off the engine
# with FS_LOG on, one game each, 2026-08-18 (`FS GATE ... sig ...`).
FS_V519_MODESWITCH = True
FS_V519_CRIPPLE_MAPS = frozenset((
    (30, 30, (2, 2), (26, 26)),        # midgard   -- gunner +20.24 / rush -29.24
    (20, 20, (2, 9), (16, 9)),         # yulerune  -- gunner  +7.46 / rush -36.07
))
FS_V519_MODE_LOG = False    # MODE519: one stderr line the first time the mode
                            # selector refuses a board (per unit).


# =============================================================================
# LOKI-FS-V520 -- THE PINCER.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v519cripple` (frozen, md5 in
# scratchpad/s51_v520_build/PARENT_FREEZE.md5).  `LOKI_FS_V520 = False`
# reproduces it -- every new branch in main.py / siege.py / raid.py is guarded
# by this flag AND by one of the three sub-flags below, read at RUN time.
# `eco.py` is untouched.
#
# WHAT PUT THIS BUILD HERE, one line per source:
#   * MAGNUS, 2026-08-18 ~09:2xZ (coordination.md:71531), verbatim intent:
#     TWO RAIDERS, "one to the BACK one to the FRONT of the enemy core, so
#     they can barrier from different sides".
#   * MAGNUS, mid-build refinement: the TERMINAL launcher's tile is a CHOSEN
#     site, not wherever the hop lattice lands -- (a) both split arcs inside
#     its d^2<=26 throw envelope, (b) its d^2<=2 pickup envelope covering the
#     most heal seats; (a) wins on conflict; after both throws it re-roles
#     EVICTOR and is exempt from teardown.
#   * AUTOPSY-closure-atoll-midgard: 85.5% of open-seat rounds are paid to
#     SERIAL sealing -- one body walking a closed curve, one action a round.
#   * BUILD-REPORT-v518fastsent: the turret-gap window is 50.4% NOBODY, i.e.
#     raider ABSENCE, not raider idleness.
#   * BUILD-REPORT-v513siegecrew: replacement latency median 90 rounds,
#     0 of 14 inside Magnus's ~15-round cap; the report names FUNDING the
#     replacement body as the binding constraint.
#   * PROBE-REPORT-doubleferry: ONE chain, two riders, gap exactly 1 in 26 of
#     30 games; the r197 defect was a LOST UPDATE on a buffered slot with two
#     writers -- higher entity id wins, silently.
#   * BUILD-REPORT-v519cripple open item 0: the beltbreak annulus floor
#     d^2 20 -> 8 is PRICED at 8 plants in 8 of 30 games (probe arm `pBAND`).
#
# ⛔ THE ECONOMICS GUARD, WRITTEN DOWN BEFORE THE MEASUREMENT.  Every crew-ON
# form this line has measured LOST: FS_CREW_ON=True 24/60 vs 32/60 (-13.3pp,
# v513), and the crewconv screen repeated it.  The pincer's case is NOT "more
# bodies is better" -- it is that the configuration never measured is
# fund-AND-fast: two riders on ONE chain (gap 1, not a second chain), arriving
# together, with a PAYING JOB each (opposite arcs) and a funded replacement.
# If the composite reads negative the build report carries the single-flag
# isolation, not an excuse.
LOKI_FS_V520 = True         # master.  False == `bots/_v519cripple`.

# --- 1.  THE PINCER (`FS_V520_PINCER`) ---------------------------------------
FS_V520_PINCER = True
# ⛔ THE CREW COMES ON AT THE READ SITE, NEVER AS A MODULE-LEVEL REASSIGNMENT.
# `FS_CREW_ON` keeps the parent's False so that (i) `LOKI_FS_V520 = False`
# reproduces the parent with no second edit, and (ii) the v515 finding-3
# derived-default hazard cannot recur: `FERRY_HOME_ON` at :3011 is a
# module-level assignment reading FS_CREW_ON, and `mkarm.sh` APPENDS overrides,
# so a flag flipped after import would leave that derivation stale (the
# COLLISION:True pre-flight of 06:24Z).  `fs_crew_on()` below is the only
# authority and it is evaluated at run time by every reader, `_ferry_home_on()`
# included.
FS_V520_CREW = True
# THE TERMINAL SPLIT.  The last launcher throws rider 1 and rider 2 to
# OPPOSITE ARCS of the enemy core.  Arc is defined against OUR OWN core:
# FRONT = the half of the ring facing us (the side the chain arrives on),
# BACK = the half beyond the core.  Rider 1 (the lead, which buys the links)
# takes the BACK arc because it is the one that needs the throw -- the far
# seats are 4-6 tiles across a 5.1-tile envelope -- and rider 2 takes the
# FRONT arc, which is reachable from any terminal tile by construction.
FS_V520_SPLIT = True
FS_V520_SPLIT_MAX_RND = 60  # a split throw is an ARRIVAL clause, not a
                            # mid-game verb.  Past this the ordinary ring-first
                            # key is used (the parent's behaviour).
FS_V520_SPLIT_WALK = True   # where the far arc is OUTSIDE the d^2<=26 envelope,
                            # land the rider on the legal site closest to
                            # opposite and let it walk the remainder.  The walk
                            # is measured (WALK520), never assumed to be zero.
# THE TERMINAL LAUNCHER'S SITE (Magnus's refinement).  Scored on the <=4
# cardinal tiles a ferry body may build on, in this priority order:
#   (a) ARCS REACHABLE -- how many of {front seat, back seat} sit inside the
#       candidate's d^2<=26 throw envelope.  Delivery before eviction: (a)
#       wins every conflict, and the conflict rate is reported per map.
#   (b) SEAT COVERAGE -- heal seats inside the candidate's d^2<=2 PICKUP
#       envelope.  The accidental placements measured 0 of 8 in 12 of 12
#       (closure autopsy 5); a purpose-sited tile reaches up to 4, and the
#       midgard counterfactual covered 279 of 280 body-on-seat rounds.
#   (c) the parent's key -- distance to the ferry target.
FS_V520_TERMSITE = True
FS_V520_TERM_DSQ = 60       # the body must be this close (d^2 to their core)
                            # before the terminal scoring engages.  Beyond it a
                            # hop is an ordinary link and the parent's siting
                            # stands -- scoring every link for seat coverage
                            # would site the whole chain for a job only its last
                            # member can do.
# ⭐ THE IN-RING FERRY EXEMPTION, AND IT IS NARROW BY CONSTRUCTION.  A launcher
# inside FS_RING_DSQ is EVICTION-ONLY forever (`_fs_launcher_turn`) -- the rule
# exists because the probe's ring launcher threw our own SEALER off the ring.
# A terminal launcher sited for seat coverage is inside the ring by arithmetic
# (a seat is at dsq_core 1, so a tile within d^2<=2 of one is at dsq_core <= 5),
# so without an exemption it could never make the split throw it was sited for.
# THE EXEMPTION THEREFORE ONLY COVERS A RIDER THAT IS STILL OUTSIDE THE RING:
# a body already at the ring can never be picked up by this branch, which is
# exactly the failure the role-by-site rule was written against.
FS_V520_INRING_FERRY = True
FS_V520_TERM_NOTEAR = True  # a launcher covering a heal seat never self-
                            # destructs: standing IS its job once the riders are
                            # down (it is the evictor, and its coverage counts
                            # as denial in `_fs_census`).
# THE ARC CHANNEL.  Published into the body's OWN slot -- one writer each, the
# r197 discipline -- in two bits above the rid field.  A body derives its own
# arc from where it LANDS (engine-side truth, no comms needed) and publishes it;
# the peer reads it and, on a collision, the HIGHER `fs_body` yields.  The
# collision is COUNTED and is an alarm: two bodies claiming one arc must be 0.
FS_V520_ARC_PUBLISH = True
FS_V520_ARC_SHIFT = 30      # ⛔ BITS 30-31, AND THE ARITHMETIC IS WHY.  The
                            # publish word is beat 0-10, phase 11-13, rid 14-29
                            # (`FS_RID_SHIFT`), so bits 28-29 -- the obvious
                            # place -- are INSIDE the rid field.  A store slot
                            # is an unsigned 32-bit integer (engine probe, s50:
                            # `2**31 | 999` round-trips, `-5` and `2**40` raise
                            # OverflowError, which uncaught destroys the unit),
                            # so 30-31 exist and `(3 << 30) | rest` is at most
                            # 2**32-1.  `_fs_state_at` masks the rid read to 16
                            # bits so these two bits cannot leak into an entity
                            # id -- inert under flag-off, since the rid is
                            # already written `& 0xFFFF` and nothing else writes
                            # above bit 29.
FS_RID_FIELD_MASK = 0xFFFF  # the rid field's own width (bits 14-29)
FS_V520_ARC_MASK = 0x3
FS_V520_ARC_NONE = 0
FS_V520_ARC_FRONT = 1
FS_V520_ARC_BACK = 2
FS_V520_ARC_SEAL = True     # each body seals its OWN arc first.  ⛔ FIRST, not
                            # ONLY: when a body's own arc has no actionable seat
                            # left it takes the other arc's, so no seat is ever
                            # orphaned by the split.
# ⛔ THE DUAL-APPOINTMENT RACE (the crewconv flag: two units both holding
# fs_body == 2).  Two doors can issue the SUPPORT seat -- the opening's
# FS_CREW_SEAT and the "support is stale" replacement door -- and nothing made
# them exclusive, so both bodies publish into FS_SUPP_SLOT and the buffered
# store silently keeps the higher entity id.  That is the r197 class again, one
# level up.  THE FIX IS A CLAIM-AND-READBACK, not a wider comment: a body may
# only take the support seat if the slot is FREE (never reported, or stale by
# FS_CREW_STALE); having claimed it, it verifies on its next turn that the rid
# in the slot is its own, and stands down to the ordinary raid doctrine if it
# is not.  Idempotent, slot-guarded, and it produces a COUNTER rather than a
# silent winner.
FS_V520_APPT_GUARD = True
FS_V520_APPT_LOG = False    # APPT520 stderr lines: CLAIM / YIELD / COLLIDE

# --- 2.  PRESENCE (`FS_V520_PRESENCE`) ---------------------------------------
# ⛔⛔ THE NUMBER: the turret-gap window is 50.4% NOBODY (v518) -- the gap is
# raider ABSENCE, not raider idleness -- and the v513 replacement latency is a
# MEDIAN OF 90 ROUNDS with 0 of 14 inside Magnus's ~15-round cap.  v513's own
# report names the binding constraint: FUNDING the replacement body, not
# noticing the vacancy (the dedicated-bit beats already notice it in <= 6).
# ⭐ THE FUNDING ANSWER IS v518's TWIN RESERVE, GENERALISED.  That mechanism is
# live and measured: while a purchase the plank needs is not yet affordable,
# the CORE raises its `convert_ammo` titanium floor by that purchase's OWN bar,
# bounded by a TTL, entering through `max()` so no other floor is lowered.
# Here the purchase is a REPLACEMENT BODY: builder + one ferry launcher.
FS_V520_PRESENCE = False    # ⛔⛔ v521 FIRED-CONFIG CORRECTION (i), AND IT IS A
                            # PARENT-CONFIG CORRECTION, NOT A NEW MECHANISM.
                            # v520's single-flag isolation (n=468/arm, four arms
                            # in the same blocks) priced this change at
                            # -2.56 pp wins / -0.21 pp k<=200 / -0.43 pp k<=300,
                            # i.e. null-to-NEGATIVE, and its OWN mechanism metric
                            # failed too: the funded reserve moved replacement
                            # latency by nothing (`pKon` 120.5 rounds / 8-of-31
                            # replaced against `pKonP` 130 / 7-of-30, same tree,
                            # same seeds, flag on and off; 0 of 31 inside
                            # Magnus's 15-round cap, exactly as v513 read 0 of
                            # 14).  Magnus's cap IS met -- at 6 rounds, 26 of 26
                            # -- but by change 1's ROLE-CONVERT of a body already
                            # at the ring, which is `FS_CREW_STALE` and does not
                            # need this flag.  ⛔ THE CODE STAYS IN THE TREE: the
                            # flag is the decision, and a better dose (the
                            # seats half alone, `FS_V520_PRES_SEATS`) is still
                            # measurable behind it.
FS_V520_PRES_MARGIN = 6     # slack above the bar, same shape as
                            # FS_V518_RES_MARGIN.
FS_V520_PRES_TTL = 20       # rounds the reserve survives the last vacancy
                            # reading.  Shorter than the twin's 30: a body is
                            # bought in one round once the bank clears, where a
                            # sentinel waits for a site.
FS_V520_PRES_CAP = 160      # ⛔ HARD CEILING on what this reserve may hold back,
                            # measured against the live scale: builder 78-105 +
                            # launcher 34-38 at the 2.6-3.0x scale seen in the
                            # v513 autopsy.  A reserve with no cap is a magazine
                            # lock wearing a different hat (autopsy #4, three
                            # times).
FS_V520_PRES_MAX_RNDS = 80  # ⛔ PER-MATCH CEILING on rounds the reserve may be
                            # open at all.  The first smoke run held it for 456
                            # consecutive rounds on one nordkap game (support
                            # dead at r36, no replacement ever arrived, seat
                            # stale for ever) -- the magazine lock in a new hat.
                            # 80 rounds is four replacement cycles' worth of
                            # saving at the measured 0.45-0.89 Ti/round bank
                            # slope; past it the plank has other problems and
                            # the ammunition is worth more than the body.
FS_V520_PRES_SEATS = True   # a dead SUPPORT seat raises the spawn budget too.
                            # The parent's replacement clause reads SLOT_FS's
                            # beat only, i.e. the SEALER -- so with the crew on,
                            # a dead support was noticed by the appointment door
                            # and by nothing that pays for a body.
FS_V520_PRES_LOG = False    # PRES520 stderr: VACANT / FILL / RESERVE lines

# --- 3.  ANNULUS FLOOR (`FS_V520_GUNNEAR`) -----------------------------------
# ⭐ THE PRICED v519 ROAD.  v519 change 1 shipped at dose ZERO: 356 attempts,
# 0 plants, with `NORAY` (142) and `NOTGT` (60) the binding refusals -- at
# d^2 = 32-85 with builder vision r^2 = 20 the enemy belt is not visible yet.
# The `pBAND` probe moved `LOKI_BELTBREAK_DSQ_LO` 20 -> 8 and produced 8 plants
# in 8 of 30 games at r9-r38 from a body at d^2 = 4-13.  ⛔ THIS IS A "WHAT"
# CHANGE (the siting rule), which is why v519 refused it and routed it here.
# THE FLOOR MOVES FOR THE GUNFIRST CLAUSE ONLY -- `_try_beltbreak_gunner` is
# called from the chassis raid doctrine as well, and that caller keeps
# LOKI_BELTBREAK_DSQ_LO exactly as it is.
FS_V520_GUNNEAR = False     # ⛔ v521 FIRED-CONFIG CORRECTION (i), second half.
                            # v520 isolation: -0.85 pp wins / +1.50 pp k<=200 /
                            # +0.64 pp k<=300 at n=468/arm -- every one of them
                            # inside the ~5 pp same-config floor that grid was
                            # measured at, i.e. a NULL.  And the mechanism arms
                            # explain why it cannot be more: the lowered floor
                            # is a SUBSTITUTION, not an addition -- plants go
                            # 7 (floor 8) vs 9 (floor 20) while the plant
                            # POSITIONS move from bodies at d^2 16-17 to bodies
                            # at d^2 4-10, because FS_V519_GF_MAX_PLANTS = 1 per
                            # body makes near and far alternatives.  ⭐ AND
                            # TURNING IT OFF RETIRES A LIVE DOCTRINE COLLISION:
                            # with the floor at 8 the shredder fires from ON the
                            # collar (d^2 4-10) at r7-r17, taking a round from
                            # the barrier ladder against Magnus's priority
                            # ruling 1 (barriers -> launchers -> sentinels).
                            # With the flag off the clause is back to v519's
                            # measured zero dose and the collision costs nothing
                            # again.  Code stays; this is a dose decision.
FS_V520_GF_DSQ_LO = 8       # the probe's value.  A gunner at d^2 >= 8 of their
                            # core is 2+ tiles out: still outside the collar
                            # tiles our own barriers want, which is the question
                            # the old floor of 20 existed to answer.
FS_V520_GF_RING_ONLY = False    # if True the lowered floor applies only at the
                                # RING call site (siege.py:1828) and the ferry
                                # site keeps 20.  Shipped False: the probe's
                                # plants came from a body at d^2 = 4-13, i.e.
                                # from the ring, but the ferry site costs
                                # nothing extra to leave open and is measured.

# --- VERIFICATION PROBES.  NEVER SHIPPED.  Each one exists to drive a guard
# --- to its OTHER verdict, because a check that has never produced the other
# --- verdict has not been seen to check. -------------------------------------
FS_V520_PROBE_DUAL_APPT = False  # force TWO opening seats to claim the SUPPORT
                                 # role in the same round.  With
                                 # FS_V520_APPT_GUARD ON the loser must BUSY or
                                 # YIELD; with it OFF both must end up holding
                                 # `fs_body == 2`, which is the crewconv defect
                                 # reproduced on demand.
FS_V520_PROBE_SEAT2 = 5          # ...the second seat the probe converts
FS_V520_PROBE_KILL_RND = -1      # ⭐ THE FORCED-DEATH PROBE, v513's method
                                 # reused verbatim (its build report §Surprise
                                 # 6: the raider self-destructs at r60, 4 reps
                                 # x 5 maps, BOTH trees instrumented
                                 # identically; v513 replaced in 10 of 14 at a
                                 # MEDIAN OF 90 ROUNDS with 0 inside Magnus's
                                 # ~15-round cap).  -1 = off.  The SEALER kills
                                 # itself on this round once it has arrived, and
                                 # `PRESKILL520` / the next `FS ARRIVE` line
                                 # bracket the replacement latency.
FS_V520_PROBE_NO_DECONFLICT = False  # skip the claim-time arc deconfliction, so
                                 # two bodies that land on the same side both
                                 # keep that arc and the DUP alarm must FIRE.
                                 # The alarm reading 0 in the shipped arm means
                                 # nothing until this arm has made it non-zero.

# --- INSTRUMENTS.  OFF in every shipped configuration ------------------------
FS_V520_SPLIT_LOG = False   # SPLIT520: one line per terminal split decision
                            # (arcs reachable, chosen site, arc, walk remainder)
FS_V520_TERM_LOG = False    # TERM520: one line per terminal-launcher siting
                            # decision (candidates, arcs, cover, conflict)
FS_V520_ARC_LOG = False     # ARC520: one line per arc claim / collision
FS_V520_COVER_LOG = False   # COVER520: one line per in-ring launcher birth with
                            # its measured heal-seat coverage (the 0/8 baseline)


# ============================================================================
# LOKI-FS v521 -- SEAL-SHOT SYNCHRONIZATION
# ============================================================================
# ⭐⭐⭐ THE REFRAME THIS BUILD EXISTS FOR, and it came out of v520's own failure
# reel rather than out of a design meeting.  v520 bought MORE seals (cumulative
# seats 6.63 -> 6.99, simultaneous closure 31.7% -> 43.9%) and pooled heal-back
# DID NOT MOVE (median 0.000 in all three arms; the >=0.90 share 18.3 / 18.4 /
# 15.6%).  The reel says why, and it is not a dose problem:
#
#   * ACROSS ALL SIX REEL GAMES, 0 OF 119 ENEMY-CORE HEAL ROUNDS FELL IN A
#     ROUND WHERE EVERY HEAL SEAT WAS DENIED.
#   * `drakkarfjord_s17_A` denied all 8 seats by r33 at ~2.5x the reel median
#     seal rate -- but NEVER SIMULTANEOUSLY (peak 7 of 8, closure_round = -1).
#     468 of our 486 damage was healed back over 72 heal rounds, every one of
#     them in an unsealed round.
#   * `glacierkeep_s37_A` held a GENUINE 43-ROUND FULL CLOSURE, r28 -> r71 --
#     and did not buy its forward sentinel until r76, FIVE ROUNDS AFTER THE
#     SEAL BROKE.  The seal window and the fire window are DISJOINT.
#
# ⇒ CUMULATIVE SEATS SEALED IS NOT THE CURRENCY.  The currency is
#   **closure-simultaneity OVERLAPPING the turret's funded life** -- the count
#   of rounds in which the collar is fully closed AND a forward turret of ours
#   is alive AND the magazine can pay for its shot.  Damage landed in such a
#   round is PERMANENT; damage landed outside one is measured, in this line's
#   own tapes, at close to zero net (v513 change A's anchor: 19,152 dealt,
#   16,962 healed straight back over 24 games, exact to the hit point in
#   eight of them).
#
# v521's mechanism is not "seal more".  It is TO MAKE THE TWO WINDOWS MEET.
# Both windows are already published on channels this tree owns:
#   * the COLLAR side publishes closure (`orth_open` from `_fs_census`, and
#     FS_PH_SEALED on SLOT_FS), and
#   * the TURRET side publishes liveness (`_fs_sent_beat_live`, the v516
#     GLOBALSENT beat, team-global and needing nobody's vision) and funding is
#     one `get_global_ammo()` read away.
# Nothing here invents a channel.  What is new is the READ that joins them and
# the three ladder reorderings that follow from it.
#
# ⛔ AND IT IS A REORDERING, NOT A LOOSENING.  No affordability gate, no siting
# gate, no purchase cap and no salt/eco gate is relaxed by any clause below.
# `_fs_sentinel_ok` is asked exactly as the parent asks it; what changes is
# WHICH RUNG GETS THE ROUND.  That is deliberate: v514's finding 1 is that
# removing a turret gate scored 23/60 against a 37/60 control, and this build
# is not re-opening that road.
LOKI_FS_V521 = True         # master.  False == `bots/_v520pincer` with
                            # FS_V520_PRESENCE / FS_V520_GUNNEAR False, i.e.
                            # the v520-PINCER-ONLY configuration the isolation
                            # grid measured and the concurrent baseline of this
                            # build's headline.

# --- CHANGE 1: THE SYNC READ -------------------------------------------------
FS_V521_SYNC = False        # ⛔⛔ v522 FIRED-CONFIG CORRECTION (i), AND IT IS
                            # THE v521 VERDICT, NOT A NEW OPINION.  The three
                            # ladder reorders (1a NEAR / 1b HOLD / 1c BUYIN)
                            # were measured INERT by the deterministic dose test
                            # (0 of 18 games changed a byte on the three maps
                            # where the sync state fires) and the `iLADDER`
                            # isolation arm read +0.21 pp wins / -4.70 pp k<=200,
                            # both under the fixture's own ~5 pp floor.  The code
                            # stays; the flag is the decision.
                            # ⭐ THE STATE READ ITSELF IS NOT SWITCHED OFF BY
                            # THIS -- `_v521_sync_state` is gated on it, but the
                            # v522 floor does NOT go through that function.  See
                            # the v522 block for why the join is recomputed on
                            # the CENSUS side instead: the Core is the unit that
                            # converts ammunition and it has no eyes at the ring.
FS_V521_SYNC_NEAR = 2       # ⭐ "CLOSURE IS NEAR" = this many seats or fewer
                            # still open.  Two, not one, and the reason is the
                            # pincer: the last TWO seats are exactly what two
                            # bodies on opposite arcs can take in ONE round,
                            # which is the only reason a NEAR window is worth
                            # a reorder at all.  With one body it would be two
                            # rounds and the window would usually break first.
                            # ⚠ UNSWEPT -- 1 and 3 are the obvious neighbours.
FS_V521_FUND_AMMO = 10      # "FUNDED" = the magazine can pay for ONE sentinel
                            # shot.  10, from the engine's own cost table, not
                            # tuned: below it a live turret is a decoration, and
                            # above it we would be asserting a cadence the reel
                            # never measured.
FS_V521_FWD_DSQ = 40        # a turret counts as FORWARD at this d^2 of their
                            # core -- FS_SENT_BEAT_DSQ's value, reused so the
                            # bot-side and beat-side definitions cannot drift.

# --- CHANGE 1a: NEAR -- CLOSE THE LAST SEATS --------------------------------
FS_V521_NEAR_CLOSE = True   # while a forward turret is ALIVE AND FUNDED and
                            # 1 <= orth_open <= FS_V521_SYNC_NEAR, the collar
                            # is the ONLY job: rungs 1' (the early sentinel)
                            # and 1'' (the shredder) are skipped, rung 1
                            # (BARRIER) runs, and if it cannot fire this round
                            # the body WALKS to a remaining seat instead of
                            # dropping to rungs 2-4.  ⛔ This is the clause the
                            # reframe actually names: a closure that lands
                            # inside a funded turret's life is worth more than
                            # any other action available in those rounds.

# --- CHANGE 1b: HOLD -- KEEP IT CLOSED --------------------------------------
FS_V521_HOLD = True         # while a forward turret is ALIVE and orth_open ==
                            # 0, rungs 2 (EVICTOR) and 3 (CLEAR) are suppressed
                            # so the body stays on the collar and re-seals a
                            # broken seat the round it breaks -- rung 1 already
                            # does that the moment `needed` refills, and what
                            # this clause buys is that the body has not walked
                            # off to buy a launcher three tiles away first.
                            # ⛔ RUNG 4 IS DELIBERATELY KEPT: a SECOND sentinel
                            # raises the damage rate INSIDE the overlap window,
                            # which is the quantity, and v517's twin plank
                            # already gates it.
FS_V521_HOLD_FUNDED = False  # if True, HOLD additionally requires the magazine
                            # to be funded.  Ships False: holding a closed
                            # collar while the bank refills is exactly the state
                            # that makes the NEXT shot permanent, and requiring
                            # funding here would drop the guard in the rounds it
                            # is cheapest to keep.  The asymmetry with 1a is
                            # deliberate and this flag is how it gets measured.

# --- CHANGE 1c: BUY INTO THE CLOSURE (the symmetric trigger) ----------------
FS_V521_BUYIN = True        # ⭐ THE OTHER HALF OF THE SAME IDEA.  When closure
                            # is NEAR-or-COMPLETE (orth_open <= NEAR) and NO
                            # forward turret of ours is alive, the SENTINEL
                            # purchase is promoted to the TOP of the ladder --
                            # above rungs 1', 1'' and 1.  `glacierkeep_s37_A`
                            # is the case: a 43-round closure with the purchase
                            # landing 5 rounds after it broke.  Rung 4 sits at
                            # the BOTTOM by design ("it fires on the rounds the
                            # collar has nothing actionable left"), and inside a
                            # closure window that design is exactly backwards --
                            # those are the rounds the turret is worth most.
                            # ⛔ GATES UNCHANGED.  `_fs_sentinel_ok` still has
                            # to say yes (salt/eco disjunction, reserve, live
                            # count, purchase cap).  Only the ORDER moves.
FS_V521_BUYIN_MAX_RND = 400  # a bounded clause, not a standing inversion.  Past
                            # this round the ladder is the parent's again.
# ⛔ THE WALK HALF OF THIS IDEA WAS DESIGNED, THEN DROPPED AS A DUPLICATE, AND
# THAT IS RECORDED HERE RATHER THAN SHIPPED AS A FLAG NOBODY READS.  The
# mandate's symmetric trigger asks that a body walk toward the sentinel site
# when the purchase is gated only by siting.  `_fs_stand_target` ALREADY DOES
# EXACTLY THAT: v516 `FS_V516_SENTREACH` makes the reach station a walker
# preference with its own patience timer, and v518 `FS_V518_EARLY_REACH_FIRST`
# already promotes it ABOVE the evictor's reach in precisely the state this
# clause would fire in -- while no forward sentinel is alive.  A second walker
# preference on the same tiles would not be a mechanism, it would be a second
# reading of the same one, and the isolation grid could never separate them.
# ⇒ v521 changes the ACTION ORDER only.  The walk is the parent's.

# --- CHANGE 1d: THE COLLAR'S MONEY (the clause the diagnostic produced) ------
# ⭐⭐⭐ THE MECHANISM THAT SURVIVED.  Clauses 1a/1b/1c reorder the raider's
# ladder; the deterministic dose test measured all three INERT on the maps where
# the sync state fires (0 of 18 games changed a byte), and `_v521_why` then named
# the two real blockers in every NEAR round: the body is not ADJACENT to the open
# seat, and THE BANK IS BELOW THE COLLAR'S PRICE.  The second one is ours: with a
# forward turret live the Core drops its conversion floor to a two-barrier repair
# allowance and converts everything above it into ammunition, and v513 change F
# measured that the bank then EQUILIBRATES TO THE FLOOR AND STAYS THERE.  So the
# funded turret is what starves the seal -- the seal-shot disjointness is not
# only a scheduling accident, IT IS PARTLY CAUSED BY US.
# ⛔ IT IS A RESERVE, NOT A SPEND.  It only ever raises a floor (`max`), it opens
# no gate, and it lapses the moment the published phase says the collar is shut.
FS_V521_PHASE_HONEST = True  # ⭐ publish FS_PH_KILL_OPEN whenever a turret is
                            # live AND the collar reads open THIS ROUND, instead
                            # of only when it has never closed.  Without this
                            # 1d is unreachable on any board whose collar closed
                            # once -- measured: 0 of 12 deterministic games on
                            # drakkarfjord/glacierkeep changed with 1d alone.
                            # ⚠ IT MOVES A SHARED CHANNEL.  The magazine's
                            # `armed` term reads `SEALED <= ph <= KILL` and would
                            # go False at KILL_OPEN -- the v516 GLOBALSENT
                            # disjunct (`beat live -> armed = True`) is what
                            # keeps the magazine armed there, and it is a
                            # DISJUNCT by construction.  `_fs_salt_ok`'s
                            # crew-wide read stops latching `fs_sealed_rnd` on an
                            # open collar, which is the correct reading of a
                            # latch whose job is to say the collar is shut.
FS_V521_COLLARFIRST = False  # ⛔⛔ v522 FIRED-CONFIG CORRECTION (ii), AND IT IS
                            # THE ONE MEASURED REJECTION OF THE v521 LEG.  The
                            # `iMAG` isolation arm (1d + 1e) carried the WHOLE
                            # composite regression: -9.83 pp on the tracked
                            # k<=200 metric and -7.48 pp at r300, BOTH OUTSIDE
                            # their intervals at n=468, with the phase budget
                            # naming the cell -- `funded -> kill` 69 -> 100
                            # rounds against a known-zero control at 69.
                            # ⭐ THE DIAGNOSIS IT WAS BUILT ON SURVIVES; THE
                            # DOSE DOES NOT.  Holding `8 * bar + 6` (56-72 Ti at
                            # the live scale) back from `convert_ammo` in EVERY
                            # open-collar round starves the magazine that is the
                            # clock.  v522 keeps the diagnosis -- our own floor
                            # pins the bank one barrier short of the seal -- and
                            # replaces the dose with a NEAR-gated one worth
                            # FS_SEAL_MARGIN, not a whole collar.  See the v522
                            # block.
FS_V521_COLLAR_BARRIERS = 8  # the whole orthogonal-8, which is the purchase that
                            # is genuinely still pending while the collar reads
                            # open -- the same `8 * bar` the parent already
                            # computes one branch up for this exact state and
                            # then overwrites with the repair allowance.
FS_V521_MAG_LOG = False     # MAG521: one line per round the collar reserve
                            # actually raises the floor.

# --- the instrument ---------------------------------------------------------
FS_V521_SYNC_LOG = False    # SYNC521: one stderr line per at-ring round with
                            # the joined state (orth_open, turret liveness,
                            # ammo, body, which clause fired).  Local only --
                            # platform replays carry no stdout (CLAUDE.md s28).
FS_V521_WHY_LOG = False     # WHY521: one line per NEAR/HOLD round naming what
                            # BLOCKED the collar that round (seats wanted, seats
                            # adjacent to this body, seats blocked by an
                            # occupant, whether rung 3 would fire, bank vs the
                            # seal price).  ⛔ This is the instrument that
                            # decided the build -- see `_v521_why`.
FS_V521_RUNG_LOG = False    # RUNG521: one line per ladder decision with the
                            # rung index, so the REORDER is readable
                            # zero-vs-nonzero rather than inferred from outcome.

# --- CHANGE 0: THE GATED-MAP LEAK, a parent-config correction ---------------
# ⛔ v520 OPEN ITEM 7, AND IT IS A DEFECT RATHER THAN A DESIGN.  Two
# `fs_crew_on()` read sites sit OUTSIDE the ferry-siege map gate
# (`main.py:1000`, the spawn-purpose anchor, and `main.py:1084`, the roster line
# that makes FS_CREW_SEAT a raider instead of an eco expander).  Both are the
# PARENT's structure; v520 only turned on the flag that reaches them.  The
# consequence is measured, not hypothetical: on a board the ferry-siege REFUSES
# (FS_MAP_SKIP / the small-board gate / FS_V519_CRIPPLE_MAPS) v520 STILL SPENDS
# SEAT 3 AS A RAIDER instead of on the economy, so the archipelago control leg
# was not the null-by-construction leg it was designed to be.
FS_V521_GATEFIX = True
# ⛔ THE ROSTER SITE NEEDS THE CORE, AND THE CORE IS RESOLVED TWENTY LINES
# LATER.  `_fs_gate` reads `self.core`, which `_builder` fills in AFTER the
# roster block.  The fix does NOT move the roster block and does NOT move the
# `if self.core is None: return` guard (moving that would change which round a
# body first increments the role counter).  It hoists the core RESOLUTION --
# the same `get_nearby_buildings` scan, idempotent, assigning the same
# attribute -- so the gate is computable where the seat is issued.  With the
# flag off the scan happens exactly where the parent does it.
FS_V521_GATEFIX_LOG = False  # GATEFIX521: one line per gated roster refusal.


# =============================================================================
# LOKI-FS-V522 -- THE MAGAZINE FLOOR STOPS STARVING THE SEAL.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v521sync` AS CONFIGURED IN THIS FILE (frozen, md5 in
# `scratchpad/s51_v522_build/PARENT_FREEZE.md5`) -- that is v520-PINCER-ONLY
# plus the gated-leak fix plus PHASE_HONEST, with FS_V521_SYNC and
# FS_V521_COLLARFIRST turned off at their definition sites above.
# `LOKI_FS_V522 = False` reproduces exactly that tree, and every branch below is
# guarded by this flag AND its own sub-flag at the READ SITE.  No doctrine-level
# derived default reads any of them (v515 finding 3: `mkarm.sh` appends arm
# overrides AFTER the module body has run, so a module-level
# `if LOKI_FS_V522: X = ...` is evaluated against the WRONG flag value).
#
# ROUTING: `docs/research/BUILD-REPORT-v521sync-2026-08-18.md`, builder verdict
# line 3 -- *"The measured lever for v522: our own magazine floor starves the
# seal ... Fix the floor, not the ladder."*
#
# ⭐⭐⭐ THE MEASUREMENT THIS BUILD EXISTS FOR, AND IT IS AN OBSERVATION ABOUT
# OUR OWN CODE, NOT ABOUT THE OPPONENT.  `_v521_why` tapes the modal NEAR round
# on three maps at seed 7:
#     drakkarfjord  adj=0 blk=0 clr=0 ti=12 price=18   (13 rounds)
#     glacierkeep   adj=0 blk=0 clr=0 ti=14 price=20   (71 rounds)
#     glacierkeep   adj=0 blk=0 clr=0 ti=16 price=22   (38 rounds)
#     nordkap       adj=0 blk=0 clr=0 ti=16 price=14   (28 rounds)
# `ti` is the bank; `price` is `seats_still_open * bar + FS_SEAL_MARGIN`.  In
# every binding row THE BANK IS EXACTLY `FS_MAG_REPAIR_BARRIERS * bar` -- 2 x 6,
# 2 x 7, 2 x 8 -- because with a forward turret live the Core drops its
# conversion floor to a two-barrier repair allowance and converts everything
# above it into ammunition, and v513 change F measured that the bank then
# EQUILIBRATES TO THE FLOOR AND STAYS THERE.  The gap is ONE BARRIER PLUS THE
# HOP MARGIN.  We are not out of money; we are holding back not-quite-enough.
#
# ⛔ AND THE PREMISE THAT SET THAT FLOOR DIED AT v515.  Its stated argument is
# "a sentinel only exists once the collar was CLOSED, so what the collar still
# needs at KILL is a REPAIR allowance, not a fresh collar".  True under v513's
# salt-only gate.  False since v515's `FS_V515_GATE_OR` eco disjunct, which buys
# a sentinel with the collar OPEN, and since v516's GLOBALSENT beat, which arms
# the branch off turret LIVENESS with no closure term at all.
#
# ⭐⭐ WHY IT IS WORTH A BUILD: THE OVERLAP LEDGER PRICES THE ROUND.  v521
# measured, replay-side, n=1,080/arm, stable across all three arms: net damage
# on the enemy core is **6.97 per round in which the collar is sealed AND a
# funded forward turret is alive**, against **1.13 in every other round** -- a
# 6x gap.  A barrier bought in a NEAR round is the purchase that converts a
# 1.13-round into a 6.97-round.  v521 bought +9.50 sealed rounds and paid
# -6.48 funded rounds for them, so OVERLAP did not move (13.35 -> 13.68 against
# a known-zero at 13.31).  ⇒ THE PLANK HAS TO BUY THE SEAL **WITHOUT** SELLING
# THE MAGAZINE, and that is the whole design constraint below.
#
# ⛔⛔ HOW THIS DIFFERS FROM v521 CHANGE 1d, WHICH IS THE SAME DIAGNOSIS AND A
# REJECTED DOSE.  1d held `FS_V521_COLLAR_BARRIERS * bar + FS_SEAL_MARGIN` =
# **8 x bar + 6 = 56-72 titanium** back in EVERY round the collar read open.
# That is the magazine's entire working capital, and the phase budget measured
# what it cost: `funded -> kill` 69 -> 100 rounds, k<=200 -9.83 pp.  v522 holds
#   * only while closure is NEAR (<= FS_V522_NEAR seats open, i.e. one or two),
#   * only while a forward turret is ALIVE **and FUNDED**,
#   * only when the raise actually BINDS (the raider publishes the state only
#     if the seal price exceeds the repair allowance the Core would hold),
#   * at most `FS_V522_NEAR * bar + FS_SEAL_MARGIN` = **20-26 titanium**,
#   * for at most FS_V522_MAX_RNDS rounds in a match,
#   * and it RELEASES the round the collar shuts, the turret dies, or the
#     raider stops publishing -- all three of which change the phase code.
# ⇒ SAME LEVER, ~1/3 OF THE DOSE, AND A NEAR GATE THAT 1d DID NOT HAVE.
#
# ⛔ IT IS A RESERVE, NOT A SPEND.  It only ever enters through `max()`, it
# opens no gate, it buys nothing, and it can never lower a floor -- so
# E1_AMMO_FLOOR's harvester guarantee and every other floor in that block are
# exactly what they were.
LOKI_FS_V522 = True         # master.  False == `bots/_v521sync` with
                            # FS_V521_SYNC / FS_V521_COLLARFIRST False, i.e. the
                            # v521 verdict's "NEXT PARENT" and the concurrent
                            # baseline of this build's headline.

FS_V522_FLOOR = False        # the mechanism.  ⭐ v524 CHANGE 2 -- flipped True
                            # -> False here, description-alignment only.  The
                            # v522 build's own KILL_TARGET panel measured ON
                            # vs OFF at 733/1080 == 733/1080 (+0.00pp,
                            # BUILD-REPORT-v522floor-2026-08-18.md:282,293) --
                            # MEASURED INDIFFERENT, not a plank that pays or
                            # costs.  This aligns the tree with the
                            # commissioning brief's own description ("pincer +
                            # leakfix + PHASE_HONEST, sync/floor off") that
                            # `_v522floor` itself shipped contradicting
                            # (PREREG-PINCERPOOL-2026-08-18.md blocker B1).
FS_V522_NEAR = 2            # ⭐ "CLOSURE IS NEAR" = this many orthogonal heal
                            # seats or fewer still open.  FS_V521_SYNC_NEAR's
                            # value, reused rather than re-derived so the two
                            # readings of "near" cannot drift.  Two, not one,
                            # because the pincer puts two bodies on opposite
                            # arcs and the last two seats are what they can take
                            # in one round.  ⚠ UNSWEPT -- 1 and 3 are the
                            # obvious neighbours and 1 is the conservative one.
FS_V522_FUND_AMMO = 10      # "FUNDED" = the magazine can pay for ONE sentinel
                            # shot.  FS_V521_FUND_AMMO's value, from the
                            # engine's own cost table, reused for the same
                            # anti-drift reason.  ⛔ READ ON THE CORE, not
                            # published: `get_global_ammo()` is a team-global
                            # read and the Core has it for free, so the funding
                            # half of the join costs no channel.
FS_V522_SEATS = 2           # the seats the raised floor PRICES.  Equal to
                            # FS_V522_NEAR by construction: the phase field's
                            # last free code carries NEAR-ness, not the count,
                            # so the Core prices the worst case inside the NEAR
                            # band.  ⚠ AT orth_open == 1 THIS OVER-RESERVES BY
                            # ONE BARRIER (3-10 Ti).  The publish-if-binding
                            # rule below is what keeps that from mattering: at
                            # one seat open the seal price already sits at or
                            # under the repair allowance on every scale where
                            # bar >= 6, so the state is not published at all.
FS_V522_FLOOR_CAP = 40      # ⛔ HARD CEILING on what this reserve may hold back,
                            # the shape v520's FS_V520_PRES_CAP uses.  `2 * bar
                            # + 6` is 12 at scale 1.0 and 26 at bar = 10; the cap
                            # binds only if the cost scale runs past ~5.7x, which
                            # is a state no measured game reaches.  It exists so
                            # a scale excursion cannot turn a 26-titanium reserve
                            # into v521's 72-titanium one by arithmetic.
FS_V522_MAX_RNDS = 150      # ⛔ PER-MATCH CEILING on the rounds this floor may
                            # BIND (raise the number, not merely be eligible).
                            # The TTL the mandate asks for, and it is counted on
                            # the Core, which is the unit that owns the decision.
                            # 150 is ~15% of a match and comfortably above the
                            # 69-round `funded -> kill` budget the plank is
                            # trying to protect; a NEAR window that has been open
                            # for 150 rounds is not a closure that is about to
                            # land, it is a stall, and a stall must not keep
                            # taxing the magazine.
FS_V522_BIND_IF = True      # ⭐ PUBLISH-IF-BINDING.  The raider publishes
                            # FS_PH_KILL_NEAR only when the remaining seal price
                            # actually EXCEEDS the repair allowance the Core
                            # would otherwise hold (`n * bar + FS_SEAL_MARGIN >
                            # FS_MAG_REPAIR_BARRIERS * bar`).  Two reasons and
                            # the second is the load-bearing one:
                            #   (a) it makes the reserve exact rather than
                            #       conservative -- with one seat open and
                            #       bar >= 6 the bank already covers the seal,
                            #       so there is nothing to fix;
                            #   (b) IT KEEPS THE CHANNEL CHANGE OFF THE ROUNDS
                            #       THE MECHANISM DOES NOT ACT ON.  A phase code
                            #       published in rounds where the floor does not
                            #       move is a shared-channel change with no
                            #       mechanism attached to it, which is exactly
                            #       the kind of unpaid risk v521's doctrine
                            #       collision 1 flagged.
                            # ⚠ IT COUPLES THE RAIDER'S PUBLISH TO A CORE-SIDE
                            # CONSTANT (FS_MAG_REPAIR_BARRIERS).  That is
                            # deliberate and it is why the constant is read
                            # rather than duplicated; set this False to sweep
                            # the un-coupled form.
FS_V522_PHASE_ONLY = False  # ⛔ THE CHANNEL-SUBSTITUTION MUTANT, NEVER SHIPPED.
                            # True publishes FS_PH_KILL_NEAR exactly as the fired
                            # build does and NEVER raises the floor.  If the
                            # nine-site enumeration above is right, this arm is
                            # BYTE-IDENTICAL to the parent -- which turns "the
                            # new phase code is behaviourally inert at every
                            # existing consumer" from an argument into a
                            # measurement.  It is also the negative control for
                            # the mechanism arms: PHASE_ONLY must drive the
                            # MAG522 column to zero while leaving PH522 nonzero.
# --- THE TWO REACHABILITY CORRECTIONS, AND BOTH WERE MEASURED BEFORE THE ------
# --- HEADLINE RATHER THAN DISCOVERED IN IT -----------------------------------
# ⛔⛔ THE PRE-HEADLINE REACHABILITY CENSUS CHANGED THIS DESIGN TWICE.  36
# instrumented games (6 maps x 3 seeds x 2 seats, noise off both sides, MAG522 +
# PH522 on) were run before a single headline block, exactly as v521's dose test
# was, and the tape showed the mechanism firing 45 times against 348 rounds in
# which the Core READ the NEAR code -- a 13% conversion with two named causes:
#
#   (1) THE CORE'S OWN FUNDING RE-CHECK KILLED 100 OF 100 GLACIERKEEP NEAR
#       ROUNDS.  Every one read `fund 0` at `ammo` 8 or 0 while the RAIDER's
#       publish-time check had passed at >= 10 in the round before.  The two
#       reads are one round apart and the turret FIRES in between: a sentinel
#       shot costs 10 and the magazine cycles 10 -> 0 every reload.  So
#       `ammo >= 10` read on the Core is not "the turret is funded", it is "the
#       magazine has a spare shot AFTER the one it just took" -- and it stands
#       the plank down in precisely the state it exists for, a turret that is
#       BURNING its funding beside a collar one barrier short.
#   (2) THE CORE WAS BLIND TO BODY 2.  `_fs_state` reads SLOT_FS, which is body
#       1's word; body 2 publishes into FS_SUPP_SLOT (v514 change D, one writer
#       per slot).  Measured: 60 of 69 nordkap publishes and 68 of 269
#       glacierkeep publishes came from body 2 and could not be seen.
#
# ⛔ NEITHER CORRECTION LOOSENS A GATE.  (1) MOVES the funding term to the read
# that measures it rather than deleting it -- the raider still refuses to
# publish below FS_V522_FUND_AMMO.  (2) reads a channel a peer body already
# writes, with a FRESHNESS test the SLOT_FS path does not have, so a dead body's
# last word cannot pin the floor.
FS_V522_CORE_FUND = False   # if True the Core RE-CHECKS `ammo >= FUND_AMMO` in
                            # its own round.  Ships False, and the reason is
                            # measured above, not preferred.  Left as a flag
                            # because it is the honest isolation arm for
                            # correction (1) and because a future magazine plank
                            # may want the re-check back.
FS_V522_CREW_READ = True    # the Core reads the NEAR code off EVERY slot a
                            # ferry-siege body of ours publishes into
                            # (`_fs_crew_slots`), not only SLOT_FS, and requires
                            # the slot's own beat to be fresh
                            # (FS_BEAT_STALE).  ⚠ IT IS A DISJUNCT: it can only
                            # ADD a NEAR round, never remove one, so the SLOT_FS
                            # reading is exactly what it was.
                            # ⚠ THE INHERITED ASYMMETRY IS NOT FIXED HERE:
                            # `_fs_salt_ok` also calls the SLOT_FS phase "the
                            # crew's shared answer" while reading one body's
                            # word.  That is the parent's and this build does
                            # not touch it -- flagged, not resolved.
FS_V522_PROBE_NOPUB = False  # ⛔ VERIFICATION PROBE, NEVER SHIPPED.  True makes
                            # `_v522_near_publish` perform every engine read it
                            # normally performs -- `get_barrier_cost` and
                            # `get_global_ammo` -- and then return False, so the
                            # phase code is never written.  It exists to
                            # SEPARATE two candidate causes of any byte
                            # divergence in the channel-substitution control:
                            # the new phase VALUE, and the two extra engine
                            # calls (which cost CPU microseconds, and this tree
                            # has CPU-budget gates -- FS_SENT_REACH_CPU_US).
                            # PROBE == parent means the calls are free and the
                            # phase value is the cause; PROBE != parent means
                            # the opposite.  v513's forced-death method applied
                            # to a channel question.
FS_V522_MAG_LOG = False     # MAG522: one line per round the floor is EVALUATED,
                            # with a `bind` field, so the denominator is visible
                            # and a zero is readable (v521 surprise 7).
FS_V522_PH_LOG = False      # PH522: one line per round the raider publishes the
                            # NEAR code, and one per round it is eligible but
                            # declines -- again so a zero has a denominator.


def fs_crew_on():
    """⭐ THE READ SITE FOR `FS_CREW_ON`.  Never a module-level derived default.

    Evaluated at RUN time by every reader, so an arm that appends
    `FS_V520_CREW = False` (or `LOKI_FS_V520 = False`) to the end of this file
    gets the value it asked for -- which a module-level `FS_CREW_ON = True`
    would not have given `FERRY_HOME_ON`, computed at import.  That is the
    v515 finding-3 hazard, confirmed live at the 06:24Z crewconv pre-flight
    (COLLISION:True), and this function is what keeps it from recurring.
    """
    if LOKI_FS_V520 and FS_V520_PINCER and FS_V520_CREW:
        return True
    return FS_CREW_ON


# =============================================================================
# LOKI-FS-V524 -- THE CRIPPLE-LIST EXACT MATCH.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v522floor` (frozen, md5 in
# scratchpad/s51_v524_build/PARENT_FREEZE.md5).  `LOKI_FS_V524 = False`
# reproduces the parent's collision bug exactly -- the mutant this build's own
# verification drives to re-select 4 maps instead of 2.
#
# THE BUG (PREREG-PINCERPOOL-2026-08-18.md finding 2 / "THE THIRD THING",
# `docs/prereg/PREREG-PINCERPOOL-2026-08-18.md:127-161`): `FS_V519_CRIPPLE_MAPS`
# keys on `(w, h, min(core), max(core))`, which is exactly `FS_MAP_SKIP`'s
# signature -- built because no map name reaches a bot.  Two OTHER pool maps
# share that signature with the two the comment names:
#     (30, 30, (2,2), (26,26))  ->  midgard   AND  ragnarok
#     (20, 20, (2,9), (16,9))   ->  yulerune  AND  frostgate
# Computed at draft with `tools/map_encode.parse_map26` over every
# `maps/*.map26` in the pool, independently of any bot code. Verified again at
# this build with the same tool, both against the committed `EXTRA_MAP_CODES`
# entries below (byte-identical, fresh encode == committed string) and against
# each other (`encode(midgard) != encode(ragnarok)`,
# `encode(yulerune) != encode(frostgate)` -- the discriminator exists).
# ⇒ `ragnarok` and `frostgate` stand down MAPSEG's second-best rush cell
# (`glacierkeep` aside, `ragnarok` is RUSH-quadrant per the MODESWITCH table
# above, doctrine.py:3881-3886) for no reason the tree's own comment states.
#
# THE FIX is the SAME MECHANISM `known_map_for` already uses for every other
# same-(w,h,anchor) collision this tree ships (eider/heart, the two 26x26s,
# `eco.py:121-134`): a coarse signature match is a CANDIDATE, confirmed
# against the actual tile grid before it is allowed to refuse a map. No new
# decode path -- the two reference grids below are `eco._decode_grid` applied
# to the exact `EXTRA_MAP_CODES` strings already committed for `# midgard` and
# `# yulerune` (doctrine.py:1167, :1171), so the only new fact this file
# states is WHICH of the two same-signature codes is the cripple one.
#
# `_fs_map_gated` (siege.py) still does the coarse `sig519 in
# FS_V519_CRIPPLE_MAPS` test first -- unchanged, so `LOKI_FS_V524 = False`
# restores the parent's four-map collision.
#
# ⛔ CORRECTED s51, 2026-08-19 (v527 hygiene). THIS SENTENCE READ "reproduces
# the parent's four-map collision exactly, BYTE-FOR-BYTE, with no other code
# path touched" AND NO BATTERY IN THAT BUILD MEASURED IT. v524's byte-identity
# table (BUILD-REPORT-v524exact-2026-08-18.md:114-134) is v524 **AS FIRED** vs
# the parent -- identical on midgard/yulerune/archipelago, DIFFERS on
# ragnarok/frostgate. The `LOKI_FS_V524 = False` arm the sentence describes was
# never run. It was a plausible inference wearing the typography of a
# measurement, in the file every session loads. The claim is downgraded to what
# the code supports (the coarse test is first and unchanged) and the flag-off
# identity is now measured for real by v527's own byte-identity battery.
#
# When `LOKI_FS_V524` is True, a coarse hit is only a CANDIDATE: it is
# confirmed against `self.map_grid` (or, if that is not yet resolved -- the one
# call site is the v516 turret beat, whose own `self.core` is None by design and
# never sets it -- against a fresh `known_map_for(mw, mh, ours, ct)` call, used
# LOCALLY AND DELIBERATELY NOT CACHED) before it is allowed to refuse.
#
# ⛔ CORRECTED s51, 2026-08-19 (v527 hygiene). THIS READ "cached into
# `self.map_grid` exactly as the Core/builder call sites already do" AND IT
# DESCRIBES THE FIRST DRAFT, WHICH WAS A CORRECTNESS BUG THAT WAS REMOVED
# BEFORE v524 SHIPPED. `self.map_grid` is ALSO the guard on `main._builder`'s
# own map init (`main.py:1325`), and the v521 gatefix crew-seat read runs
# BEFORE that init on the round a builder's `self.core` first resolves --
# so caching here made that guard false early and silently lost
# `self.map_walls` / `self.map_ores` for that unit for the whole match.
# Caught by a midgard byte-identity spot-check that should have been a no-op
# and instead diverged at r280 (winner flipped, units 6 vs 17). The shipped
# code RECOMPUTES on every early ask; the repeat `known_map_for` is cheap
# (tile-sense + compare, no re-decode -- `_decode_grid` is cache-memoised) and
# is paid only on the colliding-signature maps, only before the official init
# resolves. Provenance: BUILD-REPORT-v524exact-2026-08-18.md:51-72.
LOKI_FS_V524 = True         # master.  False == `bots/_v522floor` unchanged
                            # (the registered mutant -- must re-select 4 of 15
                            # pool maps as CRIPPLE, not 2).
FS_V524_MIDGARD_CODE = "AAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAASAAAAAAADABAAAAAAADABAAAAAASDABAAAAAAAMEAAAAAAAAAAJEAAAAAACGAAAAAAAAMBMEMEAAASAJDAADAAAAAJDAADAAAAAJDAADAAAAAAASCAAAAAAAASCAAAAAAADAADBAAAAADAADBAAAAADAADBACAAAMEMEJEAAAAAAAAGSAAAAAAMBAAAAAAAAAAMEAAAAAAAJADCAAAAAAJADAAAAAAAJADAAAAAAACAAAAAAAAAASAAAAAAAAAAAAAAAAAAAAAA"
FS_V524_YULERUNE_CODE = "AAAAAAAAAAAAAACAYAAAAPAAJCAAJAABAAAJADAAAALJGAAAAJBAAAAAMAAAAAAEAAAAAJBAAAAAMAAAAAAEAAAASDDCAAAJADAAAABADAAAFAAVAAAAYAACAAAAAAAAAAAAAA"
FS_V524_LOG = False          # V524: one stderr line the first time the exact
                            # match confirms OR rejects a coarse cripple
                            # candidate, per unit -- the BEFORE instrument.

# =============================================================================
# LOKI-FS-V525 -- THE STANDDOWN FLIP.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v524exact` (frozen, md5 in
# scratchpad/s51_v525_build/PARENT_FREEZE.md5). `LOKI_FS_V525 = False`
# reproduces the parent's 5-standdown behaviour exactly (the registered
# mutant): CRIPPLE = {midgard, yulerune}, GATED = {antler, archipelago,
# fjordgate}.
#
# BASIS -- Magnus's ask ("could we test it on all maps and check if it
# performs better than we thought?"), answered by the FORCEALL probe
# (`scratchpad/s51_forceall/results.tsv`, n=90/map, forced-rush -- every
# threshold zeroed at definition-site -- vs `bots/_v488beltbreak2`, PAR=2
# under the running PINCERPOOL shard, coordination.md tail note ~2026-08-18
# 17:08:11Z): the standdowns are stale-calibrated (gates = v510-era
# thresholds, cripple list = v513-era reads) and the rush has since gained
# pincer/funding/door-off/terminal-hop.
#     yulerune   91.1% [+-5.9]  n=90   (mirror 50.0; medkill 109; the CURRENT
#                                       rush's best cell anywhere)
#     antler     64.4%          n=90
#     fjordgate  63.3%          n=90   (10x10, core d^2=32; 0 tracebacks)
#     midgard    40.0%          n=90   -- STAYS cripple, unflipped (below the
#                                       mirror; the v519 reasoning for keeping
#                                       it off the exact-match list is still
#                                       right at current strength)
#     archipelago 17.8%         n=90   -- STAYS gated via FS_MAP_SKIP (well
#                                       below the mirror; the closure-based
#                                       skip is validated, not stale)
# Two changes, one master flag; both fire together because they are the same
# finding (stale standdown calibration), not two independent claims.
#
# CHANGE 1 -- YULERUNE LEAVES THE CRIPPLE LIST.  `FS_V519_CRIPPLE_MAPS` (the
# COARSE (w,h,anchor) signature set feeding v524's exact-grid disambiguation)
# carries two signatures: midgard's (shared with ragnarok) and yulerune's
# (shared with frostgate). At current strength yulerune is the rush's best
# cell on the whole pool (91.1 vs the 50.0 mirror, >6 half-widths clear) --
# the v519-era crater this list was built against no longer exists. Dropping
# yulerune's signature from the coarse candidate set means yulerune (AND
# frostgate, which shares the signature and was already reclaimed by v524's
# exact match) never reach the CRIPPLE test at all: both play siege-active.
# Midgard's signature stays -- midgard itself measures 40.0 (still below the
# mirror, stays crippled) and v524's exact-grid match still disambiguates it
# from ragnarok (which measured a real rush gain in MAPSEG, doctrine.py
# :3881-3886, and must keep playing siege-active).
#
# CHANGE 2 -- ANTLER + FJORDGATE UN-GATED.  `FS_MIN_MAP_DIM`/`FS_MIN_CORE_DSQ`
# are v510-era thresholds (12, 72) written before pincer/funding/door-off/
# terminal-hop existed, calibrated against a fjordgate LOSS the current rush
# does not reproduce (fjordgate 63.3%, antler 64.4%, both clear of the
# mirror). The mechanism stays -- this is a THRESHOLD change, not a removal
# (`do NOT zero them`): the new floors are DERIVED FROM THE TWO MAPS' OWN
# ACTUAL GEOMETRY, at the tightest values that still admit both, so any map
# smaller/closer than fjordgate is still refused:
#     fjordgate  10x10, core d^2=32   (`tools/map_encode.parse_map26`,
#                                      cores (2,2)/(6,6): dx=4,dy=4 -> 32)
#     antler     14x18, core d^2=64   (cores (6,4)/(6,12): dx=0,dy=8 -> 64)
# fjordgate is the binding map on BOTH axes (its d^2=32 < antler's d^2=64,
# and its larger side 10 < antler's 18) so its own measured values ARE the
# minimal thresholds that admit both:
#     FS_V525_MIN_MAP_DIM  = 10   (fjordgate's own larger side; a 9x9 or
#                                  smaller board is still refused)
#     FS_V525_MIN_CORE_DSQ = 32   (fjordgate's own core d^2; anything closer
#                                  is still refused)
# The strict `<` comparison in `_fs_map_gated` means a map matching the floor
# EXACTLY still passes (10 < 10 is False; 32 < 32 is False) -- fjordgate is
# admitted at its own boundary, not by a margin that would also sweep in
# smaller/closer maps nobody has measured. archipelago is UNCHANGED by this
# change (it is refused by `FS_MAP_SKIP`, a different, closure-based
# mechanism, not by the dim/dsq gate) and stays gated at 17.8%.
#
# `_fs_map_gated` (siege.py) reads both selections AT RUNTIME (`LOKI_FS_V525
# and ...`), never at module scope, matching every prior flag in this file --
# no derived-default hazard for the same-file append-ordering reason v515/
# v524 already document.
LOKI_FS_V525 = True         # master.  False == `bots/_v524exact` unchanged
                            # (the registered mutant -- CRIPPLE stays
                            # {midgard, yulerune}, GATED stays
                            # {antler, archipelago, fjordgate}).
FS_V525_CRIPPLE_MAPS = frozenset((
    (30, 30, (2, 2), (26, 26)),        # midgard signature (shares w/ ragnarok;
                                        # still disambiguated by v524's exact
                                        # grid match) -- yulerune's signature
                                        # is DELIBERATELY ABSENT here.
))
FS_V525_MIN_MAP_DIM = 10    # fjordgate's own larger side (was 12)
FS_V525_MIN_CORE_DSQ = 32   # fjordgate's own core d^2 (was 72)
FS_V525_LOG = False          # V525: one stderr line the first time the
                            # flipped gate/cripple selection is evaluated,
                            # per unit -- the BEFORE instrument.


# =============================================================================
# LOKI-FS-V526 -- TRANSIT.  s51, 2026-08-18.
# =============================================================================
# Parent: `bots/_v525flip` (frozen, md5 in
# scratchpad/s51_v526_build/PARENT_FREEZE.md5).  `LOKI_FS_V526 = False`
# reproduces the parent exactly -- every read below is a RUN-time read at the
# point of use and NO module-level derived default reads any v526 name (the
# v515 finding-3 hazard; `flagoff_ast.py` proves it with the FERRY_HOME_ON
# positive control).
#
# TWO SHIPPED CHANGES + ONE ROUTED NON-CHANGE, from Magnus's markers 3/4/12/13.
#
# ⭐ M6 -- OPENING TEMPO, AND THE CAUSE IS ROSTER SEQUENCING, MEASURED, NOT
# GUESSED.  The mandate named three candidates (funding order, discovery,
# roster sequencing).  Instrumented tape, 4 ferry-active games of 5
# (`scratchpad/s51_v526_build/rc/`, `RC TEMPO`):
#
#   RC TEMPO 1 id 3 body 1 born 1 lp 0 must 0 why norid ... ti 434 lcost 28
#   RC TEMPO 2 ... must 0 why norid ... ti 392 lcost 32
#   RC TEMPO 3 ... must 0 why norid ... ti 344 lcost 36
#   RC TEMPO 4 ... must 0 why norid ... ti 354 lcost 36   <- body 2 born HERE
#   RC TEMPO 5 ... must 1 why near2                       <- first link r5
#
#   * FUNDING IS EXCLUDED: the bank is 434 Ti against a launcher price of 28 in
#     the FIRST round the lead runs, and never binds in any of the four.
#   * DISCOVERY IS EXCLUDED: the lead prints a resolved enemy-core d^2 from r1.
#   * ROSTER SEQUENCING IS THE CAUSE: `_fs_relay_mustered` returns False with
#     reason `norid` -- body 2 HAS NOT REPORTED -- for rounds 1..4, because body
#     2 is roster seat 3 and the Core spawns one builder per turn.  The lead
#     does not merely decline to build; the muster branch `return`s, so it does
#     not move either.  FOUR ROUNDS OF A RUSH SPENT STANDING STILL, 4/4 games.
#
# ⇒ The fix is to issue the support seat EARLIER, not to weaken the muster (the
# muster is what buys the two-rider link).  `FS_V526_CREW_SEAT = 1` puts body 2
# on the first builder after the lead, which is what the double-ferry probe did
# (its second `# PROBE:` sacrifice, "crew seat moved 3->1 for an r1 spawn") and
# what "riders launched as spawned, eco in PARALLEL not in front" means in this
# roster.  ⛔ AND IT IS NOT AN ECO SEAT BEING SPENT: `LOKI_ECO_SEATS = (1,2,3)`
# with seat 3 removed by the crew branch gives the parent an effective eco pool
# of {1,2}; moving the crew to seat 1 gives {2,3}.  SAME COUNT, one seat later.
# The harvester-at-r30 census is this build's measured check on exactly that.
# ⛔⛔ v527 RE-CONFIGURED THE PARENT: `FS_V526_TEMPO = False`.  The v526 build
# report (docs/research/BUILD-REPORT-v526transit-2026-08-18.md §6) measured this
# plank ALONE at k<=200 **-10.83pp OUTSIDE**, median kill 173 -> 237, replicated
# across two seed blocks; the composite failed DEFENCE_ADMISSION_BAR.  Only M3
# (`FS_V526_RDV`) was ADOPTED.  ⇒ v527's parent is "v525 + RDV", and that is
# this line, not a rebuild.  The constants below are left in place so the
# routing stays greppable and so `FS_V526_TEMPO = True` reproduces v526 as
# fired for any future re-test; nothing reads them while TEMPO is False
# (`fs_crew_seat()` / `fs_muster_wait()` fall through to FS_CREW_SEAT = 3 /
# FS_MUSTER_WAIT = 8, the v525 values).
FS_V526_TEMPO = False       # ⭐ v527: DISABLED.  See the block above.
FS_V526_CREW_SEAT = 1       # was FS_CREW_SEAT = 3.  Read ONLY through
                            # `fs_crew_seat()`.
FS_V526_MUSTER_WAIT = 3     # was FS_MUSTER_WAIT = 8.  The BACKSTOP, not the
                            # mechanism: with body 2 born at r2 the muster
                            # closes on proximity, and this only decides how
                            # long a lead waits for a body 2 that DIED or was
                            # never appointed.  8 was sized against a seat-3
                            # spawn; at seat 1 it is 5 rounds of dead rush.

# ⭐ M3 -- THE RENDEZVOUS.  Magnus's marker 3 ("Why does both raiders build one
# launcher each?"): body 2 misses the first throw envelope, `FS_RELAY_PATIENCE`
# expires, and it degrades to its own parallel chain -- double launchers, double
# Ti, and (marker 10) the third launcher priced +40% over the first on the ONE
# GLOBAL additive scale factor, inflating the sentinel the rush exists to buy.
#
# ⛔ THE OBVIOUS FIX IS ALREADY REFUTED AND IS NOT WHAT THIS IS.  The probe
# measured lead-follow (body 2 walks to the lead) NEGATIVE at n=6: it occupies
# the lead's forward build tile and two-throw links went 2 -> 0
# (`VARIANT-lead-follow.patch`).  This is the probe's own named next candidate:
# HOLD STATION, plus a VETO on the tile the lead is about to build on.
#
# What the parent does during the muster, and why it is the drift: with no
# launcher on the board `_fs_relay_point` returns None, `may_build` is False, so
# body 2 falls through the whole ferry branch to `self.tgt = T; self._nav(...)`
# -- IT WALKS AT THE ENEMY CORE while the lead stands still waiting for it.
FS_V526_RDV = True
FS_V526_VETO = True         # ...and if body 2 is standing ON one of the lead's
                            # forward build candidates, it steps OFF rather than
                            # holding -- the exact failure lead-follow produced.
FS_V526_RDV_PICKUP_DSQ = 2  # the step-off destination is scored on staying
                            # inside a future launcher's pickup envelope.

# ⛔ M4 -- ROOT-CAUSED AND **NOT SHIPPED**.  The mandate is explicit: fix only if
# the cause is in the transit subsystem.  IT IS NOT.  24 instrumented games on
# the wall-heavy 30x30 class (`scratchpad/s51_v526_build/rc3/`, `stallscan2.py`)
# give 13 mid-map stalls of >= 8 rounds and **0 of 13 involve a ferry/siege
# body** (`fs 0`, roles `expand`/`defend` in 13 of 13).  The reproducer of
# Magnus's "(8,10) r32 tries to go around, why did it stop?" is
# `valkyrie_s1_A` id 7 at (9,10), r37-r59, and the tape names the mechanism:
#
#   RC WALK 36 ... pos 9,10 tgt 9,10 want NORTH  verdict moved
#   RC WALK 37 ... pos 9,10 tgt 9,9  want CENTRE verdict centre   (x23)
#
#   * (9,9) is ORE (`map_encode`: env 2) and is occupied by OUR OWN home
#     defender, which is parked on its post and never leaves.
#   * `_expand`'s adjacent-ore override re-targets any 8-neighbour ore tile with
#     no BUILDING on it -- a BODY is not a building -- so `self.tgt` is forced
#     back to (9,9) every round, defeating the `stuck >= 5` re-pick (which walks
#     `ore_cursor` and WOULD have returned a different tile).
#   * `_bfs_direction` then returns CENTRE **correctly**: the target tile is
#     blocked, its cardinal neighbours become the goals, and `start in goals` is
#     the arrival-by-adjacency convention every build in this bot depends on.
#   * `can_build_harvester` is False while a body stands there, so nothing is
#     ever built and nothing ever changes.
#
# ⇒ TRANSIT IS BEHAVING TO SPEC; the absorbing state is the ECO layer's
# ore-adjacency override having no body test.  Fixing it here would be an
# out-of-scope change to the economy inside a transit build.  ROUTED, not fixed.
FS_V526_WALK = False        # ⛔ NEVER SHIPPED, and it is not a placeholder: the
                            # cause is out of subsystem (see above).  Kept as a
                            # named constant so the routing is greppable.

FS_V526_LOG = False         # V526: stderr instrument lines (HOP / THROW /
                            # TEARDOWN / RDV), off in the fired build.


LOKI_FS_V526 = True         # master.  False == `bots/_v525flip` unchanged.


def fs_crew_seat():
    """⭐ THE READ SITE FOR THE SUPPORT SEAT.  Never a module-level default."""
    if LOKI_FS_V526 and FS_V526_TEMPO:
        return FS_V526_CREW_SEAT
    return FS_CREW_SEAT


def fs_muster_wait():
    """⭐ THE READ SITE FOR THE MUSTER BACKSTOP.  Never a module-level default."""
    if LOKI_FS_V526 and FS_V526_TEMPO:
        return FS_V526_MUSTER_WAIT
    return FS_MUSTER_WAIT


# =============================================================================
# LOKI-FS-V527 -- THE COLLAR.  s51, 2026-08-19.
# =============================================================================
# Parent: `bots/_v526transit` CONFIGURED RDV-ONLY (`FS_V526_TEMPO = False` at
# its definition site above, `FS_V526_WALK = False` unchanged).  That
# configuration IS the v526 report's adopted object: M3/RDV was measured
# benign-to-positive on every cell (wins +4.17, k<=300 +5.42, ARC_DUP 69->6)
# while M6/TEMPO carried a -10.83pp k<=200 regression alone, replicated across
# two seed blocks.  Parent digests: scratchpad/s51_v527_build/PARENT_FREEZE.md5
# (the v526 tree) and CHILD_AT_BIRTH.md5 (this tree before any v527 code).
#
# `LOKI_FS_V527 = False` reproduces that RDV-only parent EXACTLY.  Every read
# below is a RUN-time read at the point of use; NO module-level derived default
# reads any v527 name (the v515 finding-3 hazard, proved by `flagoff_ast.py`
# with its FERRY_HOME_ON positive control).
#
# THREE MECHANISMS, from Magnus's markers 5 / 11 / 14 and the v520-v526 line.
#
# -----------------------------------------------------------------------------
# ⭐ M1 -- THE BUNKER SWAP (`FS_V527_BUNKER`).  Magnus, marker 11, verbatim:
# "(19,18) r28 builders walled in themselves; switching to sentinels is
# probably not good"; and marker 14: "maybe it should plant sentinels?".
#
# A ring raider that is TRAPPED (no legal cardinal move) or standing at a
# completed collar has spent its mobility and has nothing left on the ladder.
# Its own barrier is the asset: destroy it, and build a CORE-AIMED SENTINEL in
# the freed slot.  A ring seat occupied by our SENTINEL is still a denied seat
# (the census counts any building of ours), so the collar does not open -- and
# a sentinel's ray ignores obstacles, so it shoots the core through the rest of
# the ring.
#
# ⛔⛔ IT FAILS CLOSED, AND THAT IS THE PLANK'S FIRST CLAUSE, NOT ITS CAVEAT.
# Magnus's r28 archipelago state is the REGISTERED NEGATIVE: 6v12 conveyors,
# 100v130 collected, bloated scale, an unclosable collar.  Converting a barrier
# into a sentinel there is a hail mary, and the answer is HOLD-AS-DENIAL.  The
# swap therefore inherits ruling 2's economy gate WHOLE (`_fs_sentinel_ok`:
# the salt/eco disjunction, the collar reserve, the purchase cap, the ti floor)
# AND adds a MAGAZINE clause: the team ammunition balance must already sustain
# `FS_V527_MAG_SHOTS` sentinel shots.  Banked ammunition, not a promise to
# convert -- a turret that cannot fire is a 30 Ti barrier that costs 30 Ti.
#
# ⛔ AND THE SEAT NEVER FLICKERS.  Everything is validated BEFORE the destroy
# (`can_fire_from` on a real core tile, funds, gate, magazine), and if
# `can_build_sentinel` still refuses on the freed tile the SAME TURN rebuilds
# the barrier.  Worst case is one barrier's price and zero open-seat rounds;
# `v527_bunker_reseal` counts it and it must be small.
FS_V527_BUNKER = True
FS_V527_MAG_SHOTS = 3       # sentinel shots the global magazine must already
                            # cover (10 ammo/shot) before a swap may fire.
                            # THE FAIL-CLOSED HALF of Magnus's r28 ruling.
FS_V527_BUNKER_NEAR = 1     # swap also allowed at orth_open <= this when the
                            # body is not strictly trapped (a "completed or
                            # near-complete collar", marker 14's state).
FS_V527_BUNKER_MAX = 1      # swaps per body.  A body that has converted its
                            # barrier once is not a sentinel factory.

# ⭐ M1b -- THE DEFENDED-TILE PREFERENCE.  Magnus, marker 5: "(1,16) r36 perfect
# spot for a Sentinel, defended behind the Launcher already there".  The v514
# site scorer prices standoff, gun-axis and side redundancy and has NO term for
# our own standing pieces, so the tile his eye picked was never scored up.
# A site inside the pickup envelope of one of OUR launchers is a site whose
# attacker gets thrown off it (`can_launch` has no team check -- the evictor's
# whole point), so this is coverage in the same sense the collar census already
# credits.  ORDERING TERM, not a filter: it moves a tie, it never vetoes.
FS_V527_DEFENDED = True
FS_V527_DEFENDED_BONUS = 20  # d^2 units of the standoff score.  Sized BELOW
                             # FS_SENTINEL_GUNAXIS_PENALTY (64) so it can never
                             # buy a tile back onto a visible enemy gunner's
                             # ray, and BELOW FS_SENTINEL_SIDE_PENALTY (24) so
                             # it cannot collapse the twin onto one side.
FS_V527_DEFENDED_DSQ = 2     # a launcher's pickup envelope is d^2 <= 2,
                             # engine-read (docs/research/engine-source-crash-
                             # and-launcher-2026-08-10.md).

# -----------------------------------------------------------------------------
# ⭐ M2 -- THE PURCHASE SURVIVES THE RAIDER (`FS_V527_PSURV`).  Magnus, markers
# 4-8, on the 30x30 r684 loss: "(3,16) r51 seal-all-before-sentinel", and
# marker 14 on the r1000-harvesters loss: "where's the launcher at this core?"
# -- both games show the same signature, A SEALED ENEMY CORE WITH NO TURRET ON
# IT, held for hundreds of rounds.  The collar is the expensive half and it was
# PAID FOR; the turret that converts it was never bought because the body that
# would have bought it died, and nothing else in the tree owns that purchase.
#
# TWO CLAUSES, and the second is the cheap one:
#   (a) DISPATCH.  With the collar sealed-or-near, the gate open, NO forward
#       turret ever bought (`SLOT_FWD_GUN == 0`) and NO live ring body (both
#       crew beats stale), the Core prioritises a spawn and the body that takes
#       the seat runs TURRET-FIRST: rung 4 outranks rung 1 until one turret is
#       standing.  ⛔ NO NEW STORE CHANNEL -- every input is already published
#       (phase on SLOT_FS/FS_SUPP_SLOT, the purchase count on SLOT_FWD_GUN, the
#       crew beats on their own slots), so the body DERIVES the same condition
#       the Core did.  A channel nobody needs is the v523 arc-merge defect.
#   (b) BUY BEFORE THE FINAL SEAL.  At 7-of-8 seats with no turret ever bought
#       and the gate open, the TURRET OUTRANKS THE LAST BARRIER.  This is the
#       marker's own arithmetic: the last barrier is worth nothing until
#       something is shooting through the collar it completes, and `orth_open`
#       flickers, so "seal first" can defer the purchase indefinitely.
# ⛔⛔⛔ INCUMBENT GREP, RUN BEFORE THE CODE AND IT CHANGED THE PLANK.
# CLAUSE (b) AS MANDATED IS **ALREADY SHIPPED**, AND SO IS THE TURRET-FIRST
# HALF OF CLAUSE (a).  `_v518_early_sentinel` (siege.py, v518 change 2a) sits
# ABOVE RUNG 1 in the ladder and its entire guard is:
#     live <= FS_V518_EARLY_MAX_LIVE (= 0)
#     and _fs_sentinel_ok(...) and _fs_try_sentinel(...)
# -- i.e. "while no forward sentinel is alive and the gate is open, the turret
# outranks the barrier", unconditionally, at EVERY value of orth_open.
# The mandated clause (b) adds `orth_open <= 1` (STRICTLY NARROWER) and
# `SLOT_FWD_GUN == 0` (also STRICTLY NARROWER than `live == 0`: a sentinel
# bought and then killed reads live 0 with the monotone count at 1).  A guard
# that is the conjunction of a shipped guard with two extra tests can never
# fire on a round the shipped guard did not already win.  ⇒ BOTH ARE INERT BY
# CONSTRUCTION and shipping them would have measured a feature we already have
# (CLAUDE.md: "the cheapest null is a leg testing a feature we already ship").
# They are CODED, FLAGGED OFF and kept greppable so the finding is checkable
# rather than a claim; the byte-identity arm proves they cost nothing.
#
# ⇒ WHAT SURVIVES THE GREP IS THE HALF THE MARKER ACTUALLY NAMES: **there was
# no body**.  `FS_MAX_REPLACE = 2` caps raider replacements for the WHOLE
# match, and the marker game is a sealed collar held for hundreds of rounds
# with both replacements long spent -- so the shipped clause above is correct,
# funded, and has nobody to run it.  That is clause (a), and it is the only
# part of M2 this build ships.
FS_V527_PSURV = True
FS_V527_PSURV_LASTSEAT = False  # ⛔ clause (b): DOMINATED (see above).  Coded,
                                # flag-off, retained for the mutant that proves
                                # the domination rather than asserting it.
FS_V527_PSURV_TFIRST = False    # ⛔ the turret-first ORDERING: DOMINATED by the
                                # same clause, same argument.
FS_V527_PSURV_NEAR = 1          # "7 of 8": orth_open <= this would arm (b)
FS_V527_PSURV_DISPATCH = True   # ⭐ clause (a) -- THE ONLY SHIPPED HALF.
FS_V527_PSURV_EXTRA = 2         # replacements allowed BEYOND FS_MAX_REPLACE (2)
                                # while the PSURV state holds -- a sealed collar
                                # with no turret ever bought and no live ring
                                # body.  BOUNDED: the state is rare, the extra
                                # is small, and every ordinary spawn gate
                                # (budget, unit cap, cost, LOKI_SPAWN_RESERVE)
                                # still applies.  ⚠ THIS IS THE v526 M6 LESSON'S
                                # HAZARD CLASS -- a body is 78-105 Ti at live
                                # scale, so `harv30` non-regression is this
                                # plank's own falsifier, not a courtesy check.
FS_V527_PSURV_MAXRND = 900      # a dispatch after this cannot reach the ring;
                                # bounds the eco cost the v526 M6 lesson priced
                                # (a tempo change that moves an eco seat cost
                                # harv30 2.34 -> 1.98 and -10.83pp on k<=200).

# -----------------------------------------------------------------------------
# ⭐ M3 -- THE SEAL-PATH ORDER (`FS_V527_SEALPATH`).  Magnus, marker 14,
# verbatim: "(10,19) r21 builder blocked its way to the next barrier with this
# barrier".  Rung 1 takes the FIRST orthogonally-adjacent seat in the census
# order and the census orders on arc/NW/wear/distance -- there is no term for
# whether the barrier we are about to place is the tile we have to walk
# THROUGH to reach the seats we still owe.  On a narrow approach it is, and the
# collar then needs a full lap of the ring to finish, or never finishes.
#
# THE TEST IS A BOUNDED FLOOD, not a plan: with `t` treated as blocked, can the
# body still reach every other seat it owes?  Run over the ring + one tile of
# apron only (`FS_V527_PATH_DSQ`), so it is tens of cells, not the map.
#
# ⇒ Prefer an adjacent seat that does NOT cut.  If every adjacent seat cuts AND
# the sentinel gate is open, RUNG 1 STANDS DOWN THIS ROUND and the turret takes
# it -- marker 14's own opportunity-cost switch ("when the next seat requires a
# detour AND the gate is open, the turret outranks the walk").  If the gate is
# NOT open the parent's behaviour is unchanged: seal, and pay for the lap.
FS_V527_SEALPATH = True
FS_V527_PATH_DSQ = 20       # flood radius^2 around the enemy core.  The ring is
                            # d^2 <= 8 from the 2x2 footprint; 20 gives a full
                            # tile of apron for the walk-around without paying
                            # for a map-wide BFS in a 10ms turn.
FS_V527_PATH_SWITCH = True  # the opportunity-cost switch (turret over walk)

FS_V527_LOG = False         # V527: stderr instrument lines (BUNKER / PSURV /
                            # SELFCUT / SEALNT), off in the fired build.

LOKI_FS_V527 = True         # master.  False == the RDV-only parent unchanged.


# =============================================================================
# v529 -- THE MERGE (s51, 2026-08-20).  UNION OF `_v527collar` AND `_v528eco`.
# =============================================================================
# NO NEW MECHANISM.  This file is the mechanical three-way merge of two deltas
# that share one parent (`bots/_v526transit` configured RDV-ONLY,
# `FS_V526_TEMPO = False` at its definition site).  Verified before writing:
#   * v527's doctrine MINUS its constant block is AST-IDENTICAL to that base
#     (its two non-append hunks are COMMENT-ONLY: a v524 provenance correction
#     and the TEMPO=False rationale).  Same for v528.  ⇒ neither child edited a
#     single executable statement of the shared base.
#   * the two constant blocks assign 19 and 14 names with ZERO intersection and
#     ZERO shadowing of any base name.  ⇒ NO OVERLAPPING HUNK; nothing to
#     arbitrate.
# Text taken: v527's copy of the shared base (it carries the v524 doc
# correction), then v527's block, then v528's block below.  v528's variant of
# the TEMPO=False comment is the only thing dropped and it is a COMMENT on a
# line whose value is identical in all three trees; its rationale is preserved
# verbatim in docs/research/BUILD-REPORT-v528eco-2026-08-20.md.
# Flag-off of this tree = `LOKI_FS_V527 = False` AND `LOKI_FS_V528 = False`,
# which must reproduce the RDV-only parent byte-for-byte.


# =========================================================================
# v528 -- THE ECO BUILD (s51, 2026-08-20).  Parent: `bots/_v526transit`
# configured RDV-ONLY (FS_V526_TEMPO = False at its definition site, above;
# FS_V526_WALK already False).  v526's own build report measured M6/TEMPO
# carrying that build's entire regression alone, so the shippable object in
# the parent tree -- and therefore the baseline here -- is FS_V526_RDV alone.
#
# ⛔ FILE DISCIPLINE.  Every v528 change lives in `eco.py` and in this block.
# `main.py`, `raid.py` and `siege.py` are BYTE-IDENTICAL to the parent, so a
# merge with the sibling v527 build (which owns those three files) is a
# mechanical union with no overlapping hunk.
#
# ⭐ READ-SITE ONLY.  Nothing below is folded into a module-level default; every
# flag is read inside the branch it guards, so `LOKI_FS_V528 = False` reproduces
# the parent without any other edit.  `flagoff_ast.py` asserts this with a
# positive control.
# =========================================================================

# --- M5 -- CONNECTION-COST ORDERING (Magnus marker 9) --------------------
#
# VERBATIM: "(18,15) r44 Why did we prioritise this Harvestor, when (27,22) was
# two conveyors from a quick connection?"
#
# THE PARENT'S CHOOSER, exactly: `_pick` sorts every ore on the map by
# `abs(dx)+abs(dy)` to our Core plus a hash tie-break, partitions the result
# round-robin among 2 (small map) or 4 (large map) worker seats, and then walks
# its own slice with a monotonic `ore_cursor`.  Two properties of that:
#   * the rank is MANHATTAN distance, which on a wall-heavy board is not the
#     length of any route a conveyor can actually take -- an ore 6 tiles away
#     around a wall spur costs 14 links, and an ore 9 tiles away in open ground
#     costs 9;
#   * EXISTING belt is worth nothing to it.  An ore two tiles off a live trunk
#     ranks below a virgin ore one tile nearer the Core, even though the first
#     delivers in three rounds and the second in eleven.
# Neither is the quantity the tiebreak ladder pays for.  `titanium_collected`
# counts DELIVERY TO THE CORE, so the quantity is ROUNDS-TO-FIRST-DELIVERY.
#
# WHAT REPLACES IT: a single 0-1-2 cost flood outward from the Core's own
# delivery ring (`_link_goals`) over the same padded flat grid and the same
# blocked set `_link_path` routes on -- so the number the scorer reads is the
# number the router will actually have to build.  Stepping into a tile that
# already holds one of OUR belt pieces costs 0 (it is built); an empty tile
# costs 1; a contested tile costs 1 + V528_CONN_CONTEST.  Ore is impassable to
# the flood exactly as it is impassable to `_link_path`.
#
# ⛔ THE MYOPIA GUARD IS STRUCTURAL, NOT A DIAL.  The scorer only ever RE-ORDERS
# this seat's existing candidate list; it never truncates it and never drops a
# candidate.  An unreachable ore scores V528_CONN_UNREACH -- large, and FINITE,
# so once the near ore is taken (its tile carries a building and the existing
# occupancy skip fires) the far ore is still chosen.  Quick-connect greed can
# reorder the queue; it cannot cap it.
FS_V528_CONNCOST = True

V528_CONN_W_LINK = 3        # rounds charged per NEW conveyor on the route home.
                            # One build round (build+cooldown) + one round of
                            # stack transit over that tile.
V528_CONN_W_WALK = 1        # rounds charged per step this body must walk to
                            # reach the ore.  This is the parent's implicit and
                            # ONLY term, kept so the new score is a superset.
V528_CONN_CONTEST = 2       # extra step cost for a tile the flood judges
                            # contested: a standing body of either team, or a
                            # visible enemy building's orthogonal neighbour.
V528_CONN_UNREACH = 400     # score for an ore the flood cannot reach.  FINITE
                            # ON PURPOSE -- see the myopia guard above.
V528_CONN_REFRESH = 12      # rounds between field recomputes.  The field is
                            # also invalidated when this body's own trunk chain
                            # completes, since that is when new belt appears.
V528_CONN_MAX_CAND = 24     # candidates scored per `_pick` call.  `_pick` is
                            # called only when the target is reached, missing or
                            # stale, so this is a CPU ceiling, not a cadence.
V528_CONN_NODE_BUDGET = 1400  # hard cap on flood nodes, as LINK_NODE_BUDGET.
V528_CONN_BAN_RNDS = 25     # ⭐ THE ANTI-LOCK, and it is not optional.  The
                            # parent's `ore_cursor` rotates on every call, so a
                            # permanently unbuildable tile costs it one round.
                            # A SCORER IS DETERMINISTIC and would hand the same
                            # tile back forever -- the M4 failure wearing a
                            # different hat.  When `_expand` re-picks BECAUSE
                            # the body is stuck, the tile it was stuck on is
                            # banned for this many rounds.  If the ban would
                            # empty the candidate list, it is DROPPED, not the
                            # candidates.

# --- M4 -- THE STALLED WALKER (Magnus marker "(8,10) r32 ... why did it stop?")
#
# ROUTED HERE BY v526, which root-caused it OUT of transit (13 mid-map stalls
# over 24 wall-heavy 30x30 games, 0 of 13 involving a ferry/siege body) and
# named the absorbing state precisely: `_expand`'s adjacent-ore override
# re-targets any 8-neighbour ore tile carrying no BUILDING -- and A BODY IS NOT
# A BUILDING.  With our own home defender parked on the ore at (9,9), `self.tgt`
# was forced back onto it every round, which defeated the `stuck >= 5` re-pick
# (that re-pick advances `ore_cursor` and WOULD have returned a different tile),
# and `can_build_harvester` is False for as long as the body stands there.
# `valkyrie_s1_A` id 7 held (9,10) from r37 to r59 on exactly this.
#
# THE FIX IS ONE PREDICATE: a tile occupied by a builder bot of EITHER team is
# not a valid re-target.  The override then declines, `self.tgt` keeps whatever
# the re-pick returned, and the body walks.
FS_V528_WALK = True

# --- OPTIONAL -- `_wire_tick`'s ORPHANED CHAIN HEAD ----------------------
#
# Open item 5 of BUILD-REPORT-v513siegecrew: once `SIPHON_WIRE_RNDS` elapse,
# `_wire_tick` assigns `self.link_queue = path` OVER a live queue, so every
# unbuilt tile of the chain in progress is dropped.  The harvester that chain
# was for keeps emitting into nothing -- and `titanium_collected` counts
# delivery, so that harvester is worth 0 on key 1 forever.
#
# ⭐ THE FIX IS A DEFER, NOT AN APPEND.  Concatenating the two paths would put a
# seam in the queue, and `_build_next_link` reads `link_queue[1]` to face the
# tile it is building: at the seam it would face the last link of chain A at the
# first tile of chain B.  That link is the one beside our own Core footprint --
# v513 change C measured perfect separation on it (`titanium_collected` > 0 iff
# a conveyor of ours stands beside our Core).  Mis-facing it is a worse bug than
# the one being fixed.  So: hold the pending item, refresh its clock, and let
# the live chain drain.  Bounded by V528_WIRE_MAX_DEFER so a permanently stuck
# chain cannot starve the queue -- past the bound the parent's clobber returns.
FS_V528_WIRE = True
V528_WIRE_MAX_DEFER = 4     # deferrals before falling back to parent behaviour.

FS_V528_LOG = False         # stdout instrument tapes (CONN / WALK / WIRE), off
                            # in the fired build; the instrumented arm sets it.


LOKI_FS_V528 = True         # master.  False == `_v526transit` RDV-ONLY exactly.


# ============================================================================
# LOKI-V534 "MAPTRUST" (2026-08-20, s52) -- KILL THE TWO FALSE-MATCH HAZARDS.
# ============================================================================
#
# ⭐ PORTED VERBATIM INTO `_v536trustport` (2026-08-21, s52) OFF `_v529merge`.
# v534 built this on `_v533home`, i.e. on top of the v530-v533 HOME PACKAGE.
# v536 re-sites the SAME changeset onto the clean `_v529merge` chassis and
# carries NO home package: eco.py's and siege.py's maptrust hunks applied at
# identical context (siege.py is byte-frozen since v529; eco.py's
# `known_map_for` region is byte-identical across both parents), and THIS
# doctrine block is an append whose only adaptation is the wording below --
# no constant, no flag and no code line differs from v534.  The build report
# is docs/research/BUILD-REPORT-v536trustport-2026-08-21.md.
# Queue #99, from docs/research/AUDIT-map-hardcoding-2026-08-20.md, commissioned
# on Magnus's finals concern: "if we are going to try and win the final that are
# on maps that havent been announced yet we might need to make tactics that
# arent too hardcoded to the maps we see now".
#
# ⭐ THE AUDIT'S OWN HEADLINE IS THAT THE HAZARD IS **FALSE MATCHING, NOT
# MISSING**.  A genuinely unseen map degrades SANELY everywhere in this tree:
# `known_map_for` -> None routes to the live-vision ore scan and the spiral
# search, `_bfs_direction` falls back to a cardinal step, an FS_MAP_SKIP miss
# means ferry-siege runs.  What is NOT sane is a finals map that COLLIDES with
# a catalogued signature and is therefore handed somebody else's terrain.
# Both exposures below are that: a tuple of integers standing in for a map.
#
# ---------------------------------------------------------------------------
# F1 -- `known_map_for` ADOPTED A SINGLETON WITH ZERO TERRAIN VERIFICATION
# ---------------------------------------------------------------------------
# The parent's function tested only `(width, height, our core anchor)` against
# ~31 catalogued signatures and, when exactly ONE matched, returned that stored
# grid outright: the sensed-tile comparison ran only at >=2 candidates, and
# even then returned the CLOSER known grid, never None.  So a finals board
# sharing dims and a core anchor with any one of the ~29 singleton signatures
# silently corrupted `map_walls` / `map_ores` / every pathing template for the
# WHOLE match -- cached once (main.py's `if self.map_grid is None:`), never
# re-checked.  Recurring dims (20x20 / 24x24 / 26x26 / 30x30) make that a live
# risk, not a theoretical one.
# THE FIX (eco.py `_maptrust_pick`): verify EVERY match, singleton included,
# against currently-visible tiles, and return None the moment a candidate
# disagrees with terrain we have actually looked at.  A disagreement is only
# TRUSTED on a building-free tile, so nothing our own team builds can refute the
# correct grid.
# ⛔ NOTHING IS MEMOISED -- NOT REFUTATIONS, NOT POSITIVE VERDICTS.  v534's first
# draft cached refutations under (w, h, anchor) and thereby reintroduced the
# collision bug INSIDE the collision fix (that key is precisely the thing which
# does not identify a map); `bots/_v534maptrust/eco.py`'s own header and the
# v534 build report 7.1 carry the account, and this doctrine paragraph is the
# ONE place in v534 that was never updated to match the shipped code.  Corrected
# here rather than ported forward.  Re-verifying on every ask is also what buys
# opportunistic re-verification as a unit's vision widens, for free.
# ⚠ THE RESIDUAL, STATED PLAINLY: verification is over VISIBLE tiles, so at r0
# it is partial (core vision r^2=36).  A colliding map that also matches the
# catalogue across the whole visible window is still adopted.  This narrows the
# hazard, it does not close it.
#
# ---------------------------------------------------------------------------
# F2 -- `FS_MAP_SKIP` WAS A BARE-SIGNATURE TEST
# ---------------------------------------------------------------------------
# `siege.py`'s gate did `if sig in FS_MAP_SKIP: ok = False` on five loose
# (w, h, both anchors) tuples with no terrain confirmation at all, so a board
# merely COLLIDING with one of them lost ferry-siege for the entire match with
# no tell -- and ferry-siege is the plank the programme spends its kill on.
# THE FIX is the SAME MECHANISM v524 CHANGE 1 already applies to the cripple
# list one clause below: a coarse signature hit is demoted to a CANDIDATE and
# confirmed against the actual tile grid.  On signature-hit-but-terrain-
# mismatch the board is treated as NO MATCH, i.e. an unsurveyed map, and the
# registered default for an unsurveyed map is that ferry-siege plays normally.
#
# ⭐⭐ AND F2 SURFACED A LIVE DEFECT INSIDE OUR OWN CATALOGUE, WHICH IS THE
# SURPRISE OF THIS BUILD.  The `(28, 20, (7,9), (19,9))` entry is commented
# `# heart` and comes from the closure survey
# (docs/research/BELT-ON-SEATS-SURVEY-2026-08-17.md), whose own classification
# reads **"SKIP: lighthouse 0.0, saga 1.0, moonrise 2.2, heart 2.3, snowflake
# 3.4, archipelago 3.9. Marginal: meander/atoll/antler/hive/EIDER 5.7-8.8"**.
# But EIDER SHARES HEART'S SIGNATURE EXACTLY -- both are catalogued at
# `(28, 20, 7, 9, 19, 9)` in EXTRA_MAP_CODES -- so the bare-signature test has
# been standing ferry-siege down on eider too, against the survey that
# authored the set.  Confirming by grid ends that: only heart's terrain
# confirms this entry, so **eider flips from SKIP to RUN**.  That is a
# deliberate behaviour change, it is the F2 defect class with a map we happen
# to own, and it is FREE ON THE CURRENT POOL because eider is not in it (the
# 15 live maps are nordkap fjordgate antler archipelago drumlin midgard
# glacierkeep yulerune drakkarfjord frostgate icefloe ragnarok royale valkyrie
# auroraveil).  If a finals pool brings eider back and the marginal 5.7-8.8%
# band is judged too thin, the answer is eider's OWN entry with eider's OWN
# grid, never a signature standing in for two maps.
# ⭐ snowflake AND archipelago genuinely share `(26, 26, (5,5), (19,19))` and
# are BOTH surveyed as SKIP, so that entry registers BOTH grids and the shared
# treatment is preserved exactly -- which matters, because archipelago is the
# only FS_MAP_SKIP map in the current pool.
#
# THE CODES BELOW ARE NOT RETYPED, AND v536 DID NOT RETYPE THEM EITHER -- they
# are the v534 block's own bytes, diff-verified.  `scratchpad/s52_v534_build/
# gen_doctrine_block.py` emits them from `tools/map_encode.py`'s encoder and
# refuses unless every one is ALSO found verbatim in the parent's own tables,
# with the two shared-key pairs still distinct; its `--selftest` drives that
# checker to both verdicts on three mutants.
#
# READ-SITE ONLY, same convention as the v524/v528 blocks: every name below is
# read inside the branch it guards, so `FS_V534_MAPTRUST = False` reproduces
# `_v529merge` byte-for-byte.  The v536 flag-off audit asserts it (AST scan +
# NOISE_OFF identity games).
FS_V534_MAPTRUST = True     # master.  False == `bots/_v529merge` unchanged
FS_V534_LOG = False         # stderr tape for the F2 confirmation
FS_V534_MIN_TILES = 8       # verified tiles below which `known_map_for`
                            # refuses to adopt at all.  A degenerate ask (a
                            # unit with no vision yet) must not adopt a grid on
                            # ~nothing; the caller simply asks again next round.
                            # Measured never to bind on any pool or invented
                            # map: the sparsest legal core/builder stance still
                            # sees far more than this (see the build report).

FS_V534_LIGHTHOUSE_CODE = "ENAAJEMBAAEAASNMEASMBNAACAJBAAAMHJAAAAAAACYACAAAAAADSNAAAAEAACAMBNGAJNMHAAJBAANJEAAMKB"
FS_V534_SAGA_CODE = "ENNBCMAMBNJBAAAACAAAAAAAEADAAMCMEADGJNNMEADAJNNMBAJBYIAABNJBSACAEAESAMAMEAWGAMAMBAACJKDJAASAIGAJBAGYACAABDKBSAAJEAEAGOAMEAEACMAMASACJBNJAAYIJBAJENNBADAMENNBGDAMESEAADAMAAAAAAASAAAAJBNJEAESJNNM"
FS_V534_MOONRISE_CODE = "JABAJABDDDGDDDJAAAAABDAAAAADGAAAAAGAAAUAAAJJAGABBHDDADDP"
FS_V534_HEART_CODE = "AAAAAAAAAAAAACSAAAAAAAAAAAAAAAAMAMAAAAAAMBJEAAAAANW0NEAAAJNNBNNEAAANNAANNAAADAAAAABAAAAAAAAAAAABAAAAJAACAAAAAAAGANNBAANNBAMNNBJNNEAJANWSNEJAATANCOBGBALAJBJBATAADAEAEABAASJEAJEGAYAGSGGCGAI"
FS_V534_SNOWFLAKE_CODE = "AAAAAAAAAACAAAAAAGGAJADAAAAAMEANBACAAAAAJBASAAAAGJBAGAAGAAMTAJAAAAJJBAFABAABJSABABADSDSMAABJAAEAASAAAAAASAAAAAASAGAAAAAAGAAAAAAGAAJBADABAMGJGJAABABGDABAABJCAEDAAAADAGNAASAASAAESAAAAGAAEAAAAAACANBJNAAAAAJADASSAAAAAAACAAAAAAAAAA"
FS_V534_ARCHIPELAGO_CODE = "ENNEANNENJEMBJNNKBSAAAAMAMEAEACAAAJBAAAAAAAMAAAGCMAMZBJEGNNENJAMBJNNKNCMYAAAAGEAESGSAAJBJBIAJBJBAGASAJAJAMASADAAAAAJAGAMADADAGASAAEAEASCEAEAAGSGJBJTAAAAYMAOENNEANADMKNNTJEAZNAMAUAAAMAAAAAAAAEAAAACJBJNAMAAAAGAENNEANJEMKNNBJNNKB"

FS_V534_SKIP_CODES = {
    (16, 16, (3, 3), (11, 11)): (FS_V534_LIGHTHOUSE_CODE,),
    (24, 24, (4, 4), (18, 18)): (FS_V534_SAGA_CODE,),
    (21, 8, (5, 3), (14, 3)): (FS_V534_MOONRISE_CODE,),
    (28, 20, (7, 9), (19, 9)): (FS_V534_HEART_CODE,),
    (26, 26, (5, 5), (19, 19)): (FS_V534_SNOWFLAKE_CODE, FS_V534_ARCHIPELAGO_CODE),
}


# ======================================================================
# LOKI-V537 "SOCKET" -- CLAIM OUR OWN DELIVERY SEAT BEFORE THEY BRICK IT
# ======================================================================
# PORT HEADER.  Parent tree: `bots/_v536trustport` (which is `_v529merge` +
# the v534 MAPTRUST changeset).  This block adds ONE plank and nothing else.
# Build report: docs/research/BUILD-REPORT-v537socket-2026-08-21.md.
#
# THE DEFECT, measured on 2,700 local games against `bots/_x3r0v169mjolnir`
# (docs/research/DIFF-STUDY-v169-craters-2026-08-21.md, Q2 steps 1-5):
#
#   * Our belt on the crater maps is NEVER CUT.  Median conveyor loss on
#     glacierkeep is 0% of 34 built; our harvesters live; and we still finish
#     89% of glacierkeep games and 52% of drakkarfjord games with
#     `titanium_collected` = 0.  The belt is not severed -- it never CONNECTS.
#   * The missing tile is one of the 8 tiles orthogonally beside our own 2x2
#     Core, the only tiles a conveyor can deliver into it from (`heal_seats`).
#     Mjolnir's collar barriers hold 6.56-6.84 of our 8; we hold 0.14-0.46.
#   * Ring-plug asymmetry vs win rate: Spearman rho = 0.925 over 15 maps.
#   * The dose is monotone and has a MECHANICAL hard zero -- 0 usable seats
#     => 0 of 119 games delivered anything, 9% won; 3+ seats => 73-75% won.
#   * And it is a RACE WE LOSE ON A CLOCK.  Mjolnir puts a conveyor on its own
#     Core seat at ROUND 2 ON 15 MAPS OUT OF 15, unconditionally.  We do it at
#     r2-r8 where the ore is close, at r23 on drakkarfjord, r230 on
#     glacierkeep, and NOT AT ALL in 86% of glacierkeep games.  Their first
#     plug on our ring lands at r13-r16.
#   * The cause is BUILD ORDER.  `_link_path` plans ore-end-first and
#     `_build_next_link` drains `link_queue[0]` first, so the seat is the LAST
#     tile of the trunk.  On the only two pool maps whose nearest ore is 10-11
#     tiles away, "last" arrives after their barrier does.
#
# THE PLANK, and it is deliberately the smallest thing that moves the clock:
# put ONE conveyor on ONE of our own delivery seats by round FS_V537_BY_ROUND,
# UNCONDITIONALLY -- not gated on ore distance, not on a harvester existing,
# not on a route being planned.  3 Ti and one builder turn.  The trunk still
# plans and drains exactly as before; when it arrives, `_build_next_link`'s
# own `if occupied: pop` branch walks over the seat we already hold, so the
# belt terminates on our claim.  The seat becomes the FIRST tile of the trunk
# instead of the last, which is the whole of "core-outward" that the measured
# defect actually needs: conveyor loss in the middle of the trunk is 0%.
#
# ⛔ PREVENTION, NEVER EVICTION.  Nothing here attacks their plug.  Their
# barrier is 30 HP = 15 builder pecks at 2 Ti = 30 Ti and 15 turns per seat;
# claiming first is 3 Ti and one turn -- a 10x price difference.  Because the
# plank touches only OUR OWN ring it carries no PLUG-RULE exposure, no forward
# body recall, and none of the s51 collar tar-pit constraint
# (docs/research/AUTOPSY-crater-vs-sweep-2026-08-20.md), which governs THEIRS.
#
# ⛔ NOTHING IS LATCHED AND NO STORE SLOT IS SPENT.  How many seats we hold is
# re-derived from the engine every call by reading the ring.  A latch would go
# on claiming "done" after they shoot the conveyor off the seat; a store slot
# would cost one of 16 for a fact the map already carries.  The window is what
# bounds the work, not a flag.
#
# READ-SITE ONLY, same convention as the v524/v528/v534 blocks: every name
# below is read inside the branch it guards, so `FS_V537_SOCKET = False`
# reproduces `bots/_v536trustport` byte-for-byte.  The v537 flag-off audit
# asserts it (AST scan + read-site scan + NOISE_OFF identity games).
FS_V537_SOCKET = True       # master.  False == `bots/_v536trustport` unchanged
FS_V537_LOG = False         # stderr tape for the claim; OFF in competition
FS_V537_BY_ROUND = 4        # the claim window closes after this round.  The
                            # study's constraint is "by r4"; their first plug
                            # lands r13-r16, so r4 is nine rounds of margin.
FS_V537_MAX_SOCKETS = 2     # ⚠ BOUNDED AT TWO.  The Core spawns builders on
                            # its adjacent tiles, so taking the ring starves
                            # the spawn ring.  Two of eight leaves ten of the
                            # twelve spawn tiles, and matches the existing
                            # HS_DELIVERY_SEATS = 2 reservation exactly.
FS_V537_SIDE_SPREAD = True  # seat #2 must sit on a DIFFERENT side of the Core
                            # than seat #1 -- a conveyor is 20 HP and a peck is
                            # 2 damage, so two seats on one side die together.
FS_V537_RAIDER_CLAIMS = True
                            # May seat 0 -- the r0 body, which LOKI-FERRY-SIEGE
                            # forks into THE RAIDER -- spend its first turn on
                            # the claim?  `True` is the study's spec read
                            # literally ("UNCONDITIONALLY"), and it is what
                            # ships.  The knob exists because the v537
                            # mechanism test found a cost exactly where there
                            # was no defect to fix: on the two (map, seat)
                            # cells where the PARENT already claimed early
                            # (auroraveil seat A r22, drakkarfjord seat B r23)
                            # the plank LOST 5-6 games of 30, while gaining
                            # 20-25 of 30 on every cell where the parent never
                            # claimed.  Both arms are measured in the build
                            # report; neither is asserted here.


# ======================================================================
# LOKI-V538 "CLAIM GATE" -- THE SOCKET CLAIM STANDS DOWN ON REFUSING BOARDS
# ======================================================================
# PORT HEADER.  Parent tree: `bots/_v537socket`.  This block adds ONE gate and
# nothing else.  Build report:
# docs/research/BUILD-REPORT-v538refine-2026-08-21.md.
#
# THE DEFECT, measured on the v537 screen vs `bots/_x3r0v169mjolnir`
# (BUILDER s52, 2026-08-21, full-pool): v537 read 56.67 [53.43, 59.90] and MET
# the release bar -- while ARCHIPELAGO COLLAPSED FROM 35/60 TO 8/60.  That is
# the v537 build report's own §6 surprise arriving on a different surface: the
# claim spends a builder turn at r1 UNCONDITIONALLY, and on boards where that
# turn was already doing something that mattered, the trade is bad.
#
# THE MECHANISM STORY, stated so it can be falsified rather than told: the
# claim is worth its turn where the ORE IS FAR and the trunk therefore reaches
# our own delivery seat late or never.  It is NOT worth its turn on boards the
# FERRY-SIEGE ITSELF REFUSES -- boards whose geometry already told us the
# forward plank does not pay there, where the r0 body is playing the incumbent
# raid doctrine and its first turn is not spare.  archipelago is one of exactly
# two such boards in the current pool.
#
# ⛔ AND THE PREDICATE IS THE GEOMETRIC ONE, NOT A MAP LIST.  No map name
# reaches a bot and the map-robustness policy (F3) forbids named-map
# special-casing outright, so this gate reads THE SAME VERDICT the siege gate
# already computes -- `SiegeMixin._fs_map_gated`, via the `_v535_map_refuses`
# reader ported from `bots/_v535cornergate` for this build.  On the CURRENT
# 15-map pool that verdict enumerates to {archipelago (FS_MAP_SKIP,
# grid-confirmed since v534), midgard (cripple)}; the enumeration is a
# MEASUREMENT (build report §3), not a definition, and it moves when the pool
# or the floors move.
#
# ⚠ MIDGARD IS GATED TOO, AND THAT IS DELIBERATE AND IT COSTS SOMETHING.
# v537's screen read midgard 37/60 against v536's 36 -- a GAIN, well inside
# noise at that n.  Gating the principled predicate gives that up.  The
# alternative -- gate archipelago alone -- requires a named-map list, which is
# the thing the policy forbids and the thing that does not generalise to a map
# we have not seen.  So BOTH refusing boards stand down and the powered screen
# adjudicates.  If midgard's cell falls outside noise, THAT is the finding.
#
# ⭐ THIS IS THE v535 PATTERN, APPLIED TWICE NOW.  `FS_V535_CORNER_GATE` stood
# the home package's corner barriers down on refusing boards for the same
# reason: a plank designed against a SIEGE-BOARD picture, fired map-invariantly,
# carries its deficit on the boards the siege declined.  v535 measured that as
# -14.2pp, archipelago-concentrated.  The corner gate is NOT on this lineage
# (v537 descends v536trustport <- v529merge; v535 is a separate branch), so
# what is ported here is the READER only: `_fs_enemy_anchor` (an extraction, so
# there is ONE anchor resolution in the tree) and `_v535_map_refuses` (cache +
# sign flip over `_fs_map_gated`).  The corner plank itself is untouched and
# ungated on this tree.
#
# ⛔ CALLED, NEVER RE-DERIVED (D21d).  `_v535_map_refuses` contains no copy of
# the gate's tests, no map signature, no cripple list, no floor constant.  It
# CALLS `_fs_map_gated` and `_fs_enemy_anchor`.  The build report drives that
# structurally (AST) and behaviourally (the extracted `_fs_gate` vs the frozen
# parent's, on the engine).
#
# READ-SITE ONLY, same convention as v524/v528/v534/v537: every name below is
# read inside the branch it guards, so `FS_V538_CLAIM_GATE = False` reproduces
# `bots/_v537socket` byte-for-byte (AST scan + read-site scan + NOISE_OFF
# identity games, build report §5).
LOKI_FS_V538 = True         # master.  False == `bots/_v537socket` unchanged,
                            # and the siege reader is then never called at all.
FS_V538_CLAIM_GATE = True   # the gate itself: the v537 socket claim stands
                            # down on boards the ferry-siege REFUSES.
FS_V538_LOG = False         # stderr tape for the refusal verdict; OFF in
                            # competition.

# ==========================================================================
# LOKI-REESTABLISH (v539) -- THE ECONOMY COMES BACK AFTER IT IS KILLED
# ==========================================================================
# MAGNUS, watching the v174 rated loss to `lazy` (economy wiped by ~r100;
# harvesters 0 and bank 5 Ti at r154; nothing ever rebuilt):
#     "Do we have any logic to re-establish our harvesting if we are
#      attacked like this?"
# and, on the scope of the answer:
#     "maybe we shouldn't put effort into defending that much, we are an
#      offensive player, we just want to hold out until we have killed the
#      opponent.  The issue is that we don't seem to put a sentinel at all
#      in that game."
#
# ⛔ SO THIS IS NOT AN ECONOMIC-DEFENCE PLANK.  It is KILL REFUNDING.  The
# target is the MINIMUM economy that pays for a sentinel and its ammunition:
# ONE harvester whose belt reaches our own core.  Not the eco we lost.  The
# episode ENDS the moment titanium is seen arriving again -- delivery is both
# the trigger and the stop condition, so the cap is not a number somebody
# chose, it is the definition of "the kill is funded again".
# Admissible under PROGRAMME.md `PLAY_DEFENCE: not_at_the_kill_s_expense`
# only if it clears `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`;
# its battery is scored that way and nothing here asserts it has.
#
# --------------------------------------------------------------------------
# ⛔⛔ THE COMMISSION'S ROOT CAUSE IS HALF RIGHT, AND THE OTHER HALF POINTS
# THE OPPOSITE WAY.  READ THIS BEFORE TOUCHING `SLOT_HARVESTERS`.
# --------------------------------------------------------------------------
# TRUE: `SLOT_HARVESTERS` is a monotone high-water ratchet.  `_sync_harvesters`
# (eco.py) only ever raises it and the harvester bootstrap only ever adds one;
# no site in any ancestor of this file has ever lowered it.  After a wipe the
# slot reports harvesters that are dead, for the rest of the match.
#
# FALSE, and it is the load-bearing correction: "no rebuild path can trigger".
# Every consumer of the slot was enumerated for this build (build report §3,
# ten read sites).  The bootstrap that would rebuild -- eco.py `_expand`,
# `harv < self._eco_cap(ct)` -- is gated at ECO_CAP = 18, so a phantom 5 does
# not block it and never did.  What the phantom actually does to the OTHER
# nine sites is make them MORE permissive, not less:
#   * raid.py forward SENTINEL needs `SLOT_HARVESTERS >= LOKI_FWD_MIN_HARV`(2)
#   * main.py home LAUNCHER needs `>= 1`
#   * eco.py opportunistic PAVING needs `>= 1` and `>= 2`
#   * main.py counterbattery SKIPS its refusal when `>= ECO_NEED`
# ⇒ RESETTING THE SLOT TO AN HONEST 0 WOULD **CLOSE THE SENTINEL GATE THE
# PHANTOM WAS HOLDING OPEN** -- the exact opposite of what Magnus asked for
# in the same breath.  The honest-slot reset is therefore BUILT AND SHIPPED
# OFF (`FS_V539_HONEST_SLOT`), so a leg can measure it rather than a build
# assuming it.
#
# WHAT ACTUALLY STOPPED THE REBUILD IN THAT GAME -- two things, neither of
# them the ratchet, and both are what this plank fixes:
#   1. FUNDING.  `_eco_spendable` subtracts the collar reserve and, once
#      SLOT_UNDER is latched (50-round latch, and a bot that is being wiped is
#      under attack continuously), a further SIEGE_HEAL_RESERVE_TI.  On a bank
#      the wipe has drained, the economy's bar sits permanently above the
#      bank.  This is the v513 change-C deadlock in its second costume: a
#      reserve that cannot be funded protects nothing and starves everything.
#   2. ROSTER.  Roles are assigned ONCE per body from a monotone SLOT_ROLE_N
#      ordinal, and only `LOKI_ECO_SEATS = (1, 2, 3)` are economy.  Every
#      replacement body spawned after a wipe reads n >= 4 and becomes a
#      RAIDER.  Kill the three eco seats and the team has no expander for the
#      rest of the match, whatever the slot says.
#
# --------------------------------------------------------------------------
# THE DETECTOR -- DELIVERY DROUGHT, NOT A HEAD COUNT.
# --------------------------------------------------------------------------
# A live-vs-slot head count cannot be read honestly by anyone on this team.
# `_sync_harvesters` runs on BUILDERS (main.py, in the builder turn), whose
# vision is r^2 = 20 and who only sync within d^2 <= 64 of the Core, so any
# single body's count is a LOWER BOUND and a famine call on it fires whenever
# a body walks home past ore it cannot see.  That is why the ratchet is a
# ratchet: it is a UNION over partial views.  Do not replace a union with one
# of its members.
#
# What CAN be read exactly, every round, by exactly one unit, is DELIVERY.
# v514 already gave the Core `_fs_eco_mouth()`: a friendly conveyor/splitter
# orthogonally adjacent to our own 2x2 footprint, and whether it is HOLDING a
# stack.  The mouth is always inside Core vision, so the read never degrades.
# CLAUDE.md's own engine probe is the warrant: a harvester with no route home
# collected 0 for 998 rounds.  Delivery IS the economy; head count is not.
#   famine := FS_ECO_BIT_DELIV is latched (we have delivered at least once)
#             AND round >= FS_V539_MIN_RND
#             AND no `held` sighting for FS_V539_DROUGHT rounds
# A connected harvester puts a stack on the mouth one round in four, so a
# 25-round drought on a delivering belt is ~0 probability; a belt that is cut,
# a harvester set that is dead, and a mouth that has been shot off all read
# the same because they ARE the same to the tiebreaker and to the bank.
#
# ⛔ AND IT COSTS NO STORE SLOT.  All 16 are assigned.  The famine bit and the
# episode's start round ride bits 18 and 19-29 of FS_ECO_SLOT, whose SINGLE
# WRITER is already the Core (v514 change A).  One writer, one word, one
# write per round -- the r197 lost-update discipline is preserved exactly,
# which a second Core write to the same slot would NOT be: `read_store`
# returns the pre-round value, so two writes in one turn silently drop the
# first.  That is why the famine bits are folded into `_fs_eco_publish`
# instead of living in a tick of their own.
#
# --------------------------------------------------------------------------
# THE RESPONSE -- three rungs, each the smallest thing that unblocks one of
# the two real causes, and each self-cancelling when delivery resumes.
# --------------------------------------------------------------------------
#  A. LIFELINE (fixes cause 1).  While famine is young, an EXPANDER's eco
#     spend is exempt from the collar and siege reserves -- the same
#     `essential` lifeline v513 change C already grants the last link, for the
#     same reason.  Bounded THREE ways: expanders only (a raider's spending is
#     never waived), the first FS_V539_LIFELINE_RNDS rounds of an episode
#     only, and at most FS_V539_MAX_EPISODES episodes per match.  The bank is
#     never waived below the cost itself, so the waiver can only ever spend
#     income the wipe left us -- ~100 Ti over a 40-round window at passive
#     rates.  The collar's own 8-barrier reserve outlives that.
#  B. DRAFT (fixes cause 2).  A body whose role is being assigned WHILE
#     famine holds takes "expand" instead of "raid".  It touches no existing
#     raider -- a raider already at the enemy ring is NOT recalled, which is
#     the T4_BLEED lesson written down in this file ("recalling the whole
#     economy on a latch once finished a measured game with 0 titanium
#     delivered").  Only bodies that have not started yet are diverted, and
#     they hand themselves back the moment famine clears.
#  C. SEAT-3 HOLD.  Seat 3's one-way defection to the raid (`harv >= ECO_NEED`
#     on the RATCHET, i.e. on phantoms) is suspended while famine holds.  The
#     defection is not REVERSED: on a gated map seat 3 is the ferry-siege
#     support raider and pulling it out of a live crew mid-siege is a bigger
#     change than this plank is allowed to be.
# The rebuild itself is NOT re-derived: with funding and an expander in hand,
# the existing `_expand` bootstrap builds the harvester and `_wire_on_build` /
# `_build_next_link` lay the chain, exactly as they do in the opening.  This
# plank buys those two preconditions and nothing else.
#
# ⛔ THE OPENING CURVE IS UNTOUCHED, BY CONSTRUCTION AND TWICE OVER: famine
# cannot be declared before FS_V539_MIN_RND, and it cannot be declared until
# the belt has delivered at least once.  A bot that has not yet delivered is
# in its opening, not in a famine.  (OPENFAST, s49.)
#
# READ-SITE ONLY, same convention as the v524/v528/v534/v537 blocks: every
# name below is read inside the branch it guards, so
# `LOKI_FS_V539 = False` reproduces `bots/_v537socket` byte-for-byte.
LOKI_FS_V539 = True         # master.  False == `bots/_v537socket` unchanged
FS_V539_REEST = True        # the plank.  Master and plank are separate so a
                            # flag-off battery can kill either one.
FS_V539_MIN_RND = 60        # no famine may be declared before this round.
                            # The opening is not a famine and OPENFAST is not
                            # to be touched.  The measured incident wiped at
                            # ~r100, so 60 is 40 rounds of margin and still
                            # ahead of the r150-250 survival window.
FS_V539_DROUGHT = 25        # rounds with no stack seen on the mouth before
                            # famine is declared.  One connected harvester
                            # delivers every 4 rounds and a stack sits on the
                            # mouth for a full round, so a delivering belt
                            # misses 25 consecutive polls with probability ~0;
                            # 25 also outlasts the residual stacks already in
                            # flight when the last harvester dies.
FS_V539_LIFELINE_RNDS = 40  # length of the reserve waiver from the round the
                            # episode is declared.  40 rounds is ~100 Ti of
                            # passive income -- enough for a harvester (20 x
                            # scale) and its trunk, not enough to convert a
                            # siege bank into belt.
FS_V539_MAX_RNDS = 120      # hard stop on one episode even if delivery never
                            # resumes.  Past this the economy pays full price
                            # again: a famine that cannot be fixed must not
                            # keep the reserves waived for 900 rounds.
FS_V539_MAX_EPISODES = 3    # famines per match.  The third failure to
                            # re-establish is information, not a reason to
                            # keep paying.
FS_V539_DRAFT = True        # rung B
FS_V539_SEAT3_HOLD = True   # rung C
FS_V539_LIFELINE = True     # rung A
FS_V539_RESERVE_FLOOR = False
                            # ⭐ v539.1 -- THE CONSERVATIVE ARM, SHIPPED OFF,
                            # BUILT BECAUSE OF THIS BUILD'S OWN SURPRISE.
                            # Report §6: with the lifeline unfloored the parent
                            # is ahead on "rounds the bank could afford a
                            # sentinel" 16 of 25 cells to v539's 0 -- the plank
                            # buying economy with the kill budget, which is a
                            # DEFENCE_ADMISSION-shaped risk and not a thing to
                            # settle by argument.  With this ON the rebuild may
                            # spend only down to `sentinel_cost +
                            # SIEGE_HEAL_RESERVE_TI` -- the literal bar main.py
                            # checks before buying a sentinel -- so THE REBUILD
                            # WAITS RATHER THAN RAIDING THE KILL BUDGET.
                            # ⛔ ITS COST, STATED: on a bank the wipe drained to
                            # single digits the floor means the lifeline never
                            # fires inside its 40-round window (passive is
                            # 2.5 Ti/round against a ~107 Ti bar plus the
                            # harvester).  That is the trade, and it is the
                            # point -- this arm rebuilds only out of TRUE
                            # SURPLUS, i.e. the belt-cut-while-rich case.  The
                            # battery runs BOTH arms; nothing here claims which
                            # wins.
FS_V539_HONEST_SLOT = False # ⛔ SHIPPED OFF ON PURPOSE.  The commission's
                            # "reset the ratchet to the live count" change,
                            # built so a leg can price it.  The consumer
                            # enumeration says it CLOSES the forward-sentinel
                            # gate (>= 2), the home launcher (>= 1) and both
                            # paving gates (>= 1, >= 2) at exactly the moment
                            # Magnus wants a sentinel bought.  Do not turn
                            # this on without a battery.
FS_V539_LOG = False         # stderr V539 tape; LOCAL INSTRUMENT ONLY, and
                            # platform replays strip stdout anyway (CLAUDE.md,
                            # s28: 30,664 of 30,664 BotOutput events empty).
FS_ECO_BIT_FAMINE = 1 << 18 # bit 18 of FS_ECO_SLOT
FS_ECO_FAM_RND_SHIFT = 19   # bits 19-29: round the episode was declared, + 1
FS_ECO_FAM_RND_MASK = 0x7FF # so 0 unambiguously means "no episode running"


# ============================================================================
# ⭐⭐ v541 "LOKI-QUIET, ONE MORE CARVE-OUT" -- THE ARRIVED RAIDER'S DAMAGE
# VERB.  (arm `bots/_v541quiet`; parent `bots/_v537socket` = ladder v174)
#
# THE FIELD MEASUREMENT THAT ASKS FOR IT
# (`docs/research/FIELD-DEBUT-v174-2026-08-21.md`, 25 rated games, 5 opponents,
# every number decoded off replays with a self-checking damage ledger --
# 50 of 50 ledgers report MATCH):
#
#   * an own builder reaches d^2 <= 2 of the ENEMY CORE in **25 of 25 games**,
#     median arrival r12, INCLUDING all five kladde games and both games where
#     we do zero core damage.  **We arrive everywhere, on time.**
#   * **builder-attack damage into an enemy core: 0 HP, in 25 of 25 games.**
#     100% of the 17,946 HP we put into enemy cores is SENTINEL.
#   * our first forward sentinel lands r32-r176 when it lands at all; their
#     home guard is up at median r9.  **The arr2 -> first-damage gap is 50-150
#     rounds, and the body is standing on their ring for all of it.**
#
# ⇒ The reach collapse is NOT a delivery failure.  It is a CONVERSION failure
# at the destination.
#
# ⛔⛔ AND THE PREMISE WAS CORRECTED MID-BUILD.  THIS BLOCK ORIGINALLY SAID
# "the verb that would convert is switched off" AND THAT IS FALSE.  Premise of
# record: `docs/research/AUTOPSY-v174-losses-2026-08-21.md` §5.2, ten match
# games decoded --
#
#   **556 builder attacks.  517 into enemy CONVEYORS.  12 into gunners.  27
#   onto tiles whose target was already dead.  ZERO into an enemy CORE.  And
#   419 of those attacks were made WHILE STANDING NEXT TO AN ENEMY CORE, 407 of
#   them into a 20 HP conveyor.**
#
# ⇒ **THE VERB IS NOT SILENT.  IT IS MISDIRECTED.**  `LOKI_QUIET_ON` forbids
# the CORE (raid.py clause 1) while the LOKI-SALT carve-out (doctrine.py:1744)
# permits the BELT, so an established raider spends its one action per turn on
# the cheapest object in reach with the win condition one tile away.  kladde
# g1: bot #3 parked on their socket for 64 consecutive rounds, 51 attacks on
# the conveyor at (25,27), 0 on the core -- **in a game we WON**, which is why
# "did we win" is not a dose control for this fix.  kladde g3: 229 attacks,
# 226 into conveyors, 0 into the core.
#
# ⭐ THAT CHANGES WHAT THIS BUILD IS.  It is NOT a flag flip un-silencing
# builder melee -- that road carries the -10.83 v527 precedent and is not
# tested here.  It is a **TARGET PRIORITY** fix at core adjacency: the same
# action, the same 2 Ti, the same body, the same tile, a different target.
# `LOKI_QUIET_ON` stays True; clause 1 stays silenced; the salt verb is
# untouched everywhere except the tiles orthogonally adjacent to their core.
#
# ---------------------------------------------------------------------------
# WHY THE SILENCE EXISTS, AND IT IS NOT A STYLE CHOICE -- READ THIS FIRST
# ---------------------------------------------------------------------------
# LOKI_QUIET_ON (doctrine.py:1687, LOKI-7/v123) silences ALL builder melee and
# it was a MEASURED WIN, not a tidy-up: v96 went 12-3 with core_kill_share
# 12/15 = 80% against v94 Eir's 33% (p=0.025).  The mechanism is an ENGINE
# RULE, not a heuristic: **acting and moving are mutually exclusive for a
# builder bot**, this line wins on ARRIVAL, so every peck is a step not taken.
# The second half of the argument is arithmetic: 2 damage a round against a
# 500 HP core that ONE enemy builder heals at +4 for 1 Ti is not progress.
#
# AND THE HARM IS NOT HYPOTHETICAL -- IT HAS BEEN RESURRECTED ONCE AND IT COST
# US THE LEG.  `_v178salt` (LOKI-SALT, 2026-08-12, 25 live games) re-opened a
# melee verb with a NARROWER target than this one.  Its mechanism confirmed
# perfectly (20/20 salts on a tile the same bot had pecked to <=2 HP, 6.68
# barriers/game vs a 3.48-3.72 baseline) and it **FAILED ON KILL ROUND: 13
# kills at median r179 against a pooled r129, Mann-Whitney p=0.008, outside
# the bootstrapped 90% band.**  The diagnosis was never the mechanism; it was
# that ~10 pecks is ~10 rounds of not walking.
#
# ⇒ **THE HARM THIS BUILD MUST NOT RESURRECT IS NAMED AND MEASURABLE: ROUNDS
# TAKEN FROM MOVEMENT.**  Not "melee", not "Ti spend" -- movement rounds.
#
# ---------------------------------------------------------------------------
# WHY THIS CARVE-OUT CANNOT PAY THAT PRICE, AND THE REASON IS STRUCTURAL
# ---------------------------------------------------------------------------
# **THE HARM IS A TAX ON ARRIVAL, AND THIS VERB ONLY EVER FIRES AFTER ARRIVAL
# IS COMPLETE.**  A builder orthogonally adjacent to the enemy core footprint
# has, by construction, no further step that buys arrival -- it IS at the
# destination.  That is the discriminator LOKI-SALT lacked: salt fired on
# belts anywhere in the enemy half, i.e. ON THE WAY, where a step still bought
# something.
#
# But "adjacent" is not enough on its own, because a body at the ring still
# walks -- it sweeps `needed` to seal the collar, and THAT walking is the
# plank the whole siege family is built on.  So the gate is the one LOKI-48
# already invented for exactly this question:
#
#   ⭐ **GATE ON THE MOVE, NOT ON THE ACTION.**  Being last in a verb ladder
#   only proves no better ACTION existed; the parent's next act after a
#   declined action is to WALK.  `_v541_idle_ok` REPRODUCES THE PARENT'S OWN
#   WALKER (`_fs_walk` / `_fs_supp_walk` / `_raid_station`) IN THE PARENT'S
#   ORDER and permits the attack only where that walker's decision was "stand
#   still" -- move cooldown non-zero, no station at all, or already standing
#   on the station it picked.  This is `_salt_idle_ok`'s design (raid.py) with
#   the siege walkers mirrored the same way.
#
# ⇒ **THIS VERB SPENDS ONLY ROUNDS THE PARENT SPENT DOING NOTHING.**  LOKI-48
# CLAIMED that property by ordering; here it is a PRECONDITION with its own
# predicate, and the flag-off/dose instruments measure it both ways.
#
# ---------------------------------------------------------------------------
# WHAT IT IS FOR, PRICED HONESTLY -- A FINISHER AND A PRESSURE CHANNEL
# ---------------------------------------------------------------------------
# A peck is 2 Ti for 2 damage, so a 500 HP core is 250 pecks / 500 Ti solo.
# **THIS IS NOT A SOLO KILL PLAN AND MUST NOT BE SOLD AS ONE.**  What it is:
#   * **RATE.** A forward sentinel does 18 damage / 2 rounds = 9 HP/round.  One
#     builder pecking beside it adds 2 HP/round (+22%); two add +44%.  A SECOND
#     sentinel costs 30 Ti AND +20% on the global additive cost scale, which
#     inflates every subsequent build of every type; a peck costs 2 Ti and 0%.
#   * **THE HEAL RACE.** Class (iii) of the field report is "reach without a
#     kill": 2,934 / 1,116 / 234 HP of our damage fully healed away, costing
#     two r1000 games.  A defender heals +4/round.  Chip that arrives EVERY
#     round is what a periodic 18-damage shot is not.
#   * ⚠ **A THIRD ARGUMENT IS DELIBERATELY NOT LEANED ON:** that forcing the
#     heal taxes THEIR builder-round, which is the same scarce currency
#     LOKI-QUIET is about.  Plausible, unmeasured, named here so it is not
#     smuggled into the verdict.
#
# ---------------------------------------------------------------------------
# THE TARGET IS THE ENEMY CORE AND NOTHING ELSE
# ---------------------------------------------------------------------------
# ⛔ NOT BUILDINGS GENERALLY.  Destroying an enemy building LOWERS THEIR COST
# SCALE (CLAUDE.md, guard-matrix sweep 2026-08-10: scale is team-keyed and a
# destroyed contribution is removed) -- demolition is an economic GIFT.  The
# core cannot be destroyed-for-refund; damage to it is the win condition
# itself.  The existing carve-outs (conveyor melee at doctrine.py:1744,
# FS_CLEAR_RING_ON, FS_HOME_TURRET_RESPONSE) each pierce QUIET for a target
# whose OWN arithmetic inverts; this one pierces it for the only target where
# the damage IS the scoreboard.
#
# ---------------------------------------------------------------------------
# THE KILL'S MONEY IS SENIOR TO THE PECK
# ---------------------------------------------------------------------------
# The s50 belt-lastlink autopsy is the standing warning: two reserves that had
# never been checked against each other deadlocked the bank permanently.  So
# this verb spends STRICTLY SURPLUS, and the reserve it respects is the whole
# remaining collar (every barrier still owed + FS_SEAL_MARGIN) AND, while no
# forward sentinel is alive, a whole sentinel's price.  A peck may never be
# the reason the first sentinel is unaffordable -- that sentinel is 100% of
# our measured core damage.
#
# ---------------------------------------------------------------------------
# HOW THIS LOSES (write it down before the data)
# ---------------------------------------------------------------------------
# 1. The idle predicate is wrong somewhere and the verb eats walking rounds
#    after all -> kill round regresses exactly as LOKI-SALT's did.  The
#    per-body dose counter and the both-ways selftest are aimed at this.
# 2. The peck aggroes a defender that was ignoring a parked body, and a 40 HP
#    builder trades badly against the sentinel line that does 96.8% of the
#    damage in this game.  ⚠ **UNBOUNDED BY DESIGN HERE** -- there is no
#    "stop if shot at" clause, because the retreat/dodge layer (FS_RETREAT_ON,
#    FS_DODGE_ON) already outranks every act rung and is untouched.
# 3. It is simply too small to see at n=180/cell.  A null on the kill clock
#    with a confirmed nonzero dose closes the road cheaply; that is the
#    intended cheap outcome, not a failure.
# ============================================================================

FS_V541_COREPECK = True     # master.  False == `bots/_v537socket` unchanged,
                            # byte-for-byte: every read of every flag below
                            # sits INSIDE the branch this one guards.
                            # ⭐ RENAMED from FS_V541_ATTACK mid-build, and the
                            # rename IS the correction: "attack" described
                            # un-silencing a verb, and the verb is not
                            # silenced -- it is MISDIRECTED.  What ships is a
                            # core PECK PRIORITY at core adjacency.
FS_V541_COREFIRST = True    # ⭐⭐ THE SHIPPED CLAUSE: on-seat target priority,
                            # core before conveyor (raid.py clause 6.5).  A
                            # REDIRECT of an action the parent already takes --
                            # same round, same 2 Ti, better target -- so it
                            # spends nothing in the arrival currency
                            # LOKI_QUIET_ON exists to protect.
FS_V541_IDLEPECK = False    # ⛔ THE ADDITIVE CLAUSE, SHIPPED **OFF**, AND THE
                            # ASYMMETRY IS THE POINT.  This one ADDS an action
                            # on a round the parent spent idle, so it spends
                            # titanium that would otherwise have become
                            # sentinel ammunition (the exchange rate below),
                            # and the autopsy licenses TARGET PRIORITY, not a
                            # new verb.  Kept, flagged and separately measured
                            # because the arr2 -> first-sentinel gap (median
                            # r12 to r67+) is a real 50-150 round window in
                            # which an established body with no belt in reach
                            # has nothing to redirect FROM -- the autopsy's own
                            # tape shows bodies idle in it for 85, 205 and 973
                            # consecutive rounds.
FS_V541_FINISH_ON = True    # ⭐⭐⭐ THE FINISHER CONDITION, AND THE BATTERY
                            # PUT IT HERE.  The UNCONDITIONAL redirect (this
                            # flag False) is MEASURED AND REFUTED on the
                            # deterministic paired fixture: vs beltbreak2 it
                            # lost 18 timely kills of 180 and gained 0
                            # (McNemar p=0.0000); vs mjolnir it was level on
                            # the primary but slower in 18 of the 115 cells
                            # both arms killed and faster in 0 (p=0.0000).
                            # Two cells, zero counter-rows.  See
                            # `_v541_finishable` for the mechanism -- a 20 HP
                            # conveyor FINISHES under a 2-damage peck and a
                            # 500 HP healed core does not, which is
                            # doctrine.py:1744's own argument.
FS_V541_FINISH_HP = 120     # enemy-core HP at or below which the redirect is
                            # allowed.  ⛔ NOT A FREE PARAMETER: it is the
                            # damage this body's ENTIRE remaining peck budget
                            # can deliver (2 x FS_V541_MAX_PECKS), and the code
                            # takes the MIN of the two so a body that has
                            # already spent its budget stops claiming it can
                            # finish.  Reasoned, not swept; a sweep is named as
                            # deferred in the build report rather than implied.
FS_V541_LOG = False         # stderr tape "V541 <uid> rnd hp" -- OFF in
                            # competition.  ⛔ AND IT IS NOT AN ANALYSIS
                            # INSTRUMENT: platform-downloaded replays carry
                            # `stdout` EMPTY in 30,664 of 30,664 BotOutput
                            # events (CLAUDE.md, s28).  Local only.
FS_V541_TI_FLOOR = 8        # bank left ABOVE the collar+sentinel reserve
                            # before a 2 Ti peck is allowed.  Four pecks of
                            # headroom; LOKI_PECK_TI_FLOOR = 4 is the parent's
                            # bare-minimum form and is deliberately not reused
                            # -- that floor was written for a verb with no
                            # reserve stack above it.
FS_V541_KEEP_SENT = True    # while NO forward sentinel is alive, also reserve
                            # a whole sentinel's price.  100% of our measured
                            # core damage is sentinel; a peck must never be
                            # the reason the first one is unaffordable.

# ============================================================================
# ⛔⛔ THE AMMUNITION CLAUSE -- THE BUILD'S OWN NEGATIVE, AND THE ARITHMETIC
# THAT EXPLAINS IT.  READ THIS BEFORE TOUCHING FS_V541_AMMO_AWARE.
#
# THE FIRST BUILD OF THIS PLANK HAD NO SUCH CLAUSE AND THE ws1 BATTERY SAID SO:
#
#            (180 games/cell, ws1, NOISE_OFF, paired seeds, 2026-08-21)
#   vs _v488beltbreak2   timely-kill <=r300   v541 89/180 = 49.4%
#                                             parent 105/180 = 58.3%   -8.9pp
#                        median kill round    213 vs 179               +34
#   vs _x3r0v173mjolnir  timely-kill <=r300   47/180 vs 47/180          0.0pp
#                        median kill round    285 vs 261               +24
#
# ⇒ **THE PROGRAMME PRIMARY FELL ON ONE OF TWO CELLS AND MEDIAN KILL ROSE ON
# BOTH.**  That is the LOKI-SALT signature exactly (r179 vs a pooled r129) and
# it arrived even though the idle predicate is clean -- so the harm was NOT the
# movement round this build spent its whole design budget protecting.
#
# ⭐ THE MECHANISM IS AN EXCHANGE RATE, AND IT IS ARITHMETIC, NOT A HYPOTHESIS:
#
#      builder peck     2 damage  for  2 Ti          =  1.00 HP per titanium
#      sentinel shot   18 damage  for 10 ammo
#                                 and ammo is 1:1 from titanium (`convert_ammo`
#                                 is the ONLY source; there is no passive ammo)
#                                                    =  1.80 HP per titanium
#
# **A PECK IS 44% LESS CORE DAMAGE PER TITANIUM THAN THE SAME TITANIUM SPENT AS
# SENTINEL AMMUNITION** -- and both draw on ONE bank.  `main.py`'s KILL-phase
# magazine converts the bank down to the collar floor, so titanium a peck takes
# is not idle titanium: it is titanium that WOULD have become ammunition on the
# Core's very next turn.  The plank was silently converting the team's damage
# budget from the 1.80 channel into the 1.00 channel, every round it fired.
#
# ⛔ AND THE ORIGINAL FUNDING GATE COULD NOT SEE THIS.  It reserved the
# sentinel's BUILD COST (30 Ti) and stopped there -- a turret that exists and
# cannot shoot is exactly the state the s51 autopsy calls "a full collar, a
# full magazine and nothing to fire it", inverted.  **RESERVING THE GUN AND NOT
# ITS AMMUNITION IS THE SAME CLASS OF ERROR AS THE TWO-RESERVE DEADLOCK: two
# claims on one bank, never checked against each other.**
#
# THE CLAUSE.  A peck may only spend titanium that could NOT have become
# sentinel damage.  Two states qualify and they are exhaustive:
#   (a) NO live forward sentinel -- there is nothing to feed, so ammunition
#       buys 0 HP this round and 1.00 > 0.  ⭐ This is precisely the
#       arr2 -> first-sentinel gap (median r12 to r67+) that the whole plank
#       exists to fill, so the clause does not touch the intended use.
#   (b) the magazine is ALREADY FULL (>= FS_V541_AMMO_MIN) -- beyond that the
#       marginal titanium is not converting into shots any faster, and the
#       surplus is genuinely surplus.
# Everything between those two states is the losing conversion, and is refused.
#
# ⚠ HONESTLY BOUNDED: -8.9pp on n=180 is z = -1.70, p ~ 0.09 -- NOT significant
# at the 5% level, and the other cell read exactly 0.0pp.  The clause is not
# justified by that p-value; it is justified by the EXCHANGE RATE, which is a
# rules-level fact about the engine (2 dmg / 2 Ti against 18 dmg / 10 ammo /
# 1:1) and needs no fixture at all.  The battery is what MADE US LOOK.
# ============================================================================
FS_V541_AMMO_AWARE = True   # refuse the peck while it would be starving a live
                            # sentinel's magazine.  False reproduces the FIRST
                            # build of this plank -- the one the battery scored
                            # at -8.9pp -- and is kept only so the clause's own
                            # contribution stays separately measurable.
FS_V541_AMMO_MIN = 120      # ammunition at or above which the magazine counts
                            # as full.  ⛔ NOT A NEW NUMBER: this is the tree's
                            # own FS_AMMO_KILL_MIN, the constant that already
                            # defines "the kill window is open" (12 sentinel
                            # shots = 216 HP banked).  Written as a literal
                            # rather than as `= FS_AMMO_KILL_MIN` because arm
                            # construction APPENDS overrides to this file, so a
                            # derived module-level constant would silently keep
                            # the pre-override value (the v515 finding, and
                            # `flagoff_audit.py` R1 enforces it).
FS_V541_MAX_PECKS = 60      # per-BODY lifetime budget.  120 Ti and 120 HP of
                            # core if every one lands.  Bounded in the shape
                            # of LOKI_SALT_CUT_MAX / FS_CLEAR_MAX_PECKS: a
                            # treadmill on one body is the failure mode every
                            # melee verb in this tree has had to cap.
FS_V541_RAID_ON = True      # also un-silence the RAID layer's on-seat core
                            # peck (raid.py clause 1), under `_salt_idle_ok`.
                            # Same verb, different chassis path; separable
                            # because the two layers dispatch different bodies.
FS_V541_NEED_SENTINEL = False
                            # ⭐ VARIANT, SHIPS **OFF**, and the reason is the
                            # measurement rather than a preference.  ON, the
                            # peck only fires alongside a live forward
                            # sentinel -- the "rate" argument in its purest
                            # form, and immune to the heal objection.  OFF, it
                            # also fires in the arr2 -> first-sentinel gap,
                            # which is the 50-150 rounds THIS BUILD EXISTS TO
                            # FILL.  Shipping ON would leave that gap empty
                            # and test nothing the sentinel does not already
                            # do.  Named, flagged and reversible without
                            # touching siege.py -- the house pattern
                            # (FS_SALT_LATCH, FS_V520_GUNNEAR).

# ======================================================================
# ⭐ WAVE-LATE-SURGE (s58) -- THE LATE ECONOMY PIVOT.
#
# WHAT WAS MEASURED, AND IT IS NOT THE CAP.  bifrost.map26 seed 7 vs
# _x3r0v188mjolnir, wave seat A: the harvester RATCHET (SLOT_HARVESTERS) reads
# **1** from round 25 to round 400 while ECO_CAP is 18 and the bank sits at
# 80-250 Ti all game.  The cap was never the binder; three separate upstream
# gates were.
#
#   1. THE MAP IS NOT IN THE CATALOGUE.  `known_map_for` (eco.py:214) matches
#      on (w, h, core anchor) against MAP_CODES + EXTRA_MAP_CODES, and
#      (26, 12, (2,5)) is in neither -- so `map_grid` stays None, `map_ores`
#      stays the empty list it is initialised to (main.py:77), and the ORE
#      PARTITION at eco.py:1987 (`if self.map_ores and self.role != "defend"`)
#      NEVER ENGAGES.  `_pick` degrades to the blind angular wander at the
#      bottom of the function.
#   2. THE WANDER LIVELOCKS.  With `map_grid is None`, `_bfs_direction`
#      short-circuits to `p.cardinal_direction_to(target)` -- greedy, no
#      flood -- and `_nav`'s fallback ladder (perpendicular, perpendicular,
#      OPPOSITE) then walks the body back where it came from whenever the
#      greedy step is blocked by our own paved conveyor ring.  A body pacing
#      a 2-cycle MOVES SUCCESSFULLY every round, so `self.stuck` never
#      reaches 5 and the `stuck >= 5` re-pick at eco.py:2653 never fires.
#      Measured: seat 1 (id 5) alternated (0,5)<->(1,5) and seat 2 (id 9)
#      alternated (0,9)<->(1,9) for 350 consecutive rounds, both holding an
#      unreachable wander target.
#   3. THE COLLAR RESERVE OUTRANKS THE DIG FOREVER.  With a raider parked at
#      the enemy ring, `_eco_spendable` subtracts `8 * barrier + FS_SEAL_MARGIN`
#      from the bank; on the tape `ti 89 hcost 55 spend 0` is the standing
#      reading.  This is the v513 change-C deadlock in a third costume: the
#      reserve is bought once, the seal never lands, and the economy is
#      priced out of a 55 Ti harvester on an 89 Ti bank for 700 rounds.
#
# WHAT THE PLANK DOES, AND WHAT IT DELIBERATELY DOES NOT.  From
# WAVE_SURGE_RND it (a) remembers every ore tile this body has SEEN and picks
# the nearest free one -- the same partition idea run off live vision instead
# of the catalogue, scanned only on a re-pick and never per round; (b) breaks
# the pace 2-cycle by forcing a re-pick when the body's last WAVE_SURGE_PACE_N
# recorded positions cover two tiles or fewer; (c) stops the raid's reserves
# outranking the dig while the ratchet is under WAVE_SURGE_HARV_TARGET; (d)
# raises the harvester ceiling through the EXISTING `_eco_cap` surge on a
# floor that a stalled rush can actually reach (SURGE_TI_FLOOR = 1500 is
# unreachable on a bank that never clears 900); (e) sends NEW replacement
# bodies to the economy instead of the raid while the ratchet is short.
#
# IT DOES NOT TOUCH THE RUSH.  Every clause is behind
# `round >= WAVE_SURGE_RND`, so rounds 0..249 execute the parent's bytes --
# the twelve cells that finish before r250 are unchanged by construction.  It
# also does not recall a raider that is already walking: the T4_BLEED lesson
# in this file (recalling the whole economy on a latch once finished a game
# with 0 titanium delivered) is exactly the mistake available here.
# ======================================================================
# ⛔⛔ SHIPS **OFF**, AND THE REASON IS THE MEASUREMENT, NOT A PREFERENCE.
# Built default-ON, ablated on bifrost.map26 seed 7 vs _x3r0v188mjolnir, wave
# seat A, local engine, --tle 10.  `main.py:1226` re-rolls `spawn_salt` from
# unseeded OS entropy every match, so this cell is a RANDOM DRAW and not a
# fixed cell -- every figure below is a rate over independent games, not a
# replay:
#
#   arm                                    n     wins        our mined (mean)
#   OFF   (this flag False)              180    52.2%              1,742
#   FULL  (every clause below)            80    41.2%              1,629
#   NO-FUND (mechanics only, c/e/h/k off) 80    43.8%              1,567
#   MIN   (a/b/f/j/n only)               100    48.0%              1,547
#   NAV   (b/j only)                     100    49.0%              1,530
#
# **EVERY ON variant is at or below OFF on win rate AND on delivered
# titanium.**  Pooled ON is 165/360 = 45.8% against 94/180 = 52.2% -- a 6.4pp
# gap whose 95% half-width is 8.9pp, so it is NOT significant; the reason to
# ship OFF is that the point estimate is negative in FIVE arms out of five and
# the plank's own currency (delivered titanium) moves the WRONG WAY in all of
# them.  Nothing here earned its place.
#
# ⭐ WHY IT DID NOT WORK, WHICH IS THE PART WORTH KEEPING.  Decoded off the
# replay wire (`scratchpad/s58_beatmj/belt_decode.py`): the surge does what it
# says -- the harvester ratchet goes from 1-2 to 10-13 -- and delivery does
# not move, because **2 of 12 harvesters are connected to our core** and the
# engine's `mined` figure never exceeds ~4,950 in ANY arm, which is exactly
# what TWO harvesters deliver over 1,000 rounds.  On bifrost only (1,1) and
# (1,10) are close enough to wire reliably; everything else needs a 9-link
# belt across ground the opponent contests.  The extra holes cost 75 Ti and
# +5% team cost scale each and deliver nothing, and the funding clauses take
# that money from the defence -- our core is destroyed in 40/80 games with the
# full plank against 24/80 with it off.
#
# ⇒ THE ROAD THIS CLOSES: "more harvesters" is not the plank on this map.
# "More CONNECTED harvesters" is, and that is a belt-survival problem, not an
# expansion-driver problem.  Every clause below stays written, flagged and
# individually switchable so the next attempt starts from the diagnosis rather
# than from the search.
WAVE_LATE_SURGE = False     # master flag for the whole block below
WAVE_SURGE_RND = 250        # nothing in this block can fire before this round
WAVE_SURGE_HARV_TARGET = 12 # ratchet level at which the pivot stands down and
                            # the raid's reserves outrank the dig again
WAVE_SURGE_SEEN_ORE = True  # (a) live-vision ore memory in `_pick`
WAVE_SURGE_UNSTICK = True   # (b) break the pace 2-cycle
WAVE_SURGE_PACE_N = 8       # positions kept; <=2 distinct in 8 == pacing
WAVE_SURGE_FUND = True      # (c) waive the collar/siege reserves for the dig
WAVE_SURGE_TI_FLOOR = 200   # (d) reachable replacement for SURGE_TI_FLOOR
WAVE_SURGE_SEATS = True     # (e) new bodies join the economy, not the raid
WAVE_SURGE_SPREAD = 3       # seats fan out over the N nearest free ore tiles
                            # instead of all converging on the closest one
WAVE_SURGE_LQ_STALE = 30    # (f) rounds a link queue may fail to shrink before
                            # the body abandons it.  MEASURED: seat 2 (id 9)
                            # sat at (4,1) holding `lq 4` with `link_queue[0] =
                            # (4,2)` from round ~290 to the end of the match --
                            # `_build_next_link` returns False forever when
                            # another of our own bodies is parked on the link
                            # tile (`can_build_conveyor` refuses an occupied
                            # tile and the `occupied` pop only tests
                            # BUILDINGS), and the `if self.link_queue:` branch
                            # in `_expand` returns before the re-pick can run.
                            # `stuck` reached 211 on that body.  One expander
                            # in three, deleted from the economy for 700
                            # rounds, on a deadlock between two of our own.
WAVE_SURGE_ROUTE_W = 2      # (g) weight on distance-to-CORE when the surge
                            # picks ore.  `titanium_collected` is credited on
                            # DELIVERY, so an unwired harvester is worth zero
                            # forever AND costs +5% team cost scale, i.e. it
                            # makes every later build dearer for nothing.
                            # Measured: a run whose ratchet reached 10 still
                            # delivered 2,470 -- exactly one harvester's 243
                            # stacks over 975 rounds -- because the other nine
                            # never got a belt home.  Route length is the
                            # thing to minimise, walk length only the
                            # tiebreak.
WAVE_SURGE_ENDFACE = True   # (n) ⭐ THE TERMINAL LINK THAT POINTS AT A WALL.
                            # `_build_next_link` faces the LAST tile of a plan
                            # with `nearest_cardinal(tile.direction_to(core))`
                            # -- as the crow flies, with no test of what is
                            # actually on that side.  Decoded on a final
                            # board: the row-1 trunk ran west
                            # (9,1)<(8,1)<(7,1)<(6,1)<(5,1)< and then (4,1)
                            # faced SOUTH into (4,2), which is a WALL, two
                            # tiles from the (2,1) link that would have joined
                            # it to the core.  Five conveyors and two
                            # harvesters delivering nothing because the last
                            # one points at rock.  Under the surge the
                            # terminal facing prefers a side that actually
                            # holds one of our belt tiles or our core, then a
                            # side that is at least passable, and only then
                            # falls back to the parent's compass answer.
WAVE_SURGE_WIRE_FIRST = True
                            # (m) ⭐ FINISH THE BELT BEFORE DIGGING THE NEXT
                            # HOLE.  `_build_next_link` returns False whenever
                            # the body is not ORTHOGONALLY ADJACENT to its own
                            # `link_queue[0]`, and the harvester clause sits
                            # directly below it -- so a body walking toward
                            # its unfinished route builds a NEW harvester the
                            # moment it passes an ore tile, and then walks on.
                            # That is the decoded 12-harvesters-2-connected
                            # shape exactly: each new hole costs 75 Ti and
                            # +5% on the ONE global cost factor, delivers
                            # nothing without a route, and makes the links the
                            # route still needs DEARER.  While this body holds
                            # a live plan, its action belongs to the plan.
WAVE_SURGE_AMMO_FLOOR = 160 # (k) ⭐ THE FUNDING BINDER, DECODED RATHER THAN
                            # GUESSED.  `coreConvertAmmo` events off the
                            # replay wire, our team, per 100 rounds:
                            # r0-99 = 124 Ti, r200-299 = 108 Ti,
                            # **r300-386 = 620 Ti in 42 conversions**.  That
                            # is 7.2 Ti per round against a total income of
                            # about 5 (2.5 passive + 2.5 from the two
                            # connected harvesters), which is why the bank
                            # tape reads `ti 0 .. ti 6` for hundreds of
                            # consecutive rounds while three expanders stand
                            # beside their link tiles waiting for EIGHT
                            # titanium.  The magazine is not overspending on
                            # its own terms -- every one of its floors is
                            # satisfied -- it simply has no floor that
                            # represents the economy.  This is that floor, and
                            # it enters through the same `max()` the other
                            # five reserves use, so it can only ever RAISE the
                            # bar conversion must clear and never lowers an
                            # existing one.  Turrets keep firing from whatever
                            # is already banked.
WAVE_SURGE_NAV = True       # (j) ⭐ THE DEEPEST OF THE THREE, AND THE ONE
                            # EVERYTHING ELSE DEPENDS ON.  `_bfs_direction`
                            # opens with `if self.map_grid is None: return
                            # p.cardinal_direction_to(target)` -- on a map the
                            # catalogue does not carry there is NO PATHFINDING
                            # AT ALL, only a greedy compass step.  Our own
                            # paved conveyor ring plus our own parked bodies
                            # then form pockets a greedy step cannot leave,
                            # and `_nav`'s fallback ladder ends in
                            # `desired.opposite()`, which walks the body back
                            # where it came from.  That is the 350-round
                            # (0,5)<->(1,5) pace, and it is also why an
                            # adopted belt-rescue plan is never reached: the
                            # body simply cannot walk to `link_queue[0]`.
                            # This replaces the greedy step with a flood over
                            # the tiles the body can SEE -- which is exactly
                            # the scale of the obstacle -- and falls back to
                            # the parent's compass step whenever the flood has
                            # nothing to say.
WAVE_SURGE_RESCUE = True    # (i) ⭐ THE ONE THAT ACTUALLY MOVES DELIVERY.
                            # DECODED off the replay wire (belt_decode.py,
                            # direction enum verified against a belt whose
                            # delivery is not in doubt): a 1000-round game
                            # ended with **12 of our harvesters alive and 2
                            # connected to our core**, and the engine's own
                            # `mined` figure -- 4,150 -- is exactly what two
                            # harvesters deliver.  The other ten sat on
                            # 3-to-6-link belt stubs that stop in open ground:
                            # (11,2)(10,2)(9,2)(8,2) then nothing,
                            # (14,2)(14,3)(14,4) then nothing.  A `link_queue`
                            # is PER-UNIT STATE, so when the wiring body dies
                            # or is diverted its half-built belt is orphaned
                            # and NOTHING in the tree ever picks it up:
                            # `_l4_repair` only fires for a harvester with NO
                            # acceptor at all, which a stub's first conveyor
                            # still is.  This clause lets an idle expander
                            # adopt the dead end and finish the route.
WAVE_SURGE_RESCUE_EVERY = 8 # per-body duty cycle, offset by seat, so the
                            # unknown-map `_link_path` flood (two engine calls
                            # per tile) is paid by one body per round at most
WAVE_SURGE_SPAWN_RES = 300  # (h) extra bank the Core keeps before buying
                            # another body while the ratchet is short.  At the
                            # measured late-game scale (~380%) a builder bot
                            # is 114 Ti -- MORE than a harvester -- and adds
                            # +20% to the one global cost factor, so it
                            # inflates every harvester bought after it.  The
                            # tape shows units 13-15 and a bank pinned at
                            # 12-115 while `spend 0` refuses a 74 Ti
                            # harvester: the hands were never the shortage.


def wave_surge_on(ct):
    """True once the late economy pivot is open.  One reader for every site.

    Wrapped because `get_current_round` is an engine call inside a try in
    every other hot path in this tree, and an exception escaping run() is a
    permanent unit death.
    """
    if not WAVE_LATE_SURGE:
        return False
    try:
        return ct.get_current_round() >= WAVE_SURGE_RND
    except Exception:
        return False


def wave_surge_short(ct):
    """True while the surge is open AND the harvester ratchet is under target."""
    if not wave_surge_on(ct):
        return False
    try:
        return ct.read_store(SLOT_HARVESTERS) < WAVE_SURGE_HARV_TARGET
    except Exception:
        return False

