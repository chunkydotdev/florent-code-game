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
# INSERTION DEFENSE.  Measured in the v55 0-5 ladder loss to CtrlAltDefeat
# (match e40a6c01, all five games decoded): Launcher at r1, 2-3 builders
# thrown at our Core by r2, first sentry planted at median r11 at core-dist^2
# 10-41, first Core hit r12, Core dead at median r361.  Three independent
# gaps let it through:
#   1. GEOMETRIC -- the hunt band reused INTRUDER_CORE_DSQ (20), but a
#      Sentinel's range is r^2 = 32: a turret can shell the Core from
#      outside the band entirely (observed at dist^2 25 and 41).  The band
#      for HUNTING is therefore its own constant, sized past Sentinel range
#      and measured to the nearest tile of the 2x2 footprint, not the anchor.
#   2. TEMPORAL -- HUNT_MIN_RND blocked the two games where a builder stood
#      within designation range of an in-band sentry from r3 and r20.  An
#      early-hunt waiver on big maps was BUILT AND REFUTED by ablation
#      (kladde eider 8/16 -> 0/16 with the waiver on, 8/16 with only it
#      off): pre-r120 hunting relocates the fjordgate disease to any map --
#      builders peck turrets instead of running the economy.  The pre-r120
#      answer to an inserted raider is the interceptor BODY-BLOCK (see
#      _intercept): builders are mutually impassable and raiders WALK their
#      last tiles (throws reach only r^2 <= 26), so standing in the doorway
#      costs zero Ti and no action, and cannot be traded against economy.
#   3. POPULATION -- the biggest: our builder count collapsed 5 -> 1-4 in
#      every game and the converged-healer seats were simply dead (379
#      consecutive unhealed siege rounds in game 5) while the respawn gate
#      demanded ti >= 250 from a bank pinned at 2-12 Ti.  Siege-mode respawn
#      below (SIEGE_SPAWN_*) funds bodies at exactly the moment the standing
#      floor forbids it: a 30-45 Ti replacement is +4 HP/round of heal
#      capacity against a 9 HP/round sentinel, and it only fires while the
#      Core is provably bleeding for consecutive rounds, so no other game
#      class ever sees the relaxed floor.
HUNT_BAND_DSQ = 41
HUNT_EARLY_MIN_AREA = 150
SIEGE_HURT_RNDS = 4
SIEGE_SPAWN_MARGIN = 10

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
            under = bool(last and rnd - last < 35)
            ct.write_store(SLOT_UNDER, 1 if under else 0)

        harv = ct.read_store(SLOT_HARVESTERS)
        if harv >= ECO_NEED:
            ct.write_store(SLOT_ECO_READY, 1)

        ti, ammo = ct.get_global_resources(), ct.get_global_ammo()

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
        ti_floor = 12 if (under or weapons) else 52
        # CONVERTER/SPAWNER RESERVE AGREEMENT.  The cad_probe build surfaced
        # this failure shape: a converter floor below the spawner's threshold
        # means the bank oscillates in the dead zone between them and no
        # builder is ever spawned again (measured there: 0 spawns after r4 in
        # a 405-round game).  Our own pair had exactly that shape -- floor 12
        # under siege vs siege-respawn's cost+SIEGE_SPAWN_MARGIN (~40-80
        # scaled) -- i.e. the converter was starving the one mechanism built
        # to fix the population collapse.  While the Core is actively
        # bleeding, the spawner's claim comes first and conversion takes only
        # the excess: a replacement healer (+4 HP/round, permanent) outvalues
        # its price in ammo, and conversion resumes the round after the spawn
        # is funded.
        if ct.get_hp() < ct.get_max_hp():
            ti_floor = max(ti_floor, ct.get_builder_bot_cost() + SIEGE_SPAWN_MARGIN)
        if (under or weapons or harv >= 2) and ammo < ammo_target and ti > ti_floor:
            amt = min(16, ammo_target - ammo, ti - ti_floor)
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

        # SIEGE-MODE RESPAWN (see INSERTION DEFENSE, gap 3).  The Core reads
        # its own HP bar directly -- no store round-trip -- and counts
        # consecutive bleeding rounds; a heal back to full resets the count,
        # so a long-ago-scarred Core does not qualify.  While the siege
        # holds, a replacement seat needs only the spawn's own price plus a
        # small margin, instead of the 250-Ti standing floor that gap-3
        # measured as unmeetable (banks of 2-12 Ti at death in 4/5 games).
        if ct.get_hp() < ct.get_max_hp():
            self.hurt_rnds = getattr(self, "hurt_rnds", 0) + 1
        else:
            self.hurt_rnds = 0
        under_siege = self.hurt_rnds >= SIEGE_HURT_RNDS
        replace_floor_ok = (
            (ti >= REPLACE_TI_FLOOR and rnd >= REPLACE_MIN_RND)
            or (under_siege and ti >= ct.get_builder_bot_cost() + SIEGE_SPAWN_MARGIN)
        )

        if (
            self.n < spawn_budget
            and (self.n < spawn_cap or replace_floor_ok)
            and can_spend_spawn and ti >= ct.get_builder_bot_cost()
        ):
            cands = ring(p, 2)
            # Dead branch removed: a first-builder enemy-facing sort keyed on
            # SLOT_ENEMY_CORE, written and read in the same round-0 turn, so the
            # buffered store always unpacked None.  Activating it measured 41%.
            # Stable dispersion makes paired offline results reproducible.
            cands.sort(key=lambda sp: ((sp.x * 17 + sp.y * 31 + self.n * 13) % 97, sp.y, sp.x))
            for sp in cands:
                if 0 <= sp.x < w and 0 <= sp.y < h and ct.can_spawn(sp):
                    ct.spawn_builder(sp)
                    self.n += 1
                    return

        # Cores cannot construct turrets; the defender consumes SLOT_THREAT and
        # owns all counterbattery placement.

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
        if ct.get_global_resources() < ct.get_launcher_cost():
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

        for eid in ct.get_nearby_entities():
            if ct.get_team(eid) == self.team:
                continue
            et = ct.get_entity_type(eid)
            ep = ct.get_position(eid)
            if et == EntityType.CORE:
                self.enemy = ep
                ct.write_store(SLOT_ENEMY_CORE, pack_pos(ep))
            d = self.core.distance_squared(ep)
            if (et in (EntityType.GUNNER, EntityType.SENTINEL) and d <= 64) or (
                et == EntityType.BUILDER_BOT and d <= 16
            ):
                ct.write_store(SLOT_UNDER, 1)
                ct.write_store(SLOT_ATK_RND, ct.get_current_round())
                ct.write_store(SLOT_THREAT, pack_pos(ep))

        self.enemy = unpack_pos(ct.read_store(SLOT_ENEMY_CORE))
        self._sync_harvesters(ct)

        # The Launcher acknowledges the exact bot it threw.  Without this
        # handshake, a short intermediate throw leaves a launch-wait bot trying
        # to walk home, and nearest-bot selection can steal the economy builder.
        if ct.read_store(SLOT_LAUNCHED_ID) == ct.get_id() + 1:
            self.dropped = True
            self.role = "saboteur"

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
        # See ROUND FLOOR above -- and INSERTION DEFENSE gap 2 for the waiver:
        # on any map bigger than fjordgate's class, an active Core siege (the
        # _core_shelled gate below) is reason enough to hunt from round 0.
        # The floor still owns the turn on tiny maps, where "near the Core"
        # is the whole board and the measured winning line was offense.
        if ct.get_current_round() < HUNT_MIN_RND:
            return False
        # The exact siege gate convergence and the universal heal already use:
        # the loose proximity flag AND direct evidence off the Core's HP bar.
        # Cheap store read first, so the scans below never run on a quiet map.
        if ct.read_store(SLOT_UNDER) == 0:
            return False
        # Nothing has been written yet, so bailing here is a clean no-op that
        # degrades to exactly the pre-existing behaviour (heal / converge).
        if self._cpu_exhausted(ct):
            return False
        if not self._core_shelled(ct):
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
            # INSERTION DEFENSE gap 1: the band is sized past Sentinel range
            # (r^2 = 32) and measured to the nearest tile of the 2x2
            # footprint -- the anchor alone under-measures by up to 2 tiles
            # diagonally, which is exactly how the observed dist^2 25-41
            # sentries sat outside the old INTRUDER_CORE_DSQ = 20 band.
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
            if healers < HUNT_MIN_HEALERS and hp > HUNT_FINISH_HP:
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
        # Mirror of _plan_siege's economy gate: the first emergency battery is
        # free, any further one waits for income.  Ungated, opening threat noise
        # on close-anchor maps buys three fixed-facing Sentinels aimed at
        # transient spawn tiles before the first harvester exists.
        if ct.read_store(SLOT_HOME_GUN) >= 1 and ct.read_store(SLOT_HARVESTERS) < ECO_NEED:
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
                if self.link_queue and ti >= ct.get_conveyor_cost():
                    if self._build_next_link(ct):
                        return
                # Wake the Launcher subsystem: v58's call site, deleted in the
                # v63 rework, restored here. _try_build_launcher() claims
                # SLOT_LAUNCHER before building, so this fires at most once.
                if harv >= ECO_NEED and self._try_build_launcher(ct):
                    return
                if harv < self._eco_cap(ct) and ti >= ct.get_harvester_cost() and self._try_harvester(ct, harv):
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
        if self.role_n == 1 and self._intercept(ct):
            return

        has_launch = ct.read_store(SLOT_LAUNCHER) != 0
        harv = ct.read_store(SLOT_HARVESTERS)
        allow_pave = has_launch or harv >= 2

        if ct.get_action_cooldown() == 0:
            if self.link_queue and self._build_next_link(ct):
                return
            if ct.get_global_resources() >= ct.get_harvester_cost() and harv < self._eco_cap(ct):
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
            if (
                ct.get_global_resources() >= MEDIC_TI_FLOOR
                and ct.get_current_round() >= MEDIC_MIN_RND
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
                            and ct.get_hp(bid) < ct.get_max_hp(bid)
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
        for eid in ct.get_nearby_buildings():
            if ct.get_team(eid) != self.team:
                continue
            bp = ct.get_position(eid)
            d = bp.distance_squared(tp)
            if d > 4:
                continue
            k = (0 if ct.get_hp(eid) < ct.get_max_hp(eid) else 1, d, eid)
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
        if guard is not None:
            # A victim building to escort: unchanged v53 repair-escort logic.
            if abs(p.x - guard.x) + abs(p.y - guard.y) == 1:
                if ct.get_action_cooldown() == 0:
                    if ct.can_heal(guard):
                        ct.heal(guard)
                    else:
                        self._heal_adjacent(ct)
                return True
            if ct.get_move_cooldown() == 0:
                self.tgt = guard
                self._nav(ct, pave=False)
            return True

        # BODY-BLOCK, not pursuit (ladder-scouted tactic, Magnus 2026-08-07;
        # adopted for the CtrlAltDefeat insertion counter).  A builder cannot
        # attack a unit, so walking AT a raider never stops it -- but builders
        # are mutually impassable, and every decoded insertion raider WALKS
        # its final tiles toward our Core (Launcher throws reach only
        # r^2 <= 26).  So the interceptor stands in the doorway instead: the
        # tile one cardinal step from the raider TOWARD our Core.  Costs no
        # titanium and no action; the raider's only counter is to path
        # around, which we re-block next round -- every such detour round is
        # a round its sentry is not being built.  If the doorway is a wall,
        # a building, or already behind the raider, fall back to the old
        # chase so the trail-cold bookkeeping above keeps working.
        door = None
        step = tp.cardinal_direction_to(nearest_core_tile(tp, self.core))
        if step != Direction.CENTRE:
            cand = tp.add(step)
            if cand.x == p.x and cand.y == p.y:
                door = cand
            else:
                try:
                    if ct.is_in_vision(cand) and ct.is_tile_passable(cand):
                        door = cand
                except Exception:
                    door = None
        if door is not None and p.x == door.x and p.y == door.y:
            # Holding the doorway.  The move is the job; spend the action on
            # whatever is useful from here -- peck a building the raider
            # planted beside us, else patch neighbours.
            if ct.get_action_cooldown() == 0:
                if ct.can_fire(tp):
                    ct.fire(tp)
                else:
                    self._heal_adjacent(ct)
            return True
        goal = door if door is not None else tp
        if goal is tp and abs(p.x - tp.x) + abs(p.y - tp.y) == 1:
            # Beside the raider itself with no doorway to take: act and hold.
            # Never nav from here -- _bfs_direction would aim at the occupied
            # tile, can_move would refuse it, and _nav's fallbacks would
            # slide us off the target.
            if ct.get_action_cooldown() == 0:
                if ct.can_fire(tp):
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
        if not self.link_queue or ct.get_global_resources() < ct.get_conveyor_cost():
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
        nxt = ct.get_position().add(d)
        if not (0 <= nxt.x < self.mw and 0 <= nxt.y < self.mh):
            return False
        # Pave toward core, but still attempt move (don't treat pave-only as success)
        if pave and self.core and ct.is_tile_empty(nxt) and ct.get_action_cooldown() == 0:
            if ct.read_store(SLOT_HARVESTERS) >= 1 and ct.get_global_resources() >= ct.get_conveyor_cost():
                if dist_core(nxt, self.core) > 0:
                    here = ct.get_position()
                    if abs(nxt.x - self.core.x) + abs(nxt.y - self.core.y) < abs(here.x - self.core.x) + abs(here.y - self.core.y):
                        card = nearest_cardinal(nxt.direction_to(nearest_core_tile(nxt, self.core)))
                        if ct.can_build_conveyor(nxt, card):
                            ct.build_conveyor(nxt, card)
        if ct.can_move(d):
            ct.move(d)
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
