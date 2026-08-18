# PROBE REPORT — DOUBLEFERRY: two builders launched to the enemy core (s51, 2026-08-18)

*Banked by the builder s51 from the opus probe agent. Magnus's question: "how well does it work
to launch two builders quickly to the opponent — how quickly are they at the enemy core?" and
his relay rule, folded in mid-build: "both builders need to be launched before the launcher can
be destroyed and a new launcher can be built." TIMING PROBE, NOT A SHIP CANDIDATE (two `# PROBE:`
sacrifices in-tree: chassis home-ferry off to free store slots; crew seat moved 3→1 for an r1
spawn). 30 games (5 maps × 3 seeds × 2 seats) vs `_v488beltbreak2`, `--tle 10`, NOISE as fired,
0 tracebacks (+6 variant +4 singles). Artifacts: `scratchpad/s51_doubleferry/` (trees, 30-game
logs+replays, dblferry.tsv, parsers with a 7-case both-ways fixture, DIFF patches).*

## THE ANSWER
**Both bodies at the enemy ring with a 1-round gap in 26 of 30 games, at floor+1 speed on 4 of
5 maps:**

| map | body-1 ring (median) | body-2 ring | mechanical floor (b1/b2) | walk-only | as-built body-2 (s50 crew) |
|---|---|---|---|---|---|
| nordkap | r7 | r8 | 6/7 | r15 | r8 |
| atoll | r7 | r8 | 6/7 | r17 | — |
| glacierkeep | r11 | r12 | 10/11 | r27 | r27-29 |
| drakkarfjord | r13 | r14 | 12/13 | r41 | **r197** |
| midgard | r17.5 | r27 | 12/13 | r42 | — |

Pooled medians: b1 r11, b2 r12, gap exactly 1 (26/30). Alive at arrival+10: b1 29/30, b2 27/30.
Relay vs walking: 1.9-2.9× for body-2. Incidental outcomes (n=30, one-draw, NOT a ship read):
14/30 wins, 28 core-kills, **17/30 kills ≤ r300**, median end r260.

## THE RELAY (Magnus's rule, working as specified)
Strict 2-round cycle per link: HOPBUILD launcher one tile ahead → throw body-1 → next round
throw body-2 → self-destruct → ferried body builds the next link ~5-6 tiles forward.
* **Cadence measured: one throw per round, consecutive rounds legal, never two in one round**
  (cooldown +=1, end-of-round decrement).
* **Teardown must be `self_destruct()`** — after a hop both bodies are 5 tiles away, so
  `destroy()` (needs an adjacent allied builder) is unavailable.
* **Two-throw compliance: 78/78 links on 4 maps** (midgard 6/39 — the residual).
* **Scale refund CONFIRMED ON THE ENGINE**: trace oscillates 190↔200 all chain long — exactly
  one launcher's +10% alive at a time; a six-hop chain costs +10% total, not +60%.
* Chain cost: 2 links/74 Ti (small maps) → 6.5 links/265 Ti (midgard). One launcher per hop
  ferries BOTH bodies — half the as-built launcher count.
* Throw displacement over 296 throws: median 5.10, max 6.08 tiles (launcher sits one ahead of
  the body; √26 from the launcher, never exceeded).

## WHY THE AS-BUILT CREW WAS SLOW (the drakkarfjord r197 mechanism)
**A lost update on a buffered store slot with two writers.** Writes land next round; two units
writing one slot in the same round both read last round's word and the higher entity id wins.
Measured: the sealer's `FS_CREW_SLOT` beat never advances once the support exists → the crew
staleness detector fires → **the support promotes itself to sealer ~6 rounds after spawning**
(FS PROMOTE r10) → no support exists; later bodies re-read seat 0 as stale; each body builds
its OWN parallel chain 3 rounds apart down identical tiles, double launchers, funded from the
collar's bank. The "r197 support" was a replacement appointed 150 rounds later. Probe fix:
one writer per slot (support publishes to its own slot; ferry reads both rids).
**ROUTE TO ATLAS at wrap: buffered 16-slot store + two same-round writers = silent lost update,
higher id wins. This defect class produced the single largest timing defect yet measured in the
ferry line (183 rounds).**

## RESIDUAL — midgard (the one map off floor)
Body-2 spawns d²=2 from the lead, drifts forward during the 2-round muster, and is 2 tiles
outside the first link's envelope at throw time; the chain then advances ~3 tiles/round vs a
1-tile walk, so **one lost envelope is lost forever** (body-2 r33 vs r16). The obvious fix
(walk body-2 toward the lead) was tried and measured NEGATIVE (n=6: it occupies the lead's
forward build tile; two-throw links 2→0) — reverted, in `VARIANT-lead-follow.patch`. Next
candidate: hold-station that also vetoes the lead's forward build tile.

## Instrument guard
7-case synthetic fixture through the parser, all PASS, incl. never-arrived → −1 not 0, and 4
mutations that must move the answer. Real-log negative branch confirmed (atoll-s3-A b2_adj=−1
with b2_ring=8). Independent core-side DF DEAD observer separates degrade from death.
