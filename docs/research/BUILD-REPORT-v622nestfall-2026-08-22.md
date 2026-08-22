# BUILD REPORT — bots/_v622nestfall (s55 builder, 2026-08-22)

**Parent:** bots/_v620skalman (line head ≡ v619 behaviourally). **Evidence source:**
`docs/research/DIAG-siteless-decomposition-2026-08-22.md` (the 2-cell band-exhaustion
finding). **Verdict surface:** deterministic F1/F2 screens (attribution), per the
two-surface practice — the LEVEL rides the next powered read.

## Planks

* **SK_NEST_EXHAUST_PB = True (SHIPPED ON).** When `_pick_nest`'s band scan — relax
  included — returns nothing, retry once at `lo=2` (the point-blank band the v1 ban
  excludes) at the most permissive spread. Fires only on total exhaustion.
* **SK_GAP_RELAX_SOLO = False (BUILT, OFF).** Un-welds the v613 gap-relax retry from
  SK_TUBE_FLOOR (dead code in every shipped configuration since the v614 road closure).
  On its target cell (paths_seatA) the mechanism fired exactly once (r442, site (22,16))
  and did not change the outcome — inert-on-outcome at this fixture, not refuted; stays
  a flag with its measurement attached.

## Screen results (deterministic F1 = NOISE_OFF _v542wave, F2 = NOISE_OFF Mjolnir;
15 maps × 2 seats, seed inert; tapes `scratchpad/s55_siteless/t_pb_f{1,2}`)

| tape | control (v620) | v622 (PB on) | identity |
|---|---|---|---|
| F1 | 14/30 kills | **15/30** | 28/30 cells turn-for-turn identical |
| F2 | 8/30 | 8/30 | 29/30 identical; icefloe_seatA loss delayed r386→r485 |

The one F1 flip is the diagnosis cell: icefloe_seatB, loss-at-r698 → **WIN r437**;
EXHPB fired first at r284 — exactly the round the 383-round siteless tail began — and
planted 6 point-blank sites. paths_seatA stays a r1000 loss with or without both planks
(tubes plant from r617 under both flags; they do not convert — that cell's failure is
now known to be not-siting-limited past the first relax).
**The registered expectation (coordination tail, pre-readout) was 15/30 + 28-cell
identity + those two cell outcomes: hit on all three.**
KILL_TARGET bar: the flip adds a r437 kill (past r300) and removes nothing before r300 —
timely-kill rate unchanged, non-regressing under DEFENCE_ADMISSION_BAR's form.

## The build's own defect, disclosed (routed: wrap-debt #3, retro at wrap)

The first flags-off tree FAILED the identity run (icefloe r952 vs control r698): the new
flags were missing from sk_roles' EXPLICIT `from sk_maps import (...)` list, so the first
siteless round raised NameError inside `_pick_nest` — swallowed by the run() exception
wrapper, silently rerouting the engineer every siteless round. The import smoke test
cannot catch this class; the identity RUN did. File-level bisect (3 arms) localized it;
the fix is one import line. Rule candidate: flags-off identity is RUN, never asserted,
and every new sk_maps flag consumed by sk_roles gets a same-shell
`sk_roles.<FLAG>` attribute assert (now done for both flags).

## Instruments

mkarm-pattern arm builds (rewrite + re-import + assert): `scratchpad/s55_siteless/
mkarm622.py`. Counter probes (GAPRELAX/EXHPB stderr prints) driven both ways: fired on
the hot cells, silent on quiet cells; the per-clause scan instrument was s54's, already
mutant-validated. All numbers are per-cell counts on the 30-cell deterministic fixture —
no game-share claim; DEFF does not apply (no cluster can hold two members within a
1-game cell; the fixture rule: vary MAP and SEAT, never seed).
