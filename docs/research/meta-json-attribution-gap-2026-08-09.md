# The archive has been 98% attributable all along — `join.tsv` sees 23% of it

**Research arm, session 25, 2026-08-09 ~19:0x CEST.** Found by a subagent on the CAD
lockout cut, which expected 85 attributable CAD games and found **220**. I verified the
underlying claim directly rather than accept it, and it is larger than the cut needed.

**Version tag.** Live slot **v94** = `bots/_v115dodge`, treehash `6ae6871c`. Corpus git
sha `7418e13`. Measured against `replay_archive/` as of this timestamp: **6,289
`.replay26` files, 1,261 distinct match ids, 1,260 `.meta.json` files.**

---

## THE GAP

`replay_archive/` contains a `<match-id>.meta.json` beside the replays for **almost every
archived match**, written by the archiver monitor. Each one is the full platform match
payload.

| | |
| --- | ---: |
| `.meta.json` files present | **1,260** (1,236 usable, 24 malformed/other shape) |
| distinct match ids among archived replay files | 1,261 |
| **matches covered by a meta.json** | **1,236 = 98.0%** |
| — of those, **ours** | 384 |
| — of those, **THIRD-PARTY** (neither side is us) | **852** |
| `triggeredBy: ladder` / `unrated` | 888 / **348** |
| **both `teamAVersion` and `teamBVersion` populated** | **1,236 / 1,236 = 100.0%** |
| **`corpus/join.tsv` attributes** | **1,445 of 6,289 replay files = 23.0%** |

`join.tsv` is built by paginating `match info` **for our own ladder matches**. The
archiver has been writing complete metadata for **every** match it downloads — including
other teams playing each other — the whole time.

## WHAT THIS UNLOCKS — three standing limitations, all of them softer than we thought

**1. CORPUS TRAP 4 IS LARGELY FIXABLE.** The standing caveat is *"the archive is not a
random sample of the field. It is dominated by our own games… 'Team X never does Y'
always means 'never against us, in N archived matches'."* **852 third-party matches
(~4,200 replays) are attributable and are a genuine field sample** — teams playing each
other with us absent. Top coverage: Powered by SmartFridge 107, sporks 52, team lazy 49,
Pantheon 45, Jython 41, Tyvrets 38, Pivot 37, kladde 36. **That converts "never against
us" into a testable "never, including against third parties" for the best-covered teams.**
This matters most for the opponent-modelling work, where every claim currently carries the
against-us qualifier.

**2. CORPUS TRAP 7 (DEAD VERSION COLUMNS) IS FULLY FIXABLE.** `join.tsv.oppver`,
`ladder_games.tsv.oppver` and `league_games.tsv.verA/verB` are the literal string `None`
in every row, and the only working source has been `league_matches.tsv` at 85.7% coverage.
**`meta.json` carries both versions at 100.0% of 1,236 matches.** Version-stratified
analysis — which we have repeatedly declined as impossible — becomes routine.

**3. THE UNRATED BLIND SPOT IS FIXABLE.** `ladder_games.tsv` is ladder-only by
construction, so earlier today the corpus could not see either unrated Ouroboros leg and I
had to go to the free `match list` channel to reconstruct them. **348 archived matches are
`triggeredBy: unrated` and have full metadata on disk.**

## WHAT IT DOES NOT UNLOCK

- **The 25 uncovered matches** stay unattributed, and the 24 malformed files should be
  inspected rather than assumed empty.
- **Coverage of a match is not coverage of a team.** Third-party counts are still small
  per team (36-107 matches for the top eight, far fewer in the tail) — the N still has to
  be said, it is just a *different and often larger* N.
- **Nothing here validates the replays themselves.** The seat/winner reconciliation that
  `join.tsv` passes at 100.0000% is a property of that pipeline; any new attribution path
  **must pass the same reconciliation test before a verdict consumes it.** That rule
  exists because `teamXRating` looked right for a day and was a live join.

## OWNERSHIP

**`tools/corpus/` is the builder's lane and I have not touched it.** This is a flagged
gap with numbers, not a patch. The smallest useful change is a `meta.json`-first
attribution pass in `join.py`/`ladder_meta.py` that falls back to `match info` only for
the ~2% of matches without a sidecar — and it should carry the existing reconciliation
test unchanged.

**Provenance note:** the subagent reported "220 CAD games (not 85)" and I verified the
mechanism behind it directly (file counts, third-party share, version population) before
writing this. The lockout cut's own conclusions rest on that expanded population, so the
verification was load-bearing for that deliverable as well as for this one.
