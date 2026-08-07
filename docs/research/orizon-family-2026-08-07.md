# Orizon family cross-check — 2026-08-07

THREAD 2 of `docs/research-brief-2026-08-07b.md`. Read-only: no bot edits, no submissions, no
arena runs, no unrated challenges. `fcode match info` used freely (cheap); `fcode match replay`
budget was **8/8 downloads, all landed, paced >=60s apart** (one process-management hiccup mid-run
— a manual `&`/`disown` double-backgrounded the first launch and produced a premature completion
notice; the underlying orphaned process was killed cleanly after 1 file and the download plan was
relaunched properly through the harness's own `run_in_background`, so pacing was not violated and no
extra requests were issued beyond the planned 8). Every replay decoded with
`docs/research/2026-08-07-fanout/toolkit/replay_lib.py`; **all 18 decoded games (10 team lazy + 5
Orizon + 2 Team 48 + 1 Askar City) passed every `check_all()` self-check** (delivery×10 ==
titaniumCollected, ammo converted−spent == final, no unknown fields, no id reuse, HP in bounds,
winner-vs-dead-core consistent). Map identity for every game resolved by fingerprint
(width/height/walls/ore/core-anchors) against `maps/*.map26`, not by trusting a name string.

**Budget accounting.** team lazy fully covered by `replay_archive/` (2 match ids, 10 games, 0
downloads). Orizon confirmed absent from the archive, per the brief's own steer, got the largest
share: all 5 games of `607ffaeb-4574-4ea0-8e73-f811c976c727` (its most recent series, vs our
**current live v64**). Team 48 got 2 games of `bce041d8-e96c-4871-8d6a-c3523af3ac24` (g3 fjordgate —
an anomalous tiebreak loss for us; g5 nordkap — the fastest kill in the series). Askar City got 1
game of `3c61b886-4d08-49a9-baed-c12ae050622d` (g4 nordkap — its only win in that series; the other 4
losses are already well characterised by the census and denial-book). `match info` for all three was
already cached in the session scratchpad (apparent prep by a sibling thread) — zero-cost reads, not
counted against the 8.

## Headline correction before anything else

**Orizon no longer beats us more often than not.** `607ffaeb` (Orizon v34 vs OpenSverige **v64**,
completed 2026-08-07T11:57:58Z) is **3-2 in our favour** — the first Orizon series in the record
where we win the match. This directly revises thread7's "Orizon has not adapted; we simply have no
answer" verdict, which was built entirely on v53/v56/v61 data. The correction is real but partial:
we won 2 of 3 by **tiebreak** (economy), not by denying the siege outright, and the 2 losses still
show the old kill shape. Detail in §6.

## 1. Plant-distance progression

fp_dsq = squared distance from each successive turret's spawn tile to the *opponent's* nearest core-
footprint tile, in build order (thread7/denial-book convention). Gunner unless noted.

| Team (ver) | Match, game | Progression (fp_dsq, build order) | Shape |
|---|---|---|---|
| team lazy v88 | `ed29909b` g4 (vs sporks) | 9, 8 | matches signature (2 plants, fast kill r64) |
| team lazy v88 | `52426cf4` g1 (vs Jacobs Code) | 8, 5, 2 | matches signature, monotonic |
| team lazy v88 | `ed29909b` g1 (vs sporks, 528r) | 8,9,5,1,2 then **101,100,100,100,145** | matches, then a **second wave** far out after the first battery dies (r171+) |
| Orizon v34 | `607ffaeb` g2 (lighthouse, **Orizon won**, r144) | 9,16,9,20,9,**1,1**,5,5,5 | recognisable creep-and-hold, noisy from repeated kills |
| Orizon v34 | `607ffaeb` g3 (nordkap, **Orizon won**, r550) | 9,25,37,101,101,170,**1**,82,169,5,5,**2**,16,18,13,13,4,**1**,4,8,5,4,5 | reaches d1-2 repeatedly but **not monotonic** — 23 plants total |
| Orizon v34 | `607ffaeb` g1 (antler, **we won**, tiebreak r1000) | 9,16,37,82,37,20,82 | **signature broken** — never closes past d9 |
| Orizon v34 | `607ffaeb` g4 (moonrise, **we won**, core_destroyed r133) | 9,5,13,9,9,17,**2,1**,1 | reaches d1 late (r92,124) but from a noisy base, and their own core died first |
| Orizon v34 | `607ffaeb` g5 (archipelago, **we won**, tiebreak r1000) | 162,181,288,369,369,389,452,369,450,369 | **never remotely close** — largest map in the pool (sep 19.8), no creep at all |
| Team 48 v16 | `bce041d8` g3 (fjordgate, Team48 won, tiebreak r1000) | 5,4,2,2,2,**1,1,1,1**,5 | cleanest match to the signature in this whole dataset |
| Team 48 v16 | `bce041d8` g5 (nordkap, we won, r75) | 2,5,5,9 | opens already close, does not monotonically tighten |
| Askar City v72 | `3c61b886` g4 (nordkap, Askar won, r323) | **sentinel** 9 [dies r11], **sentinel** 5 | only 2 plants in 323 rounds — one commit-and-hold, not a sustained creep |

**Read:** the dsq-16→9→4→2→1 signature thread7 documented on old versions (v53/v56/v61) **holds
cleanly only when the family member wins or the game is short**. In the 3 fresh Orizon games we won
against current v64, the progression is either badly noisy (g1, g4) or never engages at all (g5) —
Orizon is visibly failing to execute its own script, not choosing a different one. Team 48's g3 is
the cleanest reproduction of the classic shape in the whole sample. Askar City's sentinel variant
does not "creep" in the repeated-replant sense at all — it commits once and holds.

## 2. Target priority

Two metrics: **first-aggression aim distance** (census's own metric: Euclidean distance from the
first damaged entity to the opponent's core NW corner) and **whole-game core-fraction** (distinct
targeting decisions collapsed per thread5's methodology — a shot counts as a new decision only when
the chosen target id differs from that shooter's immediately preceding pick; this discounts sentinel/
gunner reload spam, e.g. team lazy's raw 824 shots in `ed29909b` g1 collapse to 217 real decisions).

| Team | First-agg aim dist (n, range) | Whole-game core-frac (range) | Note |
|---|---|---|---|
| team lazy v88 | 0.0 in **6/10** games, range 0.0-2.24 | **0.02 – 1.0** | reproduces census's own 6/10, sd 0.9 exactly; core-frac collapses toward 0 specifically against sporks' huge conveyor mass (`ed29909b` g1: 177/217 decisions are conveyor) — the gunner is not choosing economy, it is hitting whatever is first in a straight, obstacle-blocked ray |
| Orizon v34 (fresh, v64) | 0.0 in 1/5, **14.14 in g5** | **0.0 – 0.2** (low across the board) | a sharp departure from thread7's "aim distance 0.0-2.2 sd 0.9" — g5 archipelago's first hit is 14.14 tiles from the core; whole-game core-frac is low because most decisions land on builder_bot (melee/counter-fire exchanges) |
| Team 48 v16 | 0.0 in **2/2** | 0.64 – 0.83 | matches census's "sd 0" aim claim tightly; the most core-locked of the four |
| Askar City v72 | 1.0 (n=1) | 0.33 | 2 of 9 distinct decisions hit our conveyor (`3c61b886` g4) — a minor discrepancy against census's "eco damage exactly 0 in all 5 games" claim; likely near-zero in raw-damage terms but not literally zero in target selection |

**Mechanism, not policy.** Gunners fire a straight, obstacle-blocked line (CLAUDE.md). None of the
four teams show evidence of an actual priority *table* — what they hit is simply whatever first
occupies their firing ray. That ray is aimed at the core on the opening plant (hence aim-dist ~0 in
the majority of games) and stays aimed there as the family member re-plants closer, so "core-always"
is an emergent property of a fixed facing plus a short, obstacle-free ray, not a target-selection
rule with alternatives being weighed.

## 3. Ammo cadence

`ConvertAmmo(round, team, amount)` events + `ammo_curve`.

| Team | Opening pattern | Steady drip | Max bank observed | Bank at strike vs quiet (median) |
|---|---|---|---|---|
| team lazy v88 | **12, 12, 12** triple-convert, near-identical opening in **9/10** games | 4s and 8s | 36 (up to 45-46 in 2 games) | strike lower than quiet in every game (e.g. `ed29909b` g1: 28 vs 36) — spends down while firing, refills while quiet |
| Orizon v34 | small-then-spike (`607ffaeb` g1: 2,4,10,14,14,14…; g2: 2,**76**,13,10,19…) | 4-10 | **120** (g1, g3, g5 all cap at 120) | quiet bank often *at* the 120 cap (g1, g5) — far larger reserve than team lazy, matching its much larger gunner count (up to 23 in g3) |
| Team 48 v16 | opens ~20, drips 4s | ramps to 10-20 in the 1000-round game | 35-47 | strike 28 vs quiet 1 in `bce041d8` g3 (bank genuinely drawn down under fire, unlike team lazy) |
| Askar City v72 | **60, then 110** — big opening chunks | 3-10 | **160** | reflects the sentinel's 10-ammo/shot cost vs gunner's 4; consistent with the family's shared "bank up front, drip after" cadence even though the unit economics differ |

All four share the same shape — **front-load the bank, then top up in small increments to match
spend** — scaled to whichever turret type they run. Team lazy's cap (36) and Orizon's (120) differ by
roughly the ratio of their peak simultaneous gunner counts, not by a different policy.

## 4. Response to disturbance

`heals_after` = heal actions landing on the exact damaged tile within 6 rounds of the hit (own
`heal_log`).

| Team | Pattern when its own turret/builder takes damage | Cited instance |
|---|---|---|
| team lazy v88 | **Mostly unsupported.** `heals_after=0` in the immediate aftermath in 8/10 games; two games show a slow-building heal response (`ed29909b` g5: 0→2 heals across r39-43; `52426cf4` g5: up to 7 heals) but usually after the gunner has already taken lethal damage | `52426cf4` g2, gunner#10 @(4,4): hit r2-r6, `heals_after` climbs 6→7 but the gunner still dies at r8 |
| Orizon v34 | **Actively supported**, matching thread7's old finding — heals_after 1-9 in most disturbance events (`607ffaeb` g2: gunner#19 gets 3 heals across r10-12 before dying anyway to an -18hp sentinel hit) — but the support is now frequently **insufficient**: gunners still die within 2-10 rounds of planting in 4 of 5 games | `607ffaeb` g4, gunner#12 @(11,3): heals_after climbs 7→9 across r4-r8, dies anyway at r8 to a combined builder+sentinel hit |
| Team 48 v16 | **Unsupported**, same as team lazy — `heals_after=0` in every disturbance event observed in both decoded games | `bce041d8` g3, gunner#18 @(2,5): -18(sentinel)/-2(builder)/-2(sentinel)/-18(builder) across r8-r10, zero heals, dead r10 |
| Askar City v72 | **Unsupported**, fast kill — sentinel#16 @(9,15) takes 4 hits (-18/-2/-18/-2, alternating our sentinel and a builder peck) across r8-r11 with zero heals, dead r11 | `3c61b886` g4 |

**Family-relevant split: Orizon defends its front gunner; team lazy, Team 48 and Askar City do not.**
This is the clearest behavioural fork inside the "family" — three of four members leave their
creeping turret to die unsupported, which is exactly the profile a counterbattery-first response
punishes hardest. No clean "plant tile occupied" or "builder body-blocked" instance was captured in
this sample (would need denial-style pre-occupation, which none of these games show us attempting);
the closest analogue is Orizon `607ffaeb` g2 rebuilding on the *exact same tile* (11,8) three times
(r9, r13, r20) after each occupant dies, rather than diverting to a different tile — i.e. no visible
tile-avoidance behaviour when a preferred plant is repeatedly destroyed.

## 5. Economy underneath

| Team | Harvesters/conveyors **built** (range across games) | Harvesters **alive** at r200 (median, n games reaching r200) | Delivered Ti (range) |
|---|---|---|---|
| team lazy v88 | harv 1-11, conv 5-58 | **0** (n=3: 8, 0, 0) | 170 - 4390 |
| Orizon v34 (fresh) | harv 1-9, conv 1-26 | 0 (n=3 games reach r200: 0, 0, and 2 in one) | 90 - 8910 |
| Team 48 v16 | harv 2-8, conv 3-27 | n/a (only 1/2 decoded games reaches r200: 1) | 0 (our g3 delivery) - 2560 |
| Askar City v72 | harv **1**, conv 14 | 1 (n=1) | 780 |

**Correction to the census/thread7 "0-1 harvesters" / "Orizon 4 builders ever" claims, confirmed on
fresh data.** "0-1 harvesters" is an *alive-at-r200/500/800* statistic, not a built count — every
family member **does** build a handful of harvesters early (matches, not contradicts, the census once
the metric is read correctly). **"Orizon 4 builders ever" is false on the fresh series and needs
retiring as a general claim**: builder_bot **built** counts in `607ffaeb` are 7, 5, 12, 4, **45** across
g1-g5. Only g4 (moonrise, r133 — the shortest game) matches "4, never respawn." The two 1000-round
games (g1: 7 builders, g5: **45** builders) and the 550-round game (g3: 12 builders) show Orizon
clearly respawning well past its old ceiling. Read as: the "exactly 4, never respawn" rule is a
short-game artefact of thread7's 90-350-round sample: Orizon appears to hold a round- or resource-
gated respawn policy that a 6-game sample capped under 350 rounds never triggered.

**Our own economy is the swing variable, not theirs.** In `bce041d8` g3 (Team 48, fjordgate) **we
delivered 0 titanium in 1000 rounds** against Team 48's 2560 — we lost that tiebreak to our own
economy collapse, not to Team 48's strength (8 harvesters built, comparable to our own typical
range). In `607ffaeb` g1 and g5 (Orizon, antler and archipelago) we won because our economy
(5110 and 25340 Ti delivered) dwarfed Orizon's own anaemic output (1880 and 8910) — and notably in g1
**our own builder-bot population sat at zero for 317 consecutive rounds (r107-r424) while our
titanium bank reached 4198** (nowhere near a floor problem) and delivery kept climbing regardless,
because harvesters/conveyors are buildings that keep operating without a living builder — only
construction/repair/counterbattery capability is lost. This is a precise, evidenced test of piece B'
(population-floor respawn, unshipped): in this game it would have restored defensive capability, not
economy, since the economy survived the builder-zero window on its own.

## 6. Verdict — one mechanism with real variation, not four independent designs

**team lazy, Orizon and Team 48 are one code family: gunner-only, zero sentinels/launchers/barriers
(confirmed 10/10, 5/5, 2/2 decoded games respectively), a creeping-closer plant policy that a
straight-line firing ray turns into apparent "aim at the core," and a front-loaded ammo bank.** Askar
City is **convergent, not the same family**: it is a sentinel-plus-launcher-plus-barrier build (the
family's defining "zero-everything-else" signature is absent), commits its turret once rather than
sustaining a repeated creep, and opens with a fixed launcher-then-conveyor script the other three
never show. It reaches the same *outcome class* (point-blank core siege, minimal economy) by a
different, simpler mechanism.

**Where the three gunner-family members diverge from each other**: (a) Orizon defends its front
gunner with heals; team lazy and Team 48 mostly do not (§4) — this is the single most exploitable
difference. (b) Orizon's economy and builder-respawn ceiling scale with game length far past the
old "4 builders" reading (§5); team lazy and Team 48 were not observed doing this, though the sample
is smaller. (c) Team 48's plant progression is the cleanest match to the textbook signature; Orizon's
own is now visibly degraded against current v64 (§1).

**Piece routing, against what we actually ship today (`bots/_v74e4/main.py`, live v64):**

- **Piece D (duel discipline) — SHIPPED.** `_duel_safe()` (line 1351) gates builder melee against a
  live gun to: nearly dead (`HUNT_FINISH_HP`), volume (a second friendly builder already adjacent),
  or off-ray. It governs whether *our builders* peck the family's gunners — a minor contributor
  (the -2hp builder pecks visible throughout §4's disturbance logs), not the mechanism that actually
  kills them.
- **Piece J (heal-dispatch reorder) — CONFIRMED STILL NOT SHIPPED**, verified by direct code read,
  not just HANDOVER's build queue. The universal adjacent-heal check at line 1236-1238
  (`if ct.get_action_cooldown() == 0 and ct.read_store(SLOT_UNDER) != 0: if self._heal_core(ct): return`)
  still sits above role dispatch exactly as thread7 described in `_v72e2`. `_defend()`'s own internal
  ordering (line 2109-2132) now tries counterbattery *before* falling back to heal when the core is
  merely "under" (proximity-flagged) but not yet "shelled" (actually losing HP) — but the code's own
  comment at line 2119 calls this "belt and braces... if that call site ever moves," i.e. an
  acknowledgement that the universal gate still dominates once the core is actually bleeding. **Piece
  J would still matter**: it is not what is winning the fresh Orizon games.
- **Piece B' (population-floor respawn) — CONFIRMED STILL NOT SHIPPED.** Directly relevant per §5's
  g1 finding (317-round builder-zero window despite a 4198 Ti bank) — but in that specific game the
  economy did not need it to win. B' would matter for defensive/counterbattery capacity during a
  builder-zero window, which is a real, observed state in this sample, just not the one that decided
  g1.

**So what is actually killing the family's gunners in the 3 fresh Orizon wins and in the Team
48/Askar wins?** Not J, not B' — both are absent from the live code. The evidence points to the
**pre-existing counterbattery/hunt machinery already firing successfully before the heal-lock can
engage it**: `_try_counterbattery`'s only gate once a first home gun exists is
`SLOT_HARVESTERS < ECO_NEED` (`ECO_NEED = 3`, line 1999/27) — cheaply satisfied in most games — and
the universal heal at 1236 only returns early when `_heal_core` actually finds damage to repair
(`can_heal()` refuses a full-HP core), so **early, pre-damage counterbattery is not blocked by the
heal-lock at all** — only a core that is already bleeding blocks further counterbattery, which
matches why Orizon's front gunners now die in single-digit rounds (`607ffaeb` g2: gunner#19 dead r12,
built r9; g4: gunner#12 dead r8, built r4) rather than surviving 80+ rounds unanswered as in thread7's
old sample. This reads as an emergent interaction of already-shipped pieces (A+B siege solvency, C
early medic, and the existing counterbattery/hunt code), not a specific fix for this family — which
is exactly why 2 of 5 Orizon games (and Team 48's tiebreak game) are still losses: the mechanism is
opportunistic, not guaranteed.

**Practical answer to the brief's question**: yes, one mechanism (gunner-only creeping battery)
covers team lazy + Orizon + Team 48 with real confidence, and the single highest-leverage fix
remains **piece J** — because it is the one piece that would convert the *already-working*
early counterbattery into something that keeps working once the core starts bleeding, which is
precisely where the 2 current Orizon losses and the Team 48 tiebreak loss are still falling through.
Askar City should be tracked separately; it is not the same family and a J-shaped fix is not
obviously relevant to a single-commitment sentinel (its kill in `3c61b886` g4 already dies to
counterbattery in 4 rounds, r8-r11, with no heal-lock interaction visible at all).

## 7. Rider — cardinal vs diagonal core-offset, by team's own W/L record

Using already-cached `match info` (`per_opp_games.json`: 25 Orizon games / 5 series, 25 Team 48
games / 5 series, 15 Askar City games / 3 series — built by a sibling thread, zero additional
downloads) plus team lazy's own 10 decoded games. Map axis resolved once per map name from
`maps/*.map26` core-anchor parity (6 cardinal: antler, eider, heart, meander, moonrise, nordkap; 9
diagonal: archipelago, atoll, drumlin, fjordgate, hive, jackpot, lighthouse, saga, snowflake) —
zero fcode calls.

| Team | Cardinal W-L (win%) | Diagonal W-L (win%) |
|---|---|---|
| Orizon v34 | 2-6 (25%) | 11-6 (65%) |
| Team 48 v16 | 2-6 (25%) | 9-8 (53%) |
| Askar City v72 | 2-3 (40%) | 1-9 (10%) |
| team lazy v88 | 2-1 (67%) | 6-1 (86%) |
| *(sporks v2, cited for comparison)* | *9-0 (100%)* | *6-10 (38%)* |

**The axis effect is not map-level — it flips direction by team, so it is a strategy property, not a
map property.** Orizon and Team 48 (both sustained-creep aggressors) do *worse* on cardinal maps,
the opposite direction from sporks (a mid-map screener) and Askar City (single-commitment sentinel),
both of which do *better* on cardinal. team lazy wins most of its games regardless of axis (it is a
much stronger bot, 1892 rating) with only a mild lean toward diagonal. A whole-roster aggregate check
(our own win/loss across every mid-pool opponent in the cached sample, 300 games) shows **we**
ourselves do somewhat better on cardinal maps overall (63-51, 55%) than diagonal (85-101, 46%) — so
Orizon/Team 48 doing *worse than their own average* on cardinal against us specifically is a real
opponent-vs-map interaction, not just "cardinal maps are easy for everyone." Same caveat sporks'
own decode flagged applies here: cardinal maps in this pool are also lower core-separation on
average (cardinal sep range 7.0-12.0, mean ~10.0; diagonal 5.66-25.5, mean ~17.4, fjordgate the one
low-separation diagonal outlier) — axis and separation remain confounded, and per-team sample sizes
(5-25 games) are small enough that individual splits should be treated as suggestive, not final. Our
own bot's code also hard-codes per-map special cases by exact core coordinates (`chase_battery` for
nordkap (9,6)/(9,18), `hive_bunker` for hive (21,3), `snowflake_home_b`, `keep_artillery_forward` for
moonrise/nordkap/antler — `bots/_v74e4/main.py` lines 1244-1279, 2073-2104) which is an additional,
directly-visible confound: some of the per-map variance may be *our own* hand-tuning rather than a
property of the axis or the opponent.

## Not-run / caveats

- Team 48 decoded on 2 of 5 games (fjordgate tiebreak loss, nordkap fastest win); the other 3
  (`bce041d8` g1 moonrise, g2 lighthouse, g4 hive) were not downloaded — budget discipline, not
  doubt; the 2 decoded games already contradict a literal "98% core, sd 0" reading once economy
  swings are accounted for (§5).
- Askar City decoded on 1 of 5 games (its only win). The 4 losses are not independently re-verified
  here beyond the census/denial-book citations already on record.
- No "plant tile pre-occupied by us" or "builder physically body-blocked" instance was observed in
  this sample — none of these games show us attempting pre-occupation denial, so the response is
  untested rather than confirmed absent. The tile-reuse behaviour in Orizon `607ffaeb` g2 (§4) is the
  closest available evidence and points at "no avoidance," but it is a rebuild-after-death case, not
  a blocked-build case.
- The "why do we now beat Orizon 3/5" analysis in §6 is inference from code + replay evidence, not a
  controlled ablation — attributing the effect to the counterbattery eco-gate rather than to some
  other shipped piece (or plain variance in a 5-game sample) is the most consistent read available,
  not a proven mechanism. A same-map rerun against `_v74e4_noD`/an Eir-2 baseline would settle it and
  was out of scope for a read-only 8-download budget.
- Rider sample sizes (5-25 games per team) are small; treat the cardinal/diagonal splits as
  directional, matching sporks' own decode's caveat about the same confound.
