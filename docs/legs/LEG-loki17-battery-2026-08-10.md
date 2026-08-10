# LOKI-17 — LOCAL BATTERY RECORD (s28)

Prereg: `docs/prereg/PREREG-loki17-sentinel-siting-2026-08-10.md` (`03d2314`
17:27:01) + Amendment 1. **Nothing shipped, no rated exposure, no unrated games.**

## Why a LOCAL battery and not a live leg — the two facts multiplied

The side lane flagged that today's two corrections interact badly:
* a prototype leg now costs **~−8 Elo per leaked match** (measured −24.67 over 3,
  and **invisible to the poll-time tag** we would have checked with);
* **v104 is at 1641, 26 points from the rollback line**, net5 −17 against −21.

**So a single live leg could push v104 through its stop-loss on OUR testing cost,
and the rollback would then fire on a signal we contaminated rather than on
v104's merit.** That is the specific failure to avoid — not the Elo.

**It is avoidable outright here:** LOKI-17's primary is a property of *our own
placement geometry*, so it can be generated locally. **This plank needs zero
rated and zero unrated games to test its mechanism.**

## Gate — FAILED, fixed, then CLEARED with an escape flag typed on the record

1. **First run: `DO NOT MEASURE`.** Both trees carry `NOISE_ON = True`; a paired
   fixture cannot pair against a bot that reseeds. Fixed by building deterministic
   copies `bots/_det_v134loki17` and `bots/_det_v130loki13` (`NOISE_ON = False`).
2. **Second run: `DO NOT MEASURE` again** — self-play pool, 2/2 opponents our own
   prior versions.
3. **Third run: `--allow-self-play`, CLEARED.** The flag is typed deliberately and
   the gate's own words are the justification: *"This battery measures SAFETY,
   not field effect."* **That is exactly what is wanted here** — does new code in
   the raid path raise, and does the siting rate move. **It is NOT a currency
   read and no currency claim may be made from it.**

## Result

```
24 matches (3 maps x 4 seeds x 2 orderings), _det_v134loki17 vs _det_opp_v63
crashes (uncaught exceptions, each permanently kills a unit):
    _det_v134loki17: 0        _det_opp_v63: 0
win conditions: core_destroyed 24 / 24
```

**THE LOAD-BEARING RESULT IS THE FIRST LINE: 0 uncaught exceptions across 24
matches.** New code in the raid path does not raise — and an escaping exception
destroys that unit permanently, so this was the question worth asking.

**THE WIN RATE IS NOT A RESULT AND IS NOT QUOTED AS ONE.** 24/24 is against
`opp_v63`, a far older version, on a pool the gate explicitly refused until an
escape flag was typed. **Published amputation work puts self-play at ~2x field
effect with reported sign flips.** The one thing worth noting is on-programme
rather than about strength: **all 24 ended in `core_destroyed`, none at r1000.**

## ⛔ BLOCKED: THE MECHANISM IS NOT YET MEASURED, AND `arena.py` IS WHY

`tools/arena.py` **does not retain replays** — it reports win rates and discards
the games. **So this battery cannot answer the primary** (shootable-on-build), only
the safety question. **The primary remains at its Amendment 1 baseline of 50.4%
with no post-intervention figure.**

**The route, for whoever picks this up:** `tools/crash_census.py::_run_fcode(team_a,
team_b, map_path, replay_out, seed)` already generates a match **with a retained
replay**, and `tools/replay_census.parse_entity` already decodes `direction`.
Both halves exist; nothing needs building. **Generate a retained-replay battery
for `_det_v134loki17`, run the facing decode, compare against 50.4%.**

---

## MECHANISM DECODE BUILT — AND IT DOES NOT CLEAR THE GATE TONIGHT

`tools/loki17_mech.py` now drives `fcode run --replay` and decodes
shootable-on-build with `replay_census.parse_entity`. **Three blockers, and none
of them is "the plank failed".**

**1. ⚠ TEAM NUMBERING DIFFERS BY REPLAY SOURCE.** Locally-generated replays key
the map's core entries as teams **{1,2}**; platform-downloaded replays use
**{0,1}**, while `ENTITY.team` is 0/1 in both. Keying cores by team id matches
nothing locally — the tool reported *"no sentinels decoded"* on three runs while
a hand decode of the same file found three. Fixed by indexing cores by sorted
position, and the mapping was then **verified** (each team's first builder bot
spawns beside `ordered[team]`). **Any cross-source analysis that keys on team id
silently returns zero on one of the two sources.**

**2. THE TREATMENT PATH IS NOT EXERCISED BY THIS FIXTURE.** Same map, same seed:
```
_det_v130loki13: 3 sentinels, d2 = [4, 32, 16], shootable = [F, F, F]
_det_v134loki17: 3 sentinels, d2 = [4, 32, 16], shootable = [F, F, F]
```
**Byte-identical placements.** The edit lives in `raid.py::_try_forward_sentinel`;
against `opp_v63` on these maps that path either never fires or picks the same
tile. **A local battery cannot measure a change it does not trigger** — the
fixture needs opponents that produce the forward-raid state, which is the
condition the archive population had and this one does not.

**3. ⛔ AND MY METRIC IS NOT YET THE PRE-REGISTERED ONE.** I compute shootable as
**EXACT ray collinearity**; `loki9_facing.py` — the shipped tool the Amendment 1
baseline came from — uses an **ANGLE TOLERANCE** (`ALIGNED_DEG`). My local read
of 13.3% against a 50.4% baseline is therefore **two different statistics, not a
regression.** Comparing them would be the same units error this session has
caught four times already. **The baseline must be recomputed with MY predicate,
or my predicate replaced with the baseline's, before any number is quoted.**

**DECISION: no currency leg and no ship tonight.** The mechanism gate exists so
that a plank whose mechanism is unverified never reaches a currency leg. It is
unverified — for three reasons that are all about the instrument and the
fixture, none about the plank. **Firing a leg now would spend rate-limited games
measuring a change I cannot yet show is triggered.**

---

## ⭐ THE METRIC RECONCILIATION LANDED, AND IT CHANGES LOKI-17's PREMISE

The blocker was that my predicate and the baseline's are different statistics.
Resolved, on 528 sentinels across **185 real platform games** (v104, the live
bot), with the population split before any claim:

| population | n | shootable-on-build (**exact ray**) | in range |
|---|---:|---:|---:|
| ALL our sentinels | 528 | 0.8% | 73.3% |
| HOME (d² to our core ≤ 41) | 201 | 2.0% | 33.8% |
| **FORWARD (d² > 41)** | **327** | **0.0%** | **97.6%** |
| forward AND in range | 319 | **0.0%** | 100% |

**327 forward sentinels, 97.6% of them within range of the enemy core, and NOT
ONE can fire at it on the round it is built.**

### THE CONTROL, because a 0/319 is exactly the shape I have been wrong about four times today

Same predicate, same games, **opponents' forward sentinels**:

```
US (v104)               319    0.0%
The Bisons               71    0.0%
0033                     64    0.0%
Askar City               39    7.7%     <- the predicate DOES fire
Lunds Stallions          14    0.0%
ALL OPPONENTS POOLED    191    1.6%
```

**It is not a constant column — Askar reaches 7.7%. But nobody in the population
is remotely near 85%, including the exemplar the target was derived from.**

### ⇒ WHAT THIS DOES TO THE PLANK, STATED WITHOUT ACTING ON IT

**Amendment 1's baseline (50.4%) and comparator (Askar 67.6%) were computed with
`loki9_facing.py`'s `ALIGNED_DEG = 45.0` — a FULL COMPASS STEP of tolerance.**
That is a legitimate *"was it aimed roughly toward the core"* statistic. It is
**not** `can_fire_from`. Under the engine's own rule for a single-tile-wide line
shot, the same population reads **0.0% for us and 7.7% for the best opponent.**

**So the pre-registered target of >85% is not "the best real bot plus headroom".
Under the engine-exact predicate it is ~11x the best value ever observed in this
population.** The prereg's own Amendment 1 already voided the target's stated
justification once, when Askar moved 77.9% → 67.6%; **this moves the whole scale
and the two numbers are not comparable at all.**

**AND THE PREDICATE IS NOT MERELY MY OPINION:** research's facing validation
established that a gunner's `FireTurret` target lies on its facing ray in
**12,759 of 12,759** events, with one compass step of rotation taking that to
**0.0000**. Exact-ray is the validated relationship between facing and what a
turret can hit.

**NOT DECIDED TONIGHT, deliberately.** Either the primary is restated on the
engine-exact predicate — which makes it a much harder and much more interesting
claim, since almost nobody achieves it — or the prereg keeps the 45° statistic
and says so explicitly. **That is a bar decision on a leg that has not fired,
and it is exactly the kind of choice this session has repeatedly got wrong by
making it fast.** It is the first item tomorrow, with both readings on the
record and neither adopted.

---

## ⛔ RETRACTION: THE 0/319 IS MY PREDICATE, NOT A DEFECT. THE CODE IS THE POSITIVE CONTROL I NEVER RAN.

The side lane put the fork precisely: 0 shootable out of 319 admits **(a)** the
`raid.py` path builds ~none of them, or **(b)** it builds plenty and its guard is
not delivering. I claimed (a) and pre-registered LOKI-18 on it. **Settled by a
reach argument, and the answer is neither:**

`main.py:574` requires the threat within `HUNT_BAND_DSQ = 41` of **our own**
core, and the turret within sentinel range (32) of that threat. **So its
placements cannot exceed d² ≈ 145 from our own core.**

```
main.py's maximum possible d2 from our own core:   145
sentinels BEYOND that reach:                       287 / 528
  ...in range of the enemy core:                   287
  ...shootable at the enemy core (my predicate):     0
```

**Those 287 can only have come from `raid.py`** — there are exactly two
`build_sentinel` call sites — **and `raid.py` builds ONLY after
`ct.can_fire_from(bp, facing, SENTINEL, core_tile)` returns True, using that
exact facing.**

**⇒ Every one of those 287 satisfied `can_fire_from` AT BUILD TIME, by
construction. My predicate scores them 0/287. Therefore MY PREDICATE IS NOT
`can_fire_from`, and the 0.0% is an artefact of it.**

### What this retracts

* **The "0/319 forward sentinels cannot fire" finding — WITHDRAWN.** It measured
  my exact-ray rule, not the engine's.
* **LOKI-18's premise — INVALID.** Its 0.0% baseline and its "aim at the core,
  not the threat" story both rest on it. The prereg stands as a record; **the
  plank does not, and its prototype (`bots/_v135loki18`) must not be measured
  against that baseline.**
* **LOKI-17's supersession — WITHDRAWN.** It was retired for editing a
  "near-dead" path. That path is the opposite of dead: **it builds 287 of our
  528 sentinels.** LOKI-17 returns to unresolved, not retired.

### The lesson, and it is the sharpest of the session

**`raid.py`'s guard was a POSITIVE CONTROL sitting in the codebase the whole
time.** A path that builds only after `can_fire_from` passes produces a
population that is shootable **by construction** — so any predicate scoring that
population at 0% is falsified by the code, with no replay needed. **I had a
control available before I decoded a single game and did not run it**, then
built a prototype and pre-registered a plank on the uncontrolled number.

This is the same failure as the constant-column family, one level up: I checked
whether my predicate could return True *at all* (Askar 7.7%, so not a constant),
and never checked it against a population **known** to be positive. **"It can
fire" is a weaker control than "it must fire here."**

**STOP POINT. No further build tonight.** The open question for tomorrow is
narrow and well-posed: **what does `can_fire_from` actually accept for a
SENTINEL?** Read it off the engine binary, or probe it directly with
`can_fire_from` over a grid — the API is callable in a local match. Until that
is answered, no sentinel-aiming plank has a baseline.
