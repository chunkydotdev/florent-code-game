# SPEC — `corpus_sanity` TRAP 9: duplicate-key detection on append-mode surfaces

**2026-08-14, research arm (s42).** Written at the builder's request (*"research writes
specs / builder builds is the right split"*). **Scope: `tools/corpus_sanity.py` only.** The
repair of `league_matches.tsv` and the locking of the append path are separate tasks the
builder has already queued; this spec covers the alarm that would have caught them.

---

## 1. THE DEFECT THIS TRAP EXISTS FOR

**Measured 2026-08-14T19:2xZ.** `corpus/league_matches.tsv` carried **45,436 rows against
45,317 distinct `id`s — 119 duplicates, each appearing exactly twice, byte-identical, all
dated 2026-08-14.**

The structure identified the mechanism without guesswork: **the duplicates form two
contiguous tail blocks whose row-index gap between copies equals their own batch size (41
and 78)** — the file ends `[batch][same batch]`, twice. Matched against `corpus/keeper.log`:

```
keeper 14:03:15Z   "league_matches: +41 new"       -> the 41-row block
keeper 19:10:19Z   "league_matches: +78 new"       -> the 78-row block
research boot sync ~19:09:5xZ "+78 new"            -> the second writer
```

`tools/corpus/league_matches.py:77` reads `known = {r["id"] for r in rows}` and appends the
complement. **There is no lock anywhere in the append path.** Two processes that read
`known` before either writes both classify the same rows as fresh and both append.

**Why it appeared today:** keeper was re-armed after the 18:56:33Z reboot and its first
cycle landed on a lane's boot sync. **Reboot + multiple lanes booting IS the collision
condition**, so this recurs by construction, not by bad luck.

**It went unseen because `corpus_sanity.py` has TRAPs 1–8 and no duplicate-key check of any
kind.** This class has never been detectable.

---

## 2. WHAT THE TRAP CHECKS

For each configured surface, count rows against distinct values of a declared key. **A
duplicate key is a FAIL, not a WARN** — every surface below is either id-keyed by the
platform or key-unique by construction, so a duplicate is always a defect.

| surface | key | rationale |
|---|---|---|
| `corpus/league_matches.tsv` | `id` | platform match id; **the observed defect** |
| `corpus/ladder_games.tsv` | `(match, map)` | game grain; a match plays each map once — **verified: 0 duplicates in 4,920 rows** |
| `corpus/meta_join.tsv` | `file` | one row per replay file — **verified: 0 duplicates in 41,878 rows** |

**The two clean surfaces are in scope deliberately.** They are the standing negative
controls: a trap that only ever runs against the known-bad file cannot show it discriminates.

**Output must name the surface, the key, the number of duplicated keys, the number of excess
rows, and up to 5 example keys.** A bare count sends the reader hunting.

**⛔ REPORT THE MULTIPLICITY DISTRIBUTION, not just a count.** `{2: 119}` says *two writers
raced once per batch*; `{2: 40, 3: 12}` says *three writers, or a repeating loop*. **The
distribution is the diagnostic; the count is only the alarm.** This is the difference
between the trap telling you something is wrong and the trap telling you what to fix.

**⛔ AND STATE WHETHER THE DUPLICATE ROWS ARE IDENTICAL.** Byte-identical duplicates are a
race and are safely repaired by keep-first. **Duplicates that DIFFER are a different and
worse defect** — two sources disagreeing about the same match id — and must not be silently
deduped. The trap distinguishes them; the repair tool depends on the answer.

---

## 3. BOTH-VERDICTS EVIDENCE — and there is a free positive control on disk RIGHT NOW

Per the standing instruments rule (*"a check that has never produced the other verdict has
not been seen to check"*), each cell is driven both ways.

| cell | drive | must report |
|---|---|---|
| **P1 positive, LIVE DATA** | `league_matches.tsv` **as it stands before the repair** | FAIL: 119 duplicate `id`s, 119 excess rows, multiplicity `{2: 119}`, identical=yes |
| **P2 negative, LIVE DATA** | `ladder_games.tsv`, `meta_join.tsv` unmodified | PASS on both — the trap is not simply always-firing |
| **P3 positive, synthetic** | duplicate one row of a clean fixture | FAIL naming that key |
| **P4 negative, post-repair** | `league_matches.tsv` after keep-first dedup | PASS |
| **P5 differing-duplicate** | synthetic: same `id`, one field altered | FAIL **and** `identical=no` — the branch that must not be auto-repaired |
| **P6 blind** | unreadable / absent path | **must announce it could not read**, never silently pass |

⭐ **P1 IS AVAILABLE ONLY UNTIL THE FILE IS REPAIRED.** A positive control on real
production data — as opposed to a synthetic one — is rare and it evaporates the moment the
dedup runs. **Build and run the trap against the corrupt file BEFORE repairing it, and paste
its output into the commit.** If the repair lands first, P1 degrades to P3 and the trap
ships never having fired on the defect it was written for.

**P6 is not optional.** This repo's standing finding is that a monitor which cannot tell it
is blind prints a healthy line and a blind line identically. **Absence of a FAIL is not a
PASS unless the file was read.**

---

## 4. WHAT THIS TRAP DOES *NOT* DO

* **It does not prevent the race.** It detects the consequence. The lock (or
  write-temp-and-rename) is the fix; **this trap exists to tell us the fix regressed.**
* **It does not repair.** Repair is a separate deliberate action on a surface whose
  duplicates have been confirmed identical.
* **It does not extend to `corpus/*.tsv` generally.** Several corpus surfaces are
  event-grain and legitimately hold repeated keys. **A trap that fires on a legitimate
  surface gets muted, and a muted trap is worse than no trap** — hence the explicit
  three-surface allowlist rather than a glob.

---

## 5. ACCEPTANCE

1. `.venv/bin/python tools/corpus_sanity.py` prints a TRAP 9 line for each of the three
   surfaces, naming key, duplicate-key count, excess rows, multiplicity distribution and
   identical yes/no.
2. All six cells of §3 exercised, with **P1 run against the pre-repair file** and its output
   quoted in the commit message.
3. The verdict line convention is preserved: **gate on the presence of the verdict line, not
   on `$?`** — this repo's exit codes are not a health signal (`fcode status` exits 0 while
   printing `Error: True`), and TRAP 8's own root cause was a tool dying before its verdict
   line while the pipe masked the status.

---

## 6. PROVENANCE

Written by the research arm from a defect it **participated in causing** — the second writer
of the 78-row block was this lane's own boot sync at ~19:09:5xZ. Recorded here because a
spec whose author was one of the two racing processes should say so.
