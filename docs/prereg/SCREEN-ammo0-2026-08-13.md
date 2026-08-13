# SCREEN PREREG — S2: the r0 ammo pre-buy, alone, on the current chassis

**Committed before the shard's first heartbeat (two-clock).** Builder s37,
2026-08-13. Basis: mining sweep axis 2 (S2) — x3r0's 5-line pre-buy
(`_x3r0_v115/main.py:206-211`, ported verbatim behind `LOKI_AMMO0_ON`),
verified ABSENT from the incumbent (v116 reverted it, all ships descend from
v116), never screened alone (the two shipgate arms bundled launcher
deletions). Family screens at n=5408: AMMO115 51.16 · ZEROAMMO 52.90 ·
LATE160AMMO 53.31 — the record's own amplification example. Product (first
sentinel volley funded at r13) is worth strictly MORE on the salt kill-share
chassis than the era it was measured on. Cost: 17 of 500 Ti, action-free,
zero bodies/action-rounds/tiles.

## Shard
`AMMO0` = `bots/_v212ammo0` vs `_v197mapcode`, n=5400, seed base 236000.
Futility gates per RULE-futility-gates (1000/2700). D26: replicated iff
final |share−50| ≥ 2.0pp, second shard 237000, scored alone, same-side
pooling only. Kill-round paired-seed non-regression rides along — the
mechanism PREDICTS faster kills (funded first volley), so a rise is a red
flag.

## Dose
Wire-readable by construction: `global_ammo` = 17 at r0 in treatment, 0 in
control. Verified once from a single kept-replay game before the shard
starts (below); no tag machinery.

## Ship relation
If the final approaches the family's 52.9-53.3 on the CURRENT chassis, this
is a "bigger significance" candidate under Magnus's raised bar — 5 lines,
zero interaction surface by resource table (nothing else spends at r0), and
it would go to a pinned live leg before any ship packet.
