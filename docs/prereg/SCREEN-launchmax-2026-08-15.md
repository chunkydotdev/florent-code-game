# SCREEN PREREG — `launchmax`: the LAUNCHER-DENIAL **CEILING PROBE**

## ⛔ PAGE ONE — WHAT THIS IS AND WHAT IT IS NOT

**THIS IS A CEILING PROBE. IT IS NOT A SHIP CANDIDATE.** No branch of this
document ends in an activation, and the KEEP branch buys two follow-on screens,
not a submission. The question is **not** *"is this the best version of the
launcher we can ship?"* — it is **"at the maximum occurrence we can build, does
the denial mechanism pay at all?"**

Magnus, tonight, verbatim, and it is the whole commission:

> *"If we are supposed to try new ideas and we can't build a version where it
> happens more than 1.5% of games, we haven't leaned into it enough. If we are
> trying something new and it barely happens, how can we say we have tried it at
> all?"*

**HE IS DESCRIBING A MEASURED NUMBER, NOT A FEELING.** v140 builds **any**
launcher in **8.2% of games (7 of 85 archived)** and an enemy builder has reached
the pickup envelope of a home launcher in **1 of 17 launcher-games** — so the
denial mechanism occurs in roughly **0.5% of our games**. Every launcher row this
project has killed on a null was killed inside that 0.5%: `docs/coordination.md:49520-49522`
states it as arithmetic — *"every row AIMING an existing launcher (#51/#10/#9-class)
is inert in ~92% of its screen population at v140's 8.2% coverage; #51's AIMTHROW2
read 50.09 exactly as that predicts."*

⇒ **THE PRIOR NULLS ARE COVERAGE-DILUTION NULLS, NOT MECHANISM NULLS.** This leg
makes the launcher exist first, sites it where the victims are, and only then aims
it. **If it still does not pay, the idea is dead and that is the deliverable.**

**⚖ AND THE FIXTURE IS THE MOST FAVOURABLE ONE THE MECHANISM WILL EVER SEE**
(§4). That asymmetry is what makes the negative branch a real closure and the
positive branch a *bounded* one, and it is stated here rather than discovered in
the analysis.

---

**STATUS: committed BEFORE `bots/_v243launchmax` exists on disk, BEFORE the
`LAUNCHMAX` row is appended to `scratchpad/corefill_work.txt`, BEFORE the dose
probe of §6 is run, and BEFORE any row of `scratchpad/overnight/LAUNCHMAX.tsv`
exists.** Two-clock: this file's git author time against the `# FIXTURE … start=`
stamp `tools/overnight.sh:99` writes before the shard's first game (that stamp,
not the first result row, is the leg clock — `overnight.sh:82-95`). Drafted
**2026-08-15T05:09:08Z** (`date -u`, same shell call), repo at **`6c7bc8bd`**
(author time 2026-08-15T06:59:02+02:00). Verified at draft: `ls bots/ | grep -c
"_v243\|launchmax"` → **0**; no `LAUNCHMAX` row in the worklist; no
`scratchpad/overnight/LAUNCHMAX.*` of any kind.

**PROVENANCE: bots/_v223sealrepair/main.py:593-663 · bots/_v223sealrepair/raid.py:875-950 · bots/_v223sealrepair/doctrine.py:937,965,1275-1276,1536 · bots/_v233evict58/raid.py:285-292,643-705 · bots/_v233evict58/doctrine.py:1688-1702 · tools/corpus/replay_throws.py · tools/mech_battery.py · tools/overnight.sh · tools/corefill.sh · tools/prereg_check.py · scratchpad/corefill_work.txt · docs/prereg/SCREEN-sealfloor6-2026-08-14.md · docs/prereg/SCREEN-bodyaware-2026-08-14.md · QUEUE.md rows #9/#10/#47/#51/#58 · docs/coordination.md (grepped only, never read whole)**

Drafted by a **fresh agent with no inherited session context** beyond the
commission quoted above and the files named on this line. **No row of any shard
was read as an outcome for this arm; no game was run by this agent; nothing under
`bots/`, `tools/`, `PROGRAMME.md`, `CLAUDE.md`, `HANDOVER.md`, `QUEUE.md`,
`docs/coordination.md` or `scratchpad/corefill_work.txt` was edited.** Historical
finals quoted in §3 and §7 are **priors read from the worklist commentary and
`docs/coordination.md`**, cited with their chassis and n, and are comparators in
no bar on this page.

---

## 1. THE FOUR THROTTLES — EACH VERIFIED AGAINST THE TREE, EACH DECIDED

All four exist and all four are **ours**, not the engine's. Verified line by line
against `bots/_v223sealrepair` at draft:

| # | throttle | anchor | verified value | **decision** |
|---|---|---|---|---|
| T1 | round gate on the HOME launcher | `doctrine.py:1536`, consumed `main.py:613` | `LAUNCHER_MIN_RND = 160` | **NOT LIFTED** |
| T2 | one-way latch capping HOME launchers at one | `doctrine.py:937` `SLOT_LAUNCHER = 6`, consumed `main.py:626-638` | cap 1 (released on death only, `LOKI6_LAUNCHER_RELEASE`) | **NOT LIFTED** |
| T3 | siting: launcher build reachable **only** from `_defend` | `main.py:593` reached only from `main.py:672` | home-only by construction | **⭐ LIFTED** |
| T4 | throw destination sorted **away from OUR core** | `raid.py:925` | `far = sorted(sites, key=…distance_squared(self.core), reverse=True)` | **⭐ LIFTED** |

**The engine's own limits, for contrast:** pickup **d²≤2**, throw **1 ≤ d² ≤ 26
from the launcher**, **0 ammo**, cooldown **+= 1** (so a throw is legal **every
round**), position-only mutation, **no team check, no vision guard.**

### ⭐ WHY T1 AND T2 ARE NOT LIFTED — the honest cost of each, and it is measured

**This is the load-bearing judgement on the page, so it is argued rather than
asserted.** A ceiling probe maximises **OCCURRENCE**. T1 and T2 are **PRICE
levers that buy no occurrence once T3 is in**, and both have already been
measured losing on this exact fixture family.

* **T1 (`LAUNCHER_MIN_RND 160 → 0`) buys ZERO coverage given T3.** The forward
  path added by T3 (`_try_evict_launcher`) carries **no round gate of its own**,
  and its live-measured plant rate is **1.240 launchers/game** against v140's
  **0.341** (EVICT58's pinned leg vs 0033, `QUEUE.md:145`). **T3 alone takes
  coverage from 8.2% of games to ~100%.** Lifting T1 on top of that buys a
  SECOND launcher, at home, in the one place with **1-in-17** pickup
  opportunity. Its measured price: the mechanism-matched ownership premium
  **−6.34pp** (LAUNCH0 52.77 − BOTH0 46.43, n=5,408 each, s37 family sweep,
  v114 chassis, `docs/coordination.md:43852-43854`), plus the early-levy
  penalty visible as **LATE160 51.42 → RES0 48.63 ≈ 2.8pp**. **A price lever
  with no occurrence return has no place in a ceiling probe.**
* **T2 (lift the count latch) cannot move occurrence-in-games and is already
  priced.** The count dose curve was run to completion: **LAUNCH2 44.67 ·
  LAUNCH3 43.73** (n=5,408 each, same sweep) against a 1-launcher control at
  50.0 — the marginal second HOME launcher is **−5.33pp**. Count multiplies
  denial **VOLUME** (a second simultaneously-pinned victim), which is a real and
  interesting bet, but it **doubles the price of the single thing this leg is
  built to isolate** and would make the result uninterpretable.
  ⇒ **PRE-REGISTERED AS THE FOLLOW-ON, NOT SMUGGLED IN**: `LAUNCHMAX2`
  (forward cap 2) is bought **if and only if** this arm clears its bar (§8).

⚠ **THE ARM STILL CARRIES ONE MORE LAUNCHER THAN THE CONTROL** — T3 plants a
forward one in ~100% of games where the control plants any in 8.2%. **That ~0.92
extra standing launchers/game IS the economic non-exchangeability of this leg,
its price is the measured −6.34pp, and §9 bars every economy claim on the back
of it.**

---

## 2. THE CHANGES — `file:line`, old → new, buildable by another agent

**TREATMENT TREE: `bots/_v243launchmax`** — a byte-for-byte copy of
`bots/_v223sealrepair` (v140, LIVE) plus the three hunks below.
**`main.py` and `eco.py` must be BYTE-IDENTICAL to the control; `diff -rq` must
name exactly two files (`raid.py`, `doctrine.py`).**

### CHANGE A (T3, siting) — port `_try_evict_launcher`, minus its siege prerequisite

⛔ **THIS IS A PORT, NOT NEW CODE, AND SAYING SO IS OBLIGATORY** — see §7. The
forward-siting function already exists, compiles, and is **live-validated to
PLANT** at 1.240/game. Copy it verbatim from `bots/_v233evict58` with exactly one
deletion.

**A1 — `raid.py`: add the method.** Copy `bots/_v233evict58/raid.py:643-705`
(`def _try_evict_launcher`) verbatim into `bots/_v243launchmax/raid.py`
immediately above `_try_forward_sentinel`, **then delete these three lines**
(`bots/_v233evict58/raid.py:653-655`):

```
  DELETE
        live = self._live_fwd_guns(ct, E)
        if not live:
            return False
```

*Why this deletion and only this one:* it is the **only** gate in that function
that defers the plant until a forward **sentinel** exists. Everything else it
carries is discipline this leg wants kept — `LOKI58_ON` flag, the `self.l58_done`
per-unit latch, the **cap-1** live census over `LOKI58_CENSUS_DSQ`, the
`get_launcher_cost() + LOKI58_TI_FLOOR` bank floor, the `d²≤18` approach
precondition, the `LOKI58_NEAR_DSQ` site filter and the heal-seat-coverage site
score. **Cap 1 is deliberately kept — see T2 above.**

**A2 — `raid.py`: add the call site.** Copy `bots/_v233evict58/raid.py:285-292`
into `_raid_act`, i.e. immediately after the `_try_forward_sentinel` block
(control `bots/_v223sealrepair/raid.py:280-282`, the block commented
`# 3. THE FORWARD SENTINEL.`) and immediately before `# 4. BUDDY HEAL`:

```
  NEW (between step 3 and step 4 of _raid_act)
        # 3b. LAUNCHMAX (T3): the FORWARD launcher, ported from #58 minus its
        # siege prerequisite. Siting is the occurrence lever: an enemy builder
        # reached d^2<=2 of OUR core in 1 of 17 launcher-games; a raider stands
        # inside the enemy ring in essentially every game we raid.
        if self._try_evict_launcher(ct, E):
            return True
```

**A3 — `doctrine.py`: add the four constants.** Copy
`bots/_v233evict58/doctrine.py:1699-1702` verbatim to the end of
`bots/_v243launchmax/doctrine.py`:

```
  NEW
LOKI58_ON = True
LOKI58_TI_FLOOR = 40
LOKI58_NEAR_DSQ = 8
LOKI58_CENSUS_DSQ = 32
```

### CHANGE B (T4, aim) — the destination sort becomes a **PIN**, not a disposal

**`bots/_v223sealrepair/raid.py:925`, one line, inside `_launcher_turn`'s EXILE
branch.** `lp` (the launcher's own position) is already in scope at `raid.py:895`.

```
  OLD (raid.py:925)
            far = sorted(sites, key=lambda t: t.distance_squared(self.core), reverse=True)

  NEW
            far = sorted(sites, key=lambda t: (0 if t.distance_squared(lp) == 2 else 1,
                                               t.distance_squared(lp),
                                               -t.distance_squared(self.core)))
```

**⭐ WHY THIS IS THE DENIAL-MAXIMAL AIM, read off the engine's own numbers.**
Pickup is **d² ≤ 2** and a legal throw is **1 ≤ d² ≤ 26 from the launcher** — so
**a destination at d² ≤ 2 leaves the victim INSIDE the pickup envelope, and the
loop is a fixed point.** Cooldown `+= 1` decrements at end of round, so the
launcher can throw **every round**. The old `far` sort threw the victim ~5 tiles
out and it walked back over ~4-6 rounds; **the new sort re-grabs it next round.**

**⭐⭐ AND THE PRIMARY KEY IS `d² == 2`, NOT `d² == 1`, ON PURPOSE.** A builder
bot's attack requires an **orthogonally** adjacent tile — *"not diagonal"*
(`CLAUDE.md`, builder-bot actions). **d² = 2 is exactly the four diagonals: in
the pickup ring, out of attack range of the launcher it is pinned against.** d²=1
(orthogonal) is the fallback, then everything else ascending, with the incumbent's
farthest-from-our-core preference kept as the final tiebreak so behaviour is
unchanged wherever no near tile is legal.

⚠ **Three honest caveats, pre-stated:**
1. `sites` includes the launcher's own tile (`dx=dy=0`); it now sorts near the
   front and is refused by `can_launch`. One wasted predicate call per throw.
2. **A pinned victim is positionally denied, not action-denied** — it still gets
   its turn and can build or attack from wherever it lands. What it can never do
   is **arrive** anywhere. Claims on this page are about displacement, never
   about inerting a unit.
3. **The pin is only as tight as our launcher's ability to act each round**; if
   a throw is skipped the victim can step orthogonal and attack (launcher HP 30,
   builder attack 2 dmg ⇒ ~15 uninterrupted turns to kill it).

⛔ **CHANGE B APPLIES TO THE HOME LAUNCHER TOO — DECLARED, NOT DISCOVERED.**
`_launcher_turn` is shared, so in the 8.2% of games where v140 has a home
launcher we now **pin an intruder beside our own base instead of expelling it**.
That is a defensive behaviour change and it is why §10's kill-round rider binds.
**Pre-registered fallback if the rider fails: gate the pin on the launcher being
forward** (`lp.distance_squared(dest) < lp.distance_squared(self.core)`, the same
`fwd58` predicate `bots/_v233evict58/raid.py` already uses) — a follow-on arm,
never a re-read of these rows.

### NAMED NON-CHANGES (so a reviewer can check the diff against a list)

`LAUNCHER_MIN_RND` (160) · `SLOT_LAUNCHER` latch · `LAUNCHER_RESERVE` (80,
`doctrine.py:965`) · `LOKI_FERRY_ON`/`LOKI_FERRY_STALE_RNDS`
(`doctrine.py:1275-1276`) · the whole ferry branch (`raid.py:934-950`) ·
`main.py` · `eco.py`. **All byte-identical to the control.**

### CPU RIDER (hot-turn budget)

Change A adds a per-raider-per-turn scan, early-exited at `d²>18` from an enemy
core tile and after `_cpu_exhausted` (`eco.py:206`); Change B adds a 3-tuple sort
key over ≤81 sites on **launcher** turns only. Budget **10,000 µs/unit/turn**,
worst observed **8,748 µs** on 900-area maps. **`get_cpu_time_elapsed()` reads
ZERO locally**, so `_cpu_exhausted` cannot fire in this fixture and offers no
protection here. ⇒ **A `--tle 10` smoke run of ≥10 games on `midgard` and
`ragnarok` (900-area), zero tracebacks, is a build gate before the shard is
appended.** `tools/overnight.sh:127-136` enforces `--tle 10` for the shard itself.

---

## 3. REGISTRATION BLOCK

**TARGET BAND: N/A — LOCAL corefill screen with ZERO live rated exposure; no submit, no activation, no prototype on the ladder, so `tools/target_value.py`'s reachable-band question does not bind. This leg cannot pay or cost a single rating point.**
**PINNED: N/A — local screen against a byte-frozen local tree (`bots/_v223sealrepair`). Opponent churn cannot reach this shard; the pin/never-pin design rule governs PLATFORM legs only.**
**SURFACE: local**
**CLUSTER UNIT: none — enumeration performed in writing in §5; both clusters die, applicable DEFF = 0.98 (local, measured)**
**ESTIMATOR: pooled game share = treatment wins / (rows − NOWINNER rows), unweighted, over `scratchpad/overnight/LAUNCHMAX.tsv` rows only. No map weighting, no seat weighting, no pooling with any other shard.**
**DOSE: forward launchers PLANTED per game — 1.240 (measured LIVE, EVICT58's pinned leg against team 0033, the same `_try_evict_launcher` code Change A ports) vs 0.341 (v140 control, same leg, same instrument) — n = 25 live games per arm; the coverage that converts to is 8.2% of games for v140 (7 of 85 archived) against ~100% for this treatment, whose plant rate is bounded BELOW by 1.240 because Change A only DELETES a gate**
**PLANNED n: 5400 games**
**BOUNDARY: 5400 shard rows = 5400 games (LOCAL fixture: one row is one game; the platform `games = 5 × accepts` identity has no accepts to close on here — declared exemption in §11)**
**CUT-SHORT: below n=1000 games this shard publishes descriptive tallies only and takes NO comparative look; a futility drop at either gate publishes the label, the n and the share and makes NO claim about the mechanism beyond "not worth more cores now"**
**BAR: 53.32**
**BASE RATE: 50.0**
**BAR SOURCE: constructed, not observed — `50.00 + MDE(2.00pp) + half_width(1.32pp)`. Half-width recomputed in §6 as ±1.3195pp from `1.96·sqrt(p̄(1−p̄)·0.98/5400)` at p̄ = 0.5166. Clearing it means the 95% interval excludes BOTH 50.00 AND the indifference threshold below it — the point of putting the MDE inside the bar rather than beside it.**
**BASE RATE SOURCE: structural null of a paired local screen — `tools/overnight.sh:129-136` plays every (seed, map) in BOTH seat orders (`ORD` A and B), so under H0 the expected treatment share is exactly 50.0. No historical population is consumed by the bar. ⚠ Disclosed: the nearest null cell on any chassis, `NULL125` (`bots/_v198null125` vs `_v197mapcode`), read 51.04 ±1.32 at n=5,400 on this same 15-map pool — its interval contains 50, so 50.00 stands, but there is no null cell on the v140 chassis itself and a marginally-clearing KEEP is the reading most exposed to that residual.**
**REFERENCE n: none — every historical launcher final in §1/§7 is an era-labelled DIRECTION PRIOR and a THRESHOLD SOURCE, and is a comparator in no bar on this page. No fixed reference contributes a variance floor.**
**POOL ERA: post-2026-08-13-rotation (spelled `POOL_ERA: post-2026-08-13-rotation`). The local 15-map pool `tools/overnight.sh:66` — antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune — post-patch geometry (valkyrie and glacierkeep rewritten 2026-08-14; the other 13 unchanged since 08-06). Every historical launcher final quoted on this page (LAUNCH0/BOTH0/LAUNCH2/LAUNCH3/FERRY0/EXILE0/LATE160/LATE80/RES0/RES20) was measured on the PRE-rotation 8-map pool and the v114 chassis — era-labelled, which is one more reason each is a prior and not a comparator. The rated-tape boundary 2026-08-13T07:12:59Z bounds no number here, because no number here comes from the rated tape.**
**SPANS-POOL-CHANGE: no — all 5400 rows are generated inside one continuous local pool era by one runner invocation against two byte-frozen trees.**
**TREATMENT TREE: bots/_v243launchmax**
**TREATMENT DIFF REFS: none — the arm tree does not exist at lock, which is the correct order and is what a clean `git diff` looks like from the checker's side (§11).**
**MECHANISM METRIC READS: raid.py:929 (`ct.launch(bp, site)`, the EXILE branch of `_launcher_turn`) — the single line at which the mechanism this leg maximises actually occurs, and the line whose destination is chosen by the sort at raid.py:925 that Change B rewrites. TREATMENT DIFF TOUCHES: raid.py, doctrine.py. INTERSECTION: YES — the metric's read site is inside `raid.py`, which Change A and Change B both modify (§7).**
**METRIC WINDOW: r0-r1000 — every round of every dose-probe game; throws are counted from the decoded replay with no round filter of any kind.**
**GATING CONSTANTS: NONE ON THE TREATMENT PATH. `_try_evict_launcher` carries no round gate at all; its four constants are a Ti floor (40), two squared-distance filters (8 and 32) and a boolean, none of which is a round. The incumbent's only round gate, `LAUNCHER_MIN_RND` (value 160), governs the HOME path at `main.py:613`, which this arm leaves byte-identical and does not read. Verified at draft: `bots/_v223sealrepair/raid.py` contains ZERO identifiers matching the round-gate pattern.**
**MECHANISM CAN OCCUR IN WINDOW: yes**
**GATE RESOLUTION: §6 — the occurrence gate G1 is a 90%-vs-20% contrast at n=60 per arm, where the 95% half-width on 90% is ±7.6pp (CI 82.4–97.6), so the branches are separated by ~8 half-widths and the gate resolves by construction. UNRESOLVED defaults to the RESTRICTION: if G1 cannot be read, the shard is NOT appended and no share is spent.**
**PRE-STATE: the predicted-change set is NOT already in the target state at lock. Verified at draft against `bots/_v223sealrepair`: (a) no `_try_evict_launcher` and no forward launcher call site exists anywhere in the tree — the only `build_launcher` call is `main.py:658`, reached only from `_defend`; (b) `raid.py:925` sorts destinations farthest-from-our-core, the opposite of the pin; (c) `LOKI58_*` constants are absent from `doctrine.py`. No cell here is pre-satisfied, and the combination (forward siting + pin aim) has never been built in any tree in `bots/`.**
**MAP SEGMENT (primary): the 10 ≤676-area maps — antler, archipelago, auroraveil, drumlin, fjordgate, frostgate, icefloe, nordkap, royale, yulerune — versus the 5 900-area maps (drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie). MECHANISM: the pin requires our forward launcher and an enemy builder to co-occupy a d²≤2 envelope near their core, and the launcher cannot be planted until a raider is within d²≤18 of an enemy core tile. Approach length is the terrain property; on 900-area maps the raider arrives later, so fewer denial rounds land inside the r250 window that scores, and the enemy's own feeder traffic is spread over a larger ring. EVICT58's dose already saw the size effect from the other side (midgard: built in 4 of 8 games but converted in only 1 of 4).**
**EXPECTED DIRECTION: POSITIVE on-segment, WEAKER off-segment — treatment share HIGHER on the 10 ≤676-area maps than on the 5 900-area maps.**
**SEGMENT VALUE CEILING: 66.7% x 3.0pp on-segment = 2.00pp pooled**

### Proxy dilution, declared against this document

The mechanism names **rounds-to-first-forward-plant**, and no per-map
core-to-enemy-ring distance table exists in the repo at draft. **Map area is a
declared PROXY, and a proxy dilutes** — the segment will read weaker than the
true mechanism-specific split. The cheap research item this names: a per-map
core-to-enemy-ring distance table, after which this segment should be re-declared
on the real property.

**EXACTLY ONE PRIMARY SEGMENT (15b).** Every other cut on this shard — per-map,
per-seat (`ORD` A vs B), win-condition mix, the patched-vs-unpatched map pair —
is **DESCRIPTIVE ONLY** and may not be used to rescue a pooled fail. Named here
so none can be promoted later. **15c applies:** a pooled fail that clears the
pre-declared primary segment in the predicted direction buys a **NEW screen with
its own n**; the rows that suggested the segment may never confirm it.

---

## 4. ⛔ THE SELF-PLAY BIAS — direction, magnitude, and what it does to each branch

**This is the single most important caveat on the page and it is not a hedge; it
is a measured fact that changes what each branch may claim.**

In a self-play fixture the victims are **our own builders behaving as our code
does** — and **our code sends raiders into the enemy ring**, which is precisely
the envelope a forward launcher covers. Against a **back-sitting** opponent it
does not: `QUEUE.md:145` records EVICT58's pinned live leg vs `0033` —
**launchers PLANTED 1.240/game (3.6× v140's 0.341) but EVICTIONS 0.04/game
against a pre-registered >1.0 bar, a 25× miss** — *"the PLANT fired and the THROW
did not… the binding constraint is PICKUP OPPORTUNITY, not planting… THE FAILURE
IS OPPONENT-SHAPED."*

⇒ **DIRECTION AND MAGNITUDE, STATED: this fixture OVERSTATES pickup opportunity,
and the overstatement has been measured at up to ~25× against one real
opponent.** Therefore:

* **This is the MOST FAVOURABLE fixture the mechanism will ever see.** That makes
  the **NEGATIVE branch a strong closure** — a mechanism that cannot pay where
  victims are maximally available cannot pay where they are scarcer.
* It makes the **POSITIVE branch BOUNDED**. ⛔ **A KEEP HERE LICENSES NO LIVE LEG.**
  `QUEUE.md:134` (row #47) already forbids one without *"A NAMED DESIGN CHANGE AND
  AN ARGUMENT FOR WHY IT SURVIVES WHERE `MC` DID NOT"*, and #58 died on exactly
  the quantity this fixture inflates. **The KEEP branch buys local decomposition
  screens and an opponent-shape study, and nothing else** (§8).

---

## 5. CLUSTER ENUMERATION (CLAUDE.md scope procedure, performed in writing)

1. **MATCH cluster — DIES.** A local shard has no 5-game match wrapper. Each row
   is an independently seeded single game (`tools/overnight.sh:121,129-136`,
   one game per (seed, map, ORD) triple). No stratum can hold two games from one
   match because no match object exists.
2. **OPPONENT cluster — DEGENERATE.** Exactly one opponent
   (`bots/_v223sealrepair`) for all 5400 rows; no between-opponent contrast is
   drawn, so there is no multi-member opponent stratum to inflate.

⇒ **Applicable DEFF = 0.98** (local pair-weighted, ρ = −0.020, 124 shards, s39
audit). **The platform constants 1.529 / 1.833 are NOT imported** — doing so
would widen these intervals 24–35% for correlation that is not present.

⚠ **Where this could bite:** the s39 audit found local outlier arms with strong
map interaction at DEFF ≈ 1.20–1.25, and this arm declares a map segment. **The
segment split is therefore INDICATIVE; a segment claim is banked only via the
15c re-screen, never off these rows.**

---

## 6. ⭐ THE PRE-SPECIFIED MDE (OBLIGATION 16), AND THE OCCURRENCE GATE

### 6a. The MDE — sized off a value we must EXCLUDE, never off one we hope to observe

**MDE: +2.00pp. WE WILL CALL THIS ARM A MISS IF ITS TRUE LOCAL EFFECT IS AT OR
BELOW +2.00pp OF GAME SHARE.**

**There is no observed point estimate to size off, and that is deliberate** — the
treatment tree does not exist and no probe has run, so nothing in this document
can be circular. The indifference threshold comes from the arm's **PRICE**, which
is knowable before any row:

> **The arm adds ~0.92 standing launchers per game over the control** (~100%
> coverage against v140's 8.2%). **A standing launcher is priced at −6.34pp on
> this fixture family, mechanism-matched** (LAUNCH0 52.77 − BOTH0 46.43, n=5,408
> each). **A net effect at or below +2.00pp therefore means maximised denial
> bought back a launcher's premium and roughly two points more — which is inside
> the noise of the very decomposition the KEEP branch exists to fund.** Each of
> the two sub-planks (siting, aim) would then be worth a fraction of that, i.e.
> below every resolution this fixture has, and there would be nothing to
> decompose. **At or below two points, the ceiling is not worth a follow-on.**

**The sizing then follows mechanically rather than being negotiated:**

| quantity | value at n = 5,400, DEFF 0.98 |
|---|---|
| σ (game share, at p̄ = 0.5166) | **0.6732pp** |
| **95% half-width** | **±1.3195pp** *(quoted ±1.32pp)* |
| smallest excluded effect at the bar | **2.00pp** |
| effect detected with 80% power (Z = 2.8016) | **≥ 1.886pp** |
| n needed to EXCLUDE 2.00pp (half-width < 2.00) | **2,351** |
| n needed to DETECT 2.00pp at 80% power | **4,808** ⇒ 4,830 is the next balanced multiple of 30 |

**⇒ WHY 5,400 AND NOT 2,700 OR 10,800.** 2,700 would EXCLUDE the threshold
(±1.87pp) but detect only ≥2.67pp at 80% power — it could fail to see the very
effect it registered. **4,830 is the true minimum that both excludes and detects
2.00pp; 5,400 is the standing corefill shard size, adds 570 games of headroom,
and pools and compares cleanly with every other row on the board.** 10,800 buys
an MDE of 1.33pp, which this leg does not need: **a ceiling probe is asking
whether the effect is LARGE, and spending four extra worker-hours to resolve the
sub-two-point question is buying precision the question does not have.**

**⇒ WHAT THIS LEG CAN AND CANNOT DO.** It can separate *"maximised denial is
worth more than two points"* from *"two points or less"*. It **cannot**
distinguish *"worth 1.2pp"* from *"worth nothing"* — that needs ~19,000 games and
is not what is being bought.

### 6b. ⭐ THE OCCURRENCE GATE — a PRE-FIRE gate, and it is the answer to the commission

**No share row may be spent until the ceiling is shown to exist.** This is the
direct, measured answer to *"we can't build a version where it happens more than
1.5% of games"*, and it is read **before** the shard is appended.

**INSTRUMENT.** `tools/mech_battery.py` is the only local runner in this repo
that KEEPS its replays (`tools/mech_battery.py:100-106` writes a unique
`--replay <outdir>/replays/{arm}__{opp}__{map}__{seed}__{seat}.replay26` per
game; `overnight.sh:135-136` uses `--replay /dev/null` and has **no flag to
override it**, so the screen shard itself cannot produce this metric — declared,
not discovered).

```
.venv/bin/python tools/mech_battery.py \
    --variant bots/_v243launchmax --control bots/_v223sealrepair \
    --opponents bots/_v223sealrepair \
    --maps antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate \
           glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune \
    --seeds 2 --tle 10 --keep-replays -o scratchpad/launchmax_dose
.venv/bin/python tools/corpus/replay_throws.py scratchpad/launchmax_dose/replays/*.replay26
```

⇒ 15 maps × 2 seeds × 2 seats × 2 arms = **120 games, 60 per arm.**

**THE CUT.** `replay_throws.py` emits 24 columns
(`file mw mh rounds rnd kind tteam bteam amb d2_before d2_after bot life core_atk
any_atk reached to_x to_y border winner wincond vfate vlife vhp`). A throw is
**OURS AND AN EXILE** iff `kind == "EXILE"` **and** `tteam` is the arm's own team,
which the replay filename fixes: `seat == "a"` ⇒ the arm is team A, `seat == "b"`
⇒ team B (`tools/mech_battery.py:103`). **`kind` is defined at
`tools/corpus/replay_throws.py:216-218` as `"EXILE" if tteam != bteam`,
i.e. a launcher throwing the OTHER team's builder — the kidnap population.**

⛔ **FILE-SET BOUNDARY, DECLARED.** This probe decodes **its own replays only**
and **does NOT read `corpus/throws.tsv`.** That table is at **21 columns** (built
2026-08-15T04:19:47Z, before commit `6fa1d859` added `vfate/vlife/vhp`) and
carries none of the victim-outcome columns this cut uses. **No archive re-decode
is requested or required by this leg.** *(Separately and urgently, flagged for the
lane and not acted on here: the corpus keeper's incremental append will raise on
the 21-vs-24 header drift, so every corpus table is stalled until a forced
rebuild. That is a live instrument incident, not an input to this prereg.)*

**THE THREE GATE BARS, pre-committed:**

| id | metric | treatment bar | control bar |
|---|---|---|---|
| **G1 — THE CEILING** | share of games with ≥1 **our-EXILE** row | **≥ 90% of 60** | **≤ 20% of 60** |
| **G2 — THE PIN** | median `vlife` over our-EXILE rows with `vfate == "RETHROWN"` | **≤ 2 rounds** | ≥ 3 rounds |
| **G3 — VOLUME** *(descriptive)* | our-EXILE throws per game; distinct `bot` ids with ≥3 our-EXILE throws | reported, no bar | reported, no bar |

*G1 is the commission's own question in one number.* The control's expected value
is **~0.5%** (8.2% launcher coverage × 1-in-17 home pickup opportunity); the
**≤20%** bar is set far above that so the control cell is a real check rather
than a formality. *G2 discriminates the pin from the incumbent's disposal throw*:
the corpus's largest observed loop ran at a **~3.7-round cadence** (259 throws,
r47–998, game `483b5bcd…_game_1`) under the far-sort; **the pin predicts ~1.**

**⛔ IF G1 FAILS, THE LEG IS VOID AS A CEILING PROBE.** The shard is not
appended, no share is spent, and the honest report is *"we could not build a
version where it happens"* — which is itself a complete and publishable answer to
the commission. **If G1 passes and G2 fails**, the shard MAY still be fired but
every verdict sentence must read *"forward siting at ceiling coverage"* and may
**not** claim the pin, because the pin was not shown to fire.

---

## 7. HOW THIS DIFFERS FROM `_v207apprlaunch` (#47) AND `_v233evict58` (#58)

**Both are CLOSED on LIVE evidence and both are named here rather than
rediscovered.**

**`_v207apprlaunch` / QUEUE #47 — CLOSED 2026-08-14T08:07:23Z, `QUEUE.md:134`.**
Its entire treatment was **WHEN a launcher may be built**: waive
`LAUNCHER_MIN_RND` (160) and zero `LAUNCHER_RESERVE` (80) when an enemy builder
is seen within d²≤50 of **OUR** core; cap 1; **siting and aiming UNCHANGED
(home-only, far-sort)**. It screened **52.67 pooled at n=10,800** and then read
**MC 8/20 vs MA 9/20 = net −1 against a pre-committed +4 bar.**

> **HOW THIS DIFFERS: #47 changed the TRIGGER and left SITING and AIM alone.
> This leg leaves the trigger alone (T1 NOT lifted, `LAUNCHER_MIN_RND` stays
> 160) and changes SITING and AIM — the two throttles #47 never touched.** They
> are disjoint diffs on disjoint lines: #47's hunk is in `main.py:593-676`, which
> this arm holds **byte-identical**. **And this leg does not inherit #47's
> permission: it spends no live games and asks for none** (§4).

**`_v233evict58` / QUEUE #58 — REFUTED AS DESIGNED, live, s40 2026-08-14 17:04Z,
`QUEUE.md:145`.** ⛔ **IT IS THE ONE FORWARD-SITED LAUNCHER EVER BUILT IN THIS
REPO, AND CHANGE A IS ITS CODE.** Saying otherwise would be false: the
commission's *"a forward launcher has NO call site today — it is new code in
`raid.py`"* is true of the **incumbent** and false of the **repo**.

> **HOW THIS DIFFERS: #58 planted the forward launcher and then threw with the
> INCUMBENT'S AIM.** Its own closure names the surviving question exactly — *"the
> PLANT fired and the THROW did not… the binding constraint is PICKUP
> OPPORTUNITY, not planting… THE EVICTION MECHANISM ITSELF IS UNTOUCHED… THE
> FAILURE IS OPPONENT-SHAPED."* **This leg (a) removes #58's siege prerequisite,
> (b) adds the pin aim #58 never had, and (c) measures in the fixture where
> pickup opportunity is maximal instead of the one where it was measured absent.**
> **⚠ AND (c) IS A WEAKNESS, NOT A DEFENCE — §4 prices it and bars the live claim.**

**`AIMTHROW` / QUEUE #51 — the adjacent aiming row.** #51 aims the throw so the
victim **DIES** (onto a friendly sentinel's ray, plus an ammo floor); Change B
aims so the victim **STAYS DENIED** (back into the pickup envelope, on a tile it
cannot attack from). Different objective, different sort key, and **#51's
`AIMTHROW2` read 50.09 — exactly what the 8.2%-coverage dilution arithmetic
predicts for any aiming change made while the launcher does not exist.** That
prediction is the strongest single argument for this leg's ORDER: **make it
exist, then aim it.**

**#9 (exile-first grab priority) and #10 (body-block a gunner lane)** are
different mechanisms on different call paths and are untouched here.

---

## 8. THE DECISION RULE (⚖ builder ratifies the branch labels)

**Fixture.** `tools/corefill.sh` → `tools/overnight.sh`, full 15-map post-patch
pool, `--tle 10` wall-clock enforced, `--replay /dev/null`, both seat orders per
seed, one game per row.

**FUTILITY GATES** (`docs/prereg/RULE-futility-gates-2026-08-13.md`, read ONCE
each at first crossing; the builder types the decision, the watcher never
decides). ⚠ **Both are set below 50, deliberately: this arm PAYS a launcher
premium by construction and a gate at the usual 48.0/50.5 would kill it before
the denial it is measuring could show.**

* **GATE-1000 (n ≥ 1000): drop if share < 46.0% — i.e. ≤ 459 of 1000.** Label
  `FUTILITY-EARLY`. 46.0 is below **BOTH0 46.43**, the measured "pay for a
  launcher and use it for nothing" floor: a reading there means the arm is worse
  than owning a launcher and never throwing, and there is nothing to recover.
  A true 53.32% arm reads below 46.0 at n=1000 with probability < 1e-6.
* **GATE-2700 (n ≥ 2700): drop if share ≤ 50.0% — i.e. ≤ 1350 of 2700.** Label
  `FUTILITY-ALONE`. At n=2700 (σ = 0.9526pp) a true 53.32% arm reads ≤ 50.0 with
  probability ≈ 0.00025.

**⚖ THREE BRANCHES, pre-committed. All three assume G1 PASSED; if it did not,
none of them is reachable (§6b).**

| final at n = 5400 | in games | branch |
|---|---|---|
| **≥ 53.32%** | **≥ 2880** | **KEEP — THE CEILING PAYS.** Maximised denial more than covers a standing forward launcher. **This buys screens, never a ship.** Mandatory next steps, in order: (1) **D26 replication** at seed 341000, scored alone; (2) **`AIMPIN`** — Change B alone on the v140 chassis, which isolates the price-free half; (3) **`LAUNCHMAX2`** — forward cap 2, the T2 bet deferred in §1; (4) an **opponent-shape study** against the archived field before any live leg is proposed. ⛔ `SHIP_SIT` governs and no branch here activates anything. |
| **48.68% – 53.32%** | 2629 – 2879 | **DROP — NO INFORMATION AT THIS RESOLUTION.** Per the pre-committed default, **UNRESOLVED defaults to the RESTRICTION**: nothing is promoted, nothing ships, the arm is not decomposed. Written as *"the screen could not separate maximised denial from the incumbent at ±1.32pp"* — **never** as *"denial is worthless"* and **never** as *"the incumbent measured better"*. |
| **≤ 48.68%** | **≤ 2628** | **REAL NEGATIVE — THE DENIAL ROAD CLOSES.** At its occurrence ceiling, in the **most favourable fixture the mechanism will ever see** (§4), maximised denial is measurably WORSE than v140's rare launcher. Because every live fixture has strictly LESS pickup opportunity — measured at 25× less against one real opponent — **no live leg can rescue it, and none may be proposed.** #51/#9/#10's aiming family is closed with it: aiming a mechanism that does not pay at 100% coverage cannot pay at 8.2%. |

⚠ **The negative branch is intentionally NOT symmetric with the positive one**
(1.32pp below 50 against 3.32pp above): a credible harm kills an arm that also
adds +10% global scale in ~92% more games and adds work to the hot path, so **no
indifference margin is granted on the downside.** Stated here rather than
discovered in the analysis.

**D26:** any final with |share − 50| ≥ 2.0pp (≤ 2592 or ≥ 2808 games) replicates
at seed 341000 before anything is claimed.

**⚖ THE SINGLE SENTENCE THE BUILDER RATIFIES:** *only a final at or above 53.32%,
with G1 passed, keeps this arm alive — and even then it buys local screens and an
opponent-shape study, never a live leg and never a ship.*

---

## 9. ⛔ WHAT THIS SCREEN MAY NOT CONCLUDE

* **⛔ NO ECONOMY CLAIM, IN EITHER DIRECTION.** The arms are **NON-EXCHANGEABLE
  ON ECONOMY by construction**: the treatment plants ~0.92 more standing
  launchers per game and each adds **+10% to the ONE GLOBAL ADDITIVE scale
  factor**, inflating every subsequent build of every type. **Nothing on this
  page may be read as a measurement of harvester throughput, build-out size,
  scale trajectory or `titanium_collected`**, and a share result may not be
  attributed to economy OR to denial without the kept-replay evidence of §6b.
* **⛔ NO SHIP IMPLICATION.** `SHIP_SIT` governs; v140 is sitting.
* **⛔ NO LIVE-LEG PERMISSION.** §4 and §7. `QUEUE.md:134` binds.
* **⛔ NO CLAIM ABOUT T1 OR T2.** The round gate and the count latch are
  untouched (`LAUNCHER_MIN_RND` stays 160, the latch stays cap-1) and this shard
  says nothing about either. Their historical finals are priors here, not
  results.
* **⛔ NO CRASH CLAIM.** This leg is built for **DENIAL, not the crash.** The
  border-crash signature is real and **the field is immune to it**: all six
  crash-signature kills belong to one arm against the four teams it was aimed at;
  drop that arm and it is **0 of 274 corner landings across 31 opponents, 0 of
  2,027 border landings, 0 of 930 on the rated ladder.** No bar on this page
  reads `vfate == "DIED"`, and `vhp` is reported only as a descriptive column.
* **⛔ NO CLAIM THAT A PINNED UNIT IS INERT** — only that it is displaced (§2,
  caveat 2).

---

## 10. THE KILL-ROUND RIDER (defence bar, scored as an EXCLUSION)

`PROGRAMME.md` `DEFENCE_ADMISSION_BAR: kill_round_non_regression` binds twice
here: Change B alters home-launcher behaviour (pin instead of expel, §2), and
Change A spends a raider action and 20 Ti at the enemy ring that would otherwise
have sealed or pecked. **`R1000_IS_DEFEAT` is unconditional and `KILL_WINDOW_RND`
is 250; our median kill is r174.**

**⚖ THE RIDER, in both units:** the arm passes iff the 95% CI on **Δ median kill
round (treatment − control)** **EXCLUDES +10 rounds** — +10 ≈ +5.7% of our
174-round median (us-only).

**⛔ RESTATED AS AN EXCLUSION BEFORE ANY DEFF IS APPLIED**, per CLAUDE.md's
direction clause. *"No significant rise in kill round"* is a fail-to-exclude
claim, and widening an interval makes that class EASIER; DEFF applied to the
unrestated form would launder a weak null into a confident one. The bar above is
the exclusion form and the applicable DEFF is 0.98 (§5).

**UNRESOLVED ⇒ RESTRICTION:** if the CI cannot exclude +10, the rider does not
pass and a clearing share does **not** promote the arm on its own.

**⛔ THE CONDITIONING TRAP, named before the read.** `tools/overnight_read.py`
prints **median kill round GIVEN a kill**. A change in *which* games end in a
kill moves that median without anything getting faster or slower. ⇒ **The rider
is reported as a pair — P(core-kill win) AND median-kill-round-given-a-kill, both
arms, with both kill counts — or it is not reported.** This arm is expected to
move the kill/tiebreak mix (a pinned enemy builder is a builder that does not
finish its own economy), so the trap is live, not hypothetical.

---

## FALSIFIER

**The hypothesis — *"the launcher's denial mechanism has been throttled by our
own configuration, and at its occurrence ceiling it pays"* — is falsified by any
of:**

1. **G1 FAILS (treatment mechanism-occurring games < 90% of 60).** The ceiling
   could not be built. **This falsifies the leg's premise, not the idea**, and
   the honest report is that the maximum-occurrence version does not exist —
   which is the commission's question answered in the negative at the build step.
2. **A final ≤ 48.68% (≤ 2628 of 5400) with G1 passed.** Maximised denial is
   worse than v140's rare launcher **in the fixture most favourable to it**. The
   denial road closes and the aiming family (#51/#9/#10) closes with it.
3. **A final inside 48.68–53.32% with G1 passed.** The ceiling does not clear the
   registered 2.00pp indifference threshold; by the UNRESOLVED default nothing is
   promoted. *(This is the modal outcome and is pre-typed as a drop, not as a
   null to be argued with.)*
4. **A futility drop at either gate** (≤ 459/1000 or ≤ 1350/2700).
5. **The kill-round rider failing** (§10) — the arm is off-programme whatever it
   does to share.
6. **G2 failing while G1 passes** — falsifies the PIN specifically. Change B did
   not produce a re-entrant loop, every verdict must be attributed to siting
   alone, and `AIMPIN` is not bought.

**The PRIMARY SEGMENT prediction is falsified** if the treatment's share on the
10 ≤676-area maps is **≤** its share on the 5 900-area maps. *(A reversal — the
mechanism paying MORE where the approach is longest — would be a genuine surprise
and, per 15c, buys its own screen with its own n; it does not rescue a pooled
fail on these rows.)*

---

## 11. WORKLIST ROW, COLLISION CHECK, AND THE OBLIGATIONS REGISTER

**Worklist row, to be appended by the LANE (not by the drafting agent):**

```
LAUNCHMAX   bots/_v243launchmax    bots/_v223sealrepair   5400  340000
```

**COLLISION CHECK, BOTH DIRECTIONS, run at draft:**

* **Basenames** (`tools/corefill.sh:96-100` and `tools/overnight.sh:70-74` refuse
  a pair where either basename is a SUBSTRING of the other, because scoring is
  `case "$L" in *"$B"*`):
  * `_v243launchmax` contains `_v223sealrepair`? **NO.**
  * `_v223sealrepair` contains `_v243launchmax`? **NO.**
  * Equal? **NO.** ⇒ the refusal does not trigger.
* **Tree name free:** `ls bots/ | grep -c "_v243\|launchmax"` → **0**.
* **Shard key, both directions,** over every shard id in
  `scratchpad/corefill_work.txt` (134 rows) and every file in
  `scratchpad/overnight/`: no existing id contains `LAUNCHMAX`, and `LAUNCHMAX`
  contains no existing id — the nearest neighbours are `LAUNCH0`, `LAUNCH2`,
  `LAUNCH3`, `LAUNCHLATE80`, `LAUNCHLATE160`, `LAUNCHRES0`, `LAUNCHRES20`,
  `APPRLAUNCH`, `APPRLAUNCH2`, and **none of them is a substring of `LAUNCHMAX`**
  (there is no shard named bare `LAUNCH`).
  **⛔ READ HYGIENE: the shard key is `LAUNCHMAX` EXACTLY. A `grep LAUNCH` pools
  nine other launcher shards from the v114 chassis — a different contrast
  entirely. Any read that cannot show it matched the exact key is not a read of
  this shard.**
* **Seed base:** 340000, consuming **340000–340337** (`overnight.sh:121`,
  `seed = SEEDLO + n/16` at n = 5400). Nearest occupied base is **336000**
  (`BODYAWR`, 10800 games ⇒ 336000–336675) — **a 3,325-seed gap.** Every other
  base in the worklist is ≤ 336000. **Requirement ≥ 340000: met exactly.**

### INTERACTION vs the RUNNING `BODYAWR` SCREEN

`BODYAWR` (`bots/_v242bodyaware` vs `bots/_v223sealrepair`, 10800 games, seed
336000, `docs/prereg/SCREEN-bodyaware-2026-08-14.md`) is **LIVE at draft**.

* **NO CODE OVERLAP.** BODYAWR's diff is **four hunks in `eco.py:809-896`
  (`_bfs_direction`) and `eco.py` ONLY** — its own prereg requires `diff -rq` to
  name exactly one file. This arm's diff is **`raid.py` + `doctrine.py`, with
  `eco.py` byte-identical to the control.** **The two diffs are disjoint.**
  ⚠ One directional note, recorded because it is real and not acted on: BODYAWR
  makes the builder BFS treat **both teams'** bodies as passable-with-a-detour,
  and a pinned enemy builder is a body. **If BODYAWR ever ships, the pin's
  interaction with it becomes live and must be re-screened.** It is not shipped,
  the trees are independent, and neither arm is built on the other.
* **NO SEED OVERLAP** (336000–336675 vs 340000–340337) and **NO SHARD-KEY
  OVERLAP** (`BODYAWR` / `LAUNCHMAX`).
* **⚠ CORE CONTENTION IS THE ONE REAL INTERACTION.** BODYAWR is a 10,800-game
  shard; this is 5,400. `corefill.sh` gates on shard count AND 1-minute load, so
  they will interleave rather than collide, but **this leg's n was chosen partly
  to be the cheap one while the big shard runs** (§6a).
* **NO SHARED CONTROL CONFOUND OF CONSEQUENCE.** Both use `bots/_v223sealrepair`
  as the control, which is correct (`PROGRAMME.md`: every control moves with the
  ship) and creates no dependency — the two shards are never pooled, and this
  document pools with nothing.

### OBLIGATIONS REGISTER

* **Ob. 7 (PRE-STATE / outcome form):** satisfied — outcome is game share in our
  favour on this shard; §3 `PRE-STATE` verifies nothing is pre-satisfied.
* **Ob. 8 (denominator rule):** single control, single fixture, single shard;
  the denominator is 5400 rows from one worklist row, pooled with nothing.
* **Ob. 12 (gate carries its resolution statement + pre-committed default):**
  satisfied in §3 `GATE RESOLUTION` and §6b, with the explicit **UNRESOLVED ⇒
  RESTRICTION** default.
* **Ob. 13 (`file:line` + intersection):** satisfied in §3. **Honest note:** at
  lock the arm tree does not exist, so `git diff --name-only HEAD` yields no `.py`
  path (**verified at draft: zero `.py` files in the working diff**) and the
  checker renders **CANNOT-COMPUTE / WARN**, not a verified intersection. The
  intersection becomes computable — and must be re-run with `--fire` — the moment
  `bots/_v243launchmax` is committed. **Both changed files are in `raid.py` and
  `doctrine.py`, and the metric's read site `raid.py:929` is inside one of them,
  so the computed check is expected to pass by PATH, not only by import.**
* **Ob. 14 (opponent version stability):** **N/A by shape** — the control is a
  byte-frozen local tree, not a platform panel cell.
* **Ob. 15a/b/c (map dependence):** satisfied in §3 with one primary segment, a
  signed direction, a recomputable ceiling, an explicit descriptive-only list and
  a proxy-dilution declaration.
* **Ob. 16 (pre-specified MDE):** satisfied in §6a — **+2.00pp, derived from the
  arm's measured PRICE, declared before any row exists and before the treatment
  tree exists.** n is sized to both EXCLUDE and DETECT it.
* **Ob. 17 (metric window vs round gates):** satisfied in §3 — window r0–r1000,
  no round gate on the treatment path, and the one round gate in the tree
  (`LAUNCHER_MIN_RND`) verified to govern only the untouched HOME path.
* **Ob. 1–4, 6, 9–11:** Ouroboros/CAD-leg or platform-mechanism specific; they do
  not instantiate on a local single-arm screen. Stated rather than skipped.
* **⛔ NOT SATISFIED, structurally — `BOUNDARY` in accepts.**
  `tools/prereg_check.py`'s `BOUNDARY_UNITS` wants the boundary in both accepts
  and games with the platform identity `games = 5 × accepts`. **A local shard has
  no accepts**; one row is one game (which is also why the MATCH cluster dies in
  §5). The boundary is declared in the only unit it has. **Flagged as a
  local-fixture exemption the tool models explicitly, not as a waived
  obligation.**
* **⛔ INSTRUMENT FINDING, from running the checker against an earlier draft of
  this page — the SECOND recorded instance of the same defect.**
  `DOSE_BOTH_VERDICTS` splits on the FIRST `vs` in the line and takes the first
  float in each half. That draft's DOSE line read *"…1.240 (measured LIVE,
  EVICT58's pinned leg **vs 0033**…) vs 0.341…"*, so the tool split at the
  OPPONENT NAME and reported **"treatment 1.24 vs control 33.0"** — rendering
  **ok** while comparing a plant rate against an opponent's team number. **A
  guard that returns the right verdict off the wrong quantity has not checked
  anything.** The line is reworded so the parsed numbers are the actual doses
  (1.240 vs 0.341). `SCREEN-sealfloor6-2026-08-14.md` recorded the identical
  positional fragility one day earlier (it parsed a LINE NUMBER as a dose) and
  filed it for the builder; **it is still unfixed and has now fired twice, on
  two different wrong quantities.** Re-filed, not worked around.
* **⛔ DECLARED DEVIATION — `DOSE` is measured on the PORTED code, not on this
  tree.** The DOSE line in §3 carries both verdicts from EVICT58's live leg
  (1.240 vs 0.341 plants/game, same instrument, same function), because **Change
  A only DELETES a gate from that function** and so bounds this arm's plant rate
  from below. **The behavioural dose OF THIS TREE is the §6b probe, and it is a
  PRE-FIRE GATE, not a post-hoc check.** Said plainly: **the dose obligation is
  discharged by a probe this document schedules and pre-commits, not by one that
  has already run.**

## Target-value line

Local screen, zero live rated exposure ⇒ payout gate N/A (see §3 `TARGET BAND`).
