# SCREEN PREREG — #54 fix arm 1: `_v220osclock` (nav limit-cycle detector)

**Committed BEFORE the shard's first heartbeat (two-clock vs first TSV row).**
Builder s38, 2026-08-14. Queue #54 (research-stocked from the 483b5bcd trace;
prevalence census: **11.58% of ALL v125 builder-rounds in permanent two-tile
locks, 47.6% of games, midgard 35.6%**, gradient with map size).

## Mechanism being fixed (named at lines, both lanes)
`_nav` (eco.py:735) increments `stuck` ONLY when all four fallback moves
FAIL; a moving A↔B loop (BFS plan flipping per step via the
position-dependent blocked set at eco.py:646) never trips the `stuck>=5`
repick at eco.py:1055 — a permanent, silent lock. No detector existed.

## The arm (one mechanism)
`bots/_v220osclock` = v125 chassis + a last-K parity detector at the top of
`_nav` (mirrors raid.py's teleport-detector pattern): K=8 positions, strict
A/B alternation with A≠B ⇒ clear history, `tgt=None`, `stuck=5` (the
EXISTING repick machinery fires next decision round). Constants
`LOKI_OSC_DETECT_ON/LOKI_OSC_K` in doctrine.

## Dose evidence (both ways, pre-launch)
* Predicate fixture drive 5/5: lock fires, anti-phase fires; walk, 3-cycle,
  standing-still silent.
* Kept-replay midgard batch (n=12, seeds 260001-6, both seats), scored by
  research's `nav_limit_cycle_census.census_game` (the #54 regression
  instrument, positive-controlled on 483b5bcd): **treatment 1.55% locked
  builder-rounds vs control 5.37%; games with ≥1 lock 1/12 vs 4/12.**
  Control side still locking = the instrument's positive control inside the
  dose batch itself.
* **Known gap, declared:** the strict-alternation predicate misses dwell-2
  (period-4) cycles — the residual treated-side lock is consistent with
  this. Arm 1b (dwell≤2 window match) is the follow-up if the screen pays.

## Design
`OSCLOCK` vs `bots/_v197mapcode`, standard 15-map pool, n=5400, seed_lo
258000, futility gates per RULE-futility-gates, OB-F final band 48.67–51.33.
D26: replicate iff |final−50| ≥ 2.0pp (seed 259000, scored alone, same-side
pooling). Kill-round paired-seed rides (freed builders should not slow the
kill; the census says they were doing nothing anyway — median lock onset
r68). Coupling class: **self-knowledge / navigation robustness ⇒
screen-trustworthy at full weight** (no opponent-behaviour dependence; the
lock fires against every opponent class incl. self-play).

## Not licensed
No ship implication (hold + SHIP_SIT govern). No claim about raid-path
locks (raid.py movement does not flow through `_nav` — separate surface,
#48's territory). Maps note: pool's valkyrie is PRE-patch (same era fixture
as all concurrent shards, era-labeled at read).

## Target-value line
Local screen, zero live exposure ⇒ payout gate N/A.
