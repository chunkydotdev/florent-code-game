# SIDE-LANE AUDIT — s50 WRAP-FIX guard commits, independent both-ways re-drive (s51, 2026-08-18 ~03:5xZ)

**Provenance:** produced by an opus audit subagent (read-only brief: fixture copies + stubbed
fcode only; no tracked file edited, no platform command run; verified via `git status` at close).
Commissioned by the side lane per its s50 inherited item 2 — the wrap-fix commits all CLAIM
both-ways drives in their messages; per D21(g) a cited drive is re-run, not trusted. **Side-lane
spot-verification before publishing:** D1's anchor re-read on the live tree
(`tools/monitors/ship_watch.py:586-590` — env-or-state independent reads, pair re-persisted);
D2's inversion re-derived from the source table (`post-throw-tile-dwell-2026-08-09.md:409-410`:
dwell=0 84.14% for L<V vs 1.83% for L>V, against atlas:330's prose crediting L<V with 99.64%
still-there). Both confirmed. Flags with anchors, never verdicts; fixes belong to the owning
lane, and under Magnus's wrap rule ("NO tools should get fixed during the session") every TOOL
defect below routes to the wrap debt list with a behaviour-now line, while the DOCS defect (D2)
is a record correction fixable immediately.

**Score: 6 of 10 commits VERIFIED with exact reproductions · 2 HIGH · 1 MEDIUM · 1 LOW-MED · 3 notes.**

| # | Commit | Severity | One line |
|---|---|---|---|
| **D1** | a6654e98 | **HIGH** | The stale-baseline refusal is bypassable and self-laundering: `SHIP_VERSION` alone re-labels the dead v116 baseline as the live holder's, the guard passes, `net_act=+183.0 src=env` prints — and the mislabel persists to disk. |
| **D2** | f1d9ef8a | **HIGH (docs)** | The id-order inequality correction did not reach §9.3 (atlas:330 still inverted, in the same sentence as its own correct code form); the fix note's citation of `:409-410` is itself inverted; the 1.83% comparator is mis-sourced (correct us-only figure 6.2%); the commit message omits its own fact-6 rewrite. |
| **D3** | bad87392 | **MEDIUM** | `_tmp_for`'s "dot-prefixed so `glob("*")` does not see it" is false for the consumers it names: `pathlib.Path.glob` returns dotfiles — `tests/test_instruments.py:843` and `tools/corpus_sanity.py:594` both see (and the latter would parse) the transient temp. |
| **D4** | 9244bc65 | **LOW-MED** | DRAINED domain gap: `.started` markers are written at LAUNCH (`tools/corefill.sh:384`), not completion, so a corefill death after the last launch reads `DRAINED / 0 PROBLEMS`. |
| m1 | 5a402c22 | note | "6 mutants each caught by name" — M1 and M3 fire the same assertion; 6 mutants / 5 distinct names. |
| m2 | 3a7d8ecc | note | The naive-stripper "second defect" is latent: it changes no mark verdict on today's `gate_watch.sh`; only the dedicated stripper cell catches it. |
| m3 | 2322d286 | note | A run that skips EVERY cell still exits rc=0 — the log discriminates, the exit code does not. |

**Behaviour-now lines (until the wrap discharges the tool items):**
- **D1:** never set `SHIP_VERSION` without `SHIP_BASELINE` (setting it alone launders the dead
  pair past the guard AND persists the lie). Live path currently inert (`net_act_src=derived`;
  live state file still carries `v116/1655.0` — three holders dead).
- **D3:** a `corpus_sanity` failure naming a dot-prefixed transient `.tsv` during a keeper cycle
  is a race artifact — re-run before acting on it.
- **D4:** on a DRAINED read, cross-check shard heartbeats before trusting it — DRAINED currently
  proves no UNSTARTED work, not no UNFINISHED work.

---

## AGENT REPORT (verbatim, entities normalised)

Method: every guard re-driven empirically on scratchpad fixture copies + stubbed `fcode`. No `fcode` command was run. No tracked file was edited. Verified at the end: `git status --porcelain` shows nothing dirty under `tools/`, `docs/`, `corpus/ship_watch_state.json`, `scratchpad/fire_rotation_s50.sh`, `docs/prereg/BARS.tsv`.

### ea115910 — fire_rotation_s50.sh multi-line `$mid` — VERIFIED

Claim "OLD 2/2/1 lines, NEW 1/1/1" reproduced exactly on the three named fixtures (MULTILINE OLD 2 → NEW 1; SAMELINE OLD 2 → NEW 1; SINGLE 1 → 1). The stated first-uuid residual is real and the drive exhibits it: in MULTILINE the fixture prints the team id first and NEW captures the WRONG uuid silently — which is what `scratchpad/fire_rotation_s50.sh:56-61` writes down. D21 domain: the residual's named backstop (`match info "$mid"` at :66) only appends to the log; nothing gates on it — a human-read check, not enforcement.

### 2322d286 — captured-subject holder gate — VERIFIED

Stubbed fcode, fixture copy, sleep neutralised. stable → rc=0, 4/4 cells FIRED with subject captured; error (`Error: True`, no `Active bot:` line) → rc=1 ABORT "the subject is UNKNOWN, not unchanged"; churn (holder flips mid-run) → first cell FIRED, remaining 3 SKIP with both holder strings logged. Pre-fix failure reproduced on `2322d286^` with a v160 stub: all 4 cells skipped on the baked `v159` literal, "runner done" at rc=0 — fires nothing, looks healthy. NEW on same input: 4/4 FIRED.
m3: NEW's churn path also exits rc=0 after skipping 3 of 4 cells — the log discriminates, the exit code does not. The `Error: True`-exits-0 premise was STUBBED, not measured against the real CLI (per instruction).

### 5a402c22 — stub_engine `is_in_vision` — VERIFIED

Live selftests at claimed counts: STUB-ENGINE SELFTEST OK · test_instruments 43/43 OK · full discover 164/164 OK. All 6 mutants re-built and re-driven against a passing control: M1 re-add bounds check, M2 always-True, M3 always-False, M4 non-raising get_tile_building_id, M5 in-map-near-False, M6 in-map-far-True — each rc=1 with a named assertion. Citations resolve (CLAUDE.md:367-377; PROBE-DOSSIER-ferry-siege-2026-08-17.md:184-196, atoll `is_in_vision((-1,14))=True` with controls).
m1: M1 and M3 fire the SAME assertion string — 6 mutants / 5 distinct names. D21 domain: engine ground truth is 2 maps, core-scoped (atoll 3 off-map True + heart 8 off-map False); the stub generalises to all units and radii — reasonable but wider than the probe.

### 9244bc65 — fleet_health DRAINED vs MISSING — VERIFIED (with D4)

`--selftest`: 23 [ok], rc=0 (as claimed). TestWatchdog 8/8 OK. Live read: DRAINED / 0 PROBLEMS / rc=0 (matches claim). Fixture drives via `--corefill-work/--corefill-state-dir` (no live state touched): drained → DRAINED rc=0; 1 pending → ⛔ MISSING rc=1 ("not a clean drain, likely died"); unreadable → ⛔ MISSING rc=1 carrying BOTH hypotheses. Own mutants all caught by name (mutA always-drained, mutB none-is-drained, mutC drained-is-bad). Mirror fidelity confirmed: live supervisor loop matches `_corefill_remaining` (corefill_forever.sh:88-91); JSON schema unchanged; watchdog.sh matches only MISSING/DUPLICATE so DRAINED is inert there.
**D4 — DOMAIN GAP.** `remaining` counts UNSTARTED rows and the marker is written at launch (`tools/corefill.sh:384`), not completion: corefill dying after the last launch yields remaining==0 → DRAINED / 0 PROBLEMS / rc=0, and the `shard runners` row is info-only so nothing else catches it. "remaining==0 → not a problem" holds for unstarted work, not unfinished work.

### f2db0a37 — cancel kills AND stamps — VERIFIED

`cancel_shard()` extracted verbatim (`tools/corefill.sh:147-184`) into an isolated harness. All five cells: live shard → killed 0s, RUNNING→CANCELLED, bystander RUNNING still ticking, COMPLETE untouched; never-launched → "nothing to stamp", no file invented; already-terminal → left as-is; TERM-ignoring → KILL escalation at 5s, stamped at 6s; unkillable (KILL_WAIT_S=0) → "STILL ALIVE … heartbeat LEFT UNTOUCHED", refusal shouted. Stamp-deleted mutant reproduces the exact reported defect (log says CANCELLED, file says RUNNING). The documented `ps` false-ALIVE limitation was hit unprompted (the auditor's own shell matched the pattern; degraded exactly as documented). pool26 selftest + two mutants both ways; fleet_dispatch CANCELLED-terminal cell + mutant both ways. `check_cancel()` byte-identical across the three runners (diffed). Repaired-heartbeat provenance exact against `scratchpad/corefill.log:8723/:8705` and the tapes (461−2=459, 1172−2=1170). Stated caveat re-counted today: 244 heartbeats / 110 non-terminal, as written.

### bad87392 — atomic corpus writes — VERIFIED, with D3

All guards both ways: mode guard ('w' writes; 'a'/'r'/'w+'/'r+' ValueError); crash mid-write leaves original unchanged, zero leftover temps; THE INCIDENT CLASS reproduced — in-place `open(path,'w')` gave 50 short/partial reads of 64 under a concurrent reader, `atomic_write_text` gave 0; gzip roundtrip + 0644; subprocess clean and raising paths; existing 0640 preserved, new 0644.
**D3 — the temp-invisibility claim is false for the consumers it names.** `tools/corpus/atomicio.py` `_tmp_for` docstring: "Dot-prefixed so a `glob(\"*\")` sweep — tests/test_instruments.py's `_fs_signature` — does not see the transient file." But `_fs_signature` (`tests/test_instruments.py:843`) uses `pathlib.Path.glob`, which returns dotfiles (driven: `glob.glob('*')` hides the temp; `Path.glob('*')` and `Path.glob('*.tsv')` both return it; the exact expressions at test_instruments.py:843 and corpus_sanity.py:594 both return it). Consequences, race-window-only: `_fs_signature` can attribute a transient to the tool under test; `corpus_sanity.py:594` will open and parse a half-written temp as a corpus table. Also observed mid-write: a brand-NEW destination path does not exist during the window (correct for atomicity; a reader gets FileNotFoundError, no old inode exists to serve). Minor: message says "9 call sites"; 18 exist (keeper STATE/PIDFILE, sync LEDGER, archiver PRIORITY converted but unnamed) — more than claimed, not less.

### 3a7d8ecc — auto_gate `marks_agree_with_gate_watch` — VERIFIED

Pre-fix regex reimplemented verbatim beside the shipped one: unmodified live file OLD=True NEW=True; mark moved 1000→1200 both False; moved + old literal in a COMMENT: OLD=True (the s49 defect) NEW=False; 400 deleted + prose mention: OLD=True NEW=False. `auto_gate.py --selftest` rc=0 (4 new cells). Mutants in a symlink shadow-repo: mutA loose-grep caught by both comment cells; mutB naive-strip caught by the quoted-`#` cell (`gate_watch.sh:51` confirmed real).
m2 (D21 domain): under mutB the "unmodified live file still reads OK" cell did NOT fail — a naive cut-at-# would change no mark verdict on today's gate_watch.sh (the four `(( n >= … ))` lines carry no `#`). The "second defect" claim is LATENT, caught only by the dedicated stripper cell. Fix strictly safer; claim wider than the observed effect.

### d0a7be24 — BARS.tsv append idiom — VERIFIED

Fixture copy, all three ways: documented idiom → PRESENT rc=0 (+56 bytes); the s50 empty-awk (`NR==FNR` with empty first file) → awk exit 0, 0 bytes, no stderr, guard FIRES rc=1; space-for-tab mangled row → guard FIRES rc=1 (catches "wrong thing written" too). D21 domain: header comment, NOT an enforced tool — verified nothing automates it (every BARS.tsv reference in tools/ is a reader; no appender exists to bind the check to). Efficacy rests on the next author reading the header.

### f1d9ef8a — atlas routing (docs) — DEFECT (D2)

What checks out: BUILD-REPORT-v512ringladder:30-36 carries P6 verbatim (FALSE 40/40, empty-seat TRUE 383/383, 1,438 readings/8 games, `siege.py:494` = `_fs_body_blocked`); the 5.5a figures match source; the fact-3(b) cross-link resolves.
What does not:
1. **The commit message omits half its own diff** — it also rewrites fact 6 (atlas:52), inverting `launcher_id < victim_id` → `launcher_id > victim_id`, unannounced.
2. **The correction did not reach §9.3** (`BUILDER-TACTICS-ATLAS-2026-08-14.md:330`, untouched by the commit): still reads "with `launcher_id < victim_id` the victim is still there next round 99.64% of the time, against 1.83% otherwise … and the filter itself is `if victim_id < ct.get_id()`" — the prose inequality is the identical inversion just corrected at :52, in the same sentence as the correct code form. The file is internally contradictory and §9.3 is where fact 6 sends readers.
3. **The fix note's own citation is inverted**: it attributes the 1.83% escape case to `launcher_id < victim_id`; source table `post-throw-tile-dwell-2026-08-09.md:409-410` reads L<V dwell=0 84.14%, L>V dwell=0 **1.83%** — 1.83% belongs to the GOOD side.
4. **The 1.83% comparator is the wrong quantity**: it is an all-throws dwell=0 rate for the other group; the matching us-only figure (`:454-456`, dwell=0 given L<V = 93.8%, N=5,886) gives **P(≥1 dwell) = 6.2%**, not 1.83%. Same error at :105, :330, :354.
Not yet propagated into code (no `victim_id`-filter hits in `bots/_v512ringladder/` or `bots/_v513*/`, consistent with atlas:105 "Not implemented anywhere in the tree") — latent, but the atlas is the copy-paste source the correction exists to protect.

### a6654e98 — ship_watch stale-baseline refusal — DEFECT (D1); the guard itself VERIFIED

`--selftest` rc=0 (4 new cells). Re-driven through shipped `assess()` with the derivation forced to fail (the fresh-ship state): OLD form (no owner) → `net_act=+167.0 src=env` off the dead constant (defect reproduces); NEW form owner v116 ≠ holder v160 → `net_act=UNKNOWN src=REFUSED-STALE(v116!=v160)` (refusal fires, names the disagreement); owner==holder control still prints; derivation-succeeds → `src=derived` wins; baseline=None control absent. Live state confirmed: `corpus/ship_watch_state.json` = `{"version": "v116", "baseline": 1655.0}` vs holder v159 at 1838 — inert only because `net_act_src=derived`.
**D1 — THE REFUSAL IS BYPASSABLE, AND THE BYPASS PERSISTS.** `ship_watch.py:586-587` reads version and baseline from INDEPENDENT sources (env-or-state per half), then `:590` re-persists them as a PAIR. Simulated on a COPY of the live state file: no env → guard refuses (REFUSED-STALE(v116!=v159)); `SHIP_VERSION` set alone → `version=v159, baseline=1655.0`, persists `{"version": "v159", "baseline": 1655.0}` — v116's number permanently relabelled v159 — and `net_act=+183.0 src=env`: the exact class the fix exists to suppress, now self-laundering (every later run also passes). `baseline_version` tags the baseline with whatever `version` happens to be, not with the provenance of the number. The fix closes the state-file-goes-stale path; it does not close the version-moves-without-the-baseline path. (`ship_watch.py:50` describes SHIP_VERSION as an optional reporting-only knob.)

### NOT-DRIVEN cells (honest list)

- `fcode status` exits 0 while printing `Error: True` — stubbed, not measured against the platform (instructed).
- ship_watch `main()` end-to-end — not run (`:590` writes the live state file); driven at `assess()` level + a verbatim simulation of `:580-590` on a copy.
- 3a7d8ecc / f2db0a37 remote paths (`remote_cancel` FRESH check, `corefill_status.sh`) — read, not executed; consumers, not changed guards.
- fleet_health with a live corefill.sh present (found>0 control) — no such process exists right now; covered by the selftest's proc list + mutants.
