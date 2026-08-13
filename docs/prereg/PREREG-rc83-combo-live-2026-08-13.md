# PREREG — rc8.3 (COMBO, v9 candidate) LIVE PINNED LEG — arm D of the s36 tri-arm design

**Committed BEFORE leg creation (two-clock: this commit's git author time vs
platform `createdAt` of the leg's first match).** Builder s37, 2026-08-13.
Authorized by Magnus in-session: *"Could you run it as rc8.3?"*

## What fires

`bots/_v205combo` (UNDERECO + TWORAID + DIGOUT on `_v197mapcode`), platform
name **"Loki rc8.3"**, via `submit_clean --leg` (hold-until-sentinel, 300s
auto-restore, holder verified on the `Active bot:` line). **This is arm D of
`PREREG-triarm-live-2026-08-13.md` — same 5 opponent cells, same `--match`
pins (arm A's match ids), same 5-map list — so every game is matched-pair
comparable with arms A (control v125), B (UNDERECO), C (TWORAID):**

| cell | team | team id | pin (--match) |
|---|---|---|---|
| O1 | team lazy | 648d1d5b-5443-4257-a0aa-7048661b612d | ddf48911-0157-4efd-9b95-5b873ac7e401 |
| O2 | Leviathan | 26286680-d861-4f9e-9073-a6201bd48d3b | bca2bb40-8d7b-4d6f-af71-384698cd0795 |
| O3 | LingLing40 | 86d0b484-783c-47dc-99d9-6ed9af2794f8 | 446bb6a3-4ff5-4f66-83cb-9d3e1d610b55 |
| O4 | Juusto | 32087804-2dde-4265-acb2-b6ec9039fbee | c2e36a20-cc61-4f12-98d5-4e106d1ae981 |
| O5 | Coreflood | ea0d33c8-ca2b-497a-9be0-1837379eab1e | a33654a2-9927-4fe1-a386-0b801b62a209 |

Maps per match: `midgard drakkarfjord drumlin frostgate fjordgate` (identical
to arms A-C; the design's power is the pairing).

**TARGET BAND line (rule: written before the work):** at our live 1791, O1-O3
remain in-band; **O4 Juusto and O5 Coreflood have drifted BELOW the band
(−80) since the tri-arm's 1716-era admission.** Unrated pays 0 either way —
the band's role here is relevance, and the cells are kept BECAUSE changing
them would unmatch arm D from arms A-C (the pairing IS the instrument). The
drift is disclosed; no rated payout is claimed or at stake.

## Window and budget

CAL-3 runner STOPPED (yield rule; resumes after). Its last accept 18:30:54Z
holds a slot until 18:50:54Z, so the burst fires **just after the observed
~18:52:59Z rated pairing** — all 5 rate-limit slots free, ~17 min clear air
to the next pairing. Leak check per-match `ourver` at both pairing
boundaries; holder restore verified on the `Active bot:` line, never `$?`.

## Bars (n=25: dose and mechanism, NEVER a game-share verdict — same-bot
## swing ~12pp; matched-pair contrasts reported as counts only)

1. **Inherited B (income-lock fix, registered text unchanged):** in any game
   where an enemy camp latches `under` >100 rounds with our belt cut, the
   bank must NOT sit pinned ≤12 Ti for 50+ consecutive POST-CHRONIC rounds.
   FALSIFIER: a chronic-camp game with the bank still pinned — the fix is
   inert live IN THE COMBO (interaction defect, since it passed solo).
2. **Inherited C (paired contrast per tri-arm Amendment 1):** two-at-once
   raid cells counted vs arm A's SAME 25 opponent×map cells, reported as
   k-of-25 counts.
3. **Matched-pair read:** rc8.3 vs each sibling arm on shared cells, counts
   only ("D beat B on k of 25 cells"), no inferential dressing.
4. **NOT read here:** any DIGOUT-specific mechanism (its screen read
   NO-INFORMATION with kills traded away; its presence in the combo is what
   the local COMBO final prices — this leg cannot separate it).

## Relation to the ship decision

This leg + the local COMBO final (n=5400, ~2.5h out) + the UNDERECO
kill-round trade (paired-seed +11, coordination 2026-08-13T18:0xZ) are the
three inputs to the v9 ship recommendation. The recommendation goes to
Magnus with all three attached; none of the three alone decides.
