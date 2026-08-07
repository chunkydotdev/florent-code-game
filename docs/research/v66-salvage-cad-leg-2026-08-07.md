# v66 salvage read: the CAD v107 leg — 2026-08-07

> **STALENESS FLAG (s14, ~21:15): the entire CAD family moved versions
> tonight** — CAD v107→v115, Lunds v42→v43, KCM 7→1, Powerpuff 26→18.
> Historical analysis in this doc (era-internal reads, identity matches
> against v107-era replays) stands; every FORWARD-LOOKING v107-era claim
> (exact opening/throw constants, probe-fidelity assumptions, calibration
> values) is SUSPECT until re-frozen against the new versions per the
> standing constants rule.

**Version tags (rule 2):** our side = **v66 "Eir 5.1" (_v76e51)**, the only
ladder loss of its 39-minute life (a7aa49ec, 1-4, we seat A). Opponent =
**CtrlAltDefeat v107** — the probe-valid version (byte-stable vs the
cad_probe era per the unclassified-five decode). Our live slot at read
time: v67 wave_ghost. Research arm, session 13, 5/5 games direct-pulled
(second half of the declared 10-file budget). Context: the pre-ordered v66
production read was VOID as specified (no nordkap/battery-family match ever
ran under v66); this leg salvages what v66's window can still teach.

## Rotation latch under losing pressure: HELD

Fire-direction analysis of every v66 gunner across all 5 games (proxy:
direction changes between consecutive shots from the same turret;
oscillation = fast A→B→A flips within 8 rounds):

- 8 gunners with fire records, 2-37 shots each: **direction changes 0-3
  per gunner, fast A→B→A flips = 0 in every game**, including the three
  long losses (r262/672/803) under sustained insertion harassment.
- Verdict-grade caveat: the proxy undercounts silent rotations (rotate
  without a subsequent shot), and total fire volume is modest. But the
  v65 failure mode (166 rotations / 50 oscillations in one game) would be
  unmissable in this data. **The latch mechanism survives contact with a
  harassing opponent class it was not tuned against.**
- The dump-cap half of the pre-ordered read remains UNVERIFIED in
  production: v66's window contained no r1000 game. It dies unverified —
  v66 is retired; the mechanism carries into the Eir 6 lineage where the
  next r1000 game under an Eir ship can read it.

## CAD v107 throw map under the v66 era (Loki insertion-denial input)

Throw = builder-bot position jump >1 tile (launcher pickup+throw). We are
seat A; all dsq values are to OUR core footprint.

| game | map | opening throws (r2-5) | steady-state |
|---|---|---|---|
| g1 (W r393) | 21×8 | 4 throws → (9,3)/(8,5)/(10,5)/(9,6), **dsq 5-17 — direct core-ring insertion** | none |
| g2 (L r262) | 26×26 | 1 throw near their base (staging) | **r32: abducted OUR builder** (5,4)→(9,8) |
| g3 (L r672) | 25×25 | (13,13) mid-map staging ×2, dsq 98 | **ferry loop: 17 throws → (1,0), dsq 41, r66-r500** |
| g4 (L r240) | 24×24 | (13,13) staging ×1, dsq 128 | none |
| g5 (L r803) | 25×25 | (15,8)/(23,8) lateral, dsq 288+ | ferry ×2 → (1,13), dsq 50 |

Findings for the Loki candidate (design doctrine, not constants — exact
tiles expire with OUR ships per the standing rule):

1. **Small maps: opening insertion goes core-ring-deep** (dsq 5-17 by r5).
   Pre-occupying the 3-4 passable ring tiles is the denial play there —
   and notably g1 is the game we WON, without denial, on the map where
   they inserted deepest (deep raiders died to core-adjacent defense).
2. **Large maps: r2-4 throws are mid-map staging** ((13,13)-class tiles,
   dsq ~100+), not core insertion — ring denial does nothing on these;
   the staging tile itself is the deniable geometry.
3. **NEW SIGNATURE — the ferry loop**: in long games CAD recycles raiders
   to a FIXED corner tile near our quadrant ((1,0) ×17 in g3; (1,13) ×2
   in g5). A single 3-Ti barrier on the ferry tile potentially breaks a
   600-round harass pattern — the cheapest denial arithmetic seen today.
4. **Launcher abduction of our builders is real** (g2 r32) — any Loki/
   anti-CAD work must assume our builders adjacent to their launcher
   range can be displaced, same mechanic as their self-throws.

## Disposition

- Latch: confirmed under pressure (rotation half of the dead pre-order
  salvaged). Dump cap: unverifiable for v66, ever — carry to Eir 6 reads.
- Throw map: feeds the insertion-drop denial Loki candidate (gated per
  unclassified-five on a pre-mortem vs decoded throws — rows above are
  that input, v66-era-pinned; re-extract after the next Eir-line ship).
- CAD probe validity: v107 confirmed live on ladder tonight (this match),
  so cad_probe legs are CURRENTLY VALID until they flip to v112.
