# Handover — 2026-08-09/10, after session 10 — READ THE OVERNIGHT ADDENDUM FIRST

## OVERNIGHT ADDENDUM (session 10, autonomous loop while Magnus was AFK)

**Live: platform v53 "v68-saboteur-escort" (= `bots/_v68si`), 7-3 on the ladder, peak
1557 / rank #26** (from 1383/#40 at the start of session 9 — +174 in ~30 hours). One of
three allowed overnight submissions used; policy and bar held for the rest.

**What v53 is:** v52 (heal reflex) + the saboteur REPAIR ESCORT — the role-1 expander
guards whatever building a raider is chipping and out-heals the pecks (1 Ti/+4 HP beats
2 Ti/2 dmg; builders cannot attack units, an implementer catch that turned the spec into
something better). +10.0 pts on flotte_probe [intervals separated], flat everywhere else.

**The instrument triad is complete** — gate defense work against all three:
| probe | md5 | models | live-bot baseline |
| --- | --- | --- | --- |
| `bots/band_probe` | 33cd3c14… | Banminary all-in rush | 90.0% (was 26.7% pre-heal) |
| `bots/flotte_probe` | ff968416… | Flotte strangulation | 86.7% (v53) |
| `bots/kladde_probe` | 42fa9f50… | kladde slow grind | **73.8% — the open front** |

**Overnight verdicts (all in results.tsv):** `_v69pp` perimeter patrol DISCARDED (eider
gain churned away elsewhere); `_v69bc` builder-cap scaling DISCARDED as parameterized
(~13-pt opp_v50 regression from cost-scale inflation); `_v69dr` defend-succession
HOLD-in-family (proven mechanism, inert on all instruments, zero cost); `_v67hg*` battery
line CLOSED (heal package absorbed its value); dead engineer branch REMOVED in
`_v69clean` (byte-identical, verified). **Family head / next-session base: `bots/_v69clean`**
(= _v68si + succession + cleanup; unshipped — no measured improvement, bar is the bar).

**Next queue, evidence in hand:**
1. **Leaner builder-cap re-tune.** The grind probe out-collects us 17.5k vs 13.8k over
   1000 rounds (replay `si_kladde_eider.replay26` in the session scratchpad) — the cap
   thesis is right, `_v69bc`'s shape was wrong (cap 8 + 3 replacements inflated cost
   scale). Try cap 6, replacements-only, or ECO_CAP raise instead.
2. **Grind residual mechanism** (probe sweeps eider/hive 16/16 vs v53) — diagnose before
   coding, one replay is already captured.
3. **Nemesis audits:** Powerpuff Girls and I Stone have each beaten two consecutive
   versions of ours narrowly — ladder replays downloadable by match id.
4. Strangle residual (meander/eider vs flotte_probe) resisted three targeted fixes —
   revisit only with new mechanism evidence.

**Meta for the next session:** the probe-first discipline paid immediately (bc's
regression was caught by opp_v50 screening, pp/dr honestly refuted by their own target
instruments); identical-rows is now a reflex-check fingerprint (caught two dead-code
situations); the replay analyst agent's pipeline (`timeline.py`, `report_gen.py`,
`econ_curve.py` in the scratchpad) decodes any .replay26 — scratchpad dies with the
session, so REGENERATE from tools/replay_census.py + the replay files if needed.

---

## SESSION 10 LATE ADDENDUM — v8 candidate `bots/_v67ch2`, validated on a new instrument

Everything below the addendum still holds, but the evening continued past the v7 submit
(v7 went live as **platform v51**, climbing 1475 → ~1512-1517, rank #30) and produced the
highest-value change in project history:

- **Unrated scouting program (Magnus, ~12 matches, 10 teams from #33 to #1):** our offense
  wins games at every level (beat Lorem 3-2, took games off Pantheon #4 and Pivot #1); our
  early defense loses to the band's three styles — hyper-rush (Banminary r42-58 kills on
  EVERY map), mid-siege (Flotte r144-239), grind (kladde/sporks). Replays all archived in
  the session scratchpad; `tools/replay_census.py` + schema decode them.
- **Replay post-mortems found the mechanism:** (1) our own counterbattery gate locks home
  defense out when an offensive forward gun eats the free-battery allowance and harassment
  pins harvesters < ECO_NEED (meander loss, heart loss — the gate we handed x3r0 is
  exploitable from the other side); (2) core healing decided every game: 0 heals in both
  losses, 82 heals (+328 HP) in the win, and the whole heal capability hung on ONE builder
  (role_n 4) not being distracted — melee short-circuits starved it.
- **`bots/band_probe`** (md5 33cd3c140882b1466f492653cfb08dcf) — NEW frozen instrument,
  replay-extracted Banminary all-in rush (launcher-thrown builder r2, zero eco, ~75% Ti to
  ammo, 4-angle barrage, r29-56 kills). **The live bot scores 26.7% against it.**
  `rush_probe_fast` (97.5%) was measuring nothing real. Gate all early-defense work here.
- **`bots/_v67ch2` = _v66mB + the core-heal package** (universal adjacent heal on
  SLOT_UNDER!=0 — noise-free because can_heal refuses a full core; heal-beats-sabotage
  under observed shelling; role-4 defender walks home when the core visibly loses HP; zero
  store-semantics changes): **93.3% vs band_probe (from 26.7%), 64.2% vs opp_v50 (best
  ever, from 56.7%), guards 97.9/100.0/95.8 green, 0 crashes.**

```bash
# Magnus: v8 ship
cp -r bots/_v67ch2 bots/v8
.venv/bin/fcode submit bots/v8 --name v67-heal-reflex
.venv/bin/fcode status
# then rerun the loss pairings as before/after (deterministic rematches):
# fcode match unrated <flotte-id> --map meander --map eider ...
```

- **On hold, pending better design:** the `_v67hg*` battery-gate line (slot split +
  damage-gated unlock). hg4 finally made the design function (clobber guard: builders
  write SLOT_UNDER=1 only when the slot reads 0) but it costs the meander sweep vs opp_v50
  (53.3%); re-evaluate against band_probe now that it exists — the heal package may have
  absorbed most of its value anyway. Refuted en route: _v67hg naive split (45.6%),
  _v67hg2/hg3 (==2 unreachable — clobbered; identical-rows fingerprint caught it twice).
- **Equivariance program: paused with verdict "reroll, not convergence"** (rows in
  results.tsv; _v66eq* variants kept). Dead engineer branch discovered (round-0 buffered
  store read — activation measured 41%, DISCARD; branch should be deleted). Tell x3r0: his
  engine shares the dead branch and the counterbattery lockout exploitability.
- **Unrated meta-facts:** matches vs the same team on the same map are deterministic
  repeats (one sample per pairing); the CLI can queue them (`fcode match unrated <team-id>
  --map X`, up to 5); choose maps deliberately, never random; rotate opponents.
- v51's ladder record so far: 5W-3L, 1475 → ~1512. The rolling regression check matures
  around match ~161 but v8 supersedes the question.

---

# Original session-10 handover below (still accurate for the pre-addendum state)

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
2. **Counterbattery ECO_NEED gate — DELIVERED (Magnus → x3r0, end of session 10).** Expect
   his next upload to absorb it: our fjordgate/meander 32/32 sweeps against his engine
   should disappear, and our measured edge over him will shrink accordingly — that is the
   point (team Elo is shared; his bot defends the rating when his is active). When his next
   version lands: re-pin, re-gate, and CHECK THOSE TWO MAPS FIRST — they are the receipt
   that the gate went in.
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
