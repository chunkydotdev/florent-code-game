# AUTOPSY — eviction in `_v513siegecrew`'s FIRED config (s51, 2026-08-18)

*Banked by the builder s51 from the opus diagnostic agent. Question (autopsy-before-spec): does
v512-autopsy defect #8 (eviction fired 0× in 19/24) persist in v513's ship config, given that
change E's exemption (`FS_CREW_EVICT_NOWAIT`) is consumed only by the support body and the
support ships OFF? 38 games total: 30 fired-config grid (5 maps × 3 seeds × 2 seats vs
`_v488beltbreak2`, `--tle 10`, NOISE_ON — one-draw law, unrepeatable) + 6 crew-ON guard + 2
smoke. Artifacts: `scratchpad/s51_evict_autopsy/` (fired.tsv, crewon.tsv, parse.py, fixture.py,
grid.sh, logs/, instrumented copies v513_log/ + v513_crewon/ — print-only additions, canonical
trees untouched, 0 tracebacks).*

## ONE-LINE ANSWER
**DEFECT PARTIAL: eviction still fires 0× in 17/30 games (56.7%; 10/18 = 55.6% on the v512
autopsy's own three maps, down from 79.2%), the rung-2 launcher is never bought in 21/30 —
and change E is provably 100% inert — BUT the gate the spec blamed is acquitted: the seal-wait
binds 0.5% of blocked rounds. The real binders are the healer-observation minimum (49.2%) and
the collar-first funding floor (47.8%), and sustained deadlock exposure >20 rounds occurs in
only 3/30 games (median 9 rounds among the 22 exposed).**

## 1. Gate analysis (all `bots/_v513siegecrew/siege.py`, shipped tree)
Fired config: `LOKI_FS_CREW=True`, `FS_CREW_ON=False`, `LOKI_FS_SEAL_ONLY=True`,
`LOKI_FS_RING_LADDER=True`.
* `siege.py:989` and `:1821` both require `FS_CREW_ON and role=="supp"` → **False always**:
  `_fs_supp_turn` is dead code; `min_obs` falls back to `FS_HEALER_MIN_OBS = 5` (v512 value);
  the `FS_CREW_EVICT_RECOVER` income-borrow floor is unreachable. **Change E inert, verbatim
  v512 gates on the primary raider.** Empirical: 0 of 30 fired games logged a `role supp` line.
* `:1850-1857` ladder branch: evictor priced only above
  `FS_EVICT_TI_FLOOR(12) + len(needed)×barrier_cost + FS_SEAL_MARGIN(6)` — the collar-first
  reserve.
* `:1819` — `live >= FS_LADDER_EVICT_MAX(1)`: **a FERRY launcher that lands inside
  `FS_RING_DSQ` counts as the live evictor and suppresses the rung-2 purchase entirely.**

## 2. Which gate binds (4,479 at-ring rounds with no in-ring launcher, n=30)
| binding gate | rounds | share |
|---|---|---|
| healer-obs minimum unmet (`obs<5`, :1824) | 2,204 | **49.2%** |
| funding floor (:1865 via :1850) | 2,140 | **47.8%** |
| seal-wait (`_fs_seal_pending`, :1164) | 24 | **0.5%** |
| all open, no legal site | 111 | 2.5% |

Bimodal by map: drakkarfjord/glacierkeep raiders spend their entire at-ring life at `obs<5`
(e.g. drakkarfjord-s2-A 158/158 rounds) — the evictor is never even priced; on nordkap the
funding floor binds (s3-A 337/343). The seal-wait excludes body-blocked seats BY DESIGN
(`:1373-1379`) — it is not the deadlock mechanism.

## 3. Headline rates (fired arm, n=30; per-game table in fired.tsv)
* Zero-eviction games 17/30 (atoll 0/6, midgard 1/6, nordkap 4/6, drakkarfjord 6/6,
  glacierkeep 6/6). Total throws 248.
* No rung-2 evictor purchase at all: 21/30 (atoll 0/6 — the only map that always buys).
* **4 of 13 throwing games had NO rung-2 build — all midgard: the throws came from a ferry
  launcher re-roled eviction-only by `_fs_launcher_turn:2182`, which then permanently occupied
  the single evictor slot (`:1819`).**
* Deadlock exposure (enemy body on an open orth seat, no in-ring launcher): any 22/30;
  >20 rounds **3/30** (drakkarfjord-s3-B 46, nordkap-s1-A 60, glacierkeep-s3-B 223 — the one
  r1000 loss); median 9.0 / mean 22.1 rounds among exposed; 486 of 6,241 at-ring rounds.
* **Collar closed at least once: 13/30, closure r27-100. atoll 0/6 and midgard 0/6 NEVER
  closed — and atoll is the map where eviction always fires, so eviction is not sufficient
  for closure.** Wins 17/30 (atoll 2/6, drakkarfjord 5/6, glacierkeep 5/6, midgard 2/6,
  nordkap 3/6): **the two never-closing maps are the two losing maps.**

## 4. Instrument guards (driven both ways)
Synthetic fixture 8/8 (incl. mutation control reading 0 on corrupted tags, lau-cancels and
ebody-cancels negative controls, dedup). Live crew-ON arm on 6 matched cells: evictions 0→40
(nordkap-s1-A), evictor builds 0/6→3/6 — counter demonstrably live, direction confirmed.
⚠ Caveat: the crew-ON builds were logged by `role seal` bodies (support role-converts on a
stale sealer, `_fs_supp_turn:697`), so the guard proves the counter reads a difference, NOT
that the NOWAIT exemption specifically drives it. Unpaired (one-draw law). `FS_LOG=True`
costs CPU, so the logging build is not the fired build's timing profile.

## 5. What this licenses (builder reading, s51)
1. The original v514 candidate ("extend NOWAIT/seal-wait exemption to the primary") is
   **mis-aimed** — the seal-wait is acquitted. Candidate gates are `min_obs 5` and the
   funding floor, and the measured cost of the whole deadlock class is small (3/30 sustained).
2. The **closure failure on atoll+midgard** is the bigger, previously uncharacterised signal
   (0/12 closures, 4/12 wins there vs 13/18 elsewhere) — root cause not yet established;
   follow-up autopsy on the existing logs/replays owed before any spec.
3. The **ferry-occupies-evictor-slot** mis-count at `:1819` is a concrete defect with a
   one-line shape (count only launchers ROLED evictor, or exempt re-roled ferries from the
   cap) — but its game cost is unmeasured; fold into the closure follow-up.
