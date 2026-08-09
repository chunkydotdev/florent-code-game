# Loaded unrated fixture: the five hard teams, ready to fire in one ladder gap

**Side lane, 2026-08-09 15:16 CEST. Magnus: unrated is a FREE tool (zero Elo,
runs in the gap between ladder matches) that we never use — the exact failure
the test-process-proposal names (local wins by default because unrated has
ceremony). This removes the ceremony: team IDs, the worst-map targets, and
pre-registered bars, so an unrated pass is one copy-paste. Firing it is the
builder's (it plays the ACTIVE submission → needs the slot); this lane loaded
it read-only.**

## The convergence that tells us WHAT to verify

The maps where we go **0%** against the hard teams are the **same map class**
across all five — hive, drumlin, nordkap, saga, snowflake, eider, archipelago.
That is the sentinel-siege terrain the CAD read identified (stand-off sentinels
the defender can't block). **We don't lose to five different teams; we lose to
one weapon on one map class, five times.** So the unrated pass is not a
fishing trip — it tests a specific prediction: *does the sentinel rush (or any
variant) convert the 0%-maps against the teams that use that weapon?*

## The fixture (verified vs `corpus/league_matches.tsv` + `ladder_games.tsv`)

| team | teamId | latest ver | our rated baseline | worst maps (our win %, n≥4) — the `--map` targets |
| --- | --- | --- | --- | --- |
| **Ouroboros** | `a5631594-3000-457e-890d-29d547f9de93` | 8 (static since 08-06) | **15% (23/150)** | hive 0/7, drumlin 0/8, nordkap 0/8, eider 0/10, lighthouse 0/13 |
| **Lunds Stallions** | `eceb8455-7cb3-442b-ba40-c6597c16b446` | 44 | 26% (46/180) | atoll 0/10, hive 0/11, antler 1/11, nordkap 2/16, eider 2/13 |
| **Kings College Munich** | `dfa9be96-f6f6-490b-9c79-d22f9b42369d` | 8 | 27% (31/115) | drumlin 0/8, saga 0/8, snowflake 0/8, archipelago 0/9, heart 1/8 |
| **CtrlAltDefeat** | `74e43df6-bad7-474b-8e37-0ea44a2c80f1` | 120 | 31% (31/100) | hive 0/4, nordkap 0/4, saga 0/4, snowflake 0/5, jackpot 0/6 |
| **Powerpuff Girls** | `0c1fea85-495c-41e3-bb30-f6665ddd2cd4` | 46 | 32% (50/155) | saga 0/12, snowflake 1/12, fjordgate 1/9, drumlin 1/8, hive 2/12 |

`fcode match unrated <teamId> --map <m1> <m2> ...` (up to 5 maps/call).

## Two uses, both free, in priority order

**USE 1 — clean v92 baseline, fireable NOW (no build needed).** The rated
baselines above are **pooled across 80+ of our shipped versions** (v20→v91) —
a muddy denominator. One unrated cycle of the LIVE bot vs each hard team on its
worst maps gives a **confound-free, current-version** baseline, which is the
denominator every later Loki-2 delta is measured against. This is the use
Magnus's "we never use it" points at directly: it costs nothing and we've been
inferring from pooled history instead.

**USE 2 — Loki-2 verification, pre-ship.** Submit Loki-2 in a gap, fire the
same fixture, read against the pre-registered bar, roll back — all inside the
~4:13 safe gap (test-process §4). Bar: our baseline on these maps is **~0%**,
so *any* wins on the 0%-maps is signal the rush converts them.

## The discipline that binds both (test-process §5 + HANDOVER)

- Unrated **can REFUTE, can never CONFIRM**: at n=10 it has 47% power. Record
  **`NOT-REFUTED (n=10)`**, never `pass`. Confirmation is the ladder.
- Rate limit **5 unrated/10min**; a full 5-team × worst-maps sweep spans a few
  gaps — pre-register which teams matter most (Ouroboros first: worst matchup,
  static target, so a fix stays valid).
- Unrated **flips seats** between challenges — a before/after needs the seat to
  match, or treat cross-seat legs as different games.
- It plays the **ACTIVE submission**, so USE 2 needs the variant to hold the
  slot for the sweep, then a rollback (the zero-Elo loop). USE 1 just plays
  live v92 as-is.

## Ownership

Firing unrated is builder-only (slot + platform-mutating). This lane's
contribution ends at the loaded fixture. Relayed to the builder; the pick of
what/when to fire is theirs.

## Provenance

Team IDs + latest versions: `corpus/league_matches.tsv` (teamAId/Bid, latest
createdAt per team). Per-map baselines: `corpus/ladder_games.tsv`, game-level,
our lineage, n≥4/map. Map-class convergence cross-references
cad-core-kill-2026-08-09 (the sentinel-siege maps). Unrated mechanics:
docs/research/test-process-proposal-2026-08-09.md §4-5 + HANDOVER unrated block.
