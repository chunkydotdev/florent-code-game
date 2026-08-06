# Handover — 2026-08-07, updated after session 5 (parallel loop, tag `aug7`)

Start here, then [README.md](README.md) → [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md).

## Session 5 (parallel): four hypotheses, zero accepts, one real finding

Ran the loop with **three Sonnet subagents concurrently**, one hypothesis each, then a fourth
follow-up. `bots/aug7` is **unchanged** — nothing cleared the accept gate.

| hypothesis | screen (n=48) | confirm (n=256) | verdict |
| --- | --- | --- | --- |
| deliberate harvester→Core conveyor chains | 54.2% [40.3, 67.4] | **45.3% [39.3, 51.4]** | discard |
| aimed sentinel placement (`get_attackable_tiles_from`) | 56.2% [42.3, 69.3] | **50.0% [43.9, 56.1]** | discard |
| demand-driven ammo conversion | 41.7% [28.8, 55.7] | **46.1% [40.1, 52.2]** | discard |
| harvester first-conveyor fix | — | not run (no gap to fix) | closed |

Zero crashes on either side across ~800 matches. All four are written up in
[strategy-log.md](docs/strategy-log.md).

**The finding worth more than the three nulls:** `_try_build_conveyor_toward_core` is **dead
code in the entire lineage** (starter, v4, aug7) — verified, 24 calls / 0 legal / 0 built. The
cause is a grid-parity fact that constrains a whole class of ideas: *a builder adjacent to a
building it just placed can never build anything orthogonally touching that building*, because
two tiles one step apart share no common orthogonal neighbour. **Do not fix it** — instrumented
across 8 maps, 263 of 264 harvesters (99.6%) get an adjacent conveyor anyway from incidental
trail-laying. Also logged in [opponents.md](docs/opponents.md): most of the field inherits the
same dead function from the shipped starter.

**Method notes from this session:**
- **Run a null-change control.** A byte-identical copy of aug7 vs aug7 (n=96) gave 48–48 and,
  more usefully, the first real baseline for the **win-condition mix** (`core_destroyed`
  16.7%). Without it, "44 core kills" is an uninterpretable number. Both discards that looked
  mechanistically interesting were settled by comparing against it.
- **Screens are close to worthless as evidence.** Two of three screened above 50% and confirmed
  at or below it. Under "keep if the number went up" this session accepts two dead changes.
- **Parallel agents need `--jobs 3`**, and the control was re-run at that setting first to
  confirm the harness still reads a no-op as a coin flip under contention. It does.
- **One change per experiment, strictly.** The ammo experiment moved a floor *and* added a
  mechanism, so its loss is unattributable between the two. That's a wasted slot, not a result.

**Scratch dirs left on disk, untracked:** `bots/aug7_h1|h2|h3` (discarded implementations,
kept in case the code is worth reading), `bots/aug7_h4` and `bots/_probe_conv`
(instrumentation only). Delete them freely — nothing depends on them.

## Where we are

- **`bots/aug7` is the current best and the new submission candidate**: 80.5%
  [75.2%, 84.9%] vs starter over 256 matches, zero crashes vs starter's 538. It is v4 plus
  one accepted change: **Sentinel-first defense instead of Gunner-first**, confirmed 68.4%
  [62.4%, 73.7%] vs v4 over 256 matches — the biggest single-change jump since v1's crash
  fix, and it started producing `core_destroyed` wins where the Gunner-first lineage
  essentially never had any. `bots/aug7` is **not** frozen/protected like `bots/v*` — it's
  still the live edit target for the next session; freeze it into `bots/v5` when ready to lock
  it in as a submission candidate (that promotion is Magnus-only per `.claude/settings.json`).
- **Three follow-up hypotheses were tested and discarded this session**, each logged with a
  mechanism, not just a number (`docs/strategy-log.md`, all dated 2026-08-07):
  - Raising `AMMO_BUFFER` 20→50 for the sentinel's higher per-shot cost: no-verdict, 45.3%
    [39.3%, 51.4%] — a bigger buffer just parks Ti as idle ammo in quiet phases instead of
    building.
  - `SCOUT_ROUNDS=20` delay before any building starts: decisively refuted, 8.3%
    [3.3%, 19.6%] — settles that open question outright. Harvester ROI dominates the
    scale-tax-avoidance argument by a wide margin.
  - Map-size-branched defense trigger (1 harvester instead of 3 on ≤150-tile maps): refuted,
    35.4% [23.4%, 49.6%] — same failure shape as the scout-first discard, in miniature.
  - **Net effect:** two open questions closed with clear answers, and growing evidence that
    this bot's economy-first shape is robust across map size — cutting economy for earlier
    defense loses every way it's been tried so far.
- **Every offline-answerable question from session 1 is still answered and current** in
  [game-model.md](docs/game-model.md): Core spawn = the 12-tile ring; seat wipeouts were
  mostly our own absolute-direction bias (fixed) plus a real engine first-mover edge on 8×8
  (unfixable bot-side); titanium is credited — balance *and* tiebreak counter — **only on
  delivery to the Core**.
- [docs/runbook.md](docs/runbook.md) exists: the approval-day checklist and the recalibration
  procedure for the organisers' announced changes (map pool hidden until the tournament,
  possibly other variables). Probe bots are kept in `bots/probe_*` so re-verifying measured
  facts against a new engine takes minutes ([tooling.md](docs/tooling.md)).

## The one blocker (unchanged)

Registration approval — application submitted, awaiting the invitation. The moment it lands,
run [runbook.md](docs/runbook.md) §1 top to bottom: login → `maps sync` → pool census →
re-baseline arena on the real pool → submit the frozen candidate → `match test` on real
hardware → answer the platform questions in [open-questions.md](docs/open-questions.md)
(prize categories, team rules, finals dates, **how seats are assigned within a best-of-five**
— first-order now). **Note:** the runbook's step 5 still says `fcode submit bots/v2` — update
the submit target to whichever version gets frozen as the candidate (aug7's lineage, once
promoted) before running it.

## Traps

All from prior sessions still apply (python3 is 3.14 — use `.venv/bin/`; always `--tle 10`;
`print()` goes to the replay; never single-seat or pooled evaluation; the project
`CLAUDE.md`/`AGENTS.md` is the organisers' doc with known errors — game-model.md wins);
`random` is NOT seeded by `--seed`; absolute-direction habits are a bug class; program.md's
accept gate is for strategy changes, not insurance changes. New this session:

- **Compare screens/confirms against the current incumbent commit, not `starter`.** `starter`
  is now far enough behind (aug7 beats it 80.5%) that a marginal improvement over the
  incumbent is invisible in a vs-starter run — both read as "big win" regardless. This session
  checked each change out into a scratch `bots/_incumbent` dir via `git show <sha>:path >
  file` and ran `arena.py aug7 _incumbent`, deleting the scratch dir after. `results.tsv`
  entries record which commit was actually the comparison baseline.
- **A change that looks reasonable can still lose to opportunity cost.** All three discards
  this session shared one shape: trade some economy for earlier/cheaper defense or lower
  scale tax. All three lost, by comfortable margins. Don't re-try variants of "delay/skip
  economy for X" without a genuinely different mechanism — the pattern is now well-evidenced,
  not just one data point.

## Not done

- Daily retro for 2026-08-07 in the dev-knowledge vault.
- Still no `git remote`; `results.tsv` still deliberately untracked.
- Remaining unknowns, ranked with methods, in [open-questions.md](docs/open-questions.md):
  ore depletion, enemy-conveyor crediting, `destroy()` refund on dead-end stacks, adaptive
  ammo buffering (the AMMO_BUFFER discard's suggested follow-up), and the platform questions
  above.
- Untested from this session's remaining hypothesis list: `destroy()` on obsolete/dead-end
  conveyors (deprioritized — correct dead-end detection needs real topology tracking, higher
  engineering risk than a quick attributable change); harvester payback/chain-length
  crossover as an explicit lever (no concrete code change was designed for it yet).
