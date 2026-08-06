# Handover — 2026-08-09/10, after session 10 (v7 frozen and ready; x3r0 shipped three bots in one night)

Start here, then [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md) → [docs/opponents.md](docs/opponents.md).

## Where the ladder stands

**x3r0 is running his test window.** Session 10 opened with our v48 (= `bots/v6` = `_v64cbA`)
live — Magnus shipped it before the session; it went 1383 → 1421 over 3 matches. Then x3r0
uploaded and activated, twice: platform **v49** "v62-rush-deny-cpu" (18:17), then platform
**v50** "v63-rush-bunkers" (18:48, still active, ~1461 @ 140, rank #34, 4W 1L in his window).
Expected per the regression rule: teammate-activation windows are a named confound; no
rollback reasoning applies to them. When his window ends, activate our best (see next).

**Naming**: platform v45 = `bots/opp_v45` (old frozen gate). v48 = ours = `bots/v6`. v49 =
`bots/opp_v49` (md5 a3d5f0e1…, strategy-identical to the folder he handed us; his platform
copy adds a CPU bail-out + run() exception wrapper ported from our ladder1 — **note his
wrapper makes arena crash counts for him read 0 by construction**). v50 = `bots/opp_v50`
(md5 fa87d78e…) = **the current primary gate** (hardest known opponent).

## READY TO SUBMIT: `bots/v7` (= `_v66mB`), frozen by Magnus, fully validated

v6 + three gated keeps stacked into one submission:

1. **`LAUNCH_GIVEUP_RND = 180`** (`_v65lw`) — unifies the r180 give-up / r<200 re-recruit
   flip-flop that made the launchwait give-up dead code. Battery: flat everywhere, 0 cost.
2. **`LAUNCH_STALL_RNDS = 36`** (`_v65sb`) — per-unit launchwait progress bound + 12-round
   re-recruit block; bounds the waiter that otherwise idles to r180 (or forever in matches
   decided earlier). Flat-to-up everywhere, 0 cost.
3. **Wall-gated melee-before-repair** (`_v66mB`) — `MELEE_FIRST_MAX_WALL_FRAC = 0.015`
   activates opp_v49's `_saboteur` reorder ONLY on near-wall-free maps (drumlin 0.64% is
   alone under the threshold; next is meander 2.13%). The GLOBAL variant (`_v66mA`) was
   refuted: it converts drumlin but loses the hive sweep and hands moonrise away — repair-
   first is load-bearing on denser maps.

| gate | result |
| --- | --- |
| vs `opp_v49`, 480 | **62.1% [57.7, 66.3]** (baseline `_v65sb` 58.8) |
| vs `opp_v50`, 480 | **56.7% [52.2, 61.0]** — his v50 re-took drumlin, we gained lighthouse |
| starter / opp_v39 / rush, 240 each | 97.5 / 100.0 / 97.5 — all flat-or-up, 0 crashes ours anywhere |

```bash
# Magnus (bots/v* and platform writes are Magnus-only; freeze already done):
.venv/bin/fcode submit bots/v7 --name v66-launcher-drumlin
.venv/bin/fcode status   # verify — submissions have auto-activated on upload
```

## The three big things session 10 learned

1. **The mirror seat table (queue item 4, finally run) is an all-or-nothing instrument.**
   `_v66mB` self-play, 480: **all 15 maps fully seat-decided** (9 to seat B — so it is not
   first-mover advantage; it is our own asymmetries). Fixing ONE asymmetry (`_v66eq`, the
   equivariant `_plan_siege` tie-break) left all 15 still seat-decided and flipped heart's
   direction: under a deterministic engine any residual asymmetry re-decides every seed.
   Partial equivariance fixes are invisible in mirrors — judge them per-map vs a different
   engine.
2. **Map-specific counters decay at the speed of x3r0's iteration** (three bots in one
   night). Melee-first won drumlin vs v49; v50 took it back within the hour, while lighthouse
   fell to us. Structural fixes and correctness-at-the-seams keep their value; whack-a-mole
   doesn't. (Session 8's lesson, third confirmation.)
3. **SPRT works and is adopted** (queue item 6 landed): `tools/sprt.py`, calibrated on the
   settled 70% gate — H1 at 40/480 matches, estimate dead on 70.0%, 15 s wall clock.
   Screens/discards may cite SPRT; **ship gates stay fixed-480 arena** (pair correlation
   makes the boundaries approximate; the tool's own footer says so).

## The next queue, ranked

1. **Finish the equivariance set on the `_v66eq` base** — the audit inventoried the
   remaining non-equivariant sorts: spawn-ring placement (`main.py:409`, tie-break tail),
   spawn-dispersion hash (`:412`, primary key is a coordinate hash — worst offender),
   ore partition (`:1421`, hash tie-break feeding a strided split). One gated change each,
   SPRT-screened, judged per-map vs `opp_v50`. `_v66eq` alone: 58.8 vs 56.7 overlapping,
   churn (+drumlin +snowflake −lighthouse −eider); verdict HOLD — the bet pays as a
   completed set or not at all (see mirror lesson above).
2. **Second launcher wart remains half-open**: the stall bound caps the waste but the
   single-slot `_offer_launch` monopoly (no progress check, incumbent holds `SLOT_LAUNCH_ID`
   forever) is untouched, and the launcher fixes measured zero-gain vs x3r0's engine —
   insertions rarely resolve. Either make insertions actually fire (drop-site logic) or
   spend the units elsewhere; measure on non-mirror instruments.
3. **Fjordgate root causes** (unchanged from session 9 queue): SLOT_THREAT takes builder
   positions for fixed-facing aiming; absolute threat radii don't scale with map size. Both
   still live in ours AND his engines. The gate cured our symptom; his v50 still loses
   fjordgate 0/32 to us — see team etiquette.
4. **Re-tune constants on the integrated base, last** — unchanged.
5. **Weekly rotation watch**: pool censused this session — 15 maps, all local, harness needs
   NO upgrade for map coverage. When the rotation lands, runbook §2; per-map artifacts
   (melee-first threshold list, map tables) inherit the one-week shelf life.

## Team etiquette — messages for x3r0, updated

1. ~~Stale map tables~~ — **moot**, his v62 refresh fixed them (that is what flipped
   drumlin/saga/heart into contests).
2. **Counterbattery ECO_NEED gate — still the highest-value handover.** His v50 still loses
   fjordgate 32/32 and meander 32/32 to us; the six-line gate is measured at +6.7 pooled on
   his own engine class. Offer it.
3. **Launchwait warts**: his engine has the unfixed r180/r200 flip-flop AND the stall-free
   waiter (audit line refs in strategy-log). Ours are fixed in v7; the diff is small.
4. Credit where due: his platform v49/v50 adopted the CPU bail-out + exception wrapper from
   our `ladder1` — collaboration is flowing both ways. Everything on his base stays credited
   to his engine.

## Operating notes

- **Elo tape**: `elo_history.tsv` current through the v50 window; v48 baseline row 1410@134
  (activation moment between 133 and 134 unobserved — noted in the row). **Amended shipping
  rule (Magnus, session 10): local-battery-clean ships immediately; the ~20-match trajectory
  check runs ROLLING on whatever is active, post-hoc, rollback to the last healthy-record
  bot if clearly negative absent confounds. One submission per validated batch, not per
  change.** The monitor (5-min poll) appends rating ticks AND watches `submission list` for
  new team uploads — re-arm BOTH at every session start, exactly one appending monitor at a
  time.
- **Two-tier orchestration confirmed working at scale** (Magnus, this session): Opus
  subagents implement, Sonnet subagents audit read-only, ALL measurement/tape/verdicts stay
  in the main loop. Six delegations this session, zero contradictions with measurement.
- **`bots/v*` denial is harness-enforced even via Bash** — the freeze `cp` is genuinely
  Magnus-only (verified by denial this session). AFK freeze: Magnus types
  `! cp -r bots/<candidate> bots/v<N>` in the prompt.
- Gates serialized as ever; SPRT is the new screen; chained multi-gate Bash calls fit the
  10-min background cap so far, but split them if a chain risks it.
- `results.tsv` untracked append-only tape; every number above is a row. Still no remote.

## Where things live

| path | what it is |
| --- | --- |
| **`bots/v7`** | **frozen ship candidate (= `_v66mB`), awaiting Magnus submit** |
| `bots/_v66mB` | wall-gated melee-first, the v7 content |
| `bots/_v66mA` | refuted global melee-first, kept for reference |
| `bots/_v66eq` | equivariant siege tie-break, HOLD — base for queue item 1 |
| `bots/_v65sb` / `_v65lw` | the two launcher keeps (stall bound / give-up unification) |
| `bots/v6` | live-lineage v48 (= `_v64cbA`) |
| `bots/opp_v50` | **primary gate**: x3r0 "v63-rush-bunkers", md5 fa87d78e… |
| `bots/opp_v49` | x3r0 "v62-rush-deny-cpu", md5 a3d5f0e1… |
| `bots/opp_v45` / `opp_v44` / `opp_v39` / `starter` | older references / no-collapse guards |
| `bots/rush_probe_fast` | rush instrument, frozen, md5 f50ec997dd24b7721ef64f46a1a3c0b4 |
| `tools/sprt.py` | SPRT screening gate (arena.py untouched, imports its play()) |
| safe to delete | `bots/_v64cbB`, `bots/_v63*` intermediates if space is wanted (all logged) |

## Traps

All of sessions 7–9's still apply (see git history of this file for the full list; the tape
rows repeat the operative ones). New this session:

- **A mirror seat table cannot grade partial symmetry fixes.** Deterministic engine + any
  one residual asymmetry = every map 100% seat-decided regardless of how many other
  asymmetries you fixed. Direction flips (heart B→A) are the only visible signal.
- **`cd` in a compound Bash call resets cwd for relative paths of later commands** — the
  opp_v50 pin briefly landed in the scratchpad. Use absolute paths in chained commands.
- **SPRT accepts/refutes fast but its estimate is wide at stop time** (57.4 [48, 70] at
  n=108 vs fixed-480's 56.7 [52.2, 61.0]) — never quote an SPRT point estimate as a result;
  quote the fixed-run number.
- **His exception wrapper zeroes his crash column.** Any future "0 crashes theirs" row vs
  opp_v49+/v50+ is not evidence of robustness.
