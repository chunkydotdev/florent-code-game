# Handover — 2026-08-07, updated after session 4 (program.md loop, tag `aug7`)

Start here, then [README.md](README.md) → [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md).

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
