# Multi-session protocol — builder · research · side lane

Born 2026-08-07 (sessions 12/13, the Eir 5 cycle), written up on Magnus's
ask. Fable sessions run this project in parallel with disjoint write
surfaces: a **builder arm** (the measuring session, boots from HANDOVER.md)
and a **research arm**. Why it works: context isolation (the builder's
context stays on build/measure cycles; research burns its own on decodes and
fan-outs), parallel throughput (a full research brief executed while Eir 5
was built and shipped), and **independent verification** — the research arm
caught the builder's stale piece-specs against the live source; the builder
caught the research arm duplicating a finished census. Neither catch happens
inside one session.

**⭐ AMENDED 2026-08-13 (Magnus: "apply your fixes", acting on
`docs/workflow-analysis/lane-structure-review-2026-08-13.md`). THREE lanes,
not two.** The side lane was commissioned 2026-08-09 and this doc never got a
Roles entry for it — the review found the lane ran four days on an exception
clause (rule 5) alone. **Charters are AUTHORITATIVE in
`.claude/commands/{builder,research,sidelane}.md` — this doc is the map, those
files are the law.** The 2026-08-13 endgame recharter: **research =
live-measurement operator** (unrated-fixture cadence plan, pooled readouts,
decode of our own rated games, opponent-version pinning — still never fires a
platform action) and **side lane = ship-critical verification only**. Boot
enforcement is now a SessionStart hook: it names your lane from `FCODE_LANE`
or reminds you that charters are not auto-loaded.

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
touches HANDOVER.md or the tape. **Since 2026-08-13 it is additionally the
LIVE-MEASUREMENT OPERATOR — it owns the unrated-fixture cadence plan (which
leg fires each rate-limit window, pooled across windows), the pooled
readouts, the decode of our own rated games, and opponent-version pinning.
The builder still executes every platform action; research schedules and
reads.** Authoritative charter: `.claude/commands/research.md`.
**Leg accounting rule (completes-only; promoted here s37, 2026-08-13 — it
lived only in research's working rules and `panel_read` while three lanes
depended on it):** a fired match is REGISTERED off `fcode match info` at fire
time, never inferred later from `match list` — `match list` shows COMPLETED
matches, so **absence from the list is not evidence a challenge was never
accepted** (the s36 "phantom leg" near-miss: an accepted, in-flight match read
as nonexistent for the minutes it was pending). Any leg or panel count quoted
without a fire-time registration behind it says so inline.

**Side lane** (commissioned by Magnus 2026-08-09; this Roles entry added
2026-08-13 — the lane ran four days without one) owns: **ship-critical
verification** — two-clock prereg certification, gate and stop-loss
arithmetic, rated-leak checks at the pairing boundary, rollback readiness —
plus prereg hygiene for live legs, auditing ship-chain commits against
PROGRAMME.md. Since 2026-08-13 it does NOT audit every commit or every
analysis doc (review R1: its detection was the best-measured value in the
record — 16/16 real flags at ~2-minute median on 08-13 — and its volume was
the cost, 1.4–7× more channel lines than any other lane on every day it ran).
Hard limits unchanged from the rule-5 contract: no bot edits, no
arena/unrated, no verdicts, no HANDOVER/tape writes, append-only
coordination notes, commits its own named files only. Authoritative charter:
`.claude/commands/sidelane.md`.

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

**⛔ AMENDED 2026-08-12/13 — the TRIGGER and OUTPUT CONTRACT above are
RETIRED.** Research measured its own flagship at **313 files → 7 conversions →
0 decision-path citations** and retired unconditional sweeping (s33, Magnus
directive). Sweeps now fire on a **signal** (queue below floor, measured
surprise), never on boot or a schedule, and a sweep's only deliverable is a
`QUEUE.md` row that clears admission — or nothing. The authoritative version
is in `.claude/commands/research.md`; the paragraph above is kept for history
and must not be booted from.

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
6. **Consumption receipts (2026-08-13, review R6).** The builder answers
   every relayed finding with one line in the same channel: `CONSUMED: <what
   changed>` or `KILLED: <why>`. What this closes, measured: 32.6% of
   research docs self-disclaimed that they change anything, and a correct
   hand-off was indistinguishable from a dropped one — four redo clusters,
   9,134 lines, two same-question duplicates written 21 and 92 minutes apart
   with zero cross-citation.

**Channel reality check (2026-08-13):** the top-of-file IN-FLIGHT registry
fossilised on 2026-08-08 (its rows still name v67-era work) and the `ASK:`
convention last fired operationally on 2026-08-10. The working channels are
the coordination TAIL plus session pings. Announcements as dated tail notes
are fine — that is what everyone already does — but a session message that
changes anything must land as a committed note the same hour.

## Session models and effort (recommendation recorded 2026-08-13, Magnus's ask)

**Honest caveat first: no measured tier comparison exists in this repo — this
is judgment from each lane's recorded failure classes, not an A/B.** The
binding constraint is the machine's token budget (Magnus, 08-12).

- **Builder: Fable, xhigh effort.** The only lane whose errors convert
  directly to rating (verdicts, ships, the slot), and its recorded failure
  mode — errors that run toward the work it wants to do next — is exactly
  what more deliberation helps.
- **Side lane: Fable, high–xhigh.** Its whole value is subtle statistical
  detection (optional stopping vs multiplicity, a stop-loss that can never
  fire, estimator divergence on the load-bearing step). Downgrading the
  detector saves tokens where the record says the value is.
- **Research (operator charter): Opus, high.** The 2026-08-13 charter is
  operator-shaped — fire orders, pooled readouts, decode, pinning — method
  discipline more than frontier judgment. Upgrade to Fable on days that are
  genuinely synthesis/judge-panel shaped, if budget allows.
- **Subagents: unchanged standing rule** — model always explicit, `opus` for
  judgment, `sonnet` for mechanical work with a validated method, never
  inherited.
- **Ephemeral auditors: Fable xhigh with opus subagents** — the stakeless
  one-shot question is where frontier judgment pays most per token.

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
   commissioned by an arm (the research-brief pattern), never a
   *self-appointed* third peer session. **AMENDED 2026-08-09 (Magnus,
   via the process-review adoption): a THIRD LANE is sanctioned when and
   only when Magnus commissions it.** Its contract, from the pattern that
   worked on 2026-08-09: boot from the coordination tail; announce lane +
   scope there before doing anything (append-only — never edit the arms'
   content); write ONLY new files under `docs/research/`; no bot edits, no
   arena/unrated, no verdicts, no HANDOVER/tape writes; engine probes stay
   with the builder; commit only its own named files (never `add -A`); push
   every commit; relay subagent output before idling. Its high-value loop is
   adversarial peer review with the research arm — discriminating cuts +
   placebo arms exchanged BEFORE any observational finding becomes a build
   input. A peer arm cannot widen the lane; only Magnus can.

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

## Context-ceiling REBOOT SEAM (Magnus, 2026-08-09) — distinct from the wrap

The failure this prevents: **compaction hitting MID-CYCLE**, leaving a
half-finished plank/sweep/analysis whose state lived only in context, so the
lossy summary can't reconstruct it. The fix is to wrap at a CYCLE BOUNDARY
before context fills, giving a clean seam a fresh session continues from.

**This is NOT the end-of-day wrap.** The wrap is a retro (process deltas,
HANDOVER re-prioritisation) and fires only on Magnus's call. The reboot seam is
a **fast state SNAPSHOT to continue the same work** — no retro, no HANDOVER
rewrite. Do not conflate them (the recurring wrap-vs-daily-note confusion, one
level up).

**The gauge and threshold:** a model cannot precisely read its own remaining
context, so the trigger is external — **Magnus watches the three meters**.
**~80% is the seam line** (leaves headroom to execute the seam before the
harness auto-compacts, and it is roughly the "can't fit another full cycle"
line — below ~75% wastes headroom, above ~85% risks compaction mid-seam).
Per-role: the **builder trips ~75%** (biggest cycles — a whole battery — and
the most dangerous mid-cycle state, so it needs the most margin); the **side
lane can run ~85%** (cheap snapshots, no monitors). Each session also
self-flags natural boundaries as good reboot points.

**Reboot as a BARRIER, not a guillotine:** the first arm to its line signals
`READY FOR REBOOT` and drops to watch-state (no new cycles, only tiny closeable
tasks); the other two finish their CURRENT cycle to a boundary, snapshot, and
signal; once all three have signalled, Magnus reboots all together. This keeps
reboots synchronised (no cross-session staleness, one clean seam) without
yanking anyone mid-cycle. In practice the builder trips first and paces it,
which is correct — it is the session you most want caught at a boundary.

**Monitoring survives resets (2026-08-09):** the status/Elo logger, both match
watchers, the replay archiver, and the keeper all run detached (PPID 1), so a
reboot no longer creates the session-13 blind ladder gap. The seam therefore
does NOT re-arm monitors from scratch — it only **verifies the persistent
monitors are alive** (`ps`/keeper.pid) and names any that died. (Residual to
confirm: their STATE_DIR dedup files may be session-scoped — a process
surviving is not the same as its threshold state surviving; check on boot.)

**The decision rule (self-governed, near the ceiling):** do NOT start a cycle
you cannot finish in the remaining context. Prefer closing small tasks and
snapshotting over opening a new plank/sweep/deep-decode that compaction would
guillotine. A started-and-cut cycle is worse than a not-started one.

**The seam wrap, per session, one cheap pass (on Magnus's call or at a flagged
boundary):**
1. **Commit + push everything** — zero uncommitted state (the repo is the seam).
2. **Kill/relay live subagents** — they die on reboot; fold results into a
   committed doc or state they were dropped.
3. **One `REBOOT STATE` block in coordination.md**: the cycle just closed, the
   **single next action** verbatim, any in-flight-but-durable pointers, and the
   **boot pointer** (which files the fresh session reads to resume). Not a
   retro — three or four lines.
4. **Emit `READY FOR REBOOT — <one-line pointer>`** so Magnus knows the seam is
   clean and can reboot all sessions.

**The boot side:** a rebooted session reads its boot pointer (coordination tail
+ its `REBOOT STATE` block + its committed deliverables) and resumes the named
next action — same work, fresh context, nothing lost because nothing was
mid-flight. Side lane boots per its auto-memory pattern; builder per HANDOVER;
research per its boot sequence — all then read the latest `REBOOT STATE`, and
verify the detached monitors are alive.

**What still does NOT survive a reset** (so the seam must respect it): a
running arena BATTERY (the builder wraps at a battery boundary, never
mid-battery), the active-submission SLOT state, and any live SUBAGENT (fold its
result into a committed doc or state it was dropped). Monitoring is now the
exception, not the rule — everything else is either committed to the repo or
lost.

## Ephemeral auditors, and the directive rules (2026-08-13, review R5)

**No fourth standing lane.** `tools/audit_trigger.py:11-15` predicted — the
day before the side lane was created — that a permanent auditor would
eventually acquire a stake; the side lane confirmed it from the inside
(*"auditing is a defending state"*, its own retro). One-shot questions get an
**ephemeral, stakeless session**: boot from the coordination tail, announce
lane + scope there (rule 1), read-only or own-named-files-only, relay, and
terminate. The 2026-08-13 lane-structure review is the worked example.

**Directive admission bar.** A new standing directive must name its enforcing
surface — a blocking script/hook, or a file some boot sequence opens — or it
is filed as `OBSERVATION — NOT ROUTED`, not a directive. This is the retro
routing rule applied to directives themselves. Measured basis: every
prose-only rule in this repo has a recorded violation by its own author; the
durable surfaces are booted files and tools that exit 1.

**Directive sunset.** A prose directive that has not changed behaviour in two
successive retros is deleted or demoted to observation — the clause every
retro instrument already carries, now pointed at the directive stock. Basis:
the stock reached 36+ D-rules with cross-lane numbering collisions nobody
flagged, boot reads cost ~100k tokens/session
(`docs/research/BOOT-LOAD-AUDIT-2026-08-10.md`), and that audit's own cut
list sat 3 days unexecuted — the stock ate its own pruning directive.

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
