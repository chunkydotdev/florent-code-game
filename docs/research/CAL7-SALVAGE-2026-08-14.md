# CAL-7 SALVAGE — 2026-08-14

**NON-COMPARATIVE. DESCRIPTIVE ONLY.** The panel ended INCOMPLETE at 22
accepted matches / 110 games (holder changed under it before the n≥150
interim-look threshold in `PREREG-CAL7-2026-08-14.md`). Per that prereg's
stop conditions, **no comparative look is licensed at this n** — P1/P2/P3/P4,
any panel-vs-rated delta, and any resolution/annulus reading are all
**UNAVAILABLE**. What follows is the descriptive salvage the prereg allows at
any n (look-discipline item 1): per-cell tallies and ob-14 opponent-version
churn counts, nothing else.

## Why it stopped

Fire log (`scratchpad/panel_cal7_fires.tsv`) ends:

```
2026-08-14T14:46:06Z	ABORT	holder	expected v140 saw "v142 (Counter Router v3)"
```

Holder changed from v140 to v142 between the 14:41:54Z accept and the
14:46:06Z pre-fire holder check. This is the prereg's registered stop
condition **"Holder change — panel ends at the last window fully under
v140."** All 22 accepted matches complete before this abort.

## Method

Match IDs extracted from the ACCEPT rows' embedded JSON in
`scratchpad/panel_cal7_fires.tsv` (22 of 23 log lines; the 23rd is the ABORT
above). `corpus/league_matches.tsv` does not carry today's matches (checked:
0/22 IDs present — the corpus lags same-day data, per house rule R1).
Resolved instead via `.venv/bin/fcode match list --mine --type unrated
--limit 100 --json`, which covers 2026-08-14T08:02Z–15:36Z and contains all
22 target IDs. `match list` was used rather than `match info` because
`match info --json` returns a `null` opponent-version field (documented bug,
`docs/fcode-cli.md:497`); `match list --json` populates both
`teamAVersion`/`teamBVersion`. Per-match score (`scoreA`/`scoreB`) resolved
against whichever side is `OpenSverige`.

## Per-cell tallies (descriptive, n as labeled — no comparison to any rated or panel reference)

| cell | opponent (team id) | matches (n) | games (n) | our W–L | our share |
|---|---|---|---|---|---|
| D1 · 0033 | 0033 (`74ae65ff-96ae-4da5-a43e-692eb6fee38f`) | 4 | 20 | 6–14 | 30.0% |
| D2 · LingLing40 | lingling_40h (`86d0b484-783c-47dc-99d9-6ed9af2794f8`) | 4 | 20 | 10–10 | 50.0% |
| D3 · Juusto | Juusto (`32087804-2dde-4265-acb2-b6ec9039fbee`) | 4 | 20 | 3–17 | 15.0% |
| D4 · Jython | Jython (`8cf9b751-00d3-484a-b0ed-e3073ae1d46f`) | 4 | 20 | 11–9 | 55.0% |
| D5 · Big O | Big O (`f3362833-2d7a-4636-9a3c-e4f10fcebdc1`) | 3 | 15 | 5–10 | 33.3% |
| D6 · team lazy | team lazy (`648d1d5b-5443-4257-a0aa-7048661b612d`) | 3 | 15 | 12–3 | 80.0% |
| **TOTAL** | — | **22** | **110** | **47–63** | **42.7%** |

All 22 team IDs match the cell definitions registered in
`PREREG-CAL7-2026-08-14.md`. All 22 matches: `status=complete`,
`rated=false`, `triggeredBy=unrated`.

## ob-14 — opponent-version churn (per prereg amendment A4, reported at every read)

| cell | distinct opponent versions | values observed (in fire order) |
|---|---|---|
| D1 · 0033 | 1 | 57, 57, 57, 57 |
| D2 · LingLing40 | 2 | 52, 49, 49, 49 |
| D3 · Juusto | 2 | 11, 11, 13, 13 |
| D4 · Jython | 1 | 137, 137, 137, 137 |
| D5 · Big O | 1 | 21, 21, 21 |
| D6 · team lazy | 1 | 226, 226, 226 |

## Version-mismatch flags (instrument alarm per prereg stop conditions)

**None.** Our side (`ourver`) reads 140 on all 22 matches, all 22 cells,
every accepted fire. No window is voided.

## What this file does NOT contain

No comparison to rated shares, no panel-vs-rated delta, no P1/P2/P3/P4 call,
no resolution/annulus reading, no verdict on fixture bias or version
regression. The panel's comparative look requires n≥150 (interim) and the
design was powered for n≥300 (final); n=110 clears neither. This salvage is
for research to route as it sees fit.
