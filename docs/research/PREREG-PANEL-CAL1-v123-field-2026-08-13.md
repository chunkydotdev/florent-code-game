# PREREG — PANEL-CAL-1: v123 field-calibration panel (unrated, incumbent)

**Committed 2026-08-13T08:49:13Z (`date -u`), BEFORE any leg of this panel is created (two-clock
standard). Research arm s36 authors and reads; the BUILDER fires. Research never
fires, submits, or activates.**

## What this is
A CALIBRATION PANEL of the live holder — **v123, `bots/_v187saltidle_f`, the
`PROGRAMME.md INCUMBENT`** — against live target-band teams via
`fcode match unrated <team_id>`. The unrated fixture plays the ACTIVE
submission, so this panel involves **no submit, no activation, zero rated-leak
risk by construction**. It is a measurement of where the holder stands, not a
treatment leg: **there are no arms and no treatment diff.**

**Obligation 13 (mechanism metric file:line + treatment-diff intersection):
N/A, stated explicitly — both "arms" are the same bot; the treatment-diff
intersection is empty by construction.** No mechanism claim will be made from
this panel.

## TARGET BAND (gate run at boot, 2026-08-13T08:49:13Z session, tool output quoted)
17 teams admissible at our 1646 (us-80..us+125 AND 5-0 pays >= 10). Top payers:
team lazy +21.42 · Focalground +20.32 · LingLing40 +20.20. **Unrated games pay
0 rating — the band's role here is RELEVANCE: these are the ratings the ladder
will actually pair us with.** Opponent ratings below are the tool's cached
values (newest observation 07:32Z), fine for cell selection since no payoff is
at stake.

## Cells (6 opponents, stratified across the band)
| cell | team | rating | gap | team_id |
|---|---|---|---|---|
| C1 | team lazy | 1768 | +122 | 648d1d5b-5443-4257-a0aa-7048661b612d |
| C2 | Focalground | 1742 | +96 | 00191498-aa36-4f5a-aafb-e432e57607e8 |
| C3 | Juusto | 1714 | +68 | 32087804-2dde-4265-acb2-b6ec9039fbee |
| C4 | Jython | 1700 | +54 | 8cf9b751-00d3-484a-b0ed-e3073ae1d46f |
| C5 | The Bisons | 1693 | +47 | f670dfed-dfee-421b-8c01-a67b8a278ce3 |
| C6 | Lunds Stallions | 1623 | -23 | eceb8455-7cb3-442b-ba40-c6597c16b446 |

## What is recorded, per game (research decodes via `tools/corpus/sync.py`)
won · win condition (`wincond`, populated for unrated per the #34 resolution) ·
turns (kill round where cond=core_destroyed) · **map area class from mw×mh**
(<=676 vs 900 — area 900 is unambiguous under #35's proxy: only the five 30x30s).
**We cannot stratify map draws (the platform picks); we RECORD the draw.** The
900-area cells are live evidence for the builder's map-area work (queue #1);
opponent version pinned per game from `league_matches.tsv` at read time.

## Statistics and look schedule (pre-committed)
- **Currency: game_share**, pooled across windows. Kill-round median per cell
  as the secondary (PROGRAMME `SECONDARY_CURRENCY: kill_speed_score`).
- **No comparative sentence below 25 games/cell** (measured 12pp same-bot swing
  in a single 25-game window). Interim reads are DESCRIPTIVE only.
- **Comparative readouts at panel totals n=150 and n=300 (or wrap), not
  between.** Comparison target: per-cell Elo expectation E from the standard
  logistic at the cached gap, reported as share−E with exact binomial CIs.
- **Verdict sentences are the builder's.** This panel cannot ship, displace, or
  roll back anything, and no ship decision may cite it alone. It is also NOT
  rated evidence: v123's rated record is governed by its own pre-committed k=8
  look (taken, HOLD, certified 2026-08-13).

## Falsifier / what would make this panel worthless
If `wincond`/`mw×mh` fail to decode for >10% of panel games, the map-class and
kill-round columns are void for those cells and the readout says so; game_share
survives (it comes from the match record, not the replay).

## Why now
The lane-structure review measured the unrated fixture at ~8-20% of its
~1,800-games/day cap while v116→v122→v123 shipped on local self-play evidence
alone; v123 has ZERO live unrated games as holder; the organisers' map rotation
is live (builder reports today's rated tape 0/3 on 900-area maps) and no local
battery covers the new pool honestly yet.
