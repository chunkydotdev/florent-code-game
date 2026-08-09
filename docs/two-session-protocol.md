# Two-session protocol — builder arm + research arm

Born 2026-08-07 (sessions 12/13, the Eir 5 cycle), written up on Magnus's
ask. Two Fable sessions run this project in parallel with disjoint write
surfaces: a **builder arm** (the measuring session, boots from HANDOVER.md)
and a **research arm**. Why it works: context isolation (the builder's
context stays on build/measure cycles; research burns its own on decodes and
fan-outs), parallel throughput (a full research brief executed while Eir 5
was built and shipped), and **independent verification** — the research arm
caught the builder's stale piece-specs against the live source; the builder
caught the research arm duplicating a finished census. Neither catch happens
inside one session.

## Roles

**Builder arm** owns: bot edits and dev dirs (`bots/_*`), arena runs and
batteries, ALL verdicts (KEEP/REFUTED/PARKED — in spitball and on the tape),
ships/submissions/activations and the slot, the tape (`elo_history.tsv`,
`results.tsv`), repo commits, the build queue and its priorities, the four
monitors (arm/re-arm/fix), and HANDOVER.md.

**Push on every commit (Magnus, 2026-08-08).** `git push` immediately after
every commit, no batching — the repo is the backup and a 54-commit unpushed
backlog was found the morning of 08-08. Either arm noticing `ahead of
origin` pushes committed history on sight (pushing is backup, not a
verdict/ownership act).

**Watch state must have a verified wake path (Magnus retro point,
2026-08-08).** Entering watch state requires naming what will actually wake
the arm (a monitor that re-invokes the session, a message, a timer) — a
monitor that only writes files nobody reads is a log, not a wake path. On
the night of 08-07→08 both arms sat blind ~00:30-05:39 while three teammate
versions shipped and the slot bled; teammate uploads are wake events with
the same priority as opponent version bumps.

**Research arm** owns: `docs/research/*` deliverables, replay decodes
(including post-ship production reads), code-reads/specs/pre-mortems,
read-only subagent fan-outs (research briefs), cross-thread synthesis, and
relaying findings with staleness corrections. It NEVER: edits a bot,
submits/activates, runs arena or unrated challenges, writes verdicts,
touches HANDOVER.md or the tape.

**Subagents are pre-authorised for the research arm, permanently (Magnus,
2026-08-09).** No per-session permission, no asking. Announce in IN-FLIGHT
before spawning (rule 1) and relay results before idling (they die with the
session) — those two constraints are the whole ceremony. Prefer several
narrow agents to one broad one.

**Standing mandate — constant tactics research (Magnus, 2026-08-09).** The
research arm is permanently data-hungry: alongside the builder's queue it
continuously mines strategies and tactics from comparable games (Battlecode
above all — this engine is a derivative, its protobuf namespace is literally
`battlecode.*` — plus Screeps, Halite, Terminal, Lux AI, CodinGame,
BattleSnake, AI Challenge) and converts them into things the builder can use.
Mechanically: a sweep launches **at boot**, on **every queue drain** (watch
state is now a sweep, never an idle — and a sweep's completion notification is
itself the wake path rule 3 demands), and **after any measured surprise**.
Topics come from the wheel in `docs/research/tactics/INDEX.md`, which exists so
successive sessions do not re-research the same ground. Findings land as files
there with a source URL, an evidence grade, and an explicit transferability
verdict against our ruleset; **`transfers: no` is a result worth filing**, an
unsourced tactic is pollution.

**The corpus is shared read infrastructure (2026-08-09).** `tools/corpus/`
decodes the whole replay archive in ~3 min and `corpus/` holds the committed
tables (throws, builds/placement, economy/ammo/CPU, our ladder games, a
league-wide 27k-match table, and a `join.tsv` reconciled 1,155/1,155 against
the winner field inside each replay). Both arms read it; research maintains it.
**Query it before writing a new decoder** — the archive had reached 3,831 files
while the largest replay-based read in the repo was 219 games. Traps and
method: `docs/research/corpus-howto.md`.

Both read everything. Spitball stays append-for-anyone, verdict lines
builder-only (unchanged from its rules of the road).

## Channels

1. **research → builder: direct session message** (ListAgents → SendMessage;
   the builder can only reply in the window a ping opens, so pings carry the
   full payload and end with what is pending).
2. **builder → research: dated notes in `docs/coordination.md`** (durable,
   read by design; replaces the coordination sections that bloated spitball
   on day one).
3. **`docs/coordination.md`** is the ops channel: an **IN-FLIGHT registry**
   at the top (one line per commissioned agent/build: who, what, output
   path, download budget — written BEFORE spawning) and chronological dated
   notes below. Spitball returns to pure ideas/findings.
4. **ASK convention**: the builder appends `ASK:` items for the research
   queue. One focused ask sharpens a whole fan-out (the sporks
   screen-trigger ask is the template). Research prioritizes ASKs over its
   own queue.
5. **Process deltas** (retro cadence, Magnus + both arms 2026-08-07): when
   a version's verdict settles, the arm holding the datum appends 1-3
   "process delta" bullets (what slowed us / what to change) to the
   verdict's coordination note. Full retro synthesizes the deltas at
   Magnus's wrap-call (he wraps at least daily); incident-log rules still
   land immediately, not queued for retro.

## Shared platform budget (fcode)

- Builder exclusively: submissions, activations, unrated challenges. Arena
  is local and unmetered.
- Research: replay downloads with a declared per-agent budget, paced
  ≥60-90s, archive-first (`replay_archive/` before any download);
  `match list` / `match info` freely (cheap).
- Nothing platform-touching runs from unattended loops except the four
  monitors (builder-owned).
- The replay archiver is shared read infrastructure: research specs gaps,
  builder fixes them. (The `--mine` priority pass landed 2026-08-07 session
  14 in tools/monitors/replay_archiver.py — a mine-first stable sort; the
  original ours-first block was silently defeated by the newest-first sort.)

## Anti-collision rules (each bought with a real incident — see log)

1. **Announce before spawn.** Every commissioned agent/build gets an
   IN-FLIGHT line first; before commissioning, check the registry AND
   `docs/research/` for existing work. (Bought by: the duplicated census —
   one killed agent, ~30 wasted minutes.)
2. **Version-tag everything.** Every deliverable header carries: our live
   version, the exact bot dirs code-read, opponent versions cited. A claim
   about "the live bot" without a tag is invalid. The relaying arm corrects
   staleness at relay time. (Bought by: the family report calling piece J
   "unshipped" while v65 shipped it mid-decode; denial constants going stale
   across OUR OWN ships twice in one day.)
3. **Ships are announced immediately**: version, contents, baseline row —
   as a coordination note at activation, not just a tape row.
4. **No cross-writes.** Research proposes changes to builder-owned files
   (HANDOVER, tape, bots, monitors) in a note or ping; it never edits them.
   Same in reverse for `docs/research/*`.
5. **One research arm at a time.** Wider parallelism = subagent fan-outs
   commissioned by an arm (the research-brief pattern), never a third peer
   session.

## Post-ship division of labor

Builder: pre-ship arena gate (matched-noise battery), baseline row,
~20-match trajectory read, rollback criteria on the tape. Research:
**production mechanism read** from the first class-relevant replays —
per-piece checks against pre-ship baselines (the v65 read,
`docs/research/v65-production-read-2026-08-07.md`, is the template) — plus
re-extraction of any opponent-script constants after ships that touch
early-game behavior (deterministic opponents re-seed on OUR version).

## Boot sequences

- **Builder**: HANDOVER.md, unchanged (it links here from its operating
  notes).
- **Research**: (1) auto-memory points here; (2) `docs/coordination.md`
  tail — IN-FLIGHT registry + open ASKs; (3) spitball tail for fresh ideas;
  (4) ListAgents → handshake ping to the builder ("research arm online,
  picking up X"); (5) `docs/research/` for the current deliverable set.
- **Research session death/compaction**: subagent results die with their
  session — relay before idling, and append a "research arm state" note
  (open agents, pending relays) to coordination.md when wrapping.
- **Sessions wrap only on Magnus's explicit call** (directive 2026-08-07
  ~19:47, bilateral ack builder 19:5x). A drained queue = watch state
  (announce blocked, hold), never a self-initiated wrap; wrap mechanics
  (HANDOVER successor block, monitor teardown, research state note) fire
  only on his call. Context: session 13's autonomous wrap killed the
  monitors and left a ~15-min unwatched ladder gap.

## Incident log — 2026-08-07 (why the rules above exist)

- Census duplicated (rule 1): research commissioned a meta census the
  builder had committed 40 minutes earlier; killed on the builder's board
  note.
- Spec race (rule 2): the family cross-check code-read `_v74e4` while
  `_v75e5` shipped mid-flight; its "J unshipped" claim was stale on arrival
  and corrected at relay.
- Constants expire with our ships (rule 2 + post-ship split): Ouroboros
  denial tiles diverged across our v53/55/59 → v64 → v65 eras; confirmed
  twice in one day (the adjudication, then the fresh v65 meander game
  within the hour).
- Archiver gap (shared-infra clause): our own Memtrace match never archived;
  research pulled directly (2s-paced) and spec'd the `--mine` fix.
- Tooling footnote: zsh `nomatch` inside a background watcher loop burned a
  silent 30 minutes — poll with `ls | grep -q`, never bare globs.
- Tooling footnote 2 (research, session 14): zsh does NOT word-split unquoted
  variables — a watcher's `for id in $ids` (ids from a variable) looped ONCE
  over the whole string and its grep never matched, producing a false
  "nothing archived" warning 75 minutes later while every watched file was
  present. In watcher scripts: iterate literal lists, or use `${=ids}` /
  arrays. Detection false-negatives look identical to the watched event not
  happening — verify a watcher's first positive detection manually before
  trusting its silence.
- Determinism assumed (research, session 13): the K-diag divergence read
  treated same-seed arena pairs as deterministic and called their r0
  spawn divergence a base-refactor defect; piece G's UNSEEDED spawn salt
  (main.py:1082, HANDOVER MEASUREMENT WARNING) makes paired-seed runs
  nondeterministic BY DESIGN. Builder caught it within minutes; deliverable
  corrected in place. RULE: HANDOVER's measurement warnings bind research
  decodes of arena-produced artifacts — before attributing anything from
  paired replays, check NOISE_ON provenance; salt-dependent observations
  (openings, small-n outcomes) attribute nothing, salt-independent
  aggregates (action mixes, target classes) remain valid.
