# Handover — 2026-08-06, updated after session 2

Start here, then [README.md](README.md) → [docs/game-model.md](docs/game-model.md) →
[docs/strategy-log.md](docs/strategy-log.md).

## Where we are

- **`bots/v4` is the current best and the submission candidate**: 74.2% [68.5%, 79.2%]
  vs starter over 256 matches, zero crashes, mirror-fair on the maps where earlier versions
  auto-lost one seat. Lineage: v1 crash guard → v2 CPU guard → v3 ring spawn → v4 full
  direction-neutralisation. v4 cleared the strict accept gate (60.9% [54.8%, 66.7%] vs v3).
- **Every offline-answerable question from session 1 is answered**, measured, and folded into
  [game-model.md](docs/game-model.md): Core spawn = the 12-tile ring (both published numbers
  were the same ring from different reference points); the seat wipeouts were mostly our own
  absolute-direction bias (fixed) plus a real engine first-mover edge on 8×8 (~4 in 5,
  unfixable bot-side); titanium is credited — balance *and* tiebreak counter — **only on
  delivery to the Core**. Unfinished chains are pure cost.
- [docs/runbook.md](docs/runbook.md) exists: the approval-day checklist and the recalibration
  procedure for the organisers' announced changes (map pool hidden until the tournament,
  possibly other variables). Probe bots are kept in `bots/probe_*` so re-verifying measured
  facts against a new engine takes minutes ([tooling.md](docs/tooling.md)).

## The one blocker (unchanged)

Registration approval — application submitted, awaiting the invitation. The moment it lands,
run [runbook.md](docs/runbook.md) §1 top to bottom: login → `maps sync` → pool census →
re-baseline arena on the real pool → submit v4 → `match test` on real hardware → answer the
platform questions in [open-questions.md](docs/open-questions.md) (prize categories, team
rules, finals dates, **how seats are assigned within a best-of-five** — first-order now).

## Traps

All five from session 1 still apply (python3 is 3.14 — use `.venv/bin/`; always `--tle 10`;
`print()` goes to the replay; never single-seat or pooled evaluation; the project
`CLAUDE.md`/`AGENTS.md` is the organisers' doc with known errors — game-model.md wins). New:

- **Python's `random` is NOT seeded by `--seed`** — identical commands diverge. arena.py's
  many-match design absorbs it; single probe runs may need retries.
- **Absolute-direction habits are a bug class**, not a style choice: fixed tie-breaks cost
  games everywhere, invisibly. The arena's per-map mirror seat split is the standing
  regression test — run it on anything that iterates tiles or directions in a fixed order.
- **program.md's accept gate is for strategy changes.** Insurance changes (v2's CPU guard)
  used keep-unless-refuted, stated in advance and documented in the log entry. Don't let that
  become a loophole for strategy tweaks.

## Not done

- Daily retro for 2026-08-06 in the dev-knowledge vault — day wasn't wrapped yet. Two
  patterns from this project are already committed there.
- Still no `git remote`; `results.tsv` still deliberately untracked.
- Remaining unknowns, ranked with methods, in [open-questions.md](docs/open-questions.md):
  ore depletion, enemy-conveyor crediting, `destroy()` refund on dead-end stacks, and the
  platform questions above.
