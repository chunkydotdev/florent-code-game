# MAP SEGMENTATION — gunner-cripple vs barrier-rush, per map (s51, 2026-08-18)

*Banked by the builder s51 from the sonnet mining agent (method: within-tape overperformance
vs pooled, dodging the different-controls trap; instrument guard reproduced SIEGECREW pooled
49.4829% and beltbreak2-final 53.0926% exactly before any table was trusted). Tapes:
BELTBREAK2 local n=5400 full (gunner mode, primary, ±5.16pp/map) · SIEGECREW local n=1257
selected-pessimistic partial (rush mode, ±10.7pp/map) · ladder ourver=159/155 (field check,
n=7-22/map — underpowered, can contradict nothing at this n). Derived TSVs:
`scratchpad/s51_mapseg/`. Magnus's question, verbatim intent: "gunner rush might be good on a
different segment than barrier rush and quick sentry finish."*

## THE ANSWER: THE SEGMENTS EXIST AND THEY ARE COMPLEMENTARY
* **GUNNER-GOOD, RUSH-BAD: midgard (+20.2 gunner / −29.2 rush), yulerune (+7.5 / −36.1)** —
  the rush line's two craters are the cripple mode's two best siege-active maps.
* **RUSH-GOOD, GUNNER-BAD: glacierkeep (+38.6 rush / −28.7 gunner — beltbreak's WORST map is
  the rush's BEST), ragnarok (+11.2 / −8.9).**
* **BOTH-GOOD: none.** Residual 8 maps neutral/mixed. GATED (antler, archipelago, fjordgate):
  rush axis CONFOUNDED by the door-turret regression (not map affinity); archipelago is
  gunner-GOOD (+13.6) and the chassis plays it anyway under the map gate.
* Ladder field-check: no map's ladder read can contradict its local read at n=7-22 —
  "disagree: No" everywhere is UNDERPOWERED, not confirmatory.

## ⛔ ORE DISTANCE IS NOT THE SELECTOR
The earlier 21pp ore-near/ore-far split was directional but the quadrants scatter: all three
gunner-GOOD maps sit at ore-chebyshev 3, but so do three NEUTRALs; gunner-BAD spans dist 2-8;
rush-GOOD spans 2-8. **dist=3 is a contested bucket, not a discriminator. The MODESWITCH
selector must key on MEASURED CELLS, not geometry** — registered list, re-derivable from the
tapes, only cells clear of their tape's pooled mean by >1 half-width enter.

## Full per-map quadrant table
| map | ore-d | gunner Δpp (n=360) | rush Δpp (n=82-84) | quadrant |
|---|---|---|---|---|
| glacierkeep | 8 | −28.65 BAD | +38.61 GOOD | RUSH |
| ragnarok | 2 | −8.93 BAD | +11.23 GOOD | RUSH |
| drakkarfjord | 8 | +4.69 n | +21.95 GOOD | rush-lean |
| drumlin | 3 | +1.63 n | +18.37 GOOD | rush-lean |
| midgard | 3 | +20.24 GOOD | −29.24 BAD | GUNNER |
| yulerune | 3 | +7.46 GOOD | −36.07 BAD | GUNNER |
| archipelago | 3 G | +13.57 GOOD | CONFOUNDED | gunner (gated anyway) |
| antler | 2 G | −5.31 BAD | CONFOUNDED | — |
| fjordgate | 3 G | −1.43 n | CONFOUNDED | — |
| auroraveil/frostgate/icefloe/nordkap/royale/valkyrie | 3-6 | neutral | neutral | mixed/neutral |

## Builder consequence (s51)
MODESWITCH's registered CRIPPLE list = **{midgard, yulerune}** (both clear by >2 half-widths
on both axes); everything else RUSH (gated maps already play the chassis). Composition
arithmetic: replacing the two crater cells (20.2/13.4 vs control) with ~cripple parity buys
≈ +4-5pp pooled over pure rush. GUNNER-FIRST (plant-on-the-way) is the orthogonal sequencing
variant and gets its own arm. Caveats carried: rush cells are ±10.7pp partials; the cripple
"parity" on its cells is by-construction vs our own control, not a field number (rule 6).
