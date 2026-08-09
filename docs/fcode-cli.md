# `fcode` CLI reference

Verified against the **installed package**, `fcode` 2.3.6, at
`.venv/lib/python3.13/site-packages/fcode/`. Every path below is relative to
that directory unless stated otherwise. The engine itself
(`fcode_engine.cpython-313-darwin.so`) is compiled and opaque; everything else
— CLI, commands, packaging — is plain Python and was read in full.

**Verification standard**: every claim here either cites `file.py:line` in
the installed package, or is explicitly sourced to something else (the
organizers' own docs at `docs/reference/official-docs.md`, or this project's
own prior empirical logs — `docs/tooling.md`, `HANDOVER.md`,
`docs/coordination.md`) and flagged as such, or is marked `UNVERIFIED`. The
organizers' docs are **not** the installed package — they describe intended
server behavior, and at least one load-bearing claim in them is contradicted
by measured platform behavior (see Trap 1). Treat citations to
`official-docs.md` as secondary, same skepticism as project `CLAUDE.md`.

This doc complements `docs/tooling.md` (local harness / engine gotchas) and
does not repeat its content — see there for TLE, replay decoding, determinism,
and the engine-stub bugs. It focuses on the CLI's platform-facing commands.

---

## TRAPS — read this before running anything

1. **`submission activate` really can be blocked — and the organizers' own
   docs are misleading about why you'd need it at all.** The CLI itself
   refuses to activate unless the target submission's `status == "ready"`
   (`fcode/commands/submission.py:203-208`); a submission sitting in
   `flagged` (held for the platform's automated security audit) or
   `processing`/`rejected`/`error` cannot be activated. **But this block is
   irrelevant to shipping a new bot.** `submission upload` (and its alias
   `submit`) is never gated by that check — it always succeeds once the zip
   passes upload, and the platform **auto-activates** a freshly-ready
   submission with no separate `activate` call, confirmed across many
   independent ships in this project's own logs (`docs/tooling.md:490-497`,
   `HANDOVER.md:168-172`, `docs/coordination.md:8500-8501`). The organizers'
   docs (`docs/reference/official-docs.md:759-763`) say "set the active
   version with `fcode submission activate VERSION`" as if it's required —
   **that line is what caused the false belief that shelved a night of
   work.** `activate` only matters for *reactivating an old, already-uploaded*
   submission (rollback); it is never on the path for shipping something new.
   See "The submit-vs-activate question" below for the full resolution.
2. **`teamARating`/`teamBRating` in any `match` JSON is a LIVE JOIN**, not
   the rating at match time — same value on every historical row for a given
   team. Use `ratingABefore`/`ratingBBefore` instead, which reconcile to
   eleven decimals against `eloDelta` (verified:
   `docs/coordination.md:8594-8597`, `docs/research/at-match-rating-2026-08-09.md`).
   Neither field is readable in CLI source — both are opaque server JSON the
   CLI only echoes; this is empirical, not source-derived.
3. **`match info --json` returns the opponent's submission version as
   `null`**, every row (empirical, not a CLI-source finding — the server
   assembles this payload). `match list --json` does **not** have this bug —
   it carries both `teamAVersion`/`teamBVersion`, confirmed populated on
   482/482 rows in the same research pass
   (`docs/research/kill-game-split-recompute-2026-08-09.md:19-27`,
   `docs/research/opponent-constants-v80-2026-08-09.md:15-22`). Join on
   `match list`, not `match info`, if you need the opponent's version.
4. **`fcode match test` zips local bots with NO junk-exclusion filtering.**
   `submission upload`'s zip-builder (`_make_zip`,
   `fcode/commands/submission.py:57-84`) strips `.git/`, `__pycache__`,
   `.DS_Store`, etc. via `_is_junk` (lines 18-54). `match test`'s zip-builder
   (`_zip_bot`, `fcode/commands/test_run.py:18-48`) has no such filter — it
   walks the whole directory with plain `os.walk` and writes every file
   (lines 32-36). A stray `.git/` or editor cache rides along into a
   `match test` run but would be stripped from a real submission.
5. **Junk-exclusion in `submission upload` only fires when the CLI builds
   the zip from a *directory*.** If you hand it an already-built `.zip` file,
   it's uploaded byte-for-byte with **zero** filtering
   (`fcode/commands/submission.py:75-76`, plain passthrough
   `bot_path.read_bytes()`). Only the directory path
   (`fcode/commands/submission.py:59-73`) runs `_is_junk`.
6. Platform timestamps are UTC; local machine is CEST (UTC+2). Already
   covered in `docs/tooling.md`'s timezone section — don't re-derive it here,
   just remember it applies to every date field below too.
7. Rate limit **5 matches per 10 minutes per account**, shared between
   `match test` and `match unrated` — confirmed in the organizers' docs
   (`docs/reference/official-docs.md:976`, `:1843`, `:1861`), **not** present
   anywhere in the installed CLI package (only a generic 429 handler,
   `fcode/api.py:39-40`, with no numbers). See "Rate limits" below for the
   verification nuance.
8. `fcode run`'s `--tle` defaults to **0 (disabled)** — no CPU limit locally
   unless you pass it (`fcode/commands/run.py:119`). The ladder always
   enforces 10ms. `docs/tooling.md` already flags this; repeating because
   it's a `fcode run` flag default, in scope for this doc.

---

## Global behavior

| Aspect | Behavior | Source |
|---|---|---|
| Credentials | `~/.fcode/credentials.json`, mode `0o600`, holds `token`/`expires_at`/`user`/`team` | `fcode/auth.py:6-28` |
| API base URL | `https://game.code.florent.vc`, override via `FCODE_API_URL` env var | `fcode/auth.py:9-15` |
| Update check | On every invocation (unless `FCODE_NO_UPDATE_CHECK` set), GETs `pypi.org/pypi/fcode/json`, caches 300s at `~/.fcode/version_cache.json`. External network call, not to the platform; never raises. | `fcode/cli.py:16-19`, `fcode/version_check.py` |
| `--version` | Reads installed package version via `importlib.metadata`; no network call. | `fcode/cli.py:13`, `fcode/__init__.py:1-3` |
| `fcode.toml` | Per-project config: `bots_dir` (default `bots`), `maps_dir` (default `maps`), `replay` (default `replay.replay26`), `seed` (default `1`). Found by walking up from cwd. | `fcode/config.py` |
| Error display | 401 → "Session expired"; 429 → "Rate limited: {msg}" (msg from server body, no number hardcoded); 404 → "Not found"; other → generic. All raise `SystemExit(1)`. | `fcode/api.py:30-45` |
| `fcode <group> <id>` shorthand | `match` uses a `SmartGroup`: an unrecognized first token is routed to the group's default subcommand (`info` for `match`). So `fcode match abc123` == `fcode match info abc123`. | `fcode/compat.py:21-36`, `fcode/commands/match_group.py:11` |

---

## Command inventory

**Mutates platform state** = changes something visible to other teams or to
the ladder/rating/submission system on the server. Writing local files
(replays, maps, credentials, config) is never counted as platform-mutating
here even where noted.

| Command | Mutates platform? | Source | One-line |
|---|---|---|---|
| `fcode run` | **READ-ONLY** (fully local) | `commands/run.py` | Local match via the compiled engine |
| `fcode watch [FILE \| --match ID]` | **READ-ONLY** | `commands/watch.py` | Open a replay (local file or browser to platform visualiser) |
| `fcode login` | Local-only (writes credential file); server issues a session, not game/ladder data | `commands/login.py` | Browser OAuth flow |
| `fcode logout` | Local-only (deletes credential file) | `commands/logout.py` | Clear stored credentials |
| `fcode starter [DIR]` | Local-only (scaffolds files; reads map pool if logged in) | `commands/starter.py` | Scaffold a project |
| `fcode status` | **READ-ONLY** | `commands/status.py` | Team/rating/rank/active-submission summary |
| `fcode map-editor [--platform]` | **READ-ONLY** | `commands/map_editor.py` | Open the map editor (local server or browser) |
| `fcode submit PATH [--name]` | **MUTATING** — creates a new submission (alias for `submission upload`) | `cli.py:50-59` → `commands/submission.py:97-135` | Upload a bot |
| `fcode submission upload` | **MUTATING** | `commands/submission.py:93-135` | Same as `submit` |
| `fcode submission list` | **READ-ONLY** | `commands/submission.py:138-180` | List your team's submissions |
| `fcode submission activate VERSION` | **MUTATING** — changes which submission plays the ladder | `commands/submission.py:183-221` | Reactivate an older submission |
| `fcode submission rename VERSION NAME` | **MUTATING** (metadata only, no ladder effect) | `commands/submission.py:224-249` | Rename a submission |
| `fcode submission download [VERSION]` | **READ-ONLY** (writes a local file) | `commands/submission.py:252-293` | Download a submission zip |
| `fcode match info ID` (default) | **READ-ONLY** | `commands/match_detail.py` | Detailed match view incl. per-game breakdown |
| `fcode match list` | **READ-ONLY** | `commands/matches.py` | List/filter matches |
| `fcode match unrated OPPONENT_ID` | **MUTATING** — queues a real match on real hardware (no rating effect) | `commands/test.py` | Scrimmage another team |
| `fcode match test BOT_A BOT_B` | **MUTATING** — queues a real match on real hardware (no rating effect) | `commands/test_run.py` | Remote local-bot-vs-local-bot test |
| `fcode match replay ID` | **READ-ONLY** (writes local files) | `commands/match_group.py:96-140` | Download replay(s) |
| `fcode match watch ID` | **READ-ONLY** | `commands/match_group.py:145-159` | Open match in browser visualiser |
| `fcode match tests` | **READ-ONLY** | `commands/test_matches.py` | List your remote test runs |
| `fcode team search QUERY` | **READ-ONLY** | `commands/team_group.py:20-53` | Search teams |
| `fcode team info TEAM_ID` | **READ-ONLY** | `commands/team_group.py:56-86` | Team profile |
| `fcode ladder` | **READ-ONLY** | `commands/ladder.py` | Ladder rankings |
| `fcode maps list` | **READ-ONLY** | `commands/maps.py:71-112` | Show map pool vs local copies |
| `fcode maps sync` | Local-only (downloads files; reads platform) | `commands/maps.py:115-122` | Pull the current map pool |

Hidden/deprecated aliases (all print a one-time warning, then delegate to the
same code paths above): `matches` → `match list`, `unrated` → `match
unrated`, `test-run` → `match test`, `test-matches` → `match tests`, `teams`
→ `team`, `init` → `starter` (`fcode/cli.py:61-134`, `fcode/compat.py:11-18`).
Mutation status is identical to the command they delegate to.

**Every command marked MUTATING above is a "DO NOT RUN" command under this
project's working rules for a read-only research task** — this doc only
documents them; none were executed to produce it.

---

## Auth & session

`fcode login` opens `{api_url}/cli/auth?port=<local>&state=<random>` in a
browser, runs a one-shot localhost HTTP server to catch the callback
(`code`, `state`), verifies `state` matches (CSRF guard), then POSTs
`{code}` to `/api/cli/exchange` and stores the returned `token` /
`expires_at` / `user` / `team` (`commands/login.py:47-136`). Confirmation
prompt "Log in again?" is skipped with `--yes`/`-y`, or if not already logged
in. Timeout: 120s waiting for the browser callback (line 75).

`fcode logout` deletes `~/.fcode/credentials.json` if present; no server
call (`commands/logout.py`, `fcode/auth.py:40-42`).

`fcode status [--json]` — **READ-ONLY**, makes up to 4 GETs
(`/api/teams/{id}`, `/api/ladder`, `/api/submissions`,
`/api/matches?teamIds=...&limit=10`), each independently try/excepted so a
partial outage still shows what succeeded (`commands/status.py:61-114`).
Rank tiers (Bronze .. Legendary Grandmaster, `<100` matches = "Unranked") are
hardcoded client-side (`commands/status.py:14-34`) and explicitly noted in
the source comment as needing to stay "in sync with shared/src/ranks.ts" — a
server file we cannot see, so treat displayed tier names as approximate if
the server-side thresholds ever move.

---

## Submissions

### Packaging (`submission upload` / `submit`)

`PATH` may be a directory, a `.py` file, or a `.zip`. Behavior differs by type
(`commands/submission.py:49-84`):

| Input | Behavior | Junk filtering? |
|---|---|---|
| Directory | Must contain `main.py` at its root or upload fails client-side (`click.BadParameter`). CLI builds the zip itself, walking the tree. | **Yes** — see below |
| `.zip` file | Read and uploaded **as-is**, `bot_path.read_bytes()`. | **No** |
| `.py` file | Zipped as a single file renamed to `main.py`. | N/A (single file) |

Junk exclusion (only applied on the directory path,
`fcode/commands/submission.py:18-54`, `_is_junk`):

```
_JUNK_DIRS = {"__pycache__", ".git", ".svn", ".hg", ".idea", ".vscode",
              ".mypy_cache", ".pytest_cache", ".ruff_cache", "__MACOSX",
              ".tox", ".eggs", ".nox"}
_JUNK_FILES = {".DS_Store", "Thumbs.db", "desktop.ini", ".thumbs",
               "ehthumbs.db", "ehthumbs_vista.db", ".Spotlight-V100",
               ".Trashes", ".directory"}
_JUNK_EXTENSIONS = {".pyc", ".pyo"}
```

Also excluded: any file whose name starts with `._` (AppleDouble resource
forks), and any file under a directory whose name is in `_JUNK_DIRS` at any
depth (`path.parts` check, line 54) — not just top-level.

No client-side size/file-count checks exist anywhere in `_make_zip`. The
organizers' documented upload limits (5MB zip, 50MB decompressed, 500 files,
no native extensions, no path traversal) are enforced **server-side only**
(`docs/reference/official-docs.md:736-746`) — a bot that's too big fails
*after* upload, not before.

`fcode submit PATH [--name]` is a thin wrapper that calls
`submission upload` with the same args (`fcode/cli.py:50-59`).

### `submission list [--json]`

**READ-ONLY**, `GET /api/submissions`. Table/JSON fields the CLI touches:
`version`, `name`, `status`, `isActive`, `submittedByName`, `uploadedAt`
(`commands/submission.py:140-180`). `--json` dumps the raw `submissions`
array from the server verbatim — it may contain more fields than the ones
listed; only these are read/rendered by the CLI itself.

### `submission activate VERSION [--json]`

Looks up the submission by `version` in the same `/api/submissions` list,
then:
1. If not found → error, `SystemExit(1)`.
2. **If `status != "ready"` → refuses, `SystemExit(1)`**, message: `Version {v}
   has status '{status}' — only ready submissions can be activated.`
   (`commands/submission.py:203-208`). This is the real, source-confirmed
   gate — it blocks exactly the case where a submission is still `processing`
   or `flagged` (held for the platform's automated security audit per
   `docs/reference/official-docs.md:748-757`), or is `rejected`/`error`.
3. If already active → no-op, reports `already_active: true`.
4. Otherwise `POST /api/submissions/activate {submissionId}` —
   **MUTATING**, this is what makes an older submission live again (rollback).

**Rollback procedure, definitively**: `fcode submission list` to find the
target `version`, confirm its `status == "ready"`, then
`fcode submission activate VERSION`. If the target is not `ready` (rare for
an already-once-active submission, but possible under a platform freeze —
`docs/reference/official-docs.md:765-769` — or if it's since been flagged),
`activate` will refuse and there is no CLI workaround; re-upload the same
bytes as a new submission instead (which the project's own logs record as
the practical fallback: `HANDOVER.md:170-172`, "roll back by re-uploading the
predecessor's bytes").

### `submission rename VERSION NAME [--json]`

**MUTATING** (cosmetic only — no ladder/rating effect).
`POST /api/submissions/rename {submissionId, name}`
(`commands/submission.py:224-249`).

### `submission download [VERSION] [--output FILE]`

**READ-ONLY**. Defaults to the active submission if `VERSION` omitted, else
the first `status == "ready"` one, else errors
(`commands/submission.py:255-281`). Fetches a signed URL via
`GET /api/submissions/download` then `urllib.request.urlretrieve`s it to
`v<VERSION>.zip` (or `--output`). No `--json` flag exists on this command.

### The submit-vs-activate question, resolved

**`fcode submit` (== `submission upload`) is never blocked by the `status`
check that gates `activate`.** Upload always attempts the multipart POST
regardless of any prior submission's state (`commands/submission.py:97-126`
has no status check at all — it can't, there's no prior submission to check
against a brand-new upload). The `status != "ready"` gate lives exclusively
inside `activate` (`commands/submission.py:203-208`) and only ever blocks
*that* command, on *existing* submissions.

Separately — and this is **not visible in CLI source, purely server-side
behavior** — a freshly-uploaded submission that reaches `ready` becomes the
active one automatically, with no `activate` call needed. This is not a
one-off observation: it's recorded independently across multiple ships in
this project's own logs (`docs/tooling.md:490-497` — v81 and v82 both went
active on upload; `HANDOVER.md:168-172`; `docs/coordination.md:8500-8501` —
v87 "AUTO-ACTIVATED... the upload IS the ship";
`docs/workflow-analysis/instrument-audit-2026-08-08-late.md:270`). Each of
these was caught by the project's own `elo_logger` noticing a version change
on the ladder with no corresponding `activate` invocation in the operator's
command history — about as strong as empirical confirmation gets without
being able to read the server's source.

**This directly contradicts the organizers' own docs**
(`docs/reference/official-docs.md:759-763`: "Only one version is active at a
time... Set the active version with `fcode submission activate VERSION` or
the Set as Active option on the web Submissions page") — that text reads as
if activation is a required, separate step for *every* upload. It isn't, for
the common case. **The organizers' docs are the source of the false belief
this doc exists to prevent**, not the CLI or the platform's actual behavior.

**Bottom line**: to ship a new bot, `fcode submit <path>` is sufficient and
sufficient alone. `fcode submission activate VERSION` is a separate,
CLI-gated tool needed only to reactivate a *previously uploaded* version —
i.e., for rollback, never for a fresh ship.

---

## Matches

### `match info ID [--json]` (default subcommand of `match`)

**READ-ONLY**. `GET /api/matches/{id}`. `--json` dumps `{"match": ..., "games":
[...]}` verbatim. Fields the formatted view reads from `match`: `status`,
`stage`, `triggeredBy`, `rated`, `scoreA`, `scoreB`, `teamAName`/`teamBName`,
`teamAId`/`teamBId`, `winnerId`, `sourceMatchAId`/`sourceMatchBId`,
`eloDeltaA`/`eloDeltaB`, `createdAt`, `completedAt`, `errorMessage`
(`commands/match_detail.py:44-138`). From each `games[]` entry: `gameNumber`,
`mapName`, `winnerId`, `winCondition`, `turnsPlayed` (lines 157-172).
**Trap**: the opponent's submission version is `null` in this payload — see
Trap 3 above. Not fixable client-side; join `match list` instead.

### `match list [--type ladder|unrated] [--team] [--mine] [--limit N] [--cursor C] [--json]`

**READ-ONLY**. `GET /api/matches` with `limit` (capped to 100 client-side,
`commands/matches.py:17`), optional `type`, `teamIds` (resolved from
`--team` via `/api/teams/search`, falling back to treating the string as a
raw team ID if no search hit, lines 27-39), and `cursor` for pagination.
`--json` dumps `{"matches": [...], "next_cursor": ...}`. Fields read for the
table: `teamAName`/`teamBName`, `teamAId`/`teamBId`, `sourceMatchAId`/
`sourceMatchBId`, `winnerId`, `scoreA`/`scoreB`, `status`, `id`,
`completedAt`/`createdAt`, `triggeredBy` (`commands/matches.py:73-111`).
**Confirmed by this project's own research** to also carry
`ratingABefore`/`ratingBBefore` (at-match rating, not touched by the CLI's
own rendering but present in the raw JSON — `docs/coordination.md:8594-8597`)
and `teamAVersion`/`teamBVersion` (both populated, unlike `match info`'s
opponent-version bug — `docs/research/opponent-constants-v80-2026-08-09.md:21-22`).

### `match unrated OPPONENT_ID [--match SOURCE_MATCH_ID] [--map NAME ...] [--json]`

**MUTATING** — queues a real match, does not affect rating.
`POST /api/matches/unrated {opponentTeamId, sourceMatchId?, mapNames?}`
(`commands/test.py:13-42`). Note what is **not** in that body: no bot upload,
no submission-version selector for *your own* side. Confirmed by the
organizers' docs (`docs/reference/official-docs.md:962`): "Requests a
friendly, non-rated match against another team **using your currently active
submission**." And for the opponent
(`docs/reference/official-docs.md:1853`): "By default your submission
plays against the opponent's **latest ready submission**; pass `--match
<match-id>` to instead play against whichever submission they had in a
specific past match."

**This confirms the belief in full: `unrated` always plays your currently
ACTIVE submission** (there is no way to pass a candidate bot to this
command — it isn't a local file argument at all) **against the opponent's
active/ready submission (or a historical one via `--match`).** Consequence
unchanged from the working belief: "test candidate X on unrated while bot Y
holds the ladder" is not possible — activating X to test it on unrated *is*
activating it for the ladder too. It's alternation, never parallel A/B.
Up to 5 `--map` values; omitted → 5 random maps (`--map` capped at slicing
`maps[:5]`, not validated further client-side).

### `match test BOT_A BOT_B [MAPS...] [--json]`

**MUTATING** — queues a real match on real hardware, does not affect rating.
Both `BOT_A` and `BOT_B` are packaged **locally** and uploaded as
`bot_a`/`bot_b` multipart fields to `POST /api/matches/test-run`
(`commands/test_run.py:51-120`). **There is no opponent-team parameter
anywhere in this command** (contrast with `unrated`'s `opponentTeamId`) —
confirming the belief that `match test` is local-bot-vs-local-bot only and
structurally cannot supply a real opponent's submission. `MAPS` positional,
max 5 (client-side check, `commands/test_run.py:75-80`, raises before any
upload happens); each resolved via `resolve_map_path`
(`commands/run.py:66-86`) against the project's `maps_dir`. See Trap 4 for
the missing junk-filter on this path's zip-builder.

### `match replay ID [--game N] [--output FILE]`

**READ-ONLY**. `GET /api/matches/{id}` to enumerate games, then
`GET /api/matches/replay?matchId=&game=` per game to get a signed URL, then
`urlretrieve`s each to `<matchId>_game_<N>.replay26` (or `--output` if a
single game). No `--json` flag (`commands/match_group.py:96-140`).

### `match watch ID [--game N]`

**READ-ONLY**. Just opens `{api_url}/visualiser?matchId=&game=` in the
default browser — no API call at all (`commands/match_group.py:145-159`).

### `match tests [--limit N] [--json]`

**READ-ONLY**. `GET /api/matches/test-runs`, client-side sliced to `--limit`
(`commands/test_matches.py:14-17`, note: sliced *after* fetch, no `limit`
param sent to the server).

### Rate limits

The installed CLI package contains **no rate-limit numbers anywhere** — the
only rate-limit-aware code is the generic `429` handler in `fcode/api.py:39-40`,
which just prints whatever message string the server sends. The specific
figure comes from the organizers' own docs, in two places that agree with
each other:

- `docs/reference/official-docs.md:976` (CLI reference, `match test`): "Rate
  limit: 5 matches per 10 minutes per account."
- `docs/reference/official-docs.md:1843` (`match test`, narrative): "Rate
  limit: 5 per 10 minutes per account, shared with unrated challenges."
- `docs/reference/official-docs.md:1861` (`match unrated`, narrative): "Rate
  limit: 5 per 10 minutes per account, shared with remote test matches — each
  unrated challenge and each `fcode match test` run counts against the same
  10-minute bucket."

**Verdict: CONFIRMED, but by the organizers' documentation, not by the
installed package.** The project's prior "measured-but-source-unconfirmed"
belief of 5-per-10-minutes is exactly right, and the source (in the broader
sense — the organizers' own published reference, which is authoritative for
server-side behavior no client package could ever contain) states it
explicitly and consistently in two independent places. Given Trap 1's example
of the same doc set being wrong about auto-activation, treat this as
well-corroborated rather than beyond-doubt — but there is no internal
contradiction here (both mentions agree), unlike the activate case.

No rate limit is documented anywhere for `submission upload`/`submit`,
`match unrated`... wait — `match unrated` **is** in the shared bucket (listed
above). No rate limit is documented for `submission list/activate/rename/
download`, `match list/info/replay/watch/tests`, `team search/info`,
`ladder`, `maps list/sync`, or `status` — consistent with all of those being
read-only or cheap-metadata operations.

---

## Teams / Ladder / Maps

`team search QUERY [--json]` / `team info TEAM_ID [--json]` — both
**READ-ONLY**, `GET /api/teams/search?q=` and `GET /api/teams/{id}`
(`commands/team_group.py`). The deprecated `teams` group (`commands/teams.py`)
is functionally identical but has **no `--json` flag** on either subcommand —
a real capability gap if any tooling still calls the deprecated form.

`ladder [--limit N] [--around] [--json]` — **READ-ONLY**, `GET /api/ladder`.
Response is either a bare list or `{"rankings": [...]}` (handled either way,
`commands/ladder.py:22`). `--around` shows ±5 positions around your own
team, computed client-side after fetching the *entire* ranking list (no
narrower server query exists for this).

`maps list [--json]` — **READ-ONLY**, `GET /api/maps`. Compares local
`sha256` (`fcode/commands/maps.py:30-31`) against each pool entry's `sha256`
field to report `yes` / `outdated` / `no`.

`maps sync` — reads `GET /api/maps` then `GET /api/maps/download?name=` per
missing/changed map, content-addressed by sha256 so unchanged local files are
skipped (`commands/maps.py:39-63`). Writes only to the local `maps_dir`
(default `maps/`) — never touches platform state. No `--json` flag.

---

## Local dev commands (no platform contact except where noted)

- **`fcode run BOT_A BOT_B [MAP] [--replay] [--seed] [--watch] [--tle MS=0]
  [--map-random] [--json]`** — fully local, calls the compiled
  `fcode_engine.run_game` directly (`commands/run.py:127-195`). `--tle 0`
  (the default) means **no CPU enforcement locally**; the ladder always uses
  10ms (organizers' docs, `docs/reference/official-docs.md:833`; matches
  `docs/tooling.md`'s existing guidance to always pass `--tle 10`). Exits via
  `os._exit(0)` deliberately (comment cites a CPython 3.12
  sub-interpreter-finalization bug, line 192-195) — this skips normal Python
  cleanup, so don't rely on `atexit` hooks after `fcode run`.
- **`fcode watch [FILE] [--match ID] [--game N]`** — local file serves a
  bundled visualiser on `127.0.0.1:<random port>`; `--match` just opens a
  browser URL, no API call (`commands/watch.py`).
- **`fcode starter [DIR] [--yes] [--bot/--no-bot]`** — scaffolds
  `fcode.toml`, `.gitignore`, `bots/`, `maps/`; syncs the map pool from the
  platform **only if already logged in** (`commands/starter.py:91-102`), else
  prints a reminder to run `fcode maps sync` later. Non-interactive without
  `--yes` raises `click.ClickException` rather than hanging
  (`commands/starter.py:38-49`).
- **`fcode map-editor [--platform]`** — local static server or a browser tab
  to the platform's editor; no state changes either way.
- **`fcode init`** (deprecated, hidden) — alias for `starter`
  (`commands/init.py` is actually a *separate*, simpler implementation that
  only writes `fcode.toml`, but the deprecated top-level `init` command wired
  in `cli.py:127-134` calls `commands.init.init`, not `starter` — the two
  `init.py` and `starter.py` config-writers are near-duplicates; worth noting
  in case someone edits one expecting it to affect the other).

---

## JSON shapes

The CLI's `--json` variants are **thin passthroughs** — `click.echo(json.dumps(x))`
where `x` is (usually) the raw server response, sometimes a subset. This
means the true field list for any endpoint is **only fully knowable from a
live response**, which we did not fetch (no read-only network calls were made
producing new data; all `--json` field names below are corroborated either by
what the CLI code explicitly reads, or by this project's own prior empirical
captures cited inline). Fields marked "CLI-read" are proven by the source
lines already cited above; fields marked "empirical" are attested only in
this project's own logs, not in CLI source (which can't see field names it
never touches).

| Command | Wrapper shape | CLI-read fields | Empirically-attested extra fields |
|---|---|---|---|
| `status --json` | raw dict, hand-assembled by the CLI itself (not a passthrough) | `user`, `team`, `rating` (`{rating, matches_played, tier}`), `rank` (`{rank, total}`), `active_submission`, `recent_record` (`{wins, losses, sample_size}`), `members` — see `commands/status.py:116-125` | — |
| `submission list --json` | raw `submissions` array | `version`, `name`, `status`, `isActive`, `submittedByName`, `uploadedAt` | — |
| `submission upload --json` | raw `submission` object | `version`, `id` | — |
| `match list --json` | `{matches: [...], next_cursor}` | `teamAName`/`teamBName`, `teamAId`/`teamBId`, `sourceMatchAId`/`sourceMatchBId`, `winnerId`, `scoreA`/`scoreB`, `status`, `id`, `completedAt`/`createdAt`, `triggeredBy` | `ratingABefore`/`ratingBBefore` (at-match rating — **the correct field for historical analysis**), `teamARating`/`teamBRating` (live join — **trap, do not use for history**), `teamAVersion`/`teamBVersion` (both populated), `eloDelta` (reconciles against `ratingXBefore` to 11 decimals) |
| `match info --json` | `{match: {...}, games: [...]}` | `status`, `stage`, `triggeredBy`, `rated`, `scoreA`/`scoreB`, `teamAName`/`teamBName`, `teamAId`/`teamBId`, `winnerId`, `sourceMatchAId`/`sourceMatchBId`, `eloDeltaA`/`eloDeltaB`, `createdAt`, `completedAt`, `errorMessage`; per-game: `gameNumber`, `mapName`, `winnerId`, `winCondition`, `turnsPlayed` | opponent's submission **version field is `null`** here (bug — use `match list` instead) |
| `ladder --json` | raw list or `{rankings: [...]}` | `teamId`, `teamName`, `rating`, `matchesPlayed` | — |
| `team search --json` | raw `teams` array | `teamId`, `teamName`, `rating`, `matchesPlayed` | — |
| `team info --json` | `{team, rating, members}` | `id`/`name`, `rating`/`matchesPlayed`, `userName`/`role` | — |
| `maps list --json` | raw pool array | `name`, `width`, `height`, `symmetry`, `sha256` | — |

---

## Answers to the six specific questions

**1. Which commands mutate the ladder slot? How to roll back.**
Only two commands change what plays your ladder matches: `submission
upload`/`submit` (uploads a new version, which — per empirical logs, not CLI
source — auto-activates once `ready`) and `submission activate VERSION`
(explicitly reactivates an older, already-uploaded version, blocked unless
its `status == "ready"`, `commands/submission.py:203-208`). To roll back:
`fcode submission list` → find the target version → `fcode submission
activate VERSION`. `submission rename` mutates metadata only, no ladder
effect.

**2. What does `unrated`/`match test` actually play?**
Both beliefs confirmed. `match unrated` always uses **your currently active
submission** against **the opponent's latest ready submission** (or a
specific historical one via `--match`) — there is no field in the request
body to select a different bot for your own side
(`commands/test.py:13-42`; confirmed explicitly in organizer docs at
`docs/reference/official-docs.md:962,1853`). So testing a candidate on
`unrated` requires activating it first — alternation with the ladder slot,
never parallel. `match test` is local-bot-vs-local-bot: both `BOT_A` and
`BOT_B` are zipped from local paths and uploaded together; there is no
opponent-team parameter at all (`commands/test_run.py:51-120`) — it
structurally cannot supply a real opponent.

**3. What files get included in a submission zip?**
See "Packaging" above. Directory uploads exclude the `_JUNK_DIRS`/
`_JUNK_FILES`/`_JUNK_EXTENSIONS` sets listed verbatim
(`commands/submission.py:18-54`) at any depth. **Pre-built `.zip` files
bypass this filtering entirely** (`commands/submission.py:75-76`) — upload a
directory, not a hand-rolled zip, if you want the exclusion to apply.
`match test`'s bot-zipping path (`commands/test_run.py:18-48`) has **no**
junk filtering at all, regardless of input type.

**4. `match list` vs `match info` fields.**
Confirmed per Traps 2-3. `ratingABefore`/`ratingBBefore` = at-match rating
(reconciles exactly against `eloDelta`); `teamARating`/`teamBRating` = live
join, constant per team, a trap for any historical analysis. Both live in
`match list` JSON. `match info --json` additionally has a confirmed bug: the
opponent's submission version comes back `null`; get it from `match list`'s
`teamAVersion`/`teamBVersion` instead, which are populated on both sides.

**5. Timezone.** Confirmed, not re-derived — see `docs/tooling.md`'s existing
section; every `createdAt`/`completedAt`/`uploadedAt` field surfaced by this
CLI is UTC, local machine is CEST (UTC+2).

**6. What the source reveals that wasn't in the working belief set.**
- The `.zip`-passthrough bypasses junk filtering entirely (Trap 5) — a
  meaningfully different risk from "a stray `.git/` in a directory," since a
  hand-built zip gets zero protection.
- `match test`'s zip-builder has no junk filtering at all (Trap 4) — separate
  code path from `submission upload`'s, drifted independently.
- The organizers' own docs are the likely **origin** of the false
  "activate is required" belief (`docs/reference/official-docs.md:759-763`),
  not a misreading of the CLI — the CLI source never claims activation is
  required for a fresh upload.
- `submission download` has no `--json` flag, unlike every sibling
  subcommand in that group.
- The deprecated `teams` group lacks `--json` entirely (the modern `team`
  group has it on both subcommands) — a capability gap if anything still
  calls the old form.
- Two separate, near-duplicate config-file writers exist
  (`commands/init.py` and `commands/starter.py`) with overlapping but not
  identical behavior; the deprecated `fcode init` command calls the former,
  not the latter.
- `match tests --limit N` fetches the **entire** test-run list from the
  server and slices client-side (`commands/test_matches.py:16-17`) — same
  pattern as `ladder --around`. Neither sends a narrower query.
- The update-check (PyPI) call happens on *every* `fcode` invocation unless
  `FCODE_NO_UPDATE_CHECK` is set — worth knowing if a script wraps `fcode` in
  a tight loop and cares about the extra network round-trip (mitigated by a
  300s cache, `fcode/version_check.py:11`).

---

## Marked UNVERIFIED

| Claim | Why unverified | What would verify it |
|---|---|---|
| Exact complete field list of every `--json` response (beyond fields the CLI code itself reads, or fields already attested in this project's prior empirical logs) | The CLI is a passthrough; the true shape is server-defined and we made no new live calls to inspect it | Run a real (already-permitted) read-only `--json` call and diff the keys against this table |
| Whether `submission upload`'s auto-activation is unconditional (e.g. does it still auto-activate under a platform freeze, or for a team's very first submission) | Server-side behavior, no CLI source visibility, and no logged example of either edge case in this project's history | A freeze-window or first-ever-submission event, logged with before/after `submission list` state |
| Exact wording/HTTP status the server returns when `activate` is blocked by a platform freeze (`docs/reference/official-docs.md:765-769`, "uploads and active-submission changes are disabled") vs. the CLI's own `status != "ready"` block | Two different block mechanisms are documented (CLI-side status check vs. server-side freeze) but only the CLI-side one is visible in source | Attempt (in a safe/inert way, e.g. reading a past error log) to distinguish the two failure messages |
| Whether `match unrated`'s "opponent's latest ready submission" is literally their `isActive` one or merely their most-recently-uploaded `ready` one (these could differ if their active submission isn't the newest ready one) | Organizer docs say "latest ready," CLI source doesn't touch opponent-side selection at all, and no test scenario in project logs pins down the distinction | A scrimmage where the opponent's active version differs from their newest ready version, cross-checked against which one actually played |

None of the six numbered questions in the task depend on these — they're
edge cases surfaced while reading, flagged rather than guessed at.
