# LIVE: **v123 = `bots/_v187saltidle_f`** = **"Loki v7"** — shipped 06:06:27Z (s35).
# ⛔ **VERIFY WITH `fcode status | grep 'Active bot:'` BEFORE ACTING ON THIS LINE.**
# **THREE HOLDERS ON 2026-08-13: v116 → v122 (04:45:54Z) → v123 (06:06:27Z).**
# At wrap (~07:5xZ): rating **1641**, **5 matches, 19/25 games (0.760), +43.45 Elo**,
# **ZERO leaked rated matches** across both ships (per-match `ourver`, not the poll tag).

## ===== ⛔⛔ FIRST THING: THE MAP POOL ROTATED TODAY AND IT INVALIDATES HALF OUR EVIDENCE =====
##   The organisers moved to a **15-map pool**. **FOUR of our eight battery maps —
##   atoll, heart, hive, meander — ARE RETIRED.** Eleven of the fifteen had **zero
##   games in any battery**. `tools/overnight.sh` is **re-pointed at the live pool**;
##   targets must now be multiples of **30** (15 maps x 2 seats), not 16.
##   ⚠ **THE EIGHT ARMS RUNNING AT WRAP KEEP THE OLD SET** (the array is assigned once
##   at startup, so they stay internally consistent). **Their verdicts need a map
##   caveat: half their maps no longer appear.**
##   ⭐ **NEW SIZE CLASS: five 30x30 maps (area 900) against a previous maximum of 625.**

## ===== ⛔ WE CANNOT KILL ON THE 30x30 MAPS — MEASURED, THREE DOCTRINES =====
##   vs `bots/starter` (a WEAK bot) on the five 900s: **Loki v123 1 kill of 5 · Eir v94
##   1 of 5 and LOSES two · Thor v116 1 of 5.** Three designs ~50 versions apart, same wall.
##   **MECHANISM, banked over 18 games:** maps <=625 → **94 Ti banked, 27.2 buildings,
##   8/8 kills**; maps at 900 → **4,805 banked, 21.6 buildings, 3/10 kills**, one cell
##   finishing on **0 titanium mined in 1,000 rounds**. **We are not too slow. We are
##   rich and idle.** `doctrine.py` references map size **ZERO times**; every cap is an
##   absolute integer (`MAX_BUILDERS 5`, `LOKI_MAX_BUILDERS 11`, `LOKI_FWD_GUN_CAP 3`,
##   `ECO_CAP 18`) and `eco.py:372` gates harvester sync on `d^2<=64` — **58% of
##   fjordgate, 6.4% of midgard, the same 58 tiles on every map.**
##   ⇒ **THE FIX IS NOT STARTED, DELIBERATELY:** a map-area scale factor behind a flag
##   (`self.mw`/`self.mh` are already set in every unit init and unused), flag-off
##   verified behaviour-identical, tested on the NEW pool.

## ===== ⭐ PROGRAMME CHANGE, MAGNUS 2026-08-13 =====
##   **`R1000_IS_DEFEAT: conditional_on_map_area` + `R1000_DEFEAT_AREA_MAX: 676`.**
##   At or below 676 a r1000 finish is still a DEFEAT; above it (the five 30x30s) it is
##   an **admissible win**. ⚠ **Does NOT revive the tiebreak on the 10 maps <=676:**
##   controlled for rating gap we win **49.9%** of r1000 games vs **52.5%** of short ones.

## ===== THE QUEUE, IN PRIORITY ORDER =====
##   1. **MAP-AREA SCALING** — the 30x30 fix above. Highest value on the board.
##   2. **BOOT CHECK: pool vs battery set.** `fcode maps list` is one call and **no boot
##      sequence has ever made it**; that is why today happened.
##   3. **`ship_ledger.py` has an UNBACKED CLAIM** — `tools/claim_check.py` fires on it.
##      Commit the record or drop the claim.
##   4. **Read the local arms at their PRE-REGISTERED looks only** — interim n=2,704
##      (stop only outside **47.31-52.69%**), final n=5,408 (band **48.66-51.34%**).
##      O'Brien-Fleming; the naive two-look scheme measured alpha **0.0831**.
##   5. **The rated slot has ONE look, at k=8**, pre-committed while the number was good.
##   6. Counter arms (`SALTCLEAR`/`SALTROUTE`) test the trunk fix on a base that is no
##      longer live; the bug they fix is **NOT salt-specific** (the non-salting control
##      triggered it MORE often).

## ===== ROLLBACK =====
##   `bots/_v178salt` (v122). Deeper fallback `bots/_v169launchlate160` (v116).
##   Bars in `docs/prereg/SHIP-saltidle-v187-2026-08-13.md`.

# LIVE: **v116 = `bots/_v169launchlate160`** — Magnus rolled back x3r0's v120 at ~19:40Z.
# ⛔ **VERIFY WITH `fcode status | grep 'Active bot:'` BEFORE ACTING ON THIS LINE.**
# ⛔ **FIVE HOLDERS CHANGED ON 2026-08-12: v114 → v115 → v116 → v120 (x3r0) → v116.**

## ===== ARCHIVE =====
Everything superseded lives in `HANDOVER-archive.md` (boot-load audit cut 1,
executed 2026-08-13: a whole-file boot read measured ~34k tokens and regrew
after a one-time trim, so the bound is structural now). AT WRAP: rewrite the
top block above and MOVE what it replaces into the archive file — do not let
this file grow back. The top block IS the state; the archive is history.
