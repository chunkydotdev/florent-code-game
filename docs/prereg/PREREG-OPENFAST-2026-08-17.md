# SCREEN PREREG — `OPENFAST`: the economy is born on the wrong side of the core

Drafted by a fresh opus subagent with no inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `BARS.tsv` row, fired no game, started no shard, and
touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md` nor
`QUEUE.md`.

**STATUS: committed BEFORE the `OPENFAST` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any file named
`scratchpad/overnight/OPENFAST.*` exists, and BEFORE the leg's first game.**
Drafting session wall clock at write time **`2026-08-17T07:49:55Z`** (`date -u`,
same shell call); repo HEAD at draft `006c4642` (author time
`2026-08-17T09:49:04+02:00`). Verified at draft:
`grep -c 'OPENFAST' scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; `ls scratchpad/overnight/ | grep -i openfast` →
**empty**; `grep -n '836000' scratchpad/corefill_work.txt scratchpad/fleet_queue.tsv docs/prereg/*.md scratchpad/overnight/*.tsv` →
**no match** (the seed base is free; the collision audit is under `SEEDS` below).

⚠ **The treatment tree ALREADY EXISTS and is committed** (`bots/_v486openfast`,
added `78965d91`, author time `2026-08-17T09:23:55+02:00`). That is legitimate —
built and demo-verified before any registration — but this document is **NOT**
locked before the arm exists, only before the arm's first screen row. Said here
rather than left for a certifier to find. It is also what makes Obligation 13's
intersection **computable at lock time**, and it is what let this drafting agent
recompute the demo aggregate itself (see `DOSE`).

### LOCK, clock 2 (local shard) — the corrected boilerplate, cited not restated

Per `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md`
Addendum 2026-08-17T07:24:55Z (which exists because the sentence eleven preregs
copied names an instrument a third of our local tapes and **0 of 86** remote
tapes have):
**PRIMARY clock 2 = the shard tape's own `# FIXTURE … start=` stamp**
(`tools/overnight.sh:99` sets `START`, `:103` writes it to `$ROWS` before the
first `fcode run`), quoted verbatim beside this document's git author time.
**BACKSTOP, if `scratchpad/overnight/OPENFAST.tsv` carries no `# FIXTURE` line**
(a `# FIXTURE-RESUME … start=UNKNOWN-legacy-tape`, or a remote tape if
AMENDMENT-1 ever moves this shard): **the tape's FIRST COMPLETED ROW `ts`**,
which is conservative by construction — the true start is strictly earlier than
the first completion, so the backstop can only ever **OVERSTATE** the
prereg-to-start gap, never invent one (measured substitution cost on the 107
tapes where both exist: 1–2 s).
**The certificate must state which of the two it used.**

---

## ⛔⛔ READ BEFORE RATIFYING — SEVEN THINGS THE LANE OWNS. **#1 AND #4 ARE LOCK BLOCKERS AND #4 WAS NOT IN THE BUILDER'S SUMMARY.**

**1. ⛔⛔ THE ARM WILL BE ADJUDICATED AGAINST 55.0, NOT 51.33, AND THE REGISTERED
BAR IS THEREFORE UNREACHABLE AS THE FIXTURE IS CURRENTLY CONFIGURED. THIS IS A
FAMILY-WIDE DEFECT, NOT AN OPENFAST ONE, AND IT MUST BE RESOLVED BEFORE LOCK.**
`tools/auto_gate.py:715-741` (`combo_of`) decides COMBO-vs-SOLO by grepping the
**treatment tree's own `doctrine.py`** for `composed by tools/stack.py from:`.
**`bots/_v486openfast/doctrine.py:1878` carries that marker** — verbatim
`# ---- composed by tools/stack.py from: turbo (_x3r0v152), bodyaware (_v242bodyaware), samestop (_v464samestop)`
— **inherited from the control**, because `bots/_v468kladturbo` (Sleipnir v1) is
itself a hand-merge that deliberately types stack.py's phrasing so it "reads as a
COMBO" (its own comment, `doctrine.py:1881-1886`). Counted at draft:
```
_v468kladturbo 1 · _v477ecommit 1 · _v478freeround 1 · _v479routescore 1
_v480beltbreak 1 · _v483beltbreaklate 1 · _v486openfast 1   (marker count per tree)
COMBO-BAR-EXEMPT tokens in the whole of docs/prereg/BARS.tsv: 0
```
⇒ **`auto_gate.py:952-958` will fire `COMBO-BAR@2700` and STOP any of these arms
whose first-2700 prefix reads under 55.0**, while their registered `BARS.tsv`
bars all read `51.33 ge`. **The band 52.0–55.0 — which is where a real,
shippable solo eco plank is expected to land, and which the trend floor
deliberately preserves — is a dead zone: the arm survives the 52.0 trend floor
and is then cancelled by a bar built for combinations.**
**THE THREE RESOLUTIONS, and the choice is the builder's because
`auto_gate.py:303-313` requires the token to be typed by a human at
registration:**
* **(a)** append `COMBO-BAR-EXEMPT` **plus a citation to this file** to the
  `OPENFAST` row's source column in `docs/prereg/BARS.tsv`. `auto_gate.py:919-937`
  honours it only when the cited `.md` resolves on disk — a token citing nothing
  is *louder* than no token (`COMBO-BAR-BROKEN-EXEMPT`). This is the intended
  mechanism and the one I recommend.
* **(b)** register the bar AT 55.0 and accept that OPENFAST is a prospecting
  screen with a ~1-in-2 false-drop rate at a true 55 (`auto_gate.py:271-277`).
  This is honest but it is **not** the bar its six same-day siblings carry, so
  the arm stops being numerically comparable to them.
* **(c)** strip the inherited marker from the arm's `doctrine.py`. **⛔ I do not
  recommend this and it is named so it is refused deliberately rather than
  chosen quietly:** the marker is a true statement about the tree's provenance,
  removing it makes the arm's ancestry unauditable, and the control's own
  comment says a hand-merge reading as a SOLO would be "scored against the wrong
  bar".
**Whichever is chosen, `GATE RESOLUTION` below is written for (a) and must be
amended (ADD-only) if the lane picks (b) or (c).**

**2. THE CONTROL IS THE LIVE INCUMBENT, SO 50.0 MEANS "ADDS NOTHING".**
`bots/_v468kladturbo` is Sleipnir v1 (`PROGRAMME.md:8` `INCUMBENT`), pinned as
the corefill control at `scratchpad/CONTROL_PIN`
(`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). A reader importing a
61-shaped intuition from any KLADTURBO-vs-v140 read has misread the fixture:
**the same bot measured against itself reads 50.**

**3. ⛔ THE PRIMARY IS POOLED GAME SHARE. NO OPENING-TEMPO NUMBER MAY BE QUOTED
AS THIS ARM'S RESULT.** `c1`, `h1`, `conv@8`, `bld@8` and the spawn-excess are
**MECHANISM** metrics. `PROGRAMME.md` `R1000_IS_DEFEAT: yes` and the
`titanium_collected`-is-off-currency ruling make the belt **instrumental** — it
buys the kill, it never scores. A sentence of the form *"OPENFAST moves the first
conveyor 1.6 rounds earlier"* is a dose statement and is true; a sentence of the
form *"OPENFAST is worth 1.6 rounds"* is a verdict in the wrong currency and is
inadmissible.

**4. ⛔⛔ THE ECO CLOCK *IS* THE KILL CLOCK IN THIS TREE — AND I MEASURED THE
DIRECTION, WHICH IS THE WRONG ONE. THIS IS THE SECOND LOCK-BLOCKING ITEM ON THE
PAGE AND IT WAS NOT IN THE BUILDER'S SUMMARY.**

**THE MECHANISM, read off the control at `bots/_v468kladturbo/raid.py:673-678`
(verified at these exact lines, and byte-identical in the arm since `raid.py` is
byte-identical):**
```
rush = LOKI2_RUSH_ON and ct.get_current_round() < LOKI2_RUSH_RND
min_harv = LOKI2_RUSH_MIN_HARV if rush else LOKI_FWD_MIN_HARV
ti_floor = LOKI2_RUSH_TI_FLOOR if rush else LOKI_FWD_TI_FLOOR
if ct.read_store(SLOT_HARVESTERS) < min_harv:      return False
cost = ct.get_sentinel_cost()
if ct.get_global_resources() < cost + ti_floor:    return False
```
`LOKI2_RUSH_ON = False` (`doctrine.py:1409`) ⇒ the live values are
**`LOKI_FWD_MIN_HARV = 2`** (`doctrine.py:1265`) and **`LOKI_FWD_TI_FLOOR = 40`**
(`doctrine.py:1264`), and `SLOT_HARVESTERS` is a **monotone high-water mark of
harvesters BUILT** (`doctrine.py:381`). ⇒ **no forward sentinel can be sited until
two harvesters exist AND the bank holds `sentinel_cost + 40`.** The economy gate
IS the raid gate.

**⇒ THE GATE HAS TWO HALVES AND OPENFAST MOVES THEM IN OPPOSITE DIRECTIONS.**
* **The HARVESTER half opens EARLIER** — `h1` −1.63 rounds paired on pool,
  `harv@8` +0.35. Safe direction.
* **The BANK half opens LATER** — the arm spends earlier and more on belt
  (`conv@8` **+0.85** at +1% scale each) and can field the sixth builder sooner
  (`main.py:460`, `harv >= 1 and ti >= LOKI_SURPLUS_TI` = 260, satisfied sooner;
  `bld@8` +0.08 at **+20% scale each**). Both raise `get_sentinel_cost()` AND
  lower the bank at any given round. **Adverse direction.**

**⇒ WHICH HALF DOMINATES IS AN EMPIRICAL QUESTION, SO I MEASURED IT RATHER THAN
ARGUING IT. THE ANSWER IS THE BANK HALF.** Paired battery run by this drafting
agent at draft time (`2026-08-17T08:00:12Z`): **15 pool maps × both seats = 30
paired cells**, one deterministic game per cell, `--seed 11`, `--tle 0`,
`NOISE_ON=False`, opponent `opp_v63`, decoded with **`tools/replay_census.py`**
(whose documented headline number is first-sentinel timing) and classified
FORWARD/HOME against both core positions read out of `scratchpad/s48_open_table.py`:

| first-sentinel round, treatment − control | value |
|---|---|
| paired MEAN | **+5.60 rounds LATER** |
| paired MEDIAN | **+0.0** |
| earlier / tied / later | **9 / 8 / 13** |
| sign test, two-sided, over the 22 non-ties | **p = 0.523 — NOT significant** |
| cells delayed **≥20 rounds** | **9** |
| cells advanced **≥20 rounds** | **4** |
| subset where the first sentinel is FORWARD in BOTH arms (n=25), paired mean | **+8.76 rounds LATER** |
| first-sentinel siting class | base **25 FWD / 5 HOME** → arm **29 FWD / 1 HOME** |

**HOW THIS MUST BE READ, and the reading is deliberately conservative:** the
**MEDIAN delta is EXACTLY ZERO and the SIGN TEST IS A COIN FLIP.** This is **NOT**
a central-tendency finding and it must never be quoted as "OpenFast delays the
first turret by 5.6 rounds". **It is a TAIL finding**: the mean is carried by nine
cells delayed twenty rounds or more, against four advanced by as much — worst
cells `glacierkeep/A 18 → 111 (+93)`, `auroraveil/B 19 → 63 (+44)`,
`glacierkeep/B 20 → 59 (+39)`, `nordkap/B 10 → 48 (+38)`, `yulerune/A 21 → 54
(+33)`; best cells `drumlin/B 79 → 25 (−54)`, `drakkarfjord/A 66 → 38 (−28)`,
`icefloe/B 52 → 27 (−25)`, `antler/B 31 → 7 (−24)`.
**AND A TAIL IS EXACTLY WHAT THE TW HAZARD KEYS ON.** x3r0's turret-window weapon
gates on *never having seen one of our turrets*; it is triggered per-game, not by
our average. **A +93-round delay on `glacierkeep` re-enables that weapon on that
map even though the pooled median is 0.** ⇒ this is a **DISQUALIFYING-CLASS
hazard by the standard the lane set, held at n = 30, and it is the reason K1 below
is a REGISTERED PRIMARY-ADJACENT METRIC rather than a paragraph.**

**⚠ THE ONE GENUINELY GOOD HALF OF THIS RESULT, stated so the item is not read as
purely adverse:** the arm's first sentinel is **FORWARD in 29 of 30 cells against
the control's 25 of 30**. The arm converts home sentinels into forward ones — the
on-programme direction (`PLAY_DEFENCE: not_at_the_kill_s_expense`). **It plants
the siege more often and later.** Whether that trade is worth taking is what the
shard decides; it is not decided here.

**CAVEATS ON MY OWN NUMBER, and they are not small:** 30 one-game deterministic
cells; **one seed** (inert by construction, so no replication is available);
**one opponent, `opp_v63`, which is a probe bot WE WROTE** while the screen's
opponent is Sleipnir v1; **`--tle 0`, not the shard's `--tle 10`**. This is a
MECHANISM PROBE that establishes a direction worth registering. It is **not** an
effect size and it forecasts nothing about share.

**5. ⚠ THE SECOND NAMED ADVERSE MECHANISM: THE ORE SORT CLUSTERS THE ECO SEATS
WHILE `_pick`'s STRIPE PARTITION IS UNTOUCHED.** Ordinals 1, 2 and 3 all sort by
distance to the **nearest** ore-adjacent tile, so all three are born on the same
side of the core; but `_pick` and its stripe are byte-identical to the control, so
seats 2 and 3 may still be assigned ore on the **opposite** side. Observed in the
sanity cell I ran at draft (icefloe/A, seed 11, `--tle 0`, `NOISE_ON=False`):
ordinal distances `base 7,8,9,4,9 → arm 7,3,4,3,9`, i.e. the three eco seats
collapse from {8,9,4} onto {3,4,3}. **This is the mechanism by which an r8 gain
becomes an r100 loss, it is not measured anywhere in the demo (the demo's window
closes at r25), and it is a live route to a share BELOW 50.**

**6. THE SHARD TAPE CANNOT SEE THE MECHANISM, SO A FIRINGS READ IS MANDATORY
BEFORE THE PRIMARY.** `tools/overnight.sh:138-139` runs every game with
`--replay /dev/null` and the tape's columns are
`ts shard game map seed seat winner cond turns` — **no entity, build, position or
belt information exists on it, in either arm.** The plank's mechanism is
CONDITIONAL (it latches OFF when no ore is known; §7) so `docs/prereg/BARS.tsv`'s
FIRINGS-BEFORE-PRIMARY rule (adopted 2026-08-16T13:27:33Z) binds: **F1/F2/F3
below run on a SEPARATE replay-keeping battery and must be read BEFORE the
primary sentence is typed.** What the tape CAN answer is the kill-clock question
(`cond`, `turns`, `winner`), which is why D1–D3 are shard-native and F1–F3 are not.

**7. ⚠ THE MECHANISM IS CONDITIONAL ON A HARDCODED MAP FINGERPRINT DATABASE, AND
IT LATCHES.** `main.py:255` reads `self.map_grid`, filled by
`eco.py:121 known_map_for()`, which matches `(w, h, core_pos)` against
`MAP_CODES`/`EXTRA_MAP_CODES` and **returns `None` on an unrecognised map**. On
`None` the BFS falls back to the Core's own vision (r²=36) for both walls and
ore; if no ore is inside r²=36 the flood returns `{}` and
`main.py:250,309` **LATCH it permanently** (`self._of_dist` is set once). The
latch is CORRECT — the Core never moves, so `known_map_for` can never learn more
later, and re-flooding every spawn is the hot-path cost this tree removed
elsewhere — and I verified the reasoning against the code rather than accepting
the docstring. **But it means the plank can be silently INERT on an unknown map,
and the fallback flood also routes through walls it cannot see.** On the 15-map
corefill pool the dose is measured non-zero on 14 of 15 maps (§DOSE), so it is
not inert HERE; on the ladder it may be. Registered, not glossed.

---

## RATIFY: Hypothesis

**Sorting the Core's spawn-tile candidates by BFS distance to the nearest
ore-adjacent tile for the ECO spawn ordinals (1, 2, 3) only — hash retained as
tie-break, ordinals 0 and 4 untouched — raises our LOCAL pooled game share
against `bots/_v468kladturbo` itself to 51.33% or higher at n = 5,400 games
across all 15 corefill maps and both seats.**

**The mechanism claim, stated so it can be wrong** — four effects, and the
hypothesis is that the first outweighs the other three:
* **IT MOVES THE WHOLE OPENING EARLIER.** `_wire_on_build` is the only producer
  of `link_queue` and is called from exactly one place (immediately after a
  harvester is built), so **the first conveyor cannot precede the first harvester
  by construction** — measured `c1 − h1 == 1` in 90 of 97 base demo cells, `< 1`
  in **zero**. Under "do not break harvester parity" the only admissible way to
  move the belt earlier is to move the whole opening earlier, and the spawn tile
  is what was measured to cost the rounds (+10.5 median tiles of extra walking
  across the opening five, 32 local cells).
* **⛔ IT DELAYS THE FIRST FORWARD SENTINEL IN THE TAIL — MEASURED, NOT FEARED**
  (§4). The forward-sentinel gate is `SLOT_HARVESTERS >= 2` AND
  `bank >= sentinel_cost + 40` (`raid.py:673-678`); the arm opens the harvester
  half earlier and the bank half later, and over 30 pool cells the bank half won:
  paired mean **+5.60 rounds later**, median delta 0.0, **9 cells delayed ≥20
  rounds**. **In this tree the eco clock IS the kill clock, so this is the channel
  by which an economy plank goes off-programme** — registered as K1/K3 and as the
  second lock blocker.
* **⚠ IT CLUSTERS THE ECO SEATS AGAINST AN UNCHANGED STRIPE PARTITION** (§5
  above) — a real route to a longer *second* and *third* walk.
* **⚠ IT PARTIALLY REVERSES A SHIPPED PLANK ON THREE OF FIVE OPENING SEATS.** The
  base's key is `(hash(x,y,n,salt) % 97, y, x)` and its own comment says the salt
  exists so "identical-key ladder games diverge from the first spawn" — the
  `NOISE_ON` anti-repeat insurance (`doctrine.py:460-474`, priced there at
  ~0.06 Elo/game). On ordinals 1–3 the arm demotes that salt to a **tie-break
  among equal-distance tiles only**, so those three seats become far less
  divergent game-to-game. Small, measured, and named because it is a shipped
  mechanism being partly undone.

**⇒ A flat result is INFORMATIVE and is not a null about "the spawn tile is the
binding constraint".** The diagnosis is confirmed engine-side independently of
any share (§DOSE). A flat share would say that **~1.6 rounds of opening belt
tempo, at this dose, does not convert to games against Sleipnir** — which is a
statement about the CONVERSION, not about the constraint.

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068 bots/_v468kladturbo`). There is no opponent churn to pin against and no calibration relevance to protect — CLAUDE.md's rule is PIN TREATMENT LEGS / NEVER PIN CALIBRATION PANELS, and a self-play screen is neither: it is pinned by having no opponent.**
**SURFACE: local**
**PLANK CLASS: ECONOMIC (opening tempo), instrumental — a local self-play screen. It is NOT a defensive plank: no turret, barrier, seal or survival behaviour is touched. The r300 admission bar is nevertheless registered and read on this arm, because the risk in §4 (earlier +20%-per-builder cost scale inflating the first turret) is a genuine economic-to-defensive channel and I will not rely on the class declaration to excuse me from measuring it.**
**KILL-ROUND NON-REGRESSION: read in the ITT form over ALL 5,400 rows of each arm, and registered as an EXCLUSION. (i) ITT TIMELY-KILL RATE — share of ALL of the arm's games with `cond == core_destroyed` AND won by us AND `turns <= 300`; denominator is EVERY GAME THE ARM PLAYED, never the kill-conditioned subset; the 95% CI LOWER BOUND on (treatment − control) must EXCLUDE a fall of 2.0pp. (ii) ITT RMST300 — `tools/fieldcal_read.py:239 rmst_score`, `min(turns, 300)` with every game not ending in OUR core-kill scoring the full 300 horizon; the 95% CI UPPER BOUND on (treatment − control) must EXCLUDE a rise of 8.0 rounds. Intervals from `tools/cluster_ci.py` with the local DEFF. (iii) The kill-win-CONDITIONED share is reported beside both as a DIAGNOSTIC ONLY — it carries a collider (`PROGRAMME.md`, corrected 2026-08-16T05:19:38Z: kill-win-conditioned 15.1% vs ITT 7.8% on the rated tape) and may not be the bar. (iv) Median kill round crossing 300 is the gross backstop. ⛔ REGISTERED PREDICTION — REVISED BEFORE LOCK AND BEFORE ANY SHARD ROW EXISTS, because my own draft-time measurement contradicted the direction the builder's summary implied: the arm's ONLY channel to the kill clock is the shared harvester+bank gate at `raid.py:673-678` (the raider's own spawn tile, ordinal 0, is untouched), that gate's two halves move in OPPOSITE directions, and the bank half was measured to dominate — first sentinel paired mean +5.60 rounds LATER over 30 pool cells (median delta 0.0, sign p=0.523, heavy right tail; §4). ⇒ THE REGISTERED PREDICTION IS: timely-kill rate FLAT-OR-DOWN, with a fall of up to 2.0pp inside the registered exclusion and anything worse a REGRESSION. A prediction of FLAT-OR-UP would have been the comfortable one and it is not what the evidence says.**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe. Both clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit). **The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and applying them would widen every interval here 24–35% for correlation that has been measured absent.** ⚠ The s42 cross-host rider is registered and does not bind: this is a WITHIN-HOST local cell and nothing on this page pools across hosts. If a remote replication is later stocked it is REPORTED SEPARATELY and NEVER POOLED, per the GUNAXABL/SENTTHR precedent.
**ESTIMATOR: unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Interval by `tools/cluster_ci.py` (v4, at HEAD) with the local constant. Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never the bar — seat is worth ~6.8pp on byte-identical arms, which is why the n is a multiple of 30.
**SAME-HOST: N/A by shape for the PRIMARY — OPENFAST is a SOLO single-shard screen and its treatment and control games are generated inside the same `tools/overnight.sh` invocation on one host, so there is no cross-shard contrast to protect. The constraint DOES bind on the F-battery, which is a two-arm contrast: F1–F3 must run base and arm on the SAME HOST, in the SAME invocation, at the SAME `--tle`, or they are not comparable. `scratchpad/s48_demo.sh` satisfies this by construction (it builds both trees and runs both arms in one loop).**
**DOSE: spawn-tile excess walk in tiles (engine-side, decoded from builder-spawn POSITIONS in the replay; LOWER IS BETTER) — treatment 10 vs base control 21 (n=1 verified cell at draft: icefloe seat A, `--seed 11`, `--tle 0`, `NOISE_ON=False`, opponent `opp_v63`).** Instrument `scratchpad/s48_spawnring.py <replay> --team {0,1}`, column 5 = `sum(distance-to-ore-adjacent over the first 5 spawn tiles) − sum(the 5 best legal ring(core,2) tiles)`. On that cell the per-ordinal distances were `base [7,8,9,4,9] → arm [7,3,4,3,9]` — **ordinals 0 and 4 IDENTICAL, ordinals 1–3 all improved**, which is the plank's exact signature and is what makes this a targeted dose read rather than a summary. **BOTH VERDICTS ARE AVAILABLE ON THIS INSTRUMENT** and the flag-off harness is the driver: `zsh scratchpad/s48_flagoff.sh _v486openfast LOKI_OPENFAST_ON` compares replay SHA-256 for base / flag-off / flag-on and must print flag-off == base and flag-on != base. ⛔ **SEE `KNOWN OPEN ITEM 1` — the builder's claimed 16/16 + 16/16 has NO COMMITTED ARTIFACT and this is a lock blocker.** **SECONDARY DOSE (opening tempo, also engine-side), recomputed BY THIS DRAFTING AGENT from the committed `scratchpad/s48_demo_rows.tsv` and RESTRICTED TO THE 15 MAPS THE SCREEN ACTUALLY PLAYS — 60 paired cells of the 100 in the commit:** first conveyor `c1` mean paired delta **−1.62 rounds** (arm earlier 38 / same 18 / later 4), first harvester `h1` **−1.63** (38/18/4), conveyors@r8 **+0.85** (better 32 / same 24 / worse 4), harvesters@r8 **+0.35**, builders@r8 **+0.08**, conveyors@r25 **+1.22**. Per-pool-map mean `c1` delta moves in the intended direction on **14 of 15** maps (antler −4.0, fjordgate −3.25, icefloe −3.0, drakkarfjord −2.5, archipelago/frostgate/royale −2.0, valkyrie −1.5, auroraveil/drumlin/glacierkeep −1.0, nordkap/ragnarok/yulerune −0.5; **midgard +0.5 is the sole exception**). ⚠ **THIS IS A FIRING DEMONSTRATION AND NOT AN EFFECT SIZE.** One deterministic game per cell, `NOISE_ON=False --tle 0`, opponents `opp_v63`/`opp_v78` — **which are OUR OWN PROBE BOTS** (CLAUDE.md: a fixture we wrote, which lies in a known direction), and the observation window closes at **r25**. Nothing here forecasts a share.
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:66` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture.
**CUT-SHORT: floor 2700 games.** Below 2,700 completed tape rows this leg publishes descriptive tallies (share, per-seat, per-map, kill-clock) and takes **NO comparative look and no bar verdict**; the half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` cancellation at CATASTROPHE@400, TREND-FLOOR@1000, TREND-FLOOR@2700 or COMBO-BAR@2700 is an **OPERATIONAL STOP**, not a verdict, and is typed `cancellation`.
**BAR: 51.33**
**BASE RATE: 50.00**
**BAR SOURCE:** house-standard corefill futility band, `50 + 1.96*sqrt(.25/5400) = 51.33pp`, local DEFF 0.98 so naive — the identical bar carried by `docs/prereg/BARS.tsv` rows `KLADLADDER`, `ECOMMIT`, `FREEROUND`, `ROUTESCORE`, `BELTBREAK-EARLY` and `BELTBREAK-LATE`, which is what keeps this arm numerically comparable to its same-day siblings. **Constructed, not observed.** ⛔ **KIND OF BAR, per the OB16 corollary (2026-08-15T03:52:45Z): this is a POINT RULE. The standard band is `50 ± half_width`, so its implied MDE is 0.000pp and clearing it excludes 50.0 and NO positive effect size.** It may not be quoted as having excluded an effect. That is deliberate: the question this leg asks is *does earlier opening belt tempo move anything at all against the incumbent*, which is what a point rule is the right instrument for. ⛔ **AND IT IS NOT THE BAR THE CANCELLER WILL APPLY UNLESS RESOLUTION (a) OF ITEM 1 IS TAKEN — see `GATE RESOLUTION`.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own base. Empirically calibrated on the same host and fixture by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z (`results.tsv:454`, `idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:346`, `null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it.
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:66`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.) ⚠ **AND IT IS NOT COSMETIC: the committed demo ran ALL 25 maps in `maps/`, so 10 of its 25 maps and 40 of its 100 cells are OFF-POOL.** That is why the `DOSE` figures above are the **pool-restricted 60-cell recomputation** rather than the commit's 100-cell table, and why F1–F3 are re-run on the full 15-map pool before the primary.
**REFERENCE n: none** — the comparator is generated inside this same shard from the same 5,400 seeds; there is no fixed external reference sample, so no resolution floor at n→∞.
**TREATMENT TREE: bots/_v486openfast**
**TREATMENT DIFF REFS: 78965d91^ 78965d91**
**MECHANISM METRIC READS: bots/_v486openfast/main.py:502 — `cands.sort(key=lambda sp: (of.get((sp.x, sp.y), LOKI_OPENFAST_FAR), …))`, the ore-distance-led spawn sort, reached only through the guard at main.py:496-497 (`LOKI_OPENFAST_ON and self.n in LOKI_OPENFAST_SEATS`, then `self._openfast_dist(ct) or None`). Observed as F1 via the builder-SPAWN POSITIONS the engine writes into the replay entity stream, decoded by `scratchpad/s48_spawnring.py` (`tools/replay_census.parse_entity`) — an ENGINE-SIDE fact, never our own `print()`, which is stripped from platform replays. TREATMENT DIFF TOUCHES: bots/_v486openfast/main.py bots/_v486openfast/doctrine.py. INTERSECTION: yes — `main.py:502` is one of exactly four hunks the arm adds to `main.py`, and a `grep -c` for `LOKI_OPENFAST` over every source file of the control tree returns 0 in every one of them, so the metric CANNOT read identically in both arms: the control has no geometry term in its spawn key at all.**
⚠ **DIFF-REFS DISCLOSURE:** `78965d91` ADDS the whole tree plus six `scratchpad/` files, so `git diff --name-only 78965d91^ 78965d91` returns TEN paths including `eco.py` and `raid.py`. The SEMANTIC diff against the control is TWO files: `diff -rq bots/_v468kladturbo bots/_v486openfast` names `doctrine.py` and `main.py` ONLY, and **`eco.py` and `raid.py` are byte-identical (md5 verified both ways)**. `TREATMENT DIFF TOUCHES` declares the semantic two; the extra paths in the git diff are an artefact of adding a tree, not undeclared changes.
**METRIC WINDOW: r0-r8. GATING CONSTANTS: LOKI_OPENFAST_ON=1, LOKI_OPENFAST_NODES=1200, LOKI_OPENFAST_FAR=99. MECHANISM CAN OCCUR IN WINDOW: yes** — **there is NO round gate anywhere in this plank.** The mechanism fires at the moment the Core spawns ordinals 1, 2 and 3, which the demo measures at rounds 1–4 in every cell (builders-by-r8 = 5.38 base / 5.46 arm, i.e. the opening five are all placed by r8 in both arms). `LOKI_OPENFAST_NODES` is a BFS **node budget** and `LOKI_OPENFAST_FAR` is a **sentinel distance** for a ring tile the flood never reached — neither is a round threshold; they are declared because they are the constants that actually gate the plank, and an undeclared gate is the failure Obligation 17 exists for. `LOKI_OPENFAST_SEATS = (1, 2, 3)` is a **spawn-ordinal tuple**, not an integer, and is declared in prose here for the same reason: it is the real gate, and it is the one that couples to item ⑧ below.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `prereg_check.py` returns `PREREG_CHECK: OK` on this document with TWO `OBLIGATION 17` warns, and BOTH WERE CHECKED BY HAND rather than waved through.** (i) **`LAUNCHER_MIN_RND = 160`, WIDER SCOPE** — the tool flags it because it is referenced in the metric's FILE and the window `r0-r8` is entirely on its closed side, and it instructs the author to confirm the metric's read path is not downstream of it. **Checked: `main.py:836` is `if ct.get_current_round() < LAUNCHER_MIN_RND: return` inside the LAUNCHER siting path, 326 lines BELOW the spawn sort at `:502` and in a different method reached only from the builder branch. The Core's spawn-candidate sort is not downstream of it in any control flow.** The warn is correct to fire and is resolved. (ii) **`LOKI_OPENFAST_ON=1`, PARTIAL WINDOW** — an artefact of `check_metric_window` reading every declared integer as a ROUND: `LOKI_OPENFAST_ON` is a BOOLEAN whose `True` renders as `1`, not a round floor of 1. It is declared anyway because it is the flag that gates the plank, and an undeclared gate is the failure the obligation exists for.
**PRE-STATE: the predicted-change set is NOT already in the target state at lock.** Verified at draft against the control tree: `grep -c LOKI_OPENFAST bots/_v468kladturbo/*.py` → **0 in every file**; `grep -c _openfast_dist` and `_of_dist` → **0 in every file**. The control's spawn-candidate sort at `bots/_v468kladturbo/main.py` is `(hash(x,y,n,salt) % 97, y, x)` with **no geometry term of any kind**, so "spawn candidates ordered by distance to ore" cannot already be in the target state. The measured consequence is likewise not in the target state: base spawn-excess 21 on the draft sanity cell, against a best-ring floor of 0.
**MAP SEGMENT: none expected — and the reason is that I cannot SIGN one at a defensible n, which under Obligation 15a is a reason to declare none rather than to declare an unfalsifiable segment.** The mechanism's dose is a property of map geometry (how much better the best ring tile is than the hash-chosen one), and I *can* write a predicate that is computable before any game — `best ring ore-distance` vs `mean hash-chosen ore-distance` at the core. **But the per-map evidence I have is FOUR deterministic cells per map, and the per-map spread I measured (antler −4.0 to midgard +0.5) is not distinguishable from cell noise at n=4.** A segment declared off four cells is subgroup fishing with extra steps. Per-map shares WILL be printed at readout as **DESCRIPTIVE** material whose declared purpose is to size a SUCCESSOR (a segment-scoped arm with its own prereg and its own `SEGMENT VALUE CEILING`), **not to rescue a failed pooled primary. No map cut may rescue this arm**, and nothing may be banked off those shares without a fresh prereg.
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: written for resolution (a) of ITEM 1 and it must be amended if the lane picks (b) or (c).** The shard is governed by the pinned `tools/auto_gate.py` marks: **CATASTROPHE** at n≥400 if the 95% CI upper < 45.0 (`:244,247`); **TREND-FLOOR** at n≥1000 and again at n≥2700 if the corresponding PREFIX share < 52.0 (`:261`, `:888-899`); **COMBO-BAR@2700** if the prefix < 55.0 (`:278`, `:952-958`) **which fires on this arm because `combo_of` reads the control's inherited stack.py marker out of the arm's own `doctrine.py:1878`**, and which resolution (a) suspends by registering `COMBO-BAR-EXEMPT` + a citation to this file in the `BARS.tsv` source column. ⛔ **THE ARITHMETIC THE LANE MUST ACCEPT BEFORE LOCKING: the registered bar is 51.33 at n=5,400 but the OPERATIONAL floor is 52.0 on the first-1000 prefix. An arm whose true effect is +1.4pp clears its bar and is killed by the floor with probability ~83% (`auto_gate.py:869-873`, 60k-draw pricing). That is the house regime and it is not this document's to change — it is stated so the null is read correctly: a TREND-FLOOR stop is a CANCELLATION that says "not worth further compute alone", it is typed `cancellation`, rows are KEPT, and it licenses NO exclusion claim about the plank, because the registered target is 5,400.** The RESOLVABLE gate this document owns is the primary at full n, whose margin (1.33pp) exceeds its own half-width (±1.32pp) by 0.01pp — resolvable, and only just. Everything else on this page (F1–F3, D1–D3, the seat and map splits) is DIAGNOSTIC and cannot rescue a failed primary. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.
**SOLO-OR-COMBO: SOLO by construction and by diff.** The arm adds ONE flag family (`LOKI_OPENFAST_*`) in ONE append-only `doctrine.py` hunk and FOUR hunks in `main.py`; it composes no prior plank, and `tools/stack.py` was not run. **The 52.0 trend floor is the operational rule that binds it and 51.33 is its registered bar; the 55.0 COMBO bar binds it only because of the inherited-marker defect in ITEM 1, which is a registry bug and not a statement about the arm's shape.**

---

## SEEDS

**SEED BASE: 836000.** Registered worklist row (**to be appended by the builder, not by this agent**):
```
OPENFAST bots/_v486openfast bots/_v468kladturbo 5400 836000
```
**COLLISION AUDIT, run at draft (`2026-08-17T07:49:55Z`), and it names what it checked:**
* `grep -n '836000\|838000\|840000' scratchpad/corefill_work.txt scratchpad/fleet_queue.tsv docs/prereg/*.md scratchpad/overnight/*.tsv` → **no match on any of the four surfaces.**
* The live worklist's highest seed base is **826000** (`ODINVSSLEIP`, n=2700).
* The four UNLOCKED same-day drafts claim **828000** (`KLADLADDER2`), **830000** (`KLADLADDER3`), **832000** (`SEALPIERCE`) and **834000** (`ECOMMIT2`) — enumerated per file, not assumed.
* ⇒ **836000 is the next free base at the 2000-wide stride this family uses**, and a 5,400-game shard consumes 5,400 of the 2,000-seed stride… **⚠ WHICH IS THE ONE THING THIS AUDIT CANNOT BLESS: at n = 5,400 a 2,000-wide stride OVERLAPS the next row's base.** Every locked sibling in this family carries the same 2,000 stride at n = 5,400, so this is a family-wide property of `tools/overnight.sh`'s seed walk and not an OPENFAST defect — **but the builder must confirm how `overnight.sh` consumes `SEEDBASE` before treating 836000 as exclusive, because if it walks `SEEDBASE + game_index` then OPENFAST at 836000 and a future row at 838000 share 3,400 seeds.** I did not resolve this and I am not going to assert it clean. Reported, per the standing rule that a check which cannot compute must say so rather than render as clean.

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on the treatment's
pooled game share falls BELOW 51.33.** That excludes the bar and says ore-biased
eco spawn placement does NOT add measurably to Sleipnir on this fixture.
**Consequence, registered in advance and BRANCHED, because the branches license
different next moves:**
* **If F1 shows the spawn excess FELL as designed and F2 shows `c1`/`h1` moved
  earlier** — i.e. the dose was delivered on the pool — then **the CONVERSION is
  what failed, not the mechanism**, and the successor is a DOSE increase with its
  own prereg: extend the sort to ordinals 0 and 4, or re-point `_pick`'s stripe
  so the clustered births are assigned the ore they were born next to (§5). **Not
  a re-run of this arm.**
* **If F1 shows the excess did NOT fall on the pool** (the latch, §7, or a
  `known_map_for` miss), the plank did not deliver its dose in the screen fixture
  and **the primary is uninterpretable in either direction** — see the mechanism
  falsifier.

**MECHANISM FALSIFIER (independent of the primary, and it can fire first):** if
F1's treatment spawn-excess is within noise of the control's on the 15-map pool
— i.e. the 21→10 signature does not reproduce on the maps the screen actually
plays — then **the primary is reported as NOT MEASURED, not as a null.** Per the
FIRINGS-BEFORE-PRIMARY rule this is read BEFORE the primary is typed.

**KILL-CHANNEL FALSIFIER (registered separately from the share, because an arm can
clear its bar and still be off-programme):** if **K1** shows the first forward
sentinel later AND **D1/K2**'s 95% CI lower bound fails to EXCLUDE a 2.0pp fall in
the ITT timely-kill rate, **the arm is off-programme under
`PLAY_DEFENCE: not_at_the_kill_s_expense` whatever its share reads**, and no
promotion, combination claim or head-to-head follows. **This falsifier can fire on
an arm whose primary CLEARS**, which is the whole reason it is registered
separately.

**INSTRUMENT-ALARM FALSIFIER:** if F3 finds that the arm's ordinal-0 and
ordinal-4 spawn tiles differ from the control's on any `NOISE_ON=False` cell, the
"ordinals 0 and 4 placed exactly as base" claim is FALSE, the arm is not the arm
this document registers, and **nothing on this page may be read.** This is a
checkable prediction, not a courtesy — the guard is `self.n in
LOKI_OPENFAST_SEATS` at `main.py:496` and it is the only thing standing between a
one-plank arm and a five-seat rewrite.

---

## HONEST-NULL CLAUSE — what a share null does and does not kill

**Registered before the data, because this plank's honest ceiling is small and
saying so afterwards is worthless.**

**THE ARITHMETIC OF THE CEILING.** Against the field we are measured **4.42
rounds later** on the first conveyor and **3.57 conveyors short** by r8. OPENFAST
recovers **~1.6 rounds paired on the pool (~32-37% of the conveyor deficit)** and
**~0.85 conveyors@r8 (~24%)**. **The other ~65% is a DIFFERENT PLANK** — the
harvester→conveyor coupling (`_wire_on_build` being the sole `link_queue`
producer), which this arm deliberately does not touch and which
`ECOMMIT`/`ROUTESCORE`/`FREEROUND` are aimed at.

**⇒ A SHARE NULL DOES NOT REFUTE THE MECHANISM.**
* **WHAT DIES on a share null:** the claim that **opening belt tempo of this
  magnitude converts to game share against Sleipnir**. That is the claim the
  primary tests and it is the only one a share can kill.
* **WHAT SURVIVES a share null:** (i) the DIAGNOSIS — that the spawn tile, not
  ore-choice or tasking order, is the binding constraint on our opening (measured
  independently: `h1 − OPT_noS0` is 0 in 18 of 32 cells, median 0, so the walk is
  already tight from wherever the body lands); (ii) the DOSE — 21→10 excess walk
  and −1.62 rounds `c1` on-pool, which are engine-side facts about positions and
  build rounds and do not become false because a share reads 50; (iii) the arm's
  availability as a **COMBINATION input** with any plank that removes the
  harvester→conveyor coupling, where the two effects are plausibly
  super-additive (this arm moves the opening earlier; those arms shorten the
  chain from harvester to first delivered stack).
* **WHAT A NULL WOULD MEAN IN ONE SENTENCE:** *we bought a third of the opening
  tempo deficit and a third of it is not enough to move a game against a bot
  this strong* — a statement about the dose, not the direction.
* ⛔ **AND THE ANTI-RESCUE CLAUSE: a null on share is NOT a licence to re-run
  this arm at a higher n.** The bar is registered at 5,400 and the half-width
  there is ±1.32pp; a bigger n buys precision on an effect the ceiling above says
  is small, which is exactly the "paying full price for the at-the-bar class" the
  trend floor exists to stop. The successor is a bigger DOSE or a COMBINATION,
  never more games on this dose.

---

## READING, PRE-COMMITTED — four bands, written before the data

| band at n = 5,400 | pre-committed reading |
|---|---|
| **CI lower ≥ 51.33** | **ORE-BIASED ECO SPAWN PLACEMENT ADDS.** Real and resolved on this fixture. Promotes to a combination input and to a separately-registered head-to-head against the live holder. Report the size honestly and report the D-battery alongside it — a win bought while the kill clock slipped is a different plank from a win bought while it did not, and D1–D3 are what say which. |
| **point ≥ 51.33 but CI lower < 51.33** | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Registered in advance as WEAK: `NULL125`'s byte-identical A/A read 51.04, so a bare clearance in [51.33, 52.4] is not distinguishable from fixture noise by this leg alone. Rows are KEPT and the arm is available for combination; it does NOT license a ship conversation, and a replication on fresh seeds is the price of promoting it. |
| **CI includes 50.0** | **ADDS NOTHING MEASURABLE.** Read F1/F2 to say which branch of the primary falsifier applies, then apply the HONEST-NULL clause verbatim. Combination input only. |
| **CI upper < 51.33** | Primary falsifier fires — see the two branches above. **A share materially BELOW 50 is a LIVE, PRE-NAMED outcome**, and the two named routes to it are §4 (the measured first-forward-sentinel delay via the bank half of `raid.py:673-678`) and §5 (clustered eco births against an unchanged stripe partition). **§4's route is now the FIRST SUSPECT rather than one of two, because it is the only one with a draft-time measurement behind it; read K1 before writing the sentence.** It is named here so a negative is not explained away as noise. `KLADLADDER`, demo-clean on this same base with this same flag-off SHA method, finished **41.86% [40.20, 43.52] at n = 3,404** — **8 points below the null, with its dose confirmed delivered.** A clean demo predicts FIRING and predicts nothing about SHARE. |

---

## MECHANISM DIAGNOSTICS TO READ AT READOUT

Measurability is declared per metric. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape carries.

### F1–F3 — the FIRINGS read. MEASURABLE, but NOT off the shard tape. READ BEFORE THE PRIMARY.

**EXECUTING TOOL, named per Obligation 17 and VERIFIED EXECUTABLE AT DRAFT (I ran
both decoders on fresh replays before naming them):**
```
zsh scratchpad/s48_demo.sh scratchpad/s48_openfast_pool_rows.tsv
```
with the map loop restricted to the 15 pool maps, then per replay
```
.venv/bin/python scratchpad/s48_spawnring.py <replay> --team {0|1} --label <map>/<seat>
.venv/bin/python scratchpad/s48_open_table.py <replay> --team {0|1} --rounds 25 --label <map>/<seat>
```
**OB17 checks, run, and the two that could have surprised are named:**
1. *Name the executing tool* — done above.
2. *Confirm the RUNNER emits what is registered.* ⛔ **`scratchpad/s48_demo.sh`
   HARDCODES `for f in maps/*.map26` (all 25 maps) and has NO map-list argument
   — unlike `s48_demo_battery.sh`, which takes one. Its only argument is the
   OUTPUT PATH.** ⇒ **the pool restriction is NOT a flag the script has, and
   running it as-is reproduces the off-pool 100-cell demo.** The F-battery
   therefore either (i) edits the `MAPS` loop to the 15-map pool in a copy, or
   (ii) runs all 25 and the readout filters to the 15 pool maps at analysis time
   (which is exactly what this document's `DOSE` figures did, and it is
   sufficient — the extra 10 maps are discarded rows, not contamination).
   **The readout MUST print the map list it actually scored either way.**
3. *`--tle` parity.* `s48_demo.sh` runs `--tle 0`; the shard runs **`--tle 10`**
   (`tools/overnight.sh:138`). ⭐ **THIS IS THE CLAUSE THAT COULD HAVE GONE THE
   OTHER WAY AND IT DOES NOT PASS CLEANLY: the firings battery measures a
   chassis the screen does not use** (`tools/overnight.sh` documents
   `_v145bestfit` winning 6/6 with the limit off and losing 5/6 with it on).
   `--tle 0` is REQUIRED for the determinism precondition (a paired cell is only
   a function with `NOISE_ON=False` **and** the CPU killer off), so the two
   requirements are in genuine tension. **Registered disposition: F1/F2 run at
   `--tle 0` because a paired dose read needs determinism, and F3 additionally
   re-runs the six largest pool maps at `--tle 10` to confirm the BFS does not
   trip the budget there. A dose measured at `--tle 0` may not be quoted as a
   statement about the screen's chassis.**
4. *Consequence of silent non-execution* — if the ore flood latches off (§7) the
   arm's spawn tiles equal the base's and F1's excess delta reads 0 with no error
   anywhere. **That is the mechanism falsifier, and F3 is what distinguishes it
   from a decoder fault.**

**Registered size: 60 treatment sides + 60 control sides** (15 pool maps × both
seats × 2 probe opponents, one deterministic game per cell — the seed axis is
INERT under `NOISE_ON=False`, measured byte-identical opening columns for seeds
11 and 22 in all 32 cells of the first harness run, so replicating over seeds
manufactures n without adding information).

* **F1 — DOSE DELIVERY ON THE POOL THE SCREEN PLAYS.** `s48_spawnring.py` column
  5 (spawn-tile excess walk), treatment vs control, per map and pooled.
  **Pre-registered expectation: excess FALLS in a majority of the 15 pool maps
  and pooled.** Draft anchor, reported as an anecdote and NOT as an expected
  effect: **21 → 10 on icefloe/A, seed 11.** ⚠ **The excess CANNOT reach 0 by
  design** — ordinals 0 and 4 keep the hash order, so the arm's floor is the
  excess those two contribute. **"Excess still positive" is NOT under-delivery
  and may not be read as one.**
* **F2 — OPENING TEMPO, THE PAIRED TABLE.** `s48_open_table.py` columns `h1`,
  `c1`, `harv8`, `conv8`, `bld8`, `conv25`, paired per (map, seat, opponent).
  **Pre-registered expectation: `c1` and `h1` EARLIER, `conv8` HIGHER, `bld8`
  ~flat.** Draft anchors (pool-restricted, 60 cells, recomputed by this agent
  from the committed demo rows): `c1` −1.62, `h1` −1.63, `conv8` +0.85, `bld8`
  +0.08.
* **F3 — THE THREE STRUCTURAL CLAIMS, EACH AS A CHECK THAT CAN FAIL.**
  (i) **ORDINALS 0 AND 4 UNCHANGED** — the arm's and base's 1st and 5th spawn
  tiles must be IDENTICAL on every `NOISE_ON=False` cell. A single mismatch fires
  the instrument-alarm falsifier. (ii) **LATCH RATE** — count pool maps on which
  ordinals 1–3 are identical between arm and base, i.e. the flood latched off or
  the best tile was already the hash's choice. **A latch rate near 15/15 means
  the plank is inert on the screen fixture.** (iii) **CPU AT THE SERVER VALUE** —
  the six largest pool maps re-run at `--tle 10`, expecting 0 tracebacks and 0
  TLE. ⚠ **This is a WEAK check and its weakness is stated: local replays
  zero-fill `execTimeUs`** (s42 D33: `tle_census.py` reads 0 across 1,649 local
  builder-turns while reading 8,847 µs on platform replays), **so "no TLE
  observed locally" is the absence of a symptom, not a CPU measurement.**

### K1–K4 — THE KILL-CHANNEL READ. REGISTERED METRICS, NOT PROSE. READ BEFORE THE PRIMARY, BESIDE F1–F3.

**WHY THESE ARE REGISTERED AND WHY IT IS NOT OPTIONAL.** In this tree the forward
sentinel is gated on `SLOT_HARVESTERS >= 2` AND `bank >= sentinel_cost + 40`
(`raid.py:673-678`, §4), so **an economy plank mechanically moves the gate that
releases the raid.** A prereg that registered only `c1` / `conv@8` / `h1` would
bank a possible KILL LEVER as a correctness fix, and a flat share would leave the
eco claim and the kill claim indistinguishable. **These metrics exist so cells 2
and 3 of the 2×2 below can be told apart.**

**⛔ AND THE NARROW MECHANISM CLAIM, which is the honest one and is narrower than
"the opening is faster":** `LOKI_OPENFAST_SEATS = (1, 2, 3)` leaves **ordinal 0,
the raider, and ordinal 4, the home defender, placed exactly as the base places
them** (verified in the diff, and registered as the checkable prediction F3(i)).
⇒ **the raider's own walk is UNCHANGED, so the arm cannot reach the kill clock by
moving the raid body. The ONLY channel is the SHARED harvester+bank gate at
`raid.py:673-678`, plus the cost-scale term inside `get_sentinel_cost()`.** That
is the claim on the record. Any readout sentence attributing a kill-clock movement
to "a faster opening" in some broader sense is unregistered.

* **K1 — ROUND OF THE FIRST FORWARD SENTINEL, ITT over ALL cells.** Instrument:
  **`tools/replay_census.py <replays…>`** (verified executable at draft; columns
  `a_sentinel_r`/`a_sentinel_at` and `b_sentinel_r`/`b_sentinel_at` — "first-build
  round + position, per team, per entity type", its own documented headline),
  with FORWARD/HOME classified as `d²(first-sentinel tile, ENEMY core NW corner)
  ≤ 50` — the same 50 the gate itself uses at `raid.py:681` (`dsq_core(p, E) > 50
  → return False`) — and both core positions read out of
  **`scratchpad/s48_open_table.py <replay> --team {0,1} --rounds 1 --label X`**
  (column 3). **REPORT BOTH THE MEDIAN *AND* THE SHARE OF CELLS THAT EVER PLANT
  ONE** — a shift in the median means nothing if the denominators differ, and my
  own draft read moved the denominator (base 25 FWD / 5 HOME → arm 29 FWD / 1
  HOME). **Report the paired MEAN, the paired MEDIAN, the sign test, and the
  count of cells beyond ±20 rounds, because the draft read had a zero median and
  a heavy tail and a single summary statistic hides that.**
  **PRE-COMMITTED READING:** *if OpenFast does not move K1, the eco→kill link is
  not being exercised and the arm is a pure correctness fix — it may be banked as
  a tempo fix and it may NOT be described as a kill lever.* **If K1 moves LATER
  beyond the D1 exclusion, the arm is off-programme regardless of its share**
  (`PLAY_DEFENCE: not_at_the_kill_s_expense`).
* **K2 — TIMELY-KILL-BY-r300, ITT over ALL cells.** `cond == core_destroyed` AND
  won by us AND `turns <= 300`, **denominator every game the arm played**. This is
  the programme's own primary and is the metric on which an eco plank earns the
  right to be called on-currency. Shard-native; **it is the same quantity as D1
  and is registered here in the kill block so the K-set is readable as a set.**
  The kill-conditioned version is DIAGNOSTIC ONLY (collider).
* **K3 — ROUND OF THE FIRST TURRET OF ANY KIND** (`min` over the sentinel, gunner
  and launcher first-build rounds from the same `replay_census.py` row).
  **Registered because the TW hazard gates on our first VISIBLE TURRET, not on
  our first sentinel**, and the draft read found first-gunner moving in a
  different direction from first-sentinel on the few cells where a gunner is built
  at all (n = 3 of 30 — gunners are rare in this tree, so K3 will in practice be
  the sentinel round in ~27 of 30 cells; that is a fact about the tree and is
  reported rather than hidden).
* **K4 — THE ECO TIMINGS, EXPLICITLY DEMOTED.** `c1`, `h1`, `conv@8`, `harv@8`,
  `bld@8`, `conv@25` (F2 above) are **MECHANISM METRICS**. They evidence that the
  plank FIRED. **They do not evidence that it PAID, they are off-currency under
  `R1000_IS_DEFEAT`, and no verdict, bar or promotion on this page may be
  denominated in any of them.**

### ⭐ THE 2×2 DISAMBIGUATION — one pre-committed sentence per cell, written before the shard exists

Registered so no successor can re-read it after the fact. Rows: did the ECO
timings (K4/F2) move as designed? Columns: did the KILL metrics (K1/K2) move?

| | **KILL metrics MOVE (K1 earlier and/or K2 up)** | **KILL metrics FLAT** |
|---|---|---|
| **ECO timings MOVE** | **CELL 1 — THE INTENDED RESULT AND THE ARM IS A KILL LEVER.** The gate at `raid.py:673-678` was the binding link, the harvester half dominated the bank half, and OpenFast is on-currency rather than a correctness fix. Promote to a combination input and to a registered head-to-head. Report K1's denominator shift beside its median. | **⭐ CELL 2 — THE PLANK FIRED AND THE ECO→KILL LINK DID NOT TRANSMIT. THIS IS A PURE CORRECTNESS FIX AND MUST BE BANKED AS ONE.** The dose was delivered (F1's spawn excess fell, F2's `c1`/`h1` moved) and the gate did not open earlier — which means the BANK half of `raid.py:673-678` absorbed the harvester half's gain, exactly the §4 mechanism. **Pre-committed consequence: the arm may NOT be called a kill lever, its share result stands on its own as a screen, and the named successor is a BANK GUARD (do not fund belt below `sentinel_cost + LOKI_FWD_TI_FLOOR` before the first forward turret) — a different plank with its own prereg.** ⚠ This is the cell my draft-time §4 measurement predicts, and predicting it in advance is what makes it informative instead of a post-hoc story. |
| **ECO timings FLAT** | **⭐ CELL 3 — AN INSTRUMENT OR ATTRIBUTION PROBLEM, AND HERE IS HOW TO TELL WHICH.** OpenFast has no channel to the kill clock that does not pass through the eco timings (the raider's spawn tile is untouched — see the narrow mechanism claim above), so eco-flat + kill-moved cannot both be true of this plank. **THE DISCRIMINATOR IS F1, AND IT IS READ FIRST: (a) if F1's spawn excess ALSO did not fall, the plank never fired — the ore flood latched off (§7) or `known_map_for` missed — and the kill movement is UNATTRIBUTABLE noise or a wiring fault; run the §"Wiring check" md5/basename triple before anything else. (b) if F1's excess DID fall while F2's `c1`/`h1` did not move, the plank fired and the TEMPO METRIC IS THE BROKEN INSTRUMENT — the arm moved the spawn tile without moving the opening, which contradicts the `c1 − h1 == 1` structural fact measured in 90 of 97 base cells and means the decoder or the window is wrong, NOT that the bot changed. (c) if both F1 and F2 moved and only my K4 aggregate reads flat, the aggregation is wrong.** In every branch the kill movement is NOT credited to this arm. | **CELL 4 — THE PLANK DID NOTHING MEASURABLE ANYWHERE.** Read F1 first: excess-not-fallen ⇒ the mechanism falsifier fires and the primary is reported **NOT MEASURED**; excess-fallen-but-nothing-downstream ⇒ the spawn tile is not the binding constraint the diagnosis claimed, which is the one branch that genuinely refutes the §Hypothesis diagnosis, and it closes the road. |

### D1–D3 — the kill-clock read. MEASURABLE, shard-native (`cond`, `turns`, `winner`).

* **D1 — ITT TIMELY-KILL RATE** (the `DEFENCE_ADMISSION_BAR` primary), per the
  `KILL-ROUND NON-REGRESSION` line above: share of ALL of each arm's games ending
  in OUR core-kill with `turns ≤ 300`, scored as an EXCLUSION of a 2.0pp fall.
* **D2 — MEDIAN KILL ROUND**, treatment vs control, as the gross backstop (a
  median crossing 300 is disqualifying), reported alongside the r1000 share since
  `R1000_IS_DEFEAT` makes an r1000 game a cost even when its tiebreak is won.
* **D3 — ITT RMST300** — `tools/fieldcal_read.py:239 rmst_score`, mean of
  `min(turns, 300)` with every game not ending in OUR core-kill scoring the full
  300, with its interval from `tools/cluster_ci.py`. **ITT over ALL rows, not
  over kills only** — the kill-conditioned form carries a collider.
* **D4 (diagnostic) — the kill-win-CONDITIONED share**, reported beside D1 so the
  size of the collider on THIS fixture is on the record. **Diagnostic only.**

### NOT MEASURABLE on this leg — named, not silently dropped.

* **Cost scale at any round.** The §4 cause — the arm reaching +20%-per-builder
  and +1%-per-conveyor scale earlier, which is what makes
  `bank >= sentinel_cost + 40` bind later — **cannot be read on either surface
  here.** The shard tape carries no resource, scale or build column and its
  replays are discarded; `replay_census.py` reports counts and first-build rounds,
  not the scale factor or the bank. **The EFFECT is measured (K1's first-sentinel
  round); the CAUSE is inferred.** ⇒ **no readout sentence may assert that the
  scale term is or is not what moved K1** — that attribution needs a
  scale-instrumented battery this leg does not run.
* **Whether the clustered eco births hurt the SECOND and THIRD harvester** (§5).
  The demo window closes at r25 and the F-battery inherits that window. **NOT
  MEASURED by this leg**; a successor that wants it must extend
  `s48_open_table.py --rounds`.
* **Titanium actually DELIVERED** (`titanium_collected`) — no resource column on
  the tape. Under `R1000_IS_DEFEAT` this is the correct thing to be blind to
  (delivery is instrumental), but the blindness is stated rather than glossed.
* **Per-unit CPU** — see F3(iii): local replays zero-fill `execTimeUs`, so no CPU
  claim is available from this leg. The commit's "0 TLE at `--tle 10`" is an
  anecdote about crash-freedom, not a CPU measurement.
* **Seed determinism on the SHARD.** `NOISE_ON = True` in the fired trees
  (`doctrine.py:474`), so base-vs-base at one seed diverges at round 0. **No
  seed-matched or replay-diff equivalence claim is available on the SHARD
  fixture**; the flag-off equivalence claim lives on the separate `--tle 0` +
  `NOISE_ON=False` harness, never on shard rows.
* ⚠ **AND A NOISE ASYMMETRY THE SHARD CANNOT SEE BUT WHICH IS REAL:** with
  `NOISE_ON = True`, the control's spawn key is `hash+salt` alone and is fully
  re-rolled per match, while the arm's PRIMARY key (ore distance) is deterministic
  and the salt only breaks ties. **The treatment arm is therefore strictly LESS
  variable in its opening than the control.** This does not bias the share
  estimate — both arms play the same 5,400 seeds — but it means the two arms do
  not have the same variance, and it partly undoes the `NOISE_ON` anti-repeat
  plank on three of five opening seats (§Hypothesis, effect 4).

---

## THE CHANGE — `file:line`, control → treatment. THE ONE-PLANK CLAIM, VERIFIED

**TREATMENT TREE: `bots/_v486openfast`** — byte-for-byte `bots/_v468kladturbo`
apart from **TWO** files. Verified at draft with `diff -rq` and with `md5 -q` on
each of the four sources:

| file | control md5 | arm md5 | verdict |
|---|---|---|---|
| `eco.py` | `47dc496fc0d14ba950c45c3d43a5f9d0` | `47dc496fc0d14ba950c45c3d43a5f9d0` | **BYTE-IDENTICAL ✓** |
| `raid.py` | `e0ebf255ed30782de9694c2f4b18d9a7` | `e0ebf255ed30782de9694c2f4b18d9a7` | **BYTE-IDENTICAL ✓** |
| `doctrine.py` | `56bba300560195498dbd977e86523b5a` | `08b230f503099cf316797ddc45b4055f` | 1 hunk, **append-only, +80 / −0** |
| `main.py` | `f2eb2b90fdd17acb403ffa8a5d33e014` | `4a83fc3fb90332dd99a3a2b5ed2a4ad6` | 4 hunks, **+101 / −3** |

**⭐ THE COORDINATOR'S DIFF CROSS-CHECK, VERIFIED INDEPENDENTLY — CONFIRMED IN
SUBSTANCE, CORRECTED IN THE COUNTS.** I was asked to confirm or refute: *`main.py`
+103 (one sort key at `:488-504` behind `LOKI_OPENFAST_ON`), `doctrine.py` +83,
`eco.py`/`raid.py` byte-identical, `LOKI_OPENFAST_SEATS = (1,2,3)` leaving raider
seat 0 and home seat 4 untouched.*
* **`eco.py` / `raid.py` byte-identical — CONFIRMED** by md5 both ways (table
  above). **This is the strongest clause of the whole claim and it holds.**
* **`LOKI_OPENFAST_SEATS = (1,2,3)`, ordinals 0 and 4 untouched — CONFIRMED** at
  `doctrine.py:1966` and `main.py:496`, with `self.n` the Core's monotone spawn
  counter (`main.py:65,514`).
* **One sort key behind `LOKI_OPENFAST_ON` — CONFIRMED**, at `main.py:494-504`
  (the coordinator's `:488-504` brackets it slightly wide; the guard is `:496`,
  the base sort `:499-500`, the ore-led sort `:502-504`).
* **LINE COUNTS — CORRECTED.** Non-header added/removed lines are **`main.py`
  +101 / −3** and **`doctrine.py` +80 / −0**, not +103 / +83. The larger figures
  count the `---`/`+++`/`@@` header lines. Immaterial to the claim; corrected
  because a number on this page has to be the number.
* ⛔ **AND THE COUNT THAT MATTERS IS NOT A LINE COUNT: `main.py` has FOUR hunks,
  not one** — the `Environment` import (`:33`), the `self._of_dist = None` field
  (`:81`), the 78-line `_openfast_dist` method (`:233-310`) and the sort
  (`:494-504`). A summary that says "one sort key" is true about the DECISION and
  understates the SURFACE. All four are enumerated in `THE CHANGE` above.

1. **`doctrine.py` +1884-1968** — ONE append-only hunk (`@@ -1883,3 +1883,86 @@`):
   a rationale block and FOUR constants, `LOKI_OPENFAST_ON = True`,
   `LOKI_OPENFAST_SEATS = (1, 2, 3)`, `LOKI_OPENFAST_NODES = 1200`,
   `LOKI_OPENFAST_FAR = 99`. **No existing line in `doctrine.py` is modified.**
2. **`main.py:33`** — the import gains `Environment` (needed by the vision
   fallback in the flood).
3. **`main.py:81`** — one field, `self._of_dist = None`. **No store slot.**
4. **`main.py:233-310`** — one new method, `_openfast_dist`: a node-budgeted
   multi-source BFS outward from ore-adjacent tiles, computed at most once per
   match, `try/except`-wrapped with the base ordering as the exception result,
   and latching `{}` when no ore is known.
5. **`main.py:494-504`** — the plank: `of = self._openfast_dist(ct) or None` under
   `LOKI_OPENFAST_ON and self.n in LOKI_OPENFAST_SEATS`, then either the base sort
   (unchanged, `:499-500`) or the ore-led sort with the base key demoted to
   tie-break (`:502-504`).

**THE FOUR BYTE-IDENTICAL CLAIMS, EACH CHECKED RATHER THAN ACCEPTED:**
* **`eco.py` byte-identical — HELD** (md5 match). ⇒ `_link_path`, `_pick` and its
  stripe, `_wire_on_build`, `known_map_for` are untouched.
* **`raid.py` byte-identical — HELD** (md5 match).
* **SAMESTOP untouched — HELD, and stronger than claimed:** `_samestop_plan`,
  `_samestop_arm`, `_samestop_fire` and `_build_next_link` all live in `eco.py`,
  which is byte-identical, so the claim is implied by a whole-file md5 rather than
  by a hunk read.
* **TURRET ORDINALS / TURRET SITING UNCHANGED — HELD.** No turret build site,
  cost, ordering or gate appears in either changed hunk; every turret path is in
  `eco.py`/`raid.py`, both byte-identical. ⇒ **the Odin-class turret-window
  side-effect registration does not bind on this arm** — see the hazard table
  below, where it is recorded as CHECKED, not assumed.
* **`LOKI_BASE_BUILDERS` untouched — HELD** (`doctrine.py:1195`, outside the
  append-only hunk; the arm spawns the same number of bodies at the same rounds,
  modulo the §4 sixth-body effect which is downstream of the gate, not a change
  to it).
* **ORDINALS 0 AND 4 PLACED AS BASE — HELD IN THE CODE, and registered as a
  CHECKABLE PREDICTION rather than banked** (F3(i)). The guard is
  `self.n in LOKI_OPENFAST_SEATS` with `LOKI_OPENFAST_SEATS = (1, 2, 3)`, and
  `self.n` (`main.py:65,514`) is the Core's monotone spawn counter, never
  decremented — so replacements (`n ≥ 5`) are also placed as base.

---

## HAZARD TABLE — checked, not assumed

| hazard | status | evidence |
|---|---|---|
| **Odin-class turret-window (TW) gate** (an arm that delays our early visible turrets re-enables that weapon against us; it gates on never-having-seen-a-turret) | ⛔ **CHECKED, AND IT BINDS — VIA AN INDIRECT CHANNEL, MEASURED, WRONG DIRECTION IN THE TAIL** | **THE CODE HALF IS CLEAN:** every turret site, cost, ordering and gate lives in `eco.py`/`raid.py`; both are **byte-identical** by md5, and the two changed hunks contain no turret reference. ⇒ no turret code is touched. **THE BEHAVIOURAL HALF IS NOT CLEAN, and this is why the code check was not allowed to settle it:** the sentinel gate at `raid.py:673-678` reads `SLOT_HARVESTERS` and the BANK, both of which OpenFast moves. Measured by this agent at draft over 30 pool cells (§4): first-sentinel paired **mean +5.60 rounds LATER**, **median delta 0.0**, sign test **p = 0.523**, but **9 cells delayed ≥20 rounds** (worst `glacierkeep/A` **18 → 111**) against 4 advanced ≥20. **A per-game weapon keys on the TAIL, not the median** ⇒ **DISQUALIFYING-CLASS, held at n = 30, unresolved.** Registered as **K1/K3** on the full 5,400-game shard and as the second lock-blocking item (`KNOWN OPEN ITEM 3`). ⚠ Partial offset, also measured: the arm plants the FIRST sentinel FORWARD in 29 of 30 cells vs the control's 25 of 30 — more siege, later siege. |
| `LOKI_OPENFAST_SEATS` vs `LOKI_ECO_SEATS` **duplication** | **CHECKED — currently exact, structurally fragile** | Both are `(1, 2, 3)`. But `main.py:546-551` applies a POINT-OF-USE override: inside `LOKI2_RUSH_RND` (60), seats in `LOKI2_RUSH_SEATS = (0, 1)` become RAIDERS, not eco. **`LOKI2_RUSH_ON = False`** (`doctrine.py:1409`) so the override is inert today ⇒ the two tuples agree. **If `LOKI2_RUSH_ON` is ever flipped on, seat 1 becomes a raider and OPENFAST still gives it an ore-biased spawn tile.** Registered as a coupling to check before any combination with a LOKI-2 arm. |
| Core spawn ordinal (`self.n`) vs role seat (`SLOT_ROLE_N`) **desync** | **CHECKED — present in BOTH arms, cannot bias the contrast** | `self.n` (`main.py:514`) counts spawns at the Core; `SLOT_ROLE_N` (`main.py:528-530`) counts builders' FIRST RUN, in a buffered store slot. A builder that dies before ever running, or two builders first-running in the same round, shifts the role sequence relative to the spawn sequence. **This is base behaviour, identical in control and treatment, and unreachable in the opening (the Core spawns at most one body per round because spawning consumes the action cooldown).** Named so a certifier does not read "ECO ordinals" as a claim about ROLES. |
| **BFS cost / CPU** | **PARTIALLY CHECKED — the local instrument is blind** | One flood, ≤1200 nodes, once per match, on the Core only, `try/except`-wrapped. Commit reports 0 TLE at `--tle 0` across the demo and 0 at `--tle 10` on the six largest maps. ⚠ **Local replays zero-fill `execTimeUs`, so this is the absence of a symptom, not a measurement** — see F3(iii) and `NOT MEASURABLE`. |
| **Flood correctness when `known_map_for` returns `None`** | **CHECKED — degraded but safe** | Walls and ore come from Core vision (r²=36) only, so distances can be wrong where an unseen wall blocks a route. The consequence is a worse ORDERING, never an illegal action: `main.py:505-513` still runs the base's legality loop (`0 <= sp.x < w`, `can_spawn`). No crash channel. |
| **Enemy exploitation of a predictable spawn ring** | **NOT ASSESSED — out of scope, named** | The arm makes eco spawn tiles far less divergent game-to-game (§Hypothesis effect 4). Whether an opponent can exploit a predictable eco-side spawn ring (spawn-tile denial is one of the roads `CLAUDE.md` lists as open — **for US**, and it cuts both ways) is not measured here and is not claimed either way. |

---

## KNOWN OPEN ITEMS — with dispositions, and ITEM 1 IS A LOCK BLOCKER

**1. ⛔⛔ THE FLAG-OFF EQUIVALENCE CLAIM HAS NO COMMITTED ARTIFACT. SAME DEFECT
CLASS AS `SEALPIERCE`, WHICH THE s48 HANDOVER ALREADY NAMES AS A LOCK BLOCKER.**
The commit body asserts *"replay-SHA over 16 cells, flag-off == base 16/16 MATCH,
flag-on != base 16/16 DIFFER"*. **`git diff --name-only 78965d91^ 78965d91`
returns TEN paths and NOT ONE of them is a flag-off script or transcript.**
`scratchpad/s48_flagoff.sh` exists on disk but arrived with `d67eb98e`
(the ECOMMIT commit), and **its own DRIVE-EVIDENCE note records a drive against
`_v477ecommit` / `LOKI_ECOMMIT_ON` over 8 cells — not against OPENFAST.**
⇒ **the 16/16 + 16/16 result is an unbanked assertion.**
**DISPOSITION:** before lock, either
(a) run `zsh scratchpad/s48_flagoff.sh _v486openfast LOKI_OPENFAST_ON` and COMMIT
its transcript, or
(b) the primary carries **UNVERIFIED FLAG-OFF EQUIVALENCE** on its face and the
`INSTRUMENT-ALARM FALSIFIER` above becomes the only thing standing behind the
one-plank claim at runtime.
⚠ **AND THE CLAIMED CELL COUNT IS INFLATED EVEN IF THE RUN HAPPENED.**
`s48_flagoff.sh` iterates 4 maps × **2 seeds** × 2 seats = 16 cells, and **this
arm's own demo established that the seed axis is INERT under `NOISE_ON=False`**
(byte-identical opening columns for seeds 11 and 22 in 32 of 32 cells). ⇒ **the
effective cell count is 8, not 16**, and one of the four maps (`eider`) is
**OFF-POOL**, leaving **6 effective cells on pool geometry** (`drumlin`,
`icefloe`, `yulerune` × 2 seats). The claim should be restated at that size.

**2. THE UNREPRODUCED BASE-CELL TRACEBACK.** One traceback line was seen once in
a **BASE** cell (`eider` / `opp_v78` / seat B) and did not reproduce in 8 repeats
of that exact cell. **DISPOSITION: an OPEN, UNEXPLAINED item, not a cleared
one.** It is not disqualifying for OPENFAST because (i) it appeared in the
CONTROL, so it cannot be caused by a plank the control does not have, and (ii)
`eider` is **not in the 15-map corefill pool**, so the shard never plays that
geometry. **WHAT WOULD MAKE IT DISQUALIFYING:** any traceback in an ARM cell
during F1–F3, or any traceback on a POOL map in either arm. **The F-battery must
grep its stderr for `Traceback` and PRINT THE COUNT — including a count of zero.**
A battery that reports nothing about tracebacks and a battery that saw none must
not render identically.

**3. ⛔⛔ THE MEASURED FIRST-TURRET DELAY IN THE TAIL — THE SECOND LOCK BLOCKER.**
Fully stated at §4 and in the hazard table; recorded here so the two blockers are
in one list. **DISPOSITION — the builder chooses one before lock:**
* **(a) LOCK AS IS, with K1/K3 as the adjudicator.** Defensible: the median delta
  is 0.0 and the sign test is p = 0.523, so at n = 30 nothing is established
  except a tail worth watching, and the 5,400-game shard with K1/K3/D1 registered
  is precisely the instrument that resolves it. **This is what I recommend**, and
  it is only defensible BECAUSE the metrics are now registered — locking with the
  eco timings alone would have banked the tail as unknown.
* **(b) HOLD AND ADD A BANK GUARD** — refuse to fund belt below
  `sentinel_cost + LOKI_FWD_TI_FLOOR` before the first forward turret exists.
  This attacks the measured cause directly (the bank half of `raid.py:673-678`),
  but it is a **SECOND PLANK**, it makes the arm a two-plank bundle whose
  attribution is capped, and it needs its own prereg. Do not smuggle it into this
  one.
* **(c) NARROW THE PLANK to ordinals 1 and 2**, leaving seat 3 on the base
  ordering, on the theory that a smaller belt acceleration spends less bank
  before the gate. **Untested, and it halves the dose the whole arm exists to
  deliver.** Named for completeness; I do not recommend it.
**WHAT WOULD MAKE IT DISQUALIFYING RATHER THAN WATCHED:** K1 later with D1's 95%
CI lower bound failing to exclude a 2.0pp fall in the ITT timely-kill rate, or a
median kill round crossing 300. Either fires and the arm is off-programme
whatever its share reads.

**4. THE DEMO'S SEED AXIS WAS INERT AND ITS OPPONENT AXIS NEAR-DEGENERATE —
WHAT THAT DOES AND DOES NOT LICENSE.** 41 of 50 (map, seat) cells were identical
under both `opp_v63` and `opp_v78`, so the commit's "100 paired cells" are **50
informative (map, seat) cells**, and my pool-restricted recomputation is **30
informative cells** of the 60 I report.
* **IT DOES LICENSE:** the claim that the plank's opening effect is
  **opponent-independent pre-contact**. That is a genuine CHECK the near-degeneracy
  performs, and it is the right reading of it.
* **IT DOES NOT LICENSE:** treating 100 (or 60) as an n. Any interval, sign test
  or p-value computed on those cells as if they were independent observations is
  **wrong by a factor of ~2 in n**, and no such number appears on this page.
* **AND IT DOES NOT LICENSE ANY SHARE FORECAST AT ALL**, for a reason that is
  about the fixture and not the n: the demo's opponents are `opp_v63`/`opp_v78`,
  **probe bots WE WROTE**, while the screen's opponent is **Sleipnir v1**. Those
  are different fixtures and CLAUDE.md is explicit that our own probes lie in a
  known direction.

---

## AMENDMENTS

**ADD-ONLY, and blind to the data.** Any amendment to this document appends a
dated `AMENDMENT n` section, never edits a registered line, and must be committed
BEFORE the shard's first game or (for a post-start amendment) must be
demonstrably blind to any tape row — the demonstration being that no row existed
at the amendment's git author time, or that the amendment's author had not read
the tape. **The `GATE RESOLUTION` line is pre-flagged as requiring an amendment if
the lane picks resolution (b) or (c) of ITEM 1**; that amendment is blind by
construction because the choice is made before the first game.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one local core to n = 5,400, plus ~120 local games for the F-battery and
the K-battery (which share their replays — `replay_census.py`, `s48_spawnring.py`
and `s48_open_table.py` all read the same `.replay26` files, so K1/K3 cost no
extra games).**
ZERO rated ladder exposure, zero submissions, zero unrated challenges — nothing
on this page touches the platform, which is why `TARGET BAND` is N/A.

**Wiring check before the primary (the S1-shape check, and it is cheap):**
(i) `md5 -q bots/_v486openfast/*.py bots/_v468kladturbo/*.py` must reproduce the
six hashes in `THE CHANGE` table, and `md5 bots/_v468kladturbo` must match
`scratchpad/CONTROL_PIN` (`a9228ccb56ed9a65dd7d72ad1cb96068`); (ii) both
basenames must appear as winners on `scratchpad/overnight/OPENFAST.tsv` — a
column that is constant is the alarm, not the result; (iii) **the identical- and
substring-basename hazard `tools/overnight.sh:70-76` warns about is CLEARED at
draft: `_v486openfast` is not a substring of `_v468kladturbo` and vice versa**,
so the `case "$L" in *"$B"*` scoring cannot mis-attribute a game.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder, which is the pipeline step Magnus's procedure names verbatim (*"we start
by testing it against the current slot, If it beats it we can switch"*). **Gate-1
to gate-2 transitivity is UNVALIDATED in this repo (QUEUE #65: 3 concordant, 1
not), so the head-to-head is not skippable on the strength of this number.**

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read in full: obligations 7, 12, 13, 14, 15a-c, 16 + its OB16 corollary of 2026-08-15T03:52:45Z, 17, and the 2026-08-17T07:24:55Z local-shard clock-2 addendum, whose corrected boilerplate is cited rather than restated above) · `PROGRAMME.md` (the parsed field block at :8-22 — `INCUMBENT: bots/_v468kladturbo`, `R1000_IS_DEFEAT: yes`, `PLAY_DEFENCE: not_at_the_kill_s_expense`, `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`, `FIXTURE_OF_RECORD: live_unrated`; and :486-525, the r300 re-pricing of 2026-08-16T05:15:45Z, the collider correction of 2026-08-16T05:19:38Z and the estimator-under-arbitration note of ~05:3xZ) · `docs/prereg/PREREG-BELTBREAK-EARLY-2026-08-17.md` (house style; its `REFERENCE n` and `METRIC WINDOW` forms) · `docs/prereg/PREREG-ECOMMIT-2026-08-17.md` (house style, the four-band reading precedent, the CLUSTER UNIT enumeration form) · `docs/prereg/BARS.tsv` (header, the FIRINGS-BEFORE-PRIMARY rule adopted 2026-08-16T13:27:33Z, the six sibling `51.33 ge` rows, and the measured absence of any `COMBO-BAR-EXEMPT` token) · `docs/research/ECO-STUDY-fast-connected-harvesters-2026-08-17.md` · `CLAUDE.md` · git commit `78965d91` (full body and `git diff --name-only 78965d91^ 78965d91`) · `bots/_v486openfast/{doctrine,eco,main,raid}.py` and `bots/_v468kladturbo/{doctrine,eco,main,raid}.py` (diffed file-by-file with `diff -rq`, `diff -u` and `md5 -q`) · `tools/prereg_check.py` (read for `RULES`, `key_pattern`, `check_presence`, `check_arithmetic`, `check_metric_window`, `_gate_is_floor`, `_defensive_plank`, `_defence_bar_ok`) · `tools/auto_gate.py` (:244-247 the marks, :261 `TREND_FLOOR`, :264-278 `COMBO_BAR` and its pricing, :280-313 the confirmation-class exemption and the registration-time token rule, :715-741 `combo_of`, :820-899 the catastrophe/G7/trend-floor clauses, :902-958 the combo-bar clause) · `tools/overnight.sh` (:60-76 the 15-map pool and the basename-substring guard, :99-104 the `# FIXTURE start=` stamp, :138-139 `--tle 10` and `--replay /dev/null`) · `tools/fieldcal_read.py:230-250` (`our_core_kill`, `rmst_score` — the registered RMST estimator) · `tools/cluster_ci.py --help` · `tools/replay_census.py` (read for its docstring and the `*_sentinel_r`/`*_sentinel_at`/`*_gunner_r` column family; **executed** on 60 replays for the K1 draft read) · `bots/_v468kladturbo/raid.py:667-682` (the forward-sentinel gate — the coordinator's cross-check, verified at those exact lines: `rush`/`min_harv`/`ti_floor` at :673-675, the `SLOT_HARVESTERS` test at :676, the `sentinel_cost + ti_floor` bank test at :677-678, the `dsq_core(p, E) > 50` siting bound at :681) · `bots/_v468kladturbo/doctrine.py:379-381,935,1264-1265,1409-1412` (`SLOT_HARVESTERS` as a monotone high-water mark, `LOKI_FWD_TI_FLOOR = 40`, `LOKI_FWD_MIN_HARV = 2`, `LOKI2_RUSH_ON = False` and the rush-window constants) · `bots/_v486openfast/main.py:520-560` (the `SLOT_ROLE_N` role assignment and the `LOKI2_RUSH_SEATS` point-of-use override) · `scratchpad/s48_demo.sh` · `scratchpad/s48_open_table.py` (read in full, including its print block, to establish column semantics) · `scratchpad/s48_spawnring.py` (read in full; column 5 is `sum(got d) − sum(best-5 ring d)`) · `scratchpad/s48_flagoff.sh` (read in full, including its DRIVE EVIDENCE note, which is what established ITEM 1) · `scratchpad/s48_demo_rows.tsv` (the committed 200-row demo tape, re-aggregated by this agent restricted to the 15-map pool) · `scratchpad/corefill_work.txt` · `scratchpad/CONTROL_PIN` · `results.tsv` (rows 346 `null125-final`, 454 `idnull140-cert-5400`) · `docs/prereg/PREREG-{ECOMMIT2,KLADLADDER2,KLADLADDER3,SEALPIERCE}-2026-08-17.md` (seed-base claims only, for the collision audit) · the drafting brief supplied by the builder lane s48. **Games run by this agent: SIXTY-TWO, all local, all unrated, zero platform exposure** — (i) TWO instrument-verification cells (`icefloe`, seat A, `--seed 11`, `--tle 0`, `NOISE_ON=False`, opponent `opp_v63`) to confirm `s48_spawnring.py` and `s48_open_table.py` execute and accept the arguments registered above; (ii) **SIXTY paired cells (15 pool maps × both seats × {base, arm}, same settings) for the K1 draft read in §4**, censused with `tools/replay_census.py` into `/tmp/ofcen_census.tsv`. All games were run on throwaway copies `bots/_ofchk_{base,arm}` with `NOISE_ON` patched to `False`; **both copies were deleted and neither `bots/_v486openfast` nor `bots/_v468kladturbo` was modified.** ⚠ The 60-cell battery's outputs live under `/tmp` and are NOT banked; the builder should re-run it (or bank it) if the §4 table is to be cited outside this document — **the numbers in §4 are reproducible from the recipe stated there, but they are not currently a committed artifact, and that is the same defect class as `KNOWN OPEN ITEM 1`, disclosed here about my own work rather than only about the builder's.** No shard was started, no row was appended to any worklist or registry, and no file under `bots/`, `tools/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md` or `QUEUE.md` was created or modified.
