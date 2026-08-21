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
# LOKI-BEARING (2026-08-15) -- the home turret must be pointed at the thing
# that is killing us.
#
# MEASURED, over the 30 ladder games in replays/ladder (20 losses):
#   * 2,529 loss-rounds had an enemy turret inside HUNT_BAND_DSQ of our Core.
#     985 of them we had no home turret at all; of the 1,544 where we did,
#     **1,463 (95%) had NO home turret whose facing covered the besieger** and
#     only 81 did.  In the wins the same figure is 520 of 545.
#   * 21 of the 25 home turrets built in losses were Sentinels -- fixed facing,
#     no rotate -- and 11 of the 25 were born with NOTHING on their line at all.
#   * SLOT_THREAT named a tile holding no enemy on 893 loss-rounds (458 empty,
#     435 holding one of OUR OWN buildings).  Store writes land NEXT round and
#     the slot is never cleared, so a Sentinel sited with can_fire_from() on it
#     is aimed at where an enemy builder stood at least one round ago -- and it
#     stays aimed there for the rest of the match.
#   * 702 turret-rounds had a hostile ON the line and less global ammo than one
#     shot costs; the median titanium bank at those moments was 12 -- exactly
#     the ti_floor the Core refuses to convert below.
#
# The five planks, each independently ablatable:
#   CB_LIVE_TARGET_ON  -- site the counterbattery against an enemy this unit
#                         can SEE THIS ROUND, ranked turret > launcher >
#                         builder; fall back to SLOT_THREAT only when the tile
#                         it names still holds an enemy.
#   CB_MOBILE_GUNNER_ON-- a mobile target (builder) may only be answered with a
#                         Gunner, which can rotate for 10 Ti.  Freezing a 30 Ti
#                         Sentinel on a walker is what produced the silent
#                         barrels above.
#   CB_BEARING_GATE_ON -- "we already have a home gun" only suppresses the
#                         counterbattery when that gun's CURRENT facing covers
#                         the target.
#   CB_HUNT_MOVE_ON    -- the defender walks toward a besieging turret when no
#                         home turret bears on it, so that a bearing site is
#                         reachable at all (build sites are the four tiles
#                         orthogonally adjacent to this body).
#   CB_DRY_MAG_ON      -- with a weapon on the books, under attack and less
#                         than one Sentinel shot in the magazine, convert down
#                         to CB_DRY_MAG_TI_FLOOR instead of the siege floor.
#
# SHIPPED OFF IN loki_turbo5 (2026-08-15).  These five were measured
# mirror-neutral in loki_turbo3 against loki_turbo, ITS OWN PARENT.  Re-measured
# ON TOP OF turbo4 they are mildly negative on both instruments:
#
#                                     head-to-head vs turbo4      panel
#   turbo4 against a frozen COPY of itself   47.8 % (n=270)          --
#   these five OFF (the control)             46.3 % (n=540)       90.2 %
#   these five ON                            43.0 % (n=540)       87.6 %
#                                                                (n=450 each)
#
# -4.8 pp and -2.6 pp, about 1.6 and 1.2 standard errors: consistent in
# direction on two independent instruments and significant on neither.  They
# are off because "mildly negative twice" is the best evidence available, not
# because they are refuted -- turn all six back on to restore turbo3's
# behaviour exactly.  The likely conflict is documented in the T5 verdict
# block: turbo4's SEAT-FIRST already answers the state the BEARING HUNT
# answers, and T5_HUNT_BEFORE_SEAT_ON is the knob that picks between them.
# ============================================================================
#
# SHIPPED OFF AGAIN IN bots/loki_leap (2026-08-16).  loki_leap's base is
# turbo4-EQUIVALENT, not turbo6: the six flags below are the whole difference
# between the two and the ladder measured that difference the wrong way round.
# v152 (= turbo4) scored +63.8 Elo over 57 matches; v153 (= turbo6, i.e. these
# six ON) scored -39.8 over 4, and turbo4 beats the turbo6/turbo7 line ~60 %
# head-to-head locally.  That is a weak ladder sample against a strong local
# one pointing the same way, so the six go down and the three leap planks are
# measured on top of a turbo4-equivalent base.
#
# THE REVERT IS EXACTLY THIS BLOCK, and it is the same revert the T5 verdict
# block at the end of this file already prescribes.  Two further constants are
# DEAD while these are off and are left at their turbo6 values on purpose, so
# that flipping the six back on restores turbo6 byte-for-byte:
#   CB_TARGET_BUILDERS_ON -- feeds CB_RANK_ACTIVE, which `_cb_scan` consults
#       only on the CB_LIVE_TARGET_ON path (main.py: the flag-off path returns
#       from SLOT_THREAT before CB_RANK_ACTIVE is ever read).
#   CB_SMALL_MAP_CAP_ON   -- read only inside `if CB_BEARING_GATE_ON:`.
# CB_OVER_HEAL_ON is NOT one of these six: it predates them (it is in turbo4)
# and stays ON.
# ============================================================================

CB_LIVE_TARGET_ON = False
CB_MOBILE_GUNNER_ON = False
CB_BEARING_GATE_ON = False
CB_HUNT_MOVE_ON = False
CB_DRY_MAG_ON = False

CB_DRY_MAG_TI_FLOOR = 2     # titanium kept back when the magazine is dry
CB_DRY_MAG_AMMO = 10        # "dry" = below one Sentinel shot
CB_HOME_TURRET_CAP = 3      # live turrets inside the home band, hard cap
CB_HUNT_MOVE_DSQ = 9        # stop walking once this close to the besieger
CB_RANK_THREAT_ON = False
CB_TARGET_BUILDERS_ON = True   # DEAD while CB_LIVE_TARGET_ON is False

# LOKI-BEARING SMALL-MAP GUARD.  Measured in the loki_turbo mirror: the whole
# head-to-head deficit lives on tiny boards -- 6W-24L (20%) on maps of <=150
# tiles against 57% on 401-700.  A turret is impassable; on a 10x10 with a 2x2
# Core there is no room to plant three of them without strangling our own
# delivery termini and heal seats, and the games stall out to the r1000
# tiebreak.  The aiming fixes are free and stay on; only the EXTRA bodies go.
# SHIPPED OFF.  The bucket that motivated it (6W-24L on <=150 tiles) did not
# survive replication: enabling the guard moved <=150 to 40% but ALSO moved the
# 401-700 bucket, which the guard cannot touch, from 57% to 43%.  That is the
# noise floor talking, so the mechanism stays in the file and off the ladder.
CB_SMALL_MAP_CAP_ON = False
CB_SMALL_MAP_TILES = 150
CB_HOME_TURRET_CAP_SMALL = 1


# ============================================================================
# LOKI-TURBO5 (2026-08-15) -- THE BATTERY, THE TARGET LIST, THE GUNNERS AND
# THE IDLE HAND.  Every number below is from analysis/resource_gap.md.
#
# turbo5 is turbo4 (the deployed ladder build: LOKI + TURBO + the ammo/seat
# fixes) with turbo3's LOKI-BEARING counter-battery aiming planks merged in,
# plus the first four of resource_gap.md (c)'s five changes.  Everything is
# flagged; turning every T5_* flag off restores turbo4 + LOKI-BEARING exactly.
#
# THE FOUR MEASUREMENTS THIS ANSWERS (resource_gap.md (b)):
#
#  G1  WE FIGHT WITH ONE TUBE; THEY FIGHT WITH A BATTERY.  Median max
#      simultaneous forward turrets: OURS 1, top-5 2 (LI 3).  Ever 2 forward
#      alive at once: OURS 33 % of games, top-5 77 %, the top-4 in the
#      challenge games 93 %.  The arithmetic makes the lone tube a
#      STRUCTURALLY losing siege: one sentinel is 6.1 HP/round observed and
#      ONE adjacent builder heals +4 HP/round for 1 Ti, so two healers
#      out-heal one sentinel outright.  Consequence: forward-turret uptime
#      38 % of the game, i.e. for 62 % of every game we have no gun pointed
#      at their Core at all.
#
#  G3  AND IT STANDS IN THE ANSWER RANGE.  62 % of our forward turrets sit at
#      2.50-3.61 from their Core -- inside the reach of a gunner built ON the
#      Core (r^2 = 13) -- against the top-5's 33 %.  Only 20 % of ours are in
#      the 3.61-5.66 standoff band where a sentinel hits the Core and nothing
#      built on the Core hits back; the top-5 put 46 % there.  34 % of our
#      forward turrets die (71 % against the top-4).
#      The converse is the whole reason plank B is a GATE and not a placement
#      tweak: our SEAL build put 86 % of its forward turrets in the standoff
#      band and went 1W-29L, because it fed them in ONE AT A TIME.
#
#  G4  82 % OF OUR AMMUNITION GOES INTO THE ENEMY CORE AND 5 % AT THEIR
#      ECONOMY; ph and Pivot are 30/54 and 34/49 and fire 184 and 227 shots a
#      game against our 70.  One destroyed link orphans the whole tail and
#      NOBODY IN THIS GAME REPAIRS.  Note which way the correlation runs
#      inside the top five: O(1), the weakest of them, is 93 % core / 0 %
#      economy -- the profile that most resembles ours.
#
#  G2  WE BUILD ZERO GUNNERS.  Gunner Ti share: OURS 2.0 %, LI 12.4 %, Pivot
#      10.8 %.  Median gunner shots per game, every version we have ever
#      deployed: 0.  A gunner is 20 Ti base against the sentinel's 30, fires
#      EVERY round against the sentinel's every second, and is 1.75 dmg/Ti
#      against 1.8 -- our entire damage output is bottlenecked on one
#      sentinel's reload cycle.
#
#  G6  A THIRD OF OUR BUILDER LABOUR IS NEVER SPENT.  Builder-turns idle:
#      OURS 31.6 %, top-5 12.3 %, sporks 1.8 %.  11,548 of 36,546 turns over
#      30 games do nothing -- 46,000 HP of healing not delivered.
#
# ALL FOUR PLANKS MEASURED NEGATIVE AND ARE SHIPPED OFF.  The mechanisms are
# wired, flagged and ablatable; the flag values are the measured-best
# configuration, not the brief's.  READ THE VERDICT BLOCK AT THE END OF THIS
# FILE BEFORE TURNING ANY OF THEM ON.
# ============================================================================

# --- MERGE: turbo4's SEAT FIRST vs turbo3's BEARING HUNT --------------------
# Both claim the defender's move in the same state (Core bleeding, besieger in
# the band, nothing bearing on it).  turbo4 is the deployed build and wins the
# tie by default; flip this to put the hunt first and re-measure.
T5_HUNT_BEFORE_SEAT_ON = False

# --- PLANK B: THE BATTERY GATE (change 1; fixes G1 + G3) --------------------
# NEVER BUILD A FORWARD TURRET ALONE.  The gate is on the BANK, not on the
# placement: hold until two tubes are affordable at once, then plant both.
# After a pair dies the same gate re-arms itself, which is exactly the "do not
# re-poke solo" rule -- with zero live turrets the bank test is the 2x test
# again.
T5_BATTERY_GATE_ON = False
# The gate has two halves and they measured very differently, so they are two
# flags.  T5_GATE_2X_ON is the HOLD: refuse the first tube until both are
# affordable.  The follow-through half (the pair window and the third-tube
# rule) costs nothing and is what actually assembles a battery.
T5_GATE_2X_ON = False
# Slot 13 (SLOT_DEFEND_BEAT) is declared in this file with the eider evidence
# attached and read by NOBODY in this lineage (loki_analysis.md 3.2 defect E,
# 6.1 lists it among the 43 dead constants); loki_turbo2's guard layer
# reclaimed it and that layer is gone.  Re-reclaimed here after grepping that
# no caller reads it.  Value = round of the last forward-turret build + 1, so
# 0 still means "never".
SLOT_T5_BATT = 13
T5_PAIR_WINDOW = 6          # the second tube must go up within this many rounds
T5_PAIR_TI_FLOOR = 4        # ...and inside that window it outbids everything
T5_TRIPLE_AFTER = 10        # ...and the pair must then STAND this long for a 3rd
T5_BATTERY_AMMO = 40        # ammunition banked or convertible before the first
T5_TRIPLE_TI_FLOOR = 60     # extra bank demanded of the third tube

# WHERE THE PAIR STANDS.  A sentinel reaches 5 cardinal / 4 diagonal tiles
# (engine_mechanics.md D), so a site at cardinal 4-5 or diagonal 3-4 from a
# Core tile hits the Core.  A gunner reaches 3 cardinal / 2 diagonal, r^2 = 13,
# so anything at d^2 >= 14 from the footprint is outside the answer a gunner
# built ON their Core can give -- that is the 3.61-5.66 standoff band, and the
# reason our median forward distance of 2.92 loses 34 % of its turrets.
T5_NEST_ON = False
T5_STANDOFF_MIN_DSQ = 14    # strictly outside a Core-side gunner's r^2 = 13
T5_NEST_CARD = (5, 4)       # cardinal standoff ranks, farthest first
T5_NEST_DIAG = (4, 3)       # diagonal standoff ranks, farthest first
T5_NEST_MIN_SEP_DSQ = 8     # the two nests must not share one gunner's answer
T5_NEST_WALK_ON = True      # a raider walks to its assigned nest once near
T5_NEST_AXIS_PENALTY = 24   # a site standing on a visible enemy turret's ray
T5_NEST_APPROACH_DSQ = 121  # the nest walk only engages inside this of the ring

# --- PLANK R: RE-TARGET THE GUNS (change 2; fixes G4) -----------------------
# (i) an enemy TURRET in line, (ii) an enemy LAUNCHER, (iii) an enemy CONVEYOR
# 8-15 tiles back from their Core along a trunk -- or ANY enemy belt/harvester
# in line when their Core is not in line at all, which is the home turret's
# whole world -- (iv) an enemy BUILDER standing on one of their 8 heal seats,
# (v) the Core, (vi) anything else.  A sentinel must ALWAYS name an occupied
# tile: it names any tile in its 5-line whether or not anything is on it, and
# an empty name is 0 damage for 10 ammo (engine_mechanics.md D).
T5_RETARGET_ON = False
# THE ORDER IS ONE KNOB, best first, so an ablation can move a single category
# rather than the whole list.  "turret"/"launcher"/"econ"/"seat"/"core"/"other"
# is the brief's order, taken from ph (54 % of shots at economy) and Pivot
# (49 %) against our 5 % -- and O(1), the only top-5 team with our fire profile
# (93 % core / 0 % economy), is the weakest of the five.
#
# MEASURED AND REFUTED IN THIS LINEAGE -- see the T5 verdict block below.  The
# brief's order costs 15.5 pp head-to-head because two of its rungs are a
# losing trade FOR THIS BOT specifically:
#   * "seat" above "core".  A builder is 40 HP = 3 Sentinel shots, and it is
#     respawned in ~5 rounds; those 3 shots are 54 damage the Core does not
#     take, to remove +4 HP/round of healing.  Break-even needs 13 rounds of
#     it staying dead and it does not.
#   * "turret" above "core".  Same arithmetic without the respawn, and it
#     hands the initiative to whichever body they park in our line.
# Our whole win condition is a Sentinel firing THROUGH a sealed collar into a
# Core that cannot heal (raid.py header); the collar is what makes core damage
# permanent, and no other target has that property.
T5_RANK_ORDER = ("core", "turret", "launcher", "econ", "seat", "other")
T5_TRUNK_MIN_D = 8          # Manhattan from their Core: nearer than this and the
T5_TRUNK_MAX_D = 15         # tail still delivers; farther and it is not a trunk
# A barrier is 3 Ti and 30 HP: two sentinel shots and 20 ammo to remove 3 Ti of
# scale.  Never worth it unless the magazine is full and nothing else is up.
T5_BARRIER_AMMO_MIN = 40
T5_BARRIER_REPEAT_RNDS = 30

# --- PLANK G: GUNNERS (change 3; fixes G2 + G7) -----------------------------
# (a) One gunner beside each forward nest, built AFTER the pair, facing along
#     the nest's own ray -- it covers the sentinel's reload rounds and the
#     seats the defender heals from.  (b) One HOME gunner by ~r20 sited so its
#     3-tile ray covers the straight approach from the enemy Core at 2-4 tiles
#     out, verified with get_attackable_tiles_from rather than assumed.
T5_FWD_GUNNER_ON = False
T5_FWD_GUNNER_CAP = 2
T5_FWD_GUNNER_TI_FLOOR = 20
T5_HOME_GUNNER_ON = False
T5_HOME_GUN_RND = 12        # start trying here so it is standing by ~r20
T5_HOME_GUN_TI_FLOOR = 20
T5_HOME_GUN_NEAR_DSQ = 4    # the ray must cover a tile at least 2 tiles out...
T5_HOME_GUN_FAR_DSQ = 16    # ...and no more than 4, which is where they park
T5_HOME_GUN_SITE_DSQ = 25   # and the gun itself stands inside 5 of our own Core

# --- PLANK Z: ZERO IDLE (change 4a; fixes G6) -------------------------------
# A builder that reaches the end of its turn having neither acted nor moved
# gets one more pass: heal an adjacent damaged friendly, re-lay a missing trunk
# tile beside it (_l4_repair, which is already the narrow hole-filling rule),
# or step toward the objective it already has.  Nothing new is invented here --
# it is the same three things the turn was already allowed to do.
T5_ZERO_IDLE_ON = False
T5_IDLE_HEAL_ON = True      # arm 1: heal an adjacent damaged friendly
T5_IDLE_REPAIR_ON = True    # arm 2: _l4_repair a trunk hole beside us
T5_IDLE_STEP_ON = False
T5_IDLE_HEAL_GAP = 4        # one heal's worth of damage, so nothing is wasted
# G6 counts the idle turns and prices them at "1 Ti per heal", but titanium is
# the binding constraint in this lineage, not builder-turns: the measured bank
# through r20-r80 is 24-158 Ti and a scaled harvester is 40-60 of it.  An idle
# hand healing scratches out of the harvester budget is PIECE K' again, so the
# floor is set ABOVE a harvester -- idle healing spends surplus only.
T5_IDLE_HEAL_TI_FLOOR = 40


# ============================================================================
# LOKI-TURBO5 -- THE VERDICT.  READ THIS BEFORE TURNING ANYTHING ON.
#
# ALL FOUR PLANKS MEASURED NEGATIVE AGAINST loki_turbo4 AND ARE SHIPPED OFF.
# The mechanisms are in the file, wired, flagged and ablatable; the flag
# values below are the measured-best configuration, not the brief's.
#
# METHOD.  NOISE_ON draws `spawn_salt` from OS entropy per match, so repeated
# runs of the same pair are genuinely independent and n=90 is NOT a
# measurement here: two runs of the identical configuration (the brief's
# target ordering) returned 35.6 % and 43.3 % on n=90.  Every number below is
# the per-game win rate over the ab.py cell set -- 45 maps (15 competition +
# 6 synthetic + 24 synthetic_ab) x both sides x 3 seeds = 270 games -- run
# head-to-head against a FROZEN loki_turbo4 (tools/t5_variant.py stamps the
# copies; never A/B against a bot you are editing, tools/README.md).
# 0 tracebacks and 0 failures in every leg.
#
# CALIBRATE THE INSTRUMENT BEFORE READING ANY OF IT.  loki_turbo4 against a
# BYTE-IDENTICAL FROZEN COPY OF ITSELF measures **47.8 %** (n=270, CI 42-54),
# not 50 %.  So 47.8 is the zero of this scale, the brief's "head-to-head must
# be >= 50 %" is a bar that a null change does not clear, and every number
# below is read against 47.8 rather than 50.  With every T5 flag AND every CB
# flag down -- this tree reduced to turbo4 -- the build reads 47.0 % and 45.6 %
# on two independent n=270 runs: indistinguishable from the self-mirror.  THE
# MERGE IS INERT WHEN THE FLAGS ARE DOWN, which is what this file's house rules
# demand of a control leg.
#
# LEAVE-ONE-IN, from the all-planks-off build (n=270 unless marked):
#
#   configuration                                       vs loki_turbo4
#   ZERO: loki_turbo4 vs a frozen copy of itself              47.8 %
#   SHIPPED: every T5 and every CB flag down          50.0 / 47.0 / 45.6 %
#   T5 planks all off, CB planks up                          44.8 / 41.1 %
#   + plank R, retarget, the brief's order (n=90)             43.3 %
#   + plank R, retarget, core-first order                     40.0 %
#   + plank B, battery gate + nest (n=90)                     44.4 %
#   + plank B, the 2x bank hold alone (n=90)                  40.0 %
#   + plank B, the nest placement alone (n=90)                47.8 %
#   + plank G, home gunner (n=90)                             40.0 %
#   + plank Z, zero idle, all three arms (n=90)               46.7 %
#   + plank Z, the heal arm alone (n=90)                      47.8 %
#   + plank Z, the step arm alone (n=90)                      38.9 %
#   ALL FOUR PLANKS ON (n=90)                                 34.4 %
#
# NO PLANK BEATS THE 47.8 % ZERO.  loki_turbo4 (ladder v152) stays the
# deployed build; loki_turbo5 as shipped is behaviourally identical to it --
# the three shipped-config runs read 50.0 / 47.0 / 45.6 %, which is the zero,
# three times -- and it exists as the wired, flagged, measured home of these
# mechanisms and as the record of what they cost.  On the ab.py panel (45 maps
# x both sides x 5 opponents = 450 games per build, per-game win rate):
#
#   loki_turbo4                                  92.7 %
#   loki_turbo5 as shipped (every flag down)     90.2 %
#   CB planks up, T5 planks down                 87.6 %
#   every plank up (the brief's configuration)   88.0 %
#
# Against `starter`: 100 % (30/30) on the 15 competition maps both sides, and
# 95.6-97.8 % on the wider 45-map set where turbo4 reads 98.9 %.  Every
# traceback in every leg comes from bots/starter/main.py's own known
# `Position out of bounds` bug; ours took 0 across ~6,000 games.
#
# DID THE PLANKS DO WHAT THEY WERE DESIGNED TO DO?  Decoded from the replays
# with tools/analysis_scratch/resource_gap.py, 21 maps x both sides vs `seal`,
# turbo4 against the brief's full configuration -- reproduce that build with
#
#   python tools/t5_variant.py t5_full T5_BATTERY_GATE_ON=True \
#       T5_GATE_2X_ON=True T5_NEST_ON=True T5_RETARGET_ON=True \
#       T5_FWD_GUNNER_ON=True T5_HOME_GUNNER_ON=True T5_ZERO_IDLE_ON=True \
#       T5_IDLE_STEP_ON=True \
#       'T5_RANK_ORDER=("turret", "launcher", "econ", "seat", "core", "other")'
#
# (the table was taken before the self.t5_nav_rnd fix and before
# T5_IDLE_HEAL_TI_FLOOR was raised from 4 to 40, so a re-run of the command
# above will differ slightly on the idle row):
#
#   metric                          target   turbo4   all planks on
#   max simultaneous fwd turrets      >=2      2.0        2.0
#   % of games ever 2+ fwd alive     >=70 %    74 %       83 %   <- met
#   forward-turret uptime            higher    42 %       26 %   <- BACKWARDS
#   shots/game                       >=120      39         50
#   % of shots at their economy      >=35 %     0 %        5 %
#   gunner shots/game                 >=40      0.0        5.5
#   builder idle %                    <10 %   22.4 %     15.9 %  <- moved
#   win rate vs seal                            83 %       81 %
#
# READ THE THIRD ROW.  The battery gate DID assemble more pairs -- 74 % to
# 83 % of games -- and the pairs it assembled stood for 26 % of the game
# against 42 % without it.  More tubes, up later, dying faster: the gate
# spends the opening bank that used to buy the FIRST tube early, and a battery
# that arrives after their collar is manned is a battery that arrives to die.
# G1 is measured on our v151 ladder corpus (33 % of games ever 2+ forward) and
# TURBO4 HAS ALREADY LARGELY CLOSED IT (74 %) by other means -- the brief's
# largest single gap was mostly fixed before this branch started, which is the
# other half of why plank B has nothing left to win.
#
# The economy-fire and gunner targets were not approached: 5 % against a 35 %
# target and 5.5 gunner shots against 40.  Both are volume targets and volume
# is exactly what a 51-shot bot does not have.
#
# WHAT THE BATTERY TAUGHT, which outlives the flag values:
#
# 1. THE BRIEF'S TARGET LIST IS RIGHT FOR ph AND WRONG FOR THIS BOT.  Two of
#    its rungs put a target above the enemy Core that cannot pay for the
#    shots: a builder on a heal seat (40 HP = 3 Sentinel shots, respawned in
#    ~5 rounds, removing +4 HP/round -- break-even needs 13 rounds of it
#    staying dead) and an enemy turret (same arithmetic without the respawn).
#    Core-first recovers 3 pp of the 5 and is still 5 pp down.  The reason is
#    structural and is in raid.py's own header: our win condition is a
#    Sentinel firing THROUGH A SEALED COLLAR into a Core that cannot heal, and
#    THE COLLAR IS WHAT MAKES CORE DAMAGE PERMANENT.  ph's 54 %-at-economy
#    profile belongs to a bot with 184 shots a game to spend; ours has 51, and
#    every one spent elsewhere is a round the collar holds for nothing.
#    Economy fire is a strangulation strategy and strangulation needs volume
#    we do not have -- which is exactly what change 3 was supposed to buy, and
#    change 3 costs more scale than it returns (below).
#
# 2. THE 2x BANK HOLD IS THE THIRD "UNMEETABLE FLOOR" THIS LINEAGE HAS
#    MEASURED.  GUARD_RESERVE_ON took a deterministic mirror from 50 % to
#    41 %; POP_FLOOR_ON has the same comment from the other side; the battery
#    hold takes 44.8 % to 40.0 %.  All three have the identical shape -- a
#    reserve that binds precisely when the bank cannot meet it.  Two scaled
#    Sentinels plus the floor is 220 Ti and our measured bank through r20-r80
#    is 24-158 (loki_analysis.md 5.1), so "hold until you can pay for two" is
#    in practice "never open the siege".  The gate's OTHER half -- the pair
#    window, which makes the SECOND tube nearly free for 6 rounds once the
#    first is standing -- costs nothing and is what actually assembles a
#    battery; it is kept, with T5_GATE_2X_ON off.
#
# 3. THE STANDOFF NEST IS THE ONE PLACEMENT IDEA THAT SURVIVED (-3 pp, inside
#    the interval).  It is off because it did not clear 50 %, not because it
#    was refuted -- and G3's own converse says why it cannot help alone: the
#    SEAL build put 86 % of its forward turrets in the standoff band and went
#    1W-29L, because standoff placement is necessary and NOT SUFFICIENT.  It
#    needs the pair, and the pair needs titanium we do not have.
#
# 4. A HOME GUNNER IS STILL THE WRONG PRICE, for the third time.  -4.8 pp on
#    its own here, and loki_turbo2's GUARD verdict measured the same thing
#    twice ("firing it on proximity cost 13 pp; damage-gating it recovered all
#    of that and left it at break-even").  A gunner is +20 % on the ONE GLOBAL
#    ADDITIVE cost scale, levied on every later build of every type, on a bot
#    whose win condition is affording a forward Sentinel.  G2 is real -- we
#    fire 51 shots a game to Pivot's 164 -- but the answer is not to buy the
#    gun out of the siege budget.
#
# 5. THE IDLE HAND IS NOT FREE EITHER.  G6 prices 11,548 wasted builder-turns
#    at "1 Ti per heal", but titanium is this bot's binding constraint and
#    builder-turns are not.  The heal arm is the cheap one (-3 pp, and the
#    floor is now set above a harvester so it can only spend surplus); the
#    STEP arm is -9 pp and it is worth knowing why, because it is a real bug
#    class: a builder that already tried to walk and was BLOCKED still reads
#    "no move", so the step arm called _nav a second time, and the second
#    failure incremented self.stuck twice -- the exact counter `_raid` reads
#    to decide a station is unreachable, ban it for 120 rounds and pause the
#    raider.  self.t5_nav_rnd now records the attempt; the arm stays off.
#
# 6. THE MERGE ITSELF IS INSIDE THE NOISE, and the CONTROL LEG says so.  With
#    every T5 flag AND every CB flag down -- i.e. this tree reduced to turbo4 --
#    the build measures 47.0 % (n=270, CI 41-53) against loki_turbo4 itself,
#    which is the inertness proof this file's house rules demand and also the
#    honest scale of the instrument: a control that changes nothing reads 47,
#    not 50.  With the CB planks up and the T5 planks down it is 44.8 %.  The
#    2.2 pp between them is a quarter of the interval, so turbo3's
#    counter-battery aiming is neither confirmed nor refuted on top of turbo4;
#    it is kept on because turbo3 measured it mechanism-positive, and the
#    revert is one line each:
#        CB_LIVE_TARGET_ON = CB_MOBILE_GUNNER_ON = CB_BEARING_GATE_ON = False
#        CB_HUNT_MOVE_ON = CB_DRY_MAG_ON = CB_RANK_THREAT_ON = False
#    What IS worth recording is why they might conflict: turbo4's SEAT-FIRST
#    already answers the same state the BEARING HUNT answers (Core bleeding,
#    besieger in the band, nothing pointed at it), one with a heal seat and one
#    with a walk, and two answers to one state is one answer too many.
#    T5_HUNT_BEFORE_SEAT_ON is the knob that picks between them.
#
# WHAT TO DO NEXT, if anyone takes this further.  Do not re-tune these four.
# The one finding that generalises is that every plank here spends TITANIUM or
# SHOTS, and this bot is short of both -- change 5 (the round-0 full-map plan,
# resource_gap.md (c)) is the only one of the five that spends COMPUTE, of
# which we use 3 % of the allowance.  It is also the only one that makes the
# other four affordable, which is what the brief's own sequencing note says.
# ============================================================================


# ============================================================================
# LOKI-TURBO7 -- PLANK SAP: the besieger's turret is a BUILDING, so peck it.
# ============================================================================
#
# THE MEASUREMENT (analysis/nemesis_0033.md, 110 decoded ladder games against
# the four opponents we are net-negative against: 0033, gsxWins, Pantheon,
# "kladde chatte tville").
#
#   * 0033, 50 games, 16-34.  They put 226 turrets inside d <= 8 of OUR Core:
#     95 Sentinels (median build round 57, median distance 4.0) and 131
#     Gunners (median round 152, median distance 2.8, 47 of them ON one of the
#     eight orthogonal Core seats).  Those turrets did 46,375 of the 47,061
#     damage our Core took across the fixture -- 98.5 %.  Enemy BUILDERS did
#     none of it: not one point.
#   * The same signature is in all four: kladde 124 Sentinel creepers at
#     median d = 5.0, gsxWins 41 at d = 2.8, Pantheon 9 at d = 5.0.
#   * Our answer today is a home turret.  It works about a third of the time:
#     we destroyed 51 of 226 creepers vs 0033, and they destroyed 78 of ours.
#     Across the whole ladder we remove about ONE turret a game out of the
#     5.5-11.8 these teams build, and none of them re-lays a lost one -- their
#     batteries are standing accumulations, not rebuild loops.
#   * ACROSS 110 GAMES AND 4,239 BUILDER ATTACKS, WE AIMED **ZERO** OF THEM AT
#     A TURRET.  `LOKI_QUIET_ON` silences all builder melee (v96 measured it
#     +, on the argument that a raider's ROUND is worth more than its peck),
#     and the carve-out that survived is enemy conveyors only.
#
# THE MECHANIC, MEASURED HERE (bots/probe_peck vs bots/probe_pecktur on
# maps/probe/pm_near.map26, engine 2.3.7):
#
#     WATCH r=10 (6,4) type=GUNNER   hp=25 can_fire=True  can_heal=False
#     WATCH r=11 (6,4) type=GUNNER   hp=23        <- 2 damage for 2 titanium
#     WATCH r=10 (6,6) type=SENTINEL hp=40 can_fire=True
#     WATCH r=10 (6,3) type=LAUNCHER hp=30 can_fire=True
#
#   A builder bot's `fire()` hits a TURRET exactly as it hits any other
#   building, and `get_tile_building_id()` resolves a turret tile.  So:
#     Gunner   25 HP = 13 pecks = 26 Ti
#     Sentinel 40 HP = 20 pecks = 40 Ti
#     Launcher 30 HP = 15 pecks = 30 Ti
#   against a home counter-battery at ~75 Ti of turret (30 base x ~2.5 scale)
#   plus 30 Ti of ammo to land three Sentinel shots -- and the peck costs
#   **no cost-scale at all**, where the turret costs +20 % on every future
#   build the team makes (engine_mechanics.md C).  Cheapest by 2.6x, and it
#   does not tax the economy it is defending.
#
# WHY THE BESIEGER CANNOT ANSWER IT.  A Sentinel's facing is FIXED -- only
# Gunners rotate, for 10 Ti -- so a Sentinel aimed at our Core cannot turn on
# the builder dismantling it.  It can only name tiles on the ray it already
# points down, which is the ray toward our Core; three of the four tiles
# orthogonally adjacent to it are off that ray.  `_sap_seat` walks to one of
# those three by preference.  Enemy BUILDERS cannot touch our sapper at all
# (engine_mechanics.md E: `can_fire` on a builder bot is False).
#
# WHY THIS IS NOT A REPEAL OF LOKI-QUIET.  Quiet's evidence is about the
# RAIDER's round at the far end of the map, where the peck competes with
# arrival.  This plank never fires a raider: SAP_RAIDERS_ON is False.  It
# spends the HOME defender -- a body whose alternative use is standing on a
# heal seat paying 1 Ti for +4 HP against a Sentinel's 9 HP/round, i.e.
# losing -- and expanders that are already standing next to the besieger.
#
# HOW THIS LOSES.  (a) A diverted expander is a stalled trunk chain, hence
# SAP_CHAIN_GUARD and the time-box.  (b) A Gunner CAN rotate onto the sapper:
# 7 dmg/round kills a 40 HP builder in 6 rounds, while the sapper needs 13.
# That trade is still ours -- a rotating Gunner is a Gunner not shooting the
# Core, it paid 10 Ti to rotate, and any adjacent body heals the sapper for
# 1 Ti / +4 HP -- but it is the first place to look if this measures negative.
# ============================================================================

SAP_ON = True
# NO NEW SLOT, and this cost a rebuild: ALL SIXTEEN SLOTS ARE LIVE in this
# lineage.  The ancestor names near line 930 (SLOT_DROPPED, SLOT_LAUNCH_ID,
# SLOT_LAUNCHED_ID, SLOT_DEFEND_BEAT, SLOT_SIEGE) are each RE-MAPPED further
# down this file to SLOT_FWD_GUN 8, SLOT_FERRY_ID 10, SLOT_FERRY_RND 11,
# SLOT_RAID_N 12, SLOT_T5_BATT 13 and SLOT_RAID_LIVE 15 -- so grepping the
# ancestor name finds nothing while the slot is in daily use.  Grep the
# NUMBER, not the name.
#
# So the besieger gets no publisher of its own.  A unit that can SEE a rank-0
# threat this round uses its own eyes (self.sap_seen, set in the sensing loop
# that already ranks turrets above builders); anything else falls back to
# SLOT_THREAT, which already carries that same best-ranked enemy, gated on the
# detector's S1/S4 stamp so a stale tile cannot be believed -- which is the
# exact failure the CB comment above records.  _sap re-checks the tile against
# SAP_TARGET_TYPES the moment it is in vision, so a SLOT_THREAT entry that
# names a builder costs at most one wasted step before it is dropped and
# banned for SAP_BAN_RNDS.
#
# "Creeper" = enemy turret this close to OUR Core.  64 == d <= 8, the same
# band the Core's own threat latch already uses, so the scan is free.
SAP_BAND_DSQ = 64
# A borrowed SLOT_THREAT reading older than this is a ghost.  Store writes land
# next round, so the floor is 1.
SAP_STALE = 5
# THE CREW.  Exactly one body ever WALKS to a besieger, and it is the home
# defender -- answering the siege is its job and its alternative is standing on
# a heal seat losing 9 HP a round to 4.  Measured on the first build of this
# plank (nordkap, seed 1): with expanders allowed to walk as well, THREE of six
# builders committed to the same sentinel, one of them oscillated four tiles
# away for sixty rounds without ever arriving, and the economy finished the
# game on ten titanium.  An expander may therefore only peck a turret it is
# ALREADY orthogonally adjacent to, which costs it nothing it was using.
SAP_WALK_DEFENDER_ONLY = True
SAP_EXPANDER_REACH = 1
# Bank kept after paying the 2 Ti peck, so sapping can never starve a build.
SAP_TI_FLOOR = 2
# Time-box, per unit per target.  20 pecks kills a Sentinel, so 60 rounds is
# three times the honest cost and still bounded.
SAP_MAX_RNDS = 60
SAP_BAN_RNDS = 120
SAP_EXPANDERS_ON = True
SAP_RAIDERS_ON = False
SAP_CHAIN_GUARD = True
# The one-line carve-out in _sabotage_prio: a turret standing in our home band
# is melee-able under QUIET.  Same argument as the plank; this catches turrets
# the fallback did not name (e.g. two of them at once).
SAP_MELEE_TURRETS_ON = True


# ============================================================================
# THE SHARED ARCHETYPE DETECTOR -- spec: analysis/archetype_detector.md
# ============================================================================
#
# WHY IT IS SHARED.  analysis/ladder_field.md classifies 400 of our own ladder
# replays and finds we lose to two OPPOSITE archetypes and beat everything
# else: MACRO (I Stone, Pantheon -- 36 builders, 60-82 conveyors, ZERO
# turrets, 80 % of games to the r1000 tiebreak) and PRESSURE (0033, gsxWins,
# kladde -- 4-11 turrets a game creeping onto our Core, ~97 % of games end in
# a core kill).  One compromise doctrine is a middling answer to both.
# bots/loki_macro implements the MACRO branch against this same spec; this
# file implements the PRESSURE branch (PLANK SAP).  ONE detector, so the two
# planks cannot disagree about which game they are in.
#
# THE STORE CONTRACT -- the thing that has to match between the two bots.  Two
# homes, and the split is by WRITER, not by meaning: store writes are
# last-write-wins within a round, so a field with two writers loses updates.
#
#   SLOT_ARCH_SEEN = 13   EVIDENCE.  Written by ANY unit, read-modify-write.
#       bits  0-9   round+1 of the last S1/S4 sighting (PRESSURE evidence)
#       bits 10-19  round+1 of the last S3 sighting (enemy builder near us)
#       bit  20     S2 -- an enemy turret has been seen ANYWHERE, ever
#       bits 21-25  S5 -- most enemy builders seen at once near THEIR Core
#       bits 26-31  free -- merge budget for bots/loki_macro
#
#   SLOT_HEAL_BUDGET = 9, upper bits   CLASSIFICATION.  CORE-WRITTEN ONLY.
#       bits  0-15  UNCHANGED: turbo4's bleed beacon (max_hp - hp, <= 500)
#       bits 16-17  archetype code (0 DEFAULT / 1 PRESSURE / 2 MACRO / 3 WEAK)
#       bits 18-27  round+1 the current archetype was set
#
# Slot 13 is SLOT_T5_BATT, written ONLY under T5_BATTERY_GATE_ON, which this
# file ships as False -- a slot the bot writes never and reads once
# (raid.py _t5_battery_ok).  That single read is guarded on the same flag,
# which is a no-op while it is off (it read 0 anyway) and keeps the
# reclamation honest.  Turning T5_BATTERY_GATE_ON back on costs the detector
# its evidence slot; that is written down here rather than discovered later.
# Slot 9's top half is empty by arithmetic (the beacon is <= 500) and the Core
# is its only writer, which is exactly the property a classification needs.
#
# Round+1 is stored so 0 unambiguously means "never seen"; the maximum round
# is 1000, so 1001 fits in ten bits and no age comparison ever wraps.
#
# CLASSIFICATION, verbatim from the spec, with PRESSURE winning every tie:
#   S1 or S4 within ARCH_MEMORY             -> PRESSURE
#   r >= R_MACRO, never S2, no S3 in memory -> MACRO
#   r >= R_MACRO, S5 >= 8                   -> MACRO_WEAK
#   else                                    -> DEFAULT
# Being wrong about MACRO while a turret grinds the Core is the expensive
# error; being wrong about PRESSURE only costs some economy.
#
# AUDITABILITY.  The Core prints "ARCH <name> r=<round>" into the replay on
# every TRANSITION, and only on transitions -- print() is captured per unit per
# round and a per-round log is a real CPU line item.
#
# INERTNESS.  With ARCH_ON = False and SAP_ON = False this file is
# behaviourally identical to loki_turbo6: no store writes, no prints, no
# decisions, and the two slot 9 readers mask a field that is never set.
# ============================================================================

ARCH_ON = True
SLOT_ARCH_SEEN = 13
SLOT_ARCHETYPE = SLOT_HEAL_BUDGET
ARCH_BLEED_MASK = 0xFFFF
ARCH_SHIFT = 16

ARCH_DEFAULT = 0
ARCH_PRESSURE = 1
ARCH_MACRO = 2
ARCH_MACRO_WEAK = 3
ARCH_NAMES = ("DEFAULT", "PRESSURE", "MACRO", "MACRO_WEAK")

# How long a signal stays credible.  60 rounds is the spec's number and it is
# also about two creeper lifetimes (median 24 rounds, nemesis_0033.md 1.3).
ARCH_MEMORY = 60
# Earliest round a MACRO call may be made.  The spec sweeps {100, 140, 180};
# this file never acts on MACRO, so the value matters only to loki_macro and
# lives here so both bots read one constant.
ARCH_R_MACRO = 140
ARCH_S5_MANY = 8
# "within 8 of our Core" for S1 and S3 -- the same band the Core's existing
# threat latch uses, so both signals are free.
ARCH_NEAR_DSQ = 64
ARCH_LOG_ON = True

# PLANK SAP is the PRESSURE branch: it acts only while the detector says
# PRESSURE.  In practice this is nearly a no-op -- S1 is the same sighting that
# makes a besieger visible at all -- but it means the two planks share one
# switch, and it gives SAP the spec's 60-round memory instead of dropping the
# moment the besieger leaves vision.
SAP_REQUIRE_PRESSURE = True


# ============================================================================
# PLANK REPAIR (P1, bots/loki_repair) -- HEAL THE ECONOMY WE ALREADY OWN
# ============================================================================
#
# THE MEASUREMENT (analysis/leap_design.md P1, resource_gap.md, nemesis_0033).
#   * Our repair rate is 6.8 %.  The field's is 40.5 %.
#   * Farm survival r30-r120 is the single loss discriminator: games we win
#     deliver 1,950 Ti, games we lose deliver 350.
#   * In losses OUR conveyor count FALLS across the game -- the trunk is eaten
#     and never re-laid -- while the enemy's climbs.
#   * A heal is +4 HP for exactly 1 Ti and costs ZERO cost scale
#     (engine_mechanics.md E); an enemy peck is 2 dmg for 2 Ti.  Eight to one
#     on titanium, and the 1 Ti is the only spend in this tree that does not
#     make the next Sentinel more expensive.  `can_heal` is False at full HP,
#     so a gated heal can never waste titanium.
#   * PAVE_TRAIL_ON was this line's de-facto link repair and LOKI-13 turned it
#     off (38.20 conveyors/game vs The Bisons' ~11).  The volume was right to
#     kill; the repair loop went with it and nothing replaced it.
#
# WHAT ALREADY EXISTED IN loki_turbo7, and where its gaps were:
#   (a) CHAIN MEDIC, inside `EcoMixin._expand` -- heals an adjacent damaged
#       MEDIC_TYPES building.  THREE gaps: it is reachable only from the
#       ECONOMY path (a `defend` builder standing on a bleeding harvester
#       never heals it, and neither does a raider until it falls through to
#       `_expand`); it is ranked BELOW the planned chain and below the
#       harvester bootstrap; and its early window needs MEDIC_EARLY_MIN_DMG =
#       8 damage from r40, i.e. a 20-HP conveyor must be at 12 before anyone
#       touches it.  MEDIC_TI_FLOOR is 20.
#   (b) `EcoMixin._l4_repair` -- relays ONE missing tile of a chain when there
#       is a feeder on one side and an acceptor on the other.  It is stateless,
#       narrow and cannot spam, and it is the right rule.  Its documented gap
#       is in its own docstring: "A two-wide hole has no side with both a
#       feeder and an acceptor, so it is left alone."  Two adjacent trunk tiles
#       eaten -- which is what a creeper parked on the line actually does --
#       therefore sever the delivery route PERMANENTLY.  It is also only
#       called from `_expand` and from the (shipped-off) zero-idle pass.
#   (c) `EcoMixin._heal_adjacent` -- the generic version, called only from
#       `_home_defend` and as PLANK SAP's broke-fallback.
# This plank does not replace any of the three.  It adds one hook ABOVE the
# role split that all of them are downstream of, relaxes the depth/round gates
# to the arithmetic (below), gives the eco role a BOUNDED walk-to, and closes
# the two-wide hole in (b).
#
# WHY IT IS ALLOWED TO EXIST AT ALL, given section 1 of leap_prior_art.md.
# Every refuted plank in this tree spends titanium on a BUILDING and therefore
# on the one global cost scale, out of the budget for the first forward
# Sentinel.  This one buys nothing: heals are 1 Ti at zero scale, and the only
# build it adds is a 3-Ti conveyor into a hole that already has chain on both
# sides -- the same purchase `_l4_repair` was already making, one tile deeper.
#
# HOW THIS LOSES (pre-registered, so the decode cannot be written after the
# fact).  (1) The heal consumes the MOVE as well as the action, so a body that
# heals is a body that did not arrive; ARRIVAL is the scarce quantity in this
# whole lineage (LOKI-QUIET, LOKI-8).  That is why raiders are excluded by
# default and why the opening is fenced off entirely.  (2) MEDIC_MIN_RND's
# ablation flipped fjordgate (A-core-kill@297 -> B-core-kill@138) and
# lighthouse (A-tiebreak@1000 -> B-core-kill@110) purely on opening tempo; if
# REPAIR_MIN_RND is too low this plank re-creates that exactly.  (3) A patched
# conveyor the enemy re-pecks next round is 1 Ti/round against their 2 Ti/round
# -- we win that trade on titanium and LOSE it on rounds, which is how ph
# "weaponises the re-lay loop" (top5 dossier: a barrier rebuilt 13 times purely
# to drain our ammo).  The time-box on the walk is the guard.

REPAIR_ON = True            # the whole plank; False == loki_turbo7 exactly

# Types this plank considers "the economy".  Deliberately the same tuple the
# chain medic uses -- turrets and barriers are combat capital with their own
# logic and the Core has the universal heal above this.
REPAIR_TYPES = MEDIC_TYPES

# THE FLOOR.  Small on purpose.  MEDIC_TI_FLOOR is 20 because the medic
# competes with the harvester bootstrap from inside `_expand`; this hook runs
# above the role split and the thing it protects is the delivery route that
# pays for everything else, so it yields only to the Core's own spawn/ammo
# cadence.  6 Ti is a heal plus change, and never a scaled purchase.
REPAIR_TI_FLOOR = 6

# Earliest round any repair may happen.  See "HOW THIS LOSES" (2): the measured
# cost of an opening medic is two flipped maps, and it is a TEMPO cost, not a
# titanium one.  r20 is after the first links exist and well before the
# r30-r120 farm-survival window this plank is aimed at.
REPAIR_MIN_RND = 20

# Damage depth required before REPAIR_LATE_RND.  A heal is exactly +4 HP and
# tops out at max HP, so 4 is the shallowest wound a heal can fix with ZERO HP
# wasted -- the number is arithmetic, not taste.  turbo7's early medic wants 8
# because it is spending an `_expand` action that would otherwise lay chain;
# this hook is not, so it can afford the honest threshold.
REPAIR_MIN_DMG = 4
# Past this round any damage at all is worth 1 Ti (turbo7's MEDIC_MIN_RND
# behaviour, kept identical so the two rules do not disagree).
REPAIR_LATE_RND = MEDIC_MIN_RND

# WHO REPAIRS.  Expanders always.  The home defender too -- it is the body that
# stands where the trunk terminates, and "a hole beside the Core is the one
# that costs the whole chain" (_l4_repair).
#
# RAIDERS, AND WHY THE FIRST BUILD WAS WRONG ABOUT THEM.  This shipped False on
# the LOKI-QUIET argument (a raider's round is worth more than the peck it was
# spending it on, and a heal costs the whole round including the move).  Then
# the opportunity was counted off two smoke replays, from r20, with our builder
# ORTHOGONALLY ADJACENT to one of our own pipeline buildings at >= 4 damage:
# nordkap 20 such body-rounds, midgard 22 -- and the plank converted 5.  The
# roster is why.  Seat 0 raids, seats 1-3 expand until seat 3 defects at
# harv >= ECO_NEED, seat 4 defends, and every replacement raids: in an 11-body
# game the repair crew was 3 hands and the raid was 7.  Worse, a raider whose
# raid is closed runs `_expand` (raid.py:158,172) and would have used turbo7's
# own chain medic there, so refusing it here made this plank STRICTER than its
# parent for that body.  It is admitted with two fences instead: only inside
# our own home band, and only for a wound deep enough to be sustained
# attention rather than a passer-by -- which is LOKI-QUIET's argument honoured
# rather than ignored, because a raider does not stop for a scratch.
REPAIR_RAIDERS_ON = True
REPAIR_RAID_HOME_DSQ = 36       # d <= 6 of a Core tile: the home-intruder band
REPAIR_RAID_MIN_DMG = 8         # four accumulated pecks, as MEDIC_EARLY_MIN_DMG
REPAIR_DEFENDER_ON = True
# Same fence `_l4_repair` uses: a stood-down raider calls `_expand` wherever it
# is standing, and 1 Ti spent under the enemy's guns is the trade LOKI-8 exists
# to stop.  A building closer to their Core than to ours is not our farm.
REPAIR_OWN_HALF_ONLY = True

# THE DETOUR.  The eco role may walk to a damaged trunk building it can see,
# bounded by Manhattan distance.  4 tiles = at most 4 rounds out and 4 back,
# against a conveyor that carries the whole delivery route for the rest of the
# match.
REPAIR_DETOUR = 4
# ...but only for a wound deep enough to be sustained attention rather than a
# passer-by, which is exactly MEDIC_EARLY_MIN_DMG's argument (four accumulated
# pecks on a 20-HP conveyor).  A free adjacent heal has no such bar; a WALK is
# a bigger spend than the heal it buys, so it gets the higher one.
REPAIR_DETOUR_MIN_DMG = 8
# Time-box, the same shape as PLANK SAP's target commitment.  loki_cage's
# decode is the reason: one builder oscillated four tiles from its objective
# for sixty rounds and the economy finished on ten titanium.  A body that
# cannot arrive in 6 rounds writes the tile off for 60.
REPAIR_WALK_RNDS = 6
REPAIR_WALK_BAN = 60
# NEVER take a body off a chain it is carrying.  `_wire_tick`'s evidence is
# that an abandoned chain is a dead end delivering nothing at all, and this is
# the SAP_CHAIN_GUARD precedent applied to the same failure.  A DETOUR is
# abandonment and is always refused while a queue is in flight.
REPAIR_CHAIN_GUARD = True
# An in-place heal is not abandonment -- the queue survives the round intact --
# so the guard on it is narrower: refuse only when the next link tile is
# orthogonally adjacent, i.e. when the chain could be advanced THIS round and
# healing would genuinely cost it a tile.  Set True to restore the blanket
# refusal the first build had (which, with the raid fence, was most of why the
# plank converted 5 of 20-22 opportunities).
REPAIR_CHAIN_STRICT = False

# THE REBUILD HALF.  `_l4_repair` refuses a two-wide hole because neither of
# its tiles has both a feeder and an acceptor.  The opener fills the tile that
# touches the ACCEPTOR, which turns the two-wide hole into a one-wide hole that
# the inherited rule then closes on a later turn.  It keeps every property that
# makes the inherited rule safe: chain is still required on BOTH ends of the
# hole, so it cannot walk, and filling the tile removes its own precondition.
# Three tiles is a trench, not a hole, and is left alone.
REPAIR_REBUILD_ON = True
# ...and it is BUDGETED, which the parent rule is not, because the parent's own
# audit is the reason: of the tiles its belt half relaid, only 1 had ever HELD
# a conveyor -- the rest were DEAD HEADS, chains this bot abandoned mid-walk.
# One tile of slack makes that population bigger, and the first smoke game
# proved it: 8 two-wide opens against the parent rule's 1 relay, five of them
# before r14 while the opening trunk was still being LAID.  A conveyor is +1 %
# on the one global cost scale forever, and LOKI-13 measured what unbounded
# relaying costs (PAVE_TRAIL_ON, 38.20 conveyors/game vs The Bisons' ~11).
# So: not before the plank's round floor, when a gap is far more likely to be
# the enemy's doing than the planner's, and a hard per-body ceiling.
REPAIR_GAP2_MAX = 6
# ...AND IT IS GATED ON HAVING WATCHED THE TILE DIE, which is the second thing
# the smoke games said and the more important one.  The parent rule's docstring
# records an audit of its own belt half: of the tiles it relaid, only 1 had
# ever HELD a conveyor -- the rest were DEAD HEADS, chains abandoned mid-walk.
# The same audit on the two-wide opener (tools/, 3 replays, 23 relays) read
# **0 relays of a destroyed tile, 23 dead heads**.  Ungated, this plank's
# "rebuild" half was not rebuilding anything; it was extending abandoned heads
# toward the Core, which is PIECE F's pave trail and LOKI-13 measured that off
# at 38.20 conveyors/game.  So a tile is only relaid when THIS body watched one
# of our own belts stand there and then not stand there, with the tile still in
# its vision -- the only in-engine evidence that a trunk tile was DESTROYED
# rather than never laid.  Turning this off restores the wrong population.
REPAIR_GAP2_SEEN_ONLY = True
REPAIR_LOST_MAX = 32        # cap on the per-body destroyed-tile memory
# Let the home defender run the hole rule as well (it is otherwise reachable
# only from `_expand`).
REPAIR_DEFENDER_REBUILD = True

# Instrumentation.  Local only -- platform-downloaded replays strip stdout.
# Marker vocabulary: "REP heal (x,y) hp=H" on the FIRST heal of each target by
# each body, "REP rebuild (x,y)" on a hole relay, "REP rebuild2 (x,y)" on the
# two-wide opener, "REP walk (x,y)" on committing to a detour.  Events and
# transitions only; the heal and walk markers are de-duplicated per (tile,
# unit) so a 300-round grind logs one line, not three hundred.
REPAIR_LOG = True
REPAIR_MARK_MAX = 64        # hard cap on the per-unit marker set


# ============================================================================
# PLANK P3 -- SIEGE.  Fix the four MEASURED sentinel errors + the ammo pipe.
# Spec: analysis/leap_design.md P3.  Blueprint: analysis/top5_pipeline.md
# sections (d) sentinel geometry, (e) the assault clock, (f)2-4, (g).
# ============================================================================
#
# THE FOUR ERRORS, all measured on 145 games / 290 game-sides (top5_pipeline.md):
#
#   1. OUT OF RANGE.  Distance from the sentinel tile to the enemy Core 2x2
#      CENTRE at build time.  The furthest a sentinel that EVER hit a core
#      stood was 6.364 (the 5-step diagonal), max over 402 core-hitting
#      sentinels.  The winners band is 2.5-5.7: 66.8 % of every sentinel a
#      winning top-5 side builds lands there and 85.3 % of the ones that
#      actually hit a core.  OURS: 37.8 % in band, 20.3 % in the 5.7-6.4 shell
#      where only a perfect diagonal reaches (winners 6.0 %), and 35.1 %
#      BEYOND 6.4 -- structurally incapable of ever contributing to the win
#      condition.  A third of our sentinel budget, spent on nothing.
#   2. UNPROTECTED.  74 % of their core-hitting sentinels live to the end of
#      the game, against 45 % of ours; theirs land a median 17 shots (306 core
#      HP), ours 9.  The difference is a gunner: they have 1 within 6 tiles of
#      the enemy Core at the moment of the kill, we have 0 in 63 % of our
#      game-sides ever.
#   3. UNMASSED.  Peak sentinels alive within 6 of the enemy Core: theirs 2,
#      ours 1.  Sentinels added AFTER the enemy Core passes 400 HP: 51 % of
#      their wins, 23 % of ours.  Our Core-damage curve is the earliest in the
#      field (first HP off at r30, 400 by r84) and then it STALLS, because one
#      tube at 9 dmg/round loses to eight healers at 32 HP/round.
#   4. AMMO -- STARVED THEN HOARDING.  They open the pipe on r1 (median, 100 %
#      of sides) and hold an unspent balance of 16-20 ALL GAME; we open on r11
#      and hold 24 at r100 and 59.5 at r200.  Sixty titanium of dead capital
#      in the pool while our own Core is ground down.
#
# WHAT THIS PLANK DOES NOT DO.  It does not touch WHEN the first sentinel is
# built.  The corpus says winners build theirs at r76 and we build ours at
# r34, but our early raid is what wins the mid-ladder and LOKI2_RUSH_ON 360
# paired games say a change to the opening clock is worth -15.6 to -18.9 pp.
# Timing stays opportunity-gated; this plank fixes siting, survival, massing
# and supply, which are four separate errors that survive any clock.

SIEGE_LOG_ON = True         # replay markers, on EVENTS only (never per round)

# --- 1. SITING -------------------------------------------------------------
# The predicate a forward Sentinel post must now pass, in the raid own
# siting code (raid.py `_try_forward_sentinel`), not beside it:
#   (a) distance from the POST to the enemy Core CENTRE inside [2.5, 5.7]; and
#   (b) a Core footprint tile actually inside the fixed 5-tile firing line from
#       that post and facing -- `can_fire_from`, the hypothetical-turret
#       predicate, which for a Sentinel ignores walls and occupancy (a Sentinel
#       is a 5-range single-target sniper that cannot be blocked,
#       engine_mechanics.md D), so REACHING the post is the only real
#       constraint and `can_build_sentinel` is the only test of that.
# (b) was already there.  (a) is the new half, and it is the half that removes
# the 5.7-6.4 shell: a post 4 diagonal steps from a Core tile is exactly 6.36
# from the centre -- the record, hit once, by a perfect diagonal.
#
# Arithmetic in INTEGERS.  The centre of a 2x2 footprint anchored at (ox, oy)
# is (ox+0.5, oy+0.5), so doubling every coordinate makes 4*d^2 exact:
#   4*d^2 = (2*(x-ox)-1)^2 + (2*(y-oy)-1)^2 == 2 (mod 8), always.
# 4*2.50^2 = 25.00 -> the least attainable value above it is 26 (d = 2.5495)
# 4*5.70^2 = 129.96 -> the greatest attainable value below it is 122 (d = 5.52)
# so the two bounds below are exact and no float ever enters the decision.
SIEGE_SITE_ON = True
SIEGE_BAND_MIN_Q4 = 25      # 4*d^2 >= this  <=>  d >= 2.5
SIEGE_BAND_MAX_Q4 = 129     # 4*d^2 <= this  <=>  d <= 5.7
# The winners median distance for a core-hitting sentinel is 4.30 and their
# densest decile is 2.5-3.6; 4*4.30^2 = 73.96, so posts are ranked by how close
# they land to that, AFTER the exposure test below.
SIEGE_BAND_MID_Q4 = 74
# A defender Gunner built on their own Core reaches r^2 = 13.  Where the band
# offers a choice, take the post outside it: a Gunner is 7 dmg/round on a
# 1-round reload against a Sentinel that cannot rotate and cannot answer.
# PREFERENCE, not a gate -- T5_STANDOFF_MIN_DSQ was a gate and the plank that
# carried it measured 44.4 %; a gate here would re-create it.
SIEGE_GUN_REACH_DSQ = 13

# --- 1b. THE BAND IS A PREFERENCE, NEVER A VETO  (SIEGE_SITE_FALLBACK) ------
# MEASURED DEFECT, results/leap/loki_leap_vs_t4.md + the siege mechanism log.
# The band above was written as a `continue`, so a post outside [2.5, 5.7] was
# not merely ranked last -- it was UNBUILDABLE.  A raider standing where all
# four of its cardinal neighbours are out of band therefore built NOTHING,
# where the parent would have planted a tube.  Against mimic_ph on a turbo4-
# equivalent base the merged build fielded 2.77 sentinels a game against
# turbo4's 3.01, and in-band share rose 13.7 pp while the win rate fell 5.6 pp.
# Siting quality was bought with tube QUANTITY, which is the one trade the
# massing arm ten lines below exists to refuse.
#
# Note WHERE this bound and where it did not: in the standalone siege fork,
# measured on the turbo7 base, tube count ROSE.  A veto that is invisible on
# one base and costs a quarter of the battery on another is not a siting rule,
# it is a coin flip on how often the raid happens to stand in the band.
#
# THE FIX.  Rank exactly as before -- in-band first, off a Gunner's reach,
# nearest the winners' median distance -- but when NO in-band post is
# admissible and the PARENT would have built this round, build at the parent's
# own first-come choice and log `SGE fallback`.  The invariant this restores,
# and the one to check on any future edit here:
#
#     builds(SITE on) >= builds(SITE off), post for post, always.
#
# It holds by construction: the parent builds iff SOME (post, facing) passes
# can_fire_from + can_build_sentinel, and this arm now builds iff some in-band
# one does (ranked) OR some out-of-band one does (first-come).  That union is
# the parent's condition exactly.  The discount arm (SIEGE_MASS_ON) already
# had this property -- it only ever lowers a floor -- and this is the same
# property restored to the siting arm.
#
# COST: the out-of-band posts now run can_fire_from/can_build_sentinel instead
# of being skipped -- at most four posts x four Core tiles, which is the
# parent's own scan, and the scan stops at the first admissible out-of-band
# post because the parent's choice is its first one.
SIEGE_SITE_FALLBACK = True

# --- 2. MASSING ------------------------------------------------------------
# LOKI_FWD_GUN_CAP is already 3 and is NOT raised: 3 is the specialists number
# and 4 sentinels (36 dmg/round) is the only configuration that beats eight
# healers, which we can never afford.  What this arm changes is the PRICE of
# the second and third tube, and only downward -- it can add a sentinel the
# baseline would not have bought, and can never refuse one it would have.
#
#   * tube 2: once tube 1 has STOOD for SIEGE_MASS2_AGE rounds, the bank floor
#     drops from LOKI_FWD_TI_FLOOR (40) to SIEGE_MASS_TI_FLOOR.  The age gate
#     is the survivorship half: if the first tube is dying on arrival a second
#     body dies with it (this is T5_TRIPLE_AFTER argument, one tube earlier).
#   * tube 3: the same discount, once the enemy Core is below SIEGE_MASS3_HP.
#     That is the exact window the corpus says we miss -- 23 % of our wins add
#     a sentinel after 400 against 51 % of theirs -- and the 400->0 grind is
#     63 rounds at 2 tubes + 1 gunner in their games.
#
# NO NEW STORE SLOT, and this is the third plank in a row to nearly pay for
# that mistake: ALL SIXTEEN SLOTS ARE LIVE.  The ancestor names near line 930
# are each re-bound further down this file (SLOT_FWD_GUN 8, SLOT_FERRY_ID 10,
# SLOT_FERRY_RND 11, SLOT_RAID_N 12, SLOT_T5_BATT/SLOT_ARCH_SEEN 13,
# SLOT_RAID_LIVE 15).  GREP THE NUMBER, NOT THE NAME.  The only free capacity
# in the lineage is slot 9 bits 28-31 (Core-only writer) and slot 13 bits
# 26-31 (any writer), and this arm takes TWO of the latter -- bits 26-27 --
# leaving 28-31 as the reserved merge budget for loki_macro.
#
# THE MERGE COLLISION, RESOLVED IN bots/loki_leap (2026-08-16).  PLANK P2 (the
# collar) claimed slot 13 bits 26-31 for its shared titanium budget in its own
# fork, and this arm claimed 26-27 in ITS own fork.  BOTH FORKS WERE MEASURED
# IN ISOLATION AND NEITHER SAW THE OTHER: merged naively, a collar spend of
# 1 Ti writes SIEGE_HP_HIGH into the band and a band write of LOW charges the
# collar a whole budget.
#
# THIS ARM KEEPS 26-27.  The collar's counter moved OUT of slot 13 entirely --
# see COLLAR_SPENT_SLOT in the COLLAR block, and the measurement that forced
# it.  Slot 13 keeps exactly one non-detector field, and it is one that can
# survive a lost write.
SIEGE_MASS_ON = True
SIEGE_MASS2_AGE = 20        # rounds tube 1 must have stood before tube 2 is cheap
SIEGE_MASS_TI_FLOOR = 6     # bank kept after paying for a discounted tube
SIEGE_MASS3_HP = 400        # "the assault clock has started" (top5_pipeline (e))
# Enemy-Core HP band, published in SLOT_ARCH_SEEN bits 26-27 by ANY unit that
# can see a Core tile, read by raiders that cannot (builder vision is r^2 = 20,
# so a raider siting a tube at d = 5.5 is blind to the HP it is gating on).
# Two bits, three states, and 0 means "nobody has ever seen it" -- the same
# never-seen-is-zero convention the detector uses for its round stamps.
#
# UNCHANGED BY THE MERGE, and the reason is worth stating because it is the
# rule that decided where the COLLAR budget could NOT live: this field is
# RE-DERIVED from vision every round by every established raider, so a lost
# read-modify-write costs one round of latency and the next round repairs it.
# An ACCUMULATING field has no such property -- a lost increment is lost for
# good.  Slot 13 has three writers and buffered last-write-wins semantics, so
# it can host the first kind of field and must never host the second.
SIEGE_HPBAND_SHIFT = 26
SIEGE_HPBAND_MASK = 0x3
SIEGE_HP_UNKNOWN = 0
SIEGE_HP_HIGH = 1           # seen, >= SIEGE_MASS3_HP
SIEGE_HP_LOW = 2            # seen, <  SIEGE_MASS3_HP

# --- 2b. THE BAND WAS NOT ACTUALLY RE-DERIVED  (the paragraph above was wrong)
# MEASURED DEFECT, tools/leap_store_audit.py on the shipped merge: 2 of 4 games
# recorded NO band transition at all and `SGE mass3` fired 0.04 times a game.
# The claim four paragraphs up -- "RE-DERIVED from vision every round, so a lost
# write repairs itself" -- was true of the VALUE each raider computed and false
# of the PUBLISHED copy, for two separate reasons:
#
#   (i)  the publish was TRANSITION-LATCHED (`if nv != v`), so a write lost to
#        `_arch_note`'s stale read-modify-write was not repaired next round --
#        it was repaired at the next TRANSITION, and there are only ever one or
#        two of those in a game.  Transition-latched is the same failure class
#        as accumulating: the state lives in the diff, not in the value.
#   (ii) the only publishers were raiders inside LOKI_ESTABLISH_DSQ that
#        happened to call `_sge_core_band`.  Against a busy opponent
#        `_arch_note` writes slot 13 EVERY round from every body, and whichever
#        unit moves last wins with a word built from the round N-1 read.
#
# THE FIX, in three parts, and it is the same rule the collar budget was moved
# for -- a field only survives where its writers can be enumerated:
#
#   * the AUTHORITATIVE copy moves to SLOT_RAID_LIVE (15) bits 28-29, the free
#     bits above the collar lanes.  Slot 15 has exactly ONE writer in the tree,
#     `raid._raid_beat`, and the band rides in the same word as the heartbeat --
#     so it is republished every round by every established raider at no extra
#     write.  A raider WITHOUT eyes on the Core republishes what it READ, so a
#     blind body can never erase a seeing body's answer; a seeing body
#     overwrites with its own, every round.  Lost write costs one round.
#   * the LEGACY copy in slot 13 bits 26-27 is still written, unchanged and
#     still transition-latched, for backward compatibility (older decodes and
#     tools/leap_store_audit.py read it).  It is now a HINT, read only when
#     slot 15 says UNKNOWN.  It is deliberately NOT made per-round: slot 13's
#     writer is `_arch_note` and a per-round band write from a stale read would
#     stomp the DETECTOR's fresh evidence every round -- the same race, aimed
#     the other way.
#   * the RE-DERIVE broadens from "established raiders" to every body with a
#     Core tile actually in vision (`main._builder`, above the role split),
#     gated on builder vision r^2 = 20 so it costs one integer compare to any
#     body that is nowhere near.
SIEGE_BAND_SAFE_ON = True   # publish the band in SLOT_RAID_LIVE bits 28-29
SIEGE_BAND15_SHIFT = 28     # bits 28-29 of slot 15; 30-31 remain free
SIEGE_BAND_ALLSEE_ON = True # every body with a Core tile in vision re-derives
SIEGE_BAND_VIS_DSQ = 20     # builder vision r^2 -- the gate on that re-derive
# `_arch_note` rebuilds slot 13 from four fields and DROPS everything above
# bit 25, which would erase both the band AND the collar budget on the next
# detector write.  It now carries all six high bits through unchanged.  That is
# inert with the leap flags off: nothing else in the tree ever sets a bit above
# 25, so the carried mask is 0 and the word written is bit-identical to the one
# loki_turbo7 wrote.  THIS IS THE ONE CANONICAL `_arch_note` -- the collar fork
# and the siege fork each wrote their own version of this same fix and only one
# of them survives the merge (main.py, `_arch_note`).
ARCH_KEEP_HI = 0xFC000000

# --- 3. THE SCREEN ---------------------------------------------------------
# ONE forward Gunner, 2-3 tiles BEHIND a forward Sentinel, facing the way a
# defender walks in.  Its job is not core damage -- the median gunner shots
# into a core is 0 for ph and o1, both top-5 -- it is to kill the defender
# BUILDERS that come to peck our sentinels, and turrets are the only thing on
# the board that can damage a builder bot at all (engine_mechanics.md E).
#
# THIS IS NOT HOME DEFENCE, WHICH IS REFUTED THREE TIMES.  The LOKI-GUARD
# proximity battery in loki_turbo2 measured 37 % against a 50 % deterministic
# control; T5 plank G measured 40.0 % at n=90; seal v5A capped home turrets and
# moved nothing.  The address is different: this gunner exists ONLY while a
# forward Sentinel exists, ONLY beside it, and it is the second thing the
# raider tries after the sentinel itself, so it can never be the reason a tube
# was unaffordable.  Cap 1, ever -- a gunner is +20 % on the one global additive
# cost scale and the scale is levied on every later build of every type.
#
# GEOMETRY, verified rather than assumed.  A Gunner ray stops at the NEAREST
# occupant and buildings block it, so a gunner directly behind its own sentinel
# is a gunner with a permanent wall in front of it.  The post is therefore
# accepted only if `get_attackable_tiles_from` covers at least one tile
# ORTHOGONALLY ADJACENT to the sentinel -- a peck seat, the only place a
# defender builder can stand to hurt it -- and does NOT cover the sentinel own
# tile.  (`_turret` already refuses friendly targets, so the risk here was
# blockage, not friendly fire.)
#
# SHIPPED OFF IN bots/loki_leap (2026-08-16).  MEASURED WRONG-DIRECTION on the
# metric it was built for: forward-sentinel survival fell from 95.5 % to 91.4 %
# with the screen on, and the screen gunner fired 0.17 times per game -- it was
# not shooting the peckers, it was a second 20-Ti building drawing fire and
# raising the global cost scale for every later build.  This is the fourth
# independent measurement in this lineage saying a gunner is the wrong price
# (LOKI-GUARD 37 %, T5 plank G 40.0 %, seal v5A neutral, and now this), and it
# is the only one of the three SIEGE arms that did not survive.  The mechanism
# stays wired and ablatable; only the flag goes down.
SCREEN_ON = False
SCREEN_CAP = 1              # forward gunners alive at once, ever
SCREEN_MIN_DSQ = 4          # 2 tiles from the sentinel...
SCREEN_MAX_DSQ = 10         # ...to 3 (10 admits the (1,3) offset as well)
SCREEN_TI_FLOOR = 20        # bank kept after paying for it
# The ray search is 4 posts x 8 facings of `get_attackable_tiles_from` in the
# worst case, and it would otherwise re-run every round for as long as all four
# posts happen to be occupied.  Throttled: the screen is never urgent -- the
# tube it protects is already standing -- and unbounded per-round work is the
# one budget this tree has actually spent (1.8-3.1 % of 10 ms/unit/round).
SCREEN_TRY_EVERY = 4

# --- 4. JUST-IN-TIME AMMUNITION -------------------------------------------
# Replaces the whole `ammo_target` ladder in `_core` when on.  Three changes:
#
#   (a) OPEN ON ROUND 1.  The parent gates every conversion on
#       `under or weapons_top or harv >= 2`, so the pipe opens when the second
#       harvester lands -- r11 for us against r1 for 100 % of top-5 sides.
#       JIT drops the precondition and keeps every bank floor, so the opening
#       build order is protected by exactly the reserve that protected it
#       before (the harvester reserve in E1_AMMO_FLOOR).
#   (b) SIZE THE MAGAZINE BY WHAT WILL BE FIRED.  A Sentinel is 10 ammo every
#       2 rounds (5/round) and a Gunner 4 every round; the target is
#       SIEGE_JIT_HORIZON rounds of exactly that, not the parent
#       `min(120, 40 + 20*fwd)` ladder, which asks for 60 rounds of magazine on
#       ONE tube.  With one forward tube the parent target is 40 and JIT is
#       16; with two, 80 against 30.
#   (c) CAP THE DEAD CAPITAL.  A magazine that has not FALLEN in
#       SIEGE_JIT_IDLE_RNDS rounds is not being fired by anything, and above
#       SIEGE_JIT_IDLE_CAP that is the 59.5-at-r200 failure exactly.  Convert
#       nothing until it moves.  Same census as the T4 ghost-magazine brake --
#       the AMMUNITION, which is a free global read -- but on a 3-round window
#       instead of 12, because this is a spending rule and not a rubble test.
AMMO_JIT_ON = True
SIEGE_JIT_OPEN_RND = 1      # the pipe opens here.  Top-5 median: r1.
SIEGE_JIT_HORIZON = 3       # rounds of fire the magazine covers
SIEGE_JIT_SENT_BURN = 5     # ammo/round a firing Sentinel consumes (10 / 2)
SIEGE_JIT_GUN_BURN = 4      # ammo/round a firing Gunner consumes
SIEGE_JIT_MIN = 16          # AMMO_FLOOR, unchanged: one Sentinel shot plus change
SIEGE_JIT_UNDER = 24        # under attack, as the parent
SIEGE_JIT_IDLE_CAP = 20     # top-5 hold 16-20 all game; we hold 59.5 at r200
SIEGE_JIT_IDLE_RNDS = 3     # rounds of a non-falling magazine before we stop
SIEGE_JIT_TRICKLE = 4       # per-round conversion with no turret on the books
SIEGE_JIT_STEP = 16         # per-round conversion with one, as the parent
SIEGE_JIT_MIN_AMT = 4       # the parent floor: never convert less than this
#
# HOW THIS LOSES.  (a) Siting is now a REFUSAL: a raider standing where no
# in-band post exists builds nothing that round, so if the band is walled off
# on some map we field fewer tubes, not better-placed ones -- watch "% in band"
# together with "sentinels built", never alone.  (b) The band excludes the
# 6.36 diagonal, which is a real (if once-recorded) core hit.  (c) The screen
# is +20 % cost scale on a bot whose every refuted plank died of exactly that.
# (d) JIT halves the magazine: a tube that fires the round after a top-up is
# starved by an income of 3.5 Ti/round, and the honest fix for that is P1/P4,
# not this arm -- if sentinel SHOTS fall while in-band % rises, this is why.


# ============================================================================
# PLANK P2 -- THE COLLAR (analysis/leap_design.md §P2)
# ============================================================================
#
# THE PROBLEM, IN ONE NUMBER.  Our raid already lands 500-820 HP of damage on
# every opponent in the field.  The single cleanest discriminator between the
# bots we beat and the bots that beat us is whether the victim HEALS IT BACK:
# bots we beat heal 0.00-0.22 of it, bots that beat us heal 0.51-0.82, and
# I Stone healed 10,944 of 10,944 on antler (analysis/istone_heal.md,
# analysis/nemesis_0033.md §5).  A Core heals from the eight tiles orthogonally
# adjacent to its 2x2 footprint -- the SAME eight tiles a conveyor delivers
# from and eight of the twelve it spawns onto.  Denying those seats converts
# damage we already deal into kills; nothing else in this tree does.
#
# WHY loki_turbo7 DOES NOT ALREADY DO THIS.  It bricks seats opportunistically
# (raid.py _raid_act step 2) and it can heal an adjacent own building (step 5),
# but its STATION scoring adds +12 to a corner whose seats are all sealed
# (raid.py _raid_station) -- so the moment a brick lands the body that laid it
# walks away, nobody is left orthogonal to the brick, and the brick is chewed
# down at 2 dmg / 2 Ti with no tender and no reseal until a raider wanders
# back.  turbo7 bricks ~2.5 seats by r150 and does not HOLD them.  The collar
# is not a new mechanism, it is UPTIME on an existing one.
#
# THE ARITHMETIC THE PLANK RESTS ON (analysis/probe_loops_cage.md Q2.3/Q3.4,
# all measured):
#   * seat-bricking costs 0.47 Ti/seat-round at ~100 % uptime, and forces the
#     defender to spend 480 Ti of pecks against our 81 -- 5.9 : 1;
#   * HEALING a brick beats REBUILDING it: 0.8 barriers lost / 100 rounds with
#     healing vs 29-38 without.  Their peck is 2 dmg for 2 Ti, our heal is
#     +4 HP for 1 Ti -- one tender out-repairs two peckers at a quarter of the
#     cost (the 4:1 exchange this plank is named for);
#   * a body on a seat is IMMUNE TO BUILDERS (builders cannot fire on builder
#     bots), so against a zero-turret opponent a squatter is unremovable;
#   * is_tile_empty() is a trap -- it returns True on a tile holding a bot.
#     Every gate below is can_build_barrier / get_tile_builder_bot_id.
#
# WHAT THE FLAG BUYS AND WHAT IT COSTS.  COLLAR_ON changes three things and
# nothing else: (1) a RESEAL / TEND / BRICK ladder placed at the TOP of the
# raid action ranking while the raid is established, (2) corner stations that a
# tender KEEPS instead of abandoning once sealed, (3) a shared titanium budget
# so the loop cannot become an unbounded barrier race (CAGE, -9.5 to -13.2 pp,
# is exactly that failure and is not being retried).  With COLLAR_ON = False
# every one of those is skipped and this fork is loki_turbo7.
#
# HOW THIS LOSES, written down before it is measured: bodies parked at four
# corners are bodies not paving, not expanding and not screening the forward
# sentinel; against a PRESSURE opponent that ignores the collar entirely the
# spend is pure loss; and a tender standing on a corner is standing on a tile
# an enemy gunner can be aimed at -- the corner is NOT covered by the Q3.1
# diagonal-immunity result, which is about the support tiles of a seat seen
# from a gunner built on the core, not about every facing of every gunner.
COLLAR_ON = True

# THE ENGAGE GATE.  Reuses the raid layer's own establishment signals rather
# than inventing a state machine: this body inside LOKI_ESTABLISH_DSQ (40, the
# "~6 tiles from a Core tile" the design asks for), OR a teammate's foothold
# heartbeat is live (SLOT_RAID_LIVE, LOKI_FOOTHOLD_STALE), OR a forward
# sentinel has been established (SLOT_FWD_GUN) -- the turret whose damage the
# collar exists to make permanent.
COLLAR_ENGAGE_DSQ = LOKI_ESTABLISH_DSQ

# THE BUDGET.  Collar titanium comes OUT OF the raid.  When it is exhausted the
# collar stops CLAIMING the action and the parent's own step-2 seal / step-5
# heal run exactly as in loki_turbo7 -- so the budget caps the plank's MARGINAL
# spend, it never makes the bot spend less than the baseline.  Counted in a
# shared field so four raiders cannot each spend the whole thing.
#
# LOWERED 40 -> 32 IN bots/loki_leap, AND THE GATE MADE PESSIMISTIC.  The
# measurement that forced it (results/leap/loki_collar.md): against the claimed
# 40 cap the fork actually spent a mean of 13.5 and a MAX of 46 titanium a game.
# The overrun is the read-modify-write race, and it is structural, not a bug:
# store writes are buffered a round, so two raiders spending in the same round
# both read last round's total, both write, and one update is simply lost.  The
# counter therefore always reads at or below the truth and the cap always
# arrives late.
#
# The fix is a RESERVATION, not a lock: a unit treats the counter it can see as
# (observed + COLLAR_RACE_MARGIN) and declines any spend it cannot CONFIRM fits
# under the budget at that inflated figure.  A body that cannot prove headroom
# does not spend.  With margin 6 -- two bricks' worth of concurrent raiders,
# which is more than the 2-4 collar bodies a game ever fields -- and a budget of
# 32, the worst case is 32 + one in-flight round of spends and it lands under
# the 40 the plank was measured claiming.
COLLAR_TI_BUDGET = 32
COLLAR_RACE_MARGIN = 6      # titanium assumed in flight but not yet visible
#
# --- WHERE THE COUNTER LIVES, AND WHY IT MOVED -----------------------------
#
# The collar fork put this counter in SLOT_ARCH_SEEN (13) bits 26-31.  DECODED
# OUT OF THE MERGED BUILD'S OWN REPLAYS (tools/leap_store_audit.py, loki_leap
# vs mimic_istone on royale): SEVEN bricks were laid at 7 titanium each -- 49
# spent -- and the field read ZERO on every single round of the game.  Every
# increment was lost.
#
# The mechanism, and it is not a race in the incidental sense -- it is
# structural.  Store writes are BUFFERED a round, so every writer in round N
# reads the same round-N-1 word.  `_arch_note` is called by the Core AND by
# every builder AND from `eco.py`, and against an opponent that keeps a body
# near us (mimic_istone: 36 builders) its S3 stamp changes every round, so it
# writes slot 13 every round.  Whichever unit acts LAST wins, and it wins with
# a word built from the stale read -- so the collar's fresh increment is erased
# unless the collar's writer happens to be the last unit of the team to move.
# In the fork's own measurement that happened sometimes, which is exactly why
# it reported a mean of 13.5 against a real spend of ~50: the fork was not
# measuring an overrun, it was measuring a broken counter.
#
# THE RULE THIS ESTABLISHES.  A field that is RE-DERIVED every round (the siege
# HP band, the raid heartbeat, the detector's own stamps) tolerates a lost
# write: the next round repairs it.  A field that ACCUMULATES cannot -- a lost
# increment is gone.  An accumulating field therefore may only live in a slot
# whose writers it can enumerate.
#
# So the counter lives in SLOT_RAID_LIVE (15) instead, whose ONLY writers in
# the whole tree are the two raid heartbeats in `_raid` -- and the collar's
# publish is FOLDED INTO those, so slot 15 still takes exactly one write per
# raider per round from one place.  Bits 0-9 stay the heartbeat (round+1 <=
# 1001 fits in ten bits); bits 10-27 are three six-bit LANES, one per raid slot
# modulo three.
#
# A LANE IS OWNED BY ONE BODY AND HOLDS THAT BODY'S OWN CUMULATIVE SPEND, not a
# team total, and that is what makes it survivable: a body republishes its own
# lane every round, so a lost write costs one round of latency and repairs
# itself, exactly like the re-derived fields above.  The budget test reads the
# OTHER lanes out of the store and its own from `self.col_spent`, which is
# exact, so a body is never wrong about itself and is at most one round stale
# about everybody else.  COLLAR_RACE_MARGIN is reserved against precisely that
# one round of other people's in-flight spending.
#
# RESIDUAL, written down rather than discovered: more than three collar bodies
# share lanes, and two bodies in one lane show as the later writer's figure
# rather than their sum -- an UNDER-count, so the direction is overspend.  The
# measured collar crew is 1-3 bodies (doctrine above: "we field 2-4 raid bodies
# against 8 seats", and only those inside COLLAR_ENGAGE_DSQ collar at all).
COLLAR_SPENT_SLOT = SLOT_RAID_LIVE
COLLAR_BEAT_MASK = 0x3FF    # bits 0-9 of slot 15: the raid heartbeat, round+1
COLLAR_LANES = 3
COLLAR_LANE_SHIFT = 10      # first lane starts here; lanes fill bits 10-27
COLLAR_LANE_BITS = 6
COLLAR_LANE_MASK = 0x3F     # one lane saturates at 63 Ti, twice the budget
COLLAR_BUDGET_SHARED = True
# BITS 28-29 OF THIS SLOT are the siege enemy-Core HP band (SIEGE_BAND15_SHIFT,
# the SIEGE block) -- moved here because slot 15's single writer is the one
# property that field also needed.  Same word, same one write per raider per
# round; 30-31 are still free.
# NOTE the T5 guard the fork carried here is gone with the slot: slot 15 is not
# SLOT_T5_BATT and never was.  Slot 13's collision with SLOT_T5_BATT is now
# somebody else's problem (`_sge_core_band`), and that field survives it because
# it is re-derived -- see the SIEGE block.

# TENDING -- and the first thing this plank measured about itself.
#
# The obvious tend gate is "any damage": a brick at 26/30 is healed back to 30
# for 1 Ti against the 2 Ti they spent, the 4:1 exchange.  BUILT THAT WAY IT
# LOSES, and the reason is the CURRENCY, not the titanium: a builder acts once
# a round, healing and building are the same action, and topping up a 26/30
# brick spends the round that would have sealed the next seat.  Same trap that
# killed _v178salt -- "buying denial with the one currency the collar cannot
# spare" -- reached from the other side.
#
# The count that says so, and the only figure here robust to the local
# engine's non-determinism because it is an action census rather than an
# outcome: built that way the collar spent 46.5 heals a game on the enemy's
# seat tiles against loki_turbo7's 13.5, while BOTH bots lost the same 0.17
# bricks a game to enemy fire (loki_collar vs loki_turbo7, mimic_istone, 6
# games each, tools/loki_collar_mechanism.py).  It was insuring, at a third of
# the raid's actions, against a risk that was not there.  The outcome metrics
# from that same run pointed the same way (3.50 seats bricked against 5.50,
# 1375 enemy Core HP healed against 751) but n=6 on a non-deterministic engine
# is not evidence and they are recorded as indicative only -- the Measure
# phase owns those.
#
# So tending is gated on the brick being GENUINELY AT RISK, not merely dented:
# 16 of a barrier's 30 HP, i.e. eight pecks in, which one +4 heal answers and
# which still leaves eight more pecks of margin.  Uncontested bricks are left
# alone and the action goes back to sealing.  Against an opponent that really
# does chew the collar the gate opens and the Q2.3 arithmetic (0.8 barriers
# lost per 100 rounds with healing vs 29-38 without) applies unchanged.
COLLAR_TEND_HP = 16
# ...and a brick this far gone outranks even laying a new one: the seat is
# already ours and re-taking it costs a barrier plus every heal that lands
# through the gap while it is open.
COLLAR_CRIT_HP = 8

# STATION SCORING (added to the existing distance score; lower is better).
# turbo7 scores a corner -6 while it has a seat left to open and +12 once it
# has none, which is what MOVES a body on to the next unsealed corner -- the
# first build of this plank replaced the +12 with a tend bonus, parked its
# bodies on the corners they had already finished, and measured worse on every
# collar metric (see the TENDING note above).  The parent's scoring is
# therefore kept exactly as it is, and the
# collar adds ONE case it does not have: a corner whose brick is under 16 HP
# is a TEND station and outranks opening a new seat, because a body is already
# invested there and the alternative is losing a seat we own.  A corner is
# orthogonally adjacent to exactly two seats and to no Core tile, so it is the
# only tile one body can tend two bricks from; heal is d^2 == 1, so there is
# no diagonal option and no cleverer geometry to find.
COLLAR_BRICK_BONUS = 6
COLLAR_TEND_BONUS = 10

# SPREAD -- the second thing this plank measured about itself.  Every other
# term in the near-phase station score is a distance, so once a raider is at
# the ring it keeps re-picking the corners it is already standing near, and the
# far side of the ring is never sealed: traced tile by tile on antler, seats
# (5,13) (6,14) (7,14) (8,13) were free for all 90 rounds of a won game while
# three bricks sat on the near side.  One corner per raid slot -- the same
# monotone issuer the far phase already dispersed on (SLOT_RAID_N) -- with a
# bonus large enough to outweigh the two-to-four tile walk around the
# footprint.  Its own flag because it is the risky half of the plank: walking
# a body around a defended Core is how raiders die, and the existing ban/stall
# machinery is the only thing catching that.
COLLAR_SPREAD_ON = True
COLLAR_SPREAD_BONUS = 8

# --- COLLAR_SQUAT: the MACRO / MACRO_WEAK branch ---------------------------
# Against a zero-turret opponent a body on a seat cannot be removed at all --
# builders cannot fire on builder bots -- so the seat costs 0 Ti to hold
# forever, and it blocks a spawn tile with it.  The detector classifies
# I Stone MACRO_WEAK 4/5 and never MACRO (S3 blocks MACRO: with 36 builders on
# the board someone is always within d <= 8 of us), so this branch triggers on
# MACRO or MACRO_WEAK, exactly as analysis/archetype_detector.md instructs.
# The classification is READ-ONLY here; only the Core writes slot 9.
#
# DEVIATION FROM THE BRIEF, recorded on purpose: the brief says "squat free
# seats INSTEAD of bricking".  We field 2-4 raid bodies against 8 seats, so
# squat-only can never seal.  What this implements is probe Q3.4's own verdict
# -- "brick the seats you can, squat the ones adjacent to your own healers":
# under squat a raider PREFERS a seat station and never gives it up, and
# bricking continues on the seats no body is holding (can_build_barrier
# refuses a tile our own body stands on, so the two policies cannot fight).
COLLAR_SQUAT_ON = True
# A squatter is worth healing earlier than a brick: 40 HP against a gunner's
# 7/round, and two healers pin it indefinitely at 33/40 (probe Q3.1).
COLLAR_SQUAT_HEAL_GAP = 4
COLLAR_SQUAT_BONUS = 6

# LAUNCHER_PLUCK is v2 and is NOT implemented: launcher spawn-deletion was
# refuted as a primary elsewhere in this tree (probe: worse than bricking).
# The flag exists so that a merge cannot silently acquire it.
LAUNCHER_PLUCK_ON = False

# MARKERS.  Transitions and events only -- print() is captured per unit per
# round and a per-round log is a real CPU line item.  Vocabulary:
#   COL brick (x,y) n=K   a NEW seat bricked; K = enemy seats now denied
#   COL reseal (x,y)      a seat we had bricked before, bricked again
#   COL tend (x,y)        started tending a brick (re-logged after a gap)
#   COL squat (x,y)       took a seat bodily under the MACRO branch
COLLAR_LOG_ON = True
COLLAR_LOG_GAP = 25         # rounds before the same tend marker re-logs


# --- COLLAR_SURGE: the terminal window ------------------------------------
# NEW IN bots/loki_leap (2026-08-16).  Not measured in the collar fork; added
# on the SIEGE fork's evidence (results/leap/loki_siege.md), which is about the
# way BOTH arms end their games rather than about either arm alone: the raid
# grinds the enemy Core down to a median of 14 HP and then STALLS there.  Two
# separate planks both arrive at the same wall, and the wall is healing --
# eight seats delivering +4 HP per titanium against one or two tubes at 9
# damage a round.  The terminal window is precisely where heal denial has to
# outbid healing, and it is the window in which our collar is out of budget.
#
# So: while the enemy Core is below SIEGE_MASS3_HP -- the SAME signal, read
# from the SAME source, as SIEGE_MASS_ON's third-tube trigger (`_sge_core_band`
# in raid.py; slot 13 bit 31) -- two things change.
#
#   1. THE BUDGET DOUBLES.  COLLAR_TI_BUDGET * COLLAR_SURGE_MULT.  This is the
#      live half: at the measured mean spend of 13.5 Ti a game the collar has
#      usually not exhausted 32 by the time the Core reaches 400, but the
#      terminal grind is exactly where it does, and stopping there is stopping
#      at the only moment the plank's arithmetic is decisive.
#   2. TEND IS PROMOTED ABOVE BRICK inside `_collar_act`.  Out of the terminal
#      window a new seat is worth more than topping up an old one, which is why
#      the measured ladder ranks BRICK second and ordinary TEND third.  Inside
#      it that inverts: a brick that falls re-opens a seat that heals +4 HP per
#      titanium for every round it stays open, and holding it costs 1 Ti against
#      the 3-5 Ti of laying a fresh one.  Breadth first while there is time,
#      depth first when there is not.
#
# NOTE WHAT IS *NOT* GATED HERE, because the brief for this merge asked for it
# and it was already true: collar tend/brick already outranks the parent's
# Core PECK unconditionally -- `_collar_act` is step 0 of `_raid_act` and the
# peck is step 1, in the collar fork as measured and in this merge unchanged.
# There is no reorder to gate; the surge would be reordering something that is
# already on top.  Recorded so a later reader does not "fix" it.
#
# HOW THIS LOSES.  The band is a shared latch and the enemy heals: a Core seen
# at 399 that is back at 500 next round leaves every raider that cannot see it
# surging on stale evidence until a body with eyes clears the bit.  That is
# bounded by the publish-on-transition rule (any established raider republishes
# every round it can see a Core tile) and it costs at most titanium, never a
# refusal.  The other cost is the obvious one: doubling a budget doubles the
# spend it caps, in the phase of the game where titanium also buys the third
# tube -- if sentinels-per-game falls while collar spend rises, this is why.
COLLAR_SURGE_ON = True
COLLAR_SURGE_MULT = 2


# ============================================================================
# TERMINAL WEAPONS (TW) -- bots/loki_leap3, 2026-08-16
# Spec: analysis/heal_wall_diagnosis.md sections 0, 3 and 4.
# ============================================================================
#
# WHAT THE DIAGNOSIS ACTUALLY SAYS, because every constant below is downstream
# of it (144 games, loki_leap v156 vs mimic_istones, 18 maps >= 20x20, both
# sides, seeds 1-4):
#
#   * There is NO terminal wall at 14 HP.  In 40 of 46 stalls their Core's
#     minimum HP over the whole game is >= 300 -- it is never dented at all.
#   * DAMAGE PER ROUND == HEAL PER ROUND, to two decimals, in 42 of 46 stalls;
#     median net 0.000 HP/round.  It holds at 3.1 HP/round and at 23.4.  The
#     wall is a SERVO that matches whatever we bring, up to a seat-limited
#     ceiling of 4 x manned seats (measured 22.9 median, 32.0 held for 337
#     rounds on midgard_A_s2), and its bank never empties (median 360 Ti).
#   * Our sustained damage is 9.4 HP/round in stalls.  A fourth tube costs
#     20 Ti/round of ammunition against a stall-class income of 7.29, of which
#     68 % is ALREADY ammunition.  Out-damaging the servo is unfundable.
#
# So the only lever left is the OTHER side of "4 x manned seats": buy SEATS,
# not damage.  Both weapons here buy seats; neither buys damage.
#
#   W3 PLUCK.  A Launcher picks up a builder bot of EITHER team inside d^2 <= 2
#     and throws it up to d^2 <= 26, every round, for zero titanium and zero
#     ammunition (engine_mechanics F, N.4).  A RING CORNER holds exactly two
#     heal seats inside that pickup disc and is NOT one of the eight seats, so
#     it sits outside mimic_istones._fouled_seats, which scans seats only.
#     -8 HP/round of enemy heal per launcher, for ~20-30 Ti ONCE and 0 Ti/round,
#     against our entire 4.9 Ti/round ammunition budget buying 9 HP/round.
#     And a plucked seat is FREE the same round, which is precisely what
#     can_build_barrier needs -- so the collar's existing BRICK arm converts
#     each pluck into a permanent brick.  That ratchet is what closes H1
#     (denial frozen at 1-3 of 8 seats by body occupancy) and H5 (148 pecks a
#     game, 0.00 bricks standing from r300 on midgard) with one building.
#
#   W1 GUNNER.  7 damage/round for 4 Ti/round kills a stationary 40 HP warden
#     in 6 rounds, and a gunner's ray resolves to the NEAREST occupant, which
#     beside a manned wall is a seated healer (engine_mechanics D, N.3, N.8).
#     It is the ONLY unit we field that can remove a body permanently -- a
#     builder cannot fire on a builder (E).  Seat then empty for their
#     WALL_GONE slot lapse plus a walk-in: about -4 HP/round sustained, or
#     -8 if they answer by counter-healing the target (two healers pinned off
#     the Core, which is the better trade for us).  Cap 1, and ranked below
#     the tube everywhere, because it competes with tube ammunition for the
#     starved conversion budget -- that is H3 and it is confirmed.
#
# W2 (OVERWHELM SURGE, a fourth tube) is REFUTED and deliberately NOT SHIPPED:
# 20 Ti/round of conversion against 7.29 Ti/round of income, and +4 HP/round
# over their ceiling even if funded.  SGE mass3 already fires 0.15 times a
# game in stalls and buys nothing.  There is no TW_SURGE flag; a later merge
# that wants one has to argue with this paragraph first.
#
# NOT THE REFUTED PLANK.  LAUNCHER_PLUCK_ON above refers to launcher
# SPAWN-DELETION (engine_mechanics N.7 -- throwing fresh builders off their
# spawn ring), measured worse than bricking and still False.  Plucking SEATED
# HEALERS off a manned wall is a different target, a different payoff, and has
# never been fielded.  The two flags are independent on purpose.
TW_ON = True                 # master flag.  False == bots/loki_leap exactly.
TW_PLUCK_ON = True           # W3, the launcher
TW_GUN_ON = True             # W1, the gunner

# --- THE GATE, shared by both weapons ---------------------------------------
# Both weapons are built AT THE ENEMY RING, forward, unescorted and unanswered.
# That is only true against the zero-turret class: a builder cannot damage a
# builder or a building at range, so a corner launcher and a ring gunner are
# untouchable except by 2-damage pecks from an adjacent body.  Against an
# opponent that fields turrets the same two buildings are free targets and the
# forward gunner is counter-batteried, so the gate is not a preference, it is
# the precondition for the arithmetic.  Six terms, ALL required:
#
#   1. archetype in (MACRO, MACRO_WEAK)  -- slot 9 bits 16-17, Core-only writer,
#      read-only here.  MACRO_WEAK is required because the detector reads
#      I Stone as WEAK 4/5 and never as MACRO (S3 blocks it).
#   2. zero enemy turrets seen.  STRICTER than the diagnosis's "within d <= 8
#      of their Core": any enemy Gunner or Sentinel this body has EVER seen
#      latches both weapons off for this body's whole life.  A raider is at the
#      ring, so its vision disc is a superset of the d <= 8 shell on the side
#      that matters, and the latch cannot be un-set by the turret walking out
#      of view (it cannot walk, but the raider can).
#   3. this body is ESTABLISHED at the ring AND the raid heartbeat is live
#      (slot 15 bits 0-9) -- a lone thrown body does not open a weapon.
#   4. an enemy Core FOOTPRINT tile in this body's own vision.
#   5. their manned seats >= TW_MIN_MANNED.  There has to be a wall to break;
#      below three seats the collar's bricks already outrun the healing.
#   6. round >= TW_MIN_RND.  After the opening, never during it: at r33 only
#      2.0-2.5 of 8 seats are theirs (H1) and the titanium is worth more in the
#      economy, which is the one thing that predicts kills at all (H3).
TW_MIN_RND = 60
TW_MIN_MANNED = 3            # of their eight seats, seen manned at once
TW_VIS_DSQ = SIEGE_BAND_VIS_DSQ    # builder vision r^2 == 20
TW_CENSUS_DSQ = LOKI2B_CENSUS_DSQ  # count OUR TW buildings inside this of them

# --- W3 LAUNCHER PLUCK ------------------------------------------------------
# SITE: ring CORNERS ONLY, never a seat.  A seat launcher is inside their
# _fouled_seats scan (they peck it) AND it costs the seat a 3-Ti brick could
# have held; a corner is outside the scan and covers two seats.  Four corners
# cover all eight seats = the whole 32 HP/round ceiling.
#
# PROGRESSION: the first launcher immediately once the gate is open; the second
# only after the first has STOOD TW_LAUNCH_AGE rounds -- the same survivorship
# rule, and the same constant, that the second tube already uses
# (SIEGE_MASS2_AGE).  Third and fourth on the same rule while their Core is
# above TW_LAUNCH_HP_FLOOR: below that the tubes are finishing it and another
# 10 % of cost scale buys nothing.
#
# BUDGET: its OWN ledger, and the ledger is the LIVE CENSUS, not a counter.
# The collar's lane field ACCUMULATES and may only live in a slot whose writers
# it can enumerate (DOCTRINE.md section 4); a launcher census is RE-DERIVED
# from vision every round and therefore needs no field at all.  The bank gate
# is bank >= launcher_cost + TW_LAUNCH_TI_FLOOR with the floor set to the
# forward Sentinel's own floor, so the launcher can never be the reason a tube
# was unaffordable.
#
# CAP 4 -> 2, `bots/loki_leap5` (DOCTRINE.md section 14), carried over from the
# wave-4 fork.  The section-12.6 A/B split the marginal launcher: 1-2 are the
# cheap measured half (-8 HP/r each of a 20.05 HP/r ceiling actually observed
# in the stall class, which two launchers already cover), while 3-4 were sized
# off the diagnosis's 32 HP/r THEORETICAL ceiling and were speculative from the
# start.  Each of 3-4 costs a further `floor(20 x scale)` at scale 3-4.4x out
# of the same bank the tubes and their ammunition come from.  The two
# speculative buys are withdrawn; the two measured ones stay.
TW_LAUNCH_CAP = 2            # leap5: was 4.  See the paragraph above.
# MEASURED CORRECTION to the diagnosis, and the one number in it that was an
# estimate rather than a measurement.  "~20-30 Ti once" is the BASE cost; the
# price actually paid is `floor(20 x scale)` and the scale at the round this
# gate opens (r140-360) is 3-4.4x -- probe `bots/probe_pluck` with TW_LOG_WHY,
# `TW why w=bank`: c=57, 60, 61, 72, 74, 88 across four games, against a bank
# whose median in the same window is 12-56 Ti.  At the spec's floor of 40 the
# arm demanded 97-128 Ti and was refused on 48-101 of the sampled rounds in
# every game -- i.e. the RANK 1 weapon was inert in exactly the class it was
# designed for.  The floor is therefore its own constant and it is set to
# SIEGE_MASS_TI_FLOOR's value, which is the tree's own measured "bank kept
# after a purchase made at the ring in the terminal phase".  Two reasons that
# is safe where 40 was for the tube: this arm cannot open before TW_MIN_RND,
# by which round every forward Sentinel that will ever be built has been
# (first tube r23 median, cap 3); and a launcher has ZERO running cost, while
# the 40 exists to leave a tube's 5 Ti/round of ammunition affordable.
TW_LAUNCH_TI_FLOOR = SIEGE_MASS_TI_FLOOR   # 6.  Was LOKI_FWD_TI_FLOOR (40).
TW_LAUNCH_AGE = SIEGE_MASS2_AGE          # 20, tube 2's survivorship clock
TW_LAUNCH_HP_FLOOR = 100     # no 3rd/4th launcher below this enemy Core HP
TW_FWD_LAUNCH_DSQ = 40       # a launcher this close to THEIR Core is a plucker
#
# THE THROW.  Targets are ENEMY builder bots only -- the pickup is team-blind
# and our own squatters sit on the two seats the corner covers, so the team
# test is the difference between a weapon and a self-inflicted exile.  A body
# standing on one of their seats is preferred over one merely passing.  The
# landing tile is the FARTHEST legal tile from THEIR Core inside d^2 <= 26, so
# the walk back is as long as the geometry allows (their bodies move one tile
# per round), and never within TW_THROW_CLEAR_DSQ of one of our own buildings:
# a warden dropped beside our forward Sentinel pecks it for the rest of the
# game, which would hand back more than the pluck took.
TW_THROW_CLEAR_DSQ = 2       # keep victims off our own buildings' doorsteps
TW_THROW_MIN_DSQ = 9         # a landing nearer than 3 tiles is not worth a throw
#
# THE WALK.  A builder builds on an ORTHOGONALLY adjacent tile, and a corner is
# DIAGONAL to every other corner -- so a raider standing on a corner (which is
# where the collar's own station scoring puts it, `COLLAR_BRICK_BONUS`) can
# never lay this building at all.  Measured, same probe, `TW why w=site`: 36 /
# 6 / 5 / 3 refused rounds per game with the bank at ti=150, 123, 112, 109
# against c=88, 74, 72, 60 -- rich rounds thrown away for want of one step.
# So the launcher gets a walk-to of exactly the shape T5_NEST_WALK_ON already
# uses for the Sentinel nest: while the gate is open, the bank affords one and
# none stands, this raider's station becomes a tile beside a FREE corner.  It
# yields (returns None) the moment any of those stops being true, so it can
# never hold a body off the collar for longer than it takes to buy the
# building -- and the building is worth 8 HP/round of their heal, against the
# 4 HP/round one more brick would deny.
TW_LAUNCH_WALK_ON = True
TW_LAUNCH_WALK_DSQ = 100     # the walk only engages inside this of their ring
#
# THE RATCHET.  A plucked seat is free the same round, and the collar already
# polls can_build_barrier on every adjacent seat every round -- so the brick
# arm needs no new code path, only budget.  Turn order gives it for free: our
# raiders are spawned early and act BEFORE a launcher built at r >= 60 (ids run
# in creation order), so the brick lands the round AFTER the pluck, by which
# time the victim is still 4-5 tiles out.  COLLAR_TI_BUDGET is 32 and a game
# that plucks two seats a round for 200 rounds cannot be financed out of it, so
# a launcher standing at their ring raises the collar's cap by TW_COLLAR_BONUS.
# DEVIATION, recorded: the diagnosis asks for the bonus on "seats adjacent to
# one of our launchers".  It is applied at the RING level instead -- a corner
# launcher covers two of the eight seats and the collar body cannot cheaply
# attribute a seat to a launcher it may not be able to see.  The cost of the
# looser form is at most TW_COLLAR_BONUS titanium spent on the other six seats,
# which are worth the same +4 HP/round each.
TW_COLLAR_BONUS_ON = True
TW_COLLAR_BONUS = 24         # extra collar Ti while one of our launchers stands

# --- W1 GUNNER-ON-HEALERS ---------------------------------------------------
# CAP 1, and never before a tube bears: this arm spends the same starved
# conversion budget the tubes do (H3), so it is ranked below them in the raid
# ladder, gated on the same bank floor, and capped where the arithmetic still
# clears (7 damage for 4 Ti = 1.75 dmg/Ti against a Sentinel's 1.8).
#
# SITING.  The ray is 3 tiles on a cardinal facing and 2 on a diagonal
# (engine_mechanics D), it stops at the NEAREST occupant, and WALLS block it.
# A ring CORNER facing along the ring covers the TWO seats on that side --
# corner (ox-1, oy-1) facing EAST covers (ox, oy-1) and (ox+1, oy-1), both
# seats.  That is the 2-seat post and it is ranked first.  The same corner
# facing the footprint DIAGONAL puts a Core tile first in the ray with nothing
# able to stand between -- 7 HP/round of unblockable Core damage at 1.75
# dmg/Ti -- and that is the fallback when no 2-seat facing is legal.
#
# Never on a seat (a seat is worth a brick, and a gunner there blocks it
# permanently), never on a facing whose first ray tile already holds one of OUR
# buildings (_turret refuses to fire on our own team, so such a gunner is
# simply mute), and never where a wall stands before the first seat.
# Re-aiming is the parent's own ROTATE_DISCIPLINE_ON arm: 10 Ti, only for a
# facing that lands, only when the current one does not.
TW_GUN_CAP = 1
TW_GUN_TI_FLOOR = LOKI_FWD_TI_FLOOR   # 40, as the tube
TW_GUN_MIN_TUBES = 1         # never before the first forward Sentinel stands
TW_GUN_MAX_DSQ = 13          # post within ~3 tiles of the footprint (ray reach)
TW_GUN_DMG = 7               # measured gunner damage, for the kill marker
TW_GUN_RAY_CARD = 3          # cardinal ray length
TW_GUN_RAY_DIAG = 2          # diagonal ray length
#
# AMMUNITION.  A forward gunner is invisible to the Core and to SLOT_HOME_GUN
# alike, and a gunner nobody budgets for is a gunner with an empty magazine --
# the same defect SCREEN_ON's allowance exists for.  One bit of slot 15
# (bit 30, above the band) carries "a TW gunner stands at their ring", written
# by _raid_beat, which is that slot's ONLY writer, on the same
# re-derive-or-republish discipline as the HP band: a raider that can see the
# ring publishes what it counts, a blind one republishes what it read.  The
# Core adds TW_GUN_BURN to the JIT burn term when the bit is set.  This is
# "after the tubes" in the only sense the engine has: the ammunition pool is
# global and undifferentiated, so priority is expressed at the BUILD (the
# gunner is ranked below the tube in _raid_act and shares its bank floor),
# never by an ordering inside a single conversion.
TW_BEAT_GUN_SHIFT = 30       # slot 15 bit 30.  Bit 31 stays free (sign safety).
TW_BEAT_GUN_BIT = 1 << TW_BEAT_GUN_SHIFT
TW_GUN_BURN = SIEGE_JIT_GUN_BURN     # 4 ammo/round, as any firing Gunner

# --- TW_RESERVE_ON: the PER-WEAPON reservation (bots/loki_leap5) ------------
# DOCTRINE.md section 14.  This flag exists because of two measurements that
# have to be honoured at the same time, and wave 4 honoured only one of them.
#
# MEASUREMENT 1 (section 12.6, wave 3).  leap3's terminal weapons are the only
# thing in the campaign that moved the istones cell: +4.1pp (65.9 vs 61.9),
# stalls 34.3 -> 28.7 %, stall-class enemy-core min HP 462 -> 308, and the
# mechanism behind it is bulk -- 44 of 108 games built a weapon, 57 launchers,
# 3 712 plucks.
# MEASUREMENT 2, the cost, same run: our forward Sentinels at terminal fell
# 2.53 -> 2.17.  The weapons were partly paid for out of the tubes, and
# `heal_wall_diagnosis.md` 3 says lowering their ceiling is worth nothing while
# our damage is one tube.
# MEASUREMENT 3 (wave 4, `bots/loki_leap4`, results/wave4/tw_weapons.txt).  The
# fix tried there was TW_TUBES_FIRST, a GLOBAL budget order in front of BOTH
# weapons: 2 tubes standing AND ten rounds of their ammunition still affordable
# after the buy.  It protected the tubes (terminal 2.44 vs the 2.48 of the same
# run's control) by CANCELLING THE MECHANISM -- games with any weapon
# 44/108 -> 10/108, launchers 57 -> 8, plucks 3 712 -> 347, i.e. 77-91 % of the
# thing being protected was destroyed to protect it.  Net: a wash.
#
# WHAT THE THREE TOGETHER SAY.  The order was right about the SECOND weapon and
# wrong about the FIRST.  The two halves of the mechanism are not the same
# purchase:
#   * LAUNCHER #1 is the cheap half.  `floor(20 x scale)` ONCE -- measured
#     c=57-88 at the rounds this gate opens -- and ZERO per round, for -8 HP/r
#     (and -16 with #2) off a ceiling observed at 20.05 HP/r in the stall class.
#     It cannot starve a tube's ammunition because it consumes no ammunition,
#     and TW_LAUNCH_TI_FLOOR already keeps a tube's own bank floor intact at
#     the moment of the buy.  Making it wait for two standing tubes AND a
#     100-Ti ten-round magazine reserve is what emptied the fixture: in the
#     income-poor stall cells those two conditions are exactly what is missing,
#     and they are the cells the weapon was built for.
#   * LAUNCHER #2 AND THE GUNNER are the expensive half.  #2 buys the same
#     -8 HP/r for a second scaled price out of the same bank; the gunner buys
#     it for a scaled price PLUS TW_GUN_BURN = 4 ammo/round drawn from the very
#     conversion pipe the tubes drink from (H3).  These are the purchases whose
#     bill lands twenty rounds later as a conversion the Core declines, which
#     is the leak section 12.6 measured, and they are the ones that must prove
#     the tubes are funded before they are made.
#
# SO THE RESERVATION IS PER WEAPON, not global.  Same arithmetic as wave 4's,
# same two terms, applied at a different place:
#   (a) at least TW_RESERVE_MIN_TUBES forward Sentinels STANDING (live census
#       `_tw_tubes`, the two-step `_live_fwd_guns` -> SLOT_FWD_GUN the gunner's
#       TW_GUN_MIN_TUBES already performs).  A body that cannot count refuses:
#       an unknown census must not read as "the order is satisfied".
#   (b) the titanium projected to remain AFTER this purchase still covers what
#       the JIT pipe must convert to keep those tubes firing for
#       TW_RESERVE_RNDS rounds:
#           need = max(0, RNDS * SENT_BURN * tubes + own_burn - global_ammo)
#       and the test is `bank - cost >= need`.  No new state: `_sge_jit`'s own
#       burn term, 1 Ti -> 1 ammo, magazine already standing credited.
# APPLIED TO: launcher builds number TW_RESERVE_FREE_LAUNCHERS+1 and up (so
# with the constant at 1, launcher #2 -- launcher #1 keeps leap3's conditions
# EXACTLY, gate + cap + survivorship + HP floor + TW_LAUNCH_TI_FLOOR, and no
# new term at all), and to the gunner ALWAYS, with burn_extra = TW_GUN_BURN.
# The launcher census used is `_tw_census`'s live count, the same n the cap and
# the survivorship clock already use, so "how many are standing" is asked once.
#
# COST: nothing per round.  (a) reuses a census the gunner arm already takes;
# (b) is two accessor reads and arithmetic, and both run only after every
# cheaper refusal in each arm has returned.
#
# RISK, pre-registered, and it is the mirror of wave 4's: this is LOOSER than
# TW_TUBES_FIRST and stricter than leap3, so the failure mode is that the
# freed launcher #1 re-imports the tube tax on its own.  The counter-check is
# the pair of numbers this fork is measured on -- weapons per game must stay in
# leap3's band (44/108 games, not leap4's 10/108) AND forward Sentinels at
# terminal must not sit materially below leap3's own 2.17.  If both hold, the
# split was real; if tubes are unchanged at 2.17 the gate is only touching
# purchases that were not the ones taxing them and the plank is a null.
# TW_RESERVE_ON = False restores section 12 (leap3) behaviour exactly, apart
# from TW_LAUNCH_CAP.
TW_RESERVE_ON = True
TW_RESERVE_MIN_TUBES = 2     # forward Sentinels standing before a GATED weapon
TW_RESERVE_RNDS = 10         # rounds of tube fire the bank must still cover
TW_RESERVE_FREE_LAUNCHERS = 1  # launchers built before the gate applies at all
# SUB-FLAG, so the fork's two halves are separately ablatable -- the project's
# method is flag ablation and a plank that can only be measured whole is a plank
# nobody can retire (doctrine.py's own rule for adding a flag).  Down = the
# gunner keeps leap3's conditions and only launcher #2 is reserved.  It exists
# because the first measurement of this fork found the gunner arm going from 15
# builds in 60 games to ZERO: the gunner pays TW_GUN_TI_FLOOR (40) AND a
# reservation of 10 x (5 x 2 + 4) = 140 Ti, which the stall class never holds.
TW_RESERVE_GUN = True        # gate the gunner as well as launcher #2

# --- MARKERS ----------------------------------------------------------------
# Transitions and events only; print() is captured per unit per round and a
# per-round log is a real CPU line item (DOCTRINE.md section 7).  Vocabulary:
#   TW gate r=R m=M          the round the gate first opened; M = manned seats
#   TW launch (x,y) n=K      a TW launcher built on a ring corner; K = census
#                            BEFORE this build, so n=0 is the first
#   TW pluck (x,y)->(x,y)    an enemy body thrown off the ring
#   TW gun (x,y) f=D s=N     the TW gunner built; N = seats in its ray
#   TW gunkill (x,y)         a shot that takes an enemy builder bot to <= 0
#   TW resv r=R t=T need=N   the round TW_RESERVE_ON first RELEASED a GATED
#                            weapon for this body; T = tubes standing, N = the
#                            Ti reserved for their next TW_RESERVE_RNDS rounds
#                            of fire.  One line per body per game.  Unlike wave
#                            4's `TW tfirst` its absence is NOT a failure --
#                            launcher #1 is ungated and prints `TW launch n=0`
#                            without ever reaching this test, which is the
#                            whole point of the fork.  Read the two together:
#                            `TW launch n=0` present and `TW resv` absent means
#                            the cheap half fired and the expensive half was
#                            correctly refused.
TW_LOG_ON = True
TW_PLUCK_LOG_GAP = 10        # rounds between pluck markers (n= carries the count)
TW_PLUCK_LOG_ALL = False     # probe grade: log EVERY pluck and seat census
# PROBE GRADE, default OFF.  `TW why r=R w=WHY ti=T c=C n=N` -- the reason the
# launcher arm declined this round, rate-limited to TW_WHY_GAP.  WHY is one of
# cap / age / hp / bank / site / tubes / pipe -- the last two are
# TW_RESERVE_ON's and are shared with the gunner arm (`c=` on a `pipe` line
# carries cost + the reservation, so `ti` vs `c` reads as the shortfall).
# It exists because "the weapon did not fire" is
# not a diagnosis, and the answer turned out to be a constant nobody had
# measured (the SCALED launcher cost -- see TW_LAUNCH_TI_FLOOR).
TW_LOG_WHY = False
TW_WHY_GAP = 40


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
LOKI_SAMESTOP_LOG = False       # leap6: OFF by default (Sleipnir ships True).
                                # Flip to True for ONE probe game only.


# ============================================================================
# LOKI-BODYAWARE (#63) -- "a body can move, a wall cannot".  Ported from
# mate_sleipnir's hand-merged `_bfs_direction` (eco.py); see the HAND-MERGED
# BLOCK comment there for the mechanism.  In one line: the navigation flood
# runs TWICE -- pass 0 treats builder-bot bodies of EITHER team as soft
# obstacles and routes around them, pass 1 drops the bodies and repeats, and
# pass 1 runs ONLY if pass 0 exhausted without reaching a goal.  Both passes
# are charged to ONE NAV_NODE_BUDGET and the CPU probe is asked once per CALL,
# so the worst case is the parent's cost plus one extra flood on the maps
# where the parent was walking into a queue of its own builders anyway.
#
# THE FLAG IS OURS, NOT SLEIPNIR'S.  Sleipnir ships this plank UNGATED and
# unflagged, fused with SAMESTOP into a single bot, so nobody has ever
# measured which of the two carries the gain (team_bot_recommendation.md 3b,
# "Ablation, cheap and worth it").  leap6 gates it on ONE condition -- the
# `elif et == EntityType.BUILDER_BOT and LOKI_BODYAWARE_ON` branch of the
# entity scan -- because that is the whole plank's entry point:
#
#   * ON  == mate_sleipnir's `_bfs_direction` character-for-character.
#   * OFF == `bodies` stays empty, so pass 0 stamps nothing extra, pass 1
#            breaks out before doing any work, and both `continue`s fall to
#            the same `p.cardinal_direction_to(target)` the parent returned.
#            BUILDER_BOT is NOT in BFS_BLOCKING_TYPES, so falling through the
#            elif chain leaves bodies unblocked exactly as in loki_leap5.
#            I.e. flag-off is leap5's single-pass semantics, not an approximation.
# ============================================================================
LOKI_BODYAWARE_ON = True        # the whole plank; False == loki_leap5 exactly

# ---- hand-merged by builder s47 from: loki_leap5 (this tree), samestop (_v464samestop via mate_sleipnir), bodyaware (_v242bodyaware via mate_sleipnir)
# The two marker lines below are mate_sleipnir's own and are carried over
# INTACT, not rewritten: tools/dash/serve.py (_COMPOSED_FROM_RE) and
# tools/auto_gate.py (combo_of) on the teammate's side require that exact
# phrasing, and leap6 carries both of those planks verbatim.  leap6 adds
# nothing to _bfs_direction beyond the LOKI_BODYAWARE_ON gate documented
# above; the SAMESTOP methods and both _expand hooks are byte-for-byte
# mate_sleipnir's.
# ---- composed by tools/stack.py from: turbo (_x3r0v152), bodyaware (_v242bodyaware), samestop (_v464samestop)
# ---- hand-merged by builder s46 from: turbo (_x3r0v152), bodyaware (_v242bodyaware) — _bfs_direction flat-grid two-pass
# NOT produced by tools/stack.py: the two planks both REWRITE _bfs_direction, so
# stack.py's whole-statement AST merge cannot express this one.  The marker line
# above uses stack.py's literal phrasing on purpose -- tools/dash/serve.py
# (_COMPOSED_FROM_RE) and tools/auto_gate.py (combo_of) both require it verbatim,
# and a hand-merge that reads as a SOLO would be scored against the wrong bar.


# ============================================================================
# PLANK SOCKET-GUARD (SG) -- 2026-08-17, loki_leap7.
#
# THE ATTACK IT ANSWERS, and it is the one beating v155 on the ladder TODAY
# (analysis/launcher_meta.md, fresh corpus 2026-08-17, 505 games):
#
#   Juusto v13 ferries a builder into our base by turn ~14 (build launcher ->
#   throw its own builder r^2<=26 -> self-destruct the launcher, refunding the
#   +10% scale; 325 launchers, 321 throws, 100% own bots, 100% recycled, median
#   2 rounds of life, 5.7 tiles a hop).  gsxWins v53 walks the same builder in
#   on foot behind an early gunner (its first gunner is turn 9; ours is 68).
#   The ferried builder then plants 3-Ti BARRIERS on the eight tiles
#   orthogonally adjacent to our 2x2 Core -- the SOCKETS -- which are the only
#   tiles a conveyor can deliver into the Core from (engine_mechanics B), and
#   kills the one conveyor we have plugged in.
#
#   Measured, ours vs Juusto (10 wins / 15 losses):
#
#       our feeder conveyors on sockets   2.25  /  0.45
#       enemy buildings on sockets        2.43  /  4.78 (max 6.4)
#       rounds with ZERO feeder           15.6% /  72.4%
#       core deliveries                   131.6 /  22.9
#       our Ti->ammo                      619   /  89
#       our sentinel shots                50.3  /  6.1
#
#   And Ti->ammo separates the results PERFECTLY at ~300: 0/15 wins below it,
#   10/10 above.  Everything in this plank is upstream of that one number.
#
# WHY THE ECONOMY COLLAPSES ENTIRELY rather than degrading: a conveyor whose
# output tile is empty ground HOLDS its stack forever and blocks everything
# upstream (engine_mechanics B).  Killing the ONE tile where our line touches
# the Core does not slow the line down, it stops the whole line, permanently,
# until that tile is re-laid.  Our median first feeder is turn 10-14; their
# first socket barrier is turn 11-18.  It is a race we currently do not know
# we are in.
#
# FIVE ARMS, five sub-flags under one master, because they have very different
# priors and measurement must be able to kill them one at a time.
#
#   SG_TWO_FEEDERS   Claim delivery sockets on >= 2 DIFFERENT Core FACES, so no
#                    single kill unplugs us.  In our wins we hold 2.25 feeders;
#                    in our losses 0.45.
#
#                    /!\ A CONVEYOR CANNOT FORK.  It has ONE output tile and
#                    accepts from its other three sides (engine_mechanics B),
#                    so a "spur off the trunk" that receives anything is
#                    impossible without re-facing a trunk link -- which breaks
#                    the line it forked from -- or a splitter, which nothing in
#                    this tree builds and which nobody in 280 games has built.
#                    So face diversity is bought the only two ways the engine
#                    allows: (a) the SECOND trunk chain is ROUTED to a socket on
#                    an unfed face (goal biasing inside the incumbent
#                    `_link_path`, zero extra titanium, capped detour), and
#                    (b) a one-tile STUB conveyor on a free socket that is
#                    already orthogonally adjacent to one of our harvesters --
#                    a harvester feeds any adjacent acceptor directly, so that
#                    stub is a complete second line for one conveyor.
#
#   SG_SELF_FILL     Fill sockets we will never use with OUR OWN 3-Ti barriers.
#                    Nothing can be built on an occupied tile, so ~12-15 Ti
#                    makes the whole blockade impossible on the tiles it buys.
#                    /!\ THE REAL COST IS NOT THE TITANIUM.  The eight sockets
#                    are also our eight HEAL SEATS -- the only tiles a builder
#                    can stand on to heal the Core -- and are 8 of the 12 spawn
#                    tiles.  Bricking them denies the enemy and ourselves in
#                    equal measure, so SG_FILL_FREE_MIN is a hard floor on how
#                    many non-feeder sockets are left open, and the whole arm
#                    lives in a short window (turns 8-16) with a team-wide
#                    titanium cap.  This is the arm most likely to measure
#                    negative; it is separately flagged for exactly that reason.
#
#   SG_FEEDER_REBUILD  A dead feeder is the TOP economy priority next round.
#                    The socket race is decided in 1-5 rounds: in every loss
#                    where we did plug in, the feeder was destroyed and the
#                    socket barriered within 1-5 rounds.  The CORE runs the
#                    census -- all eight sockets are permanently inside its own
#                    vision, which is true of no other unit we own -- and
#                    publishes ONE 4-bit request in the top nibble of slot 9
#                    (bits 28-31, free since the merge, Core-only writer, see
#                    DOCTRINE 6).  The request is a SOCKET INDEX+1 into the
#                    fixed eight-tile order, 0 == "we are fed, do nothing".
#                    Builders answer it; `_link_path` also biases its trunk goal
#                    toward it, which is how one field serves both this arm and
#                    SG_TWO_FEEDERS without a second slot.
#
#   SG_CORNER_LAUNCHER  ONE launcher on a Core-ring DIAGONAL CORNER, under the
#                    detector's S3 signal (an enemy builder seen within d<=8 of
#                    our Core), by ~turn 15.  Pickup is r^2<=2 (re-verified on
#                    4907 throws), so a corner covers the two sockets flanking
#                    it plus the ring tiles around it, and a corner is not
#                    itself a socket so it costs no delivery tile.  Every one of
#                    the 107 socket builds in our losses was placed by a builder
#                    standing inside r^2<=26 of our Core centre -- i.e. inside a
#                    defensive launcher's throw envelope.  Eviction costs 20 Ti
#                    ONCE, zero ammunition, and may fire EVERY round.
#
#                    /!\ THIS REPLACES leap5's SEAT-PLUCK SITING, it does not
#                    add to it.  leap5 built 73 launchers across 155 ladder
#                    sides, ZERO of them before turn 100 (median turn 255), at a
#                    median 8.3 tiles from our own Core -- outside the r^2<=2
#                    pickup disc of anything that matters -- for 8 throws in
#                    total.  The mechanism was never wrong; the site and the
#                    clock were.
#
#   SG_RING_TURRET   One gunner near the ring under the same S3 trigger.
#                    Turrets are the ONLY thing that can damage a builder bot
#                    (engine_mechanics E), so without one we cannot contest an
#                    intruder at all; gsxWins' first gunner is turn 9.
#                    /!\ HOME DEFENCE HAS MEASURED NEGATIVE HERE BEFORE --
#                    T5_HOME_GUNNER_ON is False in this very file for that
#                    reason.  That refutation predates the socket-attack meta
#                    and was measured against opponents who were not trying to
#                    seal our sockets.  Kept a SEPARATE flag so a measurement
#                    can kill this one arm without touching the other four.
#
# MARKERS (SG_LOG, local replays only -- the platform strips stdout):
#   SG feeder2 (x,y)   a second-face socket claimed
#   SG fill (x,y)      one of our own bricks laid on a socket
#   SG rebuild (x,y)   a feeder conveyor re-laid on a requested socket
#   SG evict (x,y)     an enemy body thrown off our ring
#   SG gun (x,y)       the ring turret built
#   SG launch (x,y)    the corner launcher built
# ============================================================================

SG_ON = False

# --- arm 1: two feeders, two faces -----------------------------------------
SG_TWO_FEEDERS = True
SG_FEED_WANT = 2             # live feeder sockets wanted, on DISTINCT faces
SG_FEED2_RND = 120           # keep trying to open the second face until here
SG_FEED2_DETOUR = 3          # extra conveyors a face-diverse trunk may cost.
                             # Each link is 1 Ti, +1% team cost scale FOREVER
                             # and one round of delivery latency, and the long
                             # maps already spend 9-15 links on the first
                             # chain (glacierkeep's nearest ore is r^2 = 89);
                             # above 3 the second face is not worth its own
                             # scale and the unbiased route is kept.
SG_STUB_ON = True            # the harvester-adjacent one-tile second line
SG_STUB_RND = 200            # a stub after this is not worth the scale

# --- arm 2: self-fill ------------------------------------------------------
SG_SELF_FILL = True
SG_FILL_MIN_RND = 8          # before this the titanium is the economy
SG_FILL_MAX_RND = 40         # their first socket barrier lands turn 11-18, but
                             # the arm cannot open until a feeder is LIVE and
                             # our first feeder lands r14-29 locally, so a
                             # turn-16 close made the arm dead code.  They keep
                             # bricking all game (4.78 mean, 6.4 max), so a
                             # brick at r30 still denies a tile they would take.
SG_FILL_TI_CAP = 15          # team-wide, at the BASE 3 Ti price (5 bricks)
SG_FILL_FREE_MIN = 1         # spare sockets left OPEN beyond the reserved
                             # delivery seats, the Core's live request and any
                             # socket a belt/harvester of ours already touches.
                             # A FEEDER does not cost a heal seat -- conveyors
                             # are bot-passable (engine_mechanics G) so a body
                             # can stand on one and heal -- but a BRICK does,
                             # and it costs a spawn tile too.
SG_FILL_ENEMY_FACE_ONLY = True  # only the Core face nearest THEIR Core is
                             # eligible -- see `_sg_fill`.  Caps the arm at the
                             # 2 sockets of one face / 6 Ti, and keeps it off
                             # the faces our own trunk chains terminate on.
SG_FILL_MAX_PER_UNIT = 2     # bounds the re-lay loop if a brick is shot out
SG_FILL_TI_FLOOR = 12        # never take the bank below this for a brick

# --- arm 3: feeder rebuild -------------------------------------------------
SG_FEEDER_REBUILD = True
SG_FEED_SHIFT = 28           # slot 9 (SLOT_HEAL_BUDGET) bits 28-31.  CORE-ONLY
SG_FEED_MASK = 0xF           # writer, per DOCTRINE 6; 0 == no request
SG_REBUILD_BAND_DSQ = 100    # only a body already within 10 tiles is recalled
SG_REBUILD_WALK_CAP = 36     # lifetime cap per body on rounds spent diverting
SG_REBUILD_WALK_RNDS = 12    # and it walks toward the socket for at most this
                             # many rounds per request -- recalling the economy
                             # on a latch once finished a game with 0 Ti
                             # delivered (see the T4 BLEED BEACON note above)

# --- arm 4: the corner launcher --------------------------------------------
SG_CORNER_LAUNCHER = True
SG_LAUNCH_MIN_RND = 6        # their ferry lands turn ~14; median first Juusto
                             # launcher is turn 11
SG_LAUNCH_TI_FLOOR = 30      # a much lower bar than LAUNCHER_RESERVE (80):
                             # under S3 this IS the defence, not a luxury
SG_S3_FRESH = 60             # rounds an S3 sighting stays a trigger (ARCH_MEMORY)
SG_THROW_CLEAR_DSQ = 2       # never drop a victim beside one of our buildings
SG_THROW_MIN_DSQ = 5         # and never within ~2 tiles of our own Core
SG_THROW_TOWARD_ENEMY = True  # among equally-far sites, pick THEIR side

# --- arm 5: the ring turret ------------------------------------------------
SG_RING_TURRET = True
SG_GUN_MIN_RND = 10          # standing by ~turn 20
SG_GUN_TI_FLOOR = 20
SG_GUN_SITE_DSQ = 9          # within 3 tiles of the footprint...
SG_GUN_OFF_RING = True       # ...but never ON the 12 ring tiles: those are our
                             # heal seats, our delivery sockets and our spawn
                             # tiles, and a turret is an impassable building
SG_GUN_NEAR_DSQ = 1          # the ray must cover a ring tile...
SG_GUN_FAR_DSQ = 16          # ...out to 4 tiles, which is the approach

SG_LOG = True                # the markers above; local instrument only


# ============================================================================
# PLANK CAGE (CG) -- 2026-08-17, loki_leap7, on top of PLANK SOCKET-GUARD.
#
# SOCKET-GUARD is the DEFENSIVE half of the same geometry: it keeps their
# ferried builder off OUR eight sockets.  This plank is the OFFENSIVE half --
# analysis/meta_2000.md mechanisms #1 + #2 + #3 + #4, taken as one package
# because they are one machine and each is close to worthless without the rest.
#
# THE MEASUREMENT, 505 fresh ladder games / 1010 game-sides:
#
#   enemy ring12 sealed (max) |  n  | win% | heal ratio | siege length
#   --------------------------+-----+------+------------+-------------
#     0-3                     | 326 |  27% |   0.57     |   104
#     7-9                     | 278 |  58% |   0.45     |   141
#    10-11                    | 114 |  81% |   0.04     |   100
#    12/12                    |  55 |  93% |   0.00     |    63.5
#
#   and ORDERING is a second, separable +46/+49: sides where the seal PRECEDED
#   the first damage to their Core won 93% (n=70).  Jython reaches seal>=10 at
#   r56 and opens fire at r70 (+8.5 rounds of lead); WE reach it at r84 and
#   open fire at r56 -- a lead of MINUS 27 rounds.  We hand the defender the
#   entire window to heal and re-seat, and then wonder why 500 HP of Core costs
#   us up to 1206 raw hits.
#
#   The conversion number is what makes this a plank and not a rebuild: at
#   seal>=10 WE win 83% and Jython wins 85% -- statistically indistinguishable.
#   We simply reach it in 34% of games against their 91%, and we hold it a
#   median of ZERO turns against their 77.
#
# FOUR ARMS.
#
#   CAGE_FERRY   The delivery system (meta_2000 #3, +33/+41).  A raider builds
#                a launcher on an adjacent tile, stands still one round, and is
#                thrown r^2<=26 (5.7 tiles) toward their Core by our OWN
#                launcher; the launcher then self-destructs, which refunds its
#                +10% scale contribution (engine_mechanics K) so the permanent
#                price of a hop is floor(20 x scale) titanium and nothing else.
#                Repeat.  Measured on Jython: 31 tiles in 11 rounds, ~2.9
#                tiles/round against a walk's 1.0, arriving at full HP.
#
#                /!\ TURN ORDER IS THE WHOLE DESIGN.  Units act in CREATION
#                order and a building does not act on the round it is built
#                (engine_mechanics H).  The raider has a LOWER id than the
#                launcher it builds, so it acts FIRST and the launcher throws
#                it AFTER its own turn -- which is why the rider must simply
#                not walk away on the throw round, and why the cycle is two
#                rounds per hop rather than one.  `bots/probe_ferry` settles
#                the last unknown, and it was run for this plank:
#                `self_destruct()` on a LAUNCHER works, refunds the scale
#                (140% -> 140% across a destroy plus a rebuild), may be called
#                in the same round as the throw, and TERMINATES THE UNIT'S TURN
#                IMMEDIATELY -- no statement after it ever runs, so it is
#                always the last call in its branch.
#
#   CAGE_SEAL    The cage itself (meta_2000 #1, +41/+46).  The collar already
#                bricks their eight HEAL SEATS; ring12 is those eight plus the
#                four DIAGONAL CORNERS, and the corners are the half we have
#                never taken.  Seats deny HEALING; corners on their own deny
#                nothing -- but ring12 is also the SPAWN ring, and 12/12 is the
#                state in which their Core can no longer produce a body to
#                break the seal with.  That is the whole difference between the
#                10-11 row (81%) and the 12/12 row (93%).
#
#                /!\ ORDER INSIDE THE ARM IS NOT COSMETIC.  Jython's own loss
#                `eed95e8e_g3` held 12/12 for 228 rounds at heal ratio 1.00 and
#                lost: it had sealed the SPAWN tiles and left heal seats open.
#                CAGE_RING8_FLOOR is the answer -- no titanium is ever spent on
#                a corner until at least six of the eight seats are held.
#
#   CAGE_BEFORE_SIEGE   The ordering (meta_2000 #2, +46/+49).  While the seal
#                is below CAGE_SEAL_GATE, nothing we own fires at their CORE:
#                not the forward Sentinels (which may still be BUILT and sited
#                -- they simply take another target or hold), and not a
#                raider's 2-damage peck.  Every other target stays legal.
#                Opened by seal >= gate, or by CAGE_SEQ_TIMEOUT, which exists
#                because of Jython's OTHER loss shape: `73867571_g4` held a
#                full seal for 855 rounds, ran to the r1000 cap and lost the
#                titanium tiebreak.  A cage with no finisher is a loss.
#
#   CAGE_EVICT   The launcher at their ring (meta_2000 #4, +22/+37), which is
#                TW's pluck with two corrections: the victim set widens from
#                their eight seats to all twelve ring tiles, and the gate that
#                kept the launcher off the board until r60 under a MACRO
#                classification is replaced, FOR THE LAUNCHER ONLY, by "a
#                raider is established at their ring".  `ph` is the null
#                control that makes this arm honest: it builds launchers too
#                (1.5/game, 92% of sides), uses them for forward throws only,
#                bricks 1 ring tile and wins 42%.  A launcher that does not
#                orbit their Core is worth nothing.
#
#                CAGE_HOP is the same launcher aimed at OUR OWN body: a
#                tangential throw from one ring station to another.  It is the
#                genuinely novel part -- to brick a ring tile you must stand
#                orthogonally adjacent to it, the 2x2 footprint blocks the
#                short path across, and walking the shell costs ~12 moves
#                against a move cooldown.  Sides with 1-2 tangential hops brick
#                7.5 ring tiles and win 79%; sides with none brick 3 and win
#                47%.
#
# FINISHER GUARD, both of Jython's observed loss shapes, pre-registered:
#   (i)  if their Core has not been driven under CAGE_FINISH_HP by
#        CAGE_SEQ_TIMEOUT + CAGE_FINISH_GRACE, the whole plank turns itself OFF
#        for the rest of THIS game (a store bit, so every unit sees it) and the
#        tree reverts to loki_leap7's standard raid.  A cage that is not
#        killing is a titanium tiebreak we lose.
#   (ii) CAGE_RING8_FLOOR above -- spawn-sealing without heal-sealing loses.
#
# THE STORE -- ONE BIT, AND THE FIRST BUILD OF THIS PLANK GOT IT WRONG.
#
# The obvious home was slot 13 bits 28-30 (ARMED / OPEN / DISARM), above the
# HP band's 26-27, on the reasoning that slot 13's two existing writers already
# preserve that field: `_arch_note` masks with ARCH_KEEP_HI (0xFC000000) and
# `_sge_core_band` rewrites only 26-27.  MEASURED, first smoke game, nordkap
# seed 2: the OPEN latch was set at r25 and re-set on 58 consecutive rounds
# afterwards, i.e. it never once survived.  `_arch_note` preserves the high
# bits it READ, and it reads the snapshot from the start of the round -- so a
# raider that sets bit 29 and any builder that reports detector evidence later
# in the same round produce a last-write-wins race the latch always loses.
# This is FIX B's defect exactly, in a fresh field, and it is the third time
# this tree has walked into it.
#
# So the published state is ONE BIT in slot 15 (SLOT_RAID_LIVE) bit 31 --
# `_raid_beat` is the sole writer of that word in the entire tree and
# republishes it whole every round, which is the only property that makes a
# shared field safe here.  Bit 31 was reserved "for sign safety" and never
# tested; `bots/probe_store31` tested it for this plank: 0x80000000,
# 0x800003FF and 0xFFFFFFFF all survive a write/read cycle byte-identical, so
# the store is a genuine u32 and the reservation was superstition.
#
#   slot 15 bit 31  HOLD   the cage is not finished; nothing may shoot the Core
#
# The bit is RE-DERIVED every round by any raider that can SEE a footprint tile
# and merely REPUBLISHED by one that cannot -- the same discipline FIX B gave
# the HP band, and for the same reason.  OPEN and DISARM are then per-unit
# LATCHES rather than shared fields, which they can be because each is a
# function of something already visible to every body: OPEN latches on this
# body's own ring census or on a teammate having cleared the bit, and DISARM
# latches on the enemy-Core HP band, which slot 15 bits 28-29 already publish
# team-wide.
#
# MARKERS (CAGE_LOG, local replays only -- the platform strips stdout):
#   CG lift (x,y) n=K         a rider built ferry launcher number K
#   CG ferry (x,y)->(x,y)     our launcher threw our own rider forward
#   CG relay (x,y)            a ferry launcher KEPT (more riders in pickup range)
#   CG sd (x,y)               a ferry launcher self-destructed after its throw
#   CG seal n=K/12 r8=J/8     the seal census, on every change
#   CG hold r=N               a shot at their Core was withheld
#   CG open r=N               the gate opened
#   CG off r=N                finisher guard (i) tripped
#   CG evict (x,y)->(x,y)     one of THEIRS thrown off their own ring
#   CG hop (x,y)->(x,y)       one of OURS thrown between ring stations
# ============================================================================

CAGE_ON = True               # master; False == loki_leap7 + SOCKET-GUARD exactly

# --- the store ------------------------------------------------------------
CAGE_BEAT_SLOT = SLOT_RAID_LIVE   # 15, whose ONLY writer is `_raid_beat`
CAGE_BEAT_SHIFT = 31              # one bit above TW_BEAT_GUN_SHIFT
CAGE_HOLD_BIT = 1 << CAGE_BEAT_SHIFT

# --- arm 1: the launcher ferry --------------------------------------------
CAGE_FERRY = True
CAGE_FERRY_DISPOSABLE = True  # self-destruct after the throw (scale refund)
CAGE_FERRY_SEATS = 1         # raid slots allowed to ride.  ONE chain, which is
                             # both what Jython runs and what keeps SLOT_FERRY_ID
                             # (last-write-wins) uncontended.
CAGE_FERRY_CAP = 3           # ferry launchers ONE rider may build, per game
CAGE_FERRY_MIN_RND = 2       # the Core's first raider is out by r2-3
CAGE_FERRY_MAX_RND = 80      # the corpus says a fresh long throw is dead late
CAGE_FERRY_STOP_DSQ = 40     # == LOKI_ESTABLISH_DSQ: at the ring, stop ferrying
                             # /!\ THE OPENING BANK IS THE TRUNK CHAIN'S, NOT
                             # THE RAID'S, and the first build of this arm did
                             # not believe it.  MEASURED, glacierkeep side B
                             # seed 2: three hops at r2/r4/r6 took the bank
                             # 470 -> 105 by t7 against leap6's 294, the
                             # 9-conveyor trunk never connected, and the game
                             # ran to the r1000 cap with titanium_collected
                             # sitting at ZERO -- a loss on the tiebreak with a
                             # 11/12 seal held for 949 turns.  The same map is
                             # SOCKET-GUARD defect 16.3 #2 for the same reason.
                             # So the floor is a real one, and it is bigger
                             # where the trunk is longer: leap6 holds ~284 Ti
                             # through t5-t15 on that map and spends the lot in
                             # one burst at t20-t25.
CAGE_FERRY_TI_FLOOR = 220    # bank kept after paying for a hop, long trunk
CAGE_FERRY_TI_FLOOR_NEAR = 120   # ...and where the ore is on our doorstep
CAGE_FERRY_ORE_NEAR = 16     # d^2 from OUR Core to the nearest ore below which
                             # the trunk is 2-3 links and needs no war chest.
                             # antler 4, midgard 9, nordkap 9 are NEAR;
                             # auroraveil 29, drakkarfjord 58, glacierkeep 65
                             # are not.  In practice: three hops on a short
                             # chain, two on a long one
CAGE_FERRY_WAIT = 3          # rounds the rider will stand beside its launcher
CAGE_FERRY_STALE = 4         # rounds a rider's claim on SLOT_FERRY_ID is honoured
CAGE_FERRY_TAG = 1 << 20     # SLOT_FERRY_RND bit 20: "this claim is a CAGE
                             # claim, and the launcher beside the rider is
                             # DISPOSABLE".  Without it a SOCKET-GUARD corner
                             # launcher standing at OUR Core would read an
                             # ordinary LOKI ferry ping (which any raider near
                             # any launcher writes) and self-destruct our home
                             # defence.  The round stamp is <= 1000, so bit 20
                             # cannot collide with it, and the legacy reader in
                             # `_launcher_turn` step 2 is unaffected: this
                             # branch clears both fields after its own throw.
CAGE_FERRY_STAMP_MASK = 0xFFFFF   # the round half of that word
CAGE_FERRY_MIN_GAIN = 9      # a hop must close at least this much d^2 to be
                             # worth 20 Ti and two rounds of standing still
# WAVE 11, FIX 3(a).  THE LAST RELAY IN THE CHAIN IS ALREADY AN EVICTOR.
# The wave-10 verdict named LAUNCHER CAPACITY as the binding constraint on the
# ratchet (results/wave10/leap8_vs_leap6.md; DOCTRINE 19.5: "the observed rate
# is 0.25 seats closed per game ... the binding constraint on the heal wall is
# launcher COUNT and launcher SITING, not the eviction logic", and the A/B
# measured 0.107 ratchets/game).  The ferry chain ALREADY builds launchers
# marching towards their Core and then SELF-DESTRUCTS the last one for a 10%
# scale refund -- and that last one is frequently standing within its own d^2
# <= 2 pickup disc of their ring.  A launcher there is a free eviction every
# round for the rest of the game; the refund is ~2 Ti.  So: if the throw is
# made from inside pickup range of a ring tile, the relay CONVERTS instead of
# disposing.  Everything else self-destructs exactly as before.
CAGE_FERRY_CONVERT = True
CAGE_FERRY_CONVERT_DSQ = 2   # == RAT_STAGE_DSQ, the engine's pickup disc

# --- arm 2: the twelve-tile seal ------------------------------------------
CAGE_SEAL = True
CAGE_SEAL_TI_BUDGET = 45     # replaces COLLAR_TI_BUDGET (32) while the cage
                             # runs.  Twelve bricks is 36 Ti at base price plus
                             # the tending, and 41% of our bricks die.
CAGE_RING8_FLOOR = 6         # finisher guard (ii): seats held before ANY
                             # titanium is spent on a diagonal corner
CAGE_CORNER_KEEP = 1         # corners left open while we hold NO launcher at
                             # their ring -- a launcher is built ON a corner and
                             # bricking the last one kills arms 3 and 4
CAGE_OUTER_STATION = True    # once the ring is full, raiders station on the
                             # shell outside it so they can still tend and reseal

# WAVE 11, FIX 1.  THE STRICT CENSUS GATES EVERYTHING.
# DOCTRINE 19.2 (i): `_cg_seal`'s permissive count resolves a ring tile through
# `is_tile_passable`, which engine_mechanics N.6 measures as False under a
# builder bot OF EITHER TEAM -- so one of THEIR healers sitting on one of THEIR
# heal seats reads to us as a SEALED tile.  Measured on the wave-10 probe: own
# census 10 of 12 while the board said 4-8, their seat occupancy 6.45 of 8,
# enemy heal ratio 1.000.  leap8 fixed this for PLANK FIN only and left the
# defect standing in the CAGE hold-fire gate and the corner-spend gate (19.7
# risk 5).  A ring full of their healers is the OPPOSITE of a cage, and every
# GATE now reads `_fin_seal`'s strict count: terrain, a building of either
# team, or one of OUR bodies.  The permissive count survives in exactly one
# role -- SCOUTING "which tiles need an eviction before anything can be built
# on them", which is what `_cg_corner_ok`'s free-corner arithmetic asks and the
# only question `is_tile_passable` actually answers correctly.
# EXPECTED, and pre-registered: `CG open` and the corner spend both move LATER.
# That is the truthful reading of the same board, not a regression -- but the
# hold-fire stretch is the wave-8 failure mode, so `CAGE_SEQ_TIMEOUT` (150) is
# now the thing carrying the risk and the A/B must watch kill round.
CAGE_STRICT_SEAL = True      # False == leap8's split (loose gates, strict FIN)

# --- arm 3: sequencing ----------------------------------------------------
CAGE_BEFORE_SIEGE = True
CAGE_SEAL_GATE = 6
CAGE_SEQ_TIMEOUT = 150
CAGE_HOLD_LOG_GAP = 40       # rounds between `CG hold` markers, per unit

# --- arm 4: the ring launcher ---------------------------------------------
CAGE_EVICT = True
CAGE_LAUNCH_MIN_RND = 20     # the CAGE gate replaces TW_MIN_RND (60) for the
                             # launcher only -- never for the gunner
# WAVE 11, FIX 3(b).  TWO STANDING EVICTORS, ON OPPOSITE CORNERS.
# The four ring corners partition the eight heal seats into four disjoint pairs
# (corner (-1,-1) covers seats (0,-1) and (-1,0) at d^2 <= 2, and so on round),
# so ONE launcher can never reach more than two of the eight seats the ratchet
# exists to close -- DOCTRINE 19.5's ceiling, and the fixture built one
# launcher per game.  Two launchers on DIAGONALLY OPPOSITE corners cover four
# seats spread around the ring instead of four bunched on one face.
# TW_LAUNCH_CAP is already 2, so this changes nothing about the CAP -- what it
# changes is the two gates that made #2 unreachable in practice: TW_LAUNCH_AGE
# (20 rounds of survivorship, written for a DEFENSIVE plucker bought late) and
# the nearest-corner walk, which sends the second builder to whichever corner
# is closest and therefore often back to the one already covered.
CAGE_EVICT_CAP = 2           # standing evictors allowed AT THEIR RING while the
                             # cage's launcher gate is open.  REPLACES
                             # TW_LAUNCH_CAP there and is read off the same live
                             # census (`_tw_census`, launchers within
                             # TW_CENSUS_DSQ of THEIR Core), so a converted
                             # ferry relay counts against it like any other.
                             # Equal to TW_LAUNCH_CAP today on purpose: this
                             # batch changes WHEN and WHERE #2 is sited, not
                             # how many are allowed.  Raising it is a separate
                             # arm and a separate measurement.
CAGE_EVICT_AGE = 0           # survivorship rounds required of evictor #1 before
                             # #2 may be sited (TW_LAUNCH_AGE = 20 otherwise).
                             # The cage's launcher is not a defensive purchase
                             # waiting to see whether it gets answered -- it is
                             # the delivery half of the mechanism and the raid
                             # is only established for a window.
CAGE_EVICT_SPREAD = True     # site #2 on the corner FARTHEST from the evictors
                             # we already hold == the diagonal opposite
CAGE_HOP = True
CAGE_HOP_MAX_DSQ = 8         # a hop must LAND inside ~2.8 tiles of their
                             # footprint, or it is a taxi and not a hop
CAGE_HOP_GAP = 6             # rounds between hops by the same launcher
CAGE_HOP_RETRY = 3           # ...and between DECLINED hop scans, which are the
                             # expensive ones (a 12-tile census plus an 88-tile
                             # site walk) and the common ones

# --- the finisher guard ---------------------------------------------------
CAGE_FINISH_HP = SIEGE_MASS3_HP   # 400 -- the band already published in slot 15
CAGE_FINISH_GRACE = 60       # rounds after CAGE_SEQ_TIMEOUT before reverting

CAGE_LOG = True              # the markers above; local instrument only
CAGE_LOG_WHY = False         # probe grade: why the FERRY declined this round
                             # (`CG why r=N w=... ti=K`).  Off by default and
                             # stamped on with tools/leap7_variant.py -- the
                             # ferry window is 80 rounds and an unthrottled
                             # refusal marker is a real CPU line item there.
CAGE_WHY_GAP = 15            # rounds between repeats of the same reason


# ============================================================================
# PLANK PAIRS (PR) -- FORWARD SENTINELS DEPLOY IN TWOS, NEVER IN ONES.
# ============================================================================
# EVIDENCE.  analysis/meta_pipeline_diff.md gap 2, and it is the single largest
# generic lever the whole 505-game corpus produced:
#
#   peak Sentinels ALIVE within 6 tiles of the enemy Core at the same moment
#     >= 2  ->  we win 82.3 %      (top-5: 87.1 %)
#      = 1  ->  we win 33.3 %      (top-5: 35.2 %)
#   split lift +48.9 pp for us, +51.9 pp for them -- the ONE metric whose
#   MEDIAN sits on the wrong side of the split for us (our median peak is 1).
#
# And the shape of the failure is not "we cannot afford two".  Conditional on
# WINNING we already reach 2 on 62.2 % of sides, ahead of the top-5's 56.4 %.
# It is the LOSING half that never gets a second tube up: 40.0 % of all our
# sides reach >= 2, 3.2 % reach >= 3 (Jython 18.4 %).  A lone tube absorbs the
# whole response and dies at a median 6 core shots against a pair's 14 each --
# and 14 + 14 = 28 is exactly the ceil(500/18) a solo kill needs.  Our
# core-hitting Sentinels die 68 % of the time (top-5 27 %, Jython 22 %).
#
# So the tube that stands alone is not half a kill.  It is a donation.
#
# THE PLANK, in one sentence: tube 1 is BUILT on the parent's schedule but does
# not open on their Core until tube 2 is funded and sited within 6 tiles of the
# same Core; and every lever that decides whether tube 2 arrives is re-aimed at
# making that happen inside the 30 rounds tube 1 can survive alone.
#
# FOUR ARMS, and three of them are rewires of machinery that already exists.
#
#   1. THE DISCOUNT, IMMEDIATE (`PAIR_MASS2_AGE`).  SIEGE_MASS_ON already drops
#      the bank floor for tube 2 from LOKI_FWD_TI_FLOOR (40) to
#      SIEGE_MASS_TI_FLOOR (6) -- but only after tube 1 has STOOD for
#      SIEGE_MASS2_AGE (20) rounds.  That gate was written as a SURVIVORSHIP
#      test ("if the first is being answered on arrival a second dies with
#      it"), and the fresh corpus says it is backwards: the reason the first is
#      answered on arrival is that it is ALONE.  Waiting 20 rounds to find out
#      whether a solo tube survives is how the solo tube stops surviving.  With
#      PAIR_ON the age becomes 0 -- the discount arms the round tube 1 is
#      sited.  This is a strictly LOOSER gate on a DISCOUNT that can only ever
#      move a bank floor DOWN, so it cannot refuse a tube the parent bought.
#
#   2. THE HOLD (`_pr_hold`).  Tube 1 does not fire at their CORE while it is
#      alone.  Every other target stays legal exactly as under CAGE_BEFORE_SIEGE
#      -- their belts, their turrets, their bodies on seats -- so a held tube is
#      not an idle tube, it is a tube that has not yet announced itself to the
#      thing that heals 4 HP per titanium.  The corpus prices the announcement:
#      our losing sides put the first shot on their Core at r23 against r51.5 in
#      our wins, and "first core-shot round, later is better" carries +22.7 /
#      +25.7 on its own split.
#
#   3. THE RESERVE (`PAIR_JIT_RESERVE`).  The hold only pays if the titanium it
#      saves buys tube 2.  While a tube is HELD the Core stops draining the bank
#      into ammunition it cannot fire: `_sge_jit`'s conversion floor rises to
#      cover a Sentinel plus PAIR_JIT_MARGIN, so the pipe trickles instead of
#      pumping and the bank climbs to the ~36 Ti arm 1 now asks for.  The
#      MAGAZINE TARGET is untouched (SIEGE_JIT_MIN, 16, still clears one shot
#      plus change for the legal targets above) -- this is a floor on what may
#      be SPENT, not a cap on what may be held.  Suspended whenever `under`:
#      home defence outranks the second tube, always.
#
#   4. THE RELEASE (`PAIR_RELEASE_RNDS`).  A hold with no exit is the
#      `73867571_g4` failure with different furniture -- a full seal held for
#      855 rounds into a titanium tiebreak.  If tube 2 has not arrived within 30
#      rounds of tube 1 becoming able to shoot, tube 1 opens anyway and latches
#      open for the rest of the game.  Solo is worth 33.3 %; silent is worth
#      less.  30 rounds is the window the corpus gives a solo tube: our
#      core-hitting Sentinels land a median 6 shots at a 2-round reload before
#      they die, which is ~12-15 rounds of firing, and the losing half's first
#      tube goes up at r21 against a first core shot at r23.
#
# THE OPEN-FIRE MOMENT IS SHARED WITH PLANK CAGE.  Both gates answer the same
# question -- "may this body damage their Core yet?" -- and they are OR'd, so
# fire opens only when BOTH are satisfied.  They are deliberately NOT merged
# into one bit: CAGE's hold is a TEAM fact (the ring census, published in slot
# 15 bit 31) and PR's is a PER-BODY fact (this tube's own clock against a team
# census of tubes), and folding a per-body latch into a shared word is the
# race FIX B and the CAGE store note already cost this tree two rebuilds.
#
# THE STORE: NOTHING NEW, AND THAT IS THE DESIGN.  Slot 15 is full (bits 0-9
# heartbeat, 10-27 collar lanes, 28-29 HP band, 30 gun ammo, 31 cage hold) and
# slot 13's high bits are the field `_arch_note` loses races in.  PR needs no
# field: the pair census is ALREADY published as SLOT_FWD_GUN (slot 8), whose
# only writer is `_t5_note_fwd_build` and which under LOKI2B_LIVE_CAP_ON
# carries the LIVE count of forward tubes -- so it falls back to 1 when a tube
# dies, which is exactly the re-hold a body that has not yet opened should see.
# Everything else PR needs (the clock, the open latch) is per-unit.
#
#   /!\ THE LATCH IS ONE-WAY ON PURPOSE.  Once a body has opened -- by pair or
#   by release -- it never re-holds.  The measured quantity is PEAK sentinels
#   within 6, not concurrent ones, and a tube that re-mutes itself because its
#   partner died is a tube that stops being the 14-shot half of 28.
#
# THE 6-TILE PREDICATE.  `PAIR_CENTRE_Q4` is quarter-scale distance-squared to
# the 2x2 CENTRE -- the same `sge_centre_q4` the SIEGE band already uses, and
# the same metric analysis/meta_pipeline_diff.md measures "within 6 tiles" in.
# (6 * 2)^2 = 144.  It is used for the raider-side census that names the pair in
# the marker; the TURRET-side gate reads SLOT_FWD_GUN instead, because a tube
# cannot be made to depend on seeing its partner through fog.
#
# MARKERS (PAIR_LOG, local replays only -- the platform strips stdout):
#   PR pair (x,y)+(x,y)     tube 2 sited; the two tubes that now stand
#   PR release-solo r=N     a held tube gave up waiting and opened
#   PR hold r=N             a shot at their Core was withheld (throttled)
# ============================================================================

PAIR_ON = True               # master; False == loki_leap7 + SOCKET-GUARD + CAGE

PAIR_MIN = 2                 # forward tubes that constitute a pair
PAIR_MASS2_AGE = 0           # arm 1: replaces SIEGE_MASS2_AGE (20) for tube 2
PAIR_RELEASE_RNDS = 30       # arm 4: rounds a tube waits before firing solo
PAIR_CENTRE_Q4 = 144         # (6 tiles)^2 in quarter-scale centre distance
PAIR_JIT_RESERVE = True      # arm 3: hold titanium back from the ammo pipe
PAIR_JIT_MARGIN = SIEGE_MASS_TI_FLOOR   # 6 -- arm 1's own bank floor
PAIR_HOLD_LOG_GAP = 40       # rounds between `PR hold` markers, per unit
PAIR_LOG = True              # the markers above; local instrument only


# ============================================================================
# PLANK FIN (wave 10, bots/loki_leap8) -- THE SEAL-WINDOW FINISHER.
#
# WAVE 9 NAMED THE HOLE.  results/wave9/*.md: the cage machinery now WORKS --
# seal >= 10 in 45-49% of games against leap6's 20-26%, held >= 10 turns in
# 42-45% -- and the 12/12 window (15-22% of games) CONVERTS ALMOST NOTHING.
# We reach the position Jython wins from and then do not finish: the tubes fire
# at whatever cadence the ammunition pipe happens to be running, the escorts
# standing on their heal seats do nothing at all, and the third tube waits on
# an HP band that only turns LOW after the grind we are trying to shorten.
#
# THE WINDOW IS THE WHOLE POINT.  While the ring is sealed their Core's heal is
# ~0 (measured, juusto 0.05-0.17 at seal 10-12), so every point of damage is
# PERMANENT.  Outside the window damage is a loan at 4 HP per titanium.  Three
# taps, all of which only open inside the window and all of which close again
# with it:
#
#   (a) AMMO SURGE.  The Core drops its bank floor to FIN_TI_FLOAT and raises
#       the magazine target to FIN_AMMO_TARGET, so a forward Sentinel is never
#       the thing waiting on 10 ammunition while the seal is up.  PLANK PAIRS'
#       arm-3 reserve (which holds titanium back to buy tube 2) is suspended:
#       inside the window the tube that already stands is worth more than the
#       tube that might.
#   (b) ESCORT PECKS.  A builder orthogonally adjacent to a Core tile does 2
#       damage for 2 Ti at ZERO cost scale (engine_mechanics C), and our own
#       squatters are already standing on their heal seats doing nothing else.
#       Two or three spare escorts is +4-6 HP a round on top of tube fire while
#       their heal is sealed off.  LOKI_QUIET_ON silences builder melee for the
#       measured reason that a peck costs the STEP that arrival is made of --
#       this carve-out is narrow in exactly that dimension: the body has already
#       ARRIVED, it is standing on its station, and the window is the one state
#       in which 2 damage a round is not a loan.
#   (c) TUBE PRIORITY.  Tube 3's discount normally waits for the enemy Core to
#       fall below SIEGE_MASS3_HP.  Inside the window it arms immediately -- the
#       window IS the assault clock, and a sited post that goes unbought while
#       the ring is sealed is the exact trade wave 9 lost.
#
# SEAL INTEGRITY IS STRICTLY FIRST.  The peck sits BELOW the collar (reseal /
# tend / brick), below the parent's own free-seat seal, and below every
# purchase in `_raid_act`; and it additionally refuses on its own account if a
# ring tile beside this body is either brickable or holding one of our damaged
# bricks (`_fin_seal_pending`).  A lost brick is re-laid before anyone pecks,
# because one re-opened seat is +4 HP per titanium and out-earns three pecks.
#
# THE PUBLISHED BIT.  The Core cannot see the ring, so the window has to be
# published.  Slot 15 is FULL (heartbeat 0-9, collar lanes 10-27, HP band
# 28-29, TW gun bit 30, CAGE hold 31).  The only free capacity in the lineage
# is slot 13 bits 28-31 -- the merge budget reserved for bots/loki_macro, which
# is not in this tree -- and slot 13's two live writers (`_arch_note`, via
# ARCH_KEEP_HI, and the legacy band write) both carry bits 26-31 through
# untouched.  TWO bits are taken, 28-29, and bit 31 is deliberately left clear
# so no store word in this tree ever goes negative.
#
#   0 UNKNOWN   nobody with eyes has published yet
#   1 OPEN      an eyed raider's ring census is at or above the gate
#   2 SHUT      an eyed raider looked and it is not
#
# The field is RE-DERIVED every round by every eyed raider, which is the one
# class of field slot 13 can host (doctrine section 2b): a write lost to
# `_arch_note`'s stale read-modify-write costs one round of latency and the
# next round repairs it.  Readers additionally require a live raid heartbeat
# (slot 15 bits 0-9, FIN_STALE) -- a raid that has been wiped out must not
# leave the Core surging into an empty battlefield.
#
# HYSTERESIS lives in the PUBLISHER so every reader agrees: the window opens at
# FIN_GATE and does not close until FIN_DROP, so one brick shot out does not
# flicker the Core's whole ammunition policy.
#
# MARKERS (FIN_LOG, local replays only -- the platform strips stdout):
#   FIN open r=N seal=K     the window opened on this body's own census
#   FIN close r=N           ...and lost it
#   FIN peck (x,y)          an escort spent its action on their Core
#   FIN surge r=N           the Core's ammunition pipe entered the window
#
# HOW THIS LOSES, pre-registered.  (1) The peck is a step not taken: if median
# kill round RISES the carve-out re-opened the leak LOKI-QUIET closed, and the
# first thing to try is FIN_PECK_ON = False alone.  (2) The surge is titanium
# not banked, and stored titanium is tiebreak #3 -- a cage with no finisher
# that now also empties the bank loses tiebreaks it used to win, which is
# FINISHER GUARD (i)'s failure mode with a bigger price tag.  (3) Tube 3 inside
# the window is a scaled purchase made at the moment the raid is most exposed.
# ============================================================================

FIN_ON = True                # master; False == leap7_soft exactly
FIN_GATE = 10                # ring12 tiles held before the window OPENS
FIN_DROP = 8                 # ...and it stays open until the census falls below
# THE SEAT TERM, and it is the correction the wave-10 smoke forced.  A ring12
# census of 10 can be four corners and six seats -- and the two seats still open
# are worth +4 HP per titanium EACH to their Core, which beats everything the
# window buys.  MEASURED, loki_leap8 vs mimic_istones on sab_05 seed 2: strict
# seal >= 10 all game, 100% of our damage landed inside the window, 833 escort
# pecks = 1,666 Ti spent -- and the enemy heal ratio was 1.000.  Every point was
# healed back through two open seats.  ring12 is the SPAWN seal; ring8 is the
# HEAL seal, and this plank's whole premise ('their heal is ~0') is a statement
# about ring8 only.  Both terms must hold.  (analysis/meta_2000.md flagged
# exactly this as failure mode 'spawn-seal != heal-seal'; FIN is where it bites.)
FIN_SEAT_GATE = 7            # ring8 heal seats held before the window OPENS
FIN_SEAT_DROP = 6            # ...and the seat half of the hysteresis
FIN_PUB_SLOT = SLOT_ARCH_SEEN     # 13 -- see "THE PUBLISHED BIT" above
FIN_PUB_SHIFT = 28           # bits 28-29; 30-31 stay clear (sign safety)
FIN_PUB_MASK = 0x3
FIN_PUB_KEEP = 0x0FFFFFFF    # everything BELOW the field, preserved on write
FIN_PUB_UNKNOWN = 0
FIN_PUB_OPEN = 1
FIN_PUB_SHUT = 2
FIN_STALE = LOKI_FOOTHOLD_STALE   # 15 -- raid heartbeat age a reader will trust

FIN_PECK_ON = True           # (b) escort pecks
FIN_PECK_TI_FLOOR = 8        # a peck is 2 Ti; never take the bank below this,
                             # which is a barrier (3) plus a peck plus change
# WAVE 11, FIX 2.  THE PECK IS A MACRO-ONLY WEAPON.
# The peck was the one FIN arm that was NOT archetype-gated, and the wave-10
# A/B priced that: vs mimic_juusto -- a PRESSURE/DEFAULT read, where the peck
# fired hardest -- loki_leap8 lost 8.1 pp per game (77.4% vs leap6's 85.6%,
# sign test p = 0.0013) and 13.3 pp of cells on the legs where the peck ran,
# at 116 Ti/game of pecks.  The peck's premise is "inside the window their heal
# is ~0, so 2 damage is PERMANENT".  That premise is a statement about an
# opponent AT THE UNIT CAP who cannot respawn what we evict -- the same
# population `RAT_CAP_ONLY` was already written for.  Against a pressure
# opponent the 2 Ti buys 2 damage that is healed back, and the ACTION it
# spends is a step not taken (`LOKI_QUIET_ON` is a measured win because acting
# and moving are mutually exclusive).  So the peck now takes the detector's
# verdict (slot 9, upper bits) and fires only on MACRO / MACRO_WEAK.  The
# surge and the seal arms are unchanged: they cost titanium, not actions.
FIN_PECK_MACRO_ONLY = True   # False == leap8 (peck vs anyone)
FIN_AMMO_ON = True           # (a) ammo surge
FIN_TI_FLOAT = 20            # bank the Core keeps while surging
FIN_AMMO_TARGET = 60         # magazine the surge aims at (6 Sentinel shots)
# WAVE 11, FIX 4.  THE SURGE STAYS, TUBE 3 ON THE WINDOW GOES.
# Named residual-drag suspect: tube 3 in-window is a SCALED purchase made at
# the moment the raid is most exposed (19.7 risk 2), and it is bought out of
# the same bank the surge has just dropped to FIN_TI_FLOAT (20) -- the two arms
# compound, and stored titanium is tiebreak #3.  Default OFF, flag KEPT so the
# arm can be measured on its own in a later ablation rather than deleted.
FIN_TUBE3_ON = False         # (c) tube 3 arms on the window, not on the band
FIN_LOG = True               # the markers above; local instrument only


# ============================================================================
# PLANK RATCHET (wave 10, bots/loki_leap8) -- EVICT, THEN BRICK.
#
# THE WAVE-9 FAILURE, exactly.  Against mimic_istones the enemy heal ratio did
# not move at all: 0.91, and ring8 (the eight HEAL seats, the half that decides
# whether their Core comes back) topped out at 6 of 8 against leap6's 5.  The
# cause is mechanical and it is not a tuning problem: THEIR HEALERS ARE ALREADY
# SITTING ON THE SEATS.  `can_build_barrier` is False on an occupied tile, so
# our collar can only ever claim seats they left free -- we were sealing the
# empty half of the ring and calling it a cage.
#
# THE EXPLOIT.  An opponent AT the 50-unit cap CANNOT RESPAWN (engine: the Core
# spawns one builder a round onto its ring12 only if under the cap AND a ring
# tile is free).  I Stone runs 36-49 builders; the same is true of anyone whose
# ring12 we have already sealed. So a body evicted off a seat can only WALK
# back -- and a walk is rounds, and rounds are all a 3-Ti barrier needs.
#
# THE MECHANISM, three parts, none of them new machinery:
#
#   (1) THE PLUCK IS AIMED.  CAGE arm 4 widened the launcher's victim
#       preference from their eight seats to all twelve ring tiles, which made
#       a corner-squatter and a seated HEALER worth the same throw.  Inside the
#       ratchet the ranking is restored and sharpened: a SEATED enemy builder
#       first, and among those the seat that ONE OF OUR BODIES IS ALREADY
#       STANDING BESIDE -- because that is the seat that can be bricked the
#       round it empties, and a seat we evict but cannot brick is a shove
#       rather than a ratchet.  "Highest-value seat" is operationalised as
#       "the seat where the eviction becomes permanent", which is the only
#       property that is worth titanium.
#
#   (2) THE BRICKER IS THERE FIRST.  A raid station orthogonally beside a
#       seated enemy builder that is inside a launcher's r^2 <= 2 pickup disc
#       is worth RAT_STAGE_BONUS in the station scoring -- so a body walks to
#       the seat BEFORE the pluck rather than after it.
#
#   (3) THE VACANCY IS TAKEN.  The collar's BRICK arm already polls
#       `can_build_barrier` on every adjacent ring tile every round, which is
#       exactly the retry loop this needs; what the ratchet adds is that a tile
#       we watched an enemy body sit on within RAT_WATCH_RNDS goes to the FRONT
#       of that arm's list, and that the collar's titanium budget cannot refuse
#       it (RAT_BRICK_WAIVE) -- 3 Ti to close a heal seat permanently is the
#       best price on the board and the budget was written for a different arm.
#
# THE ORDERING, which is why this is safe.  Units act in creation order. Our
# launcher was built late and therefore has a HIGH entity id, so it throws LATE
# in the round -- after their Core (id 1/2, acts first) has already taken its
# turn, and after most of their builders. So the tile is vacant from the throw
# to the end of the round and through their Core's next turn only if the Core
# is over the cap; if it is not, their Core can re-spawn onto it before our
# bricker acts. That is exactly what RAT_CAP_ONLY is for.
#
# THE GATE.  RAT_CAP_ONLY: run the ratchet only when the archetype detector
# says MACRO / MACRO_WEAK, or when our own census has seen RAT_CAP_N enemy
# builders at once near their Core (S5, slot 13 bits 21-25 -- already published
# by the detector, saturating at 31). Against a low-count opponent an evicted
# builder is simply respawned for free and the ratchet leaks: we pay 3 Ti and a
# launcher action per seat and they pay a spawn they were making anyway.
#
# MARKERS (RAT_LOG, local replays only):
#   RAT pluck (x,y)         a SEATED enemy builder thrown off (x,y)
#   RAT brick (x,y)         a tile we watched one of theirs sit on, now sealed
#   RAT ratchet n=K         K seats this BODY has closed that way (per unit;
#                           take the SUM over units when reading a replay)
#
# HOW THIS LOSES, pre-registered.  (1) The aimed pluck gives up the corner
# preference CAGE arm 4 measured at +22/+37, so if the ratchet fires and the
# seal still does not move, the widening was doing the work and RAT_SEAT_FIRST
# is the first flag off.  (2) The stage bonus pulls bodies off tend stations;
# a rising count of lost bricks is that trade.  (3) The budget waive is
# unbounded per round in principle -- it is bounded in practice by the collar
# only ever seeing four tiles and by `free` being empty once the ring is shut.
# ============================================================================
#
# WAVE 12: REFUTED.  THE FLAG IS OFF AND IT STAYS OFF.
# The ratchet's premise is a HANDOFF -- the ferry/launcher chain puts an
# evictor beside a seat, the evictor plucks the body off it, a bricker
# stationed there seals the seat before the body walks back.  Wave 11 measured
# the handoff end to end (results/wave11/leap9_vs_leap6.md): the
# launcher-to-bricker conversion is 2.9%.  Ninety-seven evictions in a hundred
# buy nothing, and the three arms that spend for them are not free -- the
# aimed pluck gives up the corner preference the CAGE measured at +22/+37
# (failure mode (1) below, pre-registered in wave 10 and now observed), the
# stage bonus pulls bricklayers off tend stations, and the brick waive spends
# the collar budget outside it.  This is the pre-registered kill: the arm was
# given two waves and a capacity fix (wave 11 FIX 3) and the conversion did not
# move.  The CODE stays -- every branch below is one `RAT_ON` test away from
# live and the wave-11 replays are still readable against it -- but nothing in
# this tree may turn it back on without a NEW measurement of the handoff, not
# of the eviction count.  What survived the same measurement is the EVICTOR
# ITSELF (evictor-standing cells +4.4 pp at heal 0.562; no-evictor cells
# -9.0 pp, p = .081), and wave 12's whole design is to stop paying for the
# cage on the cells where no evictor stands -- see the CAGE EVICTOR GATE block.
# ============================================================================

RAT_ON = False               # WAVE 12: REFUTED, 2.9% handoff conversion.
                             # `True` == loki_leap9 exactly; do not.
RAT_CAP_ONLY = True          # the gate above.  False = run it against anyone
RAT_CAP_N = 8                # S5 enemy-builder census that proxies "at the cap".
                             # RETUNED FROM 20 ON EVIDENCE (wave-10 smoke, seed 2):
                             # S5 is what our own bodies SAW at once near their Core,
                             # not their army size, and 20 is unreachable on most
                             # boards.  Max enemy builders within r^2 <= 20 of their
                             # Core, measured off the replays: mimic_istones 10 / 11 /
                             # 39, mimic_0033 5 / 5, mimic_juusto 4 / 4.  8 is the
                             # detector's OWN threshold for "many builders near their
                             # Core" (ARCH_S5_MANY, which the corpus set), and it
                             # separates the fixtures cleanly with room on both sides.
RAT_SEAT_FIRST = True        # (1) aim the pluck at seated healers
RAT_STAGE_ON = True          # (2) station a bricker beside the target seat
# WAVE 11, FIX 3(c).  THE STATIONING BONUS FOLLOWS THE EVICTOR, NOT THE GATE.
# Wave 10 measured 0.107 ratchets/game and named the cause: "no launcher stood
# when needed".  The stationing bonus is the arm that puts a bricker beside the
# seat BEFORE the throw, and it was gated on `_rat_live` -- the archetype/S5
# cap read -- on top of already requiring one of OUR launchers to be in reach
# of the seat.  That second requirement is the real precondition and it is
# strictly stronger evidence: a launcher standing within d^2 <= 2 of a seat
# their body is sitting on is the eviction, observed, not predicted.  The
# PLUCK (arm 1) and the BRICK-WAIVE (arm 3) keep the cap gate -- those are the
# arms that spend the eviction and the budget.  This one only changes where a
# body that was walking anyway chooses to stand.
RAT_STAGE_ANY_EVICTOR = True # False == leap8 (stage only inside RAT_CAP_ONLY)
RAT_STAGE_BONUS = 14         # ...worth more than COLLAR_TEND_BONUS (10)
RAT_STAGE_DSQ = 2            # launcher pickup disc, engine constant
RAT_WATCH_RNDS = 6           # rounds a seat stays "recently theirs" after we
                             # last saw one of their bodies on it
RAT_BRICK_WAIVE = True       # (3) the collar budget cannot refuse a ratchet brick
RAT_LOG = True               # the markers above; local instrument only


# ============================================================================
# CAGE EVICTOR GATE (EVGATE) -- WAVE 12.  THE CAGE'S EXPENSIVE ARMS RUN ONLY
# WHILE AN EVICTOR IS ESTABLISHED.
# ============================================================================
# THE MEASUREMENT THAT FORCED THIS.  results/wave11/leap9_vs_leap6.md split the
# paired A/B by whether one of OUR launchers ever stood inside its own pickup
# disc of one of THEIR ring tiles -- an EVICTOR, standing:
#
#   evictor-standing cells   +4.4 pp over loki_leap6, enemy heal ratio 0.562
#   no-evictor cells         -9.0 pp over loki_leap6, p = .081
#
# Both halves are the SAME package.  Where the evictor stands, the cage does
# exactly what it was designed to do: the seat cannot be re-manned, the heal
# ratio falls by nearly half, and the hold-fire that bought the seal is repaid.
# Where no evictor stands, every expensive arm is a pure cost -- we hold our
# guns off their Core waiting for a seal that will never be finished, we surge
# the bank into a window opened on a ring their healers walk back onto, and we
# spend scaled titanium on diagonal corners that deny a spawn tile next to a
# Core healing faster than we shoot it.  A cage with no evictor is a bot that
# pays the full price of a siege and then declines to take it.
#
# THE PLANK, in one sentence: ESTABLISHMENT IS THE PRECONDITION, not a hope --
# the three arms that cost titanium or forgone damage (hold-fire, the FIN
# window, the corner spend) are switched OFF until a live launcher of ours
# stands within the engine's d^2 <= 2 pickup disc of a ring tile, and switched
# off again if that launcher dies and is not replaced.
#
# WHAT IS **NOT** GATED, and this is deliberate:
#   * the FERRY and the LAUNCHER themselves -- they are how establishment
#     HAPPENS; gating them on establishment is a deadlock.
#   * a barrier laid on a ring tile by an escort ALREADY STANDING BESIDE IT.
#     3 Ti, no walk, no scaled purchase, and it is the cheapest denial on the
#     board.  Only the DIAGONAL CORNER spend (`_cg_corner_ok`, the scaled arm
#     that finisher guard (ii) already rations) takes the gate.
#   * the seal CENSUS and its markers.  The instrument keeps running with the
#     gate shut, because the gate's own decisions are read off it.
#
# WHERE IT IS WIRED, and why there and nowhere else.  Two of the three arms are
# already TEAM-WIDE PUBLISHED FACTS with exactly one publisher each, and that
# publisher is a raider standing at their ring -- the one body that can see
# whether a launcher of ours is on it:
#
#   hold-fire   `_cg_beat_bit`  (slot 15 bit 31, sole writer `_raid_beat`)
#   FIN window  `_fin_publish`  (slot 13 bits 28-29, eyed raiders only)
#
# So the gate is applied at the PUBLISH, and every blind consumer -- the Core's
# ammunition JIT, a turret across the map, a tube-siting raider -- inherits it
# for free with no new store field and no second source of truth.  The two
# first-hand readers that bypass the store (`_fin_live`'s own-eyes branch and
# `_cg_corner_ok`) take the gate directly, and both of them are, by
# construction, bodies with eyes on the ring.
#
# HYSTERESIS, and why it is 15 rounds.  An evictor that is shot and rebuilt is
# the NORMAL case, not the failure case -- CAGE_EVICT_CAP allows two and the
# ferry chain replaces them.  Flapping the hold bit would be worse than either
# state: the team would open fire, re-hold and re-open, and `cg_saw`/`cg_open`
# are ONE-WAY latches, so a single spurious open is permanent for that body.
# The gate therefore closes only after CAGE_EVGATE_HYST rounds with no evictor
# seen, which is long enough to cover a rebuild (a raider at the ring with the
# bank builds inside ~3) and short enough that a dead raid stops paying.
#
# THE DEADLINE is a one-way kill, not a window.  If no evictor has EVER been
# seen by CAGE_EVGATE_DEADLINE the cage is abandoned for the rest of the game
# and this body plays the ordinary leap6-style attack: r80 is where the ferry's
# own clock (CAGE_FERRY_MAX_RND) stops, so past it the transport that would
# have delivered one is over.  Without the latch a stray launcher built at r200
# for a defensive reason would re-arm hold-fire on a game that has been a
# straight siege for a hundred rounds.
#
# HOW THIS LOSES, pre-registered.  (1) The gate is read from ONE body's eyes;
# a raider whose vision of the ring is blocked reads "no evictor" and publishes
# SHUT while an evictor stands.  That is a FALSE NEGATIVE and it degrades to
# leap6, which is the fallback by design -- but if `CG evgate` markers flicker
# on cells where `CG convert` fired, the census is the suspect, not the plank.
# (2) The gate can only make the cage RARER.  If wave 11's evictor split was
# selection (good games grow evictors) rather than causation, this batch buys
# nothing and costs the cells where the cage was winning without one.
# (3) `CAGE_SEQ_TIMEOUT` no longer carries the hold-fire risk alone: a late
# establishment (r70) now opens a hold-fire window at r70 that leap9 would have
# opened at r20 and released at r150.  Median kill round is the watch.
#
# MARKERS (CAGE_LOG, local replays only):
#   CG evictor r=N (x,y)    an evictor of ours was SEEN sited on their ring
#   CG evgate r=N off       ...and the gate closed again after the hysteresis
#   CG evgate r=N dead      the deadline passed with no evictor ever seen
#   CG post (x,y)           leap10_est: an arrived rider bought the post
#   CG chaincut r=N w=lift  wave 13 arm D refused a chain rebuild the ferry's
#   CG chaincut r=N w=ferry own clock would have ALLOWED.  Zero == inert.
# ============================================================================

CAGE_EVGATE_ON = True        # master; False == loki_leap9's cage exactly
CAGE_EVGATE_DSQ = CAGE_FERRY_CONVERT_DSQ   # 2 -- the engine's pickup disc, the
                             # same geometry `_cg_evict_sited` already tests
CAGE_EVGATE_DEADLINE = 80    # == CAGE_FERRY_MAX_RND.  No evictor ever seen by
                             # this round and the cage is dead for the game
CAGE_EVGATE_HYST = 15        # rounds an established gate survives with no
                             # evictor in sight before it closes again
CAGE_EVGATE_HOLD = True      # arm A: hold-fire follows the gate
CAGE_EVGATE_FIN = True       # arm B: the FIN window follows the gate
CAGE_EVGATE_CORNER = True    # arm C: the diagonal corner spend follows the gate

# --- THE CHAIN BILL (WAVE 13) ---------------------------------------------
# Wave 12 gated the three EXPENSIVE arms on establishment and left the FERRY
# and the LAUNCHER un-gated on purpose -- they are how establishment HAPPENS,
# and gating them on establishment is a deadlock.  The open question it left
# was whether the TRANSPORT keeps billing after the gate has given up: a body
# that has latched `cg_ev_dead` has hold-fire, the FIN window and the corner
# spend all shut, and if it were still buying 20-Ti ferry launchers to carry a
# rider toward a cage that has been retired for the game, that spend would be
# the whole residual loss of the -9.0 pp half.
#
# THIS FLAG MAKES THE ANSWER STRUCTURAL.  Arm D: a body past
# CAGE_EVGATE_DEADLINE that has never seen an evictor stops REBUILDING the
# chain -- no new ferry launchers, no new lifts, and no throw served for a
# claim stamped after the deadline.  A launcher already standing with a live
# claim finishes its current throw (the claim carries the round it was written
# and the test is on THAT, not on the launcher's own blind eyes), and
# self-destruct proceeds exactly as before.  Before the deadline nothing here
# changes.
#
# ---- AND IT IS INERT AT THE SHIPPED CONSTANTS.  MEASURED, NOT ASSUMED. ----
# `CAGE_FERRY_MAX_RND` is 80 and `CAGE_EVGATE_DEADLINE` is 80, so the ferry's
# own clock already refuses every build this arm would refuse, and
# `CAGE_FERRY_STALE` (4) already expires every claim this arm would decline to
# serve.  The wave-12 corpus says so directly -- 540 games of `leap10_est`
# (`results/wave12/replays_est/cand_vs_opp_mimic_{istones,juusto}`), split on
# whether a `CG evictor` marker ever fired by r80:
#
#   NO-EVICTOR half   n=258   CG lift 1.32-1.38/game   ALL of it at r <= 80
#                             CG ferry 1.17-1.20/game  ALL of it at r <= 80
#                             post-r80 lift/ferry/post/sd: 0 events, 0 games
#
# The residual bill wave 12 named is real and it is NOT late: every titanium
# the chain spends in a game that never establishes is spent INSIDE the
# attempt window, which is the window the plank is required to protect.  Arm D
# therefore converts a numeric coincidence between two constants into an
# invariant the gate owns, and buys nothing today.  `CG chaincut` is the
# instrument: it fires only where this arm refuses something the old clock
# would have ALLOWED, so a zero count is the proof of inertness and a non-zero
# count means the two constants have drifted apart.
CAGE_CHAIN_DEADLINE_ON = True   # arm D: the ferry chain follows the deadline

# --- ESTABLISHMENT EFFORT (bots/leap10_est only) --------------------------
# Wave 11 established an evictor in roughly HALF the games.  The gate above
# makes that number the whole win: on the other half the bot is leap6, which is
# a floor and not a gain.  This arm buys attempts.  Two changes, both bounded:
#
#   (1) THE ARRIVING FERRY BUILDS THE POST.  The rider's ferry stops dead at
#       CAGE_FERRY_STOP_DSQ ("there") and hands establishment to arm 4, whose
#       site set is the four ring CORNERS and which therefore fails whenever
#       all four are occupied, bricked or unreachable.  With this flag the
#       arrived rider may buy ONE launcher on an adjacent tile whose own pickup
#       disc touches a ring tile -- which is the definition of the evictor post
#       and a strictly larger site set than four corners.
#   (2) CONVERT BEATS SELF-DESTRUCT.  `_cg_ferry_launch` converts a sited relay
#       only when the throw ALSO landed the rider inside the establishment
#       radius or a foothold was already live.  A sited launcher IS the thing
#       this batch gates on; the establishment term is a second-guess worth the
#       ~2 Ti of scale refund.  With this flag, SITED alone converts.
#
# THE BUDGET IS THE POINT.  `CAGE_EST_LAUNCH_CAP` counts EVERY launcher this
# body buys -- ferry hops, the post, arm 4's corner build -- and 3 is the cap
# for the game.  A retry arm with no counter is how the glacierkeep opening
# bank went 470 -> 105 by t7 (see CAGE_FERRY_TI_FLOOR), and the post is a
# scaled purchase made at the ring where the scale is already high.
CAGE_EST_RETRY = True
CAGE_EST_RETRY_RND = 60      # attempts stop here: an evictor sited after this
                             # has ~no game left to earn its scale back, and
                             # the gate's own deadline is r80
CAGE_EST_LAUNCH_CAP = 3      # launcher builds per BODY per game, all arms
CAGE_EST_RESERVE = True      # hold ONE of those three back for the post, so a
                             # rider cannot spend the whole budget on transport
                             # and arrive with nothing to build.  MEASURED BOTH
                             # WAYS and unresolved -- see DOCTRINE 21.3: the
                             # reserve establishes at r5-r7 on short trunks and
                             # costs the third hop, hence the ring itself, on
                             # long ones.  `bots/leap10_noresv` is the ablation.
CAGE_EST_TI_FLOOR = CAGE_FERRY_TI_FLOOR_NEAR   # 120.  The post is bought at
                             # the ring at r20-60, past the trunk build-out the
                             # long-trunk floor (220) exists to protect, so it
                             # holds the SHORT floor -- a measured number, not a
                             # new one.


# ============================================================================
# WAVE 15 -- THE SEAT WAR.  PLANK SEATHOLD + PLANK LPECK (DOCTRINE 23)
# loki_leap12, 2026-08-17.  Fork of loki_leap11, nothing else changed.
# ============================================================================
#
# THE EVIDENCE, in one table (analysis/elite_gap.md 3, n=270 pool games):
#
#   enemy-held seats @ r50 |  n  | our r100 Ti | our win rate
#   -----------------------+-----+-------------+--------------
#            0-1           |  25 |     715     |    84.0 %
#            2-3           |  47 |     315     |    53.2 %
#            4-5           |  86 |     170     |    31.4 %
#            6-8           | 112 |      50     |    16.1 %
#
# r(seats held @ r50, our r100 Ti) = -0.759, n=251 -- STRONGER than the
# whole-game peak (-0.727), which is the tell that the seal is upstream of the
# economy and not a trailing symptom of an already-lost game.  Median state
# against `mimic_jython`: 5 of 8 seats gone by r50, 7 of 8 at peak.  Their own
# titanium is flat at 380-420 whether we win or lose: we are not out-produced,
# we are SEVERED AT THE DELIVERY SEAT.
#
# The three ranked loss causes are ONE BRICK.  A conveyor delivers into the
# Core only from the 8 orthogonal seats, and those are the same 8 tiles a
# builder must stand on to heal (engine_mechanics.md B/E).  A barrier on a
# seat is impassable and cannot be built over (N.6).  So one enemy brick on
# one seat simultaneously cuts a delivery route AND removes a heal slot --
# which is why "economy strangulation" (30.3 % of losses) and "pair-band
# siege" (39.0 %, answered by healers at +4 HP/round each) both trace back
# here.
#
# WHY BODIES AND NOT BRICKS.  We cannot brick our own seats: our own barrier
# blocks our own delivery exactly as theirs does.  The engine leaves exactly
# one denial primitive:
#   * N.6  a tile holding a bot cannot be built on BY ANYONE -- can_build is
#          False on an occupied tile, so a seated body denies the brick;
#   * F    builders cannot fire on builders -- a seated body is UNPECKABLE, it
#          can only be removed by a launcher throw;
#   * B    a body on a seat heals a Core tile for 1 Ti / +4 HP, so the denial
#          is not idle time -- it is the same +4 HP/round the band sentinel
#          answer needs.
# Three seated bodies is +12 HP/round, which beats two band sentinels.
#
# WHAT THE JYTHON DECODE SAYS WE WILL MEET (wf_c6367159-5e5):
#   * their first brick lands at t8 and it goes on a HEAL SEAT FIRST;
#   * their cage launchers stand ON our ring12 from t28 and never self-destruct
#     -- 609 evictions of our bodies across the corpus;
#   * they shoot our CONVEYORS before our Core (447 conveyor shots before the
#     first core hit).
# A launcher standing on our ring is, by definition, in peck reach of a seated
# body: 30 HP, 2 damage a peck, 15 pecks and the eviction engine is gone.  That
# is PLANK LPECK, and it is why the two planks ship together -- SEATHOLD
# without a launcher answer is 609 free throws.
#
# ---------------------------------------------------------------- SEATHOLD --
# TRIGGER.  An enemy unit or building seen within d <= 10 of our Core before
# SH_UNTIL.  Own eyes this round first (the sensing loop in `_builder` already
# computes exactly this distance for every nearby entity, so the signal is
# FREE -- one integer compare added to a loop that runs anyway); the shared
# S1/S3 stamps in SLOT_ARCH_SEEN are the fallback, so a body that has seen
# nothing itself still gets the team's eyes.  d <= 10 is deliberately WIDER
# than S1/S3's d <= 8: their first brick lands at t8 and the walk to it starts
# outside the latch band.
#
# THE ROSTER.  Up to SH_BODIES home-side builders (raiders never -- LOKI-QUIET
# is not in dispute).  There is NO FREE STORE SLOT to publish a claim on (see
# the SAP block: slots 0-15 are all multiplexed), and none is needed: the cap
# is enforced by a local scan.  A body claims a station only when
#     (bodies already ON a non-feeder seat) + (eligible peers with a LOWER id)
#         < SH_BODIES
# which is deterministic, converges without communication, and cannot produce
# the failure the SAP block records -- three of six builders committing to one
# tile and the economy finishing on ten titanium.
#
# THE FEEDER CARVE-OUT, and it is the whole safety case.  `delivery_seats()`
# already names the seats our own conveyors deliver through (HS_DELIVERY_SEATS
# = 2 of them).  SEATHOLD NEVER STATIONS ON THOSE.  A body on a feeder seat
# would block our own conveyor socket -- we would be doing the enemy's work
# for him, at 1 Ti a round.  Six seats are eligible, three are ever taken.
#
# THE SEAT CHOICE.  Nearest to the intruder's approach, because the brick
# lands where the enemy builder already is.  Ties go to the nearest to us.
#
# NOT IDLE.  A stationed body's action ladder, in order:
#   1. LPECK -- an adjacent enemy LAUNCHER (the eviction engine, 30 HP);
#   2. heal a damaged Core tile (1 Ti, +4 HP -- the band-sentinel answer);
#   3. heal a damaged adjacent own building (their 447 conveyor shots);
#   4. peck an adjacent enemy building, ring barriers first (2 dmg, 15 pecks
#      on a 30 HP brick), then the standard sabotage ranking.
# The QUIET carve-out in `_sabotage_prio` does not apply: QUIET's evidence is
# about a RAIDER's round at their ring, and this is a home body whose round is
# already committed to the tile it is standing on.
#
# EVICTION RESPONSE.  A launcher throw is detectable with no API call at all: a
# unit cannot displace more than a king move under its own power, so
# d^2 >= SH_JUMP_DSQ between this body's own consecutive positions IS a throw
# (this is the same scale-free test tools/elite_loss_decode.py uses on their
# throws).  On detection the body WALKS STRAIGHT BACK -- the claim outlives
# SH_UNTIL, because giving the seat up on a clock is exactly what the throw is
# buying -- and remembers the launcher within pickup range (d^2 <= 2) of the
# seat it lost as the TOP peck target for SH_EVICTOR_RNDS.
#
# The "top priority for every OTHER seated body" half of the design is served
# by PLANK LPECK rather than by a broadcast: with LP_ON every body already
# ranks a launcher near our Core above all other sabotage, so the evictor is
# top priority for all of them without a slot write.  Honest limitation: the
# throw VICTIM's specific memory is per-unit and does not propagate.
#
# ------------------------------------------------------------------ LPECK --
# Generalised out of SEATHOLD so it also fires for the defender, the expanders
# and the socket-guard bodies: any of our builders standing orthogonally
# adjacent to an enemy LAUNCHER within LP_NEAR_DSQ of our Core pecks it above
# all other sabotage.  Rationale, all measured: a launcher near our base is the
# cage's delivery AND eviction engine; it is 30 HP where a Sentinel is 60; it
# is a BUILDING, so unlike the enemy builder beside it we can actually hit it.
# `SAP_TARGET_TYPES` has always contained LAUNCHER; what was missing is that
# `SABOTAGE_PRIO` ranked it 3 -- below CORE and HARVESTER -- and
# `CORE_THREAT_TYPES` never let one become a SAP target at all.  LP_PRIO fixes
# the first; the adjacency peck fixes the second without touching the turret
# bearing logic (`CORE_THREAT_TYPES` is read by `_turret` and by the SLOT_THREAT
# latch, and widening it there would re-aim 30 Ti of Sentinel).
#
# The peck does NOT claim the turn: it spends the action and lets the body make
# its normal move, because `_expand` and `_raid` both re-check the action
# cooldown before every build.  A free peck is the whole point.
#
# INERTNESS.  SH_ON = LP_ON = False makes this file behaviourally identical to
# loki_leap11: no store writes, no prints, no decisions.  `bots/leap12_off` is
# the ablation.
#
# STANDING RISKS, pre-registered:
#   R1  ECONOMY.  Three bodies parked from ~r8 are three bodies not building
#       harvesters.  The feeder carve-out and SH_CHAIN_GUARD (a body carrying a
#       trunk chain is never claimed) are the mitigations; the bar is our own
#       Ti collected against a leap11 control, and it must not fall.
#   R2  SEATHOLD sits BELOW the SAP call in `_builder`, so a defender with a
#       live besieger in band still WALKS OFF a seat to sap it.  That is
#       deliberate (CT-2 is worth more than the seat and SH_BODIES = 3 leaves
#       cover), but it means the r50 census may under-read on maps where a
#       band sentinel establishes early.
#   R3  A seat that is already bricked is `is_tile_passable` False, so this
#       plank cannot RETAKE a seat -- it can only get there first.  If the
#       r50 census does not move, the trigger is late, not the mechanism wrong.
#   R4  Eviction detection cannot distinguish a launcher throw from any other
#       forced displacement.  At SH_JUMP_DSQ = 4 nothing else in this engine
#       produces one, but a future teleport primitive would false-positive.
# ============================================================================

SH_ON = True                 # PLANK SEATHOLD master switch
SH_UNTIL = 120               # last round a NEW station may be claimed; a body
                             # walking back from a throw keeps its claim past it
SH_BODIES = 1                # home-side bodies stationed at once, hard cap.
                             # WAVE-17 CHANGE, 3 -> 1.  The wave-14 dose
                             # response is the evidence: the arm that averaged
                             # ~1.4 stationed bodies a turn (leap12_eco, the
                             # eco-gated roster) read 61.9 % overall against
                             # mate_sleipnir while the un-gated three-body
                             # roster (loki_leap12) read 64.4 % -> 38.9 % on
                             # the jython cell, and the wave-15 smoke priced
                             # the difference at -59.7 Ti @r100 overall and
                             # -95 Ti against `mimic_jython`.  Seats held is a
                             # BAND, not a monotone: one body, eco-gated, sits
                             # inside it and three collapse the economy that
                             # has to pay for everything else.  With
                             # SH_ECO_GATE_ON the roster is now 1 before the
                             # harvester shell and 1 after -- the gate stays
                             # ON so the ballot keeps its early floor
                             # semantics and the flag remains the A/B knob.
SH_TRIGGER_DSQ = 100         # "within d <= 10 of our Core" -- an enemy unit OR
                             # building, seen this round by this body
SH_TEAM_SIGNAL_ON = True     # fall back to the shared S1/S3 stamps (slot 13)
SH_RAIDERS_ON = False        # raiders never station (LOKI-QUIET)
SH_BAND_DSQ = 64             # who counts as a home-side peer for the id ballot
SH_CHAIN_GUARD = True        # a body carrying a trunk chain is never claimed
SH_JUMP_DSQ = 4              # own d^2 between consecutive rounds => THROWN
SH_EVICT_DSQ = 5             # how far from the lost seat the thrower can be:
                             # pickup is d^2 <= 2 and 99.8% of 4907 field
                             # throws are within 5 once the victim's own move
                             # earlier in the round is counted
SH_BACK_RNDS = 40            # rounds a thrown body keeps walking back
SH_EVICTOR_RNDS = 30         # rounds the remembered evictor stays top target
SH_HEAL_ON = True            # arm: heal Core / adjacent own buildings
SH_PECK_ON = True            # arm: peck adjacent enemy buildings
SH_TI_FLOOR = 2              # titanium kept back from a 2 Ti peck (= SAP's)
SH_LOG = True                # SH seat (x,y) / SH back (x,y) markers

# THE ECONOMY GUARD, OFF BY DEFAULT.  Risk R1 above is not hypothetical: the
# wave-15 smoke measured it.  On frostgate the leap11 control collected 760 Ti
# by r100 and this plank collected 0, and the 693-turn grind that followed is
# what a five-body roster with three of them standing still looks like.  The
# guard holds the roster at SH_BODIES_EARLY until the harvester shell exists.
# It is a FLAG and not a default because the ask specified SH_BODIES = 3 and a
# knob turned after seeing one 12-cell batch is a fit, not a mechanism --
# `bots/leap12_eco` is the arm that settles it.
SH_ECO_GATE_ON = True
SH_ECO_HARV = 2              # harvesters that count as "the shell exists"
SH_BODIES_EARLY = 1          # roster below that floor

LP_MARK_MAX = 16             # launcher tiles a single body will ever mark

LP_ON = True                 # PLANK LPECK master switch
LP_NEAR_DSQ = 100            # "near our Core", same band as SH_TRIGGER_DSQ
LP_ANYWHERE_ON = False       # off: a raider at THEIR ring keeps QUIET
LP_PRIO = -1                 # `_sabotage_prio` rank for a launcher near our
                             # Core -- above GUNNER/SENTINEL's 0, per the ask
                             # "rank LAUNCHER >= GUNNER near our core"
LP_TI_FLOOR = 2              # titanium kept back from the peck
LP_LOG = True                # LP hit (x,y) / LP kill (x,y) markers
# THE WALK, and the measurement that forced it.  Across 8 wave-15 legs vs
# `mimic_jython` an enemy launcher stood within d <= 10 of our Core for 678,
# 533, 407, 331... ROUNDS A GAME -- and orthogonally adjacent to one of our
# bodies for 0 to 5.  A 30 HP launcher needs 15 adjacent rounds to die, so an
# adjacency-only plank cannot ever kill one: LP kill was 0 by construction, not
# by accident.  With this flag a launcher inside LP_NEAR_DSQ is nominated as a
# SAP target, which hands it to the one walker this lineage already trusts (the
# defender, one body, seat-first, committed for SAP_MAX_RNDS).  `_sap` re-checks
# SAP_BAND_DSQ = 64 itself, so the wider sighting band cannot pull the defender
# past the measured band; and it ranks strictly BELOW a real turret, which is
# still doing 9 HP a round to the Core while the launcher is doing none.
# NOT done via CORE_THREAT_TYPES: that set is read by `_turret` and by the
# SLOT_THREAT latch, and widening it would re-aim 30 Ti of Sentinel.
LP_SAP_TARGET_ON = True


# ============================================================================
# WAVE 17 -- PLANK RG, THE REACTIVE RING GUNNER  (bots/loki_leap13)
# ============================================================================
# THE PROBLEM, in one sentence from the Jython decode: ONE early raider walks
# to our ring at t8 and lays the cage a brick at a time, and nothing we own can
# touch it.  A builder cannot fire on a builder (engine_mechanics F); our
# barrier cannot go on our own seat; SEATHOLD can only get to a seat FIRST, it
# can never retake one (wave-15 risk R3).  The elite pack answers this with
# REACTIVE HOME GUNNERS 3:1 -- but at r92 and r129, which is after their own
# cage is already sealed.  We need the same answer far earlier.
#
# THE KILL MATH, and it is the whole justification:
#   * an intruding builder is 40 HP and must stand ORTHOGONALLY ADJACENT to a
#     ring tile to brick it (a build target is adjacent-only, sec G);
#   * a gunner does 7 damage a round to the NEAREST bot or building in its
#     three-tile ray, every round, no cooldown (sec D) -> six rounds, dead;
#   * turrets are the ONLY thing in this engine that can damage a builder bot,
#     so this is not one option among several, it is the only one;
#   * their launcher CANNOT evict a gunner.  A launcher throws BUILDER BOTS;
#     a gunner is a building.  The plank they use against SEATHOLD does not
#     apply to this plank at all.
#   * 30 Ti + ~24-40 Ti of shots against a 30 Ti body that is otherwise free to
#     lay eight bricks is the best trade on the board.
#
# ---------------------------------------------------------------- TRIGGER --
# ENEMY **BUILDER BOTS ONLY**, within d <= 8 of our Core, before RG_UNTIL.
# This is the detector's S3 signal, which `_arch_note` already stamps into slot
# 13 bits 10-19 and which is set from `et == EntityType.BUILDER_BOT` and from
# nothing else -- turrets set S1/S2, never S3.  That purity is the point and it
# is load-bearing: against `mimic_0033`, whose whole opening is CREEPER TURRETS
# walked onto our doorstep, this plank must stay SILENT, because the answer to
# a 60 HP Sentinel is SAP / counter-battery and not a 30 Ti gunner that will be
# out-ranged.  Own eyes this round first (`_builder`'s sensing loop already
# computes the exact distance for every nearby entity, so the signal is free);
# the shared S3 stamp is the fallback so a body that saw nothing still gets the
# team's eyes.  d <= 8, NOT SEATHOLD's d <= 10: the gunner's ray is three tiles
# from a post two tiles out, so a sighting we cannot possibly cover is not a
# trigger, it is a 30 Ti mistake.
#
# ------------------------------------------------------------------- SITE --
# ONE gunner, within RG_SITE_DSQ (d <= 2) of our Core footprint, and NEVER on
# one of the twelve ring tiles -- those are our eight delivery sockets / heal
# seats and the four corners the launcher and the spawner need, and a turret is
# an impassable building.  Sited from a builder standing beside it: a build
# target must be orthogonally adjacent to the builder (sec G), so the search is
# over the four cardinal neighbours of whichever home body gets there first.
#
# ----------------------------------------------------------------- FACING --
# Verified, never assumed, with `get_attackable_tiles_from` -- the same
# hypothetical-turret call `_t5_home_gunner` uses.  A facing is accepted only
# if BOTH:
#   (a) its ray COVERS THE TILES THE INTRUDER STANDS ON, which are NOT the
#       tiles it bricks.  A build target must be orthogonally adjacent to the
#       builder (sec G), so a body filling one of our ring tiles is standing on
#       the SHELL just outside the ring and never on the tile it fills.  The
#       first smoke leg measured the cost of getting this backwards: sited on
#       ring coverage the gun killed both bricks at (8,7) and (9,8) and the
#       builder that laid them worked the whole sequence from (8,8), (9,9),
#       (10,9), (11,9) -- never once on the ray.  WORK TILES are therefore
#       ring + shell, 1 <= dsq_core <= RG_WORK_DSQ, scored by how near each
#       covered tile is to the body we can actually see, with a dominating
#       bonus for covering that body outright.  A CARDINAL facing reaches
#       three tiles where a diagonal reaches two, so the score prefers a gun
#       laid tangentially ALONG the shell -- which is the line the intruder
#       walks;
#   (b) it is FRATRICIDE-CLEAN.  Rule 9 of the mechanics table is not a
#       footnote: "turrets hit friendly units, including your own core and your
#       own builders", and a misaimed sentinel of ours ground our own Core from
#       500 to 212.  A gunner hits the NEAREST occupant of its ray, so any
#       facing whose ray contains a tile of our own Core footprint, or a tile
#       holding one of our own buildings, or one of the two FEEDER seats our
#       conveyors deliver through, is rejected outright -- before the score,
#       not as a tiebreak.  We would rather not build than build a gun pointed
#       at our own delivery.
# Score, best first: the ray covers the intruder itself, then the most ring
# tiles covered, then the nearer post.  Ties are broken on coordinates so the
# choice is deterministic.
#
# --------------------------------------------------------------- ROTATION --
# The intruder walks; the ray is three tiles.  `_idle_rotate` already exists
# and already pays 10 Ti only for a facing that lands, only when the current
# one does not, and never straight back to the facing it just left
# (ROTATE_DISCIPLINE_ON).  What it does NOT do is prefer the builder: its
# ranking puts any CORE_THREAT_TYPES entity ahead of a builder at any distance,
# which is right for a forward tube and wrong for this one -- the whole reason
# this gun exists is the body laying bricks.  RG_ROT_ON adds one pre-pass, and
# ONLY for a gunner of ours standing within RG_SITE_DSQ of our own Core:
# prefer the nearest enemy BUILDER inside gunner range as the rotate target.
# Everything downstream -- the 10 Ti cost, the cooldown, the anti-thrash
# lock, the `can_rotate` check -- is the incumbent machinery, untouched.
# Fratricide is re-checked on the rotate too: a facing whose ray would put one
# of our own buildings or Core tiles in front of the target is refused.
#
# RE-SITING (destroy + rebuild one tile over) is DELIBERATELY NOT IMPLEMENTED,
# and RG_RESITE_ON is the stub flag that records the decision.  `destroy()`
# refunds NO titanium (sec API), so a re-site is 30 Ti plus a fresh +20 % cost
# scale for a geometry problem an 8-way rotate from a post two tiles out
# almost always solves -- diagonal facings are legal for gunners.  If the
# smoke shows rotations that cannot land, this is the flag to turn on.
#
# ----------------------------------------------------------------- BUDGET --
# ONE gunner, full stop.  RG_MAX = 1, enforced three ways: a per-unit latch, a
# local scan of our own live home turrets (`_home_guns`), and the SLOT_HOME_GUN
# counter every other turret arm in this tree already maintains.  A SECOND
# home gunner is REFUTED TERRITORY -- T5_HOME_GUNNER_ON and SG_RING_TURRET are
# both shipped OFF in this lineage precisely because home-turret spend measured
# negative -- so this plank buys the one the kill math pays for and stops.
#
# ---------------------------------------------------------------- MARKERS --
#   `RG up (x,y) f=D r=N`  the gunner went up, with its verified facing
#   `RG rot D->D r=N`      it re-aimed onto a builder
#   `RG kill (x,y) r=N`    a shot took an enemy builder to <= 0
#
# INERTNESS.  RG_ON = False makes this file behaviourally identical to
# bots/leap12_eco at SH_BODIES = 1: no builds, no rotations, no prints.
# `bots/leap13_rgoff` is the ablation.
#
# STANDING RISKS, pre-registered:
#   R1  COST SCALE.  A gunner is +20 % on every building still to be laid
#       (cost scale), on top of 30 Ti and the per-shot ammunition draw, and
#       the wave-15 measurement says the jython cell is ALREADY titanium-poor
#       at r100.  RG_TI_FLOOR and RG_MIN_RND are the mitigations; the bar is
#       our own r100 titanium against a leap12_eco control, and the honest
#       read is that this plank is a TRADE until that number is in.
#   R2  FRATRICIDE.  The build-time facing check is a snapshot.  A conveyor
#       laid later, or one of our own bodies walking into the ray, can put a
#       friendly in front of the gun -- the ray hits the NEAREST occupant and
#       does not care whose it is.  The build-time ban covers our Core, our
#       standing buildings and the two feeder seats; it CANNOT cover a
#       building that does not exist yet.  RG_SITE_DSQ = 8 keeps the gun close
#       enough that the ray is short and mostly over ring tiles.
#   R3  THE TRIGGER IS A SIGHTING, NOT AN INTENT.  A scout builder that walks
#       past our ring and leaves buys the same 30 Ti as a cage-layer.  The
#       clock (RG_UNTIL) and the one-gun cap bound the loss at exactly one
#       gunner a match.
#   R4  SENTINEL ANSWER.  Their sentinels can and will kill this gunner.  The
#       plank is priced on the assumption that if it dies after r80 it has
#       already paid for itself -- the cage it denied is worth more than the
#       30 Ti -- and that assumption is NOT measured here.
# ============================================================================

RG_ON = True                 # PLANK RG master switch
RG_UNTIL = 100               # last round a NEW reactive gunner may be built
RG_MIN_RND = 4               # never before this: the opening build order pays
                             # for the harvester shell that pays for the gun
RG_TRIGGER_DSQ = 64          # "an enemy BUILDER within d <= 8 of our Core"
RG_TEAM_SIGNAL_ON = True     # fall back to the shared S3 stamp (slot 13 bits
                             # 10-19), which is BUILDER-ONLY by construction
RG_SITE_DSQ = 8              # the post stands within 2 tiles of the footprint
RG_OFF_RING = True           # ...but NEVER on one of the twelve ring tiles
RG_COVER_RING_ON = True      # the ray must cover WORK TILES (see below)
RG_WORK_DSQ = 8              # a "work tile" is 1 <= dsq_core <= 8: our twelve
                             # ring tiles PLUS the shell just outside them.
                             # THE SHELL IS THE POINT, and the first smoke leg
                             # is why: a build target must be orthogonally
                             # adjacent to the builder, so the body bricking
                             # one of our ring tiles STANDS ON THE SHELL and
                             # never on the tile it is filling.  A ray scored
                             # on ring coverage aims one tile behind the
                             # target -- measured on nordkap, where the gun
                             # killed both bricks at (8,7)/(9,8) and never
                             # once had the builder that laid them on its ray.
RG_NEAR_M = 6                # a covered work tile scores (6 - manhattan) to
                             # the sighted intruder, floored at 0: it walks a
                             # tile a round and the ray is three tiles long
RG_INTRUDER_BONUS = 20       # ...and covering the body itself dominates
RG_MIN_SCORE = 4             # below this the gun is scenery -- wait instead.
                             # Only applied when we have a live sighting; on
                             # the team-signal-only trigger one work tile does
RG_NO_FRIENDLY_RAY = True    # ...and must contain NO tile of our own Core, no
                             # tile holding one of our own buildings, and
                             # neither of the two feeder seats.  Rule 9.
RG_TI_FLOOR = 10             # titanium kept back beyond the gunner's cost
RG_MAX = 1                   # ONE.  A second is refuted territory.
RG_ROT_ON = True             # prefer an enemy BUILDER as the rotate target,
                             # for a gunner of ours near our own Core only
RG_ROT_UNTIL = 400           # after this the incumbent ranking takes over
RG_RESITE_ON = False         # destroy+rebuild one tile over: NOT implemented,
                             # see the block above (destroy refunds nothing)
RG_LOG = True                # RG up / RG rot / RG kill markers
RG_GUN_DMG = 7               # one gunner shot, for the kill marker's threshold


# ============================================================================
# WAVE 17b -- PLANK SPLIT, THE SECOND DELIVERY ROUTE  (bots/leap13_split)
# ============================================================================
# THE PROBLEM, straight off analysis/elite_gap.md: 30.3 % of our pool losses to
# the #1's doctrine are ECO STRANGULATION -- r100 titanium 80 in losses against
# 330 in wins -- and the single variable that predicts everything is OUR OWN
# EIGHT SEATS being enemy-held by r50 (r = -0.759; 0-1 held -> 715 Ti and 84 %
# wins, 6-8 held -> 50 Ti and 16 %).  The seats are not only heal seats: they
# are the ONLY tiles a conveyor can deliver into a 2x2 Core from (a conveyor's
# facing must be cardinal, so the four diagonal ring tiles can never feed it,
# engine_mechanics B).  A trunk chain therefore ends in exactly ONE socket, and
# one brick on that socket is the whole economy.
#
# WHAT NOBODY HAS EVER TRIED.  In 1,010 decoded ladder sides there is not one
# SPLITTER.  Not ours, not the #1's, not I Stone's 198-conveyor macro.  It is
# the only building in the game with an unexplored use, and its use is exactly
# the shape of the hole above:
#
#   * it accepts input ONLY from the tile directly BEHIND it;
#   * it has THREE outputs -- the facing plus the two flanking cardinals, i.e.
#     every neighbour except the back;
#   * and it SKIPS DEAD OUTPUTS.  Measured, not assumed: a splitter at (4,3)
#     facing NORTH, back-fed by a harvester, with N and E on empty ground and
#     W on the Core, delivered to the Core EVERY four-round cycle.  It did not
#     stall and it did not lose two thirds of its stacks
#     (analysis/engine_mechanics.md B).
#
# THE GEOMETRY, and it is the whole plank.  The eight sockets are the
# orthogonal ring tiles; the four DIAGONAL ring tiles -- `core_corners` -- are
# the only tiles on the board orthogonally adjacent to TWO sockets at once (a
# corner touches the two sockets flanking it and no Core tile; the two sockets
# of one FACE have no common orthogonal neighbour at all).  So:
#
#       .  U  .            U   the trunk arriving from outside
#       S1 X  .            X   the fork: our splitter, back to U
#       #  S2 .            S1  socket, conveyor -> Core     #  Core
#                          S2  socket, conveyor -> Core
#
# One incoming line, TWO delivery sockets.  Bricking or shooting out either
# socket no longer severs delivery -- the splitter reads that output as dead
# and pushes the next stack through the other one, with no code of ours in the
# loop.  The redundancy costs 3 Ti of price difference (splitter 6, conveyor 3)
# plus one extra socket conveyor, at the SAME +1 % cost scale as the conveyor
# it replaces.
#
# ------------------------------------------------------------------- ARMS --
# A  THE FORK IS LAID BY THE TRUNK ITSELF (`_build_next_link`).  The chain is
#    planned by `_link_path`, whose goals are the sockets, and whose PENULTIMATE
#    tile is therefore always either the corner beside its terminal socket or
#    the tile straight out from it -- every socket has exactly four neighbours
#    (one Core tile, one corner, the other socket of its face, one outer tile)
#    and every socket is a BFS root, so no socket can ever be the parent of a
#    socket.  When that penultimate tile IS the corner, the trunk lays a
#    SPLITTER there instead of a conveyor, facing away from the live feeder so
#    the feeder is its back.  Zero detour, zero re-route, one build that was
#    going to happen anyway.  When it is the outer tile the geometry does not
#    carry two sockets and the plain conveyor is laid exactly as before -- that
#    is the FALLBACK, and `SP geom` counts both cases so the coverage rate is
#    measured rather than assumed.
# B  THE FORK IS RE-LAID (`_sp_fork`).  A splitter is 20 HP -- three gunner
#    rounds -- so the hole it leaves is the same hole `_l4_repair` already
#    knows how to fill, and a corner hole with a live feeder and a live
#    terminal socket beside it is re-forked rather than re-conveyored.
#    SP_CONVERT_ON additionally upgrades a STANDING corner conveyor: destroy is
#    free, costs no action cooldown and removes its own +1 % scale in the same
#    round (engine_mechanics K), so the swap is 3 Ti net.  If the splitter
#    build then fails for any reason the conveyor is put straight back in the
#    same round -- the trunk is never left severed on our own initiative.
# C  THE SECOND SOCKET IS WIRED (`_sp_wire_seat`).  A splitter output pointing
#    at empty ground is a dead output, so the fork is worth nothing until the
#    OTHER flanking socket holds a conveyor facing the Core.  Any body standing
#    beside that socket lays it.  Stateless, like `_l4_repair`: the condition
#    (our fork adjacent, socket empty, Core adjacent) is destroyed by the fix,
#    so it cannot walk and needs no memory -- which is also what re-wires the
#    socket after they shoot it out.
#
# ------------------------------------------------------------------ COSTS --
# ONE HEAL SEAT.  The second socket conveyor stands on one of our eight seats,
# and a seat holding a building is a seat no builder of ours can heal from and
# no builder of ours can spawn on.  `HS_SEAT_BAN_CONVEYORS` is False in this
# lineage -- the reservation only keeps our own HARVESTERS and TURRETS off the
# non-delivery seats -- so arm C breaks no incumbent rule, but the cost is real
# and it is pre-registered as risk R2.  It is taken because the elite-gap
# finding cuts the other way: in the games we lose those seats are THEIRS by
# r50, and a seat holding our conveyor is a seat they cannot brick.  At most
# SP_MAX of them are spent.
#
# --------------------------------------------------------------- MARKERS --
#   `SP fork (x,y) seats=N f=D r=N`       a splitter laid at a corner
#   `SP seat (x,y) f=D r=N`               the second socket wired
#   `SP conv (x,y) r=N`                   a standing corner conveyor swapped
#   `SP geom (x,y) corner=B seats=N r=N`  every trunk TERMINUS arm A evaluated,
#                                         fork or fallback -- the coverage-rate
#                                         instrument, arm A only
#   `SP corner (x,y) corner=1 seats=N r=N`  arm B re-evaluating a standing
#                                         corner.  A SEPARATE tag on purpose:
#                                         mixing it into `SP geom` inflated the
#                                         coverage denominator by a third in the
#                                         first smoke batch and made the no-bias
#                                         arm read HIGHER coverage than the
#                                         biased one.
#
# INERTNESS.  SPLIT_ON = False makes this file behaviourally identical to
# bots/loki_leap13: no splitter is ever built, `_build_next_link` takes the
# incumbent branch, and `_sp_fork` returns on its first line.
# `bots/leap13_spoff` is the ablation.
#
# STANDING RISKS, pre-registered:
#   R1  20 HP.  A splitter is as fragile as the conveyor it replaces and it now
#       carries the WHOLE line rather than one of its links.  Before this plank
#       the terminus was a 20 HP conveyor, so the exposure is unchanged in
#       kind -- but the fork concentrates it one tile further out, on a corner,
#       which is exactly where a launcher wants to stand.  Not measured.
#   R2  ONE SEAT SPENT.  See COSTS.  With SH_BODIES = 1 the seat roster is
#       already thin and this takes one more off it, permanently.
#   R3  THE FORK CAN BE POINTLESS.  If they never touch our sockets, arm C's
#       conveyor and the 3 Ti of price difference bought nothing at all.  The
#       bill is ~6 Ti and two +1 % scale ticks a game, which is the smallest
#       bet in this file; the bar is r100 titanium against a leap13 control.
#   R4  THE COVERAGE IS GEOMETRY, NOT CHOICE.  Arm A never detours: it forks
#       when the unbiased route happens to arrive through a corner and lays a
#       plain conveyor otherwise.  Biasing the route toward corners is the
#       obvious next lever and is DELIBERATELY not in this batch -- SG arm 1a
#       already measured what goal-biasing a trunk costs.
#   R5  ROUND-ROBIN LATENCY, unmeasured.  A splitter serves its live outputs
#       least-recently-used, so with two live sockets a stack that would have
#       gone straight through now alternates.  Throughput is capped at one
#       stack per tile per round either way and both sockets feed the SAME
#       Core, so this should be exactly zero -- but it has not been probed.
# ============================================================================

SPLIT_ON = False
SP_MIN_SEATS = 2             # sockets a fork must cover, or no fork is laid.
                             # 2 is the whole point: a one-socket "fork" is a
                             # conveyor with extra steps and costs 3 Ti more.
SP_MAX = 2                   # live forks on our own Core corners, team-wide,
                             # censused off the board rather than a store slot
                             # -- every arm here stands beside the corner it is
                             # acting on, so all four corners are inside its
                             # own vision (r^2 = 20) by construction.
SP_MAX_PER_UNIT = 2          # bounds the re-lay loop if a fork is shot out
SP_MIN_RND = 0               # arm A is part of the opening trunk; there is no
                             # round before which the fork is premature
SP_UNTIL = 400               # past this a new fork is not worth its scale
SP_TI_FLOOR = 6              # titanium kept back beyond the build's own cost,
                             # for the arms that START a fork (B and C)
SP_TRUNK_FLOOR = 0           # ...and NONE for arm A, which does not start
                             # anything: it substitutes one building for
                             # another in a chain `_build_next_link` has
                             # already authorised, so the marginal spend is
                             # the 3 Ti price difference and not the 6 Ti
                             # building.  Measured: at frostgate r28 the
                             # shared floor declined the only forkable
                             # terminus of the game on a 14 Ti bank.
SP_BAND_DSQ = 18             # arms B/C only run for a body already at home
SP_CONVERT_ON = True         # arm B may destroy a STANDING corner conveyor to
                             # put the fork in its place (free, no cooldown)
SP_SEAT_WIRE_ON = True       # arm C: wire the second socket
SP_LOG = True                # SP fork / SP seat / SP conv / SP geom markers

# --- arm A2: route the trunk to a corner rather than wait for one ----------
# `tools/split_geometry.py` enumerated arm A's coverage exactly, over all 15
# pool maps, both sides, the three nearest ore tiles of each Core -- i.e. the
# termini a real opening actually wires: the unbiased route arrives through a
# corner on **9.2 %** of them (16.6 % over every ore on the board).  Arm A
# alone is dead code in nine games out of ten, and that is a measurement, not
# a worry.  The same enumeration priced the fix, in extra conveyors:
#
#     detour 0 conveyors ->  39.1 % coverage   (54.7 % over every ore)
#     detour 2 conveyors ->  89.7 %
#     detour 3 conveyors ->  98.9 %            (SG_FEED2_DETOUR's own price)
#
# SP_DETOUR = 0 is therefore the default and it is FREE in the only three
# currencies a trunk has: the chain is the same length, so the same titanium,
# the same +1 % ticks and the same delivery latency -- only its shape changes.
# `bots/leap13_spd2` is the priced 2-conveyor arm for a measurement to choose.
SP_ROUTE_BIAS_ON = True      # re-flood against the corners when the unbiased
                             # route does not already arrive through one
SP_DETOUR = 0                # extra conveyors the biased chain may cost.
                             # 0 == free: an equal-length route or nothing.
SP_BIAS_RND = 120            # past this the opening is over and a second
                             # flood per plan is not worth the CPU


# ============================================================================
# WAVE 18 -- PLANK EARLYBIRD, THE CAGE-ARRIVAL DETECTOR  (bots/loki_leap14)
# ============================================================================
# WHAT THIS BATCH WAS ASKED TO CLOSE, and what the measurement said instead.
# The brief was "close the 23-round gap between their cage start (r9) and our
# response (r32)", on the wave-15 reading that PLANK RG's first kill lands at
# r32-36 against a first brick at r9.  tools/eb_probe.py re-derived both
# numbers off ground truth in the replay -- entity streams, not our own logs --
# over 10 legs of leap13_split vs mimic_jython, 5 pool maps, both sides:
#
#     map          first enemy BUILDER    their first      RG up   first
#                  in d<=8 of our Core    brick on r12             RG kill
#     fjordgate            r1                  r3            r4    r165/r13
#     frostgate            r3                  r6            r4    r109/none
#     nordkap              r3                  r6            r4    none/r304
#     midgard              r11                 r14          r12    none
#     ragnarok             r11                 r15          r15    r77/none
#
# **THE GUN IS NOT LATE.  IT IS BLIND.**  RG up lands at r4-r15, which is at
# or BEFORE their first brick on every map in the pool; the 23-round figure was
# a first-KILL statistic read as a first-BUILD statistic.  tools/eb_probe2.py
# then priced the real constraint, and it is aim: over the same 10 legs the gun
# stood for 52-585 rounds and had an enemy BUILDER on one of its three ray
# tiles for **0-36 of them**, never once in 4 legs of 10.  Ammunition is not
# the constraint either (16 in the bank at RG up, >= 4 from r2 in 10 legs of
# 10).  A three-tile cardinal ray against a body that walks the collar is a
# coin toss, and the coin is landing tails.
#
# So this plank keeps the brief's three arms and re-aims them at what the
# corpus supports.  Arms (a) and (b) are small by construction -- the things
# they were meant to unblock turned out mostly not to be blocked -- and arm
# (c), the one the brief listed last, is the one the numbers argue for: a
# BARRIER is a static 30 HP building standing on a tile one of our own bodies
# is already on, and a melee peck cannot miss.
#
# ------------------------------------------------------------- THE DETECTOR --
# An enemy BUILDER BOT inside EB_TRIGGER_DSQ (d <= 8) of our Core, before the
# window closes, THAT CANNOT HAVE WALKED THERE.  That last clause is the whole
# plank: "an enemy builder near our Core early" on its own is not a cage
# signature, it is a small map.  On fjordgate the two Cores are 6 manhattan
# apart, so their opening builders stand inside our band on ROUND 1 and every
# round after, against every opponent in the pool.  Two independent
# impossibility tests, both exact rather than heuristic:
#
#   WALK-CLOCK (EB_WALK_ON).  A builder moves in the four CARDINAL directions
#   only, one tile, on a 1-round move cooldown (docs/ALL_DOCS.md 1445, 1478).
#   Manhattan distance is therefore not an estimate of walking time, it IS
#   walking time, and a body standing manhattan M from THEIR Core footprint
#   cannot be there before round M.  Trigger when M > rnd + EB_WALK_SLACK.
#   Measured discrimination on the table above: midgard/ragnarok r11 sightings
#   stand at manhattan 39-41 from their Core -- 28 rounds of flight they did
#   not have -- while fjordgate's r1 sighting stands at manhattan 0, which is
#   their own doorstep and is silent by construction.
#
#   JUMP (EB_JUMP_ON).  One entity id, two consecutive observations, manhattan
#   displacement greater than the rounds between them.  One tile a round is the
#   hard ceiling, so anything above it was thrown, and a launcher is the only
#   thing in this engine that throws (SH_JUMP_DSQ records the same fact for our
#   own bodies).  This is what catches the small maps, where the walk-clock
#   cannot: their courier is inside our band from the start, and what gives it
#   away is that it moves 5 tiles in one round.
#
#   OUR OWN LAUNCHERS CANNOT FORGE THIS.  A launcher picks up bots of EITHER
#   team, so a plank of ours that threw an enemy body would manufacture its own
#   evidence.  SG_ON -- the eviction/throw plank -- is False in this lineage
#   and the cage ferry throws our own raiders only, so the JUMP signature has
#   exactly one possible author.
#
#   THE WINDOW, and it is map-aware because the brief was right that it has to
#   be.  EB_EARLY_MAX is the ceiling; the floor keeps a tiny map from getting a
#   window of two rounds.  c2c is the MANHATTAN Core-to-Core distance, which is
#   the walking metric, taken from enemy_core_for -- map symmetry, available
#   on round 1 without ever seeing their Core, and terrain rather than
#   opponent, so it cannot go stale when somebody ships a new version.
#
#       window = min(EB_EARLY_MAX, max(EB_EARLY_MIN, c2c * 7 // 10))
#
#   The window bounds the plank's COST, not its purity: purity is the two
#   impossibility tests, and they are exact.  Pool values: fjordgate 8,
#   nordkap 8, frostgate 9, midgard/ragnarok 15.
#
# ------------------------------------------------------------- THE EVIDENCE --
# SLOT_ARCH_SEEN (13) BIT 30, sticky.  Verified free before claiming: bits 0-9
# PRESSURE stamp, 10-19 INTRUDER stamp, 20 S2, 21-25 S5, 26-27 the enemy-Core
# HP band, 28-29 the FIN window -- and FIN_PUB_SHIFT's own comment reserves
# "30-31 clear (sign safety)".  Bit 31 stays clear; bit 30 is claimed here and
# the word stays positive.  All three incumbent writers preserve it without
# being touched: _arch_note rebuilds under ARCH_KEEP_HI = 0xFC000000 (bits
# 26-31), and _sge_core_band and _fin_publish both clear only their own
# field.  STICKY AND NOT STAMPED, deliberately: this is not a sighting that
# ages out like S1/S3, it is a classification of the opponent's DOCTRINE.  A
# team that ferried a courier onto our ring on round 11 is a launcher-cage team
# for the rest of the match, and a monotone OR has no lost-update race.
#
# ------------------------------------------------------------------- ARMS --
# (a) EB_RG_ON -- THE GUN.  Two changes, both small, because the table above
#     says the gun was already up in time.  On detection RG_MIN_RND and
#     RG_TI_FLOOR are replaced by EB_RG_MIN_RND / EB_RG_TI_FLOOR so the build
#     can happen the same round the courier lands.  The one that actually has
#     teeth is EB_RG_HOLD_ON: BEFORE detection and before EB_HOLD_UNTIL, the
#     one-per-match gun is NOT spent.  On fjordgate the incumbent buys it on
#     round 4 against a builder standing on THEIR OWN doorstep, and that gun
#     went on to hold a target for 3 rounds out of 443.  The hold is bounded:
#     past EB_HOLD_UNTIL, RG is exactly the incumbent plank again, so against
#     an opponent this detector never fires on, the arm costs at most a dozen
#     rounds of delay on a gun that is refuted-territory-capped at one anyway.
# (b) EB_SH_ON -- THE SEAT.  The eco gate (SH_ECO_GATE_ON, roster held at
#     SH_BODIES_EARLY until the harvester shell exists) is waived on detection.
#     HONEST NOTE: with SH_BODIES == SH_BODIES_EARLY == 1 in this lineage that
#     waiver is currently INERT, and _sh_pick_seat already aims at the
#     intruder, so arm (b) is a mechanism with nothing to do at today's dose.
#     EB_SH_BODIES is therefore shipped at 1 -- wave 14's dose-response is
#     explicit that 1.4 bodies/turn wins 61.9 % and 2.4 wins 8.3 %, and this
#     plank is not the place to re-litigate that -- and bots/leap14_eb2 is
#     the 2-body arm for a measurement to choose.
# (c) EB_PECK_ON -- THE BRICK.  _sh_peck already ranks a BARRIER on our own
#     ring12 second only to the launcher that can evict us, and it is reachable
#     by exactly ONE body in the whole team: the single SEATHOLD station, and
#     only on a turn where the launcher and both heals declined first.  Under
#     EARLYBIRD every home-side body gets the same peck, from wherever it is
#     standing, on the same free-action terms PLANK LPECK established (spend
#     the ACTION, never the move; _expand re-checks the cooldown before every
#     build, so a body walking past a brick loses nothing).  30 HP, 2 damage a
#     peck: one body needs 15 rounds, two need 8.  Raiders are excluded --
#     LOKI-QUIET is not in dispute and a raider is at THEIR collar anyway.
#
# --------------------------------------------------------------- MARKERS --
#   EB detect (x,y) m=M d=D why=walk|jump r=N    the latch, once per unit
#   EB gun r=N                                   RG built under an EB waiver
#   EB hold r=N                                  RG declined by the hold
#   EB peck (x,y) hp=H r=N                       a brick pecked by arm (c)
#   EB kill (x,y) r=N                            ...that peck was the last one
#
# INERTNESS.  EB_ON = False makes this file behaviourally identical to
# bots/leap13_split: no tracking dict, no store bit, no waivers, no prints.
# bots/leap14_off is the ablation and bots/leap14_ebonly carries the
# detector with all three arms off, so the detector's cost and its trigger
# purity can be priced apart from anything it does.
#
# STANDING RISKS, pre-registered:
#   R1  THE HOLD CAN COST A GUN OUTRIGHT.  EB_RG_HOLD_ON declines the build
#       for up to EB_HOLD_UNTIL rounds against an opponent whose early builder
#       really did walk.  On fjordgate that is a real behaviour change against
#       EVERY opponent, not only cage ones.  Bounded, ablatable
#       (bots/leap14_nohold), and the reason the guard cells are in the
#       smoke.  NOT measured beyond the smoke.
#   R2  THE PECK IS AN ACTION.  Arm (c) spends 2 Ti and the round's action on
#       up to five bodies at once instead of one.  It never spends the MOVE,
#       and _expand re-checks the cooldown, but a body that would have laid
#       a conveyor this round now lays it next round.  The bill is bounded by
#       adjacency -- a brick has four neighbours -- and the r100 titanium
#       column against a paired control is the price tag.
#   R3  STICKY IS STICKY.  One thrown courier arms arm (c) for 1000 rounds.
#       That is intended (a cage team stays a cage team) but it means a single
#       false positive is not a round of noise, it is a match of it.  Which is
#       why the two impossibility tests are exact and the window is not what
#       the purity rests on.
#   R4  THE DETECTOR DOES NOT FIX THE AIM.  eb_probe2's 0-36 target-rounds is
#       untouched by this batch.  Re-siting or a second facing is the obvious
#       next lever and is DELIBERATELY not in it: RG_RESITE_ON is still the
#       unimplemented stub it was in wave 17, and rotation thrash is measured
#       territory (_rotate_allowed).
#   R5  ONE BAND, TWO PLANKS.  EB_TRIGGER_DSQ and RG_TRIGGER_DSQ are the same
#       64 by design, so anything that moves one must move the other or the
#       waiver in arm (a) fires for a sighting RG itself cannot see.
# ============================================================================

EB_ON = True                 # PLANK EARLYBIRD master switch
EB_TRIGGER_DSQ = 64          # == RG_TRIGGER_DSQ: "d <= 8 of our Core" (R5)
EB_EARLY_MAX = 15            # window ceiling, the brief's default
EB_EARLY_MIN = 8             # ...and its floor, so a 6-manhattan map still
                             # has a window a thrown courier can land in
EB_C2C_NUM = 7               # window = min(MAX, max(MIN, c2c * NUM // DEN)),
EB_C2C_DEN = 10              # c2c = MANHATTAN Core-to-Core (the walk metric)
EB_WALK_ON = True            # signature 1: manhattan-from-their-Core clock
EB_WALK_SLACK = 2            # rounds of doubt handed to the enemy before the
                             # walk-clock calls a sighting impossible
EB_JUMP_ON = True            # signature 2: displacement > rounds elapsed
EB_TRACK_MAX = 16            # enemy builder ids one body remembers at once.
                             # The dict lives only inside the window and only
                             # until the latch, so this is a CPU bound and not
                             # a memory one.
EB_PUB_ON = True             # publish the classification team-wide
EB_PUB_BIT = 1 << 30         # SLOT_ARCH_SEEN bit 30, sticky.  See THE
                             # EVIDENCE: verified free, all writers preserve
                             # it, bit 31 stays clear for sign safety.
EB_LOG = True                # EB detect / gun / hold / peck / kill markers

# --- arm (a): the gun ------------------------------------------------------
EB_RG_ON = True
EB_RG_MIN_RND = 1            # replaces RG_MIN_RND once detected: the courier
                             # is already laying bricks, the opening build
                             # order is no longer the higher claim
EB_RG_TI_FLOOR = 0           # replaces RG_TI_FLOOR (10).  Measured: the bank
                             # held 352-470 Ti at the sighting round on 8 of
                             # the 10 probe legs and 50-121 on the other two,
                             # against a ~30 Ti gunner -- the floor was never
                             # what stopped this gun, and dropping it is a
                             # formality that costs nothing.
EB_RG_HOLD_ON = False         # the arm with teeth: do NOT spend the one gun
                             # before the cage signature (see R1)
EB_HOLD_UNTIL = 16           # ...and never hold past this.  One round above
                             # the largest pool window (15) so that on the big
                             # maps the hold expires exactly when the detector
                             # can no longer fire, and no later.

# --- arm (b): the seat -----------------------------------------------------
EB_SH_ON = False              # waive SH_ECO_GATE_ON's harvester precondition
EB_SH_BODIES = 1             # roster under EARLYBIRD.  1 == today's dose ==
                             # INERT.  See arm (b): wave 14 priced 2 at 8.3 %.
                             # bots/leap14_eb2 is the 2-body arm.

# --- arm (c): the brick ----------------------------------------------------
EB_PECK_ON = False            # every home-side body pecks an adjacent BARRIER
                             # standing on our own twelve-tile collar
EB_PECK_TI_FLOOR = 2         # titanium kept back from the 2 Ti peck (SAP's)
EB_PECK_RAIDERS_ON = False   # LOKI-QUIET: a raider is at THEIR collar
EB_PECK_DMG = 2              # one melee peck, for the kill marker's threshold


# ============================================================================
# WAVE 18, TRACK 2 -- PLANK SPRINT, THE FERRY RACE  (bots/leap14_race)
# ============================================================================
# THE MEASUREMENT THIS PLANK IS BUILT ON (tools/leap14_delay.py, 4 legs,
# leap14_diag vs mimic_jython, midgard + drakkarfjord, both sides, seed 2 --
# CAGE_LOG_WHY on and CAGE_WHY_GAP 3, so every refusal of the ferry is named):
#
#   THEIR ladder, every leg:  rungs at r2 r4 r6 r8 r10 r12 (six), landing at
#     dEnemy 970 -> 650 -> 394 -> 208 -> 90 -> 25, ARRIVAL (d^2 <= 40) r9-r11,
#     ON THE RING r11-r13, FIRST BRICK ON OUR RING r12-r15.
#   OURS, every leg:          rungs at r3 r5 (two -- or ONE on drakkarfjord),
#     ARRIVAL r28-r30, ON THE RING r37-r57, first brick on THEIR ring r35-r40.
#
# So the gap is ~19 rounds of arrival and ~25 rounds of cage, and the refusal
# markers say -- in the bot's own words, three reasons and no others:
#
#   r1   `CG why w=clock  ti=430 n=0`   CAGE_FERRY_MIN_RND is 2 and the rider's
#                                       FIRST TURN IS ROUND 1.  One free round,
#                                       given away for nothing: the bank is 430
#                                       and a rung is ~22.
#   r5+  `CG why w=cap    ti=209 n=2`   CAGE_EST_LAUNCH_CAP 3 minus the one
#                                       CAGE_EST_RESERVE holds back for the
#                                       evictor post == TWO hops a game.  Their
#                                       ladder is six rungs.  After hop 2 the
#                                       rider WALKS, at a measured 0.61 tiles a
#                                       round, and midgard is a 31-tile crossing.
#   r4+  `CG why w=bank   ti=246 n=1`   CAGE_FERRY_TI_FLOOR 220 (drakkarfjord is
#                                       an ORE_NEAR miss at d^2 58).  ONE hop,
#                                       then money-blocked for the whole window
#                                       -- and the trace shows the bank the
#                                       floor protected being spent by the
#                                       economy anyway: 246 -> 115 by r14.
#
# NONE of the three is a geometry problem.  Our site choice is already Jython's
# (`_cg_ferry_try` takes the CARDINALLY adjacent tile with the smallest d^2 to
# their Core == "adjacent, one step ahead"), our throw is already Jython's
# (`_cg_near_sites` is the r^2 <= 26 disc sorted nearest-THEM-first, so the
# throw is at maximum range toward their core, their measured d^2 == 25), our
# rungs already self-destruct (CAGE_FERRY_DISPOSABLE) and our cadence is already
# theirs (rungs r3, r5 == every two rounds).  WE BUILT THE RIGHT LADDER AND
# BOUGHT TWO RUNGS OF IT.
#
# WHAT THE PLANK DOES.  Inside an early window, and inside a titanium budget of
# its own, the rider is allowed the ladder Jython runs: start at r1, up to
# SPR_CAP rungs, on a bank floor sized to the trunk's NEXT build rather than to
# a war chest.  Nothing else changes -- the site choice, the throw, the
# disposal, the wait and the hand-off at the ring are the parent's code
# untouched, which is the whole point of §21.3's lesson: the machinery works,
# it was starved.
#
# THE THREE THINGS THIS PLANK DELIBERATELY DOES NOT DO
#   1. IT DOES NOT SPEND THE PARENT'S BUDGET.  A sprint rung increments
#      `spr_n` and NOT `cg_ferry_n` / `cg_launch_n`, so the evictor post
#      (CAGE_EST_RESERVE) and the parent's own two hops are still there,
#      unspent, when the window closes.  Wave 12 measured what happens when
#      transport eats the budget the destination needed (`CG post` fired once
#      in thirteen legs); this plank does not repeat it.
#   2. IT DOES NOT MOVE THE HAND-OFF.  SPR_STOP_DSQ defaults to
#      CAGE_FERRY_STOP_DSQ, so the rider still stops ferrying at the ring and
#      arm 4 / the post still take it from there.  "The same machinery, just
#      sooner."  `bots/leap14_close` prices carrying the rider all the way in.
#   3. IT DOES NOT STRANGLE THE TRUNK.  WAVE 14's verdict was that the leap12
#      hold paid for itself out of the build-out and lost the game that way, and
#      CAGE_FERRY_TI_FLOOR's own comment is the glacierkeep trace where three
#      early hops took the bank 470 -> 105 and titanium_collected finished at
#      ZERO.  Two independent brakes, both cheap: a TOTAL spend cap
#      (SPR_TI_CAP) and a per-rung bank floor (SPR_TI_FLOOR) that is still
#      above a harvester (base 20) plus its first conveyors (base 3).
# ============================================================================

SPR_ON = True                # master.  False == bots/leap13_split exactly:
                             # every gate below falls back to the parent's
                             # constant and nothing prints.
SPR_MIN_RND = 1              # the rider's first turn IS round 1 -- measured,
                             # `CG why r=1 w=clock ti=430`.  Jython's first rung
                             # is one replay turn ahead of ours for this reason
                             # and no other.
SPR_MAX_RND = 24             # the window.  Their sixth and last ladder rung is
                             # r12 and their cage launchers are a different
                             # population entirely (t28, sited AT the victim's
                             # ring).  Past this the parent's constants rule and
                             # the parent's two hops are still unspent.
SPR_CAP = 6                  # rungs inside the window, matching the six the
                             # corpus counts.  BINDING ONLY IF THE MONEY LASTS:
                             # at ~22 Ti a rung, SPR_TI_CAP is what actually
                             # stops it, and that is deliberate -- the cap that
                             # should bind is the economic one.
SPR_TI_CAP = 180             # TOTAL titanium this body may spend on rungs, for
                             # the game.  The wave-14 lesson in one number.
                             #
                             # /!\ A RUNG IS NOT 20 TI, AND THIS IS THE ONE
                             # NUMBER THE PLANK'S BRIEF GOT WRONG.  Measured off
                             # the `SPR rung ... ti=` markers on midgard and
                             # drakkarfjord: rung 1 costs 28 and rung 2 costs
                             # 38 -- because the cost scale is TEAM-WIDE and our
                             # Core spawns builders #1 and #2 at r1-r2 at +20 %
                             # of scale EACH (engine_mechanics C).  The ladder
                             # therefore prices 28, 38, 44, 50, 56, 62 ... and
                             # Jython's six-rung ladder is ~280 Ti of a 500
                             # opening bank, which it can afford only because
                             # its economy is deliberately tiny (3 builders, ~7
                             # conveyors, scale ~1.2-1.5 all game -- see the
                             # mimic's header).  At the brief's 90 this arm
                             # buys TWO rungs -- the same two the parent bought,
                             # one round earlier -- and MEASURES arrival r23
                             # against the control's r27 (`bots/leap14_spr90`,
                             # DOCTRINE 25b.4).  180 is where the sprint stops
                             # being cap-bound: the median spend is 106 Ti and
                             # `SPR_TI_FLOOR` takes over.  Above it,
                             # `bots/leap14_spr300` buys ~1 round of arrival for
                             # r100 collection of 55 against 180.  The batch
                             # reports the dose-response; the constant is not
                             # asserted, it is the knee of a measured curve.
SPR_TI_FLOOR = 60            # bank kept after paying for a rung.  A harvester
                             # is 20 base and a conveyor 3, so this is the first
                             # harvester plus a wire and change -- YIELD TO THE
                             # TRUNK, without the 220 war chest the trace shows
                             # the economy spending inside ten rounds anyway.
SPR_STOP_DSQ = CAGE_FERRY_STOP_DSQ   # 40.  Unchanged hand-off; see (2) above.
SPR_LOG = True               # `SPR rung n=K r=N` / `SPR arrive r=N s=K`


# ============================================================================
# WAVE 19, TRACK 1 -- THE TWO FIXES  (bots/loki_leap15)
# ============================================================================
# bots/loki_leap15 is bots/leap14_race (PLANK SPRINT) plus PLANK EARLYBIRD's
# DETECTOR AND GUN ONLY -- the neutral cut, EB_RG_HOLD_ON / EB_SH_ON /
# EB_PECK_ON all False -- with two defects of the parents repaired.  Nothing
# else moves; every other constant in this file is the parent's.
#
# ------------------------------------------------- FIX 1: THE ECO GATE ------
# WHAT WAVE 18 MEASURED.  The sprint bought its rungs out of the OPENING BANK
# and the trunk never recovered: `bots/leap14_race` finished 42 of 78 legs
# with ZERO titanium collected by r100 against the control's ~27, and median
# r100 titanium 99 against leap13_split's 146.  The rung gate was
# `ti >= cost + SPR_TI_FLOOR` with SPR_TI_FLOOR = 60 -- a BANK test, and a
# bank test cannot tell an opening war chest that is genuinely idle from a
# bank that is idle because the harvester it was meant to buy has not been
# built yet.  Both read 430.
#
# THE FIX IS TO CHANGE WHAT THE RUNG IS FUNDED FROM: not the bank, but
# REALIZED COLLECTION.  After the free opening (below), a rung is bought only
# once the meter has advanced SPR_COLLECT_STEP since the previous rung -- i.e.
# only once the trunk has actually delivered something.  A leg whose economy
# never starts therefore buys ONE rung and stops, which is exactly the leg the
# zero-collection column is counting.
#
# WHAT THE METER IS, AND WHAT IT IS NOT.  There is NO API for the engine's
# "titanium collected" tiebreaker statistic -- `get_global_resources()` is the
# only resource reader a unit has (docs 155/206) -- so the meter is the
# rider's own: the CUMULATIVE SUM OF POSITIVE BANK DELTAS between its own
# consecutive turns (`_spr_collect`).  Three properties, all of them wanted:
#   * it is MONOTONE, so it is a watermark and a rung can be priced against it;
#   * it UNDERCOUNTS, because a spend by another body between two of our turns
#     hides the income it was paid from.  The gate is therefore conservative --
#     it errs toward not buying a rung -- which is the correct direction for a
#     fix whose whole purpose is to stop this plank outbidding the trunk;
#   * it counts the 10 Ti / 4 rounds of PASSIVE income too (docs 145).  That is
#     deliberate and it is the floor of the gate: with a dead economy the meter
#     still creeps 2.5 a round, so SPR_COLLECT_STEP = 30 is "about twelve
#     rounds" of pure passive -- one further rung inside the window, not six.
#
# THE FREE OPENING.  Rung 1 is unconditional and so is every rung before
# SPR_FREE_RND, because the wave-18 trace is right about the opening: the bank
# holds 430+ at r2 and the economy has not yet found anything to spend it on.
# The defect was never the first rung, it was rungs three through six being
# bought at r7-r16 out of a bank the harvester shell needed.
#
# INERTNESS.  SPR_COLLECT_ON = False is bots/leap14_race's gate exactly, and
# the meter itself is then never even ticked.
#
# ACCEPTANCE, pre-registered: arrival stays <= r12 median on the pool while
# r100 titanium recovers to >= 140 mean and the zero-collection legs fall back
# to the control's ~27/78.  If arrival slips past r12 the gate is too tight and
# SPR_COLLECT_STEP is the dial.

SPR_COLLECT_ON = True        # master for FIX 1.  False == leap14_race.
SPR_COLLECT_STEP = 30        # realized collection required between rungs
SPR_FREE_RND = 6             # ...and the round before which rungs are free
SPR_COLLECT_LOG = True       # `SPR gate r=N c=C need=D` on a refusal.  It
                             # rides the `CG why` instrument rather than
                             # inventing a second stream.

# --------------------------------------------------- FIX 2: THE AIM ---------
# WHAT WAVE 18 MEASURED (tools/eb_probe2.py,
# results/wave18/eb_probe2_seed2.json).  The reactive ring gunner is NOT late
# and it is NOT unarmed: `RG up` lands at r4 on every leg, ammunition is >= 4
# from r2, and the gun stands for 52-443 rounds.  It simply never has anything
# on its ray -- ROUNDS WITH A TARGET 0, 0, 3, 8 ... of 500+.  The gun is
# scenery, and the reason is geometry plus a thrash guard written for a
# different weapon:
#
#   (i)  THE SITE WAS CHOSEN FOR ONE FACING.  `_rg_gun` scored (site, facing)
#        pairs jointly and kept the best pair.  A gunner is the ONLY turret
#        that can re-aim (docs 2287), so the thing worth maximizing at build
#        time is not the ray it starts with, it is the UNION of the rays it can
#        ever swing to.  FIX: score a site by how many WORK TILES its four
#        cardinal rays cover between them (`RG_COVER_UNION_ON`), and only then
#        pick the facing.  Coverage, not proximity to where the courier
#        happens to be standing on the build round -- that body moves.
#   (ii) THE RE-AIM COULD NOT CHASE.  `_idle_rotate` is a FORWARD TUBE's
#        discipline: an 8-round self-imposed cooldown (ROTATE_COOLDOWN_RNDS),
#        a sticky previous target, and -- the outright bug for this use -- it
#        computes ONE direction (`p.direction_to(tgt)`), tests it, tries the
#        nearest cardinal if that was diagonal, and gives up.  A courier
#        bricking our collar sits two tiles out on a bearing that is neither,
#        and the barrel never moves.  FIX: `_rg_chase`, for this gun only.  It
#        enumerates ALL EIGHT legal facings, keeps the ones whose ray actually
#        contains the body (`can_fire_from`), prefers a CARDINAL one, re-runs
#        the rule-9 fratricide test, and rotates.
#
# THE BRAKE IS TITANIUM AND IT IS SMALL.  A rotate is 10 Ti and a 1-round
# action cooldown (docs 164/251/2294), which is a shot foregone -- so a chase
# that misses costs twice.  RG_ROT_BUDGET = 40 is FOUR rotations for the whole
# game, on ONE gun, and there is no second gun (RG_MAX = 1, refuted territory).
# Worst case this plank spends 40 Ti and buys nothing.
#
# AND IT DOES NOT ROTATE AT A BODY IT CANNOT HIT.  The chase fires only when a
# facing whose ray CONTAINS the target exists; a courier standing where no ray
# reaches is left alone rather than chased with the barrel.  This is the
# explicit instruction in the brief and it is also the only thing that keeps
# the budget from evaporating in three rounds against a body walking a
# diagonal the post cannot cover.
#
# INERTNESS.  RG_CHASE_ON = False + RG_COVER_UNION_ON = False is
# bots/leap14_race's gun exactly.
#
# STANDING RISKS, pre-registered:
#   R1  A ROTATE IS A SHOT FORGONE.  If the courier moves the round we rotate,
#       we paid 10 Ti and skipped a round of fire.  Bounded at four.
#   R2  COVERAGE IS NOT PROXIMITY.  The union score can move the post one tile
#       further from the body that triggered it.  That is the intended trade
#       (the body moves, the ring does not) and `RG_COVER_UNION_ON` ablates it.
#   R3  FRATRICIDE, AGAIN.  Every chase facing gets `_rg_ray_safe`, which is
#       the same rule-9 test the build-time facing got and which fails closed.

RG_CHASE_ON = False          # LEAP16: KILLED AS NOISE, wave 18b.  The call
                             # site in main.py is removed as well, so this
                             # is a belt-and-braces head guard on a method
                             # nothing reaches.  The SITING half of FIX 2
                             # (RG_COVER_UNION_ON, below) is KEPT -- it is
                             # where the aim delta came from and it rides a
                             # scan that already runs.
RG_ROT_COST = 10             # what the engine charges for one rotate (docs
                             # 164/251/2294).  A constant, not a guess.
RG_ROT_BUDGET = 40           # titanium ONE gun may spend chasing, per game
RG_CHASE_TI_FLOOR = 10       # ...and the bank kept back beyond the 10 Ti
RG_CHASE_GAP = 2             # rounds between chase rotates.  The engine's own
                             # action cooldown is 1; this is one round of
                             # patience on top, so a body merely passing
                             # through cannot draw two rotations.
RG_CHASE_CARD_ONLY = False   # True = only cardinal facings may be chased to.
                             # Shipped False: a gunner's diagonal facing is
                             # legal (docs 272) and a courier on the diagonal
                             # adjacent tile is a real, cheap kill.
RG_CHASE_DSQ = GUNNER_RANGE_DSQ   # 13.  A body past this cannot be hit at all.
RG_COVER_UNION_ON = True     # site scored on the UNION of its cardinal rays
RG_COVER_DIRS_CARD = True    # ...and that union is over the four cardinals,
                             # which are the rays that reach three tiles out
RG_CHASE_LOG = True          # `RG chase D->D (x,y) r=N ti=T`


# ==========================================================================
# LOKI-LEAP16 -- PLANK KEYSTONE (KC).  THE KILL CONVERSION OF THE TEMPO EDGE.
# ==========================================================================
#
# THE PROBLEM, MEASURED BEFORE A LINE WAS WRITTEN.  Wave 18b shipped PLANK
# SPRINT and it does exactly what it claims.  Paired over 270 jython cells of
# the SAME run (tools/wave19_kcbatch.py): our first barrier on THEIR ring lands
# r11 against the control's r22 (194 cells earlier vs 41 later, sign p <
# 0.0001), and we hold MORE of their eight heal seats all game -- seal_max 5.0
# vs 4.5, seats held at r100 5.0 vs 4.0, p = 0.0002.  The cage is real, it is
# early, and it does NOT decay: the census RISES, 4.26 seats at r50 to 4.87 at
# r100 to 5.19 at r150 (tools/wave19_seatcensus.py, 270 games).
#
# AND IT KILLS NOTHING.  On the same 270 cells THEIR CORE SITS AT FULL 500 HP
# AT ROUND 150 IN THE MEDIAN GAME ON BOTH LEGS; the first scratch on it comes
# LATER for us than for the control (r245 vs r175); the games run 293 turns
# against 215.  We arrive eleven rounds earlier and take seventy rounds longer
# to draw blood.  That is wave 19 track 2 in two numbers.
#
# THREE HYPOTHESES WERE PUT UP AND TWO OF THEM WERE KILLED BY THE DECODE.
#   * SEAL DECAY -- REFUTED.  The seal climbs; it does not fall (above).
#   * THE AMMO PIPELINE -- REFUTED as the cause of the missing KILL.  Ammo sits
#     UNSPENT at 20-24 for hundreds of rounds in every caged game decoded.  The
#     sprint does halve realized collection (col_100 50 vs 100, p = 0.017) and
#     that is real, but it costs us the titanium TIEBREAK, not the core.
#   * A THIRD, MINE, ALSO KILLED, AND IT IS RECORDED BECAUSE IT WAS BUILT AND
#     MEASURED.  `CAGE_SEAL_TI_BUDGET` is 45 Ti for the whole match and
#     `_collar_heal` draws on the same purse as `build_barrier`, so an
#     exhausted purse makes `_collar_afford(ct, E, 1)` fail at the TOP of the
#     arm and the collar returns False for the rest of the match.  A seat
#     reserve that outlived the purse was implemented in full.  IT FIRED ONCE
#     IN TEN GAMES (`KC brick=1`, results/wave19_kc_pool.log): the purse is not
#     what is empty.  Reverted line for line.  The arithmetic that made it look
#     binding counted ALL forward builds as collar bricks; `COL brick` is 5.5 a
#     game, about 17 Ti of 45.
#
# WHAT IT ACTUALLY IS: REACH, NOT PAY.  `_collar` can only brick a ring tile
# CARDINALLY ADJACENT to the body.  Split the open-seat rounds on adjacency
# (tools/wave19_reach.py, 120 games, 36 367 forward-body rounds after r50):
#     an empty buildable seat somewhere on their ring   63.9 % of rounds
#     ... and one of them adjacent to one of our bodies  5.0 % of rounds
#                                                        (7.9 % of the above)
#     distinct seats our bodies are EVER adjacent to     median 3 of 8
# Five of their eight seats are never touched by anything of ours, all match.
# The cage is capped by where the bodies STAND, and no amount of titanium or
# tempo moves that.
#
# AND HERE IS WHY THEY STAND THERE.  `_collar_seats_by` scores a corner by the
# seats beside it that still need sealing, and it reads a seat as open when
# `get_tile_building_id` is None -- which is exactly what a seat under one of
# THEIR BUILDERS returns.  So a corner beside a seat their healer is sitting on
# keeps COLLAR_BRICK_BONUS for ever, and the body is PINNED there, polling a
# tile `can_build_barrier` refuses for as long as they choose to stand on it,
# while genuinely open seats elsewhere on the ring go unbricked.  The r100
# census is the fingerprint: 4.87 seats ours, 0.11 terrain, 1.10 simply EMPTY,
# and 1.92 under one of their bodies -- which is to say under the heal line,
# +4 HP per titanium per seat, which is why the core never moves.
#
# THE MECHANISM.  ONE THING, ONE PREDICATE, ONE LINE OF EFFECT: a seat under
# one of THEIR bodies is not an open seat.  It stops earning its corner the
# brick bonus, the body is released to a corner where a brick can actually be
# laid, and the reachable set stops being three of eight.  Nothing is
# abandoned -- the seat is rescored at the next rescan and the eviction arms
# are what take it back.  KC does not spend a titanium it was not already
# spending; it only stops paying a body to wait.
#
# WHAT COULD GO WRONG, PRE-REGISTERED.
#   R1  THRASH.  Their body steps onto a seat, we walk away, they keep it.  The
#       rescan cadence (LOKI_RAID_RESCAN) is the damper: the corner is rescored
#       only every few rounds, and a body that walks off a blocked corner walks
#       to one it can actually work.  WATCH: seats-held at r100 must not FALL.
#   R2  IT COULD UNSEAT A SQUAT.  `COLLAR_SQUAT_BONUS` and the seat stations are
#       untouched -- this predicate is only inside the CORNER arm of the score.
#   R3  IT DISCOUNTS A SEAT WE MIGHT HAVE WON ANYWAY when their body moves off
#       next round.  Accepted: the census says 1.9 such seats persist to r150,
#       so the modal blocked seat is a resident, not a passer-by.
# INERTNESS.  KC_ON = False restores leap15_kfix line for line: one flag, one
# `if`, and the predicate is never read.
KC_ON = True                 # master.  False == the incumbent corner scoring.
KC_LOG = True                # `KC free (x,y) b=N` -- a corner released because
                             # every remaining seat beside it is under one of
                             # theirs.  Deduplicated to one line per body per
                             # round; `_raid_station` asks four corners.


# ============================================================================
# WAVE 22, ARM A1 -- THE INTEGRATED OPENING  (bots/leap18_open, `opening.py`)
# ============================================================================
# The ticket is `analysis/wave22/PLAN.md` 2.1 and the design is
# `analysis/wave22/OPENING.md`.  ONE flag per arm, one arm per build, and an
# OFF twin (`bots/leap18_open_off`) that is a byte copy of this tree with
# OPEN_ON = False -- PLAN 1.2, "no exceptions, no 'we'll ablate later'".
#
# WHAT THIS ARM IS.  Not a mid-game plank: an OPENING.  It attacks the only
# finding wave 20 actually produced -- 99/270 jython games still pin at
# `titanium_collected = 0` -- by buying the two things that are cheap and
# early: SOCKET OCCUPANCY (2 builder-actions, 8 Ti, band-independent, caps the
# enemy seal at 6 by engine E3) and PURCHASING POWER (a 3-builder cap during
# the ferry, which is what pays for rungs 4-6 AND the counter-battery reserve
# at the same time -- OPENING.md 2.2: bank@10 is 230 under the cap and 95 with
# five builders, and band C with five builders is BANKRUPT at r11).
#
# WHAT IT IS NOT.  `A2_ECO` (the trunk-first band-A-2 counter-book) is NOT in
# this build.  It is a separately-flagged variant on n=3 evidence from two
# teams that lose 40 %/32 % overall, and collapsing it into the O(1) book here
# would confound the A/B that OPENING.md 1.4 and PLAN W6 pre-registered.
# `CB_READY_ON` (arm A3) is not here either -- this arm only HOLDS the reserve
# the cap lift is gated on; it never spends it.
#
# ROTATION SAFETY (OPENING.md 9).  Every number below is a mechanism constant.
# The band is computed by BFS at r0 and the ore gate is computed from the
# decoded ore layout, so nothing here is keyed on a map name and nothing here
# is a cached per-map table.
OPEN_ON = True               # MASTER.  False == bots/loki_leap16 exactly:
                             # every hook in main/eco/raid falls through to the
                             # parent's code and nothing prints.
OPEN_LOG = False              # measurement scaffolding: `OP band=`,
                             # `OP prefill`, `OP capliftr=`, `OP feeder`,
                             # `OP pair`.  MUST be False in any ship build
                             # (PLAN 1.5: "no logging flags in any build that
                             # reaches a verdict cell").

# --- the band variable (OPENING.md 1.1-1.3) --------------------------------
# need_eff = max(1, ceil((pathlen - 4.5) / 5.66)), in hundredths so the whole
# computation is integer.  5.66 is the measured maximum ferry hop (d^2 = 32);
# 4.5 is the arrival envelope.  `pathlen` is a BFS WALK distance ring-to-ring,
# which is what moves yulerune into band B (a wall belt sits on the core-to-
# core line) and is the falsifiable prediction F7.3.
OPEN_HOP_NUM = 566
OPEN_ENV_NUM = 450
OPEN_BAND_C_NEED = 5         # need_eff >= 5 is band C.  The A/B boundary sits
                             # at need_eff >= 3 (bands A1/A2 are need 1/2),
                             # because both evidence tables flip between c2c 14
                             # and 16 == need 2 -> 3.

# --- SOCKET-PREFILL (OPENING.md 2.3, 2.4, 4.3) -----------------------------
PREFILL_N = 2                # EXACTLY two, on >= 2 different core FACES.  Do
                             # not chase a third: own=2 -> 54.5 % (n=55) vs
                             # own=3+ -> 52.6 % (n=19), and four filled sockets
                             # inverts the heal arithmetic to 16 HP/rd against
                             # an 18 dmg/rd twin battery.
PREFILL_RND = 3              # the bar: "= 2 @r10 on >= 2 faces", occupied by
                             # r3.  Band-INDEPENDENT (OPENING.md 6.2).
PREFILL_FEED_MAX_L = 3       # THE ORE GATE.  `L` = walk distance socket ->
                             # nearest ore = the number of conveyors the line
                             # needs.  At L <= 3 both sockets become feeders on
                             # schedule; above it the second socket is a PLUG
                             # -- a 3-Ti conveyor that is already the terminus
                             # of the trunk that arrives later.  A plug is
                             # never wasted: it buys the seal ceiling
                             # immediately (E3) and it is the correct first
                             # tile of the eventual line.
PREFILL_FEED_MAX_L1 = 5      # ...and line 1 (the socket nearest the ore) is
                             # still laid at L = 4-5, which is the
                             # "1 feeder + 1 plug" row of OPENING.md 2.4.
OPEN_PREFILL_WALK_RND = 10   # after this a body that never reached its socket
                             # stops trying and goes back to the economy.
OPEN_TRUNK_ON = True         # core-outward feeder construction: socket, then
                             # trunk, then HARVESTER LAST.  Jython's own book
                             # is ore-inward, which buffers exactly one stack
                             # and loses the rest (engine A) and leaves the
                             # socket empty until r8.
OPEN_STATION_ON = False      # THE WALK-BACK-AND-HOLD half of rule 4, and it
                             # is OFF BY DEFAULT ON A MEASUREMENT, not on
                             # taste.  OPENING.md 3's band-B schedule has E1
                             # and E2 station on their sockets at r7/r8 and
                             # do nothing after, which is coherent for a
                             # carrier whose economy is finished by r7; ours
                             # is not.  Measured, seed 301, side A, one game
                             # per cell, this build with the flag ON vs OFF:
                             #   midgard  590 -> 1330 titanium collected
                             #   royale   420 -> 1560, and the game flips L->W
                             # with the ON leg's economy pinned at 2
                             # harvesters and 4 conveyors from r10 to r120.
                             # That is F6.3's failure mode ("the cap starved
                             # the economy") produced by our own hand, so the
                             # arm does not ship it.
                             #
                             # WHAT STILL SHIPS, unconditionally under OPEN_ON,
                             # is the half of rules 3/4 that is a CONSTRAINT
                             # rather than an errand: no body may hold an EMPTY
                             # prefill socket (`_free_seats`, `_sh_pick_seat`
                             # -- the wave-20 M3 self-seal, 106-233 own
                             # body-turns per zero-collection game), and the
                             # base's own SEATHOLD stationing is steered onto
                             # FILLED sockets, which is where the 772 measured
                             # own-conveyor core heals come from.  Diagonals
                             # were never candidates: 0 of 2332 heals came from
                             # one.  Flip this True to A/B the errand.
OPEN_STATION_RND = 7         # ...from the round the schedule stations them.

# --- the cap and the lift (OPENING.md 2.1, 2.2, 2.5) -----------------------
OPEN_CAP = 3                 # builders while the ferry is live.
OPEN_CAP_BAND_A = 4          # band A runs two eco bodies and two turret
                             # riders instead (OPENING.md 5.2).
OPEN_LIFT_MIN = 6            # the earliest the cap may lift, in any band.
                             # Band A has no ferry to wait for, but the cap is
                             # what funds the turret pair inside the r5-r7
                             # window, and OPENING.md 2.5 prices the band-A
                             # lift at r6 anyway.
CB_RESERVE_EXTRA = 30        # CB_RESERVE = 2 * gunner cost + 30 (~100-110).
                             # HELD, never spent by this arm: the cap lift is
                             # gated on `bank - CB_RESERVE >= builder cost` so
                             # a lifted population can never eat the reserve
                             # arm A3 is measured against.

# --- the rung budget (OPENING.md 2.3, engine E4) ---------------------------
OPEN_RUNG_UNCOND = True      # exactly `need_eff` rungs, UNCONDITIONAL: inside
                             # that budget the sprint's total-spend cap, its
                             # per-rung bank floor and the wave-19 collection
                             # gate are all bypassed.  The price is flat
                             # `floor(20*scale)` because `destroy` is free and
                             # removes the launcher's +10 % the same round
                             # (engine K) and the rungs already self-destruct
                             # (CAGE_FERRY_DISPOSABLE) -- the measured
                             # 28/38/44/50/56/62 escalation was our own five
                             # opening builders at +20 % of scale EACH, which
                             # is exactly what the 3-builder cap removes.

OPEN_RUNG_WAIT = 2           # rounds between rungs.  A launcher built on round
                             # R first acts on R+1 and throws then, and the
                             # rider's own R+1 turn comes BEFORE it (creation
                             # order, engine H), so R+2 is the earliest the
                             # rider can be forward and buy the next rung.  The
                             # parent's CAGE_FERRY_WAIT = 3 is one wasted round
                             # per rung -- six rounds of arrival on a need-6
                             # map, which is most of the measured residual.

# --- band A's payload switch (OPENING.md 1.4, 5.1, 5.2) --------------------
A2_TURRET = True             # DEFAULT.  The same ladder mechanism carrying a
                             # TURRET payload instead of a barrier.  Turrets
                             # are the only unit that can damage a builder, so
                             # a live pair before their ferry lands is a
                             # MECHANISTIC counter to the whole cage doctrine.
A2_ECO = False               # the trunk-first alternative.  NOT IMPLEMENTED IN
                             # THIS BUILD -- it is `bots/leap18_a2eco`, its own
                             # arm, its own A/B (PLAN W6 / F7.4).  Never
                             # collapse the two.
OPEN_PAIR_N = 2              # two sentinels, arbitrated with ZERO COMM: the
                             # two lowest raid slots, each with a per-unit
                             # one-shot latch.  fixtures.md 2 measured THREE
                             # pair sentinels the one time a buffered store
                             # counter was trusted for this.
OPEN_PAIR_EARLIEST = 5
OPEN_PAIR_DEADLINE = 7       # r5-r7.  Before the deadline the facing must put
                             # a Core tile on the fixed 5-tile ray; AT the
                             # deadline the body builds wherever it stands,
                             # own ring included -- which is the honest rule,
                             # because O(1)'s "forward pair" is opportunistic
                             # transport on Jython's launchers and on a map
                             # where nothing carries you it IS the own ring
                             # (OPENING.md 5.1).
OPEN_PAIR_MAX_DSQ = 36       # d(enemy core) <= 6 before the deadline (F7.2).
OPEN_PAIR_TI_FLOOR = 8       # bank left after paying for one.
OPEN_A_CAGE_RND = 30         # band A does not build the barrier cage before
                             # this: `rb30 <= 2` is bar F7.1 and the band-A
                             # counter-book is a turret pair, not a seal.


# ======================================================================
# WAVE 22, TRACK 3 -- PLANK RING (RING-CLAIM + EVICT-AND-REPLACE).
# Master flag `RING_ON`.  One arm, one flag, one OFF twin
# (`bots/leap18_ring_off`), per PLAN.md 1.2 attribution rule.
#
# THE MEASUREMENT THIS ANSWERS (analysis/wave22/0033_losses.md 1.1-1.2):
# RING-SEAT FORFEITURE.  We leave a median 3.8 of our 8 core sockets EMPTY
# every turn and park a builder BODY on ~1.6 more (260 body-turns/game);
# 0033 leaves 0.3 empty and plants 4.67 barriers + 1.33 gunners a game
# inside 2.5 tiles of our core.  Median 5 of our 8 sockets end the game
# carrying an enemy building and WE CLEAR 3 OF 65 (4.6 %); 0033 clears
# 34 % of the bricks on its own ring.
#
# WHY CONVEYORS AND ONLY CONVEYORS (analysis/wave22/OPENING.md 4, X2):
# passable tiles are EMPTY, ORE and conveyors/splitters of either team
# (engine G); a body standing on a conveyor does not block the stacks
# moving under it (N.10); heal is strictly d^2 == 1 (N.9).  So a socket
# carrying OUR OWN CONVEYOR is simultaneously a delivery terminus, a tile
# the enemy can never brick (E3: a tile holding a building cannot be built
# on) and a LIVE HEAL SEAT -- 772 of the corpus's 2 332 own-socket core
# heals were launched from a body standing on its own conveyor, and 0 from
# a body standing on its own barrier/harvester/turret, because those three
# are impassable.  This plank therefore NEVER lays a barrier, a harvester
# or a turret on one of our own eight sockets.
#
# NO NEW COMM SLOT (PLAN.md 1.5).  All 16 are assigned.  The eviction cap
# is settled by an id ballot among the bodies that can SEE the target, the
# claim ledger is CENSUSED off the buildings that are standing (a census
# cannot go stale the way a buffered counter can), and the refill intent
# lives on the unit that pecked, not in the store.
# ======================================================================
RING_ON = True               # MASTER.  False == bots/loki_leap16 exactly:
                             # every method below returns in its first test.
RING_LOG = False              # `RING claim/evict/refill` markers.  Measurement
                             # scaffolding; False in any verdict cell.

# --- ARM 1: RING-CLAIM -------------------------------------------------
# Reactive first, with a small unconditional floor behind it.  The A1 cap of
# "exactly 2 own sockets" rests on own=2 -> 54.5 % (n=55) vs own=3+ ->
# 52.6 % (n=19), and 0033_losses.md 3.1 records why that comparison cannot
# speak here: it comes from cells where the ring is NOT contested (the
# offline enemy brick rate is 0.06/game), and the contested case is the only
# one that lost.  So the cap lifts only when the ring is measurably under
# attack, and the unconditional part stays inside the registered band.
RING_TRIGGER_ON = True
RING_NEAR_DSQ = 16           # "any enemy BUILDING within 4.0 of our core" --
                             # 0033's barriers sit at median d = 2.53 and its
                             # first lands r7.  Measured to the FOOTPRINT.
RING_FWD_ON = True           # ...or any enemy NON-BUILDER entity forward of
                             # the midline, i.e. strictly nearer our core than
                             # theirs.  128 of their 138 turret placements are
                             # past the midline, so this is the same warning
                             # one to twenty rounds earlier.
RING_TRIG_MEM = 60           # rounds a sighting keeps the claim armed (the
                             # detector's own ARCH_MEMORY, so the two agree).
RING_TEAM_SIGNAL_ON = True   # fall back to the S1 stamp (enemy TURRET near
                             # our core, slot 13 bits 0-9) so a body that has
                             # seen nothing itself still gets the team's eyes.
                             # S3 (enemy BUILDER) is deliberately NOT used:
                             # the trigger is about non-builder presence.
RING_FLOOR_OWN = 2           # THE UNTRIGGERED CEILING, and it is ABSOLUTE:
                             # top our ring up to this many own buildings and
                             # stop.  "Up to 2 beyond the prefill count" reads
                             # as 2 on this base, because `bots/loki_leap16`
                             # has no prefill plank -- its measured ring is
                             # 0.5 own buildings at r20 -- and 2 is exactly the
                             # band A1 registered ("= 2 @r10 on >= 2 faces").
                             # ABSOLUTE and not "feed + 2" for a measured
                             # reason: `_sg_socket_scan` calls any own conveyor
                             # that outputs into a core tile a FEEDER, and a
                             # claim IS such a conveyor -- so a relative floor
                             # RATCHETS, one socket per claim, straight to 8.
                             # The screen caught it: 182 of 230 claims in a
                             # 32-game run came from the UNtriggered path.
RING_FLOOR_RND = 20          # ...and only up to this round.  Keeps the
                             # untriggered build inside A1's registered band
                             # (own = 2 @ r10 on >= 2 faces) while the
                             # contested case above lifts it.
RING_FLOOR_MIN_RND = 6       # never before this: r1-r5 is the harvester
                             # bootstrap and 3 Ti there is the whole economy.
RING_MAX_OWN = 8             # hard ceiling on own buildings on own sockets.
RING_MAX_PER_UNIT = 3        # claims a single body will ever lay.  Bounds the
                             # re-lay loop when a claim is shot out.
RING_TI_FLOOR = 30           # never take the bank below this for a claim --
                             # about one harvester, so a claim can never be
                             # the reason the next harvester is late.  Was 12
                             # (SG_FILL_TI_FLOOR's number, for a 3 Ti brick in
                             # a 2-brick window); this arm can want the whole
                             # ring, so it needs the bigger reserve.
RING_ECO_GATE_ON = True      # the shell gate applies to the EVICT and to
                             # both WALKS as well as to the claim ceiling.
                             # Only the REFILL is exempt, and only because it
                             # cannot fire unless an evict already did.
RING_ECO_HARV = 2            # THE SHELL GATE.  The ring only opens past the
                             # floor once this many harvesters exist -- the
                             # base's own `SH_ECO_HARV`, for the same reason
                             # SEATHOLD carries it.  MEASURED without it: at
                             # r30 the arm had laid 8 socket conveyors and 2
                             # trunk links, held ONE harvester against the
                             # control's two, and had collected 0 titanium
                             # against the control's 40.  0033 does plug 8
                             # sockets by r10 -- and it also runs 8 harvesters
                             # and 59 conveyors; the plugs are paid for by an
                             # economy, they are not a substitute for one.
RING_CHAIN_GUARD = True      # a body carrying a trunk chain NEVER claims: an
                             # abandoned chain is a dead end that delivers
                             # nothing at all (eco `_wire_tick`), which is the
                             # measured way this kind of plank starves a trunk.
RING_KEEP_FREE = 0           # sockets deliberately left open.  0 because a
                             # socket carrying our own conveyor IS still a
                             # heal seat and still passable (X2) -- the reason
                             # SG_FILL_FREE_MIN was 1 is that SG_SELF_FILL
                             # lays BARRIERS, which are none of those things.
RING_WALK_ON = True          # the bounded move half...
RING_WALK_BAND_DSQ = 64      # ...only a body already within 8 tiles of home...
RING_WALK_RNDS = 8           # ...for at most this many rounds per target...
RING_WALK_CAP = 24           # ...and this many rounds in its whole life.
                             # The three bounds SG_REBUILD_WALK carries, for
                             # the reason it carries them: recalling the
                             # economy on a latch once finished a measured
                             # game with 0 titanium delivered.

# --- ARM 2: EVICT-AND-REPLACE ------------------------------------------
# CLEAR + RETAKE, never clear alone.  The 5-round window truth: a socket
# cleared and not refilled the same round is re-bricked.  So the peck is
# REFUSED unless the refill is funded, and the refill outranks everything.
RING_EVICT_ON = True
RING_EVICT_BODIES = 2        # bodies that may peck one brick at once, settled
                             # by an id ballot among the bodies adjacent to it.
RING_EVICT_TI_FLOOR = 2      # titanium kept back from the 2 Ti peck (SH's).
# THE PECK BUDGET, and it is the hardest bound in this file.  A builder peck
# is 2 damage and 2 Ti, so a 30 HP barrier is 15 pecks and 30 Ti.  MEASURED
# on the first RING screen, before these two constants existed: with no
# budget at all the arm spent 1 449 pecks in one 1000-round drakkarfjord game
# -- ~2 900 Ti of ammunition -- against a ring the opponent simply re-bricked,
# and converted 11 of them into a refill.  The whole forensic budget it is
# supposed to be re-spending is 974 building attacks + 907 turret attacks over
# FIFTEEN ladder games (~125 a game).  So: one body gives up on one tile after
# `RING_EVICT_TRY_RNDS`, and gives up on the arm entirely after
# `RING_EVICT_LIFE` pecks -- 2 barriers' worth, which at six bodies is ~12
# clearable bricks a game against a measured median of 5 on our ring.
RING_EVICT_TRY_RNDS = 20     # rounds one body spends on ONE socket tile
RING_EVICT_LIFE = 30         # lifetime pecks this arm may spend, per body
RING_REFILL_RNDS = 5         # rounds a body keeps its refill intent alive
                             # after its target died.  The window, verbatim.
RING_EVICT_WALK_ON = True    # same three bounds as the claim walk, shared
                             # budget (`ring_walk_total`).

# --- ARM 3: THE BODY BAN -----------------------------------------------
# 260 body-turns a game on our own sockets, ~1.6 sockets held by a BODY at
# any moment.  A body on a FILLED socket is free (the tile is already
# unspawnable and unbrickable, and it heals); a body on an EMPTY socket is
# the wave-20 M3 self-seal -- it blocks our own claim and our own feeder.
RING_BODY_BAN_ON = True      # SEATHOLD stations on FILLED sockets only...
RING_BODY_BAN_SOFT = True    # ...unless no filled socket is available at all,
                             # in which case the parent's choice stands.  The
                             # ban must never leave the bot with no station:
                             # that would hand 0033 the seat FASTER, which is
                             # exactly what 0033_losses.md 3.1(3) warns about.

# ======================================================================
# WAVE 22, ARM A2 -- GUN DISCIPLINE  (analysis/wave22/PLAN.md sec 2.2)
# ======================================================================
#
# TWO OWN-CODE DEFECTS, NINE NAMED INSTANCES, AND NOTHING ELSE.
#
# `analysis/wave22/evidence_fixes.md` sec 0, measured with the committed
# scanner over our 15 ranked v161 games (2 600 gunner-rounds):
#
#     FIRED           5.1 %   (Jython 38.2 %)
#     emptyRay       57.6 %   (Jython  9.5 %)
#     ownInRay       35.3 %   (Jython 35.1 %) -- corrected; the published
#                             38.8 % came from a scanner that treated the
#                             core as 3x3.  OUR core is 2x2, and every
#                             occupancy test below reads the ENGINE's tile
#                             map rather than guessing a footprint, so the
#                             3x3 bug cannot recur here.
#     foeInRay-held   1.0 %
#     silent gunners  9 of 21 = 43 %   (Jython 0 of 90)
#
# 57.6 % + 35.3 % = 92.9 % of our gunner-rounds have the barrel pointed at
# nothing or at our own wall.  That is an AIMING problem, not a supply
# problem -- ammoDry is not what is missing.  Two arms:
#
#   GD_SILENT_OFF  NO SILENT GUN.  Refuse to place a gunner unless an enemy
#                  entity is ALREADY inside the ray of the intended
#                  tile+facing.  A gunner that is worth 20-30 Ti plus +20 %
#                  on every later build is worth it because it shoots; a
#                  post bought against a body that has not arrived is a
#                  prediction, and the census says we lose that bet 43 % of
#                  the time outright.  Second half: `destroy` is FREE, is
#                  uncapped, and does not consume the action or the move
#                  (engine_mechanics sec K), so a gunner that has fired ZERO
#                  shots in GD_SILENT_RNDS rounds with no enemy in vision is
#                  scrapped -- which also hands back its +20 % scale
#                  contribution for the rest of the match.
#
#   GD_LANE        CLEAR LANE.  Reject any tile+facing whose NEAREST ray
#                  occupant is one of our own structures -- a gunner
#                  resolves to the nearest occupant and does not care whose
#                  it is (sec D: our own gunner destroyed our own barriers,
#                  and killed our own builder in six shots).  Re-aim
#                  (rotate, 10 Ti) when a LATER build plugs a lane that was
#                  clean when the gun went up: that is the 35.3 % column,
#                  and the incumbent `_idle_rotate` cannot fix it, because
#                  with nothing hostile in sight the reactive ring gun
#                  deliberately HOLDS its facing (main.py, PLANK RG) and the
#                  barrel stays welded to our own conveyor.
#
# WHAT IS NOT HERE, DELIBERATELY.  `GD_TRIGGER` / TRIGGER-AUDIT is excluded
# on CRITIC X1 and PLAN.md sec 2.2: the 15.6 % "declined shot" is PLANK CAGE
# arm 3 + PLANK PAIRS arm 2 holding core fire until the cage is up, which is
# the same behaviour that measures 92 % win at seal 7-9 before first core
# damage against 45 % at 0.  The sentinel hold-fire path is NOT TOUCHED by
# this arm.
#
# ZERO COMM.  All 16 store slots are assigned in the base.  Every decision
# below is taken from what the acting unit can see this round plus that
# unit's own instance state; nothing is written to and nothing new is read
# from the store, so the buffered-store race (engine_mechanics sec J) cannot
# reach this arm.
#
# GUARD, per PLAN.md sec 3.4 G-G: gunners built per game <= 1.75 (control
# 1.40, NOT the 3.3 in action_economy.md sec 2.2 -- that column counts
# `place_entity` events, i.e. builds PLUS re-aims, evidence_fixes.md sec 2).
# Both arms of this plank push the build count DOWN, never up, so the guard
# can only be breached by the re-aim budget below -- which is why it is
# capped rather than free.
#
# INERTNESS.  GD_ON = False restores loki_leap16 line for line: one flag,
# read once per gate, and no scan runs.  `bots/leap18_gd_off` is the
# byte-copy with the flag down.
GD_ON = True                 # master.  False == bots/loki_leap16 exactly.
GD_LOG = False                # measurement scaffolding.  `GD veto`, `GD scrap`,
                             # `GD reaim`.  OFF in any ship build (PLAN sec 1.5:
                             # no logging flag in a build that reaches a verdict
                             # cell) -- ON here because 22B stage 1 is
                             # attribution, not a verdict.
GD_SILENT_OFF = True         # arm 1: NO SILENT GUN (placement veto + scrap)
GD_LANE = True               # arm 2: CLEAR LANE (placement veto + re-aim)

GD_SILENT_RNDS = 25          # N.  Rounds of life with ZERO shots and nothing
                             # hostile in vision before a gunner is scrapped.
                             # Not tuned on an outcome: it is the shortest
                             # window that cannot fire on the measured signal
                             # itself.  Gunner id 136 (`1eea783c` g3) was
                             # re-aimed at t56/63/73/88 and never fired -- a
                             # 32-round span between the first and last re-aim
                             # of a gun that was already dead weight; 25 is
                             # under that and over the 14-round median CB
                             # response latency, so a gun bought against a real
                             # besieger is never scrapped before the besieger
                             # can walk into its ray.
GD_REAIM_MAX = 2             # rotations per gunner LIFE that CLEAR LANE may
                             # buy.  We already emit 2.4 place_entity events
                             # per gunner against Pivot's 1.3 (evidence_fixes
                             # sec 2): this arm is here to stop the barrel
                             # pointing at our own wall, not to add churn.
GD_REAIM_MIN_GAP = 6         # rounds between CLEAR LANE rotations.  A rotate
                             # sets action_cooldown = 1, so back-to-back
                             # re-aims cost fire rounds as well as 10 Ti.
GD_REAIM_TI_FLOOR = 40       # bank kept clear of the 10 Ti rotate.  A turret
                             # serves an economy; it does not outbid one.


# ===========================================================================
# WAVE 22 -- ARM A4: THE OFFENSIVE SIPHON TAP  (analysis/wave22/siphon.md)
# ===========================================================================
# ONE FLAG, ONE ARM, ONE CELL.  `SIPHON_ON` is the master and it is the only
# behavioural switch this arm owns; `bots/leap18_sip_off` is this directory
# byte-for-byte with the master False, and that twin is the inertness leg.
#
# WHAT IT DOES.  A single CONVEYOR, cardinally adjacent to an ENEMY harvester,
# FACING AWAY from it onto the next tile of our own trunk, then a head-first
# chain home.  The harvester round-robins its output over its cardinal
# acceptors TEAM-BLIND (engine_mechanics.md N.1, measured 100/50/33/25 % as
# taps are added), so one 3-Ti tile takes 1/(n+1) of that harvester for the
# rest of the game and denies the victim the same amount -- a 2x swing off one
# building.  Corpus: 112 stubs / 911 stacks / 9 110 Ti over 150 games, median
# service life 110 rounds, 83 of 112 still standing at game end.
#
# WHY THERE IS NO CUT-VERTEX GATE HERE, ON THE RECORD.  The tap attacks the
# SOURCE, so its yield is 1/(n+1) of that harvester whatever the downstream
# topology is -- it is immune by construction to the `202a0ef6_g2` failure
# where Jython spent ~7 000 Ti of ammo killing one redundant conveyor 139
# times for zero effect (siphon.md 3.1).  The gate belongs on trunk-cut
# DENIAL, and siphon.md 3.2's condition G3 (our price to keep a tile dead <=
# their price to rebuild it) is FALSE for every ammo-based attack on a
# rebuildable 3-Ti conveyor, so the gate's honest output for denial is "do not
# do it".  This arm therefore builds NO edge-cut denial and runs NO cut-value
# scan: the CPU cost of the plank is the target scan and nothing else.
# `SIPHON_CUT_SHARE` is declared below for namespace completeness and is
# READ BY NOTHING.
#
# NAMESPACE WARNING.  `SIPHON_DENY_ON` / `SIPHON_WIRE_ON` above (lines ~860-929)
# are the DEFENSIVE half, shipped since v75, and mean something else entirely.
# This arm does not reuse either name and does not re-open either behaviour.
#
# TEMPO PURITY (falsifier F-S1.3, HARD FAIL).  Not one tap conveyor before
# `arrival`, and never by the rider or by E1/E2 -- the two bodies that station
# on filled sockets are the heal wall (2 bodies = 8 HP/round = a 50-round kill
# window against a twin battery; 1 body = 36 rounds), and trading 14 rounds of
# core life for 1.25 Ti/round is a bad deal at every cost scale.  In this
# carrier that is: role == "raid", seat NOT in SIP_EXCLUDE_SEATS, i.e. the
# post-cap-lift bodies (#4/#5) and the defected late-raid seat, never seat 0.
#
# COMM.  All 16 slots are assigned in the base.  This arm is ZERO-COMM: it
# carries its role on the unit and arbitrates by LOWEST LIVE BUILDER ID among
# builders that can see the target harvester (builder vision r^2 = 20, so a
# rival claimant is necessarily within ~4.5 tiles and the rule resolves
# locally).  No slot is read and no slot is written.
SIPHON_ON            = True    # master flag for the OFFENSIVE arm
SIPHON_LOG           = False    # 'SIP tap' / 'SIP yield' markers.  MEASUREMENT
                               # SCAFFOLDING -- False in any ship build.
SIPHON_MAX_CHAIN     = 14      # tiles we must BUILD, tap included, from the tap
                               # to our nearest core-reaching node.  Fitted to
                               # chain ~= 1.8 x c2c on the pre-rotation pool;
                               # re-fit after the Aug-20 rotation.
SIPHON_MAX_N         = 2       # skip a harvester that already carries > 2
                               # acceptors (our share would be <= 25 %)
SIPHON_MIN_ROUND     = 0       # 0 == "arrival" (derived per map by BFS below);
                               # a positive value is an ADDITIONAL floor
SIPHON_BAND_MAX_NEED = 4       # never fire at need_eff >= 5 (band C measured
                               # 0.03 taps/game, 0 in 20 ragnarok+drakkarfjord)
SIPHON_RETAP_WINDOW  = 60      # two kills of the same tile inside this window
                               # -> ban the tile (abort A2)
SIPHON_BAN_RNDS_TAP  = 200     # how long a banned tap tile stays banned.  NOTE
                               # the distinct name: SIPHON_BAN_RNDS above is the
                               # DEFENSIVE half's and is not touched.
SIPHON_STALL_RNDS    = 12      # chain not extended this long -> release the
                               # role so the next-lowest id may adopt it (A6)
SIPHON_GATE_EVERY    = 8       # rounds between target scans, offset by unit id
SIPHON_CUT_SHARE     = 0.50    # DECLARED, UNUSED.  See the note above: this arm
                               # runs no cut-value gate at all.
SIPHON_COLLAR_ON     = False   # A4b, PARKED (PLAN 2.4): no fixture taps us, and
                               # our measured loss is already 0.63 %.  Not
                               # implemented in this build.
SIP_EXCLUDE_SEATS    = (0, 1, 2, 4)   # rider, E1, E2, home defender
SIP_HARV_DSQ         = 20      # only consider a harvester this close, so its
                               # four cardinal neighbours are inside vision
                               # (r^2 = 20) and `n` can be counted honestly
SIP_MAX_CAND         = 4       # candidate tap tiles considered per harvester,
                               # ranked nearest-home first.  Measured at 2 the
                               # arm fired in 3 of 12 band-A/B smoke games,
                               # below F-S1.8's 0.5 floor, because the two
                               # nearest-home faces routed at k=17/19 while a
                               # k=13 face on the same harvester was never
                               # looked at.
SIP_MAX_HARV         = 3       # harvesters considered per scan, nearest first
SIP_ROUTE_BUDGET     = 3       # HARD CAP on `_link_path` floods per scan, across
                               # all harvesters and faces.  This, not the two
                               # counts above, is what bounds the plank's CPU:
                               # F-S1.9 (exec_us p95 on the tapper <= 3x control)
                               # is measured on the server and cannot be checked
                               # here (`get_cpu_time_elapsed` returns 0 on this
                               # Windows build, engine_mechanics.md I).
SIP_ONSITE_EVERY     = 2       # scan cadence while standing on an ore site.
                               # Every round was cheap when a scan was two
                               # floods and is not when it is three; the walking
                               # cadence stays SIPHON_GATE_EVERY.
SIP_CAND_SLACK       = 12      # free pre-filter: BFS length >= Manhattan, so a
                               # face more than SIPHON_MAX_CHAIN + this from our
                               # core cannot route inside the chain cap.  The
                               # slack exists because the chain may terminate on
                               # our own trunk rather than at the core ring.
SIP_MAX_TAPS         = 2       # chains one body may start in a match
SIP_CLAIM_MAX_RNDS   = 80      # hard lifetime on one chain claim.  A6 is
                               # refreshed by the A4 money pause on purpose
                               # (pausing for money is not being evicted),
                               # so without this a permanently broke body
                               # could hold the role for the whole match.
SIP_CORE_HP_HOME     = 300     # abort A5: our core below this -> go home
SIP_ABORT_A1_N       = 3       # abort A1: victim's OWN acceptors reach this and
                               # our share is <= 25 % -> stop extending
SIP_ARRIVAL_A        = 6       # arrival floor, band A (need_eff <= 2)
SIP_ARRIVAL_B        = 10      # arrival floor, band B (need_eff 3-4)
SIP_ARRIVAL_C        = 12      # arrival floor, band C -- recorded only; the
                               # band gate refuses band C outright
SIP_PROSPECT_ON      = True    # the carrier WALKS to the enemy ore field to
                               # look for a harvester.  siphon.md 4.1 assumes a
                               # carrier that already passes enemy harvesters
                               # (sporks' forward trunks run along them); in
                               # THIS carrier the forward bodies sit on the
                               # enemy core ring, `get_nearby_buildings` is
                               # bounded by builder vision r^2 = 20, and a
                               # measured smoke game found an enemy harvester
                               # in vision of an eligible body ZERO times.
                               # Without this the arm's denominator is zero and
                               # F-S1.8 fires on an unmeasurable plank.  Own
                               # sub-flag so the diversion is ablatable.
SIP_PROSPECT_RNDS    = 80      # total prospecting budget per body, walk + look.
                               # Spent once; a body that gives up never
                               # prospects again and reverts to raid work.
SIP_PROSPECT_HOLD    = 8       # rounds standing on one ore site with nothing
                               # legal in sight before moving to the next one.
                               # Standing still is the worst use of the budget:
                               # their harvesters are somewhere in the field,
                               # not necessarily on its nearest tile.
SIP_PROSPECT_SITES   = 4       # distinct ore sites tried per body, >= 3 tiles
                               # apart so the cursor cannot crawl across one
                               # patch a tile at a time
SIP_RESERVE_ON       = False   # honour A3's CB_RESERVE.  DEFAULTS OFF, and the
                               # reason is a MEASURED FINDING, not a preference:
                               # with it True the arm fires ZERO times.  On
                               # antler vs mimic_jython2 the tapper stood beside
                               # a legal n=1 harvester with a k=4 route for 40
                               # consecutive rounds while `bank - CB_RESERVE`
                               # read -160 to -59 -- our bank ran 2-95 Ti and
                               # `2 x gunner + 30` was 154-162 Ti at those cost
                               # scales.  `OPENING.md` 7's reserve is LARGER
                               # THAN OUR WHOLE BANK on this carrier, so any
                               # plank funded from `bank - CB_RESERVE` is inert
                               # by arithmetic and F-S1.8 fires on a plank that
                               # was never tried.  A3 is not in this build, so
                               # the reserve here protects nothing.  Flip it
                               # True in the stage-3 integration build (where A3
                               # exists) and this becomes the honest test of
                               # whether the two arms can be afforded together.
                               # FLAGGED FOR THE TEAM LEAD: the same arithmetic
                               # applies to A3's own funding rule.
                               #
                               # loki_leap18 INTEGRATION RULING: the sentence
                               # above -- "flip it True in the stage-3
                               # integration build (where A3 exists)" -- is
                               # VOID, and this build is that stage-3 build.
                               # A3 was KILLED (PLAN.md AMENDMENT 2026-08-18
                               # A1, results/wave22/cb_verdict.md: -7.8 pp on
                               # mimic_jython2 over 1080 games).  A3 does NOT
                               # exist here, so there is nothing for the tap
                               # to be junior to, and flipping this True would
                               # hold 154-162 Ti against a measured 2-95 Ti
                               # bank -- making A4 inert by arithmetic and
                               # firing F-S1.8 on a plank that was never
                               # tried.  IT STAYS False.  This is the second
                               # of the two dangling CB_RESERVE references the
                               # amendment ordered resolved; the first was
                               # `_op_reserve` in opening.py, deleted there.
SIP_BANK_FLOOR       = 20      # what the tap leaves in the bank when
                               # SIP_RESERVE_ON is False.  Not a doctrine, just
                               # a guard so the plank cannot strip the last
                               # titanium out of a heal or a spawn.
SIP_RESERVE_PAD      = 30      # CB_RESERVE = 2 x gunner cost + this.  A3 does
                               # not exist in this build, but the tap must be
                               # junior in funding here exactly as it will be
                               # when A3 lands, or the arm is measured against
                               # a budget it will not have.


# ===========================================================================
# WAVE 22 -- TRACK 2, ARM A5.  THE TITANIUM-TIEBREAK ENDGAME  (`END_ON`)
#
# analysis/wave21/tiebreak.md (the whole document) + its re-engineering
# shortlist row 2 ("ENDGAME PHASE at r700, armed at r400"), which is the one
# plank of the wave-21 blueprint that wave 22B never built.  ONE arm, ONE
# master flag, an OFF twin (bots/leap18_end_off) that is this directory byte
# for byte with the master False.  `END_ON = False` restores bots/loki_leap16
# line for line: every hook is inside `if END_ON` and every helper returns its
# typed empty value before it reads anything.
#
# ---------------------------------------------------------------------------
# 1.  THE HOLE THIS FILLS, IN FOUR MEASURED NUMBERS
# ---------------------------------------------------------------------------
#
#   * `titanium_collected` is the ONLY tiebreak that has ever fired --
#     `harvesters` / `titanium_stored` / `coinflip` fired 0 times in 450 games
#     (tiebreak.md 1).  It is reached in 6.7 % of elite games and 4.3 % of
#     ours, and P(r1000 | r400) is 53 % elite / 43 % ours.
#   * WE GO 2-11 (15 %) IN THOSE GAMES.  Jython goes 8-2 (80 %).
#   * Our median margin swing over r800->r1000 is **-500**.  The elite winners'
#     is **+1665**; Jython's own across all ten of its tiebreak games is +1180.
#     Negative in 11 of our 13.
#   * IN 8 OF OUR 13 THE HARVESTER / CONVEYOR / TURRET COUNTS ARE BYTE-
#     IDENTICAL AT r800 AND AT r1000.  We stop playing.  There is no late
#     program of any kind.  Two of those losses ended with **5 773** and
#     **7 991** titanium unspent, and three were inside one late program's
#     reach: -100 (that is TEN titanium, one delivery), -370, -880.
#
# ---------------------------------------------------------------------------
# 2.  CRITIC M3, AND WHY IT DECIDES THE SHAPE OF EVERY RULE BELOW
# ---------------------------------------------------------------------------
#
# `titanium_collected` counts ONLY titanium that PHYSICALLY ARRIVED AT A CORE.
# Passive income is excluded and **the bank does not count**
# (engine_mechanics.md A: idle 91-round game, 220 Ti of passive income,
# `a_titanium_collected = 0`).  Three consequences, and they are the arm:
#
#   (a) FROM ~r700 BANKED TITANIUM IS A SCORED ZERO.  Pivot ended
#       `8a106d9f_g1` sitting on 10 370 unspent and lost by 530 while its
#       collection rate was being cut 89 %.  So the endgame does not hoard --
#       but it does not spend on ANYTHING either.  It spends on DELIVERY.
#   (b) A MAGAZINE IS NOT DELIVERY.  Ammunition scores in no tiebreak and
#       moves no stack.  It is not banned -- turrets that protect the pipeline
#       are delivery infrastructure -- it is SUBORDINATED: the conversion may
#       not take the bank below the price of the next harvester and its first
#       two conveyors (arm 2).
#   (c) A SIEGE IS NOT DELIVERY EITHER, AND IT IS THE EXPENSIVE ONE.  A body
#       standing at their ring delivers nothing, and the tubes and rungs it
#       buys deliver nothing.  Jython lost `7e76fd49_g2` 70-9710 by grinding a
#       healed Core for 1000 rounds -- 1710 damage, 1.7 HP/round net of
#       healing -- and tiebreak.md calls that "our v161 profile".
#
# ---------------------------------------------------------------------------
# 3.  THE TRIGGER.  ARMED AT r400, FIRES AT r700, LATCHED ONE-WAY
# ---------------------------------------------------------------------------
#
# ARMED AT r400 (`END_ARM_RND`) because that is the alarm the corpus names:
# P(r1000 | r400) = 53 % / 43 %, i.e. from r400 it is a coin-flip whether the
# game becomes an economy exam (tiebreak.md 9 rule 12).  **Arming is
# OBSERVATIONAL ONLY and that is deliberate** -- it starts the stall clock and
# prints `END arm`, and it changes not one titanium of behaviour.  A wave that
# has already been told twice that bundling mechanisms makes a regression
# uninterpretable (PLAN.md 0.2) does not get to put half an arm at r400 and
# half at r700 and then read one number.
#
# FIRES AT r700 (`END_FIRE_RND`) because the measured comeback window is the
# last 200-300 rounds and it is worth +-2500 Ti of margin: it flipped
# `6c42117a_g4` (-420 -> +50) and `8a106d9f_g1` (-2030 -> +530).  Three of
# Jython's eight tiebreak wins were won by an economy switched ON at r739,
# r826 and r881 after 700+ rounds at zero.
#
# THE PREDICATE -- "the kill is not coming":
#
#     fire  <=>  rnd >= END_FIRE_RND
#                AND the enemy Core has not been read below the LOW band
#                    (`SIEGE_MASS3_HP`) for END_STALL_RNDS consecutive rounds
#
# and that second clause is BOTH halves of "enemy core HP high + our siege
# dead" in one quantity, on purpose.  The evidence is that the two are the
# same event: in 6 of the 10 elite tiebreak games the TOTAL core damage of the
# whole 1000-round game was already on the board by r100-r400 and never moved
# again (tiebreak.md 2).  A siege that is alive is a siege that is moving the
# HP band; one that is not is dead whether or not a body is still standing
# there -- which is exactly the `7e76fd49_g2` case, where the body WAS still
# standing there for a thousand rounds.
#
# WHY NOT `_foothold_live` AS THE "SIEGE DEAD" TEST -- and this is a defect
# that was written, read back and removed rather than shipped.  The heartbeat
# is published BY the raiders themselves.  A raider that has not yet latched
# keeps the heartbeat fresh, which keeps every other body's "siege dead" test
# False, which keeps that raider raiding: the arm would deadlock on its own
# output in exactly the games it exists for.  The HP band has no such
# self-reference -- it is a property of THEIR Core, not of our behaviour.
#
# LATCHED ONE-WAY, and the doctrine is quoted: "When the core siege stalls,
# quit it -- completely and permanently.  Median abandonment ~= r150"
# (tiebreak.md 9 rule 2).  If their Core drops below the band at r800 we do
# NOT go back; a re-arming trigger is a trigger that spends the last 300
# rounds oscillating, and the corpus says the tops abandon once and never
# return.
#
# WHERE THE STATE LIVES, AND WHY IT IS NOT A NEW COMM SLOT.  PLAN.md 1.5
# forbids one and all 16 slots are assigned.  The Core is the only unit alive
# from r0, so it is the only unit whose stall clock is complete, and it is
# ALREADY the sole writer of slot 9 (`SLOT_HEAL_BUDGET`) every single round
# (`T4_BLEED_BEACON_ON`).  That word carries the bleed figure in bits 0-15 and
# the archetype in bits 16-27; bits 28-31 belong to SOCKET-GUARD, and
# **`SG_ON` is False in this carrier**, so those four bits are unconditionally
# zero.  END takes ONE of them -- bit 28 -- republished whole every round by
# the one writer, which is the discipline doctrine.py 2b arrived at the hard
# way for the HP band itself.  The publish is guarded on `not SG_ON`: if a
# later build turns SOCKET-GUARD on, END publishes nothing and every unit
# falls back to its OWN stall clock, which fires LATER (never earlier) for a
# body that spawned after r400.  That is a typed, conservative fallback, not a
# silent collision.
#
# ---------------------------------------------------------------------------
# 4.  THE FOUR ARMS, EACH WITH THE ARITHMETIC THAT FORCES IT
# ---------------------------------------------------------------------------
#
# ARM 1 -- QUIT THE SIEGE, PERMANENTLY (`END_QUIT_ON`).  Every raider walks
#   back inside `END_HOME_DSQ` of our own Core and becomes an expander for the
#   rest of the match.  ONE hook, at the top of `_raid`, above the heartbeat
#   publish -- so the whole forward tree (forward sentinels, the screen
#   gunner, the ferry rungs, the collar, the cage, the launcher pluck) is
#   bypassed by construction rather than by a flag apiece.  The FERRY needs no
#   hook of its own: `_launcher_turn`'s ferry half is gated on
#   `SLOT_FERRY_ID`, which only `_raid_ferry_ping` writes, so it disarms
#   itself within `LOKI_FERRY_STALE_RNDS`.  The launcher's EXILE half is left
#   alone: throwing an intruder off our own doorstep is home defence and home
#   defence is delivery protection.
#   THE WALK HOME IS NOT COSMETIC.  `_pick` partitions ore by manhattan
#   distance from OUR Core, so a body left forward will happily build a
#   harvester on their half and then lay a twenty-tile chain back -- +1 % cost
#   scale per tile, delivering its first stack twenty rounds later, and by then
#   there are no rounds left.  While it walks it spends nothing at all, and its
#   ACTION is still available to the repair and heal arms that sit above the
#   role split.  Bounded by `END_RECALL_MAX`; a body that cannot get home in
#   that many rounds converts where it stands and prints `END strand`.
#
# ARM 2 -- SUBORDINATE THE MAGAZINE (`END_AMMO_SUBORD_ON`).  Section 2(b).
#   The Core keeps `get_harvester_cost() + END_ECO_RESERVE_CONV *
#   get_conveyor_cost()` back from `convert_ammo`, in BOTH the per-round JIT
#   pipe and the r960 dump.  SUSPENDED WHILE `under` IS SET -- a dry turret
#   with a besieger on its ray is the one case where the magazine outranks the
#   eleventh harvester, and `CB_DRY_MAG_ON` is still allowed to pull the floor
#   back down underneath this one.  It is a FLOOR ON THE SPEND, never a cap on
#   the target: nothing here reduces how much ammunition we want, only what we
#   are willing to starve to get it.  Note against tiebreak.md 7's "~120
#   sustained is the elite marker": that number is NOT a wave-22 target
#   (PLAN.md 1.3 demotes it to observational), and this arm does not chase it.
#
# ARM 3 -- KEEP DELIVERING TO r1000 (`END_KEEP_DELIVER_ON`).  The incumbent's
#   own `ENDGAME_SWITCH_ON` at r960 switches the trunk chain, `_l4_repair` and
#   the chain medic OFF for the last forty rounds, because it was written for
#   tiebreak #2 (`harvesters`) and tiebreak #3 (`titanium_stored`).  **Neither
#   has ever fired, in 450 games.**  A severed trunk zeroes its whole line
#   (engine_mechanics.md B) and forty rounds of a line is up to 400 Ti of the
#   only stat that scores.  Under END that freeze does not apply; the harvester
#   gate reverts to the ordinary `_eco_spendable` / `_eco_cap` pair rather than
#   the r960 branch's unconditional one, because tiebreak.md 9 rule 9 is
#   explicit that harvester COUNT is not the variable -- winners run 125-235
#   Ti/harvester/100r and losers run 0-94 with MORE harvesters.
#
# ARM 4 -- PROTECT THE PIPELINE (`END_MEDIC_ON`).  The chain medic's
#   `MEDIC_TI_FLOOR` of 20 Ti is dropped to `END_MEDIC_TI_FLOOR`.  A heal is
#   1 Ti and costs no cost-scale at all, a relay is 3 Ti and +1 % scale for
#   ever, and a belt that dies takes its whole line's income with it.  Bean
#   shrugged off 139 kills on one tile by parking bodies on the trunk
#   (tiebreak.md 4); this is the cheap half of that, using machinery that
#   already exists.
#
# ---------------------------------------------------------------------------
# 5.  WHAT IS DELIBERATELY NOT IN THIS ARM
# ---------------------------------------------------------------------------
#
# * NO EDGE-CUT DENIAL, AND IT IS MEASURED DEAD.  `202a0ef6_g2`: Jython fired
#   886 shots, 711 at Bean's economy, destroyed the conveyor at (23,21) ONE
#   HUNDRED AND THIRTY-NINE times -- roughly 7 000 Ti of ammunition -- and
#   Bean's collection rate over r200-r1000 was CONSTANT, because Bean had two
#   independent trunks.  Denial only pays against a single-path trunk, the gate
#   that would prove it is A4's (`SIPHON_CUT_SHARE`, G1-G4), and A4's own
#   doctrine records that gate's honest output for ammunition-based denial as
#   "do not do it".  This arm therefore buys no denial at all.
# * NO SOURCE TAP HERE (`END_TAP_ON`, present and **False**).  The source tap
#   -- a conveyor cardinally adjacent to an enemy harvester, facing away onto
#   our own trunk, taking 1/(n+1) of a team-blind round robin -- is the ONLY
#   denial tiebreak.md endorses, and it is ARM A4's mechanism, already built
#   and already screened in `bots/leap18_sip`.  Re-implementing it behind END's
#   flag would (i) duplicate the code, (ii) confound A4 with A5 in exactly the
#   way PLAN.md 0.2 forbids, and (iii) rest on A4's weakest evidence (n = 17
#   from a 32 %-win team) rather than on the +1665-vs--500 delivery swing that
#   is this arm's actual case.  The composition belongs in PLAN.md 3.3.6's
#   STAGE 3 integration build, where cancellation is what is being measured.
#   The flag exists so that composition is a flag flip and not a rewrite.
# * NO FORWARD TRUNK RAIDER.  `8a106d9f_g1`'s +2560 swing came from sentinels
#   at dEnemyCore 3.6-7.6 shooting conveyors, and it is real -- but it is a
#   SIEGE-SHAPED spend (bodies and tubes forward) inside an arm whose first
#   rule is that the siege is over, and blueprint row 3 gives it its own plank.
#   Recorded, deferred, not killed.
# * NO EXTRA BODIES.  `LOKI_SURPLUS_TI` (260) and `LOKI_RICH_TI` (700) already
#   lift the builder budget to `LOKI_MAX_BUILDERS` = 11 on exactly the banks
#   the two 5 773 / 7 991 losses were sitting on, so the lever is already
#   pulled; raising the ceiling would add cost scale to every later harvester
#   for a body that arrives with 300 rounds to live.
#
# ---------------------------------------------------------------------------
# 6.  WHAT WOULD KILL IT -- pre-registered, and not editable after a number
#     has been seen (PLAN.md 3.5)
# ---------------------------------------------------------------------------
#
#   F-E1  the arm never fires: `END fire` in < 60 % of games that REACH r700.
#   F-E2  it fires in a game we were winning: `END fire` while the enemy Core
#         was below `SIEGE_MASS3_HP` inside the preceding `END_STALL_RNDS`.
#         Bar = 0.  (Impossible by construction; it is registered because
#         "impossible by construction" is what wave 20 said about three
#         things that then happened.)
#   F-E3  `titanium_collected` does not rise vs control on the fired games.
#         This is the arm's entire theory of change; if it fails, ABLATE.
#   F-E4  median swing over r800->r1000 does not move above the recorded -500.
#   F-E5  harvester / conveyor counts still byte-identical at r800 and r1000
#         in > 30 % of fired games (control: 8 of 13).
#   F-E6  `titanium_collected@r100` falls vs control -- the arm has leaked
#         behaviour into the opening, which nothing in it may touch.
#   F-E7  spend-through (G-E) falls vs control: arm 2 is hoarding rather than
#         redirecting.
#   F-E8  bank at r1000 median > 200 Ti on fired games (control: 5 773 / 7 991
#         on two of thirteen).
#   F-E9  `exec_us` p95 > 3x control on `fcode match test`.
#   F-E10 the head-to-head or any panel guard breaches G-A1/G-A2 by > 2.0 pp.
#
# ---------------------------------------------------------------------------
# 7.  STANDING RISKS
# ---------------------------------------------------------------------------
#   R1  IT QUITS A WINNABLE SIEGE.  A Core at 401 HP reads HIGH.  Accepted and
#       bounded: `END_STALL_RNDS` = 200 means the band must have been HIGH or
#       UNKNOWN for two hundred consecutive rounds, and a siege landing damage
#       at any rate at all crosses 400 inside that window.
#   R2  THE RECALL FEEDS THEIR RING.  Bodies walking home past their turrets
#       die.  They were going to die standing still; a dead raider at r700 is
#       worth less than a live conveyor-layer at r760.
#   R3  ARM 3 SPENDS AT r999.  A harvester built at r999 delivers nothing and
#       costs scale.  Left in deliberately: the eco cap and `_eco_spendable`
#       are unchanged, so this is the incumbent's own spend curve running
#       forty rounds longer, not a new one.
#   R4  BIT 28 OF SLOT 9.  Safe only while `SG_ON` is False.  Guarded, with a
#       fallback, and stated here so the next build that flips `SG_ON` finds
#       this paragraph.
# ===========================================================================
END_ON = True                # master.  False == bots/loki_leap16, line for line
END_LOG = False               # `END arm/fire/quit/home/strand` markers.
                             # MEASUREMENT SCAFFOLDING -- False in any build
                             # that reaches a verdict cell (PLAN.md 1.5).

END_ARM_RND = 400            # the alarm: P(r1000 | r400) = 53 % / 43 %
END_FIRE_RND = 700           # the comeback window is the last 200-300 rounds
END_STALL_RNDS = 200         # consecutive rounds their Core stayed >= the LOW
                             # band before we call the siege dead.  200 of the
                             # 300 armed rounds; a siege landing damage at any
                             # rate crosses SIEGE_MASS3_HP inside it.
END_BIT = 1 << 28            # slot 9 bit 28, published by the Core alone and
                             # ONLY while SG_ON is False (section 3, risk R4)

END_QUIT_ON = True           # arm 1: the siege is over, permanently
END_HOME_DSQ = 64            # d <= 8 of our own Core centre == "home".  Core-
                             # relative, so it is map-independent by
                             # construction (no map name, no pool constant).
END_RECALL_MAX = 80          # rounds a recalled body may spend walking before
                             # it converts where it stands.  One tile a round
                             # crosses any map in the pool.
END_STUCK_MAX = 12           # ...or this many consecutive rounds with the body
                             # not having moved at all, which is `_builder`'s
                             # own `self.stuck` and means WALLED IN rather than
                             # slow.  Measured: nordkap/seed 204 sat one body at
                             # (9,17) with move cooldown 0 and a valid BFS step
                             # for the whole 80-round budget.

END_AMMO_SUBORD_ON = True    # arm 2: delivery outranks the magazine
END_ECO_RESERVE_CONV = 2     # ...by harvester + this many conveyors

END_KEEP_DELIVER_ON = True   # arm 3: the r960 freeze does not apply
END_MEDIC_ON = True          # arm 4: the chain medic's titanium floor
END_MEDIC_TI_FLOOR = 2       # a heal is 1 Ti and costs no cost scale

END_BAND_ON = True           # keep the enemy-Core HP band PUBLISHED even if
                             # both of its incumbent consumers are ever turned
                             # off.  A no-op on this carrier (SIEGE_MASS_ON is
                             # True), and it is here so the trigger cannot be
                             # silently starved by an unrelated ablation.
END_TAP_ON = False           # PARKED.  Section 5: the source tap is arm A4's
                             # mechanism (bots/leap18_sip) and composing the
                             # two is a STAGE 3 job, not a second copy here.



# ---------------------------------------------------------------------------
# F6 -- FRIENDLY-PECK TEAM TEST                       (MISBEHAVE_AUDIT sec 6)
#
# THE DEFECT.  388 corpus pecks on our OWN buildings (387 conveyors, 1
# harvester), 63 in the v162 ladder set; every target on our own side, 31 of
# 91 sampled exactly on a Core socket.  Verified in the engine damage record:
# `w26d game_3` yulerune r105, our builder #5 at (4,10) fired at (4,11) and
# the damage list carries `{'id':126,'kind':'conveyor','team':0,'delta':-2}`.
# Ten of the eleven `ct.fire` sites carry an inline
# `get_team(bid) == self.team: continue`.  The one that does not is
# `_ring_evict`, `ring.py` -- it reads `get_tile_building_id(t)` and trusts the
# `foe` set from `_sg_socket_scan`, which is MEMOISED PER ROUND (`eco.py`), so
# a socket cleared earlier in the same round is still listed as enemy-held.
#
# THE FIX.  `_f6_ok(ct, t)` in `eco.py`, and one line at EVERY `ct.fire` site
# in the tree (14 of them), not only the broken one: the ten that already
# carry an inline test keep it and gain a second, uniform refusal that cannot
# drift when a call site is edited.
#
# THE PREDICATE REFUSES ONLY ON POSITIVE EVIDENCE, and both halves matter:
#   * `bid is None` -> ALLOW.  A Core footprint tile that reads back no
#     building id must never be turned into a refusal, or CAGE / FIN lose the
#     core peck outright.
#   * our building on the tile, BUT an ENEMY BODY standing on it -> ALLOW.  A
#     turret shooting an enemy builder that happens to stand on our own
#     conveyor is a legitimate shot; refusing it would be a new defect.
#   * anything unreadable -> ALLOW.  Fails open, like every other guard here.
# Only "a building that is positively OURS, with no enemy body on the tile"
# is refused.  It can therefore only ever remove illegal targets.
# ---------------------------------------------------------------------------

F6_TEAM_TEST_ON = True       # MASTER.  False == v162 at every fire site.
F6_LOG = False


# ============================================================================
# WAVE 30 -- BELT EVICT.  THE APRON BARRIER IS AN EVICT TARGET.
#
# THE DEFECT.  `results/wave29/EMERGENCY_BLEED.md` section 2, and it is the
# mechanism that lost the two kladde v126 matches outright: v126 NEVER
# ATTACKS.  It drops four to five barriers across OUR BELT PATH at squared
# distances 2.2-6.4 from our Core and then waits while our harvester feed
# dies.  In two of those games we collected 0 titanium in 269 of 530 rounds;
# `titanium_collected` finished 0/3160 and 0/240.  `results/wave29/KLADDE126.md`
# prices the apron at +63 % density over v125.
#
# WHY THE INCUMBENT NEVER SHOOTS BACK AT IT.  `RING_EVICT` (ring.py, ARM 2) is
# the only arm in the tree that evicts an enemy building near our own Core,
# and its target set is EXACTLY the eight sockets of `_sg_socket_scan` --
# `sg_socket(self.core, i)`, i.e. the twelve-tile collar.  Every one of those
# tiles is at `dsq_core` 1 or 2.  A barrier at 2.2-6.4 is OUTSIDE THAT
# GEOMETRY, so `foe` is empty, `_ring_evict` returns False on its second test,
# and the brick stands for the rest of the match.  Nothing else in the tree
# reaches it either: `_lp_peck` is launchers only, `_sap` is the besieger
# band, `_eb_peck` is dead (EB_PECK_ON = False), and F5 -- the only belt arm
# ever built -- REFUSES a tile carrying an enemy building by construction
# (`is_tile_empty`) and was killed on measurement anyway
# (`results/wave28/SCREEN_CLEAN.md`).
#
# THE ARM.  ONE new target class for machinery that already exists:
#
#     an ENEMY BUILDING standing ON or ORTHOGONALLY ADJACENT to one of OUR
#     conveyor-chain tiles, within `BELT_EVICT_DSQ` of OUR Core,
#
# is pecked by at most `BELT_EVICT_BODIES` HOME bodies, and a standing home
# gunner prefers a post and a facing that cover it.  Everything else -- the id
# ballot, the per-tile clock, the walk budget, the titanium floor, the shell
# gate -- is `RING_EVICT`'s, reused verbatim.
#
# "ON, OR ORTHOGONALLY ADJACENT" IS ONE TEST, NOT TWO.  A tile carrying an
# enemy building is not one of our belt tiles -- the engine allows one
# building per tile -- so "the barrier standing ON the path" is observable
# only as "the barrier standing in the HOLE in the path", which is a tile
# orthogonally adjacent to our belt on TWO sides.  The census therefore counts
# belt adjacencies and RANKS BY THAT COUNT: a candidate touching two or more
# of our belt tiles is a hole in the line and is pecked first, a candidate
# touching one is the apron and is pecked after it.  No second geometry.
#
# WHY NO REFILL, AND WHY THAT IS NOT `RING_EVICT`'s MISTAKE REPEATED.
# `RING_EVICT` refuses to clear a socket it cannot refund because a cleared
# socket is re-bricked inside five rounds and an OPEN SOCKET IS WHAT THE ENEMY
# WANTED (ring.py, ARM 2).  A belt-apron tile is not one of our eight sockets
# and we never wanted to build on it: cleared, it is simply a tile our
# harvester feed and our bodies can pass again, and there is nothing to
# refund.  The funding test is therefore the peck's own 2 Ti plus
# `BELT_EVICT_TI_FLOOR`, and the CLEAR+RETAKE coupling is deliberately absent.
# The socket case is NOT double-handled: a candidate that IS one of our eight
# sockets is dropped from this census and left to `RING_EVICT`, which owns it
# and can fund the retake.
#
# THE FIVE BOUNDS, all of them RING's own numbers:
#   * `BELT_EVICT_MAX_PECKS` = 20 per TILE per body.  A barrier is 30 HP and a
#     builder peck is 2 damage, so 15 pecks kill it and 20 is one round of
#     slack for a peck lost to a cooldown.  Keyed on the TILE and not on the
#     building id, for `RING_EVICT_TRY_RNDS`'s reason: the failure this bounds
#     is the opponent RE-LAYING the brick, which hands us a fresh id every
#     time and would reset an id-keyed clock for ever.
#   * `BELT_EVICT_BODIES` = 2, decided by `_ring_evict_ok`'s id ballot -- the
#     same ballot, called with a different cap.  Two bodies kill a barrier in
#     eight rounds; three is the SAP failure the parent records.
#   * `BELT_EVICT_LIFE` = 40 pecks per body, two barriers' worth, RING's
#     `RING_EVICT_LIFE` scaled by the two-barrier unit it is written in.
#   * THE HOME BAND.  Only a body inside `BELT_EVICT_HOME_DSQ` of OUR Core
#     (`RING_WALK_BAND_DSQ`, unchanged) may peck or walk, and NEVER a body on
#     THEIR ring: `_f0_plug` is the guard, verbatim, because wave 27 measured
#     moving a parked body off their collar at -6 wins / +93 kill rounds
#     (`results/wave27/VERDICT_27.md` section 2).  Raiders are excluded by
#     role as well -- LOKI-QUIET is not in dispute here.
#   * THE SHELL GATE.  `_ring_eco_ready` (two harvesters), because this arm
#     defends an economy and does not substitute for one -- the same gate
#     that stopped the first RING screen finishing on 0 titanium at r30.
#
# THE GUNNER HALF, and it is why this plank is aimed at the bleed rather than
# at kladde alone.  `analysis/wave24/V162_LADDER_UPDATE.md`: their tubes@r100
# = 0 -> we win 65.8 %, >= 1 -> 29.3 %; and v162 built ZERO home gunners in
# 58 % of games against v161's 12 % because GD's NO SILENT GUN
# (`GD_SILENT_OFF`) vetoes every post whose ray does not ALREADY contain one
# of theirs.  An apron barrier IS one of theirs, standing still, at d 2.2-6.4,
# permanently in reach of a post at `RG_SITE_DSQ`.  So the same census that
# feeds the peck is added as a SCORING TERM to `_rg_gun`'s site/facing scan
# (`BELT_EVICT_GUN_BONUS`) and as the FIRST key of `_gd_reaim`'s facing
# ranking: a gunner ray clears a 30-HP barrier in 5 shots
# (`analysis/engine_mechanics.md`) against a builder's 15 pecks, and unlike
# the builder it keeps doing it to the re-lay.
#
# WHAT THE GUNNER HALF DELIBERATELY DOES NOT DO.  It does not touch
# `_rg_trigger` (the arm still needs an enemy BUILDER inside `RG_TRIGGER_DSQ`
# to open the window), it does not touch `RG_MAX` (still one gun a match), and
# it does not weaken `_rg_ray_clean` by a single tile -- a ray containing ANY
# of our own buildings is still refused outright, which means a barrier with
# our own conveyor BEHIND it on the same line is a peck target and never a gun
# target.  Rule 9 fratricide is not traded for this.  The bonus can only ever
# re-rank posts and facings that already passed every incumbent gate.
#
# CPU.  The census is memoised per unit per round and bounded by
# `BELT_EVICT_MAX_TILES`; it reads `get_nearby_buildings` (an enumeration
# `_builder` already runs) plus at most one `get_tile_building_id` per
# distinct candidate tile.  Both halves refuse themselves in two integer tests
# on every body that is not standing at home, which is most bodies most
# rounds.
#
# OFF TWIN.  `bots/leap30_beltevict_off` is this file with `BELT_EVICT_ON` and
# `F6_TEAM_TEST_ON` both False, which is `bots/loki_leap18` (v162) line for
# line: every added statement in ring.py, main.py and eco.py is inside a
# method that returns on its own head guard, or behind an
# `if BELT_EVICT_ON`/`if F6_TEAM_TEST_ON` clause.  Proof:
# `tools/analysis_scratch/w30_static_proof.py`, DOCTRINE.md "WAVE 30 BELTEVICT".
# ============================================================================

BELT_EVICT_ON = True         # MASTER.  False == bots/loki_leap18 (v162).
BELT_EVICT_LOG = False       # `BELT evict/target` markers, off in competition.
BELT_EVICT_DSQ = 49          # d <= 7 of OUR Core: the apron band the kladde
                             # v126 decode measures (barriers at d 2.2-6.4),
                             # with three tiles of margin and nothing beyond
                             # it -- past d 7 a body is walking, not defending.
BELT_EVICT_MAX_PECKS = 20    # per TILE per body.  30 HP / 2 = 15, plus slack.
BELT_EVICT_BODIES = 2        # bodies pecking one tile at once (the id ballot).
BELT_EVICT_LIFE = 40         # lifetime pecks this arm may spend, per body.
BELT_EVICT_TI_FLOOR = 2      # titanium kept back from the 2 Ti peck.
BELT_EVICT_ECO_GATE = True   # the shell gate (`_ring_eco_ready`) applies.
BELT_EVICT_WALK_ON = True    # the bounded walk, on RING's shared budget
                             # (`ring_walk_total`, `RING_WALK_CAP`).
BELT_EVICT_HOME_DSQ = 64     # a body must already be this near OUR Core.
BELT_EVICT_MAX_TILES = 40    # CPU bound on the belt census, per unit per round
BELT_EVICT_GUN_ON = True     # the gunner half: siting bonus + re-aim key.
BELT_EVICT_GUN_BONUS = 6     # per covered target tile in `_rg_gun`'s score.
                             # Above RG_MIN_SCORE (4) so one covered apron
                             # barrier can carry a post on its own, and well
                             # below RG_INTRUDER_BONUS (20) so a body we can
                             # actually see still outranks a building.


# ============================================================================
# WAVE 31 -- PLANK RESTORE.  Two flags: `RESTORE_EVICT_ON`, `RESTORE_HOLE_ON`.
#
# ONE IDEA, TWO CALL SITES: *put the income back the round it is cut.*
# `analysis/wave31/TOP3_SYNTHESIS.md` section 1 names one disease with three
# entry wounds -- cut the income, we never restart it, we go broke, broke turns
# every body into a healer, the first besieger ends it -- and sections 3(a) and
# 3(b) are the two halves of the RESTART defect.  Neither plank buys a NEW
# campaign, a NEW walk or a NEW target class outside the ones already censused
# every round; each removes exactly one refusal the forensics proved is firing
# in the games we lose 0-15.
#
# ---------------------------------------------------------------------------
# PLANK A -- `RESTORE_EVICT_ON`.  THE GATE SPLIT.
# ---------------------------------------------------------------------------
# v164 gates SIX things on the harvester shell (`_ring_eco_ready`, i.e.
# `SLOT_HARVESTERS >= RING_ECO_HARV` = 2):
#
#     (1) the CLAIM CEILING  `_ring_want`          ring.py 179
#     (2) the CLAIM WALK     `_ring_claim_walk`    ring.py 303
#     (3) the EVICT PECK     `_ring_evict`         ring.py 464
#     (4) the EVICT WALK     `_ring_evict_walk`    ring.py 560
#     (5) the BELT twin      `_belt_evict`         ring.py 859
#     (6) the BELT WALK      `_belt_evict_walk`    ring.py 926
#
# `results/wave31/TOP3_Clankers.md` section 5 is the finding: delivery needs one
# of OUR buildings on OUR ring8, Clankers bricks all eight of them, and (3)
# refuses to peck a brick off our own socket until two harvesters stand -- which
# we cannot build, because building them needs the delivery the brick is
# blocking.  Circular.  Measured over the five games: harvesters built g1 r109 /
# g2 never / g3 r14 / g4 r101 / g5 r9, and our first attack on our own ring8 g1
# never / g2 never / g3 r38 / g4 r155 / g5 r39.  It tracks the gate exactly, and
# g5 is the positive control -- harvester r9, brick r39, peck r39, one of only
# two games in five we delivered anything at all.
#
# THE SPLIT, and it is the whole plank.  Doctrine's own measurement (the
# `RING_ECO_GATE_ON` block above, ~6263) priced the CLAIM: eight socket
# conveyors by r30, 1 harvester against the control's 2, `titanium_collected@30`
# 0 against 40.  Laying plugs competes with the harvester budget, and the WALK
# is where that cost lives -- `RING_WALK_CAP` is 24 rounds per body, so five
# bodies can spend 120 body-rounds walking home in the opening.  Clearing an
# ENEMY brick off a socket we already own is a different purchase entirely: it
# cannot ratchet (`RING_MAX_OWN` still binds every claim), it costs 2 Ti a peck,
# and the refill is the conveyor we would have laid anyway.  The two halves were
# gated together for convenience, not on evidence.
#
# So (1), (2), (4) and (6) KEEP the shell gate byte for byte.  (3) and (5) route
# through `_ring_evict_gate_ok`, which returns True when the shell is up
# (v164's own condition, unchanged) and OTHERWISE only when BOTH
#
#     rnd >= RING_FLOOR_MIN_RND  -- 6.  r1-r5 is the harvester bootstrap and
#                                  nothing on the ring may pre-empt it; and
#     AN ENEMY BUILDING STANDS ON ONE OF OUR EIGHT SOCKETS
#                                 -- `_ring_foe_on_ring`, the `foe` set of
#                                  `_sg_socket_scan`, memoised per unit/round.
#
# Everything else in both arms is untouched: `RING_EVICT_TI_FLOOR`, the refill
# funding test (CLEAR + RETAKE, never CLEAR alone), `RING_EVICT_TRY_RNDS`, the
# `_ring_evict_ok` id ballot, `RING_EVICT_LIFE`, `BELT_EVICT_BODIES` = 2,
# `BELT_EVICT_MAX_PECKS` = 20, `BELT_EVICT_LIFE`, `_belt_home_ok` (the plug
# rule), `_f6_ok`.  BOUND: one 30-HP barrier is about 11 builder pecks, roughly
# 22 Ti plus a 3 Ti refill, about 7 rounds -- and `RING_EVICT_TRY_RNDS` walks a
# body away for good from a doorway it cannot win.
#
# WHY THE BELT TWIN IS IN THE SPLIT AND ITS WALK IS NOT.  `_belt_evict` drops
# our eight sockets from its own target set (`_belt_evict_targets`), so it is
# never a second peck at the same brick; what it clears is the apron barrier
# standing IN the trunk one tile further out, which is the same severance seen
# from the other side.  Its de-gate is conditioned on the SAME predicate -- a
# brick on our ring8 -- so it can only widen while the door itself is shut,
# which is exactly the deadlock window.  The WALKS stay gated because the walk
# is the thing the r30 measurement priced.
#
# WHAT THIS IS NOT.  Not `leap20_ringev`, which `return`ed from `_builder` and
# so forfeited the build action (Ti@100 -15 %); not `leap19_evict`'s resident
# evictor.  No new campaign, no new walk, no new target class -- the existing
# budgeted peck with one precondition removed.
RESTORE_EVICT_ON = False

# ---------------------------------------------------------------------------
# PLANK B -- `RESTORE_HOLE_ON`.  THE HOLE THE DETOUR COULD NOT SEE.
# ---------------------------------------------------------------------------
# `results/wave31/TOP3_Pivot.md` section 5: `eco.py::_l4_repair` fills only a
# tile ORTHOGONALLY ADJACENT to the acting body, and the only dispatch that can
# move a body toward a repair, `_rep_detour_target`, ranks
# `ct.get_nearby_buildings()` filtered on
# `get_max_hp - get_hp >= REPAIR_DETOUR_MIN_DMG`.  A DESTROYED conveyor is not a
# damaged building -- it is an empty tile with no id -- so there is no code path
# in v164 that sends a body to a hole.  Cost, measured by `w31_hole_probe.py`:
# Pivot g5, a body within 4 Manhattan steps of the one-wide hole on 74 of the 76
# unwired rounds, `titanium_collected` frozen at 50 for 133 rounds; g2 40 %;
# belt uptime 6-7 % in the two games we died fastest.
#
# THE SECOND CANDIDATE CLASS, and its definition is the whole safety case,
# because `results/wave28/VERDICT_28.md` records what the wrong one costs: F5's
# belt repair was POISON because its undirected BFS queued tiles that reconnect
# nothing.  This class is NOT a BFS and NOT "any empty tile near the belt".  A
# tile is a candidate only when ALL of the following hold:
#
#   * THIS BODY WATCHED IT DIE.  `self.rep_lost`, the death-watch memory
#     `REPAIR_REBUILD_ON` / `REPAIR_GAP2_SEEN_ONLY` already keeps
#     (`eco.py::_rep_watch`): one of OUR belts stood there when this body last
#     looked, the tile is in its vision NOW, and it is no longer there.  That is
#     the only in-engine evidence a trunk tile was DESTROYED rather than never
#     laid, and the audit behind `REPAIR_GAP2_SEEN_ONLY` is why it is mandatory:
#     ungated, 0 of 23 relays were destroyed tiles and 23 were DEAD HEADS.
#   * IT IS ON THE REMEMBERED TRUNK, WITH A REMEMBERED FACING.  `rest_face`
#     records the direction of each of our conveyors while it is ALIVE, so the
#     relay goes back DOWN the chain instead of pointing at nothing.  No facing
#     remembered = not a candidate.  A splitter is never a candidate: only
#     `EntityType.CONVEYOR` ever writes `rest_face`.
#   * IT IS EMPTY AND IN VISION NOW -- `ct.is_in_vision` then
#     `ct.is_tile_empty`, the valkyrie FIX-3 lesson: never queue a tile you
#     cannot see.
#   * IT IS WITHIN `RESTORE_HOLE_STEPS` = 6 MANHATTAN of the acting body, and
#     that body is FREE, NON-RAIDER and HOME: `role != "raid"`,
#     `dsq_core <= RESTORE_HOLE_HOME_DSQ`, and NEVER a body on THEIR ring --
#     `_f0_plug`, verbatim, which is `results/wave27/VERDICT_27.md`'s PLUG rule
#     and the one refusal here that is not about our own economy.
#   * IT IS PAVE-LEGAL AND ON OUR OWN HALF -- `pave_blocked` (the ore ban: a
#     conveyor on ore costs that harvester site for the rest of the match) and
#     `LOKI_L4_OWN_HALF_ONLY`, both identical to `_l4_repair`'s own tests.
#   * IT IS NOT BANNED.  A target not reached inside `REPAIR_WALK_RNDS` is
#     written off for `REPAIR_WALK_BAN` in the SAME `self.rep_ban` the incumbent
#     detour uses -- loki_cage's oscillating builder is the precedent.
#
# THE SEVERED-TRUNK OVERRIDE, and it is narrow on purpose.  When
# `_restore_severed` holds -- NOT ONE of our eight sockets carries a conveyor
# outputting into a Core tile, AND every socket tile is in this body's vision so
# the read is evidence rather than an absence of information -- the trunk
# delivers exactly zero, so the two refusals that would otherwise keep the body
# on its own errand are lifted FOR THIS CLASS ONLY: `REPAIR_CHAIN_GUARD` (an
# unfinished chain that terminates on a bricked door is worth nothing) and the
# `self.role != "expand"` gate (the defender and a stood-down raider inside the
# home band are the bodies actually standing there -- Pivot g4: five builders
# alive, `ownsock` 0 from r60 to r184, 10 Ti collected in 184 rounds).  When the
# sockets ARE fed the override is off and every incumbent gate stands.
#
# BUDGET.  `RESTORE_HOLE_MAX` = 6 relays per body, which is `REPAIR_GAP2_MAX`'s
# shape and its number; never before `REPAIR_MIN_RND` (before it an unfinished
# chain looks exactly like a severed one -- 5 of 8 two-wide opens landed before
# r14 while the opening trunk was still being laid); `_eco_spendable` for the
# 3 Ti; and the incumbent `REPAIR_WALK_RNDS` / `REPAIR_WALK_BAN` time-box on the
# walk.  Worst case 18 Ti of conveyor per body, against a belt uptime of 6-7 %
# in the games this plank exists for.
RESTORE_HOLE_ON = False
RESTORE_HOLE_STEPS = 6       # Manhattan reach of the hole detour.  The
                             # incumbent `REPAIR_DETOUR` is 4 and TOP3_Pivot
                             # section 6 asks for exactly one constant deeper
                             # for a SEVERED TRUNK (g1/g4: 67 % / 55 % of holes
                             # stood farther than 4).  6 = at most 6 rounds out.
RESTORE_HOLE_MAX = 6         # per-body ceiling on hole relays (REPAIR_GAP2_MAX)
RESTORE_HOLE_WALK_RNDS = 2 * RESTORE_HOLE_STEPS   # 12.  The time-box on ONE
                             # commitment.  `REPAIR_WALK_RNDS` is 6 and was
                             # sized to `REPAIR_DETOUR` = 4; this class reaches
                             # to 6 and `_rep_tick` does not own every round of
                             # a body's life, so at 6 the commitment expired --
                             # and expiry BANS the tile for `REPAIR_WALK_BAN`,
                             # i.e. the arm wrote off the holes it exists to
                             # fill (6-game _dbg: 30 commitments, 4 relays).
                             # The ban is kept; only the window is resized.
RESTORE_HOLE_HOME_DSQ = RING_WALK_BAND_DSQ   # 64: d <= 8 of a Core tile, the
                             # same home band `BELT_EVICT_HOME_DSQ` uses.
RESTORE_FACE_MAX = 48        # cap on the per-body remembered-facing map.
                             # `REPAIR_LOST_MAX` is 32, so the memory that
                             # actually decides is bounded by the smaller.
RESTORE_LOG = False          # "REP hole/relay" markers.  Off in competition;
                             # the throwaway _dbg build turns it on.

# ---------------------------------------------------------------------------
# INERTNESS.  `bots/leap31_restore_off` is this file with both flags False, and
# it is `bots/leap30_beltevict` (v164) line for line:
#   * `_ring_evict_gate_ok` with `RESTORE_EVICT_ON` False evaluates to
#     `(not gate_on) or self._ring_eco_ready(ct)`, which IS the expression it
#     replaced at both call sites, and `_ring_foe_on_ring` is read on no path;
#   * every plank-B statement is inside a method whose first line is
#     `if not (REPAIR_ON and RESTORE_HOLE_ON): return <typed empty>`, or behind
#     an `if RESTORE_HOLE_ON` clause at its call site;
#   * `_rep_watch`'s facing write is behind `if RESTORE_HOLE_ON`, and its call
#     site in `main.py` keeps the incumbent condition as its first disjunct.
# Proof: DOCTRINE.md "WAVE 31 RESTORE" section 2, the static call-site table.
# ============================================================================


# ============================================================================
# WAVE 32 -- FIXIT.  THREE REPAIRS, THREE FLAGS, ONE CARRIER.
#
# Carrier: `bots/leap30_beltevict` (v164 = v162 + BELT_EVICT + F6 friendly-peck).
# OFF TWIN: `bots/leap32_fixit_off` is this file with TUBE_REPLACE_ON,
# EXIT_GUARD_ON and STICK_ON all False, which is `bots/leap30_beltevict`
# statement for statement -- every added line in raid.py and eco.py is either
# inside a method whose first statement is a flag guard returning the parent's
# answer, or inside an `if <FLAG> ...` clause whose else-branch is the parent's
# own line.  Evidence for all three: `results/wave32/TOP5_DEFECTS.md` (25 games,
# five top-5 opponents, our version 165, 6/25 = 24%).
#
# ----------------------------------------------------------------------------
# FIX 1 -- TUBE_REPLACE_ON.  THE LAST TUBE IS NEVER REPLACED.
#
# DEFECT D3 (measured): a forward tube (our turret at dsq <= 32 of their Core
# span and nearer their Core than ours) is built 3.4 times a game and killed
# 75% of the time at a median age of 22 rounds.  3 247 rounds a corpus
# (130/game) stand with ZERO forward tubes AFTER the first one existed; 14 of
# 25 games END with none alive, mean dead tail 120 rounds; the worst is Pivot
# g4 auroraveil, last tube dead at r151 in a game that ran to r788.
#
# THE HYPOTHESIS THAT WAS FALSIFIED, AND MUST NOT BE RE-FIXED.  The cap is NOT
# the cause.  `LOKI2B_LIVE_CAP_ON` is already True and `_live_fwd_guns`
# (raid.py) is a genuine live census, so a dead tube ALREADY frees its slot --
# which is why one game managed 14 separate tubes.  Nothing here touches the
# cap, the census, or `SLOT_FWD_GUN`'s monotone arithmetic.
#
# THE CAUSE, measured over those same 3 247 zero-tube rounds: a raider stood
# within dsq <= 50 of their Core in 99% of them, but the economy gate
# (`ti >= cost + LOKI_FWD_TI_FLOOR` with LOKI_FWD_TI_FLOOR = 40, and
# `SLOT_HARVESTERS >= LOKI_FWD_MIN_HARV` = 2) would have passed in only 9%.
# The bank test alone blocks 45%, the harvester floor alone 13%, both 33%.
#
# THE BUG.  `SIEGE_MASS_ON`'s discount -- which drops that 40-Ti floor to
# SIEGE_MASS_TI_FLOOR (6) -- is gated `if SIEGE_MASS_ON and n >= 1` in
# `_try_forward_sentinel`.  It therefore cheapens tube 2 and tube 3 and can
# NEVER cheapen the replacement of a dead LAST tube (n == 0), which is exactly
# the state of all 3 247 rounds.  The siege the first tube was bought for is
# still on -- their Core still stands, our raider is still in the band -- and
# the one moment the discount is most justified is the one moment it is
# structurally unreachable.
#
# THE REPAIR.  One `elif` beside the existing discount: when the LIVE census
# says zero tubes stand AND the monotone store says at least one was ever
# built, the same floor drops to the same TUBE_REPLACE_TI_FLOOR.  This is a
# DISCOUNT, never a veto -- the floor only ever moves DOWN, so builds(FIX1 on)
# >= builds(FIX1 off), always, and no tube the parent bought can be refused.
#
# WHY THE TWO-SOURCE TEST IS THE RIGHT ONE, AND WHY IT FAILS CLOSED.  The live
# census is the ONLY thing that can say "no tube stands"; the monotone store is
# the only thing that can say "one existed".  Used together they are exactly
# the replacement predicate and nothing else.  `_live_fwd_guns` returns None
# rather than zero when the body cannot see the siege band (dsq_core >
# LOKI2B_CENSUS_DSQ * 2, or any exception), and the repair requires
# `live == 0` -- a literal integer zero from a census that could see.  A blind
# body gets the parent's 40-Ti floor, so a raider across the map can never read
# its own blindness as "the tube is dead, buy another".
#
# NO RESERVE (THE FUND LESSON, wave 20).  Nothing is saved, banked, earmarked
# or withheld for the replacement.  The tube is funded from the bank that
# exists in the round it is bought, or it is not bought.  FIX 1 adds no store
# write, no slot, no budget and no accumulator.
#
# EVERY OTHER GATE STANDS.  The cap (`n >= LOKI_FWD_GUN_CAP`, read off the LIVE
# census when it can see), `dsq_core(p, E) > 50`, `_cpu_exhausted`, the standoff
# band, `_gd_gun_ok`, `SIEGE_SITE_ON`'s ranking and the nest pick are untouched:
# this section changes a number, not a decision procedure.
#
# THE WALK.  `_t5_nest_walk_target` gates the walk on the SAME bank arithmetic
# so a raider does not leave the collar for a nest the build gate will refuse.
# It carries no discount at all, so with the build gate repaired and the walk
# gate not, the raider could be released to build and still refused the walk
# that puts it beside the nest.  The identical clause is therefore applied
# there, for the identical reason and under the identical flag.
#
# THE HARVESTER FLOOR, ON ITS OWN SUB-FLAG.  The bank is the dominant blocker
# (45% alone, 33% jointly) and TUBE_REPLACE_TI_FLOOR addresses it.  The
# harvester floor blocks a further 13% alone.  `LOKI_FWD_MIN_HARV` = 2 exists
# to stop the siege OPENING before the economy does -- but a replacement is by
# construction not an opening: a tube already stood, so the economy that bought
# it already existed and the floor is being re-asked about a decision it
# already answered.  In the replacement state only, it drops to
# TUBE_REPLACE_MIN_HARV.  This is the one arm here with an economic cost, so it
# is separately ablatable and separately named.
# ----------------------------------------------------------------------------
# FIX 2 -- EXIT_GUARD_ON.  DO NOT BRICK YOUR OWN LAST DOOR.
#
# PORTED VERBATIM from `bots/leap27_exitguard` (wave 27 + its FIX 1), which
# this lineage never received: `grep EXIT_GUARD bots/leap30_beltevict` = 0 hits.
# The rule, the helpers (`_exit_free` / `_exit_ok` / `_exit_refuse` in eco.py),
# EXIT_GUARD_MIN = 1, the fail-open reading of passability and the
# EXIT_GUARD_RAID_ONLY narrowing are the shipped wave-27 text, unchanged.  The
# ten home / economy / opening sites are NOT instrumented on this carrier at
# all (rather than instrumented and stood down), because EXIT_GUARD_RAID_ONLY
# is True and their guard would be a no-op call; EXIT_GUARD_HOME_SITES is kept
# so `_exit_refuse` is line-for-line the wave-27 method.
#
# THE RULE.  Before laying an IMPASSABLE building on tile `t`, count the
# builder's own orthogonal neighbours that are still passable and unoccupied,
# EXCLUDING `t`.  Refuse the build if that count is below EXIT_GUARD_MIN.
# "Impassable" is engine_mechanics G: barrier, harvester, gunner, sentinel,
# launcher, core footprint, wall, and any tile holding a builder body of either
# team.  CONVEYORS AND SPLITTERS OF EITHER TEAM ARE PASSABLE, so the
# belt-laying arms are untouched by this section and are not guarded.
#
# WHY IT IS BACK.  DEFECT D1 (measured on this carrier): 74 dead-idle spans of
# >= 30 rounds, 6 897 idle builder-rounds = 276 a game, 4 909 of them parked at
# the ENEMY Core; 28 of 74 spans (38%) END WITH ZERO FREE ORTHOGONAL EXITS;
# self-blocking builds 1.8 a game (self_block barrier 35, near_block barrier 63,
# self_block sentinel/launcher 8).  Citation: Pivot g4 auroraveil, unit 21
# bricks (12,2) at r173 from (11,2) and is then dead-idle r178-425 -- 248
# rounds -- at free_orth 0 with a median bank of 46 Ti.
#
# EVIDENCE IT WORKS, AT ZERO COST: `results/wave28` F3 = REAL, -93% self-bricked
# exits; wave-27 batch 2 went 20/21 and 25/25 wins with the guard in.
#
# WHAT IT IS NOT.  A pure REFUSAL on an existing build: no new arm, no new
# target, no new titanium, no new ordering.  A refused tile falls through to the
# NEXT candidate inside the same loop, so an arm is never killed -- it just does
# not spend its own last door.  It does NOT give the parked body something to
# do; `LOKI_QUIET_ON` (the core peck) stays True and untouched, exactly as
# wave 27 left it.
# ----------------------------------------------------------------------------
# FIX 3 -- STICK_ON.  A SOCKET WE OWNED AND LOST OUTRANKS A NEW ONE.
#
# DEFECT D2 (measured): our barriers inside dsq <= 12 of their Core -- the
# ring-12 collar -- are built 221 times over 25 games (8.8/game) and destroyed
# 95 times (43%, 3.8/game) at a median destroyed-lifetime of 44 rounds.  Their
# barriers on OUR ring: 192 built, we killed 61 (32%).  They de-brick at 1.34x
# our rate, and the two teams that beat us 4-1 and 5-0 head the table (Jython
# 60% of our seals, Pantheon 48%).  53 of the 95 destroyed sockets are re-laid
# (56%, median gap 22 rounds) and 42 (44%) NEVER are.
#
# AND THE 56% IS INCIDENTAL.  `_collar_act` computes `reseal = key in
# self.col_bricks` AFTER the build and uses it for a log print and nothing
# else: `order = free` promotes only RATCHET tiles.  NOTHING IN THE TREE RANKS
# A SOCKET WE OWNED AND LOST.  The re-brick happens when the ring scan's
# cardinal order happens to reach the hole again.  This is INTEL #5's never-
# built STICK half.
#
# THE REPAIR, at the one place it belongs (`_collar_act`'s BRICK/RESEAL block):
# `stickfree = [t for t in free if (t.x, t.y) in self.col_bricks]` and the order
# becomes `ratfree + stickfree + rest`, with the collar's titanium budget waived
# for a stick tile the way RAT_BRICK_WAIVE already waives it for a ratchet tile.
# `self.col_bricks` is the tree's EXISTING memory of "this seat carried one of
# ours" -- written both on our own build (raid.py, the BRICK/RESEAL block) and
# on sight of our barrier on an adjacent seat -- so a socket that is in
# `col_bricks` and is ALSO in `free` (no building, no body) is by definition one
# we owned and lost.  No new census, no new scan, no new comm slot.
#
# THE BODY IS ALREADY THERE.  Every tile in `free` is a CARD_DELTAS neighbour of
# the collar body's own position, so STICK re-ranks four tiles the body could
# already build on this round.  It cannot recall a body, cannot move one, cannot
# walk one off their ring: THE PLUG RULE is untouched because no motion exists
# in this fix.
#
# THE CAP IS ON THE WAIVER, PER BODY.  `col_bricks` is per-unit state (a dead
# raider loses the memory; team-wide memory would need a comm slot, which this
# fix does not open), so the cap is per-unit too: STICK_MAX_RELAYS budget-waived
# relays per body per game.  Past the cap STICK still RE-RANKS -- ordering costs
# nothing -- it just stops waiving `_collar_afford`, i.e. it falls back to the
# parent's own budget.
#
# NEVER IN THE TERMINAL WINDOW.  Below STICK_MIN_CORE_HP their Core is about to
# fall and 3-5 Ti belongs in damage, not in a seat whose denial has no time left
# to pay.  Read from `_tw_core_hp`, which returns None when no footprint tile is
# in vision -- unknown does NOT refuse, so a body that cannot see the Core keeps
# the fix.  A collar body is orthogonally adjacent to their ring and sees a
# footprint tile essentially always.
#
# ----------------------------------------------------------------------------
# CONFLICTS, CHECKED PAIRWISE.
#
# FIX1 x FIX2.  They meet at the three sentinel build lines of
# `_try_forward_sentinel` (the nest build, the ranked post, the fallback post).
# FIX1 only lowers `ti_floor`; FIX2 only refuses a POST that would cost the
# builder its last exit, and a refused post falls through to the next candidate
# in the same CARD_DELTAS loop.  Neither reads the other's state.  The
# composition is "buy more often, and never onto your own last door" -- FIX2 can
# reduce the number of admissible posts to zero on a fully walled-in body, which
# is a body that could not have used the tube anyway.
#
# FIX1 x FIX3.  Disjoint code, disjoint money paths.  FIX1 spends the GLOBAL
# bank through `_try_forward_sentinel`'s own floor; FIX3 spends inside
# `_collar_act` under `_collar_spend` / `_collar_afford`, the collar's own
# budget.  The only shared quantity is `ct.get_global_resources()`, and the
# ordering already in the tree (`_raid_act` step 0 is the collar, step 3 is the
# forward sentinel) is unchanged: the collar was always first and a 3-5 Ti
# barrier was always able to precede a tube.  FIX3 adds at most
# STICK_MAX_RELAYS waived barriers per body over a whole game against a tube
# floor of TUBE_REPLACE_TI_FLOOR.
#
# FIX2 x FIX3.  They meet on one line: the collar's `collar_brick` site.  FIX3
# decides WHICH free seat is tried first; FIX2 decides whether the seat being
# tried may be bricked at all.  FIX2 runs INSIDE the `for t in order:` loop, so
# a stick tile that would seal the body in is refused and the loop advances to
# the next candidate -- the ordering is preserved and the refusal is preserved.
# They cannot deadlock: FIX2's refusal is a `continue`, never a `return`.
#
# NONE OF THE THREE touches `LOKI_QUIET_ON`, `SLOT_FWD_GUN`'s arithmetic, the
# belt, BELT_EVICT, F6, the opening, or any comm slot.  No new store write of
# any kind is added by wave 32.
# ============================================================================

# --- FIX 1 -----------------------------------------------------------------
TUBE_REPLACE_ON = True       # MASTER.  False == bots/leap30_beltevict (v164).
TUBE_REPLACE_TI_FLOOR = SIEGE_MASS_TI_FLOOR   # 6.  The SAME floor tube 2 and
                             # tube 3 already get; the repair is that n == 0
                             # can reach it, not that a new number exists.
TUBE_REPLACE_HARV_ON = True  # sub-arm: the harvester floor also relaxes in the
                             # replacement state.  Separately ablatable because
                             # it is the only arm here with an economic cost.
TUBE_REPLACE_MIN_HARV = 1    # ...to this.  Not 0: a side with no harvester at
                             # all is not besieging anything.
TUBE_REPLACE_LOG = False     # `TUBEREP` markers, off in competition.

# --- FIX 2 -----------------------------------------------------------------
EXIT_GUARD_ON = False        # MASTER.  False == bots/leap30_beltevict (v164),
                             # line for line: every call site is a single
                             # `if self._exit_refuse(...)`, and `_exit_refuse`
                             # returns False on its own head guard.
EXIT_GUARD_MIN = 1           # free orthogonal exits the builder must keep
EXIT_GUARD_LOG = False       # `EXITGUARD refuse` markers, off in competition
EXIT_GUARD_RAID_ONLY = True  # wave-27 FIX 1: stand down at the home sites.
                             # On this carrier the home sites are not
                             # instrumented at all, so this is belt and braces.
EXIT_GUARD_HOME_SITES = frozenset((
    "sg_fill",          # eco `_sg_fill`      -- our own Core's sockets
    "expand_harv",      # eco `_expand`       -- the ore tile it walked to
    "op_trunk_harv",    # opening `_op_trunk` -- the trunk terminus, one tile
    "op_pair",          # opening `_op_pair`  -- the opening sentinel
    "rg_gun",           # main `_rg_gun`
    "counterbattery",   # main `_try_counterbattery`
    "launcher_corner",  # main `_try_build_launcher`, the Core corner
    "launcher_card",    # main `_try_build_launcher`, the cardinal fallback
    "sg_ring_gun",      # main `_sg_ring_gun`
    "t5_home_gun",      # main `_t5_home_gunner`
))

# --- FIX 3 -----------------------------------------------------------------
STICK_ON = False             # MASTER.  False == bots/leap30_beltevict (v164).
STICK_MAX_RELAYS = 8         # budget-waived relays per BODY per game.  Past
                             # this the re-ranking survives and only the waiver
                             # stops -- STICK never becomes a veto.
STICK_MIN_CORE_HP = 100      # never re-brick below this seen Core HP
STICK_LOG = False            # `STICK relay` markers, off in competition.
