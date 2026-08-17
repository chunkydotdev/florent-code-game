# BUILD REPORT — `bots/_v509saltray` (SALT×RAY coordination arm), s50 2026-08-17

*Banked by the builder s50 from the opus build agent's final report. The agent built and
mechanism-verified; the builder commits; no verdicts here. Scratchpad artifacts (probe arms,
logs, runners) live in the s50 session scratchpad under `v509build/`.*

## Lineage

**`_v488beltbreak2` → `_v508raydisc2`** (all four files diffed): only `main.py` and
`doctrine.py` change; `eco.py`/`raid.py` byte-identical. doctrine.py:2085-2256 = RAYDISCIPLINE
+ FF blocks (7 constants); main.py:167-187 per-sentinel state; main.py:989-1108 two-pass
sentinel scan with core→belt diversion (BUDGET=6/life, CORE_HP_STOP=90); main.py:1112-1186
`_rd_forward` + logging. v508's own contribution = ONE condition (refuse a diversion candidate
when OUR builder stands on the tile; enemy-builder tiles stay legal, counted apart).

**`_v508raydisc2` → `_v509saltray`:** doctrine.py:2257-2429 (LOKI-SALTRAY block + CAGE block);
main.py:188-200 per-unit state; main.py:317-321 + eco.py:544-546,1697-1699 (dead
`SLOT_ECO_READY` writes gated off — slot 5 reclaimed, it had three writers and ZERO readers in
any ancestor); main.py:1020-1026,1088-1091 (remember the refused-highest-value tile);
main.py:1097-1108 publish site (fires only when the refusal actually cost the diversion);
main.py:1192-1228 `_sr_publish`; raid.py:217-246 yield call ahead of the action ladder +
movement freeze; raid.py:283-459 `_sr_yield` + `_sr_break_cage`.

**The FF guard is byte-identical v508→v509** (diff of v508 main.py:1024-1051 vs v509
main.py:1048-1075 is empty).

## Flag / store

`SALTRAY_COORD_ON = True` @ doctrine.py:2347. `SLOT_RAY_YIELD` (:2350) = reclaimed slot 5.
Encoding (one int): bits 0-5 x, 6-11 y, 12-13 dx+1, 14-15 dy+1, 16+ round+1; 0 = no request.
Facing is in the packet — "step off the ray" is not computable from the tile alone.
`LOKI_SALTRAY_STALE=3`, `HOLD=4`, `MAX_BREAK=2`, `LOG=False`.
The es>1 half needed no edit: a refused candidate is excluded from `rd_best` (main.py:1086),
so a clean lower-value tile already beats a shielded higher-value one.

## Verification (fixture A = paired deterministic NOISE_OFF, 27 maps × 2 seats, tle 10;
fixture B = independent NOISE_ON; opponent = namespaced `_v488beltbreak2` copy)

| check | coord-ON | coord-OFF | driven the other way |
|---|---|---|---|
| own-builder hits | **0**/415 shots (A), 0/270 games (B) | 0/336 | FF_GUARD=False arm: **22.1%** own-hit (38/172), 0.235/g — reproduces s49's 21.8% [11.1,38.4] |
| yield events | A: 64 publishes → 10 step-offs + 54 cage-breaks (100% conversion); B: 26 → 8+18 | 0/0/0 same LOG=True binary | the zero-read is the instrument's other verdict |
| effective econ dose | A 0.809/g; B 0.756±0.178 | A 0.646/g; B 0.626±0.183 | v507-shape arm: 0.790/g effective AND 0.235 own-hits/g |
| flag-off equivalence | — | **162/162 cells identical** vs `_v508raydisc2` (+ 432/432 ON-undosed cells identical) | first comparator misread arm-name winner column (77/162); normalised → 162/162 |
| SALT composition | 36.08 fires/g (A) | 36.78 | paired Δ −0.680 ± 1.373 cluster-correct — flat |

**Dose:** paired +0.163 ± 0.057 naive, **+0.162 ± 0.172 cluster-correct (CI includes 0)**;
independent +0.130 ± 0.256. **The well-powered signal is refusals: 2.621 → 0.255/game (~90%
reduction; B −2.185 ± 1.011, CI clear of 0).** Only 6/50 independent cells ever dose (26/270
games) — **this local fixture cannot power the dose itself.**

**Outcomes, labelled not claimed:** kill≤r300 117/486 BOTH arms exactly; share −2.0pp ± 3.9
cluster-correct (A), −0.4 ± 8.4 (B); timely-kill +4.8 ± 7.4 (B). Escape cost: 54 barriers
demolished / 486 games (0.11/g), MAX_BREAK cap never observed binding.

## Surprises (agent, verbatim in substance)

1. ⭐ **THE PLANK AS BRIEFED WOULD HAVE FIRED 2/204. OUR RAIDERS ARE CAGED — BY OUR OWN
   `LOKI_BARRIER_SEAL` COLLAR.** At 204 published-tile events, move cooldown 0 but `can_move`
   False in all four cardinals in 202 (99.0%). Neighbours: 561 our-own-barrier (can_destroy
   True 561/561), 204 the ENEMY CORE (one per event), 47 wall, 4 passable. The shield raider
   sits on the enemy's core-adjacent delivery conveyor — the highest-value belt kill on the
   board — which v508's guard was declining EVERY RELOAD for the rest of the match (same tile
   republished r187,189,191,193,…). Actuator rebuilt as a **seat swap**: destroy own barrier,
   step into it, keep the seat, keep the peck.
2. **`destroy` does NOT spend the move** — destroy-then-move-in same turn 54/54 (A) and 18/18
   (B). The no-move branch is coded and has never fired (not claimed verified).
3. ⛔ **SEED INERT UNDER NOISE_OFF with fixed map + deterministic bots:** 35/50 (map,seat)
   groups produced one identical game across 9-10 seeds; effective n = 50 groups / 68 distinct
   games, not 486. A 9-seeds-9-cells false finding ("9 discordant, all ON-losing, CI excludes
   0" — all nine the same hive game) was caught by this. QUALIFIES the s49 seed law: distinct
   seeds pair on NOISE_OFF, but on most maps the seed does nothing when both bots are
   deterministic — paired NOISE_OFF cell space tops out at ~54 cells here. Intervals from this
   fixture MUST be clustered on (map,seat).
4. Comparator hazard (own instrument): the shard `winner` column holds the ARM DIRECTORY NAME;
   raw read gave 77/162 false non-equivalence; normalise to US/OPP first.

## PIDs / hygiene
All launched PIDs exited on their own (54668, 58314, 66326, 70331, 91466, 25463); the foreign
`corefill_forever.sh` (68004) identified and left alone. Nothing in the repo touched except the
new `bots/_v509saltray/` tree.
