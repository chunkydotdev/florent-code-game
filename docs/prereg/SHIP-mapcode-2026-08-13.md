# SHIP PREREG — `bots/_v197mapcode` ("Loki v8") — committed BEFORE any ship activation

**Status at write time (09:2xZ): RECOMMENDED, NOT DECIDED. The ship decision is
Magnus's** (recommendation in the s36 coordination block, 09:17Z). This file
exists so that if the call comes, the two-clock cert has its first clock and
nothing is written after the fact.

## WHAT SHIPS
`bots/_v197mapcode` — the 10 rotation maps encoded into EXTRA_MAP_CODES.
**Pure data: 18 lines in doctrine.py, zero code-path changes.** vs the live
holder v123 (`_v187saltidle_f`): that diff and nothing else.

## THE CASE
* Mechanism proven and reversed locally: builder livelock on table-missing maps
  (98.7% move-reversals, 9 actions/1000 rounds) → kills at turns 71/115/86 on
  midgard/ragnarok/yulerune vs starter; oscillation → 11.0%; 0 TLE of 3,725
  unit-turns. Encoder selftest reproduces 5 old-pool entries byte-for-byte.
* Field bleed being repaired: v123 today reads 2/8 (25%) on 900-area rated
  games vs 24/32 (75%) elsewhere; 900-area is ~1/3 of draws.
* Old-map non-regression premise: NO key equals any pre-existing entry, so
  behaviour on every previously-known map is unchanged by construction (the
  candidate filter is exact-key). Side lane note c0a0224 carries the premise
  audit.
* SHIP_SIT satisfied: v123 at k≥9 with its single pre-committed look taken
  (HOLD, certified). Displacement is programme-legal without a stop-loss.

## PRECONDITIONS FOR ACTIVATION (all must hold at ship time)
1. **The MAPCODE live leg (PREREG-mapcode-live-2026-08-13.md) ran and is
   CLEAN on its own falsifier**: zero crash-class losses, and no 900-area game
   showing the old signature. If the leg was not fired, this prereg's case is
   local-only and the ship needs Magnus's explicit override of that fact.
2. Holder read live in the ship command (submit_clean does this).
3. `--name "Loki v8"` + `--activate`; INCUMBENT rewrite by submit_clean,
   PROGRAMME.md committed with the ship commit.

## THE BAR — the amended scheme, unchanged from v122/v123
Primary `game_share`. Roll back if EITHER fires at k≥8:
1. `net5 <= -21` (rolling) — quote **fa_union** at read-out (now on the
   ship_watch line itself: 0.239 @ k=8), never `p_null`.
2. Cumulative Elo since activation `<= -21` (live tape, not the lagging
   ledger — the two-clocks rule).
3. At k≥24: pooled share below v123's baseline (0.650 at its k=8 look;
   lifetime TBD at ship time) by more than one pooled SE.
4. IMMEDIATE at any n: crash/timeout regression.
**ONE scoring look at k=8. Progress reportable, never readable as a result.
At k=8 only a disaster is detectable (LR(HOLD)=0.77 vs a 5pp regression —
audit M3); the honest gloss is pre-written here so it cannot be softened
after a favourable partial.**

## LOCAL BATTERY DISCLOSURE
MAPCODE (vs v123, live pool, n=5,400) will be PARTIAL at any same-day ship.
Its pre-registered looks (interim n=2,700 outside 47.31–52.69, final n=5,400)
are unchanged by the ship; a partial state may be reported descriptively
beside the ship, never as a verdict. The 30x30 kill evidence above is from
dedicated verification games, not from this battery.

## ROLLBACK
Target: `bots/_v187saltidle_f` (v123). Deeper: `bots/_v178salt` (v122).

---

# AMENDMENT 1 — ADD-ONLY (side lane audit, pre-decision). Two estimator pins.
1. **Trigger 3's baseline, NAMED:** v123's LIFETIME game share, computed AT
   SHIP TIME from `corpus/ladder_games.tsv` rows since its 06:06:27Z
   activation (per-match ourver=123, games won / games played). The 0.650/n=40
   k=8 figure is CONTEXT ONLY and is not the bar's estimator.
2. **The MAPCODE battery's interim look (n=2,700) is CONDITIONAL on the
   NULL123 live-pool calibration having landed and re-centred the bands.** If
   NULL123 has not reached its own n by then, the interim read is DESCRIPTIVE
   ONLY — the 47.31–52.69 band is old-pool noise width and certifies nothing
   on new-pool geometry.
