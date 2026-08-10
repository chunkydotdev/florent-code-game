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
