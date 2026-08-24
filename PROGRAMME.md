# ACTIVE PROGRAMME — machine-readable. `tools/gate.py` reads this and refuses off-programme batteries.

Edit this file ONLY on an explicit directive from Magnus. Both arms and every
successor session inherit it. The fields below are parsed; the prose is not.

    LINE: loki
    LINE_DIRS: bots/_v105loki1 bots/_v10?loki* bots/_v1??loki* bots/_v1[3-9]?* bots/_v[2-9]??*
    INCUMBENT: bots/_v542wave
    # s58 2026-08-24 ~11:0xZ: SHIPPED as platform v213 "Loki rc543.1" (= this
    # tree + the 15-map catalogue), Magnus's explicit word, displacing x3r0's
    # v188 at his order. STOP-LOSS: rating <= 1789 (baseline 1829 - 40)
    # -> restore v188 by integer. Ship watch armed on the elo tape.
    INCUMBENT_FROZEN: no
    PREVIOUS_INCUMBENT: bots/_v537socket
    BASELINE: bots/_x3r0v168mjolnir
    PRIMARY_CURRENCY: game_share
    SECONDARY_CURRENCY: kill_speed_score
    KILL_SPEED_SHIP_GATE: -1.76
    KILL_SPEED_MIN_N: 200
    KILL_SPEED_IS_LEG_VERDICT: no
    WIN_RATE_IS_VERDICT: yes
    COMPARE_AGAINST: previous_line_iteration
    KILL_WINDOW_RND: 250
    R1000_IS_DEFEAT: yes
    PLAY_DEFENCE: not_at_the_kill_s_expense
    DEFENCE_ADMISSION_BAR: r300_crossing_non_regression
    FOCUS: fortress_eco_defence_magnus_2026-08-22_builders_never_raid
    CITADEL_ZONE: chebyshev_3_of_core_footprint
    CITADEL_BAR: every_enemy_unit_entering_zone_destroyed_funding_unconstrained
    CITADEL_ECON_RIDER: maintain_economy_his_own_words
    FORTRESS_NO_RAID: builders_never_leave_home_territory_until_r300
    FORTRESS_RESPONSE: all_builders_destroy_intruding_raiders
    FORTRESS_DEMOLITION: enemy_buildings_in_our_territory_destroyed_launchers_barriers_everything
    FORTRESS_GOAL: eco_and_defence_optimized_to_the_absolute_edge
    FORTRESS_PHASE_FLIP: r300_two_raiders_sentinel_siege_until_enemy_core_down
    FORTRESS_R1000_QUESTION: RESOLVED_Q3_phased_kill_see_block_below
    CITADEL_WEAPON: turret_ring_magnus_2026-08-22_launcher_taxi_rejected_wants_them_gone_forever
    CITADEL_TARGET_ORDER: raider_first_then_gunners_remove_collar_barriers_magnus_2026-08-22
    BELT_DOCTRINE: everything_allowed_to_keep_belts_alive_interference_destroyed_safety_measures_once_online_magnus_2026-08-22
    HEIMDALL_FIXTURES: F1_baltsars_v542wave__F2_mjolnir_noiseoff__F3_sleipnir_v2_v488beltbreak2_magnus_2026-08-22
    HEIMDALL_FIXTURE_BAR: defend_remove_raiders_rebuild_until_r300_then_win
    SESSION_MODE: max_subagents_keep_builder_context_clean_magnus_watching_2026-08-22
    HEIMDALL_VICTORY_CONDITION: beat_sleipnir2_AND_baltsars_AND_current_slot_before_anything_else_magnus_2026-08-23
    HEIMDALL_VICTORY_BAR: majority_wins_per_fixture_16_of_30_each_under_v21_screens
    HEIMDALL_TACTIC_LOCK: eco_and_defence_to_r300_then_rotate_and_destroy_exploration_free_within
    HEIMDALL_PRIO_LADDER: p0_expand_eco_and_defence__p1_destroy_raiders__p2_destroy_enemy_turrets__p3_rebuild_preserve_eco_until_r300_magnus_2026-08-22
    HEIMDALL_PREDICTION: predict_their_moves_and_targets_to_react_quickly_magnus_2026-08-22
    KILL_TARGET_STATUS: superseded_for_heimdall_line_by_phase_flip_kill_lands_after_r300_by_design
    FIXTURE_OF_RECORD: live_unrated
    ALWAYS_BE_RUNNING: yes
    QUEUE_FLOOR: 3
    QUEUE_OWNER: research
    TARGET_MIN_PAYOUT: 10
    SHIP_SIT_MIN_K: 8
    X3R0_SLOT_RULE: superseded_2026-08-20_by_ship_bar_joint_amendment_no_residual_scope
    SLOT_STOP_LOSS: off
    SHIP_BAR: beat_live_holder_screen_ci_excl_50_AND_full_pool_vs_x3r0best_ci_lower_ge_53.3
    STEALTH_UNTIL_DROP: yes
    STEALTH_PREDROP_RIDER: unrated_first_contact_testing_authorized_magnus_2026-08-21_full_predrop_ruling_drop_stealth_otherwise_intact
    KILL_TARGET: median_r180_share_by_r200_floor_r300
    NEXT_LINE: skalman
    NEXT_LINE_DOCTRINE: beancounters_replication_then_amplify
    NEXT_LINE_BENCHMARK: bots/_v542wave
    NEXT_LINE_SCREEN_LADDER: benchmark_then_current_holder_then_sleipnir_v2_magnus_2026-08-21
    NEXT_LINE_EXPERIMENTS: open_magnus_2026-08-22_r1000_still_defeat_no_rush
    RUSH_LINE_STATUS: sunset_2026-08-21_magnus_directive_v177_holds_slot_until_displaced

## FORTRESS DOCTRINE 2026-08-22 (Magnus, s57, in-session, later the same evening — verbatim: "Don't send our builders on raid missions, we will work on eco and defence, how can we optimize them to the absolute edge of what can be done? Any raiders trying something, all builders are to destroy them, any enemy buildings should also be destroyed, launchers, barriers, everything")

Extends the citadel block below. Operational form, typed by the builder:
(1) **BUILDERS NEVER RAID** — no cage-walker march, no forward tubes built by
travelling engineers, no forward ore denial: all four bodies work the home
territory ("home territory" operationalized as the HOME HALF pending Magnus's
word — challenge-this, same class as the Chebyshev choice). (2) **ALL builders
are intruder-responders** — a raider in our ground is destroyed by whoever is
in reach, not by one assigned role. This RESOLVES the earlier raider-vs-unit
challenge-this: raiders die AND (3) **enemy BUILDINGS in our territory are
demolished — launchers, barriers, everything** (his enumeration). (4) **ECO +
DEFENCE TO THE ABSOLUTE EDGE** — the optimization target is measurable:
titanium delivered per round (the belt ceiling on home ore), core damage taken,
intruder survival time, enemy-structure dwell time in our half.
✅ **Q3 RESOLVED BY MAGNUS, same evening — verbatim: "until round 300 our
entire focus is eco, then we send two raiders that puts up as many sentinels
as necessary to bring the enemy core down."** The doctrine is PHASED, not
turtled: r0–300 pure eco + fortress defence; at r300 TWO raiders travel and
build a sentinel battery that kills the enemy core. Consequences, typed by
the builder: (1) **R1000_IS_DEFEAT STANDS** — the win is still core
destruction, deliberately late; tiebreaks remain a failure mode, and every
screen reports the post-r300 kill's actual landing round. (2) **KILL_TARGET
(median_r180…floor_r300) is SUPERSEDED for the Heimdall line** — the plan
kills after r300 by design; the line's kill metric is siege-phase time-to-core
(r300 → core down). (3) **DEFENCE_ADMISSION_BAR's r300 form is likewise
inapplicable to this line** (it priced defence against a sub-r300 kill that
this line does not attempt); its successor bar is: the fortress must SURVIVE
to r300 (our-core-alive-at-r300 share) and the siege must CLOSE (share of
games with enemy core down by r600, reported honestly). The original text of
the superseded collision question is preserved below for provenance.
⚠ *(superseded original)* Q3 as first flagged: this doctrine and
R1000_IS_DEFEAT collide. A bot whose builders never raid generates almost no
checkmate pressure; its games will reach r1000 often, where key 1
(titanium_collected) — which this doctrine MAXIMIZES — decides 94% of
tiebreaks in our favour by construction. Readings: (a) development-phase
exemption (build the fortress, measure the edge, the kill verb returns later
on top of it); (b) the tiebreak road is being deliberately REOPENED (reversing
the R1000_IS_DEFEAT clause for this line). The builder proceeds under reading
(a) — it requires no reversal of standing doctrine and the work is identical
for a long way — but the ruling is Magnus's, and every screen of this line
will report r1000 shares honestly rather than hiding them. **The same ruling
also settles `KILL_TARGET` (median_r180_share_by_r200_floor_r300): under
reading (a) it is DORMANT for the fortress development phase; under (b) it is
DEAD — named here so one ruling closes both fields and no successor trips on
a stale constant.**
Game context: in-game Florent Code League doctrine.

## FOCUS NARROWED TO THE CITADEL PERIMETER 2026-08-22 (Magnus, s57, in-session — verbatim: "I think we're trying to do everything at the same time, what if we start at one thing, can we make a defence and maintain economy? Spend everything we need on defence, i want every single raider destroyed that 3 squares from our core.") — EXTENDED BY THE FORTRESS BLOCK ABOVE, same evening

Operational form, typed by the builder for the record: (1) ONE THING AT A TIME —
the citadel package outranks every other build front until it measures; other
fronts (v630 tube-guard POWERED READ — its already-running SCREENS complete
and bank, the powered read is what holds — CRASHREP-BC, the field panel) HOLD
unless Magnus says otherwise. (2) THE ZONE: enemy units within Chebyshev 3 of
our 2x2 core footprint (the raider annulus; "3 squares" operationalized as
board distance — challenge this line if he meant something else). (3) THE BAR:
every enemy unit entering the zone is destroyed — ⚠ HIS NOUN WAS "RAIDER";
"every enemy UNIT" is the builder's widening (a planted point-blank gunner is
surely inside the intent, but the word is mine, not his — challenge this line
too if raiders-only was meant) — the metric is intruder survival
time and share destroyed, plus core damage taken; funding for the response is
explicitly unconstrained BY HIS WORDS ("spend everything we need"), with the
economy maintained (his same sentence). (4) The DEFENCE_ADMISSION_BAR (r300
checkmate non-regression) still governs SHIPPING; building and screening the
citadel is what the focus buys. R1000_IS_DEFEAT stands — the citadel exists so
our own checkmate lands, not so games reach tiebreaks.
Game context: in-game Florent Code League doctrine.

## FOCUS SET TO DEFENCE 2026-08-22 (Magnus, s56, in-session — verbatim: "So lets focus on defense, we just can not win by round 1000") — NARROWED BY THE CITADEL BLOCK ABOVE, same day

Read with both existing clauses intact: **R1000_IS_DEFEAT stands** (his own sentence
re-affirms it — the tiebreak road stays retired) and **DEFENCE_ADMISSION_BAR is
unchanged** (a defence plank is off-programme if it pushes checkmates past r300).
What moves is PRIORITY: the build front is now the COPY 6 class — the home-answer
half of the Bean-counters doctrine that the benchmark plateau isolated (their
home-ring clearance 76.6-79.7% vs ours 20.8-42.8%; their answer latency 4-8 rounds
at 70-91% vs ours 10-13 at 43-57%; s56 benchmark readout + DECODE-firstcontact
§3.1/§4.4). Defence here means SURVIVING THE r150-250 WINDOW SO OUR OWN CHECKMATE
LANDS — the s31 scope sentence, now as the focus rather than the side-condition.
Game context: in-game Florent Code League doctrine.

## NEXT_LINE_EXPERIMENTS OPENED 2026-08-22 (Magnus, s54, in-session — verbatim: "You're free to experiment as much as you want, but a win at r1000 is still a loss and we dont want to build a rush bot")

**The ruling, in context:** given after the launcher dose table (v611: parity axis moves
hard, currency does not follow at that design) and the two-fixture evidence chain. The
experimentation gate is OPEN — including phase-2 verbs like the home launcher — with the
two standing constraints RE-AFFIRMED in the same sentence: **`R1000_IS_DEFEAT` stands**
(a stall converted is not a win bought; kills remain the currency of every verdict) and
**no rush doctrine** (the no-rush course confirmed 2026-08-21 remains the line's shape —
experiments extend the strangle-then-kill machine, never revive the raider opening).
Adoption discipline unchanged: experiments ship into defaults only on the measured
currency (F1 by-r300 gate + F2 transfer), same as every wave so far.

## NEXT_LINE_SCREEN_LADDER ADDED 2026-08-21 (Magnus, s54, in-session — verbatim: "If we finally find something that beats our benchmark bot we will also need to run it against the current slot and sleipnir v2, but that's only if we actually beat the benchmark bot we put up.")

**The post-benchmark screening ladder, conditional and ordered:** a Skalman version that
BEATS `NEXT_LINE_BENCHMARK` (bots/_v542wave) is then screened against **(2) the CURRENT
SLOT HOLDER's bytes** (read the holder from `fcode status` at screen time — currently
x3r0's v176 "Mjolnir rotfix", whose tree is NOT yet imported locally; import-on-need per
the version_trees 2-minute pattern — local x3r0 trees stop at v175carrier) and **(3)
Sleipnir v2 = `bots/_v488beltbreak2`**. Neither downstream screen fires unless the
benchmark is actually beaten — the ladder is conditional by his phrasing. This sequences
LOCAL screens; the FIRST CONTACT unrated cells (BC mirror / Pivot / kladde, authorized
pre-drop by the exposure ruling below) are a separate surface with their own gates.

## STEALTH_PREDROP_RIDER ADDED 2026-08-21 (Magnus, s54 — exposure ruling on the explicit question)

**The question put to Magnus (research s54, in-session, coordination tail 19:29:10Z):**
does `STEALTH_UNTIL_DROP` hold at screen-clear, or does a live window open for the new
line's first-contact testing? Options offered: stealth-holds / mirror-only carve-out /
full pre-drop. **Magnus selected FULL PRE-DROP TESTING: all three FIRST CONTACT cells
(BC-v68 mirror pinned · Pivot counter-check pinned · kladde clock unpinned) fire as soon
as a Skalman version clears the local screen.** Recorded here because this file is
edit-on-his-directive-only and a successor must see WHY a parsed field changed in the
file itself.

**Scope, exactly as asked and answered:** pre-drop UNRATED testing of screen-clear
Skalman versions is authorized. **Release/submission/drop stealth is otherwise intact** —
the rider does not touch the coordinated-drop half of `STEALTH_UNTIL_DROP`, which stands.
The remaining first-contact gates are the builder's: (1) a version clears the local
screen (declaration of record required — v602's 6/30 is declared NOT MET), (2) the
activation-window pricing under the 10-min cadence.

**Provenance note, surfaced not resolved:** the s51 stealth field was set jointly by
Magnus + x3r0; this rider is Magnus solo (2026-08-21). Squaring it with x3r0 is his
conversation, no lane's.

## NEW LINE DECLARED 2026-08-21 (Magnus, s53 — verbatim in the coordination tail at ~15:5xZ: build our own version of the Bean counters tactics; basics first, then amplify our specialities; the end for two rushed raiders and Baltsars banditer; wrap when the playbook lands; next session starts from scratch)

**The next line is `SKALMAN` (builder's naming call under Magnus's "popular Swedish kid
show" instruction): Skalman from Bamse — the methodical genius turtle who carries
everything he needs in his shell, runs his life on an exact clock, and is the smartest
one in the forest.** The fit is the doctrine: the shell = the barrier cage and the clean
home ring; the clock = the drip-convert rhythm (Bean counters' 56 small `convert_ammo`
calls); the inventor = the amplification phase where the Loki toolbox goes on top.
Iterations version the name (Skalman v1, v2, …); burst-amplified variants may carry
Bamse-family flavor later.

**GAME-TERMS RULING (Magnus, s53, verbatim: "We play to destroy their cores"): the kill
stays the win in the Skalman era — strangle-then-KILL. `R1000_IS_DEFEAT: yes` survives
the line change; the cage, the belt and the nest are means; core destruction is the end.
(The s31-class collision the side lane flagged is resolved by this ruling.)**

**Doctrine, two phases per Magnus:** (1) REPLICATE the measured Bean counters basics
properly — 4-builder capped eco, big terminated home belt (their 83% harvester→core
connectivity vs our 58.8%), the core-ring barrier CAGE (55.5% of barriers on the eight
victim tiles), the d²≈25 sentinel nest (inside sentinel reach, outside gunner reach),
drip ammo conversion, home-ring turret clearance (their 79.7% vs our 42.8%); the
founding doc is `PLAYBOOK-beancounters-2026-08-21.md` + the study. (2) AMPLIFY with our
own specialities once the basics measure at parity.

**NEXT_LINE_BENCHMARK = `bots/_v542wave`, FROZEN (builder's call per the directive):**
our strongest own tree — the live ship, the retiring line's peak — with a MEASURED
position on the new-era scale (the anchor read its byte-equivalent at 51.94
[50.61,53.28] vs the BASELINE, and v542-vs-v537 is a verified paired tie), so every
Skalman read vs the benchmark CHAINS to the bar-2 scale without re-anchoring.
Iteration screens still run vs the previous line iteration (mill discipline unchanged);
the benchmark answers "has the new doctrine caught the old one," and the slot changes
hands only on the full SHIP_BAR. BASELINE (`bots/_x3r0v168mjolnir`) and bar-2 (53.3)
unchanged — they are properties of the ladder era, not of our line.

**Sunset scope:** the two-raider rush doctrine and the Baltsars banditer name end with
this directive. v177 HOLDS the ladder slot until a Skalman clears SHIP_BAR (a live bot
is not pulled for sentiment). Transferable evidence banks: v543burst's d²≤32 siting
(=the nest geometry), #50 kladde cadence (=the belt engine), DOORWAVE/#96 (=home-ring
clearance, a core verb of the NEW doctrine — its locked leg completes), #113 SEALWATCH,
the cage/anti-cage instruments. The v544 stall-and-bank governor build is CANCELLED
(the new doctrine's funding rhythm is the drip, not the burst-bank).



## BASELINE MOVED 2026-08-21 (Magnus, s52, post-rotation — verbatim: "i dont think we can keep sleipnir v2 as the baseline anymore, use x3r0's best one as baseline instead")

**The pricing/battery BASELINE (the full-pool denominator, formerly `bots/_v488beltbreak2` =
Sleipnir v2) is now `bots/_x3r0v168mjolnir`** — the builder's operational reading of "x3r0's
best", vetoable: v168 is their best BY TENURE RECORD (the 16W-9L day that recovered their
slide to 1845; the then-current v173 was a 2W-8L "SHADOW" test build). Consequences: (1)
`SHIP_BAR`'s bar (2) denominator MOVES with the baseline; **its NUMBER does not transfer**
("≥70" was Sleipnir-v2-denominated on the OLD pool — our line screens ~52-60 vs the Mjolnir
line, so the bar's number RE-ANCHORS at the first new-pool baseline shard and is then
Magnus's to set); every old-pool anchor (70.50/66.44/72.57/72.06, the 69.28 floor, the
70.4964 binding point) is a HISTORICAL quantity of the old fixture, named as such at any
citation. (2) The first new-pool shard = **the BASELINE ANCHOR: v174 (`_v537socket`) vs
`_x3r0v168mjolnir` on the rotated 15-map pool** — control-anchoring before candidate
pricing; its readout re-derives the refusing segment and KILL_TARGET bands shard-native.
(3) `PREVIOUS_INCUMBENT`-class tools accept the transition per the 2026-08-21 control_pin
fix; Sleipnir v2 remains on disk for historical cross-tape reads only.

## BAR-2 NUMBER SET 2026-08-21 (Magnus, s53, on the NEWPOOL-BASELINE anchor — verbatim: "Oh, yeah 75 is not going to happen unless we move away from the rush tactic, so we can skip that to something smaller")

**Bar (2) = the candidate's full-pool CI LOWER >= 53.3 vs `bots/_x3r0v168mjolnir` on the
rotated pool (n=5400 house form).** Basis: the anchor read the live line at 51.94
[50.61, 53.28], so 53.3 = clear the anchor's UPPER bound = a provable improvement over the
line that ships today, requiring a point read of roughly >= 54.6 at full-shard width. This
was the builder's stricter recommended form; Magnus ruled "something smaller" than the
75-class number and the recommendation stood un-overridden (run-with-recommendations).
The 75-floor/80-target vs Sleipnir v2 is RETIRED WITH ITS FIXTURE — it was a number about
a different ruler, not a lowered standard. **Magnus's rationale is recorded as doctrine
context: the rush tactic trades full-pool dominance for kill speed; bar-2 exists to stop
sideways ships, not to punish the doctrine.** Bar (1) unchanged. Note the distinction the
V543POOL lock already carries: a screen's own registered DECISION bar (51.33 comparability
floor) governs its READOUT; bar (2) governs the SHIP decision — the two are applied at
different moments and neither substitutes for the other.

## SHIP_BAR AMENDED 2026-08-20 (Magnus, s52, reporting x3r0's agreement — JOINT amendment)

**Verbatim (Magnus): "We actually just have to beat the slot and stay above 70 against
Sleipnir v2, x3r0 was okay with us going for the slot after that."** Supersedes the 75/80
block below (kept for provenance). Operational form, builder s52 encoding (Magnus may veto
either reading): **RELEASE = both of (1) BEAT THE SLOT — a head-vs-holder screen vs the LIVE
holder's imported tree (freshest available import; the anchor's version is named on every
number), **at the established screen class (n≥900/arm, full 15-map pool)**, whose CI
EXCLUDES 50** — the plain-beat reading of "just have to beat" (the powered-n clause is a
third builder encoding choice, vetoable like the other two: without it a lucky small-n
interval would satisfy the bar); the `X3R0_SLOT_RULE` 60±2 bar is **SUPERSEDED ENTIRELY —
no residual scope**: it existed to govern reclaiming the slot from a teammate mid-campaign,
and with the release jointly agreed there is no non-release slot-reclaim scenario left; the
parsed field above says so, so a successor reading either surface alone gets the same
answer —
**and (2) ≥70 vs Sleipnir v2 — the full-pool powered fixture (n=5400 class), POINT ESTIMATE
≥ 70.0 with CI-lower above 69.28** (FLIPPOOL's lower bound; "stay above 70" needs the number
to hold, not merely touch). STEALTH_UNTIL_DROP unchanged: no exposure until the release
fires; the platform CPU `match test` remains mandatory INSIDE the release window; the
release itself remains coordinated with x3r0 (their slot until we take it). Reference
points at encoding time: v525flip 70.50 [69.28,71.72] (flippool-final) · v533home 66.44
[65.19,67.70] (homepool-final) · head-vs-holder 54.33 [51.06,57.60] vs the v165B artifact
(v169 screen in flight).

## SHIP_BAR (75/80) RAISED + STEALTH ADDED 2026-08-18 (Magnus + x3r0 jointly, in-session — s51) — SUPERSEDED 2026-08-20 by the block above

**Verbatim (Magnus): "Me and x3r0 have been talking and we agreed that we need to get around
75-80 winrate against Sleipnir v2 to have a shot at the finals, and we both think you can get
us there. We dont want to release the bot yet, it needs to chock the ladder when we drop it."**
Supersedes the same-day 70 bar (kept below for provenance). Operational form: **75% = the
floor that opens a drop conversation, 80% = the target, both vs `bots/_v488beltbreak2`
(Sleipnir v2) on the full-pool powered fixture; the 6-map grid remains a non-arming read.**
**STEALTH: the new line is NOT released, NOT submitted, and NOT exposed in unrated legs
against live teams until the drop** — the panel-preview law cuts both ways (team lazy
rehearsed their v242 on us unrated before shipping it; we do not teach the field our planks).
The drop is a coordinated event with x3r0. Live-transfer confirmation happens AT the drop,
not before it — an accepted risk, stated: the two-opponent local panel (incumbent verdict +
Gungnir transfer guard) is the stealth-compatible substitute until then.

## KILL_TARGET ADDED 2026-08-18 (Magnus, direct, in-session — s51: "Great, thats the new goal then")

The ultra-rush design target, derived from measured anchors and ratified by Magnus:
**median kill ≤ r180 · tracked metric = share of kills by r200 (currently ~16.5% of games,
target >50%) · sub-r150 welcomed as tail, not planned as median · r300 stays the hard
admissibility floor (DEFENCE_ADMISSION_BAR unchanged).** Basis, all on the tape: our-death
p25 = r196 (the race we must beat), historic winning median r174, field converts against us
at r300+ (0.82), physics floor ~r130-170 (arrival r9-16 + turret ≤r75 + funded kill window).
Phase budget: ring ≤r16 · first funded turret ≤r75 · net-positive fire from first shot ·
core dead ≤r180. **Every build report from v517 on carries the kill-round CDF against the
r150/r180/r200/r300 marks.**

## SHIP_BAR (70) ADDED EARLIER 2026-08-18 — SUPERSEDED SAME DAY by the 75-80 block above, kept for provenance

**Verbatim: "We're looking for a 70+ build before we ship this time."**
Operational form (builder s51, on the record in the coordination tail
~06:2xZ): **no ship conversation until a candidate reads ≥70% game share vs
the PROGRAMME INCUMBENT (`bots/_v488beltbreak2`) on the standard full-pool
local fixture at powered n.** Non-arming reads: a 5-map grid, any sub-2700
partial, any read vs a non-incumbent control. The 55.0 COMBO floor is a
shard-survival constant, not a ship signal under this bar.
**WHICH BAR GOVERNS WHICH QUESTION** (they are different questions):
`SHIP_BAR` (70+) governs SHIPPING A NEW BUILD of ours; `X3R0_SLOT_RULE`'s
60±2 governs RECLAIMING THE SLOT from a teammate's holder with an EXISTING
measured build. Neither authorizes an activation by itself — the slot changes
only on Magnus's explicit word (SLOT_STOP_LOSS block above).

## SLOT_STOP_LOSS RETIRED 2026-08-16 (Magnus, direct, in-session)

**Verbatim, 2026-08-16 ~15:4xZ: "We dont do stop loss anymore, stop any stop
loss and let the slot be until i say we change it."** Given ~30 minutes after
the −21 rolling-5 rule fired legitimately on x3r0's v152 (15:12:54Z, net5 −29,
drawdown −64 — verified, on the record in coordination.md).

**READING.** The slot stop-loss (rolling last-5 net ≤ −21, armed at k≥8, frees
the slot) is OFF. No alarm rules toward displacing the holder: `slot_rule`
forces `slot_free=False` while this field reads `off`, `ship_watch` writes no
`corpus/SHIP_ALERT` (the SPRT bleed advisories included — they are
stop-loss-family wakes), and `elo_logger` makes no SWAP RULE announcements.
**The pollers keep logging the trend** (rating, drawdown, k) — eyes stay open,
rulings stop. **THE SLOT CHANGES ONLY ON MAGNUS'S EXPLICIT WORD.** That
supersedes the "unless a stop-loss fires" escape in SHIP_SIT_MIN_K, and it
parks the SWITCH step of X3R0_SLOT_RULE's pipeline — the 60±2 screening
continues as MEASUREMENT, but clearing it no longer authorizes an activation;
Magnus's word does. Flip this field back to `on` only on his directive; the
machinery below it is kept intact and selftested in both states for that day.

## LINE_DIRS WIDENED AGAIN 2026-08-16 (Magnus, direct, in-session: "Ok to widen the bots in programme")

The s31 defect recurred exactly as its own entry predicted: the patterns stopped
at v199 (`_v1[3-9]?*`), the line moved to v2xx, and the INCUMBENT
`bots/_v223sealrepair` failed its own programme's line check — with 26 of 27
battery invocations bypassing via `--off-programme` (s46 audit,
`docs/workflow-analysis/AUDIT-2026-08-16-instruments-vs-decisions.md` Q5-4: a
guard that refuses everything gets routed around). Widened with `bots/_v[2-9]??*`
(v200+, any name; cannot collide with the Eir era, which is all v1xx). Verified
both ways at the edit: `_v223sealrepair`/`_v242bodyaware`/`_v315siphit` now
match; `_v115dodge`/`_v116thor` still excluded.

## X3R0_SLOT_RULE RE-PRICED 2026-08-16 (Magnus, direct, in-session)

**Verbatim, 2026-08-16 ~05:2xZ: "we will not take the slot back unless we have
something with a 60% winrate ±2pp, otherwise we stay grinding."** This
supersedes the 51%-at-n1000 reactivation threshold below (kept for provenance)
and resolves the suspension question open since s44: the rule is no longer
suspended, it is RE-PRICED. Operational reading: no activation displaces a
teammate's holder unless an arm reads **≥60% game share against the v140
control with a half-width of ≤2pp or better** (at the local fixture's n=5,400
the band is ±1.31pp at p=0.6, so a completed screen already meets the precision
term; the binding term is the 60). Point estimate ≥60 with CI-lo ≥58. The
board's ceiling at this ruling is 55.24% (MIX280mix4), so the standing state is
GRIND. **This also parks the live unrated leg**: an unrated window requires
activating an arm into the slot, which this bar now governs — no leg fires
until an arm clears 60±2 locally or Magnus explicitly opens a window.

**⭐ PROCEDURE COMPLETED BY MAGNUS, 2026-08-16 ~05:3xZ, verbatim: "When we have
a bot like that we start by testing it against the current slot, If it beats it
we can switch."** So the full pipeline is: (1) an arm clears the 60±2 threshold
against the v140 control on the local screen; (2) it is then screened HEAD-TO-
HEAD against the CURRENT slot holder's artifact (staged locally, the
v142/v143 template — the mechanism of the superseded 2026-08-14 rule survives
as this step); (3) it beats the holder ⇒ switch, in a safe pairing window via
submit_clean, verified on the `Active bot:` line. The threshold gets us to the
table; the head-to-head decides the seat.

**READING SETTLED BY MAGNUS, 2026-08-16T05:32:44Z, verbatim: "It must measure at least 60 +-2pp
so 60 should be the middle of the span."** The PRECISION reading: the point
estimate must be >= 60.0 with a 95% half-width of <= 2pp (n >= ~2,260 at p=0.6;
a standard n=5,400 shard over-delivers at +-1.31). An arm reading 58-59.9 does
NOT qualify. Tolerance reading retired.

## X3R0_SLOT_RULE ADDED 2026-08-14 (Magnus, direct, in-session) — SUPERSEDED 2026-08-16, kept for provenance

**Verbatim: "Whenever he outs one up, run n=1000 against it and put ours back
if we win."** This closes the x3r0 standing-rule question OPEN since s38 and
converts the twice-executed pattern into policy: on ANY x3r0 slot upload,
(1) stage his artifact, (2) commit a SCREEN-v14XvsY prereg pre-row (the
v142/v143 template: our live-line tree as treatment, his artifact as control,
n=1000, decision rule >=51.0 -> reactivate ours in a safe pairing window,
verified on the Active bot: line), (3) execute the branch the number picks.
No counter-roll without the number; the screen IS the resolution mechanism.
Precedents: v142 (56.80 -> reactivated 15:18:51Z), v143 (screen in flight at
the directive). holder_watch is the trigger instrument; the displaced panels
problem (CAL-6/7/8) is priced into this rule — a screen takes ~15 min on the
fleet box, so the foreign-holder window stays short when we win.

## SHIP_SIT_MIN_K ADDED + RATED CADENCE CORRECTED 2026-08-13 (Magnus, via the meta lane)

**Authorisation:** Magnus, 2026-08-13, acting on the lane-structure review
(*"could you apply your fixes after that and i'll be able to wake up the new
ones with your changes"*) — review R2/R3. Recorded verbatim because this file
is edit-on-his-directive-only and the commit message is where the
authorisation lives.

**READING OF THE NEW FIELD.** `SHIP_SIT_MIN_K: 8` — a shipped version is NOT
displaced before k≥8 rated matches (its own gate's arming point) unless a
stop-loss fires. Basis: v122 shipped 04:45:54Z and was displaced 06:06Z at
k=4 — two ships in 80 minutes bought zero rated information, against roughly
4–12 remaining ship-and-converge cycles (convergence cost itself is
unvalidated in both directions; see the review). A displacement below k=8
without a fired stop-loss is off-programme.

**THE `INCUMBENT` FIELD IS NOW SCRIPT-MAINTAINED:** `submit_clean --activate`
rewrites `INCUMBENT`/`PREVIOUS_INCUMBENT` on a verified ship (cb4540a,
delegated by Magnus the same day — THAT FIELD ONLY; everything else in this
file stays edit-on-directive-only).

## ⭐⭐ REVERTED 2026-08-13 ~11:2xZ — `R1000_IS_DEFEAT: yes`, UNCONDITIONAL AGAIN

**Magnus, direct, verbatim: *"revert it, i'd like us to be an offensive team"***
— given in answer to a recommendation that named the field and the evidence.
Recorded verbatim because this file is edit-on-his-directive-only.

**WHY THE EXEMPTION'S BASIS IS GONE.** The conditional (below, kept as history)
rested on one measured fact: three doctrines could not kill a weak bot on 4 of
5 area-900 maps. **That was the MAP_CODES pathfinding defect, not a property of
big maps** — fixed and shipped as v125 "Loki v8" (`bots/_v197mapcode`,
10:16Z). Post-fix: kills at turns 71/115/86 vs starter on the 900s; local
GRAND class 93.7% ±3.6 with kill median 165 (n=742); live panel round 1: every
win `core_destroyed`, medians 153–167 **including 900-area, zero tiebreak
wins**. The kill fires everywhere, so the defeat rule holds everywhere.

**WHAT SURVIVES THE REVERT:** the CQ/STD/GRAND three-class split stays as a
MEASUREMENT dimension (overnight_read prints it; kill bars remain
class-conditional where preregs say so) — it is reporting, not doctrine. Queue
#36 re-scopes to eco-as-kill-enabler on big maps, never eco-as-win-path.
**A r1000 finish is a defeat on every map. Economy buys the kill; it never
scores.**

## SUPERSEDED 2026-08-13 (kept as history) — MAP ROTATION: `R1000_IS_DEFEAT` briefly conditional

**MAGNUS, 2026-08-13, direct: *"R1000_IS_DEFEAT does not hold on 30x30 anymore."***
Recorded verbatim because this file is edit-on-his-directive-only and this
reverses a field that has governed the whole Loki line.

**READING OF THE NEW FIELDS.** `R1000_DEFEAT_AREA_MAX: 676` — on maps of area
**<= 676 a round-1000 finish is still a DEFEAT**, exactly as before. On maps
**ABOVE 676** it is an **admissible win**. The boundary sits between
`archipelago` (26x26 = 676) and the five 30x30s (900), so it names the new size
class and nothing else. Read map area at runtime from `get_map_width()` x
`get_map_height()`.

**WHY IT CHANGED — MEASURED TODAY, NOT ARGUED.** The organisers rotated the pool
to 15 maps and **five are 30x30 (area 900), a size class we had never played.**
Our largest previous map was 625. Against `bots/starter` — a WEAK reference bot —
on those five maps:

    Loki v123 (rush)    1 kill of 5
    Eir  v94  (heal)    1 kill of 5, and LOSES two outright
    Thor v116 (offense) 1 kill of 5

**Three independent doctrines, ~50 versions of development apart, all fail to
kill a weak opponent on 4 of 5 big maps.** A win condition that does not fire is
not a standard to hold the line to.

**AND THE MECHANISM IS BANKED RATHER THAN GUESSED.** Over 18 games (2 seeds x 9
maps) the split is clean: **maps <= 625 mean 94 Ti banked, 27.2 buildings, 8/8
kills; maps at 900 mean 4,805 Ti banked, 21.6 buildings, 3/10 kills.** One cell
(`valkyrie` seed 971002) finished with **0 titanium mined in 1,000 rounds** —
pure passive income, no delivery at all. **We are not too slow on big maps; we
are rich and idle.** `doctrine.py` references map size **zero times** and every
cap is an absolute integer fitted on the old pool (`MAX_BUILDERS 5`,
`LOKI_MAX_BUILDERS 11`, `LOKI_FWD_GUN_CAP 3`, `ECO_CAP 18`), and at least one
radius is absolute too — `eco.py:372` gates the harvester-count sync on
`d^2 <= 64`, which covers **58% of `fjordgate` and 6.4% of `midgard`**, the same
58 tiles on every map.

**⛔ WHAT THIS DOES NOT LICENSE.** It does not revive the tiebreak as a TARGET on
small and medium maps, where 10 of the 15 maps still sit and where the kill
demonstrably works. It does not retire `KILL_WINDOW_RND: 250` there. **And the
measured tiebreak record is not a licence either: against EVEN opponents we win
49.9% of r1000 games and 52.5% of short ones** — controlled for rating gap — so
on maps where we CAN kill, killing is still better. **The change is scoped to the
size class where the kill does not fire at all.**

## INCUMBENT MOVED 2026-08-13T04:45:54Z — v116 -> v122 (`bots/_v178salt`)

**Edited on Magnus's explicit directive** (*"Do your recommendations"*, in answer
to a recommendation naming this field and this value). Recorded here because this
file is otherwise edit-on-directive-only and a successor must be able to see WHY
a parsed field changed.

**WHAT CHANGED AND WHAT IT MEANS.** `_v178salt` is the live slot as of 04:45:54Z
(verified on the `Active bot:` line, not an exit code). `COMPARE_AGAINST:
previous_line_iteration` therefore now points at **`_v178salt`**, not at
`_v169launchlate160`. Magnus stated the rule himself before the file caught up:
*"A counter + salt vs just salt should win more than it loses."*

**⚠ CONSEQUENCE FOR EVERY OPEN BATTERY, so nobody misreads a live number:** the
salt-family arms queued BEFORE the ship (`SALTREP`, `SALTIDLE2`, `SALTCUTONLY`,
`SALTNOBLOCK`) are controlled on `_v169launchlate160` = **the PREVIOUS
incumbent**. They remain valid — they answer *"better than the bot we
replaced?"* — but they do **NOT** answer *"better than what is live?"* Arms
queued after the ship (`NULLSALT`, `SALTCLEAR`, `SALTROUTE`, `IDLEVSALT`,
`ROUTEONLY`) are controlled on `_v178salt` and do.

**⛔ AND THE KNOCK-ON THE SIDE LANE NAMED, which is the real cost of this move:**
`QUEUE.md`'s `GREP:` admission gate is denominated in *"what was checked in the
INCUMBENT."* **Every existing row's grep was run against `_v169launchlate160`, so
all of them became potentially stale at 04:45:54Z.** The gate proves a check WAS
RUN; it never proves the result is STILL TRUE. `tools/queue_check.py` now flags
this mismatch rather than re-running the greps.

**ROLLBACK NOTE:** if v122 is rolled back, this field returns to
`bots/_v169launchlate160` and `PREVIOUS_INCUMBENT` is removed. The rollback
target is recorded in `docs/prereg/SHIP-salt-v178-2026-08-13.md`.

## ⭐⭐⭐ CORE VALUE, MAGNUS, 2026-08-11 (s31) — **ALWAYS BE RUNNING.**

**Written into this file on his direct instruction — *"put this in your
programme, it's a core value for you"* — after he had to ask THREE TIMES in ten
minutes whether anything was running locally.** The exchange, verbatim:

> *"anything running locally?"*
> *"do we not monitor the local runs? if nothing is running we're losing time we
> could use to figure out the next Loki version"*
> *"If we are not running locally we should grab items from the queue and run
> them, the researcher has a monitor that makes them put more items in the queue
> if it is running out."*

**THE RULE: IDLE CORES ARE A DEFECT. If nothing is running locally, the builder
takes the top unblocked item from `QUEUE.md` and runs it — without being asked,
without waiting for analysis, and without a window.**

**WHY IT IS A VALUE AND NOT A PREFERENCE, in this project's own numbers:**
* Local games are **free, unlimited and instant**. The rate limit (5 unrated per
  20 min) governs the PLATFORM only. **Nothing rations local cores but attention.**
* **Rated cadence is 72 matches/day at HEAD** (20.0-minute pairing gaps, 40/40
  recent — the old "~420 remaining at ~84/day" straddled the 08-10 cadence
  change; corrected 2026-08-13, lane-structure review). No hard end date is on
  record; "over in a week" (Magnus, 08-11) puts roughly 300–390 rated matches
  left. **A ship converges in the BACKGROUND while we work**, so an unshipped
  plank is a certain zero and an idle hour is unrecoverable.
* Measured on this machine 2026-08-11 13:53Z: **load average drained 14.67 -> 1.57
  with ZERO `fcode run` processes and a fully stocked queue sitting unread.**
  Ten cores idle while three planks waited.

**⛔ AND THE STRUCTURAL REASON NOBODY NOTICED — this is s30's D66 recurring:**
that session ran screens on **1 core of 10** for ninety minutes. The lesson was
recorded as *"subagents are for judgment, cores are for games"* and it **did not
prevent the same failure one session later**, because it was written as a lesson
rather than built as an instrument.

⇒ **`tools/monitors/cores_idle.py` (s31) IS THE INSTRUMENT.** It polls every
300 s, and on two consecutive polls with zero local games it prints
`*** CORES IDLE — NEXT QUEUE ITEM: <plank> ***` and writes
`corpus/CORES_IDLE_ALERT`. **The alarm carries its own remedy: it names the plank
to start.** It gates on the process count (never `$?`), reports the queue file's
AGE, and returns **BLIND rather than "idle"** if `ps` fails — because an alarm
that cannot tell it is blind is this repo's most-repeated defect.

**THE DIVISION OF LABOUR MAGNUS SET, and both halves are now instrumented:**
**RESEARCH keeps `QUEUE.md` stocked** (their monitor fires when it runs low);
**BUILDER keeps the CORES BUSY** (this monitor fires when they go quiet).
**An empty queue is a research failure; idle cores are a builder failure.**

## QUEUE_FLOOR / QUEUE_OWNER — added 2026-08-11 (s31) on Magnus's direct instruction

> *"you need to be constantly putting experiments to test, there should be a queue
> with ideas to build, the researcher will be responsible to make sure there are
> ideas to build"* … *"if the queue runs empty we go stale, that is not acceptable."*

**`QUEUE_FLOOR: 3`** — `QUEUE.md` must hold at least three items the builder can
**start today**. Unblocked means **no research number is owed**; an item gated on a
running cut does not count. **`QUEUE_OWNER: research`** — an empty queue is a
**research failure, not a builder pause.**

**⛔ THESE FIELDS EXIST BECAUSE THE DIRECTIVE AND ITS ALARM LIVED NOWHERE A LANE
BOOTS.** Audited the same day: `QUEUE.md` and `queue_check` appeared **0 times** in
this file, **0** in all three `.claude/commands/*.md`, **0** in `CLAUDE.md`, and
`gate.py` read no queue field. **Found by Magnus asking whether the programme carried
a line about it.** The s29 retro finding — a rule promoted into a file nobody opens —
committed by the lane that wrote the routing rule about it.

**ENFORCEMENT, strongest first:** a **`SessionStart` hook** runs
`tools/queue_check.py` in every lane (harness-executed, so it cannot be forgotten) ·
boot steps in all three command files · the **`GREP:` admission gate** — a row counts
only if it names what was checked in the incumbent and what was found · and these
fields, so `gate.py` can read the floor rather than have it live only inside the tool.

**⚠ THE FLOOR IS A TARGET AND TARGETS GET MET.** Its author stocked the queue to six
items at 13:27 and three had died on checks that had not yet run by 13:51 — **the
alarm reproduced the failure it was built to catch.** That is why admission requires
the grep, and why **an honest 3 that FIRES beats a padded 6 that cannot.** A successor
raising this floor should raise generation, not admission.

## ⭐⭐ DIRECTIVE, MAGNUS, 2026-08-11 — **"WIN RATE DECIDES."** GIVEN DIRECTLY TO THE BUILDER, NOT RELAYED.

Preceded in the same session by *"The goal for any of this is to climb ELO"* and
*"Any improvement no matter how small should be considered as the replacement of
v104."* **`WIN_RATE_IS_VERDICT` flips `no` -> `yes` and `PRIMARY_CURRENCY`
becomes `game_share`.**

**AND IT IS NOT A COMPROMISE WITH RIGOUR — IT IS THE OBJECTIVE FUNCTION.** The
ladder pays `delta = 32 x (S - E)` where **S = games won / 5**. Game share IS
what the ladder pays, verified to a max residual of 0.000000 across 100 matches.
`kill_speed_score` was always a PROXY, adopted because `R1000_IS_DEFEAT` made a
tiebreak win worthless *to us*; **the ladder never agreed and pays for it
anyway.** Optimising the proxy while the goal is Elo is the mistake, not the fix.

**⛔ ONE CONSEQUENCE THE BUILDER FLAGGED BACK RATHER THAN APPLYING SILENTLY, AND
IT IS THE ONLY PLACE THIS DIRECTIVE COLLIDES WITH ANOTHER:** under
`PRIMARY_CURRENCY: game_share` **a round-1000 tiebreak win is a WIN**, because the
ladder pays it. `R1000_IS_DEFEAT: yes` (below) says it is a defeat, and the
`-10` in `tools/score.py` exists precisely to make tiebreak-turtling score zero.
**Those two cannot both drive a ship decision.** Until Magnus rules:
* **`game_share` decides the SHIP** (this directive, and it is what Elo pays);
* **`R1000_IS_DEFEAT` still governs what we BUILD** — no plank may be *designed*
  to farm tiebreaks, because that is the doctrine and it was set on 2026-08-10;
* **`tools/score.py` and every baseline in it are UNCHANGED**, so v20 -10.00
  through v104 -1.76 stay mutually comparable. Changing the scale in place
  orphaned every earlier figure once already, within the hour.

## What this means, in the words of the directive (Magnus, 2026-08-09)

> *"Loki should be our main focus now, leave Eir behind to hold the lines while
> we build something that has a shot at actually ranking high."*
> *"Eir is what, iteration 50+, Loki v1 was never supposed to be shippable...
> we need a lot of iterations to make Loki stand a chance."*
> *"Although Loki is supposed to be an entirely separate bot from Eir."*
> *"We need to find good tricks we can use, poisonings, exploits, manipulations,
> anything that seems to have a shot at killing teams in the first 250 rounds,
> and lean into that hard once we find it."*

**⭐ INCUMBENT UPDATED AGAIN 2026-08-12 (s34) ON MAGNUS'S DIRECT INSTRUCTION
("Update it please"), SIDE LANE'S HAND.** `bots/_v148ferryfirst` (v112) →
**`bots/_v169launchlate160` (v116)**. **It had gone stale across THREE holders**
— v114, v115 (x3r0's ship), v116 — the second such lapse in two days.

**HOLDER VERIFIED FROM A LIVE PRIMARY, NOT FROM A DOCUMENT** (D28: a document
naming the holder is a CACHE): newest `corpus/ship_watch.log` row
**`2026-08-12T17:58:25Z v116 k=11 rating=1674 tape_age_min=4.4`**, which derives
the version from the elo tape rather than from any written claim, cross-checked
against the builder's live `fcode status` read at 17:24Z (`Active bot: v116
(Loki v5)`). Tree `bots/_v169launchlate160` confirmed present.

**`INCUMBENT_FROZEN` DELIBERATELY UNTOUCHED AT `no`** — the s31 hazard below does
not apply this time precisely because that repair was done correctly then.

**WHY THIS FIELD BEING STALE COSTS SOMETHING, which was not true when it was
merely decorative:** `gate.py` only PRINTS it (it enforces on `LINE_DIRS`), **but
`QUEUE.md`'s `GREP:` admission gate is denominated in "what was checked in the
INCUMBENT"** — so a stale pointer sends every admission grep at the wrong tree.
Audited at s34: the 16 counted rows were re-checked against the live tree and
**all hold** (`#17`'s zero border/edge refs: 0 in both, with `_v131loki14` at 7 as
the positive control; `#23`'s `LOKI_FWD_GUN_CAP = 3`: identical) — **the count is
honest and this repair is a defence against the next admission, not a correction
of the last.** One row moves in the builder's favour: `get_attackable_tiles_from`
has **0 call sites in the v112 tree and 2 in the live one** (LOKI-25), so `#10`'s
note that the component does not exist is now false.

**PRIOR ENTRY, KEPT — INCUMBENT / INCUMBENT_FROZEN** — ⭐ **BOTH FIELDS UPDATED
2026-08-11 (s31) ON MAGNUS'S DIRECT INSTRUCTION ("fix please"), AND THEY MOVED
TOGETHER ON PURPOSE.**

**WAS:** `INCUMBENT: bots/_v115dodge` (v92) with `INCUMBENT_FROZEN: yes` — *"holds
the ladder slot and receives no further planks. It defends the rating; it is not
the work."*
**NOW:** `INCUMBENT: bots/_v148ferryfirst` (v112) with `INCUMBENT_FROZEN: no`.

**WHY BOTH, AND WHY REPAIRING LINE 8 ALONE WOULD HAVE BEEN WORSE THAN LEAVING IT
STALE.** The incumbent field had gone stale across TWO ships (v104, then v112) and
both other lanes flagged it. **But the freeze clause says the incumbent receives
NO FURTHER PLANKS — so pointing `INCUMBENT` at the LIVE Loki tree while
`INCUMBENT_FROZEN: yes` stood would have made this file forbid development on the
exact bot we develop**, contradicting Magnus's own *"any improvement no matter how
small should be considered as the replacement of v104"* three sections above.
**A false-but-inert field became a false-and-binding one on repair.** The side
lane caught this before either repair was made.

**WHAT THE FREEZE ACTUALLY MEANT, AND WHY IT NO LONGER APPLIES.** It was written
when **Eir held the slot and Loki was a separate line under development** — the
point was *do not spend planks defending Eir; build Loki*. **That situation ended
when Loki itself started shipping.** v104 held for 29 h 25 m, v112 shipped
2026-08-11 13:14Z, and the line under development IS the line on the ladder.
⇒ **There is no longer a frozen rating-defender distinct from the work.**

**⛔ WHAT `INCUMBENT_FROZEN: no` DOES NOT LICENSE.** It does not retire
`COMPARE_AGAINST: previous_line_iteration` — a plank is still measured against the
CURRENT incumbent, and **when a ship lands, every control moves with it** (a stale
control measures the wrong contrast and still reads as a valid result;
`h2h.sh`/`dose.py` defaults and `unrated_run.sh`'s `MAIN` all moved on 2026-08-11
for this reason). **And a null belongs to its control** — the 4,096-game null
built against `_v130loki13` was marked STALE the moment v112 shipped.

**⛔ LINE_DIRS — WIDENED 2026-08-11 (s31), AND THIS FIELD WAS SILENTLY BREAKING
THE ONLY GATE WE HAVE.** `LINE_DIRS` is **the one field `gate.py` ENFORCES on**
(everything else it merely prints). It matched only names containing `loki` —
and **we stopped putting `loki` in bot names at `_v139heal`.**
⇒ **The LIVE SHIPPED BOT `_v148ferryfirst` (v112) failed its own programme's
line check**, as did every arm built this session. `gate.py` would have refused a
battery on any of them with *"is not on the active 'loki' line"*.
**AND THAT IS ALMOST CERTAINLY WHY `h2h.sh` BYPASSES `gate.py` AT ALL** — the
standing rule says the gate is the SOLE ENTRY to a battery, and the gate had
become unusable on the current line, so the tools routed around it. **A guard
that refuses everything gets removed from the path; that is the same failure as a
guard that fires on nothing, and this repo produced both in one day.**
Widened to `bots/_v1[3-9]?*` (v130+, any name) alongside the historical
`loki`-named patterns. **Verified: 43 line dirs match, 22 Eir-era dirs excluded
including `_v115dodge` and `_v116thor`.**

**LINE: loki** — Loki is a SEPARATE BOT, not a flag on the Eir chassis. Iterations
edit Loki's own tree. Porting Loki features onto Eir is the line-mixing this
directive forbids; `bots/_v116thor` is the last instance and is retired.

**COMPARE_AGAINST: previous_line_iteration** — LOKI-N is measured against
LOKI-(N-1), never against Eir. "Does it beat the incumbent" is the wrong
instrument for a line under development and is what buried LOKI-1 in s22: a v1
was judged against a v46+ line, on a self-play pool, and the road was closed on
the result.

**WIN_RATE_IS_VERDICT: no** — the probe pool is dominated (both arms win 87-90%),
so a win-rate ceiling that high cannot show an edge. Read
**core-kill share** and **time-to-core-kill**. Measured 2026-08-09: LOKI-1 vs v92
was a win-rate NULL (+3.1pp, p=0.22) and a core-kill landslide (91% vs 61% share,
paired sign test p=5.2e-09).

**KILL_WINDOW_RND: 250** — the target is a dead enemy core inside 250 rounds.
Our own tape: before r200 we go 277-148 (65.2%); after r200, 164-363 (31.1%).

## DIRECTIVE, Magnus, 2026-08-10 06:0x CEST — read this as the definition of the line

> *"Loki is the ultimate trickster, playing into other teams by using cheap
> tricks, manipulation, poisoning and every exploit we can find. Loki plays
> dirty and is the ultimate weapon at that. We want to destroy the enemy core,
> never play defence. A r1000 round is a defeat even if we by chance win it.
> You need to constantly figure out and test new tricks that we can use by
> building prototypes and putting them against live teams in unrated games —
> that beats our own calculations every time, and sometimes you find things
> that surprise you. Those are of fantastic importance for our growth."*

Three fields above are new and each one closes a road that was open yesterday.

**R1000_IS_DEFEAT: yes.** A tiebreak win is a LOSS in this programme's ledger.
This retires the whole tiebreak-turtle family and demotes every economic plank
whose only channel is `titanium_collected` — that currency is only ever paid out
in games we have already lost by this definition. Economy is now purely
INSTRUMENTAL: it buys the kill, it never scores.

**PLAY_DEFENCE: not_at_the_kill_s_expense.** ⭐ **AMENDED 2026-08-11 (s31) ON
MAGNUS'S DIRECT INSTRUCTION TO THE BUILDER — "update the programme".** The
directive, relayed to the side lane and confirmed to me directly:

> *"This does sound like we should allow SOME defence strategies, but our FOCUS
> should be to kill at <r250."*

**THE FIELD WAS `never`. IT IS NOW A BAR, NOT A BAN — and the bar exists because
"SOME defence" is a GRADIENT and a gradient is unenforceable unless the test is
written down.** `never` was a bright line, enforceable at zero judgement cost;
replacing it with a preference would have made every survival plank arguable.
So it is replaced with a MEASURABLE ADMISSION TEST, declared in the parsed block
at the top of this file as `DEFENCE_ADMISSION_BAR: kill_round_non_regression`.
**(Written inline as prose, NOT indented four spaces: an indented copy is read by
`gate.py` as a SECOND field declaration and, because it builds a dict, the LAST
occurrence WINS — so a prose illustration would silently override the canonical
block with no error and no diff. That is exactly what this section did for its
first eleven minutes; caught by the side lane.)**

⇒ **A defensive plank is ADMISSIBLE if and only if it does not slow the kill.**
Any survival-mechanism plank carries a **kill-round non-regression bar beside its
survival bar. If median kill round RISES, the plank is off-programme, whatever it
does to win rate.** (Operational form proposed by the side lane; adopted here
because it converts the directive into something `gate.py` can eventually read.)

**⭐ RE-PRICED 2026-08-16T05:15:45Z (s45) ON MAGNUS'S DIRECT RULING:** *"Re-price
the kill-round bar to bind at ~r300 instead of penalizing drift inside
r200-300."* The parsed field is now `DEFENCE_ADMISSION_BAR:
r300_crossing_non_regression` and the paragraph above is SUPERSEDED as the
operational form. **The admission test binds at the r300 boundary:** a plank is
off-programme if it pushes kills PAST r300 — operationally, the share of its
kill-wins landing after r300 must not rise vs control (each prereg registers its
own n/MDE for this, and per the exclusion-restatement rule the claim is scored
as "the CI excludes the registered rise", never as a bare fail-to-find), with
median-kill-round-crosses-300 as a gross backstop.

**⛔ OPERATIONAL FORM CORRECTED 2026-08-16T05:19:38Z (s45), ~4h after writing —
THE SENTENCE ABOVE CARRIES A COLLIDER AND IS SUPERSEDED AS THE PRIMARY. The bar
itself (Magnus's r300 boundary) is unmoved; what was wrong was the builder's
encoding.** "Share of KILL-WINS past r300" conditions on winning, and winning is
downstream of the treatment: a plank converting marginal slow LOSSES into slow
WINS raises that share without delaying any kill (research, measured on the
rated tape: kill-win-conditioned 15.1% vs ITT 7.8%, same defect class as the
FIRE ORDER #1 primary caught the same morning). **THE PRIMARY IS NOW ITT,
denominator ALL GAMES: the share of a plank's games ending in a core-kill BY
r300 (its timely-kill rate) MUST NOT FALL vs control.** This catches kills
delayed past the boundary and does not punish loss→late-win conversions, which
Magnus's ruling never aimed at. The kill-win-conditioned share is REPORTED
BESIDE IT as a diagnostic — where the two forms disagree, the disagreement is
itself a finding (collider size) — and the median backstop stands. Any prereg
scoring this bar registers the ITT form.

**⛔ ESTIMATOR UNDER ARBITRATION, 2026-08-16 ~05:3xZ (s45) — THE THIRD FORM IN
ONE MORNING, SO THE CHOICE IS FROZEN RATHER THAN SWAPPED AGAIN.** Research
measured (local board, decomposition exact): the ITT form is dominated by win
share — every arm above ~50% passes it by construction, so it adds almost no
constraint beyond `PRIMARY_CURRENCY`. But the proposed alternative (bind on the
SPEED factor, P(kill ≤300 | kill-win)) IS the kill-win-conditioned form — the
collider retired at 05:19. **No single outcome-based estimator separates
"delaying kills we already had" (what the bar exists to catch) from "adding new
late wins" (which raises share and is not obviously bad): that is a
counterfactual, not a measurement.** INTERIM SCORING, in force until Magnus
answers the semantic question below: **report the TRIPLE (ITT timely rate ·
rate factor · speed factor). Both-pass ⇒ admissible. Both-fail ⇒ out. Split
(ITT-pass/speed-fail — today: the MIX/SH 55-class; AWRLNCH notably passes both)
⇒ held, labelled MAGNUS-CALL, neither banked nor refused.** The question filed
with him, in game terms: when a plank WINS MORE but its added wins land after
r300, is that admissible (share is king; the bar only guards kills we already
had) or not (no new business past r300)? His answer picks the estimator; nobody
picks it by statistics.

**⭐ ARBITRATION RESOLVED 2026-08-16T05:36:10Z (s45, builder decision on a full
control matrix — the Magnus question above was WITHDRAWN as moot: on the
unbiased estimator the split class is empty, so there was nothing left for him
to rule on). THE OPERATIONAL ESTIMATOR IS ITT RMST₃₀₀: mean kill time censored
at the r300 horizon over ALL games (a non-kill scores 300; the ITT median pins
at the horizon, so the MEAN is the estimator). THE BAR: a plank's RMST₃₀₀ must
not RISE vs control by more than its prereg's registered MDE, scored as
exclusion.** Basis, four ground-truth cases where the alternatives fail:
byte-identical null reads flat (+0.42); the deliberate negatives read SLOWER
(+33.3, +64.8) where the "past-300 share" form passed them both; and MAPCODE —
the shipped v125 pathfinding fix, 73% win share — reads **−60.81 rounds
FASTER**, the one estimator that correctly reads the board's biggest known
improvement as an improvement (the timely-rate form passes it only by
correlating with win share, r²=0.93; the past-300 form FAILS it outright).
Null calibrated both directions by ±200-turn mutation drives. The triple (ITT
timely rate · rate · speed) and the conditioned median remain REPORTED
DIAGNOSTICS. Vintage rule per the side-lane certification: arms whose preregs
locked before today keep their registered rules; RMST₃₀₀ governs preregs locked
from now on. **Drift inside r200-300 is
REPORTED, no longer DISQUALIFYING.** Evidential context, stated with its limits:
the old form's empirical grounding ("the field converts 4x better late") was
PRE-map-rotation; re-derived on the post-rotation pool
(`docs/research/KILL-HAZARD-REDERIVED-2026-08-16.md` + the same-day convention
audit), r200-300 reads ~parity (0.97-1.05, sign convention-sensitive — NOT an
advantage) while r300+ remains against us (0.82, robust under both conventions).
The bar therefore now sits where the measured disadvantage actually lives. This
does NOT touch `KILL_WINDOW_RND: 250` (the offensive TARGET — kill fast — is
unchanged; what changed is what disqualifies a plank), and it does NOT touch
`R1000_IS_DEFEAT: yes` (a directive, not an inference from any hazard table).
Live-leg design constant that follows from this ruling: an RMST-style kill-speed
primary uses horizon 300.

**⛔ THE SCOPE, AND IT IS WHAT KEEPS `R1000_IS_DEFEAT` UNCHANGED.** "SOME defence"
means **surviving the r150-250 window so OUR OWN KILL LANDS.** It does NOT mean
surviving to r1000. Measured, 1800-1900 band cut (side lane, `9209e3e`):
**our median kill round is 174 and our median death is 187 — a thirteen-round
race**, and **our core dies in 46.3% of all v104 games** with 98.3% of our losses
by core destruction against the band's 89.7%. Defence aimed at that thirteen-round
gap is the good road. **Defence aimed at reaching a tiebreak is still the retired
one** — the tiebreak tail is a coin flip (1800-1900 wins 49.4% of tiebreaks vs
45.2% overall), so there is no salvage there, and `R1000_IS_DEFEAT: yes` stands
untouched.

**⭐ AND THE CHEAP CLASS IS ALREADY IDENTIFIED, MEASURED RATHER THAN ASSUMED:
SEPARATE DEFENCE THAT SPENDS THE KILL BUDGET FROM DEFENCE THAT SPENDS IDLE
RESOURCES.** When our core dies, **~5 of our builders are ALIVE** (median 5.0,
mean 4.43 vs 5.20 in wins) with **0.38 builder deaths across the whole 40 rounds
before the core falls** — they are not even in combat. Home turrets and barriers
COMPETE with the assault and must clear the bar the hard way; **re-tasking
builders who are already alive and already idle costs the kill nothing and cannot
violate the non-regression bar by construction.** That is where the first
defensive plank belongs.

**WHAT THIS DOES NOT REVIVE.** `never` killed queue items at the s26 wrap; this
amendment does not restore them wholesale. Each must now clear the
non-regression bar on its own, and heal-idle staffing / home turrets / screening
re-enter as CANDIDATES, not as confirmed planks. Note that s30 measured
`home-turrets-off` at 433/1024 and `barrier-seal-off` at 399/1024 — both REAL
NEGATIVES, i.e. **removing that defensive behaviour cost us**, which is evidence
the amended field was already the truer description of the bot we ship.

**FIXTURE_OF_RECORD: live_unrated.** `bots/*_probe` is a fixture WE WROTE, and
s26 D21 proved it lies in a specific direction: five of our probes share a
`best_core or best_any` short-circuit, so every verdict we ever resolved faced an
opponent that prefers our core over anything else — which is why zero of our
forward turrets died in 480 arena games while **46.9% die on the ladder**.
Magnus's *"beats our own calculations every time"* is therefore not a preference,
it is the already-measured fact. **`fcode match unrated <team_id>` is the
instrument** — 5 games against a real team's real bot, no rating at stake.

**THE CONSTRAINT THAT COMES WITH IT, and it is real:** `fcode match unrated`
plays **our ACTIVE submission**. There is no flag to point it at a local tree.
So testing a prototype against live teams means ACTIVATING the prototype, and
the ladder keeps pairing us (~6 rated matches/hour) for as long as it is up.
**A trick leg therefore costs rated exposure, roughly 2-3 ladder matches per
20-30 minute window, bounded and recoverable by re-activating the incumbent.**
That is the price of the only honest fixture we have. Pay it deliberately:
prototype activated -> burst of unrated challenges -> incumbent re-activated,
with the window and the rated matches inside it recorded.

## KILL-SPEED SCORE — the currency, commissioned by Magnus 2026-08-10

**Magnus commissioned it and confirmed the `PROGRAMME.md` edit directly** (asked
in-session, answered *"Yes i did"*). Spec:
`docs/research/SPEC-kill-speed-score-2026-08-10.md`; implementation
`tools/score.py`, wired into `leg_read.py`.

    core kill <100 -> 10 · <130 -> 8 · <170 -> 6 · <250 -> 4 · <400 -> 2
    slower kill -> 1 · tiebreak/titanium win -> -10 · LOSS (any cause) -> -10
    reported as MEAN POINTS PER GAME

**It SUBSUMES the two fields it replaces.** `core_kill_share` is retained as
SECONDARY because it is the cheaper diagnostic, but the score already contains
it: a kill scores 1-10 and a tiebreak win scores -10, so kill share and
time-to-kill are both inside one number. **`R1000_IS_DEFEAT` is now arithmetic
rather than doctrine** — a tiebreak win scores **-10, identical to a loss**
(Magnus, 2026-08-10: *"we should never optimize for tiebreak wins, all of our
effort should be on killing the cores"*). **This is what keeps the currency
consistent with the defence field:** at 0 a pure survival plank converting
20 losses into 20 tiebreak wins would have scored +200 and looked like a
triumph; at -10 it scores exactly zero improvement. **⭐ THIS SENTENCE SURVIVES
THE 2026-08-11 AMENDMENT AND IS NOW LOAD-BEARING RATHER THAN DECORATIVE.** It
said `PLAY_DEFENCE: never` when written; the field is now
`not_at_the_kill_s_expense`, and **the -10 is what still makes turtling score
zero once the blanket ban is gone.** The ban used to do that work by fiat; the
scoring does it arithmetically, which is why loosening the field did not reopen
the tiebreak-turtle road. Balance property verified
UNCHANGED by the switch (speed +0.75, conversion +0.63, ratio 1.20 either way).

**⛔ IT IS NOT A LEG VERDICT STATISTIC. `KILL_SPEED_IS_LEG_VERDICT: no`.**
Per-game sd is **7.74**, so a realistic change needs **~2,100 games per arm**,
and it carries only **1.1x the power of plain win rate**. **A leg reporting it as
its primary repeats the 2026-08-10 failure exactly — an 18pp bar fired at a
fixture whose own MDE floor was 19.5pp — with a better-looking number.**
Legitimate uses: **version scorecards** (free, spends no games) and the **ship
gate**. `leg_read.py` prints the prohibition on the line itself, because a label
that lives only in a spec is a label nobody re-reads.

**SHIP GATE: beat -1.76 at n >= 200** — RECOMPUTED on the -10 tiebreak scale;
the old **-1.77** was computed under the 0-tiebreak rule and is STALE. Baselines:
v20 **-10.00** · v53 **-2.60** · v72 **-4.20** · v80 **-5.54** · v94 **-5.08** ·
v102 **-2.47** · **v104 -1.76** (best shipped, n=255).
**The rescale changed the HISTORY:** v20 scores exactly **-10.00 over 110 games**
— it never destroyed a core once, every "win" was a tiebreak — and **v53, which
read -1.77 on the old scale and appeared to TIE v104, drops to -2.60.** The old
scale credited tiebreak wins and flattered our early versions into looking like
today's bot.

**THE BALANCE PROPERTY IS A MAINTENANCE OBLIGATION, NOT TRIVIA.** These exact
numbers exist so that speed and conversion are weighted comparably: killing 40
rounds faster across the board pays **+0.79/game**, converting 10 of 109 losses
pays **+0.67/game** — within 20%. **If any bucket edge or the loss penalty
moves, RE-RUN that check**, or speed silently becomes decorative and the score
degenerates into a win-rate proxy with extra steps. `score.py`'s selftest
asserts the ratio and fails loudly if it drifts.

## Exit conditions — the only things that end this programme

1. Magnus says so.
2. The Loki curve crosses Eir on the primary currency AND survives a ladder read.

A Loki iteration that measures null does NOT end the programme. That is what an
iteration is.

## TARGET_MIN_PAYOUT: 10 — re-denominated 2026-08-12 (s33) on Magnus's directive
## (was TARGET_RATING_FLOOR: 1650, added 2026-08-11 (s32) on Magnus's directive)

**The intent is unchanged: do not spend a leg where a win pays nothing.** What
changed is the UNIT. The old form was ABSOLUTE (1650) while the thing it protects
is RELATIVE (payout is a function of the GAP), so it drifted every time OUR rating
moved — and it tightened hardest exactly when we were doing worst. At 1689 it left
39 points of room below us; at 1645 it left NONE and excluded seven teams inside
the reachable band, three of which paid **12.56–15.78** while the rule was written
to exclude targets paying **0.25–0.52**. A payout threshold cannot drift, because
it is denominated in the quantity the rule cares about; no boot rule is needed to
update it because there is nothing to update.

⚠ **Measured and worth knowing: the BAND is tighter than the BAR below us.**
`BAND_LO = -80` already pays 12.38, above the 10-point bar, so the bar **never
binds on the low side** — it is a backstop, not the active gate. That is fine and
is recorded rather than tuned away: a non-binding guard that cannot drift is worth
more than a binding one that drifts wrongly.

**Verbatim: *"Dont fire on targets below 1650 ELO."*** Added under this file's own
rule (*edit ONLY on an explicit directive from Magnus*), which that sentence is.

**WHAT IT DOES.** No live leg may be aimed at a team rated below **1650**,
**regardless of what the reachable band says**. It is a floor on the TARGET, not
on the payoff, and it is **stricter than the reachability gate and supersedes it
where they disagree**. Enforced in `tools/target_value.py` — `RATING_FLOOR`, with
`admissible()` making the floor override the band, five selftest cases driving it
both ways, and the `--band` listing printing an **EXCLUDED BY THE 1650 FLOOR**
section that names every team it removes. **A filter that silently drops rows is a
filter nobody can audit.**

**WHY IT EXISTS.** s28: a crash-induction leg passed every check this repo has and
was aimed at four teams **550–860 points below us**, where a perfect 5-0 pays
**under 5 rating points** against a **−31** loss. The machinery inspected the
experiment and never asked whether the question was worth answering.

## ⛔ THE PART THAT IS INVISIBLE FROM THE DIRECTIVE'S OWN WORDING — READ THIS BEFORE APPLYING IT

**THE FLOOR IS ABSOLUTE AND THE REACHABLE BAND IS RELATIVE, SO THE CONSTRAINT
TIGHTENS AS WE FALL.** *"Don't fire below 1650"* reads as a mild filter. At our
current rating it is **a rule that admits only opponents STRONGER than us.**

| our rating | room below us inside the band |
|---:|---|
| 1689 *(when the directive was given)* | 39 pts |
| **~1663–1666 *(v114, live at 20:35Z)*** | **~13–16 pts** |
| 1650 | **none** |

**ALREADY ARRIVED, AND EARLIER THAN PROJECTED.** At our ~1663 the admissible set
is **11 teams running 1667 (Besvikomat, +4) to 1782 (HTTP 418, +119)** — **every
admissible team is at or above our rating and there are ZERO admissible targets
below us.** That was projected to happen at 1650; it happened at ~1663, because
the floor removed the band's lower half and the remaining field is not distributed
down there.
**AND WE ARE SQUEEZED FROM BOTH ENDS:** Leviathan (1793) was **+124 and admissible
at 1669**; at 1663 it is **+130 and outside `BAND_HI`**. A falling rating costs
targets at the top and the bottom simultaneously.

⇒ **WHAT THIS CHANGES ABOUT LEGGING: every leg from here is against a team rated
above us**, so target selection can no longer trade difficulty for cheapness and
the `0-5 costs` column (**−15.81** at the nearest admissible team) is the one that
moves. **`floor_warning()` fires automatically inside 40 points and is firing now.**
⚠ **A successor reading this field at a 1640 rating will read a mild filter and
get a near-total ban.** That is why the caveat is here and not only in the tool.

## PLAY-IT-WELL RULE (Magnus, direct, 2026-08-23 — verdict discipline, all lanes)

**"There's a difference between playing a tactic and playing it well."** A
refusal or park verdict must contain an EXECUTION-QUALITY line: dose
ACHIEVED vs dose ACHIEVABLE (the achievable reference measured, never
asserted — e.g. heals landed / armed-rounds-with-opportunity; pecks landed /
adjacent-idle-rounds-with-bank). A tactic executing at a small fraction of
its measured opportunity is UNDER-PLAYED, not refuted — the verdict routes
it to execution iteration, and the family's two-strikes counter does NOT
advance on an under-played arm. Same-night provenance, both directions:
the chew give-up clock was NEVER in force (memo bug — a "tested policy"
that was dead code), and the core heal-stand sat disarmed behind four
stacked gates (152 armed rounds, zero heals) — "we play tactic X" must be
verified as executed, not read off the code's intent.

## THREE-PLANK LOCK (Magnus, direct, 2026-08-23 — supersedes the try-and-discard flow)

**"We no longer try planks and throw them away, pick three planks, we will
iterate on these until they work and we do them excellently, we only
iterate on arms."** The three planks, chosen by the builder from the
banked loss autopsy and locked until Magnus says otherwise:

1. **THE BATTERY** — concurrent sentinel firepower on the enemy core (the
   rolling-battery doctrine played to spec: 4 together, rolling). Owns the
   gross-rate constraint (need ~4.5 HP/r; one sentinel caps ~2.4). The
   refused SK_AMMO_PUSH is retained as a FUNDING ARM of this plank.
2. **THE STAND** — our core survives the siege (SK_CORE_STAND adopted as
   arm 1; known execution ceilings: walled-in heal seats 1.54/8 free,
   enemy medic-taxi, staffing). Owns the 54-round closing window.
3. **THE ROUTE** — titanium delivered home (mine rate 1.21 vs 2.39,
   out-mined 38/41 losses, 13 zero-delivery cells with routeless
   harvesters). Owns the delivery input and the tiebreak games.

**RULES:** no new plank families without Magnus; iteration = new ARMS of
these three, each arm registered/screened/verdicted per the standing
method WITH the play-it-well execution-quality line; a failed arm routes
to the next arm of the same plank, never to a new plank; "excellent" =
the plank's dose-achieved approaches its measured dose-achievable, and
the victory bars (>=16/30 per fixture; currently 10/9/16) are the
campaign scoreboard.

## ECO-READY HAMMER (Magnus, direct, 2026-08-23 — supersedes the hard r300 flip)

**"The eco + defence line was so that we learn how to play those well. If
we don't play them well, we will never beat the better teams. We don't
have to lock a hard round for the sentinel barrels at r300, we should
probably have an economy level we look for when we're funded enough to
hammer the other team's core."**

Operational form: SK_PHASE_ROUND=300 as a hard boundary is RETIRED from
doctrine. The hammer (the full battery: barrels at concurrency + the ammo
stream) opens on an ECONOMIC READINESS trigger — funded enough to sustain
~2.5-3 Ti/round of ammunition plus barrel replacement (the banked
requirement for ~4.5+ HP/round through enemy core-heal absorption,
LOSSAUT-f1f2). The cheap standing pressure pair may exist earlier;
the HAMMER waits for funding, not for a round number. Eco+defence
excellence (THE ROUTE, THE STAND) is the foundation the trigger stands
on — played well first, because the readiness level is reached through
delivery. The readiness latch's exact in-bot read is design work for THE
BATTERY's arms (registered per arm); it must be an honest live signal
(bank + income trend), never a wall-clock or round constant.

## SMALL-STEPS SCALING (Magnus, direct, 2026-08-23)

**"Iterate in small steps, try something small that does something in the
right direction and then scale it up from there."** Operational form, on
top of the three-plank lock: each arm ships the SMALLEST change that can
show direction — one rung, one constant, one predicate — screened for
SIGN before size; a confirmed direction then scales in registered
increments (dose up, scope up) with the same guards at each step. A
composed arm is admissible only after its pieces have each shown
direction (or a piece is measured inert alone and the composition IS the
smallest step that can show direction — disclosed as such). Verdict
language: "direction confirmed, scaling" / "direction absent at smallest
dose, arm re-aimed" — never a big-bang arm whose failure can't name which
piece failed.

## THE KILLBOX (Magnus, direct, 2026-08-23 — raider-body answer, STAND plank head)

**"Place a sentinel and make a small pocket with barriers they can't
escape... build the sentinel + pocket early and make it as optimized as
possible. If we destroy raiders quickly we lose less infrastructure. As
soon as they are within reach plant a launcher near it to throw it to
the pocket."** Engine basis (verified rules, probe pending): sealed
4-barrier pocket is a legal throw target (passable), trapped builder has
no cardinal move, sentinel ray IGNORES OBSTACLES (executes through the
wall, 3 shots / 30 ammo), external heal impossible (orthogonal-only),
and the unhardened half of the field self-retires on a blind move()
(GameError = permanent, the approved class). Launcher planted reactively
when a raider stops to work (pickup d²<=2, throw d²<=26). Build EARLY at
low scale (~42 Ti base for box+sentinel). Sequence: engine probe of the
full choreography FIRST (small-steps), then the registered arm.

## THE BOX IS THE SIGNATURE MOVE (Magnus, direct, 2026-08-23)

**"Iterate on the box until it works please, this is our signature move
going forward. It needs to be able to handle quick rushes from teams
that use launchers to get to the other side."** Standing mandate: the
killbox family iterates until it works — Magnus's order EXEMPTS it from
the two-strikes park; failed arms route to the next box arm, always.
REQUIREMENT: the box must answer EARLY LAUNCHER-RELAY RUSHES (the banked
prediction study: Baltsars/Mjolnir relay raiders across at r1-r5 with
ammo by r5) — so the family's arms must cover the EARLY game: cheap
edge/corner pockets built in the opening at low scale, the exile
launcher planted on the measured rush corridors, and a reactive
treadmill (throw-back) that works BEFORE any pocket exists. The engine
probe (in flight) stamps the mechanics; every arm carries the
seen-choosing and play-it-well disciplines like any other.

## THE TRIANGLE (Magnus, direct, 2026-08-23 — the game's three parts and their order)

**"We have three very strong parts to our game now, eco, defence and a
finisher, which we can optimize further once eco and defence are tight."**
Optimization order under the three-plank lock: (1) DEFENCE TIGHT — the
box family to its working form (arm 3 speed package in flight; lean
3-site config: launcher + 2-chamber detention, no execution, peel where
free); (2) ECO TIGHT — the ROUTE arms: stand-smart laying (the 33%
stance rule), ore-by-route-length (rounds-to-first-delivery as the
planner objective), nearest-builder task assignment; (3) FINISHER
OPTIMIZATION LAST — battery scaling (barrels, exile-medics guard-breaker
with the sleeping-dogs rule) once 1-2 hold. Every arm keeps the standing
bars; the tempo bar binds all three (nothing may slow the kill).

## VICTORY-BAR CONFIRMATION STANDARD (s57 2026-08-23, ratified in-session)

The vh1build noise-floor measurement (a ZERO-dose flag moves a 30-cell
fixture's win column ±3-4 via trajectory divergence at fixed seed) binds
the victory condition's reading: a single-tape 16-19/30 is AT THE BAR,
UNCONFIRMED; a bar is DECLARED HELD only by >=20/30 on one tape OR
>=16/30 on the CONFIRMATION BATTERY (3 seeds x 30 cells per fixture,
floor ~±2). Iteration stays on single tapes reading direction+mechanism;
claims pay for replication. Current standing under this standard: F3
19/30 AT THE BAR UNCONFIRMED (battery scheduled behind the Sentry
verdict); F1 11, F2 10 — short outright.

## CONFIRMATION STANDARD AMENDED (s57 — the battery's own finding)

The 3-seed battery measured THE SEED INERT vs deterministic fixtures
(outcome columns bit-identical across 4 seeds — the fixture rule's own
"vary MAP and SEAT, never seed", re-learned): a 30-cell tape vs a
deterministic opponent is a CENSUS, not a sample. RESTATED: (1) a bar
vs the NAMED fixture is met exactly by the census — **F3 19/30 = HELD
with certainty vs opp_sleipnir2**; (2) the ±4 floor governs ROBUSTNESS
(generalization under perturbation — opponent drift, new maps, the live
field), which seeds cannot test; (3) the ROBUSTNESS instrument is
opponent variation: version-pinned variants locally, and THE LIVE
UNRATED FIELD as the instrument of record (doctrine point 6 alignment).

## THE IDENTITY INVERSION + THE ASSEMBLY MANDATE (Magnus, direct, 2026-08-23/24 night)

**The live leg's verdict on the objective function: seven hardening
adoptions and zero identity planks shipped = local screens vs our own
siblings can only converge to a polished chassis. And the field ruled:
Jython v266 swept us 5-0 playing THE SKALMAN DOCTRINE ITSELF (zero
launchers/barriers/gunners; pure eco -> standoff sentinels d²16-25).**

STANDING ORDER: **SKALMAN'S IDENTITY IS THE FIXED POINT; EXECUTION
ITERATES.** Screens are demoted to execution debuggers — "the doctrine
bot loses to the chassis locally" is information about execution, NEVER
an argument against the identity. The live field is the only judge of
identity (point 6, now structural). The chassis is the fallback, not
the incumbent.

THE ASSEMBLY (SK_DOCTRINE): home economy + defence until the eco latch;
NO forward bodies pre-latch (no rush — the line's stated identity);
defence = THE SENTRY (turret answers KEPT — Magnus explicit: "I'm not
saying you can't destroy enemy offense turrets, do it") + THE BOX with
TO-CELL PRIORITY for raider bodies (Magnus: "we need to get the raider
into the box otherwise it just builds more turrets" — turret-killing
without builder-boxing is whack-a-mole, measured in the leg's S5);
the bank accrues; on latch fire the burst: raiders out, standoff
4-sentinel battery in the d²16-25 band (the field's own winning band),
conversion sized to the kill (~280-350 ammo). Substrate: every adopted
hardening plank stays ON.

GOVERNANCE FIX: the drift watch gains a BEHAVIOURAL-IDENTITY row — per
adoption/wrap, decode the current bot's play (rush check, box check,
phase check) and diff against the declared identity; encoding-level
compliance is not identity-level compliance (the s57 lesson).

## THE FINAL STANDING ORDER (Magnus, direct, endgame — supersedes per-window asks)

**"Work until we have the bot we have talked about and until it beats the
nearest band in unrated games. Don't stop until we do, no questions, just
build. Use unrated games as much as you want. I'll only intervene if I
feel you need a push."** Operational form: the builder runs autonomously
to TWO exit bars — (1) SK_DOCTRINE assembled and verified as specified
(no-rush phase, box with to-cell priority, sentry, bank, standoff
burst); (2) it BEATS THE NEAREST BAND live: net winning game share vs
in-band opponents (target_value --band) over the accumulated unrated
record, sustained across >=3 cells — not one lucky window. Platform
autonomy for unrated windows is STANDING (the zero-leak procedure
remains mandatory; the GO is no longer per-window). The side lane holds
the path per Magnus: any drift from the identity gets flagged against
D38, and the builder answers flags with corrections, not compliance
theater.
